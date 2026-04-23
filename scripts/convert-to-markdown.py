#!/usr/bin/env python3
"""
Konvertiert alle WordPress-Artikel aus dem XML-Export zu sauberen Markdown-Dateien
mit YAML-Frontmatter, bereinigten Bildpfaden und neuer Kategorisierung.
"""
import json
import re
import html
from pathlib import Path
from datetime import datetime
from urllib.parse import urlparse, unquote

from bs4 import BeautifulSoup
from markdownify import markdownify as md

BASE_DIR = Path(__file__).resolve().parent.parent
INVENTORY_JSON = BASE_DIR / ".claude" / "articles-inventory.json"
CATEGORIES_JSON = BASE_DIR / "scripts" / "new-categories.json"
OUTPUT_POSTS = BASE_DIR / "content-prepared" / "blog"
OUTPUT_PAGES = BASE_DIR / "content-prepared" / "pages"
IMAGES_MANIFEST = BASE_DIR / ".claude" / "images-manifest.json"

OUTPUT_POSTS.mkdir(parents=True, exist_ok=True)
OUTPUT_PAGES.mkdir(parents=True, exist_ok=True)


def slug_for(entry, slug_rewrites):
    original_slug = entry.get("slug", "")
    return slug_rewrites.get(original_slug, original_slug)


def clean_html_fragment(html_content: str) -> str:
    """Bereinigt WordPress-HTML vor der Markdown-Konvertierung."""
    # WordPress-Blockkommentare entfernen
    html_content = re.sub(r"<!--\s*/?wp:[^>]*-->", "", html_content)
    # WordPress-Shortcodes entfernen: [caption ...]...[/caption]
    html_content = re.sub(
        r"\[caption[^\]]*\](.*?)\[/caption\]",
        r"<figure>\1</figure>",
        html_content,
        flags=re.DOTALL,
    )
    # Sonstige einfache Shortcodes entfernen (z.B. [gallery], [embed ...])
    html_content = re.sub(r"\[/?(?:gallery|embed|audio|video)[^\]]*\]", "", html_content)
    # Leere p-Tags entfernen
    html_content = re.sub(r"<p>\s*</p>", "", html_content)
    return html_content


def is_image_filename_heading(text: str) -> bool:
    """Erkennt, ob eine Überschrift nur aus einem Bilddateinamen besteht."""
    t = text.strip().lower()
    return bool(re.match(r"^[\w\-\. ]+\.(png|jpe?g|gif|webp|heic)$", t))


def cleanup_soup_artifacts(soup: BeautifulSoup) -> None:
    """Entfernt Artefakte wie Bild-Dateinamen-Überschriften und leere Elemente."""
    for tag in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"]):
        text = tag.get_text(strip=True)
        if is_image_filename_heading(text):
            tag.decompose()
            continue
        # Leere Überschriften entfernen
        if not text:
            tag.decompose()
    # Leere Paragraphen mit nur whitespace oder &nbsp; entfernen
    for p in soup.find_all("p"):
        if not p.get_text(strip=True) and not p.find("img"):
            p.decompose()


def extract_and_rewrite_images(soup: BeautifulSoup, post_slug: str, year: str) -> list[dict]:
    """Sammelt alle <img>-Tags, schreibt src auf lokale Pfade um und gibt ein Manifest zurück."""
    images: list[dict] = []
    for img in soup.find_all("img"):
        src = img.get("src") or ""
        if not src:
            continue
        # Vollständiger URL → Dateiname extrahieren
        url_path = urlparse(src).path
        filename = unquote(Path(url_path).name)
        # Auflösung aus Dateinamen entfernen (WordPress fügt "-1024x768" an)
        clean_filename = re.sub(r"-\d+x\d+(?=\.[a-zA-Z]+$)", "", filename)

        # Alt-Text, Caption extrahieren
        alt = img.get("alt", "").strip()
        title = img.get("title", "").strip()

        # Neuer lokaler Pfad: /images/blog/<slug>/<filename>
        new_src = f"/images/blog/{post_slug}/{clean_filename}"
        img["src"] = new_src
        # Srcset, sizes entfernen – machen wir später mit Astro neu
        for attr in ["srcset", "sizes", "width", "height", "loading", "class", "decoding"]:
            if attr in img.attrs:
                del img.attrs[attr]

        images.append({
            "original_url": src,
            "local_path": new_src,
            "filename": clean_filename,
            "alt": alt,
            "title": title,
            "post_slug": post_slug,
            "year": year,
        })
    return images


def html_to_markdown(html_content: str) -> str:
    """Konvertiert HTML zu Markdown mit sinnvollen Einstellungen."""
    markdown = md(
        html_content,
        heading_style="ATX",       # # Überschrift statt underline
        bullets="-",               # - als Listenzeichen
        strong_em_symbol="*",      # *bold* und _italic_
        autolinks=True,
        default_title=False,
        code_language="",
        escape_asterisks=False,
        escape_underscores=False,
    )
    # Übermäßige Leerzeilen bereinigen
    markdown = re.sub(r"\n{3,}", "\n\n", markdown)
    # Trailing whitespace pro Zeile entfernen
    markdown = "\n".join(line.rstrip() for line in markdown.split("\n"))
    return markdown.strip() + "\n"


def yaml_frontmatter(data: dict) -> str:
    """Baut YAML-Frontmatter. Keine externen YAML-Libs nötig."""
    lines = ["---"]
    for key, value in data.items():
        if value is None:
            continue
        if isinstance(value, list):
            if not value:
                continue
            lines.append(f"{key}:")
            for v in value:
                safe = str(v).replace('"', '\\"')
                lines.append(f'  - "{safe}"')
        elif isinstance(value, bool):
            lines.append(f"{key}: {str(value).lower()}")
        elif isinstance(value, (int, float)):
            lines.append(f"{key}: {value}")
        else:
            safe = str(value).replace('"', '\\"').replace("\n", " ")
            lines.append(f'{key}: "{safe}"')
    lines.append("---\n")
    return "\n".join(lines)


def process_post(post: dict, config: dict, images_all: list[dict]) -> tuple[str, str, str] | None:
    slug = post["slug"]
    mapping = config["post_mapping"]
    cat_slug = mapping.get(slug)
    if cat_slug == "_skip_":
        print(f"  [SKIP] {slug}")
        return None
    if not cat_slug:
        print(f"  [WARN] Kein Mapping für: {slug} – als 'leben-gedanken' einsortiert")
        cat_slug = "leben-gedanken"
    new_slug = config["slug_rewrites"].get(slug, slug)

    category_info = config["_categories"][cat_slug]

    # HTML Entities im Titel bereinigen
    title = html.unescape(post["title"])

    # Datum formatieren (YYYY-MM-DD)
    date_str = post["date"][:10] if post["date"] else "2015-01-01"

    # HTML bereinigen und parsen
    raw_html = clean_html_fragment(post["content_html"])
    soup = BeautifulSoup(raw_html, "lxml")

    # Artefakte bereinigen (Bilddateinamen als Überschriften etc.)
    cleanup_soup_artifacts(soup)

    # Bilder extrahieren und umschreiben
    year = date_str[:4]
    images = extract_and_rewrite_images(soup, new_slug, year)
    images_all.extend(images)

    # Description aus erstem Absatz mit Content - separator=" " behebt fehlende Leerzeichen
    description = ""
    for p in soup.find_all("p"):
        txt = p.get_text(separator=" ", strip=True)
        txt = re.sub(r"\s+", " ", txt)
        if len(txt) >= 40:
            description = txt[:160].rstrip()
            # An Satzgrenze abschneiden falls möglich
            last_dot = description.rfind(". ")
            if last_dot > 80:
                description = description[: last_dot + 1]
            break
    if not description:
        # Fallback: erste sinnvolle Textzeile
        for p in soup.find_all("p"):
            txt = p.get_text(separator=" ", strip=True)
            if txt:
                description = re.sub(r"\s+", " ", txt)[:160]
                break

    # Tags bereinigen
    tags_clean = [html.unescape(t) for t in post["tags"]]

    # HTML → Markdown
    markdown_body = html_to_markdown(str(soup))

    # Alt-Texte werden später hinzugefügt, wenn Bilder konvertiert sind

    # Frontmatter
    fm = {
        "title": title,
        "description": description,
        "pubDate": date_str,
        "category": category_info["name"],
        "categorySlug": category_info["slug"],
        "tags": tags_clean,
        "slug": new_slug,
        "heroImage": images[0]["local_path"] if images else None,
        "originalUrl": post["link"],
        "wordpressId": post["id"],
    }

    content = yaml_frontmatter(fm) + "\n" + markdown_body
    return new_slug, cat_slug, content


def process_page(page: dict, config: dict, images_all: list[dict]) -> tuple[str, str] | None:
    slug = page["slug"]
    if slug in config["pages_to_skip"]:
        print(f"  [SKIP Page] {slug}")
        return None
    if slug not in config["pages_to_keep"]:
        print(f"  [WARN Page] Unbekannte Seite: {slug}")
        return None
    new_slug = config.get("page_slug_rewrites", {}).get(slug, slug)

    title = html.unescape(page["title"])
    date_str = page["date"][:10] if page["date"] else "2015-01-01"
    raw_html = clean_html_fragment(page["content_html"])
    soup = BeautifulSoup(raw_html, "lxml")
    cleanup_soup_artifacts(soup)
    images = extract_and_rewrite_images(soup, new_slug, date_str[:4])
    images_all.extend(images)
    markdown_body = html_to_markdown(str(soup))
    description = ""
    for p in soup.find_all("p"):
        txt = re.sub(r"\s+", " ", p.get_text(separator=" ", strip=True))
        if len(txt) >= 40:
            description = txt[:160].rstrip()
            break
    if not description:
        for p in soup.find_all("p"):
            txt = re.sub(r"\s+", " ", p.get_text(separator=" ", strip=True))
            if txt:
                description = txt[:160]
                break

    fm = {
        "title": title,
        "description": description,
        "pubDate": date_str,
        "slug": new_slug,
        "type": "page",
        "originalUrl": page["link"],
    }
    return new_slug, yaml_frontmatter(fm) + "\n" + markdown_body


def main():
    print("Lese Inventar und Kategorien-Mapping...")
    with open(INVENTORY_JSON, encoding="utf-8") as f:
        inventory = json.load(f)
    with open(CATEGORIES_JSON, encoding="utf-8") as f:
        config = json.load(f)

    images_all: list[dict] = []

    print(f"\nKonvertiere {len(inventory['posts'])} Artikel...")
    converted_posts = 0
    skipped_posts = 0
    for post in inventory["posts"]:
        result = process_post(post, config, images_all)
        if result is None:
            skipped_posts += 1
            continue
        new_slug, cat_slug, content = result
        out_file = OUTPUT_POSTS / f"{new_slug}.md"
        out_file.write_text(content, encoding="utf-8")
        converted_posts += 1
        print(f"  [OK] {out_file.name} (Kategorie: {cat_slug})")

    print(f"\nKonvertiere Seiten ({len(inventory['pages'])} insgesamt)...")
    converted_pages = 0
    for page in inventory["pages"]:
        result = process_page(page, config, images_all)
        if result is None:
            continue
        new_slug, content = result
        out_file = OUTPUT_PAGES / f"{new_slug}.md"
        out_file.write_text(content, encoding="utf-8")
        converted_pages += 1
        print(f"  [OK] {out_file.name}")

    # Image Manifest speichern
    with open(IMAGES_MANIFEST, "w", encoding="utf-8") as f:
        json.dump(images_all, f, indent=2, ensure_ascii=False)

    print(f"\n=== Fertig ===")
    print(f"Artikel konvertiert: {converted_posts} (übersprungen: {skipped_posts})")
    print(f"Seiten konvertiert: {converted_pages}")
    print(f"Gefundene Bild-Referenzen: {len(images_all)}")
    print(f"Manifest: {IMAGES_MANIFEST}")


if __name__ == "__main__":
    main()
