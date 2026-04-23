#!/usr/bin/env python3
"""
Verarbeitet alle Bilder aus dem WordPress-Export:
- Findet Original im lokalen Medien-Export (mit Fuzzy-Matching für Größen-Suffixe)
- Kopiert Original in public/images/blog/<slug>/
- Konvertiert zu WebP
- Erzeugt responsive Varianten (400, 800, 1200 Breite)
- Loggt Statistiken und fehlende Bilder
"""
import json
import re
import shutil
from pathlib import Path
from urllib.parse import urlparse, unquote

import requests
from PIL import Image

BASE_DIR = Path(__file__).resolve().parent.parent
MEDIA_DIR = BASE_DIR / "export-wordpress" / "media-export-98317367-from-0-to-2157"
MANIFEST_FILE = BASE_DIR / ".claude" / "images-manifest.json"
OUTPUT_DIR = BASE_DIR / "public" / "images" / "blog"
REPORT_FILE = BASE_DIR / ".claude" / "images-report.md"

RESPONSIVE_WIDTHS = [400, 800, 1200]
WEBP_QUALITY = 82
JPEG_FALLBACK_QUALITY = 85

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def find_local_image(original_url: str) -> Path | None:
    """Sucht das Original-Bild im lokalen Medien-Export."""
    path = urlparse(original_url).path  # /wp-content/uploads/2024/09/amazon-payback-logo.png
    path = unquote(path)
    # Wir suchen alles ab YYYY/MM/... (also nach /uploads/)
    m = re.search(r"/(\d{4}/\d{2}/[^?]+)$", path)
    if not m:
        return None
    relative = m.group(1)  # 2024/09/amazon-payback-logo.png
    candidate = MEDIA_DIR / relative
    if candidate.exists():
        return candidate
    # Fuzzy: Manchmal hat WP -1.ext, -2.ext oder Größensuffix wie -1024x768
    filename = Path(relative).name
    stem = Path(filename).stem
    suffix = Path(filename).suffix
    parent = MEDIA_DIR / Path(relative).parent
    if parent.exists():
        # Versuche ohne -NxN Suffix
        base_stem = re.sub(r"-\d+x\d+$", "", stem)
        for f in parent.iterdir():
            if f.name.startswith(base_stem) and f.suffix.lower() == suffix.lower():
                return f
    return None


def download_image(url: str, target: Path) -> bool:
    """Lädt ein Bild herunter als Fallback, wenn es lokal nicht gefunden wurde."""
    try:
        clean_url = url.split("?")[0]  # Query-Parameter wie ?w=1024 entfernen
        resp = requests.get(clean_url, timeout=15)
        if resp.status_code == 200:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(resp.content)
            return True
    except Exception as e:
        print(f"    Download-Fehler: {e}")
    return False


def convert_to_webp(source: Path, target: Path, width: int | None = None) -> int:
    """Konvertiert ein Bild zu WebP, optional mit einer bestimmten Breite. Gibt Dateigröße zurück."""
    target.parent.mkdir(parents=True, exist_ok=True)
    try:
        with Image.open(source) as img:
            # GIFs mit Animation: behalten wir als GIF, kein WebP
            if img.format == "GIF" and getattr(img, "is_animated", False):
                # Animierten GIFs werden einfach kopiert
                shutil.copy2(source, target.with_suffix(".gif"))
                return target.with_suffix(".gif").stat().st_size

            # Transparenz-Handling
            if img.mode in ("RGBA", "LA", "P"):
                img = img.convert("RGBA") if img.mode != "P" else img.convert("RGBA")
            else:
                img = img.convert("RGB")

            if width and img.width > width:
                ratio = width / img.width
                new_height = int(img.height * ratio)
                img = img.resize((width, new_height), Image.Resampling.LANCZOS)

            img.save(target, format="WEBP", quality=WEBP_QUALITY, method=6)
            return target.stat().st_size
    except Exception as e:
        print(f"    [Error] WebP-Konvertierung fehlgeschlagen: {e}")
        return 0


def process_image(img_entry: dict) -> dict:
    slug = img_entry["post_slug"]
    original_url = img_entry["original_url"]
    filename = img_entry["filename"]
    dest_dir = OUTPUT_DIR / slug
    dest_dir.mkdir(parents=True, exist_ok=True)
    status = {
        "slug": slug,
        "filename": filename,
        "source": None,
        "original_size": 0,
        "webp_size": 0,
        "variants": {},
        "error": None,
    }

    local_source = find_local_image(original_url)
    if local_source is None:
        # Fallback: herunterladen
        tmp_path = dest_dir / filename
        if download_image(original_url, tmp_path):
            local_source = tmp_path
            status["source"] = "downloaded"
        else:
            status["error"] = f"Bild weder lokal gefunden noch downloadbar: {original_url}"
            return status
    else:
        status["source"] = str(local_source.relative_to(BASE_DIR))
        # Original kopieren
        tmp_path = dest_dir / filename
        if not tmp_path.exists():
            shutil.copy2(local_source, tmp_path)

    original_path = dest_dir / filename
    status["original_size"] = original_path.stat().st_size

    # Haupt-WebP (volle Auflösung, nur komprimiert)
    stem = Path(filename).stem
    webp_main = dest_dir / f"{stem}.webp"

    # Animierte GIFs: nicht zu WebP konvertieren
    try:
        with Image.open(local_source) as img:
            is_anim = img.format == "GIF" and getattr(img, "is_animated", False)
    except Exception:
        is_anim = False

    if is_anim:
        status["webp_size"] = status["original_size"]
        status["variants"]["original"] = status["original_size"]
        return status

    status["webp_size"] = convert_to_webp(local_source, webp_main)

    # Responsive Varianten
    try:
        with Image.open(local_source) as img:
            orig_width = img.width
    except Exception:
        orig_width = 0

    for w in RESPONSIVE_WIDTHS:
        if orig_width and orig_width > w:
            variant_path = dest_dir / f"{stem}-{w}w.webp"
            size = convert_to_webp(local_source, variant_path, width=w)
            if size:
                status["variants"][f"{w}w"] = size

    return status


def format_size(bytes_: int) -> str:
    if bytes_ < 1024:
        return f"{bytes_} B"
    if bytes_ < 1024 * 1024:
        return f"{bytes_ / 1024:.1f} KB"
    return f"{bytes_ / (1024 * 1024):.2f} MB"


def main():
    with open(MANIFEST_FILE, encoding="utf-8") as f:
        manifest = json.load(f)

    # Duplikate vermeiden (gleiche URL kommt teils mehrmals vor)
    seen = set()
    unique_images = []
    for img in manifest:
        key = (img["post_slug"], img["filename"])
        if key in seen:
            continue
        seen.add(key)
        unique_images.append(img)

    print(f"Verarbeite {len(unique_images)} einzigartige Bilder...\n")

    results = []
    total_original = 0
    total_webp = 0
    errors = []
    downloaded = 0

    for i, img in enumerate(unique_images, 1):
        print(f"[{i}/{len(unique_images)}] {img['post_slug']}/{img['filename']}")
        r = process_image(img)
        results.append(r)
        if r["error"]:
            errors.append(r)
            print(f"    [Fehlt] {r['error']}")
            continue
        if r["source"] == "downloaded":
            downloaded += 1
        total_original += r["original_size"]
        total_webp += r["webp_size"]
        saving_pct = 0
        if r["original_size"]:
            saving_pct = (1 - r["webp_size"] / r["original_size"]) * 100
        print(
            f"    {format_size(r['original_size'])} → {format_size(r['webp_size'])} "
            f"(-{saving_pct:.0f}%)"
        )

    # Report schreiben
    lines = ["# Bild-Verarbeitungs-Report\n"]
    lines.append(f"- **Einzigartige Bilder:** {len(unique_images)}")
    lines.append(f"- **Lokal gefunden:** {len(unique_images) - downloaded - len(errors)}")
    lines.append(f"- **Heruntergeladen:** {downloaded}")
    lines.append(f"- **Fehler:** {len(errors)}")
    lines.append(f"- **Gesamt vorher:** {format_size(total_original)}")
    lines.append(f"- **Gesamt nachher (WebP):** {format_size(total_webp)}")
    if total_original:
        saving = (1 - total_webp / total_original) * 100
        lines.append(f"- **Einsparung:** {saving:.1f} %\n")

    if errors:
        lines.append("\n## Fehlende / fehlerhafte Bilder\n")
        for e in errors:
            lines.append(f"- `{e['slug']}/{e['filename']}`: {e['error']}")

    REPORT_FILE.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nReport geschrieben: {REPORT_FILE}")

    # Manifest aktualisieren
    processed_manifest = BASE_DIR / ".claude" / "images-processed.json"
    with open(processed_manifest, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\n=== Zusammenfassung ===")
    print(f"Bilder verarbeitet: {len(unique_images) - len(errors)}")
    print(f"Fehler: {len(errors)}")
    if total_original:
        print(f"Größe: {format_size(total_original)} → {format_size(total_webp)} (-{saving:.1f}%)")


if __name__ == "__main__":
    main()
