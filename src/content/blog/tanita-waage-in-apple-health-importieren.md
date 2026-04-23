---
title: "Tanita Waage in Apple Health importieren"
description: "Tanita bietet nur für ein paar wenige Waagen ein Tool an. Und selbst die lassen zu wünschen übrig."
pubDate: "2020-03-29"
category: "Gesundheit"
categorySlug: "gesundheit"
slug: "tanita-waage-in-apple-health-importieren"
heroImage: "/images/blog/tanita-waage-in-apple-health-importieren/iu.jpeg"
originalUrl: "https://wasgelingtmir.com/2020/03/29/tanita-waage-in-apple-health-importieren/"
wordpressId: "182"
---

## CSV-Daten meiner Tanita Körperfettwaage in Apple Health importieren

### Was brauche ich dazu?

- Eine Tanita Waage – in meinem Fall ist das die alte Tanita BC-601 aus dem Jahr 2012
- Die SD-Karte der Waage (mit Messergebnissen drauf)
- Einen SD-Kartenleser oder SD-Kartenlese-Slot
- Microsoft Excel (Office)
- Vorzugsweise einen Computer oder Mac. In meinem Fall einen Mac
- Die iOS-App [Health CSV Importer](https://apps.apple.com/us/app/health-csv-importer/id1275959806)

### Warum das Ganze?

Tanita bietet nur für ein paar wenige Waagen ein Tool an. Und selbst die lassen zu wünschen übrig. Für meine BC-601-Waage gibt es von Tanita gar keine aktuelle App.

Trotzdem hat Tanita einen SD-Kartenslot eingebaut, wo die ganzen Daten gespeichert werden.

### Schritt-für-Schritt-Anleitung

Entferne die SD Karte aus der Waage:

![iu](/images/blog/tanita-waage-in-apple-health-importieren/iu.jpeg) Bildquelle: waagen-test.de

Stecke die SD-Karte in den Kartenleser und verbinde ihn mit deinem USB-Port am Computer.

(Hier sind Anwender-Kenntnisse vorausgesetzt.)

![SD Kartenleser mit Mac verbinden.png](/images/blog/tanita-waage-in-apple-health-importieren/sd-kartenleser-mit-mac-verbinden.png)

Die SD Karte wird als "NO NAME" angezeigt. Hier ist auch schon der Ordner "TANITA"

![Bildschirmfoto 2020-03-24 um 10.08.40.png](/images/blog/tanita-waage-in-apple-health-importieren/bildschirmfoto-2020-03-24-um-10.08.40.png)

Im Verzeichnis "NO Name"/TANITA/GRAPHV1/DATA/ findet ihr dann die CSV Dateien.

![Bildschirmfoto 2020-03-24 um 10.10.40.png](/images/blog/tanita-waage-in-apple-health-importieren/bildschirmfoto-2020-03-24-um-10.10.40.png)

Wenn ihr heute das letzte Mal euch gewogen habt, dann seht ihr auch das Datum

![Bildschirmfoto 2020-03-24 um 10.12.56.png](/images/blog/tanita-waage-in-apple-health-importieren/bildschirmfoto-2020-03-24-um-10.12.56.png)

***Kopiert Euch die DATAx.CSV in Euer iCloud Verzeichnis. Das ist wichtig, damit ihr nicht die Daten Beschädigt.***

Mit Rechtsklick öffnen mit Excel öffnet ihr die Datei

![Bildschirmfoto 2020-03-24 um 10.14.41.png](/images/blog/tanita-waage-in-apple-health-importieren/bildschirmfoto-2020-03-24-um-10.14.41.png)

Es zeigt sich dieses Bild:

![Bildschirmfoto 2020-03-24 um 10.15.13.png](/images/blog/tanita-waage-in-apple-health-importieren/bildschirmfoto-2020-03-24-um-10.15.13.png)

Damit ein wenig mehr System reinkommt, wollen wir die Daten sortieren.

Klickt die Spalte A an, indem ihr oben auf das A klickt:

![Bildschirmfoto 2020-03-24 um 10.16.31.png](/images/blog/tanita-waage-in-apple-health-importieren/bildschirmfoto-2020-03-24-um-10.16.31.png)

Dann geht ihr in der Menüleiste auf "Daten" und klickt auf "Text in Spalten"

![Bildschirmfoto 2020-03-24 um 10.18.42.png](/images/blog/tanita-waage-in-apple-health-importieren/bildschirmfoto-2020-03-24-um-10.18.42-1.png)

Klickt auf "Mit Trennzeichen versehen" und weiter.

![Bildschirmfoto 2020-03-24 um 10.20.33.png](/images/blog/tanita-waage-in-apple-health-importieren/bildschirmfoto-2020-03-24-um-10.20.33.png)

Wählt "Komma" und klickt auf weiter:

![Bildschirmfoto 2020-03-24 um 10.21.03.png](/images/blog/tanita-waage-in-apple-health-importieren/bildschirmfoto-2020-03-24-um-10.21.03.png)

Klickt auf erweitert:

![Bildschirmfoto 2020-03-24 um 10.32.57.png](/images/blog/tanita-waage-in-apple-health-importieren/bildschirmfoto-2020-03-24-um-10.32.57.png)

Wählt bei Dezimaltrennzeichen den "." Punkt aus

und bei 1000er Trennzeichen das "," Komma aus

![Bildschirmfoto 2020-03-24 um 10.35.05.png](/images/blog/tanita-waage-in-apple-health-importieren/bildschirmfoto-2020-03-24-um-10.35.05.png)

so sollte es aussehen: Dann auf Ok klicken

![Bildschirmfoto 2020-03-24 um 10.36.20.png](/images/blog/tanita-waage-in-apple-health-importieren/bildschirmfoto-2020-03-24-um-10.36.20.png)

Dann auf Fertig stellen klicken![Bildschirmfoto 2020-03-24 um 10.37.16.png](/images/blog/tanita-waage-in-apple-health-importieren/bildschirmfoto-2020-03-24-um-10.37.16.png)

Nun solltet es so aussehen:

Wenn nicht, dann klickt auf Rückgängig machen und wiederholt nochmal die Schritte.

![Bildschirmfoto 2020-03-24 um 10.37.33.png](/images/blog/tanita-waage-in-apple-health-importieren/bildschirmfoto-2020-03-24-um-10.37.33.png)

Hier sind jetzt alle möglichen Daten. In meinem Beispiel sind jetzt in der Spalte "N" das Datum, in der Spalte "P" die Uhrzeit und in der Spalte "AB" das Gewicht.

In der Spalte AD der Gesamtkörperfettanteil.

*Es gibt dann noch den Körperfettanteil der Arme und Beine, die habe ich aber nicht in Health importiert.*

Nun löscht ihr die restlichen Spalten.

Spalte markieren und Command + "-" (Command + Bindestrich) oder Windows: Strg. + Bindestrich (Das Minuszeichen) drücken.

Oder markieren und rechte Maustaste "Zellen löschen" wählen.

Es sollten jetzt vier Spalten übrig sein:

![Bildschirmfoto 2020-03-24 um 10.42.40.png](/images/blog/tanita-waage-in-apple-health-importieren/bildschirmfoto-2020-03-24-um-10.42.40.png)

**Bevor wir zum CSV Importer auf dem iPhone gehen, müssen wir noch das Datum und die Uhrzeit der Spalten zusammen führen und eine Kopfzeile hinzufügen:**

Drückt rechte Maustaste auf die Zeile 1 und klickt auf Zeile Einfügen:

![Bildschirmfoto 2020-03-24 um 10.45.38.png](/images/blog/tanita-waage-in-apple-health-importieren/bildschirmfoto-2020-03-24-um-10.45.38.png)

Nun solltet ihr oberhalb der Daten eine leere (Kopf)Zeile haben:

![Bildschirmfoto 2020-03-24 um 10.47.52.png](/images/blog/tanita-waage-in-apple-health-importieren/bildschirmfoto-2020-03-24-um-10.47.52.png)

Nun fügt noch eine leere Spalte ein. (Die brauchen wir um Datum und Uhrzeit zusammenzufügen):

![Bildschirmfoto 2020-03-24 um 10.49.23.png](/images/blog/tanita-waage-in-apple-health-importieren/bildschirmfoto-2020-03-24-um-10.49.23.png)

Markiert die leere Spalte, Rechtsklick auf die Spalte und Zellen formatieren:

![Bildschirmfoto 2020-03-24 um 10.54.29.png](/images/blog/tanita-waage-in-apple-health-importieren/bildschirmfoto-2020-03-24-um-10.54.29.png)

Klickt auf Benutzerdefiniert und schreibt diesen Text hinein: **TT.MM.JJJJ hh:mm:ss**

(inklusive Leerzeichen zwischen Jahr und Stunde)

![Bildschirmfoto 2020-03-24 um 10.53.15.png](/images/blog/tanita-waage-in-apple-health-importieren/bildschirmfoto-2020-03-24-um-10.53.15.png)

Datum und Uhrzeit zusammenfügen:

Schreibt in die Zeile C2 Folgendes hinein:

![Bildschirmfoto 2020-03-24 um 10.59.04.png](/images/blog/tanita-waage-in-apple-health-importieren/bildschirmfoto-2020-03-24-um-10.59.04.png)

![Datum und Zeit zusammen führen.png](/images/blog/tanita-waage-in-apple-health-importieren/datum-und-zeit-zusammen-fc3bchren.png)

Wenn ihr Enter drückt, sollte es nun so aussehen: "Datum Leerzeichen Uhrzeit"

![Bildschirmfoto 2020-03-24 um 11.02.00.png](/images/blog/tanita-waage-in-apple-health-importieren/bildschirmfoto-2020-03-24-um-11.02.00.png)

Nun drückt ihr rechts unten auf das Kästchen und zieht es komplett bis hinunter:

![Bildschirmfoto 2020-03-24 um 11.03.24.png](/images/blog/tanita-waage-in-apple-health-importieren/bildschirmfoto-2020-03-24-um-11.03.24.png)

Nun beschriftet die Kopfzeile mit "Date / Time", Weight und Bodyfat

![Bildschirmfoto 2020-03-24 um 11.06.42.png](/images/blog/tanita-waage-in-apple-health-importieren/bildschirmfoto-2020-03-24-um-11.06.42.png)

**Speichert** es in Euer **iCloud Drive Laufwerk oder auf icloud.com** und klickt bei dieser Meldung auf Ja

![Bildschirmfoto 2020-03-24 um 11.05.13.png](/images/blog/tanita-waage-in-apple-health-importieren/bildschirmfoto-2020-03-24-um-11.05.13.png)

**Tipp:** Testet den Import erstmal nur mit einem Datensatz und nicht gleich mit allen. Falls etwas schiefgeht, habt ihr nur einen Wert in Health eingetragen. Löscht dazu alle Zeilen außer die letzte.

Nun kauft die iOS App [Health CSV Importer](https://apps.apple.com/us/app/health-csv-importer/id1275959806)

![IMG_CFD474339090-1.jpeg](/images/blog/tanita-waage-in-apple-health-importieren/img_cfd474339090-1.jpeg)

Drückt auf Get Started.

![IMG_0009.PNG](/images/blog/tanita-waage-in-apple-health-importieren/img_0009.png)

Es öffnet sich iCloud Drive und ihr wählt am besten zuerst mal die Test Datei mit nur einem Datensatz drinnen.

![IMG_0012.PNG](/images/blog/tanita-waage-in-apple-health-importieren/img_0012.png)

Die Spalte mit der Kopfzeile Date / Time sollte erkannt worden sein und ihr klickt auf next:

![IMG_0019.PNG](/images/blog/tanita-waage-in-apple-health-importieren/img_0019.png)

End Date (Enddatum) könnt ihr in dem Fall überspringen. Das wäre, falls ihr Läufe oder Radtouren etc. importieren wolltet.

![IMG_0020.PNG](/images/blog/tanita-waage-in-apple-health-importieren/img_0020.png)

***Vorsicht!: Das Gewicht ist in Pfund ausgewählt! Das müsst ihr noch in kg ändern***

![IMG_0021.PNG](/images/blog/tanita-waage-in-apple-health-importieren/img_0021.png)

Pound ändern zu kg

![IMG_0022.PNG](/images/blog/tanita-waage-in-apple-health-importieren/img_0022.png)

![IMG_0023.PNG](/images/blog/tanita-waage-in-apple-health-importieren/img_0023.png)

Zugriff auf Apple Health gewähren. Erlauben klicken

![IMG_0025.PNG](/images/blog/tanita-waage-in-apple-health-importieren/img_0025.png)

Fertig!

Nun könnt ihr noch Eure Daten in der Apple Health App kontrollieren!

Gutes Gelingen!

Disclaimer

Das ist keine Werbung. Ich wurde von keinem Software-Anbieter bezahlt. Ich mache diese Anleitung nur, weil mir die App so geholfen hat und ich es anderen auch zeigen möchte.

Ich übernehme keine Haftung für irgendwelche Schäden. Alle Handlungen auf eigene Gefahr.

Falls du irgendwelche Verbesserungsvorschläge hast, hinterlasse es mir gerne hier:
