# Stoff-Patch (IMG_0202) vom schwarzen Hintergrund freistellen und quer drehen.
# Aufruf: python3 -I stoffpatch-freistellen.py <eingabe.jpg> <ausgabe.webp> [vorschau.jpg]
import sys
from PIL import Image
import numpy as np
from scipy import ndimage
im=Image.open(sys.argv[1]).convert('RGB'); a=np.asarray(im).astype(float)
L=a.mean(2)
body=ndimage.binary_fill_holes(L>70)
lab,n=ndimage.label(body); sizes=ndimage.sum(body,lab,range(1,n+1)); body=lab==(1+int(np.argmax(sizes)))
core=ndimage.binary_erosion(body,iterations=6)
soft=np.clip((L-22)/(120-22),0,1)
near=ndimage.binary_dilation(body,iterations=14)
al=np.where(core,1.0,np.where(near,soft,0.0))
col=a/np.maximum(al[...,None],1e-3)
grey=col.mean(2,keepdims=True)
col=np.where(core[...,None],a,np.clip(grey*np.array([1.02,0.99,0.96]),0,255))  # Fransen ohne Blaustich, warm wie der Stoff
out=Image.fromarray(np.dstack([col,al*255]).astype(np.uint8),'RGBA')
ys,xs=np.where(al>0.05); out=out.crop((xs.min(),ys.min(),xs.max()+1,ys.max()+1)).rotate(90,expand=True)
o2=out.resize((760,round(760*out.height/out.width)),Image.LANCZOS); o2.save(sys.argv[2],quality=86,method=6); print(o2.size)
if len(sys.argv)>3:
  b=Image.new('RGBA',o2.size,(243,236,226,255)); b.alpha_composite(o2); b.convert('RGB').save(sys.argv[3])
