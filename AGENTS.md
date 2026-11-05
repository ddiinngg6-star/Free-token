# AGENTS.md

AI 平台免费/优惠额度记录册。本文件是本仓库的约定文档：后续让 AI 增删改数据时，**必须严格遵守本文件的格式与规则**。

> - **这是公开仓库**：任何人都能看到全部文件和提交历史，页面也通过 GitHub Pages 公开。**绝不提交** API Key、账号密码、手机号等个人信息（活动链接里自带的邀请码可以）；Key 只放在仓库 Secrets 里。
> - Claude Code 通过同目录的 `CLAUDE.md`（内容只有 `@AGENTS.md`）读本文件；OpenCode 机器人直接读本文件。

## 项目结构

```
.
├── README.md                     # 项目介绍
├── tokens.json                   # 额度数据（唯一数据源，增删改都在这里）
├── index.html                    # 展示页，读取 tokens.json 渲染表格（无框架、无外部资源）
├── scripts/validate.py           # 按本文件规则校验 tokens.json（只用 Python 标准库）
├── AGENTS.md                     # 本文件：项目结构与数据格式约定
├── CLAUDE.md                     # 只有一行 @AGENTS.md，让 Claude Code 读本文件
├── .opencode/opencode.json       # OpenCode 机器人用的模型配置（智谱 GLM，Key 走环境变量）
└── .github/workflows/
    ├── opencode.yml              # 在 issue / PR 留言 /oc 或 /ocv 触发 OpenCode 机器人
    └── validate.yml              # 推送或开 PR 改到数据时自动跑 scripts/validate.py
```

## 数据格式（tokens.json）

`tokens.json` 是一个 **JSON 数组**，每个元素代表一条额度记录，字段固定如下（顺序也保持一致）：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `name` | string | 是 | 平台 / 活动名称，如 `智谱 AI 新用户礼包` |
| `type` | string | 是 | 枚举：`free-token`（免费 Token）/ `discount`（折扣）/ `trial`（试用额度） |
| `amount` | string | 是 | 额度描述，如 `2000 万 tokens`、`API 75 折` |
| `link` | string | 是 | 活动页面完整 URL，必须以 `https://` 开头 |
| `claimed_date` | string \| null | 是 | 领取日期，格式 `YYYY-MM-DD`；未领取填 `null` |
| `expire_date` | string \| null | 是 | 过期日期，格式 `YYYY-MM-DD`；长期有效填 `null` |
| `status` | string | 是 | 枚举：`unclaimed`（未领取）/ `active`（使用中）/ `used-up`（已用完）/ `expired`（已过期） |
| `notes` | string | 否 | 备注，默认为 `""` |

### 硬性约定

1. **只改 `tokens.json`**：增删改额度数据时不得改动其他文件，除非用户明确要求。
2. **保持 JSON 合法、改完跑校验**：改完必须运行 `python3 scripts/validate.py`，输出「通过」才算完成（它同时检查 JSON 语法、字段、枚举、日期格式和下面第 5 条）。
3. **不得自创字段**：字段名严格按上表，多余的键一律不加。
4. **日期格式一律 `YYYY-MM-DD`**，不使用时间戳或其他格式。
5. **`status` 与 `expire_date` 保持一致**：`expire_date` 早于今天的记录，`status` 必须为 `expired`。
6. **新增记录追加到数组末尾**（页面展示时另行排序，存储顺序不影响展示）。
7. **用户给的信息原样录入**：日期、额度、链接以用户说的为准，不自行推算或「纠正」；觉得可疑（比如「周卡」却一年后才过期）就在回复里问，不擅自改。
8. **到期顺手更新**：发现 `expire_date` 已过、`status` 还不是 `expired` 的记录，改成 `expired`（这是第 5 条，校验脚本会报错）；用完了的改 `used-up`。不删除旧记录，留作历史。

## 展示规则（index.html 的实现依据）

- **排序**：按过期时间升序，最紧急的排最前；`expire_date` 为 `null`（长期有效）的排未过期组末尾；**已过期的灰色置底**（过期组内部按过期时间降序，最近过期的靠前）。
- **整行标红**：距过期 0–7 天（含当天）的记录整行标红。
- **灰色置底**：`expire_date` 早于当天的记录整行灰色并移到表格底部。
- 以上判定均以**打开页面时的当前日期**与 `expire_date` 比较，`status` 字段仅作展示徽标。

## 验证方式

改完数据后先跑校验（GitHub 上也会自动跑，见 `.github/workflows/validate.yml`）：

```bash
python3 scripts/validate.py                      # 输出「通过」才算完成
python3 scripts/validate.py --today 2026-12-01   # 假装今天是某天，看到时候会不会报过期
```

改了 `index.html` 时，再在仓库根目录起本地服务确认渲染正常（手机宽度下表格应能左右滑、页面本身不横向滚动）：

```bash
python3 -m http.server 8000
# 浏览器打开 http://localhost:8000
```

注意：直接双击 `index.html`（`file://` 协议）会被浏览器拦截 fetch，无法读取 JSON，属正常现象。

## 页面的约定（改 index.html 时）

- 单文件、原生 HTML/CSS/JS，不引入框架、CDN、外部字体或图片。
- 日期一律按本地日期解析（`localDayMs`），不要用 `Date.parse("YYYY-MM-DD")`（会被当成 UTC 零点）。
- 颜色都用 `:root` 里的变量，深色模式在 `@media (prefers-color-scheme: dark)` 里覆盖；新加颜色两套都要写。
- 展示规则改了，要同步改本文件「展示规则」一节。

## OpenCode 机器人（GitHub 上留言干活）

- 在 issue 或 PR 里留言 `/oc 要做的事`（或 `/opencode`），机器人用智谱 GLM-5.3 改仓库并开 PR；`/ocv` 用能看图的 GLM-5.3-Flash。
- **只有仓库主人和协作者的留言会触发**（`opencode.yml` 里按 `author_association` 判断）。公开仓库里陌生人也能留言，没有这道门槛会被人白用智谱额度、往仓库里塞东西。不要去掉。
- 需要仓库 Secret `ZHIPU_API_KEY`；Key 失效时机器人会失败，到 Settings → Secrets and variables → Actions 更新。
- 机器人开的 PR 要等 `validate` 检查变绿再合并。
