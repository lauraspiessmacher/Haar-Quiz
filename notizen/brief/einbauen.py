# Baut die Brief-Animation (notizen/brief/brief.html) in alle vier Quizze ein bzw. aktualisiert sie.
# Die Umschlag-Ebenen (umschlag/frei-*.webp, erzeugt mit umschlag_offen.py aus Lauras Foto) und die Schrift werden als data-URI eingesetzt.
# Aufruf aus dem Repo-Ordner: python3 notizen/brief/einbauen.py [--nur-snippet ZIELDATEI]
import re, sys, base64
D = 'notizen/brief'
def uri(f): return 'data:image/webp;base64,' + base64.b64encode(open(f'{D}/{f}', 'rb').read()).decode()
# Zwei Designs liegen bereit (Laura 22.10.: vielleicht will sie am Ende das alte zurück):
#   Standard:  brief.html  (= brief-spitze.html, Spitzen-Umschlag aus Lauras Foto)
#   --siegel:  brief-siegel-alt.html (gezeichneter Umschlag mit Wachssiegel, das bricht)
SIEGEL = '--siegel' in sys.argv
if SIEGEL: sys.argv.remove('--siegel')
snip = open(f'{D}/' + ('brief-siegel-alt.html' if SIEGEL else 'brief.html')).read().strip()
snip = snip.replace('__BRIEF_PAPIER__', uri('papier.webp')).replace('__BRIEF_SIEGEL__', uri('siegel.webp'))
for ph, f in [('__U_HINTEN__','frei-hinten'),('__U_VORNE__','frei-vorne'),('__U_KARTE__','frei-karte')]:
    snip = snip.replace(ph, uri(f'umschlag/{f}.webp'))
for ph, f in [('__F_NORMAL__','instrument-serif-normal'),('__F_ITALIC__','instrument-serif-italic')]:   # Überschriften-Schrift, nur die Buchstaben der Karte
    snip = snip.replace(ph, 'data:font/woff2;base64,' + base64.b64encode(open(f'{D}/schrift/{f}.woff2','rb').read()).decode())
import json
for ebene, mm in json.load(open(f'{D}/umschlag/masse-frei.json')).items():   # Lage der Ebenen kommt aus umschlag_offen.py
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
