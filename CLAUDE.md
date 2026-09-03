# CLAUDE.md — Claude Code 入口

- 本仓库是技能路由包，不包含可构建的工程代码；核心内容在 `skills/`。
- 处理 Android 动态分析 / Hook / Frida 实时分析任务：读 `skills/SKILL.md` → `skills/android-dynamic/SKILL.md`。
- 处理静态逆向等其他任务：按 `skills/config/routing.json` 的远程路由转交 reverse-skill（https://github.com/zhaoxuya520/reverse-skill）。
- MCP 服务器地址从用户消息或 `ALGO_AIDE_URL` 读取；调用工具用 `python skills/scripts/aide.py`，勿手写 HTTP 请求。
- `skills/INDEX.md` 由 `python skills/scripts/extract-summaries.py` 生成，勿手改。
- 作业规则见 `RULES.md`；破坏性工具调用前必须确认。
