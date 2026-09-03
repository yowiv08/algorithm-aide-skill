# 路由矩阵

事实源：`config/routing.json`。修改路由只改该文件，本文件与其保持一致。

## 评分规则

每条关键字规则命中后计入候选集；按 `priority` 数组顺序取命中分数最高者为 PRIMARY；并列时 priority 靠前者胜出；未命中回退 `R0`。

## 路由表

| ID | 优先级 | 任务 | 目标 | 类型 |
|----|--------|------|------|------|
| R1 | 1 | Android 动态分析 / 实时 Hook / Frida 脚本与日志 / 算法分析 | `android-dynamic/SKILL.md` | 本地 |
| R2 | 2 | APK 静态反编译 / smali / 重打包 | reverse-skill `apk-reverse/` | 远程 |
| R3 | 3 | iOS / 移动通用逆向 | reverse-skill `mobile-reverse/` | 远程 |
| R4 | 4 | 前端 JS 逆向 / 抓包 / 请求重放 | reverse-skill `js-reverse/` | 远程 |
| R5 | 5 | so / ELF / IDA / Ghidra / radare2 静态分析 | reverse-skill `ida-reverse/` 等 | 远程 |
| R6 | 6 | 渗透 / 恶意软件 / CTF / 固件 / 取证 | reverse-skill 总控 | 远程 |
| R0 | 回退 | 未命中任何规则 | reverse-skill 总控 | 远程 |

## 关键字规则

### R1 Android 动态分析（本地）

- `算法助手 | algorithm-aide | 动态分析 | 动态hook | 实时hook | 运行时hook | hook日志 | 实时日志 | 算法日志 | 签名算法 | 加密算法分析 | md5分析 | 哈希分析 | 加解密hook | 行为监听 | 算法还原 | 日志采集 | 采集…日志 | 点击行为 | 行为日志`
- `frida` 且带 `脚本|script|日志|log|hook|注入|enable|import|启用|导入`（纯静态 Frida 逆向归 R5）
- `android|安卓` 且带 `hook|监听|动态|运行|启动|强停|日志`
- `hook` 且带 `app|应用|包名|登录|启动`（对应用做运行时干预）

### R2 APK 静态（远程，排除动态语境）

- `apk | smali | jadx | apktool | 反编译apk | apk加固 | 重打包 | root检测 | 证书校验 | certificate pinning`（exclude：动态|hook|实时|日志）

### R3 iOS / 移动（远程）

- `ipa | ios逆向 | ios reverse | objection | mobsf | 越狱 | jailbreak`

### R4 前端 JS（远程）

- `js逆向 | webpack逆向 | 前端签名 | 加密参数 | 抓包 | http capture | 请求重放 | cryptojs`

### R5 二进制（远程）

- `ida | ghidra | radare | r2 | 反汇编 | .so | so文件 | .elf | native分析 | jni | 脱壳`

### R6 其他安全任务（远程总控）

- `渗透 | pentest | 恶意软件 | malware | ctf | 漏洞 | exploit | pwn | 固件 | firmware | 取证`

## 远程目标解析

远程路由的 `skill` 路径拼接 `remoteBase`：

- R2 → https://github.com/zhaoxuya520/reverse-skill/tree/main/skills/apk-reverse
- R3 → https://github.com/zhaoxuya520/reverse-skill/tree/main/skills/mobile-reverse
- R4 → https://github.com/zhaoxuya520/reverse-skill/tree/main/skills/js-reverse
- R5 → https://github.com/zhaoxuya520/reverse-skill/tree/main/skills/ida-reverse
- R6 / R0 → https://github.com/zhaoxuya520/reverse-skill/tree/main/skills
