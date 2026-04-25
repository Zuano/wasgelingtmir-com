#!/usr/bin/env python3
"""
generate-with-openai.py

Optionales Script: Generiert alle Hero-Bilder automatisch via OpenAI Image API
und legt sie im Standard-Quellordner ab. Anschließend kannst du
import-hero-images.py laufen lassen.

Voraussetzungen:
    pip install openai
    export OPENAI_API_KEY=sk-...     (Key auf https://platform.openai.com/api-keys)

Kosten (Stand 2026-04):
    gpt-image-1 high   → ca. $0.19 pro Bild
    gpt-image-1 medium → ca. $0.07 pro Bild
    gpt-image-1 low    → ca. $0.02 pro Bild
    Bei 24 Bildern: ca. $0.50 (low) – $4.50 (high)

Usage:
    # Nur die 6 dringend nötigen
    python3 scripts/generate-with-openai.py --priority critical

    # Alle 24 Artikel
    python3 scripts/generate-with-openai.py --priority all

    # Mit niedriger Qualität (= günstiger zum Testen)
    python3 scripts/generate-with-openai.py --priority critical --quality low

    # In anderen Ordner ablegen
    python3 scripts/generate-with-openai.py --output /pfad/ordner
"""
from __future__ import annotations
import argparse
import base64
import json
import os
import sys
import time
from pathlib import Path

try:
    from openai import OpenAI
except ImportError:
    print("Fehlt: pip install openai")
    sys.exit(1)

BASE_DIR = Path(__file__).resolve().parent.parent
PROMPTS_JSON = BASE_DIR / "scripts" / "hero-image-prompts.json"
DEFAULT_OUTPUT = Path.home() / "Downloads" / "wasgelingtmir-hero-images"

PRIORITY_GROUPS = {
    "critical": ["priority_critical"],
    "recommended": ["priority_critical", "priority_recommended"],
    "all": ["priority_critical", "priority_recommended", "priority_optional"],
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        "--priority",
        choices=["critical", "recommended", "all"],
        default="critical",
        help="Welche Artikel? critical=6, recommended=18, all=24",
    )
    parser.add_argument(
        "--quality",
        choices=["low", "medium", "high"],
        default="medium",
        help="Qualität (=Kosten). low ist gut zum Testen.",
    )
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT), help="Zielordner für die Bilder")
    parser.add_argument("--model", default="gpt-image-1", help="OpenAI Modell")
    parser.add_argument("--size", default="1536x1024", help="Bildgröße (1024x1024, 1536x1024, 1024x1536, auto)")
    parser.add_argument("--skip-existing", action="store_true", help="Bilder, die schon vorhanden sind, überspringen")
    args = parser.parse_args()

    if "OPENAI_API_KEY" not in os.environ:
        print("Fehlt: export OPENAI_API_KEY=sk-...")
        return 1

    output_dir = Path(args.output).expanduser()
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"Zielordner: {output_dir}")

    with open(PROMPTS_JSON, encoding="utf-8") as f:
        prompts_data = json.load(f)

    style_suffix = prompts_data.get("_style_suffix", "")
    entries = []
    for group in PRIORITY_GROUPS[args.priority]:
        entries.extend(prompts_data.get(group, []))
    print(f"Generiere {len(entries)} Bilder (Qualität: {args.quality}, Größe: {args.size})\n")

    client = OpenAI()
    success = 0
    failed = []

    for i, entry in enumerate(entries, 1):
        slug = entry["slug"]
        target = output_dir / f"{slug}.png"
        if args.skip_existing and target.exists():
            print(f"[{i}/{len(entries)}] {slug}  (übersprungen, existiert bereits)")
            success += 1
            continue
        full_prompt = f"{entry['prompt']}\n\n{style_suffix}"
        print(f"[{i}/{len(entries)}] {slug}")
        print(f"    Titel: {entry['title']}")
        try:
            t0 = time.time()
            resp = client.images.generate(
                model=args.model,
                prompt=full_prompt,
                size=args.size,
                quality=args.quality,
                n=1,
            )
            duration = time.time() - t0
            b64 = resp.data[0].b64_json
            target.write_bytes(base64.b64decode(b64))
            print(f"    Gespeichert in {duration:.1f}s: {target.relative_to(Path.home())}")
            success += 1
        except Exception as e:
            print(f"    [Fehler] {e}")
            failed.append(slug)
        # Kleine Pause gegen Rate-Limit
        time.sleep(2)

    print(f"\n=== Fertig ===")
    print(f"Erfolgreich: {success}/{len(entries)}")
    if failed:
        print(f"Fehlgeschlagen ({len(failed)}):")
        for s in failed:
            print(f"  - {s}")
    print(f"\nNächster Schritt:")
    print(f"  python3 scripts/import-hero-images.py {output_dir}")
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
