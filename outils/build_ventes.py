# -*- coding: utf-8 -*-
"""Journal des ventes : chaque vente, avec le canal sur lequel elle a été faite.
Il se nourrit des factures de vente et des exports de canaux enregistrés dans factures.html."""
import json
from build_crm import coquille
import _facture
import _lire, _noms
import _donnees
C = json.load(open('cat.json'))
# cle -> [code-barres, nom, marque, contenance, prix d'achat, prix retail, prix gros, quantité]
IDX = {r[15]: [r[0], r[13], r[2], r[3], r[12], r[7], r[8], r[6]] for r in C}

CSS = r'''

.sous{margin:5px 0 0;font-size:14px;color:var(--ink-2);max-width:74ch;line-height:1.5}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(165px,1fr));gap:1px;
background:var(--line-2);border:1px solid var(--line);border-radius:9px;overflow:hidden;
margin-bottom:20px;box-shadow:0 1px 2px rgba(0,0,0,.04)}
.kpi{background:var(--surface);padding:15px 17px;display:flex;flex-direction:column;gap:3px}
.kpi .v{font-family:Inter,sans-serif;font-size:24px;font-weight:700;line-height:1;
letter-spacing:-.03em;font-variant-numeric:tabular-nums}
.kpi .v.g{color:var(--good)} .kpi .v.c{color:var(--crit)}
.kpi .k{font-size:12px;color:var(--ink-3);line-height:1.4}
.tools{display:flex;gap:9px;flex-wrap:wrap;align-items:center;margin-bottom:16px}
.tools .sp{margin-left:auto}
.srch{position:relative;flex:1 1 220px;max-width:340px}
.srch input{width:100%;padding:9px 12px 9px 33px;font-family:inherit;font-size:13.5px;
border:1px solid var(--line);border-radius:7px;background:var(--surface);color:var(--ink)}
.srch input:focus{outline:0;border-color:var(--iris);box-shadow:0 0 0 3px var(--iris-soft)}
.srch::before{content:"⌕";position:absolute;left:11px;top:50%;transform:translateY(-50%);
color:var(--ink-3);font-size:16px}
.sel{padding:9px 11px;font-family:inherit;font-size:13.5px;border:1px solid var(--line);
border-radius:7px;background:var(--surface);color:var(--ink);cursor:pointer}
.sel:focus{outline:0;border-color:var(--iris)}
h2.sec{font-size:15px;font-weight:700;letter-spacing:-.01em;margin:26px 0 10px;display:flex;
align-items:baseline;gap:10px}
h2.sec em{font-style:normal;font-family:Inter,sans-serif;font-size:12px;color:var(--ink-3);font-weight:500}

.tbl{width:100%;border-collapse:collapse;font-size:14.5px;background:var(--surface);
border:1px solid var(--line);border-radius:9px;overflow:hidden}
.tbl th{text-align:left;font-family:Inter,sans-serif;font-size:11px;letter-spacing:.11em;
text-transform:uppercase;color:var(--ink-2);font-weight:700;padding:11px 12px;
background:var(--surface-2);border-bottom:1px solid var(--line);white-space:nowrap}
.tbl th.r,.tbl td.r{text-align:right;font-variant-numeric:tabular-nums}
.tbl td{padding:10px 12px;border-bottom:1px solid var(--line-2);vertical-align:middle}
.tbl tbody tr:last-child td{border-bottom:0}
.tbl tbody tr:hover{background:var(--surface-2)}
.tbl tfoot td{background:var(--surface-2);font-weight:700;border-top:2px solid var(--line)}
.qd{font-family:Inter,sans-serif;font-size:14px;font-weight:600;white-space:nowrap;color:var(--ink)}
.qd small{display:block;font-weight:400;font-size:12.5px;color:var(--ink-3)}
.ref b{display:block;font-weight:600;line-height:1.3}
.ref span{color:var(--ink-3);font-family:Inter,sans-serif;font-size:12.5px}
.num{font-family:Inter,sans-serif;font-size:13px;color:var(--ink-2);white-space:nowrap}
.num small{display:block;color:var(--ink-3)}
.who{font-size:13.5px;color:var(--ink-2);white-space:nowrap}
.who.anon{color:var(--ink-3);font-style:italic}
.mt{font-weight:700;color:var(--ink)}
.mg{font-family:Inter,sans-serif;font-weight:700;font-size:14px;white-space:nowrap}
.mg.g{color:var(--good)} .mg.w{color:var(--warn)} .mg.c{color:var(--crit)} .mg.na{color:var(--ink-3);font-weight:400}

/* pastille de canal : une couleur par canal, stable */
.ch{display:inline-flex;align-items:center;gap:6px;font-size:11.5px;font-weight:700;
padding:4px 10px 4px 8px;border-radius:20px;white-space:nowrap;line-height:1;letter-spacing:.01em;
background:var(--surface-2);color:var(--ink-2);border:1px solid var(--line)}
.ch::before{content:"";width:7px;height:7px;border-radius:50%;background:var(--c,var(--ink-3))}
.ch.c0{--c:#5B4B8A}.ch.c1{--c:#2C6E4E}.ch.c2{--c:#B4530A}.ch.c3{--c:#1F6FB2}.ch.c4{--c:#A4262C}
.ch.cpc{--c:#E0457F;background:#FDEDF3;color:#9A2A56;border-color:#F4B8CF}
.ch.c5{--c:#8A5A00}.ch.c6{--c:#4C7C8A}.ch.c7{--c:#7A4E9E}.ch.na{--c:transparent;border-style:dashed;color:var(--ink-3);font-weight:500}

/* Par canal : un onglet par canal, avec son logo (l'icône du site du canal, jamais
   redessinée ici) et l'essentiel — la part, le montant, la marge en petit.
   Igal, 12 sept. 2026 : « de plus beaux onglets, avec les logos des canaux ». */
.par{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:6px}
.pc{flex:1 1 220px;max-width:330px;background:var(--surface);border:1px solid var(--line);border-radius:10px;
padding:9px 12px 10px;display:flex;gap:10px;align-items:flex-start;cursor:pointer;transition:border-color .12s;
position:relative;overflow:hidden;min-width:0}
.pc:hover{border-color:var(--iris)}
.pc.on{border-color:var(--iris);box-shadow:0 0 0 3px var(--iris-soft)}
.pc .lg{width:30px;height:30px;border-radius:8px;background:var(--surface-2);border:1px solid var(--line-2);
display:flex;align-items:center;justify-content:center;flex:none;margin-top:1px}
.pc .lg img{width:18px;height:18px;border-radius:3px;display:block}
.pc .lg i{font-style:normal;font-size:15px;line-height:1}
.pc .tx{min-width:0;flex:1}
.pc .t{display:flex;justify-content:space-between;align-items:baseline;gap:8px}
.pc .cn{font-size:12px;font-weight:700;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;letter-spacing:-.01em}
.pc .pct{font-family:Inter,sans-serif;font-size:11px;color:var(--ink-3);font-weight:700;flex:none}
.pc .ca{font-family:Inter,sans-serif;font-size:19px;font-weight:800;letter-spacing:-.03em;line-height:1.15;margin:1px 0 2px}
.pc .d{font-size:11px;color:var(--ink-3);line-height:1.4}
.pc .d b{font-weight:600}
.pc .d a{color:var(--warn);text-decoration:none;border-bottom:1px dotted var(--warn)}
.pc .bar{position:absolute;left:0;right:0;bottom:0;height:3px;background:var(--line-2)}
.pc .bar i{display:block;height:100%;background:var(--c,var(--iris))}
.pc.c0{--c:#5B4B8A}.pc.c1{--c:#2C6E4E}.pc.c2{--c:#B4530A}.pc.c3{--c:#1F6FB2}.pc.c4{--c:#A4262C}
.pc.cpc{--c:#E0457F}.pc.c5{--c:#8A5A00}.pc.c6{--c:#4C7C8A}.pc.c7{--c:#7A4E9E}.pc.na{--c:var(--ink-3)}

.wrapx{overflow-x:auto}
.vide{border:2px dashed var(--line);border-radius:11px;padding:38px 30px;text-align:center;
background:var(--surface-2);max-width:66ch;margin:24px auto}
.vide h3{margin:0 0 10px;font-size:19px;font-weight:700;letter-spacing:-.02em}
.vide p{margin:0 0 12px;font-size:14px;color:var(--ink-2);line-height:1.65}
.info{background:var(--iris-soft);border-left:3px solid var(--iris);border-radius:0 8px 8px 0;
padding:12px 16px;font-size:13px;color:var(--ink-2);line-height:1.6;margin-bottom:20px;max-width:88ch}
.info b{color:var(--ink)}
.plus{display:block;width:100%;margin-top:14px;padding:12px;background:var(--surface);
border:1px solid var(--line);border-radius:8px;font-family:inherit;font-size:13.5px;
color:var(--ink-2);cursor:pointer;font-weight:500}
.plus:hover{border-color:var(--iris);color:var(--iris)}

/* numéro de ligne */
.tbl td.no,.tbl th.no{width:42px;text-align:right;color:var(--ink-3);font-family:Inter,sans-serif;
font-size:12.5px;font-variant-numeric:tabular-nums;padding-right:6px}


/* le message d'un client, collé tel quel */
.msgz{display:flex;flex-direction:column;gap:5px}
.msgz textarea{font-family:inherit;font-size:14px;line-height:1.55;color:var(--ink);
background:var(--surface-2);border:1px solid var(--line);border-radius:9px;padding:11px 13px;
min-height:150px;resize:vertical;width:100%}
.msgz textarea:focus{outline:0;border-color:var(--iris);background:var(--surface);
box-shadow:0 0 0 3px var(--iris-soft)}
.mtb{width:100%;border-collapse:collapse;font-size:13.5px}
.mtb th{text-align:left;font-family:Inter,sans-serif;font-size:10px;letter-spacing:.09em;
text-transform:uppercase;color:var(--ink-3);font-weight:800;padding:0 6px 6px;border-bottom:1px solid var(--line)}
.mtb td{padding:8px 6px;border-bottom:1px solid var(--line-2);vertical-align:top}
.mtb td.r{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
.mtb .brut{display:block;font-size:11.5px;color:var(--ink-3);margin-top:2px;font-style:italic}
.mtb input[type=number]{width:64px;font:inherit;font-size:13.5px;text-align:right;
background:var(--surface-2);border:1px solid var(--line);border-radius:6px;padding:5px 7px}
.mtb select{width:100%;max-width:330px;font:inherit;font-size:13px;background:var(--surface-2);
border:1px solid var(--line);border-radius:7px;padding:6px 8px}
.mtb tr.sur td{background:var(--warn-soft)}
.mtb tr.non td{background:var(--crit-soft)}
.msur{display:inline-block;padding:1px 8px;border-radius:99px;font-family:Inter,sans-serif;
font-size:10px;font-weight:800;letter-spacing:.05em;text-transform:uppercase}
.msur.ok{background:var(--good-soft);color:var(--good)}
.msur.hm{background:var(--warn-soft);color:var(--warn)}
.msur.no{background:var(--crit-soft);color:var(--crit)}
.mrap{background:var(--iris-soft);border-left:3px solid var(--iris);border-radius:0 8px 8px 0;
padding:11px 14px;font-size:13.5px;color:var(--ink-2);line-height:1.6}
.mrap b{color:var(--ink)}

/* le bouton d'action remonte à côté du titre */
.hact{display:flex;gap:8px;align-items:center;flex-wrap:wrap}
@media(max-width:700px){ .hact{width:100%} .hact .btn{width:100%;justify-content:center} }

/* le détail d'une vente : panneau à droite sur ordinateur, plein écran sur téléphone.
   Le tableau a douze colonnes : sur un téléphone on ne lit une ligne qu'en scrollant
   de côté. Ici tout redescend à la verticale, d'un seul coup d'œil. */
.tbl tbody tr{cursor:pointer}
.tbl tbody tr:hover td{background:var(--surface-2)}
.file tr.fl-row{cursor:pointer}
.file tr.fl-row:hover td{background:var(--surface-2)}
.fet{display:inline-block;font-family:Inter,sans-serif;font-size:10.5px;font-weight:800;letter-spacing:.06em;text-transform:uppercase;padding:2px 8px;border-radius:99px;margin-left:4px}
.fet.inc{background:var(--warn-soft);color:var(--warn)}
.fet.ok{background:var(--good-soft);color:var(--good)}
.blo.fl-inc{border-left:3px solid var(--warn);padding:10px 12px;background:var(--warn-soft);border-radius:0 8px 8px 0}
.dt tr.fl-manque td{background:var(--warn-soft)}
.fl-sel{display:block;margin-top:6px;max-width:100%;font:inherit;font-size:13px;padding:5px 8px;border:1px solid var(--line);border-radius:8px;background:var(--surface)}
.fl-choix{display:flex;flex-direction:column;gap:6px;margin-top:4px}
.fl-cherche{display:block;width:100%;max-width:440px;font:inherit;font-size:13px;padding:6px 9px;border:1px solid var(--iris);border-radius:8px;background:var(--surface)}
.fl-choix small{color:var(--ink-3)}
#fj[hidden]{display:none!important}
.dov{position:fixed;inset:0;background:rgba(23,23,29,.42);z-index:85;display:none}
/* 7 nov. 2026 : la fiche d'une vente en attente ouverte DANS UNE FENÊTRE depuis Tâches (ventes.html#attente=<id>&cadre=1) :
   on ne montre que le panneau, sans le menu ni le journal, comme la fiche du Catalogue en cadre */
html.cadre .side,html.cadre .legend{display:none!important}
html.cadre:not(.cp) body{visibility:hidden}
html.cadre .main{visibility:hidden}
html.cadre .dov{visibility:visible;background:transparent;backdrop-filter:none}
html.cadre .dt{width:100%;box-shadow:none}
html.cadre,html.cadre body{background:transparent}
/* le rappel de sauvegarde (en bas à droite) passait devant les boutons d'une fiche ouverte */
body:has(.dov.on) #svtem{display:none!important}
.dov.on{display:block}
.dt{position:absolute;top:0;right:0;bottom:0;width:min(580px,100%);background:var(--surface);
border-left:1px solid var(--line);box-shadow:-14px 0 46px rgba(0,0,0,.20);
display:flex;flex-direction:column;overflow:hidden}
.dt .dh{padding:15px 20px;border-bottom:1px solid var(--line);display:flex;gap:12px;align-items:flex-start}
.dt .dh h3{margin:0;font-size:18px;font-weight:800;letter-spacing:-.02em;flex:1;line-height:1.25}
.dt .dh .sub{display:block;font-family:Inter,sans-serif;font-size:11.5px;font-weight:500;
color:var(--ink-3);margin-top:4px;line-height:1.5}
.dt .dh .x{background:none;border:1px solid var(--line);border-radius:7px;font-size:17px;
color:var(--ink-2);cursor:pointer;line-height:1;padding:5px 10px;flex:none}
.dt .db{padding:2px 20px 24px;overflow-y:auto;flex:1}
.dt .df{padding:12px 20px;border-top:1px solid var(--line);background:var(--surface-2);
display:flex;gap:8px;flex-wrap:wrap;align-items:center}
.blo{margin-top:19px}
.blo>h4{margin:0 0 7px;font-family:Inter,sans-serif;font-size:10.5px;letter-spacing:.1em;
text-transform:uppercase;color:var(--ink);font-weight:800}
.blo table{width:100%;border-collapse:collapse;font-size:13px}
.blo td{padding:6px 5px;border-bottom:1px solid var(--line-2);vertical-align:top;line-height:1.4}
.blo td.r{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
.blo td small{display:block;font-size:11px;color:var(--ink-3)}
.blo tr.ici td{background:var(--iris-soft)}
.blo tr:last-child td{border-bottom:0}
.pl{display:flex;justify-content:space-between;gap:14px;padding:5px 0;font-size:13.5px;
border-bottom:1px solid var(--line-2)}
.pl span{color:var(--ink-2)} .pl b{font-variant-numeric:tabular-nums;white-space:nowrap}
.pl:last-child{border-bottom:0}
.pl.gr{padding-top:8px;font-weight:800;font-size:15px} .pl.gr span{color:var(--ink)}
.et{display:inline-block;padding:2px 9px;border-radius:99px;font-family:Inter,sans-serif;
font-size:10.5px;font-weight:800;letter-spacing:.05em;text-transform:uppercase}
.et.ok{background:var(--good-soft);color:var(--good)}
.et.no{background:var(--crit-soft);color:var(--crit)}
.et.mi{background:var(--warn-soft);color:var(--warn)}
.nt{font-size:12.5px;color:var(--ink-3);line-height:1.55;margin:7px 0 0}
/* la fiche d'une vente (Igal, 1er oct. 2026 : « mal fichu… il n'y a pas le prix d'achat… quand il y
   a plusieurs parfums ce n'est pas net ») : une carte par parfum, avec sa photo, son prix d'achat et
   ce qu'il rapporte ; puis le calcul de la marge de la commande, ligne par ligne */
.fv{display:flex;gap:12px;padding:12px;border:1px solid var(--line);border-radius:10px;margin-bottom:8px;background:var(--surface)}
.fv.ici{border-color:var(--iris);box-shadow:0 0 0 2px var(--iris-soft)}
.fv-ph{flex:none}
.fv-ph img,.fv-ph .vig0{width:58px;height:58px;object-fit:contain;border-radius:8px;background:#fff;border:1px solid var(--line-2);display:flex;align-items:center;justify-content:center;color:var(--ink-3)}
.fv-in{flex:1;min-width:0}
.fv-nom{font-weight:800;font-size:14px;line-height:1.3}
.fv-sub{font-size:11.5px;color:var(--ink-3);margin:2px 0 7px;font-variant-numeric:tabular-nums}
.fv-fiche{margin:0 0 8px;font-size:12px}
.fv-r{display:flex;justify-content:space-between;gap:10px;font-size:13px;padding:2px 0}
.fv-r span{color:var(--ink-2)} .fv-r b{font-variant-numeric:tabular-nums;white-space:nowrap;font-weight:600}
.fv-r.t{border-top:1px dashed var(--line);margin-top:4px;padding-top:5px} .fv-r.t b{font-weight:800}
.fv-moins{color:var(--crit)} .fv-plus{color:var(--good)}
.fv-manque{color:var(--crit);font-weight:700}
.fv-calc{border:1px solid var(--line);border-radius:10px;padding:6px 14px;background:var(--surface-2)}
.fv-calc .pl.tot{border-top:2px solid var(--ink);border-bottom:0;margin-top:3px;padding-top:9px;font-weight:800;font-size:16px}
.fv-calc .pl.tot span{color:var(--ink)}
@media(max-width:700px){ .dt{width:100%;border-left:0} .dt .db{padding:2px 16px 22px} }

/* saisie d'une vente */
.ov{position:fixed;inset:0;background:rgba(23,23,29,.5);z-index:80;display:none;
align-items:flex-start;justify-content:center;padding:34px 18px;overflow-y:auto}
.ov.on{display:flex}
.mod{background:var(--surface);border:1px solid var(--line);border-radius:11px;width:100%;
max-width:860px;box-shadow:0 18px 48px rgba(0,0,0,.22)}
.mod .mh{padding:18px 22px;border-bottom:1px solid var(--line);display:flex;align-items:center;gap:12px}
.mod .mh h3{margin:0;font-size:19px;font-weight:800;letter-spacing:-.02em;flex:1}
.mod .mh .x{background:none;border:1px solid var(--line);border-radius:7px;font-size:18px;
color:var(--ink-2);cursor:pointer;line-height:1;padding:5px 11px}
.mod .mb{padding:18px 22px;display:flex;flex-direction:column;gap:16px}
.mod .mf{padding:14px 22px;border-top:1px solid var(--line);display:flex;gap:9px;align-items:center;
flex-wrap:wrap;background:var(--surface-2);border-radius:0 0 11px 11px}
.mod .mf .msg{font-size:13px;color:var(--ink-3);margin-right:auto}
.mod .mf .msg.err{color:var(--crit)} .mod .mf .msg.ok{color:var(--good)}
.fg{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:13px}
.fg>*{min-width:0}   /* un menu déroulant aux options longues ne doit pas élargir la page (téléphone) */
.fld select,.fld input{max-width:100%}
.fld{display:flex;flex-direction:column;gap:5px}
.fld label{font-family:Inter,sans-serif;font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;
color:var(--ink);font-weight:800}
.fld input,.fld select{font-family:inherit;font-size:14px;color:var(--ink);background:var(--surface-2);
border:1px solid var(--line);border-radius:7px;padding:9px 11px;width:100%}
.fld input:focus,.fld select:focus{outline:0;border-color:var(--iris);background:var(--surface);
box-shadow:0 0 0 3px var(--iris-soft)}
.fld .aide{font-size:12px;color:var(--ink-3);line-height:1.4}
.rech{position:relative}
.res{position:absolute;top:calc(100% + 4px);left:0;right:0;max-height:260px;overflow-y:auto;z-index:5;
background:var(--surface);border:1px solid var(--line);border-radius:8px;box-shadow:0 10px 28px rgba(0,0,0,.14);display:none}
.res.on{display:block}
.res div{padding:9px 12px;cursor:pointer;border-bottom:1px solid var(--line-2);font-size:13.5px}
.res div:last-child{border-bottom:0}
.res div:hover,.res div.sel{background:var(--iris-soft)}
.res b{display:block;font-weight:600}
.res span{color:var(--ink-3);font-size:11.5px}
.pan{background:var(--surface-2);border:1px solid var(--line);border-radius:9px;overflow:hidden}
.qd .hh{font-size:12.5px;color:var(--ink-3);font-variant-numeric:tabular-nums}
.pan{overflow-x:auto;-webkit-overflow-scrolling:touch}   /* sur un téléphone, le tableau défile dans son cadre au lieu d'élargir la page */
.pan table{width:100%;border-collapse:collapse;font-size:13.5px}
.pan th{text-align:left;font-family:Inter,sans-serif;font-size:10.5px;letter-spacing:.09em;
text-transform:uppercase;color:var(--ink);font-weight:800;padding:9px 11px;border-bottom:1px solid var(--line)}
.pan th.r,.pan td.r{text-align:right;font-variant-numeric:tabular-nums}
.pan td{padding:8px 11px;border-bottom:1px solid var(--line-2);vertical-align:middle}
.pan tbody tr:last-child td{border-bottom:0}
.pan input.manque{border-color:var(--crit);box-shadow:0 0 0 2px rgba(179,38,30,.15)}
.pan input{width:74px;font-family:inherit;font-size:13.5px;padding:6px 8px;border:1px solid var(--line);
border-radius:6px;text-align:right;background:var(--surface)}
.pan .del{background:none;border:0;color:var(--ink-3);font-size:16px;cursor:pointer;padding:0 4px}
.pan .pucs{display:flex;gap:4px;justify-content:flex-end;margin-top:4px;flex-wrap:wrap}
.pan .puc{font-family:Inter,sans-serif;font-size:11px;border:1px solid var(--line);background:var(--surface);color:var(--ink-2);border-radius:999px;padding:2px 8px;cursor:pointer;white-space:nowrap}
.pan .puc b{font-weight:700}
/* 5 nov. 2026 (Igal : « enlève-moi les couleurs, je comprends rien ») : toutes les pastilles de prix ont le même aspect, aucune ne s'allume */
.pan .puc.on{background:var(--surface);border-color:var(--line);color:var(--ink-2)}
.pan .puc.dp,.pan .puc.dp.on{background:var(--surface);border-color:var(--line);color:var(--ink-2)}
.pan b.vfiche{cursor:pointer}.pan b.vfiche:hover{color:var(--iris);text-decoration:underline}
#v-q2w{margin-top:12px}
.pan .del:hover{color:var(--crit)}
.pan tfoot td{background:var(--surface);font-weight:700;border-top:2px solid var(--line)}
.pan .vide{padding:18px;text-align:center;color:var(--ink-3);font-size:13px}
.mgl{font-family:Inter,sans-serif;font-weight:700;font-size:12.5px}
.mgl.g{color:var(--good)} .mgl.w{color:var(--warn)} .mgl.c{color:var(--crit)} .mgl.na{color:var(--ink-3);font-weight:400}
/* retours et remboursements */
.tbl tr.ret td{background:var(--crit-soft)}
.tbl tr.ret .qd,.tbl tr.ret .mt{color:var(--crit)}
.chret{display:inline-block;font-family:Inter,sans-serif;font-size:10px;font-weight:800;letter-spacing:.07em;
text-transform:uppercase;padding:2px 7px;border-radius:99px;background:var(--crit);color:#fff;margin-left:6px}
.tbl td.act{text-align:right;white-space:nowrap}
/* le produit est ce qu'on lit en premier : il garde de la place */
.tbl th.pdt,.tbl td.pdt{min-width:190px}
.tbl td.num{max-width:140px;overflow-wrap:anywhere}
.tbl td.cli{min-width:110px;max-width:190px;overflow-wrap:anywhere}
/* sur un portable, le tableau reprend sa taille d'avant, sinon il déborde */
@media (max-width:1450px){ .chatt{font-size:9px;padding:1px 5px;letter-spacing:0} .tbl td.num{max-width:125px} .tbl th.pdt,.tbl td.pdt{min-width:160px} .tbl{font-size:13px} .tbl th{font-size:9.5px} .qd{font-size:12.5px} .ref span,.qd .hh,.num{font-size:11.5px} .mg{font-size:12.5px} .cliv{font-size:12px} }
/* la ligne d'un jour */
.tbl tr.jour td{background:var(--surface-2);border-top:2px solid var(--ink);border-bottom:1px solid var(--line);padding:9px 12px;cursor:default}
.tbl tr.jour:hover td{background:var(--surface-2)}
.tbl tr.jour .jd{font-weight:800;font-size:15px;margin-right:14px}
.tbl tr.jour .jn{font-family:Inter,sans-serif;font-weight:700;font-size:14px;color:var(--iris)}
.tbl tr.jour .jm{font-family:Inter,sans-serif;font-weight:700;font-size:14px;margin-left:14px}
.tbl tr.jour .ja{font-family:Inter,sans-serif;font-size:13px;color:var(--iris);margin-left:12px;font-weight:600}
/* une commande reçue, pas encore facturée */
/* Perfume City (boutique de Kim) : 17 oct. 2026 (Igal) « toute la bande rose des ventes n'est pas jolie, je préférerais
   qu'il n'y ait que Perfume City qui soit rose » → la ligne garde son fond normal ; seule la pastille du canal
   (et la carte du canal) restent roses. La classe .pcr reste sur la ligne (repère pour les tests). */
.tbl tr.pcr.ret td{background:var(--crit-soft)}
@media(prefers-color-scheme:dark){:root:not([data-theme="light"]) .ch.cpc{background:#33202A;color:#F4B8CF;border-color:#6A3047}}
:root[data-theme="dark"] .ch.cpc{background:#33202A;color:#F4B8CF;border-color:#6A3047}
.tbl tr.att td{background:#F5F1FC}
.tbl tr.att:hover td{background:#EDE6F9}
@media(prefers-color-scheme:dark){:root:not([data-theme="light"]) .tbl tr.att td{background:#231E30}}
:root[data-theme="dark"] .tbl tr.att td{background:#231E30}
.tbl td.mt small.tx{display:block;font-size:11.5px;font-weight:500;color:var(--ink-3);max-width:90px;margin-left:auto;line-height:1.25}
.chatt{display:block;width:fit-content;max-width:92px;margin-top:5px;line-height:1.3;font-family:Inter,sans-serif;font-size:10.5px;font-weight:800;letter-spacing:.05em;text-transform:uppercase;
padding:2px 8px;border-radius:9px;background:var(--iris-soft);color:var(--iris);border:1px solid var(--iris);white-space:normal}
.chatt.id{background:var(--iris);color:#fff}
.cliv{color:var(--ink-3);font-style:italic;font-size:13.5px}
.tbl td.act button{font-family:inherit;font-size:13px;font-weight:600;color:var(--ink-2);background:var(--surface);
border:1px solid var(--line);border-radius:6px;padding:5px 10px;cursor:pointer}
.tbl td.act button:hover{border-color:var(--crit);color:var(--crit)}
/* les boutons l'un sous l'autre : la colonne reste étroite, et elle ne disparaît plus
   quand l'écran est juste (le tableau masque ses colonnes secondaires s'il déborde) */
.tbl td.act button{display:block;width:100%;margin:0 0 4px;text-align:center}.tbl td.act button:last-child{margin-bottom:0}
.tv2 .pl3 div{line-height:1.35;padding:2px 0}
.tv2 .pl3 em{font-style:normal;font-family:Inter,sans-serif;font-weight:700;color:var(--iris);margin-right:2px}
.tv2 .pl3 b{font-weight:600;display:inline}
.tv2 .pl3 div{font-size:14px}
.tv2 .pl3 .ty,.tv2 .pl3 i{vertical-align:1px}
.tv2 .pl3 .plus4{font-size:12.5px;color:var(--ink-3)}
/* ---- la liste des ventes, version 27 sept. 2026 ---- */
.tv2 td{padding:12px 12px}
.tv2 td.qd b{display:block;font-weight:700;font-size:14px;white-space:nowrap}
.tv2 td.qd .hh{display:block;font-size:12.5px;color:var(--ink-3);margin-top:2px}
.tv2 td.num{max-width:150px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;overflow-wrap:normal;
  font-size:13px;color:var(--ink-2);font-variant-numeric:tabular-nums;letter-spacing:0}
.tv2 td.cli{max-width:170px;overflow-wrap:normal;word-break:normal}
.tv2 .cl2{display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;line-height:1.3}
.tv2 td.mgc{white-space:nowrap}
.tv2 td.mt small.tx{max-width:none;white-space:nowrap;font-size:11.5px}
.tv2 th.pdt,.tv2 td.pdt{min-width:230px}
.tv2 td.mgc .mg{display:block;font-weight:700}
.tv2 td.mgc small.mg{font-weight:500;font-size:12.5px;margin-top:2px}
.tv2 td.mgc small.prt{display:block;font-size:11.5px;font-weight:500;color:var(--ink-3);margin-top:2px;white-space:nowrap}
.tv2 td.mgc .na{color:var(--ink-3)}
.tv2 td.etat{white-space:nowrap}
.st{display:inline-block;font-family:Inter,sans-serif;font-size:12px;font-weight:700;padding:3px 10px;border-radius:99px;line-height:1.35}
.st.ok{background:var(--good-soft);color:var(--good)}
.st.exp{background:var(--iris-soft);color:var(--iris)}
.st.id{background:var(--warn-soft);color:var(--warn)}
.st.ret{background:var(--crit-soft);color:var(--crit)}
.stm{display:block;font-size:11.5px;color:var(--ink-3);margin-top:4px;white-space:normal;max-width:130px}
.tv2 td.go,.tv2 th.go{width:22px;padding-left:0;color:var(--ink-3);font-size:20px;text-align:center}
.tv2 tbody tr:hover td.go{color:var(--iris)}
.jm .jpa{font:inherit;background:none;border:0;padding:0;color:var(--crit);text-decoration:underline;cursor:pointer}
.tv2 td.mt small.pay{display:inline-block;margin-top:3px;font-size:10.5px;font-weight:700;letter-spacing:.03em;color:var(--ink-2);background:var(--surface-2);border:1px solid var(--line);border-radius:99px;padding:1px 8px;white-space:nowrap}
.jm .jpa:hover{color:var(--iris)}
.pafix{display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.tv2 tr.att td,.tv2 tr.ret td{background:transparent}
.tv2 tr.att:hover td,.tv2 tr.ret:hover td{background:var(--surface-2)}
.tv2 tr.ret td.mt,.tv2 tr.ret td.qd b{color:var(--crit)}
@media (max-width:1450px){ .tv2 td{padding:10px 9px} .tv2 td.num{max-width:120px;font-size:12px} .st{font-size:11px;padding:2px 8px} .tv2 td.cli{max-width:140px} }
/* ---- le haut de la page, version 27 sept. 2026 ---- */
.rs{background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:20px 22px 16px;margin:4px 0 26px}
.rs-t{font-family:Inter,sans-serif;font-size:12px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--ink-3);margin-bottom:14px}
.rs-g{display:grid;grid-template-columns:repeat(4,1fr);gap:0}
.rs-c{display:flex;flex-direction:column;gap:5px;padding:0 20px;border-left:1px solid var(--line-2)}
.rs-c:first-child{padding-left:0;border-left:0}
.rs-v{font-family:Inter,sans-serif;font-size:30px;font-weight:800;letter-spacing:-.02em;line-height:1.05;color:var(--ink)}
.rs-v.g,.rs-k b.g{color:var(--good)} .rs-v.c,.rs-k b.c{color:var(--crit)}
.rs-k{font-size:13.5px;color:var(--ink-2)}
.rs-c.at .rs-v{color:var(--iris)} .rs-c.at .rs-k{color:var(--iris);font-weight:600}
.rs-n{margin-top:16px;padding-top:12px;border-top:1px solid var(--line-2);font-size:13px;color:var(--ink-3)}
.rs-n b{color:var(--ink-2)}
@media(max-width:900px){ .rs-g{grid-template-columns:1fr 1fr;row-gap:16px} .rs-c:nth-child(3){padding-left:0;border-left:0} }
.par{display:block}
.cx{background:var(--surface);border:1px solid var(--line);border-radius:14px;overflow:hidden;margin-bottom:26px}
/* les canaux en tuiles, avec les vrais logos (25 oct. 2026) */
/* une seule ligne (Igal, 25 oct. 2026) : autant de colonnes que de canaux ; en dessous de ~1 100 px, deux lignes */
.cxg{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;padding:4px 0 2px}
.cxt{background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:14px 14px 12px;cursor:pointer;position:relative;transition:box-shadow .15s,transform .15s;min-width:0}
.cxt:hover{box-shadow:0 8px 24px rgba(23,23,29,.08);transform:translateY(-1px)}
.cxt.on{border-color:var(--iris);box-shadow:0 0 0 3px var(--iris-soft)}
.cxt .lg{height:40px;display:flex;align-items:center;gap:8px;margin-bottom:10px;min-width:0}
.cxt .lg img{max-height:36px;max-width:100%;object-fit:contain;flex:0 1 auto;min-width:0}
.cxt .lg .wm{font-family:Inter,sans-serif;font-weight:800;font-size:14px;letter-spacing:-.01em;color:var(--ink);line-height:1.1;overflow:hidden;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical}
.cxt .lg .wm.ls{color:#fff;background:#1C1C1C;padding:5px 10px;border-radius:8px;font-size:13px;letter-spacing:.01em}
.cxt .lg .sub{font-family:Inter,sans-serif;font-size:11px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--ink-3);white-space:nowrap}
.cxt .ca{font-family:Inter,sans-serif;font-weight:800;font-size:21px;letter-spacing:-.02em;line-height:1.1;white-space:nowrap}
.cxt .pcou{display:flex;gap:12px;flex-wrap:wrap;font-size:12px;color:var(--ink-2);margin-top:2px}.cxt .pcou b{font-weight:700;color:var(--ink);font-variant-numeric:tabular-nums}
.cxt .bar{height:7px;border-radius:99px;background:var(--surface-2);margin:10px 0 8px;overflow:hidden}
.cxt .bar i{display:block;height:100%;border-radius:99px;background:var(--c,var(--iris))}
.cxt .l2{display:flex;justify-content:space-between;gap:8px;font-size:12.5px;color:var(--ink-2);font-variant-numeric:tabular-nums;flex-wrap:wrap}
.cxt .l2 b{color:var(--ink)}
.cxt .mgl{margin-top:8px;padding-top:8px;border-top:1px solid var(--line-2);display:flex;justify-content:space-between;align-items:baseline;gap:6px;font-size:12.5px;color:var(--ink-3);flex-wrap:wrap}
.cxt .mgl b.mg{font-weight:800;font-size:14px}
.cxt .mgl small.mg{font-weight:700;font-size:12.5px;padding:2px 7px;border-radius:99px;background:var(--surface-2)}
.cxt .cx-w{position:absolute;right:12px;top:12px}
.cxt .cn{font-size:12.5px;color:var(--ink-3);margin:-6px 0 8px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.cxt.cpc{background:#fff6fa;border-color:#f2b9d3}.cxt.cpc.on{border-color:#c2417f;box-shadow:0 0 0 3px #fbe3ee}
.cxt.c0{--c:#5B4B8A}.cxt.c1{--c:#2C6E4E}.cxt.c2{--c:#B4530A}.cxt.c3{--c:#1F6FB2}.cxt.c4{--c:#A4262C}.cxt.c5{--c:#8A5A00}.cxt.c6{--c:#4C7C8A}.cxt.c7{--c:#7A4E9E}
.cx-h,.cx-r{display:grid;grid-template-columns:minmax(210px,1.3fr) minmax(160px,1.6fr) 160px 100px 170px;gap:16px;align-items:center;padding:0 20px}
.cx.nm .cx-h,.cx.nm .cx-r{grid-template-columns:minmax(210px,1.3fr) minmax(160px,1.6fr) 160px 100px}
.cx-h{font-family:Inter,sans-serif;font-size:11px;font-weight:700;letter-spacing:.09em;text-transform:uppercase;color:var(--ink-3);padding-top:12px;padding-bottom:10px;border-bottom:1px solid var(--line)}
.cx-h .r,.cx-r .r{text-align:right;font-variant-numeric:tabular-nums}
.cx-h span{white-space:nowrap}
/* « 37 ventes affichées sur 37 » en haut à droite : redit ce que le résumé dit mieux */
body:not(.quotes) #src{display:none}
.cx-r{padding-top:13px;padding-bottom:13px;border-bottom:1px solid var(--line-2);cursor:pointer;position:relative}
.cx-r.pc{flex:none;max-width:none;width:auto;min-width:0;border:0;border-bottom:1px solid var(--line-2);border-radius:0;box-shadow:none;margin:0;display:grid;background:transparent}
.cx-r.pc:last-child{border-bottom:0}
.cx-r.pc:hover{background:var(--surface-2)}
.cx-r.pc.on{background:var(--iris-soft);box-shadow:inset 3px 0 0 var(--iris)}
.cx-r:last-child{border-bottom:0}
.cx-r:hover{background:var(--surface-2)}
.cx-r.on{background:var(--iris-soft);box-shadow:inset 3px 0 0 var(--iris)}
.cx-n{display:flex;align-items:center;gap:11px;min-width:0}
.cx-l{flex:none;width:30px;height:30px;border-radius:8px;display:flex;align-items:center;justify-content:center;background:var(--c,var(--iris));overflow:hidden}
.cx-l img{width:30px;height:30px;background:#fff;padding:5px;border:1px solid var(--line-2);border-radius:8px}
.cx-l b{font-family:Inter,sans-serif;font-size:11.5px;font-weight:800;color:#fff;letter-spacing:.02em}
.cx-n .cn{font-weight:700;font-size:15px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.cx-w{font-size:11.5px;color:var(--warn);text-decoration:none;border-bottom:1px dotted var(--warn);white-space:nowrap}
.cx-b{display:flex;align-items:center;gap:10px}
.cx-b i{display:block;height:8px;border-radius:99px;background:var(--c,var(--iris));opacity:.85;min-width:2px}
.cx-b em{font-style:normal;font-family:Inter,sans-serif;font-size:12.5px;font-weight:700;color:var(--ink-3);white-space:nowrap}
.cx-ca{font-family:Inter,sans-serif;font-weight:800;font-size:16px}
.cx-r .d{font-size:14px;color:var(--ink-2)}
.cx-r b.mg{font-weight:700;font-size:14.5px} .cx-r small.mg{font-size:12.5px;font-weight:600;margin-left:6px}
.cx-r .na{color:var(--ink-3)}
.cx-r.c0{--c:#5B4B8A}.cx-r.c1{--c:#2C6E4E}.cx-r.c2{--c:#B4530A}.cx-r.c3{--c:#1F6FB2}.cx-r.c4{--c:#A4262C}.cx-r.c5{--c:#8A5A00}.cx-r.c6{--c:#4C7C8A}.cx-r.c7{--c:#7A4E9E}
@media(max-width:1100px){ .cx-h,.cx-r{grid-template-columns:minmax(170px,1.2fr) 1fr 110px 90px 150px;gap:10px;padding-left:14px;padding-right:14px} }
@media(max-width:760px){ .cx-h{display:none} .cx-r{grid-template-columns:1fr auto;row-gap:6px} .cx-b{grid-column:1/-1} }
.rl2{background:var(--surface-2);border:1px solid var(--line);border-radius:9px;padding:12px 14px;
font-size:13.5px;color:var(--ink-2);line-height:1.6}
.rl2 b{color:var(--ink)}
.coche{display:flex;align-items:flex-start;gap:9px;font-size:13.5px;color:var(--ink-2);line-height:1.5}
.coche input{width:17px;height:17px;margin-top:1px;accent-color:var(--iris)}
/* ---- la file des ventes qui arrivent toutes seules ----
   Le site et la caisse deposent leurs ventes sur le serveur. Elles attendent ici :
   on les regarde avant qu'elles ne touchent au stock. */
.file{border:1px solid var(--iris);border-radius:12px;background:var(--surface);margin:0 0 20px;overflow:hidden}
.file .ft{display:flex;align-items:center;gap:12px;padding:12px 16px;background:var(--iris-soft);
border-bottom:1px solid var(--line);flex-wrap:wrap}
.file .ft b{font-size:15px;color:var(--ink)}
.file .ft .sp{flex:1}
.file .ft .aide{font-size:12.5px;color:var(--ink-2);width:100%;line-height:1.5}
.file table{width:100%;border-collapse:collapse;font-size:13.5px}
.file th{text-align:left;font-family:Inter,sans-serif;font-size:10.5px;letter-spacing:.09em;
text-transform:uppercase;color:var(--ink);font-weight:800;padding:8px 14px;background:var(--surface-2)}
.file td{padding:9px 14px;border-top:1px solid var(--line-2);vertical-align:top}
.file td.r{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
.file .src{display:inline-block;padding:2px 8px;border-radius:99px;font:700 10.5px Inter,sans-serif;
background:var(--surface-2);color:var(--ink-2)}
.file .prop{display:block;margin-top:4px;font-size:12.5px;color:var(--ink-2)}
.file .prop select{font:inherit;font-size:12.5px;padding:2px 6px;border:1px solid var(--line);border-radius:6px;background:#fff;max-width:320px}
.file .inc{color:var(--warn);font-weight:600}
.file .mq{color:var(--crit);font-weight:600}
.file .dec{width:100%;font-size:12.5px;line-height:1.55;color:var(--ink-2);
background:var(--crit-soft);border-left:3px solid var(--crit);border-radius:0 8px 8px 0;padding:9px 13px}
.file .dec b{color:var(--crit)}
.file .ret{color:var(--crit);font-weight:600}
.file .lg{display:block;font-size:12px;color:var(--ink-3);margin-top:2px;line-height:1.45}
.file .btn.sm{padding:4px 9px;font-size:12px}
.recap{background:var(--iris-soft);border-left:3px solid var(--iris);border-radius:0 8px 8px 0;
padding:11px 14px;font-size:13.5px;color:var(--ink-2);line-height:1.6}
.recap b{color:var(--ink)}
'''+_facture.CSS

CSS_QUOTES = r'''
.lsc{background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:18px 20px;margin:0 0 22px}
.lsc .lsc-h{font-size:18px;font-weight:700;margin:0}
.lsc-erp{display:flex;gap:10px;margin:18px 0}
.lsc-maj{display:flex;gap:12px;align-items:center;justify-content:space-between;flex-wrap:wrap;margin:0 0 12px;color:var(--ink-2);font-size:13.5px}
#lsq-aide{background:var(--surface-2);border-radius:10px;padding:12px 16px;margin-bottom:12px;font-size:14px}#lsq-aide ol{margin:0 0 8px 18px;padding:0}
.lsq-fv{margin-left:8px;cursor:grab}
.lsc .lsc-t p{color:var(--ink-2);font-size:14px;margin:4px 0 12px}
.lsc-o{display:flex;gap:8px;margin-bottom:12px}
.lsc-b{border:1px solid var(--line);background:var(--surface-2);border-radius:999px;padding:7px 14px;font:inherit;font-weight:600;cursor:pointer;color:var(--ink-2)}
.lsc-b.on{background:var(--iris);border-color:var(--iris);color:#fff}
.lsc-b b{margin-left:6px}
.lsc-l td{vertical-align:middle}.lsc-l td.lsc-c{color:var(--ink-2);font-size:13px}
.lsc-l small.lsc-p{display:block;color:var(--ink-3);font-size:12px}
.lsc-l tr.lsc-n td{color:var(--ink-3);font-size:12.5px;padding-top:0}
.lsc-f{padding:10px 4px}.lsc-f h4{margin:0 0 10px}
.lsc-g{display:flex;gap:14px;flex-wrap:wrap;margin-bottom:12px}.lsc-g label{display:flex;flex-direction:column;gap:4px;font-size:12.5px;color:var(--ink-3)}
.lsc-lg{width:100%;border-collapse:collapse}.lsc-lg td,.lsc-lg th{padding:7px 8px;border-bottom:1px solid var(--line-2);text-align:left}
.lsc-lg .r{text-align:right}.lsc-x{display:block;color:var(--warn);font-weight:600;margin-bottom:4px}.lsc-s{display:block;color:var(--ink-3);font-weight:500}.lsc-ch{width:100%;max-width:520px}
.lsc-m{color:var(--ink-2);min-height:18px}.lsc-a{display:flex;gap:8px;justify-content:flex-end}

.mdz{position:relative;margin-top:8px;border:2px dashed var(--line);border-radius:10px;padding:12px 14px;text-align:center;color:var(--ink-2);cursor:pointer;background:var(--surface)}
.mdz b{display:block;color:var(--ink);font-size:13.5px}.mdz span{font-size:12px}
.mdz.sur,.mdz:hover{border-color:var(--iris);background:var(--iris-soft)}
.mdz input{position:absolute;inset:0;opacity:0;cursor:pointer}
.mlect{margin-top:6px;font-size:12.5px;color:var(--ink-2)}.mlect.err{color:var(--crit);font-weight:600}
/* ---- la rubrique Quotes : la fenêtre du devis devient la page ----
   Sam reçoit une demande de prix (WhatsApp, mail, photo). Il choisit les parfums,
   met SES prix — c'est lui qui décide, à la main — et envoie. La liste collée ou
   déposée n'est qu'un raccourci pour remplir les lignes plus vite. Tout le reste
   de Ventes (journal, canaux, file d'attente) n'a rien à faire ici et disparaît. */
body.quotes .info:not(#msgov .info),body.quotes #file,body.quotes #kpis,body.quotes .par,body.quotes .tools,body.quotes #corps,
body.quotes h2.sec:not(.docs h2){display:none}
/* Dans Ventes, la liste « Factures et devis » faisait doublon avec les rubriques Factures et
   Cote (Igal, 25 sept. 2026) : elle ne reste que sur la page Cote, qui s'en sert */
body:not(.quotes) #docs{display:none}
body.quotes #vov{position:static;display:block;background:none;padding:0;overflow:visible;margin:0 0 26px}
body.quotes #vov .mod{max-width:none;width:auto;margin:0;box-shadow:none;border:1px solid var(--line);border-radius:12px;max-height:none}
body.quotes #vov .mh h3::after{content:''}
body.quotes #vov[hidden]{display:none}
body.quotes #vx{display:none}
body.quotes #v-liste{margin-left:auto;background:var(--iris);color:#fff;border-color:var(--iris)}
body.quotes #v-stock,body.quotes #v-stock+span{display:none}
body.quotes #v-num,body.quotes #v-num+*{display:none}
body.quotes #v-ok{background:var(--iris);color:#fff;border-color:var(--iris)}
body.quotes #m-att{display:none}
body.quotes .hact #nv{background:var(--iris);color:#fff;border-color:var(--iris)}
/* le sélectionneur : la liste des parfums trouvés reste posée sous le champ, avec
   des cases à cocher — on coche ce qu'on veut et on ajoute d'un coup */
body.quotes #v-res{position:static;max-height:380px;margin-top:6px;box-shadow:none}
body.quotes #v-res div.cand{display:flex;align-items:center;gap:12px;padding:7px 12px}
body.quotes #v-res div.cand input{width:17px;height:17px;margin:0;flex:none;accent-color:var(--iris)}
.vig{width:46px;height:46px;flex:none;border-radius:7px;background:#fff;border:1px solid var(--line-2);object-fit:contain;padding:2px}
.vig.miss{display:flex;align-items:center;justify-content:center;color:var(--ink-3);font-size:10px}
body.quotes .pan td .vig{width:38px;height:38px;vertical-align:middle;margin-right:9px;float:left}
body.quotes #v-res div.cand b{flex:1;display:inline;font-weight:600}
body.quotes #v-res div.cand span{flex:none;font-size:12px;color:var(--ink-3);white-space:nowrap}
body.quotes #v-res div.cand span i{font-style:normal;color:var(--ink);font-weight:600}
body.quotes #v-res .cand.coche{background:var(--iris-soft)}
body.quotes #v-res .cpied{display:flex;gap:10px;align-items:center;padding:9px 12px;background:var(--surface);position:sticky;bottom:0;border-top:1px solid var(--line)}
body.quotes #v-res .cpied .btn.pri{background:var(--iris);color:#fff;border-color:var(--iris)}
body.quotes #v-res .cpied .btn:disabled{opacity:.45}
.btn.off{opacity:.45;cursor:not-allowed}
body.quotes #v-res .cpied em{margin-left:auto;font-style:normal;font-size:12px;color:var(--ink-3)}
body.quotes .pan .colref{font-size:12.5px;color:var(--ink-2)}
body.sansPA .pan .colpa{display:none}
/* ---- la liste des devis, à la manière de la caisse : filtres, une ligne par devis
   qui se déplie sur ses lignes et ses boutons ---- */
body.quotes #docs-chips{display:none}
.qf{display:flex;gap:12px;flex-wrap:wrap;align-items:flex-end;margin:0 0 12px}
.qf .fld{min-width:160px}.qf .fld input,.qf .fld select{width:100%}
.ql{width:100%;border-collapse:collapse;font-size:13.5px}
.ql th{text-align:left;font:700 10.5px Inter,sans-serif;letter-spacing:.09em;text-transform:uppercase;color:var(--ink-3);padding:8px 10px;border-bottom:1px solid var(--line)}
.ql td{padding:10px;border-bottom:1px solid var(--line-2);vertical-align:middle}
.ql tr.qr{cursor:pointer}.ql tr.qr:hover td{background:var(--surface-2)}.ql tr.qr.on td{background:var(--iris-soft)}
.ql .num b{display:block}.ql .num small{color:var(--ink-3);font-size:11.5px}
.ql .cli{display:flex;gap:9px;align-items:center}.ql .cli i{flex:none;width:30px;height:30px;border-radius:50%;display:flex;align-items:center;justify-content:center;font:700 11px Inter,sans-serif;color:#fff;font-style:normal}
.ql .cli b{display:block}.ql .cli small{color:var(--ink-3);font-size:11.5px;display:block}
.ql .r{text-align:right;font-variant-numeric:tabular-nums}
.ql .et{display:inline-block;padding:2px 9px;border-radius:99px;font:700 11px Inter,sans-serif}
.ql .et.devis{background:var(--iris-soft);color:var(--iris)}.ql .et.converti{background:var(--good-soft);color:var(--good)}.ql .et.archive{background:var(--line-2);color:var(--ink-3)}
.ql .chev{color:var(--ink-3);font-size:12px;width:18px}
.ql tr.qd td{background:var(--surface);padding:16px 14px 18px;border-bottom:2px solid var(--line)}
.qdet{display:grid;grid-template-columns:1fr 220px;gap:22px}
@media(max-width:800px){ .qdet{grid-template-columns:1fr} }
/* colonnes de largeur FIXE (Igal, 1er oct. 2026 : « aligne-moi tout, les @ ne sont pas droits ») :
   chaque ligne était sa propre grille, et « auto » prenait la largeur de son texte */
.qdet .lg{display:grid;grid-template-columns:34px minmax(0,1fr) 150px 110px;gap:6px 12px;align-items:baseline;padding:7px 0;border-bottom:1px solid var(--line-2)}
.qdet .lg>span:nth-child(3),.qdet .lg>span:nth-child(4){text-align:right;white-space:nowrap;font-variant-numeric:tabular-nums}
.qdet .tot span.r{font-variant-numeric:tabular-nums}
@media(max-width:600px){ .qdet .lg{grid-template-columns:28px minmax(0,1fr) 96px 84px} }
.qdet .lg b{font-weight:600}.qdet .lg small{color:var(--ink-3)}
.qdet .tot{margin-top:10px;display:grid;grid-template-columns:1fr 122px;gap:4px 0;max-width:420px;margin-left:auto}
.qdet .tot .r{text-align:right}
.qdet .tot .tt{font-weight:800;border-top:1px solid var(--ink);padding-top:8px;margin-top:4px}
.qdet .note{margin-top:12px;font-size:13px;color:var(--ink-2)}.qdet .note b{color:var(--ink)}
.qdet .btns{display:flex;flex-direction:column;gap:8px}.qdet .btns .btn{width:100%;text-align:center}
.qdet .btns .btn.pri{background:var(--iris);color:#fff;border-color:var(--iris)}
.qdet .btns .btn.lsq-sup{color:var(--crit);border-color:var(--crit)}
'''

CORPS = r'''
<!-- Les chiffres et les canaux en haut, la file d'attente ensuite (Igal, 25 sept. 2026 :
     « cette partie-là je la veux en haut » — avec 65 commandes en attente, elle était
     repoussée tout en bas de l'écran) -->
<div id="kpis"></div>

<h2 class="sec">Par canal <em id="nbc"></em></h2>
<div class="par" id="par"></div>

<div id="file"></div>

'''+_facture.LISTE+r'''
<h2 class="sec" id="tv">Toutes les ventes <em id="nbv"></em></h2>
<div class="tools">
  <div class="srch"><input id="q" autocomplete="off" placeholder="Chercher un produit, un client, un numéro…"></div>
  <select id="fc" class="sel"><option value="">Tous les canaux</option></select>
  <select id="fp" class="sel">
    <option value="">Depuis toujours</option><option value="1">Aujourd'hui</option>
    <option value="7">7 derniers jours</option><option value="mois" selected>Depuis le début du mois</option><option value="30">30 derniers jours</option>
    <option value="90">90 derniers jours</option><option value="365">12 mois</option>
    <option value="jour">Un jour précis…</option>
  </select>
  <input type="date" id="fj" class="sel" hidden title="Le jour à afficher">
  <span class="sp"></span>
  <button class="btn" id="vcb" style="display:none" title="Relit les commandes des deux sites et de Perfume City, ajoute celles qui manquent, puis remet le stock des sites au niveau de l'ERP">Tout revérifier</button>
  <button class="btn" id="ctrb" style="display:none" title="Compare les commandes du site avec l'ERP et montre celles qui manquent">Vérifier les commandes du site</button>
  <button class="btn" id="msgb" title="Coller un WhatsApp ou un SMS de client">Message client</button>
  <button class="btn pri" id="nv">+ Enregistrer une vente</button>
  <span id="exp"></span>
</div>

<div id="corps"></div>

<div class="dov" id="dov"><div class="dt">
  <div class="dh"><h3 id="d-tit">—</h3><button class="x" id="d-x" title="Fermer">✕</button></div>
  <div class="db" id="d-corps"></div>
  <div class="df" id="d-pied"></div>
</div></div>


<div class="ov" id="vcov"><div class="mod" style="max-width:760px">
  <div class="mh"><h3>Vérification complète des ventes</h3><button class="x" id="vc-x" title="Fermer">✕</button></div>
  <div class="mb" style="max-height:68vh;overflow-y:auto">
    <p class="hint" style="margin:0 0 10px">Un seul geste, trois canaux : perfumestrade.com, wholesale.perfumestrade.com et Perfume City. L'outil relit les commandes des 14 derniers jours, les compare avec ce que l'ERP a vraiment enregistré, ajoute celles qui manquent, puis remet le stock des deux sites au niveau de l'ERP.</p>
    <div id="vc-res"></div>
  </div>
  <div class="mf"><span class="msg" id="vc-msg"></span>
    <button class="btn" id="vc-ann">Fermer</button>
    <button class="btn pri" id="vc-ok">Lancer la vérification</button></div>
</div></div>

<div class="ov" id="ctrov"><div class="mod" style="max-width:880px">
  <div class="mh"><h3>Contrôle des commandes du site</h3><button class="x" id="ctr-x" title="Fermer">✕</button></div>
  <div class="mb" style="max-height:68vh;overflow-y:auto">
    <p class="hint" style="margin:0 0 10px">Lecture seule : l'outil lit les commandes du site, les compare avec ce que l'ERP connaît (file d'attente, expéditions, factures) et montre celles qui manquent. Rien n'est ajouté sans ton clic.</p>
    <div class="psq" style="display:flex;gap:18px;flex-wrap:wrap;margin:0 0 12px">
      <label><input type="radio" name="ctrq" value="" checked> perfumestrade.com (détail)</label>
      <label><input type="radio" name="ctrq" value="gros"> wholesale.perfumestrade.com (gros)</label>
      <select id="ctr-j" class="sel"><option value="7">7 derniers jours</option><option value="14" selected>14 derniers jours</option><option value="30">30 derniers jours</option></select>
    </div>
    <div id="ctr-res"></div>
  </div>
  <div class="mf"><span class="msg" id="ctr-msg"></span>
    <button class="btn" id="ctr-xl" title="Les parfums des commandes ajoutées après un contrôle, avec les quantités retirées du stock — pour vérifier le comptage">Parfums à vérifier (Excel)</button>
    <button class="btn" id="ctr-ann">Fermer</button>
    <button class="btn pri" id="ctr-ok" disabled>Ajouter les commandes cochées</button></div>
</div></div>

<div class="ov" id="msgov"><div class="mod">
  <div class="mh"><h3>Une commande reçue par message</h3><button class="x" id="m-x" title="Fermer">✕</button></div>
  <div class="mb">
    <div class="info" style="margin:0">Colle ici le WhatsApp ou le SMS du client, tel quel.
    L'outil cherche chaque parfum dans le catalogue — sans code-barres, sur la marque, le nom et la
    contenance. Il <b>propose</b>, il ne décide pas : ce qui n'est pas sûr est signalé et t'attend.
    Rien n'est enregistré tant que tu n'as pas cliqué en bas.</div>
    <div class="fg">
      <div class="fld rech"><label>Client</label>
        <input id="m-client" placeholder="Tape 2 lettres — ou un nouveau nom" autocomplete="off">
        <div class="res" id="m-cres"></div></div>
      <div class="fld"><label>Canal</label><select id="m-canal"></select></div>
    </div>
    <div class="msgz">
      <label class="fld" style="gap:5px"><span style="font-family:Inter,sans-serif;font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;font-weight:800">Le message, ou la liste</span></label>
      <textarea id="m-txt" placeholder="Bonjour, je voudrais :&#10;2 sauvage 100ml&#10;bleu de chanel 3.4 oz x 3&#10;1 flacon good girl 80"></textarea>
      <!-- La liste arrive aussi souvent en photo ou en fichier qu'en texte : une
           seule porte pour tout, qui rend du texte dans la zone ci-dessus. -->
      <div class="mdz" id="m-dz"><b>…ou dépose la liste du client ici</b>
        <span>photo, PDF, Excel, CSV, capture d'écran — tout se lit, sur cet ordinateur</span>
        <input type="file" id="m-fichier" accept="__ACCEPT__"></div>
      <div class="mlect" id="m-lect" hidden></div>
    </div>
    <div id="m-res"></div>
    <div class="mrap" id="m-rap" hidden></div>
  </div>
  <div class="mf"><span class="msg" id="m-msg"></span>
    <button class="btn" id="m-ann">Fermer</button>
    <button class="btn" id="m-devis" disabled>Faire un devis</button>
    <button class="btn pri" id="m-att" disabled>Mettre en commande à valider</button></div>
</div></div>

<div class="ov" id="retov"><div class="mod">
  <div class="mh"><h3>Annuler une vente ou rembourser</h3><button class="x" id="ret-x" title="Fermer">✕</button></div>
  <div class="mb">
    <div class="rl2" id="ret-tete"></div>
    <div class="pan" id="ret-pan"></div>
    <div class="fg">
      <div class="fld"><label>Mode de remboursement</label><select id="ret-mode"></select>
        <span class="aide">Ce qui a été rendu au client, ou « avoir » s'il garde un crédit chez toi.</span></div>
      <div class="fld"><label>Motif</label><select id="ret-motif"></select></div>
      <div class="fld"><label>Date</label><input id="ret-date" type="date"></div>
      <div class="fld"><label>Note (facultatif)</label><input id="ret-note" placeholder="flacon ouvert, client mécontent…"></div>
    </div>
    <label class="coche"><input type="checkbox" id="ret-stock" checked>
      <span>Remettre ces flacons en stock (à décocher si la marchandise est perdue, cassée ou reste chez le client).</span></label>
    <div class="recap" id="ret-recap"></div>
  </div>
  <div class="mf"><span class="msg" id="ret-msg"></span>
    <button class="btn" id="ret-ann">Fermer</button>
    <button class="btn pri" id="ret-ok" disabled>Enregistrer le remboursement</button></div>
</div></div>

<div class="ov" id="vov"><div class="mod">
  <div class="mh"><h3>Enregistrer une vente</h3><button class="x" id="vx" title="Fermer">✕</button></div>
  <div class="mb">
    <div class="fg">
      <div class="fld"><label>Canal de vente</label><select id="v-canal"></select>
        <span class="aide" id="v-aide"></span></div>
      <div class="fld"><label>Date</label><input id="v-date" type="date"></div>
      <div class="fld rech"><label>Client (facultatif)</label>
        <input id="v-client" placeholder="Tape 2 lettres — ou un nouveau nom" autocomplete="off">
        <div class="res" id="v-cres"></div></div>
      <div class="fld"><label>N° de vente</label><input id="v-num" placeholder="automatique"></div>
    </div>
'''+_facture.BLOC_VENTE+r'''

    <div class="fld rech"><label>Ajouter un parfum — scanne le code-barres ou tape le nom</label>
      <input id="v-q" autocomplete="off" placeholder="Code-barres, marque ou nom du parfum" autocomplete="off">
      <div class="res" id="v-res"></div></div>

    <div class="pan" id="v-pan"></div>
    <!-- 4 nov. 2026 (Igal) : « quand il a tapé plusieurs références, il est obligé de remonter vers la barre de recherche » —
         la même recherche, une seconde fois SOUS les lignes. C'est la même liste de résultats (#v-res) qui vient se placer
         sous la case qu'on utilise. -->
    <div class="fld rech" id="v-q2w" hidden><label>Ajouter un autre parfum — sans remonter</label>
      <input id="v-q2" autocomplete="off" placeholder="Code-barres, marque ou nom du parfum"></div>
    <div class="fld" id="v-note-w" hidden><label>Note</label><input id="v-note" placeholder="facultatif — visible sur le devis et dans la liste" maxlength="200"></div>

    <label class="coche"><input type="checkbox" id="v-stock" checked>
      <span>Sortir ces flacons du stock (à décocher si le stock a déjà été mis à jour ailleurs).</span></label>
    <div class="recap" id="v-recap"></div>
  </div>
  <div class="mf"><span class="msg" id="v-msg"></span>
    <button class="btn" id="v-ann">Annuler</button>
    <button class="btn pri" id="v-ok" disabled>Enregistrer la vente</button></div>
</div></div>
'''+_facture.OVERLAY

JS = r'''
const IDX=__IDX__;
const KFACT='factures-v1', KUSR='crm-utilisateur-v1', KREG='reglages-v1',
      KMOD='fiches-modifiees-v1', KEXT='stock-externe-v1', KVENT='ventes-v1',
      KCLI='clients-v1', KJOU='crm-journal-v1';
let FACT=lit(KFACT,[]); if(!Array.isArray(FACT)) FACT=base(KFACT,[]);
let USR=NOM_UTIL;
/* arrivée depuis la fiche d'un parfum (11 oct. 2026) : ?q=numéro de vente → la vente cherchée, toutes périodes */
try{ const q0=new URLSearchParams(location.search).get('q'); if(q0){ window.addEventListener('load',()=>{ setTimeout(()=>{ try{ $('q').value=q0; $('fp').value=''; vus=80; dessine(); }catch(e){} },400); }); } }catch(e){}

window.__nomChange.push(v=>{ USR=v; try{ majUser(); }catch(e){} });
let REG={margeMin:10}; try{ REG=Object.assign(REG,JSON.parse(localStorage.getItem(KREG)||'{}')); }catch(e){}
let MOD=lit(KMOD,{}); if(!MOD||typeof MOD!=='object') MOD=base(KMOD,{});
let EXT={q:{}}; try{ EXT=Object.assign({q:{}},JSON.parse(localStorage.getItem(KEXT)||'{}')); }catch(e){}
/* le stock et le prix d'achat réellement en vigueur : la fiche corrigée l'emporte sur le fichier */
const qteEff=cle=>{ const m=MOD[cle]; if(m&&m.qte!=null) return +m.qte;
  const bc=(IDX[cle]||[])[0]; const e=EXT.q[bc]; return e!=null?+e:((IDX[cle]||[])[7]||0); };
/* ============ PERFUME CITY A SON PROPRE STOCK (13 oct. 2026) ============
   Igal : « sur Ventes, quand on enregistre une vente et que le canal est Perfume City, ne pas la sortir du stock
   central, mais de l'inventaire Perfume City ». Cet inventaire est celui de la rubrique Inventaire › Perfume City
   (magasin partagé pc-stock-v1, voir _fusion.py ; la quantité vendable en colonne 5). Une vente Perfume City
   le diminue ; le stock central ne bouge pas. Une modification, un remboursement ou une annulation le remettent à sa place :
   la vente garde la marque `pc` pour savoir de quel stock les flacons sont sortis. */
const estPC=n=>/perfume\s*(in\s*the\s*)?city/i.test(String(n||''));   /* « Perfume City » ou « Perfume in the City » */
let _PCI=null;
function pcRows(){ if(_PCI===null){ _PCI=pcsRows()||[]; } return _PCI; }   /* magasin partagé pc-stock-v1 (voir _fusion.py) */
const pcBC=cle=>String((IDX[cle]||[])[0]||'').replace(/^0+/,'');
function pcIdx(cle){ const bc=pcBC(cle); if(!bc) return -1; return pcRows().findIndex(x=>x&&x[0]&&String(x[0]).replace(/^0+/,'')===bc); }
const pcQte=cle=>{ const i=pcIdx(cle); return i<0?0:(+pcRows()[i][5]||0); };
function pcPose(cle,q){ const R=pcRows(), i=pcIdx(cle);
  if(i<0){ if(!pcBC(cle)||!(q>0)) return false; const v=IDX[cle]||[], pa=paEff(cle);
    R.push([v[0]||'',v[1]||'',v[2]||'',v[3]||'','',q,pa,pa!=null?q*pa:null,'non','b'+v[0],null,null]); return true; }
  R[i][5]=q; if(R[i][6]!=null) R[i][7]=q*R[i][6]; return true; }
function pcSauve(){ return pcsSauve(pcRows()); }
/* le stock d'où part une vente de ce canal */
const stkC=(cle,canal)=>estPC(canal)?pcQte(cle):qteEff(cle);
const paEff=cle=>{ const m=MOD[cle]; if(m&&m.pa!=null) return +m.pa; const v=(IDX[cle]||[])[4]; return v==null?null:+v; };
/* un parfum peut être marqué « pas vendu » sur un canal, depuis sa fiche catalogue */
const horsCanal=(cle,id)=>{ const m=MOD[cle]; return !!(m&&Array.isArray(m.pcOff)&&m.pcOff.includes(id)); };
const NP='(non précisé)';
let vus=80, canalSel='';

/* ================= LES VENTES QUI ARRIVENT TOUTES SEULES =================
   Le site (WooCommerce) et la caisse déposent leurs ventes sur le serveur. Elles
   n'entrent PAS directement dans le stock : elles attendent ici qu'on les regarde.
   C'est le même principe que l'import d'un fichier — on lit, on montre, on confirme.
   Une caisse se trompe parfois, et un stock modifié sans que personne l'ait vu passer
   est un stock que plus personne ne sait expliquer. */
const KFILE='caisse-file-v1';
const litFile=()=>{ const f=lit(KFILE,[]); return Array.isArray(f)?f:[]; };
/* le code-barres d'une ligne → la référence du catalogue, alias compris */
function cleDeBC(bc){
  if(!bc) return null;
  const n=String(bc).replace(/[^0-9]/g,'').replace(/^0+/,'');
  if(!n) return null;
  /* « 3605533286555nobox » : les mêmes chiffres que la boîte, pas la même fiche (Sam, 6 oct. 2026) */
  const mention=(typeof mentionBC==='function')?mentionBC(bc).mention:'';
  const C=[]; for(const cle in IDX){ if(String((IDX[cle]||[])[0]||'').replace(/[^0-9]/g,'').replace(/^0+/,'')===n) C.push(cle); }
  if(C.length){ if(typeof parMention!=='function') return C[0];
    const k=parMention(C,mention,cle=>(IDX[cle]||[])[1]); if(k) return k; if(mention) return null; }
  for(const cle in MOD){ const m=MOD[cle];
    if(m&&m.bcs&&String(m.bcs).split(/[^0-9]+/).map(x=>x.replace(/^0+/,'')).includes(n)) return cle; }
  /* une case collée du fichier (deux codes dans la même cellule) */
  const cx=(typeof cleParBCX==='function')?cleParBCX(n):null;
  if(cx&&IDX[cx]) return cx;
  return cleProcheBC(bc);
}
/* Un code abîmé (Amazon : chiffre collé devant, début manquant, ASIN seul) —
   même règle que dans _file_auto.py : un seul candidat, sinon rien. */
let _FIN=null, _ASIN=null;
function cleProcheBC(bc){
  if(!_FIN){ _FIN={}; _ASIN={};
    const pose=(b,cle)=>{ b=String(b||'').replace(/[^0-9]/g,'').replace(/^0+/,''); if(b.length>=10){ const f=b.slice(-10); (_FIN[f]=_FIN[f]||[]).push([b,cle]); } };
    for(const cle in IDX){ const r=IDX[cle]||[]; pose(r[0],cle); if(Array.isArray(r[19])) r[19].forEach(x=>pose(x,cle));
      const asin=String(r[18]||'').trim().toUpperCase(); if(/^B0[A-Z0-9]{8}$/.test(asin)&&!_ASIN[asin]) _ASIN[asin]=cle; }
    for(const cle in MOD){ const m=MOD[cle]; if(m&&m.bcs&&IDX[cle]) String(m.bcs).split(/[^0-9]+/).forEach(x=>pose(x,cle)); } }
  const raw=String(bc||'').trim().toUpperCase();
  if(/^B0[A-Z0-9]{8}$/.test(raw)) return _ASIN[raw]||null;
  const n=raw.replace(/[^0-9]/g,'').replace(/^0+/,''); if(n.length<10) return null;
  const C=(_FIN[n.slice(-10)]||[]).filter(([b])=>b.endsWith(n)||n.endsWith(b));
  let cles=[...new Set(C.map(([,c])=>c))]; if(cles.length===1) return cles[0];
  /* même règle que _file_auto.py : seul le premier chiffre change (seconde annonce Amazon) */
  if(!cles.length&&n.length>=12){ const D=(_FIN[n.slice(-10)]||[]).filter(([b])=>b.length===n.length&&b.slice(1)===n.slice(1));
    cles=[...new Set(D.map(([,c])=>c))]; if(cles.length===1) return cles[0]; }
  return null;
}
/* ce qu'une vente en attente deviendrait : lignes reconnues, inconnues, montant */
/* Une ligne « inconnue » : son code (SKU du site ou de la caisse) ne correspond à
   aucun code-barres du catalogue. Mais elle porte un nom — et le nom, on sait le
   lire. Si Sam a déjà dit une fois « ce nom-là, c'est ce parfum », on l'applique ;
   sinon on lui propose les parfums qui ressemblent, il choisit, et c'est retenu.
   On ne devine JAMAIS tout seul ici : une vente sort du stock, une erreur de
   devinette serait pire qu'une ligne en attente. */
function fParNom(des){
  if(!des||!/[a-zà-ÿ]{3}/i.test(des)||typeof mCherche!=='function') return {cle:'',cands:[]};
  try{ const r=mCherche(des);
    if(r.appris&&r.cands[0]&&IDX[r.cands[0].cle]) return {cle:r.cands[0].cle,cands:[],appris:true};
    return {cle:'',cands:r.cands.filter(c=>c.sc>=0.3&&IDX[c.cle]).slice(0,6)};
  }catch(e){ return {cle:'',cands:[]}; }
}
/* le nom complet du catalogue (« Chanel Bleu edp 3.4 »), pas le nom court des
   listes (« Chanel Bleu ») qui ne distingue pas l'EDP de l'EDT */
let _NOMC=null;
/* Le TYPE du parfum (EDT, EDP, OIL, SET…) : deux flacons du même nom ne sont
   pas le même produit, et ne valent pas le même prix. Il s'écrit toujours de la
   même façon, partout : une pastille juste après le nom. */
const TY=cle=>String(((IDX[cle]||[])[9])||'').trim();
const GEN={M:'Homme',W:'Femme',U:'Unisexe',K:'Enfant'};
const GN=cle=>GEN[String(((IDX[cle]||[])[10])||'').trim().toUpperCase()]||'';
/* Le type va dans le document (c'est le produit) ; le genre reste à l'écran,
   il aide à choisir mais n'a rien à faire sur la facture d'un client. */
const tyBadge=cle=>{ const t=TY(cle), g=GN(cle);
  return (t?' <i class="ty" data-nolang>'+esc(t)+'</i>':'')+(g?' <i class="gn">'+esc(g)+'</i>':''); };
const tyTexte=cle=>{ const t=TY(cle); return t?' '+t:''; };
/* Une ligne déjà enregistrée : son libellé est figé. Si le type y est déjà
   (ventes faites depuis aujourd'hui), on ne le répète pas. */
function tyVu(l){
  if(!l||!l.cle) return '';
  const t=TY(l.cle); if(!t) return '';
  const r=String(l.ref||'');
  const dedans=new RegExp('(^|[^A-Za-z])'+t.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')+'([^A-Za-z]|$)','i').test(r);
  return dedans ? tyBadge(l.cle).replace(/<i class="ty"[^>]*>[^<]*<\/i>/,'') : tyBadge(l.cle);
}

function fNomComplet(cle){
  if(!_NOMC){ _NOMC={}; try{ D_TOUS().forEach(r=>{ if(r[15]) { const n=String(r[13]||r[1]||''), ml=String(r[3]||'').trim();
        /* le nom affiché (13), pas celui du fichier (1) : la parenthèse du clone n'y est plus — et la contenance, que le
           nom court ne porte plus (« Bleu » 3.4 et « Bleu » 1.7 doivent se distinguer sur une ligne de vente) */
        const sz=(ml&&!new RegExp('(^|[^0-9.])'+ml.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')+'([^0-9]|$)').test(n))?' '+ml+' oz':'';
        _NOMC[r[15]]=((r[2]||'')+' '+n+sz+(r[4]?' '+r[4]:'')).trim(); } }); }catch(e){} }
  return _NOMC[cle]||(((IDX[cle]||[])[2]+' '+(IDX[cle]||[])[1]+tyTexte(cle)).trim());
}
/* Le code inconnu d'une vente de canal devient un « autre code-barres » de la fiche
   choisie : Amazon vend le Thé Blanc sous 7833…2503 quand l'inventaire dit 7833…4991
   (25 sept. 2026 : 38 commandes bloquées sur ce seul code). Une fois appris, toutes
   les ventes qui portent ce code se reconnaissent, quel que soit leur libellé. */
function fApprendCode(bc,cle){
  try{ const n=String(bc||'').replace(/[^0-9]/g,'').replace(/^0+/,''); if(n.length<8||!cle||!IDX[cle]) return false;
    if(cleDeBC(n)) return false;
    const m=Object.assign({},MOD[cle]||{}); const L=String(m.bcs||'').split(/[^0-9]+/).filter(Boolean);
    if(L.map(x=>x.replace(/^0+/,'')).includes(n)) return false;
    L.push(String(bc).replace(/[^0-9]/g,'')); m.bcs=L.join(', '); MOD[cle]=m; ecrit(KMOD,MOD); return true; }catch(e){ return false; }
}
function fApprend(des,cle){
  try{ const A=lit(K_ALIASN,{}); const M=(A&&typeof A==='object'&&!Array.isArray(A))?A:{}; const k=mNorm(des); if(!k) return; M[k]=cle; ecrit(K_ALIASN,M); }catch(e){}
}
function litAttente(v){
  /* les sacs, le port… ne sont pas des parfums : ils ne bloquent plus la vente */
  const ss=faSansService(v); if(ss.hors) v=Object.assign({},v,{lignes:ss.lignes,hors:(+v.hors||0)+ss.hors});
  const L=(v.lignes||[]).map(l=>{ const choisi=!!(l.cle&&IDX[l.cle]); let cle=(choisi?l.cle:null)||cleDeBC(l.bc)||(l.sku?cleDeBC(l.sku):null)||(l.asin?cleProcheBC(l.asin):null)||cleProcheBC(l.bc), cands=[], par=choisi?'appris':'';
    if(!cle){ const n=fParNom(l.des); if(n.cle){ cle=n.cle; par='appris'; } else cands=n.cands; }
    const q=+l.q||0;
    const qAv=cle?stkC(cle,v.lieu):null;
    /* Le site a vendu ce que l'ERP croit ne plus avoir. La vente est un fait :
       on ne la refuse pas. Mais on ne l'enregistre pas en silence non plus —
       un stock ramené à zéro sans un mot, c'est un écart que personne n'explique
       trois semaines plus tard. */
    const manque = (cle&&q>0&&qAv!=null&&q>qAv) ? q-qAv : 0;
    return {cle,par,cands,bc:l.bc||'',des:l.des||'',q,p:l.p==null?null:+l.p,qAv,manque}; });
  const connues=L.filter(l=>l.cle), inconnues=L.filter(l=>!l.cle);
  const montant=L.reduce((a,l)=>a+(l.q*(l.p||0)),0);
  const manquants=L.reduce((a,l)=>a+l.manque,0);
  /* Un retour (commande remboursée ou annulée par le site, annulation Amazon) :
     on cherche la vente d'origine ici. Si elle y est, le retour s'y rattache et
     le stock revient — jamais plus que ce qui en est sorti. Si elle n'y est pas
     (commande annulée avant d'avoir été enregistrée), rien ne revient en stock :
     on n'a pas sorti ces flacons, il n'y a rien à remettre. */
  let orig=null, motif='';
  if(v.annule){
    orig=FACT.find(f=>f.sens==='vente'&&!f.retour&&f.num===String(v.num||'')&&(f.auto===v.src||!f.auto))||null;
    motif=MOTIF_F[v._i]||v.motif||'retour';
  }
  return {v,L,connues,inconnues,montant,manquants,unites:L.reduce((a,l)=>a+l.q,0),orig,motif};
}
/* le motif choisi dans la file, avant l'enregistrement (par vente en attente) */
const MOTIF_F={};
const KEXP='expeditions-v1';
const SRC_C={woocommerce:'Site perfumestrade.com','woocommerce-gros':'Site wholesale.perfumestrade.com',lightspeed:'Caisse Lightspeed',shopify:'Shopify',amazon:'Amazon',message:'Commande par message'};
function peintFile(){
  const el=$('file'); if(!el) return;
  const F=litFile();
  if(!F.length){ el.innerHTML=''; return; }
  /* la plus récente en haut, comme le journal en dessous (Igal, 24 sept. 2026) */
  const A=F.map(litAttente).sort((a,b)=>String(b.v.d||'').localeCompare(String(a.v.d||''))||String(b.v.h||'').localeCompare(String(a.v.h||''))||String(b.v.recu||'').localeCompare(String(a.v.recu||'')));
  const tot=A.reduce((a,x)=>a+x.montant,0);
  const nInc=A.filter(x=>x.inconnues.length).length;
  const aDecouvert=A.filter(x=>!x.inconnues.length&&x.manquants>0);
  const totManque=aDecouvert.reduce((a,x)=>a+x.manquants,0);
  const SRC={woocommerce:'Site','woocommerce-gros':'Site gros',lightspeed:'Caisse',shopify:'Shopify',amazon:'Amazon',message:'Message client'};
  el.innerHTML=`<div class="file">
    <div class="ft">
      <b>${nf(F.length)} vente${F.length>1?'s':''} en attente d'une référence</b>
      <span style="color:var(--ink-2)">${money(tot)}</span>
      <span class="sp"></span>
      <button class="btn" id="f-vider">Tout ignorer</button>
      <button class="btn pri" id="f-ok"${(F.length-nInc)>0?'':' hidden'}>Enregistrer ${nf(F.length-nInc>0?F.length-nInc:0)} vente${F.length-nInc>1?'s':''}</button>
      <span class="aide">Les ventes du site et de la caisse s'enregistrent toutes seules à l'ouverture de l'outil.
      Celles-ci n'ont pas pu l'être : un parfum porte un code que le catalogue ne connaît pas, et le stock
      d'un parfum inconnu ne peut pas bouger. Clique sur la vente pour la voir en entier et dire quel
      parfum c'est — ce nom sera reconnu la prochaine fois. Si aucun parfum ne ressemble,
      il faut d'abord créer la référence au catalogue, ou ignorer la vente.</span>
      ${aDecouvert.length?`<span class="dec"><b>${nf(aDecouvert.length)} vente${aDecouvert.length>1?'s':''} porte${aDecouvert.length>1?'nt':''} sur du stock que l'outil n'a pas</b> —
        ${nf(totManque)} flacon${totManque>1?'s':''} de plus que ce qui est compté ici. Elles seront enregistrées quand même :
        la vente a eu lieu. Le stock concerné tombera à zéro, et l'écart part au journal.
        Si le chiffre te surprend, c'est l'inventaire de l'outil qu'il faut regarder, pas le site.</span>`:''}
    </div>
    <table><thead><tr><th>Quand</th><th>D'où</th><th>N°</th><th>Client</th><th>Contenu</th>
      <th class="r">Montant</th><th class="r"></th></tr></thead><tbody>
      ${A.slice(0,40).map((x,i)=>`<tr class="fl-row" data-fatt="${esc(x.v._i)}" title="Cliquer pour voir la vente en entier">
        <td>${esc(/^\d{4}-\d\d-\d\d$/.test(x.v.d||'')?dfr(x.v.d):(x.v.d||''))}${x.v.h?`<span class="lg">${esc(x.v.h)}</span>`:''}</td>
        <td><span class="src">${esc(SRC[x.v.src]||x.v.src||'')}</span>${x.v.lieu?`<span class="lg">${esc(x.v.lieu)}</span>`:''}</td>
        <td>${esc(x.v.num||'—')}</td>
        <td>${cliAff(x.v.client,SRC[x.v.src]||x.v.src)}</td>
        <td>${x.v.annule?'<span class="ret">retour</span> · '+(x.orig?'<span>rattaché à la vente</span> <span class="nm">'+esc(x.orig.num)+'</span> · ':'<span>vente d\'origine inconnue ici</span> · '):''}${nf(x.L.length)} parfum${x.L.length>1?'s':''}
          ${x.inconnues.length
            ?`<span class="fet inc">incomplète · ${nf(x.inconnues.length)} à identifier</span>`
            :`<span class="fet ok">complète</span>`}
          ${x.manquants?`<span class="mq">· ${nf(x.manquants)} flacon${x.manquants>1?'s':''} de plus que le stock</span>`:''}
          <span class="lg">${x.L.slice(0,3).map(l=>esc((l.cle?((IDX[l.cle]||[])[2]+' '+(IDX[l.cle]||[])[1]):(l.des||l.bc))+' ×'+l.q)).join(' · ')}${x.L.length>3?' …':''}</span></td>
        <td class="r">${money2(x.montant)}</td>
        <td class="r"><button class="btn sm" data-fvoir="${esc(x.v._i)}">${x.inconnues.length?'Compléter':'Voir'}</button>
          ${x.inconnues.length?'':`<button class="btn sm pri" data-fok="${esc(x.v._i)}" title="Enregistrer seulement cette vente, et laisser les autres en attente">Enregistrer</button> `}<button class="btn sm" data-fsup="${esc(x.v._i)}" title="Retirer cette vente de la file sans l'enregistrer">Ignorer</button></td>
      </tr>`).join('')}
    </tbody></table>
    ${A.length>40?`<div style="padding:9px 14px;color:var(--ink-3);font-size:12.5px">et ${nf(A.length-40)} de plus…</div>`:''}
  </div>`;
  $('f-ok').disabled = (F.length-nInc)<=0;
  $('f-ok').onclick=()=>enregistreFile();
  $('f-vider').onclick=videFile;
  el.querySelectorAll('[data-fsup]').forEach(b=>b.onclick=()=>retireDeFile([b.dataset.fsup],'ignorée'));
  el.querySelectorAll('[data-fok]').forEach(b=>b.onclick=()=>enregistreFile([b.dataset.fok]));
  el.querySelectorAll('[data-fok],[data-fsup],[data-fvoir]').forEach(b=>b.addEventListener('click',e=>e.stopPropagation()));
  el.querySelectorAll('[data-fvoir]').forEach(b=>b.onclick=()=>ouvreAttente(b.dataset.fvoir));
  el.querySelectorAll('tr.fl-row').forEach(tr=>tr.onclick=()=>ouvreAttente(tr.dataset.fatt));
}

/* ---------- la fiche d'une vente en attente ----------
   Igal, 24 sept. 2026 : « je ne trouve pas clair les "c'est lequel ?" ; j'aimerais
   cliquer sur la vente et avoir un vrai aperçu, et voir que c'est incomplet ».
   Donc : une fiche par vente, comme pour une vente enregistrée. Elle montre la
   vente entière, dit d'un mot si elle est complète ou non, et c'est DANS la
   fiche qu'on identifie un parfum inconnu. Le choix est retenu (le nom sera
   reconnu la prochaine fois) et, dès que plus rien ne manque, la vente
   s'enregistre — comme elle l'aurait fait toute seule à la prochaine ouverture.
   Tant qu'il manque un parfum, elle reste ici, et le stock ne bouge pas. */
function ouvreAttente(id){
  const v=litFile().find(z=>z._i===id); if(!v){ peintFile(); return; }
  const x=litAttente(v);
  const SRC={woocommerce:'Site perfumestrade.com','woocommerce-gros':'Site wholesale.perfumestrade.com',lightspeed:'Caisse Lightspeed',shopify:'Shopify',amazon:'Amazon',message:'Commande par message'};
  const inc=x.inconnues.length;
  DETAIL={attente:id};
  $('d-tit').innerHTML=`${x.v.annule?'Retour':'Vente'} <span class="nm">${esc(x.v.num||'')}</span>
    <span class="fet ${inc?'inc':'ok'}" style="margin-left:8px;vertical-align:middle">${inc?'incomplète':'complète'}</span>
    <span class="sub"><span class="ch">${esc(SRC[x.v.src]||x.v.src||'')}</span>
    <span class="nm">${x.v.d?dfr(x.v.d):''}${x.v.h?' · '+esc(x.v.h):''}${x.v.lieu?' · '+esc(x.v.lieu):''}${faNomClient(x.v.client)?' · '+esc(faNomClient(x.v.client)):''}</span></span>`;
  const l=[];
  if(inc) l.push(`<div class="blo fl-inc"><h4>Ce qui manque</h4>
    <p class="nt" style="margin:0"><b>${nf(inc)} parfum${inc>1?'s':''} de cette vente ${inc>1?'ne sont pas reconnus':"n'est pas reconnu"}</b> par le catalogue :
    le code envoyé par le canal de vente ne correspond à aucune fiche. Tant qu'il manque un parfum,
    la vente attend ici et le stock ne bouge pas. Choisis-le dans la liste ci-dessous : la vente s'enregistre aussitôt, et ce nom sera reconnu la prochaine fois.</p></div>`);
  else if(x.manquants) l.push(`<div class="blo"><h4>À savoir</h4><p class="nt" style="margin:0">Cette vente porte sur <b>${nf(x.manquants)} flacon${x.manquants>1?'s':''} de plus</b> que ce que l'outil compte en stock.
    Elle sera enregistrée quand même (la vente a eu lieu) : le stock tombera à zéro et l'écart ira au journal.</p></div>`);
  l.push(`<div class="blo"><h4>${x.v.annule?'Le retour':'La vente'} · ${nf(x.L.length)} parfum${x.L.length>1?'s':''}</h4>
    <table><tbody>${x.L.map((li,j)=>({li,j})).sort((u,w)=>(u.li.cle?1:0)-(w.li.cle?1:0)).map(({li,j})=>{
      const nom=li.cle?fNomComplet(li.cle):'';
      const stk=li.cle?stkC(li.cle,x.v.lieu):null;
      return `<tr class="${li.cle?'':'fl-manque'}">
        <td>${li.cle
          ?`<b class="nm">${esc(nom)}</b>${li.par==='appris'?'<small>reconnu d\'après un choix précédent</small>':''}${li.bc?`<small class="bc">${esc(li.bc)}</small>`:''}${li.manque?`<small style="color:var(--warn)">${nf(li.manque)} de plus que le stock (${nf(stk)} compté${stk>1?'s':''})</small>`:''}`
          :`<b class="nm">${esc(li.des||li.bc||'?')}</b><small>${li.bc?'<span>code</span> <span class="bc">'+esc(li.bc)+'</span> · ':''}<span style="color:var(--crit)">inconnu du catalogue</span></small>
            <div class="fl-choix">
            ${li.cands.length?`<select class="fl-sel" data-j="${j}" data-anom="${esc(li.des)}" data-abc="${esc(li.bc||'')}"><option value="">Quel parfum est-ce ?</option>${li.cands.map(c=>`<option value="${esc(c.cle)}">${esc(fNomComplet(c.cle))}</option>`).join('')}</select>`:''}
            <input class="fl-cherche" list="fl-cat" data-j="${j}" data-anom="${esc(li.des)}" data-abc="${esc(li.bc||'')}" placeholder="${li.cands.length?'ou tape son nom ou son code-barres…':'Tape le nom ou le code-barres du parfum…'}" autocomplete="off">
            <small>Absent du catalogue ? Crée-le d'abord dans le <a href="catalogue.html">Catalogue</a> (« + Nouvel article »), puis reviens ici.</small></div>`}</td>
        <td class="r">${nf(li.q)} ×<br><small>${li.p!=null?money2(li.p):'—'}</small></td>
        <td class="r"><b>${money2(li.q*(li.p||0))}</b></td>
      </tr>`; }).join('')}</tbody></table>
    <div class="pl gr" style="margin-top:8px"><span>${nf(x.unites)} flacon${Math.abs(x.unites)>1?'s':''}</span><b>${money2(x.montant)}</b></div>
    ${x.v.total!=null&&Math.abs((+x.v.total||0)-x.montant)>0.05?`<p class="nt"><span>Le canal annonce un total de</span> <b class="mq">${money2(+x.v.total)}</b> <span>(frais de port, taxes ou remise non détaillés ici).</span></p>`:''}
  </div>`);
  if(x.v.annule) l.push(`<div class="blo"><h4>Retour</h4>
    <div class="pl"><span>Motif</span><b><select id="fa-motif">${MOTIFS_R.map(([k,lb])=>`<option value="${k}"${k===x.motif?' selected':''}>${esc(lb)}</option>`).join('')}</select></b></div>
    <p class="nt" style="margin:6px 0 0">${x.orig?`<span>Rattaché à la vente</span> <b class="nm">${esc(x.orig.num)} · ${dfr(x.orig.d)}</b> <span>: le stock revient.</span>`:`<b>Vente d'origine inconnue ici</b> : le stock ne bougera pas.`}</p></div>`);
  l.push(`<div class="blo"><h4>Reçu</h4>
    <div class="pl"><span>Déposé par le cockpit le</span><b>${x.v.recu?esc(quandMiami(x.v.recu)):'—'}</b></div>
    ${x.v.hors?`<div class="pl"><span>Lignes de service mises de côté (port, sachet…)</span><b>${nf(x.v.hors)}</b></div>`:''}
  </div>`);
  l.push('<datalist id="fl-cat"></datalist>');
  $('d-corps').innerHTML=l.join('');
  if(document.querySelector('.fl-cherche')){ const dl=$('fl-cat');
    dl.innerHTML=Object.keys(IDX).map(k=>`<option data-cle="${esc(k)}" value="${esc(fNomComplet(k)+((IDX[k]||[])[0]?' — '+IDX[k][0]:''))}">`).join(''); }
  $('d-pied').innerHTML=`<button class="btn" id="fa-sup">Ignorer cette vente</button><span style="flex:1"></span>
    <button class="btn" id="d-ok">Fermer</button>
    <button class="btn pri${inc?' off':''}" id="fa-ok"${inc?' aria-disabled="true" title="Il reste un parfum à identifier"':''}>Enregistrer</button>`;
  $('dov').classList.add('on');
  $('d-ok').onclick=fermeDetail;
  $('fa-sup').onclick=()=>{ fermeDetail(); retireDeFile([id],'ignorée'); };
  $('fa-ok').onclick=()=>{ if(inc){ const m=document.querySelector('#d-corps tr.fl-manque'); if(m){ m.scrollIntoView({block:'center'}); const c=m.querySelector('select,input'); if(c) c.focus(); } return; } fermeDetail(); enregistreFile([id]); };
  const fm=$('fa-motif'); if(fm) fm.onchange=()=>{ MOTIF_F[id]=fm.value; };
  /* le parfum choisi : posé sur la ligne de CETTE vente (même quand le canal n'a envoyé ni nom
     ni code), et retenu par son nom et son code pour les ventes suivantes */
  const choisit=(sl,cle)=>{ if(!cle||!IDX[cle]) return;
    try{ const F=litFile(); const vv=F.find(z=>z._i===id); const lg=vv&&(vv.lignes||[])[+sl.dataset.j];
      if(lg){ lg.cle=cle; ecrit(KFILE,F); } }catch(e){}
    if(sl.dataset.anom) fApprend(sl.dataset.anom,cle);
    const codeAppris=sl.dataset.abc?fApprendCode(sl.dataset.abc,cle):false;
    try{ const J=lit(KJOU,[]); J.push({t:new Date().toISOString(),u:USR||'(non renseigné)',act:'vente',lib:'nom reconnu : « '+(sl.dataset.anom||sl.dataset.abc||'ligne sans nom')+' » = '+fNomComplet(cle)+(codeAppris?' — le code '+sl.dataset.abc+' est ajouté à la fiche (autres codes-barres)':''),ref:cle,av:null,ap:codeAppris?sl.dataset.abc:null}); ecrit(KJOU,J); }catch(e){}
    /* Le nom est retenu. Si plus rien ne manque, la vente s'enregistre tout de suite —
       comme elle l'aurait fait toute seule à la prochaine ouverture (Igal, 12 sept. :
       plus de validation). Et les autres ventes de la file qui attendaient ce même
       nom partent avec elle. S'il manque encore un parfum, la fiche reste ouverte. */
    const encore=litFile().find(z=>z._i===id);
    if(encore && litAttente(encore).inconnues.length){ peintFile(); ouvreAttente(id); return; }
    fermeDetail(); enregistreFile(undefined,true); };
  document.querySelectorAll('.fl-sel').forEach(sl=>sl.onchange=()=>choisit(sl,sl.value));
  document.querySelectorAll('.fl-cherche').forEach(inp=>inp.onchange=()=>{
    const o=[...$('fl-cat').options].find(op=>op.value===inp.value);
    if(o) choisit(inp,o.dataset.cle); });
}
/* « muet » : quand c'est l'enregistrement qui appelle, il a DÉJÀ écrit sa ligne de
   journal, avec le montant et le détail du stock. En écrire une deuxième ici donnait
   deux lignes pour un seul geste — et la seconde disait « 1 vente de la file
   enregistrées ». Un journal qu'on relit pour comprendre un écart de stock ne doit
   pas raconter la même chose deux fois. */
function retireDeFile(ids,mot,muet){
  const S=new Set(ids);
  const reste=litFile().filter(x=>!S.has(x._i));
  ecrit(KFILE,reste);
  if(!muet){
    const J=lit(KJOU,[]); J.push({t:new Date().toISOString(),u:USR||'(non renseigné)',act:'vente',
      lib:ids.length+' vente'+(ids.length>1?'s':'')+' de la file '+mot,ref:'',av:null,ap:reste.length+' en attente'});
    ecrit(KJOU,J);
  }
  peintFile();
  return reste.length;
}
function videFile(){
  const F=litFile(); if(!F.length) return;
  if(!confirm('Ignorer les '+F.length+' ventes en attente ?\n\nElles ne seront pas enregistrées et disparaîtront de la liste. Le site et la caisse, eux, gardent leur trace.')) return;
  if(!signe("vider la file d'attente",()=>{})) return;
  retireDeFile(F.map(x=>x._i),'ignorées');
}
/* Enregistrer : une facture par vente, le stock qui bouge, la file qui se vide. */
/* On peut enregistrer TOUTE la file, ou une seule vente.
   Le « tout ou rien » était un vrai manque : le jour où une commande paraît fausse,
   il fallait choisir entre l'accepter avec les autres et tout ignorer. Maintenant on
   traite les bonnes et on laisse la douteuse en attente, le temps de vérifier. */
/* 20 oct. 2026 : en ligne, la vente sort du stock RELU sur le serveur à l'instant, pas de la copie de ce
   navigateur (voir __syFrais dans _serveur.py). Serveur muet : rien n'est enregistré, on le dit. */
function relitStock(){
  MOD=lit(KMOD,{}); if(!MOD||typeof MOD!=='object') MOD={};
  try{ EXT=Object.assign({q:{}},JSON.parse(localStorage.getItem(KEXT)||'{}')); }catch(e){}
  _PCI=null;
}
function surStockServeur(faire,bouton){
  if(!(typeof window.__syEnLigne==='function'&&window.__syEnLigne()&&typeof window.__syFrais==='function')) return faire();
  if(bouton) bouton.disabled=true;
  window.__syFrais().then(ok=>{
    if(bouton) bouton.disabled=false;
    if(!ok){ alert(L3("Le serveur ne répond pas : rien n'a été enregistré, pour ne pas sortir le stock d'une copie périmée. Réessaie dans un instant.",
      "The server is not answering: nothing was saved, so as not to take stock from an outdated copy. Try again in a moment.",
      "El servidor no responde: no se ha guardado nada, para no descontar el stock de una copia desactualizada. Inténtalo de nuevo en un momento.")); return; }
    relitStock(); faire(); });
}
function enregistreFile(seulement,auto){
  if(!window.__FRAIS_OK) return surStockServeur(()=>{ window.__FRAIS_OK=true; try{ enregistreFile(seulement,auto); } finally { window.__FRAIS_OK=false; } }, $('f-ok'));
  const S = Array.isArray(seulement) && seulement.length ? new Set(seulement) : null;
  const A0=litFile().map(litAttente)
    .filter(x=>!x.inconnues.length&&x.L.length)
    .filter(x=>!S||S.has(x.v._i));
  if(!A0.length) return;
  /* Les commandes d'un canal qui livre (site, Amazon) ne sortent pas du stock ici :
     elles vont dans Expéditions, et c'est le geste « expédiée le … » qui fera la
     facture. Une annulation d'une commande encore à expédier s'y règle aussi. */
  const A=[], EXP=[], annIds=[]; let nAnn=0;
  { const J0=lit(KJOU,[]);
    A0.forEach(x=>{
      if(x.v.annule&&typeof faAnnuleAvantExp==='function'&&faAnnuleAvantExp(x.v,J0,USR||'(non renseigné)')){ nAnn++; annIds.push(x.v._i); return; }
      if(!x.v.annule&&typeof faExpedie==='function'&&faExpedie(x.v.src)) EXP.push(x); else A.push(x); });
    if(nAnn) ecrit(KJOU,J0); }
  if(EXP.length){
    const E=faLitExp(), t=new Date().toISOString();
    EXP.forEach(x=>{ const v=x.v; if(E.some(e=>e._i===v._i)) return;
      E.push({_i:v._i,src:v.src,num:v.num||'',client:faNomClient(v.client),email:v.email||undefined,tel:v.tel||undefined,ville:v.ville||undefined,pays:v.pays||undefined,d:v.d||ajd(),h:v.h||'',recu:v.recu||'',total:v.total==null?null:+v.total,hors:v.hors||0,lieu:v.lieu||'',
        lignes:x.L.map(l=>({cle:l.cle,bc:l.bc,des:l.des,q:l.q,p:l.p,ref:(((IDX[l.cle]||[])[2]||'')+' '+((IDX[l.cle]||[])[1]||'')+tyTexte(l.cle)).trim()})),
        montant:x.montant,arrive:t,statut:'attente'}); });
    ecrit(KEXP,E);
    const J=lit(KJOU,[]); J.push({t,u:USR||'(non renseigné)',act:'vente',lib:EXP.length+' commande'+(EXP.length>1?'s':'')+' à expédier ('+[...new Set(EXP.map(x=>SRC_C[x.v.src]||x.v.src))].join(', ')+') — le stock sortira à l\'expédition',ref:'',av:null,ap:Math.round(EXP.reduce((a,x)=>a+x.montant,0))+' $'}); ecrit(KJOU,J);
  }
  if(nAnn||EXP.length){ retireDeFile([...EXP.map(x=>x.v._i),...annIds],'',true); }
  if(EXP.length&&!A.length){
    const b=document.createElement('div'); b.className='info';
    b.innerHTML=`<b>${nf(EXP.length)} commande${EXP.length>1?'s':''} à expédier</b> — le stock ne bouge pas encore : il sortira quand quelqu'un l'aura marquée « expédiée » dans <a href="expeditions.html">Expéditions</a>.`;
    const w=document.querySelector('.wrap')||document.body; w.insertBefore(b,w.firstChild); setTimeout(()=>b.remove(),9000);
  }
  if(!A.length){ peintFile(); return; }
  /* Ce qui se vend à découvert doit être dit AVANT, pas découvert après. */
  const dec=A.filter(x=>x.manquants>0), totM=dec.reduce((a,x)=>a+x.manquants,0);
  if(dec.length && !auto && !confirm(
      dec.length+' vente'+(dec.length>1?'s':'')+' porte'+(dec.length>1?'nt':'')+
      ' sur '+totM+' flacon'+(totM>1?'s':'')+" de plus que ce que l'outil compte en stock.\n\n"+
      "Elles seront enregistrées : la vente a bien eu lieu. Le stock de ces références tombera à zéro,\n"+
      "et l'écart sera inscrit au journal pour qu'on puisse le retrouver.\n\n"+
      "Continuer ?")) return;
  if(!signe(A.length>1?"ces ventes":"cette vente",()=>enregistreFile(seulement,auto))) return;
  _PCI=null;
  const VENT=lit(KVENT,{}), CLI=lit(KCLI,{}), J=lit(KJOU,[]);
  const SRC={woocommerce:'Site perfumestrade.com','woocommerce-gros':'Site wholesale.perfumestrade.com',lightspeed:'Caisse Lightspeed',shopify:'Shopify',amazon:'Amazon',message:'Commande par message'};
  let nL=0, mt=0;
  const faits=[], ecarts=[];
  const retours=[];
  A.forEach(x=>{
    const v=x.v, canal=v.lieu||SRC[v.src]||'Autre';
    if(v.annule){
      /* un retour : rattaché à la vente d'origine, avec son motif, comme un
         remboursement fait à la main — et le stock ne revient que si la vente
         est connue ici, à hauteur de ce qui en était sorti */
      const o=x.orig, rendu=o?dejaRendu(o.id):{};
      const pcR=!!(o&&o.pc);                      /* la vente d'origine était une vente Perfume City */
      const lignes=x.L.map(l=>{ const n=Math.abs(l.q); const qAv=pcR?pcQte(l.cle):qteEff(l.cle); let qAp=qAv;
        if(o){ const lo=(o.lignes||[]).find(z=>z.cle===l.cle);
          const sorti=lo?Math.max(0,(lo.qAv==null||lo.qAp==null)?(lo.q||0):(lo.qAv-lo.qAp)):0;
          qAp=qAv+Math.min(n,Math.max(0,sorti-(rendu[l.cle]||0))); }
        if(qAp!==qAv){ if(pcR) pcPose(l.cle,qAp); else MOD[l.cle]=Object.assign({},MOD[l.cle]||{},{qte:qAp}); }
        nL++; mt-=n*(l.p||0);
        const ref=(((IDX[l.cle]||[])[2]||'')+' '+((IDX[l.cle]||[])[1]||'')+tyTexte(l.cle)).trim();
        (VENT[l.cle]=VENT[l.cle]||[]).push({d:v.d,h:v.h||undefined,p:l.p,c:faNomClient(v.client),q:-n,num:(o?o.num:v.num||'')+' (remboursé)',k:canal});
        return {cle:l.cle,bc:l.bc,ref,q:-n,p:l.p,qAv,qAp,pc:pcR||undefined,paAv:o?((o.lignes||[]).find(z=>z.cle===l.cle)||{}).paAv:paEff(l.cle)}; });
      const mtR=lignes.reduce((a,l)=>a+Math.abs(l.q)*(l.p||0),0);
      const nR=o?FACT.filter(z=>z.retour&&z.refId===o.id).length+1:1;
      const num=(o?o.num:(v.num||'AUTO'))+'-R'+nR;
      FACT.push({id:'r'+Date.now().toString(36)+Math.random().toString(36).slice(2,5),num,sens:'vente',retour:true,
        refId:o?o.id:'',refNum:o?o.num:(v.num||''),canal,pc:pcR||undefined,tiers:faNomClient(v.client)||(o?o.tiers:'')||'',d:v.d||ajd(),h:v.h||undefined,lignes,
        montant:-mtR,stock:!!o,mode:x.motif==='annulation'?'aucun':'carte',motif:x.motif,
        note:(SRC[v.src]||v.src||'')+(o?'':" — vente d'origine inconnue ici, stock inchangé"),
        par:USR||'(automatique)',t:new Date().toISOString(),auto:v.src||''});
      retours.push({num,mt:mtR,orig:!!o,motif:x.motif});
      faits.push(v._i);
      return;
    }
    const pcV=estPC(canal);                       /* une vente Perfume City sort de l'inventaire Perfume City */
    const lignes=x.L.map(l=>{ const qAv=pcV?pcQte(l.cle):qteEff(l.cle), qAp=Math.max(0,qAv-l.q);
      if(pcV) pcPose(l.cle,qAp); else MOD[l.cle]=Object.assign({},MOD[l.cle]||{},{qte:qAp});
      nL++; mt+=l.q*(l.p||0);
      const ref=(((IDX[l.cle]||[])[2]||'')+' '+((IDX[l.cle]||[])[1]||'')+tyTexte(l.cle)).trim();
      (VENT[l.cle]=VENT[l.cle]||[]).push({d:v.d,h:v.h||undefined,p:l.p,c:faNomClient(v.client),q:l.q,num:v.num||'',k:canal});
      if(l.manque) ecarts.push({num:v.num||'',bc:l.bc,ref,vendu:l.q,stock:qAv,manque:l.manque});
      return {cle:l.cle,bc:l.bc,ref,q:l.q,p:l.p,qAv,qAp,pc:pcV||undefined,paAv:paEff(l.cle),manque:l.manque||undefined}; });
    faClientPose(CLI,v);
    const fa={id:'c'+Date.now().toString(36)+Math.random().toString(36).slice(2,5),
      num:(v.num||('AUTO-'+Date.now().toString(36))),sens:'vente',canal,export:canal,
      tiers:faNomClient(v.client),d:v.d||ajd(),h:v.h||undefined,lignes,
      montant:x.montant,stock:true,pc:pcV||undefined,par:USR||'(automatique)',t:new Date().toISOString(),
      auto:v.src||''};
    /* 20 oct. 2026 (commande 23082) : validée à la main depuis la file, la vente perdait l'heure de réception
       par le serveur (« Reçue par le serveur : — ») et le port payé par le client. Elle les garde, comme
       une vente enregistrée automatiquement, avec la même identité (deux onglets = une seule vente). */
    if(v.recu) fa.recu=String(v.recu); if(v.arrive) fa.arrive=String(v.arrive);
    if(+v.port>0) fa.port=Math.round(+v.port*100)/100;
    if(+v.taxe>0) fa.taxe=Math.round(+v.taxe*100)/100;
    if(v.paie&&typeof v.paie==='object') fa.paie=v.paie;        /* 24 oct. 2026 : espèces / carte / autre */
    if(v._i) fa._i='fa|'+v._i;
    if(typeof faPoste==='function'){ const p=faPoste(); if(p) fa.poste=p; }
    if(typeof docAutoPour==='function') fa.doc=docAutoPour(fa,FACT);
    FACT.push(fa);
    faits.push(v._i);
  });
  pcSauve();
  ecrit(KFACT,FACT); ecrit(KMOD,MOD); ecrit(KVENT,VENT); ecrit(KCLI,CLI);
  const reste=retireDeFile(faits,'enregistrées',true);
  J.push({t:new Date().toISOString(),u:USR||'(non renseigné)',act:'vente',
    lib:faits.length+' vente'+(faits.length>1?'s':'')+' enregistrée'+(faits.length>1?'s':'')+' depuis la file — '+nL+' ligne(s)'
        +(reste?', '+reste+' encore en attente':''),
    ref:'',av:null,ap:Math.round(mt)+' $'});
  /* L'écart de stock a sa propre ligne de journal, avec le détail : c'est elle
     qu'on relira le jour où quelqu'un demandera pourquoi une référence est à zéro. */
  retours.forEach(r=>J.push({t:new Date().toISOString(),u:USR||'(non renseigné)',act:'annulation',
    lib:'remboursement '+r.num+' — '+((MOTIFS_R.find(m=>m[0]===r.motif)||['','retour'])[1]).toLowerCase()+(r.orig?', stock remis':", vente d'origine inconnue, stock inchangé"),
    n:0,impact:Math.round(r.mt),det:[]}));
  if(ecarts.length) J.push({t:new Date().toISOString(),u:USR||'(non renseigné)',act:'stock',
    lib:'vendu à découvert — '+ecarts.reduce((a,e)=>a+e.manque,0)+' flacon(s) de plus que le stock compté, sur '+ecarts.length+' ligne(s)',
    ref:'',av:null,ap:ecarts.map(e=>e.ref.trim()+' : vendu '+e.vendu+', en stock '+e.stock).join(' · '),
    n:ecarts.length,det:ecarts});
  ecrit(KJOU,J);
  construitV(); vus=80; dessine();
  const b=document.createElement('div'); b.className='info';
  b.innerHTML=`<b>${nf(faits.length)} vente${faits.length>1?'s':''} enregistrée${faits.length>1?'s':''}</b>
    — ${nf(nL)} ligne${nL>1?'s':''}, ${money(mt)}. Le stock a été mis à jour.`
    + (ecarts.length?`<br><b style="color:var(--crit)">${nf(ecarts.reduce((a,e)=>a+e.manque,0))} flacon${ecarts.reduce((a,e)=>a+e.manque,0)>1?'s':''} vendu${ecarts.reduce((a,e)=>a+e.manque,0)>1?'s':''} à découvert</b> :
       ${ecarts.slice(0,3).map(e=>esc(e.ref.trim())+' (vendu '+e.vendu+', en stock '+e.stock+')').join(', ')}${ecarts.length>3?`, et ${nf(ecarts.length-3)} autre${ecarts.length-3>1?'s':''}`:''}.
       Le détail est dans le <a href="journal.html">journal</a>.`:'');
  const w=document.querySelector('.wrap')||document.body; w.insertBefore(b,w.firstChild);
  setTimeout(()=>b.remove(),9000);
}
/* quand le serveur dépose de nouvelles ventes, la liste se redessine toute seule */
if(typeof _apresEcrit!=='undefined') _apresEcrit.push(cle=>{ if(cle===KFILE) peintFile(); });
/* appelé par la veille du serveur quand des ventes arrivent (voir _serveur.py) :
   on relit et on redessine sur place, sans recharger la page */
window.__rafraichir=()=>{ const y=window.scrollY;
  const F=lit(KFACT,[]); if(Array.isArray(F)) FACT=F; const M=lit(KMOD,{}); if(M&&typeof M==='object') MOD=M;
  construitV(); peintFile(); dessine();
  /* les cotes Lightspeed aussi — sauf si une conversion est en train d'être remplie */
  try{ if(typeof lscPeint==='function' && !LSQ_CONV) lscPeint(); }catch(e){}
  window.scrollTo(0,y); };

/* ce que coûte UN envoi à Sam, par canal (Réglages › Coût d'un envoi) — 8 $ si rien n'est réglé */
const ENVOI_DEF=8;
const carteTaux=()=>{ const v=REG&&REG.carteLS; return (v==null||v===''||isNaN(+v))?2.6:Math.max(0,+v); };   /* frais de carte Lightspeed, % (25 oct. 2026) */
function envoiDe(src){ const E=(REG&&REG.envois)||{}; const v=E[src]; return (v==null||v===''||isNaN(+v))?ENVOI_DEF:Math.max(0,+v); }
/* ---------------- les canaux de vente et leur commission ---------------- */
const CANAUX_DEF=[{id:'site',nom:'Site perfumestrade.com',maj:0,com:3},
  {id:'sitegros',nom:'Site wholesale.perfumestrade.com',base:'pvw',maj:0,com:3},{id:'amazon',nom:'Amazon',maj:18,com:15},{id:'perfumecity',nom:'Perfume City',maj:0,com:3}];
/* tant que le Catalogue ou les Réglages n'ont pas fait le changement du 24 sept.
   (Shopify retiré, site de gros ajouté), on le fait ici en lecture seulement */
const canauxReg=()=>{ let L=(REG.canaux&&REG.canaux.length?REG.canaux:CANAUX_DEF);
  if((REG.canauxV||0)<2){ L=L.filter(c=>c.id!=='shopify'); if(!L.some(c=>c.id==='sitegros')){ const i=L.findIndex(c=>c.id==='site'); L=L.slice(); L.splice(i>=0?i+1:L.length,0,CANAUX_DEF.find(c=>c.id==='sitegros')); } }
  /* 27 sept. : le canal « Boutique » est retiré (tout passe par la caisse Lightspeed) */
  if((REG.canauxV||0)<3) L=L.filter(c=>c.id!=='boutique');
  /* 17 oct. 2026 (Igal) : Shopify prend 3 % comme WooCommerce → Perfume City à 3 % (lecture seule ; Catalogue/Réglages l'écrivent une fois) */
  if(!REG.pcCom3) L=L.map(c=>(c.id==='perfumecity'&&!(+c.com))?Object.assign({},c,{com:3}):c);
  return L; };
/* la vente en gros et la caisse ne sont pas des canaux de prix : ce sont des façons de vendre */
const CANAUX_VENTE=()=>[...canauxReg().map(c=>({id:c.id,nom:c.nom,com:c.com||0,maj:c.maj||0,base:c.base||''})),
  {id:'gros',nom:'Gros',com:0,maj:0},{id:'caisse',nom:'Caisse Lightspeed',com:0,maj:0},{id:'autre',nom:'Autre',com:0,maj:0}];
/* La marge affichée est la marge NETTE : ce qui reste une fois la commission du canal
   prélevée. Amazon garde 15 %, Shopify et le site 3 %. La commission est retrouvée par le
   nom du canal enregistré sur la vente. Si ce nom ne correspond à aucun canal des Réglages
   (canal renommé ou supprimé depuis), on ne devine pas : la commission vaut 0 et la vente
   est signalée, plutôt que de voir la marge de tout l'historique bouger en silence. */
let CANAL_INCONNU=new Set();
/* Qui est ce canal : le site dont on montre l'icône (celle du canal lui-même, jamais
   redessinée), un nom court pour l'onglet, un signe de secours si l'icône ne vient pas.
   Les canaux qui arrivent tout seuls par le cockpit (site de gros, caisse) ne sont pas
   forcément dans les Réglages : on les reconnaît quand même, sans crier à l'inconnu. */
function identCanal(nom){
  const n=String(nom||'').toLowerCase();
  if(n.includes('wholesale'))     return {dom:'wholesale.perfumestrade.com',court:'wholesale.perfumestrade.com',ic:'🚚',fixe:true,direct:true};
  if(n.includes('perfumestrade')) return {dom:'perfumestrade.com',court:'perfumestrade.com',ic:'🛒',fixe:true,direct:true};
  if(n.includes('amazon'))        return {dom:'amazon.com',court:'Amazon',ic:'📮',fixe:true};
  if(n.includes('shopify'))       return {dom:'shopify.com',court:'Shopify',ic:'🏬',fixe:true};
  if(n.includes('lightspeed')||n.includes('caisse')) return {dom:'lightspeedhq.com',court:'Lightspeed',ic:'🧾',fixe:true,com:0};
  if(/perfume\s*(in\s*the\s*)?city/.test(n))  return {court:'Perfume in the City',ic:'🏬',fixe:true};   /* le nom de la boutique de Kim (Igal, 13 oct. 2026) ; le nom ENREGISTRÉ sur la vente ne change pas */
  /* 27 sept. (Igal) : « Gros » et « Boutique » ne disaient pas ce que c'était → « Vente en gros »
     et « Vente au détail ». Le nom ENREGISTRÉ sur la vente ne change pas (Gros / Boutique) :
     seul l'affichage change, et tout l'historique suit sans rien réécrire. */
  if(n==='boutique')              return {court:'Vente au détail',ic:'🏪',com:0};   /* ancien canal, retiré le 27 sept. : ses ventes restent */
  if(n==='gros')                  return {court:'Vente en gros',ic:'🤝'};
  return {court:nom,ic:'•'};
}
/* 7 nov. 2026 (Igal : « Perfume City a deux types de vente sur Shopify, boutique et en ligne ») : commission et envoi propres
   à la vente EN LIGNE de Perfume City (Réglages, ligne « Perfume City — en ligne ») ; la boutique garde ceux du canal. */
function comPcLigne(){ const c=canauxReg().find(x=>x.id==='perfumecity'); if(c&&c.comLigne!=null&&c.comLigne!==''&&!isNaN(+c.comLigne)) return Math.max(0,+c.comLigne); return comCanal(c?c.nom:'Perfume City'); }
function envoiPc(){ const E=(REG&&REG.envois)||{}; const v=E['shopify-pc']; return (v==null||v===''||isNaN(+v))?0:Math.max(0,+v); }
function comCanal(nom){
  if(!nom||nom===NP) return 0;
  const L=CANAUX_VENTE();
  const c=L.find(x=>String(x.nom).toLowerCase()===String(nom).toLowerCase());
  if(c) return +c.com||0;
  const k=identCanal(nom); if(k.com!==undefined) return k.com;
  if(!['gros','caisse','autre','divers'].includes(String(nom).toLowerCase())) CANAL_INCONNU.add(nom);
  return 0;
}

/* Une ligne par produit vendu. Un export de canal porte le détail de chaque commande :
   on éclate alors par commande, avec sa propre date et son propre client. */
/* 27 oct. 2026 (Sam : « j'ai reçu des espèces mais je ne les vois pas ») : le cockpit ne lisait pas les paiements du Zap
   Lightspeed ; il les garde maintenant à part (caisse-paie-v1, par vente), y compris pour les ventes déjà enregistrées. */
let _PAIE=null;
function paieDe(f){
  if(f&&f.paie&&typeof f.paie==='object') return f.paie;
  if(!f||!f._i) return null;
  if(!_PAIE){ try{ _PAIE=lit('caisse-paie-v1',{})||{}; }catch(e){ _PAIE={}; } }
  const p=_PAIE[String(f._i).replace(/^fa\|/,'')]; return (p&&typeof p==='object')?p:null;
}
/* 31 oct. 2026 (Igal : « repérer les ventes du site Shopify de Perfume City et les ventes en boutique ») : le cockpit garde
   l'origine de chaque commande de Perfume City (pc-origine-v1 : « boutique » = la caisse POS, « en ligne » = perfumeinthecity.com).
   Un remboursement prend l'origine de sa commande (même numéro). */
let _ORIG=null, _ORIGN=null;
function origineDe(f){
  if(!f||f.auto!=='shopify-pc') return '';
  if(!_ORIG){ try{ _ORIG=lit('pc-origine-v1',{})||{}; }catch(e){ _ORIG={}; } }
  const k=String(f._i||'').replace(/^fa\|/,''); if(_ORIG[k]) return _ORIG[k];
  if(!_ORIGN){ _ORIGN={}; FACT.forEach(g=>{ if(g&&g.auto==='shopify-pc'&&!g.retour){ const o=_ORIG[String(g._i||'').replace(/^fa\|/,'')]; if(o) _ORIGN[g.num]=o; } }); }
  return _ORIGN[f.num]||'';
}
const ouLib=o=>o==='boutique'?r3('en boutique','in store','en tienda'):o==='en ligne'?r3('en ligne','online','en línea'):o==='commande manuelle'?r3('commande manuelle','manual order','pedido manual'):/^\d+$/.test(String(o||''))?r3('autre canal','other channel','otro canal'):(o||'');   /* une application branchée sur Shopify n'a qu'un numéro */
/* le moyen de paiement, en deux mots, sur la ligne (Sam, 27 oct. 2026) */
function payLib(x){
  const L=[];
  if(x.paie){ const p=x.paie, a=v=>Math.abs(+v||0)>0.005;
    if(a(p.especes)) L.push(r3('Espèces','Cash','Efectivo')); if(a(p.carte)) L.push(r3('Carte','Card','Tarjeta')); if(a(p.autre)) L.push((Array.isArray(p.noms)&&p.noms.length)?p.noms.join(' + '):r3('Autre','Other','Otro')); }
  else { const m=x.pmode||x.mode||'';
    const T={especes:r3('Espèces','Cash','Efectivo'),zelle:'Zelle',carte:r3('Carte','Card','Tarjeta'),cheque:r3('Chèque','Check','Cheque'),virement:r3('Virement','Transfer','Transferencia'),credit:r3('Crédit','Credit','Crédito'),enligne:r3('En ligne','Online','En línea')};
    if(T[m]) L.push(T[m]);
    else if(/^(woocommerce|woocommerce-gros|amazon)$/.test(String(x.auto||''))) L.push(r3('En ligne','Online','En línea')); }
  const o=x.ou?ouLib(x.ou):'';
  return L.join(' + ')+(o?(L.length?' · ':'')+o:'');
}
let V=[];
function construitV(){
_PAIE=null; _ORIG=null; _ORIGN=null;
V=[]; CANAL_INCONNU=new Set();
FACT.filter(f=>f.sens==='vente').forEach(f=>{
  const canal=f.canal||NP;
  (f.lignes||[]).forEach(l=>{
    /* l'heure de la vente : celle notée avec elle ; pour une vente saisie à la
       main avant qu'on la note, l'heure de la saisie (à Miami) en tient lieu.
       Un fichier importé n'en a pas forcément : on ne l'invente pas. */
    const hF = f.h || (!f.export && f.t ? heureMiami(f.t) : '');
    /* `cle` suit la ligne jusqu'ici : c'est lui qui permet de retrouver le
       type d'une vente enregistrée AVANT qu'on le mette dans le libellé. */
    /* Le prix d'achat d'une vente est celui du jour de la vente — sauf AVANT la mise en
       service (1er oct. 2026) : les prix de l'ancien fichier Excel étaient faux par endroits
       (un parfum à 27 $ d'achat quand le Sheet dit 22,50 $), et une vente d'essai affichait
       une perte qui n'existe pas (Igal, 30 sept. 2026 : « erreur de marge »). Pour ces ventes,
       c'est le prix d'achat d'aujourd'hui qui compte. Date réglable : REG.paFigeDepuis. */
    const paV=(l.cle&&String(f.d||'')<String((REG&&REG.paFigeDepuis)||'2026-10-01')&&paEff(l.cle)!=null)?paEff(l.cle):l.paAv;
    const base={canal,num:f.num,ref:l.ref,cle:l.cle,bc:l.bc,pa:paV,par:f.par,t:f.t,fid:f.id,exp:!!f.export,
                ret:!!f.retour,refNum:f.refNum,mode:f.mode,motif:f.motif,manuel:!!f.manuel,h:hF,expd:!!f.exp,auto:f.auto||'',portF:f.port,
                paie:paieDe(f),   /* la caisse : part espèces / carte / autre */
                ou:origineDe(f),  /* Perfume City : en boutique / en ligne */
                pmode:(f.doc&&f.doc.pmode)||'',
                txR:(f.doc&&+f.doc.taxe>0&&+f.doc.base>0)?(+f.doc.taxe)/(+f.doc.base):0,   /* part de sales tax, pour l'afficher */
                /* les heures du parcours (1er oct. 2026) : reçue par le serveur, entrée dans l'ERP, expédiée */
                recu:f.recu||'', arr:f.arrive||(f.auto&&!f.exp?f.t:''), tExp:f.exp?(f.t||''):''};
    if(l.cmds&&l.cmds.length){
      l.cmds.forEach(c=>V.push(Object.assign({},base,{d:c.d||f.d,h:c.h||'',cmd:c.cmd||'',client:faNomClient(c.client),q:c.q||0,p:c.p!=null?c.p:l.p})));
    } else V.push(Object.assign({},base,{d:f.d,cmd:'',client:faNomClient((f.export&&!f.auto)?'':(f.tiers||'')),q:l.q||0,p:l.p}));
  });
});
/* Les commandes reçues mais pas encore facturées : celles qui attendent l'expédition
   et celles dont un parfum reste à identifier. Igal, 25 sept. 2026 : « le 24 il a fait
   beaucoup plus de ventes, je ne vois pas pourquoi il n'y a que ça » — le journal ne
   montrait que les ventes facturées (Amazon : 3 sur 47). Elles y sont, marquées
   « à expédier » / « à identifier » ; le stock, lui, ne bouge qu'à l'expédition. */
try{
  const canalDe=o=>o.lieu||FA_SRC[o.src]||o.src||NP;
  faLitExp().filter(e=>e&&e.statut==='attente').forEach(e=>(e.lignes||[]).forEach(l=>V.push({
    canal:canalDe(e),num:e.num||'',ref:l.ref||l.des||'',cle:l.cle,bc:l.bc||'',pa:l.cle?paEff(l.cle):null,par:'',t:e.arrive||'',fid:'',
    att:'exp',auto:e.src||'',aid:e._i,portF:e.port,d:e.d||'',h:e.h||'',cmd:'',client:faNomClient(e.client),q:+l.q||0,p:l.p==null?null:+l.p,
    recu:e.recu||'',arr:e.arrive||''})));
  (lit('caisse-file-v1',[])||[]).filter(v=>v&&!v.annule&&Array.isArray(v.lignes)).forEach(v=>faSansService(v).lignes.forEach(l=>{
    const cle=cleDeBC(l.bc)||(l.sku?cleDeBC(l.sku):null)||(l.asin?cleProcheBC(l.asin):null)||cleProcheBC(l.bc)||null;
    V.push({canal:canalDe(v),num:v.num||'',ref:cle?fNomComplet(cle):(l.des||l.bc||'?'),cle,bc:l.bc||'',pa:cle?paEff(cle):null,par:'',t:v.recu||'',fid:'',
      att:cle?'file':'id',auto:v.src||'',aid:v._i,portF:v.port,d:v.d||'',h:v.h||'',cmd:'',client:faNomClient(v.client),q:+l.q||0,p:l.p==null?null:+l.p,
      recu:v.recu||'',arr:''}); }));
}catch(e){ try{ console.error('commandes en attente :',e); }catch(_){} }
V.forEach(v=>{ v.mt=(v.q||0)*(v.p||0);
  v.com=(v.ou==='en ligne'&&String(v.auto||'')==='shopify-pc')?comPcLigne():comCanal(v.canal);   /* 7 nov. 2026 : Perfume City en ligne a sa commission */
  /* Sur un remboursement, la plateforme ne rend PAS sa commission : elle l'a déjà prise.
     La perte est donc le montant entier rendu au client, pas le montant moins la commission.
     (Amazon en rembourse une partie ; tant qu'on n'a pas ses conditions exactes, on compte
     le cas défavorable plutôt que d'annoncer une perte trop faible.) */
  v.comMt = v.ret ? 0 : v.mt*v.com/100;           /* ce que la plateforme prend, en dollars */
  v.net = v.mt - v.comMt;                         /* ce qui reste après la commission */
  v.mg=(v.pa!=null&&v.p!=null)?(v.net-v.pa*(v.q||0)):null;
  v.pct=(v.pa!=null&&v.mt!==0)?v.mg/Math.abs(v.mt)*100:null; });
/* ---- le port (Igal, 28-29 sept. 2026, « choix B ») ----
   Par COMMANDE (pas par flacon), sur Amazon et les deux sites : le port payé par le client
   (lu sur WooCommerce) est une rentrée, et ce que l'envoi coûte à Sam (fixe, réglé par
   canal dans Réglages, 8 $ par défaut) est retiré. Une seule fois par commande, réparti
   entre ses lignes au prorata (7 nov. 2026). Le chiffre d'affaires reste celui des
   parfums ; c'est la marge qui bouge. */
/* répartit les frais d'une commande entre ses lignes, au prorata du montant (les lignes sans prix d'achat n'en portent pas,
   sauf s'il n'y en a aucune autre) ; le dernier centime va à la dernière ligne pour que la somme tombe juste — même règle
   que le tableau de bord (_recap.py, rcRepartit) et le cockpit */
function vRepartit(L,cleDe,calc,pose){
  const G=new Map(); L.forEach(v=>{ const k=cleDe(v); if(!k) return; if(!G.has(k)) G.set(k,[]); G.get(k).push(v); });
  G.forEach(gr=>{ const tot=calc(gr[0]); if(!tot) return;
    const avec=gr.filter(v=>v.mg!=null), cible=avec.length?avec:[gr[0]];
    const somme=cible.reduce((a,v)=>a+Math.max(0,v.mt||0),0);
    const parts=cible.map(v=>{ const r=somme>0?Math.max(0,v.mt||0)/somme:1/cible.length; const x={}; Object.keys(tot).forEach(k=>{ x[k]=Math.round(tot[k]*r*100)/100; }); return x; });
    Object.keys(tot).forEach(k=>{ const d=Math.round((tot[k]-parts.reduce((a,x)=>a+x[k],0))*100)/100; parts[parts.length-1][k]=Math.round((parts[parts.length-1][k]+d)*100)/100; });
    cible.forEach((v,i)=>pose(v,parts[i])); });
}
vRepartit(V, v=>{ const src=String(v.auto||''); if(!/^(amazon|woocommerce|woocommerce-gros)$/.test(src)||v.ret) return null; return (v.fid?'f|'+v.fid+'|'+(v.cmd||''):'a|'+(v.aid||src+'|'+v.num)); },
  v=>{ const src=String(v.auto||''); let port=v.portF; if(port==null&&/^woocommerce/.test(src)&&typeof faStatutSite==='function'){ const st=faStatutSite(src,v.num); if(st&&+st.port>0) port=+st.port; }
    return {portMt:+port>0?+port:0, envoiMt:envoiDe(src)}; },
  (v,x)=>{ v.portMt=x.portMt; v.envoiMt=x.envoiMt; if(v.mg!=null){ v.mg+=x.portMt-x.envoiMt; v.pct=v.mt!==0?v.mg/Math.abs(v.mt)*100:null; } });
/* ---- les frais de carte de la caisse Lightspeed (Igal, 25 oct. 2026 : « 2,6 il me semble, mais fais en sorte qu'il
   puisse le modifier, et le modifier agira sur toutes les transactions enregistrées ») ----
   Ce que Lightspeed Payments prélève à Sam sur une carte, en % de la PART PAYÉE PAR CARTE de chaque vente de la caisse
   (paie.carte, posé par le cockpit depuis le 24 oct.) : les espèces et Zelle ne coûtent rien, donc pas un canal à
   commission. Taux dans Réglages (REG.carteLS, 2,6 % par défaut), appliqué à l'affichage : changer le taux recalcule
   toutes les ventes, passées comprises. Une seule fois par vente, répartie entre ses lignes au prorata du montant (7 nov. 2026 : avant, tout tombait sur
   la première ligne, et un parfum pouvait passer « vendu à perte » à cause du panier des autres). */
vRepartit(V, v=>(String(v.auto||'')==='shopify-pc'&&v.ou==='en ligne'&&!v.ret&&envoiPc()>0)?'f|'+(v.fid||v.num):null,
  v=>({portMt:0, envoiMt:envoiPc()}),
  (v,x)=>{ v.portMt=x.portMt; v.envoiMt=x.envoiMt; if(v.mg!=null){ v.mg+=x.portMt-x.envoiMt; v.pct=v.mt!==0?v.mg/Math.abs(v.mt)*100:null; } });
vRepartit(V, v=>(String(v.auto||'')!=='lightspeed'||v.ret||!v.paie||!(+v.paie.carte>0))?null:'f|'+(v.fid||v.num),
  v=>({carteMt:Math.round(+v.paie.carte*carteTaux())/100}),
  (v,x)=>{ v.carteMt=x.carteMt; v.carteBase=+v.paie.carte; if(v.mg!=null){ v.mg-=x.carteMt; v.pct=v.mt!==0?v.mg/Math.abs(v.mt)*100:null; } });
/* Le tri se fait sur l'heure DE LA VENTE (v.h), pas sur l'heure d'ENREGISTREMENT
   dans l'outil (v.t) : une vente d'un canal automatique porte son heure réelle
   dans v.h, mais v.t est le moment où le navigateur l'a inscrite — souvent bien
   plus tard, et pas forcément dans l'ordre chronologique des ventes elles-mêmes.
   Trier sur v.t affichait « 06:29 » après « 10:49 » du même jour (Igal, 12 sept.
   2026 : « pas dans l'ordre »). v.t ne sert plus qu'en dernier recours, pour les
   ventes sans heure connue (saisies à la main sans horodatage). */
V.sort((a,b)=>(b.d||'').localeCompare(a.d||'')||(b.h||'').localeCompare(a.h||'')||(b.t||'').localeCompare(a.t||''));
}
construitV();

let CANAUX=[...new Set(V.map(v=>v.canal))].sort((a,b)=>a===NP?1:b===NP?-1:a.localeCompare(b));
const cls=c=>c===NP?'na':estPC(c)?'cpc':'c'+(CANAUX.filter(x=>x!==NP).indexOf(c)%8);   /* Perfume City : toujours rose */
const dfr=d=>{ if(!d) return '—'; const [a,m,j]=d.split('-'); return `${m}/${j}/${a.slice(2)}`; };
const pc=v=>v==null?'—':(v<0?'−':'')+Math.abs(v).toFixed(1).replace('.',',')+' %';
const mcls=v=>v==null?'na':v<0?'c':v<REG.margeMin?'w':'g';

/* Igal, 27 sept. 2026 : « je veux un calendrier pour pouvoir sélectionner une journée ». */
const jourChoisi=()=>($('fp').value==='jour'&&$('fj').value)?$('fj').value:'';
function periode(){
  const p=$('fp').value; if(!p||p==='jour') return null;
  /* Igal, 4 oct. 2026 : « le chiffre depuis le début du mois » — le 1er du mois en cours, à
     l'heure de Miami (la nuit du 30 au 1er, c'est le jour de Miami qui compte) */
  if(p==='mois'){ const j=(typeof jourMiami==='function'?jourMiami(new Date()):isoJour(new Date()))||isoJour(new Date()); return j.slice(0,8)+'01'; }
  const d=new Date(); d.setHours(0,0,0,0); d.setDate(d.getDate()-(+p-1));
  return isoJour(d);
}
function filtre(avecCanal){
  const q=$('q').value.trim().toLowerCase(), lim=periode();
  return V.filter(v=>{
    if(lim && (v.d||'')<lim) return false;
    { const j=jourChoisi(); if(j && (v.d||'')!==j) return false; }
    if(avecCanal && canalSel && v.canal!==canalSel) return false;
    if(q){ const t=(v.ref+' '+v.bc+' '+v.client+' '+v.num+' '+v.cmd+' '+v.canal).toLowerCase(); if(!t.includes(q)) return false; }
    return true;
  });
}
const somme=(L,k)=>L.reduce((a,v)=>a+(v[k]||0),0);
/* Une VENTE, ce n'est pas une ligne : une commande à 12 parfums est une seule vente, pas 12.
   La clé (fid + commande) identifie la vente d'origine, comme hcVentes plus bas. Igal, 12
   sept. 2026 : « sur une vente à 12 articles, tu as mis 12 ventes — à faire toujours de cette
   manière ». Partout où on compte des VENTES (jamais des lignes), passer par cette fonction. */
const nbVentes=(L)=>new Set(L.map(v=>v.fid+'|'+(v.cmd||''))).size;

/* ================= LE DÉTAIL D'UNE VENTE =================
   Le tableau montre UNE ligne : un parfum, une quantité, une marge. Ce qu'il ne
   montre pas, et qu'on vient chercher ici :
     — le reste de la vente (cinq parfums vendus ensemble, ce sont cinq lignes
       sans lien visible à l'écran) ;
     — si c'est payé, et ce qui reste dû (ça vivait dans Factures uniquement) ;
     — d'où sort le prix d'achat qui a servi à calculer la marge ;
     — ce que ce client a acheté d'autre, et à quels prix ce parfum est parti.
   Sur téléphone le panneau prend tout l'écran : c'est là qu'il sert le plus,
   parce qu'un tableau de douze colonnes ne se lit pas sur un téléphone. */
let AFF=[], DETAIL=null;

function fermeDetail(){ $('dov').classList.remove('on'); DETAIL=null;
  if(document.documentElement.classList.contains('cadre')){ try{ window.parent.postMessage({fiche:'fermee'},location.origin); }catch(e){} } }
/* ANNULER UNE VENTE (Igal, 31 oct. 2026 : « un bouton pour annuler une vente, avec la raison de l'annulation, et une double
   validation »). Patron et Admin seulement (droit « annuler »). Étape 1 : la raison (obligatoire) et l'argent rendu ; étape 2 : ce
   qui va se passer, en rouge, et « Oui, annuler la vente ». Rien n'est effacé : c'est un remboursement de TOUTE la vente (mêmes
   règles que « Rembourser » : le stock revient, le chiffre d'affaires et la marge baissent), signé au Journal « vente annulée ». */
const RAISONS_ANN_=()=>[['client',L3('Le client a annulé','The customer cancelled','El cliente canceló'),'annulation'],
  ['erreur',L3('Erreur de saisie','Entry error','Error de captura'),'erreur'],
  ['double',L3('Vente enregistrée en double','Sale recorded twice','Venta registrada dos veces'),'erreur'],
  ['autre',L3('Autre raison (préciser)','Other reason (specify)','Otra razón (precisar)'),'annulation']];
let RAISONS_ANN=[];
function annuleEtape1(x,f){
  RAISONS_ANN=RAISONS_ANN_();
  const P=$('d-pied');
  P.innerHTML=`<div style="display:flex;flex-direction:column;gap:8px;width:100%">
    <b style="color:var(--crit)">${L3('Annuler la vente','Cancel the sale','Anular la venta')} ${esc(f.num||'')}</b>
    <label style="display:flex;gap:8px;align-items:center;flex-wrap:wrap">${L3('Raison','Reason','Razón')} :
      <select id="ann-r"><option value="">${L3('— choisis la raison —','— choose the reason —','— elige la razón —')}</option>${RAISONS_ANN.map(r=>`<option value="${r[0]}">${esc(r[1])}</option>`).join('')}</select></label>
    <input id="ann-n" placeholder="${L3('Précision (obligatoire pour « Autre raison »)','Details (required for “Other reason”)','Detalle (obligatorio para «Otra razón»)')}" style="padding:7px 10px;border:1px solid var(--line);border-radius:8px">
    <label style="display:flex;gap:8px;align-items:center;flex-wrap:wrap">${L3('Argent rendu au client','Money given back','Dinero devuelto')} :
      <select id="ann-m">${MODES_R.map(([v,l])=>`<option value="${v}"${v==='aucun'?' selected':''}>${esc(l)}</option>`).join('')}</select></label>
    <small id="ann-msg" style="color:var(--crit)"></small>
    <div style="display:flex;gap:8px;justify-content:flex-end"><button class="btn" id="ann-x">${L3('Retour','Back','Volver')}</button><button class="btn" id="ann-1" style="color:#fff;background:var(--crit);border-color:var(--crit)">${L3('Continuer','Continue','Continuar')}</button></div></div>`;
  $('ann-x').onclick=()=>ouvreDetail(x);
  $('ann-1').onclick=()=>{ const r=$('ann-r').value, n=$('ann-n').value.trim();
    if(!r){ $('ann-msg').textContent=L3('Choisis la raison de l\'annulation.','Choose the reason for the cancellation.','Elige la razón de la anulación.'); return; }
    if(r==='autre'&&!n){ $('ann-msg').textContent=L3('Écris la raison.','Write the reason.','Escribe la razón.'); $('ann-n').focus(); return; }
    annuleEtape2(x,f,r,n,$('ann-m').value); };
}
function annuleEtape2(x,f,r,n,mode){
  const P=$('d-pied'), R=RAISONS_ANN.find(z=>z[0]===r), rendu=dejaRendu(f.id);
  const fl=(f.lignes||[]).reduce((a,l)=>a+Math.max(0,(l.q||0)-(rendu[l.cle]||0)),0);
  const enLigne=/^(woocommerce|woocommerce-gros|shopify-pc|amazon|lightspeed)$/.test(String(f.auto||''));
  P.innerHTML=`<div style="display:flex;flex-direction:column;gap:8px;width:100%;border:2px solid var(--crit);border-radius:10px;padding:10px 12px;background:var(--crit-soft)">
    <b style="color:var(--crit)">${L3('Deuxième validation','Second confirmation','Segunda confirmación')}</b>
    <span>${L3('Tu vas annuler la vente','You are about to cancel sale','Vas a anular la venta')} <b>${esc(f.num||'')}</b>${f.tiers?' — '+esc(f.tiers):''} : <b data-nolang>${money2(f.montant||0)}</b>, ${nf(fl)} ${L3('flacon(s) remis en stock','bottle(s) back in stock','frasco(s) devueltos al stock')}.</span>
    <span>${L3('Raison','Reason','Razón')} : <b>${esc(R[1])}${n?' — '+esc(n):''}</b> · ${L3('argent rendu','money back','dinero devuelto')} : <b>${esc((MODES_R.find(m=>m[0]===mode)||['',''])[1])}</b></span>
    ${enLigne?`<span>⚠ ${L3('La commande reste sur le site / la caisse où elle a été faite : annule-la aussi là-bas si besoin.','The order stays on the site / register where it was made: cancel it there too if needed.','El pedido sigue en el sitio / la caja donde se hizo: anúlalo allí también si hace falta.')}</span>`:''}
    <div style="display:flex;gap:8px;justify-content:flex-end"><button class="btn" id="ann-x2">${L3('Non, garder la vente','No, keep the sale','No, conservar la venta')}</button><button class="btn" id="ann-2" style="color:#fff;background:var(--crit);border-color:var(--crit)">${L3('Oui, annuler la vente','Yes, cancel the sale','Sí, anular la venta')}</button></div></div>`;
  $('ann-x2').onclick=()=>ouvreDetail(x);
  $('ann-2').onclick=()=>{
    fermeDetail(); ouvreRetour(f.id); if(!RET){ return; }
    $('ret-motif').value=R[2]; $('ret-mode').value=mode;
    $('ret-note').value=R[1]+(n?' — '+n:'');
    $('ret-stock').checked=true; RET.lignes.forEach(l=>{ l.n=l.reste; }); peintRetour();
    const nJ=(lit(KJOU,[])||[]).length;
    $('ret-ok').click();
    /* la ligne du journal dit « vente annulée », pas « remboursement » */
    try{ const J=lit(KJOU,[]); if(J.length>nJ){ const j=J[J.length-1]; j.lib='vente annulée '+(f.num||'')+' — '+R[1].toLowerCase()+(n?' ('+n+')':'')+', '+(mode==='aucun'?'rien rendu':'rendu en '+(COURT[mode]||mode)); ecrit(KJOU,J); } }catch(e){}
    $('retov').classList.remove('on');
  };
}
/* ================= LA FICHE D'UNE VENTE : les parfums et le calcul de la marge =================
   Igal, 1er oct. 2026 (avec Sam la veille : « je comprends pas pourquoi il y a ci, pourquoi il y a
   ça ») : la fiche montrait le prix de vente et la marge, sans le prix d'achat entre les deux.
   Maintenant, pour chaque parfum : sa photo, son code-barres, le stock, le prix de vente, le prix
   d'achat, la commission du canal — et ce qu'il rapporte. Puis le calcul de la marge de la
   commande entière, une ligne par chiffre, du prix de vente à la marge nette : on peut refaire
   le calcul de tête. Même fiche pour une commande à expédier et pour une vente facturée. */
/* LA PHOTO D'UN PARFUM, comme dans le Catalogue (Igal, 21 oct. 2026 : « pourquoi je ne vois pas la photo du produit sur certaines commandes ? »).
   La fenêtre ne regardait que le fichier de l'outil (photos/<code>.webp) : 1 145 parfums sur 3 770 n'y ont pas de photo, alors que le Catalogue,
   lui, les montre — photo envoyée à la main (photos-perso-v1), sinon photo relevée sur le site (site-stock-v1), sinon fichier de l'outil,
   sinon adresse du fichier de départ. Même ordre ici ; chaque source qui échoue passe à la suivante. */
let _IMGS_V=null;
function imgsSiteV(){
  if(_IMGS_V) return _IMGS_V; _IMGS_V={};
  let S={}; try{ S=lit('site-stock-v1',{})||{}; }catch(e){ S={}; }
  if(!S||typeof S!=='object'||Array.isArray(S)) return _IMGS_V;
  const B=(S._base&&typeof S._base==='object')?S._base:{}, abs=(u,c)=>u&&u.charAt(0)==='/'?((B[c]||(c==='g'?'https://wholesale.perfumestrade.com':'https://perfumestrade.com'))+u):u;
  Object.keys(S).forEach(k=>{ if(k.charAt(0)==='_') return; const e=S[k]||{};
    const u=(e.d&&e.d.img?abs(e.d.img,'d'):'')||(e.g&&e.g.img?abs(e.g.img,'g'):''); if(u) _IMGS_V[k.replace(/^0+/,'')]=u; });
  /* 22 oct. 2026 : la photo de la boutique Perfume City sert quand aucun des deux sites n'en a (comme au Catalogue) */
  try{ const P=lit('shopify-pc-prix-v1',null); if(P&&typeof P==='object') Object.keys(P).forEach(k=>{ if(k.charAt(0)==='_') return; const r=P[k];
    if(Array.isArray(r)&&r[6]&&/^https?:\/\//.test(r[6])){ const kk=k.replace(/^0+/,''); if(!_IMGS_V[kk]) _IMGS_V[kk]=r[6]; } }); }catch(e){}
  return _IMGS_V;
}
try{ window.addEventListener('ck-maj',()=>{ _IMGS_V=null; }); }catch(e){}
function photoListe(cle,bc){
  const v=(cle&&IDX[cle])||[], b=String(bc||v[0]||'').trim(), L=[];
  try{ const PH=lit('photos-perso-v1',{})||{}; const u=(cle&&PH[cle])||(b&&PH['b'+b]); if(u) L.push(u); }catch(e){}
  if(b){ const u=imgsSiteV()[b.replace(/^0+/,'')]; if(u) L.push(u); L.push('photos/'+b+'.webp'); }
  if(v[8]) L.push(v[8]);
  return L.filter((u,i)=>u&&L.indexOf(u)===i);
}
/* l'image, ou la case vide quand AUCUNE source n'a de photo ; data-cle/data-bc/data-i : la source suivante est recalculée à l'échec */
function photoImg(cls,vide,cle,bc){
  const L=photoListe(cle,bc); if(!L.length) return vide;
  return `<img${cls?` class="${cls}"`:''} src="${esc(L[0])}" data-cle="${esc(cle||'')}" data-bc="${esc(bc||'')}" data-i="0" alt="" loading="lazy" onerror="photoSuite(this)">`;
}
window.photoSuite=function(img){
  const L=photoListe(img.dataset.cle,img.dataset.bc), i=(+img.dataset.i||0)+1;
  if(L[i]){ img.dataset.i=i; img.src=L[i]; return; }
  const d=document.createElement('span'); d.className=img.classList.contains('vig')?'vig miss':'vig0'; d.textContent='—'; img.replaceWith(d); };
function fvVig(cle,bc){ return photoImg('', '<span class="vig0">—</span>', cle, bc); }
const fvM=(v,signe)=>{ if(v==null) return '—'; const a=Math.abs(v);
  if(!signe) return money2(v);
  return `<span class="${v<0?'fv-moins':'fv-plus'}">${v<0?'−':'+'}${money2(a)}</span>`; };
/* Sam, 3 oct. 2026 : « dans la version pour les employés, je ne veux pas qu'ils voient les
   bénéfices ». Les rôles le disaient (Commercial : ni prix d'achat ni marge) ; la page des
   ventes montrait quand même la marge partout. vmg() = ce compte voit les marges. */
function vmg(){ try{ return typeof peut!=='function'||(peut('voirPA')&&peut('voirMarge')); }catch(e){ return true; } }
function vpa(){ try{ return typeof peut!=='function'||peut('voirPA'); }catch(e){ return true; } }
function blocsVente(grp,x,enAttente){
  const T=L3, canal=(grp[0]&&grp[0].canal)||'', VM=vmg();
  const cartes=grp.map(z=>{
    const cle=z.cle||cleDeBC(z.bc), st=cle?qteEff(cle):null, q=z.q||0;
    const paTot=z.pa!=null?z.pa*q:null, reste=(z.pa!=null&&z.p!=null)?(z.net-z.pa*q):null;
    return `<div class="fv${z===x&&grp.length>1?' ici':''}">
      <div class="fv-ph">${fvVig(cle,z.bc)}</div>
      <div class="fv-in">
        <div class="fv-nom" data-nolang>${esc(z.ref||(cle&&typeof fNomComplet==='function'?fNomComplet(cle):'')||'—')}${tyVu(z)}</div>
        <div class="fv-sub">${esc(z.bc||T('sans code-barres','no barcode','sin código'))}${st!=null?' · '+T('en stock','in stock','en stock')+' : '+nf(st):''}</div>
        ${(cle&&(IDX[cle]||(fNomComplet(cle),_NOMC&&_NOMC[cle])))?`<button type="button" class="btn sm fv-fiche" data-fiche="${esc(cle)}">${T('Voir la fiche du produit','See the product card','Ver la ficha del producto')}</button>`:''}
        <div class="fv-r"><span>${T('Prix de vente','Selling price','Precio de venta')} · ${nf(q)} × ${z.p!=null?money2(z.p):'?'}</span><b>${money2(z.mt)}</b></div>
        ${!VM?'':z.pa!=null
          ? (q<0
            ? `<div class="fv-r"><span>${T("Prix d'achat du flacon rendu (il revient en stock)",'Purchase price of the returned bottle (back in stock)','Precio de compra del frasco devuelto (vuelve al stock)')} · ${nf(Math.abs(q))} × ${money2(z.pa)}</span><b>${fvM(-paTot,true)}</b></div>`
            : `<div class="fv-r"><span>${T("Prix d'achat",'Purchase price','Precio de compra')} · ${nf(q)} × ${money2(z.pa)}</span><b>${fvM(-paTot,true)}</b></div>`)
          : `<div class="fv-r"><span>${T("Prix d'achat",'Purchase price','Precio de compra')}</span><b class="fv-manque">${T('inconnu','unknown','desconocido')}</b></div>`}
        ${z.comMt?`<div class="fv-r"><span>${T('Commission','Fee','Comisión')} ${esc(z.canal)} · ${z.com} %</span><b>${fvM(-z.comMt,true)}</b></div>`:''}
        ${grp.length<2||!VM?'':`<div class="fv-r t"><span>${T("Ce parfum rapporte (avant les frais d'envoi de la commande)","This perfume earns (before the order's shipping costs)","Este perfume deja (antes de los gastos de envío del pedido)")}</span><b class="mg ${reste==null?'na':reste<0?'c':'g'}">${reste==null?T('— (prix d\'achat inconnu)','— (purchase price unknown)','— (precio de compra desconocido)'):money2(reste)}</b></div>`}
      </div></div>`; }).join('');
  /* le calcul de la commande entière */
  const vente=grp.reduce((a,z)=>a+(z.mt||0),0), q=grp.reduce((a,z)=>a+(z.q||0),0);
  const com=grp.reduce((a,z)=>a+(z.comMt||0),0);
  const port=grp.reduce((a,z)=>a+(z.portMt||0),0), envoi=grp.reduce((a,z)=>a+(z.envoiMt||0),0);   /* répartis entre les lignes : on les additionne */
  const carte=grp.reduce((a,z)=>a+(z.carteMt||0),0), gc=grp.find(z=>z.carteBase)||{};
  const sansPa=grp.filter(z=>z.pa==null), achat=grp.filter(z=>z.pa!=null).reduce((a,z)=>a+z.pa*(z.q||0),0);
  const mg=sansPa.length?null:(vente-com+port-envoi-carte-achat), pct=(mg!=null&&vente)?mg/Math.abs(vente)*100:null;
  const pctCom=grp.find(z=>z.com)?.com;
  const calc=`<div class="fv-calc">
    <div class="pl"><span>${T('Prix de vente','Selling price','Precio de venta')} · ${nf(q)} ${T('flacon(s)','bottle(s)','frasco(s)')}</span><b>${money2(vente)}</b></div>
    ${com?`<div class="pl"><span>${T('Commission','Fee','Comisión')} ${esc(canal)}${pctCom?' · '+pctCom+' %':''}</span><b>${fvM(-com,true)}</b></div>`:''}
    ${port?`<div class="pl"><span>${T('Port payé par le client','Shipping paid by the customer','Envío pagado por el cliente')}</span><b>${fvM(port,true)}</b></div>`:''}
    ${envoi?`<div class="pl"><span>${T("Coût de l'envoi (une fois par commande, réglé dans Réglages)",'Shipping cost (once per order, set in Settings)','Coste del envío (una vez por pedido, en Ajustes)')}</span><b>${fvM(-envoi,true)}</b></div>`:''}
    ${carte?`<div class="pl"><span>${T('Frais de carte Lightspeed','Lightspeed card fees','Comisión de tarjeta Lightspeed')} · ${carteTaux()} % ${T('de','of','de')} ${money2(gc.carteBase||0)} ${T('payés par carte (réglé dans Réglages)','paid by card (set in Settings)','pagados con tarjeta (en Ajustes)')}</span><b>${fvM(-carte,true)}</b></div>`:''}
    <div class="pl"><span>${T("Prix d'achat",'Purchase price','Precio de compra')}${sansPa.length?' ('+T('connu pour','known for','conocido para')+' '+nf(grp.length-sansPa.length)+'/'+nf(grp.length)+')':''}</span><b>${fvM(-achat,true)}</b></div>
    <div class="pl tot"><span>${T('Marge nette','Net margin','Margen neto')}</span><b class="mg ${mg==null?'na':mcls(pct)}">${mg==null?T('incomplète','incomplete','incompleto'):money2(mg)+(pct!=null?' · '+pc(pct):'')}</b></div>
  </div>
  ${sansPa.length?`<p class="nt"><b>${T("Prix d'achat inconnu","Purchase price unknown","Precio de compra desconocido")}</b> : ${T("la marge ne peut pas être calculée tant qu'il manque.","the margin cannot be calculated while it is missing.","el margen no se puede calcular mientras falte.")}
    ${peutPaFix()?T("Écris-le ici : il est posé sur la fiche du parfum et sur cette vente.","Enter it here: it is set on the perfume's card and on this sale.","Escríbelo aquí: se pone en la ficha del perfume y en esta venta."):T("Corrige-le dans la fiche du parfum (Catalogue).","Fix it on the perfume's card (Catalogue).","Corrígelo en la ficha del perfume (Catálogo).")}</p>
    ${peutPaFix()?sansPa.filter(z=>z.cle).map(z=>`<div class="pl pafix"><span>${esc(z.ref||z.bc||'?')}</span>
      <b><input type="number" step="0.01" min="0" inputmode="decimal" data-pafix="${esc(z.cle)}" data-fid="${esc(z.fid||'')}" placeholder="${T("prix d'achat",'cost','precio de compra')}" style="width:110px;padding:6px 8px;font:inherit;font-weight:700;text-align:right;border:1px solid var(--line);border-radius:7px"> $
      <button class="btn pri" data-pago="${esc(z.cle)}" style="margin-left:6px">${T('Enregistrer','Save','Guardar')}</button></b></div>`).join('')+'<div id="pafix-rep" class="nt"></div>':''}`:''}
  <p class="nt">${enAttente
    ? T("Prix d'achat : celui de la fiche du parfum aujourd'hui. Il sera figé au moment de l'expédition.","Purchase price: the one on the perfume's card today. It is locked when the order ships.","Precio de compra: el de la ficha del perfume hoy. Se fija al enviar el pedido.")
    : T("Prix d'achat : celui du jour de la vente (on ne réécrit pas le passé).","Purchase price: the one on the day of the sale (the past is not rewritten).","Precio de compra: el del día de la venta (no se reescribe el pasado).")}
    ${com?' '+T(`La commission est ce que ${esc(canal)} garde sur le prix de vente.`,`The fee is what ${esc(canal)} keeps from the selling price.`,`La comisión es lo que ${esc(canal)} se queda del precio de venta.`):''}</p>`;
  const titre=enAttente?T('La commande','The order','El pedido'):(x&&x.cmd?T('La commande','The order','El pedido'):T('La vente','The sale','La venta'));
  return `<div data-nolang><div class="blo"><h4>${titre} · ${nf(grp.length)} ${grp.length>1?T('parfums','perfumes','perfumes'):T('parfum','perfume','perfume')}</h4>${cartes}</div>
    ${VM?`<div class="blo"><h4>${T('Le calcul de la marge','How the margin is calculated','Cálculo del margen')}</h4>${calc}</div>`:''}</div>`;
}

/* ================= LE PARCOURS DE LA VENTE, À LA MINUTE =================
   Igal, 1er oct. 2026 : « l'heure exacte de la vente et l'heure à laquelle elle a été intégrée
   sur l'ERP, pour vérifier qu'il n'y a pas eu une latence trop importante ». Trois heures, à
   Miami : la vente (l'heure que le canal donne — pour Amazon, celle de son email « Sold, ship
   now »), l'arrivée sur le serveur, l'entrée dans l'ERP ; et l'écart avec la vente. */
function miamiVersInstant(d,h){
  if(!d||!/^\d{1,2}:\d{2}$/.test(String(h||''))) return null;
  const p=new Date(d+'T'+String(h).padStart(5,'0')+':00Z'); if(isNaN(p)) return null;
  const ny=new Date(p.toLocaleString('en-US',{timeZone:'America/New_York'})), u=new Date(p.toLocaleString('en-US',{timeZone:'UTC'}));
  return new Date(p.getTime()+(u-ny));
}
const ecartTxt=(a,b)=>{ if(!a||!b) return ''; const m=Math.round((new Date(b)-a)/60000); if(!isFinite(m)) return '';
  if(m<1) return L3('moins d\'1 min','under 1 min','menos de 1 min'); if(m<60) return '+'+m+' min';
  const h=Math.floor(m/60), r=m%60; return '+'+h+' h '+String(r).padStart(2,'0'); };
function blocParcours(x){
  if(!x||!x.auto) return '';
  const T=L3, t0=miamiVersInstant(x.d,x.h);
  const ligne=(lab,t,av)=>`<div class="pl"><span>${lab}</span><b>${t?esc(quandMiami(t).replace(' · ',' '+T('à','at','a')+' ')):'—'}${t&&av?` <small style="color:var(--ink-3);font-weight:600">${ecartTxt(av,t)}</small>`:''}</b></div>`;
  const arr=x.arr?new Date(x.arr):null, lat=(t0&&arr)?Math.round((arr-t0)/60000):null;
  return `<div class="blo" data-nolang><h4>${T('Le parcours de la vente (heure de Miami)','How the sale came in (Miami time)','El recorrido de la venta (hora de Miami)')}</h4>
    <div class="pl"><span>${T('Vente','Sale','Venta')}${/^amazon/.test(x.auto)?' '+T("(heure de l'email d'Amazon)",'(time of the Amazon email)','(hora del email de Amazon)'):''}</span><b>${x.d?esc(dfr(x.d)):'—'}${x.h?' '+T('à','at','a')+' '+esc(x.h):''}</b></div>
    ${ligne(T('Reçue par le serveur','Received by the server','Recibida por el servidor'),x.recu,t0)}
    ${x.att==='file'||x.att==='id'
      ? `<div class="pl"><span>${T("Entrée dans l'ERP",'Entered the ERP','Entrada en el ERP')}</span><b>${T("pas encore (en file d'attente)",'not yet (waiting in the queue)','todavía no (en cola)')}</b></div>`
      : ligne(T("Entrée dans l'ERP",'Entered the ERP','Entrada en el ERP'),x.arr,t0)}
    ${x.tExp?ligne(T('Expédiée (facture faite, stock sorti)','Shipped (invoice made, stock out)','Enviada (factura hecha, stock fuera)'),x.tExp,null):''}
    ${lat!=null&&lat>15?`<p class="nt" style="color:var(--warn)"><b>${T('Latence élevée','High latency','Latencia alta')}</b> : ${ecartTxt(t0,arr)} ${T("entre la vente et l'ERP. Le serveur relève les ventes chaque minute ; un écart pareil vient en général du canal (email Amazon tardif) ou d'une page de l'ERP restée fermée.","between the sale and the ERP. The server collects sales every minute; a gap like this usually comes from the channel (late Amazon email) or from no ERP page being open.","entre la venta y el ERP. El servidor recoge las ventas cada minuto; un retraso así suele venir del canal (email de Amazon tardío) o de que no había ninguna página del ERP abierta.")}</p>`:''}
    ${!x.recu?`<p class="nt">${T("L'heure d'arrivée sur le serveur n'était pas notée avant le 1er octobre.","The server arrival time was not recorded before October 1.","La hora de llegada al servidor no se anotaba antes del 1 de octubre.")}</p>`:''}
  </div>`;
}

/* Une commande pas encore expédiée : on la VOIT ici, sans quitter la page. Igal, 27 sept.
   2026 : « quand je clique sur une commande, ça va sur l'expédition — moi je veux juste
   voir la commande ». L'expédier reste un geste de la rubrique Expéditions (un bouton y mène). */
function ouvreCommande(g){
  const L=g.lignes||[g], q=L.reduce((a,l)=>a+(l.q||0),0), mt=L.reduce((a,l)=>a+(l.mt||0),0);
  const mgs=L.filter(l=>l.mg!=null), mg=mgs.reduce((a,l)=>a+l.mg,0), mtM=mgs.reduce((a,l)=>a+(l.mt||0),0);
  $('d-tit').innerHTML=`${esc(L.length===1?(L[0].ref||(L[0].cle&&typeof fNomComplet==='function'?fNomComplet(L[0].cle):'')||'—'):nf(L.length)+' parfums')}
    <span class="sub">${pastCanal(g)}
    ${dfr(g.d)}${g.h?' · '+esc(g.h):''} · <span data-nolang>${esc(g.num||'')}</span> · <span class="st exp">à expédier</span></span>`;
  $('d-corps').innerHTML=`${blocsVente(L,null,true)}${blocParcours(g.lignes?g.lignes[0]:g)}
  <div class="blo"><h4>Client</h4><div class="pl"><span>${cliAff(g.client,g.canal)}</span><b></b></div></div>
  <div class="blo"><h4>État</h4><p class="nt" data-nolang>${L3("<b>Pas encore expédiée</b> : pas de facture, et le stock n'a pas bougé. Quand le colis part, on la marque « expédiée » dans Expéditions — c'est ce geste qui fait la facture et sort les flacons.",
    "<b>Not shipped yet</b>: no invoice, and stock has not moved. When the parcel leaves, it is marked “shipped” in Shipping — that is what makes the invoice and takes the bottles out.",
    "<b>Aún no enviado</b>: sin factura, y el stock no se movió. Cuando sale el paquete, se marca «enviado» en Envíos — ese gesto hace la factura y saca los frascos.")}</p></div>`;
  $('d-pied').innerHTML=`<a class="btn" href="expeditions.html?cmd=${encodeURIComponent(g.aid||'')}">Ouvrir dans Expéditions</a>
    <span style="flex:1"></span><button class="btn pri" id="d-ok">Fermer</button>`;
  $('d-ok').onclick=fermeDetail;
  $('d-corps').scrollTop=0;
  $('dov').classList.add('on');
}

/* ---- NOMMER LE CLIENT d'une vente qui n'en a pas (Igal, 21 oct. 2026 : « Clemencia a enregistré une vente en oubliant le nom du client »).
   Une vente arrivée toute seule (caisse Lightspeed, site) n'a pas de « Modifier la vente » : elle se corrige à la source, et la caisse ne renvoie
   jamais le ticket. Le bouton « Modifier » de la FACTURE recalcule tout, et fait disparaître la sales tax encaissée au ticket (testé : 657,69 $ → 656,50 $).
   Ici on ne change QUE le nom : ni les lignes, ni le stock, ni la taxe, ni les montants. Le nom va sur la vente (donc sa facture et le Journal des ventes),
   et le Journal garde l'avant et l'après. Pas pour Amazon, qui n'envoie jamais le nom de l'acheteur ; pas pour un export qui porte ses propres clients. */
function peutNommerClient(f,x){
  if(!f||f.sens!=='vente'||f.retour||f.annule||MODE_QUOTES) return false;
  if(typeof peut==='function'&&!peut('vendre')) return false;
  if(/amazon/i.test(String(f.canal||''))) return false;
  if(f.export&&!f.auto) return false;                       /* export de commandes : un client par commande, pas un seul pour la facture */
  if(x&&x.cmd) return false;
  return !faNomClient(f.tiers||'');
}
function demandeNomClient(f,x){
  $('d-pied').innerHTML=`<input id="d-nom-v" type="text" maxlength="120" autocomplete="off" placeholder="Nom du client" style="flex:1;min-width:200px;padding:9px 11px;border:1px solid var(--line);border-radius:8px;font:inherit">
    <button class="btn pri" id="d-nom-ok">Enregistrer le nom</button><button class="btn" id="d-nom-x">Annuler</button>
    <span id="d-nom-m" style="flex-basis:100%;font-size:12.5px;color:var(--crit)"></span>`;
  const inp=$('d-nom-v'); inp.focus();
  $('d-nom-x').onclick=()=>ouvreDetail(x);
  const ok=()=>{
    const nom=faNomClient(inp.value);
    /* faNomClient écarte « walk-in » et « guest » ; ni « client de passage » (ce que l'ERP affiche faute de nom) ni un simple numéro ne sont un nom */
    const faux=!nom||/^(client\s+de\s+passage|cliente?\s+de\s+paso|passage|inconnu|unknown|n\/?a|sans\s+nom|[\d\s.\-–—]+)$/i.test(nom)||nom.length<2;
    if(faux){ $('d-nom-m').textContent="Il faut un vrai nom (pas « client de passage », « walk-in » ni un numéro)."; inp.focus(); return; }
    if(!signe("ce nom de client",ok)) return;
    const g=FACT.find(z=>z.id===f.id)||f; if(faNomClient(g.tiers||'')){ ouvreDetail(x); return; }
    const avant=g.tiers||'';
    g.tiers=nom; if(g!==f) f.tiers=nom;
    ecrit(KFACT,FACT);
    try{ const J=lit(KJOU,[]); J.push({t:new Date().toISOString(),u:USR||'(non renseigné)',act:'vente',lib:'client nommé sur la vente '+(g.doc&&g.doc.num?g.doc.num:g.num)+' — '+nom,ref:g.id,av:avant||'(sans nom)',ap:nom,n:0,impact:0,det:[]}); ecrit(KJOU,J); }catch(e){}
    construitV();
    const nx=V.find(z=>z.fid===g.id&&(z.bc===x.bc))||V.find(z=>z.fid===g.id);
    vus=Math.max(vus||0,80); dessine();
    if(nx) ouvreDetail(nx); else fermeDetail();
  };
  $('d-nom-ok').onclick=ok;
  inp.addEventListener('keydown',e=>{ if(e.key==='Enter'){ e.preventDefault(); ok(); } });
}
/* ---- le prix d'achat saisi depuis la vente (Igal, 27 oct. 2026 : « pas devoir aller sur le catalogue… une page qui
   s'ouvre sur la droite et qui dit rajouter le prix d'achat ») ----
   Il n'était pas connu au moment de la vente : la case est VIDE, on la remplit, on ne réécrit rien. Le prix va sur la
   fiche du parfum (fiches-modifiees-v1, si elle n'en a pas) et sur cette vente ainsi que sur les autres ventes de ce
   parfum qui n'en avaient pas (paAv). Signé au Journal. Même droit que dans le Catalogue : modPrix. */
const peutPaFix=()=>{ try{ return vmg()&&(typeof peut!=='function'||peut('modPrix')); }catch(e){ return false; } };
function fixePa(cle,v,fid){
  if(!(v>0)||!cle) return null;
  relitStock(); const m=Object.assign({},MOD[cle]||{}); const avFiche=paEff(cle);
  if(avFiche==null){ m.pa=v; MOD[cle]=m; ecrit(KMOD,MOD); }
  let n=0; const nums=[];
  FACT.forEach(f=>{ if(!f||f.sens!=='vente'||!Array.isArray(f.lignes)) return; let t=false;
    f.lignes.forEach(l=>{ if(l&&l.cle===cle&&(l.paAv==null||l.paAv==='')){ l.paAv=v; t=true; } });
    if(t){ n++; nums.push(f.num); } });
  if(n) ecrit(KFACT,FACT);
  const ref=fNomComplet(cle)||cle;
  try{ const J=lit(KJOU,[]); J.push({t:new Date().toISOString(),u:USR||'(non renseigné)',act:'prix',champ:'pa',lib:"prix d'achat saisi depuis une vente"+(avFiche==null?'':" (la fiche avait déjà "+money2(avFiche)+")"),
    ref,av:'—',ap:money2(v),n,det:nums.slice(0,20).map(x=>({num:x}))}); ecrit(KJOU,J); }catch(e){}
  return {n,avFiche};
}
function ouvreDetail(x){
  if(!x) return;
  DETAIL=x;
  const f=FACT.find(z=>z.id===x.fid)||null;
  const cle=cleDeBC(x.bc);

  /* « la vente entière » : pour un export de canal, une facture contient des
     dizaines de commandes différentes. Le groupe, c'est la commande — pas le
     fichier. Sans ça on afficherait 400 lignes qui n'ont rien à voir. */
  const grp = x.cmd ? V.filter(z=>z.fid===x.fid && z.cmd===x.cmd)
                    : V.filter(z=>z.fid===x.fid);
  const totGrp=somme(grp,'mt'), uGrp=somme(grp,'q');
  const mgGrp=somme(grp.filter(z=>z.mg!=null),'mg');
  const comGrp=grp.reduce((a,z)=>a+(z.comMt||0),0);

  const paNow = cle!=null ? paEff(cle) : null;
  const stock = cle!=null ? qteEff(cle) : null;

  /* ce que ce client a acheté d'autre */
  const cli=(x.client||'').trim();
  const hc = cli ? V.filter(z=>(z.client||'').trim()===cli) : [];
  const hcAutres = hc.filter(z=>!(z.fid===x.fid && z.cmd===x.cmd));
  const hcVentes = new Set(hc.map(z=>z.fid+'|'+(z.cmd||''))).size;

  /* ce parfum, ailleurs */
  const hp = x.bc ? V.filter(z=>z.bc===x.bc && !z.ret) : [];
  const prix = hp.map(z=>z.p).filter(p=>p!=null);
  const pMin = prix.length?Math.min(...prix):null, pMax = prix.length?Math.max(...prix):null;

  /* les remboursements déjà passés sur cette vente */
  const remb = f ? FACT.filter(z=>z.retour && z.refId===f.id) : [];

  const D = f && f.doc ? f.doc : null;
  const st = D ? docStatut(f) : null;
  const regs = D ? encRegs(f) : [];

  /* Sam, 3 oct. 2026 : « dans une vente multiple, le nom du 1er parfum vendu tout en haut ne
     sert à rien ». Le titre était celui de la ligne cliquée — le premier parfum — alors que la
     fiche montre toute la vente. Plusieurs parfums : le titre dit la vente (combien, à qui). */
  const multi=grp.length>1, nP=new Set(grp.map(z=>z.bc||z.ref)).size;
  $('d-tit').innerHTML=`${multi?`<span>${nf(nP)} parfums</span>${cli?'<span data-nolang> — '+esc(cli)+'</span>':''}`:`${esc(x.ref||'—')}${tyVu(x)}`}
    <span class="sub">${pastCanal(x)}
    ${dfr(x.d)} · ${esc(x.cmd||x.num||'')}${x.bc&&!multi?' · code-barres '+esc(x.bc):''}
    ${x.ret?'<br><b style="color:var(--crit)">Ceci est un remboursement</b>':''}</span>`;

  const l=[];

  /* ---- les parfums et le calcul de la marge (1er oct. 2026) ---- */
  l.push(blocsVente(grp,x,false));
  l.push(blocParcours(x));
  if(vmg() && x.pa!=null && paNow!=null && Math.abs(paNow-x.pa)>0.005)
    l.push(`<p class="nt">Le prix d'achat de ce parfum <b>vaut ${money2(paNow)} aujourd'hui</b>.
      La marge ci-dessus garde ${money2(x.pa)}, le prix au jour de la vente. C'est voulu :
      un achat renégocié le mois dernier ne doit pas changer la marge d'une vente de janvier.</p>`);
  if(vmg() && x.pa==null)
    l.push(`<p class="nt"><b>Le prix d'achat n'était pas connu au moment de cette vente</b>, donc la marge
      n'est pas calculée — et cette ligne ne compte pas dans le taux de marge affiché en haut.
      ${peutPaFix()?"Écris-le dans la case « Prix d'achat inconnu » ci-dessus : il sera posé sur la fiche du parfum et sur cette vente.":"Corrige le prix d'achat dans la fiche du parfum."}</p>`);

  /* ---- le paiement ---- */
  if(D){
    l.push(`<div class="blo"><h4>Paiement</h4>
      <div class="pl"><span>${esc(D.type==='devis'?'Devis':'Facture')} ${esc(D.num||'')}</span>
        <b><span class="et ${st==='paye'?'ok':st==='partiel'?'mi':'no'}">${esc(FSTAT[st]||st)}</span></b></div>
      ${(+D.taxe>0)?`<div class="pl"><span>Hors taxe</span><b>${money2(D.base)}</b></div>
      <div class="pl"><span>Sales tax ${esc(String(D.taux).replace('.',','))} %</span><b>${money2(D.taxe)}</b></div>`:''}
      <div class="pl"><span>${(+D.taxe>0)?'Total payé par le client':'Total du document'}</span><b>${money2(D.total)}</b></div>
      ${regs.length?regs.map(r=>`<div class="pl"><span>&nbsp;&nbsp;reçu le ${dfr(r.d)} · ${esc(FMODES[r.m]||r.m||'')}${r.ref?' · '+esc(r.ref):''}</span><b>${money2(r.mt)}</b></div>`).join('')
        :`<div class="pl"><span>Aucun versement enregistré</span><b>—</b></div>`}
      ${(D.reste||0)>0
        ? `<div class="pl gr"><span>Reste dû</span><b style="color:var(--crit)">${money2(D.reste)}</b></div>`
        : `<div class="pl gr"><span>Soldée</span><b class="mg g">${money2(D.regle||D.total)}</b></div>`}
      ${D.fiscal==='exempt'?'<p class="nt">Document marqué exempt de sales tax.</p>':''}
    </div>`);
  } else {
    l.push(`<div class="blo"><h4>Paiement</h4>
      <p class="nt" data-nolang>${L3(
        `<b>Aucune facture n'a été émise pour cette vente</b> : elle est entrée directement au journal${x.exp?" par l'export d'un canal":(x.manuel?' par saisie manuelle':'')}. Le règlement n'est donc pas suivi ici — l'outil ne sait pas si l'argent est rentré. ${x.exp?"Pour un canal (Amazon, le site…), c'est normal : la plateforme encaisse pour toi.":"Si tu veux suivre le règlement, il faut cocher « Facture » au moment d'enregistrer la vente."}`,
        `<b>No invoice was issued for this sale</b>: it went straight into the log${x.exp?' through a channel export':(x.manuel?' by manual entry':'')}. Payment is therefore not tracked here — the tool does not know whether the money came in. ${x.exp?'For a channel (Amazon, the website…) that is normal: the platform collects for you.':'To track payment, tick “Invoice” when recording the sale.'}`,
        `<b>No se emitió ninguna factura para esta venta</b>: entró directamente en el registro${x.exp?' por la exportación de un canal':(x.manuel?' por entrada manual':'')}. Por eso el cobro no se sigue aquí — la herramienta no sabe si entró el dinero. ${x.exp?'Para un canal (Amazon, la web…) es normal: la plataforma cobra por ti.':'Para seguir el cobro, marca «Factura» al registrar la venta.'}`)}</p>
    </div>`);
  }

  /* ---- remboursements ---- */
  if(remb.length){
    l.push(`<div class="blo"><h4>Remboursé sur cette vente</h4>
      <table><tbody>${remb.map(r=>{
        const lm=(MODES_R.find(m=>m[0]===r.mode)||['','—'])[1];
        const lo=(MOTIFS_R.find(m=>m[0]===r.motif)||['','retour'])[1];
        return `<tr><td><b>${esc(r.num)}</b><small>${dfr(r.d)} · ${esc(lo.toLowerCase())} · ${r.mode==='aucun'?'rien rendu':'rendu en '+esc(COURT[r.mode]||lm.toLowerCase())}</small>${r.note?`<small>${esc(r.note)}</small>`:''}</td>
        <td class="r"><b style="color:var(--crit)">${money2(r.montant)}</b></td></tr>`; }).join('')}</tbody></table>
    </div>`);
  }

  /* ---- ce client ---- */
  if(cli){
    const tot=somme(hc,'mt');
    const ds=hc.map(z=>z.d).filter(Boolean).sort();
    l.push(`<div class="blo"><h4>Ce client</h4>
      <div class="pl"><span>${esc(cli)}</span><b>${nf(hcVentes)} vente${hcVentes>1?'s':''}</b></div>
      <div class="pl"><span>Total acheté, tous canaux</span><b>${money2(tot)}</b></div>
      ${ds.length>1?`<div class="pl"><span>Du ${dfr(ds[0])} au ${dfr(ds[ds.length-1])}</span><b>${nf(somme(hc,'q'))} flacon${Math.abs(somme(hc,'q'))>1?'s':''}</b></div>`:''}
      ${hcAutres.length?`<button class="btn sm" id="d-cli">Voir ses ${nf(hcVentes-1)} autre${hcVentes-1>1?'s':''} vente${hcVentes-1>1?'s':''}</button>`
        :`<p class="nt">C'est son seul achat enregistré à ce nom.</p>`}
      <p class="nt">Ce total ne compte que ce qui est passé par l'outil. Le nom doit être écrit
      exactement pareil d'une vente à l'autre pour être regroupé — « J. Smith » et « John Smith »
      font deux clients ici.</p>
    </div>`);
  }

  /* ---- ce parfum (une vente d'un seul parfum : pour plusieurs, chaque carte du haut le dit) ---- */
  if(x.bc && !multi){
    l.push(`<div class="blo"><h4>Ce parfum</h4>
      ${stock!=null?`<div class="pl"><span>En stock aujourd'hui</span><b class="${stock<=0?'mg c':''}">${nf(stock)} flacon${Math.abs(stock)>1?'s':''}</b></div>`
        :`<div class="pl"><span>Référence</span><b>inconnue du catalogue</b></div>`}
      <div class="pl"><span>Vendu ${nf(hp.length)} fois${hp.length?', '+nf(somme(hp,'q'))+' flacon(s)':''}</span><b>${money2(somme(hp,'mt'))}</b></div>
      ${pMin!=null&&pMax!=null&&pMax-pMin>0.005?`<div class="pl"><span>Prix pratiqués</span><b>${money2(pMin)} → ${money2(pMax)}</b></div>`:''}
      ${paNow!=null&&vpa()?`<div class="pl"><span>Prix d'achat actuel</span><b>${money2(paNow)}</b></div>`:''}
      ${x.bc?`<button class="btn sm" id="d-bc">Voir toutes ses ventes</button>`:''}
      ${stock===null?'<p class="nt">Ce code-barres ne correspond à aucune fiche du catalogue : le stock ne peut pas être suivi, et la marge non plus.</p>':''}
    </div>`);
  }

  /* ---- la saisie ---- */
  l.push(`<div class="blo"><h4>Saisie</h4>
    <div class="pl"><span>Enregistré par</span><b>${esc(x.par&&x.par!=='(non renseigné)'?x.par:'—')}</b></div>
    <div class="pl"><span>Le</span><b>${x.t?esc(quandMiami(x.t).replace(' · ',' à ')):'—'}</b></div>
    <div class="pl"><span>Origine</span><b data-nolang>${esc(origine(x))}</b></div>
    ${f&&f.poste?`<div class="pl"><span>Ordinateur</span><b data-nolang>${esc(f.poste)}</b></div>`:''}
    <div class="pl"><span>Facture interne</span><b>${esc(x.num||'—')}</b></div>
  </div>`);

  $('d-corps').innerHTML=l.join('');
  $('d-pied').innerHTML=`${D?'<button class="btn" id="d-fac">Ouvrir la facture</button>':''}
    ${x.ret?'':`<button class="btn" id="d-ret">Rembourser</button>`}
    ${!x.ret&&x.fid&&typeof peut==='function'&&peut('annuler')&&(()=>{ const r=dejaRendu(x.fid); return (f&&f.lignes||[]).some(l=>(l.q||0)>(r[l.cle]||0)); })()?`<button class="btn" id="d-ann" style="color:var(--crit);border-color:var(--crit)">${L3('Annuler la vente','Cancel the sale','Anular la venta')}</button>`:''}
    ${peutModifierVente(f)?`<button class="btn" id="d-mod">Modifier la vente</button>`:''}
    ${peutNommerClient(f,x)?`<button class="btn" id="d-nom">Nommer le client</button>`:''}
    <span style="flex:1"></span><button class="btn pri" id="d-ok">Fermer</button>`;

  $('d-ok').onclick=fermeDetail;
  const bf=$('d-fac'); if(bf) bf.onclick=()=>{ fermeDetail(); dessineDoc(f); };
  const br=$('d-ret'); if(br) br.onclick=()=>{ fermeDetail(); ouvreRetour(x.fid); };
  const ba=$('d-ann'); if(ba) ba.onclick=()=>annuleEtape1(x,f);
  const bm=$('d-mod'); if(bm) bm.onclick=()=>{ fermeDetail(); ouvreModif(f); };
  const bn=$('d-nom'); if(bn) bn.onclick=()=>demandeNomClient(f,x);
  const bc=$('d-cli'); if(bc) bc.onclick=()=>{ fermeDetail(); $('q').value=cli; $('fp').value=''; vus=80; dessine(); };
  const bb=$('d-bc'); if(bb) bb.onclick=()=>{ fermeDetail(); $('q').value=x.bc; $('fp').value=''; vus=80; dessine(); };
  $('d-corps').scrollTop=0;
  $('dov').classList.add('on');
}
$('d-x').onclick=fermeDetail;
/* Igal, 17 oct. 2026 : « quand tu cliques sur une vente, un bouton, et une deuxième fenêtre s'ouvre pour avoir plus d'information
   sans passer par le catalogue » : la fiche du parfum, dans une fenêtre par-dessus le détail de la vente (qui reste là dessous) */
$('d-corps').addEventListener('click',e=>{ const b=e.target.closest('[data-fiche]'); if(b){ e.preventDefault(); ficheFenetre(b.dataset.fiche); }
  const g=e.target.closest('[data-pago]'); if(g){ e.preventDefault(); const cle=g.dataset.pago, inp=$('d-corps').querySelector('[data-pafix="'+cle+'"]');
    const v=Math.round(parseFloat(String(inp&&inp.value||'').replace(',','.'))*100)/100, rep=$('pafix-rep');
    if(!(v>0)){ if(rep) rep.textContent=L3("Écris un prix d'achat.","Enter a cost.","Escribe un precio de compra."); if(inp) inp.focus(); return; }
    const fid=inp&&inp.dataset.fid, x=DETAIL;
    const r=fixePa(cle,v,fid); if(!r) return;
    construitV(); vus=Math.max(vus||0,80); dessine();
    const nx=(x&&V.find(z=>z.fid===x.fid&&z.cle===cle))||(x&&V.find(z=>z.fid===x.fid)); if(nx) ouvreDetail(nx);
    const rep2=$('pafix-rep'); const msg=L3(`Prix d'achat enregistré : ${money2(v)}`+(r.n>1?` sur ${r.n} ventes de ce parfum`:'')+'.',`Cost saved: ${money2(v)}`+(r.n>1?` on ${r.n} sales of this perfume`:'')+'.',`Precio de compra guardado: ${money2(v)}`+(r.n>1?` en ${r.n} ventas de este perfume`:'')+'.');
    const d=document.createElement('p'); d.className='nt'; d.style.color='var(--good)'; d.textContent=msg; const z=$('d-corps').querySelector('.fv-calc'); if(z) z.insertAdjacentElement('afterend',d); else $('d-corps').prepend(d); } });
$('dov').onclick=e=>{ if(e.target===$('dov')) fermeDetail(); };

/* Une ligne de séparation par jour, avec le nombre de commandes du jour (Igal, 25 sept.
   2026 : « une ligne de séparation par date, et savoir par jour combien il y a eu de
   commandes »). Compté sur tout ce que le filtre retient, pas seulement l'écran. */
function ligneJour(d,L){
  const M=L.filter(x=>x.d===d); const cmd=new Set(M.map(x=>x.fid||x.aid||(x.canal+'|'+x.num)));
  const n=cmd.size, q=M.reduce((a,x)=>a+(x.q||0),0), mt=M.reduce((a,x)=>a+(x.mt||0),0), na=new Set(M.filter(x=>x.att).map(x=>x.aid)).size;
  let jd=d; try{ const lg=(typeof LANG!=='undefined'&&LANG==='en')?'en-US':(typeof LANG!=='undefined'&&LANG==='es')?'es-ES':'fr-FR';
    jd=new Date(d+'T12:00:00Z').toLocaleDateString(lg,{weekday:'long',day:'numeric',month:'long',year:'numeric',timeZone:'UTC'}); jd=jd.charAt(0).toUpperCase()+jd.slice(1); }catch(e){}
  /* Igal, 30 sept. 2026 : « rajoute sur cette ligne le profit de la journée ». La marge nette
     du jour (commissions, port et envoi compris), même calcul que chaque ligne ; une vente
     dont on ne connaît pas le prix d'achat n'y entre pas, et on le dit. */
  const mgL=M.filter(x=>x.mg!=null), mg=mgL.reduce((a,x)=>a+x.mg,0), mtM=mgL.reduce((a,x)=>a+(x.mt||0),0);
  const sansPa=new Set(M.filter(x=>x.mg==null).map(x=>x.fid||x.aid||(x.canal+'|'+x.num))).size;
  /* Igal, 20 oct. 2026 : « 1 vente sans prix d'achat — comment savoir laquelle ? » : on nomme le numéro de commande et le parfum, à côté de la mention */
  /* 27 oct. 2026 (Igal : « un petit bouton pour intervenir directement de la ligne ») : chaque mention ouvre la fiche de
     cette vente, à droite, où le prix d'achat se saisit sur place. */
  const qui=[...new Map(M.filter(x=>x.mg==null).map(x=>[x.fid||x.aid||(x.canal+'|'+x.num),{k:x.fid||x.aid||(x.canal+'|'+x.num),t:(x.cmd||x.num?'n° '+numCourt(x.cmd||x.num)+' — ':'')+(x.lignes&&x.lignes.length>1?x.lignes.length+' parfums':(x.ref||x.bc||'?'))}])).values()];
  const quiTxt=qui.length?' ('+qui.slice(0,3).map(q=>`<button class="lnk jpa" data-sanspa="${esc(q.k)}" title="${esc(r3("Ouvrir cette vente et saisir le prix d'achat",'Open this sale and enter the cost','Abrir esta venta y escribir el precio de compra'))}">${esc(q.t)}</button>`).join(' ; ')+(qui.length>3?' …':'')+')':'';
  const pct=mtM?mg/mtM*100:null;
  const prof=(mgL.length||sansPa)&&vmg()?`<span class="jm mg ${mgL.length?mcls(pct):'na'}" data-nolang title="${esc(r3('Marge nette du jour : prix de vente moins le prix d’achat, les commissions et l’envoi','Net profit of the day: sale price minus cost, fees and shipping','Margen neto del día: precio de venta menos compra, comisiones y envío'))}">${mgL.length?r3('marge','profit','margen')+' '+money(mg)+(pct!=null?' · '+pc(pct):''):''}${sansPa?(mgL.length?' · ':'')+nf(sansPa)+' '+r3(sansPa>1?'ventes sans prix d’achat':'vente sans prix d’achat',sansPa>1?'sales without cost':'sale without cost',sansPa>1?'ventas sin precio de compra':'venta sin precio de compra')+quiTxt:''}</span>`:'';
  return `<tr class="jour"><td colspan="12"><span class="jd" data-nolang>${esc(jd)}</span><span class="jn">${nf(n)} commande${n>1?'s':''} · ${nf(q)} flacon${Math.abs(q)>1?'s':''} · ${money(mt)}</span>${prof}${na?`<span class="ja">dont ${nf(na)} en attente</span>`:''}</td></tr>`;
}
function dessine(){
  const P=filtre(true), L=P;                     /* les KPI suivent le filtre affiché : un seul total à l'écran */
  const TOUS=filtre(false);                      /* sert aux parts de CA entre canaux */
  const ca=somme(P,'mt'), mg=somme(P.filter(v=>v.mg!=null),'mg'), u=somme(P,'q');
  const caM=somme(P.filter(v=>v.mg!=null),'mt');
  const comTot=P.reduce((a,v)=>a+(v.comMt||0),0);
  /* le libellé de la période en français d'origine : l'écran est peut-être déjà traduit */
  const _op=$('fp').options[$('fp').selectedIndex];
  const lib=(jourChoisi()?(r3('le ','','el ')+new Date(jourChoisi()+'T12:00:00').toLocaleDateString(typeof lgLocale==='function'?lgLocale():'fr-FR',{weekday:'long',day:'numeric',month:'long',year:'numeric'})):((typeof lgFr==='function')?lgFr(_op):_op.textContent).toLowerCase())+(canalSel?' · '+canalCourt(canalSel):'');
  /* Igal, 27 sept. 2026 : « je trouve que c'est moche et pas clair ». Quatre chiffres,
     pas six, chacun avec un mot : l'argent qui est entré, ce qu'il en reste, combien de
     commandes (plus des « lignes de vente »), et ce qui attend quelqu'un. La commission
     des plateformes, déjà retirée de la marge, est dite en une phrase dessous. */
  const nCmd=nbVentes(P), nAtt=new Set(P.filter(x=>x.att).map(x=>x.aid)).size;
  const nExp=new Set(P.filter(x=>x.att==='exp').map(x=>x.aid)).size, nId=nAtt-nExp;
  $('kpis').innerHTML=`<div class="rs">
    <div class="rs-t">${esc(lib.charAt(0).toUpperCase()+lib.slice(1))}</div>
    <div class="rs-g">
      <div class="rs-c"><span class="rs-v">${money(ca)}</span><span class="rs-k">chiffre d'affaires</span></div>
      ${vmg()?`<div class="rs-c"><span class="rs-v ${mg<0?'c':'g'}">${money(mg)}</span><span class="rs-k">marge nette${caM>0?` · <b class="${mg<0?'c':'g'}">${pc(mg/caM*100)}</b>`:''}</span></div>`:''}
      <div class="rs-c"><span class="rs-v">${nf(nCmd)}</span><span class="rs-k">commande${nCmd>1?'s':''} · ${nf(u)} flacon${Math.abs(u)>1?'s':''}</span></div>
      <div class="rs-c${nAtt?' at':''}"><span class="rs-v">${nf(nAtt)}</span><span class="rs-k">${nAtt?[nExp?`${nf(nExp)} à expédier`:'',nId?`${nf(nId)} à identifier`:''].filter(Boolean).join(' · '):'rien en attente'}</span></div>
    </div>
    ${vmg()&&(comTot||caM<ca)?`<div class="rs-n">${comTot?`Les plateformes ont gardé <b>${money(comTot)}</b> de commission, déjà retirés de la marge.`:''}${caM<ca?` La marge ne compte que les ventes dont le prix d'achat est connu.`:''}</div>`:''}
  </div>`;

  /* par canal : un onglet par canal, l'essentiel seulement (part, montant, marge en petit).
     Le détail — flacons, commission prélevée — reste au survol. Une commission non réglée
     dans Réglages se signale par deux mots dans l'onglet, pas par un pavé au-dessus. */
  const parC={};
  /* c.n compte des VENTES (une commande, même à 12 parfums, ne vaut qu'une seule vente),
     jamais des lignes : un Set des ventes déjà vues par canal, comme hcVentes plus haut.
     Igal, 12 sept. 2026 : « sur une vente à 12 articles, tu as mis 12 ventes ». */
  const vusCanal={};
  TOUS.forEach(v=>{ const c=parC[v.canal]||(parC[v.canal]={n:0,u:0,ca:0,mg:0,caM:0,com:0,cpct:v.com||0});
    /* Perfume City : la boutique et le site, séparés (31 oct. 2026) */
    if(v.ou==='boutique') c.caB=(c.caB||0)+v.mt; else if(v.ou==='en ligne') c.caW=(c.caW||0)+v.mt;
    const sV=vusCanal[v.canal]||(vusCanal[v.canal]=new Set()), cleV=(v.fid||v.aid||(v.canal+'|'+v.num))+'|'+(v.cmd||'');   /* une commande en attente n'a pas encore de facture : son identifiant de file */
    if(!sV.has(cleV)){ sV.add(cleV); c.n++; }
    c.u+=v.q||0; c.ca+=v.mt;
    c.com+=v.comMt||0;
    if(v.mg!=null){ c.mg+=v.mg; c.caM+=v.mt; } });
  const caT=somme(TOUS,'mt');
  /* Perfume in the City a TOUJOURS sa ligne dans le tableau, même sans vente sur la période : Igal veut
     la voir à côté des autres canaux (13 oct. 2026). Le nom est celui des Réglages, sinon « Perfume City ». */
  if(Object.keys(parC).length && !Object.keys(parC).some(estPC)){
    const cpc=(CANAUX_VENTE().find(x=>estPC(x.nom))||{}).nom||'Perfume City';
    parC[cpc]={n:0,u:0,ca:0,mg:0,caM:0,com:0,cpct:0}; }
  const cl=Object.entries(parC).sort((a,b)=>b[1].ca-a[1].ca);
  $('nbc').textContent=cl.length?(canalSel?'clique à nouveau pour tout revoir':'clique un canal pour ne voir que ses ventes'):'';
  const maxCa=cl.length?Math.max(...cl.map(([,x])=>x.ca)):0;
  const VMc=vmg();
  /* 25 oct. 2026 (Igal : « cette partie est vraiment vilaine ») : chaque canal est une tuile avec son vrai logo —
     Amazon et Perfumes Trade depuis logos/ (fichiers officiels d'Igal), Perfume in the City depuis le logo de ses
     factures (Réglages), les autres en toutes lettres tant que leur fichier n'est pas déposé dans logos/. */
  const LOGOS_V=__LOGOS_V__;
  const logoCanal=(c,k)=>{ const n=String(c||'').toLowerCase();
    const pcLogo=(()=>{ try{ return (REG.factPC&&REG.factPC.logo)||''; }catch(e){ return ''; } })();
    if(n.includes('amazon')&&LOGOS_V.amazon) return `<img src="${LOGOS_V.amazon}" alt="Amazon">`;
    if(n.includes('wholesale')) return (LOGOS_V.site?`<img src="${LOGOS_V.site}" alt="Perfumes Trade">`:`<span class="wm">Perfumes Trade</span>`)+`<span class="sub">wholesale</span>`;
    if(n.includes('perfumestrade')) return (LOGOS_V.site?`<img src="${LOGOS_V.site}" alt="Perfumes Trade">`:`<span class="wm">Perfumes Trade</span>`)+`<span class="sub">retail</span>`;
    if(/perfume\s*(in\s*the\s*)?city/.test(n)) return LOGOS_V.perfumecity?`<img src="${LOGOS_V.perfumecity}" alt="Perfume in the City">`:pcLogo?`<img src="${pcLogo}" alt="Perfume in the City">`:`<span class="wm">Perfume in the City</span>`;
    if(n.includes('lightspeed')||n.includes('caisse')) return LOGOS_V.lightspeed?`<img src="${LOGOS_V.lightspeed}" alt="Lightspeed">`:`<span class="wm ls">Lightspeed</span><span class="sub">${L3('caisse','till','caja')}</span>`;
    if(n==='gros') return (LOGOS_V.site?`<img src="${LOGOS_V.site}" alt="Perfumes Trade">`:`<span class="wm">Perfumes Trade</span>`)+`<span class="sub">${L3('boutique','store','tienda')}</span>`;   /* Igal, 25 oct. : « boutique » / « store », pas « gros » */
    if(n==='boutique') return (LOGOS_V.site?`<img src="${LOGOS_V.site}" alt="Perfumes Trade">`:`<span class="wm">Perfumes Trade</span>`)+`<span class="sub">${L3('détail','retail','detalle')}</span>`;
    const id=(k&&k.id)||''; if(id&&LOGOS_V[id]) return `<img src="${LOGOS_V[id]}" alt="${esc(k.court||c)}">`;
    return `<span class="wm">${esc(k.court||c)}</span>`; };
  $('par').innerHTML=cl.length?`<div class="cxg">`+cl.map(([c,x])=>{
    const k=identCanal(c), part=caT>0?Math.round(x.ca/caT*100):0, inc=CANAL_INCONNU.has(c);
    const pm=x.caM>0?x.mg/x.caM*100:null;
    const det=`${nf(x.u)} flacon${x.u>1?'s':''}`+(x.cpct?` · ${x.cpct} % de commission : −${money(x.com)}`:'');
    return `<div class="cxt ${cls(c)}${canalSel===c?' on':''}" data-c="${esc(c)}" title="${esc(det)}">
      <div class="lg">${logoCanal(c,k)}</div><div class="cn"${k.fixe?' data-nolang':''}>${esc(k.court)}</div>${inc?`<a href="reglages.html" onclick="event.stopPropagation()" class="cx-w" title="Ce canal n'est pas dans Réglages : sa marge est comptée sans commission">commission non réglée</a>`:''}
      <div class="ca" data-nolang>${money(x.ca)}</div>
      ${estPC(c)&&(x.caB||x.caW)?`<div class="pcou"><span>${L3('Boutique','In store','Tienda')} <b data-nolang>${money(x.caB||0)}</b></span><span>${L3('Online','Online','Online')} <b data-nolang>${money(x.caW||0)}</b></span></div>`:''}
      <div class="bar"><i style="width:${maxCa>0?Math.max(2,x.ca/maxCa*100):0}%"></i></div>
      <div class="l2"><span><b data-nolang>${part} %</b> ${L3('du chiffre d\'affaires','of revenue','de la facturación')}</span><span><b data-nolang>${nf(x.n)}</b> ${L3('vente'+(x.n>1?'s':''),'sale'+(x.n>1?'s':''),'venta'+(x.n>1?'s':''))}</span></div>
      ${VMc?`<div class="mgl"><span>${L3('Marge nette','Net margin','Margen neto')}</span>${pm!=null?`<span><b class="mg ${mcls(pm)}" data-nolang>${money(x.mg)}</b> <small class="mg ${mcls(pm)}" data-nolang>${pc(pm)}</small></span>`:'<span class="na">—</span>'}</div>`:''}
    </div>`; }).join('')+`</div>`:'';
  /* 17 oct. 2026 (Sam) : un compte qui ne voit pas les marges (Commercial) ne voit pas non plus le chiffre d'affaires du mois
     ni les canaux : on VIDE ces blocs, on ne les cache pas (un bloc caché reste lisible dans la page). */
  if(!vmg()){ $('kpis').innerHTML=''; $('par').innerHTML=''; $('nbc').textContent=''; const hc=$('nbc').parentElement; if(hc) hc.hidden=true; }
  /* un clic sur un canal filtre « Toutes les ventes » ET y descend : avec la file
     d'attente entre les deux, le tableau filtré était 6 000 px plus bas et on ne
     voyait rien changer (Igal, 25 sept. 2026) */
  document.querySelectorAll('.cxt[data-c]').forEach(el=>el.onclick=()=>{ canalSel = canalSel===el.dataset.c ? '' : el.dataset.c; $('fc').value=canalSel; vus=80; dessine();
    if(canalSel){ const h=$('tv'); if(h) try{ h.scrollIntoView({behavior:'smooth',block:'start'}); }catch(e){ h.scrollIntoView(); } } });

  if(!V.length){
    $('corps').innerHTML=`<div class="vide"><h3>Aucune vente enregistrée</h3>
      <p>Le journal se remplit de trois façons : le bouton « + Enregistrer une vente » en haut,
      une facture de vente, ou l'import du fichier de commandes d'un canal. Chaque produit vendu
      arrive ici avec son canal.</p>
      <p><button class="btn pri" onclick="document.getElementById('nv').click()">+ Enregistrer une vente</button></p></div>`;
    $('nbv').textContent=''; $('src').innerHTML='aucune vente'; return;
  }
  if(!L.length){
    $('corps').innerHTML=`<div class="vide"><h3>Aucune vente ne correspond</h3><p>Élargis la période ou enlève un filtre.</p></div>`;
    $('nbv').textContent=''; $('src').innerHTML=`0 vente affichée<br>sur ${nf(nbVentes(V))} au total`; return;
  }
  /* Igal, 27 sept. 2026 : « quand une personne achète plusieurs parfums, il faudrait
     regrouper achat par achat ». Une ligne du tableau = UN achat (une commande, une
     facture), avec tous ses parfums dedans ; la quantité, le montant et la marge sont
     ceux de l'achat entier. */
  const G=[], parK={};
  L.forEach(x=>{ const k=x.att?'a|'+x.aid:'f|'+x.fid+'|'+(x.cmd||'');
    let g=parK[k]; if(!g){ g=parK[k]=Object.assign({},x,{lignes:[],q:0,mt:0,mg:null,mtM:0,portMt:0,envoiMt:0,carteMt:0}); G.push(g); }
    g.portMt+=x.portMt||0; g.envoiMt+=x.envoiMt||0; g.carteMt+=x.carteMt||0;
    g.lignes.push(x); g.q+=x.q||0; g.mt+=x.mt||0;
    if(x.mg!=null){ g.mg=(g.mg||0)+x.mg; g.mtM+=x.mt||0; } });
  G.forEach(g=>{ g.pct=(g.mg!=null&&g.mtM)?g.mg/g.mtM*100:null; if(g.lignes.length>1) g.p=null; });
  const v=G.slice(0,vus);
  $('nbv').textContent=`${nf(G.length)} achat${G.length>1?'s':''}`;
  /* colonnes secondaires (o1 → o5) : elles s'effacent, dans cet ordre, si le tableau
     ne tient pas dans l'écran — voir « af » dans _menu.py */
  /* Igal, 27 sept. 2026 : « les lettres sont les unes sur les autres… des fois annulé,
     des fois remboursé… après 3 % après 3 %, je comprends rien — fais quelque chose de
     joli ». Une ligne = une vente, lisible d'un coup d'œil : le numéro de commande ne
     déborde plus sur le client, l'état de la vente a SA colonne (une seule étiquette,
     toujours au même endroit), la marge dit un montant et un pourcentage — la
     commission est dans la fiche, pas répétée sur chaque ligne. Plus de boutons sur la
     ligne : on clique la vente, sa fiche s'ouvre, et c'est là qu'on rembourse. */
  const etat=x=> x.ret ? `<span class="st ret">remboursée</span><small class="stm">${esc((MOTIFS_R.find(m=>m[0]===x.motif)||['','retour'])[1])}</small>`
    : x.att==='exp' ? `<span class="st exp">à expédier</span>`
    : x.att ? `<span class="st id">${x.att==='id'?'à identifier':'en attente'}</span>`
    : (()=>{ const w=/^woocommerce/.test(String(x.auto||''))&&typeof faStatutSite==='function'?((faStatutSite(x.auto,x.num)||{}).st||''):'';
        /* Sam : « shipped » quand c'est envoyé, « to ship » sinon — le site le dit (completed) */
        if(x.expd||w==='completed') return `<span class="st ok">expédiée</span>`;
        if(/^(processing|on-hold)$/.test(w)) return `<span class="st exp">à expédier</span>`;
        return `<span class="st ok">vendue</span>`; })();
  const tipMg=x=> (x.com ? `Marge nette : prix de vente moins le prix d'achat et la commission ${x.canal} (${x.com} %)` : `Marge nette : prix de vente moins le prix d'achat`)+((x.portMt||x.envoiMt)?` ; plus le port payé par le client, moins le coût de l'envoi`:'')+(x.carteMt?` ; moins les frais de carte Lightspeed (${carteTaux()} % de la part payée par carte)`:'');
  $('corps').innerHTML=`<div class="wrapx af"><table class="tbl tv2"><thead><tr>
    <th class="no o4">N°</th><th>Date</th><th>Canal</th><th>Commande</th><th class="cli">Client</th><th class="pdt">Produit</th>
    <th class="r">Qté</th><th class="r o2">Prix unit.</th><th class="r">Montant</th><th class="r vmg" title="Après le prix d'achat et la commission du canal">Marge nette</th><th>État</th><th class="go"></th>
    </tr></thead><tbody>${v.map((x,i)=>`${(i===0||v[i-1].d!==x.d)?ligneJour(x.d,L):''}<tr class="${x.ret?'ret':''}${x.att?' att':''}${estPC(x.canal)?' pcr':''}" data-d="${i}" title="${x.att==='exp'?'Commande à expédier : voir la commande':x.att?'Commande en attente : ouvrir sa fiche':'Ouvrir la fiche de la vente'}">
      <td class="no o4">${nf(i+1)}</td>
      <td class="qd"><b>${dfr(x.d)}</b>${x.h?`<span class="hh">${esc(x.h)}</span>`:''}</td>
      <td class="cnl">${pastCanal(x)}</td>
      <td class="num" title="${esc(x.cmd||x.num||'')}"><span data-nolang>${numCourt(x.cmd||x.num)}</span></td>
      <td class="cli"><div class="cl2">${cliAff(x.client,x.canal)}</div></td>
      <td class="ref pdt">${x.lignes.length===1?`<b>${esc(x.ref)}${tyVu(x)}</b><span>${esc(x.bc)}</span>`
        :`<div class="pl3">${x.lignes.slice(0,4).map(l=>`<div><em>${nf(l.q)}×</em> <b>${esc(l.ref)}</b>${tyVu(l)}</div>`).join('')}${x.lignes.length>4?`<div class="plus4">+ ${nf(x.lignes.length-4)} autres parfums</div>`:''}</div>`}</td>
      <td class="r">${nf(x.q)}</td>
      <td class="r o2">${x.p!=null?money2(x.p):'—'}</td>
      <td class="r mt">${money2(x.mt)}${x.txR?`<small class="tx">+ ${money2(x.mt*x.txR)} de taxe</small>`:''}${(()=>{ const pl=payLib(x); return pl?`<small class="pay">${esc(pl)}</small>`:''; })()}</td>
      <td class="r mgc vmg" title="${esc(tipMg(x))}">${x.mg!=null?`<span class="mg ${mcls(x.pct)}">${money2(x.mg)}</span>${x.pct!=null?`<small class="mg ${mcls(x.pct)}">${pc(x.pct)}</small>`:''}`:'<span class="na">—</span>'}${(x.portMt||x.envoiMt)?`<small class="prt" data-nolang>${x.portMt?r3('port','shipping','envío')+' +'+money2(x.portMt)+' · ':''}${r3('envoi','parcel','paquete')} −${money2(x.envoiMt)}</small>`:''}</td>
      <td class="etat">${etat(x)}</td>
      <td class="go">›</td></tr>`).join('')}</tbody>
    <tfoot><tr><td class="o4"></td><td colspan="3">Total affiché</td><td class="cli"></td><td class="pdt"></td><td class="r">${nf(somme(L,'q'))}</td><td class="o2"></td>
      <td class="r">${money2(somme(L,'mt'))}</td><td class="r vmg"><span class="mg ${mcls(somme(L.filter(x=>x.mg!=null),'mg')<0?-1:1)}">${money2(somme(L.filter(x=>x.mg!=null),'mg'))}</span></td><td></td><td class="go"></td></tr></tfoot>
    </table></div>
    ${G.length>vus?`<button class="plus" id="plus">Afficher plus (${nf(G.length-vus)} restants)</button>`:''}`;
  const b=$('plus'); if(b) b.onclick=()=>{ vus+=80; dessine(); };
  AFF=v;                                     /* ce qui est à l'écran, pour le panneau de détail */
  const ouvre=x=>{ if(!x) return; if(x.att==='exp'){ ouvreCommande(x); return; }
    if(x.att){ try{ ouvreAttente(x.aid); }catch(e){} return; } ouvreDetail(x.lignes?x.lignes[0]:x); };   /* un achat : sa fiche montre la vente entière */
  document.querySelectorAll('[data-d]').forEach(el=>el.onclick=()=>ouvre(AFF[+el.dataset.d]));
  document.querySelectorAll('[data-sanspa]').forEach(b=>b.onclick=e=>{ e.stopPropagation(); const k=b.dataset.sanspa;
    const x=V.find(z=>(z.fid||z.aid||(z.canal+'|'+z.num))===k&&z.mg==null)||V.find(z=>(z.fid||z.aid||(z.canal+'|'+z.num))===k); if(x) ouvreDetail(x); });
  const nvL=nbVentes(L), nvV=nbVentes(V);
  $('src').innerHTML=`${nf(nvL)} vente${nvL>1?'s':''} affichée${nvL>1?'s':''}<br>sur ${nf(nvV)} au total`;
  $('sfoot').innerHTML=`${nf(V.length)} ligne${V.length>1?'s':''} de vente<br>${CANAUX.filter(c=>c!==NP).length} canaux`;
}

/* Un numéro de caisse Lightspeed arrive parfois sous sa forme interne — un long
   identifiant (161cfa62-e6f7-a592-11f1-b84381ae32d6) qui élargissait la colonne
   à lui seul. On en montre la fin, le numéro entier reste au survol et dans la fiche. */
function numCourt(n){ const s=String(n||''); return /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(s)
  ? `<span title="${esc(s)}" data-nolang>…${esc(s.slice(-8))}</span>` : esc(s); }
/* ---------------- enregistrer une vente à la main ---------------- */
let PANIER=[], CANDIDATS=[], SEL=-1;
/* la case de recherche en cours : celle du haut (v-q) ou celle du bas (v-q2, sous les lignes). La liste des résultats
   (#v-res) est unique et suit la case active ; ajouter un parfum rend la main à la même case, donc Sam reste en bas. */
let VQA='v-q';
const vq=()=>$(VQA)||$('v-q');
function vqActive(id){
  if(!$(id)) return; if(VQA!==id){ const a=$(VQA); VQA=id; try{ if(a) a.value=''; CANDIDATS=[]; SEL=-1; peintRes(); }catch(e){} }
  try{ const r=$('v-res'), w=id==='v-q2'?$('v-q2w'):$('v-q').parentNode; if(r&&w&&r.parentNode!==w) w.appendChild(r); }catch(e){}
}

/* Le numéro de vente : V + la date + un rang qui repart à 1 chaque jour.
   Deux garde-fous : on part du plus grand rang déjà utilisé ce jour-là (pas du nombre de ventes),
   et on garde en mémoire le dernier rang atteint — une vente annulée ne libère donc pas son
   numéro, et aucun numéro n'est jamais réattribué. */
const KNUM='ventes-numeros-v1';

/* Le client d'une vente, affiché : son nom ; sinon un mot gris qui dit pourquoi il
   manque (Amazon ne transmet plus le nom de l'acheteur, la caisse vend souvent sans
   client). Jamais « [object Object] » ni une phrase d'email. */
/* dans le tableau, le canal en court (« Site gros » plutôt que « Site
   wholesale.perfumestrade.com ») : le nom entier reste dans l'infobulle */
/* 27 sept. 2026 (Igal) : « pourquoi j'ai dans les ventes Till, Website ou autres, je veux
   savoir exactement d'où ça vient ». « Caisse » et « Site » étaient des mots : l'anglais les
   traduisait en « Till » et « Website », pendant que la liste des canaux, en haut, disait
   « Lightspeed » et « perfumestrade.com ». Un canal a maintenant UN nom, le même en haut,
   dans le tableau et sur la fiche, qui n'est jamais traduit ; et la bulle dit d'où vient
   la vente. */
function canalCourt(c){ const t=String(c||'');
  if(/wholesale\./i.test(t)) return 'wholesale.perfumestrade.com';
  if(/^Site perfumestrade/i.test(t)) return 'perfumestrade.com';
  if(/^Caisse Lightspeed/i.test(t)||/lightspeed/i.test(t)) return 'Lightspeed';
  return nomAff(t); }
/* le nom montré d'un canal saisi à la main (listes de choix, filtre, pastilles) */
function nomAff(c){ const t=String(c||''); return /^gros$/i.test(t)?'Vente en gros':/^boutique$/i.test(t)?'Vente au détail':t; }
/* la pastille du canal : le nom fixe n'est pas traduit (un nom propre), la bulle explique */
function pastCanal(x){ const c=x.canal, k=identCanal(c);
  return `<span class="ch ${cls(c)}" title="${esc(origine(x))}"${k.fixe?' data-nolang':''}>${esc(canalCourt(c))}</span>`; }
/* d'où vient la vente, en une phrase, dans la langue de l'écran */
function origine(x){
  const a=String(x.auto||'').toLowerCase(), c=String(x.canal||'');
  if(a==='lightspeed'||(!a&&x.att&&/lightspeed/i.test(c)))
    return r3('Caisse Lightspeed du magasin : ticket passé en caisse, arrivé tout seul dans l\'ERP (Zapier → cockpit).',
              'Lightspeed register in the store: a ticket rung up at the till, sent to the ERP automatically (Zapier → cockpit).',
              'Caja Lightspeed de la tienda: ticket cobrado en caja, llegó solo al ERP (Zapier → cockpit).');
  if(a==='woocommerce-gros')
    return r3('Commande passée sur le site de gros wholesale.perfumestrade.com, arrivée toute seule.',
              'Order placed on the wholesale website wholesale.perfumestrade.com, received automatically.',
              'Pedido hecho en la web mayorista wholesale.perfumestrade.com, llegó solo.');
  if(a==='woocommerce')
    return r3('Commande passée sur le site perfumestrade.com, arrivée toute seule.',
              'Order placed on the perfumestrade.com website, received automatically.',
              'Pedido hecho en la web perfumestrade.com, llegó solo.');
  if(a==='amazon')
    return r3('Commande Amazon, lue dans l\'email de commande qu\'Amazon envoie à Sam.',
              'Amazon order, read from the order email Amazon sends to Sam.',
              'Pedido de Amazon, leído en el email de pedido que Amazon envía a Sam.');
  if(a==='message')
    return r3('Commande reçue par message, enregistrée depuis Ventes.','Order received by message, recorded from Sales.','Pedido recibido por mensaje, registrado desde Ventas.');
  const qui=x.par&&x.par!=='(non renseigné)'?x.par:'';
  if(x.manuel)
    return r3(`Saisie à la main dans Ventes${qui?' par '+qui:''} (bouton « Nouvelle vente ») — ne vient d'aucune caisse ni d'aucun site.`,
              `Entered by hand in Sales${qui?' by '+qui:''} (“New sale” button) — not from any register or website.`,
              `Registrada a mano en Ventas${qui?' por '+qui:''} (botón «Nueva venta») — no viene de ninguna caja ni web.`);
  if(x.exp)
    return r3('Importée depuis un fichier (rubrique Factures).','Imported from a file (Invoices section).','Importada desde un archivo (sección Facturas).');
  return r3(`Facture créée dans l'ERP${qui?' par '+qui:''} (rubrique Factures).`,
            `Invoice created in the ERP${qui?' by '+qui:''} (Invoices section).`,
            `Factura creada en el ERP${qui?' por '+qui:''} (sección Facturas).`);
}
function cliAff(nom,canal){
  const n=faNomClient(nom); if(n) return esc(n);
  const c=String(canal||'');
  const pq=/amazon/i.test(c)?'acheteur Amazon':/caisse|lightspeed/i.test(c)?'client de passage':'—';
  return `<span class="cliv" title="${pq==='acheteur Amazon'?"Amazon n'envoie pas le nom de l'acheteur dans ses emails":''}">${pq}</span>`;
}
/* ---- Trouver un client vite, ou en créer un ----
   Trois carnets : les clients wholesale du Google Sheet, les clients Retail
   (fichier + import), et les noms déjà tapés dans une vente. On cherche dans
   les trois sans se soucier des accents ni des majuscules. Un nom inconnu peut
   être gardé tel quel : il entrera dans Retail à l'enregistrement de la vente. */
const cNorm=t=>String(t||'').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g,'').trim();
function carnet(){
  const out=[], vus=new Set();
  const add=(nom,tag,det)=>{ const k=cNorm(nom); if(!nom||vus.has(k)) return; vus.add(k); out.push({nom,tag,det}); };
  try{ ((window.D_CLI||{}).clients||[]).forEach(c=>add(c.nom,'gros',
        (c.total?money(c.total)+' · ':'')+(c.nb||0)+' commande'+((c.nb||0)>1?'s':''))); }catch(e){}
  try{ const R=(()=>{ try{ const t=localStorage.getItem('retail-local-v1'); if(t){ const L=JSON.parse(t); if(Array.isArray(L)) return L; } }catch(e){}
                      return Array.isArray(window.D_RETAIL)?window.D_RETAIL:[]; })();
       R.forEach(c=>add(c.nom,'détail',[c.ville,c.email].filter(Boolean).join(' · ')||'')); }catch(e){}
  try{ Object.keys(lit(KCLI,{})||{}).forEach(n=>add(n,'déjà vu','')); }catch(e){}
  return out;
}
/* La boîte de suggestions d'un champ client : rien ne s'affiche avant deux
   lettres tapées — la liste complète des clients n'est jamais déroulée d'un
   coup (c'était le comportement de la liste native du navigateur, refusé).
   Branchée sur deux champs : la fenêtre de vente et le panneau des Quotes. */
function carnetLie(idInp, idBox, apres){
  const inp=$(idInp), box=$(idBox); let CSEL=-1, CLIST=[];
  function peint(){
    const q=cNorm(inp.value);
    if(q.length<2){ box.classList.remove('on'); box.innerHTML=''; CLIST=[]; return; }
    const tous=carnet();
    const pref=tous.filter(c=>cNorm(c.nom).startsWith(q));
    const dans=tous.filter(c=>!cNorm(c.nom).startsWith(q)&&cNorm(c.nom).includes(q));
    CLIST=pref.concat(dans).slice(0,8);
    const exact=tous.some(c=>cNorm(c.nom)===q);
    const html=CLIST.map((c,i)=>`<div data-i="${i}" class="${i===CSEL?'sel':''}"><b>${esc(c.nom)}</b>
        <span>${esc(c.tag)}${c.det?' · '+esc(c.det):''}</span></div>`).join('')
      +(exact?'':`<div data-i="new" class="${CSEL===CLIST.length?'sel':''}"><b>+ Nouveau client : « ${esc(inp.value.trim())} »</b>
        <span>sera ajouté dans Retail à l'enregistrement de la vente</span></div>`);
    box.innerHTML=html; box.classList.add('on');
  }
  function choisit(i){
    if(i==='new'){ inp.dataset.nouveau='1'; }
    else { const c=CLIST[+i]; if(c){ inp.value=c.nom; delete inp.dataset.nouveau; } }
    box.classList.remove('on'); CSEL=-1;
    if(apres) apres();
  }
  inp.addEventListener('input',()=>{ CSEL=-1; delete inp.dataset.nouveau; peint(); });
  inp.addEventListener('focus',peint);
  inp.addEventListener('keydown',e=>{
    const n=CLIST.length+(box.querySelector('[data-i="new"]')?1:0);
    if(e.key==='ArrowDown'){ e.preventDefault(); CSEL=Math.min(n-1,CSEL+1); peint(); }
    else if(e.key==='ArrowUp'){ e.preventDefault(); CSEL=Math.max(-1,CSEL-1); peint(); }
    else if(e.key==='Enter'){ e.preventDefault();
      if(CSEL>=0){ const el=box.querySelector('.sel'); if(el) choisit(el.dataset.i); }
      else if(!CLIST.length && inp.value.trim()) choisit('new');
      else if(CLIST.length===1) choisit(0);
      else if(apres) apres(); }
    else if(e.key==='Escape'){ box.classList.remove('on'); }
  });
  box.addEventListener('mousedown',e=>{ const d=e.target.closest('[data-i]'); if(d){ e.preventDefault(); choisit(d.dataset.i); } });
  document.addEventListener('click',e=>{ if(!e.target.closest('#'+idInp+',#'+idBox)) box.classList.remove('on'); });
}
carnetLie('v-client','v-cres',()=>{ majChipsClient(); vq().focus(); });
carnetLie('m-client','m-cres',()=>$('m-txt').focus());

/* Un nom nouveau entre dans Retail comme une fiche vide : nom seul, à compléter. */
function clientDansRetail(nom){
  if(!nom) return;
  const k=cNorm(nom);
  const gros=((window.D_CLI||{}).clients||[]).some(c=>cNorm(c.nom)===k);
  if(gros) return;
  let R=null; try{ const t=localStorage.getItem('retail-local-v1'); if(t) R=JSON.parse(t); }catch(e){}
  if(!Array.isArray(R)) R=Array.isArray(window.D_RETAIL)?window.D_RETAIL.slice():[];
  if(R.some(c=>cNorm(c.nom)===k)) return;
  R.push({nom, email:'', tel:'', ville:'', pays:'', nb:0, total:0, der:'', derArt:''});
  try{ localStorage.setItem('retail-local-v1',JSON.stringify(R)); }catch(e){}
}
function rangs(){ try{ return JSON.parse(localStorage.getItem(KNUM)||'{}'); }catch(e){ return {}; } }
function prefixe(d){ return 'V'+(d||ajd()).slice(2).replace(/-/g,'')+'-'; }
function numAuto(d){
  const p=prefixe(d); let max=rangs()[p]||0;
  FACT.forEach(f=>{ const n=String(f.num||''); if(n.startsWith(p)){ const v=parseInt(n.slice(p.length),10); if(v>max) max=v; } });
  return p+String(max+1).padStart(3,'0');
}
function noteRang(num,d){
  const p=prefixe(d); if(!String(num).startsWith(p)) return;
  const v=parseInt(String(num).slice(p.length),10); if(!v) return;
  const R=rangs(); if(!(R[p]>=v)){ R[p]=v; try{ localStorage.setItem(KNUM,JSON.stringify(R)); }catch(e){} }
}
const numPris=n=>FACT.some(f=>String(f.num||'').toLowerCase()===n.toLowerCase());

const r2=v=>Math.round(v*100)/100;
function prixSuggere(cle,canal){
  const v=IDX[cle]||[], m=MOD[cle]||{};
  if(canal.id==='gros') return m.pvw!=null?+m.pvw:(v[6]!=null?+v[6]:null);
  const pc=(m.pc||{})[canal.id];
  if(pc!=null&&pc!=='') return +pc;
  if(canal.base==='pvw'){ const w=m.pvw!=null?+m.pvw:(v[6]!=null?+v[6]:null); return w==null?null:r2(w*(1+(canal.maj||0)/100)); }
  const pvr=m.pvr!=null?+m.pvr:(v[5]!=null?+v[5]:null);
  if(pvr==null) return null;
  return r2(pvr*(1+(canal.maj||0)/100));
}
const canalCour=()=>CANAUX_VENTE().find(c=>c.nom===$('v-canal').value)||{id:'autre',nom:'Autre',com:0,maj:0};

/* La recherche d'un parfum : au code-barres ou au nom.
   Le piège, trouvé le 16 sept. : dès qu'on tapait SIX chiffres ou plus, l'outil
   croyait avoir affaire à un code-barres complet et n'acceptait qu'une égalité
   exacte. Taper les six derniers chiffres d'un code-barres ne trouvait donc
   RIEN, alors que quatre ou cinq marchaient — c'est exactement ce qu'on fait
   quand on lit l'étiquette d'un flacon qu'on a en main.
   Maintenant : la douchette (code entier) est servie en premier et exactement,
   et si rien ne colle, on cherche ces chiffres N'IMPORTE OÙ dans le code. */
function chercheProduits(q){
  q=q.trim().toLowerCase(); if(q.length<2) return [];
  const chiffres=/^\d{4,14}$/.test(q);
  const exact=[], dedans=[], R=[];
  for(const cle in IDX){
    const v=IDX[cle];
    if(chiffres){
      const nq=q.replace(/^0+/,''), m=MOD[cle];
      const tous=[(v[0]||'')].concat(
        (m&&m.bcs)?String(m.bcs).split(/[^0-9]+/):[], bcExtra()[cle]||[]
      ).map(x=>String(x||'').replace(/^0+/,'')).filter(Boolean);
      if(tous.some(x=>x===nq)) exact.push(cle);
      else if(tous.some(x=>x.includes(nq))) dedans.push(cle);
      if(exact.length>60) break;
    } else {
      const t=((v[2]||'')+' '+(v[1]||'')+' '+(v[0]||'')).toLowerCase();
      if(t.includes(q)) R.push(cle);
      if(R.length>60) break;
    }
  }
  /* le code lu en entier passe devant : la douchette ne doit jamais hésiter */
  return chiffres ? exact.concat(dedans).slice(0,40) : R.slice(0,40);
}
function peintRes(){
  const el=$('v-res');
  if(!CANDIDATS.length){ el.classList.remove('on'); el.innerHTML=''; return; }
  el.innerHTML=CANDIDATS.map((cle,i)=>{ const v=IDX[cle];
    return `<div data-cle="${esc(cle)}" class="${i===SEL?'sel':''}"><b>${esc(v[2]||'')} ${esc(v[1]||'')}${tyBadge(cle)}</b>
      <span>${esc(v[3]||'')}${v[3]?' oz · ':''}${esc(v[0]||'sans code-barres')} · stock ${nf(qteEff(cle))}</span></div>`; }).join('');
  el.classList.add('on');
  el.querySelectorAll('[data-cle]').forEach(d=>d.onclick=()=>ajoute(d.dataset.cle));
}
function ajoute(cle){
  const ex=PANIER.find(l=>l.cle===cle);
  if(ex) ex.q++;
  else PANIER.push({cle,q:1,p:prixSuggere(cle,canalCour())});
  vq().value=''; CANDIDATS=[]; SEL=-1; peintRes(); peintPanier(); vq().focus();
}
/* Le prix d'une ligne : retail, gros, ou tapé à la main (Sam, 1er oct. 2026 : « dans Record a
   sale, on ne laisse pas à Sam le choix du prix wholesale et retail ; je veux qu'il puisse
   choisir le prix qu'il souhaite ou le modifier »). Deux pastilles sous la case du prix ; la
   case reste libre. La pastille du prix en cours est marquée. */
const pvrEff=cle=>{ const m=MOD[cle]; if(m&&m.pvr!=null) return +m.pvr; const v=(IDX[cle]||[])[5]; return v==null?null:+v; };
const pvwEff=cle=>{ const m=MOD[cle]; if(m&&m.pvw!=null) return +m.pvw; const v=(IDX[cle]||[])[6]; return v==null?null:+v; };
/* 4 nov. 2026 (Igal) : « Sam fait une cote pour Robert et met un parfum que Robert a déjà commandé : je veux qu'il sache
   exactement le prix que Robert a payé la dernière fois ». On cherche la vente la plus récente de CE parfum à CE client :
   les factures de l'ERP, les ventes d'avant les factures, et l'historique de gros d'avant l'ERP (tableur de Sam). */
const clientCour=()=>{ try{ return cNorm($('v-client').value); }catch(e){ return ''; } };
function dernierPrixClient(cle,cli){
  if(!cli) return null; let best=null;
  const prend=(d,h,p,q)=>{ if(p==null||p===''||!(+q>0)) return; const k=String(d||'')+' '+String(h||''); if(!best||k>best.k) best={k,d:d||'',p:+p,q:+q}; };
  const v=IDX[cle]||[]; const bcs=new Set([String(v[0]||'').replace(/^0+/,'')].concat((bcExtra()[cle]||[]).map(x=>String(x).replace(/^0+/,''))).filter(Boolean));
  FACT.forEach(f=>{ if(!f||f.sens!=='vente'||f.annule||f.retour||(f.doc&&f.doc.type==='devis')) return; if(cNorm(f.tiers)!==cli) return;
    (f.lignes||[]).forEach(l=>{ if(l&&(l.cle===cle||(l.bc&&bcs.has(String(l.bc).replace(/^0+/,''))))) prend(f.d,f.h,l.p,l.q); }); });
  try{ ((lit(KVENT,{})||{})[cle]||[]).forEach(x=>{ if(x&&cNorm(x.c)===cli) prend(x.d,x.h,x.p,x.q); }); }catch(e){}
  try{ const H=window.D_HG; if(H&&H.l&&H.c) bcs.forEach(b=>(H.l[b]||[]).forEach(r=>{ if(r&&cNorm(H.c[r[1]])===cli) prend(r[0],'',r[3],r[2]); })); }catch(e){}
  return best;
}
function puChips(l,i){
  const r=pvrEff(l.cle), w=pvwEff(l.cle);
  const ch=(k,lab,v,cls,titre)=>v==null?'':`<button type="button" class="puc${cls||''}${l.p!=null&&Math.abs(l.p-v)<0.005?' on':''}" data-pu="${i}" data-pk="${k}" data-pv="${v}"${titre?' title="'+esc(titre)+'"':''}><span>${lab}</span> <b data-nolang>${money2(v)}</b></button>`;
  let h=ch('r','retail',r)+ch('w','gros',w);
  try{ const cli=clientCour(), nom=$('v-client').value.trim(); const dp=cli?dernierPrixClient(l.cle,cli):null;
    if(dp) h+=ch('c',`<span data-nolang>${esc(nom)}</span> ${r3('a payé le','paid on','pagó el')} <span data-nolang>${dfr(dp.d)}</span>`,dp.p,' dp',nom+' '+r3('a payé ce prix la dernière fois','paid this price last time','pagó este precio la última vez')+' ('+dfr(dp.d)+', '+nf(dp.q)+')'); }catch(e){}
  return h?`<span class="pucs">${h}</span>`:'';
}
function peintPanier(){
  const c=canalCour();
  if(!PANIER.length){ $('v-pan').innerHTML='<div class="vide">Aucun parfum. Scanne un code-barres ou tape un nom ci-dessus.</div>';
    $('v-ok').disabled=true; $('v-recap').innerHTML=''; $('v-q2w').hidden=true; return; }
  const li=PANIER.map((l,i)=>{
    const v=IDX[l.cle]||[], pa=paEff(l.cle), st=stkC(l.cle,c.nom);
    const mt=(l.q||0)*(l.p||0), net=mt*(1-(c.com||0)/100);
    const mg=pa!=null&&l.p!=null?(net-pa*(l.q||0)):null;
    const pct=pa!=null&&mt>0?mg/mt*100:null;
    const cls=pct==null?'na':pct<0?'c':pct<(REG.margeMin||10)?'w':'g';
    return `<tr><td class="r" style="color:var(--ink-3);width:34px">${i+1}</td>
      <td><b class="vfiche" data-fiche="${esc(l.cle)}" title="${r3('Voir la fiche du parfum','See the perfume sheet','Ver la ficha del perfume')}">${esc(v[2]||'')} ${esc(v[1]||'')}${tyBadge(l.cle)}</b><br><span style="font-size:11.5px;color:var(--ink-3)" data-st="${i}">${esc(v[0]||'')} · ${estPC(c.nom)?'stock Perfume City':'stock'} ${nf(st)}${l.q>st?' — <b style="color:var(--crit)">manque '+nf(l.q-st)+'</b>':''}</span></td>
      <td class="r"><input type="number" min="1" step="1" data-i="${i}" data-f="q" value="${l.q}"></td>
      <td class="r"><input type="number" step="any" data-i="${i}" data-f="p" value="${l.p==null?'':l.p}" placeholder="prix">${puChips(l,i)}</td>
      <td class="r" data-mt="${i}">${money2(mt)}</td>
      <td class="r vmg" data-mg="${i}"><span class="mgl ${cls}">${mg!=null?money2(mg):'—'}</span>${pct!=null?`<br><span class="mgl ${cls}" style="font-weight:500;font-size:11px">${pc(pct)}</span>`:''}</td>
      <td><button class="del" data-del="${i}" title="Retirer">✕</button></td></tr>`; }).join('');
  const tot=PANIER.reduce((a,l)=>a+(l.q||0)*(l.p||0),0);
  const totMg=PANIER.reduce((a,l)=>{ const pa=paEff(l.cle);
    return a+(pa!=null&&l.p!=null?((l.q||0)*(l.p||0)*(1-(c.com||0)/100)-pa*(l.q||0)):0); },0);
  const u=PANIER.reduce((a,l)=>a+(l.q||0),0);
  $('v-pan').innerHTML=`<table><thead><tr><th class="r"></th><th>Parfum</th><th class="r">Qté</th>
    <th class="r">Prix unit.</th><th class="r">Montant</th><th class="r vmg">Marge nette</th><th></th></tr></thead>
    <tbody>${li}</tbody><tfoot><tr><td></td><td>${PANIER.length} parfum${PANIER.length>1?'s':''}</td>
    <td class="r" data-tu>${nf(u)}</td><td></td><td class="r" data-tmt>${money2(tot)}</td><td class="r vmg" data-tmg>${money2(totMg)}</td><td></td></tr></tfoot></table>`;
  $('v-pan').querySelectorAll('input').forEach(inp=>{
    inp.oninput=()=>{
      const l=PANIER[+inp.dataset.i]; if(!l) return;
      if(inp.dataset.f==='q') l.q=Math.max(1,Math.round(+inp.value||1)); else l.p=inp.value===''?null:+inp.value;
      if(inp.dataset.f==='p') inp.parentNode.querySelectorAll('.puc').forEach(x=>x.classList.toggle('on',l.p!=null&&Math.abs(l.p-(+x.dataset.pv))<0.005));
      majMontants(); recap(); };
    /* le tableau ne se refait JAMAIS pendant la saisie : refaire le tableau sur
       « change » recréait la case sous la souris — les flèches de quantité ne
       répondaient plus, et passer d'une case à l'autre coûtait un clic. Tout se met
       à jour sur place (majMontants, recap) ; en quittant la case on y remet
       seulement la valeur retenue (un 0 tapé redevient 1). */
    inp.onblur=()=>{ const l=PANIER[+inp.dataset.i]; if(!l) return;
      inp.value = inp.dataset.f==='q' ? l.q : (l.p==null?'':l.p); };
  });
  $('v-pan').querySelectorAll('[data-del]').forEach(b=>b.onclick=()=>{ PANIER.splice(+b.dataset.del,1); peintPanier(); });
  /* 4 nov. 2026 (Igal) : « de Cote, qu'il puisse cliquer sur le produit et avoir la fiche produit en latéral, comme s'il était
     sur le catalogue » — la fiche du Catalogue elle-même, en panneau à droite ; à sa fermeture, les prix qu'elle a pu changer sont relus */
  $('v-pan').querySelectorAll('[data-fiche]').forEach(b=>b.onclick=()=>{ if(typeof ficheFenetre!=='function') return;
    ficheFenetre(b.dataset.fiche,()=>{ try{ MOD=lit(KMOD,{})||{}; EXT=Object.assign({q:{}},JSON.parse(localStorage.getItem(KEXT)||'{}')); }catch(e){} peintPanier(); }); });
  $('v-q2w').hidden=PANIER.length<2;
  $('v-pan').querySelectorAll('[data-pu]').forEach(b=>b.onclick=()=>{
    const i=+b.dataset.pu, l=PANIER[i]; if(!l) return; l.p=+b.dataset.pv;
    const inp=$('v-pan').querySelector(`input[data-i="${i}"][data-f="p"]`); if(inp) inp.value=l.p;
    b.parentNode.querySelectorAll('.puc').forEach(x=>x.classList.toggle('on',x===b));
    majMontants(); recap(); });
  recap();
}
/* refait seulement les pastilles de prix (retail, gros, « a payé ») de chaque ligne, sans toucher aux cases de saisie */
function majChipsClient(){
  if(!PANIER.length) return;
  PANIER.forEach((l,i)=>{ const inp=$('v-pan').querySelector(`input[data-i="${i}"][data-f="p"]`); if(!inp) return;
    const old=inp.parentNode.querySelector('.pucs'); if(old) old.remove(); inp.insertAdjacentHTML('afterend',puChips(l,i));
    inp.parentNode.querySelectorAll('[data-pu]').forEach(b=>b.onclick=()=>{ const x=PANIER[+b.dataset.pu]; if(!x) return; x.p=+b.dataset.pv; inp.value=x.p;
      b.parentNode.querySelectorAll('.puc').forEach(y=>y.classList.toggle('on',y===b)); majMontants(); recap(); }); });
}
/* met à jour les montants et les totaux du panier sans recréer les champs de saisie */
function majMontants(){
  const c=canalCour(); let tot=0, totMg=0, u=0;
  PANIER.forEach((l,i)=>{
    const pa=paEff(l.cle);
    const mt=(l.q||0)*(l.p||0), net=mt*(1-(c.com||0)/100);
    const mg=pa!=null&&l.p!=null?(net-pa*(l.q||0)):null;
    const pct=pa!=null&&mt>0?mg/mt*100:null;
    const cls=pct==null?'na':pct<0?'c':pct<(REG.margeMin||10)?'w':'g';
    tot+=mt; u+=l.q||0; if(mg!=null) totMg+=mg;
    const cm=$('v-pan').querySelector(`[data-mt="${i}"]`); if(cm) cm.textContent=money2(mt);
    const cs=$('v-pan').querySelector(`[data-st="${i}"]`); if(cs){ const st=stkC(l.cle,c.nom), v=IDX[l.cle]||[];
      cs.innerHTML=`${esc(v[0]||'')} · ${estPC(c.nom)?'stock Perfume City':'stock'} ${nf(st)}${l.q>st?' — <b style="color:var(--crit)">manque '+nf(l.q-st)+'</b>':''}`; }
    const cg=$('v-pan').querySelector(`[data-mg="${i}"]`);
    if(cg) cg.innerHTML=`<span class="mgl ${cls}">${mg!=null?money2(mg):'—'}</span>`+
      (pct!=null?`<br><span class="mgl ${cls}" style="font-weight:500;font-size:11px">${pc(pct)}</span>`:'');
  });
  const a=$('v-pan').querySelector('[data-tu]'); if(a) a.textContent=nf(u);
  const b=$('v-pan').querySelector('[data-tmt]'); if(b) b.textContent=money2(tot);
  const d=$('v-pan').querySelector('[data-tmg]'); if(d) d.textContent=money2(totMg);
}
function recap(){
  const c=canalCour(), tot=PANIER.reduce((a,l)=>a+(l.q||0)*(l.p||0),0);
  const u=PANIER.reduce((a,l)=>a+(l.q||0),0);
  const net=c.com?tot*(1-c.com/100):tot;
  const pa=PANIER.reduce((a,l)=>{ const x=paEff(l.cle); return a+(x!=null?x*(l.q||0):0); },0);
  const manque=PANIER.filter(l=>l.q>stkC(l.cle,c.nom));
  const hors=PANIER.filter(l=>horsCanal(l.cle,c.id));
  const sansPrix=PANIER.filter(l=>l.p==null||!(l.p>0));
  $('v-recap').innerHTML=`Vente de <b>${nf(u)} flacon${u>1?'s':''}</b> sur <b>${esc(c.nom)}</b> pour <b>${money2(tot)}</b>.
    ${c.com?`${esc(c.nom)} garde ${c.com} % (${money2(tot*c.com/100)}) → il reste <b>${money2(net)}</b>. `:''}
    <span class="vmg">Ces flacons ont coûté ${money2(pa)} → marge <b>${money2(net-pa)}</b>${tot>0?` (${pc((net-pa)/tot*100)})`:''}.</span>
    ${$('v-stock').checked?(estPC(c.nom)?"L'inventaire de <b>Perfume City</b> sera diminué de ces quantités ; le stock central ne bouge pas.":'Le stock sera diminué de ces quantités.'):'Le stock ne bouge pas.'}
    ${hors.length?`<br><b style="color:var(--warn)">${hors.length===1?'Ce parfum est marqué':'Ces '+hors.length+' parfums sont marqués'} « pas vendu sur ${esc(c.nom)} »</b> dans la fiche catalogue. La vente s'enregistre quand même — à corriger dans la fiche si c'est une erreur.`:''}
    ${manque.length?`<br><b style="color:var(--crit)">${manque.length} parfum${manque.length>1?'s':''} en stock insuffisant</b> — la vente est enregistrée quand même, le stock tombe à zéro.`:''}
    ${sansPrix.length?`<br><b style="color:var(--crit)">${sansPrix.length} ligne${sansPrix.length>1?'s':''} sans prix de vente.</b>`:''}`;
  $('v-ok').disabled = !PANIER.length || sansPrix.length>0 || (!!$('v-doc').value && !$('v-client').value.trim());
  /* un bouton gris sans explication, c'est un écran bloqué : on dit ce qui manque,
     à côté du bouton, et la case vide est cerclée de rouge */
  const pourquoi = !PANIER.length ? '' : sansPrix.length ? (sansPrix.length===1
      ? 'Il manque le prix de « '+(((IDX[sansPrix[0].cle]||[])[2]||'')+' '+((IDX[sansPrix[0].cle]||[])[1]||'')).trim()+' » — tape-le dans la colonne des prix.'
      : sansPrix.length+' lignes sans prix — tape-les dans la colonne des prix.')
    : (!!$('v-doc').value && !$('v-client').value.trim()) ? 'Un document a besoin d\'un nom de client.' : '';
  if(pourquoi || $('v-msg').dataset.auto==='1'){ $('v-msg').textContent=pourquoi; $('v-msg').dataset.auto=pourquoi?'1':''; $('v-msg').style.color=pourquoi?'var(--crit)':''; }
  $('v-pan').querySelectorAll('input[data-f="p"]').forEach(inp=>{ const l=PANIER[+inp.dataset.i]; inp.classList.toggle('manque', !!l && (l.p==null||!(l.p>0))); });
  try{ docTotaux(); }catch(e){}
}
/* ---- modifier une vente déjà enregistrée (Sam, 6 oct. 2026 : « quand je record une sale et
   qu'elle est enregistrée, j'aimerais pouvoir la modifier ») ----
   Même fenêtre que la saisie, pré-remplie. À l'enregistrement : les flacons de l'ancienne
   version reviennent en stock, ceux de la nouvelle en sortent, la facture est recalculée en
   gardant son numéro, et le journal garde l'avant et l'après. Seules les ventes saisies ici
   se modifient : une vente venue d'Amazon, du site ou de la caisse se corrige à la source,
   et une vente déjà remboursée ne bouge plus. */
let EDIT=null;
/* 6 nov. 2026 (Igal pour Sam : « fusionner les cotes qu'il a faites pour le même client ») : la cote dans laquelle on réunit
   les autres, et les autres (qui seront archivées « fusionnée dans … » une fois la cote réunie enregistrée). */
let FUSION=null;
/* les autres cotes « créées » (ni converties, ni archivées, ni Lightspeed) du même client */
function cotesAFusionner(f){
  if(!f||!f.doc||f.doc.type!=='devis'||f.doc.converti||f.doc.archive||f.lsq) return [];
  const k=cNorm(f.tiers); if(!k) return [];
  return FACT.filter(x=>x&&x.id!==f.id&&x.doc&&x.doc.type==='devis'&&!x.doc.converti&&!x.doc.archive&&!x.lsq&&cNorm(x.tiers)===k)
    .sort((a,b)=>String(a.t||a.d||'').localeCompare(String(b.t||b.d||'')));
}
/* réunir les lignes : un même parfum au même prix additionne ses quantités ; sinon la ligne reste à part */
function fusionneLignes(cotes){
  const out=[];
  cotes.forEach(c=>(c.lignes||[]).filter(l=>l.cle&&l.q).forEach(l=>{ const p=(l.remise&&l.pAv!=null)?+l.pAv:(l.p==null?null:+l.p);
    const m=out.find(x=>x.cle===l.cle&&x.p===p); if(m) m.q+=+l.q||0; else out.push({cle:l.cle,q:+l.q||0,p}); }));
  return out;
}
function fusionneCotes(f){
  f=FACT.find(z=>z.id===f.id)||f; const A=cotesAFusionner(f); if(!A.length||!peutModifierDevis(f)) return;
  const nums=A.map(x=>x.doc.num);
  const msg=r3(`Fusionner ${A.length+1} cotes de ${f.tiers} dans ${f.doc.num} ?\n\nLes parfums de ${nums.join(', ')} sont ajoutés à ${f.doc.num} (un même parfum au même prix : les quantités s'additionnent). Tu vérifies, puis « Enregistrer ». À ce moment-là, ${nums.join(' et ')} ${A.length>1?'seront archivées':'sera archivée'} avec la mention « fusionnée dans ${f.doc.num} ».`,
    `Merge ${A.length+1} quotes of ${f.tiers} into ${f.doc.num}?\n\nThe perfumes of ${nums.join(', ')} are added to ${f.doc.num} (same perfume at the same price: quantities add up). Check, then "Save". At that point, ${nums.join(' and ')} will be archived as "merged into ${f.doc.num}".`,
    `¿Fusionar ${A.length+1} cotizaciones de ${f.tiers} en ${f.doc.num}?\n\nLos perfumes de ${nums.join(', ')} se añaden a ${f.doc.num} (mismo perfume al mismo precio: las cantidades se suman). Revisa y luego «Guardar». En ese momento ${nums.join(' y ')} se archivará(n) como «fusionada en ${f.doc.num}».`);
  if(!confirm(msg)) return;
  ouvreModif(f);
  PANIER=fusionneLignes([f].concat(A));
  FUSION={into:f.id,autres:A.map(x=>x.id)};
  const h=document.querySelector('#vov .mh h3'); if(h) h.textContent=r3('Fusion des cotes','Merging quotes','Fusión de cotizaciones')+' '+[f.doc.num].concat(nums).join(' + ');
  peintPanier(); recap();
  $('v-msg').textContent=r3(`${A.length+1} cotes réunies : vérifie les parfums et les prix, puis Enregistrer. ${nums.join(', ')} ${A.length>1?'seront archivées':'sera archivée'}.`,
    `${A.length+1} quotes combined: check the perfumes and prices, then Save. ${nums.join(', ')} will be archived.`,
    `${A.length+1} cotizaciones reunidas: revisa los perfumes y los precios y luego Guardar. ${nums.join(', ')} se archivará(n).`); $('v-msg').className='msg';
}
function peutModifierVente(f){
  if(!f||MODE_QUOTES) return false;
  if(typeof peut==='function'&&!peut('vendre')) return false;
  if(!f.manuel||f.sens!=='vente'||f.retour||f.annule) return false;
  if(f.doc&&f.doc.converti) return false;
  if(FACT.some(z=>z.retour&&z.refId===f.id)) return false;
  return true;
}
/* 15 oct. 2026 (Igal : « quand Sam fait une cote et qu'il clique dessus, il faut qu'il puisse la
   modifier ») : une cote faite dans l'ERP se rouvre dans le formulaire de cote, pré-remplie
   (client, parfums, quantités, prix, remise, note). Elle garde son numéro, sa date d'émission et
   ses envois ; le stock ne bouge pas, une cote n'en sort jamais. Une cote déjà convertie en
   facture ne se modifie plus (sa facture, elle, se corrige dans Ventes) ; une cote de Lightspeed
   se corrige dans Lightspeed. */
function peutModifierDevis(f){
  if(!f||!MODE_QUOTES||f.lsq) return false;
  if(typeof peut==='function'&&!peut('vendre')) return false;
  if(!f.doc||f.doc.type!=='devis'||f.doc.converti) return false;
  return true;
}
function ouvreModif(f){
  f=FACT.find(z=>z.id===f.id)||f;
  const estD=peutModifierDevis(f);
  if(!estD&&!peutModifierVente(f)) return;
  ouvreVente(); EDIT=f;
  const CV=CANAUX_VENTE();
  if(f.canal&&!CV.some(c=>c.nom===f.canal)) $('v-canal').insertAdjacentHTML('beforeend',`<option value="${esc(f.canal)}">${esc(nomAff(f.canal))}</option>`);
  if(f.canal) $('v-canal').value=f.canal;
  $('v-date').value=f.d||ajd(); $('v-client').value=f.tiers||''; $('v-num').value=f.num||'';
  if($('v-note')) $('v-note').value=(f.doc&&f.doc.note)||'';
  $('v-stock').checked=estD?false:f.stock!==false; $('v-stock').dataset.touche='1';
  PANIER=(f.lignes||[]).filter(l=>l.cle).map(l=>({cle:l.cle,q:+l.q||0,p:(l.remise&&l.pAv!=null)?+l.pAv:(l.p==null?null:+l.p)}));
  const D=f.doc||{};
  $('v-doc').value=f.doc?(estD?'devis':'facture'):''; $('v-doc').dataset.touche='1';
  if(f.doc){
    if(D.pmode&&FMODES[D.pmode]) $('v-pmode').value=D.pmode;
    const regle=+D.regle||0, reste=+D.reste||0;
    $('v-pstat').value=reste<=0?'paye':(regle>0?'partiel':'apayer'); $('v-pregle').value=(reste>0&&regle>0)?regle:'';
    $('v-fiscal').value=D.fiscal||'taxable'; $('v-fref').value=D.fref||'';
    $('v-remtype').value=D.remType||'pct'; $('v-remval').value=D.remVal||''; $('v-remlib').value=D.remLib||'';
    if($('v-port')) $('v-port').value=D.port>0?D.port:'';
    $('v-langue').value=D.langue||'';
  }
  majAide();
  const h=document.querySelector('#vov .mh h3'); if(h) h.textContent=vf(estD?'Modifier le devis':'Modifier la vente')+' '+(estD?(D.num||''):(f.num||''));
  $('v-ok').textContent=vf('Enregistrer les modifications');
  try{ docChampsMaj(); }catch(e){}
  peintPanier(); recap();
  if(estD){ try{ $('vov').scrollIntoView({behavior:'smooth',block:'start'}); }catch(e){} }
}
function ouvreVente(){
  _PCI=null;
  PANIER=[]; CANDIDATS=[]; SEL=-1; EDIT=null; FUSION=null;
  { const h=document.querySelector('#vov .mh h3'); if(h) h.textContent=vf('Enregistrer une vente'); $('v-ok').textContent=vf('Enregistrer la vente'); }
  const CV=CANAUX_VENTE();
  $('v-canal').innerHTML=CV.map(c=>`<option value="${esc(c.nom)}">${esc(nomAff(c.nom))}</option>`).join('');
  if(canalSel && CV.some(c=>c.nom===canalSel)) $('v-canal').value=canalSel;
  $('v-date').value=ajd();
  $('v-client').value=''; $('v-num').value=numAuto($('v-date').value); vqActive('v-q'); vq().value=''; $('v-q2').value=''; $('v-msg').textContent='';
  if($('v-note')) $('v-note').value='';
  $('v-msg').className='msg';
  $('v-stock').checked=true;
  majAide(); peintRes(); peintPanier();
  try{ docReset(); }catch(e){}
  $('vov').classList.add('on'); setTimeout(()=>vq().focus(),60);
}
function majAide(){
  const c=canalCour();
  /* 28 sept. : la phrase restait en français sur l'écran anglais (capture d'Igal) */
  const _nc=canalCourt(c.nom);
  $('v-aide').textContent = c.com ? r3(`${_nc} garde ${c.com} % sur chaque vente (réglages).`, `${_nc} keeps ${c.com}% of every sale (settings).`, `${_nc} se queda con el ${c.com} % de cada venta (ajustes).`)
    : c.id==='gros' ? r3('Prix de gros proposé automatiquement.','Wholesale price filled in automatically.','Precio mayorista propuesto automáticamente.') : r3('Prix de vente du canal proposé automatiquement.','Channel selling price filled in automatically.','Precio de venta del canal propuesto automáticamente.');
}
/* ---------------- annuler une vente / rembourser ----------------
   Rien n'est effacé : le remboursement est enregistré comme une ligne en négatif rattachée
   à la vente d'origine. Le chiffre d'affaires et la marge baissent d'eux-mêmes, et on garde
   la trace de ce qui a été rendu, comment, et pourquoi. */
const MODES_R=[['especes','Espèces'],['zelle','Zelle'],['virement','Virement'],['carte','Carte (remboursement)'],
  ['cheque','Chèque'],['avoir','Avoir / crédit chez nous'],['echange','Échange contre un autre parfum'],['aucun','Rien rendu (annulation d\'une erreur de saisie)']];
/* libellé court, pour la ligne du journal */
const COURT={especes:'espèces',zelle:'Zelle',virement:'virement',carte:'carte',cheque:'chèque',
  avoir:'avoir',echange:'échange',aucun:'rien rendu'};
const MOTIFS_R=[['retour','Retour du client'],['erreur','Erreur de saisie'],['annulation','Commande annulée'],
  ['defectueux','Produit défectueux ou abîmé'],['perdu','Colis perdu ou volé'],['autre','Autre']];
let RET=null;

/* ce qui a déjà été remboursé sur une vente, ligne par ligne */
function dejaRendu(fid){
  const r={};
  FACT.filter(f=>f.retour&&f.refId===fid).forEach(f=>(f.lignes||[]).forEach(l=>{ r[l.cle]=(r[l.cle]||0)+Math.abs(l.q||0); }));
  return r;
}
function ouvreRetour(fid){
  const f=FACT.find(x=>x.id===fid); if(!f) return;
  if(f.retour){ alert("Cette ligne est déjà un remboursement."); return; }
  const rendu=dejaRendu(fid);
  const lignes=(f.lignes||[]).map(l=>{ const reste=Math.max(0,(l.q||0)-(rendu[l.cle]||0));
    /* ce qui est réellement sorti du stock à la vente : c'est le maximum qui peut y revenir.
       Une vente de 10 sur un stock de 3 n'a fait sortir que 3 flacons. */
    const sorti=Math.max(0,(l.qAv==null||l.qAp==null)?(l.q||0):(l.qAv-l.qAp));
    return {cle:l.cle,bc:l.bc,ref:l.ref,q:l.q,p:l.p,paAv:l.paAv,reste,n:reste,sorti,rendu:(rendu[l.cle]||0)}; }).filter(l=>l.q);
  if(!lignes.some(l=>l.reste>0)){ alert("Cette vente a déjà été entièrement remboursée."); return; }
  RET={f,lignes};
  { const np=(f.lignes||[]).length, pl=np>1, B=x=>'<b>'+x+'</b>';
    const cn=esc((typeof lgMot==='function'&&lgMot(f.canal||NP))||f.canal||NP);
    $('ret-tete').innerHTML='<span data-nolang>'+L3(
      `Vente ${B(esc(f.num))} du ${B(dfr(f.d))} sur ${B(cn)}${f.tiers?' — '+B(esc(f.tiers)):''}, ${nf(np)} parfum${pl?'s':''} pour ${B(money2(f.montant||0))}, enregistrée par ${esc(f.par||'—')}.`,
      `Sale ${B(esc(f.num))} of ${B(dfr(f.d))} on ${B(cn)}${f.tiers?' — '+B(esc(f.tiers)):''}, ${nf(np)} perfume${pl?'s':''} for ${B(money2(f.montant||0))}, recorded by ${esc(f.par||'—')}.`,
      `Venta ${B(esc(f.num))} del ${B(dfr(f.d))} en ${B(cn)}${f.tiers?' — '+B(esc(f.tiers)):''}, ${nf(np)} perfume${pl?'s':''} por ${B(money2(f.montant||0))}, registrada por ${esc(f.par||'—')}.`)
      +(Object.keys(rendu).length?'<br>'+L3('Une partie a déjà été remboursée : les quantités proposées tiennent compte de ce qui reste.','Part of it has already been refunded: the quantities offered take what remains into account.','Una parte ya se reembolsó: las cantidades propuestas tienen en cuenta lo que queda.'):'')+'</span>'; }
  $('ret-mode').innerHTML=MODES_R.map(([v,l])=>`<option value="${v}">${l}</option>`).join('');
  $('ret-motif').innerHTML=MOTIFS_R.map(([v,l])=>`<option value="${v}">${l}</option>`).join('');
  $('ret-date').value=ajd();
  $('ret-note').value=''; $('ret-stock').checked=true; $('ret-msg').textContent=''; $('ret-msg').className='msg';
  peintRetour();
  $('retov').classList.add('on');
}
function peintRetour(){
  const L=RET.lignes;
  $('ret-pan').innerHTML=`<table><thead><tr><th></th><th>Parfum</th><th class="r">Vendu</th>
    <th class="r">À rembourser</th><th class="r">Prix unit.</th><th class="r">Montant rendu</th></tr></thead>
    <tbody>${L.map((l,i)=>`<tr><td class="r" style="color:var(--ink-3);width:30px">${i+1}</td>
      <td><b>${esc(l.ref)}${tyVu(l)}</b><br><span style="font-size:11.5px;color:var(--ink-3)">${esc(l.bc||'')}${l.reste<l.q?` · déjà remboursé ${nf(l.q-l.reste)}`:''}</span></td>
      <td class="r">${nf(l.q)}</td>
      <td class="r"><input type="number" min="0" max="${l.reste}" step="1" data-r="${i}" value="${l.n}"${l.reste?'':' disabled'}></td>
      <td class="r">${l.p!=null?money2(l.p):'—'}</td>
      <td class="r">${money2((l.n||0)*(l.p||0))}</td></tr>`).join('')}</tbody>
    <tfoot><tr><td></td><td>Total rendu au client</td><td></td>
      <td class="r">${nf(L.reduce((a,l)=>a+(l.n||0),0))}</td><td></td>
      <td class="r">${money2(L.reduce((a,l)=>a+(l.n||0)*(l.p||0),0))}</td></tr></tfoot></table>`;
  /* On ne redessine pas le tableau pendant la frappe : le champ serait recréé et le
     deuxième chiffre partirait dans le vide (« 12 » donnait « 1 »). On met à jour les
     totaux, et le tableau se refait quand on quitte la case. */
  $('ret-pan').querySelectorAll('input[data-r]').forEach(inp=>{
    inp.oninput=()=>{ const l=RET.lignes[+inp.dataset.r]; const t=inp.value.trim();
      if(t==='') { l.n=0; recapRetour(); return; }
      l.n=Math.max(0,Math.min(l.reste,Math.round(+t||0)));
      recapRetour(); };
    inp.onchange=()=>{ const l=RET.lignes[+inp.dataset.r];
      if(+inp.value!==l.n) inp.value=l.n;   /* on remet la valeur retenue si elle a été bornée */
      peintRetour(); };
  });
  recapRetour();
}
/* Combien de flacons d'une ligne peuvent revenir en stock.
   Igal, 26 sept. 2026 : « quand il y a un refund, il faut que le stock se mette à jour ».
   Avant, on ne remettait que ce que l'ERP avait fait sortir : une vente de 5 sur un stock
   compté à 0 ne remettait rien au retour. Or les 5 flacons existaient bien — ils sont
   partis chez le client — c'est le compte de l'ERP qui était faux. Quand la marchandise
   revient, elle est de nouveau sur l'étagère : on remet tout ce qui a été vendu.
   Deux exceptions : la vente avait été enregistrée « sans toucher au stock » (rien à
   défaire), et l'erreur de saisie (on défait seulement ce que l'ERP avait bougé : une
   vente tapée 10 au lieu de 1 sur un stock de 3 ne doit pas fabriquer 7 flacons). */
function retourMax(l,f,motif){
  if(f&&f.stock===false) return 0;
  const base = motif==='erreur' ? (l.sorti||0) : (l.q||0);
  return Math.max(0, base-(l.rendu||0));
}
/* le récapitulatif est écrit dans la langue de l'écran, d'un seul tenant : la
   traduction mot à mot laissait « 5 bottles … in Cash » au milieu d'une phrase
   française (le nom du canal et les montants empêchaient de reconnaître la phrase) */
function r3(fr,en,es){ const lg=(typeof LANG==='string')?LANG:'fr'; return lg==='en'?en:lg==='es'?es:fr; }
const MODES_R3={especes:['en espèces','in cash','en efectivo'],zelle:['par Zelle','by Zelle','por Zelle'],
  virement:['par virement','by bank transfer','por transferencia'],carte:['sur la carte','to the card','a la tarjeta'],
  cheque:['par chèque','by check','con cheque']};
function recapRetour(){
  const L=RET.lignes, f=RET.f;
  const n=L.reduce((a,l)=>a+(l.n||0),0), mt=L.reduce((a,l)=>a+(l.n||0)*(l.p||0),0);
  const pa=L.reduce((a,l)=>a+(l.paAv!=null?l.paAv*(l.n||0):0),0);
  const comR=comCanal(f.canal);
  const total=(f.lignes||[]).reduce((a,l)=>a+(l.q||0),0);
  const mode=$('ret-mode').value, motif=$('ret-motif').value;
  const B=x=>'<b>'+x+'</b>', can='<span data-nolang>'+esc(f.canal||'')+'</span>';
  const fl=(k)=>r3(k>1?'flacons':'flacon', k>1?'bottles':'bottle', k>1?'frascos':'frasco');
  if(!n){ $('ret-recap').innerHTML='<span data-nolang>'+r3('Indique au moins une quantité à rembourser.','Enter at least one quantity to refund.','Indica al menos una cantidad a reembolsar.')+'</span>'; $('ret-ok').disabled=true; return; }
  let comment;
  if(mode==='avoir') comment=r3('sous forme d\'<b>avoir</b> (rien ne sort de la caisse)','as <b>store credit</b> (no money leaves the till)','como <b>crédito</b> (no sale dinero de la caja)');
  else if(mode==='aucun') comment=r3('<b>sans rien rendre</b> — la vente est simplement effacée des chiffres','<b>with nothing given back</b> — the sale is simply removed from the figures','<b>sin devolver nada</b> — la venta simplemente se borra de las cifras');
  else if(mode==='echange') comment=r3('par <b>échange</b> — pense à enregistrer la nouvelle vente ensuite','by <b>exchange</b> — remember to record the new sale afterwards','por <b>cambio</b> — recuerda registrar la nueva venta después');
  else { const m=MODES_R3[mode]||['','','']; comment=B(r3(m[0],m[1],m[2])); }
  const p1=r3(`Remboursement de ${B(nf(n)+' '+fl(n))} sur ${nf(total)} pour ${B(money2(mt))} ${comment}.`,
              `Refund of ${B(nf(n)+' '+fl(n))} out of ${nf(total)} for ${B(money2(mt))} ${comment}.`,
              `Reembolso de ${B(nf(n)+' '+fl(n))} de ${nf(total)} por ${B(money2(mt))} ${comment}.`);
  const com=comR?r3(` — dont ${money2(mt*comR/100)} de commission que ${can} garde malgré le retour`,
                    ` — including ${money2(mt*comR/100)} of fees that ${can} keeps despite the return`,
                    ` — incluidos ${money2(mt*comR/100)} de comisión que ${can} se queda pese a la devolución`):'';
  const p2=!vmg()?r3(`Le chiffre d'affaires baisse de ${money2(mt)}${com}.`,`Sales go down by ${money2(mt)}${com}.`,`Las ventas bajan ${money2(mt)}${com}.`):r3(`Le chiffre d'affaires baisse de ${money2(mt)} et la marge nette de ${B(money2(mt-pa))}${com}.`,
              `Sales go down by ${money2(mt)} and net margin by ${B(money2(mt-pa))}${com}.`,
              `Las ventas bajan ${money2(mt)} y el margen neto ${B(money2(mt-pa))}${com}.`);
  let p3;
  if(!$('ret-stock').checked) p3=r3('Le stock ne bouge pas.','Stock does not change.','El stock no cambia.');
  else {
    const r=L.reduce((a,l)=>a+Math.min(l.n||0,retourMax(l,f,motif)),0);
    if(r) p3=r3(`${B(nf(r)+' '+fl(r))} ${r>1?'reviennent':'revient'} en stock${r<n?` (les ${nf(n-r)} autres n'avaient pas été sortis par l'ERP)`:''}.`,
                `${B(nf(r)+' '+fl(r))} ${r>1?'go':'goes'} back into stock${r<n?` (the other ${nf(n-r)} had not been taken out by the ERP)`:''}.`,
                `${B(nf(r)+' '+fl(r))} ${r>1?'vuelven':'vuelve'} al stock${r<n?` (los otros ${nf(n-r)} no habían salido en el ERP)`:''}.`);
    else p3=f.stock===false
      ? r3('Aucun flacon ne revient en stock : la vente avait été enregistrée sans toucher au stock.','No bottle goes back into stock: the sale was recorded without touching stock.','Ningún frasco vuelve al stock: la venta se registró sin tocar el stock.')
      : r3('Aucun flacon ne revient en stock : pour une erreur de saisie, on ne défait que ce que l\'ERP avait sorti, et il n\'avait rien sorti.','No bottle goes back into stock: for a typing error, only what the ERP had taken out is undone, and it had taken out nothing.','Ningún frasco vuelve al stock: en un error de captura solo se deshace lo que el ERP había sacado, y no había sacado nada.');
  }
  const p4=n===total?'<br>'+r3('C\'est la vente entière : elle sera annulée.','This is the whole sale: it will be cancelled.','Es la venta completa: quedará anulada.'):'';
  $('ret-recap').innerHTML='<span data-nolang>'+p1+' '+p2+' '+p3+p4+'</span>';
  $('ret-ok').disabled = !n;
}
['ret-mode','ret-motif','ret-stock'].forEach(i=>$(i).addEventListener('change',recapRetour));
$('ret-x').onclick=$('ret-ann').onclick=()=>{ $('retov').classList.remove('on'); RET=null; };
$('ret-ok').onclick=()=>{
  if(!RET) return;
  if(!signe("ce remboursement",()=>$('ret-ok').click())) return;
  _PCI=null;
  const f=RET.f, L=RET.lignes.filter(l=>l.n>0);
  const d=$('ret-date').value||ajd();
  const mode=$('ret-mode').value, motif=$('ret-motif').value, note=$('ret-note').value.trim();
  const VENT=lit(KVENT,{}), JOU=lit(KJOU,[]);
  const lignes=[], det=[]; let remis=0;
  const pcR=!!f.pc;                               /* la vente était une vente Perfume City : les flacons reviennent à SON inventaire */
  L.forEach(l=>{
    const qAv=pcR?pcQte(l.cle):qteEff(l.cle);
    const remisMax=retourMax(l,f,motif);   /* voir retourMax : tout ce qui a été vendu, sauf erreur de saisie */
    const qAp=$('ret-stock').checked?qAv+Math.min(l.n,remisMax):qAv;
    lignes.push({cle:l.cle,bc:l.bc,ref:l.ref,q:-l.n,p:l.p,qAv,qAp,paAv:l.paAv,pc:pcR||undefined});
    if(qAp!==qAv){ if(pcR) pcPose(l.cle,qAp); else MOD[l.cle]=Object.assign({},MOD[l.cle]||{},{qte:qAp}); det.push({bc:l.bc,ref:l.ref,av:qAv,ap:qAp}); remis+=(qAp-qAv); }
    (VENT[l.cle]=VENT[l.cle]||[]).push({d,p:l.p,c:f.tiers||'',q:-l.n,num:f.num+' (remboursé)',k:f.canal});
  });
  const mt=L.reduce((a,l)=>a+l.n*(l.p||0),0);
  const nR=FACT.filter(x=>x.retour&&x.refId===f.id).length+1;
  const num=f.num+'-R'+nR;
  FACT.push({id:'r'+Date.now().toString(36),num,sens:'vente',retour:true,refId:f.id,refNum:f.num,
    canal:f.canal,tiers:f.tiers,d,lignes,montant:-mt,stock:$('ret-stock').checked,pc:pcR||undefined,
    mode,motif,note,par:USR||'(non renseigné)',t:new Date().toISOString()});
  pcSauve();
  ecrit(KFACT,FACT); ecrit(KMOD,MOD); ecrit(KVENT,VENT);
  const libMode=(MODES_R.find(m=>m[0]===mode)||['','—'])[1], libMotif=(MOTIFS_R.find(m=>m[0]===motif)||['','—'])[1];
  JOU.push({t:new Date().toISOString(),u:USR||'(non renseigné)',act:'annulation',
    lib:'remboursement '+num+' — '+libMotif.toLowerCase()+', '+(mode==='aucun'?'rien rendu':'rendu en '+(COURT[mode]||libMode.toLowerCase()))+(note?' ('+note+')':''),
    n:det.length,impact:Math.round(mt),det});
  ecrit(KJOU,JOU);
  construitV();
  $('retov').classList.remove('on'); RET=null; vus=80; dessine();
  const b=document.createElement('div'); b.className='info';
  b.style.background='var(--crit-soft)'; b.style.borderLeftColor='var(--crit)';
  b.innerHTML=`<b>Remboursement ${esc(num)} enregistré</b> — ${money2(mt)} ${mode==='aucun'?'(rien rendu au client)':'rendu en '+esc(COURT[mode]||libMode.toLowerCase())}${remis?`, ${nf(remis)} flacon${remis>1?'s':''} remis en stock`:', stock inchangé'}. La vente d'origine reste au journal.`;
  $('corps').parentNode.insertBefore(b,$('corps'));
  setTimeout(()=>b.remove(),9000);
};

$('nv').onclick=ouvreVente;
function fermeVente(force){
  if(!force && PANIER.length && !confirm(`Abandonner cette vente ?\n\n${PANIER.length} parfum${PANIER.length>1?'s':''} dans le panier, ${money2(PANIER.reduce((a,l)=>a+(l.q||0)*(l.p||0),0))}. Rien ne sera enregistré.`)) return;
  $('vov').classList.remove('on');
}
$('vx').onclick=$('v-ann').onclick=()=>fermeVente(false);
document.addEventListener('keydown',e=>{
  if(e.key!=='Escape') return;
  if($('retov').classList.contains('on')){ $('retov').classList.remove('on'); RET=null; return; }
  if($('dov').classList.contains('on')){ fermeDetail(); return; }
  if($('msgov').classList.contains('on')){ mFerme(); return; }
  if($('vov').classList.contains('on')) fermeVente(false);
});
$('v-canal').onchange=()=>{ majAide();
  PANIER.forEach(l=>{ if(l.pf) return; /* prix donné par la liste du client : on n'y touche pas */ const p=prixSuggere(l.cle,canalCour()); if(p!=null) l.p=p; });
  /* une vente saisie ici est une facture, sur tous les canaux (Igal, 12 sept. 2026) */
  if(!$('v-doc').dataset.touche){ $('v-doc').value='facture'; try{ docChampsMaj(); }catch(e){} }
  peintPanier(); };
$('v-doc').addEventListener('change',()=>{ $('v-doc').dataset.touche='1'; recap(); });
$('v-client').addEventListener('input',recap);
/* le client vient de changer : seules les pastilles de prix sont refaites, et un instant après — si Sam clique une pastille
   juste en quittant la case du client, le clic arrive AVANT que la pastille soit remplacée (sinon il se perdait) */
$('v-client').addEventListener('change',()=>{ setTimeout(majChipsClient,250); });
$('v-stock').onchange=recap;
/* on change la date : le numéro proposé suit, tant qu'il n'a pas été retouché à la main */
$('v-date').onchange=()=>{ const v=$('v-num').value.trim();
  if(!v || /^V\d{6}-\d{3}$/.test(v)) $('v-num').value=numAuto($('v-date').value); };
$('v-num').oninput=()=>{ const v=$('v-num').value.trim();
  if(v && numPris(v)){ const f=FACT.find(x=>String(x.num||'').toLowerCase()===v.toLowerCase());
    $('v-msg').textContent='Ce numéro est déjà pris (vente du '+dfr(f.d)+(f.canal?' sur '+f.canal:'')+').';
    $('v-msg').className='msg err'; }
  else { $('v-msg').textContent=''; $('v-msg').className='msg'; } };
vq().oninput=()=>{ CANDIDATS=chercheProduits(vq().value); SEL=-1; peintRes();
  if(CANDIDATS.length===1 && /^\d{8,14}$/.test(vq().value.trim())) ajoute(CANDIDATS[0]); };
vq().onkeydown=e=>{
  if(e.key==='ArrowDown'){ e.preventDefault(); SEL=Math.min(SEL+1,CANDIDATS.length-1); peintRes(); }
  else if(e.key==='ArrowUp'){ e.preventDefault(); SEL=Math.max(SEL-1,0); peintRes(); }
  else if(e.key==='Enter'){ e.preventDefault(); if(CANDIDATS.length) ajoute(CANDIDATS[SEL<0?0:SEL]); }
};
{ const h=$('v-q'); $('v-q2').oninput=h.oninput; $('v-q2').onkeydown=h.onkeydown;
  ['v-q','v-q2'].forEach(id=>$(id).addEventListener('focus',()=>vqActive(id))); }
$('v-ok').onclick=()=>{
  if(!PANIER.length) return;
  if(!window.__FRAIS_OK) return surStockServeur(()=>{ window.__FRAIS_OK=true; try{ $('v-ok').onclick(); } finally { window.__FRAIS_OK=false; } }, $('v-ok'));
  if(!signe("cette vente",()=>$('v-ok').click())) return;
  _PCI=null;                                      /* l'inventaire Perfume City est relu : un autre onglet a pu le changer */
  const canal=$('v-canal').value, d=$('v-date').value||ajd();
  const client=$('v-client').value.trim();
  const num=$('v-num').value.trim() || numAuto(d);
  const old=EDIT?(FACT.find(z=>z.id===EDIT.id)||EDIT):null;
  if(numPris(num)&&!(old&&String(old.num||'').toLowerCase()===num.toLowerCase())){
    const f=FACT.find(x=>String(x.num||'').toLowerCase()===num.toLowerCase());
    $('v-msg').textContent='Le numéro '+num+' existe déjà (vente du '+dfr(f.d)+(f.canal?' sur '+f.canal:'')+'). Change-le : deux ventes ne peuvent pas porter le même numéro.';
    $('v-msg').className='msg err'; $('v-num').focus(); return; }
  const VENT=lit(KVENT,{}), CLI=lit(KCLI,{}), JOU=lit(KJOU,[]);
  const lignes=[], det=[];
  let sortis=0;
  const estDevis=$('v-doc').value==='devis';
  /* Le document se calcule sur les prix affichés — plein tarif — parce que c'est
     lui qui porte la remise en clair, sous les yeux du client. Les lignes
     ENREGISTRÉES, elles, prennent les prix réellement encaissés, remise répartie.
     Sans ça, l'ERP garderait le prix plein et la marge serait fausse à la hausse :
     une remise de 10 % sur 2 178 $, c'est 218 $ de marge envolés que personne ne
     verrait jamais passer. */
  const doc=docPourVente(PANIER.map(l=>({q:l.q,p:l.p})),client,d,CLI,estPC(canal)), devis=!!(doc&&doc.type==='devis');
  const PAN=(doc&&doc.remise)?repartitRemise(PANIER,doc):PANIER;
  /* modification : l'ancienne version rend d'abord ses flacons et ses lignes de ventes */
  if(old){
    if(old.stock!==false) (old.lignes||[]).forEach(l=>{ if(!l.cle) return;
      const sorti=(l.qAv!=null&&l.qAp!=null)?Math.max(0,(+l.qAv)-(+l.qAp)):(+l.q||0); if(!sorti) return;
      const dePC=!!(l.pc||old.pc);                /* les flacons étaient sortis de l'inventaire Perfume City : ils y retournent */
      const q0=dePC?pcQte(l.cle):qteEff(l.cle);
      if(dePC) pcPose(l.cle,q0+sorti); else MOD[l.cle]=Object.assign({},MOD[l.cle]||{},{qte:q0+sorti});
      const v=IDX[l.cle]||[]; det.push({bc:v[0],ref:l.ref,av:q0,ap:q0+sorti}); });
    if(old.sens!=='devis') (old.lignes||[]).forEach(l=>{ if(!l.cle||!VENT[l.cle]) return;
      VENT[l.cle]=VENT[l.cle].filter(e=>!(String(e.num||'')===String(old.num||'')&&e.k===old.canal&&e.d===old.d)); });
  }
  const pcVente=estPC(canal);                     /* Perfume City : les flacons sortent de SON inventaire */
  PAN.forEach(l=>{
    const v=IDX[l.cle]||[], ref=((v[2]||'')+' '+(v[1]||'')+tyTexte(l.cle)).trim(), qAv=pcVente?pcQte(l.cle):qteEff(l.cle);
    const qAp=($('v-stock').checked&&!estDevis)?Math.max(0,qAv-(l.q||0)):qAv;
    lignes.push({cle:l.cle,bc:v[0],ref,q:l.q,p:l.p,qAv,qAp,manque:Math.max(0,(l.q||0)-qAv),paAv:paEff(l.cle),
                 pAv:l.pAv==null?undefined:l.pAv,pc:pcVente||undefined});
    if(qAp!==qAv){ if(pcVente) pcPose(l.cle,qAp); else MOD[l.cle]=Object.assign({},MOD[l.cle]||{},{qte:qAp}); det.push({bc:v[0],ref,av:qAv,ap:qAp}); sortis+=qAv-qAp; }
    if(!estDevis) (VENT[l.cle]=VENT[l.cle]||[]).push({d,h:heureMiami(),p:l.p,c:client,q:l.q,num,k:canal});
  });
  pcSauve();                                      /* inventaire Perfume City : écrit une fois, après tous les mouvements */
  if(client) CLI[client]=Object.assign({nom:client},CLI[client]||{},{maj:new Date().toISOString()});
  if(client) clientDansRetail(client);
  const montant=PAN.reduce((a,l)=>a+(l.q||0)*(l.p||0),0);
  let f={id:'v'+Date.now().toString(36),num,sens:devis?'devis':'vente',canal,tiers:client,d,h:heureMiami(),lignes,montant,
           stock:$('v-stock').checked,manuel:true,par:USR||'(non renseigné)',t:new Date().toISOString()};
  if(pcVente) f.pc=true;
  if(doc) f.doc=doc;
  if(doc&&doc.port>0) f.port=doc.port;
  if(old){
    /* la facture garde son numéro, sa date d'émission, ses encaissements et son lien public */
    const D0=old.doc||null;
    if(doc&&D0){ doc.num=D0.num; doc.emis=D0.emis||doc.emis; if(D0.regs) doc.regs=D0.regs; if(D0.lien) doc.lien=D0.lien; if(D0.deDevis) doc.deDevis=D0.deDevis;
      /* une cote modifiée garde ce qu'on en a fait : ses envois et son rangement dans les archives */
      if(D0.type==='devis'){ if(D0.envoye) doc.envoye=D0.envoye; if(D0.archive) doc.archive=D0.archive; } }
    const avant={num:old.num,client:old.tiers||'',montant:old.montant,total:D0?D0.total:old.montant,n:(old.lignes||[]).length};
    Object.assign(old,{num,canal,tiers:client,d,lignes,montant,stock:$('v-stock').checked});
    if(pcVente) old.pc=true; else delete old.pc;
    if(doc) old.doc=doc; else delete old.doc;
    if(doc&&doc.port>0) old.port=doc.port; else delete old.port;
    (old.modifs=old.modifs||[]).push({t:new Date().toISOString(),u:USR||'(non renseigné)',av:avant});
    f=old;
    if(String(avant.num)!==String(num)) noteRang(num,d);
    ecrit(KFACT,FACT); ecrit(KMOD,MOD); ecrit(KVENT,VENT); ecrit(KCLI,CLI);
    JOU.push({t:new Date().toISOString(),u:USR||'(non renseigné)',act:'vente',
      lib:(old.sens==='devis'?'devis '+(doc?doc.num:num)+' modifié':'vente modifiée — '+num)+(client?' — '+client:'')+' — '+canal+(doc?' — '+(FMODES[doc.pmode]||doc.pmode):'')+(pcVente&&sortis?" — flacons sortis de l'inventaire Perfume City":''),
      ref:num,av:money2(avant.total),ap:money2(doc?doc.total:montant),n:det.length,impact:-Math.round(montant-(+avant.montant||0)),det});
  } else {
    FACT.push(f); noteRang(num,d);
    ecrit(KFACT,FACT); ecrit(KMOD,MOD); ecrit(KVENT,VENT); ecrit(KCLI,CLI);
    JOU.push({t:new Date().toISOString(),u:USR||'(non renseigné)',act:'vente',
      lib:(devis?'devis '+doc.num:(doc?'facture '+doc.num+' — ':'vente saisie à la main — ')+canal)+(client?' — '+client:'')+(devis?'':' — '+num)+(doc&&!devis?' — '+(FMODES[doc.pmode]||doc.pmode)+(doc.reste>0?', reste dû '+money2(doc.reste):', payée'):'')+(pcVente&&sortis?" — flacons sortis de l'inventaire Perfume City":''),
      n:det.length,impact:devis?0:-Math.round(montant),det});
  }
  /* la fusion (6 nov. 2026) : la cote réunie est enregistrée, les autres s'archivent avec la mention, le journal le dit */
  if(FUSION&&old&&FUSION.into===old.id&&devis){
    const arch=[];
    FUSION.autres.forEach(id=>{ const x=FACT.find(z=>z.id===id); if(!x||!x.doc) return; x.doc.archive=true; x.doc.fusion=doc.num; arch.push(x.doc.num); });
    if(arch.length){ ecrit(KFACT,FACT); JOU.push({t:new Date().toISOString(),u:USR||'(non renseigné)',act:'vente',lib:'cotes '+arch.join(', ')+' fusionnées dans '+doc.num+(client?' — '+client:''),n:0,impact:0,det:[]}); }
  }
  FUSION=null;
  ecrit(KJOU,JOU);
  const etaitModif=!!old; EDIT=null;
  construitV();
  CANAUX=[...new Set(V.map(x=>x.canal))].sort((a,b)=>a===NP?1:b===NP?-1:a.localeCompare(b));
  const gard=$('fc').value;
  $('fc').innerHTML='<option value="">Tous les canaux</option>'+CANAUX.map(c=>`<option value="${esc(c)}">${esc(nomAff(c))}</option>`).join('');
  $('fc').value=gard; $('fp').value='mois'; $('fj').hidden=true;
  $('vov').classList.remove('on');
  vus=80; dessine();
  const b=document.createElement('div'); b.className='info'; b.style.borderLeftColor='var(--good)';
  b.style.background='var(--good-soft)';
  b.innerHTML=devis&&etaitModif?`<b>Devis ${esc(doc.num)} modifié</b> — ${PANIER.length} parfum${PANIER.length>1?'s':''}, ${money2(doc.total)}${client?' pour '+esc(client):''}. Le stock ne bouge pas. `
    :devis?`<b>Devis ${esc(doc.num)} enregistré</b> — ${PANIER.length} parfum${PANIER.length>1?'s':''}, ${money2(doc.total)}${client?' pour '+esc(client):''}. Le stock ne bouge pas. `
    :etaitModif?`<b>${doc?'Facture '+esc(doc.num):'Vente '+esc(num)} modifiée</b> — ${PANIER.length} parfum${PANIER.length>1?'s':''}, ${money2(doc?doc.total:montant)} sur ${esc(canal)}. Le stock a été remis d'aplomb, le journal garde l'avant et l'après. `
    :`<b>${doc?'Facture '+esc(doc.num):'Vente '+esc(num)} enregistrée</b> — ${PANIER.length} parfum${PANIER.length>1?'s':''}, ${money2(doc?doc.total:montant)} sur ${esc(canal)}${sortis?(pcVente?`, ${nf(sortis)} flacon${sortis>1?'s':''} sorti${sortis>1?'s':''} de l'inventaire Perfume City (le stock central ne bouge pas)`:`, ${nf(sortis)} flacon${sortis>1?'s':''} sortis du stock`):', stock inchangé'}. `;
  if(doc){ const vb=document.createElement('button'); vb.className='btn sm'; vb.textContent='Voir le document'; vb.style.marginLeft='8px'; vb.onclick=()=>dessineDoc(f); b.appendChild(vb); }
  $('corps').parentNode.insertBefore(b,$('corps'));
  try{ peintDocs(); }catch(e){}
  setTimeout(()=>b.remove(),doc?20000:9000);
  if(doc) dessineDoc(f);
  /* cote modifiée : le formulaire repart à zéro, derrière le document — un second clic sur « Enregistrer » ne doit pas faire une cote de plus */
  if(etaitModif&&devis&&MODE_QUOTES){ try{ ouvreVente(); }catch(e){} }
};

$('fc').innerHTML='<option value="">Tous les canaux</option>'+CANAUX.map(c=>`<option value="${esc(c)}">${esc(nomAff(c))}</option>`).join('');
$('fc').addEventListener('input',()=>{ canalSel=$('fc').value; vus=80; dessine(); });
['q','fp'].forEach(i=>$(i).addEventListener('input',()=>{ vus=80; dessine(); }));
/* « Un jour précis… » : le calendrier s'ouvre, aujourd'hui par défaut */
$('fp').addEventListener('change',()=>{ const j=$('fp').value==='jour'; $('fj').hidden=!j;
  if(j){ if(!$('fj').value) $('fj').value=isoJour(new Date()); try{ $('fj').showPicker(); }catch(e){ $('fj').focus(); } }
  vus=80; dessine(); });
$('fj').addEventListener('change',()=>{ vus=80; dessine(); });

/* Ce qui sort, c'est ce qui est à l'écran : le même filtre, la même période, le
   même canal. Un export qui ne correspond pas à ce qu'on regarde est un export
   qu'on n'ose plus utiliser. Le filtre part avec le fichier, écrit en toutes
   lettres, pour qu'un papier retrouvé dans trois mois dise de quoi il parle. */
poseSortie('exp', ()=>{
  const L=filtre(true);
  const per=jourChoisi()?('le '+dfr(jourChoisi())):$('fp').options[$('fp').selectedIndex].textContent;
  const q=$('q').value.trim();
  return {
    titre:'Journal des ventes',
    fichier:'ventes',
    filtre:[per, canalSel?'canal '+canalCourt(canalSel):'tous les canaux', q?'recherche « '+q+' »':''].filter(Boolean).join(' · '),
    colonnes:[{t:'Date',y:'d'},{t:'Canal'},{t:'N° facture'},{t:'N° commande'},{t:'Client'},
      {t:'Code-barres'},{t:'Produit'},{t:'Quantité',y:'n'},{t:'Prix unitaire',y:'m'},
      {t:'Montant',y:'m'},{t:'Commission %',y:'p'},{t:'Encaissé net',y:'m'},
      ...(vmg()?[{t:'Prix d\'achat',y:'m'},{t:'Marge nette',y:'m'},{t:'Taux de marge',y:'p'}]:[]),{t:'Enregistré par'},{t:'État'}],
    lignes:L.map(x=>[x.d,x.canal,x.num,x.cmd,x.client,x.bc,x.ref,x.q,x.p,x.mt,
      x.com||0,x.net,...(vmg()?[x.pa,x.mg,x.pct]:[]),x.par,x.att==='exp'?'à expédier':x.att==='id'?'à identifier':x.att?'en attente':'facturée'])
  };
});


/* ================= UNE COMMANDE RECUE PAR MESSAGE =================
   Les clients de Sam commandent par WhatsApp ou par SMS, en toutes lettres :
   « 2 sauvage 100ml », « bleu de chanel 3.4 oz x3 ». Personne n'écrit un
   code-barres. Recopier ça à la main dans l'outil, c'est cinq minutes et deux
   erreurs par commande.

   Ce que fait ce bloc : il lit le message et retrouve les parfums du catalogue
   sur la marque, le nom et la contenance. Il PROPOSE — il ne décide pas. Ce dont
   il n'est pas sûr est marqué et attend une main humaine, comme la file d'attente.

   Le point qui décide si l'outil sera utilisé dans six mois : il RETIENT les
   corrections. La première fois qu'on lui dit que « sauvage 100 » c'est Dior
   Sauvage EDT 3.4 oz, c'est réglé pour toujours. Sans mémoire, on recorrige les
   mêmes trois parfums chaque semaine et on abandonne au bout d'un mois. */
__NOMS__
/* Une ligne du message → une ligne de commande, ou rien. */
let M_L=[];
function mLit(texte){
  const lignes=String(texte||'').split(/\r?\n/)
    .map(l=>l.replace(/^\s*(?:[-–—•*·]|\d+[.)])\s*/,'').trim())
    .filter(l=>l.length>=3);
  const out=[];
  lignes.forEach(l=>{
    /* les politesses et les questions ne sont pas des produits */
    if(/^(bonjour|bonsoir|salut|hello|hi|merci|thanks|thank you|ok|d'accord|bien re[cç]u)\b/i.test(l) && l.length<40) return;
    const r=mCherche(l);
    if(!r.mots.length) return;
    const best=r.cands[0], second=r.cands[1];
    /* on ne choisit tout seul que si c'est net : bon score, et nettement devant
       le suivant. Sinon on propose et on attend. */
    const sur = r.appris ? 'ok'
      : (best && best.sc>=0.72 && (!second || best.sc-second.sc>=0.13)) ? 'ok'
      : (best && best.sc>=0.45) ? 'hm' : 'no';
    /* code-barres de la liste inconnu de l'ERP : la référence se confirme à la main */
    const conf = !!r.bcInconnu && best;
    out.push({brut:l, q:(r.qte&&r.qte.q)||1, p:(r.px!=null?r.px:null), taille:r.taille, cands:r.cands,
              cle:(sur==='ok'&&best&&!conf)?best.cle:'', sur:conf?'bc':sur, appris:r.appris, bc:r.bcInconnu||''});
  });
  M_L=out;
  return out;
}

/* le prix d'une ligne lue : celui du FICHIER s'il y est (la cote du client), sinon celui de l'ERP pour le canal */
const mPrix=l=>l.p!=null?l.p:(l.cle?prixSuggere(l.cle,mCanal()):null);
const mPanierLigne=(l,q)=>Object.assign({cle:l.cle,q:q==null?l.q:q,p:l.p!=null?l.p:prixSuggere(l.cle,canalCour())},l.p!=null?{pf:true}:{});
function mPeint(){
  const el=$('m-res');
  if(!M_L.length){ el.innerHTML=''; $('m-rap').hidden=true;
    $('m-att').disabled=true; $('m-devis').disabled=true; return; }
  const LIB={ok:'trouvé',hm:'à confirmer',no:'pas trouvé',bc:'code-barres inconnu : confirme'};
  el.innerHTML=`<table class="mtb"><thead><tr>
    <th style="width:34%">Ce que le client a écrit</th><th>Le parfum</th>
    <th class="r">Qté</th><th class="r">Prix</th><th class="r"></th></tr></thead><tbody>
    ${M_L.map((l,i)=>{
      const v=l.cle?IDX[l.cle]:null;
      const px=l.cle?mPrix(l):null;
      return `<tr class="${l.sur==='hm'||l.sur==='bc'?'sur':l.sur==='no'?'non':''}">
      <td><span class="msur ${l.sur}">${LIB[l.sur]}</span>${l.appris?' <span class="msur ok">appris</span>':''}
        <span class="brut">${esc(l.brut)}</span></td>
      <td>${l.cands.length?`<select data-ml="${i}">
          <option value="">— choisir —</option>
          ${l.cands.map(c=>{ const w=IDX[c.cle]||[];
            return `<option value="${esc(c.cle)}"${c.cle===l.cle?' selected':''}>${esc(((w[2]||'')+' '+(w[1]||'')+tyTexte(c.cle)).trim())} · ${esc(w[3]||'?')} oz · stock ${nf(qteEff(c.cle))}</option>`; }).join('')}
        </select>`:'<span style="color:var(--crit)">aucun parfum approchant dans le catalogue</span>'}
        ${l.bc?`<span class="brut" style="color:var(--crit)">code-barres de la liste <b data-nolang>${esc(l.bc)}</b> : aucune fiche de l'ERP ne le porte — choisis le bon parfum</span>`:''}
        ${l.cle&&v?`<span class="brut">code-barres ${esc(v[0]||'—')}${l.taille?` · le client demande ${l.taille.ml} ml`:''}</span>`:''}</td>
      <td class="r"><input type="number" min="1" step="1" data-mq="${i}" value="${l.q}"></td>
      <td class="r">${l.cle?`<input type="number" min="0" step="0.01" data-mp="${i}" value="${px!=null?(+px).toFixed(2):''}" title="${esc(L3('Le prix pour ce client : tape-le ici','The price for this customer: type it here','El precio para este cliente: escríbelo aquí'))}" style="width:86px;text-align:right">${l.pm?`<span class="msur ok" style="margin-left:4px">${L3('modifié','changed','cambiado')}</span>`:''}`:'—'}</td>
      <td class="r"><button class="btn sm" data-msup="${i}" title="Retirer cette ligne">✕</button></td>
    </tr>`; }).join('')}</tbody></table>`;

  const pris=M_L.filter(l=>l.cle);
  const total=pris.reduce((a,l)=>a+(l.q*(mPrix(l)||0)),0);
  const flous=M_L.filter(l=>!l.cle).length;
  const manque=pris.filter(l=>l.q>qteEff(l.cle));
  const r=$('m-rap'); r.hidden=false;
  r.innerHTML=`<b>${nf(pris.length)} parfum${pris.length>1?'s':''} reconnu${pris.length>1?'s':''}</b>
    sur ${nf(M_L.length)} ligne${M_L.length>1?'s':''} lue${M_L.length>1?'s':''} · ${money2(total)} ${pris.some(l=>l.pm)?(pris.filter(l=>l.pm).length+' prix modifié'+(pris.filter(l=>l.pm).length>1?'s':'')+' à la main, le reste au prix du canal.'):pris.some(l=>l.p!=null)?(pris.every(l=>l.p!=null)?'aux prix de ta liste.':'(prix de ta liste quand elle en donne un, sinon prix du canal).'):'au prix du canal.'}
    ${flous?`<br><b style="color:var(--crit)">${nf(flous)} ligne${flous>1?'s':''} sans parfum choisi</b> — elle${flous>1?'s ne partiront':' ne partira'} pas.
      Choisis dans la liste, ou laisse : le client sera rappelé pour cette ligne.`:''}
    ${manque.length?`<br><b style="color:var(--warn)">${nf(manque.length)} ligne${manque.length>1?'s':''} dépasse${manque.length>1?'nt':''} le stock compté</b> :
      ${manque.slice(0,3).map(l=>esc(((IDX[l.cle]||[])[1]||''))+' — demandé '+l.q+', en stock '+nf(qteEff(l.cle))).join(' · ')}${manque.length>3?'…':''}.
      Ce n'est pas bloquant : ce n'est encore qu'une commande à valider.`:''}
    <br>Ce que tu corriges ici est <b>retenu</b> : la prochaine fois, la même phrase sera reconnue toute seule.`;

  el.querySelectorAll('[data-ml]').forEach(sl=>sl.onchange=()=>{
    const i=+sl.dataset.ml; M_L[i].cle=sl.value; M_L[i].sur=sl.value?'ok':(M_L[i].bc?'bc':'no'); mPeint(); });
  el.querySelectorAll('[data-mq]').forEach(ip=>ip.onchange=()=>{
    const i=+ip.dataset.mq; M_L[i].q=Math.max(1,parseInt(ip.value,10)||1); mPeint(); });
  /* Igal, 22 oct. 2026 : « Sam rentre le texte de Carmen, les produits s'affichent, mais il ne peut pas changer les prix ».
     Le prix tapé ici est celui de la cote : il est gardé tel quel (comme un prix donné par la liste du client). */
  el.querySelectorAll('[data-mp]').forEach(ip=>ip.onchange=()=>{
    const i=+ip.dataset.mp; const v=parseFloat(String(ip.value).replace(',','.'));
    if(isFinite(v)&&v>=0){ M_L[i].p=Math.round(v*100)/100; M_L[i].pm=true; }
    setTimeout(mPeint,0); });   /* le redessin attend la fin du « change » (sinon la case en cours de perte de focus disparaît sous le navigateur) */
  el.querySelectorAll('[data-msup]').forEach(b=>b.onclick=()=>{
    M_L.splice(+b.dataset.msup,1); mPeint(); });

  $('m-att').disabled = !pris.length;
  $('m-devis').disabled = !pris.length;
}

const mCanal=()=>CANAUX_VENTE().find(c=>c.nom===$('m-canal').value)||{id:'autre',nom:'Autre',com:0,maj:0};

/* On retient la phrase du client → la référence choisie. C'est ce qui fait que
   l'outil s'améliore au lieu de redemander la même chose chaque semaine. */
function mApprend(){
  const A=lit(K_ALIASN,{}); const M=(A&&typeof A==='object'&&!Array.isArray(A))?A:{};
  let n=0;
  M_L.forEach(l=>{ if(!l.cle) return; const k=mNorm(l.brut); if(!k) return;
    if(M[k]!==l.cle){ M[k]=l.cle; n++; } });
  if(n) ecrit(K_ALIASN,M);
  return n;
}

function mOuvre(){
  M_L=[]; $('m-txt').value=''; $('m-client').value=''; $('m-msg').textContent='';
  const CV=CANAUX_VENTE();
  $('m-canal').innerHTML=CV.map(c=>`<option value="${esc(c.nom)}">${esc(nomAff(c.nom))}</option>`).join('');
  const CLI=lit(KCLI,{});
  mPeint();
  $('msgov').classList.add('on'); setTimeout(()=>$('m-txt').focus(),60);
}
function mFerme(){ $('msgov').classList.remove('on'); }

$('m-x').onclick=$('m-ann').onclick=mFerme;
$('m-txt').addEventListener('input',()=>{ mLit($('m-txt').value); mPeint(); });
/* la liste du client en fichier : photo, PDF, tableur — lue ici, versee dans la
   zone de texte, puis reconnue ligne par ligne comme un message colle */
async function mFichier(f){
  if(!f) return;
  const L=$('m-lect'); L.hidden=false; L.className='mlect'; L.textContent='Lecture de '+f.name+'…';
  try{
    const t=await lireFichier(f, m=>{ L.textContent=m; });
    /* un tableau a colonnes (CSV, Excel) devient une ligne par article : les
       separateurs de colonnes deviennent des espaces, la ligne d'en-tete tombe */
    const lignes=String(t).split(/\r?\n/).map(l=>l.replace(/[\t;|]+/g,'  ').trim()).filter(Boolean);
    if(lignes.length>1 && /code|barre|sku|ean|upc|nom|name|qt|quant|prix|price|ref/i.test(lignes[0]) && !/\d{8,}/.test(lignes[0])) lignes.shift();
    $('m-txt').value=lignes.join('\n');
    mLit($('m-txt').value); mPeint();
    const n=M_L.length, pris=M_L.filter(l=>l.cle).length;
    L.textContent=`Lu : ${f.name} — ${n} ligne${n>1?'s':''}, ${pris} reconnue${pris>1?'s':''} tout de suite.`;
  }catch(e){ L.className='mlect err'; L.textContent=(e&&e.message)||'Lecture impossible.'; }
}
$('m-fichier').addEventListener('change',e=>{ mFichier(e.target.files[0]); e.target.value=''; });
['dragenter','dragover'].forEach(ev=>$('m-dz').addEventListener(ev,e=>{ e.preventDefault(); $('m-dz').classList.add('sur'); }));
['dragleave','drop'].forEach(ev=>$('m-dz').addEventListener(ev,e=>{ e.preventDefault(); $('m-dz').classList.remove('sur'); }));
$('m-dz').addEventListener('drop',e=>{ const f=e.dataTransfer.files[0]; if(f) mFichier(f); });
/* un fichier lache sur la zone de texte elle-meme est lu pareil */
$('m-txt').addEventListener('dragover',e=>e.preventDefault());
$('m-txt').addEventListener('drop',e=>{ if(e.dataTransfer.files&&e.dataTransfer.files[0]){ e.preventDefault(); mFichier(e.dataTransfer.files[0]); } });
$('m-canal').addEventListener('change',mPeint);

/* Vers la file d'attente : une commande à valider, qui ne touche à rien.
   C'est le même endroit que les commandes du site et de la caisse — un seul
   endroit où regarder ce qui attend, plutôt que trois. */
$('m-att').onclick=()=>{
  const pris=M_L.filter(l=>l.cle); if(!pris.length) return;
  const appris=mApprend();
  const F=litFile();
  const v={_i:'message|'+Date.now().toString(36)+Math.random().toString(36).slice(2,5),
    src:'message', num:'MSG-'+new Date().toISOString().slice(2,10).replace(/-/g,''),
    d:ajd(),
    lieu:$('m-canal').value, client:$('m-client').value.trim(),
    total:pris.reduce((a,l)=>a+l.q*(mPrix(l)||0),0), annule:false,
    lignes:pris.map(l=>{ const w=IDX[l.cle]||[];
      return {bc:w[0]||'', des:((w[2]||'')+' '+(w[1]||'')).trim(), q:l.q, p:mPrix(l)}; }),
    recu:new Date().toISOString(), texte:$('m-txt').value.slice(0,2000)};
  F.push(v); ecrit(KFILE,F);
  const J=lit(KJOU,[]); J.push({t:new Date().toISOString(),u:USR||'(non renseigné)',act:'vente',
    lib:'commande reçue par message'+($('m-client').value.trim()?' de '+$('m-client').value.trim():'')
      +' — '+pris.length+' ligne(s), mise en attente',ref:'',av:null,ap:Math.round(v.total)+' $'});
  ecrit(KJOU,J);
  mFerme(); peintFile();
  const b=document.createElement('div'); b.className='info';
  b.innerHTML=`<b>Commande mise en attente</b> — ${nf(pris.length)} parfum${pris.length>1?'s':''}, ${money2(v.total)}.
    Elle est dans la file d'attente en haut de cette page : rien n'a bougé dans le stock tant qu'elle n'est pas enregistrée.
    ${appris?`<br>${nf(appris)} façon${appris>1?'s':''} d'écrire retenue${appris>1?'s':''} : la prochaine fois, ce sera reconnu tout seul.`:''}`;
  const w=document.querySelector('.wrap')||document.body; w.insertBefore(b,w.firstChild);
  setTimeout(()=>b.remove(),10000);
  window.scrollTo({top:0,behavior:'smooth'});
};

/* Vers un devis : c'est la fenêtre de vente habituelle, déjà remplie. On ne
   refait pas un deuxième chemin pour émettre un document — un seul endroit
   où le devis se fabrique, c'est un seul endroit où le corriger. */
/* 20 oct. 2026 (Igal : « Create a New Quote doit être dans la rubrique Cote, pas dans Ventes où il y a Message client ») :
   une cote ne se fabrique plus depuis Ventes. Le bouton emmène dans la rubrique Cote avec le message déjà collé — c'est
   là que les parfums sont reconnus, les prix posés et la cote enregistrée. */
$('m-devis').onclick=()=>{
  const pris=M_L.filter(l=>l.cle); if(!pris.length) return;
  mApprend();
  try{ localStorage.setItem('cote-depuis-message',JSON.stringify({txt:$('m-txt').value,client:$('m-client').value.trim(),t:Date.now()})); }catch(e){}
  location.href='quotes.html';
};

/* « + Enregistrer une vente » monte à côté du titre : c'est la première chose qu'on
   veut faire en arrivant ici, pas la dernière à laquelle on arrive en scrollant.
   On DÉPLACE le bouton au lieu d'en poser un deuxième — deux boutons identiques sur
   un écran, c'est une hésitation de plus à chaque saisie. Il garde son identifiant,
   donc tout ce qui l'actionne ailleurs (l'écran vide, les raccourcis) marche encore.
   La recherche et les filtres, eux, restent collés au tableau : un filtre loin de
   son résultat, on le change et on croit qu'il ne s'est rien passé. */
(function boutonEnHaut(){
  const h=document.querySelector('header'), b=$('nv'), m=$('msgb'), s=$('src');
  if(!h||!b) return;
  const z=document.createElement('div'); z.className='hact';
  if(m) z.appendChild(m);
  z.appendChild(b);
  if(s) h.insertBefore(z,s); else h.appendChild(z);
})();
$('msgb').onclick=mOuvre;

/* ===== Contrôle des commandes du site (10 oct. 2026) =====
   Sam : « j'ai fait des ventes sur le site retail qui n'apparaissent pas sur l'ERP — on n'a pas le
   droit à l'erreur ». Le Patron / l'admin lit ici ce que le site a, ce que l'ERP connaît, et ajoute
   à la file ce qui manque. */
const CTR_ST={processing:['En cours (payée)','ok'],completed:['Terminée','ok'],'on-hold':['En pause (paiement à confirmer)','wa'],pending:['En attente de paiement','na'],
  cancelled:['Annulée','na'],failed:['Échouée','na'],refunded:['Remboursée','na'],draft:['Brouillon','na']};
const ctrPeut=()=>{ try{ const r=(typeof session==='function'?session():JSON.parse(localStorage.getItem('sam-session-v1')||'null')).role; return (r==='patron'||r==='admin')&&typeof CK_URL!=='undefined'&&typeof ckTok==='function'&&!!ckTok(); }catch(e){ return false; } };
const ctrQuel=()=>{ const r=document.querySelector('input[name=ctrq]:checked'); return r?r.value:''; };
let CTR=[];
/* 27 oct. 2026 (Igal : « pourquoi on n'a pas Perfume City, j'aimerais vérifier tout en même temps ») : le bouton
   « Vérifier les commandes du site » (deux sites WooCommerce, un à la fois) disparaît de la barre — « Tout revérifier »
   fait les trois canaux d'un coup, ventes et stock. La fenêtre reste dans le code (ctrov), plus de bouton pour l'ouvrir. */
(function(){ const m=()=>{ if(!ctrPeut()) return; const v=$('vcb'); if(v) v.style.display=''; };
  m(); window.addEventListener('load',()=>{ m(); setTimeout(m,1500); setTimeout(m,5000); }); })();

/* ===== La vérification complète (Igal, 22 oct. 2026) =====
   « Un bouton que Sam appuiera de temps en temps pour être sûr qu'il n'y a rien de loupé, et remettre l'ERP à jour,
   stock et ventes. » Le cockpit fait le tour des trois canaux et dépose ce qui manque dans la file ; cette page
   enregistre la file tout de suite (comme une vente qui arrive), puis demande au cockpit de remettre le stock des
   sites au niveau. Chaque canal rend son compte, lisible, canal par canal. */
const VC_NOM={detail:'perfumestrade.com',gros:'wholesale.perfumestrade.com',pc:'Perfume City'};
function vcCanal(k,c){
  const nom=VC_NOM[k]||k;
  if(!c) return '';
  if(c.absent) return `<div class="pl"><span data-nolang>${esc(nom)}</span><b class="hint">${L3('non relié','not connected','no conectado')}</b></div>`;
  if(c.err) return `<div class="pl"><span data-nolang>${esc(nom)}</span><b style="color:var(--crit)">${L3('panne','failure','fallo')} — ${esc(c.err)}</b></div>`;
  const aj=(c.ajoutees||[]).length, pe=(c.perdues||[]).length, pause=(c.enCours||c.enPause||[]).length;   /* 5 nov. 2026 : payées mais pas encore expédiées (processing, on-hold) */
  const nonP=+c.autres||0;
  let d=`<b>${nf(c.lues)}</b> ${L3('commandes lues','orders read','pedidos leídos')} : <b>${nf(c.connues+aj)}</b> ${L3('vente'+(c.connues+aj>1?'s':'')+' terminée'+(c.connues+aj>1?'s':'')+' (completed)','completed sale(s)','venta(s) terminada(s) (completed)')}`;
  d+=aj?` ${L3('dont','including','de las cuales')} <b style="color:var(--crit)">${nf(aj)} ${L3('qui manquai'+(aj>1?'ent':'t')+', ajoutée'+(aj>1?'s':''),'missing, now added','que faltaba(n), añadida(s)')}</b> (<span data-nolang>${esc(c.ajoutees.join(', '))}</span>)`:` ${L3('toutes dans l\'ERP','all in the ERP','todas en el ERP')} — <b style="color:var(--ok)">${L3('rien ne manque','nothing missing','no falta nada')}</b>`;
  if(nonP) d+=`, ${nf(nonP)} ${L3('non payée'+(nonP>1?'s':'')+' ou annulée'+(nonP>1?'s':'')+' (ne compte'+(nonP>1?'nt':'')+' pas)','unpaid or cancelled (not counted)','sin pagar o anulada(s) (no cuentan)')}`;
  if(pe) d+=` — ${L3('dont','including','de los cuales')} ${nf(pe)} ${L3('perdue'+(pe>1?'s':'')+' après dépôt','lost after deposit','perdido'+(pe>1?'s':'')+' tras el depósito')}`;
  if(pause) d+=` — ${nf(pause)} ${L3('en cours sur le site (payée'+(pause>1?'s':'')+', pas encore expédiée'+(pause>1?'s':'')+' : elle'+(pause>1?'s':'')+' entrera'+(pause>1?'ont':'')+' une fois « completed »)','in progress on the site (paid, not shipped yet: it enters once "completed")','en curso en el sitio (pagada, aún no enviada: entrará al pasar a «completed»)')}`;
  if((c.refus||[]).length) d+=` — <span style="color:var(--crit)">${esc(c.refus.join(' / '))}</span>`;
  return `<div class="pl" style="align-items:flex-start"><span data-nolang style="min-width:200px">${esc(nom)}</span><span>${d}</span></div>`;
}
function vcStock(r){
  if(!r) return '';
  if(r.err||r.verrou||r.eteint) return `<div class="pl"><span>${L3('Stock des sites','Sites stock','Stock de los sitios')}</span><b style="color:var(--crit)">${esc(r.err||'')}</b></div>`;
  if(r.attend) return `<div class="pl"><span>${L3('Stock des sites','Sites stock','Stock de los sitios')}</span><b class="hint">${L3('vérifié par le cockpit toutes les 5 minutes — pas relancé maintenant','checked by the cockpit every 5 minutes — not rerun now','verificado por el cockpit cada 5 minutos — no relanzado ahora')} (${esc(r.attend)})</b></div>`;
  const S=r.sites||{}; const un=(k,x)=>x?(x.err?`${k} : <span style="color:var(--crit)">${esc(x.err)}</span>`:`${k} : <b>${nf(x.ecrites||0)}</b> ${L3('fiche'+((x.ecrites||0)>1?'s':'')+' remise'+((x.ecrites||0)>1?'s':'')+' au niveau','product(s) brought in line','ficha(s) ajustada(s)')}`):'';
  return `<div class="pl" style="align-items:flex-start"><span style="min-width:200px">${L3('Stock des sites','Sites stock','Stock de los sitios')}</span><span>${[un('détail',S.detail),un('gros',S.gros)].filter(Boolean).join(' · ')||L3('rien à corriger','nothing to fix','nada que corregir')}</span></div>`;
}
/* le stock : si une égalisation automatique tourne déjà (toutes les 5 min), on attend qu'elle finisse et on relance, trois fois */
async function vcStockAttend(){
  let stock=null;
  for(let i=0;i<4;i++){
    if(i) await new Promise(x=>setTimeout(x,8000));
    try{ const r2=await fetch(CK_URL+'/api/o/'+CK_ORG+'/verification/stock',{method:'POST',headers:{'Content-Type':'application/json',Authorization:'Bearer '+ckTok()},body:'{}'}); stock=await r2.json().catch(()=>({err:'échec'})); }catch(e){ stock={err:(e&&e.message)||'échec'}; }
    if(!(stock&&stock.attend&&/en cours/.test(stock.attend))) break;
    $('vc-msg').textContent=L3('Le stock est déjà en cours de vérification, on attend…','Stock check already running, waiting…','El stock ya se está verificando, esperando…');
  }
  $('vc-msg').textContent='';
  return stock;
}
async function vcLance(){
  const b=$('vc-ok'); b.disabled=true; $('vc-msg').textContent='';
  $('vc-res').innerHTML=`<p class="hint">${L3('Lecture des trois canaux… (jusqu\'à une minute)','Reading the three channels… (up to a minute)','Leyendo los tres canales… (hasta un minuto)')}</p>`;
  try{
    const r=await fetch(CK_URL+'/api/o/'+CK_ORG+'/verification',{method:'POST',headers:{'Content-Type':'application/json',Authorization:'Bearer '+ckTok()},body:JSON.stringify({jours:14})});
    const j=await r.json().catch(()=>({}));
    if(!r.ok) throw new Error(j.erreur||('erreur '+r.status));
    let h=['detail','gros','pc'].map(k=>vcCanal(k,j.canaux[k])).join('');
    const aj=Object.values(j.canaux||{}).reduce((a,c)=>a+((c&&c.ajoutees)||[]).length,0);
    let stock=j.stock;
    if(aj){
      $('vc-res').innerHTML=h+`<p class="hint">${L3('Enregistrement des ventes ajoutées…','Recording the added sales…','Registrando las ventas añadidas…')}</p>`;
      /* la file est relue au serveur et enregistrée ici, comme une vente qui arrive */
      try{ if(typeof window.__syVeille==='function') await window.__syVeille(true); }catch(e){}
      try{ if(typeof window.__syTraiteFile==='function') await window.__syTraiteFile(); }catch(e){}
      await new Promise(x=>setTimeout(x,4000));   /* le tableau des quantités part 3 s après l'écriture du stock */
      stock=await vcStockAttend();
    } else if(stock&&stock.attend&&/en cours/.test(stock.attend)) stock=await vcStockAttend();
    h+=vcStock(stock);
    const reste=(lit('caisse-file-v1',[])||[]).length;
    if(reste) h+=`<p class="hint" style="color:var(--crit)">${nf(reste)} ${L3('vente'+(reste>1?'s':'')+' attend'+(reste>1?'ent':'')+' encore dans la file (référence à identifier) : voir « Ventes à compléter ».','sale(s) still waiting in the queue (reference to identify): see "Sales to complete".','venta(s) aún en la cola (referencia por identificar): ver «Ventas por completar».')}</p>`;
    $('vc-res').innerHTML=h;
    try{ if(typeof window.__rafraichir==='function') window.__rafraichir(); }catch(e){}
  }catch(e){ $('vc-res').innerHTML=`<p class="hint" style="color:var(--crit)">${esc((e&&e.message)||'échec')}</p>`; }
  b.disabled=false;
}
$('vcb').onclick=()=>{ $('vc-res').innerHTML=''; $('vcov').classList.add('on'); };
$('vc-x').onclick=$('vc-ann').onclick=()=>$('vcov').classList.remove('on');
$('vc-ok').onclick=vcLance;
async function ctrCharge(){
  $('ctr-res').innerHTML='<p class="hint">Lecture du site…</p>'; $('ctr-ok').disabled=true; $('ctr-msg').textContent='';
  try{
    const r=await fetch(CK_URL+'/api/o/'+CK_ORG+'/site/controle?quel='+encodeURIComponent(ctrQuel())+'&jours='+$('ctr-j').value,{headers:{Authorization:'Bearer '+ckTok()}});
    const j=await r.json().catch(()=>({}));
    if(!r.ok) throw new Error(j.erreur||('erreur '+r.status));
    CTR=j.manquantes||[];
    const ligne=x=>{ const e=CTR_ST[x.statut]||[x.statut,'na'];
      return `<tr>${x.__ck?`<td><input type="checkbox" data-ctr="${x.id}" ${x.statut==='on-hold'?'':'checked'}></td>`:'<td></td>'}
        <td data-nolang>#${esc(x.num)}</td><td data-nolang>${esc(x.date)}</td><td data-nolang>${esc(x.client)}</td>
        <td class="r">${x.total==null?'—':money(x.total)}</td><td data-nolang>${esc(x.paiement)}</td><td><span class="st ${e[1]}">${esc(vf(e[0]))}</span>${x.perdue?`<div class="hint" style="color:var(--crit)">${L3('déposée le','deposited on','depositada el')} <span data-nolang>${esc(x.perdue)}</span> ${L3('puis perdue dans l\'ERP','then lost in the ERP','y luego perdida en el ERP')}</div>`:''}</td></tr>`; };
    CTR.forEach(x=>{ x.__ck=1; });
    let h=`<div class="pstot"><b>${nf(j.lues)}</b> ${L3('commandes lues sur','orders read on','pedidos leídos en')} ${esc(j.site)} (${nf(j.jours)} ${L3('jours','days','días')}) — <b>${nf(j.connues)}</b> ${L3('connues de l\'ERP','known to the ERP','conocidos por el ERP')}.</div>`;
    if(!CTR.length) h+=`<div class="psvide" style="margin:10px 0">${L3('Aucune vente ne manque : toutes les commandes payées du site sont dans l\'ERP.','No sale is missing: every paid order on the site is in the ERP.','No falta ninguna venta: todos los pedidos pagados del sitio están en el ERP.')}</div>`;
    else h+=`<div class="pstot" style="color:var(--crit)"><b>${nf(CTR.length)}</b> ${L3('commande'+(CTR.length>1?'s':'')+' du site '+(CTR.length>1?'sont':'est')+' absente'+(CTR.length>1?'s':'')+' de l\'ERP','order(s) from the site missing in the ERP','pedido(s) del sitio ausentes del ERP')} :</div>
      <table class="pst"><thead><tr><th></th><th>N°</th><th>${L3('Date','Date','Fecha')}</th><th>${L3('Client','Customer','Cliente')}</th><th class="r">Total</th><th>${L3('Paiement','Payment','Pago')}</th><th>${L3('Statut sur le site','Status on the site','Estado en el sitio')}</th></tr></thead><tbody>${CTR.map(ligne).join('')}</tbody></table>
      <p class="hint">${L3('« En pause » = le site attend la confirmation du paiement : décoché par défaut, coche-la si la vente est bien payée.','"On hold" = the site waits for payment confirmation: unticked by default, tick it if the sale is really paid.','«En pausa» = el sitio espera la confirmación del pago: sin marcar por defecto, márcalo si la venta está pagada.')}</p>`;
    const A=j.autres||[];
    if(A.length) h+=`<details style="margin-top:12px"><summary class="hint" style="cursor:pointer">${nf(A.length)} ${L3('autre'+(A.length>1?'s':'')+' commande'+(A.length>1?'s':'')+' non payée'+(A.length>1?'s':'')+' ou annulée'+(A.length>1?'s':'')+' (ne comptent pas comme des ventes)','other order(s) unpaid or cancelled (not counted as sales)','otros pedidos sin pagar o cancelados (no cuentan como ventas)')}</summary>
      <table class="pst"><tbody>${A.map(x=>ligne(Object.assign({},x,{__ck:0}))).join('')}</tbody></table></details>`;
    $('ctr-res').innerHTML=h; $('ctr-ok').disabled=!CTR.length; ctrMaj();
  }catch(e){ $('ctr-res').innerHTML=`<p class="hint" style="color:var(--crit)">${esc((e&&e.message)||'échec')}</p>`; }
}
function ctrMaj(){ const n=document.querySelectorAll('#ctr-res input[data-ctr]:checked').length; $('ctr-ok').disabled=!n;
  $('ctr-ok').textContent=n?L3('Ajouter '+n+' commande'+(n>1?'s':'')+' à la file','Add '+n+' order'+(n>1?'s':'')+' to the queue','Añadir '+n+' pedido'+(n>1?'s':'')+' a la cola'):L3('Ajouter les commandes cochées','Add the ticked orders','Añadir los pedidos marcados'); }
$('ctrb').onclick=()=>{ $('ctrov').classList.add('on'); ctrCharge(); };
$('ctr-x').onclick=$('ctr-ann').onclick=()=>$('ctrov').classList.remove('on');
$('ctr-j').onchange=ctrCharge;
document.querySelectorAll('input[name=ctrq]').forEach(r=>r.onchange=ctrCharge);
$('ctr-res').addEventListener('change',e=>{ if(e.target.matches('input[data-ctr]')) ctrMaj(); });

/* Les parfums des commandes ajoutées après un contrôle (leur stock a été retiré d'un coup, parfois
   des jours après la vente : si quelqu'un avait corrigé la quantité à la main entre-temps, elle est
   retirée deux fois). On les sort en Excel, par parfum, pour ne recompter que ceux-là. */
$('ctr-xl').onclick=()=>{
  const F=lit('factures-v1',[])||[]; const J=lit('crm-journal-v1',[])||[];
  /* les commandes ajoutées après contrôle : notées au journal avec leurs numéros */
  const nums=new Set(); J.forEach(j=>{ if(j&&/ajoutée\(s\) après contrôle/.test(j.lib||'')){ const m=/\(([^)]*)\)\s*$/.exec(j.lib); if(m) m[1].split(',').forEach(n=>nums.add(n.trim())); } });
  const P={}; let nV=0;
  F.forEach(f=>{ if(!f||f.sens!=='vente'||f.retour||!f.auto||!nums.has(String(f.num))) return; nV++;
    (f.lignes||[]).forEach(l=>{ const k=l.cle||l.bc||l.ref; const o=P[k]=P[k]||{ref:l.ref||'',bc:l.bc||'',q:0,cmd:new Set(),dates:[]};
      o.q+=+l.q||0; o.cmd.add(f.num); o.dates.push(f.d||''); }); });
  const L=Object.values(P).sort((a,b)=>b.q-a.q).map(o=>[o.ref,o.bc,o.q,[...o.cmd].join(', '),o.dates.sort()[0],o.dates.sort().slice(-1)[0]]);
  if(!L.length){ $('ctr-msg').textContent=L3('Aucune commande ajoutée après contrôle dans cet ERP.','No order added after a check in this ERP.','Ningún pedido añadido tras control en este ERP.'); $('ctr-msg').className='msg'; return; }
  sortieXlsx({titre:'Parfums des commandes du site ajoutées après contrôle',filtre:nV+' commande(s)',fichier:'parfums-a-verifier',
    colonnes:[{t:'Parfum'},{t:'Code-barres'},{t:'Flacons retirés du stock',y:'n'},{t:'Commandes'},{t:'Première vente',y:'d'},{t:'Dernière vente',y:'d'}],lignes:L});
};
$('ctr-ok').onclick=async()=>{
  const ids=[...document.querySelectorAll('#ctr-res input[data-ctr]:checked')].map(i=>+i.dataset.ctr); if(!ids.length) return;
  $('ctr-ok').disabled=true; $('ctr-msg').textContent=L3('Ajout…','Adding…','Añadiendo…'); $('ctr-msg').className='msg';
  try{
    const r=await fetch(CK_URL+'/api/o/'+CK_ORG+'/site/controle/ajoute',{method:'POST',headers:{'Content-Type':'application/json',Authorization:'Bearer '+ckTok()},body:JSON.stringify({quel:ctrQuel(),ids})});
    const j=await r.json().catch(()=>({}));
    if(!r.ok) throw new Error(j.erreur||('erreur '+r.status));
    $('ctr-msg').textContent=j.faites.length+' '+L3('ajoutée(s) à la file','added to the queue','añadido(s) a la cola')+((j.refus&&j.refus.length)?' — '+j.refus.length+' '+L3('refusée(s) : ','refused: ','rechazado(s): ')+j.refus.map(x=>'#'+x.id+' '+x.pourquoi).join(', '):'')+'.';
    $('ctr-msg').className='msg ok';
    try{ const J=lit('crm-journal-v1',[]); J.push({t:new Date().toISOString(),u:NOM_UTIL||'(non renseigné)',act:'vente',lib:j.faites.length+' commande(s) du site ajoutée(s) après contrôle ('+j.faites.map(x=>x.num).join(', ')+')',n:j.faites.length,impact:0,det:[]}); ecrit('crm-journal-v1',J); }catch(e){}
    await ctrCharge();
  }catch(e){ $('ctr-msg').textContent=(e&&e.message)||'échec'; $('ctr-msg').className='msg err'; $('ctr-ok').disabled=false; }
};

/* La liste du client (photo d'un Excel, PDF, fichier) depuis « Enregistrer une vente »
   (Sam, 1er oct. 2026 : « envoyer la photo d'un Excel et qu'il me la transforme en commande sans
   avoir besoin de la retaper »). C'est la même lecture que « Message client » ; les parfums
   reconnus rejoignent la vente en cours, ce qui a été ajouté à la main reste. */
let M_VENTE=false;
if('__MODE__'!=='quotes'){   /* MODE_QUOTES n'est défini que plus bas */
  const bl=document.createElement('button'); bl.type='button'; bl.className='btn'; bl.id='v-liste';
  bl.textContent='Importer une liste (photo, Excel, PDF)';
  $('vov').querySelector('.mh h3').after(bl);
  bl.onclick=()=>{ const cl=$('v-client').value.trim(), cn=$('v-canal').value;
    M_VENTE=true; $('vov').classList.remove('on'); mOuvre(); $('m-client').value=cl;
    try{ if([...$('m-canal').options].some(o=>o.value===cn)) $('m-canal').value=cn; }catch(e){}
    $('m-devis').textContent='Mettre ces parfums dans la vente →'; $('m-devis').classList.add('pri'); $('m-att').hidden=true; mPeint(); };
  const _mf=mFerme;
  mFerme=function(){ _mf(); if(M_VENTE){ M_VENTE=false; $('vov').classList.add('on');
    $('m-devis').textContent='Faire un devis'; $('m-devis').classList.remove('pri'); $('m-att').hidden=false; } };
  $('m-x').onclick=$('m-ann').onclick=()=>mFerme();
  const _md=$('m-devis').onclick;
  $('m-devis').onclick=e=>{
    if(!M_VENTE) return _md(e);
    const pris=M_L.filter(l=>l.cle); if(!pris.length) return;
    mApprend();
    const client=$('m-client').value.trim();
    mFerme();
    if(client&&!$('v-client').value.trim()) $('v-client').value=client;
    pris.forEach(l=>{ const x=PANIER.find(z=>z.cle===l.cle); if(x){ x.q+=l.q; if(l.p!=null){ x.p=l.p; x.pf=true; } } else PANIER.push(mPanierLigne(l)); });
    peintPanier();
    $('v-msg').textContent='Rempli depuis la liste du client — vérifie les quantités et les prix avant d\'enregistrer.';
  };
}

function majUser(){ try{ piedSession(); }catch(e){} }
majUser();
/* ---- la rubrique Quotes ----
   La meme page que Ventes, reduite a un seul chemin : le client, sa liste (collee
   ou deposee), les lignes reconnues, puis le devis avec ses prix — et l'envoi. Rien
   n'est reecrit : une seule mecanique de devis dans l'outil, celle-ci. */
const MODE_QUOTES=('__MODE__'==='quotes');
/* ================= LES DEVIS DE LIGHTSPEED =================
   Igal, 29 sept. 2026 (après avoir ouvert Lightspeed avec moi) : « sur la Cote de l'ERP,
   que apparaissent toutes les lignes mises en devis sur Lightspeed, avec la même possibilité
   de les convertir en vente — donc de déstocker —, de les envoyer, ou de les archiver ».
   Les devis arrivent par le favori « Devis → ERP » cliqué sur la page Devis de Lightspeed
   (le cockpit les range dans lightspeed-devis-v1). La liste est celle de Lightspeed : état
   (Créés / Convertis / Archivés), client, n° ; le détail se déplie ; mêmes boutons.
   « Convertir en vente » : la fiche (client, date, payé Zelle, chaque parfum reconnu ou à
   choisir) → facture, stock sorti, et le devis passe « Converti ». Seuls les devis créés à
   partir de REG.devisDepuis se convertissent : avant, le stock de départ (Google Sheet) en
   tient déjà compte — Igal veut ceux du 29 et du 30 sept. pour essayer. */
const KDEV='lightspeed-devis-v1';
let LSQ_F={etat:'cree',cli:'',num:''}, LSQ_OUV='', LSQ_CONV='', COTE_VOULUE=false;
/* 30 sept. (Igal) : « je veux que ce soit effectif qu'à partir du 1er octobre » — les devis
   d'avant cette date ne s'affichent pas du tout (le stock de départ en tient compte) */
/* 30 sept. (Igal) : « mets-moi les cotes d'hier et d'aujourd'hui, qu'on effacera à minuit heure
   de Miami » — un essai daté : tant que le jour de Miami est avant REG.devisEssaiFin, la date de
   départ réglée (devisDepuis) vaut ; à partir de ce jour-là, c'est devisEssaiFin, tout seul,
   sans que personne n'ait à y penser à minuit. */
const lsqDepuis=()=>{ const r=String((REG&&REG.devisDepuis)||'2026-10-01'), fin=String((REG&&REG.devisEssaiFin)||'');
  const auj=(typeof jourMiami==='function')?jourMiami():new Date().toISOString().slice(0,10);
  return (fin&&auj>=fin&&r<fin)?fin:r; };
const lsqTous=()=>{ const L=lit(KDEV,[]); return Array.isArray(L)?L:[]; };
const lsqEtat=x=>(x.erp&&x.erp.etat==='vendue')?'converti':(x.erp&&x.erp.archive)?'archive':x.statut==='CONVERTED'?'converti':x.statut==='ARCHIVED'?'archive':'cree';
const LSQ_LIB={cree:'Créé',converti:'Converti',archive:'Archivé'};
/* 1er oct. 2026 — Sam convertit ses devis dans l'ERP seulement (« retirer la vente seulement sur
   l'ERP »). Le devis reste ouvert dans Lightspeed : s'il y était converti aussi, la vente
   reviendrait par la caisse et le stock sortirait deux fois. Tant que Lightspeed ne l'a pas
   archivé, on le signale. */
const lsqAArchiver=x=>!!(x&&x.erp&&x.erp.etat==='vendue'&&x.statut!=='ARCHIVED'&&x.statut!=='CONVERTED');
function lsqLignes(x){
  const C=(typeof faContexte==='function')?faContexte():null;
  return (x.lignes||[]).map((l,j)=>{ const choix=(x.erp&&x.erp.choix&&x.erp.choix[j])||null;
    const cle=choix||(C&&l.bc?C.cleDe({bc:l.bc,des:l.des}):null)||null;
    /* 3 nov. 2026 (Sam : « il faut qu'on puisse rajouter les card charge ») : une ligne de la caisse qui n'est pas un parfum
       (card charge, sac, port…) n'est plus « à identifier » : c'est un frais. Le card charge devient les « Frais carte » de la
       facture, payée par carte ; les autres frais sont mis de côté comme pour une vente de caisse. */
    const service=!cle&&typeof faEstService==='function'&&faEstService({bc:l.bc,des:l.des});
    const carte=service&&/card\s*charge|cc\s*fee|frais\s*(?:de\s*)?carte|credit\s*card/i.test(String(l.des||''));
    return {j,cle,bc:l.bc||'',des:l.des||'',q:+l.q||0,p:l.p==null?null:+l.p,remise:+l.remise||0,service:!!service,carte:!!carte}; });
}
const lsqFraisCarte=LG=>Math.round(LG.filter(l=>l.carte).reduce((a,l)=>a+(+l.q||0)*(+l.p||0),0)*100)/100;
function lsqMaj(id,fn){ const L=lsqTous(); const x=L.find(z=>z&&z.id===id); if(!x) return null; fn(x); ecrit(KDEV,L); return x; }
function lscPeint(){
  const el=$('lsc'); if(!el) return;
  const T=lsqTous().filter(x=>x&&!x.supprime&&!(x.erp&&x.erp.supprime)&&String(x.d||'')>=lsqDepuis());
  const n={cree:0,converti:0,archive:0}; T.forEach(x=>n[lsqEtat(x)]++);
  const V=T.filter(x=>{ const e=lsqEtat(x);
    if(LSQ_F.etat&&e!==LSQ_F.etat) return false;
    if(LSQ_F.cli&&!cNorm(x.client||'').includes(cNorm(LSQ_F.cli))) return false;
    if(LSQ_F.num&&!String(x.num||'').includes(LSQ_F.num.trim())) return false; return true; });
  /* la date du dernier passage du favori (magasin tenu par le cockpit) ; à défaut, la réception du devis le plus récent */
  const lect=lit('lightspeed-lecture-v1',null);
  const maj=(lect&&lect.t)||T.reduce((a,x)=>String(x.recu||'')>a?String(x.recu||''):a,'');
  const ageH=maj?Math.max(0,(Date.now()-Date.parse(maj))/36e5):0;
  const vieux=(maj&&ageH>=20)?(ageH>=48?r3(`${Math.floor(ageH/24)} jours`,`${Math.floor(ageH/24)} days`,`${Math.floor(ageH/24)} días`):r3(`${Math.round(ageH)} heures`,`${Math.round(ageH)} hours`,`${Math.round(ageH)} horas`)):'';
  el.innerHTML=`<div class="lsc-t"><h2 class="lsc-h">Les devis de Lightspeed</h2>
      <p>Les ventes mises en cote sur la caisse Lightspeed (payées par Zelle). Rien ne sort du stock tant qu'elles ne sont pas converties en vente ici.</p>
      <div class="lsc-maj"><span>${T.length?`<span data-nolang>${nf(T.length)} ${r3('cotes depuis le','quotes since','cotizaciones desde el')} ${dfr(lsqDepuis())} · ${r3('mis à jour le','updated on','actualizadas el')} <b>${esc(quandMiami(maj))}</b></span>`:`<span data-nolang>${r3('Aucune cote Lightspeed depuis le','No Lightspeed quote since','Ninguna cotización de Lightspeed desde el')} ${dfr(lsqDepuis())}.</span>`}</span>
        <button class="btn" id="lsq-fav">Recevoir les cotes automatiquement</button></div>
      ${vieux?`<div class="note" data-nolang style="border-color:var(--crit);margin-top:10px">${r3(`<b>Lightspeed n'a pas été lu depuis ${vieux}.</b> Les cotes faites depuis dans la caisse ne sont pas encore ici. Cette liste se lit sans Lightspeed ; seule sa mise à jour en a besoin.`,`<b>Lightspeed has not been read for ${vieux}.</b> Quotes made at the register since then are not here yet. This list can be read without Lightspeed; only updating it needs it.`,`<b>Lightspeed no se lee desde hace ${vieux}.</b> Las cotizaciones hechas en la caja desde entonces aún no están aquí. Esta lista se lee sin Lightspeed; solo actualizarla lo necesita.`)}</div>`:''}
      <div id="lsq-aide" hidden></div></div>
    <div class="qf"><div class="fld"><label>État</label><select id="lsq-etat"><option value="cree">Créés (${nf(n.cree)})</option><option value="converti">Convertis (${nf(n.converti)})</option><option value="archive">Archivés (${nf(n.archive)})</option><option value="">Tous</option></select></div>
      <div class="fld"><label>Client</label><input id="lsq-cli" placeholder="Chercher un client" value="${esc(LSQ_F.cli)}"></div>
      <div class="fld"><label>Devis</label><input id="lsq-num" placeholder="N° de devis" value="${esc(LSQ_F.num)}"></div></div>`
    +(!V.length?`<p class="ecr">${T.length?'Aucun devis dans cette catégorie.':''}</p>`
    :`<table class="ql lsc-l"><thead><tr><th></th><th>Devis</th><th>Client</th><th>Créé par</th><th>Note</th><th class="r">Total du devis</th><th>État</th></tr></thead><tbody>
      ${V.slice(0,120).map(x=>{ const e=lsqEtat(x), on=LSQ_OUV===x.id;
        const ligne=`<tr class="qr ${on?'on':''}" data-q="${esc(x.id)}"><td class="chev">${on?'⌄':'›'}</td>
          <td class="num" data-nolang><b>${esc(x.num)}</b><small>${dfr(x.d)}${x.h?', '+esc(x.h):''}</small></td>
          <td><b>${esc(x.client||'—')}</b>${x.email?`<small class="lsc-p">${esc(x.email)}</small>`:''}</td>
          <td>${esc(x.par||'—')}</td><td>${esc(x.note||'')}</td>
          <td class="r"><b>${x.total!=null?money2(x.total):'—'}</b></td>
          <td><span class="et ${e==='cree'?'devis':e}">${LSQ_LIB[e]}</span>${x.erp&&(x.erp.etat==='vendue'||x.erp.archive)?'<small class="lsc-p">dans l\'ERP</small>':''}${lsqAArchiver(x)?`<small class="lsc-p" data-nolang style="color:var(--crit);font-weight:700">${L3('à archiver dans Lightspeed','to archive in Lightspeed','por archivar en Lightspeed')}</small>`:''}</td></tr>`;
        return on?ligne+`<tr class="qd"><td colspan="7">${LSQ_CONV===x.id?lsqFiche(x):lsqDetail(x)}</td></tr>`:ligne; }).join('')}
      </tbody></table>${V.length>120?`<p class="ecr">et ${nf(V.length-120)} de plus — affine avec le client ou le n°.</p>`:''}`);
  $('lsq-etat').value=LSQ_F.etat;
  $('lsq-etat').onchange=()=>{ LSQ_F.etat=$('lsq-etat').value; LSQ_OUV=''; LSQ_CONV=''; lscPeint(); };
  $('lsq-cli').oninput=()=>{ LSQ_F.cli=$('lsq-cli').value; lscPeint(); const i=$('lsq-cli'); i.focus(); i.setSelectionRange(i.value.length,i.value.length); };
  $('lsq-num').oninput=()=>{ LSQ_F.num=$('lsq-num').value; lscPeint(); const i=$('lsq-num'); i.focus(); i.setSelectionRange(i.value.length,i.value.length); };
  $('lsq-fav').onclick=lsqAide;
  el.querySelectorAll('tr.qr').forEach(tr=>tr.onclick=()=>{ LSQ_OUV=LSQ_OUV===tr.dataset.q?'':tr.dataset.q; LSQ_CONV=''; lscPeint(); });
  el.querySelectorAll('[data-la]').forEach(b=>b.onclick=ev=>{ ev.stopPropagation(); lsqAction(b.dataset.la,b.dataset.q); });
  const f=el.querySelector('.lsc-f'); if(f) lscBranche(f);
}
function lsqDetail(x){
  const LG=lsqLignes(x), e=lsqEtat(x), avant=String(x.d||'')<lsqDepuis();
  return `<div class="qdet"><div>
      ${LG.map(l=>`<div class="lg"><span>${nf(l.q)}</span><span><b>${esc(l.cle?fNomComplet(l.cle):(l.des||l.bc||'?'))}</b><br><small>${esc(l.bc||'')}${l.cle?'':' — pas reconnu dans le catalogue'}</small></span><span>@ ${l.p!=null?money2(l.p):'—'}${l.remise?`<br><small>remise ${money2(l.remise)}</small>`:''}</span><span class="r"><b>${money2((l.q||0)*(l.p||0))}</b></span></div>`).join('')}
      <div class="tot"><span>Sous-total</span><span class="r">${money2(x.sousTotal||0)}</span>
        <span>Sales tax</span><span class="r">${money2(x.taxe||0)}</span>
        <span class="tt">TOTAL</span><span class="r tt">${money2(x.total||0)}</span></div>
      ${x.note?`<div class="note"><b>Note</b> — ${esc(x.note)}</div>`:''}
      ${x.erp&&x.erp.etat==='vendue'?`<div class="note"><b>Converti en vente dans l'ERP</b> le ${dfr(x.erp.d||'')} par ${esc(x.erp.par||'')} — payé Zelle, stock sorti.</div>`:''}
      ${lsqAArchiver(x)?`<div class="note" data-nolang style="border-color:var(--crit)">${L3("<b>Dans Lightspeed : ARCHIVE ce devis, ne le convertis pas.</b> La vente est déjà faite ici ; convertie aussi dans Lightspeed, elle reviendrait par la caisse et le stock sortirait deux fois.","<b>In Lightspeed: ARCHIVE this quote, do not convert it.</b> The sale is already made here; converted in Lightspeed too, it would come back through the register and stock would go out twice.","<b>En Lightspeed: ARCHIVA este presupuesto, no lo conviertas.</b> La venta ya está hecha aquí; convertida también en Lightspeed, volvería por la caja y el stock saldría dos veces.")}</div>`:''}
      ${x.statut==='CONVERTED'&&x.erp&&x.erp.etat==='vendue'?`<div class="note" data-nolang style="border-color:var(--crit);color:var(--crit)">${L3("<b>Attention : converti ici ET dans Lightspeed.</b> La vente risque d'être comptée deux fois. Regarde dans Ventes si elle apparaît deux fois, et rembourse le doublon.","<b>Warning: converted here AND in Lightspeed.</b> The sale may be counted twice. Check Sales for a duplicate and refund it.","<b>Atención: convertido aquí Y en Lightspeed.</b> La venta puede contarse dos veces. Revisa en Ventas si aparece dos veces y reembolsa el duplicado.")}</div>`:''}
      ${x.statut==='CONVERTED'&&!(x.erp&&x.erp.etat==='vendue')?`<div class="note"><b>Converti dans Lightspeed</b> — la vente arrive dans Ventes par la caisse.</div>`:''}
      ${e==='cree'&&avant?`<div class="note"><b>Devis d'avant le ${dfr(lsqDepuis())}</b> — le stock de départ en tient déjà compte : il ne se convertit pas ici.</div>`:''}
    </div><div class="btns">
      ${e==='cree'&&!avant?`<button class="btn pri" data-la="conv" data-q="${esc(x.id)}">Convertir en vente</button>`:''}
      <button class="btn" data-la="mail" data-q="${esc(x.id)}">Envoyer le devis par e-mail</button>
      <button class="btn" data-la="print" data-q="${esc(x.id)}">Imprimer le devis</button>
      ${x.erp&&x.erp.archive?`<button class="btn" data-la="desarch" data-q="${esc(x.id)}">Désarchiver</button>`:(e==='cree'?`<button class="btn" data-la="arch" data-q="${esc(x.id)}">Archiver</button>`:'')}
      ${!(x.erp&&x.erp.etat==='vendue')?`<button class="btn lsq-sup" data-la="sup" data-q="${esc(x.id)}">Supprimer</button>`:''}
    </div></div>`;
}
/* le devis Lightspeed en document de l'ERP (pour l'e-mail et l'impression), fait une fois */
function lsqDoc(x){
  let F=lit('factures-v1',[]); if(!Array.isArray(F)) F=[];
  let f=F.find(z=>z&&z.lsq===x.id);
  if(!f){ const LG=lsqLignes(x);
    f={id:'lsq'+x.id,num:'LS-'+x.num,sens:'devis',lsq:x.id,canal:'Caisse Lightspeed',tiers:x.client||'',d:x.d,h:x.h,par:x.par||'',t:new Date().toISOString(),
       lignes:LG.map(l=>({cle:l.cle,bc:l.bc,ref:l.cle?fNomComplet(l.cle):(l.des||l.bc),q:l.q,p:l.p})),montant:x.sousTotal||0};
    const D=docAutoPour(Object.assign({},f,{taxe:x.taxe}),F);
    Object.assign(D,{type:'devis',num:'LS-'+x.num,pmode:'zelle',pstat:'attente',regle:0,reste:D.total,note:'Devis Lightspeed n° '+x.num});
    f.doc=D; F.push(f); ecrit('factures-v1',F); }
  FACT=lit('factures-v1',[]); return FACT.find(z=>z.id===f.id)||f;
}
function lsqAction(a,id){
  const x=lsqTous().find(z=>z.id===id); if(!x) return;
  if(a==='conv'){ LSQ_CONV=id; LSQ_OUV=id; lscPeint(); return; }
  /* Supprimer (Sam, 1er oct. 2026 : « donner la possibilité de supprimer, avec une seconde
     validation »). Deux questions, la seconde dit ce qui se passe vraiment. Le devis n'est pas
     effacé du cockpit : il est marqué « supprimé par l'ERP », sinon le favori le ramènerait à
     la relève suivante. Un devis déjà converti en vente ne se supprime pas : il a sa vente. */
  if(a==='sup'){
    if(x.erp&&x.erp.etat==='vendue') return;
    const qui=(x.client?x.client+' — ':'')+money2(x.total||0);
    if(!confirm(vf(L3(`Supprimer la cote ${x.num} (${qui}) ?`,`Delete quote ${x.num} (${qui})?`,`¿Eliminar la cotización ${x.num} (${qui})?`)))) return;
    if(!confirm(vf(L3(`Seconde validation : la cote ${x.num} disparaît de l'ERP pour de bon. Elle reste dans Lightspeed : archive-la aussi là-bas.\n\nSupprimer ?`,
      `Second confirmation: quote ${x.num} disappears from the ERP for good. It stays in Lightspeed: archive it there too.\n\nDelete?`,
      `Segunda confirmación: la cotización ${x.num} desaparece del ERP para siempre. Sigue en Lightspeed: archívala también allí.\n\n¿Eliminar?`)))) return;
    lsqMaj(id,z=>{ z.erp=Object.assign({},z.erp||{}); z.erp.supprime=true; z.erp.supPar=USR||''; z.erp.supT=new Date().toISOString(); });
    try{ const J=lit(KJOU,[]); J.push({t:new Date().toISOString(),u:USR||'(non renseigné)',act:'vente',lib:'devis Lightspeed '+x.num+' supprimé'+(x.client?' — '+x.client:'')+' ('+money2(x.total||0)+')',n:0,impact:0,det:[]}); ecrit(KJOU,J); }catch(e){}
    LSQ_OUV=''; lscPeint(); return; }
  if(a==='arch'||a==='desarch'){ lsqMaj(id,z=>{ z.erp=Object.assign({},z.erp||{}); if(a==='arch'){ z.erp.archive=true; z.erp.archPar=USR||''; z.erp.archT=new Date().toISOString(); } else delete z.erp.archive; });
    try{ const J=lit(KJOU,[]); J.push({t:new Date().toISOString(),u:USR||'(non renseigné)',act:'vente',lib:'devis Lightspeed '+x.num+(a==='arch'?' archivé':' désarchivé')+(x.client?' — '+x.client:''),n:0,impact:0,det:[]}); ecrit(KJOU,J); }catch(e){}
    LSQ_OUV=''; lscPeint(); return; }
  const f=lsqDoc(x); dessineDoc(f);
  try{ $('doc-conv').hidden=true; }catch(e){}          /* on convertit par « Convertir en vente », qui suit le devis */
  if(a==='mail') setTimeout(()=>$('doc-mail').click(),150);
  else if(a==='print') setTimeout(()=>$('doc-print').click(),150);
}
function lsqFiche(x){
  const LG=lsqLignes(x), inc=LG.filter(l=>!l.cle&&!l.service).length, fc=lsqFraisCarte(LG);
  const auj=(typeof jourMiami==='function'?jourMiami():new Date().toISOString().slice(0,10));
  const pay=(x.erp&&x.erp.pay)||(fc>0?'carte':'zelle');
  return `<div class="lsc-f" data-c="${esc(x.id)}"><h4>Convertir en vente — devis ${esc(x.num||'')}</h4>
    <div class="lsc-g"><label>Client<input class="sel" id="lsc-cli" value="${esc(x.client||'')}" placeholder="Nom du client"></label>
      <label>Date de la vente<input class="sel" type="date" id="lsc-d" value="${esc(auj)}"></label>
      <label>Paiement<select class="sel" id="lsc-pay"><option value="zelle" ${pay==='zelle'?'selected':''}>Zelle</option><option value="carte" ${pay==='carte'?'selected':''}>Carte bancaire</option></select></label></div>
    <table class="lsc-lg"><thead><tr><th>Parfum</th><th class="r">Qté</th><th class="r">Prix</th><th class="r">Stock</th></tr></thead><tbody>
    ${LG.map(l=>`<tr>${l.service?`<td><span class="lsc-s">${l.carte?'Frais carte':'Frais'} — la caisse dit « ${esc(l.des||'?')} »${l.carte?'':' · hors stock, pas sur la facture'}</span></td>`
        :`<td>${l.cle?`<b>${esc(fNomComplet(l.cle))}</b><small> ${esc(l.bc)}</small>`
        :`<span class="lsc-x">à identifier — la caisse dit « ${esc(l.des||l.bc||'?')} »</span><input class="sel lsc-ch" list="lsc-cat" data-j="${l.j}" placeholder="Tape le nom ou le code-barres du parfum…" autocomplete="off">`}</td>`}
      <td class="r">${nf(l.q)}</td><td class="r">${l.p!=null?money2(l.p):'—'}</td><td class="r">${l.cle?nf(qteEff(l.cle)):'—'}</td></tr>`).join('')}
    </tbody></table><datalist id="lsc-cat"></datalist>
    <p class="lsc-m" id="lsc-m">${inc?`<b>${inc} parfum${inc>1?'s':''} à identifier</b> avant de valider.`:(fc>0?`Le card charge de la caisse (${money2(fc)}) sera porté sur la facture en « Frais carte », ajouté au total.`:'')}</p>
    <div class="lsc-a"><button class="btn" data-lx="1">Annuler</button> <button class="btn pri" id="lsc-ok" ${inc?'disabled':''}>Valider la vente — sortir du stock</button></div></div>`;
}
function lscBranche(f){
  const id=f.dataset.c;
  if(f.querySelector('.lsc-ch')){ const dl=$('lsc-cat'); dl.innerHTML=Object.keys(IDX).map(k=>`<option data-cle="${esc(k)}" value="${esc(fNomComplet(k)+((IDX[k]||[])[0]?' — '+IDX[k][0]:''))}">`).join(''); }
  f.querySelectorAll('.lsc-ch').forEach(inp=>inp.onchange=()=>{ const o=[...$('lsc-cat').options].find(op=>op.value===inp.value); if(!o) return;
    const cli=$('lsc-cli').value, pay=$('lsc-pay')?$('lsc-pay').value:'';
    lsqMaj(id,z=>{ z.erp=Object.assign({},z.erp||{}); z.erp.choix=Object.assign({},z.erp.choix||{},{[inp.dataset.j]:o.dataset.cle}); if(pay) z.erp.pay=pay; });
    lscPeint(); try{ $('lsc-cli').value=cli; }catch(e){} });
  f.querySelector('[data-lx]').onclick=()=>{ LSQ_CONV=''; lscPeint(); };
  $('lsc-ok').onclick=()=>{
    const x=lsqTous().find(z=>z.id===id); if(!x||lsqEtat(x)!=='cree') return;
    const nom=$('lsc-cli').value.trim(), d=$('lsc-d').value;
    if(!nom){ $('lsc-m').innerHTML='<b>Le nom du client</b> est nécessaire : la facture est à son nom.'; $('lsc-cli').focus(); return; }
    if(!/^\d{4}-\d{2}-\d{2}$/.test(d)){ $('lsc-m').innerHTML='<b>La date</b> de la vente est nécessaire.'; return; }
    const LG0=lsqLignes(x); if(LG0.some(l=>!l.cle&&!l.service)) return;
    const LG=LG0.filter(l=>l.cle), fc=lsqFraisCarte(LG0), nh=LG0.filter(l=>l.service&&!l.carte).length;
    const pay=($('lsc-pay')&&$('lsc-pay').value==='carte')?'carte':'zelle', payLib=pay==='carte'?'carte bancaire':'Zelle';
    const C=faContexte();
    const v={_i:'lsq|'+x.id,src:'lightspeed',num:'Devis '+x.num,client:nom,d,h:(typeof heureMiami==='function'?heureMiami():''),lieu:'Caisse Lightspeed',taxe:x.taxe,total:x.total,recu:x.recu,hors:nh};
    /* payée par carte SANS card charge : Sam supporte les frais de carte (2,6 % retirés de la marge, comme à la caisse) ;
       AVEC card charge : le client les a payés, ils s'annulent — rien n'est retiré de la marge, le frais n'entre pas dans le chiffre */
    if(fc>0) v.fraisCarte=fc; else if(pay==='carte'){ const tot=Math.round((LG.reduce((a,l)=>a+(+l.q||0)*(+l.p||0),0)+(+x.taxe||0))*100)/100; v.paie={carte:tot}; }
    if(pay==='carte') v.mode='carte';
    const r=faEnregistre([{v,L:LG.map(l=>({cle:l.cle,bc:l.bc,des:l.des,q:l.q,p:l.p}))}],C,{lib:'devis Lightspeed '+(x.num||'')+' converti en vente, payé par '+payLib+' ('+nom+')'+(fc>0?', card charge '+money2(fc)+' en frais carte':'')+' — facture faite, stock sorti'});
    if(!r||!r.ventes){ $('lsc-m').innerHTML="<b>La vente n'a pas pu être enregistrée.</b> Recharge la page et réessaie."; return; }
    const fid=r.ids[0]||'';
    const F=lit('factures-v1',[]); const fa=F.find(z=>z.id===fid);
    if(fa){ fa.mode=pay; fa.devisLS=x.num; if(fa.doc){ fa.doc.pmode=pay; fa.doc.note='Devis Lightspeed '+(x.num||'')+' — payé par '+payLib; } ecrit('factures-v1',F); }
    lsqMaj(id,z=>{ z.erp=Object.assign({},z.erp||{},{etat:'vendue',factId:fid,par:USR||'',t:new Date().toISOString(),d,pay,fraisCarte:fc||undefined}); });
    FACT=lit('factures-v1',[]);
    LSQ_CONV=''; LSQ_OUV=''; LSQ_F.etat='converti'; lscPeint();
    try{ construitV(); }catch(e){}
  };
}
/* « Mettre à jour depuis Lightspeed » : le mode d'emploi, et le favori pour qui a le droit Réglages */
async function lsqAide(){
  const a=$('lsq-aide'); if(!a) return; if(!a.hidden){ a.hidden=true; return; }
  a.hidden=false; a.setAttribute('data-nolang','');
  /* 20 oct. 2026 (Igal : « à chaque fois qu'une cote est faite sur Lightspeed, je veux qu'elle soit sur l'ERP ») : Lightspeed refuse de relier
     une application sur le forfait actuel. L'extension Chrome, installée une fois sur l'ordinateur de la caisse, envoie les cotes toute seule
     tant que Lightspeed est ouvert et connecté (ce qu'il est quand on fait une cote). Le favori reste en secours. */
  a.innerHTML=`<p><b>${r3('Les cotes de la caisse arrivent ici toutes seules, avec l\'extension Chrome.','Register quotes arrive here by themselves, with the Chrome extension.','Las cotizaciones de la caja llegan aquí solas, con la extensión de Chrome.')}</b> ${r3('À installer une seule fois, sur l\'ordinateur où se fait la caisse Lightspeed.','Install it once, on the computer where the Lightspeed register is used.','Instálala una sola vez, en el ordenador donde se usa la caja Lightspeed.')}</p>
    <ol><li>${r3('Télécharge-la :','Download it:','Descárgala:')} <button class="btn pri" id="lsq-ext">${r3('Télécharger l\'extension','Download the extension','Descargar la extensión')}</button> <span id="lsq-ext-m"></span></li>
    <li>${r3('Ouvre le fichier téléchargé (<b>cotes-lightspeed-erp.zip</b>) : il se décompresse en un dossier <b>cotes-lightspeed-erp</b>. Range-le quelque part où il restera (par exemple dans Documents) : ne le supprime pas.','Open the downloaded file (<b>cotes-lightspeed-erp.zip</b>): it unzips into a folder <b>cotes-lightspeed-erp</b>. Put it somewhere it will stay (for example Documents): do not delete it.','Abre el archivo descargado (<b>cotes-lightspeed-erp.zip</b>): se descomprime en una carpeta <b>cotes-lightspeed-erp</b>. Guárdala donde se quede (por ejemplo Documentos): no la borres.')}</li>
    <li>${r3('Dans Chrome, tape <b>chrome://extensions</b> dans la barre d\'adresse. En haut à droite, active <b>Mode développeur</b>.','In Chrome, type <b>chrome://extensions</b> in the address bar. At the top right, turn on <b>Developer mode</b>.','En Chrome, escribe <b>chrome://extensions</b> en la barra de direcciones. Arriba a la derecha, activa <b>Modo de desarrollador</b>.')}</li>
    <li>${r3('Clique <b>Charger l\'extension non empaquetée</b> et choisis le dossier <b>cotes-lightspeed-erp</b>.','Click <b>Load unpacked</b> and choose the <b>cotes-lightspeed-erp</b> folder.','Haz clic en <b>Cargar descomprimida</b> y elige la carpeta <b>cotes-lightspeed-erp</b>.')}</li>
    <li>${r3('Ouvre Lightspeed (connecté) : un cadre vert « Cotes → ERP : actif » apparaît 8 secondes. Ensuite, chaque cote faite dans la caisse arrive ici en quelques minutes. Rien à cliquer.','Open Lightspeed (signed in): a green box “Cotes → ERP: actif” shows for 8 seconds. After that, every quote made at the register arrives here within minutes. Nothing to click.','Abre Lightspeed (con sesión iniciada): aparece 8 segundos un cuadro verde «Cotes → ERP: actif». Después, cada cotización hecha en la caja llega aquí en pocos minutos. Nada que pulsar.')}</li></ol>
    <p class="ecr">${r3('Condition : l\'ordinateur de la caisse doit avoir Chrome ouvert sur Lightspeed, connecté. C\'est une limite de Lightspeed (forfait actuel), pas de l\'ERP.','Condition: the register computer must have Chrome open on Lightspeed, signed in. This is a Lightspeed limit (current plan), not the ERP\'s.','Condición: el ordenador de la caja debe tener Chrome abierto en Lightspeed, con sesión iniciada. Es un límite de Lightspeed (plan actual), no del ERP.')}</p>
    <p id="lsq-fl" class="ecr"></p>`;
  const peut=()=>typeof CK_URL!=='undefined'&&typeof ckTok==='function'&&!!ckTok();
  const bt=$('lsq-ext'), mm=$('lsq-ext-m');
  bt.onclick=async()=>{
    mm.textContent=''; bt.disabled=true;
    try{
      if(!peut()) throw new Error(r3('Il faut ouvrir l\'ERP en ligne, connecté.','Open the online ERP, signed in.','Abre el ERP en línea, con sesión iniciada.'));
      const r=await fetch(CK_URL+'/api/o/'+CK_ORG+'/lightspeed/extension.zip',{headers:{Authorization:'Bearer '+ckTok()}});
      if(!r.ok){ let m=''; try{ m=(await r.json()).erreur||''; }catch(e){} throw new Error(m==='Il faut le droit Réglages.'?r3('Le téléchargement se fait depuis un compte qui a le droit Réglages.','Downloading needs an account with the Settings right.','La descarga requiere una cuenta con el derecho Ajustes.'):(m||('erreur '+r.status))); }
      const bl=await r.blob(), u=URL.createObjectURL(bl), l=document.createElement('a');
      l.href=u; l.download='cotes-lightspeed-erp.zip'; document.body.appendChild(l); l.click(); l.remove(); setTimeout(()=>URL.revokeObjectURL(u),4000);
      mm.textContent=r3('Téléchargée.','Downloaded.','Descargada.');
    }catch(e){ mm.textContent=String(e.message||e); }
    bt.disabled=false;
  };
  /* le favori « Devis → ERP » reste en secours, pour un ordinateur où l'extension ne peut pas s'installer */
  try{
    if(!peut()) throw new Error('hors ligne');
    const r=await fetch(CK_URL+'/api/o/'+CK_ORG+'/lightspeed/favori',{headers:{Authorization:'Bearer '+ckTok()}});
    const j=await r.json().catch(()=>({}));
    if(!r.ok) throw new Error(j.erreur||r.status);
    $('lsq-fl').innerHTML=`${r3('En secours, sans extension : fais glisser ce bouton dans la barre des favoris de Chrome, puis clique-le sur la page Devis de Lightspeed.','As a fallback, without the extension: drag this button into Chrome\'s bookmarks bar, then click it on Lightspeed\'s Quotes page.','De respaldo, sin extensión: arrastra este botón a la barra de marcadores de Chrome y púlsalo en la página de cotizaciones de Lightspeed.')} <a class="btn lsq-fv" href="${esc(j.lien)}" onclick="event.preventDefault();alert('${r3('Fais-le glisser dans la barre des favoris (ne clique pas dessus ici).','Drag it to the bookmarks bar (do not click it here).','Arrástralo a la barra de marcadores (no pulses aquí).')}')">Devis → ERP</a>`;
  }catch(e){ $('lsq-fl').textContent=''; }
}
function lscInit(){
  if(!$('lsc')){ const s=document.createElement('section'); s.id='lsc'; s.className='lsc'; $('docs').after(s); }  /* ordre : la fenêtre d'une cote (si ouverte), les cotes de l'ERP, puis celles de Lightspeed */
  lscPeint();
  /* 29 sept. (Igal : « regarde bien la partie cote, ça n'a rien à voir avec ce que je t'ai
     demandé ») : la rubrique Cote, c'est LES COTES DE LIGHTSPEED. Le devis fait dans l'ERP
     (fenêtre « Nouveau devis » et sa liste) passe en dessous, replié, derrière un bouton. */
  /* 20 oct. 2026 (Igal : « c'est pas normal qu'à chaque fois les cotes s'effacent de l'ERP ») : la liste des cotes
     faites dans l'ERP et la fenêtre pour en faire une étaient repliées derrière « afficher » (retenu par ordinateur) —
     sur un ordinateur neuf, une cote qu'on venait de faire n'était plus visible. Plus de repli : la liste est
     toujours là, et la fenêtre s'ouvre avec « + Nouvelle cote » ou « Coller un message du client » (en haut). */
  /* Le bouton « Supprimer les cotes d'essai faites dans l'ERP » est retiré : une seule confirmation effaçait TOUTES les
     cotes non converties faites dans l'ERP. Une cote se supprime une par une (bouton « Supprimer » de sa ligne). */
  $('docs').hidden=false;
  window.addEventListener('ck-maj',e=>{ try{ if((e.detail&&e.detail.cles||[]).includes(KDEV)&&!document.querySelector('.lsc-f')) lscPeint(); }catch(_){} });
}
/* dans un setTimeout : le bloc des documents (DOCS_F, peintDocs) est declare plus
   bas dans le script, apres celui-ci — on attend que tout soit en place */
if(MODE_QUOTES) setTimeout(()=>{
  document.body.classList.add('quotes');
  /* la fenetre de vente devient la fenetre du devis, ouverte en permanence et
     posee en tete de page : ce qui ne concerne pas un devis s'efface */
  try{ $('docs').before($('vov')); }catch(e){}
  /* les reglages du document (paiement, remise, taxe) passent SOUS les lignes :
     ce qu'on fait d'abord ici, c'est choisir les parfums et poser les prix */
  try{ $('v-recap').before($('v-docbloc')); }catch(e){}
  const canalGros=()=>{ try{ if([...$('v-canal').options].some(o=>o.value==='Gros')){ $('v-canal').value='Gros'; majAide(); } }catch(e){} };
  const _ouvre=ouvreVente;
  ouvreVente=function(){ _ouvre(); $('vov').querySelector('.mh h3').textContent='Nouveau devis';
    const vd=$('v-pan').querySelector('.vide'); if(vd) vd.textContent='Aucun parfum. Tape une marque ou un nom ci-dessus, coche, ajoute.';
    $('v-ok').textContent='Enregistrer le devis'; $('v-stock').checked=false; canalGros();
    $('vov').classList.remove('on');   /* ce n'est plus une fenetre : Echap ne doit rien fermer */
    try{ $('v-doc').value='devis'; $('v-doc').dataset.touche='1'; docChampsMaj(); }catch(e){}
    /* 20 oct. 2026 : la fenêtre n'est plus ouverte en permanence derrière un repli caché — elle s'ouvre quand on la demande
       (« + Nouvelle cote », « Coller un message du client », « Modifier » sur une cote), et se referme une fois la cote enregistrée */
    const voulu=COTE_VOULUE; COTE_VOULUE=false; $('vov').hidden=!voulu; };
  /* ouvre la fenêtre d'une cote neuve (ou la laisse telle quelle si elle est déjà ouverte et en cours) */
  window.coteNouvelle=function(){
    if($('vov').hidden){ COTE_VOULUE=true; ouvreVente(); }
    try{ $('vov').scrollIntoView({behavior:'smooth',block:'start'}); }catch(e){}
    setTimeout(()=>{ try{ $('v-client').focus(); }catch(e){} },250); };
  /* « Modifier » sur une cote de l'ERP : la fenêtre se montre avec la cote dedans */
  { const _om=ouvreModif; ouvreModif=function(f){ _om(f); if(EDIT){ $('vov').hidden=false; try{ $('vov').scrollIntoView({behavior:'smooth',block:'start'}); }catch(e){} } }; }
  /* une cote enregistrée (neuve ou modifiée) : la fenêtre se referme et repart à zéro — la cote est dans la liste juste dessous */
  { const _ok=$('v-ok').onclick;
    $('v-ok').onclick=function(e){ const avant=FACT.length, edit=!!EDIT; const r=_ok.call(this,e);
      setTimeout(()=>{ if((edit&&!EDIT)||FACT.length>avant){ try{ localStorage.removeItem('cote-brouillon'); }catch(_){} try{ ouvreVente(); }catch(_){}
        try{ const l=document.querySelector('.docs'); if(l) l.scrollIntoView({behavior:'smooth',block:'start'}); }catch(_){} } },60);
      return r; }; }
  /* 20 oct. 2026 (Igal : Sam faisait une cote, a ajouté un parfum, la page est devenue blanche et tout s'est effacé — « on ne peut pas avoir ce
     genre d'erreur ») : la cote en cours est gardée sur ce poste toutes les 3 secondes (clé locale, jamais envoyée au serveur) et remise telle
     quelle à la réouverture de la page — quoi qu'il arrive : page blanche, session expirée, onglet fermé, panne. Elle ne disparaît que
     par « Enregistrer le devis » ou « Vider » (confirmé). Au bout de 24 h on ne la reprend plus. */
  { const KBR='cote-brouillon';
    const brSauve=()=>{ try{
      if($('vov').hidden||EDIT) return;
      const lignes=PANIER.map(l=>Object.assign({},l)), client=$('v-client').value, note=$('v-note')?$('v-note').value:'';
      if(!lignes.length&&!client.trim()&&!note.trim()) return;       /* rien à garder : on n'efface PAS un brouillon existant ici */
      localStorage.setItem(KBR,JSON.stringify({t:Date.now(),client,note,canal:$('v-canal').value,lignes})); }catch(e){} };
    window.__brSauve=brSauve;
    setInterval(brSauve,3000);
    ['v-client','v-note','v-canal'].forEach(id=>{ const e=$(id); if(e) e.addEventListener('input',brSauve); });
    window.addEventListener('pagehide',brSauve); document.addEventListener('visibilitychange',()=>{ if(document.hidden) brSauve(); });
  }
  /* en haut de la page, deux gestes : une cote à la main, ou le message du client collé */
  { const nv=$('nv'), mb=$('msgb');
    if(nv){ nv.textContent='+ Nouveau devis'; nv.title=''; nv.onclick=window.coteNouvelle; }
    if(mb){ mb.textContent='Coller un message du client'; mb.title='';
      mb.onclick=()=>{ mOuvre(); try{ if([...$('m-canal').options].some(o=>o.value==='Gros')) $('m-canal').value='Gros'; }catch(e){} mPeint(); }; } }
  /* le raccourci : coller ou deposer la liste du client, qui remplit les lignes */
  const bl=document.createElement('button'); bl.type='button'; bl.className='btn'; bl.id='v-liste';
  bl.textContent='Coller ou déposer la liste du client';
  $('vov').querySelector('.mh h3').after(bl);
  bl.onclick=()=>{ const cl=$('v-client').value.trim(); mOuvre(); $('m-client').value=cl;
    try{ if([...$('m-canal').options].some(o=>o.value==='Gros')) $('m-canal').value='Gros'; }catch(e){} mPeint(); };
  $('m-devis').textContent='Mettre ces parfums dans le devis →';
  /* les lignes reconnues REJOIGNENT le devis en cours : ce que Sam a deja ajoute
     a la main n'est pas perdu, et un parfum deja present voit sa quantite s'ajouter */
  $('m-devis').onclick=()=>{
    const pris=M_L.filter(l=>l.cle); if(!pris.length) return;
    mApprend();
    const client=$('m-client').value.trim(); mFerme();
    if($('vov').hidden){ COTE_VOULUE=true; ouvreVente(); }
    if(client && !$('v-client').value.trim()) $('v-client').value=client;
    pris.forEach(l=>{ const e=PANIER.find(x=>x.cle===l.cle); if(e){ e.q+=l.q; if(l.p!=null){ e.p=l.p; e.pf=true; } } else PANIER.push(mPanierLigne(l)); });
    peintPanier();
    $('v-msg').textContent='Rempli depuis le message du client — vérifie les prix avant d\'émettre le devis.';
    try{ $('vov').scrollIntoView({behavior:'smooth',block:'start'}); }catch(e){}
    setTimeout(()=>$('v-pan').querySelector('input[data-f="p"]')?.focus(),360);
  };
  /* « Annuler » vide le devis en cours au lieu de fermer une fenetre qui n'en est plus une */
  $('v-ann').textContent='Vider';
  $('v-ann').onclick=()=>{ if(EDIT){ if(confirm(vf('Abandonner les modifications ? Le devis reste comme avant.'))) ouvreVente(); return; }
    if(!PANIER.length || confirm(vf('Vider ce devis ? Rien ne sera enregistré.'))){ try{ localStorage.removeItem('cote-brouillon'); }catch(e){} ouvreVente(); } };
  $('vx').onclick=null;
  /* ---- le sélectionneur de parfums ----
     Il tape « Paco Rabanne » : TOUS les Paco Rabanne s'affichent, rangés, avec le prix
     d'achat, le tarif de gros et le stock. Il coche ceux qu'il veut, il ajoute. Le
     champ n'est plus une simple recherche à un coup : c'est un choix dans le catalogue. */
  let COCHES=new Set();
  /* la photo du parfum : celle de l'outil (photos/), sinon celle du site, sinon une case vide */
  window.vignette=function(cle){ return photoImg('vig','<span class="vig miss">—</span>',cle,''); };
  try{ vq().previousElementSibling.textContent='Choisir les parfums — tape une marque ou un nom, coche, ajoute'; ['v-q','v-q2'].forEach(id=>{ $(id).placeholder='Marque, nom du parfum ou code-barres'; }); $('v-q2').previousElementSibling.textContent='Ajouter d\'autres parfums — sans remonter'; }catch(e){}
  chercheProduits=function(q){
    q=q.trim().toLowerCase(); if(q.length<2) return [];
    const chiffres=/^\d{6,14}$/.test(q), mots=q.split(/\s+/).filter(Boolean);
    const R=[];
    for(const cle in IDX){
      const v=IDX[cle];
      if(chiffres){ const nq=q.replace(/^0+/,''); const m=MOD[cle];
        if((v[0]||'').replace(/^0+/,'')===nq || (m&&m.bcs&&String(m.bcs).split(/[^0-9]+/).map(x=>x.replace(/^0+/,'')).includes(nq)) || (bcExtra()[cle]||[]).includes(nq)) R.push(cle); }
      else { const t=((v[2]||'')+' '+(v[1]||'')+' '+(v[0]||'')).toLowerCase(); if(mots.every(m=>t.includes(m))) R.push(cle); }
      if(R.length>300) break;
    }
    /* la marque demandée d'abord (« Paco Rabanne 1 Million »), les parfums qui ne
       font que la citer ensuite (« Dumont Nitro Red (Paco Rabanne Invictus) ») */
    const nom=c=>((IDX[c][2]||'')+' '+(IDX[c][1]||'')).toLowerCase();
    const rang=c=>mots.every(m=>(IDX[c][2]||'').toLowerCase().includes(m))?0:mots.every(m=>(IDX[c][1]||'').toLowerCase().includes(m))?1:2;
    return R.sort((a,b)=>rang(a)-rang(b)||nom(a).localeCompare(nom(b))||(+IDX[a][3]||0)-(+IDX[b][3]||0));
  };
  peintRes=function(){
    const el=$('v-res');
    if(!CANDIDATS.length){ el.classList.remove('on'); el.innerHTML=''; COCHES.clear(); return; }
    const CAND=new Set(CANDIDATS); [...COCHES].forEach(c=>{ if(!CAND.has(c)) COCHES.delete(c); });
    const gros=CANAUX_VENTE().find(c=>c.id==='gros')||canalCour();
    el.innerHTML=CANDIDATS.map((cle,i)=>{ const v=IDX[cle], st=qteEff(cle), on=COCHES.has(cle);
      return `<div class="cand ${on?'coche':''} ${i===SEL?'sel':''}" data-cle="${esc(cle)}"><input type="checkbox" ${on?'checked':''} tabindex="-1">
        ${vignette(cle)}
        <b>${esc(v[2]||'')} ${esc(v[1]||'')}${tyBadge(cle)}${v[3]?' <span style="font-weight:500;color:var(--ink-2)">'+esc(v[3])+' oz</span>':''}</b>
        <span>stock <i>${nf(st)}</i></span></div>`; }).join('')
      +`<div class="cpied"><button type="button" class="btn pri" id="v-cadd" ${COCHES.size?'':'disabled'}>Ajouter ${COCHES.size?COCHES.size+' ':''}au devis</button>
        <button type="button" class="btn" id="v-ctous">Tout cocher</button>
        <em>${CANDIDATS.length} parfum${CANDIDATS.length>1?'s':''} trouvé${CANDIDATS.length>1?'s':''} — coche, puis ajoute</em></div>`;
    el.classList.add('on');
    el.querySelectorAll('[data-cle]').forEach(d=>d.onclick=()=>{ const c=d.dataset.cle; if(COCHES.has(c)) COCHES.delete(c); else COCHES.add(c); peintRes(); });
    $('v-cadd').onclick=()=>ajouteCoches();
    $('v-ctous').onclick=()=>{ CANDIDATS.forEach(c=>COCHES.add(c)); peintRes(); };
  };
  function ajouteCoches(){
    const L=CANDIDATS.filter(c=>COCHES.has(c)); if(!L.length) return;
    L.forEach(cle=>{ if(!PANIER.some(l=>l.cle===cle)) PANIER.push({cle,q:1,p:prixSuggere(cle,canalCour())}); });
    COCHES.clear(); vq().value=''; CANDIDATS=[]; SEL=-1; peintRes(); peintPanier(); vq().focus();
  }
  /* Entrée : ce qui est coché part dans le devis ; rien de coché, le parfum surligné y va seul */
  ['v-q','v-q2'].forEach(id=>$(id).addEventListener('keydown',e=>{ if(e.key==='Enter'&&COCHES.size){ e.stopImmediatePropagation(); e.preventDefault(); ajouteCoches(); } },true));
  /* ---- les lignes du devis : prix d'achat, tarif de gros, et LE prix qu'il propose ---- */
  const _peintPanier=peintPanier;
  peintPanier=function(){
    _peintPanier();
    const t=$('v-pan').querySelector('table'); if(!t) return;
    const gros=CANAUX_VENTE().find(c=>c.id==='gros')||canalCour();
    const th=t.querySelector('thead tr'); const ths=th.children;
    ths[3].textContent='Prix proposé';
    const h1=document.createElement('th'); h1.className='r colpa'; h1.textContent="Prix d'achat";
    const h2=document.createElement('th'); h2.className='r'; h2.textContent='Tarif gros';
    th.insertBefore(h2,ths[3]); th.insertBefore(h1,h2);
    t.querySelectorAll('tbody tr').forEach((tr,i)=>{ const l=PANIER[i]; if(!l) return;
      const pa=paEff(l.cle), pg=prixSuggere(l.cle,gros);
      try{ tr.children[1].insertAdjacentHTML('afterbegin', vignette(l.cle)); }catch(e){}
      const c1=document.createElement('td'); c1.className='r colref colpa'; c1.textContent=pa!=null?money2(pa):'—';
      const c2=document.createElement('td'); c2.className='r colref'; c2.textContent=pg!=null?money2(pg):'—';
      tr.insertBefore(c2,tr.children[3]); tr.insertBefore(c1,c2); });
    const tf=t.querySelector('tfoot tr'); if(tf){ const e1=document.createElement('td'); e1.className='colpa'; tf.insertBefore(document.createElement('td'),tf.children[3]); tf.insertBefore(e1,tf.children[3]); }
  };
  ouvreVente();
  $('v-note-w').hidden=false;
  /* un message collé dans Ventes (« Faire un devis ») arrive ici : fenêtre des messages ouverte, parfums reconnus */
  try{ const brut=localStorage.getItem('cote-depuis-message');
    if(brut){ localStorage.removeItem('cote-depuis-message'); const o=JSON.parse(brut);
      if(o&&o.txt&&Date.now()-(+o.t||0)<10*60e3){ mOuvre(); $('m-txt').value=o.txt; $('m-client').value=o.client||'';
        try{ if([...$('m-canal').options].some(x=>x.value==='Gros')) $('m-canal').value='Gros'; }catch(e){}
        mLit($('m-txt').value); mPeint(); } } }catch(e){}
  /* le brouillon d'une cote en cours est remis ici, APRÈS l'ouverture initiale de la fenêtre (qui la remet à zéro) */
  { const KBR='cote-brouillon';
  if(!$('msgov').classList.contains('on')) try{ const br=JSON.parse(localStorage.getItem(KBR)||'null');
      if(br&&Date.now()-(+br.t||0)<24*3600e3&&Array.isArray(br.lignes)&&(br.lignes.length||String(br.client||'').trim()||String(br.note||'').trim())){
        COTE_VOULUE=true; ouvreVente();
        PANIER=br.lignes.filter(l=>l&&IDX[l.cle]);
        $('v-client').value=br.client||''; if($('v-note')) $('v-note').value=br.note||'';
        try{ if(br.canal&&[...$('v-canal').options].some(o=>o.value===br.canal)) $('v-canal').value=br.canal; majAide(); }catch(e){}
        peintPanier(); try{ recap(); }catch(e){}
        $('v-msg').textContent=r3('Cote en cours retrouvée (brouillon gardé sur cet ordinateur) — vérifie-la, puis enregistre-la ou clique « Vider ».','Quote in progress recovered (draft kept on this computer) — check it, then save it or click “Clear”.','Cotización en curso recuperada (borrador guardado en este ordenador) — revísala y guárdala, o pulsa «Vaciar».'); } } catch(e){} }
  /* ---- la liste des devis, comme dans la caisse Lightspeed que Sam connaît ----
     Filtres (état, client, numéro), une ligne par devis : numéro et heure, client
     avec son email, créé par, note, total, état. La ligne se déplie sur ses lignes
     et ses boutons : convertir en facture, WhatsApp, e-mail, PDF, archiver. */
  var Q_F={etat:'devis',cli:'',num:''}, Q_OUVERT='';
  const couleur=n=>{ let h=0; for(const c of String(n||'')) h=(h*31+c.charCodeAt(0))%360; return `hsl(${h} 45% 52%)`; };
  const initiales=n=>String(n||'?').trim().split(/\s+/).slice(0,2).map(x=>x[0]||'').join('').toUpperCase()||'?';
  const etatDe=f=>f.doc.archive?'archive':(f.doc.converti?'converti':'devis');
  const LIB_ET={devis:'Créé',converti:'Converti en facture',archive:'Archivé'};
  peintDocs=function(){
    const L=FACT.filter(f=>f.doc&&f.doc.type==='devis'&&!f.lsq).sort((a,b)=>(b.t||'').localeCompare(a.t||''));
    const V=L.filter(f=>{ const e=etatDe(f);
      if(Q_F.etat==='devis'&&e!=='devis') return false; if(Q_F.etat==='converti'&&e!=='converti') return false; if(Q_F.etat==='archive'&&e!=='archive') return false;
      if(Q_F.cli&&!cNorm(f.tiers||'').includes(cNorm(Q_F.cli))) return false;
      if(Q_F.num&&!String(f.doc.num||'').toLowerCase().includes(Q_F.num.toLowerCase())) return false;
      return true; });
    { const n=V.length, pl=n>1?'s':''; const et=Q_F.etat==='devis'?' créé'+pl:Q_F.etat==='converti'?' converti'+pl:Q_F.etat==='archive'?' archivé'+pl:'';
      $('docs-em').textContent=L.length?vf(`${nf(n)} devis${et}${n!==L.length?' · '+nf(L.length)+' au total':''}`):vf('aucun encore'); }
    const h=document.querySelector('.docs h2.sec'); if(h) h.firstChild.textContent='Devis ';
    $('docs-table').innerHTML=`<div class="qf">
        <div class="fld"><label>État</label><select id="q-etat"><option value="devis">Créés</option><option value="converti">Convertis en facture</option><option value="archive">Archivés</option><option value="">Tous les devis</option></select></div>
        <div class="fld"><label>Client</label><input id="q-cli" placeholder="Chercher un client" value="${esc(Q_F.cli)}"></div>
        <div class="fld"><label>Devis</label><input id="q-num" placeholder="N° de devis" value="${esc(Q_F.num)}"></div></div>`
      +(!L.length?'':!V.length?'<p class="ecr">Aucun devis dans cette catégorie.</p>':`<table class="ql"><thead><tr><th></th><th>Devis</th><th>Client</th><th>Créé par</th><th>Note</th><th class="r">Total du devis</th><th>État</th></tr></thead><tbody>
      ${V.slice(0,80).map(f=>{ const co=coordTiers(f.tiers), e=etatDe(f), on=Q_OUVERT===f.id;
        const heure=f.h||(f.t?heureMiami(f.t):'');
        const ligne=`<tr class="qr ${on?'on':''}" data-q="${esc(f.id)}"><td class="chev">${on?'⌄':'›'}</td>
          <td class="num"><b>${esc(f.doc.num)}</b><small>${dfr(f.d)}${heure?', '+esc(heure):''}</small></td>
          <td><div class="cli">${f.tiers?`<i style="background:${couleur(f.tiers)}">${esc(initiales(f.tiers))}</i>`:''}<span><b>${esc(f.tiers||'—')}</b>${co.email||co.tel?`<small>${esc([co.email,co.tel].filter(Boolean).join(' · '))}</small>`:''}</span></div></td>
          <td>${esc(f.par||'—')}</td><td>${f.doc.fusion?`<span class="lbl">fusionnée dans</span> <span data-nolang>${esc(f.doc.fusion)}</span>${f.doc.note?' · ':''}`:''}${esc(f.doc.note||'')}</td>
          <td class="r"><b>${money2(f.doc.total)}</b></td><td><span class="et ${e}">${LIB_ET[e]}</span></td></tr>`;
        if(!on) return ligne;
        const D=f.doc, lignes=(f.lignes||[]).filter(l=>l.q);
        return ligne+`<tr class="qd"><td colspan="7"><div class="qdet"><div>
            ${lignes.map(l=>`<div class="lg"><span>${nf(l.q)}</span><span><b>${esc(l.ref)}${tyVu(l)}</b><br><small>${esc(l.bc||'')}</small></span><span>@ ${money2(l.p)}</span><span class="r"><b>${money2((l.q||0)*(l.p||0))}</b></span></div>`).join('')}
            <div class="tot"><span>Sous-total</span><span class="r">${money2(D.sousTotal)}</span>
              ${D.remise?`<span>Remise</span><span class="r">−${money2(D.remise)}</span>`:''}
              <span>${D.taux?`Sales tax ${D.taux} %`:'Sales tax — exonéré'}</span><span class="r">${money2(D.taxe||0)}</span>
              <span class="tt">TOTAL DU DEVIS</span><span class="r tt">${money2(D.total)}</span></div>
            ${D.note?`<div class="note"><b>Note</b> — ${esc(D.note)}</div>`:''}
            ${(f.modifs||[]).length?`<div class="note">Modifié ${f.modifs.length>1?nf(f.modifs.length)+' fois':'une fois'} — dernière modification le ${esc(dfr(String(f.modifs[f.modifs.length-1].t||'').slice(0,10)))} par ${esc(f.modifs[f.modifs.length-1].u||'—')}</div>`:''}
            ${D.converti?`<div class="note"><b>Converti en facture</b> ${esc(D.convertiNum||'')}</div>`:''}
            ${(D.envoye||[]).length?`<div class="note">Envoyé par e-mail à ${esc(D.envoye.map(x=>x.a).join(', '))}</div>`:''}
          </div><div class="btns">
            ${e==='devis'?`<button class="btn pri" data-qa="conv" data-q="${esc(f.id)}">Convertir en facture</button>`:''}
            ${!D.converti?`<button class="btn" data-qa="modif" data-q="${esc(f.id)}" title="Changer les parfums, les quantités, les prix, le client ou la note">Modifier</button>`:''}
            ${(()=>{ const A=e==='devis'?cotesAFusionner(f):[]; return A.length?`<button class="btn" data-qa="fus" data-q="${esc(f.id)}" data-nolang title="${esc(r3('Réunir dans cette cote les autres cotes créées pour ce client : '+A.map(x=>x.doc.num).join(', '),'Combine into this quote the other created quotes of this customer: '+A.map(x=>x.doc.num).join(', '),'Reunir en esta cotización las otras cotizaciones creadas para este cliente: '+A.map(x=>x.doc.num).join(', ')))}">${esc(r3(`Fusionner les ${A.length+1} cotes de ${f.tiers}`,`Merge the ${A.length+1} quotes of ${f.tiers}`,`Fusionar las ${A.length+1} cotizaciones de ${f.tiers}`))}</button>`:''; })()}
            <button class="btn" data-qa="wa" data-q="${esc(f.id)}">Envoyer par WhatsApp</button>
            <button class="btn" data-qa="mail" data-q="${esc(f.id)}">Envoyer par e-mail</button>
            <button class="btn" data-qa="voir" data-q="${esc(f.id)}">Voir / imprimer le devis</button>
            ${e==='archive'?`<button class="btn" data-qa="desarch" data-q="${esc(f.id)}">Désarchiver</button>`:`<button class="btn" data-qa="arch" data-q="${esc(f.id)}">Archiver</button>`}
            ${e!=='converti'?`<button class="btn" data-qa="sup" data-q="${esc(f.id)}" title="Retirer ce devis pour de bon — un devis converti en facture ne se supprime pas, il s'archive">Supprimer</button>`:''}
          </div></div></td></tr>`; }).join('')}</tbody></table>`);
    $('q-etat').value=Q_F.etat;
    $('q-etat').onchange=()=>{ Q_F.etat=$('q-etat').value; peintDocs(); };
    $('q-cli').oninput=()=>{ Q_F.cli=$('q-cli').value; peintDocs(); $('q-cli').focus(); const v=$('q-cli').value; $('q-cli').setSelectionRange(v.length,v.length); };
    $('q-num').oninput=()=>{ Q_F.num=$('q-num').value; peintDocs(); $('q-num').focus(); const v=$('q-num').value; $('q-num').setSelectionRange(v.length,v.length); };
    $('docs-table').querySelectorAll('tr.qr').forEach(tr=>tr.onclick=()=>{ Q_OUVERT=Q_OUVERT===tr.dataset.q?'':tr.dataset.q; peintDocs(); });
    $('docs-table').querySelectorAll('[data-qa]').forEach(b=>b.onclick=e=>{ e.stopPropagation();
      const f=FACT.find(x=>x.id===b.dataset.q); if(!f) return; const a=b.dataset.qa;
      /* supprimer : un devis qui ne sert à rien disparaît pour de bon. Pas de stock derrière,
         pas de paiement — rien à défaire. Un devis déjà converti garde sa facture : il s'archive. */
      if(a==='sup'){ if(f.doc.converti) return;
        if(!confirm(vf('Supprimer le devis '+f.doc.num+(f.tiers?' ('+f.tiers+')':'')+' ?\n\nIl disparaîtra de la liste, pour tout le monde. Cela ne peut pas être annulé.'))) return;
        const i=FACT.findIndex(x=>x.id===f.id); if(i>=0) FACT.splice(i,1); ecrit(KFACT,FACT);
        try{ const J=lit(KJOU,[]); J.push({t:new Date().toISOString(),u:USR||'(non renseigné)',act:'vente',lib:'devis '+f.doc.num+' supprimé'+(f.tiers?' — '+f.tiers:''),n:0,impact:0,det:[]}); ecrit(KJOU,J); }catch(e){}
        if(Q_OUVERT===f.id) Q_OUVERT=''; peintDocs(); return; }
      if(a==='arch'||a==='desarch'){ docMaj(f,x=>{ if(a==='arch') x.doc.archive=true; else delete x.doc.archive; });
        try{ const J=lit(KJOU,[]); J.push({t:new Date().toISOString(),u:USR||'(non renseigné)',act:'vente',lib:'devis '+f.doc.num+(a==='arch'?' archivé':' désarchivé')+(f.tiers?' — '+f.tiers:''),n:0,impact:0,det:[]}); ecrit(KJOU,J); }catch(e){}
        peintDocs(); return; }
      if(a==='modif'){ ouvreModif(f); return; }
      if(a==='fus'){ fusionneCotes(f); return; }
      dessineDoc(FACT.find(x=>x.id===f.id)||f);
      if(a==='conv') setTimeout(()=>$('doc-conv').click(),150);
      else if(a==='wa') setTimeout(()=>$('doc-wa').click(),150);
      else if(a==='mail') setTimeout(()=>$('doc-mail').click(),150);
    });
  };
  try{ DOCS_F='devis'; peintDocs(); }catch(e){}
  try{ lscInit(); }catch(e){ try{ console.error('cotes Lightspeed :',e); }catch(_){} }
  /* le devis emis et refermé : on repart propre pour le suivant */
  $('doc-x').addEventListener('click',()=>{ try{ ouvreVente(); }catch(e){} });
  /* depuis le document ouvert d'une cote : « Modifier les parfums et les prix » le rouvre dans le formulaire */
  { const bl=$('doc-lignes'); if(bl) bl.onclick=()=>{ const f=DOC; if(!f) return; $('doc-x').click(); ouvreModif(f); }; }
},0);
$('sfoot').innerHTML=`${nf(V.length)} lignes de vente<br>${CANAUX.filter(c=>c!==NP).length} canaux`;
dessine();
peintFile();
/* 7 nov. 2026 : depuis Tâches, une vente en attente à compléter, dans une fenêtre (ventes.html#attente=<id>&cadre=1) */
try{ const ma=location.hash.match(/[#&]attente=([^&]+)/); if(ma&&document.documentElement.classList.contains('cadre')){
  document.addEventListener('click',e=>{ const a=e.target.closest&&e.target.closest('a[href]'); if(a&&!a.target&&!/^#/.test(a.getAttribute('href')||'')){ a.target='_blank'; a.rel='noopener'; } },true);
  setTimeout(()=>{ try{ ouvreAttente(decodeURIComponent(ma[1])); }catch(e){} document.documentElement.classList.add('cp'); },60); } }catch(e){}
/* une facture demandée par l'adresse (depuis la rubrique Factures) : ventes.html#doc=<id> */
try{ const m=location.hash.match(/doc=([^&]+)/); if(m){ const f=FACT.find(x=>x.id===decodeURIComponent(m[1])); if(f&&f.doc) setTimeout(()=>{ dessineDoc(f); if(/edit=1/.test(location.hash)) setTimeout(()=>{ const b=$('doc-edit'); if(b) b.click(); },200); },300); } }catch(e){}
/* tout ce qui est arrivé est maintenant sous les yeux : la pastille « nouvelles ventes » s'éteint */
try{ if(typeof mnVentesVues==='function') mnVentesVues(); }catch(e){}
/* pour les tests : de quoi lire l'état sans passer par l'écran */
window.__V={litFile,litAttente,peintFile,enregistreFile,qteEff,cleDeBC,lit,ecrit,KFILE};
'''+_facture.JS

# r[4] = le TYPE (EDT, EDP, OIL, SET…). Il était dans les données depuis le
# début et n'arrivait jamais à l'écran : Sam ne voyait pas s'il vendait
# l'eau de toilette ou l'eau de parfum du même parfum. Ajouté en 9.
# r[5] = le GENRE (M/W/U/K), demandé dans la foulée. Ajouté en 10.
_IDX = 'Object.fromEntries(D_TOUS().map(r=>[r[15],[r[0],r[13],r[2],r[3],r[12],r[7],r[8],r[6],r[9],r[4],r[5]]]))'
# 25 oct. 2026 (Igal : « cette partie est vraiment vilaine, fais-moi quelque chose de mieux avec les vrais logos ») : les logos
# déposés dans logos/ (fichiers officiels fournis par Igal, jamais dessinés par l'outil) sont incorporés dans la page.
import base64 as _b64, glob as _glob, os as _os, json as _json
_logos = {}
for _f in sorted(_glob.glob('logos/*.png')) + sorted(_glob.glob('logos/*.svg')):
    _id = _os.path.splitext(_os.path.basename(_f))[0]
    if _id in _logos: continue
    _logos[_id] = 'data:' + ('image/png' if _f.endswith('.png') else 'image/svg+xml') + ';base64,' + _b64.b64encode(open(_f, 'rb').read()).decode()
JS = JS.replace('__LOGOS_V__', _json.dumps(_logos))
CADRE_TETE='<script>/* 7 nov. 2026 : ouverte dans une fenêtre depuis Tâches (#attente=…&cadre=1) : le corps reste caché jusqu\'à ce que la fiche soit ouverte (classe « cp »), avec une sécurité de 4 s */try{if(/[#&]cadre=1/.test(location.hash)&&window.parent!==window){document.documentElement.classList.add(\'cadre\');setTimeout(function(){document.documentElement.classList.add(\'cp\');},4000);}}catch(e){}</script>'
html = coquille("Journal des ventes", "Ventes",
    "Chaque produit vendu, avec le canal d'où vient la vente : Lightspeed, perfumestrade.com, "
    "wholesale.perfumestrade.com, Amazon, vente en gros. Chiffre d'affaires et marge par canal, et la saisie "
    "d'une vente à la main.",
    CSS + CSS_QUOTES, CORPS.replace('__ACCEPT__', _lire.ACCEPT), JS.replace('__NOMS__', _noms.NOMS).replace('__MODE__', 'ventes'), donnees=('produits','clients','retail','histgros'))
html = html.replace('__IDX__', _IDX).replace('<head><meta charset="utf-8">', '<head><meta charset="utf-8">' + CADRE_TETE, 1)
open('ventes.html','w').write(html)
print('ventes.html', len(html)//1024, 'Ko')

# La rubrique Quotes : meme page, autre porte. Le client, sa liste, le devis, l'envoi.
html = coquille("Devis", "Devis",
    "Faire un devis (à la main, ou depuis le message WhatsApp du client) et retrouver ceux de la caisse Lightspeed : "
    "convertir en vente (payé Zelle, sort du stock), envoyer par e-mail, imprimer, archiver.",
    CSS + CSS_QUOTES, CORPS.replace('__ACCEPT__', _lire.ACCEPT), JS.replace('__NOMS__', _noms.NOMS).replace('__MODE__', 'quotes'), donnees=('produits','clients','retail','histgros'))
html = html.replace('__IDX__', _IDX)
open('quotes.html','w').write(html)
print('quotes.html', len(html)//1024, 'Ko')
