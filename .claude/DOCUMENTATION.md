# Dokumentation – wasgelingtmir.com Neuaufbau

Diese Datei ist der **zentrale Einstiegspunkt** in die Projekt-Dokumentation. Sie verlinkt alle anderen `.md`-Dateien und erklärt, wofür sie da sind.

Die Doku wächst mit dem Projekt. Wenn etwas neu hinzukommt, wird hier verlinkt.

---

## Übersicht – welche Dokumente gibt es?

### Planung & Stand

| Datei | Zweck |
|---|---|
| [`plan.md`](./plan.md) | Gesamtplan aller 6 Phasen (Export → Konvertierung → Bilder → Astro → Deployment → DNS) |
| [`TODO.md`](./TODO.md) | Aktuelle Aufgabenliste + Änderungsprotokoll |
| [`DECISIONS.md`](./DECISIONS.md) | Alle getroffenen technischen Entscheidungen mit Begründung |

### Analyse der bestehenden Website

| Datei | Zweck |
|---|---|
| [`articles-inventory.md`](./articles-inventory.md) | Lesbare Übersicht aller Artikel & Seiten mit Metadaten |
| [`articles-inventory.json`](./articles-inventory.json) | Inventar als JSON (Datenbasis für die Scripts) |
| [`images-manifest.json`](./images-manifest.json) | Alle im Export gefundenen Bildreferenzen |

### Ergebnisse der Migration

| Datei | Zweck |
|---|---|
| [`images-report.md`](./images-report.md) | Zusammenfassung Bildkomprimierung (wie viel gespart) |
| [`images-processed.json`](./images-processed.json) | Pro Bild: Originalgröße, WebP-Größe, Varianten |
| [`link-check-report.md`](./link-check-report.md) | Gefundene tote Links + Weiterleitungen |
| [`link-check-results.json`](./link-check-results.json) | Rohdaten aus der Link-Prüfung |
| [`CHANGELOG-articles.md`](./CHANGELOG-articles.md) | Jede einzelne Änderung an Artikeln (Link-Fixes, Rechtschreibung, Grammatik) |

### Deployment & Domain

| Datei | Zweck |
|---|---|
| [`DNS-UMZUG.md`](./DNS-UMZUG.md) | Schritt-für-Schritt-Anleitung zur DNS-Umstellung auf GitHub Pages |

### Design & Produktvision *(wird später erstellt)*

| Datei | Zweck |
|---|---|
| `DESIGN.md` | Designkonzept für die neue Website (Farben, Typografie, Layout) |
| `features/` | Einzelne Feature-Beschreibungen, sobald wir in der Bauphase sind |

---

## Wie arbeite ich mit dieser Doku?

- **Wenn du eine Entscheidung brauchst:** schau in `DECISIONS.md` – dort steht, warum wir was so gemacht haben.
- **Wenn du wissen willst, was als nächstes ansteht:** schau in `TODO.md` oder `plan.md`.
- **Wenn du nachvollziehen willst, was an Artikeln geändert wurde:** schau in `CHANGELOG-articles.md`.
- **Wenn du wissen willst, wie viele Bilder wir haben und wie groß:** schau in `images-report.md`.
- **Wenn du wissen willst, welche Links geändert wurden:** schau in `link-check-report.md`.

---

## Projektphasen (aktuelle Einordnung)

| Phase | Status | Details in |
|---|---|---|
| **1. Export & Analyse** | ✅ Abgeschlossen | `articles-inventory.md` |
| **2. Inhalte aufbereiten** | 🔄 In Arbeit (Markdown fertig, Lektorat läuft) | `CHANGELOG-articles.md` |
| **3. Bilder optimieren** | ✅ Abgeschlossen | `images-report.md` |
| **4. Website aufbauen** | ⏳ Offen | – |
| **5. GitHub & Deployment** | ⏳ Offen | – |
| **6. Domain-Umzug** | ⏳ Offen | – |

---

## Grundsätze für diese Doku

1. **Jede Änderung am Inhalt wird dokumentiert.** Wir ändern nichts, ohne es im `CHANGELOG-articles.md` festzuhalten.
2. **Jede technische Entscheidung landet in `DECISIONS.md`** – kurz, mit Datum, mit Begründung.
3. **Alles in Deutsch.** Code, Scripts, Commits zweisprachig (Englisch + Deutsch), Doku rein Deutsch.
4. **Keine versteckten Abkürzungen.** Wer später hier reinschaut (auch der User in 6 Monaten), soll ohne Vorwissen alles verstehen.

---

**Letzte Aktualisierung:** 2026-04-23
