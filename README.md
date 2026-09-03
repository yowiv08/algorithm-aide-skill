# 算法助手技能包 (Algorithm Aide Skill)

Android 动态分析技能路由包。通过 MCP 协议连接 [算法助手 Pro](#)（Android 端 HTTP-MCP 服务器），对运行中的 Android 应用做实时 Hook、算法分析、行为监听与日志采集。

静态分析、二进制逆向、前端逆向等非动态分析任务，路由到远程 [reverse-skill](https://github.com/zhaoxuya520/reverse-skill)。

## 结构

```
skills/
├── SKILL.md              # 总控入口：路由执行契约
├── routing.md            # 任务路由矩阵
├── INDEX.md              # 模块索引（自动生成，勿手改）
├── tool-index.md         # MCP 服务器检测结果（脚本刷新）
├── config/
│   └── routing.json      # 路由单一事实源
├── scripts/              # 跨平台 Python 工具
│   ├── mcp.py            # MCP 客户端库
│   ├── aide.py           # 命令行入口
│   ├── master-route.py   # 任务路由器
│   ├── extract-summaries.py  # INDEX.md 生成器
│   └── test-tools.py     # 服务器连通性测试
└── android-dynamic/      # 唯一本地模块：算法助手 Android 动态分析
    ├── SKILL.md          # 模块入口与工作流
    └── references/       # 分领域 API 参考（按需加载）
```

## 快速开始

1. Android 设备安装并启动算法助手 Pro，确认 MCP 服务器地址（如 `http://192.168.8.104:8788/mcp`）。
2. 连通性测试：

```bash
python skills/scripts/test-tools.py --url http://192.168.8.104:8788/mcp
```

3. 服务器地址写入环境变量后，命令行直接调用工具：

```bash
export ALGO_AIDE_URL=http://192.168.8.104:8788/mcp
python skills/scripts/aide.py list                      # 列出 34 个工具
python skills/scripts/aide.py call service_isRunning {} # 调用任意工具
```

4. AI Agent（Claude Code / Codex 等）从 [skills/SKILL.md](skills/SKILL.md) 进入，按路由契约执行。

## 路由

| 任务 | 目标 |
|------|------|
| Android 动态分析、实时 Hook、Frida 脚本、算法日志 | 本地 `skills/android-dynamic/` |
| APK 静态反编译、smali、重打包 | 远程 reverse-skill `apk-reverse` |
| so / ELF / IDA / Ghidra | 远程 reverse-skill `ida-reverse` 等 |
| 前端 JS 逆向、抓包 | 远程 reverse-skill `js-reverse` |
| 其他逆向 / 安全任务 | 远程 reverse-skill 总控 |

路由规则见 [skills/routing.md](skills/routing.md)，事实源为 `skills/config/routing.json`。

## 环境要求

- Python 3.10+（仅标准库，无第三方依赖）
- 算法助手 Pro（Android 端，MCP 服务器）
- 设备与执行机网络互通

## 许可

MIT
