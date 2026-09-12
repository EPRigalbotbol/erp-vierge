# -*- coding: utf-8 -*-
import json
from build_crm import coquille
import _donnees
C=json.load(open('cat.json'))
IDX={r[15]:[r[0],r[13],r[2],r[12],r[6],r[8],r[7]] for r in C}   # bc,nom,marque,pa,qte,pvw,pvr

CSS = r'''
.sous{margin:5px 0 0;font-size:14px;color:var(--ink-2);max-width:74ch;line-height:1.5}
.blocs{display:flex;flex-direction:column;gap:20px;max-width:900px}
.rg{background:var(--surface);border:1px solid var(--line);border-radius:11px;padding:22px 24px;
display:flex;flex-direction:column;gap:14px}
.rg > header{display:flex;align-items:baseline;gap:12px;flex-wrap:wrap;
padding-bottom:13px;border-bottom:1px solid var(--line-2)}
.rg h2{margin:0;font-size:17px;font-weight:700;letter-spacing:-.02em}
.rg header p{margin:0;font-size:13px;color:var(--ink-3);flex:1 1 100%;line-height:1.55;max-width:70ch}
.champ{display:flex;align-items:center;gap:11px;flex-wrap:wrap;font-size:14px;color:var(--ink-2)}
.champ input[type=number]{width:78px;padding:8px 9px;font-family:inherit;font-size:15px;font-weight:700;
text-align:center;border:1px solid var(--line);border-radius:7px;background:var(--surface-2);
color:var(--ink);-moz-appearance:textfield}
.champ input::-webkit-outer-spin-button,.champ input::-webkit-inner-spin-button{
-webkit-appearance:none;margin:0}
.champ input:hover{border-color:var(--ink-3)}
.champ input:focus{outline:0;border-color:var(--iris);box-shadow:0 0 0 3px var(--iris-soft);
background:var(--surface)}
.champ b{font-weight:600;color:var(--ink)}
.logoz{display:flex;gap:16px;align-items:flex-start;flex-wrap:wrap}
.logoap{flex:none;width:150px;height:104px;border:1px dashed var(--line);border-radius:10px;
background:#fff;display:flex;align-items:center;justify-content:center;color:var(--ink-3);
font-size:11.5px;text-align:center;padding:8px;overflow:hidden}
.logoap img{max-width:100%;max-height:88px;object-fit:contain}
.logoz .aide{display:block;max-width:52ch;margin-top:7px;font-size:12px;color:var(--ink-3);line-height:1.5}
.eff{font-size:13px;line-height:1.6;border-radius:8px;padding:12px 15px;background:var(--surface-2);
color:var(--ink-2)}
.eff b{color:var(--ink);font-weight:700}
.eff.bon{background:var(--good-soft);color:var(--good)}
.eff.bof{background:var(--warn-soft);color:var(--warn)}
.eff.non{background:var(--crit-soft);color:var(--crit)}
.jauge{height:8px;border-radius:5px;background:var(--line-2);overflow:hidden;margin-top:9px}
.jauge div{height:100%;background:var(--iris);transition:width .2s}
.jauge div.bof{background:var(--warn)} .jauge div.non{background:var(--crit)}
.exs{list-style:none;margin:11px 0 0;padding:0;display:flex;flex-direction:column;gap:1px;
background:var(--line);border:1px solid var(--line);border-radius:8px;overflow:hidden}
.exs li{background:var(--surface);padding:9px 13px;display:flex;align-items:baseline;gap:11px;font-size:13px}
.exs .n{margin-left:auto;font-weight:700;font-variant-numeric:tabular-nums;white-space:nowrap}
.exs .mq{font-size:11px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:var(--iris);
white-space:nowrap}
.exs .nm{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.can{width:100%;border-collapse:collapse;font-size:13.5px}
.can th{text-align:left;font-family:Inter,sans-serif;font-size:9.5px;letter-spacing:.11em;text-transform:uppercase;
color:var(--ink-2);font-weight:700;padding:6px 8px;border-bottom:1px solid var(--line)}
.can th.r,.can td.r{text-align:right}
.can td{padding:7px 8px;border-bottom:1px solid var(--line-2);vertical-align:middle}
.can input[type=text]{width:100%;min-width:150px;padding:7px 9px;font-family:inherit;font-size:13.5px;font-weight:600;
border:1px solid var(--line);border-radius:7px;background:var(--surface-2);color:var(--ink)}
.can input[type=number]{width:70px;padding:7px 8px;font-family:inherit;font-size:14px;font-weight:700;text-align:center;
border:1px solid var(--line);border-radius:7px;background:var(--surface-2);color:var(--ink);-moz-appearance:textfield}
.can input:focus{outline:0;border-color:var(--iris);box-shadow:0 0 0 3px var(--iris-soft);background:var(--surface)}
.can .ex{font-family:Inter,sans-serif;font-variant-numeric:tabular-nums;color:var(--ink-2);white-space:nowrap}
.can .ex b{color:var(--ink)}
.can .x{background:none;border:0;color:var(--ink-3);font-size:18px;cursor:pointer;padding:2px 6px;line-height:1}
.can .x:hover{color:var(--crit)}
.can .fixe{color:var(--ink-3);font-size:11px;font-style:italic}
.pied{display:flex;gap:11px;align-items:center;flex-wrap:wrap;margin-top:6px}
.pied .msg{font-size:13px;color:var(--good);font-weight:600}
'''

CORPS = r'''
<div class="blocs">

<section class="rg">
  <header><h2>Prévenir quand le stock devient bas</h2>
    <p>Une référence passe en alerte quand il en reste moins que ce nombre. Elle apparaît alors
    en orange dans le catalogue et remonte dans le tableau de bord.</p></header>
  <div class="champ"><span>Prévenir en dessous de</span>
    <input type="number" id="r-qte" min="0" max="999" step="1"><b>flacons</b></div>
  <div id="e-qte"></div>
  <ul class="exs" id="x-qte"></ul>
</section>

<section class="rg">
  <header><h2>Ignorer les petites références</h2>
    <p>Sans ce filtre, une alerte se déclenche aussi bien sur un flacon à 11 $ que sur un Creed à 225 $.
    En ne gardant que les références qui immobilisent au moins un certain montant, la liste
    d'alerte reste courte et ne contient que ce qui coûte de l'argent. Mettre 0 désactive le filtre.</p></header>
  <div class="champ"><span>Ne prévenir que si la référence représente au moins</span>
    <input type="number" id="r-cap" min="0" max="99999" step="10"><b>$ de marchandise</b></div>
  <div id="e-cap"></div>
</section>

<section class="rg">
  <header><h2>Prévenir en cas de baisse rapide</h2>
    <p>Indépendamment du niveau restant : si une référence a perdu une bonne partie de son stock
    en peu de temps, elle mérite un coup d'œil même s'il en reste encore. La baisse est mesurée
    sur les mouvements enregistrés dans le journal.</p></header>
  <div class="champ"><span>Prévenir si le stock a baissé de plus de</span>
    <input type="number" id="r-bp" min="0" max="100" step="5"><b>%</b>
    <span>en</span><input type="number" id="r-bj" min="1" max="365" step="1"><b>jours</b></div>
  <div id="e-bai"></div>
</section>

<section class="rg">
  <header><h2>Seuil de marge</h2>
    <p>En dessous de cette marge sur le prix de gros, la référence est signalée comme mal placée
    dans le catalogue et dans le tableau de bord.</p></header>
  <div class="champ"><span>Signaler une marge de gros inférieure à</span>
    <input type="number" id="r-mg" min="0" max="90" step="1"><b>%</b></div>
  <div id="e-mg"></div>
</section>

<section class="rg">
  <header><h2>Canaux de vente et règle de prix</h2>
    <p>Chaque produit a <b>une case de prix par canal</b>. Elle est pré-remplie par la règle
    « prix retail + majoration du canal », et peut être écrasée à la main dans la fiche produit.
    La <b>commission</b> sert à calculer la marge nette réellement encaissée sur ce canal, et le
    plancher sous lequel un prix est refusé (prix d'achat + seuil de marge, commission comprise).
    Exemple sur un parfum acheté 50 $, retail 89 $.</p></header>
  <table class="can"><thead><tr><th>Canal</th><th class="r">Majoration</th><th class="r">Commission</th>
    <th class="r">Prix obtenu</th><th class="r">Marge nette</th><th class="r">Plancher</th><th></th></tr></thead>
    <tbody id="canaux"></tbody></table>
  <div class="champ"><button class="btn" id="can-add">+ Ajouter un canal</button>
    <span style="font-size:12.5px;color:var(--ink-3)">Boutique, site, Shopify, Amazon, Perfume City, caisse… ce que tu vends réellement. La commission, c’est ce que la plateforme garde sur chaque vente.</span></div>
</section>

<section class="rg">
  <header><h2>Ma société</h2>
    <p>Sert à lire les factures : le nom de ta société y figure toujours, il ne faut pas le prendre
    pour le fournisseur ou le client.</p></header>
  <div class="champ"><span>Nom tel qu'il apparaît sur les factures</span>
    <input type="text" id="r-soc" style="width:220px;text-align:left;font-weight:600"></div>
</section>

<section class="rg" id="sec-fact">
  <header><h2>Factures et devis</h2>
    <p>Ce qui est imprimé en tête et en pied de chaque facture ou devis envoyé à un client, et les
    règles de calcul. Les cases vides restent vides sur le document : à remplir avec Sam.</p></header>
  <div class="champ"><span>Logo de l'entreprise</span>
    <div class="logoz">
      <div class="logoap" id="f-logoap">aucun logo</div>
      <div>
        <input type="file" id="f-logofic" accept="image/png,image/jpeg,image/webp,image/svg+xml" hidden>
        <button class="btn" id="f-logobtn">Choisir une image…</button>
        <button class="btn" id="f-logosup" hidden>Retirer</button>
        <span class="aide" id="f-logoaide">PNG, JPEG ou WebP. L'image est réduite à 600 px de large :
        assez pour une impression nette, assez léger pour se synchroniser entre les postes.
        Un PNG sur fond transparent est ce qui rend le mieux.</span>
      </div>
    </div></div>
  <div class="champ"><span>Raison sociale exacte (sur la facture)</span>
    <input type="text" id="f-raison" placeholder="DASY LLC" style="width:300px;text-align:left;font-weight:600"></div>
  <div class="champ"><span>Nom commercial (sous la raison sociale)</span>
    <input type="text" id="f-enseigne" placeholder="Perfumes Trade" style="width:300px;text-align:left"></div>
  <div class="champ"><span>Adresse (une ligne)</span>
    <input type="text" id="f-adresse" placeholder="1881 NW 20th St, Miami, FL 33142" style="width:360px;text-align:left"></div>
  <div class="champ"><span>Téléphone</span>
    <input type="text" id="f-tel" placeholder="+1 305 …" style="width:300px;text-align:left"></div>
  <div class="champ"><span>Email sur la facture</span>
    <input type="text" id="f-email" placeholder="perfumestradellc@gmail.com" style="width:300px;text-align:left"></div>
  <div class="champ"><span>N° de Sales Tax (Florida certificate)</span>
    <input type="text" id="f-taxid" placeholder="23-…" style="width:300px;text-align:left"></div>
  <div class="champ"><span>Taux de sales tax appliqué (%)</span>
    <input type="number" id="f-taux" step="0.01" min="0" max="20" placeholder="7"></div>
  <div class="champ"><span>Frais si paiement par carte (%)</span>
    <input type="number" id="f-carte" step="0.1" min="0" max="10" placeholder="2.6"></div>
  <div class="champ"><span>Coordonnées Zelle (imprimées sur les factures à payer)</span>
    <input type="text" id="f-zelle" placeholder="Zelle : perfumestradellc@gmail.com" style="width:360px;text-align:left"></div>
  <div class="champ"><span>Préfixe des numéros de facture</span>
    <input type="text" id="f-prefixe" placeholder="PT" style="width:120px"></div>
  <div class="champ"><span>Conditions (pied de facture)</span>
    <input type="text" id="f-conditions" placeholder="Paiement à réception. Marchandise ni reprise ni échangée." style="width:420px;text-align:left"></div>
  <div class="champ"><span>Mention pour les clients exonérés</span>
    <input type="text" id="f-exo" placeholder="Sale for resale — Florida Annual Resale Certificate on file." style="width:420px;text-align:left"></div>
</section>

<section class="rg">
  <header><h2>Écrire aux clients et aux fournisseurs</h2>
    <p>Sert au bouton <b>Écrire</b> des fiches. Perfumes Trade ne peut pas envoyer un email
    à ta place — pour ça il faudra le serveur. Ce qu'il fait : ouvrir ta messagerie avec le
    message déjà écrit, à ton nom, et te laisser appuyer sur Envoyer.</p></header>
  <div class="champ"><span>Ton nom, en bas des messages</span>
    <input type="text" id="r-sign" placeholder="Sam — Perfumes Trade"
      style="width:260px;text-align:left"></div>
  <div class="champ"><span>Ton adresse email</span>
    <input type="text" id="r-mail" placeholder="sam@perfumestrade.com"
      style="width:260px;text-align:left"></div>
  <div class="champ"><span>Ton téléphone WhatsApp</span>
    <input type="text" id="r-tel" placeholder="+1 305 555 0100"
      style="width:260px;text-align:left"></div>
  <div class="champ"><span>Quand j'appuie sur « Ouvrir l'email »</span>
    <select id="r-boite" style="width:260px;text-align:left">
      <option value="defaut">Ouvrir mon logiciel de mail (Mail, Outlook…)</option>
      <option value="gmail">Ouvrir Gmail dans le navigateur</option>
      <option value="outlook">Ouvrir Outlook.com dans le navigateur</option>
    </select></div>
  <div class="champ"><span style="max-width:none">Si tu lis ton courrier dans Gmail, choisis
    <b>Gmail</b> : le message s'ouvre dans une fenêtre de rédaction Gmail, déjà remplie, depuis
    ton adresse. C'est ce qui ressemble le plus à « envoyer depuis mon email » sans serveur.</span></div>
</section>

<div class="pied">
  <button class="btn" id="def">Revenir aux valeurs de départ</button>
  <span class="msg" id="msg"></span>
  <span style="margin-left:auto"><a class="btn pri" href="tableau.html">Voir le tableau de bord</a></span>
</div>
</div>
'''

JS = r'''
const IDX=__IDX__;
const KREG='reglages-v1', KJOU='crm-journal-v1', KMOD='fiches-modifiees-v1', KEXT='stock-externe-v1';
const CANAUX_DEF=[{id:'boutique',nom:'Boutique',maj:0,com:0},{id:'site',nom:'Site perfumestrade.com',maj:0,com:3},
  {id:'shopify',nom:'Shopify',maj:0,com:3},{id:'amazon',nom:'Amazon',maj:18,com:15},{id:'perfumecity',nom:'Perfume City',maj:0,com:0}];
const DEF={seuilQte:3,capMin:0,baissePct:30,baisseJours:30,margeMin:10,societe:'DASY LLC',
  canaux:CANAUX_DEF, signature:'', monMail:'', monTel:'', boite:'defaut',
  fact:{raison:'',enseigne:'Perfumes Trade',adresse:'',tel:'',email:'',taxid:'',taux:7,carte:2.6,zelle:'',prefixe:'PT',conditions:'',exo:'Sale for resale — Florida Annual Resale Certificate on file.',logo:''}};
let REG=Object.assign({},DEF);
try{ const r=JSON.parse(localStorage.getItem(KREG)||'null'); if(r) REG=Object.assign({},DEF,r); }catch(e){}
base(KREG,REG);
(function(){ try{ const K='canaux-ebay-perfumecity-v1'; if(localStorage.getItem(K)) return;
  if(Array.isArray(REG.canaux)){ REG.canaux=REG.canaux.filter(c=>c.id!=='ebay');
    if(!REG.canaux.some(c=>c.id==='perfumecity')) REG.canaux.push({id:'perfumecity',nom:'Perfume City',maj:0,com:0});
    localStorage.setItem(KREG,JSON.stringify(REG)); }
  localStorage.setItem(K,'1'); }catch(e){} })();
try{ const v=localStorage.getItem('seuil-stock-faible-v1');
  if(v!==null && !localStorage.getItem(KREG)) REG.seuilQte=+v; }catch(e){}
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
function baisses(){
  const lim=Date.now()-REG.baisseJours*86400000, mv={};
  JOU.forEach(e=>{
    if(new Date(e.t).getTime()<lim) return;
    if((e.act==='import'||e.act==='reception'||e.act==='vente'||e.act==='annulation')&&e.det) e.det.forEach(d=>{ (mv[d.bc]=mv[d.bc]||[]).push([d.av,d.ap]); });
    else if(e.act==='stock'&&e.bc&&e.av!=null&&e.ap!=null) (mv[e.bc]=mv[e.bc]||[]).push([e.av,e.ap]);
    else if(e.act==='verif'&&0){}
  });
  const out=[];
  Object.entries(mv).forEach(([bc,l])=>{
    const av=l[0][0], ap=l[l.length-1][1];
    if(av<=0||ap>=av) return;
    const pct=(av-ap)/av*100;
    if(pct< REG.baissePct) return;
    const p=ART.find(x=>x.bc===bc); if(!p) return;
    out.push({p,av,ap,pct});
  });
  return out.sort((a,b)=>b.pct-a.pct);
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
  $('e-qte').innerHTML = REG.seuilQte<=0
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

  // filtre capital
  const sansFiltre=enStock.filter(p=>REG.seuilQte>0&&p.qte<REG.seuilQte);
  $('e-cap').innerHTML = REG.capMin<=0
    ? `<div class="eff">Filtre désactivé : les <b>${nf(sansFiltre.length)}</b> références sous le seuil
       remontent toutes, y compris celles qui ne pèsent que quelques dollars.</div>`
    : `<div class="eff">Le filtre écarte <b>${nf(sansFiltre.length-touchees().length)}</b> référence${sansFiltre.length-touchees().length>1?'s':''}
       de trop faible valeur. Il en reste <b>${nf(touchees().length)}</b>.</div>`;

  // baisses
  const b=baisses();
  const nmv=JOU.filter(e=>['import','stock','reception','vente','annulation'].includes(e.act)).length;
  $('e-bai').innerHTML = !nmv
    ? `<div class="eff">Aucun mouvement de stock n'a encore été enregistré, donc aucune baisse à détecter.
       Cette alerte s'activera dès la première mise à jour du stock ou le premier comptage.</div>`
    : `<div class="eff ${b.length?'bof':'bon'}"><b>${nf(b.length)} référence${b.length>1?'s':''}</b>
       ${b.length>1?'ont':'a'} baissé de plus de ${REG.baissePct} % sur ${REG.baisseJours} jours.</div>
       ${b.length?`<ul class="exs">${b.slice(0,5).map(x=>`<li>
         <span class="mq">${esc(x.p.marque||'')}</span><span class="nm">${esc(x.p.nom||'')}</span>
         <span class="n">${x.av} → ${x.ap} · −${Math.round(x.pct)} %</span></li>`).join('')}</ul>`:''}`;

  // marge
  const mm=enStock.filter(p=>p.pvw!=null&&p.pa!=null&&p.pvw>0&&((p.pvw-p.pa)/p.pvw*100)<REG.margeMin);
  const cm=mm.reduce((a,p)=>a+cap(p),0);
  $('e-mg').innerHTML=`<div class="eff ${mm.length/tot>0.15?'bof':''}"><b>${nf(mm.length)} référence${mm.length>1?'s':''}</b>
    passent sous ${REG.margeMin} % de marge de gros, soit <b>${money(cm)}</b> de marchandise.</div>`;
  $('src').innerHTML=`${nf(touchees().length)} alerte${touchees().length>1?'s':''} de stock<br>${nf(tot)} références en stock`;
}

/* ---- canaux ---- */
const r2=v=>Math.round(v*100)/100;
function dessineCanaux(){
  if(!Array.isArray(REG.canaux)||!REG.canaux.length) REG.canaux=JSON.parse(JSON.stringify(CANAUX_DEF));
  const pa=50, pvr=89;
  $('canaux').innerHTML=REG.canaux.map((c,i)=>{
    const v=r2(pvr*(1+(c.maj||0)/100)), net=(v*(1-(c.com||0)/100)-pa)/v*100;
    const den=1-(c.com||0)/100-REG.margeMin/100, pl=den>0?r2(pa/den):null;
    return `<tr data-i="${i}">
      <td><input type="text" data-k="nom" value="${esc(c.nom)}"></td>
      <td class="r">+ <input type="number" data-k="maj" min="-50" max="200" step="1" value="${c.maj||0}"> %</td>
      <td class="r"><input type="number" data-k="com" min="0" max="60" step="0.1" value="${c.com||0}"> %</td>
      <td class="r ex"><b>${v.toFixed(2).replace('.',',')} $</b></td>
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

const champs=[['r-qte','seuilQte'],['r-cap','capMin'],['r-bp','baissePct'],['r-bj','baisseJours'],['r-mg','margeMin']];
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
                margeMin:'marge minimum exigée'};
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
 ['f-prefixe','prefixe','préfixe des factures'],['f-conditions','conditions','conditions'],['f-exo','exo','mention exonération']].forEach(([id,k,lib])=>{
  const el=$(id); if(!el) return;
  el.value=REG.fact[k]==null?'':REG.fact[k];
  el.addEventListener('input',()=>{
    const av=REG.fact[k]; let v=el.value.trim();
    if(el.type==='number') v=v===''?'':+v;
    REG.fact[k]=v; logReg('reg-fact-'+k,'facture — '+lib,av,v); sauve(); });
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
'''

html = coquille("Réglages", "Réglages",
  "À partir de quand veux-tu être prévenu. Chaque réglage affiche en direct le nombre de "
  "références qu'il déclenche : tu vois tout de suite si tu crées une alerte utile ou du bruit.",
  CSS, CORPS, JS, donnees=('produits',)).replace('__IDX__', 'Object.fromEntries(D_TOUS().map(r=>[r[15],[r[0],r[13],r[2],r[12],r[6],r[8],r[7]]]))')
open('reglages.html','w').write(html)
print('reglages.html',len(html)//1024,'Ko')
