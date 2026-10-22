# Zerlegt Lauras zwei Umschlag-Fotos (zu/offen) in Ebenen für die Brief-Animation.
# Aufruf: python3 notizen/brief/umschlag.py ZU.jpg OFFEN.jpg  -> notizen/brief/umschlag/*.webp + Maße
import sys, json, numpy as np, cv2
from PIL import Image, ImageDraw
from scipy import ndimage as nd
ZU, OF = [np.asarray(Image.open(f).convert('RGB')).astype(float) for f in sys.argv[1:3]]
H, W = ZU.shape[:2]
X0, Y0, CW, CH = 150, 60, 900, 1440          # Ausschnitt (Hand reicht bis unten)
S = 0.6                                       # Exportgröße
OUT = 'notizen/brief/umschlag/'
BG = np.array([230., 230., 230.])
L = OF.mean(2)

def poly(pts):
    m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).polygon(pts, fill=255); return np.asarray(m) > 0

# Karte im offenen Foto: hell, im Kartenbereich zusammenhängend
box = np.zeros((H, W), bool); box[268:712, 345:892] = True
hell = (L > 222) & box
lab, n = nd.label(hell); keep = lab == lab[400, 600]
karte_sicht = nd.binary_closing(keep, iterations=3)
cols = range(345, 892)
unten = {x: (np.where(karte_sicht[:, x])[0].max() if karte_sicht[:, x].any() else 395) for x in cols}

# Kartenform (ganz): leicht schräge Oberkante wie im Foto
KX0, KX1, KY0, KY1 = 352, 886, 272, 800
kform = poly([(KX0, 273), (KX1, 281), (KX1, KY1), (KX0, KY1)])
# Papierstruktur aus dem sichtbaren Teil kacheln
tile = OF[292:372, 372:866]
pap = np.zeros_like(OF)
for y in range(KY0, KY1 + 1):
    pap[y, 372:866] = tile[(y - 292) % 80]
pap[:, KX0:372] = pap[:, 372:392][:, ::-1][:, :372 - KX0]; pap[:, 866:KX1 + 1] = pap[:, 845:866][:, ::-1][:, :KX1 + 1 - 866]
k = pap.copy()                                  # Karte ganz aus Papierstruktur, ohne Fransen aus dem Foto
# sanfter Verlauf nach unten (Papier liegt im Umschlag etwas im Schatten)
yy = np.arange(H)[:, None, None]; k = k * (1 - np.clip((yy - 520) / 900, 0, .12))
karte = np.dstack([k, kform * 255])

# Hinten: offenes Foto, Karte und Klappe entfernt
klappe_auf = poly([(605, 108), (972, 414), (238, 414)])
hint = OF.copy()
loch = nd.binary_dilation(kform | karte_sicht, iterations=3)
innen = np.roll(ZU, -60, axis=0) * 0.72                               # Spitze aus dem geschlossenen Foto als Innenseite, etwas dunkler
hint = np.where((loch & (np.arange(H)[:, None] >= 395))[..., None], innen, hint)
oben = np.arange(H)[:, None] < 395
hint = np.where(oben[..., None], BG + np.random.default_rng(1).normal(0, 1.2, OF.shape), hint)   # oberhalb des Knicks nur Hintergrund (Klappe ist eigene Ebene)

# Klappe (offen): Spitze aus dem Foto, hinter der Karte mit Spitze aus dem geschlossenen Foto aufgefüllt
kl_auf_rgb = np.where(loch[..., None], np.roll(ZU, -260, axis=0) * 0.95, OF)
kl_auf_a = (klappe_auf & oben)

# Vorne: Tasche vor der Karte (alle Kartenspalten unterhalb der sichtbaren Kartenkante) + Hand
vorne_a = np.zeros((H, W))
for x in cols:
    b = unten[x]
    vorne_a[b + 1:, x] = 1
    band = slice(max(b - 16, 0), b + 1)
    vorne_a[band, x] = np.clip((150 - L[band, x]) / 110, 0, 1)   # Wimpern-Fransen der Spitze bleiben vorne
vorne_a[:, :345] = 0; vorne_a[:, 892:] = 0
vorne_a[:395, :362] = 0; vorne_a[:395, 876:] = 0      # Randspalten: über dem Knick nichts

# Klappe (zu) aus dem geschlossenen Foto
kl_zu_a = poly([(256, 396), (966, 396), (622, 772)])

def save(name, rgb, a=None, bbox=True):
    rgb = rgb[Y0:Y0 + CH, X0:X0 + CW]
    if a is None:
        im = Image.fromarray(np.clip(rgb, 0, 255).astype('uint8'), 'RGB'); bb = (0, 0, CW, CH)
    else:
        a = (np.clip(a, 0, 1) * 255 if a.dtype != bool else a * 255)[Y0:Y0 + CH, X0:X0 + CW]
        a = cv2.GaussianBlur(a.astype(np.float32), (0, 0), 0.7)
        im = Image.fromarray(np.dstack([np.clip(rgb, 0, 255), a]).astype('uint8'), 'RGBA')
        bb = im.getchannel('A').point(lambda v: 255 if v > 6 else 0).getbbox() if bbox else (0, 0, CW, CH)
        im = im.crop(bb)
    im = im.resize((round(im.width * S), round(im.height * S)), Image.LANCZOS)
    im.save(OUT + name + '.webp', 'WEBP', quality=80)
    return {'l': bb[0] / CW * 100, 't': bb[1] / CH * 100, 'w': (bb[2] - bb[0]) / CW * 100, 'h': (bb[3] - bb[1]) / CH * 100}

m = {}
m['zu'] = save('zu', ZU)
m['hinten'] = save('hinten', hint)
m['klappezu'] = save('klappe-zu', ZU, kl_zu_a)
m['klappeauf'] = save('klappe-auf', kl_auf_rgb, kl_auf_a)
m['vorne'] = save('vorne', OF, vorne_a)
m['karte'] = save('karte', karte[..., :3], karte[..., 3] / 255)
m['scharnier_y'] = (396 - Y0) / CH * 100          # Knick der Klappe
m['kartenhoehe_px'] = KY1 - 272
json.dump({k: v for k, v in m.items() if isinstance(v, dict)}, open(OUT + 'masse.json', 'w'), indent=1)
print(json.dumps({k: (({kk: round(vv, 3) for kk, vv in v.items()}) if isinstance(v, dict) else round(v, 3)) for k, v in m.items()}))
