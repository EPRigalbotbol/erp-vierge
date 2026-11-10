import json
from build_crm import barre
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
import _lire
import _sortie
data=open('cat.json').read()
import _donnees
_donnees.produits()
S=json.load(open('cat_stats.json'))
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
<script>/* Fiche ouverte dans une fenêtre (mode « cadre ») : on le sait dès l'entête, avant le premier dessin. Sinon on voyait un instant le menu et la liste du Catalogue à côté de la fiche (Igal, 17 oct. 2026 : « c'est pas joli »). Le corps reste caché jusqu'à ce que la fiche soit ouverte (classe « cp »), avec une sécurité de 4 s. */try{if(/[#&]cadre=1/.test(location.hash)&&window.parent!==window){document.documentElement.classList.add('cadre');setTimeout(function(){document.documentElement.classList.add('cp');},4000);}}catch(e){}</script>
<script>/* le contenu de la page reste caché jusqu'à ce que son code l'ait dessiné (voir _serveur.py) */try{document.documentElement.classList.add('pg-attente');setTimeout(function(){document.documentElement.classList.remove('pg-attente');},4000);}catch(e){}</script>
<style>.mn-attente .side nav{visibility:hidden} .pg-attente .main{visibility:hidden}</style>

<title>Catalogue — Perfumes Trade</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap">
<style>
:root{--ground:#F4F4F1;--surface:#FFF;--surface-2:#FAFAF8;--ink:#17171D;--ink-2:#33333D;--ink-3:#5C5C68;
--line:#E0E0DC;--line-2:#EDEDE9;--line-3:#CFCFC8;--iris:#5B4B8A;--iris-soft:#EDE9F6;
--good:#2C6E4E;--good-soft:#E9F3ED;--warn:#8A5A00;--warn-soft:#FBF3E2;--crit:#A4262C;--crit-soft:#FBECEC;}
@media(prefers-color-scheme:dark){:root:not([data-theme="light"]){
--ground:#121217;--surface:#1A1A21;--surface-2:#202028;--ink:#ECECF1;--ink-2:#C9C9D3;--ink-3:#A4A4B2;
--line:#2C2C36;--line-2:#26262F;--line-3:#3D3D4B;--iris:#A99AE0;--iris-soft:#272036;
--good:#77C79C;--good-soft:#152A20;--warn:#D9A94A;--warn-soft:#2E2411;--crit:#E8898D;--crit-soft:#33191B;}}
:root[data-theme="dark"]{--ground:#121217;--surface:#1A1A21;--surface-2:#202028;--ink:#ECECF1;--ink-2:#C9C9D3;
--ink-3:#A4A4B2;--line:#2C2C36;--line-2:#26262F;--line-3:#3D3D4B;--iris:#A99AE0;--iris-soft:#272036;
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
font-family:Inter,-apple-system,BlinkMacSystemFont,sans-serif;font-size:15px;
-webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility}
.mono{font-family:Inter,sans-serif;font-variant-numeric:tabular-nums}
.eyebrow{font-family:Inter,sans-serif;font-size:11px;letter-spacing:.13em;
text-transform:uppercase;color:var(--ink-3);font-weight:500}
/* ---------- COQUILLE CRM ---------- */
.app{display:flex;align-items:flex-start;min-height:100vh}
.side{width:234px;flex:0 0 234px;position:sticky;top:0;height:100vh;overflow-y:auto;
background:var(--surface);border-right:1px solid var(--line);
display:flex;flex-direction:column;padding:14px 0 10px}
.logo{padding:0 18px 12px;border-bottom:1px solid var(--line-2);margin-bottom:8px}
.logo .n{font-size:16px;font-weight:700;letter-spacing:-.02em;line-height:1.2}
.logo .s{font-family:Inter,sans-serif;font-size:9.5px;letter-spacing:.15em;
text-transform:uppercase;color:var(--ink-3);margin-top:3px}
nav{display:flex;flex-direction:column;gap:1px;padding:0 10px}
.navlab{font-family:Inter,sans-serif;font-size:11.5px;letter-spacing:.14em;text-transform:uppercase;
color:var(--iris);font-weight:800;padding:10px 8px 4px}
.nv{display:flex;align-items:center;gap:9px;padding:5px 10px;white-space:nowrap;border-radius:4px;font-size:13.5px;
color:var(--ink);font-weight:600;text-decoration:none;line-height:1.3;border-left:2px solid transparent}
.nv .ic{width:15px;text-align:center;flex:0 0 15px;opacity:.75}
.nv .ct{margin-left:auto;font-family:Inter,sans-serif;font-size:10.5px;font-weight:500;color:var(--ink-3);
font-variant-numeric:tabular-nums}
.nv .ct.pt{background:var(--iris-soft);color:var(--iris);font-weight:700;font-size:10.5px;border-radius:10px;padding:2px 7px;min-width:20px;text-align:center;line-height:1.5}
.nv:hover{background:var(--surface-2);color:var(--ink)}
.nv.on{background:var(--iris-soft);color:var(--iris);font-weight:700;border-left-color:var(--iris)}
.nv.on .ic{opacity:1}
.nv.sub{padding:3px 10px 3px 36px;font-size:12.5px;font-weight:500}
@media(max-height:860px) and (min-width:901px){.nv{padding-top:2px;padding-bottom:2px}.navlab{padding-top:4px;padding-bottom:3px}.side{padding-top:6px;padding-bottom:5px}.logo{padding-bottom:7px;margin-bottom:4px}}  /* portable : voir _base.css (4 nov. 2026 : un cran de plus, Transfert interstore) */
@media(max-width:900px){.nv.sub{padding:5px 10px}}
.nv.soon{color:var(--ink-3);font-weight:500;cursor:default;pointer-events:none}
.nv.soon .ct{font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.8}
.ver{margin-top:9px;font-family:Inter,sans-serif;font-size:10px;color:var(--ink-3);opacity:.75;letter-spacing:.02em}
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
/* une seule largeur de page pour tout l'outil (Igal, 25 sept. 2026 : « certaines pages n'ont pas
   le même encadrement », les Ventes trop étroites avec de la place sur les côtés) */
.wrap{max-width:1600px;margin:0 auto;padding:26px 26px 70px}
@media(max-width:900px){
 .app{flex-direction:column}
 .side{width:100%;flex:none;height:auto;position:static;border-right:0;
  border-bottom:1px solid var(--line);padding:14px 0 10px}
 .logo{padding:0 16px 12px}
 nav{flex-direction:row;overflow-x:auto;gap:4px;padding:0 12px;scrollbar-width:none}
 nav::-webkit-scrollbar{display:none}
 .navlab{display:none}
 .nv{white-space:nowrap;border-left:0;border-bottom:2px solid transparent;border-radius:3px}
 .nv.on{border-left:0;border-bottom-color:var(--iris)}
 .nv .ct,.nv .ic{display:none}
 /* Le pied de barre portait « Se déconnecter » et « Une question ? ». Le masquer
    sous 900 px enlevait la SEULE sortie de session : sur un écran étroit,
    impossible de changer de compte. On garde l'identité et les boutons, on ne
    laisse tomber que les chiffres, qui ne sont qu'un rappel. */
 .sfoot{display:flex;align-items:center;gap:14px;margin-top:0;padding:8px 16px 10px;
  border-top:1px solid var(--line-2)}
 .sfoot #sfoot,.sfoot .ver{display:none}
 .sfoot .sfu{display:flex;align-items:center;gap:8px}
 .sfoot .sfu b,.sfoot .sfu span{display:inline!important}
 .wrap{padding:20px 16px 60px}
}
header{border-bottom:2px solid var(--ink);padding-bottom:18px;margin-bottom:18px;display:flex;
flex-wrap:wrap;gap:16px;align-items:flex-end;justify-content:space-between}
h1{margin:0;font-size:clamp(25px,4vw,34px);font-weight:700;letter-spacing:-.028em;line-height:1.05}
.src{text-align:right;font-family:Inter,sans-serif;font-size:11.5px;color:var(--ink-2);line-height:1.7}
/* ================= BARRE DE FILTRES ================= */
.bar{position:sticky;top:0;z-index:9;background:var(--ground);padding:12px 0 0;margin-bottom:18px}
.bar::after{content:'';display:block;height:1px;background:var(--line);margin-top:12px}
.brow{display:flex;flex-wrap:wrap;gap:8px;align-items:center}
.srch{position:relative;flex:1 1 210px;min-width:170px;display:flex;align-items:center}
.srch svg{position:absolute;left:11px;width:15px;height:15px;color:var(--ink-3);pointer-events:none}
.srch input{width:100%;font-family:inherit;font-size:13.5px;color:var(--ink);background:var(--surface);
border:1px solid var(--line);border-radius:6px;padding:9px 30px 9px 33px;transition:border-color .12s}
.srch input::-webkit-search-cancel-button{display:none}
.srch input:hover{border-color:var(--ink-3)}
.srch input:focus{outline:0;border-color:var(--iris);box-shadow:0 0 0 3px var(--iris-soft)}
.srch .clr{position:absolute;right:7px;background:none;border:0;color:var(--ink-3);font-size:17px;
line-height:1;cursor:pointer;padding:2px 5px;border-radius:4px;display:none}
.srch .clr:hover{color:var(--ink);background:var(--line-2)}
.srch.has .clr{display:block}
.seg{display:inline-flex;background:var(--line-2);border-radius:6px;padding:2px;gap:2px}
.seg button{font-family:inherit;font-size:12.5px;font-weight:500;color:var(--ink-3);background:none;
border:0;border-radius:4px;padding:6px 12px;cursor:pointer;white-space:nowrap;transition:all .12s}
.seg button:hover{color:var(--ink)}
.seg button.on{background:var(--surface);color:var(--ink);font-weight:600;box-shadow:0 1px 2px rgba(23,23,29,.09)}
.selw{position:relative;display:inline-flex;flex:0 1 auto;min-width:0}
.selw::after{content:'';position:absolute;right:12px;top:50%;width:6px;height:6px;
border-right:1.5px solid var(--ink-3);border-bottom:1.5px solid var(--ink-3);
transform:translateY(-70%) rotate(45deg);pointer-events:none}
.selw select{appearance:none;-webkit-appearance:none;font-family:inherit;font-size:13.5px;color:var(--ink);
background:var(--surface);border:1px solid var(--line);border-radius:6px;padding:9px 30px 9px 12px;
cursor:pointer;max-width:178px;text-overflow:ellipsis;transition:border-color .12s}
.selw select:hover{border-color:var(--ink-3)}
.selw select:focus{outline:0;border-color:var(--iris);box-shadow:0 0 0 3px var(--iris-soft)}
.selw.act select{border-color:var(--iris);color:var(--iris);font-weight:500;background:var(--iris-soft)}
.selw.act::after{border-color:var(--iris)}
.more{display:inline-flex;align-items:center;gap:7px;font-family:inherit;font-size:13.5px;font-weight:500;
color:var(--ink-2);background:var(--surface);border:1px solid var(--line);border-radius:6px;
padding:9px 13px;cursor:pointer;white-space:nowrap;transition:all .12s}
.more:hover{border-color:var(--ink-3);color:var(--ink)}
.more.on{border-color:var(--iris);color:var(--iris);background:var(--iris-soft)}
.more .bdg{font-family:Inter,sans-serif;font-size:10px;font-weight:600;background:var(--iris);
color:#fff;border-radius:99px;min-width:17px;height:17px;display:none;align-items:center;
justify-content:center;padding:0 5px}
.more .bdg.vis{display:inline-flex}
.more .cv{width:7px;height:7px;border-right:1.5px solid currentColor;border-bottom:1.5px solid currentColor;
transform:translateY(-2px) rotate(45deg);transition:transform .16s}
.more.on .cv{transform:translateY(1px) rotate(-135deg)}
.acts{margin-left:auto;display:flex;align-items:center;gap:8px}
.count{font-family:Inter,sans-serif;font-size:12.5px;color:var(--ink-3);white-space:nowrap;
font-variant-numeric:tabular-nums}
.adv{display:none;flex-wrap:wrap;gap:9px;align-items:center;margin-top:9px;padding:12px 14px;
background:var(--surface);border:1px solid var(--line);border-radius:8px}
.adv.on{display:flex}
.adv .lab{font-family:Inter,sans-serif;font-size:9.5px;letter-spacing:.13em;
text-transform:uppercase;color:var(--ink-3);font-weight:500}
.adv .sep{width:1px;height:24px;background:var(--line);margin:0 3px}
.sw{display:inline-flex;align-items:center;gap:8px;font-size:13px;color:var(--ink-2);
cursor:pointer;white-space:nowrap;user-select:none}
.sw input{position:absolute;opacity:0;width:0;height:0}
.sw .tr{width:32px;height:18px;border-radius:99px;background:var(--line);position:relative;
transition:background .16s;flex:0 0 32px}
.sw .tr::after{content:'';position:absolute;top:2px;left:2px;width:14px;height:14px;border-radius:50%;
background:var(--surface);box-shadow:0 1px 2px rgba(0,0,0,.2);transition:transform .16s}
.sw input:checked + .tr{background:var(--iris)}
.sw input:checked + .tr::after{transform:translateX(14px)}
.sw input:focus-visible + .tr{box-shadow:0 0 0 3px var(--iris-soft)}
.sw input:checked ~ .tx{color:var(--iris);font-weight:500}
.status{display:flex;flex-wrap:wrap;gap:8px 12px;align-items:center;margin-top:11px}
.chips{display:none;flex-wrap:wrap;gap:6px;align-items:center}
.chips.on{display:flex}
.chip{display:inline-flex;align-items:center;gap:7px;font-size:12px;background:var(--iris-soft);
color:var(--iris);border-radius:99px;padding:4px 5px 4px 11px;font-weight:500}
.chip .k{font-family:Inter,sans-serif;font-size:9px;letter-spacing:.1em;text-transform:uppercase;opacity:.7}
.chip button{background:none;border:0;color:inherit;cursor:pointer;font-size:14px;line-height:1;
padding:1px 4px;border-radius:99px;opacity:.6}
.chip button:hover{opacity:1;background:rgba(127,110,180,.22)}
.chips .raz{font-size:12px;color:var(--ink-3);background:none;border:0;cursor:pointer;
text-decoration:underline;text-underline-offset:2px;padding:4px 6px}
.chips .raz:hover{color:var(--crit)}
body.client .ph .qty{display:none}
@media(max-width:700px){.acts{margin-left:0;width:100%;justify-content:space-between}
 .selw select{max-width:148px}}

/* ---------- VIGNETTE ---------- */
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(206px,1fr));gap:16px;align-items:stretch}
.card{background:var(--surface);border:1px solid var(--line);border-radius:5px;overflow:hidden;
display:flex;flex-direction:column;
transition:border-color .13s ease}
.card:hover{border-color:var(--ink-3)}
.card.alert{border-color:var(--crit)}
.card.warn{border-color:var(--warn)}

.ph{aspect-ratio:1/1;flex:0 0 auto;overflow:hidden;background:var(--surface-2);display:flex;align-items:center;justify-content:center;
border-bottom:1px solid var(--line-2);position:relative;padding:14px}
.ph img{width:100%;height:100%;max-width:100%;max-height:100%;min-width:0;min-height:0;
object-fit:contain;object-position:center;display:block;mix-blend-mode:multiply}
@media(prefers-color-scheme:dark){:root:not([data-theme="light"]) .ph img{mix-blend-mode:normal}}
:root[data-theme="dark"] .ph img{mix-blend-mode:normal}
.miss{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:9px;
width:100%;height:100%;color:var(--line);opacity:.9}
.miss svg{width:38%;height:auto;display:block}
.miss span{font-family:Inter,sans-serif;font-size:8.5px;letter-spacing:.14em;
text-transform:uppercase;color:var(--ink-3);opacity:.7}
.qty{position:absolute;top:9px;right:9px;font-family:Inter,sans-serif;font-size:10.5px;
font-weight:500;padding:3px 8px;border-radius:99px;background:var(--good-soft);color:var(--good);
font-variant-numeric:tabular-nums;letter-spacing:.02em}
.qty.low{background:var(--warn-soft);color:var(--warn)}
.qty.out{background:var(--line-2);color:var(--ink-3);letter-spacing:.06em}

.body{padding:13px 14px 14px;display:flex;flex-direction:column;gap:0;flex:1}
.brand{font-family:Inter,sans-serif;font-size:12px;font-weight:700;letter-spacing:.08em;
text-transform:uppercase;color:var(--iris);line-height:1.35;margin-bottom:4px;overflow-wrap:anywhere}
.nm{font-size:17px;font-weight:700;line-height:1.24;letter-spacing:-.02em;color:var(--ink);
overflow-wrap:anywhere;min-height:2.48em;margin-bottom:6px;text-wrap:balance}
.meta{font-size:13px;color:var(--ink-2);line-height:1.4;letter-spacing:.005em;
white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.meta b{font-weight:600;color:var(--ink-2);font-variant-numeric:tabular-nums}
.flags{display:flex;flex-wrap:wrap;gap:5px;margin-top:9px}
.fl{display:inline-flex;align-items:center;gap:6px;font-family:Inter,sans-serif;font-size:11.5px;
padding:4px 10px 4px 8px;border-radius:20px;font-weight:600;line-height:1.4;letter-spacing:.005em;
white-space:nowrap;max-width:100%;overflow:hidden;text-overflow:ellipsis}
.fl::before{content:"";width:6px;height:6px;border-radius:50%;background:currentColor;flex:0 0 auto}
.fl.c{background:var(--crit-soft);color:var(--crit)}
.fl.w{background:var(--warn-soft);color:var(--warn)}

.led{margin-top:auto;padding-top:11px;border-top:1px solid var(--line-2);
display:grid;grid-template-columns:auto 1fr;gap:3px 10px;align-items:baseline}
.led dt{font-family:Inter,sans-serif;font-size:10px;letter-spacing:.11em;
text-transform:uppercase;color:var(--ink-2);font-weight:600}
.led dd{margin:0;font-family:Inter,sans-serif;text-align:right;
font-variant-numeric:tabular-nums;white-space:nowrap}
.led .vp{font-size:15px;font-weight:600;color:var(--ink-2);letter-spacing:-.015em}
.led .vr{font-size:19px;font-weight:700;color:var(--ink);letter-spacing:-.025em;line-height:1.12}
.led .vw{font-size:17px;font-weight:700;color:var(--iris);letter-spacing:-.02em}
.led .na{color:var(--ink-3);font-size:11px;font-style:italic;letter-spacing:0;font-weight:400}
.led .bad{color:var(--crit)}
.ast{color:var(--iris);font-weight:500;font-size:10px;vertical-align:super;margin-left:1px}
.ast.bad{color:var(--crit)}
.bcline{margin-top:9px;padding-top:8px;border-top:1px solid var(--line-2);
font-family:Inter,sans-serif;font-size:9.5px;letter-spacing:.06em;color:var(--ink-3);
white-space:nowrap;overflow:hidden;text-overflow:ellipsis}


/* DIFFUSION : trois pastilles par parfum */
.dif{display:inline-flex;flex-direction:column;align-items:flex-start;gap:3px;vertical-align:middle}
.dfrow .dif{display:flex}
.card .dfrow .dif{flex-direction:row;flex-wrap:wrap;gap:4px 6px}
.dfi{position:relative;display:inline-block;padding:1px 8px;border-radius:9px;font-family:Inter,sans-serif;font-size:10.5px;font-weight:600;letter-spacing:.01em;line-height:1.35;text-align:left;color:#fff;text-transform:none;white-space:nowrap}
.dfi.d-site{background:#d6155f}.dfi.d-sitegros{background:#4b3a86}.dfi.d-perfumecity{background:#4f8a2b}
.dfi.non{background:var(--surface-2,#eee);color:var(--ink-3,#999);box-shadow:inset 0 0 0 1px var(--line,#ddd)}
.dfi.non{text-decoration:line-through;text-decoration-color:var(--crit,#c0392b);text-decoration-thickness:1.5px}
.fl.dfx{white-space:normal;overflow:visible;text-overflow:clip;max-width:100%}
.dfi.na{opacity:.25}
.dfrow{margin:4px 0 1px}
#fd{min-width:220px}
/* METTRE EN LIGNE : la barre sous le compteur et sa fenêtre (Igal, 17 oct. 2026 : « fais tout ») */
.mel{display:flex;flex-wrap:wrap;align-items:center;gap:8px 14px;margin:8px 0 2px;padding:9px 14px;border-radius:10px;background:var(--iris-soft,#efeaf9);color:var(--ink-2,#444);font-size:13.5px;line-height:1.45}
.mel b{font-weight:700;color:var(--ink,#111)}
.mel[hidden],body.client .mel{display:none}
.mel .btn{margin-left:auto}
.mvoile{position:fixed;inset:0;z-index:2000;background:rgba(20,16,30,.45);display:flex;align-items:center;justify-content:center;padding:16px}
.mfen{background:var(--surface,#fff);color:var(--ink,#111);border-radius:14px;max-width:560px;width:100%;max-height:90vh;overflow:auto;padding:22px 24px;box-shadow:0 20px 60px rgba(0,0,0,.3);font-size:14px;line-height:1.5}
.mfen h3{margin:0 0 4px;font-size:18px}
.mfen .ml{display:flex;align-items:flex-start;gap:9px;margin:10px 0;padding:10px 12px;border-radius:9px;background:var(--surface-2,#f4f2f8)}
.mfen .ml small{display:block;color:var(--ink-3,#777)}
.mfen .mrep{margin-top:12px;padding:10px 12px;border-radius:9px;background:var(--surface-2,#f4f2f8);font-size:13px}
.mfen .mrep.bad{background:var(--crit-soft,#fdecea)}
.mfen .mbtn{display:flex;gap:10px;justify-content:flex-end;margin-top:16px}
.mfen select{padding:5px 8px;border-radius:7px}
/* ================= FICHE PRODUIT ================= */
html.cadre .side,html.cadre .legend,html.cadre #more{display:none!important}
html.cadre:not(.cp) body{visibility:hidden}   /* rien ne se montre avant que la fiche soit ouverte */
html.cadre .main{visibility:hidden}
html.cadre .dr,html.cadre .dov{visibility:visible}
/* 31 oct. 2026 (Igal : « Remettre en vente, ça bug, il ne se passe rien ») : les fenêtres de la fiche (confirmer les prix, identité…)
   vivent dans .main, cachée en mode cadre — elles s'ouvraient INVISIBLES dans la fiche ouverte depuis le tableau de bord */
html.cadre .ov{visibility:visible}
html.cadre,html.cadre body{background:transparent}
html.cadre .dov{background:transparent;backdrop-filter:none}
html.cadre .dr{width:100%;box-shadow:none}
html.cadre .dnav #dprev,html.cadre .dnav #dnext{display:none}
.dov{position:fixed;inset:0;background:rgba(23,23,29,.42);backdrop-filter:blur(2px);z-index:40;
opacity:0;pointer-events:none;transition:opacity .18s}
.dov.on{opacity:1;pointer-events:auto}
.dr{position:fixed;top:0;right:0;bottom:0;width:min(940px,100%);background:var(--surface);
border-left:1px solid var(--line);z-index:41;display:flex;flex-direction:column;
transform:translateX(100%);transition:transform .22s cubic-bezier(.32,.72,0,1);
box-shadow:-8px 0 32px rgba(0,0,0,.13)}
.dr.on{transform:none}
.dh{padding:16px 20px;border-bottom:1px solid var(--line);display:flex;align-items:flex-start;gap:12px;flex:0 0 auto}
.dh .id{flex:1;min-width:0}
.dh .b{font-family:Inter,sans-serif;font-size:12.5px;letter-spacing:.08em;
text-transform:uppercase;color:var(--iris);font-weight:700}
.dh h2{margin:3px 0 0;font-size:23px;font-weight:700;letter-spacing:-.026em;line-height:1.2}
.dnav{display:flex;gap:2px;flex:0 0 auto}
.dnav button,.dx{background:var(--surface-2);border:1px solid var(--line);border-radius:5px;
width:30px;height:30px;cursor:pointer;color:var(--ink-2);font-size:15px;line-height:1;
display:flex;align-items:center;justify-content:center;padding:0}
.dnav button:hover,.dx:hover{border-color:var(--iris);color:var(--iris)}
.dnav button:disabled{opacity:.35;cursor:default}
.dnav button:disabled:hover{border-color:var(--line);color:var(--ink-2)}
.db{flex:1;overflow-y:auto;padding:20px 22px 26px;display:flex;flex-direction:column;gap:22px}

/* --- bandeau haut : photo + stock --- */
.dhero{display:grid;grid-template-columns:152px 1fr;gap:18px;align-items:start}
.dph{aspect-ratio:1/1;background:var(--surface-2);border:1px solid var(--line-2);border-radius:8px;
display:flex;align-items:center;justify-content:center;overflow:hidden;padding:6px;position:relative}
.dcan .cvoir{display:inline-block;margin-top:6px;font-size:11.5px;color:var(--iris);text-decoration:none;border-bottom:1px solid transparent}
.dcan .cvoir:hover{border-bottom-color:var(--iris)}
.dphw{display:flex;flex-direction:column;gap:8px;min-width:0}
.dphb{display:flex;flex-direction:column;gap:6px;align-items:stretch}
.dphb .dphc{font-size:12px;padding:7px 6px;justify-content:center;text-align:center;line-height:1.2}
.dphb .dphr{font-size:11.5px;text-align:center;background:none;border:0;color:var(--ink-3);cursor:pointer;text-decoration:underline;padding:0}
.dstk{display:flex;flex-direction:column;gap:11px;min-width:0}
.dstk .big{display:flex;align-items:baseline;gap:9px;flex-wrap:wrap}
.dstk .big b{font-family:Inter,sans-serif;font-size:36px;font-weight:600;line-height:.92;
letter-spacing:-.03em;font-variant-numeric:tabular-nums}
.dstk .big em{font-style:normal;font-size:13px;color:var(--ink-3)}
.dqte{display:flex;flex-direction:column;gap:7px;align-self:flex-start;padding:10px 14px 12px;
border:2px solid var(--iris);border-radius:10px;background:var(--iris-soft)}
.dqte label{font-family:Inter,sans-serif;font-size:12px;font-weight:700;letter-spacing:.06em;
text-transform:uppercase;color:var(--iris)}
.dqte-l{display:flex;align-items:baseline;gap:10px}
.dqte input{font-family:Inter,sans-serif;font-size:34px;font-weight:600;line-height:1.1;width:150px;
padding:4px 10px;color:var(--ink);background:var(--surface);border:1px solid var(--line);border-radius:7px;
font-variant-numeric:tabular-nums}
.dqte input:hover{border-color:var(--iris)}
.dqte input:focus{outline:0;border-color:var(--iris);box-shadow:0 0 0 3px var(--iris-soft)}
.dqte em{font-style:normal;font-size:15px;font-weight:600;color:var(--ink-2)}
.dqte.ch{border-color:var(--warn);background:var(--warn-soft)}
.dcanw.flash{box-shadow:0 0 0 3px var(--iris);border-radius:10px;transition:box-shadow .3s}
.dqte.dqpc.ro{border-color:#d4789a;background:#fbeef3}.dqte.dqpc.ro label{color:#b04a72}.dqte.dqpc.ro b{font-family:Inter,sans-serif;font-size:34px;font-weight:600;line-height:1.1;color:var(--ink)}
.dqte.dqpc.ro small{font-size:11.5px;color:var(--ink-3)}
.dqte.ch label{color:var(--warn)}
.dstk .cap{font-family:Inter,sans-serif;font-size:17px;font-weight:600;color:var(--iris);
font-variant-numeric:tabular-nums;line-height:1}
.dstk .rk{font-size:12px;color:var(--ink-3);line-height:1.55}
.dstk .rk b{color:var(--ink-2);font-weight:600}
.dvf{display:inline-flex;align-items:center;gap:7px;font-size:11.5px;font-weight:600;
padding:6px 11px;border-radius:20px;align-self:flex-start;line-height:1}
.dvf::before{content:"";width:6px;height:6px;border-radius:50%;background:currentColor;flex:0 0 auto}
.dvf.vok{background:var(--good-soft);color:var(--good)}
.dvf.vnon{background:var(--warn-soft);color:var(--warn)}
.dvf.vav{background:var(--crit-soft);color:var(--crit)}
.dvf.vvide{background:var(--surface-2);color:var(--ink-3)}
.dvf.vrupt{background:var(--surface-2);color:var(--ink-3)}
.dvz{display:flex;flex-wrap:wrap;align-items:center;gap:8px}
.dvq{font-size:11.5px;color:var(--ink-3);line-height:1.45}
.dvq b{color:var(--ink-2);font-weight:600}
.btn.ptt{font-size:12px;padding:5px 11px}
.dsst{font-size:13px;color:var(--ink-2);background:var(--surface-2);border-radius:6px;padding:9px 11px;display:flex;flex-direction:column;gap:6px}
.dsst b{font-family:Inter,sans-serif;font-weight:700;color:var(--ink)}.dsst b.ecart{color:var(--crit)}
.dsst.faux{border-left:3px solid var(--crit)}.dsst2{font-size:12px;color:var(--ink-3)}
.dsst3{font-size:12px;color:var(--ink-2);font-weight:600}
.dcompt{font-size:12px;color:var(--ink-3);background:var(--surface-2);border-radius:6px;
padding:8px 11px;line-height:1.5;border-left:2px solid var(--line)}
.dcompt.ec{border-left-color:var(--crit)}
.dcompt b{color:var(--ink-2)}

/* --- rail de prix --- */
.dtop{display:flex;flex-wrap:wrap;align-items:stretch;gap:10px}
.dqte.ro{border-color:var(--line);background:var(--surface-2)}
.dqte.ro label{color:var(--ink-3)}
.dqte.ro b{font-family:Inter,sans-serif;font-size:26px;font-weight:700;line-height:1.1;font-variant-numeric:tabular-nums;letter-spacing:-.02em}
.dqte.ro small{font-size:11px;color:var(--ink-3)}
.dqte{padding:7px 12px 8px;gap:3px}
.dqte label{font-size:10.5px}
.dqte input{font-size:26px;width:104px;padding:2px 8px}
.dqte em{font-size:13px}
.dtop .cap{display:flex;flex-direction:column;justify-content:center;gap:2px;padding:7px 14px;border:1px solid var(--line);border-radius:10px;background:var(--surface-2);font-size:20px;line-height:1.1}
.dtop .cap small{font-size:10.5px;font-weight:600;color:var(--ink-3);letter-spacing:.06em;text-transform:uppercase}
.damz{display:flex;flex-direction:column;justify-content:center;gap:3px;padding:7px 14px;border:1px solid var(--line);border-radius:10px;background:var(--surface-2);text-decoration:none;color:var(--ink)}
.damz span{font-family:Inter,sans-serif;font-size:12.5px;font-weight:700;color:var(--iris)}
.damz small{font-family:Inter,sans-serif;font-size:10.5px;color:var(--ink-3);letter-spacing:.04em}
.damz .lg img{height:16px}
.damz:hover{border-color:var(--iris)}
.drail.mini{gap:8px}
.drail.mini .st{padding:7px 6px;gap:3px}
.drail.mini .st span{font-size:10.5px;letter-spacing:.08em}
.drail.mini .st input{font-size:22px}
.drail.mini .st .in em{font-size:13px}
.drail.mini .st .lsl{display:block;margin-top:3px;font-size:11px;color:var(--mut,#6b6b6b);line-height:1.25;text-align:center}
.drail.mini .mg{font-size:12px;padding:2px 8px}
.dhero{grid-template-columns:120px 1fr;gap:14px}
.drail{display:grid;grid-template-columns:1fr 1fr 1fr;align-items:stretch;gap:10px}
.drail .st{display:flex;flex-direction:column;align-items:center;gap:5px;min-width:0;
background:var(--surface-2);border:1px solid var(--line);border-radius:9px;padding:11px 8px}
.drail .st span{font-family:Inter,sans-serif;font-size:12.5px;letter-spacing:.1em;
text-transform:uppercase;color:var(--ink);font-weight:800}
.drail .st .in{display:flex;align-items:baseline;justify-content:center;gap:3px;width:100%;
/* une cale de la largeur du « $ » à gauche : le montant tombe au milieu de la case */
border:1px solid transparent;border-radius:5px;padding:2px 5px;
transition:background .12s,border-color .12s}
.drail .st .in:hover{background:var(--surface);border-color:var(--line)}
.drail .st .in:focus-within{background:var(--surface);border-color:var(--iris);
box-shadow:0 0 0 3px var(--iris-soft)}
.drail .st .in::before{content:"";flex:0 0 13px}
.drail .st .in em{font-style:normal;font-family:Inter,sans-serif;font-size:17px;
font-weight:700;color:var(--ink);flex:0 0 13px;text-align:left}
.drail .st input{font-family:Inter,sans-serif;font-size:32px;font-weight:800;color:var(--ink);
font-variant-numeric:tabular-nums;letter-spacing:-.035em;text-align:center;line-height:1.08;
flex:1 1 auto;min-width:0;width:100%;
background:transparent;border:0;border-radius:0;padding:1px 0;-moz-appearance:textfield}
.drail .st input::-webkit-outer-spin-button,.drail .st input::-webkit-inner-spin-button{
-webkit-appearance:none;margin:0}
.drail .st input:focus{outline:0}
.drail .st .in:has(input.vide){border-color:var(--warn);border-style:dashed}
.drail .st.ch .in{border-color:var(--iris);background:var(--iris-soft)}
.drail .mg{font-style:normal;font-family:Inter,sans-serif;font-size:14.5px;font-weight:800;
white-space:nowrap;padding:4px 10px;border-radius:20px;letter-spacing:-.01em;line-height:1;margin-top:2px}
.drail .mg.g{background:var(--good-soft);color:var(--good)}
.drail .mg.w{background:var(--warn-soft);color:var(--warn)}
.drail .mg.c{background:var(--crit-soft);color:var(--crit)}
.drail .mg.na{background:var(--surface);color:var(--ink-3);border:1px dashed var(--line)}
.drail.amz{grid-template-columns:repeat(auto-fit,minmax(250px,1fr));max-width:900px}
.drail .st.lien{align-items:stretch;text-align:center;gap:7px}
.drail .st.lien .rang{font-family:Inter,sans-serif;font-size:26px;font-weight:800;letter-spacing:-.03em;
line-height:1.05;color:var(--ink)}
.drail .st.lien .rang small{display:block;font-size:12px;font-weight:600;color:var(--ink-2);
letter-spacing:0;text-transform:none;margin-top:3px}
.drail .st.lien .rien{font-family:Inter,sans-serif;font-size:14px;font-weight:600;color:var(--ink-3);padding:6px 0}
.drail .st.lien a.go{display:inline-flex;align-items:center;justify-content:center;gap:6px;
font-family:Inter,sans-serif;font-size:13.5px;font-weight:700;color:#fff;background:var(--iris);
border-radius:7px;padding:9px 12px;text-decoration:none;letter-spacing:0;text-transform:none}
.drail .st.lien a.go:hover{filter:brightness(1.08)}
.drail .st.lien .dt{font-family:Inter,sans-serif;font-size:12px;color:var(--ink-2);letter-spacing:0;
text-transform:none;font-weight:500;line-height:1.45}
.drail .st.lien button.maj{font-family:inherit;font-size:12.5px;font-weight:600;color:var(--ink-2);
background:var(--surface);border:1px solid var(--line);border-radius:7px;padding:7px 11px;cursor:pointer;
letter-spacing:0;text-transform:none}
.drail .st.lien button.maj:hover{border-color:var(--iris);color:var(--iris)}
.drail .st.ref{background:var(--surface);border-style:dashed}
.drail .st .in.ro{cursor:default}
.drail .st .in.ro b{font-family:Inter,sans-serif;font-size:32px;font-weight:800;color:var(--ink);letter-spacing:-.035em;line-height:1.08;flex:0 0 auto}
.drail .st .in.ro::before{display:none}
.drail .st .in.ro em{flex:0 0 auto}
.drail .st.man .in{border-color:var(--iris);background:var(--iris-soft)}
.drail .st .rl{font-family:Inter,sans-serif;font-size:13px;color:var(--ink-2);white-space:normal;text-align:center;letter-spacing:0;text-transform:none;font-weight:600}
.drail .st .rl a{color:var(--iris)}
.drail .st .expl{font-family:Inter,sans-serif;font-size:13px;color:var(--ink);letter-spacing:0;text-transform:none;font-weight:500;
text-align:center;line-height:1.45;font-variant-numeric:tabular-nums}
.drail .st .expl b{font-weight:700}.drail .st .expl b.g{color:var(--good)}.drail .st .expl b.w{color:var(--warn)}.drail .st .expl b.c{color:var(--crit)}.drail .st .expl b.na{color:var(--ink-3)}
.drail .st .rl button{background:none;border:0;padding:0;font:inherit;color:var(--iris);text-decoration:underline;cursor:pointer}
/* bulle d'explication : un petit i, le texte au survol ou au clavier */
@supports (field-sizing: content){
  .drail .st .in input,.cn .in input{field-sizing:content;flex:0 1 auto;width:auto;min-width:2ch;max-width:100%}
  .drail .st .in::before,.cn .in::before{display:none}
  .drail .st .in em,.cn .in em{flex:0 0 auto}
}
.bul{display:inline-flex;align-items:center;justify-content:center;width:18px;height:18px;border-radius:50%;
border:1.5px solid var(--ink);color:var(--ink);font-family:Georgia,serif;font-style:italic;font-size:12px;font-weight:700;
letter-spacing:0;text-transform:none;cursor:help;position:relative;vertical-align:middle;margin-left:3px}
.bul::after{content:attr(data-bul);position:absolute;left:50%;bottom:calc(100% + 8px);transform:translateX(-50%);
width:300px;background:var(--ink);color:var(--surface);font-family:Inter,sans-serif;font-style:normal;font-weight:500;
font-size:13.5px;line-height:1.45;letter-spacing:0;text-transform:none;padding:9px 11px;border-radius:7px;
box-shadow:0 6px 20px rgba(0,0,0,.18);opacity:0;pointer-events:none;transition:opacity .12s;z-index:5;white-space:normal;text-align:left}
.bul:hover::after,.bul:focus::after{opacity:1}
.lg{display:inline-flex;align-items:center;justify-content:center;max-width:100%;vertical-align:middle;letter-spacing:inherit;text-transform:inherit}
.lg img{height:18px;max-width:110px;object-fit:contain;display:block}
.lg-site img{height:40px;max-width:200px}
.drail .st span .lg img{height:20px}
.dsec > h3 .lg img{height:20px}
/* relevé Amazon : on colle le bloc de la page produit, l'outil en tire les chiffres */
.mzone{width:100%;min-height:150px;font-family:inherit;font-size:13px;line-height:1.55;color:var(--ink);
background:var(--surface-2);border:1px solid var(--line);border-radius:8px;padding:11px 13px;resize:vertical}
.mzone:focus{outline:0;border-color:var(--iris);background:var(--surface);box-shadow:0 0 0 3px var(--iris-soft)}
.mlu{background:var(--good-soft);border-left:3px solid var(--good);border-radius:0 8px 8px 0;padding:10px 13px;
font-size:12.5px;color:var(--good);line-height:1.6;margin-top:10px}
.mlu.rien{background:var(--warn-soft);border-left-color:var(--warn);color:var(--warn)}
.mlu b{color:inherit}
.mnote{display:flex;align-items:baseline;gap:6px}
.mnote .et{color:var(--warn);font-size:14px;letter-spacing:1px}
.dbtns{display:flex;gap:9px;flex-wrap:wrap;align-self:flex-start}
.ajl{display:flex;flex-direction:column;gap:6px}
/* --- fenêtre « ajuster le stock » --- */
.ajgrp{margin:0 0 4px}
.ajgt{display:flex;align-items:center;gap:8px;margin:0 0 8px}
.ajgt b{font-family:Inter,sans-serif;font-size:10px;letter-spacing:.12em;text-transform:uppercase;
color:var(--ink-3);font-weight:700}
.ajgt i{flex:1;height:1px;background:var(--line-2)}
.ajgt .sg{display:inline-flex;align-items:center;justify-content:center;width:17px;height:17px;
border-radius:5px;font-family:Inter,sans-serif;font-size:12px;font-weight:800;line-height:1}
.ajgt .sg.m{background:var(--crit-soft);color:var(--crit)}
.ajgt .sg.p{background:var(--good-soft);color:var(--good)}
.ajgt .sg.e{background:var(--iris-soft);color:var(--iris);font-size:11px}
.ajmot{display:grid;grid-template-columns:repeat(auto-fit,minmax(168px,1fr));gap:7px;margin:0 0 15px}
.ajmot label{display:flex;flex-direction:column;gap:2px;font-size:13.5px;color:var(--ink);
background:var(--surface);border:1px solid var(--line);border-radius:9px;padding:10px 12px;
cursor:pointer;transition:border-color .12s,background .12s;position:relative}
.ajmot label:hover{border-color:var(--ink-3);background:var(--surface-2)}
.ajmot label input{position:absolute;opacity:0;pointer-events:none}
.ajmot label .t{font-weight:600;line-height:1.25}
.ajmot label .a{font-size:11.5px;color:var(--ink-3);line-height:1.35}
.ajmot label.on{border-color:var(--iris);background:var(--iris-soft);box-shadow:inset 0 0 0 1px var(--iris)}
.ajmot label.on .t{color:var(--iris)}
.ajmot label.on .a{color:var(--ink-2)}
/* Le bloc « chez Perfume City » : ce qui arrive vraiment dans la boutique quand
   des flacons partent d'ici. Un flacon part en vitrine comme testeur : il est
   présent, mais il ne se vend pas. Le compte vendable de la boutique est donc
   inférieur d'un flacon au nombre livré, la première fois seulement. */
.pcbloc{border:1px solid var(--line);border-radius:10px;background:var(--surface-2);
padding:12px 14px;margin:0 0 14px;font-size:13px;color:var(--ink-2);line-height:1.5}
.pcbloc h4{margin:0 0 8px;font-size:12px;font-weight:700;letter-spacing:.04em;
text-transform:uppercase;color:var(--ink-3)}
.pcbloc .rep{display:flex;gap:18px;flex-wrap:wrap;align-items:baseline;margin:0 0 8px}
.pcbloc .rep b{font-family:Inter,sans-serif;font-size:22px;font-weight:700;color:var(--ink);
display:block;line-height:1.1}
.pcbloc .rep .k{font-size:11.5px;color:var(--ink-3)}
.pcbloc label.sw{display:flex;gap:8px;align-items:flex-start;cursor:pointer;font-size:12.5px}
.pcbloc label.sw input{margin-top:2px}
.pcbloc .dj{color:var(--ink-3);font-size:12px;margin:6px 0 0}
.ajq{display:flex;align-items:center;gap:8px}
.ajq button{font-family:inherit;font-size:22px;font-weight:600;width:44px;height:46px;border-radius:9px;
border:1px solid var(--line);background:var(--surface);color:var(--ink-2);cursor:pointer;line-height:1}
.ajq button:hover{border-color:var(--iris);color:var(--iris);background:var(--iris-soft)}
.ajq input{width:104px;height:46px;text-align:center;font-family:Inter,sans-serif;font-size:23px;font-weight:800}
/* le résultat, en gros */
.ajres{display:flex;align-items:center;gap:14px;padding:14px 16px;border-radius:10px;
background:var(--surface-2);border:1px solid var(--line-2);flex-wrap:wrap}
.ajres.vide{color:var(--ink-3);font-size:13.5px;line-height:1.5;display:block}
.ajch{display:flex;align-items:baseline;gap:9px;font-family:Inter,sans-serif;font-variant-numeric:tabular-nums}
.ajch .av{font-size:22px;font-weight:700;color:var(--ink-3)}
.ajch .vers{font-size:17px;color:var(--ink-3);font-weight:500}
.ajch .ap{font-size:30px;font-weight:800;letter-spacing:-.02em;line-height:1}
.ajch .ap.m{color:var(--crit)} .ajch .ap.p{color:var(--good)} .ajch .ap.n{color:var(--ink)}
.ajres .dt{flex:1;min-width:170px;font-size:12.5px;color:var(--ink-2);line-height:1.55}
.ajres .dt b{color:var(--ink)}
.ajres .dt .w{color:var(--crit);font-weight:600}
.ajaide{font-size:12.5px;color:var(--ink-3);line-height:1.55;margin:7px 0 0}
.achp{display:none;align-items:center;gap:12px;padding:9px 11px;border:1px solid var(--iris);background:var(--iris-soft);border-radius:8px;margin-bottom:6px}
.achp.on{display:flex}
.achp img,.achp .miss{width:38px;height:48px;object-fit:contain;flex:0 0 auto;border-radius:4px;background:var(--surface)}
.achp .t{min-width:0;flex:1}
.achp .t b{display:block;font-size:14px;letter-spacing:-.01em}
.achp .t span{font-family:Inter,sans-serif;font-size:11.5px;color:var(--ink-2)}
.achp button{background:none;border:0;font:inherit;font-size:12px;color:var(--iris);text-decoration:underline;cursor:pointer}
.achres{border:1px solid var(--line);border-radius:8px;background:var(--surface);max-height:240px;overflow-y:auto;margin-top:4px;box-shadow:0 8px 24px rgba(0,0,0,.08)}
.achres div{padding:8px 11px;cursor:pointer;display:flex;justify-content:space-between;gap:10px;font-size:13px;border-bottom:1px solid var(--line-2)}
.achres div:last-child{border-bottom:0}
.achres div:hover{background:var(--iris-soft)}
.achres div b{font-weight:600}
.achres div span{font-family:Inter,sans-serif;font-size:11.5px;color:var(--ink-3);white-space:nowrap}
.achres .vide{color:var(--ink-3);cursor:default;font-style:italic}
.achrecap{font-size:13px;color:var(--ink-2);line-height:1.6;background:var(--surface-2);border-radius:8px;padding:10px 13px;min-height:22px}
/* ce qui manque encore pour pouvoir enregistrer : en rouge, on ne peut pas le rater */
.achrecap .manque{color:var(--crit);font-weight:600}
.achfn{font-size:12.5px;color:var(--ink-3);line-height:1.5;margin:0 0 9px}
.achfn b{color:var(--ink-2)}
.chknote{display:block;font-size:11.5px;color:var(--ink-3);line-height:1.5;margin-top:3px;font-weight:400}
.chknote b{color:var(--warn);font-weight:600}
.achrecap b{color:var(--ink)}
.achrecap .g{color:var(--good)} .achrecap .c{color:var(--crit)}
.dcanw{padding:0}
.dcanw summary{cursor:pointer;list-style:none;display:flex;align-items:center;gap:8px}
.dcanw summary::-webkit-details-marker{display:none}
.dcanw summary::before{content:"▸";font-size:12px;color:var(--ink-3);transition:transform .12s}
.dcanw[open] summary::before{transform:rotate(90deg)}
.dcanw summary h3{margin:0}
.dcanw .dcan{margin-top:12px}
@media(min-width:900px){.dr .dcan{grid-template-columns:repeat(4,1fr)}}
.dph img{width:100%;height:100%;max-width:100%;max-height:100%;object-fit:contain;
mix-blend-mode:multiply;display:block}
@media(prefers-color-scheme:dark){:root:not([data-theme="light"]) .dph img{mix-blend-mode:normal}}
:root[data-theme="dark"] .dph img{mix-blend-mode:normal}
.dchips{display:flex;flex-wrap:wrap;gap:5px}
.dsec{display:flex;flex-direction:column;gap:10px}
.dsec > h3,.dsec > summary > h3{margin:0;font-family:Inter,sans-serif;font-size:12.5px;letter-spacing:.12em;
text-transform:uppercase;color:var(--ink);font-weight:800;
padding-bottom:7px;border-bottom:1px solid var(--line-2)}
.dgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:11px}
.dcard{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:14px 16px;display:flex;flex-direction:column;gap:8px}
.dgrid.dg3{grid-template-columns:repeat(3,1fr)}
@media(max-width:760px){.dgrid.dg3{grid-template-columns:1fr 1fr}}
.dident .dfld input,.dident .dfld select,.dfrns .dfld input{background:var(--surface-2);border:1px solid var(--line);border-radius:8px;padding:8px 10px;font-size:14px}
.dident .dfld input:focus,.dident .dfld select:focus{background:var(--surface)}
.dident .dfld label{font-size:10px;color:var(--ink-3);letter-spacing:.1em}
.dhint{font-size:12px;color:var(--ink-3);line-height:1.5}
.dline{display:flex;flex-wrap:wrap;gap:6px 18px;font-size:12.5px;color:var(--ink-2);padding-top:8px;border-top:1px dashed var(--line-2)}
.dline b{font-weight:600;color:var(--ink)}

.dfld{display:flex;flex-direction:column;gap:4px}
.dfld label{font-family:Inter,sans-serif;font-size:9px;letter-spacing:.12em;
text-transform:uppercase;color:var(--ink-3);font-weight:500;display:flex;gap:5px;align-items:center}
.dfld input,.dfld select{font-family:inherit;font-size:14.5px;color:var(--ink);background:transparent;
border:1px solid transparent;border-bottom-color:var(--line-2);border-radius:4px;
padding:6px 8px;width:100%;transition:background .12s,border-color .12s}
.dfld input:hover,.dfld select:hover{background:var(--surface-2);border-color:var(--line)}
.dfld input:focus,.dfld select:focus{outline:0;border-color:var(--iris);box-shadow:0 0 0 3px var(--iris-soft);
background:var(--surface)}
.dfld input.vide{border-color:var(--warn);border-style:dashed;background:var(--warn-soft)}
.dfld input.mono{font-family:Inter,sans-serif;font-variant-numeric:tabular-nums}
.dfld.ch input{border-color:var(--iris);background:var(--iris-soft)}
.dcalc{display:grid;grid-template-columns:repeat(auto-fit,minmax(128px,1fr));gap:1px;
background:var(--line);border:1px solid var(--line);border-radius:6px;overflow:hidden}
.dcalc div{background:var(--surface-2);padding:11px 13px;display:flex;flex-direction:column;gap:3px}
.dcalc .v{font-family:Inter,sans-serif;font-size:17px;font-weight:600;line-height:1;
font-variant-numeric:tabular-nums}
.dcalc .k{font-size:11.5px;color:var(--ink-3)}
.dinfo{font-size:13.5px;color:var(--ink-2);line-height:1.6;background:var(--surface-2);
border-radius:5px;padding:10px 13px}
.dinfo b{color:var(--ink-2)}
.dinfo .mono{font-size:11.5px}
.df{flex:0 0 auto;padding:13px 20px;border-top:1px solid var(--line);background:var(--surface-2);
display:flex;gap:9px;align-items:center}
.df .st{font-size:12.5px;color:var(--ink-3);margin-right:auto}
.df .st.ok{color:var(--good)} .df .st.ko{color:var(--crit)}
.df .dsup{color:var(--crit);border-color:var(--crit)}
.df .dsup:hover{background:var(--crit-soft)}
.df .dsup[hidden]{display:none}
.df #dmod[hidden]{display:none}
#idov .fg{display:grid;grid-template-columns:1fr 1fr;gap:12px}#idov .fld.l{grid-column:1/-1}#idov .msg{min-height:20px;margin-top:8px;color:var(--crit)}
.card{cursor:pointer}
.card:focus-visible{outline:2px solid var(--iris);outline-offset:2px}
@media(max-width:640px){.dr{width:100%}.dhero{grid-template-columns:104px 1fr;gap:13px}
.dstk .big b{font-size:29px}.dqte input{font-size:28px;width:120px}.drail{grid-template-columns:1fr 1fr}
.drail .st:first-child{grid-column:1/-1}}

.svact{display:flex;gap:10px;flex-wrap:wrap;align-items:center;margin-top:4px}
.svinv{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:1px;
background:var(--line);border:1px solid var(--line);border-radius:8px;overflow:hidden}
.svinv div{background:var(--surface);padding:12px 14px;display:flex;flex-direction:column;gap:2px}
.svinv .v{font-family:Inter,sans-serif;font-size:21px;font-weight:700;line-height:1;
letter-spacing:-.03em;font-variant-numeric:tabular-nums}
.svinv .k{font-size:11.5px;color:var(--ink-3)}
.svok{background:var(--good-soft);color:var(--good);border-radius:6px;padding:11px 14px;
font-size:13px;font-weight:500;line-height:1.55;margin-top:12px}
.svko{background:var(--crit-soft);color:var(--crit);border-radius:6px;padding:11px 14px;
font-size:13px;font-weight:500;line-height:1.55;margin-top:12px}

.mhist{font-size:12.5px;color:var(--ink-2);line-height:1.55;background:var(--surface-2);border-radius:8px;padding:10px 13px}
.mhist b{color:var(--ink)}
.mhist ul{margin:6px 0 0;padding-left:18px;font-family:Inter,sans-serif;font-size:12px;font-variant-numeric:tabular-nums}
/* --- prix par canal --- */
.dcan{display:grid;grid-template-columns:repeat(auto-fill,minmax(190px,1fr));gap:10px}
.dcanl{display:flex;flex-direction:column;gap:6px}
.dcanl .cnh{display:grid;grid-template-columns:150px 150px 1fr 190px 110px;gap:12px;padding:0 10px}
.dcanl .cnh span{font-family:Inter,sans-serif;font-size:10px;letter-spacing:.1em;text-transform:uppercase;color:var(--ink-3);font-weight:700}
.dcanl .cn{display:grid;grid-template-columns:150px 150px 1fr 190px 110px;gap:12px;align-items:center;padding:9px 10px;text-align:left}
.dcanl .cn .c1{display:flex;flex-direction:column;gap:6px;align-items:center;text-align:center}
.dcanl .cn .nm{text-align:center;font-size:11px;display:flex;flex-direction:column;align-items:center;gap:3px}
.dcanl .cn .lg img{height:16px}.dcanl .cn .lg-site img{height:34px}
.dcanl .cn .sous{font-size:10px;margin-top:0;text-align:center;font-weight:700}
.dcanl .cn .etat{align-self:center;font-size:10px;padding:1px 7px;margin-top:2px}
.dcanl .cn .c2{display:flex;flex-direction:column;gap:3px;align-items:flex-start}
.dcanl .cn .in{justify-content:flex-start;padding:1px 4px}
.dcanl .cn .in::before{display:none}
.dcanl .cn input{font-size:24px;text-align:left;width:100px;flex:0 0 auto}
.dcanl .cn .in em{font-size:14px;flex:0 0 auto}
.dcanl .cn .rl{text-align:left;font-size:11.5px;font-weight:500}
.dcanl .cn .c3{min-width:0}
.dcanl .cn .sb{margin:0;padding:6px 8px;display:flex;flex-direction:column;gap:4px;align-items:stretch}
.dcanl .cn .sb .sbt{text-align:left}
.dcanl .cn .sb label{display:flex;align-items:center;gap:6px;justify-content:flex-start}
.dcanl .cn .sb label span{font-size:11px;color:var(--ink-3);width:64px;flex:0 0 64px;text-align:left}
.dcanl .cn .sb label input{width:84px;flex:0 0 84px}
.spw[hidden]{display:none}
.spw{display:inline-flex;align-items:center;gap:10px;margin:0 8px}
.spw select{font:600 13px Inter,sans-serif;padding:6px 8px;border:1px solid var(--line);border-radius:8px;background:var(--surface)}
.spw .spq{display:inline-flex;align-items:center;gap:6px;font:600 12.5px Inter,sans-serif;color:var(--ink-2)}
.dcanl .cn .sb label.rc{align-items:flex-start}
.dcanl .cn .sb label.rc span{width:auto;flex:1 1 auto;font-size:12px;color:var(--ink-2);font-weight:600}
.dcanl .cn .sb label.rc input{width:16px;flex:0 0 16px;margin:1px 0 0}
.dcanl .cn .sb .envs,.dcanl .cn .sb .lnk{align-self:flex-start}
.dcanl .cn .c2 .in input{width:auto;field-sizing:content;min-width:52px;max-width:120px}
.dcanl .cn .azp{display:flex;flex-direction:column;gap:2px;padding:6px 8px;border:1px solid var(--line);border-radius:8px;background:var(--surface)}
.dcanl .cn .azp .sbt{font-family:Inter,sans-serif;font-size:10px;letter-spacing:.08em;text-transform:uppercase;color:var(--ink-3);font-weight:700}
.dcanl .cn .azp b{font-family:Inter,sans-serif;font-size:20px;font-weight:800;letter-spacing:-.02em;line-height:1.1}
.dcanl .cn .azp small{font-size:11px;color:var(--ink-3)}
.dcanl .cn .azp .sbw{margin:4px 0 0}
.dcanl .cn .calc2{display:flex;flex-direction:column;gap:1px}
.dcanl .cn .calc2 b{font-family:Inter,sans-serif;font-size:20px;font-weight:800;letter-spacing:-.02em;line-height:1.1}
.dcanl .cn .calc2 b.g{color:var(--good)}.dcanl .cn .calc2 b.w{color:var(--warn)}.dcanl .cn .calc2 b.c{color:var(--crit)}.dcanl .cn .calc2 b.na{color:var(--ink-3)}
.dcanl .cn .calc2 small{font-size:11px;font-weight:600;color:var(--ink-2)}
.dcanl .cn .calc2 span{font-size:10.5px;color:var(--ink-3);line-height:1.35}
.dcanl .cn .calc.vide{font-size:11.5px;color:var(--ink-3)}
.dcanl .cn .sbd .sbs{display:flex;align-items:center;gap:8px;flex-wrap:wrap;padding:2px 0}
.dcanl .cn .sbd .sbs b{font-family:Inter,sans-serif;font-size:20px;font-weight:800;letter-spacing:-.02em}
.dcanl .cn .sbd .sbs small{font-size:11px;color:var(--ink-3)}
.dcanl .cn .sbd .sb{margin-top:4px}
.dcanl .cn{padding:6px 10px}
.dcanl .cn .azp{padding:4px 8px}
.dcanl .cn .azp b{font-size:18px}
.dcanl .cn .calc2 b{font-size:18px}
.dcanl .cn .c5{display:flex;justify-content:flex-end}
.dcanl .cn.off{opacity:.75}
.dcanl .cn .offtx{font-size:12px}
@media(max-width:900px){.dcanl .cnh{display:none}.dcanl .cn{grid-template-columns:1fr 1fr}.dcanl .cn .c3{grid-column:1/-1}.dcanl .cn .c5{justify-content:flex-start}}

.cn{display:flex;flex-direction:column;gap:5px;background:var(--surface-2);border:1px solid var(--line);
border-radius:9px;padding:10px 9px 9px;min-width:0}
.cn .nm{font-family:Inter,sans-serif;font-size:12.5px;letter-spacing:.08em;text-transform:uppercase;color:var(--ink);
font-weight:800;display:flex;flex-wrap:wrap;align-items:center;justify-content:center;gap:4px;white-space:normal;line-height:1.25;text-align:center;min-height:32px}
.cn .in{display:flex;align-items:baseline;justify-content:center;gap:3px;border:1px solid transparent;border-radius:5px;padding:2px 5px;
transition:background .12s,border-color .12s}
.cn .in:hover{background:var(--surface);border-color:var(--line)}
.cn .in:focus-within{background:var(--surface);border-color:var(--iris);box-shadow:0 0 0 3px var(--iris-soft)}
.cn .in::before{content:"";flex:0 0 13px}
.cn .in em{font-style:normal;font-family:Inter,sans-serif;font-size:17px;font-weight:700;color:var(--ink);flex:0 0 13px;text-align:left}
.cn input{font-family:Inter,sans-serif;font-size:32px;font-weight:800;color:var(--ink);font-variant-numeric:tabular-nums;
letter-spacing:-.03em;text-align:center;line-height:1.08;flex:1 1 auto;min-width:0;width:100%;background:transparent;border:0;padding:1px 0;-moz-appearance:textfield}
.cn input::-webkit-outer-spin-button,.cn input::-webkit-inner-spin-button{-webkit-appearance:none;margin:0}
.cn input:focus{outline:0}
.cn.off{background:var(--surface);border-style:dashed;justify-content:center;gap:9px;text-align:center;opacity:.85}
.cn.off .nm{color:var(--ink-3)}
.cn .offtx{font-family:Inter,sans-serif;font-size:13px;font-weight:700;color:var(--crit);letter-spacing:0;text-transform:none}
.cn .offb{font-family:inherit;font-size:11.5px;font-weight:600;color:var(--ink-3);background:none;border:1px solid var(--line);
border-radius:99px;padding:4px 10px;cursor:pointer;align-self:center;margin-top:2px}
.cn .offb:hover{border-color:var(--crit);color:var(--crit)}
.cn.off .offb:hover{border-color:var(--good);color:var(--good)}
.cn.man .in{border-color:var(--iris);background:var(--iris-soft)}
.cn.man input{color:var(--iris)}
.cn .ft{display:flex;flex-direction:column;align-items:center;gap:4px}
.cn .mg{font-style:normal;font-family:Inter,sans-serif;font-size:14.5px;font-weight:800;white-space:normal;text-align:center;padding:4px 9px;border-radius:12px;line-height:1.3;max-width:100%}
.cn .mg.g{background:var(--good-soft);color:var(--good)} .cn .mg.w{background:var(--warn-soft);color:var(--warn)}
.cn .mg.c{background:var(--crit-soft);color:var(--crit)} .cn .mg.na{background:var(--surface);color:var(--ink-3);border:1px dashed var(--line)}
.cn .rl{font-family:Inter,sans-serif;font-size:13px;color:var(--ink-2);white-space:normal;text-align:center;font-weight:600;line-height:1.4}
.cn .expl{font-family:Inter,sans-serif;font-size:13px;color:var(--ink);font-weight:500;text-align:center;line-height:1.45;font-variant-numeric:tabular-nums}
.cn .expl b{font-weight:800}.cn .expl b.g{color:var(--good)}.cn .expl b.w{color:var(--warn)}.cn .expl b.c{color:var(--crit)}.cn .expl b.na{color:var(--ink-3)}
.cn .lg img{height:20px}.cn .lg-site img{height:48px}
/* 24 sept. 2026 : la carte se lit de haut en bas — le canal, s'il est relié, le prix, d'où il
   vient, puis le calcul posé comme une addition : vendu, frais, achat, ce qu'il te reste. */
.dcanx{font-size:13px;color:var(--ink-2);line-height:1.55;margin:8px 0 0;max-width:80ch}
.dcanx b{color:var(--ink)}
.cn .sous{display:block;width:100%;font-size:10.5px;letter-spacing:.14em;color:var(--ink-2);margin-top:-2px}
.cn .etat{align-self:center;font-family:Inter,sans-serif;font-size:11px;font-weight:600;padding:2px 8px;border-radius:99px;text-align:center;line-height:1.35}
.cn .etat.ok{background:var(--good-soft);color:var(--good)} .cn .etat.no{background:var(--surface);color:var(--ink-3);border:1px dashed var(--line)}
.cn .mp{align-self:center;font-family:Inter,sans-serif;font-size:11px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--ink-2);display:flex;gap:4px;align-items:center}
.cn table.calc{width:100%;border-collapse:collapse;font-family:Inter,sans-serif;font-size:12.5px;font-variant-numeric:tabular-nums;margin-top:2px}
.cn table.calc td{padding:3px 2px;color:var(--ink-2);border-bottom:1px solid var(--line-2)}
.cn table.calc td:last-child{text-align:right;white-space:nowrap;color:var(--ink)}
.cn table.calc tr.tot td{border-bottom:0;border-top:1.5px solid var(--ink-3);padding-top:5px;color:var(--ink);font-weight:700}
.cn table.calc tr.tot b{font-size:15px;font-weight:800}
.cn table.calc tr.tot b.g{color:var(--good)} .cn table.calc tr.tot b.w{color:var(--warn)} .cn table.calc tr.tot b.c{color:var(--crit)}
.cn table.calc small{display:block;font-size:11px;font-weight:600;color:var(--ink-3)}
.cn .ss{font-family:Inter,sans-serif;font-size:12px;color:var(--ink-2);text-align:center;line-height:1.4}
.cn .ss b{color:var(--ink);font-variant-numeric:tabular-nums} .cn .ss.no{color:var(--ink-3)}
.cn .ss small{display:block;font-size:11px;color:var(--ink-3);text-decoration:line-through}
.cn .sb{display:flex;flex-direction:column;gap:5px;background:var(--surface);border:1px solid var(--line);border-radius:8px;padding:7px 8px}
.cn .sb .sbt{font-family:Inter,sans-serif;font-size:10.5px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:var(--ink-2);text-align:center}
.cn .sb label{display:flex;align-items:center;gap:6px;font-family:Inter,sans-serif;font-size:12px;color:var(--ink-2)}
.cn .sb label span{flex:1}
.cn .sb input{width:78px;font:600 13px Inter,sans-serif;text-align:right;padding:4px 6px;border:1px solid var(--line);border-radius:6px;background:var(--surface-2);font-variant-numeric:tabular-nums}
.cn .sb input:focus{outline:0;border-color:var(--iris);box-shadow:0 0 0 2px var(--iris-soft)}
.cn .sb em{font-style:normal;font-size:12px;color:var(--ink-3)}
.cn .sb .lnk{background:none;border:0;padding:0;font:600 11.5px Inter,sans-serif;color:var(--iris);text-decoration:underline;cursor:pointer;text-align:center}
.cn .envs{align-self:stretch;font-family:Inter,sans-serif;font-size:12.5px;font-weight:700;color:#fff;background:var(--iris);border:0;border-radius:8px;padding:7px 8px;cursor:pointer;line-height:1.3}
.cn .envs:hover{filter:brightness(1.08)} .cn .envs:disabled{opacity:.6;cursor:wait}
.cn .calc.vide{font-family:Inter,sans-serif;font-size:12.5px;color:var(--ink-3);text-align:center;line-height:1.45;padding:4px 2px}
.cn .rl button{background:none;border:0;padding:0;font:inherit;color:var(--iris);text-decoration:underline;cursor:pointer}
.dsec h3 .hh{font-weight:500;font-size:13px;color:var(--ink-2);letter-spacing:0;text-transform:none;margin-left:10px}
.dsec h3 .hh a{color:var(--iris)}
.pxt{width:100%;border-collapse:collapse;font-size:13.5px}
.pxt th{text-align:left;font-family:Inter,sans-serif;font-size:9.5px;letter-spacing:.11em;text-transform:uppercase;color:var(--ink-2);
font-weight:700;padding:7px 9px;border-bottom:1px solid var(--line);white-space:nowrap}
.pxt th.r,.pxt td.r{text-align:right;font-variant-numeric:tabular-nums}
.pxt td{padding:9px 9px;border-bottom:1px solid var(--line-2);vertical-align:middle}
.pxt td.av{color:var(--ink-3);text-decoration:line-through}
.pxt td.ap{font-weight:700;font-size:15px}
.pxt tr.bad td{background:var(--crit-soft)}
.pxt tr.bad td.ap{color:var(--crit)}
.pxt tr.big td.ap{color:var(--warn)}
.pxt .st{font-family:Inter,sans-serif;font-size:11.5px;font-weight:600;white-space:nowrap}
.pxt .st.ok{color:var(--good)} .pxt .st.ko{color:var(--crit)} .pxt .st.wa{color:var(--warn)} .pxt .st.na{color:var(--ink-3);font-weight:400}
.pxnote{font-size:12.5px;color:var(--ink-2);line-height:1.55;background:var(--surface-2);border-radius:8px;padding:10px 13px}
.pxnote b{color:var(--ink)}
/* --- historique du prix d'achat + position marché --- */
.per{display:flex;gap:4px;flex-wrap:wrap}
.per button{background:var(--surface-2);border:1px solid var(--line);border-radius:20px;
padding:5px 12px;font-family:inherit;font-size:11.5px;font-weight:600;color:var(--ink-2);cursor:pointer;
line-height:1;transition:all .12s}
.per button:hover{border-color:var(--iris);color:var(--iris)}
.per button.on{background:var(--iris);border-color:var(--iris);color:#fff}
:root[data-theme="dark"] .per button.on{color:#16121F}
@media(prefers-color-scheme:dark){:root:not([data-theme="light"]) .per button.on{color:#16121F}}
.crb{background:var(--surface-2);border:1px solid var(--line);border-radius:9px;padding:10px 8px 6px;
position:relative}
.crb svg{display:block;width:100%;height:118px}
.crb .gl{stroke:var(--line);stroke-width:1}
.crb .ln{fill:none;stroke:var(--iris);stroke-width:2;stroke-linejoin:round;stroke-linecap:round}
.crb .ar{fill:var(--iris);opacity:.09}
.crb .pt{fill:var(--surface);stroke:var(--iris);stroke-width:2;cursor:pointer}
.crb .pt:hover{stroke-width:3.5}
.crb .pt.lo{stroke:var(--good)} .crb .pt.hi{stroke:var(--crit)}
.crb .pt.der{fill:var(--iris)}
.crb text{font-family:Inter,sans-serif;fill:var(--ink-3)}
.crb text.ax{font-size:10px}
.crb text.lab{font-size:12px;font-weight:700;fill:var(--ink-2)}
.crb text.lo{fill:var(--good)} .crb text.hi{fill:var(--crit)}
.crb .hit{fill:transparent;cursor:pointer}
.crb .hit:hover~.pt,.crb .pt:hover{stroke-width:3}
.cinf{position:absolute;pointer-events:none;background:var(--ink);color:var(--surface);
border-radius:6px;padding:7px 10px;font-size:11.5px;line-height:1.45;white-space:nowrap;
opacity:0;transition:opacity .1s;z-index:5;font-family:Inter,sans-serif}
.cinf.on{opacity:1}
.cinf b{color:var(--surface);font-weight:700}
.vdet{margin-top:8px;border-top:1px solid var(--line);padding-top:6px}
.vdet>summary{cursor:pointer;font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:var(--ink-3);font-weight:700;padding:4px 0}
.vdet>summary:hover{color:var(--ink)}
.dvt>summary{list-style:none;cursor:pointer;display:flex;align-items:baseline;gap:12px;flex-wrap:wrap;padding:2px 0}
.dvt>summary::-webkit-details-marker{display:none}
.dvt .vs-t{font-size:11px;letter-spacing:.1em;text-transform:uppercase;font-weight:700}
.dvt .vs-n{font-size:12.5px;color:var(--ink-2)}
.dvt .vs-c{margin-left:auto;color:var(--ink-3);transition:transform .15s}
.dvt[open]>summary .vs-c{transform:rotate(180deg)}
.dvt>summary:hover .vs-c{color:var(--ink)}
.vryt{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:1px;background:var(--line);border:1px solid var(--line);border-radius:8px;overflow:hidden;margin-bottom:8px}
.vryt div{background:var(--surface-2);padding:9px 12px;display:flex;flex-direction:column;gap:2px}
.vryt .v{font-family:Inter,sans-serif;font-size:16px;font-weight:700;line-height:1.1;font-variant-numeric:tabular-nums;letter-spacing:-.02em}
.vryt .k{font-size:10.5px;color:var(--ink-3);line-height:1.3}
.vmois{display:flex;gap:4px;align-items:flex-end;height:84px;padding:6px 4px 0;border:1px solid var(--line);border-radius:8px;background:var(--surface);margin-bottom:10px}
.vmois .vm{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:flex-end;gap:2px;min-width:0}
.vmois i{display:block;width:70%;background:var(--iris);border-radius:3px 3px 0 0;min-height:2px}
.vmois i.z{background:var(--line)} .vmois i.neg{background:var(--crit)}
.vmois b{font-family:Inter,sans-serif;font-size:10px;font-weight:700;line-height:1;height:10px}
.vmois span{font-size:9.5px;color:var(--ink-3);text-transform:uppercase;letter-spacing:.04em}
.vlist li.vlk{cursor:pointer} .vlist li.vlk:hover{background:var(--surface-2)}
.vlist .mg{font-family:Inter,sans-serif;font-size:11.5px;font-weight:600;color:var(--good);min-width:64px;text-align:right}
.vlist .mg.neg,.vtab td.neg{color:var(--crit)}
.vtab{width:100%;border-collapse:collapse;font-size:12.5px;margin-top:4px}
.vtab th{text-align:left;font-size:10px;letter-spacing:.08em;text-transform:uppercase;color:var(--ink-3);padding:4px 8px;border-bottom:1px solid var(--line)}
.vtab td{padding:6px 8px;border-bottom:1px solid var(--line-2)}
.vtab .r{text-align:right;font-variant-numeric:tabular-nums}
.vdeux{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin:10px 0}
@media(max-width:760px){.vdeux{grid-template-columns:1fr}}
.vdeux h4,.dsec h4{margin:8px 0 2px;font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:var(--ink-3)}
.vlist .q.ret{color:var(--crit);font-weight:700}
.hst{display:grid;grid-template-columns:repeat(auto-fit,minmax(104px,1fr));gap:1px;
background:var(--line);border:1px solid var(--line);border-radius:8px;overflow:hidden}
.hst div{background:var(--surface-2);padding:10px 12px;display:flex;flex-direction:column;gap:2px}
.hst .v{font-family:Inter,sans-serif;font-size:16px;font-weight:700;line-height:1;
font-variant-numeric:tabular-nums;letter-spacing:-.025em}
.hst .k{font-size:10.5px;color:var(--ink-3);line-height:1.3}
.hst .v.lo{color:var(--good)} .hst .v.hi{color:var(--crit)}
.ach{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:1px;
background:var(--line);border:1px solid var(--line);border-radius:8px;overflow:hidden}
.ach li{background:var(--surface);padding:9px 12px;display:flex;align-items:baseline;gap:10px;
font-size:12.5px}
.ach .d{font-family:Inter,sans-serif;font-size:11.5px;color:var(--ink-3);flex:0 0 74px}
.ach .f{flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.ach .q{font-family:Inter,sans-serif;color:var(--ink-3);font-size:11.5px}
.ach .p{font-family:Inter,sans-serif;font-weight:700;font-variant-numeric:tabular-nums}
.ach .p.lo{color:var(--good)} .ach .p.hi{color:var(--crit)}
.ach .x{background:none;border:0;color:var(--ink-3);cursor:pointer;font-size:15px;line-height:1;padding:0 2px}
.ach .x:hover{color:var(--crit)}
.rgb{display:grid;grid-template-columns:auto 1fr;gap:14px;align-items:center;
background:var(--surface-2);border:1px solid var(--line);border-radius:9px;padding:14px 16px}
.rgn{display:flex;flex-direction:column;align-items:center;gap:1px;padding-right:14px;
border-right:1px solid var(--line)}
.rgn b{font-family:Inter,sans-serif;font-size:30px;font-weight:700;line-height:1;
letter-spacing:-.04em;color:var(--iris)}
.rgn span{font-size:9.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--ink-3);font-weight:600}
.rgd{display:flex;flex-direction:column;gap:5px;min-width:0}
.rgd .cat{font-size:13.5px;font-weight:600;line-height:1.3}
.rgd .dem{font-size:12px;color:var(--ink-2)}
.rgd .dem b{color:var(--iris);font-weight:700}
.rgd .dt{font-size:11px;color:var(--ink-3);font-family:Inter,sans-serif}
.cmp{display:grid;grid-template-columns:repeat(auto-fit,minmax(96px,1fr));gap:1px;
background:var(--line);border:1px solid var(--line);border-radius:8px;overflow:hidden}
.cmp div{background:var(--surface);padding:10px 12px;display:flex;flex-direction:column;gap:2px}
.cmp .v{font-family:Inter,sans-serif;font-size:15px;font-weight:700;
font-variant-numeric:tabular-nums;letter-spacing:-.02em;line-height:1.1}
.cmp .k{font-size:10px;letter-spacing:.06em;text-transform:uppercase;color:var(--ink-3);font-weight:600}
.cmp .moi{background:var(--iris-soft)}
.cmp .moi .k{color:var(--iris)}
.mvide{font-size:12.5px;color:var(--ink-3);line-height:1.6;background:var(--surface-2);
border-radius:7px;padding:12px 14px}
.mvide b{color:var(--ink-2)}


.frow3{display:grid;grid-template-columns:1fr 168px 168px;gap:12px}
@media(max-width:660px){.frow3{grid-template-columns:1fr}}
.fzone2{margin-top:12px}
.fzone2 textarea{width:100%;min-height:170px;font-family:Inter,sans-serif;font-size:12px;
border:1px solid var(--line);border-radius:7px;padding:11px;background:var(--surface-2);color:var(--ink);
resize:vertical;line-height:1.6}
.fzone2 textarea:focus{outline:0;border-color:var(--iris);box-shadow:0 0 0 3px var(--iris-soft);background:var(--surface)}
.chk{display:flex;gap:9px;align-items:flex-start;font-size:12.5px;color:var(--ink-2);line-height:1.5;
cursor:pointer;max-width:76ch}
.chk input{margin-top:2px;flex:0 0 auto}
.chk b{color:var(--ink)}
.ftb{width:100%;border-collapse:collapse;font-size:12.5px}
.ftb th{text-align:left;font-family:Inter,sans-serif;font-size:9.5px;letter-spacing:.11em;
text-transform:uppercase;color:var(--ink-2);font-weight:700;padding:8px 10px;border-bottom:1px solid var(--line)}
.ftb td{padding:8px 10px;border-bottom:1px solid var(--line-2);vertical-align:top}
.ftb td.n{font-family:Inter,sans-serif;text-align:right;font-variant-numeric:tabular-nums;
white-space:nowrap;font-weight:600}
.ftb .baisse{color:var(--good)} .ftb .hausse{color:var(--crit)}
.ftb .ref b{display:block;font-weight:600}
.ftb .ref span{color:var(--ink-3);font-size:11px;font-family:Inter,sans-serif}
.ftb tr.inc{background:var(--warn-soft)}


/* ---------- BASCULE ET VUE EN LISTE ---------- */
.vue{display:inline-flex;gap:2px;background:var(--surface-2);border:1px solid var(--line);
border-radius:8px;padding:2px}
.vue button{background:none;border:0;border-radius:6px;padding:6px 12px;font-family:inherit;
font-size:12.5px;font-weight:600;color:var(--ink-3);cursor:pointer;line-height:1.3;white-space:nowrap}
.vue button:hover{color:var(--ink)}
.vue button.on{background:var(--surface);color:var(--iris);box-shadow:0 1px 2px rgba(0,0,0,.08)}
.lstw{overflow:visible;border:1px solid var(--line);border-radius:10px;background:var(--surface)}
/* (l'ancien « @media(max-width:1439px){.lstw{overflow-x:auto}} » est remplacé par .defile, posé par le script seulement quand le tableau dépasse) */
.lstw.defile .lst thead th{position:static}   /* un en-tête figé dans une boîte qui défile se retrouve au milieu du tableau */
/* Igal, 24 sept. 2026 : sur son grand écran, la colonne Alertes sortait du cadre
   (le tableau était plus large que sa boîte, et la boîte laissait dépasser).
   Deux choses : le cadre du catalogue est plus large (1600 px au lieu de 1400),
   et si malgré tout le tableau ne tient pas, la boîte le fait défiler au lieu
   de le laisser dépasser — c'est le script qui pose .defile quand ça arrive. */
.lstw.defile{overflow-x:auto}
body.cat .wrap{max-width:1600px}
.lst{width:100%;border-collapse:collapse;font-size:13.5px;min-width:0}
/* Plus de min-width : les colonnes se retirent d'après la largeur de la boîte
   (container queries plus bas), le tableau n'a donc jamais besoin d'être plus
   large que sa boîte. S'il l'est quand même, le script pose .defile. */
.lst td.colsite{width:74px}
/* la fenêtre « Mettre les sites à jour » */
.sbw{font-size:12.5px;line-height:1.45;color:#b3261e;background:#fff3f0;border:1px solid #f3c9bf;border-radius:7px;padding:6px 9px;margin:4px 0 6px}
.psq{display:flex;flex-direction:column;gap:7px;margin:14px 0 0;font-size:13.5px}
.psq label{display:flex;align-items:center;gap:8px;cursor:pointer}
.pstot{margin:12px 0 10px;font-size:14px}
.pstot b{font-weight:800}
.psz{color:var(--crit)}
.pst{width:100%;border-collapse:collapse;font-size:13px;border:1px solid var(--line);border-radius:8px;overflow:hidden}
.pst th{text-align:left;font-family:Inter,sans-serif;font-size:10.5px;letter-spacing:.08em;text-transform:uppercase;
 color:var(--ink-3);font-weight:700;padding:8px 10px;background:var(--surface-2);border-bottom:1px solid var(--line)}
.pst th.r,.pst td.r{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
.pst td{padding:7px 10px;border-bottom:1px solid var(--line-2)}
.pst td small{display:block;color:var(--ink-3);font-size:11px}
.pst tbody tr:last-child td{border-bottom:0}
.psvide{padding:22px;text-align:center;color:var(--ink-2);border:2px dashed var(--line);border-radius:10px}
.lst td.lno,.lst th.lno{width:46px;text-align:right;padding-right:9px;color:var(--ink-3);
font-family:Inter,sans-serif;font-size:11.5px;font-variant-numeric:tabular-nums}
.lst th.lno{cursor:default;background:var(--surface-2)}
.lst thead th{position:sticky;top:var(--barh,0px);z-index:2;background:var(--surface-2);box-shadow:0 1px 0 var(--line);
font-family:Inter,sans-serif;font-size:9.5px;letter-spacing:.11em;text-transform:uppercase;
color:var(--ink-2);font-weight:700;text-align:left;padding:12px 12px;
border-bottom:1px solid var(--line);white-space:nowrap}
.lst thead th.r{text-align:right}
.lst tbody tr{cursor:pointer;border-bottom:1px solid var(--line-3)}
.lst tbody tr:last-child{border-bottom:0}
/* Dix colonnes : une ligne sur deux teintee, pour suivre la meme ligne
   du nom jusqu'au code-barres sans se tromper de rangee. */
.lst tbody tr:nth-child(even){background:var(--surface-2)}
.lst tbody tr:hover,.lst tbody tr:nth-child(even):hover{background:var(--iris-soft)}
.lst tbody tr:focus-visible{outline:2px solid var(--iris);outline-offset:-2px}
.lst tbody tr.alert{box-shadow:inset 3px 0 0 var(--crit)}
.lst tbody tr.warn{box-shadow:inset 3px 0 0 var(--warn)}
.lst td{padding:11px 12px;vertical-align:middle}
.lst td.r{text-align:right;font-family:Inter,sans-serif;font-variant-numeric:tabular-nums;
white-space:nowrap}
.lph{width:62px;height:62px;border-radius:9px;background:var(--surface-2);border:1px solid var(--line-2);
display:flex;align-items:center;justify-content:center;overflow:hidden;flex:0 0 62px}
.lph img{width:100%;height:100%;object-fit:contain;mix-blend-mode:multiply;display:block;padding:5px}
@media(prefers-color-scheme:dark){:root:not([data-theme="light"]) .lph img{mix-blend-mode:normal}}
:root[data-theme="dark"] .lph img{mix-blend-mode:normal}
.lph svg{width:23px;height:34px;color:var(--line-3)}
.lph .miss{border:0;background:none;padding:0;gap:0;width:100%;height:100%;
display:flex;align-items:center;justify-content:center}
.lph .miss span{display:none}
.lph .miss svg{width:23px;height:34px}
.lid{display:flex;align-items:center;gap:14px;min-width:0}
.lid .tx{min-width:0}
.lmq{font-size:11.5px;font-weight:700;letter-spacing:.07em;text-transform:uppercase;color:var(--iris);
line-height:1.3;overflow-wrap:anywhere}
/* 11 oct. 2026 (Igal) : le nom coupé par « … » rendait deux parfums proches indiscernables
   (« Le Male Elixir Absolu 4.2 » et « Le Male Elixir … »). Le nom s'écrit en entier, sur
   deux lignes s'il le faut : la ligne est un peu plus haute, mais on sait ce qu'on regarde. */
.lnm{font-size:15px;font-weight:700;color:var(--ink);letter-spacing:-.015em;line-height:1.3;
white-space:normal;overflow-wrap:anywhere;max-width:420px}
/* « 3.4 oz · EDC · Homme » tenait sur une seule ligne coûte que coûte, et cette
   colonne à elle seule prenait 141 px de large. Elle se replie maintenant sur
   deux lignes quand il le faut : la place gagnée sert au tableau à tenir dans
   l'écran, ce qui vaut mieux qu'un débordement sur la droite. */
.lmeta{font-size:12.5px;color:var(--ink-2)}
.laz{display:inline-flex;align-items:center;margin-left:7px;vertical-align:middle;text-transform:none;letter-spacing:0;padding:1px 6px;border:1px solid var(--line);border-radius:99px;background:var(--surface);line-height:1}
.laz .lg img{height:11px;display:block}
.meta .laz{margin-left:6px}
.lbc{font-family:Inter,sans-serif;font-size:11px;color:var(--ink-3);white-space:nowrap}
.lq{font-family:Inter,sans-serif;font-weight:700;font-size:15px;font-variant-numeric:tabular-nums}
.lq.out{color:var(--ink-3);font-weight:400;font-size:11.5px;font-family:Inter,sans-serif}
/* étiquette de comptage, sous la quantité */
.lvf{display:flex;justify-content:flex-end;align-items:center;gap:3px;margin-top:2px;
font-family:Inter,sans-serif;font-size:10.5px;font-weight:600;letter-spacing:.01em;
white-space:nowrap;line-height:1.2}
.lvf svg{width:9px;height:9px;flex:none}
.lvf.ok{color:var(--good)}
.lvf.fic{color:var(--ink-3);font-weight:500}
.lvf.non{color:var(--ink-3);font-weight:400;opacity:.65}
.lvf.av{color:var(--warn)}
.lq.low{color:var(--warn)}
/* Les cinq chiffres d'une ligne — achat, gros, retail et les deux marges —
   ont la meme taille et la meme graisse : on les compare d'un coup d'oeil.
   Seule la couleur les distingue. */
.lpa,.lpr,.lpw,.lmg{font-family:Inter,sans-serif;font-size:16px;font-weight:700;
 letter-spacing:-.015em;font-variant-numeric:tabular-nums}
.lpa{color:var(--ink-2)}
.lpr{color:var(--ink)}
.lpw{color:var(--iris)}
.lna{color:var(--ink-3);font-size:11.5px;font-style:italic;font-family:Inter,sans-serif;font-weight:400}
/* La colonne Amazon : le prix qu'on trouve en face, et l'ecart avec le mien.
   L'ecart n'est ni vert ni rouge : etre au-dessus d'Amazon n'est pas une faute
   en boutique, et etre en dessous n'est pas une victoire. La seule chose
   vraiment mauvaise — Amazon vend moins cher que ce que j'ai paye — est le seul
   cas colore. */
.laz{color:var(--ink);font-weight:600}
.lazd{display:block;font-family:Inter,sans-serif;font-size:11px;color:var(--ink-3);
font-weight:500;margin-top:1px;white-space:nowrap}
.lazd.perte{color:var(--crit);font-weight:700}
.lazv{color:var(--ink-3);font-size:11.5px;font-style:italic;font-family:Inter,sans-serif}
.lsq{display:block;font-family:Inter,sans-serif;font-size:13px;color:var(--ink-2);white-space:nowrap;font-variant-numeric:tabular-nums}
.lsq b.ecart{color:var(--warn);font-weight:800}
.lsn{font-style:normal;color:var(--ink-3);opacity:.7}
.lsd{display:block;font-family:Inter,sans-serif;font-size:11px;color:var(--ink-3);line-height:1.25}
.lsz{display:block;font-family:Inter,sans-serif;font-size:11px;color:var(--crit);white-space:nowrap}
.lsv{color:var(--ink-3);font-size:11.5px;font-style:italic;font-family:Inter,sans-serif}
.lst thead th.colsite span{white-space:normal;line-height:1.25;max-width:62px}
.laz.vieux{color:var(--ink-2);font-weight:500}
.lazage{display:block;font-family:Inter,sans-serif;font-size:10px;color:var(--ink-3);
letter-spacing:.02em;margin-top:1px;white-space:nowrap}
.lazage.perime{color:var(--warn)}
.lmg.g{color:var(--good)} .lmg.w{color:var(--warn)} .lmg.c{color:var(--crit)}
.lfl{display:flex;flex-direction:column;align-items:flex-start;gap:4px;white-space:nowrap;max-width:230px}
.lfl>*{white-space:normal}
.lfl .fl{font-size:11px;padding:4px 9px 4px 7px}
.lst td.colfl{min-width:190px}
.lst thead th.colmg span{white-space:normal;line-height:1.25;max-width:78px}
/* Les alertes restent écrites en toutes lettres (demande d'Igal : pas de « +1 »),
   mais une alerte longue se replie au lieu d'élargir la colonne — et donc le
   tableau entier — jusqu'à déborder de l'écran. */
.lfl .fl{max-width:none;overflow:visible;white-space:normal}
@media(max-width:1560px){.lfl{white-space:normal}}
.lst thead th.r span{white-space:normal;line-height:1.2;max-width:72px}
/* Sur un ecran de portable, le nom se resserre et le code-barres se cache pour que
   la colonne Alertes reste visible sans faire defiler le tableau. */
.lnm{max-width:240px}.lst td,.lst thead th{padding-left:8px;padding-right:8px}
/* Le tableau doit TENIR dans l'écran. Il débordait sur la droite — 1 342 px de
   colonnes pour 1 152 px de place sur un portable — et la page entière prenait
   une barre de défilement horizontale. On resserre donc par paliers : le
   code-barres disparaît le premier (il se lit dans la fiche), puis le nom se
   raccourcit, puis les colonnes de chiffres se serrent. Rien n'est supprimé. */
/* le code-barres ne revient que quand il y a vraiment la place : à 1 700 px
   il repoussait encore le tableau de 41 px hors de l'écran. Et même au-delà,
   il doit se serrer : la zone de contenu ne dépasse jamais 1 346 px. */
@media(max-width:20000px){.lst .colbc{display:none}}
.lst .colbc{padding-left:4px;padding-right:4px}
.lst td.colbc .lbc{font-size:11px;letter-spacing:0}
@media(max-width:1560px){.lnm{max-width:170px}.lst td,.lst thead th{padding-left:7px;padding-right:7px}
  .lst td.r,.lst thead th.r{padding-left:6px;padding-right:6px}
  .lst td.colfl{min-width:140px}.lmeta{font-size:12px}.lst td.colsite{width:64px}}
/* En dessous, on ne peut plus se contenter de resserrer : Igal travaille dans une
   fenêtre d'environ mille pixels, et douze colonnes n'y tiennent pas, quoi qu'on
   fasse. On en RETIRE donc, de la moins utile à la plus utile, et on le dit à
   l'écran pour que personne ne croie que l'outil a perdu une donnée :
     — le Format, déjà écrit sous le nom du parfum (« 3.4 oz · EDP · Homme ») ;
     — la Marge retail, qui se recalcule de tête depuis le prix d'achat ;
     — le prix Amazon, qui n'a de sens que quand un relevé vient d'être fait ;
     — le Prix retail en dernier, parce qu'on ne vend pas au détail en gros.
   Tout reste dans la fiche du parfum, et revient dès qu'on élargit la fenêtre. */
/* 24 sept. 2026 : ces seuils étaient mesurés sur la LARGEUR DE LA FENÊTRE, alors
   que ce qui compte est la largeur de la boîte du tableau (fenêtre moins le menu
   de gauche, moins les marges). Chez Igal, à 1 456 px de fenêtre, la boîte ne
   faisait que 1 170 px : aucune colonne n'était retirée et les Alertes sortaient
   du cadre. On mesure donc la boîte elle-même (container query). */
.lstw{container-type:inline-size}
/* Quand le tableau dépasse quand même (anglais, espagnol : des en-têtes plus longs),
   ajusteDefile retire ces colonnes une par une, dans cet ordre, avant de se résoudre
   à faire défiler : on garde toujours les Alertes dans le cadre. */
/* 30 sept. 2026 (Igal) : la marge retail doit se voir — le prix Amazon part avant elle */
.lstw.x1 .lst .colfmt,.lstw.x2 .lst .colaz,.lstw.x3 .lst .colmgr,.lstw.x4 .lst .colpvr{display:none}
.lbn{font-family:ui-monospace,Menlo,monospace;font-size:11px;color:var(--ink-3);letter-spacing:.02em;margin-top:1px}
@container (max-width:1270px){.lst .colfmt{display:none}}
/* 11 oct. 2026 (Igal : « j'aimerais bien qu'il y ait la contenance ») : quand la colonne Format
   n'a plus la place, la contenance, le type et le genre passent sous le nom, toujours lisibles */
.lsub{display:none;font-size:12px;color:var(--ink-2);margin-top:1px}
.lsub b{font-weight:600}
.lstw.x1 .lst .lsub{display:block}
@container (max-width:1270px){.lst .lsub{display:block}}
@container (max-width:1080px){.lst .colaz{display:none}}
/* 12 oct. 2026 (Igal : « enlève-moi Amazon sur la ligne ») : la colonne Amazon n'est plus affichée dans la liste (le prix Amazon n'est plus suivi) ; la cellule reste dans la page pour les contrôles */
.lst .colaz,.lst th.colaz{display:none!important}
@container (max-width:960px){.lst .colmgr{display:none}}
@container (max-width:860px){.lst .colpvr{display:none}.lnm{max-width:130px}
  .lst td.colfl{min-width:0}.lfl .fl{font-size:10.5px;padding:3px 7px 3px 6px}
  .lst td,.lst thead th{padding-left:5px;padding-right:5px}
  .lst td.r,.lst thead th.r{padding-left:4px;padding-right:4px}
  .lst thead th.r span{max-width:56px;font-size:10px}
  .lid .lph{display:none}          /* la vignette part : elle prend 40 px par ligne */
  .lst td.colsite{width:56px}.lmeta{font-size:11.5px}}
/* La barre d'outils : elle passait à la ligne trop tard et poussait la page
   entière vers la droite. Elle se replie maintenant dès qu'elle est serrée. */
@media(max-width:1180px){.bar .acts{flex-wrap:wrap;justify-content:flex-end}
  .bar .btn{font-size:12.5px;padding:7px 10px}}
body.client .lst .colpa,body.client .lst .colq,body.client .lst .colmg,body.client .lst .colfl{display:none}
/* Igal, 12 oct. 2026 : « quand j'appuie sur décroissant / croissant, toute la ligne bouge ».
   Tableau en largeurs automatiques : chaque tri change les textes visibles, donc la largeur
   de CHAQUE colonne se recalculait et tout glissait (nom 331 → 369 → 306 px). Largeurs fixes :
   les colonnes de chiffres ont leur largeur, le nom prend le reste, et rien ne bouge au tri. */
body.cat .status{min-height:28px}   /* la pastille « TRI » apparaît et disparaît : sans hauteur réservée, l'en-tête montait et descendait de 9 px à chaque clic */
body.cat .lst{table-layout:fixed}
body.cat .lst thead th.lno{width:46px}
body.cat .lst thead th.r{width:92px}
body.cat .lst thead th.colq{width:84px}
body.cat .lst thead th.colsite{width:78px}
body.cat .lst thead th.colmg{width:100px}
body.cat .lst thead th.colfl{width:200px}
@media(max-width:1560px){body.cat .lst thead th.r{width:84px}body.cat .lst thead th.colq{width:76px}body.cat .lst thead th.colsite{width:68px}body.cat .lst thead th.colmg{width:90px}body.cat .lst thead th.colfl{width:150px}}
@container (max-width:860px){body.cat .lst thead th.colfl{width:auto}}


.lst thead th.so{cursor:pointer;user-select:none;transition:color .12s,background .12s}
.lst thead th.so span{display:inline-flex;align-items:center;gap:5px}
.lst thead th.so i{font-style:normal;font-size:10px;opacity:.28;transition:opacity .12s}
.lst thead th.so:hover{color:var(--iris);background:var(--iris-soft)}
.lst thead th.so:hover i{opacity:.7}
.lst thead th.so:focus-visible{outline:2px solid var(--iris);outline-offset:-2px}
.lst thead th.so.on{color:var(--iris);background:var(--iris-soft);
box-shadow:inset 0 -2px 0 var(--iris)}
.lst thead th.so.on i{opacity:1;font-size:11px}
.lst thead th.r span{justify-content:flex-end}


.seuil{display:inline-flex;align-items:center;gap:7px;font-size:12.5px;color:var(--ink-2);
white-space:nowrap;cursor:default}
.seuil input{width:52px;padding:6px 7px;font-family:inherit;font-size:13px;font-weight:700;
text-align:center;border:1px solid var(--line);border-radius:6px;background:var(--surface);
color:var(--ink);-moz-appearance:textfield}
.seuil input::-webkit-outer-spin-button,.seuil input::-webkit-inner-spin-button{
-webkit-appearance:none;margin:0}
.seuil input:hover{border-color:var(--ink-3)}
.seuil input:focus{outline:0;border-color:var(--iris);box-shadow:0 0 0 3px var(--iris-soft)}
.seuil em{font-style:normal;font-size:11.5px;color:var(--warn);font-weight:600}

/* ---------- MISE A JOUR DU STOCK ---------- */
.rapsv{display:flex;align-items:center;gap:12px;flex-wrap:wrap;font-size:13px;color:var(--ink-2);
background:var(--warn-soft);border:1px solid var(--warn);border-left-width:4px;border-radius:0 8px 8px 0;
padding:12px 16px;margin:0 0 14px;line-height:1.5}
.rapsv b{color:var(--ink)}
.rapsv .btn{margin-left:auto;flex:0 0 auto}
.extb{display:flex;align-items:center;gap:11px;flex-wrap:wrap;font-size:13px;color:var(--ink-2);
background:var(--iris-soft);border:1px solid var(--iris);border-radius:8px;
padding:10px 14px;margin:0 0 14px}

.mjz{border:2px dashed var(--line);border-radius:9px;padding:16px;background:var(--surface-2);
display:flex;flex-direction:column;gap:9px;align-items:flex-start}
.mjz textarea{width:100%;min-height:130px;font-family:Inter,sans-serif;font-size:12px;
border:1px solid var(--line);border-radius:6px;padding:10px;background:var(--surface);
color:var(--ink);resize:vertical;line-height:1.5}
.mjz textarea:focus{outline:0;border-color:var(--iris);box-shadow:0 0 0 3px var(--iris-soft)}
.mjmap{display:flex;gap:14px;flex-wrap:wrap;font-size:12.5px;color:var(--ink-2);
background:var(--iris-soft);border-radius:7px;padding:10px 14px;align-items:center}
.mjmap b{font-family:Inter,sans-serif;color:var(--iris);font-weight:600}
.mjk{display:grid;grid-template-columns:repeat(auto-fit,minmax(112px,1fr));gap:1px;
background:var(--line);border:1px solid var(--line);border-radius:8px;overflow:hidden}
.mjk div{background:var(--surface);padding:11px 13px;display:flex;flex-direction:column;gap:2px}
.mjk .v{font-family:Inter,sans-serif;font-size:20px;font-weight:700;line-height:1;
font-variant-numeric:tabular-nums;letter-spacing:-.025em}
.mjk .k{font-size:11.5px;color:var(--ink-3)}
.mjt{width:100%;border-collapse:collapse;font-size:12.5px}
.mjt th{text-align:left;font-family:Inter,sans-serif;font-size:9.5px;letter-spacing:.11em;
text-transform:uppercase;color:var(--ink-2);font-weight:700;padding:7px 9px;
border-bottom:1px solid var(--line)}
.mjt td{padding:7px 9px;border-bottom:1px solid var(--line-2);vertical-align:top}
.mjt td.n{font-family:Inter,sans-serif;text-align:right;font-variant-numeric:tabular-nums;
white-space:nowrap;font-weight:600}
.mjt .up{color:var(--good)} .mjt .dn{color:var(--crit)}
.mjt tbody tr:hover{background:var(--surface-2)}
.mjw{font-size:12.5px;color:var(--ink-2);background:var(--warn-soft);border-left:3px solid var(--warn);
border-radius:5px;padding:11px 14px;line-height:1.55}
.mjw b{color:var(--ink)}
.mjsrc{display:inline-flex;align-items:center;gap:6px;font-size:11px;font-weight:600;
background:var(--iris-soft);color:var(--iris);padding:5px 10px;border-radius:20px;line-height:1}

/* ---------- AJOUT D'ARTICLE ---------- */
.ov{position:fixed;inset:0;background:rgba(23,23,29,.55);backdrop-filter:blur(2px);
z-index:50;display:none;align-items:flex-start;justify-content:center;padding:36px 18px;overflow-y:auto}
.ov.on{display:flex}
.mod{background:var(--surface);border:1px solid var(--line);border-radius:6px;width:100%;
max-width:820px;box-shadow:0 18px 48px rgba(0,0,0,.22);display:flex;flex-direction:column}
.mh{padding:18px 22px;border-bottom:1px solid var(--line);display:flex;align-items:center;gap:14px}
.mh h2{margin:0;font-size:18px;font-weight:700;letter-spacing:-.02em}
.mh .x{margin-left:auto;background:none;border:0;font-size:22px;color:var(--ink-3);
cursor:pointer;line-height:1;padding:2px 6px}
.mh .x:hover{color:var(--ink)}
.tabs{display:flex;gap:2px;padding:0 22px;border-bottom:1px solid var(--line);background:var(--surface-2)}
.tab{background:none;border:0;border-bottom:2px solid transparent;padding:11px 14px;font-family:inherit;
font-size:13.5px;font-weight:500;color:var(--ink-3);cursor:pointer}
.tab.on{color:var(--iris);border-bottom-color:var(--iris);font-weight:600}
.mb{padding:20px 22px;display:flex;flex-direction:column;gap:16px}
.pane{display:none;flex-direction:column;gap:16px}
.pane.on{display:flex}
.fg{display:grid;grid-template-columns:repeat(auto-fit,minmax(178px,1fr));gap:13px}
.fld{display:flex;flex-direction:column;gap:5px}
.fld label{font-family:Inter,sans-serif;font-size:9.5px;letter-spacing:.12em;
text-transform:uppercase;color:var(--ink-3);font-weight:500}
.fld label b{color:var(--crit)}
.fhint{font-size:11.5px;color:var(--ink-3);line-height:1.4}
.pxsit{margin-top:14px;padding:12px 14px;border:1px solid var(--iris);border-radius:8px;background:var(--iris-soft);font-size:13.5px}
.pxenv{padding:12px 14px;border:1px solid var(--iris);border-radius:8px;background:var(--iris-soft);font-size:13.5px}.pxsit ul{margin:8px 0 0;padding-left:20px;line-height:1.7}.pxsit small{color:var(--ink-3)}
.pxsc{display:flex;gap:8px;align-items:center;font-weight:700;cursor:pointer}
.pxbas{margin:8px 0 0;color:var(--crit)}
body.sansPA .legend,body.sansPA .flags,body.sansPA .selw:has(#fan){display:none!important}
.fld input,.fld select,.mb textarea{font-family:inherit;font-size:13.5px;color:var(--ink);
background:var(--surface-2);border:1px solid var(--line);border-radius:3px;padding:8px 10px;width:100%}
.fld input:focus,.fld select:focus,.mb textarea:focus{outline:2px solid var(--iris);outline-offset:1px;background:var(--surface)}
.mb textarea{min-height:150px;resize:vertical;font-family:Inter,sans-serif;font-size:12px;line-height:1.6}
.hint{font-size:12.5px;color:var(--ink-3);line-height:1.6;margin:0}
.hint code{font-family:Inter,sans-serif;font-size:11.5px;background:var(--line-2);
padding:1px 5px;border-radius:2px;color:var(--ink-2)}
.mf{padding:15px 22px;border-top:1px solid var(--line);display:flex;gap:9px;align-items:center;background:var(--surface-2)}
.mf .msg{font-size:12.5px;color:var(--ink-3);margin-right:auto}
.mf .msg.err{color:var(--crit)} .mf .msg.ok{color:var(--good)}
.btn{font-family:inherit;font-size:13.5px;font-weight:500;color:var(--ink-2);background:var(--surface);
border:1px solid var(--line);border-radius:3px;padding:9px 16px;cursor:pointer}
.btn:hover{border-color:var(--iris);color:var(--iris)}
.btn.pri{background:var(--iris);border-color:var(--iris);color:#fff;font-weight:600}
.btn.pri:hover{filter:brightness(1.08);color:#fff}
.prev{border:1px solid var(--line);border-radius:3px;overflow:auto;max-height:280px}
.prev table{width:100%;border-collapse:collapse;font-size:12.5px}
.prev th{position:sticky;top:0;background:var(--surface-2);text-align:left;padding:7px 10px;
font-family:Inter,sans-serif;font-size:9.5px;letter-spacing:.09em;text-transform:uppercase;
color:var(--ink-3);border-bottom:1px solid var(--line);white-space:nowrap}
.prev td{padding:6px 10px;border-bottom:1px solid var(--line-2)}
.prev td.n{font-family:Inter,sans-serif;text-align:right;font-variant-numeric:tabular-nums}
.prev .vide{color:var(--warn);font-style:italic}
.card.neuf{border-color:var(--iris);border-width:1px;box-shadow:inset 3px 0 0 var(--iris)}
.chipn{position:absolute;top:9px;left:9px;font-family:Inter,sans-serif;font-size:9px;
letter-spacing:.08em;text-transform:uppercase;padding:3px 7px;border-radius:99px;
background:var(--iris);color:#fff;font-weight:600}
.fl.todo{background:var(--iris-soft);color:var(--iris)}
.fl.plus{background:var(--surface-2);color:var(--ink-3)}
.fl.plus::before{display:none}
.empty b{display:block;font-size:15.5px;font-weight:600;color:var(--ink);margin-bottom:6px;
letter-spacing:-.01em}
.empty span{display:block;font-size:13.5px;line-height:1.6;max-width:60ch;margin:0 auto 14px}
.empty .btn{margin-top:2px}
.empty{text-align:center;padding:70px 20px;color:var(--ink-3)}
#more{display:block;margin:26px auto 0;font-family:inherit;font-size:14px;font-weight:500;color:var(--ink);
background:var(--surface);border:1px solid var(--line);border-radius:3px;padding:11px 26px;cursor:pointer}
#more:hover{border-color:var(--iris);color:var(--iris)}
.legend{margin-top:20px;padding:14px 18px;background:var(--iris-soft);border-left:3px solid var(--iris);
border-radius:0 3px 3px 0;font-size:13px;color:var(--ink-2);line-height:1.65;max-width:78ch}
.legend b{color:var(--ink)}
.legend .k{font-family:Inter,sans-serif;font-weight:700;color:var(--iris)}
.legend .k.bad{color:var(--crit)}
footer{margin-top:40px;border-top:1px solid var(--line);padding-top:15px;font-size:12.5px;color:var(--ink-3);
display:flex;flex-wrap:wrap;gap:8px;justify-content:space-between}
__AIDECSS__
/* nouvelles références pour Lightspeed */
.btn.lspd{background:#e8412c;border-color:#e8412c;color:#fff;font-weight:700;display:inline-flex;align-items:center;gap:8px;padding:9px 16px 9px 12px}
.btn.lspd:hover{filter:brightness(1.08);color:#fff}
.btn.lspd svg{width:16px;height:18px;flex:none;fill:#fff}
.lsm-etat{display:flex;gap:14px;flex-wrap:wrap;align-items:center;padding:12px 14px;border:1px solid var(--line);border-radius:6px;background:var(--surface-2)}
.lsm-etat b{font-size:15px}
.lsm-kpi{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px}
.lsm-kpi div{border:1px solid var(--line);border-radius:6px;padding:10px 12px}
.lsm-kpi b{display:block;font-size:20px;font-weight:700}
.lsm-kpi span{font-size:12px;color:var(--ink-3)}
.lsm-tab td{vertical-align:middle}
.lsm-tab select{max-width:320px;font:inherit;font-size:12.5px;padding:4px 6px}
.lsm-tab .btn{padding:5px 9px;font-size:12px;margin-left:4px}
.lsm-depot{font-size:12.5px;color:var(--ink-3)}
.lsm-fiche{color:inherit;font-weight:600;text-decoration:underline;text-underline-offset:2px}
.lsm-bloque{margin:8px 0;padding:10px 12px;border:1px solid #e8412c;border-left:4px solid #e8412c;border-radius:6px;background:rgba(232,65,44,.07);font-size:13px;font-weight:600}
.lsm-depot input{font-size:12px}
.lsnv-tete{margin:4px 0 2px;font-size:14px}
.lsnv-av{margin-top:16px;color:var(--crit)}
.lsnv-case{display:flex;gap:8px;align-items:center;margin:6px 0 10px;font-size:13.5px;cursor:pointer}
.lsnv-tab{max-height:300px}
.lsnv-tab td.num,.lsnv-tab th.num{text-align:right;white-space:nowrap}
.lsnv-why{color:var(--crit);font-size:12px}
.lsnv-tab small{color:var(--ink-3)}
</style></head><body class="cat">
<div class="app">

<aside class="side">
  <div class="logo">
    <div class="n">Perfumes Trade</div>
    <div class="s">ERP</div>
  </div>
  <nav>
    <span class="navlab">Produits</span>
__BARRE__
  </nav>
  <div class="sfoot"><div id="sfu" class="sfu"></div><span id="sfoot">__TOTAL__ références · __ENSTOCK__ en stock · __UNITES__ unités</span>
  <div class="ver" title="Si cette date n'est pas la derni&egrave;re, recharge avec Cmd+Option+R">version du __VERSION__</div>
    <div class="sfline" id="sfline"></div></div>
</aside>

<div class="main"><div class="wrap">

<header><div><div class="eyebrow">Catalogue</div><h1>Catalogue Parfums</h1></div>
<div class="src">Photos : perfumestrade.com<br>Stock : Test inventory sam.xlsx<br>2 septembre 2026</div></header>

<div class="bar">
 <div class="brow">
  <div class="srch" id="srch">
    <svg viewBox="0 0 20 20" fill="none" aria-hidden="true"><circle cx="9" cy="9" r="6.2"
      stroke="currentColor" stroke-width="1.9"/><path d="M13.6 13.6L17.5 17.5" stroke="currentColor"
      stroke-width="1.9" stroke-linecap="round"/></svg>
    <input type="search" id="q" autocomplete="off" placeholder="Rechercher une marque, un nom, un code-barres…" aria-label="Rechercher">
    <button class="clr" id="qx" aria-label="Effacer la recherche">&times;</button>
  </div>

  <div class="seg" id="seg" role="group" aria-label="Disponibilité">
    <button data-v="in" class="on">En stock</button>
    <button data-v="out">Historique</button>
    <button data-v="">Tout</button>
    <button data-v="az">Vendus sur Amazon</button>
    <button data-v="sp">Sans prix sur le site</button>
  </div>
  <span id="spwrap" class="spw" hidden><select id="fsp" aria-label="Site"><option value="">Wholesale et retail</option><option value="g">Wholesale seulement</option><option value="d">Retail seulement</option></select><label class="spq"><input type="checkbox" id="fspq" checked><span>En stock seulement</span></label></span>
  <select id="fs" hidden><option value="in" selected></option><option value="out"></option><option value=""></option><option value="az"></option><option value="sp"></option></select>

  <div class="selw"><select id="fb" aria-label="Marque"><option value="">Toutes les marques</option></select></div>
  <div class="selw"><select id="fg" aria-label="Genre"><option value="">Tous genres</option>
    <option value="M">Homme</option><option value="W">Femme</option>
    <option value="U">Unisexe</option><option value="K">Enfant</option></select></div>
  <!-- Igal, 17 oct. 2026 : « sur le catalogue et dans les filtres, cibler tout de suite ceux qui ne sont pas diffusés sur un des trois canaux » -->
  <div class="selw"><select id="fd" aria-label="Diffusion"><option value="">Diffusion : toute</option>
    <option value="any">Pas diffusé sur un des trois</option><option value="site">Pas sur perfumestrade.com</option>
    <option value="sitegros">Pas sur le site de gros</option><option value="perfumecity">Pas sur Perfume City</option>
    <option value="all">Diffusé sur les trois</option></select></div>

  <button class="more" id="advb" aria-expanded="false">Plus de filtres
    <span class="bdg" id="bdg">0</span><span class="cv"></span></button>

  <div class="acts">
    <button class="btn" id="exa" style="display:none">Exporter mes corrections</button>
    <div class="vue" id="vue">
      <button data-vue="grille" title="Vignettes">▦ Vignettes</button>
      <button data-vue="liste" title="Liste">☰ Liste</button>
    </div>
    <button class="btn" id="azimp">Relevé Amazon</button>
    <button class="btn" id="fac">Enregistrer une facture</button>
    <button class="btn" id="svg">Sauvegarder mon travail</button>
    <button class="btn" id="lsnv">Nouvelles réf. pour Lightspeed</button>
    <button class="btn lspd" id="lsmaj" data-nolang><svg viewBox="0 0 16 18" aria-hidden="true"><path d="M8.6 0.4c0.3 2.6 1.9 3.9 3.6 5.7 1.8 1.9 3 4 2.6 6.6-0.5 3.2-3.1 5.3-6.6 5.3-3.8 0-6.5-2.5-6.5-6.1 0-2.5 1.3-4.3 3.3-6.2-0.1 1.6 0.4 2.8 1.5 3.3-0.4-2.3 0.2-4.6 2.1-8.6zM8.1 9.6c-1.6 1.1-2.4 2.3-2.4 3.5 0 1.5 1 2.6 2.4 2.6s2.4-1 2.4-2.5c0-1.2-0.8-2.3-2.4-3.6z"/></svg><span id="lsmaj-t">Mettre à jour Lightspeed</span></button>
    <button class="btn" id="plb" title="La liste de tout ce qui est en stock, avec le prix de gros — en PDF ou en Excel, à envoyer à un client">Price list</button>
    <button class="btn" id="maj">Mettre à jour le stock</button>
    <button class="btn" id="psite" style="display:none">Mettre les sites à jour</button>
    <button class="btn pri" id="add">+ Nouvel article</button>
  </div>
 </div>

 <div class="adv" id="adv">
  <span class="lab">Affiner</span>
  <div class="selw"><select id="ft" aria-label="Type"><option value="">Tous types</option></select></div>
  <div class="selw"><select id="fan" aria-label="Prix"><option value="">Prix : tous</option>
    <option value="all">⚠ Toute anomalie (__A0__)</option>
    <option value="1">Gros à perte (__A1__)</option><option value="2">Retail à perte (__A2__)</option>
    <option value="3">Gros supérieur au retail (__A3__)</option><option value="4">Marge gros sous 10 % (__A4__)</option>
    <option value="5">Marge gros au-dessus de 60 % (__A5__)</option><option value="6">Retail &gt; 3x le prix d'achat (__A6__)</option>
    <option value="7">Aucun prix de gros (__A7__)</option><option value="8">Aucun prix retail (__A8__)</option>
    <option value="9">Gros = retail (__A9__)</option></select></div>
  <div class="selw"><select id="fp" aria-label="Photo"><option value="">Photo : toutes</option>
    <option value="1">Avec photo</option><option value="0">Sans photo</option></select></div>
  <div class="selw"><select id="fx" aria-label="Fiche"><option value="">Fiches : toutes</option>
    <option value="neuf">Ajoutées à la main</option><option value="mod">Modifiées</option>
    <option value="todo">À compléter</option><option value="retire">Retirées du catalogue</option></select></div>
  <div class="selw"><select id="fo" aria-label="Tri"><option value="b">Tri : marque</option>
    <option value="q">Tri : stock ↓</option><option value="p">Tri : prix gros ↑</option></select></div>
  <span class="sep"></span>
  <label class="seuil" title="En dessous de ce nombre de flacons, la quantité s'affiche en orange">
    <span>Stock faible sous</span>
    <input type="number" id="fseuil" min="0" max="999" step="1" value="3">
    <span>flacons</span><em id="fseuiln"></em></label>
  <span class="sep"></span>
  <label class="sw"><input type="checkbox" id="fa"><span class="tr"></span><span class="tx">Prix repris du site *</span></label>
  <label class="sw"><input type="checkbox" id="fc"><span class="tr"></span><span class="tx">Mode client</span></label>
 </div>

 <div class="extb" id="extb" style="display:none"></div>
 <div class="status"><span class="count" id="cnt"></span><span class="chips" id="chips"></span></div>
 <div class="mel" id="mel" hidden></div>
</div>

<div class="ov" id="fcov">
 <div class="mod" style="max-width:880px">
  <div class="mh"><h2>Enregistrer une facture ou une feuille de tarifs</h2><button class="x" id="fcx">&times;</button></div>
  <div class="mb" style="max-height:72vh;overflow-y:auto">
   <p class="hint">Colle les lignes. Chaque ligne doit contenir un <b>code-barres</b> et un <b>prix unitaire</b>.
   Les produits déjà connus reçoivent un nouveau point dans leur historique de prix —
   <b>aucun doublon n'est créé</b>. Les codes inconnus sont signalés à part.
   Un PDF ne peut pas être lu par la page : ouvre-le, sélectionne le tableau, copie, colle ici.</p>
   <div class="frow3">
     <div class="fld"><label>Fournisseur</label><input id="fc-frn" list="l-frns" placeholder="Miami Trading Zone"><datalist id="l-frns"></datalist></div>
     <div class="fld"><label>Date de la facture</label><input id="fc-date" type="date"></div>
     <div class="fld"><label>Numéro (facultatif)</label><input id="fc-num" placeholder="MPSINV79971"></div>
   </div>
   <div class="fzone2"><textarea id="fc-txt" placeholder="1  614514464441  RASASI HAWAS TROPICAL 3.4 EDP M  47  24.50  1,151.50"></textarea></div>
   <label class="chk" style="margin-top:10px"><input type="checkbox" id="fc-maj" checked>
     <span>Adopter ces prix comme <b>nouveau prix d'achat courant</b> — c'est ce qu'on veut d'une feuille de tarifs, pas d'une vieille facture.</span></label>
   <div id="fc-res" style="margin-top:16px"></div>
  </div>
  <div class="mf"><span class="msg" id="fc-msg"></span>
    <button class="btn" id="fc-c">Annuler</button>
    <button class="btn pri" id="fc-ok" disabled>Enregistrer</button></div>
 </div>
</div>
<div class="ov" id="svov">
 <div class="mod" style="max-width:640px">
  <div class="mh"><h2>Sauvegarder mon travail</h2><button class="x" id="svx">&times;</button></div>
  <div class="mb">
   <p class="hint"><b>À ne pas confondre avec « Exporter mes corrections ».</b> Cette sauvegarde
   est un fichier qui se <b>recharge dans l'outil</b> — c'est ton filet de sécurité.
   L'export, lui, est un tableau lisible dans Excel, pour reporter les changements
   dans le fichier maître ou les transmettre à quelqu'un.</p>
   <p class="hint">Tout ce que tu saisis vit dans <b>ce navigateur, sur cet ordinateur</b>.
   Un nettoyage de l'historique, un autre navigateur, un déplacement du dossier, et c'est perdu.
   Une sauvegarde est un fichier que tu gardes — c'est la seule copie qui ne dépend de rien.</p>
   <div id="svinv"></div>
   <div class="svact">
     <button class="btn pri" id="svdl">Télécharger la sauvegarde</button>
     <label class="btn" for="svup" style="cursor:pointer">Restaurer un fichier…</label>
     <input type="file" id="svup" accept=".json" hidden>
   </div>
   <div id="svmsg2"></div>
  </div>
  <div class="mf"><span class="msg" id="svmsg"></span><button class="btn" id="svc">Fermer</button></div>
 </div>
</div>
<div class="ov" id="plov">
 <div class="mod" style="max-width:640px">
  <div class="mh"><h2>Price list</h2><button class="x" id="pl-x">&times;</button></div>
  <div class="mb">
   <p class="hint" style="margin:0 0 12px">Tous les parfums <b>en stock</b>, triés par marque. Coche ce que le client doit voir, choisis le format, puis télécharge ou envoie.</p>
   <div class="fg" style="display:grid;gap:10px">
    <label><input type="checkbox" id="pl-prix" checked> <b>Prix de gros</b></label>
    <label><input type="checkbox" id="pl-qte"> Quantité en stock</label>
    <label><input type="checkbox" id="pl-sans"> Mettre aussi les parfums sans prix de gros (« prix sur demande »)</label>
    <div style="display:flex;gap:18px;flex-wrap:wrap;align-items:center;margin-top:4px">
     <span>Format :</span>
     <label><input type="radio" name="plf" value="pdf" checked> PDF avec le logo</label>
     <label><input type="radio" name="plf" value="xlsx"> Excel</label>
    </div>
    <div style="display:flex;gap:18px;flex-wrap:wrap;align-items:center">
     <span>Langue du document :</span>
     <select id="pl-lg" class="sel"><option value="en" selected>English</option><option value="es">Español</option><option value="fr">Français</option></select>
    </div>
    <div class="fld"><label for="pl-client">Pour le client (facultatif, écrit en tête du document)</label><input id="pl-client" placeholder="Nom du client" autocomplete="off"></div>
   </div>
   <p class="hint" id="pl-compte" style="margin:12px 0 0"></p>
   <div id="pl-env" style="display:none;margin-top:12px;border-top:1px solid var(--line,#e4e2ea);padding-top:12px">
    <div class="fld"><label for="pl-tel">WhatsApp — numéro du client</label><input id="pl-tel" placeholder="305 555 0100" autocomplete="off"></div>
    <div class="fld" style="margin-top:8px"><label for="pl-mail">Email — adresse du client</label><input id="pl-mail" placeholder="client@exemple.com" autocomplete="off"></div>
   </div>
  </div>
  <div class="mf"><span class="msg" id="pl-msg"></span>
   <button class="btn" id="pl-ann">Fermer</button>
   <button class="btn" id="pl-wa" title="Le PDF est déposé en ligne et le lien part dans WhatsApp">WhatsApp</button>
   <button class="btn" id="pl-em" title="Le PDF est déposé en ligne et le lien part par email">Email</button>
   <button class="btn pri" id="pl-dl">Télécharger</button></div>
 </div>
</div>

<div class="ov" id="mjov">
 <div class="mod">
  <div class="mh"><h2>Mettre à jour le stock</h2><button class="x" id="mjx">&times;</button></div>
  <div class="mb" style="max-height:68vh;overflow-y:auto">
   <p class="hint">Ouvre ton Google Sheet, sélectionne tout (<b>Ctrl/Cmd + A</b>) puis copie
   (<b>Ctrl/Cmd + C</b>), et colle ici. Un fichier CSV exporté depuis le Sheet marche aussi.
   Rien ne part sur Internet : tout est lu dans ce navigateur.</p>
   <div class="mjz">
    <textarea id="mjtxt" placeholder="Colle ici les lignes du Google Sheet..."></textarea>
    <input type="file" id="mjfile" accept="__ACCEPT_TAB__" style="font-size:12.5px">
   </div>
   <div id="mjres" style="margin-top:16px"></div>
  </div>
  <div class="mf"><span class="msg" id="mjmsg"></span>
   <button class="btn" id="mjc">Annuler</button>
   <button class="btn pri" id="mjok" disabled>Appliquer</button></div>
 </div>
</div>
<div class="ov" id="psov">
 <div class="mod" style="max-width:820px">
  <div class="mh"><h2>Mettre les sites à jour</h2><button class="x" id="psx">&times;</button></div>
  <div class="mb" style="max-height:66vh;overflow-y:auto">
   <p class="hint">Ce qui suit part sur <b>la vraie boutique</b>, visible par les clients. Seule la
   quantité restante est modifiée par « Envoyer au site » (les prix ont leur propre bouton, plus bas, et rien ne part sans ton clic) : ni les textes, ni les photos, ni la mise en ligne.
   Une fiche qui ne compte pas ses unités sur le site n'est pas touchée, et une référence absente du
   site n'y est pas créée.</p>
   <div class="psq">
     <label><input type="radio" name="psq" value="" checked> Le site de détail — perfumestrade.com</label>
     <label><input type="radio" name="psq" value="gros"> Le site de gros — wholesale.perfumestrade.com</label>
   </div>
   <div id="psres" style="margin-top:14px"></div>
   <div id="psecarts"></div>
   <div id="psprix"></div>
  </div>
  <div class="mf"><span class="msg" id="psmsg"></span>
   <button class="btn" id="psc">Annuler</button>
   <button class="btn pri" id="psok" disabled>Envoyer au site</button></div>
 </div>
</div>
<div class="ov" id="achov">
 <div class="mod" style="max-width:720px">
  <div class="mh"><h2>Enregistrer un achat</h2><button class="x" id="achx">&times;</button></div>
  <div class="mb">
   <p class="hint" style="margin:0 0 12px;padding:9px 12px;background:var(--iris-soft);border-radius:8px;font-size:13px;line-height:1.5">
     <b>Tu as la facture en PDF ?</b> Dépose-la dans <a href="factures.html?sens=achat">Factures</a> : elle est lue,
     tu vérifies les lignes, tu confirmes — sans rien retaper. Le formulaire ci-dessous sert pour un achat sans facture.</p>
   <div class="fld"><label>Produit</label>
     <div class="achp" id="achp"></div>
     <input id="ach-q" placeholder="Scanner ou taper un code-barres, ou chercher par nom…" autocomplete="off">
     <div class="achres" id="achres" hidden></div></div>
   <div class="fg">
     <div class="fld"><label>Fournisseur <b>*</b></label>
       <select id="ach-f"></select>
       <input id="ach-fn" placeholder="Nom du nouveau fournisseur" hidden></div>
     <div class="fld"><label>Date de l'achat</label><input id="ach-d" type="date"></div>
     <div class="fld"><label>Quantité achetée</label><input id="ach-n" type="number" min="1" step="1" inputmode="numeric" placeholder="ex : 12"></div>
     <div class="fld"><label>Prix d'achat unitaire ($) <b>*</b></label><input id="ach-p" type="number" min="0" step="any" inputmode="decimal" placeholder="ex : 74.50"></div>
     <div class="fld"><label>N° de facture (facultatif)</label><input id="ach-num" placeholder="MPSINV79971"></div>
   </div>
   <div id="ach-nouveau" hidden>
     <div class="achfn" id="ach-fsrc"></div>
     <div class="fg">
       <div class="fld"><label>Téléphone du fournisseur</label><input id="ach-ft" placeholder="(305) 000-0000"></div>
       <div class="fld"><label>E-mail du fournisseur</label><input id="ach-fe" placeholder="contact@…"></div>
     </div>
   </div>
   <label class="chk"><input type="checkbox" id="ach-prix" checked><span><b>Adopter ce prix comme prix d'achat</b> du produit — c'est ce qu'on attend d'un achat récent. Décoche si tu saisis un vieil achat.<br><span class="chknote">Aujourd'hui ce prix <b>remplace</b> l'ancien. Faut-il plutôt faire la moyenne de ce qu'il a réellement payé ? C'est la question 32, à trancher avec lui.</span></span></label>
   <label class="chk"><input type="checkbox" id="ach-stock"><span><b>Ajouter la quantité au stock</b> — coche si cette marchandise n'est pas encore comptée dans le stock affiché.</span></label>
   <div class="achrecap" id="achrecap"></div>
  </div>
  <div class="mf"><span class="msg" id="achmsg"></span>
   <button class="btn" id="achc">Annuler</button>
   <button class="btn pri" id="achok" disabled>Enregistrer l'achat</button></div>
 </div>
</div>
<div class="ov" id="ajov">
 <div class="mod" style="max-width:660px">
  <div class="mh"><h2>Ajuster le stock</h2><button class="x" id="ajx">&times;</button></div>
  <div class="mb">
   <div class="achp on" id="ajp"></div>
   <div id="ajmot"></div>
   <div class="fg">
     <div class="fld"><label id="ajnlab">Combien de flacons</label>
       <div class="ajq"><button type="button" id="ajm" title="Un de moins">−</button>
         <input id="aj-n" type="number" min="0" step="1" inputmode="numeric" placeholder="0">
         <button type="button" id="ajp2" title="Un de plus">+</button></div></div>
     <div class="fld"><label>Quand</label><input id="aj-d" type="date"></div>
     <div class="fld"><label>Précision (facultatif)</label><input id="aj-note" placeholder="tombé au comptoir, carton non livré…"></div>
   </div>
   <div class="pcbloc" id="ajpc" hidden></div>
   <div class="ajres vide" id="ajrecap"></div>
  </div>
  <div class="mf"><span class="msg" id="ajmsg"></span>
   <button class="btn" id="ajc">Annuler</button>
   <button class="btn pri" id="ajok" disabled>Enregistrer l'ajustement</button></div>
 </div>
</div>
<div class="ov" id="marov">
 <div class="mod" style="max-width:760px">
  <div class="mh"><h2>Relevé Amazon</h2><button class="x" id="marx">&times;</button></div>
  <div class="mb">
   <div class="fld"><label>Colle ici ce que tu vois sur la fiche Amazon</label>
     <textarea class="mzone" id="mar-colle" placeholder="Ouvre la fiche Amazon du parfum, sélectionne le prix, le bloc « Best Sellers Rank », les avis, l'adresse de la page — et colle tout ici. L'outil en tire les chiffres tout seul."></textarea>
     <div id="mar-lu"></div></div>
   <div class="fg">
     <div class="fld"><label>Prix le moins cher ($)</label><input id="mar-amz" type="number" step="any" inputmode="decimal" placeholder="vide si indisponible"></div>
     <div class="fld"><label>Rang dans sa catégorie</label><input id="mar-rang" type="number" step="1" inputmode="numeric" placeholder="674"></div>
     <div class="fld"><label>Nom de la catégorie</label><input id="mar-cat" placeholder="Men's Eau de Toilette"></div>
     <div class="fld"><label>Rang général</label><input id="mar-rangG" type="number" step="1" inputmode="numeric" placeholder="157867"></div>
     <div class="fld"><label>Catégorie générale</label><input id="mar-catG" placeholder="Beauty &amp; Personal Care"></div>
     <div class="fld"><label>Note (sur 5)</label><input id="mar-note" type="number" step="0.1" min="0" max="5" inputmode="decimal" placeholder="4.2"></div>
     <div class="fld"><label>Nombre d'avis</label><input id="mar-avis" type="number" step="1" inputmode="numeric" placeholder="111"></div>
     <div class="fld"><label>Achetés le mois dernier</label><input id="mar-dem" placeholder="200+"></div>
     <div class="fld"><label>Vendu par</label><input id="mar-vend" placeholder="Amazon.com"></div>
     <div class="fld"><label>Nombre de vendeurs</label><input id="mar-n" type="number" step="1" inputmode="numeric" placeholder="2"></div>
   </div>
   <div class="fld"><label>Lien de la fiche Amazon</label><input id="mar-url" placeholder="https://www.amazon.com/dp/…"></div>
   <div class="fld"><label>Remarque</label><input id="mar-obs" placeholder="indisponible, édition limitée, plus que 3 en stock…"></div>
   <div class="achrecap" id="marrecap"></div>
  </div>
  <div class="mf"><span class="msg" id="marmsg"></span>
   <button class="btn" id="marc">Annuler</button>
   <button class="btn pri" id="marok">Enregistrer le relevé</button></div>
 </div>
</div>
<div class="ov" id="pxov">
 <div class="mod" style="max-width:700px">
  <div class="mh"><h2>Confirmer les prix</h2><button class="x" id="pxx">&times;</button></div>
  <div class="mb" id="pxb"></div>
  <div class="mf"><span class="msg" id="pxmsg"></span>
   <button class="btn" id="pxc">Revenir à la fiche</button>
   <button class="btn pri" id="pxok">OK, enregistrer</button></div>
 </div>
</div>
<div class="ov" id="azov"><div class="mod" role="dialog" aria-modal="true" aria-labelledby="azt" style="max-width:660px">
  <div class="mh"><h2 id="azt">Relevé Amazon</h2><button class="x" id="azx" aria-label="Fermer">&times;</button></div>
  <div class="mb">
    <p class="hint">Un fichier de prix relevés sur Amazon, une ligne par parfum.
    Je reconnais les colonnes <code>asin</code> ou <code>code-barres</code> pour retrouver la référence, et
    <code>prix</code> pour la valeur — plus, si elles y sont, <code>vendeur</code>, <code>nb vendeurs</code>,
    <code>rang</code>, <code>catégorie</code>, <code>note</code>, <code>avis</code>, <code>date</code>, <code>url</code>.
    L'ordre et la casse n'ont pas d'importance. <code>.csv</code> ou <code>.xlsx</code>.</p>
    <p class="hint">Une ligne sans prix vaut <b>indisponible sur Amazon</b> — ce n'est pas la même chose
    qu'une ligne absente, qui elle ne touche à rien.</p>
    <input type="file" id="azfi" accept="__ACCEPT_TAB__" style="font-size:13.5px">
    <div class="prev" id="azpv" style="display:none"></div>
  </div>
  <div class="mf"><span class="msg" id="azmsg"></span>
    <button class="btn" id="azannul">Annuler</button>
    <button class="btn pri" id="azok" disabled>Enregistrer les relevés</button></div>
</div></div>
<!-- 3 oct. 2026 — point 8 de Sam : le fichier d'inventaire envoyé à Lightspeed ne crée pas
     les parfums que la caisse ne connaît pas. Ce fichier-ci les crée, avec ce que Sam a mis dans l'ERP. -->
<div class="ov" id="lsmov"><div class="mod" role="dialog" aria-modal="true" aria-labelledby="lsmt" style="max-width:860px">
  <div class="mh"><h2 id="lsmt" data-nolang>Mettre à jour Lightspeed</h2><button class="x" id="lsmx" aria-label="Fermer">&times;</button></div>
  <div class="mb" id="lsmcorps" data-nolang></div>
  <div class="mf"><span class="msg" id="lsmmsg" data-nolang></span>
    <button class="btn" id="lsmannul" data-nolang>Fermer</button>
    <button class="btn lspd" id="lsmok" data-nolang disabled>Préparer les fichiers</button></div>
</div></div>
<div class="ov" id="arrov"><div class="mod" role="dialog" aria-modal="true" aria-labelledby="arr-t">
  <div class="mh"><h2 id="arr-t" data-nolang>Envoyer les nouveaux arrivages</h2><button class="x" id="arr-x" aria-label="Fermer">&times;</button></div>
  <div class="mb" id="arr-corps" data-nolang></div>
  <div class="mf"><span class="msg" id="arr-msg" data-nolang></span><button class="btn" id="arr-ferme" data-nolang>Fermer</button></div>
</div></div>
<div class="ov" id="lsov"><div class="mod" role="dialog" aria-modal="true" aria-labelledby="lst" style="max-width:720px">
  <div class="mh"><h2 id="lst">Nouvelles références pour Lightspeed</h2><button class="x" id="lsx" aria-label="Fermer">&times;</button></div>
  <div class="mb">
    <p class="hint">Les parfums de l'ERP que la caisse ne connaît pas encore, dans le format d'import des produits de Lightspeed : nom, code-barres, marque, prix d'achat, prix détail, quantité.</p>
    <p class="hint">Dans Lightspeed : Catalog → Products → Import, puis choisir ce fichier. Le prix de gros n'y va pas : Lightspeed le range dans un barème de prix à part.</p>
    <div id="lsres"></div>
  </div>
  <div class="mf"><span class="msg" id="lsmsg"></span>
    <button class="btn" id="lsannul">Fermer</button>
    <button class="btn pri" id="lsok" disabled>Télécharger le fichier</button></div>
</div></div>
<div class="ov" id="ov"><div class="mod" role="dialog" aria-modal="true" aria-labelledby="mt">
  <div class="mh"><h2 id="mt">Nouvel article</h2><button class="x" id="mx" aria-label="Fermer">&times;</button></div>
  <div class="tabs">
    <button class="tab on" data-p="man">Saisie manuelle</button>
    <button class="tab" data-p="col">Coller des lignes de facture</button>
    <button class="tab" data-p="fic">Importer un fichier</button>
  </div>
  <div class="mb">

    <div class="pane on" id="p-man">
      <p class="hint">Seuls <b>la marque</b> et <b>le nom</b> sont obligatoires. Tout le reste peut rester vide :
      l'article sera créé et marqué <b>à compléter</b>, visible dans le filtre correspondant.</p>
      <div class="fg">
        <div class="fld"><label>Marque <b>*</b></label><input id="f-marque" list="l-marques" autocomplete="off">
          <span class="fhint">Nouvelle marque : tape son nom, elle est créée avec l'article.</span></div>
        <div class="fld"><label>Nom du parfum <b>*</b></label><input id="f-nom" autocomplete="off"></div>
        <div class="fld"><label>Code-barres</label><input id="f-bc" inputmode="numeric" autocomplete="off"></div>
        <div class="fld"><label>Contenance (oz)</label><input id="f-ml" inputmode="decimal" autocomplete="off"></div>
        <div class="fld"><label>Type</label><input id="f-type" list="l-types" placeholder="EDP, EDT…" autocomplete="off"></div>
        <div class="fld"><label>Genre</label><select id="f-genre">
          <option value="">— inconnu —</option><option value="M">Homme</option>
          <option value="W">Femme</option><option value="U">Unisexe</option><option value="K">Enfant</option></select></div>
        <div class="fld"><label>Quantité en stock</label><input id="f-qte" inputmode="numeric" placeholder="0"></div>
        <div class="fld"><label>Prix d'achat</label><input id="f-pa" inputmode="decimal"></div>
        <div class="fld"><label>Prix retail</label><input id="f-pvr" inputmode="decimal"></div>
        <div class="fld"><label>Prix de gros</label><input id="f-pvw" inputmode="decimal"></div>
      </div>
      <datalist id="l-marques"></datalist><datalist id="l-types"></datalist>
    </div>

    <div class="pane" id="p-col">
      <p class="hint">Colle ici les lignes d'une facture fournisseur, telles quelles.
      Je reconnais le format habituel : <code>quantité · désignation · marque · code-barres · stock · prix</code>,
      séparé par des tabulations ou des points-virgules. La contenance, le type et le genre sont déduits
      de la désignation quand ils y figurent.</p>
      <textarea id="ta" spellcheck="false" placeholder="12&#9;LATTAFA KHAMRAH 3.4 EDP U (122401)&#9;LATTAFA&#9;6291108737194&#9;999&#9;17"></textarea>
      <div style="display:flex;gap:9px"><button class="btn" id="an">Analyser les lignes</button></div>
      <div class="prev" id="pv" style="display:none"></div>
    </div>

    <div class="pane" id="p-fic">
      <p class="hint">Choisis un fichier <code>.csv</code> exporté depuis Excel ou depuis le site.
      La première ligne doit contenir les intitulés de colonnes — je reconnais
      <code>code-barres</code>, <code>nom</code>, <code>marque</code>, <code>contenance</code>,
      <code>type</code>, <code>genre</code>, <code>quantité</code>, <code>prix achat</code>,
      <code>retail</code>, <code>gros</code>, quelle que soit leur casse ou leur ordre.</p>
      <input type="file" id="fi" accept="__ACCEPT_TAB__" style="font-size:13.5px">
      <p class="hint"><b>Une facture en PDF ou en photo ne peut pas être lue par cette page.</b>
      Envoie-la-moi dans la conversation : je la dépouille et je te rends les lignes prêtes à coller
      dans l'onglet précédent.</p>
      <div class="prev" id="pv2" style="display:none"></div>
    </div>

  </div>
  <div class="mf">
    <span class="msg" id="msg"></span>
    <button class="btn" id="mc">Annuler</button>
    <button class="btn pri" id="mo">Ajouter</button>
  </div>
</div></div>

<div class="dov" id="dov"></div>
<aside class="dr" id="dr" role="dialog" aria-modal="true" aria-labelledby="dnom">
  <div class="dh">
    <div class="id"><div class="b" id="dmarque"></div><h2 id="dnom"></h2></div>
    <div class="dnav">
      <button id="dprev" aria-label="Précédent" title="Précédent (←)">‹</button>
      <button id="dnext" aria-label="Suivant" title="Suivant (→)">›</button>
      <button class="dx" id="ddx" aria-label="Fermer" title="Fermer (Échap)">&times;</button>
    </div>
  </div>
  <div class="db" id="ddb"></div>
  <div class="df">
    <button class="btn" id="dmod" hidden>Modifier le parfum</button>
    <button class="btn dsup" id="dret" hidden>Retirer du catalogue</button>
    <button class="btn dsup" id="dsup" hidden>Supprimer ce produit</button>
    <span class="st" id="dst"></span>
    <button class="btn" id="dann">Annuler</button>
    <button class="btn pri" id="dok">Enregistrer</button>
  </div>
</aside>

<div class="grid" id="grid"></div>
<div class="lstw" id="lstw" style="display:none"></div>
<div class="empty" id="empty" style="display:none">Aucun produit ne correspond à ces filtres.</div>
<button id="more" style="display:none">Afficher plus</button>

<div class="legend">
<span class="k">*</span> <b>Prix retail repris de perfumestrade.com</b>, absent du fichier d'inventaire — 936 références, dont 539 en stock. À valider avant toute utilisation commerciale.<br>
<span class="k bad">*</span> <b>Prix du site inférieur ou égal au prix d'achat</b> — 27 références, dont 21 en stock, affichées en rouge. Ne pas les reprendre tels quels.<br>
Les prix sans astérisque viennent du fichier d'inventaire. Les prix de gros ne viennent jamais du site.<br><br>
<b>Anomalies de prix</b> — 731 références sur 1 892 en portent au moins une, soit 434 572 $ de capital.
Le menu « Prix » les isole. Bordure rouge : la référence perd de l'argent ou n'a pas de prix de vente.
Bordure orange : marge douteuse, à contrôler.
</div>

<footer><span>__PHOTOS__ références illustrées sur __TOTAL__ · photos locales normalisées en 800 × 800</span>
<span class="mono">RUBRIQUE CATALOGUE</span></footer></div></div></div>

<script>__VOCAB__</script>
<script src="donnees/langue.js?v=__VER__"></script>
<script>
/* le menu réglé et la langue de l'écran, AVANT le code de la page : rien ne saute, rien n'est vu dans une autre langue */
__IDENT_TOT__
__MENU__
__LANGUE__
</script>
<script src="donnees/produits.js?v=__VER__"></script>__GARDE__
<script src="donnees/histgros.js?v=__VER__"></script>
<script>
__FUSION__
__COMPTES__
__IDENT__
__FILE_AUTO__
__SAUVE__
__LIRE__
__SORTIE__
const MARCHE_INIT=__MARCHE__;
const FACTURE_INIT=__FACTURE__;
const FRN_INIT=__FRNINIT__;
const DATE_INV='2026-09-02';
const P=__DATA__.map(r=>({bc:r[0],nomSrc:r[1],marque:r[2],ml:r[3],type:r[4],genre:r[5],
 qte:r[6],pvr:r[7],pvw:r[8],img:r[9],src:r[10],an:r[11],pa:r[12],nom:r[13],
 verif:r[14],cle:r[15],rang:r[16],partCap:r[17],asin:r[18]||''}));
const G={M:'Homme',W:'Femme',U:'Unisexe',K:'Enfant'};
const AN={1:['Gros à perte','c'],2:['Retail à perte','c'],3:['Gros > retail','c'],
 4:['Marge wholesale < 10 %','w'],5:['Marge wholesale > 60 %','w'],6:['Retail > 3x achat','w'],
 7:['Pas de prix gros','w'],8:['Pas de prix retail','c'],9:['Gros = retail','w']};
/* ordre d'affichage des alertes : le meme que les colonnes — retail d'abord, puis gros, puis les deux */
const AN_ORDRE=[2,8,6,1,7,4,5,3,9];
const triAn=a=>a.slice().sort((x,y)=>AN_ORDRE.indexOf(x)-AN_ORDRE.indexOf(y));
const VER_URL='__VER__';
const $=i=>document.getElementById(i);
const PAGE=120; let shown=PAGE, cur=[];
/* la barre du haut est figee ; l'en-tete du tableau se fige juste en dessous, a sa hauteur reelle */
function mesureBarre(){ const b=document.querySelector('.bar'); if(b) document.documentElement.style.setProperty('--barh',(b.offsetHeight)+'px'); }
window.addEventListener('resize',mesureBarre); window.addEventListener('load',mesureBarre);
if(document.fonts&&document.fonts.ready) document.fonts.ready.then(mesureBarre);

/* ============ ARTICLES AJOUTES A LA MAIN ============ */
const KADD='articles-ajoutes-v1';
/* Photos choisies à la main dans la fiche (Igal, 17 oct. 2026) : { identifiant du produit : image }.
   Elles passent avant la photo du site et celle du fichier. Elles restent dans l'outil : rien n'est envoyé aux sites. */
const KPHO='photos-perso-v1';
let PHO=lit(KPHO,{}); if(!PHO||typeof PHO!=='object'||Array.isArray(PHO)) PHO=base(KPHO,{});
let AJ=lit(KADD,[]); if(!Array.isArray(AJ)) AJ=base(KADD,[]);
const sauveAJ=()=>ecrit(KADD,AJ);

const CHAMPS=['bc','nom','marque','ml','type','genre','qte','pvr','pvw','pa'];
function manque(p){
  const m=[];
  if(!p.bc) m.push('code-barres'); if(!p.ml) m.push('contenance');
  if(!p.type) m.push('type'); if(!p.genre) m.push('genre');
  if(p.pa==null) m.push("prix d'achat"); if(p.pvw==null) m.push('prix de gros');
  if(p.pvr==null) m.push('prix retail');
  return m;
}
function normAJ(o){
  return {bc:(o.bc||'').trim(), nomSrc:o.nom||'', nom:o.nom||'', marque:o.marque||'',
    ml:(o.ml||'').toString().trim(), type:(o.type||'').toUpperCase().trim(),
    genre:(o.genre||'').toUpperCase().trim(),
    qte:o.qte==null||o.qte===''?0:+o.qte,
    pvr:o.pvr==null||o.pvr===''?null:+o.pvr,
    pvw:o.pvw==null||o.pvw===''?null:+o.pvw,
    pa:o.pa==null||o.pa===''?null:+o.pa,
    img:'', src:0, an:[], neuf:true};
}
/* Stock importé d'une source externe (Google Sheet). Il s'applique AVANT
   les modifications faites à la main dans la fiche, qui restent prioritaires. */
const KEXT='stock-externe-v1';
let EXT={q:{},date:null,src:''};
try{ const r=JSON.parse(localStorage.getItem(KEXT)||'null'); if(r&&r.q) EXT=r; }catch(e){}
base(KEXT,EXT);
const sauveEXT=()=>ecrit(KEXT,EXT);
/* Les ecarts releves dans le Google Sheet du 3 septembre sont installes une fois :
   quantites dans le stock externe, prix dans les fiches, et une ligne au journal.
   Une mise a jour ulterieure depuis le Sheet (bouton « Mettre a jour le stock ») les remplace. */
/* quand un fichier installe des donnees apres coup, on releve le repere de depart d'autant :
   ces donnees ne sont pas des saisies a la main et ne doivent pas declencher le rappel de sauvegarde */
function bumpBase(k,n){ try{ const K='repere-installation-v1'; const b=JSON.parse(localStorage.getItem(K)||'null'); if(!b||!n) return;
  b[k]=(b[k]||0)+n; localStorage.setItem(K,JSON.stringify(b)); }catch(e){} }
const SHEET_INIT=__SHEET__;
(function(){
  const K='sheet-installe-2026-09-03';
  try{ if(localStorage.getItem(K)) return; }catch(e){ return; }
  const dejaSheet = EXT.date && new Date(EXT.date) > new Date(SHEET_INIT.date);
  if(!dejaSheet){ let n=0; Object.entries(SHEET_INIT.q).forEach(([bc,q])=>{ if(EXT.q[bc]===undefined) n++; EXT.q[bc]=q; }); EXT.date=EXT.date||SHEET_INIT.date; EXT.src=EXT.src||SHEET_INIT.src; sauveEXT(); bumpBase('stock-externe-v1',n); }
  window.__sheetInit={n:dejaSheet?0:Object.keys(SHEET_INIT.q).length};
  try{ localStorage.setItem(K,'1'); }catch(e){}
})();
function externe(p){
  const q=EXT.q[p.bc];
  if(q===undefined||q===null||q===p.qte) return p;
  const o=Object.assign({},p,{qte:q}); o.an=calcAn(o); o.ext=true; return o;
}
/* La photo : celle du site quand il en a une. Le cockpit relit chaque heure les
   deux boutiques (site-stock-v1) et range la première photo de chaque fiche ; le
   fichier de départ, lui, date de septembre — des parfums ajoutés ou re-photographiés
   depuis sur le site restaient « sans photo » ici. Le détail d'abord, le gros ensuite,
   avec ou sans les zéros du début du code-barres. */
let _IMGS=null;
function imgsSite(){
  if(_IMGS) return _IMGS; _IMGS={};
  let S={}; try{ S=lit('site-stock-v1',{})||{}; }catch(e){ S={}; }
  if(!S||typeof S!=='object') return _IMGS;
  /* le cockpit range l'adresse sans le site devant (« /wp-content/… ») : on la recolle */
  const B=(S._base&&typeof S._base==='object')?S._base:{}, abs=(u,c)=>u&&u.charAt(0)==='/'?((B[c]||(c==='g'?'https://wholesale.perfumestrade.com':'https://perfumestrade.com'))+u):u;
  Object.keys(S).forEach(k=>{ if(k.startsWith('_')) return; const e=S[k]||{};
    const u=(e.d&&e.d.img?abs(e.d.img,'d'):'')||(e.g&&e.g.img?abs(e.g.img,'g'):''); if(u) _IMGS[k.replace(/^0+/,'')]=u; });
  /* 22 oct. 2026 (Igal : « s'ils sont sur Perfume City, il n'y a aucune raison qu'on n'ait pas la photo ») : la photo de la
     boutique Perfume City (relue chaque heure avec ses prix, shopify-pc-prix-v1) sert quand aucun des deux sites n'en a */
  try{ const P=lit('shopify-pc-prix-v1',null); if(P&&typeof P==='object') Object.keys(P).forEach(k=>{ if(k.startsWith('_')) return; const r=P[k];
    if(Array.isArray(r)&&r[6]&&/^https?:\/\//.test(r[6])){ const kk=k.replace(/^0+/,''); if(!_IMGS[kk]) _IMGS[kk]=r[6]; } }); }catch(e){}
  return _IMGS;
}
try{ window.addEventListener('ck-maj',()=>{ _IMGS=null; }); }catch(e){}
function avecPhotoSite(p){
  if(!p||!p.bc) return p;
  const I=imgsSite(), b=String(p.bc);
  let u=I[b.replace(/^0+/,'')];
  /* deux codes collés dans la même case du fichier :
     on essaie chacun des deux */
  if(!u&&/^\d{16,28}$/.test(b)) for(let i=8;i<=b.length-8&&!u;i++){
    u=I[b.slice(0,i).replace(/^0+/,'')]&&/^\d{11,14}$/.test(b.slice(0,i))?I[b.slice(0,i).replace(/^0+/,'')]
     :(/^\d{11,14}$/.test(b.slice(i))?I[b.slice(i).replace(/^0+/,'')]:undefined); }
  if(!u||u===p.img) return p;
  const o=Object.assign({},p,{img:u,imgSite:true}); o.an=calcAn(o); return o;
}
function avecPhotoPerso(p){
  const u=p&&PHO[p.id]; if(!u) return p;
  const o=Object.assign({},p,{img:u,imgPerso:true}); o.an=calcAn(o); return o;
}
function tousLesArticles(){
  return AJ.map((o,i)=>{const x=normAJ(o); x.id=o.id||('a'+i); x.an=calcAn(x); return avecPhotoPerso(avecPhotoSite(applique(x)));})
           .concat(P.map(p=>avecPhotoPerso(avecPhotoSite(applique(externe(p))))));
}

/* Sam, 3 oct. 2026 : « comment je crée une nouvelle marque dans le catalogue ? » — en tapant
   son nom dans « Marque » d'un nouvel article. Mais la liste « Toutes les marques » ne lisait
   que le fichier de départ : une marque créée dans l'ERP n'y apparaissait jamais, comme si
   elle n'existait pas. Elle lit maintenant toutes les fiches, et se refait après un ajout. */
function remplitMarques(){
  const sel=$('fb'); if(!sel) return; const v=sel.value;
  const ms=[...new Set(tousLesArticles().map(p=>String(p.marque||'').trim()).filter(Boolean))].sort((a,b)=>a.localeCompare(b,'fr'));
  sel.innerHTML='<option value="">Toutes les marques</option>'+ms.map(b=>`<option value="${esc(b)}">${esc(b)}</option>`).join('');
  if(v&&ms.includes(v)) sel.value=v;
}
[...new Set(P.map(p=>p.type).filter(Boolean))].sort().forEach(t=>
 $('ft').insertAdjacentHTML('beforeend',`<option value="${t}">${t}</option>`));

// 1) photo locale  2) photo du site  3) message
/* Igal, 12 oct. : ça se fige au 5e clic de tri. Chaque tri redessine ~120 vignettes ; 119 sur 130 n'ont
   PAS de photo locale : chaque redessin renvoyait ~120 requêtes qui échouent (404) puis ~120 vers le site.
   Cinq clics = 1 200 requêtes en file. On retient donc les photos locales absentes : elles partent
   directement vers l'adresse du site (déjà en cache du navigateur), sans repasser par le 404. */
const PHOTO_KO=new Set();
const phSrc=p=>p.imgPerso?p.img:(PHOTO_KO.has(p.bc)&&p.img?p.img:`photos/${p.bc}.webp`);
function secours(img){
  const far=img.dataset.far;
  if(far && img.src.indexOf('photos/')>-1){ try{ const m=img.src.match(/photos\/([^\/?#]+)\.webp/); if(m) PHOTO_KO.add(decodeURIComponent(m[1])); }catch(e){} img.src=far; return; }
  const d=document.createElement('div'); d.innerHTML=`<div class="miss"><svg viewBox="0 0 40 64" fill="none" aria-hidden="true"><rect x="14.5" y="2" width="11" height="9" rx="1.5" stroke="currentColor" stroke-width="2.4"/><path d="M11 20a6 6 0 016-6h6a6 6 0 016 6v34a6 6 0 01-6 6H17a6 6 0 01-6-6V20z" stroke="currentColor" stroke-width="2.4"/></svg><span>sans photo</span></div>`;
  img.replaceWith(d.firstElementChild);
}
/* Le dollar (Igal, 30 sept. 2026 : « le dollar est décalé ») : une espace INSÉCABLE entre le
   montant et le $, pour que le $ ne parte jamais seul à la ligne suivante. Le format reste
   « 3 837,50 $ » : le dictionnaire de traduction reconnaît les phrases sur ce modèle. */
const _usd=(v,d)=>{ if(v==null) return '—'; const n=Number(v); 
  return n.toLocaleString('fr-FR',{minimumFractionDigits:d,maximumFractionDigits:d})+' $'; };
const money=v=>v==null?null:_usd(v,2);
const esc=s=>String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));

function card(p){
 const meta=[p.ml?`<b>${esc(p.ml)}</b> oz`:'',esc(p.type),G[p.genre]||''].filter(Boolean).join(' · ');
 const ph=p.img
  ?`<img src="${phSrc(p)}" data-far="${p.imgPerso?'':p.img}" alt="${esc(p.marque)} ${esc(p.nom)}"
     loading="lazy" decoding="async" onerror="secours(this)">`
  :`<div class="miss"><svg viewBox="0 0 40 64" fill="none" aria-hidden="true"><rect x="14.5" y="2" width="11" height="9" rx="1.5" stroke="currentColor" stroke-width="2.4"/><path d="M11 20a6 6 0 016-6h6a6 6 0 016 6v34a6 6 0 01-6 6H17a6 6 0 01-6-6V20z" stroke="currentColor" stroke-width="2.4"/></svg><span>sans photo</span></div>`;
 const CLIENT=document.body.classList.contains('client');
 const mq=manque(p);
 const chipn=p.neuf?'<span class="chipn">nouveau</span>':'';
 const chiptodo=(!CLIENT&&mq.length)?`<span class="fl todo" title="${mq.join(', ')}">${mq.length} champ${mq.length>1?'s':''} à compléter</span>`:'';
 const flags=(!CLIENT&&p.an.length)
  ?`<div class="flags">${p.an.map(a=>`<span class="fl ${AN[a][1]}">${AN[a][0]}</span>`).join('')}</div>`:'';
 const star=p.src===1?'<span class="ast">*</span>':p.src===2?'<span class="ast bad">*</span>':'';
 const val=(v,cls,extra='')=>v==null
   ?`<dd class="${cls} na">à définir</dd>`
   :`<dd class="${cls}${extra}">${money(v)}${cls==='vr'?star:''}</dd>`;
 const nf=(MOD[p.id]&&MOD[p.id].frn)?MOD[p.id].frn.filter(f=>f.n).length:0;
 const chipf=(!CLIENT&&nf>1)?`<span class="fl todo">${nf} fournisseurs</span>`:'';
 const cd=CLIENT?null:pastilleDiff(p), chipd=cd?`<span class="fl ${cd.c}">${esc(cd.t)}</span>`:'';
 return `<article class="card${p.neuf?' neuf':''}${CLIENT?'':(p.an.some(a=>[1,2,3,8].includes(a))?' alert':p.an.length?' warn':'')}" data-id="${p.id}" tabindex="0" role="button" aria-label="Ouvrir la fiche">
  <div class="ph">${ph}${chipn}<span class="qty${p.qte===0?' out':(SEUIL>0&&p.qte<SEUIL)?' low':''}">${p.qte===0?'historique':p.qte}</span></div>
  <div class="body">
    <div class="brand">${esc(p.marque)}</div>
    <div class="nm">${esc(p.nom)}</div>
    <div class="meta">${meta||'&nbsp;'}${badgeAmazon(p)}</div>
    ${CLIENT?'':`<div class="dfrow">${logosDiff(p)}</div>`}
    ${(chipd||chiptodo||chipf||flags)?`<div class="flags">${chipd}${chiptodo}${chipf}${flags?flags.replace(/<\/?div[^>]*>/g,''):''}</div>`:''}
    <dl class="led">
      ${CLIENT?'':`<dt>Achat</dt>${val(p.pa,'vp')}`}
      <dt>Retail</dt>${val(p.pvr,'vr',p.src===2?' bad':'')}
      <dt>Gros</dt>${val(p.pvw,'vw')}
    </dl>
    ${CLIENT?'':`<div class="bcline">${p.bc}</div>`}
  </div></article>`;
}


/* ================= TRI PAR COLONNE =================
   Une valeur absente n'est ni la plus petite ni la plus grande : elle part
   toujours en fin de liste, dans les deux sens. Sinon "le moins cher" ferait
   remonter les produits sans prix. */
const KTRI='tri-colonne-v1';
let TRI=null; try{ TRI=JSON.parse(localStorage.getItem(KTRI)||'null'); }catch(e){ TRI=null; }
const sauveTRI=()=>{ try{ TRI?localStorage.setItem(KTRI,JSON.stringify(TRI)):localStorage.removeItem(KTRI); }catch(e){} };

const marge=(p,v)=>(v!=null&&p.pa!=null&&v>0)?((v-p.pa)/v*100):null;
/* ---------- Le prix d'Amazon, en face du mien ----------
   Les relevés vivent dans « marche-v1 », le même magasin que la fiche produit
   remplit avec « Saisir un relevé ». Un seul endroit : si un jour une source
   automatique remplit ce magasin tous les matins, la colonne se met à jour
   toute seule et la fiche aussi, sans une ligne de plus.

   Ce qui est affiché est l'ÉCART, pas le prix d'Amazon tout seul. « Amazon est
   à 103,89 $ » ne dit rien tant qu'on ne sait pas où on est, soi. */
function azReleve(p){ const m=MAR[p.id]; return (m && m.amz!=null) ? m : null; }
function azEcart(p){
  const m=azReleve(p);
  if(!m || p.pvr==null || !(m.amz>0)) return null;
  return {m, d:p.pvr-m.amz, pc:(p.pvr-m.amz)/m.amz*100};
}
/* L'âge du relevé compte autant que le relevé : un prix Amazon de trois
   semaines n'est pas une information, c'est un souvenir. */
function azJours(m){
  if(!m || !m.le) return null;
  const t=Date.parse(m.le); if(isNaN(t)) return null;
  return Math.floor((Date.now()-t)/86400000);
}
function azCell(p){
  const m=MAR[p.id];
  if(!m) return p.asin
    ? `<span class="lazv" title="Cette référence a une fiche Amazon (${esc(p.asin)}) mais son prix n'a jamais été relevé.">jamais relevé</span>`
    : `<span class="lazv" title="Aucun ASIN dans l'inventaire : impossible de savoir quelle fiche Amazon correspond à ce parfum.">pas d'ASIN</span>`;
  if(m.amz==null)
    return `<span class="lazv" title="Relevé fait, mais le parfum n'était pas disponible sur Amazon ce jour-là.">indisponible</span>`;

  const j=azJours(m), vieux=j!=null&&j>14;
  const e=azEcart(p);
  const perte = p.pa!=null && m.amz < p.pa;
  const ec = e
    ? `<span class="lazd${perte?' perte':''}">${e.d>0?'+':e.d<0?'−':''}${money(Math.abs(e.d)).replace(/^−/,'')} ${e.d>=0?'au-dessus':'en dessous'}</span>`
    : (p.pvr==null ? `<span class="lazd">pas de prix retail à comparer</span>` : '');
  const age = j==null ? ''
    : `<span class="lazage${j>30?' perime':''}">${j===0?"relevé aujourd'hui":j===1?'relevé hier':'relevé il y a '+j+' jours'}</span>`;
  const t = perte
    ? "Amazon vend moins cher que ce que ce parfum t'a coûté : à ce prix-là tu ne peux pas t'aligner."
    : (e ? `Ton prix retail ${money(p.pvr)} face aux ${money(m.amz)} d'Amazon${m.vend?' (vendu par '+m.vend+')':''}.` : '');
  return `<span class="laz${vieux?' vieux':''}" title="${esc(t)}">${money(m.amz)}</span>${ec}${age}`;
}
/* L'adresse exacte de la fiche Amazon quand on a l'ASIN — sinon une recherche,
   qui tombe parfois à côté. C'est tout l'intérêt d'avoir remis l'ASIN dans les
   données : /dp/B08NSZ4GWG ouvre LA fiche, pas dix résultats approchants. */
/* « Vendu sur Amazon » (Igal, 11 oct. 2026) : un ASIN sur la fiche = le parfum est en annonce chez Sam
   (sa feuille porte l'ASIN de ce qu'il vend là-bas) ; une vente Amazon enregistrée le confirme. */
let _AZV=null;
/* « Sans prix sur le site » (12 oct. 2026, Igal : voir les produits où il manque le prix, wholesale ou retail) :
   fiche retirée de la vente faute de prix, ou fiche en ligne dont le prix du site est vide. */
/* DIFFUSION (Igal, 17 oct. 2026) : ce parfum est-il EN VENTE sur chacun des trois canaux ?
   perfumestrade.com et le site de gros (WooCommerce) : la fiche existe sur le site ; une fiche retirée (brouillon) ne compte pas.
   Perfume City (Shopify) : le produit existe ET il est actif ; un brouillon ne compte pas.
   « na » = on ne peut pas le dire : pas de code-barres, relevé du canal jamais lu, ou canal coupé pour ce parfum
   (« ne pas vendre ici » : ce n'est pas un manque, c'est un choix). Un « na » n'est jamais compté comme « pas diffusé ». */
const CAN_DIFF=[['site','perfumestrade.com','perfumestrade.com'],['sitegros','le site de gros','wholesale.perfumestrade.com'],['perfumecity','Perfume City','Perfume City']];
let DIFF_S=null, DIFF_OK={site:false,sitegros:false,perfumecity:false};
function majDiff(){
  let S=null; try{ S=lit('shopify-pc-prix-v1',null); }catch(e){ S=null; }
  DIFF_S=(S&&typeof S==='object')?S:null;
  const cles=o=>o&&typeof o==='object'?Object.keys(o).filter(k=>k[0]!=='_'):[];
  const sw=cles(SITE);
  DIFF_OK={site:sw.some(k=>SITE[k]&&SITE[k].d), sitegros:sw.some(k=>SITE[k]&&SITE[k].g), perfumecity:!!DIFF_S&&cles(DIFF_S).length>0};
  /* les compteurs, sur ce qui est en stock : c'est ce qu'on veut diffuser */
  const n={any:0,site:0,sitegros:0,perfumecity:0,all:0};
  const ARTS=tousLesArticles();
  pubVerifie(ARTS);
  ARTS.forEach(p=>{ if(!(p.qte>0)) return;
    const st=CAN_DIFF.map(c=>statutDiff(p,c[0]));
    st.forEach((x,i)=>{ if(x==='non') n[CAN_DIFF[i][0]]++; });
    if(st.includes('non')) n.any++; else if(st.includes('oui')) n.all++; });
  const lib={'':'Diffusion : toute',any:'Pas diffusé sur un des trois',site:'Pas sur perfumestrade.com',sitegros:'Pas sur le site de gros',perfumecity:'Pas sur Perfume City',all:'Diffusé sur les trois'};
  const sel=document.getElementById('fd'); if(!sel) return;
  Array.from(sel.options).forEach(o=>{ const v=o.value; if(v==='') return;
    const sans=(DIFF_OK[v]===false&&CAN_DIFF.some(c=>c[0]===v));
    o.disabled=sans; o.textContent=lib[v]+(sans?' (relevé pas encore lu)':' ('+Number(n[v]).toLocaleString('fr-FR')+')'); });
}
function statutDiff(p,id){
  if(horsCanal(p,id)||!p.bc||!DIFF_OK[id]) return 'na';
  const cote=COTE_SITE[id];
  if(cote){
    const k=siteCle(p); if(!k) return 'non';          /* le relevé est lu et ce code-barres n'y figure pas : le parfum n'est pas sur ce site */
    const e=SITE[k]; return e&&e[cote]?'oui':'non';
  }
  if(id==='perfumecity'){
    const S=DIFF_S; if(!S) return 'na';
    const s0=x=>String(x||'').replace(/[^0-9A-Za-z]/g,'').replace(/^0+/,'');
    const ks=[p.bc].concat(String(p.bcs||'').split(/[\s,;]+/)).map(s0).filter(Boolean);
    for(const k of ks){ const e=S[k]; if(Array.isArray(e)&&e[2]>0) return e[4]===1?'oui':'non'; }   /* trouvé mais brouillon : pas diffusé */
    return ks.some(k=>(S._amb||[]).includes(k))?'oui':'non';
  }
  return 'na';
}
function diffOk(p,f){
  const st=CAN_DIFF.map(c=>statutDiff(p,c[0]));
  if(f==='any') return st.includes('non');
  if(f==='all') return !st.includes('non')&&st.includes('oui');
  const i=CAN_DIFF.findIndex(c=>c[0]===f); return i>=0&&st[i]==='non';
}
/* trois pastilles par parfum (Igal, 17 oct. 2026 : « un petit logo barré ou visible sur les lignes du catalogue, pour les voir visuellement et rapidement »).
   En couleur = en vente ; grisée et BARRÉE = pas diffusé ; très pâle = on ne sait pas (pas de code-barres, relevé pas lu, canal coupé).
   Des pastilles plutôt que les vrais logos : le logo du site est un titre long, illisible à cette taille, et la colonne du nom est déjà étroite. */
function logosDiff(p){
  const T={oui:'en vente',non:'PAS en vente',na:'inconnu'};
  const un=(id,nom,court)=>{ const st=statutDiff(p,id);
    const raison=st==='na'?(horsCanal(p,id)?' (canal coupé pour ce parfum)':!p.bc?' (pas de code-barres)':' (relevé pas encore lu)'):'';
    return `<span class="dfi ${st} d-${id}" title="${esc(nom)} : ${T[st]}${raison}">${court}</span>`; };
  /* Igal, 17 oct. 2026 : « les pastilles gros et PC, j'aime pas, mets le nom des sites directement » */
  return `<span class="dif" data-nolang>${CAN_DIFF.map(c=>un(c[0],c[2],c[2])).join('')}</span>`;
}
/* la pastille « pas sur : … » sur chaque ligne, seulement quand on filtre sur la diffusion */
function pastilleDiff(p){
  /* 17 oct. 2026 : les pastilles portent maintenant le NOM des sites, barrées là où le parfum manque : la puce « pas sur : … » disait
     la même chose en plus long, et débordait de la colonne des alertes. Elle n'existe plus. */
  return null;
}
/* ---------------------------------------------------------------------------
   METTRE EN LIGNE (Igal, 17 oct. 2026 : « quand je rentre une nouvelle référence, est-ce que j'ai moyen de la diffuser
   automatiquement sur les canaux de vente » puis « fais tout »). L'ERP décide QUOI envoyer et à QUEL PRIX, le cockpit écrit.
   Garde-fous côté ERP : seul le dirigeant ; seulement ce qui est EN STOCK ; jamais sans prix, ni en dessous du prix d'achat ;
   rien de ce qui existe déjà (même en brouillon) ; 200 parfums au plus par passage, envoyés 20 par 20 ; tout en brouillon
   par défaut (Perfume City : toujours). Le prix envoyé est celui que l'ERP montre pour ce canal, en un seul prix (pas de promo).
--------------------------------------------------------------------------- */
const MEL_MAX=200, MEL_LOT=20, GEN_EN={F:'Women',M:'Men',U:'Unisex',K:'Kids'};
const MEL_CANAL={site:{nom:'perfumestrade.com'},sitegros:{nom:'wholesale.perfumestrade.com'},perfumecity:{nom:'Perfume City'}};
function melNom(p){
  const n=String(p.nom||''), t=[(p.marque||'')+' '+n];
  if(p.ml&&!/oz/i.test(n)) t.push(p.ml+' oz');
  if(p.type&&n.toUpperCase().indexOf(String(p.type).toUpperCase())<0) t.push(p.type);
  if(p.genre&&GEN_EN[p.genre]&&!/women|men|unisex|kids/i.test(n)) t.push(GEN_EN[p.genre]);
  return t.join(' ').replace(/\s+/g,' ').trim();
}
/* un produit existe déjà sur ce canal (en vente OU en brouillon) : on ne le recrée jamais */
function existeCanal(p,id){
  const cote=COTE_SITE[id];
  if(cote) return !!retireCote(p,cote)||statutDiff(p,id)==='oui';
  const S=DIFF_S; if(!S) return false;
  const s0=x=>String(x||'').replace(/[^0-9A-Za-z]/g,'').replace(/^0+/,'');
  const ks=[p.bc].concat(String(p.bcs||'').split(/[\s,;]+/)).map(s0).filter(Boolean);
  return ks.some(k=>(Array.isArray(S[k])&&S[k][1])||(S._amb||[]).includes(k));
}
function candidatsMel(liste,ids){
  const res={}, skip={};
  ids.forEach(id=>{
    const c=(REG.canaux||[]).find(x=>x.id===id)||{id,base:id==='sitegros'?'pvw':'pvr',maj:0};
    res[id]=[]; skip[id]={sansPrix:0,perte:0,existe:0};
    liste.forEach(p=>{
      /* Perfume City : la fiche y est créée aussi, avec le stock de SON inventaire (0 tant que Sam ne lui a rien donné) */
      if(!(p.qte>0||(id==='perfumecity'&&qtePCde(p)>0))||!p.bc||statutDiff(p,id)!=='non') return;
      if(existeCanal(p,id)){ skip[id].existe++; return; }
      const v=prixCanal(p,c).v;
      if(!(v>0)){ skip[id].sansPrix++; return; }
      if(p.pa!=null&&v<p.pa){ skip[id].perte++; return; }
      res[id].push({p,v:r2(v)});
    });
  });
  return {res,skip};
}
const melOk=()=>{ try{ return peutPrixSite()&&typeof ckTok==='function'&&!!ckTok(); }catch(e){ return false; } };
function majMel(){
  const el=document.getElementById('mel'); if(!el) return;
  try{
    const fd=$('fd').value;
    if(!fd||fd==='all'||!melOk()){ el.hidden=true; return; }
    const ids=fd==='any'?['site','sitegros','perfumecity']:[fd];
    const {res,skip}=candidatsMel(cur,ids);
    const uniq=new Set(); ids.forEach(i=>res[i].forEach(x=>uniq.add(String(x.p.bc)))); const n=uniq.size;
    const sk=ids.reduce((a,i)=>({sansPrix:a.sansPrix+skip[i].sansPrix,perte:a.perte+skip[i].perte,existe:a.existe+skip[i].existe}),{sansPrix:0,perte:0,existe:0});
    const note=[sk.sansPrix?sk.sansPrix+" sans prix dans l'ERP":'',sk.perte?sk.perte+" sous le prix d'achat":'',sk.existe?sk.existe+' déjà en brouillon sur le site':''].filter(Boolean).join(' · ');
    el.hidden=false;
    el.innerHTML=n
      ?`<span><b>${nf(n)}</b> parfum${n>1?'s':''} en stock peu${n>1?'vent':'t'} être mis en ligne${ids.length>1?' — '+ids.map(i=>nf(res[i].length)+' sur '+MEL_CANAL[i].nom).join(' · '):' sur '+MEL_CANAL[ids[0]].nom}.${note?' <small>Écartés : '+note+'.</small>':''}</span><button class="btn" id="melb">Mettre en ligne…</button>`
      :`<span>Rien à mettre en ligne automatiquement dans cette liste.${note?' <small>Écartés : '+note+'.</small>':''}</span>`;
    const b=$('melb'); if(b) b.onclick=()=>ouvreMel(cur,ids);
  }catch(e){ el.hidden=true; }
}
function ouvreMel(liste,ids){
  if(!melOk()){ alert('Seul le dirigeant (rôle Patron), connecté au cockpit, peut mettre un parfum en ligne.'); return; }
  const {res,skip}=candidatsMel(liste,ids);
  const unique=liste.length===1?liste[0]:null;
  const lignes=ids.map(id=>{ const n=res[id].length, k=skip[id], nom=MEL_CANAL[id].nom;
    const ecart=[k.sansPrix?k.sansPrix+' sans prix':'',k.perte?k.perte+" sous le prix d'achat":'',k.existe?k.existe+' déjà là (brouillon)':''].filter(Boolean).join(' · ');
    /* 17 oct. 2026 (Sam : « il n'arrive pas à cocher ») : un parfum sans prix dans l'ERP donnait une case grisée sans un mot d'explication.
       Pour UN parfum on demande maintenant son prix, ici, et il est gardé dans la fiche ; pour une liste on explique pourquoi rien n'est proposé. */
    /* UN parfum : on montre ses prix, modifiables, avec un prix barré facultatif sur le site de détail et Perfume City
       (Igal, 17 oct. 2026 : « pas la possibilité de mettre un cross price »). Le prix de vente est gardé dans la fiche. */
    if(unique&&(n||k.sansPrix)){
      const st=x=>'style="margin-top:5px;width:110px;padding:5px 8px;border-radius:7px;border:1px solid var(--line,#ccc)"';
      const pv=n?String(res[id][0].v).replace('.',','):'';
      const barre=id!=='sitegros'?` &nbsp; <small style="display:inline">prix barré (facultatif)</small> <input type="text" inputmode="decimal" data-mb="${id}" placeholder="ex. 89,00" ${st()}> $`:'';
      return `<label class="ml"><input type="checkbox" data-mc="${id}" checked><span><b>${nom}</b>${n?'':" — ce parfum n'a pas de prix dans l'ERP."}<small>${n?'Prix de vente envoyé :':'Écris son prix de vente pour ce site :'}</small><input type="text" inputmode="decimal" data-mp="${id}" value="${pv}" placeholder="ex. 64,00" ${st()}> $${barre}<small>${n?'Tu peux le changer ici : il sera aussi gardé dans la fiche.':'Il sera aussi gardé dans la fiche du parfum.'}${barre?' Avec un prix barré, le client voit l\'ancien prix rayé et paie le prix de vente.':''}</small></span></label>`; }
    /* 31 oct. 2026 (Igal : « quand je mets Mettre en ligne, je peux pas cocher, ce n'est pas clair ») : 494 parfums EXISTENT sur le site de
       gros, retirés de la vente (brouillon) le 8 oct. faute de prix. La fenêtre disait « rien à créer » sans rien proposer. Pour UN parfum,
       elle propose maintenant de le REMETTRE EN VENTE, case cochée, avec son prix modifiable — même chemin que la case de la fiche. */
    if(unique&&!n&&k.existe&&COTE_SITE[id]&&retireCote(unique,COTE_SITE[id])&&unique.qte>0){
      const c=(REG.canaux||[]).find(x=>x.id===id)||{id,base:id==='sitegros'?'pvw':'pvr',maj:0};
      const v0=prixCanal(unique,c).v, pv=v0>0?String(r2(v0)).replace('.',','):'';
      const st='style="margin-top:5px;width:110px;padding:5px 8px;border-radius:7px;border:1px solid var(--line,#ccc)"';
      const barre=id!=='sitegros'?` &nbsp; <small style="display:inline">prix barré (facultatif)</small> <input type="text" inputmode="decimal" data-mb="${id}" placeholder="ex. 89,00" ${st}> $`:'';
      return `<label class="ml"><input type="checkbox" data-mc="${id}" data-remet="1" checked><span><b>${nom}</b> — ${L3('déjà sur ce site mais retiré de la vente : il sera REMIS EN VENTE','already on this site but withdrawn from sale: it will be PUT BACK ON SALE','ya está en este sitio pero retirado de la venta: se VOLVERÁ A PONER A LA VENTA')}<small>${L3('Prix de vente :','Selling price:','Precio de venta:')}</small><input type="text" inputmode="decimal" data-mp="${id}" value="${pv}" ${st}> $${barre}</span></label>`;
    }
    if(!n){ const pq=unique?(!(unique.qte>0)?"Ce parfum n'est pas en stock.":k.existe?'Il est déjà sur ce site (en brouillon) : utilise « Remettre en vente ».':k.perte?"Son prix est inférieur au prix d'achat : corrige-le dans la fiche.":''):''; 
      return `<div class="ml"><span><b>${nom}</b> — rien à créer.<small>${pq||ecart||'Aucun parfum de cette liste ne peut y être créé.'}</small></span></div>`; }
    return `<label class="ml"><input type="checkbox" data-mc="${id}" checked><span><b>${nom}</b> — ${nf(n)} à créer${n>MEL_MAX?' (200 maintenant, relance pour la suite)':''}${ecart?'<small>Écartés : '+ecart+'</small>':''}</span></label>`; }).join('');
  const aWoo=ids.some(i=>COTE_SITE[i]);
  const v=document.createElement('div'); v.className='mvoile';
  v.innerHTML=`<div class="mfen" role="dialog" aria-modal="true" data-nolang><h3>Mettre en ligne</h3>
    <div style="color:var(--ink-3,#777)">Seuls les parfums en stock, avec un prix dans l'ERP au-dessus du prix d'achat. Le prix envoyé est celui que l'ERP montre pour ce site.</div>
    ${lignes}
    <div class="ml"><span><span id="melou">Sur les sites perfumestrade.com</span> : <select id="melm"><option value="brouillon">créer en brouillon (je publie ensuite)</option><option value="publie">créer ET mettre en vente tout de suite</option></select><small id="melpc">Perfume City : toujours en brouillon, tu le publies dans Shopify.</small></span></div>
    <div id="melr"></div>
    <div class="mbtn"><button class="btn" id="mela">Annuler</button><button class="btn pri" id="melg">Mettre en ligne</button></div></div>`;
  document.body.appendChild(v);
  /* Perfume City : la mise en vente directe n'est possible que si Sam a donné le droit de poser le STOCK (write_inventory) —
     sinon un produit actif s'afficherait « épuisé ». On demande au cockpit, et on adapte la phrase. */
  window.__melPcStock=false;
  if(ids.includes('perfumecity')){ fetch(CK_URL+'/api/o/'+CK_ORG+'/shopify/droits',{headers:{Authorization:'Bearer '+ckTok()}}).then(r=>r.json()).then(j=>{
    window.__melPcStock=!!(j&&j.stock); const e=v.querySelector('#melpc'), o=v.querySelector('#melou'); if(!e) return;
    if(j&&j.stock){ e.textContent='Perfume City aussi : le stock de l\'ERP part avec la fiche.'; if(o) o.textContent=ids.some(i=>COTE_SITE[i])?'Sur les sites et Perfume City':'Chez Perfume City'; }
    else e.textContent='Perfume City : toujours en brouillon (Sam n\'a pas encore donné le droit write_inventory), tu le publies dans Shopify.'; }).catch(()=>{}); }
  let enCours=false, stop=false;
  const ferme=()=>{ if(enCours&&!confirm('Un envoi est en cours : arrêter après la fiche en cours ?')) return; stop=true; v.remove(); try{ render(); }catch(e){} };
  v.querySelector('#mela').onclick=ferme;
  v.querySelector('#melg').onclick=async()=>{
    const sel=ids.filter(id=>{ const c=v.querySelector('[data-mc="'+id+'"]'); return c&&c.checked&&!c.disabled; });
    if(!sel.length){ v.querySelector('#melr').innerHTML='<div class="mrep bad">Coche au moins un site.</div>'; return; }
    const mode=(v.querySelector('#melm')||{}).value||'brouillon';
    const msg=t=>{ v.querySelector('#melr').innerHTML='<div class="mrep bad">'+t+'</div>'; };
    const num=x=>{ const t=String(x==null?'':x).trim(); if(!t) return null; const n=Math.round(parseFloat(t.replace(',','.'))*100)/100; return Number.isFinite(n)?n:NaN; };
    for(const id of sel){ const inp=v.querySelector('[data-mp="'+id+'"]'); if(!inp) continue;
      const val=num(inp.value), ib=v.querySelector('[data-mb="'+id+'"]'), bar=ib?num(ib.value):null;
      if(!(val>0)){ msg('Écris un prix de vente pour '+MEL_CANAL[id].nom+'.'); return; }
      if(unique.pa!=null&&val<unique.pa){ msg('Ce prix est inférieur au prix d\'achat : on ne met pas un parfum en ligne à perte.'); return; }
      if(bar!=null&&!(bar>val)){ msg('Le prix barré doit être plus haut que le prix de vente ('+MEL_CANAL[id].nom+').'); return; }
      const avant=res[id][0]; res[id]=[{p:unique,v:val,barre:bar||null,saisi:!avant||Math.abs(avant.v-val)>0.004}]; }
    const remet=sel.filter(id=>{ const c=v.querySelector('[data-mc="'+id+'"]'); return c&&c.dataset.remet==='1'; });
    if(remet.length){
      for(const id of remet){ const x=res[id][0]; if(x.p.pa!=null&&x.v<x.p.pa&&!confirm('Ce prix est inférieur au prix d\'achat sur '+MEL_CANAL[id].nom+'. Le remettre en vente quand même ?')) return; }
      if(!confirm('Remettre en vente : '+remet.map(i=>MEL_CANAL[i].nom).join(', ')+'.\n\nLe parfum sera EN VENTE tout de suite, au prix indiqué.\n\nContinuer ?')) return;
      if(!demandeUser(false,'remettre un parfum en vente',()=>{})) return;
      enCours=true; v.querySelector('#melg').disabled=true;
      const lignes=[];
      for(const id of remet){ const x=res[id][0];
        v.querySelector('#melr').innerHTML='<div class="mrep">'+MEL_CANAL[id].nom+'…</div>';
        const r=await remetEnVente(x.p,COTE_SITE[id],x.barre||x.v,x.barre?x.v:null);
        lignes.push(r.ok?'<b>'+MEL_CANAL[id].nom+'</b> : en vente à '+money2(r.prix)+'.':'<b>'+MEL_CANAL[id].nom+'</b> : pas remis en vente — '+esc(r.err||'erreur')+'.'); }
      sel.splice(0,sel.length,...sel.filter(id=>!remet.includes(id)));
      if(!sel.length){ enCours=false; v.querySelector('#mela').textContent='Fermer'; v.querySelector('#melr').innerHTML='<div class="mrep">'+lignes.join('<br>')+'</div>'; return; }
      v.querySelector('#melr').innerHTML='<div class="mrep">'+lignes.join('<br>')+'</div>';
      v.querySelector('#melg').disabled=false; enCours=false;
    }
    const nTot=sel.reduce((a,id)=>a+Math.min(MEL_MAX,res[id].length),0);
    if(!confirm('Créer '+nTot+' fiche(s) : '+sel.map(i=>MEL_CANAL[i].nom).join(', ')+(mode==='publie'&&sel.some(i=>COTE_SITE[i])?'\n\nSur les sites perfumestrade.com, elles seront EN VENTE tout de suite.':'\n\nElles seront créées en brouillon.')+'\n\nContinuer ?')) return;
    if(!demandeUser(false,'mettre des parfums en ligne',()=>{})) return;
    enCours=true; v.querySelector('#melg').disabled=true;
    const R=await lanceMel(sel,res,mode,txt=>{ v.querySelector('#melr').innerHTML='<div class="mrep">'+txt+'</div>'; },()=>stop);
    enCours=false; v.querySelector('#mela').textContent='Fermer';
    v.querySelector('#melr').innerHTML=R;
  };
}
/* ---- Mise en ligne AUTOMATIQUE à la création d'un produit (Igal, 20 oct. 2026) ----
   « Quand on crée un produit et qu'on met ses prix, il doit être mis tout seul sur les canaux de vente, sans retourner sur la fiche :
   j'ai vu qu'il était en brouillon sur Shopify et absent du site retail. » Même chemin que « Mettre en ligne » (mêmes garde-fous :
   en stock, code-barres, prix au-dessus du prix d'achat, jamais recréé s'il existe), mais sans case à cocher : les deux sites
   perfumestrade.com sont créés EN VENTE, Perfume City aussi si Sam a donné le droit de poser le stock (sinon brouillon, et on le dit).
   Ce qui n'a pas pu partir est expliqué ligne par ligne, avec le geste pour le faire ensuite. */
function enLigneSansDroit(id){
  /* un compte qui ne peut pas publier crée le produit : le Patron doit le savoir, le tableau de bord le lui dira */
  try{ const p0=cur.find(z=>z.id===id)||tousLesArticles().find(z=>z.id===id);
    if(p0) ['site','sitegros','perfumecity'].forEach(i=>{ if(!horsCanal(p0,i)) pubNote(p0,i,"créé par un compte qui ne peut pas le publier : le Patron doit cliquer « Mettre en ligne » sur la fiche"); }); }catch(e){}
  return '<div class="mrep bad">Pas mis en ligne : seul le dirigeant (rôle Patron), relié au cockpit, peut créer le produit sur les sites. Il le fera depuis la fiche (bouton « Mettre en ligne »).</div>';
}
async function enLigneAuto(id){
  const v=document.createElement('div'); v.className='mvoile';
  const rep=(h,fin)=>{ v.innerHTML=`<div class="mfen" role="dialog" aria-modal="true" data-nolang><h3>Mise en ligne automatique</h3><div id="eaR">${h}</div><div class="mbtn">${fin?'<button class="btn pri" id="eaF">Fermer</button>':''}</div></div>`;
    const b=v.querySelector('#eaF'); if(b) b.onclick=()=>{ v.remove(); try{ render(); }catch(e){} }; };
  if(!melOk()){ document.body.appendChild(v); rep(enLigneSansDroit(id),1); return; }
  if(!demandeUser(false,'mettre le produit en ligne',()=>{ enLigneAuto(id); })) return;
  document.body.appendChild(v); rep('<div class="mrep">Préparation…</div>');
  rep(await enLigneUn(id,h=>rep(h)),1);
}
/* 5 nov. 2026 (Igal) : « quand Sam crée une nouvelle référence dans une facture, qu'il puisse la mettre en ligne à la validation, sans
   aller la chercher dans le Catalogue une par une ». La page Factures ouvre le Catalogue en mode cadre (#enligne=id1,id2&cadre=1) : la même
   mise en ligne automatique, produit après produit, dans une seule fenêtre. */
async function enLigneAutoListe(ids,canauxIds){
  const cadre=document.documentElement.classList.contains('cadre');
  /* 7 nov. 2026 (depuis Tâches) : seulement les canaux demandés (sinon les trois) */
  const seuls=(canauxIds||[]).filter(c=>['site','sitegros','perfumecity'].includes(c));
  const v=document.createElement('div'); v.className='mvoile';
  const noms=id=>{ const p=cur.find(z=>z.id===id)||tousLesArticles().find(z=>z.id===id); return p?esc(((p.marque||'')+' '+(p.nom||'')).trim()):esc(id); };
  const rep=(h,fin)=>{ v.innerHTML=`<div class="mfen" role="dialog" aria-modal="true" data-nolang style="max-height:90vh;overflow:auto"><h3>Mise en ligne des nouvelles références (${ids.length})</h3><div id="eaR">${h}</div><div class="mbtn">${fin?'<button class="btn pri" id="eaF">Fermer</button>':''}</div></div>`;
    const b=v.querySelector('#eaF'); if(b) b.onclick=()=>{ v.remove(); try{ render(); }catch(e){} if(cadre){ try{ window.parent.postMessage({fiche:'fermee'},location.origin); }catch(e){} } }; };
  document.body.appendChild(v);
  if(!melOk()){ rep(ids.map(id=>`<p><b>${noms(id)}</b></p>`+enLigneSansDroit(id)).join(''),1); return; }
  if(!demandeUser(false,'mettre les produits en ligne',()=>{ v.remove(); enLigneAutoListe(ids); })) return;
  const faits=[];
  for(const id of ids){
    const avant=faits.join('');
    const r=await enLigneUn(id,h=>rep(avant+`<p><b>${noms(id)}</b></p>`+h),seuls.length?seuls:null);
    faits.push(`<div style="margin:0 0 12px;padding:0 0 10px;border-bottom:1px solid var(--line,#ddd)"><p style="margin:0 0 4px"><b>${noms(id)}</b></p>${r}</div>`);
    rep(faits.join(''));
  }
  /* la liste « pas en vente partout » publiée pour les tâches (diffusion-erp-v1, tableau de bord) est mise à jour tout de suite :
     ce qui est maintenant en vente n'y manque plus — sinon la tâche « Mettre en ligne N parfums » gardait son chiffre jusqu'à la
     prochaine ouverture du tableau de bord */
  try{ const DIF=lit('diffusion-erp-v1',null); if(DIF&&Array.isArray(DIF.L)){ let ch=false;
    DIF.L.forEach(x=>{ if(!ids.includes(x.cle)) return; const p=cur.find(z=>z.id===x.cle)||tousLesArticles().find(z=>z.id===x.cle); if(!p) return;
      const m=(x.manque||[]).filter(c=>statutDiff(p,c)!=='oui'); if(m.length!==(x.manque||[]).length){ x.manque=m; x.retire=(x.retire||[]).filter(c=>m.includes(c)); ch=true; } });
    if(ch){ DIF.L=DIF.L.filter(x=>(x.manque||[]).length); DIF.n=DIF.L.length; ecrit('diffusion-erp-v1',DIF); } } }catch(e){}
  rep(faits.join(''),1);
}
/* la mise en ligne d'UN produit : rend le compte rendu (html) ; `rep` montre l'avancement */
async function enLigneUn(id,rep,seuls){
  try{
    let p=cur.find(z=>z.id===id)||tousLesArticles().find(z=>z.id===id);
    if(!p){ return '<div class="mrep bad">Produit introuvable.</div>'; }
    const ids=(seuls&&seuls.length)?seuls:['site','sitegros','perfumecity'];
    const {res,skip}=candidatsMel([p],ids);
    const pq=[];
    if(!(p.qte>0)) pq.push("il n'est pas en stock");
    if(!p.bc) pq.push("il n'a pas de code-barres");
    const sel=ids.filter(i=>res[i].length);
    const raison=i=>{ const k=skip[i];
      return pq.length?pq.join(' et '):k.sansPrix?"pas de prix pour ce canal":k.perte?"son prix est inférieur au prix d'achat":k.existe?"il existe déjà sur ce canal":"déjà présent ou statut du canal inconnu"; };
    const manque=ids.filter(i=>!res[i].length).map(i=>`<li><b>${MEL_CANAL[i].nom}</b> : pas mis en ligne — ${raison(i)}.</li>`).join('');
    /* ce qui n'est pas parti est NOTÉ pour le tableau de bord (sauf : déjà en vente, ou canal coupé exprès pour ce parfum) */
    ids.filter(i=>!res[i].length).forEach(i=>{ const st=statutDiff(p,i);
      if(st==='oui'){ pubClair(p,i); return; }
      if(horsCanal(p,i)) return;
      pubNote(p,i,(st==='na'&&!pq.length&&!skip[i].sansPrix&&!skip[i].perte&&!skip[i].existe)?"impossible de savoir s'il est en vente (relevé de ce canal pas encore lu)":raison(i)); });
    window.__melPcStock=false;
    if(sel.includes('perfumecity')){ try{ const r=await fetch(CK_URL+'/api/o/'+CK_ORG+'/shopify/droits',{headers:{Authorization:'Bearer '+ckTok()}}); const j=await r.json(); window.__melPcStock=!!(j&&j.stock); }catch(e){} }
    let R='';
    if(sel.length) R=await lanceMel(sel,res,'publie',t=>rep('<div class="mrep">'+t+'</div>'),()=>false);
    const nb=sel.includes('perfumecity')&&!window.__melPcStock?`<li><b>Perfume City</b> : créé en BROUILLON — l'application Shopify n'a pas encore le droit de poser le stock (write_inventory). Une fois le droit donné : bouton « Mettre en vente » sur la fiche.</li>`:'';
    const fin=(manque||nb)?`<ul style="margin:10px 0 0 18px;padding:0;font-size:13px;line-height:1.5">${nb}${manque}</ul>`:'';
    return (R||'<div class="mrep bad">Rien n\'a pu être mis en ligne.</div>')+fin+(pq.length?`<p style="font-size:12.5px;color:var(--ink-3,#777);margin-top:10px">Dès que ce sera réglé, ouvre la fiche : « Mettre en ligne » le fait en un clic.</p>`:'');
  }catch(e){ return '<div class="mrep bad">La mise en ligne a échoué : '+esc((e&&e.message)||'erreur')+'. Rien n\'est perdu : la fiche est dans le Catalogue, « Mettre en ligne » réessaie.</div>'; }
}
/* 7 nov. 2026 (Igal : « Prix à vérifier » se règle depuis Tâches : il corrige les prix sur place, puis l'ERP demande sur quels
   canaux les poser). La page Tâches ouvre catalogue.html#prix=<id>&canaux=site,sitegros,perfumecity&cadre=1 : on pose les prix de
   l'outil sur les canaux cochés, avec les mêmes règles que la fiche (promo gardée, prix retail = prix payé, Patron seulement),
   et on rend compte canal par canal dans une seule fenêtre. */
async function prixAutoCanaux(id,canauxIds){
  const cadre=document.documentElement.classList.contains('cadre');
  const p0=cur.find(z=>z.id===id)||tousLesArticles().find(z=>z.id===id), p=p0?applique(p0):null;
  const v=document.createElement('div'); v.className='mvoile';
  const nom=p?esc(((p.marque||'')+' '+(p.nom||'')).trim()):esc(id);
  const NOMS={site:'perfumestrade.com',sitegros:'wholesale.perfumestrade.com',perfumecity:'Perfume City (Shopify)'};
  const rep=(h,fin)=>{ v.innerHTML=`<div class="mfen" role="dialog" aria-modal="true" data-nolang style="max-height:90vh;overflow:auto"><h3>${esc(L3('Prix sur les canaux de vente','Prices on the sales channels','Precios en los canales de venta'))} — ${nom}</h3><div id="pxR">${h}</div><div class="mbtn">${fin?'<button class="btn pri" id="pxF">'+esc(L3('Fermer','Close','Cerrar'))+'</button>':''}</div></div>`;
    const b=v.querySelector('#pxF'); if(b) b.onclick=()=>{ v.remove(); try{ render(); }catch(e){} if(cadre){ try{ window.parent.postMessage({fiche:'fermee',prix:'fait'},location.origin); }catch(e){} } }; };
  document.body.appendChild(v);
  if(!p){ rep('<div class="mrep bad">'+esc(L3('Produit introuvable.','Product not found.','Producto no encontrado.'))+'</div>',1); return; }
  const ids=(canauxIds||[]).filter(c=>NOMS[c]);
  if(!ids.length){ rep('<div class="mrep">'+esc(L3('Aucun canal choisi.','No channel chosen.','Ningún canal elegido.'))+'</div>',1); return; }
  if(!prixSitesOk()&&!prixPCOk()){ rep('<div class="mrep bad">'+esc(L3('Seul le Patron, relié au cockpit, peut changer un prix sur un site.','Only the Owner, linked to the cockpit, can change a price on a website.','Solo el Jefe, conectado al cockpit, puede cambiar un precio en una web.'))+'</div>',1); return; }
  if(!demandeUser(false,'changer un prix sur les sites',()=>{ v.remove(); prixAutoCanaux(id,canauxIds); })) return;
  const L=[]; const ligne=(c,t)=>L.push(`<li><b>${esc(NOMS[c])}</b> : ${t}</li>`); const montre=fin=>rep('<ul style="margin:0;padding-left:18px;line-height:1.7">'+L.join('')+'</ul>',fin);
  montre();
  for(const c of ids){
    try{
      if(COTE_SITE[c]){
        const cote=COTE_SITE[c], e=siteDe(p), f=e&&e[cote];
        if(!f||f.pr===undefined){ ligne(c,esc(L3('pas en vente sur ce site — rien à changer','not for sale on this website — nothing to change','no está a la venta en esta web — nada que cambiar'))); montre(); continue; }
        const x=planPrixSites(p).plan.find(y=>y.cid===c);
        if(!x){ ligne(c,esc(L3('déjà au bon prix','already at the right price','ya tiene el precio correcto'))+' ('+money2(f.ps!=null?f.ps:f.pr)+')'); montre(); continue; }
        const r=await envoiePrixFiche(id,cote,true);
        if(r&&r.ok) ligne(c,esc(L3('prix changé','price changed','precio cambiado'))+' → <b>'+money2(x.v)+'</b>'); else ligne(c,esc(L3('pas changé','not changed','sin cambio'))+' — '+esc((r&&r.ko&&r.ko.join(' ; '))||L3('refusé','refused','rechazado')));
      } else {
        const ch=canaux().find(y=>y.id==='perfumecity'), sh=prixShopifyDe(p);
        if(!ch||!sh||sh.amb||!(sh.prix>0)){ ligne(c,esc(L3('pas en vente chez Perfume City — rien à changer','not for sale at Perfume City — nothing to change','no está a la venta en Perfume City — nada que cambiar'))); montre(); continue; }
        /* le prix de l'outil pour Perfume City, c'est d'habitude celui de Shopify : ici on veut y POSER le prix de la fiche
           (manuel du canal s'il y en a un, sinon retail ou gros selon la règle du canal) */
        const pm=(p.pc||{})[ch.id], bse=ch.base==='pvw'?p.pvw:p.pvr;
        const n=(pm!=null&&pm!=='')?+pm:((bse!=null&&bse>0)?r2(bse*(1+(ch.maj||0)/100)):null);
        if(n==null||!(n>0)){ ligne(c,esc(L3('pas de prix pour ce canal','no price for this channel','sin precio para este canal'))); montre(); continue; }
        const nn=Math.round(n*100)/100;
        if(Math.abs(nn-sh.prix)<0.005){ ligne(c,esc(L3('déjà au bon prix','already at the right price','ya tiene el precio correcto'))+' ('+money2(sh.prix)+')'); montre(); continue; }
        if(!prixPCOk()){ ligne(c,esc(L3('seul le Patron peut changer ce prix','only the Owner can change this price','solo el Jefe puede cambiar este precio'))); montre(); continue; }
        const r=await fetch(CK_URL+'/api/o/'+CK_ORG+'/shopify/prix',{method:'POST',headers:{'Content-Type':'application/json',Authorization:'Bearer '+ckTok()},
          body:JSON.stringify({bc:p.bc,prix:nn,attendu:sh.prix})});
        const j=await r.json().catch(()=>({}));
        if(j&&j.avant!=null&&!j.ok) PCSHOP_OVR[sh.k]=j.avant;
        if(!r.ok) throw new Error(j.erreur||('erreur '+r.status));
        PCSHOP_OVR[sh.k]=j.apres;
        if(!j.inchange) log({act:'prix',lib:'prix changé chez Perfume City (Shopify)',bc:p.bc,ref:(p.marque||'')+' '+(p.nom||''),av:money2(j.avant),ap:money2(j.apres)});
        ligne(c,esc(L3('prix changé','price changed','precio cambiado'))+' → <b>'+money2(j.apres)+'</b>');
      }
    }catch(err){ ligne(c,esc(L3('pas changé','not changed','sin cambio'))+' — '+esc((err&&err.message)||'erreur')); }
    montre();
  }
  montre(1);
}
async function photoPourSite(p){
  if(p.imgPerso&&/^data:image\/(jpeg|png|webp);base64,/.test(p.img||'')) return {data:p.img};
  if(/^https:\/\//.test(p.img||'')) return {url:p.img};
  if(p.bc&&!PHOTO_KO.has(p.bc)&&/^https:/.test(location.protocol)){
    const u=location.origin+location.pathname.replace(/[^/]*$/,'')+'photos/'+encodeURIComponent(p.bc)+'.webp';
    try{ const r=await fetch(u,{method:'HEAD'}); if(r.ok&&/image/.test(r.headers.get('content-type')||'')) return {url:u}; }catch(e){}
    PHOTO_KO.add(p.bc);
  }
  return {};
}
/* remet en vente une fiche RETIRÉE d'un site WooCommerce (cote 'd' ou 'g'), avec son prix : la route /site/prix « republier »,
   la même que la case de la fiche ; le relevé local suit la réponse du site */
async function remetEnVente(p,cote,barre,promo){
  const rf=retireCote(p,cote); if(!rf) return {ok:false,err:"la fiche n'est plus retirée sur ce site"};
  try{
    const r=await fetch(CK_URL+'/api/o/'+CK_ORG+'/site/prix',{method:'POST',headers:{'Content-Type':'application/json',Authorization:'Bearer '+ckTok()},
      body:JSON.stringify({quel:cote==='g'?'gros':'',bc:rf.k,barre:barre,promo:promo==null?'':promo,republier:true})});
    const j=await r.json().catch(()=>({}));
    if(!r.ok||!j.ok) return {ok:false,err:j.erreur||('erreur '+r.status)};
    const R=Object.assign({},(SITE._retires&&SITE._retires[cote])||{});
    const g=Object.assign({},rf.f,{pr:j.apres.barre,ps:j.apres.promo}); delete g.t; delete R[rf.k];
    SITE._retires=Object.assign({},SITE._retires,{[cote]:R});
    const kk=(SITE[rf.k]?rf.k:Object.keys(SITE).find(x=>!x.startsWith('_')&&x.replace(/^0+/,'')===rf.k.replace(/^0+/,'')))||rf.k;
    SITE[kk]=Object.assign({},SITE[kk]||{},{[cote]:g});
    ecrit(KSITE,SITE); _FMC=null; _SITE0=null; _RETS=null;
    const nomSite=cote==='g'?'wholesale.perfumestrade.com':'perfumestrade.com';
    log({act:'prix',lib:'fiche remise en vente avec son prix sur '+nomSite+' (fenêtre « Mettre en ligne »)',bc:p.bc,ref:(p.marque||'')+' '+(p.nom||''),av:'retirée de la vente',ap:money2(j.apres.promo!=null?j.apres.promo:j.apres.barre)});
    return {ok:true,prix:j.apres.promo!=null?j.apres.promo:j.apres.barre};
  }catch(e){ return {ok:false,err:(e&&e.message)||'le cockpit ne répond pas'}; }
}
async function lanceMel(sel,res,mode,prog,arret){
  const T={cree:0,deja:0,refus:0,erreur:0}, pb=[];
  for(const id of sel){
    const items=res[id].slice(0,MEL_MAX), cote=COTE_SITE[id];
    for(let i=0;i<items.length;i+=MEL_LOT){
      if(arret()) break;
      const lot=items.slice(i,i+MEL_LOT);
      prog(MEL_CANAL[id].nom+' : '+i+' / '+items.length+'…');
      /* 5 nov. 2026 (le Mont Blanc : « Sam en a envoyé 6 à Perfume City, Shopify a reçu 14 ») : chez Perfume City, le stock posé est celui
         de SON inventaire (pc-stock-v1), jamais le stock de Perfumes Trade */
      const corps={items:await Promise.all(lot.map(async x=>{ const it={bc:x.p.bc,nom:melNom(x.p),marque:x.p.marque||'',type:x.p.type||'',barre:x.barre||x.v,qte:id==='perfumecity'?qtePCde(x.p):x.p.qte}; if(x.barre) it.promo=x.v;   /* type : la catégorie Shopify (5 nov. 2026) */
        /* la photo : celle choisie dans l'ERP (sans adresse : le cockpit la prête au site), sinon l'adresse https connue, sinon la photo de l'ERP si elle existe */
        const ph=await photoPourSite(x.p); if(ph.data) it.imageData=ph.data; else if(ph.url) it.image=ph.url; return it; }))};
      if(id==='sitegros') corps.quel='gros';
      if(mode==='publie'&&(cote||window.__melPcStock)) corps.publie=true;
      let j={};
      try{
        const r=await fetch(CK_URL+'/api/o/'+CK_ORG+(id==='perfumecity'?'/shopify/cree':'/site/cree'),{method:'POST',
          headers:{'Content-Type':'application/json',Authorization:'Bearer '+ckTok()},body:JSON.stringify(corps)});
        j=await r.json().catch(()=>({}));
        if(!r.ok||!j.lignes){ pb.push(MEL_CANAL[id].nom+' : '+(j.erreur||('erreur '+r.status))); T.erreur+=lot.length; if(mode==='publie') lot.forEach(x=>pubNote(x.p,id,j.erreur||('le cockpit a répondu erreur '+r.status))); break; }
      }catch(e){ pb.push(MEL_CANAL[id].nom+' : '+((e&&e.message)||'le cockpit ne répond pas')); T.erreur+=lot.length; if(mode==='publie') lot.forEach(x=>pubNote(x.p,id,(e&&e.message)||'le cockpit ne répond pas')); break; }
      const par=new Map(lot.map(x=>[String(x.p.bc),x]));
      (j.lignes||[]).forEach(l=>{
        if(l.etat==='brouillon'||l.etat==='en ligne'){ T.cree++; const X=par.get(String(l.bc)); melRange(id,cote,l,X&&X.p); if(l.visible) pb.push((l.nom||l.bc)+' (Perfume City) : en vente mais pas visible — '+l.visible);
          if(mode==='publie'&&X&&X.p){ if(l.etat==='en ligne'&&!l.visible) pubClair(X.p,id);
            else pubNote(X.p,id,l.visible?('en vente mais pas visible sur la boutique : '+l.visible):(id==='perfumecity'&&!window.__melPcStock?"créé en brouillon : le droit de poser le stock (write_inventory) manque":'créé en brouillon, pas en vente')); }
          if(X&&X.saisi){ try{ MOD[X.p.id]=Object.assign({},MOD[X.p.id]||{}); MOD[X.p.id].pc=Object.assign({},MOD[X.p.id].pc,{[id]:X.v}); sauveMOD(); }catch(e){} } }
        else if(l.etat==='deja') T.deja++;
        else { if(l.etat==='refus') T.refus++; else T.erreur++; pb.push((l.bc||'?')+' ('+MEL_CANAL[id].nom+') : '+(l.pourquoi||l.etat));
          if(mode==='publie'){ const X=par.get(String(l.bc)); if(X&&X.p) pubNote(X.p,id,(l.etat==='refus'?'refusé : ':'erreur : ')+(l.pourquoi||l.etat)); } }
      });
      try{ if(cote){ ecrit(KSITE,SITE); _FMC=null; _SITE0=null; _RETS=null; } else { ecrit('shopify-pc-prix-v1',DIFF_S||{}); } }catch(e){}
    }
  }
  try{ const J=lit('crm-journal-v1',[]); J.push({t:new Date().toISOString(),u:(typeof NOM_UTIL!=='undefined'&&NOM_UTIL)||'(non renseigné)',act:'site',lib:T.cree+' fiche(s) créée(s) sur '+sel.map(i=>MEL_CANAL[i].nom).join(', ')+(mode==='publie'?' (en ligne)':' (brouillon)'),n:T.cree,impact:0,det:[]}); ecrit('crm-journal-v1',J); }catch(e){}
  try{ majDiff(); }catch(e){}
  return `<div class="mrep${T.erreur||T.refus?' bad':''}"><b>${nf(T.cree)}</b> fiche(s) créée(s) · ${nf(T.deja)} déjà là · ${nf(T.refus)} refusée(s) · ${nf(T.erreur)} en erreur.`
    +(T.cree?`<br><small>${mode==='publie'?(window.__melPcStock?'Elles sont en vente.':'Celles des sites perfumestrade.com sont en vente ; chez Perfume City, en brouillon.'):"Elles sont en brouillon : pour les publier sur les sites perfumestrade.com, utilise « Remettre en vente » dans l'onglet « Sans prix sur le site » ; chez Perfume City, publie-les dans Shopify."}</small>`:'')
    +(pb.length?'<br><small>'+pb.slice(0,8).map(esc).join('<br>')+(pb.length>8?'<br>… et '+(pb.length-8)+' autre(s)':'')+'</small>':'')+'</div>';
}
/* ---------------------------------------------------------------------------
   ALERTES « PAS EN LIGNE » (Igal, 21 oct. 2026 : « l'ERP ne doit jamais mentir sans le dire » — Coach FLORAL était resté en brouillon
   chez Perfume City et absent du site retail, et personne ne l'a su avant que Sam regarde la fiche).
   Chaque fois qu'une mise en ligne EN VENTE n'aboutit pas sur un canal (refus, erreur, brouillon, pas de prix, pas de stock…), on le
   note ici, par parfum et par canal, avec la raison. Le tableau de bord les affiche tant que le parfum n'est pas vraiment en vente.
   Elles se retirent toutes seules dès que le relevé du canal montre le parfum en vente (majDiff), ou à la main depuis le tableau de bord.
   Ce n'est PAS la liste des parfums « pas diffusés » : ceux-là, on a choisi de ne pas les publier (le filtre Diffusion les montre).
--------------------------------------------------------------------------- */
const KPUB='publications-v1';
const pubCle=p=>{ const b=String((p&&p.bc)||'').replace(/[^0-9A-Za-z]/g,'').replace(/^0+/,''); return b||String((p&&p.id)||''); };
function pubLit(){ let o=null; try{ o=lit(KPUB,{}); }catch(e){} return (o&&typeof o==='object'&&!Array.isArray(o))?o:{}; }
function pubNote(p,canal,raison){
  try{ const k=pubCle(p); if(!k||!MEL_CANAL[canal]) return; const O=pubLit(), t=new Date().toISOString();
    const e=O[k]||{k,id:p.id||'',bc:p.bc||'',ko:{}};
    e.nom=((p.marque||'')+' '+(p.nom||'')).replace(/\s+/g,' ').trim().slice(0,120); e.t=t; e.ko=e.ko||{};
    e.ko[canal]={r:String(raison||'raison inconnue').slice(0,220),t}; O[k]=e;
    const ks=Object.keys(O); if(ks.length>300) ks.sort((a,b)=>String(O[a].t).localeCompare(String(O[b].t))).slice(0,ks.length-300).forEach(x=>delete O[x]);
    ecrit(KPUB,O); }catch(e){}
}
function pubClair(p,canal){
  try{ const k=pubCle(p), O=pubLit(); if(!O[k]) return; if(O[k].ko) delete O[k].ko[canal];
    if(!Object.keys(O[k].ko||{}).length) delete O[k]; ecrit(KPUB,O); }catch(e){}
}
/* au chargement et après chaque lecture de relevé : ce qui est maintenant en vente (ou coupé exprès pour ce parfum) sort de la liste */
function pubVerifie(arts){
  try{ const O=pubLit(), ks=Object.keys(O); if(!ks.length) return;
    const par=new Map(arts.map(p=>[pubCle(p),p])); let ch=false;
    ks.forEach(k=>{ const e=O[k], p=par.get(k); if(!p) return;
      Object.keys(e.ko||{}).forEach(c=>{ if(statutDiff(p,c)==='oui'||horsCanal(p,c)){ delete e.ko[c]; ch=true; } });
      if(!Object.keys(e.ko||{}).length){ delete O[k]; ch=true; } });
    if(ch) ecrit(KPUB,O); }catch(e){}
}
/* on recolle tout de suite ce que le cockpit vient de ranger */
function melRange(id,cote,l,p){
  const cle0=String(l.bc||'').replace(/[^0-9A-Za-z]/g,'');
  if(cote){
    const f={id:l.id,pr:l.barre,ps:l.promo!=null?l.promo:null,q:l.qte,nom:String(l.nom||'').slice(0,90)};
    if(l.etat==='brouillon'){ const R=Object.assign({},(SITE._retires&&SITE._retires[cote])||{}); R[cle0]=Object.assign({},f,{t:new Date().toISOString()}); SITE._retires=Object.assign({},SITE._retires,{[cote]:R}); }
    else { const kk=(p&&siteCle(p))||cle0; SITE[kk]=Object.assign({},SITE[kk]||{},{[cote]:f}); }
  }else{
    if(!DIFF_S) DIFF_S={};
    DIFF_S[cle0.replace(/^0+/,'')]=[String(l.id),String(l.vid||''),l.prix,l.barre!=null?l.barre:null,l.etat==='en ligne'?1:0,String(l.handle||'')];
  }
}
/* Igal, 17 oct. 2026 : « il est encore en draft » — un produit créé en brouillon chez Perfume City se met en vente d'un clic :
   le cockpit pose d'abord le stock de l'ERP, puis passe le produit en actif. */
document.addEventListener('click',async e=>{ const b=e.target.closest&&e.target.closest('[data-pcpub]'); if(!b) return;
  const p=(typeof FICHE!=='undefined'&&FICHE&&cur[FICHE.pos])||null; if(!p||!melOk()) return;
  const qpc=qtePCde(p);
  if(!(qpc>0)){ alert(vf('Perfume City n\'a pas ce parfum dans son inventaire (0) : donne-lui d\'abord des flacons (facture d\'achat ou transfert), puis mets-le en vente.')); return; }
  if(!confirm('Mettre « '+((p.marque||'')+' '+(p.nom||'')).trim()+' » en vente chez Perfume City, avec '+nf(qpc)+' en stock (son inventaire) ?')) return;
  if(!demandeUser(false,'mettre un produit en vente chez Perfume City',()=>{})) return;
  b.disabled=true; b.textContent='Envoi…';
  const dit=(t,cls)=>{ const d=$('dst'); if(d){ d.textContent=t; d.className='st'+(cls?' '+cls:''); } };
  try{
    const r=await fetch(CK_URL+'/api/o/'+CK_ORG+'/shopify/publie',{method:'POST',headers:{'Content-Type':'application/json',Authorization:'Bearer '+ckTok()},body:JSON.stringify({bc:p.bc,qte:qpc})});
    const j=await r.json().catch(()=>({}));
    if(!r.ok||!j.ok) throw new Error(j.erreur||('erreur '+r.status));
    try{ const S=lit('shopify-pc-prix-v1',{}); const k=String(p.bc||'').replace(/[^0-9A-Za-z]/g,'').replace(/^0+/,''); if(Array.isArray(S[k])){ S[k][4]=1; ecrit('shopify-pc-prix-v1',S); DIFF_S=S; } }catch(e){}
    log({act:'site',lib:'produit mis en vente chez Perfume City (stock '+j.stock+') — '+((p.marque||'')+' '+(p.nom||'')).trim(),bc:p.bc||'',ref:'',av:'brouillon',ap:'en vente'});
    dessineFiche();   /* redessine la fiche (le bouton change), PUIS écrit l'état — sinon le redessin l'efface */
    if(j.visible){ dit('En vente chez Perfume City (stock '+j.stock+'), mais PAS visible sur la boutique en ligne : '+j.visible,''); }
    else dit('En vente et visible chez Perfume City, stock '+j.stock+(j.canaux?' ('+j.canaux+' canal/canaux)':'')+'.','ok');
  }catch(err){ b.disabled=false; b.textContent='Mettre en vente'; dit('Pas mis en vente : '+((err&&err.message)||''),''); }
});
/* le bouton « Mettre en ligne » de la fiche, quand le parfum n'est pas sur ce site.
   31 oct. 2026 (Igal : « cette fenêtre m'empêche de voir les autres prix, je ne peux pas la bouger, change de méthode ») : plus de
   fenêtre par-dessus la fiche. Le parfum est créé EN VENTE sur ce site, au prix que la ligne du canal montre (celui qu'on règle dans
   la fiche), avec UNE validation ; ce qui se passe s'écrit à côté du bouton. Mêmes garde-fous que « Mettre en ligne » : en stock,
   code-barres, prix au-dessus du prix d'achat (Patron : avertissement), jamais recréé s'il existe. */
document.addEventListener('click',async e=>{ const b=e.target.closest&&e.target.closest('[data-mel1]'); if(!b) return;
  const p=(typeof FICHE!=='undefined'&&FICHE&&cur[FICHE.pos])||null; if(!p) return;
  const id=b.dataset.mel1, c=(REG.canaux||[]).find(x=>x.id===id)||{id,base:id==='sitegros'?'pvw':'pvr',maj:0};
  const out=(t,ok)=>{ let d=b.parentElement.querySelector('.mel1r'); if(!d){ d=document.createElement('small'); d.className='mel1r'; b.after(d); } d.textContent=t; d.style.color=ok?'var(--good)':'var(--crit)'; };
  if(!melOk()){ out('Seul le dirigeant, relié au cockpit, peut mettre en ligne.'); return; }
  const br=FICHE.brouillon&&FICHE.brouillon.pc&&FICHE.brouillon.pc[id];
  const v=r2(br!=null&&br!==''?+br:prixCanal(p,c).v);
  if(!(v>0)){ out('Pas de prix pour ce site : écris-le dans la case de la ligne, puis recommence.'); return; }
  if(!(p.qte>0)){ out('Pas de stock : rien à mettre en vente.'); return; }
  const perte=p.pa!=null&&v<p.pa;
  if(!confirm((p.marque||'')+' '+(p.nom||'')+'\n\nMettre EN VENTE sur '+MEL_CANAL[id].nom+' à '+money2(v)+' ?'+(perte?'\n\nAttention : c\'est moins que le prix d\'achat.':''))) return;
  if(!demandeUser(false,'mettre un parfum en ligne',()=>{})) return;
  b.disabled=true; b.textContent='…';
  if(id==='perfumecity'){ try{ const r=await fetch(CK_URL+'/api/o/'+CK_ORG+'/shopify/droits',{headers:{Authorization:'Bearer '+ckTok()}}); const j=await r.json(); window.__melPcStock=!!(j&&j.stock); }catch(x){} }
  const R=await lanceMel([id],{[id]:[{p,v}]},'publie',t=>{ b.textContent=t; },()=>false);
  const txt=String(R||'').replace(/<[^>]+>/g,' ').replace(/\s+/g,' ').trim();
  try{ render(); const l=cur.findIndex(x=>x.id===p.id); if(l>=0){ FICHE.pos=l; dessineFiche(); } }catch(x){}
  const b2=document.querySelector('[data-cn="'+id+'"] [data-mel1]')||document.querySelector('[data-mel1="'+id+'"]');
  const zone=document.querySelector('[data-cn="'+id+'"]');
  if(zone){ const d=document.createElement('div'); d.className='mel1r'; d.style.cssText='font-size:12.5px;margin-top:6px;color:'+(/créée|en vente/i.test(txt)&&!/0 fiche/.test(txt)?'var(--good)':'var(--crit)'); d.textContent=txt; zone.appendChild(d); }
  else if(b2) out(txt,/en vente/i.test(txt)); });
function sansPrixSite(p,site){
  const L=site==='g'?['g']:site==='d'?['d']:['d','g'];
  const e=siteDe(p);
  return L.some(c=>{
    /* 12 oct. 2026 (Igal : « ça reste dans no price on website, et ça ne doit pas le faire ») : une fiche retirée À LAQUELLE ON A POSÉ un prix
       (« Enregistrer le prix, reste hors ligne ») n'est plus « sans prix » : elle sort de l'onglet. Elle y reste tant qu'aucun prix n'est sur le site. */
    const rr=retireCote(p,c); if(rr) return !(rr.f.pr>0);
    const f=e&&e[c]; return !!(f&&f.pr!==undefined&&(f.pr==null||+f.pr===0)&&(f.ps==null||+f.ps===0));
  });
}
/* 12 oct. 2026 (Sam : « le logo Amazon est sur des produits qui ne sont pas sur Amazon ») : l'ASIN de l'inventaire sert à
   comparer les prix, il ne prouve PAS que Sam vend ce parfum (2 079 fiches en ont un). Seule une vente Amazon enregistrée
   le prouve : le logo, l'onglet « Vendus sur Amazon » et la pastille ne se fondent plus que sur elle. */
function venduAmazon(p){
  if(_AZV===null){ _AZV=new Set(); try{ (lit('factures-v1',[])||[]).forEach(f=>{ if(f&&f.sens==='vente'&&/amazon/i.test(f.canal||'')) (f.lignes||[]).forEach(l=>{ if(l.cle) _AZV.add(l.cle); if(l.bc) _AZV.add(String(l.bc)); }); }); }catch(e){} }
  return _AZV.has(p.cle||p.id)||_AZV.has(String(p.bc||''));
}
const badgeAmazon=p=>venduAmazon(p)?`<span class="laz" title="${p.asin?'Vendu sur Amazon · ASIN '+esc(p.asin):'Vendu sur Amazon'}">${logo('amazon','Amazon')}</span>`:'';
function azLien(p, m){
  if(m && m.url) return m.url;
  if(p.asin) return 'https://www.amazon.com/dp/'+encodeURIComponent(p.asin);
  /* 11 oct. 2026 (Igal : « les parfums ne sont pas trouvables ») : la recherche par code-barres
     ne donne presque jamais rien sur Amazon ; par marque + nom + contenance, si */
  return 'https://www.amazon.com/s?k='+encodeURIComponent(((p.marque||'')+' '+(p.nom||'')+' '+(p.type||'')+' '+(p.ml?p.ml+' oz':'')).replace(/\s+/g,' ').trim());
}

/* Igal, 17 oct. 2026 : « à chaque fois que je cliquais sur "ouvrir la fiche Amazon", je tombais sur des produits sans prix. Ce qui
   m'intéresse, c'est de connaître les prix vendus sur Amazon. » L'ASIN de l'inventaire ne prouve pas qu'Amazon vend ce parfum
   AUJOURD'HUI : la page tombait souvent sur « actuellement indisponible », sans prix. Le lien direct n'est donc donné que si l'on SAIT
   que la page porte un prix — l'annonce de Sam (rapport des annonces, prix et quantité du jour) ou un relevé de marché avec son prix.
   Sinon : une recherche Amazon par marque, nom et contenance, qui montre les offres réelles avec leur prix. Le prix connu est écrit
   sur le bouton. */
function azPourFiche(p){
  const m=MAR[p.id], ann=prixAmazonDe(p);
  const asin=(ann&&ann.asin)||p.asin||'';
  if(ann&&ann.prix>0&&(asin||(m&&m.url))) return {exact:true,href:(m&&m.url)||('https://www.amazon.com/dp/'+encodeURIComponent(asin)),prix:ann.prix,asin,
    titre:L3('Ton annonce Amazon, au prix du jour','Your Amazon listing, at today\'s price','Tu anuncio de Amazon, al precio de hoy')+(asin?' · ASIN '+asin:'')};
  /* un relevé ancien : la page avait un prix ce jour-là. Le lien direct reste, mais son prix ne s'écrit pas (Igal, 27 sept. : plus de vieux prix Amazon) */
  if(m&&m.url&&m.amz>0) return {exact:true,href:m.url,prix:null,asin,
    titre:L3('Page relevée avec son prix','Page recorded with its price','Página registrada con su precio')+(asin?' · ASIN '+asin:'')};
  return {exact:false,href:azLien({marque:p.marque,nom:p.nom,type:p.type,ml:p.ml},null),prix:null,asin:'',
    titre:L3('Aucun prix Amazon connu pour ce parfum : recherche par nom, qui montre les offres en vente','No known Amazon price for this perfume: search by name, which shows the live offers','Ningún precio de Amazon conocido para este perfume: búsqueda por nombre, que muestra las ofertas')};
}
/* ---------- Déposer un relevé pour tout le catalogue d'un coup ----------
   La fiche produit sait déjà saisir UN relevé à la main. À 2 083 références
   avec un ASIN, ça ne tient pas : il faut une porte par laquelle un fichier
   entier arrive. C'est la même porte qu'une source automatique empruntera le
   jour où elle existera — elle écrit dans le même magasin, et la colonne comme
   la fiche se mettent à jour sans une ligne de plus.

   Les intitulés sont reconnus par égalité EXACTE, jamais par « contient » :
   un fichier de relevés porte prix_achat, prix_gros, prix_retail ET
   prix_amazon côte à côte, et un « contient prix » collerait le prix d'achat
   dans la colonne Amazon sans que personne ne s'en aperçoive. */
const AZ_ALIAS={
  asin:  ['asin','_asin','amazon asin'],
  bc:    ['code_barres','code-barres','codebarres','code barres','barcode','ean','upc','a_barcode'],
  prix:  ['prix_amazon','prix amazon','amazon','amz','buybox','buy box','buy_box','prix'],
  vend:  ['vendeur','seller','vendu par'],
  n:     ['nb_vendeurs','nb vendeurs','nombre de vendeurs','offres','offers'],
  rang:  ['rang_categorie','rang categorie','rang catégorie','rang','rank','bsr'],
  cat:   ['categorie','catégorie','category'],
  rangG: ['rang_general','rang general','rang général'],
  note5: ['note5','note_5','rating','etoiles','étoiles'],
  avis:  ['avis','reviews','nb_avis'],
  dem:   ['achetes_mois','achetes mois','achetés le mois dernier','demande','bought'],
  url:   ['url','lien','adresse','link'],
  date:  ['date','date_releve','date relevé','le'],
  note:  ['note','remarque','commentaire','observation'],
};
let AZ_LOT=null;   /* ce qui a été lu et attend le bouton Enregistrer */

function azAnalyse(texte){
  const L=csvLignes(texte);
  if(L.length<2) return {err:'Fichier vide, ou une seule ligne : il faut les intitulés puis au moins un relevé.'};
  const head=L[0].map(h=>h.replace(/^﻿/,'').trim().toLowerCase());
  const map={};
  Object.entries(AZ_ALIAS).forEach(([k,al])=>{
    const i=head.findIndex(h=>al.includes(h));
    if(i>=0) map[k]=i;
  });
  if(map.asin===undefined && map.bc===undefined)
    return {err:'Aucune colonne « asin » ni « code_barres » : impossible de savoir de quel parfum on parle.'};
  if(map.prix===undefined)
    return {err:'Aucune colonne « prix_amazon » : il n\'y a rien à relever.'};

  /* deux répertoires : par ASIN et par code-barres. Un ASIN peut désigner
     plusieurs références — Sam met parfois deux produits sous la même fiche —
     et dans ce cas le relevé va sur toutes. */
  const TOUS=tousLesArticles();
  const parAsin={}, parBc={};
  TOUS.forEach(p=>{
    if(p.asin){ const ka=String(p.asin).toUpperCase(); (parAsin[ka]=parAsin[ka]||[]).push(p); }
    if(p.bc){ const kb=String(p.bc).trim(); (parBc[kb]=parBc[kb]||[]).push(p); }
  });

  const val=(r,k)=>map[k]===undefined?'':String(r[map[k]]==null?'':r[map[k]]).trim();
  const lignes=[], inconnues=[];
  let sansPrix=0, touchees=0;
  for(let i=1;i<L.length;i++){
    const r=L[i];
    const a=val(r,'asin').toUpperCase(), b=val(r,'bc');
    const cibles=(a&&parAsin[a])||(b&&parBc[b])||[];
    if(!cibles.length){ if(a||b) inconnues.push(a||b); continue; }
    const brut=val(r,'prix');
    const prix=/^(indisponible|unavailable|n\/a|-|—)?$/i.test(brut)?null:nombre(brut);
    if(prix==null) sansPrix++;
    touchees+=cibles.length;
    lignes.push({cibles, prix,
      vend:val(r,'vend')||null, n:nombre(val(r,'n')), rang:nombre(val(r,'rang')),
      cat:val(r,'cat')||null, rangG:nombre(val(r,'rangG')), note5:nombre(val(r,'note5')),
      avis:nombre(val(r,'avis')), dem:val(r,'dem')||null, url:val(r,'url')||null,
      date:val(r,'date')||null, note:val(r,'note')||null});
  }
  return {map, head, lignes, inconnues, sansPrix, touchees, total:L.length-1};
}

function azApercu(res){
  const box=$('azpv'), msg=$('azmsg'), ok=$('azok');
  box.style.display=''; msg.className='msg';
  if(res.err){ AZ_LOT=null; ok.disabled=true; box.innerHTML=`<div style="padding:14px">${esc(res.err)}</div>`;
    msg.textContent=''; return; }
  AZ_LOT=res; ok.disabled=!res.lignes.length;
  const cols=Object.keys(res.map).map(k=>esc(res.head[res.map[k]])).join(' · ');
  const inc=res.inconnues.slice(0,8).map(esc).join(', ');
  box.innerHTML=`<div style="padding:14px;font-size:13.5px;line-height:1.7">
    <b>${nf(res.lignes.length)}</b> ligne${res.lignes.length>1?'s':''} sur ${nf(res.total)} correspondent à une référence
    ${res.touchees!==res.lignes.length?` (<b>${nf(res.touchees)}</b> fiches touchées : un ASIN sert à plusieurs références)`:''}.<br>
    ${res.sansPrix?`<b>${nf(res.sansPrix)}</b> sans prix : ${res.sansPrix>1?'elles seront marquées':'elle sera marquée'} « indisponible sur Amazon ».<br>`:''}
    ${res.inconnues.length?`<b style="color:var(--warn)">${nf(res.inconnues.length)}</b> ligne${res.inconnues.length>1?'s':''} sans référence connue — ${res.inconnues.length>1?'ignorées':'ignorée'} : <span class="mono">${inc}</span>${res.inconnues.length>8?'…':''}<br>`:''}
    <span style="color:var(--ink-3)">Colonnes reconnues : ${cols||'aucune'}</span>
  </div>`;
  msg.textContent=res.lignes.length?'':'Rien à enregistrer.';
}

function azEnregistre(){
  if(!AZ_LOT||!AZ_LOT.lignes.length) return;
  const t=new Date().toISOString();
  let n=0;
  AZ_LOT.lignes.forEach(l=>{
    /* la date du fichier fait foi quand elle est là : un relevé de ce matin
       importé ce soir reste un relevé de ce matin */
    let le=t;
    if(l.date){ const d=new Date(l.date); if(!isNaN(d.getTime())) le=d.toISOString(); }
    l.cibles.forEach(p=>{
      const av=MAR[p.id];
      const m={amz:l.prix, le, par:'relevé importé'+(USR?' · '+USR:''), bc:p.bc||''};
      [['rang',l.rang],['cat',l.cat],['rangG',l.rangG],['note5',l.note5],['avis',l.avis],
       ['dem',l.dem],['vend',l.vend],['n',l.n],['url',l.url],['note',l.note]]
        .forEach(([k,v])=>{ if(v!=null&&v!=='') m[k]=v; });
      /* ce que le fichier ne dit pas, on ne l'efface pas : le rang relevé à la
         main la semaine dernière survit à un import qui n'apporte que le prix */
      if(av) ['rang','cat','rangG','catG','note5','avis','dem','vend','n','url','note']
        .forEach(k=>{ if(m[k]===undefined && av[k]!==undefined) m[k]=av[k]; });
      m.hist=(av&&av.hist&&av.hist.length)?av.hist.slice()
            :(av&&av.le?[{le:av.le,amz:av.amz??null,rang:av.rang??null}]:[]);
      m.hist.push({le:m.le,amz:m.amz??null,rang:m.rang??null});
      if(m.hist.length>120) m.hist=m.hist.slice(-120);
      MAR[p.id]=m; n++;
    });
  });
  sauveMAR();
  log({act:'prix',lib:'relevés Amazon importés',ref:n+' référence'+(n>1?'s':''),
       av:null,ap:n+' relevé'+(n>1?'s':'')+' enregistré'+(n>1?'s':'')});
  /* on ne referme pas : le compte de ce qui vient d'être écrit est la seule
     preuve que l'import a fait ce qu'il annonçait, et une fenêtre qui se ferme
     l'emporte avec elle */
  AZ_LOT=null; $('azok').disabled=true; $('azfi').value='';
  $('azmsg').textContent=nf(n)+' relevé'+(n>1?'s':'')+' enregistré'+(n>1?'s':'')+'.';
  $('azmsg').className='msg ok';
  $('azannul').textContent='Fermer';
  paint();
}

const COLS=[
  {k:'nom',   lib:'Marque et nom', t:'txt', v:p=>(p.marque||'')+' '+(p.nom||'')},
  {k:'fmt',   lib:'Format',        t:'num', v:p=>parseFloat(String(p.ml).replace(',','.')), cls:'colfmt'},
  {k:'qte',   lib:'Stock',         t:'num', v:p=>p.qte, cls:'colq',  al:'r'},
  /* Trier sur l'ÉCART, comme pour Amazon : la question est « où sommes-nous le
     plus loin de ce que le site raconte au client », pas « qui a le plus de
     stock en ligne ». Sans relevé du site, la valeur est nulle et la ligne
     part en bas, avec les autres colonnes vides. */
  {k:'site',  lib:'Sur les sites', t:'num', v:p=>{ const e=siteEcart(p); return e?Math.abs(e.d):null; },
              cls:'colsite', al:'r'},
  {k:'pa',    lib:"Prix d'achat",  t:'num', v:p=>p.pa,  cls:'colpa', al:'r'},
  {k:'pvr',   lib:'Prix retail',   t:'num', v:p=>p.pvr, cls:'colpvr', al:'r'},
  /* Trier sur l'ECART, pas sur le prix Amazon : « qui est le plus loin du
     marche » est la question qu'on se pose ; « qui coute le plus cher chez
     Amazon » n'interesse personne. Sans releve, la valeur est nulle et la
     ligne part en bas, comme les autres colonnes vides. */
  {k:'az',    lib:'Amazon',        t:'num', v:p=>{ const e=azEcart(p); return e?e.d:null; },
              cls:'colaz', al:'r'},
  {k:'pvw',   lib:'Prix de gros',  t:'num', v:p=>p.pvw, al:'r'},
  {k:'mgr',   lib:'Marge retail',  t:'num', v:p=>marge(p,p.pvr), cls:'colmg colmgr', al:'r'},
  {k:'mgw',   lib:'Marge wholesale',t:'num', v:p=>marge(p,p.pvw), cls:'colmg', al:'r'},
  {k:'an',    lib:'Alertes',       t:'num', v:p=>p.an.length, cls:'colfl'},
  {k:'bc',    lib:'Code-barres',   t:'txt', v:p=>p.bc||'', cls:'colbc'}
];
const COLI=Object.fromEntries(COLS.map(c=>[c.k,c]));

function trieur(){
  if(!TRI) return null;
  const c=COLI[TRI.col]; if(!c) return null;
  const sens=TRI.dir==='asc'?1:-1;
  return (a,b)=>{
    const va=c.v(a), vb=c.v(b);
    const na=va==null||va===''||(typeof va==='number'&&isNaN(va));
    const nb=vb==null||vb===''||(typeof vb==='number'&&isNaN(vb));
    if(na&&nb) return 0;
    if(na) return 1;            /* les vides toujours en bas */
    if(nb) return -1;
    if(c.t==='txt') return sens*String(va).localeCompare(String(vb),'fr',{numeric:true});
    return sens*(va-vb);
  };
}
function bascule(col){
  const c=COLI[col]; if(!c) return;
  const depart = c.t==='txt' ? 'asc' : 'desc';   /* un prix ou un stock : le plus grand d'abord */
  if(!TRI||TRI.col!==col) TRI={col,dir:depart};
  else TRI={col,dir:TRI.dir==='asc'?'desc':'asc'};  /* Igal, 12 oct. : le 3e clic remettait l'ordre d'origine, « ni croissant ni décroissant, ça bloque » → on alterne seulement ; la croix de la pastille « TRI » remet l'ordre d'origine */
  sauveTRI();
  const sel=$('fo'); if(sel&&TRI) sel.value='b';
  /* Igal, 12 oct. : « au bout de 4-5 clics sur Stock c'est comme si c'était freeze ».
     Un clic de tri refaisait TOUT (reconstruire les 3 800 articles, refiltrer) alors que seul
     l'ordre change : sur un ordinateur plus lent, les clics s'empilaient. La liste déjà
     filtrée (cur) est simplement retriée, puis redessinée. */
  const tc=trieur();
  if(tc && Array.isArray(cur) && cur.length){ cur.sort(tc); shown=PAGE; paint(); }
  else render();
}


/* Seuil de stock faible. Il n'existe aucune bonne valeur universelle :
   elle depend de la vitesse d'ecoulement, qu'on ne connait pas encore.
   C'est donc a l'utilisateur de la fixer, en voyant combien de references
   son choix declenche. */
/* Reglages partages par toutes les rubriques. */
const KREG='reglages-v1';
const CANAUX_DEF=[{id:'site',nom:'Site perfumestrade.com',maj:0,com:3},
  {id:'sitegros',nom:'Site wholesale.perfumestrade.com',base:'pvw',maj:0,com:3},{id:'amazon',nom:'Amazon',maj:18,com:15},{id:'perfumecity',nom:'Perfume City',maj:0,com:3}];
const REG_DEF={seuilQte:3,capMin:0,baissePct:30,baisseJours:30,margeMin:10,canaux:CANAUX_DEF};
let REG=Object.assign({},REG_DEF);
try{ const r=JSON.parse(localStorage.getItem(KREG)||'null'); if(r) REG=Object.assign({},REG_DEF,r); }catch(e){}
/* 3 septembre : eBay quitte la liste des canaux, Perfume City arrive (une seule fois, sans toucher aux autres) */
(function(){ try{ const K='canaux-ebay-perfumecity-v1'; if(localStorage.getItem(K)) return;
  if(Array.isArray(REG.canaux)){ REG.canaux=REG.canaux.filter(c=>c.id!=='ebay');
    if(!REG.canaux.some(c=>c.id==='perfumecity')) REG.canaux.push({id:'perfumecity',nom:'Perfume City',maj:0,com:3});
    localStorage.setItem(KREG,JSON.stringify(REG)); }
  localStorage.setItem(K,'1'); }catch(e){} })();
/* reprise de l'ancien reglage isole */
try{ const v=localStorage.getItem('seuil-stock-faible-v1');
  if(v!==null && !localStorage.getItem(KREG)){ REG.seuilQte=+v;
    localStorage.setItem(KREG,JSON.stringify(REG)); localStorage.removeItem('seuil-stock-faible-v1'); }
}catch(e){}
base(KREG,REG);
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
const sauveREG=()=>ecrit(KREG,REG);
let SEUIL=REG.seuilQte;
function majSeuil(){
  const el=$('fseuiln'); if(!el) return;
  const T=tousLesArticles();
  const n=T.filter(p=>p.qte>0&&p.qte<SEUIL).length;
  const st=T.filter(p=>p.qte>0).length||1;
  const cap=T.filter(p=>p.qte>0&&p.qte<SEUIL).reduce((a,p)=>a+p.qte*(p.pa||0),0);
  el.textContent = SEUIL<=0 ? 'aucune alerte'
    : `${nf(n)} référence${n>1?'s':''} · ${Math.round(n/st*100)} % du stock · ${money(cap)}`;
}

/* ================= VUE EN LISTE =================
   Meme donnees, meme filtres, meme clic vers la fiche.
   Ordre des prix impose : achat, retail, gros. */
const KVUE='vue-catalogue-v1';
/* La LISTE est la vue par defaut. Les vignettes sont belles pour parcourir un
   catalogue qu'on decouvre ; la liste sert a travailler — on y voit d'un coup
   la quantite, les trois prix et l'etat du comptage, sans survoler chaque carte.
   Le choix reste memorise des qu'on clique sur l'autre bouton. */
let VUE='liste'; try{ VUE=localStorage.getItem(KVUE)||'liste'; }catch(e){}

/* Étiquette de comptage affichée sous la quantité, dans la liste.
   Vert avec le ✓ UNIQUEMENT quand quelqu'un a réellement compté les flacons dans SAM
   (on connaît alors qui et quand). Quand c'est le fichier d'inventaire qui l'affirme,
   sans nom ni date, l'étiquette reste grise : ce n'est pas une preuve. */
const OKICO='<svg viewBox="0 0 12 12" fill="none" aria-hidden="true"><path d="M1.8 6.4l2.7 2.8L10.2 3" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>';
function badgeComptage(p){
  const m=MOD[p.id]||{};
  const st=m.verif!==undefined?m.verif:(p.verif||'');
  if(st==='ok'){
    if(m.verifLe){
      const q=m.qteC!=null?` (${nf(m.qteC)} flacon${Math.abs(m.qteC)>1?'s':''})`:'';
      return `<span class="lvf ok" title="Compté par ${esc(m.verifPar||'?')} le ${dateFr(m.verifLe)}${q}">${OKICO}comptage vérifié</span>`;
    }
    return `<span class="lvf fic" title="C'est le fichier d'inventaire qui l'affirme : ni nom, ni date, personne n'a compté les flacons.">selon le fichier</span>`;
  }
  if(st==='doute'||st==='av') return `<span class="lvf av" title="Signalé comme à recompter">à recompter</span>`;
  return '';   /* jamais compté : pas d'étiquette. L'absence de coche verte est déjà le signal. */
}
function ligneListe(p,i){
  const CLIENT=document.body.classList.contains('client');
  const ph = p.img
    ? `<span class="lph"><img src="${phSrc(p)}" data-far="${p.imgPerso?'':p.img}" alt="" loading="lazy" onerror="secours(this)"></span>`
    : `<span class="lph"><svg viewBox="0 0 40 64" fill="none" aria-hidden="true"><rect x="14.5" y="2" width="11" height="9" rx="1.5" stroke="currentColor" stroke-width="3"/><path d="M11 20a6 6 0 016-6h6a6 6 0 016 6v34a6 6 0 01-6 6H17a6 6 0 01-6-6V20z" stroke="currentColor" stroke-width="3"/></svg></span>`;
  const meta=[p.ml?p.ml+' oz':'',p.type,GEN[p.genre]&&p.genre?GEN[p.genre]:''].filter(Boolean).join(' · ');
  const mg=(v)=>(v!=null&&p.pa!=null&&v>0)?((v-p.pa)/v*100):null;
  const cm=v=>v==null?'':v<0?'c':v<(REG.margeMin||10)?'w':'g';
  const pc=v=>v==null?'—':(v<0?'−':'')+Math.abs(v).toFixed(0)+' %';
  const prix=(v,cls,ast)=>v==null?`<span class="lna">à définir</span>`
    :`<span class="${cls}">${money(v)}${ast||''}</span>`;
  const star=p.src===1?'<span class="ast">*</span>':p.src===2?'<span class="ast bad">*</span>':'';
  const mq=manque(p);
  /* Toutes les alertes sont ecrites en toutes lettres, la plus grave en premier
     (demande d'Igal : pas de « +1 »). La ligne s'allonge si besoin. */
  let alertes='';
  if(!CLIENT){
    const l=[];
    p.an.forEach(a=>l.push({t:AN[a][0],c:AN[a][1]}));
    if(mq.length) l.push({t:`${mq.length} champ${mq.length>1?'s':''} à compléter`,c:'w'});
    if(p.neuf) l.push({t:'ajouté à la main',c:'todo'});
    { const d=pastilleDiff(p); if(d) l.unshift(d); }
    /* les alertes de prix restent dans l'ordre des colonnes ; les « à compléter » et « ajouté » en dernier */
    const rang=x=>(x.c==='todo'||/à compléter$/.test(x.t))?1:0;
    l.sort((a,b)=>rang(a)-rang(b));
    if(l.length){
      alertes=`<div class="lfl">${l.map(x=>`<span class="fl ${x.c}">${x.t}</span>`).join('')}</div>`;
    }
  }
  const cls=CLIENT?'':(p.an.some(a=>[1,2,3,8].includes(a))?'alert':p.an.length?'warn':'');
  return `<tr class="${cls}" data-id="${p.id}" tabindex="0">
    <td class="lno">${nf((i||0)+1)}</td>
    <td><div class="lid">${ph}<div class="tx">
      <div class="lmq">${esc(p.marque)}${badgeAmazon(p)}</div>
      <div class="lnm">${esc(p.nom)}</div>${meta?`<div class="lsub">${meta}</div>`:''}${p.bc?`<div class="lbn" data-nolang>${esc(p.bc)}</div>`:''}${CLIENT?'':`<div class="dfrow">${logosDiff(p)}</div>`}</div></div></td>
    <td class="colfmt"><span class="lmeta">${meta||'—'}</span></td>
    <td class="r colq"><span class="lq${p.qte===0?' out':(SEUIL>0&&p.qte<SEUIL)?' low':''}">${p.qte===0?'historique':nf(p.qte)}</span>${p.qte===0?'':badgeComptage(p)}</td>
    <td class="r colsite">${siteCell(p)}</td>
    <td class="r colpa">${prix(p.pa,'lpa')}</td>
    <td class="r colpvr">${prix(p.pvr,'lpr',star)}</td>
    <td class="r colaz">${azCell(p)}</td>
    <td class="r">${prix(p.pvw,'lpw')}</td>
    <td class="r colmg colmgr"><span class="lmg ${cm(mg(p.pvr))}">${pc(mg(p.pvr))}</span></td>
    <td class="r colmg"><span class="lmg ${cm(mg(p.pvw))}">${pc(mg(p.pvw))}</span></td>
    <td class="colfl">${alertes}</td>
    <td class="colbc"><span class="lbc">${p.bc||'—'}</span></td>
  </tr>`;
}

function peintListe(){
  const th=COLS.map(c=>{
    const on = TRI&&TRI.col===c.k;
    const fl = on ? (TRI.dir==='asc'?'▲':'▼') : '';
    const titre = on
      ? (TRI.dir==='asc'?'Croissant — cliquer pour inverser':'Décroissant — cliquer pour inverser')
      : (c.t==='txt'?'Trier de A à Z':'Trier du plus grand au plus petit');
    return `<th class="${[c.al,c.cls,'so',on?'on':''].filter(Boolean).join(' ')}"
      data-col="${c.k}" title="${titre}" tabindex="0" role="button"
      aria-sort="${on?(TRI.dir==='asc'?'ascending':'descending'):'none'}"
      ><span>${c.lib.replace(/ (R|G)$/,'&nbsp;$1')}<i>${fl||'⇅'}</i></span></th>`;
  }).join('');
  $('lstw').innerHTML=`<table class="lst"><thead><tr><th class="lno">N°</th>${th}</tr></thead>
    <tbody>${cur.slice(0,shown).map((p,i)=>ligneListe(p,i)).join('')}</tbody></table>`;
}

function majVue(){
  const liste = VUE==='liste';
  $('grid').style.display = liste?'none':'';
  $('lstw').style.display = liste?'':'none';
  requestAnimationFrame(ajusteDefile);
  document.querySelectorAll('#vue button').forEach(b=>b.classList.toggle('on',b.dataset.vue===VUE));
}
document.getElementById('vue').addEventListener('click',e=>{
  const b=e.target.closest('[data-vue]'); if(!b) return;
  VUE=b.dataset.vue; try{ localStorage.setItem(KVUE,VUE); }catch(x){}
  majVue(); paint();
});
/* le tableau dépasse-t-il sa boîte ? alors elle défile (en-tête plus figé, mais rien ne sort du cadre) */
function ajusteDefile(){ const w=$('lstw'), t=w&&w.querySelector('.lst'); if(!t||!w.clientWidth) return;
  if(ajusteDefile.en) return; ajusteDefile.en=true;
  try{
    const trop=()=>t.scrollWidth>w.clientWidth+1;
    w.classList.remove('defile','x1','x2','x3','x4');
    for(let i=1;i<=4&&trop();i++) w.classList.add('x'+i);
    w.classList.toggle('defile', trop());
  } finally { setTimeout(()=>{ ajusteDefile.en=false; },0); }
}
window.addEventListener('resize',ajusteDefile);
/* Le tableau change de largeur APRÈS le premier calcul : la traduction (anglais,
   espagnol) allonge les en-têtes, les photos arrivent, les polices se chargent.
   Un seul calcul au dessin laissait la colonne Alertes sortir du cadre en anglais
   (Igal, 24 sept. 2026 : « tu me refais ça à chaque fois »). On surveille donc la
   taille réelle du tableau, et on recalcule à chaque changement. */
try{ const RO=new ResizeObserver(()=>ajusteDefile()); const ob=()=>{ const t=$('lstw')&&$('lstw').querySelector('.lst'); if(t&&t!==ob.t){ ob.t=t; RO.observe(t); } };
  new MutationObserver(ob).observe($('lstw'),{childList:true}); RO.observe($('lstw')); ob(); }catch(e){}
$('lstw').addEventListener('click',e=>{
  const th=e.target.closest('th[data-col]');
  if(th){ bascule(th.dataset.col); return; }
  const tr=e.target.closest('tr[data-id]'); if(tr) ouvreFiche(tr.dataset.id);
});
$('lstw').addEventListener('keydown',e=>{
  if(e.key!=='Enter'&&e.key!==' ') return;
  const th=e.target.closest('th[data-col]');
  if(th){ e.preventDefault(); bascule(th.dataset.col); return; }
  const tr=e.target.closest('tr[data-id]'); if(tr){ e.preventDefault(); ouvreFiche(tr.dataset.id); }
});

function paint(){
 if(VUE==='liste'){ peintListe(); $('grid').innerHTML=''; }
 else $('grid').innerHTML=cur.slice(0,shown).map(card).join('');
 $('more').style.display=cur.length>shown?'block':'none';
 $('more').textContent=`Afficher plus (${(cur.length-shown).toLocaleString('fr-FR')} restants)`;
 majVide();
 const u=cur.reduce((a,p)=>a+p.qte,0);
 $('cnt').textContent=`${cur.length.toLocaleString('fr-FR')} réf. · ${u.toLocaleString('fr-FR')} unités`;
 majBarre(); majSeuil(); majMel();
 const ex=$('exa'); if(ex){ const nm=Object.keys(MOD).length, n=AJ.length+nm;
   ex.style.display=n?'inline-block':'none';
   ex.textContent=`Exporter mes corrections (${n})`;
   ex.title=`Télécharge un tableau des ${AJ.length} article(s) ajouté(s) et ${nm} fiche(s) corrigée(s), `
     +`avec le détail de ce qui a changé, pour le reporter dans le fichier Excel maître. `
     +`Ce n'est pas une sauvegarde : pour ça, utilise « Sauvegarder mon travail ».`;
   ex.onclick=exporteAjouts; }
}
function majVide(){
  const el=$('empty');
  if(cur.length){ el.style.display='none'; return; }
  el.style.display='block';
  const st=$('fs').value;
  const ail=AILLEURS.length;
  const q=$('q').value.trim();
  if(st==='az'){
    el.innerHTML=`<b>${q?'Aucun parfum vendu sur Amazon ne correspond à « '+esc(q)+' ».':'Aucun parfum n\'est marqué comme vendu sur Amazon.'}</b>
      <span>Un parfum compte comme vendu sur Amazon quand il a une vente Amazon enregistrée.</span>
      ${ail?`<button class="btn pri" id="vvoir">Voir ${ail>1?'les '+ail+' références':'la référence'} hors Amazon</button>`:''}`;
    if(ail) $('vvoir').onclick=()=>{ $('fs').value=''; SEG.querySelectorAll('button').forEach(x=>x.classList.toggle('on',x.dataset.v==='')); render(); };
    return;
  }
  if(st==='sp'){
    el.innerHTML=`<b>${q?'Aucun produit sans prix ne correspond à « '+esc(q)+' ».':'Aucun produit sans prix sur ce site.'}</b>
      <span>Un produit compte comme sans prix quand sa fiche est retirée de la vente faute de prix, ou quand le site n'affiche aucun prix.</span>`;
    return;
  }
  if(ail && st){
    const ou = st==='in' ? "en historique (plus de stock)" : "en stock";
    const vers = st==='in' ? '' : 'in';
    el.innerHTML=`<b>${ail} référence${ail>1?'s':''} correspond${ail>1?'ent':''} — mais ${ail>1?'elles sont':'elle est'} ${ou}.</b>
      <span>Le catalogue n'affiche que ${st==='in'?'le stock disponible':"l'historique"} pour l'instant.</span>
      <button class="btn pri" id="vvoir">${ail>1?'Les':'La'} voir</button>`;
    $('vvoir').onclick=()=>{ $('fs').value=vers; render(); };
    return;
  }
  const nAutres=['fb','fg','ft','fp','fa','fan','fx','fd'].filter(i=>{
    const e=$(i); return e.type==='checkbox'?e.checked:!!e.value; }).length;
  if(ail===0 && q && nAutres){
    el.innerHTML=`<b>Aucune référence ne correspond à « ${esc(q)} » avec les filtres actuels.</b>
      <span>${nAutres} filtre${nAutres>1?'s sont actifs':' est actif'} en plus de la recherche.</span>
      <button class="btn pri" id="vraz">Enlever les filtres, garder la recherche</button>`;
    $('vraz').onclick=()=>{ ['fb','fg','ft','fp','fan','fx','fd'].forEach(i=>$(i).value='');
      $('fa').checked=false; $('fs').value=''; render(); };
    return;
  }
  if(q){
    /* les deux nombres se recalculent : après une vente ou un comptage,
       la phrase reste vraie */
    const T=tousLesArticles();
    el.innerHTML=`<b>« ${esc(q)} » n'est nulle part dans le fichier.</b>
      <span>Ni dans les ${nf(T.filter(x=>x.qte>0).length)} références en stock,
      ni dans les ${nf(T.filter(x=>x.qte===0).length)} en historique.
      Si le produit existe vraiment, il n'a jamais été saisi — le bouton
      <b>+ Nouvel article</b> permet de le créer.</span>`;
    return;
  }
  el.innerHTML=`<b>Aucun produit ne correspond à ces filtres.</b>
    <span>Enlève-en un pour élargir.</span>`;
}
/* La recherche (réécrite le 9 oct. 2026 — Igal : « la barre de recherche du catalogue déconne »).
   Trois défauts : « chloe » ne trouvait pas « Chloé » (accents) ; « jadore » ne trouvait pas
   « J'adore » (apostrophe) ; et « le male » ramenait « Animale » avant le vrai Le Male, parce qu'un
   mot était cherché n'importe où DANS un autre et que la liste restait rangée par marque.
   Maintenant : sans accents ni ponctuation ; chaque mot tapé doit COMMENCER un mot de la fiche
   (les suites de chiffres de 3 et plus se cherchent n'importe où : codes-barres, « 212 ») ; et
   quand on cherche, les fiches qui contiennent la phrase tapée passent en premier. */
/* 11 oct. 2026 (Igal : « j'ai tapé le nom en entier, il me dit qu'il n'y en a pas ») :
   - « 3oz » et « 3 oz », « 100ml » et « 100 ml » doivent se trouver : un espace est glissé entre
     chiffres et lettres des deux côtés ;
   - le type (EDP, EDT…), la contenance et le genre font partie du texte cherché : un nom repris
     d'une facture ou du site (« Lattafa Yara EDP 3.4 oz Women ») les contient toujours. */
function rNorm(s){ return String(s==null?'':s).toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g,'').replace(/œ/g,'oe').replace(/æ/g,'ae')
  .replace(/(\d)([a-z])/g,'$1 $2').replace(/([a-z])(\d)/g,'$1 $2'); }
function rVar(s){ const n=rNorm(s);
  return [' '+n.replace(/['’`´]/g,'').replace(/[^a-z0-9.]+/g,' ').trim()+' ', ' '+n.replace(/[^a-z0-9.]+/g,' ').trim()+' ']; }
function rTexte(p){
  const GG={M:'homme men man for him',W:'femme women woman for her',U:'unisexe unisex mixte',K:'enfant kids'}[p.genre]||'';
  const k=p.nom+'|'+p.nomSrc+'|'+p.marque+'|'+p.bc+'|'+(p.bcs||'')+'|'+(p.type||'')+'|'+(p.ml||'')+'|'+(p.genre||'');
  /* la contenance est en oz dans l'outil ; les sites et les factures la disent souvent en ml */
  const ml=p.ml?Math.round(+String(p.ml).replace(',','.')*29.5735/5)*5:0;
  if(p.__rqk!==k){ p.__rqk=k; p.__rq=rVar(p.nom+' '+p.nomSrc+' '+p.marque+' '+p.bc+' '+(p.bcs||'')+' '+(p.type||'')+' '+(p.ml?p.ml+' oz '+p.ml+' fl oz '+(ml?ml+' ml':''):'')+' '+GG); }
  return p.__rq;
}
function rMot(t,m){ return (/^\d{3,}$/.test(m)?t.includes(m):t.includes(' '+m)); }
/* les sigles que tout le monde tape : « ysl » doit trouver Yves Saint Laurent */
const R_SIGLES={ysl:'yves saint laurent',jpg:'jean paul gaultier',dg:'dolce gabbana',ch:'carolina herrera',ck:'calvin klein',
  mfk:'maison francis kurkdjian',tf:'tom ford',bulgari:'bvlgari',paco:'paco rabanne',armani:'armani',vs:'victoria secret',
  jlo:'jennifer lopez',ysl2:'yves saint laurent',edp:'edp',edt:'edt',edc:'edc',parfum:'parfum',oz:'oz',ml:'ml'};
function rQuery(q){ const Q=rVar(q).map(v=>v.trim().split(' ').filter(Boolean).flatMap(m=>(R_SIGLES[m]&&R_SIGLES[m]!==m)?R_SIGLES[m].split(' '):[m]));
  return Q; }
/* « Bleu de Chanel » : la fiche s'appelle « Chanel Bleu » — les petits mots (de, du, of, the…)
   ne servent pas à trouver, tant qu'il reste d'autres mots tapés */
const R_PETITS=new Set(['de','du','des','la','les','of','the','by','pour','for','and','et']);
function rUtiles(L){ const u=L.filter(m=>!R_PETITS.has(m)); return u.length?u:L; }
function qMots(Q,p){ const T=rTexte(p), A=rUtiles(Q[0]), B=rUtiles(Q[1]);
  return (A.length>0&&A.every(m=>rMot(T[0],m))) || (B.length>0&&B.every(m=>rMot(T[1],m))); }
/* le rang d'une fiche pour la phrase tapée : plus haut = plus haut dans la liste */
function rScore(Q,p){
  const nom=rVar(p.nom), mq=rVar(p.marque), ph=Q[1].join(' '), m1=Q[1][0]||'';
  const complet=rVar(p.marque+' '+p.nom)[1];
  let sc=0;
  if(String(p.bc)===Q[1].join('')||(p.bcs||'').split(/\s+/).includes(Q[1].join(''))) sc+=10;
  if(complet.includes(' '+ph+' ')||complet.includes(' '+ph)) sc+=4;
  if(nom[1].startsWith(' '+m1)) sc+=2;
  if(mq[1].startsWith(' '+m1)) sc+=1;
  /* la marque enlevée des mots tapés, le premier mot qui reste doit ouvrir le nom :
     « dior sauvage » met Sauvage avant Eau Sauvage */
  const mqMots=new Set(mq[1].trim().split(' ')), reste=Q[1].filter(m=>!mqMots.has(m));
  if(reste.length&&nom[1].startsWith(' '+reste[0])) sc+=3;
  return sc;
}
function render(){ mesureBarre();
 const TOUS=tousLesArticles();
 const q=$('q').value.trim().toLowerCase(),QQ=q?rQuery(q):null,b=$('fb').value,g=$('fg').value,t=$('ft').value,st=$('fs').value,
  fx=$('fx').value, fd=$('fd').value,
  ph=$('fp').value,ast=$('fa').checked,an=$('fan').value,o=$('fo').value;
 majDiff(); const critere=p=>(fx==='retire'?!!p.masque:(!p.masque&&(!fx||(fx==='neuf'?!!p.neuf:fx==='mod'?!!p.mod:manque(p).length>0))))&&
  (!b||p.marque===b)&&(!g||p.genre===g)&&(!t||p.type===t)&&(ph===''||(ph==='1'?!!p.img:!p.img))&&
  (!ast||p.src>0)&&(!an||(an==='all'?p.an.length>0:p.an.includes(+an)))&&
  (!QQ||qMots(QQ,p))&&(!fd||diffOk(p,fd));
 /* Ce que la recherche trouverait SANS le filtre de stock : sert à expliquer
    une liste vide au lieu de laisser croire que le produit n'existe pas. */
 AILLEURS=TOUS.filter(critere);
 /* 12 oct. 2026 (Igal : « un onglet produits vendus sur Amazon ») : l'onglet « Vendus sur Amazon » montre les parfums
    vendus là-bas, en stock ou non (le stock reste affiché sur chaque fiche) */
 const spSite=$('fsp').value, spStock=$('fspq').checked;
 $('spwrap').hidden=(st!=='sp');
 cur=AILLEURS.filter(p=>st==='az'?venduAmazon(p):st==='sp'?(sansPrixSite(p,spSite)&&(!spStock||p.qte>0)):(!st||(st==='in'?p.qte>0:p.qte===0)));
 /* Taper un code-barres, c'est demander CE parfum — pas « ce parfum s'il me
    reste du stock ». Igal a cherché 8011003861224, l'écran est resté vide, et
    il a fallu cliquer sur « La voir » pour comprendre que la référence existait
    mais était à zéro. Quand la recherche est un code-barres et qu'elle ne trouve
    rien à cause du seul filtre de stock, on montre quand même la référence. */
 if(!cur.length && AILLEURS.length && st && st!=='az' && st!=='sp' && /^\s*\d{4,}\s*$/.test($('q').value)) cur=AILLEURS.slice();
 /* 28 sept. (Igal) : une vente Amazon de Hanae Mori Blue Butterfly, et la recherche par le
    NOM ne la trouvait pas — elle est à 0 en stock et le filtre « en stock » la cachait.
    Chercher, c'est chercher partout : avec un texte tapé, le filtre « en stock » ne cache
    plus rien (le filtre « hors stock », choisi exprès, reste respecté). */
 if(q && st==='in' && AILLEURS.length>cur.length) cur=AILLEURS.slice();
 const tc=trieur();
 if(tc) cur.sort(tc);
 else if(o==='q')cur.sort((a,b)=>b.qte-a.qte);
 else if(o==='p')cur.sort((a,b)=>(a.pvw??1e9)-(b.pvw??1e9));
 else if(QQ&&o==='b'){ cur.forEach(p=>{ p.__sc=rScore(QQ,p); });
   cur.sort((a,b)=>(b.__sc-a.__sc)||a.marque.localeCompare(b.marque,'fr')||a.nom.localeCompare(b.nom,'fr')); }
 else cur.sort((a,b)=>a.marque.localeCompare(b.marque,'fr')||a.nom.localeCompare(b.nom,'fr'));
 shown=PAGE; paint();
}
$('more').addEventListener('click',()=>{shown+=PAGE;paint();});
$('fc').addEventListener('input',()=>{document.body.classList.toggle('client',$('fc').checked);render();});
['q','fs','fx','fd','fb','fg','ft','fp','fa','fan','fsp','fspq'].forEach(i=>$(i).addEventListener('input',render));
$('fo').addEventListener('input',()=>{ TRI=null; sauveTRI(); render(); });



/* ================= FICHE PRODUIT ================= */
/* ================= QUI FAIT QUOI, ET QUAND =================
   Un fichier ouvert en local n'a pas de serveur : personne ne peut être
   authentifié. Le journal enregistre donc un nom DÉCLARÉ, pas un nom prouvé.
   Pour une équipe de deux ou trois, ça répond à « qui a changé ce prix ».
   Ça ne vaut pas preuve. */
const KUSR='crm-utilisateur-v1', KJOU='crm-journal-v1';
let USR=NOM_UTIL;
let JOU=lit(KJOU,[]); if(!Array.isArray(JOU)) JOU=base(KJOU,[]);
const sauveJOU=()=>ecrit(KJOU,JOU);

/* Aucune fenetre a l'enregistrement : le nom se regle une fois dans la barre laterale
   (« Indiquer qui tu es »), et chacun aura son propre acces avec le serveur. */
/* Le nom de la personne, exigé avant toute écriture. « force » rouvre la fenêtre
   pour en changer ; sinon, elle ne s'ouvre que si personne n'est identifié. */
function demandeUser(force,action,apres){
  if(force){ fenetreNom('',apres); return USR; }
  if(USR) return USR;
  return signe(action||'', apres||(()=>{}));
}
window.__nomChange.push(v=>{ USR=v; try{ majUser(); }catch(e){} });
function majUser(){ try{ piedSession(); }catch(e){} }

/* act : 'prix' | 'stock' | 'fiche' | 'verif' | 'fournisseur' | 'import' | 'creation' */
function log(e){
  JOU.push(Object.assign({t:new Date().toISOString(),u:USR||'(non renseigné)'},e));
  sauveJOU();
}
const LIBV={ok:'comptage vérifié',non:'jamais compté',av:'à vérifier','':'inconnu'};
const dateFr=iso=>{ const d=new Date(iso); return d.toLocaleDateString((typeof lgLocale==='function'?lgLocale():'fr-FR'),{timeZone:'America/New_York',day:'numeric',month:'long'})
  +(typeof L3==='function'?L3(' à ',' at ',' a las '):' à ')+d.toLocaleTimeString('fr-FR',{timeZone:'America/New_York',hour:'2-digit',minute:'2-digit'}); };
const LIBCH={pa:"prix d'achat",pvw:'prix de gros',pvr:'prix retail',qte:'quantité en stock',
  bc:'code-barres',bcs:'autres codes-barres',nom:'nom',ml:'contenance',marque:'marque',type:'type',genre:'genre'};
/* les autres codes-barres d'une fiche, sous forme de liste propre */
const bcsDe=p=>String(p&&p.bcs||'').split(/[^0-9]+/).map(x=>x.replace(/^0+/,'')).filter(x=>x.length>=6);
const CATCH={pa:'prix',pvw:'prix',pvr:'prix',qte:'stock'};

const KMOD='fiches-modifiees-v1';
let MOD=lit(KMOD,{}); if(!MOD||typeof MOD!=='object'||Array.isArray(MOD)) MOD=base(KMOD,{});
const sauveMOD=()=>ecrit(KMOD,MOD);
/* L'identifiant d'une fiche est son CODE-BARRES, jamais sa position dans le fichier.
   Sinon, le jour où l'inventaire est remplacé par une version à jour — lignes ajoutées,
   supprimées, réordonnées — toutes les corrections saisies se rattacheraient au mauvais
   produit. Avec le code-barres, elles suivent le produit d'un fichier à l'autre. */
P.forEach(p=>p.id = p.cle);

/* Reprise des données saisies sous les anciens identifiants :
   'p<numéro de ligne>' au tout début, puis 'b<code-barres>' — ce dernier ne
   distinguait pas les 11 paires qui partagent un code-barres ni les 74 lignes
   qui n'en ont pas. */
(function migre(){
  let n=0, perdus=0;
  Object.keys(MOD).filter(k=>/^p\d+$/.test(k)).forEach(k=>{
    const p=P[+k.slice(1)];
    if(p && !MOD[p.id]){ MOD[p.id]=MOD[k]; n++; }
    delete MOD[k];
  });
  Object.keys(MOD).filter(k=>/^b[0-9]+$/.test(k)).forEach(k=>{
    if(P.some(p=>p.id===k)) return;                 // clé encore valable
    const bc=k.slice(1), c=P.filter(p=>p.bc===bc);
    if(c.length===1 && !MOD[c[0].id]){ MOD[c[0].id]=MOD[k]; n++; }
    else perdus++;                                  // ambigu : on ne devine pas
    delete MOD[k];
  });
  if(MOD['bNaN']){ delete MOD['bNaN']; perdus++; }
  if(n||perdus){ sauveMOD();
    console.info('Fiches rattachées : '+n+(perdus?' · '+perdus+' non rattachables (code-barres ambigu)':'')); }
})();

function calcAn(p){
  const an=[], pa=p.pa, pvr=p.pvr, pvw=p.pvw;
  if(pa!=null){
    if(pvw!=null&&pvw<=pa) an.push(1);
    if(pvr!=null&&pvr<=pa) an.push(2);
    if(pvw!=null&&pvw>pa&&(pvw-pa)/pvw*100<10) an.push(4);
    if(pvw!=null&&(pvw-pa)/pvw*100>60) an.push(5);
    if(pvr!=null&&pvr>3*pa) an.push(6);
  }
  if(pvw!=null&&pvr!=null){ if(pvw>pvr) an.push(3); if(pvw===pvr) an.push(9); }
  if(pvw==null) an.push(7);
  if(pvr==null) an.push(8);
  return triAn(an);
}
function applique(p){
  const m=MOD[p.id]; if(!m) return p;
  const o=Object.assign({},p,m); o.an=calcAn(o); o.mod=true; return o;
}

let FICHE=null;
let AILLEURS=[];
const NUM=new Set(['qte','pa','pvr','pvw']);
/* --- prix par canal : regle (retail + majoration) ou valeur manuelle --- */
const r2=v=>Math.round(v*100)/100;
const money2=v=>_usd(v,2);
/* Logo d'un canal : le fichier logos/<id>.png ou .svg s'il existe dans le dossier, sinon une pastille avec le nom.
   Les logos sont des marques deposees : ils ne sont pas fournis, c'est a lui de deposer les fichiers officiels. */
/* Les logos déposés dans logos/ au moment de la génération sont incorporés dans la page :
   ils s'affichent même si le fichier est ouvert depuis un autre dossier (Téléchargements, clé USB…). */
const LOGOS_EMB=__LOGOS__;
const logo=(id,nom)=>LOGOS_EMB[id]?`<span class="lg lg-${esc(id)}"><img src="${LOGOS_EMB[id]}" alt="${esc(nom)}"></span>`
 :`<span class="lg lg-${esc(id)}"><img src="logos/${esc(id)}.png" alt="${esc(nom)}" onerror="this.onerror=null;this.src='logos/${esc(id)}.svg';this.onerror=function(){this.replaceWith(document.createTextNode('${esc(nom).replace(/'/g,"\\'")}'))}"></span>`;
const pct1=v=>v==null?'—':(v>=0?'':'−')+Math.abs(v).toFixed(1).replace('.',',')+' %';
const canaux=()=>(Array.isArray(REG.canaux)&&REG.canaux.length)?REG.canaux:CANAUX_DEF;
/* Un parfum n'est pas forcément vendu partout : on peut couper un canal pour ce produit-là.
   La liste des canaux coupés vit dans la fiche (pcOff), comme les prix manuels. */
const horsCanal=(p,id)=>Array.isArray(p.pcOff)&&p.pcOff.includes(id);
function offCour(){ const b=FICHE&&FICHE.brouillon; if(b&&b.pcOff) return b.pcOff;
  const base=cur[FICHE.pos]; return Array.isArray(base.pcOff)?base.pcOff:[]; }
/* Le prix de l'annonce Amazon de Sam (rapport des annonces importé dans le cockpit, 11 oct. 2026) :
   rangé par code-barres et par ASIN dans amazon-prix-v1. */
function prixAmazonDe(p){
  let A=null; try{ A=lit('amazon-prix-v1',null); }catch(e){ A=null; }
  if(!A||typeof A!=='object') return null;
  const ks=[p.bc].concat(String(p.bcs||'').split(/[\s,;]+/)).concat([p.asin]).filter(Boolean);
  for(const k of ks){ const e=A[k]; if(e&&e.prix>0) return Object.assign({le:A._le||''},e); }
  return null;
}
/* Le prix de Perfume City sur Shopify (15 oct. 2026, Igal : « je veux modifier sur la fiche produit le site Perfume City
   qui est sur Shopify »). Le cockpit relit toute la boutique chaque heure et range, par code-barres sans zéro de tête :
   [id produit, id variante, prix, prix barré, actif]. Un code porté par deux produits sur Shopify (_amb) n'est jamais
   proposé à la modification : on ne devine pas lequel changer. */
const PCSHOP_OVR={};   /* ce que Shopify vient de répondre à un envoi, avant que la relève du serveur ne le rapporte */
function prixShopifyDe(p){
  let S=null; try{ S=lit('shopify-pc-prix-v1',null); }catch(e){ S=null; }
  if(!S||typeof S!=='object') return null;
  const s0=x=>String(x||'').replace(/[^0-9A-Za-z]/g,'').replace(/^0+/,'');
  const ks=[p.bc].concat(String(p.bcs||'').split(/[\s,;]+/)).map(s0).filter(Boolean);
  for(const k of ks){ const e=S[k]; if(Array.isArray(e)&&e[2]>0)
    return {k,prix:PCSHOP_OVR[k]!=null?PCSHOP_OVR[k]:e[2],barre:e[3],actif:e[4]===1,le:S._t||'',pid:e[0],handle:e[5]||'',boutique:S._b||''}; }
  for(const k of ks) if((S._amb||[]).includes(k)) return {amb:true,k};
  return null;
}
function prixCanal(p,c){
  const o=(p.pc||{})[c.id];
  if(o!=null&&o!=='') return {v:+o,man:true,src:'man'};
  /* Amazon : le prix de l'annonce de Sam, c'est LE prix (Igal, 11 oct. 2026) */
  if(c.id==='amazon'){ const az=prixAmazonDe(p); if(az) return {v:az.prix,man:false,src:'amazon'}; }
  /* Perfume City : le prix affiché sur Shopify, c'est LE prix (15 oct. 2026) */
  if(c.id==='perfumecity'){ const sh=prixShopifyDe(p); if(sh&&sh.prix) return {v:sh.prix,man:false,src:'shopify'}; }
  /* le site de gros vend au prix de gros, pas au retail */
  const b=c.base==='pvw'?p.pvw:p.pvr;
  if(b!=null&&b>0) return {v:r2(b*(1+(c.maj||0)/100)),man:false,src:'calc'};
  return {v:null,man:false,src:'rien'};
}
/* Igal, 17 oct. 2026 : « dans la ligne des canaux de vente, un lien qui m'amène directement sur CE parfum, sur cette boutique »
   — pour vérifier sur la boutique que le prix a bien bougé, sans aller le chercher à la main. Les deux sites WooCommerce :
   la page publique du produit (WordPress renvoie « ?p=numéro » vers l'adresse définitive). Perfume City : la page publique sur
   Shopify quand on connaît le « handle » du produit, sinon sa page d'administration. Pas de lien quand le parfum n'est pas sur la boutique. */
function lienCanal(p,c,info){
  const cote=COTE_SITE[c.id];
  if(cote){
    const e=siteDe(p); let f=e&&e[cote], brouillon=false;
    /* 21 oct. 2026 (Igal : « il n'y a pas le lien "voir sur le site" » sur Coach Floral, retirée de la vente) : une fiche en brouillon/retirée
       a elle aussi un numéro sur le site — le lien ouvre son APERÇU, que WordPress montre à une personne connectée à l'administration du site. */
    if(!f||f.id==null||f.id===''){ const rr=retireCote(p,cote); f=rr&&rr.f; brouillon=true; }
    if(!f||f.id==null||f.id==='') return null;
    const B=(SITE&&SITE._base&&typeof SITE._base==='object')?SITE._base:{};
    const b=String(B[cote]||(cote==='g'?'https://wholesale.perfumestrade.com':'https://perfumestrade.com')).replace(/\/+$/,'');
    if(info&&brouillon) info.brouillon=true;
    return b+'/?post_type=product&p='+encodeURIComponent(f.id)+(brouillon?'&preview=true':'');
  }
  if(c.id==='perfumecity'){
    const sh=prixShopifyDe(p); if(!sh||sh.amb||!sh.boutique) return null;
    /* un brouillon Shopify n'a pas de page publique : on ouvre sa page d'administration, qui le montre */
    if(!sh.actif&&sh.pid){ if(info) info.brouillon=true; return 'https://admin.shopify.com/store/'+encodeURIComponent(sh.boutique.replace(/\.myshopify\.com$/,''))+'/products/'+encodeURIComponent(sh.pid); }
    if(sh.handle) return 'https://'+sh.boutique+'/products/'+encodeURIComponent(sh.handle);
    if(sh.pid) return 'https://admin.shopify.com/store/'+encodeURIComponent(sh.boutique.replace(/\.myshopify\.com$/,''))+'/products/'+encodeURIComponent(sh.pid);
  }
  return null;
}
/* Ce que la case dit d'elle-même, en une ligne : d'où vient ce prix. */
function sourcePrix(p,c,man,src){
  if(man) return 'saisi à la main';
  if(src==='amazon') return 'le prix de ton annonce Amazon';
  if(src==='shopify') return 'le prix de Perfume City sur Shopify';
  const gros=c.base==='pvw', b=gros?p.pvw:p.pvr, nomB=gros?'prix de gros':'prix retail';
  if(b==null) return (gros?'pas de prix de gros':'pas de prix retail')+' : saisis-le';
  return c.maj?`${nomB} ${money(b)} + ${c.maj} %`:`= le ${nomB}`;
}
/* ---- Le prix affiché SUR LE SITE, et l'envoi (24 sept. 2026) ----
   Igal : « au lieu de 64 je mets 63, et ça le modifie directement sur le site ;
   seul Sam, en tant que dirigeant, peut le faire ». Pour les deux sites
   WooCommerce seulement. Rien ne part tout seul : le bouton montre le prix
   exact qui va partir, et le cockpit relit la fiche du site juste avant
   d'écrire (si quelqu'un l'a changée entre-temps, il refuse). */
const COTE_SITE={site:'d',sitegros:'g'};
/* 4 nov. 2026 (Sam : « il l'a mis à 81, il est à 81 sur le site, mais sur le Catalogue il reste à 88 ») : le prix tapé dans la
   case du site partait bien sur le site, et l'outil le gardait comme « prix manuel du canal » (pc), mais le prix RETAIL (ou de GROS)
   du Catalogue, celui des listes, des marges et des price lists, restait l'ancien. Désormais le prix payé sur le site devient LE prix
   de l'outil : retail pour perfumestrade.com, gros pour le site de gros (la règle d'Igal du 9 oct. : le prix payé sur le site est
   celui de l'outil). Les autres canaux (Perfume City) gardent leur prix par canal. */
function alignePrixOutil(base,cid,v){
  const id=base.id, m=MOD[id]=MOD[id]||{};
  const k=cid==='site'?'pvr':cid==='sitegros'?'pvw':null;
  if(!k||!(+v>0)){ m.pc=Object.assign({},m.pc||{},{[cid]:v}); sauveMOD(); return; }
  const c=canaux().find(x=>x.id===cid)||{}; const b=r2(+v/(1+(c.maj||0)/100));
  const av=m[k]!=null?m[k]:base[k];
  m[k]=b;
  if(m.pc){ delete m.pc[cid]; if(!Object.keys(m.pc).length) delete m.pc; }
  sauveMOD();
  if(av!=null&&Math.abs(+av-b)>=0.005) log({act:'prix',champ:k,lib:LIBCH[k]||k,bc:base.bc,ref:(base.marque||'')+' '+(base.nom||''),av:av,ap:b});
}
/* une seule fois, par Sam ou Igal : les prix déjà changés sur les sites avant ce correctif (prix « manuel » du canal site / gros)
   deviennent le prix retail / gros du Catalogue */
function alignePrixAnciens(){
  try{
    /* 9 nov. 2026 : à chaque ouverture (Patron, admin), un prix « manuel » resté sur un site devient le prix du Catalogue */
    if(!peutPrixSite()) return;
    let n=0;
    Object.keys(MOD).forEach(id=>{ const m=MOD[id]; if(!m||!m.pc||typeof m.pc!=='object') return;
      [['site','pvr'],['sitegros','pvw']].forEach(([cid,k])=>{ const v=m.pc[cid]; if(v==null||v===''||!(+v>0)) return;
        const c=canaux().find(x=>x.id===cid)||{}; m[k]=r2(+v/(1+(c.maj||0)/100)); delete m.pc[cid]; n++; });
      if(m.pc&&!Object.keys(m.pc).length) delete m.pc; });
    if(REG.prixAligne!==2){ REG.prixAligne=2; sauveREG(); }
    if(n){ sauveMOD(); log({act:'prix',lib:'prix retail / gros du Catalogue alignés sur les prix payés sur les sites ('+n+')',bc:'',ref:'',av:null,ap:null}); }
  }catch(e){ try{ console.warn('alignement des prix',e); }catch(_){} }
}
const peutPrixSite=()=>{ try{ const s=session(); return !!(s&&['patron','admin'].includes(s.role)); }catch(e){ return false; } };
function surSite(p,c,v){
  const cote=COTE_SITE[c.id]; if(!cote) return '';
  const e=siteDe(p), f=e&&e[cote];
  if(!f){
    /* 12 oct. 2026 (Sam ne pouvait pas mettre de prix sur « Boss The Scent - Tester ») : une fiche retirée de la vente
       (brouillon, faute de prix) n'avait AUCUNE case. Maintenant : un prix, et elle repasse en vente avec lui. */
    const rf=retireCote(p,cote);
    if(rf){
      const ecritR=peutPrixSite()&&typeof CK_URL!=='undefined'&&typeof ckTok==='function'&&ckTok();
      if(!ecritR) return `<span class="ss no">retirée de la vente (aucun prix sur le site)</span>`;
      /* 12 oct. 2026 (Igal : « quand je reviens sur un produit modifié avec Sam, il ne tient pas compte des modifs ») : Sam règle le
         prix de gros dans l'outil (v), mais le site n'en a aucun : la case restait VIDE. Elle propose maintenant le prix de l'outil. */
      /* 5 nov. 2026 (Igal) : sur le détail, le client paie le prix retail de l'outil ; la seule case est le prix barré (facultatif) */
      const pv=cote==='g'?(rf.f.pr!=null?Number(rf.f.pr).toFixed(2):(v>0?Number(v).toFixed(2):'')):(rf.f.ps!=null&&rf.f.pr!=null?Number(rf.f.pr).toFixed(2):'');
      return `<div class="sb" data-sbr="${c.id}"><span class="sbt">${vf(rf.f.pr>0?'retirée de la vente : prix enregistré, hors ligne':'retirée de la vente : aucun prix sur le site')}</span>
    <label><span>${vf(cote==='g'?'prix de vente':'prix barré')}</span><input data-sr="${c.id}" type="number" step="0.01" min="0" inputmode="decimal" value="${pv}" placeholder="${cote==='g'?'0.00':'—'}"><em>$</em></label>
    ${cote==='g'?'':`<small class="sbh">${vf('Le client paiera le prix retail de la fiche. Un prix barré plus haut affiche une promo sur le site ; vide = pas de promo.')}</small>`}
    <button class="btn pri" type="button" data-sbr-go="${c.id}" style="margin-top:8px">${vf('Remettre en vente')}</button>
    <small class="sbh">${vf('Vérifie le prix, puis « Remettre en vente » : la fiche repasse en ligne tout de suite avec ce prix (une seule validation).')}</small>
    </div>`;
    }
    return `<span class="ss no">pas sur ce site</span>`;
  }
  if(f.pr===undefined) return `<span class="ss">prix du site pas encore lu</span>`;
  /* Sur perfumestrade.com presque tout est « en promo » : le client paie le prix
     promo, le prix barré est affiché à côté. Les DEUX se règlent ici (Igal, 24 sept.
     2026 : « qu'on puisse gérer les deux sans aller dans WooCommerce »). */
  const promo=f.ps!=null, paye=promo?f.ps:f.pr;
  const ecrit=peutPrixSite()&&typeof CK_URL!=='undefined'&&typeof ckTok==='function'&&ckTok();
  /* 5 nov. 2026 (Igal : « je ne veux plus que cette case rouge existe… la seule chose que je veux qui existe, c'est prix barré ») :
     sur perfumestrade.com, le client paie LE PRIX RETAIL de la fiche (la case de gauche), point. Ici une seule case, le prix barré,
     facultatif : plus haut que le retail, le site affiche une promo ; vide, pas de promo. Plus d'avertissement « le client paie X pas Y »,
     plus de lien « mettre le prix de l'outil » : l'Enregistrer du bas met le site au niveau de la fiche. */
  const n=x=>x==null?'':Number(x).toFixed(2);
  if(!ecrit) return cote==='g'?`<span class="ss">sur le site : <b>${paye!=null?money2(paye):'sans prix'}</b></span>`
    :`<span class="ss">${promo&&f.pr!=null?`${vf('prix barré')} <b>${money2(f.pr)}</b>`:vf('pas de promo')}</span>`;
  return `<div class="sb" data-sbx="${c.id}"><span class="sbt">sur le site</span>
    ${cote==='g'
      /* 12 oct. 2026 (Igal : « ça fait dix fois que je te dis que je ne veux pas de cross price pour le wholesale ») : le gros n'a qu'UN prix, celui que le client paie */
      ?`<label><span>prix de vente</span><input data-sb="${c.id}" type="number" step="0.01" min="0" inputmode="decimal" value="${n(paye)}"><em>$</em></label>`
      :`<label><span>prix barré</span><input data-sb="${c.id}" type="number" step="0.01" min="0" inputmode="decimal" value="${promo?n(f.pr):''}" placeholder="—"><em>$</em></label>
    <small class="sbh">${vf('Le client paie le prix retail (à gauche). Un prix barré plus haut affiche une promo ; vide = pas de promo.')}</small>`}
    </div>`;   /* 12 oct. 2026 : pas de bouton d'envoi — l'Enregistrer du bas envoie ces prix */
}
/* la fiche retirée de la vente de ce côté (brouillon), ou null — le code peut avoir perdu son 0 du début */
function retireCote(p,cote){
  const R=SITE._retires&&SITE._retires[cote]; if(!R||!p||!p.bc) return null;
  const {brut,b,let_,sep}=siteCodes(p), bl=brut.replace(/^0+/,'').toLowerCase(), b0=b.replace(/^0+/,'');
  const k=(let_?Object.keys(R).find(x=>x.replace(/^0+/,'').toLowerCase()===bl):null)||(sep?null:Object.keys(R).find(x=>x.replace(/^0+/,'')===b0));
  return k?{k,f:R[k]}:null;
}
/* le prix tapé sur une fiche retirée : le bouton s'allume dès qu'il y a un prix */
/* 12 oct. 2026 (Igal : « pas besoin de ces boutons, on a déjà Enregistrer en bas ») : taper dans une case du site marque seulement
   la fiche « non enregistrée » ; c'est l'Enregistrer du bas qui envoie (voir boitesEnAttente / envoieBoitesSite). */
function marqueSite(){
  const m=$('dst'); if(m && !/non enregistré/.test(m.textContent||'')){ m.textContent='modifié — non enregistré'; m.className='st'; }
}
const majEnvoiR=marqueSite, majEnvoi=marqueSite;
async function remetsPrixSite(cid,mode){
  const base=cur[FICHE.pos];
  const p=Object.assign({},base,FICHE.brouillon);
  const cote=COTE_SITE[cid]; const rf=retireCote(p,cote); if(!cote||!rf) return true;
  const box=document.querySelector(`[data-sbr="${cid}"]`); if(!box) return true;
  const txt=box.querySelector('[data-sr]').value.trim(); let n=txt===''?null:Math.round(+txt*100)/100, nP=null;
  const publie=true;   /* enregistrer le prix d'une fiche retirée = la remettre en ligne (Igal, 12 oct.) */
  const nomSite=cote==='g'?'wholesale.perfumestrade.com':'perfumestrade.com';
  if(cote==='g'){ if(n==null||!(n>0)){ alert(vf('Il faut un prix de vente.')); return false; } }
  else{
    /* 5 nov. 2026 (Igal) : le client paie le prix retail de la fiche ; le prix barré, plus haut, fait la promo */
    const v=retailFiche();
    if(v==null||!(v>0)){ alert(vf('Il faut un prix retail sur la fiche.')); return false; }
    if(n!=null&&!(n>v)) n=null;   /* un prix barré pas plus haut que le retail : pas de promo */
    if(n!=null) nP=Math.round(v*100)/100; else n=Math.round(v*100)/100;
  }
  const sousPA=(p.pa!=null&&(nP!=null?nP:n)<p.pa);
  const voitPA=typeof peut!=='function'||peut('voirPA');   /* qui ne voit pas les prix d'achat ne l'apprend pas par ce message (cette constante manquait ici : le message plantait quand on vendait à perte) */
  const msg=`« ${(p.marque||'')+' '+(p.nom||'')} » sur ${nomSite} :\n\n${cote==='g'?`prix de vente : ${money2(n)}`:(nP!=null?`prix barré (promo) : ${money2(n)}\nle client paiera : ${money2(nP)} (le prix retail)`:`le client paiera : ${money2(n)} (le prix retail), pas de promo`)}\n\n`
    +(publie?`La fiche est retirée de la vente aujourd'hui. Elle repasse EN VENTE avec ce prix.`:`Le prix est enregistré sur le site. La fiche reste HORS LIGNE (retirée de la vente) : personne ne peut l'acheter.`)
    +(sousPA?`\n\nAttention : c'est moins que le prix d'achat${voitPA?' ('+money2(p.pa)+')':''}. Tu vends à perte.`:'')+`\n\nContinuer ?`;
  if(mode==='resume') return msg;   /* la fenêtre unique de l'Enregistrer montre ce texte ; rien n'est envoyé */
  if(mode!=='envoie'&&!confirm(vf(msg))) return false;
  if(!demandeUser(false,'changer un prix sur le site',()=>{})) return false;
  try{
    const r=await fetch(CK_URL+'/api/o/'+CK_ORG+'/site/prix',{method:'POST',
      headers:{'Content-Type':'application/json',Authorization:'Bearer '+ckTok()},
      body:JSON.stringify(Object.assign({quel:cote==='g'?'gros':'',bc:rf.k,barre:n,promo:nP==null?'':nP},publie?{republier:true}:{}))});
    const j=await r.json().catch(()=>({}));
    if(!r.ok||!j.ok) throw new Error(j.erreur||('erreur '+r.status));
    const R=Object.assign({},(SITE._retires&&SITE._retires[cote])||{});
    if(publie){
      /* ce que le site a répondu : la fiche quitte les retirées et rejoint le site */
      const g=Object.assign({},rf.f,{pr:j.apres.barre,ps:j.apres.promo}); delete g.t;
      delete R[rf.k];
      SITE._retires=Object.assign({},SITE._retires,{[cote]:R});
      const kk=(SITE[rf.k]?rf.k:Object.keys(SITE).find(x=>!x.startsWith('_')&&x.replace(/^0+/,'')===rf.k.replace(/^0+/,'')))||rf.k;
      SITE[kk]=Object.assign({},SITE[kk]||{},{[cote]:g});
    }else{
      /* le prix est écrit, la fiche reste retirée : elle le garde */
      R[rf.k]=Object.assign({},rf.f,{pr:j.apres.barre,ps:j.apres.promo});
      SITE._retires=Object.assign({},SITE._retires,{[cote]:R});
    }
    ecrit(KSITE,SITE); _FMC=null; _SITE0=null; _RETS=null; oubliBoite(cid);
    alignePrixOutil(base,cid,j.apres.promo!=null?j.apres.promo:j.apres.barre);
    log({act:'prix',lib:(publie?'fiche remise en vente avec son prix sur ':'prix posé sur une fiche retirée (hors ligne) sur ')+nomSite,bc:base.bc,ref:(base.marque||'')+' '+(base.nom||''),av:'retirée de la vente',ap:cote==='g'?money2(j.apres.barre):'barré '+money2(j.apres.barre)+' · promo '+(j.apres.promo!=null?money2(j.apres.promo):'aucune')});
    render(); const l=cur.findIndex(x=>x.id===base.id); if(l>=0) FICHE.pos=l; dessineFiche();
    $('dst').textContent=vf(publie?`${money2(n)} en ligne sur ${nomSite}`:`${money2(n)} enregistré sur ${nomSite} (reste hors ligne)`); $('dst').className='st ok';
    return true;
  }catch(err){
    dessineFiche();
    alert(vf('Le prix n\'a pas été changé sur le site. La fiche reste retirée de la vente.\n\n')+(err&&err.message||''));
    return false;
  }
}
/* Les cases « sur le site » qui ne disent pas ce que le site dit : ce que l'Enregistrer du bas doit envoyer (Igal, 12 oct. 2026 :
   « sam a mis 58 en promo et 65 en prix barré, ça devrait être noté »). Une case retirée de la vente compte dès qu'elle porte un prix. */
function boitesEnAttente(){
  const L=[], base=cur[FICHE.pos]; if(!base) return L;
  const dif=(x,y)=>{ const a=x===''||x==null?null:+x; return (a==null)!==(y==null)||(a!=null&&Math.abs(a-y)>=0.005); };
  document.querySelectorAll('[data-sbx]').forEach(box=>{
    const cid=box.dataset.sbx, f=(siteDe(base)||{})[COTE_SITE[cid]]; if(!f) return;
    if(cid==='sitegros'){ if(dif(box.querySelector('[data-sb]').value,f.ps!=null?f.ps:f.pr)) L.push({cid,retire:false}); return; }   /* le gros : un seul prix, celui que le client paie */
    /* le détail (5 nov. 2026) : le client doit payer le prix retail de la fiche ; la case est le prix barré (vide = pas de promo) */
    const v=retailFiche(), paye=f.ps!=null?f.ps:f.pr, barre=f.ps!=null?f.pr:null;
    if((v!=null&&dif(v,paye))||dif(box.querySelector('[data-sb]').value,barre)) L.push({cid,retire:false});
  });
  document.querySelectorAll('[data-sbr]').forEach(box=>{
    const cid=box.dataset.sbr, rf=retireCote(base,COTE_SITE[cid]); if(!rf) return;
    const v=box.querySelector('[data-sr]').value;
    const force=!!(FICHE.repForce&&FICHE.repForce[base.id+'|'+cid]);   /* « Remettre en ligne » : le prix est déjà bon, on republie quand même */
    if(cid==='sitegros'){ if(+v>0&&(force||dif(v,rf.f.pr)||rf.f.ps!=null)) L.push({cid,retire:true}); return; }
    /* le détail (5 nov. 2026) : le client paiera le prix retail ; la case est le prix barré (vide = pas de promo) */
    const r=retailFiche(), paye=rf.f.ps!=null?rf.f.ps:rf.f.pr, barre=rf.f.ps!=null?rf.f.pr:null;
    if(r!=null&&r>0&&(force||dif(r,paye)||dif(v,barre))) L.push({cid,retire:true});
  });
  return L;
}
/* le prix retail de la fiche telle qu'elle est en train d'être modifiée (brouillon compris) */
function retailFiche(){
  const base=cur[FICHE.pos]; if(!base) return null;
  const p=Object.assign({},base,FICHE.brouillon); const c=canaux().find(x=>x.id==='site'); if(!c) return p.pvr==null?null:+p.pvr;
  const r=prixCanal(p,c); return r&&r.v!=null?+r.v:null;
}
/* envoie ces cases une à une (chacune demande sa confirmation) ; faux = on s'arrête, la fiche n'est pas enregistrée */
async function envoieBoitesSite(mode){
  let reste=boitesEnAttente().length;
  while(reste-- >0){
    const x=boitesEnAttente()[0]; if(!x) break;
    const ok=x.retire?await remetsPrixSite(x.cid,mode):await envoiePrixSite(x.cid,mode);
    if(!ok) return false;
  }
  return true;
}
async function envoiePrixSite(cid,mode){
  const base=cur[FICHE.pos];
  const p=Object.assign({},base,FICHE.brouillon);
  const cote=COTE_SITE[cid]; const cle=siteCle(p), f=(siteDe(p)||{})[cote]; if(!cote||!f) return true;
  const box=document.querySelector(`[data-sbx="${cid}"]`); if(!box) return true;
  const gros=cote==='g';
  const sB=box.querySelector('[data-sb]').value.trim();
  const nomSite=gros?'wholesale.perfumestrade.com':'perfumestrade.com';
  let nB=sB===''?null:Math.round(+sB*100)/100, nP=null, barreBas=null;
  if(gros){ if(nB==null||!(nB>0)){ alert(vf('Il faut un prix de vente.')); return false; } }
  else{
    /* 5 nov. 2026 (Igal) : le client paie le prix retail de la fiche ; le prix barré, plus haut, fait la promo */
    const v=retailFiche();
    if(v==null||!(v>0)){ alert(vf('Il faut un prix retail sur la fiche.')); return false; }
    /* un prix barré qui n'est pas plus haut que le retail ne veut rien dire : pas de promo, le client paie le retail (dit dans la fenêtre) */
    if(nB!=null&&!(nB>v)){ barreBas=nB; nB=null; }
    if(nB!=null){ nP=Math.round(v*100)/100; } else { nB=Math.round(v*100)/100; }
  }
  const paye=nP!=null?nP:nB;
  /* la faute de frappe (6,3 au lieu de 63) : avant, l'envoi était refusé sous le prix d'achat.
     9 oct. 2026 (Igal : « ne refuse jamais, pour Sam et moi ») : on prévient dans la
     confirmation, et c'est eux qui décident. */
  const sousPA=(p.pa!=null&&paye<p.pa);
  const voitPA=typeof peut!=='function'||peut('voirPA');   /* qui ne voit pas les prix d'achat ne l'apprend pas par ce message (cette constante manquait ici : le message plantait quand on vendait à perte) */
  const ancien=f.ps!=null?f.ps:f.pr, ec=ancien?Math.abs(paye-ancien)/ancien*100:0;
  const ligne=(x,y)=>`${y!=null?money2(y):'aucune'} → ${x!=null?money2(x):'aucune'}`;
  const msg=`« ${(p.marque||'')+' '+(p.nom||'')} » sur ${nomSite} :\n\n`+(gros?`prix de vente : ${ligne(nB,f.ps!=null?f.ps:f.pr)}`:(nP!=null?`prix barré (promo) : ${ligne(nB,f.ps!=null?f.pr:null)}`:`pas de promo (prix barré : ${f.ps!=null&&f.pr!=null?money2(f.pr)+' → aucun':'aucun'})${barreBas!=null?` — le prix barré tapé (${money2(barreBas)}) n'est pas plus haut que le retail, il ne compte pas`:''}`))+`\n\nLe client paiera ${money2(paye)}${gros?'':' (le prix retail de la fiche)'}.`
    +(sousPA?`\n\nAttention : c'est moins que le prix d'achat${voitPA?' ('+money2(p.pa)+')':''}. Tu vends à perte.`:'')+(ec>20?`\n\nAttention : ${Math.round(ec)} % d'écart avec le prix payé aujourd'hui.`:'')+`\n\nLe prix change tout de suite sur le site. Continuer ?`;
  if(mode==='resume') return msg;   /* la fenêtre unique de l'Enregistrer montre ce texte ; rien n'est envoyé */
  if(mode!=='envoie'&&!confirm(vf(msg))) return false;
  if(!demandeUser(false,'changer un prix sur le site',()=>{})) return false;
  try{
    const r=await fetch(CK_URL+'/api/o/'+CK_ORG+'/site/prix',{method:'POST',
      headers:{'Content-Type':'application/json',Authorization:'Bearer '+ckTok()},
      body:JSON.stringify({quel:cote==='g'?'gros':'',bc:cle||p.bc,barre:nB,promo:nP==null?'':nP,attendu:{barre:f.pr,promo:f.ps}})});
    const j=await r.json().catch(()=>({}));
    /* ce que le site a répondu, même en cas de refus : l'outil montre les vrais prix */
    if(j&&j.avant&&typeof j.avant==='object'&&!j.ok){ f.pr=j.avant.barre; f.ps=j.avant.promo; ecrit(KSITE,SITE); }
    if(!r.ok) throw new Error(j.erreur||('erreur '+r.status));
    f.pr=j.apres.barre; f.ps=j.apres.promo; ecrit(KSITE,SITE); oubliBoite(cid);
    /* le prix payé devient le prix du canal dans l'outil */
    const payeF=f.ps!=null?f.ps:f.pr;
    alignePrixOutil(base,cid,payeF);
    const b=FICHE.brouillon; if(b.pc){ delete b.pc[cid]; if(!Object.keys(b.pc).length) delete b.pc; }
    const dit=x=>gros?(x.promo!=null?money2(x.promo):x.barre!=null?money2(x.barre):'—'):'barré '+(x.barre!=null?money2(x.barre):'—')+' · promo '+(x.promo!=null?money2(x.promo):'aucune');
    log({act:'prix',lib:'prix changés sur le site '+nomSite,bc:base.bc,ref:(base.marque||'')+' '+(base.nom||''),av:dit(j.avant||{}),ap:dit(j.apres)});
    render(); const l=cur.findIndex(x=>x.id===base.id); if(l>=0) FICHE.pos=l; dessineFiche();
    $('dst').textContent=vf(`${money2(payeF)} en ligne sur ${nomSite}`); $('dst').className='st ok';
    return true;
  }catch(err){
    dessineFiche();
    alert(vf('Le prix n\'a pas été changé sur le site.\n\n')+(err&&err.message||''));
    return false;
  }
}
/* Les ventes de ce canal arrivent-elles dans l'outil ? (état au 24 sept. 2026 —
   la page Connecteurs donne l'état réel, en direct) */
const CANAL_ETAT={site:['ok','ventes reliées'],sitegros:['ok','ventes reliées'],amazon:['ok','ventes reliées'],
  perfumecity:['ok','ventes reliées']};
const margeNette=(p,c,v)=>(p.pa!=null&&v>0)?((v*(1-(c.com||0)/100)-p.pa)/v*100):null;
/* plancher : le prix sous lequel la marge nette passe sous le seuil des reglages */
function plancher(p,com){ if(p.pa==null) return null;
  const den=1-(com||0)/100-(REG.margeMin||0)/100;
  /* commission + marge minimum >= 100 % : aucun prix ne peut tenir ce seuil.
     On renvoie l'infini plutôt que rien, sinon le contrôle disparaissait en silence. */
  return den>0?r2(p.pa/den):Infinity; }
const pcCls=t=>t==null?'na':t<0?'c':t<(REG.margeMin||0)?'w':'g';
const CH=[['bc','Code-barres','A','txt'],['nom','Nom du parfum','B','txt'],
 ['ml','Contenance (oz)','C','txt'],['marque','Marque','D','txt'],
 ['type','Type','E','txt'],['genre','Genre','F','sel'],
 ['qte','Quantité en stock','G','num'],['pa',"Prix d'achat",'H','num'],
 ['pvr','Prix retail','J','num'],['pvw','Prix de gros','K','num']];
const GEN={'':'— inconnu —',M:'Homme',W:'Femme',U:'Unisexe',K:'Enfant'};

function ouvreFiche(id){
  const l=cur.findIndex(x=>x.id===id); if(l<0) return;
  FICHE={id,pos:l,brouillon:{},frn:(MOD[id]&&MOD[id].frn)?JSON.parse(JSON.stringify(MOD[id].frn)):[]};
  dessineFiche();
  $('dov').classList.add('on'); $('dr').classList.add('on');
  document.body.style.overflow='hidden';
}
function fermeFiche(){
  clearTimeout(T_REDRAW);
  $('dov').classList.remove('on'); $('dr').classList.remove('on');
  document.body.style.overflow=''; FICHE=null;
  try{ if(typeof lsmRetour==='function') lsmRetour(); }catch(e){}   /* ouverte depuis « Mettre à jour Lightspeed » : la fenêtre revient */
  if(document.documentElement.classList.contains('cadre')){ try{ window.parent.postMessage({fiche:'fermee'},location.origin); }catch(e){} }   /* mode cadre : prévient la page qui a ouvert la fenêtre */
}
function valCour(p,k){ const b=(FICHE&&FICHE.brouillon)||{}; return b[k]!==undefined?b[k]:p[k]; }

/* Comptage physique : la feuille de stock (stock.html) enregistre ses saisies
   sous cette clé, dans le même navigateur. On la relit ici si elle existe. */
const KCPT='comptage-parfums-v1';
function comptage(bc){
  let S={}; try{ S=JSON.parse(localStorage.getItem(KCPT)||'{}'); }catch(e){ return ''; }
  const c=S[bc];
  if(c==null||c==='') return '';
  const base=P.find(x=>x.bc===bc); if(!base) return '';
  const n=+c, ec=n-(base.qte||0);
  if(ec===0) return `<div class="dcompt">Compté sur la feuille de stock : <b>${n} flacon${n>1?'s':''}</b>,
    conforme à l'inventaire.</div>`;
  const val=base.pa!=null?Math.abs(ec)*base.pa:null;
  return `<div class="dcompt ec">Compté sur la feuille de stock : <b>${n} flacon${n>1?'s':''}</b>,
    soit <b>${ec>0?'+':'−'}${Math.abs(ec)}</b> par rapport à l'inventaire${val?` (${money(val)})`:''}.
    L'inventaire n'a pas encore été corrigé.</div>`;
}


/* ================= HISTORIQUE DU PRIX D'ACHAT ET POSITION MARCHE ================= */
const KHIST='prix-achat-hist-v1', KMAR='marche-v1';
let HIST={}, MAR={};
HIST=lit(KHIST,{}); if(!HIST||typeof HIST!=='object') HIST=base(KHIST,{});
MAR=lit(KMAR,{}); if(!MAR||typeof MAR!=='object') MAR=base(KMAR,{});
const sauveHIST=()=>ecrit(KHIST,HIST);
const sauveMAR =()=>ecrit(KMAR,MAR);

/* ================= CE QUE LES DEUX SITES ANNONCENT =================
   Le stock des sites est tenu à la main, tous les jours. L'écart ne se voyait
   qu'en ouvrant le site à côté : dix-huit en ligne, quinze ici, et personne ne
   le sait. Le cockpit relit maintenant les deux catalogues chaque heure et
   dépose ce qu'ils annoncent ; cette colonne le met en face du nôtre.

   Trois états, et il faut les trois : une quantité, « pas compté » quand la
   fiche du site ne suit pas ses unités (WooCommerce le permet — dire « 0 »
   serait un mensonge), et rien du tout quand le parfum n'est pas sur ce site. */
/* Le type (EDT, EDP, OIL…) et le genre : ils sont déjà sur chaque fiche, il ne
   manquait que de les montrer dans les fenêtres. Même pastille que partout. */
const tyBadge=p=>{ const t=String((p&&p.type)||'').trim(), g=G[String((p&&p.genre)||'').trim().toUpperCase()]||'';
  return (t?' <i class="ty" data-nolang>'+esc(t)+'</i>':'')+(g?' <i class="gn">'+esc(g)+'</i>':''); };

const KSITE='site-stock-v1';
let SITE={}; { const s=lit(KSITE,{}); if(s&&typeof s==='object'&&!Array.isArray(s)) SITE=s; }
/* Le site a parfois perdu le 0 du début du code-barres (085715169587 y est rangé
   85715169587) : 66 parfums le 24 sept. On retrouve la fiche avec ou sans ces zéros. */
let _SITE0=null;
/* 10 nov. 2026 (Sam : même code-barres, ancienne et nouvelle boîte, deux prix) : un code avec des lettres (« …oldbox ») a SON produit
   sur le site ; une ancienne boîte pas encore créée n'y est pas, elle ne se rabat jamais sur le produit de l'autre boîte. */
const siteCodes=(p)=>{ const brut=String((p&&p.bc)||'').replace(/[^0-9A-Za-z]/g,''), b=brut.replace(/[^0-9]/g,'');
  const let_=/[A-Za-z]/.test(brut), sep=let_&&typeof mentionBC==='function'&&typeof FA_SEPAREES!=='undefined'&&FA_SEPAREES.has(mentionBC(brut).mention);
  return {brut,b,let_,sep}; };
const siteCle=(p)=>{ if(!p||!p.bc) return null; const {brut,b,let_,sep}=siteCodes(p); if(!brut) return null;
  if(!_SITE0){ _SITE0={}; Object.keys(SITE).forEach(k=>{ if(k.startsWith('_')) return; _SITE0[k.replace(/^0+/,'')]=k; if(/[A-Za-z]/.test(k)) _SITE0['~'+k.replace(/^0+/,'').toLowerCase()]=k; }); }
  if(let_){ if(SITE[brut]) return brut; const kl=_SITE0['~'+brut.replace(/^0+/,'').toLowerCase()]; if(kl) return kl; if(sep) return null; }
  if(!b) return null; if(SITE[b]) return b;
  return _SITE0[b.replace(/^0+/,'')]||null; };
const siteDe=(p)=>{ const k=siteCle(p); return k?(SITE[k]||null):null; };
/* Quel site fait foi ? Le DÉTAIL, parce que c'est lui qui vend au client. Prendre
   le pire des deux — ce que faisait la première version — rendait la colonne
   inutilisable : 472 parfums sont à zéro sur le site de gros alors que le détail
   concorde exactement avec nous. Ce ne sont pas des erreurs de stock, ce sont des
   parfums qu'on ne propose pas en gros, et ils noyaient les vrais écarts.
   Le gros ne sert de référence que pour un parfum absent du détail. */
function siteEcart(p){
  const e=siteDe(p); if(!e) return null;
  const val=(c)=>(c&&c.suivi&&c.q!=null)?c.q:null;
  const d=val(e.d), g=val(e.g);
  /* un code partagé (boîte / NOBOX / tester) : l'écart se mesure à ce que les fiches
     annoncent ENSEMBLE sous ce code, pas à cette fiche seule */
  const P=(typeof fichesMemeCode==='function')?fichesMemeCode(p):[p];
  const nous=P.length>1?qteSiteDe(P,e.d||e.g):sstVendable(p).q;   /* notre quantité À VENDRE : stock moins les commandes déjà vendues, pas encore parties */
  if(d!=null) return {cote:'d', q:d, d:d-nous, partage:P.length>1};
  if(g!=null) return {cote:'g', q:g, d:g-nous, partage:P.length>1};
  return null;
}
/* Deux chiffres sur une seule ligne — détail, puis gros — pour que la colonne
   tienne dans le tableau sans le faire défiler : « 18 / 4 ». Un tiret quand le
   parfum n'est pas sur ce site-là, un point quand le site ne compte pas. */
/* les codes retirés de la vente (brouillon), les deux sites confondus — un jeu refait quand SITE change */
let _RETS=null;
function retireDeLaVente(p){
  const R=SITE._retires; if(!R||!p||!p.bc) return false;
  if(!_RETS||_RETS.ref!==R){ const s=new Set(); ['d','g'].forEach(c=>Object.keys(R[c]||{}).forEach(k=>s.add(k.replace(/^0+/,'').toLowerCase()))); _RETS={ref:R,s}; }
  const {brut,b,let_,sep}=siteCodes(p);
  if(let_&&_RETS.s.has(brut.replace(/^0+/,'').toLowerCase())) return true;
  if(sep) return false;
  return _RETS.s.has(b.replace(/^0+/,''));
}
function siteCell(p){
  const e=siteDe(p);
  if(!e&&retireDeLaVente(p)) return `<span class="lsv" title="Retirée de la vente (brouillon) : aucun prix sur le site. Voir « Mettre les sites à jour ».">retiré de la vente</span>`;
  if(!e) return `<span class="lsv" title="Aucune fiche avec ce code-barres sur les deux sites.">pas en ligne</span>`;
  const ec=siteEcart(p);
  const un=(k)=>{ const c=e[k]; if(!c) return '<i class="lsn">—</i>';
    if(!c.suivi||c.q==null) return '<i class="lsn">·</i>';
    const ref = ec && ec.cote===k && ec.d!==0;
    return `<b data-nolang class="${ref?'ecart':''}">${nf(c.q)}</b>`; };
  const zero = p.qte>0 && e.d && e.d.suivi && e.d.q===0;
  return `<span class="lsq" title="Ce que les deux sites annoncent — détail, puis gros — en face de notre stock.">`
    + un('d')+'<i class="lsn"> / </i>'+un('g')+`</span>`
    + (ec&&ec.d ? `<span class="lsd"><b data-nolang>${ec.d>0?'+':'−'}${nf(Math.abs(ec.d))}</b> par rapport à notre stock</span>` : '')
    + (zero ? `<span class="lsz">en rupture sur le site</span>` : '');
}

/* ---- Le stock d'UN parfum sur les deux sites, depuis sa fiche (1er oct. 2026) ----
   Igal : « sur les sites il y a 32, j'aimerais le faire passer à 0, mais il est déjà à
   zéro dans le catalogue — donne-moi la possibilité de le passer à zéro ». L'envoi
   automatique ne part que quand NOTRE chiffre bouge ; un parfum déjà juste chez nous
   mais faux sur le site restait faux. Ici, on pousse notre quantité vendable (stock
   moins les commandes à expédier) sur ce seul parfum, sur les deux sites, après une
   question claire. Même droit que l'écran « Envoyer le stock au site » : compter. */
function sstVendable(p){
  const att=(typeof _ssAExpedier==='function')?((_ssAExpedier()[p.cle||p.id])||0):0;
  return {q:Math.max(0,Math.round(p.qte||0)-att), att};
}
/* la quantité qu'UN code doit annoncer sur le site quand plusieurs fiches le partagent :
   la fiche du site dit « no box » / « tester » → les fiches de l'ERP qui portent la même
   mention ; sinon celles sans mention ; plusieurs restent (ancien / nouveau packaging) →
   leur somme. Une seule fiche → sa quantité vendable, comme avant. */
function qteSiteDe(P,c,EXPA){
  EXPA=EXPA||((typeof _ssAExpedier==='function')?_ssAExpedier():{});
  const qv=x=>Math.max(0,Math.round(x.qte||0)-(EXPA[x.cle||x.id]||0));
  if(!P||!P.length) return 0; if(P.length===1) return qv(P[0]);
  const men=(typeof nomMention==='function')?nomMention:(()=>'' );
  const m=c?men(c.nom||''):'';
  const avec=P.filter(x=>men(String(x.bc||'').replace(/[0-9]/g,'')+' '+(x.nom||'')+' '+(x.nomSrc||''))===m);
  return (avec.length?avec:P).reduce((a,x)=>a+qv(x),0);
}
/* les fiches de l'ERP qui partagent le code du site de cette fiche */
let _FMC=null, _FMC_T=0;
function fichesMemeCode(p){ const k=siteCle(p); if(!k) return [p];
  if(!_FMC||Date.now()-_FMC_T>1500){ _FMC={}; _FMC_T=Date.now(); tousLesArticles().forEach(x=>{ if(!x.bc) return; const kk=siteCle(x); if(kk) (_FMC[kk]=_FMC[kk]||[]).push(x); }); }
  return _FMC[k]||[p]; }
function blocStockSites(p){
  const e=siteDe(p); if(!e) return '';
  const val=c=>(c&&c.suivi&&c.q!=null)?c.q:null;
  const d=val(e.d), g=val(e.g); if(d==null&&g==null) return '';
  const P=fichesMemeCode(p), partage=P.length>1;
  const q=partage?qteSiteDe(P,e.d||e.g):sstVendable(p).q, att=sstVendable(p).att;
  const faux=(d!=null&&d!==q)||(g!=null&&g!==q);
  const peutEnv=(typeof peut==='function'&&peut('compter'))&&typeof ckTok==='function'&&!!ckTok();
  const un=(lab,x)=>`<span>${lab}</span> <b data-nolang class="${x!=null&&x!==q?'ecart':''}">${x==null?'—':nf(x)}</b>`;
  return `<div class="dsst${faux?' faux':''}">
    <div><span>Sur les sites</span> : ${un('détail',d)} · ${un('gros',g)}</div>
    <div class="dsst2">${faux?`<span>${partage?'Chez nous, à vendre sous ce code ('+P.length+' fiches) :':'Chez nous, à vendre :'}</span> <b data-nolang>${nf(q)}</b>`
      +(att?` <span>(${nf(att)} déjà vendu${att>1?'s':''}, pas encore parti${att>1?'s':''})</span>`:'')
      :'<span>Les sites annoncent notre quantité.</span>'}</div>
    ${faux&&peutEnv?`<div class="dsst3"><span>Pour corriger les sites : tape la quantité dans « Quantité en stock », puis Enregistrer.</span></div>`:''}
  </div>`;
}
async function envoieStockSites(btn){
  const base=cur[FICHE.pos]; if(!base) return;
  const e=siteDe(base), k=siteCle(base); if(!e||!k) return;
  const P=fichesMemeCode(base);
  const q=P.length>1?qteSiteDe(P,e.d||e.g):sstVendable(base).q;
  const nom=((base.marque||'')+' '+(base.nom||'')).trim();
  const a=[];
  if(e.d&&e.d.suivi&&e.d.q!=null&&e.d.q!==q) a.push({quel:'',cote:'d',lib:'perfumestrade.com',avant:e.d.q});
  if(e.g&&e.g.suivi&&e.g.q!=null&&e.g.q!==q) a.push({quel:'gros',cote:'g',lib:'site de gros',avant:e.g.q});
  if(!a.length) return;
  if(!confirm(vf(`« ${nom} »\n\n`+a.map(x=>`${x.lib} : ${x.avant} → ${q}`).join('\n')+`\n\nLe stock change tout de suite sur les sites. Continuer ?`))) return;
  if(btn){ btn.disabled=true; btn.textContent=vf('Envoi…'); }
  const ok=[], ko=[];
  for(const x of a){
    try{
      const r=await fetch(CK_URL+'/api/o/'+CK_ORG+'/site/stock',{method:'POST',
        headers:{'Content-Type':'application/json',Authorization:'Bearer '+ckTok()},
        body:JSON.stringify({quel:x.quel,confirme:true,lignes:[{bc:k,q}]})});
      const j=await r.json().catch(()=>({}));
      if(!r.ok) throw new Error(j.erreur||('erreur '+r.status));
      if(!j.ecrites&&!j.dejaBon) throw new Error((j.refus&&j.refus[0]&&j.refus[0].pourquoi)
        ||((j.nonSuivies||[]).length?'la fiche du site ne compte pas ses unités':'')||((j.inconnues||[]).length?'parfum introuvable sur ce site':'')||'rien n\'a été écrit');
      /* SITE a pu être relu pendant l'envoi (une autre page a écrit) : on corrige le SITE
         d'aujourd'hui, pas l'objet lu avant la question */
      { const z=SITE[siteCle(base)||k]; if(z&&z[x.cote]) z[x.cote].q=q; if(e[x.cote]) e[x.cote].q=q; }
      ok.push(x);
    }catch(err){ ko.push(x.lib+' : '+((err&&err.message)||'échec')); }
  }
  if(ok.length){
    ecrit(KSITE,SITE);
    try{ const J=lit('crm-journal-v1',[]);
      J.push({t:new Date().toISOString(),u:NOM_UTIL||'(non renseigné)',act:'stock',
        lib:`stock de « ${nom} » mis à ${q} sur `+ok.map(x=>x.lib+' (avant '+x.avant+')').join(' et '),
        n:1,impact:0,det:[{bc:base.bc,ref:nom,ap:q}]});
      ecrit('crm-journal-v1',J); }catch(_){}
  }
  if(ko.length) alert(vf('Pas envoyé — '+ko.join(' / ')));
  dessineFiche(); paint();
}

/* ================= ENVOYER NOTRE STOCK SUR LES SITES =================
   Le sens inverse de la colonne « Sur les sites ». C'est l'action la plus
   dangereuse de l'outil : elle touche une boutique ouverte au public. D'où
   l'écran de relecture — on montre CE QUI VA CHANGER, ligne par ligne, avant
   que quoi que ce soit ne parte. Le garde-fou du cockpit refuse en plus tout
   lot qui mettrait beaucoup de références à zéro d'un coup.

   On n'envoie que les références du site choisi, qui comptent leurs unités,
   et dont la quantité diffère de la nôtre. Le reste n'est pas du silence :
   il est compté et affiché, pour qu'on sache pourquoi une ligne manque. */
let PS={quel:'', lignes:[], zeros:0};
function psQuel(){ const r=document.querySelector('input[name="psq"]:checked'); return r?r.value:''; }
function psCalcule(){
  const cote = psQuel()==='gros' ? 'g' : 'd';
  const chg=[], nonSuivi=[], absent=[], egal=[];
  /* les commandes « à expédier » (Statut shipping) sont vendues : le site ne doit plus
     les proposer, même si l'ERP ne les déstocke qu'à l'envoi (1er oct. 2026) */
  const EXPA=(typeof _ssAExpedier==='function')?_ssAExpedier():{}; let nAtt=0;
  /* tousLesArticles() = le catalogue avec les corrections en cours appliquées :
     c'est NOTRE stock d'aujourd'hui, pas celui du fichier d'origine. */
  /* un code partagé par plusieurs fiches (boîte / NOBOX / tester) : le site n'a qu'une fiche
     pour ce code — on envoie UNE quantité par code, calculée par qteSiteDe (6-7 oct. 2026 :
     avant, les deux fiches s'envoyaient l'une après l'autre et le site changeait à chaque tour) */
  const parK={};
  tousLesArticles().forEach(p=>{ if(!p.bc) return; const k=siteCle(p); if(!k){ absent.push(p); return; } (parK[k]=parK[k]||[]).push(p); });
  Object.keys(parK).forEach(k=>{
    const P=parK[k], e=SITE[k], c=e&&e[cote], p=P[0];
    if(!c||!c.id){ P.forEach(x=>absent.push(x)); return; }
    if(!c.suivi){ P.forEach(x=>nonSuivi.push(x)); return; }
    P.forEach(x=>{ const att=EXPA[x.cle||x.id]||0; if(att) nAtt+=att; });
    const q=qteSiteDe(P,c,EXPA);
    if(c.q===q){ P.forEach(x=>egal.push(x)); return; }
    const nom=P.length>1?(P.map(x=>(x.marque?x.marque+' ':'')+(x.nom||'')).join(' + ')):((p.marque?p.marque+' ':'')+(p.nom||''));
    /* le code tel que le SITE le range (parfois sans le 0 du début) */
    chg.push({bc:k, q, avant:c.q, nom});
  });
  PS.quel=psQuel(); PS.lignes=chg;
  PS.zeros=chg.filter(l=>l.q===0 && (l.avant==null||l.avant>0)).length;
  const maj=SITE._maj&&SITE._maj[cote];
  const tete = (nAtt?`<p class="hint">Les commandes à expédier sont déjà retirées : <b>${nf(nAtt)}</b> flacon(s) vendu(s), pas encore partis.</p>`:'')
             + (maj ? `<p class="hint">Catalogue du site lu le <b>${esc(String(maj).slice(0,10).replace(/^(\d{4})-(\d{2})-(\d{2}).*$/,'$2/$3/$1'))}</b>.</p>`
                   : `<p class="hint" style="color:var(--crit)">Ce site n'a pas encore été lu par le cockpit — rien ne peut partir.</p>`);
  const $r=$('psres');
  if(!chg.length){
    $r.innerHTML=tete+`<div class="psvide">Rien à envoyer : les ${nf(egal.length)} références suivies par ce site
      annoncent déjà notre quantité.</div>`+psPied(nonSuivi.length,absent.length,egal.length);
    $('psok').disabled=true; psSansPrix(); return;
  }
  const L=chg.slice().sort((a,b)=>Math.abs((b.avant==null?0:b.avant)-b.q)-Math.abs((a.avant==null?0:a.avant)-a.q));
  $r.innerHTML=tete
    +`<div class="pstot"><b>${nf(chg.length)}</b> référence${chg.length>1?'s':''} vont changer sur le site`
    +(PS.zeros?` — dont <b class="psz">${nf(PS.zeros)}</b> qui passeront à zéro`:'')+`.</div>`
    +`<table class="pst"><thead><tr><th>Référence</th><th class="r">Sur le site</th><th class="r">Chez nous</th></tr></thead><tbody>`
    +L.slice(0,300).map(l=>`<tr><td data-nolang>${esc(l.nom)}<small data-nolang>${esc(l.bc)}</small></td>
        <td class="r">${l.avant==null?'—':nf(l.avant)}</td>
        <td class="r"><b class="${l.q===0?'psz':''}">${nf(l.q)}</b></td></tr>`).join('')
    +`</tbody></table>`
    +(L.length>300?`<p class="hint">… et ${nf(L.length-300)} autres.</p>`:'')
    +psPied(nonSuivi.length,absent.length,egal.length);
  $('psok').disabled = !maj;
  psSansPrix();
}
/* Les PRIX : ce que le client paie sur le site doit être le prix de l'outil (le grand chiffre de
   la fiche). Igal, 9 oct. 2026, devant une fiche à 169 $ dans l'outil et 159 $ sur le site :
   « illogique, vérifie que le prix soit le même en haut et au prix définitif ». Ici, TOUTES les
   références de ce site dont le prix payé diffère, et un bouton (Patron/admin) pour les aligner.
   Rien ne part sans ce clic ; le prix barré ne bouge pas, c'est la promo qui prend notre prix. */
function psEcartsPrix(){
  const el=$('psecarts'); if(!el) return;
  const cote=psQuel()==='gros'?'g':'d', L=[];
  tousLesArticles().forEach(p=>{ if(!p.bc) return; let pl; try{ pl=planPrixSites(p).plan; }catch(e){ return; }
    pl.filter(x=>x.cote===cote).forEach(x=>L.push({p,x})); });
  /* un code partagé par plusieurs fiches ne compte qu'une fois */
  const vus=new Set(), U=L.filter(o=>{ const k=siteCle(o.p); if(vus.has(k)) return false; vus.add(k); return true; });
  U.sort((a,b)=>Math.abs((b.x.paye||0)-b.x.v)-Math.abs((a.x.paye||0)-a.x.v));
  PS.ecarts=U;
  const lu=SITE._maj&&SITE._maj[cote];
  if(!lu){ el.innerHTML=''; return; }
  const patron=prixSitesOk();
  if(!U.length){ el.innerHTML=`<div class="psvide" style="margin-top:14px">${L3('Prix : tous les prix payés sur ce site sont ceux de l\'outil.','Prices: every price paid on this site is the tool\'s price.','Precios: todos los precios pagados en este sitio son los de la herramienta.')}</div>`; return; }
  el.innerHTML=`<div class="pstot" style="margin-top:14px"><b>${nf(U.length)}</b> ${L3('prix sur le site ne sont pas ceux de l\'outil','prices on the site are not the tool\'s','precios del sitio no son los de la herramienta')}.</div>`
    +`<table class="pst"><thead><tr><th>${L3('Référence','Product','Referencia')}</th><th class="r">${L3('Le client paie sur le site','Customer pays on the site','El cliente paga en el sitio')}</th><th class="r">${L3('Prix de l\'outil','Tool price','Precio de la herramienta')}</th></tr></thead><tbody>`
    +U.slice(0,300).map(o=>`<tr><td data-nolang>${esc(((o.p.marque||'')+' '+(o.p.nom||'')).trim())}<small data-nolang>${esc(o.p.bc)}</small></td>
        <td class="r">${o.x.paye!=null?money2(o.x.paye):'—'}</td><td class="r"><b>${money2(o.x.v)}</b></td></tr>`).join('')
    +`</tbody></table>`+(U.length>300?`<p class="hint">… ${L3('et','and','y')} ${nf(U.length-300)} ${L3('autres','more','más')}.</p>`:'')
    +(patron?`<p style="margin:12px 0 0"><button class="btn pri" id="psalign">${L3('Mettre ces '+nf(U.length)+' prix de l\'outil sur le site','Put these '+nf(U.length)+' tool prices on the site','Poner estos '+nf(U.length)+' precios de la herramienta en el sitio')}</button></p>`
            :`<p class="hint">${L3('Seul le dirigeant (Patron) peut changer les prix du site.','Only the owner (Patron role) can change the site prices.','Solo el dirigente (Patrón) puede cambiar los precios del sitio.')}</p>`);
  const b=$('psalign'); if(b) b.onclick=psAligne;
}
async function psAligne(){
  const U=(PS.ecarts||[]).slice(), cote=psQuel()==='gros'?'g':'d'; if(!U.length) return;
  const site=cote==='g'?'wholesale.perfumestrade.com':'perfumestrade.com';
  if(!confirm(vf(`Mettre ${nf(U.length)} prix de l'outil sur ${site} ?\\n\\nLe client paiera le prix de l'outil. Le prix barré ne bouge pas : c'est le prix promo qui prend notre prix. Chaque changement est inscrit au journal.`))) return;
  const b=$('psalign'); if(b) b.disabled=true; let ok=0; const ko=[];
  for(let i=0;i<U.length;i++){
    $('psmsg').textContent=`Prix ${i+1} / ${U.length}…`; $('psmsg').className='msg';
    try{ const r=await envoiePrixFiche(U[i].p.id,cote,true); if(r){ ok+=r.ok; r.ko.forEach(k=>ko.push(((U[i].p.marque||'')+' '+(U[i].p.nom||'')).trim()+' — '+k)); } }
    catch(e){ ko.push(((U[i].p.marque||'')+' '+(U[i].p.nom||'')).trim()+' — '+((e&&e.message)||'échec')); }
  }
  $('psmsg').textContent=`${ok} prix mis sur ${site}`+(ko.length?` — ${ko.length} refusé(s) : ${ko.slice(0,3).join(' ; ')}`:'')+'.';
  $('psmsg').className='msg '+(ko.length?'err':'ok');
  psCalcule(); paint();
}
/* Les fiches SANS AUCUN PRIX sur ce site (Igal, 7 oct. 2026 : 504 fiches du site de gros à
   0,00 $, achetables — aucun prix de gros n'existe pour elles). Le dirigeant les retire de la
   vente (brouillon WooCommerce : plus visibles, plus achetables, rien d'effacé) le temps qu'un
   prix soit fixé, puis les remet en vente. Le cockpit garde les fiches retirées (SITE._retires). */
function psSansPrix(){
  psEcartsPrix();
  const cote=psQuel()==='gros'?'g':'d';
  const L=[]; Object.keys(SITE).forEach(k=>{ if(k.startsWith('_')) return; const c=SITE[k][cote]; if(!c||!c.id) return;
    const pr=(c.pr!=null&&c.pr!=='')?+c.pr:0, ps=(c.ps!=null&&c.ps!=='')?+c.ps:0; if(!pr&&!ps) L.push({bc:k,nom:c.nom||'',q:c.q||0}); });
  const R=(SITE._retires&&SITE._retires[cote])||{}; const nR=Object.keys(R).length;
  PS.sansPrix=L; PS.retires=Object.keys(R);
  const el=$('psprix'); if(!el) return;
  if(!L.length&&!nR){ el.innerHTML=''; return; }
  const patron=peutPrixSite(), stock=L.filter(x=>x.q>0).length, n=L.length;
  el.innerHTML=`<div class="pspx" style="margin-top:14px;padding:10px 12px;border-radius:8px;background:#fff3f0;border:1px solid #f3c9bf;font-size:13.5px;line-height:1.6">`
    +(n?`<p style="margin:0">${L3(`<b>${nf(n)}</b> fiche${n>1?'s':''} de ce site n'${n>1?'ont':'a'} <b>aucun prix</b> (0,00 $) et ${n>1?'sont':'est'} achetable${n>1?'s':''}${stock?`, dont ${nf(stock)} en stock`:''}.`,
        `<b>${nf(n)}</b> product${n>1?'s':''} on this site ${n>1?'have':'has'} <b>no price at all</b> ($0.00) and can be bought${stock?`, ${nf(stock)} of them in stock`:''}.`,
        `<b>${nf(n)}</b> ficha${n>1?'s':''} de este sitio no ${n>1?'tienen':'tiene'} <b>ningún precio</b> (0,00 $) y se ${n>1?'pueden':'puede'} comprar${stock?`, ${nf(stock)} en stock`:''}.`)}
       ${patron?`<button class="btn" id="psret" style="margin-left:8px">${L3('Retirer de la vente (brouillon)','Take off sale (draft)','Retirar de la venta (borrador)')}</button>`
               :`<span class="hint">${L3('Seul le dirigeant (Patron) peut les retirer de la vente.','Only the owner (Patron role) can take them off sale.','Solo el dirigente (Patrón) puede retirarlas de la venta.')}</span>`}</p>`:'')
    +(nR?`<p style="margin:${n?'8px':'0'} 0 0">${L3(`<b>${nf(nR)}</b> fiche${nR>1?'s':''} retirée${nR>1?'s':''} de la vente, en attente d'un prix.`,
        `<b>${nf(nR)}</b> product${nR>1?'s':''} taken off sale, waiting for a price.`,
        `<b>${nf(nR)}</b> ficha${nR>1?'s':''} retirada${nR>1?'s':''} de la venta, a la espera de un precio.`)}
       ${patron?`<button class="btn" id="psrep" style="margin-left:8px">${L3('Remettre en vente','Put back on sale','Volver a poner en venta')}</button>`:''}</p>`:'')
    +`</div>`;
  const b1=$('psret'); if(b1) b1.onclick=()=>psStatut('retirer');
  const b2=$('psrep'); if(b2) b2.onclick=()=>psStatut('republier');
}
async function psStatut(sens){
  const quel=psQuel(), cote=quel==='gros'?'g':'d';
  const bcs=sens==='retirer'?(PS.sansPrix||[]).map(x=>x.bc):(PS.retires||[]);
  if(!bcs.length) return;
  const site=L3(quel==='gros'?'le site de gros':'le site',quel==='gros'?'the wholesale site':'the website',quel==='gros'?'el sitio mayorista':'el sitio');
  const q = sens==='retirer'
    ? L3(`Retirer de la vente ${nf(bcs.length)} fiche(s) sans prix sur ${site} ?\n\nElles passent en brouillon dans WooCommerce : plus visibles, plus achetables. Rien n'est effacé.`,
         `Take ${nf(bcs.length)} product(s) without a price off sale on ${site}?\n\nThey become drafts in WooCommerce: no longer visible or purchasable. Nothing is deleted.`,
         `¿Retirar de la venta ${nf(bcs.length)} ficha(s) sin precio en ${site}?\n\nPasan a borrador en WooCommerce: ya no se ven ni se compran. No se borra nada.`)
    : L3(`Remettre en vente ${nf(bcs.length)} fiche(s) sur ${site} ?\n\nVérifie d'abord qu'elles ont un prix.`,
         `Put ${nf(bcs.length)} product(s) back on sale on ${site}?\n\nCheck first that they have a price.`,
         `¿Volver a poner en venta ${nf(bcs.length)} ficha(s) en ${site}?\n\nComprueba antes que tienen precio.`);
  if(!confirm(q)) return;
  $('psmsg').textContent=L3('Envoi au site…','Sending to the site…','Enviando al sitio…'); $('psmsg').className='msg';
  try{
    const r=await fetch(CK_URL+'/api/o/'+CK_ORG+'/site/statut',{method:'POST',
      headers:{'Content-Type':'application/json',Authorization:'Bearer '+ckTok()},
      body:JSON.stringify({quel,sens,bcs})});
    const j=await r.json().catch(()=>({}));
    if(!r.ok) throw new Error(j.erreur||('erreur '+r.status));
    /* on recolle tout de suite ce que le cockpit vient de ranger */
    const refus=new Set((j.refus||[]).map(x=>String(x.bc)));
    const R=Object.assign({},(SITE._retires&&SITE._retires[cote])||{});
    if(sens==='retirer'){ bcs.forEach(k=>{ const e=SITE[k]; if(!e||!e[cote]||refus.has(k)) return;
        R[k]=Object.assign({},e[cote],{t:new Date().toISOString()}); delete e[cote]; if(!e.d&&!e.g) delete SITE[k]; }); }
    else { bcs.forEach(k=>{ const f=R[k]; if(!f||refus.has(k)) return;
        SITE[k]=SITE[k]||{}; const g=Object.assign({},f); delete g.t; SITE[k][cote]=g; delete R[k]; }); }
    SITE._retires=Object.assign({},SITE._retires,{[cote]:R}); ecrit(KSITE,SITE); _FMC=null; _SITE0=null; _RETS=null;
    const lib=(sens==='retirer'?j.ecrites+' fiche(s) sans prix retirée(s) de la vente':j.ecrites+' fiche(s) remise(s) en vente')+' sur le site'+(quel==='gros'?' de gros':'');
    try{ const J=lit('crm-journal-v1',[]); J.push({t:new Date().toISOString(),u:NOM_UTIL||'(non renseigné)',act:'site',lib,n:j.ecrites,impact:0,det:[]}); ecrit('crm-journal-v1',J); }catch(e){}
    $('psmsg').textContent=lib+((j.refus&&j.refus.length)?' — '+j.refus.length+' refusée(s)':'')+'.'; $('psmsg').className='msg ok';
    psCalcule(); paint();
  }catch(e){ $('psmsg').textContent=(e&&e.message)||'échec'; $('psmsg').className='msg err'; }
}
const psPied=(ns,ab,eg)=>`<p class="hint" style="margin-top:12px">Non envoyées : <b>${nf(eg)}</b> déjà à la bonne quantité,
  <b>${nf(ns)}</b> dont la fiche ne compte pas ses unités sur ce site, <b>${nf(ab)}</b> absentes de ce site.</p>`;

async function psEnvoie(confirme){
  const b=$('psok'); b.disabled=true;
  $('psmsg').textContent='Envoi au site…'; $('psmsg').className='msg';
  try{
    const r=await fetch(CK_URL+'/api/o/'+CK_ORG+'/site/stock',{method:'POST',
      headers:{'Content-Type':'application/json',Authorization:'Bearer '+ckTok()},
      body:JSON.stringify({quel:PS.quel, confirme:!!confirme, lignes:PS.lignes.map(l=>({bc:l.bc,q:l.q}))})});
    const j=await r.json().catch(()=>({}));
    /* `confirme` doit être le dernier mot : si le serveur refuse encore APRÈS
       une confirmation, on s'arrête et on le dit. Sans ce garde, un refus qui
       persiste faisait reposer la question en boucle, sans fin. */
    if(r.status===409 && j.confirmable && !confirme){
      /* le garde-fou du cockpit : on repose la question, en clair */
      if(confirm(vf(j.erreur+'\n\nEnvoyer quand même ?'))) return psEnvoie(true);
      $('psmsg').textContent='Rien n\'a été envoyé.'; $('psmsg').className='msg'; b.disabled=false; return;
    }
    if(r.status===409) throw new Error((j.erreur||'refusé')+' (le site a refusé même après confirmation)');
    if(!r.ok) throw new Error(j.erreur||('erreur '+r.status));
    /* on recolle ce que le site dit maintenant, pour que la colonne soit juste
       tout de suite au lieu d'attendre la relecture de l'heure suivante */
    const cote=PS.quel==='gros'?'g':'d';
    PS.lignes.forEach(l=>{ const e=SITE[l.bc]; if(e&&e[cote]) e[cote].q=l.q; });
    ecrit(KSITE,SITE);
    try{ const J=lit('crm-journal-v1',[]);
      J.push({t:new Date().toISOString(),u:NOM_UTIL||'(non renseigné)',act:'stock',
        lib:j.ecrites+' fiche(s) mises à jour sur le site'+(PS.quel==='gros'?' de gros':'')+(j.zeros?', dont '+j.zeros+' à zéro':''),
        n:j.ecrites,impact:0,det:[]});
      ecrit('crm-journal-v1',J); }catch(e){}
    $('psmsg').textContent=j.ecrites+' fiche(s) mises à jour sur le site'
      +((j.refus&&j.refus.length)?' — '+j.refus.length+' refusée(s) par le site':'')+'.';
    $('psmsg').className='msg ok';
    psCalcule(); paint();
  }catch(e){
    $('psmsg').textContent=(e&&e.message)||'échec'; $('psmsg').className='msg err';
  }
  b.disabled=false;
}
(function(){
  const bt=$('psite'); if(!bt) return;
  /* Trois conditions, et chacune évite une bêtise :
     — le droit de compter (un commercial ne touche pas au stock d'une boutique) ;
     — un jeton du cockpit, sinon il n'y a personne à qui parler ;
     — un catalogue du site déjà lu, sinon on écrirait à l'aveugle.
     On regarde le jeton et NON « EN_LIGNE » : c'est le cockpit qui compte ici,
     pas l'adresse de la page. */
  const lu = SITE && SITE._maj && (SITE._maj.d || SITE._maj.g);
  const relie = (typeof ckTok==='function') && !!ckTok();
  if(!(typeof peut==='function' && peut('compter')) || !lu || !relie) return;
  bt.style.display='';
  bt.onclick=()=>{ $('psmsg').textContent=''; psCalcule(); $('psov').classList.add('on'); };
  $('psx').onclick=$('psc').onclick=()=>$('psov').classList.remove('on');
  $('psov').addEventListener('click',e=>{ if(e.target===$('psov')) $('psov').classList.remove('on'); });
  document.querySelectorAll('input[name="psq"]').forEach(r=>r.onchange=()=>{ $('psmsg').textContent=''; psCalcule(); });
  $('psok').onclick=()=>psEnvoie(false);
})();

/* les relevés déjà faits à la main sont installés une fois, sans écraser une saisie */
(function(){ let n=0;
  Object.entries(MARCHE_INIT).forEach(([k,v])=>{ if(!MAR[k]){ MAR[k]=v; n++; } });
  if(n){ sauveMAR(); bumpBase('marche-v1',n); }
})();
/* suite de l'installation du Sheet : prix modifies + journal (MOD et log existent ici) */
(function(){
  if(!window.__sheetInit) return; const K='sheet-prix-installe-2026-09-03';
  try{ if(localStorage.getItem(K)) return; }catch(e){ return; }
  let np=0;
  Object.entries(SHEET_INIT.prix||{}).forEach(([cle,v])=>{
    const m=Object.assign({},MOD[cle]||{}); let ch=false; const neuf=!MOD[cle];
    ['pa','pvr','pvw'].forEach(k=>{ if(v[k]!==undefined && m[k]===undefined){ m[k]=v[k]; ch=true; } });
    if(ch){ MOD[cle]=m; np++; if(neuf) bumpBase('fiches-modifiees-v1',1); }
  });
  if(np) sauveMOD();
  if(window.__sheetInit.n||np){
    log({act:'import',lib:'Google Sheet du 3 septembre — écarts installés avec le catalogue',u:'installation',
         n:window.__sheetInit.n,impact:Math.round((SHEET_INIT.det||[]).reduce((a,x)=>{ const p=P.find(y=>String(y.bc)===String(x.bc)); return a+(x.ap-x.av)*((p&&p.pa)||0); },0)),
         det:(SHEET_INIT.det||[]).map(x=>({bc:x.bc,ref:x.ref,av:x.av,ap:x.ap})),
         note:np?`${np} fiche${np>1?'s':''} avec prix modifiés dans le Sheet`:undefined});
    bumpBase('crm-journal-v1',1);
  }
  try{ localStorage.setItem(K,'1'); }catch(e){}
})();

let PERIODE='tout';
const PERIODES=[['3','3 mois'],['6','6 mois'],['12','12 mois'],['tout','Tout']];

/* Le prix du fichier d'inventaire compte comme un relevé : sans lui, un produit
   jamais racheté depuis n'aurait aucun historique du tout. */
function achats(p){
  const l=(HIST[p.id]||[]).slice();
  /* Le prix du fichier ne sert que de point de depart : des qu'une facture
     est enregistree, elle fait foi et le point synthetique disparait. */
  if(!l.length && p.pa!=null) l.push({d:DATE_INV,p:p.pa,f:"fichier d'inventaire",q:null,src:'fichier'});
  return l.filter(x=>x.p!=null).sort((a,b)=>a.d.localeCompare(b.d));
}
function achatsPeriode(p){
  const l=achats(p);
  if(PERIODE==='tout') return l;
  const lim=new Date(); lim.setMonth(lim.getMonth()-(+PERIODE));
  const s=isoJour(lim);
  return l.filter(x=>x.d>=s);
}
const jourFr=d=>{ const [a,m,j]=d.split('-'); return m+'/'+j+'/'+a.slice(2); };
/* le dernier prix réellement encaissé à la caisse Lightspeed pour ce parfum (les ventes reçues de la caisse) */
/* Le prix d'achat de la fiche est un prix MOYEN (moyenne des achats pondérée par les quantités) : Igal, 17 oct. 2026,
   « le prix moyen mis en façade ». Sous le chiffre, en petit, le dernier prix payé au fournisseur et sa date. */
function dernierPrixPaye(p){
  let best=null;
  try{ (HIST[p.id]||[]).forEach(x=>{ if(!x||!(x.p>0)) return; if(!best||String(x.d||'')>=best.d) best={d:String(x.d||''),p:+x.p}; }); }catch(e){}
  return `<small class="lsl">${best?`<span>dernier prix payé</span> : <b>${money2(best.p)}</b>${best.d?' · '+jourFr(best.d):''}`:'<span>aucun achat enregistré</span>'}</small>`;
}
function dernierPrixCaisse(p){
  let best=null;
  try{ (lit('factures-v1',[])||[]).forEach(f=>{
    if(!f||f.sens==='retour'||!/lightspeed/i.test((f.canal||'')+' '+(f.auto||''))) return;
    (f.lignes||[]).forEach(l=>{ if(!(l.p>0)) return; const m=(l.cle&&l.cle===p.cle)||(l.bc&&p.bc&&String(l.bc).replace(/^0+/,'')===String(p.bc).replace(/^0+/,''));
      if(m&&(!best||String(f.d||'')>=best.d)) best={d:String(f.d||''),p:+l.p}; }); });
  }catch(e){}
  return `<small class="lsl">${best?`<span>dernière vente en caisse</span> : <b>${money2(best.p)}</b> · ${jourFr(best.d)}`:vf('pas encore vendu en caisse')}</small>`;
}

/* Un seul jeu de données : ligne fine, points visibles, extrêmes seuls étiquetés. */
function courbePrix(l){
  if(l.length<2) return '';
  /* Coordonnées en pixels réels : un viewBox minuscule étiré à 100 % grossirait
     le texte et les traits dans les mêmes proportions. */
  const W=520,H=118, ML=10,MR=10,MT=26,MB=22;
  const xs=l.map(x=>new Date(x.d).getTime()), ys=l.map(x=>x.p);
  const x0=Math.min(...xs), x1=Math.max(...xs), y0=Math.min(...ys), y1=Math.max(...ys);
  const dx=(x1-x0)||1, dy=(y1-y0)||1;
  const px=t=>ML+(t-x0)/dx*(W-ML-MR);
  const py=v=>MT+(1-(v-y0)/dy)*(H-MT-MB);
  const pts=l.map((x,i)=>({x:px(xs[i]),y:py(x.p),o:x}));
  const iLo=ys.indexOf(y0), iHi=ys.indexOf(y1), iDer=l.length-1;
  const d='M'+pts.map(q=>q.x.toFixed(1)+','+q.y.toFixed(1)).join('L');
  const bas=H-MB;
  const aire=d+`L${pts[iDer].x.toFixed(1)},${bas}L${pts[0].x.toFixed(1)},${bas}Z`;
  const g=[0,.5,1].map(f=>{const y=(MT+f*(H-MT-MB)).toFixed(1);
    return `<line class="gl" x1="${ML}" x2="${W-MR}" y1="${y}" y2="${y}"/>`;}).join('');
  const marque=(q,i)=>{
    const cls=i===iHi?'hi':i===iLo?'lo':(i===iDer?'der':'');
    return `<circle class="pt ${cls}" cx="${q.x.toFixed(1)}" cy="${q.y.toFixed(1)}" r="4.5"><title>${
      jourFr(q.o.d)} · ${money(q.o.p)}${q.o.f?' · '+esc(q.o.f):''}${q.o.q?' · ×'+q.o.q:''}</title></circle>`;
  };
  /* On n'étiquette que les extrêmes : une valeur sur chaque point noierait la forme. */
  const etiq=(i,cls)=>{
    const q=pts[i];
    const anc = q.x>W-90 ? 'end' : (q.x<90 ? 'start' : 'middle');
    const dxl = anc==='end' ? 6 : (anc==='start' ? -6 : 0);
    const haut = q.y < MT+18;
    return `<text class="lab ${cls}" x="${(q.x-dxl).toFixed(1)}" y="${(haut?q.y+18:q.y-11).toFixed(1)}"
      text-anchor="${anc}">${money(q.o.p)}</text>`;
  };
  return `<div class="crb"><svg viewBox="0 0 ${W} ${H}" preserveAspectRatio="xMidYMid meet" role="img"
     aria-label="Prix d'achat de ${money(y0)} le ${jourFr(l[iLo].d)} à ${money(y1)} le ${jourFr(l[iHi].d)}, ${l.length} relevés">
    ${g}<path class="ar" d="${aire}"/><path class="ln" d="${d}"/>
    ${pts.map(marque).join('')}
    ${iHi!==iLo ? etiq(iHi,'hi')+etiq(iLo,'lo') : etiq(0,'')}
    <text class="ax" x="${ML}" y="${H-6}" text-anchor="start">${jourFr(l[0].d)}</text>
    <text class="ax" x="${W-MR}" y="${H-6}" text-anchor="end">${jourFr(l[iDer].d)}</text>
  </svg></div>`;
}


/* ================= LES VENTES DE CE PARFUM =================
   Sam, 11 oct. 2026 : « taper le nom ou le code-barres d'un produit et avoir tout son historique :
   combien vendus, sur quel canal, à qui ». Tout vient des factures (file du site, caisse, Amazon,
   ventes saisies ici) : un retour compte en moins. Le filtre de période est celui du bloc d'à côté. */
function ventesDe(p){
  const k=p.cle||p.id, bcs=new Set([String(p.bc||'')].concat(String(p.bcs||'').split(/[\s,;]+/)).filter(Boolean));
  let F=[]; try{ F=lit('factures-v1',[])||[]; }catch(e){ F=[]; }
  const out=[];
  F.forEach(f=>{ if(!f||f.sens!=='vente'||f.annule) return;
    (f.lignes||[]).forEach(l=>{ if(!l||!(l.cle===k||(l.bc&&bcs.has(String(l.bc))))) return;
      const q=+l.q||0; if(!q) return;
      out.push({d:f.d||'',h:f.h||'',num:f.num||'',fid:f.id||'',client:f.tiers||'',canal:f.canal||'',q:f.retour?-Math.abs(q):q,p:l.p==null?null:+l.p,
        pa:l.paAv==null?null:+l.paAv,retour:!!f.retour,auto:f.auto||''}); }); });
  /* les ventes d'avant les factures (ventes-v1), si elles n'ont pas déjà leur facture */
  try{ const V=(lit('ventes-v1',{})||{})[k]||[]; const vus=new Set(out.map(x=>String(x.num).replace(/ \(remboursé\)$/,'')+'|'+x.d));
    V.forEach(v=>{ const n=String(v.num||'').replace(/ \(remboursé\)$/,''); if(vus.has(n+'|'+v.d)) return;
      out.push({d:v.d||'',h:v.h||'',num:n,fid:'',client:v.c||'',canal:v.k||'',q:+v.q||0,p:v.p==null?null:+v.p,pa:null,retour:(+v.q||0)<0,auto:''}); }); }catch(e){}
  histGrosLignes(p).forEach(x=>out.push(x));
  out.sort((a,b)=>(b.d+(b.h||'')).localeCompare(a.d+(a.h||'')));
  return out;
}
function ventesPeriode(p){ const l=ventesDe(p); if(PERIODE==='tout') return l;
  const lim=new Date(); lim.setMonth(lim.getMonth()-(+PERIODE)); const s=isoJour(lim); return l.filter(x=>x.d>=s); }
/* le prix d'achat qui vaut pour une vente : celui noté sur la facture, sinon celui d'aujourd'hui
   (même règle que la page Ventes : avant la mise en service, le prix d'aujourd'hui) */
function vPa(p,x){ const fige=String((REG&&REG.paFigeDepuis)||'2026-10-01'); const paNow=(typeof paEff2==='function')?paEff2(p):(p.pa==null?null:+p.pa);
  if(x.d&&x.d<fige&&paNow!=null) return paNow; return x.pa!=null?x.pa:paNow; }
/* le rythme : flacons par mois sur les 12 derniers mois, en petites barres */
function vMois(l){
  const M=[]; const d=new Date(); d.setDate(1);
  for(let i=11;i>=0;i--){ const x=new Date(d.getFullYear(),d.getMonth()-i,1); M.push({k:x.getFullYear()+'-'+String(x.getMonth()+1).padStart(2,'0'),lib:x.toLocaleDateString('en-US',{month:'short'}),q:0,m:0}); }
  const idx=Object.fromEntries(M.map((o,i)=>[o.k,i]));
  l.forEach(x=>{ const i=idx[String(x.d).slice(0,7)]; if(i!=null){ M[i].q+=x.q; M[i].m+=x.q*(x.p||0); } });
  return M;
}
function vBarres(M){
  const mx=Math.max(1,...M.map(o=>Math.max(0,o.q)));
  return `<div class="vmois">${M.map(o=>`<div class="vm" title="${esc(o.lib)} : ${nf(o.q)} flacon(s) · ${money(o.m)}"><i style="height:${Math.round(Math.max(0,o.q)/mx*52)}px" class="${o.q<0?'neg':o.q?'':'z'}"></i><b>${o.q?nf(o.q):''}</b><span>${esc(o.lib)}</span></div>`).join('')}</div>`;
}
function joursDepuis(d){ if(!d) return null; const a=new Date(d+'T12:00:00'), b=new Date(); return Math.max(0,Math.round((b-a)/86400e3)); }
/* L'historique de gros d'AVANT l'ERP (tableur de Sam, jusqu'au 30 sept. 2026) : ses lignes entrent dans
   « Ventes de ce parfum » comme n'importe quelle vente — totaux, par canal, par client, rythme, 12 mois,
   Excel. 13 oct. 2026, Igal : « l'historique n'y est pas dans la fiche produit ». Ensuite, ce sont les ventes
   de l'ERP. Pas de n° de facture : un clic sur la ligne n'ouvre donc rien dans Ventes. */
const CANAL_HG="Vente en gros · avant l'ERP";
function histGrosLignes(p){
  const H=window.D_HG; if(!H||!H.l) return [];
  const ks=new Set([String(p.bc||'').replace(/^0+/,'')].concat(typeof bcsDe==='function'?bcsDe(p):[]));
  const out=[]; ks.forEach(k=>{ (H.l[k]||[]).forEach(r=>out.push({d:r[0]||'',h:'',num:'',fid:'',client:H.c[r[1]]||'',canal:CANAL_HG,q:r[2],p:r[3],pa:null,retour:false,auto:'',hist:1})); });
  return out;
}
function blocVentes(p){
  const tous=ventesDe(p), l=ventesPeriode(p);
  const VPA=typeof peut!=='function'||peut('voirPA'), VMG=VPA&&(typeof peut!=='function'||peut('voirMarge'));
  const T=L3;
  const chips=`<div class="per">${PERIODES.map(([v,lib])=>`<button data-per="${v}" class="${PERIODE===v?'on':''}">${lib}</button>`).join('')}</div>`;
  const titre=`<h3>${T('Ventes de ce parfum','Sales of this perfume','Ventas de este perfume')} <span style="float:right">${nf(l.filter(x=>x.q>0).length)} ${T('vente'+(l.filter(x=>x.q>0).length>1?'s':''),'sale'+(l.filter(x=>x.q>0).length>1?'s':''),'venta'+(l.filter(x=>x.q>0).length>1?'s':''))}</span></h3>`;
  if(!l.length) return `<div class="dsec">${titre}${chips}
    <div class="mvide">${tous.length?T(`Aucune vente sur cette période. Il y en a ${tous.length} en tout — élargis la période.`,`No sale in this period. There are ${tous.length} in all — widen the period.`,`Ninguna venta en este período. Hay ${tous.length} en total — amplía el período.`)
      :T('Aucune vente enregistrée pour ce parfum.','No sale recorded for this perfume.','Ninguna venta registrada para este perfume.')}</div></div>`;
  const nQ=l.reduce((a,x)=>a+x.q,0), ca=l.reduce((a,x)=>a+x.q*(x.p||0),0), nRet=l.filter(x=>x.q<0).reduce((a,x)=>a+Math.abs(x.q),0);
  /* pas de marge sur l'historique d'avant l'ERP : on ne connaît pas le prix d'achat de l'époque (celui d'aujourd'hui donnerait des pertes fausses) */
  const marge=x=>{ if(x.hist) return null; const pa=vPa(p,x); return (pa==null||x.p==null)?null:(x.p-pa)*x.q; };
  const mgTot=VMG?l.reduce((a,x)=>{ const m=marge(x); return m==null?a:a+m; },0):null;
  /* le rythme et la couverture : sur les 90 derniers jours, retours déduits */
  const j90=isoJour(new Date(Date.now()-90*86400e3)); const q90=tous.filter(x=>x.d>=j90).reduce((a,x)=>a+x.q,0);
  const parSem=q90/13, stock=+p.qte||0, semaines=parSem>0?stock/parSem:null;
  const derniere=tous.find(x=>x.q>0), premiere=tous.slice().reverse().find(x=>x.q>0), dj=derniere?joursDepuis(derniere.d):null;
  /* 1er nov. 2026 (Igal : « sur ces valeurs-là, rajouter le prix payé par le customer ») : par client, le prix moyen payé
     par flacon (montant ÷ flacons), et la fourchette « de X à Y » quand le client n'a pas toujours payé le même prix.
     Les retours ne comptent pas dans la fourchette (leur prix n'est pas un prix payé). */
  const grp=(cle)=>{ const G={}; l.forEach(x=>{ const g=cle(x)||'—'; const o=G[g]=G[g]||{n:g,q:0,m:0,mg:0,d:'',pmin:null,pmax:null}; o.q+=x.q; o.m+=x.q*(x.p||0); const mm=marge(x); if(mm!=null){ o.mg+=mm; o.mgk=1; } if(x.d>o.d) o.d=x.d;
      if(x.q>0&&x.p!=null){ o.pmin=o.pmin==null?x.p:Math.min(o.pmin,x.p); o.pmax=o.pmax==null?x.p:Math.max(o.pmax,x.p); } });
    return Object.values(G).sort((a,b)=>b.q-a.q||b.m-a.m); };
  const C=grp(x=>x.canal), K=grp(x=>x.client);
  const pxPaye=o=>{ if(!(o.q>0)) return '—'; const moy=money(o.m/o.q);
    return (o.pmin!=null&&o.pmax-o.pmin>0.004)?`${moy}<br><small class="hint">${T('de','from','de')} ${money(o.pmin)} ${T('à','to','a')} ${money(o.pmax)}</small>`:moy; };
  const tab=(T2,tete,max,mg,px)=>`<table class="vtab"><thead><tr><th>${tete}</th><th class="r">${T('Flacons','Bottles','Frascos')}</th><th class="r">${T('Montant','Amount','Importe')}</th>${px?`<th class="r" title="${esc(T('Prix moyen payé par flacon, et la fourchette si le client n\'a pas toujours payé le même prix','Average price paid per bottle, and the range if the customer did not always pay the same price','Precio medio pagado por frasco, y el rango si el cliente no siempre pagó el mismo precio'))}">${T('Prix payé','Price paid','Precio pagado')}</th>`:''}${mg?`<th class="r">${T('Il te reste','Left for you','Te queda')}</th>`:''}<th class="r">${T('Dernière','Last','Última')}</th></tr></thead>
    <tbody>${T2.slice(0,max).map(o=>`<tr><td data-nolang>${esc(o.n)}</td><td class="r">${nf(o.q)}</td><td class="r">${money(o.m)}</td>${px?`<td class="r">${pxPaye(o)}</td>`:''}${mg?`<td class="r ${o.mgk&&o.mg<0?'neg':''}">${o.mgk?money(o.mg):'—'}</td>`:''}<td class="r">${o.d?jourFr(o.d):'—'}</td></tr>`).join('')}
    ${T2.length>max?`<tr><td colspan="6" class="hint">… ${T('et','and','y')} ${nf(T2.length-max)} ${T('autres','more','más')}</td></tr>`:''}</tbody></table>`;
  const ligne=x=>{ const m=VMG?marge(x):null;
    return `<li${x.num?` class="vlk" data-vnum="${esc(x.num)}" title="${esc(T('Ouvrir cette vente dans Ventes','Open this sale in Sales','Abrir esta venta en Ventas'))}"`:''}><span class="d">${x.d?jourFr(x.d):'—'}${x.h?' '+esc(x.h):''}</span>
      <span class="f" title="${esc(x.client)}"><b data-nolang>${esc(x.client||T('client non noté','customer not noted','cliente no anotado'))}</b> · <span data-nolang>${esc(x.canal)}</span>${x.num?` · <small data-nolang>${esc(x.num)}</small>`:''}</span>
      <span class="q ${x.q<0?'ret':''}">${x.q<0?'retour ':'×'}${nf(Math.abs(x.q))}</span><span class="p">${x.p==null?'—':money(x.p)}</span>${VMG?`<span class="mg ${m!=null&&m<0?'neg':''}">${m==null?'':(m>=0?'+':'')+money(m)}</span>`:''}</li>`; };
  const rythme=`<div class="vryt">
      <div><span class="v">${nf(Math.round(parSem*10)/10)}</span><span class="k">${T('flacons / semaine (90 derniers jours)','bottles / week (last 90 days)','frascos / semana (últimos 90 días)')}</span></div>
      <div><span class="v">${semaines==null?'—':(semaines>99?'99+':nf(Math.round(semaines)))}</span><span class="k">${T('semaines de stock au rythme actuel','weeks of stock at current pace','semanas de stock al ritmo actual')}${stock?` (${nf(stock)} ${T('en stock','in stock','en stock')})`:''}</span></div>
      <div><span class="v">${dj==null?'—':dj===0?T('aujourd\'hui','today','hoy'):nf(dj)+' j'}</span><span class="k">${T('depuis la dernière vente','since the last sale','desde la última venta')}${derniere?' · '+jourFr(derniere.d):''}</span></div>
      <div><span class="v">${premiere?jourFr(premiere.d):'—'}</span><span class="k">${T('première vente connue','first known sale','primera venta conocida')}</span></div>
    </div>`;
  const nV=l.filter(x=>x.q>0).length;
  const resume=`<span class="vs-n">${nf(nV)} ${T('vente'+(nV>1?'s':''),'sale'+(nV>1?'s':''),'venta'+(nV>1?'s':''))} · ${nf(nQ)} ${T('flacons','bottles','frascos')} · ${money(ca)}${derniere?' · '+T('dernière','last','última')+' '+jourFr(derniere.d):''}</span>`;
  const nVoir=(FICHE&&FICHE.vTout)?60:10, nPlus=l.length;
  /* 12 oct. 2026 (Igal : « il faut réduire cette page et donner la possibilité de cliquer pour ouvrir ») : le bloc est REPLIÉ — un titre et une ligne de chiffres ;
     un clic l'ouvre. Même ouvert, la liste ne montre que les 10 dernières ventes (un bouton pour les 60). Il reste ouvert quand la fiche se redessine. */
  return `<details class="dsec dvt" id="dvtes"${FICHE&&FICHE.vOpen===false?'':' open'}><summary><span class="vs-t">${T('Ventes de ce parfum','Sales of this perfume','Ventas de este perfume')}</span>${resume}<span class="vs-c">▾</span></summary>
    ${chips}
    <div class="hst">
      <div><span class="v">${nf(nQ)}</span><span class="k">${T('flacons vendus (retours déduits)','bottles sold (returns deducted)','frascos vendidos (devoluciones deducidas)')}</span></div>
      <div><span class="v">${money(ca)}</span><span class="k">${T('chiffre de vente','sales amount','importe de ventas')}</span></div>
      <div><span class="v">${nQ>0?money(ca/nQ):'—'}</span><span class="k">${T('prix moyen','average price','precio medio')}</span></div>
      ${VMG?`<div><span class="v ${mgTot<0?'hi':'lo'}">${money(mgTot)}</span><span class="k">${T('il te reste, achat déduit','left for you, purchase deducted','te queda, compra deducida')}</span></div>`:''}
      <div><span class="v ${nRet?'hi':''}">${nf(nRet)}</span><span class="k">${T('flacons rendus','bottles returned','frascos devueltos')}</span></div>
    </div>
    <div class="vdeux">
      <div><h4>${T('Par canal','By channel','Por canal')}</h4>${tab(C,T('Canal','Channel','Canal'),6,VMG)}</div>
      <div><h4>${T('Par client','By customer','Por cliente')}</h4>${tab(K,T('Client','Customer','Cliente'),5,false,true)}</div>
    </div>
    <details class="vdet" id="dvdet"${FICHE&&FICHE.vDet?' open':''}><summary>${T('Le rythme et chaque vente','Pace and every sale','El ritmo y cada venta')} <small class="hint">${T('— cliquer pour agrandir','— click to expand','— clic para ampliar')} (${nf(l.length)})</small></summary>
    <h4>${T('Le rythme','The pace','El ritmo')}</h4>
    ${rythme}
    ${vBarres(vMois(tous))}
    <h4>${T('Chaque vente','Each sale','Cada venta')} <small class="hint">${T('— un clic ouvre la vente','— click to open the sale','— un clic abre la venta')}</small></h4>
    <ul class="ach vlist">${l.slice(0,nVoir).map(ligne).join('')}</ul>
    <div class="dbtns" style="margin-top:8px">${nPlus>10?`<button class="btn" data-vmore="1">${(FICHE&&FICHE.vTout)?T('Voir seulement les 10 dernières','Show only the last 10','Ver solo las 10 últimas'):T('Voir plus de ventes','Show more sales','Ver más ventas')}</button>`:''}
      ${l.length>nVoir?`<span class="hint">${T(`Les ${nVoir} plus récentes sont affichées ; l'Excel les a toutes.`,`The ${nVoir} most recent are shown; the Excel has them all.`,`Se muestran las ${nVoir} más recientes; el Excel las tiene todas.`)}</span>`:''}</div>
    </details>
    <div class="dbtns" style="margin-top:8px"><button class="btn" data-vxl="1">${T('Historique complet (Excel)','Full history (Excel)','Historial completo (Excel)')}</button></div>
  </details>`;
}
/* l'Excel de l'historique et l'ouverture d'une vente : posés une fois, sur la fiche */
$('ddb').addEventListener('toggle',e=>{ if(!FICHE||!e.target) return; if(e.target.id==='dvtes') FICHE.vOpen=e.target.open; else if(e.target.id==='dvdet') FICHE.vDet=e.target.open; },true);
document.addEventListener('click',e=>{
  const mo=e.target.closest('[data-vmore]'); if(mo&&FICHE){ FICHE.vTout=!FICHE.vTout; FICHE.vOpen=true; FICHE.vDet=true; dessineFiche(); return; }
  const li=e.target.closest('.vlist li.vlk'); if(li&&FICHE){ location.href='ventes.html?v=__VER__&q='+encodeURIComponent(li.dataset.vnum); return; }
  const b=e.target.closest('[data-vxl]'); if(!b||!FICHE) return;
  const p=cur[FICHE.pos]; const l=ventesDe(p); const VMG=(typeof peut!=='function'||(peut('voirPA')&&peut('voirMarge')));
  const nom=((p.marque||'')+' '+(p.nom||'')).trim();
  const col=[{t:'Date',y:'d'},{t:'Heure'},{t:'N° de vente'},{t:'Client'},{t:'Canal'},{t:'Flacons',y:'n'},{t:'Prix unitaire',y:'m'},{t:'Montant',y:'m'}];
  if(VMG) col.push({t:'Prix d\'achat',y:'m'},{t:'Il te reste',y:'m'});
  const L=l.map(x=>{ const r=[x.d,x.h||'',x.num,x.client,x.canal,x.q,x.p,x.p==null?null:Math.round(x.q*x.p*100)/100];
    if(VMG){ const pa=x.hist?null:vPa(p,x); r.push(pa,(pa==null||x.p==null)?null:Math.round((x.p-pa)*x.q*100)/100); } return r; });
  sortieXlsx({titre:'Ventes — '+nom,filtre:l.length+' vente(s), toutes périodes',fichier:'ventes-'+nom.replace(/[^A-Za-z0-9]+/g,'-').slice(0,40),colonnes:col,lignes:L});
});
function blocHistorique(p){
  const tous=achats(p), l=achatsPeriode(p);
  const chips=`<div class="per">${PERIODES.map(([v,lib])=>
    `<button data-per="${v}" class="${PERIODE===v?'on':''}">${lib}</button>`).join('')}</div>`;
  if(!l.length) return `<div class="dsec"><h3>Prix d'achat dans le temps</h3>${chips}
    <div class="mvide">Aucun achat sur cette période. ${tous.length?`Il y en a ${tous.length} en tout — élargis la période.`:''}</div>
    <div class="dbtns"><button class="btn" data-ach="new">+ Enregistrer un achat</button>
      <button class="btn" data-ajust="new">Ajuster le stock</button></div></div>`;
  const ps=l.map(x=>x.p), lo=Math.min(...ps), hi=Math.max(...ps), der=l[l.length-1].p;
  const qt=l.reduce((a,x)=>a+(x.q||0),0);
  const moy = qt>0 ? l.reduce((a,x)=>a+x.p*(x.q||0),0)/qt : ps.reduce((a,b)=>a+b,0)/ps.length;
  const seul = l.length===1;
  const ecart = hi>lo ? `<div class="mvide">Entre le moins cher et le plus cher, l'écart est de
      <b>${money(hi-lo)}</b> par flacon, soit <b>${((hi-lo)/hi*100).toFixed(1).replace('.',',')} %</b>.
      ${der>lo?`Le dernier achat est <b>${money(der-lo)}</b> au-dessus du meilleur prix obtenu.`:'Le dernier achat est au meilleur prix obtenu.'}</div>` : '';
  return `<div class="dsec"><h3>Prix d'achat dans le temps <span style="float:right">${l.length} relevé${l.length>1?'s':''}</span></h3>
    ${chips}
    ${courbePrix(l)}
    <div class="hst">
      <div><span class="v lo">${money(lo)}</span><span class="k">le plus bas</span></div>
      <div><span class="v hi">${money(hi)}</span><span class="k">le plus haut</span></div>
      <div><span class="v">${money(moy)}</span><span class="k">moyen${qt>0?' pondéré':''}</span></div>
      <div><span class="v" style="color:var(--iris)">${money(der)}</span><span class="k">dernier achat</span></div>
    </div>
    ${ecart}
    <ul class="ach">${l.slice().reverse().map((x,i)=>{
      const idx=tous.indexOf(x);
      return `<li><span class="d">${jourFr(x.d)}</span>
      <span class="f">${esc(x.f||'fournisseur inconnu')}</span>
      ${x.q?`<span class="q">×${x.q}</span>`:''}
      <span class="p ${x.p===lo?'lo':x.p===hi?'hi':''}">${money(x.p)}</span>
      ${x.src==='fichier'?'':`<button class="x" data-achx="${idx}" title="Retirer">×</button>`}</li>`;}).join('')}</ul>
    ${seul?`<div class="mvide">Un seul relevé : <b>le prix du fichier d'inventaire</b>.
      L'historique se construit en enregistrant les factures fournisseur.</div>`:''}
    <div class="dbtns"><button class="btn" data-ach="new">+ Enregistrer un achat</button>
      <button class="btn" data-ajust="new">Ajuster le stock</button></div>
  </div>`;
}

function blocMarche(p){
  const m=MAR[p.id];
  const maj=`<button class="btn" data-mar="edit" style="align-self:flex-start">${m?'Mettre à jour le relevé':'Saisir un relevé'}</button>`;
  /* Sans relevé, il n'y a rien à ajouter : les deux cases du haut disent déjà
     « pas de relevé » et portent le bouton pour en saisir un. */
  if(!m) return '';
  const d=m.le?new Date(m.le):null;
  const cel=(v,k,cls='')=>`<div class="${cls}"><span class="v">${v==null?'—':money(v)}</span><span class="k">${k}</span></div>`;
  const rang = m.rang
    ? `<div class="rgb"><div class="rgn"><b>#${nf(m.rang)}</b><span>rang</span></div>
        <div class="rgd"><div class="cat">${esc(m.cat||'catégorie inconnue')}</div>
        ${m.rangG?`<div class="dem">#${nf(m.rangG)} dans ${esc(m.catG||'la catégorie générale')}</div>`:''}
        ${m.dem?`<div class="dem"><b>${esc(m.dem)}</b> achetés le mois dernier sur Amazon</div>`:''}
        ${m.note5?`<div class="dem"><b>${String(m.note5).replace('.',',')}/5</b> ${'★'.repeat(Math.round(m.note5))}${'☆'.repeat(5-Math.round(m.note5))}${m.avis?` · ${nf(m.avis)} avis`:''}</div>`:''}
        ${m.vend?`<div class="dem">vendu par <b>${esc(m.vend)}</b>${m.n>1?` · ${m.n} vendeurs`:''}</div>`:''}
        <div class="dt">relevé le ${d?d.toLocaleDateString('en-US',{timeZone:'America/New_York'}):'?'}${m.par?' · '+esc(m.par):''}</div></div></div>`
    : `<div class="mvide">${m.dem?`<b>${esc(m.dem)}</b> achetés le mois dernier sur Amazon. `:''}Le rang n'a pas été relevé
        — il se lit sur la fiche produit Amazon, section « Best Sellers Rank ».
        ${d?`<span class="dt">Relevé le ${d.toLocaleDateString('en-US',{timeZone:'America/New_York'})}.</span>`:''}</div>`;
  const note = m.note?`<div class="dinfo">${esc(m.note)}</div>`:'';
  /* historique des relevés : chaque mise à jour garde l'ancien point */
  const H=(m.hist&&m.hist.length?m.hist:[{le:m.le,amz:m.amz,rang:m.rang}]).filter(h=>h.amz!=null);
  let histo='';
  if(H.length>=2){
    const lo=Math.min(...H.map(h=>h.amz)), hi=Math.max(...H.map(h=>h.amz));
    histo=`<div class="mhist"><b>${H.length} relevés Amazon</b> · plus bas ${money(lo)} · plus haut ${money(hi)}
      <ul>${H.slice(-8).reverse().map(h=>`<li>${new Date(h.le).toLocaleDateString('en-US',{timeZone:'America/New_York'})} — ${money(h.amz)}${h.rang?` · rang #${nf(h.rang)}`:''}</li>`).join('')}</ul></div>`;
  } else if(H.length===1){
    histo=`<div class="mhist">Premier relevé : l'historique Amazon se construira à chaque mise à jour (plus bas, plus haut, courbe).
      Amazon ne publie pas l'historique de ses prix ; seul un relevé régulier le donne.</div>`;
  }
  const alerte = (()=>{
    if(m.amz==null) return m.note&&/indisponible/i.test(m.note)?`<div class="dinfo" style="border-left:3px solid var(--good);background:var(--good-soft)">
      <b>Amazon n'en a pas.</b> Une référence indisponible chez Amazon se vend sans concurrence de prix : c'est le moment de tenir le retail.</div>`:'';
    const t=[];
    if(p.pa!=null&&p.pa>=m.amz*0.92) t.push(`il est acheté ${money(p.pa)} alors qu'Amazon le vend ${money(m.amz)}`);
    if(p.pvw!=null&&p.pvw>=m.amz*0.92) t.push(`le prix de gros ${money(p.pvw)} ne laisse rien au revendeur face à ${money(m.amz)}`);
    if(p.pvr!=null&&p.pvr>m.amz*1.05) t.push(`le retail ${money(p.pvr)} dépasse Amazon de ${money(p.pvr-m.amz)}`);
    if(t.length) return `<div class="dinfo" style="border-left:3px solid var(--crit);background:var(--crit-soft)"><b>À corriger :</b> ${t.join(' ; ')}.</div>`;
    if(p.pvr!=null&&p.pvr<m.amz*0.85) return `<div class="dinfo" style="border-left:3px solid var(--good);background:var(--good-soft)">
      <b>Marge de manœuvre :</b> le retail ${money(p.pvr)} est ${money(m.amz-p.pvr)} sous Amazon (${money(m.amz)}).</div>`;
    return '';
  })();
  /* Ce que les deux cases du haut ne disent pas : le verdict sur ses prix, et l'historique
     des relevés. Le rang, la note et le vendeur sont déjà affichés là-haut. */
  if(!alerte && !note && !histo) return '';
  return `<div class="dsec"><h3>Amazon — ce que ça change pour ses prix</h3>
    <div class="cmp">
      ${cel(p.pa,'son achat','moi')}${cel(p.pvw,'son gros','moi')}${cel(p.pvr,'son retail','moi')}
      ${cel(m.amz,m.amz==null?'Amazon — indisponible':'Amazon')}
    </div>
    ${alerte}${note}${histo}</div>`;
}

/* 12 oct. 2026 (Igal : « Sam a mis 58 en promo et 65 en prix barré, il l'a save et ça n'a pas save ») : la fiche se redessine dès qu'on change une autre
   case (le prix de l'outil, par ex.), et les prix tapés dans les cases du site — pas encore enregistrés — repartaient aux valeurs du site. On les garde. */
const CLES_BOITE=['sb','sp','sr','srp'];
function dessineFiche(){
  const F=FICHE, zone=$('ddb');
  if(F){ F.bv=F.bv||{};
    if(zone.dataset.fid===String(F.id)) zone.querySelectorAll('[data-sb],[data-sp],[data-sr],[data-srp]').forEach(i=>{
      const c=CLES_BOITE.find(x=>i.dataset[x]!==undefined), k=c+':'+i.dataset[c];
      if(i.value!==i.defaultValue) F.bv[k]=i.value; else delete F.bv[k]; });
  }
  dessineFiche0();
  if(F){ zone.dataset.fid=String(F.id);
    zone.querySelectorAll('[data-sb],[data-sp],[data-sr],[data-srp]').forEach(i=>{
      const c=CLES_BOITE.find(x=>i.dataset[x]!==undefined), k=c+':'+i.dataset[c];
      if(F.bv[k]!==undefined) i.value=F.bv[k]; });
  }
}
const oubliBoite=cid=>{ if(FICHE&&FICHE.bv) Object.keys(FICHE.bv).forEach(k=>{ if(k.endsWith(':'+cid)) delete FICHE.bv[k]; }); };
function dessineFiche0(){
  if(!FICHE) return;                       /* une action arrivée après la fermeture de la fiche */
  const base=cur[FICHE.pos]; if(!base) return fermeFiche();
  FICHE.id=base.id;
  const p={}; Object.assign(p,base);
  Object.keys(FICHE.brouillon).forEach(k=>p[k]=FICHE.brouillon[k]);
  p.pc=Object.assign({},base.pc||{},FICHE.brouillon.pc||{});
  Object.keys(p.pc).forEach(k=>{ if(p.pc[k]==null) delete p.pc[k]; });
  p.an=calcAn(p);
  const mq=manque(p);

  $('dmarque').textContent=p.marque||'—';
  $('dnom').textContent=p.nom||'Sans nom';
  { const bs=$('dsup'); if(bs) bs.hidden=!(base.neuf&&typeof peut==='function'&&peut('annuler')); }
  /* 20 oct. 2026 (Igal : « je veux avoir la possibilité de modifier ou de supprimer un parfum ») : n'importe quel parfum se corrige
     (marque, nom, contenance, type, genre) ; ceux du fichier de départ, qui portent l'historique, se RETIRENT du catalogue (réversible)
     au lieu de s'effacer ; ceux ajoutés à la main se suppriment pour de bon (bouton existant). */
  { const bm=$('dmod'), br=$('dret');
    if(bm){ bm.hidden=!(typeof peut==='function'&&peut('modPrix')); bm.textContent=L3('Modifier le parfum','Edit the perfume','Modificar el perfume'); }
    if(br){ br.hidden=base.neuf||!(typeof peut==='function'&&peut('annuler'));
      br.textContent=base.masque?L3('Remettre au catalogue','Put back in the catalogue','Volver a poner en el catálogo'):L3('Retirer du catalogue','Remove from the catalogue','Quitar del catálogo'); } }   /* produit ajouté à la main + Patron/Admin seulement */
  $('dprev').disabled=FICHE.pos<=0;
  $('dnext').disabled=FICHE.pos>=cur.length-1;

  /* Sam, 3 oct. 2026 : « dans la version pour les employés, je ne veux pas qu'ils voient les
     bénéfices ». Le rôle le disait déjà (Commercial : ni prix d'achat ni marge), mais la fiche
     montrait quand même le prix d'achat, les marges et « ce qu'il te reste ». */
  const VPA=typeof peut!=='function'||peut('voirPA'), VMG=VPA&&(typeof peut!=='function'||peut('voirMarge'));
  const chips=[];
  if(p.neuf) chips.push('<span class="fl todo">ajouté à la main</span>');
  if(base.mod) chips.push('<span class="fl todo">fiche modifiée</span>');
  if(mq.length) chips.push(`<span class="fl w">${mq.length} champ${mq.length>1?'s':''} à compléter</span>`);
  if(VMG) p.an.forEach(a=>chips.push(`<span class="fl ${AN[a][1]}">${AN[a][0]}</span>`));

  const img=p.img?`<img src="${phSrc(p)}" data-far="${p.imgPerso?'':p.img}" alt="" onerror="secours(this)">`
    :`<div class="miss"><svg viewBox="0 0 40 64" fill="none"><rect x="14.5" y="2" width="11" height="9" rx="1.5" stroke="currentColor" stroke-width="2.4"/><path d="M11 20a6 6 0 016-6h6a6 6 0 016 6v34a6 6 0 01-6 6H17a6 6 0 01-6-6V20z" stroke="currentColor" stroke-width="2.4"/></svg><span>sans photo</span></div>`;

  const champ=([k,lab,_col,t,opt])=>{
    const v=valCour(p,k), vide=(v==null||v==='')&&!opt, chg=FICHE.brouillon[k]!==undefined;
    if(t==='sel') return `<div class="dfld${chg?' ch':''}"><label>${lab}</label>
      <select data-k="${k}">${Object.entries(GEN).map(([o,n])=>
        `<option value="${o}"${(v||'')===o?' selected':''}>${n}</option>`).join('')}</select></div>`;
    return `<div class="dfld${chg?' ch':''}"><label>${lab}</label>
      <input data-k="${k}" class="${t==='num'?'mono ':''}${vide?'vide':''}"
       type="${t==='num'?'number':'text'}" ${t==='num'?'step="any" inputmode="decimal"':''}
       value="${v==null?'':String(v).replace(/"/g,'&quot;')}"
       placeholder="${vide?'à compléter':(opt||'')}"></div>`;
  };

  const pa=p.pa, cap=(p.qte||0)*(pa||0);
  const mg=(v)=>(v!=null&&pa!=null&&v>0)?((v-pa)/v*100):null;
  const pc=v=>v==null?'—':(v>=0?'':'−')+Math.abs(v).toFixed(1).replace('.',',')+' %';
  const col=v=>v==null?'var(--ink-3)':v<0?'var(--crit)':v<10?'var(--warn)':'var(--good)';

  const frnHtml=FICHE.frn.map((f,i)=>`
    <div class="dgrid" style="grid-template-columns:1fr 118px 34px;gap:8px;align-items:end">
      <div class="dfld"><label>Fournisseur</label>
        <input data-f="n" data-i="${i}" value="${(f.n||'').replace(/"/g,'&quot;')}" placeholder="Nom"></div>
      <div class="dfld"><label>Prix d'achat</label>
        <input data-f="p" data-i="${i}" class="mono" type="number" step="any"
         value="${f.p==null?'':f.p}" placeholder="—"></div>
      <button class="btn" data-fx="${i}" title="Retirer" style="padding:8px 0;height:35px">&times;</button>
    </div>`).join('');

  const q=p.qte||0;
  const VF={ok:['vok','comptage vérifié'],non:['vnon','jamais compté physiquement'],
             av:['vav','signalé à vérifier'],'':['vvide','statut de comptage inconnu']};
  const vst=base.verif||'';
  const vf = q>0 ? (VF[vst]||VF['']) : ['vrupt','plus de stock'];
  const cpt=comptage(p.bc);
  const mm=MOD[base.id]||{};
  const vbloc = q===0 ? `<span class="dvf ${vf[0]}">${vf[1]}</span>` : `
    <div class="dvz">
      <span class="dvf ${vf[0]}">${vf[1]}</span>
      ${vst==='ok'
        ? (mm.verifLe
            ? `<span class="dvq">compté par <b>${esc(mm.verifPar||'?')}</b> le ${dateFr(mm.verifLe)}${
                 mm.qteC!=null&&mm.qteAv!=null&&+mm.qteAv!==+mm.qteC
                   ? ` — la quantité est passée de ${nf(mm.qteAv)} à ${nf(mm.qteC)}` : ''}
               <button class="lnk" data-v="non">déverrouiller ce comptage</button></span>`
            : `<span class="dvq"><b>personne ne l'a compté</b> : c'est le fichier d'inventaire qui l'affirme
               <button class="lnk" data-v="non">déverrouiller ce comptage</button></span>`)
        : `<button class="btn ptt" data-v="ok">Confirmer le comptage</button>
           ${vst!=='av'?`<button class="btn ptt" data-v="av">Signaler à vérifier</button>`:''}`}
    </div>`;

  // rail de prix : achat -> gros -> retail, avec l'écart entre chaque étape
  /* Trois cases : achat, gros, retail. La marge (par rapport au prix d'achat)
     est ecrite dans la case du prix de vente concerne, comme dans la liste. */
  const etape=(k,lab,_col,avecMarge,extra)=>{
    const v=valCour(p,k), vide=(v==null||v===''), chg=FICHE.brouillon[k]!==undefined;
    let mg='';
    if(avecMarge&&VMG){
      const t=marge(p,v);
      if(t==null) mg=`<i class="mg na">marge —</i>`;
      else mg=`<i class="mg ${t<0?'c':t<REG.margeMin?'w':'g'}">marge ${pc(t)}</i>`;
    }
    return `<div class="st${chg?' ch':''}"><span>${lab}</span>
      <div class="in"><input data-k="${k}" type="number" step="any" inputmode="decimal"
       class="${vide?'vide':''}" value="${v==null?'':v}" placeholder="—"><em>$</em></div>${mg}${extra||''}</div>`;
  };

  $('ddb').innerHTML=`
    <div class="dhero">
      <div class="dphw">
        <div class="dph">${img}</div>
        ${(typeof peut!=='function'||peut('modPrix'))?`<div class="dphb">
          <button type="button" class="btn dphc" data-phchg>${L3('Changer la photo','Change photo','Cambiar la foto')}</button>
          <button type="button" class="btn dphc dphw2" data-phweb>${L3('Chercher sur Internet','Find on the Internet','Buscar en Internet')}</button>
          ${p.imgPerso?`<button type="button" class="lnk dphr" data-phrst>${L3('Revenir à la photo d\'origine','Back to the original photo','Volver a la foto original')}</button>`:''}
          ${p.img&&typeof ckTok==='function'&&ckTok()?`<button type="button" class="lnk dphr" data-phenv>${L3('Envoyer cette photo aux sites','Send this photo to the websites','Enviar esta foto a los sitios')}</button>`:''}
          <input type="file" id="dphf" accept="image/*" hidden>
        </div>`:''}
      </div>
      <div class="dstk">
        <!-- Sam, 2 oct. 2026 : « Quantity in stock dans la fiche du produit pas très visible » ;
             Igal, 11 oct. 2026 : « ça prend trop de place », et la quantité ne se modifie ici que
             par Sam ou lui (Patron, admin) — les autres passent par l'Inventaire. -->
        ${(()=>{ const r=(()=>{ try{ return (typeof session==='function'?session():JSON.parse(localStorage.getItem('sam-session-v1')||'null')||{}).role||''; }catch(e){ return ''; } })();
          const edit=(r==='patron'||r==='admin');
          return `<div class="dtop">
          <div class="dqte${FICHE.brouillon.qte!==undefined?' ch':''}${edit?'':' ro'}"><label for="dqte-in">${L3('Stock Perfumes Trade','Perfumes Trade stock','Stock Perfumes Trade')}</label>
            <div class="dqte-l">${edit?`<input id="dqte-in" data-k="qte" type="number" step="1" min="0" inputmode="numeric" value="${q}">`:`<b data-nolang>${nf(q)}</b>`}<em>${q>1?'flacons':'flacon'}</em></div>
            ${edit?'':`<small>${L3('modifiable par le dirigeant, ou par l\'Inventaire','editable by the owner, or via Inventory','modificable por el dirigente, o desde Inventario')}</small>`}</div>
          ${(()=>{ /* 31 oct. 2026 (Igal : « dans la fiche produit, la quantité de stock Perfumes Trade et la quantité de stock Perfume City ») :
             le stock de la boutique de Kim (inventaire Perfume City, pc-stock-v1), lu par le code-barres — lecture seule, il se corrige
             dans l'Inventaire Perfume City */
             const qp=pcStockFiche(p);
             return `<div class="dqte dqpc ro"><label>${L3('Stock Perfume City','Perfume City stock','Stock Perfume City')}</label>
               <div class="dqte-l">${qp?`<b data-nolang>${nf(qp.q)}</b><em>${qp.q>1?L3('flacons','bottles','frascos'):L3('flacon','bottle','frasco')}</em>`:`<b data-nolang>—</b>`}</div>
               <small>${qp?L3('dans la boutique · se corrige dans l\'Inventaire Perfume City','in the shop · corrected in the Perfume City inventory','en la tienda · se corrige en el Inventario Perfume City'):L3('pas dans l\'inventaire de Perfume City','not in the Perfume City inventory','no está en el inventario de Perfume City')}</small></div>`; })()}
          ${q>0&&VPA?`<div class="cap">${cap?money(cap):'—'}<small>${L3('de marchandise','of goods','de mercancía')}</small></div>`:''}
          ${(()=>{ const a=azPourFiche(p);
             return `<a class="damz" href="${esc(a.href)}" target="_blank" rel="noopener" title="${esc(a.titre)}">${logo('amazon','Amazon')}<span>${a.exact?L3('Ouvrir la fiche','Open the listing','Abrir la ficha'):L3('Chercher','Search','Buscar')} ↗</span>${a.prix!=null?`<small data-nolang>${money2(a.prix)}</small>`:(a.exact&&a.asin?`<small data-nolang>${esc(a.asin)}</small>`:'')}</a>`; })()}
        </div>`; })()}
        ${vbloc}
        ${q>0&&base.rang&&VPA?`<div class="rk">Cette référence est la <b>n° ${base.rang}</b> du stock par l'argent
          qu'elle immobilise, soit <b>${(base.partCap||0).toFixed(2).replace('.',',')} %</b> du capital total.</div>`:''}
        ${q===0?`<div class="rk">Conservée pour l'historique : elle a déjà été vendue, ses prix
          et son code-barres restent disponibles pour un réassort.</div>`:''}
        ${cpt}
        ${blocStockSites(base)}
        <!-- 12 oct. 2026 (Igal : « ça porte à confusion », puis « laisse-moi une case avec le prix qu'il y a sur Lightspeed ») : plus de cartes gros / retail ;
             la carte du prix d'achat reste, et UNE carte « Lightspeed » : le prix boutique que l'outil envoie à la caisse, avec le dernier prix réellement encaissé en caisse. -->
        <div class="drail mini">${VPA?etape('pa','achat moyen',null,false,dernierPrixPaye(p)):''}${etape('pvr','Lightspeed · prix boutique',null,true,dernierPrixCaisse(p))}</div>
      </div>
    </div>
    ${chips.length?`<div class="dchips">${chips.join('')}</div>`:''}

    ${blocVentes(p)}

    <details class="dsec dcanw" open><summary><h3>Mes canaux de vente<span class="hh">${(()=>{ const off=canaux().filter(c=>c.id!=='boutique'&&c.id!=='amazon'&&horsCanal(p,c.id));
        return off.length?`<b style="color:var(--crit)">pas vendu sur ${off.map(c=>esc(c.nom)).join(', ')}</b> · `:''; })()}<a href="reglages.html?v=__VER__">régler les canaux</a></span></h3></summary>
      <!-- 11 oct. 2026 (Igal : « refais-moi cette partie plus clairement ») : une ligne par canal, quatre
           colonnes toujours aux mêmes places — le canal, le prix de l'outil, ce que le client paie
           vraiment (site, annonce Amazon), ce qu'il te reste. Le prix Amazon est celui de l'annonce de
           Sam (rapport des annonces importé dans le cockpit), plus un prix calculé. -->
      <div class="dcan dcanl">
        <div class="cnh"><span>Canal</span><span>Prix de l'outil</span><span>Le client paie</span>${VMG?'<span>Il te reste</span>':'<span></span>'}<span></span></div>
        ${canaux().filter(c=>c.id!=='boutique'&&c.id!=='amazon').sort((x,y)=>(y.id==='sitegros')-(x.id==='sitegros')).map(c=>{
        /* 11 oct. 2026 (Igal : « inverse les deux canaux ») : wholesale d'abord, puis retail. Amazon : la ligne Amazon est retirée — son prix ne peut pas être connu
           sans rapport, « elle ne sert à rien ». Amazon reste un canal pour les ventes reçues. */
        const tete=`<span class="nm" title="${esc(c.nom)}">${c.id==='sitegros'?logo('site',c.nom)+'<span class="sous">wholesale</span>':logo(c.id,c.nom)}</span>`
          +(CANAL_ETAT[c.id]?`<span class="etat ${CANAL_ETAT[c.id][0]}">${CANAL_ETAT[c.id][1]}</span>`:'')
          +(()=>{ const inf={}, u=lienCanal(p,c,inf);
            return u?`<a class="cvoir" href="${esc(u)}" target="_blank" rel="noopener" title="${esc(inf.brouillon?L3('Brouillon : pas visible du public. Ouvre l\'aperçu (il faut être connecté à l\'administration du site).','Draft: not public. Opens the preview (you must be logged in to the site admin).','Borrador: no es público. Abre la vista previa (hay que estar conectado a la administración del sitio).'):L3('Ouvrir ce parfum sur ','Open this perfume on ','Abrir este perfume en ')+c.nom)}">${inf.brouillon?L3('Voir le brouillon','See the draft','Ver el borrador'):L3('Voir sur la boutique','See on the shop','Ver en la tienda')} ↗</a>`:''; })();
        if(horsCanal(p,c.id)) return `<div class="cn off"><div class="c1">${tete}</div>
          <div class="c2"><span class="offtx">pas vendu ici</span></div><div class="c3"></div><div class="c4"></div>
          <div class="c5"><button class="offb" data-on="${c.id}">Remettre ce canal</button></div></div>`;
        /* Igal, 17 oct. 2026 (le gros) : « le prix de l'outil, ce que le client paie, un avertissement, et une case "prix de vente" : ça porte
           à confusion, il faut juste un endroit où noter le prix ». Pour le site de gros, quand on connaît son prix en ligne : UNE case, ce prix.
           Elle part sur le site à l'Enregistrer, et l'outil reprend ce prix (voir envoiePrixSite) ; plus de ligne « ⚠ pas 19 », plus de second prix. */
        /* Précision d'Igal, même jour : « cette partie reste intéressante seulement quand il y a un cross price (prix barré + promo). Sinon aucun
           intérêt de laisser les prix sur deux cases différentes. » Donc : le site de détail aussi n'a qu'UNE case tant qu'il n'a pas de promo ;
           avec une promo (prix barré + prix payé), il garde ses deux cases. Le gros n'a jamais qu'un prix. */
        const fG=COTE_SITE[c.id]?((siteDe(p)||{})[COTE_SITE[c.id]]):null;
        /* 5 nov. 2026 (Igal) : le détail a toujours la même ligne — prix retail à gauche, case « prix barré » à droite ; le mode une-case reste au gros */
        const uni=!!(fG&&fG.pr!==undefined&&(fG.ps!=null?fG.ps:fG.pr)!=null&&c.id==='sitegros');
        /* 10 nov. 2026 (Igal : « le Catalogue dit 53,76 $, la fiche dit 85 $ ») : la case affiche le prix de gros de la FICHE, plus celui du site */
        let {v,man,src}=prixCanal(p,c); if(uni&&v==null){ v=fG.ps!=null?fG.ps:fG.pr; }
        const t=margeNette(p,c,v), chg=FICHE.brouillon.pc&&FICHE.brouillon.pc[c.id]!==undefined;
        const frais=v!=null?r2(v*(c.com||0)/100):null, reste=(v!=null&&p.pa!=null)?r2(v-(frais||0)-p.pa):null;
        const calc = !VMG ? '' : v==null ? `<span class="calc vide">Pas de prix : tape-le.</span>`
          : p.pa==null ? `<span class="calc vide">Prix d'achat inconnu.</span>`
          : `<div class="calc2"><b class="${pcCls(t)}">${money2(reste)}</b><small>${pc(t)} du prix</small>
             <span>${money2(v)}${c.com?` − ${money2(frais)} ${L3('frais','fees','gastos')} (${String(c.com).replace('.',',')} %)`:''} − ${money2(p.pa)} ${L3('achat','purchase','compra')}</span></div>`;
        /* colonne 3 : ce que le client paie vraiment */
        let paie='';
        if(c.id==='site'||c.id==='sitegros'){
          /* une seule ligne : ce que le client paie ; les cases (prix barré, promo, envoyer) sous « régler » */
          const e=siteDe(p), f=e&&e[COTE_SITE[c.id]];
          const box=surSite(p,c,v);
          paie = !f ? (retireCote(p,COTE_SITE[c.id])&&peutPrixSite() ? `<div class="sbd">${box}</div>` : `<div class="azp"><small>${L3(retireCote(p,COTE_SITE[c.id])?'retirée de la vente':'pas sur ce site',retireCote(p,COTE_SITE[c.id])?'taken off sale':'not on this site',retireCote(p,COTE_SITE[c.id])?'retirada de la venta':'no está en este sitio')}</small>${!retireCote(p,COTE_SITE[c.id])&&peutPrixSite()&&p.qte>0&&melOk()?`<button class="lnk" data-mel1="${c.id}">Mettre en ligne</button>`:''}</div>`)
            /* Igal, 11 oct. 2026 : « je veux que tu me les laisses ouvertes » — les cases restent visibles */
            : `<div class="sbd">${box}</div>`; }
        else if(c.id==='amazon'){ const az=prixAmazonDe(p);
          paie = az ? `<div class="azp"><span class="sbt">sur Amazon</span><b data-nolang>${money2(az.prix)}</b>${az.qte!=null?`<small>${nf(az.qte)} ${L3('en vente','on sale','en venta')}</small>`:''}<small>${L3('annonce du','listing of','anuncio del')} ${az.le?jourFr(String(az.le).slice(0,10)):'—'}</small>
              ${v!=null&&Math.abs(v-az.prix)>=0.005?`<div class="sbw">⚠ ${L3('Amazon vend à','Amazon sells at','Amazon vende a')} <b>${money2(az.prix)}</b>, ${L3('pas','not','no')} <b>${money2(v)}</b>. <button class="lnk" data-prend="amazon" data-pv="${az.prix}">${L3('prendre le prix Amazon','use the Amazon price','usar el precio de Amazon')}</button></div>`:''}</div>`
            : `<div class="azp"><span class="sbt">sur Amazon</span><small>${L3('prix inconnu : importe le rapport des annonces dans le cockpit','unknown price: import the listings report in the cockpit','precio desconocido: importa el informe de anuncios en el cockpit')}</small></div>`; }
        else if(c.id==='perfumecity'){ const sh=prixShopifyDe(p);
          paie = !sh ? `<div class="azp"><span class="sbt">sur Shopify</span><small>${L3('pas trouvé : le code-barres n\'est pas sur Shopify','not found: the barcode is not on Shopify','no encontrado: el código de barras no está en Shopify')}</small>${peutPrixSite()&&p.qte>0&&melOk()?`<button class="lnk" data-mel1="perfumecity">${L3('Mettre en ligne','Put online','Poner en línea')}</button>`:''}</div>`
            : sh.amb ? `<div class="azp"><span class="sbt">sur Shopify</span><small class="sbw">⚠ ${L3('ce code-barres est sur plusieurs produits de Shopify : à corriger là-bas','this barcode is on several Shopify products: fix it there','este código está en varios productos de Shopify: corrígelo allí')}</small></div>`
            : `<div class="azp"><span class="sbt">sur Shopify</span><b data-nolang>${money2(sh.prix)}</b>${sh.actif?(peutPrixSite()&&(qtePCde(p)>0||p.qte>0)&&melOk()?`<button class="lnk" data-pcpub="${esc(p.bc||'')}" title="${L3('Repose le stock de l\'inventaire Perfume City et publie le produit sur les canaux de vente de la boutique','Re-posts the Perfume City inventory stock and publishes the product on the shop\'s sales channels','Vuelve a poner el stock del inventario Perfume City y publica el producto en los canales de la tienda')}">${L3('Publier / stock '+nf(qtePCde(p)),'Publish / stock '+nf(qtePCde(p)),'Publicar / stock '+nf(qtePCde(p)))}</button>`:''):`<small>${L3('brouillon','draft','borrador')}</small>${peutPrixSite()&&(qtePCde(p)>0||p.qte>0)&&melOk()?`<button class="lnk" data-pcpub="${esc(p.bc||'')}">${L3('Mettre en vente (stock Perfume City : '+nf(qtePCde(p))+')','Put on sale (Perfume City stock: '+nf(qtePCde(p))+')','Poner en venta (stock Perfume City: '+nf(qtePCde(p))+')')}</button>`:''}`}${sh.barre?`<small>${L3('barré','was','tachado')} ${money2(sh.barre)}</small>`:''}
              ${v!=null&&Math.abs(v-sh.prix)>=0.005?`<div class="sbw">⚠ ${L3('Shopify vend à','Shopify sells at','Shopify vende a')} <b>${money2(sh.prix)}</b>, ${L3('pas','not','no')} <b>${money2(v)}</b>. ${prixPCOk()?`<span>${L3('Enregistrer envoie le nouveau prix à Shopify.','Save sends the new price to Shopify.','Guardar envía el nuevo precio a Shopify.')}</span> `:''}<button class="lnk" data-prend="perfumecity" data-pv="${sh.prix}">${L3('prendre le prix Shopify','use the Shopify price','usar el precio de Shopify')}</button></div>`:''}</div>`; }
        else paie=`<div class="azp"><small>${L3('ventes non reliées','sales not connected','ventas no conectadas')}</small></div>`;
        if(uni) return `<div class="cn uni" data-cn="${c.id}">
          <div class="c1">${tete}</div>
          <div class="c2"><div class="usb" data-sbx="${c.id}" style="display:contents">${peutPrixSite()
            ? `<div class="in"><input data-sb="${c.id}" type="number" step="0.01" min="0" inputmode="decimal" value="${Number(v).toFixed(2)}"><em>$</em></div>`
            : `<div class="in"><b data-nolang style="font-size:24px">${money2(v)}</b></div>`}
            <span class="rl">${L3('prix de vente','selling price','precio de venta')}</span></div>
            </div>
          <div class="c3"></div>
          <div class="c4">${calc}</div>
          <div class="c5"><button class="offb" data-off="${c.id}" title="Ce parfum n'est pas vendu sur ${esc(c.nom)}">ne pas vendre ici</button></div>
        </div>`;
        return `<div class="cn${man?' man':''}${chg?' ch':''}" data-cn="${c.id}">
          <div class="c1">${tete}</div>
          <div class="c2"><div class="in"><input data-pc="${c.id}" type="number" step="any" inputmode="decimal" value="${v==null?'':v}" placeholder="—"><em>$</em></div>
            <span class="rl">${man?`saisi à la main · <button data-pcr="${c.id}">revenir au calcul</button>`:esc(sourcePrix(p,c,false,src))}</span></div>
          <div class="c3">${paie}</div>
          <div class="c4">${calc}</div>
          <div class="c5"><button class="offb" data-off="${c.id}" title="Ce parfum n'est pas vendu sur ${esc(c.nom)}">ne pas vendre ici</button></div>
        </div>`; }).join('')}</div>
      ${p.src?`<div class="dinfo">Le prix retail vient de <b>perfumestrade.com</b>, il n'était pas dans l'inventaire.
        ${p.src===2&&VPA?'<b style="color:var(--crit)">Il est inférieur ou égal au prix d\'achat</b> — à ne pas reprendre tel quel.':'À valider.'}</div>`:''}
    </details>

    ${VPA?blocHistorique(p):''}


    <!-- 11 oct. 2026 (Igal : « arrange-moi cette partie, vraiment pas jolie ») : une seule carte
         propre — les champs encadrés sur trois colonnes, les autres codes en champ facultatif avec
         une courte aide, les fournisseurs en dessous, et l'état de la fiche en une ligne. -->
    <div class="dsec dident"><h3>Identification</h3>
      <div class="dcard">
        <div class="dgrid dg3">${CH.slice(0,6).map(champ).join('')}</div>
        <div class="dgrid" style="grid-template-columns:1fr;margin-top:10px">${[['bcs','Autres codes-barres de la même référence','-','txt','ex. 3348900012345, 3348900012346']].map(champ).join('')}</div>
        <div class="dhint">Le même parfum arrive parfois sous un autre code (autre lot, emballage, coffret) : chacun de ces codes ramène à cette fiche.</div>
        <div class="dline"><span>Nom d'origine dans le fichier : <b data-nolang>${esc(p.nomSrc||p.nom||'—')}</b></span>
          <span>Photo : ${p.img?'<b>oui</b>':'<b style="color:var(--warn)">aucune</b>'}</span>
          <span>${mq.length?`À compléter : <b style="color:var(--warn)">${mq.join(', ')}</b>`:'<b style="color:var(--good)">Fiche complète</b>'}</span></div>
      </div>
    </div>

    ${VPA?`<div class="dsec dfrns"><h3>Fournisseurs</h3>
      <div class="dcard">
        ${frnHtml||'<div class="dhint">Aucun fournisseur enregistré pour cette référence.</div>'}
        <div class="dbtns"><button class="btn" id="dfrn">+ Ajouter un fournisseur</button></div>
        <div id="dfsyn">${synthFrn()}</div>
      </div>
    </div>`:''}`;
  const n=Object.keys(FICHE.brouillon).length;
  $('dst').textContent=n?`${n} modification${n>1?'s':''} non enregistrée${n>1?'s':''}`:'';
  $('dst').className='st';
}

function synthFrn(){
  const l=FICHE.frn.filter(f=>f.n&&f.p!=null).map(f=>({n:f.n,p:+f.p}));
  if(FICHE.frn.length<2) return '';
  if(l.length<2) return '<div class="dinfo">Renseigne le prix de chaque fournisseur pour comparer.</div>';
  l.sort((a,b)=>a.p-b.p);
  const best=l[0], worst=l[l.length-1], ec=worst.p-best.p;
  const pct=worst.p>0?(ec/worst.p*100):0;
  return `<div class="dinfo">Cette référence a <b>${FICHE.frn.length} fournisseurs</b>.
    Le meilleur prix est <b>${money(best.p)}</b> chez <b>${esc(best.n)}</b>`+
    (ec>0?`, soit <b style="color:var(--good)">${money(ec)} de moins</b> que ${esc(worst.n)}
     (${pct.toFixed(1).replace('.',',')} %).`:'.')+`</div>`;
}

/* --- interactions de la fiche ---
   La fiche recalcule les marges en se redessinant entièrement. Un champ redessiné est un
   champ recréé : le curseur repart au début, la sélection est perdue, et les chiffres tapés
   se collent devant l'ancienne valeur (126 + « 160 » donnait « 160126 »). Règle appliquée :
   TANT QU'UNE CASE DE LA FICHE A LE FOCUS, ON NE REDESSINE PAS. Le recalcul se fait quand on
   quitte les cases (clic ailleurs, Tab hors du groupe), ou à l'enregistrement. */
let T_REDRAW=0;
const enSaisie=()=>{ const a=document.activeElement; return !!(a&&a.dataset&&(a.dataset.k!==undefined||a.dataset.pc!==undefined||a.dataset.sb!==undefined||a.dataset.sp!==undefined)); };
function redessineApres(){
  clearTimeout(T_REDRAW);
  const marque=$('dst');
  if(marque && !/non enregistré/.test(marque.textContent||'')){
    marque.textContent='modifié — non enregistré'; marque.className='st';
  }
  T_REDRAW=setTimeout(function attends(){
    if(!FICHE) return;
    if(enSaisie()){ T_REDRAW=setTimeout(attends,400); return; }  /* on écrit encore : on repasse plus tard */
    redessineFiche();
  },400);
}
let RD=false;
function redessineFiche(){
  if(RD||!FICHE||enSaisie()) return;
  RD=true;
  try{ dessineFiche(); } finally{ setTimeout(()=>{ RD=false; },0); }
}
$('ddb').addEventListener('input',e=>{
  const t=e.target;
  if(t.dataset.sb!==undefined||t.dataset.sp!==undefined){ majEnvoi(t.dataset.sb||t.dataset.sp); return; }
  if(t.dataset.sr!==undefined||t.dataset.srp!==undefined){ marqueSite(); return; }
  /* 9 nov. 2026 : la case d'un site EST le prix retail / de gros de la fiche (plus de prix « manuel » à part) */
  if(t.dataset.pc==='site'||t.dataset.pc==='sitegros'){
    const id=t.dataset.pc, base=cur[FICHE.pos], k=id==='site'?'pvr':'pvw', c=canaux().find(x=>x.id===id)||{};
    const v = t.value===''? null : r2(+t.value/(1+(c.maj||0)/100));
    FICHE.brouillon[k]=v; if((base[k]??null)===(v??null)) delete FICHE.brouillon[k];
    const pc=Object.assign({},FICHE.brouillon.pc||{});
    if((base.pc||{})[id]!=null) pc[id]=null; else delete pc[id];
    if(Object.keys(pc).length) FICHE.brouillon.pc=pc; else delete FICHE.brouillon.pc;
    redessineApres();
    return;
  }
  if(t.dataset.pc){
    const id=t.dataset.pc, base=cur[FICHE.pos];
    const v = t.value===''? null : +t.value;
    const pc=Object.assign({},FICHE.brouillon.pc||{}); pc[id]=v;
    const bv=(base.pc||{})[id];
    if((bv??null)===(v??null)) delete pc[id];
    if(Object.keys(pc).length) FICHE.brouillon.pc=pc; else delete FICHE.brouillon.pc;
    redessineApres();
    return;
  }
  if(t.dataset.k){
    const k=t.dataset.k; let v=t.value;
    if(k==='qte') FICHE.qteTapee=true;   /* même chiffre retapé : on l'enverra quand même aux sites */
    if(NUM.has(k)) v = v===''? (k==='qte'?0:null) : +v;
    FICHE.brouillon[k]=v;
    const base=cur[FICHE.pos];
    if((base[k]??'')===(v??'')) delete FICHE.brouillon[k];
    redessineApres();
  }
  if(t.dataset.f){
    const i=+t.dataset.i;
    FICHE.frn[i][t.dataset.f] = t.dataset.f==='p' ? (t.value===''?null:+t.value) : t.value;
    const syn=$('dfsyn'); if(syn) syn.innerHTML=synthFrn();
    $('dst').textContent='fournisseurs modifiés — non enregistré'; $('dst').className='st';
  }
});
$('ddb').addEventListener('click',e=>{
  const per=e.target.closest('[data-per]');
  if(per){ PERIODE=per.dataset.per; dessineFiche(); return; }

  const ax=e.target.closest('[data-achx]');
  if(ax){
    const base=cur[FICHE.pos], i=+ax.dataset.achx, l=achats(base), x=l[i];
    if(!x||x.src==='fichier') return;
    if(!confirm(`Retirer l'achat du ${jourFr(x.d)} à ${money(x.p)} ?`)) return;
    if(!demandeUser(false,"retirer un achat",()=>ax.click())) return;
    HIST[base.id]=(HIST[base.id]||[]).filter(y=>!(y.d===x.d&&y.p===x.p&&y.f===x.f&&y.q===x.q));
    if(!HIST[base.id].length) delete HIST[base.id];
    sauveHIST();
    log({act:'prix',lib:"achat retiré de l'historique",bc:base.bc,
         ref:(base.marque||'')+' '+(base.nom||''),av:jourFr(x.d)+' · '+money(x.p),ap:null});
    dessineFiche(); return;
  }

  const an=e.target.closest('[data-ach]');
  if(an){ ouvreAchat(cur[FICHE.pos]); return; }

  const aj=e.target.closest('[data-ajust]');
  if(aj){ ouvreAjust(cur[FICHE.pos]); return; }

  const mr=e.target.closest('[data-mar]');
  if(mr){ ouvreMarche(); return; }

  const v=e.target.closest('[data-v]');
  if(v){
    const base=cur[FICHE.pos], id=base.id, nv=v.dataset.v;
    if(!demandeUser(false,"changer le statut de comptage",()=>v.click())) return;
    const m=Object.assign({},MOD[id]||{});
    m.verif=nv;
    let rendu=null;
    if(nv==='ok'){ m.verifPar=USR||'(non renseigné)'; m.verifLe=new Date().toISOString(); }
    else {
      delete m.verifPar; delete m.verifLe;
      /* déverrouiller, c'est défaire le comptage en entier : on rend la quantité d'avant,
         exactement comme le fait la page Stock. Sinon la fiche disait « jamais compté »
         alors que la quantité posée par ce comptage restait en vigueur. */
      if(m.qteC!=null && +m.qte===+m.qteC){
        rendu={de:+m.qte, a:(m.qteAv!=null?+m.qteAv:null)};
        if(m.qteAv!=null) m.qte=m.qteAv; else delete m.qte;
      }
      delete m.qteC; delete m.qteAv; delete m.qteTh0;
    }
    if(!Object.keys(m).length) delete MOD[id]; else MOD[id]=m;
    sauveMOD();
    log({act:'verif',lib:'statut de comptage'+(rendu?' — comptage défait, la quantité revient à celle d\'avant':''),
         bc:base.bc, ref:(base.marque||'')+' '+(base.nom||''),
         av:LIBV[base.verif||'']||'inconnu', ap:LIBV[nv]});
    if(rendu) log({act:'stock',lib:'comptage déverrouillé — quantité d\'avant rétablie',
         bc:base.bc, ref:(base.marque||'')+' '+(base.nom||''), av:rendu.de, ap:rendu.a});
    render();
    const l=cur.findIndex(x=>x.id===id); if(l>=0) FICHE.pos=l;
    dessineFiche();
    return;
  }
  const cof=e.target.closest('[data-off]'), con=e.target.closest('[data-on]');
  if(cof||con){
    const id=(cof||con).dataset.off||(cof||con).dataset.on;
    const base=cur[FICHE.pos];
    let L=offCour().slice();
    if(cof){ if(!L.includes(id)) L.push(id); } else L=L.filter(x=>x!==id);
    const baseL=Array.isArray(base.pcOff)?base.pcOff.slice().sort():[];
    if(JSON.stringify(L.slice().sort())===JSON.stringify(baseL)) delete FICHE.brouillon.pcOff;
    else FICHE.brouillon.pcOff=L;
    dessineFiche(); return;
  }
  const pd=e.target.closest('[data-prend]');
  if(pd&&(pd.dataset.prend==='amazon'||pd.dataset.prend==='perfumecity')){ /* « prendre le prix Amazon / Shopify » : le prix de l'outil pour ce canal devient celui de l'annonce */
    const pc=Object.assign({},FICHE.brouillon.pc||{}); pc[pd.dataset.prend]=+pd.dataset.pv; FICHE.brouillon.pc=pc; dessineFiche(); return; }
  if(pd){ const box=document.querySelector(`[data-sbx="${pd.dataset.prend}"]`); if(box){
      const sb=box.querySelector('[data-sb]'); if(sb) sb.value=(+pd.dataset.pv).toFixed(2);
      majEnvoi(pd.dataset.prend); } return; }
  const pr=e.target.closest('[data-pcr]');
  if(pr){ const id=pr.dataset.pcr, base=cur[FICHE.pos];
    const pc=Object.assign({},FICHE.brouillon.pc||{});
    if((base.pc||{})[id]!=null) pc[id]=null; else delete pc[id];
    if(Object.keys(pc).length) FICHE.brouillon.pc=pc; else delete FICHE.brouillon.pc;
    dessineFiche(); return; }
  if(e.target.id==='dfrn'){ FICHE.frn.push({n:'',p:null}); dessineFiche();
    const l=$('ddb').querySelectorAll('[data-f="n"]'); if(l.length) l[l.length-1].focus(); }
  const x=e.target.closest('[data-fx]');
  if(x){ FICHE.frn.splice(+x.dataset.fx,1); dessineFiche(); }
});
/* --- confirmation des prix : ce qui change, canal par canal, avec la marge et le plancher --- */
function lignesPrix(){
  const base=cur[FICHE.pos], b=FICHE.brouillon;
  const p=Object.assign({},base,b); p.pc=Object.assign({},base.pc||{},b.pc||{});
  const L=[]; const ref=(base.marque||'')+' '+(base.nom||'');
  const paChg=b.pa!==undefined&&(base.pa??null)!==(b.pa??null);
  if(paChg) L.push({lib:"Prix d'achat",av:base.pa,ap:b.pa,mg:null,st:'na',txt:'change tous les planchers'});
  const vente=(lib,av,ap,com,force)=>{
    if(!force&&(av??null)===(ap??null)) return;
    const mg=margeNette(p,{com},ap), pl=plancher(p,com);
    let st='ok',txt=mg==null?'marge inconnue':'marge nette '+pct1(mg), cls='';
    if(ap==null){ st='na'; txt='vide'; }
    else if(pl===Infinity){ st='ko'; txt=`aucun prix ne tient : ${com} % de commission + ${REG.margeMin||0} % de marge minimum dépassent 100 %`; cls='bad'; }
    else if(pl!=null&&ap<pl){ st='ko'; txt=`sous le plancher (min ${money(pl)})`; cls='bad'; }
    else if(mg!=null&&mg<(REG.margeMin||0)){ st='wa'; txt='marge nette '+pct1(mg)+' — sous le seuil'; }
    if(av!=null&&ap!=null&&(ap>=av*5||ap<=av/5)){ cls=cls||'big'; txt+=av<ap?` · ×${(ap/av).toFixed(0)} par rapport à avant`:` · ÷${(av/ap).toFixed(0)} par rapport à avant`; }
    L.push({lib,av,ap,mg,st,txt,cls,inchange:(av??null)===(ap??null)});
  };
  vente('Prix de gros',base.pvw,p.pvw,0,paChg);
  vente('Prix retail',base.pvr,p.pvr,0,paChg);
  const pvrChg=b.pvr!==undefined&&(base.pvr??null)!==(b.pvr??null);
  canaux().forEach(c=>{
    if(horsCanal(p,c.id)) return;      /* canal coupé pour ce parfum : rien à confirmer */
    const av=prixCanal(base,c).v, ap=prixCanal(p,c).v;
    const manChg=b.pc&&b.pc[c.id]!==undefined;
    vente(c.nom+(prixCanal(p,c).man?' (manuel)':''),av,ap,c.com||0,paChg||pvrChg||manChg);
  });
  return L;
}
function confirmePrix(L,envois){
  envois=envois||[];
  const ko0=L.some(l=>l.st==='ko');
  /* 9 oct. 2026 (Igal : « pour Sam et moi, si on décide de vendre au prix d'achat ou à perte,
     ne refuse jamais ») : le Patron et l'admin voient l'avertissement mais enregistrent quand
     même, et le prix part aussi aux sites. Les autres comptes restent bloqués sous le plancher. */
  const libre=peutPrixSite(), ko=ko0&&!libre;
  /* 20 oct. 2026 (Igal : « Sam est obligé de valider plusieurs fois le changement de prix, en cliquant sur plusieurs fenêtres à la suite ») :
     UNE seule fenêtre à l'Enregistrer. Elle montre tout : les prix tapés dans les cases des sites (WooCommerce), celui de Perfume City
     (Shopify) et les prix de l'outil. Un seul « Enregistrer » les valide et les envoie, sans autre question. */
  const resume=envois.length?`<div class="pxenv" style="margin:0 0 14px"><p style="margin:0 0 8px"><b>${L3('Envoyé tout de suite sur les sites :','Sent to the websites right away:','Enviado a los sitios de inmediato:')}</b></p>${envois.map(m=>`<p style="white-space:pre-line;margin:0 0 10px;padding:8px 10px;border-left:3px solid var(--iris);background:var(--surface-2);font-size:13px;line-height:1.5">${esc(vf(String(m)).replace(/\n\n[^\n]*Continuer \?\s*$/,'').replace(/\n*Continuer \?\s*$/,''))}</p>`).join('')}</div>`:'';
  $('pxb').innerHTML=resume+(L.length?`<table class="pxt"><thead><tr><th>Prix</th><th class="r">Avant</th><th class="r">Après</th><th>Résultat</th></tr></thead>
    <tbody>${L.map(l=>`<tr class="${l.cls||''}"><td>${esc(l.lib)}${l.inchange?' <span class="st na">(inchangé)</span>':''}</td>
      <td class="r av">${l.av==null?'—':money(l.av)}</td><td class="r ap">${l.ap==null?'—':money(l.ap)}</td>
      <td><span class="st ${l.st}">${esc(l.txt)}</span></td></tr>`).join('')}</tbody></table>`:'')+`
    <div class="pxnote">${ko?`<b>Un prix est sous le plancher.</b> Le plancher, c'est le prix d'achat plus ${REG.margeMin||0} % de marge minimum,
      commission du canal comprise. Corrige-le dans la fiche : rien n'est enregistré tant qu'il est là.`
      :ko0?`<b>Un prix est sous le plancher — tu peux quand même l'enregistrer.</b> Le plancher, c'est le prix d'achat plus ${REG.margeMin||0} % de marge minimum,
      commission du canal comprise. Rien n'est refusé : tu décides, et le prix part au journal avec ton nom.`
      :`<b>Vérifie les marges avant de valider.</b> La marge nette tient compte de la commission de chaque canal.
      Une fois enregistré, chaque prix part au journal avec ton nom, la date et l'heure.`}</div>`;
  /* Sam, 3 oct. 2026 (Opium pour Homme à 95 $, « ça n'a pas changé sur WooCommerce ») : ce que
     ce nouveau prix change sur les sites, dans la MÊME fenêtre, coché d'office. Décoché, les
     sites gardent leur prix. */
  if(!ko&&prixSitesOk()&&(!envois.length||L.length)){   /* des cases de sites SEULES (aucun prix d'outil touché) : pas de proposition en plus */
    const base=cur[FICHE.pos], d=Object.assign({},base,FICHE.brouillon);
    d.pc=Object.assign({},base.pc||{},FICHE.brouillon.pc||{}); Object.keys(d.pc).forEach(k=>{ if(d.pc[k]==null) delete d.pc[k]; });
    /* un site dont la case est en attente reçoit CE qui est tapé dans sa case (envoyé juste avant) : le prix de l'outil ne le repasse pas */
    const excl=envois.length?boitesEnAttente().map(x=>x.cid):[];
    let {plan,bas,garde}=planPrixSites(d); plan=plan.filter(x=>!excl.includes(x.cid));
    if(plan.length||bas.length||garde.length) $('pxb').insertAdjacentHTML('beforeend',`<div class="pxsit">
      ${plan.length?`<label class="pxsc"><input type="checkbox" id="pxsites" checked> <span>Mettre aussi ces prix sur les sites</span></label>
      <ul>${plan.map(x=>`<li>${lignePlanSite(x)}</li>`).join('')}</ul>`:''}
      ${bas.length?`<p class="pxbas">Sous le prix d'achat : pas envoyé sur ${esc(bas.join(', '))}.</p>`:''}
      ${garde.length?`<p class="pxbas"><span>Le prix de l'outil dépasse le prix barré du site : rien n'est changé sur</span> ${esc(garde.join(', '))}. <span>Règle le prix barré et la promo dans la case « sur le site ».</span></p>`:''}</div>`);
  }
  $('pxok').disabled=ko; $('pxmsg').textContent=ko?'enregistrement bloqué':'';
  $('pxov').classList.add('on');
}
$('pxx').onclick=$('pxc').onclick=()=>{ $('pxov').classList.remove('on'); if(FICHE){ FICHE.envoisSites=false; FICHE.repForce=null; } };
$('pxok').onclick=async()=>{
  if(!FICHE) return;
  FICHE.pxSites=!!($('pxsites')&&$('pxsites').checked); $('pxov').classList.remove('on');
  FICHE.pxExclu=FICHE.envoisSites?boitesEnAttente().map(x=>x.cid):[];
  /* les prix des cases des sites et de Perfume City partent maintenant, SANS reposer de question : cette fenêtre est leur validation */
  if(FICHE.envoisSites){
    FICHE.envoisSites=false;   /* les sites dont la case est en attente sont exclus du prix de l'outil (pxExclu) ; les autres suivent la case cochée */
    $('dok').disabled=true;
    try{
      if(boitesEnAttente().length && !(await envoieBoitesSite('envoie'))) return;
      if(!FICHE) return;
      if(pcShopEnAttente() && !(await envoiePCShopify('envoie'))) return;
    } finally { $('dok').disabled=false; if(FICHE) FICHE.repForce=null; }
    if(!FICHE) return;
  }
  enregistreFiche();
};

/* Le prix tapé pour Perfume City part sur Shopify à l'Enregistrer (15 oct. 2026), comme les cases des sites WooCommerce :
   un seul produit, confirmé, par le Patron ou l'admin ; le cockpit relit le produit juste avant d'écrire et refuse si le prix
   a changé entre-temps. Seule une modification tapée dans CETTE ouverture de fiche compte : un ancien prix manuel resté dans
   la fiche ne redemande rien à chaque enregistrement. */
function pcShopEnAttente(){
  if(!prixPCOk()||!FICHE) return null;
  const base=cur[FICHE.pos], b=FICHE.brouillon.pc&&FICHE.brouillon.pc.perfumecity;
  if(!base||b==null||b==='') return null;
  const sh=prixShopifyDe(base); if(!sh||sh.amb||!(sh.prix>0)) return null;
  const n=Math.round(+b*100)/100; if(!(n>0)||Math.abs(n-sh.prix)<0.005) return null;
  return {k:sh.k,nouveau:n,attendu:sh.prix,base};
}
async function envoiePCShopify(mode){
  const x=pcShopEnAttente(); if(!x) return true;
  const {base}=x, p=Object.assign({},base,FICHE.brouillon);
  const ref=(base.marque||'')+' '+(base.nom||'');
  const sousPA=(p.pa!=null&&x.nouveau<p.pa), ec=x.attendu?Math.abs(x.nouveau-x.attendu)/x.attendu*100:0;
  /* qui ne voit pas les prix d'achat n'apprend jamais le prix d'achat par un message d'erreur : on refuse sans le chiffre */
  const voitPA=typeof peut!=='function'||peut('voirPA');
  if(sousPA&&!peutPrixSite()){ alert(vf('Ce prix est trop bas : le prix n\'a pas été changé sur Shopify.\n\nDemande au patron.')); return false; }
  const msg=`« ${ref} » chez Perfume City (Shopify) :\n\nprix : ${money2(x.attendu)} → ${money2(x.nouveau)}\n\nLe client paiera ${money2(x.nouveau)}.`
    +(sousPA?`\n\nAttention : c'est moins que le prix d'achat${voitPA?' ('+money2(p.pa)+')':''}. Tu vends à perte.`:'')
    +(ec>20?`\n\nAttention : ${Math.round(ec)} % d'écart avec le prix affiché aujourd'hui.`:'')
    +`\n\nLe prix change tout de suite sur Shopify. Continuer ?`;
  if(mode==='resume') return msg;
  if(mode!=='envoie'&&!confirm(vf(msg))) return false;
  if(!demandeUser(false,'changer un prix sur Shopify',()=>{})) return false;
  try{
    const r=await fetch(CK_URL+'/api/o/'+CK_ORG+'/shopify/prix',{method:'POST',
      headers:{'Content-Type':'application/json',Authorization:'Bearer '+ckTok()},
      body:JSON.stringify({bc:base.bc,prix:x.nouveau,attendu:x.attendu})});
    const j=await r.json().catch(()=>({}));
    if(j&&j.avant!=null&&!j.ok) PCSHOP_OVR[x.k]=j.avant;      /* même en cas de refus : l'outil montre le vrai prix de Shopify */
    if(!r.ok) throw new Error(j.erreur||('erreur '+r.status));
    PCSHOP_OVR[x.k]=j.apres;
    /* le prix de Shopify est maintenant celui de l'outil : plus rien d'« en attente » pour ce canal */
    const b=FICHE.brouillon; if(b.pc){ delete b.pc.perfumecity; if(!Object.keys(b.pc).length) delete b.pc; }
    const m=MOD[base.id]=MOD[base.id]||{}; if(m.pc){ delete m.pc.perfumecity; if(!Object.keys(m.pc).length) delete m.pc; } sauveMOD();
    if(!j.inchange) log({act:'prix',lib:'prix changé chez Perfume City (Shopify)',bc:base.bc,ref,av:money2(j.avant),ap:money2(j.apres)});
    render(); const l=cur.findIndex(y=>y.id===base.id); if(l>=0) FICHE.pos=l; dessineFiche();
    $('dst').textContent=vf(`${money2(j.apres)} en ligne chez Perfume City`); $('dst').className='st ok';
    return true;
  }catch(err){
    dessineFiche();
    alert(vf('Le prix n\'a pas été changé sur Shopify.\n\n')+(err&&err.message||''));
    return false;
  }
}
/* ---- Supprimer définitivement un produit (Igal, 17 oct. 2026) ----
   « un bouton sur la fiche catalogue quand je veux supprimer définitivement un produit, avec une deuxième validation ».
   Seulement un produit AJOUTÉ À LA MAIN (les ~3 800 fiches du fichier de départ portent l'historique des ventes, des
   achats et les liens avec les sites et la caisse : on ne les efface pas d'un clic), seulement le Patron et l'Admin
   (le droit « annuler »), et jamais un produit déjà dans une facture : l'historique de la facture le citerait encore.
   Deux validations : la fenêtre de confirmation, puis le mot SUPPRIMER à taper. Les sites et Lightspeed ne sont pas touchés. */
function supprimeProduit(){
  const F=FICHE; if(!F) return; const base=cur[F.pos]; if(!base||!base.neuf) return;
  if(!(typeof peut==='function'&&peut('annuler'))){ alert(L3('Seuls le Patron et l\'Admin suppriment un produit.','Only the Owner and the Admin can delete a product.','Solo el Dueño y el Admin pueden eliminar un producto.')); return; }
  AJ.forEach((o,k)=>{ if(o&&!o.id) o.id='a'+k; });          /* un produit sans identifiant le garde : l'index ne doit plus bouger */
  const id=base.id, nom=((base.marque||'')+' '+(base.nom||'')).trim()||id;
  const i=AJ.findIndex(o=>o&&o.id===id);
  if(i<0){ alert(L3('Ce produit n\'est pas un produit ajouté à la main : il ne peut pas être supprimé ici.','This product was not added by hand: it cannot be deleted here.','Este producto no se añadió a mano: no se puede eliminar aquí.')); return; }
  let facts=[]; try{ facts=(lit('factures-v1',[])||[]).filter(f=>f&&(f.lignes||[]).some(l=>l&&l.cle===id)); }catch(e){}
  if(facts.length){
    alert(L3(`« ${nom} » figure dans ${facts.length} facture${facts.length>1?'s':''} (${facts.slice(0,4).map(f=>f.num).join(', ')}${facts.length>4?'…':''}).\n\nIl ne peut pas être supprimé : l\'historique de ${facts.length>1?'ces factures':'cette facture'} le citerait encore.`,
      `"${nom}" is on ${facts.length} invoice${facts.length>1?'s':''} (${facts.slice(0,4).map(f=>f.num).join(', ')}${facts.length>4?'…':''}).\n\nIt cannot be deleted: the history would still mention it.`,
      `«${nom}» figura en ${facts.length} factura${facts.length>1?'s':''} (${facts.slice(0,4).map(f=>f.num).join(', ')}${facts.length>4?'…':''}).\n\nNo se puede eliminar: el historial lo seguiría citando.`));
    return; }
  const qte=+base.qte||0;
  if(!confirm(L3(`Supprimer définitivement « ${nom} » ?\n\nCode-barres : ${base.bc||'—'}\nStock : ${qte}\n\nLe produit disparaît du Catalogue. Les sites et Lightspeed ne sont pas touchés.`,
      `Permanently delete "${nom}"?\n\nBarcode: ${base.bc||'—'}\nStock: ${qte}\n\nThe product disappears from the Catalogue. The websites and Lightspeed are not touched.`,
      `¿Eliminar definitivamente «${nom}»?\n\nCódigo de barras: ${base.bc||'—'}\nStock: ${qte}\n\nEl producto desaparece del Catálogo. Los sitios y Lightspeed no se tocan.`))) return;
  const rep=prompt(L3(`Deuxième validation.\n\nPour supprimer « ${nom} » pour de bon, tape le mot SUPPRIMER :`,`Second confirmation.\n\nTo delete "${nom}" for good, type the word SUPPRIMER:`,`Segunda confirmación.\n\nPara eliminar «${nom}» definitivamente, escribe la palabra SUPPRIMER:`),'');
  if(rep==null||rep.trim().toUpperCase()!=='SUPPRIMER'){ alert(L3('Rien n\'a été supprimé.','Nothing was deleted.','No se eliminó nada.')); return; }
  AJ.splice(i,1); sauveAJ(); delete MOD[id]; sauveMOD();
  log({act:'suppression',lib:'produit supprimé définitivement — '+nom,bc:base.bc||'',ref:nom,av:qte,ap:null});
  fermeFiche(); render(); try{ remplitMarques(); }catch(e){}
}
/* ---- Modifier un parfum, le retirer du catalogue (Igal, 20 oct. 2026) ----
   « Je veux avoir la possibilité de modifier ou de supprimer un parfum. » Modifier : marque, nom, contenance, type, genre — sur
   n'importe quelle fiche, sans toucher au code-barres (c'est lui qui relie le parfum à l'historique, aux sites et à la caisse).
   Retirer : les ~3 800 fiches du fichier de départ portent l'historique des ventes et des achats ; on ne les efface donc pas,
   on les retire de la vue (réversible : filtre « Retirées du catalogue » › « Remettre au catalogue »). Refusé s'il reste du stock. */
function ouvreIdentite(){
  const F=FICHE; if(!F) return; const base=cur[F.pos]; if(!base) return;
  if(typeof peut==='function'&&!peut('modPrix')) return;
  let ov=$('idov');
  if(!ov){ ov=document.createElement('div'); ov.className='ov'; ov.id='idov'; document.body.appendChild(ov); }
  const g=base.genre||'';
  ov.innerHTML=`<div class="mod" role="dialog" aria-modal="true"><div class="mh"><h2>${L3('Modifier le parfum','Edit the perfume','Modificar el perfume')}</h2><button class="x" id="idx" aria-label="Fermer">&times;</button></div>
    <div class="mb"><div class="fg">
      <div class="fld"><label>${L3('Marque','Brand','Marca')} <b>*</b></label><input id="id-marque" list="l-marques" autocomplete="off" value="${esc(base.marque||'')}"></div>
      <div class="fld"><label>${L3('Nom du parfum','Perfume name','Nombre del perfume')} <b>*</b></label><input id="id-nom" autocomplete="off" value="${esc(base.nom||'')}"></div>
      <div class="fld"><label>${L3('Contenance (oz)','Size (oz)','Contenido (oz)')}</label><input id="id-ml" inputmode="decimal" autocomplete="off" value="${esc(base.ml||'')}"></div>
      <div class="fld"><label>${L3('Type','Type','Tipo')}</label><input id="id-type" list="l-types" autocomplete="off" placeholder="EDP, EDT…" value="${esc(base.type||'')}"></div>
      <div class="fld"><label>${L3('Genre','Gender','Género')}</label><select id="id-genre"><option value="">${L3('— inconnu —','— unknown —','— desconocido —')}</option><option value="M"${g==='M'?' selected':''}>${L3('Homme','Men','Hombre')}</option><option value="W"${g==='W'?' selected':''}>${L3('Femme','Women','Mujer')}</option><option value="U"${g==='U'?' selected':''}>${L3('Unisexe','Unisex','Unisex')}</option><option value="K"${g==='K'?' selected':''}>${L3('Enfant','Kids','Niños')}</option></select></div>
      <div class="fld"><label>${L3('Code-barres','Barcode','Código de barras')}</label><input id="id-bc" disabled value="${esc(base.bc||'')}"></div>
    </div>
    <p class="hint">${L3('Le code-barres ne se change pas ici : il relie ce parfum à son historique de ventes, aux sites et à la caisse. Les ventes passées restent attachées au parfum, avec le nouveau nom.','The barcode cannot be changed here: it links this perfume to its sales history, the websites and the register. Past sales stay attached to the perfume, under the new name.','El código de barras no se cambia aquí: une este perfume con su historial de ventas, los sitios y la caja. Las ventas pasadas siguen unidas al perfume, con el nuevo nombre.')}</p>
    <div class="msg" id="id-msg"></div></div>
    <div class="df"><span class="st"></span><button class="btn" id="id-ann">${L3('Annuler','Cancel','Cancelar')}</button><button class="btn pri" id="id-ok">${L3('Enregistrer','Save','Guardar')}</button></div></div>`;
  ov.classList.add('on');
  const ferme=()=>ov.classList.remove('on');
  $('idx').onclick=$('id-ann').onclick=ferme;
  $('id-ok').onclick=()=>enregistreIdentite(ferme);
  setTimeout(()=>{ try{ $('id-nom').focus(); }catch(e){} },60);
}
function enregistreIdentite(ferme){
  const F=FICHE; if(!F) return; const base=cur[F.pos]; if(!base) return;
  const v={marque:$('id-marque').value.trim(),nom:$('id-nom').value.trim(),ml:$('id-ml').value.trim().replace(',','.'),type:$('id-type').value.trim(),genre:$('id-genre').value};
  if(!v.marque||!v.nom){ $('id-msg').textContent=L3('La marque et le nom sont obligatoires.','Brand and name are required.','La marca y el nombre son obligatorios.'); return; }
  if(v.ml&&!/^\d+(\.\d+)?$/.test(v.ml)){ $('id-msg').textContent=L3('La contenance est un nombre (ex. 3.4).','The size is a number (e.g. 3.4).','El contenido es un número (p. ej. 3.4).'); return; }
  const chg=Object.keys(v).filter(k=>String(v[k]||'')!==String(base[k]||''));
  if(!chg.length){ ferme(); return; }
  if(!demandeUser(false,L3('modifier un parfum','edit a perfume','modificar un perfume'),()=>{})) return;
  const id=base.id, m=Object.assign({},MOD[id]||{}); chg.forEach(k=>{ m[k]=v[k]; });
  MOD[id]=m; sauveMOD();
  const avant=((base.marque||'')+' '+(base.nom||'')).trim(), apres=(v.marque+' '+v.nom).trim();
  log({act:'fiche',lib:'parfum modifié ('+chg.join(', ')+')'+(avant!==apres?' — « '+avant+' » devient « '+apres+' »':''),bc:base.bc||'',ref:apres,av:avant,ap:apres});
  ferme(); render(); const l=cur.findIndex(x=>x.id===id); if(l>=0){ FICHE.pos=l; dessineFiche(); }
  try{ remplitMarques(); }catch(e){}
}
function retireProduit(){
  const F=FICHE; if(!F) return; const base=cur[F.pos]; if(!base||base.neuf) return;
  if(!(typeof peut==='function'&&peut('annuler'))){ alert(L3('Seuls le Patron et l\'Admin retirent un parfum du catalogue.','Only the Owner and the Admin can remove a perfume from the catalogue.','Solo el Dueño y el Admin pueden quitar un perfume del catálogo.')); return; }
  const id=base.id, nom=((base.marque||'')+' '+(base.nom||'')).trim()||id;
  if(!demandeUser(false,L3('retirer un parfum du catalogue','remove a perfume from the catalogue','quitar un perfume del catálogo'),()=>{})) return;
  const m=Object.assign({},MOD[id]||{});
  if(base.masque){
    delete m.masque; delete m.masquePar; delete m.masqueLe;
    if(Object.keys(m).length) MOD[id]=m; else delete MOD[id];
    sauveMOD(); log({act:'fiche',lib:'parfum remis au catalogue — '+nom,bc:base.bc||'',ref:nom,av:null,ap:null});
  } else {
    const qte=+base.qte||0;
    if(qte>0){ alert(L3(`« ${nom} » a encore ${qte} flacon${qte>1?'s':''} en stock : il ne peut pas être retiré.\n\nMets d'abord son stock à 0 (inventaire ou vente), puis retire-le.`,`"${nom}" still has ${qte} bottle${qte>1?'s':''} in stock: it cannot be removed.\n\nSet its stock to 0 first, then remove it.`,`«${nom}» todavía tiene ${qte} frasco${qte>1?'s':''} en stock: no se puede quitar.\n\nPon primero su stock en 0 y luego quítalo.`)); return; }
    if(!confirm(L3(`Retirer « ${nom} » du catalogue ?\n\nIl disparaît de la liste, mais son historique de ventes et d'achats est conservé. Tu pourras le remettre : filtre « Retirées du catalogue », puis « Remettre au catalogue ». Les sites et Lightspeed ne sont pas touchés.`,`Remove "${nom}" from the catalogue?\n\nIt disappears from the list, but its sales and purchase history is kept. You can put it back: filter "Removed from the catalogue", then "Put back in the catalogue". The websites and Lightspeed are not touched.`,`¿Quitar «${nom}» del catálogo?\n\nDesaparece de la lista, pero se conserva su historial de ventas y compras. Podrás volver a ponerlo: filtro «Quitadas del catálogo» y luego «Volver a poner en el catálogo». Los sitios y Lightspeed no se tocan.`))) return;
    m.masque=true; m.masquePar=USR||''; m.masqueLe=new Date().toISOString(); MOD[id]=m; sauveMOD();
    log({act:'suppression',lib:'parfum retiré du catalogue — '+nom,bc:base.bc||'',ref:nom,av:qte,ap:null});
  }
  fermeFiche(); render();
}
/* CHANGER LA PHOTO (Igal, 17 oct. 2026) : « on peut pas modifier la photo du produit ».
   Choisie sur l'ordinateur ou prise au téléphone, réduite, gardée dans l'outil (photos-perso-v1),
   et affichée à la place de celle du site. Ça ne touche ni les sites ni Lightspeed. */
function photoDeFiche(){ const F=FICHE; return F&&cur[F.pos]; }
/* la photo est prête (choisie sur l'ordinateur, ou trouvée sur Internet) : on la range et on redessine */
function rangePhoto(base,u){
  if(typeof peut==='function'&&!peut('modPrix')) return;
  if(!demandeUser(false,L3('changer une photo','change a photo','cambiar una foto'),()=>{})) return;
  PHO[base.id]=u;
  try{ ecrit(KPHO,PHO); }catch(e){ delete PHO[base.id]; throw e; }
  const nom=((base.marque||'')+' '+(base.nom||'')).trim();
  log({act:'fiche',lib:'photo du produit changée — '+nom,bc:base.bc||'',ref:nom,av:null,ap:null});
  render(); const l=cur.findIndex(x=>x.id===base.id); if(l>=0) FICHE.pos=l; dessineFiche();
  const s2=$('dst'); if(s2){ s2.textContent=L3('photo changée','photo changed','foto cambiada'); s2.className='st ok'; }
  diffusePhoto(base,u);
}
/* Igal, 17 oct. 2026 : « je veux modifier la photo sur l'ERP et qu'elle arrive sur WooCommerce ». La photo part toute seule
   vers les canaux où le parfum existe déjà (les deux sites, Perfume City) ; là où il n'est pas, rien. Le résultat s'affiche
   dans la fiche. Pas de cockpit (hors ligne) : la photo reste dans l'outil, et on le dit. */
async function diffusePhoto(base,u){
  const s2=$('dst'); const dit=(t,cls)=>{ const e=$('dst'); if(e){ e.textContent=t; e.className='st'+(cls?' '+cls:''); } };
  if(typeof CK_URL==='undefined'||typeof ckTok!=='function'||!ckTok()){ dit(L3('photo changée — elle reste dans l\'outil (pas relié au cockpit)','photo changed — it stays in the tool (not connected to the cockpit)','foto cambiada — queda en la herramienta (sin cockpit)')); return; }
  const data=/^data:image\/(jpeg|png|webp);base64,/.test(u||'')?u:'';
  const url=/^https:\/\//.test(u||'')?u:'';
  if(!data&&!url) return;
  dit(L3('photo changée — envoi aux sites…','photo changed — sending to the websites…','foto cambiada — enviando a los sitios…'));
  try{
    const r=await fetch(CK_URL+'/api/o/'+CK_ORG+'/photo/diffuse',{method:'POST',headers:{'Content-Type':'application/json',Authorization:'Bearer '+ckTok()},
      body:JSON.stringify(Object.assign({bc:base.bc||'',nom:((base.marque||'')+' '+(base.nom||'')).trim()},data?{imageData:data}:{image:url}))});
    const j=await r.json().catch(()=>({}));
    if(!r.ok) throw new Error(j.erreur||('erreur '+r.status));
    const C=j.canaux||{}, N={site:'perfumestrade.com',sitegros:'wholesale.perfumestrade.com',perfumecity:'Perfume City'};
    const ok=Object.keys(N).filter(k=>C[k]&&C[k].ok).map(k=>N[k]);
    const ko=Object.keys(N).filter(k=>C[k]&&!C[k].ok&&!C[k].absent).map(k=>N[k]+' : '+(C[k].err||'refus'));
    /* la photo du site a changé : on la range aussi ici, pour que la colonne « Sur les sites » la voie */
    try{ Object.keys(COTE_SITE).forEach(k=>{ const c=C[k]; if(c&&c.ok&&c.img){ const kk=siteCle(base); const e=kk&&SITE[kk]&&SITE[kk][COTE_SITE[k]]; if(e) e.img=c.img; } }); ecrit(KSITE,SITE); _FMC=null; _SITE0=null; }catch(e){}
    if(ok.length) log({act:'site',lib:'photo envoyée sur '+ok.join(', ')+' — '+((base.marque||'')+' '+(base.nom||'')).trim(),bc:base.bc||'',ref:'',av:null,ap:null});
    dit((ok.length?L3('photo changée et envoyée sur ','photo changed and sent to ','foto cambiada y enviada a ')+ok.join(', '):L3('photo changée — ce parfum n\'est sur aucun site','photo changed — this perfume is not on any website','foto cambiada — este perfume no está en ningún sitio'))+(ko.length?' · '+ko.join(' · '):''),ko.length?'':'ok');
  }catch(e){ dit(L3('photo changée dans l\'outil, mais pas envoyée aux sites : ','photo changed in the tool, but not sent to the websites: ','foto cambiada en la herramienta, pero no enviada a los sitios: ')+((e&&e.message)||'')); }
}
async function changePhoto(fichier){
  const base=photoDeFiche(); if(!base||!fichier) return;
  if(typeof peut==='function'&&!peut('modPrix')) return;
  const st=$('dst');
  try{ rangePhoto(base,await photoReduite(fichier)); }
  catch(err){ if(st){ st.textContent=L3('Photo non enregistrée : ','Photo not saved: ','Foto no guardada: ')+(err&&err.message||''); st.className='st'; } }
}
/* Igal, 17 oct. 2026 : « chercher la photo sur Internet, proposer un choix, un clic pour l'intégrer » */
async function photoDuWeb(){
  const base=photoDeFiche(); if(!base) return;
  if(typeof peut==='function'&&!peut('modPrix')) return;
  const q=[base.marque,base.nom,base.ml?base.ml+' oz':'',base.type,'perfume'].map(v=>String(v||'').trim()).filter(Boolean).join(' ');
  const u=await photoWeb(q); if(!u) return;
  const b2=photoDeFiche(); if(!b2||b2.id!==base.id) return;
  try{ rangePhoto(b2,u); }catch(err){ const st=$('dst'); if(st){ st.textContent=L3('Photo non enregistrée : ','Photo not saved: ','Foto no guardada: ')+(err&&err.message||''); st.className='st'; } }
}
function photoOrigine(){
  const base=photoDeFiche(); if(!base||!PHO[base.id]) return;
  if(!(typeof peut!=='function'||peut('modPrix'))) return;
  delete PHO[base.id]; ecrit(KPHO,PHO);
  log({act:'fiche',lib:'photo du produit remise à l\'origine — '+((base.marque||'')+' '+(base.nom||'')).trim(),bc:base.bc||'',ref:((base.marque||'')+' '+(base.nom||'')).trim(),av:null,ap:null});
  render(); const l=cur.findIndex(x=>x.id===base.id); if(l>=0) FICHE.pos=l; dessineFiche();
}
$('ddb').addEventListener('click',e=>{
  if(e.target.closest('[data-phchg]')){ const f=$('dphf'); if(f){ f.value=''; f.click(); } return; }
  if(e.target.closest('[data-phweb]')){ photoDuWeb(); return; }
  if(e.target.closest('[data-phrst]')){ photoOrigine(); }
  if(e.target.closest('[data-phenv]')){ const b=photoDeFiche(); if(b&&b.img){ if(typeof peut==='function'&&!peut('modPrix')) return; diffusePhoto(b,b.img); } }
});
$('ddb').addEventListener('change',e=>{ if(e.target&&e.target.id==='dphf'&&e.target.files&&e.target.files[0]) changePhoto(e.target.files[0]); });
document.addEventListener('click',e=>{ const b=e.target.closest&&e.target.closest('[data-sbr-go]'); if(!b||!FICHE) return;
  const base=cur[FICHE.pos]; if(!base) return;
  FICHE.repForce=Object.assign({},FICHE.repForce,{[base.id+'|'+b.dataset.sbrGo]:true});
  $('dok').click(); });
$('dsup').onclick=supprimeProduit;
$('dmod').onclick=ouvreIdentite;
$('dret').onclick=retireProduit;
$('dok').onclick=async()=>{
  /* les prix tapés dans les cases du site partent d'abord (Igal, 12 oct. 2026) ; si on annule ou si le site refuse, rien d'autre n'est enregistré.
     20 oct. 2026 : une SEULE fenêtre de confirmation pour tout (cases des sites, Perfume City, prix de l'outil) — plus de fenêtres à la suite. */
  if(!FICHE) return;
  FICHE.envoisSites=false;
  const attente=boitesEnAttente(), pcA=pcShopEnAttente(), b=FICHE.brouillon;
  const prixChg=['pa','pvw','pvr'].some(k=>b[k]!==undefined)||b.pc!==undefined;
  if(attente.length||pcA){
    const envois=[];
    /* on valide d'abord, sans rien envoyer : un prix absurde (promo au-dessus du prix barré…) est refusé avant toute question */
    for(const x of attente){ const m=await (x.retire?remetsPrixSite(x.cid,'resume'):envoiePrixSite(x.cid,'resume')); if(m===false){ FICHE.repForce=null; return; } if(typeof m==='string') envois.push(m); }
    if(!FICHE) return;
    if(pcA){ const m=await envoiePCShopify('resume'); if(m===false) return; if(typeof m==='string') envois.push(m); }
    if(!FICHE) return;
    if(!envois.length){ if(prixChg){ confirmePrix(lignesPrix()); return; } enregistreFiche(); return; }
    FICHE.envoisSites=true;
    confirmePrix(prixChg?lignesPrix():[],envois); return;
  }
  if(prixChg){ confirmePrix(lignesPrix()); return; }
  enregistreFiche();
};
function enregistreFiche(){
  const id=FICHE.id;
  /* Igal, 1er oct. 2026 : « quand je vais dans quantité en stock, il y a écrit zéro, mais le
     site dit 32 — je veux pouvoir la mettre à zéro et qu'elle apparaisse à zéro sur les sites ».
     Retaper le même chiffre ne change rien chez nous, donc l'envoi automatique ne partait
     pas. La quantité tapée part donc aussi aux sites à l'enregistrement, s'ils disent autre
     chose. Quand le chiffre change et que l'envoi automatique est allumé, c'est lui qui s'en
     charge (pas de double question). */
  const qteTapee=!!FICHE.qteTapee, qteChange=FICHE.brouillon.qte!==undefined;
  const prixChange=['pvr','pvw','pc'].some(k=>FICHE.brouillon[k]!==undefined), pxSites=!!FICHE.pxSites, pxExclu=FICHE.pxExclu||[];
  FICHE.pxSites=false; FICHE.pxExclu=null;
  FICHE.qteTapee=false;
  const base=cur[FICHE.pos];
  const nch=Object.keys(FICHE.brouillon).length;
  const frnAv=JSON.stringify((MOD[id]&&MOD[id].frn)||[]);
  const frnAp=JSON.stringify(FICHE.frn);
  if((nch||frnAv!==frnAp) && !demandeUser(false,"enregistrer la fiche",()=>enregistreFiche())) return;
  Object.keys(FICHE.brouillon).forEach(k=>{
    if(k==='pc'||k==='pcOff') return;
    const av=base[k], ap=FICHE.brouillon[k];
    if((av??'')===(ap??'')) return;
    log({act:CATCH[k]||'fiche',champ:k,lib:LIBCH[k]||k,bc:base.bc,
         ref:(base.marque||'')+' '+(base.nom||''),av:av??null,ap:ap??null});
  });
  if(FICHE.brouillon.pc){
    const pAv=Object.assign({},base), pAp=Object.assign({},base,FICHE.brouillon); pAp.pc=Object.assign({},base.pc||{},FICHE.brouillon.pc);
    canaux().forEach(c=>{ if(FICHE.brouillon.pc[c.id]===undefined) return;
      const av=prixCanal(pAv,c), ap=prixCanal(pAp,c);
      log({act:'prix',champ:'pc.'+c.id,lib:'prix '+c.nom+(ap.man?' (manuel)':' (retour à la règle)'),bc:base.bc,
           ref:(base.marque||'')+' '+(base.nom||''),av:av.v??null,ap:ap.v??null}); });
  }
  if(FICHE.brouillon.pcOff){
    const av=Array.isArray(base.pcOff)?base.pcOff:[], ap=FICHE.brouillon.pcOff;
    const nom=id=>{ const c=canaux().find(x=>x.id===id); return c?c.nom:id; };
    ap.filter(x=>!av.includes(x)).forEach(id=>log({act:'prix',champ:'canal.'+id,lib:'canal coupé pour ce parfum : '+nom(id),
      bc:base.bc,ref:(base.marque||'')+' '+(base.nom||''),av:'vendu',ap:'pas vendu'}));
    av.filter(x=>!ap.includes(x)).forEach(id=>log({act:'prix',champ:'canal.'+id,lib:'canal remis pour ce parfum : '+nom(id),
      bc:base.bc,ref:(base.marque||'')+' '+(base.nom||''),av:'pas vendu',ap:'vendu'}));
  }
  if(frnAv!==frnAp){
    log({act:'fournisseur',bc:base.bc,ref:(base.marque||'')+' '+(base.nom||''),
         av:JSON.parse(frnAv).filter(f=>f.n).map(f=>f.n+(f.p!=null?' @ '+f.p:'')).join(' | ')||null,
         ap:FICHE.frn.filter(f=>f.n).map(f=>f.n+(f.p!=null?' @ '+f.p:'')).join(' | ')||null,
         lib:'fournisseurs'});
  }
  const m=Object.assign({},MOD[id]||{},FICHE.brouillon);
  if(FICHE.brouillon.pc){ m.pc=Object.assign({},(MOD[id]&&MOD[id].pc)||{},FICHE.brouillon.pc);
    Object.keys(m.pc).forEach(k=>{ if(m.pc[k]==null) delete m.pc[k]; }); if(!Object.keys(m.pc).length) delete m.pc; }
  if(FICHE.brouillon.pcOff!==undefined){ if(FICHE.brouillon.pcOff.length) m.pcOff=FICHE.brouillon.pcOff; else delete m.pcOff; }
  if(FICHE.frn.length) m.frn=FICHE.frn; else delete m.frn;
  if(Object.keys(m).length) MOD[id]=m; else delete MOD[id];
  sauveMOD(); FICHE.brouillon={};
  render();
  const l=cur.findIndex(x=>x.id===id); if(l>=0) FICHE.pos=l;
  dessineFiche();
  $('dst').textContent='enregistré'; $('dst').className='st ok';
  setTimeout(()=>{ if(FICHE) $('dst').textContent=''; },2200);
  const auto=qteChange&&typeof _ssAllume==='function'&&_ssAllume();
  if(qteTapee&&!auto) setTimeout(()=>{ if(FICHE&&FICHE.id===id) envoieStockSites(null); },60);
  if(prixChange&&pxSites) setTimeout(()=>{ envoiePrixFiche(id,undefined,undefined,pxExclu); },qteTapee&&!auto?900:80);
  try{ remplitMarques(); }catch(e){}
}
/* ---- Le prix changé dans la fiche part aussi sur les sites (Sam, 3 oct. 2026) ----
   « J'ai voulu changer le prix d'Opium pour Homme, le mettre à 95 $, mais ça n'a pas changé
   sur WooCommerce. » Le prix retail et le prix de gros de la fiche sont ceux de l'ERP ; les
   sites ne bougeaient que par la case « sur le site » de Mes canaux de vente, que Sam n'avait
   pas vue. Désormais, quand il enregistre un nouveau prix, l'ERP lui propose de le mettre
   aussi sur les sites — une seule question, qui dit pour chaque site ce que le client paie
   aujourd'hui et ce qu'il paiera. Sur un site en promo, c'est la promo qui change (le prix
   barré reste) ; si le nouveau prix dépasse le prix barré, il devient le prix normal et la
   promo s'enlève. Jamais sous le prix d'achat. Seul le Patron peut le faire, comme avant. */
function planPrixSites(p){
  const plan=[], bas=[], garde=[];
  const e=siteDe(p); if(!e) return {plan,bas,garde};
  canaux().forEach(c=>{
    const cote=COTE_SITE[c.id]; if(!cote||horsCanal(p,c.id)) return;
    const f=e[cote]; if(!f||f.pr===undefined) return;
    const v=prixCanal(p,c).v; if(v==null||!(v>0)) return;
    const paye=f.ps!=null?f.ps:f.pr;
    if(paye!=null&&Math.abs(v-paye)<0.005) return;
    const nomSite=cote==='g'?'wholesale.perfumestrade.com':'perfumestrade.com';
    if(p.pa!=null&&v<p.pa&&!peutPrixSite()){ bas.push(nomSite); return; }   /* Patron/admin : jamais de refus, même à perte (9 oct. 2026) */
    /* 12 oct. 2026 (Sam : 58 $ dans l'outil a fait disparaître le prix barré sur perfumestrade.com : barré 35 / promo 29 → barré 58, plus de promo) :
       un prix d'outil au-dessus du prix barré ne remplace plus le barré en effaçant la promo. Le site n'est pas touché : les deux prix se règlent
       dans la case « sur le site » (prix barré + promo), que l'Enregistrer envoie. */
    if(cote!=='g'&&f.ps!=null&&f.pr!=null&&v>=f.pr){ garde.push(nomSite); return; }
    const promo=(cote!=='g'&&f.ps!=null&&f.pr!=null&&v<f.pr);   /* le gros n'a pas de prix barré : un seul prix */
    plan.push({cid:c.id,cote,f,v,paye,nomSite,nB:promo?f.pr:v,nP:promo?v:null});
  });
  return {plan,bas,garde};
}
const prixSitesOk=()=>peutPrixSite()&&typeof CK_URL!=='undefined'&&typeof ckTok==='function'&&!!ckTok();
/* Perfume City (Shopify) a son propre droit « prixPC » : on peut le donner à Kim, qui ne voit pas les marges, sans lui ouvrir
   les prix des autres sites. Le Patron et l'Admin l'ont d'office. */
const peutPrixPC=()=>{ try{ return peutPrixSite()||(typeof peut==='function'&&peut('prixPC')); }catch(e){ return false; } };
const prixPCOk=()=>peutPrixPC()&&typeof CK_URL!=='undefined'&&typeof ckTok==='function'&&!!ckTok();
/* la ligne d'un site, telle que Sam la lit avant de valider */
const lignePlanSite=x=>`<b>${x.nomSite}</b> : le client paie ${x.paye!=null?money2(x.paye):'sans prix'} → <b>${money2(x.v)}</b>`
  +(x.nP!=null?` <small>(prix promo ; le prix barré ${money2(x.nB)} ne bouge pas)</small>`:(x.f.ps!=null?' <small>(la promo est retirée)</small>':''));
async function envoiePrixFiche(id,seulCote,silencieux,exclus){
  if(!prixSitesOk()) return;
  const p=cur.find(x=>x.id===id)||tousLesArticles().find(x=>x.id===id); if(!p) return;
  let {plan}=planPrixSites(p);
  if(seulCote) plan=plan.filter(x=>x.cote===seulCote);
  if(exclus&&exclus.length) plan=plan.filter(x=>!exclus.includes(x.cid));
  if(!plan.length) return;
  const nom=((p.marque||'')+' '+(p.nom||'')).trim();
  const ok=[], ko=[];
  for(const x of plan){
    try{
      const r=await fetch(CK_URL+'/api/o/'+CK_ORG+'/site/prix',{method:'POST',
        headers:{'Content-Type':'application/json',Authorization:'Bearer '+ckTok()},
        body:JSON.stringify({quel:x.cote==='g'?'gros':'',bc:siteCle(p)||p.bc,barre:x.nB,promo:x.nP==null?'':x.nP,attendu:{barre:x.f.pr,promo:x.f.ps}})});
      const j=await r.json().catch(()=>({}));
      if(j&&j.avant&&typeof j.avant==='object'&&!j.ok){ x.f.pr=j.avant.barre; x.f.ps=j.avant.promo; }
      if(!r.ok) throw new Error(j.erreur||('erreur '+r.status));
      x.f.pr=j.apres.barre; x.f.ps=j.apres.promo; ok.push(x);
      const dit=o=>'barré '+(o&&o.barre!=null?money2(o.barre):'—')+' · promo '+(o&&o.promo!=null?money2(o.promo):'aucune');
      log({act:'prix',lib:'prix changés sur le site '+x.nomSite,bc:p.bc,ref:nom,av:dit(j.avant||{}),ap:dit(j.apres)});
    }catch(err){ ko.push(x.nomSite+' : '+((err&&err.message)||'échec')); }
  }
  ecrit(KSITE,SITE);
  if(silencieux) return {ok:ok.length,ko};
  if(FICHE&&FICHE.id===id){ dessineFiche();
    if(ok.length){ $('dst').textContent=ok.map(x=>vf(`${money2(x.v)} en ligne sur ${x.nomSite}`)).join(' · '); $('dst').className='st ok'; } }
  if(ko.length) alert(vf('Le prix n\'a pas été changé sur le site.\n\n')+ko.join('\n'));
}
$('dann').onclick=()=>{ FICHE.brouillon={}; FICHE.qteTapee=false;
  FICHE.frn=(MOD[FICHE.id]&&MOD[FICHE.id].frn)?JSON.parse(JSON.stringify(MOD[FICHE.id].frn)):[];
  dessineFiche(); };
$('ddx').onclick=fermeFiche; $('dov').onclick=fermeFiche;
$('dprev').onclick=()=>{ if(FICHE.pos>0){FICHE.pos--;FICHE.brouillon={}; FICHE.qteTapee=false;
  FICHE.frn=(MOD[cur[FICHE.pos].id]&&MOD[cur[FICHE.pos].id].frn)?JSON.parse(JSON.stringify(MOD[cur[FICHE.pos].id].frn)):[];
  dessineFiche();} };
$('dnext').onclick=()=>{ if(FICHE.pos<cur.length-1){FICHE.pos++;FICHE.brouillon={}; FICHE.qteTapee=false;
  FICHE.frn=(MOD[cur[FICHE.pos].id]&&MOD[cur[FICHE.pos].id].frn)?JSON.parse(JSON.stringify(MOD[cur[FICHE.pos].id].frn)):[];
  dessineFiche();} };
document.addEventListener('keydown',e=>{
  /* une fenêtre ouverte se ferme la première : Échap ne doit pas fermer la fiche
     dessous et laisser la fenêtre orpheline */
  if(e.key==='Escape'){
    if(document.getElementById('pw-ov')) return;      /* la recherche de photo se ferme la première */
    const f=['ajov','achov','marov','fcov'].find(i=>$(i)&&$(i).classList.contains('on'));
    if(f){ $(f).classList.remove('on'); return; }
  }
  if(!FICHE) return;
  if(e.key==='Escape') fermeFiche();
  if(/INPUT|SELECT|TEXTAREA/.test(e.target.tagName)) return;
  if(e.key==='ArrowLeft') $('dprev').click();
  if(e.key==='ArrowRight') $('dnext').click();
});
$('grid').addEventListener('click',e=>{
  const c=e.target.closest('.card'); if(c&&c.dataset.id) ouvreFiche(c.dataset.id);
});

/* ================= BARRE : SEGMENTÉ, TIROIR, PASTILLES ================= */
const SEG=$('seg');
SEG.addEventListener('click',e=>{
  const b=e.target.closest('button'); if(!b) return;
  SEG.querySelectorAll('button').forEach(x=>x.classList.toggle('on',x===b));
  $('fs').value=b.dataset.v; render();
});
$('qx').onclick=()=>{ $('q').value=''; render(); $('q').focus(); };
/* arrivée depuis le journal (ou un lien) avec ?q=code-barres : on montre la référence, en stock ou en historique */

$('advb').onclick=()=>{
  const o=$('adv').classList.toggle('on');
  $('advb').classList.toggle('on',o); $('advb').setAttribute('aria-expanded',o);
};

const LIB={fb:'Marque',fg:'Genre',ft:'Type',fan:'Prix',fp:'Photo',fx:'Fiches',fd:'Diffusion',fo:'Tri'};
const txtOpt=id=>{const e=$(id),o=e.options[e.selectedIndex];return o?o.textContent.trim():'';};

function majBarre(){
  const q=$('q').value.trim();
  $('srch').classList.toggle('has',!!q);

  // état visuel des listes
  ['fb','fg','ft','fan','fp','fx','fd'].forEach(id=>{
    const w=$(id).closest('.selw'); if(w) w.classList.toggle('act',$(id).value!=='');
  });
  const w=$('fo').closest('.selw'); if(w) w.classList.toggle('act',$('fo').value!=='b');

  // compteur du tiroir
  const nAdv=['ft','fan','fp','fx'].filter(id=>$(id).value!=='').length
            +($('fo').value!=='b'?1:0)+($('fa').checked?1:0)+($('fc').checked?1:0);
  const b=$('bdg'); b.textContent=nAdv; b.classList.toggle('vis',nAdv>0);

  // pastilles
  const ch=[];
  if(q) ch.push(['q','Recherche',q]);
  ['fb','fg','ft','fan','fp','fx','fd'].forEach(id=>{ if($(id).value!=='') ch.push([id,LIB[id],txtOpt(id)]); });
  if($('fo').value!=='b') ch.push(['fo',LIB.fo,txtOpt('fo').replace(/^Tri\s*:\s*/,'')]);
  if(TRI&&COLI[TRI.col]) ch.push(['tri','Tri',
    COLI[TRI.col].lib+(TRI.dir==='asc'?' ↑ croissant':' ↓ décroissant')]);
  if($('fa').checked) ch.push(['fa','','Prix repris du site']);
  if($('fc').checked) ch.push(['fc','','Mode client']);

  const box=$('chips');
  box.classList.toggle('on',ch.length>0);
  box.innerHTML=ch.map(([id,k,v])=>
    `<span class="chip">${k?`<span class="k">${k}</span>`:''}${esc(v)}
      <button data-r="${id}" aria-label="Retirer">&times;</button></span>`).join('')
    +(ch.length>1?'<button class="raz" id="raz">Tout effacer</button>':'');
}
$('chips').addEventListener('click',e=>{
  const b=e.target.closest('button[data-r]');
  if(b){ const id=b.dataset.r;
    if(id==='q') $('q').value='';
    else if(id==='tri'){ TRI=null; sauveTRI(); }
    else if(id==='fa'||id==='fc'){ $(id).checked=false; if(id==='fc') document.body.classList.remove('client'); }
    else $(id).value = id==='fo' ? 'b' : '';
    render(); return; }
  if(e.target.id==='raz'){
    $('q').value=''; ['fb','fg','ft','fan','fp','fx','fd'].forEach(i=>$(i).value='');
    $('fo').value='b'; $('fa').checked=false; $('fc').checked=false; TRI=null; sauveTRI();
    document.body.classList.remove('client'); render();
  }
});

/* ============ MODALE : OUVERTURE / ONGLETS ============ */
let PARSED=[];
const msg=(t,c='')=>{const m=$('msg');m.textContent=t;m.className='msg '+c;};
function ouvre(){
  $('ov').classList.add('on');
  const ms=[...new Set(tousLesArticles().map(p=>p.marque).filter(Boolean))].sort((a,b)=>a.localeCompare(b,'fr'));
  $('l-marques').innerHTML=ms.map(m=>`<option value="${m}">`).join('');
  $('l-types').innerHTML=[...new Set(P.map(p=>p.type).filter(Boolean))].sort()
    .map(t=>`<option value="${t}">`).join('');
  msg(''); setTimeout(()=>$('f-marque').focus(),60);
}
function ferme(){ $('ov').classList.remove('on'); }
$('add').onclick=ouvre; $('mx').onclick=ferme; $('mc').onclick=ferme;

/* ---- la fenêtre du relevé Amazon ---- */
function azFerme(){ $('azov').classList.remove('on'); }
$('azimp').onclick=()=>{
  AZ_LOT=null; $('azfi').value=''; $('azpv').style.display='none';
  $('azok').disabled=true; $('azmsg').textContent=''; $('azmsg').className='msg';
  $('azannul').textContent='Annuler';
  $('azov').classList.add('on');
};
$('azx').onclick=azFerme; $('azannul').onclick=azFerme;
$('azov').addEventListener('click',e=>{ if(e.target===$('azov')) azFerme(); });
document.addEventListener('keydown',e=>{ if(e.key==='Escape'&&$('azov').classList.contains('on')) azFerme(); });
$('azfi').onchange=e=>{
  const f=e.target.files[0]; if(!f) return;
  $('azpv').style.display=''; $('azpv').innerHTML='<div style="padding:14px">Lecture de '+esc(f.name)+'…</div>';
  lireFichier(f, m=>{ $('azpv').innerHTML='<div style="padding:14px">'+esc(m)+'</div>'; })
    .then(t=>azApercu(azAnalyse(String(t||''))))
    .catch(err=>azApercu({err:err.message||'Fichier illisible.'}));
};
$('azok').onclick=()=>{
  if(!demandeUser(false,"enregistrer les relevés Amazon",()=>$('azok').click())) return;
  azEnregistre();
};
$('ov').addEventListener('click',e=>{ if(e.target===$('ov')) ferme(); });
document.addEventListener('keydown',e=>{ if(e.key==='Escape'&&$('ov').classList.contains('on')) ferme(); });
document.querySelectorAll('.tab').forEach(t=>t.onclick=()=>{
  document.querySelectorAll('.tab').forEach(x=>x.classList.remove('on'));
  document.querySelectorAll('.pane').forEach(x=>x.classList.remove('on'));
  t.classList.add('on'); $('p-'+t.dataset.p).classList.add('on'); msg('');
  $('mo').textContent = t.dataset.p==='man' ? 'Ajouter' : `Ajouter ${PARSED.length||''} article${PARSED.length>1?'s':''}`.trim();
});




/* ================= FACTURE / FEUILLE DE TARIFS =================
   Une ligne connue n'a jamais le droit de creer un doublon : elle depose
   un point de plus dans l'historique du produit. */
const KFRN='fournisseurs-v1';
let FRN=lit(KFRN,{}); if(!FRN||typeof FRN!=='object') FRN=base(KFRN,{});
const sauveFRN=()=>ecrit(KFRN,FRN);

/* ================= AJUSTER LE STOCK (fenetre) =================
   Tout ce qui fait bouger une quantité sans être un achat ni une vente : casse, vol,
   retour au fournisseur, testeur ouvert, cadeau, erreur d'inventaire. Le motif est
   obligatoire — c'est lui qui donne son sens au mouvement, et il part au journal. */
const KAJ='ajustements-v1';
let AJU=lit(KAJ,[]); if(!Array.isArray(AJU)) AJU=base(KAJ,[]);
/* LE FIL EN DIRECT (1er oct. 2026) : une modification faite sur un autre poste (stock, prix,
   fiche, achat, vente) arrive dans la seconde ; la page relit ses données et se redessine sur
   place, à la même hauteur — sans recharger, et jamais pendant une saisie ou une fiche ouverte
   (dans ce cas, un bandeau propose de recharger). */
window.__rafraichir=()=>{ const y=window.scrollY;
  { const m=lit(KMOD,{}); if(m&&typeof m==='object'&&!Array.isArray(m)) MOD=m; }
  { const a=lit(KADD,[]); if(Array.isArray(a)) AJ=a; }
  { const h=lit(KPHO,{}); if(h&&typeof h==='object'&&!Array.isArray(h)) PHO=h; }
  { const a=lit(KAJ,[]); if(Array.isArray(a)) AJU=a; }
  { const j=lit(KJOU,[]); if(Array.isArray(j)) JOU=j; }
  { const s=lit(KSITE,{}); if(s&&typeof s==='object'&&!Array.isArray(s)) SITE=s; }
  try{ const r=JSON.parse(localStorage.getItem(KEXT)||'null'); if(r&&r.q) EXT=r; }catch(e){}
  paint(); window.scrollTo(0,y); };
const sauveAJU=()=>ecrit(KAJ,AJU);
const MOTIFS=[
 {id:'casse',   lib:'Casse',              sens:-1, aide:'flacon cassé ou abîmé'},
 {id:'vol',     lib:'Vol ou perte',       sens:-1, aide:'disparu, non retrouvé'},
 {id:'testeur', lib:'Testeur ouvert',     sens:-1, aide:'mis en test en boutique'},
 {id:'offert',  lib:'Offert',             sens:-1, aide:'cadeau, échantillon client'},
 {id:'retourf', lib:'Retour fournisseur', sens:-1, aide:'renvoyé au fournisseur'},
 /* Perfume City est la boutique de la femme de Sam : Perfumes Trade lui sort
    de la marchandise. Le motif est nommé pour qu'on sache, au journal, où sont
    partis les flacons — et combien, sur une période. */
 {id:'pcity',   lib:'Transfert vers Perfume City', sens:-1, aide:'marchandise sortie pour la boutique'},
 {id:'trouve',  lib:'Retrouvé',           sens:+1, aide:'réapparu en réserve'},
 {id:'autre',   lib:'Autre sortie',       sens:-1, aide:'à préciser dans la note'},
 {id:'erreur',  lib:'Erreur d\'inventaire', sens:0, aide:'la quantité comptée était fausse'}];
/* « perdue » est faux pour une marchandise qui part ailleurs : elle change de
   place, elle ne disparaît pas. Le mot suit le motif. */
function motMot(m,d){
  if(m.sens===0) return d<0?'en moins que prévu':'en plus que prévu';
  if(d>0) return 'retrouvée';
  if(m.id==='pcity')   return 'transférée à Perfume City';
  if(m.id==='retourf') return 'renvoyée au fournisseur';
  if(m.id==='offert')  return 'offerte';
  if(m.id==='testeur') return 'passée en testeur';
  return 'perdue';
}
/* ---------- Perfume City : le flacon de vitrine ----------
   Quand Perfumes Trade sort des flacons pour la boutique, la boutique n'en met
   pas autant en vente : le premier flacon d'une référence part en vitrine comme
   testeur. Livrer 5 flacons donne 4 vendables et 1 testeur. Le testeur ne se
   pose qu'une fois : la deuxième livraison de la même référence entre en entier.
   Les deux chiffres sont écrits séparément — le vendable dans l'inventaire de la
   boutique, le testeur dans sa propre liste — pour que la feuille de comptage
   attende bien 5 flacons en rayon et n'invente pas un écart. */
const K_TEST='testeurs-pc-v1';
function pcClef(p){ return p.bc ? String(p.bc).replace(/^0+/,'') : 'n-'+((p.marque||'')+(p.nom||'')+(p.ml||'')).toLowerCase().replace(/[^a-z0-9]/g,''); }
function pcTesteurs(){ const t=lit(K_TEST,{}); return (t&&typeof t==='object'&&!Array.isArray(t))?t:{}; }
function pcLignes(){ return pcsRows(); }
/* le stock de Perfume City d'une fiche : son code-barres, ou un de ses autres codes (fiches-modifiees-v1 › bcs) ; null si absent */
/* la quantité de ce parfum dans l'inventaire Perfume City (0 s'il n'y est pas) */
function qtePCde(p){ const r=pcStockFiche(p); return r?r.q:0; }
function pcStockFiche(p){
  try{ const m=pcsCarte(); const s0=x=>String(x||'').replace(/[^0-9A-Za-z]/g,'').replace(/^0+/,'');
    const ks=[p.bc].concat(String((MOD[p.id]||{}).bcs||p.bcs||'').split(/[\s,;]+/)).map(s0).filter(Boolean);
    for(const k of ks){ const o=m[k]; if(o) return {q:Math.max(0,Math.round(+o.q||0))}; }
    const o=m[String(p.id||'')]; if(o) return {q:Math.max(0,Math.round(+o.q||0))};
  }catch(e){}
  return null;
}   /* le stock de Perfume City est un magasin partagé (voir _fusion.py) */
/* n flacons partent : combien deviennent vendables chez Perfume City, combien en vitrine */
function pcRepartit(p,n,forceT){
  const k=pcClef(p), T=pcTesteurs();
  const deja=+(T[k]&&T[k].n||0);
  const t = forceT==null ? (deja>0?0:(n>0?1:0)) : (forceT?1:0);
  return {k, deja, t:Math.min(t,n), vend:Math.max(0,n-Math.min(t,n))};
}
function pcPeint(){
  const el=$('ajpc'); if(!el) return;
  const p=AJC.p;
  if(!p||AJC.motif!=='pcity'){ el.hidden=true; return; }
  const n=Math.max(0,Math.round(+$('aj-n').value||0));
  const r=pcRepartit(p,n,AJC.pcT);
  AJC.pc=r;
  const inv=pcLignes();
  el.hidden=false;
  el.innerHTML=`<h4>Ce que Perfume City reçoit</h4>
    <div class="rep">
      <div><b>${nf(r.vend)}</b><span class="k">en vente</span></div>
      <div><b>${nf(r.t)}</b><span class="k">tester</span></div>
      <div><b>${nf(n)}</b><span class="k">flacons livrés</span></div>
    </div>
    <label class="sw"><input type="checkbox" id="ajpct" ${r.t?'checked':''}>
      <span>Un flacon part comme tester${r.deja?' — <b>attention : la boutique en a déjà un</b> pour cette référence'
        :''}. Décoche si les ${nf(n)} flacons partent tous en vente.</span></label>
    ${inv===null?`<p class="dj">L'inventaire de Perfume City est encore vide : cette sortie va le créer.</p>`:''}`;
  const c=$('ajpct'); if(c) c.onchange=()=>{ AJC.pcT=c.checked; pcPeint(); recapAjust(); };
}
/* écrit dans l'inventaire de la boutique : la ligne existe, on ajoute ; sinon on la crée */
function pcDepose(p,r){
  let rows=pcLignes();
  if(rows===null) rows=[];
  const idx=rows.findIndex(x=>{
    const bc=x&&x[0]?String(x[0]).replace(/^0+/,''):'';
    return bc ? bc===r.k : (x&&x[9]===r.k);
  });
  const pa = paEff2(p);
  if(idx>=0){ rows[idx][5]=(+rows[idx][5]||0)+r.vend;
    if(rows[idx][6]==null&&pa!=null) rows[idx][6]=pa;
    rows[idx][7]= rows[idx][6]!=null ? rows[idx][5]*rows[idx][6] : null; }
  else rows.push([p.bc||'',p.nom||'',p.marque||'',p.ml||'',p.type||'',r.vend,pa,
                  pa!=null?r.vend*pa:null,'non',(p.bc?'b'+p.bc:r.k),null,null]);
  if(!pcsSauve(rows)) return false;
  if(r.t){ const T=pcTesteurs();
    T[r.k]=Object.assign({},T[r.k]||{},{n:1,   /* 10 nov. 2026 (Igal) : un tester par parfum chez Perfume City, jamais plus */
      bc:p.bc||'', ref:((p.marque||'')+' '+(p.nom||'')).trim(),
      t:new Date().toISOString(), u:USR||'(non renseigné)'});
    ecrit(K_TEST,T); }
  return true;
}
function paEff2(p){ const m=MOD[p.id]||{}; return m.pa!=null?+m.pa:(p.pa!=null?+p.pa:null); }
/* ---------- 3 nov. 2026 (Igal) : un transfert depuis la fiche va AUSSI sur Shopify ----------
   La réception d'une facture envoyait déjà la part de Perfume City à Shopify ; le transfert fait depuis « Ajuster le stock »
   ne mettait à jour que l'ERP, et la boutique en ligne gardait l'ancienne quantité. Même envoi que les factures (route
   stock-ajoute du cockpit, un identifiant par transfert : rien n'est compté deux fois). Ce qui n'a pas pu partir attend
   dans une file et repart tout seul à l'ouverture suivante du Catalogue ou au transfert suivant. Seuls les flacons EN VENTE
   partent : le tester de vitrine n'est pas à vendre. */
const K_PC_FILE='pc-shopify-attente-v1';
function pcFile(){ const f=lit(K_PC_FILE,[]); return Array.isArray(f)?f:[]; }
function pcShopifyAjoute(p,r){
  if(!(r.vend>0)||!p.bc) return;
  const f=pcFile(); f.push({cle:'aj|'+p.bc+'|'+Date.now(),items:[{bc:String(p.bc),ajout:r.vend,nom:((p.marque||'')+' '+(p.nom||'')).trim()}],t:new Date().toISOString()});
  ecrit(K_PC_FILE,f);
  return pcShopifyVide();
}
let _pcVideEnCours=false;
async function pcShopifyVide(){
  if(_pcVideEnCours) return {attente:true}; _pcVideEnCours=true;
  try{
    if(typeof CK_URL==='undefined'||typeof ckTok!=='function'||!ckTok()) return {hors:true};
    let f=pcFile(), res=null;
    while(f.length){
      const e=f[0];
      try{
        const r=await fetch(CK_URL+'/api/o/'+CK_ORG+'/shopify/stock-ajoute',{method:'POST',headers:{'Content-Type':'application/json',Authorization:'Bearer '+ckTok()},
          body:JSON.stringify({cle:e.cle,items:e.items})});
        const j=await r.json().catch(()=>({}));
        if(!r.ok){ res={erreur:j.erreur||('erreur '+r.status)}; break; }
        res=j;
      }catch(err){ res={erreur:'le cockpit ne répond pas'}; break; }
      f=f.slice(1); ecrit(K_PC_FILE,f);
      const ko=(res.lignes||[]).filter(l=>l.etat&&l.etat!=='ok');
      log({act:'site',lib:'transfert à Perfume City : stock envoyé à Shopify'+(ko.length?' — '+ko.map(l=>(l.nom||l.bc)+' : '+(l.raison||l.etat)).join(' ; '):''),
           n:e.items.length,impact:0,det:e.items.map(i=>({bc:i.bc,ref:i.nom,q:i.ajout}))});
    }
    return res||{ok:true};
  } finally { _pcVideEnCours=false; }
}
setTimeout(()=>{ try{ if(pcFile().length) pcShopifyVide(); }catch(e){} },12000);

let AJC={p:null,motif:null};
function ouvreAjust(p){
  AJC={p,motif:null,pcT:null};
  const bpc=$('ajpc'); if(bpc){ bpc.hidden=true; bpc.innerHTML=''; }
  $('ajp').innerHTML=`<div><b>${esc(p.marque||'')} ${esc(p.nom||'')}${tyBadge(p)}</b>
    <span style="display:block;font-size:12px;color:var(--ink-3)">${esc(p.bc||'sans code-barres')} · stock actuel <b>${nf(p.qte)}</b></span></div>`;
  const carte=m=>`<label data-m="${m.id}"><input type="radio" name="ajm" value="${m.id}">
    <span class="t">${esc(m.lib)}</span><span class="a">${esc(m.aide)}</span></label>`;
  const grp=(sg,cls,titre,list)=>list.length?`<div class="ajgrp">
      <div class="ajgt"><span class="sg ${cls}">${sg}</span><b>${titre}</b><i></i></div>
      <div class="ajmot">${list.map(carte).join('')}</div></div>`:'';
  $('ajmot').innerHTML=
      grp('−','m','Des flacons sortent du stock', MOTIFS.filter(m=>m.sens===-1))
    + grp('+','p','Des flacons reviennent',       MOTIFS.filter(m=>m.sens===+1))
    + grp('=','e','Ce n\'est pas un mouvement : la quantité était fausse', MOTIFS.filter(m=>m.sens===0));
  $('ajmot').querySelectorAll('input').forEach(r=>r.onchange=()=>{
    AJC.motif=r.value;
    $('ajmot').querySelectorAll('label').forEach(l=>l.classList.toggle('on',l.dataset.m===r.value));
    const m=MOTIFS.find(x=>x.id===r.value);
    $('ajnlab').textContent = m && m.sens===0 ? 'Quantité réelle en rayon'
                            : m && m.sens===+1 ? 'Combien de flacons reviennent'
                            : 'Combien de flacons sortent';
    $('aj-n').focus(); $('aj-n').select();
    AJC.pcT=null; pcPeint(); recapAjust(); });
  $('aj-n').value=''; $('aj-d').value=ajd();
  $('ajnlab').textContent='Combien de flacons';
  $('aj-note').value=''; $('ajmsg').textContent=''; recapAjust();
  $('ajov').classList.add('on');
}
function sensAjust(){ const m=MOTIFS.find(x=>x.id===AJC.motif); return m?m.sens:0; }
function recapAjust(){
  const p=AJC.p; if(!p) return;
  const brut=$('aj-n').value.trim();
  const n=Math.max(0,Math.round(+brut||0));
  const m=MOTIFS.find(x=>x.id===AJC.motif);
  /* une correction d'inventaire peut valoir zéro (« il n'en reste aucun ») ; une sortie, non */
  if(!m||brut===''||(!n&&m.sens!==0)){
    $('ajrecap').className='ajres vide';
    $('ajrecap').innerHTML = !m
      ? '<b>1.</b> Choisis ce qui est arrivé aux flacons, ci-dessus.'
      : (m.sens===0
          ? '<b>2.</b> Indique la quantité <b>réellement</b> en rayon. Elle remplacera celle de SAM.'
          : `<b>2.</b> Indique combien de flacons ${m.sens===-1?'sortent':'reviennent'}.`);
    $('ajok').disabled=true; return; }
  let ap;
  if(m.sens===-1) ap=Math.max(0,p.qte-n);
  else if(m.sens===+1) ap=p.qte+n;
  else ap=n;                                  /* erreur d'inventaire / autre : la quantité devient n */
  const d=ap-p.qte;
  const val=p.pa!=null?Math.abs(d)*p.pa:null;
  /* on a demandé plus que ce qu'il y a : on le dit, au lieu de l'écrêter en silence */
  const trop = m.sens===-1 && n>p.qte ? n-p.qte : 0;
  const cls = d<0?'m':d>0?'p':'n';
  $('ajrecap').className='ajres';
  $('ajrecap').innerHTML=`
    <div class="ajch"><span class="av">${nf(p.qte)}</span><span class="vers">→</span>
      <span class="ap ${cls}">${nf(ap)}</span></div>
    <div class="dt">
      <b>${esc(m.lib)}</b> · ${m.sens===0?`écart de ${d>0?'+':''}${nf(d)} avec ce que SAM affichait`
                                        :`${d>0?'+':''}${nf(d)} flacon${Math.abs(d)>1?'s':''}`}
      ${val!=null&&d!==0?`<br>${money(val)} de marchandise ${motMot(m,d)}`:''}
      ${m.sens===0?'<br>Correction d\'écriture : aucun flacon n\'a bougé, c\'est le chiffre de SAM qui était faux.':''}
      ${d===0?'<br>Le stock est déjà à cette valeur — rien à enregistrer.':''}
      ${trop?`<br><span class="w">Tu déclares ${nf(n)} flacons, il n'y en avait que ${nf(p.qte)}.</span> Seuls ${nf(p.qte)} sortent — vérifie le chiffre, ou passe par « Erreur d'inventaire ».`:''}
      ${m.id==='pcity'&&AJC.pc?`<br>Chez Perfume City : <b>${nf(AJC.pc.vend)}</b> en vente${AJC.pc.t?` et <b>${nf(AJC.pc.t)}</b> en tester`:''}.`:''}
    </div>`;
  $('ajok').disabled = d===0;
  AJC.ap=ap; AJC.n = m.sens===-1 ? Math.min(n,p.qte) : n; AJC.d=d;
}
['aj-n','aj-note'].forEach(id=>$(id).addEventListener('input',recapAjust));
$('aj-n').addEventListener('input',pcPeint);
$('aj-n').addEventListener('focus',()=>$('aj-n').select());
$('ajm').onclick=()=>{ $('aj-n').value=Math.max(0,(+$('aj-n').value||0)-1); pcPeint(); recapAjust(); };
$('ajp2').onclick=()=>{ $('aj-n').value=(+$('aj-n').value||0)+1; pcPeint(); recapAjust(); };
$('ajx').onclick=$('ajc').onclick=()=>$('ajov').classList.remove('on');
$('ajov').addEventListener('click',e=>{ if(e.target.id==='ajov') $('ajov').classList.remove('on'); });
$('ajok').onclick=()=>{
  const p=AJC.p, m=MOTIFS.find(x=>x.id===AJC.motif); if(!p||!m) return;
  if(!demandeUser(false,"ajuster le stock",()=>$('ajok').click())) return;
  const av=p.qte, ap=AJC.ap;
  const mm=Object.assign({},MOD[p.id]||{},{qte:ap});
  /* le comptage physique ne décrit plus la réalité une fois le stock ajusté :
     on retire sa trace, sinon la page Stock affichait un écart fantôme et
     « annuler le comptage » rendait une quantité d'avant l'ajustement. */
  const avaitCompte = mm.qteC!=null;
  delete mm.qteC; delete mm.qteAv;
  MOD[p.id]=mm;
  sauveMOD();
  AJU.push({t:new Date().toISOString(),d:$('aj-d').value||ajd(),
    cle:p.id,bc:p.bc,ref:(p.marque||'')+' '+(p.nom||''),motif:m.id,lib:m.lib,
    n:AJC.n,av,ap,delta:ap-av,pa:p.pa??null,val:p.pa!=null?(ap-av)*p.pa:null,
    note:$('aj-note').value.trim()||undefined,u:USR||'(non renseigné)'});
  sauveAJU();
  /* le transfert ne fait pas que sortir du stock d'ici : il entre chez Perfume City */
  let suitePC='';
  let envoiPC=null;
  if(m.id==='pcity'){
    const r=pcRepartit(p,AJC.n,AJC.pcT);
    if(pcDepose(p,r)){ suitePC=' — Perfume City : '+r.vend+' en vente'+(r.t?', '+r.t+' en tester':''); envoiPC=pcShopifyAjoute(p,r); }
    else $('ajmsg').textContent='inventaire Perfume City non mis à jour (mémoire du navigateur pleine)';
  }
  if(envoiPC&&envoiPC.then) envoiPC.then(res=>{
    if(!res||res.attente) return;
    const txt=res.hors||res.erreur
      ? L3(`Stock de Perfume City à jour dans l'ERP, mais PAS encore sur Shopify (${res.hors?"l'ERP n'est pas relié au cockpit":res.erreur}). L'envoi repartira tout seul à la prochaine ouverture du Catalogue.`,
           `Perfume City's stock is up to date in the ERP, but NOT yet on Shopify (${res.hors?'the ERP is not connected to the cockpit':res.erreur}). It will be sent again by itself the next time the Catalog opens.`,
           `Stock de Perfume City al día en el ERP, pero AÚN NO en Shopify (${res.hors?'el ERP no está conectado al cockpit':res.erreur}). Se reenviará solo la próxima vez que se abra el Catálogo.`)
      : L3('Perfume City : stock envoyé à Shopify','Perfume City: stock sent to Shopify','Perfume City: stock enviado a Shopify');
    if(res.hors||res.erreur) log({act:'site',lib:'transfert à Perfume City : stock NON envoyé à Shopify ('+(res.hors?'hors ligne':res.erreur)+'), en attente',n:1,impact:0,det:[]});
    const d=$('dst'); if(d){ d.textContent=txt; d.className='st '+((res.hors||res.erreur)?'ko':'ok'); }
  });
  log({act:'stock',lib:'ajustement — '+m.lib.toLowerCase()+suitePC+($('aj-note').value.trim()?' ('+$('aj-note').value.trim()+')':''),
       bc:p.bc,ref:(p.marque||'')+' '+(p.nom||''),av,ap});
  $('ajov').classList.remove('on');
  render();
  if(FICHE){
    const l=cur.findIndex(x=>x.id===p.id);
    if(l>=0){ FICHE.pos=l; dessineFiche(); }
    else {   /* le produit est sorti du filtre (stock à zéro) : on ferme plutôt que
                d'afficher la fiche du voisin sous le nom du produit ajusté */
      fermeFiche();
      const b=document.createElement('div'); b.className='info';
      b.innerHTML=`<b>Stock ajusté</b> — ${esc((p.marque||'')+' '+(p.nom||''))} : ${nf(av)} → ${nf(ap)}.
        ${ap===0?'La fiche a quitté la liste « en stock ». Passe le filtre sur « Tout » pour la retrouver.':''}`;
      const w=document.querySelector('.wrap')||document.body; w.insertBefore(b,w.firstChild);
      setTimeout(()=>b.remove(),9000);
      return;
    }
  }
  $('dst').textContent='stock ajusté'+(avaitCompte?' — le comptage précédent est effacé':'');
  $('dst').className='st ok';
  setTimeout(()=>{ if(FICHE) $('dst').textContent=''; },3600);
};

/* ================= RELEVÉ AMAZON (fenetre) =================
   On colle ce qu'affiche la fiche Amazon (prix, « Best Sellers Rank », avis, adresse) et
   l'outil en tire les chiffres. Tant qu'il n'y a pas de serveur, c'est la seule façon
   d'avoir le rang : Amazon ne le publie que sur la page du produit. */
const MCH=['mar-amz','mar-rang','mar-cat','mar-rangG','mar-catG','mar-note','mar-avis','mar-dem','mar-vend','mar-n','mar-url','mar-obs'];
function ouvreMarche(){
  const p=cur[FICHE.pos], m=MAR[p.id]||{};
  const v=(id,val)=>{ $(id).value = (val==null?'':String(val)); };
  v('mar-amz',m.amz); v('mar-rang',m.rang); v('mar-cat',m.cat); v('mar-rangG',m.rangG); v('mar-catG',m.catG);
  v('mar-note',m.note5); v('mar-avis',m.avis); v('mar-dem',m.dem); v('mar-vend',m.vend); v('mar-n',m.n);
  v('mar-url',m.url); v('mar-obs',m.note);
  $('mar-colle').value=''; $('mar-lu').innerHTML=''; $('marmsg').textContent='';
  recapMarche();
  $('marov').classList.add('on'); setTimeout(()=>$('mar-colle').focus(),60);
}
function litAmazon(t){
  const r={}, T=t.replace(/ /g,' ');
  let mm=T.match(/\$\s*([\d.,]+)/); if(mm) r.amz=nombre(mm[1]);
  const tous=[...T.matchAll(/#\s*([\d.,\s]+?)\s+in\s+\[?([^\n\]\(]+)/gi)];
  if(tous.length){
    r.rangG=nombre(tous[0][1]); r.catG=tous[0][2].trim();
    if(tous.length>1){ r.rang=nombre(tous[1][1]); r.cat=tous[1][2].trim(); }
    else { r.rang=r.rangG; r.cat=r.catG; delete r.rangG; delete r.catG; }
  }
  mm=T.match(/([\d.,]+)\s*(?:out of|sur)\s*5/i); if(mm) r.note5=nombre(mm[1]);
  mm=T.match(/\(\s*([\d.,]+)\s*\)/); if(mm) r.avis=nombre(mm[1]);
  mm=T.match(/([\d.,]+K?\+?)\s*(?:bought in past month|achet[ée]s le mois dernier)/i); if(mm) r.dem=mm[1];
  mm=T.match(/(?:Ships from and sold by|Sold by|Vendu par)\s*:?\s*([^\n,]{2,45})/i);
  if(mm) r.vend=mm[1].trim().replace(/\.$/,'');
  mm=T.match(/https?:\/\/[^\s)\]]*amazon\.[^\s)\]]*/i); if(mm) r.url=mm[0];
  else { mm=T.match(/\b(B0[A-Z0-9]{8})\b/); if(mm) r.url='https://www.amazon.com/dp/'+mm[1]; }
  if(/currently unavailable|indisponible|non disponible/i.test(T)){ r.obs='indisponible sur Amazon'; delete r.amz; }
  mm=T.match(/Only\s+(\d+)\s+left in stock|Plus que\s+(\d+)/i);
  if(mm) r.obs=(r.obs?r.obs+' · ':'')+'plus que '+(mm[1]||mm[2])+' en stock chez Amazon';
  return r;
}
function recapMarche(){
  const p=cur[FICHE.pos]; if(!p) return;
  const amz=$('mar-amz').value===''?null:+$('mar-amz').value;
  const rang=$('mar-rang').value===''?null:+$('mar-rang').value;
  const t=[];
  if(amz!=null){
    t.push(`Amazon le vend <b>${money(amz)}</b>`);
    if(p.pa!=null) t.push(`marge à ce prix-là <b class="${pcCls((amz-p.pa)/amz*100)}">${pct1((amz-p.pa)/amz*100)}</b>`);
    if(p.pvr!=null) t.push(p.pvr>amz?`ton retail est <b class="c">${money(p.pvr-amz)} au-dessus</b>`
      :p.pvr<amz?`ton retail est <b class="g">${money(amz-p.pvr)} en dessous</b>`:'même prix que ton retail');
  } else t.push("Pas de prix : le produit sera marqué <b>indisponible sur Amazon</b>");
  if(rang!=null) t.push(`rang <b>#${nf(rang)}</b>${$('mar-cat').value?' en '+esc($('mar-cat').value):''}`);
  $('marrecap').innerHTML=t.join(' · ')+'.';
}
$('mar-colle').addEventListener('input',()=>{
  const t=$('mar-colle').value;
  if(!t.trim()){ $('mar-lu').innerHTML=''; return; }
  const r=litAmazon(t), pris=[];
  const pose=(id,val,lib)=>{ if(val==null||val==='') return; $(id).value=String(val); pris.push(lib); };
  pose('mar-amz',r.amz,'le prix'); pose('mar-rang',r.rang,'le rang'); pose('mar-cat',r.cat,'la catégorie');
  pose('mar-rangG',r.rangG,'le rang général'); pose('mar-catG',r.catG,'la catégorie générale');
  pose('mar-note',r.note5,'la note'); pose('mar-avis',r.avis,"le nombre d'avis");
  pose('mar-dem',r.dem,'les achats du mois'); pose('mar-vend',r.vend,'le vendeur');
  pose('mar-url',r.url,'le lien'); pose('mar-obs',r.obs,'la disponibilité');
  $('mar-lu').innerHTML = pris.length
    ? `<div class="mlu"><b>Lu dans ce que tu as collé :</b> ${pris.join(', ')}. Vérifie les cases ci-dessous et corrige au besoin.</div>`
    : `<div class="mlu rien"><b>Rien reconnu.</b> Copie le bloc « Best Sellers Rank » de la fiche Amazon, le prix et l'adresse de la page — ou remplis les cases à la main.</div>`;
  recapMarche();
});
MCH.forEach(id=>$(id).addEventListener('input',recapMarche));
$('marx').onclick=$('marc').onclick=()=>$('marov').classList.remove('on');
$('marov').addEventListener('click',e=>{ if(e.target.id==='marov') $('marov').classList.remove('on'); });
$('marok').onclick=()=>{
  const base=cur[FICHE.pos], av=MAR[base.id], m={};
  const n=id=>{ const v=$(id).value.trim(); return v===''?null:nombre(v); };
  const st=id=>{ const v=$(id).value.trim(); return v===''?null:v; };
  const met=(k,v)=>{ if(v!=null) m[k]=v; };
  met('amz',n('mar-amz')); met('rang',n('mar-rang')); met('cat',st('mar-cat'));
  met('rangG',n('mar-rangG')); met('catG',st('mar-catG')); met('note5',n('mar-note'));
  met('avis',n('mar-avis')); met('dem',st('mar-dem')); met('vend',st('mar-vend'));
  met('n',n('mar-n')); met('url',st('mar-url')); met('note',st('mar-obs'));
  if(!demandeUser(false,"enregistrer le relevé Amazon",()=>$('marok').click())) return;
  m.le=new Date().toISOString(); m.par=USR||'(non renseigné)'; m.bc=base.bc;
  m.hist=(av&&av.hist&&av.hist.length)?av.hist.slice():(av&&av.le?[{le:av.le,amz:av.amz??null,rang:av.rang??null}]:[]);
  m.hist.push({le:m.le,amz:m.amz??null,rang:m.rang??null});
  MAR[base.id]=m; sauveMAR();
  log({act:'prix',lib:'relevé Amazon',bc:base.bc,ref:(base.marque||'')+' '+(base.nom||''),
       av:av?`${av.amz??'—'} $ · rang ${av.rang??'—'}`:null,
       ap:`${m.amz??'—'} $ · rang ${m.rang??'—'}${m.note5?' · '+m.note5+'/5':''}`});
  $('marov').classList.remove('on');
  dessineFiche();
};

/* ================= ENREGISTRER UN ACHAT (fenetre) =================
   Produit trouve par code-barres (douchette) ou par nom, fournisseur existant ou nouveau,
   date, quantite, prix. L'achat rejoint l'historique du prix d'achat ; au choix il devient
   le prix d'achat courant et/ou entre dans le stock. Tout part au journal. */
let ACH={p:null};
const NEUF='__nouveau__';
function fournisseursConnus(){
  const n=new Set(Object.keys(FRN));
  Object.values(HIST).forEach(l=>l.forEach(x=>{ if(x.f) n.add(x.f); }));
  return [...n].filter(Boolean).sort((a,b)=>a.localeCompare(b,'fr'));
}
function ouvreAchat(p){
  ACH={p:p||null};
  const sel=$('ach-f');
  sel.innerHTML='<option value="">— choisir —</option>'+fournisseursConnus().map(f=>`<option value="${esc(f)}">${esc(f)}</option>`).join('')+`<option value="${NEUF}">+ Nouveau fournisseur…</option>`;
  $('ach-fn').hidden=true; $('ach-nouveau').hidden=true; $('ach-fn').value=''; $('ach-ft').value=''; $('ach-fe').value='';
  $('ach-fsrc').innerHTML='';
  $('ach-d').value=ajd();
  $('ach-n').value=''; $('ach-p').value=''; $('ach-num').value=''; $('ach-q').value='';
  $('ach-prix').checked=true; $('ach-stock').checked=false; $('achmsg').textContent='';
  $('achres').hidden=true;
  peintAchP(); recapAchat();
  $('achov').classList.add('on');
  setTimeout(()=>{ (ACH.p?$('ach-f'):$('ach-q')).focus(); },50);
}
function peintAchP(){
  const el=$('achp'), p=ACH.p;
  if(!p){ el.className='achp'; el.innerHTML=''; $('ach-q').hidden=false; return; }
  el.className='achp on';
  el.innerHTML=`${p.img?`<img src="photos/${p.bc}.webp" alt="" onerror="this.style.visibility='hidden'">`:'<div class="miss"></div>'}
    <div class="t"><b>${esc(p.marque||'')} ${esc(p.nom||'')}${tyBadge(p)}</b><span>${esc(p.ml||'')} ${p.ml?'oz · ':''}${esc(p.bc||'sans code-barres')} · stock ${nf(p.qte)} · achat actuel ${p.pa!=null?money(p.pa):'—'}</span></div>
    <button type="button" id="achchg">changer</button>`;
  $('ach-q').hidden=true;
  $('achchg').onclick=()=>{ ACH.p=null; peintAchP(); recapAchat(); $('ach-q').focus(); };
}
function chercheAchat(q){
  const t=q.trim().toLowerCase(); const res=$('achres');
  if(!t){ res.hidden=true; return; }
  const num=t.replace(/\D/g,'');
  const L=tousLesArticles().filter(p=>{
    if(num.length>=6 && String(p.bc||'').replace(/^0+/,'').includes(num.replace(/^0+/,''))) return true;
    return (p.marque+' '+p.nom).toLowerCase().includes(t);
  }).slice(0,8);
  res.innerHTML=L.length?L.map(p=>`<div data-id="${p.id}"><b>${esc(p.marque||'')} ${esc(p.nom||'')}${tyBadge(p)}</b><span>${esc(p.ml||'')}${p.ml?' oz · ':''}${esc(p.bc||'')} · stock ${nf(p.qte)}</span></div>`).join('')
    :`<div class="vide">Aucun produit ne correspond — crée-le d'abord avec « + Nouvel article ».</div>`;
  res.hidden=false;
  if(num.length>=8&&L.length===1&&String(L[0].bc||'').replace(/^0+/,'')===num.replace(/^0+/,'')){ ACH.p=L[0]; peintAchP(); recapAchat(); res.hidden=true; $('ach-f').focus(); }
}
function recapAchat(){
  const p=ACH.p, px=nombre($('ach-p').value), n=parseInt($('ach-n').value,10);
  const f=$('ach-f').value===NEUF?$('ach-fn').value.trim():$('ach-f').value;
  const ok=!!p && px!=null && px>0 && !!f;
  $('achok').disabled=!ok;
  if(!p){ $('achrecap').innerHTML='<span class="manque">Choisis d\'abord le produit</span> : scanne-le, ou tape son code-barres ou son nom.'; return; }
  const parts=[];
  if(px!=null&&px>0){
    if(p.pa!=null){ const d=px-p.pa; parts.push(d===0?`Même prix qu'aujourd'hui (${money(p.pa)}).`:`<b class="${d<0?'g':'c'}">${d<0?'Baisse':'Hausse'} de ${money(Math.abs(d))}</b> par rapport au prix d'achat actuel (${money(p.pa)}).`); }
    if(p.pvw!=null) parts.push(`Marge de gros à ce prix : <b>${pct1((p.pvw-px)/p.pvw*100)}</b>.`);
    if(p.pvr!=null) parts.push(`Marge retail : <b>${pct1((p.pvr-px)/p.pvr*100)}</b>.`);
    if(n>0) parts.push(`Montant : <b>${money(px*n)}</b> pour ${nf(n)} flacon${n>1?'s':''}.`);
    if($('ach-stock').checked&&n>0) parts.push(`Stock : ${nf(p.qte)} → <b>${nf(p.qte+n)}</b>.`);
  } else parts.push('<span class="manque">Indique le prix d\'achat unitaire.</span>');
  if(!f) parts.push('<span class="manque">Choisis ou crée le fournisseur.</span>');
  $('achrecap').innerHTML=parts.join(' ');
}
$('ach-q').addEventListener('input',e=>chercheAchat(e.target.value));
$('ach-q').addEventListener('keydown',e=>{ if(e.key==='Enter'){ e.preventDefault(); chercheAchat(e.target.value); const first=$('achres').querySelector('[data-id]'); if(first) first.click(); } });
$('achres').addEventListener('click',e=>{ const d=e.target.closest('[data-id]'); if(!d) return;
  ACH.p=tousLesArticles().find(p=>p.id===d.dataset.id)||null; $('achres').hidden=true; peintAchP(); recapAchat(); $('ach-f').focus(); });
/* Les coordonnées ne se retapent pas : elles viennent de la fiche du fournisseur.
   On les affiche dès qu'un fournisseur est choisi, modifiables — une correction ici
   met la fiche à jour. Pour un nouveau fournisseur, les cases sont vides. */
function coordFrn(){
  const v=$('ach-f').value, neuf=v===NEUF;
  $('ach-fn').hidden=!neuf;
  $('ach-nouveau').hidden = !neuf && !v;
  if(neuf){ $('ach-fsrc').innerHTML='Ces coordonnées créeront sa fiche fournisseur.';
    $('ach-ft').value=''; $('ach-fe').value=''; return; }
  if(!v) return;
  const c=FRN[v]||{};
  $('ach-ft').value=c.tel||''; $('ach-fe').value=c.email||'';
  const a=[]; if(c.raison&&c.raison!==v) a.push(esc(c.raison)); if(c.contact) a.push(esc(c.contact));
  $('ach-fsrc').innerHTML = (c.tel||c.email)
    ? `Repris de la fiche de <b>${esc(v)}</b>${a.length?' — '+a.join(' · '):''}. Une correction ici met sa fiche à jour.`
    : `<b>${esc(v)}</b> n'a ni téléphone ni e-mail dans sa fiche. Ce que tu tapes ici l'y ajoutera.`;
}
$('ach-f').addEventListener('change',()=>{ coordFrn(); if($('ach-f').value===NEUF) $('ach-fn').focus(); recapAchat(); });
['ach-fn','ach-n','ach-p','ach-stock','ach-prix','ach-d'].forEach(i=>$(i).addEventListener('input',recapAchat));
$('achx').onclick=$('achc').onclick=()=>$('achov').classList.remove('on');
$('achok').onclick=()=>{
  const p=ACH.p; if(!p) return;
  const px=nombre($('ach-p').value), n=parseInt($('ach-n').value,10)||null, d=$('ach-d').value||ajd();
  const neuf=$('ach-f').value===NEUF, f=(neuf?$('ach-fn').value:$('ach-f').value).trim(), num=$('ach-num').value.trim();
  if(!f||px==null||px<=0) return;
  const ref=(p.marque||'')+' '+(p.nom||'');
  const tel=$('ach-ft').value.trim(), mail=$('ach-fe').value.trim();
  const av=FRN[f]||{};
  if(neuf||!FRN[f]||av.tel!==(tel||undefined)||av.email!==(mail||undefined))
    FRN[f]=Object.assign({nom:f},av,{tel:tel||undefined,email:mail||undefined,maj:new Date().toISOString()});
  else FRN[f].maj=new Date().toISOString();
  sauveFRN();
  (HIST[p.id]=HIST[p.id]||[]).push({d,p:px,f,q:n,src:'manuel',num:num||undefined});
  sauveHIST();
  log({act:'prix',lib:"achat enregistré"+(num?' — facture '+num:''),bc:p.bc,ref,av:null,ap:jourFr(d)+' · '+money(px)+' · '+f+(n?' · '+n+' u.':'')});
  const m=Object.assign({},MOD[p.id]||{}); let ch=false;
  if($('ach-prix').checked && (p.pa??null)!==px){ log({act:'prix',lib:"prix d'achat — achat "+f,champ:'pa',bc:p.bc,ref,av:p.pa??null,ap:px}); m.pa=px; ch=true; }
  if($('ach-stock').checked && n>0){ const av=p.qte, ap=av+n; log({act:'stock',lib:'réception — achat '+f,champ:'qte',bc:p.bc,ref,av,ap}); m.qte=ap; ch=true; }
  if(ch){ MOD[p.id]=m; sauveMOD(); }
  if(neuf) log({act:'fournisseur',lib:'fournisseur créé',ref:f,av:null,ap:f});
  $('achov').classList.remove('on');
  render(); if(FICHE){ const l=cur.findIndex(x=>x.id===p.id); if(l>=0) FICHE.pos=l; dessineFiche(); }
};
let FACT=null;

function normBC2(v){ const d=String(v==null?'':v).replace(/[^0-9]/g,'');
  return (d.length>=8&&d.length<=14)?d:''; }

/* Retrouve un produit meme si le zero de tete a saute quelque part. */
function trouve(bc){
  const T=tousLesArticles();
  /* « 3605533286555nobox » : les mêmes chiffres que la boîte, pas la même fiche (Sam, 6 oct. 2026) */
  const M=(typeof mentionBC==='function')?mentionBC(bc):{digits:String(bc).replace(/[^0-9]/g,''),mention:''};
  bc=M.digits||String(bc);
  const nu=bc.replace(/^0+/,'');
  const chif=x=>{ const s=String(x.bc); return /^\d{8,}[A-Za-z]+$/.test(s)?s.replace(/[^0-9]/g,''):s; };
  const C=T.filter(x=>x.bc && chif(x).replace(/^0+/,'')===nu);
  if(C.length){ const p=(typeof parMention==='function')?parMention(C,M.mention,x=>String(x.bc).replace(/[0-9]/g,'')+' '+x.nom+' '+(x.nomSrc||'')):C[0]; if(p) return p; if(M.mention) return null; }
  if(M.mention) return null;
  return T.find(x=>x.bcs && bcsDe(x).includes(nu))
    || T.find(x=>(bcExtra()[x.cle]||[]).includes(nu)) || null;
}

function litFacture(txt){
  const out=[];
  txt.replace(/\r/g,'').split('\n').forEach(l=>{
    if(!l.trim()) return;
    l=l.replace(/\((\d{4,})\)/g,' ');            // code interne du fournisseur, pas un prix
    const ch=l.split(/\t|;|\s{2,}|\|/).map(x=>x.trim()).filter(x=>x!=='');
    const plat = ch.length>=3 ? ch : l.trim().split(/\s+/);
    let bc='', iBc=-1;
    for(let i=0;i<plat.length;i++){ const b=normBC2(plat[i]);
      if(b && b.length>=11){ bc=b; iBc=i; break; } }
    if(!bc) return;
    const nums=[];
    plat.forEach((x,i)=>{ if(i===iBc) return;
      if(/^\d{6,}$/.test(x.replace(/[^0-9]/g,''))&&!/[.,]\d{2}$/.test(x)) return;  // reference, pas un montant
      const v=nombre(x); if(v!=null&&v>0) nums.push({v,i,dec:/[.,]\d{2}\b/.test(x)}); });
    if(!nums.length) return;
    /* prix unitaire = celui dont quantite x prix retombe sur un autre nombre de la ligne */
    let q=null,p=null;
    for(const a of nums){ if(!Number.isInteger(a.v)||a.v>5000) continue;
      for(const b of nums){ if(b.i===a.i||b.v<=0||b.v>4000) continue;
        const t=a.v*b.v;
        if(nums.some(c=>c.i!==a.i&&c.i!==b.i&&Math.abs(c.v-t)<=Math.max(0.6,t*0.004))){ q=a.v;p=b.v;break; } }
      if(p!=null) break; }
    if(p==null){                       /* feuille de tarifs : pas de quantite ni de total */
      let c=nums.filter(x=>x.dec&&x.v>0.5&&x.v<4000);
      if(!c.length) c=nums.filter(x=>x.v>0.5&&x.v<4000&&!(Number.isInteger(x.v)&&x.v<=60&&x.i===0));
      if(!c.length) return;
      p=c[c.length-1].v;
      const e=nums.find(x=>Number.isInteger(x.v)&&x.v<=5000&&x.i<c[c.length-1].i&&x.v!==p&&x.i!==0);
      q=e?e.v:null;
    }
    const mots=plat.filter((x,i)=>i!==iBc&&/[A-Za-zÀ-ÿ]{3}/.test(x));
    mots.sort((a,b)=>b.length-a.length);
    out.push({bc,des:(mots[0]||'').slice(0,80),q,p});
  });
  return out;
}

function dessineFacture(){
  const box=$('fc-res'), txt=$('fc-txt').value;
  if(txt.trim().length<12){ box.innerHTML=''; $('fc-ok').disabled=true; FACT=null; return; }
  const L=litFacture(txt);
  if(!L.length){ box.innerHTML=`<div class="mjw">Aucune ligne exploitable.
    Il faut au minimum un code-barres et un prix par ligne.</div>`;
    $('fc-ok').disabled=true; FACT=null; return; }
  let connues=0, inconnues=0, effet=0, montant=0;
  const li=L.map(x=>{
    const p=trouve(x.bc); x.p0=p; 
    montant += (x.q||0)*x.p;
    if(!p){ inconnues++;
      return `<tr class="inc"><td class="ref"><b>${esc(x.des||'—')}</b><span>${x.bc}</span></td>
        <td class="n">${x.q??'—'}</td><td class="n">${money(x.p)}</td>
        <td class="n">—</td><td>absent de l'inventaire</td></tr>`; }
    connues++;
    const anc=p.pa, d=anc!=null?x.p-anc:null;
    if(d!=null) effet += d*(x.q||0);
    const cls=d==null?'':(d<0?'baisse':d>0?'hausse':'');
    return `<tr><td class="ref"><b>${esc(p.marque)} ${esc(p.nom)}${tyBadge(p)}</b><span>${p.bc}</span></td>
      <td class="n">${x.q??'—'}</td><td class="n">${money(x.p)}</td>
      <td class="n">${anc!=null?money(anc):'—'}</td>
      <td class="n ${cls}">${d==null?'—':(d===0?'inchangé':(d>0?'+':'−')+money(Math.abs(d)))}</td></tr>`;
  }).join('');
  FACT={L,connues,inconnues,effet,montant};
  box.innerHTML=`
   <div class="mjk">
     <div><span class="v">${nf(L.length)}</span><span class="k">lignes lues</span></div>
     <div><span class="v" style="color:var(--iris)">${nf(connues)}</span><span class="k">produits reconnus</span></div>
     <div><span class="v"${inconnues?' style="color:var(--warn)"':''}>${nf(inconnues)}</span><span class="k">codes inconnus</span></div>
     <div><span class="v">${money(montant)}</span><span class="k">montant de la facture</span></div>
     <div><span class="v" style="color:${effet<0?'var(--good)':effet>0?'var(--crit)':'var(--ink-3)'}">${effet?(effet>0?'+':'−')+money(Math.abs(effet)):'0 $'}</span><span class="k">écart vs prix connus</span></div>
   </div>
   <div style="overflow-x:auto;margin-top:14px"><table class="ftb"><thead><tr>
     <th>Référence</th><th style="text-align:right">Qté</th><th style="text-align:right">Prix facturé</th>
     <th style="text-align:right">Prix connu</th><th style="text-align:right">Écart</th>
     </tr></thead><tbody>${li}</tbody></table></div>
   ${inconnues?`<div class="mjw" style="margin-top:12px"><b>${inconnues} code${inconnues>1?'s':''}-barres inconnu${inconnues>1?'s':''}.</b>
     Ces lignes ne seront pas enregistrées. Crée d'abord la fiche avec <b>+ Nouvel article</b>,
     puis rejoue la facture.</div>`:''}`;
  $('fc-ok').disabled = connues===0;
  $('fc-ok').textContent = connues?`Enregistrer ${nf(connues)} ligne${connues>1?'s':''}`:'Enregistrer';
}

function listeFrns(){
  const n=new Set(Object.keys(FRN));
  Object.values(HIST).forEach(l=>l.forEach(x=>{ if(x.f) n.add(x.f); }));
  $('l-frns').innerHTML=[...n].sort().map(x=>`<option value="${esc(x)}">`).join('');
}

$('fac').onclick=()=>{ location.href='factures.html'; return; $('fcov').classList.add('on'); $('fc-res').innerHTML='';
  $('fc-txt').value=''; $('fc-ok').disabled=true; $('fc-msg').textContent=''; FACT=null;
  if(!$('fc-date').value) $('fc-date').value=ajd();
  listeFrns(); setTimeout(()=>$('fc-frn').focus(),60); };
const fermeFac=()=>$('fcov').classList.remove('on');
$('fcx').onclick=fermeFac; $('fc-c').onclick=fermeFac;
$('fcov').addEventListener('click',e=>{ if(e.target===$('fcov')) fermeFac(); });
let fcT=null;
$('fc-txt').addEventListener('input',()=>{ clearTimeout(fcT); fcT=setTimeout(dessineFacture,320); });

$('fc-ok').onclick=()=>{
  if(!FACT) return;
  const frn=$('fc-frn').value.trim();
  if(!frn){ $('fc-msg').textContent='Indique le fournisseur.'; $('fc-frn').focus(); return; }
  const d=$('fc-date').value || ajd();
  const num=$('fc-num').value.trim();
  const majPrix=$('fc-maj').checked;
  if(!demandeUser(false,"enregistrer cette facture",()=>$('fc-ok').click())) return;
  let n=0, nmaj=0;
  FACT.L.forEach(x=>{
    const p=x.p0; if(!p) return;
    (HIST[p.id]=HIST[p.id]||[]).push({d,p:x.p,f:frn,q:x.q||null,src:'facture',num:num||null});
    n++;
    if(majPrix && p.pa!==x.p){
      const m=Object.assign({},MOD[p.id]||{}); m.pa=x.p; MOD[p.id]=m; nmaj++;
      log({act:'prix',lib:"prix d'achat, depuis "+frn,bc:p.bc,
           ref:(p.marque||'')+' '+(p.nom||''),av:p.pa??null,ap:x.p});
    }
  });
  FRN[frn]=Object.assign({nom:frn},FRN[frn]||{},{maj:new Date().toISOString()});
  sauveHIST(); sauveMOD(); sauveFRN();
  log({act:'fournisseur',lib:'facture enregistrée'+(num?' n° '+num:'')+' — '+frn,
       av:null, ap:`${n} ligne${n>1?'s':''} · ${money(FACT.montant)} · écart ${FACT.effet>=0?'+':'−'}${money(Math.abs(FACT.effet))}`});
  fermeFac(); render();
  if(FICHE) dessineFiche();
  alert(`${n} ligne${n>1?'s':''} ajoutée${n>1?'s':''} à l'historique.`+
        (nmaj?`\n${nmaj} prix d'achat mis à jour.`:'')+
        `\n\nTélécharge une sauvegarde : bouton « Sauvegarder mon travail ».`);
};


/* --- Facture déjà dépouillée, installée une seule fois ---
   Elle est posée ici pour que la rubrique Fournisseurs soit remplie dès la
   première ouverture, sans que personne ait à ressaisir la facture.
   Le marqueur empêche qu'elle soit comptée deux fois si elle est aussi
   enregistrée à la main. */
const KFACI='factures-installees-v1';
(function installe(){
  let faites=[]; try{ faites=JSON.parse(localStorage.getItem(KFACI)||'[]'); }catch(e){}
  const F=FACTURE_INIT;
  if(!F||!F.num||faites.includes(F.num)) return;
  /* si quelqu'un l'a déjà saisie à la main, on ne double pas */
  const dejaLa=Object.values(HIST).some(l=>l.some(a=>a.num===F.num));
  let n=0,maj=0;
  if(!dejaLa){
    F.lignes.forEach(l=>{
      (HIST[l.cle]=HIST[l.cle]||[]).push({d:F.d,p:l.p,f:F.frn,q:l.q,src:'facture',num:F.num});
      n++;
      if(l.pa0!=null && l.p!==l.pa0){
        const m=Object.assign({},MOD[l.cle]||{}); m.pa=l.p; MOD[l.cle]=m; maj++;
        log({act:'prix',lib:"prix d'achat, facture "+F.num+" — "+F.frn,bc:l.bc,ref:l.ref,av:l.pa0,ap:l.p});
      }
    });
    if(n){ log({act:'fournisseur',lib:'facture installée n° '+F.num+' — '+F.frn,av:null,
      ap:`${n} lignes · ${money(F.lignes.reduce((a,l)=>a+l.q*l.p,0))}`}); }
    sauveHIST(); sauveMOD();
  }
  FRN[F.frn]=Object.assign({nom:F.frn},FRN_INIT[F.frn]||{},FRN[F.frn]||{});
  sauveFRN();
  faites.push(F.num);
  try{ localStorage.setItem(KFACI,JSON.stringify(faites)); }catch(e){}
})();

/* Repere de depart : tout ce qui a ete pose par les fichiers eux-memes.
   Le rappel de sauvegarde ne doit compter que ce qu'une personne a reellement saisi —
   le reste se reinstalle tout seul et ne peut pas etre perdu. */
const KBASE='repere-installation-v1';
let BASE_NEUVE=false;
(function repere(){
  try{
    if(localStorage.getItem(KBASE)) return;
    BASE_NEUVE=true;
    localStorage.setItem(KBASE,JSON.stringify({
      'fiches-modifiees-v1':Object.keys(MOD).length,
      'articles-ajoutes-v1':AJ.length,
      'stock-externe-v1':Object.keys(EXT.q||{}).length,
      'comptage-parfums-v1':(function(){try{return Object.keys(JSON.parse(localStorage.getItem('comptage-parfums-v1')||'{}')).length;}catch(e){return 0;}})(),
      'crm-journal-v1':JOU.length,
      'prix-achat-hist-v1':Object.values(HIST).reduce((a,l)=>a+l.length,0),
      'marche-v1':Object.keys(MAR).length,
      'fournisseurs-v1':Object.keys(FRN).length,
      'factures-installees-v1':(function(){try{return JSON.parse(localStorage.getItem(KFACI)||'[]').length;}catch(e){return 0;}})(),
      'factures-v1':(function(){try{return JSON.parse(localStorage.getItem('factures-v1')||'[]').length;}catch(e){return 0;}})(),
      'reglages-v1':1}));
  }catch(e){}
})();


/* ================= SAUVEGARDE COMPLETE =================
   Un seul fichier qui contient TOUT ce qui a été saisi : corrections de fiches,
   articles ajoutés, stock importé, comptages, journal, nom de l'utilisateur.
   C'est ce fichier qui rend le travail indépendant de ce navigateur. */
const CLES=[['fiches-modifiees-v1','fiches corrigées',v=>Object.keys(v||{}).length],
            ['articles-ajoutes-v1','articles ajoutés',v=>(v||[]).length],
            ['stock-externe-v1','stock importé',v=>Object.keys((v&&v.q)||{}).length],
            ['comptage-parfums-v1','comptages saisis',v=>Object.keys(v||{}).length],
            ['crm-journal-v1','actions au journal',v=>(v||[]).length],
            ['prix-achat-hist-v1','achats historisés',v=>Object.values(v||{}).reduce((a,l)=>a+l.length,0)],
            ['marche-v1','relevés de marché',v=>Object.keys(v||{}).length],
            ['fournisseurs-v1','fournisseurs',v=>Object.keys(v||{}).length],
            ['factures-installees-v1','factures installées',v=>(v||[]).length],
            ['factures-v1','factures enregistrées',v=>(v||[]).length],
            ['ventes-v1','ventes historisées',v=>Object.values(v||{}).reduce((a,l)=>a+l.length,0)],
            ['clients-v1','clients',v=>Object.keys(v||{}).length],
            ['reglements-v1','règlements clients',v=>Object.keys(v||{}).length],
            ['commandes-v1','commandes déjà importées',v=>Object.keys(v||{}).length],
            ['connecteurs-v1','avancement des connexions',v=>Object.keys(v||{}).length],
            ['ventes-numeros-v1','numéros de vente utilisés',v=>Object.keys(v||{}).length],
            ['ajustements-v1','ajustements de stock',v=>(v||[]).length],
            ['reglages-v1','réglages',v=>v?1:0]];

function litCle(k){ try{ return JSON.parse(localStorage.getItem(k)||'null'); }catch(e){ return null; } }
/* Reparation unique : les navigateurs qui ont recu le Sheet et les releves Amazon du 3 septembre
   avec l'ancienne version ont vu ces installations comptees comme des saisies a la main. */
(function(){
  try{
    const K='repere-corrige-2026-09-03'; if(BASE_NEUVE||localStorage.getItem(K)) return;
    const b=JSON.parse(localStorage.getItem(KBASE)||'null'); if(!b) return;
    const n=k=>{ const c=CLES.find(x=>x[0]===k); return c?c[2](litCle(k)):0; };
    const bump=(k,d)=>{ b[k]=Math.min(n(k),(b[k]||0)+d); };
    bump('stock-externe-v1',Object.keys(SHEET_INIT.q).filter(bc=>EXT.q[bc]===SHEET_INIT.q[bc]).length);
    bump('fiches-modifiees-v1',Object.keys(SHEET_INIT.prix||{}).filter(c=>MOD[c]).length);
    bump('crm-journal-v1',JOU.filter(e=>e.u==='installation').length);
    bump('marche-v1',Object.keys(MARCHE_INIT).filter(k=>MAR[k]&&MAR[k].par==='relevé manuel').length - (b['marche-v1']||0) > 0 ? Object.keys(MARCHE_INIT).filter(k=>MAR[k]).length-(b['marche-v1']||0) : 0);
    localStorage.setItem(KBASE,JSON.stringify(b)); localStorage.setItem(K,'1');
  }catch(e){}
})();

function inventaireSauvegarde(){
  let base={}; try{ base=JSON.parse(localStorage.getItem('repere-installation-v1')||'{}'); }catch(e){}
  return CLES.map(([k,lib,cnt])=>{
    const n=cnt(litCle(k)), b=base[k]||0;
    return {k,lib,n,pose:Math.min(b,n),saisi:Math.max(0,n-b)};
  });
}
function dessineSvg(){
  const inv=inventaireSauvegarde();
  const tot=inv.reduce((a,x)=>a+x.n,0), saisi=inv.reduce((a,x)=>a+x.saisi,0);
  $('svinv').innerHTML=`<div class="svinv">${inv.map(x=>
    `<div><span class="v"${x.n?'':' style="color:var(--ink-3)"'}>${x.n}</span><span class="k">${x.lib}${
      x.pose&&x.saisi?`<br><em style="font-style:normal;opacity:.7">dont ${x.saisi} saisi${x.saisi>1?'s':''}</em>`:''}</span></div>`
    ).join('')}</div>` + (tot?'':`<div class="svko">Rien à sauvegarder pour l'instant.</div>`)
    + (tot&&!saisi?`<div class="svok" style="margin-top:12px">Tout ce qui est ici a été posé par les
      fichiers eux-mêmes : rien n'a encore été saisi à la main, donc rien ne peut être perdu.
      La sauvegarde reste possible, elle n'est simplement pas urgente.</div>`:'');
  $('svdl').disabled=!tot;
}
$('svg').onclick=()=>{ $('svov').classList.add('on'); $('svmsg2').innerHTML=''; dessineSvg(); };
const fermeSvg=()=>$('svov').classList.remove('on');
$('svx').onclick=fermeSvg; $('svc').onclick=fermeSvg;
$('svov').addEventListener('click',e=>{ if(e.target===$('svov')) fermeSvg(); });

$('svdl').onclick=()=>{
  const d={format:'crm-parfums-sauvegarde',version:1,le:new Date().toISOString(),
           par:(localStorage.getItem('crm-utilisateur-v1')||''),donnees:{}};
  CLES.forEach(([k])=>{ const v=litCle(k); if(v!=null) d.donnees[k]=v; });
  const u=localStorage.getItem('crm-utilisateur-v1'); if(u) d.donnees['crm-utilisateur-v1']=u;
  const b=new Blob([JSON.stringify(d)],{type:'application/json'});
  const a=document.createElement('a'); a.href=URL.createObjectURL(b);
  a.download='sauvegarde-crm-'+new Date().toISOString().slice(0,16).replace(/[:T]/g,'-')+'.json';
  a.click(); URL.revokeObjectURL(a.href);
  $('svmsg2').innerHTML='<div class="svok">Sauvegarde téléchargée. Range-la dans le dossier perfumestrade, à côté des autres fichiers.</div>';
};

$('svup').addEventListener('change',e=>{
  const f=e.target.files[0]; if(!f) return;
  const rd=new FileReader();
  rd.onload=()=>{
    let d; try{ d=JSON.parse(rd.result); }catch(x){
      $('svmsg2').innerHTML='<div class="svko">Ce fichier n\'est pas une sauvegarde lisible.</div>'; return; }
    if(!d||d.format!=='crm-parfums-sauvegarde'||!d.donnees){
      $('svmsg2').innerHTML='<div class="svko">Ce fichier n\'est pas une sauvegarde de cet outil.</div>'; return; }
    const q=Object.entries(d.donnees).map(([k,v])=>{
      const c=CLES.find(x=>x[0]===k); return c?`${c[2](v)} ${c[1]}`:null; }).filter(Boolean);
    const dd=new Date(d.le);
    if(!confirm(`Restaurer la sauvegarde du ${dd.toLocaleDateString('en-US',{timeZone:'America/New_York',})} à `+
      `${dd.toLocaleTimeString('fr-FR',{timeZone:'America/New_York',hour:'2-digit',minute:'2-digit'})}`+
      (d.par?` (${d.par})`:'')+` ?\n\n${q.join('\n')}\n\n`+
      `Tout ce qui est actuellement saisi dans ce navigateur sera remplacé.`)) return;
    Object.entries(d.donnees).forEach(([k,v])=>{
      try{ localStorage.setItem(k, typeof v==='string'?v:JSON.stringify(v)); }catch(x){}
    });
    $('svmsg2').innerHTML='<div class="svok">Sauvegarde restaurée. La page va se recharger.</div>';
    setTimeout(()=>location.reload(),900);
  };
  rd.readAsText(f,'utf-8');
  e.target.value='';
});

/* Rappel : si rien n'a été sauvegardé depuis 7 jours et qu'il y a du travail en cours. */
(function rappel(){
  const K='derniere-sauvegarde-v1';
  const tot=inventaireSauvegarde().reduce((a,x)=>a+x.saisi,0);
  if(tot<10) return;
  let d=0; try{ d=+(localStorage.getItem(K)||0); }catch(e){}
  if(d && Date.now()-d < 7*86400000) return;
  const el=$('extb'); if(!el) return;
  const w=document.createElement('div');
  w.className='rapsv';
  w.innerHTML=`<b>${tot} saisies faites à la main ne sont enregistrées que dans ce navigateur.</b>
    Télécharge une sauvegarde — c'est la seule copie qui survivra à un nettoyage d'historique.
    <button class="btn" id="rapok">Sauvegarder maintenant</button>`;
  el.parentNode.insertBefore(w,el);
  $('rapok').onclick=()=>{ $('svg').click(); };
})();
const marqueSauvegarde=()=>{ try{ localStorage.setItem('derniere-sauvegarde-v1',Date.now()); }catch(e){} };
$('svdl').addEventListener('click',marqueSauvegarde);

/* ================= MISE A JOUR DU STOCK DEPUIS UN TABLEUR ================= */
/* On ne demande pas a l'utilisateur de nommer ses colonnes : on les devine.
   Le code-barres est la colonne qui contient le plus de suites de 8 a 14 chiffres,
   la quantite est la colonne d'entiers la plus proche de l'inventaire connu. */
let MJ=null;
const nf=n=>Number(n||0).toLocaleString('fr-FR');

function decoupe(txt){
  const li=txt.replace(/\r/g,'').split('\n').filter(l=>l.trim()!=='');
  if(!li.length) return [];
  const sep = li[0].includes('\t') ? '\t' : (li[0].split(';').length>li[0].split(',').length ? ';' : ',');
  return li.map(l=>{
    const out=[]; let cur='', q=false;
    for(let i=0;i<l.length;i++){
      const c=l[i];
      if(c==='"'){ if(q&&l[i+1]==='"'){cur+='"';i++;} else q=!q; }
      else if(c===sep && !q){ out.push(cur); cur=''; }
      else cur+=c;
    }
    out.push(cur);
    return out.map(x=>x.trim());
  });
}

/* ============ MISE À JOUR DEPUIS LE TABLEUR (Google Sheet) ============
   30 sept. 2026 — la mise à jour ne reprenait que les QUANTITÉS : les prix restaient
   ceux du fichier de début septembre (un prix d'achat deux fois trop haut faussait une
   marge Amazon), et un parfum ajouté au Sheet depuis n'existait pas ici (une trentaine
   en stock, dont un vendu sur Amazon). Elle reprend maintenant, pour chaque ligne :
     - la quantité (le tableau fait foi, comme avant) ;
     - le prix d'achat, le prix de détail et le prix de gros, s'il y a une colonne
       qui porte ce nom (unit price / pvr / pvw, ou prix d'achat / retail / gros) ;
     - le parfum lui-même quand il n'existe pas ici et qu'il est en stock.
   Rapprochement : par le code-barres (avec ou sans zéros du début, les codes collés,
   les « autres codes-barres » d'une fiche), et à défaut par la marque + le nom exact
   — c'est ainsi qu'un code-barres changé dans le Sheet retrouve sa fiche, et le
   nouveau code est ajouté à la fiche au lieu d'en créer une seconde.
   Un code écrit avec des lettres (« …NOBOX », « …tester ») est un article à part :
   on ne le confond plus avec la version en boîte qui porte les mêmes chiffres. */
function cleCodes(v){
  const s=String(v==null?'':v).trim();
  if(!s||s==='-'||s==='—') return [];
  if(/[A-Za-z]/.test(s)){
    /* « 3605533286555nobox » : les chiffres de la boîte + la mention — rapproché par les
       chiffres, départagé par la mention (voir trouve) ; un vrai texte reste un texte */
    const M=(typeof mentionBC==='function')?mentionBC(s):{digits:'',mention:''};
    if(M.mention&&M.digits.length>=8) return ['M:'+M.mention+':'+M.digits.replace(/^0+/,'')];
    return ['T:'+s.toUpperCase().replace(/[^A-Z0-9]/g,'')];
  }
  const out=[], tout=s.replace(/[^0-9]/g,'').replace(/^0+/,'');
  if(tout.length>=6) out.push(tout);
  s.split(/[^0-9]+/).forEach(t=>{ if(t.length>=8&&t.length<=14) out.push(t.replace(/^0+/,'')); });
  return [...new Set(out)];
}
function normBC(v){ const k=cleCodes(v).find(x=>!x.startsWith('T:')&&x.length<=14); return k||''; }
const nomCle=(m,n)=>(String(m||'')+' | '+String(n||'')).toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g,'')
  .replace(/[^a-z0-9|]+/g,' ').replace(/\s+/g,' ').trim();
const COLS_SHEET={
  pa:/^(unit ?price|prix d.?achat|co[uû]t( d.?achat)?|cost|pa)$/i,
  pvr:/^(pvr|retail( price)?|prix (de )?d[ée]tail|prix retail)$/i,
  pvw:/^(pvw|wholesale( price)?|prix de gros)$/i,
  nom:/^(name|nom|d[ée]signation|product|produit)$/i,
  marque:/^(brand|marque)$/i,
  ml:/^(ml|oz|ml ?\/ ?fl ?oz|contenance|size|taille)$/i,
  type:/^type$/i, genre:/^(gender|genre|sexe)$/i
};
function analyseStock(txt){
  const L=decoupe(txt);
  if(L.length<2) return {err:"Il faut au moins une ligne d'en-tête et une ligne de données."};
  const nc=Math.max(...L.map(r=>r.length));
  const ent=L[0], corps=L.slice(1);
  const T=tousLesArticles();
  const IDX={}, NOMS={};
  /* un même code peut porter DEUX fiches (le coffret et le flacon, la version sans boîte :
     11 paires dans le fichier de Sam) — on garde toutes les fiches d'un code */
  const pose=(k,a)=>{ if(!k) return; const l=IDX[k]||(IDX[k]=[]); if(!l.includes(a)) l.push(a); };
  /* une fiche dont le code porte LUI-MÊME la mention (« …tester » en toutes lettres, créée par
     un import d'avant la règle des mentions) est aussi rangée sous ses chiffres : la ligne
     « …tester » du Sheet la retrouve, au lieu de donner ses flacons à la boîte */
  T.forEach(a=>{ cleCodes(a.bc).forEach(k=>{ pose(k,a); if(k.startsWith('M:')) pose(k.split(':')[2],a); });
    (bcExtra()[a.cle||a.id]||[]).forEach(k=>pose(String(k).replace(/^0+/,''),a));
    bcsDe(a).forEach(k=>pose(k,a));
    /* marque + nom : seulement quand UNE seule fiche le porte (sinon on ne devine pas) */
    [...new Set([a.nomSrc,a.nom].filter(Boolean))].forEach(n=>{ const k=nomCle(a.marque,n);
      if(!(k in NOMS)) NOMS[k]=a; else if(NOMS[k]!==a) NOMS[k]=null; }); });
  const nomsDe=a=>[a.nomSrc,a.nom].filter(Boolean).map(n=>nomCle(a.marque,n));
  /* plusieurs fiches pour ce code : celle qui porte le même nom, sinon une pas encore prise */
  const trouve=(c,nk,pris)=>{ const K=cleCodes(c); const C=[];
    /* un code à mention : les fiches des mêmes chiffres, puis celle qui porte la mention — et
       seulement elle : sans fiche « nobox », la ligne est un parfum à créer, pas la boîte */
    if(K.length&&K[0].startsWith('M:')){ const [,mention,digits]=K[0].split(':');
      (IDX[digits]||[]).forEach(a=>{ if(!C.includes(a)) C.push(a); });
      return (typeof parMention==='function')?parMention(C,mention,a=>a.nom+' '+(a.nomSrc||'')):null; }
    for(const k of K) (IDX[k]||[]).forEach(a=>{ if(!C.includes(a)) C.push(a); });
    if(C.length<2) return C[0]||null;
    /* un code sans mention ne prend pas une fiche « nobox » / « tester » s'il y a la boîte */
    const sans=C.filter(a=>!nomMention(a.nom+' '+(a.nomSrc||'')));
    const P=sans.length?sans:C;
    return (nk&&P.find(a=>nomsDe(a).includes(nk)))||(pris&&P.find(a=>!pris[a.id]))||P[0]; };

  /* colonne code-barres : celle qui reconnaît le plus de références */
  let cbc=-1, meilleur=0;
  for(let c=0;c<nc;c++){ let n=0; for(const r of corps) if(trouve(r[c])) n++; if(n>meilleur){ meilleur=n; cbc=c; } }
  if(cbc<0||meilleur<3) return {err:"Aucune colonne de codes-barres reconnue. Le tableau doit contenir une colonne de codes-barres correspondant à l'inventaire."};

  /* colonne quantité : son nom d'abord (REAL QTY, quantité, stock), sinon celle des
     entiers dont l'écart avec l'inventaire est le plus faible */
  let cq=ent.findIndex((h,c)=>c!==cbc&&/^(real ?qty|qty|quantit[ée]s?|qt[ée]|stock|quantity)$/i.test(String(h||'').trim()));
  if(cq<0){ let best=Infinity;
    for(let c=0;c<nc;c++){
      if(c===cbc) continue;
      let n=0, ecart=0, gros=0;
      for(const r of corps){ const a=trouve(r[cbc]); if(!a) continue; const v=nombre(r[c]);
        if(v==null||v<0||!Number.isInteger(v)) continue; if(v>100000){ gros++; continue; } n++; ecart+=Math.abs(v-(a.qte||0)); }
      if(n<3||gros>n) continue;
      const moy=ecart/n; if(moy<best){ best=moy; cq=c; }
    } }
  if(cq<0) return {err:"Aucune colonne de quantités trouvée. Il faut une colonne de nombres entiers."};
  const col={}; Object.entries(COLS_SHEET).forEach(([k,re])=>{ const i=ent.findIndex((h,c)=>c!==cbc&&c!==cq&&re.test(String(h||'').trim())); if(i>=0) col[k]=i; });

  const res={colBC:ent[cbc]||('colonne '+(cbc+1)), colQ:ent[cq]||('colonne '+(cq+1)), col,
             lignes:corps.length, connues:0, inconnues:[], change:[], egales:0, doublons:0,
             q:{}, prix:[], nouveaux:[], alias:[], parNom:0};
  const vu={}, qte={}, prixVu={};
  /* une fiche déjà retrouvée par son code sur une autre ligne n'est jamais reprise par le nom */
  const nkDe=r=>col.nom!=null?nomCle(col.marque!=null?r[col.marque]:'',r[col.nom]):'';
  const parCode={}; corps.forEach(r=>{ const a=trouve(r[cbc],nkDe(r),parCode); if(a) parCode[a.id]=true; });
  for(const r of corps){
    const code=String(r[cbc]||'').trim(), v=nombre(r[cq]);
    const nom=col.nom!=null?String(r[col.nom]||'').trim():'', marque=col.marque!=null?String(r[col.marque]||'').trim():'';
    let a=trouve(code,nkDe(r),vu), parNom=false;
    if(!a&&nom){ const x=NOMS[nomCle(marque,nom)]; if(x&&!vu[x.id]&&!parCode[x.id]){ a=x; parNom=true; } }
    const px=k=>{ if(col[k]==null) return null; const n=nombre(r[col[k]]); return (n!=null&&n>0&&n<100000)?Math.round(n*100)/100:null; };
    if(!a){
      if(code&&res.inconnues.length<40) res.inconnues.push(code);
      if(nom&&v!=null&&Number.isInteger(v)&&v>0){
        const k=cleCodes(code)[0]||nomCle(marque,nom);
        const M=(typeof mentionBC==='function')?mentionBC(code):{digits:'',mention:''};
        const bcN=(code==='-'||code==='—')?'':(M.mention&&M.digits.length>=8?M.digits:code);
        const nomN=(M.mention&&typeof nomAvecMention==='function')?nomAvecMention(nom,M.mention):nom;
        if(!res.nouveaux.some(o=>o._k===k))
          res.nouveaux.push({_k:k,bc:bcN,nom:nomN,marque,
            ml:col.ml!=null?String(r[col.ml]||'').trim():'',type:col.type!=null?String(r[col.type]||'').trim().toUpperCase():'',
            genre:col.genre!=null?String(r[col.genre]||'').trim().toUpperCase().slice(0,1):'',
            qte:v,pa:px('pa'),pvr:px('pvr'),pvw:px('pvw')});
      }
      continue;
    }
    if(parNom){ res.parNom++;
      const n=cleCodes(code).find(x=>!x.startsWith('T:')&&x.length<=14);
      if(n&&!res.alias.some(z=>z.id===a.id)) res.alias.push({id:a.id,code:n,marque:a.marque,nom:a.nom}); }
    if(v==null||v<0||!Number.isInteger(v)) continue;
    if(vu[a.id]!==undefined) res.doublons++;
    vu[a.id]=true; res.connues++; qte[a.id]={a,v};
    ['pa','pvr','pvw'].forEach(k=>{ const n=px(k); if(n==null) return; prixVu[a.id+'|'+k]={a,k,n}; });
  }
  /* le stock importé est rangé par code-barres : deux fiches qui partagent un code
     prendraient la même quantité — pour elles, la quantité va dans la fiche */
  const nbBC={}; T.forEach(a=>{ if(!String(a.id).startsWith('a')&&a.bc) nbBC[a.bc]=(nbBC[a.bc]||0)+1; });
  res.qMod={};
  Object.values(qte).forEach(({a,v})=>{
    /* une fiche SANS code-barres (74 dans le fichier) : sa quantité va dans la fiche —
       rangée sous la clé vide, elle aurait été donnée à toutes les fiches sans code */
    if(!String(a.id).startsWith('a')){ if(!a.bc||nbBC[a.bc]>1) res.qMod[a.id]=v; else res.q[a.bc]=v; }
    const av=a.qte||0;
    if(v===av) res.egales++;
    else res.change.push({id:a.id,bc:a.bc,nom:a.nom,marque:a.marque,type:a.type,genre:a.genre,av,ap:v,d:v-av,val:(v-av)*(a.pa||0)});
  });
  res.qId=Object.fromEntries(Object.values(qte).map(({a,v})=>[a.id,v]));
  Object.values(prixVu).forEach(({a,k,n})=>{ const av=a[k]; if(av==null||Math.abs(av-n)>0.005)
    res.prix.push({id:a.id,bc:a.bc,marque:a.marque,nom:a.nom,k,av:av==null?null:av,ap:n}); });
  res.prix.sort((x,y)=>Math.abs((y.ap||0)-(y.av||0))-Math.abs((x.ap||0)-(x.av||0)));
  res.change.sort((a,b)=>Math.abs(b.val)-Math.abs(a.val));
  res.impact=res.change.reduce((a,c)=>a+c.val,0);
  res.absents=T.filter(a=>a.qte>0 && res.qId[a.id]===undefined);
  res.perdusMod=Object.keys(MOD).filter(id=>MOD[id].qte!==undefined&&res.qId[id]!==undefined&&res.qId[id]!==MOD[id].qte).length;
  res.total=res.change.length+res.prix.length+res.nouveaux.length+res.alias.length;
  return res;
}

function dessineMJ(r){
  const box=$('mjres');
  if(r.err){ box.innerHTML=`<div class="mjw">${esc(r.err)}</div>`; $('mjok').disabled=true; MJ=null; return; }
  MJ=r;
  const t3=(a,b,c)=>(typeof L3==='function'?L3(a,b,c):a);
  const LIBK={pa:t3("prix d'achat",'cost','precio de compra'),pvr:t3('prix de détail','retail price','precio minorista'),pvw:t3('prix de gros','wholesale price','precio mayorista')};
  const h3=s=>`<h3 data-nolang style="font-family:Inter,sans-serif;font-size:9.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--ink-2);font-weight:700;margin:18px 0 8px">${s}</h3>`;
  const li=r.change.slice(0,15).map(c=>`<tr>
    <td><b>${esc(c.marque)}</b><br><span style="color:var(--ink-3)">${esc(c.nom)}${tyBadge(c)}</span></td>
    <td class="n">${c.av}</td>
    <td class="n ${c.d>0?'up':'dn'}">${c.d>0?'+':'−'}${Math.abs(c.d)}</td>
    <td class="n">${c.ap}</td>
    <td class="n ${c.val>0?'up':'dn'}">${c.val?money(c.val):'—'}</td></tr>`).join('');
  const lp=r.prix.slice(0,20).map(c=>`<tr><td><b>${esc(c.marque)}</b> <span style="color:var(--ink-3)">${esc(c.nom)}</span></td>
    <td data-nolang>${esc(LIBK[c.k])}</td><td class="n" data-nolang>${c.av==null?'—':money(c.av)}</td><td class="n" data-nolang>${money(c.ap)}</td></tr>`).join('');
  const ln=r.nouveaux.map(o=>`<tr><td><b>${esc(o.marque)}</b> <span style="color:var(--ink-3)">${esc(o.nom)}</span></td>
    <td class="mono" style="font-size:11.5px" data-nolang>${esc(o.bc||'—')}</td><td class="n" data-nolang>${o.qte}</td>
    <td class="n" data-nolang>${o.pa==null?'—':money(o.pa)}</td></tr>`).join('');
  const la=r.alias.map(z=>`<tr><td><b>${esc(z.marque)}</b> <span style="color:var(--ink-3)">${esc(z.nom)}</span></td><td class="mono" data-nolang>${esc(z.code)}</td></tr>`).join('');
  box.innerHTML=`
  <div class="mjmap">Colonne code-barres reconnue : <b>${esc(r.colBC)}</b> ·
    colonne quantité : <b>${esc(r.colQ)}</b></div>
  <div class="mjk" style="margin-top:12px">
    <div><span class="v">${nf(r.connues)}</span><span class="k">références reconnues</span></div>
    <div><span class="v" style="color:var(--iris)">${nf(r.change.length)}</span><span class="k">quantités modifiées</span></div>
    <div><span class="v" style="color:var(--iris)">${nf(r.prix.length)}</span><span class="k" data-nolang>${t3('prix modifiés','prices changed','precios modificados')}</span></div>
    <div><span class="v" style="color:var(--iris)">${nf(r.nouveaux.length)}</span><span class="k" data-nolang>${t3('parfums créés','perfumes created','perfumes creados')}</span></div>
    <div><span class="v" style="color:${r.impact>=0?'var(--good)':'var(--crit)'}">${r.impact?money(r.impact):'0 $'}</span><span class="k">effet sur la valeur du stock</span></div>
  </div>
  ${(r.col.pa==null&&r.col.pvr==null&&r.col.pvw==null)?`<div class="mjw" style="margin-top:12px" data-nolang>${t3('Aucune colonne de prix reconnue (unit price, pvr, pvw) : seules les quantités seront reprises.','No price column recognized (unit price, pvr, pvw): only quantities will be updated.','Ninguna columna de precios reconocida (unit price, pvr, pvw): solo se actualizarán las cantidades.')}</div>`:''}
  ${r.absents.length?`<div class="mjw" style="margin-top:12px"><b>${nf(r.absents.length)} référence${r.absents.length>1?'s':''} en stock ici mais absente${r.absents.length>1?'s':''} du tableau collé.</b>
    Leur quantité n'est <b>pas</b> remise à zéro — le tableau est peut-être partiel. Si le Sheet est censé être complet, ces références sont écoulées et il faut les passer à zéro à la main.</div>`:''}
  ${r.doublons?`<div class="mjw" style="margin-top:12px"><b>${nf(r.doublons)} code${r.doublons>1?'s':''}-barres en double</b> dans le tableau — c'est la dernière ligne qui l'emporte.</div>`:''}
  ${r.perdusMod?`<div class="mjw" style="margin-top:12px"><b>${nf(r.perdusMod)} quantité${r.perdusMod>1?'s':''} que tu avais corrigée${r.perdusMod>1?'s':''} à la main</b> ${r.perdusMod>1?'seront remplacées':'sera remplacée'} par la valeur du tableau. Le tableau fait foi.</div>`:''}
  ${r.nouveaux.length?h3(t3(`${r.nouveaux.length} parfum${r.nouveaux.length>1?'s':''} en stock dans le tableau, absent${r.nouveaux.length>1?'s':''} d'ici — ${r.nouveaux.length>1?'ils seront créés':'il sera créé'}`,`${r.nouveaux.length} perfume${r.nouveaux.length>1?'s':''} in stock in the sheet, missing here — will be created`,`${r.nouveaux.length} perfume${r.nouveaux.length>1?'s':''} en stock en la hoja, ausente${r.nouveaux.length>1?'s':''} aquí — se crearán`))+
    `<div style="overflow-x:auto"><table class="mjt"><thead><tr data-nolang><th>${t3('Parfum','Perfume','Perfume')}</th><th>${t3('Code-barres','Barcode','Código de barras')}</th><th style="text-align:right">${t3('Stock','Stock','Stock')}</th><th style="text-align:right">${t3('Achat','Cost','Compra')}</th></tr></thead><tbody>${ln}</tbody></table></div>`:''}
  ${r.alias.length?h3(t3(`${r.alias.length} code${r.alias.length>1?'s':''}-barres changé${r.alias.length>1?'s':''} dans le tableau — ajouté${r.alias.length>1?'s':''} à la fiche existante`,`${r.alias.length} barcode${r.alias.length>1?'s':''} changed in the sheet — added to the existing item`,`${r.alias.length} código${r.alias.length>1?'s':''} cambiado${r.alias.length>1?'s':''} en la hoja — añadido${r.alias.length>1?'s':''} a la ficha existente`))+
    `<div style="overflow-x:auto"><table class="mjt"><tbody>${la}</tbody></table></div>`:''}
  ${r.prix.length?h3(t3(`Les ${Math.min(20,r.prix.length)} plus gros changements de prix${r.prix.length>20?' sur '+nf(r.prix.length):''}`,`The ${Math.min(20,r.prix.length)} biggest price changes${r.prix.length>20?' out of '+nf(r.prix.length):''}`,`Los ${Math.min(20,r.prix.length)} mayores cambios de precio${r.prix.length>20?' de '+nf(r.prix.length):''}`))+
    `<div style="overflow-x:auto"><table class="mjt"><thead><tr data-nolang><th>${t3('Parfum','Perfume','Perfume')}</th><th>${t3('Prix','Price','Precio')}</th><th style="text-align:right">${t3('Avant','Before','Antes')}</th><th style="text-align:right">${t3('Après','After','Después')}</th></tr></thead><tbody>${lp}</tbody></table></div>`:''}
  ${r.change.length?`<h3 style="font-family:Inter,sans-serif;font-size:9.5px;letter-spacing:.14em;
    text-transform:uppercase;color:var(--ink-2);font-weight:700;margin:18px 0 8px">
    Les ${Math.min(15,r.change.length)} plus gros mouvements${r.change.length>15?` sur ${nf(r.change.length)}`:''}</h3>
   <div style="overflow-x:auto"><table class="mjt"><thead><tr>
    <th>Référence</th><th style="text-align:right">Avant</th><th style="text-align:right">Écart</th>
    <th style="text-align:right">Après</th><th style="text-align:right">Valeur</th></tr></thead>
    <tbody>${li}</tbody></table></div>`:(r.total?'':'<div class="mjw" style="margin-top:12px">Aucune quantité ne change : le tableau est identique à l\'inventaire actuel.</div>')}`;
  $('mjok').disabled = !r.total;
  $('mjok').textContent = r.total?`Appliquer ${nf(r.total)} changement${r.total>1?'s':''}`:'Appliquer';
}

/* ===== LA PRICE LIST (Igal, 22 oct. 2026) =====
   « À la demande d'un client, Sam doit envoyer la price list de 100 % de ses produits en stock, avec le prix de
   gros, en Excel ou en PDF avec le logo ; à lui de cocher s'il met les prix, la quantité. » Tout ce qui est en
   stock, trié par marque ; le PDF est un vrai texte (pas une photo) : 1 900 lignes tiennent en ~40 pages légères. */
const PL_T={
  en:{titre:'Wholesale price list',pour:'Prepared for',date:'Date',n:'products in stock',brand:'Brand',prod:'Product',size:'Size',type:'Type',qty:'Qty',price:'Wholesale',upc:'UPC',demande:'on request',page:'Page',pdf:'price-list'},
  es:{titre:'Lista de precios mayorista',pour:'Preparada para',date:'Fecha',n:'productos en stock',brand:'Marca',prod:'Producto',size:'Tamaño',type:'Tipo',qty:'Cant.',price:'Mayorista',upc:'UPC',demande:'a consultar',page:'Página',pdf:'lista-de-precios'},
  fr:{titre:'Price list de gros',pour:'Préparée pour',date:'Date',n:'parfums en stock',brand:'Marque',prod:'Parfum',size:'Contenance',type:'Type',qty:'Qté',price:'Prix de gros',upc:'Code-barres',demande:'sur demande',page:'Page',pdf:'price-list'}};
function plOpts(){ return {prix:$('pl-prix').checked,qte:$('pl-qte').checked,sans:$('pl-sans').checked,fmt:(document.querySelector('input[name=plf]:checked')||{}).value||'pdf',lg:$('pl-lg').value||'en',client:$('pl-client').value.trim()}; }
function plLignes(o){
  const out=[];
  tousLesArticles().forEach(p=>{ const q=+p.qte||0; if(q<=0) return;
    const nom=String(p.nom||'').trim(), marque=String(p.marque||'').trim(); if(!nom&&!marque) return;
    const pvw=(p.pvw!=null&&p.pvw!=='')?+p.pvw:null; if(!(pvw>0)&&!o.sans) return;
    out.push({bc:String(p.bc||'').trim(),marque,nom,ml:String(p.ml||'').trim(),type:String(p.type||'').trim(),q,pvw:pvw>0?pvw:null}); });
  out.sort((a,b)=>(a.marque.toLowerCase()+' '+a.nom.toLowerCase()).localeCompare(b.marque.toLowerCase()+' '+b.nom.toLowerCase()));
  return out;
}
function plCompte(){ try{ const o=plOpts(); const L=plLignes(o); const sans=L.filter(x=>x.pvw==null).length;
  $('pl-compte').textContent=nf(L.length)+' '+L3('parfums en stock','products in stock','perfumes en stock')+(sans?' — '+nf(sans)+' '+L3('sans prix de gros','without wholesale price','sin precio mayorista'):'')+(o.prix?'':' — '+L3('sans les prix','without prices','sin precios'));
  $('pl-wa').style.display=$('pl-em').style.display=o.fmt==='pdf'?'':'none'; $('pl-env').style.display=o.fmt==='pdf'?'':'none'; }catch(e){} }
const plNum=()=>{ const d=new Date(); const z=n=>String(n).padStart(2,'0'); return 'PL-'+d.getFullYear()+z(d.getMonth()+1)+z(d.getDate())+'-'+z(d.getHours())+z(d.getMinutes()); };
const plDateUS=()=>{ const d=new Date(); return (d.getMonth()+1)+'/'+d.getDate()+'/'+d.getFullYear(); };
const plUSD=v=>'$'+Number(v).toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g,',');
function plXlsx(L,o){
  const T=PL_T[o.lg]||PL_T.en;
  const col=[{t:T.brand},{t:T.prod},{t:T.size},{t:T.type}]; if(o.qte) col.push({t:T.qty,y:'n'}); if(o.prix) col.push({t:T.price,y:'m'}); col.push({t:T.upc});
  sortieXlsx({titre:T.titre+(o.client?' — '+o.client:''),fichier:T.pdf+'-'+plDateUS().replace(/\//g,'-'),colonnes:col,
    lignes:L.map(x=>{ const r=[x.marque,x.nom,x.ml?x.ml+' oz':'',x.type]; if(o.qte) r.push(x.q); if(o.prix) r.push(x.pvw==null?T.demande:x.pvw); r.push(x.bc); return r; })});
}
async function plPdfLibs(){
  if(window.jspdf) return;
  if(location.protocol==='file:') throw new Error("Le PDF se fabrique sur la version en ligne de l'outil.");
  await new Promise((res,rej)=>{ const sc=document.createElement('script'); sc.src='lib/pdf/jspdf.umd.min.js'; sc.onload=res; sc.onerror=()=>rej(new Error('Moteur PDF introuvable')); document.head.appendChild(sc); });
}
/* la taille d'une image (data URL) pour la placer sans la déformer */
const plImg=src=>new Promise(r=>{ const i=new Image(); i.onload=()=>r({w:i.naturalWidth,h:i.naturalHeight,ok:true}); i.onerror=()=>r({ok:false}); i.src=src; });
async function plPdf(L,o){
  await plPdfLibs();
  const T=PL_T[o.lg]||PL_T.en, F=Object.assign({enseigne:'Perfumes Trade'},(REG&&REG.fact)||{});
  const {jsPDF}=window.jspdf; const pdf=new jsPDF({unit:'pt',format:'letter',orientation:'portrait',compress:true});
  const W=pdf.internal.pageSize.getWidth(), H=pdf.internal.pageSize.getHeight(), m=40, ligneH=13.5, bas=H-40;
  /* les colonnes : largeur fixe pour ce qui est court, le reste au nom */
  const cols=[{k:'marque',t:T.brand,w:100},{k:'nom',t:T.prod,w:0},{k:'ml',t:T.size,w:44,r:true},{k:'type',t:T.type,w:40}];
  if(o.qte) cols.push({k:'q',t:T.qty,w:34,r:true}); if(o.prix) cols.push({k:'pvw',t:T.price,w:62,r:true}); cols.push({k:'bc',t:T.upc,w:76});
  const fixe=cols.reduce((a,c)=>a+(c.w||0),0); cols.find(c=>!c.w).w=W-2*m-fixe;
  const coupe=(s,w,taille)=>{ pdf.setFontSize(taille); s=String(s==null?'':s); if(pdf.getTextWidth(s)<=w) return s; while(s.length&&pdf.getTextWidth(s+'…')>w) s=s.slice(0,-1); return s+'…'; };
  const val=(x,k)=>k==='ml'?(x.ml?x.ml+' oz':''):k==='q'?String(x.q):k==='pvw'?(x.pvw==null?T.demande:plUSD(x.pvw)):(x[k]||'');
  let y=m, page=1;
  const entete=async()=>{
    y=m;
    if(page===1){
      let x=m;
      if(F.logo){ const im=await plImg(F.logo); if(im.ok){ const h=46, w=Math.min(170,h*im.w/im.h); try{ pdf.addImage(F.logo,'PNG',m,y,w,h); x=m+w+14; }catch(e){ try{ pdf.addImage(F.logo,'JPEG',m,y,w,h); x=m+w+14; }catch(_){} } } }
      pdf.setFont('helvetica','bold'); pdf.setFontSize(16); pdf.text(F.enseigne||'Perfumes Trade',x,y+16);
      pdf.setFont('helvetica','normal'); pdf.setFontSize(9); pdf.setTextColor(90);
      const co=[F.adresse,F.tel,F.email].filter(Boolean).join('  ·  '); if(co) pdf.text(coupe(co,W-x-m,9),x,y+30);
      pdf.setTextColor(0);
      y+=62;
      pdf.setFont('helvetica','bold'); pdf.setFontSize(13); pdf.text(T.titre,m,y);
      pdf.setFont('helvetica','normal'); pdf.setFontSize(9.5);
      /* chiffres en anglais : l'espace fine du format français n'existe pas dans la police du PDF */
      pdf.text(T.date+': '+plDateUS()+'   ·   '+L.length.toLocaleString('en-US')+' '+T.n,W-m,y,{align:'right'});
      y+=16;
      if(o.client){ pdf.setFontSize(10.5); pdf.text(T.pour+' '+o.client,m,y); y+=16; }
      y+=4;
    }
    /* les titres des colonnes, sur chaque page */
    pdf.setFillColor(240,239,244); pdf.rect(m,y-9,W-2*m,ligneH+1,'F');
    pdf.setFont('helvetica','bold'); pdf.setFontSize(8.5); let x=m+3;
    cols.forEach(c=>{ pdf.text(c.t,c.r?x+c.w-6:x,y+1,c.r?{align:'right'}:undefined); x+=c.w; });
    y+=ligneH+2; pdf.setFont('helvetica','normal'); pdf.setFontSize(8.5);
  };
  const pied=()=>{ pdf.setFontSize(8); pdf.setTextColor(120); pdf.text((F.enseigne||'Perfumes Trade')+'  ·  '+T.titre+'  ·  '+plDateUS(),m,H-22); pdf.text(T.page+' '+page,W-m,H-22,{align:'right'}); pdf.setTextColor(0); };
  await entete();
  let marqueAv='';
  for(const x of L){
    if(y+ligneH>bas){ pied(); pdf.addPage(); page++; await entete(); marqueAv=''; }
    let px=m+3;
    cols.forEach(c=>{ let v=val(x,c.k);
      if(c.k==='marque'){ if(v===marqueAv) v=''; else marqueAv=v; pdf.setFont('helvetica',v?'bold':'normal'); } else pdf.setFont('helvetica','normal');
      v=coupe(v,c.w-8,8.5); pdf.text(v,c.r?px+c.w-6:px,y,c.r?{align:'right'}:undefined); px+=c.w; });
    pdf.setDrawColor(228); pdf.line(m,y+4,W-m,y+4);
    y+=ligneH;
  }
  pied();
  return pdf.output('blob');
}
function plNote(o,L,quoi,a){
  log({act:'vente',lib:'price list de gros '+quoi+(a?' — '+a:'')+' ('+(o.fmt==='pdf'?'PDF':'Excel')+', '+nf(L.length)+' parfums'+(o.prix?', avec les prix':', sans les prix')+(o.qte?', avec les quantités':'')+(o.client?', pour '+o.client:'')+')',ref:'',av:null,ap:null});
}
async function plLien(blob,o,L){
  if(typeof CK_URL==='undefined'||typeof ckTok!=='function'||!ckTok()) throw new Error("Pas de session serveur : télécharge le PDF et envoie-le toi-même.");
  const T=PL_T[o.lg]||PL_T.en, num=plNum(), F=(REG&&REG.fact)||{};
  const q='?type=pricelist&enseigne='+encodeURIComponent(F.enseigne||'Perfumes Trade')+'&date='+encodeURIComponent(plDateUS())+'&lignes='+L.length+'&langue='+o.lg;
  const r=await fetch(CK_URL+'/api/o/'+CK_ORG+'/docs/'+encodeURIComponent(num)+q,{method:'PUT',headers:{'Content-Type':'application/pdf',Authorization:'Bearer '+ckTok()},body:blob});
  const j=await r.json().catch(()=>({})); if(!r.ok) throw new Error(j.erreur||('Dépôt du PDF refusé ('+r.status+')'));
  return {num,url:j.url,T};
}
const plMsg=(t,err)=>{ const e=$('pl-msg'); e.textContent=t||''; e.style.color=err?'var(--crit)':''; };
$('plb').onclick=()=>{ $('plov').classList.add('on'); plMsg(''); plCompte(); };
$('pl-x').onclick=$('pl-ann').onclick=()=>$('plov').classList.remove('on');
['pl-prix','pl-qte','pl-sans','pl-lg'].forEach(i=>$(i).addEventListener('change',plCompte));
document.querySelectorAll('input[name=plf]').forEach(r=>r.addEventListener('change',plCompte));
$('pl-dl').onclick=async()=>{ const o=plOpts(), L=plLignes(o); if(!L.length){ plMsg('Aucun parfum en stock.',true); return; }
  $('pl-dl').disabled=true;
  try{
    if(o.fmt==='xlsx'){ plXlsx(L,o); plNote(o,L,'téléchargée'); plMsg(L3('Excel téléchargé.','Excel downloaded.','Excel descargado.')); }
    else { plMsg(L3('Fabrication du PDF…','Building the PDF…','Creando el PDF…')); const b=await plPdf(L,o); const a=document.createElement('a'); a.href=URL.createObjectURL(b); a.download=(PL_T[o.lg]||PL_T.en).pdf+'-'+plDateUS().replace(/\//g,'-')+'.pdf'; a.click(); setTimeout(()=>URL.revokeObjectURL(a.href),4000); plNote(o,L,'téléchargée'); plMsg(L3('PDF téléchargé.','PDF downloaded.','PDF descargado.')); }
  }catch(e){ plMsg((e&&e.message)||'échec',true); }
  $('pl-dl').disabled=false; };
$('pl-wa').onclick=async()=>{ const o=plOpts(), L=plLignes(o); const num=String($('pl-tel').value||'').replace(/[^\d]/g,'');
  if(!num||num.length<8){ plMsg(L3('Tape le numéro WhatsApp du client.','Type the customer\'s WhatsApp number.','Escribe el número de WhatsApp del cliente.'),true); $('pl-tel').focus(); return; }
  const w=window.open('','_blank'); $('pl-wa').disabled=true;
  try{ plMsg(L3('Fabrication du PDF…','Building the PDF…','Creando el PDF…')); const b=await plPdf(L,o); plMsg(L3('Dépôt en ligne…','Uploading…','Subiendo…')); const d=await plLien(b,o,L);
    const txt=(o.lg==='es'?'Hola'+(o.client?' '+o.client:'')+', aquí está nuestra lista de precios mayorista ('+plDateUS()+').':o.lg==='fr'?'Bonjour'+(o.client?' '+o.client:'')+', voici notre price list de gros ('+plDateUS()+').':'Hello'+(o.client?' '+o.client:'')+', here is our wholesale price list ('+plDateUS()+').')+'\n\n'+d.url;
    const url='https://wa.me/'+(num.length<=10?'1'+num:num)+'?text='+encodeURIComponent(txt); window.__wa=url;
    let ok=false; try{ if(w&&!w.closed){ w.location.href=url; ok=true; } }catch(e){} if(!ok) window.open(url,'_blank');
    plNote(o,L,'envoyée par WhatsApp',num); plMsg(L3('Lien envoyé dans WhatsApp.','Link sent to WhatsApp.','Enlace enviado a WhatsApp.'));
  }catch(e){ try{ if(w&&!w.closed) w.close(); }catch(_){} plMsg((e&&e.message)||'échec',true); }
  $('pl-wa').disabled=false; };
$('pl-em').onclick=async()=>{ const o=plOpts(), L=plLignes(o); const a=String($('pl-mail').value||'').trim();
  if(!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(a)){ plMsg(L3('Tape l\'adresse email du client.','Type the customer\'s email address.','Escribe el email del cliente.'),true); $('pl-mail').focus(); return; }
  $('pl-em').disabled=true;
  try{ plMsg(L3('Fabrication du PDF…','Building the PDF…','Creando el PDF…')); const b=await plPdf(L,o); plMsg(L3('Dépôt en ligne…','Uploading…','Subiendo…')); const d=await plLien(b,o,L);
    const F=(REG&&REG.fact)||{}; const ens=F.enseigne||'Perfumes Trade';
    const sujet=(o.lg==='es'?'Lista de precios mayorista — ':o.lg==='fr'?'Price list de gros — ':'Wholesale price list — ')+ens+' ('+plDateUS()+')';
    const texte=(o.lg==='es'?'Hola'+(o.client?' '+o.client:'')+',\n\nAquí está nuestra lista de precios mayorista del '+plDateUS()+' ('+nf(L.length)+' productos en stock) :\n\n'+d.url+'\n\nGracias,\n'+ens
      :o.lg==='fr'?'Bonjour'+(o.client?' '+o.client:'')+',\n\nVoici notre price list de gros du '+plDateUS()+' ('+nf(L.length)+' parfums en stock) :\n\n'+d.url+'\n\nMerci,\n'+ens
      :'Hello'+(o.client?' '+o.client:'')+',\n\nHere is our wholesale price list as of '+plDateUS()+' ('+nf(L.length)+' products in stock):\n\n'+d.url+'\n\nThank you,\n'+ens);
    plMsg(L3('Envoi…','Sending…','Enviando…'));
    const r=await fetch(CK_URL+'/api/o/'+CK_ORG+'/docs/'+encodeURIComponent(d.num)+'/courrier',{method:'POST',headers:{'Content-Type':'application/json',Authorization:'Bearer '+ckTok()},body:JSON.stringify({a,sujet,texte})});
    const j=await r.json().catch(()=>({})); if(!r.ok) throw new Error(j.erreur||('Envoi refusé ('+r.status+')'));
    plNote(o,L,'envoyée par email',a); plMsg(L3('Envoyée à ','Sent to ','Enviada a ')+a+' ✓');
  }catch(e){ plMsg((e&&e.message)||'échec',true); }
  $('pl-em').disabled=false; };

$('maj').onclick=()=>{ $('mjov').classList.add('on'); $('mjres').innerHTML='';
  $('mjtxt').value=''; $('mjok').disabled=true; $('mjmsg').textContent=''; MJ=null;
  setTimeout(()=>$('mjtxt').focus(),60); };
const fermeMJ=()=>$('mjov').classList.remove('on');
$('mjx').onclick=fermeMJ; $('mjc').onclick=fermeMJ;
$('mjov').addEventListener('click',e=>{ if(e.target===$('mjov')) fermeMJ(); });
let mjT=null;
$('mjtxt').addEventListener('input',()=>{ clearTimeout(mjT);
  mjT=setTimeout(()=>{ const t=$('mjtxt').value.trim(); if(t.length<10){ $('mjres').innerHTML=''; $('mjok').disabled=true; return; }
    dessineMJ(analyseStock(t)); },350); });
$('mjfile').addEventListener('change',e=>{ const f=e.target.files[0]; if(!f) return;
  /* tableur, CSV, PDF ou photo : une seule porte, qui rend des lignes */
  $('mjres').innerHTML='<p class="hint">Lecture de '+esc(f.name)+'…</p>';
  lireFichier(f, m=>{ $('mjres').innerHTML='<p class="hint">'+esc(m)+'</p>'; })
    .then(t=>{ $('mjtxt').value=t; dessineMJ(analyseStock(t)); })
    .catch(err=>{ $('mjres').innerHTML='<p class="hint" style="color:var(--crit)">'+esc(err.message||'Lecture impossible.')+'</p>'; });
  e.target.value=''; });
$('mjok').onclick=()=>{
  if(!MJ) return;
  if(!demandeUser(false,"mettre le stock à jour",()=>$('mjok').click())) return;
  const t=new Date().toISOString();
  EXT={q:MJ.q,date:t,src:MJ.colBC+' / '+MJ.colQ};
  /* les articles ajoutés ici portent leur quantité eux-mêmes */
  AJ.forEach(o=>{ if(o&&o.id&&MJ.qId[o.id]!==undefined) o.qte=MJ.qId[o.id]; });
  if(MJ.change.length) log({act:'import',lib:'mise à jour du stock depuis un tableur',
       n:MJ.change.length,impact:Math.round(MJ.impact),
       det:MJ.change.slice(0,600).map(c=>({bc:c.bc,ref:c.marque+' '+c.nom,av:c.av,ap:c.ap}))});
  /* le tableau fait foi : on retire les corrections de quantité qu'il contredit */
  Object.keys(MOD).forEach(id=>{
    if(MOD[id].qte===undefined||MJ.qId[id]===undefined) return;
    delete MOD[id].qte;
    if(!Object.keys(MOD[id]).length) delete MOD[id];
  });
  Object.entries(MJ.qMod||{}).forEach(([id,v])=>{ MOD[id]=Object.assign({},MOD[id]||{},{qte:v}); });
  /* les prix du tableau */
  MJ.prix.forEach(c=>{ MOD[c.id]=Object.assign({},MOD[c.id]||{},{[c.k]:c.ap}); });
  /* une ligne de journal par prix, comme un changement fait dans la fiche */
  MJ.prix.forEach(c=>log({act:'prix',champ:c.k,lib:(LIBCH[c.k]||c.k)+' — repris du tableur',bc:c.bc,ref:c.marque+' '+c.nom,av:c.av,ap:c.ap}));
  /* un code-barres changé dans le tableau : ajouté à la fiche, pas une seconde fiche */
  MJ.alias.forEach(z=>{ const m=MOD[z.id]||{}; const l=String(m.bcs||'').split(/[^0-9]+/).filter(Boolean);
    if(!l.includes(z.code)) l.push(z.code); MOD[z.id]=Object.assign({},m,{bcs:l.join(', ')}); });
  if(MJ.alias.length) log({act:'fiche',lib:MJ.alias.length+(MJ.alias.length>1?' codes-barres ajoutés depuis le tableur':' code-barres ajouté depuis le tableur'),
       n:MJ.alias.length,det:MJ.alias.map(z=>({bc:z.code,ref:z.marque+' '+z.nom,champ:'bcs',av:null,ap:z.code}))});
  /* les parfums qui n'existaient pas ici */
  MJ.nouveaux.forEach(o=>{
    const x={id:'a'+Date.now().toString(36)+Math.random().toString(36).slice(2,6),bc:o.bc,nom:o.nom,marque:o.marque,ml:o.ml,
      type:o.type,genre:o.genre,qte:o.qte,pa:o.pa,pvr:o.pvr,pvw:o.pvw,src:'tableur',cree:t};
    AJ.push(x); });
  if(MJ.nouveaux.length) log({act:'creation',lib:MJ.nouveaux.length+(MJ.nouveaux.length>1?' parfums créés depuis le tableur':' parfum créé depuis le tableur'),
       n:MJ.nouveaux.length,det:MJ.nouveaux.map(o=>({bc:o.bc,ref:o.marque+' '+o.nom,av:null,ap:o.qte}))});
  sauveEXT(); sauveMOD(); sauveAJ(); fermeMJ(); render(); majBandeau();
};

function majBandeau(){
  const el=$('extb'); if(!el) return;
  if(!EXT.date){ el.style.display='none'; return; }
  const d=new Date(EXT.date), n=Object.keys(EXT.q).length;
  el.style.display='';
  el.innerHTML=`<span class="mjsrc">stock importé</span>
    <span data-nolang>${(()=>{ const j=d.toLocaleDateString((typeof lgLocale==='function'?lgLocale():'fr-FR'),{timeZone:'America/New_York',day:'numeric',month:'long'}), h=d.toLocaleTimeString('fr-FR',{timeZone:'America/New_York',hour:'2-digit',minute:'2-digit'});
      return L3(`${nf(n)} références mises à jour depuis le tableur le ${j} à ${h}.`,`${nf(n)} references updated from the spreadsheet on ${j} at ${h}.`,`${nf(n)} referencias actualizadas desde la hoja de cálculo el ${j} a las ${h}.`); })()}</span>
    <button class="btn" id="extx" style="margin-left:auto">Revenir au fichier d'origine</button>`;
  $('extx').onclick=()=>{ if(!confirm("Abandonner le stock importé et revenir aux quantités du fichier d'inventaire ?")) return;
    EXT={q:{},date:null,src:''}; sauveEXT(); render(); majBandeau(); };
}
majBandeau();

/* ============ LECTURE D'UNE DESIGNATION ============ */
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
/* Un montant peut s'ecrire 1,151.50 (US) ou 1 151,50 (FR) : le dernier separateur
   rencontre est le decimal, l'autre marque les milliers. Confondre les deux divisait
   les prix par mille sur les factures americaines. */
const nombre=v=>{
  if(v==null) return null;
  let t=String(v).replace(/[$\u00a0\u202f\s]/g,'').replace(/[^0-9.,\-]/g,'');
  if(t===''||t==='-'||t==='.'||t===',') return null;
  const dp=t.lastIndexOf('.'), dv=t.lastIndexOf(',');
  if(dp>=0&&dv>=0){                       // les deux presents
    const dec=Math.max(dp,dv), mil=Math.min(dp,dv);
    t=t.slice(0,mil).replace(/[.,]/g,'')+t.slice(mil+1,dec).replace(/[.,]/g,'')+'.'+t.slice(dec+1);
  } else if(dv>=0){                       // virgule seule
    const ap=t.length-dv-1;
    t = (ap===3 && t.replace(/[^0-9]/g,'').length>3 && (t.match(/,/g)||[]).length>=1 && dv>0 && /^\d{1,3}(,\d{3})+$/.test(t.replace('-','')))
        ? t.replace(/,/g,'') : t.replace(',','.');
  } else if(dp>=0){                       // point seul
    if(/^-?\d{1,3}(\.\d{3})+$/.test(t)) t=t.replace(/\./g,'');
  }
  t=t.replace(/(?!^)-/g,'');
  const n=parseFloat(t); return isNaN(n)?null:n;
};

/* ============ COLLER DES LIGNES DE FACTURE ============ */
function analyse(txt){
  const out=[];
  txt.split(/\r?\n/).forEach(l=>{
    if(!l.trim()) return;
    let ch=l.split(/\t|;|\s{2,}/).map(x=>x.trim()).filter(x=>x!=='');
    if(ch.length<2) return;
    const bcI=ch.findIndex(x=>/^\d{8,14}$/.test(x));
    const bc=bcI>=0?ch[bcI]:'';
    let qte=null; const q=ch[0].match(/^(\d+)\s*x?$/i); if(q) qte=+q[1];
    const txts=ch.map((x,i)=>({x,i})).filter(o=>o.i!==bcI&&/[A-Za-zÀ-ÿ]{3}/.test(o.x));
    if(!txts.length) return;
    txts.sort((a,b)=>b.x.length-a.x.length);
    const des=txts[0].x;
    const brand=txts.length>1?txts[1].x:'';
    const nums=ch.map((x,i)=>({v:nombre(x),i})).filter(o=>o.v!=null&&o.i!==bcI&&o.i!==0&&o.i!==txts[0].i);
    // le prix unitaire est celui dont quantite x prix = un autre nombre de la ligne (le total)
    let pa=null; const nn=nums.map(o=>o.v);
    if(qte>0){
      for(const p of nn){
        if(p<=0||p>3000) continue;
        if(nn.some(t=>t!==p && Math.abs(t-qte*p)<=Math.max(0.6,qte*p*0.003))){ pa=p; break; }
      }
    }
    if(pa==null){ const c=nn.filter(v=>v>0.5&&v<3000&&v!==999);
      pa=c.length>1?c[c.length-2]:(c.length?c[0]:null); }
    const d=litDesignation(des);
    let nom=des.replace(/\s*\(\d+\)\s*/,' ').replace(/\s*-\s*[A-Za-z. ]+\s*-\s*\d+pcs ByBox\s*$/i,'')
              .replace(/\s*-\s*(Emirates|France|Spain|Italy|USA|Switzerland|United Arab Emir\.?)\s*$/i,'')
              .replace(/\s{2,}/g,' ').trim();
    if(brand){ const bw=brand.split(/\s+/);
      let i=0,nw=nom.split(/\s+/);
      const nz=x=>x.toLowerCase().replace(/[^a-z0-9]/g,'');
      const bset=new Set(bw.map(nz));
      while(i<nw.length-1 && (nz(nw[i])===nz(bw[i]||'') || bset.has(nz(nw[i])))) i++;
      if(i) nom=nw.slice(i).join(' ');
    }
    nom=nom.replace(/\s+\d+(?:[.,]\d+)?\s*(?:oz|ml)?\s*(?:EDP|EDT|EDC)?\s*[MLUW]?\s*$/i,'').trim();
    nom=nom.replace(/\s+(EDP|EDT|EDC)\s*[MLUW]?\s*$/i,'').trim();
    out.push({bc,nom:nom||des,marque:brand,ml:d.ml||'',type:d.type||'',genre:d.genre||'',
              qte:qte??0,pa,pvr:null,pvw:null,brut:l});
  });
  return out;
}
function apercu(rows,cible){
  const el=$(cible);
  if(!rows.length){ el.style.display='none'; return; }
  const v=x=>(x==null||x===''?'<span class="vide">à compléter</span>':x);
  el.innerHTML=`<table><thead><tr><th>Marque</th><th>Nom</th><th>Cont.</th><th>Type</th><th>Genre</th>
    <th>Code-barres</th><th class="n">Qté</th><th class="n">Achat</th></tr></thead><tbody>`+
    rows.map(r=>`<tr><td>${v(r.marque)}</td><td>${v(r.nom)}</td><td>${v(r.ml)}</td><td>${v(r.type)}</td>
      <td>${v(r.genre)}</td><td>${v(r.bc)}</td><td class="n">${r.qte??0}</td>
      <td class="n">${r.pa==null?'<span class="vide">?</span>':r.pa}</td></tr>`).join('')+'</tbody></table>';
  el.style.display='block';
}
$('an').onclick=()=>{
  PARSED=analyse($('ta').value);
  apercu(PARSED,'pv');
  msg(PARSED.length?`${PARSED.length} ligne${PARSED.length>1?'s':''} reconnue${PARSED.length>1?'s':''} — vérifie l'aperçu avant d'ajouter`:'Aucune ligne reconnue.',PARSED.length?'ok':'err');
  $('mo').textContent=`Ajouter ${PARSED.length} article${PARSED.length>1?'s':''}`;
};

/* ============ IMPORT CSV ============ */
const ALIAS={bc:['code-barres','code barre','barcode','ean','upc','gtin','sku','a_barcode'],
 nom:['nom','name','produit','designation','désignation','article','b_nom'],
 marque:['marque','brand','brands','d_marque'],ml:['contenance','taille','size','oz','ml','c_contenance'],
 type:['type','concentration','e_type'],genre:['genre','gender','sexe','f_genre'],
 qte:['quantite','quantité','qte','qty','stock','g_qte'],
 pa:["prix d'achat",'prix achat','achat','cost','h_prix_achat'],
 pvr:['pvr','retail','prix retail','prix de vente','j_pvr'],
 pvw:['pvw','gros','wholesale','prix de gros','k_pvw']};
function csvLignes(t){
  const L=[];let c='',r=[],q=false;
  for(let i=0;i<t.length;i++){const ch=t[i];
    if(q){ if(ch==='"'){ if(t[i+1]==='"'){c+='"';i++;} else q=false; } else c+=ch; }
    else if(ch==='"') q=true;
    else if(ch===','||ch===';'||ch==='\t'){ r.push(c);c=''; }
    else if(ch==='\n'){ r.push(c);L.push(r);r=[];c=''; }
    else if(ch!=='\r') c+=ch; }
  if(c||r.length){ r.push(c); L.push(r); }
  return L.filter(x=>x.some(y=>y.trim()!==''));
}
$('fi').onchange=e=>{
  const f=e.target.files[0]; if(!f) return;
  lireFichier(f, m=>msg(m,'')).then(texte=>{
    const L=csvLignes(texte); if(L.length<2){ msg('Fichier vide ou illisible.','err'); return; }
    const head=L[0].map(h=>h.trim().toLowerCase());
    const map={};
    Object.entries(ALIAS).forEach(([k,al])=>{
      const i=head.findIndex(h=>al.some(a=>h===a||h.includes(a))); if(i>=0) map[k]=i; });
    if(map.nom==null&&map.marque==null){ msg("Aucune colonne « nom » ou « marque » trouvée.",'err'); return; }
    PARSED=L.slice(1).map(r=>{
      const g=k=>map[k]!=null?(r[map[k]]||'').trim():'';
      const d=litDesignation(g('nom'));
      return {bc:g('bc'),nom:g('nom'),marque:g('marque'),ml:g('ml')||d.ml||'',
        type:(g('type')||d.type||'').toUpperCase(),genre:(g('genre')||d.genre||'').toUpperCase(),
        qte:nombre(g('qte'))??0,pa:nombre(g('pa')),pvr:nombre(g('pvr')),pvw:nombre(g('pvw'))};
    }).filter(x=>x.nom||x.marque);
    apercu(PARSED,'pv2');
    msg(`${PARSED.length} ligne${PARSED.length>1?'s':''} lue${PARSED.length>1?'s':''} — vérifie l'aperçu`,'ok');
    $('mo').textContent=`Ajouter ${PARSED.length} article${PARSED.length>1?'s':''}`;
  }).catch(err=>msg(err.message||'Lecture impossible.','err'));
};

/* ============ ENREGISTREMENT ============ */
$('mo').onclick=()=>{
  const pane=document.querySelector('.tab.on').dataset.p;
  let lot=[];
  if(pane==='man'){
    const g=i=>$('f-'+i).value.trim();
    if(!g('marque')||!g('nom')){ msg('La marque et le nom sont obligatoires.','err'); return; }
    lot=[{bc:g('bc'),nom:g('nom'),marque:g('marque'),ml:g('ml'),type:g('type'),genre:g('genre'),
          qte:nombre(g('qte'))??0,pa:nombre(g('pa')),pvr:nombre(g('pvr')),pvw:nombre(g('pvw'))}];
  } else {
    if(!PARSED.length){ msg("Rien à ajouter — analyse d'abord les lignes.",'err'); return; }
    lot=PARSED;
  }
  const dejaLa=new Set(tousLesArticles().map(p=>p.bc).filter(Boolean));
  let doubl=0;
  /* identifiant stable : avant, les articles étaient insérés en tête et numérotés par position,
     et chaque nouvel article décalait les précédents (leurs corrections, leurs ventes). */
  lot.forEach(x=>{ if(x.bc&&dejaLa.has(x.bc)) doubl++; else { x.id='a'+Date.now().toString(36)+Math.random().toString(36).slice(2,6); AJ.push(x); } });
  sauveAJ(); PARSED=[]; $('ta').value=''; $('fi').value='';
  $('pv').style.display='none'; $('pv2').style.display='none';
  CHAMPS.forEach(k=>{ const el=$('f-'+k); if(el) el.value=''; });
  ferme(); $('fx').value='neuf'; remplitMarques(); render();
  const n=lot.length-doubl;
  if(n===0){ alert(`Aucun article ajouté.\n\nLes ${doubl} ligne${doubl>1?'s':''} correspondent à des codes-barres déjà présents dans le catalogue — ce sont des références que tu as déjà.`); return; }
  alert(`${n} article${n>1?'s':''} ajouté${n>1?'s':''}.`+
    (doubl?`\n${doubl} ignoré${doubl>1?'s':''} : code-barres déjà présent dans le catalogue.`:'')+
    `\n\nIls apparaissent avec une bordure violette et l'étiquette « nouveau ».\nPense à les exporter pour les intégrer au fichier maître.`);
  /* Igal, 18 oct. 2026 : « quand tu crées un produit, est-ce qu'on peut intégrer une photo ou en chercher une ? » — UN article saisi à
     la main : sa fiche s'ouvre tout de suite, et s'il n'a pas de photo, la recherche sur Internet se lance (un clic pour choisir). */
  if(pane==='man'&&n===1){ const x=lot.find(z=>z.id); if(x){ let i=cur.findIndex(p=>p.id===x.id);
    if(i<0&&$('fs').value==='in'){ $('fs').value=''; render(); i=cur.findIndex(p=>p.id===x.id); }   /* un article créé à 0 en stock était caché par « En stock » */
    if(i>=0){ ouvreFiche(x.id);
    setTimeout(()=>{ const b=photoDeFiche(); if(b&&b.id===x.id&&!b.img&&typeof ckTok==='function'&&ckTok()) photoDuWeb(); },400); }
    /* 20 oct. 2026 (Igal) : le produit est mis sur tous les canaux tout de suite, sans repasser par la fiche */
    /* …mais APRÈS la recherche de photo si elle est ouverte : la photo choisie part alors avec le produit, et les deux fenêtres ne se marchent pas dessus */
    const attends=()=>{ if(document.getElementById('pw-ov')) { setTimeout(attends,600); return; } enLigneAuto(x.id); };
    if((+x.pvr>0)||(+x.pvw>0)) setTimeout(attends,900); } }   /* sans aucun prix saisi, rien à mettre en ligne : l'article reste « à compléter » */
};

/* ============ EXPORT DES AJOUTS ============ */
function exporteAjouts(){
  const nm=Object.keys(MOD).length;
  if(!AJ.length&&!nm){ alert("Aucun ajout ni modification pour l'instant."); return; }
  const q=s=>`"${String(s??'').replace(/"/g,'""')}"`;
  const li=['origine;champs_modifies;code_barres;nom;marque;contenance;type;genre;quantite;prix_achat;prix_retail;prix_gros;verification;fournisseurs;prix_par_canal;detail_avant_apres'];
  const nomCanal=k=>{ const c=canaux().find(x=>x.id===k); return c?c.nom:k; };
  const pcs=o=>[...Object.entries(o.pc||{}).filter(([k,v])=>v!=null).map(([k,v])=>nomCanal(k)+' @ '+v),
                ...((o.pcOff||[]).map(k=>nomCanal(k)+' : pas vendu'))].join(' | ');
  const frn=o=>(o.frn||[]).filter(f=>f.n).map(f=>f.n+(f.p!=null?' @ '+f.p:'')).join(' | ');
  const LIB={bc:'code-barres',nom:'nom',marque:'marque',ml:'contenance',type:'type',genre:'genre',
             qte:'quantité',pa:"prix d'achat",pvr:'prix retail',pvw:'prix de gros',verif:'vérification'};
  const VER={ok:'vérifié',non:'jamais compté',av:'à vérifier'};
  AJ.forEach((a,i)=>{const m=MOD[a.id||('a'+i)]||{}; const v=Object.assign({},a,m);
    li.push(['ajout','"créé à la main"',q(v.bc),q(v.nom),q(v.marque),q(v.ml),q(v.type),q(v.genre),
      v.qte??0,v.pa??'',v.pvr??'',v.pvw??'',q(VER[v.verif]||''),q(frn(m)),q(pcs(m)),'""'].join(';'));});
  P.forEach(p=>{const m=MOD[p.id]; if(!m) return; const v=Object.assign({},p,m);
    /* on liste les champs reellement touches, et l'avant -> apres de chacun :
       sans ca, il faut comparer ligne a ligne pour retrouver ce qui a bouge */
    const ch=Object.keys(m).filter(k=>k in LIB && (p[k]??'')!==(m[k]??''));
    const det=ch.map(k=>{
      const av = k==='verif' ? (VER[p[k]]||'inconnu') : (p[k]??'—');
      const ap = k==='verif' ? (VER[m[k]]||'inconnu') : (m[k]??'—');
      return `${LIB[k]} : ${av} -> ${ap}`;}).join(' | ');
    const noms=ch.map(k=>LIB[k]);
    if(JSON.stringify((MOD[p.id]||{}).frn||[])!=='[]') noms.push('fournisseurs');
    if(pcs(m)) noms.push('prix par canal');
    li.push(['modification',q(noms.join(', ')),q(v.bc),q(v.nom),q(v.marque),q(v.ml),q(v.type),q(v.genre),
      v.qte??0,v.pa??'',v.pvr??'',v.pvw??'',q(VER[v.verif]||''),q(frn(m)),q(pcs(m)),q(det)].join(';'));});
  const el=document.createElement('a');
  el.href=URL.createObjectURL(new Blob(['﻿'+li.join('\n')],{type:'text/csv;charset=utf-8'}));
  el.download=`mes_corrections_${ajd()}.csv`;
  el.click(); URL.revokeObjectURL(el.href);
}

/* ============ NOUVELLES RÉFÉRENCES POUR LIGHTSPEED (3 oct. 2026) ============
   Sam, point 8 : « dans l'inventaire que j'envoie à Lightspeed, s'il y a une nouvelle
   référence, les infos rentrées dans l'ERP seront-elles prises en compte ? » Non : le
   fichier d'inventaire ne fait que changer des quantités, et ignore un code inconnu.
   Ce fichier-ci est l'import PRODUITS de Lightspeed (X-Series), mêmes colonnes que son
   export : il crée les fiches. On compare à la liste des produits de la caisse que le
   cockpit tient à jour (caisse-produits-v1, nourrie par le zap « produits »).
   Ce qui est douteux reste HORS du fichier et s'affiche à part :
     - un code-barres retrouvé DANS un SKU de la caisse (« …NOBOX », préfixe) : le
       produit existe peut-être déjà, c'est à Sam de trancher ;
     - pas de code-barres : impossible de savoir s'il existe déjà ;
     - pas de prix détail : il passerait à 0 $ à la caisse. */
const LS_COLS=['id','handle','sku','composite_name','composite_sku','composite_quantity','name','description','product_category','variant_option_one_name','variant_option_one_value','variant_option_two_name','variant_option_two_value','variant_option_three_name','variant_option_three_value','tags','active_online','weight','weight_unit','length','width','height','dimensions_unit','supply_price','retail_price','account_code','account_code_purchase','brand_name','supplier_name','supplier_code','active','track_inventory','outlet_tax_Main_Outlet','inventory_Main_Outlet','reorder_point_Main_Outlet','reorder_quantity_Main_Outlet','min_quantity_Main_Outlet','max_quantity_Main_Outlet','items_on_special_order_Main_Outlet'];
let LSNV=null;
const lsNorm=s=>String(s||'').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g,'').replace(/[^a-z0-9.]+/g,' ').trim();
/* le nom à la façon de la caisse : « Bois d'Iris by Geparlys - EDP - 3.4 oz » */
function lsNom(a){
  const n=String(a.nom||'').trim(), m=String(a.marque||'').trim(), t=String(a.type||'').trim(), ml=String(a.ml||'').trim();
  const nn=' '+lsNorm(n)+' ';
  let s=n;
  if(m && nn.indexOf(' '+lsNorm(m)+' ')<0) s+=' by '+m;
  if(t && nn.indexOf(' '+lsNorm(t)+' ')<0) s+=' - '+t;
  if(ml && nn.indexOf(' '+lsNorm(ml)+' ')<0) s+=' - '+ml+(parseFloat(ml)>20?' ml':' oz');
  return s.replace(/\s+/g,' ').trim();
}
/* range chaque parfum de l'ERP : connu de la caisse, nouveau, ou à vérifier */
function lsTrie(V,tous){
  const codes=new Set(), skus=[], skuSet=new Set(), parSku={};
  Object.values(V||{}).forEach(p=>{ if(!p) return;
    if(p.bc) codes.add(String(p.bc).replace(/^0+/,''));
    const k=String(p.sku||'').toUpperCase().replace(/[^A-Z0-9]/g,'');
    if(k){ skus.push(k); skuSet.add(k); skuSet.add(k.replace(/^0+/,'')); parSku[k]=p; } });
  const out={neufs:[],verif:[],connus:0};
  tousLesArticles().forEach(a=>{
    const q=+a.qte||0;
    const brut=String(a.bc||'').toUpperCase().replace(/[^A-Z0-9]/g,'');
    const ks=cleCodes(a.bc).filter(k=>!k.startsWith('T:')), ex=bcsDe(a);
    if(brut&&(skuSet.has(brut)||skuSet.has(brut.replace(/^0+/,'')))){ out.connus++; return; }
    if([...ks,...ex].some(k=>codes.has(k)||skuSet.has(k))){ out.connus++; return; }
    if(!tous&&q<=0) return;
    if(!brut){ out.verif.push({a,why:'pas de code-barres'}); return; }
    const pres=ks.filter(k=>k.length>=8).map(k=>skus.find(s=>s!==k&&s.indexOf(k)>=0)).find(Boolean);
    if(pres){ out.verif.push({a,why:'code-barres déjà dans un SKU de la caisse',ls:pres+' — '+((parSku[pres]||{}).nom||'')}); return; }
    /* un vrai code-barres = 8 à 14 chiffres. Deux codes collés (« 783320427152783320413698 »),
       un nom (« Cloudnobox1oz ») ou une mention (« …tester ») feraient une fiche que la
       caisse ne retrouvera jamais au scanner : on les montre, on ne les crée pas. */
    if(!/^\d{8,14}$/.test(brut)){ out.verif.push({a,why:'code-barres à corriger : pas 8 à 14 chiffres'}); return; }
    if(a.pvr==null||!(+a.pvr>0)){ out.verif.push({a,why:'pas de prix détail'}); return; }
    out.neufs.push(a);
  });
  const tri=(x,y)=>String(x.marque||'').localeCompare(String(y.marque||''),'fr')||String(x.nom||'').localeCompare(String(y.nom||''),'fr');
  out.neufs.sort(tri); out.verif.sort((x,y)=>tri(x.a,y.a));
  return out;
}
function lsLigne(a){
  const code=String(a.bc||'').toUpperCase().replace(/[^A-Z0-9]/g,'');
  const o={handle:code,sku:code,name:lsNom(a),active_online:'0',
    variant_option_one_name:a.type?'type':'',variant_option_one_value:a.type||'',
    variant_option_two_name:a.ml?'content':'',variant_option_two_value:a.ml||'',
    supply_price:a.pa!=null?String(+a.pa):'',retail_price:(+a.pvr).toFixed(2),
    brand_name:a.marque||'',active:'1',track_inventory:'1',outlet_tax_Main_Outlet:'Default Tax',
    inventory_Main_Outlet:String(Math.max(0,Math.round(+a.qte||0))),items_on_special_order_Main_Outlet:'0'};
  const q=v=>{ v=String(v==null?'':v); return /[",\n\r]/.test(v)?'"'+v.replace(/"/g,'""')+'"':v; };
  return LS_COLS.map(c=>q(o[c]||'')).join(',');
}
function lsPeint(){
  const R=LSNV; if(!R) return;
  const tous=!!($('lstous')&&$('lstous').checked);
  const T=lsTrie(R.V,tous); R.T=T;
  const m=R.maj?new Date(R.maj):null;
  const d=m&&!isNaN(m)?m.toLocaleDateString('fr-FR')+' '+m.toLocaleTimeString('fr-FR',{hour:'2-digit',minute:'2-digit'}):'';
  const ligne=a=>`<tr><td data-nolang>${esc(a.bc||'—')}</td><td data-nolang>${esc(lsNom(a))}</td><td class="num">${+a.qte||0}</td><td class="num" data-nolang>${a.pa!=null?money(+a.pa):'—'}</td><td class="num" data-nolang>${a.pvr!=null?money(+a.pvr):'—'}</td></tr>`;
  let h=`<div class="lsnv-tete"><b>${T.neufs.length} parfum${T.neufs.length>1?'s':''} à créer dans la caisse</b></div>`;
  h+=`<p class="hint">Comparé aux ${R.n} produits que la caisse connaît${d?` (mis à jour le ${d})`:''}.</p>`;
  h+=`<label class="lsnv-case"><input type="checkbox" id="lstous"${tous?' checked':''}> <span>Ajouter aussi ceux à 0 en stock</span></label>`;
  if(T.neufs.length){
    h+=`<div class="prev lsnv-tab"><table><thead><tr><th>Code-barres</th><th>Nom dans la caisse</th><th class="num">Qté</th><th class="num">Achat</th><th class="num">Détail</th></tr></thead><tbody>`
      +T.neufs.slice(0,200).map(ligne).join('')+`</tbody></table></div>`;
    if(T.neufs.length>200) h+=`<p class="hint">Les ${T.neufs.length-200} autres sont dans le fichier.</p>`;
  } else h+=`<p class="hint">Rien à créer : la caisse connaît déjà tous ces parfums.</p>`;
  if(T.verif.length){
    h+=`<div class="lsnv-tete lsnv-av"><b>À vérifier avant : ${T.verif.length} hors du fichier</b></div>`
      +`<div class="prev lsnv-tab"><table><tbody>`+T.verif.map(x=>`<tr><td data-nolang>${esc(x.a.bc||'—')}</td><td data-nolang>${esc(lsNom(x.a))}${x.ls?`<br><small><span>Dans la caisse :</span> <span data-nolang>${esc(x.ls)}</span></small>`:''}</td><td class="num">${+x.a.qte||0}</td><td class="lsnv-why">${esc(x.why)}</td></tr>`).join('')+`</tbody></table></div>`;
  }
  $('lsres').innerHTML=h;
  $('lstous').onchange=lsPeint;
  $('lsok').disabled=!T.neufs.length;
}
async function lsOuvre(){
  LSNV=null; $('lsres').innerHTML='<p class="hint">Lecture des produits de la caisse…</p>';
  $('lsok').disabled=true; $('lsmsg').textContent=''; $('lsmsg').className='msg';
  $('lsov').classList.add('on');
  if(!(typeof CK_URL!=='undefined'&&typeof ckTok==='function'&&ckTok())){
    $('lsres').innerHTML='<p class="hint">Il faut ouvrir l\'ERP en ligne : la liste des produits de la caisse est sur le serveur.</p>'; return; }
  try{
    const r=await fetch(CK_URL+'/api/o/'+CK_ORG+'/donnees/caisse-produits-v1',{headers:{Authorization:'Bearer '+ckTok()},cache:'no-store'});
    if(r.status===404) throw new Error('vide');
    if(!r.ok) throw new Error('serveur '+r.status);
    const j=await r.json(); const V=(j&&j.val&&typeof j.val==='object')?j.val:{};
    const n=Object.keys(V).length; if(!n) throw new Error('vide');
    LSNV={V,n,maj:j.maj||''}; lsPeint();
  }catch(e){
    $('lsres').innerHTML=(e&&e.message==='vide')
      ?'<p class="hint">Le serveur ne connaît pas encore les produits de la caisse : sans eux, impossible de savoir lesquels sont nouveaux.</p>'
      :'<p class="hint">Le serveur ne répond pas. Réessaie dans un instant.</p>';
  }
}
function lsTelecharge(){
  const T=LSNV&&LSNV.T; if(!T||!T.neufs.length) return;
  const li=[LS_COLS.join(',')].concat(T.neufs.map(lsLigne));
  const el=document.createElement('a');
  el.href=URL.createObjectURL(new Blob(['﻿'+li.join('\r\n')],{type:'text/csv;charset=utf-8'}));
  el.download=`lightspeed_nouvelles_references_${ajd()}.csv`;
  document.body.appendChild(el); el.click(); el.remove(); setTimeout(()=>URL.revokeObjectURL(el.href),1000);
  const m=$('lsmsg'); m.textContent=`Fichier prêt : ${T.neufs.length} parfum${T.neufs.length>1?'s':''}.`; m.className='msg ok';
}
function lsFerme(){ $('lsov').classList.remove('on'); }
$('lsnv').onclick=lsOuvre; $('lsx').onclick=lsFerme; $('lsannul').onclick=lsFerme; $('lsok').onclick=lsTelecharge;

/* ============ METTRE À JOUR LIGHTSPEED (Igal, 8 nov. 2026) ============
   « En un clic, transférer le fichier Wholesale et le fichier Retail sur Lightspeed pour mettre à niveau les prix, avec un
   formulaire déjà pré-rempli par l'ERP. » Lightspeed (forfait de Sam) n'ouvre aucune porte automatique : il ne met à jour que ce
   qu'il reconnaît dans SON export, par son identifiant. Donc :
     1. l'export des produits de la caisse (Catalogue → Produits → Exporter la liste → CSV) est déposé ici — le cockpit le garde
        (lightspeed-export-v1), sans les colonnes de stock ;
     2. chaque produit de la caisse est rapproché d'une fiche du Catalogue par son code-barres (trouve : codes, « nobox »,
        autres codes) ou par une équivalence confirmée à la main (lightspeed-paires-v1 : sku → clé, ou « - » = pas dans l'ERP) ;
        les non-reconnus sont listés avec une fiche probable à confirmer d'un clic ;
     3. « Préparer les fichiers » fabrique le fichier RETAIL (seulement les lignes dont le prix change ; TOUTES les colonnes de
        l'export sauf le stock, telles quelles, retail_price remplacé par celui du Catalogue) et le fichier WHOLESALE
        (au format de l'export d'un catalogue de prix : sku, handle, id, retail_price…, prix de gros du Catalogue).

   « On n'a pas le droit à l'erreur » (Igal, 8 nov. 2026). Les garde-fous :
     • un prix qui change de plus du double ou de moins de la moitié, ou qui dépasse 5 000 $, n'est PAS envoyé : il est listé
       « à vérifier » (le premier essai portait deux miniatures Burberry à 45 416 $, un 17,50 $ passé à 185 $) ;
     • un prix de gros AU-DESSUS du prix retail n'est pas envoyé non plus (liste « à vérifier ») ;
     • le fichier Retail reprend l'export TEL QUEL (sauf le stock) : essai du 8 nov. 2026 dans Lightspeed, un fichier réduit à
       id/nom/prix est refusé sans SKU, et sans « supply_price » Lightspeed annonce qu'il mettra le prix d'achat à 0 $. C'est la
       méthode de l'aide Lightspeed (exporter, retirer le stock, changer, réimporter) ; comme l'export doit être frais (ci-dessous),
       il ne remet aucune ancienne valeur ;
     • Lightspeed CRÉE UN DOUBLON dans un catalogue de prix pour toute ligne sans l'identifiant de la ligne existante (aide
       Lightspeed, « Updating a price book »). Une fois des prix de gros envoyés, le fichier Wholesale n'est plus fabriqué
       sans un export du catalogue wholesale déposé APRÈS : il donne l'identifiant de chaque ligne ; une ligne au même prix
       n'est pas renvoyée ;
     • l'export des produits doit dater de moins de 24 h et être plus récent que les derniers fichiers préparés. */
const K_LSM_P='lightspeed-paires-v1', K_LSM_E='lightspeed-envoye-v1', K_LSM_T='lightspeed-tarif-wholesale-v1';
const LSM_FRAIS=24*3600e3, LSM_MAX=5000;
const LSM_STOCK=/^(inventory|reorder_point|reorder_quantity|min_quantity|max_quantity|items_on_special_order)_/;
const LSM_ENTETE_W='sku,handle,id,retail_price,loyalty_value,min_units,max_units';
let LSM=null, LSM_RETOUR=null;
/* la clé d'une fiche : `cle` quand elle en a une, sinon son identifiant (31 fiches créées dans l'ERP n'ont pas de `cle` : avec
   elle seule, « Même parfum » ne faisait rien sur elles — Igal, 8 nov. 2026, Ariana Grande Cloud no box) */
const lsmCle=a=>String((a&&(a.cle||a.id))||'');
const lsmT=(a,b,c)=>(typeof L3==='function'?L3(a,b,c):a);
const lsmQ=v=>{ v=String(v==null?'':v); return /[",\n\r]/.test(v)?'"'+v.replace(/"/g,'""')+'"':v; };
const lsmPaires=()=>{ const P=lit(K_LSM_P,{}); return (P&&typeof P==='object'&&!Array.isArray(P))?P:{}; };
const lsmTarif=()=>{ const T=lit(K_LSM_T,null); return (T&&typeof T==='object'&&T.par&&typeof T.par==='object')?T:null; };
/* quand des fichiers ont été préparés pour la dernière fois : retail (tR) et wholesale (tW), séparément */
const lsmEnvoi=()=>{ const E=lit(K_LSM_E,null); if(!E||typeof E!=='object') return {tR:0,tW:0,E:null};
  const t=Date.parse(E.t||'')||0; return {E, tR:Date.parse(E.tR||'')||(E.retail>0?t:0), tW:Date.parse(E.tW||'')||(E.gros>0?t:0)}; };
const lsmTok=s=>{ const t=String(s||'').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g,'').replace(/[^a-z0-9 ]+/g,' ').split(' ');
  const STOP=new Set('by the de du des la le les pour for eau edp edt edc parfum toilette cologne spray oz ml men homme women femme unisex tester no box nobox new set gift coffret and'.split(' '));
  return new Set(t.filter(x=>x.length>1&&!STOP.has(x))); };
function lsmSuggere(nom,arts){
  const ta=lsmTok(nom); if(ta.size<2) return [];
  const out=[];
  for(const a of arts){ const te=a._tok||(a._tok=lsmTok((a.marque||'')+' '+(a.nom||'')+' '+(a.nomSrc||''))); if(!te.size) continue;
    let n=0; ta.forEach(x=>{ if(te.has(x)) n++; }); if(n<2||n/ta.size<0.6||n/te.size<0.6) continue;
    out.push({s:n/Math.max(ta.size,te.size),a}); }
  return out.sort((x,y)=>y.s-x.s).slice(0,3);
}
/* la même recherche que trouve(), mais avec un index construit une fois (2 660 produits × 3 800 fiches : trouve() relit tout à chaque appel) */
function lsmIndex(arts){
  const I={}; const pose=(k,a)=>{ if(!k) return; (I[k]=I[k]||[]).push(a); };
  const EX=(typeof bcExtra==='function')?bcExtra():{};
  arts.forEach(a=>{ if(a.bc) pose(String(a.bc).replace(/[^0-9]/g,'').replace(/^0+/,''),a); bcsDe(a).forEach(k=>pose(k,a)); (EX[a.cle]||[]).forEach(k=>pose(String(k).replace(/^0+/,''),a)); });
  return I;
}
function lsmTrouve(I,sku){
  const M=(typeof mentionBC==='function')?mentionBC(sku):{digits:String(sku).replace(/[^0-9]/g,''),mention:''};
  const nu=String(M.digits||'').replace(/^0+/,''); if(!nu) return null;
  const C=I[nu]||[]; if(!C.length) return null;
  if(typeof parMention==='function') return parMention(C,M.mention,x=>String(x.bc||'').replace(/[0-9]/g,'')+' '+x.nom+' '+(x.nomSrc||''))||null;
  return M.mention?null:C[0];
}
/* rapproche chaque produit de la caisse d'une fiche : par équivalence confirmée, sinon par code-barres ; puis les garde-fous */
function lsmCalc(){
  const X=LSM&&LSM.X; if(!X) return;
  const arts=tousLesArticles(), parCle={}; arts.forEach(a=>{ const k=lsmCle(a); if(k) parCle[k]=a; }); LSM.parCle=parCle;
  const I=lsmIndex(arts);
  const P=lsmPaires(), T=lsmTarif(), TP=(T&&T.par)||{};
  const rec=[], inc=[], dout=[]; let retail=0, gros=0, ignores=0, memes=0;
  (X.lignes||[]).forEach(r=>{
    const sku=String(r.sku||'').trim(); if(!sku) return;
    if(String(r.composite_sku||'').trim()||String(r.composite_name||'').trim()){ ignores++; return; }   /* un lot : réglé à la main */
    let a=null; const pa=P[sku];
    if(pa==='-'){ ignores++; return; }
    if(pa&&parCle[pa]) a=parCle[pa]; else { try{ a=lsmTrouve(I,sku); }catch(e){ a=null; } }
    if(!a){ inc.push({r,sug:lsmSuggere(r.name,arts)}); return; }
    const pvr=a.pvr!=null&&a.pvr!==''?+a.pvr:null, pvw=a.pvw!=null&&a.pvw!==''?+a.pvw:null;
    const ancien=+r.retail_price||0;
    let chR=pvr>0&&Math.abs(pvr-ancien)>0.005;
    if(chR){ const k=ancien>0?pvr/ancien:1;
      if(pvr>=LSM_MAX||k>2||k<0.5){ dout.push({r,a,quoi:'retail',de:ancien,vers:pvr}); chR=false; } }
    const fin=chR?pvr:ancien;
    let w=null;
    if(pvw>0){
      if(pvw>=LSM_MAX||(fin>0&&pvw>fin+0.005)) dout.push({r,a,quoi:'gros',de:fin,vers:pvw});
      else { const t=TP[sku]; if(t&&Math.abs((+t.p||0)-pvw)<=0.005) memes++; else w={id:t?t.id:'',t:t||null}; } }
    if(chR) retail++; if(w) gros++;
    rec.push({r,a,pvr,pvw,chR,w});
  });
  const now=Date.now(), V=lsmEnvoi(), tX=Date.parse(X.t||'')||0, tT=T?(Date.parse(T.t||'')||0):0, bloque={};
  if(now-tX>LSM_FRAIS||(V.tR&&tX<=V.tR)) bloque.retail='vieux';
  if(V.tW&&(!tT||tT<=V.tW)) bloque.gros='tarif';
  else if(tT&&now-tT>LSM_FRAIS) bloque.gros='tarifVieux';
  LSM.rec=rec; LSM.inc=inc; LSM.dout=dout; LSM.bloque=bloque; LSM.T=T; LSM.n={retail,gros,ignores,memes};
}
function lsmPeint(){
  const z=$('lsmcorps'); if(!LSM){ z.innerHTML=''; return; }
  const X=LSM.X; let h='';
  const depot=`<label class="lsm-depot">${lsmT('Déposer les exports de Lightspeed (les produits, et le catalogue de prix wholesale) :','Drop the Lightspeed exports (products, and the wholesale price book):','Dejar las exportaciones de Lightspeed (los productos y el catálogo de precios wholesale):')} <input type="file" id="lsm-fic" accept=".csv,text/csv" multiple></label>`;
  if(!X){ h+=`<div class="lsm-etat"><b>${lsmT("Pas encore d'export de la caisse.","No register export yet.","Todavía no hay exportación de la caja.")}</b> <span>${lsmT("Il faut d'abord déposer l'export des produits de Lightspeed : c'est lui qui porte les identifiants que Lightspeed reconnaît.","First drop Lightspeed's product export: it carries the identifiers Lightspeed recognizes.","Primero hay que dejar la exportación de productos de Lightspeed: lleva los identificadores que Lightspeed reconoce.")}</span></div>${depot}`;
    z.innerHTML=h; lsmBranche(); $('lsmok').disabled=true; return; }
  const quand=t=>{ const d=t?new Date(t):null; return d&&!isNaN(d)?d.toLocaleDateString(typeof lgLocale==='function'?lgLocale():'fr-FR')+' '+d.toLocaleTimeString('fr-FR',{hour:'2-digit',minute:'2-digit'}):''; };
  const T=LSM.T, B=LSM.bloque||{};
  h+=`<div class="lsm-etat"><b>${lsmT('Export de la caisse du','Register export of','Exportación de la caja del')} ${esc(quand(X.t))}</b><span>${nf(X.n||(X.lignes||[]).length)} ${lsmT('produits','products','productos')}</span>`
    +`<span>${T?`${lsmT('Catalogue wholesale exporté le','Wholesale price book exported on','Catálogo wholesale exportado el')} ${esc(quand(T.t))} — ${nf(T.n||0)} ${lsmT('prix','prices','precios')}`:lsmT('Catalogue wholesale : pas encore déposé (normal tant que rien n\'y a été envoyé)','Wholesale price book: not dropped yet (normal while nothing has been sent to it)','Catálogo wholesale: todavía no depositado (normal mientras no se haya enviado nada)')}</span>${depot}</div>`;
  const BL={vieux:lsmT("Fichier RETAIL bloqué : l'export des produits a plus de 24 h, ou des fichiers ont déjà été préparés depuis. Refais l'export (Catalogue → Produits → Exporter la liste) et dépose-le ici.","RETAIL file blocked: the product export is over 24 h old, or files were already prepared since. Export again (Catalog → Products → Export list) and drop it here.","Archivo RETAIL bloqueado: la exportación de productos tiene más de 24 h, o ya se prepararon archivos desde entonces. Vuelve a exportar (Catálogo → Productos → Exportar la lista) y déjala aquí."),
    tarif:lsmT("Fichier WHOLESALE bloqué : des prix de gros ont déjà été envoyés. Dépose d'abord l'export du catalogue wholesale (Catalogue → Catalogues de prix → wholesale → Exporter) : sans lui, Lightspeed créerait des doublons.","WHOLESALE file blocked: wholesale prices were already sent. First drop the wholesale price book export (Catalog → Price books → wholesale → Export): without it, Lightspeed would create duplicates.","Archivo WHOLESALE bloqueado: ya se enviaron precios mayoristas. Primero deja la exportación del catálogo wholesale (Catálogo → Catálogos de precios → wholesale → Exportar): sin ella, Lightspeed crearía duplicados."),
    tarifVieux:lsmT("Fichier WHOLESALE bloqué : l'export du catalogue wholesale a plus de 24 h. Refais-le (Catalogue → Catalogues de prix → wholesale → Exporter).","WHOLESALE file blocked: the wholesale price book export is over 24 h old. Export it again (Catalog → Price books → wholesale → Export).","Archivo WHOLESALE bloqueado: la exportación del catálogo wholesale tiene más de 24 h. Vuelve a hacerla (Catálogo → Catálogos de precios → wholesale → Exportar).")};
  ['retail','gros'].forEach(k=>{ if(B[k]) h+=`<div class="lsm-bloque">${esc(BL[B[k]])}</div>`; });
  const n=LSM.n||{}, rec=LSM.rec||[], inc=LSM.inc||[], dout=LSM.dout||[];
  h+=`<div class="lsm-kpi">
    <div><b>${nf(rec.length)}</b><span>${lsmT('produits de la caisse reconnus dans le Catalogue','register products matched in the Catalog','productos de la caja reconocidos en el Catálogo')}</span></div>
    <div><b>${nf(B.retail?0:(n.retail||0))}</b><span>${lsmT('prix retail à changer dans la caisse','retail prices to change in the register','precios retail a cambiar en la caja')}</span></div>
    <div><b>${nf(B.gros?0:(n.gros||0))}</b><span>${lsmT('prix de gros à envoyer (catalogue wholesale)','wholesale prices to send (wholesale price book)','precios mayoristas a enviar (catálogo wholesale)')}${n.memes?` · ${nf(n.memes)} ${lsmT('déjà au bon prix','already right','ya correctos')}`:''}</span></div>
    <div><b>${nf(dout.length)}</b><span>${lsmT('prix à vérifier — pas envoyés','prices to check — not sent','precios a verificar — no enviados')}</span></div>
    <div><b>${nf(inc.length)}</b><span>${lsmT('non reconnus — à confirmer ci-dessous','not matched — confirm below','no reconocidos — confirmar abajo')}${n.ignores?` · ${nf(n.ignores)} ${lsmT('ignorés','ignored','ignorados')}`:''}</span></div></div>`;
  if(dout.length){
    h+=`<div class="lsnv-tete"><b>${lsmT('Prix à vérifier dans le Catalogue','Prices to check in the Catalog','Precios a verificar en el Catálogo')}</b> — ${lsmT("l'écart est trop grand pour être envoyé les yeux fermés. Corrige la fiche si elle est fausse : la prochaine fois, le prix partira.","the gap is too big to send blindly. Fix the item if it is wrong: next time, the price will go.","la diferencia es demasiado grande para enviarla a ciegas. Corrige la ficha si está mal: la próxima vez, el precio saldrá.")}</div>`;
    h+=`<div class="prev lsnv-tab lsm-tab" style="max-height:260px"><table><thead><tr><th>${lsmT('Produit','Product','Producto')}</th><th>${lsmT('Quoi','What','Qué')}</th><th>${lsmT('Caisse','Register','Caja')}</th><th>ERP</th></tr></thead><tbody>`
      +dout.map(x=>`<tr><td><a href="#" class="lsm-fiche" data-lsmfiche="${esc(x.a.id||'')}" title="${esc(lsmT('Ouvrir la fiche du Catalogue','Open the Catalog item','Abrir la ficha del Catálogo'))}">${esc(x.r.name||'')}</a><br><small>${esc(x.r.sku||'')}</small></td><td>${x.quoi==='retail'?lsmT('prix retail','retail price','precio retail'):lsmT('prix de gros au-dessus du retail','wholesale above retail','mayorista por encima del retail')}</td><td>${money(+x.de||0)}</td><td>${money(+x.vers||0)}</td></tr>`).join('')+`</tbody></table></div>`;
  }
  if(inc.length){
    const avecSug=inc.filter(x=>x.sug.length), sans=inc.filter(x=>!x.sug.length);
    h+=`<div class="lsnv-tete"><b>${lsmT('Non reconnus par le code-barres','Not matched by barcode','No reconocidos por el código de barras')}</b> — ${lsmT("si c'est le même parfum qu'une fiche du Catalogue, confirme : l'ERP s'en souviendra et ses prix suivront.","if it is the same perfume as a Catalog item, confirm: the ERP will remember and its prices will follow.","si es el mismo perfume que una ficha del Catálogo, confirma: el ERP lo recordará y sus precios seguirán.")}</div>`;
    const ligne=x=>{ const sel=x.sug.length?`<select data-lsmsel="${esc(x.r.sku)}">${x.sug.map(s=>`<option value="${esc(lsmCle(s.a))}">${esc((s.a.marque||'')+' '+(s.a.nom||''))}${s.a.pvr!=null?' — '+money(+s.a.pvr):''}</option>`).join('')}</select><button class="btn" data-lsmvoir="${esc(x.r.sku)}">${lsmT('Voir la fiche','See the item','Ver la ficha')}</button><button class="btn" data-lsmoui="${esc(x.r.sku)}">${lsmT('Même parfum','Same perfume','Mismo perfume')}</button>`:`<span class="hint">${lsmT('aucune fiche ressemblante','no similar item','ninguna ficha parecida')}</span>`;
      return `<tr><td>${esc(x.r.sku)}</td><td>${esc(x.r.name||'')}<br><small>${lsmT('prix caisse','register price','precio caja')} ${esc(String(x.r.retail_price||''))} $</small></td><td>${sel}<button class="btn" data-lsmnon="${esc(x.r.sku)}">${lsmT("Pas dans l'ERP","Not in the ERP","No está en el ERP")}</button></td></tr>`; };
    h+=`<div class="prev lsnv-tab lsm-tab" style="max-height:360px"><table><thead><tr><th>SKU ${lsmT('caisse','register','caja')}</th><th>${lsmT('Produit dans la caisse','Product in the register','Producto en la caja')}</th><th>${lsmT('Fiche du Catalogue','Catalog item','Ficha del Catálogo')}</th></tr></thead><tbody>`
      +avecSug.concat(sans).slice(0,150).map(ligne).join('')+`</tbody></table></div>`;
    if(inc.length>150) h+=`<p class="hint">${lsmT(`… et ${inc.length-150} autres, après ceux-ci.`,`… and ${inc.length-150} more, after these.`,`… y ${inc.length-150} más, después de estos.`)}</p>`;
  }
  const E=lsmEnvoi().E;
  if(E&&E.t) h+=`<p class="hint">${lsmT('Derniers fichiers préparés le','Last files prepared on','Últimos archivos preparados el')} ${esc(dateFr(E.t))} — ${nf(E.retail||0)} retail, ${nf(E.gros||0)} wholesale${E.u?' ('+esc(E.u)+')':''}.</p>`;
  h+=`<p class="hint">${lsmT('Ensuite, dans Lightspeed : Catalogue → Produits → Importer → fichier Retail ; Catalogue → Catalogues de prix → wholesale → Modifier → fichier Wholesale → Enregistrer. Seuls les prix changent : ni le stock, ni les noms, ni les taxes.','Then, in Lightspeed: Catalog → Products → Import → Retail file; Catalog → Price books → wholesale → Edit → Wholesale file → Save. Only prices change: not stock, names or taxes.','Luego, en Lightspeed: Catálogo → Productos → Importar → archivo Retail; Catálogo → Catálogos de precios → wholesale → Modificar → archivo Wholesale → Guardar. Solo cambian los precios: ni el stock, ni los nombres, ni los impuestos.')}</p>`;
  z.innerHTML=h; lsmBranche();
  $('lsmok').disabled=!((B.retail?0:(n.retail||0))+(B.gros?0:(n.gros||0)));
}
function lsmBranche(){
  const f=$('lsm-fic'); if(f) f.onchange=()=>{ const fs=f.files?Array.from(f.files):[]; if(fs.length) lsmDepose(fs); };
  document.querySelectorAll('[data-lsmoui]').forEach(b=>b.onclick=()=>{ const sku=b.dataset.lsmoui, sel=document.querySelector(`[data-lsmsel="${CSS.escape(sku)}"]`); if(!sel||!sel.value) return;
    const P=lsmPaires(); P[sku]=sel.value; ecrit(K_LSM_P,P); log({act:'prix',lib:'Lightspeed : « '+sku+' » = fiche '+sel.value+' (même parfum, confirmé)',n:1,impact:0,det:[]}); lsmCalc(); lsmPeint(); });
  document.querySelectorAll('[data-lsmnon]').forEach(b=>b.onclick=()=>{ const sku=b.dataset.lsmnon; const P=lsmPaires(); P[sku]='-'; ecrit(K_LSM_P,P); lsmCalc(); lsmPeint(); });
  document.querySelectorAll('[data-lsmvoir]').forEach(b=>b.onclick=()=>{ const sel=document.querySelector(`[data-lsmsel="${CSS.escape(b.dataset.lsmvoir)}"]`); const a=sel&&LSM&&LSM.parCle&&LSM.parCle[sel.value]; if(a) lsmVoirFiche(a.id); });
  document.querySelectorAll('[data-lsmfiche]').forEach(b=>b.onclick=e=>{ e.preventDefault(); lsmVoirFiche(b.dataset.lsmfiche); });
}
/* Igal, 8 nov. 2026 : « quand on clique sur un produit, la barre latérale s'ouvre pour voir le parfum, sans quitter la page ».
   La fenêtre Lightspeed s'efface le temps de la fiche, et revient telle quelle (recalculée : un prix corrigé dans la fiche compte
   tout de suite) quand la fiche se ferme ; la recherche du Catalogue est remise comme avant. */
function lsmVoirFiche(id){
  if(!id) return;
  LSM_RETOUR={q:$('q').value,fs:$('fs').value};
  $('lsmov').classList.remove('on');
  if(cur.findIndex(x=>x.id===id)<0){ const a=tousLesArticles().find(x=>x.id===id); if(!a){ lsmRetour(); return; } $('fs').value=''; $('q').value=a.bc||a.nom||''; render(); }
  ouvreFiche(id);
}
function lsmRetour(){
  const R=LSM_RETOUR; if(!R) return; LSM_RETOUR=null;
  if($('q').value!==R.q||$('fs').value!==R.fs){ $('q').value=R.q; $('fs').value=R.fs; render(); }
  $('lsmov').classList.add('on'); lsmCalc(); lsmPeint();
}
async function lsmCharge(){
  LSM={X:null};
  if(!(typeof CK_URL!=='undefined'&&typeof ckTok==='function'&&ckTok())){ $('lsmcorps').innerHTML=`<p class="hint">${lsmT("Il faut ouvrir l'ERP en ligne : l'export de la caisse est gardé sur le serveur.","Open the online ERP: the register export is kept on the server.","Hay que abrir el ERP en línea: la exportación de la caja está en el servidor.")}</p>`; return; }
  try{ const r=await fetch(CK_URL+'/api/o/'+CK_ORG+'/donnees/lightspeed-export-v1',{headers:{Authorization:'Bearer '+ckTok()},cache:'no-store'});
    if(r.status!==404){ if(!r.ok) throw new Error('serveur '+r.status); const j=await r.json(); if(j&&j.val&&Array.isArray(j.val.lignes)) LSM.X=j.val; } }
  catch(e){ $('lsmcorps').innerHTML=`<p class="hint">${lsmT('Le serveur ne répond pas. Réessaie dans un instant.','The server is not responding. Try again in a moment.','El servidor no responde. Vuelve a intentarlo en un momento.')}</p>`; return; }
  lsmCalc(); lsmPeint();
}
/* l'export du catalogue wholesale : l'identifiant de chaque ligne (sans lui, Lightspeed crée un doublon) et son prix actuel */
function lsmLitTarif(texte){
  const L=csvLignes(texte); if(L.length<1) return null;
  const H=L[0].map(x=>String(x).trim().toLowerCase()), ix=k=>H.indexOf(k), par={};
  L.slice(1).forEach(c=>{ const g=k=>String(c[ix(k)]==null?'':c[ix(k)]).trim(); const sku=g('sku'), id=g('id'); if(!sku||!id) return;
    const e={id,h:g('handle'),p:+g('retail_price')||0,lv:g('loyalty_value'),mn:g('min_units'),mx:g('max_units')};
    if(par[sku]&&(e.mn||e.mx)) return;   /* un palier par quantité : la ligne simple reste celle de référence */
    par[sku]=e; });
  return par;
}
/* on peut déposer les deux exports d'un coup : on reconnaît chacun à sa première ligne */
async function lsmDepose(fichiers){
  const m=$('lsmmsg'); m.textContent=lsmT("Lecture…","Reading…","Leyendo…"); m.className='msg';
  const dits=[];
  for(const f of [].concat(fichiers)){
    let texte=''; try{ texte=String(await f.text()).replace(/^﻿/,''); }catch(e){}
    const tete=(texte.split(/\r?\n/,1)[0]||'').trim().toLowerCase().replace(/"/g,'');
    if(tete.startsWith(LSM_ENTETE_W)){
      if(!/wholesale/i.test(f.name||'')){ dits.push({err:1,t:lsmT(`« ${f.name} » est un autre catalogue de prix : il faut l'export du catalogue wholesale.`,`“${f.name}” is another price book: the wholesale price book export is needed.`,`«${f.name}» es otro catálogo de precios: hace falta la exportación del catálogo wholesale.`)}); continue; }
      const par=lsmLitTarif(texte)||{}, nb=Object.keys(par).length;
      ecrit(K_LSM_T,{t:new Date().toISOString(),n:nb,u:USR||'',par});
      log({act:'prix',lib:'Lightspeed : export du catalogue wholesale déposé ('+nb+' prix)',n:nb,impact:0,det:[]});
      dits.push({t:lsmT(`Catalogue wholesale reçu : ${nf(nb)} prix.`,`Wholesale price book received: ${nf(nb)} prices.`,`Catálogo wholesale recibido: ${nf(nb)} precios.`)});
    } else if(/^id,handle,sku/.test(tete)){
      try{ const r=await fetch(CK_URL+'/api/o/'+CK_ORG+'/lightspeed/export',{method:'POST',headers:{'Content-Type':'text/csv',Authorization:'Bearer '+ckTok()},body:texte});
        const j=await r.json().catch(()=>({})); if(!r.ok) throw new Error(j.erreur||('serveur '+r.status));
        dits.push({t:lsmT(`Export reçu : ${nf(j.exportGarde)} produits.`,`Export received: ${nf(j.exportGarde)} products.`,`Exportación recibida: ${nf(j.exportGarde)} productos.`)}); }
      catch(e){ dits.push({err:1,t:(e&&e.message)||'échec'}); }
    } else dits.push({err:1,t:lsmT(`« ${f.name} » n'est ni l'export des produits ni celui du catalogue wholesale.`,`“${f.name}” is neither the product export nor the wholesale price book export.`,`«${f.name}» no es ni la exportación de productos ni la del catálogo wholesale.`)});
  }
  await lsmCharge();
  m.textContent=dits.map(d=>d.t).join(' '); m.className='msg '+(dits.some(d=>d.err)?'err':'ok');
}
function lsmFichiers(){
  const X=LSM&&LSM.X, rec=LSM&&LSM.rec; if(!X||!rec) return;
  lsmCalc(); const B=LSM.bloque||{}, recs=LSM.rec;
  const cols=(X.cols||[]).filter(c=>!LSM_STOCK.test(c));
  const R=B.retail?[]:recs.filter(x=>x.chR).map(x=>cols.map(c=>lsmQ(c==='retail_price'?(+x.pvr).toFixed(2):x.r[c])).join(','));
  const W=B.gros?[]:recs.filter(x=>x.w).map(x=>{ const t=x.w.t||{}; return [x.r.sku,x.r.handle||x.r.sku,x.w.id||'',(+x.pvw).toFixed(2),t.lv||'',t.mn||'',t.mx||''].map(lsmQ).join(','); });
  const m=$('lsmmsg');
  if(!R.length&&!W.length){ m.textContent=lsmT('Rien à envoyer.','Nothing to send.','Nada que enviar.'); m.className='msg'; return; }
  /* bom : le fichier Retail garde le BOM (accents lus en UTF-8 : essai réussi le 8 nov.) ; le fichier WHOLESALE n'en a PAS :
     la page des catalogues de prix de Lightspeed ignore EN SILENCE un fichier qui commence par un BOM (essai du 8 nov. 2026 :
     « Your pricebook is importing », puis rien — le même fichier sans BOM est passé) */
  const tele=(nom,lignes,bom)=>{ const el=document.createElement('a'); el.href=URL.createObjectURL(new Blob([(bom?'﻿':'')+lignes.join('\r\n')+'\r\n'],{type:'text/csv;charset=utf-8'})); el.download=nom; document.body.appendChild(el); el.click(); el.remove(); setTimeout(()=>URL.revokeObjectURL(el.href),2000); };
  if(R.length) tele(`lightspeed-retail-${ajd()}.csv`,[cols.join(',')].concat(R),true);
  if(W.length) setTimeout(()=>tele(`lightspeed-wholesale-${ajd()}.csv`,[LSM_ENTETE_W].concat(W),false),600);
  LSM.bom={R:true,W:false};   /* pour les tests */
  const V=lsmEnvoi(), ici=new Date().toISOString();
  const E={t:ici,u:USR||'',retail:R.length,gros:W.length,tR:R.length?ici:(V.tR?new Date(V.tR).toISOString():''),tW:W.length?ici:(V.tW?new Date(V.tW).toISOString():'')};
  ecrit(K_LSM_E,E);
  log({act:'prix',lib:'fichiers Lightspeed préparés : '+R.length+' prix retail à changer, '+W.length+' prix de gros (catalogue wholesale)'+(LSM.dout&&LSM.dout.length?', '+LSM.dout.length+' prix à vérifier non envoyés':''),n:R.length+W.length,impact:0,det:[]});
  const msgs=[]; if(R.length) msgs.push(lsmT(`Retail (${nf(R.length)} prix)`,`Retail (${nf(R.length)} prices)`,`Retail (${nf(R.length)} precios)`)); if(W.length) msgs.push(lsmT(`Wholesale (${nf(W.length)} prix)`,`Wholesale (${nf(W.length)} prices)`,`Wholesale (${nf(W.length)} precios)`));
  m.textContent=lsmT('Fichiers téléchargés : ','Files downloaded: ','Archivos descargados: ')+msgs.join(lsmT(' et ',' and ',' y '))+lsmT('. À charger dans Lightspeed.','. Load them in Lightspeed.','. Cárgalos en Lightspeed.'); m.className='msg ok';
  LSM.derniers={R:R.length?[cols.join(',')].concat(R):[],W:W.length?[LSM_ENTETE_W].concat(W):[]};   /* pour les tests */
}
function lsmOuvre(){ $('lsmt').textContent=lsmT('Mettre à jour Lightspeed','Update Lightspeed','Actualizar Lightspeed'); $('lsmannul').textContent=lsmT('Fermer','Close','Cerrar'); $('lsmok').textContent=lsmT('Préparer les fichiers','Prepare the files','Preparar los archivos');
  $('lsmmsg').textContent=''; $('lsmmsg').className='msg'; $('lsmcorps').innerHTML=`<p class="hint">${lsmT('Lecture…','Loading…','Cargando…')}</p>`; $('lsmok').disabled=true; $('lsmov').classList.add('on'); lsmCharge(); }
function lsmFerme(){ $('lsmov').classList.remove('on'); }
{ const b=$('lsmaj'); if(b){ b.onclick=lsmOuvre; const t=$('lsmaj-t'); if(t) t.textContent=lsmT('Mettre à jour Lightspeed','Update Lightspeed','Actualizar Lightspeed');
    if(typeof peut==='function'&&!(peut('voirMarge')&&peut('voirPA'))) b.style.display='none'; } }
$('lsmx').onclick=lsmFerme; $('lsmannul').onclick=lsmFerme; $('lsmok').onclick=lsmFichiers;
$('lsmov').addEventListener('click',e=>{ if(e.target===$('lsmov')) lsmFerme(); });
document.addEventListener('keydown',e=>{ if(e.key==='Escape'&&$('lsmov').classList.contains('on')) lsmFerme(); });
window.__LSM={get(){ return LSM; }, calc:lsmCalc, fichiers:lsmFichiers, ouvre:lsmOuvre};
/* NOUVEAUX ARRIVAGES (8 nov. 2026) : le code vit dans lib/arrivage.js, chargé seulement quand la fenêtre s'ouvre
   (la page du Catalogue reste sous le million d'octets) */
function arrivageOuvre(fid){
  if(typeof arrivageFenetreOuvre==='function') return arrivageFenetreOuvre(fid);
  const sc=document.createElement('script'); sc.src='lib/arrivage.js?v=__VER__';
  sc.onload=()=>{ try{ arrivageFenetreOuvre(fid); }catch(e){ console.error(e); } };
  sc.onerror=()=>alert(L3('La fenêtre des arrivages ne se charge pas : recharge la page.','The arrivals window does not load: reload the page.','La ventana de arribos no carga: recarga la página.'));
  document.head.appendChild(sc);
}
$('lsov').addEventListener('click',e=>{ if(e.target===$('lsov')) lsFerme(); });
document.addEventListener('keydown',e=>{ if(e.key==='Escape'&&$('lsov').classList.contains('on')) lsFerme(); });

majVue();
try{ remplitMarques(); }catch(e){}
$('fseuil').value=SEUIL;
$('fseuil').addEventListener('input',()=>{
  const v=parseInt($('fseuil').value,10);
  SEUIL = isNaN(v)?0:Math.max(0,Math.min(999,v));
  REG.seuilQte=SEUIL; sauveREG();
  paint(); majSeuil();
});
alignePrixAnciens();
{ const sc=document.createElement('script'); sc.src='lib/prixsites.js?v=__VER__'; document.head.appendChild(sc); }   /* les prix des fiches publiés pour les sites (_prixsites.py) */
render();
majSeuil();
/* catalogue.html?q=… (lien depuis une autre page) et, depuis le 25 oct. 2026, catalogue.html?photo=0 (le tableau
   de bord envoie sur « Sans photo »). Ici, APRÈS le premier render : plus haut dans le script, nf() n'existait
   pas encore et le lien plantait la page. */
{ const sp=new URLSearchParams(location.search), q0=sp.get('q'), ph0=sp.get('photo');
  if(q0){ $('q').value=q0; $('fs').value=''; render(); }
  if(ph0==='0'||ph0==='1'){ $('fp').value=ph0; render(); }
  /* 25 oct. 2026 : le tableau de bord (« Pas en vente partout ») envoie sur le filtre Diffusion */
  const df=sp.get('diff'); if(df&&['any','site','sitegros','perfumecity','all'].includes(df)){ $('fd').value=df; render(); } }
/* catalogue.html#cle=b123… : ouvrir directement une fiche (lien depuis VIP wholesale, Ventes…) */
/* Arrivée depuis l'Inventaire par « Mettre à jour depuis un fichier » :
   la fenêtre d'import s'ouvre toute seule. */
(function(){ if(location.hash!=='#maj') return;
  setTimeout(()=>{ try{ $('maj').click(); }catch(e){} },120); })();

/* Mode « cadre » (17 oct. 2026, Igal : « quand je clique sur un produit, une fenêtre s'ouvre pour que Sam ait la fiche ») :
   la page Factures ouvre catalogue.html#cle=…&cadre=1 dans une fenêtre. On n'y montre que la fiche, sans le menu ni la
   liste, et sa fermeture prévient la page qui l'a ouverte. */
if(/[#&]cadre=1/.test(location.hash) && window.parent!==window){
  document.documentElement.classList.add('cadre');
  /* un lien de la fiche ne doit jamais remplacer la fiche par une autre page DANS la fenêtre : il s'ouvre dans un nouvel onglet,
     et la page d'où l'on vient (Ventes, Factures…) reste là où elle est */
  document.addEventListener('click',e=>{ const a=e.target.closest&&e.target.closest('a[href]');
    if(a&&!a.target&&!/^#/.test(a.getAttribute('href')||'')){ a.target='_blank'; a.rel='noopener'; } },true);
}
(function(){ const cadre=document.documentElement.classList.contains('cadre');
  const pret=()=>{ if(cadre) document.documentElement.classList.add('cp'); };
  /* 5 nov. 2026 : depuis une facture d'achat, les nouvelles références à mettre en ligne (#enligne=id1,id2&cadre=1) */
  const me=location.hash.match(/enligne=([^&]+)/);
  if(me){ const ids=decodeURIComponent(me[1]).split(',').filter(Boolean); const mc=location.hash.match(/[#&]canaux=([^&]+)/); const cs=(mc&&mc[1]!=='1')?decodeURIComponent(mc[1]).split(',').filter(Boolean):[];
    pret(); setTimeout(()=>{ try{ enLigneAutoListe(ids,cs); }catch(e){ console.error(e); } },80); return; }
  /* 7 nov. 2026 : depuis Tâches, poser les prix corrigés sur les canaux cochés (#prix=id&canaux=site,sitegros,perfumecity&cadre=1) */
  const mp=location.hash.match(/[#&]prix=([^&]+)/);
  if(mp){ const id=decodeURIComponent(mp[1]); const mc=location.hash.match(/[#&]canaux=([^&]+)/); const cs=mc?decodeURIComponent(mc[1]).split(',').filter(Boolean):[];
    pret(); setTimeout(()=>{ try{ prixAutoCanaux(id,cs); }catch(e){ console.error(e); } },80); return; }
  /* 8 nov. 2026 : depuis une réception (Factures), envoyer les nouveaux arrivages aux clients favoris (#arrivage=<id>&cadre=1) */
  const ma=location.hash.match(/[#&]arrivage=([^&]+)/);
  if(ma){ pret(); setTimeout(()=>{ try{ arrivageOuvre(decodeURIComponent(ma[1])); }catch(e){ console.error(e); } },80); return; }
  const m=location.hash.match(/cle=([^&]+)/); if(!m){ pret(); return; }
  const id=decodeURIComponent(m[1]); const p=tousLesArticles().find(x=>x.id===id); if(!p){ pret(); return; }
  $('fs').value=''; $('q').value=p.bc||p.nom; render(); setTimeout(()=>{ ouvreFiche(id); pret();
    /* 25 oct. 2026 : depuis le tableau de bord (« Pas en vente partout »), &mel=1 ouvre tout de suite la fenêtre
       « Mettre en ligne » de CE parfum, sur les canaux où il manque — un clic depuis le tableau de bord, pas trois. */
    /* 31 oct. 2026 : depuis le tableau de bord (&canaux=1), la fiche s'ouvre directement sur « Mes canaux de vente », où chaque site
       manquant a son bouton (Mettre en ligne / Remettre en vente) — rien ne cache les prix */
    if(/[#&]canaux=1/.test(location.hash)){ setTimeout(()=>{ try{ const z=document.querySelector('.dcanw'); if(z){ z.open=true; z.scrollIntoView({block:'start'}); z.classList.add('flash'); setTimeout(()=>z.classList.remove('flash'),2200); } }catch(e){} },150); }
    if(/[#&]mel=1/.test(location.hash)){ try{ const ids=CAN_DIFF.map(c=>c[0]).filter(i=>statutDiff(p,i)==='non');
      if(ids.length){ ouvreMel([p],ids);
        /* depuis le tableau de bord on vient pour mettre EN VENTE (Igal, 30 oct. 2026 : « qu'ils aillent directement sur le
           site concerné ») : le choix est déjà sur « en vente tout de suite », le brouillon reste possible */
        const mm=document.getElementById('melm'); if(mm) mm.value='publie'; } }catch(e){} }
  },60); })();

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
import base64, os, glob as _glob
_logos={}
for _f in sorted(_glob.glob('logos/*.png'))+sorted(_glob.glob('logos/*.svg')):
    _id=os.path.splitext(os.path.basename(_f))[0]
    if _id in _logos: continue
    _mime='image/png' if _f.endswith('.png') else 'image/svg+xml'
    _logos[_id]='data:'+_mime+';base64,'+base64.b64encode(open(_f,'rb').read()).decode()
out=(TPL.replace('__FUSION__',FUSION)
       .replace('__COMPTES__',COMPTES).replace('__AIDECSS__',_aide.CSS)
       .replace('__SAUVE__',SAUVE)
       .replace('__MENU__',MENU)
       .replace('__LANGUE__',LANGUE).replace('__VOCAB__',_langue.VOCAB).replace('__LIRE__',_lire.bloc()).replace('__SORTIE__',_sortie.JS).replace('__ACCEPT_TAB__',_lire.ACCEPT_TAB)
       .replace('__IDENT__',IDENT).replace('__IDENT_TOT__',_identite.TOT).replace('__FILE_AUTO__',_file_auto.FILE_AUTO)
       .replace('__GARDE__',_donnees.garde(['produits']))
       .replace('__DATA__','window.D_PROD')
       .replace('__LOGOS__',json.dumps(_logos))
       .replace('__MARCHE__',open('marche_seed.json').read())
       .replace('__SHEET__',open('sheet_seed.json').read())
       .replace('__FACTURE__',open('facture_seed.json').read())
       .replace('__FRNINIT__',open('frn_seed.json').read().strip()))
_ncli=(len([c for c in json.load(open('clients_seed.json'))['clients']
            if any(not x['devis'] and not x['douteux'] for x in c['cmds'])])
       if os.path.exists('clients_seed.json') else 0)
out=out.replace('__BARRE__', barre('Catalogue'))
for k,v in {'__NCLI__':str(_ncli),'__TOTAL__':n(S['total']),'__ENSTOCK__':n(S['enstock']),'__RUPTURE__':n(S['rupture']),
            '__UNITES__':n(S['unites']),'__PHOTOS__':n(S['photos']),'__A0__':n(S['anytot']),
            '__VERSION__':__import__('datetime').datetime.now().strftime('%m/%d/%Y \u00e0 %Hh%M'),
            '__VER__':__import__('datetime').datetime.now().strftime('%Y%m%d%H%M')}.items():
    out=out.replace(k,v)
for i in range(1,10):
    out=out.replace(f'__A{i}__', n(S['an'].get(str(i),0)))
open('catalogue.html','w').write(enligne(out))
import _prixsites; _prixsites.ecrit('.')   # lib/prixsites.js : les prix des fiches publiés pour le cockpit
import _arrivage; _arrivage.ecrit('.')   # lib/arrivage.js : la fenêtre des nouveaux arrivages (chargée à la demande)
import os;print('catalogue.html',round(os.path.getsize('catalogue.html')/1024),'Ko')
