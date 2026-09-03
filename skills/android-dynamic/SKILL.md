---
name: android-dynamic
description: 通过算法助手 Pro（Android 端 MCP 服务器）做 Android 动态分析时使用。适用于实时 Hook、算法分析（哈希/HMAC/加解密）、行为监听、Frida 脚本管理、应用控制与算法日志采集。服务器地址由用户提供。
---
## ACTION REQUIRED（读完后立刻执行）

1. `NOW`: 确认 MCP 服务器地址（用户消息 / `ALGO_AIDE_URL`），执行 `python skills/scripts/test-tools.py --url <地址>`；`service_isRunning` 不为 `true` 时停止并报告。
2. `NOW`: 确认目标包名与任务（Hook 哪个方法 / 采集哪类算法日志）。
3. `NEXT`: 按需读 references/（协议 → 对应 API 文档），不要一次全读。
4. `ACT`: 进入"工作流"第一步并执行，不要停在确认状态。

# Android 动态分析作业规范（算法助手 Pro）

## 适用范围

- 分析运行中应用的加密/签名算法（MD5、HMAC、加解密、WebView 加解密库）
- 实时 Hook 指定类/方法，采集参数与返回值
- 行为监听：文件、Shell、SharedPreferences、SQLite、点击、Activity、弹窗
- Frida 脚本导入、启用、日志读取
- 目标应用启动 / 强停 / 开关 Hook 总开关

不在范围（路由到远程 reverse-skill，见 `../routing.md`）：APK 静态反编译、so/ELF 静态分析、iOS、前端 JS 逆向。

## 服务器

- 算法助手 Pro 运行于 Android 设备，暴露 MCP Streamable HTTP 端点（默认端口 8788）
- 地址由用户提供；协议细节见 [references/mcp-protocol.md](references/mcp-protocol.md)
- 验证：`python skills/scripts/test-tools.py --url <地址>`

## 工具分组（34 个，全部实测）

| 分组 | 数量 | 文档 |
|------|------|------|
| 服务管理 | 8 | [references/service-api.md](references/service-api.md) |
| 应用控制 + 应用配置 | 10 | [references/app-api.md](references/app-api.md) |
| Hook + Frida 脚本 | 6 | [references/hook-script-api.md](references/hook-script-api.md) |
| 日志 | 10 | [references/log-api.md](references/log-api.md) |

配置项全表（41 项：算法分析/设备环境/网络环境/行为监听/交互与界面/WebView 与数据库/存储与/Frida）见 [references/app-api.md](references/app-api.md#配置项全表)。

## 工作流

### 1. 检查服务

`service_isRunning` → `service_getVersion`。异常时停止，提示用户检查算法助手 Pro 与网络。

### 2. 确认目标

`service_getAppsWithSwitch`（已开 Hook 的应用）、`service_appIsRunning`（目标是否在运行）。目标未开过 Hook 时继续第 3 步。

### 3. 配置

- 按 `app_listConfigOptions` 的 41 项选择开关，`app_setConfigItem` 逐项设置或 `app_setConfig` 批量合并
- 自定义方法 Hook：`app_addHook`（只追加，不替换现有 Hook 列表）
- Frida 脚本：`app_importScript` → `enable_script`（见 pitfalls：全新目标可能导入失败）

### 4. 启动采集

1. `app_setSwitch` 开启目标应用 Hook 总开关
2. `app_start` 启动应用（已运行会先强停再启动）
3. 等待数秒后 `service_appIsRunning` 确认运行；应用未运行时检查是否配置了过重的 Hook（见 pitfalls）

### 5. 采集日志

- 实时：`list_logs`（分页，最新在前）、`search_logs`（字符串/hex/base64）、`get_log_graph`（上游数据流）
- 详情：`get_log` / `get_logs`（参数字节 base64 + 调用栈）——依赖日志数据库，全新目标不可用，见 pitfalls
- Frida 脚本输出：`frida_get_log`

### 6. 收尾

- 结论：算法名、输入输出字节（base64 解码后分析）、调用栈关键帧、logId
- 清理：`clear_logs` / `frida_clear_log`（破坏性，先确认）、`app_setSwitch` 关闭、临时脚本 `app_deleteScript`

## 输出要求

- 算法结论必须给出：方法名、输入参数（解码后）、输出（解码后）、logId
- Hook 配置变更必须列明：包名、类名、方法名、开关项
- 落盘与实时工具结果不一致时，按 pitfalls 判断原因并说明

## 禁止事项

- 禁止对未授权设备/应用操作；服务器地址禁止猜测
- 禁止一开始就 Hook 超高频方法（如 `java.lang.String.toString`），会导致应用启动即死
- 破坏性工具（clear/forceStop/deleteScript/clearConfig）未确认禁止执行
- 全新目标上 `get_log` 等落盘工具返回空 ≠ 无日志，禁止据此下"无数据"结论

## 路由上下文

**上游入口**: `../SKILL.md`（总控）、`../routing.md`
**下游出口**:
- 需要静态定位类名/方法名 → 远程 reverse-skill `apk-reverse`（jadx 反编译）
- 核心算法在 native so → 远程 reverse-skill `ida-reverse` / `ghidra-reverse`
**同级关联**: 远程 reverse-skill `mobile-reverse`（通用移动动态插桩，本模块为算法助手 Pro 专用）
