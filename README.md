# Free-token · AI 平台免费/优惠额度记录册

统一记录各家 AI 平台（OpenAI、Anthropic、智谱、阿里云百炼等）的免费 token、折扣、试用额度，集中管理领取与到期情况，避免遗忘浪费。

## 功能

- 数据与展示分离：所有额度记录存放在 `tokens.json`，页面 `index.html` 读取后自动渲染成表格
- 按到期时间升序排列，最紧急的排最前
- **7 天内到期**的记录整行标红提醒
- **已过期**的记录灰色并置底

## 使用方法

`index.html` 通过 `fetch` 读取 `tokens.json`，直接双击打开（file:// 协议）会被浏览器拦截，请用本地服务器打开：

```bash
python3 -m http.server 8000
# 浏览器访问 http://localhost:8000
```

## 数据格式

每条记录字段如下（详见 `AGENTS.md`）：

| 字段 | 说明 |
| --- | --- |
| name | 平台/活动名称 |
| type | 类型：free（免费额度）/ trial（试用）/ discount（折扣） |
| amount | 额度数量或折扣力度，如 `1000000 tokens`、`5 折` |
| link | 活动或控制台链接 |
| claimed_date | 领取日期，`YYYY-MM-DD` |
| expire_date | 过期日期，`YYYY-MM-DD`，`null` 表示永久有效 |
| status | 状态：active（生效中）/ used-up（已用完）/ cancelled（已取消） |
| notes | 备注 |

## 项目结构

```
.
├── README.md      # 项目介绍
├── tokens.json    # 额度数据（唯一数据源）
├── index.html     # 展示页，读取 tokens.json 渲染
└── AGENTS.md      # 项目结构与数据格式约定
```
