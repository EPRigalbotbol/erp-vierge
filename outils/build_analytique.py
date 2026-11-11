# -*- coding: utf-8 -*-
"""ANALYTIQUE — la rubrique des admins, sous le Tableau de bord (9 nov. 2026).

Igal, 8 nov. 2026 : « qu'on crée une rubrique en dessous de dashboard… l'analytics de tous les sites référencés, tous les
canaux de vente… voir l'amélioration en direct » (le but premier : savoir si Google Shopping fait vendre), puis
« fais-moi un très beau truc », et « c'est vraiment une rubrique qu'on crée pour les admins » : en français et en
anglais seulement (en espagnol, la page est en anglais), et fermée au Commercial (mur « voirMarge », comme le Tableau de bord).

Ce que la page montre, sur la période choisie (7 jours, 30 jours, ce mois, mois dernier, 90 jours, cette année),
comparée à la période d'avant de même longueur :
  1. cinq chiffres : chiffre d'affaires de tous les canaux, marge nette, ventes des sites en ligne, commandes en ligne
     (panier moyen), part venue de Google — chacun avec sa courbe jour par jour ;
  2. D'OÙ VIENNENT LES COMMANDES DES SITES : Google Shopping, Google Ads, recherche Google, réseaux sociaux, email,
     venus directement, autres — en colonnes empilées jour par jour, et en classement ;
  3. les mêmes origines, site par site (perfumestrade.com, wholesale, Perfume City en ligne) ;
  4. tous les canaux de vente (sites, Amazon, caisse, gros, Perfume City), avec leur évolution ;
  5. les parfums qui se vendent en ligne, et la part de Google pour chacun.

Les chiffres de vente sont CEUX DU TABLEAU DE BORD ET DE LA PAGE VENTES : la page reprend le même calcul (_recap.py,
rcLignes / rcAgrege). L'origine d'une commande vient du cockpit (magasin « ventes-origine-v1 », origines.js), qui la
lit chez WooCommerce (attribution de commande) et chez Shopify (parcours client) — en lecture seule.
"""
import json
from build_crm import coquille
from _recap import RECAP_CSS, RECAP_JS

CSS = RECAP_CSS + r'''
.mur{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:34px 32px;max-width:640px;margin:26px auto}
.mur h2{margin:0 0 10px;font-size:20px;font-weight:700;letter-spacing:-.015em}
.mur p{margin:0;color:var(--ink-2);font-size:14.5px;line-height:1.65}
'''

CORPS = '<div id="an"></div>'

JS = r'''
/*__RECAP__*/
const IDX=__IDX__;
const KREG='reglages-v1', KMOD='fiches-modifiees-v1', KFACT='factures-v1';
let REG={}, MOD={}, FACT=[];
try{ REG=JSON.parse(localStorage.getItem(KREG)||'{}')||{}; }catch(e){}
try{ MOD=JSON.parse(localStorage.getItem(KMOD)||'{}')||{}; }catch(e){}
try{ FACT=JSON.parse(localStorage.getItem(KFACT)||'[]')||[]; }catch(e){}
if(!Array.isArray(FACT)) FACT=[];
/* une rubrique des admins : en français ou en anglais (Igal, 9 nov. 2026) — l'espagnol lit l'anglais */
const A3=(fr,en)=>L3(fr,en,en);
const AN_K='analytique-vue';      /* la période et la mesure choisies : propres à ce navigateur, jamais envoyées au serveur */
const AN={sel:'rel:30',met:'n',site:'tous',src:'n'};
try{ const r=JSON.parse(localStorage.getItem(AN_K)||'null'); if(r&&typeof r==='object'){ ['sel','met','site','src','ppf','pptri'].forEach(k=>{ if(r[k]) AN[k]=r[k]; }); } }catch(e){}
const anSauve=()=>{ try{ const o=Object.assign({},AN); delete o.ppq; delete o.ppn; localStorage.setItem(AN_K,JSON.stringify(o)); }catch(e){} };

/* ---- les origines : sept familles + « inconnue », une couleur fixe chacune (palette validée, clair et sombre) ---- */
const AN_GR=[
  {k:'gshop',c:1,fr:'Google Shopping',en:'Google Shopping',aide:['les fiches produits gratuites de Google','Google\'s free product listings']},
  {k:'gads',c:2,fr:'Google Ads (payant)',en:'Google Ads (paid)',aide:['un clic sur une publicité Google','a click on a Google ad']},
  {k:'google',c:3,fr:'Recherche Google',en:'Google search',aide:['les résultats ordinaires de Google','Google\'s regular results']},
  {k:'social',c:4,fr:'Réseaux sociaux',en:'Social media',aide:['Instagram, Facebook, TikTok…','Instagram, Facebook, TikTok…']},
  {k:'email',c:5,fr:'Email',en:'Email',aide:['un email ou une newsletter','an email or a newsletter']},
  {k:'direct',c:6,fr:'Venus directement',en:'Direct',aide:['adresse tapée, favori, lien sans source','typed address, bookmark, link without source']},
  {k:'autre',c:7,fr:'Autres sources',en:'Other sources',aide:['autres sites, autres moteurs, IA, commandes saisies à la main','other sites, other search engines, AI, orders entered by hand']},
  {k:'inconnu',c:0,fr:'Origine inconnue',en:'Unknown origin',aide:['la boutique ne l\'a pas notée','the store did not record it']}];
/* le petit « i » de chaque origine (Igal, 9 nov. 2026 : « email, je ne sais pas ce que ça veut dire, venu direct… explique avec un petit i ») */
const AN_INFO={
  gshop:['Le client a cliqué sur une fiche produit GRATUITE de Google : l\'onglet Shopping, ou les photos de produits dans les résultats. Ça ne coûte rien à Sam.','The customer clicked a FREE Google product listing: the Shopping tab, or product photos in the results. It costs Sam nothing.'],
  gads:['Le client a cliqué sur une PUBLICITÉ Google payée par Sam (annonce Shopping, Performance Max ou annonce texte). Chaque clic est facturé par Google.','The customer clicked a Google AD paid for by Sam (Shopping ad, Performance Max or text ad). Google charges for every click.'],
  google:['Le client a cherché sur Google et cliqué sur un résultat normal, non payant, qui mène au site.','The customer searched on Google and clicked a regular, unpaid result leading to the site.'],
  social:['Le client est arrivé depuis un réseau social : Instagram, Facebook, TikTok, WhatsApp… (une publication, le lien de la bio, une story). Le détail est écrit sous le nom.','The customer came from social media: Instagram, Facebook, TikTok, WhatsApp… (a post, the bio link, a story). Details are shown under the name.'],
  email:['Le client a cliqué sur un lien dans un email : une newsletter (Klaviyo), un email de relance de panier, ou un email envoyé par Sam.','The customer clicked a link in an email: a newsletter (Klaviyo), an abandoned-cart reminder, or an email sent by Sam.'],
  direct:['Le client a tapé l\'adresse du site, utilisé un favori, ou cliqué sur un lien qui ne dit pas d\'où il vient (souvent un lien envoyé par WhatsApp ou SMS). En général : un client qui connaît déjà le site.','The customer typed the site address, used a bookmark, or clicked a link that doesn\'t say where it comes from (often a link sent by WhatsApp or text). Usually a customer who already knows the site.'],
  autre:['Tout le reste : un autre site (blog, forum, comparateur), un autre moteur (Bing, Yahoo), une IA (ChatGPT…), l\'application Shop de Shopify, ou une commande saisie à la main. Le détail est écrit sous le nom.','Everything else: another website (blog, forum, price comparison), another search engine (Bing, Yahoo), an AI (ChatGPT…), Shopify\'s Shop app, or an order entered by hand. Details are shown under the name.'],
  inconnu:['La boutique n\'a pas noté d\'où venait le client : navigateur qui bloque le suivi, commande trop ancienne, ou commande passée depuis l\'administration du site.','The store did not record where the customer came from: a browser blocking tracking, an order that is too old, or an order placed from the site\'s admin.']};
const anInfo=k=>{ const t=AN_INFO[k]; return t?`<button type="button" class="ga-i" data-info="${esc(A3(t[0],t[1]))}" aria-label="${esc(A3('Qu\'est-ce que c\'est ?','What is this?'))}">i</button>`:''; };
const anGr=k=>AN_GR.find(g=>g.k===k)||AN_GR[AN_GR.length-1];
const anCoul=k=>`var(--an-${anGr(k).c})`;
const anNomGr=k=>{ const g=anGr(k); return A3(g.fr,g.en); };
const GOOGLE=new Set(['gshop','gads','google']);
function anFamille(code){ const c=String(code||''); const t=c.split(':')[0];
  if(t==='gshop'||t==='gads'||t==='google'||t==='email'||t==='direct') return t;
  if(t==='social') return 'social';
  if(!c||t==='inconnu') return 'inconnu';
  return 'autre'; }
/* le détail d'une origine (« instagram », « fragrantica.com », « IA »…), pour les sous-lignes */
function anDetail(code){ const c=String(code||''); const [t,d]=c.split(/:(.*)/s);
  if(t==='social') return ({instagram:'Instagram',facebook:'Facebook',tiktok:'TikTok',pinterest:'Pinterest',youtube:'YouTube',whatsapp:'WhatsApp',x:'X',snapchat:'Snapchat',linkedin:'LinkedIn',reddit:'Reddit',threads:'Threads'})[d]||d||'';
  if(t==='site') return d||''; if(t==='moteur') return A3('autres moteurs','other search engines'); if(t==='ia') return A3('IA (ChatGPT…)','AI (ChatGPT…)');
  if(t==='manuel') return A3('saisie à la main','entered by hand'); return ''; }

/* ---- les sites en ligne ---- */
const AN_SITES=[{id:'site',auto:'woocommerce',nom:'perfumestrade.com'},{id:'sitegros',auto:'woocommerce-gros',nom:'wholesale.perfumestrade.com'},
  {id:'pc',auto:'shopify-pc',ou:'en ligne',nom:'Perfume City',sous:['en ligne','online']}];
const anSiteDe=v=>{ const a=String(v.auto||''); if(a==='woocommerce') return 'site'; if(a==='woocommerce-gros') return 'sitegros'; if(a==='shopify-pc'&&v.ou==='en ligne') return 'pc'; return ''; };
const anSiteNom=id=>{ const s=AN_SITES.find(x=>x.id===id); return s?(s.nom+(s.sous?' '+A3(s.sous[0],s.sous[1]):'')):id; };

let ORI={};
try{ ORI=JSON.parse(localStorage.getItem('ventes-origine-v1')||'{}')||{}; }catch(e){ ORI={}; }

/* les commandes des sites, une par facture (les lignes du même calcul que Ventes, regroupées) */
function anCommandes(L){
  const I={}; FACT.forEach(f=>{ if(f&&f.id) I[f.id]=String(f._i||'').replace(/^fa\|/,''); });
  const M=new Map();
  L.forEach(v=>{ const s=anSiteDe(v); if(!s||v.hist) return;
    const k=(v.fid||v.num)+'|'+(v.cmd||'');
    let o=M.get(k); if(!o){ const id=I[v.fid]||''; const code=id?ORI[id]:'';
      o={k,site:s,d:v.d,ca:0,mg:0,q:0,ret:!!v.ret,code:code||'',fam:anFamille(code),lu:!!code,lignes:[]}; M.set(k,o); }
    o.ca+=v.mt||0; o.mg+=v.mg||0; o.q+=v.q||0; o.lignes.push(v); });
  return [...M.values()];
}
const anDans=(X,a,b)=>X.filter(o=>o.d>=a&&o.d<=b);
function anSomme(C){ const T={ca:0,mg:0,n:0,q:0}; C.forEach(o=>{ T.ca+=o.ca; T.mg+=o.mg; T.q+=o.q; if(!o.ret) T.n++; }); return T; }
function anParFam(C){ const G={}; C.forEach(o=>{ const g=G[o.fam]=G[o.fam]||{ca:0,n:0,q:0,det:{}}; g.ca+=o.ca; g.q+=o.q; if(!o.ret){ g.n++; const d=anDetail(o.code); if(d) g.det[d]=(g.det[d]||0)+1; } }); return G; }

/* ================= LE DESSIN (refait le 9 nov. 2026) =================
   Igal : « je n'aime pas du tout les organigrammes… fais-moi quelque chose de plus animé, plus clair, plus professionnel,
   qui ressemble plus à du Google » et « remettre les cases chiffre d'affaires, marge nette… c'est pas logique, on les a déjà
   dans le dashboard ». Donc, à la manière de Google Analytics :
     1. une carte à onglets (commandes en ligne, chiffre d'affaires, marge, commandes Google Ads) : l'onglet choisi trace sa
        courbe jour par jour, la période d'avant en pointillé, une ligne verticale et une bulle au survol ;
     2. les sources des commandes en barres horizontales qui se remplissent ;
     3. Google Ads : est-ce que la pub rapporte ? — deux courbes cumulées (la marge des commandes venues de la pub, la pub
        dépensée) et un verdict en une phrase ;
     4. les parfums qui se vendent en ligne.
   Les chiffres arrivent en comptant, les courbes se dessinent ; rien ne bouge pour qui a demandé moins d'animations. */
/* l'évolution, écrite en clair (Igal, 9 nov. 2026, devant « 69 % ↓ 22 % » : « même moi, je ne les comprends pas ») :
   « ↓ 22 % vs octobre 2026 » — jamais une flèche seule */
function anDelta(a,b,lib){ if(b==null) return '';
  const p=gaPct(a,b); if(p==null) return a?`<span class="ga-d up">${A3('nouveau','new')}${lib?` <span class="ga-vs">vs <span data-nolang>${esc(lib)}</span></span>`:''}</span>`:'';
  const s=p>0.5?'up':p<-0.5?'dn':'eq';
  return `<span class="ga-d ${s}">${s==='up'?'↑':s==='dn'?'↓':'='} ${nf(Math.round(Math.abs(p)))} %${lib?` <span class="ga-vs">vs <span data-nolang>${esc(lib)}</span></span>`:''}</span>`; }
/* ---- les jours (ou les mois) de la période, sans les jours à venir ---- */
function anJours(P){ const B=rcBuckets(P,[]); const auj=rcISO(new Date());
  const K=B.K.filter(k=>B.jour?k.k<=auj:k.k<=auj.slice(0,7)); return {K,jour:B.jour}; }
function anSerieK(B,X,val){ const idx={}; B.K.forEach((k,i)=>idx[k.k]=i); const s=B.K.map(()=>0);
  X.forEach(o=>{ const i=idx[B.jour?o.d:o.d.slice(0,7)]; if(i!=null) s[i]+=val(o); }); return s; }
/* la période d'avant, posée jour pour jour sous la période choisie (même nombre de colonnes) */
function anSeriePrec(B,Q,X,val){ if(!Q) return null; const BQ=rcBuckets({a:Q.a,b:Q.b},[]); if(BQ.jour!==B.jour) return null;
  const s=anSerieK(BQ,X,val); return B.K.map((_,i)=>i<s.length?s[i]:null); }

/* ---- l'état des relectures du cockpit (dernière lecture, panne) ---- */
function anEtat(){
  const E=[['_woocommerce','perfumestrade.com'],['_woocommerce-gros','wholesale.perfumestrade.com'],['_shopify-pc','Perfume City']];
  const vu=E.map(([k,n])=>({n,e:ORI[k]})).filter(x=>x.e);
  const pannes=vu.filter(x=>x.e.err);
  return {vu,pannes,pannesTxt:pannes.map(x=>`<span data-nolang>${esc(x.n)} — ${esc(String(x.e.err).slice(0,160))}</span>`).join('<br>')};
}
/* la pub Google (google-pub-v1, jour par jour : [pub, ventes Google, clics, affichages, conversions, clics gratuits, affichages gratuits]) */
function anPubJ(){ let G={}; try{ G=JSON.parse(localStorage.getItem('google-pub-v1')||'{}')||{}; }catch(e){} G=G||{};
  /* 10 nov. 2026 : quand le script posé dans Google Ads envoie ses chiffres (google-ads-v1), ils remplacent ceux de l'extension
     pour la pub payante — toutes les campagnes, pas seulement Performance Max ; les fiches gratuites restent celles de l'extension */
  const A=anAdsJ(); if(!A||!A.j||!Object.keys(A.j).length) return G;
  const J=Object.assign({},G.j||{});
  Object.keys(A.j).forEach(d=>{ const a=A.j[d]||[], g=J[d]||[]; J[d]=[+a[0]||0,+a[1]||0,+a[2]||0,+a[3]||0,+a[4]||0,+g[5]||0,+g[6]||0]; });
  const R=Object.assign({},G,{j:J,_err:''}); if(A.p&&Array.isArray(A.p.L)&&A.p.L.length) R.p=A.p; return R; }
function anAdsJ(){ try{ const A=JSON.parse(localStorage.getItem('google-ads-v1')||'null'); return (A&&typeof A==='object')?A:null; }catch(e){ return null; } }
function anPub(a,b){ const G=anPubJ(); const J=G.j||{}; const T={pub:0,ventes:0,clics:0,aff:0,conv:0,gClics:0,gAff:0,jours:0};
  Object.keys(J).forEach(d=>{ if(d<a||d>b) return; const r=J[d]||[]; T.jours++; T.pub+=+r[0]||0; T.ventes+=+r[1]||0; T.clics+=+r[2]||0; T.aff+=+r[3]||0; T.conv+=+r[4]||0; T.gClics+=+r[5]||0; T.gAff+=+r[6]||0; });
  return {T,J,lu:Object.keys(J).length>0,err:G._err||''}; }

function anDessine(){
  const z=document.getElementById('an'); if(!z) return;
  const L=rcLignes(), P=rcPlage(AN.sel), Q0=rcPrec(AN.sel,P);
  /* comme le Tableau de bord : pas de comparaison avec une période d'avant le 1er oct. 2026 (chiffres incomplets) */
  const Q=(Q0&&Q0.a<RC_COMPLET)?null:Q0, lib=Q?rcLibPrec(AN.sel,Q):'';
  const tous=anCommandes(L), duSite=o=>AN.site==='tous'||o.site===AN.site;
  const CMD=tous.filter(duSite), C=anDans(CMD,P.a,P.b), CP=Q?anDans(CMD,Q.a,Q.b):null;
  const B=anJours(P);
  B.K.forEach(k=>{ k.court2=B.jour?new Date(k.k+'T12:00:00').toLocaleDateString(A3('fr-FR','en-US'),{day:'numeric',month:'short'}):k.court; });
  const per=[['rel:7',A3('7 jours','7 days')],['rel:30',A3('30 jours','30 days')],['cemois',A3('Ce mois','This month')],['moisdernier',A3('Mois dernier','Last month')],['rel:90',A3('90 jours','90 days')],['cetteannee',A3('Cette année','This year')]];
  const sites=[['tous',A3('Tous les sites','All sites')],['site','perfumestrade.com'],['sitegros','wholesale'],['pc',A3('Perfume City en ligne','Perfume City online')]];
  let h=`<div class="ga-top"><div class="ga-seg">${per.map(([v,l])=>`<button type="button" class="${AN.sel===v?'on':''}" data-an="${v}">${l}</button>`).join('')}</div>
    <div class="ga-seg">${sites.map(([v,l])=>`<button type="button" class="${AN.site===v?'on':''}" data-ans="${v}"><span data-nolang>${esc(l)}</span></button>`).join('')}</div></div>
    <p class="ga-per"><b data-nolang>${esc(rcLib(AN.sel,P))}</b>${Q?` · ${A3('comparé à','compared with')} <span data-nolang>${esc(lib)}</span>`:''}</p>`;
  const etat=anEtat();
  if(etat.pannes.length) h+=`<div class="an-alerte">${A3('Le cockpit n\'arrive pas à lire l\'origine des commandes de :','The cockpit cannot read the origin of orders from:')}<br>${etat.pannesTxt}</div>`;
  /* ---- 1. la carte à onglets ---- */
  const ok=o=>!o.ret;
  const M=[{k:'n',nom:A3('Commandes en ligne','Online orders'),f:'n',val:o=>ok(o)?1:0},
    {k:'ca',nom:A3("Chiffre d'affaires en ligne",'Online revenue'),f:'$',val:o=>o.ca},
    {k:'mg',nom:A3('Marge nette en ligne','Online net margin'),f:'$',val:o=>o.mg},
    {k:'gads',nom:A3('Commandes via Google Ads','Orders via Google Ads'),f:'n',val:o=>ok(o)&&o.fam==='gads'?1:0}];
  if(!M.some(m=>m.k===AN.met)) AN.met='n';
  const tot=(X,m)=>X?X.reduce((a,o)=>a+m.val(o),0):null;
  h+=`<section class="ga-card"><div class="ga-tabs">${M.map(m=>{ const v=tot(C,m), vp=tot(CP,m);
      return `<button type="button" class="ga-tab ${AN.met===m.k?'on':''}" data-anm="${m.k}"><span class="ga-tl">${m.nom}</span><span class="ga-tv">${gaCnt(v,m.f,v<0?'neg':'')}</span>${anDelta(v,vp,lib)}</button>`; }).join('')}</div>
    <div class="ga-plot" id="ga-c1"></div>
    <div class="ga-leg"><span><i class="ga-li"></i><span data-nolang>${esc(rcLib(AN.sel,P))}</span></span>${Q?`<span><i class="ga-li prec"></i><span data-nolang>${esc(lib)}</span></span>`:''}</div></section>`;
  /* ---- 2. les sources ---- */
  const G=anParFam(C), GP=CP?anParFam(CP):null;
  const nTot=Math.max(1,C.filter(ok).length), caTot=Math.max(1,C.reduce((a,o)=>a+Math.max(0,o.ca),0));
  const parCA=AN.src==='ca';
  const rangs=AN_GR.filter(g=>G[g.k]&&(G[g.k].n||G[g.k].ca)).sort((a,b)=>(a.k==='inconnu')-(b.k==='inconnu')||(parCA?G[b.k].ca-G[a.k].ca:G[b.k].n-G[a.k].n));
  const max=Math.max(1,...rangs.map(g=>parCA?Math.max(0,G[g.k].ca):G[g.k].n));
  const det=g=>{ const d=Object.entries(g.det).sort((a,b)=>b[1]-a[1]); return d.length?`<small data-nolang>${d.slice(0,4).map(([n,c])=>esc(n)+' '+c).join(' · ')}</small>`:''; };
  h+=`<div class="ga-duo"><section class="ga-card ga-pad"><div class="ga-h"><h3>${A3('D\'où viennent les commandes','Where orders come from')}</h3>
      <div class="ga-mini">${[['n',A3('Commandes','Orders')],['ca',A3("Chiffre d'affaires",'Revenue')]].map(([v,l])=>`<button type="button" class="${(AN.src||'n')===v?'on':''}" data-ansrc="${v}">${l}</button>`).join('')}</div></div>
      ${rangs.length?`<div class="ga-bars">${rangs.map(gr=>{ const g=G[gr.k], gp=GP&&GP[gr.k]; const v=parCA?g.ca:g.n; const part=parCA?Math.max(0,g.ca)/caTot*100:g.n/nTot*100;
        return `<div class="ga-bar"><div class="ga-bn"><i style="background:${anCoul(gr.k)}"></i><span><span class="ga-bnm">${esc(anNomGr(gr.k))}${anInfo(gr.k)}</span>${det(g)}</span></div>
          <div class="ga-bt"><div class="ga-bf" style="--w:${Math.max(1.5,Math.max(0,v)/max*100).toFixed(1)}%;background:${anCoul(gr.k)}"></div></div>
          <div class="ga-bv">${parCA?gaCnt(v,'$'):gaCnt(v,'n')+' <span class="ga-u">'+A3('cmd','ord.')+'</span>'}<small>${nf(Math.round(part))} % ${parCA?A3('du chiffre d\'affaires','of revenue'):A3('des commandes','of orders')}</small>${GP?'<small>'+(gp?anDelta(parCA?g.ca:g.n,parCA?gp.ca:gp.n,lib):`<span class="ga-d up">${A3('nouveau','new')}</span>`)+'</small>':''}</div></div>`; }).join('')}</div>`
        :`<p class="ga-vide">${A3('Aucune commande en ligne sur cette période.','No online order in this period.')}</p>`}
    </section>`;
  /* ---- 3. Google Ads : est-ce que la pub rapporte ? (la pub tourne sur perfumestrade.com : on compare avec ce site seulement) ---- */
  const pub=anPub(P.a,P.b);
  h+=`<section class="ga-card ga-pad"><div class="ga-h"><h3>${A3('Google Ads : est-ce que la pub rapporte ?','Google Ads: do the ads pay off?')}</h3><span class="ga-src" data-nolang>perfumestrade.com</span></div>`;
  let ads=null;
  if(!pub.lu){ h+=`<p class="ga-vide">${pub.err?A3('Le cockpit n\'arrive pas à lire les chiffres de Google : ','The cockpit cannot read Google\'s figures: ')+'<span data-nolang>'+esc(pub.err)+'</span>':A3('Les chiffres de Google arrivent : le cockpit les lit une fois par heure.','Google\'s figures are on their way: the cockpit reads them once an hour.')}</p>`; }
  else {
    const A=anDans(tous.filter(o=>o.site==='site'&&o.fam==='gads'),P.a,P.b);
    const mgA=A.reduce((a,o)=>a+o.mg,0), caA=A.reduce((a,o)=>a+o.ca,0), nA=A.filter(ok).length, reste=mgA-pub.T.pub;
    ads={A,mgA,pub};
    const bon=reste>=0;
    h+=`<div class="ga-verdict ${bon?'bon':'mal'}"><span class="ga-vv">${gaCnt(reste,'$')}</span><span class="ga-vt">${bon?A3('gagnés après avoir payé la pub','earned after paying for the ads'):A3('perdus : la pub a coûté plus que la marge des commandes qu\'elle a amenées','lost: the ads cost more than the margin of the orders they brought')}</span></div>
      <div class="ga-plot ga-plot2" id="ga-c2"></div>
      <div class="ga-stats">
        <div><span>${A3('La pub coûte, par commande','Ad cost per order')}</span><b>${nA?money(pub.T.pub/nA):'—'}</b></div>
        <div><span>${A3('Une commande de la pub rapporte','An order from the ads earns')}</span><b>${nA?money(mgA/nA):'—'}</b><small>${A3('de marge nette','net margin')}</small></div>
        <div><span>${A3('Ventes : selon Google / réelles','Sales: per Google / actual')}</span><b>${money(pub.T.ventes)} / ${money(caA)}</b><small>${nf(nA)} ${A3('commandes expédiées','shipped orders')}</small></div>
      </div>${anAttente(P)}
      <div class="ga-free ${pub.T.gClics?'':'ko'}"><b>${A3('Google Shopping gratuit','Free Google Shopping')}</b> · ${nf(Math.round(pub.T.gClics))} ${A3('clic'+(pub.T.gClics>1?'s':''),'click'+(pub.T.gClics>1?'s':''))} · ${nf(Math.round(pub.T.gAff))} ${A3('affichages','impressions')}${pub.T.gClics?'':` — <span>${A3('aucun clic : Google ne montre presque pas les fiches gratuites (à voir dans Merchant Center)','no clicks: Google barely shows the free listings (to check in Merchant Center)')}</span>`}</div>`;
  }
  h+=`</section></div>`;
  /* ---- 3a. les visites et les recherches Google, en direct (robot Google, 11 nov. 2026) ---- */
  if(AN.site==='tous'||AN.site==='site') h+=anVisites();
  /* ---- 3b. la pub, parfum par parfum (90 jours) : lesquels garder, lesquels sortir, combien Sam économiserait ---- */
  if(AN.site==='tous'||AN.site==='site') h+=anCampagnes(tous);
  if(AN.site==='tous'||AN.site==='site') h+=anParfumsPub(tous);
  /* (9 nov. 2026) « Les parfums qui se vendent en ligne » retiré à la demande d'Igal : sur une période courte, chaque parfum ne
     se vend qu'une ou deux fois en ligne — un classement sans intérêt. Le détail par parfum reste dans la fiche du Catalogue. */
  /* ---- 5. la stratégie et le rapport du mois (agents, cockpit) ---- */
  h+=anStrategie(L,tous);
  /* ---- 6. le journal des actions (11 nov. 2026) ---- */
  h+=anJournal();
  const lus=C.filter(o=>ok(o)&&o.lu).length, nC=C.filter(ok).length;
  h+=`<p class="ga-note">${A3('Ventes et marges comptées comme dans Ventes et le Tableau de bord (commandes expédiées, remboursements déduits). L\'origine d\'une commande est notée par la boutique elle-même (WooCommerce, Shopify) ; « Google Ads » = un clic sur une publicité payante. La pub est lue chaque heure chez Google.','Sales and margins counted as in Sales and the Dashboard (shipped orders, refunds deducted). The origin of an order is recorded by the store itself (WooCommerce, Shopify); “Google Ads” = a click on a paid ad. Ad spend is read from Google every hour.')}${nC?' '+A3(`Origine connue pour ${nf(lus)} des ${nf(nC)} commandes.`,`Origin known for ${nf(lus)} of the ${nf(nC)} orders.`):''}</p>`;
  z.innerHTML=h;
  /* les courbes, une fois la page posée (il faut la largeur réelle des cartes) */
  const m=M.find(x=>x.k===AN.met);
  const cur=anSerieK(B,C,m.val), prev=CP?anSeriePrec(B,Q,CP,m.val):null;
  const REP=anReperes(B,P);
  gaCourbe(document.getElementById('ga-c1'),B.K,[{v:cur,c:'var(--an-1)',nom:m.nom,nomTip:rcLib(AN.sel,P),aire:true}].concat(prev?[{v:prev,c:'var(--ga-prec)',nom:lib,nomTip:lib,pointille:true}]:[]),m.f,{id:'a',h:270,titre:m.nom,reperes:REP,
    tipPlus:i=>(REP[i]||[]).length?`<div class="ga-tip-j">${REP[i].slice(0,4).map(e=>`<p><i></i>${esc(e.quoi)}</p>`).join('')}${REP[i].length>4?`<p>+ ${REP[i].length-4}</p>`:''}</div>`:''});
  if(ads){ const cum=a=>{ let s=0; return a.map(v=>s+=v); };
    const pubJ=B.K.map(k=>{ let s=0; Object.keys(ads.pub.J).forEach(d=>{ if((B.jour?d:d.slice(0,7))===k.k&&d>=P.a&&d<=P.b) s+=+(ads.pub.J[d]||[])[0]||0; }); return s; });
    const mgJ=anSerieK(B,ads.A,o=>o.mg);
    gaCourbe(document.getElementById('ga-c2'),B.K,[{v:cum(mgJ),c:'var(--an-3)',nom:A3('Marge des commandes de la pub','Margin of ad orders'),aire:true,etiquette:true},{v:cum(pubJ),c:'var(--an-2)',nom:A3('Pub dépensée','Ad spend'),etiquette:true}],'$',{id:'b',h:210,droite:16,titre:A3('Marge cumulée et pub cumulée','Cumulative margin and ad spend')}); }
  /* les barres se remplissent */
  if(GA_MOUV&&gaAnime){ z.querySelectorAll('.ga-bf,.ga-pb i').forEach(b=>{ b.style.width='0'; }); requestAnimationFrame(()=>requestAnimationFrame(()=>z.querySelectorAll('.ga-bf,.ga-pb i').forEach(b=>{ b.style.width=''; }))); }
  gaCompte(z);
  anBranche(); gaAnime=false;
}
function anBranche(){
  const z=document.getElementById('an'); if(!z) return;
  const bulle=()=>{ let t=document.getElementById('ga-info'); if(!t){ t=document.createElement('div'); t.id='ga-info'; t.className='ga-info'; document.body.appendChild(t); } return t; };
  const montre=b=>{ const t=bulle(); t.textContent=b.dataset.info; t.style.display='block'; const r=b.getBoundingClientRect(), w=t.offsetWidth;
    let L=r.left+r.width/2-w/2; L=Math.max(8,Math.min(innerWidth-w-8,L)); let T=r.bottom+8; if(T+t.offsetHeight>innerHeight-8) T=r.top-t.offsetHeight-8; t.style.left=L+'px'; t.style.top=T+'px'; };
  const cache=()=>{ const t=document.getElementById('ga-info'); if(t) t.style.display='none'; };
  z.querySelectorAll('.ga-i').forEach(b=>{ b.onmouseenter=()=>montre(b); b.onmouseleave=cache; b.onfocus=()=>montre(b); b.onblur=cache; b.onclick=e=>{ e.stopPropagation(); montre(b); }; });
  if(!window._anInfoDoc){ window._anInfoDoc=1; document.addEventListener('click',cache); window.addEventListener('scroll',cache,{passive:true}); }
  const xl=document.getElementById('an-xl'); if(xl) xl.onclick=anExportPub;
  anGcBranche();
  if(document.getElementById('pp-liste')){ anPPListe();
    z.querySelectorAll('[data-ppf]').forEach(b=>b.onclick=()=>{ AN.ppf=b.dataset.ppf; AN.ppn=25; z.querySelectorAll('[data-ppf]').forEach(x=>x.classList.toggle('on',x===b)); anSauve(); anPPListe(); });
    const t=document.getElementById('pp-tri'); if(t) t.onchange=()=>{ AN.pptri=t.value; AN.ppn=25; anSauve(); anPPListe(); };
    const q=document.getElementById('pp-q'); if(q) q.oninput=()=>{ AN.ppq=q.value; AN.ppn=25; anPPListe(); }; }
  clearInterval(window._anChrono); const ch=document.querySelector('.sc-chrono');
  if(ch) window._anChrono=setInterval(()=>{ const el=document.querySelector('.sc-chrono'); if(!el){ clearInterval(window._anChrono); return; } const d=Math.max(0,Math.round((Date.now()-Date.parse(el.dataset.depuis))/1000)); el.textContent=Math.floor(d/60)+':'+String(d%60).padStart(2,'0'); const E=(STRAT||{}).encours, b=document.querySelector('.sc-barre i'); if(E&&b){ const v=anPct(E); b.style.width=v+'%'; b.parentNode.setAttribute('aria-valuenow',v); } },1000);
  const sm=document.getElementById('st-maj'); if(sm) sm.onclick=()=>{ const C=(STRAT||{}).courante, act=C&&C.active&&Date.now()<Date.parse(C.active.fin); if(confirm((act?A3('Attention : la stratégie actuelle est ACTIVE (mesure en cours). Une nouvelle stratégie la remplacera et il faudra l\'activer à nouveau.\n\n','Warning: the current strategy is ACTIVE (measurement in progress). A new strategy will replace it and will need to be activated again.\n\n'):'')+A3('Lancer les agents ? Ils travaillent quelques minutes sur les chiffres de cette page.','Start the agents? They work for a few minutes on the figures of this page.'))) anStratLance('strategie'); };
  const sr=document.getElementById('st-rap'); if(sr) sr.onclick=()=>{ if(confirm(A3('Préparer le rapport du mois ? Les agents comparent les chiffres du jour de la stratégie à ceux d\'aujourd\'hui.','Prepare the monthly report? The agents compare the figures from the day of the strategy with today\'s.'))) anStratLance('rapport'); };
  z.querySelectorAll('[data-stf]').forEach(b=>b.onclick=()=>{ const f=b.dataset.f==='1'; if(!f&&!confirm(A3('Remettre cette action « à faire » ?','Set this action back to “to do”?'))) return; anStratFait(+b.dataset.stf,f); });
  const se=document.getElementById('sel-env'); if(se) se.onclick=()=>{ const A=window._anXL; if(A&&confirm(A3(`Ne garder en pub que les ${A.garder.length} parfums gagnants ?\n\nLes ${A.sortir.length} qui font perdre de l'argent et les ${A.stock.length} plus en stock sortent de la pub payante (ils restent en vente sur le site). C'est noté au journal.`,`Keep only the ${A.garder.length} winning perfumes in the ads?\n\nThe ${A.sortir.length} losing money and the ${A.stock.length} out of stock leave the paid ads (they stay for sale on the website). It is written in the log.`))) anSelEnvoie(); };
  const jo=document.getElementById('jp-ok'); if(jo) jo.onclick=anJPAjoute;
  const jq=document.getElementById('jp-quoi'); if(jq) jq.onkeydown=e=>{ if(e.key==='Enter') anJPAjoute(); };
  const jm=document.getElementById('jp-plus'); if(jm) jm.onclick=()=>{ AN.jpn=(AN.jpn||15)+30; gaAnime=false; anDessine(); };
  const sa=document.getElementById('st-active'); if(sa) sa.onclick=()=>{ if(confirm(A3('Activer la stratégie ? Les 30 jours de mesure commencent maintenant.','Activate the strategy? The 30-day measurement starts now.'))) anStratActive(); };
  const re=()=>{ gaAnime=true; anSauve(); anDessine(); };
  z.querySelectorAll('[data-an]').forEach(b=>b.onclick=()=>{ AN.sel=b.dataset.an; re(); });
  z.querySelectorAll('[data-ans]').forEach(b=>b.onclick=()=>{ AN.site=b.dataset.ans; re(); });
  z.querySelectorAll('[data-anm]').forEach(b=>b.onclick=()=>{ AN.met=b.dataset.anm; re(); });
  z.querySelectorAll('[data-ansrc]').forEach(b=>b.onclick=()=>{ AN.src=b.dataset.ansrc; re(); });
}
let _anLarg=0; window.addEventListener('resize',()=>{ const w=innerWidth; if(Math.abs(w-_anLarg)<40) return; _anLarg=w; clearTimeout(window._anRz); window._anRz=setTimeout(()=>{ if(document.getElementById('ga-c1')) anDessine(); },200); });
/* ============ LA STRATÉGIE ET LE RAPPORT DU MOIS (9 nov. 2026) ============
   Igal : « une partie stratégie… vérifiée par plusieurs agents… en appuyant sur un bouton », « un rapport au bout d'un mois…
   une vraie explication de professionnel ». La page prépare un DOSSIER avec les chiffres qu'elle calcule déjà (toujours sur les
   30 derniers jours et les 30 d'avant, quelle que soit la période affichée), l'envoie au cockpit, qui le fait travailler par ses
   agents (strategie.js) ; le résultat revient dans le magasin strategie-v1 (administrateurs seulement) et s'affiche ici. */
let STRAT={}; try{ STRAT=JSON.parse(localStorage.getItem('strategie-v1')||'{}')||{}; }catch(e){ STRAT={}; }
const r0=v=>Math.round((+v||0)*100)/100;
function anDossier(L,tous){
  const auj=rcISO(new Date()), j=n=>rcISO(new Date(Date.now()-n*86400e3));
  const P={a:j(29),b:auj}, Q={a:j(59),b:j(30)};
  const fen=(X)=>{ const R=rcAgrege(L,X.a,X.b); const C=anDans(tous,X.a,X.b), G=anParFam(C), S=anSomme(C), pub=anPub(X.a,X.b).T;
    const ads=C.filter(o=>o.site==='site'&&o.fam==='gads'), mgA=ads.reduce((a,o)=>a+o.mg,0), caA=ads.reduce((a,o)=>a+o.ca,0);
    return { du:X.a, au:X.b,
      tous_canaux:{ca:r0(R.T.ca),marge_nette:r0(R.T.mg),ventes:R.T.n,flacons:R.T.q},
      par_canal:Object.values(R.G).map(o=>({canal:o.canal,ca:r0(o.ca),marge_nette:o.hist?null:r0(o.mg),ventes:o.n,perfume_city:rcId(o.canal)==='pc'?Object.fromEntries(Object.entries(o.ou||{}).map(([k,v])=>[k||'?',r0(v.ca)])):undefined})),
      sites_en_ligne:{commandes:S.n,ca:r0(S.ca),marge_nette:r0(S.mg),par_site:Object.fromEntries(AN_SITES.map(x=>{ const Y=C.filter(o=>o.site===x.id); return [anSiteNom(x.id),{commandes:Y.filter(o=>!o.ret).length,ca:r0(Y.reduce((a,o)=>a+o.ca,0))}]; })),
        par_origine:Object.fromEntries(Object.entries(G).map(([k,g])=>[anNomGr(k),{commandes:g.n,ca:r0(g.ca),detail:g.det}]))},
      google_ads:{pub_depensee:r0(pub.pub),ventes_selon_google:r0(pub.ventes),clics:pub.clics,commandes_reelles_venues_de_la_pub:ads.filter(o=>!o.ret).length,ca_reel_de_la_pub:r0(caA),marge_nette_de_ces_commandes:r0(mgA),reste_apres_pub:r0(mgA-pub.pub)},
      google_shopping_gratuit:{clics:pub.gClics,affichages:pub.gAff} }; };
  const A=anAnalysePub(tous);
  const G=anPubJ(), mois={}; Object.keys(G.j||{}).forEach(d=>{ const m=d.slice(0,7), r=G.j[d]||[]; const o=mois[m]=mois[m]||{pub:0,ventes_google:0}; o.pub+=+r[0]||0; o.ventes_google+=+r[1]||0; });
  Object.values(mois).forEach(o=>{ o.pub=r0(o.pub); o.ventes_google=r0(o.ventes_google); });
  const att=((ORI['_attente_woocommerce']||{}).L||[]).filter(x=>x.o==='gads');
  return { date:auj, devise:'USD',
    trente_derniers_jours:fen(P), trente_jours_d_avant:(Q.a>=RC_COMPLET?fen(Q):'incomplet (avant le 1er octobre 2026)'),
    pub_google_par_mois:mois,
    campagnes_google_ads:anCampDossier(tous),
    pub_parfum_par_parfum_90j:A?{pub_par_mois:r0(A.pub90/3),gain_par_mois_si_on_sort_les_perdants:r0(A.gain90/3),a_garder:{nombre:A.garder.length,pub_par_mois:r0(A.garder.reduce((a,o)=>a+o.pub,0)/3)},a_sortir_perdent:{nombre:A.sortir.length,pub_par_mois:r0(A.sortir.reduce((a,o)=>a+o.pub,0)/3)},a_sortir_plus_en_stock:{nombre:A.stock.length,pub_par_mois:r0(A.stock.reduce((a,o)=>a+o.pub,0)/3)},a_verifier:A.verif.length,
      les_10_qui_perdent_le_plus:A.sortir.concat(A.stock).sort((a,b)=>(a.res??-a.pub)-(b.res??-b.pub)).slice(0,10).map(o=>({parfum:(o.marque?o.marque+' ':'')+(o.nom||o.sku),pub_90j:r0(o.pub),resultat_90j:r0(o.res??-o.pub)})),
      les_10_qui_rapportent_le_plus:A.garder.slice().sort((a,b)=>b.res-a.res).slice(0,10).map(o=>({parfum:(o.marque?o.marque+' ':'')+(o.nom||o.sku),pub_90j:r0(o.pub),resultat_90j:r0(o.res)}))}:'pas encore lu',
    commandes_de_la_pub_payees_pas_encore_expediees:{nombre:att.length,montant:r0(att.reduce((a,x)=>a+(+x.mt||0),0))},
    outils_en_place:['WooCommerce (perfumestrade.com, wholesale)','Shopify (Perfume City)','Google Ads (campagnes créées par un prestataire, reprises par Sam en novembre 2026 : voir campagnes_google_ads)','Google for WooCommerce (2 837 produits envoyés à Google)','Klaviyo (emails)','WhatsApp (envoi des nouveaux arrivages aux clients favoris)','Amazon','Lightspeed (caisse)'],
    donnees_manquantes:['Search Console non branchée : on ne connaît ni les recherches Google qui mènent au site, ni ses positions','nombre de visiteurs des sites non mesuré : pas de taux de conversion','historique des ventes du site avant octobre 2026 hors de l\'ERP (seulement la pub Google, par mois)'] };
}
/* L'ATTENTE (11 nov. 2026). Igal : « plus de vidéo », une barre de progression à la place. Pendant que les agents travaillent
   (sur le cockpit, une à dix minutes), on voit : les trois étapes, celle en cours, une barre qui avance, le chrono.
   La barre : chaque étape vaut un tiers ; à l'intérieur d'une étape elle avance avec le temps écoulé depuis le début de
   l'étape (E.maj, posé par le cockpit), sans jamais dépasser 90 % de l'étape tant que le serveur n'a pas annoncé la suivante. */
const AN_DUREE=[240,240,240];   /* durée habituelle d'une étape, en secondes */
function anPhase(E){
  const rap=E.type==='rapport', e=String(E.etape||'');
  return rap?(/contr[ôo]leur/i.test(e)?1:/r[ée]dacteur/i.test(e)?2:0):(/v[ée]rificateur/i.test(e)?1:/r[ée]dacteur/i.test(e)?2:0);
}
function anPct(E){
  const ph=anPhase(E), t0=Date.parse(E.maj||E.depuis)||Date.now();
  const dans=Math.min(.9,Math.max(0,(Date.now()-t0)/1000/AN_DUREE[ph]));
  return Math.round((ph+dans)/3*100);
}
function anScene(E){
  const rap=E.type==='rapport', ph=anPhase(E);
  const etapes=rap?[A3('L\'analyste compare avant / après','The analyst compares before / after'),A3('Le contrôleur vérifie chaque chiffre','The controller checks every figure'),A3('Le rédacteur écrit le rapport','The editor writes the report')]
    :[A3('Le stratège propose','The strategist proposes'),A3('Trois vérificateurs relisent','Three checkers review'),A3('Le rédacteur écrit','The editor writes')];
  const depuis=Math.max(0,Math.round((Date.now()-Date.parse(E.depuis))/1000));
  return `<div class="sc"><div class="sc-haut"><span class="sc-live"><i></i>${rap?A3('Rapport du mois en préparation','Monthly report in progress'):A3('Stratégie en préparation','Strategy in progress')}</span><span data-nolang class="sc-chrono" data-depuis="${esc(E.depuis)}">${Math.floor(depuis/60)}:${String(depuis%60).padStart(2,'0')}</span></div>
    <div class="sc-barre" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="${anPct(E)}"><i style="width:${anPct(E)}%"></i></div>
    <ol class="sc-etapes">${etapes.map((t,i)=>`<li class="${i<ph?'ok':i===ph?'on':''}">${esc(t)}</li>`).join('')}</ol>
    <p class="sc-note">${A3('Vous pouvez changer de page : l\'analyse continue sur le serveur, le point bleu du menu clignote jusqu\'à la fin.','You can change page: the analysis keeps going on the server, the blue dot in the menu blinks until it ends.')}</p></div>`;
}
/* la décision est prise : la barre pleine quelques secondes, puis le résultat */
function anSceneFin(rap){
  return `<div class="sc sc-fin"><div class="sc-barre"><i style="width:100%"></i></div><div class="sc-accord"><b>✓</b><span>${rap?A3('Le rapport est prêt','The report is ready'):A3('Décision prise : la stratégie est prête','Decision made: the strategy is ready')}</span></div></div>`;
}
async function anStratLance(type){
  const st=document.getElementById('st-msg');
  try{ const d=anDossier(rcLignes(),anCommandes(rcLignes()));
    const r=await fetch(CK_URL+'/api/o/'+CK_ORG+'/strategie/lance',{method:'POST',headers:{'Content-Type':'application/json',Authorization:'Bearer '+ckTok()},body:JSON.stringify({type,dossier:d})});
    const j=await r.json().catch(()=>({}));
    if(!r.ok){ if(st) st.textContent=j.erreur||('erreur '+r.status); return; }
    STRAT.encours={type,etape:A3('départ','starting'),depuis:new Date().toISOString()}; gaAnime=true; anDessine();
  }catch(e){ if(st) st.textContent=A3('Le cockpit ne répond pas : ','The cockpit is not answering: ')+(e&&e.message||e); }
}
/* 11 nov. 2026 : plus de case « Fait » à cocher. L'ERP constate lui-même (Google Ads, réglages) ; seule une action « manuelle »
   a un bouton « C'est fait », qui note le jour, l'heure et le nom. */
async function anStratFait(i,fait){
  try{ const r=await fetch(CK_URL+'/api/o/'+CK_ORG+'/strategie/action',{method:'POST',headers:{'Content-Type':'application/json',Authorization:'Bearer '+ckTok()},body:JSON.stringify({i,fait})});
    if(r.ok&&STRAT.courante&&STRAT.courante.faits){ const s=session()||{}; STRAT.courante.faits[i]=fait?{date:new Date().toISOString(),par:s.nom||'',comment:'déclaré fait'}:null; anDessine(); } }catch(e){}
}
async function anStratActive(){
  const st=document.getElementById('st-msg');
  try{ const r=await fetch(CK_URL+'/api/o/'+CK_ORG+'/strategie/active',{method:'POST',headers:{'Content-Type':'application/json',Authorization:'Bearer '+ckTok()},body:'{}'});
    const j=await r.json().catch(()=>({}));
    if(!r.ok){ if(st) st.textContent=j.erreur||('erreur '+r.status); return; }
    if(STRAT.courante){ const s=session()||{}; STRAT.courante.active={date:j.date,fin:j.fin,par:s.nom||''}; }
    gaAnime=true; anDessine();
  }catch(e){ if(st) st.textContent=A3('Le cockpit ne répond pas : ','The cockpit is not answering: ')+(e&&e.message||e); }
}
/* « fait le 12 novembre 2026 à 14:32 » */
const anQuand=iso=>{ try{ const d=new Date(iso); return A3('le ','on ')+d.toLocaleDateString(A3('fr-FR','en-US'),{day:'numeric',month:'long',year:'numeric'})+A3(' à ',' at ')+d.toLocaleTimeString(A3('fr-FR','en-US'),{hour:'2-digit',minute:'2-digit'}); }catch(e){ return ''; } };
/* LES RÉSULTATS DEPUIS L'ACTIVATION (11 nov. 2026, « résultats sur 30 jours ») : les jours écoulés depuis le clic, comparés aux
   mêmes nombre de jours juste avant — tous les sites, mêmes règles que le haut de la page (commandes payées, retours déduits). */
function anStratResultats(C,tous){
  const A=C.active; if(!A) return '';
  const d0=rcISO(new Date(A.date)), auj=rcISO(new Date());
  const n=Math.max(1,Math.min(30,Math.round((Date.parse(auj)-Date.parse(d0))/86400e3)+1));
  const av0=rcISO(new Date(Date.parse(d0+'T12:00:00')-n*86400e3)), av1=rcISO(new Date(Date.parse(d0+'T12:00:00')-86400e3));
  const ap=anSomme(anDans(tous,d0,auj)), av=anSomme(anDans(tous,av0,av1));
  const pa=anPub(d0,auj).T, pv=anPub(av0,av1).T;
  const lig=(lib,a,b,f,bon)=>{ const dv=b?((a-b)/Math.abs(b)*100):null; const cl=dv==null?'':((dv>=0)===bon?'st-up':'st-down');
    return `<tr><td>${lib}</td><td>${f(b)}</td><td><b>${f(a)}</b></td><td class="${cl}">${dv==null?'—':(dv>=0?'+':'')+Math.round(dv)+' %'}</td></tr>`; };
  return `<div class="st-res"><b>${A3(`Résultats depuis l'activation — jour ${n} sur 30`,`Results since activation — day ${n} of 30`)}</b>
    <table><thead><tr><th></th><th>${A3(`${n} jours avant`,`${n} days before`)}</th><th>${A3('Depuis l\'activation','Since activation')}</th><th>${A3('Écart','Change')}</th></tr></thead><tbody>
    ${lig(A3('Commandes en ligne','Online orders'),ap.n,av.n,nf,true)}${lig(A3('Chiffre d\'affaires en ligne','Online revenue'),ap.ca,av.ca,money,true)}${lig(A3('Marge nette en ligne','Online net margin'),ap.mg,av.mg,money,true)}
    ${lig(A3('Dépense Google Ads','Google Ads spend'),pa.pub,pv.pub,money,false)}${lig(A3('Marge après pub','Margin after ads'),ap.mg-pa.pub,av.mg-pv.pub,money,true)}</tbody></table>
    <p class="ga-note">${A3('Les chiffres de chaque jour s\'ajoutent tout seuls jusqu\'au 30e jour ; ensuite, le « Rapport du mois » explique ce qui vient de la stratégie et ce qui vient d\'ailleurs.','Each day\'s figures add up on their own until day 30; then the “Monthly report” explains what comes from the strategy and what comes from elsewhere.')}</p></div>`;
}
const anLg=()=>LANG==='fr'?'fr':'en';
const anDate=s=>{ try{ return new Date(s).toLocaleDateString(A3('fr-FR','en-US'),{day:'numeric',month:'long',year:'numeric'}); }catch(e){ return String(s||'').slice(0,10); } };
const anLi=a=>(Array.isArray(a)&&a.length)?'<ul>'+a.map(x=>`<li>${esc(x)}</li>`).join('')+'</ul>':'';
function anStrategie(L,tous){
  const S=STRAT||{}, C=S.courante, E=S.encours, R=(S.rapports||[])[0];
  let h=`<section class="ga-card ga-pad st"><div class="ga-h"><h3>${A3('Stratégie','Strategy')}</h3><span class="ga-src">${A3('proposée et vérifiée par cinq agents','proposed and checked by five agents')}</span></div>`;
  h+=`<p class="st-com">${A3('Un stratège propose 3 actions au plus, appuyées sur les chiffres de cette page. Trois vérificateurs indépendants les relisent — les chiffres, la marge, la faisabilité — et une action refusée par un seul d\'entre eux est retirée. Un rédacteur écrit la version finale. Au bout d\'un mois, le « Rapport du mois » compare avant / après, action par action.','A strategist proposes up to 3 actions, based on the figures on this page. Three independent checkers review them — the figures, the margin, the feasibility — and an action refused by any one of them is dropped. An editor writes the final version. After a month, the “Monthly report” compares before / after, action by action.')}</p>`;
  const enCours=E&&!E.err&&(Date.now()-Date.parse(E.maj||E.depuis))<30*60e3;
  if(enCours){ h+=anScene(E); window._anEnCours=E.type; }
  else if(window._anEnCours&&!(E&&E.err)){ const t=window._anEnCours; window._anEnCours=null; window._anFin=Date.now(); window._anFinType=t; setTimeout(()=>{ gaAnime=true; anDessine(); },6500); }
  if(!enCours&&window._anFin&&Date.now()-window._anFin<6000) h+=anSceneFin(window._anFinType==='rapport');
  /* 9 nov. 2026 : une analyse restée plus d'une demi-heure sans nouvelle étape, ni fin ni erreur (cockpit redémarré, modèle muet) : on le dit, au lieu de rien */
  if(!enCours&&E&&!E.err&&E.depuis) h+=`<div class="an-alerte">${A3(`L'analyse lancée à ${new Date(E.depuis).toLocaleTimeString('fr-FR',{hour:'2-digit',minute:'2-digit'})} s'est arrêtée en route (étape : « ${esc(E.etape||'')} »). Relancez-la avec le bouton ci-dessous.`,`The analysis started at ${new Date(E.depuis).toLocaleTimeString('en-US',{hour:'numeric',minute:'2-digit'})} stopped on the way. Start it again with the button below.`)}</div>`;
  if(!enCours&&E&&E.err) h+=`<div class="an-alerte">${A3('La dernière analyse n\'a pas abouti : ','The last analysis did not finish: ')}<span data-nolang>${esc(E.err)}</span></div>`;
  const age=C?Math.floor((Date.now()-Date.parse(C.date))/86400e3):0;
  h+=`<div class="ga-actions"><button type="button" class="ga-btn" id="st-maj" ${enCours?'disabled':''}>${C?A3('Mettre à jour la stratégie','Update the strategy'):A3('Établir la stratégie','Build the strategy')}</button>`
    +(C?`<button type="button" class="ga-btn sec" id="st-rap" ${enCours?'disabled':''}>${A3('Rapport du mois','Monthly report')}</button><span>${age<28?A3(`Le rapport est plus parlant après 4 semaines (dans ${28-age} jour${28-age>1?'s':''}).`,`The report means more after 4 weeks (in ${28-age} day${28-age>1?'s':''}).`):A3('La stratégie a plus de 4 semaines : c\'est le moment du rapport.','The strategy is over 4 weeks old: time for the report.')}</span>`:'')
    +`<span id="st-msg" class="st-msg"></span></div>`;
  if(C&&C.res){ const X=C.res[anLg()]||C.res.fr||{};
    h+=`<div class="st-bloc"><div class="st-t">${esc(X.titre||A3('Stratégie','Strategy'))} <small>${A3('du','of')} ${esc(anDate(C.date))}</small></div>${X.diagnostic?`<p class="st-diag">${esc(X.diagnostic)}</p>`:''}
      ${X.objectif?`<p class="st-obj"><span>${A3('Objectif du mois','Goal for the month')}</span>${esc(X.objectif)}</p>`:''}
      ${C.active?`<p class="st-on"><i></i>${A3('Stratégie active','Strategy active')} ${esc(anQuand(C.active.date))} · ${A3('mesure jusqu\'au','measured until')} ${esc(anDate(C.active.fin))}</p>`
        :`<div class="st-act"><button type="button" class="ga-btn" id="st-active" ${enCours?'disabled':''}>${A3('Activer la stratégie','Activate the strategy')}</button><span>${A3('Le clic ouvre les 30 jours de mesure. Ensuite l\'ERP note seul chaque action faite, avec le jour et l\'heure.','The click opens the 30-day measurement. Then the ERP records each action done by itself, with the day and time.')}</span></div>`}
      <ol class="st-acts">${(X.actions||[]).map((a,i)=>{ const f=(C.faits||[])[i], fa=(C.res.fr&&C.res.fr.actions||[])[i]||a, v=(fa.verif||{}).type||'manuel', qui=fa.qui||a.qui||'';
        const etat=f?`<span class="st-fait">✓ ${A3('Fait','Done')} ${f.date?esc(anQuand(f.date)):''}${f.par&&f.par!=='ERP'?' · '+esc(f.par):''}${f.comment&&f.par==='ERP'?`<small data-nolang>${esc(f.comment)}</small>`:''}</span>${f.par!=='ERP'&&C.active?`<button type="button" class="st-annule" data-stf="${i}" data-f="0">${A3('annuler','undo')}</button>`:''}`
          :!C.active?`<span class="st-afaire">${A3('À faire après l\'activation','To do after activation')}</span>`
          :v==='manuel'?`<span class="st-afaire">${A3('À faire','To do')}</span><button type="button" class="ga-btn sec st-cfait" data-stf="${i}" data-f="1">${A3('C\'est fait','It\'s done')}</button>`
          :`<span class="st-afaire">${v==='campagne'?A3('À faire — l\'ERP le verra seul dans Google Ads','To do — the ERP will see it in Google Ads by itself'):A3('À faire — l\'ERP le verra seul dans les Réglages','To do — the ERP will see it in Settings by itself')}</span>`;
        return `<li class="${f?'fait':''}"><div class="st-ah"><b>${esc(a.titre||'')}</b>${qui?`<span class="st-qui" data-nolang>${esc(qui)}</span>`:''}</div><div class="st-etat">${etat}</div>
        ${a.pourquoi?`<p><span>${A3('Pourquoi','Why')}</span>${esc(a.pourquoi)}</p>`:''}${(a.comment||[]).length?`<div><span>${A3('Comment','How')}</span>${anLi(a.comment)}</div>`:''}
        <div class="st-kv">${a.cout?`<div><span>${A3('Coût','Cost')}</span>${esc(a.cout)}</div>`:''}${a.gain?`<div><span>${A3('Gain attendu','Expected gain')}</span>${esc(a.gain)}</div>`:''}${a.mesure?`<div><span>${A3('Ce qu\'on mesurera dans un mois','What we will measure in a month')}</span>${esc(a.mesure)}</div>`:''}${a.delai?`<div><span>${A3('Délai','Timing')}</span>${esc(a.delai)}</div>`:''}</div></li>`; }).join('')}</ol>${anStratResultats(C,tous)}`;
    const pv=X.previsions||{};
    if(pv.ca||pv.marge) h+=`<div class="st-prev"><b>${A3('Les 30 prochains jours, en fourchette','The next 30 days, as a range')}</b><table><thead><tr><th></th><th>${A3('Prudent','Cautious')}</th><th>${A3('Probable','Likely')}</th><th>${A3('Haut','High')}</th></tr></thead><tbody>
      ${pv.ca?`<tr><td>${A3("Chiffre d'affaires",'Revenue')}</td><td>${money(pv.ca.prudent)}</td><td><b>${money(pv.ca.probable)}</b></td><td>${money(pv.ca.haut)}</td></tr>`:''}${pv.marge?`<tr><td>${A3('Marge après pub','Margin after ads')}</td><td>${money(pv.marge.prudent)}</td><td><b>${money(pv.marge.probable)}</b></td><td>${money(pv.marge.haut)}</td></tr>`:''}</tbody></table>${pv.texte?`<p>${esc(pv.texte)}</p>`:''}</div>`;
    if((X.retire||[]).length||(X.manques||[]).length) h+=`<details class="ga-calc"><summary>${A3('Ce que les vérificateurs ont retiré, et ce qui manque','What the checkers removed, and what is missing')}</summary>${(X.retire||[]).length?`<p class="ga-note"><b>${A3('Retiré','Removed')}</b></p>${anLi(X.retire)}`:''}${(X.manques||[]).length?`<p class="ga-note"><b>${A3('Données manquantes','Missing data')}</b></p>${anLi(X.manques)}`:''}</details>`;
    h+=`</div>`; }
  else if(!enCours) h+=`<p class="ga-vide">${A3('Pas encore de stratégie : clique sur « Établir la stratégie ».','No strategy yet: click “Build the strategy”.')}</p>`;
  if(R&&R.res){ const Y=R.res[anLg()]||R.res.fr||{};
    h+=`<div class="st-bloc st-rapport"><div class="st-t">${esc(Y.titre||A3('Rapport du mois','Monthly report'))} <small>${A3('du','of')} ${esc(anDate(R.date))}</small></div>${Y.bilan?`<p class="st-diag">${esc(Y.bilan)}</p>`:''}${Y.prevision_verifiee?`<p><span class="st-l">${A3('La prévision','The forecast')}</span>${esc(Y.prevision_verifiee)}</p>`:''}
      ${(Y.actions||[]).map(a=>`<div class="st-ra"><div class="st-ah"><b>${esc(a.titre||'')}</b><span class="st-v">${esc(a.verdict||'')}</span></div>${(a.avant||a.apres)?`<p class="st-av">${esc(a.avant||'')} → <b>${esc(a.apres||'')}</b></p>`:''}${a.explication?`<p>${esc(a.explication)}</p>`:''}</div>`).join('')}
      <div class="st-kv">${(Y.garder||[]).length?`<div><span>${A3('À garder','Keep')}</span>${anLi(Y.garder)}</div>`:''}${(Y.arreter||[]).length?`<div><span>${A3('À arrêter','Stop')}</span>${anLi(Y.arreter)}</div>`:''}${(Y.essayer||[]).length?`<div><span>${A3('À essayer ensuite','Try next')}</span>${anLi(Y.essayer)}</div>`:''}</div>
      ${Y.prudence?`<p class="ga-prud">${esc(Y.prudence)}</p>`:''}</div>`;
    if((S.rapports||[]).length>1) h+=`<details class="ga-calc"><summary>${A3('Rapports précédents','Previous reports')}</summary>${S.rapports.slice(1).map(x=>{ const Z=(x.res&&(x.res[anLg()]||x.res.fr))||{}; return `<p class="ga-note"><b>${esc(anDate(x.date))}</b> — ${esc(Z.bilan||'')}</p>`; }).join('')}</details>`; }
  return h+`</section>`;
}
/* ============ LES CAMPAGNES GOOGLE ADS, EN DIRECT (10 nov. 2026) ============
   Igal : « que je puisse récupérer toutes les infos en live pour l'analytique de l'ERP ». Un script posé dans le compte Google Ads
   envoie ses chiffres au cockpit toutes les heures (google-ads-v1 ; voir googleads.js dans le cockpit). Ici, chaque campagne :
   active ou en pause, budget par jour, objectif de rentabilité, ce qu'elle a coûté et ce que Google lui attribue sur 30 et 7 jours.
     ventes pour 1 $ = ventes selon Google ÷ coût ;
     résultat estimé = ventes selon Google × (ventes réelles ÷ ventes selon Google) × taux de marge moyen des parfums de la pub − coût ;
     seuil = le « ventes pour 1 $ » en dessous duquel la campagne perd de l'argent (même calcul, à l'envers).
   Le taux de marge et la correction « ventes réelles » viennent de l'analyse parfum par parfum (mêmes chiffres, mêmes règles). */
function anCampCalc(tous){
  const A=anAdsJ(); if(!A||!Array.isArray(A.c)) return null;
  const X=(()=>{ try{ return anAnalysePub(tous); }catch(e){ return null; } })();
  let taux=0.3, k=0.8;
  if(X){ k=X.k; const Lt=X.L.filter(o=>o.taux!=null&&o.vg>0), sv=Lt.reduce((a,o)=>a+o.vg,0); if(sv>0) taux=Math.max(0.05,Lt.reduce((a,o)=>a+o.vg*o.taux,0)/sv); }
  const seuil=1/(k*taux);
  const C=A.c.map(c=>{ const m=c.m30||[0,0,0,0,0], s=c.m7||[0,0,0,0,0];
    return {id:c.id,n:c.n,on:c.etat==='ENABLED',type:c.type,budget:c.budget,troas:c.troas,cout:+m[0]||0,vg:+m[1]||0,conv:+m[2]||0,cout7:+s[0]||0,vg7:+s[1]||0,
      roas:(+m[0]>0)?(+m[1]||0)/(+m[0]):null,res:(+m[1]||0)*k*taux-(+m[0]||0)}; });
  C.sort((a,b)=>(b.on-a.on)||(b.cout-a.cout));
  return {A,C,taux,k,seuil};
}
function anCampDossier(tous){ const R=anCampCalc(tous); if(!R) return 'pas encore branché';
  return {recu:R.A.maj,seuil_ventes_pour_1_dollar:Math.round(R.seuil*100)/100,
    campagnes:R.C.filter(c=>c.on||c.cout>0).map(c=>({nom:c.n,etat:c.on?'active':'en pause',type:c.type,budget_par_jour:c.budget,objectif_ventes_pour_1_dollar:c.troas,cout_30j:Math.round(c.cout),ventes_selon_google_30j:Math.round(c.vg),ventes_pour_1_dollar:c.roas!=null?Math.round(c.roas*100)/100:null,resultat_estime_30j:Math.round(c.res),cout_7j:Math.round(c.cout7)})),
    autres_campagnes_en_pause_sans_depense:R.C.filter(c=>!c.on&&!c.cout).length}; }
/* ============ LA SÉLECTION PUB (11 nov. 2026) ============
   Igal : « supprimer les produits qu'on n'a pas en stock, ceux qui nous font perdre de l'argent, et se concentrer sur ceux qui nous
   font gagner ». Rien n'est supprimé du site ni de Google Shopping gratuit : la décision de chaque parfum part chez Google comme
   étiquette (custom_label_4 : pt_garder, pt_sortir, pt_sans_stock, pt_a_verifier) par un flux que Merchant Center relit chaque jour ;
   la campagne, réglée sur « pt_garder », ne paie plus que pour les gagnants. L'envoi est la première ligne du journal. */
const anEtiq=()=>{ try{ return JSON.parse(localStorage.getItem('gads-etiquettes-v1')||'null'); }catch(e){ return null; } };
function anSelection(A){
  const E=anEtiq();
  let h=`<div class="sel-pub"><div><b>${A3(`Ne garder en pub que les ${nf(A.garder.length)} gagnants`,`Keep only the ${nf(A.garder.length)} winners in the ads`)}</b>
    <p>${A3(`${nf(A.sortir.length)} parfums qui font perdre de l'argent et ${nf(A.stock.length)} plus en stock sortent de la pub payante. Ils restent en vente sur le site et dans Google Shopping gratuit.`,`${nf(A.sortir.length)} perfumes losing money and ${nf(A.stock.length)} out of stock leave the paid ads. They stay for sale on the website and in free Google Shopping.`)}</p>`;
  if(E&&E.maj) h+=`<p class="sel-ok">✓ ${A3('Envoyé','Sent')} ${esc(anQuand(E.maj))}${E.par?' · '+esc(E.par):''} — ${nf((E.n||{}).garder||0)} ${A3('gagnants gardés','winners kept')}</p>`;
  return h+`</div><button type="button" class="ga-btn" id="sel-env">${E&&E.maj?A3('Renvoyer la sélection à jour','Send the updated selection'):A3('Ne garder en pub que les gagnants','Keep only the winners in the ads')}</button><span id="sel-msg" class="st-msg"></span></div>`;
}
async function anSelEnvoie(){
  const A=window._anXL, m=document.getElementById('sel-msg'); if(!A) return;
  const L=A.L.filter(o=>o.sku).map(o=>[o.sku,o.dec]);
  try{ const r=await fetch(CK_URL+'/api/o/'+CK_ORG+'/google/etiquettes',{method:'POST',headers:{'Content-Type':'application/json',Authorization:'Bearer '+ckTok()},body:JSON.stringify({L})});
    const j=await r.json().catch(()=>({}));
    if(!r.ok){ if(m) m.textContent=j.erreur||('erreur '+r.status); return; }
    const s=session()||{}; try{ localStorage.setItem('gads-etiquettes-v1',JSON.stringify({maj:new Date().toISOString(),par:s.nom||'',n:j.n})); }catch(e){}
    window._anFlux=j.flux||''; gaAnime=false; anDessine();
  }catch(e){ if(m) m.textContent=A3('Le cockpit ne répond pas : ','The cockpit is not answering: ')+(e&&e.message||e); }
}
/* ============ LE JOURNAL (11 nov. 2026) ============
   Igal : « un journal avec les horaires, sur l'analytique, des actions qui ont été faites ». Il se remplit tout seul (journalpub.js
   dans le cockpit) : l'ERP, la stratégie, et l'historique des modifications de Google Ads lu par le script ; plus un repère à la main.
   Chaque jour qui a un événement porte un petit repère sur la courbe du haut. Heures de Miami. */
const anJP=()=>{ try{ const J=JSON.parse(localStorage.getItem('journal-pub-v1')||'null'); return (J&&Array.isArray(J.L))?J.L:[]; }catch(e){ return []; } };
const AN_SRC={erp:['ERP','ERP'],gads:['Google Ads','Google Ads'],strategie:['Stratégie','Strategy'],main:['Repère','Note']};
const anHeure=iso=>{ try{ return new Date(iso).toLocaleString(A3('fr-FR','en-US'),{timeZone:'America/New_York',day:'numeric',month:'short',year:'numeric',hour:'2-digit',minute:'2-digit'}); }catch(e){ return String(iso||''); } };
const anJourMiami=iso=>{ try{ return new Date(iso).toLocaleDateString('en-CA',{timeZone:'America/New_York'}); }catch(e){ return String(iso||'').slice(0,10); } };
function anJournal(){
  const L=anJP(), A=anAdsJ(), n=Math.max(15,AN.jpn||15);
  let h=`<section class="ga-card ga-pad" id="jp"><div class="ga-h"><h3>${A3('Journal des actions','Action log')}</h3><span class="ga-src">${A3('se remplit tout seul : ERP, stratégie, Google Ads · heures de Miami','fills itself: ERP, strategy, Google Ads · Miami time')}</span></div>`;
  if(A&&(+A.v||1)<2) h+=`<p class="gc-alerte">${A3('Pour voir ici les changements faits dans Google Ads (budget, campagne activée ou en pause…), le script du compte Google Ads doit être remplacé par sa version 2 : section « Les campagnes Google Ads » › « Afficher le script ».','To see here the changes made in Google Ads (budget, campaign on or paused…), the script in the Google Ads account must be replaced by version 2: section “Google Ads campaigns” › “Show the script”.')}</p>`;
  h+=`<div class="jp-ajout"><input type="text" id="jp-quoi" maxlength="200" placeholder="${esc(A3('Ajouter un repère : « Sam lance une promo WhatsApp »…','Add a note: “Sam starts a WhatsApp promo”…'))}"><button type="button" class="ga-btn sec" id="jp-ok">${A3('Ajouter','Add')}</button><span id="jp-msg" class="st-msg"></span></div>`;
  if(!L.length) return h+`<p class="ga-vide">${A3('Rien encore : la première action notée sera l\'envoi de la sélection pub.','Nothing yet: the first action recorded will be sending the ads selection.')}</p></section>`;
  h+=`<ol class="jp-l">${L.slice(0,n).map(e=>`<li class="jp-${esc(e.src)}"><span class="jp-t" data-nolang>${esc(anHeure(e.t))}</span><span class="jp-s">${A3(...(AN_SRC[e.src]||AN_SRC.erp))}</span><div class="jp-q"><b data-nolang>${esc(e.quoi)}</b>${e.detail?`<small data-nolang>${esc(e.detail)}</small>`:''}</div><span class="jp-p" data-nolang>${esc(e.par||'')}</span></li>`).join('')}</ol>`;
  if(L.length>n) h+=`<button type="button" class="ga-btn sec" id="jp-plus">${A3(`Voir plus (${nf(L.length-n)})`,`Show more (${nf(L.length-n)})`)}</button>`;
  return h+`</section>`;
}
async function anJPAjoute(){
  const i=document.getElementById('jp-quoi'), m=document.getElementById('jp-msg'); const q=(i&&i.value||'').trim(); if(!q) return;
  try{ const r=await fetch(CK_URL+'/api/o/'+CK_ORG+'/journal-pub',{method:'POST',headers:{'Content-Type':'application/json',Authorization:'Bearer '+ckTok()},body:JSON.stringify({quoi:q})});
    const j=await r.json().catch(()=>({}));
    if(!r.ok){ if(m) m.textContent=j.erreur||('erreur '+r.status); return; }
    const s=session()||{}; let J={L:[]}; try{ J=JSON.parse(localStorage.getItem('journal-pub-v1')||'{"L":[]}')||{L:[]}; }catch(e){}
    J.L=[{t:new Date().toISOString(),src:'main',quoi:q,par:s.nom||''}].concat(J.L||[]); try{ localStorage.setItem('journal-pub-v1',JSON.stringify(J)); }catch(e){}
    gaAnime=false; anDessine();
  }catch(e){ if(m) m.textContent=A3('Le cockpit ne répond pas : ','The cockpit is not answering: ')+(e&&e.message||e); }
}
/* les repères de la courbe : pour chaque point (jour ou mois), les événements du journal qui y tombent */
function anReperes(B,P){
  const idx={}; B.K.forEach((k,i)=>idx[k.k]=i); const R={};
  anJP().forEach(e=>{ const d=anJourMiami(e.t); if(d<P.a||d>P.b) return; const i=idx[B.jour?d:d.slice(0,7)]; if(i==null) return; (R[i]=R[i]||[]).push(e); });
  return R;
}
/* ============ LES VISITES ET LES RECHERCHES GOOGLE (11 nov. 2026) ============
   Igal : « être relié en live tout le temps ». Le robot Google du cockpit (googlerobot.js, lecture seule) lit toutes les heures
   Google Analytics (visites de perfumestrade.com, d'où elles viennent, qui achète) et Search Console (ce que les gens tapent dans
   Google avant d'arriver). Rangé dans « google-sources-v1 ». Ici : les 30 derniers jours comparés aux 30 d'avant, jour pour jour. */
const anSrcG=()=>{ try{ return JSON.parse(localStorage.getItem('google-sources-v1')||'null'); }catch(e){ return null; } };
function anVisites(){
  const G=anSrcG();
  let h=`<section class="ga-card ga-pad" id="vis"><div class="ga-h"><h3>${A3('Les visites du site et les recherches Google','Website visits and Google searches')}</h3>`;
  if(!G) return h+`<span class="ga-src">${A3('pas encore branché','not connected yet')}</span></div><p class="gc-txt">${A3('Le robot Google (lecture seule) lira ici Google Analytics et Search Console toutes les heures, dès que sa clé sera déposée et qu\'il sera ajouté comme lecteur.','The Google robot (read only) will read Google Analytics and Search Console here every hour, as soon as its key is in place and it is added as a reader.')}</p></section>`;
  const A=G.ga||{}, S=G.sc||{};
  h+=`<span class="ga-src">${A3('en direct · Google Analytics et Search Console','live · Google Analytics and Search Console')} · ${A3('lu','read')} ${anDepuis(G.maj)}</span></div>`;
  if(A.err) h+=`<p class="gc-alerte">Google Analytics : <span data-nolang>${esc(A.err)}</span></p>`;
  if(S.err) h+=`<p class="gc-alerte">Search Console : <span data-nolang>${esc(S.err)}</span></p>`;
  const auj=rcISO(new Date()), j=n=>rcISO(new Date(Date.now()-n*86400e3));
  const som=(J,a,b,k)=>Object.keys(J||{}).filter(d=>d>=a&&d<=b).reduce((t,d)=>t+(+(J[d]||[])[k]||0),0);
  const a0=j(29),a1=auj,b0=j(59),b1=j(30);
  const ses=som(A.jours,a0,a1,0), sesP=som(A.jours,b0,b1,0), ach=som(A.jours,a0,a1,2), achP=som(A.jours,b0,b1,2);
  const cl=som(S.jours,a0,a1,0), clP=som(S.jours,b0,b1,0);
  const ev=(x,y)=>y>0?`<small class="${x>=y?'st-up':'st-down'}">${x>=y?'+':''}${Math.round((x-y)/y*100)} % ${A3('vs 30 jours d\'avant','vs previous 30 days')}</small>`:'';
  h+=`<div class="ga-stats ga-stats4">
    <div><span>${A3('Sur le site en ce moment','On the site right now')}</span><b>${nf(A.live||0)}</b><small>${A3('visiteurs','visitors')}</small></div>
    <div><span>${A3('Visites, 30 jours','Visits, 30 days')}</span><b>${nf(ses)}</b>${ev(ses,sesP)}</div>
    <div><span>${A3('Visiteurs qui achètent','Visitors who buy')}</span><b>${ses?(Math.round(ach/ses*1000)/10).toLocaleString(A3('fr-FR','en-US')):'0'} %</b><small>${nf(ach)} ${A3('achats','purchases')}</small></div>
    <div><span>${A3('Clics gratuits depuis Google','Free clicks from Google')}</span><b>${nf(cl)}</b>${ev(cl,clP)}</div></div>`;
  const tab=(tit,ent,L)=>L&&L.length?`<div class="vis-t"><b>${tit}</b><table><thead><tr>${ent.map((e,i)=>`<th class="${i?'n':''}">${e}</th>`).join('')}</tr></thead><tbody>${L.map(r=>`<tr>${r.map((c,i)=>`<td class="${i?'n':''}" ${i?'':'data-nolang'}>${esc(String(c))}</td>`).join('')}</tr>`).join('')}</tbody></table></div>`:'';
  h+=`<div class="vis-g">`
    +tab(A3('D\'où viennent les visites (30 jours)','Where visits come from (30 days)'),[A3('Source','Source'),A3('Visites','Visits'),A3('Achats','Purchases')],(A.sources||[]).slice(0,8).map(r=>[r[0],nf(r[1]),nf(r[2])]))
    +tab(A3('Ce que les gens tapent dans Google (28 jours)','What people type in Google (28 days)'),[A3('Recherche','Search'),A3('Clics','Clicks'),A3('Position','Position')],(S.requetes||[]).slice(0,10).map(r=>[r[0],nf(r[1]),(Math.round(r[3]*10)/10).toLocaleString(A3('fr-FR','en-US'))]))
    +tab(A3('Pays des visiteurs (30 jours)','Visitors\' countries (30 days)'),[A3('Pays','Country'),A3('Visites','Visits'),A3('Achats','Purchases')],(A.pays||[]).slice(0,8).map(r=>[r[0],nf(r[1]),nf(r[2])]))
    +`</div>`;
  h+=`<p class="ga-note">${A3('« Position » : la place moyenne du site dans Google pour cette recherche (1 = premier). Les achats sont ceux que Google Analytics voit ; les ventes de référence restent celles de l\'ERP, en haut de la page.','“Position”: the site\'s average rank in Google for that search (1 = first). Purchases are those Google Analytics sees; the reference sales remain the ERP\'s, at the top of the page.')}</p>`;
  return h+`</section>`;
}
function anDepuis(iso){ const m=Math.max(0,Math.round((Date.now()-Date.parse(iso))/60000)); if(!isFinite(m)) return '';
  if(m<1) return A3('à l\'instant','just now'); if(m<60) return A3(`il y a ${m} min`,`${m} min ago`);
  const h=Math.round(m/60); if(h<48) return A3(`il y a ${h} h`,`${h} h ago`); return A3(`il y a ${Math.round(h/24)} jours`,`${Math.round(h/24)} days ago`); }
function anCampagnes(tous){
  const R=anCampCalc(tous);
  let h=`<section class="ga-card ga-pad" id="gc"><div class="ga-h"><h3>${A3('Les campagnes Google Ads','Google Ads campaigns')}</h3>`;
  if(!R) return h+`<span class="ga-src">${A3('pas encore branchées','not connected yet')}</span></div>
    <p class="gc-txt">${A3('Pour voir ici, en direct, chaque campagne (active ou en pause, budget, objectif, ce qu\'elle coûte et rapporte), un petit script se pose une fois dans le compte Google Ads. Il ne fait que lire : il ne change rien aux campagnes.','To see each campaign here, live (running or paused, budget, target, what it costs and brings), a small script is set up once in the Google Ads account. It only reads: it changes nothing in the campaigns.')}</p>
    <button type="button" class="ga-btn" id="gc-voir">${A3('Afficher le script à coller dans Google Ads','Show the script to paste into Google Ads')}</button><div id="gc-script"></div></section>`;
  const vieux=Date.now()-Date.parse(R.A.maj)>3*3600e3;
  h+=`<span class="ga-src ${vieux?'gc-vieux':''}">${A3('en direct de Google Ads','live from Google Ads')} · ${A3('reçu','received')} ${anDepuis(R.A.maj)}</span></div>`;
  if(vieux) h+=`<p class="gc-alerte">${A3('Plus de nouvelles du compte Google Ads depuis plus de 3 heures : vérifier que le script tourne toutes les heures (Outils › Actions groupées › Scripts).','No news from the Google Ads account for more than 3 hours: check that the script runs every hour (Tools › Bulk actions › Scripts).')}</p>`;
  const V=R.C.filter(c=>c.on||c.cout>0), autres=R.C.length-V.length, nOn=R.C.filter(c=>c.on).length;
  const tot=V.reduce((a,c)=>({cout:a.cout+c.cout,vg:a.vg+c.vg,res:a.res+c.res,b:a.b+(c.on?(+c.budget||0):0)}),{cout:0,vg:0,res:0,b:0});
  h+=`<div class="ga-stats ga-stats4">
    <div><span>${A3('Campagnes actives','Running campaigns')}</span><b>${nf(nOn)}</b><small>${nOn?money(tot.b)+' '+A3('de budget par jour','daily budget'):A3('aucune pub ne passe','no ad is running')}</small></div>
    <div><span>${A3('Coût sur 30 jours','Cost over 30 days')}</span><b>${money(tot.cout)}</b><small>${A3('ventes selon Google','sales per Google')} ${money(tot.vg)}</small></div>
    <div><span>${A3('Ventes pour 1 $ de pub','Sales per $1 of ads')}</span><b>${tot.cout>0?(tot.vg/tot.cout).toFixed(2).replace('.',A3(',','.')):'—'}</b><small>${A3('seuil de rentabilité','break-even')} ≈ ${R.seuil.toFixed(1).replace('.',A3(',','.'))}</small></div>
    <div><span>${A3('Résultat estimé, 30 jours','Estimated result, 30 days')}</span><b class="${tot.res<0?'gc-neg':'gc-pos'}">${money(tot.res)}</b><small>${A3('marge rapportée − pub','margin brought − ads')}</small></div></div>`;
  h+=`<div class="gc-tete"><span>${A3('Campagne','Campaign')}</span><span>${A3('Budget / jour','Budget / day')}</span><span>${A3('Coût 30 j','Cost 30 d')}</span><span>${A3('Pour 1 $','Per $1')}</span><span>${A3('Résultat 30 j','Result 30 d')}</span></div>`
    +V.map(c=>`<div class="gc-l"><span class="gc-n"><b data-nolang>${esc(c.n)}</b><small><i class="gc-e ${c.on?'on':''}">${c.on?A3('Active','Running'):A3('En pause','Paused')}</i> <span data-nolang>${esc(gcType(c.type))}</span>${c.troas?' · '+A3('objectif','target')+' '+Math.round(c.troas*100)+' %':''}${c.cout7>0?' · '+A3('7 j','7 d')+' : '+money(c.cout7):''}</small></span>
      <span class="gc-v">${c.budget!=null?money(c.budget):'—'}</span><span class="gc-v">${money(c.cout)}</span>
      <span class="gc-v ${c.roas==null?'':c.roas<R.seuil?'gc-neg':'gc-pos'}">${c.roas==null?'—':c.roas.toFixed(2).replace('.',A3(',','.'))}</span>
      <span class="gc-v ${c.cout>0?(c.res<0?'gc-neg':'gc-pos'):''}">${c.cout>0?money(c.res):'—'}</span></div>`).join('')
    +(autres?`<p class="ga-note">${A3(`+ ${nf(autres)} autre${autres>1?'s':''} campagne${autres>1?'s':''} en pause, sans dépense sur 30 jours.`,`+ ${nf(autres)} other paused campaign${autres>1?'s':''}, no spend in 30 days.`)}</p>`:'')
    +`<p class="ga-note">${A3(`« Pour 1 $ » = ventes que Google attribue à la campagne pour 1 $ de pub. Sous ${R.seuil.toFixed(1).replace('.',',')}, elle perd de l'argent : marge moyenne des parfums de la pub ${Math.round(R.taux*100)} %, et Google s'attribue environ ${Math.round(100/R.k)} % des ventes réelles.`,`“Per $1” = sales Google credits to the campaign for $1 of ads. Below ${R.seuil.toFixed(1)}, it loses money: average margin of advertised perfumes ${Math.round(R.taux*100)}%, and Google credits itself about ${Math.round(100/R.k)}% of actual sales.`)}</p></section>`;
  return h;
}
function gcType(t){ return ({PERFORMANCE_MAX:'Performance Max',SHOPPING:'Shopping',SEARCH:A3('Recherche','Search'),DISPLAY:'Display',VIDEO:A3('Vidéo','Video'),DEMAND_GEN:'Demand Gen'})[t]||String(t||'').toLowerCase(); }
function anGcBranche(){
  const b=document.getElementById('gc-voir'); if(!b) return;
  b.onclick=async()=>{ const z=document.getElementById('gc-script'); b.disabled=true;
    try{ const r=await fetch(CK_URL+'/api/o/'+CK_ORG+'/google/script',{headers:{Authorization:'Bearer '+ckTok()}}); const j=await r.json().catch(()=>({}));
      if(!r.ok) throw new Error(j.erreur||('HTTP '+r.status));
      z.innerHTML=`<ol class="gc-etapes"><li>${A3('Dans Google Ads : <b>Outils</b> › <b>Actions groupées</b> › <b>Scripts</b>, puis le bouton <b>+</b> › <b>Nouveau script</b>.','In Google Ads: <b>Tools</b> › <b>Bulk actions</b> › <b>Scripts</b>, then the <b>+</b> button › <b>New script</b>.')}</li>
        <li>${A3('Efface le texte proposé et colle celui-ci (bouton <b>Copier</b>).','Delete the suggested text and paste this one (<b>Copy</b> button).')}</li>
        <li>${A3('Clique <b>Autoriser</b> et suis les écrans avec le compte de Sam.','Click <b>Authorize</b> and follow the screens with Sam\'s account.')}</li>
        <li>${A3('Clique <b>Exécuter</b> une fois : les campagnes apparaissent ici dans la minute.','Click <b>Run</b> once: the campaigns show up here within a minute.')}</li>
        <li>${A3('Règle la <b>fréquence</b> sur <b>Toutes les heures</b> et enregistre.','Set the <b>frequency</b> to <b>Hourly</b> and save.')}</li></ol>
        <textarea class="gc-code" readonly spellcheck="false" data-nolang>${esc(j.script||'')}</textarea>
        <button type="button" class="ga-btn" id="gc-copie">${A3('Copier','Copy')}</button>`;
      const c=document.getElementById('gc-copie'), t=z.querySelector('textarea');
      c.onclick=async()=>{ try{ await navigator.clipboard.writeText(t.value); }catch(e){ t.select(); document.execCommand('copy'); } c.textContent=A3('Copié ✓','Copied ✓'); };
    }catch(e){ z.innerHTML=`<p class="gc-alerte">${A3('Le cockpit ne donne pas le script : ','The cockpit does not give the script: ')}<span data-nolang>${esc(e.message||'')}</span></p>`; b.disabled=false; }
  };
}
/* ============ LA PUB, PARFUM PAR PARFUM (9 nov. 2026) ============
   Igal : « la liste des parfums qui rapportent assez pour mériter de la pub » et « quelle économie on pourrait faire par mois ».
   Pour chaque fiche où Google a dépensé de l'argent ces 90 derniers jours (lu par le cockpit, google-pub-v1 › p) :
     marge d'un flacon = prix du site − commission du site (2,9 % + 0,30 $) − prix d'achat − envoi + port payé en moyenne ;
     ventes réelles estimées = ventes que Google lui attribue × (ventes réelles de la pub ÷ ventes selon Google, sur la même période) ;
     ce qu'il rapporte = ventes réelles estimées × (marge ÷ prix) − ce que la pub a coûté.
   Négatif : la pub sur ce parfum coûte plus qu'elle ne rapporte → « Sortir de la pub ». Pas en stock : « Sortir » aussi.
   Pas de prix d'achat ou de prix dans l'ERP : « À vérifier ». L'économie par mois = la perte évitée sur 90 jours ÷ 3. */
function anFiches(){ const M={}; let MOD={}, EXT={q:{}}; try{ MOD=JSON.parse(localStorage.getItem('fiches-modifiees-v1')||'{}')||{}; }catch(e){}
  try{ const r=JSON.parse(localStorage.getItem('stock-externe-v1')||'null'); if(r&&r.q) EXT=r; }catch(e){}
  Object.entries(IDX).forEach(([cle,v])=>{ const m=MOD[cle]||{}; const bc=String(v[0]||''); if(!bc) return;
    let q=v[4]; if(EXT.q[bc]!=null) q=EXT.q[bc]; if(m.qte!=null) q=m.qte;
    const f={cle,bc,nom:v[1],marque:v[2],pa:m.pa!=null?+m.pa:(v[3]==null?null:+v[3]),pvr:m.pvr!=null?+m.pvr:(v[6]==null?null:+v[6]),q:+q||0};
    String(bc).split(/[^0-9A-Za-z]+/).filter(Boolean).forEach(b=>{ M[b.replace(/^0+/,'')]=f; }); });
  return M; }
function anAnalysePub(tous){
  const G=anPubJ();
  const P=G.p; if(!P||!Array.isArray(P.L)||!P.L.length) return null;
  const F=anFiches();
  const site=(REG.canaux||[]).find(c=>c.id==='site')||{}, com=(+site.com>=0&&site.com!=='')?+site.com:2.9, fixe=(site.fixe!=null&&site.fixe!=='')?+site.fixe:0.3;
  const envoi=rcEnvoi('woocommerce');
  /* le port payé en moyenne par commande, et le rapport ventes réelles / ventes selon Google, sur les mêmes 90 jours */
  const C=anDans(tous.filter(o=>o.site==='site'),P.a,P.b), nC=C.filter(o=>!o.ret).length;
  const port=nC?C.reduce((a,o)=>a+o.lignes.reduce((b,v)=>b+(+v.portMt||0),0),0)/nC:0;
  const caAds=C.filter(o=>o.fam==='gads').reduce((a,o)=>a+o.ca,0), ventesG=anPub(P.a,P.b).T.ventes;
  const k=ventesG>0?Math.max(0.3,Math.min(1,caAds/ventesG)):0.8;
  const L=P.L.map(r=>{ const [sku,pub,vg,conv,clics,nomG]=r; const f=F[String(sku||'').replace(/^0+/,'')]||null;
    const o={sku,nom:f?f.nom:nomG,marque:f?f.marque:'',pub:+pub||0,vg:+vg||0,conv:+conv||0,q:f?f.q:null,pvr:f?f.pvr:null,pa:f?f.pa:null};
    if(!f||!(o.pvr>0)||o.pa==null){ o.dec='verif'; return o; }
    o.m=o.pvr*(1-com/100)-fixe-o.pa-envoi+port; o.taux=o.m/o.pvr;
    o.mgE=o.vg*k*o.taux; o.res=o.mgE-o.pub;
    o.dec=(o.q<=0)?'stock':(o.res<0?'sortir':'garder'); return o; });
  const S=d=>L.filter(o=>o.dec===d), som=(X,c)=>X.reduce((a,o)=>a+(o[c]||0),0);
  const sortir=S('sortir'), stock=S('stock'), garder=S('garder'), verif=S('verif');
  /* l'économie : on évite la perte des parfums à sortir, et toute la pub des parfums plus en stock (leur marge réelle est nulle ou incertaine) */
  const gain90=-som(sortir,'res')+Math.max(0,som(stock,'pub')-som(stock,'mgE'));
  return {P,L,k,port,envoi,com,fixe,sortir,stock,garder,verif,gain90,pub90:som(L,'pub')};
}
function anParfumsPub(tous){
  const A=anAnalysePub(tous);
  let h=`<section class="ga-card ga-pad"><div class="ga-h"><h3>${A3('La pub, parfum par parfum','Ads, perfume by perfume')}</h3><span class="ga-src">${A3('90 derniers jours · perfumestrade.com','last 90 days · perfumestrade.com')}</span></div>`;
  if(!A) return h+`<p class="ga-vide">${A3('Les chiffres de Google par parfum arrivent : le cockpit les lit toutes les six heures.','Google\'s per-perfume figures are on their way: the cockpit reads them every six hours.')}</p></section>`;
  const mois=A.gain90/3, pubMois=A.pub90/3;
  const nS=A.sortir.length+A.stock.length;
  h+=`<div class="ga-verdict ${mois>0?'bon':'mal'}"><span class="ga-vv">${gaCnt(Math.round(mois),'$')}</span><span class="ga-vt">${A3(`par mois en plus pour Sam, en sortant de la pub ${nf(nS)} parfums qui coûtent plus qu'ils ne rapportent (sur ${money(pubMois)} de pub par mois)`,`more per month for Sam, by taking out of the ads ${nf(nS)} perfumes that cost more than they bring (out of ${money(pubMois)} of ads per month)`)}</span></div>
  <div class="ga-stats ga-stats4">
    <div><span>${A3('À garder dans la pub','Keep in the ads')}</span><b>${nf(A.garder.length)}</b><small>${money(A.garder.reduce((a,o)=>a+o.pub,0)/3)} ${A3('de pub par mois','of ads per month')}</small></div>
    <div><span>${A3('À sortir : perdent de l\'argent','Take out: losing money')}</span><b>${nf(A.sortir.length)}</b><small>${money(A.sortir.reduce((a,o)=>a+o.pub,0)/3)} ${A3('de pub par mois','of ads per month')}</small></div>
    <div><span>${A3('À sortir : plus en stock','Take out: out of stock')}</span><b>${nf(A.stock.length)}</b><small>${money(A.stock.reduce((a,o)=>a+o.pub,0)/3)} ${A3('de pub par mois','of ads per month')}</small></div>
    <div><span>${A3('À vérifier (prix manquant dans l\'ERP)','To check (price missing in the ERP)')}</span><b>${nf(A.verif.length)}</b><small>${money(A.verif.reduce((a,o)=>a+o.pub,0)/3)} ${A3('de pub par mois','of ads per month')}</small></div>
  </div>`;
  /* 9 nov. 2026 (Igal : « pourquoi on ne peut pas tous les voir, avec un filtre… ceux qui coûtent le plus en pub, ceux où il gagne le
     plus de marge ») : TOUS les parfums, avec un filtre par décision, un tri, une recherche ; 25 lignes, puis « voir plus » */
  h+=`<div class="pp-barre"><div class="ga-mini" id="pp-f">${[['tous',A3('Tous','All'),A.L.length],['garder',A3('À garder','Keep'),A.garder.length],['sortir',A3('À sortir','Take out'),A.sortir.length],['stock',A3('Plus en stock','Out of stock'),A.stock.length],['verif',A3('À vérifier','To check'),A.verif.length]].map(([k,l,n])=>`<button type="button" data-ppf="${k}" class="${(AN.ppf||'tous')===k?'on':''}">${l} <small>${nf(n)}</small></button>`).join('')}</div>
    <label class="pp-tri">${A3('Trier par','Sort by')} <select id="pp-tri">${[['perte',A3('Ceux qui perdent le plus','Biggest losses')],['gain',A3('Ceux qui rapportent le plus','Biggest gains')],['pub',A3('Ceux qui coûtent le plus en pub','Highest ad spend')],['ventes',A3('Ceux qui vendent le plus (selon Google)','Most sales (per Google)')],['marge',A3('Meilleure marge par flacon','Best margin per bottle')]].map(([k,l])=>`<option value="${k}" ${(AN.pptri||'perte')===k?'selected':''}>${l}</option>`).join('')}</select></label>
    <input type="search" id="pp-q" class="pp-q" placeholder="${esc(A3('Chercher un parfum…','Search a perfume…'))}" value="${esc(AN.ppq||'')}"></div>
  <div id="pp-liste"></div>`;
  h+=anSelection(A);
  h+=`<div class="ga-actions"><button type="button" class="ga-btn sec" id="an-xl">${A3('Télécharger la liste complète (Excel)','Download the full list (Excel)')}</button>
    <span>${A3('Pour la personne qui gère les campagnes Google Ads : une ligne par parfum, avec la décision « garder » / « sortir ».','For whoever runs the Google Ads campaigns: one line per perfume, with the decision “keep” / “take out”.')}</span></div>
  <div class="ga-expl"><b>${A3('Pourquoi ce tableau ?','Why this table?')}</b>
    <p>${A3('Google Ads fait payer Sam à chaque clic sur un parfum, même quand le client n\'achète pas. Ce tableau regarde, parfum par parfum, ce que Google a dépensé ces 90 derniers jours, et ce que ce parfum a vraiment rapporté en marge.','Google Ads charges Sam for every click on a perfume, even when the customer does not buy. This table looks, perfume by perfume, at what Google spent over the last 90 days, and at the margin that perfume really brought in.')}</p>
    <ul><li>${A3('<b>À garder</b> : le parfum rapporte plus que sa pub. On continue.','<b>Keep</b>: the perfume brings in more than its ads cost. Keep going.')}</li>
      <li>${A3('<b>À sortir</b> : la pub coûte plus que ce que le parfum rapporte. On arrête de payer Google pour lui. <b>Il reste en vente sur le site</b> : seulement, Google ne le met plus en avant.','<b>Take out</b>: the ads cost more than the perfume brings in. Stop paying Google for it. <b>It stays for sale on the website</b>: Google just stops promoting it.')}</li>
      <li>${A3('<b>Plus en stock</b> : Google dépense encore pour un parfum qu\'on ne peut pas vendre. À sortir tout de suite.','<b>Out of stock</b>: Google still spends on a perfume we cannot sell. Take it out right away.')}</li>
      <li>${A3('<b>À vérifier</b> : il manque le prix ou le prix d\'achat dans l\'ERP ; on ne peut pas trancher.','<b>To check</b>: the price or purchase price is missing in the ERP, so no decision can be made.')}</li></ul>
    <p><b>${A3('Que faire ?','What to do?')}</b> ${A3('Appuyer sur « Ne garder en pub que les gagnants » : la décision part chez Google (Merchant Center la relit chaque jour), et c\'est noté au journal avec l\'heure. Revenir ici chaque mois et renvoyer : le tableau se met à jour tout seul.','Press “Keep only the winners in the ads”: the decision goes to Google (Merchant Center re-reads it every day), and it is written in the log with the time. Come back every month and send again: the table updates by itself.')}</p>
    <p class="ga-prud">${A3('C\'est une estimation : quelques ventes peuvent venir d\'un client qui a d\'abord vu un autre parfum en pub. Le plus sûr est d\'essayer 4 semaines, puis de comparer ici.','This is an estimate: a few sales may come from a customer who first saw another perfume in an ad. The safest is to try for 4 weeks, then compare here.')}</p></div>
  <details class="ga-calc"><summary>${A3('Comment c\'est calculé','How it is calculated')}</summary><p class="ga-note">${A3(`Marge d'un flacon = prix du site − commission (${nf(A.com)} % + ${money2(A.fixe)}) − prix d'achat − envoi (${money(A.envoi)}) + port payé en moyenne (${money2(A.port)}). Les ventes que Google attribue à chaque parfum sont ramenées au réel (× ${nf(Math.round(A.k*100))} % : ce que la pub a vraiment vendu, divisé par ce que Google annonce). Estimation, à revoir chaque mois.`,`Margin per bottle = site price − fee (${nf(A.com)} % + ${money2(A.fixe)}) − purchase price − shipping (${money(A.envoi)}) + average shipping paid (${money2(A.port)}). Sales Google credits to each perfume are scaled to reality (× ${nf(Math.round(A.k*100))} %: what the ads really sold, divided by what Google reports). An estimate, to review every month.`)}</p></details></section>`;
  window._anXL=A;
  return h;
}
function anPPListe(){
  const A=window._anXL, el=document.getElementById('pp-liste'); if(!A||!el) return;
  const f=AN.ppf||'tous', tri=AN.pptri||'perte', q=String(AN.ppq||'').trim().toLowerCase(), n=AN.ppn||25;
  const res=o=>o.res!=null?o.res:-o.pub;
  let X=A.L.filter(o=>f==='tous'||o.dec===f);
  if(q) X=X.filter(o=>((o.nom||'')+' '+(o.marque||'')+' '+(o.sku||'')).toLowerCase().includes(q));
  /* « à vérifier » : pas de résultat connu, donc toujours en bas des tris par résultat (jamais présenté comme la pire perte) */
  const dern=(a,b)=>(a.dec==='verif')-(b.dec==='verif');
  const T={perte:(a,b)=>dern(a,b)||res(a)-res(b),gain:(a,b)=>dern(a,b)||res(b)-res(a),pub:(a,b)=>b.pub-a.pub,ventes:(a,b)=>b.vg-a.vg,marge:(a,b)=>(b.m??-1e9)-(a.m??-1e9)}[tri]||((a,b)=>res(a)-res(b));
  X=X.slice().sort(T);
  const lib={garder:A3('À garder','Keep'),sortir:A3('À sortir','Take out'),stock:A3('Plus en stock','Out of stock'),verif:A3('À vérifier','To check')};
  el.innerHTML=X.length?`<div class="pp-tete"><span>${A3('Parfum','Perfume')}</span><span>${A3('Pub (90 j)','Ads (90 d)')}</span><span>${A3('Ventes Google','Google sales')}</span><span>${A3('Marge rapportée','Margin brought')}</span><span>${A3('Résultat','Result')}</span></div>`
    +X.slice(0,n).map(o=>`<div class="pp-l"><span class="pp-n"><b data-nolang>${esc(o.nom||o.sku)}</b><small><i class="pp-d ${o.dec}">${lib[o.dec]}</i> <span data-nolang>${esc(o.marque||'')}</span>${o.m!=null?' · '+A3('marge/flacon','margin/bottle')+' '+money(o.m):''}</small></span>
      <span class="pp-v">${money(o.pub)}</span><span class="pp-v">${money(o.vg)}</span><span class="pp-v">${o.mgE!=null?money(o.mgE):'—'}</span><span class="pp-v ${o.dec==='verif'?'':res(o)<0?'neg':'pos'}">${o.dec==='verif'?'—':money(res(o))}</span></div>`).join('')
    +(X.length>n?`<button type="button" class="ga-btn sec pp-plus" id="pp-plus">${A3(`Voir plus (${nf(X.length-n)} de plus)`,`Show more (${nf(X.length-n)} more)`)}</button>`:'')
    +`<p class="ga-note">${A3(`${nf(X.length)} parfum${X.length>1?'s':''} · total de la pub : ${money(X.reduce((a,o)=>a+o.pub,0))} sur 90 jours`,`${nf(X.length)} perfume${X.length>1?'s':''} · total ad spend: ${money(X.reduce((a,o)=>a+o.pub,0))} over 90 days`)}</p>`
    :`<p class="ga-vide">${A3('Aucun parfum ne correspond.','No perfume matches.')}</p>`;
  const plus=document.getElementById('pp-plus'); if(plus) plus.onclick=()=>{ AN.ppn=n+50; anPPListe(); };
}
function anExportPub(){ const A=window._anXL; if(!A||typeof sortieXlsx!=='function') return;
  const lib={garder:A3('Garder','Keep'),sortir:A3('Sortir de la pub','Take out of ads'),stock:A3('Sortir de la pub (plus en stock)','Take out of ads (out of stock)'),verif:A3('À vérifier','To check')};
  const ordre={sortir:0,stock:1,verif:2,garder:3};
  const L=A.L.slice().sort((a,b)=>ordre[a.dec]-ordre[b.dec]||((a.res!=null?a.res:-a.pub)-(b.res!=null?b.res:-b.pub)));
  sortieXlsx({titre:A3('La pub, parfum par parfum','Ads, perfume by perfume'),filtre:A.P.a+' → '+A.P.b,fichier:A3('Pub-Google-parfum-par-parfum','Google-Ads-perfume-by-perfume'),
    colonnes:[{t:A3('Décision','Decision')},{t:A3('Code-barres (SKU)','Barcode (SKU)')},{t:A3('Parfum','Perfume')},{t:A3('Marque','Brand')},{t:A3('Stock','Stock'),y:'n'},{t:A3('Prix du site','Site price'),y:'m'},{t:A3("Prix d'achat",'Purchase price'),y:'m'},{t:A3('Marge par flacon','Margin per bottle'),y:'m'},{t:A3('Pub (90 j)','Ads (90 d)'),y:'m'},{t:A3('Ventes selon Google (90 j)','Sales per Google (90 d)'),y:'m'},{t:A3('Marge rapportée (estimée)','Margin brought (est.)'),y:'m'},{t:A3('Résultat (marge − pub)','Result (margin − ads)'),y:'m'}],
    lignes:L.map(o=>[lib[o.dec],o.sku,o.nom||'',o.marque||'',o.q,o.pvr,o.pa,o.m!=null?Math.round(o.m*100)/100:null,o.pub,o.vg,o.mgE!=null?Math.round(o.mgE*100)/100:null,o.res!=null?Math.round(o.res*100)/100:(o.dec==='stock'?-o.pub:null)])}); }
/* 9 nov. 2026 (Igal, sur l'écart « selon Google / réelles ») : les commandes venues de la pub, PAYÉES mais pas encore expédiées.
   Google les compte déjà ; l'ERP les comptera à leur expédition. Le cockpit en garde la liste du moment (_attente_woocommerce) :
   elle ne s'affiche que si la période choisie va jusqu'à aujourd'hui. */
function anAttente(P){ const A=(ORI['_attente_woocommerce']&&ORI['_attente_woocommerce'].L)||[]; if(P.b<rcISO(new Date())) return '';
  const X=A.filter(x=>x&&x.o==='gads'); if(!X.length) return '';
  const mt=X.reduce((a,x)=>a+(+x.mt||0),0);
  return `<div class="ga-attente">+ <b>${nf(X.length)}</b> ${A3(X.length>1?'commandes de la pub payées, pas encore expédiées':'commande de la pub payée, pas encore expédiée',X.length>1?'orders from the ads paid, not shipped yet':'order from the ads paid, not shipped yet')} : <b>${money(mt)}</b> <span>${A3('— elles compteront dès leur expédition','— they will count once shipped')}</span></div>`; }
/* les administrateurs de l'ERP : les rôles Admin et Patron, et eux seuls (un Comptable, qui voit les marges, n'y entre pas) */
function anAdmin(){ const s=session(); return !!s&&/^(admin|patron)$/.test(String(s.role||'')); }
window.__an={AN,anCommandes,anFamille,anDessine,ORI:()=>ORI};
function majUser(){ try{ piedSession(); }catch(e){} }
majUser();
(function(){
  const s=session(); if(!s) return;
  /* Igal, 9 nov. 2026 : « personne à part les admins de l'ERP ne peut la regarder » — Admin (Igal) et Patron (Sam), aucun autre rôle */
  if(!anAdmin()){
    document.querySelector('.wrap').insertAdjacentHTML('beforeend',`<div class="mur"><h2>${A3('Cette rubrique n\'est pas pour ce rôle','This section is not for this role')}</h2><p>${A3('L\'analytique est réservée aux administrateurs de l\'ERP.','Analytics is for the ERP administrators only.')}</p></div>`);
    const a=$('an'); if(a) a.remove(); try{ $('src').innerHTML=A3('accès refusé','access denied'); }catch(e){} return;
  }
  anDessine();
  try{ $('src').innerHTML=A3('origine des commandes<br>relue toutes les 10 min','order origin<br>re-read every 10 min'); }catch(e){}
  /* une nouvelle version des factures ou des origines arrive du serveur (toutes les 8 s) : on relit et on redessine */
  /* 9 nov. 2026 : la relève du serveur (toutes les 8 s) annonce les magasins arrivés par « ck-maj » (et non par « storage ») :
     sans cette écoute, la vidéo restait sur la première étape et le résultat des agents n'apparaissait qu'en rechargeant */
  const AN_CLES=['ventes-origine-v1','google-pub-v1','google-ads-v1','strategie-v1','journal-pub-v1','gads-etiquettes-v1','google-sources-v1',KFACT];
  window.addEventListener('ck-maj',e=>{ const c=(e.detail&&e.detail.cles)||[]; if(!c.some(k=>AN_CLES.includes(k))) return;
    try{ ORI=JSON.parse(localStorage.getItem('ventes-origine-v1')||'{}')||{}; FACT=JSON.parse(localStorage.getItem(KFACT)||'[]')||[]; STRAT=JSON.parse(localStorage.getItem('strategie-v1')||'{}')||{}; }catch(_){}
    anDessine(); });
  window.addEventListener('storage',e=>{ if(e.key==='ventes-origine-v1'||e.key==='google-pub-v1'||e.key==='google-ads-v1'||e.key==='strategie-v1'||e.key==='journal-pub-v1'||e.key==='gads-etiquettes-v1'||e.key==='google-sources-v1'||e.key===KFACT){ try{ ORI=JSON.parse(localStorage.getItem('ventes-origine-v1')||'{}')||{}; FACT=JSON.parse(localStorage.getItem(KFACT)||'[]')||[]; STRAT=JSON.parse(localStorage.getItem('strategie-v1')||'{}')||{}; }catch(_){} anDessine(); } });
})();
'''

html = coquille("Analytique", "Analytique",
  "D'où viennent les commandes des sites, et ce que la publicité Google rapporte vraiment. Réservé aux administrateurs de l'ERP.",
  CSS, CORPS, JS.replace('/*__RECAP__*/', RECAP_JS), donnees=('produits', 'histgros')).replace('__IDX__', 'Object.fromEntries(D_TOUS().map(r=>[r[15],[r[0],r[13],r[2],r[12],r[6],r[8],r[7],r[14],r[4],r[5],r[9]]]))')
open('analytique.html', 'w').write(html)
print('analytique.html', len(html)//1024, 'Ko')
