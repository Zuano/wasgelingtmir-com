# Technische Entscheidungen – wasgelingtmir.com

## 2026-04-23 – Framework: Astro
**Entscheidung:** Astro als Static Site Generator.
**Begründung:**
- Sehr schnelle Ladezeiten (versendet fast kein JavaScript)
- Markdown-Artikel direkt unterstützt (einfach zu pflegen für Vibe Coder)
- Gute Bildoptimierung eingebaut (automatische WebP-Konvertierung, responsive Bilder)
- Große aktive Community, ausführliche Doku auf Deutsch verfügbar
- Alternative wäre Hugo (Go-basiert, auch schnell) oder 11ty – Astro gewählt wegen besserer Entwickler-Erfahrung und moderner Komponenten-Syntax

## 2026-04-23 – Hosting: GitHub Pages
**Entscheidung:** GitHub Pages für das Hosting.
**Begründung:**
- Kostenlos
- Eigene Domain möglich (wasgelingtmir.com)
- Automatisches HTTPS via Let's Encrypt
- Automatisches Deployment via GitHub Actions
- Git-basierter Workflow passt zu statischer Seite
- Alternativen: Netlify, Vercel, Cloudflare Pages – alle gut, aber GitHub Pages reicht und ist direkt mit dem Repo verbunden

## 2026-04-23 – Bildformat: WebP
**Entscheidung:** Alle Bilder werden zu WebP konvertiert (mit JPEG-Fallback für ganz alte Browser).
**Begründung:**
- 50–80 % kleinere Dateigröße bei gleicher Qualität im Vergleich zu JPEG/PNG
- Von allen modernen Browsern unterstützt (>95 % weltweit)
- Astro unterstützt WebP nativ via `@astrojs/image`

## 2026-04-23 – Domain bleibt bestehen
**Entscheidung:** Die Domain wasgelingtmir.com wird auf GitHub Pages umgeleitet.
**Begründung:**
- Bestehende Besucher, SEO-Rankings, interne Verlinkung bleiben erhalten
- Keine 301-Redirects auf neue Domain nötig

## 2026-04-23 – Automatische Fehlerkorrektur
**Entscheidung:** Gefundene Fehler (Rechtschreibung, Grammatik, tote Links) werden automatisch korrigiert, alle Änderungen aber in `CHANGELOG-articles.md` dokumentiert.
**Begründung:**
- User-Wunsch nach effizientem Workflow
- Trotzdem volle Nachvollziehbarkeit: User kann jede Änderung einzeln nachlesen und ggf. rückgängig machen
