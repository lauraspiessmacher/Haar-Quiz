// Baut die Prüfseite für den Routine-Check aus quiz-routine.html.
// Alle Texte kommen direkt aus dem Quiz, damit die Prüfseite immer zum Quiz passt.
// Aufruf: node gen.js   → schreibt ../pruefseite.html
const fs = require("fs"), path = require("path");
const ROOT = path.resolve(__dirname, "../../..");
const html = fs.readFileSync(path.join(ROOT, "quiz-routine.html"), "utf8");
const cut = (a, b) => { const i = html.indexOf(a), j = html.indexOf(b, i); if (i < 0 || j < 0) throw new Error("Marke fehlt: " + a); return html.slice(i, j); };

const code = cut("const TAGE = ", "/* ---------- Ablauf ---------- */") + cut("/* ---------- Regeln ---------- */", "/* ---------- Ergebnis ---------- */");
const Q_ = new Function(code + "\nreturn {TAGE,Q,FINE,DICKE,plan};")();
const { Q, FINE, DICKE, plan } = Q_;

const strip = s => s.replace(/<[^>]+>/g, "").replace(/\s+/g, " ").trim();
const grab = (re) => { const m = html.match(re); if (!m) throw new Error("Text fehlt: " + re); return strip(m[1]); };

/* ---------- Bausteine ---------- */
const BASE = { kopf: "normal", dicke: "normal", struktur: "glatt", wunsch: "gesund", laenge: "schulter", chem: ["nichts"], zustand: "weich", spliss: "kaum", wash: "2", sport: "nein", styling: "kaum", hitze: "selten", schlaf: ["offen"], aufwand: "mittel" };
const P = o => plan(Object.assign({}, BASE, o));
const sec = (R, h) => { const s = R.T.find(x => x.h === h); if (!s) throw new Error("Abschnitt fehlt: " + h); return s; };
const DL = ["Fein", "Dünn", "Normal", "Dick", "Sehr dick"];
const KL = { normal: "Unkompliziert", fettend: "Fettet schnell", trocken: "Trocken", sensibel: "Sensibel", schuppen: "Schuppig" };

const M = [];
let gruppe = "";
const G = g => { gruppe = g; };
/* text: String oder Liste von [Variante, Text]; gleiche Varianten werden zusammengefasst */
function add(id, wann, text) {
  if (Array.isArray(text)) {
    const uniq = [];
    for (const [l, t] of text) { const u = uniq.find(x => x[1] === t); if (u) u[0] += ", " + l; else uniq.push([l, t]); }
    text = uniq.length === 1 ? uniq[0][1] : uniq;
  }
  M.push({ id, gruppe, wann, text });
}
const byDicke = f => DICKE.map((d, i) => [DL[i], f(d, i)]);

G("Rahmen");
add("start", "Startseite des Quiz", grab(/<p class="lead">([\s\S]*?)<\/p>/));
add("start_tipp", "Startseite, wenn noch nicht alle drei anderen Quizze gemacht sind", "Tipp: Mach zuerst die anderen drei Quizze. " + grab(/missing \? `<p class="hint"[^>]*>([\s\S]*?)<\/p>`/));
add("intro", "Ganz oben im Ergebnis", grab(/<p class="intro">([\s\S]*?)<\/p>/));
add("produkte", "Kasten „Welche Produkte?“ unten im Ergebnis", grab(/<h3>Welche Produkte\?<\/h3><p>([\s\S]*?)<\/p>/));
add("fine", "Kleingedrucktes auf Start- und Ergebnisseite", FINE);

G("Deine Basis (immer)");
add("basis_intro", "Immer", sec(P({}), "Deine Basis").p[0]);
["basis_leave", "basis_ll", "basis_hitze", "basis_oel", "basis_cond"].forEach((id, k) =>
  add(id, "Immer, Wortlaut je nach Haardicke", byDicke(d => sec(P({ dicke: d }), "Deine Basis").li[k])));

G("Deine Waschtage");
add("wasch_tage", "Immer, Tage und Anzahl ändern sich", [
  ["Beispiel: 2× waschen, kein Sport", sec(P({}), "Deine Waschtage").p[0]],
  ["Beispiel: 3× waschen, Sport Di und Do", sec(P({ wash: "3", sport: "ruhig", sporttage: ["1", "3"] }), "Deine Waschtage").p[0]],
  ["Beispiel: 1× waschen", sec(P({ wash: "1" }), "Deine Waschtage").p[0]]]);
add("maske", "Immer, Zusatz je nach Haardicke (die Anzahl ändert sich, siehe Tabelle unten)", byDicke(d => sec(P({ dicke: d }), "Deine Waschtage").p[1]));
add("maske_wenig", "Bei wenig Aufwand, wenn eigentlich mehr Masken gingen (Beispiel: dicke Haare, 4× waschen)", sec(P({ dicke: "dick", wash: "4", aufwand: "wenig" }), "Deine Waschtage").p[1].split("fuzzy aussieht.").pop().trim());
{
  const row = (o) => DICKE.map((d, i) => [DL[i], ["1", "2", "3", "4", "5"].map(w => P(Object.assign({ dicke: d, wash: w }, o)).chips[1].replace(" Maske", "")).join(" · ")]);
  add("maske_tabelle", "So viele Masken pro Woche schlägt das Quiz vor. Werte für 1 · 2 · 3 · 4 · 5 Wäschen pro Woche, mittlerer Aufwand", [
    ...row({}).map(([l, t]) => ["Gesund, " + l, t]),
    ...row({ chem: ["gefaerbt"], zustand: "trocken", hitze: "manchmal" }).map(([l, t]) => ["Beansprucht (z. B. gefärbt, etwas trocken), " + l, t]),
    ...row({ chem: ["blond"], zustand: "strohig" }).map(([l, t]) => ["Stark geschädigt (blondiert, strohig), " + l, t])]);
}
add("prewash", "Nur bei „Viel, ich liebe Haarpflege“", byDicke(d => sec(P({ dicke: d, aufwand: "viel" }), "Deine Waschtage").p.find(x => x.startsWith("**Pre-Wash"))));

G("Zwischen den Wäschen");
add("ts", "Je nach Kopfhaut (bei bis zu 4 Wäschen pro Woche)", Object.keys(KL).map(k => [KL[k], sec(P({ kopf: k }), "Zwischen den Wäschen").p[0]]));
add("ts_styling", "Unkomplizierte Kopfhaut und Styling-Produkte „ab und zu“ oder „fast täglich“", sec(P({ styling: "manchmal" }), "Zwischen den Wäschen").p[0]);
add("tief", "Immer, je nach Styling und Kopfhaut", [
  ["Kaum Styling, unkomplizierte Kopfhaut", sec(P({ wash: "5" }), "Zwischen den Wäschen").p[1]],
  ["Styling ab und zu", sec(P({ styling: "manchmal", wash: "5" }), "Zwischen den Wäschen").p[1]],
  ["Styling fast täglich", sec(P({ styling: "viel", wash: "5" }), "Zwischen den Wäschen").p[1]],
  ["Styling fast täglich und fettende Kopfhaut", sec(P({ styling: "viel", kopf: "fettend", wash: "5" }), "Zwischen den Wäschen").p[1]]]);

G("Beim Sport");
add("sport", "Nur wenn Sport angegeben ist", [
  ["Viel Bewegung", sec(P({ sport: "viel", sporttage: ["0"] }), "Beim Sport").p[0]],
  ["Ruhiger Sport", sec(P({ sport: "ruhig", sporttage: ["0"] }), "Beim Sport").p[0]],
  ["Schuppige Kopfhaut und Sport an einem Tag ohne Wäsche", sec(P({ sport: "ruhig", sporttage: ["2"], kopf: "schuppen" }), "Beim Sport").p[0]]]);

G("Hitze und Hitzeschutz");
add("hitze", "Immer", sec(P({}), "Hitze und Hitzeschutz").p[0]);
add("hitze_taeglich", "Bei „fast täglich“ Hitze", sec(P({ hitze: "taeglich" }), "Hitze und Hitzeschutz").p[1]);
add("hitze_fuerdich", "Immer, je nach Haardicke", byDicke(d => sec(P({ dicke: d }), "Hitze und Hitzeschutz").p.slice(-1)[0]));
{ const m = html.match(/<summary>Welcher Hitzeschutz passt zu wem\?<\/summary><div class="inner">([\s\S]*?)<\/div><\/details>/);
  const items = [...m[1].matchAll(/<li>([\s\S]*?)<\/li>/g)].map(x => x[1].replace(/<strong>([\s\S]*?)<\/strong>/g, "**$1**").replace(/<[^>]+>/g, "").replace(/\s+/g, " ").trim());
  add("hitze_details", "Zum Aufklappen unter „Hitze und Hitzeschutz“", items.map((t, k) => ["Punkt " + (k + 1), t])); }

G("Trocknen");
add("trocknen", "Immer, Zusatz bei Locken je nach Kopfhaut", [
  ["Glatt oder wellig", sec(P({}), "Trocknen").p[0]],
  ...Object.keys(KL).map(k => ["Lockig, Kopfhaut " + KL[k].toLowerCase(), sec(P({ struktur: "lockig", kopf: k }), "Trocknen").p[0]])]);

G("Nachts");
add("nachts", "Je nach Antwort zum Schlafen", [
  ["Offen", sec(P({ schlaf: ["offen"] }), "Nachts").p[0]],
  ["Offen, mit Seidenkissen", sec(P({ schlaf: ["offen", "kissen"] }), "Nachts").p[0]],
  ["Dutt oder Pferdeschwanz", sec(P({ schlaf: ["zopf"] }), "Nachts").p[0]],
  ["Dutt oder Pferdeschwanz, mit Seidenkissen", sec(P({ schlaf: ["zopf", "kissen"] }), "Nachts").p[0]],
  ["Geflochten", sec(P({ schlaf: ["flecht"] }), "Nachts").p[0]],
  ["Geflochten, mit Seidenkissen", sec(P({ schlaf: ["flecht", "kissen"] }), "Nachts").p[0]],
  ["Seidenhaube", sec(P({ schlaf: ["haube"] }), "Nachts").p[0]]]);

G("Repair ist nicht gleich Repair");
const RP = o => sec(P(o), "Repair ist nicht gleich Repair");
add("repair_intro", "Nur bei Färben, Blondieren, Chemie, fast täglicher Hitze oder viel Haarbruch. Nur bei trockenen Längen erscheint der Abschnitt nicht.", [
  ["Blondiert, chemisch behandelt oder nass wie Gummi", RP({ chem: ["blond"] }).p[0]],
  ["Gefärbt", RP({ chem: ["gefaerbt"] }).p[0]],
  ["Fast täglich Hitze", RP({ hitze: "taeglich" }).p[0]],
  ["Gefärbt und fast täglich Hitze", RP({ chem: ["gefaerbt"], hitze: "taeglich" }).p[0]],
  ["Gefärbt und viel Haarbruch", RP({ chem: ["gefaerbt"], spliss: "bruch" }).p[0]],
  ["Nur viel Haarbruch", RP({ spliss: "bruch" }).p[0]]]);
add("repair_stufen", "Gleich danach", RP({ chem: ["gefaerbt"] }).p[1]);
RP({ chem: ["gefaerbt"] }).li.forEach((t, k) => add("repair_li" + k, "Liste im Repair-Abschnitt", t));

G("Dein Wunschergebnis");
const WS = (o, h) => sec(P(o), h).p.join(" ");
add("wunsch_glatt", "Nur bei Wunsch „glatt und glänzend“", [
  ["Glatte Haare", WS({ wunsch: "glatt", struktur: "glatt" }, "Dein Wunsch: glatt und glänzend")],
  ["Wellige Haare", WS({ wunsch: "glatt", struktur: "wellig" }, "Dein Wunsch: glatt und glänzend")],
  ["Lockige Haare", WS({ wunsch: "glatt", struktur: "lockig" }, "Dein Wunsch: glatt und glänzend")]]);
add("wunsch_volumen", "Nur bei Wunsch „mehr Volumen“", [
  ["Feine oder dünne Haare", WS({ wunsch: "volumen", dicke: "fein" }, "Dein Wunsch: mehr Volumen")],
  ["Normale Haare", WS({ wunsch: "volumen", dicke: "normal" }, "Dein Wunsch: mehr Volumen")],
  ["Dicke Haare", WS({ wunsch: "volumen", dicke: "dick" }, "Dein Wunsch: mehr Volumen")]]);
add("wunsch_locken", "Nur bei Wunsch „definierte Wellen oder Locken“", [
  ["Glatte Haare", WS({ wunsch: "locken", struktur: "glatt" }, "Dein Wunsch: Wellen oder Locken")],
  ["Wellig, wenig Aufwand", WS({ wunsch: "locken", struktur: "wellig", aufwand: "wenig" }, "Dein Wunsch: definierte Wellen")],
  ["Lockig, normale Haardicke, mittlerer oder viel Aufwand", WS({ wunsch: "locken", struktur: "lockig", aufwand: "viel" }, "Dein Wunsch: definierte Locken")],
  ["Lockig, dicke Haare, mittlerer oder viel Aufwand", WS({ wunsch: "locken", struktur: "lockig", dicke: "dick", aufwand: "viel" }, "Dein Wunsch: definierte Locken")]]);

G("Weitere Abschnitte");
add("gummi", "Nur bei „nass wie Gummi“, ganz oben als Warnung", P({ zustand: "gummi" }).T[0].p[0]);
add("spliss", "Bei Spliss oder Haarbruch", [
  ["Spliss", sec(P({ spliss: "spliss" }), "Spliss lässt sich nicht reparieren").p[0]],
  ["Viel Haarbruch", sec(P({ spliss: "bruch" }), "Spliss lässt sich nicht reparieren").p[0]]]);
add("lang", "Ab Brustlänge", sec(P({ laenge: "brust" }), "Lange Haare").p[0]);
add("klappt", "Immer, ganz unten", sec(P({}), "Wenn es mal nicht klappt").p[0]);

/* Zeilen im Wochenplan und in „Regelmäßig“: über viele Antwort-Kombinationen einsammeln */
const pick = a => a[Math.floor(Math.random() * a.length)];
const OPT = id => Q.find(q => q.id === id).a.map(x => x[1]);
const weekItems = new Map(), regelItems = new Map();
for (let i = 0; i < 6000; i++) {
  const a = {}; for (const q of Q) { if (q.multi) { const o = OPT(q.id).filter(x => x !== "nichts"); a[q.id] = o.filter(() => Math.random() < .35); if (!a[q.id].length) a[q.id] = [pick(OPT(q.id))]; } else a[q.id] = pick(OPT(q.id)); }
  const R = plan(a);
  R.week.forEach(d => d.items.forEach(t => weekItems.set(t, (weekItems.get(t) || 0) + 1)));
  R.regel.forEach(([w, t]) => (w === "Jede Woche" ? t.split(/(?<=\.) /) : [t]).forEach(x => regelItems.set(w + ": " + x, 1)));
}
G("Zeilen im Wochenplan");
const wi = [...weekItems.keys()].sort((x, y) => x.localeCompare(y, "de"));
add("woche_zeilen", "Diese Zeilen können in der Tabelle „Deine Woche“ stehen (alle Varianten)", wi.map((t, k) => ["Zeile " + (k + 1), t]));
G("Tabelle „Regelmäßig“");
const ri = [...regelItems.keys()].sort((x, y) => x.localeCompare(y, "de"));
add("regel_zeilen", "Diese Zeilen können in der Tabelle „Regelmäßig“ stehen. Bei „Jede Woche“ werden die passenden Sätze hintereinander gesetzt.", ri.map((t, k) => ["Zeile " + (k + 1), t]));

/* ---------- Fragen ---------- */
const FR = Q.map(q => ({ id: "frage_" + q.id, t: q.t, h: q.h || "", a: q.a.map(x => x[0]), multi: !!q.multi, wann: q.if ? "Nur wenn Sport angegeben ist" : "" }));

/* ---------- Beispiel-Ergebnisse ---------- */
const PERS = [
  ["Feine Haare, wenig Zeit", "Fettende Kopfhaut, fein, glatt, schulterlang, nicht gefärbt, etwas trocken, 4× waschen, kein Sport, Styling ab und zu, Hitze 1–2× pro Woche, schläft offen, wenig Aufwand",
    { kopf: "fettend", dicke: "fein", struktur: "glatt", laenge: "schulter", chem: ["nichts"], zustand: "trocken", spliss: "kaum", wash: "4", sport: "nein", styling: "manchmal", hitze: "manchmal", schlaf: ["offen"], aufwand: "wenig" }],
  ["Dicke, blondierte Haare, wäscht fast täglich", "Unkomplizierte Kopfhaut, dick, wellig, lang, blondiert, strohig, Spliss, 5× waschen, ruhiger Sport Mo/Mi/Fr, kaum Styling, fast täglich Hitze, Dutt und Seidenkissen, viel Aufwand",
    { kopf: "normal", dicke: "dick", struktur: "wellig", laenge: "lang", chem: ["blond"], zustand: "strohig", spliss: "spliss", wash: "5", sport: "ruhig", sporttage: ["0", "2", "4"], styling: "kaum", hitze: "taeglich", schlaf: ["zopf", "kissen"], aufwand: "viel" }],
  ["Locken mit viel Sport", "Sensible Kopfhaut, normal dick, lockig, brustlang, nicht gefärbt, etwas trocken, 2× waschen, viel Sport Di/Do/Sa, viel Styling, selten Hitze, Seidenhaube, mittlerer Aufwand",
    { kopf: "sensibel", dicke: "normal", struktur: "lockig", laenge: "brust", chem: ["nichts"], zustand: "trocken", spliss: "kaum", wash: "2", sport: "viel", sporttage: ["1", "3", "5"], styling: "viel", hitze: "selten", schlaf: ["haube"], aufwand: "mittel" }],
  ["Haarbruch ohne Färben und Hitze", "Trockene Kopfhaut, dünn, glatt, brustlang, nicht gefärbt, etwas trocken, viel Haarbruch, 3× waschen, kein Sport, kaum Styling, selten Hitze, offen mit Seidenkissen, mittlerer Aufwand",
    { kopf: "trocken", dicke: "duenn", struktur: "glatt", laenge: "brust", chem: ["nichts"], zustand: "trocken", spliss: "bruch", wash: "3", sport: "nein", styling: "kaum", hitze: "selten", schlaf: ["offen", "kissen"], aufwand: "mittel" }],
  ["Nass wie Gummi, schuppige Kopfhaut", "Schuppige Kopfhaut, normal dick, glatt, schulterlang, gefärbt und blondiert, nass wie Gummi, viel Haarbruch, 2× waschen, ruhiger Sport So, Styling ab und zu, Hitze 1–2× pro Woche, geflochten, wenig Aufwand",
    { kopf: "schuppen", dicke: "normal", struktur: "glatt", laenge: "schulter", chem: ["gefaerbt", "blond"], zustand: "gummi", spliss: "bruch", wash: "2", sport: "ruhig", sporttage: ["6"], styling: "manchmal", hitze: "manchmal", schlaf: ["flecht"], aufwand: "wenig" }]
].map(([name, wer, a], k) => { const R = plan(a); return { id: "beispiel_" + (k + 1), name, wer, T: R.T, week: R.week, regel: R.regel, chips: R.chips }; });

const DATA = { stand: new Date().toISOString().slice(0, 10), bausteine: M, fragen: FR, beispiele: PERS };
const tpl = fs.readFileSync(path.join(__dirname, "vorlage.html"), "utf8");
fs.writeFileSync(path.join(__dirname, "..", "pruefseite.html"), tpl.replace("__DATA__", JSON.stringify(DATA).replace(/</g, "\\u003c")));
console.log("ok", M.length, "Bausteine,", FR.length, "Fragen,", PERS.length, "Beispiele,", wi.length, "Wochenzeilen,", ri.length, "Regelzeilen");
