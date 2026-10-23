# Free-token · AI 平台免费/优惠额度记录册

统一记录各家 AI 平台（OpenAI、Anthropic、智谱、DeepSeek、通义、Kimi 等）的**免费 Token、折扣、试用额度**，集中管理有效期，避免错过薅羊毛的最佳时机。

## 功能

- 数据统一存放在 `tokens.json`，一条记录对应一个平台的额度/优惠
- `index.html` 自动读取 `tokens.json` 渲染成表格：
  - 按**过期时间升序**排列，最紧急的排最前
  - **7 天内到期**的条目整行标红
  - **已过期**的条目灰色置底

## 本地查看

由于浏览器对 `file://` 协议的 fetch 有限制，请通过本地 HTTP 服务打开：

```bash
python3 -m http.server 8000
# 浏览器访问 http://localhost:8000
```

## 数据维护

额度数据的增删改全部在 `tokens.json` 中进行，字段格式与约定见 [AGENTS.md](AGENTS.md)。
