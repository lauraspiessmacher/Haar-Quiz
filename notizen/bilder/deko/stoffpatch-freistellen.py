# Stoff-Patch (IMG_0202) vom schwarzen Hintergrund freistellen und quer drehen.
# Fransen bekommen die Stofffarbe (kein dunkler Rand), der Schlagschatten auf dem schwarzen Grund fällt weg,
# dunkle Schattenkanten am Patch-Rand werden sanft aufgehellt, damit er auf der hellen Seite natürlich liegt.
# Aufruf: python3 -I stoffpatch-freistellen.py <eingabe.jpg> <ausgabe.webp> <drehung 90|270> [vorschau.jpg]
import sys
from PIL import Image
import numpy as np
from scipy import ndimage
im=Image.open(sys.argv[1]).convert('RGB'); a=np.asarray(im).astype(float)
L=a.mean(2)
body=ndimage.binary_fill_holes(L>90)
lab,n=ndimage.label(body); sizes=ndimage.sum(body,lab,range(1,n+1)); body=lab==(1+int(np.argmax(sizes)))
core=ndimage.binary_erosion(body,iterations=4)
cream=np.array([222,215,206.0])
# Fransen: Alpha aus Helligkeit (Schatten < 60 fällt weg), Farbe = Stofffarbe
fr=np.clip((L-60)/(205-60),0,1)
near=ndimage.binary_dilation(body,iterations=16)
al=np.where(core,1.0,np.where(near,fr,0.0))
col=np.where(core[...,None],a,cream)
# dunkle Kanten innerhalb des Patches sanft aufhellen (nur nahe am Rand)
dist=ndimage.distance_transform_edt(core)
edge=np.clip(1-dist/34,0,1)
dark=np.clip((175-L)/120,0,1)
k=(edge*dark*0.75)[...,None]
col=np.where(core[...,None],col+(cream-col)*k,col)
out=Image.fromarray(np.dstack([np.clip(col,0,255),al*255]).astype(np.uint8),'RGBA')
ys,xs=np.where(al>0.05); out=out.crop((xs.min(),ys.min(),xs.max()+1,ys.max()+1)).rotate(int(sys.argv[3]),expand=True)
o2=out.resize((700,round(700*out.height/out.width)),Image.LANCZOS); o2.save(sys.argv[2],quality=88,method=6); print(o2.size)
if len(sys.argv)>4:
  b=Image.new('RGBA',o2.size,(249,246,242,255)); b.alpha_composite(o2); b.convert('RGB').save(sys.argv[4])
