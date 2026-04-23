#!/usr/bin/env python3
"""
Einmaliges Reparatur-Script: Stellt in allen Markdown-Frontmattern die
korrekte Einrückung von List-Items (2 Spaces) wieder her.
"""
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CONTENT_DIR = BASE_DIR / "content-prepared"


def fix(text: str) -> tuple[str, bool]:
    if not text.startswith("---\n"):
        return text, False
    end = text.find("\n---\n", 4)
    if end < 0:
        return text, False
    fm = text[: end + 5]
    body = text[end + 5 :]

    # Innerhalb Frontmatter: Zeilen, die mit " - " anfangen (1 Space + Dash), auf "  - " bringen
    new_fm_lines = []
    changed = False
    for line in fm.split("\n"):
        if re.match(r"^ - ", line):
            new_line = " " + line  # Eins vor, dann startet es mit 2 Spaces + "- "
            new_fm_lines.append(new_line)
            changed = True
        else:
            new_fm_lines.append(line)
    return "\n".join(new_fm_lines) + body, changed


def main():
    md_files = list((CONTENT_DIR / "blog").glob("*.md")) + list((CONTENT_DIR / "pages").glob("*.md"))
    fixed = 0
    for md in md_files:
        content = md.read_text(encoding="utf-8")
        new_content, changed = fix(content)
        if changed:
            md.write_text(new_content, encoding="utf-8")
            fixed += 1
            print(f"[FIX] {md.name}")
    print(f"\nReparierte Dateien: {fixed}")


if __name__ == "__main__":
    main()
