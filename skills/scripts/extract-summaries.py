"""INDEX.md 生成器：读取各模块 SKILL.md frontmatter，重建模块索引。

用法:
    python extract-summaries.py
"""
import io
import os
import re
import sys

if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
SKILLS_DIR = os.path.join(HERE, "..")


def parse_frontmatter(path):
    text = open(path, encoding="utf-8").read()
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end < 0:
        return None
    fm = {}
    for line in text[4:end].splitlines():
        m = re.match(r"(\w+):\s*(.+)", line.strip())
        if m:
            fm[m.group(1)] = m.group(2).strip()
    return fm


def main():
    rows = []
    for entry in sorted(os.listdir(SKILLS_DIR)):
        skill_md = os.path.join(SKILLS_DIR, entry, "SKILL.md")
        if not os.path.isfile(skill_md):
            continue
        fm = parse_frontmatter(skill_md) or {}
        desc = fm.get("description", "")
        rows.append((entry, desc))

    out = [
        "# 模块索引",
        "",
        "> 本文件由 `scripts/extract-summaries.py` 自动生成，请勿手改。",
        "> 修改摘要请编辑对应模块 `SKILL.md` 的 frontmatter `description`，然后重跑脚本。",
        "",
        "## 模块总览",
        "",
        "| 模块 | 摘要 |",
        "|------|------|",
    ]
    for name, desc in rows:
        out.append(f"| [{name}]({name}/SKILL.md) | {desc} |")
    out += [
        "",
        "## 远程委托",
        "",
        "静态逆向、二进制分析、前端逆向、渗透等任务路由到远程 "
        "[reverse-skill](https://github.com/zhaoxuya520/reverse-skill)，见 [routing.md](routing.md)。",
        "",
    ]
    path = os.path.join(SKILLS_DIR, "INDEX.md")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(out))
    print(f"已生成 {path}（{len(rows)} 个模块）")


if __name__ == "__main__":
    main()
