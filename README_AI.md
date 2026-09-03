# Algorithm Aide Skill — AI Agent Bootstrap

> ⚡ **For AI agents only.** If you are a human reader, go back to [README.md](README.md).

This file contains the bootstrap instructions and behavior chain for AI agents (Claude Code, Codex CLI, Cursor, Cline, Windsurf, Kiro, etc.). If you are an AI agent, **execute section 0 immediately** after finishing this file.

> This package can be placed in any directory. The AI will automatically detect its actual path. In the following text, `<SKILL_ROOT>` refers to your real installation path.

---

## 0. First Instruction for the AI (Execute Immediately After Reading This File)

> After the AI finishes reading this file, it must automatically execute the following configuration process and then report what was changed. The user does not need to operate manually.

### Automatic Configuration Process

```text
1. Detect the actual installation path of this package (the directory containing this file)
2. Verify the runtime: python --version (3.10+ required, standard library only)
3. Obtain the Algorithm Aide Pro MCP server URL:
   - From the user's message, or
   - From the ALGO_AIDE_URL environment variable
   - If neither exists, ask the user for the address (it is device-specific, never guess it)
4. Verify connectivity and refresh the tool index:
   python skills/scripts/test-tools.py --url <服务器地址>
   - service_isRunning must be "true"; otherwise report and stop
5. Read RULES.md → follow its authorization boundary, tool-call discipline, and evidence requirements
6. Route the task:
   python skills/scripts/master-route.py "<任务描述>"
   - Local PRIMARY (Android dynamic analysis) → open skills/android-dynamic/SKILL.md
   - Remote PRIMARY → reverse-skill repo module (https://github.com/zhaoxuya520/reverse-skill)
7. Open PRIMARY SKILL.md → execute ACTION REQUIRED. Do not stop at "configuration completed".
8. End with evidence: conclusions must cite logId / tool names / key response fields.
```

### Example Report Format

```markdown
✅ **Algorithm Aide Skill Configured Successfully**

**Installation path**: C:\path\to\algorithm-aide-skill
**Runtime**: Python 3.x detected
**MCP server**: http://192.168.x.x:8788/mcp (algorithm-aide-pro, running)
**Tool status**: 34 tools available (tool-index.md refreshed)
**Rules loaded**: RULES.md (authorization boundary + destructive-op confirmation)
**Routing**: local `android-dynamic/` for dynamic analysis; other reverse tasks → remote reverse-skill

Ready for the task.
```

---

This is not a tool installer. It is an **Android dynamic-analysis skill router** for code agents:

1. When the AI encounters Android runtime hooking / algorithm analysis / Frida script / log collection tasks, it routes to the local `android-dynamic` module and drives the real MCP server.
2. Tasks outside dynamic analysis (static APK, binary, JS, pentest) are delegated to the remote [reverse-skill](https://github.com/zhaoxuya520/reverse-skill) router — this package does not duplicate its content.

---

## Package Layout

```text
<SKILL_ROOT>\
├── README.md                     # Human introduction
├── README_AI.md                  # The AI bootstrap file you are reading
├── RULES.md                      # Authorization boundary, tool discipline, evidence rules
├── AGENTS.md                     # Agent entry summary
├── CLAUDE.md                     # Claude Code entry summary
└── skills\
    ├── SKILL.md                  # Main controller + routing contract
    ├── routing.md                # Routing matrix (R1–R6, R0 fallback)
    ├── INDEX.md                  # Module index (auto-generated, do not edit)
    ├── tool-index.md             # MCP server detection result (script-refreshed)
    ├── config\routing.json       # Single source of truth for routing
    ├── scripts\                  # Cross-platform Python (stdlib only)
    │   ├── mcp.py                # MCP client library
    │   ├── aide.py               # CLI: ping / list / call / apps / logs / log / search
    │   ├── master-route.py       # Task router
    │   ├── extract-summaries.py  # INDEX.md generator
    │   └── test-tools.py         # Connectivity test + tool-index refresh
    └── android-dynamic\          # The only local module
        ├── SKILL.md              # Module entry + 6-step workflow
        └── references\           # Load on demand, not all at once
            ├── mcp-protocol.md   # Session, headers, response format, error format
            ├── service-api.md    # 8 service tools
            ├── app-api.md        # 10 app control/config tools + 41 config options
            ├── hook-script-api.md# 6 hook/Frida script tools
            ├── log-api.md        # 10 log tools
            └── pitfalls.md       # Live-buffer vs persisted-DB behavior, tested traps
```

---

## How to Drive the MCP Server

The Algorithm Aide Pro app runs the MCP server on an Android device (Streamable HTTP). All tool calls go through the package scripts — never hand-write HTTP:

```bash
# Connectivity + server info
python skills/scripts/aide.py --url http://192.168.x.x:8788/mcp ping

# List all 34 tools
python skills/scripts/aide.py --url http://192.168.x.x:8788/mcp list

# Call any tool with JSON arguments
python skills/scripts/aide.py --url http://192.168.x.x:8788/mcp call list_logs '{"packageName":"com.example.app","page":0}'
```

Or set `ALGO_AIDE_URL` once and omit `--url`.

Server address rules (enforced by RULES.md):
- The address is device-specific and may change with the device's network (e.g. 192.168.8.x → 192.168.137.x). Never hardcode or guess.
- The URL must come from the user's message or `ALGO_AIDE_URL`.

## Critical Behavior Notes (from live testing, see skills/android-dynamic/references/pitfalls.md)

- `list_logs` / `search_logs` / `get_log_graph` read the in-memory live buffer and always work.
- `get_log` / `get_logs` / `get_log_total` / `list_databases` / `clear_logs` / `app_importScript` require the target app to have a persisted log database — on a fresh target they return empty/false. This does NOT mean "no logs".
- Never hook ultra-high-frequency methods (e.g. `java.lang.String.toString`) with the master switch on — the target app will die on launch.
- Tool errors return `isError: true` with `{"error": ..., "stackTrace": ...}` in the text content — fix the arguments per the error message and retry.

---

## Integration with AI Clients

Whatever client you use (Claude Code, Codex CLI, Cursor, Cline, Windsurf), you need only:

1. This package directory
2. The Algorithm Aide Pro MCP server address (from the user)
3. A way to inject "read README_AI.md / skills/SKILL.md first for Android reverse tasks"
4. Python 3.10+ (stdlib only — no pip install needed)

### Minimum Prompt Injection

Tell the AI about these entry files:

- `skills/SKILL.md`
- `skills/routing.md`
- `skills/tool-index.md`

And the principle: **route first, execute second; dynamic analysis local, everything else remote.**

### Claude Code

`CLAUDE.md` at the package root is auto-loaded. Just open the session inside the package directory.

### Codex CLI / Cursor / Others

Inject the package path and the three entry files above into your rules / project instructions.

---

## Adding a New Local Module

1. Create `skills/<module-name>/SKILL.md` with frontmatter `name` + `description`
2. Add reference docs under `skills/<module-name>/references/`
3. Add a route entry in `skills/config/routing.json` (keywords + priority)
4. Keep `skills/routing.md` consistent with the JSON
5. Regenerate the index: `python skills/scripts/extract-summaries.py`

---

## FAQ

**Q1: The MCP server is unreachable.**
Check that the Android device is on the same network and the Algorithm Aide Pro app is running. The address changes with the device's network — ask the user for the current one.

**Q2: `app_importScript` returns false.**
The target app has no workspace yet. Configure the app once in the Algorithm Aide Pro app UI, then retry. See pitfalls.md.

**Q3: Does this package handle APK decompilation / so analysis?**
No. Route to remote reverse-skill (`apk-reverse/`, `ida-reverse/`, etc.). This package only does dynamic analysis.

**Q4: Can I register the MCP server directly in my client's MCP config?**
The server is on an Android device and its address changes; routing through `skills/scripts/aide.py` with a user-provided `--url` / `ALGO_AIDE_URL` is the supported path.

---

## License

MIT. Intended for analysis of apps and devices you own or are explicitly authorized to test.
