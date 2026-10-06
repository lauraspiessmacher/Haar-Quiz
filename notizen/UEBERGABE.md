# Übergabe: Haar-Guides

## Dateien
- `index.html` – Haar-Quiz (war ursprünglich eine umbenannte ZIP, jetzt entpackt)
- `leave-in-guide.html` – Leave-in-Guide, 101 Produkte (56 Drogerie, 45 High-End), alle mit freigestelltem Bild
- `shampoo-guide.html` – Shampoo-Guide, 159 Produkte, Reiter „Liste“, alle 159 mit freigestelltem Bild
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
- Shampoo-Guide: fertig, alle 159 Bilder drin.
- Rossmann-Bilder kamen als Screenshots von Laura (je Screenshot eine Nachricht, sonst kommen sie nur als Vorschau an).
- Guides sind nur auf dem Branch, noch nicht online/in main.
