# Grenzfälle: Name/Werbung und INCI passen nicht zusammen

Automatisch aus klassen.json (classify.py). Schwerpunkte = was in der INCI weit vorne steht.

## Name verspricht Repair, aber keine Repair-Wirkstoffe vor Parfum und Konservierer (30)
- maske: Ida Warg – Repair Hair Mask → nährend
- maske: Herbal Essences – Repair Arganöl Haarmaske → glättend
- maske: Color Wow – Dreaming Advanced Repair Treatment → nährend
- maske: Kérastase – Première Masque Filler Réparateur → glättend
- maske: Wella Professionals – Ultimate Repair Mask → Feuchtigkeit
- maske: L'Oréal Professionnel – Absolut Repair Molecular Mask → Feuchtigkeit, glättend
- maske: Coco & Eve – Bond Building Pre-Shampoo Treatment → Feuchtigkeit, nährend, glättend
- conditioner: Pantene Pro-V – Repair & Care Conditioner → glättend
- conditioner: L'Oréal Paris Elvital – Bond Repair Conditioner → glättend
- conditioner: Herbal Essences – Repair Arganöl Conditioner → glättend
- conditioner: John Frieda – Frizz Ease Wunder-Reparatur Conditioner → Feuchtigkeit, nährend
- conditioner: OGX – Bond Protein Repair Conditioner → Feuchtigkeit
- conditioner: MONDAY – Repair Conditioner → Feuchtigkeit, nährend, glättend
- conditioner: Olaplex – No.5 CURL Bond Shaper Hydrating Curl Conditioner → Feuchtigkeit, nährend
- conditioner: Schwarzkopf Gliss – Ultimate Repair Express-Repair-Kur 7 sec → Feuchtigkeit, nährend
- leavein: Pantene Pro-V – Miracles Molecular Bond Repair Wunder Haarcreme → nährend, glättend
- leavein: L'Oréal Elvital – Leave-In Haarserum Bond Repair → Feuchtigkeit, glättend
- leavein: Garnier Fructis – Haarserum Keratin Sleek & Stay → glättend
- leavein: Jean&Len – Leave-In Haarmaske Peptide Intense Repair → Feuchtigkeit, nährend
- leavein: Bali Curls – Bonding Repair Overnight Elixir No.4 → Feuchtigkeit, nährend
- leavein: Bali Curls – Leave-In Cream Bonding Repair No.3 → nährend
- leavein: John Frieda – Frizz Ease Der Retter Weightless Repair Serum → Feuchtigkeit
- leavein: Schwarzkopf Gliss – Sprüh-Conditioner Express-Repair Aqua Revive → Feuchtigkeit, nährend, glättend
- leavein: OUAI – Leave In Conditioner North Bondi → Feuchtigkeit, glättend
- leavein: OGX – Bond Protein Repair Leave-in Conditioning Mist → Feuchtigkeit
- leavein: L'Oréal Professionnel – Absolut Repair Molecular Leave-In Mask → nährend, glättend
- leavein: Goldwell – Dualsenses Rich Repair 6 Effects Serum → Feuchtigkeit
- leavein: Wella Professionals – Ultimate Repair Miracle Hair Rescue → Feuchtigkeit, glättend
- leavein: Wella Professionals – Ultimate Repair Protective Leave-In → nährend, glättend
- leavein: Wella Professionals – Ultimate Repair Night Serum → nährend, glättend

## Name verspricht Feuchtigkeit, der Schwerpunkt laut INCI liegt woanders (11)
- maske: Garnier Fructis – Locken Methode Feuchtigkeitsauffüllende Maske → nährend; Repair: protein
- maske: Living Proof – Moisture Rescue Mask → nährend
- maske: Oribe – Signature Moisture Masque → nährend, glättend
- conditioner: Herbal Essences – Feuchtigkeit Aloe Vera Conditioner → glättend
- conditioner: Jean&Len – Hydration Pfirsich Chia Conditioner → nährend
- conditioner: Pantene Pro-V – Moisture Boost Conditioner → glättend
- leavein: Aussie – Leave-In Haarserum 100 Hours Hydration → nährend, glättend
- leavein: Pantene Pro-V – Leave-In Moisture Boost Heat & Glow → glättend
- leavein: John Frieda – Frizz Ease Der Beschützer Moisture Protect Serum → nährend, glättend
- leavein: Redken – All Soft Moisture Restore Leave-In → nährend
- leavein: Redken – All Soft Mega Curls Hydramelt → nährend

## Name verspricht Glätte oder Glanz, glättet laut INCI aber nicht stärker als andere (26)
- maske: Garnier Fructis – Keratin Sleek Maske → nährend; Repair: protein
- maske: L'Oréal Elvital – Glycolic Gloss Spiegelglanz Maske → Feuchtigkeit
- maske: Gisou – Honey Gloss Ceramide Therapy Hair Mask → Feuchtigkeit, nährend
- maske: Kérastase – Gloss Absolu Masque Crème Hydra-Glaze → Feuchtigkeit, nährend
- maske: Wella Professionals – Ultimate Smooth Mask → Feuchtigkeit
- conditioner: Langhaarmädchen – Hydrate & Shine Conditioner → Feuchtigkeit
- conditioner: Herbal Essences – Limettenduft Tiefenreinigung & Glanz Conditioner → Feuchtigkeit
- conditioner: John Frieda – Frizz Ease Unendlich Smooth Conditioner → Feuchtigkeit, nährend; Repair: protein
- conditioner: Santé – Glossy Shine Conditioner → Feuchtigkeit, nährend
- conditioner: Balea Professional – Glossy Color Conditioner → Feuchtigkeit, nährend
- conditioner: OGX – Brazilian Keratin Smooth Conditioner → nährend; Repair: protein
- conditioner: NIVEA – Hairmilk Shine Spülung → Feuchtigkeit, nährend
- conditioner: ISANA Professional – Spülung Glycol & Glanz → Feuchtigkeit, nährend
- conditioner: neboa – Repair & Shine Regenerierende Spülung → nährend; Repair: protein
- conditioner: MONDAY – Smooth Antifrizz Conditioner → Feuchtigkeit
- conditioner: Kérastase – Chroma Absolu Soin Acide Chroma Gloss → Feuchtigkeit, nährend
- conditioner: amika – flash instant shine mask → Feuchtigkeit; Repair: protein
- leavein: L'Oréal Elvital – Leave-In Serum Glycolic Gloss Spiegelglanz → nährend
- leavein: Aussie – Leave-In Haarserum Oh My Gloss → Feuchtigkeit, nährend
- leavein: Pomélo+Co – Haarmaske Shine Therapy → Feuchtigkeit
- leavein: Schwarzkopf Gliss – Sprühnebel Night Glanz → Feuchtigkeit
- leavein: Balea – Sprühpflege Seidenglanz 5in1 → Feuchtigkeit
- leavein: Bali Curls – High Shine Gloss Leave-In Cream No.3 → Feuchtigkeit
- leavein: L'Oréal Elvital – Dream Length Dreamy Sleek Serum → Feuchtigkeit, nährend; Repair: protein
- leavein: Goldwell – Dualsenses Just Smooth 6 Effects Serum → Feuchtigkeit
- leavein: Kérastase – Gloss Absolu Frizz-Glaze Cream → Feuchtigkeit, nährend

## Name verspricht Nährendes, Öle und Fette stehen aber nicht weit vorne (12)
- maske: OGX – Coconut Miracle Oil Haarkur → Feuchtigkeit, glättend
- maske: Herbal Essences – Repair Arganöl Haarmaske → glättend
- maske: OGX – Argan Oil of Morocco Extra Strength Hair Mask → Feuchtigkeit, glättend; Repair: protein
- maske: Kérastase – Nutritive Masquintense → Feuchtigkeit, glättend
- maske: Olaplex – Weightless Nourishing Mask → Feuchtigkeit, glättend
- maske: Wella Professionals – Oil Reflections Luminous Reboost Mask → Feuchtigkeit
- conditioner: Herbal Essences – Repair Arganöl Conditioner → glättend
- leavein: Kérastase – Nutritive 8H Magic Night Serum → Feuchtigkeit, glättend
- leavein: Kérastase – Nutritive Nectar Thermique → Feuchtigkeit, glättend
- leavein: Goldwell – Dualsenses Rich Repair 6 Effects Serum → Feuchtigkeit
- leavein: Olaplex – No.9 Bond Protector Nourishing Hair Serum → Feuchtigkeit; Repair: bond
- leavein: Wella Professionals – Ultimate Smooth Miracle Oil Serum → glättend
