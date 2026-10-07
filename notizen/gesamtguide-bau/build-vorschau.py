# Baut die Gesamtseite „Haarpflege einfach erklärt“ aus allen Einzel-Guides.
# 1) node dump.js data.json   2) python3 build-vorschau.py data.json
# Ergebnis: haarpflege.html (Hauptordner, zum lokalen Öffnen, Quiz liegen daneben)
#           notizen/gesamtguide-bau/haarpflege-link.html (für den privaten Link, ohne eigenes Seitengerüst)
import sys, os, re
S = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(f'{S}/../..')
data = open(sys.argv[1]).read().replace('</', '<\\/')
t = open(f'{S}/vorschau2-template.html').read().replace('__DATA__', data)
t = t.replace('__QUIZ_HAAR__', 'quiz-haar.html').replace('__QUIZ_PFLEGE__', 'quiz-pflege.html').replace('__QUIZ_KOPF__', 'quiz-kopfhaut.html')
t = t.replace('<p class="note-banner">Vorschau mit allen echten Produkten aus deinen 6 Guides. Quiz und Wissen sind noch Platzhalter.</p>',
              '<p class="note-banner">Wissen ist noch ein Platzhalter. Die Wissenstexte kommen später.</p>')
open(f'{ROOT}/haarpflege.html', 'w').write(t)
a = re.sub(r'^<!DOCTYPE html>\s*<html[^>]*>\s*<head>\s*', '', t)
a = re.sub(r'<meta charset="utf-8">\s*<meta name="viewport"[^>]*>\s*', '', a)
a = a.replace('</head>\n<body>\n', '\n', 1)
a = re.sub(r'</body>\s*</html>\s*$', '\n', a)
assert a.lstrip().startswith('<title>'), a[:80]
open(f'{S}/haarpflege-link.html', 'w').write(a)
# Design-Vorschau mit Umschalter (eigener Link, die offizielle Seite bleibt unverändert)
d = t.replace('<!--DESIGN-->', open(f'{S}/design-varianten.html').read()).replace('<!--DESIGN-SWITCH-->', open(f'{S}/design-umschalter.html').read())
d = d.replace('<title>Haarpflege einfach erklärt</title>', '<title>Haarpflege Designvarianten</title>')
d = re.sub(r'^<!DOCTYPE html>\s*<html[^>]*>\s*<head>\s*', '', d)
d = re.sub(r'<meta charset="utf-8">\s*<meta name="viewport"[^>]*>\s*', '', d)
d = d.replace('</head>\n<body>\n', '\n', 1)
d = re.sub(r'</body>\s*</html>\s*$', '\n', d)
open(f'{S}/design-vorschau-link.html', 'w').write(d)
print('ok', len(t)//1024, 'KB')
