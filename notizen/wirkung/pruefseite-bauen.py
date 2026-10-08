# Baut notizen/wirkung/pruefseite.html: Lauras Prüfliste der INCI-Einordnung (Feuchtigkeit / Nährend / Glättend, Repair: Proteine / Bond)
# Aufruf: python3 pruefseite-bauen.py <klassen.json>
import json, re, sys, datetime
K = json.load(open(sys.argv[1]))
TYP = {'maske': 'Maske', 'conditioner': 'Conditioner', 'leavein': 'Leave-in'}
DK = ['fein', 'duenn', 'normal', 'dick', 'sehrdick']
# Welche Produkte landen gerade in „Meine Empfehlung“? (gleiche Logik wie pickRec im Template)
def best(lst, key):
    return sorted(lst, key=lambda v: (-key(v), (v['brand'] + v['name']).lower()))[0] if lst else None
def sc(v): return v['H'] if v['kind'] == 'feucht' else v['E'] if v['kind'] == 'naehrend' else 0
empf = {}
for t in TYP:
    for d in DK:
        it = [v for v in K.values() if v['type'] == t and d in v['cats']]
        used = []
        def pick(c, lab, stufe):
            if c:
                used.append(c); empf.setdefault(c['type'] + '|' + c['brand'] + '|' + c['name'], set()).add(f"{lab} · {d.replace('duenn','dünn').replace('sehrdick','sehr dick')}{stufe}")
        f = best([v for v in it if v['kind'] == 'feucht' and not v['rep']], sc) or best([v for v in it if v['kind'] == 'feucht'], sc); pick(f, 'Feuchtigkeit', '')
        n = best([v for v in it if v['kind'] == 'naehrend' and not v['rep'] and v not in used], sc) or best([v for v in it if v['kind'] == 'naehrend' and v not in used], sc); pick(n, 'Nährend', '')
        rep = [v for v in it if 'kaputt' in v['cats'] and v not in used]
        b = best([v for v in rep if v['rep'] == 'bond'], sc) or best([v for v in rep if v['rep'] == 'protein'], sc); pick(b, 'Repair', ' (Bond-Stufe)')
        p = best([v for v in rep if v['rep'] == 'protein'], sc); pick(p, 'Repair', ' (Protein-Stufe)')
rows = []
for k, v in K.items():
    pid = re.sub(r'[^A-Za-z0-9_\-.~:@+]', '-', k)[:180]
    why = []
    if v['hum']: why.append('Feuchtigkeit: ' + ', '.join(v['hum']))
    if v['emo']: why.append('Öle/Fette: ' + ', '.join(v['emo']))
    if v['bond']: why.append('Bond: ' + ', '.join(v['bond']))
    elif v['prot']: why.append('Proteine: ' + ', '.join(v['prot']))
    if v.get('note2'): why.append(v['note2'])
    rows.append({'id': pid, 'typ': v['type'], 'brand': v['brand'], 'name': v['name'], 'seg': v['segment'],
                 'dk': [c for c in v['cats'] if c in DK], 'kaputt': 'kaputt' in v['cats'], 'w': v['kind'], 'r': v['rep'],
                 'why': ' · '.join(why), 'note': v['note'], 'empf': sorted(empf.get(k, []))})
rows.sort(key=lambda r: (list(TYP).index(r['typ']), (r['brand'] + r['name']).lower()))
data = json.dumps({'stand': datetime.date.today().isoformat(), 'rows': rows}, ensure_ascii=False).replace('</', '<\\/')
t = open('pruefseite-vorlage.html').read().replace('__DATA__', data)
open('pruefseite.html', 'w').write(t)
print(len(rows), 'Produkte,', sum(1 for r in rows if r['empf']), 'davon in Empfehlungen')
