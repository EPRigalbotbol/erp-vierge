# -*- coding: utf-8 -*-
"""Les ventes du site et de la caisse s'enregistrent toutes seules.

Avant : le cockpit déposait les commandes dans une file d'attente, et quelqu'un
devait cliquer « Enregistrer » dans Ventes. Igal a tranché (12 septembre 2026) :
plus de validation. Ce qui est reconnu entre dans le stock à l'ouverture de
n'importe quelle page de l'outil — tableau de bord, ventes, catalogue…

Ce qui reste dans la file, parce qu'on ne PEUT pas l'enregistrer : une ligne
dont le code ne correspond à aucun parfum du catalogue (et dont le nom n'a pas
encore été reconnu une fois). Le stock d'un parfum qui n'existe pas ne se met
pas à jour ; la ligne attend qu'on lui dise lequel c'est, dans Ventes.

Ce bloc tourne AVANT le code de la page, pour que la page lise des magasins déjà
à jour. Il ne dépend que des données brutes (D_TOUS) et des magasins partagés :
pas des index propres à chaque page, qui ne rangent pas les colonnes pareil.
"""

FILE_AUTO = r"""
/* ===== UN CODE-BARRES SUIVI D'UNE MENTION (Sam, 6 oct. 2026) =====
   « 3605533286555nobox » dans le Sheet et dans la caisse : les mêmes chiffres que la
   version en boîte, mais pas le même produit ni le même prix. La mention fait partie
   de l'identité : on ne confond jamais « nobox » avec la boîte, ni « tester » avec le
   flacon. La fiche porte la mention entre parenthèses à la suite du nom : « … (NOBOX) ». */
const FA_MENTIONS=[['NOBOX',/no\s*-?\s*box|unbox|sans\s*bo[iî]te|\(\s*nb\s*\)/i],['TESTER',/tester|testeur|probador/i]];
function mentionBC(code){
  const s=String(code==null?'':code).trim();
  const digits=s.replace(/[^0-9]/g,''), lettres=s.replace(/[0-9]/g,'');
  let mention=''; for(const [m,re] of FA_MENTIONS){ if(re.test(lettres)){ mention=m; break; } }
  return {digits, mention, lettres:lettres.replace(/[^A-Za-z]/g,'')};
}
function nomMention(nom){ const n=String(nom||''); for(const [m,re] of FA_MENTIONS){ if(re.test(n)) return m; } return ''; }
/* parmi des fiches qui partagent les mêmes chiffres : celle dont le nom porte la mention du
   code — ou, sans mention dans le code, une fiche sans mention. Le code dit « nobox » et
   aucune fiche ne l'est : rien (on ne confond pas avec la boîte). */
function parMention(fiches,mention,nomDe){
  if(!fiches||!fiches.length) return null;
  const avec=fiches.filter(f=>nomMention(nomDe(f))===mention);
  if(avec.length) return avec[0];
  return mention?null:fiches[0];
}
/* le nom affiché d'une fiche créée depuis un code à mention : « … (NOBOX) » */
function nomAvecMention(nom,mention){ let n=String(nom||'').trim(); if(!mention) return n;
  const re=(FA_MENTIONS.find(x=>x[0]===mention)||[])[1];
  if(re) n=n.replace(new RegExp('\\s*[\\(\\[]?\\s*(?:'+re.source+')\\s*[\\)\\]]?','i'),'').trim().replace(/[\s\-–·,]+$/,'');
  return (n||String(nom||'').trim())+' ('+mention+')'; }

/* ===== LES VENTES DÉPOSÉES S'ENREGISTRENT TOUTES SEULES ===== */
const FA_KFILE='caisse-file-v1';
const FA_SRC={woocommerce:'Site perfumestrade.com','woocommerce-gros':'Site wholesale.perfumestrade.com',lightspeed:'Caisse Lightspeed',shopify:'Shopify','shopify-pc':'Perfume City (Shopify)',amazon:'Amazon',message:'Commande par message'};
const FA_MOTIFS={retour:'Retour du client',erreur:'Erreur de saisie',annulation:'Commande annulée',defectueux:'Produit défectueux ou abîmé',perdu:'Colis perdu ou volé',autre:'Autre'};
/* La facture d'une vente de canal, faite toute seule. Igal, 12 sept. 2026 : « je ne
   veux pas que quelqu'un crée les invoices ; elles se créent automatiquement à partir
   du moment où il y a eu une vente dans un canal de vente, n'importe lequel ». Le
   numéro suit la série PT-AAAA-NNNN des Réglages ; le prix est celui du canal, taxes
   comprises (le site et Amazon encaissent la taxe eux-mêmes) ; la facture est payée. */
function docAutoPour(f,FACT){
  let R={}; try{ R=JSON.parse(localStorage.getItem('reglages-v1')||'{}')||{}; }catch(e){}
  const E=Object.assign({raison:'',enseigne:'Perfumes Trade',adresse:'',tel:'',email:'',taxid:'',taux:7,carte:2.6,zelle:'',prefixe:'PT',conditions:'',exo:''},R.fact||{});
  if(!E.raison) E.raison=R.societe||'DASY LLC';
  delete E.logo;   /* le logo vient des Réglages à l'affichage (voir _facture.py, enteteDoc) */
  const an=String(f.d||new Date().toISOString()).slice(0,4), pre=(E.prefixe||'PT').toUpperCase()+'-'+an+'-';
  let n=0; (FACT||[]).forEach(x=>{ const m=x&&x.doc&&x.doc.num&&String(x.doc.num).startsWith(pre)?+String(x.doc.num).slice(pre.length):0; if(m>n) n=m; });
  /* le prix affiché de chaque ligne (pAv quand une remise a été répartie), puis la remise une fois */
  const sous=Math.round((f.lignes||[]).reduce((a,l)=>a+(+l.q||0)*(+((l.remise&&l.pAv!=null)?l.pAv:l.p)||0),0)*100)/100;
  const rem=Math.min(sous,Math.max(0,Math.round((+f.remiseCaisse||0)*100)/100)), base=Math.round((sous-rem)*100)/100;
  const src=String(f.auto||f.export||f.canal||'').toLowerCase();
  const pmode=/lightspeed|caisse|boutique/.test(src)?'caisse':'enligne';
  /* la caisse Lightspeed vend HORS taxe et ajoute la sales tax au ticket (39 $ → 41,73 $) :
     quand la source donne la taxe, la facture la porte, comme le ticket du client */
  const tx=(+f.taxe>0&&base>0)?Math.round(+f.taxe*100)/100:0;
  /* le card charge de la caisse (3 nov. 2026) : les « Frais carte » de la facture, au montant encaissé */
  const fc=(+f.fraisCarte>0)?Math.round(+f.fraisCarte*100)/100:0;
  const tot=Math.round((base+fc+tx)*100)/100;
  return {type:'facture',num:pre+String(n+1).padStart(4,'0'),pmode:f.mode==='carte'?'carte':pmode,pstat:'paye',fiscal:'taxable',fref:'',langue:'en',
    emis:new Date().toISOString(),entete:E,auto:true,note:tx?'Prix de la caisse hors taxe, sales tax encaissée au ticket':'Prix du canal, taxes comprises',
    sousTotal:sous,remType:rem?'montant':'pct',remVal:rem,remise:rem,remPct:rem&&sous?Math.round(rem/sous*1000)/10:0,remLib:'',base,fraisPct:fc&&base?Math.round(fc/base*1000)/10:0,frais:fc,
    taux:tx?Math.round(tx/base*10000)/100:0,taxe:tx,total:tot,regle:tot,reste:0};
}
window.docAutoPour=docAutoPour;
/* ---- Les commandes à EXPÉDIER (Igal, 24 sept. 2026) ----
   « Sur certains canaux il doit y avoir une livraison. Ça reste en attente tant
   qu'une personne de chez Sam n'a pas statué la commande : c'est seulement quand
   elle a dit "envoyée ce jour" que le déstock doit être fait. »
   Donc : une vente du site ou d'Amazon n'entre pas dans le stock à son arrivée.
   Elle va dans la rubrique Expéditions, et c'est le geste « expédiée le … » qui
   fait la facture et sort les flacons. La caisse, elle, reste immédiate : le
   client repart avec le flacon. Le choix des canaux se règle dans Expéditions. */
/* ---- le client d'une vente de canal ----
   Igal, 25 sept. 2026 : « sur les ventes j'aimerais le nom du client qui a commandé, et
   qu'un nouveau client s'enregistre sur la liste des clients de l'ERP ». Deux défauts
   vus en ligne le même jour : la caisse envoyait « [object Object] », et Amazon « is
   expecting this to ship by… » à la place du nom. Ce qui n'est pas un nom reste vide. */
function faNomClient(s){
  let n=String(s==null?'':s).replace(/\s+/g,' ').trim();
  if(!n) return '';
  if(/^\[object/i.test(n)||/expect|ship by|^walk[\s-]*in|^anonym|^guest$/i.test(n)) return '';
  if(/^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(n)) return '';
  return n.slice(0,120);
}
const faNormNom=s=>String(s==null?'':s).toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g,'').replace(/[^a-z0-9]+/g,' ').trim();
/* Range le client dans clients-v1 dès que sa commande arrive (pas seulement à la
   facture : une commande du site attend l'expédition, parfois des jours). On ne
   remplit que ce qui manque — une coordonnée corrigée à la main n'est jamais écrasée.
   Le même nom écrit autrement (accents, majuscules) retrouve la fiche existante. */
function faClientPose(CLI,v){
  const nom=faNomClient(v&&v.client); if(!nom) return false;
  const k=faNormNom(nom);
  let cle=Object.keys(CLI).find(x=>faNormNom(x)===k);
  let chg=false;
  if(!cle){ cle=nom; CLI[cle]={nom,depuis:v.d||'',source:FA_SRC[v.src]||v.src||''}; chg=true; }
  const c=CLI[cle];
  [['email','email'],['tel','tel'],['ville','ville'],['pays','pays']].forEach(([a,b])=>{ const x=v[a]; if(x&&!c[b]){ c[b]=String(x).slice(0,120); chg=true; } });
  return chg;
}
function faInscritClients(L){
  try{ const CLI=lit('clients-v1',{})||{}; let chg=false;
    (L||[]).forEach(v=>{ if(v&&!v.annule&&faClientPose(CLI,v)) chg=true; });
    if(chg) ecrit('clients-v1',CLI); return chg; }catch(e){ return false; }
}
/* ---- les lignes qui ne sont pas des parfums ----
   Sacs, papier cadeau, frais de port, échantillons… vendus à la caisse sans code-barres.
   Le 24 sept. 2026, « bags ×90 » a bloqué une vente de caisse dans la file : l'outil
   attendait qu'on lui dise quel parfum c'était. Ces lignes passent désormais sans toucher
   au stock ; une ligne qui porte un vrai code-barres n'est JAMAIS prise pour un service. */
const FA_SERVICE=/^\s*(?:(?:small|medium|large|big|gift|shopping|paper|plastic|petits?|grands?)\s+)?(?:bags?|sacs?|sachets?|bolsas?|gift\s*(?:bag|wrap|box|card)s?|emballages?|papier\s+cadeau|shipping|delivery|livraison|port|samples?|[ée]chantillons?|atomi[sz]ers?|card\s*charge|cc\s*fee|fees?|frais|tax|taxe|tip|pourboire|rounding|discount|remise)\b/i;
function faEstService(l){ return !!l && !/\d{8}/.test(String(l.bc||'')+String(l.sku||'')) && FA_SERVICE.test(String(l.des||'')); }
/* la vente sans ses lignes de service ; `hors` = combien ont été mises de côté */
function faSansService(v){
  const L0=Array.isArray(v&&v.lignes)?v.lignes:[];
  /* 8 oct. 2026 : le « prix » qu'Amazon écrit pour une commande de plusieurs flacons est le TOTAL de la
     ligne. Le cockpit (ck47) envoie maintenant le prix d'un flacon et marque la ligne `pu`. Une ligne
     Amazon à plusieurs flacons arrivée sans cette marque porte encore le total : on la ramène au flacon. */
  const L=(v&&v.src==='amazon')?L0.map(l=>(l&&!l.pu&&l.p!=null&&Math.abs(+l.q)>1)?Object.assign({},l,{p:Math.round(+l.p/Math.abs(+l.q)*100)/100,pu:1}):l):L0;
  const garde=L.filter(l=>!faEstService(l));
  return {lignes:garde, hors:L.length-garde.length};
}
const FA_KEXP='expeditions-v1';
const FA_KST='site-statuts-v1';      /* l'état des commandes sur les sites, rangé par le cockpit */
function faStatutSite(src,num){ try{ const S=lit(FA_KST,{})||{}; return S[String(src||'')+'|'+String(num||'')]||null; }catch(e){ return null; } }
const FA_EXP_DEFAUT={woocommerce:true,'woocommerce-gros':true,amazon:true,shopify:true};
/* EN VEILLE (2 oct. 2026). Sam ne voit pas l'utilité de « Statut shipping » : la rubrique
   sort du menu, et plus aucune commande n'attend un geste pour sortir du stock — le stock sort
   à la vente, comme la caisse. Les réglages par canal sont gardés tels quels : remettre
   FA_EXP_VEILLE à false rallume tout comme avant. */
const FA_EXP_VEILLE=!window.__EXP_ACTIF;   /* les tests de la mécanique la rallument (window.__EXP_ACTIF) */
function faCanauxExp(){
  if(FA_EXP_VEILLE) return {};
  let R={}; try{ R=JSON.parse(localStorage.getItem('reglages-v1')||'{}')||{}; }catch(e){}
  return Object.assign({},FA_EXP_DEFAUT,(R.exped&&typeof R.exped==='object')?R.exped:{});
}
const faExpedie=src=>!!faCanauxExp()[String(src||'')];
function faLitExp(){ try{ const v=(typeof lit==='function')?lit(FA_KEXP,[]):JSON.parse(localStorage.getItem(FA_KEXP)||'[]'); return Array.isArray(v)?v:[]; }catch(e){ return []; } }

/* Ce que le catalogue sait, pour reconnaître une ligne et compter le stock. */
function faContexte(){
  const MOD=lit('fiches-modifiees-v1',{})||{};
  let EXT={q:{}}; try{ EXT=Object.assign({q:{}},JSON.parse(localStorage.getItem('stock-externe-v1')||'{}')); }catch(e){}
  const parBC={}, parCle={}, parASIN={}, parFin={};
  /* un code peut porter plusieurs fiches (la boîte et la « (NOBOX) ») : on les garde toutes,
     et la mention du code départage (Sam, 6 oct. 2026) */
  const pose=(b,cle)=>{ b=String(b||'').replace(/[^0-9]/g,'').replace(/^0+/,''); if(!b) return; (parBC[b]=parBC[b]||[]); if(!parBC[b].includes(cle)) parBC[b].push(cle);
    if(b.length>=10){ const f=b.slice(-10); (parFin[f]=parFin[f]||[]).push([b,cle]); } };
  D_TOUS().forEach(r=>{ if(!r||!r[15]) return; parCle[r[15]]=r; pose(r[0],r[15]);
    if(Array.isArray(r[19])) r[19].forEach(x=>pose(x,r[15]));
    const asin=String(r[18]||'').trim().toUpperCase(); if(/^B0[A-Z0-9]{8}$/.test(asin)&&!parASIN[asin]) parASIN[asin]=r[15]; });
  for(const cle in MOD){ const m=MOD[cle]; if(m&&m.bcs&&parCle[cle]) String(m.bcs).split(/[^0-9]+/).forEach(x=>pose(x,cle)); }
  let AL={}; try{ const a=lit('alias-noms-v1',{}); if(a&&typeof a==='object') AL=a; }catch(e){}
  const norm=s=>String(s==null?'':s).toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g,'').replace(/[^a-z0-9]+/g,' ').trim();
  /* Amazon (24 sept. 2026) : le code arrive souvent abîmé — « 1783320424991 » (un
     chiffre collé devant : le SKU de Sam), « 83320822414 » ou « 3320452505 » (le
     début manque), « 50456082933 » pour 5050456082933, ou l'ASIN B0… tout court.
     On ne devine pas : on accepte seulement quand UN SEUL code du catalogue
     partage les dix derniers chiffres ET que l'un est la fin de l'autre. */
  const cleProche=bc=>{ const raw=String(bc||'').trim().toUpperCase();
    if(/^B0[A-Z0-9]{8}$/.test(raw)) return parASIN[raw]||null;
    const n=raw.replace(/[^0-9]/g,'').replace(/^0+/,''); if(n.length<10) return null;
    const C=(parFin[n.slice(-10)]||[]).filter(([b])=>b.endsWith(n)||n.endsWith(b));
    let cles=[...new Set(C.map(([,c])=>c))]; if(cles.length===1) return cles[0];
    /* Sam crée parfois une seconde annonce Amazon en changeant le PREMIER chiffre du code
       (5291419205986 pour le Khair Fusion 6291419205986, 25 sept. 2026). Même longueur,
       les 12 derniers chiffres identiques, un seul parfum possible : c'est lui. */
    if(!cles.length&&n.length>=12){ const D=(parFin[n.slice(-10)]||[]).filter(([b])=>b.length===n.length&&b.slice(1)===n.slice(1));
      cles=[...new Set(D.map(([,c])=>c))]; if(cles.length===1) return cles[0]; }
    return null; };
  const cleDe=l=>{ if(l.cle&&parCle[l.cle]) return l.cle;
    const codes=[l.bc,l.sku,l.asin].filter(Boolean);   /* l'ASIN : donné par les annonces Amazon de Sam (cockpit) */
    let mentionne=false;
    for(const c of codes){ const n=String(c).replace(/[^0-9]/g,'').replace(/^0+/,''); if(!n||!parBC[n]) continue;
      const mention=mentionBC(c).mention; if(mention) mentionne=true;
      const k=parMention(parBC[n],mention,cle=>((parCle[cle]||[])[13]||'')+' '+((parCle[cle]||[])[1]||'')); if(k) return k; }
    const a=AL[norm(l.des)]; if(a&&a!=='__aucun'&&parCle[a]) return a;
    /* un code « …nobox » sans fiche (NOBOX) ne se rabat pas sur la boîte : Sam tranche */
    if(mentionne) return null;
    for(const c of codes){ const k=cleProche(c); if(k) return k; }
    return null; };
  const qteEff=cle=>{ const m=MOD[cle]; if(m&&m.qte!=null) return +m.qte; const r=parCle[cle]; const e=EXT.q[r[0]]; return e!=null?+e:(+r[6]||0); };
  const paEff=cle=>{ const m=MOD[cle]; if(m&&m.pa!=null) return +m.pa; const v=parCle[cle][12]; return v==null?null:+v; };
  /* Le libellé figé sur chaque vente qui entre toute seule (site, caisse,
     Amazon). Il porte le TYPE : sans lui, une vente d'eau de toilette et une
     d'eau de parfum s'écrivent pareil dans l'historique et sur la facture. */
  const nomDe=cle=>{ const r=parCle[cle]; return ((r[2]||'')+' '+(r[13]||r[1]||'')+(r[4]?' '+r[4]:'')).trim(); };
  const jour=()=>{ try{ return (typeof ajd==='function')?ajd():new Date().toISOString().slice(0,10); }catch(e){ return new Date().toISOString().slice(0,10); } };
  const par=(typeof NOM_UTIL==='string'&&NOM_UTIL)?NOM_UTIL:'(automatique)';
  /* ---- Perfume City (Shopify) : des codes-barres abîmés, 13 oct. 2026 ----
     Beaucoup de codes de la boutique de Kim ont perdu leurs derniers chiffres (8435415100000 : le début
     est bon, la fin est remplacée par des zéros, comme un Excel qui arrondit), et d'autres lignes n'ont
     aucun code. Pour ces lignes SEULEMENT (jamais pour le site, la caisse ou Amazon), on retrouve le
     parfum avec prudence : le début du code, quand il y en a un, puis le nom, la contenance et le type.
     On n'accepte que si UN parfum domine nettement ; sinon la ligne reste à compléter à la main. */
  const sw=new Set('by the de la le pour for and et of with oz ml edp edt edc edi extrait parfum perfume cologne spray vapo men man women woman homme femme gift set pcs piece pieces unisex eau toilette'.split(' '));
  /* ce qui n'est pas un flacon de parfum : un gel douche ne se confond pas avec l'eau de parfum du même nom */
  const FORME=['body','lotion','shower','gel','deodorant','deo','roll','soap','cream','mist','hair','candle','diffuser','oil'];
  const strip=t=>String(t||'').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g,'').replace(/\([^)]*(\)|$)/g,' ').replace(/[|\/\-–,.()]+/g,' ').replace(/\s+/g,' ').trim();
  const tok=t=>strip(t).split(' ').filter(w=>w&&!sw.has(w)&&!FORME.includes(w)&&!/^\d+(\.\d+)?$/.test(w)&&!/^\d+(ml|oz|pcs|pc)$/.test(w));
  /* la contenance se lit sur le texte brut : « 2.5 oz » perdrait son point dans strip() */
  const taille=t=>{ const x=String(t||'').toLowerCase(); let m=x.match(/(\d+(?:\.\d+)?)\s*oz/); if(m) return Math.round(+m[1]*10)/10; m=x.match(/(\d+)\s*ml/); if(m) return Math.round(+m[1]/29.5735*10)/10; return null; };
  const formeDe=t=>new Set(strip(t).split(' ').filter(w=>FORME.includes(w)));
  const coffret=t=>/\b(gift|set|coffret|pcs)\b/i.test(String(t||''));
  const typeDe=t=>{ const x=strip(t); return /\bedp\b|eau de parfum/.test(x)?'EDP':/\bedt\b|eau de toilette/.test(x)?'EDT':/\bedc\b|cologne/.test(x)?'EDC':/extrait|extract/.test(x)?'EXT':''; };
  let CATS=null; const MEMO={};
  const cleShopify=l=>{
    const memo=String(l.bc||'')+'|'+String(l.des||''); if(memo in MEMO) return MEMO[memo];
    if(!CATS) CATS=D_TOUS().filter(r=>r&&r[15]).map(r=>{ const nom=(r[2]||'')+' '+(r[13]||r[1]||''), sans=nom.replace(/\([^)]*\)/g,' ');   /* la parenthèse « (… inspiré de …) » n'est pas le nom */
      return {cle:r[15],bcs:[String(r[0])].concat(Array.isArray(r[19])?r[19].map(String):[]),t:new Set(tok(sans)),f:formeDe(sans),g:coffret(sans),sz:parseFloat(r[3])||null,ty:String(r[4]||'').toUpperCase(),men:nomMention(nom)}; });
    const bc=String(l.bc||'').replace(/[^0-9]/g,''), ts=new Set(tok(l.des)), sz=taille(l.des), ty=typeDe(l.des), fs=formeDe(l.des), g=coffret(l.des), men=nomMention(l.des)||mentionBC(l.bc).mention;
    const z=bc.replace(/0+$/,''); let pool=CATS, viaCode=false;
    if(bc.length>=12&&bc.length-z.length>=3&&z.length>=6){
      /* le code est tronqué ou ARRONDI à ses premiers chiffres (8435415076937 devient 8435415100000) : on garde les codes qui commencent
         pareil et ceux qui, arrondis au même nombre de chiffres, donnent le même nombre */
      const k=z.length, zn=+z, mem=b=>b.length===bc.length&&(b.startsWith(z)||Math.round(+b/Math.pow(10,b.length-k))===zn);
      const P=CATS.filter(c=>c.bcs.some(mem)); if(P.length){ pool=P; viaCode=true; } }
    const sc=c=>{ let i=0; ts.forEach(w=>{ if(c.t.has(w)) i++; }); const d=2*i/((ts.size+c.t.size)||1), cov=ts.size?i/ts.size:0;
      let x=d*.5+cov*.5; if(sz!=null&&c.sz!=null) x+=Math.abs(sz-c.sz)<.25?.15:-.3; if(ty&&c.ty) x+=ty===c.ty?.1:-.2; if(c.men!==men) x-=.5;
      c.f.forEach(w=>{ if(!fs.has(w)) x-=.4; }); fs.forEach(w=>{ if(!c.f.has(w)) x-=.3; }); if(c.g!==g) x-=.3; return x; };
    /* un parfum doit dominer : soit nettement devant le suivant, soit identique mot pour mot (nom, contenance, type) et un cran devant */
    const choisit=(P,seuil,marge)=>{ const L=P.map(c=>[sc(c),c]).sort((a,b)=>b[0]-a[0]);
      if(!L.length||!ts.size) return null; const b=L[0], s2=(L.find(x=>x[1].cle!==b[1].cle)||[-1])[0];
      const tout=[...ts].every(w=>b[1].t.has(w));   /* tous les mots du titre Shopify se retrouvent dans ce parfum */
      return ((b[0]>=seuil&&b[0]-s2>=marge)||(b[0]>=1.2&&b[0]-s2>=.09)||(tout&&b[0]>=.7&&b[0]-s2>=.2))?b[1].cle:null; };
    /* le début du code d'abord ; s'il ne tranche pas (ou ne mène à rien), le NOM seul, plus exigeant */
    const r=(viaCode?choisit(pool,.55,.12):null)||choisit(CATS,.9,.2);
    MEMO[memo]=r; return r; };
  /* une vente résolue : ses lignes avec leur clé, ou null si une est inconnue */
  const resout=v=>{ if(!v||!Array.isArray(v.lignes)||!v.lignes.length) return null;
    const LL=faSansService(v).lignes; if(!LL.length) return null;
    const pcs=v.src==='shopify-pc';
    const L=LL.map(l=>({cle:cleDe(l)||(pcs?cleShopify(l):null),bc:l.bc||'',des:l.des||'',q:+l.q||0,p:l.p==null?null:+l.p})).filter(l=>l.q);
    /* Perfume City : un article que le catalogue central ne connaît pas (produit propre à la boutique) n'arrête JAMAIS la vente :
       elle s'enregistre avec la ligne « hors catalogue » (nom de Shopify, aucun stock touché). Igal : « plus de vente en attente ». */
    if(pcs) L.forEach(l=>{ if(!l.cle) l.cle=''; });
    if(!L.length||(!pcs&&L.some(l=>!l.cle))) return null; return L; };
  return {MOD,parCle,cleDe,qteEff,paEff,nomDe,jour,par,resout};
}

/* Enregistre pour de bon une liste de ventes résolues [{v,L}] : facture, stock,
   historique par parfum, client, journal. `o.lib` = la phrase du journal pour les
   ventes (sinon « enregistrée automatiquement ») ; `o.exp` = l'expédition (date,
   suivi) portée sur la facture. Renvoie ce qui a été fait. */
/* QUEL ORDINATEUR a enregistré une vente (20 oct. 2026) : deux postes ouverts sous le même compte signaient
   tous deux « Sam » — impossible de savoir lequel s'était trompé. Un nom par navigateur, jamais partagé. */
function faPoste(){
  try{ let p=JSON.parse(localStorage.getItem('ck-poste')||'null');
    if(!p||!p.id){ const u=navigator.userAgent||'';
      const os=/iPhone|iPad/.test(u)?'iPhone/iPad':/Android/.test(u)?'Android':/Mac/.test(u)?'Mac':/Windows/.test(u)?'Windows':/Linux/.test(u)?'Linux':'ordinateur';
      const nav=/Edg\//.test(u)?'Edge':/Chrome\//.test(u)?'Chrome':/Firefox\//.test(u)?'Firefox':/Safari\//.test(u)?'Safari':'navigateur';
      p={id:Math.random().toString(36).slice(2,6).toUpperCase(),lib:os+' · '+nav}; localStorage.setItem('ck-poste',JSON.stringify(p)); }
    return p.lib+' · '+p.id; }catch(e){ return ''; }
}
window.faPoste=faPoste;
function faEnregistre(A,C,o){
  o=o||{}; const rien={faites:[],ventes:0,retours:0,mt:0,ecarts:[],ids:[]};
  if(!A||!A.length) return rien;
  const {MOD,qteEff,paEff,nomDe,jour}=C, par=o.par||C.par;
  let FACT=lit('factures-v1',[]); if(!Array.isArray(FACT)) FACT=[];
  const VENT=lit('ventes-v1',{})||{}, CLI=lit('clients-v1',{})||{}, J=lit('crm-journal-v1',[])||[];
  const dejaRendu=fid=>{ const r={}; FACT.filter(f=>f.retour&&f.refId===fid).forEach(f=>(f.lignes||[]).forEach(l=>{ r[l.cle]=(r[l.cle]||0)+Math.abs(l.q||0); })); return r; };
  const faits=[], ecarts=[], retours=[], ids=[]; let nL=0, mt=0, nV=0, nPC=0, nPCsans=0;
  /* ---- Perfume City (Shopify), 13 oct. 2026 ----
     Les ventes de la boutique de Kim n'entrent JAMAIS dans le stock central : elles sortent de l'inventaire
     Perfume City (magasin partagé pc-stock-v1, voir _fusion.py). Celles d'AVANT le jour de la liaison
     (`sansStock`, marque posée par le cockpit) ne touchent aucun stock : le stock de Kim a été compté depuis. */
  const pcOk=typeof pcsRows==='function'&&typeof pcsSauve==='function';
  let PCR=null; const pcRows=()=>{ if(PCR===null) PCR=(pcOk&&pcsRows())||[]; return PCR; };
  const pcBC=cle=>String(((C.parCle||{})[cle]||[])[0]||'').replace(/[^0-9]/g,'').replace(/^0+/,'');
  const pcIdx=cle=>{ const b=pcBC(cle); return b?pcRows().findIndex(z=>z&&z[0]&&String(z[0]).replace(/^0+/,'')===b):-1; };
  const pcQ=cle=>{ const i=pcIdx(cle); return i<0?0:(+pcRows()[i][5]||0); };
  let pcTouche=false;
  const pcPoseQ=(cle,q)=>{ const i=pcIdx(cle), R=pcRows();
    if(i<0){ if(!pcBC(cle)||!(q>0)) return false; const r=C.parCle[cle], pa=paEff(cle);
      R.push([r[0]||'',r[13]||r[1]||'',r[2]||'',r[3]||'','',q,pa,pa!=null?q*pa:null,'non','b'+r[0],null,null]); pcTouche=true; return true; }
    R[i][5]=q; if(R[i][6]!=null) R[i][7]=q*R[i][6]; pcTouche=true; return true; };
  A.forEach(x=>{
    const v=x.v, canal=v.lieu||FA_SRC[v.src]||'Autre';
    const pcV=v.src==='shopify-pc', aucun=!!(pcV&&v.sansStock);
    if(v.annule){
      /* un retour : rattaché à la vente d'origine si on la connaît, avec le motif que
         la source donne ; le stock ne revient que si la vente est connue ici */
      const o2=FACT.find(f=>f.sens==='vente'&&!f.retour&&f.num===String(v.num||'')&&(f.auto===v.src||!f.auto))||null;
      const rendu=o2?dejaRendu(o2.id):{}, motif=v.motif||'retour';
      const sansR=pcV&&(aucun||(o2&&o2.stock===false));   /* Perfume City : la vente n'avait touché aucun stock, le remboursement non plus */
      const lignes=x.L.map(l=>{ const n=Math.abs(l.q);
        if(!l.cle){ nL++; return {cle:'',bc:l.bc,ref:l.des||'(article hors catalogue)',q:-n,p:l.p,qAv:0,qAp:0,hors:true,pc:true}; }
        const qAv=pcV?pcQ(l.cle):qteEff(l.cle); let qAp=qAv;
        if(o2&&!sansR){ const lo=(o2.lignes||[]).find(z=>z.cle===l.cle);
          /* tout ce qui a été vendu revient (26 sept. 2026) : les flacons vendus « à
             découvert » existaient bien, c'est le compte de l'ERP qui était court */
          const vendu=(lo&&o2.stock!==false)?Math.max(0,lo.q||0):0;
          qAp=qAv+Math.min(n,Math.max(0,vendu-(rendu[l.cle]||0))); }
        if(qAp!==qAv){ if(pcV) pcPoseQ(l.cle,qAp); else MOD[l.cle]=Object.assign({},MOD[l.cle]||{},{qte:qAp}); }
        nL++;
        (VENT[l.cle]=VENT[l.cle]||[]).push({d:v.d||jour(),h:v.h||undefined,p:l.p,c:v.client||'',q:-n,num:(o2?o2.num:v.num||'')+' (remboursé)',k:canal});
        return Object.assign({cle:l.cle,bc:l.bc,ref:nomDe(l.cle),q:-n,p:l.p,qAv,qAp,paAv:o2?((o2.lignes||[]).find(z=>z.cle===l.cle)||{}).paAv:paEff(l.cle)},pcV?{pc:true}:{}); });
      const mtR=lignes.reduce((a,l)=>a+Math.abs(l.q)*(l.p||0),0);
      const nR=o2?FACT.filter(z=>z.retour&&z.refId===o2.id).length+1:1;
      const num=(o2?o2.num:(v.num||'AUTO'))+'-R'+nR;
      FACT.push({id:'r'+Date.now().toString(36)+Math.random().toString(36).slice(2,5),num,sens:'vente',retour:true,
        refId:o2?o2.id:'',refNum:o2?o2.num:(v.num||''),canal,tiers:faNomClient(v.client)||(o2?o2.tiers:'')||'',d:v.d||jour(),h:v.h||undefined,lignes,
        montant:-mtR,stock:pcV?(!!o2&&!sansR):!!o2,mode:motif==='annulation'?'aucun':'carte',motif,
        note:(FA_SRC[v.src]||v.src||'')+(o2?(sansR?" — vente d'avant la liaison, aucun stock touché":''):" — vente d'origine inconnue ici, stock inchangé"),
        par,t:new Date().toISOString(),auto:v.src||'',recu:v.recu||undefined,_i:v._i?'fr|'+v._i:undefined});
      if(pcV) FACT[FACT.length-1].pc=true;
      retours.push({num,mt:mtR,orig:!!o2,motif,sans:!!sansR});
      faits.push(v._i); return;
    }
    /* Sam, 3 oct. 2026 : « j'ai fait une vente sur Lightspeed à 16:20, avec 10 % de remise à la
       cliente (Nasha) ; l'ERP n'a pas tenu compte des 10 % ». Une remise sur toute la vente arrive
       de la caisse comme une ligne « Discount » à prix négatif ; elle était mise de côté avec les
       sacs, et la vente comptait 392 $ au lieu de 352,80 $. Le cockpit la donne maintenant à part
       (v.remise). Elle est répartie sur les lignes comme pour une vente saisie ici : chaque ligne
       garde le prix encaissé (marge, statistiques) et le prix affiché ; la facture porte la remise. */
    const plein=x.L.reduce((a,l)=>a+(+l.q||0)*(+l.p||0),0);
    const remC=(+v.remise>0&&plein>0)?Math.min(plein,Math.round(+v.remise*100)/100):0, kR=remC?(plein-remC)/plein:1;
    const lignes=x.L.map(l=>{
      if(!l.cle){ nL++; mt+=l.q*(l.p||0); return {cle:'',bc:l.bc,ref:l.des||'(article hors catalogue)',q:l.q,p:l.p,qAv:0,qAp:0,hors:true,pc:true}; }   /* hors catalogue : aucun stock, aucun historique de parfum */
      const qAv=pcV?pcQ(l.cle):qteEff(l.cle), qAp=aucun?qAv:Math.max(0,qAv-l.q), manque=(!aucun&&l.q>0&&l.q>qAv&&!(pcV&&!pcBC(l.cle)))?l.q-qAv:0;   /* Perfume City : un article sans code-barres (mini vaporisateur…) n'a pas de ligne dans son inventaire : rien à « découvert » */
      const pE=(remC&&l.p!=null)?Math.round(l.p*kR*100)/100:l.p;
      if(pcV){ if(qAp!==qAv) pcPoseQ(l.cle,qAp); } else MOD[l.cle]=Object.assign({},MOD[l.cle]||{},{qte:qAp});
      nL++; mt+=l.q*(pE||0);
      (VENT[l.cle]=VENT[l.cle]||[]).push({d:v.d||jour(),h:v.h||undefined,p:pE,c:faNomClient(v.client),q:l.q,num:v.num||'',k:canal});
      if(manque) ecarts.push({num:v.num||'',bc:l.bc,ref:nomDe(l.cle),vendu:l.q,stock:qAv,manque});
      return Object.assign({cle:l.cle,bc:l.bc,ref:nomDe(l.cle),q:l.q,p:pE,qAv,qAp,paAv:paEff(l.cle),manque:manque||undefined},
        (remC&&l.p!=null)?{pAv:l.p,remise:true}:{},pcV?{pc:true}:{}); });
    faClientPose(CLI,v);
    const fa={id:'c'+Date.now().toString(36)+Math.random().toString(36).slice(2,5),
      num:(v.num||('AUTO-'+Date.now().toString(36))),sens:'vente',canal,export:canal,
      tiers:faNomClient(v.client),d:v.d||jour(),h:v.h||undefined,lignes,
      montant:lignes.reduce((a,l)=>a+l.q*(l.p||0),0),stock:!aucun,par,t:new Date().toISOString(),auto:v.src||'',poste:faPoste()||undefined};
    if(pcV){ fa.pc=true; nPC++; if(aucun){ nPCsans++; fa.note='Commande Shopify d\'avant la liaison : aucun stock touché'; }
      const nHors=lignes.filter(l=>l.hors).length; if(nHors) fa.note=((fa.note||'')+' '+nHors+' article'+(nHors>1?'s':'')+' hors catalogue central (aucun stock touché)').trim(); }
    /* 1er oct. 2026 (Igal : « l'heure exacte de la vente et l'heure où elle est arrivée sur l'ERP ») :
       quand le serveur l'a reçue, et quand l'ERP l'a prise en compte (commande à expédier : son arrivée) */
    if(v.recu) fa.recu=String(v.recu); if(v.arrive) fa.arrive=String(v.arrive);
    /* son identité vient de la vente, pas du hasard : si deux onglets l'enregistrent en même
       temps, les deux factures sont reconnues comme une seule à la fusion (1er oct. 2026) */
    if(v._i) fa._i='fa|'+v._i;
    if(+v.taxe>0) fa.taxe=Math.round(+v.taxe*100)/100;          /* la sales tax du ticket, à part du chiffre d'affaires */
    if(v.paie&&typeof v.paie==='object') fa.paie=v.paie;        /* 24 oct. 2026 : espèces / carte / autre, pour la caisse (Tableau de bord) */
    if(remC) fa.remiseCaisse=remC;
    /* Amazon : commande restée « pending » le temps de vérifier le paiement, confirmée des jours
       après. La vente est au jour de la confirmation ; la date de commande est dite (3 oct. 2026) */
    if(v.commande&&v.commande!==v.d){ const us=x=>String(x||'').replace(/^(\d{4})-(\d{2})-(\d{2}).*$/,'$2/$3/$1');
      fa.commande=v.commande; fa.note=((fa.note||'')+' commandée sur Amazon le '+us(v.commande)+', paiement confirmé le '+us(v.d)).trim(); }
    if(+v.port>0) fa.port=Math.round(+v.port*100)/100;          /* 29 sept. : le port payé par le client (site) */
    /* 3 nov. 2026 : le « card charge » d'une cote de la caisse, payé par le client — « Frais carte » sur la facture, ajouté au
       total, hors chiffre d'affaires et hors marge (il couvre les frais de carte, les deux s'annulent) */
    if(+v.fraisCarte>0) fa.fraisCarte=Math.round(+v.fraisCarte*100)/100;
    if(v.mode) fa.mode=String(v.mode);
    const nh=faSansService(v).hors+(+v.hors||0);
    if(nh) fa.note=((fa.note||'')+' '+nh+' ligne'+(nh>1?'s':'')+' hors parfum (sac, port…) — pas dans le stock').trim();
    if(remC) fa.note=((fa.note||'')+' remise de '+remC.toFixed(2)+' $ faite à la caisse ('+Math.round(remC/plein*1000)/10+' %)').trim();
    if(o.exp){ fa.exp=o.exp; fa.note=((fa.note||'')+' expédiée le '+String(o.exp.d||'').replace(/^(\d{4})-(\d{2})-(\d{2}).*$/,'$2/$3/$1')+(o.exp.suivi?' — suivi '+o.exp.suivi:'')).trim(); }
    /* Perfume City : Shopify envoie déjà son reçu au client ; pas de facture automatique (elle ne ferait que
       remplir la série PC-AAAA-NNNN de centaines de numéros). Kim fait la sienne depuis Ventes si on la lui demande. */
    if(!pcV) fa.doc=docAutoPour(fa,FACT);
    FACT.push(fa);
    nV++; faits.push(v._i); ids.push(fa.id);
  });
  if(pcTouche) pcsSauve(pcRows());                /* inventaire Perfume City : écrit une fois, après tous les mouvements */
  ecrit('factures-v1',FACT); ecrit('fiches-modifiees-v1',MOD); ecrit('ventes-v1',VENT); ecrit('clients-v1',CLI);
  const t=new Date().toISOString();
  if(nPC) J.push({t,u:par,act:'vente',lib:nPC+' vente'+(nPC>1?'s':'')+' Shopify de Perfume City'+(nPC-nPCsans?' — '+(nPC-nPCsans)+' sortie'+(nPC-nPCsans>1?'s':'')+' de l\'inventaire Perfume City':'')+(nPCsans?' — '+nPCsans+' d\'avant la liaison, aucun stock touché':'')+' (stock central intact)',ref:'',av:null,ap:'',n:0,det:[],poste:faPoste()||undefined});
  if(nV) J.push({t,u:par,act:'vente',lib:(o.lib||(nV+' vente'+(nV>1?'s':'')+' du site ou de la caisse enregistrée'+(nV>1?'s':'')+' automatiquement'))+' — '+nL+' ligne(s)'+(o.suite||''),ref:'',av:null,ap:Math.round(mt)+' $',poste:faPoste()||undefined});
  retours.forEach(r=>J.push({t,u:par,act:'annulation',lib:'remboursement '+r.num+' — '+(FA_MOTIFS[r.motif]||'retour').toLowerCase()+(r.sans?", aucun stock touché (vente d'avant la liaison)":r.orig?', stock remis':", vente d'origine inconnue, stock inchangé")+' (automatique)',n:0,impact:Math.round(r.mt),det:[]}));
  if(ecarts.length) J.push({t,u:par,act:'stock',
    lib:'vendu à découvert — '+ecarts.reduce((a,e)=>a+e.manque,0)+' flacon(s) de plus que le stock compté, sur '+ecarts.length+' ligne(s)',
    ref:'',av:null,ap:ecarts.map(e=>e.ref+' : vendu '+e.vendu+', en stock '+e.stock).join(' · '),n:ecarts.length,det:ecarts,poste:faPoste()||undefined});
  ecrit('crm-journal-v1',J);
  return {faites:faits,ventes:nV,retours:retours.length,mt,ecarts,ids};
}

/* Une commande annulée par le canal AVANT d'avoir été expédiée : elle sort
   simplement de la rubrique Expéditions. Rien n'est sorti du stock, rien n'y
   revient, pas de facture d'avoir. Renvoie vrai si c'était le cas. */
function faAnnuleAvantExp(v,J,par){
  if(!v||!v.annule) return false;
  const E=faLitExp(); const i=E.findIndex(e=>e.statut==='attente'&&e.src===v.src&&String(e.num||'')===String(v.num||''));
  if(i<0) return false;
  const e=E[i]; E.splice(i,1); ecrit(FA_KEXP,E);
  J.push({t:new Date().toISOString(),u:par,act:'annulation',lib:'commande '+(e.num||'')+' annulée par '+(FA_SRC[e.src]||e.src||'le canal')+' avant expédition — rien n\'était sorti du stock',n:0,impact:Math.round(e.montant||0),det:[]});
  return true;
}

/* ---- RÉPARATION des ventes Perfume City rangées par une ancienne page (13 oct. 2026) ----
   Le soir de la liaison Shopify, des pages de l'ERP restées ouvertes avec l'ANCIEN code ont enregistré 383 ventes de la
   boutique de Kim comme des ventes ordinaires : flacons sortis du stock CENTRAL, facture DASY en prime. Cette
   réparation, qui tourne à l'ouverture de n'importe quelle page, retrouve ces ventes (source shopify-pc, sans la marque `pc`) et :
   remet le stock central comme avant, retire la facture automatique, marque la vente Perfume City, puis sort de l'inventaire
   Perfume City SEULEMENT celles du jour de la liaison et d'après. Elle ne fait rien une fois la marque posée. */
const FA_PC_DEBUT='2026-10-13';
function faReparePC(){
  try{
    if(typeof pcsRows!=='function'||typeof pcsSauve!=='function'||typeof D_TOUS!=='function'||typeof lit!=='function'||typeof ecrit!=='function') return 0;
    const FACT=lit('factures-v1',[]); if(!Array.isArray(FACT)) return 0;
    /* trois sortes de ventes mal rangées : (a) sans la marque `pc` (ancienne page : stock CENTRAL touché) ;
       (b) marquées `pc` mais avec une facture DASY ; (c) d'avant la liaison mais sorties de l'inventaire Perfume City
       (un « Compléter » à la main sur une vieille vente) */
    const tous=FACT.filter(f=>f&&f.auto==='shopify-pc'&&(!f.pc||f.doc||(!f.retour&&String(f.d||'')<FA_PC_DEBUT&&f.stock!==false)));
    if(!tous.length) return 0;
    const mal=tous.filter(f=>!f.pc), dejaPC=tous.filter(f=>f.pc);
    const C=faContexte(), MOD=C.MOD, R=pcsRows()||[];
    const bcDe=cle=>String(((C.parCle||{})[cle]||[])[0]||'').replace(/[^0-9]/g,'').replace(/^0+/,'');
    const idx=cle=>{ const b=bcDe(cle); return b?R.findIndex(z=>z&&z[0]&&String(z[0]).replace(/^0+/,'')===b):-1; };
    const pcQ=cle=>{ const i=idx(cle); return i<0?0:(+R[i][5]||0); };
    let touche=false;
    const pcPose=(cle,q)=>{ const i=idx(cle);
      if(i<0){ if(!bcDe(cle)||!(q>0)) return; const r=C.parCle[cle], pa=C.paEff(cle); R.push([r[0]||'',r[13]||r[1]||'',r[2]||'',r[3]||'','',q,pa,pa!=null?q*pa:null,'non','b'+r[0],null,null]); touche=true; return; }
      R[i][5]=q; if(R[i][6]!=null) R[i][7]=q*R[i][6]; touche=true; };
    /* d'abord les ventes (par date), puis les retours : un retour a besoin de sa vente */
    const ordre=(a,b)=>String(a.d||'').localeCompare(String(b.d||''))||String(a.h||'').localeCompare(String(b.h||''));
    const ventes=mal.filter(f=>!f.retour).sort(ordre), retours=mal.filter(f=>f.retour).sort(ordre);
    let nV=0, nR=0, nSorties=0;
    /* 0. déjà marquées Perfume City : seulement la facture en trop, et les flacons d'une vente d'avant la liaison remis à l'inventaire */
    dejaPC.forEach(f=>{
      if(!f.retour&&String(f.d||'')<FA_PC_DEBUT&&f.stock!==false){
        (f.lignes||[]).forEach(l=>{ if(!l||!l.cle||!(C.parCle||{})[l.cle]||l.qAv==null||l.qAp==null) return;
          if(l.qAv!==l.qAp) pcPose(l.cle,Math.max(0,pcQ(l.cle)+(l.qAv-l.qAp)));
          const q=pcQ(l.cle); l.qAv=q; l.qAp=q; delete l.manque; });
        f.stock=false; f.note='Commande Shopify d\'avant la liaison : aucun stock touché'; }
      delete f.doc; });
    /* 1. le stock central redevient ce qu'il était : chaque ligne avait enlevé qAv-qAp (ou remis qAp-qAv pour un retour) */
    mal.forEach(f=>(f.lignes||[]).forEach(l=>{ if(!l||!l.cle||!(C.parCle||{})[l.cle]||l.qAv==null||l.qAp==null||l.qAv===l.qAp) return;
      MOD[l.cle]=Object.assign({},MOD[l.cle]||{},{qte:Math.max(0,C.qteEff(l.cle)+(l.qAv-l.qAp))}); }));
    /* 2. les ventes du jour de la liaison et d'après sortent de l'inventaire Perfume City ; les autres ne touchent rien */
    ventes.forEach(f=>{
      const jour=String(f.d||'')>=FA_PC_DEBUT;
      (f.lignes||[]).forEach(l=>{ if(!l) return;
        const qAv=l.cle?pcQ(l.cle):0, q=+l.q||0;
        if(jour&&l.cle){ const qAp=Math.max(0,qAv-q); l.qAv=qAv; l.qAp=qAp; l.manque=(q>qAv)?q-qAv:undefined; if(qAp!==qAv){ pcPose(l.cle,qAp); nSorties+=qAv-qAp; } }
        else { l.qAv=qAv; l.qAp=qAv; delete l.manque; }
        l.pc=true; });
      f.pc=true; f.stock=!!jour; delete f.doc; delete f.remiseCaisse;
      f.note=jour?'Commande Shopify de Perfume City':'Commande Shopify d\'avant la liaison : aucun stock touché';
      nV++; });
    retours.forEach(f=>{
      const o2=FACT.find(z=>z&&z.sens==='vente'&&!z.retour&&z.num===String(f.refNum||'')&&z.auto==='shopify-pc')||null;
      const rendre=!!(o2&&o2.stock!==false);
      (f.lignes||[]).forEach(l=>{ if(!l) return; const n=Math.abs(+l.q||0), qAv=l.cle?pcQ(l.cle):0; let qAp=qAv;
        if(rendre&&l.cle){ const lo=(o2.lignes||[]).find(z=>z.cle===l.cle); qAp=qAv+Math.min(n,Math.max(0,lo?+lo.q||0:0)); if(qAp!==qAv){ pcPose(l.cle,qAp); nSorties-=qAp-qAv; } }
        l.qAv=qAv; l.qAp=qAp; l.pc=true; });
      f.pc=true; f.stock=rendre; f.note='Perfume City (Shopify)'+(o2?(rendre?'':' — vente d\'avant la liaison, aucun stock touché'):" — vente d'origine inconnue ici, stock inchangé");
      nR++; });
    if(touche) pcsSauve(R);
    nV+=dejaPC.length;
    ecrit('fiches-modifiees-v1',MOD); ecrit('factures-v1',FACT);
    const J=lit('crm-journal-v1',[])||[]; const par=(typeof NOM_UTIL==='string'&&NOM_UTIL)?NOM_UTIL:'(automatique)';
    J.push({t:new Date().toISOString(),u:par,act:'stock',lib:'réparation : '+nV+' vente'+(nV>1?'s':'')+' et '+nR+' retour'+(nR>1?'s':'')+' Shopify de Perfume City, rangés par erreur dans le stock central, remis comme avant ; factures DASY automatiques retirées ; '+(nSorties>0?nSorties+' flacon(s) sortis':'aucun flacon sorti')+' de l\'inventaire Perfume City',ref:'',av:null,ap:'',n:0,det:[]});
    ecrit('crm-journal-v1',J);
    return nV+nR;
  }catch(e){ try{ console.error('réparation Perfume City :',e); }catch(_){} return 0; }
}
window.faReparePC=faReparePC;

function fileAuto(){
  const rien={faites:0,restent:0,mt:0,ecarts:[],exp:0};
  try{
    if(typeof D_TOUS!=='function'||typeof lit!=='function'||typeof ecrit!=='function') return rien;
    if(typeof session==='function'&&!session()) return rien;      /* pas de session : on ne touche à rien */
    faReparePC();                                                  /* avant tout : ce que d'anciennes pages ont mal rangé */
    const F=lit(FA_KFILE,[]); if(!Array.isArray(F)||!F.length) return rien;
    faInscritClients(F);
    const C=faContexte();
    /* ce qu'on peut faire, vente par vente */
    const A=[], EXP=[], ANN=[], ILL=[], SVC=[];
    /* une ligne sans code lisible ET sans nom (un email de retour Amazon mal lu :
       code « Return », rien d'autre) ne pourra jamais être rattachée : elle sort
       de la file, avec une ligne de journal, au lieu d'y rester « à identifier » */
    const codeLisible=c=>/\d{8}|^B0[A-Z0-9]{8}$/i.test(String(c||'').trim());
    const illisible=v=>Array.isArray(v.lignes)&&v.lignes.length&&v.lignes.every(l=>!codeLisible(l.bc)&&!codeLisible(l.sku)&&!/[a-zà-ÿ]{3}/i.test(String(l.des||'')));
    /* Une vente déjà facturée (même canal, même numéro) qui revient — un rattrapage,
       une boîte relue — ne doit pas sortir le stock une deuxième fois. */
    let FA0=[]; try{ FA0=lit('factures-v1',[])||[]; }catch(e){}
    const dejaFact=new Set((Array.isArray(FA0)?FA0:[]).filter(f=>f&&f.auto&&!f.retour).map(f=>f.auto+'|'+f.num));
    const DEJA=[];
    F.forEach(v=>{
      if(v&&v.src==='shopify-pc'&&(typeof pcsRows!=='function'||typeof pcsSauve!=='function')) return;   /* jamais contre le stock central */
      if(v&&!v.annule&&v.src&&v.num&&dejaFact.has(v.src+'|'+v.num)){ DEJA.push(v); return; }
      if(v&&illisible(v)){ ILL.push(v); return; }
      if(v&&!v.annule&&Array.isArray(v.lignes)&&v.lignes.length&&!faSansService(v).lignes.length){ SVC.push(v); return; }
      const L=C.resout(v); if(!L) return;                  /* une inconnue : toute la vente attend */
      if(v.annule) ANN.push({v,L});
      else if(faExpedie(v.src)) EXP.push({v,L});
      else A.push({v,L});
    });
    if(!A.length&&!EXP.length&&!ANN.length&&!ILL.length&&!DEJA.length&&!SVC.length) return Object.assign(rien,{restent:F.length});
    const faits=[]; const J=lit('crm-journal-v1',[])||[]; let nAnn=0;
    if(DEJA.length){ DEJA.forEach(v=>faits.push(v._i));
      J.push({t:new Date().toISOString(),u:C.par,act:'vente',lib:DEJA.length+' vente'+(DEJA.length>1?'s':'')+' reçue'+(DEJA.length>1?'s':'')+' une deuxième fois, déjà facturée'+(DEJA.length>1?'s':'')+' — ignorée'+(DEJA.length>1?'s':'')+' (n° '+DEJA.map(v=>v.num).slice(0,6).join(', ')+')',ref:'',av:null,ap:null}); nAnn++; }
    if(ILL.length){ ILL.forEach(v=>faits.push(v._i));
      J.push({t:new Date().toISOString(),u:C.par,act:'vente',lib:ILL.length+' message'+(ILL.length>1?'s':'')+' de canal sans produit lisible ('+[...new Set(ILL.map(v=>FA_SRC[v.src]||v.src))].join(', ')+') retiré'+(ILL.length>1?'s':'')+' de la file — n° '+ILL.map(v=>v.num||'?').slice(0,6).join(', ')+(ILL.length>6?'…':''),ref:'',av:null,ap:null}); nAnn++; }
    if(SVC.length){ SVC.forEach(v=>faits.push(v._i));
      J.push({t:new Date().toISOString(),u:C.par,act:'vente',lib:SVC.length+' vente'+(SVC.length>1?'s':'')+' sans parfum ('+SVC.map(v=>(v.lignes||[]).map(l=>(l.des||'?')+' ×'+(l.q||1)).join(', ')).slice(0,4).join(' ; ')+') — rien à sortir du stock, retirée'+(SVC.length>1?'s':'')+' de la file',ref:'',av:null,ap:null}); nAnn++; }
    /* les annulations : d'abord celles d'une commande encore à expédier */
    ANN.forEach(x=>{ if(faAnnuleAvantExp(x.v,J,C.par)){ faits.push(x.v._i); nAnn++; } else A.push(x); });
    if(nAnn) ecrit('crm-journal-v1',J);
    /* les commandes à expédier : elles attendent le geste de quelqu'un */
    if(EXP.length){
      const E=faLitExp(); const t=new Date().toISOString();
      EXP.forEach(x=>{ const v=x.v;
        if(E.some(e=>e._i===v._i)) { faits.push(v._i); return; }
        E.push({_i:v._i,src:v.src,num:v.num||'',client:faNomClient(v.client),email:v.email||undefined,tel:v.tel||undefined,ville:v.ville||undefined,pays:v.pays||undefined,d:v.d||C.jour(),h:v.h||'',recu:v.recu||'',total:v.total==null?null:+v.total,hors:v.hors||0,lieu:v.lieu||'',port:+v.port>0?+v.port:undefined,
          lignes:x.L.map(l=>({cle:l.cle,bc:l.bc,des:l.des,q:l.q,p:l.p,ref:C.nomDe(l.cle)})),
          montant:x.L.reduce((a,l)=>a+l.q*(l.p||0),0),arrive:t,statut:'attente'});
        faits.push(v._i); });
      ecrit(FA_KEXP,E);
      const J2=lit('crm-journal-v1',[])||[];
      J2.push({t,u:C.par,act:'vente',lib:EXP.length+' commande'+(EXP.length>1?'s':'')+' à expédier reçue'+(EXP.length>1?'s':'')+' ('+[...new Set(EXP.map(x=>FA_SRC[x.v.src]||x.v.src))].join(', ')+') — le stock sortira à l\'expédition',ref:'',av:null,ap:Math.round(EXP.reduce((a,x)=>a+x.L.reduce((b,l)=>b+l.q*(l.p||0),0),0))+' $'});
      ecrit('crm-journal-v1',J2);
    }
    const resteApres=F.length-faits.length-A.length;
    const r=faEnregistre(A,C,{suite:resteApres>0?', '+resteApres+' en attente (référence inconnue)':''});
    faits.push(...r.faites);
    const reste=F.filter(v=>!faits.includes(v._i));
    ecrit(FA_KFILE,reste);
    return {faites:faits.length,ventes:r.ventes,retours:r.retours,restent:reste.length,mt:r.mt,ecarts:r.ecarts,exp:EXP.length};
  }catch(e){ try{ console.error('enregistrement automatique :',e); }catch(_){} return rien; }
}

/* « Expédiée le … » : LE geste qui fait la facture et sort les flacons.
   o = {d:'AAAA-MM-JJ', suivi:'', transporteur:''}. Renvoie la facture faite, ou null. */
function faExpedier(id,o){
  o=o||{};
  const E=faLitExp(); const e=E.find(x=>x._i===id&&x.statut==='attente'); if(!e) return null;
  const C=faContexte();
  const L=e.lignes.map(l=>({cle:C.cleDe(l),bc:l.bc,des:l.des,q:+l.q||0,p:l.p==null?null:+l.p})).filter(l=>l.q);
  if(!L.length||L.some(l=>!l.cle)) return null;      /* une référence a disparu du catalogue : on ne devine pas */
  const exp={d:o.d||C.jour(),t:new Date().toISOString(),par:C.par,suivi:String(o.suivi||'').trim(),transporteur:String(o.transporteur||'').trim()};
  if(o.auto) exp.auto=true;
  let port=e.port; if(port==null){ const st=faStatutSite(e.src,e.num); if(st&&+st.port>0) port=+st.port; }
  const v={_i:e._i,src:e.src,num:e.num,client:e.client,d:e.d,h:e.h,lieu:e.lieu,recu:e.recu,arrive:e.arrive,total:e.total,hors:e.hors,port};
  const r=faEnregistre([{v,L}],C,{exp,lib:o.lib||('commande '+(e.num||'')+' expédiée le '+exp.d.replace(/^(\d{4})-(\d{2})-(\d{2}).*$/,'$2/$3/$1')+' ('+(FA_SRC[e.src]||e.src)+') — facture faite, stock sorti'+(o.auto?' (marquée « completed » sur le site)':''))});
  if(!r.ventes) return null;
  e.statut='expedie'; e.exp=exp; e.factId=r.ids[0]||'';
  /* l'historique des expédiées ne grossit pas sans fin */
  const faites=E.filter(x=>x.statut==='expedie').sort((a,b)=>String(a.exp&&a.exp.t||'').localeCompare(String(b.exp&&b.exp.t||'')));
  if(faites.length>300) faites.slice(0,faites.length-300).forEach(x=>{ const i=E.indexOf(x); if(i>=0) E.splice(i,1); });
  ecrit(FA_KEXP,E);
  return {fact:r.ids[0]||'',ecarts:r.ecarts,mt:r.mt};
}
/* retirer une commande à expédier sans l'expédier (annulée au téléphone, doublon…) */
function faRetireExp(id,motif){
  const E=faLitExp(); const i=E.findIndex(x=>x._i===id&&x.statut==='attente'); if(i<0) return false;
  const e=E[i]; E.splice(i,1); ecrit(FA_KEXP,E);
  const J=lit('crm-journal-v1',[])||[]; const par=(typeof NOM_UTIL==='string'&&NOM_UTIL)?NOM_UTIL:'(non renseigné)';
  J.push({t:new Date().toISOString(),u:par,act:'annulation',lib:'commande '+(e.num||'')+' retirée des expéditions sans être expédiée'+(motif?' — '+motif:'')+' — rien n\'est sorti du stock',n:0,impact:Math.round(e.montant||0),det:[]});
  ecrit('crm-journal-v1',J);
  return true;
}
window.faStatutSite=faStatutSite; window.faEnregistre=faEnregistre; window.faContexte=faContexte; window.faExpedier=faExpedier; window.faRetireExp=faRetireExp; window.faLitExp=faLitExp; window.faCanauxExp=faCanauxExp; window.faExpedie=faExpedie; window.faAnnuleAvantExp=faAnnuleAvantExp;
/* à l'ouverture de la page, avant son propre code */
/* ---- les heures Amazon d'avant le 25 sept. 2026, remises à l'heure de Miami ----
   Jusqu'au cockpit ck28, l'heure d'une commande Amazon était celle de l'email, en temps
   universel : 4 h de trop (Igal : « tu me dis 10 h 42, moi je vois 10 h 38 » — la
   commande de 06:38 à Miami s'affichait 10:38, déposée à 06:42). On corrige une fois,
   chaque ligne marquée `hM` pour ne jamais la décaler deux fois, même sur deux postes.
   Une heure proche de celle du dépôt en temps universel est une heure UTC ; une heure
   déjà à ~4 h de là est déjà celle de Miami et ne bouge pas. */
const FA_CUT_H='2026-09-25T12:52:30Z';
function faMoinsFuseau(d,h){
  const m=String(h||'').match(/^(\d{1,2}):(\d{2})$/); if(!m) return null;
  let mn=(+m[1])*60+(+m[2])-4*60, j=String(d||'');
  if(mn<0){ mn+=1440; const t=new Date(j+'T12:00:00Z'); if(!isNaN(t)){ t.setUTCDate(t.getUTCDate()-1); j=t.toISOString().slice(0,10); } }
  return {d:j, h:String(Math.floor(mn/60)).padStart(2,'0')+':'+String(mn%60).padStart(2,'0')};
}
function faEstUTC(h,recu){
  const m=String(h||'').match(/^(\d{1,2}):(\d{2})$/), r=String(recu||'').match(/T(\d{2}):(\d{2})/);
  if(!m||!r) return null;
  let e=Math.abs(((+r[1])*60+(+r[2]))-((+m[1])*60+(+m[2]))); e=Math.min(e,1440-e);
  return e<=150;       /* l'email et le dépôt : quelques minutes, pas 4 heures */
}
function faHeuresMiami(){
  try{
    if(typeof lit!=='function'||typeof ecrit!=='function') return;
    if(typeof session==='function'&&!session()) return;
    const fixe=(o,avant)=>{ if(!o||o.hM||!o.h) return false; if(!avant) return false; const n=faMoinsFuseau(o.d,o.h); if(!n) return false; o.d=n.d; o.h=n.h; o.hM=1; return true; };
    const utcQ=o=>{ const u=faEstUTC(o.h,o.recu); if(u!==null) return u; const r=String(o.recu||o.arrive||''); return !!r&&r<FA_CUT_H; };   /* sans date de dépôt : on ne sait pas, on ne touche pas */
    let F=lit(FA_KFILE,[]); if(Array.isArray(F)){ let c=false; F.forEach(v=>{ if(v&&v.src==='amazon'&&fixe(v,utcQ(v))) c=true; }); if(c) ecrit(FA_KFILE,F); }
    let E=faLitExp(); { let c=false; E.forEach(e=>{ if(e&&e.src==='amazon'&&fixe(e,utcQ(e))) c=true; }); if(c) ecrit(FA_KEXP,E); }
    let X=lit('factures-v1',[]); if(Array.isArray(X)){ let c=false; X.forEach(f=>{ if(f&&f.auto==='amazon'&&fixe(f,String(f.t||'')<FA_CUT_H)) c=true; }); if(c) ecrit('factures-v1',X);
      /* l'historique par parfum garde la même heure que la facture */
      const nums=new Set(X.filter(f=>f&&f.auto==='amazon'&&f.hM).map(f=>String(f.num)));
      const V=lit('ventes-v1',{})||{}; let cv=false;
      Object.keys(V).forEach(k=>(V[k]||[]).forEach(x=>{ if(x&&x.k==='Amazon'&&nums.has(String(x.num||'').replace(/ \(remboursé\)$/,''))&&fixe(x,true)) cv=true; }));
      if(cv) ecrit('ventes-v1',V); }
  }catch(e){ try{ console.error('heures Amazon :',e); }catch(_){} }
}
faHeuresMiami();
/* Igal, 28 sept. 2026 : « les commandes n'arrivent pas dans l'ordre, il y en a une avant l'autre ».
   Cause trouvée dans ses données : une commande Amazon passée entre minuit et 3 h du matin
   à Miami porte, dans l'email d'Amazon, la date de la côte Ouest — la VEILLE. L'heure, elle,
   était bien celle de Miami. « 26/09 à 00:01 » se rangeait donc tout en bas du 26 au lieu
   d'être en haut du 27. On la remet au bon jour, une fois : la date de dépôt par le cockpit
   (quelques minutes après l'email) doit tomber le lendemain de la date lue, sinon on ne
   touche à rien — c'est ce qui rend la correction sans risque de la refaire deux fois. */
function faJoursAmazon(){
  try{
    if(typeof lit!=='function'||typeof ecrit!=='function'||typeof jourMiami!=='function') return;
    if(typeof session==='function'&&!session()) return;
    const plus1=d=>{ const t=new Date(String(d)+'T12:00:00Z'); if(isNaN(t)) return ''; t.setUTCDate(t.getUTCDate()+1); return t.toISOString().slice(0,10); };
    const fixe=o=>{ if(!o||!o.d||!/^0[0-2]:\d{2}$/.test(String(o.h||''))||!o.recu) return false;
      const jm=jourMiami(o.recu); if(!jm||jm!==plus1(o.d)) return false; o.d=jm; return true; };
    const bon={};                                  /* numéro de commande → le bon jour */
    let F=lit(FA_KFILE,[]); if(Array.isArray(F)){ let c=false; F.forEach(v=>{ if(v&&v.src==='amazon'){ if(fixe(v)) c=true; bon[String(v.num)]={d:v.d,h:v.h}; } }); if(c) ecrit(FA_KFILE,F); }
    let E=faLitExp(); { let c=false; E.forEach(e=>{ if(e&&e.src==='amazon'){ if(fixe(e)) c=true; bon[String(e.num)]={d:e.d,h:e.h}; } }); if(c) ecrit(FA_KEXP,E); }
    /* la facture et l'historique par parfum suivent la commande, à heure égale */
    let X=lit('factures-v1',[]); if(Array.isArray(X)){ let c=false;
      X.forEach(f=>{ if(!f||f.auto!=='amazon') return; const b=bon[String(f.num||'').replace(/-R\d+$/,'')]; if(b&&b.h&&f.h===b.h&&f.d!==b.d){ f.d=b.d; c=true; } });
      if(c) ecrit('factures-v1',X); }
    const V=lit('ventes-v1',{})||{}; let cv=false;
    Object.keys(V).forEach(k=>(V[k]||[]).forEach(x=>{ if(!x||x.k!=='Amazon') return; const b=bon[String(x.num||'').replace(/ \(remboursé\)$/,'')]; if(b&&b.h&&x.h===b.h&&x.d!==b.d){ x.d=b.d; cv=true; } }));
    if(cv) ecrit('ventes-v1',V);
  }catch(e){ try{ console.error('jours Amazon :',e); }catch(_){} }
}
faJoursAmazon();
/* 8 oct. 2026 (Igal : « 3 × 417 $ — erreur, pourquoi multiplié par 3 ? »). Deux ventes Amazon à plusieurs
   flacons avaient été entrées avec le TOTAL de la ligne comme prix d'un flacon : Hanae Mori EDT ×2 (266 $ au lieu de
   2 × 133 $) et Hanae Mori EDP ×3 (417 $ au lieu de 3 × 139 $). Les 154 ventes Amazon ont été passées en revue :
   ce sont les deux seules lignes à plusieurs flacons. On les remet au prix d'un flacon, une fois (marque `puFix`) :
   la facture, son total, l'historique par parfum. Le stock n'a pas bougé (la quantité était juste). */
function faPrixAmazonTotal(){
  try{
    if(typeof lit!=='function'||typeof ecrit!=='function') return;
    if(typeof session==='function'&&!session()) return;
    const NUMS={'111-3516935-9401028':1,'114-7638431-2221805':1};
    const X=lit('factures-v1',[]); if(!Array.isArray(X)) return;
    const R=Math.round; let c=false; const fait=[];
    X.forEach(f=>{
      if(!f||f.auto!=='amazon'||f.retour||f.puFix||!NUMS[String(f.num)]) return;
      let touche=false;
      (f.lignes||[]).forEach(l=>{ const q=Math.abs(+l.q); if(q>1&&l.p!=null&&!l.pu){ l.pAvFix=l.p; l.p=R(+l.p/q*100)/100; l.pu=1; touche=true; } });
      if(!touche) return;
      f.puFix=1; f.montant=R((f.lignes||[]).reduce((a,l)=>a+(+l.q||0)*(+l.p||0),0)*100)/100;
      const d=f.doc; if(d&&typeof d==='object'){ const m=f.montant; d.sousTotal=m; d.base=m; d.total=m; d.regle=m; d.reste=0; }
      f.note=((f.note||'')+" prix corrigé le 8 oct. 2026 : Amazon donne le total de la ligne, pas le prix d'un flacon").trim();
      c=true; fait.push(f);
    });
    if(!c) return;
    ecrit('factures-v1',X);
    const V=lit('ventes-v1',{})||{}; let cv=false;
    Object.keys(V).forEach(k=>(V[k]||[]).forEach(x=>{ if(!x||x.k!=='Amazon'||x.puFix) return; const f=fait.find(z=>String(z.num)===String(x.num||'')); if(!f) return;
      const l=(f.lignes||[]).find(z=>('b'+z.bc===k)||z.cle===k); if(l&&Math.abs(+x.q)>1){ x.p=l.p; x.puFix=1; cv=true; } }));
    if(cv) ecrit('ventes-v1',V);
    const J=lit('crm-journal-v1',[])||[];
    J.push({t:new Date().toISOString(),u:'(automatique)',act:'vente',lib:'prix de '+fait.length+' vente(s) Amazon à plusieurs flacons corrigés — Amazon donne le total de la ligne : '+fait.map(f=>f.num).join(', '),ref:'',av:null,ap:null});
    ecrit('crm-journal-v1',J);
  }catch(e){ try{ console.error('prix Amazon :',e); }catch(_){} }
}
faPrixAmazonTotal();
/* 20 oct. 2026 : en ligne, la file ne s'enregistre plus à l'ouverture sur la copie de ce navigateur — elle passe
   par le serveur (voir _serveur.py, __syTraiteFile) : un seul onglet, et le stock relu à l'instant. Le serveur
   injoignable à l'ouverture (window.__CK.hors) : rien n'est enregistré, les ventes attendent, intactes. */
(function(){
  let enL=false; try{ enL=!!(window.__CK&&window.__CK.enLigne&&localStorage.getItem('ck-token')); }catch(e){}
  if(!enL){ window.__FILE_AUTO=fileAuto(); return; }
  setTimeout(()=>{ try{ if(typeof window.__syTraiteFile==='function') window.__syTraiteFile(); }catch(e){} },1200);
})();
/* ---- Statut shipping (Igal, 28 sept. 2026) ----
   Le cockpit relit l'état des commandes des deux sites (site-statuts-v1 : processing,
   completed, cancelled…). Une commande du site encore « à expédier » ici et marquée
   « completed » sur WooCommerce EST partie : on fait ce que le bouton « Expédiée »
   aurait fait (facture, stock sorti), daté du jour où le site l'a terminée. Annulée ou
   remboursée sur le site avant d'être partie : elle sort de la liste, rien ne bouge. */
function faStatutsSites(){
  const out={exp:0,ret:0};
  try{
    if(typeof D_TOUS!=='function'||typeof lit!=='function'||typeof ecrit!=='function') return out;
    if(typeof session==='function'&&!session()) return out;
    const S=lit(FA_KST,{}); if(!S||typeof S!=='object'||Array.isArray(S)) return out;
    faLitExp().filter(e=>e&&e.statut==='attente'&&/^woocommerce/.test(String(e.src||''))).forEach(e=>{
      const s=S[e.src+'|'+e.num]; if(!s) return;
      if(s.st==='completed'){
        const d=(/^\d{4}-\d{2}-\d{2}/.test(String(s.fini||''))?String(s.fini).slice(0,10):'')||(typeof jourMiami==='function'?jourMiami():'');
        if(faExpedier(e._i,{d,auto:true})) out.exp++;
      } else if(/^(cancelled|refunded|failed)$/.test(String(s.st))){
        if(faRetireExp(e._i,'annulée sur le site (WooCommerce : '+s.st+')')) out.ret++;
      }
    });
  }catch(e){ try{ console.error('statuts des sites :',e); }catch(_){} }
  return out;
}
window.__FA_STATUTS=faStatutsSites();
/* La mise en veille vide la liste : les commandes qui attendaient d'être marquées « expédiées »
   sortent du stock maintenant, datées du jour de la vente (c'est ce jour-là qu'elles ont été
   vendues). Une commande dont un parfum n'est plus reconnu reste : elle ne se devine pas. */
function faVeilleExp(){
  const out={n:0,reste:0};
  try{
    if(!FA_EXP_VEILLE) return out;
    if(typeof D_TOUS!=='function'||typeof lit!=='function'||typeof ecrit!=='function') return out;
    if(typeof session==='function'&&!session()) return out;
    faLitExp().filter(e=>e&&e.statut==='attente').forEach(e=>{
      const d=/^\d{4}-\d{2}-\d{2}$/.test(String(e.d||''))?e.d:'';
      const r=faExpedier(e._i,{d,auto:true,lib:'commande '+(e.num||'')+' ('+(FA_SRC[e.src]||e.src)+') — stock sorti à la vente (Statut shipping en veille), facture faite'});
      if(r) out.n++; else out.reste++;
    });
  }catch(e){ try{ console.error('veille des expéditions :',e); }catch(_){} }
  return out;
}
window.__FA_VEILLE=faVeilleExp();
"""
