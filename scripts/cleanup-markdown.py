#!/usr/bin/env python3
"""
Bereinigt alle Markdown-Dateien von WordPress-Artefakten:
- Non-Breaking Spaces (U+00A0) → normale Leerzeichen (im Body UND im Frontmatter-Werten)
- Andere Zero-Width-Zeichen
- Doppelte Leerzeichen im Fließtext (nicht am Zeilenanfang, nicht in YAML-Frontmatter)
- Leerzeichen am Zeilenende
- Max. 2 Leerzeilen in Folge

WICHTIG: YAML-Frontmatter wird separat behandelt, damit die Einrückung von
Listen (`  - "tag"`) erhalten bleibt.
"""
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CONTENT_DIR = BASE_DIR / "content-prepared"

REPLACEMENTS = {
    "\u00A0": " ",
    "\u200B": "",
    "\u200C": "",
    "\uFEFF": "",
    "\u2028": "\n",
    "\u2029": "\n\n",
}


def split_frontmatter(text: str) -> tuple[str, str]:
    """Teilt in Frontmatter und Body. Gibt ('', text) zurück, falls kein Frontmatter."""
    if not text.startswith("---\n"):
        return "", text
    end = text.find("\n---\n", 4)
    if end < 0:
        return "", text
    fm = text[: end + 5]
    body = text[end + 5 :]
    return fm, body


def clean_frontmatter(fm: str) -> tuple[str, list[str]]:
    """Bereinigt nur Unicode-Whitespace im Frontmatter – Einrückung bleibt erhalten."""
    changes = []
    new = fm
    for char, repl in REPLACEMENTS.items():
        if char in new:
            count = new.count(char)
            new = new.replace(char, repl)
            changes.append(f"Frontmatter: {count}× U+{ord(char):04X} bereinigt")
    return new, changes


def clean_body(body: str) -> tuple[str, list[str]]:
    changes = []
    new = body
    for char, repl in REPLACEMENTS.items():
        if char in new:
            count = new.count(char)
            new = new.replace(char, repl)
            changes.append(f"Body: {count}× U+{ord(char):04X} bereinigt")
    # Doppelte Spaces NUR zwischen Wörtern, nicht am Zeilenanfang
    cleaned_lines = []
    body_changed = False
    for line in new.split("\n"):
        # Einrückung merken
        leading = len(line) - len(line.lstrip(" "))
        stripped = line[leading:]
        collapsed = re.sub(r" {2,}", " ", stripped)
        if collapsed != stripped:
            body_changed = True
        # Trailing Whitespace weg
        cleaned_lines.append((" " * leading) + collapsed.rstrip())
    if body_changed:
        changes.append("Body: Doppelte Leerzeichen zwischen Wörtern zusammengefasst")
    new = "\n".join(cleaned_lines)
    # Max. 2 Leerzeilen
    new_collapsed = re.sub(r"\n{3,}", "\n\n", new)
    if new_collapsed != new:
        changes.append("Body: Mehr als 2 Leerzeilen zusammengefasst")
        new = new_collapsed
    return new, changes


def main():
    md_files = list((CONTENT_DIR / "blog").glob("*.md")) + list((CONTENT_DIR / "pages").glob("*.md"))
    total_changes = 0
    for md in md_files:
        content = md.read_text(encoding="utf-8")
        fm, body = split_frontmatter(content)
        all_changes = []
        if fm:
            fm_new, ch = clean_frontmatter(fm)
            all_changes.extend(ch)
            fm = fm_new
        body_new, ch = clean_body(body)
        all_changes.extend(ch)
        body = body_new
        new_content = fm + body if fm else body
        if new_content != content:
            md.write_text(new_content, encoding="utf-8")
            total_changes += 1
            print(f"[OK] {md.name}")
            for c in all_changes:
                print(f"     - {c}")
    print(f"\nBereinigte Dateien: {total_changes}/{len(md_files)}")


if __name__ == "__main__":
    main()
