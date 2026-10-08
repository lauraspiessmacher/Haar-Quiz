# Baut die Brief-Animation (notizen/brief/brief.html) in alle vier Quizze ein bzw. aktualisiert sie.
# Aufruf aus dem Repo-Ordner: python3 notizen/brief/einbauen.py
import re
snip = open('notizen/brief/brief.html').read().strip()
for f in ('quiz-pflege.html', 'quiz-kopfhaut.html', 'quiz-haar.html', 'quiz-routine.html'):
    t = open(f).read()
    if '<!-- BRIEF START' in t:
        t = re.sub(r'<!-- BRIEF START.*?<!-- BRIEF END -->', lambda m: snip, t, flags=re.S)
    else:
        i = t.rindex('</body>'); t = t[:i] + snip + '\n' + t[i:]
    open(f, 'w').write(t); print('ok', f)
