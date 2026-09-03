# 实测陷阱与数据源差异

以下结论全部来自对 algorithm-aide-pro 0001473 的实测。

## 实时缓冲 vs 落盘数据库

| 工具 | 数据源 | 全新目标行为 |
|------|--------|-------------|
| `list_logs` / `search_logs` / `get_log_graph` | 内存实时缓冲 | 正常返回 |
| `get_log` / `get_logs` / `get_log_total` | 落盘数据库 | `{}` / `[]` / `{"total":0}` |
| `list_databases` | 落盘数据库 | `[]` |
| `clear_logs` | 落盘数据库 | `{"success":false}` |
| `app_importScript` | 文件系统 | `false` |

全新目标（未在算法助手 Pro App 内配置过、无历史日志库）上，落盘类工具返回空。此时：

- 应用运行中产生的日志用 `list_logs` / `search_logs` / `get_log_graph` 采集
- 需要参数字节与调用栈时：先用 `list_logs`/`search_logs` 拿 logId，落盘工具为空则说明该目标无数据库，改从摘要 + `get_log_graph` 分析，并在结论中注明数据源
- `app_importScript` 返回 `false` 时：先在算法助手 Pro App 内为目标应用完成一次配置（生成工作区），再重试

## 启动与运行时序

- `app_start` 返回 `success:true` 是"已发起启动"；`service_appIsRunning` 要等数秒才变 `true`，不要立即判定启动失败
- `app_start` 对已运行应用先强停再启动（响应含 `wasRunning` / `forceStopped`）

## Hook 重量

- Hook `java.lang.String.toString` 这类超高频方法 + 总开关开启，会导致目标应用启动即死（实测：应用无法保持运行，清空 hookList 后恢复正常）
- 自定义 Hook 从低频业务方法开始；算法分析优先用内置开关（`digestSwitch` 等）而不是手工 Hook

## 配置语义

- `app_setConfig` 是合并：`configData` 中 absent 的字段保留；清空数组字段需显式传空值（`"hookList":[]`）
- `app_getConfig` / `app_getScript` 返回的是 JSON/源码**字符串**，需二次解析
- `enable_script` 只写 `enableScript` 配置值，不校验脚本存在性；启用一个脚本会关闭其他脚本
- `app_deleteScript` 对不存在的脚本也返回 `true`
- `service_getConfigItem` 对不存在的键返回 `""`（不是 null/error）

## 错误处理

- 缺少必填参数等错误：`isError:true` + text 为 `{"error":"No value for logId","stackTrace":"org.json.JSONException: ..."}`，按 error 信息修正参数即可
- 会话丢失（`Mcp-Session-Id` 失效）：重新 `initialize` 建立新会话
