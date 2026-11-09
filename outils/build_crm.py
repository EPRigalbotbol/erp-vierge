# -*- coding: utf-8 -*-
"""Génère les rubriques Fournisseurs et Clients du CRM.
Elles partagent la charte du catalogue et lisent les mêmes données locales."""
import json
from _garde import GARDE
from _fusion import FUSION
from _comptes import COMPTES
from _identite import IDENT
import _identite
from _sauvegarde import SAUVE
from _menu import MENU
from _langue import LANGUE
import _langue
import _contact, _xlsx, _sortie, _aide, _lire, _file_auto

import datetime
VERSION = datetime.datetime.now().strftime('%m/%d/%Y \u00e0 %Hh%M')
VERSION_URL = datetime.datetime.now().strftime('%Y%m%d%H%M')

BASE = open('_base.css').read()
MODALES = open('_modales.css').read()
S = json.load(open('cat_stats.json'))
n = lambda v: f"{v:,}".replace(',', ' ')

import os
# on ne compte que les clients qui ont réellement commandé (les devis sans suite ne sont pas des clients)
NCLI = (len([c for c in json.load(open('clients_seed.json'))['clients']
             if any(not x['devis'] and not x['douteux'] for x in c['cmds'])])
        if os.path.exists('clients_seed.json') else 0)

# Icônes du menu : un trait, une taille, la couleur du texte (8 oct. 2026 — les signes
# typographiques d'avant n'avaient ni la même taille ni le même poids d'une rubrique à l'autre).
_IC = {
 'catalogue.html':'<rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/>',
 'stock.html':'<path d="M21 8 12 3 3 8v8l9 5 9-5z"/><path d="m3 8 9 5 9-5M12 13v8"/>',
 'inventaire_pc.html':'<path d="M4 9h16l-1-5H5z"/><path d="M5 9v11h14V9"/><path d="M10 20v-5h4v5"/>',
 'quotes.html':'<path d="M14 3H6a1 1 0 0 0-1 1v16a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V8z"/><path d="M14 3v5h5M9 13h6M9 17h4"/>',
 'factures.html':'<path d="M6 3h12v18l-3-2-3 2-3-2-3 2z"/><path d="M9 8h6M9 12h6"/>',
 'ventes.html':'<path d="M3 17l5-5 4 4 8-9"/><path d="M15 7h5v5"/>',
 'fournisseurs.html':'<path d="M3 7h11v9H3zM14 10h4l3 3v3h-7z"/><circle cx="7" cy="18" r="1.8"/><circle cx="17" cy="18" r="1.8"/>',
 'etude.html':'<circle cx="11" cy="11" r="6.5"/><path d="m16 16 5 5"/>',
 'clients.html':'<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20a6.5 6.5 0 0 1 13 0"/><path d="M16 4.5a3.5 3.5 0 0 1 0 7M18 14a6.5 6.5 0 0 1 3.5 6"/>',
 'connecteurs.html':'<path d="M7 7h10l-3-3M17 17H7l3 3"/>',
 'messages.html':'<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>',
 '#support':'<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="3.5"/><path d="m9.5 9.5-4-4M14.5 9.5l4-4M14.5 14.5l4 4M9.5 14.5l-4 4"/>',
 '#galou':'<path d="M4 5h16v10H9l-5 4z"/><path d="M8 9h8M8 12h5"/>',
 'demandes_pc.html':'<path d="M4 8h13l-3-3M20 16H7l3 3"/>',
 'taches.html':'<rect x="3" y="4" width="18" height="16" rx="2"/><path d="m8 12 3 3 5-6"/>',
 'journal.html':'<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
 'tableau.html':'<rect x="3" y="3" width="8" height="10" rx="1.5"/><rect x="13" y="3" width="8" height="6" rx="1.5"/><rect x="13" y="11" width="8" height="10" rx="1.5"/><rect x="3" y="15" width="8" height="6" rx="1.5"/>',
 'analytique.html':'<path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/>',
 'acces.html':'<path d="M12 3 4 6v6c0 4.5 3.3 8 8 9 4.7-1 8-4.5 8-9V6z"/><path d="m9 12 2 2 4-4"/>',
 'https://app.gusto.com':'<circle cx="12" cy="12" r="9"/><path d="M14.5 9a2.5 2 0 0 0-2.5-1.5c-1.4 0-2.5.8-2.5 2s1 1.7 2.5 2 2.5.8 2.5 2-1.1 2-2.5 2A2.7 2 0 0 1 9.5 15M12 6v1.5M12 16.5V18"/>',
 'reglages.html':'<circle cx="12" cy="12" r="3"/><path d="M12 2.5v3M12 18.5v3M2.5 12h3M18.5 12h3M5.3 5.3l2.1 2.1M16.6 16.6l2.1 2.1M18.7 5.3l-2.1 2.1M7.4 16.6l-2.1 2.1"/>',
}
def _svg(h): return '<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'+_IC.get(h,'')+'</svg>'

def barre(actif):
    VER = VERSION_URL
    L = [('catalogue.html','▦','Catalogue', '#'+n(S['total'])),
         ('stock.html','▤','Inventaire', '#'+n(S['enstock'])),
         ('inventaire_pc.html','▥','Inventaire Perfume City',''),
         # 4 nov. 2026 (Igal) : les transferts de parfums entre Perfume City et Perfumes Trade — « Transfert interstore » (build_demandes_pc.py)
         ('demandes_pc.html','⇆','Transfert interstore',''),
         ('quotes.html','◇','Devis',''),
         ('factures.html','▧','Factures',''),
         ('ventes.html','◔','Ventes',''),
         # Statut shipping : en veille depuis le 2 oct. 2026 (Sam n'en voit pas l'utilité) —
         # la page existe toujours ; remettre la ligne la remet au menu.
         # ('expeditions.html','⇢','Statut shipping','à expédier'),
         ('fournisseurs.html','⬒','Fournisseurs',''),
         # Retirée du menu le 12 sept., remise à la demande d'Igal le 15 : on y
         # entrait par le tableau de bord, et personne ne la retrouvait.
         ('etude.html','⌕','Étude de devis',''),
         ('clients.html','◉','Clients', '!'+str(NCLI)),
         ('connecteurs.html','⇄','Connecteurs',''),
         # 3 nov. 2026 (Igal) : Galou, l'assistant d'Igal — une fenêtre pour lui parler, sur n'importe quelle page (_galou.py)
         ('#galou','✦','Parler à Léa',''),
         # 9 oct. 2026 (Igal) : la messagerie interne est retirée du menu pour tout le monde ; à sa
         # place, « Support technique » ouvre la boîte de dialogue qui envoie une réclamation à Igal
         # (cockpit, table support). La page messages.html existe toujours mais n'est plus liée.
         ('#support','?','Support technique',''),
         ('journal.html','◷','Journal',''),
         ('tableau.html','◧','Tableau de bord',''),
         # 9 nov. 2026 (Igal) : l'analytique de tous les canaux — d'où viennent les ventes, ce que Google coûte et rapporte ;
         # réservée aux administrateurs (Admin, Patron) : cachée à tout autre rôle (_menu.py, mn-pasadmin) (build_analytique.py)
         ('analytique.html','◔','Analytique',''),
         # 3 nov. 2026 (Igal) : les tâches que Galou trouve dans l'ERP — « le bras droit de Sam » (build_taches.py)
         ('taches.html','☑','Tâches',''),
         ('acces.html','⛨','Accès',''),
         ('https://app.gusto.com','$','Paie',''),
         ('reglages.html','⚙','Réglages','')]
    out=[]
    for href,ic,lab,ct in L:
        if lab in ('Devis',): out.append('<div class="navlab">Commerce</div>')
        if lab=='Support technique': out.append('<div class="navlab" data-pilotage="1">Pilotage</div>')
        # 17 oct. 2026 (Sam) : « toute la partie Pilotage ne doit pas être vue par un Commercial » —
        # ces rubriques portent data-pilotage ; le menu les retire pour un rôle sans marges, sans accès, sans réglages (_menu.py)
        pil=' data-pilotage="1"' if lab in ('Connecteurs','Journal','Tableau de bord','Analytique','Tâches','Accès','Paie','Réglages') else ''
        cls='nv'+(' on' if lab==actif else '')+('' if href else ' soon')
        ext=bool(href) and href.startswith('http')
        a=f'<a class="{cls}"{pil}'+((f' href="{href}" target="_blank" rel="noopener" title="Ouvre Gusto dans un nouvel onglet"' if ext else f' href="{href}?v={VER}"') if href else '')+'>'
        if href=='#support':
            a=f'<a class="{cls}"{pil} href="#support" id="aid-btn" data-id="support" onclick="if(typeof aidOuvre===\'function\')aidOuvre();return false">'
        if href=='#galou':
            a=f'<a class="{cls}" href="#galou" id="gl-btn" data-id="galou" onclick="if(typeof galouOuvre===\'function\')galouOuvre();return false">'
        cid='ct-'+('pcity' if lab.startswith('Inventaire Perfume') else 'expeditions' if lab in ('Expéditions','Statut shipping') else 'taches' if lab=='Tâches' else 'demandes' if lab=='Transfert interstore' else lab.lower().split()[0].replace('&',''))
        # 8 oct. 2026 (Igal) : plus de petit texte gris à droite des rubriques — seuls restent le
        # nombre de clients et la pastille des nouvelles ventes (et la pastille rouge des messages
        # non lus, quand il y en a). Les chiffres de Catalogue et d'Inventaire continuent d'être
        # calculés (tests, journal) mais ne s'affichent plus : retirer la classe « nu » les rend.
        kl='ct'+(' nb' if ct.startswith('!') else ' nu' if ct.startswith('#') else '')
        out.append(f'{a}<span class="ic">{_svg(href)}</span>{lab}<span class="{kl}" id="{cid}">{ct[1:] if ct[:1] in "!#" else ct}</span></a>')
        # 13 oct. 2026 (Igal) : « en sous-rubrique de Clients, je veux les clients VIP » — une ligne
        # plus petite sous Clients qui ouvre la liste des favoris (clients.html#vip). Son identité
        # est à part (data-id) : sinon le menu réglé la confondrait avec « Clients ».
        if href=='clients.html':
            out.append(f'<a class="nv sub" href="clients.html?v={VER}#vip" data-id="clients-vip" data-sous="clients.html">Clients VIP</a>')
    return '\n    '.join(out)

import _donnees
from _serveur import enligne


def coquille(titre, actif, sous, css, corps, js, donnees=()):
    return enligne(f'''<!DOCTYPE html>
<html lang="fr"><head><meta charset="utf-8">
<!-- l'icône d'onglet : Sam a toujours beaucoup d'onglets ouverts ; le flacon du logo, blanc sur rose vif (choisi par Igal), se repère d'un coup d'œil (27 sept. 2026) -->
<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='14' fill='%23FF1F7A'/%3E%3Cg fill='none' stroke='%23fff' stroke-width='4' stroke-linejoin='round'%3E%3Crect x='25' y='7' width='14' height='8' rx='2' fill='%23fff'/%3E%3Crect x='28' y='15' width='8' height='6'/%3E%3Cpath d='M19 21 H45 L51 27 V51 L45 57 H19 L13 51 V27 Z'/%3E%3C/g%3E%3Cpath d='M36 28 Q44 29 45 36' stroke='%23fff' stroke-width='3' fill='none' stroke-linecap='round'/%3E%3C/svg%3E">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta http-equiv="Cache-Control" content="no-store, no-cache, must-revalidate">
<meta http-equiv="Pragma" content="no-cache">
<meta http-equiv="Expires" content="0">
<script>/* en anglais ou en espagnol, l'écran reste caché le temps que la traduction passe (quelques ms) : on ne voit jamais le français d'origine */try{{var _l=localStorage.getItem('langue-v1');if(_l&&_l!=='fr'){{document.documentElement.style.visibility='hidden';setTimeout(function(){{document.documentElement.style.visibility='';}},1500);}}
/* un menu réglé (ordre, rubriques cachées) : la barre reste cachée le temps qu'il s'applique, pour que les rubriques ne sautent pas */
var _m=JSON.parse(localStorage.getItem('menu-perso-v1')||'null');if(_m&&((_m.ordre&&_m.ordre.length)||(_m.caches&&_m.caches.length))){{document.documentElement.classList.add('mn-attente');setTimeout(function(){{document.documentElement.classList.remove('mn-attente');}},1500);}}
/* 7 nov. 2026 (Igal : « je ne veux pas qu'un Commercial aperçoive les autres rubriques, même une seconde ») : d'après la session déjà
   en mémoire, un rôle sans marges (ni Patron, ni Admin, ni Comptable) cache Pilotage et Léa AVANT la première peinture (mn-cial) ;
   le menu confirme ou corrige ensuite avec les droits réels (_menu.py, mnPilotage) */
var _s=JSON.parse(localStorage.getItem('sam-session-v1')||'null');if(_s&&_s.role&&!/^(patron|admin|comptable)$/.test(String(_s.role))){{document.documentElement.classList.add('mn-cial');}}
/* 9 nov. 2026 : « Analytique » est aux seuls administrateurs (Admin, Patron) — cachée avant la première peinture pour tout autre rôle */
if(!_s||!/^(patron|admin)$/.test(String(_s.role||''))){{document.documentElement.classList.add('mn-pasadmin');}}}}catch(e){{}}</script>
<script>/* le contenu de la page reste caché jusqu'à ce que son code l'ait dessiné (voir _serveur.py) */try{{document.documentElement.classList.add('pg-attente');setTimeout(function(){{document.documentElement.classList.remove('pg-attente');}},4000);}}catch(e){{}}</script>
<style>.mn-attente .side nav{{visibility:hidden}} .pg-attente .main{{visibility:hidden}} html.mn-cial .side nav [data-pilotage],html.mn-cial .side nav #gl-btn{{display:none!important}} html.mn-pasadmin .side nav a.nv[href^="analytique.html"]{{display:none!important}}</style>

<title>{titre} — Perfumes Trade</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Cormorant+Garamond:wght@300;400;500;600;700&display=swap">
<style>
{BASE}
body{{font-variant-numeric:tabular-nums;font-feature-settings:"tnum" 1}}
.sfu{{margin-bottom:9px;padding-bottom:9px;border-bottom:1px solid var(--line-2);
font-family:Inter,sans-serif;font-size:11.5px;color:var(--ink-3);line-height:1.5}}
.sfu b{{color:var(--iris);font-weight:600}}
.lnk{{background:none;border:0;padding:0;font-family:inherit;font-size:11.5px;color:var(--ink-3);
text-decoration:underline;cursor:pointer}}
.lnk:hover{{color:var(--iris)}}
.ver{{margin-top:9px;font-family:Inter,sans-serif;font-size:10px;color:var(--ink-3);opacity:.75;
letter-spacing:.02em}}
{MODALES}
{_contact.CSS}
{_aide.CSS}
{_xlsx.CSS}
{_sortie.CSS}
{css}
</style></head><body>
<div class="app">
<aside class="side">
  <div class="logo"><div class="n">Perfumes Trade</div><div class="s">ERP</div></div>
  <nav>
    <div class="navlab">Produits</div>
    {barre(actif)}
  </nav>
  <div class="sfoot"><div id="sfu" class="sfu"></div><span id="sfoot"></span>
    <div class="ver" title="Si cette date n'est pas la derni&egrave;re, recharge avec Cmd+Option+R">version du {VERSION}</div>
    <div class="sfline" id="sfline"></div></div>
</aside>
<main class="main"><div class="wrap">
<header><div><h1>{titre}</h1><p class="sous">{sous}</p></div><div class="src" id="src"></div></header>
{corps}
</div></main>
</div>
<script>__VOCAB__</script>
<script src="donnees/langue.js?v={VERSION_URL}"></script>
<script>
/* le menu réglé et la langue de l'écran, AVANT le code de la page : rien ne saute, rien n'est vu dans une autre langue */
__IDENT_TOT__
__MENU__
__LANGUE__
</script>
{''.join('<script src="donnees/'+d+'.js?v='+VERSION_URL+'"></script>' for d in donnees)}
{_donnees.garde(donnees)}
<script>
const VER_URL='{VERSION_URL}';
const $=i=>document.getElementById(i);
const esc=s=>String(s==null?'':s).replace(/[&<>"]/g,c=>({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}}[c]));
const nf=v=>Number(v||0).toLocaleString('fr-FR');
/* Le dollar (Igal, 30 sept. 2026 : « le dollar est décalé ») : une espace INSÉCABLE entre le
   montant et le $, pour que le $ ne parte jamais seul à la ligne suivante. Le format reste
   « 3 837,50 $ » : le dictionnaire de traduction reconnaît les phrases sur ce modèle. */
const _usd=(v,d)=>{{ if(v==null) return '—'; const n=Number(v); 
  return n.toLocaleString('fr-FR',{{minimumFractionDigits:d,maximumFractionDigits:d}})+' $'; }};
const money=v=>_usd(v,0);
const money2=v=>_usd(v,2);
/* 1,151.50 (US) ou 1 151,50 (FR) : le dernier separateur est le decimal, l'autre marque les milliers. */
const nombre=v=>{{
  if(v==null) return null;
  let t=String(v).replace(/[$\\u00a0\\u202f\\s]/g,'').replace(/[^0-9.,\\-]/g,'');
  if(t===''||t==='-'||t==='.'||t===',') return null;
  const dp=t.lastIndexOf('.'), dv=t.lastIndexOf(',');
  if(dp>=0&&dv>=0){{ const dec=Math.max(dp,dv), mil=Math.min(dp,dv);
    t=t.slice(0,mil).replace(/[.,]/g,'')+t.slice(mil+1,dec).replace(/[.,]/g,'')+'.'+t.slice(dec+1); }}
  else if(dv>=0){{ t = /^-?\\d{{1,3}}(,\\d{{3}})+$/.test(t) ? t.replace(/,/g,'') : t.replace(',','.'); }}
  else if(dp>=0){{ if(/^-?\\d{{1,3}}(\\.\\d{{3}})+$/.test(t)) t=t.replace(/\\./g,''); }}
  t=t.replace(/(?!^)-/g,'');
  const n=parseFloat(t); return isNaN(n)?null:n; }};
__FUSION__
__COMPTES__
__IDENT__
__FILE_AUTO__
__SAUVE__
__CONTACT__
__XLSX__
__SORTIE__
{js}
__GARDE__
</script></body></html>'''.replace('__FUSION__', FUSION).replace('__COMPTES__', COMPTES).replace('__IDENT__', IDENT).replace('__IDENT_TOT__', _identite.TOT).replace('__FILE_AUTO__', _file_auto.FILE_AUTO).replace('__SAUVE__', SAUVE).replace('__MENU__', MENU).replace('__LANGUE__', LANGUE).replace('__VOCAB__', _langue.VOCAB).replace('__CONTACT__', _contact.CONTACT).replace('__XLSX__', _xlsx.XLSX + _lire.bloc()).replace('__SORTIE__', _sortie.JS).replace('__GARDE__', GARDE))
