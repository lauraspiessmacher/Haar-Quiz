# Übergabe: Haar-Guides

- WICHTIG: Mit Laura IMMER auf Deutsch schreiben, auch kurze Zwischenmeldungen während der Arbeit.

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

## 07.10.2026 – Vorschau 2 der Gesamtseite (notizen/ux-vorschau-2.html)
- Lauras Wunsch: muss auch auf dem Laptop gut aussehen; vor allem IHR Nachschlage-Werkzeug für Beratungen (später Website). Navigation OBEN wie bei einer Website (Produkte · Quiz · Wissen · Meine Haare, mit Symbolen), Titel „Haarpflege einfach erklärt“. Produktarten als klar klickbare Kacheln ohne „Waschen/Pflegen“-Stufen (z. B. „Shampoo – nach Kopfhauttyp · 163“). Button heißt „Meine Haare“, dazu „Quiz machen“. Suche bleibt. Nichts weglassen, nur anders anordnen.
- Umgesetzt mit ALLEN 518 echten Produkten. Bau: notizen/gesamtguide-bau/dump.js (liest alle 6 Guides → JSON) + build-vorschau.py + vorschau2-template.html. Neu bauen: `node dump.js data.json && python3 build-vorschau.py data.json`.
- Funktionen: Suche über alle Produktarten (Wörter wie „shampoo“, „öl“ grenzen ein; „fettige“, „feine“ werden verstanden), Drogerie/High-End, Kategorien, Liste mit Kopieren, „Meine Haare“ (Haardicke, Kopfhaut, Zusatz kaputt) mit „Nur passende / Alle“, Punkt an den eigenen Kategorien, Teilen-Links über die Adresse (#/shampoo/kraeftig), Quiz-Seite (verlinkt index.html), Wissen-Platzhalter.
- Laura: Produktarten sind die HAUPTREITER → als zweite Reiterzeile in der Kopfzeile (Shampoo · Maske · Conditioner · Leave-in · Haaröl · Kopfhautpflege, mit Symbol und Anzahl), Kacheln entfernt, Überschrift „Alle Produkte“ entfernt. Auf dem Handy ist die Reiterzeile seitlich wischbar.
- Problem 07.10.: In Lauras Vorschaufenster lief das Programm der 3,2-MB-Datei nicht (nur Suchleiste sichtbar). Lösung: privater Link https://claude.ai/artifact/7GncL1B7ZJVHi8Dtsj6cbS (Datei notizen/ux-vorschau-2-link.html + Quiz als quiz.html). Updates: build-vorschau.py ausführen und dieselbe Datei neu veröffentlichen (gleiche Adresse). Bereichs-Links: …#shampoo.kraeftig, …#oel.fein, …#quiz.
- Quiz 2 von Laura: quiz-kopfhaut.html (Kopfhaut-Check, 9 Fragen). Unter „Quiz“ verlinkt. Quiz 3 fehlt noch.

## 07.10.2026 – OFFIZIELLE GESAMTSEITE (Laura: „Go“)
- Datei: haarpflege.html (Hauptordner, zum lokalen Öffnen) + privater Link https://claude.ai/artifact/7GncL1B7ZJVHi8Dtsj6cbS (Datei notizen/gesamtguide-bau/haarpflege-link.html + die drei Quiz als Zusatzdateien).
- Neu bauen nach jeder Guide-Änderung: `cd notizen/gesamtguide-bau && node dump.js data.json && python3 build-vorschau.py data.json`, dann haarpflege-link.html neu veröffentlichen (Artifact mit url oben, gleiche Adresse).
- Quiz: quiz-haar.html (Haar-Check, Struktur), quiz-pflege.html (Pflege-Check, Dicke + Zustand), quiz-kopfhaut.html (Kopfhaut-Check). Das alte Quiz index.html („Finde deinen Haartyp“) ist nicht mehr verlinkt, Datei bleibt (Laura fragen, ob es weg kann).
- Alte Vorschauen liegen in notizen/archiv/.
- Nächste Schritte: Laura nutzt die Seite und sammelt Feedback (Design, Anordnung, Texte) → in kleinen Runden umsetzen. Später: Wissenstexte, Website (Ladezeit: Bilder als einzelne Dateien), vorher „Fast die gleiche Basis wie …“ klären.
- Laura (07.10.): Aufbau „nahezu perfekt“. Wunsch: Suchleiste kleiner (umgesetzt, auch im offiziellen Link) und mehr Eleganz/„ihr Touch“, Signature-Farbe kühles Dunkelbraun (#382F2E). Design-Vorschau mit Umschalter: https://claude.ai/artifact/K1wkeRzkxv3iDQ6cuP9mwU — A Espresso (Kopfzeile dunkelbraun), B Hell (viel Luft, Großbuchstaben, feine Linien), C Braun (wie die Quiz), „Jetzt“ = aktueller Stand. Schriften dort: Cormorant Garamond + Jost (Google Fonts), sanftes Einblenden der Karten. Dateien: notizen/gesamtguide-bau/design-varianten.html + design-umschalter.html (wird von build-vorschau.py in design-vorschau-link.html eingesetzt). Laura entscheidet; evtl. schickt sie eine Website als Vorbild.
- Laura sah Variante C nicht → Umschalter zusätzlich oben auf der Seite, Farben von B/C mit Vorrang (!important), getestet in Hell/Dunkel.
- Laura (07.10.): Favorit Variante B. Wünsche umgesetzt in der Design-Vorschau (https://claude.ai/artifact/K1wkeRzkxv3iDQ6cuP9mwU): Schrift-Auswahl für Überschriften (Cormorant, Bodoni, Playfair, Italiana, Gilda), alle OFL und EINGEBETTET (keine Google-Fonts-Verbindung wegen Abmahnungen!) – Dateien: notizen/gesamtguide-bau/schriften/*.woff2 + schriften-eingebettet.css, Fließtext Jost (ebenfalls eingebettet). Erklärtext je Produktart jetzt sichtbar und umrandet (leicht braun hinterlegt) statt Aufklappen. Quiz-Seite: drei dunkelbraune Karten mit Strähnen-Linien, „Für dein Shampoo/deine Pflege/dein Styling“, Fragenzahl und Dauer, Schlusssatz. „Meine Haare“ in Sandton. Signatur-Strähnen neben dem Namen. Offizieller Link bekommt das erst nach Lauras Entscheidung (Schrift wählen).
- Laura: Beige bei „Meine Haare“ passt nicht → raus (jetzt feine braune Umrandung). Schrift: Playfair gefällt am besten (voreingestellt). Name „Haarpflege einfach erklärt“ oben wie die Überschrift „Shampoo“: Playfair kursiv, dunkelbraun. Laura möchte eine Website als Vibe-Vorbild schicken (Beauty-Bereich, Startseite, Produktbilder; elegant + verspielt).

## Design-Runde (Variante B, Feinschliff)
- Beige/Sand (#D6B98F) komplett raus, auch bei den Quiz-Labels „Für dein …“ (jetzt #E9DFD2).
- Dunkelbraune Flächen bleiben (Laura mag sie). „Meine Haare“ = helleres kühles Braun #7A6A65 mit cremefarbener Schrift.
- Produkte wieder mit dünnem dunkelbraunem Rahmen (rgba(56,47,46,.30), Radius 14px).
- Logo „HAARPFLEGE EINFACH ERKLÄRT“ testweise in Großbuchstaben (Playfair).
- Referenz-Webseite von Laura: rouje.com (Seite „homepage-leichter“, Beauty). Schriften dort: „Panama“ (schmale Serifenschrift, Großbuchstaben) und „Diatype“ (Grotesk) – beide kostenpflichtig, kostenlose Ersatzschriften nötig.
- Rouje-Stil als Umschalter in der Design-Vorschau (Stil: Bisher / Rouje-Stil; Standard = Rouje-Stil + Schrift „Instrument“):
  Ersatz für „Panama“ = Instrument Serif (OFL), alternativ Libre Caslon Condensed (OFL); Ersatz für „Diatype“ = Instrument Sans (OFL). Alle eingebettet (schriften/ + schriften-eingebettet.css).
  Riesige Überschriften in Großbuchstaben (SHAMPOO, QUIZ), Untertitel kursiv, hellerer Cremegrund #FBF7F3, eckigere Knöpfe,
  Produktbild groß auf hellem Feld oben in der Karte (Handy: Bild rechts), dünner dunkelbrauner Rahmen bleibt.
  Hinweis: Produktbilder sind nur ~150 px hoch – für die echte Webseite später größere Bilder nehmen.
- ENTSCHEIDUNG Laura: Rouje-Stil + Schrift „Instrument“ bleiben. Große Überschriften und umrahmte Produkte gefallen ihr sehr.
- „Passt zu“-Rahmen: bei langem Text kleinere Schrift und weniger runde Ecken (Klasse .also.long ab 35 Zeichen), damit nichts mehr auf der Linie sitzt (Beispiel: Balea Kopfhaut Tonikum).
- Untertitel „Von Laura, deiner Haarpflege-Bestie“: gerade, ohne Serifen (Instrument Sans), hebt sich vom Logo ab.
- Fotos macht Laura selbst, kommen später.
- Quizze in den privaten Links: Als eigene Unterseiten blieben sie leer (alle Quiztexte entstehen per Skript, das dort nicht lief).
  Jetzt stecken sie direkt in der Seite (quiz-einbettung.html, eingefügt von build-vorschau.py) und öffnen sich als Vollbild-Fenster mit „Zurück zum Guide“.
  Die lokale haarpflege.html verlinkt weiter auf die Dateien quiz-*.html daneben. Für die spätere echte Webseite gehen normale Unterseiten.

## Startseite (Landingpage) – in der Design-Vorschau
- Neue Ansicht „start“ (Standard ohne #, Logo-Klick führt hin, Link #start). Inhalt: Foto-Platzhalter (Torbogen), „Von kaputten zu gesunden Haaren“, Vorstellung,
  dunkler Block „Meine Einschätzung, nicht die der Marken“, 4 Kacheln (Produkte, Quiz, Wissen, Meine Haare), „Deine Routine“ mit 6 Zeichnungen.
- Texte sind ENTWURF – Laura soll sie prüfen. Behauptung „nicht gesponsert“ bewusst vorsichtig formuliert („Nichts davon ist von den Marken übernommen“).
- Zeichnungen: routine-zeichnungen.html (wird von build-vorschau.py für __ROUTINE__ eingesetzt). Laura will sie später mit einem KI-Bildprogramm (Higgsfield) neu machen → nur diese Datei ersetzen.
- Offizieller Link (7GncL…) noch NICHT neu veröffentlicht: er würde sonst auch mit der Startseite öffnen (Laura nutzt ihn für Beratungen).
- Zukunftsidee: „Produkt kaufen“-Knopf in der Produktkarte mit Affiliate-Link (Amazon o. ä.) – Werbekennzeichnung nötig. Noch nicht bauen.
- Suchleiste wieder rund (Laura mag es runder, auch im Rouje-Stil).
- Wissen-Bereich = auch Lauras Ideen-Speicher (graue „Kommt bald“-Kacheln). Themen: Spliss & Haarbruch: der Unterschied · Die LL-Methode · Pre-Wash-Routinen (statt ÖWC) ·
  Haaröle erklärt (statt Trockene Öle) · Der Haarzyklus · Haarausfall (Arten) · Kopfhautgesundheit · Haarmythen · Haarporosität. Laura schickt die Texte.
- Startseite: laufende Leiste „Haarpflege 1×1“ (Lauras Serie, Instagram + TikTok) zwischen Kacheln und Routine. Daten im Template unter `const SERIE` (teil, titel, url, bild), `SERIE_MAX = 10` (neueste zuerst).
  Hält bei Maus darüber / Antippen an, bei „Bewegung reduzieren“ keine Animation. Knopf „Alle Folgen ansehen“ → aktuell Instagram-Profil (Platzhalter).
  KEINE eingebetteten Instagram-/TikTok-Player (laden fremde Skripte/Cookies → Einwilligung nötig, Abmahnrisiko). Stattdessen: Titelbild + Link zur Plattform.
- Startseiten-Foto: notizen/bilder/laura-startseite.jpg (Original), Web-Version gesamtguide-bau/laura-startseite-web.jpg (900 px), wird von build-vorschau.py für __LAURA_FOTO__ eingesetzt. Laura: „noch nicht das perfekteste Bild“ → später austauschbar (Datei ersetzen).
- Hair Journey (angepinnter Beitrag auf Instagram + TikTok, Haarverlauf von der Jugend bis heute):
  Link-Zeile unter den Hero-Knöpfen („Du glaubst mir nicht? Schau dir meine Hair Journey an →“) + eigener Abschnitt nach „Meine Einschätzung“ mit Cover und Knöpfen Instagram/TikTok.
  Links in build-vorschau.py (JOURNEY_IG, JOURNEY_TT – noch Platzhalter: Profil bzw. tiktok.com). Cover: gesamtguide-bau/hair-journey-cover.jpg ablegen → wird automatisch eingesetzt.
- Merkliste: „+“ oben rechts an jeder Produktkarte (gemerkt = dunkelbraun mit Haken). Neuer Reiter „Merkliste“ mit Zähler (Handy: 5 Reiter).
  Ansicht #merkliste: Produkte nach Routine-Reihenfolge gruppiert, „Als Einkaufsliste kopieren“, „Alle entfernen“. Speicherung nur im Browser (localStorage „merkliste“, Schlüssel Produktart|Marke|Name), kein Konto, keine Daten bei Laura.
  Später möglich: Merkliste per Link teilen, „Kaufen“-Links (Affiliate, gekennzeichnet) direkt in der Merkliste.
- Merkliste kompakt: kleine Karten (Bild, Marke, Name, Drogerie/High-End), Laptop ~5 nebeneinander, Handy 2.
- „Jetzt kaufen“-Knopf: unten rechts in der Produktkarte, mit „Werbelink“-Hinweis daneben (Kennzeichnungspflicht). Links kommen in gesamtguide-bau/kauflinks.json
  (Schlüssel „produktart|Marke|Name“ → URL), build-vorschau.py setzt sie als KAUF ein. Ohne Link erscheint KEIN Knopf; nur die Design-Vorschau zeigt gestrichelte Platzhalter (window.KAUF_DEMO).
  Hinweise: dm/Rossmann-Eigenmarken haben kein Partnerprogramm; Arzneimittel (Ketozolin) ohne Kaufen-Link. Links mit rel="sponsored".
