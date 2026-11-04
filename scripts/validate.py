#!/usr/bin/env python3
"""校验 tokens.json 是否符合 AGENTS.md 的数据约定。

用法：
    python3 scripts/validate.py              # 校验仓库根目录的 tokens.json
    python3 scripts/validate.py 路径.json     # 校验指定文件
    python3 scripts/validate.py --today 2026-11-04   # 指定"今天"（测试用）

只用 Python 标准库，不需要安装任何东西。
有错误时退出码为 1（CI 会显示红叉），只有提醒时退出码为 0。
"今天"默认按北京时间（UTC+8）算，和本人看页面时的日期一致。
"""

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path

FIELDS = [
    "name",
    "type",
    "amount",
    "link",
    "claimed_date",
    "expire_date",
    "status",
    "notes",
]
REQUIRED = FIELDS[:-1]  # notes 可省略
TYPES = {"free-token", "discount", "trial"}
STATUSES = {"unclaimed", "active", "used-up", "expired"}
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
WARN_DAYS = 7
UTC8 = dt.timezone(dt.timedelta(hours=8))


def parse_date(value):
    if not isinstance(value, str) or not DATE_RE.match(value):
        return None
    try:
        return dt.date.fromisoformat(value)
    except ValueError:
        return None


def check_record(i, rec, today, errors, warnings):
    where = f"第 {i + 1} 条"
    if not isinstance(rec, dict):
        errors.append(f"{where}：不是对象（{{...}}）")
        return
    name = rec.get("name")
    if isinstance(name, str) and name:
        where = f"第 {i + 1} 条「{name}」"

    keys = list(rec.keys())
    extra = [k for k in keys if k not in FIELDS]
    missing = [k for k in REQUIRED if k not in rec]
    if extra:
        errors.append(f"{where}：有约定以外的字段 {extra}（规则 3：不得自创字段）")
    if missing:
        errors.append(f"{where}：缺少必填字段 {missing}")
    expected_order = [k for k in FIELDS if k in rec]
    if not extra and keys != expected_order:
        errors.append(f"{where}：字段顺序应为 {expected_order}，实际是 {keys}")

    for key in ("name", "type", "amount", "link", "status"):
        if key in rec and (not isinstance(rec[key], str) or not rec[key].strip()):
            errors.append(f"{where}：{key} 必须是非空字符串")
    if "notes" in rec and not isinstance(rec["notes"], str):
        errors.append(f"{where}：notes 必须是字符串（没有备注就写 \"\"）")

    if rec.get("type") not in TYPES and isinstance(rec.get("type"), str):
        errors.append(f"{where}：type「{rec['type']}」不在 {sorted(TYPES)} 里")
    if rec.get("status") not in STATUSES and isinstance(rec.get("status"), str):
        errors.append(f"{where}：status「{rec['status']}」不在 {sorted(STATUSES)} 里")

    link = rec.get("link")
    if isinstance(link, str) and not link.startswith("https://"):
        errors.append(f"{where}：link 必须以 https:// 开头")

    dates = {}
    for key in ("claimed_date", "expire_date"):
        if key not in rec:
            continue
        value = rec[key]
        if value is None:
            dates[key] = None
            continue
        parsed = parse_date(value)
        if parsed is None:
            errors.append(f"{where}：{key}「{value}」不是合法的 YYYY-MM-DD 日期（不填就写 null）")
        dates[key] = parsed

    claimed, expire = dates.get("claimed_date"), dates.get("expire_date")
    status = rec.get("status")
    if claimed and expire and claimed > expire:
        warnings.append(f"{where}：领取日期 {claimed} 晚于过期日期 {expire}，是不是写反了？")
    if status == "unclaimed" and claimed:
        warnings.append(f"{where}：状态是「未领取」，但填了领取日期 {claimed}")
    if status in ("active", "used-up") and "claimed_date" in rec and rec["claimed_date"] is None:
        warnings.append(f"{where}：状态是「{status}」，但领取日期是 null")
    if expire:
        left = (expire - today).days
        if left < 0 and status != "expired":
            errors.append(
                f"{where}：{expire} 已过期 {-left} 天，status 应改为 expired（规则 5）"
            )
        elif left >= 0 and status == "expired":
            warnings.append(f"{where}：status 是 expired，但过期日期 {expire} 还没到")
        elif 0 <= left <= WARN_DAYS and status in ("unclaimed", "active"):
            warnings.append(f"{where}：还剩 {left} 天到期（{expire}），记得用掉")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="校验 tokens.json")
    parser.add_argument("path", nargs="?", default=None)
    parser.add_argument("--today", help="把这一天当作今天，格式 YYYY-MM-DD")
    args = parser.parse_args()

    path = Path(args.path) if args.path else Path(__file__).resolve().parent.parent / "tokens.json"
    if args.today:
        today = parse_date(args.today)
        if today is None:
            print(f"--today「{args.today}」不是合法日期")
            return 2
    else:
        today = dt.datetime.now(UTC8).date()

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(f"找不到文件：{path}")
        return 1
    except json.JSONDecodeError as exc:
        print(f"❌ {path.name} 不是合法 JSON：第 {exc.lineno} 行第 {exc.colno} 列，{exc.msg}")
        return 1

    errors, warnings = [], []
    if not isinstance(data, list):
        errors.append("最外层必须是 JSON 数组 [ ... ]")
    else:
        names = {}
        for i, rec in enumerate(data):
            check_record(i, rec, today, errors, warnings)
            if isinstance(rec, dict) and isinstance(rec.get("name"), str):
                names.setdefault(rec["name"], []).append(i + 1)
        for name, rows in names.items():
            if len(rows) > 1:
                warnings.append(f"「{name}」出现了 {len(rows)} 次（第 {rows} 条），是不是重复录入？")

    count = len(data) if isinstance(data, list) else 0
    print(f"校验 {path.name}：共 {count} 条记录，今天按 {today} 算")
    for msg in errors:
        print(f"  ❌ {msg}")
    for msg in warnings:
        print(f"  ⚠️  {msg}")
    if errors:
        print(f"未通过：{len(errors)} 处错误，{len(warnings)} 处提醒")
        return 1
    print(f"通过：0 处错误，{len(warnings)} 处提醒")
    return 0


if __name__ == "__main__":
    sys.exit(main())
