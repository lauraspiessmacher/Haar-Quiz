# Geparkt (aus der Seite genommen, aber aufbewahrt)

## Leave-in-Klecks / Konsistenz-Patch auf der Startseite (geparkt 23.10.)
Laura: „mach bitte den Konsistenz-Patch auf der Startseite weg und speicher ihn, bis ich eine andere Stelle gefunden habe“.
- Bild: `notizen/bilder/deko/leavein-klecks.webp` (Platzhalter `__KLECKS__` in build-vorschau.py bleibt bestehen)
- CSS bleibt im Template (`.journey .klecks`, `.klecks-anker`, `.klecks-handy`)
- Zum Zurückholen diese zwei Zeilen wieder einsetzen:
  - in `<div class="journey">` direkt als erstes Kind (anstelle des Kommentars „Leave-in-Klecks geparkt“):
    `<img class="klecks" src="__KLECKS__" alt="" aria-hidden="true">`
  - direkt nach `<div class="fdm" id="fdm"></div>` (Handy-Version):
    `<div class="klecks-anker" aria-hidden="true"><img class="klecks-handy" src="__KLECKS__" alt=""></div>`
- Letzte Position: Desktop rechts oben an der Hair-Journey-Box (right 39px, top −141px, 176px breit, bei 760–1139px ausgeblendet); Handy am „Frage des Monats“-Kasten (right −6px, bottom −62px, 88px).
