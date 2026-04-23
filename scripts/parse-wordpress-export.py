#!/usr/bin/env python3
"""
WordPress Export Parser
Liest die WordPress XML-Export-Datei und erstellt ein Inventar aller Artikel und Seiten.
"""
import xml.etree.ElementTree as ET
import json
import re
from pathlib import Path
from datetime import datetime

# Pfade
BASE_DIR = Path(__file__).resolve().parent.parent
XML_FILE = BASE_DIR / "export-wordpress" / "zuano039santwortenfinden.WordPress.2026-04-23.xml"
OUTPUT_DIR = BASE_DIR / ".claude"
OUTPUT_DIR.mkdir(exist_ok=True)

# WordPress-Namespaces
NS = {
    "content": "http://purl.org/rss/1.0/modules/content/",
    "wp": "http://wordpress.org/export/1.2/",
    "dc": "http://purl.org/dc/elements/1.1/",
    "excerpt": "http://wordpress.org/export/1.2/excerpt/",
}


def clean_text(text: str | None) -> str:
    if not text:
        return ""
    return text.strip()


def strip_html(html: str) -> str:
    """Entfernt HTML-Tags für Preview."""
    if not html:
        return ""
    text = re.sub(r"<[^>]+>", " ", html)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def parse_item(item) -> dict:
    title = clean_text(item.findtext("title"))
    link = clean_text(item.findtext("link"))
    pub_date = clean_text(item.findtext("pubDate"))
    creator = clean_text(item.findtext("dc:creator", namespaces=NS))
    content = clean_text(item.findtext("content:encoded", namespaces=NS))
    excerpt = clean_text(item.findtext("excerpt:encoded", namespaces=NS))
    post_id = clean_text(item.findtext("wp:post_id", namespaces=NS))
    post_date = clean_text(item.findtext("wp:post_date", namespaces=NS))
    post_name = clean_text(item.findtext("wp:post_name", namespaces=NS))
    post_type = clean_text(item.findtext("wp:post_type", namespaces=NS))
    status = clean_text(item.findtext("wp:status", namespaces=NS))

    # Kategorien und Tags
    categories = []
    tags = []
    for cat in item.findall("category"):
        domain = cat.get("domain", "")
        name = clean_text(cat.text)
        if domain == "category":
            categories.append(name)
        elif domain == "post_tag":
            tags.append(name)

    # Word count
    plain_text = strip_html(content)
    word_count = len(plain_text.split())

    # Bilder im Content zählen
    image_count = len(re.findall(r"<img[^>]+>", content, re.IGNORECASE))

    # Externe Links zählen
    links = re.findall(r'<a[^>]+href=["\']([^"\']+)["\']', content, re.IGNORECASE)
    external_links = [l for l in links if l.startswith("http") and "wasgelingtmir.com" not in l]

    return {
        "id": post_id,
        "type": post_type,
        "status": status,
        "title": title,
        "slug": post_name,
        "date": post_date,
        "link": link,
        "creator": creator,
        "categories": categories,
        "tags": tags,
        "word_count": word_count,
        "image_count": image_count,
        "external_links_count": len(external_links),
        "external_links": external_links,
        "excerpt": excerpt or plain_text[:200] + "..." if len(plain_text) > 200 else plain_text,
        "content_html": content,
    }


def main():
    print(f"Lese XML: {XML_FILE}")
    tree = ET.parse(XML_FILE)
    root = tree.getroot()
    channel = root.find("channel")

    # Site-Metadaten
    site_title = clean_text(channel.findtext("title"))
    site_link = clean_text(channel.findtext("link"))
    site_description = clean_text(channel.findtext("description"))

    items = channel.findall("item")
    posts = []
    pages = []
    attachments = []

    for item in items:
        parsed = parse_item(item)
        if parsed["type"] == "post" and parsed["status"] == "publish":
            posts.append(parsed)
        elif parsed["type"] == "page" and parsed["status"] == "publish":
            pages.append(parsed)
        elif parsed["type"] == "attachment":
            attachments.append(parsed)

    # Sortieren nach Datum
    posts.sort(key=lambda x: x["date"], reverse=True)
    pages.sort(key=lambda x: x["date"])

    # Inventar schreiben (JSON für späteres Processing)
    inventory = {
        "site": {
            "title": site_title,
            "link": site_link,
            "description": site_description,
            "export_date": datetime.now().isoformat(),
        },
        "posts": posts,
        "pages": pages,
        "attachments_count": len(attachments),
    }

    json_path = OUTPUT_DIR / "articles-inventory.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(inventory, f, indent=2, ensure_ascii=False)
    print(f"JSON-Inventar geschrieben: {json_path}")

    # Lesbares Markdown-Inventar
    md_lines = []
    md_lines.append(f"# Artikel-Inventar – {site_title}\n")
    md_lines.append(f"**Site-URL:** {site_link}  ")
    md_lines.append(f"**Beschreibung:** {site_description}  ")
    md_lines.append(f"**Exportiert:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    md_lines.append(f"**Zahlen:** {len(posts)} Artikel · {len(pages)} Seiten · {len(attachments)} Medien-Anhänge\n")

    md_lines.append("\n---\n")
    md_lines.append("## Blogartikel (sortiert nach Datum, neueste zuerst)\n")
    md_lines.append("| # | Datum | Titel | Kategorie | Wörter | Bilder | Ext. Links |")
    md_lines.append("|---|---|---|---|---|---|---|")
    for i, p in enumerate(posts, 1):
        cats = ", ".join(p["categories"]) or "—"
        date_str = p["date"][:10] if p["date"] else "—"
        title = p["title"].replace("|", "\\|")
        md_lines.append(
            f"| {i} | {date_str} | {title} | {cats} | {p['word_count']} | {p['image_count']} | {p['external_links_count']} |"
        )

    md_lines.append("\n---\n")
    md_lines.append("## Seiten (Pages)\n")
    md_lines.append("| # | Titel | Slug | Wörter |")
    md_lines.append("|---|---|---|---|")
    for i, p in enumerate(pages, 1):
        title = p["title"].replace("|", "\\|") or "(ohne Titel)"
        md_lines.append(f"| {i} | {title} | {p['slug']} | {p['word_count']} |")

    md_lines.append("\n---\n")
    md_lines.append("## Statistiken\n")
    total_words = sum(p["word_count"] for p in posts)
    total_images = sum(p["image_count"] for p in posts)
    total_ext_links = sum(p["external_links_count"] for p in posts)
    md_lines.append(f"- **Gesamt-Wortzahl (Artikel):** {total_words:,}")
    md_lines.append(f"- **Bilder in Artikeln (inline):** {total_images}")
    md_lines.append(f"- **Externe Links gesamt:** {total_ext_links}")
    all_cats = {}
    for p in posts:
        for c in p["categories"]:
            all_cats[c] = all_cats.get(c, 0) + 1
    md_lines.append(f"\n**Kategorien-Verteilung:**")
    for cat, count in sorted(all_cats.items(), key=lambda x: -x[1]):
        md_lines.append(f"- {cat}: {count} Artikel")

    md_path = OUTPUT_DIR / "articles-inventory.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))
    print(f"Markdown-Inventar geschrieben: {md_path}")

    print(f"\n=== Zusammenfassung ===")
    print(f"Artikel: {len(posts)}")
    print(f"Seiten: {len(pages)}")
    print(f"Medien: {len(attachments)}")
    print(f"Gesamt-Wortzahl: {total_words:,}")
    print(f"Kategorien: {list(all_cats.keys())}")


if __name__ == "__main__":
    main()
