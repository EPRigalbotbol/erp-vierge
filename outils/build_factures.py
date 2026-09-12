# -*- coding: utf-8 -*-
"""Rubrique Factures : un PDF ou un texte collé -> le stock, les prix, les fournisseurs,
les clients et le journal se mettent à jour. Lecture du PDF entièrement locale (pdf.js embarqué)."""
import json
from build_crm import coquille
import _donnees
import _lire
C=json.load(open('cat.json'))
IDX={r[15]:[r[0],r[13],r[2],r[12],r[6],r[8],r[7]] for r in C}   # cle -> bc,nom,marque,pa,qte,pvw,pvr
PDF_MAIN=open('_pdfjs/package/build/pdf.min.mjs').read()
PDF_WORKER=open('_pdfjs/package/build/pdf.worker.min.mjs').read()

CSS = r'''
.tb input.ed{width:78px;padding:5px 7px;border:1px solid var(--line);border-radius:6px;font:inherit;font-size:13px;text-align:right;background:var(--surface)}
.tb input.ed:focus{border-color:var(--iris);outline:0}
.tb tr.corr td{background:var(--iris-soft)}
.tb .sup{color:var(--ink-3);margin-left:6px;text-decoration:none;font-size:14px}.tb .sup:hover{color:var(--crit)}
.ecr{font-size:12.5px;color:var(--ink-3)}
.sous{margin:5px 0 0;font-size:14px;color:var(--ink-2);max-width:76ch;line-height:1.5}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:1px;
background:var(--line-2);border:1px solid var(--line);border-radius:10px;overflow:hidden;margin-bottom:22px;
box-shadow:0 1px 2px rgba(0,0,0,.04)}
.kpi{background:var(--surface);padding:15px 17px;display:flex;flex-direction:column;gap:3px}
.kpi .v{font-size:24px;font-weight:700;line-height:1;letter-spacing:-.03em}
.kpi .k{font-size:12px;color:var(--ink-3);line-height:1.4}
.kpi.iris .v{color:var(--iris)} .kpi.good .v{color:var(--good)} .kpi.warm .v{color:var(--warn)}

.imp{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:22px 24px;
display:flex;flex-direction:column;gap:16px;margin-bottom:28px}
.sens{display:inline-flex;gap:3px;background:var(--surface-2);border:1px solid var(--line);
border-radius:10px;padding:3px;align-self:flex-start}
.sens button{background:none;border:0;border-radius:8px;padding:9px 16px;font-family:inherit;
font-size:13.5px;font-weight:600;color:var(--ink-3);cursor:pointer;display:flex;flex-direction:column;
align-items:flex-start;gap:1px;line-height:1.25}
.sens button small{font-weight:500;font-size:11.5px;color:var(--ink-3)}
/* Le bouton choisi etait a peine plus clair que les deux autres : on ne savait
   pas dans quel mode on se trouvait, donc pas ce que l'enregistrement allait
   faire au stock. Il est maintenant PLEIN, dans la couleur du sens. */
.sens button.on{color:#fff;box-shadow:0 1px 4px rgba(0,0,0,.18)}
.sens button.on small{color:rgba(255,255,255,.82)}
.sens button.on.a{background:var(--good)}
.sens button.on.v{background:var(--iris)}
.sens button.on.c{background:var(--warn)}
/* ---- la phrase qui dit ce qui va se passer ----
   Trois onglets et un formulaire identique en dessous : rien n'annoncait la
   consequence. Cette bande la dit en toutes lettres, dans la couleur du mode. */
.quoi{display:flex;align-items:flex-start;gap:11px;border-radius:9px;padding:12px 15px;
font-size:13.5px;line-height:1.55;border-left:3px solid}
.quoi .fl{font-size:17px;line-height:1.1;flex:none}
.quoi b{font-weight:700}
.quoi.a{background:var(--good-soft);border-color:var(--good);color:var(--ink-2)}
.quoi.a b{color:var(--good)}
.quoi.v{background:var(--iris-soft);border-color:var(--iris);color:var(--ink-2)}
.quoi.v b{color:var(--iris)}
.quoi.c{background:var(--warn-soft);border-color:var(--warn);color:var(--ink-2)}
.quoi.c b{color:var(--warn)}
.canal{display:flex;align-items:center;gap:12px;flex-wrap:wrap;background:var(--warn-soft);border-radius:9px;
padding:11px 14px;font-size:12.5px;color:var(--ink-2);line-height:1.5}
.canal label{font-size:11px;letter-spacing:.09em;text-transform:uppercase;color:var(--ink-2);font-weight:700}
.canal select{font-family:inherit;font-size:13.5px;padding:7px 10px;border:1px solid var(--line);border-radius:7px;
background:var(--surface);color:var(--ink)}
.canal span{flex:1 1 320px}
.tag.c{background:var(--warn-soft);color:var(--warn)}
.dz{border:2px dashed var(--line-3);border-radius:11px;padding:26px 22px;text-align:center;
background:var(--surface-2);cursor:pointer;transition:border-color .12s,background .12s;position:relative}
.dz:hover,.dz.sur{border-color:var(--iris);background:var(--iris-soft)}
.dz b{display:block;font-size:15px;font-weight:700;margin-bottom:4px}
.dz span{font-size:12.5px;color:var(--ink-3)}
.dz input{position:absolute;inset:0;opacity:0;cursor:pointer;width:100%;height:100%}
.dz.lu{border-style:solid;border-color:var(--good);background:var(--good-soft)}
.dz.lu b{color:var(--good)}
.txt{display:none;flex-direction:column;gap:6px}
.txt.on{display:flex}
.txt textarea{width:100%;min-height:150px;font-family:inherit;font-size:12.5px;border:1px solid var(--line);
border-radius:8px;padding:11px;background:var(--surface-2);color:var(--ink);resize:vertical;line-height:1.55}
.txt textarea:focus{outline:0;border-color:var(--iris);box-shadow:0 0 0 3px var(--iris-soft);background:var(--surface)}
.lnk{background:none;border:0;padding:0;font-family:inherit;font-size:12.5px;color:var(--iris);
text-decoration:underline;cursor:pointer;align-self:flex-start}
.ent{display:grid;grid-template-columns:1.6fr 1fr 1fr;gap:12px}
@media(max-width:700px){.ent{grid-template-columns:1fr}}
.fld{display:flex;flex-direction:column;gap:5px}
.fld label{font-size:11px;letter-spacing:.09em;text-transform:uppercase;color:var(--ink-2);font-weight:700}
.fld input{font-family:inherit;font-size:14.5px;padding:9px 11px;border:1px solid var(--line);border-radius:7px;
background:var(--surface);color:var(--ink)}
.fld input:focus{outline:0;border-color:var(--iris);box-shadow:0 0 0 3px var(--iris-soft)}
.fld input.auto{border-color:var(--good);background:var(--good-soft)}
.fld small{font-size:11px;color:var(--good);font-weight:600}
.opts{display:flex;flex-direction:column;gap:9px}
.chk{display:flex;gap:10px;align-items:flex-start;font-size:13.5px;color:var(--ink-2);line-height:1.5;cursor:pointer}
.chk input{margin-top:3px;flex:0 0 auto;width:16px;height:16px}
.chk b{color:var(--ink)}
.ap{display:grid;grid-template-columns:repeat(auto-fit,minmax(128px,1fr));gap:1px;background:var(--line);
border:1px solid var(--line);border-radius:9px;overflow:hidden}
.ap div{background:var(--surface);padding:11px 13px;display:flex;flex-direction:column;gap:2px}
.ap .v{font-size:20px;font-weight:700;line-height:1;letter-spacing:-.025em}
.ap .k{font-size:11.5px;color:var(--ink-3)}
.tb{width:100%;border-collapse:collapse;font-size:13px}
.tb th{text-align:left;font-size:9.5px;letter-spacing:.11em;text-transform:uppercase;color:var(--ink-2);
font-weight:700;padding:9px 10px;border-bottom:1px solid var(--line);white-space:nowrap}
.tb th.r{text-align:right}
.tb td{padding:9px 10px;border-bottom:1px solid var(--line-2);vertical-align:middle}
.tb tbody tr:nth-child(even){background:var(--surface-2)}
.tb td.r{text-align:right;white-space:nowrap;font-weight:600}
.tb .ref b{display:block;font-weight:700}
.tb .ref span{color:var(--ink-3);font-size:11px}
.tb .mq{font-size:10.5px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:var(--iris)}
.tb .plus{color:var(--good)} .tb .moins{color:var(--crit)}
.tb tr.inc td{background:var(--warn-soft)}
.tb tr.neg td{background:var(--crit-soft)}
.mv{font-size:12.5px;white-space:nowrap}
.mv b{font-size:14px}
.mapbox{border:1px solid var(--line);border-radius:9px;background:var(--surface-2);margin:0 0 12px;padding:0}
.mapbox summary{cursor:pointer;padding:9px 13px;font-size:12.5px;color:var(--iris);font-weight:600;list-style:none}
.mapbox summary::-webkit-details-marker{display:none}
.mapbox summary:before{content:'\25B8 ';display:inline-block;transition:transform .12s}
.mapbox[open] summary:before{transform:rotate(90deg)}
.mapg{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:9px;padding:0 13px 13px}
.mapg .mp{display:flex;flex-direction:column;gap:3px;font-size:11.5px;color:var(--ink-3)}
.mapg .mp select{font-family:inherit;font-size:12.5px;padding:6px 8px;border:1px solid var(--line);
border-radius:7px;background:var(--surface);color:var(--ink);max-width:100%}
.av{background:var(--warn-soft);border-left:3px solid var(--warn);border-radius:0 7px 7px 0;
padding:11px 15px;font-size:13px;color:var(--ink-2);line-height:1.6}
.av.c{background:var(--crit-soft);border-left-color:var(--crit)}
.av b{color:var(--ink)}
.actions{display:flex;gap:10px;align-items:center;flex-wrap:wrap;padding-top:6px;border-top:1px solid var(--line-2)}
.actions .msg{font-size:13px;color:var(--crit);font-weight:600}
.btn:disabled{opacity:.45;cursor:not-allowed}
.actions .ok{color:var(--good)}
.spacer{flex:1}

h2.sec{font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:var(--ink);font-weight:700;
margin:8px 0 13px;padding-bottom:9px;border-bottom:1px solid var(--line);
display:flex;justify-content:space-between;align-items:baseline;gap:12px;flex-wrap:wrap}
h2.sec em{font-style:normal;font-size:12.5px;letter-spacing:0;text-transform:none;color:var(--ink-3);font-weight:400}
.hist{width:100%;border-collapse:collapse;font-size:13.5px;background:var(--surface);
border:1px solid var(--line);border-radius:10px;overflow:hidden}
.hist th{text-align:left;font-size:9.5px;letter-spacing:.11em;text-transform:uppercase;color:var(--ink-2);
font-weight:700;padding:11px 13px;background:var(--surface-2);border-bottom:1px solid var(--line);white-space:nowrap}
.hist th.r{text-align:right}
.hist td{padding:12px 13px;border-bottom:1px solid var(--line-3);vertical-align:middle}
.hist tbody tr:nth-child(even){background:var(--surface-2)}
.hist tbody tr:last-child td{border-bottom:0}
.hist td.r{text-align:right;white-space:nowrap;font-weight:700}
.tag{display:inline-flex;align-items:center;gap:6px;font-size:11px;font-weight:700;padding:4px 10px 4px 8px;
border-radius:20px;white-space:nowrap;line-height:1}
.tag::before{content:"";width:6px;height:6px;border-radius:50%;background:currentColor}
.tag.a{background:var(--good-soft);color:var(--good)} .tag.v{background:var(--iris-soft);color:var(--iris)}
.tag.s{background:var(--surface-2);color:var(--ink-3)}
.hist .tiers b{display:block;font-weight:700}
.hist .tiers span{color:var(--ink-3);font-size:11.5px}
.hist .x{background:none;border:1px solid var(--line);border-radius:6px;padding:5px 10px;font-family:inherit;
font-size:12px;color:var(--ink-2);cursor:pointer}
.hist .x:hover{border-color:var(--crit);color:var(--crit)}
/* ---- les factures rangees par canal ---- */
.grp{margin:0 0 18px}
.grp h3{display:flex;align-items:baseline;gap:10px;flex-wrap:wrap;margin:0 0 8px;
font-size:14px;font-weight:700;letter-spacing:-.01em;color:var(--ink)}
.grp h3 .cpt{font-family:Inter,sans-serif;font-size:11.5px;font-weight:500;color:var(--ink-3)}
.grp h3 .tot{margin-left:auto;font-size:14px;font-weight:700;font-variant-numeric:tabular-nums}
.hist tbody tr.cl{cursor:pointer}
.hist tbody tr.cl:hover td{background:var(--iris-soft)}
.hist td .fl{color:var(--ink-3);font-size:11px}
/* ---- le detail d'une facture ---- */
#dov{position:fixed;inset:0;background:rgba(20,18,26,.5);z-index:9000;display:none;
overflow:auto;padding:24px 14px}
#dov.on{display:block}
.dw{max-width:820px;margin:0 auto;background:var(--surface);border-radius:12px;
border:1px solid var(--line);overflow:hidden;box-shadow:0 20px 60px rgba(0,0,0,.3)}
.dw .dt{display:flex;align-items:flex-start;gap:14px;padding:18px 22px;border-bottom:1px solid var(--line)}
.dw .dt h3{margin:0;font-size:18px;letter-spacing:-.015em}
.dw .dt p{margin:4px 0 0;font-size:13px;color:var(--ink-2)}
.dw .dt .ferm{margin-left:auto;background:none;border:1px solid var(--line);border-radius:7px;
padding:6px 12px;font:inherit;font-size:13px;color:var(--ink-2);cursor:pointer}
.dw .dt .ferm:hover{border-color:var(--ink-3);color:var(--ink)}
.dw .db{padding:18px 22px}
.dw table{width:100%;border-collapse:collapse;font-size:13px}
.dw th{text-align:left;font-size:9.5px;letter-spacing:.11em;text-transform:uppercase;
color:var(--ink-3);padding:0 10px 8px;border-bottom:1px solid var(--line)}
.dw th.r{text-align:right}
.dw td{padding:9px 10px;border-bottom:1px solid var(--line-3);vertical-align:top}
.dw td.r{text-align:right;white-space:nowrap;font-variant-numeric:tabular-nums}
.dw tr:last-child td{border-bottom:0}
.dw td small{display:block;color:var(--ink-3);font-size:11px;font-family:"IBM Plex Mono",monospace}
.dw .stk{font-size:11.5px;color:var(--ink-3);white-space:nowrap}
.dw .tot2{display:flex;justify-content:flex-end;gap:26px;padding:14px 22px;
border-top:1px solid var(--line);background:var(--surface-2);font-size:14px}
.dw .tot2 b{font-variant-numeric:tabular-nums}
.vide{border:2px dashed var(--line);border-radius:11px;padding:30px 28px;text-align:center;
background:var(--surface-2);max-width:66ch;margin:0 auto}
.vide p{margin:0;font-size:14px;color:var(--ink-2);line-height:1.65}
'''

CORPS = r'''
<div id="kpis"></div>

<section class="imp">
  <div class="sens" id="sens">
    <button data-s="achat" class="on a">Achat<small>réception de marchandise · le stock augmente</small></button>
    <button data-s="vente" class="v">Vente<small>facture émise · le stock baisse</small></button>
    <button data-s="canal" class="c">Importer des ventes<small>fichier exporté depuis Shopify, Amazon, Perfume City, WooCommerce, la caisse · le stock baisse</small></button>
  </div>
  <div class="quoi" id="quoi"></div>

  <div class="canal" id="canal" hidden>
    <label>Canal</label>
    <select id="canal-nom">
      <option>Shopify</option><option>WooCommerce</option><option>Amazon</option><option>Perfume City</option>
      <option>Caisse Lightspeed</option><option>Autre</option></select>
    <span>Dépose ici le fichier CSV des commandes, exporté depuis ce canal. Les colonnes sont
    reconnues par leur nom ; une commande déjà importée n'est jamais comptée deux fois, même si
    deux fichiers se chevauchent.</span>
  </div>

  <div class="canal" id="canalv" hidden>
    <label>Canal</label>
    <select id="canal-vente">
      <option>Boutique</option><option>Gros</option><option>Site perfumestrade.com</option>
      <option>Shopify</option><option>Amazon</option><option>Perfume City</option>
      <option>Caisse Lightspeed</option><option>Autre</option></select>
    <span>Sur quel canal cette vente a-t-elle été faite ? Le <a href="ventes.html">journal des ventes</a>
    classe chaque vente par canal.</span>
  </div>

  <div class="dz" id="dz">
    <b>Dépose la facture ici — PDF ou photo —, ou clique pour la choisir</b>
    <span>PDF, photo, scan, Excel (.xlsx), CSV — tout se lit, entièrement sur cet ordinateur :
    rien n'est envoyé nulle part. Une photo prise droite et nette se lit bien ; l'aperçu
    ci-dessous montre toujours ce qui a été lu avant d'enregistrer quoi que ce soit.</span>
    <input type="file" id="fichier" accept="__ACCEPT__">
  </div>
  <button class="lnk" id="basc">…ou coller le texte de la facture</button>
  <div class="txt" id="txt"><textarea id="colle" placeholder="Colle ici les lignes de la facture : un code-barres et un prix par ligne au minimum."></textarea></div>

  <div class="ent">
    <div class="fld"><label id="l-tiers">Fournisseur</label><input id="tiers" list="l-noms" autocomplete="off" placeholder="Tape un nom — nouveau ou existant"><datalist id="l-noms"></datalist><small id="a-tiers" hidden>reconnu dans la facture</small><small id="n-tiers" hidden></small></div>
    <div class="fld"><label>Date</label><input id="date" type="date"><small id="a-date" hidden>lue dans la facture</small></div>
    <div class="fld"><label>Numéro</label><input id="num" placeholder="MPSINV79971"><small id="a-num" hidden>lu dans la facture</small></div>
  </div>

  <div class="opts">
    <label class="chk"><input type="checkbox" id="o-stock" checked>
      <span><b>Mettre le stock à jour</b> — <span id="o-stock-lib">ajouter les quantités reçues</span>.
      Décoche si cette marchandise est déjà comptée dans le stock actuel.</span></label>
    <label class="chk" id="w-prix"><input type="checkbox" id="o-prix" checked>
      <span><b>Adopter ces prix comme nouveau prix d'achat</b> — c'est ce qu'on attend d'une facture récente.</span></label>
  </div>

  <div id="apercu"></div>

  <div class="actions">
    <span class="msg" id="msg"></span><span class="spacer"></span>
    <button class="btn" id="raz">Vider</button>
    <button class="btn pri" id="ok" disabled>Enregistrer la facture</button>
  </div>
</section>

<h2 class="sec">Factures enregistrées <em id="nbf"></em></h2>
<div id="liste"></div>

<div id="dov"><div class="dw">
  <div class="dt"><div><h3 id="d-num"></h3><p id="d-sous"></p></div>
    <button class="ferm" id="d-ferm">Fermer</button></div>
  <div class="db" id="d-corps"></div>
  <div class="tot2" id="d-tot"></div>
</div></div>
'''

JS = r'''
const IDX=__IDX__;
const K={reg:'reglages-v1',mod:'fiches-modifiees-v1',ext:'stock-externe-v1',hist:'prix-achat-hist-v1',
         vent:'ventes-v1',frn:'fournisseurs-v1',cli:'clients-v1',fact:'factures-v1',jou:'crm-journal-v1',
         usr:'crm-utilisateur-v1',faci:'factures-installees-v1'};
let REG=Object.assign({seuilQte:3,capMin:0,baissePct:30,baisseJours:30,margeMin:10,societe:'DASY LLC'},lit(K.reg,{}));
let MOD=lit(K.mod,{}), EXT=lit(K.ext,{q:{}}), HIST=lit(K.hist,{}), VENT=lit(K.vent,{}),
    FRN=lit(K.frn,{}), CLI=lit(K.cli,{}), FACT=lit(K.fact,[]), JOU=lit(K.jou,[]);
let USR=NOM_UTIL;
window.__nomChange.push(v=>{ USR=v; try{ majUser(); }catch(e){} });
if(!EXT.q) EXT.q={};

function demandeUser(){ return USR; }   /* jamais de fenetre a l'enregistrement : le nom se regle dans la barre laterale */
function majUser(){ try{ piedSession(); }catch(e){} }

/* quantité effective : fichier -> tableur importé -> corrections a la main */
function qteEff(cle){
  const b=IDX[cle]; if(!b) return 0;
  let q=b[4]; const e=EXT.q[b[0]]; if(e!==undefined&&e!==null) q=e;
  const m=MOD[cle]; if(m&&m.qte!=null) q=m.qte;
  return q;
}
const paEff=cle=>{ const m=MOD[cle]; return (m&&m.pa!=null)?m.pa:(IDX[cle]?IDX[cle][3]:null); };
/* une ligne au journal, signée par le compte connecté (fonction perdue lors du passage aux comptes :
   l'enregistrement d'une facture plantait avant d'écrire quoi que ce soit) */
function log(e){ JOU.push(Object.assign({t:new Date().toISOString(),u:USR||'(non renseigné)'},e)); ecrit(K.jou,JOU); }
const parBC={}; Object.entries(IDX).forEach(([cle,v])=>{ parBC[v[0]]=cle; });
/* les autres codes-barres déclarés sur une fiche (même parfum, autre lot ou coffret) */
function aliasBC(){ Object.entries(MOD).forEach(([cle,m])=>{ if(!m||!m.bcs||!IDX[cle]) return;
  String(m.bcs).split(/[^0-9]+/).filter(x=>x.length>=6).forEach(b=>{ if(!parBC[b]) parBC[b]=cle; }); }); }
aliasBC();
function trouve(bc){
  const c=[bc,bc.replace(/^0+/,''),bc.padStart(12,'0'),bc.padStart(13,'0')];
  for(const x of c){ if(parBC[x]) return parBC[x]; }
  const nu=bc.replace(/^0+/,'');
  const k=Object.keys(parBC).find(b=>b.replace(/^0+/,'')===nu); return k?parBC[k]:null;
}

/* ---------------- lecture d'une facture ---------------- */
const normBC=v=>{ const d=String(v==null?'':v).replace(/[^0-9]/g,''); return (d.length>=8&&d.length<=14)?d:''; };
function litLignes(txt){
  const out=[];
  txt.replace(/\r/g,'').split('\n').forEach(l=>{
    if(!l.trim()) return;
    l=l.replace(/\((\d{4,})\)/g,' ');
    const ch=l.split(/\t|;|\s{2,}|\|/).map(x=>x.trim()).filter(x=>x!=='');
    const plat=ch.length>=3?ch:l.trim().split(/\s+/);
    let bc='',iBc=-1;
    for(let i=0;i<plat.length;i++){ const b=normBC(plat[i]); if(b&&b.length>=11){ bc=b;iBc=i;break; } }
    /* sans code-barres : une facture ne se lit pas (on n'enregistre rien sur un
       nom deviné), mais un devis, si — il y a un nom et un prix, le nom fera le lien */
    if(!bc && !(DOC==='devis' && /[A-Za-zÀ-ÿ]{3}/.test(l) && /\d/.test(l))) return;
    const nums=[];
    plat.forEach((x,i)=>{ if(i===iBc) return;
      if(/^\d{6,}$/.test(x.replace(/[^0-9]/g,''))&&!/[.,]\d{2}$/.test(x)) return;
      const v=nombre(x); if(v!=null&&v>0) nums.push({v,i,dec:/[.,]\d{2}\b/.test(x)}); });
    if(!nums.length) return;
    let q=null,p=null;
    for(const a of nums){ if(!Number.isInteger(a.v)||a.v>5000) continue;
      for(const b of nums){ if(b.i===a.i||b.v<=0||b.v>4000) continue; const t=a.v*b.v;
        if(nums.some(c=>c.i!==a.i&&c.i!==b.i&&Math.abs(c.v-t)<=Math.max(0.6,t*0.004))){ q=a.v;p=b.v;break; } }
      if(p!=null) break; }
    if(p==null){ let c=nums.filter(x=>x.dec&&x.v>0.5&&x.v<4000);
      if(!c.length) c=nums.filter(x=>x.v>0.5&&x.v<4000&&!(Number.isInteger(x.v)&&x.v<=60&&x.i===0));
      if(!c.length) return; p=c[c.length-1].v;
      const e=nums.find(x=>Number.isInteger(x.v)&&x.v<=5000&&x.i<c[c.length-1].i&&x.v!==p&&x.i!==0); q=e?e.v:null; }
    const mots=plat.filter((x,i)=>i!==iBc&&/[A-Za-zÀ-ÿ]{3}/.test(x)); mots.sort((a,b)=>b.length-a.length);
    out.push({bc,des:(mots[0]||'').slice(0,80),q,p});
  });
  return out;
}
/* Un fichier à colonnes nommées (CSV, TSV) n'est pas un texte de facture : on lit ses
   en-têtes plutôt que de deviner. Sans en-tête reconnaissable, on rend null et on repasse
   à la lecture heuristique. Ça évite qu'un relevé de prix soit pris pour une facture. */
const H_BC=['code_barres','code-barres','codebarres','code barre','barcode','ean','upc','gtin','sku','ugs','reference','référence','ref'];
const H_Q =['quantite','quantité','qte','qté','qty','quantity','units','unites','unités','nb_pieces','pieces','pcs','ordered'];
const H_P =['prix_achat','prix achat','prix unitaire','prix_unitaire','prix','unit price','unit cost','price','cost','pu','tarif','prix_vente','prix vente'];
const H_D =['designation','désignation','description','nom','name','produit','product','item','libelle','libellé','article'];
const H_T =['total','montant','amount','line total','total ligne'];
/* Cette lecture sert deux pages : les factures fournisseurs et l'Étude de devis. Les
   messages d'erreur doivent nommer le bon document, sinon on lit « ce n'est pas une
   facture » sur la page des devis et on ne comprend plus rien. */
const DOC=(typeof DOC_PAGE==='string')?DOC_PAGE:'facture';
const UN_DOC=DOC==='devis'?'un devis':'une facture';
/* Un export d'annonces (le catalogue d'un site : WooCommerce, Shopify, Amazon) ressemble
   de loin à un tableau de prix, et il a bien un code-barres et un prix. Mais ce sont NOS
   annonces, pas la proposition d'un fournisseur. On le reconnaît à ses colonnes de mise en
   vente — publication, visibilité, photos, catégories — qu'aucun devis ne porte. */
const H_ANNONCE=['published','visibility in catalog','in stock?','regular price','sale price',
  'short description','tax status','tax class','sold individually?','backorders allowed?',
  'shipping class','images','cross-sells','upsells','purchase note','allow customer reviews?',
  'body (html)','variant sku','variant price','variant inventory qty','image src','handle',
  'item-name','listing-id','open-date','product-id','fulfillment-channel','item-condition'];
function litTableau(txt){
  const li=txt.replace(/\r/g,'').split('\n').filter(l=>l.trim()!=='');
  if(li.length<2) return null;
  const sep=[';','\t',','].map(c=>({c,n:li[0].split(c).length})).sort((a,b)=>b.n-a.n)[0];
  if(sep.n<3) return null;
  const dec=l=>l.split(sep.c).map(x=>x.trim().replace(/^"|"$/g,'').replace(/""/g,'"'));
  const head=dec(li[0]).map(h=>h.toLowerCase().replace(/^\ufeff/,'').trim());
  const cherche=(L)=>{ for(const m of L){ const i=head.findIndex(h=>h===m); if(i>=0) return i; }
                       for(const m of L){ const i=head.findIndex(h=>h.includes(m)); if(i>=0) return i; } return -1; };
  const iB=cherche(H_BC), iQ=cherche(H_Q), iP=cherche(H_P), iD=cherche(H_D), iT=cherche(H_T);
  /* pas de colonne code-barres : ce n'est pas un tableau de facture — sauf sur la
     page des devis, où une price list sans codes se lit par le NOM des parfums */
  const parNom = iB<0 && DOC==='devis' && iD>=0 && iP>=0;
  if(iB<0 && !parNom) return null;
  /* 1) Export d'annonces. On le nomme au lieu de dire « ce n'est pas une facture » : la
        personne a déposé un vrai fichier, elle a besoin de savoir CE QU'IL EST et pourquoi
        il n'a rien à faire ici. Trois colonnes de mise en vente suffisent à le signer. */
  const sigA=H_ANNONCE.filter(m=>head.some(h=>h===m||h.includes(m)));
  if(sigA.length>=3){
    return {err:`Ce fichier est l'export du catalogue d'une boutique en ligne — la liste de ce qui est mis en vente `+
      `(colonnes « ${sigA.slice(0,3).join(' », « ')} », photos, catégories). Ce ne sont pas des prix proposés par un fournisseur, `+
      `ce sont tes propres annonces.\n\n`+
      (DOC==='devis'
        ? `Un devis, c'est une ligne par référence avec le code-barres, la quantité proposée et le prix. Rien de tout ça ici : cette page ne peut rien en tirer.`
        : `L'enregistrer ici ajouterait du stock qui n'existe pas et écraserait des prix d'achat.`)};
  }
  /* 2) Relevé de marché. Colonnes qui n'appartiennent qu'à une veille de prix ou à un export
        de fiches Amazon. Termes forts uniquement : « catégorie », « note » ou « position »
        traînent dans trop de fichiers ordinaires pour accuser quoi que ce soit. */
  const SUSPECT=['prix_amazon','prix amazon','buy box','buybox','asin','prix_retail','prix retail',
                 'prix_gros','prix gros','rang amazon','sales rank','best sellers rank','nombre de vendeurs'];
  const trouvees=SUSPECT.filter(m=>head.some(h=>h.includes(m)));
  if(trouvees.length>=2){
    return {err:`Ce fichier n'est pas ${UN_DOC} : il contient les colonnes « ${trouvees.slice(0,4).join(' », « ')} ». `+
      `C'est un relevé de prix du marché.`+
      (DOC==='devis' ? '' : ` L'enregistrer ici écraserait des prix d'achat et ajouterait du stock qui n'existe pas.`)};
  }
  const colonnes=[['code-barres',iB],['quantité',iQ],['prix',iP],['désignation',iD],['total',iT]]
    .filter(x=>x[1]>=0).map(x=>x[0]+' → « '+dec(li[0])[x[1]]+' »').join(', ');
  if((iQ<0 && !parNom) || iP<0){
    return {err:`Ce fichier a des colonnes nommées, mais il manque `+
      (iQ<0&&iP<0?'la quantité et le prix':iQ<0?'la quantité':'le prix')+
      `. Colonnes lues : ${head.filter(Boolean).slice(0,12).join(', ')}. `+
      (DOC==='devis'
        ? `Un devis se lit s'il porte au moins un code-barres, une quantité et un prix par ligne.`
        : `Si ce n'est pas une facture (relevé de prix, liste d'annonces…), n'utilise pas cette page : rien ne doit être enregistré depuis un fichier de ce genre.`)};
  }
  const out=[];
  for(let i=1;i<li.length;i++){
    const c=dec(li[i]); if(!c.some(x=>x)) continue;
    const bc=iB>=0?normBC(c[iB]||''):'';
    const des=(iD>=0?c[iD]:'').slice(0,80);
    if(!bc && !(parNom && des.trim())) continue;
    const q=iQ>=0?nombre(c[iQ]):null, p=nombre(c[iP]);
    if(q==null&&p==null) continue;
    out.push({bc,des,q:q==null?null:q,p:p==null?null:p,
              mt:iT>=0?nombre(c[iT]):null});
  }
  if(!out.length) return {err:parNom
    ? `Colonnes reconnues (${colonnes}), mais aucune ligne exploitable : il faut au moins un nom et un prix par ligne.`
    : `Colonnes reconnues (${colonnes}), mais aucune ligne exploitable : vérifie que la colonne code-barres contient bien des codes.`};
  return {lignes:out,colonnes,entete:true};
}

/* en-tete : numero, date, tiers — devines, toujours modifiables */
function litEntete(txt){
  const o={};
  let m=txt.match(/\b([A-Z]{2,8}INV[A-Z0-9-]*\d{3,})\b/) || txt.match(/(?:Invoice|Facture|Document\s+Number|N[°º]|No\.?)\s*[:#]?\s*([A-Z]{0,6}[-\/]?\d{4,}[A-Z0-9-]*)/i);
  if(m) o.num=m[1];
  m=txt.match(/\b(\d{1,2})\/(\d{1,2})\/(\d{4})\b/);
  if(m){ let a=+m[1],b=+m[2]; const y=m[3];
    const mois = a>12 ? b : a, jour = a>12 ? a : b;        /* américain par défaut, sauf si impossible */
    o.date=`${y}-${String(mois).padStart(2,'0')}-${String(jour).padStart(2,'0')}`; }
  else { m=txt.match(/\b(\d{4})-(\d{2})-(\d{2})\b/); if(m) o.date=m[0]; }
  const soc=(REG.societe||'').toLowerCase();
  const connus=[...Object.keys(FRN),...Object.keys(CLI)];
  const bas=txt.toLowerCase();
  const c=connus.find(n=>n&&bas.includes(n.toLowerCase()));
  if(c) o.tiers=c;
  else {
    const li=txt.split('\n').map(s=>s.trim()).filter(s=>/\b(LLC|INC\.?|CORP\.?|LTD\.?|GROUP|SAS|SARL|GMBH|S\.A\.|TRADING|DISTRIBUTION|IMPORT|EXPORT)\b/i.test(s) && !(soc&&s.toLowerCase().includes(soc)));
    if(li.length) o.tiers=li[0].replace(/\s{2,}.*$/,'').replace(/\b(COMPANY|LOGO)\b/gi,'').trim().slice(0,60);
  }
  return o;
}


/* ---------------- export de ventes d'un canal ----------------
   Un export de commandes n'est pas une facture : chaque ligne porte une commande, un SKU,
   une quantité. Les colonnes sont reconnues par leur nom (Shopify, Amazon, eBay, WooCommerce,
   caisses), sinon par leur contenu. Les commandes déjà vues sont ignorées. */
const K_CMD='commandes-v1';
let CMD=lit(K_CMD,{});          // "canal|commande|sku" -> date d'import
function decoupe(txt){
  const li=txt.replace(/\r/g,'').split('\n').filter(l=>l.trim()!=='');
  if(!li.length) return [];
  const t=li[0];
  const sep = t.includes('\t') ? '\t' : ((t.match(/;/g)||[]).length > (t.match(/,/g)||[]).length ? ';' : ',');
  return li.map(l=>{ const out=[]; let cur='',q=false;
    for(let i=0;i<l.length;i++){ const c=l[i];
      if(c==='"'){ if(q&&l[i+1]==='"'){cur+='"';i++;} else q=!q; }
      else if(c===sep&&!q){ out.push(cur); cur=''; } else cur+=c; }
    out.push(cur); return out.map(x=>x.trim()); });
}
const COLS={
  sku:  [/^(lineitem )?sku$/i,/^upc$/i,/^ean$/i,/^gtin$/i,/barcode|code.?barres|code ean|codebarre/i,/custom label/i,/^(product )?(code|reference|référence)$/i,/seller.?sku/i,/^item.?sku$/i],
  qte:  [/^(lineitem )?quantity$/i,/^qty\.?$/i,/^quantit[eé]/i,/^quantity.?(purchased|sold)?$/i,/^units?( sold)?$/i,/items sold/i],
  prix: [/^(lineitem )?price$/i,/^item.?price$/i,/sold for/i,/^prix( unitaire)?$/i,/unit.?price/i,/^price$/i],
  cmd:  [/^name$/i,/^order( number| id| #)?$/i,/^(amazon-)?order-?id$/i,/^sales record number$/i,/^n[°º]? ?(de )?commande$/i,/^order$/i,/^id$/i,/receipt|ticket|transaction/i],
  date: [/^created at$/i,/^purchase-?date$/i,/^sale date$/i,/^date/i,/^order date$/i,/^paid at$/i],
  client:[/^email$/i,/^buyer.?(email|name)$/i,/^customer/i,/^billing name$/i,/^client$/i,/^buyer$/i],
  nom:  [/^(lineitem )?name$/i,/^product.?(name|title)$/i,/^title$/i,/^item title$/i,/^d[eé]signation$/i,/^description$/i],
  /* Sam a deux caisses dans la meme boutique, et Perfume City en aura une autre :
     l'export les melange. La colonne qui les distingue sert a n'importer qu'un
     magasin a la fois, sous son propre nom de canal. */
  lieu: [/^outlet$/i,/^store$/i,/^register$/i,/^location$/i,/^boutique$/i,/^magasin$/i,/^caisse$/i,/outlet name/i,/register name/i]
};
/* Le choix fait dans l'apercu : quelle colonne pour quoi, et quel magasin garder.
   Vide = ce que la lecture a devine toute seule. */
let MAP={}, LIEU='';
function reconnaitColonnes(entete){
  const idx={}; const H=entete.map(h=>h.replace(/^﻿/,'').trim());
  Object.entries(COLS).forEach(([k,pats])=>{
    for(const p of pats){ const i=H.findIndex(h=>p.test(h)); if(i>=0){ idx[k]=i; break; } } });
  /* ce que la personne a corrige a la main l'emporte sur la devinette */
  Object.entries(MAP).forEach(([k,v])=>{ if(v==='') delete idx[k]; else if(v!=null) idx[k]=+v; });
  return idx;
}
function litExport(txt){
  const R=decoupe(txt); if(R.length<2) return {err:"Il faut une ligne d'en-tête et au moins une commande."};
  const H=R[0]; let idx=reconnaitColonnes(H); const corps=R.slice(1);
  /* secours : la colonne code-barres est celle qui reconnaît le plus de références */
  if(idx.sku==null){ let best=-1,n=0;
    for(let c=0;c<H.length;c++){ const m=corps.filter(r=>{ const b=normBC(r[c]); return b&&trouve(b); }).length; if(m>n){n=m;best=c;} }
    if(n>=1) idx.sku=best; }
  if(idx.sku==null) return {err:"Aucune colonne de SKU / code-barres reconnue. Vérifie que l'export contient le code-barres du produit (SKU)."};
  if(idx.qte==null){ let best=-1,n=0;
    for(let c=0;c<H.length;c++){ if(c===idx.sku) continue;
      const m=corps.filter(r=>{ const v=nombre(r[c]); return v!=null&&Number.isInteger(v)&&v>0&&v<500; }).length; if(m>n){n=m;best=c;} }
    if(n>=1) idx.qte=best; }
  if(idx.qte==null) return {err:"Aucune colonne de quantité reconnue."};
  const canal=$('canal-nom').value;
  /* les magasins presents dans le fichier, pour n'en importer qu'un a la fois */
  let lieux=[];
  if(idx.lieu!=null) lieux=[...new Set(corps.map(r=>String(r[idx.lieu]||'').trim()).filter(Boolean))].sort();
  const lignes=[]; let deja=0, sansSku=0, sansCmd=0, retours=0, horsLieu=0;
  corps.forEach((r,i)=>{
    if(LIEU && idx.lieu!=null && String(r[idx.lieu]||'').trim()!==LIEU){ horsLieu++; return; }
    const sku=normBC(r[idx.sku]||''); if(!sku){ sansSku++; return; }
    /* une quantite negative est un retour : elle doit compter en moins, pas disparaitre */
    const q=nombre(r[idx.qte]); if(q==null||q===0) return;
    if(q<0) retours++;
    const p=idx.prix!=null?nombre(r[idx.prix]):null;
    const cmd=idx.cmd!=null?String(r[idx.cmd]||'').trim():'';
    if(!cmd) sansCmd++;
    const cleCmd=canal+'|'+(cmd||('ligne'+i))+'|'+sku;
    if(cmd && CMD[cleCmd]){ deja++; return; }
    let d=idx.date!=null?String(r[idx.date]||'').trim():'';
    let iso=''; let m=d.match(/(\d{4})-(\d{2})-(\d{2})/); if(m) iso=`${m[1]}-${m[2]}-${m[3]}`;
    else { m=d.match(/(\d{1,2})\/(\d{1,2})\/(\d{4})/); if(m){ const a=+m[1],b=+m[2]; const mo=a>12?b:a, jo=a>12?a:b; iso=`${m[3]}-${String(mo).padStart(2,'0')}-${String(jo).padStart(2,'0')}`; } }
    /* l'heure de la vente, si la colonne date la porte (« 2026-09-09 14:32 », « 9/9/2026 2:32 PM ») */
    let h=''; const mh=d.match(/(\d{1,2}):(\d{2})(?::\d{2})?\s*([AaPp][Mm])?/);
    if(mh){ let hh=+mh[1]; const ap=(mh[3]||'').toUpperCase(); if(ap==='PM'&&hh<12) hh+=12; if(ap==='AM'&&hh===12) hh=0;
      if(hh<24) h=String(hh).padStart(2,'0')+':'+mh[2]; }
    lignes.push({bc:sku,des:idx.nom!=null?String(r[idx.nom]||'').slice(0,80):'',q,p,cmd,cleCmd,d:iso,h,
                 client:idx.client!=null?String(r[idx.client]||'').trim():''});
  });
  const colonnes=Object.entries(idx).map(([k,i])=>`${k} ← « ${H[i]} »`).join(' · ');
  return {lignes,deja,sansSku,sansCmd,retours,horsLieu,colonnes,canal,entete:H,idx,lieux};
}

/* ---------------- etat de l'import ---------------- */
let SENS='achat', TEXTE='', APERCU=null;
/* Ce qu'on corrige dans l'aperçu (quantité, prix, ligne retirée) avant d'enregistrer : la facture
   lue sert de base, on la vérifie, on ne la retape pas. Indexé par position dans la lecture. */
let EDITS={};
/* l'index des produits se refait quand un article est créé depuis l'aperçu */
function refaitIndex(){ const N=Object.fromEntries(D_TOUS().map(r=>[r[15],[r[0],r[13],r[2],r[12],r[6],r[8],r[7]]]));
  Object.keys(IDX).forEach(k=>delete IDX[k]); Object.assign(IDX,N);
  Object.keys(parBC).forEach(k=>delete parBC[k]); Object.entries(IDX).forEach(([cle,v])=>{ parBC[v[0]]=cle; }); aliasBC(); }
function razMap(){ MAP={}; LIEU=''; }
function majSens(){
  document.querySelectorAll('#sens button').forEach(b=>b.classList.toggle('on',b.dataset.s===SENS));
  const canal=SENS==='canal';
  $('canal').hidden=!canal; $('canalv').hidden=SENS!=='vente';
  $('l-tiers').textContent = SENS==='achat'?'Fournisseur':(canal?'Canal (rempli automatiquement)':'Client');
  $('tiers').placeholder = SENS==='achat'?'Nom du fournisseur':(canal?'':'Nom du client');
  $('tiers').readOnly=canal; if(canal){ $('tiers').value=$('canal-nom').value; }
  $('o-stock-lib').textContent = SENS==='achat'?'ajouter les quantités reçues':'retirer les quantités vendues';
  $('w-prix').style.display = SENS==='achat'?'':'none';
  $('dz').querySelector('b').textContent = canal?("Dépose ici le fichier CSV exporté depuis "+($('canal-nom').value||'ce canal')+", ou clique pour le choisir"):'Dépose la facture ici — PDF ou photo —, ou clique pour la choisir';
  $('l-noms').innerHTML=Object.keys(SENS==='achat'?FRN:CLI).sort().map(n=>`<option value="${esc(n)}">`).join('');
  $('tiers').placeholder = SENS==='achat' ? 'Tape un nom — nouveau ou existant'
    : (SENS==='canal' ? '' : 'Tape un nom — nouveau ou existant');
  /* Ce que ce mode va faire, ecrit en clair, et le bouton nomme la meme action.
     « Enregistrer la facture » sur les trois modes ne disait rien : on pouvait
     importer un export de caisse en croyant saisir un achat. */
  const Q=QUOI();
  $('quoi').className='quoi '+Q.c;
  $('quoi').innerHTML=`<span class="fl">${Q.fl}</span><span>${Q.t} ${Q.d}</span>`;
  $('ok').textContent=libelleBouton();
  try{ tiersNeuf(); }catch(e){}
  dessineApercu();
}
/* Le libelle du bouton se calcule a UN seul endroit. Trois fonctions le
   reecrivaient chacune de leur cote — l'apercu, la remise a zero, le changement
   de mode — et deux d'entre elles remettaient « Enregistrer la facture », ce qui
   effacait le mode juste apres qu'on l'ait choisi. */
function QUOI(){ return {
    achat:{c:'a', fl:'↓', t:'Tu enregistres une <b>réception de marchandise</b>.',
      d:'Le stock va <b>augmenter</b> des quantités reçues, et les prix de la facture deviendront les nouveaux prix d\'achat.',
      bouton:'Enregistrer l\'achat'},
    vente:{c:'v', fl:'↑', t:'Tu enregistres <b>une vente</b>, facture par facture.',
      d:'Le stock va <b>baisser</b> des quantités vendues. Le client sera créé s\'il n\'existe pas encore.',
      bouton:'Enregistrer la vente'},
    canal:{c:'c', fl:'⇊', t:'Tu importes <b>un fichier de ventes</b> exporté depuis un canal.',
      d:'Plusieurs ventes d\'un coup. Le stock va <b>baisser</b>, et une commande déjà importée n\'est jamais comptée deux fois.',
      bouton:'Importer les ventes'},
  }[SENS]; }
function libelleBouton(n){
  const b=QUOI().bouton;
  return n ? `${b} · ${nf(n)} ligne${n>1?'s':''}` : b;
}
$('sens').addEventListener('click',e=>{ const b=e.target.closest('[data-s]'); if(!b) return; SENS=b.dataset.s; majSens(); });
/* on arrive depuis « Enregistrer un achat » ou depuis une fiche fournisseur : sens et nom déjà posés */
{ const U=new URLSearchParams(location.search); const sn=U.get('sens'), fr=U.get('frn');
  if(sn&&['achat','vente','canal'].includes(sn)) SENS=sn;
  if(fr){ setTimeout(()=>{ $('tiers').value=fr; },0); }
  if(sn||fr) setTimeout(()=>{ majSens(); if(fr) $('tiers').value=fr; document.getElementById('dz').scrollIntoView({block:'center'}); },0); }
$('canal-nom').addEventListener('change',()=>{ $('tiers').value=$('canal-nom').value; majSens(); dessineApercu(); });
$('tiers').addEventListener('change',dessineApercu);

/* ---- un nom qui n'existe pas encore est un nom valable ----
   Le champ est libre : la liste déroulante ne fait que proposer ce qui existe
   déjà. La fiche du fournisseur (ou du client) se crée à l'enregistrement, avec
   cette facture comme première ligne. Mais rien ne le disait tant qu'aucun
   fichier n'était déposé, et le petit triangle de la liste donnait l'impression
   d'une liste fermée : on allait créer la fiche ailleurs avant de revenir. */
function tiersNeuf(){
  const el=$('n-tiers'); if(!el) return;
  const v=$('tiers').value.trim();
  const s=SENS==='achat', canal=SENS==='canal';
  const connus = s?FRN:CLI;
  if(!v||canal){ el.hidden=true; return; }
  if(connus[v]){
    el.hidden=false; el.style.color='var(--ink-3)';
    el.textContent = (s?'Fournisseur':'Client')+' déjà connu — sa fiche sera complétée.';
  } else {
    el.hidden=false; el.style.color='var(--iris)';
    el.textContent = 'Nouveau '+(s?'fournisseur':'client')+' : sa fiche sera créée à l\'enregistrement. Rien à préparer avant.';
  }
}
$('tiers').addEventListener('input',tiersNeuf);


async function lirePDF(buf){
  const pdf=await pdfjsLib.getDocument({data:buf}).promise; const out=[];
  for(let i=1;i<=pdf.numPages;i++){
    const pg=await pdf.getPage(i), tc=await pg.getTextContent(), L={};
    tc.items.forEach(it=>{ if(!it.str.trim()) return; const y=Math.round(it.transform[5]/2)*2;
      (L[y]=L[y]||[]).push({x:it.transform[4],s:it.str}); });
    Object.keys(L).map(Number).sort((a,b)=>b-a).forEach(y=>out.push(L[y].sort((a,b)=>a.x-b.x).map(o=>o.s).join('  ')));
  }
  return out.join('\n');
}
async function charge(file){
  $('msg').textContent=''; $('msg').className='msg'; razMap();
  try{
    /* tout passe par la meme porte : tableur, CSV, PDF avec texte, PDF scanne,
       photo. Les lectures longues (une photo) disent ou elles en sont. */
    $('dz').querySelector('b').textContent='Lecture de '+file.name+'…';
    TEXTE=await lireFichier(file, m=>{ $('dz').querySelector('b').textContent=m; });
    $('dz').classList.add('lu'); $('dz').querySelector('b').textContent='Lu : '+file.name;
    $('colle').value=TEXTE;
    entete();
  }catch(e){
    /* meme regle qu'a l'Etude : on garde ce qui est deja tape, mais on dit que
       l'apercu ci-dessous ne vient pas du fichier qu'on vient de deposer */
    const reste=($('colle').value||'').trim();
    $('msg').textContent=((e&&e.message)||'Lecture impossible.')
      + (reste?" L'aperçu ci-dessous est encore celui du document précédent.":'');
    $('dz').classList.remove('lu'); $('dz').querySelector('b').textContent='Dépose la facture ici — PDF ou photo —, ou clique pour la choisir';
    TEXTE=reste; }
  dessineApercu();
}
function entete(){
  const o=litEntete(TEXTE);
  const pose=(id,v)=>{ const el=$(id), a=$('a-'+id); if(v&&!el.value){ el.value=v; el.classList.add('auto'); a.hidden=false; } };
  pose('num',o.num); pose('date',o.date); pose('tiers',o.tiers);
}
['tiers','date','num'].forEach(id=>$(id).addEventListener('input',()=>{ $(id).classList.remove('auto'); $('a-'+id).hidden=true; dessineApercu(); }));
$('fichier').addEventListener('change',e=>{ const f=e.target.files[0]; if(f) charge(f); e.target.value=''; });
['dragenter','dragover'].forEach(ev=>$('dz').addEventListener(ev,e=>{ e.preventDefault(); $('dz').classList.add('sur'); }));
['dragleave','drop'].forEach(ev=>$('dz').addEventListener(ev,e=>{ e.preventDefault(); $('dz').classList.remove('sur'); }));
$('dz').addEventListener('drop',e=>{ const f=e.dataTransfer.files[0]; if(f) charge(f); });
$('basc').onclick=()=>{ $('txt').classList.toggle('on'); if($('txt').classList.contains('on')) $('colle').focus(); };
let cT=null; $('colle').addEventListener('input',()=>{ clearTimeout(cT); cT=setTimeout(()=>{ TEXTE=$('colle').value; razMap(); entete(); dessineApercu(); },300); });
['o-stock','o-prix'].forEach(id=>$(id).addEventListener('change',dessineApercu));

function analyse(){
  if(!TEXTE||TEXTE.trim().length<12) return null;
  let L, X=null;
  if(SENS==='canal'){ X=litExport(TEXTE); if(X.err) return X; L=X.lignes;
    if(!L.length) return {err: X.deja?`Les ${X.deja} lignes de cet export ont déjà été importées : rien de nouveau.`:"Aucune ligne exploitable dans cet export."}; }
  else {
    const T=litTableau(TEXTE);
    if(T&&T.err) return T;
    if(T){ L=T.lignes; X={canal:'Fichier à colonnes nommées',colonnes:T.colonnes,tableau:true}; }
    else L=litLignes(TEXTE);
    if(!L.length) return {err:"Aucune ligne exploitable : il faut au moins un code-barres et un prix par ligne."};
    L=L.map((x,i)=>{ x._i=i; const e=EDITS[i]; if(!e) return x; if(e.sup) return null;
      if(e.q!=null) x.q=e.q; if(e.p!=null) x.p=e.p; return x; }).filter(Boolean);
    if(!L.length) return {err:"Toutes les lignes ont été retirées."};
  }
  const stock=$('o-stock').checked, majPrix=SENS==='achat'&&$('o-prix').checked;
  if(SENS==='canal'){
    const agg={};
    L.forEach(x=>{ const k=x.bc; if(!agg[k]) agg[k]={bc:x.bc,des:x.des,q:0,p:x.p,mt:0,cmds:[]};
      agg[k].q+=x.q; agg[k].mt+=(x.p||0)*x.q; if(x.p!=null) agg[k].p=x.p; agg[k].cmds.push(x); });
    /* une reference vendue puis rendue en entier s'annule : on ne l'affiche pas */
    L=Object.values(agg).map(a=>{ a.p = a.q? a.mt/a.q : (a.p||0); return a; }).filter(a=>a.q!==0);
  }
  let connues=0,inconnues=0,montant=0,ecart=0,unites=0,neg=0;
  L.forEach(x=>{
    x.cle=trouve(x.bc); montant+=(x.q||0)*(x.p||0);
    if(!x.cle){ inconnues++; return; }
    connues++; unites+=(x.q||0);
    x.qAv=qteEff(x.cle);
    const d=SENS==='achat'?(x.q||0):-(x.q||0);
    x.qAp=stock?Math.max(0,x.qAv+d):x.qAv;
    if(stock&&SENS!=='achat'&&x.qAv+d<0){ x.manque=-(x.qAv+d); neg++; }
    x.paAv=paEff(x.cle);
    if(SENS==='achat'&&x.paAv!=null){ x.dp=x.p-x.paAv; ecart+=x.dp*(x.q||0); }
  });
  const num=$('num').value.trim();
  const doublon=num&&FACT.some(f=>f.num.toLowerCase()===num.toLowerCase());
  return {L,connues,inconnues,montant,ecart,unites,neg,stock,majPrix,doublon,X};
}
/* ---- corriger a la main ce que la lecture a devine ----
   Les exports de caisse ne portent pas tous les memes titres de colonnes : quand la
   devinette se trompe, on la corrige ici plutot que de renoncer au fichier. */
const MAP_LIB={sku:'Code-barres (SKU)',qte:'Quantité',prix:'Prix unitaire',cmd:'N° de ticket',
               date:'Date',client:'Client',nom:'Désignation',lieu:'Magasin / caisse'};
function barreMap(X){
  if(!X||!X.entete) return '';
  const opt=(k)=>{ const cur = MAP[k]!=null ? MAP[k] : (X.idx[k]!=null?String(X.idx[k]):'');
    return `<select data-map="${k}"><option value=""${cur===''?' selected':''}>— aucune —</option>`
      + X.entete.map((h,i)=>`<option value="${i}"${String(cur)===String(i)?' selected':''}>${esc(h||('colonne '+(i+1)))}</option>`).join('')
      + `</select>`; };
  const lieux = (X.lieux&&X.lieux.length>1) ? `<label class="mp"><span>Magasin à importer</span>
      <select id="map-lieu"><option value="">— tous —</option>${
      X.lieux.map(l=>`<option value="${esc(l)}"${LIEU===l?' selected':''}>${esc(l)}</option>`).join('')}</select></label>` : '';
  return `<details class="mapbox"${(X.idx.sku==null||X.idx.qte==null)?' open':''}>
    <summary>Les colonnes ne sont pas les bonnes ? Corrige-les ici</summary>
    <div class="mapg">${Object.keys(MAP_LIB).map(k=>`<label class="mp"><span>${esc(MAP_LIB[k])}</span>${opt(k)}</label>`).join('')}${lieux}</div>
  </details>`;
}
function dessineApercu(){
  const A=analyse(); APERCU=A; const box=$('apercu'); $('ok').disabled=true;
  if(!A){ box.innerHTML=''; return; }
  if(A.err){ box.innerHTML=`<div class="av" style="white-space:pre-line">${esc(A.err)}</div>`; return; }
  const s=SENS==='achat';
  const edit=(SENS!=='canal');
  const cell=(x,k)=>edit?`<input class="ed" type="number" step="${k==='q'?'1':'0.01'}" min="0" data-e="${k}" data-i="${x._i}" value="${x[k]==null?'':x[k]}">`:(k==='q'?(x.q??'—'):money2(x.p));
  const sup=x=>edit?`<button class="lnk sup" data-sup="${x._i}" title="Retirer cette ligne de la facture">✕</button>`:'';
  const li=A.L.map(x=>{
    if(!x.cle) return `<tr class="inc"><td class="ref"><b>${esc(x.des||'—')}</b><span>${x.bc}</span></td>
      <td class="r">${cell(x,'q')}</td><td class="r">${cell(x,'p')}</td><td colspan="2">code-barres absent du catalogue — ${s?`<button class="lnk" data-cree="${x._i}">créer l'article</button> ou `:''}<button class="lnk" data-sup="${x._i}">retirer la ligne</button></td></tr>`;
    const v=IDX[x.cle];
    const mv = A.stock ? `<span class="mv">${nf(x.qAv)} → <b class="${s?'plus':'moins'}">${nf(x.qAp)}</b>${x.manque?` <b class="moins">· ${x.manque} manquant${x.manque>1?'s':''}</b>`:''}</span>` : `<span class="mv" style="color:var(--ink-3)">inchangé (${nf(x.qAv)})</span>`;
    const pr = s ? (x.paAv==null?'—':(x.dp===0?'<span style="color:var(--ink-3)">inchangé</span>':`<span class="${x.dp<0?'plus':'moins'}">${x.dp>0?'+':'−'}${money2(Math.abs(x.dp))}</span>`)) : `<span style="color:var(--ink-3)">achat ${x.paAv==null?'—':money2(x.paAv)}</span>`;
    return `<tr class="${x.manque?'neg':''}${EDITS[x._i]?' corr':''}"><td class="ref"><div class="mq">${esc(v[2])}</div><b>${esc(v[1])}</b><span>${v[0]}</span></td>
      <td class="r">${cell(x,'q')}</td><td class="r">${cell(x,'p')}</td><td>${mv}</td><td class="r">${pr} ${sup(x)}</td></tr>`;
  }).join('');
  const nCorr=Object.keys(EDITS).length;
  const nouveauFrn = s && $('tiers').value.trim() && !FRN[$('tiers').value.trim()];
  /* un export qui contient des retours peut sortir un solde negatif : le signe suit le solde */
  const eff = s ? `+${nf(A.unites)}` : (A.unites<0 ? `+${nf(-A.unites)}` : `−${nf(A.unites)}`);
  const X=A.X;
  const bandeau = X ? `<div class="av" style="margin-bottom:12px;background:var(--surface-2);border-left-color:var(--iris)">
    <b>${esc(X.canal)}</b> · colonnes reconnues : ${esc(X.colonnes)}.
    ${X.tableau?`<b>Vérifie ces colonnes avant d'enregistrer</b> : un fichier qui n'est pas une facture (relevé de prix, liste d'annonces) ne doit pas être enregistré ici. `:''}
    ${X.deja?`<b>${nf(X.deja)} ligne${X.deja>1?'s':''} déjà importée${X.deja>1?'s':''}</b>, ignorée${X.deja>1?'s':''}. `:''}
    ${X.sansSku?`${nf(X.sansSku)} ligne${X.sansSku>1?'s':''} sans SKU lisible. `:''}
    ${X.sansCmd?`<b>${nf(X.sansCmd)} ligne${X.sansCmd>1?'s':''} sans numéro de commande</b> — elles ne pourront pas être dédoublonnées si tu réimportes le même export. `:''}
    ${X.retours?`<b>${nf(X.retours)} ligne${X.retours>1?'s':''} en négatif</b> : ce sont des retours, ils sont comptés en moins et remettent les flacons en stock. `:''}
    ${X.horsLieu?`${nf(X.horsLieu)} ligne${X.horsLieu>1?'s':''} d'un autre magasin, laissée${X.horsLieu>1?'s':''} de côté. `:''}
    Les quantités d'une même référence sont cumulées.</div>${barreMap(X)}` : '';
  box.innerHTML=bandeau+`
    <div class="ap">
      <div><span class="v">${nf(A.L.length)}</span><span class="k">lignes lues</span></div>
      <div><span class="v" style="color:var(--iris)">${nf(A.connues)}</span><span class="k">produits reconnus</span></div>
      <div><span class="v"${A.inconnues?' style="color:var(--warn)"':''}>${nf(A.inconnues)}</span><span class="k">codes inconnus</span></div>
      <div><span class="v">${money(A.montant)}</span><span class="k">montant</span></div>
      <div><span class="v" style="color:${A.stock?(s?'var(--good)':'var(--iris)'):'var(--ink-3)'}">${A.stock?eff:'0'}</span><span class="k">unités ${s?'en stock':'sorties'}</span></div>
      ${s?`<div><span class="v" style="color:${A.ecart<0?'var(--good)':A.ecart>0?'var(--crit)':'var(--ink-3)'}">${A.ecart?(A.ecart>0?'+':'−')+money(Math.abs(A.ecart)):'0 $'}</span><span class="k">écart vs prix connus</span></div>`:''}
    </div>
    ${edit?`<p class="ecr" style="margin:12px 0 0">Vérifie la lecture : quantités et prix se corrigent dans le tableau, une ligne se retire avec ✕. Rien n'est enregistré avant le bouton.${nCorr?` <b>${nCorr} correction${nCorr>1?'s':''}</b> pour l'instant.`:''}</p>`:''}
    ${nouveauFrn?`<div class="av" style="margin-top:12px;background:var(--iris-soft);border-left-color:var(--iris)"><b>Nouveau fournisseur : ${esc($('tiers').value.trim())}.</b> Sa fiche sera créée à l'enregistrement, avec cette facture comme première ligne — coordonnées à compléter ensuite dans <a href="fournisseurs.html">Fournisseurs</a>.</div>`:''}
    <div style="overflow-x:auto;margin-top:12px"><table class="tb"><thead><tr>
      <th>Référence</th><th class="r">Qté</th><th class="r">Prix</th><th>Stock</th><th class="r">${s?'Écart prix':'Prix d\'achat'}</th>
    </tr></thead><tbody>${li}</tbody></table></div>
    ${A.doublon?`<div class="av c" style="margin-top:12px"><b>Le numéro ${esc($('num').value)} est déjà enregistré.</b> Enregistrer deux fois la même facture doublerait les quantités. Si c'est vraiment une autre facture, change le numéro.</div>`:''}
    ${A.neg?`<div class="av c" style="margin-top:12px"><b>${A.neg} ligne${A.neg>1?'s':''} ${A.neg>1?'font':'fait'} passer le stock sous zéro.</b> On vend plus qu'il n'y a en stock : le stock est ramené à 0, et le comptage est faux quelque part. La quantité manquante est notée au journal.</div>`:''}
    ${A.inconnues?`<div class="av" style="margin-top:12px"><b>${A.inconnues} code${A.inconnues>1?'s':''}-barres inconnu${A.inconnues>1?'s':''}</b> — ces lignes ne seront pas enregistrées. Crée d'abord la fiche dans le catalogue (<b>+ Nouvel article</b>), puis réimporte.</div>`:''}`;
  $('ok').disabled = !(A.connues>0 && !A.doublon);
  $('ok').textContent = libelleBouton(A.connues || 0);
  /* corrections : on relit l'aperçu à chaque changement validé (Entrée ou sortie du champ) */
  /* la valeur est retenue à chaque frappe ou clic de flèche ; l'aperçu ne se
     redessine qu'en quittant la case — le redessiner sur « change » recréait la
     case sous la souris et les flèches de quantité ne répondaient plus */
  box.querySelectorAll('input.ed').forEach(inp=>{ inp.oninput=()=>{ const i=+inp.dataset.i, k=inp.dataset.e, v=inp.value.trim();
    EDITS[i]=Object.assign({},EDITS[i]||{}); if(v==='') delete EDITS[i][k]; else EDITS[i][k]=k==='q'?Math.max(0,Math.round(+v)):Math.max(0,+v);
    if(!Object.keys(EDITS[i]).length) delete EDITS[i]; };
    inp.onblur=()=>dessineApercu(); });
  box.querySelectorAll('[data-sup]').forEach(b=>b.onclick=()=>{ const i=+b.dataset.sup; EDITS[i]=Object.assign({},EDITS[i]||{},{sup:true}); dessineApercu(); });
  box.querySelectorAll('[data-cree]').forEach(b=>b.onclick=()=>creeDepuisLigne(+b.dataset.cree));
  box.querySelectorAll('[data-map]').forEach(sel=>sel.onchange=()=>{
    MAP[sel.dataset.map]=sel.value; dessineApercu();
    const d=box.querySelector('.mapbox'); if(d) d.open=true; });
  const ml=box.querySelector('#map-lieu');
  if(ml) ml.onchange=()=>{ LIEU=ml.value; dessineApercu();
    const d=box.querySelector('.mapbox'); if(d) d.open=true; };
}
/* un code-barres inconnu sur une facture d'achat : on crée l'article ici, avec ce qu'on sait */
function creeDepuisLigne(i){
  const x=(APERCU&&APERCU.L||[]).find(l=>l._i===i); if(!x) return;
  const d=litDesignation(x.des||'');
  const marque=prompt('Marque de cet article ?',(x.des||'').split(/\s+/)[0]||''); if(marque==null) return;
  const nom=prompt('Nom du parfum (sans la marque) ?',(x.des||'').replace(new RegExp('^'+marque.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')+'\\s*','i'),'')||''); if(nom==null||!nom.trim()) return;
  const ml=prompt('Contenance (oz) ?',d.ml||''); if(ml==null) return;
  const AJ=lit('articles-ajoutes-v1',[]); const L=Array.isArray(AJ)?AJ:[];
  const o={id:'a'+Date.now().toString(36)+Math.random().toString(36).slice(2,6),bc:x.bc,nom:nom.trim(),marque:marque.trim(),ml:String(ml).trim(),type:d.type||'',genre:d.genre||'',qte:0,pa:x.p,pvr:null,pvw:null};
  L.push(o); ecrit('articles-ajoutes-v1',L);
  log({act:'creation',lib:'article créé depuis la facture '+($('num').value.trim()||'')+' — '+(o.marque+' '+o.nom),bc:o.bc,ref:o.marque+' '+o.nom,av:null,ap:o.pa});
  refaitIndex(); dessineApercu();
}
function litDesignation(txt){
  const o={};
  let m=txt.match(/\b(\d+(?:[.,]\d+)?)\s*(?:oz|ml)?\s*(?=EDP|EDT|EDC|PARFUM|COLOGNE)/i);
  if(!m) m=txt.match(/\b(\d{1,2}[.,]\d)\b/);
  if(m) o.ml=m[1].replace(',','.');
  const t=txt.match(/\b(EDP|EDT|EDC)\b/i); if(t) o.type=t[1].toUpperCase();
  const g=txt.match(/\b(EDP|EDT|EDC)\s+([MLUW])\b/i);
  if(g){ const c=g[2].toUpperCase(); o.genre = c==='L'?'W' : c==='W'?'W' : c==='M'?'M':'U'; }
  return o;
}

$('ok').onclick=()=>{
  const A=APERCU; if(!A||A.err) return;
  const canal=SENS==='canal';
  const tiers=canal?$('canal-nom').value:$('tiers').value.trim();
  const canalV = canal ? tiers : (SENS==='vente' ? $('canal-vente').value : undefined);
  if(!tiers){ $('msg').textContent=SENS==='achat'?'Indique le fournisseur.':'Indique le client.'; $('tiers').focus(); return; }
  const d=$('date').value||ajd();
  const num=$('num').value.trim()||((canal?'EXPORT-'+tiers.toUpperCase().replace(/\s+/g,'')+'-':'SANS-NUM-')+d.replace(/-/g,'')+'-'+Date.now().toString(36).slice(-4).toUpperCase());
  demandeUser();
  const s=SENS==='achat', lignes=[], det=[];
  let nCmd=0;
  if(canal){ A.L.forEach(x=>(x.cmds||[]).forEach(c=>{ if(c.cmd){ CMD[c.cleCmd]=d; nCmd++; } })); ecrit(K_CMD,CMD); }
  let nprix=0;
  A.L.forEach(x=>{
    if(!x.cle) return;
    const v=IDX[x.cle], ref=v[2]+' '+v[1];
    lignes.push({cle:x.cle,bc:v[0],ref,q:x.q||0,p:x.p,qAv:x.qAv,qAp:x.qAp,manque:x.manque||0,paAv:x.paAv,paAp:(s&&A.majPrix)?x.p:x.paAv,
                 cmds: canal ? (x.cmds||[]).map(c=>({cmd:c.cmd,q:c.q,p:c.p,d:c.d,h:c.h||undefined,client:c.client})) : undefined});
    if(A.stock&&x.qAp!==x.qAv){ MOD[x.cle]=Object.assign({},MOD[x.cle]||{},{qte:x.qAp}); det.push({bc:v[0],ref,av:x.qAv,ap:x.qAp}); }
    if(s){
      (HIST[x.cle]=HIST[x.cle]||[]).push({d,p:x.p,f:tiers,q:x.q||null,src:'facture',num});
      if(A.majPrix&&x.paAv!==x.p){ MOD[x.cle]=Object.assign({},MOD[x.cle]||{},{pa:x.p}); nprix++;
        log({act:'prix',lib:"prix d'achat, facture "+num+" — "+tiers,bc:v[0],ref,av:x.paAv??null,ap:x.p}); }
    } else {
      /* un fichier de canal : une entrée par commande, avec sa date et son heure —
         c'est ce qui permet de voir plus tard à quelles heures ça vend */
      if(canalV && x.cmds && x.cmds.length) x.cmds.forEach(c=>(VENT[x.cle]=VENT[x.cle]||[]).push({d:c.d||d,h:c.h||undefined,p:c.p!=null?c.p:x.p,c:c.client||tiers,q:c.q||null,num,k:canalV}));
      else (VENT[x.cle]=VENT[x.cle]||[]).push({d,p:x.p,c:tiers,q:x.q||null,num,k:canalV});
    }
  });
  if(s) FRN[tiers]=Object.assign({nom:tiers},FRN[tiers]||{},{maj:new Date().toISOString()});
  else if(!canal) CLI[tiers]=Object.assign({nom:tiers},CLI[tiers]||{},{maj:new Date().toISOString()});
  const f={id:'f'+Date.now().toString(36),num,sens:canal?'vente':SENS,canal:canalV,export:canal||undefined,tiers,d,lignes,montant:A.montant,stock:A.stock,
           par:USR||'(non renseigné)',t:new Date().toISOString(),
           commandes: canal ? A.L.flatMap(x=>(x.cmds||[]).map(c=>c.cleCmd)) : undefined};
  FACT.push(f);
  ecrit(K.mod,MOD); ecrit(K.hist,HIST); ecrit(K.vent,VENT); ecrit(K.frn,FRN); ecrit(K.cli,CLI); ecrit(K.fact,FACT);
  log({act:s?'reception':'vente',lib:(s?'réception facture ':(canal?'ventes '+tiers+' — export ':'vente facture '))+num+(canal?'':' — '+tiers),
       n:det.length,impact:Math.round(det.reduce((a,x)=>a+(x.ap-x.av)*(paEff(parBC[x.bc])||0),0)),
       det, note:A.neg?`${A.neg} ligne(s) avec stock insuffisant`:undefined});
  raz(); dessineListe(); dessineKpis();
  $('msg').textContent=(canal?`Ventes ${tiers} importées : ${lignes.length} référence${lignes.length>1?'s':''}${nCmd?` sur ${nf(nCmd)} ligne${nCmd>1?'s':''} de commande`:''}`:`Facture ${num} enregistrée : ${lignes.length} ligne${lignes.length>1?'s':''}`)+(A.stock?`, stock ${s?'+':'−'}${nf(A.unites)} unités`:'')+(nprix?`, ${nprix} prix d'achat mis à jour`:'')+'.';
  $('msg').className='msg ok';
};
/* le code de cette page est un module (à cause de pdf.js) : ce qui suit sert aux tests automatiques */
window.__F={get APERCU(){ return APERCU; }, get EDITS(){ return EDITS; }, qteEff, paEff, parBC, trouve, lit, $};
function raz(){ TEXTE=''; APERCU=null; EDITS={}; $('colle').value=''; $('apercu').innerHTML=''; $('ok').disabled=true; $('ok').textContent=libelleBouton(); $('txt').classList.remove('on');
  ['tiers','date','num'].forEach(id=>{ $(id).value=''; $(id).classList.remove('auto'); $('a-'+id).hidden=true; });
  $('dz').classList.remove('lu'); $('dz').querySelector('b').textContent='Dépose la facture ici — PDF ou photo —, ou clique pour la choisir'; }
$('raz').onclick=()=>{ raz(); $('msg').textContent=''; };

/* ---------------- annulation d'une facture ---------------- */
function annule(id){
  /* annuler une facture défait du stock et de l'historique des prix : réservé au
     Patron et à l'Admin (droit « annuler »), pas à celui qui a saisi la vente */
  if(!peut('annuler')){ alert("Annuler une facture est réservé au Patron et à l'Admin."); return; }
  const i=FACT.findIndex(f=>f.id===id); if(i<0) return;
  const f=FACT[i];
  if(f.id.startsWith('seed-')){ alert("Cette facture a été installée avec le catalogue et n'a pas touché au stock : rien à annuler."); return; }
  if(!confirm(`Annuler la facture ${f.num} (${f.tiers}) ?\n\nLe stock revient à ce qu'il était, les prix enregistrés par cette facture sont retirés de l'historique. L'opération est inscrite au journal.`)) return;
  demandeUser();
  const det=[];
  f.lignes.forEach(l=>{
    if(f.stock&&l.qAp!==l.qAv){ const cur=qteEff(l.cle), nv=Math.max(0,cur-(l.qAp-l.qAv));
      MOD[l.cle]=Object.assign({},MOD[l.cle]||{},{qte:nv}); det.push({bc:l.bc,ref:l.ref,av:cur,ap:nv}); }
    if(f.sens==='achat'){ if(HIST[l.cle]) HIST[l.cle]=HIST[l.cle].filter(x=>x.num!==f.num);
      if(l.paAp!==l.paAv && paEff(l.cle)===l.paAp){ MOD[l.cle]=Object.assign({},MOD[l.cle]||{},{pa:l.paAv});
        log({act:'prix',lib:"prix d'achat rétabli (facture "+f.num+" annulée)",bc:l.bc,ref:l.ref,av:l.paAp,ap:l.paAv}); } }
    else if(VENT[l.cle]) VENT[l.cle]=VENT[l.cle].filter(x=>x.num!==f.num);
  });
  if(f.commandes){ f.commandes.forEach(k=>{ delete CMD[k]; }); ecrit(K_CMD,CMD); }
  FACT.splice(i,1);
  ecrit(K.mod,MOD); ecrit(K.hist,HIST); ecrit(K.vent,VENT); ecrit(K.fact,FACT);
  log({act:'annulation',lib:'facture annulée '+f.num+' — '+f.tiers,n:det.length,impact:0,det});
  dessineListe(); dessineKpis();
}

/* ---------------- liste et chiffres ---------------- */
const dfr=d=>{ if(!d) return '—'; const [a,m,j]=d.split('-'); return `${j}/${m}/${a.slice(2)}`; };
/* ---------------- LE DETAIL D'UNE FACTURE ----------------
   La liste disait combien de lignes et combien d'argent, jamais QUOI. Pour savoir
   ce qu'il y avait dans une reception, il fallait rouvrir le PDF d'origine — quand
   on l'avait encore. Le detail est pourtant deja enregistre, ligne par ligne, avec
   le stock avant et apres : il ne manquait que de l'afficher. */
function detail(id){
  const f=FACT.find(x=>x.id===id); if(!f) return;
  const achat=f.sens==='achat';
  const u=f.lignes.reduce((a,l)=>a+(l.q||0),0);
  $('d-num').textContent=(achat?'Achat ':(f.export?'Ventes importées ':'Vente '))+(f.num||'');
  $('d-sous').innerHTML=`<b>${esc(f.tiers)}</b> · ${dfr(f.d)} · ${nf(f.lignes.length)} référence${f.lignes.length>1?'s':''}`
    +` · ${nf(u)} unité${u>1?'s':''}`+(f.canal?` · canal ${esc(f.canal)}`:'')
    +(f.par?` · saisi par ${esc(f.par)}`:'')
    +(f.stock?'':' · <b style="color:var(--warn)">stock non modifié</b>');
  $('d-corps').innerHTML=`<div style="overflow-x:auto"><table><thead><tr>
      <th>Référence</th><th class="r">Qté</th><th class="r">Prix unité</th><th class="r">Total ligne</th>
      ${f.stock?'<th class="r">Stock</th>':''}</tr></thead><tbody>
    ${f.lignes.map(l=>{
      /* le stock avant → apres est garde a l'enregistrement : c'est la seule trace
         de ce que cette facture a REELLEMENT fait, meme si le stock a bouge depuis */
      const bouge=(l.qAv!=null&&l.qAp!=null)?`<span class="stk">${nf(l.qAv)} → <b>${nf(l.qAp)}</b></span>`
                 :'<span class="stk">—</span>';
      return `<tr><td><b>${esc(l.ref||l.des||'—')}</b><small>${esc(l.bc||'')}</small>
          ${l.manque?`<small style="color:var(--crit)">vendu à découvert : ${nf(l.manque)} de plus que le stock</small>`:''}</td>
        <td class="r">${nf(l.q||0)}</td>
        <td class="r">${l.p!=null?money2(l.p):'—'}</td>
        <td class="r"><b>${money2((l.q||0)*(l.p||0))}</b></td>
        ${f.stock?`<td class="r">${bouge}</td>`:''}</tr>`; }).join('')}
    </tbody></table></div>`;
  $('d-tot').innerHTML=`<span>${nf(u)} unité${u>1?'s':''}</span>`
    +`<span>Total <b>${money2(f.montant)}</b></span>`;
  $('dov').classList.add('on');
}
$('d-ferm').onclick=()=>$('dov').classList.remove('on');
$('dov').onclick=e=>{ if(e.target.id==='dov') $('dov').classList.remove('on'); };
document.addEventListener('keydown',e=>{ if(e.key==='Escape') $('dov').classList.remove('on'); });

/* ---------------- LA LISTE, RANGEE PAR CANAL ----------------
   Une seule liste melangeait les receptions fournisseurs, les factures clients et
   les exports de caisse : trois choses qui n'ont ni les memes chiffres ni le meme
   sens, empilees par date. On les range donc par origine — les achats d'un cote,
   puis chaque canal de vente separement — avec son total. C'est ainsi qu'on lit
   un commerce : d'ou vient la marchandise, et par ou elle repart. */
function groupeDe(f){
  if(f.sens==='achat') return {cle:'achat', lib:'Achats — réceptions de marchandise', rang:0};
  const c=(f.canal||'').trim() || 'Sans canal';
  return {cle:'v:'+c.toLowerCase(), lib:'Ventes · '+c, rang:1};
}
function dessineListe(){
  const L=FACT.slice().sort((a,b)=>(b.d||'').localeCompare(a.d||'')||(b.t||'').localeCompare(a.t||''));
  $('nbf').textContent=L.length?`${nf(L.length)} · rangées par canal, la plus récente en premier`:'';
  if(!L.length){ $('liste').innerHTML=`<div class="vide"><p>Aucune facture enregistrée. Dépose un PDF ci-dessus : le stock, les prix et les fiches fournisseurs se mettront à jour tout seuls.</p></div>`; return; }

  const G=new Map();
  L.forEach(f=>{ const g=groupeDe(f);
    if(!G.has(g.cle)) G.set(g.cle,{lib:g.lib,rang:g.rang,L:[]});
    G.get(g.cle).L.push(f); });
  /* les achats d'abord, puis les canaux du plus gros au plus petit : l'ordre
     alphabetique ferait remonter « Autre » avant « Gros », ce qui n'apprend rien */
  const groupes=[...G.values()].sort((a,b)=>a.rang-b.rang
    || b.L.reduce((x,f)=>x+f.montant,0)-a.L.reduce((x,f)=>x+f.montant,0));

  $('liste').innerHTML=groupes.map(g=>{
    const tot=g.L.reduce((a,f)=>a+f.montant,0);
    const un=g.L.reduce((a,f)=>a+f.lignes.reduce((x,l)=>x+(l.q||0),0),0);
    return `<div class="grp">
      <h3>${esc(g.lib)}
        <span class="cpt">${nf(g.L.length)} facture${g.L.length>1?'s':''} · ${nf(un)} unité${un>1?'s':''}</span>
        <span class="tot">${money(tot)}</span></h3>
      <div style="overflow-x:auto"><table class="hist"><thead><tr>
      <th>Date</th><th>Tiers</th><th>Numéro</th><th class="r">Lignes</th><th class="r">Unités</th><th class="r">Montant</th><th>Par</th><th></th>
      </tr></thead><tbody>${g.L.map(f=>{
        const u=f.lignes.reduce((a,l)=>a+(l.q||0),0);
        const st=f.stock?(f.sens==='achat'?`<span class="plus">+${nf(u)}</span>`:`<span class="moins">−${nf(u)}</span>`)
                        :`<span style="color:var(--ink-3)" title="${esc(f.note||'stock non modifié')}">${nf(u)} · hors stock</span>`;
        return `<tr class="cl" data-d="${esc(f.id)}"><td>${dfr(f.d)}</td>
          <td class="tiers"><b>${esc(f.tiers)}</b>${f.note?`<span>${esc(f.note)}</span>`:''}</td>
          <td>${esc(f.num)}<span class="fl"> · voir le détail</span></td>
          <td class="r">${nf(f.lignes.length)}</td><td class="r">${st}</td>
          <td class="r">${money(f.montant)}</td>
          <td style="color:var(--ink-3);font-size:12.5px">${esc(f.par||'')}</td>
          <td>${(f.id.startsWith('seed-')||!peut('annuler'))?'':`<button class="x" data-x="${esc(f.id)}">Annuler</button>`}</td></tr>`; }).join('')}
      </tbody></table></div></div>`; }).join('');

  /* le bouton Annuler est DANS la ligne cliquable : sans ce stopPropagation,
     un clic dessus ouvrirait aussi le detail par-dessus la confirmation */
  document.querySelectorAll('[data-x]').forEach(b=>b.onclick=e=>{ e.stopPropagation(); annule(b.dataset.x); });
  document.querySelectorAll('tr.cl').forEach(tr=>tr.onclick=()=>detail(tr.dataset.d));
}
function dessineKpis(){
  const ach=FACT.filter(f=>f.sens==='achat'), ven=FACT.filter(f=>f.sens==='vente');
  const uIn=ach.filter(f=>f.stock).reduce((a,f)=>a+f.lignes.reduce((x,l)=>x+(l.q||0),0),0);
  const uOut=ven.filter(f=>f.stock).reduce((a,f)=>a+f.lignes.reduce((x,l)=>x+(l.q||0),0),0);
  $('kpis').innerHTML=`<div class="kpis">
    <div class="kpi"><span class="v">${nf(FACT.length)}</span><span class="k">facture${FACT.length>1?'s':''} enregistrée${FACT.length>1?'s':''}</span></div>
    <div class="kpi good"><span class="v">${money(ach.reduce((a,f)=>a+f.montant,0))}</span><span class="k">d'achats · ${nf(ach.length)} facture${ach.length>1?'s':''}</span></div>
    <div class="kpi iris"><span class="v">${money(ven.reduce((a,f)=>a+f.montant,0))}</span><span class="k">de ventes · ${nf(ven.length)} facture${ven.length>1?'s':''}</span></div>
    <div class="kpi"><span class="v">+${nf(uIn)} / −${nf(uOut)}</span><span class="k">unités entrées / sorties par facture</span></div>
    <div class="kpi"><span class="v">${nf(Object.keys(FRN).length)} · ${nf(Object.keys(CLI).length)}</span><span class="k">fournisseurs · clients connus</span></div>
  </div>`;
  $('src').innerHTML=`${nf(FACT.length)} facture${FACT.length>1?'s':''}<br>lecture PDF locale`;
}
majUser(); $('sfoot').innerHTML='achats et ventes<br>mettent le stock à jour';
majSens(); dessineListe(); dessineKpis();
if(!$('date').value) $('date').value='';
'''

html = coquille("Factures", "Factures",
  "Une facture d'achat ajoute les quantités reçues au stock, une facture de vente les retire. "
  "Le fournisseur ou le client, l'historique des prix et le journal se mettent à jour en même temps. "
  "Plus besoin d'un tableur à côté.",
  CSS, CORPS.replace("__ACCEPT__", _lire.ACCEPT), JS, donnees=('produits',)).replace('__IDX__', 'Object.fromEntries(D_TOUS().map(r=>[r[15],[r[0],r[13],r[2],r[12],r[6],r[8],r[7]]]))')
# pdf.js : le module "worker" est chargé sur le fil principal (il expose globalThis.pdfjsWorker),
# ce qui evite tout fichier externe et tout reseau. Le script de page devient un module, apres pdf.js.
import re as _re
# La coquille ouvre son script par VER_URL puis $ : on coupe juste avant, quoi
# qu'il y ait entre les deux, pour ne rien perdre en chemin.
_m = _re.search(r'<script type="text/plain" id="page-js">\n(const VER_URL=[^\n]*\n)?const \$=i=>document\.getElementById\(i\);', html)
assert _m, "ancre du script de page introuvable"
html = (html[:_m.start()]
        + '<script type="module">' + PDF_WORKER + '</script>\n'
        + '<script type="module">' + PDF_MAIN
        + '\npdfjsLib.GlobalWorkerOptions.workerSrc="inline";\nwindow.pdfjsLib=pdfjsLib;</script>\n'
        + '<script type="text/plain" id="page-js" data-module="1">\n' + (_m.group(1) or '')
        + 'const $=i=>document.getElementById(i);'
        + html[_m.end():])
assert 'data-module="1"' in html
open('factures.html','w').write(html)
print('factures.html',len(html)//1024,'Ko')
