import sys, os, re, json, io, base64
from PIL import Image
S = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, S)
import importlib, data
importlib.reload(data)
P = data.P

# INCI für die Silikon-Erkennung: dm aus dm.json, Screenshots aus den Notizen
inci = {}
for k, v in json.load(open(f'{S}/dm.json')).items():
    inci[k] = v['groups'].get('Inhaltsstoffe', '').replace(' • ', ', ')
notes = open('/home/user/Haar-Quiz/notizen/oel-liste.md').read()
for m in re.finditer(r'#### \[(o\d+)\][^\n]*\n([^\n#]*)', notes):
    inci[m.group(1)] = m.group(2)
missing = [k for k in P if not inci.get(k)]
assert not missing, missing
def silikone(k):
    out = []
    for part in re.split(r'[,•|·]', inci[k]):
        p = re.sub(r'(?i)^\s*ingredients:\s*', '', part.strip())
        if re.search(r'(?i)methicon|siloxan|silicone', p):
            name = re.sub(r'\s*\(.*?\)', '', p).strip().title().replace('-Di', '-di')
            name = re.sub(r'(?i)\b(peg|ppg)\b', lambda m: m.group(1).upper(), name)
            if name and name not in out: out.append(name)
    return out

tpl = open('/home/user/Haar-Quiz/masken-guide.html').read()
def between(t, a, b):
    i = t.index(a) + len(a); j = t.index(b, i); return i, j
keyname = lambda k: P[k][0] + '|' + P[k][1]
order = sorted(P, key=lambda k: (P[k][0] + P[k][1]).lower())
rows = ',\n'.join(' ' + json.dumps(list(P[k]), ensure_ascii=False) for k in order)
t = tpl
i, j = between(t, 'const P = [\n', '\n].map(([brand,name,c,note,zustand,tip,segment])')
t = t[:i] + rows + t[j:]
a = '].map(([brand,name,c,note,zustand,tip,segment]) => ({segment, brand, name, cats:c.split(" "), note, hair:["",zustand], tip}));'
assert a in t
t = t.replace(a, '].map(([brand,name,c,note,zustand,tip,segment,dry]) => ({segment, brand, name, cats:c.split(" "), note, hair:["",zustand], tip, dry}));')
t = t.replace('/* [Marke, Produkt, Kategorien, Einschätzung, Haarzustand, Gut zu wissen, Segment] */', '/* [Marke, Produkt, Kategorien, Einschätzung, Haarzustand, Gut zu wissen, Segment, trockenes Öl] */')

def setobj(t, name, obj):
    m = re.search(r'const ' + name + r' = (\{.*?\});\n', t, re.S)
    return t[:m.start(1)] + json.dumps(obj, ensure_ascii=False) + t[m.end(1):]
t = setobj(t, 'REP', {})
t = setobj(t, 'SIL', {keyname(k): silikone(k) for k in P})
imgs = {}
for k in P:
    f = f'{S}/cut/{k}.png'
    im = Image.open(f).convert('RGBA')
    im = im.crop(im.getchannel('A').point(lambda v: 255 if v > 8 else 0).getbbox()); im.thumbnail((180, 180), Image.LANCZOS)
    b = io.BytesIO(); im.save(b, 'WEBP', quality=85, method=6)
    imgs[keyname(k)] = 'data:image/webp;base64,' + base64.b64encode(b.getvalue()).decode()
t = setobj(t, 'IMG', imgs)

CATS = '''const CATS = [
 {id:"fein", label:"Feines Haar", desc:"Für Feenhaar: Das einzelne Haar ist hauchdünn und fällt sofort platt. Hier stehen nur echte trockene Öle. Sie verdunsten zum größten Teil und hinterlassen nur einen hauchdünnen Pflegefilm, ohne schweres Silikon-Serum. Ein Pumpstoß oder ein paar Tropfen nur in die Spitzen."},
 {id:"duenn", label:"Dünnes Haar", desc:"Du hast eher wenige Haare und wenig Fülle, das einzelne Haar ist aber nicht besonders fein. Trockene Öle und leichte Öl-Seren, die Glanz geben und pflegen, ohne dir die Fülle zu nehmen. Sparsam dosieren und nicht an den Ansatz geben."},
 {id:"normal", label:"Normales Haar", desc:"Die solide Mitte. Hier darfst du nach deinem Haarzustand auswählen, zum Beispiel nach mehr Glanz, weniger Frizz oder mehr Pflege für trockene Spitzen."},
 {id:"dick", label:"Dickes Haar", desc:"Kräftiges Haar, das Pflege gut verträgt. Klassische Silikon-Seren und Öle mit mehr Pflanzenöl machen es geschmeidig und bändigen Frizz, ohne dass es platt wirkt."},
 {id:"sehrdick", label:"Sehr dickes Haar", desc:"Sehr kräftiges Haar, oft auch trocken, lockig oder kraus. Hier stehen die reichhaltigsten Öle: glättende Seren mit viel Silikon und reine Pflanzenöle. Feineres Haar fällt damit schnell platt."}
];'''
t = re.sub(r'const CATS = \[.*?\n\];', lambda m: CATS, t, count=1, flags=re.S)

# Merkmal „Trockenes Öl“ als Pille neben Drogerie/High-End, und in der Suche
a = '<span class="tags"><span class="tag">${p.segment}</span></span>'
assert a in t
t = t.replace(a, '<span class="tags"><span class="tag">${p.segment}</span>${p.dry?`<span class="heat">Trockenes Öl</span>`:""}</span>')
a = 'p.sil.length?"silikone "'
assert a in t
t = t.replace(a, '(p.dry?"trockenes öl dry oil ":"")+(p.sil.length?"silikone "', 1)
# Klammer schließen: das Original ist ...p.sil.length?"silikone "+p.sil.join(" "):"silikonfrei",...
m = re.search(r'\(p\.dry\?"trockenes öl dry oil ":""\)\+\(p\.sil\.length\?"silikone "\+p\.sil\.join\(" "\):"silikonfrei"', t)
assert m, 'Suche'
t = t[:m.end()] + ')' + t[m.end():]

rep = [
 ('<title>Dein Haarmasken-Guide</title>', '<title>Dein Haaröl-Guide</title>'),
 ('<h1>Dein Haarmasken-Guide</h1>', '<h1>Dein Haaröl-Guide</h1>'),
 ('Dazu habe ich gerade keine Haarmaske in der Liste.', 'Dazu habe ich gerade kein Haaröl in der Liste.'),
 ('"Alle Haarmasken" : (seg==="Drogerie" ? "Alle Drogerie-Haarmasken" : "Alle High-End-Haarmasken")', '"Alle Haaröle" : (seg==="Drogerie" ? "Alle Drogerie-Haaröle" : "Alle High-End-Haaröle")'),
 ('Fang bei feinem Haar mit wenig Produkt an, gib die Maske nicht an den Ansatz und spül sie gründlich aus.', 'Fang bei feinem Haar mit wenig Produkt an und gib das Öl nicht an den Ansatz.'),
]
for a, b in rep:
    assert a in t, a; t = t.replace(a, b)
i, j = between(t, '<p class="lead">', '</div>\n  </div>')
t = t[:i] + '''Ein Haaröl ist der letzte Schritt deiner Pflege. Es legt sich wie ein Schutzfilm um die Längen und Spitzen, macht sie geschmeidig und glänzend und bändigt Frizz. So reiben deine Haare weniger aneinander und brechen seltener ab. Dein Öl wählst du nach deiner Haardicke: Je feiner dein Haar, desto leichter sollte das Öl sein.</p>
    <div class="box">
      <p><b>Was ist ein trockenes Öl?</b> Es besteht vor allem aus leichten Stoffen, die nach dem Auftragen verdunsten. Zurück bleibt nur ein hauchdünner Film. Deshalb fettet es kaum und passt auch zu feinem Haar. Du erkennst es an der Markierung „Trockenes Öl“. Nicht jedes leichte Öl ist ein trockenes Öl: Klassische Silikon-Seren glätten stark und geben viel Glanz, legen sich aber als dickerer Film um das Haar und beschweren feines Haar schnell.</p>
      <p><b>Gut zu wissen:</b> Kein Öl repariert Spliss. Ist die Haarspitze einmal gespalten, wächst sie nicht wieder zusammen. Ein Öl kann Spliss nur vorbeugen und kurz kaschieren. Weg geht er nur, wenn man ihn abschneidet.</p>
      <p><b>So verwendest du es:</b> Ein bis drei Pumpstöße in den Handflächen verreiben und in Längen und Spitzen geben, nicht an den Ansatz. Entweder ins handtuchtrockene Haar vor dem Föhnen oder ins trockene Haar gegen Frizz und für Glanz. Bei feinem Haar mit einem Tropfen anfangen.</p>
    ''' + t[j:]
open('/home/user/Haar-Quiz/oel-guide.html', 'w').write(t)
print('ok', len(P), 'Öle,', len(imgs), 'Bilder')
print({k: silikone(k) for k in ['o22','d10','d16','o20','o06','d17']})
