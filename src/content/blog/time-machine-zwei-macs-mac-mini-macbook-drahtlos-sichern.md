---
title: "Time Machine für zwei Macs: MacBook drahtlos über den Mac mini sichern"
description: "Wie ich ein MacBook drahtlos über meinen Mac mini per Time Machine gesichert habe – inklusive der Stolperfallen mit versiegelten APFS-Volumes und dem zweiten Volume als Lösung."
pubDate: "2026-05-04"
category: "Apple & Mac"
categorySlug: "apple-mac"
slug: "time-machine-zwei-macs-mac-mini-macbook-drahtlos-sichern"
heroImage: "/images/blog/time-machine-zwei-macs-mac-mini-macbook-drahtlos-sichern/hero.webp"
---

Hallo,

ich habe einen Mac mini, der bei mir ohnehin **24/7** läuft, und zusätzlich ein MacBook, das ich gerne **drahtlos** sichern wollte. Klingt nach einem Schulbuch-Setup für Time Machine: externe Platte an den Mini, beide Macs sichern dort hinein. So einfach ist es leider doch nicht – und ich bin in genau die Stolperfallen gelaufen, die diesen Beitrag wert sind.

Wenn du dieselbe Konstellation hast (ein „immer laufender" Mac plus ein zweiter, der drahtlos gesichert werden soll), führt dich diese Anleitung sauber durch das ganze Setup.

---

## **Was ich am Ende erreicht habe**

- **Mac mini** mit fest angeschlossener externer SSD (4 TB)
- **MacBook**, das übers WLAN auf den Mini sichert
- Beide Macs nutzen Time Machine, aber auf **getrennten APFS-Volumes** auf derselben Platte
- Eigener „Sharing-Only"-Benutzer für die Authentifizierung übers Netzwerk

---

## **Die richtige Festplatte wählen**

Time Machine braucht Platz für Versionsverläufe, nicht nur für die aktuelle Datenmenge. Faustregel: **zwei- bis dreimal so viel** wie die belegten Daten beider Macs zusammen.

Bei mir: Mac mini mit 2 TB SSD, MacBook mit 500 GB SSD, gemeinsame Belegung etwa **700 GB**. Eine 4-TB-Platte ist damit komfortabel. Wer absehbar mehr Daten ansammelt (Fotomediathek, Videoschnitt), greift besser zu 5 TB. Backup-Historie ist etwas, das man erst zu schätzen lernt, wenn man sie braucht – und beim Plattenwechsel beginnt Time Machine bei null.

**HDD oder SSD?** Für reine Backup-Zwecke reicht eine HDD. Eine externe Platte für Time Machine wartet die meiste Zeit nur auf den nächsten Snapshot.

**Partitionieren?** Nein. Time Machine kann mehrere Macs problemlos auf eine Platte sichern. Klassische Partitionen sind unflexibel – wir nutzen stattdessen mehrere **APFS-Volumes** im selben Container, die sich den Platz dynamisch teilen.

---

## **Schritt 1: Die Platte am Mac mini einrichten**

Externe Platte anstecken, Festplattendienstprogramm öffnen.

- Platte links auswählen
- Oben auf **„Löschen"** klicken
- Format: **APFS** (verschlüsselt, wenn die Platte das Haus verlassen könnte)
- Schema: **GUID-Partitionstabelle**
- Name vergeben, z. B. `4TB SSD TimeMachine`

Anschließend in **Systemeinstellungen → Allgemein → Time Machine** das Volume als Backup-Ziel hinzufügen. Time Machine konvertiert es automatisch in ein Backup-Volume und beginnt das erste Backup.

<figure>
  <img src="/images/blog/time-machine-zwei-macs-mac-mini-macbook-drahtlos-sichern/01-systemeinstellungen-allgemein.webp" alt="Systemeinstellungen am Mac, Bereich Allgemein" loading="lazy">
  <figcaption>Über Systemeinstellungen → Allgemein erreichst du sowohl Time Machine als auch die Freigaben.</figcaption>
</figure>

Das initiale Backup ist groß – wenn der Mini am Strom hängt und sowieso läuft, lass es einfach über Nacht durchziehen.

---

## **Die erste Stolperfalle: Das versiegelte Time-Machine-Volume**

Hier kommt die Erkenntnis, die mich am meisten Zeit gekostet hat.

Sobald macOS eine APFS-Platte als Time-Machine-Ziel verwendet, **versiegelt** das System das Volume. Du erkennst das, wenn du im Finder „Informationen" auf die Platte aufrufst: Unter „Teilen & Zugriffsrechte" steht **„Du darfst nur lesen"**. Selbst als Admin kannst du dort weder Ordner anlegen noch Rechte ändern.

Das ist Absicht – Apple verhindert, dass Backups versehentlich beschädigt werden. Konsequenz: Du kannst dieses versiegelte Volume **nicht** zusätzlich per SMB freigeben, damit ein zweiter Mac darauf sichert. **Zwei Macs können sich keine direkt-angeschlossene Time-Machine-Platte teilen.**

Die Lösung ist überraschend elegant.

---

## **Schritt 2: Ein zweites APFS-Volume für das MacBook**

APFS erlaubt mehrere Volumes innerhalb desselben Containers, die sich den Platz dynamisch teilen. Das existierende Mini-Backup bleibt unangetastet, wir fügen einfach ein neues Volume daneben hinzu.

Im Festplattendienstprogramm:

- Platte links auswählen
- Oben auf **„+ Volume"** klicken (nicht „Partition"!)
- Name: z. B. `MacBook-Backup`
- Format: **APFS** (oder APFS verschlüsselt)
- Auf **„Größenoptionen"** klicken

Hier gibt es zwei Felder, die man verstehen sollte:

- **Reservegröße:** Was dauerhaft für dieses Volume gesperrt wird, auch wenn es leer ist. Lass es leer oder setze einen kleinen Wert (z. B. 200 GB) als Mindestgarantie.
- **Kontingentgröße:** Die Obergrenze. Bei mir 1 TB für das MacBook.

**Die Reserve niedrig zu halten ist klug**, weil sonst der Mini-Backup-Verlauf unnötig früh gekürzt wird. Mit Quota allein hat das MacBook trotzdem ein hartes Limit, kann aber dynamisch wachsen, solange Platz da ist.

OK → Erstellen. Das neue Volume taucht im Finder als ganz normale, beschreibbare APFS-Platte auf.

---

## **Schritt 3: Sharing-Only-Benutzer am Mac mini anlegen**

Für die Authentifizierung übers Netzwerk legen wir einen eigenen Benutzer an, der **nur** auf das Backup-Volume schreiben darf. Sicherer, als das MacBook mit dem normalen Account einzuloggen.

**Systemeinstellungen → Benutzer & Gruppen → Hinzufügen.**

Im Dropdown ganz oben **„Nur Freigabe"** wählen. Das ist entscheidend – ein Sharing-Only-Account kann sich nicht am Mini einloggen, sieht keinen Schreibtisch und existiert nur als Netzwerkidentität.

- Vollständiger Name: „MacBook Backup" oder ähnlich
- Account-Name: `timemachine` (nur Kleinbuchstaben, keine Sonderzeichen)
- Passwort: ein eigenes, das du im Passwortmanager speicherst

---

## **Schritt 4: Berechtigungen auf dem neuen Volume setzen**

Damit der `timemachine`-User auf das Volume schreiben darf, müssen wir ihm explizit Rechte geben.

Im Finder das Volume `MacBook-Backup` auswählen → **Cmd + I**.

Unten unter „Teilen & Zugriffsrechte":

- Schloss aufklicken, Admin-Passwort
- Mit **„+"** den User `timemachine` hinzufügen
- Rechts auf **„Lesen & Schreiben"** stellen
- Zahnrad → „Auf alle enthaltenen Objekte anwenden"

Wichtig: Die Checkbox **„Eigentumsrechte auf diesem Volume ignorieren"** muss **AUS** sein. Mit aktivierter Option funktioniert die Rechteverwaltung nicht korrekt.

---

## **Schritt 5: SMB-Freigabe und Time-Machine-Flag**

Jetzt geben wir das neue Volume übers Netzwerk frei und markieren es als Time-Machine-Ziel.

Den Eintrag „Teilen" findest du am schnellsten über die Suche oben in den Systemeinstellungen.

<figure>
  <img src="/images/blog/time-machine-zwei-macs-mac-mini-macbook-drahtlos-sichern/02-teilen-suchen.webp" alt="Suche nach 'Freigabe' in den Systemeinstellungen" loading="lazy">
  <figcaption>Suche oben links nach „Freigabe", dann erscheinen alle Freigabe-Einstellungen direkt.</figcaption>
</figure>

In der Übersicht **Dateifreigabe einschalten**. Internetfreigabe braucht es für Time Machine nicht – falls dort versehentlich aktiviert, kannst du sie ausschalten.

<figure>
  <img src="/images/blog/time-machine-zwei-macs-mac-mini-macbook-drahtlos-sichern/03-teilen-uebersicht.webp" alt="Teilen-Übersicht mit aktivierter Dateifreigabe" loading="lazy">
  <figcaption>Dateifreigabe ist aktiv. Den lokalen Hostname unten brauchst du später, wenn das MacBook den Mini findet.</figcaption>
</figure>

Auf das **Info-Symbol („i")** neben „Dateifreigabe" klicken. Dort siehst du alle geteilten Ordner und kannst neue hinzufügen. Mit **„+"** das Volume `MacBook-Backup` auswählen.

Anschließend in der Benutzer-Spalte rechts:

- `timemachine` hinzufügen → **Lesen & Schreiben**
- „Jeder" → **Kein Zugriff**

<figure>
  <img src="/images/blog/time-machine-zwei-macs-mac-mini-macbook-drahtlos-sichern/04-dateifreigabe-volume-hinzu.webp" alt="MacBook-Backup als geteilten Ordner hinzufügen" loading="lazy">
  <figcaption>Volume „MacBook-Backup" hinzugefügt, der User „timemachine" hat Lese- und Schreibrechte.</figcaption>
</figure>

Dann auf den Eintrag **rechtsklicken** → „Erweiterte Optionen".

<figure>
  <img src="/images/blog/time-machine-zwei-macs-mac-mini-macbook-drahtlos-sichern/05-erweiterte-optionen-menu.webp" alt="Kontextmenü mit Erweiterte Optionen" loading="lazy">
  <figcaption>Hier nicht nur Berechtigungen ändern, sondern unbedingt die „Erweiterten Optionen" öffnen – sonst fehlt der Time-Machine-Schalter.</figcaption>
</figure>

Im Dialog die Schalter setzen:

- **Gastbenutzer:innen zulassen: AUS** (sehr wichtig, sonst kann jeder im Netz ohne Passwort drauf)
- **Nur SMB-verschlüsselte Verbindungen erlauben: AN**
- **Als Ziel eines Time Machine-Backups teilen: AN**
- **Backups begrenzen auf:** z. B. 900 GB (etwas weniger als das 1-TB-Volume, gibt Puffer)

<figure>
  <img src="/images/blog/time-machine-zwei-macs-mac-mini-macbook-drahtlos-sichern/06-erweiterte-optionen-tm.webp" alt="Erweiterte Optionen mit Time-Machine-Schalter und 900 GB Limit" loading="lazy">
  <figcaption>Der entscheidende Schalter: „Als Ziel eines Time Machine-Backups teilen". Die Größenbegrenzung verhindert, dass das MacBook das ganze Volume ausreizt.</figcaption>
</figure>

OK → Fertig.

---

## **Schritt 6: Energieeinstellungen am Mac mini**

Damit das MacBook nachts auch sichern kann, muss der Mini erreichbar sein.

**Systemeinstellungen → Energie → „Wake for network access"** (auf Deutsch je nach macOS-Version „Aufwachen bei Netzwerkzugriff" oder „Power Nap bei Netzbetrieb") aktivieren. Sonst schläft der Mini, das MacBook findet kein Ziel und Backups schlagen fehl.

---

## **Schritt 7: Am MacBook das Backup-Ziel hinzufügen**

Jetzt der eigentliche Moment der Wahrheit.

Am MacBook: **Systemeinstellungen → Allgemein → Time Machine → „+"**.

In der Liste sollte das Volume `MacBook-Backup` auf dem Mini erscheinen.

<figure>
  <img src="/images/blog/time-machine-zwei-macs-mac-mini-macbook-drahtlos-sichern/07-macbook-time-machine-volume.webp" alt="Volume-Auswahl am MacBook mit MacBook-Backup auf dem Mini" loading="lazy">
  <figcaption>Das freigegebene Volume vom Mini taucht in der Liste auf. Auswählen und „Volume konfigurieren" klicken.</figcaption>
</figure>

Im nächsten Dialog fragt macOS nach den Anmeldedaten. Hier nicht deinen normalen Benutzer eintragen, sondern den **`timemachine`-Sharing-User**, den du in Schritt 3 angelegt hast.

<figure>
  <img src="/images/blog/time-machine-zwei-macs-mac-mini-macbook-drahtlos-sichern/08-login-name-erklaerung.webp" alt="Login-Dialog mit Erklärung welcher Benutzername gemeint ist" loading="lazy">
  <figcaption>Wichtig: hier kommt der Account-Name vom Mac-mini-User („timemachine"), nicht dein Apple-Account.</figcaption>
</figure>

<figure>
  <img src="/images/blog/time-machine-zwei-macs-mac-mini-macbook-drahtlos-sichern/09-login-timemachine.webp" alt="Login mit timemachine als Benutzername" loading="lazy">
  <figcaption>So sieht's aus, wenn der Sharing-Only-User korrekt eingetragen ist. Passwort kommt aus dem Passwortmanager.</figcaption>
</figure>

Danach kommt der **Konfigurations-Dialog** mit drei wichtigen Schaltern:

- **Backup verschlüsseln: AN** (Pflicht – das Backup liegt sonst unverschlüsselt im Netz)
- Ein eigenes Verschlüsselungspasswort vergeben → **unbedingt** im Passwortmanager speichern, ohne das kommst du nie wieder ans Backup ran
- Festplattennutzungslimit: **Eigenes** auswählen, wenn du dem MacBook eine harte Grenze setzen willst

<figure>
  <img src="/images/blog/time-machine-zwei-macs-mac-mini-macbook-drahtlos-sichern/10-backup-konfigurieren-ohne-limit.webp" alt="Backup-Konfiguration mit Verschlüsselung an, Limit auf 'Ohne'" loading="lazy">
  <figcaption>Verschlüsselung einschalten ist nicht optional, wenn das Backup übers Netzwerk geht.</figcaption>
</figure>

<figure>
  <img src="/images/blog/time-machine-zwei-macs-mac-mini-macbook-drahtlos-sichern/11-backup-konfigurieren-mit-limit.webp" alt="Backup-Konfiguration mit eigenem Limit von ca. 895 GB" loading="lazy">
  <figcaption>Mit „Eigenes" Limit kannst du nochmal eine Obergrenze pro Mac setzen – zusätzlich zur Quota auf Mini-Seite.</figcaption>
</figure>

„Fertig" klicken.

---

## **Das erste Backup**

Nach dem Bestätigen erscheint das Volume in der Time-Machine-Liste – zunächst mit dem Status „Auf Backup warten".

<figure>
  <img src="/images/blog/time-machine-zwei-macs-mac-mini-macbook-drahtlos-sichern/12-backup-warten.webp" alt="Time Machine zeigt MacBook-Backup, Status: Auf Backup warten" loading="lazy">
  <figcaption>Volume eingerichtet, Time Machine wartet auf den nächsten Backup-Zeitpunkt – meist sofort innerhalb der nächsten Minute.</figcaption>
</figure>

Kurz darauf wechselt der Status zu „Backup-Vorgang vorbereiten". Hier passiert noch nichts Sichtbares – Time Machine prüft, was alles gesichert werden muss.

<figure>
  <img src="/images/blog/time-machine-zwei-macs-mac-mini-macbook-drahtlos-sichern/13-backup-vorbereiten.webp" alt="Backup-Vorgang wird vorbereitet, Fortschrittsbalken am Anfang" loading="lazy">
  <figcaption>Time Machine indexiert die Dateien, die gesichert werden sollen. Bei großen Volumes kann das ein paar Minuten dauern.</figcaption>
</figure>

Und dann läuft das Backup. Das initiale Sichern ist langsam, weil alles übers Netzwerk geht.

<figure>
  <img src="/images/blog/time-machine-zwei-macs-mac-mini-macbook-drahtlos-sichern/14-backup-laeuft.webp" alt="Backup läuft mit 0,4 % fertig, ca. 8 Stunden verbleibend" loading="lazy">
  <figcaption>0,4 % nach den ersten Minuten – noch ungefähr 8 Stunden. Das ist normal beim ersten Backup.</figcaption>
</figure>

Das initiale Backup eines MacBooks mit 200 GB Daten kann übers WLAN gerne mal **eine Nacht oder zwei** brauchen. Wenn du beschleunigen willst:

- MacBook per Ethernet (USB-C-Adapter) direkt an den Mac mini oder den Switch hängen, **nur** fürs erste Backup
- Anschließend reicht WLAN völlig, weil nur noch Differenzen übertragen werden

WLAN sollte 5 GHz oder Wi-Fi 6 sein – über 2,4 GHz wird das eine Geduldsprobe.

---

## **Häufige Probleme und ihre Lösungen**

**„Zugriff verweigert" beim Verbinden:** Meistens fehlende Schreibrechte des Sharing-Users auf dem Volume oder „Eigentumsrechte ignorieren" eingeschaltet. Schritt 4 nochmal prüfen.

**Volume erscheint am MacBook nicht in der Liste:** Mac mini einmal neustarten, damit Bonjour den neuen Time-Machine-Share sauber annonciert. Beide Macs müssen im selben WLAN sein.

**Backup startet, bricht aber nach Minuten ab:** Oft ein Energiesparproblem – Mini ist eingeschlafen, bevor das Backup durch war. Wake-on-Network prüfen.

**Du kannst auf der Backup-Platte keinen Ordner anlegen:** Die Platte ist als Time-Machine-Volume versiegelt. Das ist normal. Lege stattdessen ein zweites APFS-Volume für andere Zwecke an (siehe Schritt 2).

---

## **Was diese Lösung nicht ist**

Time Machine schützt vor Hardwareausfällen und versehentlich gelöschten Dateien – aber **nicht vor allem**. Wenn dir die Daten wirklich wichtig sind, ergänze:

- **Offsite-Backup:** Backblaze, iCloud oder eine zweite Platte, die du regelmäßig austauschst und außer Haus lagerst
- **Cloud-Sync für aktive Projekte:** für die Sachen, an denen du gerade arbeitest, ist iCloud Drive oder Dropbox schneller im Wiederherstellen einzelner Dateien

Time Machine ist eine **Säule** deiner Backup-Strategie, nicht die ganze.

---

## **Fazit**

Was nach „einfach Platte anstecken" klingt, hat in der Praxis ein paar Fallstricke – versiegelte Volumes, Sharing-Only-User, Quota-Logik, Energiesparen. Wenn der Setup einmal steht, läuft er aber unsichtbar im Hintergrund, und im Notfall hast du beide Macs jederzeit wiederherstellbar.

Die wichtigste Erkenntnis: Eine einzige direkt angeschlossene APFS-Platte kann nicht gleichzeitig Time-Machine-Ziel für zwei Macs sein. Mit zwei APFS-Volumes im selben Container geht es trotzdem auf einer physischen Platte, **ohne** den Aufwand klassischer Partitionen.

Wenn du nach dieser Anleitung an einer Stelle hängst: Die meisten Fehler sitzen in den **Berechtigungen** – nicht beim Passwort, nicht im Netzwerk. Dort zuerst suchen.

Gutes Gelingen wünsch ich Dir!

Zuano
