# Baut die Brief-Animation (notizen/brief/brief.html) in alle vier Quizze ein bzw. aktualisiert sie.
# Papier (papier.webp) und Siegel (siegel.webp) werden als data-URI eingesetzt.
# Aufruf aus dem Repo-Ordner: python3 notizen/brief/einbauen.py [--nur-snippet ZIELDATEI]
import re, sys, base64
D = 'notizen/brief'
def uri(f): return 'data:image/webp;base64,' + base64.b64encode(open(f'{D}/{f}', 'rb').read()).decode()
snip = open(f'{D}/brief.html').read().strip().replace('__BRIEF_PAPIER__', uri('papier.webp')).replace('__BRIEF_SIEGEL__', uri('siegel.webp'))
if len(sys.argv) > 2 and sys.argv[1] == '--nur-snippet':
    open(sys.argv[2], 'w').write(snip); sys.exit()
for f in ('quiz-pflege.html', 'quiz-kopfhaut.html', 'quiz-haar.html', 'quiz-routine.html'):
    t = open(f).read()
    if '<!-- BRIEF START' in t:
        t = re.sub(r'<!-- BRIEF START.*?<!-- BRIEF END -->', lambda m: snip, t, flags=re.S)
    else:
        i = t.rindex('</body>'); t = t[:i] + snip + '\n' + t[i:]
    open(f, 'w').write(t); print('ok', f)
