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
try{ const r=JSON.parse(localStorage.getItem(AN_K)||'null'); if(r&&typeof r==='object'){ ['sel','met','site','src'].forEach(k=>{ if(r[k]) AN[k]=r[k]; }); } }catch(e){}
const anSauve=()=>{ try{ localStorage.setItem(AN_K,JSON.stringify(AN)); }catch(e){} };

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
function anDelta(a,b,lib){ if(b==null) return '';
  const p=gaPct(a,b); if(p==null) return a?`<span class="ga-d up">${A3('nouveau','new')}</span>`:'';
  const s=p>0.5?'up':p<-0.5?'dn':'eq';
  return `<span class="ga-d ${s}" title="${esc(A3('par rapport à ','compared with ')+lib)}">${s==='up'?'↑':s==='dn'?'↓':'='} ${nf(Math.round(Math.abs(p)))} %</span>`; }
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
function anPubJ(){ let G={}; try{ G=JSON.parse(localStorage.getItem('google-pub-v1')||'{}')||{}; }catch(e){} return G||{}; }
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
          <div class="ga-bv">${gaCnt(v,parCA?'$':'n')}<small>${nf(Math.round(part))} %${GP?' '+(gp?anDelta(parCA?g.ca:g.n,parCA?gp.ca:gp.n,lib):`<span class="ga-d up">${A3('nouveau','new')}</span>`):''}</small></div></div>`; }).join('')}</div>`
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
      </div>
      <div class="ga-free ${pub.T.gClics?'':'ko'}"><b>${A3('Google Shopping gratuit','Free Google Shopping')}</b> · ${nf(Math.round(pub.T.gClics))} ${A3('clic'+(pub.T.gClics>1?'s':''),'click'+(pub.T.gClics>1?'s':''))} · ${nf(Math.round(pub.T.gAff))} ${A3('affichages','impressions')}${pub.T.gClics?'':` — <span>${A3('aucun clic : le réglage « Checkout » de Merchant Center bloque la visibilité','no clicks: the Merchant Center “Checkout” setting limits visibility')}</span>`}</div>`;
  }
  h+=`</section></div>`;
  /* ---- 4. les parfums qui se vendent en ligne ---- */
  const PF={}; C.forEach(o=>o.lignes.forEach(v=>{ if(!v.cle) return; const p=PF[v.cle]=PF[v.cle]||{cle:v.cle,q:0,ca:0,qG:0}; p.q+=v.q||0; p.ca+=v.mt||0; if(o.fam==='gads') p.qG+=v.q||0; }));
  const top=Object.values(PF).filter(p=>p.q>0).sort((a,b)=>b.ca-a.ca).slice(0,10), topMax=Math.max(1,...top.map(p=>p.ca));
  if(top.length) h+=`<section class="ga-card ga-pad"><div class="ga-h"><h3>${A3('Les parfums qui se vendent en ligne','Perfumes selling online')}</h3><span class="ga-src">${A3('les dix premiers','top ten')}</span></div>
    <div class="ga-top10">${top.map((p,i)=>{ const r=IDX[p.cle]||[]; return `<a class="ga-pf" href="catalogue.html#fiche=${encodeURIComponent(p.cle)}"><span class="ga-rk">${i+1}</span><span class="ga-pn"><b data-nolang>${esc(r[1]||p.cle)}</b><small data-nolang>${esc(r[2]||'')}</small></span>
      <span class="ga-pb"><i style="--w:${(p.ca/topMax*100).toFixed(1)}%"></i></span><span class="ga-pv"><b>${money(p.ca)}</b><small>${nf(p.q)} ${A3('flacon'+(p.q>1?'s':''),'bottle'+(p.q>1?'s':''))}${p.qG?' · '+nf(p.qG)+' '+A3('via Google Ads','via Google Ads'):''}</small></span></a>`; }).join('')}</div></section>`;
  const lus=C.filter(o=>ok(o)&&o.lu).length, nC=C.filter(ok).length;
  h+=`<p class="ga-note">${A3('Ventes et marges comptées comme dans Ventes et le Tableau de bord (commandes expédiées, remboursements déduits). L\'origine d\'une commande est notée par la boutique elle-même (WooCommerce, Shopify) ; « Google Ads » = un clic sur une publicité payante. La pub est lue chaque heure chez Google.','Sales and margins counted as in Sales and the Dashboard (shipped orders, refunds deducted). The origin of an order is recorded by the store itself (WooCommerce, Shopify); “Google Ads” = a click on a paid ad. Ad spend is read from Google every hour.')}${nC?' '+A3(`Origine connue pour ${nf(lus)} des ${nf(nC)} commandes.`,`Origin known for ${nf(lus)} of the ${nf(nC)} orders.`):''}</p>`;
  z.innerHTML=h;
  /* les courbes, une fois la page posée (il faut la largeur réelle des cartes) */
  const m=M.find(x=>x.k===AN.met);
  const cur=anSerieK(B,C,m.val), prev=CP?anSeriePrec(B,Q,CP,m.val):null;
  gaCourbe(document.getElementById('ga-c1'),B.K,[{v:cur,c:'var(--an-1)',nom:m.nom,nomTip:rcLib(AN.sel,P),aire:true}].concat(prev?[{v:prev,c:'var(--ga-prec)',nom:lib,nomTip:lib,pointille:true}]:[]),m.f,{id:'a',h:270,titre:m.nom});
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
  const re=()=>{ gaAnime=true; anSauve(); anDessine(); };
  z.querySelectorAll('[data-an]').forEach(b=>b.onclick=()=>{ AN.sel=b.dataset.an; re(); });
  z.querySelectorAll('[data-ans]').forEach(b=>b.onclick=()=>{ AN.site=b.dataset.ans; re(); });
  z.querySelectorAll('[data-anm]').forEach(b=>b.onclick=()=>{ AN.met=b.dataset.anm; re(); });
  z.querySelectorAll('[data-ansrc]').forEach(b=>b.onclick=()=>{ AN.src=b.dataset.ansrc; re(); });
}
let _anLarg=0; window.addEventListener('resize',()=>{ const w=innerWidth; if(Math.abs(w-_anLarg)<40) return; _anLarg=w; clearTimeout(window._anRz); window._anRz=setTimeout(()=>{ if(document.getElementById('ga-c1')) anDessine(); },200); });
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
  window.addEventListener('storage',e=>{ if(e.key==='ventes-origine-v1'||e.key==='google-pub-v1'||e.key===KFACT){ try{ ORI=JSON.parse(localStorage.getItem('ventes-origine-v1')||'{}')||{}; FACT=JSON.parse(localStorage.getItem(KFACT)||'[]')||[]; }catch(_){} anDessine(); } });
})();
'''

html = coquille("Analytique", "Analytique",
  "D'où viennent les commandes des sites, et ce que la publicité Google rapporte vraiment. Réservé aux administrateurs de l'ERP.",
  CSS, CORPS, JS.replace('/*__RECAP__*/', RECAP_JS), donnees=('produits', 'histgros')).replace('__IDX__', 'Object.fromEntries(D_TOUS().map(r=>[r[15],[r[0],r[13],r[2],r[12],r[6],r[8],r[7],r[14],r[4],r[5],r[9]]]))')
open('analytique.html', 'w').write(html)
print('analytique.html', len(html)//1024, 'Ko')
