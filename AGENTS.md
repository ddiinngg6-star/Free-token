# AGENTS.md

AI 平台免费/优惠额度记录册。本文件是本仓库的约定文档：后续让 AI 增删改数据时，**必须严格遵守本文件的格式与规则**。

## 项目结构

```
.
├── README.md      # 项目介绍
├── tokens.json    # 额度数据（唯一数据源，增删改都在这里）
├── index.html     # 展示页，读取 tokens.json 渲染表格
└── AGENTS.md      # 本文件：项目结构与数据格式约定
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
2. **保持 JSON 合法**：改完必须能通过 `JSON.parse`（或 `python3 -m json.tool tokens.json`）校验。
3. **不得自创字段**：字段名严格按上表，多余的键一律不加。
4. **日期格式一律 `YYYY-MM-DD`**，不使用时间戳或其他格式。
5. **`status` 与 `expire_date` 保持一致**：`expire_date` 早于今天的记录，`status` 必须为 `expired`。
6. **新增记录追加到数组末尾**（页面展示时另行排序，存储顺序不影响展示）。

## 展示规则（index.html 的实现依据）

- **排序**：按过期时间升序，最紧急的排最前；`expire_date` 为 `null`（长期有效）的排未过期组末尾；**已过期的灰色置底**（过期组内部按过期时间降序，最近过期的靠前）。
- **整行标红**：距过期 0–7 天（含当天）的记录整行标红。
- **灰色置底**：`expire_date` 早于当天的记录整行灰色并移到表格底部。
- 以上判定均以**打开页面时的当前日期**与 `expire_date` 比较，`status` 字段仅作展示徽标。

## 验证方式

改完数据后，在仓库根目录起本地服务确认渲染正常：

```bash
python3 -m http.server 8000
# 浏览器打开 http://localhost:8000
```

注意：直接双击 `index.html`（`file://` 协议）会被浏览器拦截 fetch，无法读取 JSON，属正常现象。
