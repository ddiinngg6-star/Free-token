# AGENTS.md

本项目是「AI 平台免费/优惠额度记录册」，统一记录各家 AI 平台的免费 token、折扣、试用额度。

## 项目结构

```
.
├── README.md      # 项目介绍（面向人类读者）
├── tokens.json    # 额度数据，唯一数据源，所有增删改只动这个文件
├── index.html     # 展示页，运行时 fetch tokens.json 渲染表格（无需构建）
└── AGENTS.md      # 本文件，结构与数据约定
```

## 数据格式约定（tokens.json）

顶层为 JSON 数组，每个对象代表一条额度记录，**字段顺序固定如下，缺失字段写 `null`，不得增删改名**：

| 字段 | 类型 | 必填 | 约定 |
| --- | --- | --- | --- |
| `name` | string | 是 | 平台/活动名称，如 `智谱 AI 新用户注册礼` |
| `type` | string | 是 | 枚举：`free`（免费额度）/ `trial`（试用）/ `discount`（折扣） |
| `amount` | string | 是 | 额度数量或折扣力度，如 `1000000 tokens`、`5 折` |
| `link` | string | 否 | 完整 URL（含 https://），无则填 `null` |
| `claimed_date` | string | 否 | 领取日期，格式 `YYYY-MM-DD`，未知填 `null` |
| `expire_date` | string | 否 | 过期日期，格式 `YYYY-MM-DD`；永久有效填 `null` |
| `status` | string | 是 | 枚举：`active`（生效中）/ `used-up`（已用完）/ `cancelled`（已取消） |
| `notes` | string | 否 | 备注，可写限制条件（限新用户、指定模型等），无则填 `null` |

### 硬性规则

1. **日期一律 `YYYY-MM-DD`**，不写时间、不写 `YYYY/MM/DD`、不写相对日期（"下个月底"需换算成具体日期）。
2. **过期状态由页面根据 `expire_date` 与当前日期自动计算**，不要因为过期就手动改 `status`；`status` 只表示人工维护的领取/使用状态。
3. 数组**不要求按日期预排序**（页面运行时排序），但新增记录统一**追加到数组末尾**，便于 diff 审查。
4. 修改数据时**只改 `tokens.json`**，不要把数据写死进 `index.html`；页面逻辑（排序、7 天标红、过期置底）无需随数据变动。
5. 删除记录 = 整个对象从数组移除；改字段 = 原地修改，保持字段顺序。

## 展示逻辑（index.html 已实现，一般无需改动）

- 有效记录按 `expire_date` 升序，`expire_date` 为 `null`（永久）的排最后
- 距过期 ≤ 7 天：整行标红并显示剩余天数
- 已过期（`expire_date` < 今天）：整行灰色、划线、置底
- 本地预览需起 HTTP 服务：`python3 -m http.server 8000`（直接双击打开会因 file:// 协议无法 fetch）
