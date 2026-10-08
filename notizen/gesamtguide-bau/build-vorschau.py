# Baut die Gesamtseite „Haarpflege einfach erklärt“ aus allen Einzel-Guides.
# 1) node dump.js data.json   2) python3 build-vorschau.py data.json
# Ergebnis: haarpflege.html (Hauptordner, zum lokalen Öffnen, Quiz liegen daneben)
#           notizen/gesamtguide-bau/haarpflege-link.html (für den privaten Link, ohne eigenes Seitengerüst)
import sys, os, re, json
S = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(f'{S}/../..')
_data = json.load(open(sys.argv[1]))
# Produktkategorie Hitzeschutz: Leave-ins und Öle mit Hitzeschutz, sortiert nach Konsistenz (hitzeschutz.json)
_h = json.load(open(f'{S}/hitzeschutz.json'))
_hitems = []
for e in _h['produkte']:
    src = [x for x in _data[e['quelle']]['items'] if x['brand'] == e['brand'] and x['name'] == e['name']]
    assert len(src) == 1, ('Hitzeschutz: Produkt nicht gefunden', e)
    x = dict(src[0])
    dk = [c for c in x['cats'] if c in ('fein', 'duenn', 'normal', 'dick', 'sehrdick')]
    if e['form'] == 'oel': dk = [c for c in dk if c not in ('fein', 'duenn')] or dk  # Öle erst ab normaler Haardicke
    x['dk'] = dk; x['cats'] = [e['form']]; x['von'] = e['quelle']
    m = re.search(r'bis (\d{3})\s*°', (x.get('note', '') + ' ' + x.get('tip', '')).replace('\xa0', ' '))
    if e.get('heat') or m: x['heat'] = e.get('heat') or m.group(1)
    _hitems.append(x)
_hitems += _h.get('eigene', [])
_data['hitze'] = {'cats': _h['cats'], 'rank': None, 'items': _hitems, 'intro': {
  'lead': 'Deinen Hitzeschutz suchst du nach deiner Haardicke aus und danach, ob du ihn ins feuchte oder ins trockene Haar gibst. Er legt sich wie ein Schutzfilm um deine Haare, damit Föhn, Glätteisen und Lockenstab weniger Schaden anrichten.',
  'how': '',
  'box': '<p><b>So wendest du ihn an:</b> Vor jeder Hitze, egal ob Föhn, Glätteisen oder Lockenstab. Meine Empfehlung: das Tool nicht heißer einstellen als nötig und danach eine Leave-in-Pflege oder ein Öl.</p>'}}
data = json.dumps(_data, ensure_ascii=False).replace('</', '<\\/')
t = open(f'{S}/vorschau2-template.html').read().replace('__DATA__', data)
# Vintage-Regal im Wissen-Bereich (Teile aus notizen/bilder/regal/variante-1.png, zugeschnitten in regal/)
for _k, _f in (('FACH','fach'),):
    t = t.replace(f'__REGAL_{_k}__', 'data:image/webp;base64,' + __import__('base64').b64encode(open(f'{S}/regal/{_f}.webp','rb').read()).decode())
t = t.replace('__ROUTINE__', open(f'{S}/routine-zeichnungen.html').read())
t = t.replace('__KAUF__', open(f'{S}/kauflinks.json').read().strip() or '{}')
# Wissenstexte: Übersicht aus wissen.json, Inhalt aus wissen/<id>.html
_w = json.load(open(f'{S}/wissen.json'))
for w in _w: w['html'] = open(f'{S}/wissen/' + w.pop('datei')).read()
t = t.replace('__WISSEN__', json.dumps(_w, ensure_ascii=False).replace('</', '<\\/'))
# Serie „Haarpflege 1x1“: Titelbilder als eingebettete Bilder
_serie = json.load(open(f'{S}/serie.json'))
for r in _serie:
    if r.get('bild'): r['bild'] = 'data:image/jpeg;base64,' + __import__('base64').b64encode(open(f'{S}/serie/' + r['bild'], 'rb').read()).decode()
t = t.replace('__SERIE__', json.dumps(_serie, ensure_ascii=False))
# Hair Journey: angepinnte Beiträge auf Instagram und TikTok, Cover = hair-journey-cover.jpg
JOURNEY_IG = 'https://www.instagram.com/p/DVS6Ig9jeKW/'
JOURNEY_TT = 'https://www.tiktok.com/@lauraspiessmacher/photo/7612557590056422659'
cov = f'{S}/hair-journey-cover.jpg'
t = t.replace('__JOURNEY_IG__', JOURNEY_IG).replace('__JOURNEY_TT__', JOURNEY_TT)
import base64, glob
def _b64(fn): return 'data:image/jpeg;base64,' + base64.b64encode(open(fn,'rb').read()).decode()
# Hair Journey als Buch: Cover = Collage, darunter Papierseiten, die beim Hinscrollen/Drüberfahren kurz aufblättern
_book = '<span class="bstack" aria-hidden="true"></span>' + ''.join(f'<span class="bleaf" style="--i:{i}" aria-hidden="true"></span>' for i in range(1, 7)) + f'<span class="bcover"><img src="{_b64(cov)}" alt=""></span>'
t = t.replace('<div class="jcover" aria-label="Platz für das Cover deiner Hair Journey">__JOURNEY_COVER__</div>',
  ('<a class="jcover book" id="jbook" href="' + JOURNEY_IG + '" target="_blank" rel="noopener" aria-label="My Hair Journey: Collage meiner Haare von früher bis heute, auf Instagram ansehen">' + _book + '</a>') if os.path.exists(cov)
  else '<div class="jcover">Hier kommt das Cover deiner Hair Journey hin</div>')
import base64
t = t.replace('__LAURA_FOTO__', 'data:image/jpeg;base64,' + base64.b64encode(open(f'{S}/laura-startseite-web.jpg','rb').read()).decode())
t = t.replace('__QUIZ_HAAR__', 'quiz-haar.html').replace('__QUIZ_PFLEGE__', 'quiz-pflege.html').replace('__QUIZ_KOPF__', 'quiz-kopfhaut.html').replace('__QUIZ_ROUTINE__', 'quiz-routine.html')
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
d = t.replace('<!--DESIGN-->', open(f'{S}/design-varianten.html').read().replace('/*FONTS*/', open(f'{S}/schriften-eingebettet.css').read())).replace('<!--DESIGN-SWITCH-->', open(f'{S}/design-umschalter.html').read())
d = d.replace('<title>Haarpflege einfach erklärt</title>', '<title>Haarpflege Designvarianten</title>')
d = re.sub(r'^<!DOCTYPE html>\s*<html[^>]*>\s*<head>\s*', '', d)
d = re.sub(r'<meta charset="utf-8">\s*<meta name="viewport"[^>]*>\s*', '', d)
d = d.replace('</head>\n<body>\n', '\n', 1)
d = re.sub(r'</body>\s*</html>\s*$', '\n', d)
open(f'{S}/design-vorschau-link.html', 'w').write(d)
# Quizze direkt einbetten (in den privaten Links laufen eigene Unterseiten nicht zuverlässig)
q = {f: open(f'{ROOT}/{f}').read() for f in ('quiz-kopfhaut.html', 'quiz-pflege.html', 'quiz-haar.html', 'quiz-routine.html')}
emb = open(f'{S}/quiz-einbettung.html').read().replace('__QUIZ_JSON__', json.dumps(q, ensure_ascii=False).replace('</', '<\\/'))
for fn in ('haarpflege-link.html', 'design-vorschau-link.html'):
    x = open(f'{S}/{fn}').read().rstrip('\n') + '\n' + emb
    open(f'{S}/{fn}', 'w').write(x)
print('ok', len(t)//1024, 'KB')
