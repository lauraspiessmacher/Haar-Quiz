# Erzeugt regal/fach.webp: Holz-Rückwand aus dem Higgsfield-Foto (bilder/regal/fach-b.png),
# geglättet und in kühles Dunkelbraun umgefärbt (Mischung aus echt und gezeichnet),
# dazu ein gezeichnetes Brett mit klarer Lichtkante. Standlinie der Bücher bei STAND (Anteil der Höhe).
import sys
from PIL import Image, ImageFilter, ImageDraw
import numpy as np
W, H = 1600, 686
STAND = 0.89
wall = sys.argv[1] if len(sys.argv) > 1 else '4A3F3C'
out = sys.argv[2] if len(sys.argv) > 2 else 'regal/fach.webp'
src = Image.open('../bilder/regal/fach-b.png').convert('L')
# nur die Rückwand (ohne Brett) nehmen und auf volle Höhe ziehen
src = src.crop((0, 40, src.width, int(src.height * 0.80))).resize((W, H), Image.LANCZOS)
g = src.filter(ImageFilter.MedianFilter(5)).filter(ImageFilter.GaussianBlur(1.2))
a = np.asarray(g).astype(float)
a = (a - a.mean()) / (a.std() + 1e-6)          # Maserung normiert
a = np.clip(a, -2.2, 2.2) / 2.2                  # -1 … 1
base = np.array([int(wall[i:i+2], 16) for i in (0, 2, 4)], float)
img = base[None, None, :] * (1 + 0.22 * a[..., None])
# Schatten vom Brett darüber
y = np.arange(H)[:, None, None]
img *= 1 - 0.38 * np.exp(-y / 38)
im = Image.fromarray(np.clip(img, 0, 255).astype('uint8'))
d = ImageDraw.Draw(im)
s = int(H * STAND)
dark = tuple(int(c * 0.62) for c in base)
d.rectangle((0, s - 14, W, s + 2), fill=tuple(int(c * 1.32) for c in base))   # Brett-Oberseite
d.rectangle((0, s + 2, W, H), fill=tuple(int(c * 0.95) for c in base))       # Brett-Vorderkante
d.line((0, s + 2, W, s + 2), fill=tuple(min(255, int(c * 1.75)) for c in base), width=2)  # Lichtkante
d.line((0, s - 14, W, s - 14), fill=dark, width=2)                             # Fuge hinten
d.line((0, H - 1, W, H - 1), fill=dark, width=3)                               # Unterkante
im.save(out, 'WEBP', quality=80)
