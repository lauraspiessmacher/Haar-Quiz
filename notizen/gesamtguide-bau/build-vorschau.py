# Baut die Gesamt-Vorschau aus allen Einzel-Guides.
# 1) node dump.js data.json   2) python3 build-vorschau.py data.json
# Ergebnis: notizen/ux-vorschau-2.html (zum lokalen Öffnen) und
#           notizen/ux-vorschau-2-link.html (für den privaten Link, ohne eigenes Seitengerüst; Quiz liegt daneben als quiz.html)
import sys, os, re
S = os.path.dirname(os.path.abspath(__file__))
data = open(sys.argv[1]).read().replace('</', '<\\/')
t = open(f'{S}/vorschau2-template.html').read().replace('__DATA__', data)
open(f'{S}/../ux-vorschau-2.html', 'w').write(t.replace('__QUIZ__', '../index.html').replace('__QUIZ2__', '../quiz-kopfhaut.html'))
a = t.replace('__QUIZ__', 'quiz.html').replace('__QUIZ2__', 'quiz-kopfhaut.html')
a = re.sub(r'^<!DOCTYPE html>\s*<html[^>]*>\s*<head>\s*', '', a)
a = re.sub(r'<meta charset="utf-8">\s*<meta name="viewport"[^>]*>\s*', '', a)
a = a.replace('</head>\n<body>\n', '\n', 1)
a = re.sub(r'</body>\s*</html>\s*$', '\n', a)
assert a.lstrip().startswith('<title>'), a[:80]
open(f'{S}/../ux-vorschau-2-link.html', 'w').write(a)
print('ok', len(t)//1024, 'KB')
