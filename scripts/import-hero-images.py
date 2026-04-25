#!/usr/bin/env python3
"""
import-hero-images.py

Liest alle Bilder aus einem Quellordner (Standard: ~/Downloads/wasgelingtmir-hero-images/),
matcht den Dateinamen gegen die Artikel-Slugs, kopiert die Bilder als
public/images/blog/<slug>/hero.webp (komprimiert!) und aktualisiert das Frontmatter
des Artikels.

Usage:
    # Standardordner ~/Downloads/wasgelingtmir-hero-images/
    python3 scripts/import-hero-images.py

    # Anderer Quellordner
    python3 scripts/import-hero-images.py /pfad/zum/ordner

    # Trockenlauf (zeigt nur, was passieren würde)
    python3 scripts/import-hero-images.py --dry-run

Erwartete Dateinamen im Quellordner:
    <slug>.png    oder    <slug>.jpg    oder    <slug>.jpeg / .webp / .gif

Beispiel:
    quitter-die-einfache-losung-gegen-nervige-inaktivitats-popups.png
    → wird zu public/images/blog/quitter-.../hero.webp
    → heroImage im Frontmatter wird auf "/images/blog/quitter-.../hero.webp" gesetzt
"""
from __future__ import annotations
import argparse
import json
import re
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("Fehlt: pip install Pillow")
    sys.exit(1)

BASE_DIR = Path(__file__).resolve().parent.parent
PROMPTS_JSON = BASE_DIR / "scripts" / "hero-image-prompts.json"
PUBLIC_IMAGES = BASE_DIR / "public" / "images" / "blog"
CONTENT_BLOG = BASE_DIR / "src" / "content" / "blog"
CONTENT_PREPARED = BASE_DIR / "content-prepared" / "blog"

WEBP_QUALITY = 85
TARGET_WIDTH = 1600  # für Karten reicht das, ist aber noch retina-tauglich
RESPONSIVE_WIDTHS = [400, 800, 1200, 1600]
SUPPORTED_INPUT_EXT = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".heic"}


def load_known_slugs() -> set[str]:
    """Liest alle gültigen Slugs aus den Artikel-Dateien (Dateiname ohne .md)."""
    slugs = set()
    for md in CONTENT_BLOG.glob("*.md"):
        slugs.add(md.stem)
    return slugs


def load_prompt_slugs() -> dict[str, dict]:
    """Liest die Prompts-JSON und gibt slug → {title, prompt, ...} zurück."""
    if not PROMPTS_JSON.exists():
        return {}
    with open(PROMPTS_JSON, encoding="utf-8") as f:
        data = json.load(f)
    result = {}
    for key in ("priority_critical", "priority_recommended", "priority_optional"):
        for entry in data.get(key, []):
            result[entry["slug"]] = entry
    return result


def find_input_files(source: Path, known_slugs: set[str]) -> list[tuple[Path, str]]:
    """Findet alle Bilder im Quellordner, die zu einem bekannten Slug passen."""
    if not source.exists():
        print(f"Quellordner existiert nicht: {source}")
        return []
    matches: list[tuple[Path, str]] = []
    for f in sorted(source.iterdir()):
        if not f.is_file():
            continue
        if f.suffix.lower() not in SUPPORTED_INPUT_EXT:
            continue
        # Versuche den Slug aus dem Dateinamen zu extrahieren
        stem = f.stem
        if stem in known_slugs:
            matches.append((f, stem))
            continue
        # Fuzzy: längster bekannter Slug, der im Dateinamen vorkommt
        possible = sorted(
            (s for s in known_slugs if s in stem),
            key=len,
            reverse=True,
        )
        if possible:
            matches.append((f, possible[0]))
    return matches


def convert_to_webp(source: Path, target: Path, width: int | None = None) -> int:
    """Konvertiert ein Bild zu WebP (optional resized). Gibt Dateigröße zurück."""
    target.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(source) as img:
        if img.mode in ("RGBA", "LA", "P"):
            img = img.convert("RGBA")
        else:
            img = img.convert("RGB")
        if width and img.width > width:
            ratio = width / img.width
            new_height = int(img.height * ratio)
            img = img.resize((width, new_height), Image.Resampling.LANCZOS)
        img.save(target, format="WEBP", quality=WEBP_QUALITY, method=6)
    return target.stat().st_size


def update_frontmatter_hero(slug: str, hero_path: str, dry_run: bool = False) -> bool:
    """Setzt heroImage im Frontmatter eines Artikels (sowohl src/content als auch content-prepared)."""
    changed = False
    for base in (CONTENT_BLOG, CONTENT_PREPARED):
        md = base / f"{slug}.md"
        if not md.exists():
            continue
        content = md.read_text(encoding="utf-8")
        if not content.startswith("---"):
            continue
        end = content.find("\n---\n", 4)
        if end < 0:
            continue
        fm = content[: end + 5]
        body = content[end + 5 :]

        new_hero_line = f'heroImage: "{hero_path}"'
        if "heroImage:" in fm:
            new_fm = re.sub(r'heroImage:\s*"[^"]*"', new_hero_line, fm)
        else:
            # Vor dem schließenden --- einfügen
            new_fm = fm.rstrip("\n---\n") + f"\n{new_hero_line}\n---\n"

        if new_fm != fm:
            if not dry_run:
                md.write_text(new_fm + body, encoding="utf-8")
            changed = True
            print(f"    Frontmatter aktualisiert: {md.relative_to(BASE_DIR)}")
    return changed


def format_size(b: int) -> str:
    if b < 1024:
        return f"{b} B"
    if b < 1024 * 1024:
        return f"{b/1024:.1f} KB"
    return f"{b/(1024*1024):.2f} MB"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        "source",
        nargs="?",
        default=str(Path.home() / "Downloads" / "wasgelingtmir-hero-images"),
        help="Quellordner mit den generierten Bildern",
    )
    parser.add_argument("--dry-run", action="store_true", help="Nichts schreiben, nur anzeigen")
    parser.add_argument("--no-responsive", action="store_true", help="Keine responsiven Varianten erzeugen")
    args = parser.parse_args()

    source = Path(args.source).expanduser()
    print(f"Quellordner: {source}")
    print(f"Trockenlauf: {args.dry_run}\n")

    known_slugs = load_known_slugs()
    print(f"Bekannte Artikel-Slugs: {len(known_slugs)}")

    matches = find_input_files(source, known_slugs)
    if not matches:
        print("\nKeine passenden Bilder gefunden.")
        print(f"Erwartet: <slug>.png/jpg/webp im Ordner {source}")
        return 0

    print(f"Gefundene Bilder zum Importieren: {len(matches)}\n")
    total_in = 0
    total_out = 0
    for src_file, slug in matches:
        print(f"📷 {src_file.name}  →  {slug}")
        target_dir = PUBLIC_IMAGES / slug
        target_main = target_dir / "hero.webp"
        in_size = src_file.stat().st_size
        total_in += in_size
        if args.dry_run:
            print(f"    [dry-run] würde anlegen: {target_main.relative_to(BASE_DIR)}")
        else:
            out_size = convert_to_webp(src_file, target_main, width=TARGET_WIDTH)
            total_out += out_size
            print(f"    Hauptbild: {format_size(in_size)} → {format_size(out_size)} (hero.webp)")
            if not args.no_responsive:
                for w in RESPONSIVE_WIDTHS:
                    variant = target_dir / f"hero-{w}w.webp"
                    convert_to_webp(src_file, variant, width=w)
                print(f"    Responsive Varianten: 400w, 800w, 1200w, 1600w")
        update_frontmatter_hero(slug, f"/images/blog/{slug}/hero.webp", dry_run=args.dry_run)
        print()

    print(f"\n=== Zusammenfassung ===")
    print(f"Importierte Bilder: {len(matches)}")
    if total_in:
        print(f"Original gesamt: {format_size(total_in)}")
    if total_out:
        saving = (1 - total_out / total_in) * 100 if total_in else 0
        print(f"WebP gesamt:     {format_size(total_out)} (-{saving:.0f} %)")
    if not args.dry_run:
        print(f"\nNächste Schritte:")
        print(f"  1) git status   — schau, was sich geändert hat")
        print(f"  2) npm run build && npm run preview — lokal testen (optional)")
        print(f"  3) git add -A && git commit -m 'feat: hero images for X articles'")
        print(f"  4) git push    — auf GitHub Pages live schieben")
    return 0


if __name__ == "__main__":
    sys.exit(main())
