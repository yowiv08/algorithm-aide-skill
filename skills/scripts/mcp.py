"""算法助手 Pro MCP 客户端库（MCP Streamable HTTP，仅标准库）。

服务器地址解析顺序：
1. url 参数
2. 环境变量 ALGO_AIDE_URL
3. 默认 http://127.0.0.1:8788/mcp
"""
import json
import os
import urllib.error
import urllib.request

DEFAULT_URL = "http://127.0.0.1:8788/mcp"
HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json, text/event-stream",
}


def resolve_url(url=None):
    return url or os.environ.get("ALGO_AIDE_URL") or DEFAULT_URL


class McpError(Exception):
    """工具级错误：isError=true 或 content 携带 {"error":..., "stackTrace":...}"""


class MCP:
    def __init__(self, url=None):
        self.base = resolve_url(url)
        self.session = None
        self._id = 0

    def _post(self, payload, timeout=30):
        headers = dict(HEADERS)
        if self.session:
            headers["Mcp-Session-Id"] = self.session
        req = urllib.request.Request(
            self.base, data=json.dumps(payload).encode("utf-8"),
            headers=headers, method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                sid = resp.headers.get("Mcp-Session-Id")
                if sid:
                    self.session = sid
                body = resp.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            raise McpError(f"HTTP {e.code}: {e.read().decode('utf-8', 'replace')[:300]}") from None
        except urllib.error.URLError as e:
            reason = getattr(e.reason, "strerror", None) or str(e.reason)
            raise McpError(f"无法连接 {self.base}: {reason}") from None
        if not body.strip():
            return None
        if body.startswith("event:") or body.startswith("data:"):
            lines = [l[5:].strip() for l in body.splitlines() if l.startswith("data:")]
            body = lines[-1] if lines else "{}"
        return json.loads(body)

    def _next_id(self):
        self._id += 1
        return self._id

    def initialize(self):
        r = self._post({
            "jsonrpc": "2.0", "id": self._next_id(), "method": "initialize",
            "params": {
                "protocolVersion": "2025-06-18",
                "capabilities": {},
                "clientInfo": {"name": "algorithm-aide-skill", "version": "1.0"},
            },
        })
        if r is None or "result" not in r:
            raise McpError(f"initialize 失败: {json.dumps(r, ensure_ascii=False)[:300]}")
        self._post({"jsonrpc": "2.0", "method": "notifications/initialized"})
        return r["result"]

    def list_tools(self):
        r = self._post({"jsonrpc": "2.0", "id": self._next_id(), "method": "tools/list"})
        return r.get("result", {}).get("tools", [])

    def call(self, name, arguments=None):
        r = self._post({
            "jsonrpc": "2.0", "id": self._next_id(), "method": "tools/call",
            "params": {"name": name, "arguments": arguments or {}},
        })
        if r is None:
            raise McpError(f"{name}: 空响应")
        if "error" in r:
            raise McpError(f"{name}: {r['error'].get('message', r['error'])}")
        result = r.get("result", {})
        if result.get("isError"):
            raise McpError(f"{name}: {text_of(result)}")
        return result

    def call_text(self, name, arguments=None):
        return text_of(self.call(name, arguments))


def text_of(result):
    """tools/call 结果 → 文本（算法助手 Pro 全部工具返回单条 text）。"""
    parts = []
    for c in result.get("content", []):
        if c.get("type") == "text":
            parts.append(c.get("text", ""))
    return "\n".join(parts)
