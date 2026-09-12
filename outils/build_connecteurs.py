# -*- coding: utf-8 -*-
"""Rubrique « Connecteurs » : pour chaque canal de vente, la marche à suivre exacte pour créer
l'accès API, l'état d'avancement (coché à la main), et le contrôle des SKU par import de l'export
des annonces. Rien ici ne se connecte : la page prépare le branchement, elle ne le fait pas."""
import json
from build_crm import coquille
import _donnees

C = json.load(open('cat.json'))
# code-barres (sans les zéros de tête) -> "marque nom"
BC = {}
for r in C:
    if r[0]:
        BC[str(r[0]).lstrip('0')] = ((r[2] or '') + ' ' + (r[13] or '')).strip()

CSS = r"""
.sous{margin:5px 0 0;font-size:14px;color:var(--ink-2);max-width:78ch;line-height:1.5}
.btn{font-family:inherit;font-size:13.5px;font-weight:500;color:var(--ink-2);background:var(--surface);
border:1px solid var(--line);border-radius:7px;padding:9px 15px;cursor:pointer}
.btn:hover{border-color:var(--iris);color:var(--iris)}
.btn.pri{background:var(--iris);border-color:var(--iris);color:#fff;font-weight:600}
.btn.pri:hover{filter:brightness(1.08);color:#fff}
.btn.sm{padding:6px 11px;font-size:12.5px}

.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:12px;margin-bottom:20px}
.kpi{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:15px 18px}
.kpi .v{font-family:Inter,sans-serif;font-size:28px;font-weight:800;line-height:1;letter-spacing:-.03em;
font-variant-numeric:tabular-nums}
.kpi .v.g{color:var(--good)} .kpi .v.w{color:var(--warn)} .kpi .v.i{color:var(--iris)}
.kpi .k{font-size:13px;color:var(--ink-2);margin-top:6px;line-height:1.4}

.avert{background:var(--warn-soft);border-left:3px solid var(--warn);border-radius:0 9px 9px 0;
padding:14px 18px;font-size:14px;color:var(--ink-2);line-height:1.65;margin-bottom:22px;max-width:92ch}
.avert b{color:var(--ink)}
.info{background:var(--iris-soft);border-left:3px solid var(--iris);border-radius:0 9px 9px 0;
padding:14px 18px;font-size:13.5px;color:var(--ink-2);line-height:1.65;margin:22px 0;max-width:92ch}
.info b{color:var(--ink)}

h2.sec{font-family:Inter,sans-serif;font-size:12px;letter-spacing:.12em;text-transform:uppercase;
color:var(--ink);font-weight:800;margin:30px 0 14px;padding-bottom:9px;border-bottom:1px solid var(--line);
display:flex;justify-content:space-between;align-items:baseline;gap:12px;flex-wrap:wrap}
h2.sec em{font-style:normal;font-size:13px;letter-spacing:0;text-transform:none;color:var(--ink-2);font-weight:500}

/* une carte par canal */
.cx{background:var(--surface);border:1px solid var(--line);border-radius:11px;margin-bottom:16px;
overflow:hidden;display:flex;flex-direction:column}
.cx.pret{border-left:4px solid var(--good)}
.cx.encours{border-left:4px solid var(--warn)}
.cx.afaire{border-left:4px solid var(--line)}
.cx.hors{border-left:4px solid var(--ink-3);opacity:.92}
.ch{display:flex;align-items:center;gap:14px;padding:16px 20px;cursor:pointer;user-select:none;margin:0}
.ch .lg{flex:0 0 auto;display:flex;align-items:center}
.ch .lg img{height:22px;max-width:130px;object-fit:contain;display:block}
.ch .lg-site img{height:34px}
.ch h3{margin:0;font-size:18px;font-weight:800;letter-spacing:-.02em;flex:1;min-width:0;
display:flex;align-items:center;gap:10px;flex-wrap:wrap}
.ch h3 .role{font-size:12.5px;font-weight:500;color:var(--ink-2);letter-spacing:0}
.et{font-family:Inter,sans-serif;font-size:11px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;
padding:5px 11px;border-radius:99px;white-space:nowrap}
.et.pret{background:var(--good-soft);color:var(--good)}
.et.encours{background:var(--warn-soft);color:var(--warn)}
.et.afaire{background:var(--surface-2);color:var(--ink-3);border:1px solid var(--line)}
.et.hors{background:var(--surface-2);color:var(--ink-2)}
.jauge{width:110px;height:6px;border-radius:3px;background:var(--line-2);overflow:hidden;flex:0 0 auto}
.jauge i{display:block;height:100%;background:var(--good)}
.ch .fl{font-size:18px;color:var(--ink-3);transition:transform .15s}
.cx.on .ch .fl{transform:rotate(90deg)}
.cb{display:none;padding:0 20px 20px;border-top:1px solid var(--line-2)}
.cx.on .cb{display:block}

.quoi{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:12px;margin:16px 0 20px}
.quoi div{background:var(--surface-2);border:1px solid var(--line);border-radius:9px;padding:12px 14px;
font-size:13px;color:var(--ink-2);line-height:1.55}
.quoi div > b:first-child{display:block;color:var(--ink);font-family:Inter,sans-serif;font-size:10.5px;
letter-spacing:.1em;text-transform:uppercase;font-weight:800;margin-bottom:5px}
.quoi b{color:var(--ink);font-weight:700}

ol.et2{margin:0;padding:0;list-style:none;counter-reset:e}
ol.et2 li{counter-increment:e;display:flex;gap:12px;align-items:flex-start;padding:11px 0;
border-bottom:1px dashed var(--line-2);font-size:14px;line-height:1.6;color:var(--ink-2)}
ol.et2 li:last-child{border-bottom:0}
ol.et2 li b{color:var(--ink)}
ol.et2 .n{flex:0 0 26px;height:26px;border-radius:50%;background:var(--surface-2);border:1px solid var(--line);
display:flex;align-items:center;justify-content:center;font-family:Inter,sans-serif;font-size:12px;
font-weight:800;color:var(--ink-2)}
ol.et2 li.ok .n{background:var(--good);border-color:var(--good);color:#fff}
ol.et2 li.ok .tx{color:var(--ink-3);text-decoration:line-through;text-decoration-color:var(--line)}
ol.et2 .tx{flex:1;min-width:0}
ol.et2 input{width:19px;height:19px;margin-top:3px;accent-color:var(--good);cursor:pointer;flex:0 0 auto}
.cles{margin-top:14px;background:var(--iris-soft);border-radius:8px;padding:11px 14px;font-size:13px;
color:var(--iris);line-height:1.6;font-family:Inter,sans-serif;font-weight:600}
.cles span{display:block;color:var(--ink-2);font-weight:400;font-size:12.5px;margin-top:4px}

/* contrôle des SKU */
.sku{margin-top:18px;border:1px dashed var(--line);border-radius:10px;padding:15px 17px;background:var(--surface-2)}
.sku h4{margin:0 0 8px;font-family:Inter,sans-serif;font-size:11px;letter-spacing:.11em;text-transform:uppercase;
color:var(--ink);font-weight:800}
.sku p{margin:0 0 12px;font-size:13px;color:var(--ink-2);line-height:1.6}
.dz{border:2px dashed var(--line);border-radius:9px;padding:20px;text-align:center;background:var(--surface);
cursor:pointer;font-size:13.5px;color:var(--ink-2);line-height:1.6}
.dz:hover,.dz.over{border-color:var(--iris);color:var(--iris);background:var(--iris-soft)}
.dz b{display:block;color:var(--ink);font-size:14px;margin-bottom:3px}
.res{margin-top:14px}
.res .bl{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:10px;margin-bottom:12px}
.res .bl div{background:var(--surface);border:1px solid var(--line);border-radius:9px;padding:11px 13px}
.res .bl b{display:block;font-family:Inter,sans-serif;font-size:21px;font-weight:800;letter-spacing:-.03em;line-height:1}
.res .bl b.g{color:var(--good)} .res .bl b.c{color:var(--crit)} .res .bl b.w{color:var(--warn)}
.res .bl span{display:block;font-size:12px;color:var(--ink-2);margin-top:4px}
.res table{width:100%;border-collapse:collapse;font-size:13px;background:var(--surface);
border:1px solid var(--line);border-radius:9px;overflow:hidden}
.res th{text-align:left;font-family:Inter,sans-serif;font-size:10.5px;letter-spacing:.09em;text-transform:uppercase;
color:var(--ink);font-weight:800;padding:9px 12px;background:var(--surface-2);border-bottom:1px solid var(--line)}
.res td{padding:8px 12px;border-bottom:1px solid var(--line-2)}
.res tr:last-child td{border-bottom:0}
.res code{font-family:Inter,sans-serif;font-size:12.5px;background:var(--line-2);padding:1px 6px;border-radius:4px}
.verdict{border-radius:8px;padding:11px 14px;font-size:13.5px;line-height:1.6;margin-bottom:12px}
.verdict.g{background:var(--good-soft);color:var(--good)}
.verdict.w{background:var(--warn-soft);color:var(--warn)}
.verdict.c{background:var(--crit-soft);color:var(--crit)}
.verdict b{color:inherit}
.note{margin-top:14px}
.note label{display:block;font-family:Inter,sans-serif;font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;
color:var(--ink);font-weight:800;margin-bottom:6px}
.note textarea{width:100%;min-height:64px;font-family:inherit;font-size:13.5px;color:var(--ink);
background:var(--surface);border:1px solid var(--line);border-radius:8px;padding:10px 12px;resize:vertical;line-height:1.55}
.note textarea:focus{outline:0;border-color:var(--iris);box-shadow:0 0 0 3px var(--iris-soft)}
.ordre{counter-reset:o;margin:0;padding-left:0;list-style:none}
.ordre li{counter-increment:o;display:flex;gap:12px;padding:10px 0;border-bottom:1px dashed var(--line-2);
font-size:14px;line-height:1.6;color:var(--ink-2)}
.ordre li:last-child{border-bottom:0}
.ordre li::before{content:counter(o);flex:0 0 24px;height:24px;border-radius:50%;background:var(--iris);color:#fff;
display:flex;align-items:center;justify-content:center;font-family:Inter,sans-serif;font-size:12px;font-weight:800}
.ordre b{color:var(--ink)}
"""

CORPS = r"""
<div class="avert" id="tete"></div>
<div id="kpis"></div>

<h2 class="sec">Les canaux <em>clique sur un canal pour dérouler sa procédure</em></h2>
<div id="cartes"></div>

<h2 class="sec">Dans quel ordre s'y prendre</h2>
<ol class="ordre">
  <li><b>Le site et Shopify d'abord.</b> Ce sont les plus simples : la boutique prévient l'outil en
    quelques secondes dès qu'une commande tombe, et les clés se créent en dix minutes sans validation.</li>
  <li><b>Amazon ensuite.</b> L'inscription développeur demande une validation par Amazon : à lancer tôt,
    parce que ça peut prendre des jours, et le dossier se ferme sans réponse sous 5 jours.</li>
  <li><b>La caisse en dernier.</b> Il faut d'abord savoir laquelle : Lightspeed série X (jeton, ou application privée sur les comptes récents)
    ou série R (demande d'accès à faire auprès de Lightspeed). Sans la caisse, les ventes en boutique
    restent saisies à la main.</li>
  <li><b>Le gros ne se connecte pas.</b> Une commande de Javier ou de Carmen se saisit dans Perfumes Trade
    (Ventes → + Enregistrer une vente) : il n'y a aucune plateforme derrière.</li>
</ol>

<div class="info" id="pied"></div>
"""

JS = r"""
const BC=__BC__;
const KCON='connecteurs-v1', KUSR='crm-utilisateur-v1', KJOU='crm-journal-v1';
let CON=lit(KCON,{}); if(!CON||typeof CON!=='object'||Array.isArray(CON)) CON=base(KCON,{});
let USR=NOM_UTIL;
window.__nomChange.push(v=>{ USR=v; try{ majUser(); }catch(e){} });
const sauve=()=>ecrit(KCON,CON);
const journal=(lib,ref,ap)=>{ const J=lit(KJOU,[]);
  J.push({t:new Date().toISOString(),u:USR||'(non renseigné)',act:'connecteur',lib,ref,av:null,ap:ap||null});
  ecrit(KJOU,J); };

/* Chaque canal : ce que le connecteur fera, la procédure exacte, les clés à obtenir. */
const CANAUX=[
{id:'site',nom:'Site perfumestrade.com',logo:'site',role:'boutique WooCommerce',sku:true,
 recoit:'Chaque commande payée, en quelques secondes (WooCommerce prévient l\'outil), et les clients inscrits sur le site (rubrique Retail).',
 envoie:'Le stock après chaque vente, et les prix depuis la fiche produit — le site n\'aura plus jamais un stock en retard.',
 note:'C\'est le canal le plus simple : les clés se créent seul, en dix minutes, sans validation de personne, et <b>ça ne touche à rien</b> sur le site (ni thème, ni plugin, ni adresse IP). Sam a dit que le stock du site n\'est plus à jour depuis longtemps : c\'est exactement ce que ce connecteur corrige.',
 etapes:[
  'Ouvre <b>perfumestrade.com/wp-admin</b> et connecte-toi avec un compte <b>Administrateur</b> (pas Gestionnaire de boutique : lui ne voit pas les clés).',
  'Dans le menu de gauche : <b>WooCommerce → Réglages</b>, onglet <b>Avancé</b>, puis le lien <b>API REST</b> en haut de l\'onglet.',
  'Bouton <b>Ajouter une clé</b>. Description : « Perfumes Trade ». Utilisateur : ton compte admin. Permissions : <b>Lecture/écriture</b>. Clique <b>Générer la clé API</b>.',
  'WooCommerce affiche une <b>Clé client</b> (commence par ck_) et une <b>Clé secrète</b> (commence par cs_). <b>Elles ne seront plus jamais réaffichées</b> : copie-les tout de suite, toutes les deux, dans les cases ci-dessous (ou envoie-les à Igal par un canal privé, pas par SMS ni WhatsApp de groupe).',
  'Menu WordPress <b>Réglages → Permaliens</b> : vérifie que la structure n\'est <b>pas</b> « Simple » (avec « Simple », l\'API ne répond pas). « Titre de la publication » convient. Si tu changes quelque chose ici, clique <b>Enregistrer</b>.',
  'Vérifie trois fiches produit au hasard (<b>Produits → Tous les produits</b>) : le champ <b>UGS</b> (SKU) doit contenir le <b>code-barres</b>. C\'est ce qui relie le site au catalogue.',
  'Pour la liste des clients (rubrique Retail) : <b>WooCommerce → Analytique → Clients</b>, bouton <b>Télécharger</b> en haut à droite → fichier CSV à envoyer à Igal. (Si l\'onglet Analytique n\'existe pas, <b>Utilisateurs → Tous les utilisateurs</b>, filtre « Client », suffit pour compter ; l\'export se fera par l\'API.)',
  'Rien d\'autre à installer : les commandes arriveront par l\'API et par un <b>webhook</b> que je créerai moi-même avec ces clés quand le serveur sera prêt.'],
 cles:'Clé client (ck_…) · Clé secrète (cs_…) · adresse du site (https://perfumestrade.com)'},

{id:'shopify',nom:'Shopify',logo:'shopify',role:'boutique en ligne',sku:true,
 recoit:'Chaque commande dès qu\'elle est payée (Shopify prévient l\'outil immédiatement).',
 envoie:'Le stock et les prix, une fois l\'écriture autorisée.',
 note:'Depuis 2026, Shopify fait passer par son Dev Dashboard : c\'est normal, ce n\'est pas une erreur.',
 etapes:[
  'Admin Shopify → <b>Paramètres</b> → <b>Applications et canaux de vente</b> → <b>Développer des applications</b>.',
  'Shopify renvoie vers le <b>Dev Dashboard</b> (dev.shopify.com) : accepte, puis <b>Créer une app</b>, nom « Perfumes Trade ».',
  'Dans la version de l\'app, coche les autorisations : <b>read_orders</b>, <b>read_products</b>, <b>write_products</b>, <b>read_inventory</b>, <b>write_inventory</b>. Les deux dernières sont indispensables : chez Shopify, la quantité en stock ne fait pas partie du produit, elle a ses propres autorisations — sans elles le connecteur pourra lire les commandes mais jamais remettre le stock à jour.',
  '<b>Release</b> la version, puis <b>Distribution</b> → <b>Custom distribution</b> → entre le domaine de la boutique → <b>Générer le lien</b>.',
  'Ouvre le lien généré et clique <b>Installer</b>. Note le <b>Client ID</b>, le <b>Client Secret</b> et l\'adresse xxx.myshopify.com.',
  'Ouvre trois produits : le champ <b>SKU</b> doit contenir le code-barres.'],
 cles:'Client ID · Client Secret · adresse de la boutique (xxx.myshopify.com)'},

{id:'amazon',nom:'Amazon',logo:'amazon',role:'place de marché',sku:true,
 recoit:'Les commandes (quelques minutes de décalage : Amazon ne prévient pas, l\'outil demande régulièrement), le <b>prix le plus bas</b> et le <b>rang</b> de chaque produit, rafraîchis tout seuls.',
 envoie:'<b>Rien.</b> Décision prise : l\'outil <b>regarde</b> les prix d\'Amazon, il n\'y touche pas. Les prix Amazon se changent dans Seller Central, comme aujourd\'hui.',
 note:'À lancer en premier dans le temps : Amazon valide le dossier développeur, ça peut prendre des jours. <b>Sans réponse de ta part sous 5 jours, le dossier est fermé et tout est à refaire.</b><br><br>Ce qu\'Amazon donnera : commandes, prix le plus bas, rang de vente. Ce qu\'il ne donne pas par l\'API : <b>la note et le nombre d\'avis</b> — ils resteront saisis à la main dans la fiche produit.<br><br><b>Ce compte n\'est pas obligatoire pour surveiller les prix.</b> Il rend la surveillance gratuite ; sans lui, les prix s\'achètent à l\'extérieur (≈ 49 €/mois). Ce qu\'il apporte en propre, c\'est la remontée des <b>commandes</b> Amazon.',
 etapes:[
  'Connecte-toi à <b>Seller Central</b>. Il faut un compte vendeur <b>Professionnel</b> (pas Individuel).',
  'Menu → <b>Apps et services</b> → <b>Développer des apps</b>.',
  'Formulaire d\'inscription développeur. À « accès aux données », choisis <b>Développeur privé : j\'intègre ma propre entreprise</b>. Cas d\'usage : « suivi des commandes et du stock de ma propre boutique ».',
  'Amazon répond par e-mail et pose souvent des questions. <b>Réponds sous 5 jours.</b>',
  'Une fois validé : <b>Développer des apps</b> → <b>Ajouter une app</b>, nom « Perfumes Trade ». Note le <b>Client ID</b> et le <b>Client Secret</b> (LWA).',
  'Sur la ligne de l\'app, bouton <b>Autoriser</b> : Amazon affiche un <b>refresh token</b>. Note-le, il ne se réaffiche pas.',
  'Ouvre trois annonces : le <b>SKU vendeur</b> doit contenir le code-barres — c\'est lui qui relie une commande Amazon à une référence de l\'inventaire.',
  '<b>L\'ASIN sert, lui aussi</b> : c\'est le seul lien vers la fiche Amazon d\'un parfum, donc vers son prix. 1 187 références en stock n\'en ont pas — un export de Seller Central les donne toutes d\'un coup.'],
 cles:'Client ID · Client Secret · Refresh token · Seller ID'},

{id:'lightspeed',nom:'Caisse Lightspeed',logo:'lightspeed',role:'boutique physique',sku:true,
 recoit:'Les tickets de caisse : c\'est le seul moyen que les ventes en boutique arrivent dans l\'outil.',
 envoie:'Le stock, pour que la caisse et l\'outil affichent le même chiffre.',
 note:'Deux Lightspeed très différents existent. <b>La série à identifier d\'abord</b>, tout en dépend.',
 etapes:[
  'Regarde l\'adresse de la caisse quand tu es connecté : <b>…retail.lightspeed.app</b> ou <b>…vendhq.com</b> = <b>série X</b> ; <b>…lightspeedapp.com</b> ou <b>…merchantos.com</b> = <b>série R</b>.',
  '<b>Série X</b> : <b>Configuration</b> → <b>Jetons personnels</b> → <b>Ajouter un jeton</b>, nom « Perfumes Trade ». Note le jeton et le nom de la boutique dans l\'adresse. Si le menu « Jetons personnels » n\'existe pas, c\'est un compte récent (ouvert après janvier 2026) : passe par <b>Configuration</b> → <b>Apps</b> → application privée.',
  '<b>Série R</b> : pas de jeton dans l\'interface. Il faut faire la demande d\'accès API auprès de Lightspeed (formulaire « API client registration ») : réponse sous quelques jours, avec un Client ID et un Client Secret.',
  'Vérifie que les articles de la caisse portent le <b>code-barres</b> comme référence : c\'est ce qui les relie au catalogue.'],
 cles:'La série (X ou R) · le jeton, ou Client ID + Client Secret · le nom de la boutique'},

{id:'perfumecity',nom:'Perfume City',logo:'perfumecity',role:'deuxième boutique',sku:false,
 recoit:'Rien pour l\'instant : on ne sait pas encore ce qui encaisse là-bas.',
 envoie:'Rien pour l\'instant.',
 note:'Réponses de Sam (7 septembre) : Perfume City a <b>son propre inventaire</b>, séparé. La marchandise arrive chez Perfumes Trade puis part chez Perfume City en <b>déstockage, sans facture</b>. Et quand 5 flacons partent, <b>1 passe en vitrine comme testeur</b> : le stock vendable de Perfume City est 4. Reste à savoir quelle caisse encaisse là-bas.',
 etapes:[
  'Demander à Sam : <b>quelle caisse</b> encaisse à Perfume City (Lightspeed, autre, ou rien) ?',
  'Demander : veut-il <b>suivre le stock de Perfume City</b> dans l\'outil (deuxième inventaire), ou seulement voir ce qui est sorti ?',
  'Si c\'est une caisse connue, refaire la procédure Lightspeed pour ce deuxième magasin.'],
 cles:'À déterminer après la réponse'},

{id:'gros',nom:'Vente en gros',logo:'gros',role:'clients grossistes',sku:false,horsligne:true,
 recoit:'Rien : il n\'y a aucune plateforme derrière. C\'est du téléphone, du WhatsApp et des factures.',
 envoie:'Rien.',
 note:'Ce canal ne se connectera jamais — et ce n\'est pas un manque : une commande de Javier ou de Carmen se saisit dans <b>Ventes → + Enregistrer une vente</b>, canal « Gros », et le stock suit. C\'est déjà en place.',
 etapes:[
  'Rien à créer. Vérifier seulement que le personnel saisit bien chaque commande de gros dans Perfumes Trade.'],
 cles:'Aucune'}
];

/* ---------- état d'un canal ---------- */
const st=id=>CON[id]||(CON[id]={faites:[],cles:false,note:''});
function etat(c){
  const s=st(c.id), n=s.faites.length, t=c.etapes.length;
  if(c.horsligne) return {k:'hors',lib:'saisie à la main',pct:100};
  if(s.cles) return {k:'pret',lib:'clés reçues',pct:100};
  if(n>=t&&t) return {k:'encours',lib:'étapes faites, clés à remettre',pct:100};
  if(n) return {k:'encours',lib:n+' étape'+(n>1?'s':'')+' sur '+t,pct:Math.round(n/t*100)};
  return {k:'afaire',lib:'à faire',pct:0};
}

function carte(c){
  const s=st(c.id), e=etat(c), ouvert=!!s.ouvert, sk=s.sku;
  return `<article class="cx ${e.k}${ouvert?' on':''}" data-c="${c.id}">
    <header class="ch">
      ${logoHtml(c)}
      <h3>${esc(c.nom)}<span class="role">${esc(c.role)}</span></h3>
      ${c.horsligne?'':`<span class="jauge"><i style="width:${e.pct}%"></i></span>`}
      <span class="et ${e.k}">${e.lib}</span>
      <span class="fl">▸</span>
    </header>
    <div class="cb">
      <div class="quoi">
        <div><b>Ce qu'il fera entrer</b>${c.recoit}</div>
        <div><b>Ce qu'il fera sortir</b>${c.envoie}</div>
        <div><b>À savoir</b>${c.note}</div>
      </div>
      <ol class="et2">${c.etapes.map((t,i)=>`<li class="${s.faites.includes(i)?'ok':''}">
        <input type="checkbox" data-c="${c.id}" data-i="${i}"${s.faites.includes(i)?' checked':''}>
        <span class="n">${i+1}</span><span class="tx">${t}</span></li>`).join('')}</ol>
      ${c.horsligne?'':`<div class="cles">À remettre : ${esc(c.cles)}
        <span>Jamais dans un message, jamais dans cette page : un fichier texte, remis en main propre ou sur une clé USB.
        Coche ci-dessous quand le fichier est entre tes mains.</span>
        <label style="display:flex;align-items:center;gap:9px;margin-top:9px;color:var(--ink-2);font-weight:500">
          <input type="checkbox" data-cles="${c.id}"${s.cles?' checked':''} style="width:18px;height:18px;accent-color:var(--good)">
          J'ai reçu le fichier des clés pour ce canal</label></div>`}
      ${c.sku?blocSku(c,sk):''}
      <div class="note"><label>Notes sur ce canal</label>
        <textarea data-note="${c.id}" placeholder="Ce qu'il a répondu, ce qui bloque, la date de la demande…">${esc(s.note||'')}</textarea></div>
    </div>
  </article>`;
}
/* Le logo officiel s'il est dans logos/ ; sinon rien du tout : le nom est déjà écrit à côté. */
function logoHtml(c){
  if(!['amazon','shopify','site'].includes(c.logo)) return '';
  return `<span class="lg lg-${c.logo}"><img src="logos/${c.logo}.png" alt=""
    onerror="this.onerror=null;this.src='logos/${c.logo}.svg';
      this.onerror=function(){ this.parentNode.remove(); }"></span>`;
}

/* ---------- contrôle des SKU ---------- */
function blocSku(c,r){
  return `<div class="sku">
    <h4>Contrôle des SKU — ${esc(c.nom)}</h4>
    <p>C'est le point qui décide de tout : quand une vente arrive, ${esc(c.nom)} dit « vendu : SKU untel ».
    Si ce SKU est le code-barres, l'outil sait de quel parfum il s'agit et sort le bon flacon du stock.
    Sinon la vente tombe dans un panier « non reconnues » à démêler à la main.<br>
    Dépose ici l'<b>export des annonces</b> de ce canal (un fichier CSV avec une colonne SKU) : je compare
    avec les 3 830 codes-barres du catalogue.</p>
    <div class="dz" data-dz="${c.id}"><b>Dépose le fichier CSV ici</b>ou clique pour le choisir
      <input type="file" accept=".csv,.txt,.tsv" hidden data-file="${c.id}"></div>
    <div class="res" id="res-${c.id}">${r?resultatSku(c,r):''}</div>
  </div>`;
}
function resultatSku(c,r){
  const pct=r.total?Math.round(r.ok/r.total*100):0;
  const v = pct>=98?'g':pct>=80?'w':'c';
  const msg = pct>=98?`<b>Tout est en ordre.</b> ${pct} % des annonces portent un code-barres connu : les ventes de ce canal se rattacheront toutes seules au bon parfum.`
    : pct>=80?`<b>Presque.</b> ${pct} % des annonces sont reconnues, ${r.total-r.ok} ne le sont pas — à corriger sur ${esc(c.nom)} avant de brancher, sinon ces ventes-là devront être démêlées une par une.`
    : `<b>Ça ne suivra pas.</b> Seules ${pct} % des annonces portent un code-barres connu. Brancher le canal dans cet état créerait plus de travail que de saisir les ventes à la main : il faut d'abord remettre les SKU en ordre sur ${esc(c.nom)}.`;
  return `<div class="verdict ${v}">${msg}</div>
    <div class="bl">
      <div><b>${nf(r.total)}</b><span>annonces lues</span></div>
      <div><b class="g">${nf(r.ok)}</b><span>rattachées au catalogue</span></div>
      <div><b class="${r.inconnus.length?'c':'g'}">${nf(r.inconnus.length)}</b><span>SKU inconnus</span></div>
      <div><b class="${r.vides?'w':'g'}">${nf(r.vides)}</b><span>sans SKU du tout</span></div>
    </div>
    <div style="font-size:12.5px;color:var(--ink-3);margin-bottom:10px">Fichier : ${esc(r.fichier)} · colonne SKU utilisée : <code>${esc(r.colonne)}</code> · lu le ${esc(r.date)}</div>
    ${r.inconnus.length?`<table><thead><tr><th>SKU non reconnu</th><th>Annonce</th></tr></thead><tbody>${
      r.inconnus.slice(0,15).map(x=>`<tr><td><code>${esc(x[0])}</code></td><td>${esc(x[1]||'—')}</td></tr>`).join('')}</tbody></table>
      ${r.inconnus.length>15?`<p style="margin:8px 0 0;font-size:12.5px;color:var(--ink-3)">…et ${nf(r.inconnus.length-15)} autres.</p>`:''}
      <p style="margin:10px 0 0"><button class="btn sm" data-exp="${c.id}">Exporter les SKU non reconnus (CSV)</button>
      <button class="btn sm" data-raz="${c.id}">Effacer ce contrôle</button></p>`
    :`<p style="margin:0"><button class="btn sm" data-raz="${c.id}">Effacer ce contrôle</button></p>`}`;
}

/* lecture du CSV : on trouve la colonne SKU et une colonne de libellé */
function decoupe(t){
  const rows=[]; let cur=[], f='', q=false;
  const sep = (t.split('\n')[0].split('\t').length > t.split('\n')[0].split(',').length) ? '\t'
            : (t.split('\n')[0].split(';').length > t.split('\n')[0].split(',').length) ? ';' : ',';
  for(let i=0;i<t.length;i++){ const ch=t[i];
    if(q){ if(ch=='"'){ if(t[i+1]=='"'){ f+='"'; i++; } else q=false; } else f+=ch; }
    else { if(ch=='"') q=true;
      else if(ch===sep){ cur.push(f); f=''; }
      else if(ch=='\n'){ cur.push(f); rows.push(cur); cur=[]; f=''; }
      else if(ch!='\r') f+=ch; } }
  if(f||cur.length){ cur.push(f); rows.push(cur); }
  return rows;
}
const MOTS_SKU=['seller-sku','seller sku','sku vendeur','sku','ugs','référence','reference','code article','item number','barcode','code-barres','ean','upc','gtin'];
const MOTS_LIB=['item-name','title','titre','nom','product','produit','description','libellé','libelle','name'];
function analyse(nomFichier,texte){
  const rows=decoupe(texte).filter(r=>r.some(x=>(x||'').trim()));
  if(rows.length<2) return {err:"Ce fichier ne contient pas de tableau lisible."};
  const head=rows[0].map(h=>(h||'').trim().toLowerCase().replace(/^﻿/,''));
  let ci=-1;
  for(const m of MOTS_SKU){ const j=head.findIndex(h=>h===m); if(j>=0){ ci=j; break; } }
  if(ci<0) for(const m of MOTS_SKU){ const j=head.findIndex(h=>h.includes(m)); if(j>=0){ ci=j; break; } }
  if(ci<0) return {err:"Aucune colonne SKU trouvée. Les en-têtes lus : "+head.filter(Boolean).slice(0,10).join(', ')};
  let li=-1;
  for(const m of MOTS_LIB){ const j=head.findIndex(h=>h.includes(m)); if(j>=0&&j!==ci){ li=j; break; } }
  let ok=0, vides=0; const inconnus=[], vus=new Set();
  for(let i=1;i<rows.length;i++){
    const s=(rows[i][ci]||'').trim();
    if(!s){ vides++; continue; }
    const n=s.replace(/^0+/,'');
    if(BC[n]) ok++;
    else if(!vus.has(s)){ vus.add(s); inconnus.push([s, li>=0?(rows[i][li]||'').slice(0,70):'']); }
  }
  return {total:rows.length-1, ok, vides, inconnus, colonne:rows[0][ci]||('colonne '+(ci+1)),
          fichier:nomFichier, date:new Date().toLocaleDateString('fr-FR')};
}

/* ---------- dessin ---------- */
function dessine(){
  $('cartes').innerHTML=CANAUX.map(carte).join('');
  const pret=CANAUX.filter(c=>!c.horsligne&&etat(c).k==='pret').length;
  const enc=CANAUX.filter(c=>!c.horsligne&&etat(c).k==='encours').length;
  const af=CANAUX.filter(c=>!c.horsligne&&etat(c).k==='afaire').length;
  const skus=CANAUX.filter(c=>c.sku&&st(c.id).sku);
  const skuOk=skus.filter(c=>{const r=st(c.id).sku; return r.total&&r.ok/r.total>=0.98;}).length;
  $('kpis').innerHTML=`<div class="kpis">
    <div class="kpi"><div class="v g">${pret}</div><div class="k">canaux dont les clés sont reçues</div></div>
    <div class="kpi"><div class="v w">${enc}</div><div class="k">en cours chez ton ami</div></div>
    <div class="kpi"><div class="v">${af}</div><div class="k">pas encore commencés</div></div>
    <div class="kpi"><div class="v i">${skuOk} / ${skus.length||0}</div><div class="k">canaux dont les SKU sont vérifiés bons</div></div>
    <div class="kpi"><div class="v">0</div><div class="k">vente reçue automatiquement — il n'y a pas encore de serveur</div></div>
  </div>`;
  $('src').innerHTML=`${CANAUX.filter(c=>!c.horsligne).length} canaux à brancher<br>aucun connecté`;
}

$('tete').innerHTML=`<b>Cette page ne connecte rien — elle prépare le branchement.</b>
  Un connecteur a besoin de trois choses : un <b>serveur allumé en permanence</b> pour interroger les canaux,
  un <b>accès API créé par ton ami</b> sur chacun de ses comptes (personne d'autre ne peut le faire à sa place),
  et le <b>SKU de chaque annonce égal au code-barres</b> pour savoir de quel parfum on parle.
  Ici : la marche à suivre exacte pour chaque canal, l'avancement à cocher, et le contrôle des SKU dès qu'il
  envoie ses exports. Les clés, elles, ne se collent nulle part dans l'outil.`;
$('pied').innerHTML=`<b>Ce qui restera manuel, même tout branché.</b> Une vente encaissée en boutique sans passer
  par la caisse n'existe pour personne. Une commande de gros livrée de la main à la main non plus. Et il faudra
  traiter les <b>remboursements et annulations</b> (une vente annulée doit remettre le flacon en stock), les
  <b>lots</b> (une annonce « pack de 2 » doit sortir deux flacons) et le <b>stock envoyé chez Amazon</b> (FBA),
  qui n'est plus dans l'entrepôt. Aucun connecteur ne devine ces trois choses : elles se décident et se règlent.`;

/* ---------- interactions ---------- */
$('cartes').addEventListener('click',e=>{
  const h=e.target.closest('.ch');
  if(h && !e.target.closest('input')){ const c=h.parentNode.dataset.c; const s=st(c);
    s.ouvert=!s.ouvert; sauve(); dessine(); return; }
  const dz=e.target.closest('[data-dz]');
  if(dz){ dz.querySelector('input[type=file]').click(); return; }
  const ex=e.target.closest('[data-exp]');
  if(ex){ const id=ex.dataset.exp, r=st(id).sku; if(!r) return;
    const q=x=>'"'+String(x==null?'':x).replace(/"/g,'""')+'"';
    const li=['sku_non_reconnu;annonce'].concat(r.inconnus.map(x=>q(x[0])+';'+q(x[1])));
    const b=new Blob(['﻿'+li.join('\n')],{type:'text/csv;charset=utf-8'});
    const a=document.createElement('a'); a.href=URL.createObjectURL(b);
    a.download='sku-non-reconnus-'+id+'.csv'; a.click(); URL.revokeObjectURL(a.href); return; }
  const rz=e.target.closest('[data-raz]');
  if(rz){ delete st(rz.dataset.raz).sku; sauve(); dessine(); return; }
});
$('cartes').addEventListener('change',e=>{
  const t=e.target;
  if(t.dataset.i!==undefined){ const s=st(t.dataset.c), i=+t.dataset.i;
    if(t.checked){ if(!s.faites.includes(i)) s.faites.push(i); } else s.faites=s.faites.filter(x=>x!==i);
    sauve(); dessine();
    const c=CANAUX.find(x=>x.id===t.dataset.c);
    journal('étape '+(i+1)+(t.checked?' faite':' décochée'),c.nom,etat(c).lib); return; }
  if(t.dataset.cles!==undefined){ const s=st(t.dataset.cles); s.cles=t.checked; sauve(); dessine();
    journal(t.checked?'clés reçues':'clés non reçues',CANAUX.find(x=>x.id===t.dataset.cles).nom,null); return; }
  const f=t.dataset.file;
  if(f && t.files && t.files[0]){
    const fic=t.files[0], lec=new FileReader();
    lec.onload=()=>{ const r=analyse(fic.name,String(lec.result||''));
      if(r.err){ $('res-'+f).innerHTML=`<div class="verdict c">${esc(r.err)}</div>`; return; }
      st(f).sku=r; sauve(); dessine();
      journal('contrôle des SKU : '+r.ok+' sur '+r.total+' reconnus',CANAUX.find(x=>x.id===f).nom,r.fichier); };
    lec.readAsText(fic,'utf-8'); }
});
$('cartes').addEventListener('input',e=>{
  if(e.target.dataset.note!==undefined){ st(e.target.dataset.note).note=e.target.value; sauve(); }
});
['dragover','dragleave','drop'].forEach(ev=>$('cartes').addEventListener(ev,e=>{
  const dz=e.target.closest('[data-dz]'); if(!dz) return;
  e.preventDefault();
  if(ev==='dragover') dz.classList.add('over'); else dz.classList.remove('over');
  if(ev==='drop' && e.dataTransfer.files && e.dataTransfer.files[0]){
    const id=dz.dataset.dz, fic=e.dataTransfer.files[0], lec=new FileReader();
    lec.onload=()=>{ const r=analyse(fic.name,String(lec.result||''));
      if(r.err){ $('res-'+id).innerHTML=`<div class="verdict c">${esc(r.err)}</div>`; return; }
      st(id).sku=r; sauve(); dessine(); };
    lec.readAsText(fic,'utf-8'); }
}));

$('sfu').innerHTML = USR ? `Connecté : <b>${esc(USR)}</b>` : '';
$('sfoot').innerHTML='préparation<br>des branchements';
dessine();

/* ---------- le mur : seul un Admin branche les services extérieurs ----------
   Cette page manipule des clés d'API. Une clé WooCommerce donne accès aux
   commandes et aux clients du site ; une liaison de caisse, à ce qui s'y encaisse.
   Ce n'est pas de la gestion d'entreprise, c'est de la plomberie — et une erreur
   ici ne se voit pas : elle se découvre, plus tard, quand quelque chose a fuité
   ou cessé de remonter. Le patron dirige la boutique ; l'admin branche les tuyaux. */
(function(){
  const s=session(); if(!s) return;
  if(typeof peut!=='function' || peut('technique')) return;
  const w=document.querySelector('.wrap'); if(!w) return;
  w.querySelectorAll('#tete,#kpis,#cartes,.sec,.ordre').forEach(e=>e.remove());
  w.insertAdjacentHTML('beforeend',
    `<div class="mur" style="border:1px solid var(--line);border-radius:12px;padding:26px 28px;
      background:var(--surface);max-width:70ch">
     <h2 style="margin:0 0 8px;font-size:19px">Cette page est réservée à un compte Admin</h2>
     <p style="margin:0;color:var(--ink-2);line-height:1.65">Tu es connecté comme
     <b>${esc(s.nom)}</b> (${esc((ROLES[s.role]||{}).lib||s.role)}).
     Brancher un service extérieur, c'est manipuler des clés qui donnent accès au site,
     à la caisse et à ce qui s'y encaisse. Ce droit est réservé au compte qui installe
     et entretient l'outil.<br><br>
     Si tu as besoin qu'un canal soit branché, demande-le à l'Admin — il n'y a rien
     à préparer de ton côté.</p></div>`);
  const src=document.getElementById('src'); if(src) src.innerHTML='réservé à un Admin';
})();
"""

html = coquille("Connecteurs", "Connecteurs",
    "Brancher les canaux de vente sur Perfumes Trade : la marche à suivre pour créer chaque accès, "
    "l'avancement, et le contrôle des SKU. Rien ne se connecte tant qu'il n'y a pas de serveur.",
    CSS, CORPS, JS, donnees=('produits',))
html = html.replace('__BC__',
  'Object.fromEntries(window.D_PROD.filter(r=>r[0]).map(r=>'
  '[String(r[0]).replace(/^0+/,\'\'),((r[2]||\'\')+\' \'+(r[13]||\'\')).trim()]))')
open('connecteurs.html', 'w').write(html)
print('connecteurs.html', len(html)//1024, 'Ko')
