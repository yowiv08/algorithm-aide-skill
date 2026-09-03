# 服务管理 API（8 工具）

## service_isRunning

**功能**：算法助手服务是否在运行。

**请求**：无参数。

**响应**：`true` / `false`

## service_getVersion

**功能**：获取服务版本号。

**请求**：无参数。

**响应**：整数，如 `112`

## service_getVersionName

**功能**：获取 32 位服务版本名（MD5 格式）。

**请求**：无参数。

**响应**：字符串，如 `"d17ac658fa6322e0c70449db7aa8b1be"`

## service_getConfigSize

**功能**：获取全局配置大小（字节数）。

**请求**：无参数。

**响应**：整数；配置为空时 `0`

## service_getConfigItem

**功能**：读取一个全局配置项。

**请求**：

| 参数 | 类型 | 必填 |
|------|------|------|
| configName | string | 是 |

**响应**：配置值字符串；不存在时 `""`

## service_setConfigItem

**功能**：设置一个全局配置项。

**请求**：

| 参数 | 类型 | 必填 |
|------|------|------|
| configName | string | 是 |
| configValue | string | 是 |

**响应**：`{"success":true}`

## service_clearConfig

**功能**：清空全局服务配置。破坏性操作。

**请求**：无参数。

**响应**：`{"success":true}`

## service_getAppsWithSwitch

**功能**：获取已开启 Hook 的应用包名列表。仅用于确认目标是否在 Hook 列表中。

**请求**：无参数。

**响应**：包名数组，如 `["com.jingdong.app.mall"]`；无应用时 `[]`
