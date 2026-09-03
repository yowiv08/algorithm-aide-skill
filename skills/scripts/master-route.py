"""任务路由器：按 routing.json 的关键字规则给任务定 PRIMARY。

用法:
    python master-route.py "<任务描述>"
"""
import io
import json
import os
import re
import sys

if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
ROUTING = os.path.join(HERE, "..", "config", "routing.json")


def load_routing():
    with open(ROUTING, encoding="utf-8") as f:
        return json.load(f)


def score(task, route):
    hits = 0
    for kw in route.get("keywords", []):
        if not re.search(kw["must"], task, re.IGNORECASE):
            continue
        if "exclude" in kw and re.search(kw["exclude"], task, re.IGNORECASE):
            continue
        if "mustAll" in kw and not all(re.search(p, task, re.IGNORECASE) for p in kw["mustAll"]):
            continue
        hits += 1
    return hits


def resolve_target(cfg, route):
    if not route.get("remote"):
        return f"本地模块: skills/{route['skill']}"
    base = cfg["meta"].get("remoteBase", "")
    if route.get("remoteRoot"):
        return f"远程: {base}"
    return f"远程: {base}/{route['skill'].rsplit('/', 1)[0]}"


def route(task):
    cfg = load_routing()
    routes = cfg["routes"]
    priority = cfg.get("priority", list(routes))
    scored = [(score(task, routes[rid]), idx, rid)
              for idx, rid in enumerate(priority) if rid in routes]
    best = max(scored, key=lambda x: (x[0], -x[1]))
    rid = best[2] if best[0] > 0 else cfg["meta"]["fallbackId"]
    return cfg, routes[rid], rid


def main():
    task = " ".join(sys.argv[1:])
    if not task:
        print("用法: python master-route.py \"<任务描述>\"")
        sys.exit(2)
    cfg, r, rid = route(task)
    print(f"任务   : {task}")
    print(f"PRIMARY: [{rid}] {r['label']}")
    print(f"目标   : {resolve_target(cfg, r)}")


if __name__ == "__main__":
    main()
