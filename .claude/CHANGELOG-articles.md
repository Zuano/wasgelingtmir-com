# Änderungen an Artikeln – Protokoll

Alle inhaltlichen Korrekturen (Rechtschreibung, Grammatik, Formatierung) werden hier
pro Artikel einzeln dokumentiert, damit du jede Änderung nachvollziehen und ggf.
rückgängig machen kannst.

**Grundsatz:** Es werden nur eindeutige Fehler korrigiert. Stil, Formulierung und
persönliche Schreibweise bleiben erhalten.

**Automatisierte Schritte (für alle Artikel ausgeführt):**
- HTML → Markdown konvertiert (WordPress-Shortcodes `[caption]` etc. entfernt)
- YAML-Frontmatter mit sauberen Metadaten ergänzt
- Non-Breaking Spaces (U+00A0) und andere Unicode-Artefakte entfernt
- Doppelte Leerzeichen zusammengefasst
- Trailing Whitespace entfernt

**Kategorien neu zugeordnet** (nicht mehr alles unter "Allgemein"):
- Apple & Mac (12)
- Web & Dienste (5)
- Gesundheit (2)
- Ernährung (2)
- Leben & Gedanken (3)

---

## Automatische Link-Korrekturen (Weiterleitungen + tote Links)

### diese-verfluchten-whatsapp-haeckchen.md
- Link `http://wasgelingtmir.com/2019/07/10/hammer-und-nagel-geschichte-von-paul-watzlawick/` → `https://wasgelingtmir.com/2019/07/10/hammer-und-nagel-geschichte-von-paul-watzlawick/`

### mitteilung-auf-dem-iphone-ueber-batterie-lebensdauer.md
- Link `https://support.apple.com/de-de/HT210512` → `https://support.apple.com/de-de/108055`

### birkenbihl-sprachen-adobe-air-loesung.md
- Link `https://blog.adobe.com/.../the-future-of-adobe-air.html` → `.../the-future-of-adobe-air` (neuer Apple-Blog)
- Link `https://airsdk.harman.com/runtime` → `https://airsdk.harman.com` (404 behoben)
- Zwei tote Helpx-Adobe-Links → zusammengefasst zu `https://helpx.adobe.com/at/air.html`

### so-loschen-sie-alle-erledigten-erinnerungen-auf-einmal-auf-iphone-und-ipad.md
- Interner Link aktualisiert (Slug-Änderung)

### wie-lange-erhalt-mein-gebrauchtes-iphone-ipad-oder-mac-noch-softwareupdates.md
- 3 Apple-Support-Links auf neue URL-Struktur aktualisiert (HT-IDs → neue IDs)

### apple-beats-airpods-probleme-erste-hilfe.md
- Apple-Support-Link auf aktuelle Beats-Reset-Anleitung aktualisiert

### fisch-enthaelt-kein-omega-3-dafuer-enthaelt-weidefleisch-welches.md
- Dropbox-Audio-Link auf neue URL aktualisiert (2×)

### die-magie-des-90-minuten-schlafzyklus-wie-ich-durch-bewusste-schlafrhythmen-mein-leben-verandert-habe.md
- Sleep-Cycle-Link aktualisiert (trailing slash + ohne www)

### mein-weg-zu-bewusster-ernaehrung-empfehlung.md
- Urgeschmack-Link auf HTTPS + www aktualisiert

### paypal-passkey.md
- 3 externe Links aktualisiert (Reddit + PayPal auf finale URLs)

---

## Manuelle Korrekturen (Rechtschreibung, Grammatik, Formatierung)

### quitter-die-einfache-losung-gegen-nervige-inaktivitats-popups.md
- "Downlaod Link" → "Download-Link"

### spart-euch-bei-der-telefonnummer-diese-null-in-klammer.md
- "Zunao" → "Zuano" (Name-Tippfehler)

### macos-anrufe-nicht-automatisch-uber-skype.md
- "Facetime" und "FacTime" → "FaceTime" (einheitlich)

### macos-schliesse-dauernd-die-falschen-fenster.md
- "So schwierig ist es mir es umzugewöhnen" → "So schwierig ist es, sich umzugewöhnen"
- "Alles Leuchtet" → "Alles leuchtet" (Verb klein)
- "das dunkle" → "das Dunkle" (Substantivierung)
- "Aktive" → "aktive"
- fehlendes Verb am Ende ergänzt

### wie-fuehlt-es-sich-an-zu-hoeren.md
- fehlender Anführungszeichenabschluss korrigiert
- "teilst ihn an Deinen Freund" → "teilst ihn mit Deinem Freund" (Fallsetzung)
- "Weil woher soll der Andere ... erzählt" → "Denn woher soll ... erzählt?" (Frage + Komma)

### apple-beats-airpods-probleme-erste-hilfe.md
- "kam von Ihr die plötzlich Lösung" → "kam von ihr plötzlich die Lösung"
- "Apple Telefonsupport Mitarbeiterin" → "Apple-Telefonsupport-Mitarbeiterin" (Bindestriche)
- "auch der Beste" → "auch der beste" (Adjektiv klein)
- "Kopfhörer Anpassungen" → "Kopfhörer-Anpassungen"
- "immer wieder Mal" → "immer wieder mal"
- "Beatskopfhörer" → "Beats-Kopfhörer"
- fehlender Satzpunkt am Ende

### willhaben-betrug-mit-amazon-gutscheinen.md
- "zur Zeit" → "zurzeit"
- "Amazon Gutscheine" → "Amazon-Gutscheine"
- fehlende Kommas nach Relativsätzen ergänzt
- "Paypal" → "PayPal" (Markenname)
- "Gewerbsmäßigem" → "gewerbsmäßigem" (Adjektiv klein)
- "Bagatellebeträgen" → "Bagatellbeträgen"
- "Am Besten" → "Am besten"

### mein-weg-zu-bewusster-ernaehrung-empfehlung.md
- Überflüssiges `**Felix**` entfernt
- Nackte URLs als Markdown-Links formatiert
- Alt-Text des Hero-Bildes ergänzt
- Doppelte Link-Verlinkung des Bildes entfernt

### mantram-hilfe-durch-die-kraft-des-wortes-von-eknath-easwaran.md
- "Hier eine Testseite um sich ... zu überzeugen" → Komma ergänzt
- doppelter PDF-Link zusammengefasst
- "€15,-" Preisformat vereinheitlicht auf "15 €"
- Formular-Referenz entfernt (gibt es in statischer Site nicht)

### wie-man-den-personlichen-hotspot-auf-dem-iphone-...md
- Anführungszeichen um "iPhone" und "iPhone von Christian" korrigiert

### einfacher-weg-um-payback-punkte-bei-amazon-einkaufen-...md
- KI-Kommentar am Ende entfernt ("Ich hoffe, dieser ergänzte Blogartikel ist hilfreich ...")
- "Video Anleitung" → "Video-Anleitung"
- nackte YouTube-URL als Markdown-Link formatiert
- "Beispiel Icon" → "Beispiel-Icon"

### wie-lange-erhalt-mein-gebrauchtes-iphone-ipad-oder-mac-noch-softwareupdates.md
- "Apple Gerät" → "Apple-Gerät"
- fehlende Kommas ergänzt
- "5 Jahre Jahre lang" → "5 Jahre lang" (Dopplung entfernt)
- "Betriebsystem" → "Betriebssystem" (überall korrigiert)
- "eine neues" → "ein neues"
- "Macbook" → "MacBook" (Markenschreibweise)
- "wenn man sich ... genügt" → "wenn man sich ... begnügt"
- Fazit-Abschnitt als Liste strukturiert für bessere Lesbarkeit
- "alle zwei drei Jahre" → "alle zwei bis drei Jahre"

### ios15-macos12-erledigte-erinnerungen-loeschen.md
- "in macOS Monterey" → "In macOS Monterey" (Satzanfang)
- "Löschen Button" → "Löschen-Button"
- "Um den Löschen-Button hervorzurufen braucht" → "muss ... zu scrollen"
- Kommas nach Nebensätzen ergänzt
- fehlender Satzpunkt ergänzt

### so-loschen-sie-alle-erledigten-erinnerungen-auf-einmal-auf-iphone-und-ipad.md
- Kurzbefehl-Link-Text vereinheitlicht (Gedankenstrich)
- "Tippen Sie auf 'Filter hinzufügen'" – fehlender Punkt
- Komma-Korrektur im Satz "Je nach Anzahl ..."
- fehlender Satzpunkt ergänzt

### fisch-enthaelt-kein-omega-3-dafuer-enthaelt-weidefleisch-welches.md
- "nachgewiesener maßen" → "nachgewiesenermaßen"
- "Omega 3 Fettsäuren" → "Omega-3-Fettsäuren" (durchgängig)
- "Das hoch propagierte" → "Das hochpropagierte"
- "Wo bekommt man den nun" → "Wo bekommt man denn nun"
- "zurück halten" → "zurückhalten"
- "Soja enthält viel Protein, dass das" → "Soja enthält viel Protein, das das"
- "Omega 6 haben wir so und so" → "Omega 6 haben wir sowieso"
- "Tiere die auf der Weide" → "Tiere, die auf der Weide"
- "dazu gehören Schweine genauso dazu" → "dazu gehören Schweine genauso" (Dopplung entfernt)
- "von alles Möglichen, dass sich rundum Gräser handelt" → "von allem Möglichen, was rund um die Gräser wächst"
- "freilaufendem" → "freilaufenden" (Kasus-Fehler)
- "Das ein Bio-Freiland Huhn, dass sich" → "Dass ein Bio-Freilandhuhn, das sich" (das/dass)
- "Seeen" → "Seen"
- "Endgeld" → "Entgelt"
- "Affiliate Link" → "Affiliate-Link"
- "Tiere die viele Gräser" → "Tiere, die viele Gräser"

### diese-verfluchten-whatsapp-haeckchen.md
- "das ich nur noch" → "dass ich nur noch"
- Satzteilungsfehler bei "online ist und es liest. Dann gebe ich" → Komma verwendet
- "zurück schreiben" → "zurückschreiben"
- "online Status" → "Online-Status"
- "Eurer" → "Euer" (Nominativ-Kasus)

### tanita-waage-in-apple-health-importieren.md
- Viele Bindestrich-Korrekturen: "SD Karte" → "SD-Karte", "USB Port" → "USB-Port", etc.
- "Schritt für Schritt Anleitung" → "Schritt-für-Schritt-Anleitung"
- "Klickte" → "Klickt"
- "rein kommt markiert wollen" → "reinkommt, wollen"
- "alle Möglichen" → "alle möglichen"
- fehlende Klammer ergänzt
- "Get Startet" → "Get Started"
- "skipen" → "überspringen", "währe" → "wäre"
- "von keinen Software Anbieter" → "von keinem Software-Anbieter"

### welchen-anteil-geld-erhalten-kuenstler-durch-apple-music.md
- "Ich möchte, das" → "Ich möchte, dass"
- Signatur-Platzhalter `*******` durch "Zuano" ersetzt
- P.S. in Kursivformatierung
- Update-Absatz neu strukturiert, nackte URL als Markdown-Link

### birkenbihl-sprachen-adobe-air-loesung.md
- "Um Die Birkenbihl" → "Um die Birkenbihl" (Großschreibung nach Kolon)
- Doppelten Helpx-Link zusammengefasst

### facetime-anrufe-auf-dem-mac-transkribieren-trotz-offizieller-einschrankungen.md
- KI-Kommentar entfernt ("Gerne. Hier ist ein zusätzlicher, sachlicher und rechtlich nüchterner Absatz ...")

### miele-dampfgarer-guenstig-entkalken.md (Seite)
- "Entkalkungstabletten um circa an" → "Entkalkungstabletten an" (sinnvoller Satzbau)
- "€13,41" → "13,41 €" (österreichisches Währungsformat)
- "Inhaltstoffe" → "Inhaltsstoffe"
- "€1,59 Euro" → "1,59 €" (doppeltes Währungssymbol entfernt)
- "sein Gutes getan hat" → "ihr Gutes getan hat" (feminines Subjekt)

### ueber-mich.md (Seite)
- WordPress-Default-Text **komplett ersetzt** durch eine echte Über-Seite mit Kategorien-Übersicht
- **TODO:** Persönlicher Text über Zuano wird noch ergänzt (vom User)

### paypal-passkey.md (Seite)
- Leerzeichen vor Punkt entfernt ("Passkey ." → "Passkey.")
- Dreifach-h4-Struktur zusammengefasst (lesbarer)
