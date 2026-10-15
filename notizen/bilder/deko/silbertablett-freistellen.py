import sys
from PIL import Image
import numpy as np
from scipy import ndimage
S=sys.argv[1]
im=Image.open('notizen/bilder/deko/vorlagen/silbertablett.jpg').convert('RGB'); a=np.asarray(im).astype(float); H,W=a.shape[:2]
m=np.asarray(Image.open(S+'/tablett-mask-bire.png').convert('L')).astype(float)/255
g=np.asarray(Image.open(S+'/glove-sam.png').convert('L'))>127
lab,n=ndimage.label(g); sizes=ndimage.sum(g,lab,range(1,n+1)); g=lab==(1+int(np.argmax(sizes)))
g=ndimage.binary_erosion(g,iterations=1)
gs=np.clip(ndimage.gaussian_filter(g.astype(float),1.2)*1.15,0,1)
mask=np.maximum(m,gs)
filled=ndimage.binary_fill_holes(mask>0.5)
mask=np.where(filled&(mask<0.5),1.0,mask)
out=Image.fromarray(np.dstack([a,np.clip(mask,0,1)*255]).astype(np.uint8),'RGBA'); out.save(S+'/tablett-v3.png')
ims=[]
for c in [(251,247,243),(120,90,80)]:
  b=Image.new('RGBA',out.size,c+(255,)); b.alpha_composite(out); ims.append(b.convert('RGB'))
s=Image.new('RGB',(W*2,H)); s.paste(ims[0],(0,0)); s.paste(ims[1],(W,0)); s.thumbnail((1800,1200)); s.save(S+'/tablett-check.jpg')
