# -*- coding: utf-8 -*-
"""Génère les rubriques Fournisseurs et Clients du CRM.
Elles partagent la charte du catalogue et lisent les mêmes données locales."""
import json
from _garde import GARDE
from _fusion import FUSION
from _comptes import COMPTES
from _identite import IDENT
from _sauvegarde import SAUVE
from _menu import MENU
from _langue import LANGUE
import _contact, _xlsx, _sortie, _aide, _lire

import datetime
VERSION = datetime.datetime.now().strftime('%d/%m/%Y \u00e0 %Hh%M')
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

def barre(actif):
    VER = VERSION_URL
    L = [('catalogue.html','▦','Catalogue', n(S['total'])),
         ('stock.html','▤','Inventaire', n(S['enstock'])),
         ('inventaire_pc.html','▥','Inventaire Perfume City','boutique'),
         ('etude.html','◈','Étude de devis','fournisseur'),
         ('factures.html','▧','Factures','—'),
         ('ventes.html','◔','Ventes','par canal'),
         ('quotes.html','◇','Quotes','devis clients'),
         ('fournisseurs.html','⬒','Fournisseurs','—'),
         ('clients.html','◉','VIP wholesale', str(NCLI)),
         ('retail.html','◍','Retail','site'),
         ('connecteurs.html','⇄','Connecteurs','à brancher'),
         ('messages.html','✉','Messages','équipe'),
         ('journal.html','◷','Journal','—'),
         ('tableau.html','◧','Tableau de bord','—'),
         ('acces.html','⛨','Accès','comptes'),
         ('https://app.gusto.com','$','Payroll','Gusto'),
         ('reglages.html','⚙','Réglages','—')]
    out=[]
    for href,ic,lab,ct in L:
        if lab in ('Étude de devis',): out.append('<div class="navlab">Commerce</div>')
        if lab=='Messages': out.append('<div class="navlab">Pilotage</div>')
        cls='nv'+(' on' if lab==actif else '')+('' if href else ' soon')
        ext=bool(href) and href.startswith('http')
        a=f'<a class="{cls}"'+((f' href="{href}" target="_blank" rel="noopener" title="Ouvre Gusto dans un nouvel onglet"' if ext else f' href="{href}?v={VER}"') if href else '')+'>'
        cid='ct-'+('pcity' if lab.startswith('Inventaire Perfume') else lab.lower().split()[0].replace('&',''))
        out.append(f'{a}<span class="ic">{ic}</span>{lab}<span class="ct" id="{cid}">{ct}</span></a>')
    return '\n    '.join(out)

import _donnees
from _serveur import enligne


def coquille(titre, actif, sous, css, corps, js, donnees=()):
    return enligne(f'''<!DOCTYPE html>
<html lang="fr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta http-equiv="Cache-Control" content="no-store, no-cache, must-revalidate">
<meta http-equiv="Pragma" content="no-cache">
<meta http-equiv="Expires" content="0">

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
    <div class="ver" title="Si cette date n'est pas la derni&egrave;re, recharge avec Cmd+Option+R">version du {VERSION}</div></div>
</aside>
<main class="main"><div class="wrap">
<header><div><h1>{titre}</h1><p class="sous">{sous}</p></div><div class="src" id="src"></div></header>
{corps}
</div></main>
</div>
<script src="donnees/langue.js"></script>
{''.join('<script src="donnees/'+d+'.js"></script>' for d in donnees)}
{_donnees.garde(donnees)}
<script>
const VER_URL='{VERSION_URL}';
const $=i=>document.getElementById(i);
const esc=s=>String(s==null?'':s).replace(/[&<>"]/g,c=>({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}}[c]));
const nf=v=>Number(v||0).toLocaleString('fr-FR');
const money=v=>v==null?'—':Number(v).toLocaleString('fr-FR',{{maximumFractionDigits:0}})+' $';
const money2=v=>v==null?'—':Number(v).toLocaleString('fr-FR',{{minimumFractionDigits:2,maximumFractionDigits:2}})+' $';
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
__SAUVE__
__MENU__
__LANGUE__
__CONTACT__
__XLSX__
__SORTIE__
{js}
__GARDE__
</script></body></html>'''.replace('__FUSION__', FUSION).replace('__COMPTES__', COMPTES).replace('__IDENT__', IDENT).replace('__SAUVE__', SAUVE).replace('__MENU__', MENU).replace('__LANGUE__', LANGUE).replace('__CONTACT__', _contact.CONTACT).replace('__XLSX__', _xlsx.XLSX + _lire.bloc()).replace('__SORTIE__', _sortie.JS).replace('__GARDE__', GARDE))
