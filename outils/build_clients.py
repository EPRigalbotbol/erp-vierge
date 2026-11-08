# -*- coding: utf-8 -*-
"""Rubrique « Clients » : TOUS ceux qui achètent, dans une seule liste — les grossistes,
les clients du site, ceux de la boutique, Amazon — et pour chacun sa fiche : ce qu'il a
acheté, quand, à quelle heure, par quel canal, comment il a payé, et ses coordonnées.

Igal, 12 septembre 2026 : « la partie client, c'est-à-dire tous ceux qui achètent, en
linéaire, avec la fiche technique du client de ce qu'il a acheté, quand, comment, à
quelle heure ». Avant, il y avait deux rubriques (VIP wholesale d'un côté, Retail de
l'autre) et un même client pouvait être dans les deux sans qu'on le voie.

Trois sources, fondues par le nom :
  - le tableur de Sam (onglet « carmen ») : les commandes de gros d'avant l'outil ;
  - les ventes enregistrées dans l'outil (factures-v1) : site, caisse, boutique, gros,
    Amazon — avec l'heure, le canal, les lignes et le paiement ;
  - la liste des clients du site (retail-local-v1 / fichier retail) : coordonnées.
Les coordonnées corrigées ici vivent dans clients-v1, comme avant."""
import json
from build_crm import coquille
import _donnees
C = json.load(open('cat.json'))
SEED = json.load(open('clients_seed.json'))

# ---- version compacte pour la page : chaque ligne devient un tableau ----
K = ['bc', 'nom', 'ml', 'marque', 'type', 'p', 'q', 't', 'fact', 'sorti', 'note']
def compact(cl):
    return {'nom': cl['nom'], 'total': cl['total'], 'nb': cl['nb'], 'nbDevis': cl['nbDevis'],
            'totalDevis': cl['totalDevis'], 'q': cl['q'], 'prem': cl['prem'], 'der': cl['der'],
            'ecritures': cl['ecritures'],
            'cmds': [{'num': c['num'], 'd': c['date'], 'de': c['date_estimee'], 'devis': c['devis'],
                      'note': c['note'], 'total': c['total'], 'sous': c['sous'], 'ecart': c['ecart_sous'],
                      'douteux': c['douteux'], 'sl': c['sans_lignes'], 'ls': c['ligne_sheet'],
                      'f': c.get('fact', ''), 's': c.get('sorti', ''),
                      'l': [[l[k] for k in K] for l in c['lignes']]} for c in cl['cmds']]}
DATA = {'date': SEED['date'], 'src': SEED['src'], 'clients': [compact(c) for c in SEED['clients']]}

CSS = r"""
.ptop{display:flex;gap:6px;align-items:center;flex-wrap:wrap;margin:0 0 12px;font-size:13px;color:var(--ink-2)}
.ptop .sp{margin-left:auto}
.ptop .btn.on{background:var(--iris);border-color:var(--iris);color:#fff}
.reldest{display:flex;align-items:center;gap:9px;margin-bottom:11px}
.reldest label{font-size:9.5px;letter-spacing:.12em;text-transform:uppercase;color:var(--ink-3);
font-weight:600;flex:none}
.reldest input{flex:1;font-family:inherit;font-size:13.5px;color:var(--ink);background:var(--surface-2);
border:1px solid var(--line);border-radius:3px;padding:8px 10px}
.reldest input:focus{outline:2px solid var(--iris);outline-offset:1px;background:var(--surface)}
.reldest input.manque{border-color:var(--crit);background:var(--crit-soft)}
.reldest span{font-size:12px;color:var(--ink-3)}
.reldest span.err{color:var(--crit);font-weight:600}

.sous{margin:5px 0 0;font-size:14px;color:var(--ink-2);max-width:74ch;line-height:1.5}
.tools{display:flex;gap:9px;flex-wrap:wrap;align-items:center;margin-bottom:16px}
.tools .sp{margin-left:auto}
.srch{position:relative;flex:1 1 220px;max-width:360px}
.srch input{width:100%;padding:10px 12px 10px 34px;font-family:inherit;font-size:14px;
border:1px solid var(--line);border-radius:7px;background:var(--surface);color:var(--ink)}
.srch input:focus{outline:0;border-color:var(--iris);box-shadow:0 0 0 3px var(--iris-soft)}
.srch::before{content:"⌕";position:absolute;left:11px;top:50%;transform:translateY(-50%);color:var(--ink-3);font-size:16px}
.sel{padding:10px 11px;font-family:inherit;font-size:14px;border:1px solid var(--line);border-radius:7px;background:var(--surface);color:var(--ink);cursor:pointer}
.sel:focus{outline:0;border-color:var(--iris)}
.btn{font-family:inherit;font-size:14px;font-weight:500;color:var(--ink-2);background:var(--surface);border:1px solid var(--line);border-radius:7px;padding:10px 16px;cursor:pointer}
.btn:hover{border-color:var(--iris);color:var(--iris)}
.btn.pri{background:var(--iris);border-color:var(--iris);color:#fff;font-weight:600}
.btn.pri:hover{filter:brightness(1.08);color:#fff}
a.btn{text-decoration:none;display:inline-block}

/* quatre chiffres, pas plus */
.kpis{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:22px}
.kpi{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:16px 20px}
.kpi .v{font-family:Inter,sans-serif;font-size:30px;font-weight:800;line-height:1;letter-spacing:-.03em;font-variant-numeric:tabular-nums;color:var(--ink)}
.kpi .v.i{color:var(--iris)}
.kpi .k{font-size:13px;color:var(--ink-2);margin-top:6px}

/* les types de client : gros, site, boutique, Amazon */
.tg{display:inline-block;font-family:Inter,sans-serif;font-size:10px;font-weight:800;letter-spacing:.06em;text-transform:uppercase;padding:2px 7px;border-radius:99px;margin-left:6px;vertical-align:middle;background:var(--line-2);color:var(--ink-2)}
.tg.gros{background:var(--iris-soft);color:var(--iris)}
.tg.site{background:var(--good-soft);color:var(--good)}
.tg.boutique{background:var(--warn-soft);color:var(--warn)}
.tg.amazon{background:#fde9c8;color:#8a5a00}
.tg.retour{background:var(--crit-soft);color:var(--crit)}

/* la liste des clients : un tableau, une ligne par client */
.tbl{width:100%;border-collapse:collapse;font-size:14px;background:var(--surface);border:1px solid var(--line);border-radius:10px;overflow:hidden}
.tbl th{text-align:left;font-family:Inter,sans-serif;font-size:11.5px;letter-spacing:.09em;text-transform:uppercase;color:var(--ink);
font-weight:800;padding:12px 14px;background:var(--surface-2);border-bottom:2px solid var(--line);white-space:nowrap;cursor:pointer;user-select:none}
.tbl th:hover{color:var(--iris)}
.tbl th.on::after{content:" ▾";color:var(--iris)}
.tbl th.n,.tbl td.n{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
.tbl td{padding:12px 14px;border-bottom:1px solid var(--line-2);vertical-align:middle}
.tbl tbody tr:last-child td{border-bottom:0}
.tbl tbody tr{cursor:pointer}
.tbl tbody tr:hover td{background:var(--iris-soft)}
.tbl td.rg{color:var(--ink-3);font-family:Inter,sans-serif;font-size:12px;width:34px}
/* l'étoile des favoris : creuse tant qu'elle n'est pas mise, pleine ensuite.
   Elle vit dans la fiche du client, donc tout le monde voit les mêmes. */
.tbl td.fav,.tbl th.fav{width:30px;padding-left:4px;padding-right:0;text-align:center}
.tbl td.coch,.tbl th.coch{width:32px;padding-right:0;text-align:center}
.et{background:none;border:0;padding:2px 4px;font-size:17px;line-height:1;cursor:pointer;
 color:var(--line);border-radius:5px}
.et:hover{color:var(--warn)}
.et.on{color:#e0a400}
.dh .et{font-size:24px;vertical-align:middle;margin-left:4px}
.tbl tbody tr.vip td{background:#fffaf0}
.tbl tbody tr.vip:hover td{background:var(--iris-soft)}
.tbl input.ck{width:15px;height:15px;accent-color:var(--iris);cursor:pointer;vertical-align:middle}
/* La barre qui apparaît dès qu'une case est cochée.
   Surtout PAS « .sel » : les filtres de la page portent déjà cette classe, et
   un display:none dessus fait disparaître les menus déroulants. */
.selb{display:none;align-items:center;gap:12px;flex-wrap:wrap;margin:0 0 14px;padding:11px 15px;
 background:var(--iris-soft);border:1px solid var(--iris);border-radius:10px;font-size:13.5px;color:var(--ink)}
.selb.on{display:flex}
.selb b{font-weight:800}
.selb .sp{margin-left:auto}
.tbl td.nom{font-weight:700;font-size:15px}
.tbl td.nom small{display:block;font-weight:400;font-size:12px;color:var(--ink-3);margin-top:2px}
.tbl td.mt{font-family:Inter,sans-serif;font-weight:800;font-size:15px;color:var(--iris)}
.tbl td.mt .bar{height:5px;border-radius:3px;background:var(--line-2);margin-top:6px;overflow:hidden;min-width:120px}
.tbl td.mt .bar i{display:block;height:100%;background:var(--iris)}
.tbl td.dim{color:var(--ink-2)}
.warn{display:inline-block;font-family:Inter,sans-serif;font-size:10.5px;font-weight:700;padding:2px 7px;border-radius:99px;background:var(--crit-soft);color:var(--crit);margin-left:8px;vertical-align:middle}
.wrapx{overflow-x:auto}
.foot{margin-top:18px;font-size:12.5px;color:var(--ink-3);line-height:1.6}
.foot a{color:var(--iris)}
details.src{margin-top:12px;font-size:13px;color:var(--ink-2);line-height:1.65;max-width:80ch}
details.src summary{cursor:pointer;color:var(--iris);font-weight:600}
details.src b{color:var(--ink)}

/* fiche client : un tiroir, trois onglets */
.dr{position:fixed;top:0;right:0;bottom:0;width:min(980px,100%);background:var(--surface);
box-shadow:-12px 0 40px rgba(0,0,0,.18);transform:translateX(102%);transition:transform .18s;z-index:60;display:flex;flex-direction:column}
.dr.on{transform:none}
.drov{position:fixed;inset:0;background:rgba(23,23,29,.35);z-index:59;display:none}
.drov.on{display:block}
.dh{padding:20px 28px 0;border-bottom:1px solid var(--line)}
.dh .row{display:flex;align-items:flex-start;gap:14px}
.dh h2{margin:0;font-size:28px;font-weight:800;letter-spacing:-.025em;line-height:1.1;flex:1}
.dh h2 .tg{font-size:10px;vertical-align:middle;position:relative;top:-4px}
.dh .co{font-size:13px;color:var(--ink-2);margin-top:6px}
.dh .x{background:none;border:1px solid var(--line);border-radius:7px;font-size:18px;color:var(--ink-2);cursor:pointer;line-height:1;padding:6px 11px}
.dh .x:hover{border-color:var(--ink);color:var(--ink)}
.dk{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:18px 0 20px}
.dk div{background:var(--surface-2);border:1px solid var(--line);border-radius:9px;padding:12px 14px}
.dk b{display:block;font-family:Inter,sans-serif;font-size:22px;font-weight:800;letter-spacing:-.03em;line-height:1;font-variant-numeric:tabular-nums}
.dk b.i{color:var(--iris)}
.dk span{display:block;font-size:12px;color:var(--ink-2);margin-top:5px}
.tabs{display:flex;gap:4px}
.tab{background:none;border:0;border-bottom:3px solid transparent;padding:10px 16px;font-family:inherit;font-size:14.5px;font-weight:600;color:var(--ink-3);cursor:pointer}
.tab.on{color:var(--iris);border-bottom-color:var(--iris)}
.db{padding:20px 28px 40px;overflow-y:auto;flex:1}
.pane{display:none}.pane.on{display:block}
.t2{width:100%;border-collapse:collapse;font-size:14px;background:var(--surface);border:1px solid var(--line);border-radius:10px;overflow:hidden}
.t2 th{text-align:left;font-family:Inter,sans-serif;font-size:11.5px;letter-spacing:.09em;text-transform:uppercase;color:var(--ink);font-weight:800;padding:11px 14px;background:var(--surface-2);border-bottom:2px solid var(--line);white-space:nowrap}
.t2 th.n,.t2 td.n{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
.t2 td{padding:11px 14px;border-bottom:1px solid var(--line-2);vertical-align:middle}
.t2 tbody tr:last-child td{border-bottom:0}
.t2 tr.cmd{cursor:pointer}
.t2 tr.cmd:hover td{background:var(--surface-2)}
.t2 tr.cmd.on td{background:var(--iris-soft)}
.t2 tr.cmd.ret td{color:var(--crit)}
.t2 td.mt{font-family:Inter,sans-serif;font-weight:800}
.t2 .reste{font-size:12px;color:var(--crit);white-space:nowrap}.t2 .reste b{font-weight:800}
.t2 a.voir{display:inline-block;margin-left:8px;font-size:12px;color:var(--iris);white-space:nowrap}
.t2 td .est{color:var(--ink-3)}
.t2 td .hh{font-family:Inter,sans-serif;font-variant-numeric:tabular-nums;color:var(--ink-2)}
.t2 tr.lig td{background:var(--surface-2);padding:6px 14px 14px 40px}
.t2 tr.lig table{width:100%;border-collapse:collapse;font-size:13px}
.t2 tr.lig table th{font-size:10px;padding:8px 8px 6px;background:none;border-bottom:1px solid var(--line)}
.t2 tr.lig table td{padding:7px 8px;border-bottom:1px dashed var(--line-2);background:none;color:var(--ink)}
.t2 tr.lig table td.n{font-family:Inter,sans-serif}
.t2 tr.lig a{color:var(--ink);text-decoration:none;border-bottom:1px dotted var(--ink-3)}
.t2 tr.lig a:hover{color:var(--iris);border-bottom-color:var(--iris)}
.t2 td.nom{font-weight:600}
.t2 td.nom small{display:block;font-weight:400;font-size:12px;color:var(--ink-3)}
.ok{color:var(--good);font-weight:700}.non{color:var(--ink-3)}.du{color:var(--crit);font-weight:700}
.avert{background:var(--warn-soft);border-left:3px solid var(--warn);border-radius:0 8px 8px 0;padding:11px 14px;font-size:13px;color:var(--ink-2);line-height:1.6;margin:0 0 16px}
.avert b{color:var(--ink)}
.ed{display:grid;grid-template-columns:repeat(2,1fr);gap:14px;max-width:640px}
.pjs{margin-top:22px;padding-top:16px;border-top:1px solid var(--line-2);max-width:640px}
.pjs h4{margin:0 0 10px;font-size:13px;letter-spacing:.06em;text-transform:uppercase}
.pjadd{display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin-top:10px}
.pjadd label.btn{cursor:pointer}.pjmsg{font-size:13px;color:var(--ink-3)}
.pjt td small{display:block;color:var(--ink-3);font-size:11.5px}
.ed label{display:flex;flex-direction:column;gap:5px;font-family:Inter,sans-serif;font-size:11px;letter-spacing:.09em;text-transform:uppercase;color:var(--ink);font-weight:800}
.ed input,.ed textarea{font-family:inherit;font-size:14px;color:var(--ink);background:var(--surface-2);border:1px solid var(--line);border-radius:7px;padding:10px 12px;letter-spacing:0;text-transform:none;font-weight:400}
.ed input:focus,.ed textarea:focus{outline:0;border-color:var(--iris);background:var(--surface);box-shadow:0 0 0 3px var(--iris-soft)}
.ed textarea{min-height:80px;resize:vertical;grid-column:1/-1}
.ecr{margin-top:22px;font-size:13px;color:var(--ink-2);line-height:1.7}
.ecr b{color:var(--ink)}
.vide{border:2px dashed var(--line);border-radius:12px;padding:40px 32px;text-align:center;background:var(--surface-2);max-width:66ch;margin:16px auto;color:var(--ink-2)}
.t2 select.pay{font-family:inherit;font-size:13px;padding:5px 7px;border:1px solid var(--line);border-radius:6px;background:var(--surface);color:var(--ink);cursor:pointer}
.t2 select.pay.du{border-color:var(--crit);color:var(--crit);font-weight:700;background:var(--crit-soft)}
.t2 select.pay.ok{border-color:var(--good);color:var(--good);font-weight:700;background:var(--good-soft)}
.t2 select.pay.part{border-color:var(--warn);color:var(--warn);font-weight:700;background:var(--warn-soft)}
.t2 input.part{width:80px;font-family:inherit;font-size:13px;padding:5px 7px;border:1px solid var(--line);border-radius:6px;text-align:right}
.t2 td .rel{display:block;font-size:11px;color:var(--ink-3);margin-top:3px}
.dk b.c{color:var(--crit)}
.dh .btn.rel{white-space:nowrap}
.dh .btn.rel[disabled]{opacity:.45;cursor:default}
.barre2{display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin:0 0 14px;font-size:13px;color:var(--ink-2)}
.barre2 .sp{margin-left:auto}
.btn.sm{padding:6px 12px;font-size:13px}
.ov{position:fixed;inset:0;background:rgba(23,23,29,.5);z-index:80;display:none;align-items:flex-start;justify-content:center;padding:40px 18px;overflow-y:auto}
.ov.on{display:flex}
.mod{background:var(--surface);border:1px solid var(--line);border-radius:10px;width:100%;max-width:720px;box-shadow:0 18px 48px rgba(0,0,0,.22)}
.mod.pt{max-width:460px}
.mod .mh{padding:18px 22px;border-bottom:1px solid var(--line);display:flex;align-items:center;gap:12px}
.mod .mh h3{margin:0;font-size:18px;font-weight:800;letter-spacing:-.02em;flex:1}
.mod .mb{padding:18px 22px;display:flex;flex-direction:column;gap:12px}
.mod textarea{width:100%;min-height:260px;font-family:inherit;font-size:14px;line-height:1.55;color:var(--ink);background:var(--surface-2);border:1px solid var(--line);border-radius:7px;padding:12px 14px;resize:vertical}
.mod textarea:focus,.mod input:focus{outline:0;border-color:var(--iris);background:var(--surface);box-shadow:0 0 0 3px var(--iris-soft)}
.mod input{width:100%;font-family:inherit;font-size:14px;color:var(--ink);background:var(--surface-2);border:1px solid var(--line);border-radius:7px;padding:10px 12px}
.mod .mf{padding:14px 22px;border-top:1px solid var(--line);display:flex;gap:9px;align-items:center;flex-wrap:wrap;background:var(--surface-2);border-radius:0 0 10px 10px}
.mod .mf .msg{font-size:12.5px;color:var(--ink-3);margin-right:auto}
.lang{display:flex;gap:4px}
.lang button{font-family:inherit;font-size:12.5px;font-weight:600;padding:5px 10px;border:1px solid var(--line);border-radius:99px;background:var(--surface);color:var(--ink-2);cursor:pointer}
.lang button.on{background:var(--iris);border-color:var(--iris);color:#fff}
@media(max-width:900px){.kpis,.dk{grid-template-columns:repeat(2,1fr)}}
"""

CORPS = r"""
<div class="tools">
  <div class="srch"><input id="q" autocomplete="off" placeholder="Chercher un client, un e-mail, une ville…"></div>
  <select id="typ" class="sel">
    <option value="">Tous les clients</option>
    <option value="vip">Favoris (VIP)</option>
    <option value="gros">Grossistes</option>
    <option value="site">Clients du site</option>
    <option value="boutique">Boutique et caisse</option>
    <option value="amazon">Amazon</option>
    <option value="sans">Sans achat enregistré</option></select>
  <select id="per" class="sel">
    <option value="0">Toute la période</option>
    <option value="30">30 derniers jours</option>
    <option value="90">3 derniers mois</option>
    <option value="180">6 derniers mois</option>
    <option value="365">12 derniers mois</option></select>
  <span class="sp"></span>
  <button class="btn" id="diff" title="Envoyer une offre à tous les clients de la liste affichée, par email et par WhatsApp">Liste de diffusion</button>
  <button class="btn" id="nouv">+ Nouveau client</button>
  <a class="btn" href="retail.html" title="Déposer la liste des clients du site (fichier CSV ou Excel)">Importer un fichier</a>
  <span id="exp"></span>
</div>
<div id="kpis"></div>
<div class="selb" id="selbar">
  <span><b id="selnb">0</b> <span id="sellib">clients sélectionnés</span></span>
  <button class="btn sm" id="selvip">Mettre en favoris</button>
  <button class="btn sm" id="selnon">Retirer des favoris</button>
  <span class="sp"></span>
  <button class="btn sm" id="selrien">Tout décocher</button>
  <button class="btn pri sm" id="selecr">Écrire aux sélectionnés</button>
</div>
<div id="corps"></div>
<details class="src" id="note"><summary>D'où viennent ces chiffres, et ce qui est approximatif</summary><div id="notetxt"></div></details>

<div class="drov" id="drov"></div>
<aside class="dr" id="dr" aria-hidden="true">
  <div class="dh">
    <div class="row"><div style="flex:1"><h2 id="dnom"></h2><div class="co" id="dco"></div></div><button class="et" id="dfav" title="Mettre ce client en favoris">☆</button><button class="btn" id="decr">Écrire</button><button class="btn pri rel" id="drel">Relance de paiement</button><button class="x" id="dx" title="Fermer">✕</button></div>
    <div class="dk" id="dk"></div>
    <div class="tabs">
      <button class="tab on" data-t="cmd">Ses achats</button>
      <button class="tab" data-t="prod">Les parfums qu'il prend</button>
      <button class="tab" data-t="coord">Coordonnées</button>
    </div>
  </div>
  <div class="db">
    <div class="pane on" id="p-cmd"></div>
    <div class="pane" id="p-prod"></div>
    <div class="pane" id="p-coord"></div>
  </div>
</aside>

<div class="ov" id="novov"><div class="mod pt">
  <div class="mh"><h3>Nouveau client</h3></div>
  <div class="mb"><input id="novnom" placeholder="Nom du client ou de la société" autocomplete="off">
    <p class="ecr" style="margin:0">Le nom sert de clé : c'est lui qu'on retrouve sur les factures et les cotes. Les coordonnées se remplissent ensuite dans sa fiche.</p></div>
  <div class="mf"><span class="msg" id="novmsg"></span><button class="btn" id="novx">Annuler</button><button class="btn pri" id="novok">Créer la fiche</button></div>
</div></div>

<div class="ov" id="relov"><div class="mod">
  <div class="mh"><h3>Relance de paiement — <span id="relnom"></span></h3><div class="lang" id="rellang"><button data-l="fr" class="on">FR</button><button data-l="en">EN</button><button data-l="es">ES</button></div></div>
  <div class="mb">
    <div class="reldest">
      <label for="reldest">Envoyer à</label>
      <input type="email" id="reldest" placeholder="adresse@exemple.com" autocomplete="off">
      <span id="reldn"></span>
    </div>
    <textarea id="reltxt"></textarea>
    <p class="ecr" style="margin:0">Le texte est modifiable. L'adresse ci-dessus est celle de la fiche client ;
    si tu la corriges ici, elle est enregistrée dans la fiche. « Ouvrir dans Mail » prépare l'e-mail dans ton
    logiciel de messagerie ; WhatsApp utilise le téléphone de la fiche. L'outil n'envoie rien tout seul :
    c'est toi qui appuies sur Envoyer.</p></div>
  <div class="mf"><span class="msg" id="relmsg"></span>
    <button class="btn" id="relcopy">Copier le texte</button>
    <button class="btn" id="relwa">WhatsApp</button>
    <button class="btn pri" id="relmail">Ouvrir dans Mail</button>
    <button class="btn" id="relx">Fermer</button></div>
</div></div>
"""

JS = r"""
const D=__DATA__, BC2CLE=__BC2CLE__;
const KCLI='clients-v1', KJOU='crm-journal-v1', KPAY='reglements-v1', KFACT='factures-v1', KRET='retail-local-v1';
let CLI={}, USR='', PAY={}, FACT=[];
CLI=lit(KCLI,{}); if(!CLI||typeof CLI!=='object') CLI=base(KCLI,{});
PAY=lit(KPAY,{}); if(!PAY||typeof PAY!=='object') PAY=base(KPAY,{});
FACT=lit(KFACT,[]); if(!Array.isArray(FACT)) FACT=[];
const sauvePAY=()=>ecrit(KPAY,PAY);
const sauveCLI=()=>ecrit(KCLI,CLI);
const journal=(act,lib,ref,ap)=>{ const J=lit(KJOU,[]);
  J.push({t:new Date().toISOString(),u:USR||'(non renseigné)',act,lib,ref,av:null,ap:ap||null});
  ecrit(KJOU,J); };
USR=NOM_UTIL;
window.__nomChange.push(v=>{ USR=v; });
const MODES=[['','—'],['especes','Espèces'],['zelle','Zelle'],['virement','Virement'],['carte','Carte'],['cheque','Chèque'],['credit','Crédit / store credit'],['autre','Autre']];
const MODE_LIB={especes:'Espèces',zelle:'Zelle',virement:'Virement',carte:'Carte bancaire',cheque:'Chèque',credit:'Crédit chez nous',autre:'Autre',enligne:'Payé en ligne',caisse:'Payé à la caisse',aucun:'Rien rendu',avoir:'Avoir',echange:'Échange'};
const STATUTS=[['','non renseigné'],['du','À payer'],['paye','Payée'],['part','Partielle']];
const TYPES={gros:'Gros',site:'Site',boutique:'Boutique',amazon:'Amazon'};
const MOTIFS={retour:'retour du client',erreur:'erreur de saisie',annulation:'commande annulée',defectueux:'produit défectueux',perdu:'colis perdu',autre:'autre'};
const pkey=(nom,x)=>nom+'|'+(x.num||'l'+x.ls);
const [BC,NOM,ML,MARQUE,TYPE,P,Q,T,FACTC,SORTI,NOTE]=[0,1,2,3,4,5,6,7,8,9,10];
/* La fiche catalogue d'un parfum : marque, contenance, type et genre. Une vente
   enregistrée ne garde qu'un libellé figé ; tout le reste se retrouve ici. */
let _FI=null;
function fiche(cle){
  if(!cle) return null;
  if(!_FI){ _FI={}; try{ D_TOUS().forEach(r=>{ if(r[15]) _FI[r[15]]=[r[0],r[13],r[2],r[3],r[4],r[5]]; }); }catch(e){} }
  return _FI[cle]||null;
}
const GEN={M:'Homme',W:'Femme',U:'Unisexe',K:'Enfant'};
const tyBadge=(type,genre)=>{ const t=String(type||'').trim(), g=GEN[String(genre||'').trim().toUpperCase()]||'';
  return (t?' <i class="ty" data-nolang>'+esc(t)+'</i>':'')+(g?' <i class="gn">'+esc(g)+'</i>':''); };
/* le type d'une ligne : celui gardé avec elle, sinon celui de la fiche */
const tyDe=l=>{ const fi=fiche(l&&l.cle); return [(l&&l.type)||(fi&&fi[4])||'', (fi&&fi[5])||'']; };
const cNorm=s=>String(s==null?'':s).toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/[^a-z0-9]+/g,' ').trim();
const dfr=d=>{ if(!d) return '—'; const [a,m,j]=String(d).slice(0,10).split('-'); return m+'/'+j+'/'+a.slice(2); };
/* 13 oct. 2026 (Igal) : « Juan » et « Juan Carlos » sont le client La Casa del Perfume ; « Myriam » est
   le client Robert. Le tableur est déjà rangé ainsi (build_clients_data.py) ; ici, ce sont les ventes
   faites dans l'outil et les fiches déjà enregistrées sous l'ancien nom, qui rejoignent le même client.
   Les fiches ne sont pas réécrites : Ventes et Cote retrouvent toujours « Juan Carlos » par son nom. */
const ALIAS_CLI={'juan':'Casa del Perfume','juan carlos':'Casa del Perfume','la casa del perfume':'Casa del Perfume','casa del perfume':'Casa del Perfume','myriam':'Robert','miriam':'Robert',   /* 7 nov. 2026 (Igal) : Miriam et Robert, un seul client */
  /* 31 oct. 2026 (Igal : « c'est le même client ») : le nom de la société, tapé dans Lightspeed, rejoint « Habibi » */
  'habibi perfumes llc':'Habibi','habibi perfumes':'Habibi','habibi perfume':'Habibi'};
const canon=nom=>ALIAS_CLI[cNorm(nom)]||nom;
/* 7 nov. 2026 (Igal, rôle Commercial : « enlever le CA des clients et l'argent qu'on lui doit ») : un compte qui ne voit
   pas les marges ne voit ni le chiffre d'affaires par client, ni ce qu'un client doit ; ces blocs sont VIDÉS, pas cachés */
const voitCA=()=>{ try{ return typeof peut!=='function'||!!peut('voirMarge'); }catch(e){ return true; } };
const AUJ=new Date();
let TRI='mt', PTOP=10, PTRI='q';

/* ---------- les favoris (VIP) ----------
   L'étoile est rangée dans la fiche du client (clients-v1), pas dans un coin
   du navigateur : elle appartient à l'entreprise, elle part sur le serveur
   comme le reste, et un commercial voit les mêmes favoris que Sam.
   Les cases cochées, elles, ne durent que le temps de l'écran : cocher trois
   clients pour leur écrire n'est pas une décision à garder. */
/* Les autres noms d'un client (ses alias). Calculé UNE fois par redessin : avant, chaque appel (des
   milliers par tri de la liste) renormalisait les 480 noms — la liste mettait presque une seconde à se
   redessiner et la page « se figeait » dès qu'un autre poste écrivait (13 oct. 2026, Igal). */
let _ALX=null, _ALXc=null;
const clesAlias=nom=>{
  if(!_ALX||_ALXc!==CLI){ _ALX=new Map(); _ALXc=CLI;
    Object.keys(CLI).forEach(k=>{ const c=canon(k); if(c!==k){ let L=_ALX.get(c); if(!L) _ALX.set(c,L=[]); L.push(k); } }); }
  return _ALX.get(nom)||[]; };
const estVip=nom=>!!(CLI[nom]&&CLI[nom].vip)||clesAlias(nom).some(k=>CLI[k]&&CLI[k].vip);
let COCHES=new Set();
function basculeVip(nom,veut){
  _ALX=null;
  /* la fiche du client relue juste avant : un autre poste a pu mettre l'étoile entre-temps
     (1er oct. 2026 : Igal met Javier en favori, l'écran de Sam ne le montre pas, Sam clique
     deux fois — l'étoile est mise puis retirée, et plus personne ne la voit) */
  { const c=lit(KCLI,null); if(c&&typeof c==='object') CLI=c; }
  const v=(veut===undefined)?!estVip(nom):!!veut;
  if(v===estVip(nom)) return v;
  CLI[nom]=Object.assign({},CLI[nom]||{},{nom,vip:v||undefined,maj:new Date().toISOString()});
  if(!v){ delete CLI[nom].vip; clesAlias(nom).forEach(k=>{ if(CLI[k]&&CLI[k].vip) delete CLI[k].vip; }); }
  sauveCLI();
  journal('client', v?'client mis en favoris (VIP)':'client retiré des favoris', nom, null);
  return v;
}

/* Changer un règlement refait la fiche : elle doit rester EXACTEMENT où elle était. Avant, chaque
   changement la ramenait tout en haut (13 oct. 2026, Igal : sur un client à 196 commandes,
   « ça bug » — on ne pouvait pas régler la 50e sans remonter tout en haut à chaque fois). */
function redessineFiche(nom){
  const db=document.querySelector('#dr .db'), y=db?db.scrollTop:0;
  const ouvertes=[...document.querySelectorAll('#p-cmd tr.lig:not([hidden])')].map(r=>r.dataset.i);
  construit(); dessine(); ouvre(nom); onglet('cmd');
  ouvertes.forEach(i=>{ const l=document.querySelector('#p-cmd tr.lig[data-i="'+i+'"]'), c=document.querySelector('#p-cmd tr.cmd[data-i="'+i+'"]');
    if(l){ if(window.__remplitLig) window.__remplitLig(i); l.hidden=false; if(c) c.classList.add('on'); } });
  const d2=document.querySelector('#dr .db'); if(d2) d2.scrollTop=y;
}
/* ce que le tableur dit déjà : « paid in cash », « paid zelle »… */
function payInit(nom,x){
  const k=pkey(nom,x); if(PAY[k]) return PAY[k];
  const txt=[x.note,x.f,x.s,...x.l.map(l=>l[FACTC]+' '+l[SORTI]+' '+l[NOTE])].join(' ').toLowerCase();
  if(/\bpaid\b/.test(txt)){ const p={st:'paye',mode:/cash/.test(txt)?'especes':/zelle/.test(txt)?'zelle':'',src:'tableur'}; return p; }
  return {st:'',mode:''};
}
/* le canal d'une vente de l'outil dit quel genre de client c'est */
function typeCanal(canal,f){
  const c=String(canal||'').toLowerCase();
  if(/gros|wholesale/.test(c) || (f&&f.doc&&f.doc.fiscal==='resale')) return 'gros';
  if(/amazon/.test(c)) return 'amazon';
  if(/site|perfumestrade|shopify|web/.test(c)) return 'site';
  if(/boutique|caisse|lightspeed|comptoir/.test(c)) return 'boutique';
  return 'boutique';
}
/* le paiement d'une vente de l'outil : facture (réglé / reste dû), vente du site (payée en ligne), caisse */
/* 31 oct. 2026 : une vente ANNULÉE en entier (« Annuler la vente », ou un remboursement de tout) ne reste pas « à payer » :
   la fiche de Habibi affichait encore « 687 $ à payer » pour une vente en double annulée le 27 oct. */
let _RFD=null;
function rembourseDe(fid){
  if(!_RFD){ _RFD={}; (FACT||[]).forEach(r=>{ if(r&&r.retour&&r.refId) _RFD[r.refId]=(_RFD[r.refId]||0)+Math.abs(+r.montant||0); }); }
  return _RFD[fid]||0; }
function payErp(f){
  if(f.retour) return {st:'rembourse',mode:f.mode||'',lib:'remboursé — '+(MOTIFS[f.motif]||f.motif||'retour')};
  if(f.id&&(+f.montant||0)>0&&rembourseDe(f.id)>=(+f.montant||0)-0.01) return {st:'annule',mode:(f.doc&&f.doc.pmode)||'',lib:'annulée'};
  if(f.doc){ const D=f.doc; const st=(D.reste||0)<=0?'paye':((+D.regle||0)>0?'part':'du');
    return {st,mode:D.pmode||'',regle:+D.regle||0,reste:+D.reste||0,total:+D.total||0}; }
  if(f.auto){ const a=String(f.auto); return {st:'paye',mode:/lightspeed|caisse/.test(a)?'caisse':'enligne'}; }
  return {st:'',mode:''};
}
const payLib=p=>{ if(!p) return '—'; if(p.st==='rembourse') return `<span class="du">${esc(p.lib)}</span>`;
  if(p.st==='annule') return `<span class="non">annulée</span>`;
  const m=MODE_LIB[p.mode]||(MODES.find(x=>x[0]===p.mode)||['',''])[1]||'';
  if(p.st==='paye') return `<span class="ok">payé</span>${m?' · '+esc(m):''}`;
  if(p.st==='part') return `<span class="du">acompte ${money2(p.regle||0)}</span> · reste ${money2(p.reste!=null?p.reste:0)}${m?' · '+esc(m):''}`;
  if(p.st==='du') return `<span class="du">à payer</span>${p.reste!=null&&voitCA()?' · '+money2(p.reste):''}${m?' · '+esc(m):''}`;
  return `<span class="non">—</span>${m?' · '+esc(m):''}`; };
const regleDe=(a)=>{ const p=a.pay||{}; if(a.src==='tableur') return p.st==='paye'?a.montant:(+p.regle||0); return p.st==='paye'?a.montant:(+p.regle||0); };
const resteDe=(a)=>{ const p=a.pay||{}; if(a.src==='tableur') return p.st==='du'?a.montant:p.st==='part'?Math.max(0,a.montant-(+p.regle||0)):0;
  if(p.st==='du'||p.st==='part') return Math.max(0,+p.reste||0); return 0; };

/* ---------- TOUS les clients, fondus par le nom ---------- */
let TOUS=[];
function construit(){
  _ALX=null; _RFD=null;
  const M={};
  const get=(nom)=>{ nom=canon(nom); const k=cNorm(nom); if(!k) return null;
    if(!M[k]) M[k]={nom:String(nom).trim(),k,types:new Set(),achats:[],devis:[],co:{},tableur:null,site:null,ecritures:[],douteux:[]};
    return M[k]; };
  /* 1. le tableur de Sam : les commandes de gros d'avant l'outil */
  (D.clients||[]).forEach(c=>{ const o=get(c.nom); if(!o) return; o.types.add('gros'); o.tableur=c; o.ecritures=c.ecritures||[];
    c.cmds.forEach(x=>{
      if(x.douteux){ o.douteux.push(x); return; }
      if(x.devis){ o.devis.push({src:'tableur',d:x.d||'',num:x.num||'',total:x.total||0}); return; }
      o.achats.push({src:'tableur',id:pkey(c.nom,x),cnom:c.nom,x,d:x.d||'',de:!!x.de,h:'',num:x.num||'',canal:'Gros (tableur)',montant:+x.total||0,
        fl:x.l.reduce((s,l)=>s+(+l[Q]||0),0),
        lignes:x.l.map(l=>({nom:l[NOM],marque:l[MARQUE],ml:l[ML],type:l[TYPE]||'',bc:l[BC],q:+l[Q]||0,p:l[P]==null?null:+l[P],t:+l[T]||0,cle:BC2CLE[String(l[BC]||'').replace(/^0+/,'')]||''})),
        pay:payInit(c.nom,x),f:/x/i.test(x.f)||(x.l.length&&x.l.every(l=>/x/i.test(l[FACTC]))),s:/x/i.test(x.s)||(x.l.length&&x.l.every(l=>/x/i.test(l[SORTI]))),note:x.note||''}); }); });
  /* 2. les ventes enregistrées dans l'outil : site, caisse, boutique, gros, Amazon */
  /* un nom qui n'en est pas un (« [object Object] » de la caisse, phrase d'email Amazon) ne fait pas un client */
  FACT.forEach(f=>{ if(!f||!faNomClient(f.tiers)||(f.sens!=='vente'&&f.sens!=='devis')) return; const o=get(faNomClient(f.tiers)); if(!o) return;
    if(f.sens==='devis'||(f.doc&&f.doc.type==='devis')){ o.devis.push({src:'erp',d:f.d||'',num:(f.doc&&f.doc.num)||f.num||'',total:+((f.doc&&f.doc.total)||f.montant)||0}); return; }
    /* le statut fiscal retenu sur sa dernière facture (resale, passeport) */
    if(f.doc&&f.doc.fiscal&&!o.co.fiscal){ o.co.fiscal=f.doc.fiscal; if(f.doc.fref) o.co.fiscalRef=f.doc.fref; }
    const canal=f.canal||'Boutique'; o.types.add(typeCanal(canal,f));
    const L=(f.lignes||[]).map(l=>{ const fi=fiche(l.cle);
      return {nom:l.ref||'',marque:(fi&&fi[2])||'',ml:(fi&&fi[3])||'',type:(fi&&fi[4])||'',
              bc:l.bc||'',q:+l.q||0,p:l.p==null?null:+l.p,t:(+l.q||0)*(+l.p||0),cle:l.cle||''}; });
    o.achats.push({src:'erp',id:f.id,d:f.d||'',h:f.h||(f.t&&typeof heureMiami==='function'?heureMiami(f.t):''),num:f.doc?f.doc.num:(f.num||''),canal,
      montant:+(f.doc?f.doc.total:f.montant)||0,fl:L.reduce((s,l)=>s+l.q,0),lignes:L,pay:payErp(f),retour:!!f.retour,motif:f.motif||'',f}); });
  /* 3. la liste des clients du site : des coordonnées, et ce que le site dit d'eux */
  let RET=[]; try{ const t=lit(KRET,null); RET=Array.isArray(t)?t:(Array.isArray(window.D_RETAIL)?window.D_RETAIL:[]); }catch(e){}
  RET.forEach(r=>{ if(!r||!r.nom) return; const o=get(r.nom); if(!o) return; o.types.add('site'); o.site=r;
    ['email','tel','ville','pays'].forEach(k=>{ if(r[k]&&!o.co[k]) o.co[k]=r[k]; }); });
  /* 4. les fiches de l'outil : les coordonnées corrigées ici l'emportent ; un nom sans vente reste un client */
  /* les fiches enregistrées sous un ancien nom passent d'abord : celle du nom retenu l'emporte */
  Object.keys(CLI).sort((a,b)=>(canon(a)===a?1:0)-(canon(b)===b?1:0)).forEach(nom=>{ if(!faNomClient(nom)) return; const c=CLI[nom]||{}; const o=get(nom); if(!o) return;
    ['email','tel','tel2','tel3','prenom','nomfam','raison','adresse','note','fiscal','fiscalRef','pmode','ville','pays','nodiff'].forEach(k=>{ if(c[k]) o.co[k]=c[k]; }); });
  TOUS=Object.values(M).map(o=>{
    o.achats.sort((a,b)=>(b.d||'').localeCompare(a.d||'')||(b.h||'').localeCompare(a.h||''));
    const v=o.achats.filter(a=>!a.retour);
    o.total=o.achats.reduce((s,a)=>s+a.montant,0); o.nb=v.length; o.fl=o.achats.reduce((s,a)=>s+(a.retour?-Math.abs(a.fl):a.fl),0);
    o.der=v.reduce((m,a)=>a.d>m?a.d:m,''); o.prem=v.reduce((m,a)=>(!m||(a.d&&a.d<m))?a.d:m,'');
    o.reste=o.achats.reduce((s,a)=>s+resteDe(a),0);
    return o; });
  return TOUS;
}
const parNom=nom=>TOUS.find(o=>o.k===cNorm(canon(nom)))||null;

function lignes(){
  const per=+$('per').value, q=cNorm($('q').value), typ=$('typ').value;
  const lim=per?isoJour(new Date(AUJ.getTime()-per*864e5)):null;
  return TOUS.filter(o=>!q||[o.nom,o.co.prenom,o.co.nomfam,o.co.email,o.co.ville,o.co.tel,o.co.tel2,o.co.tel3,o.co.raison].some(v=>cNorm(v).includes(q)))
    .filter(o=>typ==='vip'?estVip(o.nom):typ==='sans'?!o.achats.length:(!typ||o.types.has(typ)))
    .map(o=>{ const A=o.achats.filter(a=>!lim||(a.d&&a.d>=lim)), v=A.filter(a=>!a.retour);
      return {o,A,vip:estVip(o.nom),total:A.reduce((s,a)=>s+a.montant,0),nb:v.length,fl:A.reduce((s,a)=>s+(a.retour?-Math.abs(a.fl):a.fl),0),der:v.reduce((m,a)=>a.d>m?a.d:m,'')}; })
    /* un favori reste visible même s'il n'a rien acheté sur la période :
       c'est justement pour le retrouver vite qu'on l'a mis en favori */
    .filter(r=>typ==='sans'||typ==='vip'||r.vip||r.nb||!lim&&(r.o.site||r.o.devis.length||Object.keys(r.o.co).length));
}
const badges=o=>[...o.types].map(t=>`<span class="tg ${t}">${TYPES[t]||t}</span>`).join('');

function dessine(){
  _ALX=null;
  const R=lignes();
  const rang=r=>TRI==='nb'?-r.nb : TRI==='dt'?0 : TRI==='fl'?-r.fl : -r.total;
  R.sort((a,b)=>{
    /* les favoris tiennent le haut de la liste, quel que soit le tri choisi :
       c'est ce qu'on attend d'un favori. À l'intérieur, le tri demandé. */
    const va=a.vip?0:1, vb=b.vip?0:1; if(va!==vb) return va-vb;
    return TRI==='nb'?b.nb-a.nb : TRI==='dt'?(b.der||'').localeCompare(a.der||'') : TRI==='az'?a.o.nom.localeCompare(b.o.nom,'fr') : TRI==='fl'?b.fl-a.fl : b.total-a.total; });
  const tot=R.reduce((a,r)=>a+r.total,0), ncmd=R.reduce((a,r)=>a+r.nb,0), max=Math.max(...R.map(r=>r.total),0);
  const nGros=TOUS.filter(o=>o.types.has('gros')).length, nSite=TOUS.filter(o=>o.types.has('site')).length;
  const du=TOUS.reduce((s,o)=>s+o.reste,0);
  $('kpis').innerHTML=`<div class="kpis">
    <div class="kpi"><div class="v">${nf(TOUS.length)}</div><div class="k">clients — ${nf(nGros)} en gros, ${nf(nSite)} du site</div></div>
    ${voitCA()?`<div class="kpi"><div class="v i">${money(tot)}</div><div class="k">vendu aux clients affichés</div></div>`:''}
    <div class="kpi"><div class="v">${nf(ncmd)}</div><div class="k">achats sur la période</div></div>
    ${voitCA()?`<div class="kpi"><div class="v${du>0?' c':''}" style="${du>0?'color:var(--crit)':''}">${money(du)}</div><div class="k">reste à encaisser, tous clients</div></div>`:''}</div>`;
  const th=(k,l,cls)=>`<th class="${cls||''}${TRI===k?' on':''}" data-k="${k}">${l}</th>`;
  $('corps').innerHTML = R.length ? `<div class="wrapx"><table class="tbl"><thead><tr>
      <th class="coch"><input type="checkbox" class="ck" id="cktout" title="Tout cocher / tout décocher"></th><th class="fav" title="Favoris">★</th>${th('az','Client')}${voitCA()?th('mt','Vendu à ce client','n'):''}${th('nb','Achats','n')}${th('fl','Flacons','n')}${th('dt','Dernier achat','n')}</tr></thead>
      <tbody>${R.map((r,i)=>`<tr data-c="${esc(r.o.nom)}"${r.vip?' class="vip"':''}>
        <td class="coch"><input type="checkbox" class="ck" data-ck="${esc(r.o.nom)}"${COCHES.has(r.o.nom)?' checked':''}></td>
        <td class="fav"><button class="et${r.vip?' on':''}" data-fav="${esc(r.o.nom)}" title="${r.vip?'Retirer des favoris':'Mettre en favoris'}">${r.vip?'★':'☆'}</button></td>
        <td class="nom"><span data-nolang>${esc(r.o.nom)}</span>${badges(r.o)}${r.o.douteux.length?'<span class="warn">à vérifier</span>':''}${r.o.reste>0&&voitCA()?`<span class="warn">${money(r.o.reste)} à payer</span>`:''}<small data-nolang>${esc([r.o.co.raison,r.o.co.email,r.o.co.tel,r.o.co.ville].filter(Boolean).join(' · '))}</small></td>
        ${voitCA()?`<td class="n mt">${r.nb||r.total?money(r.total):'<span class="non">—</span>'}<div class="bar"><i style="width:${max?Math.max(1,r.total/max*100):0}%"></i></div></td>`:''}
        <td class="n">${r.nb?nf(r.nb):'<span class="non">—</span>'}${r.o.devis.length&&!r.nb?`<small style="display:block;color:var(--ink-3)">${r.o.devis.length} devis</small>`:''}</td>
        <td class="n dim">${r.fl?nf(Math.round(r.fl)):'—'}</td><td class="n dim">${r.der?dfr(r.der):(r.o.site&&r.o.site.der?'<span title="d\'après le fichier du site">'+dfr(r.o.site.der)+' ≈</span>':'—')}</td></tr>`).join('')}</tbody>
      <tfoot><tr><td></td><td></td><td style="font-weight:700">${R.length} clients</td>${voitCA()?`<td class="n mt">${money(tot)}</td>`:''}<td class="n" style="font-weight:700">${nf(ncmd)}</td><td class="n dim">${nf(Math.round(R.reduce((a,r)=>a+r.fl,0)))}</td><td></td></tr></tfoot></table></div>`
    : `<div class="vide">Aucun client ne correspond.</div>`;
  document.querySelectorAll('.tbl tbody tr').forEach(el=>el.onclick=e=>{
    /* l'étoile et la case ne doivent pas ouvrir la fiche */
    if(e.target.closest('[data-fav]')||e.target.closest('[data-ck]')) return;
    ouvre(el.dataset.c); });
  document.querySelectorAll('.tbl th[data-k]').forEach(el=>el.onclick=()=>{ TRI=el.dataset.k; dessine(); });
  document.querySelectorAll('[data-fav]').forEach(b=>b.onclick=e=>{
    e.stopPropagation(); basculeVip(b.dataset.fav); dessine(); });
  document.querySelectorAll('[data-ck]').forEach(c=>c.onclick=e=>{
    e.stopPropagation();
    if(c.checked) COCHES.add(c.dataset.ck); else COCHES.delete(c.dataset.ck);
    peintSel(); });
  const kt=$('cktout');
  if(kt){ kt.checked=R.length>0 && R.every(r=>COCHES.has(r.o.nom));
    kt.onclick=e=>{ e.stopPropagation();
      R.forEach(r=>{ if(kt.checked) COCHES.add(r.o.nom); else COCHES.delete(r.o.nom); });
      dessine(); }; }
  peintSel();
  $('src').innerHTML=`${nf(TOUS.length)} clients<br>tableur lu le ${dfr(D.date)}`;
  const ct=document.getElementById('ct-clients'); if(ct) ct.textContent=nf(TOUS.length);
}

/* ---------- la barre de sélection ----------
   Elle n'apparaît que lorsqu'au moins une case est cochée : tant qu'on ne
   sélectionne rien, elle ne prend pas de place et ne pose pas de question. */
function peintSel(){
  const n=COCHES.size, b=$('selbar'); if(!b) return;
  b.classList.toggle('on', n>0);
  if(!n) return;
  $('selnb').textContent=nf(n);
  $('sellib').textContent=n>1?'clients sélectionnés':'client sélectionné';
  const dejaVip=[...COCHES].filter(estVip).length;
  $('selvip').style.display = dejaVip===n ? 'none' : '';
  $('selnon').style.display = dejaVip===0 ? 'none' : '';
}
function selClients(){
  return [...COCHES].map(nom=>parNom(nom)).filter(Boolean)
    .map(o=>({nom:o.nom, email:o.co.email||'', tel:o.co.tel||''}));
}

/* Écrire à un client : même fenêtre que les Fournisseurs. */
function jlogContact(nom,par,quoi){
  const J=lit(KJOU,[]);
  J.push({t:new Date().toISOString(),u:USR||'(non renseigné)',act:'contact',lib:'message préparé — '+quoi,ref:nom,av:null,ap:par});
  ecrit(KJOU,J);
}
function ecrire(o){
  contacte({nom:o.nom, email:o.co.email, tel:o.co.tel, modele:'promo',
    onSave:(mail,tel)=>{
      if(mail===(o.co.email||'') && tel===(o.co.tel||'')) return;
      CLI[o.nom]=Object.assign({},CLI[o.nom]||{},{nom:o.nom,email:mail||undefined, tel:tel||undefined, maj:new Date().toISOString()});
      sauveCLI(); construit(); dessine();
    }});
}

/* ---------- fiche client ---------- */
let OUV=null;
function ouvre(nom){
  const o=parNom(nom); if(!o) return; OUV=o;
  const v=o.achats.filter(a=>!a.retour);
  $('dnom').innerHTML=`<span data-nolang>${esc(o.nom)}</span>${badges(o)}`;
  $('dco').innerHTML=[[o.co.prenom,o.co.nomfam].filter(Boolean).join(' '),o.co.raison,o.co.email,o.co.tel,o.co.tel2,o.co.tel3,[o.co.ville,o.co.pays].filter(Boolean).join(', ')].filter(Boolean).map(x=>`<span data-nolang>${esc(x)}</span>`).join(' · ')||'<span class="non">pas de coordonnées — onglet Coordonnées</span>';
  const dus=o.achats.filter(a=>resteDe(a)>0);
  $('dk').innerHTML=(voitCA()?`<div><b class="i">${money(o.total)}</b><span>vendu à ce client au total</span></div>
    <div><b>${nf(v.length)}</b><span>achats · ${v.length?money(o.total/v.length):'—'} en moyenne</span></div>
    <div><b class="${o.reste>0?'c':''}">${money(o.reste)}</b><span>reste à payer${dus.length?' · '+dus.length+' achat'+(dus.length>1?'s':''):''}</span></div>`
    :`<div><b>${nf(v.length)}</b><span>achats</span></div>`)+`
    <div><b>${dfr(o.der)}</b><span>dernier achat${o.prem?' · premier le '+dfr(o.prem):''}</span></div>`;
  $('drel').disabled=!dus.length||!voitCA(); $('drel').title=dus.length?'':'Rien à relancer : aucun achat marqué « À payer ».'; $('drel').hidden=!voitCA();
  $('drel').onclick=()=>relance(o,dus);
  $('decr').onclick=()=>ecrire(o);
  const fv=$('dfav');
  const peintEtoile=()=>{ const v=estVip(o.nom);
    fv.textContent=v?'★':'☆'; fv.classList.toggle('on',v);
    fv.title=v?'Retirer des favoris':'Mettre ce client en favoris'; };
  peintEtoile();
  fv.onclick=()=>{ basculeVip(o.nom); peintEtoile(); dessine(); };

  /* onglet achats : tout, dans l'ordre, avec l'heure et le paiement */
  const A=o.achats;
  /* le détail d'une commande (ses parfums) ne se dessine qu'au clic : un client à 196 commandes en
     portait des milliers de lignes cachées, et chaque changement de règlement refaisait tout (13 oct.) */
  const ligHtml=a=>`${a.lignes.length?`<table><thead><tr><th>Parfum</th><th>Marque</th><th>Cont.</th><th class="n">Prix</th><th class="n">Qté</th><th class="n">Montant</th></tr></thead><tbody>${
        a.lignes.map(l=>`<tr><td data-nolang>${l.cle?`<a href="catalogue.html#cle=${esc(l.cle)}" title="ouvrir la fiche catalogue">${esc(l.nom)}</a>`:esc(l.nom)}${tyBadge(...tyDe(l))}</td><td data-nolang>${esc(l.marque)}</td><td>${esc(l.ml)}</td><td class="n">${l.p!=null?money2(l.p):'—'}</td><td class="n">${nf(l.q)}</td><td class="n"><b>${money2(l.t)}</b></td></tr>`).join('')}</tbody></table>`
        :'<span class="est">Le tableur ne donne que le total de cette commande.</span>'}`;
  const remplitLig=i=>{ const l=document.querySelector(`#p-cmd tr.lig[data-i="${i}"]`); if(l&&!l.dataset.ok){ l.firstElementChild.innerHTML=ligHtml(A[i]); l.dataset.ok='1'; } return l; };
  window.__remplitLig=remplitLig;
  $('p-cmd').innerHTML=`${o.douteux.length?`<div class="avert"><b>À vérifier dans le tableur :</b> ${o.douteux.map(x=>`commande ${esc(x.num||'sans n°')} notée ${money(x.total)} (ligne ${x.ls})`).join(', ')} — montant invraisemblable, laissé de côté.</div>`:''}
    ${o.site&&(o.site.nb||o.site.total)?`<div class="avert"><b>D'après le fichier du site :</b> ${nf(o.site.nb||0)} commande${(o.site.nb||0)>1?'s':''} pour ${money(o.site.total||0)}${o.site.der?', la dernière le '+dfr(o.site.der):''}. Le détail n'est connu que pour les commandes arrivées dans l'outil.</div>`:''}
    ${A.length?`<div class="barre2"><span>Clique sur un achat pour voir ses parfums. Le règlement des commandes du tableur se note ici ; celui des factures de l'outil se règle dans Factures.</span>
      <span class="sp"></span>${A.some(a=>a.src==='tableur')?'<button class="btn sm" id="toutpaye">Marquer les commandes du tableur comme payées</button>':''}</div>
    <table class="t2"><thead><tr><th>Date</th><th>Heure</th><th>N°</th><th>Canal</th><th class="n">Parfums</th><th class="n">Montant</th><th>Paiement</th></tr></thead>
    <tbody>${A.map((a,i)=>{
      const p=a.pay||{}, k=a.id, cls=p.st==='du'?'du':p.st==='paye'?'ok':p.st==='part'?'part':'';
      const paie = a.src==='tableur'
        ? `<select class="pay ${cls}" data-k="${esc(k)}" data-f="st" onclick="event.stopPropagation()">${STATUTS.map(([v,l])=>`<option value="${v}"${p.st===v?' selected':''}>${l}</option>`).join('')}</select>
           <select class="pay" data-k="${esc(k)}" data-f="mode" onclick="event.stopPropagation()">${MODES.map(([v,l])=>`<option value="${v}"${p.mode===v?' selected':''}>${l}</option>`).join('')}</select>${p.st==='part'?` <input class="part" data-k="${esc(k)}" data-f="regle" type="number" step="any" value="${p.regle||''}" placeholder="réglé $" onclick="event.stopPropagation()"> <span class="reste">reste <b>${money2(Math.max(0,a.montant-(+p.regle||0)))}</b></span>`:''}${p.rel?`<span class="rel">relancé le ${dfr(p.rel)}</span>`:''}`
        : payLib(p)+((PAY['erp|'+k]||{}).rel?`<span class="rel">relancé le ${dfr(PAY['erp|'+k].rel)}</span>`:'')
          +(a.f&&a.f.doc?` <a class="voir" href="ventes.html#doc=${encodeURIComponent(k)}" onclick="event.stopPropagation()" title="Ouvrir la facture : la voir, l'envoyer par WhatsApp ou par e-mail, télécharger le PDF">Voir la facture</a>`:'');
      return `<tr class="cmd${a.retour?' ret':''}" data-i="${i}">
        <td>${a.d?(a.de?`<span class="est" title="date absente du tableur, reprise de la commande voisine">≈ ${dfr(a.d)}</span>`:dfr(a.d)):'—'}</td>
        <td class="hh">${a.h?esc(a.h):'<span class="est">—</span>'}</td>
        <td>${a.num?esc(a.num):'<span class="est">sans n°</span>'}${a.retour?' <span class="tg retour">retour</span>':''}${a.note?` · <span class="est" data-nolang>${esc(a.note)}</span>`:''}</td>
        <td><span data-nolang>${esc(a.canal)}</span>${a.src==='tableur'?`<small style="display:block;color:var(--ink-3)">${a.f?'facturée':'—'} · ${a.s?'sortie':'—'}</small>`:''}</td>
        <td class="n">${a.lignes.length?nf(a.lignes.length):'<span class="est">total seul</span>'}</td><td class="n mt">${money2(a.montant)}</td>
        <td>${paie}</td></tr>
      <tr class="lig" data-i="${i}" hidden><td colspan="7"></td></tr>`; }).join('')}</tbody></table>`
    :`<div class="vide">Aucun achat enregistré pour ce client.${o.site?' Le site l\'a inscrit ; ses commandes apparaîtront ici quand elles arriveront dans l\'outil.':''}</div>`}
    ${o.devis.length?`<p class="ecr">${o.devis.length} devis pour ${money(o.devis.reduce((a,x)=>a+x.total,0))}, non comptés dans les achats.</p>`:''}`;
  document.querySelectorAll('#p-cmd tr.cmd').forEach(tr=>tr.onclick=e=>{ if(e.target.closest('select,input')) return;
    const l=remplitLig(tr.dataset.i); l.hidden=!l.hidden; tr.classList.toggle('on',!l.hidden); });
  document.querySelectorAll('#p-cmd .pay, #p-cmd input.part').forEach(el=>el.onchange=()=>{
    const k=el.dataset.k, a=A.find(y=>y.id===k); if(!a||a.src!=='tableur') return;
    const p=Object.assign({},payInit(a.cnom,a.x),PAY[k]||{});
    if(el.dataset.f==='regle') p.regle=+el.value||0; else p[el.dataset.f]=el.value;
    delete p.src; p.maj=new Date().toISOString(); p.u=USR||''; PAY[k]=p; sauvePAY();
    const lib=el.dataset.f==='st'?'règlement : '+(STATUTS.find(s=>s[0]===p.st)||['','—'])[1]:el.dataset.f==='mode'?'mode de règlement : '+(MODES.find(m=>m[0]===p.mode)||['','—'])[1]:'montant réglé : '+money(p.regle);
    journal('client',lib,o.nom+' · commande '+(a.num||'sans n°'),money(a.montant)); redessineFiche(o.nom); });
  const tp=$('toutpaye'); if(tp) tp.onclick=()=>{ let n=0; A.filter(a=>a.src==='tableur').forEach(a=>{ const k=a.id; const p=Object.assign({},payInit(a.cnom,a.x),PAY[k]||{}); if(p.st!=='paye'){ p.st='paye'; delete p.src; p.maj=new Date().toISOString(); p.u=USR||''; PAY[k]=p; n++; } });
    if(n){ sauvePAY(); journal('client',n+' commandes marquées payées',o.nom,null); redessineFiche(o.nom); } };

  /* onglet parfums */
  const M={}; v.forEach(a=>a.lignes.forEach(l=>{ const k=l.cle||l.bc||cNorm(l.nom); const m=(M[k]=M[k]||{nom:l.nom,marque:l.marque,ml:l.ml,type:l.type||'',bc:l.bc,cle:l.cle,q:0,t:0,n:0,der:''}); m.q+=l.q; m.t+=l.t; m.n++; if(a.d>m.der) m.der=a.d; if(!m.marque&&l.marque) m.marque=l.marque; }));
  const prodsTous=Object.values(M).sort(PTRI==='mt'?(a,b)=>b.t-a.t||b.q-a.q:(a,b)=>b.q-a.q||b.t-a.t);
  /* 13 oct. 2026 (Igal) : le top 10 ou 20 des parfums qu'un client prend le plus */
  const prods=PTOP?prodsTous.slice(0,PTOP):prodsTous;
  const MQ={}; prods.forEach(p=>{ if(p.marque) MQ[p.marque]=(MQ[p.marque]||0)+p.t; });
  const mq=Object.entries(MQ).sort((a,b)=>b[1]-a[1]).slice(0,8);
  const barreTop=`<div class="ptop"><span>Afficher</span>${[[10,'Top 10'],[20,'Top 20'],[0,'Tous']].map(([n,l])=>`<button class="btn sm${PTOP===n?' on':''}" data-top="${n}">${l}</button>`).join('')}
    <span class="sp"></span><span>Classer par</span>${[['q','Flacons'],['mt','Montant']].map(([k,l])=>`<button class="btn sm${PTRI===k?' on':''}" data-ptri="${k}">${l}</button>`).join('')}</div>`;
  $('p-prod').innerHTML=prods.length?`<p class="ecr" style="margin:0 0 10px">${nf(prodsTous.length)} parfums différents${PTOP&&prodsTous.length>PTOP?', les '+nf(PTOP)+' premiers sont affichés':''}.${mq.length?' Ses marques : '+mq.map(([m,t])=>`<b data-nolang>${esc(m)}</b> ${money(t)}`).join(' · ')+'.':''}</p>
    ${barreTop}<table class="t2"><thead><tr><th></th><th>Parfum</th><th>Marque</th><th class="n">Fois acheté</th><th class="n">Flacons</th><th class="n">Montant</th><th class="n">Dernier achat</th></tr></thead>
    <tbody>${prods.map((p,i)=>`<tr><td class="n" style="color:var(--ink-3);width:30px">${i+1}</td><td class="nom" data-nolang>${p.cle?`<a href="catalogue.html#cle=${esc(p.cle)}" style="color:inherit;text-decoration:none">${esc(p.nom)}</a>`:esc(p.nom)}${tyBadge(...tyDe(p))}<small>${p.ml?esc(p.ml)+' oz':''}${p.bc?' · '+esc(p.bc):''}</small></td><td data-nolang>${esc(p.marque)}</td><td class="n">${nf(p.n)}</td><td class="n">${nf(Math.round(p.q))}</td><td class="n mt">${money(p.t)}</td><td class="n dim">${dfr(p.der)}</td></tr>`).join('')}</tbody></table>`
    :`<div class="vide">Aucun parfum acheté pour l'instant.</div>`;
  document.querySelectorAll('#p-prod [data-top]').forEach(b=>b.onclick=()=>{ PTOP=+b.dataset.top; ouvre(o.nom); onglet('prod'); });
  document.querySelectorAll('#p-prod [data-ptri]').forEach(b=>b.onclick=()=>{ PTRI=b.dataset.ptri; ouvre(o.nom); onglet('prod'); });

  /* onglet coordonnées */
  const co=Object.assign({},o.co,CLI[o.nom]||{});
  const FISC={taxable:'Taxable (Floride)',resale:'Exonéré — resale certificate',etranger:'Exonéré — client étranger (passeport)'};
  $('p-coord').innerHTML=`<div class="ed">
      <label>Prénom<input id="e-prenom" value="${esc(co.prenom||'')}"></label>
      <label>Nom<input id="e-nomfam" value="${esc(co.nomfam||'')}"></label>
      <label>Téléphone 1<input id="e-tel" value="${esc(co.tel||'')}"></label>
      <label>E-mail<input id="e-email" value="${esc(co.email||'')}"></label>
      <label>Téléphone 2<input id="e-tel2" value="${esc(co.tel2||'')}"></label>
      <label>Téléphone 3<input id="e-tel3" value="${esc(co.tel3||'')}"></label>
      <label>Société<input id="e-raison" value="${esc(co.raison||'')}"></label>
      <label>Adresse<input id="e-adresse" value="${esc(co.adresse||'')}"></label>
      <label>Ville<input id="e-ville" value="${esc(co.ville||'')}"></label>
      <label>Pays<input id="e-pays" value="${esc(co.pays||'')}"></label>
      <label style="grid-column:1/-1">Note<textarea id="e-note" placeholder="Conditions, délais, remarques…">${esc(co.note||'')}</textarea></label>
    </div>
    <p style="margin:14px 0 0"><button class="btn pri" id="e-ok">Enregistrer</button> <span id="e-msg" style="font-size:13px;color:var(--good);margin-left:8px"></span></p>
    <p class="ecr">${co.fiscal?`Statut fiscal retenu sur ses factures : <b>${esc(FISC[co.fiscal]||co.fiscal)}</b>${co.fiscalRef?' — n° <span data-nolang>'+esc(co.fiscalRef)+'</span>':''}. `:''}Ces coordonnées sont gardées dans l'outil.${o.ecritures.length?`<br>Dans le tableur, ce client est écrit : <b data-nolang>${o.ecritures.slice(0,6).map(esc).join('</b>, <b data-nolang>')}</b>${o.ecritures.length>6?' …':''}.`:''}${o.site?'<br>Inscrit sur le site.':''}</p>
    <div class="pjs"><h4>Pièces jointes : resale certificate, passeport</h4>
      <div id="pj-liste"></div>
      <div class="pjadd"><select id="pj-type"><option value="resale">Resale certificate</option><option value="passeport">Passeport</option><option value="autre">Autre pièce</option></select>
        <label class="btn" for="pj-f">Joindre une photo ou un PDF</label><input type="file" id="pj-f" accept="image/*,application/pdf,.heic" hidden>
        <span id="pj-msg" class="pjmsg"></span></div>
      <p class="ecr" style="margin:6px 0 0">Ces pièces ne sont jamais publiques : seuls les comptes de l'ERP peuvent les ouvrir.</p></div>`;
  pjPeint(o.nom);
  $('pj-f').onchange=e=>{ const f=e.target.files[0]; e.target.value=''; if(f) pjDepose(o.nom,f,$('pj-type').value); };
  $('e-ok').onclick=()=>{
    /* 7 nov. 2026 (Igal) : trois numéros de téléphone ; une case vidée efface le numéro (avant, un champ vidé gardait l'ancien) */
    const n={nom:o.nom}; ['prenom','nomfam','tel','tel2','tel3','email','raison','adresse','ville','pays','note'].forEach(k=>{ const val=$('e-'+k).value.trim(); if(val) n[k]=val; else if(/^tel[23]$/.test(k)) n[k]=undefined; });
    CLI[o.nom]=Object.assign({},CLI[o.nom]||{},n,{maj:new Date().toISOString()}); Object.keys(CLI[o.nom]).forEach(k=>{ if(CLI[o.nom][k]===undefined) delete CLI[o.nom][k]; }); sauveCLI();
    journal('client','fiche client modifiée',o.nom,'coordonnées');
    $('e-msg').textContent='enregistré'; setTimeout(()=>$('e-msg').textContent='',2000); construit(); dessine(); };
  onglet('cmd');
  $('dr').classList.add('on'); $('drov').classList.add('on'); document.querySelector('.db').scrollTop=0;
}
/* ---------- pièces jointes du client (2 oct. 2026) ----------
   Sam : « une pièce jointe pour le resale certificate ou le passeport des acheteurs étrangers,
   dans les coordonnées du client ». Le fichier part au cockpit, dans un coin privé : seule une
   session de l'ERP l'ouvre (jamais de lien public). La fiche du client garde la liste : type,
   nom du fichier, date, qui l'a joint. Retirer le met de côté au cockpit, il ne se détruit pas. */
const PJ_LIB={resale:'Resale certificate',passeport:'Passeport',autre:'Autre pièce'};
const pjUrl=id=>CK_URL+'/api/o/'+CK_ORG+'/pieces/'+encodeURIComponent(id);
const pjEnLigne=()=>typeof CK_URL!=='undefined'&&typeof ckTok==='function'&&!!ckTok();
function pjPeint(nom){
  const el=$('pj-liste'); if(!el) return;
  const L=((CLI[nom]||{}).pieces)||[];
  el.innerHTML=L.length?`<table class="t2 pjt"><tbody>${L.map(p=>`<tr><td><b>${esc(PJ_LIB[p.type]||p.type)}</b></td>
      <td data-nolang>${esc(p.nom||'')}<small>${dfr(p.t)}${p.par?' · '+esc(p.par):''}</small></td>
      <td class="n"><button class="btn sm" data-pjv="${esc(p.id)}">Voir</button> <button class="btn sm" data-pjr="${esc(p.id)}">Retirer</button></td></tr>`).join('')}</tbody></table>`
    :'<p class="ecr" style="margin:0">Aucune pièce jointe.</p>';
  el.querySelectorAll('[data-pjv]').forEach(b=>b.onclick=()=>pjVoir(b.dataset.pjv));
  el.querySelectorAll('[data-pjr]').forEach(b=>b.onclick=()=>pjRetire(nom,b.dataset.pjr));
}
async function pjDepose(nom,f,type){
  const m=$('pj-msg');
  if(!pjEnLigne()){ m.textContent='Les pièces jointes se déposent depuis l\'ERP en ligne.'; return; }
  let mime=f.type||''; if(!mime&&/\.hei[cf]$/i.test(f.name)) mime='image/heic';
  if(!/^(image\/(jpeg|png|webp|heic|heif)|application\/pdf)$/.test(mime)){ m.textContent='Il faut une photo (JPEG, PNG, HEIC) ou un PDF.'; return; }
  if(f.size>10*1024*1024){ m.textContent='Fichier trop lourd (10 Mo au plus).'; return; }
  const id='pj'+Date.now().toString(36)+Math.random().toString(36).slice(2,8);
  m.textContent='Envoi…';
  try{
    const r=await fetch(pjUrl(id),{method:'PUT',headers:{'Content-Type':mime,Authorization:'Bearer '+ckTok()},body:f});
    const j=await r.json().catch(()=>({}));
    if(!r.ok) throw new Error(j.erreur||('erreur '+r.status));
    { const c=lit(KCLI,null); if(c&&typeof c==='object') CLI=c; }
    const x=Object.assign({},CLI[nom]||{},{nom});
    x.pieces=(Array.isArray(x.pieces)?x.pieces:[]).concat([{id,type,nom:f.name,ext:j.ext,taille:j.taille,t:new Date().toISOString(),par:USR||''}]);
    x.maj=new Date().toISOString(); CLI[nom]=x; sauveCLI();
    journal('client','pièce jointe ajoutée : '+(PJ_LIB[type]||type)+' ('+f.name+')',nom,null);
    m.textContent='jointe'; setTimeout(()=>{ const z=$('pj-msg'); if(z&&z.textContent==='jointe') z.textContent=''; },2500);
    pjPeint(nom);
  }catch(e){ m.textContent='Pas jointe — '+((e&&e.message)||'échec'); }
}
async function pjVoir(id){
  if(!pjEnLigne()){ alert(vf('Les pièces jointes s\'ouvrent depuis l\'ERP en ligne.')); return; }
  const w=window.open('','_blank');
  try{
    const r=await fetch(pjUrl(id),{headers:{Authorization:'Bearer '+ckTok()}});
    if(!r.ok){ const j=await r.json().catch(()=>({})); throw new Error(j.erreur||('erreur '+r.status)); }
    const u=URL.createObjectURL(await r.blob());
    if(w) w.location.href=u; else window.location.href=u;
  }catch(e){ if(w) w.close(); alert(vf('Impossible d\'ouvrir la pièce — '+((e&&e.message)||'échec'))); }
}
async function pjRetire(nom,id){
  const p=(((CLI[nom]||{}).pieces)||[]).find(x=>x.id===id); if(!p) return;
  if(!confirm(vf('Retirer « '+(PJ_LIB[p.type]||p.type)+' — '+(p.nom||'')+' » de la fiche de '+nom+' ?'))) return;
  try{
    if(pjEnLigne()){ const r=await fetch(pjUrl(id),{method:'DELETE',headers:{Authorization:'Bearer '+ckTok()}}); if(!r.ok){ const j=await r.json().catch(()=>({})); throw new Error(j.erreur||('erreur '+r.status)); } }
    { const c=lit(KCLI,null); if(c&&typeof c==='object') CLI=c; }
    const x=Object.assign({},CLI[nom]||{}); x.pieces=(x.pieces||[]).filter(z=>z.id!==id); x.maj=new Date().toISOString(); CLI[nom]=x; sauveCLI();
    journal('client','pièce jointe retirée : '+(PJ_LIB[p.type]||p.type)+' ('+(p.nom||'')+')',nom,null);
    pjPeint(nom);
  }catch(e){ alert(vf('Pas retirée — '+((e&&e.message)||'échec'))); }
}
/* ---------- relance de paiement ---------- */
let REL=null;
const mon=(v,l)=>l==='fr'?money2(v):'$'+Number(v).toLocaleString(l==='es'?'es-ES':'en-US',{minimumFractionDigits:2,maximumFractionDigits:2});
const dl=(d,l)=>{ if(!d) return '—'; const [a,m,j]=String(d).slice(0,10).split('-'); return m+'/'+j+'/'+a.slice(2); };
const TXT={
 fr:(nom,L,tot,soc)=>`Bonjour ${nom},\n\nSauf erreur de notre part, ${L.length>1?'les commandes suivantes restent':'la commande suivante reste'} à régler :\n\n${L.map(a=>`  • ${a.num?'n° '+a.num:'commande'} du ${dfr(a.d)} — ${(a.pay||{}).st==='part'?`${money2(a.montant)}, reçu ${money2(regleDe(a))}, reste ${money2(resteDe(a))}`:money2(resteDe(a))}`).join('\n')}\n\nTotal : ${money2(tot)}\n\nMerci de nous indiquer la date de règlement, ou de nous signaler si un paiement a déjà été fait.\n\nBien cordialement,\n${soc}`,
 en:(nom,L,tot,soc)=>`Hi ${nom},\n\nUnless we missed something, the following ${L.length>1?'orders are':'order is'} still unpaid:\n\n${L.map(a=>`  • ${a.num?'#'+a.num:'order'} of ${dl(a.d,'en')} — ${(a.pay||{}).st==='part'?`${mon(a.montant,'en')}, received ${mon(regleDe(a),'en')}, balance ${mon(resteDe(a),'en')}`:mon(resteDe(a),'en')}`).join('\n')}\n\nTotal due: ${mon(tot,'en')}\n\nCould you let us know when the payment will be made, or tell us if it was already sent?\n\nThank you,\n${soc}`,
 es:(nom,L,tot,soc)=>`Hola ${nom},\n\nSalvo error de nuestra parte, ${L.length>1?'los siguientes pedidos siguen pendientes':'el siguiente pedido sigue pendiente'} de pago:\n\n${L.map(a=>`  • ${a.num?'n.º '+a.num:'pedido'} del ${dl(a.d,'es')} — ${(a.pay||{}).st==='part'?`${mon(a.montant,'es')}, recibido ${mon(regleDe(a),'es')}, saldo ${mon(resteDe(a),'es')}`:mon(resteDe(a),'es')}`).join('\n')}\n\nTotal: ${mon(tot,'es')}\n\n¿Nos puede indicar la fecha de pago, o avisarnos si ya fue realizado?\n\nGracias,\n${soc}`};
function relance(o,dus){
  let soc='Perfumes Trade'; try{ const r=JSON.parse(localStorage.getItem('reglages-v1')||'{}'); if(r.societe) soc=r.societe; }catch(e){}
  const tot=dus.reduce((a,x)=>a+resteDe(x),0);
  REL={nom:o.nom,o,dus,tot,soc,lang:'fr'};
  $('relnom').textContent=o.nom; $('reltxt').value=TXT.fr(o.nom,dus,tot,soc); $('relmsg').textContent='';
  const co0=Object.assign({},o.co,CLI[o.nom]||{});
  $('reldest').value=co0.email||''; $('reldest').classList.remove('manque');
  $('reldn').textContent=co0.email?'':'aucune adresse dans la fiche — écris-la ici';
  $('reldn').className=co0.email?'':'err';
  document.querySelectorAll('#rellang button').forEach(b=>b.classList.toggle('on',b.dataset.l==='fr'));
  $('relov').classList.add('on'); $('reltxt').scrollTop=0;
}
document.querySelectorAll('#rellang button').forEach(b=>b.onclick=()=>{ if(!REL) return; REL.lang=b.dataset.l;
  document.querySelectorAll('#rellang button').forEach(x=>x.classList.toggle('on',x===b)); $('reltxt').value=TXT[b.dataset.l](REL.nom,REL.dus,REL.tot,REL.soc); });
function relFaite(voie){ if(!REL) return; const d=ajd(), nom=REL.nom;
  REL.dus.forEach(a=>{ const k=a.src==='tableur'?a.id:'erp|'+a.id; PAY[k]=Object.assign({},a.src==='tableur'?payInit(a.cnom,a.x):{},PAY[k]||{},{rel:d}); }); sauvePAY();
  journal('client','relance de paiement ('+voie+')',nom,money(REL.tot)+' · '+REL.dus.length+' achat'+(REL.dus.length>1?'s':''));
  $('relmsg').textContent='relance notée dans le journal — '+voie;
  setTimeout(()=>{ $('relov').classList.remove('on'); REL=null; }, 1400);
  construit(); ouvre(nom); onglet('cmd'); }
$('relmail').onclick=()=>{ if(!REL) return;
  const dest=$('reldest').value.trim();
  if(!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(dest)){
    $('reldest').classList.add('manque'); $('reldest').focus();
    $('reldn').textContent='adresse manquante ou mal écrite'; $('reldn').className='err';
    $('relmsg').textContent='rien n\'a été envoyé'; return; }
  $('reldest').classList.remove('manque'); $('reldn').textContent=''; $('reldn').className='';
  const co=CLI[REL.nom]||{};
  if(co.email!==dest){ CLI[REL.nom]=Object.assign({},co,{nom:REL.nom,email:dest,maj:new Date().toISOString()});
    sauveCLI(); journal('client','e-mail du client enregistré',REL.nom,dest); }
  const suj={fr:'Rappel de règlement',en:'Payment reminder',es:'Recordatorio de pago'}[REL.lang];
  const url='mailto:'+encodeURIComponent(dest)+'?subject='+encodeURIComponent(suj+' — '+REL.soc)+'&body='+encodeURIComponent($('reltxt').value);
  const a=document.createElement('a'); a.href=url; a.style.display='none';
  document.body.appendChild(a); a.click(); setTimeout(()=>a.remove(),0);
  relFaite('e-mail'); };
$('relwa').onclick=()=>{ if(!REL) return; const co=Object.assign({},REL.o.co,CLI[REL.nom]||{}); const tel=(co.tel||'').replace(/[^0-9]/g,'');
  if(!tel){ $('relmsg').textContent='pas de téléphone dans la fiche : ajoute-le dans Coordonnées'; return; }
  window.open('https://wa.me/'+(tel.length===10?'1'+tel:tel)+'?text='+encodeURIComponent($('reltxt').value),'_blank'); relFaite('WhatsApp'); };
$('relcopy').onclick=async()=>{ try{ await navigator.clipboard.writeText($('reltxt').value); }catch(e){ $('reltxt').select(); document.execCommand('copy'); } relFaite('texte copié'); };
$('relx').onclick=()=>{ $('relov').classList.remove('on'); REL=null; };

/* ---------- nouveau client ---------- */
$('nouv').onclick=()=>{ $('novnom').value=''; $('novmsg').textContent=''; $('novov').classList.add('on'); setTimeout(()=>$('novnom').focus(),50); };
$('novx').onclick=()=>$('novov').classList.remove('on');
$('novok').onclick=()=>{ const nom=$('novnom').value.trim(); if(!nom){ $('novmsg').textContent='il faut un nom'; return; }
  const deja=parNom(nom); if(deja){ $('novov').classList.remove('on'); ouvre(deja.nom); onglet('coord'); return; }
  CLI[nom]=Object.assign({},CLI[nom]||{},{nom,depuis:ajd(),maj:new Date().toISOString()}); sauveCLI();
  journal('client','fiche client créée',nom,null);
  construit(); dessine(); $('novov').classList.remove('on'); ouvre(nom); onglet('coord'); };
$('novnom').addEventListener('keydown',e=>{ if(e.key==='Enter') $('novok').click(); });

function onglet(t){ document.querySelectorAll('.tab').forEach(b=>b.classList.toggle('on',b.dataset.t===t));
  document.querySelectorAll('.pane').forEach(p=>p.classList.toggle('on',p.id==='p-'+t)); }
document.querySelectorAll('.tab').forEach(b=>b.onclick=()=>onglet(b.dataset.t));
function coordChangees(){
  if(!OUV) return false;
  const co=Object.assign({},OUV.co,CLI[OUV.nom]||{});
  return ['prenom','nomfam','tel','tel2','tel3','email','raison','adresse','ville','pays','note'].some(k=>{ const el=$('e-'+k); return el && el.value.trim()!==((co[k]||'').trim()); });
}
function ferme(force){
  if(!force && coordChangees() && !confirm("Les coordonnées saisies ne sont pas enregistrées.\n\nFermer quand même ? Ce qui a été tapé sera perdu.")) return;
  $('dr').classList.remove('on'); $('drov').classList.remove('on'); OUV=null;
}
$('dx').onclick=()=>ferme(false); $('drov').onclick=()=>ferme(false);
document.addEventListener('keydown',e=>{ if(e.key==='Escape'){ if(REL){ $('relov').classList.remove('on'); REL=null; } else if($('novov').classList.contains('on')) $('novov').classList.remove('on'); else if(OUV) ferme(false); } });

['q','per','typ'].forEach(i=>$(i).addEventListener('input',dessine));
poseSortie('exp', ()=>{
  const L=[];
  TOUS.forEach(o=>o.achats.forEach(a=>{ if(a.lignes.length) a.lignes.forEach(l=>L.push([o.nom,[...o.types].map(t=>TYPES[t]||t).join(' '),a.d||'',a.h||'',a.num,a.canal,a.retour?'retour':'',l.bc,l.nom,l.marque,l.p,l.q,l.t,(a.pay||{}).st||'',(a.pay||{}).mode||'']));
    else L.push([o.nom,[...o.types].map(t=>TYPES[t]||t).join(' '),a.d||'',a.h||'',a.num,a.canal,a.retour?'retour':'','','','',null,null,a.montant,(a.pay||{}).st||'',(a.pay||{}).mode||'']); }));
  return { titre:'Clients', fichier:'clients', filtre:'tous les achats de tous les clients',
    colonnes:[{t:'Client'},{t:'Type'},{t:'Date',y:'d'},{t:'Heure'},{t:'N°'},{t:'Canal'},{t:'Retour'},{t:'Code-barres'},{t:'Parfum'},{t:'Marque'},{t:'Prix',y:'m'},{t:'Quantité',y:'n'},{t:'Montant',y:'m'},{t:'Règlement'},{t:'Mode'}],
    lignes:L };
});

$('notetxt').innerHTML=`Trois sources, fondues par le nom du client.<br>
  <b>Le tableur</b> (onglet « carmen », lu le ${dfr(D.date)}) : les commandes de gros d'avant l'outil — ${nf((D.clients||[]).reduce((a,c)=>a+c.cmds.length,0))} commandes. Dates lues dans le titre de la commande ; quand elles manquent, la date voisine est reprise et marquée ≈. Les « quote » ne comptent pas dans les achats.<br>
  <b>L'outil</b> : chaque vente enregistrée ici — site, caisse, boutique, gros, Amazon — avec son heure, son canal, ses lignes et son paiement.<br>
  <b>Le site</b> : la liste de ses clients (coordonnées). Ses totaux à lui sont montrés à part dans la fiche, jamais additionnés.`;

$('sfu').innerHTML = USR ? `Connecté : <b>${esc(USR)}</b>` : '';
$('sfoot').innerHTML='tous les clients<br>gros, site, boutique';
construit(); dessine();
$('selrien').onclick=()=>{ COCHES.clear(); dessine(); };
$('selvip').onclick=()=>{ COCHES.forEach(n=>basculeVip(n,true)); dessine(); };
$('selnon').onclick=()=>{ COCHES.forEach(n=>basculeVip(n,false)); dessine(); };
$('selecr').onclick=()=>{ const L=selClients(); if(!L.length) return;
  contacteGroupe({liste:L, titre:'Écrire aux clients sélectionnés', modele:'promo'}); };

/* ---------- La liste de diffusion (Igal, 7 oct. 2026) ----------
   « Une liste de diffusion accessible à tous tes clients, en WhatsApp et en email, pour que Sam
   envoie ses offres de parfums. » Les clients sont déjà là avec leurs coordonnées : le bouton
   prend la liste AFFICHÉE (le filtre Grossistes, Clients du site, Favoris… choisit le public),
   sans les désinscrits, et ouvre la fenêtre d'envoi groupé. Rien ne part tout seul. */
function offreCherche(q){
  q=cNorm(q); if(q.length<2) return [];
  let M={}; try{ M=lit('fiches-modifiees-v1',{})||{}; }catch(e){}
  const gros=$('typ').value==='gros', out=[];
  let T=[]; try{ T=D_TOUS(); }catch(e){}
  for(const r of T){
    const m=M[r[15]||r[14]]||{}, nom=String(r[13]||r[1]||'').trim(), marque=String(r[2]||'').trim(), ml=String(r[3]||'').trim();
    if(!nom||!cNorm(marque+' '+nom+' '+ml).includes(q)) continue;
    const vw=m.pvw!==undefined?m.pvw:r[8], vr=m.pvr!==undefined?m.pvr:r[7];
    const v=gros?(vw>0?vw:null):(vr>0?vr:(vw>0?vw:null));
    if(v==null) continue;
    out.push({lib:(marque?marque+' ':'')+nom+(ml?' '+ml:''), prix:money2(v)});
    if(out.length>=8) break;
  }
  return out;
}
/* ---- Le fichier d'offre : Sam ne cherche plus les parfums un par un ----
   (Igal, 7 oct. 2026 : « un fichier type qu'il puisse intégrer sur son envoi pour éviter d'aller
   chercher tous les parfums »). Le modèle contient les parfums EN STOCK avec leur prix du moment ;
   Sam met un x dans la colonne OFFRE (et change le prix s'il veut un prix spécial), puis
   importe : le message se remplit tout seul. */
function offreStock(){
  const M=lit('fiches-modifiees-v1',{})||{}; let X={q:{}}; try{ X=Object.assign({q:{}},JSON.parse(localStorage.getItem('stock-externe-v1')||'{}')); }catch(e){}
  const gros=$('typ').value==='gros', out=[];
  let T=[]; try{ T=D_TOUS(); }catch(e){}
  T.forEach(r=>{ const m=M[r[15]||r[14]]||{}, bc=String(r[0]||'').trim();
    let q=(m.qte!=null)?+m.qte:(X.q&&X.q[bc]!=null?+X.q[bc]:(+r[6]||0)); if(!(q>0)) return;
    const vw=m.pvw!==undefined?m.pvw:r[8], vr=m.pvr!==undefined?m.pvr:r[7];
    const v=gros?(vw>0?vw:(vr>0?vr:null)):(vr>0?vr:(vw>0?vw:null));
    const nom=String(r[13]||r[1]||'').trim(); if(!nom) return;
    out.push({bc,marque:String(r[2]||'').trim(),nom,ml:String(r[3]||'').trim(),q,prix:v}); });
  out.sort((a,b)=>(a.marque.toLowerCase()+' '+a.nom.toLowerCase()).localeCompare(b.marque.toLowerCase()+' '+b.nom.toLowerCase()));
  return out;
}
function offreModele(){
  /* un vrai fichier Excel (.xlsx) : sur le Mac de Sam un .csv s'ouvre dans Numbers, pas dans Excel */
  sortieXlsx({titre:"Modèle d'offre", fichier:'modele-offre',
    colonnes:[{t:'OFFRE'},{t:'BARCODE'},{t:'BRAND'},{t:'NAME'},{t:'ML/fl oZ'},{t:'STOCK',y:'n'},{t:'PRICE',y:'n'}],
    lignes:offreStock().map(p=>['',p.bc,p.marque,p.nom,p.ml,p.q,p.prix==null?'':p.prix])});
}
function offreCsv(txt){
  const li=txt.replace(/\r/g,'').split('\n').filter(l=>l.trim()!=='');
  if(!li.length) return [];
  const sep=li[0].includes('\t')?'\t':(li[0].split(';').length>li[0].split(',').length?';':',');
  return li.map(l=>{ const o=[]; let c='', qt=false;
    for(let i=0;i<l.length;i++){ const ch=l[i];
      if(ch==='"'){ if(qt&&l[i+1]==='"'){ c+='"'; i++; } else qt=!qt; }
      else if(ch===sep&&!qt){ o.push(c); c=''; } else c+=ch; }
    o.push(c); return o; });
}
async function offreImporte(f){
  let L;
  if(/\.xlsx$/i.test(f.name)){
    if(typeof xlLis!=='function'||!xlsxDispo) return {lignes:[],ignorees:0,raison:"Ce navigateur ne sait pas lire l'Excel : enregistre le fichier en CSV."};
    const {onglets}=await xlLis(await f.arrayBuffer()); L=(onglets[0]&&onglets[0].lignes)||[];
  } else L=offreCsv(await f.text());
  if(L.length<2) return {lignes:[],ignorees:0,raison:"Le fichier est vide."};
  const ent=L[0].map(h=>String(h||'').trim().toLowerCase());
  const col=re=>ent.findIndex(h=>re.test(h));
  const cO=col(/^(offre|offer|x|inclure|ok)$/), cB=col(/^(barcode|code|code[- ]?barres?|upc|ean)$/), cM=col(/^(brand|marque)$/),
        cN=col(/^(name|nom|parfum)$/), cL=col(/^(ml|ml ?\/ ?fl ?oz|oz|contenance)$/), cP=col(/^(price|prix|pvw|pvr|offer price|prix offre)$/);
  if(cO<0) return {lignes:[],ignorees:0,raison:"Je ne trouve pas la colonne OFFRE : prends le modèle d'offre et mets un x devant les parfums."};
  const parBC={}; offreStock().forEach(p=>{ parBC[p.bc.replace(/^0+/,'')]=p; });
  const sortie=[]; let ign=0;
  L.slice(1).forEach(r=>{
    const x=String(r[cO]==null?'':r[cO]).trim().toLowerCase(); if(!x||/^(0|non|no|n|false|faux)$/.test(x)) return;
    const bc=cB>=0?String(r[cB]||'').replace(/[^0-9]/g,'').replace(/^0+/,''):'', ref=bc?parBC[bc]:null;
    const marque=cM>=0?String(r[cM]||'').trim():(ref?ref.marque:''), nom=cN>=0?String(r[cN]||'').trim():(ref?ref.nom:'');
    const ml=cL>=0?String(r[cL]||'').trim():(ref?ref.ml:'');
    let px=cP>=0?parseFloat(String(r[cP]||'').replace(/[^0-9.,]/g,'').replace(',','.')):NaN; if(!(px>0)&&ref&&ref.prix>0) px=ref.prix;
    const lib=((marque?marque+' ':'')+nom+(ml?' '+ml:'')).trim();
    if(!lib||!(px>0)){ ign++; return; }
    sortie.push(lib+' — '+money2(px)); });
  return {lignes:sortie,ignorees:ign};
}
function ouvreDiffusion(){
  const R=lignes().map(r=>r.o);
  const avec=R.filter(o=>!o.co.nodiff&&(ctMail(o.co.email)||ctNum(o.co.tel)));
  const stops=new Set(R.filter(o=>o.co.nodiff).map(o=>(ctMail(o.co.email)?o.co.email.trim().toLowerCase():'')||ctNum(o.co.tel)||o.nom)).size;
  if(!avec.length){ alert('Aucun client de cette liste n\'a d\'email ni de numéro WhatsApp. Change le filtre, ou complète les coordonnées dans les fiches.'); return; }
  const lib=$('typ').selectedOptions[0].textContent;
  contacteGroupe({liste:avec.map(o=>({nom:o.nom,email:o.co.email||'',tel:o.co.tel||''})), titre:'Liste de diffusion — '+lib, modele:'promo', pied:true,
    desinscrits:stops, catalogue:offreCherche, modeleOffre:offreModele, importeOffre:offreImporte,
    onStop:nom=>{ /* la personne, pas la fiche : toutes les fiches qui portent la même adresse ou le même numéro */
      const x=parNom(nom), mails=new Set([x&&x.co.email].filter(m=>ctMail(m)).map(m=>m.trim().toLowerCase())), tels=new Set([x&&ctNum(x.co.tel)].filter(Boolean));
      TOUS.filter(o=>o.nom===nom||(ctMail(o.co.email)&&mails.has(o.co.email.trim().toLowerCase()))||(ctNum(o.co.tel)&&tels.has(ctNum(o.co.tel))))
        .forEach(o=>{ CLI[o.nom]=Object.assign({},CLI[o.nom]||{},{nom:o.nom,nodiff:true,maj:new Date().toISOString()}); });
      sauveCLI(); construit(); dessine(); },
    onRestore:()=>{ Object.keys(CLI).forEach(n=>{ if(CLI[n]&&CLI[n].nodiff){ CLI[n]=Object.assign({},CLI[n],{nodiff:false}); } }); sauveCLI(); construit(); dessine();
      setTimeout(ouvreDiffusion,0); return null; }});
}
$('diff').onclick=ouvreDiffusion;

/* si un autre onglet (ou le cockpit) écrit des ventes, la liste se refait */
if(typeof _apresEcrit!=='undefined') _apresEcrit.push(cle=>{ if(cle===KFACT||cle===KCLI||cle===KRET){ try{ FACT=lit(KFACT,[]); CLI=lit(KCLI,{}); construit(); dessine(); }catch(e){} } });
/* Ce qu'un AUTRE poste écrit arrive par le fil en direct : la liste et l'étoile de la fiche
   ouverte se redessinent tout de suite, sans recharger la page (Sam ne voyait pas les
   favoris mis par Igal — la page n'avait pas de quoi se redessinir). */
function clRafraichit(){
  FACT=lit(KFACT,[]); if(!Array.isArray(FACT)) FACT=[];
  { const c=lit(KCLI,{}); CLI=(c&&typeof c==='object')?c:{}; }
  { const p=lit(KPAY,{}); if(p&&typeof p==='object') PAY=p; }
  construit(); dessine();
  if(OUV){ const fv=$('dfav'), v=estVip(OUV.nom); if(fv){ fv.textContent=v?'★':'☆'; fv.classList.toggle('on',v);
    fv.title=v?'Retirer des favoris':'Mettre ce client en favoris'; } }
}
window.__rafraichir=clRafraichit;
window.addEventListener('ck-maj',e=>{ try{ const k=(e.detail&&e.detail.cles)||[];
  if(k.includes(KCLI)||k.includes(KFACT)||k.includes(KPAY)||k.includes(KRET)) clRafraichit(); }catch(_){} });
/* « Clients VIP » du menu de gauche : clients.html#vip ouvre la liste des favoris (le même filtre que
   « Favoris (VIP) » plus haut). Le menu et le filtre se suivent dans les deux sens. */
function vipSync(){ window.__filtreVip=($('typ').value==='vip'); if(typeof mnSous==='function') mnSous(); }
function vipDepuisAdresse(){ const h=location.hash; if(/nom=/.test(h)) return;
  const veut=/(^|[#&])vip\b/.test(h), cible=veut?'vip':($('typ').value==='vip'?'':$('typ').value);
  if($('typ').value!==cible){ $('typ').value=cible; dessine(); }
  vipSync(); }
$('typ').addEventListener('input',()=>{ try{ if(!/nom=/.test(location.hash))
  history.replaceState(null,'',location.pathname+location.search+($('typ').value==='vip'?'#vip':'')); }catch(e){} vipSync(); });
window.addEventListener('hashchange',vipDepuisAdresse);
vipDepuisAdresse();
/* une fiche demandée par l'adresse : clients.html#nom=Maria%20Lopez */
try{ const m=location.hash.match(/nom=([^&]+)/); if(m) ouvre(decodeURIComponent(m[1])); }catch(e){}
window.__C={construit,parNom,ouvre,TOUS:()=>TOUS};
"""

html = coquille("Clients", "Clients",
  "Tous ceux qui achètent — en gros, sur le site, à la boutique, sur Amazon — dans une seule liste. "
  "Pour chacun : ce qu'il a acheté, quand, à quelle heure, par quel canal, comment il a payé, et ses coordonnées.",
  CSS, CORPS, JS, donnees=('produits','clients','retail'))
_donnees.pose('clients', DATA, 'D_CLI')
# L'historique de gros d'avant l'ERP, LIGNE PAR LIGNE et par code-barres : lu par la fiche du Catalogue, qui
# en fait des ventes comme les autres (« Ventes de ce parfum » : total, canal, client, rythme, 12 mois).
# 13 oct. 2026, Igal : « l'historique n'y est pas dans la fiche produit » — il était dans un bloc à part,
# avec ses propres chiffres, au lieu d'être dans les statistiques de ventes.
# Format : {c:[noms de clients], l:{code sans zéros: [[jour, n° du client dans c, flacons, prix unitaire], …]}}
import re as _re
_HGC = []; _HGI = {}; _HGL = {}
for _c in SEED['clients']:
    for _x in _c['cmds']:
        if _x['devis'] or _x['douteux']: continue
        for _l in _x['lignes']:
            _b = _re.sub(r'^0+', '', _re.sub(r'\D', '', str(_l.get('bc') or '')))
            _q = _l.get('q') or 0
            if not _b or _q <= 0: continue
            if _c['nom'] not in _HGI: _HGI[_c['nom']] = len(_HGC); _HGC.append(_c['nom'])
            _p = _l.get('p')
            if _p is None and _l.get('t'): _p = _l['t'] / _q
            _HGL.setdefault(_b, []).append([_x['date'] or '', _HGI[_c['nom']], round(_q, 2) if _q != int(_q) else int(_q),
                                            None if _p is None else round(_p, 2)])
for _v in _HGL.values(): _v.sort(key=lambda r: r[0], reverse=True)
_donnees.pose('histgros', {'c': _HGC, 'l': _HGL}, 'D_HG')
html = html.replace('__DATA__', 'window.D_CLI')
html = html.replace('__BC2CLE__',
  'Object.fromEntries(D_TOUS().filter(r=>r[0]).map(r=>[String(r[0]).replace(/^0+/,\'\'),r[15]]))')
open('clients.html', 'w').write(html)
print('clients.html', len(html)//1024, 'Ko')
