# TODO – wasgelingtmir.com Neuaufbau

Siehe auch: [`DOCUMENTATION.md`](./DOCUMENTATION.md) · [`plan.md`](./plan.md)

## Gerade in Arbeit
- 🔄 Manuelles Lektorat aller 24 Artikel (Rechtschreibung, Grammatik, Formatierung)
- 🔄 Veraltete Infos markieren und Hinweise einbauen

## Als nächstes
- [ ] Astro-Projekt aufsetzen in `src/`
- [ ] Content-Collections in Astro konfigurieren
- [ ] Basis-Layout und Typografie
- [ ] Startseite mit Neuen Artikeln
- [ ] Kategorie-Seiten
- [ ] Such-Funktion
- [ ] RSS-Feed
- [ ] Sitemap + robots.txt
- [x] SEO (Meta-Tags, Open Graph, structured data) – Grundausstattung 2026-11-02
- [x] Zu lange Titel: 13 Seiten haben jetzt ein kürzeres `seoTitle` (2026-11-02)
- [ ] Artikel „Wie fühlt es sich an, zu hören: Den ...“ hat einen abgeschnittenen Titel → mit Christian klären
- [ ] Manche Artikel-Beschreibungen zu kurz (<120) oder zu lang (>160) Zeichen
- [ ] Performance-Check (Lighthouse-Ziel 95+)

## GitHub & Deployment
- [ ] Git-Repo lokal initialisieren mit sinnvollen Commits
- [ ] GitHub-Repo `wasgelingtmir-com` anlegen (Account Zuano)
- [ ] GitHub Actions Workflow `deploy.yml` für Pages
- [ ] Test-Deployment prüfen
- [ ] CNAME-Datei für eigene Domain

## Domain-Umzug (gemeinsam mit User)
- [ ] Prüfen, wo die Domain registriert ist
- [ ] DNS-Records auf GitHub Pages umstellen (4× A-Records + CNAME)
- [ ] HTTPS-Zertifikat aktivieren (Let's Encrypt via GitHub)
- [ ] Alte WordPress-Seite auf Wartungsseite oder Weiterleitung stellen
- [ ] WordPress.com-Abo ggf. kündigen

## Änderungsprotokoll
- **2026-04-23** Projekt gestartet, Plan + Doku erstellt.
- **2026-04-23** GitHub-Auth geprüft: Account "Zuano" aktiv, Rechte ausreichend.
- **2026-04-23** Website-Analyse abgeschlossen: WordPress.com, ca. 25–30 Artikel.
- **2026-04-23** WordPress-Export eingelesen: 25 Artikel, 8 Seiten, 148 Medien, 22 Kommentare.
- **2026-04-23** Python-Environment aufgesetzt (markdownify, beautifulsoup4, Pillow, requests, pyspellchecker, lxml).
- **2026-04-23** Artikel-Inventar erstellt (siehe `articles-inventory.md`).
- **2026-04-23** Kategorien neu strukturiert: Apple & Mac, Web & Dienste, Gesundheit, Ernährung, Leben & Gedanken.
- **2026-04-23** 24 Artikel + 4 Seiten zu Markdown konvertiert; "Hallo Welt!" und leere Seiten übersprungen.
- **2026-04-23** 95 Bilder zu WebP + responsive Varianten verarbeitet; **-70 % Größe** (17,10 MB → 5,12 MB).
- **2026-04-23** Linkprüfung: 26 externe URLs geprüft, 14 Weiterleitungen automatisch angewendet, 4 tote Links mit sinnvollen Ersatz-URLs versehen.
- **2026-04-23** Zentrale Doku (`README.md`, `DOCUMENTATION.md`) angelegt.
- **2026-04-23** Astro 5 + Tailwind CSS v4 Projekt aufgesetzt mit Layouts, Komponenten und Seiten.
- **2026-04-23** Pagefind-Suche integriert (2329 Wörter indiziert, komplett clientseitig, keine Server).
- **2026-04-23** Erste Astro-Build erfolgreich: 37 Seiten in 1,56 s gebaut.
- **2026-04-23** GitHub-Repository angelegt (https://github.com/Zuano/wasgelingtmir-com).
- **2026-04-23** GitHub Actions Deployment-Workflow eingerichtet und gestartet.
- **2026-04-23** DNS-Umzugsanleitung (`DNS-UMZUG.md`) erstellt – wartet auf Domain-Registrar-Infos.
- **2026-11-02** Skill „seobility-optimizer" (github.com/echo3x3e/seobility-optimizer) geprüft: Prüfskript ist harmlos (liest nur), bildet aber Seobility nur grob nach; Live-Modus nutzt eine inoffizielle Seobility-Schnittstelle mit vorgetäuschtem Browser → nicht verwenden. Lokaler Test: Startseite ~71 %, Time-Machine-Artikel ~78 %. Echte Funde: `og-default.png` fehlt (404 → kaputte Vorschau beim Teilen), kein JSON-LD (strukturierte Daten), Titel zu lang (Startseite 86 Zeichen, Artikel durch Zusatz „· wasgelingtmir.com"), manche Beschreibungen zu lang/kurz. Umsetzung wartet auf Christians Auswahl.
- **2026-11-02** SEO umgesetzt (Branch `claude/seobility-website-optimization-846cb4`): `public/og-default.png` (fehlte, war 404) + Generator `scripts/make-og-image.mjs`; JSON-LD `WebSite` + `BlogPosting`; Titel hängen „· wasgelingtmir.com“ nur an, wenn ≤ 60 Zeichen; Startseiten-Titel auf 58 Zeichen gekürzt. Build ok, JSON-LD gültig. Noch nicht live/gemergt.
- **2026-11-02** Neues freiwilliges Feld `seoTitle` (Artikel + Seiten) für Google/Browser-Tab; 13 Seiten mit Kurztiteln (50–60 Zeichen) versehen, Überschriften im Artikel unverändert. Build ok, jetzt keine Seite mehr über 60 Zeichen. Noch nicht gemergt.
- **2026-11-02** Lighthouse (Handy) Startseite live: SEO 100, Best Practices 100, Barrierefreiheit 95 – Kontrast weiße Schrift auf `brand-600` zu schwach (3,8 statt 4,5). Behoben: Button Startseite + 404-Seite und Tastatur-Sprunglink auf `brand-700` (Kontrast 5,5), Hover `brand-800`. Lokal nachgeprüft: Barrierefreiheit 100. PageSpeed-Geschwindigkeit noch nicht gemessen (Google-Schnittstelle war über Tageslimit).
