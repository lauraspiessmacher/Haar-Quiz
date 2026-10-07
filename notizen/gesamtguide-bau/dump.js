// Liest alle Einzel-Guides aus (CATS, P, Bilder) und schreibt sie als eine JSON-Datei.
const {chromium}=require('playwright');const fs=require('fs');
const GUIDES=[['shampoo','shampoo-guide'],['maske','masken-guide'],['conditioner','conditioner-guide'],['leavein','leave-in-guide'],['oel','oel-guide'],['kopfhaut','kopfhaut-guide']];
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});const p=await b.newPage();const out={};
for(const [k,f] of GUIDES){await p.goto('file:///home/user/Haar-Quiz/'+f+'.html');
 out[k]=await p.evaluate(()=>({
  cats:CATS.map(c=>({id:c.id,label:c.label,desc:c.desc})),
  rank:(typeof RANK!=='undefined')?RANK:null,
  intro:{lead:(document.querySelector('.lead')||{}).innerHTML||'',how:(document.querySelector('.how')||{}).innerHTML||'',box:(document.querySelector('.box')||{}).innerHTML||''},
  items:P.map(x=>{const o={};for(const [kk,v] of Object.entries(x)){if(v!==undefined&&v!==null&&v!==''&&!(Array.isArray(v)&&!v.length))o[kk]=v;}return o;})}));}
fs.writeFileSync(process.argv[2],JSON.stringify(out));await b.close();})();
