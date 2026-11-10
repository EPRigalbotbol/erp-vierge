import json
from _fusion import FUSION
from _comptes import COMPTES
import _aide
from _serveur import enligne
from _identite import IDENT
import _identite
import _file_auto
from _sauvegarde import SAUVE
from _menu import MENU
from _langue import LANGUE
import _langue
import _xlsx, _sortie
import _lire
data=open('stock.json').read()
import _donnees
from build_crm import barre
_donnees.pose('inventaire', data, 'D_INV')
S=json.load(open('stock_stats.json'))
n=lambda v: f"{v:,}".replace(',',' ')

TPL = r'''<!DOCTYPE html>
<html lang="fr"><head><meta charset="utf-8">
<!-- l'icône d'onglet : Sam a toujours beaucoup d'onglets ouverts ; le flacon du logo, blanc sur rose vif (choisi par Igal), se repère d'un coup d'œil (27 sept. 2026) -->
<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='14' fill='%23FF1F7A'/%3E%3Cg fill='none' stroke='%23fff' stroke-width='4' stroke-linejoin='round'%3E%3Crect x='25' y='7' width='14' height='8' rx='2' fill='%23fff'/%3E%3Crect x='28' y='15' width='8' height='6'/%3E%3Cpath d='M19 21 H45 L51 27 V51 L45 57 H19 L13 51 V27 Z'/%3E%3C/g%3E%3Cpath d='M36 28 Q44 29 45 36' stroke='%23fff' stroke-width='3' fill='none' stroke-linecap='round'/%3E%3C/svg%3E">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta http-equiv="Cache-Control" content="no-store, no-cache, must-revalidate">
<meta http-equiv="Pragma" content="no-cache">
<meta http-equiv="Expires" content="0">
<script>/* en anglais ou en espagnol, l'écran reste caché le temps que la traduction passe (quelques ms) : on ne voit jamais le français d'origine */try{var _l=localStorage.getItem('langue-v1');if(_l&&_l!=='fr'){document.documentElement.style.visibility='hidden';setTimeout(function(){document.documentElement.style.visibility='';},1500);}
/* un menu réglé (ordre, rubriques cachées) : la barre reste cachée le temps qu'il s'applique, pour que les rubriques ne sautent pas */
var _m=JSON.parse(localStorage.getItem('menu-perso-v1')||'null');if(_m&&((_m.ordre&&_m.ordre.length)||(_m.caches&&_m.caches.length))){document.documentElement.classList.add('mn-attente');setTimeout(function(){document.documentElement.classList.remove('mn-attente');},1500);}}catch(e){}</script>
<script>/* le contenu de la page reste caché jusqu'à ce que son code l'ait dessiné (voir _serveur.py) */try{document.documentElement.classList.add('pg-attente');setTimeout(function(){document.documentElement.classList.remove('pg-attente');},4000);}catch(e){}</script>
<style>.mn-attente .side nav{visibility:hidden} .pg-attente .main{visibility:hidden}</style>

<title>Inventaire — Perfumes Trade</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap">
<style>
:root{--ground:#F4F4F1;--surface:#FFF;--surface-2:#FAFAF8;--ink:#17171D;--ink-2:#33333D;--ink-3:#5C5C68;
--line:#E0E0DC;--line-2:#EDEDE9;--iris:#5B4B8A;--iris-soft:#EDE9F6;
--good:#2C6E4E;--good-soft:#E9F3ED;--warn:#8A5A00;--warn-soft:#FBF3E2;--crit:#A4262C;--crit-soft:#FBECEC;}
@media(prefers-color-scheme:dark){:root:not([data-theme="light"]){
--ground:#121217;--surface:#1A1A21;--surface-2:#202028;--ink:#ECECF1;--ink-2:#C9C9D3;--ink-3:#A4A4B2;
--line:#2C2C36;--line-2:#26262F;--iris:#A99AE0;--iris-soft:#272036;
--good:#77C79C;--good-soft:#152A20;--warn:#D9A94A;--warn-soft:#2E2411;--crit:#E8898D;--crit-soft:#33191B;}}
:root[data-theme="dark"]{--ground:#121217;--surface:#1A1A21;--surface-2:#202028;--ink:#ECECF1;--ink-2:#C9C9D3;
--ink-3:#A4A4B2;--line:#2C2C36;--line-2:#26262F;--iris:#A99AE0;--iris-soft:#272036;
--good:#77C79C;--good-soft:#152A20;--warn:#D9A94A;--warn-soft:#2E2411;--crit:#E8898D;--crit-soft:#33191B;}
*{box-sizing:border-box}
body{font-variant-numeric:tabular-nums;font-feature-settings:"tnum" 1,"cv05" 1}
/* ---- lisible (Igal, 25 sept. 2026 : « beaucoup d'écritures en gris clair, ça me dérange ;
   agrandis la police des écritures, pas des titres ») : gris plus foncés (ci-dessus, dans
   les couleurs), et tout le contenu de la page 8 % plus grand — le grand titre garde sa
   taille. Les tableaux restent dans leur cadre (colonnes secondaires rangées, voir « af »). */
.wrap{zoom:1.08}
.wrap h1{zoom:.926}
@media (max-width:1300px){.wrap{zoom:1}.wrap h1{zoom:1}}   /* portable : taille normale, sinon les tableaux débordent */

body{margin:0;background:var(--ground);color:var(--ink);
font-family:Inter,-apple-system,BlinkMacSystemFont,sans-serif;font-size:15px;-webkit-font-smoothing:antialiased}
.mono{font-family:Inter,sans-serif;font-variant-numeric:tabular-nums}
.eyebrow{font-family:Inter,sans-serif;font-size:11px;letter-spacing:.13em;
text-transform:uppercase;color:var(--ink-3);font-weight:500}
.pg .sous{margin:7px 0 0;font-size:13.5px;color:var(--ink-2);line-height:1.6;max-width:82ch}
.impban{display:flex;align-items:center;gap:12px;flex-wrap:wrap;margin:0 0 16px;
 padding:11px 15px;background:var(--iris-soft);border-left:3px solid var(--iris);
 border-radius:5px;font-size:13.5px;color:var(--ink-2);line-height:1.55}
.impban b{color:var(--ink)}
.impban button{margin-left:auto;font-family:inherit;font-size:13px;color:var(--ink-2);
 background:var(--surface);border:1px solid var(--line);border-radius:5px;padding:7px 13px;cursor:pointer}
.impban button:hover{border-color:var(--iris);color:var(--iris)}

.app{display:flex;align-items:flex-start;min-height:100vh}
.side{width:234px;flex:0 0 234px;position:sticky;top:0;height:100vh;overflow-y:auto;
background:var(--surface);border-right:1px solid var(--line);display:flex;flex-direction:column;padding:14px 0 10px}
.logo{padding:0 18px 12px;border-bottom:1px solid var(--line-2);margin-bottom:8px}
.logo .n{font-size:16px;font-weight:700;letter-spacing:-.02em;line-height:1.2}
.logo .s{font-family:Inter,sans-serif;font-size:9.5px;letter-spacing:.15em;
text-transform:uppercase;color:var(--ink-3);margin-top:3px}
nav{display:flex;flex-direction:column;gap:1px;padding:0 10px}
.navlab{font-family:Inter,sans-serif;font-size:11.5px;letter-spacing:.14em;text-transform:uppercase;
color:var(--iris);font-weight:800;padding:10px 8px 4px}
.nv{display:flex;align-items:center;gap:9px;padding:5px 10px;white-space:nowrap;border-radius:4px;
font-size:13.5px;color:var(--ink);font-weight:600;text-decoration:none;line-height:1.3;border-left:2px solid transparent}
.nv .ic{width:15px;text-align:center;flex:0 0 15px;opacity:.75}
.nv .ct{margin-left:auto;font-family:Inter,sans-serif;font-size:10.5px;font-weight:500;color:var(--ink-3);
font-variant-numeric:tabular-nums}
.nv .ct.pt{background:var(--iris-soft);color:var(--iris);font-weight:700;font-size:10.5px;border-radius:10px;padding:2px 7px;min-width:20px;text-align:center;line-height:1.5}
.nv:hover{background:var(--surface-2);color:var(--ink)}
.nv.on{background:var(--iris-soft);color:var(--iris);font-weight:700;border-left-color:var(--iris)}
.nv.on .ic{opacity:1}
.nv.sub{padding:3px 10px 3px 36px;font-size:12.5px;font-weight:500}
@media(max-height:860px) and (min-width:901px){.nv{padding-top:1px;padding-bottom:1px}.navlab{padding-top:3px;padding-bottom:2px}.side{padding-top:6px;padding-bottom:5px}.logo{padding-bottom:7px;margin-bottom:4px}}  /* portable : voir _base.css (4 nov. 2026 : un cran de plus, Transfert interstore ; 10 nov. : la rubrique Offre) */
@media(max-width:900px){.nv.sub{padding:5px 10px}}
.nv.soon{color:var(--ink-3);font-weight:500;cursor:default;pointer-events:none}
.nv.soon .ct{font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.8}
.sfu{margin-bottom:9px;padding-bottom:9px;border-bottom:1px solid var(--line-2);
font-family:Inter,sans-serif;font-size:11.5px;color:var(--ink-3);line-height:1.5}
.sfu b{color:var(--iris);font-weight:600}
.lnk{background:none;border:0;padding:0;font-family:inherit;font-size:11.5px;color:var(--ink-3);
text-decoration:underline;cursor:pointer}
.lnk:hover{color:var(--iris)}
.sfoot{margin-top:auto;padding:10px 18px 8px;border-top:1px solid var(--line-2);
font-family:Inter,sans-serif;font-size:10px;color:var(--ink-3);line-height:1.6}
/* Le TYPE du parfum (EDT, EDP, OIL, SET…) et son GENRE — même pastille que
   partout ailleurs (voir _base.css ; ces deux pages ont leur propre charte). */
.ty{display:inline-block;font-style:normal;font-family:Inter,sans-serif;font-size:10.5px;font-weight:800;
 letter-spacing:.05em;padding:1px 6px;margin-left:6px;border-radius:5px;vertical-align:middle;
 background:var(--iris-soft);color:var(--iris);white-space:nowrap}
.gn{display:inline-block;font-style:normal;font-family:Inter,sans-serif;font-size:10.5px;font-weight:600;
 letter-spacing:.03em;padding:1px 6px;margin-left:4px;border-radius:5px;vertical-align:middle;
 background:var(--line-2);color:var(--ink-3);white-space:nowrap}
/* le pied garde sa place dès le départ (voir _base.css) */
.sfoot #sfu{min-height:64px}
.sfoot .sfline{display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin-top:6px}
.sfoot .sfline #lgsel{margin-top:0!important}
.sfoot .sfline #mn-btn{display:inline!important;margin-top:0!important}
.sfoot #aid-slot{min-height:20px}

.main{flex:1;min-width:0}
.wrap{max-width:1600px;margin:0 auto;padding:26px 26px 80px;display:flex;flex-direction:column;gap:30px}
@media(max-width:900px){.app{flex-direction:column}
.side{width:100%;flex:none;height:auto;position:static;border-right:0;border-bottom:1px solid var(--line);padding:14px 0 10px}
.logo{padding:0 16px 12px} nav{flex-direction:row;overflow-x:auto;gap:4px;padding:0 12px;scrollbar-width:none}
nav::-webkit-scrollbar{display:none} .navlab{display:none}
.nv{border-left:0;border-bottom:2px solid transparent;border-radius:3px}
.nv.on{border-left:0;border-bottom-color:var(--iris)} .nv .ct,.nv .ic{display:none}
/* Le pied de barre portait « Se déconnecter » et « Une question ? ». Le masquer
    sous 900 px enlevait la SEULE sortie de session : sur un écran étroit,
    impossible de changer de compte. On garde l'identité et les boutons, on ne
    laisse tomber que les chiffres, qui ne sont qu'un rappel. */
 .sfoot{display:flex;align-items:center;gap:14px;margin-top:0;padding:8px 16px 10px;
  border-top:1px solid var(--line-2)}
 .sfoot #sfoot,.sfoot .ver{display:none}
 .sfoot .sfu{display:flex;align-items:center;gap:8px}
 .sfoot .sfu b,.sfoot .sfu span{display:inline!important}
.wrap{padding:20px 16px 60px}}

header.pg{border-bottom:2px solid var(--ink);padding-bottom:18px;display:flex;flex-wrap:wrap;
gap:14px;align-items:flex-end;justify-content:space-between}
h1{margin:0;font-size:clamp(25px,4vw,34px);font-weight:700;letter-spacing:-.028em;line-height:1.05}
h2{margin:0;font-size:19px;font-weight:600;letter-spacing:-.015em}
section{display:flex;flex-direction:column;gap:15px}

.xlong{display:flex;flex-wrap:wrap;gap:7px;margin-top:13px;align-items:center}
.xlong .lab{font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--ink-3);
 font-weight:700;margin-right:3px}
.xlb{padding:6px 12px;font-family:inherit;font-size:13px;border:1px solid var(--line);
 border-radius:20px;background:var(--surface);color:var(--ink-2);cursor:pointer}
.xlb:hover{border-color:var(--iris);color:var(--iris)}
.xlb.on{background:var(--iris);border-color:var(--iris);color:#fff;font-weight:600}

.ver{margin-top:9px;font-family:Inter,sans-serif;font-size:10px;color:var(--ink-3);opacity:.75;letter-spacing:.02em}
.vhint{margin:10px 0 12px;padding:10px 14px;background:var(--iris-soft);border-left:3px solid var(--iris);border-radius:0 8px 8px 0;font-size:13.5px;color:var(--ink-2);line-height:1.55}
.vhint b{color:var(--ink)}
.shead{border-bottom:1px solid var(--line);padding-bottom:10px;display:flex;
justify-content:space-between;align-items:baseline;gap:12px;flex-wrap:wrap}
.sdesc{font-size:13.5px;color:var(--ink-2);max-width:70ch;margin:0}

.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:1px;
background:var(--line);border:1px solid var(--line);border-radius:3px;overflow:hidden}
.stat{background:var(--surface);padding:14px 16px;display:flex;flex-direction:column;gap:5px}
.stat .n{font-family:Inter,sans-serif;font-size:24px;font-weight:600;letter-spacing:-.02em;
line-height:1;font-variant-numeric:tabular-nums}
.stat .l{font-size:12.5px;color:var(--ink-3);line-height:1.35}
.stat.g .n{color:var(--good)} .stat.c .n{color:var(--crit)} .stat.i .n{color:var(--iris)}

.hero{background:var(--iris-soft);border-left:4px solid var(--iris);padding:10px 14px;
border-radius:0 4px 4px 0;display:flex;flex-direction:column;gap:8px}
.hero .hl{display:flex;align-items:center;gap:14px;flex-wrap:wrap}
.hero .ht{display:flex;flex-direction:column;gap:1px;min-width:200px}
.hero h3{margin:0;font-size:13.5px;font-weight:700;color:var(--iris);line-height:1.2}
.hero .hs{font-size:11.5px;color:var(--ink-3);line-height:1.3}
.hero .hq{margin-left:auto;width:22px;height:22px;border-radius:50%;border:1px solid var(--iris);
background:transparent;color:var(--iris);font-family:inherit;font-size:12px;font-weight:700;cursor:pointer;
display:flex;align-items:center;justify-content:center;flex:none}
.hero .hq:hover,.hero .hq.on{background:var(--iris);color:#fff}
.hero p.hx{margin:0;font-size:13px;color:var(--ink-2);line-height:1.55;max-width:80ch}
.hero p b{color:var(--ink)}
.pal{display:flex;flex-wrap:wrap;gap:5px}
.pil{background:var(--surface);border:1px solid var(--line);border-radius:20px;padding:4px 10px;
cursor:pointer;font-family:Inter,sans-serif;font-size:11.5px;color:var(--ink-3);
display:inline-flex;align-items:baseline;gap:5px;line-height:1.3;white-space:nowrap}
.pil b{font-size:12.5px;color:var(--ink);font-weight:600}
.pil:hover{border-color:var(--iris);color:var(--iris)}
.pil.on{background:var(--iris);border-color:var(--iris);color:#fff}
.pil.on b{color:#fff}

.tools{display:flex;flex-wrap:wrap;gap:8px;align-items:center}
input[type=search],select{font-family:inherit;font-size:13.5px;color:var(--ink);background:var(--surface);
border:1px solid var(--line);border-radius:3px;padding:8px 11px}
input[type=search]{flex:1;min-width:190px}
input:focus,select:focus{outline:2px solid var(--iris);outline-offset:1px}
select#ftri.on{border-color:var(--iris);color:var(--iris);font-weight:600}
button{font-family:inherit;font-size:13.5px;font-weight:500;color:var(--ink-2);background:var(--surface);
border:1px solid var(--line);border-radius:3px;padding:8px 14px;cursor:pointer}
button:hover{border-color:var(--iris);color:var(--iris)}
button.pri{background:var(--iris);border-color:var(--iris);color:#fff;font-weight:600}
button.pri:hover{filter:brightness(1.08);color:#fff}
.count{font-family:Inter,sans-serif;font-size:12.5px;color:var(--ink-3);margin-left:auto}

.tw{border:1px solid var(--line);border-radius:4px;overflow:hidden;background:var(--surface)}
.tscroll{overflow-x:auto;max-height:70vh;overflow-y:auto}
table{width:100%;border-collapse:collapse;font-size:13.5px}
thead th{position:sticky;top:0;z-index:2;background:var(--surface-2);text-align:left;
font-family:Inter,sans-serif;font-size:10px;letter-spacing:.09em;text-transform:uppercase;
color:var(--ink-3);font-weight:500;padding:10px 12px;border-bottom:1px solid var(--line);white-space:nowrap}
thead th[data-tri]{cursor:pointer;user-select:none}
thead th[data-tri]:hover{color:var(--ink)}
thead th[data-tri]::after{content:"";display:inline-block;width:0;margin-left:5px;opacity:.55}
thead th.tri-asc::after{content:"\2191";width:auto}
thead th.tri-desc::after{content:"\2193";width:auto}
thead th.tri-asc,thead th.tri-desc{color:var(--iris)}
td{padding:7px 12px;border-bottom:1px solid var(--line-2);vertical-align:middle}
td.no,th.no{width:44px;text-align:right;padding-right:7px;color:var(--ink-3);
font-family:Inter,sans-serif;font-size:11.5px;font-variant-numeric:tabular-nums}
tbody tr:last-child td{border-bottom:0}
tbody tr:hover{background:var(--surface-2)}
td.num{font-family:Inter,sans-serif;text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
td.code{font-family:Inter,sans-serif;font-size:11.5px;color:var(--ink-3);white-space:nowrap}
.pd{display:flex;flex-direction:column;gap:1px;min-width:210px}
.pd .b{font-family:Inter,sans-serif;font-size:9.5px;letter-spacing:.12em;
text-transform:uppercase;color:var(--ink-3)}
.pd .n{font-size:13.5px;font-weight:500;line-height:1.3}
.pd[data-fiche]:not([data-fiche=""]){cursor:pointer}.pd[data-fiche]:not([data-fiche=""]):hover .n{text-decoration:underline;color:var(--accent,#5b3f8c)}
.pd .m{font-size:11.5px;color:var(--ink-3)}
.tag{font-family:Inter,sans-serif;font-size:9.5px;padding:2px 7px;border-radius:99px;
font-weight:500;letter-spacing:.03em;white-space:nowrap}
.tag.ok{background:var(--good-soft);color:var(--good)}
.tag.non{background:var(--warn-soft);color:var(--warn)}
.tag.doute{background:var(--crit-soft);color:var(--crit)}
input.scan{margin:8px 0 12px;padding:10px 14px;border-radius:8px;font-size:13.5px;line-height:1.5;border:1px solid var(--line);background:var(--surface-2)}
.scan.ok{border-color:var(--good);background:var(--good-soft);color:var(--good)}
.scan.ko{border-color:var(--crit);background:var(--crit-soft);color:var(--crit)}
.scan b{color:inherit}
.cnt{width:72px;font-family:Inter,sans-serif;font-size:13.5px;text-align:right;
padding:5px 8px;border:1px solid var(--line);border-radius:3px;background:var(--surface-2);
color:var(--ink);font-variant-numeric:tabular-nums}
input.cnt:focus{outline:2px solid var(--iris);outline-offset:1px;background:var(--surface)}
input.cnt.filled{background:var(--iris-soft);border-color:var(--iris)}
.vit{display:block;font-family:Inter,sans-serif;font-size:10px;font-weight:600;
color:var(--iris);letter-spacing:.02em;margin-top:1px}
.gap{font-family:Inter,sans-serif;font-size:13px;font-weight:600;font-variant-numeric:tabular-nums}
.gap.pos{color:var(--good)} .gap.neg{color:var(--crit)} .gap.zero{color:var(--ink-3);font-weight:400}
/* Igal, 30 sept. 2026 : une ligne comptée devient VIOLET PÂLE — c'est la preuve que le
   stock a été compté ; l'écart et sa valeur ne s'affichent plus (colonnes 6 et 7 masquées),
   le capital reste. */
tr.done,tr.ecart{background:var(--iris-soft)}
tr.done:hover,tr.ecart:hover{background:var(--iris-soft)}
#tb td:nth-child(6),#tb td:nth-child(7),.tscroll thead th:nth-child(6),.tscroll thead th:nth-child(7){display:none}
/* sans le prix d'achat (rôle Commercial, Entrepôt) : pas de capital — il est au prix d'achat (3 oct. 2026) */
body.sansPA #tb td:nth-child(8),body.sansPA .tscroll thead th:nth-child(8),body.sansPA .stat.c,body.sansPA #bilan>div:nth-child(2){display:none}

.bilan{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:1px;
background:var(--line);border:1px solid var(--line);border-radius:3px;overflow:hidden}
.bilan div{background:var(--surface);padding:13px 15px;display:flex;flex-direction:column;gap:4px}
.bilan .v{font-family:Inter,sans-serif;font-size:20px;font-weight:600;font-variant-numeric:tabular-nums;line-height:1}
.bilan .k{font-size:12px;color:var(--ink-3)}
.note{background:var(--warn-soft);border-left:3px solid var(--warn);padding:14px 17px;
border-radius:0 3px 3px 0;font-size:13.5px;color:var(--ink-2);line-height:1.6;max-width:76ch}
.note b{color:var(--ink)}
footer{border-top:1px solid var(--line);padding-top:15px;font-size:12.5px;color:var(--ink-3);
display:flex;flex-wrap:wrap;gap:8px;justify-content:space-between}
__CSSSORTIE__
@media print{.side,.tools,.hero .pal,footer,.note{display:none}
.tscroll{max-height:none} input.cnt{border:1px solid #999;background:#fff}
body{background:#fff} .tw{border-color:#999}}
/* ---------- fenêtre « nouvel inventaire » ---------- */
.ov{position:fixed;inset:0;background:rgba(23,23,29,.55);backdrop-filter:blur(2px);
z-index:60;display:none;align-items:flex-start;justify-content:center;padding:40px 18px;overflow-y:auto}
.ov.on{display:flex}
.mod{background:var(--surface);border:1px solid var(--line);border-radius:8px;width:100%;
box-shadow:0 18px 48px rgba(0,0,0,.24);display:flex;flex-direction:column}
.mh{padding:17px 21px;border-bottom:1px solid var(--line);display:flex;align-items:center;gap:14px}
.mh h2{margin:0;font-size:17.5px;font-weight:700;letter-spacing:-.02em}
.mh .x{margin-left:auto;background:none;border:0;font-size:22px;color:var(--ink-3);cursor:pointer;line-height:1;padding:2px 6px}
.mh .x:hover{color:var(--ink)}
.mb{padding:19px 21px;display:flex;flex-direction:column;gap:2px}
.mf{padding:14px 21px;border-top:1px solid var(--line);background:var(--surface-2);
display:flex;gap:9px;justify-content:flex-end;align-items:center}
.mod .fld{display:flex;flex-direction:column;gap:5px}
.mod .fld label{font-family:Inter,sans-serif;font-size:10px;letter-spacing:.11em;
text-transform:uppercase;color:var(--ink-3);font-weight:600}
.mod select{padding:9px 11px;font-family:inherit;font-size:13.5px;border:1px solid var(--line);
border-radius:7px;background:var(--surface);color:var(--ink);width:100%}
.mod .why{font-size:13px;color:var(--ink-2);line-height:1.65}
.mod .cb{font-size:13.5px;color:var(--ink-2);line-height:1.5;cursor:pointer}
.achrecap{font-size:13px;color:var(--ink-2);line-height:1.6;background:var(--surface-2);
border-radius:8px;padding:11px 13px;min-height:22px}
.btn{padding:9px 14px;font-family:inherit;font-size:13.5px;font-weight:500;border:1px solid var(--line);
border-radius:7px;background:var(--surface);color:var(--ink);cursor:pointer}
.btn:hover{border-color:var(--ink-3)}
.btn.pri{background:var(--iris);border-color:var(--iris);color:#fff;font-weight:600}
.btn.pri:disabled{opacity:.45;cursor:not-allowed}
.info{background:var(--iris-soft);border-left:3px solid var(--iris);border-radius:0 8px 8px 0;
padding:12px 16px;font-size:13.5px;color:var(--ink-2);line-height:1.6;margin:0 0 18px;max-width:88ch}
.info b{color:var(--ink)}

__AIDECSS__
</style></head><body>
<div class="app">

<aside class="side">
  <div class="logo"><div class="n">Perfumes Trade</div><div class="s">ERP</div></div>
  <nav>
    <span class="navlab">Produits</span>
__BARRE__
  </nav>
  <div class="sfoot"><div id="sfu" class="sfu"></div><span id="sfoot">__TOTAL__ références · __ENSTOCK__ en stock · __UNITES__ unités</span>
  <div class="ver" title="Si cette date n'est pas la derni&egrave;re, recharge avec Cmd+Option+R">version du __VERSION__</div>
    <div class="sfline" id="sfline"></div></div>
</aside>

<div class="main"><div class="wrap">

<header class="pg">
  <div><div class="eyebrow">__EYEBROW__</div><h1>Comptage et écarts</h1>__SOUS__</div>
  <div class="mono" style="font-size:11.5px;color:var(--ink-2);text-align:right;line-height:1.7">
    Partagé en direct avec l'équipe<br>Chaque comptage est signé à ton nom
  </div>
</header>

<div id="impban" class="impban" hidden></div>

<section>
  <div class="stats">
    <div class="stat"><div class="n" id="s-enstock">—</div><div class="l">références en stock</div></div>
    <div class="stat"><div class="n" id="s-zero">—</div><div class="l">à zéro — l'historique<br><span style="color:var(--ink-3)">à confirmer aussi</span></div></div>
    <div class="stat g"><div class="n" id="s-ok">—</div><div class="l">vérifiées physiquement</div></div>
    <div class="stat c"><div class="n" id="s-capnon">—</div><div class="l">capital en stock non vérifié</div></div>
  </div>
</section>

<section>
  <div class="hero">
    <div class="hl">
      <div class="ht"><h3>Compte ce qui porte l'argent</h3>
        <span class="hs" id="hs">Lot à compter, trié par capital en jeu, jamais vérifié d'abord.</span></div>
      <div class="pal" id="pal"></div>
      <button class="hq" id="hq" title="Pourquoi ?" aria-label="Pourquoi">?</button>
    </div>
    <p class="hx" id="hx" hidden>Compter <span id="c-nb">—</span> références prend des jours et personne ne le fera.
    Mais le stock est très concentré : <b><span id="c-lot">200</span> références portent
    <span id="c-pct">—</span> % du capital</b>. En une demi-journée sur les bonnes étagères, on sait si
    l'inventaire dit vrai là où ça compte.</p>
  </div>
</section>

<section>
  <div class="shead">
    <h2>Feuille de comptage</h2>
    <span class="count" id="cnt"></span>
  </div>
  <p class="vhint" id="vhint" data-nolang></p>
  <div class="tools">
    <input type="search" id="q" autocomplete="off" placeholder="Rechercher une marque, un nom, un code-barres… ou scanner" aria-label="Rechercher">
  <div id="scan" class="scan" hidden></div>
    <select id="fs"><option value="" id="o-all" selected>Tout</option>
      <option value="in" id="o-in">En stock</option>
      <option value="out" id="o-out">Historique, annoncées à zéro</option></select>
    <select id="fv"><option value="">Tous les statuts</option>
      <option value="non">Jamais vérifiées</option><option value="doute">À vérifier</option>
      <option value="ok">Déjà vérifiées</option></select>
    <select id="fe"><option value="">Tout afficher</option>
      <option value="todo">Reste à compter</option><option value="done">Déjà comptées</option>
      <option value="gap">Avec écart</option></select>
    <select id="ftri" title="L'ordre de la liste"><option value="">Trier : capital en jeu</option>
      <option value="nom|asc">Nom, de A à Z</option><option value="nom|desc">Nom, de Z à A</option>
      <option value="th|desc">Stock, du plus grand</option><option value="th|asc">Stock, du plus petit</option></select>
    <span id="exp"></span>
    <button onclick="window.print()">Imprimer</button>
    <button id="raz">Effacer la saisie</button>
    <button id="neuf">Préparer un inventaire…</button>
    <button id="majf" title="Un fichier Excel ou CSV, ou les lignes collées depuis le Google Sheet">Mettre à jour depuis un fichier…</button>
  </div>

  <div class="bilan" id="bilan"></div>
  
<div class="ov" id="impov"><div class="mod" style="max-width:760px">
  <div class="mh"><h2>Mettre à jour l'inventaire depuis un fichier</h2>
    <button class="x" id="impx">&times;</button></div>
  <div class="mb">
    <p class="hint">Dépose un fichier <b>Excel (.xlsx)</b> ou <b>CSV</b> — ou colle directement
    les lignes du tableur. La première ligne doit porter les noms de colonnes :
    je reconnais <b>code-barres</b>, <b>nom</b>, <b>marque</b>, <b>contenance</b>, <b>type</b>,
    <b>genre</b>, <b>quantité</b> et <b>prix d'achat</b>, en français comme en anglais,
    quelle que soit la casse ou l'ordre.</p>
    <input type="file" id="impfile" style="font-size:12.5px">
    <div class="xlong" id="imponglets" hidden></div>
    <textarea id="imptxt" placeholder="…ou colle ici les lignes du tableur"
      style="min-height:150px"></textarea>
    <div id="impres"></div>
    <label class="chk" id="impremp-l"><input type="checkbox" id="impremp">
      <span><b>Remplacer tout l'inventaire</b> par ce fichier. Décoché, le fichier ne fait que
      mettre à jour les quantités des références qu'il contient et ajouter celles qui manquent.</span></label>
  </div>
  <div class="mf"><span class="msg" id="impmsg"></span>
    <button class="btn" id="impann">Annuler</button>
    <button class="btn pri" id="impok" disabled>Mettre l'inventaire à jour</button></div>
</div></div>
<div class="ov" id="invov">
   <div class="mod" style="max-width:640px">
    <div class="mh"><h2>Préparer un inventaire</h2><button class="x" id="invx">&times;</button></div>
    <div class="mb">
     <p class="why" style="margin:0 0 4px">Chaque parfum porte une étiquette dans SAM :
     <b>« quelqu'un a compté les flacons »</b> ou <b>« personne ne les a comptés »</b>.
     C'est elle qui décide de ce qui apparaît dans la colonne « Jamais vérifiées ».</p>
     <p class="why" style="margin:0 0 16px">Le problème : <b><span id="inv-faux">—</span> portent l'étiquette
     « compté » alors que personne ne les a comptés.</b> C'est une colonne du fichier Excel de départ qui l'affirmait,
     et SAM l'a reprise telle quelle. Tant que ces fausses étiquettes sont là, la feuille de comptage
     dit à l'équipe qu'il n'y a presque rien à faire — alors que tout est à faire.
     Ce bouton enlève les fausses étiquettes.</p>
     <div class="fld"><label>Quelles étiquettes on enlève</label>
      <select id="inv-quoi">
       <option value="fichier">Seulement les fausses — celles qui viennent du fichier Excel &nbsp;(à choisir)</option>
       <option value="tout">Toutes — y compris les comptages réellement faits dans SAM</option>
       <option value="filtre">Seulement les lignes affichées à l'écran en ce moment</option>
      </select></div>
     <label class="cb" style="display:flex;gap:9px;align-items:flex-start;margin:14px 0">
      <input type="checkbox" id="inv-saisie" checked>
      <span>Effacer aussi les chiffres déjà tapés dans la colonne « Compté » de cette feuille</span></label>
     <div class="achrecap" id="inv-recap"></div>
     <p class="why" style="margin:14px 0 0"><b>Aucune quantité en stock ne change.</b> Si un parfum est à
     7 flacons, il reste à 7 flacons. On ne touche qu'à l'étiquette. C'est écrit au journal, et le comptage
     se refait normalement ensuite, référence par référence.</p>
    </div>
    <div class="mf"><button class="btn" id="inv-ann">Annuler</button>
     <button class="btn pri" id="inv-ok">Enlever les étiquettes</button></div>
   </div>
  </div>

  <div class="tw"><div class="tscroll af"><table>
    <thead><tr>
      <th class="no o3">N°</th><th data-tri="nom">Produit</th><th data-tri="statut" class="o4">Statut</th><th class="num" data-tri="th">Théorique</th>
      <th class="num" data-tri="compte">Compté</th><th class="num" data-tri="ecart">Écart</th><th class="num o2" data-tri="val">Valeur écart</th>
      <th class="num o1" data-tri="cap">Capital</th>
      <th class="num pv o5" hidden data-tri="pvr">PV détail</th><th class="num pv o5" hidden data-tri="pvw">PV gros</th>
    </tr></thead>
    <tbody id="tb"></tbody>
  </table></div></div>
  <p class="sdesc" id="plus" style="text-align:center;padding:8px 0"></p>

  <div class="note" style="background:var(--iris-soft);border-left-color:var(--iris)">
    <b>Pourquoi compter aussi les références annoncées à zéro.</b> Il y en a <span id="z-nb">—</span>, et
    <b><span id="z-non">—</span> d'entre elles n'ont jamais été vérifiées</b> : « zéro » n'est pas un fait constaté,
    c'est une supposition héritée du fichier. Une ligne à zéro qui contient en réalité des flacons,
    c'est du stock invisible — donc de l'argent immédiatement vendable qu'on ignore posséder.
    Le comptage ne peut y apporter que de la bonne nouvelle. Choisis « Annoncées à zéro »
    dans le premier menu pour les passer en revue.
  </div>

  <div class="note">
    <b>Ce que fait cette page.</b> Chaque quantité comptée est enregistrée sur le serveur de l'ERP :
    les autres postes la voient, et le journal la signe avec ton nom et l'heure.
    « Exporter » donne en plus un fichier du lot, pour garder une trace.
  </div>
</section>

<footer><span><span id="f-total">—</span> références · triées par capital en jeu, les jamais vérifiées en tête</span>
<span class="mono">RUBRIQUE STOCK</span></footer>

</div></div></div>

<script>__VOCAB__</script>
<script src="donnees/langue.js?v=__VER__"></script>
<script>
/* le menu réglé et la langue de l'écran, AVANT le code de la page : rien ne saute, rien n'est vu dans une autre langue */
__IDENT_TOT__
__MENU__
__LANGUE__
</script>
<script src="donnees/inventaire.js?v=__VER__"></script>__GARDE__
<script>
__FUSION__
__COMPTES__
__IDENT__
__FILE_AUTO__
__SAUVE__
__XLSX__
__SORTIE__
let P=__DATA__.map(r=>({bc:r[0],nom:r[1],marque:r[2],ml:r[3],type:r[4],
 qte:r[5],pa:r[6],cap:r[7],v:r[8],cle:r[9],pvr:r[10],pvw:r[11]}));
/* Si un inventaire a été importé sur ce poste, c'est lui qui fait foi. */
(function(){ try{
  /* Perfume City : son stock est un magasin PARTAGÉ (pc-stock-v1), le même pour Kim et pour Sam */
  let L=null;
  if('__CIBLE__'==='pc') L=pcsRows();
  else { const t=localStorage.getItem('inventaire-local-__CIBLE__-v1'); if(t) L=JSON.parse(t); }
  if(Array.isArray(L)) P=L.map(r=>({bc:r[0],nom:r[1],marque:r[2],ml:r[3],type:r[4],
    qte:r[5],pa:r[6],cap:r[7],v:r[8],cle:r[9],pvr:r[10],pvw:r[11]}));
}catch(e){} })();
/* Les parfums ajoutés dans l'ERP (fiche créée à la main, ou par la mise à jour du Sheet
   du 30 sept. 2026) n'étaient pas dans l'inventaire de l'entrepôt : on ne pouvait ni les
   voir ni les compter. Ils y entrent, avec leur quantité. */
if('__CIBLE__'==='pt'){ try{
  const A=(typeof lit==='function'?lit('articles-ajoutes-v1',[]):JSON.parse(localStorage.getItem('articles-ajoutes-v1')||'[]'))||[];
  const deja=new Set(P.map(p=>p.cle));
  (Array.isArray(A)?A:[]).forEach(o=>{ if(!o||!o.id||deja.has(o.id)) return;
    const q=+o.qte||0, pa=o.pa==null||o.pa===''?null:+o.pa;
    P.push({bc:String(o.bc||''),nom:o.nom||'',marque:o.marque||'',ml:String(o.ml||''),type:String(o.type||'').toUpperCase(),
      qte:q,pa,cap:pa!=null?q*pa:0,v:'non',cle:o.id,pvr:o.pvr==null||o.pvr===''?null:+o.pvr,pvw:o.pvw==null||o.pvw===''?null:+o.pvw,aj:true}); });
}catch(e){} }
const PAL=__PAL__;
const KEY='comptage-parfums-v1';
const VER_URL='__VER__';
const $=i=>document.getElementById(i);
const VL={ok:['Vérifiée','ok'],non:['Jamais vérifiée','non'],doute:['À vérifier','doute']};
const vl=v=>VL[v]||VL.non;
let saisie={}, lot=0, shown=0;
const PAGE=150;

saisie=lit(KEY,{}); if(!saisie||typeof saisie!=='object') saisie=base(KEY,{});
const sauve=()=>ecrit(KEY,saisie);
/* 10 nov. 2026 (Igal : « ils ont rempli les chiffres de l'inventaire, c'est toujours Jamais vérifiée ») : le comptage était rangé par
   code-barres. Les 50 parfums SANS code-barres partageaient donc la même case : le chiffre tapé sur l'un s'affichait sur tous, et
   s'enregistrait sur le premier de la liste. Chaque ligne a maintenant sa clé : le code-barres, sinon l'identifiant de la fiche.
   L'ancienne case commune (clé vide) ne veut rien dire : elle est retirée. */
const kc=p=>p.bc?String(p.bc):'#'+p.cle;
const kSel=k=>`.cnt[data-bc="${(window.CSS&&CSS.escape)?CSS.escape(k):k}"]`;
if(saisie&&saisie['']!=null){ delete saisie['']; try{ sauve(); }catch(e){} }

const nf=n=>n.toLocaleString('fr-FR');
/* Le dollar (Igal, 30 sept. 2026 : « le dollar est décalé ») : une espace INSÉCABLE entre le
   montant et le $, pour que le $ ne parte jamais seul à la ligne suivante. Le format reste
   « 3 837,50 $ » : le dictionnaire de traduction reconnaît les phrases sur ce modèle. */
const _usd=(v,d)=>{ if(v==null) return '—'; const n=Number(v); 
  return n.toLocaleString('fr-FR',{minimumFractionDigits:d,maximumFractionDigits:d})+' $'; };
const money=n=>_usd(n,0);
const money2=n=>_usd(n,2);
const esc=s=>String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));

/* Les chiffres du haut se comptent sur la liste réellement affichée : après un
   import, une vente ou un comptage, ils restent vrais. */
function chiffres(){
  /* le stock d'aujourd'hui (ventes, comptages, import du Sheet), pas celui du fichier de
     départ : le haut de page disait 1 892 en stock quand la liste en montrait 1 863 */
  const qn=x=>{ try{ return qteTh(x); }catch(e){ return x.qte; } };
  const enstock=P.filter(x=>qn(x)>0).length, zero=P.length-enstock;
  const ok=P.filter(x=>x.v==='ok').length;
  /* 6 nov. 2026 (Igal : « tout doit être fixé par rapport au prix du catalogue ») : le capital à
     recompter se calcule avec le prix d'achat de la fiche Catalogue, plus avec celui du fichier de départ */
  const capx=x=>{ try{ return capEff(x); }catch(e){ return x.cap||0; } };
  const capnon=P.filter(x=>x.v!=='ok'&&qn(x)>0).reduce((s,x)=>s+capx(x),0);
  const znon=P.filter(x=>qn(x)===0&&x.v!=='ok').length;
  const set=(id,v)=>{ const e=$(id); if(e) e.textContent=v; };
  set('s-enstock',nf(enstock)); set('s-zero',nf(zero));
  /* le menu : les parfums EN STOCK pas encore vérifiés (Igal, 1er oct. 2026) — il descend à
     chaque comptage et tombe à 0 quand tout le stock a été recompté */
  if('__CIBLE__'==='pt'){ window.__CT_INV_PAGE=true; set('ct-inventaire',nf(P.filter(x=>x.v!=='ok'&&qn(x)>0).length)); }
  set('s-ok',nf(ok)); set('s-capnon',money(Math.round(capnon)));
  set('f-total',nf(P.length)); set('c-nb',nf(P.length));
  set('z-nb',nf(zero)); set('z-non',nf(znon));
  const o=(id,t)=>{ const e=$(id); if(e) e.textContent=t; };
  o('o-in','En stock ('+nf(enstock)+')');
  o('o-out','Historique, annoncées à zéro ('+nf(zero)+')');
  o('o-all','Tout ('+nf(P.length)+')');
  /* On n'écrit QUE les chiffres, dans leur propre span. Avant, cette fonction
     réécrivait tout le pied de la barre et recopiait #sfu par innerHTML : le nom
     et le rôle revenaient, mais le bouton « Se déconnecter » perdait son clic —
     une copie d'innerHTML ne transporte pas les écouteurs. Sur Inventaire, le
     bouton était donc là et mort. Le tampon de version et le bouton d'aide
     étaient emportés au passage. */
  const sfo=document.getElementById('sfoot');
  if(sfo){ const u=P.reduce((s,x)=>s+(qn(x)||0),0);
    sfo.innerHTML=nf(P.length)+' références · '+nf(enstock)+' en stock · '+nf(u)+' unités'; }
}
chiffres();

$('pal').innerHTML=Object.entries(PAL).map(([n,p])=>
 `<button class="pil" data-n="${n}" title="${n} références = ${p} % du capital"><b>${n}</b>${p} %</button>`).join('')
 +`<button class="pil" data-n="0" title="Toutes les références"><b>Tout</b>${nf(P.length)}</button>`;
/* l'explication, repliée : le « ? » l'ouvre, et les chiffres viennent des vrais lots */
(function(){
  const ent=Object.entries(PAL), k=ent.find(([n])=>+n===200)||ent[ent.length-1];
  if(k){ $('c-lot').textContent=k[0]; $('c-pct').textContent=String(k[1]).replace('.',','); }
  $('hq').onclick=()=>{ const o=$('hx').hidden; $('hx').hidden=!o; $('hq').classList.toggle('on',o); };
})();

function filtre(){
  const q=$('q').value.trim().toLowerCase(), fv=$('fv').value, fe=$('fe').value, st=$('fs').value;
  /* 28 sept. : avec un texte tapé, « en stock » ne cache plus un parfum à 0 — au comptage,
     c'est justement le flacon trouvé sur l'étagère que l'outil croit épuisé */
  let l=P.filter(p=>(!st||(st==='in'?(q||qteTh(p)>0):qteTh(p)===0))&&(!fv||p.v===fv)&&
    (!q||q.split(/\s+/).filter(Boolean).every(m=>(p.nom+' '+p.marque+' '+p.bc).toLowerCase().includes(m))));
  if(lot>0 && !q && !fv && st==='in') l=l.slice(0,lot);
  l=trie(l);
  if(fe){
    l=l.filter(p=>{
      const c=cpt(p);
      if(fe==='todo') return c==null||c==='';
      if(fe==='done') return c!=null&&c!=='';
      if(fe==='gap')  return c!=null&&c!==''&&(+c)!==qteTh(p);
      return true;
    });
  }
  return l;
}

/* Le tri : un clic sur un titre trie croissant, un second décroissant, un
   troisième remet l'ordre du fichier. Retenu sur le poste. */
const K_TRI='comptage-tri-__CIBLE__-v1';
let TRI=null; try{ TRI=JSON.parse(localStorage.getItem(K_TRI)||'null'); }catch(e){}
const valTri={
  nom:   p=>(p.marque||'')+' '+(p.nom||''),
  statut:p=>vl(p.v)[0],
  th:    p=>qteAtt(p),
  compte:p=>{ const c=cpt(p); return (c==null||c==='')?null:+c; },
  ecart: p=>{ const c=cpt(p); return (c==null||c==='')?null:(+c)-qtePhys(p); },
  val:   p=>{ const c=cpt(p); return (c==null||c===''||paEff(p)==null)?null:((+c)-qtePhys(p))*paEff(p); },
  cap:   p=>capEff(p),
  pvr:   p=>p.pvr==null?null:+p.pvr,
  pvw:   p=>p.pvw==null?null:+p.pvw };
function trie(l){
  if(!TRI||!valTri[TRI.k]) return l;
  const f=valTri[TRI.k], s=TRI.sens==='desc'?-1:1;
  return l.slice().sort((a,b)=>{
    const x=f(a), y=f(b);
    if(x==null&&y==null) return 0;
    if(x==null) return 1; if(y==null) return -1;   /* les vides toujours à la fin */
    if(typeof x==='string') return s*x.localeCompare(y,'fr',{sensitivity:'base'});
    return s*(x-y);
  });
}
function peintTri(){
  document.querySelectorAll('thead th[data-tri]').forEach(th=>{
    th.classList.remove('tri-asc','tri-desc');
    if(TRI&&th.dataset.tri===TRI.k) th.classList.add(TRI.sens==='desc'?'tri-desc':'tri-asc');
  });
  /* 3 nov. 2026 (Igal) : le même tri, visible dans un menu au-dessus de la liste — un clic sur un titre de colonne et le menu
     disent toujours la même chose ; un tri que le menu ne propose pas (capital, écart…) le remet sur sa première ligne */
  const m=$('ftri'); if(m){ const v=TRI?TRI.k+'|'+TRI.sens:''; m.value=[...m.options].some(o=>o.value===v)?v:''; m.classList.toggle('on',!!m.value); }
}
{ const m=$('ftri'); if(m) m.onchange=()=>{ const [k,sens]=m.value.split('|'); TRI=k?{k,sens:sens||'asc'}:null;
    try{ TRI?localStorage.setItem(K_TRI,JSON.stringify(TRI)):localStorage.removeItem(K_TRI); }catch(e){}
    peintTri(); rend(true); }; }
document.querySelectorAll('thead th[data-tri]').forEach(th=>th.onclick=()=>{
  const k=th.dataset.tri;
  if(!TRI||TRI.k!==k) TRI={k,sens:'asc'};
  else if(TRI.sens==='asc') TRI={k,sens:'desc'};
  else TRI=null;
  try{ TRI?localStorage.setItem(K_TRI,JSON.stringify(TRI)):localStorage.removeItem(K_TRI); }catch(e){}
  peintTri(); rend(true);
});
peintTri();

function ligne(p,i){
  const c=cpt(p);
  const rempli=c!=null&&c!=='';
  const ec=rempli?(+c)-qtePhys(p):null;
  const val=rempli&&paEff(p)!=null?ec*paEff(p):null;
  const vit=tst(p);
  const cls=!rempli?'':(ec===0?'done':'ecart');
  const gcls=ec==null?'zero':ec>0?'pos':ec<0?'neg':'zero';
  return `<tr class="${cls}" data-bc="${esc(kc(p))}">
   <td class="no o3">${nf((i||0)+1)}</td>
   <td><div class="pd" data-fiche="${esc(p.cle||'')}" title="${esc(typeof L3==='function'?L3('Ouvrir la fiche du parfum','Open the perfume card','Abrir la ficha del perfume'):'Ouvrir la fiche du parfum')}"><span class="b">${esc(p.marque)}</span>
     <span class="n">${esc(p.nom)}</span>
     <span class="m">${[p.ml?p.ml+' oz':'',p.type].filter(Boolean).join(' · ')} &nbsp;<span class="code">${p.bc}</span></span></div></td>
   <td class="o4"><span class="tag ${vl(p.v)[1]}">${vl(p.v)[0]}</span></td>
   <td class="num">${qteAtt(p)===0?'<span style="color:var(--ink-3)">0</span>':nf(qteAtt(p))}${
       vit?`<span class="vit" title="${nf(vit)} tester${vit>1?'s':''}, non vendable${vit>1?'s':''} — à compter quand même">+${nf(vit)} tester${vit>1?'s':''}</span>`:''}</td>
   <td class="num"><input class="cnt${rempli?' filled':''}" type="number" min="0" inputmode="numeric"
       value="${rempli?c:''}" data-bc="${esc(kc(p))}" aria-label="Quantité comptée"></td>
   <td class="num"><span class="gap ${gcls}">${ec==null?'—':(ec>0?'+':'')+nf(ec)}</span></td>
   <td class="num o2"><span class="gap ${gcls}">${val==null?'—':(val>0?'+':'')+money(val)}</span></td>
   <td class="num o1" style="color:var(--ink-3)">${money(capEff(p))}</td>
   ${AVEC_PV?`<td class="num pv o5">${p.pvr==null?'—':money2(p.pvr)}</td><td class="num pv o5">${p.pvw==null?'—':money2(p.pvw)}</td>`:''}
  </tr>`;
}

function bilan(l){
  const f=l.filter(p=>cpt(p)!=null&&cpt(p)!=='');
  const g=f.filter(p=>(+cpt(p))!==qtePhys(p));
  const vg=g.reduce((a,p)=>a+((+cpt(p))-qtePhys(p))*(paEff(p)||0),0);
  const capf=f.reduce((a,p)=>a+capEff(p),0);
  $('bilan').innerHTML=`
   <div><span class="v">${nf(f.length)} / ${nf(l.length)}</span><span class="k">références comptées</span></div>
   <div><span class="v" style="color:var(--iris)">${money(capf)}</span><span class="k">capital vérifié</span></div>
`;
}

/* Les prix de vente n'apparaissent que si les lignes en portent : l'entrepôt
   n'en a pas (ils vivent dans le catalogue), Perfume City si — son fichier
   est le seul endroit où ils existent. */
let AVEC_PV=false;
function majPV(){
  AVEC_PV=P.some(p=>p.pvr!=null||p.pvw!=null);
  document.querySelectorAll('th.pv').forEach(th=>{ th.hidden=!AVEC_PV; });
}
function rend(reset){
  majPV();
  const l=filtre();
  if(reset) shown=PAGE;
  $('tb').innerHTML=l.slice(0,shown).map((p,i)=>ligne(p,i)).join('');
  $('plus').innerHTML=l.length>shown
    ? `<button id="mp">Afficher ${Math.min(PAGE,l.length-shown)} de plus (${nf(l.length-shown)} restantes)</button>` : '';
  const mp=$('mp'); if(mp) mp.onclick=()=>{shown+=PAGE;rend(false);};
  $('cnt').textContent=`${nf(l.length)} références affichées`;
  bilan(l);
}

/* ---- Compter une référence, c'est la confirmer ----
   La saisie d'un comptage passe le statut de la fiche à « comptage vérifié »
   et écrit la ligne dans le journal des actions, avec le nom et l'heure. */
/* Perfume City a SON stock : ses fiches corrigées vivent à part (27 sept. 2026). Elles
   partageaient la même boîte que l'entrepôt, avec les mêmes clés (« b » + code-barres) :
   compter 3 flacons chez Perfume City aurait mis l'entrepôt à 3 — et, depuis que le stock
   part tout seul sur les sites, les sites avec. */
const KMOD='__KMOD__', KUSR='crm-utilisateur-v1', KJOU='crm-journal-v1';
let MOD=lit(KMOD,{}); if(!MOD||typeof MOD!=='object'||Array.isArray(MOD)) MOD=base(KMOD,{});
/* L'état « vérifiée / à compter » corrigé dans l'ERP (comptage, « nouvel inventaire », démarrage
   du 1er oct. 2026 où tout est repassé « à compter ») l'emporte sur celui du fichier de départ.
   La liste et le chiffre « vérifiées » lisaient le fichier : 1 263 « vérifiées » restaient affichées. */
P.forEach(p=>{ const m=MOD[p.cle]; if(m&&m.verif!==undefined) p.v=m.verif; });
/* 30 oct. 2026 : le nom, la marque, la contenance et le type changés dans la fiche du Catalogue se voient ici aussi
   (avant, l'Inventaire gardait « Nom (Clone de…) » quand le Catalogue disait « Nom ») */
/* 10 nov. 2026 (Igal : « Sam a rajouté le code-barres sur la fiche, mais l'inventaire ne le trouvait pas ») : un parfum arrivé
   sans code-barres prend celui que Sam a posé sur sa fiche du Catalogue — la recherche et la douchette le trouvent ; un chiffre
   déjà compté sous l'identifiant de la fiche suit le code-barres. */
function bcFiche(p){ const m=MOD[p.cle]; if(p.bc||!m||!m.bc) return; const b=String(m.bc).trim(); if(!b) return;
  p.bc=b; try{ if(saisie['#'+p.cle]!=null&&saisie[b]==null){ saisie[b]=saisie['#'+p.cle]; delete saisie['#'+p.cle]; sauve(); } }catch(e){} }
P.forEach(p=>{ const m=MOD[p.cle]; if(!m) return; ['nom','marque','ml','type'].forEach(k=>{ if(m[k]!=null&&m[k]!=='') p[k]=(k==='type')?String(m[k]).toUpperCase():String(m[k]); }); });
  P.forEach(bcFiche);
/* 6 nov. 2026 (Sam : Asad à 18,50 $ de gros au Catalogue, 18 $ dans l'Inventaire) : c'est le Catalogue qui fixe les prix.
   Le prix retail et le prix de gros changés dans la fiche se voient ici aussi — l'Inventaire ne garde plus ceux du fichier. */
if('__CIBLE__'==='pt') P.forEach(p=>{ const m=MOD[p.cle]; if(!m) return; if(m.pvr!=null&&m.pvr!=='') p.pvr=+m.pvr; if(m.pvw!=null&&m.pvw!=='') p.pvw=+m.pvw; });
/* une fiche retirée du catalogue (« Retirer du catalogue », Patron/admin) disparaît aussi de l'Inventaire : Sam,
   30 oct. 2026, « supprime-les définitivement du stock ». Elle reste dans l'historique (ventes, achats, journal). */
if('__CIBLE__'==='pt') P=P.filter(p=>!(MOD[p.cle]&&MOD[p.cle].masque));

/* Le stock théorique n'est pas celui du fichier : c'est celui d'aujourd'hui, une fois
   comptées les ventes, les réceptions et l'import du tableur. Sans ça, la feuille de
   comptage annonce des écarts qui n'existent pas. */
let EXT={q:{}}; try{ EXT=Object.assign({q:{}},JSON.parse(localStorage.getItem('stock-externe-v1')||'{}')); }catch(e){}
function qteTh(p){
  const m=MOD[p.cle];
  if(m&&m.qte!=null) return +m.qte;
  /* 31 oct. 2026 (Sam : « l'inventaire de Perfume City est faux ») : stock-externe-v1 est le stock de L'ENTREPÔT (import du
     Google Sheet de Sam). La page Perfume City le lisait aussi : un parfum affichait 15 (l'entrepôt) au lieu de 1 (la boutique).
     Perfume City n'a que son propre stock (pc-stock-v1). */
  const e='__CIBLE__'==='pt'&&EXT.q?EXT.q[p.bc]:null;
  if(e!=null) return +e;
  return p.qte;
}
/* Le théorique affiché face à un comptage, c'est celui d'AVANT le comptage : sinon
   l'écart tombe à zéro dès qu'on l'a saisi, et la colonne ne sert plus à rien. */
setTimeout(()=>{ try{ chiffres(); }catch(e){} },0);
/* LE FIL EN DIRECT (1er oct. 2026) : un comptage, une vente ou un achat fait sur un autre poste
   arrive dans la seconde ; la liste se relit et se redessine sur place (jamais pendant une
   saisie : le champ qu'on est en train de remplir garde la main, un bandeau propose de recharger) */
/* 10 nov. 2026 (Igal : « sur la partie inventaire, cliquer sur le produit et avoir le panneau latéral avec la fiche produit ») :
   la fiche du Catalogue elle-même, en panneau à droite (comme dans la Cote) ; à sa fermeture, la liste se relit */
document.addEventListener('click',e=>{ const d=e.target.closest&&e.target.closest('.pd[data-fiche]');
  if(!d||!d.dataset.fiche||typeof ficheFenetre!=='function') return;
  ficheFenetre(d.dataset.fiche,()=>{ try{ window.__rafraichir(); }catch(_){} }); });
window.__rafraichir=()=>{ const y=window.scrollY;
  { const m=lit(KMOD,{}); if(m&&typeof m==='object'&&!Array.isArray(m)) MOD=m; }
  try{ EXT=Object.assign({q:{}},JSON.parse(localStorage.getItem('stock-externe-v1')||'{}')); }catch(e){}
  P.forEach(p=>{ const m=MOD[p.cle]; if(m&&m.verif!==undefined) p.v=m.verif; });
  P.forEach(p=>{ const m=MOD[p.cle]; if(!m) return; ['nom','marque','ml','type'].forEach(k=>{ if(m[k]!=null&&m[k]!=='') p[k]=(k==='type')?String(m[k]).toUpperCase():String(m[k]); }); });
  P.forEach(bcFiche);
/* 6 nov. 2026 (Sam : Asad à 18,50 $ de gros au Catalogue, 18 $ dans l'Inventaire) : c'est le Catalogue qui fixe les prix.
   Le prix retail et le prix de gros changés dans la fiche se voient ici aussi — l'Inventaire ne garde plus ceux du fichier. */
if('__CIBLE__'==='pt') P.forEach(p=>{ const m=MOD[p.cle]; if(!m) return; if(m.pvr!=null&&m.pvr!=='') p.pvr=+m.pvr; if(m.pvw!=null&&m.pvw!=='') p.pvw=+m.pvw; });
  if('__CIBLE__'==='pt') P=P.filter(p=>!(MOD[p.cle]&&MOD[p.cle].masque));
  { const s=lit(KEY,{}); if(s&&typeof s==='object') saisie=s; }
  { const j=lit(KJOU,[]); if(Array.isArray(j)) JOU=j; }
  try{ rend(false); }catch(e){} try{ chiffres(); }catch(e){} window.scrollTo(0,y); };
/* UN COMPTAGE PÉRIMÉ (Sam, 30 oct. 2026 : « ce parfum, j'en ai acheté plusieurs, l'Inventaire dit 0 et
   vérifié ») : le comptage du 2 oct. disait 0, puis une réception en a mis 87. L'Inventaire montrait encore le
   théorique d'AVANT ce comptage (1) et la case comptée (0). Dès que le stock a bougé depuis le comptage (vente,
   réception, correction), ce comptage ne dit plus rien du rayon : la ligne montre le stock d'aujourd'hui, la case
   est vide, et le prochain comptage repart de ce stock-là. */
/* ce que la case « compté » contient pour cette ligne — rien si le comptage est périmé */
function cpt(p){ return comptagePerime(p)?undefined:saisie[kc(p)]; }
function comptagePerime(p){ const m=MOD[p.cle]; return !!(m&&m.qteC!=null&&(m.qte==null||+m.qte!==+m.qteC)); }
function qteAtt(p){ const m=MOD[p.cle];
  return (m&&m.qteC!=null&&m.qteTh0!=null&&!comptagePerime(p))?+m.qteTh0:qteTh(p); }
/* ---- Les flacons de vitrine (Perfume City) ----
   Quand Perfumes Trade sort 5 flacons pour la boutique, un part en vitrine comme
   testeur : 4 sont vendables, mais 5 sont physiquement là. Le stock compte le
   vendable ; la personne qui compte, elle, en voit 5. On garde donc les deux :
   la colonne « Théorique » affiche le vendable et signale la vitrine, et l'écart
   se calcule sur le total physique — sinon chaque comptage annonce un faux écart. */
const CIBLE='__CIBLE__';
let TSTPC={}; if(CIBLE==='pc'){ const t=lit('testeurs-pc-v1',{}); if(t&&typeof t==='object'&&!Array.isArray(t)) TSTPC=t; }
function tst(p){
  if(CIBLE!=='pc') return 0;
  const k=p.bc?String(p.bc).replace(/^0+/,''):'';
  const e=(k&&TSTPC[k])||TSTPC[p.cle];
  /* 10 nov. 2026 (Igal : « sur tous les parfums, un tester chez Perfume City, pas plus ») : le Sheet importé le 13 oct. portait 95, 72, 60… dans la colonne des testers. Un parfum a un tester, ou aucun : jamais plus, à la lecture comme à l'écriture. */
  return e&&(+e.n>0)?1:0;
}
/* ce qu'on doit trouver en rayon : le vendable plus ce qui est en vitrine */
function qtePhys(p){ return qteAtt(p)+tst(p); }
/* le prix d'achat et le capital en vigueur : la fiche corrigée l'emporte sur le fichier */
function paEff(p){ const m=MOD[p.cle]; return (m&&m.pa!=null)?+m.pa:p.pa; }
function capEff(p){ const a=paEff(p); return a==null?0:qteTh(p)*a; }

let USR=NOM_UTIL;
let JOU=lit(KJOU,[]); if(!Array.isArray(JOU)) JOU=base(KJOU,[]);
function demandeUser(force,action,apres){
  if(force){ fenetreNom('',apres); return USR; }
  if(USR) return USR;
  return signe(action||'', apres||(()=>{}));
}
window.__nomChange.push(v=>{ USR=v; try{ majUser(); }catch(e){} });
function majUser(){ try{ piedSession(); }catch(e){} }

/* ============ IMPORT D'UN FICHIER D'INVENTAIRE ============
   Marche sur les deux rubriques. Sur celle de Perfumes Trade, le fichier met à
   jour les quantités des références existantes. Sur celle de Perfume City, qui
   part vide, c'est lui qui construit l'inventaire.
   Les lignes importées sont gardées dans le navigateur (K_LOCAL) : au prochain
   chargement, la page repart de là. */
const K_LOCAL='inventaire-local-__CIBLE__-v1';
let IMP=null;

const impNorm=s=>String(s||'').toLowerCase()
  .normalize('NFD').replace(/[̀-ͯ]/g,'').replace(/[^a-z0-9]/g,'');
const IMP_COLS={
  bc:['codebarres','codebarre','barcode','upc','ean','sku','abarcode'],
  nom:['nom','name','designation','description','produit','product','bname'],
  marque:['marque','brand','dmarque','dbrand'],
  ml:['contenance','taille','size','oz','ml','cml'],
  type:['type','concentration','etype'],
  genre:['genre','gender','sexe','fgenre'],
  qte:['quantite','qte','quantity','qty','stock','gqte','stockreel','onhand'],
  pa:['prixachat','prixdachat','purchaseprice','cost','costprice','prixunitaire','unitprice','hprixachat',
      'supplierprice','supplier','prixfournisseur','buyprice','coutachat','achat','pa'],
  /* les prix de vente : pas affichés dans cet inventaire (qui compte des flacons),
     mais gardés — pour Perfume City, ce fichier est le seul endroit où ils existent */
  pvr:['pvr','prixretail','retailprice','prixdetail','prixvente','sellingprice','retail','prixdevente'],
  pvw:['pvw','prixwholesale','wholesaleprice','prixgros','prixdegros','wholesale'],
  /* Perfume City : les testeurs (flacons de vitrine) ont leur propre colonne dans le Sheet */
  tst:['testerqty','testeurs','testeur','tester','vitrine']};

function impDecoupe(t){
  const l=t.split(/\r?\n/).filter(x=>x.trim());
  if(!l.length) return [];
  const sep = (l[0].match(/\t/g)||[]).length ? '\t'
            : (l[0].match(/;/g)||[]).length >= (l[0].match(/,/g)||[]).length ? ';' : ',';
  /* un CSV peut contenir des virgules entre guillemets : on les respecte */
  const coupe=ligne=>{
    const out=[]; let cur='', dans=false;
    for(let i=0;i<ligne.length;i++){ const c=ligne[i];
      if(c==='"'){ if(dans&&ligne[i+1]==='"'){ cur+='"'; i++; } else dans=!dans; }
      else if(c===sep && !dans){ out.push(cur); cur=''; }
      else cur+=c; }
    out.push(cur); return out.map(x=>x.trim());
  };
  return l.map(coupe);
}

function impAnalyse(t){
  const L=Array.isArray(t)?t:impDecoupe(t);
  if(L.length<2) return {err:'Il faut au moins une ligne de titres et une ligne de produit.'};
  const tetes=L[0].map(impNorm);
  const idx={};
  for(const [k,noms] of Object.entries(IMP_COLS)){
    idx[k]=tetes.findIndex(h=>noms.includes(h));
    if(idx[k]<0) idx[k]=tetes.findIndex(h=>h&&noms.some(n=>h.startsWith(n)||n.startsWith(h)));
  }
  if(idx.bc<0 && idx.nom<0)
    return {err:'Aucune colonne de code-barres ni de nom reconnue dans la première ligne. Les titres attendus : code-barres, nom, marque, quantité, prix d\'achat.'};
  if(idx.qte<0)
    return {err:'Aucune colonne de quantité reconnue. Il faut une colonne « quantité », « qté », « stock » ou « quantity ».'};
  const nb=v=>{ const x=String(v==null?'':v).replace(/[^0-9.,-]/g,'').replace(/\s/g,'');
    if(!x) return null;
    const p=x.lastIndexOf('.'), c=x.lastIndexOf(',');
    const y = c>p ? x.replace(/\./g,'').replace(',','.') : x.replace(/,/g,'');
    const n=parseFloat(y); return isFinite(n)?n:null; };
  const lignes=[], vides=[];
  for(let i=1;i<L.length;i++){
    const r=L[i]; if(!r.join('').trim()) continue;
    const bc=idx.bc>=0?String(r[idx.bc]||'').replace(/[^0-9]/g,''):'';
    const nom=idx.nom>=0?String(r[idx.nom]||'').trim():'';
    if(!bc && !nom){ vides.push(i+1); continue; }
    const q=nb(r[idx.qte]); if(q==null){ vides.push(i+1); continue; }
    lignes.push({bc, nom: nom||('Sans nom '+bc),
      marque: idx.marque>=0?String(r[idx.marque]||'').trim():'',
      ml: idx.ml>=0?String(r[idx.ml]||'').trim():'',
      type: idx.type>=0?String(r[idx.type]||'').trim():'',
      qte: Math.round(q),
      pa: idx.pa>=0?nb(r[idx.pa]):null,
      pvr: idx.pvr>=0?nb(r[idx.pvr]):null,
      pvw: idx.pvw>=0?nb(r[idx.pvw]):null,
      tst: idx.tst>=0?Math.max(0,Math.round(nb(r[idx.tst])||0)):null});
  }
  if(!lignes.length) return {err:'Aucune ligne exploitable : chaque ligne doit avoir un code-barres ou un nom, et une quantité.'};
  return {lignes, vides, cols:idx, tetes:L[0]};
}

function impPeint(a){
  const el=$('impres');
  if(a.err){ el.innerHTML=`<p class="hint" style="color:var(--crit)"><b>${esc(a.err)}</b></p>`;
    $('impok').disabled=true; IMP=null; return; }
  IMP=a;
  const connus={}; P.forEach(p=>{ if(p.bc) connus[String(p.bc).replace(/^0+/,'')]=1; });
  const dej=a.lignes.filter(l=>l.bc&&connus[l.bc.replace(/^0+/,'')]).length;
  const neuf=a.lignes.length-dej;
  const u=a.lignes.reduce((s,l)=>s+l.qte,0);
  const aPvr=a.cols.pvr>=0, aPvw=a.cols.pvw>=0, aPa=a.cols.pa>=0;
  el.innerHTML=(aPa?'':`<p class="hint" style="color:var(--warn)"><b>Aucune colonne de prix d'achat
      reconnue.</b> Les quantités entreront, mais sans prix la valeur du stock restera vide.
      Titres compris : prix d'achat, cost, supplier price, purchase price.</p>`)
   +`<div class="prev"><table><thead><tr><th>Code-barres</th><th>Nom</th>
      <th>Marque</th><th class="n">Qté</th><th class="n">Achat</th>${aPvr?'<th class="n">PVR</th>':''}${aPvw?'<th class="n">PVW</th>':''}</tr></thead><tbody>${
      a.lignes.slice(0,12).map(l=>`<tr><td>${esc(l.bc||'—')}</td><td>${esc(l.nom)}</td>
      <td>${esc(l.marque||'—')}</td><td class="n">${nf(l.qte)}</td>
      <td class="n">${l.pa==null?'—':money2(l.pa)}</td>${aPvr?`<td class="n">${l.pvr==null?'—':money2(l.pvr)}</td>`:''}${aPvw?`<td class="n">${l.pvw==null?'—':money2(l.pvw)}</td>`:''}</tr>`).join('')}</tbody></table></div>
    <p class="hint"><b>${nf(a.lignes.length)} ligne${a.lignes.length>1?'s':''} lue${a.lignes.length>1?'s':''}</b>
    — ${nf(u)} flacons au total. ${nf(dej)} déjà dans cet inventaire, <b>${nf(neuf)} nouvelle${neuf>1?'s':''}</b>.
    ${a.vides.length?`${a.vides.length} ligne${a.vides.length>1?'s':''} sans code-barres, sans nom ou sans quantité : ignorée${a.vides.length>1?'s':''}.`:''}</p>`;
  $('impok').disabled=false;
}

function impApplique(){
  if(!IMP) return;
  const remp=$('impremp').checked;
  const base0 = remp ? [] : P.map(p=>({bc:p.bc,nom:p.nom,marque:p.marque,ml:p.ml,type:p.type,
                                       qte:p.qte,pa:p.pa,cle:p.cle,pvr:p.pvr,pvw:p.pvw}));
  const par={}; base0.forEach((x,i)=>{ if(x.bc) par[String(x.bc).replace(/^0+/,'')]=i; });
  let maj=0, ajout=0;
  IMP.lignes.forEach(l=>{
    const k=l.bc?String(l.bc).replace(/^0+/,''):null;
    const i=(k!=null&&par[k]!=null)?par[k]:-1;
    if(i>=0){ base0[i].qte=l.qte; if(l.pa!=null) base0[i].pa=l.pa;
      if(l.pvr!=null) base0[i].pvr=l.pvr; if(l.pvw!=null) base0[i].pvw=l.pvw;
      if(l.nom&&!base0[i].nom) base0[i].nom=l.nom; maj++; }
    else { const cle = l.bc ? 'b'+l.bc : 'n-'+impNorm(l.marque+l.nom+l.ml);
      base0.push({bc:l.bc,nom:l.nom,marque:l.marque,ml:l.ml,type:l.type,qte:l.qte,pa:l.pa,cle,
                  pvr:l.pvr,pvw:l.pvw});
      if(k!=null) par[k]=base0.length-1; ajout++; }
  });
  const rows=base0.map(x=>[x.bc,x.nom,x.marque,x.ml,x.type,x.qte,x.pa,
                           (x.pa!=null?x.qte*x.pa:null),'non',x.cle,
                           x.pvr==null?null:x.pvr, x.pvw==null?null:x.pvw]);
  if(CIBLE==='pc'){
    /* Perfume City : magasin partagé (le même pour Kim et Sam) ; « remplacer » vide d'abord */
    if(!pcsSauve(rows,remp)){ $('impmsg').textContent='enregistrement impossible'; return; }
    /* les flacons de vitrine (colonne TESTER QTY du Sheet) */
    if(IMP.cols.tst>=0){ const T=remp?{}:Object.assign({},lit('testeurs-pc-v1',{}));
      if(remp) lit('testeurs-pc-v1',{});
      IMP.lignes.forEach(l=>{ if(l.tst==null) return;
        const k=l.bc?String(l.bc).replace(/^0+/,''):'n-'+impNorm(l.marque+l.nom+l.ml);
        if(l.tst>0) T[k]=Object.assign({},T[k]||{},{n:1,   /* un tester, jamais plus, quoi que dise la colonne */ bc:l.bc||'',ref:((l.marque||'')+' '+(l.nom||'')).trim(),t:new Date().toISOString(),u:(typeof NOM_UTIL!=='undefined'?NOM_UTIL:USR)||''});
        else delete T[k]; });
      ecrit('testeurs-pc-v1',T); }
  } else {
  try{ localStorage.setItem(K_LOCAL,JSON.stringify(rows)); }catch(e){
    $('impmsg').textContent='fichier trop gros pour le navigateur'; return; }
  }
  try{ const J=lit(KJOU,[]);
    J.push({t:new Date().toISOString(),u:(typeof NOM_UTIL!=='undefined'?NOM_UTIL:USR),
            act:'stock',lib:'inventaire importé — __CIBLE_LIB__',ref:'',av:null,
            ap:maj+' mise(s) à jour, '+ajout+' ajout(s)'});
    ecrit(KJOU,J); }catch(e){}
  $('impmsg').textContent='inventaire mis à jour';
  setTimeout(()=>location.reload(),700);
}

/* Tant qu'un fichier importé remplace l'inventaire livré, on le dit — et on
   laisse revenir en arrière. Un remplacement invisible est un piège. */
(function(){
  const b=$('impban'); if(!b) return;
  let t=null; try{ t=localStorage.getItem(K_LOCAL); }catch(e){}
  if(!t) return;
  let n=0; try{ n=JSON.parse(t).length; }catch(e){}
  b.hidden=false;
  b.innerHTML='<span><b>inventaire importé</b> — cette page affiche '+nf(n)+
    ' référence'+(n>1?'s':'')+' venant d\'un fichier, pas de l\'inventaire livré avec l\'outil.</span>'+
    '<button id="impraz">Revenir au fichier d\'origine</button>';
  const r=document.getElementById('impraz');
  if(r) r.onclick=()=>{
    if(!confirm('Revenir à l\'inventaire d\'origine ?\n\nLes lignes importées sont oubliées. Les comptages déjà saisis, eux, restent.')) return;
    try{ localStorage.removeItem(K_LOCAL); }catch(e){}
    try{ const J=lit(KJOU,[]);
      J.push({t:new Date().toISOString(),u:(typeof NOM_UTIL!=='undefined'?NOM_UTIL:USR),
              act:'stock',lib:'retour à l\'inventaire d\'origine — __CIBLE_LIB__',ref:'',av:null,ap:null});
      ecrit(KJOU,J); }catch(e){}
    location.reload();
  };
})();

(function(){
  const ov=$('impov'); if(!ov) return;
  const ferme=()=>ov.classList.remove('on');
  $('impx').onclick=ferme; $('impann').onclick=ferme;
  ov.addEventListener('click',e=>{ if(e.target===ov) ferme(); });
  let t=null;
  $('imptxt').addEventListener('input',()=>{ clearTimeout(t);
    t=setTimeout(()=>{ const v=$('imptxt').value.trim();
      if(v.length<10){ $('impres').innerHTML=''; $('impok').disabled=true; IMP=null; return; }
      impPeint(impAnalyse(v)); },320); });
  $('impfile').addEventListener('change',e=>{ const f=e.target.files[0]; if(!f) return;
    /* un classeur garde son chemin a lui (choix de l'onglet) ; tout le reste —
       CSV, texte, PDF, photo — passe par la porte commune */
    if(xlEstExcel(f)) return impExcel(f);
    impOnglets(null);
    $('impres').innerHTML='<p class="hint">Lecture de '+esc(f.name)+'…</p>';
    lireFichier(f, m=>{ $('impres').innerHTML='<p class="hint">'+esc(m)+'</p>'; })
      .then(t=>{ $('imptxt').value=t; impPeint(impAnalyse(String(t))); })
      .catch(err=>{ $('impres').innerHTML='<p class="hint" style="color:var(--crit)"><b>'+esc(err.message||'Lecture impossible.')+'</b></p>';
        $('impok').disabled=true; IMP=null; });
    e.target.value=''; });

  /* Un classeur Excel : on le lit ici même, et s'il a plusieurs onglets
     (le Google Sheet de Sam en a), on les propose au lieu de deviner. */
  let XLONG=null;
  function impOnglets(o){
    XLONG=o; const z=$('imponglets');
    if(!o||o.length<2){ z.hidden=true; z.innerHTML=''; return; }
    z.hidden=false;
    z.innerHTML='<span class="lab">Onglet</span>'+o.map((t,i)=>
      `<button class="xlb${i===0?' on':''}" data-o="${i}">${esc(t.nom)}`
      +` <span style="opacity:.65">${t.lignes.length}</span></button>`).join('');
  }
  $('imponglets').addEventListener('click',ev=>{
    const b=ev.target.closest('button[data-o]'); if(!b||!XLONG) return;
    [...$('imponglets').querySelectorAll('button')].forEach(x=>x.classList.remove('on'));
    b.classList.add('on');
    impPeint(impAnalyse(XLONG[+b.dataset.o].lignes));
  });
  async function impExcel(f){
    if(!xlsxDispo){
      $('impres').innerHTML='<p class="hint" style="color:var(--crit)"><b>Ce navigateur est trop '
        +'ancien pour lire un .xlsx.</b> Depuis Google Sheets : Fichier → Télécharger → CSV.</p>';
      $('impok').disabled=true; return;
    }
    $('impres').innerHTML='<p class="hint">Lecture du fichier Excel…</p>';
    try{
      const {onglets}=await xlLis(await f.arrayBuffer());
      const utiles=onglets.filter(o=>o.lignes.length>1);
      if(!utiles.length) throw new Error('Aucun onglet ne contient de lignes.');
      $('imptxt').value='';
      impOnglets(utiles);
      impPeint(impAnalyse(utiles[0].lignes));
    }catch(err){
      $('impres').innerHTML='<p class="hint" style="color:var(--crit)"><b>Impossible de lire ce '
        +'fichier Excel.</b> '+esc(err.message||'')+'<br>Essaie en l\'enregistrant à nouveau en '
        +'<b>.xlsx</b>, ou passe par un CSV.</p>';
      $('impok').disabled=true; IMP=null;
    }
  }
  $('impok').onclick=impApplique;
  const b=document.getElementById('majf');
  if(b) b.onclick=()=>{ $('imptxt').value=''; $('impres').innerHTML='';
    $('impmsg').textContent=''; $('impok').disabled=true; IMP=null;
    $('impremp').checked=__REMP0__; ov.classList.add('on'); setTimeout(()=>$('imptxt').focus(),80); };
})();

/* ---- Valider un comptage ----
   Igal, 27 sept. 2026 : « dans la partie inventaire je ne vois pas où on peut valider
   l'inventaire ». Il n'y a pas de bouton : chaque quantité tapée est validée quand on
   quitte sa case. Mais la fonction qui validait avait disparu du fichier (le journal
   aussi) : la case gardait le chiffre, l'écart s'affichait, et RIEN n'était validé —
   ni le stock, ni le statut « comptage vérifié », ni le journal. La revoilà.
   Le comptage physique voit aussi les flacons de vitrine (Perfume City) : le stock
   vendable retenu est le compté moins la vitrine. */
/* dit comment on valide, dans la langue de l'écran (le paragraphe porte du gras) */
try{ document.getElementById('vhint').innerHTML=L3(
  "<b>Pas de bouton « Valider » : chaque quantité est validée dès que tu quittes sa case</b> (Entrée, Tab ou clic ailleurs). Le stock prend le chiffre compté, la ligne passe en « comptage vérifié » et c'est écrit au journal avec ton nom. Pour annuler, vide la case.",
  "<b>There is no “Confirm” button: each quantity is confirmed as soon as you leave its box</b> (Enter, Tab or a click elsewhere). Stock takes the counted figure, the line turns to “count checked” and it is written in the log with your name. To undo, empty the box.",
  "<b>No hay botón «Validar»: cada cantidad se valida en cuanto sales de su casilla</b> (Intro, Tab o clic fuera). El stock toma la cifra contada, la línea pasa a «conteo verificado» y queda anotado en el registro con tu nombre. Para anular, vacía la casilla."); }catch(e){}
function jlog(e){
  try{ const J=lit(KJOU,[]); J.push(Object.assign({t:new Date().toISOString(),u:USR||(typeof NOM_UTIL==='string'&&NOM_UTIL)||'(non renseigné)'},e)); ecrit(KJOU,J); }catch(x){}
}
function confirmeComptage(p,valeur){
  const id=p.cle, m0=MOD[id]||{};
  const avant=(m0.verif)||p.v||'';
  const m=Object.assign({},m0);
  if(m.qteC==null||comptagePerime(p)){       /* premier comptage (ou l'ancien est périmé) : on garde de quoi revenir en arrière */
    if(m0.qte!=null) m.qteAv=m0.qte; else delete m.qteAv;
    m.qteTh0=qteTh(p);
  }
  const th=m.qteTh0!=null?+m.qteTh0:qteTh(p);
  const vend=Math.max(0,valeur-tst(p));
  m.qte=vend; m.qteC=vend;
  m.verif='ok'; m.verifPar=USR||(typeof NOM_UTIL==='string'&&NOM_UTIL)||'(non renseigné)'; m.verifLe=new Date().toISOString();
  MOD[id]=m; ecrit(KMOD,MOD); p.v='ok';
  const ref=(p.marque||'')+' '+(p.nom||'');
  jlog({act:'verif',lib:'comptage physique',bc:p.bc,ref,av:vl(avant)[0],ap:'comptage vérifié'});
  if(vend!==th){ const pa=paEff(p);
    jlog({act:'stock',lib:'quantité corrigée par comptage',bc:p.bc,ref,av:th,ap:vend,n:1,
          impact:pa!=null?Math.round((vend-th)*pa):undefined,det:[{bc:p.bc,ref,av:th,ap:vend}]}); }
}
function annuleComptage(p){
  const id=p.cle, m=MOD[id]; if(!m) return;
  /* annuler un comptage remet la ligne « à recompter » (1er oct. 2026). Avant, l'état était
     effacé : la ligne reprenait celui du fichier de septembre — « vérifiée » pour 632 parfums,
     alors que tout le stock était repassé à compter au démarrage. */
  m.verif='non'; p.v='non'; delete m.verifPar; delete m.verifLe;
  /* on ne retire que la quantité posée par CE comptage : celles qui viennent des ventes,
     des réceptions ou de l'import tableur ne doivent pas disparaître avec lui. */
  if(m.qteC!=null && +m.qte===+m.qteC){
    if(m.qteAv!=null) m.qte=m.qteAv; else delete m.qte;   /* on rend la quantité d'avant le comptage */
  }
  delete m.qteC; delete m.qteAv; delete m.qteTh0;
  ecrit(KMOD,MOD);
  jlog({act:'verif',lib:'comptage annulé',bc:p.bc,ref:(p.marque||'')+' '+(p.nom||''),
        av:'comptage vérifié',ap:'à recompter'});
}

/* ---------------- douchette / scanner ----------------
   Une douchette est un clavier : elle tape les chiffres du code-barres tres vite, puis Entree.
   On reconnait cette rafale (>= 8 caracteres en moins d'une demi-seconde, terminee par Entree),
   ou un code tape dans la recherche suivi d'Entree. Le produit s'ouvre, le curseur va sur la
   quantite ; Entree apres la quantite prepare le scan suivant. */
const SCAN={buf:'',t0:0,el:null,val:''};
function normScan(c){ return String(c||'').replace(/[^0-9]/g,''); }
function trouveBC(code){
  const c=normScan(code); if(c.length<8) return null;
  const cands=[c, c.length===12?'0'+c:null, c.length===13&&c[0]==='0'?c.slice(1):null, c.length===14&&c[0]==='0'?c.slice(1):null].filter(Boolean);
  for(const k of cands){ const p=P.find(x=>x.bc===k); if(p) return p; }
  /* les autres codes-barres déclarés sur la fiche catalogue (même parfum, autre lot ou coffret) */
  const nu=c.replace(/^0+/,'');
  for(const cle in MOD){ const m=MOD[cle]; if(!m||!m.bcs) continue;
    if(String(m.bcs).split(/[^0-9]+/).map(x=>x.replace(/^0+/,'')).includes(nu)){ const p=P.find(x=>x.cle===cle||x.id===cle); if(p) return p; } }
  /* une case collée du fichier (deux codes dans la même cellule) */
  const cx=(typeof cleParBCX==='function')?cleParBCX(nu):null;
  if(cx){ const p=P.find(x=>x.cle===cx||x.id===cx); if(p) return p; }
  return null;
}
function bandeau(cls,html){ const b=$('scan'); b.className='scan '+cls; b.innerHTML=html; b.hidden=false; }
function scanne(code){
  const p=trouveBC(code);
  const T3=(typeof L3==='function')?L3:(f)=>f;
  if(!p){ const k=esc(normScan(code));
    bandeau('ko',T3(`<b>Code ${k} inconnu</b> dans l'inventaire — produit sans code-barres, code faux, ou référence absente du fichier. Cherche-le au nom.`,
      `<b>Code ${k} unknown</b> in the inventory — product without a barcode, wrong code, or reference missing from the file. Search it by name.`,
      `<b>Código ${k} desconocido</b> en el inventario — producto sin código de barras, código erróneo o referencia que no está en el archivo. Búscalo por el nombre.`));
    $('q').value=''; rend(true); $('q').focus(); return; }
  $('q').value=p.bc; rend(true);
  const inp=document.querySelector(kSel(kc(p)));
  const nomP=`<b>${esc(p.marque||'')} ${esc(p.nom||'')}${p.type?' <i class="ty" data-nolang>'+esc(p.type)+'</i>':''}</b>`, dj=inp&&inp.value!==''?esc(inp.value):null;
  bandeau('ok',T3(`${nomP} · ${nf(qteTh(p))} attendus${dj!=null?` · déjà compté : ${dj}`:''} — tape la quantité comptée puis Entrée.`,
    `${nomP} · ${nf(qteTh(p))} expected${dj!=null?` · already counted: ${dj}`:''} — type the counted quantity, then Enter.`,
    `${nomP} · ${nf(qteTh(p))} esperados${dj!=null?` · ya contado: ${dj}`:''} — escribe la cantidad contada y pulsa Intro.`));
  if(inp){ inp.focus(); inp.select(); }
}
document.addEventListener('keydown',e=>{
  const now=Date.now();
  if(e.key==='Enter'){
    const t=e.target;
    /* rafale de douchette, ou code tape dans la recherche */
    const rafale = SCAN.buf.length>=8 && now-SCAN.t0<600;
    const dansQ = t&&t.id==='q' && /^\d{8,14}$/.test(normScan(t.value)) && normScan(t.value).length===t.value.trim().length;
    if(rafale||dansQ){
      e.preventDefault();
      const code = rafale ? SCAN.buf : t.value;
      if(rafale && SCAN.el && SCAN.el===t && (t.classList.contains('cnt')||t.id==='q')) t.value=SCAN.val;   /* on retire ce que la douchette a tape dans le champ */
      SCAN.buf=''; scanne(code); return;
    }
    SCAN.buf='';
    /* Entree apres une quantite : on prepare le scan suivant */
    /* on quitte la case AVANT de redessiner : le comptage est validé (événement change), et la ligne
       redessinée dit tout de suite « Vérifiée ». Avant (19 oct. 2026), la liste se redessinait d'abord :
       le comptage était bien enregistré, mais la ligne restait « Jamais vérifiée » jusqu'au rechargement. */
    if(t&&t.classList.contains('cnt')){ e.preventDefault(); t.blur(); $('q').value=''; rend(true); $('scan').hidden=true; $('q').focus(); }
    return;
  }
  if(e.key.length===1){
    if(!SCAN.buf||now-SCAN.t0>600){ SCAN.buf=''; SCAN.t0=now; SCAN.el=e.target; SCAN.val=e.target&&e.target.value!=null?e.target.value:''; }
    SCAN.buf+=e.key;
  }
},true);

const T_CNT={};
/* la quantité comptée est enregistrée quand on quitte la case (Tab, clic ailleurs, Entrée) */
document.addEventListener('change',e=>{
  if(!e.target.classList||!e.target.classList.contains('cnt')) return;
  const bc=e.target.dataset.bc, v=e.target.value, p0=P.find(x=>kc(x)===bc);
  if(!p0) return;
  if(v!=='' && Number.isInteger(+v) && +v>=0) confirmeComptage(p0,+v);
  else if(v==='') annuleComptage(p0);
  /* la ligne affichait encore l'ancien théorique après une annulation : on la repeint,
     sans toucher au champ qu'on vient de quitter */
  majLigne(p0);
  /* les chiffres du haut et du menu suivent chaque comptage */
  try{ chiffres(); }catch(_){}
},true);
/* réécrit les cellules calculées d'une ligne (théorique, écart, capital) sans recréer le champ */
function majLigne(p){
  const inp=document.querySelector(kSel(kc(p)));
  const tr=inp?inp.closest('tr'):null; if(!tr) return;
  const c=cpt(p), rempli=c!=null&&c!=='';
  const th=qtePhys(p), ec=rempli?(+c)-th:null;
  const val=ec==null||paEff(p)==null?null:ec*paEff(p);
  const gcls=ec==null?'zero':ec>0?'pos':ec<0?'neg':'zero';
  const td=tr.querySelectorAll('td');
  /* colonnes fixes (N°, Produit, Statut, Théorique, Compté, Écart, Valeur, Capital[, PV…]).
     On comptait depuis la fin : quand les colonnes PV existent, le théorique
     s'écrivait dans « Écart » et le capital dans « PV gros ». */
  if(td.length>=8){
    const ta=qteAtt(p), vit=tst(p);
    td[3].innerHTML = (ta===0?'<span style="color:var(--ink-3)">0</span>':nf(ta))
      +(vit?`<span class="vit">+${nf(vit)} tester${vit>1?'s':''}</span>`:'');   /* « tester » et non « vitrine » (Igal, 31 oct. 2026) */
    td[5].innerHTML = `<span class="gap ${gcls}">${ec==null?'—':(ec>0?'+':'')+nf(ec)}</span>`;
    td[6].innerHTML = `<span class="gap ${gcls}">${val==null?'—':(val>0?'+':'')+money(val)}</span>`;
    td[7].innerHTML = money(capEff(p));
    const st=td[2].querySelector('.tag'); const v=(MOD[p.cle]&&MOD[p.cle].verif)||p.v||'';
    if(st){ st.className='tag '+vl(v)[1]; st.textContent=vl(v)[0]; }
  }
  tr.className = !rempli?'':(ec===0?'done':'ecart');
  inp.classList.toggle('filled',rempli);
  bilan(filtre());
}
document.addEventListener('input',e=>{
  if(e.target.classList.contains('cnt')){
    const bc=e.target.dataset.bc, v=e.target.value;
    const p0=P.find(x=>kc(x)===bc);
    const avait=saisie[bc]!=null&&saisie[bc]!=='';
    if(v==='') delete saisie[bc]; else saisie[bc]=v;
    sauve();
    /* on n'écrit ni dans le stock ni dans le journal à chaque touche : une saisie de
       « 120 » écrivait 6 lignes, dont « 782 → 1 » et « 782 → 12 ». On attend la fin. */
    clearTimeout(T_CNT[bc]);
    const p=P.find(x=>kc(x)===bc), tr=e.target.closest('tr');
    const rempli=v!=='', ec=rempli?(+v)-qtePhys(p):null;
    e.target.classList.toggle('filled',rempli);
    tr.className=!rempli?'':(ec===0?'done':'ecart');
    const sp=tr.querySelectorAll('.gap');
    const g=ec==null?'zero':ec>0?'pos':ec<0?'neg':'zero';
    sp[0].className='gap '+g; sp[0].textContent=ec==null?'—':(ec>0?'+':'')+nf(ec);
    const val=rempli&&paEff(p)!=null?ec*paEff(p):null;
    sp[1].className='gap '+g; sp[1].textContent=val==null?'—':(val>0?'+':'')+money(val);
    bilan(filtre());
  }
});
['q','fs','fv','fe'].forEach(i=>$(i).addEventListener('input',()=>rend(true)));
$('pal').addEventListener('click',e=>{
  const b=e.target.closest('.pil'); if(!b) return;
  document.querySelectorAll('.pil').forEach(x=>x.classList.remove('on'));
  b.classList.add('on'); lot=+b.dataset.n; rend(true);
});
/* ---------- repartir pour un nouvel inventaire ---------- */
function cibleInv(){
  const quoi=$('inv-quoi').value;
  const src = quoi==='filtre' ? filtre() : P;
  return src.filter(p=>{
    const m=MOD[p.cle]||{};
    const st=m.verif!==undefined?m.verif:(p.v||'');
    if(st!=='ok') return false;                     /* déjà à recompter */
    if(quoi==='fichier' && m.verifLe) return false; /* comptage réellement fait dans SAM : on le garde */
    return true;
  });
}
function recapInv(){
  const L=cibleInv();
  const cap=L.reduce((a,p)=>a+capEff(p),0);
  const n=$('inv-saisie').checked?Object.keys(saisie).length:0;
  $('inv-recap').innerHTML = L.length
    ? `En cliquant, <b>${nf(L.length)} parfum${L.length>1?'s':''}</b> passe${L.length>1?'nt':''} de
       « compté » à <b>« à compter »</b>. Ça fait <b>${money(cap)}</b> de marchandise que l'équipe devra
       vérifier flacon par flacon.
       ${n?`<br>Les ${nf(n)} chiffre${n>1?'s':''} déjà tapé${n>1?'s':''} dans la colonne « Compté » ${n>1?'seront effacés':'sera effacé'}.`:''}
       <br><span style="color:var(--ink-3)">Le stock, lui, ne change pas d'un flacon.</span>`
    : 'Rien à faire avec ce choix : aucune étiquette à enlever.';
  $('inv-ok').disabled = !L.length && !( $('inv-saisie').checked && Object.keys(saisie).length );
}
$('neuf').addEventListener('click',()=>{
  const faux=P.filter(p=>{ const m=MOD[p.cle]||{};
    const st=m.verif!==undefined?m.verif:(p.v||'');
    return st==='ok' && !m.verifLe; }).length;
  $('inv-faux').textContent = faux>1 ? nf(faux)+' parfums' : faux===1 ? '1 parfum' : 'aucun parfum ne';
  $('inv-quoi').value='fichier';
  recapInv(); $('invov').classList.add('on'); });
$('invx').onclick=$('inv-ann').onclick=()=>$('invov').classList.remove('on');
$('invov').addEventListener('click',e=>{ if(e.target.id==='invov') $('invov').classList.remove('on'); });
['inv-quoi','inv-saisie'].forEach(i=>$(i).addEventListener('change',recapInv));
$('inv-ok').addEventListener('click',()=>{
  const L=cibleInv();
  L.forEach(p=>{
    const m=Object.assign({},MOD[p.cle]||{});
    m.verif='non';
    delete m.verifPar; delete m.verifLe; delete m.qteC; delete m.qteAv; delete m.qteTh0;
    if(!Object.keys(m).length) delete MOD[p.cle]; else MOD[p.cle]=m;
  });
  const nS=$('inv-saisie').checked?Object.keys(saisie).length:0;
  if($('inv-saisie').checked){ saisie={}; sauve(); }
  ecrit(KMOD,MOD);
  jlog({act:'verif',lib:'nouvel inventaire — '+nf(L.length)+' référence'+(L.length>1?'s':'')+' remise'+(L.length>1?'s':'')+' à recompter'
        +(nS?' et '+nf(nS)+' quantité'+(nS>1?'s':'')+' effacée'+(nS>1?'s':''):''),
        av:'comptage vérifié',ap:'à recompter',n:L.length});
  $('invov').classList.remove('on');
  rend(true);
  const b=document.createElement('div'); b.className='info';
  b.innerHTML=`<b>C'est prêt</b> — ${nf(L.length)} parfum${L.length>1?'s':''} ${L.length>1?'sont':'est'} maintenant
    marqué${L.length>1?'s':''} « à compter ». Aucune quantité en stock n'a changé.
    Pour avoir la liste de ce qui reste : filtre <b>Jamais vérifiées</b> juste au-dessus du tableau.`;
  const w=document.querySelector('.wrap')||document.body; w.insertBefore(b,w.firstChild);
  setTimeout(()=>b.remove(),11000);
});

$('raz').addEventListener('click',()=>{
  if(!confirm('Effacer toutes les quantités comptées ? Cette action est définitive.')) return;
  saisie={}; sauve(); rend(true);
  /* Sur un inventaire rempli par un fichier, « effacer » veut souvent dire
     « repartir de zéro » : on le propose, au lieu de laisser croire que rien
     ne s'est passé parce que les lignes importées sont toujours là. */
  let imp=null; try{ imp=localStorage.getItem(K_LOCAL); }catch(e){}
  if(imp){
    let n=0; try{ n=JSON.parse(imp).length; }catch(e){}
    if(confirm('Les quantités sont effacées.\n\nEnlever aussi les '+nf(n)+' lignes venues du fichier importé, '
      +'pour repartir de l\'inventaire d\'origine ? (Tu pourras réimporter un fichier ensuite.)')){
      try{ localStorage.removeItem(K_LOCAL); }catch(e){}
      location.reload();
    }
  }
});
/* Ici « exporter », c'est la feuille de comptage : seulement les références sur
   lesquelles quelqu'un a posé un chiffre. Sortir les 3 830 lignes dont 3 700 vides
   ne servirait à rien et ferait croire que tout a été compté. */
poseSortie('exp', ()=>{
  const l=P.filter(p=>cpt(p)!=null&&cpt(p)!=='');
  return {
    titre:'Comptage d\'inventaire — __CIBLE_LIB__',
    fichier:'comptage',
    filtre:l.length?(nf(l.length)+' référence(s) comptée(s) sur '+nf(P.length)+' affichée(s)')
                   :'aucune quantité saisie',
    colonnes:[{t:'Code-barres'},{t:'Marque'},{t:'Nom'},{t:'Contenance'},{t:'Type'},{t:'Statut'},
      {t:'Théorique',y:'n'},{t:'Compté',y:'n'},{t:'Écart',y:'n'},
      {t:'Prix d\'achat',y:'m'},{t:'Valeur de l\'écart',y:'m'},{t:'PV détail',y:'m'},{t:'PV gros',y:'m'}],
    lignes:l.map(p=>{ const c=+cpt(p), th=qteTh(p), ec=c-th;
      return [p.bc,p.marque,p.nom,p.ml,p.type,vl(p.v)[0],th,c,ec,
        p.pa==null?null:+p.pa, p.pa!=null?ec*p.pa:null, p.pvr==null?null:+p.pvr, p.pvw==null?null:+p.pvw]; })
  };
});
rend(true);

/* ---------------------------------------------------------------
   Ouvert depuis une copie (Téléchargements, Bureau) : les autres
   rubriques ne sont pas à côté du fichier, les liens tombent dans le
   vide. On répare les liens avec le dossier de l'outil mémorisé, et on
   le dit clairement.
   --------------------------------------------------------------- */
(function(){
  if(location.protocol!=='file:') return;
  try{
    var p=decodeURIComponent(location.pathname);
    var i=p.lastIndexOf('/'), fichier=p.slice(i+1);
    var dossier=p.slice(0,i).split('/').filter(Boolean).pop()||'';
    var K='dossier-outil-v1';
    var copie=/_\d+\.html$/i.test(fichier)
      || /^(downloads|t[ée]l[ée]chargements|desktop|bureau|documents)$/i.test(dossier);
    var base=location.href.slice(0,location.href.lastIndexOf('/')+1);
    if(!copie){ try{ localStorage.setItem(K,base); }catch(e){} return; }
    var vrai=''; try{ vrai=localStorage.getItem(K)||''; }catch(e){}
    var n=0;
    if(vrai && vrai!==base){
      document.querySelectorAll('a[href$=".html"]').forEach(function(a){
        var h=a.getAttribute('href');
        if(!h || /^([a-z]+:|\/|#)/i.test(h)) return;
        a.setAttribute('href',vrai+h); n++;
      });
    }
    var d=document.createElement('div');
    d.setAttribute('style','margin:0 0 18px;padding:13px 16px;border-radius:0 8px 8px 0;'
      +'background:var(--warn-soft,#FBF3E2);border-left:3px solid var(--warn,#8A5A00);'
      +'color:var(--ink-2,#4A4A56);font-size:13.5px;line-height:1.6;max-width:88ch');
    d.innerHTML='<b style="color:var(--ink,#17171D)">Tu as ouvert une copie de la page, pas l\'outil.</b> '
      +'Ce fichier est dans « '+dossier+' » : les autres rubriques ne sont pas à côté de lui. '
      +(n? 'J\'ai réparé les '+n+' liens de la barre de gauche pour cette fois. ' : '')
      +'Pour de bon : ouvre le dossier <b>perfumestrade</b> sur ton Bureau et double-clique le fichier qui s\'y trouve '
      +'(pas la copie des Téléchargements). Tes saisies ne sont pas dans le fichier : elles restent dans le navigateur.';
    var cible=document.querySelector('.wrap')||document.body;
    cible.insertBefore(d,cible.firstChild);
  }catch(e){}
})();
</script></body></html>'''


# --------------------------------------------------------------------------
# Deux rubriques, le même tableau.
#   stock.html          : l'entrepôt de Perfumes Trade, avec ses 3 830 lignes
#   inventaire_pc.html  : la boutique Perfume City, vide au départ
# La deuxième se remplit par l'import de fichier — c'est le même écran, les
# mêmes filtres, la même feuille de comptage, mais son propre stock et sa
# propre saisie : les deux ne se mélangent jamais.
# --------------------------------------------------------------------------
_donnees.pose('inventaire_pc', '[]', 'D_INV_PC')

VIDE = {'paliers': {}, 'ok': 0, 'non': 0, 'total': 0, 'enstock': 0,
        'rupture': 0, 'u': 0, 'capnon': 0}

CIBLES = [
    dict(fichier='stock.html', cible='pt', lib='Perfumes Trade',
         actif='stock.html', donnees='inventaire', variable='window.D_INV',
         cle='comptage-parfums-v1', stats=S, remp0='false',
         titre='Inventaire', sous=None),
    dict(fichier='inventaire_pc.html', cible='pc', lib='Perfume City',
         actif='inventaire_pc.html', donnees='inventaire_pc', variable='window.D_INV_PC',
         cle='comptage-pc-v1', stats=VIDE, remp0='true',
         titre='Inventaire Perfume City',
         sous="L'inventaire de la boutique de Perfume City, à part de celui de l'entrepôt. "
              "Il se remplit avec « Mettre à jour depuis un fichier… » : le CSV du Google Sheet, "
              "ou les lignes collées. Même tableau, mêmes filtres, même feuille de comptage — "
              "mais son propre stock, et sa propre saisie."),
]

for C in CIBLES:
    T = C['stats']
    html = (TPL.replace('__FUSION__', FUSION)
               .replace('__COMPTES__', COMPTES).replace('__AIDECSS__', _aide.CSS)
               .replace('__SAUVE__', SAUVE)
               .replace('__MENU__', MENU)
               .replace('__LANGUE__', LANGUE).replace('__VOCAB__', _langue.VOCAB)
               .replace('__XLSX__', _xlsx.XLSX + _lire.bloc()).replace('__ACCEPT_TAB__', _lire.ACCEPT_TAB)
               .replace('__SORTIE__', _sortie.JS)
               .replace('__CSSSORTIE__', _sortie.CSS)
               .replace('__VER__', __import__('datetime').datetime.now().strftime('%Y%m%d%H%M'))
               .replace('__VERSION__', __import__('datetime').datetime.now().strftime('%m/%d/%Y \u00e0 %Hh%M'))
               .replace('__IDENT__', IDENT).replace('__IDENT_TOT__', _identite.TOT).replace('__FILE_AUTO__', _file_auto.FILE_AUTO)
               .replace('__GARDE__', _donnees.garde([C['donnees']]))
               .replace('donnees/inventaire.js', 'donnees/' + C['donnees'] + '.js')
               .replace('__DATA__', C['variable'])
               .replace("const KEY='comptage-parfums-v1';", "const KEY='%s';" % C['cle'])
               .replace('__CIBLE__', C['cible'])
               .replace('__KMOD__', 'fiches-modifiees-pc-v1' if C['cible'] == 'pc' else 'fiches-modifiees-v1')
               .replace('__CIBLE_LIB__', C['lib'])
               .replace('__REMP0__', C['remp0'])
               .replace('__PAL__', json.dumps(T['paliers']))
               .replace('__OK__', n(T['ok']))
               .replace('__NON__', n(T['non']))
               # la barre de gauche montre toujours l'entrepôt, quelle que soit la page
               .replace('__TOTAL__', n(S['total']))
               .replace('__ENSTOCK__', n(S['enstock']))
               .replace('__UNITES__', n(S['u']))
               .replace('__EYEBROW__', C['titre'])
               .replace('__SOUS__', ('<p class="sous">%s</p>' % C['sous']) if C['sous'] else ''))
    # la barre de gauche : la même que partout, avec la bonne rubrique allumée
    html = html.replace('__BARRE__', barre(C['titre']))
    if C['cible'] == 'pc':
        html = html.replace('<title>Inventaire — Perfumes Trade</title>',
                            '<title>Inventaire Perfume City — Perfumes Trade</title>')
        html = html.replace('>Feuille de comptage<', '>Feuille de comptage — Perfume City<')
    open(C['fichier'], 'w').write(enligne(html))
    import os
    print(C['fichier'], round(os.path.getsize(C['fichier']) / 1024), 'Ko')
