# wasgelingtmir.com – Neuaufbau

Neuaufbau des Blogs **"Zuano's Antworten finden"** (ehemals WordPress.com) als moderne statische Website mit Astro, gehostet auf GitHub Pages.

- **Live-Domain:** https://wasgelingtmir.com (später, nach DNS-Umzug)
- **GitHub-Account:** Zuano
- **Technologie:** Astro + GitHub Pages + GitHub Actions

## Projektstruktur

```
wasgelingtmir.com/
├── README.md                           Projekt-Einstieg (diese Datei)
├── .claude/                            Projekt-Doku und interne Arbeitsdateien
│   ├── DOCUMENTATION.md                → Zentrale Doku und Inhaltsverzeichnis
│   ├── plan.md                         Gesamtplan aller Phasen
│   ├── TODO.md                         Aktuelle Aufgaben und Änderungsprotokoll
│   ├── DECISIONS.md                    Getroffene technische Entscheidungen
│   ├── CHANGELOG-articles.md           Pro-Artikel-Änderungsprotokoll
│   ├── articles-inventory.md / .json   Inventar aller Artikel/Seiten
│   ├── images-manifest.json            Alle Bildreferenzen aus dem Export
│   ├── images-processed.json           Ergebnisse der Bildverarbeitung
│   ├── images-report.md                Zusammenfassung Bildkomprimierung
│   ├── link-check-report.md            Gefundene tote Links & Weiterleitungen
│   └── link-check-results.json         Rohergebnisse Linkprüfung
├── export-wordpress/                   Original-Export aus WordPress.com
│   ├── zuano039s…WordPress.*.xml       Alle Texte, Kategorien, Tags, Kommentare
│   └── media-export-*.tar              Alle Mediendateien (Bilder, PDFs)
├── scripts/                            Python-Werkzeuge für die Migration
│   ├── parse-wordpress-export.py       XML einlesen, Inventar erzeugen
│   ├── convert-to-markdown.py          HTML → Markdown mit Frontmatter
│   ├── new-categories.json             Neue Kategorie-Zuordnung pro Artikel
│   ├── prepare-images.py               Bilder kopieren, WebP, responsive
│   ├── check-links.py                  Linkprüfung aller externen URLs
│   └── apply-link-fixes.py             Weiterleitungen/tote Links automatisch fixen
├── content-prepared/                   Aufbereiteter Content vor Astro-Import
│   ├── blog/                           Alle 24 Artikel als Markdown
│   └── pages/                          Aufbereitete Seiten (Impressum etc.)
├── public/                             Statische Assets für Astro
│   └── images/blog/<slug>/             Optimierte Bilder je Artikel
├── src/                                Astro-Quellcode (wird angelegt)
└── .venv/                              Python virtuelles Environment (für Scripts)
```

## Aktueller Stand (Stand: 2026-04-23)

### Abgeschlossen
- [x] WordPress-Export importiert (XML + Medien)
- [x] Inventar erstellt (25 Artikel, 8 Seiten, 148 Medien)
- [x] 24 Artikel zu sauberem Markdown konvertiert ("Hallo Welt!" übersprungen)
- [x] 4 Seiten übernommen (leere Seiten verworfen)
- [x] Kategorien neu strukturiert: Apple & Mac, Web & Dienste, Gesundheit, Ernährung, Leben & Gedanken
- [x] 95 Bilder zu WebP + responsive Varianten konvertiert (**17,10 MB → 5,12 MB, -70 %**)
- [x] Linkprüfung durchgeführt: 14 Weiterleitungen angewendet, 4 tote Links gefixt

### In Arbeit
- [ ] Manuelles Lektorat (Rechtschreibung, Grammatik, Formatierung) pro Artikel
- [ ] Veraltete Infos markieren

### Offen
- [ ] Astro-Projekt aufsetzen
- [ ] Modernes Design (Mobile-First, Dark Mode)
- [ ] Kategorien-, Archiv- und Suchseiten
- [ ] SEO-Optimierung und RSS-Feed
- [ ] GitHub-Repository und Deployment
- [ ] DNS-Umstellung auf GitHub Pages
- [ ] HTTPS-Zertifikat

## Lokal arbeiten

Alle Python-Scripts laufen in einem virtuellen Environment (nicht im System-Python):

```bash
# Einmalig:
python3 -m venv .venv
source .venv/bin/activate
pip install markdownify beautifulsoup4 Pillow requests pyspellchecker lxml

# Für jeden Durchlauf:
source .venv/bin/activate
python3 scripts/<script-name>.py
```

## Kontakt

**Autor:** Zuano
**Original-URL:** https://wasgelingtmir.com
