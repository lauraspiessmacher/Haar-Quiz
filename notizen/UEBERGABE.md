# Übergabe: Haar-Guides

## Dateien
- `index.html` – Haar-Quiz (war ursprünglich eine umbenannte ZIP, jetzt entpackt)
- `leave-in-guide.html` – Leave-in-Guide, 103 Produkte (56 Drogerie, 47 High-End), alle mit freigestelltem Bild
- `shampoo-guide.html` – Shampoo-Guide, 163 Produkte, Reiter „Liste“, alle mit freigestelltem Bild
- `kopfhaut-guide.html` – Kopfhaut-Guide, 50 Produkte (Reiter: Normale, Trockene, Sensible, Juckende, Schuppige, Schnell fettende Kopfhaut, Kopfhautpeeling, Liste). Daten + Bau-Skript: notizen/kopfhaut-bau/ (data.py, build.py; Bilder als PNG im scratchpad kh/cut, gesichert als webp in notizen/kopfhaut-bilder/fertig). Notizen/INCI: notizen/kopfhaut-liste.md. Regel (Laura): nach INCI einordnen, nicht nach Marketing; Peeling = eigene Sektion; normale + fettende Kopfhaut bekommen auch Feuchtigkeitspflegen.
- `oel-guide.html` – Haaröl-Guide (letzter Einzel-Guide): 45 Öle (25 Drogerie, 20 High-End), Reiter nach Haardicke, Pille „Trockenes Öl“. Bau: notizen/oel-bau/, Notizen/INCI: notizen/oel-liste.md.
- `conditioner-guide.html` – Conditioner-Guide: 94 Conditioner (82 Drogerie, 12 High-End), davon 7 flüssige (Wonder Water) in „Feines Haar“. Bau: notizen/conditioner-bau/, Notizen/INCI: notizen/conditioner-liste.md.
- `masken-guide.html` – Haarmasken-Guide, 61 Masken (18 dm, 13 Rossmann, 30 High-End inkl. Olaplex Rich Hydration + Weightless Nourishing); Olaplex No.8 bewusst NICHT drin (nicht mehr im Handel), Aufbau wie Leave-in-Guide, Repair-Box mit „Wirkt im Inneren/von außen“
- `notizen/vorschau-gesamtguide.html` – klickbare VORSCHAU für den Gesamt-Guide. Laura will BEIDE Ansichten: A = Suche versteht „feine Haare fettige Kopfhaut kaputt“ + Marke, zeigt Routine (Shampoo nach Kopfhaut, Maske/Leave-in nach Haardicke, Kopfhautprodukte nur wenn Kopfhaut eingetippt); B = wie die einzelnen Guides (Reiter pro Produktart, darunter Alle/Kategorien/Liste). Später automatisch aus den Einzel-Guides zusammenbauen. Bau-Skripte: notizen/gesamtguide-bau/ (dump.js liest die Guides per Playwright aus → data.json, in template.html für __DATA__ einsetzen).
- `notizen/haarmasken-liste.md` – alle Masken mit Inhaltsstoffen, `notizen/masken-bilder/` – Lauras Rossmann-Produktbilder
- `notizen/leave-in-inhaltsstoffe.md` – abgeschriebene INCI-Listen aller Leave-ins

## Aufbau der Guides (beide gleich)
- Alles in einer HTML-Datei, Bilder als WebP-Data-URI in `const IMG = {"Marke|Produktname": "data:image/webp;base64,..."}`.
- Schlüssel = `brand + "|" + name` genau wie in den Produktdaten.
- Bilder: max. ca. 140–180 px breit/hoch, WebP Qualität ~85, Darstellung `.pic` 52×90 px rechts neben dem Text.
- Reiter „Liste“: nur Namen pro Kategorie, Knopf „Liste kopieren“.

## Bilder freistellen (was funktioniert hat)
- Laura möchte **echte Freisteller, ohne Hintergrund, nichts abgeschnitten** (Deckel, Pumpen, Sprühköpfe vollständig). Sie prüft genau.
- Bei weißem/hellem Hintergrund: Kontur pro Zeile und Spalte nachzeichnen (Abstand zur Hintergrundfarbe > ~3.5, 3–4× hochskaliert, Zeilen- UND Spaltenausdehnung schneiden, dann glätten). Das war am saubersten.
- `rembg` (Modell `isnet-general-use`) nur als Hilfe; bei weißen Flaschen auf weißem Grund schneidet es Teile ab.
- Shop-Abzeichen („Neu“, „Top bewertet“, dm-Badges) vorher übermalen, sonst bleiben sie hängen oder schneiden Deckel ab.
- Immer auf knallpinkem Hintergrund kontrollieren, dann sieht man jeden Rest.

## Arbeitsweise mit Lauras Screenshots (WICHTIG)
- Sobald Laura ein Bild/Screenshot schickt: SOFORT Produktname + Inhaltsstoffe in die passende Notiz abschreiben und, falls als Datei vorhanden, das Bild nach `notizen/…-bilder/` kopieren, committen, pushen. Nicht auf später verschieben.
- Bilder kommen manchmal nur als Vorschau an (keine Datei) und verschwinden später aus der Ansicht. Wenige Bilder ohne Text kommen meist als Datei an.
- Sonst so arbeiten, wie es am schnellsten geht (z. B. dm selbst abrufen).

## Inhaltliche Regeln (Lauras Haltung)
- Einordnung nach Inhaltsstoffen, nicht nach Werbung. Ehrliche „Gut zu wissen“-Hinweise, positiv formuliert.
- Spliss-Hinweis nur oben in der Einleitung, nicht bei Produkten.
- „Kaputte Haare“ nur, wenn Proteine/Peptide/Aminosäuren/Bond-Wirkstoffe **vor Parfum und Konservierungsstoffen** stehen. Ausnahme auf Lauras Wunsch: Redken Acidic Bonding (Zitronensäure) zählt als Repair.
- Feines Haar = „Feenhaar“: nur sehr leichte, wässrige Produkte.
- Fettende Kopfhaut: nur kräftige Reinigung ohne Silikon/Öle weit vorne. Silikon weit vorne → Normale Kopfhaut. Mit pflegenden Polymeren/Perlglanz/etwas Ölersatz → bleibt, aber Haardicke „normal bis dick“ (Okt. 2026 von Laura so gewünscht).
- Keine Fachwörter wie „Ester“ (stattdessen „leichter Ölersatz“).
- Laura ist keine Technikerin: Antworten auf Deutsch, einfach, ohne Fachbegriffe.

## Hitzeschutz im Leave-in-Guide
- `HEAT` = Gradzahl laut Hersteller (dm-Produktseite, Müller, Hagel, Lookfantastic, Marken-Shops). Nur mit Gradzahl wird das Feld angezeigt.
- Hitzeschutz ohne Gradzahl (deshalb ohne Feld): Pantene Wunder Haarcreme, Herbal Essences Blütensanft Spray, Bali Curls Leave-In Cream N°3, Oribe Priming Lotion.
- Wella Miracle Hair Rescue und Night Serum: laut Wella kein Hitzeschutz.
- Beschreibungen positiv formulieren: „pflegt leicht“ statt „kaum Pflegestoffe“.

## Bildquellen (was funktioniert)
- dm: Suche `product-search.services.dmtech.com/de/search/crawl?query=…`, Bilder von `products.dm-static.com` als PNG mit `f_png,c_fit,h_1000,w_1000` – schon freigestellt. Erstes Bild prüfen (L'Oréal hat oft einen Kreis dahinter → zweites Bild).
- High-End: Lookfantastic, Hagel-Shop (hagel-shop.de, sehr saubere Packshots), Marken-Shops (Shopify: `/products/<handle>.js`), Breuninger, Vichy.de, Shop-Apotheke.
- Müller (mueller.de) für einige Drogerie-Produkte, die dm nicht hat.
- Rossmann, Douglas, Flaconi, Notino: blocken automatische Abrufe (Sicherheitsabfrage), auch bei vollem Netzzugang.
- Schatten: rembg (isnet-general-use) mit eigener Kontur schneiden (Schnittmenge) entfernt Schatten; bei weißen Deckeln auf Weiß Vereinigung nehmen.

## Offen
- Masken-Guide: Regel für Kaputte Haare – einzelne Aminosäuren, die vermutlich nur den pH einstellen (Glutaminsäure bei Pantene/Herbal Essences, Arginin bei Fructis Locken), zählen NICHT. Mit Laura abstimmen, falls sie das anders sieht.
- Shampoo-Guide: fertig, 162 Shampoos (3× neboa von Rossmann ergänzt), alle mit Bild.
- Rossmann-Bilder kamen als Screenshots von Laura (je Screenshot eine Nachricht, sonst kommen sie nur als Vorschau an).
- Guides sind nur auf dem Branch, noch nicht online/in main.

## Großes Ziel (Laura, 06.10.2026) – beim Fertigbauen berücksichtigen
- Irgendwann EIN Tool / eine Webseite: alle Guides + alle Quiz + Wissensteil (Erklärtexte zu Themen, z. B. „Haarausfall“: was es gibt, was man tun kann – dort KEINE Produktempfehlungen, nur Erklärung). Soll sich wie eine Experience/Infoseite anfühlen, „von Laura für ihre Follower“.
- Follower sollen nachschauen können: „Neues Shampoo in der Drogerie – hat Laura es schon drin, für welchen Kopfhauttyp?“
- „Mein Haar“: Haardicke, Kopfhaut (mehrere), Haarzustand (mehrere, z. B. blondiert) einstellen → nur passende Produkte; Regler „Nur passende / Alle“.
- Gesamt-Guide: Ansicht A (Suche mit kombinierbaren Schlagwörtern, Routine Shampoo→Conditioner→Maske→Leave-in→Kopfhautpflege) UND Ansicht B (wie die Einzel-Guides). Laura will beide.
- Regeln: Shampoo nach KOPFHAUTTYP. Maske, Leave-in, Conditioner nach HAARDICKE + HAARZUSTAND. „Kaputte Haare“ = Aufbau (Protein/Bond), z. B. bei stark blondiert.
- Kopfhautpflege (Guide kommt noch) nach Bedürfnis: Feuchtigkeit, Schuppen, Haarausfall (Ausfallphase hinauszögern/blocken), evtl. beruhigend/ausgleichend. Ob immer alle Themen gezeigt werden oder nur das passende: mit Laura klären, wenn die Produkte da sind (Vorschau: passendes hervorgehoben, andere daneben).

- UPDATE (Laura, 06.10. nachmittags): KEINE Buttons „Ansicht A / Ansicht B“ mehr (Follower wären verwirrt). Stattdessen:
  - Oben Menü: Produkte · Quiz · Wissen + ein Button „Meine Haare“ (oben im Menü oder dort, wo vorher Ansicht A war).
  - „Meine Haare“ ist freiwillig: Haardicke/Haartyp, Kopfhauttyp, Kopfhautproblem, strapaziert/blondiert/stark geschädigt auswählen → nur passende Produkte (Regler Nur passende/Alle). Kann man auslassen.
  - Ohne Einstellung: normal nach Produkten suchen; Produktbereich aufgebaut wie die Einzel-Guides (Reiter pro Produktart, darunter Kategorien), mit Lauras Einschätzung unter jedem Produkt.
  - Die Schlagwort-Suche (feine Haare Schuppen …) darf versteckt weiter funktionieren, Laura weiß, wie es geht.
  - REIHENFOLGE: erst Einzel-Guides fertig (Masken, Conditioner, Kopfhautpflege), DANN den großen Guide bauen. Quiz: index.html = „Finde deinen Haartyp“; Laura hat insgesamt 3 Quiz, die anderen 2 schickt sie. Wissenstexte schreibt sie noch.
- Nachtrag 06.10. spät (notizen/nachtrag-liste.md): Wella Ultimate Smooth Miracle Oil Serum + 24/7 Silky Milk → Leave-in; Wella Ultimate Smooth Mask, Oil Reflections Mask, Coco & Eve Pre-Shampoo → Masken; The Ordinary Glycolic Toner (Peeling) + Goldwell Scalp Rebalance Fluid → Kopfhaut (jetzt 52); Goldwell Deep Cleansing Shampoo → Shampoo (Fettend).
- OFFENE FRAGE an Laura VOR einer Live-Website: Sollen Hinweise wie „Fast die gleiche Basis/Rezeptur wie …“ in den Guides bleiben? (Laura findet sie für sich gut, würde sie für live evtl. rausnehmen – unbedingt nachfragen.)
- OFFENE FRAGE: Dünn-Text „wenige Haare und wenig Fülle“ auch im Conditioner-, Masken- und Leave-in-Guide an die neue Definition (Dicke des einzelnen Haares, nicht Fülle) anpassen?

## Stand 06.10.2026 spät – NÄCHSTER SCHRITT: Gesamtseite bauen
- Alle 6 Einzel-Guides fertig: shampoo-guide.html (163), conditioner-guide.html (94), masken-guide.html (61), leave-in-guide.html (103), kopfhaut-guide.html (52), oel-guide.html (45).
- UX-Konzept: notizen/ux-konzept.md + notizen/ux-mockup.html (+ ux-mockup-optionen.html). Empfehlung Option 1 „Regal“ (Produktart zuerst, Leiste unten Produkte·Quiz·Wissen·Meine Haare, Routine-Schritte, Teilen-Links, Bilder als einzelne WebP-Dateien mit Nachladen). Laura hat die Richtung noch NICHT bestätigt.
- Vor dem Bauen mit Laura klären (aus ux-konzept.md Abschnitt 6): Startseite mit Routine-Kacheln oder direkt Shampoo? Welche Haarzustände bei „Meine Haare“, was macht „Gefärbt“? Quiz (Fein/Mittel/Dick) → 5 Haardicken? Webadresse + wer lädt hoch? Dazu: Dünn-Text in Conditioner/Masken/Leave-in angleichen? „Fast die gleiche Basis wie …“ live behalten?
- Laura wollte die Zusammenführung mit ihr gemeinsam starten (Limit fast erreicht).
- Lauras Antworten (06.10. spät): „Meine Haare“ optional, Auswahl Haardicke (5) + Kopfhauttyp reicht; „Gefärbt“ unwichtig. Blondiert/geschädigt nur, wenn sinnvoll und nicht umständlich. Quiz bleibt wie es ist, KEINE Verknüpfung der Quiz-Ergebnisse mit den Produktseiten (fein/sehr dick sind ihr Add-on). Startseite: Laura möchte eine Empfehlung. Sie hatte die Vorschau (ux-mockup.html) nicht gesehen → erneut geschickt.
- Dünn-Text in Conditioner-, Masken- und Leave-in-Guide angeglichen („Das einzelne Haar ist dünn, aber nicht hauchdünn. Wie viele Haare du hast, spielt dabei keine Rolle. …“).
- Laura zur Gesamtseite: Regal-Übersicht wirkt ihr UNÜBERSICHTLICH → neue Idee nötig. Reihenfolge der Routine: Shampoo → Maske → Conditioner → Leave-in → Haaröl (Kopfhautpflege außerhalb der Reihenfolge). Button heißt nur „Meine Haare“. „Meine Haare“: Haardicke + Kopfhauttyp (+ evtl. Schalter kaputt/blondiert).
- Laura: Für die Gesamtseite morgen MEHRERE klickbare Vorschauen mit Alternativen zeigen (mindestens Idee A „direkt wie die Guides, Produktart-Zeile oben“ und Idee B „schlichte Liste als Startseite“), sie kann es sich sonst schwer vorstellen. Erst danach entscheiden und bauen.
