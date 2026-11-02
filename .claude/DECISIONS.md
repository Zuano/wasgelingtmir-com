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

## 2026-11-02 – SEO-Grundausstattung: Vorschaubild, JSON-LD, Titelregel
**Entscheidung:**
- Standard-Vorschaubild `public/og-default.png` (1200×630) für Seiten ohne eigenes Titelbild; erzeugt mit `scripts/make-og-image.mjs` (nutzt das schon vorhandene Paket `sharp`).
- Strukturierte Daten (JSON-LD) in `BaseLayout.astro`: auf jeder Seite `WebSite`, auf Artikeln zusätzlich `BlogPosting` (Autor, Datum, Bild, Kategorie).
- Titelregel: „· wasgelingtmir.com“ wird nur angehängt, wenn der Titel dann höchstens 60 Zeichen hat (so viel zeigt Google ungefähr). Startseiten-Titel: „wasgelingtmir.com – Tipps zu Apple, Gesundheit & Ernährung“.
**Begründung:** Die Prüfung mit dem Skill „seobility-optimizer“ hat diese drei echten Lücken gezeigt. Bewusst NICHT übernommen: versteckter Fülltext, Teilen-Knöpfe und Wikipedia-Links nur für Punkte sowie `robots: index, follow` (wird nicht gebraucht). Grund: Das bringt Seobility-Punkte, aber keinen Nutzen für Leser oder Google, und versteckter Text kann sogar schaden.

## 2026-11-02 – Kurztitel über `seoTitle`
**Entscheidung:** Artikel und Seiten können im Kopfbereich ein `seoTitle` haben. Es ersetzt nur den `<title>` (Google, Browser-Tab, Teilen-Vorschau); die Überschrift im Artikel und `headline` in den strukturierten Daten bleiben der volle `title`.
**Begründung:** 13 Titel waren allein schon 64–124 Zeichen lang. Die Überschriften umzuschreiben hätte den Text verändert; ein eigenes Feld kürzt nur dort, wo Google abschneidet.
