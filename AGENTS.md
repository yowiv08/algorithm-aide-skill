# AGENTS.md — AI Agent 入口

任何 AI Agent（Codex、Cursor、Claude 等）处理 Android 逆向 / 动态分析 / Hook 类任务时，按以下顺序进入本包：

1. 读 `skills/SKILL.md`，执行路由契约，确定 PRIMARY。
2. Android 动态分析任务 → 打开 `skills/android-dynamic/SKILL.md`，按其工作流执行。
3. 其他逆向任务 → 按 `skills/config/routing.json` 中的远程路由，访问 reverse-skill 仓库（https://github.com/zhaoxuya520/reverse-skill）。
4. 作业规则（授权边界、破坏性操作、证据要求）见 `RULES.md`，对任何 Agent 生效。

MCP 服务器地址由用户提供，通过 `ALGO_AIDE_URL` 环境变量或 `--url` 参数传入，或直接从用户消息中读取。

连通性验证：

```bash
python skills/scripts/test-tools.py --url <服务器地址>
```
