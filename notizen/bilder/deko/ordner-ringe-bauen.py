# Ringstreifen aus Lauras Ordner-Foto (vorlagen/ordner-ringbuch.jpg) als nahtlos wiederholbare Kachel.
# Der Ordnerrücken ist im Foto leicht schräg, deshalb wird jede Zeile so verschoben, dass er senkrecht steht.
import sys
from PIL import Image
import numpy as np
from scipy import ndimage
src=np.asarray(Image.open(sys.argv[1]).convert('RGB')).astype(float)
y0,P,W=358,472,200
ys=np.arange(y0-40,y0+P)
# Rückenmitte je Zeile (gewichteter Schwerpunkt der Dunkelheit in x 50..78), linear geglättet
cx=[]
for y in ys:
  r=255-src[y,50:78].mean(1); r=np.clip(r-60,0,None); cx.append(50+(r*np.arange(28)).sum()/max(r.sum(),1e-3))
m,b=np.polyfit(ys,cx,1); target=m*y0+b
rows={}
for y in ys:
  d=(m*y+b)-target
  rows[y]=np.stack([ndimage.shift(src[y,:W+20,c],-d,order=1,mode='nearest') for c in range(3)],1)[:W]
a=np.stack([rows[y] for y in range(y0,y0+P)])
n=30
for i in range(n):
  w=(i+1)/(n+1); a[P-n+i]=a[P-n+i]*(1-w)+rows[y0-n+i]*w
pc=np.array([240.5,240.3,238.0])
for x in range(W-30,W):
  w=(x-(W-30)+1)/30; a[:,x]=a[:,x]*(1-w)+pc*w
o=Image.fromarray(np.clip(a,0,255).astype(np.uint8)); o.save(sys.argv[2],quality=90,method=6)
if len(sys.argv)>3:
  pv=Image.new('RGB',(400,P*3),(240,240,238))
  for k in range(3): pv.paste(o,(0,k*P))
  pv.save(sys.argv[3])
print('Neigung px/Zeile', round(m,4))
