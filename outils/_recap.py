# -*- coding: utf-8 -*-
"""Le récap « Ventes par canal » en tête du tableau de bord.

1er nov. 2026 (Igal : « j'aimerais avoir un tableau récapitulatif du mois dernier avec un graphisme de tous les canaux
de vente par mois… un truc récapitulatif où Sam pourra sélectionner son mois, la période, l'année »).

Ce que ça fait :
  - une barre de périodes (ce mois, mois dernier, 30 jours, 90 jours, cette année, tout) + un menu Mois + un menu Année ;
  - quatre chiffres (chiffre d'affaires, marge nette, flacons, ventes) comparés à la période d'avant ;
  - un tableau canal par canal, avec la part de chacun, et pour Perfume City la part boutique / en ligne ;
  - un graphique en colonnes empilées (par jour sur une période courte, par mois sinon), bascule chiffre d'affaires /
    marge / flacons, infobulle au survol, et les mêmes chiffres dans un tableau dépliable.

Les chiffres sont CEUX DE LA PAGE VENTES : mêmes règles de marge (commission du canal, port encaissé moins coût de
l'envoi sur Amazon et les sites, frais de carte Lightspeed, remboursements en négatif, prix d'achat figé avant la mise
en service). Un test (_test_recap.py) compare canal par canal avec ventes.html. Les commandes reçues mais pas encore
expédiées ne comptent pas : elles ne sont pas des ventes faites.

Pas de camembert : des colonnes et un tableau se comparent mieux que des parts de cercle.
"""

RECAP_CSS = r'''
/* ---- le récap « Ventes par canal » (1er nov. 2026) ---- */
.rc{margin:0 0 30px}
.rc h2.sec{margin-top:0}
.rc-bar{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:0 0 14px}
.rc-chip{font-family:inherit;font-size:13px;font-weight:600;color:var(--ink-2);background:var(--surface);border:1px solid var(--line);
  border-radius:999px;padding:6px 13px;cursor:pointer;line-height:1.2}
.rc-chip:hover{border-color:var(--iris);color:var(--iris)}
.rc-chip.on{background:var(--iris);border-color:var(--iris);color:#fff}
.rc-bar label{font-size:12.5px;color:var(--ink-3);margin-left:6px}
.rc-bar select{font-family:inherit;font-size:13px;color:var(--ink);background:var(--surface);border:1px solid var(--line);border-radius:8px;padding:6px 8px}
.rc-bar select.on{border-color:var(--iris);color:var(--iris);font-weight:600}
.rc .kpis{margin-bottom:18px}
.rc .kpi .e{font-size:12.5px;font-weight:600;margin-top:4px}
.rc .kpi .e.up{color:var(--good)} .rc .kpi .e.dn{color:var(--crit)} .rc .kpi .e.eq{color:var(--ink-3)}
.rc-grid{display:grid;grid-template-columns:minmax(340px,1fr) minmax(340px,1fr);gap:18px;align-items:start}
@media(max-width:900px){.rc-grid{grid-template-columns:1fr}}
.rc-card{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:16px 18px;box-shadow:0 1px 2px rgba(0,0,0,.04);overflow-x:auto;min-width:0}
.rc-card h3{margin:0 0 10px;font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:var(--ink);font-weight:700}
.rc-tab{width:100%;border-collapse:collapse;font-size:13.5px}
.rc-tab th{font-size:10.5px;letter-spacing:.08em;text-transform:uppercase;color:var(--ink-3);font-weight:700;text-align:left;padding:4px 6px 8px;border-bottom:1px solid var(--line)}
.rc-tab td{padding:9px 6px;border-bottom:1px solid var(--line-2);vertical-align:middle}
.rc-tab .r{text-align:right;font-variant-numeric:tabular-nums}
.rc-tab tr.tot td{border-bottom:0;font-weight:700;padding-top:12px}
.rc-tab .nm{font-weight:600;display:flex;align-items:center;gap:8px}
.rc-tab .nm small{display:block;font-weight:400;color:var(--ink-3);font-size:12px;line-height:1.35}
.rc-sw{display:inline-block;width:10px;height:10px;border-radius:3px;background:var(--c);flex:none}
.rc-part{display:flex;align-items:center;gap:6px;justify-content:flex-end;margin-top:3px}
.rc-part i{display:inline-block;height:5px;border-radius:3px;background:var(--c);width:calc(var(--w)*1px);min-width:2px;max-width:60px}
.rc-part b{font-weight:500;font-size:11.5px;font-variant-numeric:tabular-nums;color:var(--ink-3);white-space:nowrap}
.rc-tab td.r{white-space:nowrap}
.rc .neg{color:var(--crit)}
.rc-met{display:flex;gap:6px;margin:0 0 10px;flex-wrap:wrap}
.rc-met .rc-chip{font-size:12.5px;padding:5px 11px}
.rc-pw{display:grid;grid-template-columns:auto 1fr;gap:0 6px}
.rc-y{display:flex;flex-direction:column;justify-content:space-between;font-size:11px;color:var(--ink-3);text-align:right;font-variant-numeric:tabular-nums;height:230px}
.rc-plot{position:relative;height:230px;border-left:0;border-bottom:1px solid var(--line)}
.rc-gl{position:absolute;left:0;right:0;border-top:1px solid var(--line-2);height:0}
.rc-gl.zero{border-top:1px solid var(--ink-3)}
.rc-cols{position:absolute;inset:0;display:flex;align-items:stretch}
.rc-col{flex:1 1 0;position:relative;min-width:0;cursor:default;outline:none}
.rc-col:hover .rc-b,.rc-col:focus .rc-b{filter:brightness(.9)}
.rc-b{position:absolute;left:50%;transform:translateX(-50%);width:62%;max-width:44px;top:0;bottom:0}
.rc-s{position:absolute;left:0;right:0;background:var(--c);border-top:2px solid var(--surface)}
.rc-s.top{border-radius:4px 4px 0 0}
.rc-s.neg{border-top:0;border-bottom:2px solid var(--surface);border-radius:0 0 4px 4px}
.rc-x{display:grid;grid-column:2;font-size:11px;color:var(--ink-3);margin-top:6px}
.rc-x span{text-align:center;overflow:hidden;white-space:nowrap}
.rc-x i{font-style:normal;font-variant-numeric:tabular-nums}
.rc-gl{border-top-style:solid;border-top-color:var(--line-2);opacity:.9}
.rc-leg{display:flex;flex-wrap:wrap;gap:6px 14px;margin:12px 0 0;font-size:12.5px;color:var(--ink-2)}
.rc-leg span{display:inline-flex;align-items:center;gap:6px}
.rc-tip{position:fixed;z-index:50;pointer-events:none;background:var(--ink);color:var(--surface);font-size:12.5px;line-height:1.5;padding:8px 11px;border-radius:8px;box-shadow:0 6px 18px rgba(0,0,0,.18);max-width:260px;display:none}
.rc-tip .t{display:block;font-weight:700;margin-bottom:3px}
.rc-tip div{display:flex;justify-content:space-between;gap:14px}
.rc-tip .tot{border-top:1px solid rgba(255,255,255,.25);margin-top:4px;padding-top:4px;font-weight:700}
.rc-tip .rc-sw{width:8px;height:8px;margin-right:5px}
.rc details{margin-top:12px}
.rc .rc-card details summary{cursor:pointer;color:var(--iris);font-weight:600;font-size:13px;list-style-position:inside}
.rc details table{margin-top:8px}
.rc-note{font-size:12.5px;color:var(--ink-3);margin:14px 0 0;line-height:1.5;max-width:90ch}
.rc .kpis+.rc-inc{margin:-8px 0 18px}
.rc-vide{background:var(--surface);border:1px dashed var(--line);border-radius:12px;padding:22px;color:var(--ink-2);font-size:14px;line-height:1.6}
:root{--rc-c-site:#0072B2;--rc-c-sitegros:#7B52AB;--rc-c-amazon:#009E73;--rc-c-gros:#E69F00;--rc-c-caisse:#D55E00;--rc-c-pc:#E0457F;--rc-c-detail:#5C6B7A;--rc-c-autre:#8C8C8C}
@media(prefers-color-scheme:dark){:root:not([data-theme="light"]){--rc-c-site:#4DA3E0;--rc-c-sitegros:#A98BD8;--rc-c-amazon:#2EC49B;--rc-c-gros:#F2B641;--rc-c-caisse:#F08A4B;--rc-c-pc:#F06A9C;--rc-c-detail:#9AA7B5;--rc-c-autre:#A6A6A6}}
:root[data-theme="dark"]{--rc-c-site:#4DA3E0;--rc-c-sitegros:#A98BD8;--rc-c-amazon:#2EC49B;--rc-c-gros:#F2B641;--rc-c-caisse:#F08A4B;--rc-c-pc:#F06A9C;--rc-c-detail:#9AA7B5;--rc-c-autre:#A6A6A6}
'''

GA_CSS = r'''
/* ---- les cartes « à la Google Analytics » (9 nov. 2026) : Tableau de bord et Analytique ---- */
:root{--an-1:#2a78d6;--an-2:#eb6834;--an-3:#1baf7a;--an-4:#eda100;--an-5:#e87ba4;--an-6:#008300;--an-7:#6250d6;--an-0:#a3a29b;--ga-prec:#9aa0a6}
@media(prefers-color-scheme:dark){:root:not([data-theme="light"]){--an-1:#3987e5;--an-2:#d95926;--an-3:#199e70;--an-4:#c98500;--an-5:#d55181;--an-6:#008300;--an-7:#9085e9;--an-0:#6e6d66;--ga-prec:#80868b}}
:root[data-theme="dark"]{--an-1:#3987e5;--an-2:#d95926;--an-3:#199e70;--an-4:#c98500;--an-5:#d55181;--an-6:#008300;--an-7:#9085e9;--an-0:#6e6d66;--ga-prec:#80868b}
.an-alerte{background:var(--warn-soft);color:var(--warn);border-radius:10px;padding:10px 13px;font-size:13px;margin:0 0 16px;line-height:1.5}
.neg{color:var(--crit)}
.ga-top{display:flex;flex-wrap:wrap;gap:10px 16px;align-items:center;justify-content:space-between;margin:2px 0 8px}
.ga-seg{display:inline-flex;flex-wrap:wrap;background:var(--surface);border:1px solid var(--line);border-radius:999px;padding:3px;gap:2px}
.ga-seg button{font:inherit;font-size:13px;font-weight:600;color:var(--ink-2);background:none;border:0;border-radius:999px;padding:6px 13px;cursor:pointer;transition:background .2s,color .2s}
.ga-seg button:hover{color:var(--an-1)}
.ga-seg button.on{background:var(--an-1);color:#fff}
.ga-per{font-size:13px;color:var(--ink-3);margin:6px 2px 16px}
.ga-per b{color:var(--ink-2);font-weight:600}
.ga-card{background:var(--surface);border:1px solid var(--line);border-radius:14px;box-shadow:0 1px 2px rgba(0,0,0,.04),0 4px 14px rgba(0,0,0,.03);margin:0 0 18px;overflow:hidden;min-width:0;animation:gaIn .5s ease both}
.ga-pad{padding:18px 20px}
@keyframes gaIn{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}
.ga-duo .ga-card:nth-child(2){animation-delay:.08s}
@media(prefers-reduced-motion:reduce){.ga-card{animation:none}}
.ga-tabs{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));border-bottom:1px solid var(--line)}
@media(max-width:760px){.ga-tabs{grid-template-columns:repeat(2,minmax(0,1fr))}}
.ga-tab{font:inherit;text-align:left;background:none;border:0;border-top:3px solid transparent;border-right:1px solid var(--line-2);padding:14px 18px 15px;cursor:pointer;display:flex;flex-direction:column;gap:5px;min-width:0;transition:background .2s}
.ga-tab:last-child{border-right:0}
.ga-tab:hover{background:var(--surface-2)}
.ga-tab.on{border-top-color:var(--an-1);background:color-mix(in srgb,var(--an-1) 6%,var(--surface))}
.ga-tl{font-size:12.5px;color:var(--ink-3);font-weight:600;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.ga-tab.on .ga-tl{color:var(--an-1)}
.ga-tv{font-size:28px;font-weight:600;letter-spacing:-.02em;line-height:1.1;color:var(--ink);font-variant-numeric:tabular-nums}
.ga-d{font-size:12.5px;font-weight:700;font-variant-numeric:tabular-nums}
.ga-d.up{color:#188038}.ga-d.dn{color:#d93025}.ga-d.eq{color:var(--ink-3)}
@media(prefers-color-scheme:dark){:root:not([data-theme="light"]) .ga-d.up{color:#81c995}:root:not([data-theme="light"]) .ga-d.dn{color:#f28b82}}
:root[data-theme="dark"] .ga-d.up{color:#81c995}:root[data-theme="dark"] .ga-d.dn{color:#f28b82}
.ga-plot{position:relative;padding:12px 8px 0 4px;min-height:270px}
.ga-plot2{min-height:210px;padding:4px 0 0}
.ga-svg{display:block;max-width:100%;overflow:visible}
.ga-gl{stroke:var(--line-2);stroke-width:1}
.ga-gl.z{stroke:var(--line)}
.ga-yl,.ga-xl{fill:var(--ink-3);font-size:11.5px;font-family:inherit;font-variant-numeric:tabular-nums}
.ga-l{fill:none;stroke-width:2.6;stroke-linejoin:round;stroke-linecap:round}
.ga-l.prec{stroke-width:1.8;stroke-dasharray:5 5}
.ga-vx{stroke:var(--ink-3);stroke-width:1;stroke-dasharray:3 3}
.ga-pt{stroke:var(--surface);stroke-width:2.5}
.ga-fin{stroke:var(--surface);stroke-width:2}
.ga-zone{cursor:crosshair}
.ga-leg{display:flex;gap:18px;flex-wrap:wrap;padding:6px 20px 16px;font-size:12.5px;color:var(--ink-3)}
.ga-leg span{display:inline-flex;align-items:center;gap:7px}
.ga-li{display:inline-block;width:18px;height:0;border-top:2.6px solid var(--an-1);border-radius:2px}
.ga-li.prec{border-top:2px dashed var(--ga-prec)}
.ga-labs{display:flex;gap:18px;flex-wrap:wrap;margin:4px 0 0;font-size:12.5px;color:var(--ink-2)}
.ga-lab{display:inline-flex;align-items:center;gap:7px}.ga-lab i{width:10px;height:10px;border-radius:50%;background:var(--c)}
.ga-tip{position:fixed;z-index:60;pointer-events:none;background:var(--surface);color:var(--ink);border:1px solid var(--line);font-size:12.5px;line-height:1.5;padding:9px 12px;border-radius:10px;box-shadow:0 8px 24px rgba(0,0,0,.16);min-width:170px;display:none}
.ga-tip>b{display:block;margin-bottom:4px;font-size:12px;color:var(--ink-3);font-weight:600}
.ga-tip div{display:flex;justify-content:space-between;gap:16px;align-items:center}
.ga-tip div span{display:inline-flex;align-items:center;gap:7px;color:var(--ink-2)}
.ga-tip div i{width:9px;height:9px;border-radius:50%}
.ga-tip div b{font-variant-numeric:tabular-nums}
.ga-duo{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:18px;align-items:start}
@media(max-width:1050px){.ga-duo{grid-template-columns:1fr}}
.ga-duo .ga-card{margin:0 0 18px}
.ga-h{display:flex;justify-content:space-between;align-items:center;gap:10px;flex-wrap:wrap;margin:0 0 14px}
.ga-h h3{margin:0;font-size:15.5px;font-weight:600;letter-spacing:-.01em;color:var(--ink)}
.ga-src{font-size:12.5px;color:var(--ink-3)}
.ga-mini{display:inline-flex;background:var(--surface-2);border-radius:8px;padding:2px}
.ga-mini button{font:inherit;font-size:12px;font-weight:600;color:var(--ink-3);background:none;border:0;border-radius:6px;padding:5px 10px;cursor:pointer}
.ga-mini button.on{background:var(--surface);color:var(--an-1);box-shadow:0 1px 2px rgba(0,0,0,.08)}
.ga-bars{display:flex;flex-direction:column;gap:13px}
.ga-bar{display:grid;grid-template-columns:minmax(120px,34%) minmax(0,1fr) auto;gap:12px;align-items:center}
.ga-bn{display:flex;align-items:flex-start;gap:9px;font-size:13.5px;font-weight:600;color:var(--ink);min-width:0}
.ga-bn i{width:10px;height:10px;border-radius:50%;flex:none;margin-top:4px}
.ga-bn span{min-width:0}
.ga-bnm{display:inline-flex;align-items:center;gap:6px}
.ga-i{font:italic 700 11px Georgia,'Times New Roman',serif;width:17px;height:17px;border-radius:50%;border:1px solid var(--line);background:var(--surface);color:var(--ink-3);display:inline-flex;align-items:center;justify-content:center;padding:0;cursor:help;flex:none;transition:all .15s}
.ga-i:hover,.ga-i:focus{background:var(--an-1);border-color:var(--an-1);color:#fff;outline:none}
.ga-info{position:fixed;z-index:70;max-width:290px;background:var(--ink);color:var(--surface);font-size:12.5px;line-height:1.5;padding:9px 12px;border-radius:9px;box-shadow:0 8px 24px rgba(0,0,0,.2);display:none;pointer-events:none}
.ga-bn small{display:block;font-weight:400;font-size:11.5px;color:var(--ink-3);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.ga-bt{height:10px;background:var(--surface-2);border-radius:999px;overflow:hidden}
.ga-bf{height:100%;width:var(--w);border-radius:999px;transition:width .9s cubic-bezier(.2,.7,.2,1)}
.ga-bv{text-align:right;font-size:14px;font-weight:700;font-variant-numeric:tabular-nums;min-width:132px}
.ga-u{font-size:11.5px;font-weight:500;color:var(--ink-3)}
.ga-vs{font-weight:500;color:var(--ink-3)}
.ga-bv small{display:block;font-size:11.5px;font-weight:500;color:var(--ink-3)}
.ga-bv small .ga-d{font-size:11.5px}
.ga-verdict{display:flex;align-items:baseline;gap:12px;flex-wrap:wrap;padding:12px 14px;border-radius:12px;margin:0 0 6px}
.ga-verdict.bon{background:color-mix(in srgb,#188038 9%,transparent)}.ga-verdict.mal{background:color-mix(in srgb,#d93025 9%,transparent)}
.ga-vv{font-size:30px;font-weight:700;letter-spacing:-.02em;font-variant-numeric:tabular-nums}
.ga-verdict.bon .ga-vv{color:#188038}.ga-verdict.mal .ga-vv{color:#d93025}
.ga-vt{font-size:13.5px;color:var(--ink-2);line-height:1.4;flex:1 1 220px}
.ga-stats{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px;margin:14px 0 0}
@media(max-width:560px){.ga-stats{grid-template-columns:1fr}}
.ga-stats div{background:var(--surface-2);border-radius:10px;padding:10px 12px;display:flex;flex-direction:column;gap:3px;min-width:0}
.ga-stats span{font-size:11.5px;color:var(--ink-3);line-height:1.3}
.ga-stats b{font-size:16px;font-variant-numeric:tabular-nums}
.ga-stats small{font-size:11px;color:var(--ink-3)}
.ga-attente{margin:12px 0 0;padding:9px 12px;border-radius:10px;background:var(--surface-2);font-size:13px;color:var(--ink-2);line-height:1.45}.ga-attente span{color:var(--ink-3)}
.ga-stats4{grid-template-columns:repeat(4,minmax(0,1fr))}@media(max-width:900px){.ga-stats4{grid-template-columns:repeat(2,minmax(0,1fr))}}
.ga-st2{font-size:12px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:var(--ink-3);margin:18px 0 6px}
.ga-pp{display:flex;flex-direction:column}
.ga-ppr{display:grid;grid-template-columns:minmax(0,1fr) 90px 120px 90px;gap:10px;align-items:center;padding:8px 2px;border-bottom:1px solid var(--line-2)}
.ga-ppr:last-child{border-bottom:0}
.ga-ppn b{display:block;font-size:13.5px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.ga-ppn small{font-size:11.5px;color:var(--ink-3)}
.ga-ppv{text-align:right;font-size:13.5px;font-weight:600;font-variant-numeric:tabular-nums}.ga-ppv small{display:block;font-size:10.5px;font-weight:500;color:var(--ink-3)}
.ga-ppv.neg{color:#d93025}
.ga-actions{display:flex;align-items:center;gap:12px;flex-wrap:wrap;margin:14px 0 4px;font-size:12.5px;color:var(--ink-3)}
.ga-btn{font:inherit;font-size:13px;font-weight:600;color:#fff;background:var(--an-1);border:0;border-radius:999px;padding:9px 16px;cursor:pointer}
.ga-btn:hover{filter:brightness(.95)}
.ga-expl{margin:16px 0 0;padding:14px 16px;border-radius:12px;background:color-mix(in srgb,var(--an-1) 6%,var(--surface));border:1px solid color-mix(in srgb,var(--an-1) 18%,transparent);font-size:13.5px;line-height:1.55;color:var(--ink-2)}
.ga-expl>b{display:block;font-size:14.5px;color:var(--ink);margin-bottom:4px}
.ga-expl p{margin:6px 0}.ga-expl ul{margin:6px 0;padding-left:18px}.ga-expl li{margin:3px 0}.ga-expl li b,.ga-expl p b{color:var(--ink)}
.ga-prud{font-size:12.5px;color:var(--ink-3)}
.ga-calc{margin:10px 0 0}.ga-calc summary{cursor:pointer;font-size:12.5px;font-weight:600;color:var(--an-1)}
.ga-free{margin:12px 0 0;font-size:12.5px;color:var(--ink-2);line-height:1.5}
.ga-free.ko span{color:#d93025}
.ga-top10{display:flex;flex-direction:column}
.ga-pf{display:grid;grid-template-columns:26px minmax(0,1.3fr) minmax(60px,1fr) auto;gap:12px;align-items:center;padding:9px 4px;border-bottom:1px solid var(--line-2);color:inherit;text-decoration:none;border-radius:8px}
.ga-pf:last-child{border-bottom:0}.ga-pf:hover{background:var(--surface-2)}
.ga-rk{font-size:12px;font-weight:700;color:var(--ink-3);text-align:center}
.ga-pn b{display:block;font-size:13.5px;font-weight:600;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.ga-pn small{font-size:11.5px;color:var(--ink-3)}
.ga-pb{height:8px;background:var(--surface-2);border-radius:999px;overflow:hidden}
.ga-pb i{display:block;height:100%;width:var(--w);background:var(--an-1);border-radius:999px;transition:width .9s cubic-bezier(.2,.7,.2,1)}
.ga-pv{text-align:right}.ga-pv b{display:block;font-size:13.5px;font-variant-numeric:tabular-nums}.ga-pv small{font-size:11.5px;color:var(--ink-3);white-space:nowrap}
.ga-vide{font-size:13.5px;color:var(--ink-3);margin:6px 0}
.ga-note{font-size:12px;color:var(--ink-3);line-height:1.55;margin:4px 2px 0;max-width:110ch}
'''
RECAP_CSS += GA_CSS
RECAP_CSS += r"""
.rc-ga{margin:0 0 18px}
.ga-ts{font-size:12px;color:var(--ink-3);line-height:1.35}
.ga-tab .e{font-size:12.5px;font-weight:700}
.ga-tab .e.up{color:#188038}.ga-tab .e.dn{color:#d93025}.ga-tab .e.eq{color:var(--ink-3);font-weight:500}
.rc-chs{display:flex;flex-wrap:wrap;gap:6px;padding:4px 20px 14px}
.rc-chs button{font:inherit;font-size:12.5px;font-weight:600;color:var(--ink-2);background:var(--surface);border:1px solid var(--line);border-radius:999px;padding:5px 11px;cursor:pointer;display:inline-flex;align-items:center;gap:7px;transition:all .15s}
.rc-chs button i{width:9px;height:9px;border-radius:50%}
.rc-chs button:hover{border-color:var(--an-1)}
.rc-chs button.on{background:var(--ink);border-color:var(--ink);color:var(--surface)}
.rc-figs{padding:0 20px 16px}
.rc-figs details{margin-top:0}
.ga-tsep{border-top:1px solid var(--line);margin:5px 0 4px}
.rc-card-tab{margin-bottom:6px}
"""

# Le moteur des courbes, partagé par le Tableau de bord et l'Analytique (Igal, 9 nov. 2026 : « je n'aime pas du tout les
# organigrammes… fais-moi quelque chose de plus animé, plus clair, plus professionnel, qui ressemble plus à du Google »).
GA_JS = r'''
/* ============ LES COURBES « À LA GOOGLE » (9 nov. 2026) ============ */
const GA_MOUV=!(window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches);
let gaAnime=true;   /* la première fois et à chaque choix : on anime ; une simple relève du serveur redessine sans rejouer */
const gaPct=(a,b)=>(b==null||Math.abs(b)<0.005)?null:(a-b)/Math.abs(b)*100;
const gaFmt=(f,v)=>f==='$'?money(v):f==='%'?nf(Math.round(v))+' %':nf(Math.round(v));
/* un chiffre qui arrive en comptant */
const gaCnt=(v,f,cls='')=>`<span class="ga-cnt ${cls}" data-v="${v}" data-f="${f}">${gaFmt(f,v)}</span>`;
function gaCompte(z){ if(!GA_MOUV||!gaAnime) return;
  z.querySelectorAll('.ga-cnt').forEach(el=>{ const v=+el.dataset.v, f=el.dataset.f; if(!isFinite(v)) return; const t0=performance.now(), D=750;
    const pas=t=>{ const k=Math.min(1,(t-t0)/D), e=1-Math.pow(1-k,3); el.textContent=gaFmt(f,v*e); if(k<1) requestAnimationFrame(pas); else el.textContent=gaFmt(f,v); };
    requestAnimationFrame(pas); }); }

/* une courbe douce qui ne dépasse jamais ses points (interpolation monotone : pas de creux sous zéro inventé) */
function gaLisse(S){ const n=S.length; if(n<3) return 'M'+S.map(p=>p[0].toFixed(1)+' '+p[1].toFixed(1)).join(' L');
  const dx=[],dy=[],m=[]; for(let i=0;i<n-1;i++){ dx[i]=S[i+1][0]-S[i][0]; dy[i]=S[i+1][1]-S[i][1]; m[i]=dy[i]/(dx[i]||1); }
  const t=[m[0]]; for(let i=1;i<n-1;i++) t[i]=(m[i-1]*m[i]<=0)?0:(3*(dx[i-1]+dx[i]))/((2*dx[i]+dx[i-1])/m[i-1]+(dx[i]+2*dx[i-1])/m[i]); t[n-1]=m[n-2];
  let d='M'+S[0][0].toFixed(1)+' '+S[0][1].toFixed(1);
  for(let i=0;i<n-1;i++){ const h=dx[i]/3; d+=` C${(S[i][0]+h).toFixed(1)} ${(S[i][1]+t[i]*h).toFixed(1)} ${(S[i+1][0]-h).toFixed(1)} ${(S[i+1][1]-t[i+1]*h).toFixed(1)} ${S[i+1][0].toFixed(1)} ${S[i+1][1].toFixed(1)}`; }
  return d; }
/* ---- LA COURBE (SVG dessiné à la largeur réelle de la carte) ----
   series : [{v:[…], c:'var(--an-1)', nom, pointille, aire, etiquette}] ; K : les jours ; f : format des valeurs */
function gaCourbe(el,K,series,f,opt={}){
  if(!el) return; const W=Math.max(320,el.clientWidth||700), H=opt.h||260, g=58, d=opt.droite||16, h0=14, b=30;
  const vals=series.flatMap(s=>s.v.filter(x=>x!=null)); let hi=Math.max(0,...vals), lo=Math.min(0,...vals);
  let pasY=rcNice(Math.max(hi-lo,f==='n'?4:10)/4); if(f==='n') pasY=Math.max(1,Math.ceil(pasY));   /* des commandes : jamais « 2,5 » sur l'axe */ hi=Math.ceil(hi/pasY)*pasY||pasY; lo=Math.floor(lo/pasY)*pasY;
  const n=K.length, x=i=>g+(n<=1?0.5:i/(n-1))*(W-g-d), y=v=>h0+(1-(v-lo)/((hi-lo)||1))*(H-h0-b);
  let svg=`<svg class="ga-svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}" role="img" aria-label="${esc(opt.titre||'')}"><defs>`;
  series.forEach((s,j)=>{ svg+=`<linearGradient id="gaG${opt.id||''}${j}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${s.c}" stop-opacity=".22"/><stop offset="1" stop-color="${s.c}" stop-opacity="0"/></linearGradient>`; });
  svg+='</defs>';
  for(let t=lo;t<=hi+1e-9;t+=pasY){ const yy=y(t).toFixed(1); svg+=`<line class="ga-gl ${Math.abs(t)<1e-9?'z':''}" x1="${g}" x2="${W-d}" y1="${yy}" y2="${yy}"/><text class="ga-yl" x="${g-10}" y="${(+yy+4).toFixed(1)}" text-anchor="end">${esc(gaFmt(f,t))}</text>`; }
  const pasX=Math.max(1,Math.ceil(n/Math.max(2,Math.floor((W-g-d)/72))));
  K.forEach((k,i)=>{ if(i%pasX===0||i===n-1&&n>1&&(n-1)%pasX>pasX/2) svg+=`<text class="ga-xl" x="${x(i).toFixed(1)}" y="${H-8}" text-anchor="middle">${esc(k.court2||k.court)}</text>`; });
  series.slice().reverse().forEach((s,jr)=>{ const j=series.length-1-jr; const pts=s.v.map((v,i)=>v==null?null:[x(i),y(v)]);
    /* une ligne coupée là où il n'y a pas de valeur (la période d'avant plus courte) */
    let dl='', seg=[]; const segs=[]; pts.forEach(p=>{ if(p){ seg.push(p); } else if(seg.length){ segs.push(seg); seg=[]; } }); if(seg.length) segs.push(seg);
    segs.forEach(S=>{ dl+=gaLisse(S); });
    if(s.aire&&segs.length){ const S=segs[0]; const da=gaLisse(S)+` L${S[S.length-1][0].toFixed(1)} ${y(Math.max(lo,0)).toFixed(1)} L${S[0][0].toFixed(1)} ${y(Math.max(lo,0)).toFixed(1)} Z`;
      svg+=`<path class="ga-aire" d="${da}" fill="url(#gaG${opt.id||''}${j})"/>`; }
    svg+=`<path class="ga-l ${s.pointille?'prec':''}" d="${dl}" style="stroke:${s.c}"/>`;
    if(s.etiquette&&segs.length){ const S=segs[segs.length-1], p=S[S.length-1]; svg+=`<circle class="ga-fin" cx="${p[0].toFixed(1)}" cy="${p[1].toFixed(1)}" r="4" style="fill:${s.c}"/>`; } });
  svg+=`<line class="ga-vx" x1="0" x2="0" y1="${h0}" y2="${H-b}" style="display:none"/>`+series.map((s,j)=>`<circle class="ga-pt" data-j="${j}" r="5" style="fill:${s.c};display:none"/>`).join('')
    +`<rect class="ga-zone" x="${g}" y="${h0}" width="${W-g-d}" height="${H-h0-b}" fill="transparent"/></svg>`;
  /* les étiquettes au bout des courbes (Google Ads : « Marge 7 642 $ », « Pub 8 155 $ ») */
  const lab=series.filter(s=>s.etiquette).map(s=>{ const v=[...s.v].reverse().find(z=>z!=null); return v==null?'':`<span class="ga-lab" style="--c:${s.c}"><i></i>${esc(s.nom)} <b>${gaFmt(f,v)}</b></span>`; }).join('');
  el.innerHTML=svg+(lab?`<div class="ga-labs">${lab}</div>`:'');
  /* le dessin : chaque ligne se trace de gauche à droite, l'aire apparaît ensuite */
  if(GA_MOUV&&gaAnime) el.querySelectorAll('.ga-l').forEach(p=>{ const L=p.getTotalLength?p.getTotalLength():0; if(!L) return;
    p.style.strokeDasharray=p.classList.contains('prec')?'5 5':L+' '+L; if(!p.classList.contains('prec')){ p.style.strokeDashoffset=L; p.getBoundingClientRect(); p.style.transition='stroke-dashoffset 1.1s cubic-bezier(.2,.7,.2,1)'; p.style.strokeDashoffset='0'; } else { p.style.opacity='0'; p.style.transition='opacity .6s .5s'; p.getBoundingClientRect(); p.style.opacity='1'; } });
  else el.querySelectorAll('.ga-l.prec').forEach(p=>p.style.strokeDasharray='5 5');
  if(GA_MOUV&&gaAnime) el.querySelectorAll('.ga-aire,.ga-fin,.ga-labs').forEach(a=>{ a.style.opacity='0'; a.getBoundingClientRect(); a.style.transition='opacity .7s .55s'; a.style.opacity='1'; });
  /* le survol : une ligne verticale, un point sur chaque courbe, une bulle */
  const zone=el.querySelector('.ga-zone'), vx=el.querySelector('.ga-vx'), pts=[...el.querySelectorAll('.ga-pt')];
  const bulle=()=>{ let t=document.getElementById('ga-tip'); if(!t){ t=document.createElement('div'); t.id='ga-tip'; t.className='ga-tip'; document.body.appendChild(t); } return t; };
  const montre=ev=>{ const r=zone.getBoundingClientRect(); const fx=(ev.clientX-r.left)/r.width; const i=Math.max(0,Math.min(n-1,Math.round(fx*(n-1))));
    const X=x(i); vx.setAttribute('x1',X); vx.setAttribute('x2',X); vx.style.display='';
    pts.forEach(c=>{ const s=series[+c.dataset.j], v=s.v[i]; if(v==null){ c.style.display='none'; return; } c.setAttribute('cx',X); c.setAttribute('cy',y(v)); c.style.display=''; });
    const t=bulle(); t.innerHTML=`<b>${esc(K[i].lib)}</b>`+series.map(s=>s.v[i]==null?'':`<div><span><i style="background:${s.c}"></i>${esc(s.nomTip||s.nom)}</span><b>${gaFmt(f,s.v[i])}</b></div>`).join('')+(opt.tipPlus?opt.tipPlus(i):'');
    t.style.display='block'; const w=t.offsetWidth; let L=ev.clientX+14; if(L+w>innerWidth-8) L=ev.clientX-w-14; t.style.left=L+'px'; t.style.top=Math.max(8,ev.clientY-t.offsetHeight-12)+'px'; };
  const cache=()=>{ vx.style.display='none'; pts.forEach(c=>c.style.display='none'); const t=document.getElementById('ga-tip'); if(t) t.style.display='none'; };
  zone.addEventListener('mousemove',montre); zone.addEventListener('mouseleave',cache);
}

'''

RECAP_JS = r'''
/*__GA__*/
/* ============ LE RÉCAP « VENTES PAR CANAL » (1er nov. 2026) ============
   Les règles de calcul sont celles de ventes.html (construitV) — recopiées ici parce que les deux pages sont
   fabriquées à part ; _test_recap.py vérifie qu'elles donnent les mêmes chiffres canal par canal. */
const RC_K='tableau-recap-v1';
const RC={sel:'moisdernier',metric:'ca',canal:''};
try{ const r=lit(RC_K,null); if(r&&typeof r==='object'){ if(r.sel) RC.sel=r.sel; if(r.metric) RC.metric=r.metric; } }catch(e){}
function rcSauve(){ try{ ecrit(RC_K,{sel:RC.sel,metric:RC.metric}); }catch(e){} }
/* ---- les canaux, comme dans Ventes ---- */
const RC_CANAUX_DEF=[{id:'site',nom:'Site perfumestrade.com',com:3},{id:'sitegros',nom:'Site wholesale.perfumestrade.com',com:3},
  {id:'amazon',nom:'Amazon',com:15},{id:'perfumecity',nom:'Perfume City',com:3}];
function rcCanauxReg(){ let L=(REG.canaux&&REG.canaux.length?REG.canaux:RC_CANAUX_DEF);
  if((REG.canauxV||0)<2){ L=L.filter(c=>c.id!=='shopify'); if(!L.some(c=>c.id==='sitegros')){ const i=L.findIndex(c=>c.id==='site'); L=L.slice(); L.splice(i>=0?i+1:L.length,0,RC_CANAUX_DEF[1]); } }
  if((REG.canauxV||0)<3) L=L.filter(c=>c.id!=='boutique');
  if(!REG.pcCom3) L=L.map(c=>(c.id==='perfumecity'&&!(+c.com))?Object.assign({},c,{com:3}):c);
  /* 7 nov. 2026 (Igal) : les commissions réelles — sites WooCommerce 2,9 % + 0,30 $ par transaction ; Perfume City boutique 2,5 % + 0,10 $,
     en ligne 2,7 % + 0,30 $ (et 8 $ d'envoi). Valables depuis le début de l'ERP : lues ici tant que Réglages ne les a pas écrites (comV4). */
  if(!REG.comV4) L=L.map(RC_COM_V4);
  return L; }
const RC_COM_V4=(c=>{ if(!c) return c; if(c.id==='site'||c.id==='sitegros') return Object.assign({},c,{com:2.9,fixe:0.3}); if(c.id==='perfumecity') return Object.assign({},c,{com:2.5,fixe:0.1,comLigne:2.7,fixeLigne:0.3}); return c; });
/* la part FIXE par transaction (0,30 $, 0,10 $…), retirée une fois par commande et répartie entre ses lignes */
function rcFixeDe(v){ const c=rcCanauxReg().find(x=>String(x.nom).toLowerCase()===String(v.canal||'').toLowerCase()); if(!c) return 0;
  const f=rcPcEnLigne(v)?(c.fixeLigne!=null&&c.fixeLigne!==''?c.fixeLigne:c.fixe):c.fixe; return (f==null||f===''||isNaN(+f))?0:Math.max(0,+f); }
function rcCom(nom){
  const n=String(nom||'').toLowerCase(); if(!n||n==='(non précisé)') return 0;
  const c=rcCanauxReg().find(x=>String(x.nom).toLowerCase()===n); if(c) return +c.com||0;
  if(n.includes('lightspeed')||n.includes('caisse')||n==='boutique') return 0;
  return 0;
}
/* 7 nov. 2026 (Igal : « Perfume City a deux types de vente sur Shopify, boutique et en ligne ») : la vente EN LIGNE de Perfume
   City a sa propre commission (Réglages, ligne « Perfume City — en ligne », comLigne) et un coût d'envoi par commande
   (REG.envois['shopify-pc'], 0 tant que rien n'est réglé) ; la vente en boutique garde la commission du canal, sans envoi. */
const rcPcCanal=()=>rcCanauxReg().find(c=>c.id==='perfumecity');
const rcPcEnLigne=v=>!!(v&&String(v.auto||'')==='shopify-pc'&&v.ou==='en ligne');
function rcComDe(v){ if(rcPcEnLigne(v)){ const c=rcPcCanal(); if(c&&c.comLigne!=null&&c.comLigne!==''&&!isNaN(+c.comLigne)) return Math.max(0,+c.comLigne); } return rcCom(v.canal); }
const rcEnvoiPc=()=>{ const E=(REG&&REG.envois)||{}; const v=E['shopify-pc']; return (v==null||v===''||isNaN(+v))?(REG.comV4?0:8):Math.max(0,+v); };
const rcPaAct=cle=>{ const m=MOD[cle]; if(m&&m.pa!=null) return +m.pa; const v=(IDX[cle]||[])[3]; return v==null?null:+v; };
const rcCarteTaux=()=>{ const v=REG&&REG.carteLS; return (v==null||v===''||isNaN(+v))?2.6:Math.max(0,+v); };
const rcEnvoi=src=>{ const E=(REG&&REG.envois)||{}; const v=E[src]; return (v==null||v===''||isNaN(+v))?8:Math.max(0,+v); };
let _rcPaie=null, _rcOrig=null;
/* 8 nov. 2026 : le magasin du cockpit (relu chez Shopify) a le dernier mot sur la copie embarquée, sauf correction à la main (corrige) */
function rcPaie(f){ if(!f) return null; const emb=(f.paie&&typeof f.paie==='object')?f.paie:null; if(emb&&emb.corrige) return emb;
  if(f._i){ if(!_rcPaie){ try{ _rcPaie=lit('caisse-paie-v1',{})||{}; }catch(e){ _rcPaie={}; } }
    const p=_rcPaie[String(f._i).replace(/^fa\|/,'')]; if(p&&typeof p==='object') return p; }
  return emb; }
/* 8 nov. 2026 : le port payé par le client d'une commande Perfume City voyage avec son paiement (relu chez Shopify) */
function rcPortDe(f){ if(!f) return undefined; if(f.port!=null) return f.port; if(String(f.auto||'')!=='shopify-pc'||f.retour) return undefined;
  const p=rcPaie(f); return (p&&+p.port>0)?+p.port:undefined; }
function rcOrigineFn(F){ let O={}; try{ O=lit('pc-origine-v1',{})||{}; }catch(e){}
  const parNum={}; F.forEach(g=>{ if(g&&g.auto==='shopify-pc'&&!g.retour){ const o=O[String(g._i||'').replace(/^fa\|/,'')]; if(o) parNum[g.num]=o; } });
  return f=>{ if(!f||f.auto!=='shopify-pc') return ''; const k=String(f._i||'').replace(/^fa\|/,''); return O[k]||parNum[f.num]||''; }; }
/* une ligne par parfum vendu (ou par commande quand l'export en porte le détail), avec sa marge nette */
function rcLignes(){
  _rcPaie=null;
  let F=[]; try{ F=lit(KFACT,[])||[]; }catch(e){ F=FACT; } if(!Array.isArray(F)) F=[];
  const orig=rcOrigineFn(F), L=[];
  const fige=String((REG&&REG.paFigeDepuis)||'2026-10-01');
  F.filter(f=>f&&f.sens==='vente').forEach(f=>{
    const canal=f.canal||'(non précisé)';
    (f.lignes||[]).forEach(l=>{
      const paV=(l.cle&&String(f.d||'')<fige&&rcPaAct(l.cle)!=null)?rcPaAct(l.cle):l.paAv;
      const base={canal,num:f.num,cle:l.cle,pa:paV,fid:f.id,ret:!!f.retour,auto:f.auto||'',portF:rcPortDe(f),paie:rcPaie(f),ou:orig(f)};
      if(l.cmds&&l.cmds.length) l.cmds.forEach(c=>L.push(Object.assign({},base,{d:c.d||f.d,cmd:c.cmd||'',q:c.q||0,p:c.p!=null?c.p:l.p})));
      else L.push(Object.assign({},base,{d:f.d,cmd:'',q:l.q||0,p:l.p}));
    });
  });
  L.forEach(v=>{ v.d=String(v.d||'').slice(0,10); v.mt=(v.q||0)*(v.p||0); v.com=rcComDe(v);
    v.comMt=v.ret?0:v.mt*v.com/100; v.net=v.mt-v.comMt;
    v.mg=(v.pa!=null&&v.p!=null)?(v.net-v.pa*(v.q||0)):null; });
  /* 7 nov. 2026 (Igal : « en quoi il perd de l'argent ? » — un parfum vendu 38,50 $, acheté 29 $, donné « à perte » parce que les
     16,45 $ de frais de carte d'un panier de 616 $ étaient posés sur lui seul). Les frais d'une COMMANDE (port payé par le client,
     8 $ d'envoi, frais de carte de la caisse) sont maintenant répartis entre ses lignes, au prorata du montant de chacune :
     les totaux par canal ne bougent pas, et plus aucun parfum ne porte les frais des autres. */
  rcRepartit(L, v=>{ const src=String(v.auto||''); if(!/^(amazon|woocommerce|woocommerce-gros)$/.test(src)||v.ret) return null; return (v.fid?'f|'+v.fid+'|'+(v.cmd||''):'a|'+src+'|'+v.num); },
    v=>{ const src=String(v.auto||''); let port=v.portF; if(port==null&&/^woocommerce/.test(src)&&typeof faStatutSite==='function'){ const st=faStatutSite(src,v.num); if(st&&+st.port>0) port=+st.port; }
      return {portMt:+port>0?+port:0, envoiMt:rcEnvoi(src)}; },
    (v,x)=>{ v.portMt=x.portMt; v.envoiMt=x.envoiMt; if(v.mg!=null) v.mg+=x.portMt-x.envoiMt; });
  /* la part fixe de la commission, une fois par transaction (commande), répartie entre ses lignes ; comptée dans la commission */
  rcRepartit(L, v=>(!v.ret&&rcFixeDe(v)>0)?(v.fid?'f|'+v.fid+'|'+(v.cmd||''):'a|'+String(v.auto||'')+'|'+v.num):null,
    v=>({fixeMt:rcFixeDe(v)}),
    (v,x)=>{ v.fixeMt=x.fixeMt; v.comMt=Math.round((v.comMt+x.fixeMt)*100)/100; v.net=v.mt-v.comMt; if(v.mg!=null) v.mg-=x.fixeMt; });
  rcRepartit(L, v=>(String(v.auto||'')==='shopify-pc'&&!v.ret&&(rcPcEnLigne(v)&&rcEnvoiPc()>0||+v.portF>0))?'f|'+(v.fid||v.num):null,
    v=>({portMt:+v.portF>0?+v.portF:0, envoiMt:rcPcEnLigne(v)?rcEnvoiPc():0}),
    (v,x)=>{ v.portMt=x.portMt; v.envoiMt=x.envoiMt; if(v.mg!=null) v.mg+=x.portMt-x.envoiMt; });
  rcRepartit(L, v=>(String(v.auto||'')!=='lightspeed'||v.ret||!v.paie||!(+v.paie.carte>0))?null:'f|'+(v.fid||v.num),
    v=>({carteMt:Math.round(+v.paie.carte*rcCarteTaux())/100}),
    (v,x)=>{ v.carteMt=x.carteMt; if(v.mg!=null) v.mg-=x.carteMt; });
  /* 2 nov. 2026 : les ventes en gros d'AVANT l'ERP (tableur de Sam jusqu'au 30 sept. 2026, donnees/histgros.js) comptent
     comme dans la fiche parfum : chiffre d'affaires et flacons, sans marge (le prix d'achat de l'époque est inconnu).
     Elles ne sont pas dans Ventes : le test de parité avec Ventes les laisse de côté (hist). */
  try{ const H=window.D_HG; if(H&&H.l){ Object.keys(H.l).forEach(k=>{ (H.l[k]||[]).forEach(r=>{ if(!r||!r[0]) return;
      const q=+r[2]||0, p=r[3]==null?0:+r[3]; L.push({canal:RC_HG,num:'',cle:null,pa:null,fid:'hg|'+r[0]+'|'+(r[1]||0),ret:false,auto:'',d:String(r[0]).slice(0,10),cmd:'',q,p,mt:q*p,com:0,comMt:0,net:q*p,mg:null,hist:true,client:(H.c||[])[r[1]]||''}); }); }); } }catch(e){}
  return L;
}
/* répartit les frais d'une commande entre ses lignes, au prorata du montant (les lignes sans prix d'achat n'en portent pas,
   sauf s'il n'y en a aucune autre) ; le dernier centime va à la dernière ligne pour que la somme tombe juste */
function rcRepartit(L,cleDe,calc,pose){
  const G=new Map(); L.forEach(v=>{ const k=cleDe(v); if(!k) return; if(!G.has(k)) G.set(k,[]); G.get(k).push(v); });
  G.forEach(gr=>{ const tot=calc(gr[0]); if(!tot) return;
    const avec=gr.filter(v=>v.mg!=null), cible=avec.length?avec:[gr[0]];
    const somme=cible.reduce((a,v)=>a+Math.max(0,v.mt||0),0);
    const parts=cible.map((v,i)=>{ const r=somme>0?Math.max(0,v.mt||0)/somme:1/cible.length; const x={}; Object.keys(tot).forEach(k=>{ x[k]=Math.round(tot[k]*r*100)/100; }); return x; });
    Object.keys(tot).forEach(k=>{ const d=Math.round((tot[k]-parts.reduce((a,x)=>a+x[k],0))*100)/100; parts[parts.length-1][k]=Math.round((parts[parts.length-1][k]+d)*100)/100; });
    cible.forEach((v,i)=>pose(v,parts[i])); });
}
const RC_HG="Vente en gros · avant l'ERP";
/* le premier jour dont les chiffres sont complets sur tous les canaux (mise en service de l'ERP, Amazon compris) */
const RC_COMPLET='2026-10-01';
/* ---- les périodes ---- */
const rcISO=d=>isoJour(d);
function rcPlage(sel){
  const auj=new Date(); const y=auj.getFullYear(), m=auj.getMonth();
  const deb=(Y,M)=>new Date(Y,M,1), fin=(Y,M)=>new Date(Y,M+1,0);
  let s=String(sel||'moisdernier'), mm;
  if(s==='cemois') return {a:rcISO(deb(y,m)),b:rcISO(auj),cour:true};
  if(s==='moisdernier') return {a:rcISO(deb(y,m-1)),b:rcISO(fin(y,m-1))};
  if(s==='cetteannee') return {a:rcISO(deb(y,0)),b:rcISO(auj),cour:true,an:true};
  if(s==='tout') return {a:'0000-01-01',b:'9999-12-31',tout:true};
  if((mm=s.match(/^rel:(\d+)$/))){ const d=new Date(auj); d.setDate(d.getDate()-(+mm[1]-1)); return {a:rcISO(d),b:rcISO(auj),rel:+mm[1]}; }
  if((mm=s.match(/^mois:(\d{4})-(\d{2})$/))){ const Y=+mm[1],M=+mm[2]-1; const c=(Y===y&&M===m); return {a:rcISO(deb(Y,M)),b:c?rcISO(auj):rcISO(fin(Y,M)),cour:c}; }
  if((mm=s.match(/^annee:(\d{4})$/))){ const Y=+mm[1]; const c=(Y===y); return {a:rcISO(deb(Y,0)),b:c?rcISO(auj):rcISO(fin(Y,11)),cour:c,an:true}; }
  return rcPlage('moisdernier');
}
/* la période d'avant, de même longueur : le mois précédent, les N jours d'avant, l'année d'avant (sur le même nombre de jours écoulés) */
function rcPrec(sel,P){
  const s=String(sel||''); let mm;
  const j=x=>{ const [Y,M,D]=x.split('-').map(Number); return new Date(Y,M-1,D); };
  if(P.tout) return null;
  if(s==='cemois'||(mm=s.match(/^mois:(\d{4})-(\d{2})$/))){ const a=j(P.a); const d0=new Date(a.getFullYear(),a.getMonth()-1,1);
    if(P.cour){ const n=Math.round((j(P.b)-a)/86400e3); const d1=new Date(d0); d1.setDate(d1.getDate()+n); const f=new Date(a.getFullYear(),a.getMonth(),0); return {a:rcISO(d0),b:rcISO(d1<f?d1:f)}; }
    return {a:rcISO(d0),b:rcISO(new Date(a.getFullYear(),a.getMonth(),0))}; }
  if(s==='moisdernier'){ const a=j(P.a); return {a:rcISO(new Date(a.getFullYear(),a.getMonth()-1,1)),b:rcISO(new Date(a.getFullYear(),a.getMonth(),0))}; }
  if(s==='cetteannee'||(mm=s.match(/^annee:(\d{4})$/))){ const a=j(P.a), b=j(P.b); return {a:rcISO(new Date(a.getFullYear()-1,0,1)),b:rcISO(new Date(b.getFullYear()-1,b.getMonth(),b.getDate()))}; }
  if(P.rel){ const a=j(P.a); const b1=new Date(a); b1.setDate(b1.getDate()-1); const a1=new Date(b1); a1.setDate(a1.getDate()-(P.rel-1)); return {a:rcISO(a1),b:rcISO(b1)}; }
  return null;
}
const RC_LOC=()=>LANG==='en'?'en-US':LANG==='es'?'es-ES':'fr-FR';
const rcMoisLib=(Y,M)=>new Date(Y,M,1).toLocaleDateString(RC_LOC(),{month:'long',year:'numeric'});   /* « octobre 2026 », « October 2026 », « octubre de 2026 » */
function rcLib(sel,P){
  const s=String(sel||''); let mm;
  if(s==='cemois') return L3('Ce mois','This month','Este mes')+' · '+rcMoisLib(+P.a.slice(0,4),+P.a.slice(5,7)-1);
  if(s==='moisdernier') return L3('Mois dernier','Last month','Mes pasado')+' · '+rcMoisLib(+P.a.slice(0,4),+P.a.slice(5,7)-1);
  if(s==='cetteannee') return L3('Cette année','This year','Este año')+' · '+P.a.slice(0,4);
  if(s==='tout') return L3('Depuis le début','Since the beginning','Desde el principio');
  if((mm=s.match(/^rel:(\d+)$/))) return L3(`${mm[1]} derniers jours`,`Last ${mm[1]} days`,`Últimos ${mm[1]} días`);
  if((mm=s.match(/^mois:(\d{4})-(\d{2})$/))) return rcMoisLib(+mm[1],+mm[2]-1);
  if((mm=s.match(/^annee:(\d{4})$/))) return L3('Année','Year','Año')+' '+mm[1];
  return '';
}
/* 9 nov. 2026 (Igal : « est-ce que c'est par rapport à la date ou au mois complet ? Je veux que ça corresponde au 9 octobre ») :
   la comparaison d'un mois ou d'une année EN COURS se fait déjà jour pour jour (1er–9 nov. contre 1er–9 oct.) ; l'étiquette le dit
   maintenant : « 1–9 oct. 2026 » et non plus « octobre 2026 », qui laissait croire au mois complet */
function rcLibJours(a,b){ const j=x=>{ const [Y,M,D]=x.split('-').map(Number); return new Date(Y,M-1,D); };
  const A=j(a), B=j(b), memeMois=A.getMonth()===B.getMonth()&&A.getFullYear()===B.getFullYear();
  if(memeMois){ const m=B.toLocaleDateString(RC_LOC(),{month:'short',year:'numeric'}); return LANG==='en'?B.toLocaleDateString('en-US',{month:'short'})+' '+A.getDate()+'–'+B.getDate()+', '+B.getFullYear():A.getDate()+'–'+B.getDate()+' '+m; }
  const o={day:'numeric',month:'short'}; return A.toLocaleDateString(RC_LOC(),o)+' – '+B.toLocaleDateString(RC_LOC(),Object.assign({year:'numeric'},o)); }
function rcLibPrec(sel,Q){ const s=String(sel||''); if(!Q) return '';
  const j=x=>{ const [Y,M,D]=x.split('-').map(Number); return new Date(Y,M-1,D); };
  const finMois=x=>{ const d=j(x); return new Date(d.getFullYear(),d.getMonth()+1,0).getDate()===d.getDate(); };
  if(/^(cemois|moisdernier|mois:)/.test(s)) return (Q.a.slice(8)==='01'&&finMois(Q.b))?rcMoisLib(+Q.a.slice(0,4),+Q.a.slice(5,7)-1):rcLibJours(Q.a,Q.b);
  if(/^(cetteannee|annee:)/.test(s)) return (Q.a.slice(5)==='01-01'&&Q.b.slice(5)==='12-31')?Q.a.slice(0,4):rcLibJours(Q.a,Q.b);
  return L3('la période d\'avant','the previous period','el período anterior'); }
/* ---- l'identité d'un canal : une couleur fixe, un nom à l'écran ---- */
function rcId(nom){ const n=String(nom||'').toLowerCase();
  if(/perfume\s*(in\s*the\s*)?city/.test(n)) return 'pc';
  if(n.includes('wholesale')) return 'sitegros';
  if(n.includes('perfumestrade')) return 'site';
  if(n.includes('amazon')) return 'amazon';
  if(n.includes('lightspeed')||n.includes('caisse')) return 'caisse';
  if(n==='gros'||n===RC_HG.toLowerCase()) return 'gros'; if(n==='boutique') return 'detail';
  return 'autre'; }
const rcCoul=n=>`var(--rc-c-${rcId(n)})`;
function rcNomVu(nom){ const n=String(nom||'').toLowerCase();
  if(n==='gros') return L3('Vente en gros','Wholesale sale','Venta mayorista');
  if(n===RC_HG.toLowerCase()) return L3("Vente en gros · avant l'ERP",'Wholesale · before the ERP','Mayorista · antes del ERP');
  if(n==='boutique') return L3('Vente au détail','Retail sale','Venta al detalle');
  if(n==='caisse lightspeed') return L3('Caisse Lightspeed','Lightspeed register','Caja Lightspeed');
  if(n==='(non précisé)') return L3('(non précisé)','(not specified)','(sin precisar)');
  return nom; }
const rcOuLib=o=>o==='boutique'?L3('en boutique','in store','en tienda'):o==='en ligne'?L3('en ligne','online','en línea'):L3('autre','other','otro');
/* ---- l'agrégat d'une période : total, par canal, et pour Perfume City par origine ---- */
function rcAgrege(L,a,b){
  const S=L.filter(v=>v.d>=a&&v.d<=b);
  const G={}, T={ca:0,mg:0,q:0,n:0,nR:0,sansPa:0}; const ventes=new Set(), remb=new Set();
  S.forEach(v=>{ const o=G[v.canal]=G[v.canal]||{canal:v.canal,ca:0,mg:0,q:0,n:0,nR:0,sansPa:0,ou:{},vs:new Set(),rs:new Set()};
    o.ca+=v.mt; T.ca+=v.mt; o.q+=v.q||0; T.q+=v.q||0;
    if(v.mg==null){ if(!v.ret&&!v.hist){ o.sansPa++; T.sansPa++; } if(v.hist){ o.hist=1; } } else { o.mg+=v.mg; T.mg+=v.mg; }
    const k=(v.fid||v.num||'')+'|'+(v.cmd||''); if(v.ret){ o.rs.add(k); remb.add(k); } else { o.vs.add(k); ventes.add(k); }
    if(rcId(v.canal)==='pc'){ const ou=v.ou||''; const z=o.ou[ou]=o.ou[ou]||{ca:0,q:0}; z.ca+=v.mt; z.q+=v.q||0; } });
  Object.values(G).forEach(o=>{ o.n=o.vs.size; o.nR=o.rs.size; delete o.vs; delete o.rs; });
  T.n=ventes.size; T.nR=remb.size;
  return {S,G,T};
}
/* ---- le graphique : une colonne par jour (période ≤ 92 jours) ou par mois ---- */
function rcBuckets(P,S){
  const j=x=>{ const [Y,M,D]=x.split('-').map(Number); return new Date(Y,M-1,D); };
  let a=P.a, b=P.b;
  if(P.tout){ const ds=S.map(v=>v.d).filter(Boolean).sort(); if(!ds.length) return {K:[],jour:false}; a=ds[0]; b=ds[ds.length-1]; }
  /* un mois en cours occupe tout le mois (les jours à venir restent vides), une année en cours ses douze mois :
     deux jours de ventes ne font pas deux colonnes géantes, et le dessin garde la même forme d'un mois à l'autre */
  if(P.cour&&P.an) b=rcISO(new Date(+a.slice(0,4),11,31));
  else if(P.cour) b=rcISO(new Date(+a.slice(0,4),+a.slice(5,7),0));
  const A=j(a), B=j(b); const nJ=Math.round((B-A)/86400e3)+1;
  const K=[];
  if(nJ<=92&&!P.tout&&!P.an){ for(let d=new Date(A);d<=B;d.setDate(d.getDate()+1)){ const k=rcISO(d);
      K.push({k,lib:d.toLocaleDateString(RC_LOC(),{weekday:'short',day:'numeric',month:'short'}),court:String(d.getDate())}); }
    return {K,jour:true}; }
  for(let d=new Date(A.getFullYear(),A.getMonth(),1);d<=B;d.setMonth(d.getMonth()+1)){ const k=rcISO(d).slice(0,7);
    K.push({k,lib:rcMoisLib(d.getFullYear(),d.getMonth()),court:d.toLocaleDateString(RC_LOC(),{month:'short'})+(d.getMonth()===0||K.length===0?' '+String(d.getFullYear()).slice(2):'')}); }
  return {K,jour:false};
}
function rcNice(x){ if(x<=0) return 1; const p=Math.pow(10,Math.floor(Math.log10(x))); const r=x/p; const n=r<=1?1:r<=2?2:r<=2.5?2.5:r<=5?5:10; return n*p; }
const rcFmt=(metric,v)=>metric==='q'?nf(Math.round(v)):money(v);
const rcMetLib=m=>m==='mg'?L3('Marge nette','Net margin','Margen neto'):m==='q'?L3('Flacons','Bottles','Frascos'):L3("Chiffre d'affaires",'Revenue','Facturación');
function rcChart(P,R,ordre,metric){
  const B=rcBuckets(P,R.S); if(!B.K.length) return '';
  const idx={}; B.K.forEach((k,i)=>idx[k.k]=i);
  const cel=B.K.map(()=>({}));
  R.S.forEach(v=>{ const k=B.jour?v.d:v.d.slice(0,7); const i=idx[k]; if(i==null) return;
    const val=metric==='mg'?(v.mg||0):metric==='q'?(v.q||0):v.mt; cel[i][v.canal]=(cel[i][v.canal]||0)+val; });
  let hi=0, lo=0;
  cel.forEach(c=>{ let up=0, dn=0; Object.values(c).forEach(x=>{ if(x>0) up+=x; else dn+=x; }); hi=Math.max(hi,up); lo=Math.min(lo,dn); });
  const pas=rcNice(Math.max(hi,-lo)/4); const top=Math.ceil(hi/pas)*pas||pas, bas=Math.floor(lo/pas)*pas; const tot=top-bas;
  const pc=v=>((v-bas)/tot*100);
  const ticks=[]; for(let t=bas;t<=top+1e-9;t+=pas) ticks.push(t);
  const yl=ticks.slice().reverse().map(t=>`<span>${rcFmt(metric,t)}</span>`).join('');
  const gl=ticks.map(t=>`<i class="rc-gl ${t===0?'zero':''}" style="bottom:${pc(t)}%"></i>`).join('');
  const cols=B.K.map((k,i)=>{ const c=cel[i]; let up=0, dn=0, segs='';
    const arr=ordre.filter(n=>(c[n]||0)!==0), dernierPos=arr.filter(n=>c[n]>0).pop();
    arr.forEach(n=>{ const v=c[n]; const h=Math.abs(v)/tot*100;
      if(v>0){ segs+=`<i class="rc-s ${n===dernierPos?'top':''}" style="--c:${rcCoul(n)};bottom:${pc(0)+up}%;height:${h}%"></i>`; up+=h; }
      else { dn+=h; segs+=`<i class="rc-s neg" style="--c:${rcCoul(n)};bottom:${pc(0)-dn}%;height:${h}%"></i>`; } });
    const tip=`<b class="t" data-nolang>${esc(k.lib)}</b>`+arr.map(n=>`<div><span><i class="rc-sw" style="--c:${rcCoul(n)}"></i><span data-nolang>${esc(rcNomVu(n))}</span></span><b>${rcFmt(metric,c[n])}</b></div>`).join('')
      +(arr.length>1?`<div class="tot"><span>${L3('Total','Total','Total')}</span><b>${rcFmt(metric,arr.reduce((a,n)=>a+c[n],0))}</b></div>`:'');
    const lab=k.lib+L3(' : ',': ',': ')+(arr.length?arr.map(n=>rcNomVu(n)+' '+rcFmt(metric,c[n])).join(', '):L3('rien','nothing','nada'));
    return `<div class="rc-col" tabindex="0" data-i="${i}" data-tip="${esc(tip)}" aria-label="${esc(lab)}"><div class="rc-b">${segs}</div></div>`; }).join('');
  const nX=B.K.length, pasX=B.jour?(nX<=16?1:nX<=31?2:nX<=62?4:7):(nX<=12?1:3);
  const xl=B.K.map((k,i)=>`<span>${i%pasX===0?`<i data-nolang>${esc(k.court)}</i>`:''}</span>`).join('');
  const leg=ordre.filter(n=>R.G[n]).map(n=>`<span><i class="rc-sw" style="--c:${rcCoul(n)}"></i><span data-nolang>${esc(rcNomVu(n))}</span></span>`).join('');
  const figs=`<details><summary>${L3('Voir les chiffres','See the figures','Ver las cifras')}, ${B.jour?L3('jour par jour','day by day','día a día'):L3('mois par mois','month by month','mes a mes')}</summary>
    <table class="rc-tab"><thead><tr><th>${B.jour?L3('Jour','Day','Día'):L3('Mois','Month','Mes')}</th>${ordre.filter(n=>R.G[n]).map(n=>`<th class="r" data-nolang>${esc(rcNomVu(n))}</th>`).join('')}<th class="r">${L3('Total','Total','Total')}</th></tr></thead>
    <tbody>${B.K.map((k,i)=>{ const c=cel[i]; const t=Object.values(c).reduce((a,x)=>a+x,0); if(!Object.keys(c).length) return '';
      return `<tr><td data-nolang>${esc(k.lib)}</td>${ordre.filter(n=>R.G[n]).map(n=>`<td class="r ${c[n]<0?'neg':''}">${c[n]?rcFmt(metric,c[n]):'·'}</td>`).join('')}<td class="r ${t<0?'neg':''}"><b>${rcFmt(metric,t)}</b></td></tr>`; }).join('')}</tbody></table></details>`;
  return `<div class="rc-pw"><div class="rc-y">${yl}</div><div class="rc-plot">${gl}<div class="rc-cols">${cols}</div></div><div class="rc-x" style="grid-template-columns:repeat(${nX},1fr)">${xl}</div></div>
    <div class="rc-leg">${leg}</div>${figs}`;
}
/* ---- tout dessiner ---- */
function rcDessine(){
  const z=document.getElementById('recap'); if(!z) return;
  const L=rcLignes(), P=rcPlage(RC.sel), R=rcAgrege(L,P.a,P.b), Q0=rcPrec(RC.sel,P);
  /* 3 nov. 2026 (Igal) : pas de comparaison quand la période d'avant commence avant RC_COMPLET, parce que ses chiffres
     sont incomplets (septembre 2026 n'a pas les ventes Amazon FBA). Dès novembre, octobre sert de référence et la
     comparaison revient toute seule. Si l'export Amazon de septembre est importé un jour, reculer RC_COMPLET. */
  const Q=(Q0&&Q0.a<RC_COMPLET)?null:Q0, Qinc=(Q0&&!Q)?Q0:null, RP=Q?rcAgrege(L,Q.a,Q.b):null;
  const auj=new Date(); const y=auj.getFullYear(), m=auj.getMonth();
  /* les mois et les années qui ont des ventes, pour les deux menus */
  const moisVus=new Set(L.map(v=>v.d.slice(0,7)).filter(x=>/^\d{4}-\d{2}$/.test(x))); moisVus.add(rcISO(auj).slice(0,7));
  const mois=[...moisVus].sort().reverse(), annees=[...new Set(mois.map(x=>x.slice(0,4)))];
  const chips=[['cemois',L3('Ce mois','This month','Este mes')],['moisdernier',L3('Mois dernier','Last month','Mes pasado')],['rel:30',L3('30 jours','30 days','30 días')],['rel:90',L3('90 jours','90 days','90 días')],['cetteannee',L3('Cette année','This year','Este año')],['tout',L3('Tout','All','Todo')]];
  const selM=/^mois:/.test(RC.sel)?RC.sel:'', selA=/^annee:/.test(RC.sel)?RC.sel:'';
  let h=`<h2 class="sec">${L3('Ventes par canal','Sales by channel','Ventas por canal')} <em data-nolang>${esc(rcLib(RC.sel,P))}</em><a href="ventes.html">${L3('Journal des ventes','Sales log','Diario de ventas')}</a></h2>
    <div class="rc-bar">${chips.map(([v,l])=>`<button type="button" class="rc-chip ${RC.sel===v?'on':''}" data-rc="${v}">${l}</button>`).join('')}
      <label for="rc-mois">${L3('Mois','Month','Mes')}</label><select id="rc-mois" class="${selM?'on':''}"><option value="">—</option>${mois.map(x=>`<option value="mois:${x}" ${selM==='mois:'+x?'selected':''}>${esc(rcMoisLib(+x.slice(0,4),+x.slice(5,7)-1))}</option>`).join('')}</select>
      <label for="rc-an">${L3('Année','Year','Año')}</label><select id="rc-an" class="${selA?'on':''}"><option value="">—</option>${annees.map(x=>`<option value="annee:${x}" ${selA==='annee:'+x?'selected':''}>${x}</option>`).join('')}</select></div>`;
  if(!R.S.length){
    h+=`<div class="rc-vide">${L3('Aucune vente sur cette période.','No sale in this period.','Ninguna venta en este período.')} ${L.length?L3('Choisis une autre période ci-dessus.','Pick another period above.','Elige otro período arriba.'):L3('Dès qu\'une vente est saisie, importée d\'un canal ou facturée, elle apparaît ici.','As soon as a sale is entered, imported from a channel or invoiced, it shows up here.','En cuanto una venta se registra, se importa de un canal o se factura, aparece aquí.')}</div>`;
    z.innerHTML=h; rcBranche(); return;
  }
  const pct=(a,b)=>(b==null||Math.abs(b)<0.005)?null:(a-b)/Math.abs(b)*100;
  const evo=(a,b,fmt)=>{ if(!RP) return ''; const p=pct(a,b); const lib=rcLibPrec(RC.sel,Q); fmt=fmt||money;
    if(p==null) return `<span class="e eq">${L3('rien à comparer','nothing to compare','nada que comparar')} (${esc(lib)})</span>`;
    const s=p>0.5?'up':p<-0.5?'dn':'eq'; const fl=s==='up'?'▲':s==='dn'?'▼':'=';
    /* un pourcentage à cinq chiffres ne dit rien (« +19 511 % » quand le mois d'avant n'avait presque rien) : on donne le chiffre d'avant */
    if(Math.abs(p)>500) return `<span class="e ${s}">${fl} <span data-nolang>${esc(lib)}</span> : ${fmt(b)}</span>`;
    return `<span class="e ${s}">${fl} ${nf(Math.round(Math.abs(p)))} % vs <span data-nolang>${esc(lib)}</span></span>`; };
  const T=R.T, TP=RP?RP.T:null;
  const panier=T.n?T.ca/T.n:null, pctMg=T.ca>0?T.mg/T.ca*100:null;
  /* 9 nov. 2026 (Igal : « je n'aime pas du tout les organigrammes… plus animé, plus clair, plus professionnel, qui ressemble plus
     à du Google ») : les quatre chiffres deviennent les onglets d'une carte ; l'onglet choisi trace sa courbe juste dessous */
  const tabs=[['ca',L3("Chiffre d'affaires",'Revenue','Facturación'),T.ca,'$',L3('remboursements déduits','refunds deducted','reembolsos deducidos'),evo(T.ca,TP&&TP.ca)],
    ['mg',L3('Marge nette','Net margin','Margen neto'),T.mg,'$',(pctMg!=null?nf(Math.round(pctMg*10)/10)+' %':'')+(T.sansPa?' · <span class="neg">'+L3(`${T.sansPa} ligne${T.sansPa>1?'s':''} sans prix d'achat`,`${T.sansPa} line${T.sansPa>1?'s':''} without purchase price`,`${T.sansPa} línea${T.sansPa>1?'s':''} sin precio de compra`)+'</span>':''),evo(T.mg,TP&&TP.mg)],
    ['q',L3('Flacons vendus','Bottles sold','Frascos vendidos'),T.q,'n','',evo(T.q,TP&&TP.q,nf)],
    ['n',L3('Ventes','Sales','Ventas'),T.n,'n',(panier!=null?L3('panier moyen','average basket','cesta media')+' '+money(panier):'')+(T.nR?' · '+nf(T.nR)+' '+L3('remboursement'+(T.nR>1?'s':''),'refund'+(T.nR>1?'s':''),'reembolso'+(T.nR>1?'s':'')):''),evo(T.n,TP&&TP.n,nf)]];
  if(!tabs.some(t=>t[0]===RC.metric)) RC.metric='ca';
  const ordre0=Object.values(R.G).sort((a,b)=>b.ca-a.ca||b.q-a.q).map(o=>o.canal);
  if(RC.canal&&!R.G[RC.canal]) RC.canal='';
  h+=`<div class="ga-card rc-ga"><div class="ga-tabs">${tabs.map(([k,l,v,f,sous,e])=>`<button type="button" class="ga-tab ${RC.metric===k?'on':''}" data-rcm="${k}"><span class="ga-tl">${l}</span><span class="ga-tv">${gaCnt(v,f,v<0?'neg':'')}</span>${sous?`<span class="ga-ts">${sous}</span>`:''}${e}</button>`).join('')}</div>
    <div class="ga-plot" id="rc-c"></div>
    <div class="rc-chs"><button type="button" class="${RC.canal?'':'on'}" data-rcc="">${L3('Tous les canaux','All channels','Todos los canales')}</button>${ordre0.map(n=>`<button type="button" class="${RC.canal===n?'on':''}" data-rcc="${esc(n)}"><i style="background:${rcCoul(n)}"></i><span data-nolang>${esc(rcNomVu(n))}</span></button>`).join('')}</div>
    <div class="rc-figs">${rcFigs(P,R,ordre0,RC.metric)}</div></div>`;
  if(Qinc){ const lib=rcLibPrec(RC.sel,Qinc);
    h+=`<p class="rc-note rc-inc">${L3('Pas de comparaison avec','No comparison with','Sin comparación con')} <span data-nolang>${esc(lib)}</span> : ${L3('les chiffres d\'avant le 1er octobre 2026 sont incomplets (ventes Amazon absentes). La comparaison reviendra d\'elle-même sur les mois suivants.','figures before October 1, 2026 are incomplete (Amazon sales missing). The comparison will come back by itself on the following months.','las cifras anteriores al 1 de octubre de 2026 están incompletas (faltan las ventas de Amazon). La comparación volverá sola en los meses siguientes.')}</p>`; }
  const ordre=Object.values(R.G).sort((a,b)=>b.ca-a.ca||b.q-a.q).map(o=>o.canal);
  const caPos=Object.values(R.G).reduce((a,o)=>a+Math.max(0,o.ca),0)||1;
  const sous=o=>{ if(rcId(o.canal)!=='pc') return ''; const ks=Object.keys(o.ou).filter(k=>k&&(o.ou[k].q||o.ou[k].ca)); if(!ks.length) return '';
    return `<small>${ks.sort().map(k=>rcOuLib(k)+' <b data-nolang>'+money(o.ou[k].ca)+'</b>').join(' · ')}</small>`; };
  h+=`<div class="rc-card rc-card-tab"><h3>${L3('Par canal','By channel','Por canal')}</h3>
    <table class="rc-tab" id="rc-tab"><thead><tr><th>${L3('Canal','Channel','Canal')}</th><th class="r">${L3('Ventes','Sales','Ventas')}</th><th class="r">${L3('Flacons','Bottles','Frascos')}</th><th class="r">${L3("Chiffre d'affaires",'Revenue','Facturación')}</th><th class="r">${L3('Marge nette','Net margin','Margen neto')}</th></tr></thead><tbody>
    ${ordre.map(n=>{ const o=R.G[n]; const part=Math.max(0,o.ca)/caPos*100;
      return `<tr data-c="${esc(n)}"><td><div class="nm"><i class="rc-sw" style="--c:${rcCoul(n)}"></i><span data-nolang>${esc(rcNomVu(n))}</span></div>${sous(o)}</td><td class="r">${nf(o.n)}${o.nR?` <small class="neg">−${nf(o.nR)}</small>`:''}</td><td class="r">${nf(o.q)}</td><td class="r ${o.ca<0?'neg':''}"><b>${money(o.ca)}</b><span class="rc-part" title="${esc(L3('part du chiffre d\'affaires','share of revenue','parte de la facturación'))}"><i style="--c:${rcCoul(n)};--w:${Math.round(part*0.6)}"></i><b>${nf(Math.round(part))} %</b></span></td><td class="r ${o.mg<0?'neg':''}">${o.hist?'<span title="'+esc(L3("prix d'achat de l'époque inconnu : pas de marge",'purchase price at the time unknown: no margin','precio de compra de la época desconocido: sin margen'))+'">—</span>':money(o.mg)}${o.sansPa?' <small class="neg" title="'+esc(L3('lignes sans prix d\'achat','lines without purchase price','líneas sin precio de compra'))+'">?</small>':''}</td></tr>`; }).join('')}
    <tr class="tot"><td>${L3('Total','Total','Total')}</td><td class="r">${nf(T.n)}</td><td class="r">${nf(T.q)}</td><td class="r ${T.ca<0?'neg':''}">${money(T.ca)}</td><td class="r ${T.mg<0?'neg':''}">${money(T.mg)}</td></tr></tbody></table></div>`;
  h+=`
    <p class="rc-note">${L3('La marge est nette : commission du canal, port et frais de carte déduits, comme dans Ventes. Les commandes reçues mais pas encore expédiées ne comptent pas. Les ventes en gros d\'avant l\'ERP (tableur, jusqu\'au 30 sept. 2026) comptent dans le chiffre d\'affaires, sans marge.','The margin is net: channel commission, shipping and card fees deducted, as in Sales. Orders received but not yet shipped do not count. Wholesale sales from before the ERP (spreadsheet, until Sept 30, 2026) count in revenue, without margin.','El margen es neto: comisión del canal, envío y comisiones de tarjeta deducidos, como en Ventas. Los pedidos recibidos pero aún no enviados no cuentan. Las ventas mayoristas de antes del ERP (hoja de cálculo, hasta el 30 sept. 2026) cuentan en la facturación, sin margen.')}</p>`;
  z.innerHTML=h; rcCourbe(P,Q,R,RP,ordre0); gaCompte(z); rcBranche(); gaAnime=false;
}
/* la courbe de l'onglet choisi : tous les canaux (bleu, avec le détail par canal dans la bulle) ou un seul canal (sa couleur) ;
   la période d'avant en pointillé gris */
function rcValeurs(B,S,metric,canal){ const idx={}; B.K.forEach((k,i)=>idx[k.k]=i); const v=B.K.map(()=>0), ventes=B.K.map(()=>new Set());
  S.forEach(x=>{ if(canal&&x.canal!==canal) return; const i=idx[B.jour?x.d:x.d.slice(0,7)]; if(i==null) return;
    if(metric==='n'){ if(!x.ret) ventes[i].add((x.fid||x.num||'')+'|'+(x.cmd||'')); } else v[i]+=metric==='mg'?(x.mg||0):metric==='q'?(x.q||0):x.mt; });
  return metric==='n'?ventes.map(s=>s.size):v; }
function rcCourbe(P,Q,R,RP,ordre){
  const el=document.getElementById('rc-c'); if(!el) return;
  const B0=rcBuckets(P,R.S), auj=rcISO(new Date());
  const B={jour:B0.jour,K:B0.K.filter(k=>B0.jour?k.k<=auj:k.k<=auj.slice(0,7))}; if(!B.K.length) return;
  B.K.forEach(k=>{ k.court2=B.jour?new Date(k.k+'T12:00:00').toLocaleDateString(RC_LOC(),{day:'numeric',month:'short'}):k.court; });
  const m=RC.metric, f=(m==='q'||m==='n')?'n':'$', c=RC.canal;
  const cur=rcValeurs(B,R.S,m,c);
  let prev=null; if(RP&&Q){ const BQ=rcBuckets({a:Q.a,b:Q.b},RP.S); if(BQ.jour===B.jour){ const pv=rcValeurs(BQ,RP.S,m,c); prev=B.K.map((_,i)=>i<pv.length?pv[i]:null); } }
  const libP=rcLib(RC.sel,P), libQ=Q?rcLibPrec(RC.sel,Q):'';
  const parCanal=c?null:ordre.map(n=>({n,v:rcValeurs(B,R.S,m,n)}));
  const tipPlus=i=>{ if(!parCanal) return ''; const L=parCanal.filter(x=>x.v[i]).sort((a,b)=>b.v[i]-a.v[i]); if(!L.length) return '';
    return '<div class="ga-tsep"></div>'+L.map(x=>`<div><span><i style="background:${rcCoul(x.n)}"></i><span data-nolang>${esc(rcNomVu(x.n))}</span></span><b>${gaFmt(f,x.v[i])}</b></div>`).join(''); };
  gaCourbe(el,B.K,[{v:cur,c:c?rcCoul(c):'var(--an-1)',nom:libP,nomTip:c?rcNomVu(c):libP,aire:true}].concat(prev?[{v:prev,c:'var(--ga-prec)',nom:libQ,nomTip:libQ,pointille:true}]:[]),f,{id:'rc',h:280,titre:rcMetLib(m),tipPlus});
  el.insertAdjacentHTML('beforeend',`<div class="ga-leg"><span><i class="ga-li" style="border-top-color:${c?rcCoul(c):'var(--an-1)'}"></i><span data-nolang>${esc(libP)}</span></span>${prev?`<span><i class="ga-li prec"></i><span data-nolang>${esc(libQ)}</span></span>`:''}</div>`);
}
/* les mêmes chiffres dans un tableau (jour par jour ou mois par mois), pour qui veut les lire */
function rcFigs(P,R,ordre,metric){
  const B=rcBuckets(P,R.S); if(!B.K.length) return '';
  const idx={}; B.K.forEach((k,i)=>idx[k.k]=i); const cel=B.K.map(()=>({}));
  if(metric==='n'){ const S=B.K.map(()=>({})); R.S.forEach(v=>{ if(v.ret) return; const i=idx[B.jour?v.d:v.d.slice(0,7)]; if(i==null) return; (S[i][v.canal]=S[i][v.canal]||new Set()).add((v.fid||v.num||'')+'|'+(v.cmd||'')); });
    S.forEach((o,i)=>Object.keys(o).forEach(n=>cel[i][n]=o[n].size)); }
  else R.S.forEach(v=>{ const i=idx[B.jour?v.d:v.d.slice(0,7)]; if(i==null) return; const val=metric==='mg'?(v.mg||0):metric==='q'?(v.q||0):v.mt; cel[i][v.canal]=(cel[i][v.canal]||0)+val; });
  const fm=v=>(metric==='q'||metric==='n')?nf(Math.round(v)):money(v); const vus=ordre.filter(n=>R.G[n]);
  return `<details><summary>${L3('Voir les chiffres','See the figures','Ver las cifras')}, ${B.jour?L3('jour par jour','day by day','día a día'):L3('mois par mois','month by month','mes a mes')}</summary>
    <table class="rc-tab"><thead><tr><th>${B.jour?L3('Jour','Day','Día'):L3('Mois','Month','Mes')}</th>${vus.map(n=>`<th class="r" data-nolang>${esc(rcNomVu(n))}</th>`).join('')}<th class="r">${L3('Total','Total','Total')}</th></tr></thead>
    <tbody>${B.K.map((k,i)=>{ const c=cel[i]; if(!Object.keys(c).length) return ''; const t=Object.values(c).reduce((a,x)=>a+x,0);
      return `<tr><td data-nolang>${esc(k.lib)}</td>${vus.map(n=>`<td class="r ${c[n]<0?'neg':''}">${c[n]?fm(c[n]):'·'}</td>`).join('')}<td class="r ${t<0?'neg':''}"><b>${fm(t)}</b></td></tr>`; }).join('')}</tbody></table></details>`;
}
let _rcTip=null;
function rcBranche(){
  const z=document.getElementById('recap'); if(!z) return;
  z.querySelectorAll('[data-rc]').forEach(b=>b.onclick=()=>{ RC.sel=b.dataset.rc; rcSauve(); gaAnime=true; rcDessine(); });
  z.querySelectorAll('[data-rcm]').forEach(b=>b.onclick=()=>{ RC.metric=b.dataset.rcm; rcSauve(); gaAnime=true; rcDessine(); });
  z.querySelectorAll('[data-rcc]').forEach(b=>b.onclick=()=>{ RC.canal=b.dataset.rcc; gaAnime=true; rcDessine(); });
  const sm=document.getElementById('rc-mois'), sa=document.getElementById('rc-an');
  if(sm) sm.onchange=()=>{ if(sm.value){ RC.sel=sm.value; rcSauve(); gaAnime=true; rcDessine(); } };
  if(sa) sa.onchange=()=>{ if(sa.value){ RC.sel=sa.value; rcSauve(); gaAnime=true; rcDessine(); } };
  if(!_rcTip){ _rcTip=document.createElement('div'); _rcTip.className='rc-tip'; document.body.appendChild(_rcTip); }
  const montre=(el,ev)=>{ _rcTip.innerHTML=el.dataset.tip||''; _rcTip.style.display='block';
    const r=el.getBoundingClientRect(); let x=(ev&&ev.clientX!=null?ev.clientX:r.left+r.width/2)+12, yy=(ev&&ev.clientY!=null?ev.clientY:r.top)-10;
    const w=_rcTip.offsetWidth||220; if(x+w>window.innerWidth-8) x=x-w-24; if(yy<8) yy=8; _rcTip.style.left=x+'px'; _rcTip.style.top=yy+'px'; };
  const cache=()=>{ _rcTip.style.display='none'; };
  z.querySelectorAll('.rc-col').forEach(c=>{ c.onmouseenter=e=>montre(c,e); c.onmousemove=e=>montre(c,e); c.onmouseleave=cache; c.onfocus=()=>montre(c,null); c.onblur=cache; });
}
window.__recap={RC,rcLignes,rcPlage,rcPrec,rcAgrege,rcDessine};
'''
RECAP_JS = RECAP_JS.replace('/*__GA__*/', GA_JS, 1)
