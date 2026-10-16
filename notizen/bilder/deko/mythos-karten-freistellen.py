"""Mythos-oder-Fakt-Karte: Lauras Vorlagen freistellen (rembg-Masken aus dem Scratchpad, Pfad als Argument).
Bügel: Handschrift entfernen, Stange an beiden Enden weich auslaufen lassen. Stapel: auf den Inhalt zuschneiden."""
import sys
import numpy as np, cv2
from PIL import Image
S = sys.argv[1]
# --- Bügel ---
im = np.asarray(Image.open('vorlagen/mythos-buegel.jpg').convert('RGB')).copy()
m = np.asarray(Image.open(S + '/buegel-bire.png').convert('L')).astype(float)
reg = im[740:1030, 250:960].astype(int)
dark = (reg.sum(2) < 3 * 150)
mask = np.zeros(im.shape[:2], np.uint8); mask[740:1030, 250:960] = dark * 255
mask = cv2.dilate(mask, np.ones((5, 5), np.uint8), iterations=2)
bgr = cv2.cvtColor(im, cv2.COLOR_RGB2BGR)
bgr = cv2.inpaint(bgr, mask, 9, cv2.INPAINT_TELEA)
# feines Papierkorn wieder drüberlegen, damit die Stelle nicht glatt wirkt
rng = np.random.default_rng(3); noise = rng.normal(0, 2.2, bgr.shape[:2])
sel = mask > 0
for c in range(3):
    ch = bgr[..., c].astype(float); ch[sel] += noise[sel]; bgr[..., c] = np.clip(ch, 0, 255).astype(np.uint8)
im = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
a = m.copy()
# rembg hat die Stange rechts vom rechten Clip verloren: aus dem Foto nachholen (dunkler als der Hintergrund)
g = im[430:495, 880:].astype(float).sum(2) / 3
bar = np.clip((205 - g) / 40, 0, 1) * 255
a[430:495, 880:] = np.maximum(a[430:495, 880:], bar)
x0, x1 = 44, 1200; fade = 110
xs = np.arange(im.shape[1])
f = np.clip(np.minimum(xs - x0, x1 - xs) / fade, 0, 1)
a[400:520, :] *= f[None, :]
out = Image.fromarray(np.dstack([im, a.clip(0, 255)]).astype(np.uint8), 'RGBA').crop((x0, 20, x1, 1290))
out.save('mythos-buegel.webp', quality=88, method=6); print('buegel', out.size)
# --- Stapel ---
im = Image.open('vorlagen/mythos-papierstapel.jpg').convert('RGBA')
im.putalpha(Image.open(S + '/stapel-bire.png').convert('L'))
out = im.crop((203, 253, 897, 1095)); out.save('mythos-stapel.webp', quality=88, method=6); print('stapel', out.size)
