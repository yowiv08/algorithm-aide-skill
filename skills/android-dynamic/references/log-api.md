# 日志 API（10 工具）

日志分两类数据源（详见 [pitfalls.md](pitfalls.md)）：

- **实时缓冲**：`list_logs` / `search_logs` / `get_log_graph` —— 应用运行时随时可用
- **落盘数据库**：`get_log` / `get_logs` / `get_log_total` / `list_databases` / `clear_logs` —— 依赖目标应用已存在日志数据库

## list_logs

**功能**：读取一页日志摘要；`page` 从 0 开始，最新在前。

**请求**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| packageName | string | 是 | |
| page | integer | 否 | 页码，0 起 |
| group | string | 否 | `HASH` / `CIPHER` / `OTHER`；省略查全部分类 |

**响应**：摘要数组：

```json
[{"desc":"签名内容:bUbhX!Vv07&v0Iye17884273612990001",
  "id":2938,"methodName":"MD5","read":false,
  "returnValue":"签名结果:cc08c43de3a11c2a85bba518738e8f15",
  "size":943,"time":1788427361303,"type":15}]
```

## search_logs

**功能**：搜索日志并返回匹配摘要；支持搜索字符串、hex、base64。

**请求**：

| 参数 | 类型 | 必填 |
|------|------|------|
| packageName | string | 是 |
| text | string | 是 |
| group | string | 否 | 同 list_logs |

**响应**：匹配数组；`match` 为命中偏移，`desc` 为 `日志名称:<方法名>`：

```json
[{"desc":"日志名称:MD5\n\n","id":2972,"match":[5,8],
  "methodName":"MD5","read":false,
  "returnValue":"签名结果:dc077e8ed27e2f47b761fc89d04f2fd1",
  "size":943,"time":1788427406371,"type":15}]
```

## get_log

**功能**：读取单条日志完整详情：参数（名/类型/base64 字节）+ 调用栈。依赖日志数据库。

**请求**：

| 参数 | 类型 | 必填 |
|------|------|------|
| packageName | string | 是 |
| logId | integer | 是 |
| group | string | 否 |

**响应**：

```json
{"time":1788424130653,"LogName":"MD5",
 "data":[{"name":"签名内容","type":"byte[]","value":{"bytes":"Y29tLmppbmdkb25nLmFwcC5tYWxs\n"}},
         {"name":"签名结果","type":"byte[]","value":{"bytes":"T7sw63txZhGb0l5B7d7uLw=="}}],
 "callStack":"at dAlc.Y.io.sw.UMmauSdvX.XC_MethodHook.callAfterHookedMethod(...)"}
```

`value.bytes` 为 base64；无数据库/ID 不存在时 `{}`

## get_logs

**功能**：批量读取日志完整详情。依赖日志数据库。

**请求**：

| 参数 | 类型 | 必填 |
|------|------|------|
| packageName | string | 是 |
| logIds | integer[] | 是 |
| group | string | 否 |

**响应**：详情数组（元素结构同 `get_log`）；无数据时 `[]`

## get_log_graph

**功能**：追踪单条日志的上游数据流；返回依赖优先的图节点与参数到来源日志 ID 的映射。实时可用。

**请求**：

| 参数 | 类型 | 必填 |
|------|------|------|
| packageName | string | 是 |
| logId | integer | 是 |
| group | string | 否 |

**响应**：

```json
{"nodes":[{"id":2938,"name":"MD5","input":{"签名内容":[]},"output":"签名结果"}]}
```

`input` 值为该参数的来源 logId 列表（空数组表示无上游）。

## get_log_total

**功能**：获取日志条数。依赖日志数据库。

**请求**：`packageName`（必填）、`group`（可选）

**响应**：`{"total":1510}`；无数据库时 `{"total":0}`

## list_databases

**功能**：列出存在算法助手日志数据库的应用。仅用于确认目标是否有日志数据库。

**请求**：无参数。

**响应**：

```json
[{"packageName":"com.jingdong.app.mall","size":6254592,"time":1788424293558}]
```

无数据库时 `[]`

## clear_logs

**功能**：清空应用普通日志行，不删除数据库文件。破坏性操作。

**请求**：`packageName`（string，必填）

**响应**：`{"success":true}`；无数据库时 `{"success":false}`

## frida_get_log

**功能**：读取 Frida 日志为 JSON 数组；无效 JSON 行保留为原始条目。

**请求**：`packageName`（string，必填）

**响应**：JSON 数组；无日志时 `[]`

## frida_clear_log

**功能**：清空应用 Frida 日志。破坏性操作。

**请求**：`packageName`（string，必填）

**响应**：`{"success":true}`
