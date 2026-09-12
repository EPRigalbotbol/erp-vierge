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

.tbl{width:100%;border-collapse:collapse;font-size:13px;background:var(--surface);
border:1px solid var(--line);border-radius:9px;overflow:hidden}
.tbl th{text-align:left;font-family:Inter,sans-serif;font-size:9.5px;letter-spacing:.11em;
text-transform:uppercase;color:var(--ink-2);font-weight:700;padding:11px 12px;
background:var(--surface-2);border-bottom:1px solid var(--line);white-space:nowrap}
.tbl th.r,.tbl td.r{text-align:right;font-variant-numeric:tabular-nums}
.tbl td{padding:10px 12px;border-bottom:1px solid var(--line-2);vertical-align:middle}
.tbl tbody tr:last-child td{border-bottom:0}
.tbl tbody tr:hover{background:var(--surface-2)}
.tbl tfoot td{background:var(--surface-2);font-weight:700;border-top:2px solid var(--line)}
.qd{font-family:Inter,sans-serif;font-size:12.5px;font-weight:600;white-space:nowrap;color:var(--ink)}
.qd small{display:block;font-weight:400;font-size:11px;color:var(--ink-3)}
.ref b{display:block;font-weight:600;line-height:1.3}
.ref span{color:var(--ink-3);font-family:Inter,sans-serif;font-size:11px}
.num{font-family:Inter,sans-serif;font-size:11.5px;color:var(--ink-2);white-space:nowrap}
.num small{display:block;color:var(--ink-3)}
.who{font-size:12px;color:var(--ink-2);white-space:nowrap}
.who.anon{color:var(--ink-3);font-style:italic}
.mt{font-weight:700;color:var(--ink)}
.mg{font-family:Inter,sans-serif;font-weight:700;font-size:12.5px;white-space:nowrap}
.mg.g{color:var(--good)} .mg.w{color:var(--warn)} .mg.c{color:var(--crit)} .mg.na{color:var(--ink-3);font-weight:400}

/* pastille de canal : une couleur par canal, stable */
.ch{display:inline-flex;align-items:center;gap:6px;font-size:11.5px;font-weight:700;
padding:4px 10px 4px 8px;border-radius:20px;white-space:nowrap;line-height:1;letter-spacing:.01em;
background:var(--surface-2);color:var(--ink-2);border:1px solid var(--line)}
.ch::before{content:"";width:7px;height:7px;border-radius:50%;background:var(--c,var(--ink-3))}
.ch.c0{--c:#5B4B8A}.ch.c1{--c:#2C6E4E}.ch.c2{--c:#B4530A}.ch.c3{--c:#1F6FB2}.ch.c4{--c:#A4262C}
.ch.c5{--c:#8A5A00}.ch.c6{--c:#4C7C8A}.ch.c7{--c:#7A4E9E}.ch.na{--c:transparent;border-style:dashed;color:var(--ink-3);font-weight:500}

.par{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:10px;margin-bottom:6px}
.pc{background:var(--surface);border:1px solid var(--line);border-radius:9px;padding:13px 15px;
display:flex;flex-direction:column;gap:8px;cursor:pointer;transition:border-color .12s}
.pc:hover{border-color:var(--iris)}
.pc.on{border-color:var(--iris);box-shadow:0 0 0 3px var(--iris-soft)}
.pc .t{display:flex;justify-content:space-between;align-items:center;gap:8px}
.pc .t .pct{font-family:Inter,sans-serif;font-size:11.5px;color:var(--ink-3);font-weight:600}
.pc .ca{font-family:Inter,sans-serif;font-size:22px;font-weight:700;letter-spacing:-.03em;line-height:1}
.pc .d{font-size:11.5px;color:var(--ink-2);line-height:1.5}
.pc .bar{height:4px;border-radius:2px;background:var(--line-2);overflow:hidden}
.pc .bar i{display:block;height:100%;background:var(--c,var(--iris))}
.pc.c0{--c:#5B4B8A}.pc.c1{--c:#2C6E4E}.pc.c2{--c:#B4530A}.pc.c3{--c:#1F6FB2}.pc.c4{--c:#A4262C}
.pc.c5{--c:#8A5A00}.pc.c6{--c:#4C7C8A}.pc.c7{--c:#7A4E9E}.pc.na{--c:var(--ink-3)}

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
font-size:11.5px;font-variant-numeric:tabular-nums;padding-right:6px}


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
.dov{position:fixed;inset:0;background:rgba(23,23,29,.42);z-index:85;display:none}
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
.qd .hh{font-size:11px;color:var(--ink-3);font-variant-numeric:tabular-nums}
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
.tbl td.act button{font-family:inherit;font-size:12px;font-weight:600;color:var(--ink-2);background:var(--surface);
border:1px solid var(--line);border-radius:6px;padding:5px 10px;cursor:pointer}
.tbl td.act button:hover{border-color:var(--crit);color:var(--crit)}
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
body.quotes #vov{position:static;display:block;background:none;padding:0;overflow:visible;margin:0 0 26px}
body.quotes #vov .mod{max-width:none;width:auto;margin:0;box-shadow:none;border:1px solid var(--line);border-radius:12px;max-height:none}
body.quotes #vov .mh h3::after{content:''}
body.quotes #vx{display:none}
body.quotes #v-liste{margin-left:auto;background:var(--iris);color:#fff;border-color:var(--iris)}
body.quotes #v-stock,body.quotes #v-stock+span{display:none}
body.quotes #v-num,body.quotes #v-num+*{display:none}
body.quotes #v-ok{background:var(--iris);color:#fff;border-color:var(--iris)}
body.quotes #m-att{display:none}
body.quotes .hact #msgb,body.quotes .hact #nv{display:none}
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
.qdet .lg{display:grid;grid-template-columns:34px 1fr auto auto;gap:6px 12px;align-items:baseline;padding:7px 0;border-bottom:1px solid var(--line-2)}
.qdet .lg b{font-weight:600}.qdet .lg small{color:var(--ink-3)}
.qdet .tot{margin-top:10px;display:grid;grid-template-columns:1fr auto;gap:4px 24px;max-width:420px;margin-left:auto}
.qdet .tot .tt{font-weight:800;border-top:1px solid var(--ink);padding-top:8px;margin-top:4px}
.qdet .note{margin-top:12px;font-size:13px;color:var(--ink-2)}.qdet .note b{color:var(--ink)}
.qdet .btns{display:flex;flex-direction:column;gap:8px}.qdet .btns .btn{width:100%;text-align:center}
.qdet .btns .btn.pri{background:var(--iris);color:#fff;border-color:var(--iris)}
'''

CORPS = r'''
<div class="info"><b>D'où viennent ces lignes.</b> Trois façons : le bouton <b>+ Enregistrer une vente</b>
en haut de la page (on scanne ou on tape les parfums, on choisit le canal, le stock se met à jour) ; une
<b>facture de vente</b> enregistrée dans la rubrique Factures ; un <b>fichier de ventes importé</b> d'un canal
(Shopify, Amazon, WooCommerce, caisse) déposé dans cette même rubrique. Une vente qui ne passe par aucune
des trois n'existe pas pour l'outil.</div>

<div id="file"></div>

<div id="kpis"></div>

<h2 class="sec">Par canal <em id="nbc"></em></h2>
<div class="par" id="par"></div>

'''+_facture.LISTE+r'''
<h2 class="sec">Toutes les ventes <em id="nbv"></em></h2>
<div class="tools">
  <div class="srch"><input id="q" autocomplete="off" placeholder="Chercher un produit, un client, un numéro…"></div>
  <select id="fc" class="sel"><option value="">Tous les canaux</option></select>
  <select id="fp" class="sel">
    <option value="">Depuis toujours</option><option value="1">Aujourd'hui</option>
    <option value="7">7 derniers jours</option><option value="30" selected>30 derniers jours</option>
    <option value="90">90 derniers jours</option><option value="365">12 mois</option>
  </select>
  <span class="sp"></span>
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
window.__nomChange.push(v=>{ USR=v; try{ majUser(); }catch(e){} });
let REG={margeMin:10}; try{ REG=Object.assign(REG,JSON.parse(localStorage.getItem(KREG)||'{}')); }catch(e){}
let MOD=lit(KMOD,{}); if(!MOD||typeof MOD!=='object') MOD=base(KMOD,{});
let EXT={q:{}}; try{ EXT=Object.assign({q:{}},JSON.parse(localStorage.getItem(KEXT)||'{}')); }catch(e){}
/* le stock et le prix d'achat réellement en vigueur : la fiche corrigée l'emporte sur le fichier */
const qteEff=cle=>{ const m=MOD[cle]; if(m&&m.qte!=null) return +m.qte;
  const bc=(IDX[cle]||[])[0]; const e=EXT.q[bc]; return e!=null?+e:((IDX[cle]||[])[7]||0); };
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
  for(const cle in IDX){ if(String((IDX[cle]||[])[0]||'').replace(/^0+/,'')===n) return cle; }
  for(const cle in MOD){ const m=MOD[cle];
    if(m&&m.bcs&&String(m.bcs).split(/[^0-9]+/).map(x=>x.replace(/^0+/,'')).includes(n)) return cle; }
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
    return {cle:'',cands:r.cands.filter(c=>c.sc>=0.4&&IDX[c.cle]).slice(0,4)};
  }catch(e){ return {cle:'',cands:[]}; }
}
/* le nom complet du catalogue (« Chanel Bleu edp 3.4 »), pas le nom court des
   listes (« Chanel Bleu ») qui ne distingue pas l'EDP de l'EDT */
let _NOMC=null;
function fNomComplet(cle){
  if(!_NOMC){ _NOMC={}; try{ D_TOUS().forEach(r=>{ if(r[15]) _NOMC[r[15]]=(r[2]||'')+' '+(r[1]||''); }); }catch(e){} }
  return _NOMC[cle]||((IDX[cle]||[])[2]+' '+(IDX[cle]||[])[1]);
}
function fApprend(des,cle){
  try{ const A=lit(K_ALIASN,{}); const M=(A&&typeof A==='object'&&!Array.isArray(A))?A:{}; const k=mNorm(des); if(!k) return; M[k]=cle; ecrit(K_ALIASN,M); }catch(e){}
}
function litAttente(v){
  const L=(v.lignes||[]).map(l=>{ let cle=cleDeBC(l.bc), cands=[], par='';
    if(!cle){ const n=fParNom(l.des); if(n.cle){ cle=n.cle; par='appris'; } else cands=n.cands; }
    const q=+l.q||0;
    const qAv=cle?qteEff(cle):null;
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
function peintFile(){
  const el=$('file'); if(!el) return;
  const F=litFile();
  if(!F.length){ el.innerHTML=''; return; }
  const A=F.map(litAttente);
  const tot=A.reduce((a,x)=>a+x.montant,0);
  const nInc=A.filter(x=>x.inconnues.length).length;
  const aDecouvert=A.filter(x=>!x.inconnues.length&&x.manquants>0);
  const totManque=aDecouvert.reduce((a,x)=>a+x.manquants,0);
  const SRC={woocommerce:'Site','woocommerce-gros':'Site gros',lightspeed:'Caisse',shopify:'Shopify',amazon:'Amazon',message:'Message client'};
  el.innerHTML=`<div class="file">
    <div class="ft">
      <b>${nf(F.length)} vente${F.length>1?'s':''} en attente</b>
      <span style="color:var(--ink-2)">${money(tot)}</span>
      <span class="sp"></span>
      <button class="btn" id="f-vider">Tout ignorer</button>
      <button class="btn pri" id="f-ok">Enregistrer ${nf(F.length-nInc>0?F.length-nInc:0)} vente${F.length-nInc>1?'s':''}</button>
      <span class="aide">Le site et la caisse les ont déposées ici. Elles n'ont encore touché à rien :
      le stock ne bougera qu'une fois enregistrées. Le bouton vert de chaque ligne n'enregistre
      que cette vente-là : si une commande te paraît fausse, prends les autres et laisse-la ici.${nInc?` <b>${nf(nInc)} contien${nInc>1?'nent':'t'} un code-barres inconnu du catalogue</b> — celles-là restent en attente
      tant que la référence n'existe pas ici. Quand le nom ressemble à un parfum du catalogue, l'outil te le propose sous la ligne :
      choisis-le une fois, il s'en souviendra.`:''}</span>
      ${aDecouvert.length?`<span class="dec"><b>${nf(aDecouvert.length)} vente${aDecouvert.length>1?'s':''} porte${aDecouvert.length>1?'nt':''} sur du stock que l'outil n'a pas</b> —
        ${nf(totManque)} flacon${totManque>1?'s':''} de plus que ce qui est compté ici. Elles seront enregistrées quand même :
        la vente a eu lieu. Le stock concerné tombera à zéro, et l'écart part au journal.
        Si le chiffre te surprend, c'est l'inventaire de l'outil qu'il faut regarder, pas le site.</span>`:''}
    </div>
    <table><thead><tr><th>Quand</th><th>D'où</th><th>N°</th><th>Client</th><th>Contenu</th>
      <th class="r">Montant</th><th class="r"></th></tr></thead><tbody>
      ${A.slice(0,40).map((x,i)=>`<tr>
        <td>${esc(x.v.d||'')}</td>
        <td><span class="src">${esc(SRC[x.v.src]||x.v.src||'')}</span>${x.v.lieu?`<span class="lg">${esc(x.v.lieu)}</span>`:''}</td>
        <td>${esc(x.v.num||'—')}</td>
        <td>${esc(x.v.client||'—')}</td>
        <td>${x.v.annule?'<span class="ret">retour</span> · ':''}${nf(x.L.length)} ligne${x.L.length>1?'s':''}
          ${x.inconnues.length?`<span class="inc">· ${nf(x.inconnues.length)} inconnue${x.inconnues.length>1?'s':''}</span>`:''}
          ${x.manquants?`<span class="mq">· ${nf(x.manquants)} flacon${x.manquants>1?'s':''} de plus que le stock</span>`:''}
          <span class="lg">${x.L.slice(0,3).map(l=>esc((l.cle?((IDX[l.cle]||[])[2]+' '+(IDX[l.cle]||[])[1]):(l.des||l.bc))+' ×'+l.q)).join(' · ')}${x.L.length>3?' …':''}</span>
          ${x.v.annule?`<span class="prop"><b>Motif</b> <select data-fmotif="${esc(x.v._i)}">${MOTIFS_R.map(([k,l])=>`<option value="${k}"${k===x.motif?' selected':''}>${esc(l)}</option>`).join('')}</select>
            ${x.orig?`· rattaché à la vente <b>${esc(x.orig.num)} du ${dfr(x.orig.d)}</b> — le stock revient`:`· <b>vente d'origine inconnue ici</b> — le stock ne bougera pas`}</span>`:''}
          ${x.inconnues.map((l,j)=>`<span class="prop"><b>${esc(l.des||l.bc||'?')}</b>${l.bc?` <small>(${esc(l.bc)})</small>`:''} → ${l.cands.length?`<select data-fnom="${esc(x.v._i)}" data-fdes="${esc(l.des)}"><option value="">c'est lequel ?</option>${l.cands.map(c=>`<option value="${esc(c.cle)}">${esc(fNomComplet(c.cle))}</option>`).join('')}</select>`:'<small>aucun parfum du catalogue ne ressemble à ce nom</small>'}</span>`).join('')}</td>
        <td class="r">${money2(x.montant)}</td>
        <td class="r">${x.inconnues.length?'':`<button class="btn sm pri" data-fok="${esc(x.v._i)}" title="Enregistrer seulement cette vente, et laisser les autres en attente">Enregistrer</button> `}<button class="btn sm" data-fsup="${esc(x.v._i)}" title="Retirer cette vente de la file sans l'enregistrer">Ignorer</button></td>
      </tr>`).join('')}
    </tbody></table>
    ${A.length>40?`<div style="padding:9px 14px;color:var(--ink-3);font-size:12.5px">et ${nf(A.length-40)} de plus…</div>`:''}
  </div>`;
  $('f-ok').disabled = (F.length-nInc)<=0;
  $('f-ok').onclick=()=>enregistreFile();
  $('f-vider').onclick=videFile;
  el.querySelectorAll('[data-fsup]').forEach(b=>b.onclick=()=>retireDeFile([b.dataset.fsup],'ignorée'));
  el.querySelectorAll('[data-fok]').forEach(b=>b.onclick=()=>enregistreFile([b.dataset.fok]));
  el.querySelectorAll('[data-fmotif]').forEach(sl=>sl.onchange=()=>{ MOTIF_F[sl.dataset.fmotif]=sl.value; });
  el.querySelectorAll('[data-fnom]').forEach(sl=>sl.onchange=()=>{ const cle=sl.value; if(!cle) return;
    fApprend(sl.dataset.fdes,cle);
    try{ const J=lit(KJOU,[]); J.push({t:new Date().toISOString(),u:USR||'(non renseigné)',act:'vente',lib:'nom reconnu : « '+sl.dataset.fdes+' » = '+fNomComplet(cle),ref:cle,av:null,ap:null}); ecrit(KJOU,J); }catch(e){}
    peintFile(); });
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
function enregistreFile(seulement){
  const S = Array.isArray(seulement) && seulement.length ? new Set(seulement) : null;
  const A=litFile().map(litAttente)
    .filter(x=>!x.inconnues.length&&x.L.length)
    .filter(x=>!S||S.has(x.v._i));
  if(!A.length) return;
  /* Ce qui se vend à découvert doit être dit AVANT, pas découvert après. */
  const dec=A.filter(x=>x.manquants>0), totM=dec.reduce((a,x)=>a+x.manquants,0);
  if(dec.length && !confirm(
      dec.length+' vente'+(dec.length>1?'s':'')+' porte'+(dec.length>1?'nt':'')+
      ' sur '+totM+' flacon'+(totM>1?'s':'')+" de plus que ce que l'outil compte en stock.\n\n"+
      "Elles seront enregistrées : la vente a bien eu lieu. Le stock de ces références tombera à zéro,\n"+
      "et l'écart sera inscrit au journal pour qu'on puisse le retrouver.\n\n"+
      "Continuer ?")) return;
  if(!signe(A.length>1?"ces ventes":"cette vente",()=>enregistreFile(seulement))) return;
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
      const lignes=x.L.map(l=>{ const n=Math.abs(l.q); const qAv=qteEff(l.cle); let qAp=qAv;
        if(o){ const lo=(o.lignes||[]).find(z=>z.cle===l.cle);
          const sorti=lo?Math.max(0,(lo.qAv==null||lo.qAp==null)?(lo.q||0):(lo.qAv-lo.qAp)):0;
          qAp=qAv+Math.min(n,Math.max(0,sorti-(rendu[l.cle]||0))); }
        if(qAp!==qAv) MOD[l.cle]=Object.assign({},MOD[l.cle]||{},{qte:qAp});
        nL++; mt-=n*(l.p||0);
        const ref=((IDX[l.cle]||[])[2]||'')+' '+((IDX[l.cle]||[])[1]||'');
        (VENT[l.cle]=VENT[l.cle]||[]).push({d:v.d,h:v.h||undefined,p:l.p,c:v.client||'',q:-n,num:(o?o.num:v.num||'')+' (remboursé)',k:canal});
        return {cle:l.cle,bc:l.bc,ref,q:-n,p:l.p,qAv,qAp,paAv:o?((o.lignes||[]).find(z=>z.cle===l.cle)||{}).paAv:paEff(l.cle)}; });
      const mtR=lignes.reduce((a,l)=>a+Math.abs(l.q)*(l.p||0),0);
      const nR=o?FACT.filter(z=>z.retour&&z.refId===o.id).length+1:1;
      const num=(o?o.num:(v.num||'AUTO'))+'-R'+nR;
      FACT.push({id:'r'+Date.now().toString(36)+Math.random().toString(36).slice(2,5),num,sens:'vente',retour:true,
        refId:o?o.id:'',refNum:o?o.num:(v.num||''),canal,tiers:v.client||(o?o.tiers:'')||'',d:v.d||ajd(),h:v.h||undefined,lignes,
        montant:-mtR,stock:!!o,mode:x.motif==='annulation'?'aucun':'carte',motif:x.motif,
        note:(SRC[v.src]||v.src||'')+(o?'':" — vente d'origine inconnue ici, stock inchangé"),
        par:USR||'(automatique)',t:new Date().toISOString(),auto:v.src||''});
      retours.push({num,mt:mtR,orig:!!o,motif:x.motif});
      faits.push(v._i);
      return;
    }
    const lignes=x.L.map(l=>{ const qAv=qteEff(l.cle), qAp=Math.max(0,qAv-l.q);
      MOD[l.cle]=Object.assign({},MOD[l.cle]||{},{qte:qAp});
      nL++; mt+=l.q*(l.p||0);
      const ref=((IDX[l.cle]||[])[2]||'')+' '+((IDX[l.cle]||[])[1]||'');
      (VENT[l.cle]=VENT[l.cle]||[]).push({d:v.d,h:v.h||undefined,p:l.p,c:v.client||'',q:l.q,num:v.num||'',k:canal});
      if(l.manque) ecarts.push({num:v.num||'',bc:l.bc,ref,vendu:l.q,stock:qAv,manque:l.manque});
      return {cle:l.cle,bc:l.bc,ref,q:l.q,p:l.p,qAv,qAp,paAv:paEff(l.cle),manque:l.manque||undefined}; });
    if(v.client && !CLI[v.client]) CLI[v.client]={nom:v.client,depuis:v.d||''};
    FACT.push({id:'c'+Date.now().toString(36)+Math.random().toString(36).slice(2,5),
      num:(v.num||('AUTO-'+Date.now().toString(36))),sens:'vente',canal,export:canal,
      tiers:v.client||'',d:v.d||ajd(),h:v.h||undefined,lignes,
      montant:x.montant,stock:true,par:USR||'(automatique)',t:new Date().toISOString(),
      auto:v.src||''});
    faits.push(v._i);
  });
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

/* ---------------- les canaux de vente et leur commission ---------------- */
const CANAUX_DEF=[{id:'boutique',nom:'Boutique',maj:0,com:0},{id:'site',nom:'Site perfumestrade.com',maj:0,com:3},
  {id:'shopify',nom:'Shopify',maj:0,com:3},{id:'amazon',nom:'Amazon',maj:18,com:15},
  {id:'perfumecity',nom:'Perfume City',maj:0,com:0}];
const canauxReg=()=>(REG.canaux&&REG.canaux.length?REG.canaux:CANAUX_DEF);
/* la vente en gros et la caisse ne sont pas des canaux de prix : ce sont des façons de vendre */
const CANAUX_VENTE=()=>[...canauxReg().map(c=>({id:c.id,nom:c.nom,com:c.com||0,maj:c.maj||0})),
  {id:'gros',nom:'Gros',com:0,maj:0},{id:'caisse',nom:'Caisse Lightspeed',com:0,maj:0},{id:'autre',nom:'Autre',com:0,maj:0}];
/* La marge affichée est la marge NETTE : ce qui reste une fois la commission du canal
   prélevée. Amazon garde 15 %, Shopify et le site 3 %. La commission est retrouvée par le
   nom du canal enregistré sur la vente. Si ce nom ne correspond à aucun canal des Réglages
   (canal renommé ou supprimé depuis), on ne devine pas : la commission vaut 0 et la vente
   est signalée, plutôt que de voir la marge de tout l'historique bouger en silence. */
let CANAL_INCONNU=new Set();
function comCanal(nom){
  if(!nom||nom===NP) return 0;
  const L=CANAUX_VENTE();
  const c=L.find(x=>String(x.nom).toLowerCase()===String(nom).toLowerCase());
  if(c) return +c.com||0;
  if(!['gros','caisse','autre','divers'].includes(String(nom).toLowerCase())) CANAL_INCONNU.add(nom);
  return 0;
}

/* Une ligne par produit vendu. Un export de canal porte le détail de chaque commande :
   on éclate alors par commande, avec sa propre date et son propre client. */
let V=[];
function construitV(){
V=[]; CANAL_INCONNU=new Set();
FACT.filter(f=>f.sens==='vente').forEach(f=>{
  const canal=f.canal||NP;
  (f.lignes||[]).forEach(l=>{
    /* l'heure de la vente : celle notée avec elle ; pour une vente saisie à la
       main avant qu'on la note, l'heure de la saisie (à Miami) en tient lieu.
       Un fichier importé n'en a pas forcément : on ne l'invente pas. */
    const hF = f.h || (!f.export && f.t ? heureMiami(f.t) : '');
    const base={canal,num:f.num,ref:l.ref,bc:l.bc,pa:l.paAv,par:f.par,t:f.t,fid:f.id,exp:!!f.export,
                ret:!!f.retour,refNum:f.refNum,mode:f.mode,motif:f.motif,manuel:!!f.manuel,h:hF};
    if(l.cmds&&l.cmds.length){
      l.cmds.forEach(c=>V.push(Object.assign({},base,{d:c.d||f.d,h:c.h||'',cmd:c.cmd||'',client:c.client||'',q:c.q||0,p:c.p!=null?c.p:l.p})));
    } else V.push(Object.assign({},base,{d:f.d,cmd:'',client:f.export?'':(f.tiers||''),q:l.q||0,p:l.p}));
  });
});
V.forEach(v=>{ v.mt=(v.q||0)*(v.p||0);
  v.com=comCanal(v.canal);
  /* Sur un remboursement, la plateforme ne rend PAS sa commission : elle l'a déjà prise.
     La perte est donc le montant entier rendu au client, pas le montant moins la commission.
     (Amazon en rembourse une partie ; tant qu'on n'a pas ses conditions exactes, on compte
     le cas défavorable plutôt que d'annoncer une perte trop faible.) */
  v.comMt = v.ret ? 0 : v.mt*v.com/100;           /* ce que la plateforme prend, en dollars */
  v.net = v.mt - v.comMt;                         /* ce qui reste après la commission */
  v.mg=(v.pa!=null&&v.p!=null)?(v.net-v.pa*(v.q||0)):null;
  v.pct=(v.pa!=null&&v.mt!==0)?v.mg/Math.abs(v.mt)*100:null; });
V.sort((a,b)=>(b.d||'').localeCompare(a.d||'')||(b.t||'').localeCompare(a.t||''));
}
construitV();

let CANAUX=[...new Set(V.map(v=>v.canal))].sort((a,b)=>a===NP?1:b===NP?-1:a.localeCompare(b));
const cls=c=>c===NP?'na':'c'+(CANAUX.filter(x=>x!==NP).indexOf(c)%8);
const dfr=d=>{ if(!d) return '—'; const [a,m,j]=d.split('-'); return `${j}/${m}/${a.slice(2)}`; };
const pc=v=>v==null?'—':(v<0?'−':'')+Math.abs(v).toFixed(1).replace('.',',')+' %';
const mcls=v=>v==null?'na':v<0?'c':v<REG.margeMin?'w':'g';

function periode(){
  const p=$('fp').value; if(!p) return null;
  const d=new Date(); d.setHours(0,0,0,0); d.setDate(d.getDate()-(+p-1));
  return isoJour(d);
}
function filtre(avecCanal){
  const q=$('q').value.trim().toLowerCase(), lim=periode();
  return V.filter(v=>{
    if(lim && (v.d||'')<lim) return false;
    if(avecCanal && canalSel && v.canal!==canalSel) return false;
    if(q){ const t=(v.ref+' '+v.bc+' '+v.client+' '+v.num+' '+v.cmd+' '+v.canal).toLowerCase(); if(!t.includes(q)) return false; }
    return true;
  });
}
const somme=(L,k)=>L.reduce((a,v)=>a+(v[k]||0),0);

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

function fermeDetail(){ $('dov').classList.remove('on'); DETAIL=null; }

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

  $('d-tit').innerHTML=`${esc(x.ref||'—')}
    <span class="sub"><span class="ch ${cls(x.canal)}">${esc(x.canal)}</span>
    ${dfr(x.d)} · ${esc(x.cmd||x.num||'')}${x.bc?' · code-barres '+esc(x.bc):''}
    ${x.ret?'<br><b style="color:var(--crit)">Ceci est un remboursement</b>':''}</span>`;

  const l=[];

  /* ---- cette ligne ---- */
  l.push(`<div class="blo"><h4>Cette ligne</h4>
    <div class="pl"><span>${nf(x.q)} flacon${Math.abs(x.q)>1?'s':''} à ${x.p!=null?money2(x.p):'prix inconnu'}</span><b>${money2(x.mt)}</b></div>
    ${x.comMt?`<div class="pl"><span>Commission ${esc(x.canal)} · ${x.com} %</span><b style="color:var(--crit)">−${money2(x.comMt)}</b></div>
      <div class="pl"><span>Encaissé après commission</span><b>${money2(x.net)}</b></div>`:''}
    ${x.pa!=null
      ? `<div class="pl"><span>Prix d'achat retenu · ${money2(x.pa)} le flacon</span><b style="color:var(--crit)">−${money2(x.pa*(x.q||0))}</b></div>
         <div class="pl gr"><span>Marge</span><b class="mg ${mcls(x.pct)}">${money2(x.mg)}${x.pct!=null?' · '+pc(x.pct):''}</b></div>`
      : `<div class="pl gr"><span>Marge</span><b>—</b></div>`}
    ${x.pa==null
      ? `<p class="nt"><b>Le prix d'achat n'était pas connu au moment de cette vente</b>, donc la marge
         n'est pas calculée — et cette ligne ne compte pas dans le taux de marge affiché en haut.
         Corrige le prix d'achat dans la fiche du parfum : les ventes suivantes seront justes,
         celle-ci restera sans marge (on ne réécrit pas le passé).</p>`
      : (paNow!=null && Math.abs(paNow-x.pa)>0.005
         ? `<p class="nt">Le prix d'achat de ce parfum <b>vaut ${money2(paNow)} aujourd'hui</b>.
            La marge ci-dessus garde ${money2(x.pa)}, le prix au jour de la vente. C'est voulu :
            un achat renégocié le mois dernier ne doit pas changer la marge d'une vente de janvier.</p>`
         : '')}
  </div>`);

  /* ---- la vente entière ---- */
  l.push(`<div class="blo"><h4>${x.cmd?'La commande entière':'La vente entière'} · ${nf(grp.length)} ligne${grp.length>1?'s':''}</h4>
    <table><tbody>${grp.map(z=>`<tr class="${z===x?'ici':''}">
      <td><b>${esc(z.ref||'—')}</b><small>${esc(z.bc||'')}</small></td>
      <td class="r">${nf(z.q)} ×<br><small>${z.p!=null?money2(z.p):'—'}</small></td>
      <td class="r"><b>${money2(z.mt)}</b><small class="mg ${mcls(z.pct)}">${z.mg!=null?money2(z.mg):'marge inconnue'}</small></td>
    </tr>`).join('')}</tbody></table>
    <div class="pl gr" style="margin-top:8px"><span>${nf(uGrp)} flacon${Math.abs(uGrp)>1?'s':''}</span><b>${money2(totGrp)}</b></div>
    ${comGrp?`<div class="pl"><span>dont commission ${esc(x.canal)}</span><b style="color:var(--crit)">−${money2(comGrp)}</b></div>`:''}
    <div class="pl"><span>marge nette de l'ensemble</span><b class="mg ${mgGrp<0?'c':'g'}">${money2(mgGrp)}</b></div>
    ${grp.length===1&&!x.cmd?'<p class="nt">Cette vente ne contenait que ce parfum.</p>':''}
  </div>`);

  /* ---- le paiement ---- */
  if(D){
    l.push(`<div class="blo"><h4>Paiement</h4>
      <div class="pl"><span>${esc(D.type==='devis'?'Devis':'Facture')} ${esc(D.num||'')}</span>
        <b><span class="et ${st==='paye'?'ok':st==='partiel'?'mi':'no'}">${esc(FSTAT[st]||st)}</span></b></div>
      <div class="pl"><span>Total du document</span><b>${money2(D.total)}</b></div>
      ${regs.length?regs.map(r=>`<div class="pl"><span>&nbsp;&nbsp;reçu le ${dfr(r.d)} · ${esc(FMODES[r.m]||r.m||'')}${r.ref?' · '+esc(r.ref):''}</span><b>${money2(r.mt)}</b></div>`).join('')
        :`<div class="pl"><span>Aucun versement enregistré</span><b>—</b></div>`}
      ${(D.reste||0)>0
        ? `<div class="pl gr"><span>Reste dû</span><b style="color:var(--crit)">${money2(D.reste)}</b></div>`
        : `<div class="pl gr"><span>Soldée</span><b class="mg g">${money2(D.regle||D.total)}</b></div>`}
      ${D.fiscal==='exempt'?'<p class="nt">Document marqué exempt de sales tax.</p>':''}
    </div>`);
  } else {
    l.push(`<div class="blo"><h4>Paiement</h4>
      <p class="nt"><b>Aucune facture n'a été émise pour cette vente</b> : elle est entrée
      directement au journal${x.exp?" par l'export d'un canal":(x.manuel?' par saisie manuelle':'')}.
      Le règlement n'est donc pas suivi ici — l'outil ne sait pas si l'argent est rentré.
      ${x.exp?"Pour un canal (Amazon, le site…), c'est normal : la plateforme encaisse pour toi.":
        "Si tu veux suivre le règlement, il faut cocher « Facture » au moment d'enregistrer la vente."}</p>
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

  /* ---- ce parfum ---- */
  if(x.bc){
    l.push(`<div class="blo"><h4>Ce parfum</h4>
      ${stock!=null?`<div class="pl"><span>En stock aujourd'hui</span><b class="${stock<=0?'mg c':''}">${nf(stock)} flacon${Math.abs(stock)>1?'s':''}</b></div>`
        :`<div class="pl"><span>Référence</span><b>inconnue du catalogue</b></div>`}
      <div class="pl"><span>Vendu ${nf(hp.length)} fois${hp.length?', '+nf(somme(hp,'q'))+' flacon(s)':''}</span><b>${money2(somme(hp,'mt'))}</b></div>
      ${pMin!=null&&pMax!=null&&pMax-pMin>0.005?`<div class="pl"><span>Prix pratiqués</span><b>${money2(pMin)} → ${money2(pMax)}</b></div>`:''}
      ${paNow!=null?`<div class="pl"><span>Prix d'achat actuel</span><b>${money2(paNow)}</b></div>`:''}
      ${x.bc?`<button class="btn sm" id="d-bc">Voir toutes ses ventes</button>`:''}
      ${stock===null?'<p class="nt">Ce code-barres ne correspond à aucune fiche du catalogue : le stock ne peut pas être suivi, et la marge non plus.</p>':''}
    </div>`);
  }

  /* ---- la saisie ---- */
  l.push(`<div class="blo"><h4>Saisie</h4>
    <div class="pl"><span>Enregistré par</span><b>${esc(x.par&&x.par!=='(non renseigné)'?x.par:'—')}</b></div>
    <div class="pl"><span>Le</span><b>${x.t?esc(String(x.t).slice(0,10).split('-').reverse().join('/'))+' à '+esc(String(x.t).slice(11,16)):'—'}</b></div>
    <div class="pl"><span>Origine</span><b>${x.exp?'fichier importé':(x.manuel?'saisie manuelle':'facture')}</b></div>
    <div class="pl"><span>Facture interne</span><b>${esc(x.num||'—')}</b></div>
  </div>`);

  $('d-corps').innerHTML=l.join('');
  $('d-pied').innerHTML=`${D?'<button class="btn" id="d-fac">Ouvrir la facture</button>':''}
    ${x.ret?'':`<button class="btn" id="d-ret">Rembourser</button>`}
    <span style="flex:1"></span><button class="btn pri" id="d-ok">Fermer</button>`;

  $('d-ok').onclick=fermeDetail;
  const bf=$('d-fac'); if(bf) bf.onclick=()=>{ fermeDetail(); dessineDoc(f); };
  const br=$('d-ret'); if(br) br.onclick=()=>{ fermeDetail(); ouvreRetour(x.fid); };
  const bc=$('d-cli'); if(bc) bc.onclick=()=>{ fermeDetail(); $('q').value=cli; $('fp').value=''; vus=80; dessine(); };
  const bb=$('d-bc'); if(bb) bb.onclick=()=>{ fermeDetail(); $('q').value=x.bc; $('fp').value=''; vus=80; dessine(); };
  $('d-corps').scrollTop=0;
  $('dov').classList.add('on');
}
$('d-x').onclick=fermeDetail;
$('dov').onclick=e=>{ if(e.target===$('dov')) fermeDetail(); };

function dessine(){
  const P=filtre(true), L=P;                     /* les KPI suivent le filtre affiché : un seul total à l'écran */
  const TOUS=filtre(false);                      /* sert aux parts de CA entre canaux */
  const ca=somme(P,'mt'), mg=somme(P.filter(v=>v.mg!=null),'mg'), u=somme(P,'q');
  const caM=somme(P.filter(v=>v.mg!=null),'mt');
  const comTot=P.reduce((a,v)=>a+(v.comMt||0),0);
  const lib=$('fp').options[$('fp').selectedIndex].textContent.toLowerCase()+(canalSel?' · '+canalSel:'');
  $('kpis').innerHTML=`<div class="kpis">
    <div class="kpi"><span class="v">${nf(P.length)}</span><span class="k">ligne${P.length>1?'s':''} de vente · ${lib}</span></div>
    <div class="kpi"><span class="v">${nf(u)}</span><span class="k">flacon${Math.abs(u)>1?'s':''} vendu${Math.abs(u)>1?'s':''}</span></div>
    <div class="kpi"><span class="v">${money(ca)}</span><span class="k">chiffre d'affaires</span></div>
    <div class="kpi"><span class="v ${mg<0?'c':'g'}">${money(mg)}</span><span class="k">marge nette, commissions déduites${caM<ca?' (sur les ventes à prix d\'achat connu)':''}</span></div>
    <div class="kpi"><span class="v">${caM>0?pc(mg/caM*100):'—'}</span><span class="k">taux de marge nette</span></div>
    ${comTot?`<div class="kpi"><span class="v c">${money(comTot)}</span><span class="k">pris par les plateformes</span></div>`:''}
  </div>`;

  if(CANAL_INCONNU.size){
    const l=[...CANAL_INCONNU];
    $('kpis').insertAdjacentHTML('afterbegin',`<div class="info" style="background:var(--warn-soft);border-left-color:var(--warn)">
      <b>Commission inconnue pour ${l.length>1?'ces canaux':'ce canal'} : ${l.map(esc).join(', ')}.</b>
      ${l.length>1?'Ils ne figurent':'Il ne figure'} plus dans Réglages — renommé ou supprimé depuis ces ventes.
      Leur marge est calculée <b>sans commission</b>, donc surévaluée.
      <a href="reglages.html">Corriger le nom dans Réglages</a>.</div>`);
  }

  /* par canal */
  const parC={};
  TOUS.forEach(v=>{ const c=parC[v.canal]||(parC[v.canal]={n:0,u:0,ca:0,mg:0,caM:0,com:0,cpct:v.com||0}); c.n++; c.u+=v.q||0; c.ca+=v.mt;
    c.com+=v.comMt||0;
    if(v.mg!=null){ c.mg+=v.mg; c.caM+=v.mt; } });
  const caT=somme(TOUS,'mt');
  const cl=Object.entries(parC).sort((a,b)=>b[1].ca-a[1].ca);
  $('nbc').textContent=cl.length?`${cl.length} ${cl.length>1?'canaux':'canal'} · clique pour filtrer`:'';
  $('par').innerHTML=cl.map(([c,x])=>`<div class="pc ${cls(c)}${canalSel===c?' on':''}" data-c="${esc(c)}">
    <div class="t"><span class="ch ${cls(c)}">${esc(c)}</span><span class="pct">${caT>0?Math.round(x.ca/caT*100):0} % du CA</span></div>
    <div class="ca">${money(x.ca)}</div>
    <div class="bar"><i style="width:${caT>0?Math.round(x.ca/caT*100):0}%"></i></div>
    <div class="d">${nf(x.n)} vente${x.n>1?'s':''} · ${nf(x.u)} flacon${x.u>1?'s':''}<br>marge nette <b class="mg ${mcls(x.caM>0?x.mg/x.caM*100:null)}">${money(x.mg)}</b>${x.caM>0?' · '+pc(x.mg/x.caM*100):''}${x.cpct?`<br><span style="color:var(--crit)">${x.cpct} % de commission : −${money(x.com)}</span>`:''}</div>
  </div>`).join('');
  document.querySelectorAll('.pc').forEach(el=>el.onclick=()=>{ canalSel = canalSel===el.dataset.c ? '' : el.dataset.c; $('fc').value=canalSel; vus=80; dessine(); });

  if(!V.length){
    $('corps').innerHTML=`<div class="vide"><h3>Aucune vente enregistrée</h3>
      <p>Le journal se remplit de trois façons : le bouton « + Enregistrer une vente » en haut,
      une facture de vente, ou l'import du fichier de commandes d'un canal. Chaque produit vendu
      arrive ici avec son canal.</p>
      <p><button class="btn pri" onclick="document.getElementById('nv').click()">+ Enregistrer une vente</button>
      <a class="btn" href="factures.html">Importer les ventes d'un canal</a></p></div>`;
    $('nbv').textContent=''; $('src').innerHTML='aucune vente'; return;
  }
  if(!L.length){
    $('corps').innerHTML=`<div class="vide"><h3>Aucune vente ne correspond</h3><p>Élargis la période ou enlève un filtre.</p></div>`;
    $('nbv').textContent=''; $('src').innerHTML=`0 vente affichée<br>sur ${nf(V.length)} au total`; return;
  }
  const v=L.slice(0,vus);
  $('nbv').textContent=`${nf(L.length)} ligne${L.length>1?'s':''}`;
  $('corps').innerHTML=`<div class="wrapx"><table class="tbl"><thead><tr>
    <th class="no">N°</th><th>Date</th><th>Canal</th><th>Vente</th><th>Client</th><th>Produit</th>
    <th class="r">Qté</th><th class="r">Prix unit.</th><th class="r">Montant</th><th class="r">Marge nette</th><th>Enregistré par</th><th></th>
    </tr></thead><tbody>${v.map((x,i)=>`<tr class="${x.ret?'ret':''}" data-d="${i}" title="Voir toute la vente">
      <td class="no">${nf(i+1)}</td>
      <td class="qd">${dfr(x.d)}${x.h?`<br><span class="hh">${esc(x.h)}</span>`:''}</td>
      <td><span class="ch ${cls(x.canal)}">${esc(x.canal)}</span></td>
      <td class="num">${esc(x.cmd||x.num)}${x.ret?` <span class="chret">remboursé</span><small>${esc((MOTIFS_R.find(m=>m[0]===x.motif)||['','retour'])[1])} · ${x.mode==='aucun'?'rien rendu':'rendu en '+esc(COURT[x.mode]||'—')}</small>`:(x.cmd?`<small>${esc(x.num)}</small>`:'')}</td>
      <td>${esc(x.client)||'<span style="color:var(--ink-3)">—</span>'}</td>
      <td class="ref"><b>${esc(x.ref)}</b><span>${esc(x.bc)}</span></td>
      <td class="r">${nf(x.q)}</td>
      <td class="r">${x.p!=null?money2(x.p):'—'}</td>
      <td class="r mt">${money2(x.mt)}</td>
      <td class="r"><span class="mg ${mcls(x.pct)}">${x.mg!=null?money2(x.mg):'—'}</span>${x.pct!=null?`<br><span class="mg ${mcls(x.pct)}" style="font-weight:500;font-size:11px">${pc(x.pct)}</span>`:''}${x.com?`<br><span style="font-size:10.5px;color:var(--ink-3)">après ${x.com} %</span>`:''}</td>
      <td class="who${x.par&&x.par!=='(non renseigné)'?'':' anon'}">${esc(x.par||'—')}</td>
      <td class="act"><button data-det="${i}" title="Toute la vente : lignes, client, marge, remboursements">Détail</button> ${x.ret?'':`<button data-ret="${esc(x.fid)}" title="Annuler cette vente ou rembourser une partie">Rembourser</button>`}</td></tr>`).join('')}</tbody>
    <tfoot><tr><td colspan="6">Total affiché</td><td class="r">${nf(somme(L,'q'))}</td><td></td>
      <td class="r">${money2(somme(L,'mt'))}</td><td class="r"><span class="mg ${mcls(somme(L.filter(x=>x.mg!=null),'mg')<0?-1:1)}">${money2(somme(L.filter(x=>x.mg!=null),'mg'))}</span></td><td></td><td></td></tr></tfoot>
    </table></div>
    ${L.length>vus?`<button class="plus" id="plus">Afficher plus (${nf(L.length-vus)} restantes)</button>`:''}`;
  const b=$('plus'); if(b) b.onclick=()=>{ vus+=80; dessine(); };
  AFF=v;                                     /* ce qui est à l'écran, pour le panneau de détail */
  document.querySelectorAll('[data-ret]').forEach(el=>el.onclick=e=>{ e.stopPropagation(); ouvreRetour(el.dataset.ret); });
  document.querySelectorAll('[data-d]').forEach(el=>el.onclick=()=>ouvreDetail(AFF[+el.dataset.d]));
  document.querySelectorAll('[data-det]').forEach(el=>el.onclick=e=>{ e.stopPropagation(); ouvreDetail(AFF[+el.dataset.det]); });
  $('src').innerHTML=`${nf(L.length)} vente${L.length>1?'s':''} affichée${L.length>1?'s':''}<br>sur ${nf(V.length)} au total`;
  $('sfoot').innerHTML=`${nf(V.length)} ligne${V.length>1?'s':''} de vente<br>${CANAUX.filter(c=>c!==NP).length} canaux`;
}

/* ---------------- enregistrer une vente à la main ---------------- */
let PANIER=[], CANDIDATS=[], SEL=-1;

/* Le numéro de vente : V + la date + un rang qui repart à 1 chaque jour.
   Deux garde-fous : on part du plus grand rang déjà utilisé ce jour-là (pas du nombre de ventes),
   et on garde en mémoire le dernier rang atteint — une vente annulée ne libère donc pas son
   numéro, et aucun numéro n'est jamais réattribué. */
const KNUM='ventes-numeros-v1';

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
carnetLie('v-client','v-cres',()=>$('v-q').focus());
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
  const pvr=m.pvr!=null?+m.pvr:(v[5]!=null?+v[5]:null);
  if(pvr==null) return null;
  return r2(pvr*(1+(canal.maj||0)/100));
}
const canalCour=()=>CANAUX_VENTE().find(c=>c.nom===$('v-canal').value)||{id:'autre',nom:'Autre',com:0,maj:0};

function chercheProduits(q){
  q=q.trim().toLowerCase(); if(q.length<2) return [];
  const chiffres=/^\d{6,14}$/.test(q);
  const R=[];
  for(const cle in IDX){
    const v=IDX[cle];
    if(chiffres){ const nq=q.replace(/^0+/,''); const m=MOD[cle];
      if((v[0]||'').replace(/^0+/,'')===nq || (m&&m.bcs&&String(m.bcs).split(/[^0-9]+/).map(x=>x.replace(/^0+/,'')).includes(nq))) R.push(cle); }
    else { const t=((v[2]||'')+' '+(v[1]||'')+' '+(v[0]||'')).toLowerCase(); if(t.includes(q)) R.push(cle); }
    if(R.length>60) break;
  }
  return R.slice(0,40);
}
function peintRes(){
  const el=$('v-res');
  if(!CANDIDATS.length){ el.classList.remove('on'); el.innerHTML=''; return; }
  el.innerHTML=CANDIDATS.map((cle,i)=>{ const v=IDX[cle];
    return `<div data-cle="${esc(cle)}" class="${i===SEL?'sel':''}"><b>${esc(v[2]||'')} ${esc(v[1]||'')}</b>
      <span>${esc(v[3]||'')}${v[3]?' oz · ':''}${esc(v[0]||'sans code-barres')} · stock ${nf(qteEff(cle))}</span></div>`; }).join('');
  el.classList.add('on');
  el.querySelectorAll('[data-cle]').forEach(d=>d.onclick=()=>ajoute(d.dataset.cle));
}
function ajoute(cle){
  const ex=PANIER.find(l=>l.cle===cle);
  if(ex) ex.q++;
  else PANIER.push({cle,q:1,p:prixSuggere(cle,canalCour())});
  $('v-q').value=''; CANDIDATS=[]; SEL=-1; peintRes(); peintPanier(); $('v-q').focus();
}
function peintPanier(){
  const c=canalCour();
  if(!PANIER.length){ $('v-pan').innerHTML='<div class="vide">Aucun parfum. Scanne un code-barres ou tape un nom ci-dessus.</div>';
    $('v-ok').disabled=true; $('v-recap').innerHTML=''; return; }
  const li=PANIER.map((l,i)=>{
    const v=IDX[l.cle]||[], pa=paEff(l.cle), st=qteEff(l.cle);
    const mt=(l.q||0)*(l.p||0), net=mt*(1-(c.com||0)/100);
    const mg=pa!=null&&l.p!=null?(net-pa*(l.q||0)):null;
    const pct=pa!=null&&mt>0?mg/mt*100:null;
    const cls=pct==null?'na':pct<0?'c':pct<(REG.margeMin||10)?'w':'g';
    return `<tr><td class="r" style="color:var(--ink-3);width:34px">${i+1}</td>
      <td><b>${esc(v[2]||'')} ${esc(v[1]||'')}</b><br><span style="font-size:11.5px;color:var(--ink-3)" data-st="${i}">${esc(v[0]||'')} · stock ${nf(st)}${l.q>st?' — <b style="color:var(--crit)">manque '+nf(l.q-st)+'</b>':''}</span></td>
      <td class="r"><input type="number" min="1" step="1" data-i="${i}" data-f="q" value="${l.q}"></td>
      <td class="r"><input type="number" step="any" data-i="${i}" data-f="p" value="${l.p==null?'':l.p}" placeholder="prix"></td>
      <td class="r" data-mt="${i}">${money2(mt)}</td>
      <td class="r" data-mg="${i}"><span class="mgl ${cls}">${mg!=null?money2(mg):'—'}</span>${pct!=null?`<br><span class="mgl ${cls}" style="font-weight:500;font-size:11px">${pc(pct)}</span>`:''}</td>
      <td><button class="del" data-del="${i}" title="Retirer">✕</button></td></tr>`; }).join('');
  const tot=PANIER.reduce((a,l)=>a+(l.q||0)*(l.p||0),0);
  const totMg=PANIER.reduce((a,l)=>{ const pa=paEff(l.cle);
    return a+(pa!=null&&l.p!=null?((l.q||0)*(l.p||0)*(1-(c.com||0)/100)-pa*(l.q||0)):0); },0);
  const u=PANIER.reduce((a,l)=>a+(l.q||0),0);
  $('v-pan').innerHTML=`<table><thead><tr><th class="r"></th><th>Parfum</th><th class="r">Qté</th>
    <th class="r">Prix unit.</th><th class="r">Montant</th><th class="r">Marge nette</th><th></th></tr></thead>
    <tbody>${li}</tbody><tfoot><tr><td></td><td>${PANIER.length} parfum${PANIER.length>1?'s':''}</td>
    <td class="r" data-tu>${nf(u)}</td><td></td><td class="r" data-tmt>${money2(tot)}</td><td class="r" data-tmg>${money2(totMg)}</td><td></td></tr></tfoot></table>`;
  $('v-pan').querySelectorAll('input').forEach(inp=>{
    inp.oninput=()=>{
      const l=PANIER[+inp.dataset.i]; if(!l) return;
      if(inp.dataset.f==='q') l.q=Math.max(1,Math.round(+inp.value||1)); else l.p=inp.value===''?null:+inp.value;
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
  recap();
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
    const cs=$('v-pan').querySelector(`[data-st="${i}"]`); if(cs){ const st=qteEff(l.cle), v=IDX[l.cle]||[];
      cs.innerHTML=`${esc(v[0]||'')} · stock ${nf(st)}${l.q>st?' — <b style="color:var(--crit)">manque '+nf(l.q-st)+'</b>':''}`; }
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
  const manque=PANIER.filter(l=>l.q>qteEff(l.cle));
  const hors=PANIER.filter(l=>horsCanal(l.cle,c.id));
  const sansPrix=PANIER.filter(l=>l.p==null||!(l.p>0));
  $('v-recap').innerHTML=`Vente de <b>${nf(u)} flacon${u>1?'s':''}</b> sur <b>${esc(c.nom)}</b> pour <b>${money2(tot)}</b>.
    ${c.com?`${esc(c.nom)} garde ${c.com} % (${money2(tot*c.com/100)}) → il reste <b>${money2(net)}</b>. `:''}
    Ces flacons ont coûté ${money2(pa)} → marge <b>${money2(net-pa)}</b>${tot>0?` (${pc((net-pa)/tot*100)})`:''}.
    ${$('v-stock').checked?'Le stock sera diminué de ces quantités.':'Le stock ne bouge pas.'}
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
function ouvreVente(){
  PANIER=[]; CANDIDATS=[]; SEL=-1;
  const CV=CANAUX_VENTE();
  $('v-canal').innerHTML=CV.map(c=>`<option value="${esc(c.nom)}">${esc(c.nom)}</option>`).join('');
  if(canalSel && CV.some(c=>c.nom===canalSel)) $('v-canal').value=canalSel;
  $('v-date').value=ajd();
  $('v-client').value=''; $('v-num').value=numAuto($('v-date').value); $('v-q').value=''; $('v-msg').textContent='';
  if($('v-note')) $('v-note').value='';
  $('v-msg').className='msg';
  $('v-stock').checked=true;
  majAide(); peintRes(); peintPanier();
  try{ docReset(); }catch(e){}
  $('vov').classList.add('on'); setTimeout(()=>$('v-q').focus(),60);
}
function majAide(){
  const c=canalCour();
  $('v-aide').textContent = c.com ? `${c.nom} garde ${c.com} % sur chaque vente (réglages).`
    : c.id==='gros' ? 'Prix de gros proposé automatiquement.' : 'Prix de vente du canal proposé automatiquement.';
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
  $('ret-tete').innerHTML=`Vente <b>${esc(f.num)}</b> du <b>${dfr(f.d)}</b> sur <b>${esc(f.canal||NP)}</b>${f.tiers?` — <b>${esc(f.tiers)}</b>`:''},
    ${nf((f.lignes||[]).length)} parfum${(f.lignes||[]).length>1?'s':''} pour <b>${money2(f.montant||0)}</b>, enregistrée par ${esc(f.par||'—')}.
    ${Object.keys(rendu).length?'<br>Une partie a déjà été remboursée : les quantités proposées tiennent compte de ce qui reste.':''}`;
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
      <td><b>${esc(l.ref)}</b><br><span style="font-size:11.5px;color:var(--ink-3)">${esc(l.bc||'')}${l.reste<l.q?` · déjà remboursé ${nf(l.q-l.reste)}`:''}</span></td>
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
function recapRetour(){
  const L=RET.lignes, f=RET.f;
  const n=L.reduce((a,l)=>a+(l.n||0),0), mt=L.reduce((a,l)=>a+(l.n||0)*(l.p||0),0);
  const pa=L.reduce((a,l)=>a+(l.paAv!=null?l.paAv*(l.n||0):0),0);
  const comR=comCanal(f.canal);
  const total=(f.lignes||[]).reduce((a,l)=>a+(l.q||0),0);
  const mode=$('ret-mode').value;
  $('ret-recap').innerHTML= n? `Remboursement de <b>${nf(n)} flacon${n>1?'s':''}</b> sur ${nf(total)} pour <b>${money2(mt)}</b>
      ${mode==='avoir'?'sous forme d\'<b>avoir</b> (rien ne sort de la caisse)':mode==='aucun'?'<b>sans rien rendre</b> — la vente est simplement effacée des chiffres':mode==='echange'?'par <b>échange</b> — pense à enregistrer la nouvelle vente ensuite':`en <b>${esc((MODES_R.find(m=>m[0]===mode)||['','—'])[1])}</b>`}.
      Le chiffre d'affaires baisse de ${money2(mt)} et la marge nette de <b>${money2(mt-pa)}</b>${comR?` — dont ${money2(mt*comR/100)} de commission que ${esc(f.canal)} garde malgré le retour`:''}.
      ${(()=>{ if(!$('ret-stock').checked) return 'Le stock ne bouge pas.';
        const r=L.reduce((a,l)=>a+Math.min(l.n||0,Math.max(0,(l.sorti||0)-(l.rendu||0))),0);
        return r? `<b>${nf(r)} flacon${r>1?'s':''}</b> ${r>1?'reviennent':'revient'} en stock${r<n?` (les ${nf(n-r)} autres n'en étaient jamais sortis)`:''}.`
                : 'Aucun flacon ne revient en stock : la vente n\'en avait pas fait sortir.'; })()}
      ${n===total?'<br>C\'est la vente entière : elle sera annulée.':''}`
    : 'Indique au moins une quantité à rembourser.';
  $('ret-ok').disabled = !n;
}
['ret-mode','ret-motif','ret-stock'].forEach(i=>$(i).addEventListener('change',recapRetour));
$('ret-x').onclick=$('ret-ann').onclick=()=>{ $('retov').classList.remove('on'); RET=null; };
$('ret-ok').onclick=()=>{
  if(!RET) return;
  if(!signe("ce remboursement",()=>$('ret-ok').click())) return;
  const f=RET.f, L=RET.lignes.filter(l=>l.n>0);
  const d=$('ret-date').value||ajd();
  const mode=$('ret-mode').value, motif=$('ret-motif').value, note=$('ret-note').value.trim();
  const VENT=lit(KVENT,{}), JOU=lit(KJOU,[]);
  const lignes=[], det=[]; let remis=0;
  L.forEach(l=>{
    const qAv=qteEff(l.cle);
    const remisMax=Math.max(0,(l.sorti||0)-(l.rendu||0));   /* jamais plus que ce qui est sorti */
    const qAp=$('ret-stock').checked?qAv+Math.min(l.n,remisMax):qAv;
    lignes.push({cle:l.cle,bc:l.bc,ref:l.ref,q:-l.n,p:l.p,qAv,qAp,paAv:l.paAv});
    if(qAp!==qAv){ MOD[l.cle]=Object.assign({},MOD[l.cle]||{},{qte:qAp}); det.push({bc:l.bc,ref:l.ref,av:qAv,ap:qAp}); remis+=(qAp-qAv); }
    (VENT[l.cle]=VENT[l.cle]||[]).push({d,p:l.p,c:f.tiers||'',q:-l.n,num:f.num+' (remboursé)',k:f.canal});
  });
  const mt=L.reduce((a,l)=>a+l.n*(l.p||0),0);
  const nR=FACT.filter(x=>x.retour&&x.refId===f.id).length+1;
  const num=f.num+'-R'+nR;
  FACT.push({id:'r'+Date.now().toString(36),num,sens:'vente',retour:true,refId:f.id,refNum:f.num,
    canal:f.canal,tiers:f.tiers,d,lignes,montant:-mt,stock:$('ret-stock').checked,
    mode,motif,note,par:USR||'(non renseigné)',t:new Date().toISOString()});
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
  PANIER.forEach(l=>{ const p=prixSuggere(l.cle,canalCour()); if(p!=null) l.p=p; });
  if(!$('v-doc').dataset.touche){ $('v-doc').value=canalCour().id==='gros'?'facture':''; try{ docChampsMaj(); }catch(e){} }
  peintPanier(); };
$('v-doc').addEventListener('change',()=>{ $('v-doc').dataset.touche='1'; recap(); });
$('v-client').addEventListener('input',recap);
$('v-stock').onchange=recap;
/* on change la date : le numéro proposé suit, tant qu'il n'a pas été retouché à la main */
$('v-date').onchange=()=>{ const v=$('v-num').value.trim();
  if(!v || /^V\d{6}-\d{3}$/.test(v)) $('v-num').value=numAuto($('v-date').value); };
$('v-num').oninput=()=>{ const v=$('v-num').value.trim();
  if(v && numPris(v)){ const f=FACT.find(x=>String(x.num||'').toLowerCase()===v.toLowerCase());
    $('v-msg').textContent='Ce numéro est déjà pris (vente du '+dfr(f.d)+(f.canal?' sur '+f.canal:'')+').';
    $('v-msg').className='msg err'; }
  else { $('v-msg').textContent=''; $('v-msg').className='msg'; } };
$('v-q').oninput=()=>{ CANDIDATS=chercheProduits($('v-q').value); SEL=-1; peintRes();
  if(CANDIDATS.length===1 && /^\d{8,14}$/.test($('v-q').value.trim())) ajoute(CANDIDATS[0]); };
$('v-q').onkeydown=e=>{
  if(e.key==='ArrowDown'){ e.preventDefault(); SEL=Math.min(SEL+1,CANDIDATS.length-1); peintRes(); }
  else if(e.key==='ArrowUp'){ e.preventDefault(); SEL=Math.max(SEL-1,0); peintRes(); }
  else if(e.key==='Enter'){ e.preventDefault(); if(CANDIDATS.length) ajoute(CANDIDATS[SEL<0?0:SEL]); }
};
$('v-ok').onclick=()=>{
  if(!PANIER.length) return;
  if(!signe("cette vente",()=>$('v-ok').click())) return;
  const canal=$('v-canal').value, d=$('v-date').value||ajd();
  const client=$('v-client').value.trim();
  const num=$('v-num').value.trim() || numAuto(d);
  if(numPris(num)){
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
  const doc=docPourVente(PANIER.map(l=>({q:l.q,p:l.p})),client,d,CLI), devis=!!(doc&&doc.type==='devis');
  const PAN=(doc&&doc.remise)?repartitRemise(PANIER,doc):PANIER;
  PAN.forEach(l=>{
    const v=IDX[l.cle]||[], ref=(v[2]||'')+' '+(v[1]||''), qAv=qteEff(l.cle);
    const qAp=($('v-stock').checked&&!estDevis)?Math.max(0,qAv-(l.q||0)):qAv;
    lignes.push({cle:l.cle,bc:v[0],ref,q:l.q,p:l.p,qAv,qAp,manque:Math.max(0,(l.q||0)-qAv),paAv:paEff(l.cle),
                 pAv:l.pAv==null?undefined:l.pAv});
    if(qAp!==qAv){ MOD[l.cle]=Object.assign({},MOD[l.cle]||{},{qte:qAp}); det.push({bc:v[0],ref,av:qAv,ap:qAp}); sortis+=qAv-qAp; }
    if(!estDevis) (VENT[l.cle]=VENT[l.cle]||[]).push({d,h:heureMiami(),p:l.p,c:client,q:l.q,num,k:canal});
  });
  if(client) CLI[client]=Object.assign({nom:client},CLI[client]||{},{maj:new Date().toISOString()});
  if(client) clientDansRetail(client);
  const montant=PAN.reduce((a,l)=>a+(l.q||0)*(l.p||0),0);
  const f={id:'v'+Date.now().toString(36),num,sens:devis?'devis':'vente',canal,tiers:client,d,h:heureMiami(),lignes,montant,
           stock:$('v-stock').checked,manuel:true,par:USR||'(non renseigné)',t:new Date().toISOString()};
  if(doc) f.doc=doc;
  FACT.push(f); noteRang(num,d);
  ecrit(KFACT,FACT); ecrit(KMOD,MOD); ecrit(KVENT,VENT); ecrit(KCLI,CLI);
  JOU.push({t:new Date().toISOString(),u:USR||'(non renseigné)',act:'vente',
    lib:(devis?'devis '+doc.num:(doc?'facture '+doc.num+' — ':'vente saisie à la main — ')+canal)+(client?' — '+client:'')+(devis?'':' — '+num)+(doc&&!devis?' — '+(FMODES[doc.pmode]||doc.pmode)+(doc.reste>0?', reste dû '+money2(doc.reste):', payée'):''),
    n:det.length,impact:devis?0:-Math.round(montant),det});
  ecrit(KJOU,JOU);
  construitV();
  CANAUX=[...new Set(V.map(x=>x.canal))].sort((a,b)=>a===NP?1:b===NP?-1:a.localeCompare(b));
  const gard=$('fc').value;
  $('fc').innerHTML='<option value="">Tous les canaux</option>'+CANAUX.map(c=>`<option value="${esc(c)}">${esc(c)}</option>`).join('');
  $('fc').value=gard; $('fp').value='30';
  $('vov').classList.remove('on');
  vus=80; dessine();
  const b=document.createElement('div'); b.className='info'; b.style.borderLeftColor='var(--good)';
  b.style.background='var(--good-soft)';
  b.innerHTML=devis?`<b>Devis ${esc(doc.num)} enregistré</b> — ${PANIER.length} parfum${PANIER.length>1?'s':''}, ${money2(doc.total)}${client?' pour '+esc(client):''}. Le stock ne bouge pas. `
    :`<b>${doc?'Facture '+esc(doc.num):'Vente '+esc(num)} enregistrée</b> — ${PANIER.length} parfum${PANIER.length>1?'s':''}, ${money2(doc?doc.total:montant)} sur ${esc(canal)}${sortis?`, ${nf(sortis)} flacon${sortis>1?'s':''} sortis du stock`:', stock inchangé'}. `;
  if(doc){ const vb=document.createElement('button'); vb.className='btn sm'; vb.textContent='Voir le document'; vb.style.marginLeft='8px'; vb.onclick=()=>dessineDoc(f); b.appendChild(vb); }
  $('corps').parentNode.insertBefore(b,$('corps'));
  try{ peintDocs(); }catch(e){}
  setTimeout(()=>b.remove(),doc?20000:9000);
  if(doc) dessineDoc(f);
};

$('fc').innerHTML='<option value="">Tous les canaux</option>'+CANAUX.map(c=>`<option value="${esc(c)}">${esc(c)}</option>`).join('');
$('fc').addEventListener('input',()=>{ canalSel=$('fc').value; vus=80; dessine(); });
['q','fp'].forEach(i=>$(i).addEventListener('input',()=>{ vus=80; dessine(); }));

/* Ce qui sort, c'est ce qui est à l'écran : le même filtre, la même période, le
   même canal. Un export qui ne correspond pas à ce qu'on regarde est un export
   qu'on n'ose plus utiliser. Le filtre part avec le fichier, écrit en toutes
   lettres, pour qu'un papier retrouvé dans trois mois dise de quoi il parle. */
poseSortie('exp', ()=>{
  const L=filtre(true);
  const per=$('fp').options[$('fp').selectedIndex].textContent;
  const q=$('q').value.trim();
  return {
    titre:'Journal des ventes',
    fichier:'ventes',
    filtre:[per, canalSel?'canal '+canalSel:'tous les canaux', q?'recherche « '+q+' »':''].filter(Boolean).join(' · '),
    colonnes:[{t:'Date',y:'d'},{t:'Canal'},{t:'N° facture'},{t:'N° commande'},{t:'Client'},
      {t:'Code-barres'},{t:'Produit'},{t:'Quantité',y:'n'},{t:'Prix unitaire',y:'m'},
      {t:'Montant',y:'m'},{t:'Commission %',y:'p'},{t:'Encaissé net',y:'m'},
      {t:'Prix d\'achat',y:'m'},{t:'Marge nette',y:'m'},{t:'Taux de marge',y:'p'},{t:'Enregistré par'}],
    lignes:L.map(x=>[x.d,x.canal,x.num,x.cmd,x.client,x.bc,x.ref,x.q,x.p,x.mt,
      x.com||0,x.net,x.pa,x.mg,x.pct,x.par])
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
    out.push({brut:l, q:(r.qte&&r.qte.q)||1, taille:r.taille, cands:r.cands,
              cle:(sur==='ok'&&best)?best.cle:'', sur, appris:r.appris});
  });
  M_L=out;
  return out;
}

function mPeint(){
  const el=$('m-res');
  if(!M_L.length){ el.innerHTML=''; $('m-rap').hidden=true;
    $('m-att').disabled=true; $('m-devis').disabled=true; return; }
  const LIB={ok:'trouvé',hm:'à confirmer',no:'pas trouvé'};
  el.innerHTML=`<table class="mtb"><thead><tr>
    <th style="width:34%">Ce que le client a écrit</th><th>Le parfum</th>
    <th class="r">Qté</th><th class="r">Prix</th><th class="r"></th></tr></thead><tbody>
    ${M_L.map((l,i)=>{
      const v=l.cle?IDX[l.cle]:null;
      const px=l.cle?prixSuggere(l.cle,mCanal()):null;
      return `<tr class="${l.sur==='hm'?'sur':l.sur==='no'?'non':''}">
      <td><span class="msur ${l.sur}">${LIB[l.sur]}</span>${l.appris?' <span class="msur ok">appris</span>':''}
        <span class="brut">${esc(l.brut)}</span></td>
      <td>${l.cands.length?`<select data-ml="${i}">
          <option value="">— choisir —</option>
          ${l.cands.map(c=>{ const w=IDX[c.cle]||[];
            return `<option value="${esc(c.cle)}"${c.cle===l.cle?' selected':''}>${esc((w[2]||'')+' '+(w[1]||''))} · ${esc(w[3]||'?')} oz · stock ${nf(qteEff(c.cle))}</option>`; }).join('')}
        </select>`:'<span style="color:var(--crit)">aucun parfum approchant dans le catalogue</span>'}
        ${l.cle&&v?`<span class="brut">code-barres ${esc(v[0]||'—')}${l.taille?` · le client demande ${l.taille.ml} ml`:''}</span>`:''}</td>
      <td class="r"><input type="number" min="1" step="1" data-mq="${i}" value="${l.q}"></td>
      <td class="r">${px!=null?money2(px):'—'}</td>
      <td class="r"><button class="btn sm" data-msup="${i}" title="Retirer cette ligne">✕</button></td>
    </tr>`; }).join('')}</tbody></table>`;

  const pris=M_L.filter(l=>l.cle);
  const total=pris.reduce((a,l)=>a+(l.q*(prixSuggere(l.cle,mCanal())||0)),0);
  const flous=M_L.filter(l=>!l.cle).length;
  const manque=pris.filter(l=>l.q>qteEff(l.cle));
  const r=$('m-rap'); r.hidden=false;
  r.innerHTML=`<b>${nf(pris.length)} parfum${pris.length>1?'s':''} reconnu${pris.length>1?'s':''}</b>
    sur ${nf(M_L.length)} ligne${M_L.length>1?'s':''} lue${M_L.length>1?'s':''} · ${money2(total)} au prix du canal.
    ${flous?`<br><b style="color:var(--crit)">${nf(flous)} ligne${flous>1?'s':''} sans parfum choisi</b> — elle${flous>1?'s ne partiront':' ne partira'} pas.
      Choisis dans la liste, ou laisse : le client sera rappelé pour cette ligne.`:''}
    ${manque.length?`<br><b style="color:var(--warn)">${nf(manque.length)} ligne${manque.length>1?'s':''} dépasse${manque.length>1?'nt':''} le stock compté</b> :
      ${manque.slice(0,3).map(l=>esc(((IDX[l.cle]||[])[1]||''))+' — demandé '+l.q+', en stock '+nf(qteEff(l.cle))).join(' · ')}${manque.length>3?'…':''}.
      Ce n'est pas bloquant : ce n'est encore qu'une commande à valider.`:''}
    <br>Ce que tu corriges ici est <b>retenu</b> : la prochaine fois, la même phrase sera reconnue toute seule.`;

  el.querySelectorAll('[data-ml]').forEach(sl=>sl.onchange=()=>{
    const i=+sl.dataset.ml; M_L[i].cle=sl.value; M_L[i].sur=sl.value?'ok':'no'; mPeint(); });
  el.querySelectorAll('[data-mq]').forEach(ip=>ip.onchange=()=>{
    const i=+ip.dataset.mq; M_L[i].q=Math.max(1,parseInt(ip.value,10)||1); mPeint(); });
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
  $('m-canal').innerHTML=CV.map(c=>`<option value="${esc(c.nom)}">${esc(c.nom)}</option>`).join('');
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
    total:pris.reduce((a,l)=>a+l.q*(prixSuggere(l.cle,mCanal())||0),0), annule:false,
    lignes:pris.map(l=>{ const w=IDX[l.cle]||[];
      return {bc:w[0]||'', des:((w[2]||'')+' '+(w[1]||'')).trim(), q:l.q, p:prixSuggere(l.cle,mCanal())}; }),
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
$('m-devis').onclick=()=>{
  const pris=M_L.filter(l=>l.cle); if(!pris.length) return;
  mApprend();
  const canal=$('m-canal').value, client=$('m-client').value.trim(), txt=$('m-txt').value;
  mFerme();
  ouvreVente();
  if([...$('v-canal').options].some(o=>o.value===canal)) $('v-canal').value=canal;
  $('v-client').value=client;
  PANIER=pris.map(l=>({cle:l.cle,q:l.q,p:prixSuggere(l.cle,canalCour())}));
  try{ majAide(); }catch(e){}
  try{ $('v-doc').value='devis'; $('v-doc').dataset.touche='1'; docChampsMaj(); }catch(e){}
  peintPanier();
  $('v-msg').textContent='Rempli depuis le message du client — vérifie les prix avant d\'émettre le devis.';
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

function majUser(){ try{ piedSession(); }catch(e){} }
majUser();
/* ---- la rubrique Quotes ----
   La meme page que Ventes, reduite a un seul chemin : le client, sa liste (collee
   ou deposee), les lignes reconnues, puis le devis avec ses prix — et l'envoi. Rien
   n'est reecrit : une seule mecanique de devis dans l'outil, celle-ci. */
const MODE_QUOTES=('__MODE__'==='quotes');
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
    try{ $('v-doc').value='devis'; $('v-doc').dataset.touche='1'; docChampsMaj(); }catch(e){} };
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
    if(client && !$('v-client').value.trim()) $('v-client').value=client;
    pris.forEach(l=>{ const e=PANIER.find(x=>x.cle===l.cle); if(e) e.q+=l.q; else PANIER.push({cle:l.cle,q:l.q,p:prixSuggere(l.cle,canalCour())}); });
    peintPanier();
    $('v-msg').textContent='Rempli depuis le message du client — vérifie les prix avant d\'émettre le devis.';
    setTimeout(()=>$('v-pan').querySelector('input[data-f="p"]')?.focus(),60);
  };
  /* « Annuler » vide le devis en cours au lieu de fermer une fenetre qui n'en est plus une */
  $('v-ann').textContent='Vider';
  $('v-ann').onclick=()=>{ if(!PANIER.length || confirm(vf('Vider ce devis ? Rien ne sera enregistré.'))) ouvreVente(); };
  $('vx').onclick=null;
  /* ---- le sélectionneur de parfums ----
     Il tape « Paco Rabanne » : TOUS les Paco Rabanne s'affichent, rangés, avec le prix
     d'achat, le tarif de gros et le stock. Il coche ceux qu'il veut, il ajoute. Le
     champ n'est plus une simple recherche à un coup : c'est un choix dans le catalogue. */
  let COCHES=new Set();
  /* la photo du parfum : celle de l'outil (photos/), sinon celle du site, sinon une case vide */
  window.vignette=function(cle){ const v=IDX[cle]||[], bc=v[0]||'', far=v[8]||'';
    if(!bc && !far) return '<span class="vig miss">—</span>';
    return `<img class="vig" src="photos/${esc(bc)}.webp" data-far="${esc(far)}" alt="" loading="lazy" onerror="vigSecours(this)">`; };
  window.vigSecours=function(img){ const far=img.dataset.far; if(far && img.src.indexOf('photos/')>-1 && img.src!==far){ img.src=far; return; }
    const d=document.createElement('span'); d.className='vig miss'; d.textContent='—'; img.replaceWith(d); };
  try{ $('v-q').previousElementSibling.textContent='Choisir les parfums — tape une marque ou un nom, coche, ajoute'; $('v-q').placeholder='Marque, nom du parfum ou code-barres'; }catch(e){}
  chercheProduits=function(q){
    q=q.trim().toLowerCase(); if(q.length<2) return [];
    const chiffres=/^\d{6,14}$/.test(q), mots=q.split(/\s+/).filter(Boolean);
    const R=[];
    for(const cle in IDX){
      const v=IDX[cle];
      if(chiffres){ const nq=q.replace(/^0+/,''); const m=MOD[cle];
        if((v[0]||'').replace(/^0+/,'')===nq || (m&&m.bcs&&String(m.bcs).split(/[^0-9]+/).map(x=>x.replace(/^0+/,'')).includes(nq))) R.push(cle); }
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
        <b>${esc(v[2]||'')} ${esc(v[1]||'')}${v[3]?' <span style="font-weight:500;color:var(--ink-2)">'+esc(v[3])+' oz</span>':''}</b>
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
    COCHES.clear(); $('v-q').value=''; CANDIDATS=[]; SEL=-1; peintRes(); peintPanier(); $('v-q').focus();
  }
  /* Entrée : ce qui est coché part dans le devis ; rien de coché, le parfum surligné y va seul */
  $('v-q').addEventListener('keydown',e=>{ if(e.key==='Enter'&&COCHES.size){ e.stopImmediatePropagation(); e.preventDefault(); ajouteCoches(); } },true);
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
    const L=FACT.filter(f=>f.doc&&f.doc.type==='devis').sort((a,b)=>(b.t||'').localeCompare(a.t||''));
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
          <td>${esc(f.par||'—')}</td><td>${esc(f.doc.note||'')}</td>
          <td class="r"><b>${money2(f.doc.total)}</b></td><td><span class="et ${e}">${LIB_ET[e]}</span></td></tr>`;
        if(!on) return ligne;
        const D=f.doc, lignes=(f.lignes||[]).filter(l=>l.q);
        return ligne+`<tr class="qd"><td colspan="7"><div class="qdet"><div>
            ${lignes.map(l=>`<div class="lg"><span>${nf(l.q)}</span><span><b>${esc(l.ref)}</b><br><small>${esc(l.bc||'')}</small></span><span>@ ${money2(l.p)}</span><span class="r"><b>${money2((l.q||0)*(l.p||0))}</b></span></div>`).join('')}
            <div class="tot"><span>Sous-total</span><span class="r">${money2(D.sousTotal)}</span>
              ${D.remise?`<span>Remise</span><span class="r">−${money2(D.remise)}</span>`:''}
              <span>${D.taux?`Sales tax ${D.taux} %`:'Sales tax — exonéré'}</span><span class="r">${money2(D.taxe||0)}</span>
              <span class="tt">TOTAL DU DEVIS</span><span class="r tt">${money2(D.total)}</span></div>
            ${D.note?`<div class="note"><b>Note</b> — ${esc(D.note)}</div>`:''}
            ${D.converti?`<div class="note"><b>Converti en facture</b> ${esc(D.convertiNum||'')}</div>`:''}
            ${(D.envoye||[]).length?`<div class="note">Envoyé par e-mail à ${esc(D.envoye.map(x=>x.a).join(', '))}</div>`:''}
          </div><div class="btns">
            ${e==='devis'?`<button class="btn pri" data-qa="conv" data-q="${esc(f.id)}">Convertir en facture</button>`:''}
            <button class="btn" data-qa="wa" data-q="${esc(f.id)}">Envoyer par WhatsApp</button>
            <button class="btn" data-qa="mail" data-q="${esc(f.id)}">Envoyer par e-mail</button>
            <button class="btn" data-qa="voir" data-q="${esc(f.id)}">Voir / imprimer le devis</button>
            ${e==='archive'?`<button class="btn" data-qa="desarch" data-q="${esc(f.id)}">Désarchiver</button>`:`<button class="btn" data-qa="arch" data-q="${esc(f.id)}">Archiver</button>`}
          </div></div></td></tr>`; }).join('')}</tbody></table>`);
    $('q-etat').value=Q_F.etat;
    $('q-etat').onchange=()=>{ Q_F.etat=$('q-etat').value; peintDocs(); };
    $('q-cli').oninput=()=>{ Q_F.cli=$('q-cli').value; peintDocs(); $('q-cli').focus(); const v=$('q-cli').value; $('q-cli').setSelectionRange(v.length,v.length); };
    $('q-num').oninput=()=>{ Q_F.num=$('q-num').value; peintDocs(); $('q-num').focus(); const v=$('q-num').value; $('q-num').setSelectionRange(v.length,v.length); };
    $('docs-table').querySelectorAll('tr.qr').forEach(tr=>tr.onclick=()=>{ Q_OUVERT=Q_OUVERT===tr.dataset.q?'':tr.dataset.q; peintDocs(); });
    $('docs-table').querySelectorAll('[data-qa]').forEach(b=>b.onclick=e=>{ e.stopPropagation();
      const f=FACT.find(x=>x.id===b.dataset.q); if(!f) return; const a=b.dataset.qa;
      if(a==='arch'||a==='desarch'){ docMaj(f,x=>{ if(a==='arch') x.doc.archive=true; else delete x.doc.archive; });
        try{ const J=lit(KJOU,[]); J.push({t:new Date().toISOString(),u:USR||'(non renseigné)',act:'vente',lib:'devis '+f.doc.num+(a==='arch'?' archivé':' désarchivé')+(f.tiers?' — '+f.tiers:''),n:0,impact:0,det:[]}); ecrit(KJOU,J); }catch(e){}
        peintDocs(); return; }
      dessineDoc(FACT.find(x=>x.id===f.id)||f);
      if(a==='conv') setTimeout(()=>$('doc-conv').click(),150);
      else if(a==='wa') setTimeout(()=>$('doc-wa').click(),150);
      else if(a==='mail') setTimeout(()=>$('doc-mail').click(),150);
    });
  };
  try{ DOCS_F='devis'; peintDocs(); }catch(e){}
  /* le devis emis et refermé : on repart propre pour le suivant */
  $('doc-x').addEventListener('click',()=>{ try{ ouvreVente(); }catch(e){} });
},0);
$('sfoot').innerHTML=`${nf(V.length)} lignes de vente<br>${CANAUX.filter(c=>c!==NP).length} canaux`;
dessine();
peintFile();
/* pour les tests : de quoi lire l'état sans passer par l'écran */
window.__V={litFile,litAttente,peintFile,enregistreFile,qteEff,cleDeBC,lit,ecrit,KFILE};
'''+_facture.JS

_IDX = 'Object.fromEntries(D_TOUS().map(r=>[r[15],[r[0],r[13],r[2],r[3],r[12],r[7],r[8],r[6],r[9]]]))'
html = coquille("Journal des ventes", "Ventes",
    "Chaque produit vendu, avec le canal sur lequel la vente a été faite : boutique, gros, site, "
    "Shopify, Amazon, Perfume City, caisse. Chiffre d'affaires et marge par canal, et la saisie "
    "d'une vente à la main.",
    CSS + CSS_QUOTES, CORPS.replace('__ACCEPT__', _lire.ACCEPT), JS.replace('__NOMS__', _noms.NOMS).replace('__MODE__', 'ventes'), donnees=('produits','clients','retail'))
html = html.replace('__IDX__', _IDX)
open('ventes.html','w').write(html)
print('ventes.html', len(html)//1024, 'Ko')

# La rubrique Quotes : meme page, autre porte. Le client, sa liste, le devis, l'envoi.
html = coquille("Quotes", "Quotes",
    "Tu choisis les parfums, tu mets tes prix, tu envoies par WhatsApp ou email. "
    "La liste du client — collée, en photo ou en fichier — remplit les lignes pour toi. "
    "Le devis est gardé et devient une facture en un clic.",
    CSS + CSS_QUOTES, CORPS.replace('__ACCEPT__', _lire.ACCEPT), JS.replace('__NOMS__', _noms.NOMS).replace('__MODE__', 'quotes'), donnees=('produits','clients','retail'))
html = html.replace('__IDX__', _IDX)
open('quotes.html','w').write(html)
print('quotes.html', len(html)//1024, 'Ko')
