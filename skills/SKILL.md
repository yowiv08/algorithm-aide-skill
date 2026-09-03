---
name: algorithm-aide-router
description: 将 Android 动态分析、实时 Hook、Frida 脚本管理、算法日志采集任务路由到本地 android-dynamic 模块；静态逆向、二进制分析、前端逆向等其他逆向任务路由到远程 reverse-skill。任务跨模块或入口不明时使用本文件。
---
# 算法助手技能总控

本目录是一个技能路由包：一个本地模块（Android 动态分析）+ 一组远程委托路由（reverse-skill）。

## 路由执行契约（读完立即执行）

不允许只回复"已读/已理解"。按顺序执行：

1. `NOW`：跑路由器确定 PRIMARY：

```bash
python skills/scripts/master-route.py "<任务描述>"
```

2. `NOW`：PRIMARY 为本地模块时，确认 MCP 服务器地址（用户提供 / `ALGO_AIDE_URL`），并执行连通性检查：

```bash
python skills/scripts/test-tools.py --url <服务器地址>
```

3. `ACT`：打开 PRIMARY 模块的 `SKILL.md` 并执行其工作流，不要停在确认状态。
4. `NEXT`：PRIMARY 为远程路由时，访问 reverse-skill 仓库对应模块（`https://github.com/zhaoxuya520/reverse-skill`），以其文档为准；本包不复制其内容。
5. 结论遵循 `RULES.md` 的证据要求：结论必须附带 logId / 工具返回。

路由无法命中时回退 `R0`（reverse-skill 总控），禁止把任务硬塞进不匹配的模块。

## 当前模块

| 模块 | 目录 | 适用场景 |
|------|------|---------|
| **Android 动态分析** | `android-dynamic/` | 算法助手 Pro MCP 全部 34 工具：实时 Hook、算法分析（哈希/加解密/HMAC）、行为监听、Frida 脚本管理、日志采集与依赖图 |

## 远程委托（reverse-skill）

以下任务不在本包能力范围内，委托给远程 [reverse-skill](https://github.com/zhaoxuya520/reverse-skill)：

| 任务 | 远程目标 |
|------|---------|
| APK 静态反编译、smali 修改、重打包 | `skills/apk-reverse/` |
| so / ELF / PE 静态分析（IDA、Ghidra、radare2） | `skills/ida-reverse/`、`skills/ghidra-reverse/`、`skills/radare2/` |
| iOS / 移动通用逆向 | `skills/mobile-reverse/` |
| 前端 JS 逆向、抓包、请求重放 | `skills/js-reverse/` |
| 渗透、恶意软件分析、CTF 等 | reverse-skill 总控 `skills/SKILL.md` |

## 分工原则

- 动态分析（应用运行时观察/干预）→ 本包 `android-dynamic/`
- 静态分析（不运行目标、看代码/二进制）→ 远程 reverse-skill
- 完整 Android 逆向流程：reverse-skill 静态定位目标 → 本包动态 Hook 验证 → 日志证据落结论

## 统一入口

遇到逆向、Hook、算法分析、抓包类任务时，按顺序进入：

1. `scripts/master-route.py "<任务>"` → PRIMARY（依据 `config/routing.json`）
2. 本地模块：连通性检查 → 模块 `SKILL.md`
3. 远程路由：reverse-skill 仓库对应模块
4. 疑难时读 `routing.md`，服务器状态不明时读 `tool-index.md`
