import sys
import json, re, unicodedata
from parse import norm
E=json.load(open('entries.json'))
D=json.load(open(sys.argv[1] if len(sys.argv)>1 else '../ux2/data.json'))
STOP=set('haarmaske maske haarkur kur conditioner spulung leave in leavein ml the de la le und mit fur for hair haar pflege care 1 2 3 4 5 100 150 200 250 300 400 50 75 125'.split())
BRALIAS={'loreal':'l oreal','l oreal paris elvital':'elvital'}
def toks(s): return [{'maske':'mask','masque':'mask'}.get(t,t) for t in norm(s).split() if t not in STOP and len(t)>1]
SRC={'maske':['haarmasken-liste.md','nachtrag-liste.md'],'conditioner':['conditioner-liste.md','dm.json','nachtrag-liste.md'],'leavein':['leave-in-inhaltsstoffe.md','nachtrag-liste.md','oel-liste.md']}
out={}
for t in ['maske','conditioner','leavein']:
    for p in D[t]['items']:
        bt=set(toks(p['brand'])); nt=set(toks(p['name']))
        best=None
        for i,e in enumerate(E):
            h=set(toks(e['hdr']))
            bo=len(bt&h)/max(1,len(bt))
            if bo<0.5: continue
            no=len(nt&h)/max(1,len(nt))
            hn=norm(e['hdr'])
            pen=0
            if t=='maske' and 'leave' in hn: pen=0.5
            if t=='leavein' and re.search(r'\b(haarmaske|maske|mask|kur)\b',hn) and 'leave' not in hn and 'serum' not in hn: pen=0.4
            if t=='conditioner' and 'leave' in hn: pen=0.4
            sc=no+0.3*bo+(0.15 if e['src'] in SRC[t] else 0)-pen
            if not best or sc>best[0]: best=(sc,i,no)
        key=t+'|'+p['brand']+'|'+p['name']
        out[key]={'score':round(best[0],2) if best else 0,'nameov':round(best[2],2) if best else 0,'hdr':E[best[1]]['hdr'] if best else None,'inci':E[best[1]]['inci'] if best else None,'src':E[best[1]]['src'] if best else None}
json.dump(out,open('matched.json','w'),ensure_ascii=False,indent=1)
import collections
c=collections.Counter(('ok' if v['nameov']>=0.6 else 'weak' if v['nameov']>=0.3 else 'none') for v in out.values()); print(c)
for k,v in out.items():
    if v['nameov']<0.6: print(round(v['nameov'],2),'|',k,'=>',(v['hdr'] or '')[:100])
