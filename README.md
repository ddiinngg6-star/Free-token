# Free-token · AI 平台免费/优惠额度记录册

统一记录各家 AI 平台（OpenAI、Anthropic、智谱、DeepSeek、通义、Kimi 等）的**免费 Token、折扣、试用额度**，集中管理有效期，避免额度白白过期。

> 这是**公开仓库**，页面也公开。只记录额度本身，不要提交 API Key、账号密码等个人信息。

## 功能

- 数据统一存放在 `tokens.json`，一条记录对应一个平台的额度/优惠
- `index.html` 自动读取 `tokens.json` 渲染成表格：
  - 按**过期时间升序**排列，最紧急的排最前
  - **7 天内到期**的条目整行标红
  - **已过期**的条目灰色置底
  - 支持手机（表格左右滑动）和深色模式
- `scripts/validate.py` 按 [AGENTS.md](AGENTS.md) 的规则校验数据；推送到 GitHub 时自动运行

## 在线查看

仓库开了 GitHub Pages，`main` 分支更新后自动发布：<https://ddiinngg6-star.github.io/Free-token/>
（如果打不开，到仓库 Settings → Pages 看实际网址。）

## 本地查看

由于浏览器对 `file://` 协议的 fetch 有限制，请通过本地 HTTP 服务打开：

```bash
python3 -m http.server 8000
# 浏览器访问 http://localhost:8000
```

## 怎么加一条记录

三种方式任选：

1. **直接改** `tokens.json`，在数组末尾追加一条，然后运行 `python3 scripts/validate.py` 确认「通过」。
2. **让 GitHub 上的机器人改**：新建一个 issue，留言 `/oc 添加：××平台，××额度，××日到期，领取链接 https://…`，机器人会开一个 PR，检查变绿后合并即可。
3. **让 Claude Code / 其他 AI 助手改**：它们会读 `AGENTS.md` 里的规则。

字段格式与约定见 [AGENTS.md](AGENTS.md)。

## 检查

```bash
python3 scripts/validate.py
```

只用 Python 标准库，不需要安装任何依赖。
