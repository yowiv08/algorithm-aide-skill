# 应用控制与应用配置 API（10 工具）

## service_appIsRunning

**功能**：应用当前是否有运行中的进程。

**请求**：`packageName`（string，必填）

**响应**：`true` / `false`

## app_start

**功能**：启动应用；已在运行时先强停再启动。

**请求**：`packageName`（string，必填）

**响应**：

```json
{"success":true,"wasRunning":false,"forceStopped":false}
```

## service_forceStopApp

**功能**：强停应用，等价于系统"强制停止"。破坏性操作。

**请求**：`packageName`（string，必填）

**响应**：`{"success":true}`

## app_isSwitch

**功能**：读取应用 Hook 总开关状态。

**请求**：`packageName`（string，必填）

**响应**：`true` / `false`

## app_setSwitch

**功能**：设置应用 Hook 总开关。

**请求**：

| 参数 | 类型 | 必填 |
|------|------|------|
| packageName | string | 是 |
| isSwitch | boolean | 是 |

**响应**：`{"success":true}`

## app_getConfig

**功能**：读取应用完整配置。

**请求**：`packageName`（string，必填）

**响应**：JSON 字符串（注意是字符串，非对象）；未配置时 `""`：

```json
"{\"digestSwitch\":true,\"hookList\":[...],\"macSwitch\":true}"
```

## app_setConfig

**功能**：合并应用配置；`configData` 中 absent 的字段（含 `script_data`）保留。清空某数组字段需显式传空数组（如 `"hookList":[]`）。

**请求**：

| 参数 | 类型 | 必填 |
|------|------|------|
| packageName | string | 是 |
| configData | string（JSON 对象序列化） | 是 |

**响应**：`{"success":true}`

## app_listConfigOptions

**功能**：列出全部应用配置项：configName、标题、类型、默认值、分类、描述。

**请求**：无参数。

**响应**：

```json
{"options":[{"configName":"digestSwitch","title":"哈希算法","category":"算法分析",
  "type":"boolean","default":false,"description":"启用\"哈希算法\"相关的 Hook 或日志功能。"}]}
```

## app_getConfigItem

**功能**：读取单个应用配置项。

**请求**：`packageName`、`configName`（string，必填）

**响应**：

```json
{"value":true}      // boolean 项
{"value":"test.js"} // string 项
{"value":null}      // 未设置
```

## app_setConfigItem

**功能**：设置单个应用配置项。`value` 支持 boolean / string / number。

**请求**：

| 参数 | 类型 | 必填 |
|------|------|------|
| packageName | string | 是 |
| configName | string | 是 |
| value | boolean/string/number | 是 |

**响应**：

```json
{"success":true,"value":true}
```

---

## 配置项全表

`app_listConfigOptions` 返回 41 项（实测）。开关类默认均为 `false`。

### 算法分析

| configName | 标题 | 说明 |
|------------|------|------|
| digestSwitch | 哈希算法 | 哈希算法相关 Hook/日志 |
| macSwitch | 密钥哈希（HMAC） | HMAC 相关 Hook/日志 |
| cipherSwitch | 加解密算法 | 加解密相关 Hook/日志 |
| webCryptSwitch | WebView 加解密库 | WebView 加解密库 Hook/日志 |

### 设备环境

| configName | 标题 |
|------------|------|
| checkRootSwitch | 隐藏 Root |
| hiddenXposedSwitch | 隐藏 Xposed |

### 网络环境

| configName | 标题 |
|------------|------|
| hiddenWifiProxySwitch | 隐藏 Wi-Fi 代理 |
| hiddenVpnSwitch | 隐藏 VPN |
| justTrustMePlushSwitch | 绕过 SSL 证书校验 |
| reqableSwitch | Reqable 堆栈跟踪（Java） |
| reqableSwitch_native | Reqable 堆栈跟踪（Native） |

### 行为监听

| configName | 标题 |
|------------|------|
| assetsSwitch | Assets 读取 |
| fileSwitch | 文件读取 |
| fileWriteSwitch | 文件写入 |
| fileDeleteSwitch | 文件删除 |
| shellSwitch | Shell 命令 |

### 交互与界面

| configName | 标题 |
|------------|------|
| onClickSwitch | 点击事件 |
| dialogSwitch | 弹窗定位 |
| closeDialogSwitch | 拦截关键词弹窗 |
| textViewSwitch | 控件文本赋值 |
| activitySwitch | Activity 跳转记录 |
| dialogKeyword | 弹窗拦截关键词（string，默认 `注册码,机器码,激活码`，逗号分隔） |

### WebView 与数据库

| configName | 标题 |
|------------|------|
| webViewDebugSwitch | WebView 调试 |
| webViewLoadUrlSwitch | WebView LoadUrl |
| sqliteOpenSwitch | 打开数据库 |
| sqliteInsertSwitch | 数据库 Insert |
| sqliteDeleteSwitch | 数据库 Delete |
| sqliteUpdateSwitch | 数据库 Update |
| sqliteQuerySwitch | 数据库 Query |
| sqliteExecSQLSwitch | 数据库 ExecSQL |

### 存储与其他

| configName | 标题 |
|------------|------|
| getSharedPreferencesSwitch | 读取 SharedPreferences |
| SharedPreferencesGetSwitch | SharedPreferences Get |
| SharedPreferencesPutSwitch | SharedPreferences Put |
| cameraHookSwitch | 相机替换为选图 |
| logSwitch | Logcat 捕获 |
| ApplicationSwitch | Application 信息 |
| exitSwitch | 拦截应用退出 |
| ExceptionSwitch | 防止应用闪退 |
| screenSwitch | 解除截屏/录屏限制 |
| signSwitch | 应用签名读取 |

### Frida

| configName | 标题 | 说明 |
|------------|------|------|
| enableScript | 启用的 Frida 脚本 | string；值为 scriptList 返回的脚本文件名，空字符串表示禁用 |
