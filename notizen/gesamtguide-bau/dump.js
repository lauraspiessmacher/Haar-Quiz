const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});const p=await b.newPage();const out={};
for(const [k,f] of [['shampoo','shampoo-guide'],['leavein','leave-in-guide'],['maske','masken-guide']]){await p.goto('file:///home/user/Haar-Quiz/'+f+'.html');
out[k]=await p.evaluate(()=>({cats:CATS.map(c=>({id:c.id,label:c.label,desc:c.desc})),items:P.map(x=>({s:x.segment,b:x.brand,n:x.name,c:x.cats,no:x.note,h:x.hair||[],t:x.tip||'',r:x.rep||null,si:x.sil||null,he:x.heat||null,i:x.img||''}))}));}
fs.writeFileSync(process.argv[2],JSON.stringify(out));await b.close();})();
