import sys, json, io, base64, os, re
from PIL import Image
S = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, S)
from data import CATS, P, ANW

tpl = open('/home/user/Haar-Quiz/masken-guide.html').read()
css = tpl[tpl.index('<style>'):tpl.index('</style>')] + '.also{border-radius:12px;line-height:1.5;padding:2px 10px}\n.tip.anw{font-size:13px;line-height:1.45;padding:5px 10px}\n.hint{font-size:13px;color:var(--muted);margin-top:6px;font-style:italic}\n</style>'

imgs = {}
for key, *_ in P:
    f = f'{S}/cut/{key}.png'
    if not os.path.exists(f): continue
    im = Image.open(f).convert('RGBA')
    im = im.crop(im.getchannel('A').point(lambda v: 255 if v > 8 else 0).getbbox()); im.thumbnail((180, 180), Image.LANCZOS)
    b = io.BytesIO(); im.save(b, 'WEBP', quality=85, method=6)
    imgs[key] = 'data:image/webp;base64,' + base64.b64encode(b.getvalue()).decode()

rows = [[k, b, n, c, a, no, w, d, ANW.get(an, an), hi, s] for k, b, n, c, a, no, w, d, an, hi, s in P]
cats = [{"id": i, "label": l, "desc": d} for i, l, d in CATS]

html = '''<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Dein Kopfhaut-Guide</title>
''' + css + '''
</head>
<body>
<main class="wrap">
  <div class="head">
    <svg viewBox="0 0 60 100" fill="none" aria-hidden="true">
      <path d="M22 4 C 14 30, 30 55, 20 96" stroke="#382F2E" stroke-width="1.2"/>
      <path d="M40 4 C 32 30, 48 55, 38 96" stroke="#9E8C80" stroke-width="1.2"/>
    </svg>
    <div class="by">Von Laura, deiner Haarpflege-Bestie</div>
    <h1>Dein Kopfhaut-Guide</h1>
    <p class="lead">Gesunde Haare fangen an der Kopfhaut an. Hier findest du Seren, Tonika, Öle und Peelings, sortiert nach deinem Kopfhauttyp. Eingeordnet habe ich alles nach den Inhaltsstoffen, nicht nach dem, was auf der Packung steht.</p>
    <div class="box">
      <p><b>So verwendest du sie:</b> Kopfhautpflege kommt direkt auf die Kopfhaut, nicht in die Längen. Am besten klappt das mit der Scheiteltechnik: Zieh dir vier bis fünf Scheitel über die ganze Kopfhaut und gib das Produkt mit dem Applikator, der Pipette oder dem Spray direkt auf die Scheitel. Danach sanft mit den Fingerkuppen einmassieren.</p>
      <p><b>Wann?</b> Am besten nach dem Waschen auf die noch feuchte Kopfhaut, vor dem Föhnen. Viele Seren sind für jeden Tag gedacht. Auch dann ist die Scheiteltechnik am saubersten, weil kaum Produkt in die Haare kommt und sie nicht beschwert.</p>
    </div>
  </div>

  <div class="bar">
    <div class="switch" id="seg" role="group" aria-label="Drogerie oder High-End">
      <button data-seg="alle" aria-pressed="true">Alle</button><button data-seg="Drogerie" aria-pressed="false">Drogerie</button><button data-seg="High-End" aria-pressed="false">High-End</button>
    </div>
    <input class="search" id="q" type="search" placeholder="Marke oder Produkt suchen" aria-label="Marke oder Produkt suchen">
    <div class="chips" id="chips" role="group" aria-label="Kopfhauttyp auswählen"></div>
  </div>

  <div id="out"></div>
  <p class="empty" id="empty" hidden>Dazu habe ich gerade kein Produkt in der Liste.</p>

  <p class="fine">Stand: Oktober 2026. Rezepturen können sich ändern, deshalb lohnt sich vor dem Kauf ein kurzer Blick auf die Inhaltsstoffe. Die Einordnung ist eine Orientierung, jede Kopfhaut reagiert etwas anders. Neue Produkte erst an einer kleinen Stelle testen. Bei starkem Juckreiz, Rötungen, Schmerzen oder Haarausfall gehört die Kopfhaut zum Hautarzt.</p>
</main>

<script>
const CATS = ''' + json.dumps(cats, ensure_ascii=False) + ''';

/* [Kürzel, Marke, Produkt, Kategorien, Art, Einschätzung, wichtige Inhaltsstoffe, Duft und Alkohol, Anwendung, Hinweis, Segment] */
const P = [
''' + ',\n'.join(' ' + json.dumps(r, ensure_ascii=False) for r in rows) + '''
].map(([key,brand,name,c,art,note,wirk,duft,anw,hint,segment]) => ({key, segment, brand, name, cats:c.split(" "), art, note, wirk, duft, anw, hint}));
/* Produktbilder, klein neben dem Produkt */
const IMG = ''' + json.dumps(imgs) + ''';
P.forEach(p => p.img = IMG[p.key]);

const chips = document.getElementById("chips"), out = document.getElementById("out"), q = document.getElementById("q"), empty = document.getElementById("empty");
let active = "alle", seg = "alle";
const segBox = document.getElementById("seg");
segBox.querySelectorAll("button").forEach(b => b.onclick = () => {
  seg = b.dataset.seg;
  segBox.querySelectorAll("button").forEach(x => x.setAttribute("aria-pressed", x===b));
  draw();
});
const esc = s => s.replace(/[&<>"]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));

chips.innerHTML = [`<button class="chip" data-id="alle" aria-pressed="true">Alle</button>`]
  .concat(CATS.map(c=>`<button class="chip" data-id="${c.id}" aria-pressed="false">${c.label}</button>`))
  .concat([`<button class="chip" data-id="liste" aria-pressed="false">Liste</button>`]).join("");
chips.querySelectorAll(".chip").forEach(b => b.onclick = () => {
  active = b.dataset.id;
  chips.querySelectorAll(".chip").forEach(x => x.setAttribute("aria-pressed", x===b));
  draw();
});
q.addEventListener("input", draw);

const LABEL = Object.fromEntries(CATS.map(c => [c.id, c.label]));
const passtZu = p => p.cats.map(c => LABEL[c]).join(", ");
function itemHtml(p){
  return `<li class="${p.img?"has-img":""}">${p.img?`<img class="pic" src="${p.img}" alt="" loading="lazy">`:""}<div class="txt">
    <div class="row"><span class="brand">${esc(p.brand)}</span><span class="tags"><span class="tag">${p.segment}</span><span class="heat">${esc(p.art)}</span></span></div>
    <div class="name">${esc(p.name)}</div>
    <div class="note">${esc(p.note)}</div>
    <div class="hair"><b>Wichtige Inhaltsstoffe:</b> ${esc(p.wirk)}</div>
    <div class="hair"><b>Duft und Alkohol:</b> ${esc(p.duft)}</div>
    <span class="also">Passt zu: ${esc(passtZu(p))}</span>
    <div class="tip anw"><b>Anwendung:</b> ${esc(p.anw)}</div>
    ${p.hint?`<div class="hint">${esc(p.hint)}</div>`:""}
  </div></li>`;
}
/* Suche ohne Akzente, Apostrophe, Leer- und Sonderzeichen: „kerastase“ findet „Kérastase“, „loreal“ findet „L'Oréal“. Jedes Suchwort wird einzeln gesucht. */
const plain = s => s.toLowerCase().replace(/ß/g,"ss").normalize("NFD").replace(/[\\u0300-\\u036f]/g,"").replace(/[^a-z0-9]/g,"");
const matches = (p, term) => { if(!(seg==="alle" || p.segment===seg)) return false; if(!term.length) return true; const h = plain([p.brand,p.name,p.note,p.wirk,p.duft,p.art,p.anw,p.hint].join(" ")); return term.every(t => h.includes(t)); };
const byName = (a,b) => (a.brand+a.name).localeCompare(b.brand+b.name,"de");

function drawListe(term){
  let shown = 0;
  out.innerHTML = `<section class="cat" id="liste"><h2>Liste</h2><p class="cat-desc">Alle Produkte pro Kategorie, nur mit Namen. Zum Kopieren auf „Liste kopieren“ tippen.</p>` +
    CATS.map(c => {
      const items = P.filter(p => p.cats.includes(c.id) && matches(p, term)).sort(byName);
      if(!items.length) return "";
      shown += items.length;
      const lines = items.map(p => `${p.brand} – ${p.name}`);
      return `<h3>${c.label}<span class="count">${items.length}</span></h3>
        <button class="copy" type="button" data-text="${esc(c.label + "\\n" + lines.join("\\n"))}">Liste kopieren</button>
        <ul class="plain">${lines.map(l=>`<li>${esc(l)}</li>`).join("")}</ul>`;
    }).join("") + `</section>`;
  out.querySelectorAll(".copy").forEach(b => b.onclick = async () => {
    const t = b.dataset.text;
    try { await navigator.clipboard.writeText(t); }
    catch(e){ const ta=document.createElement("textarea"); ta.value=t; document.body.appendChild(ta); ta.select(); try{document.execCommand("copy");}catch(_){} ta.remove(); }
    b.textContent = "Kopiert ✓"; setTimeout(()=>b.textContent="Liste kopieren",1500);
  });
  empty.hidden = shown > 0;
}
function draw(){
  const term = q.value.split(/\\s+/).map(plain).filter(Boolean);
  let shown = 0;
  if(active==="liste"){ drawListe(term); return; }
  if(active==="alle"){
    const items = P.filter(p => matches(p, term)).sort(byName);
    const title = seg==="alle" ? "Alle Kopfhautprodukte" : (seg==="Drogerie" ? "Alle Drogerie-Kopfhautprodukte" : "Alle High-End-Kopfhautprodukte");
    out.innerHTML = items.length ? `<section class="cat" id="alle">
      <h2>${title}<span class="count">${items.length}</span></h2>
      <ul class="list">${items.map(itemHtml).join("")}</ul>
    </section>` : "";
    empty.hidden = items.length > 0;
    return;
  }
  out.innerHTML = CATS.filter(c => c.id===active).map(c => {
    const items = P.filter(p => p.cats.includes(c.id) && matches(p, term)).sort(byName);
    if(!items.length) return "";
    shown += items.length;
    return `<section class="cat" id="${c.id}">
      <h2>${c.label}<span class="count">${items.length}</span></h2>
      <p class="cat-desc">${c.desc}</p>
      <ul class="list">${items.map(itemHtml).join("")}</ul>
    </section>`;
  }).join("");
  empty.hidden = shown > 0;
}
draw();
</script>
</body>
</html>
'''
open('/home/user/Haar-Quiz/kopfhaut-guide.html', 'w').write(html)
print('ok', len(P), 'Produkte,', len(imgs), 'Bilder; ohne Bild:', [k for k, *_ in P if k not in imgs])
