import sys, os, re, json, io, base64
from PIL import Image
S = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, S)
import importlib, data
importlib.reload(data)
P, REP = data.P, data.REP

# INCI für die Silikon-Erkennung: dm aus dm.json, Rossmann aus den Notizen
inci = {}
dm = json.load(open(f'{S}/dm.json'))
for k, v in dm.items():
    inci[k] = v['groups'].get('Inhaltsstoffe', '')
notes = open('/home/user/Haar-Quiz/notizen/conditioner-liste.md').read()
for m in re.finditer(r'#### \[([rho]\d+)\][^\n]*\n([^\n#]*)', notes):
    inci[m.group(1)] = m.group(2)
SILRE = re.compile(r'(?i)\b([A-Za-z\-/ ]*?(?:methicone|methiconol|siloxane|silicone quaternium-\d+))\b')
EXTRA = {'h1': ['Quaternium-80']}  # Silikon-Quat, fällt nicht unter die Regex
def silikone(k):
    out = list(EXTRA.get(k, []))
    for part in re.split(r'[,•|·]', inci.get(k, '')):
        p = part.strip()
        if re.search(r'(?i)methicon|siloxan|silicone quaternium', p):
            name = re.sub(r'\s*\(.*?\)', '', p).strip().title().replace('-Di', '-di')
            name = re.sub(r'(?i)^silicone quaternium', 'Silicone Quaternium', name)
            name = re.sub(r'(?i)\b(peg|ppg)\b', lambda m: m.group(1).upper(), name)
            if name and name not in out: out.append(name)
    return out

tpl = open('/home/user/Haar-Quiz/masken-guide.html').read()
def between(t, a, b):
    i = t.index(a) + len(a); j = t.index(b, i); return i, j

keyname = lambda k: P[k][0] + '|' + P[k][1]
rows = ',\n'.join(' ' + json.dumps(list(P[k][:7]), ensure_ascii=False) for k in P)
t = tpl
i, j = between(t, 'const P = [\n', '\n].map(([brand,name,c,note,zustand,tip,segment])')
t = t[:i] + rows + t[j:]

def setobj(t, name, obj):
    m = re.search(r'const ' + name + r' = (\{.*?\});\n', t, re.S)
    return t[:m.start(1)] + json.dumps(obj, ensure_ascii=False) + t[m.end(1):]
t = setobj(t, 'REP', {keyname(k): {"art": a, "list": l} for k, (a, l) in REP.items()})
t = setobj(t, 'SIL', {keyname(k): silikone(k) for k in P})
imgs = {}
for k in P:
    f = f'{S}/cut/{k}.png'
    if not os.path.exists(f): continue
    im = Image.open(f).convert('RGBA')
    im = im.crop(im.getchannel('A').point(lambda v: 255 if v > 8 else 0).getbbox()); im.thumbnail((180, 180), Image.LANCZOS)
    b = io.BytesIO(); im.save(b, 'WEBP', quality=85, method=6)
    imgs[keyname(k)] = 'data:image/webp;base64,' + base64.b64encode(b.getvalue()).decode()
t = setobj(t, 'IMG', imgs)

CATS = '''const CATS = [
 {id:"fein", label:"Feines Haar", desc:"Für Feenhaar: Das einzelne Haar ist hauchdünn und fällt sofort platt. Hier stehen nur die leichtesten Conditioner, ohne schwere Öle und Butter. Nur in Längen und Spitzen geben und gründlich ausspülen."},
 {id:"duenn", label:"Dünnes Haar", desc:"Du hast eher wenige Haare und wenig Fülle, das einzelne Haar ist aber nicht besonders fein. Leichte Conditioner, die pflegen, ohne dir die Fülle zu nehmen. Nicht an den Ansatz geben."},
 {id:"normal", label:"Normales Haar", desc:"Die solide Mitte. Hier darfst du nach deinem Haarzustand auswählen, zum Beispiel nach mehr Glanz, weniger Frizz oder mehr Pflege für trockenes oder strapaziertes Haar."},
 {id:"dick", label:"Dickes Haar", desc:"Kräftiges Haar, das viel Pflege verträgt. Conditioner mit Silikon, Ölen, Butter oder Fettalkoholen machen es weich und geschmeidig, ohne dass es platt wirkt."},
 {id:"sehrdick", label:"Sehr dickes Haar", desc:"Sehr kräftiges Haar, oft auch trocken, lockig oder kraus. Hier stehen die reichhaltigsten Conditioner mit viel Butter, Öl oder Silikon. Feineres Haar fällt damit schnell platt."},
 {id:"kaputt", label:"Kaputte Haare", desc:"Hier stehen nur Conditioner mit einem echten Repair-Effekt: Bond-Wirkstoffe, Keratin, Proteine oder Peptide stehen vor Parfum und Konservierer und weit genug vorne in der Liste. Proteine legen sich von außen an beschädigte Stellen an und machen das Haar widerstandsfähiger, Bond-Wirkstoffe stabilisieren es von innen. Ein Conditioner wirkt nur kurz ein. Für mehr Aufbau zusätzlich eine Repair-Maske."}
];'''
t = re.sub(r'const CATS = \[.*?\n\];', lambda m: CATS, t, count=1, flags=re.S)

rep = [
 ('<title>Dein Haarmasken-Guide</title>', '<title>Dein Conditioner-Guide</title>'),
 ('<h1>Dein Haarmasken-Guide</h1>', '<h1>Dein Conditioner-Guide</h1>'),
 ('Dazu habe ich gerade keine Haarmaske in der Liste.', 'Dazu habe ich gerade keinen Conditioner in der Liste.'),
 ('"Alle Haarmasken" : (seg==="Drogerie" ? "Alle Drogerie-Haarmasken" : "Alle High-End-Haarmasken")', '"Alle Conditioner" : (seg==="Drogerie" ? "Alle Drogerie-Conditioner" : "Alle High-End-Conditioner")'),
 ('Fang bei feinem Haar mit wenig Produkt an, gib die Maske nicht an den Ansatz und spül sie gründlich aus.', 'Fang bei feinem Haar mit wenig Produkt an, gib den Conditioner nicht an den Ansatz und spül ihn gründlich aus.'),
]
for a, b in rep:
    assert a in t, a; t = t.replace(a, b)
i, j = between(t, '<p class="lead">', '</div>\n  </div>')
t = t[:i] + '''Ein Conditioner ist der Pflegeschritt nach jeder Haarwäsche. Er glättet die Oberfläche, macht deine Haare geschmeidig und leichter kämmbar. So brechen sie beim Bürsten und Föhnen seltener ab. Deinen Conditioner wählst du nach deiner Haardicke und deinem Haarzustand, denn beides entscheidet, ob er pflegt oder beschwert.</p>
    <div class="box">
      <p><b>Gut zu wissen:</b> Kein Conditioner repariert Spliss. Ist die Haarspitze einmal gespalten, wächst sie nicht wieder zusammen. Ein Conditioner kann Spliss nur vorbeugen und kurz kaschieren. Weg geht er nur, wenn man ihn abschneidet.</p>
      <p><b>So verwendest du ihn:</b> Nach jedem Shampoo in Längen und Spitzen geben, kurz einwirken lassen und gründlich ausspülen. Ein- bis zweimal pro Woche kannst du stattdessen eine Maske nehmen. Danach am besten noch ein Leave-in. Und wenn es mal schnell gehen muss: Lieber ein Conditioner als gar keine Pflege.</p>
    ''' + t[j:]
open('/home/user/Haar-Quiz/conditioner-guide.html', 'w').write(t)
print('ok', len(P), 'Produkte,', len(imgs), 'Bilder; ohne Bild:', [k for k in P if keyname(k) not in imgs])
print('Silikone Beispiele:', {k: silikone(k) for k in ['c01','r13','o1','h1','h2','h3','h9']})
