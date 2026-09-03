"""算法助手 Pro 命令行入口。

用法:
    python aide.py ping                                # 连通性 + 服务器信息
    python aide.py list                                # 列出全部工具
    python aide.py call <tool> '<json参数>'            # 调用工具
    python aide.py apps                                # 已开启 Hook 的应用
    python aide.py logs <packageName> [page]           # 日志摘要（实时）
    python aide.py log <packageName> <logId>           # 日志详情
    python aide.py search <packageName> <text>         # 搜索日志

服务器地址: --url 参数 > ALGO_AIDE_URL 环境变量 > 默认值
"""
import argparse
import io
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp import MCP, McpError  # noqa: E402

if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")


def pretty(text):
    try:
        return json.dumps(json.loads(text), ensure_ascii=False, indent=2)
    except (ValueError, TypeError):
        return text


def main():
    ap = argparse.ArgumentParser(description="算法助手 Pro MCP 命令行")
    ap.add_argument("--url", help="MCP 服务器地址")
    ap.add_argument("command", choices=["ping", "list", "call", "apps", "logs", "log", "search"])
    ap.add_argument("args", nargs="*")
    a = ap.parse_args()

    mcp = MCP(a.url)
    try:
        if a.command == "ping":
            info = mcp.initialize()
            print(f"server : {info.get('serverInfo', {}).get('name')}")
            print(f"version: {info.get('serverInfo', {}).get('version')}")
            print(f"proto  : {info.get('protocolVersion')}")
            running = mcp.call_text("service_isRunning")
            print(f"running: {running}")
        elif a.command == "list":
            mcp.initialize()
            for t in mcp.list_tools():
                req = ",".join(t.get("inputSchema", {}).get("required", []))
                print(f"{t['name']:24} {req}")
        elif a.command == "call":
            tool = a.args[0]
            args = json.loads(a.args[1]) if len(a.args) > 1 else {}
            mcp.initialize()
            print(pretty(mcp.call_text(tool, args)))
        elif a.command == "apps":
            mcp.initialize()
            print(pretty(mcp.call_text("service_getAppsWithSwitch")))
        elif a.command == "logs":
            pkg = a.args[0]
            page = int(a.args[1]) if len(a.args) > 1 else 0
            mcp.initialize()
            print(pretty(mcp.call_text("list_logs", {"packageName": pkg, "page": page})))
        elif a.command == "log":
            mcp.initialize()
            print(pretty(mcp.call_text("get_log", {"packageName": a.args[0], "logId": int(a.args[1])})))
        elif a.command == "search":
            mcp.initialize()
            print(pretty(mcp.call_text("search_logs", {"packageName": a.args[0], "text": a.args[1]})))
    except McpError as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        pass


if __name__ == "__main__":
    main()
