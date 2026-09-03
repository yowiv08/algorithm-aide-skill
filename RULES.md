# RULES — 算法助手技能包作业规则

## 授权边界

- 仅分析自己拥有或已获得明确授权的设备与应用。
- 目标应用、设备、服务器地址三者必须由用户明确给出，禁止猜测后直接操作。
- `service_clearConfig`、`clear_logs`、`frida_clear_log`、`app_deleteScript`、`service_forceStopApp` 属于破坏性操作：执行前必须说明影响对象，得到确认。

## 工具调用纪律

- 服务器地址只能来自用户配置（环境变量 `ALGO_AIDE_URL`、`--url` 参数或用户消息），禁止硬编码到任何 skill 文档或脚本默认值之外的地方。
- 调用工具前先 `tools/list` 校验工具名与参数，禁止凭记忆猜测参数结构。
- 工具返回 `isError: true` 或 `{"error": ..., "stackTrace": ...}` 时，按错误信息修正参数后重试，不要换工具绕过。
- 落盘类工具（见 `skills/android-dynamic/references/pitfalls.md`）依赖目标应用已存在日志数据库；全新目标返回空结果不代表无日志，应改用实时类工具。

## 证据要求

- 分析结论必须附带日志 ID（`logId`）、工具名与关键返回字段，可复现。
- 算法还原必须以 `get_log` 的参数字节与返回值为证据，不得只凭 `desc` 摘要下结论。

## 完成自检

- [ ] 使用的是真实服务器地址，且 `service_isRunning` 为 `true`
- [ ] 每个结论都有 logId / 工具返回支撑
- [ ] 破坏性操作均已获得确认
- [ ] 测试产生的临时配置、脚本已清理，设备状态已恢复
