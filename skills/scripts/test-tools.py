"""算法助手 Pro 服务器连通性测试 + tool-index.md 刷新。

用法:
    python test-tools.py --url http://192.168.8.104:8788/mcp   # 测试并刷新 tool-index.md
    python test-tools.py --url ... --no-write                   # 只测试
"""
import argparse
import io
import json
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp import MCP, McpError  # noqa: E402

if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
TOOL_INDEX = os.path.join(HERE, "..", "tool-index.md")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", help="MCP 服务器地址")
    ap.add_argument("--no-write", action="store_true", help="不刷新 tool-index.md")
    a = ap.parse_args()

    mcp = MCP(a.url)
    try:
        info = mcp.initialize()
    except McpError as e:
        print(f"连接失败: {e}")
        sys.exit(1)

    server = info.get("serverInfo", {})
    running = mcp.call_text("service_isRunning")
    tools = mcp.list_tools()
    apps = mcp.call_text("service_getAppsWithSwitch")

    print(f"服务器 : {mcp.base}")
    print(f"名称   : {server.get('name')}")
    print(f"版本   : {server.get('version')}")
    print(f"协议   : {info.get('protocolVersion')}")
    print(f"运行   : {running}")
    print(f"工具数 : {len(tools)}")
    print(f"已开Hook应用: {apps}")

    if not a.no_write:
        lines = [
            "# MCP 服务器检测结果",
            "",
            "> 由 `scripts/test-tools.py --url <地址>` 刷新，勿手改。",
            "",
            f"- 检测时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"- 服务器地址: `{mcp.base}`",
            f"- 服务: {server.get('name')} {server.get('version')}",
            f"- 协议版本: {info.get('protocolVersion')}",
            f"- 服务运行: {running}",
            f"- 已开启 Hook 的应用: {apps}",
            f"- 可用工具: {len(tools)} 个",
            "",
            "| 工具 | 必填参数 |",
            "|------|---------|",
        ]
        for t in tools:
            req = ", ".join(t.get("inputSchema", {}).get("required", [])) or "-"
            lines.append(f"| `{t['name']}` | {req} |")
        with open(TOOL_INDEX, "w", encoding="utf-8", newline="\n") as f:
            f.write("\n".join(lines) + "\n")
        print(f"\n已刷新 {TOOL_INDEX}")


if __name__ == "__main__":
    main()
