# Baut die Gesamtseite „Haarpflege einfach erklärt“ aus allen Einzel-Guides.
# 1) node dump.js data.json   2) python3 build-vorschau.py data.json
# Ergebnis: haarpflege.html (Hauptordner, zum lokalen Öffnen, Quiz liegen daneben)
#           notizen/gesamtguide-bau/haarpflege-link.html (für den privaten Link, ohne eigenes Seitengerüst)
import sys, os, re, json
S = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(f'{S}/../..')
_data = json.load(open(sys.argv[1]))
# Wirkung je Produkt nach INCI (notizen/wirkung/classify.py): wt = Schwerpunkte (feucht/naehrend/glaettend),
# wh/we/wg = Stärke Feuchtigkeit/Nährend/Glätte, rk = protein/bond, rp = Bond mit Proteinen
_wk = json.load(open(f'{S}/wirkung.json'))
for _t in ('maske', 'conditioner', 'leavein'):
    for x in _data[_t]['items']:
        e = _wk.get(_t + '|' + x['brand'] + '|' + x['name'])
        assert e, ('Wirkung fehlt', _t, x['brand'], x['name'])
        x['wt'] = e['t']; x['wh'] = e['h']; x['we'] = e['e']; x['wg'] = e['g']
        if e['r']: x['rk'] = e['r']
        if e['p']: x['rp'] = 1
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
# Haarbürsten (buersten.json) und Hitze-Tools (kommt bald, Laura sucht die Empfehlungen noch raus)
_data['buerste'] = json.load(open(f'{S}/buersten.json'))
# Hitze-Tools (hitzetools.json, Bilder in notizen/bilder/hitze-tools/, freigestellt aus den Herstellerbildern)
_ht = json.load(open(f'{S}/hitzetools.json'))
for _i, _p in enumerate(_ht['items']):
    _p['ord'] = _i
    _p['img'] = 'data:image/webp;base64,' + __import__('base64').b64encode(open(f'{S}/../bilder/hitze-tools/' + _p.pop('bild'), 'rb').read()).decode()
_data['tools'] = {'cats': _ht['cats'], 'rank': None, 'items': _ht['items'], 'intro': _ht['intro']}
# Seitenverhältnis jedes Produktbilds (Breite/Höhe), damit Kacheln die Bilder ohne Skript gleich groß zeigen können
import base64 as _b64, io as _io
from PIL import Image as _Img
for _t, _v in _data.items():
    for _x in (_v.get('items') or []) if isinstance(_v, dict) else []:
        _u = _x.get('img') or ''
        if _u.startswith('data:image'):
            try:
                _w, _h = _Img.open(_io.BytesIO(_b64.b64decode(_u.split(',', 1)[1]))).size
                _x['ir'] = round(_w / _h, 3)
            except Exception:
                pass
data = json.dumps(_data, ensure_ascii=False).replace('</', '<\\/')
t = open(f'{S}/vorschau2-template.html').read().replace('__DATA__', data)
# Regal im Wissen-Bereich entfernt (08.10.); Dateien liegen weiter in regal/
t = t.replace('__ROUTINE__', open(f'{S}/routine-zeichnungen.html').read())
t = t.replace('__KAUF__', open(f'{S}/kauflinks.json').read().strip() or '{}')
# Wissenstexte: Übersicht aus wissen.json, Inhalt aus wissen/<id>.html
_w = json.load(open(f'{S}/wissen.json'))
for w in _w: w['html'] = open(f'{S}/wissen/' + w.pop('datei')).read()
# Lauras Fotos in den Kapiteln (wissen-bilder/*.jpg) als data-URI einsetzen
import re as _re
def _wbild(m):
    return 'src="data:image/jpeg;base64,' + _b64.b64encode(open(f'{S}/wissen-bilder/' + m.group(1), 'rb').read()).decode() + '"'
for w in _w: w['html'] = _re.sub(r'src="wbild:([\w.-]+)"', _wbild, w['html'])
t = t.replace('__WISSEN__', json.dumps(_w, ensure_ascii=False).replace('</', '<\\/'))
t = t.replace('__FAQ__', json.dumps(json.load(open(f'{S}/faq.json')), ensure_ascii=False).replace('</', '<\\/'))
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
_fav = json.load(open(f'{S}/favoriten.json'))
for _a in _fav['abschnitte']:  # eigene Bilder für Produkte, die (noch) nicht im Guide sind
    for _x in _a['produkte']:
        if _x.get('hd'): _x['imgHD'] = 'data:image/webp;base64,' + __import__('base64').b64encode(open(f'{S}/../bilder/favoriten/hd/' + _x.pop('hd'), 'rb').read()).decode()  # scharfe Bilder nur für die Favorites
        if _x.get('bild'): _x['img'] = 'data:image/webp;base64,' + __import__('base64').b64encode(open(f'{S}/../bilder/favoriten/' + _x.pop('bild'), 'rb').read()).decode()
if _fav.get('teaserbild'):  # Titelbild für die Favorites-Leiste auf der Startseite (aus ../bilder/favoriten/)
    _tb = _fav['teaserbild']; _mime = 'image/webp' if _tb.endswith('.webp') else ('image/png' if _tb.endswith('.png') else 'image/jpeg')
    _fav['teaserbild'] = f'data:{_mime};base64,' + __import__('base64').b64encode(open(f'{S}/../bilder/favoriten/' + _tb, 'rb').read()).decode()
t = t.replace('__FAV__', json.dumps(_fav, ensure_ascii=False))
t = t.replace('__TEX_SCHAUM__', 'data:image/webp;base64,' + base64.b64encode(open(f'{S}/../bilder/deko/textur-schaum.webp','rb').read()).decode())
t = t.replace('__TEX_MILCH__', 'data:image/webp;base64,' + base64.b64encode(open(f'{S}/../bilder/deko/textur-milch.webp','rb').read()).decode())
t = t.replace('__TEX_SERUM__', 'data:image/webp;base64,' + base64.b64encode(open(f'{S}/../bilder/deko/textur-serum.webp','rb').read()).decode())
t = t.replace('__TEX_CREME__', 'data:image/webp;base64,' + base64.b64encode(open(f'{S}/../bilder/deko/textur-creme.webp','rb').read()).decode())
# Lauras Konsistenz-Fotos (20.10.): weitere Kopfbänder
for _k in ('oel', 'kopf', 'tube', 'glanz', 'maske'):
    t = t.replace('__TEX_' + _k.upper() + '__', 'data:image/webp;base64,' + base64.b64encode(open(f'{S}/../bilder/deko/textur-' + _k + '.webp','rb').read()).decode())
t = t.replace('__FRAG_LAURA__', json.dumps(json.load(open(f'{S}/frag-laura.json', encoding='utf-8')), ensure_ascii=False))
t = t.replace('__ALTERNATIVEN__', json.dumps({k: v for k, v in json.load(open(f'{S}/alternativen.json', encoding='utf-8')).items() if not k.startswith('_')}, ensure_ascii=False))
t = t.replace('__HAARPLAN__', json.dumps({k: v for k, v in json.load(open(f'{S}/haarplan.json', encoding='utf-8')).items() if not k.startswith('_')}, ensure_ascii=False))
t = t.replace('__HAARTYP__', json.dumps({k: v for k, v in json.load(open(f'{S}/haartyp.json', encoding='utf-8')).items() if not k.startswith('_')}, ensure_ascii=False))
t = t.replace('__NEU__', json.dumps(json.load(open(f'{S}/neu.json', encoding='utf-8')), ensure_ascii=False))
t = t.replace('__LL_AUSWAHL__', json.dumps(json.load(open(f'{S}/ll-auswahl.json', encoding='utf-8')), ensure_ascii=False))
for _k, _f in [('__MYTHOS_STAPEL__', 'mythos-stapel.webp')]:  # Bügel-Variante verworfen (16.10.)
    t = t.replace(_k, 'data:image/webp;base64,' + base64.b64encode(open(f'{S}/../bilder/deko/' + _f, 'rb').read()).decode())
t = t.replace('__SILBERTABLETT__', 'data:image/webp;base64,' + base64.b64encode(open(f'{S}/../bilder/deko/silbertablett.webp','rb').read()).decode())
t = t.replace('__ORDNER__', 'data:image/webp;base64,' + base64.b64encode(open(f'{S}/../bilder/deko/ordner-ringe.webp','rb').read()).decode())
# Stoff-Patch im Wissen auf Lauras Wunsch wieder entfernt (16.10.), Bild liegt weiter in bilder/deko
# t = t.replace('__STOFFPATCH__', 'data:image/webp;base64,' + base64.b64encode(open(f'{S}/../bilder/deko/stoffpatch-quer.webp','rb').read()).decode())
# LL-Methode: Lauras Schritt-Fotos (Schritt 3 folgt)
for _n in (1, 2):
    t = t.replace('__LL_SCHRITT%d__' % _n, 'data:image/jpeg;base64,' + base64.b64encode(open(f'{S}/../bilder/deko/ll-schritt%d.jpg' % _n,'rb').read()).decode())
# Schnitt-Animation auf der Startseite (Lauras Scheren-Fotos, freigestellt)
for _k in ('offen', 'zu'):
    t = t.replace('__SCHERE_' + _k.upper() + '__', 'data:image/webp;base64,' + base64.b64encode(open(f'{S}/../bilder/deko/schere-' + _k + '.webp','rb').read()).decode())
t = t.replace('__STECKNADEL__', 'data:image/webp;base64,' + base64.b64encode(open(f'{S}/../bilder/deko/stecknadel.webp','rb').read()).decode())
t = t.replace('__LAURA_FOTO__', 'data:image/jpeg;base64,' + base64.b64encode(open(f'{S}/laura-startseite-web.jpg','rb').read()).decode())
t = t.replace('__QUIZ_HAAR__', 'quiz-haar.html').replace('__QUIZ_PFLEGE__', 'quiz-pflege.html').replace('__QUIZ_KOPF__', 'quiz-kopfhaut.html').replace('__QUIZ_ROUTINE__', 'quiz-routine.html').replace('__QUIZ_TOOLS__', 'quiz-tools.html').replace('__QUIZ_SCHNITT__', 'quiz-schnitt.html').replace('__QUIZ_SPLISS__', 'quiz-spliss.html').replace('__QUIZ_LEAVEIN__', 'quiz-leavein.html').replace('__QUIZ_KOPFPFLEGE__', 'quiz-kopfpflege.html').replace('__QUIZ_AUSFALL__', 'quiz-ausfall.html')
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
q = {f: open(f'{ROOT}/{f}').read() for f in ('quiz-kopfhaut.html', 'quiz-pflege.html', 'quiz-haar.html', 'quiz-routine.html', 'quiz-tools.html', 'quiz-schnitt.html', 'quiz-spliss.html', 'quiz-leavein.html', 'quiz-kopfpflege.html', 'quiz-ausfall.html')}
emb = open(f'{S}/quiz-einbettung.html').read().replace('__QUIZ_JSON__', json.dumps(q, ensure_ascii=False).replace('</', '<\\/'))
for fn in ('haarpflege-link.html', 'design-vorschau-link.html'):
    x = open(f'{S}/{fn}').read().rstrip('\n') + '\n' + emb
    open(f'{S}/{fn}', 'w').write(x)
print('ok', len(t)//1024, 'KB')
