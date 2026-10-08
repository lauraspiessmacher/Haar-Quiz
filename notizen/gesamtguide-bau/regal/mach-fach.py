# Erzeugt regal/fach.webp aus dem Higgsfield-Foto (bilder/regal/fach-b.png):
# echtes Holz mit Brett, Maserung leicht verstärkt und in kühles Schwarzbraun umgefärbt.
# Aufruf aus gesamtguide-bau: python3 regal/mach-fach.py [Grundfarbe hex] [Ziel]
# Brett im Foto: Lichtkante vorne bei 92,7 % der Höhe (siehe alignShelf im Template).
import sys
from PIL import Image, ImageFilter
import numpy as np
base_hex = sys.argv[1] if len(sys.argv) > 1 else '231C1B'
out = sys.argv[2] if len(sys.argv) > 2 else 'regal/fach.webp'
W, H = 1600, 686
im = Image.open('../bilder/regal/fach-b.png').convert('L').resize((W, H), Image.LANCZOS)
a = np.asarray(im).astype(float)
b = np.asarray(im.filter(ImageFilter.GaussianBlur(16))).astype(float)
lum = b + (a - b) * 1.7                     # Maserung etwas deutlicher
lum = np.clip(lum / 52.0, 0.35, 1.9)        # 1.0 = mittlere Rückwand
base = np.array([int(base_hex[i:i+2], 16) for i in (0, 2, 4)], float)
img = base[None, None, :] * lum[..., None]
Image.fromarray(np.clip(img, 0, 255).astype('uint8')).save(out, 'WEBP', quality=78)
