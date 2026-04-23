# Plan: Neuaufbau wasgelingtmir.com

**Erstellt:** 2026-04-23
**Status:** In Planung – wartet auf WordPress-Export

---

## Ziel (einfach erklärt)
Die bestehende WordPress.com-Seite **wasgelingtmir.com** wird komplett neu aufgebaut als moderne, schnelle statische Website. Die neue Seite läuft auf **GitHub Pages** (kostenlos), ist **mobil optimiert**, hat **komprimierte Bilder** (schnellere Ladezeiten) und alle Artikel werden vorher auf Fehler geprüft und korrigiert.

## Aktuelle Situation
- **Plattform jetzt:** WordPress.com (gehostet)
- **Inhalt:** Blog "Zuano's Antworten finden" mit ~25–30 Artikeln seit 2015
- **Kategorien:** Computer & Technik, Ernährung, Gesundheit, Impressum
- **Domain:** wasgelingtmir.com (bleibt bestehen)
- **GitHub-Account:** Zuano (bereits verbunden, alle Rechte vorhanden)

## Gewählte Technologie
- **Framework:** Astro (modern, schnell, einfache Markdown-Artikel)
- **Hosting:** GitHub Pages (kostenlos, direkt aus Repository)
- **Bilder:** Automatische Konvertierung zu WebP mit responsive Varianten
- **Design:** Modernes, eigenständiges Design mit Fokus auf Lesbarkeit und Mobile

---

## Geplante Schritte

### Phase 1 – Export & Analyse (Du + ich)
1. **Du:** WordPress-Export (XML + Medien-TAR) nach `export-wordpress/`
2. **Ich:** XML einlesen, Artikelstruktur analysieren, Liste aller Artikel mit Metadaten erstellen
3. **Ich:** Alle Bilder aus dem Export + aus HTML extrahieren und sammeln
4. **Ich:** Fehlende Bilder (externe Links) zusätzlich über Crawl von wasgelingtmir.com holen

### Phase 2 – Inhalte aufbereiten
5. **Ich:** Jeden Artikel zu Markdown konvertieren (sauberes Format)
6. **Ich:** Rechtschreibung + Grammatik prüfen und korrigieren (automatisch)
7. **Ich:** Tote Links finden und reparieren (oder mit Hinweis versehen)
8. **Ich:** Veraltete Screenshots / Infos markieren (z.B. alte iOS-Versionen)
9. **Ich:** Alle Änderungen in einem Änderungs-Log dokumentieren (damit du nachlesen kannst, was geändert wurde)

### Phase 3 – Bilder optimieren
10. **Ich:** Alle Bilder zu WebP konvertieren (ca. 50–80 % kleiner)
11. **Ich:** Responsive Varianten erstellen (klein für Handy, groß für Desktop)
12. **Ich:** Lazy Loading einbauen (Bilder laden erst, wenn man sie sieht)
13. **Ich:** Alt-Texte ergänzen (Barrierefreiheit + SEO)

### Phase 4 – Website aufbauen
14. **Ich:** Astro-Projekt anlegen mit sauberer Ordnerstruktur
15. **Ich:** Modernes Design erstellen:
    - Klare Typografie (große, gut lesbare Schrift)
    - Dark Mode Option
    - Mobile-First Layout
    - Übersichtliche Navigation (Kategorien, Suche, Archiv)
    - Schnelle Ladezeiten (Performance-Score 95+)
16. **Ich:** Kategorien-Seiten (Technik, Ernährung, Gesundheit)
17. **Ich:** Such-Funktion integrieren
18. **Ich:** Impressum + Datenschutz übernehmen
19. **Ich:** RSS-Feed für Abonnenten
20. **Ich:** SEO-Optimierung (Meta-Tags, Sitemap, strukturierte Daten)

### Phase 5 – GitHub & Deployment
21. **Ich:** Git-Repository lokal initialisieren, sinnvolle Commits machen
22. **Ich:** GitHub-Repository `wasgelingtmir-com` anlegen (unter Account Zuano)
23. **Ich:** GitHub Actions für automatisches Deployment einrichten
24. **Ich:** Seite auf `zuano.github.io/wasgelingtmir-com` testen lassen

### Phase 6 – Domain umziehen (Du + ich)
25. **Du:** Prüfen, wo die Domain **wasgelingtmir.com** registriert ist (Domain-Registrar, nicht WordPress)
26. **Ich:** DNS-Einstellungen Schritt für Schritt erklären (4 A-Records auf GitHub + CNAME)
27. **Du:** DNS umstellen beim Domain-Anbieter
28. **Ich:** HTTPS-Zertifikat auf GitHub Pages aktivieren
29. **Beide:** Testen, dass alles funktioniert
30. **Du:** Ggf. WordPress.com-Abo kündigen

---

## Betroffene Dateien / Ordner (neu erstellt)
- `export-wordpress/` – die Original-Dateien aus WordPress (Archiv)
- `src/` – Quellcode der neuen Seite (Astro)
- `src/content/blog/` – alle Artikel als Markdown
- `src/assets/images/` – alle optimierten Bilder
- `src/components/` – Bausteine der Website (Header, Footer, Artikel-Layout)
- `src/pages/` – Seiten (Startseite, Kategorien, Impressum)
- `public/` – statische Dateien (Favicon, robots.txt)
- `.github/workflows/deploy.yml` – automatisches Deployment
- `.claude/TODO.md` – laufende Aufgaben
- `.claude/DECISIONS.md` – technische Entscheidungen
- `.claude/CHANGELOG-articles.md` – was an welchen Artikeln geändert wurde

## Risiken / Seiteneffekte
- **DNS-Umzug:** Während der Umstellung kann die Seite kurz (bis zu 24h) nicht erreichbar sein. Darum erst testen, dann umstellen.
- **Inhaltliche Korrekturen:** Bei älteren Artikeln (z.B. iOS-Anleitungen von 2015) könnten Infos nicht mehr stimmen. Ich markiere das, statt zu löschen.
- **Kommentare gehen verloren:** WordPress-Kommentare werden im Export exportiert, aber auf einer statischen Seite gibt es kein eingebautes Kommentarsystem. Option: externes System (z.B. giscus über GitHub Discussions) – das besprechen wir später.
- **Abonnenten / Email-Liste:** Falls du Email-Abonnenten hast, müssen die manuell informiert werden.

## Offene Fragen (werde ich zu gegebener Zeit fragen)
- Sollen die Kommentare übernommen werden oder weggelassen?
- Brauchst du eine Newsletter-Funktion oder reicht RSS?
- Gibt es Analytics (z.B. Statistiken, wer die Seite besucht)? WordPress hat das eingebaut – auf der neuen Seite bräuchte es z.B. Plausible oder Umami (datenschutzfreundlich).
- Soll es weiterhin eine Suchfunktion geben?
- Farbwelt / Stil-Vorlieben für das neue Design?

---

## Nächster Schritt
⏳ **Warte auf WordPress-Export im Ordner `export-wordpress/`.**
