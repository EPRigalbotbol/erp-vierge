# -*- coding: utf-8 -*-
import json
from build_crm import coquille
import _donnees
C=json.load(open('cat.json'))
IDX={r[15]:[r[0],r[13],r[2],r[12],r[6],r[8],r[7]] for r in C}   # bc,nom,marque,pa,qte,pvw,pvr

CSS = r'''
.sous{margin:5px 0 0;font-size:14px;color:var(--ink-2);max-width:74ch;line-height:1.5}
.blocs{display:flex;flex-direction:column;gap:16px;max-width:900px}

/* Refonte du 25 oct. 2026 (Igal : « mal organisé, pas clair, pas du tout compréhensible »).
   Cinq onglets, un seul visible à la fois ; dans chacun, UNE ligne par réglage : son nom,
   une phrase, la case. Les explications longues et les exemples passent derrière un « ? ».
   Les identifiants des champs ne bougent pas : le code qui les lit ne change pas. */
.ong{display:flex;flex-wrap:wrap;gap:6px;margin:0 0 18px;border-bottom:1px solid var(--line);padding-bottom:0}
.ong button{display:flex;align-items:center;gap:8px;font:inherit;font-size:13.5px;font-weight:600;color:var(--ink-2);
background:none;border:0;border-bottom:3px solid transparent;border-radius:0;padding:9px 14px 10px;cursor:pointer;margin-bottom:-1px}
.ong button .ic{font-size:15px}
.ong button:hover{color:var(--ink)}
.ong button.on{color:var(--iris);border-bottom-color:var(--iris)}
.pan[hidden]{display:none}
.pan-sous{margin:0 0 14px;font-size:13.5px;color:var(--ink-3);max-width:74ch;line-height:1.5}

.rg{background:var(--surface);border:1px solid var(--line);border-radius:11px;padding:6px 20px;display:flex;flex-direction:column}
.rg > h3{margin:14px 0 4px;font-size:12px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--ink-3);
display:flex;align-items:center;gap:10px}
.rg > h3 .q{margin-left:0}
.lg{display:grid;grid-template-columns:minmax(0,1fr) auto 30px;align-items:center;gap:8px 16px;padding:12px 0}
.lg + .lg{border-top:1px solid var(--line-2)}
.rg > .plus{margin:4px 0 10px}
.lg .une:empty{display:none}
.lg .nm2{font-size:14px;font-weight:600;color:var(--ink);line-height:1.35}
.lg .une{display:block;font-size:12.5px;font-weight:400;color:var(--ink-3);line-height:1.45;margin-top:2px;max-width:60ch}
.lg .ctl{display:flex;align-items:center;gap:8px;flex-wrap:wrap;justify-content:flex-end;font-size:13.5px;color:var(--ink-2)}
.lg .ctl b{font-weight:600;color:var(--ink)}
.lg input[type=number]{width:78px;padding:8px 9px;font-family:inherit;font-size:15px;font-weight:700;
text-align:center;border:1px solid var(--line);border-radius:7px;background:var(--surface-2);
color:var(--ink);-moz-appearance:textfield}
.lg input::-webkit-outer-spin-button,.lg input::-webkit-inner-spin-button{-webkit-appearance:none;margin:0}
.lg input[type=text],.lg input[type=date],.lg select{padding:8px 10px;font-family:inherit;font-size:14px;
border:1px solid var(--line);border-radius:7px;background:var(--surface-2);color:var(--ink);width:300px;max-width:100%}
.lg input:hover,.lg select:hover{border-color:var(--ink-3)}
.lg input:focus,.lg select:focus{outline:0;border-color:var(--iris);box-shadow:0 0 0 3px var(--iris-soft);background:var(--surface)}
.lg input[type=checkbox]{width:20px;height:20px;accent-color:var(--iris);cursor:pointer}
.lg .etat{grid-column:1;font-size:12.5px;color:var(--ink-3);line-height:1.5;margin-top:-6px}
.lg .etat b{color:var(--ink);font-weight:700}
.lg .etat:empty{display:none}
.lg .etat .pt{display:inline-block;width:8px;height:8px;border-radius:50%;background:var(--line);margin-right:7px;vertical-align:1px}
.lg .etat .pt.bon{background:var(--good)} .lg .etat .pt.bof{background:var(--warn)} .lg .etat .pt.non{background:var(--crit)}
.plus .eff{margin-top:2px}
.can caption{caption-side:bottom;text-align:left;font-size:12.5px;color:var(--ink-3);padding:8px 0 0;line-height:1.5}
.lg .plus{grid-column:1/-1}
.lg .plus[hidden]{display:none}
.q{width:26px;height:26px;border-radius:50%;border:1px solid var(--line);background:var(--surface-2);color:var(--ink-3);
font:700 13px/1 Inter,sans-serif;cursor:pointer;display:inline-flex;align-items:center;justify-content:center;flex:none;
transition:background .12s,color .12s,border-color .12s}
.q:hover,.q[aria-expanded=true]{background:var(--iris);color:#fff;border-color:var(--iris)}
.plus{font-size:13px;color:var(--ink-2);line-height:1.6;background:var(--surface-2);border-radius:8px;padding:12px 15px;
display:flex;flex-direction:column;gap:8px}
.plus p{margin:0;max-width:72ch}
.plus b{color:var(--ink)}
.lg.large{grid-template-columns:minmax(0,1fr) 30px}
.lg.large .ctl{grid-column:1/-1;justify-content:flex-start}

.logoz{display:flex;gap:16px;align-items:flex-start;flex-wrap:wrap}
.logoap{flex:none;width:150px;height:104px;border:1px dashed var(--line);border-radius:10px;
background:#fff;display:flex;align-items:center;justify-content:center;color:var(--ink-3);
font-size:11.5px;text-align:center;padding:8px;overflow:hidden}
.logoap img{max-width:100%;max-height:88px;object-fit:contain}
.logoz .aide{display:block;max-width:52ch;margin-top:7px;font-size:12px;color:var(--ink-3);line-height:1.5}
.eff{font-size:12.5px;line-height:1.55;border-radius:8px;padding:9px 12px;background:var(--surface-2);color:var(--ink-2)}
.eff b{color:var(--ink);font-weight:700}
.eff.bon{background:var(--good-soft);color:var(--good)}
.eff.bof{background:var(--warn-soft);color:var(--warn)}
.eff.non{background:var(--crit-soft);color:var(--crit)}
.jauge{height:6px;border-radius:5px;background:var(--line-2);overflow:hidden;margin-top:8px}
.jauge div{height:100%;background:var(--iris);transition:width .2s}
.jauge div.bof{background:var(--warn)} .jauge div.non{background:var(--crit)}
.exs{list-style:none;margin:8px 0 0;padding:0;display:flex;flex-direction:column;gap:1px;
background:var(--line);border:1px solid var(--line);border-radius:8px;overflow:hidden}
.exs li{background:var(--surface);padding:7px 12px;display:flex;align-items:baseline;gap:11px;font-size:12.5px}
.exs .n{margin-left:auto;font-weight:700;font-variant-numeric:tabular-nums;white-space:nowrap}
.exs .mq{font-size:11px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:var(--iris);white-space:nowrap}
.exs .nm{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.can{width:100%;border-collapse:collapse;font-size:13.5px;margin:4px 0 10px}
.can th{text-align:left;font-family:Inter,sans-serif;font-size:9.5px;letter-spacing:.11em;text-transform:uppercase;
color:var(--ink-2);font-weight:700;padding:6px 8px;border-bottom:1px solid var(--line)}
.can th.r,.can td.r{text-align:right}
.can td{padding:7px 8px;border-bottom:1px solid var(--line-2);vertical-align:middle}
.can .bs{font-size:12px;color:var(--ink-3);font-family:Inter,sans-serif}
.can input[type=text]{width:100%;min-width:150px;padding:7px 9px;font-family:inherit;font-size:13.5px;font-weight:600;
border:1px solid var(--line);border-radius:7px;background:var(--surface-2);color:var(--ink)}
.can input[type=number]{width:70px;padding:7px 8px;font-family:inherit;font-size:14px;font-weight:700;text-align:center;
border:1px solid var(--line);border-radius:7px;background:var(--surface-2);color:var(--ink);-moz-appearance:textfield}
.can input:focus{outline:0;border-color:var(--iris);box-shadow:0 0 0 3px var(--iris-soft);background:var(--surface)}
.can .ex{font-family:Inter,sans-serif;font-variant-numeric:tabular-nums;color:var(--ink-2);white-space:nowrap}
.can .ex b{color:var(--ink)}
.can .x{background:none;border:0;color:var(--ink-3);font-size:18px;cursor:pointer;padding:2px 6px;line-height:1}
.can .x:hover{color:var(--crit)}
.pied{display:flex;gap:11px;align-items:center;flex-wrap:wrap;margin-top:6px}
.pied .msg{font-size:13px;color:var(--good);font-weight:600}
.agit{display:flex;flex-wrap:wrap;align-items:center;gap:7px}
.agit .lbl{font-size:11px;font-weight:700;letter-spacing:.05em;text-transform:uppercase;color:var(--ink-3)}
.agit .rb{font-size:11.5px;font-weight:600;color:var(--iris);background:var(--iris-soft);border-radius:99px;padding:3px 10px;white-space:nowrap}
@media (max-width:640px){.lg{grid-template-columns:minmax(0,1fr) 30px}.lg .ctl{grid-column:1/-1;justify-content:flex-start}
.lg input[type=text],.lg input[type=date],.lg select{width:100%}}
'''

# Une ligne de réglage : nom + phrase à gauche, la case à droite, le « ? » au bout.
# `plus` = ce qu'on lit en appuyant sur « ? » ; `etat` = la ligne d'effet que le JS remplit.
def ligne(nom, une, ctl, plus='', etat_id='', sid='', large=False, extra=''):
    q = '<button class="q" type="button" aria-expanded="false" title="Explications">?</button>' if plus else '<span></span>'
    etat = f'<div class="etat" id="{etat_id}"></div>' if etat_id else ''
    plusb = f'<div class="plus" hidden>{plus}</div>' if plus else ''
    return (f'<div class="lg{" large" if large else ""}"{(" id=" + chr(34) + sid + chr(34)) if sid else ""}>'
            f'<div class="nm2">{nom}<span class="une">{une}</span></div>'
            f'<div class="ctl">{ctl}</div>{q}{extra}{etat}{plusb}</div>')

def agit(*rb):
    return '<div class="agit"><span class="lbl">agit sur</span>' + ''.join(f'<span class="rb">{r}</span>' for r in rb) + '</div>'

def texte(id_, ph='', w=300, bold=False):
    return f'<input type="text" id="{id_}"{(" placeholder=" + chr(34) + ph + chr(34)) if ph else ""} style="width:{w}px{";font-weight:600" if bold else ""}">'

def coche(id_, lib):
    return f'<label style="display:flex;gap:10px;align-items:center;cursor:pointer;font-weight:600"><input type="checkbox" id="{id_}">{lib}</label>'

def logo(pfx, aide):
    return (f'<div class="logoz"><div class="logoap" id="{pfx}-logoap">aucun logo</div><div>'
            f'<input type="file" id="{pfx}-logofic" accept="image/png,image/jpeg,image/webp,image/svg+xml" hidden>'
            f'<button class="btn" id="{pfx}-logobtn">Choisir une image…</button> '
            f'<button class="btn" id="{pfx}-logosup" hidden>Retirer</button>'
            f'<span class="aide" id="{pfx}-logoaide">{aide}</span></div></div>')

# 25 oct. 2026 (Igal) : « la commission me suffit, je ne vois pas l'intérêt de la majoration » — la colonne
# disparaît et la valeur passe à 0 (le prix Amazon vient de l'annonce, le prix Perfume City de Shopify,
# les sites sont à 0 %). « Ou alors rajouter le coût du transport » : l'envoi entre dans le tableau.
P_CANAUX = ('<p><b>Commission</b> : ce que la plateforme garde sur chaque vente. Elle sert à calculer la marge '
  'nette réellement encaissée sur ce canal, et le plancher sous lequel un prix est refusé '
  '(prix d\'achat + seuil de marge, commission comprise).</p>'
  '<p><b>Envoi</b> : ce qu\'un colis coûte à Sam, par commande, sur chaque canal qui expédie. Il est retiré de la '
  'marge de la commande ; le port payé par le client sur le site, lui, y est ajouté. Vide = 8 $.</p>'
  '<p>Sites, Amazon, Perfume City… ce que tu vends réellement.</p>'
  + agit('Catalogue — case de prix par canal', 'Ventes — marge nette et commission « Par canal »'))

CORPS = r'''
<div class="ong" id="ong">
  <button type="button" class="on" data-t="soc"><span class="ic">🏢</span> Ma société</button>
  <button type="button" data-t="pc"><span class="ic">🛍️</span> <span data-nolang>Perfume City</span></button>
  <button type="button" data-t="prix"><span class="ic">💲</span> Prix et canaux</button>
  <button type="button" data-t="stock"><span class="ic">📦</span> Stock</button>
  <button type="button" data-t="caisse"><span class="ic">💵</span> Caisse</button>
</div>

<div class="pan" id="pan-soc">
<p class="pan-sous">Ce qui est imprimé sur chaque document envoyé à un client ou à un fournisseur, et ce que le bouton « Écrire » utilise.</p>
<div class="blocs">
<section class="rg">
''' + ligne('Ma société', 'Nom tel qu\'il apparaît sur les factures', texte('r-soc', w=260, bold=True),
            '<p>Le nom de ta société : il figure toujours sur tes factures, il ne faut pas le confondre avec le nom du fournisseur ou du client.</p>'
            + agit('Factures &amp; Cote — identité de l\'émetteur')) + r'''
</section>

<section class="rg" id="sec-fact">
  <h3>Factures et devis <button class="q" type="button" aria-expanded="false" title="Explications">?</button></h3>
  <div class="plus" hidden>
    <p>Ce qui est imprimé en tête et en pied de chaque facture ou devis envoyé à un client, et les
    règles de calcul. Les cases vides restent vides sur le document : à remplir avec Sam.</p>
    ''' + agit('Factures — en-tête, pied et calculs', 'Cote — mêmes en-tête et pied') + r'''</div>
''' + ligne('Logo de l\'entreprise', '', logo('f', 'PNG, JPEG ou WebP. L\'image est réduite à 600 px de large : assez pour une impression nette, assez léger pour se synchroniser entre les postes. Un PNG sur fond transparent est ce qui rend le mieux.'), large=True) \
    + ligne('Raison sociale exacte (sur la facture)', '', texte('f-raison', 'DASY LLC', bold=True)) \
    + ligne('Nom commercial (sous la raison sociale)', '', texte('f-enseigne', 'Perfumes Trade')) \
    + ligne('Adresse (une ligne)', '', texte('f-adresse', '1881 NW 20th St, Miami, FL 33142', 360)) \
    + ligne('Téléphone', '', texte('f-tel', '+1 305 …')) \
    + ligne('Email sur la facture', '', texte('f-email', 'perfumestradellc@gmail.com')) \
    + ligne('N° de Sales Tax (Florida certificate)', '', texte('f-taxid', '23-…')) \
    + ligne('Taux de sales tax appliqué (%)', '', '<input type="number" id="f-taux" step="0.01" min="0" max="20" placeholder="7"><b>%</b>') \
    + ligne('Frais si paiement par carte (%)', '', '<input type="number" id="f-carte" step="0.1" min="0" max="10" placeholder="2.6"><b>%</b>') \
    + ligne('Coordonnées Zelle (imprimées sur les factures à payer)', '', texte('f-zelle', 'Zelle : perfumestradellc@gmail.com', 360)) \
    + ligne('Préfixe des numéros de facture', '', texte('f-prefixe', 'PT', 120)) + r'''
</section>

<section class="rg">
  <h3>Écrire aux clients et aux fournisseurs <button class="q" type="button" aria-expanded="false" title="Explications">?</button></h3>
  <div class="plus" hidden>
    <p>Sert au bouton <b>Écrire</b> des fiches. Perfumes Trade ne peut pas envoyer un email
    à ta place — pour ça il faudra le serveur. Ce qu'il fait : ouvrir ta messagerie avec le
    message déjà écrit, à ton nom, et te laisser appuyer sur Envoyer.</p>
    <p>Si tu lis ton courrier dans Gmail, choisis <b>Gmail</b> : le message s'ouvre dans une fenêtre de rédaction Gmail, déjà remplie, depuis
    ton adresse. C'est ce qui ressemble le plus à « envoyer depuis mon email » sans serveur.</p>
    ''' + agit('Clients — bouton Écrire', 'Fournisseurs — bouton Écrire') + r'''</div>
''' + ligne('Ton nom, en bas des messages', '', texte('r-sign', 'Sam — Perfumes Trade', 260)) \
    + ligne('Ton adresse email', '', texte('r-mail', 'sam@perfumestrade.com', 260)) \
    + ligne('Ton téléphone WhatsApp', '', texte('r-tel', '+1 305 555 0100', 260)) \
    + ligne('Quand j\'appuie sur « Ouvrir l\'email »', '', '''<select id="r-boite" style="width:360px">
      <option value="defaut">Ouvrir mon logiciel de mail (Mail, Outlook…)</option>
      <option value="gmail">Ouvrir Gmail dans le navigateur</option>
      <option value="outlook">Ouvrir Outlook.com dans le navigateur</option>
    </select>''') + r'''
</section>
</div>
</div>

<div class="pan" id="pan-pc" hidden>
<p class="pan-sous">La boutique de Sam : l'en-tête de ses factures, et son stock sur Shopify.</p>
<div class="blocs">
<section class="rg" id="sec-factpc">
  <h3>Factures de Perfume City <button class="q" type="button" aria-expanded="false" title="Explications">?</button></h3>
  <div class="plus" hidden>
    <p>Quand une vente est faite sur le canal <b>Perfume City</b> et que le client veut une facture
    (payée en Zelle, par exemple), la facture part avec <b>cet en-tête-là</b> et non celui de DASY.
    Le taux de sales tax et les frais de carte restent ceux de l'entreprise.</p>
    ''' + agit('Ventes — facture d\'une vente Perfume City') + r'''</div>
''' + ligne('Logo de Perfume City', '', logo('p', 'Sans logo, la facture porte seulement le nom en texte.'), large=True) \
    + ligne('Nom exact sur la facture', '', texte('p-raison', 'Perfume City', bold=True)) \
    + ligne('Nom commercial (sous le nom, si différent)', '', texte('p-enseigne', 'Perfume City')) \
    + ligne('Adresse (une ligne)', '', texte('p-adresse', 'adresse de la boutique', 360)) \
    + ligne('Téléphone', '', texte('p-tel')) \
    + ligne('Email sur la facture', '', texte('p-email')) \
    + ligne('Instagram de la boutique (imprimé sous l\'email)', '', texte('p-insta', '@nomdelaboutique')) \
    + ligne('N° de Sales Tax de la boutique', '', texte('p-taxid')) \
    + ligne('Coordonnées Zelle de la boutique', '', texte('p-zelle', 'Zelle : …', 360)) \
    + ligne('Préfixe des numéros de facture', '', texte('p-prefixe', 'PC', 120)) + r'''
</section>

<section class="rg">
''' + ligne('Prévenir quand le stock de Perfume City n\'a pas suivi sur Shopify', 'Afficher les réceptions dont le stock n\'est pas parti sur Shopify',
            '<input type="checkbox" id="r-alpc">',
            '<p>À la réception d\'un achat, la part de Perfume City entre dans son stock de l\'ERP puis est envoyée à Shopify. Si l\'envoi échoue '
            '(hors ligne, parfum absent de la boutique…) ou reste à moitié fait, la facture est listée dans le tableau de bord jusqu\'à ce que '
            '« Renvoyer à Shopify » ait réussi. Rien n\'est compté deux fois.</p>'
            + agit('Tableau de bord — liste des alertes', 'Factures — bouton « Renvoyer à Shopify »'), etat_id='e-alpc', sid='sec-alpc') + r'''
</section>
</div>
</div>

<div class="pan" id="pan-prix" hidden>
<p class="pan-sous">Comment chaque canal calcule son prix et sa marge, et à partir de quand un prix est signalé.</p>
<div class="blocs">
<section class="rg">
''' + ligne('Seuil de marge', 'Signaler une marge de gros inférieure à', '<input type="number" id="r-mg" min="0" max="90" step="1"><b>%</b>',
            '<p>En dessous de cette marge sur le prix de gros, la référence est signalée comme mal placée.</p>'
            + agit('Catalogue — pastille de marge', 'Tableau de bord — liste des alertes'), etat_id='e-mg') + r'''
</section>

<section class="rg" id="sec-envois">
  <h3>Canaux de vente et règle de prix <button class="q" type="button" aria-expanded="false" title="Explications">?</button></h3>
  <div class="plus" hidden>''' + P_CANAUX + r'''</div>
  <table class="can"><thead><tr><th>Canal</th><th class="r">Commission</th><th class="r">Envoi par commande</th>
    <th class="r">Prix</th><th class="r">Marge nette</th><th class="r">Plancher</th><th></th></tr></thead>
    <tbody id="canaux"></tbody>
    <caption>Prix, marge nette et plancher : un exemple, pas tes chiffres — un parfum acheté 50 $, vendu seul dans sa commande, 89 $ au retail, 62 $ en gros.</caption></table>
  <div style="padding:2px 0 12px"><button class="btn" id="can-add">+ Ajouter un canal</button></div>
</section>

</div>
</div>

<div class="pan" id="pan-stock" hidden>
<p class="pan-sous">Ce qui fait apparaître une référence en alerte, et le stock envoyé aux deux sites.</p>
<div class="blocs">
<section class="rg">
''' + ligne('Prévenir quand le stock devient bas', 'Prévenir en dessous de', '<input type="number" id="r-qte" min="0" max="999" step="1"><b>flacons</b>',
            '<p>Une référence passe en alerte quand il en reste moins que ce nombre.</p>'
            + agit('Catalogue — pastille orange', 'Tableau de bord — liste des alertes') + '<div id="d-qte"></div><ul class="exs" id="x-qte"></ul>', etat_id='e-qte') + r'''
</section>

<section class="rg">
''' + ligne('Stock sur les deux sites', 'Envoyer le stock aux deux sites automatiquement',
            '<input type="checkbox" id="r-stsites">',
            '<p>Allumé, chaque changement de stock dans l\'ERP — facture d\'achat, vente, comptage, retour, '
            'expédition — part tout seul sur <b>perfumestrade.com</b> et sur <b>le site de gros</b>, quelques '
            'secondes après. Seuls les parfums déjà en ligne, dont la fiche compte ses unités, sont touchés : '
            'rien n\'est créé, aucun prix ne change. Un envoi qui mettrait plus de 25 parfums à zéro d\'un coup '
            'est bloqué et signalé.</p>'
            '<p><b>À allumer le jour de la mise en ligne</b>, une fois le vrai stock importé. À partir de là, '
            'plus personne ne corrige le stock des sites à la main : l\'ERP écraserait la correction. '
            'La caisse Lightspeed n\'est pas concernée : le forfait actuel ne permet pas d\'y écrire.</p>'
            '<p>Une vente Amazon, de la caisse ou d\'un des deux sites baisse aussitôt le stock des autres sites, même la nuit, sans attendre qu\'une page de l\'ERP soit ouverte. Les commandes à expédier ne sont plus proposées sur les sites.</p>'
            + agit('perfumestrade.com — stock', 'wholesale.perfumestrade.com — stock') + '<div id="d-stsites"></div>', etat_id='e-stsites', sid='sec-stsites') + r'''
</section>
</div>
</div>

<div class="pan" id="pan-caisse" hidden>
<p class="pan-sous">La caisse Lightspeed du magasin : les espèces du tiroir, et les devis qu'on peut convertir.</p>
<div class="blocs">
<section class="rg">
''' + ligne('Fonds de caisse', 'Fonds de caisse laissé dans le tiroir', '<input type="number" id="r-fond" min="0" max="100000" step="1"><b>$</b>',
            '<p>Les espèces que Sam laisse toujours dans le tiroir de la caisse. Le tableau de bord compte les espèces encaissées à la caisse '
            'depuis la dernière récolte ; quand Sam récolte, il laisse ce montant et appuie sur « Récolte faite ».</p>'
            + agit('Tableau de bord — case « Espèces en caisse »'), sid='sec-caisse') \
    + ligne('Fonds de caisse de Perfume City', 'Fonds laissé dans le tiroir de la boutique de Kim', '<input type="number" id="r-fondpc" min="0" max="100000" step="1"><b>$</b>',
            '<p>Les espèces que Kim laisse toujours dans le tiroir de Perfume City. Le tableau de bord compte les espèces encaissées par la boutique '
            '(les commandes Shopify payées en « cash ») depuis la dernière récolte, dans un bloc à part de celui de Sam.</p>'
            + agit('Tableau de bord — case « Espèces en caisse · Perfume City »'), sid='sec-caisse-pc') \
    + ligne('Frais de carte Lightspeed', 'Ce que Lightspeed Payments prend sur un paiement par carte', '<input type="number" id="r-cartels" min="0" max="10" step="0.1"><b>%</b>',
            '<p>Retiré de la marge de chaque vente de la caisse, sur la part payée par carte seulement : les espèces et Zelle ne coûtent rien. '
            'Changer le taux recalcule toutes les ventes enregistrées, passées comprises.</p>'
            '<p>Ce n\'est pas le « Frais si paiement par carte » des factures (onglet Ma société) : celui-là, c\'est ce que Sam facture au client.</p>'
            + agit('Ventes — marge nette des ventes de la caisse'), sid='sec-cartels') \
    + ligne('Devis Lightspeed', 'Convertibles en vente à partir de cette date.', '<input type="date" id="r-devisdep" style="width:180px">',
            '<p>Les devis de la caisse créés <b>à partir de cette date</b> peuvent être convertis en vente dans la rubrique Cote. '
            'Ceux d\'avant restent en lecture seule : le stock de départ en tient déjà compte.</p>', sid='sec-devisls') + r'''
</section>
</div>
</div>

<div class="pied">
  <button class="btn" id="def">Revenir aux valeurs de départ</button>
  <span class="msg" id="msg"></span>
  <span style="margin-left:auto"><a class="btn pri" href="tableau.html">Voir le tableau de bord</a></span>
</div>
'''

JS_ONGLETS = r'''
/* ---- les onglets (25 oct. 2026) : un seul visible, le dernier ouvert est retenu ; un lien
   vers #sec-… ou vers un champ ouvre l'onglet qui le contient et déplie ses explications. */
const K_ONG='reglages-onglet-v1';
function rgOnglet(t){
  if(!document.getElementById('pan-'+t)) t='soc';
  document.querySelectorAll('.pan').forEach(p=>{ p.hidden=(p.id!=='pan-'+t); });
  document.querySelectorAll('#ong button').forEach(b=>b.classList.toggle('on',b.dataset.t===t));
  try{ localStorage.setItem(K_ONG,t); }catch(e){}
}
window.__rgOnglet=rgOnglet;
document.getElementById('ong').addEventListener('click',e=>{ const b=e.target.closest('button[data-t]'); if(b) rgOnglet(b.dataset.t); });
document.querySelectorAll('.q').forEach(b=>b.addEventListener('click',()=>{
  const bloc=b.closest('.lg')||b.closest('.rg'); const plus=bloc&&bloc.querySelector('.plus'); if(!plus) return;
  plus.hidden=!plus.hidden; b.setAttribute('aria-expanded',String(!plus.hidden));
}));
function rgVers(h){
  const el=h&&document.getElementById(h.replace(/^#/,'')); if(!el) return false;
  const pan=el.closest('.pan'); if(!pan) return false;
  rgOnglet(pan.id.replace('pan-',''));
  const lg=el.closest('.lg')||el; const plus=lg.querySelector('.plus'), q=lg.querySelector('.q');
  if(plus){ plus.hidden=false; if(q) q.setAttribute('aria-expanded','true'); }
  try{ el.scrollIntoView({block:'start'}); }catch(e){}
  return true;
}
(function(){ let t='soc'; try{ t=localStorage.getItem(K_ONG)||'soc'; }catch(e){}
  rgOnglet(t); if(location.hash) rgVers(location.hash); })();
window.addEventListener('hashchange',()=>rgVers(location.hash));
'''

JS = r'''
const IDX=__IDX__;
const KREG='reglages-v1', KJOU='crm-journal-v1', KMOD='fiches-modifiees-v1', KEXT='stock-externe-v1';
const CANAUX_DEF=[{id:'site',nom:'Site perfumestrade.com',maj:0,com:3},
  {id:'sitegros',nom:'Site wholesale.perfumestrade.com',base:'pvw',maj:0,com:3},{id:'amazon',nom:'Amazon',maj:18,com:15},{id:'perfumecity',nom:'Perfume City',maj:0,com:3}];
const DEF={seuilQte:3,capMin:0,baissePct:30,baisseJours:30,margeMin:10,fondCaisse:200,fondCaissePC:0,societe:'DASY LLC',
  canaux:CANAUX_DEF, signature:'', monMail:'', monTel:'', boite:'defaut',
  fact:{raison:'',enseigne:'Perfumes Trade',adresse:'',tel:'',email:'',taxid:'',taux:7,carte:2.6,zelle:'',prefixe:'PT',conditions:'',exo:'',logo:''},
  factPC:{raison:'',enseigne:'Perfume City',adresse:'',tel:'',email:'',insta:'',taxid:'',zelle:'',prefixe:'PC',logo:''}};
let REG=Object.assign({},DEF);
try{ const r=JSON.parse(localStorage.getItem(KREG)||'null'); if(r) REG=Object.assign({},DEF,r); }catch(e){}
base(KREG,REG);
(function(){ try{ const K='canaux-ebay-perfumecity-v1'; if(localStorage.getItem(K)) return;
  if(Array.isArray(REG.canaux)){ REG.canaux=REG.canaux.filter(c=>c.id!=='ebay');
    if(!REG.canaux.some(c=>c.id==='perfumecity')) REG.canaux.push({id:'perfumecity',nom:'Perfume City',maj:0,com:3});
    localStorage.setItem(KREG,JSON.stringify(REG)); }
  localStorage.setItem(K,'1'); }catch(e){} })();
try{ const v=localStorage.getItem('seuil-stock-faible-v1');
  if(v!==null && !localStorage.getItem(KREG)) REG.seuilQte=+v; }catch(e){}
/* 24 sept. 2026 (Igal) : Shopify quitte les canaux — c'est la caisse de Perfume City,
   rien n'en remonte, et Perfume City a déjà sa case. Le site de GROS arrive, calculé
   sur le prix de gros (pas sur le retail). Une seule fois : le repère est rangé DANS
   les réglages, donc partagé par tous les ordinateurs, et un canal remis à la main
   ensuite n'est plus jamais retiré. */
/* 27 sept. 2026 (Igal) : « Boutique / Shop, supprime ça, ça ne sert à rien » — tout ce
   qui se vend au magasin passe par la caisse Lightspeed, qui a son propre canal. Même
   principe : une seule fois, repère dans les réglages. Les ventes déjà enregistrées
   sous « Boutique » gardent leur nom (l'historique ne se réécrit pas). */
(function(){ try{ const v0=REG.canauxV||0; if(v0>=3) return;
  let L=(Array.isArray(REG.canaux)&&REG.canaux.length)?REG.canaux.slice():JSON.parse(JSON.stringify(CANAUX_DEF));
  if(v0<2){
    L=L.filter(c=>c&&c.id!=='shopify');
    if(!L.some(c=>c.id==='sitegros')){ const i=L.findIndex(c=>c.id==='site'); L.splice(i>=0?i+1:L.length,0,{id:'sitegros',nom:'Site wholesale.perfumestrade.com',base:'pvw',maj:0,com:3}); }
  }
  L=L.filter(c=>c&&c.id!=='boutique');
  if(!L.length) L=JSON.parse(JSON.stringify(CANAUX_DEF));
  REG.canaux=L; REG.canauxV=3; ecrit(KREG,REG); }catch(e){} })();
/* 17 oct. 2026 (Igal) : « sur WooCommerce on déduit 3 % de commission, il faut faire de même sur Shopify » → le canal
   Perfume City passe à 3 % UNE fois (repère pcCom3 dans les réglages) ; si Sam le remet à 0 ensuite, c'est respecté. */
(function(){ try{ if(REG.pcCom3) return;
  if(Array.isArray(REG.canaux)) REG.canaux=REG.canaux.map(c=>(c&&c.id==='perfumecity'&&!(+c.com))?Object.assign({},c,{com:3}):c);
  REG.pcCom3=1; ecrit(KREG,REG); }catch(e){} })();
const sauve=()=>{ ecrit(KREG,REG);
  $('msg').textContent='enregistré'; clearTimeout(sauve._t);
  sauve._t=setTimeout(()=>$('msg').textContent='',1600); };

/* Un réglage change les marges de TOUT le catalogue : passer la commission Amazon
   de 15 % à 3 %, c'est refaire tous les calculs de l'outil. Ça doit être signé et daté
   comme n'importe quelle modification de prix. On regroupe les frappes successives
   pour n'écrire qu'une ligne par valeur réellement changée. */
const KJOU_R='crm-journal-v1';
const AV={};                      /* la valeur d'avant, prise à la première frappe */
const T_LOG={};
function logReg(cle,lib,avant,apres){
  if(String(avant)===String(apres)) return;
  if(!(cle in AV)) AV[cle]=avant;
  clearTimeout(T_LOG[cle]);
  T_LOG[cle]=setTimeout(()=>{
    const dep=AV[cle]; delete AV[cle];
    if(String(dep)===String(apres)) return;
    const J=lit(KJOU_R,[]);
    J.push({t:new Date().toISOString(),u:NOM_UTIL||'(non renseigné)',act:'reglage',
            lib,av:dep===''||dep==null?'—':dep,ap:apres===''||apres==null?'—':apres});
    ecrit(KJOU_R,J);
  },900);
}

/* etat courant du stock : le fichier, corrige par ce qui a ete saisi ou importe */
let MOD={},EXT={q:{}},JOU=[];
try{ MOD=JSON.parse(localStorage.getItem(KMOD)||'{}'); }catch(e){}
try{ const r=JSON.parse(localStorage.getItem(KEXT)||'null'); if(r&&r.q) EXT=r; }catch(e){}
try{ JOU=JSON.parse(localStorage.getItem(KJOU)||'[]'); }catch(e){}
const ART=Object.entries(IDX).map(([cle,v])=>{
  const [bc,nom,marque,pa,qte,pvw,pvr]=v;
  let q=qte;
  if(EXT.q[bc]!==undefined&&EXT.q[bc]!==null) q=EXT.q[bc];
  const m=MOD[cle]; 
  return {cle,bc,nom,marque,pa,qte:(m&&m.qte!=null)?m.qte:q,
          pvw:(m&&m.pvw!=null)?m.pvw:pvw, pa:(m&&m.pa!=null)?m.pa:pa};
});
const enStock=ART.filter(p=>p.qte>0);
const cap=p=>p.qte*(p.pa||0);

function touchees(){
  return enStock.filter(p=>REG.seuilQte>0 && p.qte<REG.seuilQte && cap(p)>=REG.capMin);
}
function jauge(n,tot){
  const pc=tot?n/tot*100:0;
  const cls=pc>35?'non':pc>18?'bof':'';
  return `<div class="jauge"><div class="${cls}" style="width:${Math.min(100,pc)}%"></div></div>`;
}
function liste(l,val){
  if(!l.length) return '';
  return `<ul class="exs">${l.slice(0,5).map(p=>`<li>
    <span class="mq">${esc(p.marque||'')}</span><span class="nm">${esc(p.nom||'')}</span>
    <span class="n">${val(p)}</span></li>`).join('')}
    ${l.length>5?`<li style="color:var(--ink-3)"><span class="nm">et ${nf(l.length-5)} autres</span></li>`:''}</ul>`;
}

function dessine(){
  const tot=enStock.length;
  // seuil quantite
  const t=touchees();
  const c=t.reduce((a,p)=>a+cap(p),0);
  const pc=tot?Math.round(t.length/tot*100):0;
  const cls = REG.seuilQte<=0 ? '' : pc>35?'non':pc>18?'bof':'bon';
  /* 25 oct. 2026 (Igal : « il y en a de partout ») : sous le nom, UNE ligne de chiffres ; le conseil,
     la jauge et les exemples sont derrière « ? ». */
  const pt=k=>`<span class="pt ${k}"></span>`;
  $('e-qte').innerHTML = REG.seuilQte<=0
    ? pt('')+`Aucune alerte de niveau.`
    : pt(cls)+`${nf(t.length)} référence${t.length>1?'s':''} en alerte · ${pc} % du stock · ${money(c)}`;
  $('d-qte').innerHTML = REG.seuilQte<=0
    ? `<div class="eff">Aucune alerte de niveau. Les quantités restent en noir dans le catalogue.</div>`
    : `<div class="eff ${cls}"><b>${nf(t.length)} référence${t.length>1?'s':''}</b> déclenchent l'alerte,
       soit <b>${pc} %</b> du stock et <b>${money(c)}</b> de marchandise.
       ${pc>35?"C'est trop : une alerte sur plus d'un tiers du stock n'attire plus l'œil.":
         pc>18?"Encore un peu large. Le filtre du dessous permet d'écarter les petites références.":
         "Liste courte : l'alerte garde du sens."}${jauge(t.length,tot)}</div>`;
  $('x-qte').outerHTML = `<ul class="exs" id="x-qte" hidden></ul>`;
  const sorted=t.slice().sort((a,b)=>cap(b)-cap(a));
  const zone=document.getElementById('x-qte');
  zone.outerHTML = liste(sorted,p=>`${p.qte} en stock · ${money(cap(p))}`).replace('<ul class="exs">','<ul class="exs" id="x-qte">')
    || '<ul class="exs" id="x-qte" hidden></ul>';

  /* 25 oct. 2026 (Igal : « enlève-le ») : le filtre « petites références » (capMin) n'est plus réglable ;
     il est remis à 0 une fois pour toutes, pour qu'une vieille valeur ne trie plus en silence. */
  if(REG.capMin){ REG.capMin=0; ecrit(KREG,REG); }

  // marge
  const mm=enStock.filter(p=>p.pvw!=null&&p.pa!=null&&p.pvw>0&&((p.pvw-p.pa)/p.pvw*100)<REG.margeMin);
  const cm=mm.reduce((a,p)=>a+cap(p),0);
  $('e-mg').innerHTML=pt(mm.length/tot>0.15?'bof':'bon')+`${nf(mm.length)} référence${mm.length>1?'s':''} sous ${REG.margeMin} % de marge de gros · ${money(cm)}`;
  $('src').innerHTML=`${nf(touchees().length)} alerte${touchees().length>1?'s':''} de stock<br>${nf(tot)} références en stock`;
}

/* ---- canaux ---- */
const r2=v=>Math.round(v*100)/100;
const ENV_DE=c=>({site:'woocommerce',sitegros:'woocommerce-gros',amazon:'amazon'})[c&&c.id]||'';
const envDe=k=>{ const E=REG.envois||{}; return (E[k]==null||E[k]==='')?8:+E[k]; };
/* 25 oct. 2026 : la majoration ne s'affiche plus et passe à 0, une seule fois (repère majOff). */
(function(){ try{ if(REG.majOff) return; if(Array.isArray(REG.canaux)) REG.canaux=REG.canaux.map(c=>c?Object.assign({},c,{maj:0}):c);
  REG.majOff=1; ecrit(KREG,REG); }catch(e){} })();
function dessineCanaux(){
  if(!Array.isArray(REG.canaux)||!REG.canaux.length) REG.canaux=JSON.parse(JSON.stringify(CANAUX_DEF));
  const pa=50, pvr=89, pvw=62;
  $('canaux').innerHTML=REG.canaux.map((c,i)=>{
    const ek=ENV_DE(c), env=ek?envDe(ek):0;
    const v=r2(c.base==='pvw'?pvw:pvr), net=(v*(1-(c.com||0)/100)-pa-env)/v*100;
    const den=1-(c.com||0)/100-REG.margeMin/100, pl=den>0?r2(pa/den):null;
    return `<tr data-i="${i}">
      <td><input type="text" data-k="nom" value="${esc(c.nom)}"></td>
      <td class="r"><input type="number" data-k="com" min="0" max="60" step="0.1" value="${c.com||0}"> %</td>
      <td class="r">${ek?`<input type="number" data-k="env" id="env-${ek}" min="0" step="0.5" value="${env}"> $`:'<span class="bs">n\'expédie pas</span>'}</td>
      <td class="r ex"><b>${v.toFixed(2).replace('.',',')} $</b> <span class="bs">${c.base==='pvw'?'gros':'retail'}</span></td>
      <td class="r ex" style="color:${net<REG.margeMin?'var(--crit)':'var(--good)'}"><b>${net.toFixed(1).replace('.',',')} %</b></td>
      <td class="r ex">${pl!=null?pl.toFixed(2).replace('.',',')+' $':'—'}</td>
      <td class="r">${REG.canaux.length>1?`<button class="x" data-del="${i}" title="Retirer ce canal">&times;</button>`:''}</td></tr>`;
  }).join('');
}
/* On ne redessine JAMAIS le tableau pendant qu'une case a le focus : le champ serait recréé,
   le curseur repartirait au début et les chiffres s'écriraient à l'envers (taper « 15.5 »
   donnait « 50.51 »). Le tableau se recalcule quand on quitte la case. */
let T_CAN=0;
const enSaisieCan=()=>{ const a=document.activeElement; return !!(a && a.closest && a.closest('#canaux')); };
function recalculeCanaux(){
  clearTimeout(T_CAN);
  T_CAN=setTimeout(function attends(){
    if(enSaisieCan()){ T_CAN=setTimeout(attends,300); return; }
    dessineCanaux();
  },300);
}
$('canaux').addEventListener('input',e=>{
  const tr=e.target.closest('tr'); if(!tr) return; const c=REG.canaux[+tr.dataset.i]; const k=e.target.dataset.k;
  const avant=c[k];
  if(k==='nom'){ c.nom=e.target.value; if(!c.id) c.id='c'+Date.now().toString(36); }
  else if(k==='env'){ const ek=ENV_DE(c); const E2=Object.assign({},REG.envois||{}); const av=envDe(ek);
         const t=e.target.value.trim(); if(t==='') delete E2[ek]; else E2[ek]=Math.max(0,+t.replace(',','.')||0);
         REG.envois=E2; logReg('envoi-'+ek,"coût d'un envoi — "+c.nom,av+' $',envDe(ek)+' $'); sauve(); recalculeCanaux(); return; }
  else { const t=e.target.value.trim().replace(',','.');
         const v=parseFloat(t);
         if(t==='' || t==='-' || /[.,]$/.test(t)) return;   /* saisie en cours : on ne fige rien */
         c[k]=isNaN(v)?0:Math.max(0,Math.min(60,v)); }
  const LIBK={nom:'nom du canal',maj:'majoration',com:'commission prélevée par le canal'};
  logReg('can-'+(c.id||tr.dataset.i)+'-'+k,
         (LIBK[k]||k)+' — '+(k==='nom'?'canal':c.nom),
         k==='nom'?avant:(avant+' %'), k==='nom'?c[k]:(c[k]+' %'));
  sauve();
  if(k!=='nom') recalculeCanaux();
});
$('canaux').addEventListener('click',e=>{
  const b=e.target.closest('[data-del]'); if(!b) return;
  const c=REG.canaux[+b.dataset.del];
  if(!confirm(`Retirer le canal « ${c.nom} » ? Les prix manuels saisis pour ce canal dans les fiches ne seront plus affichés.`)) return;
  const nom=c.nom;
  REG.canaux.splice(+b.dataset.del,1); sauve(); dessineCanaux();
  const J=lit(KJOU_R,[]);
  J.push({t:new Date().toISOString(),u:NOM_UTIL||'(non renseigné)',act:'reglage',
          lib:'canal de vente supprimé',av:nom,ap:'—'});
  ecrit(KJOU_R,J);
});
$('can-add').onclick=()=>{ REG.canaux.push({id:'c'+Date.now().toString(36),nom:'Nouveau canal',maj:0,com:0}); sauve(); dessineCanaux();
  { const J=lit(KJOU_R,[]);
    J.push({t:new Date().toISOString(),u:NOM_UTIL||'(non renseigné)',act:'reglage',
            lib:'canal de vente ajouté',av:'—',ap:'Nouveau canal'});
    ecrit(KJOU_R,J); }
  const last=document.querySelector('#canaux tr:last-child input[data-k="nom"]'); if(last){ last.focus(); last.select(); } };

/* ---- les deux alertes de Shopify / de mise en ligne (21 oct. 2026) : allumées tant qu'on ne les coupe pas ---- */
function peintAlertes(){
  $('r-alpc').checked=REG.alerteStockPC!==false;
  let np=0;   /* 25 oct. 2026 : l'alerte « mise en ligne non aboutie » n'a plus de réglage, elle est toujours affichée */
  try{ (lit('factures-v1',[])||[]).forEach(f=>{ if(f&&f.pcShopify&&['echec','partiel'].includes(f.pcShopify.etat)) np++; }); }catch(e){}
  const pt=k=>`<span class="pt ${k}"></span>`;
  $('e-alpc').innerHTML=(REG.alerteStockPC!==false?pt(np?'bof':'bon'):pt(''))+(REG.alerteStockPC!==false?(np?`<b>${np}</b> facture${np>1?'s':''} à renvoyer à Shopify en ce moment.`:'Rien à renvoyer en ce moment.'):'<b>Éteint</b> : un stock non envoyé à Shopify n\'est plus listé.');
}
[['r-alpc','alerteStockPC','alerte « stock Perfume City non envoyé à Shopify »']].forEach(([id,k,lib])=>{
  $(id).addEventListener('change',()=>{ const av=REG[k]!==false; REG[k]=$(id).checked; sauve(); logReg(k,lib,av?'allumée':'éteinte',REG[k]?'allumée':'éteinte'); peintAlertes(); });
});
try{ peintAlertes(); }catch(e){}

/* ---- le stock envoyé aux sites (27 sept. 2026) ---- */
function peintStSites(){
  const on=REG.stockSitesAuto===true; $('r-stsites').checked=on;
  const J=(lit(KJOU_R,[])||[]).filter(j=>j&&/^stock (NON )?envoyé aux sites/.test(j.lib||'')).slice(-5).reverse();
  $('e-stsites').innerHTML=on?'<span class="pt bon"></span><b>Allumé.</b>':'<span class="pt"></span><b>Éteint</b> : rien ne part sur les sites.';
  $('d-stsites').innerHTML=(J.length?'Derniers envois :<br>'+J.map(j=>`<span data-nolang>${esc(new Date(j.t).toLocaleString('en-US',{timeZone:'America/New_York',day:'2-digit',month:'2-digit',hour:'2-digit',minute:'2-digit'}))}</span> — ${esc(j.lib)}`).join('<br>'):'');
}
$('r-stsites').addEventListener('change',()=>{
  const on=$('r-stsites').checked;
  if(on&&!confirm("À partir de maintenant, chaque changement de stock dans l'ERP part tout seul sur les deux sites.\n\nPlus personne ne doit corriger le stock des sites à la main.\n\nAllumer ?")){ $('r-stsites').checked=false; return; }
  const avant=REG.stockSitesAuto===true;
  REG.stockSitesAuto=on; sauve();
  logReg('stockSitesAuto','envoi automatique du stock aux sites',avant?'allumé':'éteint',on?'allumé':'éteint');
  peintStSites();
});
try{ peintStSites(); }catch(e){}

/* ---- les frais de carte Lightspeed (25 oct. 2026) : 2,6 % par défaut, sur la part carte des ventes de la caisse ---- */
{ const el=$('r-cartels'); if(el){ const lu=()=>{ const v=REG.carteLS; return (v==null||v===''||isNaN(+v))?2.6:+v; }; el.value=lu();
  el.addEventListener('input',()=>{ const t=el.value.trim().replace(',','.'); if(t===''||/[.,]$/.test(t)) return; const v=parseFloat(t); if(isNaN(v)) return;
    const av=lu(); REG.carteLS=Math.max(0,Math.min(10,v)); sauve(); logReg('carteLS','frais de carte Lightspeed (%)',av+' %',REG.carteLS+' %'); }); } }
/* ---- la date à partir de laquelle un devis Lightspeed se convertit (29 sept. 2026) ---- */
{ const el=$('r-devisdep'); if(el){ el.value=REG.devisDepuis||'2026-10-01';
  el.addEventListener('change',()=>{ if(!/^\d{4}-\d{2}-\d{2}$/.test(el.value)) return; const av=REG.devisDepuis||'2026-10-01'; REG.devisDepuis=el.value; sauve(); logReg('devisDepuis','devis Lightspeed convertibles à partir du',av,el.value); }); } }

const champs=[['r-qte','seuilQte'],['r-mg','margeMin'],['r-fond','fondCaisse'],['r-fondpc','fondCaissePC']];
champs.forEach(([id,k])=>{
  $(id).value=REG[k];
  $(id).addEventListener('input',()=>{
    const t=$(id).value.trim();
    if(t==='') return;
    const v=parseInt(t,10);
    /* le seuil de marge est plafonné : au-delà, le plancher de prix deviendrait impossible
       à calculer (commission + marge ≥ 100 %) et plus aucun prix ne serait refusé. */
    const avant=REG[k];
    REG[k]=isNaN(v)?0:(k==='margeMin'?Math.max(0,Math.min(35,v)):Math.max(0,v));
    if(k==='margeMin'&&REG[k]!==v) $(id).value=REG[k];
    const LIBS={seuilQte:'seuil de stock faible',capMin:'capital minimum surveillé',
                baissePct:'baisse de prix signalée',baisseJours:'fenêtre de la baisse (jours)',
                margeMin:'marge minimum exigée',fondCaisse:'fonds de caisse ($)',fondCaissePC:'fonds de caisse de Perfume City ($)'};
    logReg('reg-'+k,LIBS[k]||k,avant,REG[k]);
    sauve(); dessine();
  });
});
$('r-soc').value=REG.societe||'';
/* Les coordonnées de l'expéditeur : le bouton Écrire des fiches les relit. */
[['r-sign','signature','signature des messages'],
 ['r-mail','monMail','adresse email de l\'expéditeur'],
 ['r-tel','monTel','téléphone WhatsApp'],
 ['r-boite','boite','messagerie à ouvrir']].forEach(([id,k,lib])=>{
  const el=$(id); if(!el) return;
  el.value=REG[k]||(k==='boite'?'defaut':'');
  el.addEventListener(el.tagName==='SELECT'?'change':'input',()=>{
    const av=REG[k]; REG[k]=el.value.trim?el.value.trim():el.value;
    logReg('reg-'+k,lib,av,REG[k]); sauve(); });
});
/* Factures et devis : un objet à part, relu par la rubrique Ventes au moment d'imprimer. */
REG.fact=Object.assign({},DEF.fact,REG.fact||{});
[['f-raison','raison','raison sociale'],['f-enseigne','enseigne','nom commercial'],['f-adresse','adresse','adresse'],
 ['f-tel','tel','téléphone facture'],['f-email','email','email facture'],['f-taxid','taxid','n° sales tax'],
 ['f-taux','taux','taux de sales tax'],['f-carte','carte','frais carte'],['f-zelle','zelle','coordonnées Zelle'],
 ['f-prefixe','prefixe','préfixe des factures']].forEach(([id,k,lib])=>{
  const el=$(id); if(!el) return;
  el.value=REG.fact[k]==null?'':REG.fact[k];
  el.addEventListener('input',()=>{
    const av=REG.fact[k]; let v=el.value.trim();
    if(el.type==='number') v=v===''?'':+v;
    REG.fact[k]=v; logReg('reg-fact-'+k,'facture — '+lib,av,v); sauve(); });
});

/* Factures de Perfume City : son propre en-tête (REG.factPC), lu par la rubrique Ventes. */
REG.factPC=Object.assign({},DEF.factPC,REG.factPC||{});
[['p-raison','raison','raison sociale'],['p-enseigne','enseigne','nom commercial'],['p-adresse','adresse','adresse'],
 ['p-tel','tel','téléphone'],['p-email','email','email'],['p-insta','insta','Instagram'],['p-taxid','taxid','n° sales tax'],
 ['p-zelle','zelle','coordonnées Zelle'],['p-prefixe','prefixe','préfixe des factures']].forEach(([id,k,lib])=>{
  const el=$(id); if(!el) return;
  el.value=REG.factPC[k]==null?'':REG.factPC[k];
  el.addEventListener('input',()=>{
    const av=REG.factPC[k], v=el.value.trim();
    REG.factPC[k]=v; logReg('reg-factpc-'+k,'facture Perfume City — '+lib,av,v); sauve(); });
});

/* ---- le logo de l'entreprise ----
   Il finit imprimé sur chaque facture, donc il doit être net ; il vit dans les
   réglages synchronisés entre les postes, donc il doit rester léger. On le réduit
   à 600 px de large avant de l'enregistrer : au-delà, on alourdit la
   synchronisation de tout le monde pour un gain invisible sur le papier.
   Le SVG passe tel quel — il est net à toute taille et ne pèse rien. */
const LOGO_LARGE=600, LOGO_MAX=260000;
function logoAffiche(src){
  const z=$('f-logoap'); if(!z) return;
  z.innerHTML = src ? '<img src="'+src+'" alt="">' : 'aucun logo';
  $('f-logosup').hidden = !src;
}
function logoReduit(file){
  return new Promise((ok,err)=>{
    const r=new FileReader();
    if(/svg/i.test(file.type||'')){
      r.onload=()=>ok(r.result); r.onerror=()=>err(new Error('Lecture impossible.'));
      r.readAsDataURL(file); return;
    }
    r.onload=()=>{ const im=new Image();
      im.onload=()=>{
        const k=Math.min(1, LOGO_LARGE/(im.width||1));
        const c=document.createElement('canvas');
        c.width=Math.max(1,Math.round(im.width*k)); c.height=Math.max(1,Math.round(im.height*k));
        c.getContext('2d').drawImage(im,0,0,c.width,c.height);
        /* PNG d'abord, pour garder la transparence d'un logo ; JPEG si le PNG est
           trop lourd, ce qui arrive quand l'image est en réalité une photo. */
        let out=c.toDataURL('image/png');
        if(out.length>LOGO_MAX){ const j=c.toDataURL('image/jpeg',0.86); if(j.length<out.length) out=j; }
        ok(out);
      };
      im.onerror=()=>err(new Error("Ce fichier n'est pas une image lisible."));
      im.src=r.result; };
    r.onerror=()=>err(new Error('Lecture impossible.'));
    r.readAsDataURL(file);
  });
}
if($('f-logobtn')){
  $('f-logobtn').onclick=()=>$('f-logofic').click();
  $('f-logofic').addEventListener('change',async e=>{
    const f=e.target.files[0]; e.target.value=''; if(!f) return;
    const aide=$('f-logoaide');
    try{
      const src=await logoReduit(f);
      if(src.length>LOGO_MAX*1.6){
        aide.innerHTML='<b style="color:var(--crit)">Cette image reste trop lourde après réduction.</b> '
          +'Un logo pèse quelques dizaines de kilo-octets : reprends-le en PNG ou en JPEG, sans photo en fond.';
        return;
      }
      const av=REG.fact.logo?'un logo':'aucun';
      REG.fact.logo=src; sauve(); logoAffiche(src);
      aide.textContent='Logo enregistré — il apparaîtra en haut de chaque facture et de chaque devis.';
      logReg('reg-fact-logo','facture — logo',av,'un logo');
    }catch(ex){ aide.textContent=(ex&&ex.message)||'Image illisible.'; }
  });
  $('f-logosup').onclick=()=>{
    if(!confirm('Retirer le logo ?\n\nLes prochaines factures repartiront sans logo. Les documents déjà émis gardent le leur : leur en-tête est figé au moment de l\'émission.')) return;
    REG.fact.logo=''; sauve(); logoAffiche('');
    $('f-logoaide').textContent='Logo retiré.';
    logReg('reg-fact-logo','facture — logo','un logo','aucun');
  };
  logoAffiche(REG.fact.logo||'');
}

function logoAfficheP(src){
  const z=$('p-logoap'); if(!z) return;
  z.innerHTML = src ? '<img src="'+src+'" alt="">' : 'aucun logo';
  $('p-logosup').hidden = !src;
}
if($('p-logobtn')){
  $('p-logobtn').onclick=()=>$('p-logofic').click();
  $('p-logofic').addEventListener('change',async e=>{
    const f=e.target.files[0]; e.target.value=''; if(!f) return;
    const aide=$('p-logoaide');
    try{
      const src=await logoReduit(f);
      if(src.length>LOGO_MAX*1.6){
        aide.innerHTML='<b style="color:var(--crit)">Cette image reste trop lourde après réduction.</b> Reprends-la en PNG ou en JPEG, sans photo en fond.';
        return;
      }
      const av=REG.factPC.logo?'un logo':'aucun';
      REG.factPC.logo=src; sauve(); logoAfficheP(src);
      aide.textContent='Logo enregistré — il apparaîtra en haut des factures Perfume City.';
      logReg('reg-factpc-logo','facture Perfume City — logo',av,'un logo');
    }catch(ex){ aide.textContent=(ex&&ex.message)||'Image illisible.'; }
  });
  $('p-logosup').onclick=()=>{
    if(!confirm('Retirer le logo de Perfume City ?\n\nLes factures déjà émises gardent leur en-tête.')) return;
    REG.factPC.logo=''; sauve(); logoAfficheP('');
    $('p-logoaide').textContent='Logo retiré.';
    logReg('reg-factpc-logo','facture Perfume City — logo','un logo','aucun');
  };
  logoAfficheP(REG.factPC.logo||'');
}

$('r-soc').addEventListener('input',()=>{ const av=REG.societe;
  REG.societe=$('r-soc').value.trim(); logReg('reg-soc','nom de la société',av,REG.societe); sauve(); });
$('def').onclick=()=>{
  if(!confirm('Revenir aux valeurs de départ ?')) return;
  REG=Object.assign({},DEF,{canaux:JSON.parse(JSON.stringify(CANAUX_DEF))}); champs.forEach(([id,k])=>$(id).value=REG[k]); $('r-soc').value=REG.societe;
  $('r-sign').value=''; $('r-mail').value=''; $('r-tel').value=''; $('r-boite').value='defaut';
  sauve(); dessine(); dessineCanaux();
  const J=lit(KJOU_R,[]);
  J.push({t:new Date().toISOString(),u:NOM_UTIL||'(non renseigné)',act:'reglage',
          lib:'tous les réglages remis aux valeurs de départ',av:'réglages modifiés',ap:'valeurs de départ'});
  ecrit(KJOU_R,J);
};
/* la marge minimum change le plancher des canaux */
$('r-mg').addEventListener('input',dessineCanaux);
dessineCanaux();
function majUser(){ try{ piedSession(); }catch(e){} }
majUser();
$('sfoot').innerHTML='réglages partagés<br>par toutes les rubriques';
dessine();
''' + JS_ONGLETS

html = coquille("Réglages", "Réglages",
  "Un onglet par sujet, une ligne par réglage. Le « ? » au bout d'une ligne explique ce qu'elle change et où. "
  "Tout s'enregistre au fur et à mesure.",
  CSS, CORPS, JS, donnees=('produits',)).replace('__IDX__', 'Object.fromEntries(D_TOUS().map(r=>[r[15],[r[0],r[13],r[2],r[12],r[6],r[8],r[7]]]))')
open('reglages.html','w').write(html)
print('reglages.html',len(html)//1024,'Ko')
