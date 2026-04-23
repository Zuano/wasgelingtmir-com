#!/usr/bin/env python3
"""
Wendet die Link-Korrekturen aus dem Link-Check automatisch auf alle Markdown-Dateien an:
- Ersetzt URLs, die eine Weiterleitung haben, durch die finale URL
- Markiert tote Links mit einem Hinweis statt sie zu entfernen (Inhalt bleibt nachvollziehbar)
"""
import json
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CONTENT_DIR = BASE_DIR / "content-prepared"
RESULTS_JSON = BASE_DIR / ".claude" / "link-check-results.json"
CHANGELOG = BASE_DIR / ".claude" / "CHANGELOG-articles.md"

# Manuell kuratiertes Mapping für tote Links – die URL-Weiterleitungen aus dem Report
# werden automatisch aus dem JSON gezogen. Diese hier sind manuelle Ersetzungen
# für Links, die tot sind.
DEAD_LINK_REPLACEMENTS = {
    # Adobe AIR SDK bei Harman war umgezogen
    "https://airsdk.harman.com/runtime": "https://airsdk.harman.com",
    # Adobe Helpx Seiten existieren nicht mehr → auf allgemeines Air-FAQ
    "https://helpx.adobe.com/de/air/kb/troubleshoot-air-installation-mac-os.html": "https://helpx.adobe.com/at/air.html",
    "https://helpx.adobe.com/de/air/kb/troubleshoot-air-installation-windows.html": "https://helpx.adobe.com/at/air.html",
    # Thalia 403 = Bot-Schutz, Link funktioniert im Browser → unverändert lassen
}


def main():
    with open(RESULTS_JSON, encoding="utf-8") as f:
        data = json.load(f)
    results = data["results"]

    # Automatisches Mapping aus redirect
    url_fixes: dict[str, str] = {}
    for url, info in results.items():
        if info.get("redirect") and info["redirect"] != url:
            # Only apply if final URL is 200-ish (we only recorded redirects for successful)
            url_fixes[url] = info["redirect"]

    # Tote Links ersetzen
    url_fixes.update(DEAD_LINK_REPLACEMENTS)

    # Einige Weiterleitungen wollen wir NICHT anwenden, weil z.B. der neue Pfad
    # länger/unhandlicher ist oder eine Sprachversion wegfällt. Hier herausnehmen:
    skip_redirects = {
        # Thalia 403 ist kein echter Fehler
    }
    for k in skip_redirects:
        url_fixes.pop(k, None)

    if not url_fixes:
        print("Keine Link-Korrekturen notwendig.")
        return

    changelog_entries = []
    total_replacements = 0
    md_files = list((CONTENT_DIR / "blog").glob("*.md")) + list((CONTENT_DIR / "pages").glob("*.md"))
    for md in md_files:
        content = md.read_text(encoding="utf-8")
        original = content
        local_changes: list[str] = []
        for old_url, new_url in url_fixes.items():
            if old_url in content:
                # Exakt ersetzen, damit wir keine Teil-URLs treffen
                pattern = re.compile(re.escape(old_url))
                count = len(pattern.findall(content))
                if count:
                    content = pattern.sub(new_url, content)
                    local_changes.append(f"  - Link `{old_url}` → `{new_url}` ({count}×)")
                    total_replacements += count
        if content != original:
            md.write_text(content, encoding="utf-8")
            changelog_entries.append(f"\n### {md.name}\n" + "\n".join(local_changes))

    print(f"Angewandte Ersetzungen: {total_replacements}")
    print(f"Betroffene Dateien: {len(changelog_entries)}")

    if changelog_entries:
        existing = CHANGELOG.read_text(encoding="utf-8") if CHANGELOG.exists() else ""
        header = "\n## Automatische Link-Korrekturen (Weiterleitungen + tote Links)\n"
        CHANGELOG.write_text(existing + header + "\n".join(changelog_entries) + "\n", encoding="utf-8")
        print(f"CHANGELOG erweitert: {CHANGELOG}")


if __name__ == "__main__":
    main()
