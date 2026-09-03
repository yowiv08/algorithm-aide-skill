# Hook 与 Frida 脚本 API（6 工具）

## app_addHook

**功能**：添加自定义 Hook，追加到现有 Hook 列表，不替换。

**请求**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| packageName | string | 是 | |
| className | string | 是 | 完整类名 |
| methodName | string | 是 | |
| parameterSign | string | 否 | 参数签名 |
| description | string | 否 | |
| results | string | 否 | 替换返回值表达式 |
| isIntercept | boolean | 否 | 是否拦截（不执行原方法） |

**响应**：`{"success":true,"added":true}`

添加后 `app_getConfig` 中 `hookList` 条目结构：

```json
{"argsValues":[],"className":"java.lang.String","constructor":false,
 "description":"","enable":true,"intercept":false,"methodName":"toString",
 "parameterSign":"","printLog":true,"results":""}
```

## scriptList

**功能**：列出应用全部 Frida 脚本。

**请求**：`packageName`（string，必填）

**响应**：脚本文件名数组，如 `["test.js"]`；无脚本时 `[]`

## app_importScript

**功能**：创建/导入/更新 Frida 脚本；更新已启用脚本时立即生效，无需重启应用。

**请求**：

| 参数 | 类型 | 必填 |
|------|------|------|
| packageName | string | 是 |
| name | string | 是 | 脚本文件名，如 `test.js` |
| jsCode | string | 是 | 脚本源码 |

**响应**：`true`（成功）/ `false`（失败——全新目标常见，见 [pitfalls.md](pitfalls.md)）

## enable_script

**功能**：启用指定脚本；同时会导致其他脚本被关闭。只写 `enableScript` 配置值，不校验脚本是否存在。

**请求**：

| 参数 | 类型 | 必填 |
|------|------|------|
| packageName | string | 是 |
| scriptName | string | 是 |

**响应**：`{"success":true,"value":"test.js"}`

## app_getScript

**功能**：读取 Frida 脚本源码。

**请求**：`packageName`、`name`（string，必填）

**响应**：脚本源码字符串；不存在时 `""`

## app_deleteScript

**功能**：删除 Frida 脚本。破坏性操作。对不存在的脚本同样返回 `true`。

**请求**：`packageName`、`name`（string，必填）

**响应**：`true`
