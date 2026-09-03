# MCP 协议与连接

## 服务器

- 名称：`algorithm-aide-pro`
- 传输：MCP Streamable HTTP（POST 单端点）
- 协议版本：`2025-06-18`
- 端点：`http://<设备IP>:8788/mcp`（地址由用户提供）

## 请求头

```
Content-Type: application/json
Accept: application/json, text/event-stream
Mcp-Session-Id: <initialize 返回>
```

## 会话流程

1. `initialize` → 响应头携带 `Mcp-Session-Id`，后续请求必须带上
2. `notifications/initialized` → 返回 202 空 body
3. `tools/list` / `tools/call`

```json
{"jsonrpc":"2.0","id":1,"method":"initialize","params":{
  "protocolVersion":"2025-06-18","capabilities":{},
  "clientInfo":{"name":"client","version":"1.0"}}}
```

```json
{"jsonrpc":"2.0","id":2,"method":"tools/call",
 "params":{"name":"service_isRunning","arguments":{}}}
```

## 响应格式

工具结果（成功与失败都是 `result`，无 JSON-RPC error 层）：

```json
{"jsonrpc":"2.0","id":2,"result":{
  "content":[{"type":"text","text":"true"}],
  "isError":false}}
```

失败时 `isError: true`，`text` 为 JSON 字符串：

```json
{"error":"No value for logId","stackTrace":"org.json.JSONException: ..."}
```

未知工具名同样以 `isError: true` + `{"error":"unknown tool: ..."}` 返回。

## 客户端

本包自带客户端，勿手写 HTTP：

```bash
python skills/scripts/aide.py --url http://192.168.8.104:8788/mcp ping
python skills/scripts/aide.py list
python skills/scripts/aide.py call list_logs '{"packageName":"com.example.app","page":0}'
```

或作为库：`from mcp import MCP; mcp = MCP("http://..."); mcp.call_text("service_isRunning")`
