# -*- coding: utf-8 -*-
"""Rubrique « Étude de devis » : un fournisseur envoie un devis (PDF, fichier, texte) ; l'outil
compare chaque ligne à ce qu'on sait déjà — prix d'achat moyen, dernier achat, meilleur prix,
stock, ventes des 90 derniers jours, prix de gros et de détail, Amazon — et dit si ça vaut le
coup d'acheter. Rien n'est enregistré dans le stock ni dans les prix : c'est une étude.
La lecture des lignes est la même que celle des factures (build_factures.py)."""
import re
from build_crm import coquille
import _lire, _noms

# On réutilise la lecture des lignes de build_factures : mêmes heuristiques, même robustesse.
_SRC = open('build_factures.py', encoding='utf-8').read()
_a = _SRC.index('/* ---------------- lecture d\'une facture')
_b = _SRC.index('function litEntete(')
LECTURE = _SRC[_a:_b]
_c = _SRC.index('async function lirePDF(')
_d = _SRC.index('async function charge(')
LIRE_PDF = _SRC[_c:_d]
PDF_MAIN = open('_pdfjs/package/build/pdf.min.mjs').read()
PDF_WORKER = open('_pdfjs/package/build/pdf.worker.min.mjs').read()

CSS = r"""
.info{background:var(--iris-soft);border-left:3px solid var(--iris);border-radius:0 9px 9px 0;padding:13px 17px;font-size:13.5px;color:var(--ink-2);line-height:1.6;margin-bottom:18px;max-width:92ch}
.info b{color:var(--ink)}
.dz{border:2px dashed var(--line);border-radius:12px;padding:24px;text-align:center;background:var(--surface);cursor:pointer;color:var(--ink-2);position:relative;margin-bottom:10px}
.dz b{display:block;color:var(--ink);font-size:15px;margin-bottom:4px}.dz span{font-size:12.5px}
.dz.sur,.dz:hover{border-color:var(--iris);background:var(--iris-soft)}.dz.lu{border-style:solid;border-color:var(--good);background:var(--good-soft)}
.dz input{position:absolute;inset:0;opacity:0;cursor:pointer}
.lnk{background:none;border:0;padding:0;font:inherit;font-size:13px;color:var(--iris);text-decoration:underline;cursor:pointer}
.txt{display:none;margin:8px 0}.txt.on{display:block}
.txt textarea{width:100%;min-height:120px;border:1px solid var(--line);border-radius:9px;padding:10px 12px;font:12.5px/1.5 ui-monospace,Menlo,monospace;background:var(--surface)}
.ent{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px;margin:12px 0 16px}
.fld label{display:block;font-family:Inter,sans-serif;font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--ink-3);font-weight:800;margin-bottom:5px}
.fld input{width:100%;padding:9px 11px;border:1px solid var(--line);border-radius:8px;font:inherit;background:var(--surface)}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:12px;margin:14px 0}
.kpi{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:13px 16px}
.kpi .v{font-family:Inter,sans-serif;font-size:24px;font-weight:800;letter-spacing:-.03em;line-height:1;font-variant-numeric:tabular-nums}
.kpi .k{display:block;font-size:12.5px;color:var(--ink-2);margin-top:6px;line-height:1.4}
.g{color:var(--good)}.w{color:var(--warn)}.c{color:var(--crit)}
.tb{width:100%;border-collapse:collapse;font-size:13px;background:var(--surface);border:1px solid var(--line);border-radius:10px;overflow:hidden}
.tb th{text-align:left;font-family:Inter,sans-serif;font-size:10.5px;letter-spacing:.08em;text-transform:uppercase;color:var(--ink);font-weight:800;padding:9px 10px;background:var(--surface-2);border-bottom:1px solid var(--line);white-space:nowrap}
.tb td{padding:9px 10px;border-bottom:1px solid var(--line-2);vertical-align:top}
.tb tr:last-child td{border-bottom:0}
.tb td.r,.tb th.r{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
.tb .ref b{display:block}.tb .ref span{font-size:11.5px;color:var(--ink-3)}.tb .ref .mq{font-family:Inter,sans-serif;font-size:10.5px;letter-spacing:.08em;text-transform:uppercase;color:var(--ink-3)}
.tb small{display:block;color:var(--ink-3);font-size:11px;line-height:1.35}
.vd{display:inline-block;padding:3px 9px;border-radius:99px;font-family:Inter,sans-serif;font-size:11px;font-weight:800;letter-spacing:.04em;white-space:nowrap}
.vd.bon{background:var(--good-soft);color:var(--good)}.vd.ok{background:var(--surface-2);color:var(--ink-2)}.vd.cher{background:var(--crit-soft);color:var(--crit)}
.vd.inc{background:var(--warn-soft);color:var(--warn)}
.fl{display:inline-block;margin:3px 4px 0 0;padding:2px 7px;border-radius:5px;font-size:11px;font-weight:600;background:var(--warn-soft);color:var(--warn)}
.fl.i{background:var(--iris-soft);color:var(--iris)}.fl.c{background:var(--crit-soft);color:var(--crit)}
.ref .dnom{display:block;margin-top:4px;font-size:11.5px;color:var(--ink-3);font-style:italic}
select.cand{display:block;margin-top:5px;max-width:320px;font:12.5px Inter,sans-serif;padding:4px 6px;border:1px solid var(--line);border-radius:6px;background:var(--surface)}
tr.l-verif td{background:var(--warn-soft)}
.actions{display:flex;gap:10px;align-items:center;margin:14px 0 26px;flex-wrap:wrap}
/* le devis chargé, dit en haut, avec la porte de sortie à côté : un fichier mal
   lu se jette d'ici, sans descendre chercher le bouton sous le tableau */
.haut{display:flex;gap:12px;align-items:center;flex-wrap:wrap;margin:0 0 14px;padding:10px 14px;background:var(--iris-soft);border-radius:10px;font-size:13.5px}
.haut span{flex:1;min-width:200px}.haut b{font-weight:700}
.btn.d{border-color:var(--crit);color:var(--crit)}.btn.d:hover{background:var(--crit);color:#fff}
.actions[hidden]{display:none}   /* display:flex l'emportait sur l'attribut hidden : les boutons s'affichaient sans étude */
.msg{font-size:13px;color:var(--ink-2)}.msg.ok{color:var(--good)}.msg.err{color:var(--crit)}
.spk{display:inline-block;vertical-align:middle;margin-left:6px}
h2.sec{font-family:Inter,sans-serif;font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--ink);font-weight:800;margin:30px 0 14px;padding-bottom:9px;border-bottom:1px solid var(--line);display:flex;justify-content:space-between;align-items:baseline;gap:12px;flex-wrap:wrap}
h2.sec em{font-style:normal;font-size:13px;letter-spacing:0;text-transform:none;color:var(--ink-2);font-weight:500}
.vide{padding:26px;text-align:center;color:var(--ink-3);border:1px dashed var(--line);border-radius:10px;font-size:13.5px}

/* --- une fois l'étude faite, ce qui a servi à la lancer s'efface ---
   Le pavé d'explication et la grande zone de dépôt gardaient toute la hauteur de
   l'écran alors qu'ils ne servaient plus : on devait défiler pour voir le résultat
   du travail qu'on venait de demander. */
.zdepot.replie .dz{padding:10px 14px;text-align:left;opacity:.62;font-size:12.5px}
.zdepot.replie .dz b{display:inline;font-size:12.5px}
.zdepot.replie .dz span{display:none}
.zdepot.replie .txt textarea{min-height:52px;opacity:.62}
.zdepot.replie:hover .dz,.zdepot.replie:focus-within .txt textarea{opacity:1}

/* --- les chiffres du haut : quatre, dont un qui compte plus que les autres --- */
.kpi.gros{background:var(--iris-soft);border-color:transparent}
.kpi.gros .v{font-size:30px}
.kpi .k i{font-style:normal;color:var(--ink-3);font-size:11.5px}

/* --- le tableau --- */
.tb tfoot td{border-top:2px solid var(--line);background:var(--surface-2);font-weight:700;padding:10px}
.tb .px{font-size:14.5px}
.tb .na{color:var(--ink-3)}
.tb tr.l-cher td{background:color-mix(in srgb, var(--crit-soft) 45%, transparent)}
.tb tr.l-bon  td{background:color-mix(in srgb, var(--good-soft) 40%, transparent)}
.tb tr.linc td{background:var(--warn-soft)}
/* La colonne des verdicts était un pavé bariolé : le verdict et ses remarques
   avaient le même poids visuel. Le verdict d'abord, seul sur sa ligne ; les
   remarques en dessous, plus petites et grises tant qu'elles ne sont pas graves. */
.tb td.vc{min-width:172px;max-width:230px}
.tb td.vc .vd{display:inline-block;font-size:11.5px;padding:4px 11px}
.tb td.vc .rem{margin-top:5px;display:flex;flex-direction:column;gap:3px;align-items:flex-start}
.tb td.vc .fl{margin:0;font-size:10.5px;font-weight:600;background:transparent;color:var(--ink-3);padding:0}
.tb td.vc .fl.c{background:transparent;color:var(--crit);font-weight:700}
.tb td.vc .fl.i{background:transparent;color:var(--iris);font-weight:700}
.jargon{margin:9px 0 0;font-size:11.5px;color:var(--ink-3);line-height:1.55;max-width:92ch}
.jargon b{color:var(--ink-2)}
.repris{background:var(--good-soft);border-left:3px solid var(--good);border-radius:0 9px 9px 0;
padding:10px 15px;font-size:13px;color:var(--ink-2);line-height:1.55;margin:0 0 14px;max-width:92ch}
.repris b{color:var(--ink)}
.btn.sm{padding:5px 11px;font-size:12px}
.btn.sm.sup{color:var(--crit);border-color:color-mix(in srgb, var(--crit) 30%, var(--line))}
.btn.sm.sup:hover{background:var(--crit-soft);border-color:var(--crit)}
"""

CORPS = r"""
<div class="info" id="bandeau"><b>Un fournisseur propose un devis : vaut-il le coup ?</b> Dépose le devis (PDF, fichier à colonnes, ou lignes collées).
Pour chaque référence, l'outil compare le prix proposé au <b>prix d'achat moyen</b> de Sam, au dernier achat et au meilleur prix jamais payé,
regarde le <b>stock</b> et ce qui s'est <b>vendu sur 90 jours</b>, et calcule la <b>marge</b> aux prix de gros et de détail.
Rien n'est enregistré dans le stock ni dans les prix : c'est une étude, à garder ou à jeter.</div>

<div class="zdepot" id="zdepot">
<div class="dz" id="dz"><b>Dépose le devis ici, ou clique pour le choisir</b>
  <span>PDF, photo, scan, Excel (.xlsx), CSV/TSV, ou texte. Tout se lit, entièrement sur cet ordinateur.</span>
  <input type="file" id="fichier" accept="__ACCEPT__"></div>
<button class="lnk" id="basc">…ou coller les lignes du devis</button>
<div class="txt" id="txt"><textarea id="colle" placeholder="Une ligne par référence : code-barres, quantité, prix — dans n'importe quel ordre."></textarea></div>
</div>

<div class="haut" id="haut" hidden>
  <span id="haut-txt"></span>
  <button class="btn d" id="sup-haut">Supprimer ce devis</button>
</div>

<div class="ent">
  <div class="fld"><label>Fournisseur</label><input id="frn" list="l-frn" placeholder="Nom du fournisseur"><datalist id="l-frn"></datalist></div>
  <div class="fld"><label>Date du devis</label><input id="date" type="date"></div>
  <div class="fld"><label>Référence du devis</label><input id="num" placeholder="facultatif"></div>
</div>

<div id="kpis"></div>
<div id="apercu"></div>
<div class="actions" id="acts" hidden>
  <button class="btn pri" id="garde">Garder cette étude</button>
  <span id="exp"></span>
  <button class="btn" id="raz">Étudier un autre devis</button>
  <span class="msg" id="msg"></span>
</div>

<h2 class="sec">Études gardées <em id="nbe"></em></h2>
<div id="liste"></div>
"""

JS = r"""
const IDX=__IDX__;
const K={mod:'fiches-modifiees-v1',ext:'stock-externe-v1',hist:'prix-achat-hist-v1',vent:'ventes-v1',frn:'fournisseurs-v1',
         mar:'marche-v1',reg:'reglages-v1',etu:'etudes-devis-v1',jou:'crm-journal-v1'};
let MOD=lit(K.mod,{}), EXT=lit(K.ext,{q:{}}), HIST=lit(K.hist,{}), VENT=lit(K.vent,{}), FRN=lit(K.frn,{}), MAR=lit(K.mar,{});
let REG=Object.assign({margeMin:10},lit(K.reg,{}));
let ETU=lit(K.etu,[]); if(!Array.isArray(ETU)) ETU=base(K.etu,[]);
let USR=NOM_UTIL;
window.__nomChange.push(v=>{ USR=v; });
if(!EXT.q) EXT.q={};
const dfr=d=>{ if(!d) return '—'; const [a,m,j]=String(d).slice(0,10).split('-'); return j?`${j}/${m}/${a.slice(2)}`:d; };
function qteEff(cle){ const m=MOD[cle]; if(m&&m.qte!=null) return +m.qte; const v=IDX[cle]||[]; const e=EXT.q[v[0]]; return e!=null?+e:(v[6]||0); }
const paEff=cle=>{ const m=MOD[cle]; return (m&&m.pa!=null)?+m.pa:(IDX[cle]&&IDX[cle][3]!=null?+IDX[cle][3]:null); };
const pvwEff=cle=>{ const m=MOD[cle]; return (m&&m.pvw!=null)?+m.pvw:(IDX[cle]&&IDX[cle][4]!=null?+IDX[cle][4]:null); };
const pvrEff=cle=>{ const m=MOD[cle]; return (m&&m.pvr!=null)?+m.pvr:(IDX[cle]&&IDX[cle][5]!=null?+IDX[cle][5]:null); };
const parBC={}; Object.entries(IDX).forEach(([cle,v])=>{ parBC[v[0]]=cle; });
Object.entries(MOD).forEach(([cle,m])=>{ if(!m||!m.bcs||!IDX[cle]) return; String(m.bcs).split(/[^0-9]+/).filter(x=>x.length>=6).forEach(b=>{ if(!parBC[b]) parBC[b]=cle; }); });
function trouve(bc){
  const c=[bc,bc.replace(/^0+/,''),bc.padStart(12,'0'),bc.padStart(13,'0')];
  for(const x of c){ if(parBC[x]) return parBC[x]; }
  const nu=bc.replace(/^0+/,'');
  const k=Object.keys(parBC).find(b=>b.replace(/^0+/,'')===nu); return k?parBC[k]:null;
}
/* La lecture des lignes est celle des factures, mot pour mot. Un seul mot change : sur
   cette page le document déposé est un DEVIS, et les messages d'erreur doivent le dire. */
const DOC_PAGE='devis';
__LECTURE__
__LIRE_PDF__
/* ---- retrouver par le nom ----
   Une price list arrive souvent sans codes-barres. Le moteur des noms (le même
   que pour les messages clients) propose alors un parfum du catalogue, avec un
   score ; on ne prend seul que ce qui est net, le reste est marqué à vérifier.
   Et quand un code-barres est là mais que le nom du devis ne ressemble pas au
   nôtre, on le dit : c'est souvent un code recopié sur la mauvaise ligne. */
const cleDeBC=b=>trouve(String(b||''));
__NOMS__
function parNom(des){
  if(!des||!/[a-zà-ÿ]{3}/i.test(des)) return {cle:'',sur:'no',cands:[],appris:false};
  const r=mCherche(des);
  /* « aucun de ceux-là », dit une fois : on ne repropose pas — mais on garde les
     candidats sous la main, au cas où Sam change d'avis */
  try{ const A=lit(K_ALIASN,{})||{}; if(A[mNorm(des)]==='__aucun') return {cle:'',sur:'no',cands:r.cands.slice(0,5),appris:true,refuse:true}; }catch(e){}
  const best=r.cands[0], second=r.cands[1];
  const sur = r.appris ? 'ok'
    : (best && best.sc>=0.72 && (!second || best.sc-second.sc>=0.13)) ? 'ok'
    : (best && best.sc>=0.45) ? 'hm' : 'no';
  return {cle:(sur!=='no'&&best)?best.cle:'', sur, cands:r.cands.slice(0,5), appris:r.appris};
}
/* le nom du devis ressemble-t-il au nôtre ? (0 = rien à voir, 1 = identique) */
function ressemble(des,cle){
  if(!des||!cle) return null;
  const r=mCherche(des); const c=r.cands.find(x=>x.cle===cle);
  return c?c.sc:0;
}
/* la correction de Sam est retenue : la prochaine fois, cette ligne est reconnue d'elle-même */
function apprendNom(des,cle){
  try{ const A=lit(K_ALIASN,{})||{}; const k=mNorm(des); if(!k) return;
    A[k]=cle||'__aucun'; ecrit(K_ALIASN,A); }catch(e){}
}

/* ---- ce qu'on sait déjà d'une référence ---- */
const J90=90*86400000;
/* L'outil a-t-il seulement vu passer une vente ? Tant que non, il ne peut RIEN
   conclure sur la rotation d'un produit, et il vaut mieux ne rien dire que
   d'annoncer que tout est invendu. */
const VENTES_CONNUES=(()=>{ try{
  return Object.values(VENT||{}).some(l=>Array.isArray(l)&&l.some(x=>x&&x.q>0)); }catch(e){ return false; } })();
/* Depuis combien de jours l'outil voit-il les ventes ? « Ne se vend pas » veut
   dire « rien en 90 jours » : tant que le journal n'a pas 90 jours d'âge, on ne
   peut pas le dire — on dit seulement ce qu'on a vu, avec l'âge du journal. */
const JOURS_HIST=(()=>{ try{ let min='';
  Object.values(VENT||{}).forEach(l=>(Array.isArray(l)?l:[]).forEach(x=>{ if(x&&x.q>0&&x.d&&(!min||x.d<min)) min=String(x.d).slice(0,10); }));
  return min?Math.max(0,Math.round((Date.now()-new Date(min).getTime())/86400000)):0; }catch(e){ return 0; } })();
function connu(cle){
  const H=(HIST[cle]||[]).filter(h=>h&&h.p>0).slice().sort((a,b)=>String(a.d||'').localeCompare(String(b.d||'')));
  let sq=0,sp=0; H.forEach(h=>{ if(h.q>0){ sq+=h.q; sp+=h.q*h.p; } });
  const moy = sq? sp/sq : (H.length? H.reduce((a,h)=>a+h.p,0)/H.length : paEff(cle));
  const dernier=H.length?H[H.length-1]:null;
  const meilleur=H.length?H.reduce((a,h)=>h.p<a.p?h:a,H[0]):null;
  const lim=Date.now()-J90;
  const v90=(VENT[cle]||[]).filter(x=>x&&x.q>0&&x.d&&new Date(x.d).getTime()>=lim).reduce((a,x)=>a+x.q,0);
  const stock=qteEff(cle);
  const mois = v90>0 ? stock/(v90/3) : (stock>0?Infinity:0);
  /* la date de la dernière vente connue : c'est elle qui parle le mieux */
  let derniereVente=''; (VENT[cle]||[]).forEach(x=>{ if(x&&x.q>0&&x.d&&String(x.d)>derniereVente) derniereVente=String(x.d).slice(0,10); });
  return {moy:moy==null?null:+moy, dernier, meilleur, v90, stock, mois, derniereVente, pvw:pvwEff(cle), pvr:pvrEff(cle), amz:(MAR[cle]||{}).amz??null, nH:H.length};
}
function verdict(x,c){
  if(!c) return {k:'inc',lib:'inconnu',flags:[],note:''};
  const flags=[];
  let k='ok', lib='dans les prix';
  const mgw=(c.pvw!=null&&x.p!=null)?(c.pvw-x.p)/c.pvw*100:null;
  const mini=+REG.margeMin||10;

  if(c.moy!=null&&x.p!=null){
    const e=(x.p-c.moy)/c.moy;
    if(e<=-0.03){ k='bon'; lib='bon prix'; } else if(e>=0.03){ k='cher'; lib='plus cher'; }
    if(c.meilleur&&x.p<=c.meilleur.p*1.001) flags.push(['i','meilleur prix jamais vu']);
  } else if(x.p!=null){ k='ok'; lib='premier achat'; flags.push(['i','aucun prix d\'achat connu']); }

  /* Un prix sous la moyenne qui ne laisse aucune marge n'est PAS un bon prix.
     L'ancienne version affichait « bon prix » à côté de « marge gros −67 % » :
     elle conseillait d'acheter un produit revendu à perte. Deux étiquettes qui se
     contredisent, c'est un outil qu'on cesse de croire. La marge l'emporte. */
  if(mgw!=null&&mgw<0){ k='cher'; lib='revendu à perte'; }
  else if(mgw!=null&&mgw<mini&&k==='bon'){ k='ok'; lib='marge trop mince'; }

  /* « ne se vend pas » n'a de sens que si l'outil a vu passer des ventes.
     Tant que le journal des ventes est vide, TOUT paraît invendu — et le drapeau
     le plus voyant du tableau devient celui qui n'apprend rien. On se tait. */
  if(VENTES_CONNUES){
    if(c.mois===Infinity){
      /* la règle : aucune vente en 90 jours, avec au moins 90 jours de journal.
         Avec moins, on donne le fait brut et l'âge du journal — pas un verdict */
      if(JOURS_HIST>=90) flags.push(['','ne se vend pas — aucune vente en 90 j, '+nf(c.stock)+' en stock']);
      else if(JOURS_HIST>=14) flags.push(['i','aucune vente en '+nf(JOURS_HIST)+' j de journal — '+nf(c.stock)+' en stock']);
    }
    else if(c.mois>=6&&JOURS_HIST>=30) flags.push(['','stock pour '+Math.round(c.mois)+' mois']);
    else if(c.stock===0&&c.v90>0) flags.push(['i','rupture — '+nf(c.v90)+' vendus sur 90 j']);
    if(c.derniereVente) flags.push(['i','dernière vente le '+dfr(c.derniereVente)]);
  } else if(c.stock===0) flags.push(['i','plus rien en stock']);
  /* Sans historique de ventes, « déjà 385 en stock » ne faisait que répéter la
     colonne Stock, sur onze lignes sur douze. Un drapeau qui se répète partout
     ne signale plus rien : on ne garde que la rupture, qui est actionnable. */

  if(mgw!=null&&mgw<mini) flags.push(['c','marge gros '+mgw.toFixed(0)+' %']);
  if(c.amz!=null&&x.p!=null&&c.amz<x.p) flags.push(['c','Amazon vend moins cher ('+money2(c.amz)+')']);
  return {k,lib,flags};
}
const spark=(H)=>{ const P=H.filter(h=>h.p>0).slice(-12); if(P.length<2) return '';
  const mn=Math.min(...P.map(h=>h.p)), mx=Math.max(...P.map(h=>h.p)), w=64,h=18;
  const pts=P.map((x,i)=>`${(i/(P.length-1)*w).toFixed(1)},${(h-2-(mx===mn?h/2:(x.p-mn)/(mx-mn)*(h-4))).toFixed(1)}`).join(' ');
  return `<svg class="spk" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}"><polyline points="${pts}" fill="none" stroke="var(--iris)" stroke-width="1.5"/></svg>`; };

/* ---- l'étude ---- */
let TEXTE='', ETUDE=null;
function analyse(){
  if(!TEXTE||TEXTE.trim().length<12) return null;
  let L, X=null;
  const T=litTableau(TEXTE);
  if(T&&T.err) return T;
  if(T){ L=T.lignes; X={colonnes:T.colonnes}; } else L=litLignes(TEXTE);
  if(!L.length) return {err:"Aucune ligne exploitable : il faut au moins un code-barres et un prix par ligne."};
  let montant=0, eco=0, nBon=0, nCher=0, nInc=0, nEvite=0, nPerte=0;
  L.forEach(x=>{ x.cle=(x.bc?trouve(x.bc):null)||''; x.par=x.cle?'code':''; x.sur=''; x.cands=[];
    if(!x.cle && x.des){ const n=parNom(x.des); x.cands=n.cands; x.sur=n.sur; x.refuse=!!n.refuse; if(n.cle){ x.cle=n.cle; x.par=n.appris?'appris':'nom'; } }
    else if(x.cle && x.des && /[a-zà-ÿ]{3}/i.test(x.des)){ const sc=ressemble(x.des,x.cle); x.nomOk = sc==null ? null : sc>=0.3; }
    x.c=x.cle?connu(x.cle):null; x.v=verdict(x,x.c);
    if(x.par==='nom'&&x.sur==='hm') x.v.flags.unshift(['c','retrouvé par le nom — à vérifier']);
    else if(x.par==='nom') x.v.flags.unshift(['i','retrouvé par le nom']);
    else if(x.par==='appris') x.v.flags.unshift(['i','nom déjà corrigé une fois']);
    if(x.nomOk===false) x.v.flags.unshift(['c','le nom du devis ne ressemble pas au nôtre']);
    montant+=(x.q||0)*(x.p||0);
    if(x.c&&x.c.moy!=null&&x.p!=null) eco+=(x.c.moy-x.p)*(x.q||1);
    if(x.v.lib==='revendu à perte') nPerte++;
    else if(x.v.k==='bon') nBon++; else if(x.v.k==='cher') nCher++;
    if(x.v.k==='inc') nInc++;
    /* Sans ventes enregistrées, on ne peut pas dire qu'un stock est « de trop » :
       on l'ignore plutôt que de gonfler un compteur avec une supposition. */
    if(x.c&&VENTES_CONNUES&&(x.c.mois===Infinity||x.c.mois>=6)) nEvite++; });
  return {L,X,montant,eco,nBon,nCher,nInc,nEvite,nPerte};
}
function dessine(){
  const A=analyse(); ETUDE=A; const box=$('apercu'); $('acts').hidden=true; $('kpis').innerHTML=''; $('haut').hidden=true;
  const range=(oui)=>{ const b=document.getElementById('bandeau'), z=document.getElementById('zdepot');
    if(b) b.hidden=oui; if(z) z.classList.toggle('replie',oui); };
  if(!A){ box.innerHTML=''; range(false); return; }
  const nSans=(A.L||[]).filter(x=>!x.cle).length;
  $('haut-txt').innerHTML=`<b>Devis chargé</b> — <span>${nf((A.L||[]).length)} ligne${(A.L||[]).length>1?'s':''}</span>${nSans?`, <b>${nf(nSans)} non reconnue${nSans>1?'s':''}</b>`:''}. <span>Si le fichier a été mal lu, supprime-le et redépose-le.</span>`;
  $('haut').hidden=false;
  if(A.err){ box.innerHTML=`<div class="info" style="border-left-color:var(--crit);background:var(--crit-soft);white-space:pre-line">${esc(A.err)}</div>`; range(false); return; }
  range(true);

  /* Quatre chiffres, pas sept. « Références proposées » et « montant du devis »
     sont déjà lisibles au bas du tableau ; les garder en gros volait la place de
     la seule chose qui décide vraiment : ce que ce devis coûte ou fait gagner. */
  const aRisque=A.nCher+A.nPerte;
  $('kpis').innerHTML=`<div class="kpis">
    <div class="kpi gros"><span class="v ${A.eco>0?'g':A.eco<0?'c':''}">${A.eco?(A.eco>0?'−':'+')+money(Math.abs(A.eco)):'0 $'}</span>
      <span class="k">${A.eco>=0?'moins cher':'plus cher'} que ses prix d'achat habituels,<br>sur ${money(A.montant)} de devis</span></div>
    <div class="kpi"><span class="v g">${nf(A.nBon)}</span><span class="k">à prendre<br><i>bon prix, marge correcte</i></span></div>
    <div class="kpi"><span class="v ${aRisque?'c':''}">${nf(aRisque)}</span><span class="k">à discuter<br><i>${A.nPerte?A.nPerte+' revendu(s) à perte, ':''}${A.nCher} plus cher${A.nCher>1?'s':''} que d'habitude</i></span></div>
    <div class="kpi"><span class="v ${A.nEvite||A.nInc?'w':''}">${nf(A.nEvite+A.nInc)}</span><span class="k">à regarder de près<br><i>${A.nEvite?A.nEvite+' déjà bien en stock':''}${A.nEvite&&A.nInc?', ':''}${A.nInc?A.nInc+' inconnue'+(A.nInc>1?'s':'')+' du catalogue':''}${!A.nEvite&&!A.nInc?'rien à signaler':''}</i></span></div>
  </div>`;

  /* Une colonne vide sur toute sa hauteur occupe la place sans rien dire.
     « Dernier achat » ne s'affiche que si au moins une ligne en a un. */
  const aDernier=A.L.some(x=>x.c&&x.c.dernier);
  const aAmazon =A.L.some(x=>x.c&&x.c.amz!=null);

  const li=A.L.map(x=>{
    const choix=(x,i)=>`<select class="cand" data-i="${i}"><option value="">${x.cle?'— autre parfum ? —':'— choisir le parfum —'}</option>${(x.cands||[]).map(c=>`<option value="${esc(c.cle)}" ${c.cle===x.cle?'selected':''}>${esc((IDX[c.cle]||[])[2]||'')} ${esc((IDX[c.cle]||[])[1]||'')}${(IDX[c.cle]||[])[3]?' '+esc((IDX[c.cle]||[])[3])+' oz':''} · ${Math.round(c.sc*100)} %</option>`).join('')}${x.cle&&!(x.cands||[]).some(c=>c.cle===x.cle)?`<option value="${esc(x.cle)}" selected>${esc(IDX[x.cle][2])} ${esc(IDX[x.cle][1])}</option>`:''}<option value="__aucun">— aucun de ceux-là —</option></select>`;
    if(!x.cle) return `<tr class="linc"><td class="ref"><b>${esc(x.des||'—')}</b><span>${x.bc}</span></td>
      <td class="r">${x.q??'—'}</td><td class="r"><b>${money2(x.p)}</b></td>
      <td colspan="${aDernier?5:4}"><small>${x.bc?'Code-barres absent du catalogue : rien à comparer. Si Sam achète, l\'article se créera à la facture.'
        :x.refuse?'Marqué « aucun de ceux-là » — reste inconnu, sauf si tu choisis un parfum.'
        :(x.cands&&x.cands.length?'Pas sûr du parfum : choisis-le, l\'outil s\'en souviendra.':'Aucun parfum du catalogue ne ressemble à ce nom.')}</small>
        ${x.cands&&x.cands.length?choix(x,A.L.indexOf(x)):''}</td>
      <td class="vc"><span class="vd inc">inconnu</span></td></tr>`;
    const v=IDX[x.cle], c=x.c;
    const e=(c.moy!=null&&x.p!=null)?(x.p-c.moy)/c.moy*100:null;
    const mgw=(c.pvw!=null&&x.p!=null)?(c.pvw-x.p)/c.pvw*100:null, mgr=(c.pvr!=null&&x.p!=null)?(c.pvr-x.p)/c.pvr*100:null;
    const pc=(m)=>m==null?'<span class="na">—</span>':`<b class="${m<0?'c':m<(+REG.margeMin||10)?'c':m<20?'w':'g'}">${m.toFixed(0)} %</b>`;
    return `<tr class="l-${x.v.k}${x.par==='nom'&&x.sur==='hm'?' l-verif':''}"><td class="ref"><div class="mq">${esc(v[2])}</div><b>${esc(v[1])}</b><span>${v[0]}</span>${(x.par==='nom'||x.par==='appris'||x.nomOk===false)?`<small class="dnom">sur le devis : « ${esc(x.des)} »</small>${choix(x,A.L.indexOf(x))}`:''}</td>
      <td class="r">${x.q??'—'}</td>
      <td class="r"><b class="px">${money2(x.p)}</b></td>
      <td class="r">${c.moy!=null?money2(c.moy):'<span class="na">—</span>'}${e!=null?`<small class="${e<=-3?'g':e>=3?'c':''}">${e>0?'+':''}${e.toFixed(1)} %</small>`:'<small>aucun achat connu</small>'}</td>
      ${aDernier?`<td class="r">${c.dernier?`${money2(c.dernier.p)}<small>${dfr(c.dernier.d)}${c.dernier.f?' · '+esc(c.dernier.f):''}</small>`:'<span class="na">—</span>'}${c.meilleur&&c.nH>1?`<small>meilleur : ${money2(c.meilleur.p)}</small>`:''}${spark(HIST[x.cle]||[])}</td>`:''}
      <td class="r">${nf(c.stock)}${VENTES_CONNUES?`<small>${c.v90?nf(c.v90)+' vendus / 90 j':'rien vendu / 90 j'}</small>${c.mois!==Infinity&&c.v90?`<small>${c.mois<1?'moins d\'un mois':Math.round(c.mois)+' mois'} de stock</small>`:''}`:''}</td>
      <td class="r">${pc(mgw)}<small>revendu ${c.pvw!=null?money2(c.pvw):'—'}</small></td>
      <td class="r">${pc(mgr)}<small>retail ${c.pvr!=null?money2(c.pvr):'—'}</small>${aAmazon&&c.amz!=null?`<small>Amazon ${money2(c.amz)}</small>`:''}</td>
      <td class="vc"><span class="vd ${x.v.k}">${esc(x.v.lib)}</span>
        ${x.v.flags.length?`<div class="rem">${x.v.flags.map(([k,t])=>`<span class="fl ${k}">${esc(t)}</span>`).join('')}</div>`:''}</td></tr>`;
  }).join('');

  box.innerHTML=`<div style="overflow-x:auto"><table class="tb"><thead><tr>
      <th>Référence</th><th class="r">Qté</th><th class="r">Prix proposé</th><th class="r">Son prix habituel</th>
      ${aDernier?'<th class="r">Dernier achat</th>':''}
      <th class="r">Stock</th><th class="r">Marge en gros</th><th class="r">Marge en détail</th><th>Verdict</th>
    </tr></thead><tbody>${li}</tbody>
    <tfoot><tr><td>${nf(A.L.length)} référence${A.L.length>1?'s':''}</td>
      <td class="r">${nf(A.L.reduce((a,x)=>a+(+x.q||0),0))}</td>
      <td class="r"><b>${money(A.montant)}</b></td>
      <td colspan="${aDernier?6:5}"></td></tr></tfoot></table></div>
    ${A.X?`<p class="jargon">Colonnes reconnues : ${esc(A.X.colonnes)}.</p>`:''}
    ${VENTES_CONNUES?'':`<p class="jargon"><b>Aucune vente n'est encore enregistrée dans l'outil</b>,
      donc rien n'est dit ici sur la rotation des produits — l'étude compare les prix, pas les ventes.
      Ces indications apparaîtront d'elles-mêmes dès que les ventes seront saisies.</p>`}`;
  box.querySelectorAll('select.cand').forEach(sel=>sel.onchange=()=>{
    const x=A.L[+sel.dataset.i]; if(!x) return;
    const v=sel.value; if(!v) return;
    apprendNom(x.des, v==='__aucun'?'':v);
    dessine();
  });
  $('acts').hidden=false;
  try{ sauveBrouillon(); }catch(e){}
}
async function charge(file){
  $('msg').textContent=''; $('msg').className='msg';
  try{
    $('dz').querySelector('b').textContent='Lecture de '+file.name+'…';
    TEXTE=await lireFichier(file, m=>{ $('dz').querySelector('b').textContent=m; });
    $('dz').classList.add('lu'); $('dz').querySelector('b').textContent='Lu : '+file.name;
    $('colle').value=TEXTE;
  }catch(e){
    /* On ne vide PAS la zone de texte : elle peut contenir des lignes tapees a la
       main, et les effacer sur un depot rate serait pire que le depot rate. Mais
       on dit alors franchement que ce qui reste a l'ecran est l'ancien devis —
       sinon on lit une etude en croyant qu'elle vient du fichier qu'on vient de
       deposer. */
    const reste=($('colle').value||'').trim();
    $('msg').textContent=((e&&e.message)||'Lecture impossible.')
      + (reste?" L'étude affichée ci-dessous est encore celle du document précédent.":'');
    $('msg').className='msg err'; $('dz').classList.remove('lu');
    $('dz').querySelector('b').textContent='Dépose le devis ici, ou clique pour le choisir';
    TEXTE=reste; }
  dessine();
}
$('fichier').addEventListener('change',e=>{ const f=e.target.files[0]; if(f) charge(f); e.target.value=''; });
['dragenter','dragover'].forEach(ev=>$('dz').addEventListener(ev,e=>{ e.preventDefault(); $('dz').classList.add('sur'); }));
['dragleave','drop'].forEach(ev=>$('dz').addEventListener(ev,e=>{ e.preventDefault(); $('dz').classList.remove('sur'); }));
$('dz').addEventListener('drop',e=>{ const f=e.dataTransfer.files[0]; if(f) charge(f); });
$('basc').onclick=()=>{ $('txt').classList.toggle('on'); if($('txt').classList.contains('on')) $('colle').focus(); };
let cT=null; $('colle').addEventListener('input',()=>{ clearTimeout(cT); cT=setTimeout(()=>{ TEXTE=$('colle').value; dessine(); },300); });

/* ---- le devis en cours reste en place ----
   Avant, un devis collé ne vivait qu'en mémoire : on allait voir une fiche
   produit, on revenait, tout avait disparu — et il fallait recoller. Or c'est
   exactement ce qu'on fait pendant une étude : on va vérifier un stock, un
   prix, une fiche, et on revient.
   Le devis en cours est donc gardé, et il reste jusqu'à ce qu'on le supprime
   (« Étudier un autre devis ») ou qu'on le range (« Garder cette étude »).

   Volontairement en localStorage brut, et PAS via ecrit() : un brouillon en
   cours de saisie n'a rien à faire sur l'écran d'un collègue au milieu de sa
   propre étude. Ce qui se partage, ce sont les études gardées. */
const K_BRO='etude-brouillon-v1';
const BRO_MAX=400000;                      /* un devis, pas un catalogue entier */
function sauveBrouillon(){
  try{
    const t=TEXTE||'';
    if(!t.trim()){ localStorage.removeItem(K_BRO); return; }
    if(t.length>BRO_MAX) return;            /* trop gros : on ne garde rien plutôt que de saturer */
    localStorage.setItem(K_BRO, JSON.stringify({
      texte:t, frn:$('frn').value, date:$('date').value, num:$('num').value,
      t:new Date().toISOString() }));
  }catch(e){}
}
function oublieBrouillon(){ try{ localStorage.removeItem(K_BRO); }catch(e){} }
function litBrouillon(){
  try{ const b=JSON.parse(localStorage.getItem(K_BRO)||'null');
    return (b && typeof b==='object' && b.texte) ? b : null; }catch(e){ return null; }
}
function repriseBrouillon(){
  const b=litBrouillon(); if(!b) return false;
  TEXTE=b.texte;
  $('colle').value=b.texte; $('txt').classList.add('on');
  if(b.frn) $('frn').value=b.frn;
  if(b.date) $('date').value=b.date;
  if(b.num) $('num').value=b.num;
  dessine();
  const q=new Date(b.t||Date.now());
  const el=document.createElement('div');
  el.className='repris';
  el.innerHTML=`<b>Devis repris là où tu l'avais laissé</b> — collé le
    ${String(q.getDate()).padStart(2,'0')}/${String(q.getMonth()+1).padStart(2,'0')} à
    ${String(q.getHours()).padStart(2,'0')}h${String(q.getMinutes()).padStart(2,'0')}.
    Il restera ici tant que tu ne l'auras pas gardé ou remplacé.`;
  const k=$('kpis'); if(k&&k.parentNode) k.parentNode.insertBefore(el,k);
  return true;
}
/* « input » autant que « change » : sans lui, une référence tapée puis quittée
   par un clic ailleurs plutôt que par la tabulation n'était pas enregistrée. */
['frn','date','num'].forEach(i=>['input','change'].forEach(ev=>$(i).addEventListener(ev,sauveBrouillon)));

$('date').value=ajd();
$('l-frn').innerHTML=Object.keys(FRN).sort().map(n=>`<option value="${esc(n)}">`).join('');
/* « Étudier un autre devis » remet l'écran à neuf. Avant, le bouton s'appelait
   « Vider » : personne ne devine que c'est comme ça qu'on en commence un nouveau,
   et la date du devis précédent restait en place — on datait le devis suivant du
   jour du précédent sans s'en apercevoir. */
document.getElementById('sup-haut').onclick=()=>nouveauDevis();
function nouveauDevis(){
  if(TEXTE && TEXTE.trim().length>12 && !confirm(vf(
      "Effacer le devis à l'écran et en étudier un autre ?\n\n"
      +"Cette étude n'est pas gardée : si tu veux la retrouver plus tard, ferme cette fenêtre "
      +"et clique d'abord sur « Garder cette étude »."))) return;
  TEXTE=''; ETUDE=null;
  oublieBrouillon();
  document.querySelectorAll('.repris').forEach(e=>e.remove());
  $('colle').value=''; $('num').value=''; $('frn').value='';
  $('date').value=ajd();
  $('fichier').value='';
  $('dz').classList.remove('lu');
  $('dz').querySelector('b').textContent='Dépose le devis ici, ou clique pour le choisir';
  $('msg').textContent=''; $('msg').className='msg';
  dessine();
  $('frn').focus();
  window.scrollTo({top:0,behavior:'smooth'});
}
$('raz').onclick=nouveauDevis;

/* ---- garder / relire ---- */
$('garde').onclick=()=>{
  const A=ETUDE; if(!A||A.err) return;
  const frn=$('frn').value.trim()||'(fournisseur non précisé)';
  const e={id:'e'+Date.now().toString(36),frn,d:$('date').value||ajd(),num:$('num').value.trim(),
    par:USR||'(non renseigné)',t:new Date().toISOString(),montant:A.montant,eco:A.eco,nBon:A.nBon,nCher:A.nCher,nEvite:A.nEvite,
    lignes:A.L.map(x=>({bc:x.bc,cle:x.cle,ref:x.cle?(IDX[x.cle][2]+' '+IDX[x.cle][1]):(x.des||''),q:x.q,p:x.p,moy:x.c?x.c.moy:null,stock:x.c?x.c.stock:null,v90:x.c?x.c.v90:0,verdict:x.v.lib,flags:x.v.flags.map(f=>f[1])}))};
  ETU.push(e); ecrit(K.etu,ETU);
  const J=lit(K.jou,[]); J.push({t:new Date().toISOString(),u:USR||'(non renseigné)',act:'fournisseur',lib:'étude de devis gardée — '+frn+' — '+nf(A.L.length)+' références, '+money(A.montant),ref:frn,av:null,ap:(A.eco>=0?'économie ':'surcoût ')+money(Math.abs(A.eco))}); ecrit(K.jou,J);
  /* Une fois rangée, l'étude vit dans la liste du bas : garder AUSSI le brouillon
     la ferait réapparaître au prochain passage comme si elle n'avait pas été
     gardée, et on ne saurait plus laquelle des deux fait foi. */
  oublieBrouillon();
  document.querySelectorAll('.repris').forEach(el=>el.remove());
  $('msg').innerHTML='Étude gardée — elle est dans « Études gardées » en bas, avec un bouton <b>Rouvrir</b>.';
  $('msg').className='msg ok';
  dessineListe();
};
poseSortie('exp', ()=>{
  const A=ETUDE; if(!A||A.err) return null;
  const frn=$('frn').value.trim()||'fournisseur';
  return {
    titre:'Étude du devis — '+frn,
    fichier:'etude-devis-'+frn.replace(/\s+/g,'_')+($('date').value?'-'+$('date').value:''),
    filtre:'devis '+frn+($('date').value?' du '+$('date').value:'')+' · '+A.L.length+' ligne(s)',
    colonnes:[{t:'Code-barres'},{t:'Référence'},{t:'Quantité',y:'n'},{t:'Prix proposé',y:'m'},
      {t:'Prix d\'achat moyen',y:'m'},{t:'Écart',y:'p'},{t:'Dernier prix payé',y:'m'},
      {t:'Dernier achat',y:'d'},{t:'Stock',y:'n'},{t:'Vendus 90 j',y:'n'},
      {t:'Prix de gros',y:'m'},{t:'Marge gros',y:'p'},{t:'Verdict'},{t:'Remarques'}],
    lignes:A.L.map(x=>{ const v=x.cle?IDX[x.cle]:null, cc=x.c||{};
      return [x.bc, v?(v[2]+' '+v[1]):(x.des||''), x.q==null?null:+x.q, x.p,
        cc.moy, (cc.moy!=null&&x.p!=null)?((x.p-cc.moy)/cc.moy*100):null,
        cc.dernier&&cc.dernier.p, (cc.dernier&&cc.dernier.d)||'',
        cc.stock, cc.v90, cc.pvw, (cc.pvw!=null&&x.p!=null)?((cc.pvw-x.p)/cc.pvw*100):null,
        x.v.lib, x.v.flags.map(f=>f[1]).join(' · ')]; })
  };
});
function dessineListe(){
  const L=ETU.slice().sort((a,b)=>(b.t||'').localeCompare(a.t||''));
  $('nbe').textContent=L.length?`${nf(L.length)} étude${L.length>1?'s':''}`:'aucune';
  $('liste').innerHTML=!L.length?'<div class="vide">Les études gardées apparaîtront ici, avec leur verdict, pour comparer les devis d\'un même fournisseur dans le temps.</div>':
    `<table class="tb"><thead><tr><th>Date</th><th>Fournisseur</th><th>Réf.</th><th class="r">Lignes</th><th class="r">Montant</th><th class="r">Économie</th><th class="r">Bons prix</th><th class="r">Plus chers</th><th>Par</th><th></th></tr></thead><tbody>
    ${L.map(e=>`<tr><td>${dfr(e.d)}</td><td><b>${esc(e.frn)}</b></td><td>${esc(e.num||'—')}</td><td class="r">${nf(e.lignes.length)}</td><td class="r">${money(e.montant)}</td><td class="r ${e.eco>0?'g':e.eco<0?'c':''}">${e.eco?(e.eco>0?'−':'+')+money(Math.abs(e.eco)):'0 $'}</td><td class="r">${nf(e.nBon)}</td><td class="r">${nf(e.nCher)}</td><td>${esc(e.par||'')}</td><td class="r"><button class="btn sm" data-rl="${esc(e.id)}">Rouvrir</button> <button class="btn sm sup" data-sup="${esc(e.id)}" title="Supprimer définitivement cette étude">Supprimer</button></td></tr>`).join('')}</tbody></table>`;
  $('liste').querySelectorAll('[data-rl]').forEach(b=>b.onclick=()=>{ const e=ETU.find(x=>x.id===b.dataset.rl); if(!e) return;
    TEXTE=e.lignes.map(l=>`${l.bc}\t${l.ref}\t${l.q??''}\t${l.p??''}`).join('\n'); $('colle').value=TEXTE; $('txt').classList.add('on');
    $('frn').value=e.frn; $('date').value=e.d; $('num').value=e.num||''; dessine(); window.scrollTo({top:0,behavior:'smooth'}); });
  $('liste').querySelectorAll('[data-sup]').forEach(b=>b.onclick=()=>{
  const i=ETU.findIndex(x=>x.id===b.dataset.sup); if(i<0) return;
  const e=ETU[i];
  /* On nomme ce qu'on supprime : « Jeter cette étude ? » ne dit pas laquelle,
     et sur une liste de dix devis du même fournisseur, on efface le mauvais. */
  if(!confirm('Supprimer l\'étude du devis '+(e.num||'sans référence')+' de '+e.frn
      +' du '+dfr(e.d)+' ?\n\n'+nf(e.lignes.length)+' ligne(s), '+money(e.montant)
      +'.\nC\'est définitif — le devis d\'origine, lui, reste chez toi.')) return;
  ETU.splice(i,1); ecrit(K.etu,ETU);
  const J=lit(K.jou,[]); J.push({t:new Date().toISOString(),u:USR||'(non renseigné)',act:'suppression',
    lib:'étude de devis supprimée — '+e.frn+(e.num?' · '+e.num:''),ref:'',av:money(e.montant),ap:null});
  ecrit(K.jou,J);
  dessineListe();
});
}
window.__E={lit,qteEff,paEff,trouve,IDX,etude:()=>ETUDE,nouveauDevis,VENTES_CONNUES,
  litBrouillon,oublieBrouillon,sauveBrouillon,charge,apprendNom,dessine,texte:()=>TEXTE};
dessineListe();
repriseBrouillon();
$('sfoot').innerHTML=`${nf(Object.keys(HIST).length)} références avec historique d'achat`;
"""

JS = JS.replace('__LECTURE__', LECTURE).replace('__LIRE_PDF__', LIRE_PDF).replace('__NOMS__', _noms.NOMS)

html = coquille("Étude de devis", "Étude de devis",
  "Un devis de fournisseur, ligne par ligne, comparé à ce que Sam a déjà payé, à son stock et à ses ventes. "
  "L'outil dit ce qui vaut le coup, ce qui est plus cher que d'habitude, et ce qu'il est inutile de racheter.",
  CSS, CORPS.replace("__ACCEPT__", _lire.ACCEPT), JS, donnees=('produits',)).replace('__IDX__', 'Object.fromEntries(D_TOUS().map(r=>[r[15],[r[0],r[13],r[2],r[12],r[8],r[7],r[6]]]))')
# pdf.js, comme dans Factures : le script de page devient un module, après pdf.js
_m = re.search(r'<script type="text/plain" id="page-js">\n(const VER_URL=[^\n]*\n)?const \$=i=>document\.getElementById\(i\);', html)
assert _m, "ancre du script de page introuvable"
html = (html[:_m.start()]
        + '<script type="module">' + PDF_WORKER + '</script>\n'
        + '<script type="module">' + PDF_MAIN
        + '\npdfjsLib.GlobalWorkerOptions.workerSrc="inline";\nwindow.pdfjsLib=pdfjsLib;</script>\n'
        + '<script type="text/plain" id="page-js" data-module="1">\n' + (_m.group(1) or '')
        + 'const $=i=>document.getElementById(i);'
        + html[_m.end():])
open('etude.html', 'w').write(html)
print('etude.html', len(html) // 1024, 'Ko')
