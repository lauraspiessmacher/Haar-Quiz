# Baut notizen/ux-vorschau-2.html aus allen Einzel-Guides.
# 1) node dump.js <data.json>   2) python3 build-vorschau.py <data.json>
import sys, os
S = os.path.dirname(os.path.abspath(__file__))
data = open(sys.argv[1]).read().replace('</', '<\\/')
t = open(f'{S}/vorschau2-template.html').read().replace('__DATA__', data)
open(f'{S}/../ux-vorschau-2.html', 'w').write(t)
print('ok', len(t)//1024, 'KB')
