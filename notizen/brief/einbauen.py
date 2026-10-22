# Baut die Brief-Animation (notizen/brief/brief.html) in alle vier Quizze ein bzw. aktualisiert sie.
# Die Umschlag-Ebenen (umschlag/*.webp, erzeugt mit umschlag.py aus Lauras Fotos) werden als data-URI eingesetzt.
# Aufruf aus dem Repo-Ordner: python3 notizen/brief/einbauen.py [--nur-snippet ZIELDATEI]
import re, sys, base64
D = 'notizen/brief'
def uri(f): return 'data:image/webp;base64,' + base64.b64encode(open(f'{D}/{f}', 'rb').read()).decode()
snip = open(f'{D}/brief.html').read().strip()
for ph, f in [('__U_ZU__','zu'),('__U_HINTEN__','hinten'),('__U_KLAPPEZU__','klappe-zu'),('__U_KLAPPEAUF__','klappe-auf'),('__U_VORNE__','vorne'),('__U_KARTE__','karte')]:
    snip = snip.replace(ph, uri(f'umschlag/{f}.webp'))
import json
for ebene, mm in json.load(open(f'{D}/umschlag/masse.json')).items():   # Lage der Ebenen kommt aus umschlag.py
    for k, v in mm.items(): snip = snip.replace(f'__M_{ebene}_{k}__', f'{v:.3f}')
assert '__M_' not in snip
if len(sys.argv) > 2 and sys.argv[1] == '--nur-snippet':
    open(sys.argv[2], 'w').write(snip); sys.exit()
for f in ('quiz-pflege.html', 'quiz-kopfhaut.html', 'quiz-haar.html', 'quiz-routine.html', 'quiz-tools.html', 'quiz-schnitt.html', 'quiz-spliss.html', 'quiz-leavein.html', 'quiz-ausfall.html', 'quiz-kopfpflege.html'):
    t = open(f).read()
    if '<!-- BRIEF START' in t:
        t = re.sub(r'<!-- BRIEF START.*?<!-- BRIEF END -->', lambda m: snip, t, flags=re.S)
    else:
        i = t.rindex('</body>'); t = t[:i] + snip + '\n' + t[i:]
    open(f, 'w').write(t); print('ok', f)
