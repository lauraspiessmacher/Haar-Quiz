import sys
import json, re
M=json.load(open('matched.json')); D=json.load(open(sys.argv[1] if len(sys.argv)>1 else '../ux2/data.json'))
def ings(s):
    s=re.sub(r'\(.*?\)','',s); s=re.sub(r'^\s*(ingredients|inhaltsstoffe|inci)\s*:?\s*','',s,flags=re.I)
    s=re.sub(r'denat\.','denat',s,flags=re.I)
    parts=re.split(r'\s*[,•|]\s*|\.\s+(?=[A-Za-z])',s)
    out=[]
    for p in parts:
        p=p.strip().strip('.').split('/')[0].strip().lower()
        if p: out.append(p)
    return out
CUT=re.compile(r'^(parfum|fragrance|perfume|phenoxyethanol|sodium benzoate|potassium sorbate|benzyl alcohol|methylparaben|propylparaben|benzoic acid|sorbic acid|chlorphenesin|methylisothiazolinone|methylchloroisothiazolinone|dmdm hydantoin|ethylhexylglycerin|dehydroacetic acid|sodium dehydroacetate|caprylyl glycol|1,2-hexanediol)')
HUM=re.compile(r'^(glycerin|glycerol|propylene glycol|butylene glycol|propanediol|dipropylene glycol|pentylene glycol|aloe|panthenol|sodium hyaluronate|hyaluronic acid|hydrolyzed hyaluronic acid|betaine|urea|hydroxyethyl urea|sodium pca|pca|honey|mel|sorbitol|glucose|fructose|sucrose|trehalose|inulin|sodium lactate|sodium polyglutamate|polyglutamic|xylitol|lactitol|hydroxypropyltrimonium hyaluronate|glycereth|isopentyldiol|saccharide|beta-glucan|pectin|hydrolyzed corn starch|tremella)')
ESS=re.compile(r'(peel oil|flower oil|leaf oil|bark oil|herb oil|lavandula|pogostemon|juniperus|citrus|mentha|rosmarinus|eucalyptus|cananga|santalum|cedrus|pelargonium|lemongrass|cymbopogon|origanum|salvia)')
EMO=re.compile(r'(oil\b|butter|squalane|squalene|isopropyl myristate|isopropyl palmitate|caprylic/capric triglyceride|caprylic|coco-caprylate|ethylhexyl stearate|ethylhexyl palmitate|dicaprylyl|triethylhexanoin|octyldodecanol|hexyldecanol|cetyl esters|jojoba esters|lanolin|paraffinum|mineral oil|petrolatum|isodecyl oleate|c10-18 triglycerides|oleyl alcohol|isocetyl|myristyl myristate|decyl oleate|glyceryl oleate|ceramide|phytosteryl|shea|cera alba|beeswax|isostearyl|ethylhexyl isononanoate|isononyl isononanoate|c12-15 alkyl benzoate|tridecyl|olive|argan|murumuru|macadamia|avocado|persea)')
PROT=re.compile(r'(hydrolyzed .*protein|hydrolyzed keratin|^keratin|hydrolyzed collagen|hydrolyzed silk|silk amino|amino acids|peptide|^arginine|^serine|^glycine$|^glycine |silanetriol|hydrolyzed .*amino|protein\b|aminopropyl triethoxysilane|hydrolyzed pearl)')
BOND=re.compile(r'(bis-aminopropyl diglycol dimaleate|maleic acid|diethylhexyl maleate|hydroxypropylgluconamide|hydroxypropylammonium gluconate|oligopeptide-78|sh-oligopeptide)')
res={}
for t in ['maske','conditioner','leavein']:
    for p in D[t]['items']:
        key=t+'|'+p['brand']+'|'+p['name']; m=M[key]
        L=ings(m['inci']) if (m['inci'] and m['nameov']>=0.6) else []
        cut=next((i for i,x in enumerate(L) if CUT.match(x)),len(L))
        w=lambda i: (1.0/(1+0.35*i)) if i<cut else 0.04
        H=sum(w(i) for i,x in enumerate(L) if HUM.match(x))
        E=sum(w(i) for i,x in enumerate(L) if EMO.search(x) and not ESS.search(x))
        prot=[x for i,x in enumerate(L) if i<cut and PROT.search(x)]
        bond=[x for i,x in enumerate(L) if i<cut and BOND.search(x)]
        rep_curated=json.dumps(p.get('rep'),ensure_ascii=False) if p.get('rep') else ''
        if 'bond' in rep_curated.lower() and not bond and 'Zitronens' in rep_curated: bond=['citric acid (Bond laut Marke)']
        hum_top=[x for i,x in enumerate(L) if i<cut and HUM.match(x)][:3]
        emo_top=[x for i,x in enumerate(L) if i<cut and EMO.search(x) and not ESS.search(x)][:3]
        if not L: kind='?'
        elif E>=0.18 and E>=H*0.9: kind='naehrend'
        elif H>=0.18: kind='feucht'
        elif E>=0.12: kind='naehrend'
        else: kind='glaettend'
        rep='bond' if bond else ('protein' if prot else '')
        res[key]={'type':t,'brand':p['brand'],'name':p['name'],'cats':p['cats'],'segment':p['segment'],'kind':kind,'rep':rep,'H':round(H,2),'E':round(E,2),'hum':hum_top,'emo':emo_top,'prot':prot[:3],'bond':bond[:2],'note':p['note'],'inci_ok':bool(L)}
# Handkorrekturen ohne INCI in den Notizen
res['maske|Olaplex|Rich Hydration Mask'].update(kind='naehrend',rep='',emo=['avocado oil','shea butter','coconut oil'],note2='INCI online (Cosmeterie/John Beerens); Bond-Wirkstoff erst hinter Parfum')
res['maske|Olaplex|Weightless Nourishing Mask'].update(kind='feucht',rep='',hum=['glycerin','panthenol','sodium hyaluronate'],note2='INCI online (Liberty/Galaxus); Bond-Wirkstoff erst hinter Parfum')
for k,v in res.items():
    if 'kaputt' in v['cats'] and not v['rep'] and re.search(r'bond',v['name'],re.I): v.update(rep='bond',bond=['Bond-Komplex laut Marke'])
json.dump(res,open('klassen.json','w'),ensure_ascii=False,indent=1)
import collections
for t in ['maske','conditioner','leavein']:
    print(t,collections.Counter(v['kind'] for v in res.values() if v['type']==t),collections.Counter(v['rep'] for v in res.values() if v['type']==t))
