import json
from build_crm import barre
from _fusion import FUSION
from _comptes import COMPTES
import _aide
from _serveur import enligne
from _identite import IDENT
from _sauvegarde import SAUVE
from _menu import MENU
from _langue import LANGUE
import _lire
data=open('cat.json').read()
import _donnees
_donnees.produits()
S=json.load(open('cat_stats.json'))
n=lambda v: f"{v:,}".replace(',',' ')
TPL = r'''<!DOCTYPE html>
<html lang="fr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta http-equiv="Cache-Control" content="no-store, no-cache, must-revalidate">
<meta http-equiv="Pragma" content="no-cache">
<meta http-equiv="Expires" content="0">

<title>Catalogue — Perfumes Trade</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap">
<style>
:root{--ground:#F4F4F1;--surface:#FFF;--surface-2:#FAFAF8;--ink:#17171D;--ink-2:#4A4A56;--ink-3:#7C7C88;
--line:#E0E0DC;--line-2:#EDEDE9;--line-3:#CFCFC8;--iris:#5B4B8A;--iris-soft:#EDE9F6;
--good:#2C6E4E;--good-soft:#E9F3ED;--warn:#8A5A00;--warn-soft:#FBF3E2;--crit:#A4262C;--crit-soft:#FBECEC;}
@media(prefers-color-scheme:dark){:root:not([data-theme="light"]){
--ground:#121217;--surface:#1A1A21;--surface-2:#202028;--ink:#ECECF1;--ink-2:#B0B0BC;--ink-3:#80808E;
--line:#2C2C36;--line-2:#26262F;--line-3:#3D3D4B;--iris:#A99AE0;--iris-soft:#272036;
--good:#77C79C;--good-soft:#152A20;--warn:#D9A94A;--warn-soft:#2E2411;--crit:#E8898D;--crit-soft:#33191B;}}
:root[data-theme="dark"]{--ground:#121217;--surface:#1A1A21;--surface-2:#202028;--ink:#ECECF1;--ink-2:#B0B0BC;
--ink-3:#80808E;--line:#2C2C36;--line-2:#26262F;--line-3:#3D3D4B;--iris:#A99AE0;--iris-soft:#272036;
--good:#77C79C;--good-soft:#152A20;--warn:#D9A94A;--warn-soft:#2E2411;--crit:#E8898D;--crit-soft:#33191B;}
*{box-sizing:border-box}
body{font-variant-numeric:tabular-nums;font-feature-settings:"tnum" 1,"cv05" 1}
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
display:flex;flex-direction:column;padding:20px 0 16px}
.logo{padding:0 18px 18px;border-bottom:1px solid var(--line-2);margin-bottom:14px}
.logo .n{font-size:16px;font-weight:700;letter-spacing:-.02em;line-height:1.2}
.logo .s{font-family:Inter,sans-serif;font-size:9.5px;letter-spacing:.15em;
text-transform:uppercase;color:var(--ink-3);margin-top:3px}
nav{display:flex;flex-direction:column;gap:1px;padding:0 10px}
.navlab{font-family:Inter,sans-serif;font-size:11.5px;letter-spacing:.14em;text-transform:uppercase;
color:var(--iris);font-weight:800;padding:16px 8px 6px}
.nv{display:flex;align-items:center;gap:9px;padding:8px 10px;white-space:nowrap;border-radius:4px;font-size:14px;
color:var(--ink);font-weight:600;text-decoration:none;line-height:1.3;border-left:2px solid transparent}
.nv .ic{width:15px;text-align:center;flex:0 0 15px;opacity:.75}
.nv .ct{margin-left:auto;font-family:Inter,sans-serif;font-size:10.5px;font-weight:500;color:var(--ink-3);
font-variant-numeric:tabular-nums}
.nv .ct.pt{background:var(--iris-soft);color:var(--iris);font-weight:700;font-size:10.5px;border-radius:10px;padding:2px 7px;min-width:20px;text-align:center;line-height:1.5}
.nv:hover{background:var(--surface-2);color:var(--ink)}
.nv.on{background:var(--iris-soft);color:var(--iris);font-weight:700;border-left-color:var(--iris)}
.nv.on .ic{opacity:1}
.nv.soon{color:var(--ink-3);font-weight:500;cursor:default;pointer-events:none}
.nv.soon .ct{font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.8}
.ver{margin-top:9px;font-family:Inter,sans-serif;font-size:10px;color:var(--ink-3);opacity:.75;letter-spacing:.02em}
.sfu{margin-bottom:9px;padding-bottom:9px;border-bottom:1px solid var(--line-2);
font-family:Inter,sans-serif;font-size:11.5px;color:var(--ink-3);line-height:1.5}
.sfu b{color:var(--iris);font-weight:600}
.lnk{background:none;border:0;padding:0;font-family:inherit;font-size:11.5px;color:var(--ink-3);
text-decoration:underline;cursor:pointer}
.lnk:hover{color:var(--iris)}
.sfoot{margin-top:auto;padding:14px 18px 14px;border-top:1px solid var(--line-2);
font-family:Inter,sans-serif;font-size:10px;color:var(--ink-3);line-height:1.7}
.main{flex:1;min-width:0}
.wrap{max-width:1400px;margin:0 auto;padding:26px 26px 70px}
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
text-transform:uppercase;color:var(--iris);line-height:1.35;margin-bottom:4px;
white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.nm{font-size:18px;font-weight:700;line-height:1.24;letter-spacing:-.02em;color:var(--ink);
display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;
min-height:2.48em;margin-bottom:6px;text-wrap:balance}
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


/* ================= FICHE PRODUIT ================= */
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
display:flex;align-items:center;justify-content:center;overflow:hidden;padding:13px;position:relative}
.dstk{display:flex;flex-direction:column;gap:11px;min-width:0}
.dstk .big{display:flex;align-items:baseline;gap:9px;flex-wrap:wrap}
.dstk .big b{font-family:Inter,sans-serif;font-size:36px;font-weight:600;line-height:.92;
letter-spacing:-.03em;font-variant-numeric:tabular-nums}
.dstk .big em{font-style:normal;font-size:13px;color:var(--ink-3)}
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
.dcompt{font-size:12px;color:var(--ink-3);background:var(--surface-2);border-radius:6px;
padding:8px 11px;line-height:1.5;border-left:2px solid var(--line)}
.dcompt.ec{border-left-color:var(--crit)}
.dcompt b{color:var(--ink-2)}

/* --- rail de prix --- */
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
.df .st.ok{color:var(--good)}
.card{cursor:pointer}
.card:focus-visible{outline:2px solid var(--iris);outline-offset:2px}
@media(max-width:640px){.dr{width:100%}.dhero{grid-template-columns:104px 1fr;gap:13px}
.dstk .big b{font-size:29px}.drail{grid-template-columns:1fr 1fr}
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
@media(max-width:1439px){.lstw{overflow-x:auto}}   /* ecran etroit : le tableau defile, l'en-tete ne peut plus rester fige */
.lst{width:100%;border-collapse:collapse;font-size:13.5px;min-width:940px}
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
line-height:1.3;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.lnm{font-size:15px;font-weight:700;color:var(--ink);letter-spacing:-.015em;line-height:1.3;
white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:340px}
.lmeta{font-size:12.5px;color:var(--ink-2);white-space:nowrap}
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
.laz.vieux{color:var(--ink-2);font-weight:500}
.lazage{display:block;font-family:Inter,sans-serif;font-size:10px;color:var(--ink-3);
letter-spacing:.02em;margin-top:1px;white-space:nowrap}
.lazage.perime{color:var(--warn)}
.lmg.g{color:var(--good)} .lmg.w{color:var(--warn)} .lmg.c{color:var(--crit)}
.lfl{display:flex;flex-direction:column;align-items:flex-start;gap:4px;white-space:nowrap}
.lfl .fl{font-size:11px;padding:4px 9px 4px 7px}
.lst td.colfl{min-width:190px}
.lst thead th.colmg span{white-space:normal;line-height:1.25;max-width:78px}
.lfl .fl{max-width:none;overflow:visible}
/* Sur un ecran de portable, le nom se resserre et le code-barres se cache pour que
   la colonne Alertes reste visible sans faire defiler le tableau. */
.lnm{max-width:240px}.lst td,.lst thead th{padding-left:8px;padding-right:8px}
@media(max-width:1560px){.lst .colbc{display:none}.lnm{max-width:190px}.lst td,.lst thead th{padding-left:7px;padding-right:7px}.lst td.colfl{min-width:170px}.lmeta{font-size:12px}}
body.client .lst .colpa,body.client .lst .colq,body.client .lst .colmg,body.client .lst .colfl{display:none}


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
</style></head><body>
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
  <div class="sfoot"><div id="sfu" class="sfu"></div><span id="sfoot">__TOTAL__ références<br>__ENSTOCK__ en stock<br>__UNITES__ unités</span>
  <div class="ver" title="Si cette date n'est pas la derni&egrave;re, recharge avec Cmd+Option+R">version du __VERSION__</div></div>
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
  </div>
  <select id="fs" hidden><option value="in" selected></option><option value="out"></option><option value=""></option></select>

  <div class="selw"><select id="fb" aria-label="Marque"><option value="">Toutes les marques</option></select></div>
  <div class="selw"><select id="fg" aria-label="Genre"><option value="">Tous genres</option>
    <option value="M">Homme</option><option value="W">Femme</option>
    <option value="U">Unisexe</option><option value="K">Enfant</option></select></div>

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
    <button class="btn" id="maj">Mettre à jour le stock</button>
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
    <option value="todo">À compléter</option></select></div>
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
        <div class="fld"><label>Marque <b>*</b></label><input id="f-marque" list="l-marques" autocomplete="off"></div>
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

<script src="donnees/langue.js"></script>
<script src="donnees/produits.js"></script>__GARDE__
<script>
__FUSION__
__COMPTES__
__IDENT__
__SAUVE__
__MENU__
__LANGUE__
__LIRE__
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
function tousLesArticles(){
  return AJ.map((o,i)=>{const x=normAJ(o); x.id=o.id||('a'+i); x.an=calcAn(x); return applique(x);})
           .concat(P.map(p=>applique(externe(p))));
}

[...new Set(P.map(p=>p.marque))].sort((a,b)=>a.localeCompare(b,'fr')).forEach(b=>
 $('fb').insertAdjacentHTML('beforeend',`<option value="${b}">${b}</option>`));
[...new Set(P.map(p=>p.type).filter(Boolean))].sort().forEach(t=>
 $('ft').insertAdjacentHTML('beforeend',`<option value="${t}">${t}</option>`));

// 1) photo locale  2) photo du site  3) message
function secours(img){
  const far=img.dataset.far;
  if(far && img.src.indexOf('photos/')>-1){ img.src=far; return; }
  const d=document.createElement('div'); d.innerHTML=`<div class="miss"><svg viewBox="0 0 40 64" fill="none" aria-hidden="true"><rect x="14.5" y="2" width="11" height="9" rx="1.5" stroke="currentColor" stroke-width="2.4"/><path d="M11 20a6 6 0 016-6h6a6 6 0 016 6v34a6 6 0 01-6 6H17a6 6 0 01-6-6V20z" stroke="currentColor" stroke-width="2.4"/></svg><span>sans photo</span></div>`;
  img.replaceWith(d.firstElementChild);
}
const money=v=>v==null?null:v.toLocaleString('fr-FR',{minimumFractionDigits:2,maximumFractionDigits:2})+' $';
const esc=s=>String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));

function card(p){
 const meta=[p.ml?`<b>${esc(p.ml)}</b> oz`:'',esc(p.type),G[p.genre]||''].filter(Boolean).join(' · ');
 const ph=p.img
  ?`<img src="photos/${p.bc}.webp" data-far="${p.img}" alt="${esc(p.marque)} ${esc(p.nom)}"
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
 return `<article class="card${p.neuf?' neuf':''}${CLIENT?'':(p.an.some(a=>[1,2,3,8].includes(a))?' alert':p.an.length?' warn':'')}" data-id="${p.id}" tabindex="0" role="button" aria-label="Ouvrir la fiche">
  <div class="ph">${ph}${chipn}<span class="qty${p.qte===0?' out':(SEUIL>0&&p.qte<SEUIL)?' low':''}">${p.qte===0?'historique':p.qte}</span></div>
  <div class="body">
    <div class="brand">${esc(p.marque)}</div>
    <div class="nm">${esc(p.nom)}</div>
    <div class="meta">${meta||'&nbsp;'}</div>
    ${(chiptodo||chipf||flags)?`<div class="flags">${chiptodo}${chipf}${flags?flags.replace(/<\/?div[^>]*>/g,''):''}</div>`:''}
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
function azLien(p, m){
  if(m && m.url) return m.url;
  if(p.asin) return 'https://www.amazon.com/dp/'+encodeURIComponent(p.asin);
  if(p.bc)   return 'https://www.amazon.com/s?k='+encodeURIComponent(p.bc);
  return 'https://www.amazon.com/s?k='+encodeURIComponent(((p.marque||'')+' '+(p.nom||'')+' '+(p.ml?p.ml+' oz':'')).trim());
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
    if(p.asin) (parAsin[String(p.asin).toUpperCase()] ||= []).push(p);
    if(p.bc)   (parBc[String(p.bc).trim()] ||= []).push(p);
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
  {k:'fmt',   lib:'Format',        t:'num', v:p=>parseFloat(String(p.ml).replace(',','.'))},
  {k:'qte',   lib:'Stock',         t:'num', v:p=>p.qte, cls:'colq',  al:'r'},
  {k:'pa',    lib:"Prix d'achat",  t:'num', v:p=>p.pa,  cls:'colpa', al:'r'},
  {k:'pvr',   lib:'Prix retail',   t:'num', v:p=>p.pvr, al:'r'},
  /* Trier sur l'ECART, pas sur le prix Amazon : « qui est le plus loin du
     marche » est la question qu'on se pose ; « qui coute le plus cher chez
     Amazon » n'interesse personne. Sans releve, la valeur est nulle et la
     ligne part en bas, comme les autres colonnes vides. */
  {k:'az',    lib:'Amazon',        t:'num', v:p=>{ const e=azEcart(p); return e?e.d:null; },
              cls:'colaz', al:'r'},
  {k:'pvw',   lib:'Prix de gros',  t:'num', v:p=>p.pvw, al:'r'},
  {k:'mgr',   lib:'Marge retail',  t:'num', v:p=>marge(p,p.pvr), cls:'colmg', al:'r'},
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
  else if(TRI.dir===depart) TRI={col,dir:depart==='asc'?'desc':'asc'};
  else TRI=null;                                  /* troisieme clic : on revient au tri par defaut */
  sauveTRI();
  const sel=$('fo'); if(sel&&TRI) sel.value='b';
  render();
}


/* Seuil de stock faible. Il n'existe aucune bonne valeur universelle :
   elle depend de la vitesse d'ecoulement, qu'on ne connait pas encore.
   C'est donc a l'utilisateur de la fixer, en voyant combien de references
   son choix declenche. */
/* Reglages partages par toutes les rubriques. */
const KREG='reglages-v1';
const CANAUX_DEF=[{id:'boutique',nom:'Boutique',maj:0,com:0},{id:'site',nom:'Site perfumestrade.com',maj:0,com:3},
  {id:'shopify',nom:'Shopify',maj:0,com:3},{id:'amazon',nom:'Amazon',maj:18,com:15},{id:'perfumecity',nom:'Perfume City',maj:0,com:0}];
const REG_DEF={seuilQte:3,capMin:0,baissePct:30,baisseJours:30,margeMin:10,canaux:CANAUX_DEF};
let REG=Object.assign({},REG_DEF);
try{ const r=JSON.parse(localStorage.getItem(KREG)||'null'); if(r) REG=Object.assign({},REG_DEF,r); }catch(e){}
/* 3 septembre : eBay quitte la liste des canaux, Perfume City arrive (une seule fois, sans toucher aux autres) */
(function(){ try{ const K='canaux-ebay-perfumecity-v1'; if(localStorage.getItem(K)) return;
  if(Array.isArray(REG.canaux)){ REG.canaux=REG.canaux.filter(c=>c.id!=='ebay');
    if(!REG.canaux.some(c=>c.id==='perfumecity')) REG.canaux.push({id:'perfumecity',nom:'Perfume City',maj:0,com:0});
    localStorage.setItem(KREG,JSON.stringify(REG)); }
  localStorage.setItem(K,'1'); }catch(e){} })();
/* reprise de l'ancien reglage isole */
try{ const v=localStorage.getItem('seuil-stock-faible-v1');
  if(v!==null && !localStorage.getItem(KREG)){ REG.seuilQte=+v;
    localStorage.setItem(KREG,JSON.stringify(REG)); localStorage.removeItem('seuil-stock-faible-v1'); }
}catch(e){}
base(KREG,REG);
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
    ? `<span class="lph"><img src="photos/${p.bc}.webp" data-far="${p.img}" alt="" loading="lazy" onerror="secours(this)"></span>`
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
      <div class="lmq">${esc(p.marque)}</div>
      <div class="lnm">${esc(p.nom)}</div></div></div></td>
    <td><span class="lmeta">${meta||'—'}</span></td>
    <td class="r colq"><span class="lq${p.qte===0?' out':(SEUIL>0&&p.qte<SEUIL)?' low':''}">${p.qte===0?'historique':nf(p.qte)}</span>${p.qte===0?'':badgeComptage(p)}</td>
    <td class="r colpa">${prix(p.pa,'lpa')}</td>
    <td class="r">${prix(p.pvr,'lpr',star)}</td>
    <td class="r colaz">${azCell(p)}</td>
    <td class="r">${prix(p.pvw,'lpw')}</td>
    <td class="r colmg"><span class="lmg ${cm(mg(p.pvr))}">${pc(mg(p.pvr))}</span></td>
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
  document.querySelectorAll('#vue button').forEach(b=>b.classList.toggle('on',b.dataset.vue===VUE));
}
document.getElementById('vue').addEventListener('click',e=>{
  const b=e.target.closest('[data-vue]'); if(!b) return;
  VUE=b.dataset.vue; try{ localStorage.setItem(KVUE,VUE); }catch(x){}
  majVue(); paint();
});
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
 majBarre(); majSeuil();
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
  if(ail && st){
    const ou = st==='in' ? "en historique (plus de stock)" : "en stock";
    const vers = st==='in' ? '' : 'in';
    el.innerHTML=`<b>${ail} référence${ail>1?'s':''} correspond${ail>1?'ent':''} — mais ${ail>1?'elles sont':'elle est'} ${ou}.</b>
      <span>Le catalogue n'affiche que ${st==='in'?'le stock disponible':"l'historique"} pour l'instant.</span>
      <button class="btn pri" id="vvoir">${ail>1?'Les':'La'} voir</button>`;
    $('vvoir').onclick=()=>{ $('fs').value=vers; render(); };
    return;
  }
  const nAutres=['fb','fg','ft','fp','fa','fan','fx'].filter(i=>{
    const e=$(i); return e.type==='checkbox'?e.checked:!!e.value; }).length;
  if(ail===0 && q && nAutres){
    el.innerHTML=`<b>Aucune référence ne correspond à « ${esc(q)} » avec les filtres actuels.</b>
      <span>${nAutres} filtre${nAutres>1?'s sont actifs':' est actif'} en plus de la recherche.</span>
      <button class="btn pri" id="vraz">Enlever les filtres, garder la recherche</button>`;
    $('vraz').onclick=()=>{ ['fb','fg','ft','fp','fan','fx'].forEach(i=>$(i).value='');
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
function render(){ mesureBarre();
 const TOUS=tousLesArticles();
 const q=$('q').value.trim().toLowerCase(),b=$('fb').value,g=$('fg').value,t=$('ft').value,st=$('fs').value,
  fx=$('fx').value,
  ph=$('fp').value,ast=$('fa').checked,an=$('fan').value,o=$('fo').value;
 const critere=p=>(!fx||(fx==='neuf'?!!p.neuf:fx==='mod'?!!p.mod:manque(p).length>0))&&
  (!b||p.marque===b)&&(!g||p.genre===g)&&(!t||p.type===t)&&(ph===''||(ph==='1'?!!p.img:!p.img))&&
  (!ast||p.src>0)&&(!an||(an==='all'?p.an.length>0:p.an.includes(+an)))&&
  (!q||(p.nom+' '+p.nomSrc+' '+p.marque+' '+p.bc+' '+(p.bcs||'')).toLowerCase().includes(q));
 /* Ce que la recherche trouverait SANS le filtre de stock : sert à expliquer
    une liste vide au lieu de laisser croire que le produit n'existe pas. */
 AILLEURS=TOUS.filter(critere);
 cur=AILLEURS.filter(p=>(!st||(st==='in'?p.qte>0:p.qte===0)));
 const tc=trieur();
 if(tc) cur.sort(tc);
 else if(o==='q')cur.sort((a,b)=>b.qte-a.qte);
 else if(o==='p')cur.sort((a,b)=>(a.pvw??1e9)-(b.pvw??1e9));
 else cur.sort((a,b)=>a.marque.localeCompare(b.marque,'fr')||a.nom.localeCompare(b.nom,'fr'));
 shown=PAGE; paint();
}
$('more').addEventListener('click',()=>{shown+=PAGE;paint();});
$('fc').addEventListener('input',()=>{document.body.classList.toggle('client',$('fc').checked);render();});
['q','fs','fx','fb','fg','ft','fp','fa','fan'].forEach(i=>$(i).addEventListener('input',render));
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
const dateFr=iso=>{ const d=new Date(iso); return d.toLocaleDateString('fr-FR',{day:'numeric',month:'long'})
  +' à '+d.toLocaleTimeString('fr-FR',{hour:'2-digit',minute:'2-digit'}); };
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
function prixCanal(p,c){
  const o=(p.pc||{})[c.id];
  if(o!=null&&o!=='') return {v:+o,man:true};
  if(p.pvr!=null&&p.pvr>0) return {v:r2(p.pvr*(1+(c.maj||0)/100)),man:false};
  return {v:null,man:false};
}
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
}
function valCour(p,k){ return FICHE.brouillon[k]!==undefined?FICHE.brouillon[k]:p[k]; }

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
const jourFr=d=>{ const [a,m,j]=d.split('-'); return j+'/'+m+'/'+a.slice(2); };

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
        <div class="dt">relevé le ${d?d.toLocaleDateString('fr-FR'):'?'}${m.par?' · '+esc(m.par):''}</div></div></div>`
    : `<div class="mvide">${m.dem?`<b>${esc(m.dem)}</b> achetés le mois dernier sur Amazon. `:''}Le rang n'a pas été relevé
        — il se lit sur la fiche produit Amazon, section « Best Sellers Rank ».
        ${d?`<span class="dt">Relevé le ${d.toLocaleDateString('fr-FR')}.</span>`:''}</div>`;
  const note = m.note?`<div class="dinfo">${esc(m.note)}</div>`:'';
  /* historique des relevés : chaque mise à jour garde l'ancien point */
  const H=(m.hist&&m.hist.length?m.hist:[{le:m.le,amz:m.amz,rang:m.rang}]).filter(h=>h.amz!=null);
  let histo='';
  if(H.length>=2){
    const lo=Math.min(...H.map(h=>h.amz)), hi=Math.max(...H.map(h=>h.amz));
    histo=`<div class="mhist"><b>${H.length} relevés Amazon</b> · plus bas ${money(lo)} · plus haut ${money(hi)}
      <ul>${H.slice(-8).reverse().map(h=>`<li>${new Date(h.le).toLocaleDateString('fr-FR')} — ${money(h.amz)}${h.rang?` · rang #${nf(h.rang)}`:''}</li>`).join('')}</ul></div>`;
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

function dessineFiche(){
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
  $('dprev').disabled=FICHE.pos<=0;
  $('dnext').disabled=FICHE.pos>=cur.length-1;

  const chips=[];
  if(p.neuf) chips.push('<span class="fl todo">ajouté à la main</span>');
  if(base.mod) chips.push('<span class="fl todo">fiche modifiée</span>');
  if(mq.length) chips.push(`<span class="fl w">${mq.length} champ${mq.length>1?'s':''} à compléter</span>`);
  p.an.forEach(a=>chips.push(`<span class="fl ${AN[a][1]}">${AN[a][0]}</span>`));

  const img=p.img?`<img src="photos/${p.bc}.webp" data-far="${p.img}" alt="" onerror="secours(this)">`
    :`<div class="miss"><svg viewBox="0 0 40 64" fill="none"><rect x="14.5" y="2" width="11" height="9" rx="1.5" stroke="currentColor" stroke-width="2.4"/><path d="M11 20a6 6 0 016-6h6a6 6 0 016 6v34a6 6 0 01-6 6H17a6 6 0 01-6-6V20z" stroke="currentColor" stroke-width="2.4"/></svg><span>sans photo</span></div>`;

  const champ=([k,lab,_col,t])=>{
    const v=valCour(p,k), vide=(v==null||v===''), chg=FICHE.brouillon[k]!==undefined;
    if(t==='sel') return `<div class="dfld${chg?' ch':''}"><label>${lab}</label>
      <select data-k="${k}">${Object.entries(GEN).map(([o,n])=>
        `<option value="${o}"${(v||'')===o?' selected':''}>${n}</option>`).join('')}</select></div>`;
    return `<div class="dfld${chg?' ch':''}"><label>${lab}</label>
      <input data-k="${k}" class="${t==='num'?'mono ':''}${vide?'vide':''}"
       type="${t==='num'?'number':'text'}" ${t==='num'?'step="any" inputmode="decimal"':''}
       value="${v==null?'':String(v).replace(/"/g,'&quot;')}"
       placeholder="${vide?'à compléter':''}"></div>`;
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
  const etape=(k,lab,_col,avecMarge)=>{
    const v=valCour(p,k), vide=(v==null||v===''), chg=FICHE.brouillon[k]!==undefined;
    let mg='';
    if(avecMarge){
      const t=marge(p,v);
      if(t==null) mg=`<i class="mg na">marge —</i>`;
      else mg=`<i class="mg ${t<0?'c':t<REG.margeMin?'w':'g'}">marge ${pc(t)}</i>`;
    }
    return `<div class="st${chg?' ch':''}"><span>${lab}</span>
      <div class="in"><input data-k="${k}" type="number" step="any" inputmode="decimal"
       class="${vide?'vide':''}" value="${v==null?'':v}" placeholder="—"><em>$</em></div>${mg}</div>`;
  };

  $('ddb').innerHTML=`
    <div class="dhero">
      <div class="dph">${img}</div>
      <div class="dstk">
        <div class="big"><b>${q}</b><em>flacon${q>1?'s':''} en stock</em></div>
        ${q>0?`<div class="cap">${cap?money(cap)+' de marchandise':'valeur inconnue'}</div>`:''}
        ${vbloc}
        ${q>0&&base.rang?`<div class="rk">Cette référence est la <b>n° ${base.rang}</b> du stock par l'argent
          qu'elle immobilise, soit <b>${(base.partCap||0).toFixed(2).replace('.',',')}\u00a0%</b> du capital total.</div>`:''}
        ${q===0?`<div class="rk">Conservée pour l'historique : elle a déjà été vendue, ses prix
          et son code-barres restent disponibles pour un réassort.</div>`:''}
        ${cpt}
      </div>
    </div>
    ${chips.length?`<div class="dchips">${chips.join('')}</div>`:''}

    <div class="dsec"><h3>Prix et marges</h3>
      <div class="drail">
        ${etape('pa','achat')}${etape('pvw','gros',null,true)}${etape('pvr','retail · prix boutique',null,true)}
      </div>
      <div class="dgrid" style="grid-template-columns:minmax(150px,220px)">${[CH[6]].map(champ).join('')}</div>
    </div>

    <div class="dsec"><h3>${logo('amazon','Amazon')}</h3>
      <div class="drail amz">
        ${(()=>{ const m=MAR[p.id]; const ca=canaux().find(c=>c.id==='amazon')||{id:'amazon',nom:'Amazon',maj:18,com:15};
          const {v}=prixCanal(p,ca);
          const ref=m&&m.amz!=null?m.amz:null;
          const d=m&&m.le?new Date(m.le).toLocaleDateString('fr-FR'):null;
          const bulle=`Prix de vente le moins cher relevé sur Amazon pour ce produit (ou un produit similaire, même contenance)${d?', relevé le '+d:''}. Ce n'est pas mon prix : c'est ce que le client trouve en face. Mon prix Amazon se règle plus bas, avec les autres canaux.`;
          return `<div class="st ref"><span>${logo('amazon','Amazon')} — le moins cher <i class="bul" tabindex="0" data-bul="${esc(bulle)}">i</i></span>
            <div class="in ro"><b>${ref!=null?money(ref):(m?'indisponible':'—')}</b></div>
            ${ref!=null&&p.pa!=null?`<i class="mg ${pcCls((ref-p.pa)/ref*100)}">${pct1((ref-p.pa)/ref*100)} de marge à ce prix-là</i>`:`<i class="mg na">${m?'aucun prix':'pas de relevé'}</i>`}
            ${horsCanal(p,'amazon')?`<span class="rl"><b style="color:var(--crit)">ce parfum n'est pas vendu sur Amazon</b></span>`
              :(ref!=null&&v!=null?`<span class="rl">mon prix Amazon (${money(v)}) est ${v>ref?`${money(v-ref)} au-dessus`:v<ref?`${money(ref-v)} en dessous`:'identique'}</span>`:'')}</div>
          ${(()=>{ /* le lien vers la fiche Amazon équivalente et son rang */
            const lien = azLien(p,m);
            /* L'ASIN ouvre LA fiche ; le code-barres ouvre dix résultats
               approchants dont il faut deviner lequel est le bon. */
            const exact = !!((m&&m.url) || p.asin);
            const bulleL = (m&&m.url)
              ? "Lien enregistré avec le relevé : la fiche Amazon du produit équivalent."
              : p.asin
              ? "ASIN "+esc(p.asin)+" repris de l'inventaire : ce lien ouvre directement la fiche Amazon de ce parfum, sans passer par une recherche."
              : (p.bc ? "Ce parfum n'a pas d'ASIN dans l'inventaire : à défaut, recherche Amazon sur son code-barres. Colle l'adresse exacte dans « Saisir un relevé » pour la garder."
                      : "Recherche Amazon sur la marque et le nom : ce parfum n'a ni ASIN ni code-barres.");
            return `<div class="st lien"><span>${logo('amazon','Amazon')} — rang et fiche <i class="bul" tabindex="0" data-bul="${esc(bulleL)}">i</i></span>
              ${m&&m.rang?`<div class="rang">#${nf(m.rang)}<small>${esc(m.cat||'catégorie non précisée')}${m.rangG?` · #${nf(m.rangG)} au général`:''}</small></div>`
                          :`<div class="rien">rang non relevé</div>`}
              ${m&&m.note5?`<span class="dt mnote"><b style="color:var(--ink);font-size:14px">${String(m.note5).replace('.',',')}/5</b>
                 <span class="et">${'★'.repeat(Math.round(m.note5))}${'☆'.repeat(5-Math.round(m.note5))}</span>
                 ${m.avis?`<span>${nf(m.avis)} avis</span>`:''}</span>`:''}
              <a class="go" href="${esc(lien)}" target="_blank" rel="noopener">${exact?'Ouvrir la fiche Amazon':'Chercher sur Amazon'} ↗</a>
              ${m?`<span class="dt">${m.dem?`<b>${esc(m.dem)}</b> achetés le mois dernier · `:''}${m.vend?`vendu par ${esc(m.vend)} · `:''}relevé le ${d||'?'}</span>`
                  :`<span class="dt">Aucun relevé. Ouvre la fiche Amazon, note le prix le plus bas et le « Best Sellers Rank », puis saisis-les ici.</span>`}
              <button class="maj" data-mar="edit">${m?'Mettre à jour le relevé':'Saisir un relevé'}</button></div>`; })()}`; })()}
      </div>
    </div>

    <details class="dsec dcanw" open><summary><h3>Mes canaux de vente<span class="hh">${(()=>{ const off=canaux().filter(c=>c.id!=='boutique'&&horsCanal(p,c.id));
        const n=canaux().length-1-off.length;
        return off.length?`${n>1?n+' canaux actifs':n===1?'1 canal actif':'aucun canal actif'} · <b style="color:var(--crit)">pas vendu sur ${off.map(c=>esc(c.nom)).join(', ')}</b>`
          :canaux().filter(c=>c.id!=='boutique').map(c=>esc(c.nom)).join(' · '); })()} · la boutique vend au prix retail · règle : retail + majoration · <a href="reglages.html?v=__VER__">régler</a></span></h3></summary>
      <div class="dcan">${canaux().filter(c=>c.id!=='boutique').map(c=>{
        if(horsCanal(p,c.id)) return `<div class="cn off"><span class="nm" title="${esc(c.nom)}">${logo(c.id,c.nom)}${c.id==='amazon'?' — mon prix':''}</span>
          <div class="offtx">pas vendu ici</div>
          <button class="offb" data-on="${c.id}">Remettre ce canal</button></div>`;
        const {v,man}=prixCanal(p,c), t=margeNette(p,c,v), chg=FICHE.brouillon.pc&&FICHE.brouillon.pc[c.id]!==undefined;
        const bulle=c.id==='amazon'?`Le prix auquel je veux vendre sur Amazon. Pré-rempli par la règle des Réglages (retail + ${c.maj||0} %), modifiable ici. La marge nette tient compte de la commission Amazon (${c.com||0} %). Ce prix reste dans l'outil : il n'est pas envoyé à Amazon, et il n'est pas prévu de l'envoyer. L'outil regarde les prix d'Amazon, il n'y touche pas.`:'';
        return `<div class="cn${man?' man':''}${chg?' ch':''}"><span class="nm" title="${esc(c.nom)}">${logo(c.id,c.nom)}${c.id==='amazon'?' — mon prix <i class="bul" tabindex="0" data-bul="'+esc(bulle)+'">i</i>':''}</span>
          <div class="in"><input data-pc="${c.id}" type="number" step="any" inputmode="decimal" value="${v==null?'':v}" placeholder="—"><em>$</em></div>
          <div class="ft"><i class="mg ${pcCls(t)}">${t==null?'marge —':'marge '+pc(t)+(c.com?' après les '+c.com+' % du canal':'')}</i>
          ${c.com&&v!=null&&p.pa!=null?`<span class="expl">${esc(c.nom)} garde ${c.com} % (${money(v*c.com/100)}) → il reste ${money(v*(1-c.com/100))} → moins l'achat ${money(p.pa)} = <b class="${pcCls(t)}">${money(v*(1-c.com/100)-p.pa)} de marge</b></span>`:''}
          <span class="rl">${man?`saisi à la main · <button data-pcr="${c.id}">revenir au calcul</button>`:(c.maj?`calculé : retail ${p.pvr!=null?money(p.pvr):''} + ${c.maj} %`:'= le retail')}</span>
          <button class="offb" data-off="${c.id}" title="Ce parfum n'est pas vendu sur ${esc(c.nom)}">ne pas vendre ici</button></div>
        </div>`; }).join('')}</div>
      ${p.src?`<div class="dinfo">Le prix retail vient de <b>perfumestrade.com</b>, il n'était pas dans l'inventaire.
        ${p.src===2?'<b style="color:var(--crit)">Il est inférieur ou égal au prix d\'achat</b> — à ne pas reprendre tel quel.':'À valider.'}</div>`:''}
    </details>

    ${blocHistorique(p)}

    ${blocMarche(p)}

    <div class="dsec"><h3>Identification</h3>
      <div class="dgrid">${CH.slice(0,6).map(champ).join('')}</div>
      <div class="dgrid" style="grid-template-columns:1fr;margin-top:8px">${[['bcs','Autres codes-barres de la même référence (séparés par des virgules)','-','txt']].map(champ).join('')}</div>
      <div class="dinfo" style="margin-top:6px">Le même parfum arrive parfois avec un code différent (autre lot, autre emballage, coffret). Scanné dans une facture, une vente ou un comptage, chacun de ces codes ramène à cette fiche.</div></div>

    <div class="dsec"><h3>Fournisseurs</h3>
      ${frnHtml||'<div class="dinfo">Aucun fournisseur enregistré pour cette référence.</div>'}
      <button class="btn" id="dfrn" style="align-self:flex-start">+ Ajouter un fournisseur</button>
      <div id="dfsyn">${synthFrn()}</div>
    </div>

    <div class="dsec"><h3>Fiche</h3>
      <div class="dinfo">
        Nom d'origine dans le fichier : <span class="mono">${esc(p.nomSrc||p.nom||'—')}</span><br>
        Photo : ${p.img?'<b>locale, calibrée 800 × 800</b>':'<b style="color:var(--warn)">aucune</b>'}<br>
        ${mq.length?`À compléter : <b>${mq.join(', ')}</b>`:'<b style="color:var(--good)">Fiche complète</b>'}
      </div>
    </div>`;
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
const enSaisie=()=>{ const a=document.activeElement; return !!(a&&a.dataset&&(a.dataset.k!==undefined||a.dataset.pc!==undefined)); };
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
function confirmePrix(L){
  const ko=L.some(l=>l.st==='ko');
  $('pxb').innerHTML=`<table class="pxt"><thead><tr><th>Prix</th><th class="r">Avant</th><th class="r">Après</th><th>Résultat</th></tr></thead>
    <tbody>${L.map(l=>`<tr class="${l.cls||''}"><td>${esc(l.lib)}${l.inchange?' <span class="st na">(inchangé)</span>':''}</td>
      <td class="r av">${l.av==null?'—':money(l.av)}</td><td class="r ap">${l.ap==null?'—':money(l.ap)}</td>
      <td><span class="st ${l.st}">${esc(l.txt)}</span></td></tr>`).join('')}</tbody></table>
    <div class="pxnote">${ko?`<b>Un prix est sous le plancher.</b> Le plancher, c'est le prix d'achat plus ${REG.margeMin||0} % de marge minimum,
      commission du canal comprise. Corrige-le dans la fiche : rien n'est enregistré tant qu'il est là.`
      :`<b>Vérifie les marges avant de valider.</b> La marge nette tient compte de la commission de chaque canal.
      Une fois enregistré, chaque prix part au journal avec ton nom, la date et l'heure.`}</div>`;
  $('pxok').disabled=ko; $('pxmsg').textContent=ko?'enregistrement bloqué':'';
  $('pxov').classList.add('on');
}
$('pxx').onclick=$('pxc').onclick=()=>$('pxov').classList.remove('on');
$('pxok').onclick=()=>{ $('pxov').classList.remove('on'); enregistreFiche(); };

$('dok').onclick=()=>{
  const b=FICHE.brouillon;
  const prixChg=['pa','pvw','pvr'].some(k=>b[k]!==undefined)||b.pc!==undefined;
  if(prixChg){ confirmePrix(lignesPrix()); return; }
  enregistreFiche();
};
function enregistreFiche(){
  const id=FICHE.id;
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
}
$('dann').onclick=()=>{ FICHE.brouillon={};
  FICHE.frn=(MOD[FICHE.id]&&MOD[FICHE.id].frn)?JSON.parse(JSON.stringify(MOD[FICHE.id].frn)):[];
  dessineFiche(); };
$('ddx').onclick=fermeFiche; $('dov').onclick=fermeFiche;
$('dprev').onclick=()=>{ if(FICHE.pos>0){FICHE.pos--;FICHE.brouillon={};
  FICHE.frn=(MOD[cur[FICHE.pos].id]&&MOD[cur[FICHE.pos].id].frn)?JSON.parse(JSON.stringify(MOD[cur[FICHE.pos].id].frn)):[];
  dessineFiche();} };
$('dnext').onclick=()=>{ if(FICHE.pos<cur.length-1){FICHE.pos++;FICHE.brouillon={};
  FICHE.frn=(MOD[cur[FICHE.pos].id]&&MOD[cur[FICHE.pos].id].frn)?JSON.parse(JSON.stringify(MOD[cur[FICHE.pos].id].frn)):[];
  dessineFiche();} };
document.addEventListener('keydown',e=>{
  /* une fenêtre ouverte se ferme la première : Échap ne doit pas fermer la fiche
     dessous et laisser la fenêtre orpheline */
  if(e.key==='Escape'){
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
{ const q0=new URLSearchParams(location.search).get('q'); if(q0){ $('q').value=q0; $('fs').value=''; render(); } }
$('advb').onclick=()=>{
  const o=$('adv').classList.toggle('on');
  $('advb').classList.toggle('on',o); $('advb').setAttribute('aria-expanded',o);
};

const LIB={fb:'Marque',fg:'Genre',ft:'Type',fan:'Prix',fp:'Photo',fx:'Fiches',fo:'Tri'};
const txtOpt=id=>{const e=$(id),o=e.options[e.selectedIndex];return o?o.textContent.trim():'';};

function majBarre(){
  const q=$('q').value.trim();
  $('srch').classList.toggle('has',!!q);

  // état visuel des listes
  ['fb','fg','ft','fan','fp','fx'].forEach(id=>{
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
  ['fb','fg','ft','fan','fp','fx'].forEach(id=>{ if($(id).value!=='') ch.push([id,LIB[id],txtOpt(id)]); });
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
    $('q').value=''; ['fb','fg','ft','fan','fp','fx'].forEach(i=>$(i).value='');
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
const K_PC='inventaire-local-pc-v1', K_TEST='testeurs-pc-v1';
function pcClef(p){ return p.bc ? String(p.bc).replace(/^0+/,'') : 'n-'+((p.marque||'')+(p.nom||'')+(p.ml||'')).toLowerCase().replace(/[^a-z0-9]/g,''); }
function pcTesteurs(){ const t=lit(K_TEST,{}); return (t&&typeof t==='object'&&!Array.isArray(t))?t:{}; }
function pcLignes(){ let r=null; try{ r=JSON.parse(localStorage.getItem(K_PC)||'null'); }catch(e){}
  return Array.isArray(r)?r:null; }
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
      <div><b>${nf(r.t)}</b><span class="k">en vitrine (testeur)</span></div>
      <div><b>${nf(n)}</b><span class="k">flacons livrés</span></div>
    </div>
    <label class="sw"><input type="checkbox" id="ajpct" ${r.t?'checked':''}>
      <span>Un flacon part en vitrine comme testeur${r.deja?' — <b>attention : la boutique en a déjà un</b> pour cette référence'
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
  try{ localStorage.setItem(K_PC,JSON.stringify(rows)); }catch(e){ return false; }
  if(r.t){ const T=pcTesteurs();
    T[r.k]=Object.assign({},T[r.k]||{},{n:(+(T[r.k]&&T[r.k].n||0))+r.t,
      bc:p.bc||'', ref:((p.marque||'')+' '+(p.nom||'')).trim(),
      t:new Date().toISOString(), u:USR||'(non renseigné)'});
    ecrit(K_TEST,T); }
  return true;
}
function paEff2(p){ const m=MOD[p.id]||{}; return m.pa!=null?+m.pa:(p.pa!=null?+p.pa:null); }

let AJC={p:null,motif:null};
function ouvreAjust(p){
  AJC={p,motif:null,pcT:null};
  const bpc=$('ajpc'); if(bpc){ bpc.hidden=true; bpc.innerHTML=''; }
  $('ajp').innerHTML=`<div><b>${esc(p.marque||'')} ${esc(p.nom||'')}</b>
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
      ${m.id==='pcity'&&AJC.pc?`<br>Chez Perfume City : <b>${nf(AJC.pc.vend)}</b> en vente${AJC.pc.t?` et <b>${nf(AJC.pc.t)}</b> en vitrine`:''}.`:''}
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
  if(m.id==='pcity'){
    const r=pcRepartit(p,AJC.n,AJC.pcT);
    if(pcDepose(p,r)) suitePC=' — Perfume City : '+r.vend+' en vente'+(r.t?', '+r.t+' en vitrine':'');
    else $('ajmsg').textContent='inventaire Perfume City non mis à jour (mémoire du navigateur pleine)';
  }
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
    <div class="t"><b>${esc(p.marque||'')} ${esc(p.nom||'')}</b><span>${esc(p.ml||'')} ${p.ml?'oz · ':''}${esc(p.bc||'sans code-barres')} · stock ${nf(p.qte)} · achat actuel ${p.pa!=null?money(p.pa):'—'}</span></div>
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
  res.innerHTML=L.length?L.map(p=>`<div data-id="${p.id}"><b>${esc(p.marque||'')} ${esc(p.nom||'')}</b><span>${esc(p.ml||'')}${p.ml?' oz · ':''}${esc(p.bc||'')} · stock ${nf(p.qte)}</span></div>`).join('')
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
  const cand=[bc, bc.replace(/^0+/,''), bc.padStart(12,'0'), bc.padStart(13,'0')];
  for(const c of cand){ const p=T.find(x=>x.bc===c); if(p) return p; }
  const nu=bc.replace(/^0+/,'');
  return T.find(x=>x.bc && x.bc.replace(/^0+/,'')===nu) || T.find(x=>x.bcs && bcsDe(x).includes(nu)) || null;
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
    return `<tr><td class="ref"><b>${esc(p.marque)} ${esc(p.nom)}</b><span>${p.bc}</span></td>
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
    if(!confirm(`Restaurer la sauvegarde du ${dd.toLocaleDateString('fr-FR')} à `+
      `${dd.toLocaleTimeString('fr-FR',{hour:'2-digit',minute:'2-digit'})}`+
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

function normBC(v){
  const d=String(v==null?'':v).replace(/[^0-9]/g,'');
  return (d.length>=8&&d.length<=14)?d:'';
}

function analyseStock(txt){
  const L=decoupe(txt);
  if(L.length<2) return {err:"Il faut au moins une ligne d'en-tête et une ligne de données."};
  const nc=Math.max(...L.map(r=>r.length));
  const corps=L.slice(1);
  const INDEX={}; P.forEach(p=>INDEX[p.bc]=p);

  /* colonne code-barres : celle qui reconnaît le plus de références de l'inventaire */
  let cbc=-1, meilleur=0;
  for(let c=0;c<nc;c++){
    let n=0;
    for(const r of corps){ const b=normBC(r[c]); if(b&&INDEX[b]) n++; }
    if(n>meilleur){ meilleur=n; cbc=c; }
  }
  if(cbc<0||meilleur<3) return {err:"Aucune colonne de codes-barres reconnue. Le tableau doit contenir une colonne de codes-barres correspondant à l'inventaire."};

  /* colonne quantité : entiers, jamais un code-barres, et dont l'écart total
     avec l'inventaire est le plus faible — c'est ce qui la distingue d'une colonne de prix */
  let cq=-1, best=Infinity;
  for(let c=0;c<nc;c++){
    if(c===cbc) continue;
    let n=0, ecart=0, gros=0;
    for(const r of corps){
      const b=normBC(r[cbc]); if(!b||!INDEX[b]) continue;
      const v=nombre(r[c]);
      if(v==null||v<0||!Number.isInteger(v)) continue;
      if(v>100000){ gros++; continue; }
      n++; ecart+=Math.abs(v-(INDEX[b].qte||0));
    }
    if(n<3||gros>n) continue;
    const moy=ecart/n;
    if(moy<best){ best=moy; cq=c; }
  }
  if(cq<0) return {err:"Aucune colonne de quantités trouvée. Il faut une colonne de nombres entiers."};

  const ent=L[0];
  const res={colBC:ent[cbc]||('colonne '+(cbc+1)), colQ:ent[cq]||('colonne '+(cq+1)),
             lignes:corps.length, connues:0, inconnues:[], change:[], egales:0, doublons:0, q:{}};
  const vu={};
  for(const r of corps){
    const b=normBC(r[cbc]); if(!b) continue;
    const p=INDEX[b];
    if(!p){ if(res.inconnues.length<40) res.inconnues.push(b); continue; }
    const v=nombre(r[cq]);
    if(v==null||v<0||!Number.isInteger(v)) continue;
    if(vu[b]!==undefined){ res.doublons++; }
    vu[b]=true;
    res.connues++;
    res.q[b]=v;
    const av=p.qte||0;
    if(v===av) res.egales++;
    else res.change.push({bc:b,nom:p.nom,marque:p.marque,av,ap:v,d:v-av,
                          val:(v-av)*(p.pa||0)});
  }
  res.change.sort((a,b)=>Math.abs(b.val)-Math.abs(a.val));
  res.impact=res.change.reduce((a,c)=>a+c.val,0);
  res.absents=P.filter(p=>p.qte>0 && res.q[p.bc]===undefined);
  res.perdusMod=Object.keys(MOD).filter(id=>{
    if(MOD[id].qte===undefined) return false;
    const p=P.find(x=>x.id===id); return p && res.q[p.bc]!==undefined && res.q[p.bc]!==MOD[id].qte;
  }).length;
  return res;
}

function dessineMJ(r){
  const box=$('mjres');
  if(r.err){ box.innerHTML=`<div class="mjw">${esc(r.err)}</div>`; $('mjok').disabled=true; MJ=null; return; }
  MJ=r;
  const li=r.change.slice(0,15).map(c=>`<tr>
    <td><b>${esc(c.marque)}</b><br><span style="color:var(--ink-3)">${esc(c.nom)}</span></td>
    <td class="n">${c.av}</td>
    <td class="n ${c.d>0?'up':'dn'}">${c.d>0?'+':'−'}${Math.abs(c.d)}</td>
    <td class="n">${c.ap}</td>
    <td class="n ${c.val>0?'up':'dn'}">${c.val?money(c.val):'—'}</td></tr>`).join('');
  box.innerHTML=`
  <div class="mjmap">Colonne code-barres reconnue : <b>${esc(r.colBC)}</b> ·
    colonne quantité : <b>${esc(r.colQ)}</b></div>
  <div class="mjk" style="margin-top:12px">
    <div><span class="v">${nf(r.connues)}</span><span class="k">références reconnues</span></div>
    <div><span class="v" style="color:var(--iris)">${nf(r.change.length)}</span><span class="k">quantités modifiées</span></div>
    <div><span class="v">${nf(r.egales)}</span><span class="k">inchangées</span></div>
    <div><span class="v" style="color:${r.impact>=0?'var(--good)':'var(--crit)'}">${r.impact?money(r.impact):'0 $'}</span><span class="k">effet sur la valeur du stock</span></div>
  </div>
  ${r.inconnues.length?`<div class="mjw" style="margin-top:12px"><b>${nf(r.inconnues.length)}${r.inconnues.length>=40?'+':''} code${r.inconnues.length>1?'s':''}-barres absent${r.inconnues.length>1?'s':''} de l'inventaire</b> — ces lignes seront ignorées.
    Ce sont soit de nouvelles références à créer, soit des codes mal saisis :
    <span class="mono" style="font-size:11.5px">${r.inconnues.slice(0,6).map(esc).join(', ')}${r.inconnues.length>6?'…':''}</span></div>`:''}
  ${r.absents.length?`<div class="mjw" style="margin-top:12px"><b>${nf(r.absents.length)} référence${r.absents.length>1?'s':''} en stock ici mais absente${r.absents.length>1?'s':''} du tableau collé.</b>
    Leur quantité n'est <b>pas</b> remise à zéro — le tableau est peut-être partiel. Si le Sheet est censé être complet, ces références sont écoulées et il faut les passer à zéro à la main.</div>`:''}
  ${r.doublons?`<div class="mjw" style="margin-top:12px"><b>${nf(r.doublons)} code${r.doublons>1?'s':''}-barres en double</b> dans le tableau — c'est la dernière ligne qui l'emporte.</div>`:''}
  ${r.perdusMod?`<div class="mjw" style="margin-top:12px"><b>${nf(r.perdusMod)} quantité${r.perdusMod>1?'s':''} que tu avais corrigée${r.perdusMod>1?'s':''} à la main</b> ${r.perdusMod>1?'seront remplacées':'sera remplacée'} par la valeur du tableau. Le tableau fait foi.</div>`:''}
  ${r.change.length?`<h3 style="font-family:Inter,sans-serif;font-size:9.5px;letter-spacing:.14em;
    text-transform:uppercase;color:var(--ink-2);font-weight:700;margin:18px 0 8px">
    Les ${Math.min(15,r.change.length)} plus gros mouvements${r.change.length>15?` sur ${nf(r.change.length)}`:''}</h3>
   <div style="overflow-x:auto"><table class="mjt"><thead><tr>
    <th>Référence</th><th style="text-align:right">Avant</th><th style="text-align:right">Écart</th>
    <th style="text-align:right">Après</th><th style="text-align:right">Valeur</th></tr></thead>
    <tbody>${li}</tbody></table></div>`:'<div class="mjw" style="margin-top:12px">Aucune quantité ne change : le tableau est identique à l\'inventaire actuel.</div>'}`;
  $('mjok').disabled = !r.change.length;
  $('mjok').textContent = r.change.length?`Appliquer ${nf(r.change.length)} changement${r.change.length>1?'s':''}`:'Appliquer';
}

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
  EXT={q:MJ.q,date:new Date().toISOString(),src:MJ.colBC+' / '+MJ.colQ};
  log({act:'import',lib:'mise à jour du stock depuis un tableur',
       n:MJ.change.length,impact:Math.round(MJ.impact),
       det:MJ.change.slice(0,600).map(c=>({bc:c.bc,ref:c.marque+' '+c.nom,av:c.av,ap:c.ap}))});
  /* le tableau fait foi : on retire les corrections manuelles de quantite qu'il contredit */
  Object.keys(MOD).forEach(id=>{
    if(MOD[id].qte===undefined) return;
    const p=P.find(x=>x.id===id);
    if(p&&MJ.q[p.bc]!==undefined&&MJ.q[p.bc]!==MOD[id].qte){
      delete MOD[id].qte;
      if(!Object.keys(MOD[id]).length) delete MOD[id];
    }
  });
  sauveEXT(); sauveMOD(); fermeMJ(); render(); majBandeau();
};

function majBandeau(){
  const el=$('extb'); if(!el) return;
  if(!EXT.date){ el.style.display='none'; return; }
  const d=new Date(EXT.date), n=Object.keys(EXT.q).length;
  el.style.display='';
  el.innerHTML=`<span class="mjsrc">stock importé</span>
    <span>${nf(n)} références mises à jour depuis le tableur le
    ${d.toLocaleDateString('fr-FR',{day:'numeric',month:'long'})} à
    ${d.toLocaleTimeString('fr-FR',{hour:'2-digit',minute:'2-digit'})}.</span>
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
  ferme(); $('fx').value='neuf'; render();
  const n=lot.length-doubl;
  if(n===0){ alert(`Aucun article ajouté.\n\nLes ${doubl} ligne${doubl>1?'s':''} correspondent à des codes-barres déjà présents dans le catalogue — ce sont des références que tu as déjà.`); return; }
  alert(`${n} article${n>1?'s':''} ajouté${n>1?'s':''}.`+
    (doubl?`\n${doubl} ignoré${doubl>1?'s':''} : code-barres déjà présent dans le catalogue.`:'')+
    `\n\nIls apparaissent avec une bordure violette et l'étiquette « nouveau ».\nPense à les exporter pour les intégrer au fichier maître.`);
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

majVue();
$('fseuil').value=SEUIL;
$('fseuil').addEventListener('input',()=>{
  const v=parseInt($('fseuil').value,10);
  SEUIL = isNaN(v)?0:Math.max(0,Math.min(999,v));
  REG.seuilQte=SEUIL; sauveREG();
  paint(); majSeuil();
});
render();
majSeuil();
/* catalogue.html#cle=b123… : ouvrir directement une fiche (lien depuis VIP wholesale, Ventes…) */
/* Arrivée depuis l'Inventaire par « Mettre à jour depuis un fichier » :
   la fenêtre d'import s'ouvre toute seule. */
(function(){ if(location.hash!=='#maj') return;
  setTimeout(()=>{ try{ $('maj').click(); }catch(e){} },120); })();

(function(){ const m=location.hash.match(/cle=([^&]+)/); if(!m) return;
  const id=decodeURIComponent(m[1]); const p=tousLesArticles().find(x=>x.id===id); if(!p) return;
  $('fs').value=''; $('q').value=p.bc||p.nom; render(); setTimeout(()=>ouvreFiche(id),60); })();

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
       .replace('__LANGUE__',LANGUE).replace('__LIRE__',_lire.bloc()).replace('__ACCEPT_TAB__',_lire.ACCEPT_TAB)
       .replace('__IDENT__',IDENT)
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
            '__VERSION__':__import__('datetime').datetime.now().strftime('%d/%m/%Y \u00e0 %Hh%M'),
            '__VER__':__import__('datetime').datetime.now().strftime('%Y%m%d%H%M')}.items():
    out=out.replace(k,v)
for i in range(1,10):
    out=out.replace(f'__A{i}__', n(S['an'].get(str(i),0)))
open('catalogue.html','w').write(enligne(out))
import os;print('catalogue.html',round(os.path.getsize('catalogue.html')/1024),'Ko')
