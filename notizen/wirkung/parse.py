import re, json, unicodedata, sys
N='/home/user/Haar-Quiz/notizen/'
def norm(s):
    s=unicodedata.normalize('NFD',s.lower()).encode('ascii','ignore').decode()
    return re.sub(r'[^a-z0-9 ]',' ',s.replace('&',' '))
def is_inci(l):
    l=l.strip()
    seps=l.count(',')+l.count('•')
    return seps>=3 and re.search(r'\b(aqua|water|alcohol|dimethicone|glycerin|parfum|cetearyl|isododecane|isohexadecane|oil|butter|acid|isododecane|siloxane|dimethiconol)\b',l,re.I) and not l.startswith('|')
entries=[]
for f in ['haarmasken-liste.md','conditioner-liste.md','leave-in-inhaltsstoffe.md','nachtrag-liste.md','oel-liste.md']:
    lines=open(N+f).read().split('\n'); hdr=''
    for l in lines:
        s=l.strip()
        if not s: continue
        if s.startswith('#') or re.match(r'^[A-Za-z]?\d+\.\s',s) or re.match(r'^\*\*',s) or (' | ' in s and not s.startswith('|')) or re.match(r'^- \*\*',s):
            hdr=s; continue
        if is_inci(s):
            if hdr: entries.append({'src':f,'hdr':hdr,'inci':re.sub(r'^(INGREDIENTS|Inhaltsstoffe|INCI)\s*:\s*','',s,flags=re.I)})
            continue
# conditioner dm.json + data.py
ns={}; exec(open(N+'conditioner-bau/data.py').read(),ns)
dm=json.load(open(N+'conditioner-bau/dm.json'))
for k,v in dm.items():
    inc=v['groups'].get('Inhaltsstoffe','')
    if inc and k in ns['P']:
        b,n=ns['P'][k][0],ns['P'][k][1]
        entries.append({'src':'dm.json','hdr':b+' | '+n+' | '+v['title'],'inci':re.sub(r'^INGREDIENTS:\s*','',inc)})
json.dump(entries,open('entries.json','w'),ensure_ascii=False,indent=0)
print(len(entries))
