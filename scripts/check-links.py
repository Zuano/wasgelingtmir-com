#!/usr/bin/env python3
"""
Prüft alle externen Links in den konvertierten Markdown-Artikeln auf Erreichbarkeit.
Schreibt einen Report nach .claude/link-check-report.md
"""
import re
import json
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

BASE_DIR = Path(__file__).resolve().parent.parent
CONTENT_DIR = BASE_DIR / "content-prepared"
REPORT_FILE = BASE_DIR / ".claude" / "link-check-report.md"
RESULTS_JSON = BASE_DIR / ".claude" / "link-check-results.json"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/605.1.15 "
                  "(KHTML, like Gecko) Version/17.0 Safari/605.1.15"
}
TIMEOUT = 15


def make_session():
    s = requests.Session()
    retry = Retry(total=2, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
    s.mount("https://", HTTPAdapter(max_retries=retry))
    s.mount("http://", HTTPAdapter(max_retries=retry))
    s.headers.update(HEADERS)
    return s


SESSION = make_session()


def check_url(url: str) -> dict:
    result = {"url": url, "status": None, "error": None, "redirect": None}
    try:
        # Erst HEAD versuchen, wenn das 405/403 liefert GET
        r = SESSION.head(url, timeout=TIMEOUT, allow_redirects=True)
        if r.status_code in (405, 403, 400):
            r = SESSION.get(url, timeout=TIMEOUT, allow_redirects=True, stream=True)
            r.close()
        result["status"] = r.status_code
        if r.history:
            result["redirect"] = r.url
    except requests.exceptions.Timeout:
        result["error"] = "timeout"
    except requests.exceptions.SSLError as e:
        result["error"] = f"ssl_error: {e}"[:200]
    except requests.exceptions.ConnectionError:
        result["error"] = "connection_error"
    except Exception as e:
        result["error"] = f"{type(e).__name__}: {e}"[:200]
    return result


def extract_links_from_md(file_path: Path) -> list[tuple[str, str]]:
    """Extrahiert alle Markdown-Links [text](url) und gibt (file, url) zurück."""
    content = file_path.read_text(encoding="utf-8")
    # Einfacher Markdown-Link-Regex
    links = re.findall(r"\[([^\]]*)\]\((https?://[^)\s]+)\)", content)
    return [(text, url.rstrip(".,;:")) for text, url in links]


def main():
    md_files = list((CONTENT_DIR / "blog").glob("*.md")) + list((CONTENT_DIR / "pages").glob("*.md"))
    all_links: dict[str, list[str]] = {}  # url -> list of filenames

    for f in md_files:
        for text, url in extract_links_from_md(f):
            # Bilder-URLs /images/... überspringen
            if url.startswith("/images/"):
                continue
            all_links.setdefault(url, []).append(f.name)

    unique_urls = list(all_links.keys())
    print(f"Gefundene einzigartige externe URLs: {len(unique_urls)}\n")

    results = {}
    with ThreadPoolExecutor(max_workers=8) as ex:
        futures = {ex.submit(check_url, u): u for u in unique_urls}
        for i, fut in enumerate(as_completed(futures), 1):
            url = futures[fut]
            r = fut.result()
            results[url] = r
            status_info = r["status"] or r["error"] or "?"
            marker = "OK" if r["status"] and 200 <= r["status"] < 400 else "FAIL"
            print(f"[{i}/{len(unique_urls)}] {marker} {status_info} {url[:80]}")

    ok = [u for u, r in results.items() if r["status"] and 200 <= r["status"] < 400]
    redirected = [u for u, r in results.items() if r["redirect"]]
    failed = [u for u, r in results.items() if not (r["status"] and 200 <= r["status"] < 400)]

    # Report schreiben
    lines = ["# Link-Check Report\n"]
    lines.append(f"- **Geprüfte URLs:** {len(unique_urls)}")
    lines.append(f"- **Erreichbar (2xx/3xx):** {len(ok)}")
    lines.append(f"- **Mit Weiterleitung:** {len(redirected)}")
    lines.append(f"- **Fehler / nicht erreichbar:** {len(failed)}\n")

    if failed:
        lines.append("\n## Fehlerhafte / tote Links\n")
        for u in failed:
            r = results[u]
            files = ", ".join(sorted(set(all_links[u])))
            status = r["status"] or r["error"]
            lines.append(f"- **{status}** – `{u}`")
            lines.append(f"  - In Dateien: {files}")

    if redirected:
        lines.append("\n## Weiterleitungen (URL sollte aktualisiert werden)\n")
        for u in redirected:
            r = results[u]
            if r["redirect"] != u:
                files = ", ".join(sorted(set(all_links[u])))
                lines.append(f"- `{u}`")
                lines.append(f"  - → `{r['redirect']}`")
                lines.append(f"  - In Dateien: {files}")

    REPORT_FILE.write_text("\n".join(lines), encoding="utf-8")
    with open(RESULTS_JSON, "w", encoding="utf-8") as f:
        json.dump({"results": results, "files_by_url": all_links}, f, indent=2, ensure_ascii=False)

    print(f"\nReport: {REPORT_FILE}")


if __name__ == "__main__":
    main()
