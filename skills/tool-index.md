# MCP 服务器检测结果

> 由 `scripts/test-tools.py --url <地址>` 刷新，勿手改。

- 检测时间: 2026-09-03 20:24:51
- 服务器地址: `http://192.168.8.104:8788/mcp`
- 服务: algorithm-aide-pro 0001473
- 协议版本: 2025-06-18
- 服务运行: true
- 已开启 Hook 的应用: []
- 可用工具: 34 个

| 工具 | 必填参数 |
|------|---------|
| `service_isRunning` | - |
| `service_getVersion` | - |
| `service_getVersionName` | - |
| `service_getConfigSize` | - |
| `service_clearConfig` | - |
| `service_getAppsWithSwitch` | - |
| `service_getConfigItem` | configName |
| `service_setConfigItem` | configName, configValue |
| `service_appIsRunning` | packageName |
| `service_forceStopApp` | packageName |
| `app_start` | packageName |
| `app_getConfig` | packageName |
| `app_listConfigOptions` | - |
| `app_setConfig` | packageName, configData |
| `app_getConfigItem` | packageName, configName |
| `app_setConfigItem` | packageName, configName, value |
| `app_addHook` | packageName, className, methodName |
| `app_isSwitch` | packageName |
| `app_setSwitch` | packageName, isSwitch |
| `scriptList` | packageName |
| `enable_script` | packageName, scriptName |
| `app_importScript` | packageName, name, jsCode |
| `app_deleteScript` | packageName, name |
| `app_getScript` | packageName, name |
| `list_databases` | - |
| `get_log_total` | packageName |
| `list_logs` | packageName |
| `search_logs` | packageName, text |
| `get_log` | packageName, logId |
| `get_log_graph` | packageName, logId |
| `get_logs` | packageName, logIds |
| `clear_logs` | packageName |
| `frida_get_log` | packageName |
| `frida_clear_log` | packageName |
