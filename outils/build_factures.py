# -*- coding: utf-8 -*-
"""Rubrique Factures : un PDF ou un texte collé -> le stock, les prix, les fournisseurs,
les clients et le journal se mettent à jour. Lecture du PDF entièrement locale (pdf.js embarqué)."""
import json
from build_crm import coquille
import _donnees
import _lire
import _noms
C=json.load(open('cat.json'))
IDX={r[15]:[r[0],r[13],r[2],r[12],r[6],r[8],r[7]] for r in C}   # cle -> bc,nom,marque,pa,qte,pvw,pvr
# pdf.js n'est plus embarqué (1,7 Mo qui ralentissaient chaque ouverture — Igal, 12 sept. 2026 :
# « les invoices mettent du temps à se charger ») : _lire le charge à la demande depuis lib/pdfjs/.

CSS = r'''
.tb input.ed{width:78px;padding:5px 7px;border:1px solid var(--line);border-radius:6px;font:inherit;font-size:13px;text-align:right;background:var(--surface)}
.tb input.ed:focus{border-color:var(--iris);outline:0}
.tb tr.corr td{background:var(--iris-soft)}
.tb td.moy,.tb td.moy b{font-size:16px}
/* RÉPARTITION d'une réception entre Perfumes Trade et Perfume City (Igal, 20 oct. 2026) */
.tb th.rep2,.tb td.rep{white-space:nowrap}.tb td.rep{text-align:right}
.tb td.rep label{display:inline-flex;flex-direction:column;align-items:flex-end;gap:2px;margin-left:8px;font-size:9.5px;letter-spacing:.06em;text-transform:uppercase;color:var(--ink-3);font-weight:600}
.tb td.rep input.rp{width:56px;padding:5px 6px;border:1px solid var(--line);border-radius:6px;font:inherit;font-size:13px;text-align:right;background:var(--surface);color:var(--ink)}
.tb td.rep input.rp:focus{border-color:var(--iris);outline:0}
.tb td.rep input.rp[data-rp="pc"]{border-color:#e8a7c8;background:#fdf1f7}
.repnote{margin:12px 0 0;padding:10px 12px;border-radius:8px;background:#fdf1f7;border-left:3px solid #e8a7c8;font-size:13px;line-height:1.45;color:var(--ink-2)}
.tb td.pfac{font-size:12px;font-weight:500;color:var(--ink-3)}.tb td.pfac input.ed{width:66px;font-size:12px;padding:4px 6px}
.tb .mex{display:block;margin-top:3px;font-size:11px;line-height:1.35;color:var(--ink-3);font-weight:400;white-space:normal;max-width:210px;margin-left:auto}.tb .mex b{color:var(--ink-2)}
.tb a.fiche{color:inherit;text-decoration:none;border-bottom:1px dotted var(--ink-3);cursor:pointer}.tb a.fiche:hover{color:var(--iris);border-bottom-color:var(--iris)}
.ft-ov{position:fixed;inset:0;z-index:70;background:rgba(23,23,29,.5);backdrop-filter:blur(2px);display:flex;align-items:center;justify-content:center;padding:18px;overflow:auto}
.ft{background:var(--surface);border-radius:14px;width:min(720px,100%);max-height:100%;overflow:auto;box-shadow:0 20px 60px rgba(0,0,0,.28);display:flex;flex-direction:column}
.ft-h{display:flex;justify-content:space-between;gap:12px;padding:18px 22px 12px;border-bottom:1px solid var(--line)}
.ft-h h2{margin:0 0 3px;font-size:19px}.ft-h p{margin:0;font-size:12.5px;color:var(--ink-3)}.ft-h p b{color:var(--ink-2);font-weight:600}
.ft-x{border:0;background:none;font-size:26px;line-height:1;color:var(--ink-3);cursor:pointer;align-self:flex-start}.ft-x:hover{color:var(--iris)}
.ft-b{display:grid;grid-template-columns:168px 1fr;gap:20px;padding:18px 22px 6px}
.ft-ph{display:flex;flex-direction:column;gap:8px;align-items:stretch}
.ft-img{aspect-ratio:1/1;border:1px dashed var(--line);border-radius:10px;background:var(--surface-2);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:6px;color:var(--ink-3);font-size:12px;overflow:hidden;padding:10px}
.ft-img svg{width:34px;height:54px}.ft-img img{width:100%;height:100%;object-fit:contain}
.ft-ph .btn{justify-content:center;font-size:12.5px;line-height:1.25}.ft-ph .lnk{font-size:11.5px}
.ft-g{display:grid;grid-template-columns:1fr 1fr;gap:12px 14px;align-content:start}
.ft-sec{grid-column:1/-1;margin-top:6px;padding-top:10px;border-top:1px solid var(--line);font-size:11px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:var(--ink-3)}
.ft-f2{display:flex;flex-direction:column;gap:4px;min-width:0}.ft-f2:nth-child(1),.ft-f2:nth-child(2){grid-column:1/-1}
.ft-f2 label{font-size:11.5px;font-weight:600;color:var(--ink-2)}.ft-f2 label b{color:var(--bad,#c0392b)}
.ft-f2 input,.ft-f2 select{padding:8px 10px;border:1px solid var(--line);border-radius:8px;font:inherit;font-size:14px;background:var(--surface);color:var(--ink);min-width:0}
.ft-f2 input:focus,.ft-f2 select:focus{border-color:var(--iris);outline:0;box-shadow:0 0 0 3px var(--iris-soft)}
.ft-f2 small{font-size:11px;color:var(--ink-3)}
.ft-ph [hidden]{display:none!important}
.ft-note{margin:6px 22px 0;font-size:12px;color:var(--ink-3)}
.ft-ft{display:flex;align-items:center;justify-content:flex-end;gap:9px;padding:14px 22px 18px}
.ft-msg{margin-right:auto;font-size:12.5px;color:var(--bad,#c0392b)}
@media(max-width:600px){.ft-b{grid-template-columns:1fr}.ft-ph{flex-direction:row;align-items:center}.ft-img{width:96px;flex:none}}
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
.ent2{margin-top:12px}
.choix{display:flex;flex-wrap:wrap;gap:6px 8px;align-items:center;font-size:12.5px}
.choix select,.choix input{font:inherit;font-size:12.5px;padding:5px 8px;border:1px solid var(--line);border-radius:7px;background:var(--surface);max-width:320px}
.choix input{min-width:200px}
td.ref .lu{display:block;font-size:11px;color:var(--ink-3);font-style:italic}
td.ref .chg{display:flex;flex-wrap:wrap;gap:4px 6px;align-items:center;margin-top:4px;font-size:11.5px;color:var(--warn)}
td.ref .chg select{font:inherit;font-size:11.5px;padding:3px 6px;border:1px solid var(--line);border-radius:6px;max-width:300px}
#w-taux[hidden],#a-dev[hidden]{display:none!important}
.fld .conv{display:block;margin-top:4px;font-size:11.5px;color:var(--ink-3)}
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

/* la liste des factures de vente */
.fl{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:16px 18px 12px;margin-bottom:18px}
#kpis[hidden],.fl[hidden],#sens[hidden]{display:none!important}
.fltb{display:flex;gap:9px;flex-wrap:wrap;align-items:center;margin-bottom:12px}
.fltb .sp{margin-left:auto}
.fltb #fnb{font-size:12.5px;color:var(--ink-3)}
.fltb .srch{position:relative;flex:1 1 220px;max-width:360px}
.fltb .srch input{width:100%;padding:9px 12px 9px 32px;font-family:inherit;font-size:14px;border:1px solid var(--line);border-radius:7px;background:var(--surface);color:var(--ink)}
.fltb .srch::before{content:"⌕";position:absolute;left:10px;top:50%;transform:translateY(-50%);color:var(--ink-3);font-size:16px}
.fltb .sel{padding:9px 11px;font-family:inherit;font-size:14px;border:1px solid var(--line);border-radius:7px;background:var(--surface);color:var(--ink);cursor:pointer}
.flt{width:100%;border-collapse:collapse;font-size:13.5px}
.flt th{text-align:left;font-size:9.5px;letter-spacing:.11em;text-transform:uppercase;color:var(--ink-2);font-weight:700;padding:8px 10px;border-bottom:2px solid var(--line);white-space:nowrap}
.flt td{padding:9px 10px;border-bottom:1px solid var(--line-2);vertical-align:middle}
.flt tr.cl{cursor:pointer}.flt tr.cl:hover td{background:var(--surface-2)}
.flt tr:last-child td{border-bottom:0}
.flt .r{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
.flt td.num b{font-family:Inter,sans-serif}
.flt td.cli{font-weight:600}
.flt .hh{font-family:Inter,sans-serif;font-variant-numeric:tabular-nums;color:var(--ink-2)}
.flt .tg{display:inline-block;font-family:Inter,sans-serif;font-size:10px;font-weight:800;letter-spacing:.06em;text-transform:uppercase;padding:2px 7px;border-radius:99px;background:var(--line-2);color:var(--ink-2)}
.flt .tg.ret{background:var(--crit-soft);color:var(--crit)}
.flt .ok{color:var(--good);font-weight:700}.flt .du{color:var(--crit);font-weight:700}
.flt a.btn,.flt button.btn{padding:5px 10px;font-size:12.5px;text-decoration:none;display:inline-block;margin-left:4px}
.flaide{margin:12px 0 0;font-size:12.5px;color:var(--ink-3);line-height:1.6}
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
<!-- Igal, 27 sept. 2026 : « vide-moi toute la rubrique Factures, ce n'est pas là que je
     mettrai les factures — laisse juste la partie où on insère les factures rentrantes ».
     Les factures de vente ne disparaissent pas : elles sont dans Ventes (fiche d'une vente →
     « Ouvrir la facture »). On garde les blocs dans la page, cachés, parce que le code
     s'appuie encore sur eux ; rien ne s'y affiche. -->
<div id="kpis" hidden></div>

<!-- Les factures de vente : une liste, toutes, la plus récente en premier. Personne
     ne les crée : chaque vente d'un canal (site, Amazon, caisse, boutique, gros) fait
     la sienne toute seule (voir _file_auto.py). Igal, 12 sept. 2026. -->
<section class="fl" hidden>
  <div class="fltb">
    <div class="srch"><input id="fq" autocomplete="off" placeholder="Chercher un client, un numéro, un montant…"></div>
    <select id="fcanal" class="sel"><option value="">Tous les canaux</option></select>
    <select id="fper" class="sel"><option value="0">Toute la période</option><option value="7">7 derniers jours</option><option value="30">30 derniers jours</option><option value="90">3 derniers mois</option><option value="365">12 derniers mois</option></select>
    <span class="sp"></span><span id="fnb"></span>
  </div>
  <div id="factures"></div>
  <p class="flaide">Une facture se fait toute seule à chaque vente, sur tous les canaux. « Voir » l'ouvre — impression, PDF, WhatsApp, e-mail, encaissement — et « Modifier » corrige le client, la date, le paiement, la taxe ou la note. Pour changer les lignes, on annule la facture et on enregistre la bonne.</p>
</section>

<h2 class="sec" id="depot">Déposer une facture fournisseur <em>réception de marchandise · le stock augmente</em></h2>
<section class="imp">
  <div class="sens" id="sens" hidden>
    <button data-s="achat" class="on a">Achat<small>réception de marchandise · le stock augmente</small></button>
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
  <!-- Igal, 27 sept. 2026 : certaines factures viennent de France, en euros, hors taxe.
       On les saisit telles quelles, en euros, avec le taux réellement payé ; les frais
       d'arrivée (transport, douane) s'ajoutent au coût des flacons. -->
  <div class="ent ent2">
    <div class="fld"><label>Devise de la facture</label><select id="dev"><option value="USD">Dollars ($)</option><option value="EUR">Euros (€)</option></select><small id="a-dev" hidden>€ repéré dans la facture</small></div>
    <div class="fld" id="w-taux" hidden><label>Taux payé : 1 € = … $</label><input id="taux" type="number" step="0.0001" min="0" inputmode="decimal" placeholder="1.0850"><small class="conv">celui du débit sur le relevé bancaire, frais de change compris</small></div>
    <div class="fld"><label>Frais d'arrivée ($)</label><input id="frais" type="number" step="0.01" min="0" inputmode="decimal" placeholder="0"><small class="conv">transport, douane… répartis sur les flacons selon leur prix</small></div>
  </div>

  <div class="opts">
    <label class="chk"><input type="checkbox" id="o-stock" checked>
      <span><b>Mettre le stock à jour</b> — <span id="o-stock-lib">ajouter les quantités reçues</span>.
      Décoche si cette marchandise est déjà comptée dans le stock actuel.</span></label>
    <label class="chk" id="w-prix"><input type="checkbox" id="o-prix" checked>
      <span><b>Recalculer le prix d'achat moyen</b> — il se lit sur la fiche du produit.</span></label>
  </div>

  <div id="apercu"></div>
  <datalist id="l-cat"></datalist>

  <div class="actions">
    <span class="msg" id="msg"></span><span class="spacer"></span>
    <button class="btn" id="raz">Vider</button>
    <button class="btn pri" id="ok" disabled>Enregistrer la facture</button>
  </div>
</section>

<h2 class="sec">Achats fournisseurs <em id="nbf"></em></h2>
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
/* Le type (EDT, EDP, OIL…) et le genre, comme sur les autres écrans. */
const TY=cle=>String(((IDX[cle]||[])[7])||'').trim();
const GEN={M:'Homme',W:'Femme',U:'Unisexe',K:'Enfant'};
const GN=cle=>GEN[String(((IDX[cle]||[])[8])||'').trim().toUpperCase()]||'';
const tyBadge=cle=>{ const t=TY(cle), g=GN(cle);
  return (t?' <i class="ty" data-nolang>'+esc(t)+'</i>':'')+(g?' <i class="gn">'+esc(g)+'</i>':''); };
function tyVu(l){
  if(!l||!l.cle) return '';
  const t=TY(l.cle); if(!t) return '';
  const dedans=new RegExp('(^|[^A-Za-z])'+t.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')+'([^A-Za-z]|$)','i').test(String(l.ref||''));
  return dedans ? tyBadge(l.cle).replace(/<i class="ty"[^>]*>[^<]*<\/i>/,'') : tyBadge(l.cle);
}
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
const parBC={}; Object.entries(IDX).forEach(([cle,v])=>{ if(v[0]) parBC[v[0]]=cle; });
/* les autres codes-barres déclarés sur une fiche (même parfum, autre lot ou coffret) */
function aliasBC(){ Object.entries(MOD).forEach(([cle,m])=>{ if(!m||!m.bcs||!IDX[cle]) return;
  String(m.bcs).split(/[^0-9]+/).filter(x=>x.length>=6).forEach(b=>{ if(!parBC[b]) parBC[b]=cle; }); });
  /* les cases collées du fichier (deux codes dans la même cellule) */
  Object.entries(bcExtra()).forEach(([cle,L])=>{ if(!IDX[cle]) return; L.forEach(b=>{ if(!parBC[b]) parBC[b]=cle; if(!parBC['0'+b]) parBC['0'+b]=cle; }); }); }
aliasBC();
function trouve(bc){
  bc=String(bc||''); if(!bc) return null;       /* une ligne sans code-barres ne « trouve » pas l'article ajouté sans code */
  const c=[bc,bc.replace(/^0+/,''),bc.padStart(12,'0'),bc.padStart(13,'0')];
  for(const x of c){ if(parBC[x]) return parBC[x]; }
  const nu=bc.replace(/^0+/,'');
  const k=Object.keys(parBC).find(b=>b.replace(/^0+/,'')===nu); return k?parBC[k]:null;
}

/* ---- retrouver un parfum sans code-barres (27 sept. 2026) ----
   Le moteur des noms est celui de l'Étude de cote. Pour une FACTURE, on ne prend seul que
   ce qui a déjà été confirmé une fois (le code article de CE fournisseur, ou ce nom exact) :
   le reste, Sam le choisit dans la ligne, et c'est retenu pour la facture suivante. */
const cleDeBC=b=>trouve(String(b||''));
__NOMS__
const K_ALIASR='alias-refs-v1';
const rNorm=v=>String(v==null?'':v).toUpperCase().replace(/[^A-Z0-9]/g,'');
const fNorm=v=>String(v==null?'':v).normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase().replace(/[^a-z0-9]/g,'');
const cleRef=(frn,ref)=>{ const r=rNorm(ref); return r?fNorm(frn)+'|'+r:''; };
function refAlias(ref,frn){ try{ const k=cleRef(frn,ref); if(!k) return ''; const A=lit(K_ALIASR,{})||{}; const c=A[k]; return (c&&IDX[c])?c:''; }catch(e){ return ''; } }
function apprendRef(ref,cle,frn){ try{ const k=cleRef(frn,ref); if(!k) return; const A=lit(K_ALIASR,{})||{}; if(cle) A[k]=cle; else delete A[k]; ecrit(K_ALIASR,A); }catch(e){} }
function apprendNom(des,cle){ try{ const k=mNorm(des); if(!k||!cle) return; const A=lit(K_ALIASN,{})||{}; A[k]=cle; ecrit(K_ALIASN,A); }catch(e){} }
const nomCat=cle=>{ const v=IDX[cle]||[]; return [v[2],v[1]].filter(Boolean).join(' '); };
let _OZ=null; const ozDe=cle=>{ if(!_OZ){ _OZ={}; try{ D_TOUS().forEach(r=>{ if(r&&r[15]) _OZ[r[15]]=String(r[3]||'').trim(); }); }catch(e){} } return _OZ[cle]||''; };

/* ---------------- lecture d'une facture ---------------- */
/* Excel écrit parfois un code-barres en notation scientifique : « 6.290171002345E12 »
   (price list UNITED Perfumes, 3 oct. 2026). Sans le remettre en chiffres, les 1 686 lignes
   se lisaient « par le nom » au lieu du code-barres. */
const sciBC=v=>{ const t=String(v==null?'':v).trim(); const m=t.match(/^(\d)(?:[.,](\d+))?e\+?(\d{1,2})$/i);
  if(!m) return t; const e=+m[3], f=m[2]||''; if(e<7||e>13||f.length>e) return t; return m[1]+f.padEnd(e,'0'); };
const normBC=v=>{ const d=sciBC(v).replace(/[^0-9]/g,''); return (d.length>=8&&d.length<=14)?d:''; };
/* La référence du fournisseur : son propre code article, celui qui revient d'une price list
   à l'autre alors que le libellé, lui, change. Ce n'est ni un code-barres, ni une quantité,
   ni un prix — et un mot sans chiffre n'en est pas une. Elle ne sert jamais à deviner : elle
   ne reconnaît une ligne que si Sam a corrigé cette référence-là une fois (voir build_etude). */
const normREF=v=>{ const s=String(v==null?'':v).trim();
  if(!/^[A-Za-z0-9][A-Za-z0-9._\/-]{2,23}$/.test(s)) return '';
  if(!/\d/.test(s)) return '';
  if(/^\d{1,3}([.,]\d{1,2})?$/.test(s)) return '';
  if(/[.,]\d{2}$/.test(s)) return '';
  if(/^\d{11,14}$/.test(s)) return '';
  return s; };
/* Une proforma de fournisseur a souvent DEUX parties : la commande (code, nom, quantité, prix, total) puis le
   COLISAGE — « Packing Slip », caisse par caisse : « Box #  Carton/Box ID  UPC  Description  Pcs on Box ».
   Les lignes du colisage portent le même code-barres que la commande, avec un nombre de pièces : lues comme
   une suite de la commande, elles ajoutaient des lignes en trop avec « 24 » pour prix (Igal, 17 oct. 2026,
   proforma Miami Trading Zone n° 91713 : 11 lignes de commande + 15 caisses lues en plus). La commande
   s'arrête donc au premier titre de colisage. S'il n'y a rien avant ce titre, on lit tout comme avant. */
const COLISAGE=/^.{0,40}(packing\s*(slip|list)|liste\s+de\s+colisage|bordereau\s+de\s+colisage|carton\s*\/?\s*box\s*id|pcs\s+on\s+box|pallet\s*\/\s*box\s*id)/im;
function litLignes(txt){
  const m=COLISAGE.exec(txt);
  if(m&&m.index>0){ const r=litLignesBrut(txt.slice(0,m.index)); if(r.length) return r; }
  return litLignesBrut(txt);
}
function litLignesBrut(txt){
  const out=[];
  /* Une facture française (SARL CVPF, 27 sept. 2026) coupe parfois une ligne en deux :
     « … RABANNE 1 MILLION GOLD EDP INTENSE  100 ML » puis « 0  12  48,26  579,12 ». Une
     ligne de nom sans aucun prix, suivie d'une ligne de chiffres seuls, n'en font qu'une. */
  const brut=txt.replace(/\r/g,'').split('\n'), LIGNES=[];
  for(let i=0;i<brut.length;i++){ let l=brut[i]; const n=brut[i+1];
    if(n!=null && /[A-Za-zÀ-ÿ]{3}/.test(l) && !/\d[.,]\d{2}\b/.test(l) && !/[A-Za-zÀ-ÿ]/.test(n) && /\d[.,]\d{2}\b/.test(n) && n.trim().split(/\s{2,}|\t/).length>=3){ l=l+'  '+n; i++; }
    LIGNES.push(l); }
  LIGNES.forEach(l=>{
    if(!l.trim()) return;
    l=l.replace(/\((\d{4,})\)/g,' ');
    const ch=l.split(/\t|;|\s{2,}|\|/).map(x=>x.trim()).filter(x=>x!=='');
    const plat=ch.length>=3?ch:l.trim().split(/\s+/);
    let bc='',iBc=-1;
    for(let i=0;i<plat.length;i++){
      /* « 0020729 / 7381759S » (n° de commande / code maison) n'est pas un code-barres :
         on ne recolle jamais des chiffres séparés par une barre, ni des morceaux mêlés de lettres */
      const t=String(plat[i]); if(/\d\s*\/\s*\d/.test(t) || (/[A-Za-z]/.test(t) && (t.match(/\d+/g)||[]).length>1)) continue;
      const b=normBC(t); if(b&&b.length>=11){ bc=b;iBc=i;break; } }
    /* Sans code-barres : un devis se lit par le nom. Une facture aussi, depuis le 27 sept.
       2026 (Igal : « ils reçoivent une facture soit avec le nom, soit avec le code-barres »),
       mais plus strictement : la ligne doit porter une quantité, un prix et un total qui
       se multiplient (48 × 25,00 = 1 200,00) — sinon une adresse ou un téléphone passerait
       pour un article. Et rien ne s'enregistre sur un nom deviné : c'est Sam qui confirme. */
    if(!bc && !(/[A-Za-zÀ-ÿ]{3}/.test(l) && /\d/.test(l))) return;
    const nums=[];
    plat.forEach((x,i)=>{ if(i===iBc) return;
      /* « RABANNE 1 MILLION GOLD » n'est pas le nombre 1 : un morceau fait de mots n'est pas un chiffre */
      if(/[A-Za-zÀ-ÿ]{3,}/.test(x) && !/^\s*(usd|eur|€|\$)?\s*[\d.,\s]+\s*(usd|eur|€|\$)?\s*$/i.test(x)) return;
      if(/^\d{6,}$/.test(x.replace(/[^0-9]/g,''))&&!/[.,]\d{2}$/.test(x)) return;
      const v=nombre(x); if(v!=null&&v>0) nums.push({v,i,dec:/[.,]\d{2}\b/.test(x)}); });
    if(!nums.length) return;
    let q=null,p=null;
    for(const a of nums){ if(!Number.isInteger(a.v)||a.v>5000) continue;
      for(const b of nums){ if(b.i===a.i||b.v<=0||b.v>4000) continue; const t=a.v*b.v;
        if(nums.some(c=>c.i!==a.i&&c.i!==b.i&&Math.abs(c.v-t)<=Math.max(0.6,t*0.004))){ q=a.v;p=b.v;break; } }
      if(p!=null) break; }
    if(p==null && !bc && DOC!=='devis') return;     /* facture, pas de code : quantité × prix = total exigé */
    if(p==null){ let c=nums.filter(x=>x.dec&&x.v>0.5&&x.v<4000);
      if(!c.length) c=nums.filter(x=>x.v>0.5&&x.v<4000&&!(Number.isInteger(x.v)&&x.v<=60&&x.i===0));
      if(!c.length) return; p=c[c.length-1].v;
      const e=nums.find(x=>Number.isInteger(x.v)&&x.v<=5000&&x.i<c[c.length-1].i&&x.v!==p&&x.i!==0); q=e?e.v:null; }
    const mots=plat.filter((x,i)=>i!==iBc&&/[A-Za-zÀ-ÿ]{3}/.test(x)); mots.sort((a,b)=>b.length-a.length);
    const refs=[]; for(let i=0;i<plat.length;i++){ if(i===iBc) continue; const r=normREF(plat[i]); if(r) refs.push(r); }
    /* la contenance posée à part (« 100 ML ») fait partie du nom : c'est elle qui sépare un 50 d'un 100 */
    let des=(mots[0]||'');
    const tl=plat.find(x=>/^\d+([.,]\d+)?\s*(ml|oz)\.?$/i.test(x)); if(tl&&!des.includes(tl)) des+=' '+tl;
    out.push({bc,refs,ref:refs[0]||'',des:des.slice(0,90),q,p});
  });
  /* la référence d'un article est propre à sa ligne : une valeur répétée sur toutes les
     lignes (le numéro de commande « 0020729 ») n'en est pas une */
  if(out.length>1){ const n={}; out.forEach(x=>(x.refs||[]).forEach(r=>{ n[r]=(n[r]||0)+1; }));
    out.forEach(x=>{ x.ref=(x.refs||[]).find(r=>n[r]===1)||''; }); }
  out.forEach(x=>{ delete x.refs; });
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
/* La colonne du code article du fournisseur. Elle porte souvent le même nom qu'une colonne
   de code-barres (« reference », « sku ») : c'est normal, on prend alors la même, et c'est
   la valeur qui tranche — 12 chiffres, c'est un code-barres ; PT-4419, une référence. */
const H_REF=['reference','référence','ref','sku','ugs','code article','code_article','code-article','item code','article','item','code'];
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
  let li=txt.replace(/\r/g,'').split('\n').filter(l=>l.trim()!=='');
  if(li.length<2) return null;
  /* L'en-tête n'est pas toujours la première ligne : une price list commence souvent par le
     nom du fournisseur et un titre (« UNITEDPerfumes », « EXPORT PRICE LIST Sep 28, 2026 »,
     3 oct. 2026). On prend la première des 12 premières lignes qui ressemble à un en-tête :
     au moins un prix, et un code-barres ou une désignation. */
  { const est=l=>{ const sp=[';','\t',','].map(c=>({c,n:l.split(c).length})).sort((a,b)=>b.n-a.n)[0]; if(sp.n<3) return false;
      const h=l.split(sp.c).map(x=>x.trim().replace(/^"|"$/g,'').toLowerCase());
      const a=L=>L.some(m=>h.some(x=>x===m)); return a(H_P)&&(a(H_BC)||a(H_D)||a(H_Q)); };
    const k=li.slice(0,12).findIndex(est); if(k>0) li=li.slice(k); }
  const sep=[';','\t',','].map(c=>({c,n:li[0].split(c).length})).sort((a,b)=>b.n-a.n)[0];
  if(sep.n<3) return null;
  const dec=l=>l.split(sep.c).map(x=>x.trim().replace(/^"|"$/g,'').replace(/""/g,'"'));
  const head=dec(li[0]).map(h=>h.toLowerCase().replace(/^\ufeff/,'').trim());
  const cherche=(L)=>{ for(const m of L){ const i=head.findIndex(h=>h===m); if(i>=0) return i; }
                       for(const m of L){ const i=head.findIndex(h=>h.includes(m)); if(i>=0) return i; } return -1; };
  let iB=cherche(H_BC), iQ=cherche(H_Q), iP=cherche(H_P), iD=cherche(H_D), iT=cherche(H_T), iR=cherche(H_REF);
  /* 21 oct. 2026 (Sam : « le fichier portait bien les noms Price et Quantity, et l'ERP les a intervertis ») : sa feuille Google n'a de titre
     QUE sur « Price » et « Qty » — les colonnes du code-barres et du nom n'en ont pas. Sans colonne code-barres nommée, ce lecteur renonçait,
     et la lecture « en vrac » (quantité d'abord, prix ensuite) prenait le prix pour la quantité. Quand « Price » et « Qty » sont NOMMÉS,
     on retrouve le code-barres (la colonne de nombres à 8-14 chiffres) et le nom (la colonne de texte) d'après le CONTENU, et on garde
     les titres : le prix reste le prix, la quantité reste la quantité. */
  if(iB<0&&iQ>=0&&iP>=0){
    const R=li.slice(1).map(dec).filter(c=>c.some(x=>x)), n=head.length;
    const ch=j=>R.map(c=>String(c[j]||'').trim()).filter(Boolean);
    let meilleur=-1, nb=0;
    for(let j=0;j<n;j++){ if(j===iQ||j===iP) continue; const v=ch(j), k=v.filter(x=>/^\d{8,14}$/.test(x.replace(/[\s'-]/g,''))).length;
      if(k>nb&&k>=Math.max(1,Math.ceil(R.length/2))){ nb=k; meilleur=j; } }
    if(meilleur>=0){ iB=meilleur;
      if(iD<0){ let md=-1, nd=0; for(let j=0;j<n;j++){ if(j===iB||j===iQ||j===iP) continue; const k=ch(j).filter(x=>/[A-Za-zÀ-ÿ]{3,}/.test(x)).length;
        if(k>nd&&k>=Math.max(1,Math.ceil(R.length/2))){ nd=k; md=j; } }
        if(md>=0) iD=md; } } }
  /* « Stock » sur une price list : ce que le fournisseur a de disponible — ni une quantité
     commandée, ni un prix (elle était lue comme le prix : 3 352 $ pour un 9PM Elixir) */
  const iS=head.findIndex(h=>/^(stock|available|availability|disponible|dispo|existencia|inventario|on hand|qty available)$/.test(h));
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
  /* Une colonne « reference » peut porter des codes-barres ou des codes maison : on ne
     l'annonce pour ce qu'elle est qu'une fois les lignes lues. */
  const colDesc=(bcLu)=>[[bcLu?'code-barres':'référence',iB],['référence',(iR>=0&&iR!==iB)?iR:-1],
                         ['quantité',iQ],['prix',iP],['désignation',iD],['total',iT]]
    .filter(x=>x[1]>=0).map(x=>x[0]+' → '+(dec(li[0])[x[1]]?'« '+dec(li[0])[x[1]]+' »':'colonne '+String.fromCharCode(65+x[1])+' (sans titre)')).join(', ');
  const colonnes=colDesc(true);
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
    /* Une colonne « reference » qui ne contient pas de code-barres n'est pas une erreur de
       fichier : c'est le code article du fournisseur. Sur un devis, la ligne se lit quand
       même — par le nom, ou par cette référence si elle a déjà été corrigée une fois. */
    const ref=normREF(iR>=0?c[iR]:(bc?'':(iB>=0?c[iB]:'')));
    if(!bc && !((parNom||DOC==='devis') && (des.trim()||ref))) continue;
    const q=iQ>=0?nombre(c[iQ]):null, p=nombre(c[iP]);
    if(q==null&&p==null) continue;
    const o={bc,ref,des,q:q==null?null:q,p:p==null?null:p,mt:iT>=0?nombre(c[iT]):null};
    if(iS>=0&&iS!==iQ&&iS!==iP){ const d=nombre(c[iS]); if(d!=null) o.dispo=d; }
    out.push(o);
  }
  if(!out.length) return {err:parNom
    ? `Colonnes reconnues (${colonnes}), mais aucune ligne exploitable : il faut au moins un nom et un prix par ligne.`
    : `Colonnes reconnues (${colonnes}), mais aucune ligne exploitable : vérifie que la colonne code-barres contient bien des codes.`};
  return {lignes:out,colonnes:colDesc(out.some(x=>x.bc)),entete:true};
}

/* en-tete : numero, date, tiers — devines, toujours modifiables */
function litEntete(txt){
  const o={};
  /* un en-tête en tableau (« Date  Invoice # ») dont les valeurs sont sur une ligne
     suivante (« 9/24/2026  250985 ») : on prend la valeur de la même colonne */
  { const L=txt.split('\n');
    for(let i=0;i<L.length&&!o.num;i++){
      const h=L[i].split(/\s{2,}|\t/).map(x=>x.trim()); const k=h.findIndex(x=>/^(invoice|facture|inv)\s*(#|no\.?|n[°º]|number|num[ée]ro)$/i.test(x));
      if(k<0) continue;
      for(let j=i+1;j<Math.min(L.length,i+4);j++){ const v=L[j].split(/\s{2,}|\t/).map(x=>x.trim());
        if(v.length===h.length&&/^[A-Z0-9][A-Z0-9-\/]{2,}$/i.test(v[k])&&/\d{3,}/.test(v[k])){ o.num=v[k]; break; } } } }
  let m=txt.match(/\b([A-Z]{2,8}INV[A-Z0-9-]*\d{3,})\b/);
  if(!m){ const re=/(?:Invoice|Facture|Document\s+Number|N[°º]|No\.?)\s*[:#]?\s*([A-Z]{0,6}[-\/]?\d{4,}[A-Z0-9-]*)/ig; let x;
    /* « Client N° 6275199 », « N° TVA », « Tel » : ce n'est pas le numéro de la facture */
    while((x=re.exec(txt))){ const avant=txt.slice(Math.max(0,x.index-12),x.index); if(/client|customer|tva|vat|siret|t[ée]l|compte|account/i.test(avant)) continue; m=x; break; } }
  if(m&&!o.num) o.num=m[1];
  m=txt.match(/\b(\d{1,2})\/(\d{1,2})\/(\d{4})\b/);
  if(m){ let a=+m[1],b=+m[2]; const y=m[3];
    const mois = a>12 ? b : a, jour = a>12 ? a : b;        /* américain par défaut, sauf si impossible */
    o.date=`${y}-${String(mois).padStart(2,'0')}-${String(jour).padStart(2,'0')}`; }
  else { m=txt.match(/\b(\d{4})-(\d{2})-(\d{2})\b/); if(m) o.date=m[0]; }
  if(!o.date){ m=txt.match(/\b(\d{1,2})\/(\d{1,2})\/(\d{2})\b/);
    /* 01/09/26 : une facture en français met le jour d'abord */
    if(m){ let a=+m[1],b=+m[2]; const fr=/facture|tva|libell|montant|net à payer/i.test(txt);
      const jour = (fr||a>12) ? a : b, mois = (fr||a>12) ? b : a;
      if(mois>=1&&mois<=12&&jour>=1&&jour<=31) o.date=`20${m[3]}-${String(mois).padStart(2,'0')}-${String(jour).padStart(2,'0')}`; } }
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
let REP={};
let SWAP=false, INV_OK=false, AUTO_SWAP=0, TEXTE_VU=null;   /* garde « prix et quantités inversés » (20 oct. 2026) */   /* la part de chaque ligne donnée à Perfume City : index de ligne → flacons */
/* l'index des produits se refait quand un article est créé depuis l'aperçu */
function refaitIndex(){ const N=Object.fromEntries(D_TOUS().map(r=>[r[15],[r[0],r[13],r[2],r[12],r[6],r[8],r[7]]]));
  Object.keys(IDX).forEach(k=>delete IDX[k]); Object.assign(IDX,N);
  Object.keys(parBC).forEach(k=>delete parBC[k]); Object.entries(IDX).forEach(([cle,v])=>{ if(v[0]) parBC[v[0]]=cle; }); aliasBC(); M_CAT=null; _OZ=null; CAT_OK=false; }
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
$('sens').addEventListener('click',e=>{ const b=e.target.closest('[data-s]'); if(!b) return; SENS='achat'; majSens(); });
/* on arrive depuis « Enregistrer un achat » ou depuis une fiche fournisseur : sens et nom déjà posés */
{ const U=new URLSearchParams(location.search); const sn=U.get('sens'), fr=U.get('frn');
  /* la page ne reçoit plus que des factures fournisseurs, quoi que dise l'adresse */
  SENS='achat';
  if(fr){ setTimeout(()=>{ $('tiers').value=fr; },0); }
  if(sn||fr) setTimeout(()=>{ majSens(); if(fr) $('tiers').value=fr; document.getElementById('dz').scrollIntoView({block:'center'}); },0);
  /* le document déposé dans Fournisseurs arrive ici tout seul */
  if(U.get('doc')==='attente') setTimeout(()=>docAttentePrend().then(f=>{ if(f) charge(f); }),50); }
/* le tableau de bord ouvre ici la facture dont le stock n'est pas parti sur Shopify (21 oct. 2026) */
{ const oid=new URLSearchParams(location.search).get('ouvre'); if(oid) setTimeout(()=>{ try{ if(FACT.some(x=>x.id===oid)) detail(oid); }catch(e){} },400); }
$('canal-nom').addEventListener('change',()=>{ $('tiers').value=$('canal-nom').value; majSens(); dessineApercu(); });
$('tiers').addEventListener('change',dessineApercu);
let DEV_CHOISIE=false;
function majDevise(){ $('w-taux').hidden=$('dev').value!=='EUR'; }
$('dev').addEventListener('change',()=>{ DEV_CHOISIE=true; $('a-dev').hidden=true; majDevise(); dessineApercu(); });
['taux','frais'].forEach(id=>$(id).addEventListener('change',dessineApercu));

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
  const pdf=await (await _pdfjs()).getDocument({data:buf}).promise; const out=[];
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
    if(TEXTE!==TEXTE_VU){ TEXTE_VU=TEXTE; SWAP=false; INV_OK=false; AUTO_SWAP=0; }   /* un nouveau fichier repart de zéro */
    L=L.map((x,i)=>{ x._i=i; if(SWAP&&SENS==='achat'){ const a=x.q; x.q=x.p==null?null:x.p; x.p=a==null?null:a; } if(REP[i]!=null) x.pcVoulu=REP[i]; const e=EDITS[i]; if(!e) return x; if(e.sup) return null;
      if(e.q!=null) x.q=e.q; if(e.p!=null) x.p=e.p; return x; }).filter(Boolean);
    if(!L.length) return {err:"Toutes les lignes ont été retirées."};
  }
  const stock=$('o-stock').checked, majPrix=SENS==='achat'&&$('o-prix').checked;
  /* 20 oct. 2026 (Igal : « quand Sam rentre une new order … il doit pouvoir dispatcher le stock sur la boutique Perfume City ») :
     sur une réception qui met le stock à jour, chaque ligne peut en donner une part à Perfume City (qui a son propre stock,
     et sa boutique Shopify). Réservé à ceux qui peuvent modifier les prix, comme l'envoi à Shopify. */
  const pcOK=SENS==='achat'&&stock&&(typeof peut!=='function'||peut('modPrix'));
  /* la devise : une facture française porte des « € » — on le repère, on ne devine pas le taux */
  if(SENS==='achat'&&!DEV_CHOISIE&&$('dev').value==='USD'&&/€|\bEUR\b|\beuros?\b/i.test(TEXTE)){ $('dev').value='EUR'; $('a-dev').hidden=false; majDevise(); }
  const DEV=SENS==='achat'?$('dev').value:'USD';
  let TX=DEV==='EUR'?(+String($('taux').value).replace(',','.')||0):1;
  const FR=SENS==='achat'?Math.max(0,+String($('frais').value).replace(',','.')||0):0;
  /* sans taux, on montre quand même ce qui a été lu : c'est l'enregistrement qui attend */
  const tauxManque = DEV==='EUR' && !(TX>0);
  if(DEV==='EUR'&&TX>0&&(TX<0.5||TX>2)) return {err:"Le taux "+TX+" ne ressemble pas à un taux euro → dollar (autour de 1,1). Vérifie la case."};
  if(SENS==='canal'){
    const agg={};
    L.forEach(x=>{ const k=x.bc; if(!agg[k]) agg[k]={bc:x.bc,des:x.des,q:0,p:x.p,mt:0,cmds:[]};
      agg[k].q+=x.q; agg[k].mt+=(x.p||0)*x.q; if(x.p!=null) agg[k].p=x.p; agg[k].cmds.push(x); });
    /* une reference vendue puis rendue en entier s'annule : on ne l'affiche pas */
    L=Object.values(agg).map(a=>{ a.p = a.q? a.mt/a.q : (a.p||0); return a; }).filter(a=>a.q!==0);
  }
  let connues=0,inconnues=0,montant=0,ecart=0,unites=0,neg=0,pcU=0;
  /* le coût d'un flacon, en dollars : le prix de la facture converti, plus sa part des
     frais d'arrivée (au prorata de la valeur de la ligne, sur les lignes enregistrées) */
  const r2=v=>Math.round(v*100)/100;
  if(tauxManque) TX=1;
  const valUsd=L.reduce((a,x)=>a+(trouve(x.bc)?(x.q||0)*(x.p||0)*TX:0),0);
  const kFr=(SENS==='achat'&&valUsd>0)?FR/valUsd:0;
  L.forEach(x=>{ x.pUsd=r2((x.p||0)*TX); x.cout=r2((x.p||0)*TX*(1+kFr)); });
  const FRN_NOM=$('tiers').value.trim();
  /* UN MÊME PARFUM SUR DEUX LIGNES (Igal, 21 oct. 2026, facture MPSINV82395 : Gold Digger en 48 puis en 1 — stock enregistré 23 au lieu de 71).
     Chaque ligne repartait du stock d'AVANT la facture : la dernière écrasait les autres et 48 flacons disparaissaient, sur l'ERP puis sur les
     deux sites. Le stock et le prix d'achat moyen se cumulent maintenant d'une ligne à l'autre : la 2e ligne part de ce que la 1re a laissé. */
  const RUN_Q={}, RUN_PA={};
  L.forEach(x=>{
    x.cle=trouve(x.bc); montant+=(x.q||0)*(x.p||0);
    if(!x.cle && SENS==='achat' && !x.bc){
      const a=refAlias(x.ref,FRN_NOM); if(a){ x.cle=a; x.par='ref'; }
      else if(x.des){ const r=mCherche(x.des);
        if(r.appris&&r.cands[0]){ x.cle=r.cands[0].cle; x.par='nom'; }
        else {
          x.cands=r.cands.slice(0,6);
          /* la référence est parfois la fin du code-barres (Hanae Mori : « 02354 » = 3526790002354) */
          const rb=/^\d{4,7}$/.test(x.ref||'') ? r.cands.find(c=>String((IDX[c.cle]||[])[0]||'').endsWith(x.ref)) : null;
          const b0=r.cands[0], b1=r.cands[1];
          if(rb){ x.cle=rb.cle; x.par='devine'; }
          /* un nom sans ambiguïté est pris, mais la ligne le montre et se change d'un clic */
          else if(b0 && b0.sc>=0.72 && (!b1 || b0.sc-b1.sc>=0.13)){ x.cle=b0.cle; x.par='devine'; }
        } }
    }
    if(!x.cle){ inconnues++; return; }
    connues++; unites+=(x.q||0);
    x.qAv=(x.cle in RUN_Q)?RUN_Q[x.cle]:qteEff(x.cle);
    /* la part donnée à Perfume City ne dépasse jamais ce qui est reçu ; le reste entre au stock de Perfumes Trade */
    x.pc=pcOK?Math.max(0,Math.min(x.q||0,Math.round(+x.pcVoulu||0))):0; pcU+=x.pc;
    const d=SENS==='achat'?(x.q||0)-x.pc:-(x.q||0);
    x.qAp=stock?Math.max(0,x.qAv+d):x.qAv;
    RUN_Q[x.cle]=x.qAp;
    if(stock&&SENS!=='achat'&&x.qAv+d<0){ x.manque=-(x.qAv+d); neg++; }
    x.paAv=(x.cle in RUN_PA)?RUN_PA[x.cle]:paEff(x.cle);
    if(SENS==='achat'){
      /* Le prix d'achat de référence est la MOYENNE des achats, pondérée par les quantités
         (décision d'Igal) : le stock déjà là compte à son prix, les flacons reçus au leur.
         10 en stock à 30 $ + 20 reçus à 36 $ → 34 $, pas 36 $ ni 33 $. Avant, la facture
         écrasait le prix avec le dernier payé. */
      const deja = stock ? Math.max(0,x.qAv) : Math.max(0,x.qAv-(x.q||0));
      /* le prix moyen est celui du stock de Perfumes Trade : seuls les flacons qui y entrent comptent (pas la part de Perfume City) */
      const qC=(x.q||0)-(x.pc||0);
      x.paNv = qC<=0 ? (x.paAv!=null?x.paAv:x.cout) : ((x.paAv!=null&&deja>0) ? r2((deja*x.paAv+qC*x.cout)/(deja+qC)) : x.cout);
      x.deja=deja;
      if(x.paAv!=null){ x.dp=r2(x.paNv-x.paAv); ecart+=(x.cout-x.paAv)*(x.q||0); }
    }
    RUN_PA[x.cle]=(SENS==='achat'&&majPrix&&x.paNv!=null)?x.paNv:x.paAv;
  });
  /* LA GARDE (Igal, 20 oct. 2026 : « l'ERP a interverti le prix avec les quantités, alors que la colonne portait bien le nom de price et
     quantity ; il ne faut plus que ça arrive »). Quel que soit le nom des colonnes, on compare à ce que l'ERP sait déjà : si les
     « quantités » lues ressemblent aux prix connus des fiches (Sauvage Elixir : « quantité » 180 = son prix d'achat) et les « prix »
     à des quantités, la lecture est probablement inversée — l'enregistrement est bloqué tant qu'on n'a pas tranché. Une « quantité »
     avec des décimales est suspecte aussi (on ne reçoit pas 17,5 flacons). */
  let inversion=null;
  if(SENS==='achat'){
    let inv=0, bon=0, frac=0;
    L.forEach(x=>{ if(!x.cle) return;
      if(x.q!=null&&Math.abs(x.q-Math.round(x.q))>1e-9) frac++;
      if(!(x.paAv>0)||!(x.q>0)||!(x.p>0)) return;
      const proche=a=>Math.abs(a-x.paAv)/x.paAv<=0.25;
      if(proche(x.p)) bon++; else if(proche(x.q)&&x.q!==x.p) inv++; });
    if((inv>=2&&inv>bon)||frac>0) inversion={inv,bon,frac};
    /* 21 oct. 2026 (Igal : « toujours le même problème, il inverse quantity et price, c'est fatigant ») : quand la preuve est NETTE — au moins
       deux parfums dont la « quantité » est le prix connu de la fiche, et deux fois plus que de parfums dont le prix est le bon —, l'ERP
       inverse TOUT SEUL, une seule fois, et le DIT (bandeau + « Annuler l'inversion »). Il ne bloque plus l'enregistrement pour ça.
       Le cas courant : une feuille copiée SANS sa ligne de titres (« Price | Qty ») est lue « quantité puis prix ». Une preuve plus
       faible, ou des quantités à décimales, bloquent toujours et demandent de trancher. Annuler = on garde la lecture telle quelle. */
    if(inversion&&!SWAP&&!INV_OK&&inv>=2&&inv>=2*bon){ SWAP=true; AUTO_SWAP=inv; return analyse(); }
  }
  const num=$('num').value.trim();
  const doublon=num&&FACT.some(f=>f.num.toLowerCase()===num.toLowerCase());
  const montantUsd=r2(montant*TX);
  return {L,connues,inconnues,montant,montantUsd,dev:DEV,taux:TX,frais:FR,tauxManque,ecart,unites,pcU,pcOK,neg,stock,majPrix,doublon,X,inversion};
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
/* Quitter une case redessinait tout l'aperçu : si on passait à la case voisine, elle était recréée sous la souris et la frappe
   se perdait. Désormais on ne redessine que si le focus ne passe pas à une autre case du tableau — et, pendant qu'on tape les
   parts de Perfume City, l'aperçu se met à jour tout seul en gardant la case active (Igal, 20 oct. 2026). */
let T_REP=null;
function apresChamp(){ setTimeout(()=>{ const a=document.activeElement; if(a&&a.matches&&a.matches('input.rp,input.ed')) return; dessineApercu(); },0); }
function redessineGardantLeChamp(){
  const a=document.activeElement; let sel=null, pos=null;
  if(a&&a.matches&&a.matches('input.rp,input.ed')){ sel=a.classList.contains('rp')?`input.rp[data-rp="${a.dataset.rp}"][data-i="${a.dataset.i}"]`:`input.ed[data-e="${a.dataset.e}"][data-i="${a.dataset.i}"]`; try{ pos=[a.selectionStart,a.selectionEnd]; }catch(e){} }
  dessineApercu();
  if(sel){ const n=$('apercu').querySelector(sel); if(n){ n.focus(); try{ if(pos&&pos[0]!=null) n.setSelectionRange(pos[0],pos[1]); }catch(e){} } }
}
function dessineApercu(){
  const A=analyse(); APERCU=A; const box=$('apercu'); $('ok').disabled=true;
  if(!A){ box.innerHTML=''; return; }
  if(A.err){ box.innerHTML=`<div class="av" style="white-space:pre-line">${esc(A.err)}</div>`; return; }
  const s=SENS==='achat';
  const rep=s&&A.pcOK;   /* colonne « Répartition » : seulement quand la réception met le stock à jour */
  const edit=(SENS!=='canal');
  const repCell=x=>`<td class="rep"><label>Perfumes Trade<input class="rp" type="number" min="0" max="${x.q||0}" step="1" data-rp="pt" data-i="${x._i}" value="${(x.q||0)-(x.pc||0)}" aria-label="${L3('Flacons pour Perfumes Trade','Bottles for Perfumes Trade','Frascos para Perfumes Trade')}"></label><label>Perfume City<input class="rp" type="number" min="0" max="${x.q||0}" step="1" data-rp="pc" data-i="${x._i}" value="${x.pc||0}" aria-label="${L3('Flacons pour Perfume City','Bottles for Perfume City','Frascos para Perfume City')}"></label></td>`;
  const cell=(x,k)=>edit?`<input class="ed" type="number" step="${k==='q'?'1':'0.01'}" min="0" data-e="${k}" data-i="${x._i}" value="${x[k]==null?'':x[k]}">`:(k==='q'?(x.q??'—'):money2(x.p));
  const sup=x=>edit?`<button class="lnk sup" data-sup="${x._i}" title="Retirer cette ligne de la facture">✕</button>`:'';
  const li=A.L.map(x=>{
    if(!x.cle && s && !x.bc) return `<tr class="inc"><td class="ref"><b data-nolang>${esc(x.des||'—')}</b><span data-nolang>${x.ref?'réf. '+esc(x.ref):'sans code-barres'}</span></td>
      <td class="r">${cell(x,'q')}</td>${rep?'<td></td>':''}<td colspan="2"><div class="choix"><b>C'est lequel ?</b>
        <select data-choix="${x._i}"><option value="">— choisir le parfum —</option>${(x.cands||[]).map(c=>`<option value="${esc(c.cle)}">${esc(nomCat(c.cle))}${ozDe(c.cle)?' · '+esc(ozDe(c.cle))+' oz':''}</option>`).join('')}</select>
        <input data-cherche="${x._i}" list="l-cat" placeholder="ou tape son nom…" autocomplete="off">
        <span>ou <button class="lnk" data-cree="${x._i}">créer l'article</button> · <button class="lnk" data-sup="${x._i}">retirer la ligne</button></span></div></td><td class="r pfac">${cell(x,'p')}</td></tr>`;
    if(!x.cle) return `<tr class="inc"><td class="ref"><b>${esc(x.des||'—')}</b><span>${x.bc}</span></td>
      <td class="r">${cell(x,'q')}</td>${rep?'<td></td>':''}${s?'':`<td class="r">${cell(x,'p')}</td>`}<td colspan="2">code-barres absent du catalogue — ${s?`<button class="lnk" data-cree="${x._i}">créer l'article</button> ou `:''}<button class="lnk" data-sup="${x._i}">retirer la ligne</button></td>${s?`<td class="r pfac">${cell(x,'p')}</td>`:''}</tr>`;
    const v=IDX[x.cle];
    const mv = A.stock ? `<span class="mv">${nf(x.qAv)} → <b class="${s?'plus':'moins'}">${nf(x.qAp)}</b>${x.manque?` <b class="moins">· ${x.manque} manquant${x.manque>1?'s':''}</b>`:''}</span>` : `<span class="mv" style="color:var(--ink-3)">inchangé (${nf(x.qAv)})</span>`;
    /* 18 oct. 2026 (Igal : « ce qui m'intéresse, c'est à combien on les a payés la dernière fois ; le prix moyen sera calculé sur la
       fiche du produit ») : sur la facture, le DERNIER PRIX PAYÉ (et sa date), comparé au prix de cette facture. Le prix moyen est
       toujours recalculé (case cochée plus haut), il se lit dans la fiche. */
    const dern = (()=>{ let b=null; try{ (HIST[x.cle]||[]).forEach(h=>{ if(!h||!(h.p>0)) return; if(!b||String(h.d||'')>=b.d) b={d:String(h.d||''),p:+h.p}; }); }catch(e){} return b; })();
    /* 20 oct. 2026 (Igal : « pourquoi tous les produits sont pas sortis ? Il y a de l'historique » — tout affichait « premier achat ») :
       un parfum déjà en stock et déjà vendu n'a pas forcément de facture d'achat enregistrée ici (son stock vient de l'inventaire de départ).
       Sans historique, on montre le prix d'achat connu de la fiche, marqué comme tel ; « premier achat » seulement s'il n'y a rien du tout. */
    const dernOuFiche = dern || ((x.paAv!=null && x.paAv>0) ? {d:'',p:+x.paAv,fiche:true} : null);
    const pr = s ? (dernOuFiche ? `<b>${money2(dernOuFiche.p)}</b>${dernOuFiche.fiche?`<small class="mex" style="display:block;text-align:right">${L3('prix de la fiche','price on the product sheet','precio de la ficha')}</small>`:dernOuFiche.d?`<small class="mex" style="display:block;text-align:right">${(d=>{ const [a,m,j]=String(d).slice(0,10).split('-'); return m&&j?m+'/'+j+'/'+String(a).slice(2):d; })(dernOuFiche.d)}</small>`:''}${(!A.tauxManque&&x.cout>0&&Math.abs(x.cout-dernOuFiche.p)>=0.005)?`<small class="mex" style="display:block;text-align:right;color:${x.cout<dernOuFiche.p?'var(--good)':'var(--crit)'}">${x.cout<dernOuFiche.p?L3('moins cher de','cheaper by','más barato de'):L3('plus cher de','more expensive by','más caro de')} ${money2(Math.abs(x.cout-dernOuFiche.p))}</small>`:''}${(!A.tauxManque&&x.cout>0&&(x.cout>=dernOuFiche.p*2||x.cout<=dernOuFiche.p/2))?`<small class="mex" style="display:block;text-align:right;color:var(--crit);font-weight:700">⚠ ${L3('écart énorme : vérifie','huge gap: check','diferencia enorme: revisa')}</small>`:''}` : `<span style="color:var(--ink-3)">${L3('premier achat','first purchase','primera compra')}</span>`) : `<span style="color:var(--ink-3)">achat ${x.paAv==null?'—':money2(x.paAv)}</span>`;
    /* Igal, 17 oct. 2026 (« 22,50 $ → 20,37 $ ✕ … j'aimerais que cela soit expliqué ») : sous la flèche, le calcul en clair */
    const expl='';
    /* sous le prix de la facture : ce que le flacon coûte vraiment, en dollars */
    const cvt = (s&&!A.tauxManque&&(A.dev==='EUR'||A.frais>0)) ? `<small class="conv" style="display:block;font-size:11px;color:var(--ink-3);white-space:nowrap">= ${money2(x.cout)} rendu</small>` : '';
    const lu = x.par ? `<span class="lu" data-nolang>« ${esc(x.des||'')} »${x.ref?' · réf. '+esc(x.ref):''}</span>` : '';
    const chg = (x.par==='devine' && (x.cands||[]).length) ? `<span class="chg"><span>reconnu par le nom — vérifie :</span> <select data-choix="${x._i}">${(x.cands||[]).map(c=>`<option value="${esc(c.cle)}"${c.cle===x.cle?' selected':''}>${esc(nomCat(c.cle))}${ozDe(c.cle)?' · '+esc(ozDe(c.cle))+' oz':''}</option>`).join('')}</select></span>` : '';
    /* le nom du parfum ouvre sa fiche dans une fenêtre (Igal, 17 oct. 2026 : « quand je clique sur un produit, une fenêtre s'ouvre pour que Sam ait la fiche ») */
    const nomF=`<a class="fiche" href="catalogue.html#cle=${encodeURIComponent(x.cle)}" data-fiche="${esc(x.cle)}" title="Ouvrir la fiche de ce parfum">${esc(v[1])}</a>`;
    const tete=`<tr class="${x.manque?'neg':''}${EDITS[x._i]?' corr':''}"><td class="ref"><div class="mq">${esc(v[2])}</div><b>${nomF}${tyBadge(x.cle)}</b><span>${v[0]||'sans code-barres'}</span>${lu}${chg}</td>`;
    /* Igal, 17 oct. 2026 : sur une facture d'achat le PRIX MOYEN est le chiffre principal (« 22,50 → 20,37 »), le prix de la
       facture passe au second plan, plus petit, à droite */
    if(s) return tete+`<td class="r">${cell(x,'q')}</td>${rep?repCell(x):''}<td>${mv}</td><td class="r moy">${pr}${expl}</td><td class="r pfac">${cell(x,'p')}${cvt} ${sup(x)}</td></tr>`;
    return tete+`<td class="r">${cell(x,'q')}</td><td class="r">${cell(x,'p')}${cvt}</td><td>${mv}</td><td class="r">${pr} ${sup(x)}</td></tr>`;
  }).join('');
  const nCorr=Object.keys(EDITS).length;
  const nouveauFrn = s && $('tiers').value.trim() && !FRN[$('tiers').value.trim()];
  /* un export qui contient des retours peut sortir un solde negatif : le signe suit le solde */
  const eff = s ? `+${nf(A.unites-(A.pcU||0))}` : (A.unites<0 ? `+${nf(-A.unites)}` : `−${nf(A.unites)}`);
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
  box.innerHTML=bandeau+(A.tauxManque?`<div class="av c" style="margin-bottom:12px"><b>Facture en euros : indique le taux payé</b> (1 € = combien de dollars), dans la case au-dessus. Il est sur le relevé bancaire, au débit de cette facture. Tant qu'il manque, rien ne s'enregistre.</div>`:'')+`
    <div class="ap">
      <div><span class="v">${nf(A.L.length)}</span><span class="k">lignes lues</span></div>
      <div><span class="v" style="color:var(--iris)">${nf(A.connues)}</span><span class="k">produits reconnus</span></div>
      <div><span class="v"${A.inconnues?' style="color:var(--warn)"':''}>${nf(A.inconnues)}</span><span class="k">à reconnaître</span></div>
      <div><span class="v">${A.tauxManque?`<span data-nolang>${nf(Math.round(A.montant))} €</span>`:money(A.montantUsd+(s?A.frais:0))}</span><span class="k">${s&&A.dev==='EUR'?`coût en dollars · <span data-nolang>${nf(Math.round(A.montant))} € × ${String(A.taux).replace('.',',')}</span>`:'montant'}${s&&A.frais?` · dont ${money(A.frais)} de frais`:''}</span></div>
      <div><span class="v" style="color:${A.stock?(s?'var(--good)':'var(--iris)'):'var(--ink-3)'}">${A.stock?eff:'0'}</span><span class="k">${s?(A.pcU?L3('unités pour Perfumes Trade','units for Perfumes Trade','unidades para Perfumes Trade'):'unités en stock'):'unités sorties'}</span></div>
      ${A.pcU?`<div><span class="v" style="color:#c2417f">+${nf(A.pcU)}</span><span class="k">${L3('unités pour Perfume City','units for Perfume City','unidades para Perfume City')}</span></div>`:''}
      ${s?`<div><span class="v" style="color:${A.ecart<0?'var(--good)':A.ecart>0?'var(--crit)':'var(--ink-3)'}">${A.ecart?(A.ecart>0?'+':'−')+money(Math.abs(A.ecart)):'0 $'}</span><span class="k">écart vs prix connus</span></div>`:''}
    </div>
    ${edit?`<p class="ecr" style="margin:12px 0 0">Vérifie la lecture : quantités et prix se corrigent dans le tableau, une ligne se retire avec ✕. Rien n'est enregistré avant le bouton.${nCorr?` <b>${nCorr} correction${nCorr>1?'s':''}</b> pour l'instant.`:''}</p>`:''}
    ${nouveauFrn?`<div class="av" style="margin-top:12px;background:var(--iris-soft);border-left-color:var(--iris)"><b>Nouveau fournisseur : « ${esc($('tiers').value.trim())} ».</b> Sa fiche sera créée à l'enregistrement, avec cette facture comme première ligne — coordonnées à compléter ensuite dans <a href="fournisseurs.html">Fournisseurs</a>.</div>`:''}
    ${(AUTO_SWAP>0&&SWAP&&!A.inversion)?`<div class="av" id="inv-auto" style="margin-top:12px;background:var(--iris-soft);border-left-color:var(--iris)"><b>${L3('Prix et quantités inversés automatiquement.','Prices and quantities swapped automatically.','Precios y cantidades invertidos automáticamente.')}</b>
      ${L3(`Sur ${nf(AUTO_SWAP)} parfums, la colonne lue comme « quantité » était en fait le prix connu de la fiche. Vérifie les quantités et les prix dans le tableau ci-dessous.`,`On ${nf(AUTO_SWAP)} perfumes, the column read as "quantity" was actually the price known on the product sheet. Check the quantities and prices in the table below.`,`En ${nf(AUTO_SWAP)} perfumes, la columna leída como «cantidad» era en realidad el precio conocido de la ficha. Revisa las cantidades y los precios en la tabla de abajo.`)}
      <div style="margin-top:8px"><button type="button" class="btn" id="inv-undo">${L3('Annuler l\'inversion (c\'était correct)','Undo the swap (it was correct)','Deshacer la inversión (era correcto)')}</button></div></div>`:''}
    ${(A.inversion&&!INV_OK)?`<div class="av c" id="inv-bloc" style="margin-top:12px"><b>${SWAP?L3('Prix et quantités inversés : vérifie encore.','Prices and quantities swapped: check again.','Precios y cantidades invertidos: revisa de nuevo.'):L3('Attention : les prix et les quantités semblent INVERSÉS.','Warning: prices and quantities look SWAPPED.','Atención: los precios y las cantidades parecen INVERTIDOS.')}</b>
      ${A.inversion.inv>=2?L3(`Sur ${nf(A.inversion.inv)} parfums, la « quantité » lue ressemble au prix connu de la fiche (et le « prix » à une quantité).`,`On ${nf(A.inversion.inv)} perfumes, the "quantity" read looks like the price known on the product sheet (and the "price" like a quantity).`,`En ${nf(A.inversion.inv)} perfumes, la «cantidad» leída se parece al precio conocido de la ficha (y el «precio» a una cantidad).`):''}
      ${A.inversion.frac>0?L3(`${nf(A.inversion.frac)} « quantité(s) » ne sont pas des nombres entiers.`,`${nf(A.inversion.frac)} "quantity" value(s) are not whole numbers.`,`${nf(A.inversion.frac)} «cantidad(es)» no son números enteros.`):''}
      ${L3('Rien ne s\'enregistre tant que tu n\'as pas choisi.','Nothing is saved until you choose.','No se guarda nada hasta que elijas.')}
      <div style="margin-top:8px"><button type="button" class="btn pri" id="inv-swap">${L3('Inverser prix et quantités','Swap prices and quantities','Invertir precios y cantidades')}</button>
      <button type="button" class="btn" id="inv-ok" style="margin-left:8px">${L3('Non, c\'est correct','No, it is correct','No, es correcto')}</button></div></div>`:''}
    ${rep&&A.connues?`<p class="repnote">${L3(`<b>Perfume City :</b> pour chaque parfum, tape combien de flacons vont à Perfume City — le reste reste à Perfumes Trade (les deux cases se complètent). À l'enregistrement, le stock des deux est mis à jour, et Perfume City aussi sur Shopify (les flacons sont <b>ajoutés</b> à son stock actuel). Le premier flacon d'une référence que la boutique n'a pas encore part en <b>tester</b> (vitrine) : il n'est pas mis en vente, comme pour un transfert depuis la fiche.`,`<b>Perfume City:</b> for each perfume, type how many bottles go to Perfume City — the rest stays with Perfumes Trade (the two boxes add up). When you save, both stocks are updated, and Perfume City's on Shopify too (the bottles are <b>added</b> to its current stock). The first bottle of a reference the shop does not have yet goes as a <b>tester</b> (display): it is not put on sale, as for a transfer from the record.`,`<b>Perfume City:</b> para cada perfume, escribe cuántos frascos van a Perfume City — el resto se queda en Perfumes Trade (las dos casillas se completan). Al guardar, se actualiza el stock de ambos, y el de Perfume City también en Shopify (los frascos se <b>suman</b> a su stock actual). El primer frasco de una referencia que la tienda aún no tiene va como <b>tester</b> (vitrina): no se pone a la venta, como en un traslado desde la ficha.`)}</p>`:''}
    <div style="overflow-x:auto;margin-top:12px"><table class="tb"><thead><tr>
      ${s?`<th>Référence</th><th class="r">Qté</th>${rep?`<th class="r rep2">${L3('Répartir : Perfumes Trade · Perfume City','Split: Perfumes Trade · Perfume City','Repartir: Perfumes Trade · Perfume City')}</th>`:''}<th>Stock</th><th class="r">${L3('Dernier prix payé','Last price paid','Último precio pagado')}</th><th class="r">Prix de la facture${A.dev==='EUR'?' (€)':''}</th>`:`<th>Référence</th><th class="r">Qté</th><th class="r">Prix</th><th>Stock</th><th class="r">Prix d'achat</th>`}
    </tr></thead><tbody>${li}</tbody></table></div>
    ${A.doublon?`<div class="av c" style="margin-top:12px"><b>Le numéro ${esc($('num').value)} est déjà enregistré.</b> Enregistrer deux fois la même facture doublerait les quantités. Si c'est vraiment une autre facture, change le numéro.</div>`:''}
    ${A.neg?`<div class="av c" style="margin-top:12px"><b>${A.neg} ligne${A.neg>1?'s':''} ${A.neg>1?'font':'fait'} passer le stock sous zéro.</b> On vend plus qu'il n'y a en stock : le stock est ramené à 0, et le comptage est faux quelque part. La quantité manquante est notée au journal.</div>`:''}
    ${A.inconnues?`<div class="av" style="margin-top:12px"><b>${A.inconnues} ligne${A.inconnues>1?'s':''} pas encore reconnue${A.inconnues>1?'s':''}</b> — elle${A.inconnues>1?'s':''} ne ser${A.inconnues>1?'ont':'a'} pas enregistrée${A.inconnues>1?'s':''} tant que tu n'as pas dit quel parfum c'est (choix dans la ligne, ou « créer l'article »). Ton choix est retenu pour les prochaines factures de ce fournisseur.</div>`:''}`;
  $('ok').disabled = !(A.connues>0 && !A.doublon && !A.tauxManque && !(A.inversion&&!INV_OK));
  { const b1=$('inv-swap'), b2=$('inv-ok');
    if(b1) b1.onclick=()=>{ SWAP=!SWAP; INV_OK=false; dessineApercu(); };
    if(b2) b2.onclick=()=>{ INV_OK=true; dessineApercu(); }; }
  { const bu=$('inv-undo'); if(bu) bu.onclick=()=>{ SWAP=false; AUTO_SWAP=0; INV_OK=true; dessineApercu(); }; }
  $('ok').textContent = libelleBouton(A.connues || 0);
  /* corrections : on relit l'aperçu à chaque changement validé (Entrée ou sortie du champ) */
  /* la valeur est retenue à chaque frappe ou clic de flèche ; l'aperçu ne se
     redessine qu'en quittant la case — le redessiner sur « change » recréait la
     case sous la souris et les flèches de quantité ne répondaient plus */
  box.querySelectorAll('input.ed').forEach(inp=>{ inp.oninput=()=>{ const i=+inp.dataset.i, k=inp.dataset.e, v=inp.value.trim();
    EDITS[i]=Object.assign({},EDITS[i]||{}); if(v==='') delete EDITS[i][k]; else EDITS[i][k]=k==='q'?Math.max(0,Math.round(+v)):Math.max(0,+v);
    if(!Object.keys(EDITS[i]).length) delete EDITS[i]; };
    inp.onblur=()=>apresChamp(); });
  /* les deux cases se complètent : taper l'une règle l'autre (la somme est toujours la quantité reçue) */
  box.querySelectorAll('input.rp').forEach(inp=>{ inp.oninput=()=>{ const i=+inp.dataset.i, x=(A.L||[]).find(l=>l._i===i); if(!x) return;
      const q=x.q||0, v=Math.max(0,Math.min(q,Math.round(+inp.value||0))), pc=inp.dataset.rp==='pc'?v:q-v;
      REP[i]=pc;
      const autre=box.querySelector(`input.rp[data-i="${i}"][data-rp="${inp.dataset.rp==='pc'?'pt':'pc'}"]`);
      if(autre) autre.value=inp.dataset.rp==='pc'?q-pc:pc; };
    inp.onblur=()=>apresChamp();
    inp.addEventListener('input',()=>{ clearTimeout(T_REP); T_REP=setTimeout(redessineGardantLeChamp,700); }); });
  box.querySelectorAll('[data-sup]').forEach(b=>b.onclick=()=>{ const i=+b.dataset.sup; EDITS[i]=Object.assign({},EDITS[i]||{},{sup:true}); dessineApercu(); });
  box.querySelectorAll('[data-cree]').forEach(b=>b.onclick=()=>creeDepuisLigne(+b.dataset.cree));
  box.querySelectorAll('a[data-fiche]').forEach(a=>a.onclick=e=>{ e.preventDefault(); ouvreFicheFenetre(a.dataset.fiche); });
  /* « c'est lequel ? » : le choix est retenu (code article de ce fournisseur, et ce nom) */
  const retient=(i,cle)=>{ const x=(A.L||[]).find(l=>l._i===i); if(!x||!cle||!IDX[cle]) return;
    apprendRef(x.ref,cle,$('tiers').value.trim()); apprendNom(x.des,cle);
    log({act:'creation',lib:'ligne de facture reconnue — « '+(x.des||x.ref||'')+' » = '+nomCat(cle),bc:IDX[cle][0],ref:nomCat(cle),av:null,ap:null});
    dessineApercu(); };
  box.querySelectorAll('[data-choix]').forEach(sel=>sel.onchange=()=>retient(+sel.dataset.choix,sel.value));
  box.querySelectorAll('[data-cherche]').forEach(inp=>inp.onchange=()=>{ const o=[...$('l-cat').options].find(op=>op.value===inp.value); if(o) retient(+inp.dataset.cherche,o.dataset.cle); });
  if(box.querySelector('[data-cherche]')) remplitCat();
  box.querySelectorAll('[data-map]').forEach(sel=>sel.onchange=()=>{
    MAP[sel.dataset.map]=sel.value; dessineApercu();
    const d=box.querySelector('.mapbox'); if(d) d.open=true; });
  const ml=box.querySelector('#map-lieu');
  if(ml) ml.onchange=()=>{ LIEU=ml.value; dessineApercu();
    const d=box.querySelector('.mapbox'); if(d) d.open=true; };
}
let CAT_OK=false;
function remplitCat(){ if(CAT_OK) return; CAT_OK=true;
  const dl=$('l-cat'); dl.innerHTML=Object.entries(IDX).map(([cle,v])=>`<option data-cle="${esc(cle)}" value="${esc(nomCat(cle)+(ozDe(cle)?' '+ozDe(cle)+' oz':'')+(v[0]?' — '+v[0]:''))}">`).join(''); }
/* La fiche du parfum dans une fenêtre, par-dessus la facture (Igal, 17 oct. 2026). C'est la fiche du Catalogue elle-même,
   ouverte en « mode cadre » (catalogue.html#cle=…&cadre=1) : mêmes champs, mêmes droits, même enregistrement. À la fermeture,
   l'aperçu est relu, pour que le stock et le prix d'achat montrés tiennent compte de ce qui vient d'être changé. */
function ouvreFicheFenetre(cle){ ficheFenetre(cle,()=>{ try{ refaitIndex(); }catch(e){} dessineApercu(); }); }
/* un code-barres inconnu sur une facture d'achat : on crée l'article ici, avec ce qu'on sait.
   Igal, 17 oct. 2026 : « quand je crée l'article et que ça bouffe des petites fenêtres carrées, je déteste ça.
   Je veux une fiche technique que je remplis » — une vraie fiche, avec la photo, au lieu de trois questions à la suite. */
function creeDepuisLigne(i){
  const x=(APERCU&&APERCU.L||[]).find(l=>l._i===i); if(!x) return;
  if(document.getElementById('ft-ov')) return;
  const d=litDesignation(x.des||'');
  /* 28 sept. (capture d'Igal) : « MAISON » + « ALHAMBRA JEAN LOWE… » — la marque proposée
     était le premier mot. On propose la plus longue marque DÉJÀ connue du catalogue par
     laquelle la désignation commence (Maison Alhambra, Fragrance World…), écrite comme au
     catalogue ; et le nom proposé perd la contenance, le type et le genre, qui ont leurs cases.
     La fiche est dans la langue de l'écran. */
  const lg=(typeof LANG==='string')?LANG:'fr', t3=(fr,en,es)=>lg==='en'?en:lg==='es'?es:fr;
  const des=String(x.des||'').replace(/\s+/g,' ').trim(), desN=des.toLowerCase();
  let mq='';
  Object.values(IDX).forEach(v=>{ const m=String(v[2]||'').trim(); if(m.length>mq.length && (desN===m.toLowerCase()||desN.startsWith(m.toLowerCase()+' '))) mq=m; });
  if(!mq) mq=des.split(' ')[0]||'';
  const reste=des.replace(new RegExp('^'+mq.trim().replace(/[.*+?^${}()|[\]\\]/g,'\\$&')+'\\s*','i'),'')
    .replace(/\s+\d+(?:[.,]\d+)?\s*(?:oz|ml)?\b.*$/i,'').replace(/\s+(EDP|EDT|EDC)\b.*$/i,'').trim();
  const marques=[...new Set(Object.values(IDX).map(v=>String(v[2]||'').trim()).filter(Boolean))].sort((a,b)=>a.localeCompare(b));
  const pa0=(x.pUsd!=null?x.pUsd:x.p);
  const nb=v=>v==null||v===''?'':String(v).replace('.',',');
  const bcN=v=>String(v||'').replace(/\D/g,'').replace(/^0+/,'');
  /* Igal, 17 oct. 2026 : « je veux qu'il puisse mettre les prix de chaque canal » — un prix par canal de vente, ceux des Réglages.
     Le site (retail) et le site de gros sont les deux prix de base de la fiche ; les autres canaux (Amazon, Perfume City…)
     gardent leur prix dans la fiche, canal par canal, comme dans le Catalogue. */
  const CAN=(()=>{ let L=null; try{ const r=lit('reglages-v1',{}); if(r&&Array.isArray(r.canaux)&&r.canaux.length) L=r.canaux.filter(c=>c&&c.id); }catch(e){}
    L=L||[{id:'site',nom:'Site perfumestrade.com'},{id:'sitegros',nom:'Site wholesale.perfumestrade.com'},{id:'amazon',nom:'Amazon'},{id:'perfumecity',nom:'Perfume City'}];
    if(!L.some(c=>c.id==='site')) L=[{id:'site',nom:'Site perfumestrade.com'}].concat(L);
    if(!L.some(c=>c.id==='sitegros')) L.splice(L.findIndex(c=>c.id==='site')+1,0,{id:'sitegros',nom:'Site wholesale.perfumestrade.com'});
    return L; })();
  const idCan=c=>c.id==='site'?'ft-pvr':c.id==='sitegros'?'ft-pvw':'ft-c-'+c.id;
  const champCan=c=>`<div class="ft-f2"><label for="${idCan(c)}">${esc(c.nom||c.id)} ($)</label><input id="${idCan(c)}" inputmode="decimal" autocomplete="off" placeholder="${t3('à compléter plus tard','fill in later','completar después')}"></div>`;
  const ov=document.createElement('div'); ov.id='ft-ov'; ov.className='ft-ov';
  const picto='<svg viewBox="0 0 40 64" fill="none" aria-hidden="true"><rect x="14.5" y="2" width="11" height="9" rx="1.5" stroke="currentColor" stroke-width="2.4"/><path d="M11 20a6 6 0 016-6h6a6 6 0 016 6v34a6 6 0 01-6 6H17a6 6 0 01-6-6V20z" stroke="currentColor" stroke-width="2.4"/></svg>';
  ov.innerHTML=`<div class="ft" role="dialog" aria-modal="true" aria-labelledby="ft-t">
    <div class="ft-h"><div><h2 id="ft-t">${t3('Nouvel article','New item','Nuevo artículo')}</h2>
      <p>${t3('Ligne de la facture','Invoice line','Línea de la factura')} : <b>${esc(des)}</b></p></div>
      <button type="button" class="ft-x" id="ft-x" aria-label="${t3('Fermer','Close','Cerrar')}">&times;</button></div>
    <div class="ft-b">
      <div class="ft-ph">
        <div class="ft-img" id="ft-img">${picto}<span>${t3('sans photo','no photo','sin foto')}</span></div>
        <button type="button" class="btn" id="ft-phb">${t3('Ajouter une photo','Add a photo','Añadir una foto')}</button>
        <button type="button" class="btn" id="ft-web">${t3('Chercher la photo sur Internet','Find the photo on the Internet','Buscar la foto en Internet')}</button>
        <input type="file" id="ft-phf" accept="image/*" hidden>
        <button type="button" class="lnk" id="ft-phx" hidden>${t3('Retirer la photo','Remove the photo','Quitar la foto')}</button>
      </div>
      <div class="ft-g">
        <div class="ft-f2"><label for="ft-marque">${t3('Marque','Brand','Marca')} <b>*</b></label><input id="ft-marque" list="ft-marques" autocomplete="off" value="${esc(mq)}">
          <small>${t3('Nouvelle marque : tape son nom, elle est créée avec l\'article.','New brand: type its name, it is created with the item.','Marca nueva: escribe su nombre, se crea con el artículo.')}</small></div>
        <div class="ft-f2"><label for="ft-nom">${t3('Nom du parfum (sans la marque)','Perfume name (without the brand)','Nombre del perfume (sin la marca)')} <b>*</b></label><input id="ft-nom" autocomplete="off" value="${esc(reste)}"></div>
        <div class="ft-f2"><label for="ft-ml">${t3('Contenance (oz)','Size (oz)','Tamaño (oz)')}</label><input id="ft-ml" inputmode="decimal" autocomplete="off" value="${esc(d.ml||'')}"></div>
        <div class="ft-f2"><label for="ft-type">Type</label><input id="ft-type" list="ft-types" placeholder="EDP, EDT…" autocomplete="off" value="${esc(d.type||'')}"></div>
        <div class="ft-f2"><label for="ft-genre">${t3('Genre','Gender','Género')}</label><select id="ft-genre">
          <option value="">${t3('— inconnu —','— unknown —','— desconocido —')}</option>
          <option value="M"${d.genre==='M'?' selected':''}>${t3('Homme','Men','Hombre')}</option>
          <option value="W"${d.genre==='W'?' selected':''}>${t3('Femme','Women','Mujer')}</option>
          <option value="U"${d.genre==='U'?' selected':''}>${t3('Unisexe','Unisex','Unisex')}</option>
          <option value="K">${t3('Enfant','Kids','Niños')}</option></select></div>
        <div class="ft-f2"><label for="ft-bc">${t3('Code-barres','Barcode','Código de barras')}</label><input id="ft-bc" inputmode="numeric" autocomplete="off" value="${esc(x.bc||'')}"></div>
        <div class="ft-f2"><label for="ft-pa">${t3('Prix d\'achat','Purchase price','Precio de compra')} ($)</label><input id="ft-pa" inputmode="decimal" autocomplete="off" value="${esc(nb(pa0))}"></div>
        <div class="ft-sec">${t3('Prix de vente par canal','Selling price by channel','Precio de venta por canal')}</div>
        ${CAN.map(champCan).join('')}
      </div>
      <datalist id="ft-marques">${marques.map(m=>`<option value="${esc(m)}">`).join('')}</datalist>
      <datalist id="ft-types"><option value="EDP"><option value="EDT"><option value="EDC"><option value="PARFUM"><option value="EXTRAIT"><option value="COLOGNE"></datalist>
    </div>
    <p class="ft-note">${t3('Seuls la marque et le nom sont obligatoires. Le stock arrive avec la facture, quand tu l\'enregistres.','Only the brand and the name are required. The stock arrives with the invoice, when you save it.','Solo la marca y el nombre son obligatorios. El stock llega con la factura, cuando la guardas.')}</p>
    <div class="ft-ft"><span class="ft-msg" id="ft-msg" role="alert"></span>
      <button type="button" class="btn" id="ft-ann">${t3('Annuler','Cancel','Cancelar')}</button>
      <button type="button" class="btn pri" id="ft-ok">${t3('Créer l\'article','Create the item','Crear el artículo')}</button></div>
  </div>`;
  document.body.appendChild(ov);
  const g=id=>document.getElementById(id);
  let photo='';
  const ferme=()=>{ document.removeEventListener('keydown',onKey); ov.remove(); };
  const onKey=e=>{ if(e.key==='Escape'&&!document.getElementById('pw-ov')) ferme(); };   /* la recherche de photo, ouverte par-dessus, se ferme la première */
  document.addEventListener('keydown',onKey);
  const msg=m=>{ g('ft-msg').textContent=m||''; };
  const montrePhoto=()=>{
    g('ft-img').innerHTML=photo?`<img src="${photo}" alt="">`:picto+`<span>${t3('sans photo','no photo','sin foto')}</span>`;
    g('ft-phx').hidden=!photo; g('ft-phb').textContent=photo?t3('Changer la photo','Change photo','Cambiar la foto'):t3('Ajouter une photo','Add a photo','Añadir una foto');
  };
  g('ft-phb').onclick=()=>{ g('ft-phf').value=''; g('ft-phf').click(); };
  g('ft-phx').onclick=()=>{ photo=''; montrePhoto(); };
  /* Igal, 17 oct. 2026 : « chercher la photo sur Internet, proposer un choix à Sam » — la recherche part de ce qui est déjà rempli dans la fiche */
  g('ft-web').onclick=async()=>{
    const q=[g('ft-marque').value,g('ft-nom').value,g('ft-ml').value.trim()?g('ft-ml').value.trim()+' oz':'',g('ft-type').value,'perfume'].map(v=>String(v).trim()).filter(Boolean).join(' ');
    const u=await photoWeb(q); if(u){ photo=u; msg(''); montrePhoto(); }
  };
  g('ft-phf').onchange=async e=>{
    const f=e.target.files&&e.target.files[0]; if(!f) return;
    try{ photo=await photoReduite(f); msg(''); }catch(err){ msg(t3('Photo illisible : ','Unreadable photo: ','Foto ilegible: ')+(err&&err.message||'')); }
    montrePhoto();
  };
  g('ft-x').onclick=ferme; g('ft-ann').onclick=ferme;
  const num=id=>{ const v=g(id).value.trim().replace(',','.'); if(v==='') return null; const n=+v; return isFinite(n)&&n>=0?n:NaN; };
  g('ft-ok').onclick=()=>{
    const marque=g('ft-marque').value.trim(), nom=g('ft-nom').value.trim();
    if(!marque){ msg(t3('Indique la marque.','Enter the brand.','Indica la marca.')); g('ft-marque').focus(); return; }
    if(!nom){ msg(t3('Indique le nom du parfum.','Enter the perfume name.','Indica el nombre del perfume.')); g('ft-nom').focus(); return; }
    const pa=num('ft-pa'), pvr=num('ft-pvr'), pvw=num('ft-pvw'), pc={};
    CAN.forEach(c=>{ if(c.id==='site'||c.id==='sitegros') return; const v=num(idCan(c)); pc[c.id]=v; });
    if([pa,pvr,pvw].concat(Object.values(pc)).some(v=>Number.isNaN(v))){ msg(t3('Un prix n\'est pas un nombre.','A price is not a number.','Un precio no es un número.')); return; }
    const bc=g('ft-bc').value.replace(/\s+/g,'');
    if(bc && !/^\d{6,20}$/.test(bc)){ msg(t3('Le code-barres ne doit contenir que des chiffres.','The barcode must contain digits only.','El código de barras solo lleva cifras.')); g('ft-bc').focus(); return; }
    if(bc){ const dj=Object.entries(IDX).find(([,v])=>bcN(v[0])===bcN(bc)); if(dj){ msg(t3('Ce code-barres existe déjà : ','This barcode already exists: ','Este código de barras ya existe: ')+((dj[1][2]||'')+' '+(dj[1][1]||'')).trim()); g('ft-bc').focus(); return; } }
    const AJ=lit('articles-ajoutes-v1',[]); const L=Array.isArray(AJ)?AJ:[];
    const o={id:'a'+Date.now().toString(36)+Math.random().toString(36).slice(2,6),bc:bc,nom:nom,marque:marque,ml:g('ft-ml').value.trim().replace(',','.'),type:g('ft-type').value.trim().toUpperCase(),genre:g('ft-genre').value,qte:0,pa:pa,pvr:pvr,pvw:pvw};
    L.push(o); ecrit('articles-ajoutes-v1',L);
    Object.keys(pc).forEach(k=>{ if(pc[k]==null) delete pc[k]; });
    if(Object.keys(pc).length){ MOD[o.id]=Object.assign({},MOD[o.id]||{},{pc}); ecrit(K.mod,MOD); }
    if(photo){ try{ const H=lit('photos-perso-v1',{}); const HH=(H&&typeof H==='object'&&!Array.isArray(H))?H:{}; HH[o.id]=photo; ecrit('photos-perso-v1',HH); }catch(e){} }
    /* une ligne sans code-barres (ou dont le code a été changé ici) : l'article créé est retenu pour cette référence et ce nom */
    if(!x.bc || bcN(bc)!==bcN(x.bc)){ refaitIndex(); apprendRef(x.ref,o.id,$('tiers').value.trim()); apprendNom(x.des,o.id); }
    log({act:'creation',lib:'article créé depuis la facture '+($('num').value.trim()||'')+' — '+(o.marque+' '+o.nom),bc:o.bc,ref:o.marque+' '+o.nom,av:null,ap:o.pa});
    ferme(); refaitIndex(); dessineApercu();
  };
  setTimeout(()=>{ const f=g(g('ft-marque').value?'ft-nom':'ft-marque'); if(f) f.focus(); },30);
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
  if(A.inversion&&!INV_OK) return;   /* prix et quantités à vérifier : rien ne s'enregistre */
  const r2=v=>Math.round(v*100)/100;
  const canal=SENS==='canal';
  const tiers=canal?$('canal-nom').value:$('tiers').value.trim();
  const canalV = canal ? tiers : (SENS==='vente' ? $('canal-vente').value : undefined);
  if(!tiers){ $('msg').textContent=SENS==='achat'?'Indique le fournisseur.':'Indique le client.'; $('tiers').focus(); return; }
  const d=$('date').value||ajd();
  const num=$('num').value.trim()||((canal?'EXPORT-'+tiers.toUpperCase().replace(/\s+/g,'')+'-':'SANS-NUM-')+d.replace(/-/g,'')+'-'+Date.now().toString(36).slice(-4).toUpperCase());
  /* Igal, 18 oct. 2026 : « demander une double validation : est-ce que Save the purchase augmente le stock ? » — avant d'enregistrer
     une facture d'ACHAT, on dit en clair ce qui va se passer sur le stock, et on demande confirmation. */
  if(SENS==='achat'){
    const nL=A.L.filter(x=>x.cle).length, nU=A.L.filter(x=>x.cle).reduce((a,x)=>a+(x.q||0),0);
    const nPC=A.L.filter(x=>x.cle).reduce((a,x)=>a+(x.pc||0),0), nPT=nU-nPC;
    const q = (A.stock&&nPC>0)
      ? L3(`Enregistrer cette facture d'achat ?\n\nOUI, le stock augmente de ${nf(nU)} flacon${nU>1?'s':''} reçu${nU>1?'s':''} :\n• ${nf(nPT)} pour Perfumes Trade\n• ${nf(nPC)} pour Perfume City (son stock est aussi augmenté sur Shopify)`+(A.majPrix?`\nLe prix d'achat moyen de Perfumes Trade est recalculé.`:''),
           `Save this purchase?\n\nYES, stock goes up by ${nf(nU)} bottle${nU>1?'s':''} received:\n• ${nf(nPT)} for Perfumes Trade\n• ${nf(nPC)} for Perfume City (its stock also goes up on Shopify)`+(A.majPrix?`\nThe Perfumes Trade average cost is recalculated.`:''),
           `¿Guardar esta compra?\n\nSÍ, el stock sube ${nf(nU)} frasco${nU>1?'s':''} recibido${nU>1?'s':''}:\n• ${nf(nPT)} para Perfumes Trade\n• ${nf(nPC)} para Perfume City (su stock también sube en Shopify)`+(A.majPrix?`\nEl precio de compra medio de Perfumes Trade se recalcula.`:''))
      : A.stock
      ? L3(`Enregistrer cette facture d'achat ?\n\nOUI, le stock augmente : ${nf(nU)} flacon${nU>1?'s':''} ajouté${nU>1?'s':''} sur ${nf(nL)} référence${nL>1?'s':''}.`+(A.majPrix?`\nLe prix d'achat moyen est recalculé (il se lit sur la fiche).`:''),
           `Save this purchase?\n\nYES, stock goes up: ${nf(nU)} bottle${nU>1?'s':''} added across ${nf(nL)} reference${nL>1?'s':''}.`+(A.majPrix?`\nThe average cost is recalculated (shown on the product sheet).`:''),
           `¿Guardar esta compra?\n\nSÍ, el stock sube: ${nf(nU)} frasco${nU>1?'s':''} añadido${nU>1?'s':''} en ${nf(nL)} referencia${nL>1?'s':''}.`+(A.majPrix?`\nEl precio de compra medio se recalcula (se ve en la ficha).`:''))
      : L3(`Enregistrer cette facture d'achat ?\n\nNON, le stock ne bouge pas (case « Mettre le stock à jour » décochée) : la facture est seulement archivée.`,
           `Save this purchase?\n\nNO, stock does not change ("Update stock" is unchecked): the invoice is only filed.`,
           `¿Guardar esta compra?\n\nNO, el stock no cambia (casilla «Actualizar el stock» desmarcada): la factura solo se archiva.`);
    if(!confirm(q)) return;
  }
  demandeUser();
  const s=SENS==='achat', lignes=[], det=[], det_pc=[], pcRate=[]; let nTest=0;
  let nCmd=0;
  if(canal){ A.L.forEach(x=>(x.cmds||[]).forEach(c=>{ if(c.cmd){ CMD[c.cleCmd]=d; nCmd++; } })); ecrit(K_CMD,CMD); }
  let nprix=0;
  A.L.forEach(x=>{
    if(!x.cle) return;
    const v=IDX[x.cle], ref=v[2]+' '+v[1];
    lignes.push({cle:x.cle,bc:v[0],ref,q:x.q||0,pc:(s&&x.pc>0)?x.pc:undefined,p:s?x.pUsd:x.p,pDev:(s&&A.dev==='EUR')?x.p:undefined,cout:s?x.cout:undefined,qAv:x.qAv,qAp:x.qAp,manque:x.manque||0,paAv:x.paAv,paAp:(s&&A.majPrix)?x.paNv:x.paAv,
                 cmds: canal ? (x.cmds||[]).map(c=>({cmd:c.cmd,q:c.q,p:c.p,d:c.d,h:c.h||undefined,client:c.client})) : undefined});
    if(A.stock&&x.qAp!==x.qAv){ MOD[x.cle]=Object.assign({},MOD[x.cle]||{},{qte:x.qAp}); det.push({bc:v[0],ref,av:x.qAv,ap:x.qAp}); }
    /* la part de Perfume City entre dans SON stock (magasin partagé pc-stock-v1) — jamais dans celui de Perfumes Trade */
    if(s&&A.stock&&x.pc>0){ const pt=pcPartage(v[0],x.pc), L=lignes[lignes.length-1]; L.pcVend=pt.vend; L.pcT=pt.t;
      const pr=pt.vend>0?pcAjouteErp(x.cle,pt.vend):{av:null,ap:null};
      if(pr){ if(pt.t) pcTestNote(v[0],ref,+pt.t); if(pt.vend>0) det_pc.push({bc:v[0],ref,av:pr.av,ap:pr.ap}); L.pcAv=pr.av; L.pcAp=pr.ap; if(pt.t) nTest+=pt.t; } else pcRate.push(ref); }
    if(s&&x.par==='devine'){ apprendRef(x.ref,x.cle,tiers); apprendNom(x.des,x.cle); }
    if(s){
      (HIST[x.cle]=HIST[x.cle]||[]).push({d,p:x.cout,f:tiers,q:x.q||null,src:'facture',num,dev:A.dev==='EUR'?'EUR':undefined,pDev:A.dev==='EUR'?x.p:undefined});
      if(A.majPrix&&x.paAv!==x.paNv){ MOD[x.cle]=Object.assign({},MOD[x.cle]||{},{pa:x.paNv}); nprix++;
        log({act:'prix',lib:"prix d'achat moyen, facture "+num+" — "+tiers,bc:v[0],ref,av:x.paAv??null,ap:x.paNv}); }
    } else {
      /* un fichier de canal : une entrée par commande, avec sa date et son heure —
         c'est ce qui permet de voir plus tard à quelles heures ça vend */
      if(canalV && x.cmds && x.cmds.length) x.cmds.forEach(c=>(VENT[x.cle]=VENT[x.cle]||[]).push({d:c.d||d,h:c.h||undefined,p:c.p!=null?c.p:x.p,c:c.client||tiers,q:c.q||null,num,k:canalV}));
      else (VENT[x.cle]=VENT[x.cle]||[]).push({d,p:x.p,c:tiers,q:x.q||null,num,k:canalV});
    }
  });
  if(s) FRN[tiers]=Object.assign({nom:tiers},FRN[tiers]||{},{maj:new Date().toISOString()});
  else if(!canal) CLI[tiers]=Object.assign({nom:tiers},CLI[tiers]||{},{maj:new Date().toISOString()});
  const f={id:'f'+Date.now().toString(36),num,sens:canal?'vente':SENS,canal:canalV,export:canal||undefined,tiers,d,lignes,
           montant:s?r2(A.montantUsd+A.frais):A.montant,stock:A.stock,
           devise:(s&&A.dev==='EUR')?'EUR':undefined,taux:(s&&A.dev==='EUR')?A.taux:undefined,montantDevise:(s&&A.dev==='EUR')?A.montant:undefined,frais:(s&&A.frais)?A.frais:undefined,
           par:USR||'(non renseigné)',t:new Date().toISOString(),
           commandes: canal ? A.L.flatMap(x=>(x.cmds||[]).map(c=>c.cleCmd)) : undefined};
  /* une vente de canal importée a sa facture, comme celles qui arrivent toutes seules */
  if(f.sens==='vente'&&typeof docAutoPour==='function') f.doc=docAutoPour(f,FACT);
  if(f.lignes.some(l=>pcVendDe(l)>0)) f.pcShopify={etat:'attente'};
  FACT.push(f);
  ecrit(K.mod,MOD); ecrit(K.hist,HIST); ecrit(K.vent,VENT); ecrit(K.frn,FRN); ecrit(K.cli,CLI); ecrit(K.fact,FACT);
  log({act:s?'reception':'vente',lib:(s?'réception facture ':(canal?'ventes '+tiers+' — export ':'vente facture '))+num+(canal?'':' — '+tiers),
       n:det.length,impact:Math.round(det.reduce((a,x)=>a+(x.ap-x.av)*(paEff(parBC[x.bc])||0),0)),
       det, note:A.neg?`${A.neg} ligne(s) avec stock insuffisant`:undefined});
  if(det_pc.length||nTest) log({act:'reception',lib:'part de Perfume City, réception facture '+num+' — '+det_pc.reduce((a,x)=>a+(x.ap-x.av),0)+' flacon(s) au stock de Perfume City'+(nTest?' + '+nTest+' en tester (vitrine)':''),n:det_pc.length,impact:0,det:det_pc});
  raz(); dessineListe(); dessineKpis();
  $('msg').textContent=(canal?`Ventes ${tiers} importées : ${lignes.length} référence${lignes.length>1?'s':''}${nCmd?` sur ${nf(nCmd)} ligne${nCmd>1?'s':''} de commande`:''}`:`Facture ${num} enregistrée : ${lignes.length} ligne${lignes.length>1?'s':''}`)+(A.stock?`, stock ${s?'+':'−'}${nf(A.unites)} unités`:'')+(nprix?`, ${nprix} prix d'achat mis à jour`:'')+'.';
  $('msg').className='msg ok';
  if(pcRate.length){ $('msg').className='msg'; $('msg').textContent+=' '+L3(`ATTENTION : le stock de Perfume City n'a pas pu être mis à jour dans l'ERP pour ${pcRate.length} parfum${pcRate.length>1?'s':''} (${pcRate.slice(0,3).join(', ')}${pcRate.length>3?'…':''}). Préviens Igal.`,`WARNING: Perfume City's stock could not be updated in the ERP for ${pcRate.length} perfume${pcRate.length>1?'s':''}. Tell Igal.`,`ATENCIÓN: no se pudo actualizar el stock de Perfume City en el ERP para ${pcRate.length} perfume${pcRate.length>1?'s':''}. Avisa a Igal.`); }
  if(f.pcShopify) pcEnvoiFacture(f.id);
};

/* ---------------- PERFUME CITY : la part d'une réception (Igal, 20 oct. 2026) ----------------
   « Quand Sam rentre une new order, il doit pouvoir dispatcher le stock sur la boutique Perfume City : sur 16 parfums,
   il en donne 6 à Perfume City, et le stock est mis à jour chez Perfume City et chez Perfumes Trade. »
   1. dans l'ERP, les flacons de Perfume City entrent dans SON stock (pc-stock-v1) et pas dans celui de Perfumes Trade ;
   2. sur Shopify, ils sont AJOUTÉS au stock actuel de la boutique (jamais écrasé), une seule fois par réception ;
   3. si l'envoi à Shopify échoue (hors ligne, parfum absent de la boutique…), l'ERP est déjà à jour, la facture le dit,
      et « Renvoyer à Shopify » refait l'envoi sans jamais compter deux fois. */
/* 3 nov. 2026 (Igal) : la même règle du tester que le transfert depuis la fiche — le premier flacon d'une référence livré à
   Perfume City part en vitrine, pas en vente ; la boutique n'en a qu'un, les livraisons suivantes entrent en entier. Le vendable
   entre dans son inventaire et part sur Shopify ; le tester est noté à part (testeurs-pc-v1), pour la feuille de comptage. */
const K_PC_TEST='testeurs-pc-v1';
const pcTestClef=bc=>String(bc||'').replace(/^0+/,'');
function pcTesteurs(){ const t=lit(K_PC_TEST,{}); return (t&&typeof t==='object'&&!Array.isArray(t))?t:{}; }
function pcPartage(bc,n){ const k=pcTestClef(bc); const deja=+((pcTesteurs()[k]||{}).n||0); const t=(deja>0||!(n>0))?0:1; return {k,t,vend:Math.max(0,n-t)}; }
function pcTestNote(bc,ref,dt){ try{ const T=pcTesteurs(), k=pcTestClef(bc); const n=Math.max(0,+((T[k]||{}).n||0)+dt);
    if(n) T[k]=Object.assign({},T[k]||{},{n,bc:String(bc||''),ref:ref||'',t:new Date().toISOString(),u:USR||'(non renseigné)'}); else delete T[k];
    ecrit(K_PC_TEST,T); }catch(e){} }
/* ce qui part sur Shopify pour une ligne : le vendable ; une facture d'avant cette règle (sans pcVend) envoie tout, comme à l'époque */
const pcVendDe=l=>l.pcVend!=null?+l.pcVend:+l.pc;
function pcAjouteErp(cle,n){
  try{
    const v=IDX[cle]; if(!v||!v[0]||!n||typeof pcsCarte!=='function'||typeof pcsSauve!=='function') return null;
    const m=pcsCarte(), k=pcsCle([v[0]]);
    const o=Object.assign({},m[k]||{bc:String(v[0]),nom:v[1],m:v[2],ml:(typeof ozDe==='function'?ozDe(cle):'')||'',ty:TY(cle),q:0,pa:null,pvr:null,pvw:null,cle:'b'+v[0]});
    const av=Math.round(+o.q||0), ap=Math.max(0,av+n);
    o.q=ap;
    if(!pcsSauve([pcsVers(o)])) return null;
    return {av,ap};
  }catch(e){ return null; }
}
const PC_ENVOI_EN_COURS=new Set();
/* l'appel au cockpit : { hors:true } (pas relié), { erreur } ou { lignes:[…] } ; annule=true retire au lieu d'ajouter */
async function pcPousse(f,annule){
  const lg=(f.lignes||[]).filter(l=>pcVendDe(l)>0&&l.bc);
  try{
    if(typeof CK_URL==='undefined'||typeof ckTok!=='function'||!ckTok()) return {hors:true};
    const r=await fetch(CK_URL+'/api/o/'+CK_ORG+'/shopify/stock-ajoute',{method:'POST',headers:{'Content-Type':'application/json',Authorization:'Bearer '+ckTok()},
      body:JSON.stringify({cle:annule?f.id+'-annule':f.id,items:lg.map(l=>({bc:l.bc,ajout:annule?-pcVendDe(l):pcVendDe(l),nom:l.ref}))})});
    const j=await r.json().catch(()=>({}));
    return r.ok?j:{erreur:j.erreur||('erreur '+r.status)};
  }catch(e){ return {erreur:L3("le cockpit ne répond pas","the cockpit is not responding","el cockpit no responde")}; }
}
async function pcEnvoiFacture(id){
  const f=FACT.find(x=>x.id===id); if(!f) return;
  const lg=(f.lignes||[]).filter(l=>pcVendDe(l)>0&&l.bc);
  if(!lg.length) return;
  const annule=false;
  if(PC_ENVOI_EN_COURS.has(id)) return; PC_ENVOI_EN_COURS.add(id);
  const maj=(o)=>{ const g=FACT.find(x=>x.id===id); if(!g) return; g.pcShopify=Object.assign({},o,{t:new Date().toISOString()}); try{ ecrit(K.fact,FACT); }catch(e){} };
  const dit=(txt,cls)=>{ const m=$('msg'); if(m){ m.textContent=txt; m.className='msg'+(cls?' '+cls:''); } };
  dit(L3('Facture enregistrée — envoi du stock à Perfume City (Shopify)…','Invoice saved — sending the stock to Perfume City (Shopify)…','Factura guardada — enviando el stock a Perfume City (Shopify)…'));
  const res=await pcPousse(f,false);
  PC_ENVOI_EN_COURS.delete(id);
  const nom=l=>l.nom||l.bc;
  if(res.hors||res.erreur){
    maj({etat:'echec',raison:res.hors?'hors ligne':res.erreur});
    dit(L3(`Facture enregistrée, le stock de Perfume City est à jour DANS L'ERP, mais PAS encore sur Shopify (${res.hors?"l'ERP n'est pas relié au cockpit":res.erreur}). Ouvre la facture et clique « Renvoyer à Shopify » : rien ne sera compté deux fois.`,
      `Invoice saved, Perfume City's stock is up to date IN THE ERP, but NOT yet on Shopify (${res.hors?'the ERP is not connected to the cockpit':res.erreur}). Open the invoice and click "Send again to Shopify": nothing will be counted twice.`,
      `Factura guardada, el stock de Perfume City está al día EN EL ERP, pero AÚN NO en Shopify (${res.hors?'el ERP no está conectado al cockpit':res.erreur}). Abre la factura y pulsa «Reenviar a Shopify»: nada se contará dos veces.`),'');
    log({act:'site',lib:(annule?'annulation':'réception')+' '+f.num+' : stock de Perfume City NON envoyé à Shopify ('+(res.hors?'hors ligne':res.erreur)+')',n:lg.length,impact:0,det:[]});
    dessineListe(); return;
  }
  const L=res.lignes||[];
  const bon=L.filter(l=>l.etat==='ok'||l.etat==='deja'), mal=L.filter(l=>!(l.etat==='ok'||l.etat==='deja'||l.etat==='ignore'));
  maj({etat:mal.length?'partiel':'ok',lignes:L.map(l=>({bc:l.bc,nom:l.nom,etat:l.etat,raison:l.raison,avant:l.avant,apres:l.apres}))});
  if(!mal.length) dit(L3(`Facture enregistrée — stock de Perfume City mis à jour sur Shopify (${bon.length} parfum${bon.length>1?'s':''}).`,`Invoice saved — Perfume City stock updated on Shopify (${bon.length} perfume${bon.length>1?'s':''}).`,`Factura guardada — stock de Perfume City actualizado en Shopify (${bon.length} perfume${bon.length>1?'s':''}).`),'ok');
  else dit(L3(`Facture enregistrée. Perfume City : ${bon.length} parfum${bon.length>1?'s':''} mis à jour sur Shopify, ${mal.length} PAS (${mal.slice(0,3).map(l=>nom(l)+' — '+(l.raison||l.etat)).join(' ; ')}${mal.length>3?'…':''}). Le stock de l'ERP, lui, est à jour.`,
    `Invoice saved. Perfume City: ${bon.length} perfume${bon.length>1?'s':''} updated on Shopify, ${mal.length} NOT (${mal.slice(0,3).map(l=>nom(l)+' — '+(l.raison||l.etat)).join('; ')}${mal.length>3?'…':''}). The ERP stock is up to date.`,
    `Factura guardada. Perfume City: ${bon.length} perfume${bon.length>1?'s':''} actualizado${bon.length>1?'s':''} en Shopify, ${mal.length} NO (${mal.slice(0,3).map(l=>nom(l)+' — '+(l.raison||l.etat)).join('; ')}${mal.length>3?'…':''}). El stock del ERP está al día.`),'');
  log({act:'site',lib:(annule?'annulation':'réception')+' '+f.num+' : stock de Perfume City envoyé à Shopify ('+bon.length+' ok'+(mal.length?', '+mal.length+' non':'')+')',n:bon.length,impact:0,det:[]});
  dessineListe();
}
/* le code de cette page est un module (à cause de pdf.js) : ce qui suit sert aux tests automatiques */
window.__F={get APERCU(){ return APERCU; }, get EDITS(){ return EDITS; }, qteEff, paEff, parBC, trouve, lit, $, pcsCarte, pcsCle, annule, detail};
function raz(){ TEXTE=''; APERCU=null; EDITS={}; REP={}; SWAP=false; INV_OK=false; AUTO_SWAP=0; TEXTE_VU=null; $('colle').value=''; $('apercu').innerHTML=''; $('ok').disabled=true; $('ok').textContent=libelleBouton(); $('txt').classList.remove('on');
  ['tiers','date','num'].forEach(id=>{ $(id).value=''; $(id).classList.remove('auto'); $('a-'+id).hidden=true; });
  $('dev').value='USD'; $('taux').value=''; $('frais').value=''; $('a-dev').hidden=true; DEV_CHOISIE=false; majDevise();
  $('dz').classList.remove('lu'); $('dz').querySelector('b').textContent='Dépose la facture ici — PDF ou photo —, ou clique pour la choisir'; }
$('raz').onclick=()=>{ raz(); $('msg').textContent=''; };

/* ---------------- annulation d'une facture ---------------- */
async function annule(id){
  /* annuler une facture défait du stock et de l'historique des prix : réservé au
     Patron et à l'Admin (droit « annuler »), pas à celui qui a saisi la vente */
  if(!peut('annuler')){ alert("Annuler une facture est réservé au Patron et à l'Admin."); return; }
  const i=FACT.findIndex(f=>f.id===id); if(i<0) return;
  const f=FACT[i];
  if(f.id.startsWith('seed-')){ alert("Cette facture a été installée avec le catalogue et n'a pas touché au stock : rien à annuler."); return; }
  if(!confirm(`Annuler la facture ${f.num} (${f.tiers}) ?\n\nLe stock revient à ce qu'il était, les prix enregistrés par cette facture sont retirés de l'historique. L'opération est inscrite au journal.`)) return;
  /* la part de Perfume City est retirée de SON stock sur Shopify AVANT de toucher l'ERP : si Shopify ne répond pas, on le dit
     et on laisse choisir, plutôt que de défaire l'ERP à moitié sans le dire */
  if(f.sens==='achat'&&f.stock&&(f.lignes||[]).some(l=>pcVendDe(l)>0&&l.bc)){
    const res=await pcPousse(f,true);
    const mal=(res.hors||res.erreur)?[{raison:res.hors?L3("l'ERP n'est pas relié au cockpit","the ERP is not connected to the cockpit","el ERP no está conectado al cockpit"):res.erreur}]
      :(res.lignes||[]).filter(l=>!['ok','deja','ignore','absent'].includes(l.etat));
    if(mal.length&&!confirm(L3(`Le stock de Perfume City n'a pas pu être retiré sur Shopify (${mal[0].raison||mal[0].etat}${mal.length>1?' …':''}).\n\nAnnuler quand même la facture dans l'ERP ? Le stock de Perfume City sur Shopify sera alors à corriger à la main.`,
        `Perfume City's stock could not be reduced on Shopify (${mal[0].raison||mal[0].etat}${mal.length>1?' …':''}).\n\nCancel the invoice in the ERP anyway? Perfume City's stock on Shopify will then need fixing by hand.`,
        `No se pudo restar el stock de Perfume City en Shopify (${mal[0].raison||mal[0].etat}${mal.length>1?' …':''}).\n\n¿Anular la factura en el ERP de todos modos? El stock de Perfume City en Shopify habrá que corregirlo a mano.`))) return;
  }
  demandeUser();
  const det=[], detPc=[];
  f.lignes.forEach(l=>{
    if(f.stock&&l.qAp!==l.qAv){ const cur=qteEff(l.cle), nv=Math.max(0,cur-(l.qAp-l.qAv));
      MOD[l.cle]=Object.assign({},MOD[l.cle]||{},{qte:nv}); det.push({bc:l.bc,ref:l.ref,av:cur,ap:nv}); }
    if(f.sens==='achat'&&f.stock&&l.pc>0){ const v=pcVendDe(l); const pr=v>0?pcAjouteErp(l.cle,-v):null; if(pr) detPc.push({bc:l.bc,ref:l.ref,av:pr.av,ap:pr.ap}); if(l.pcT) pcTestNote(l.bc,l.ref,-l.pcT); }
    if(f.sens==='achat'){ if(HIST[l.cle]) HIST[l.cle]=HIST[l.cle].filter(x=>x.num!==f.num);
      if(l.paAp!==l.paAv && paEff(l.cle)===l.paAp){ MOD[l.cle]=Object.assign({},MOD[l.cle]||{},{pa:l.paAv});
        log({act:'prix',lib:"prix d'achat rétabli (facture "+f.num+" annulée)",bc:l.bc,ref:l.ref,av:l.paAp,ap:l.paAv}); } }
    else if(VENT[l.cle]) VENT[l.cle]=VENT[l.cle].filter(x=>x.num!==f.num);
  });
  if(f.commandes){ f.commandes.forEach(k=>{ delete CMD[k]; }); ecrit(K_CMD,CMD); }
  FACT.splice(i,1);
  ecrit(K.mod,MOD); ecrit(K.hist,HIST); ecrit(K.vent,VENT); ecrit(K.fact,FACT);
  log({act:'annulation',lib:'facture annulée '+f.num+' — '+f.tiers,n:det.length,impact:0,det});
  if(detPc.length) log({act:'annulation',lib:'facture annulée '+f.num+' — stock de Perfume City remis comme avant',n:detPc.length,impact:0,det:detPc});
  dessineListe(); dessineKpis();
}

/* ---------------- liste et chiffres ---------------- */
const dfr=d=>{ if(!d) return '—'; const [a,m,j]=d.split('-'); return `${m}/${j}/${a.slice(2)}`; };
/* ---------------- LE DETAIL D'UNE FACTURE ----------------
   La liste disait combien de lignes et combien d'argent, jamais QUOI. Pour savoir
   ce qu'il y avait dans une reception, il fallait rouvrir le PDF d'origine — quand
   on l'avait encore. Le detail est pourtant deja enregistre, ligne par ligne, avec
   le stock avant et apres : il ne manquait que de l'afficher. */
function detail(id){
  const f=FACT.find(x=>x.id===id); if(!f) return;
  const achat=f.sens==='achat';
  const u=f.lignes.reduce((a,l)=>a+(l.q||0),0);
  { const lg=(typeof LANG==='string')?LANG:'fr', t3=(fr,en,es)=>lg==='en'?en:lg==='es'?es:fr;   /* 28 sept. : « Achat » restait en français */
    const d=$('d-num'); d.setAttribute('data-nolang','');
    d.textContent=(achat?t3('Achat ','Purchase ','Compra '):(f.export?t3('Ventes importées ','Imported sales ','Ventas importadas '):t3('Vente ','Sale ','Venta ')))+(f.num||''); }
  $('d-sous').innerHTML=`<b>${esc(f.tiers)}</b> · ${dfr(f.d)} · ${nf(f.lignes.length)} référence${f.lignes.length>1?'s':''}`
    +` · ${nf(u)} unité${u>1?'s':''}`+(f.canal?` · canal ${esc(f.canal)}`:'')
    +(f.par?` · saisi par ${esc(f.par)}`:'')
    +(f.stock?'':' · <b style="color:var(--warn)">stock non modifié</b>')
    +(f.devise==='EUR'?` · facture en euros : <span data-nolang>${nf(Math.round(f.montantDevise||0))} € × ${String(f.taux).replace('.',',')}</span>`:'')
    +(f.frais?` · ${money(f.frais)} de frais d'arrivée`:'');
  $('d-corps').innerHTML=`<div style="overflow-x:auto"><table><thead><tr>
      <th>Référence</th><th class="r">Qté</th><th class="r">Prix unité</th><th class="r">Total ligne</th>
      ${f.stock?'<th class="r">Stock</th>':''}</tr></thead><tbody>
    ${f.lignes.map(l=>{
      /* le stock avant → apres est garde a l'enregistrement : c'est la seule trace
         de ce que cette facture a REELLEMENT fait, meme si le stock a bouge depuis */
      const bouge=(l.qAv!=null&&l.qAp!=null)?`<span class="stk">${nf(l.qAv)} → <b>${nf(l.qAp)}</b></span>`
                 :'<span class="stk">—</span>';
      return `<tr><td><b>${esc(l.ref||l.des||'—')}${tyVu(l)}</b><small>${esc(l.bc||'')}</small>
          ${l.pc>0?`<small style="color:#c2417f">${L3(`dont ${nf(l.pc)} pour Perfume City`,`of which ${nf(l.pc)} for Perfume City`,`de los cuales ${nf(l.pc)} para Perfume City`)}${l.pcT?' ('+L3(`${nf(l.pcT)} en tester`,`${nf(l.pcT)} as tester`,`${nf(l.pcT)} como tester`)+')':''}</small>`:''}
          ${l.manque?`<small style="color:var(--crit)">vendu à découvert : ${nf(l.manque)} de plus que le stock</small>`:''}</td>
        <td class="r">${nf(l.q||0)}</td>
        <td class="r">${l.p!=null?money2(l.p):'—'}</td>
        <td class="r"><b>${money2((l.q||0)*(l.p||0))}</b></td>
        ${f.stock?`<td class="r">${bouge}</td>`:''}</tr>`; }).join('')}
    </tbody></table></div>`+(()=>{
      const P=f.pcShopify; if(!f.lignes.some(l=>l.pc>0)) return '';
      const uPC=f.lignes.reduce((a,l)=>a+(l.pc||0),0);
      const etat=!P||P.etat==='attente'?L3('envoi à Shopify en cours ou non fait','sending to Shopify in progress or not done','envío a Shopify en curso o no hecho')
        :P.etat==='ok'?L3('stock envoyé à Shopify','stock sent to Shopify','stock enviado a Shopify')
        :P.etat==='partiel'?L3('envoyé à Shopify pour une partie des parfums seulement','sent to Shopify for some perfumes only','enviado a Shopify solo para una parte de los perfumes')
        :L3('PAS envoyé à Shopify','NOT sent to Shopify','NO enviado a Shopify');
      const mal=((P&&P.lignes)||[]).filter(l=>!['ok','deja','ignore'].includes(l.etat));
      return `<p class="repnote" id="d-pc"><b>${L3('Perfume City','Perfume City','Perfume City')} : ${nf(uPC)} ${L3('flacon(s)','bottle(s)','frasco(s)')}</b> — ${etat}.`
        +(mal.length?`<br>${mal.slice(0,6).map(l=>esc((l.nom||l.bc)+' — '+(l.raison||l.etat))).join('<br>')}`:'')
        +(P&&P.etat==='ok'?'':` <button type="button" class="btn" id="d-pc-renvoi" style="margin-left:8px">${L3('Renvoyer à Shopify','Send again to Shopify','Reenviar a Shopify')}</button>`)+`</p>`; })();
  { const b=$('d-pc-renvoi'); if(b) b.onclick=async()=>{ b.disabled=true; await pcEnvoiFacture(f.id); $('dov').classList.remove('on'); detail(f.id); }; }
  $('d-tot').innerHTML=`<span>${nf(u)} unité${u>1?'s':''}</span>`
    +`<span>Total <b>${money2(f.montant)}</b></span>`;
  /* Igal, 24 oct. 2026 : « comment je fais pour changer le nom du fournisseur ? » — sur une réception déjà enregistrée,
     le nom se corrige ici (Patron/Admin, comme l'annulation) : la réception, l'historique des prix d'achat et la liste des
     fournisseurs suivent ; rien d'autre ne bouge (stock, prix, lignes). Le Journal garde l'avant et l'après. */
  if(achat&&!f.id.startsWith('seed-')&&peut('annuler')){
    const b=document.createElement('button'); b.type='button'; b.className='btn'; b.id='d-frn'; b.style.marginLeft='8px';
    b.textContent=L3('Changer le fournisseur','Change the supplier','Cambiar el proveedor');
    $('d-sous').appendChild(b);
    b.onclick=()=>{
      const z=document.createElement('span'); z.id='d-frn-z'; z.style.cssText='display:inline-flex;gap:6px;align-items:center;margin-left:8px';
      z.innerHTML=`<input id="d-frn-nom" value="${esc(f.tiers||'')}" style="padding:6px 8px;border:1px solid var(--line);border-radius:7px;min-width:220px" list="d-frn-liste">
        <datalist id="d-frn-liste">${Object.keys(FRN||{}).sort().map(n=>`<option value="${esc(n)}">`).join('')}</datalist>
        <button type="button" class="btn pri" id="d-frn-ok">${L3('Enregistrer','Save','Guardar')}</button><button type="button" class="btn" id="d-frn-ann">${L3('Annuler','Cancel','Cancelar')}</button>`;
      b.replaceWith(z); const i=$('d-frn-nom'); i.focus(); i.select();
      $('d-frn-ann').onclick=()=>detail(f.id);
      const ok=()=>{ const nv=i.value.trim(); if(!nv){ i.focus(); return; } const av=f.tiers||'';
        if(nv===av){ detail(f.id); return; }
        f.tiers=nv;
        try{ Object.keys(HIST).forEach(c=>(HIST[c]||[]).forEach(h=>{ if(h&&h.num===f.num&&h.src==='facture'&&h.f===av) h.f=nv; })); }catch(e){}
        if(!FRN[nv]) FRN[nv]=Object.assign({nom:nv},{maj:new Date().toISOString()});
        ecrit(K.fact,FACT); ecrit(K.hist,HIST); ecrit(K.frn,FRN);
        log({act:'reception',lib:'fournisseur changé sur la réception '+(f.num||''),ref:f.num||'',av,ap:nv,n:0,impact:0,det:[]});
        try{ dessineListe(); }catch(e){} detail(f.id); };
      $('d-frn-ok').onclick=ok; i.addEventListener('keydown',e=>{ if(e.key==='Enter') ok(); });
    };
  }
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
/* ---- les factures de vente, toutes, en ligne ---- */
const FMODES_L={zelle:'Zelle',carte:'Carte',especes:'Espèces',virement:'Virement',credit:'Crédit',enligne:'Payé en ligne',caisse:'Payé à la caisse'};
function paieDe(f){
  if(f.retour) return `<span class="du">remboursé</span>`;
  const D=f.doc; if(!D) return f.auto?'<span class="ok">payé</span>':'<span style="color:var(--ink-3)">—</span>';
  const m=FMODES_L[D.pmode]||D.pmode||'';
  if((D.reste||0)<=0) return `<span class="ok">payé</span>${m?' · '+esc(m):''}`;
  if((+D.regle||0)>0) return `<span class="du">acompte ${money2(D.regle)}</span> · reste ${money2(D.reste)}`;
  return `<span class="du">à payer</span> · ${money2(D.reste)}${m?' · '+esc(m):''}`;
}
function dessineFactures(){
  const q=String($('fq').value||'').trim().toLowerCase(), canal=$('fcanal').value, per=+$('fper').value;
  const lim=per?isoJour(new Date(Date.now()-per*864e5)):null;
  const V=FACT.filter(f=>f&&f.sens==='vente'&&!(f.doc&&f.doc.type==='devis'));
  /* les canaux qu'on a vus, pour le filtre */
  const CS=[...new Set(V.map(f=>(f.canal||'').trim()).filter(Boolean))].sort((a,b)=>a.localeCompare(b,'fr'));
  const sel=$('fcanal'); if(sel.options.length!==CS.length+1){ const cur=sel.value; sel.innerHTML='<option value="">Tous les canaux</option>'+CS.map(c=>`<option value="${esc(c)}">${esc(c)}</option>`).join(''); sel.value=cur; }
  const L=V.filter(f=>(!canal||(f.canal||'').trim()===canal)&&(!lim||(f.d||'')>=lim)
      &&(!q||[f.tiers,f.num,f.doc&&f.doc.num,f.canal,String(Math.round(Math.abs(f.montant||0)))].some(v=>String(v||'').toLowerCase().includes(q))))
    .sort((a,b)=>(b.d||'').localeCompare(a.d||'')||(b.h||'').localeCompare(a.h||'')||(b.t||'').localeCompare(a.t||''));
  const tot=L.reduce((a,f)=>a+(f.montant||0),0);
  $('fnb').textContent=L.length?`${nf(L.length)} facture${L.length>1?'s':''} · ${money(tot)}`:'';
  if(!L.length){ $('factures').innerHTML=`<div class="vide"><p>${V.length?'Aucune facture ne correspond.':'Aucune facture de vente pour l\'instant. Elles apparaîtront ici toutes seules, à chaque vente enregistrée — site, Amazon, caisse, boutique, gros.'}</p></div>`; return; }
  const heure=f=>f.h||(f.t&&typeof heureMiami==='function'?heureMiami(f.t):'');
  /* colonnes secondaires o1 → o5 : elles s'effacent si le tableau ne tient pas (voir « af », _menu.py) */
  $('factures').innerHTML=`<div class="af"><table class="flt"><thead><tr>
    <th>Date</th><th class="o3">Heure</th><th>N° facture</th><th>Client</th><th class="o4">Canal</th><th class="r o2">Parfums</th><th class="r">Montant</th><th class="o5">Paiement</th><th class="o1">Par</th><th></th></tr></thead><tbody>${
    L.slice(0,300).map(f=>{ const u=(f.lignes||[]).reduce((a,l)=>a+Math.abs(l.q||0),0);
      return `<tr class="cl" data-d="${esc(f.id)}" title="Voir ce qui a bougé en stock">
        <td>${dfr(f.d)}</td><td class="hh o3">${esc(heure(f)||'—')}</td>
        <td class="num"><b>${esc(f.doc?f.doc.num:(f.num||'—'))}</b>${f.doc&&f.num&&f.num!==f.doc.num?`<span style="display:block;font-size:11px;color:var(--ink-3)">commande ${esc(f.num)}</span>`:''}${f.retour?' <span class="tg ret">retour</span>':''}</td>
        <td class="cli" data-nolang>${esc(f.tiers||'—')}</td><td class="o4"><span data-nolang>${esc(f.canal||'—')}</span></td>
        <td class="r o2">${nf(u)}</td><td class="r"><b>${money2(f.montant||0)}</b></td>
        <td class="o5">${paieDe(f)}</td><td class="o1" style="color:var(--ink-3);font-size:12px" data-nolang>${esc(f.par||'')}</td>
        <td class="r">${f.doc?`<a class="btn" href="ventes.html#doc=${encodeURIComponent(f.id)}">Voir</a><a class="btn" href="ventes.html#doc=${encodeURIComponent(f.id)}&edit=1">Modifier</a>`:`<button class="btn" data-det="${esc(f.id)}">Détail</button>`}${(f.id.startsWith('seed-')||!peut('annuler'))?'':`<button class="x" data-x="${esc(f.id)}">Annuler</button>`}</td></tr>`; }).join('')}</tbody></table>${L.length>300?`<p class="flaide">… et ${nf(L.length-300)} de plus ; affine avec la recherche ou la période.</p>`:''}</div>`;
  $('factures').querySelectorAll('[data-x]').forEach(b=>b.onclick=e=>{ e.stopPropagation(); annule(b.dataset.x); });
  $('factures').querySelectorAll('[data-det]').forEach(b=>b.onclick=e=>{ e.stopPropagation(); detail(b.dataset.det); });
  $('factures').querySelectorAll('a.btn').forEach(a=>a.onclick=e=>e.stopPropagation());
  $('factures').querySelectorAll('tr.cl').forEach(tr=>tr.onclick=()=>detail(tr.dataset.d));
}
['fq','fcanal','fper'].forEach(i=>$(i).addEventListener('input',dessineFactures));

function dessineListe(){
  dessineFactures();
  const L=FACT.filter(f=>f&&f.sens==='achat').sort((a,b)=>(b.d||'').localeCompare(a.d||'')||(b.t||'').localeCompare(a.t||''));
  $('nbf').textContent=L.length?`${nf(L.length)} · réceptions de marchandise, la plus récente en premier`:'';
  if(!L.length){ $('liste').innerHTML=`<div class="vide"><p>Aucun achat enregistré. Dépose une facture fournisseur ci-dessus : le stock, les prix et la fiche du fournisseur se mettront à jour tout seuls.</p></div>`; return; }

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
  $('src').innerHTML=`${nf(ach.length)} facture${ach.length>1?'s':''} fournisseur${ach.length>1?'s':''}<br>lecture PDF locale`;
}
majUser(); $('sfoot').innerHTML='factures fournisseurs<br>le stock augmente';
majSens(); dessineListe(); dessineKpis();
if(!$('date').value) $('date').value='';
/* le script de page est un module : ses fonctions ne sont pas globales. Le bouton « Support technique » du menu appelle aidOuvre() depuis un onclick : sans cette ligne il ne faisait RIEN sur cette page (trouvé par _test_aide.py, 15 oct. 2026). */
if(typeof aidOuvre==='function') window.aidOuvre=aidOuvre;
'''

html = coquille("Factures", "Factures",
  "Les factures des fournisseurs, quand la marchandise arrive. Déposée ici, une facture ajoute les "
  "quantités reçues au stock, met à jour le prix d'achat, la fiche du fournisseur et le journal. "
  "Les factures de vente sont dans Ventes.",
  CSS, CORPS.replace("__ACCEPT__", _lire.ACCEPT), JS.replace('__NOMS__', _noms.NOMS), donnees=('produits',)).replace('__IDX__', 'Object.fromEntries(D_TOUS().map(r=>[r[15],[r[0],r[13],r[2],r[12],r[6],r[8],r[7],r[4],r[5]]]))')
# Le script de page reste un module (historique : pdf.js était embarqué ici ; il ne l est plus,
# mais les tests et le code comptent sur ce mode module).
import re as _re
# La coquille ouvre son script par VER_URL puis $ : on coupe juste avant, quoi
# qu'il y ait entre les deux, pour ne rien perdre en chemin.
_m = _re.search(r'<script type="text/plain" id="page-js">\n(const VER_URL=[^\n]*\n)?const \$=i=>document\.getElementById\(i\);', html)
assert _m, "ancre du script de page introuvable"
html = (html[:_m.start()]
        + '<script type="text/plain" id="page-js" data-module="1">\n' + (_m.group(1) or '')
        + 'const $=i=>document.getElementById(i);'
        + html[_m.end():])
assert 'data-module="1"' in html
open('factures.html','w').write(html)
print('factures.html',len(html)//1024,'Ko')
