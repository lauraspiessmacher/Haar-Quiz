# Offener Spitzen-Umschlag (Lauras Foto) freigestellt für braunen Hintergrund: Ebenen hinten / Karte / vordere Tasche.
# Aufruf: python3 notizen/brief/umschlag_offen.py OFFEN.jpg MASKE.png   (MASKE: rembg isnet-general-use, only_mask)
import sys, json, numpy as np, cv2
from PIL import Image, ImageDraw
from scipy import ndimage as nd
OF = np.asarray(Image.open(sys.argv[1]).convert('RGB')).astype(float)
ISN = np.asarray(Image.open(sys.argv[2]).convert('L')).astype(float) / 255
H, W = OF.shape[:2]; L = OF.mean(2)
X0, Y0, CW, CH, S = 150, 60, 900, 1440, 0.6
OUT = 'notizen/brief/umschlag/'
def poly(pts):
    m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).polygon(pts, fill=255); return np.asarray(m) > 0
yy = np.arange(H)[:, None]

klappe = poly([(605, 108), (972, 414), (238, 414)]) & (yy < 395)
koerper = poly([(247, 395), (970, 395), (970, 1016), (247, 1016)])
voll = nd.binary_fill_holes(ISN > .5)
kern = nd.binary_erosion(voll, iterations=7)                       # innen immer deckend (Spitze nicht durchscheinend)
obj = np.where(kern, 1.0, np.clip((ISN - .2) / .6, 0, 1))
aussen = ~nd.binary_erosion(voll, iterations=12)                   # Randzone: hellgrauen Fotohintergrund herausnehmen
obj = np.where(aussen, obj * (1 - np.clip((L - 150) / 50, 0, 1)), obj)

# Karte
box = np.zeros((H, W), bool); box[268:712, 345:892] = True
lab, _ = nd.label((L > 222) & box); karte_sicht = nd.binary_closing(lab == lab[400, 600], iterations=3)
cols = range(345, 892)
unten = {x: (np.where(karte_sicht[:, x])[0].max() if karte_sicht[:, x].any() else 395) for x in cols}
KX0, KX1, KY0, KY1 = 352, 886, 272, 800
kform = poly([(KX0, 273), (KX1, 281), (KX1, KY1), (KX0, KY1)])
tile = OF[292:372, 372:866]; pap = np.zeros_like(OF)
for y in range(KY0, KY1 + 1): pap[y, 372:866] = tile[(y - 292) % 80]
pap[:, KX0:372] = pap[:, 372:392][:, ::-1][:, :372 - KX0]; pap[:, 866:KX1 + 1] = pap[:, 845:866][:, ::-1][:, :KX1 + 1 - 866]
pap = pap * (1 - np.clip((yy[..., None] - 520) / 900, 0, .12))

# Hinten: Karte weg; unter dem Knick Spitze als Innenseite, darüber in der Klappe Spitze, sonst durchsichtig
loch = nd.binary_dilation(kform | karte_sicht, iterations=3)
innen = np.roll(OF, 330, axis=0) * 0.7                     # Spitze der Tasche weiter unten als Innenseite
hint = np.where((loch & (yy >= 395))[..., None], innen, OF)
hint = np.where((loch & klappe)[..., None], np.roll(OF, -420, axis=0) * .85, hint)
a_hint = np.where(loch & (yy < 395) & ~klappe, 0, np.where(loch, 1, obj))

# Vorne: Tasche vor der Karte + Hand
vorne_a = np.zeros((H, W))
for x in cols:
    b = unten[x]; vorne_a[b + 1:, x] = 1
    band = slice(max(b - 16, 0), b + 1); vorne_a[band, x] = np.clip((150 - L[band, x]) / 110, 0, 1)
vorne_a[:, :345] = 0; vorne_a[:, 892:] = 0; vorne_a[:395, :362] = 0; vorne_a[:395, 876:] = 0
vorne_a = np.minimum(vorne_a, obj)

def entsaumen(rgb, a):
    voll = a > .95
    idx = nd.distance_transform_edt(~voll, return_distances=False, return_indices=True)
    rand = (a <= .95) & nd.binary_dilation(a < .05, iterations=5)
    rgb = np.where(rand[..., None], rgb[idx[0], idx[1]], rgb)
    a = np.where(rand, np.clip((a - .15) / .85, 0, 1), a)
    return rgb, a

def save(name, rgb, a):
    rgb, a = entsaumen(rgb, a)
    rgb = rgb[Y0:Y0 + CH, X0:X0 + CW]; a = cv2.GaussianBlur((a[Y0:Y0 + CH, X0:X0 + CW] * 255).astype(np.float32), (0, 0), .6)
    im = Image.fromarray(np.dstack([np.clip(rgb, 0, 255), a]).astype('uint8'), 'RGBA')
    bb = im.getchannel('A').point(lambda v: 255 if v > 6 else 0).getbbox(); im = im.crop(bb)
    im = im.resize((round(im.width * S), round(im.height * S)), Image.LANCZOS); im.save(OUT + name + '.webp', 'WEBP', quality=82)
    return {'l': bb[0] / CW * 100, 't': bb[1] / CH * 100, 'w': (bb[2] - bb[0]) / CW * 100}
m = {'hinten': save('frei-hinten', hint, a_hint), 'vorne': save('frei-vorne', OF, vorne_a), 'karte': save('frei-karte', pap, kform.astype(float))}
json.dump(m, open(OUT + 'masse-frei.json', 'w'), indent=1); print(m)
