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
# pdf.js n'est plus embarqué : _lire le charge à la demande depuis lib/pdfjs/ (12 sept. 2026).

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
.fld input.manque{border-color:var(--warn);box-shadow:0 0 0 3px color-mix(in srgb, var(--warn) 22%, transparent)}
.fdev{display:none;margin-top:4px;font-size:11.5px;color:var(--iris);font-weight:600}
.fdev.on{display:block}
.tb td .rn{display:inline-block;margin-left:6px;font-size:11px;color:var(--iris);cursor:pointer;text-decoration:underline dotted}
.tb td input.rni{padding:4px 8px;border:1px solid var(--iris);border-radius:6px;font:inherit;width:170px}
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
/* rien ne déborde (Igal, 24 sept. 2026) : les petites lignes sous un chiffre
   (fournisseur du dernier achat, « revendu … », mois de stock) passent à la ligne
   au lieu d'élargir la colonne ; les en-têtes longs aussi (« Marge en détail »,
   « Margen al por menor ») ; la référence garde une largeur lisible */
.tb td.r small{white-space:normal}
.tb th,.tb th.r{white-space:normal;vertical-align:bottom}
.tb td.ref{min-width:170px;max-width:340px;overflow-wrap:anywhere}
.tb td.vc{min-width:120px}
.vd{display:inline-block;padding:3px 9px;border-radius:99px;font-family:Inter,sans-serif;font-size:11px;font-weight:800;letter-spacing:.04em;white-space:nowrap}
.vd.bon{background:var(--good-soft);color:var(--good)}.vd.ok{background:var(--surface-2);color:var(--ink-2)}.vd.cher{background:var(--crit-soft);color:var(--crit)}
.vd.inc{background:var(--warn-soft);color:var(--warn)}
.fl{display:inline-block;margin:3px 4px 0 0;padding:2px 7px;border-radius:5px;font-size:11px;font-weight:600;background:var(--warn-soft);color:var(--warn)}
.fl.i{background:var(--iris-soft);color:var(--iris)}.fl.c{background:var(--crit-soft);color:var(--crit)}
.ref .dnom{display:block;margin-top:4px;font-size:11.5px;color:var(--ink-3);font-style:italic}
select.cand{display:block;margin-top:5px;width:100%;max-width:100%;min-width:0;font:12.5px Inter,sans-serif;padding:4px 6px;border:1px solid var(--line);border-radius:6px;background:var(--surface)}
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

/* ===== la liste du devis, refaite le 3 oct. 2026 : lisible, et modifiable dans la ligne ===== */
.filt{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:4px 0 12px}
.filt .fb{display:inline-flex;gap:7px;align-items:center;padding:7px 13px;border:1px solid var(--line);border-radius:99px;background:var(--surface);font:600 13px Inter,sans-serif;color:var(--ink-2);cursor:pointer}
.filt .fb b{font-variant-numeric:tabular-nums;color:var(--ink)}
.filt .fb:hover{border-color:var(--iris)}
.filt .fb.on{background:var(--ink);border-color:var(--ink);color:var(--surface)}.filt .fb.on b{color:var(--surface)}
.filt .f-stk0 b{color:var(--iris)}.filt .f-bon b{color:var(--good)}.filt .f-cher b,.filt .f-chk b{color:var(--crit)}.filt .f-inc b{color:var(--warn)}
.filt .rch{margin-left:auto;min-width:260px;flex:0 1 340px;padding:8px 12px;border:1px solid var(--line);border-radius:9px;font:inherit;font-size:13.5px;background:var(--surface)}
.tw2{border:1px solid var(--line);border-radius:12px;overflow:auto;max-height:calc(100vh - 150px);background:var(--surface)}
.tb2{width:100%;border-collapse:separate;border-spacing:0;font-size:13.5px}
.tb2 thead th{position:sticky;top:0;z-index:2;background:var(--surface-2);text-align:left;font:800 10.5px Inter,sans-serif;letter-spacing:.08em;text-transform:uppercase;color:var(--ink);padding:10px 8px;border-bottom:1px solid var(--line);white-space:normal;vertical-align:bottom}
.tb2 th.r,.tb2 td.r{text-align:right;font-variant-numeric:tabular-nums}
.tb2 td{padding:10px 8px;border-bottom:1px solid var(--line-2);vertical-align:middle}
.tb2 tbody tr:hover td{background:var(--surface-2)}
.tb2 tbody tr[hidden]{display:none}
.tb2 td.pf{min-width:200px;max-width:300px}
.tb2 .pnm{line-height:1.3}.tb2 .pnm b{font-size:14px;font-weight:700}
.tb2 .pmq{font:700 10.5px Inter,sans-serif;letter-spacing:.08em;text-transform:uppercase;color:var(--ink-3);margin-right:2px}
.tb2 .sub{font-size:11.5px;color:var(--ink-3);margin-top:2px}
.tb2 .lu{font-size:12px;color:var(--ink-3);margin-top:4px}.tb2 .lu i{font-style:normal;color:var(--ink-2)}
.tb2 .lu.av{color:var(--warn)}.tb2 .lu.av span{font-weight:700}
.tb2 .chx{margin-top:6px}.tb2 .chx select{width:100%;font:13px Inter,sans-serif;padding:6px 8px;border:1px solid var(--iris);border-radius:7px;background:var(--surface)}
.tb2 input.ed{width:70px;text-align:right;padding:6px 8px;border:1px solid var(--line);border-radius:7px;font:600 14px Inter,sans-serif;font-variant-numeric:tabular-nums;background:var(--surface);color:var(--ink)}
.tb2 input.ed:hover{border-color:var(--ink-3)}
.tb2 input.ed:focus{outline:0;border-color:var(--iris);box-shadow:0 0 0 3px var(--iris-soft)}
.tb2 input.ed.edt{border-color:var(--iris);background:var(--iris-soft)}
.tb2 input.ed.mauv{border-color:var(--crit);background:var(--crit-soft)}
.tb2 td small.off{color:var(--iris);font-weight:600;white-space:nowrap;margin-top:3px}
.tb2 td small{display:block;font-size:11.5px;color:var(--ink-3);line-height:1.35}
.tb2 .ec{display:block;font:700 12px Inter,sans-serif;color:var(--ink-3)}.tb2 .ec.g{color:var(--good)}.tb2 .ec.c{color:var(--crit)}
.tb2 .mg2 div{white-space:nowrap;line-height:1.55}.tb2 .mg2 em{font-style:normal;font-weight:600;color:var(--ink);font-variant-numeric:tabular-nums;margin-right:6px}.tb2 .mg2 b{display:inline-block;min-width:44px}
.tb2 td small.inl{display:inline;font-size:11.5px}
.tb2 td.stk{min-width:100px}.tb2 td.dsp b{font-size:14px}.tb2 td.stk small{max-width:150px;margin-left:auto}
.tb2 td.vc{min-width:150px;max-width:180px}
.tb2 td.vc .vd{white-space:normal;line-height:1.3;border-radius:8px;padding:4px 10px}.tb2 .mg2 span{font-size:11.5px;color:var(--ink-3);margin-right:4px}
.tb2 .mg2 b.g{color:var(--good)}.tb2 .mg2 b.w{color:var(--warn)}.tb2 .mg2 b.c{color:var(--crit)}
.tb2 td.vc{min-width:150px;max-width:220px}.tb2 td.vc small{margin-top:4px}.tb2 td.vc small.c{color:var(--crit);font-weight:600}
.vd.chk{background:var(--crit-soft);color:var(--crit)}
.tb2 tr.r-bon td:first-child{box-shadow:inset 3px 0 0 var(--good)}
.tb2 tr.r-cher td:first-child,.tb2 tr.r-chk td:first-child{box-shadow:inset 3px 0 0 var(--crit)}
.tb2 tr.r-inc td:first-child{box-shadow:inset 3px 0 0 var(--warn)}
.tb2 tr.r-inc td{background:color-mix(in srgb, var(--warn-soft) 55%, transparent)}
.tb2 td.inc-t{font-size:12.5px;color:var(--ink-2)}
.tb2 tfoot td{position:sticky;bottom:0;background:var(--surface-2);border-top:2px solid var(--line);font-weight:700;padding:10px 12px}
.tb2 tfoot .pied-t{font-weight:500;font-size:12.5px;color:var(--ink-3)}
.kpi.sel{background:var(--good-soft);border-color:transparent}
.bc-ent{display:grid;grid-template-columns:1fr 1fr;gap:14px;font-size:13.5px;line-height:1.5}
.bc-ent b{display:block;font-family:Inter,sans-serif;font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--ink-3);margin-bottom:3px}
.prev b.off{color:var(--iris)}.prev s{color:var(--ink-3)}
.bc-tot{display:flex;justify-content:space-between;padding:10px 12px;background:var(--surface-2);font-weight:700}
#bdc[disabled]{opacity:.45;cursor:not-allowed}
@media(max-width:700px){.filt .rch{margin-left:0;min-width:0;flex:1 1 100%}}
"""

CORPS = r"""
<div class="info" id="bandeau"><b>Un fournisseur propose un devis : vaut-il le coup ?</b> Dépose le devis (PDF, fichier à colonnes, ou lignes collées).
Pour chaque référence, l'outil compare le prix proposé au <b>prix d'achat moyen</b> de Sam, au dernier achat et au meilleur prix jamais payé,
regarde le <b>stock</b> et ce qui s'est <b>vendu sur 90 jours</b>, et calcule la <b>marge</b> aux prix de gros et de détail.
Rien n'est enregistré dans le stock ni dans les prix : c'est une étude, à garder ou à jeter.
<br>Une ligne mal reconnue se corrige dans la liste : le nom <b>et le code article du fournisseur</b> sont retenus, et la prochaine price list de ce fournisseur se lit toute seule.</div>

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
  <div class="fld"><label>Fournisseur</label><input id="frn" list="l-frn" placeholder="Nom du fournisseur"><datalist id="l-frn"></datalist><small class="fdev" id="frn-dev"></small></div>
  <div class="fld"><label>Date du devis</label><input id="date" type="date"></div>
  <div class="fld"><label>Référence du devis</label><input id="num" placeholder="facultatif"></div>
</div>

<div id="kpis"></div>
<div id="apercu"></div>
<div class="actions" id="acts" hidden>
  <button class="btn pri" id="bdc">Bon de commande</button>
  <button class="btn" id="garde">Garder cette étude</button>
  <span id="exp"></span>
  <button class="btn" id="raz">Étudier un autre devis</button>
  <span class="msg" id="msg"></span>
</div>

<!-- 4 oct. 2026 : le bon de commande, fait des quantités tapées dans « Je commande » -->
<div class="ov" id="bcov"><div class="mod" role="dialog" aria-modal="true" aria-labelledby="bct" style="max-width:760px">
  <div class="mh"><h2 id="bct">Bon de commande</h2><button class="x" id="bcx" aria-label="Fermer">&times;</button></div>
  <div class="mb">
    <div class="bc-ent" id="bc-ent"></div>
    <div class="prev" id="bc-liste"></div>
    <p class="hint">Trois façons de l'envoyer au fournisseur : le PDF (imprimer → « Enregistrer en PDF »), le fichier Excel, ou le texte à coller dans un e-mail ou un WhatsApp.</p>
  </div>
  <div class="mf"><span class="msg" id="bc-msg"></span>
    <button class="btn" id="bc-txt">Copier le texte</button>
    <button class="btn" id="bc-xls">Excel</button>
    <button class="btn pri" id="bc-pdf">Imprimer / PDF</button></div>
</div></div>

<h2 class="sec">Études gardées <em id="nbe"></em></h2>
<div id="liste"></div>
"""

JS = r"""
const IDX=__IDX__;
/* IDX = [bc, nom, marque, prix d'achat, prix gros, prix retail, qté, CONTENANCE, TYPE, genre].
   Attention à la place 3 : c'est le PRIX D'ACHAT, pas la contenance. Le menu de
   choix du parfum affichait « 22.5 oz » pour un flacon à 22,50 $ — la contenance
   est en 7 depuis qu'on l'y a mise. */
const GEN={M:'Homme',W:'Femme',U:'Unisexe',K:'Enfant'};
const ml7=cle=>String(((IDX[cle]||[])[7])||'').trim();
const tyBadge=cle=>{ const v=IDX[cle]||[]; const t=String(v[8]||'').trim(), g=GEN[String(v[9]||'').trim().toUpperCase()]||'';
  return (t?' <i class="ty" data-nolang>'+esc(t)+'</i>':'')+(g?' <i class="gn">'+esc(g)+'</i>':''); };
const tyTexte=cle=>{ const t=String(((IDX[cle]||[])[8])||'').trim(); return t?' '+t:''; };
const K={mod:'fiches-modifiees-v1',ext:'stock-externe-v1',hist:'prix-achat-hist-v1',vent:'ventes-v1',frn:'fournisseurs-v1',
         mar:'marche-v1',reg:'reglages-v1',etu:'etudes-devis-v1',jou:'crm-journal-v1'};
let MOD=lit(K.mod,{}), EXT=lit(K.ext,{q:{}}), HIST=lit(K.hist,{}), VENT=lit(K.vent,{}), FRN=lit(K.frn,{}), MAR=lit(K.mar,{});
let REG=Object.assign({margeMin:10},lit(K.reg,{}));
let ETU=lit(K.etu,[]); if(!Array.isArray(ETU)) ETU=base(K.etu,[]);
let USR=NOM_UTIL;
window.__nomChange.push(v=>{ USR=v; });
if(!EXT.q) EXT.q={};
const dfr=d=>{ if(!d) return '—'; const [a,m,j]=String(d).slice(0,10).split('-'); return j?`${m}/${j}/${a.slice(2)}`:d; };
function qteEff(cle){ const m=MOD[cle]; if(m&&m.qte!=null) return +m.qte; const v=IDX[cle]||[]; const e=EXT.q[v[0]]; return e!=null?+e:(v[6]||0); }
const paEff=cle=>{ const m=MOD[cle]; return (m&&m.pa!=null)?+m.pa:(IDX[cle]&&IDX[cle][3]!=null?+IDX[cle][3]:null); };
const pvwEff=cle=>{ const m=MOD[cle]; return (m&&m.pvw!=null)?+m.pvw:(IDX[cle]&&IDX[cle][4]!=null?+IDX[cle][4]:null); };
const pvrEff=cle=>{ const m=MOD[cle]; return (m&&m.pvr!=null)?+m.pvr:(IDX[cle]&&IDX[cle][5]!=null?+IDX[cle][5]:null); };
const parBC={}; Object.entries(IDX).forEach(([cle,v])=>{ parBC[v[0]]=cle; });
Object.entries(MOD).forEach(([cle,m])=>{ if(!m||!m.bcs||!IDX[cle]) return; String(m.bcs).split(/[^0-9]+/).filter(x=>x.length>=6).forEach(b=>{ if(!parBC[b]) parBC[b]=cle; }); });
Object.entries(bcExtra()).forEach(([cle,L])=>{ if(!IDX[cle]) return; L.forEach(b=>{ if(!parBC[b]) parBC[b]=cle; if(!parBC['0'+b]) parBC['0'+b]=cle; }); });
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
/* 3 oct. 2026 (Igal : « il y a vraiment un temps de latence quand je vais sur price list ») :
   pour chaque ligne reconnue par son code-barres, on cherchait son nom dans TOUT le
   catalogue (3 800 fiches) juste pour savoir s'il ressemble au nôtre — 1 000 lignes,
   1 000 tours complets, 7 s d'écran figé. On le compare maintenant à cette fiche-là seule. */
function ressemble(des,cle){
  if(!des||!cle) return null;
  if(typeof mScoreCle==='function'){ const sc=mScoreCle(des,cle); return sc>0.34?sc:0; }
  const r=mCherche(des); const c=r.cands.find(x=>x.cle===cle);
  return c?c.sc:0;
}
/* la correction de Sam est retenue : la prochaine fois, cette ligne est reconnue d'elle-même */
function apprendNom(des,cle){
  try{ const A=lit(K_ALIASN,{})||{}; const k=mNorm(des); if(!k) return;
    A[k]=cle||'__aucun'; ecrit(K_ALIASN,A); }catch(e){}
}

/* ---- retrouver par la référence du fournisseur ----
   Le nom d'une price list bouge : « Bleu EDP 3.4 » un mois, « CHANEL BLEU 100ML » le
   suivant. Le code article du fournisseur, lui, ne bouge pas. Corrigé une fois, il vaut
   pour toutes les listes suivantes de CE fournisseur — deux fournisseurs peuvent très
   bien donner le même code à deux parfums différents, la clé porte donc les deux.
   Rien n'est deviné ici : sans correction préalable, une référence ne reconnaît rien. */
const K_ALIASR='alias-refs-v1';
const rNorm=v=>String(v==null?'':v).toUpperCase().replace(/[^A-Z0-9]/g,'');
const fNorm=v=>String(v==null?'':v).normalize('NFD').replace(/[̀-ͯ]/g,'').toLowerCase().replace(/[^a-z0-9]/g,'');
const cleRef=(frn,ref)=>{ const r=rNorm(ref); return r?fNorm(frn)+'|'+r:''; };
function refAlias(ref,frn){
  try{ const k=cleRef(frn===undefined?($('frn')?$('frn').value:''):frn,ref); if(!k) return '';
    const A=lit(K_ALIASR,{})||{}; const c=A[k]; return (c&&IDX[c])?c:''; }catch(e){ return ''; }
}
function apprendRef(ref,cle,frn){
  try{ const k=cleRef(frn===undefined?($('frn')?$('frn').value:''):frn,ref); if(!k) return;
    const A=lit(K_ALIASR,{})||{};
    /* « aucun de ceux-là » n'apprend pas une référence : elle ne sert qu'à reconnaître,
       jamais à écarter — on retire simplement ce qui avait été retenu à tort. */
    if(cle) A[k]=cle; else delete A[k];
    ecrit(K_ALIASR,A); }catch(e){}
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
let DEBUT_HIST='';
const JOURS_HIST=(()=>{ try{ let min='';
  Object.values(VENT||{}).forEach(l=>(Array.isArray(l)?l:[]).forEach(x=>{ if(x&&x.q>0&&x.d&&(!min||x.d<min)) min=String(x.d).slice(0,10); }));
  DEBUT_HIST=min; return min?Math.max(0,Math.round((Date.now()-new Date(min).getTime())/86400000)):0; }catch(e){ return 0; } })();
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
  /* 3 oct. 2026 : « 9pm Elixir » à 3 352 $ (la colonne Stock lue comme le prix) affichait
     une marge de −11 459 %. Un prix 4 fois au-dessus de ce qu'on paie d'habitude, ou de
     notre prix de vente, n'est pas un mauvais prix : c'est une case à vérifier. */
  { const ref=c.moy!=null?c.moy:(c.pvw!=null?c.pvw:c.pvr);
    if(x.p!=null&&ref>0&&x.p>ref*4) return {k:'chk',lib:'prix à vérifier',flags:[['c','le prix proposé vaut '+Math.round(x.p/ref)+' fois notre prix habituel — colonne mal lue ?']]}; }
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
let TEXTE='', ETUDE=null, EDITS={}, FILTRE='';
function analyse(){
  if(!TEXTE||TEXTE.trim().length<12) return null;
  let L, X=null;
  const T=litTableau(TEXTE);
  if(T&&T.err) return T;
  if(T){ L=T.lignes; X={colonnes:T.colonnes}; } else L=litLignes(TEXTE);
  if(!L.length) return {err:"Aucune ligne exploitable : il faut au moins un code-barres et un prix par ligne."};
  /* les retouches faites à l'écran (quantité, prix) — gardées avec le brouillon */
  L.forEach((x,i)=>{ x.p0=x.p; const e=EDITS[i]; if(!e) return; if('q' in e){ x.q=e.q; x.edQ=true; } if('p' in e&&e.p!=null&&e.p!==x.p0){ x.p=e.p; x.edP=true; } });
  L.forEach(x=>{ x.cle=(x.bc?trouve(x.bc):null)||''; x.par=x.cle?'code':''; x.sur=''; x.cands=[];
    /* la référence déjà corrigée passe avant le nom : c'est une décision de Sam, pas une
       ressemblance calculée */
    if(!x.cle && x.ref){ const a=refAlias(x.ref); if(a){ x.cle=a; x.par='ref'; } }
    if(!x.cle && x.des){ const n=parNom(x.des); x.cands=n.cands; x.sur=n.sur; x.refuse=!!n.refuse; if(n.cle){ x.cle=n.cle; x.par=n.appris?'appris':'nom'; } }
    else if(x.par==='ref' && x.des){ x.cands=parNom(x.des).cands; }
    else if(x.cle && x.des && /[a-zà-ÿ]{3}/i.test(x.des)){ const sc=ressemble(x.des,x.cle); x.nomOk = sc==null ? null : sc>=0.3; }
    evalue(x); });
  return Object.assign({L,X},compte(L));
}
/* le verdict d'une ligne, refait seul quand Sam change sa quantité ou son prix */
function evalue(x){
  x.c=x.cle?connu(x.cle):null; x.v=verdict(x,x.c);
  if(x.par==='nom'&&x.sur==='hm') x.v.flags.unshift(['c','retrouvé par le nom — à vérifier']);
  else if(x.par==='nom') x.v.flags.unshift(['i','retrouvé par le nom']);
  else if(x.par==='appris') x.v.flags.unshift(['i','nom déjà corrigé une fois']);
  else if(x.par==='ref') x.v.flags.unshift(['i','référence fournisseur déjà corrigée une fois']);
  if(x.nomOk===false) x.v.flags.unshift(['c','le nom du devis ne ressemble pas au nôtre']);
}
/* les chiffres du haut, recomptés sur toutes les lignes */
function compte(L){
  let montant=0, eco=0, nBon=0, nCher=0, nInc=0, nEvite=0, nPerte=0, nChk=0, nOk=0, qSel=0, mSel=0;
  L.forEach(x=>{
    montant+=(x.q||0)*(x.p||0);
    if(x.q>0){ qSel+=x.q; mSel+=x.q*(x.p||0); }
    if(x.v.k!=='chk'&&x.c&&x.c.moy!=null&&x.p!=null) eco+=(x.c.moy-x.p)*(x.q||1);
    if(x.v.lib==='revendu à perte') nPerte++;
    else if(x.v.k==='bon') nBon++; else if(x.v.k==='cher') nCher++;
    if(x.v.k==='inc') nInc++; if(x.v.k==='chk') nChk++; if(x.v.k==='ok') nOk++;
    /* Sans ventes enregistrées, on ne peut pas dire qu'un stock est « de trop » :
       on l'ignore plutôt que de gonfler un compteur avec une supposition. */
    if(x.c&&VENTES_CONNUES&&JOURS_HIST>=30&&(x.c.mois===Infinity||x.c.mois>=6)) nEvite++; });
  return {montant,eco,nBon,nCher,nInc,nEvite,nPerte,nChk,nOk,qSel,mSel};
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
  peintKpis(A);
  /* ---- La liste, refaite le 3 oct. 2026 (Igal : « cette page n'est vraiment pas claire, et
     elle est moche — fais quelque chose de plus lisible et modifiable ») :
     - des onglets en haut pour ne voir qu'une sorte de lignes (à prendre, à discuter…) et
       une recherche, au lieu de 1 700 lignes à faire défiler ;
     - une ligne = un parfum, sur une hauteur : nom, quantité, prix, notre prix habituel avec
       l'écart, notre stock, les deux marges l'une sous l'autre, UN verdict ;
     - la quantité et le prix se corrigent dans la ligne (colonne mal lue, quantité voulue) :
       le verdict et les totaux suivent tout de suite, et c'est gardé avec le devis ;
     - la liste « choisir le parfum » ne s'ouvre que quand on clique « changer ». ---- */
  A.AVD=A.L.some(x=>x.dispo!=null);
  const LI=A.L.map((x,ix)=>ligneHTML(x,ix));
  const PREM=150, tok=(window.__etTok=(window.__etTok||0)+1);
  box.innerHTML=`<div class="filt" id="filt">${filtresHTML(A)}
      <input class="rch" id="rch" type="search" placeholder="Chercher un parfum, une marque, un code-barres…" autocomplete="off"></div>
    <div class="tw2"><table class="tb2" id="tb2"><thead><tr>
      <th>Parfum</th>${A.L.some(x=>x.dispo!=null)?'<th class="r">Stock fournisseur</th>':''}<th class="r">${A.L.some(x=>x.dispo!=null)?'Je commande':'Qté'}</th><th class="r" title="${esc(L3("Le prix de la price list. Tape le tien pour faire une contre-offre : le bon de commande montrera les deux.","The list price. Type yours to make a counter-offer: the purchase order will show both.","El precio de la lista. Escribe el tuyo para hacer una contraoferta: la orden mostrará ambos."))}">Prix proposé</th><th class="r">Notre prix habituel</th>
      <th class="r">Notre stock</th><th class="r">Nos prix de vente · ta marge</th><th>Verdict</th>
    </tr></thead><tbody>${LI.slice(0,PREM).join('')}</tbody>
    <tfoot><tr><td id="pied-n"></td>${A.AVD?'<td></td>':''}<td class="r" id="pied-q"></td><td class="r" id="pied-m"></td><td colspan="4" class="pied-t" id="pied-t"></td></tr></tfoot></table></div>
    ${A.X?`<p class="jargon"><span>Colonnes reconnues :</span> ${String(A.X.colonnes||'').split(', ').map(x=>{ const [a,b]=x.split(' → '); return b?`<span>${esc(a)}</span> → <span data-nolang>${esc(b)}</span>`:`<span data-nolang>${esc(x)}</span>`; }).join(', ')}.</p>`:''}`;
  peintPied(A);
  const tb=box.querySelector('tbody');
  if(LI.length>PREM){ let i=PREM;
    const suite=()=>{ if(tok!==window.__etTok||!tb.isConnected) return;
      tb.insertAdjacentHTML('beforeend',LI.slice(i,i+300).join('')); i+=300; filtre();
      if(i<LI.length) setTimeout(suite,0); };
    setTimeout(suite,30); }
  /* les onglets, la recherche */
  $('filt').onclick=e=>{ const b=e.target.closest('[data-f]'); if(!b) return; FILTRE=b.dataset.f; filtre(); };
  $('rch').oninput=()=>filtre();
  filtre();
  /* « changer » ouvre la liste des parfums ; un choix est retenu (nom et référence du fournisseur) */
  box.onclick=e=>{ const c=e.target.closest('[data-chg]'); if(!c) return; const z=c.parentNode.parentNode.querySelector('.chx'); if(z){ z.hidden=!z.hidden; const s=z.querySelector('select'); if(s&&!z.hidden) s.focus(); } };
  box.onchange=e=>{
    const sel=e.target.closest&&e.target.closest('select.cand');
    if(sel){ const x=(ETUDE&&ETUDE.L||[])[+sel.dataset.i]; if(!x) return;
      const v=sel.value; if(!v) return;
      apprendNom(x.des, v==='__aucun'?'':v);
      /* et sa référence, s'il y en a une : c'est elle qui tiendra quand le libellé changera */
      if(x.ref) apprendRef(x.ref, v==='__aucun'?'':v);
      dessine(); return; }
    const ed=e.target.closest&&e.target.closest('input[data-ed]');
    if(ed) retouche(ed);
  };
  box.onkeydown=e=>{ if(e.key==='Enter'&&e.target.matches&&e.target.matches('input[data-ed]')){ e.preventDefault(); e.target.blur(); } };
  $('acts').hidden=false;
  try{ sauveBrouillon(); }catch(e){}
}
/* une quantité ou un prix corrigé dans la ligne */
function retouche(inp){
  const A=ETUDE; if(!A) return; const i=+inp.dataset.i, x=A.L[i]; if(!x) return;
  const k=inp.dataset.ed, t=String(inp.value||'').trim(), v=t===''?null:nombre(t);
  if(t!==''&&(v==null||v<0)){ inp.classList.add('mauv'); return; }
  inp.classList.remove('mauv');
  x[k]=v; (EDITS[i]=EDITS[i]||{})[k]=v; if(k==='q') x.edQ=true; else x.edP=true;
  evalue(x);
  const tr=inp.closest('tr'); if(tr){ tr.outerHTML=ligneHTML(x,i); }
  Object.assign(A,compte(A.L)); peintKpis(A); peintPied(A); $('filt').innerHTML=filtresHTML(A)+$('filt').querySelector('.rch').outerHTML;
  $('rch').oninput=()=>filtre(); filtre();
  try{ sauveBrouillon(); }catch(e){}
}
/* Igal, 4 oct. 2026 : « qu'il puisse voir vite les produits qui ne sont pas dans le stock de Sam,
   sans faire défiler toute la liste » — l'onglet « Pas en stock chez nous » : les parfums connus
   dont il n'a plus un flacon. Les inconnus du catalogue restent à part (on ne sait rien d'eux). */
const FILTRES=[['','Tout'],['stk0','Pas en stock chez nous'],['bon','À prendre'],['cher','À discuter'],['ok','Dans les prix'],['chk','Prix à vérifier'],['inc','Inconnus'],['sel','Ma sélection']];
function filtresHTML(A){
  const n={'':A.L.length,stk0:A.L.filter(x=>x.cle&&x.c&&!(x.c.stock>0)).length,bon:A.nBon,cher:A.nCher+A.nPerte,ok:A.nOk,chk:A.nChk,inc:A.nInc,sel:A.L.filter(x=>x.q>0).length};
  return FILTRES.filter(([k])=>k===''||n[k]>0).map(([k,lib])=>`<button type="button" class="fb${FILTRE===k?' on':''} f-${k||'tout'}" data-f="${k}"><span>${lib}</span> <b>${nf(n[k])}</b></button>`).join('');
}
function filtre(){
  const tb=$('tb2'); if(!tb) return;
  const q=String(($('rch')||{}).value||'').trim().toLowerCase();
  document.querySelectorAll('#filt .fb').forEach(b=>b.classList.toggle('on',b.dataset.f===FILTRE));
  tb.querySelectorAll('tbody tr').forEach(tr=>{
    const okF=!FILTRE||(FILTRE==='sel'?tr.dataset.sel==='1':FILTRE==='stk0'?tr.dataset.stk==='0':tr.dataset.k===FILTRE);
    const okQ=!q||(tr.dataset.s||'').includes(q);
    tr.hidden=!(okF&&okQ); });
}
function peintKpis(A){
  const aRisque=A.nCher+A.nPerte;
  $('kpis').innerHTML=`<div class="kpis">
    <div class="kpi gros"><span class="v ${A.eco>0?'g':A.eco<0?'c':''}">${A.eco?(A.eco>0?'−':'+')+money(Math.abs(A.eco)):'0 $'}</span>
      <span class="k">${A.eco>=0?'moins cher':'plus cher'} que ses prix d'achat habituels</span></div>
    <div class="kpi"><span class="v g">${nf(A.nBon)}</span><span class="k">à prendre<br><i>bon prix, marge correcte</i></span></div>
    <div class="kpi"><span class="v ${aRisque?'c':''}">${nf(aRisque)}</span><span class="k">à discuter<br><i>${A.nPerte?A.nPerte+' revendu(s) à perte, ':''}${A.nCher} plus cher${A.nCher>1?'s':''} que d'habitude</i></span></div>
    ${A.qSel>0?`<div class="kpi sel"><span class="v">${money(A.mSel)}</span><span class="k">ma sélection<br><i>${nf(A.qSel)} flacon${A.qSel>1?'s':''} sur ${nf(A.L.filter(x=>x.q>0).length)} parfum${A.L.filter(x=>x.q>0).length>1?'s':''}</i></span></div>`
      :`<div class="kpi"><span class="v ${A.nEvite||A.nInc||A.nChk?'w':''}">${nf(A.nEvite+A.nInc+A.nChk)}</span><span class="k">à regarder de près<br><i>${[A.nChk?A.nChk+' prix à vérifier':'',A.nEvite?A.nEvite+' déjà bien en stock':'',A.nInc?A.nInc+' inconnue'+(A.nInc>1?'s':'')+' du catalogue':''].filter(Boolean).join(', ')||'rien à signaler'}</i></span></div>`}
  </div>`;
}
function peintPied(A){
  const n=A.L.length, q=A.L.reduce((a,x)=>a+(+x.q||0),0);
  const nb=A.L.filter(x=>x.q>0).length, b=$('bdc');
  if(b){ b.disabled=!nb; b.textContent=nb?`Bon de commande (${nf(nb)} parfum${nb>1?'s':''})`:'Bon de commande'; }
  if($('pied-n')) $('pied-n').textContent=`${nf(n)} référence${n>1?'s':''}`;
  if($('pied-q')) $('pied-q').textContent=q?nf(q):'—';
  if($('pied-m')) $('pied-m').textContent=A.montant?money(A.montant):'—';
  if($('pied-t')) $('pied-t').textContent=q?'':'Tape une quantité sur les parfums qui t\'intéressent : le total se fait ici.';
}
/* une ligne de la liste */
const pct0=m=>m==null?'—':(m>0?'+':m<0?'−':'')+Math.abs(m).toFixed(0)+' %';
const pctM=m=>m==null?'—':(m<0?'−':'')+Math.abs(m).toFixed(0)+' %';
function ligneHTML(x,ix){
  const choix=()=>`<select class="cand" data-i="${ix}"><option value="">${x.cle?'— un autre parfum ? —':'— choisir le parfum —'}</option>${(x.cands||[]).map(c=>`<option value="${esc(c.cle)}" ${c.cle===x.cle?'selected':''}>${esc((IDX[c.cle]||[])[2]||'')} ${esc((IDX[c.cle]||[])[1]||'')}${esc(tyTexte(c.cle))}${ml7(c.cle)?' '+esc(ml7(c.cle))+' oz':''} · ${Math.round(c.sc*100)} %</option>`).join('')}${x.cle&&!(x.cands||[]).some(c=>c.cle===x.cle)?`<option value="${esc(x.cle)}" selected>${esc(IDX[x.cle][2])} ${esc(IDX[x.cle][1])}${esc(tyTexte(x.cle))}</option>`:''}<option value="__aucun">— aucun de ceux-là —</option></select>`;
  const inp=(k,v,ed)=>`<input class="ed${ed?' edt':''}" data-ed="${k}" data-i="${ix}" inputmode="decimal" value="${v==null?'':String(v).replace('.',',')}" placeholder="—">`;
  const sub=[x.bc?`<span data-nolang>${esc(x.bc)}</span>`:'',x.ref?`<span data-nolang>${esc(x.ref)}</span>`:''].filter(Boolean).join(' · ');
  const dispoTd=(ETUDE&&ETUDE.L&&ETUDE.AVD)?`<td class="r dsp">${x.dispo!=null?`<b>${nf(x.dispo)}</b>`:'<span class="na">—</span>'}</td>`:'';
  const srch=esc(((x.cle?(IDX[x.cle][2]+' '+IDX[x.cle][1]):'')+' '+(x.des||'')+' '+(x.bc||'')+' '+(x.ref||'')).toLowerCase());
  const k=x.v.k, sel=x.q>0?'1':'0';
  if(!x.cle){
    return `<tr class="r-inc" data-k="inc" data-sel="${sel}" data-s="${srch}"><td class="pf"><div class="pnm"><b data-nolang>${esc(x.des||'—')}</b></div><div class="sub">${sub}</div></td>
      ${dispoTd}<td class="r">${inp('q',x.q,x.edQ)}</td><td class="r">${inp('p',x.p,x.edP)}${x.edP&&x.p0!=null?`<small class="off">${L3('notre offre — sa price list :','our offer — his list price:','nuestra oferta — su lista:')} <span data-nolang>${money2(x.p0)}</span></small>`:''}</td>
      <td colspan="3" class="inc-t">${x.cands&&x.cands.length
        ?`<span>${x.refuse?'Marqué « aucun de ceux-là ».':'Pas sûr du parfum.'}</span> <button type="button" class="lnk" data-chg>choisir le parfum</button><div class="chx" hidden>${choix()}</div>`
        :`<span>${x.bc?'Code-barres absent du catalogue : rien à comparer.':'Aucun parfum du catalogue ne ressemble à ce nom.'}</span>`}</td>
      <td><span class="vd inc">inconnu</span></td></tr>`;
  }
  const v=IDX[x.cle], c=x.c||{};
  const e=(c.moy!=null&&x.p!=null)?(x.p-c.moy)/c.moy*100:null;
  const mgw=(c.pvw!=null&&x.p!=null)?(c.pvw-x.p)/c.pvw*100:null, mgr=(c.pvr!=null&&x.p!=null)?(c.pvr-x.p)/c.pvr*100:null;
  const cm=m=>m==null?'':m<(+REG.margeMin||10)?'c':m<20?'w':'g';
  const chk=k==='chk';
  const lu=(x.par==='nom'||x.par==='appris'||x.par==='ref'||x.nomOk===false);
  const aVerif=(x.par==='nom'&&x.sur==='hm')||x.nomOk===false;
  const f0=x.v.flags.find(f=>!/^(retrouvé par le nom|nom déjà corrigé|référence fournisseur déjà|marge gros |dernière vente le |aucune vente en |ne se vend pas)/.test(f[1])&&f[1]!=='le nom du devis ne ressemble pas au nôtre');
  /* Igal, 3 oct. 2026 (« 27 · rien vendu / 90 j · gros 10 % · plus cher · marge gros 10 % — je ne
     comprends pas du tout ») : le verdict dit maintenant quoi faire, avec le chiffre qui le justifie */
  const VLIB={'bon prix':'Bon prix : à prendre','plus cher':'Plus cher que d\'habitude'+(e!=null?' ('+pct0(e)+')':'')+' : à négocier',
    'revendu à perte':'Revendu à perte : ne pas prendre','marge trop mince':'Marge trop faible','dans les prix':'Prix habituel',
    'premier achat':'Jamais acheté avant','prix à vérifier':'Prix à vérifier'};
  const vlib=VLIB[x.v.lib]||x.v.lib;
  return `<tr class="r-${k}${aVerif?' r-verif':''}" data-k="${k==='cher'&&x.v.lib==='revendu à perte'?'cher':k}" data-sel="${sel}" data-stk="${c.stock>0?'1':'0'}" data-s="${srch}">
    <td class="pf"><div class="pnm"><span class="pmq" data-nolang>${esc(v[2])}</span> <b data-nolang>${esc(v[1])}</b>${tyBadge(x.cle)}</div>
      <div class="sub">${sub}</div>
      ${lu?`<div class="lu${aVerif?' av':''}"><span>${aVerif?'À vérifier — lu sur le devis :':'Lu sur le devis :'}</span> <i data-nolang>« ${esc(x.des||x.ref)} »</i> <button type="button" class="lnk" data-chg>changer</button></div><div class="chx" hidden>${choix()}</div>`:''}</td>
    ${dispoTd}<td class="r">${inp('q',x.q,x.edQ)}</td>
    <td class="r">${inp('p',x.p,x.edP)}${x.edP&&x.p0!=null?`<small class="off">${L3('notre offre — sa price list :','our offer — his list price:','nuestra oferta — su lista:')} <span data-nolang>${money2(x.p0)}</span></small>`:''}</td>
    <td class="r"><b>${c.moy!=null?money2(c.moy):'—'}</b>${e!=null&&!chk?`<span class="ec ${e<=-3?'g':e>=3?'c':''}">${pct0(e)}</span>`:(c.moy==null?'<small>jamais acheté</small>':'')}${c.dernier&&c.dernier.p&&(c.moy==null||Math.abs(c.dernier.p-c.moy)>=0.01)?`<small>dernier achat : ${money2(c.dernier.p)}</small>`:''}</td>
    <td class="r stk"><b>${nf(c.stock||0)}</b> <small class="inl">en stock</small>${VENTES_CONNUES?`<small>${JOURS_HIST<90
        ?(c.v90?nf(c.v90)+' vendu'+(c.v90>1?'s':'')+' depuis le '+String(DEBUT_HIST).slice(5).replace('-','/'):'aucune vente depuis le '+String(DEBUT_HIST).slice(5).replace('-','/'))
        :(c.v90?nf(c.v90)+' vendus en 90 jours':'aucune vente en 90 jours')}</small>${JOURS_HIST>=30&&c.mois!==Infinity&&c.v90&&c.stock?`<small>${c.mois<1?'moins d\'un mois':Math.round(c.mois)+' mois'} de stock</small>`:''}`:''}</td>
    <td class="r mg2">${chk?'<span class="na">—</span>':`<div><span>en gros</span> <em>${c.pvw!=null?money2(c.pvw):'—'}</em> <b class="${cm(mgw)}">${mgw==null?'—':pctM(mgw)}</b></div><div><span>au détail</span> <em>${c.pvr!=null?money2(c.pvr):'—'}</em> <b class="${cm(mgr)}">${mgr==null?'—':pctM(mgr)}</b></div>`}</td>
    <td class="vc"><span class="vd ${k}">${esc(vlib)}</span>${f0?`<small class="${f0[0]==='c'?'c':''}" title="${esc(x.v.flags.map(f=>f[1]).join(' · '))}">${esc(f0[1])}</small>`:''}</td></tr>`;
}
/* ---- le fournisseur se devine ----
   4 oct. 2026 (Igal : « tu me parles de UNITED, mais ça ne les met pas quand je veux garder en
   archive cette price list ») : la case « Fournisseur » restait vide si personne ne la tapait,
   et l'étude partait aux archives sous « (fournisseur non précisé) » — inutile pour comparer ses
   price lists dans le temps. On lit donc le nom du fichier et les premières lignes du document :
   un fournisseur déjà connu (fiche Fournisseurs, étude gardée) qui s'y trouve est pris ; sinon
   le premier mot du nom du fichier qui n'est pas « price list », « stock », une date… Et on le
   dit sous la case, pour qu'on corrige d'un coup d'œil si ce n'est pas lui. */
const FRN_BRUIT=/^(price|pricelist|list|liste|lista|prix|precio|precios|stock|inventory|inventario|inventaire|catalog|catalogue|catalogo|offer|offre|oferta|devis|quote|cotizacion|copy|copie|copia|new|nouveau|nuevo|final|update|updated|maj|v\d*|the|of|de|du|des|la|le|les|el|los|and|et|y|sheet|feuille|hoja|xlsx|xls|csv|pdf|txt|wholesale|perfume|perfumes|parfum|parfums|fragrance|fragrances|usd|eur|jan|janv|feb|fev|mar|apr|avr|abr|may|mai|jun|juin|jul|juil|aug|aout|ago|sep|sept|oct|nov|dec|dic|january|february|march|april|june|july|august|september|october|november|december|janvier|fevrier|mars|avril|juin|juillet|septembre|octobre|novembre|decembre|enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre|\d+)$/i;
const frnNorm=t=>String(t||'').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/[^a-z0-9]+/g,' ').trim();
function frnConnus(){
  const S=new Set(Object.keys(FRN||{}));
  (ETU||[]).forEach(e=>{ if(e&&e.frn&&!/^\(/.test(e.frn)) S.add(e.frn); });
  return [...S].filter(n=>frnNorm(n).replace(/ /g,'').length>=3).sort((a,b)=>b.length-a.length);
}
function devineFrn(nomFichier, texte){
  const dev=$('frn-dev'); if(dev){ dev.textContent=''; dev.className='fdev'; }
  if($('frn').value.trim()) return null;
  const base=String(nomFichier||'').replace(/\.[a-z0-9]{2,5}$/i,'');
  const tete=String(texte||'').split(/\r?\n/).slice(0,15).join(' ');
  const hayF=' '+frnNorm(base)+' ', hayT=' '+frnNorm(tete)+' ';
  let nom=null, dou=null;
  for(const n of frnConnus()){ const k=' '+frnNorm(n)+' '; if(hayF.includes(k)){ nom=n; dou='nom du fichier'; break; } }
  if(!nom) for(const n of frnConnus()){ const k=' '+frnNorm(n)+' '; if(hayT.includes(k)){ nom=n; dou='document'; break; } }
  if(!nom){
    const mots=base.split(/[\s_\-.,()\[\]]+/).filter(m=>/[a-zA-Zà-ÿ]{3}/.test(m)&&!FRN_BRUIT.test(m));
    if(mots.length){ nom=mots.slice(0, mots.length>1&&!FRN_BRUIT.test(mots[1])&&mots[1].length<=12?2:1).join(' '); dou='nom du fichier'; }
  }
  if(!nom) return null;
  $('frn').value=nom; $('frn').classList.remove('manque'); sauveBrouillon();
  if(dev){ dev.innerHTML=vf('fournisseur lu dans le '+dou)+' — <span data-nolang>'+esc(nom)+'</span>. '+vf("Corrige si ce n'est pas lui."); dev.className='fdev on'; }
  return nom;
}
$('frn').addEventListener('input',()=>{ $('frn').classList.remove('manque'); const d=$('frn-dev'); if(d) d.className='fdev'; });
/* garder sans fournisseur : on refuse, et on montre où l'écrire */
function frnManque(){
  if($('frn').value.trim()) return false;
  $('frn').classList.add('manque'); $('frn').focus();
  $('msg').innerHTML=vf("Écris d'abord le nom du fournisseur, dans la case « Fournisseur » en haut : sans lui, l'étude gardée ne dit pas de qui vient la price list.");
  $('msg').className='msg err';
  window.scrollTo({top:0,behavior:'smooth'});
  return true;
}
async function charge(file){
  $('msg').textContent=''; $('msg').className='msg';
  try{
    $('dz').querySelector('b').textContent='Lecture de '+file.name+'…';
    TEXTE=await lireFichier(file, m=>{ $('dz').querySelector('b').textContent=m; }); EDITS={};
    $('dz').classList.add('lu'); $('dz').querySelector('b').textContent='Lu : '+file.name;
    $('colle').value=TEXTE;
    devineFrn(file.name, TEXTE);
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
      texte:t, frn:$('frn').value, date:$('date').value, num:$('num').value, ed:EDITS,
      t:(litBrouillon()||{}).t||new Date().toISOString() }));
  }catch(e){}
}
function oublieBrouillon(){ try{ localStorage.removeItem(K_BRO); }catch(e){} }
function litBrouillon(){
  try{ const b=JSON.parse(localStorage.getItem(K_BRO)||'null');
    return (b && typeof b==='object' && b.texte) ? b : null; }catch(e){ return null; }
}
function repriseBrouillon(){
  const b=litBrouillon(); if(!b) return false;
  TEXTE=b.texte; EDITS=(b.ed&&typeof b.ed==='object')?b.ed:{};
  $('colle').value=b.texte; $('txt').classList.add('on');
  if(b.frn) $('frn').value=b.frn;
  if(b.date) $('date').value=b.date;
  if(b.num) $('num').value=b.num;
  dessine();
  const q=new Date(b.t||Date.now());
  const el=document.createElement('div');
  el.className='repris';
  el.innerHTML=`<b>Repris là où tu l'avais laissé</b> — collé le
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
  TEXTE=''; ETUDE=null; EDITS={};
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

/* ---- le bon de commande (Igal, 4 oct. 2026 : « à partir du moment où il décide ce qu'il
   prend, préparer un document qui lui permette d'envoyer la commande au fournisseur ») ---- */
const dUS=d=>{ const m=String(d||'').match(/^(\d{4})-(\d{2})-(\d{2})/); return m?`${m[2]}/${m[3]}/${m[1]}`:String(d||''); };
function bcReg(){ const R=lit(K.reg,{})||{}; const F=Object.assign({raison:'',enseigne:'Perfumes Trade',adresse:'',tel:'',email:''},R.fact||{}); if(!F.raison) F.raison=R.societe||'DASY LLC'; return F; }
function bcLignes(){ const A=ETUDE; if(!A||A.err) return []; return A.L.filter(x=>x.q>0).map(x=>{ const v=x.cle?IDX[x.cle]:null;
  return {ref:x.ref||'',bc:x.bc||(v?v[0]:''),nom:v?((v[2]||'')+' '+(v[1]||'')+tyTexte(x.cle)).trim():(x.des||''),q:+x.q,p:x.p==null?null:+x.p,mt:(+x.q)*(x.p||0),
    offre:(x.edP&&x.p0!=null&&x.p!=null&&Math.abs(x.p-x.p0)>=0.005)?+x.p0:null}; }); }
const bcOffre=L=>L.some(l=>l.offre!=null);
function bcSortie(){
  const L=bcLignes(), frn=$('frn').value.trim()||'fournisseur', d=$('date').value||ajd();
  const F=bcReg(), tot=L.reduce((a,l)=>a+l.mt,0), q=L.reduce((a,l)=>a+l.q,0);
  return {titre:L3('Bon de commande — ','Purchase order — ','Orden de compra — ')+frn,
    fichier:'bon-de-commande-'+frn.replace(/\s+/g,'_')+'-'+ajd(),
    filtre:L3(`de ${F.raison} à ${frn} · price list du ${dUS(d)} · ${nf(q)} flacons · ${money(tot)}`,`from ${F.raison} to ${frn} · price list of ${dUS(d)} · ${nf(q)} bottles · ${money(tot)}`,`de ${F.raison} a ${frn} · lista de precios del ${dUS(d)} · ${nf(q)} frascos · ${money(tot)}`),
    colonnes:bcOffre(L)
      ?[{t:L3('Réf. fournisseur','Supplier ref.','Ref. proveedor')},{t:L3('Code-barres','Barcode','Código de barras')},{t:L3('Parfum','Perfume','Perfume')},{t:L3('Quantité','Quantity','Cantidad'),y:'n'},{t:L3('Votre prix (price list)','Your price (price list)','Su precio (lista)'),y:'m'},{t:L3('Notre offre','Our offer','Nuestra oferta'),y:'m'},{t:'Total',y:'m'}]
      :[{t:L3('Réf. fournisseur','Supplier ref.','Ref. proveedor')},{t:L3('Code-barres','Barcode','Código de barras')},{t:L3('Parfum','Perfume','Perfume')},{t:L3('Quantité','Quantity','Cantidad'),y:'n'},{t:L3('Prix unitaire','Unit price','Precio unitario'),y:'m'},{t:'Total',y:'m'}],
    lignes:bcOffre(L)?L.map(l=>[l.ref,l.bc,l.nom,l.q,l.offre!=null?l.offre:l.p,l.p,l.mt]):L.map(l=>[l.ref,l.bc,l.nom,l.q,l.p,l.mt])};
}
function bcTexte(){
  const L=bcLignes(), frn=$('frn').value.trim()||'', d=$('date').value||ajd(), F=bcReg();
  const tot=L.reduce((a,l)=>a+l.mt,0), q=L.reduce((a,l)=>a+l.q,0);
  const m2=v=>v==null?'—':Number(v).toFixed(2);
  const off=bcOffre(L);
  const li=L.map(l=>`• ${[l.ref,l.bc].filter(Boolean).join(' · ')}${l.ref||l.bc?' · ':''}${l.nom} — ${l.q} × $${m2(l.p)}${l.offre!=null?' '+L3(`(votre price list : $${m2(l.offre)})`,`(your list price: $${m2(l.offre)})`,`(su lista: $${m2(l.offre)})`):''} = $${m2(l.mt)}`).join('\n');
  const intro=off?L3(`Voici notre commande, d'après votre price list du ${dUS(d)}, avec les prix que nous vous proposons sur certaines lignes :`,`Please find our order, based on your price list of ${dUS(d)}, with the prices we propose on some lines:`,`Aquí está nuestro pedido, según su lista de precios del ${dUS(d)}, con los precios que proponemos en algunas líneas:`)
    :L3(`Voici notre commande, d'après votre price list du ${dUS(d)} :`,`Please find our order, based on your price list of ${dUS(d)}:`,`Aquí está nuestro pedido, según su lista de precios del ${dUS(d)}:`);
  const fin=off?L3('Merci de nous confirmer ces prix, la disponibilité et le délai.','Please confirm these prices, availability and lead time.','Por favor confirmen estos precios, la disponibilidad y el plazo.')
    :L3('Merci de confirmer la disponibilité et le délai.','Please confirm availability and lead time.','Por favor confirmen disponibilidad y plazo.');
  const sig=`${F.raison}${F.enseigne&&F.enseigne!==F.raison?' — '+F.enseigne:''}${F.adresse?'\n'+F.adresse:''}${F.tel?'\n'+F.tel:''}${F.email?'\n'+F.email:''}`;
  return `${L3('Bonjour','Hello','Hola')}${frn?' '+frn:''},\n\n${intro}\n\n${li}\n\nTotal${L3(' : ',': ',': ')}${nf(q)} ${L3('flacons','bottles','frascos')} — $${m2(tot)}\n\n${fin}\n\n${sig}`;
}
function bcOuvre(){
  const L=bcLignes(); if(!L.length){ alert(vf("Tape d'abord une quantité dans « Je commande » sur les parfums que tu veux.")); return; }
  const frn=$('frn').value.trim(), d=$('date').value||ajd(), F=bcReg();
  const tot=L.reduce((a,l)=>a+l.mt,0), q=L.reduce((a,l)=>a+l.q,0);
  $('bc-ent').innerHTML=`<div><b>De</b><span data-nolang>${esc(F.raison)}${F.enseigne&&F.enseigne!==F.raison?' — '+esc(F.enseigne):''}${F.adresse?'<br>'+esc(F.adresse):''}${F.tel?'<br>'+esc(F.tel):''}${F.email?'<br>'+esc(F.email):''}</span></div>
    <div><b>À</b><span data-nolang>${esc(frn||'—')}</span><br><b style="margin-top:8px">Price list du</b><span data-nolang>${dUS(d)}</span></div>`;
  if(!frn) $('bc-ent').insertAdjacentHTML('beforeend',`<p class="hint" style="grid-column:1/-1;color:var(--warn)">Le fournisseur n'est pas renseigné : écris son nom dans la case « Fournisseur » en haut de la page.</p>`);
  const off=bcOffre(L);
  $('bc-liste').innerHTML=`<table><thead><tr><th>Réf.</th><th>Parfum</th><th class="r">Qté</th>${off?'<th class="r">Sa price list</th><th class="r">Notre offre</th>':'<th class="r">Prix unit.</th>'}<th class="r">Total</th></tr></thead><tbody>${L.map(l=>`<tr><td data-nolang>${esc(l.ref||l.bc||'—')}</td><td data-nolang>${esc(l.nom)}${l.ref&&l.bc?'<br><small>'+esc(l.bc)+'</small>':''}</td><td class="r">${nf(l.q)}</td>${off?`<td class="r" data-nolang>${l.offre!=null?'<s>'+money2(l.offre)+'</s>':(l.p!=null?money2(l.p):'—')}</td><td class="r" data-nolang>${l.offre!=null?'<b class="off">'+money2(l.p)+'</b>':''}</td>`:`<td class="r">${l.p!=null?money2(l.p):'—'}</td>`}<td class="r"><b>${money2(l.mt)}</b></td></tr>`).join('')}</tbody></table>
    ${off?`<p class="hint" style="margin:8px 0 0;color:var(--iris)">Contre-offre : le document montre le prix de sa price list et le tien, et lui demande de confirmer.</p>`:''}
    <div class="bc-tot"><span>${nf(L.length)} parfum${L.length>1?'s':''} · ${nf(q)} flacon${q>1?'s':''}</span><span data-nolang>${money2(tot)}</span></div>`;
  $('bc-msg').textContent=''; $('bc-msg').className='msg';
  $('bcov').classList.add('on');
}
function bcJournal(comment){
  try{ const L=bcLignes(), frn=$('frn').value.trim()||'(fournisseur non précisé)', tot=L.reduce((a,l)=>a+l.mt,0);
    const J=lit(K.jou,[]); J.push({t:new Date().toISOString(),u:USR||'(non renseigné)',act:'fournisseur',lib:'bon de commande préparé — '+frn+' — '+nf(L.length)+' parfums, '+money(tot)+' ('+comment+')',ref:frn,av:null,ap:money(tot)}); ecrit(K.jou,J); }catch(e){}
}
$('bdc').onclick=bcOuvre;
$('bcx').onclick=()=>$('bcov').classList.remove('on');
$('bcov').addEventListener('click',e=>{ if(e.target===$('bcov')) $('bcov').classList.remove('on'); });
$('bc-pdf').onclick=()=>{ const S=bcSortie(); bcJournal('PDF'); sortieImprime(S); };
$('bc-xls').onclick=()=>{ const S=bcSortie(); bcJournal('Excel'); sortieXlsx(S); $('bc-msg').textContent=vf('fichier Excel téléchargé'); $('bc-msg').className='msg ok'; };
$('bc-txt').onclick=async()=>{ const t=bcTexte(); bcJournal('texte');
  try{ await navigator.clipboard.writeText(t); $('bc-msg').textContent=vf('texte copié — colle-le dans ton e-mail ou WhatsApp'); $('bc-msg').className='msg ok'; }
  catch(e){ const ta=document.createElement('textarea'); ta.value=t; ta.style.cssText='width:100%;min-height:200px;font:12.5px/1.5 ui-monospace,Menlo,monospace'; $('bc-liste').replaceWith(ta); ta.id='bc-liste'; ta.select(); $('bc-msg').textContent=vf('sélectionne et copie le texte ci-dessus'); } };
window.__bc={bcLignes,bcTexte,bcSortie};

/* ---- garder / relire ---- */
$('garde').onclick=()=>{
  const A=ETUDE; if(!A||A.err) return;
  if(frnManque()) return;
  const frn=$('frn').value.trim();
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
    ${L.map(e=>`<tr><td>${dfr(e.d)}</td><td><b data-frn="${esc(e.id)}">${esc(e.frn)}</b>${/^\(/.test(e.frn||'')?`<span class="rn" data-rn="${esc(e.id)}">${vf('nommer')}</span>`:''}</td><td>${esc(e.num||'—')}</td><td class="r">${nf(e.lignes.length)}</td><td class="r">${money(e.montant)}</td><td class="r ${e.eco>0?'g':e.eco<0?'c':''}">${e.eco?(e.eco>0?'−':'+')+money(Math.abs(e.eco)):'0 $'}</td><td class="r">${nf(e.nBon)}</td><td class="r">${nf(e.nCher)}</td><td>${esc(e.par||'')}</td><td class="r"><button class="btn sm" data-rl="${esc(e.id)}">Rouvrir</button> <button class="btn sm sup" data-sup="${esc(e.id)}" title="Supprimer définitivement cette étude">Supprimer</button></td></tr>`).join('')}</tbody></table>`;
  $('liste').querySelectorAll('[data-rl]').forEach(b=>b.onclick=()=>{ const e=ETU.find(x=>x.id===b.dataset.rl); if(!e) return;
    TEXTE=e.lignes.map(l=>`${l.bc}\t${l.ref}\t${l.q??''}\t${l.p??''}`).join('\n'); EDITS={}; $('colle').value=TEXTE; $('txt').classList.add('on');
    $('frn').value=e.frn; $('date').value=e.d; $('num').value=e.num||''; dessine(); window.scrollTo({top:0,behavior:'smooth'}); });
  /* une étude archivée sans fournisseur : on la nomme ici, sans la rouvrir ni la garder deux fois */
  $('liste').querySelectorAll('[data-rn]').forEach(b=>b.onclick=()=>{
    const e=ETU.find(x=>x.id===b.dataset.rn); if(!e) return;
    const td=b.parentNode, inp=document.createElement('input'); inp.className='rni'; inp.setAttribute('list','l-frn'); inp.placeholder=vf('Nom du fournisseur');
    td.innerHTML=''; td.appendChild(inp); inp.focus();
    let fait=false;
    const fini=()=>{ if(fait) return; fait=true; const v=inp.value.trim(); if(v){ const av=e.frn; e.frn=v; ecrit(K.etu,ETU);
        const J=lit(K.jou,[]); J.push({t:new Date().toISOString(),u:USR||'(non renseigné)',act:'fournisseur',lib:'étude de devis renommée — '+v+(e.num?' · '+e.num:''),ref:v,av,ap:v}); ecrit(K.jou,J); }
      dessineListe(); };
    inp.addEventListener('keydown',ev=>{ if(ev.key==='Enter') fini(); if(ev.key==='Escape'){ fait=true; dessineListe(); } });
    inp.addEventListener('blur',fini);
  });
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
window.__E={lit,qteEff,paEff,pvwEff,pvrEff,trouve,IDX,etude:()=>ETUDE,nouveauDevis,VENTES_CONNUES,refAlias,apprendRef,devineFrn,frnConnus,
  litBrouillon,oublieBrouillon,sauveBrouillon,charge,apprendNom,dessine,texte:()=>TEXTE};
dessineListe();
repriseBrouillon();
/* venu de la fiche d'un fournisseur : etude.html?frn=Donna pré-remplit son nom ;
   etude.html?etude=<id> rouvre une price list gardée */
try{ const u=new URLSearchParams(location.search);
  if(u.get('frn')&&!$('frn').value) $('frn').value=u.get('frn');
  if(u.get('etude')){ const b=$('liste').querySelector('[data-rl="'+CSS.escape(u.get('etude'))+'"]'); if(b) b.click(); }
  /* la price list déposée dans Fournisseurs arrive ici toute seule */
  if(u.get('doc')==='attente') setTimeout(()=>docAttentePrend().then(f=>{ if(f) charge(f); }),50);
}catch(e){}
$('sfoot').innerHTML=`${nf(Object.keys(HIST).length)} références avec historique d'achat`;
"""

JS = JS.replace('__LECTURE__', LECTURE).replace('__LIRE_PDF__', LIRE_PDF).replace('__NOMS__', _noms.NOMS)

html = coquille("Étude de devis", "Étude de devis",
  "Un devis de fournisseur, ligne par ligne, comparé à ce que Sam a déjà payé, à son stock et à ses ventes. "
  "L'outil dit ce qui vaut le coup, ce qui est plus cher que d'habitude, et ce qu'il est inutile de racheter.",
  CSS, CORPS.replace("__ACCEPT__", _lire.ACCEPT), JS, donnees=('produits',)).replace('__IDX__', 'Object.fromEntries(D_TOUS().map(r=>[r[15],[r[0],r[13],r[2],r[12],r[8],r[7],r[6],r[3],r[4],r[5]]]))')
# comme dans Factures : le script de page reste un module
_m = re.search(r'<script type="text/plain" id="page-js">\n(const VER_URL=[^\n]*\n)?const \$=i=>document\.getElementById\(i\);', html)
assert _m, "ancre du script de page introuvable"
html = (html[:_m.start()]
        + '<script type="text/plain" id="page-js" data-module="1">\n' + (_m.group(1) or '')
        + 'const $=i=>document.getElementById(i);'
        + html[_m.end():])
open('etude.html', 'w').write(html)
print('etude.html', len(html) // 1024, 'Ko')
