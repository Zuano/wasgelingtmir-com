# DNS-Umstellung auf GitHub Pages – Anleitung

Diese Datei erklärt, wie du die Domain **wasgelingtmir.com** von WordPress.com auf GitHub Pages umziehst.

## Warum DNS umstellen?
Aktuell zeigt **wasgelingtmir.com** auf WordPress.com. Damit die neue Seite unter dieser Domain erreichbar wird, müssen die DNS-Einträge (Domain Name System) bei deinem Domain-Anbieter auf GitHub Pages zeigen.

## Vorbereitung: Wo ist die Domain registriert?

Bevor wir etwas ändern: **Wo hast du wasgelingtmir.com gekauft?**
Mögliche Anbieter:
- WordPress.com / Automattic (falls über WordPress gekauft)
- GoDaddy, Namecheap, Gandi, Hetzner, world4you, ...

Du findest das raus:
1. Rechnungen durchsuchen nach "Domain" / "wasgelingtmir.com"
2. Oder im WordPress.com-Dashboard: **Verwalten → Domains** → dort steht, wer sie verwaltet.

## Die neuen DNS-Einträge für GitHub Pages

Diese **vier A-Records** und **ein AAAA-Record** für das Root-Domain (`wasgelingtmir.com`):

| Typ | Host | Wert |
|---|---|---|
| A | @ | `185.199.108.153` |
| A | @ | `185.199.109.153` |
| A | @ | `185.199.110.153` |
| A | @ | `185.199.111.153` |
| AAAA | @ | `2606:50c0:8000::153` |
| AAAA | @ | `2606:50c0:8001::153` |
| AAAA | @ | `2606:50c0:8002::153` |
| AAAA | @ | `2606:50c0:8003::153` |

Und ein **CNAME-Record** für `www.wasgelingtmir.com`:

| Typ | Host | Wert |
|---|---|---|
| CNAME | www | `zuano.github.io` |

## Schritt-für-Schritt

1. **Melde dich beim Domain-Anbieter an.**
2. Suche nach der DNS-Verwaltung (oft "DNS", "Nameserver", "Zone-File", "DNS-Einträge").
3. **Alte WordPress-Einträge** zu den A-Records und AAAA-Records notieren (zur Sicherheit), dann löschen.
4. Die oben genannten acht IP-Adressen als A- bzw. AAAA-Records einfügen.
5. CNAME-Record für `www` auf `zuano.github.io` setzen.
6. Speichern.

Die Änderungen können **bis zu 24 Stunden** weltweit durchgereicht werden – meistens viel schneller.

## Nach der Umstellung: HTTPS aktivieren

1. Gehe auf **https://github.com/Zuano/wasgelingtmir-com/settings/pages**
2. Unter "Custom domain" steht `wasgelingtmir.com`. Warte bis daneben ein grünes Häkchen erscheint.
3. Aktiviere **Enforce HTTPS** (kleine Checkbox ganz unten).

Das kann ein paar Minuten bis zu 24 Stunden dauern, weil ein Let's-Encrypt-Zertifikat automatisch ausgestellt wird.

## Verifizieren

Wenn alles passt:
```bash
# Sollte 185.199.x.153 liefern / should return 185.199.x.153
dig wasgelingtmir.com +short

# Seite sollte antworten
curl -I https://wasgelingtmir.com
```

## WordPress.com – optional
Nach erfolgreicher Umstellung kannst du:
- Dein WordPress.com-Abo herunterstufen auf **kostenlos** (oder kündigen)
- Die alte Seite löschen – aber erst, wenn die neue Seite 100 % funktioniert!

## Wenn etwas nicht geht
- In GitHub Pages Settings zeigt es dir oft direkt Probleme an.
- DNS-Check: https://dnschecker.org/#A/wasgelingtmir.com
- HTTPS-Zertifikat braucht manchmal 1–2 Stunden nach DNS-Änderung.

---

## Für Claude: was am Code umgestellt werden muss

Zur Zeit läuft die Seite auf dem GitHub-Pages-Unterordner `/wasgelingtmir-com/`.
Sobald du weißt, dass der DNS-Umzug durch ist, mache ich Folgendes:

1. **`public/CNAME` neu anlegen** mit Inhalt `wasgelingtmir.com`
2. **GitHub Actions Workflow anpassen** (`.github/workflows/deploy.yml`):
   - Env-Variable `CUSTOM_DOMAIN=true` setzen beim Build-Schritt
3. **Rebuild + Push** – dann lädt die Seite unter der eigenen Domain ohne Unterordner, alle Links passen sich automatisch an (wegen der Link-Helper-Struktur).
4. **In GitHub Pages Settings:** Custom Domain eintragen (`wasgelingtmir.com`) und "Enforce HTTPS" aktivieren.

Kein Code-Umbau nötig – alles fertig vorbereitet.
