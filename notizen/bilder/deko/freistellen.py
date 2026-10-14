import sys
from PIL import Image
import numpy as np
from scipy import ndimage
S=sys.argv[1]; tol=float(sys.argv[2])
im=Image.open(S+'/heic/IMG_0200_2.png').convert('RGB'); a=np.asarray(im).astype(float)
diff=np.abs(a-235).max(2)
lab,n=ndimage.label(diff<=tol)
border=set(np.unique(np.concatenate([lab[0],lab[-1],lab[:,0],lab[:,-1]])))-{0}
bg=np.isin(lab,list(border))
fg=ndimage.binary_fill_holes(~bg)
# smooth the mask edge: open to remove specks, then feather 1px
fg=ndimage.binary_opening(fg,iterations=1); fg=ndimage.binary_erosion(fg,iterations=2)
alpha=ndimage.gaussian_filter(fg.astype(float),0.8)
alpha=np.clip((alpha-0.15)/0.7,0,1)
out=np.dstack([a,alpha*255]).astype(np.uint8)
o=Image.fromarray(out,'RGBA'); bb=o.getbbox()
o=o.crop((max(0,bb[0]-4),max(0,bb[1]-4),bb[2]+4,bb[3]+4)); o.save(S+'/pin-cut.png')
ims=[]
for c in [(255,255,255),(56,47,46),(150,120,100)]:
  b=Image.new('RGBA',o.size,c+(255,)); b.alpha_composite(o); ims.append(b.convert('RGB'))
s=Image.new('RGB',(o.width*3,o.height)); [s.paste(x,(i*o.width,0)) for i,x in enumerate(ims)]
s.thumbnail((1800,800)); s.save(S+'/pin-check.jpg'); print(o.size)
