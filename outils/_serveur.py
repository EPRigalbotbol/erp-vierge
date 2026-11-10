# -*- coding: utf-8 -*-
"""Les données de l'entreprise sur le serveur (le cockpit), et plus seulement dans le navigateur.

Avant : chaque navigateur avait SON stock, SES ventes, SON journal. Quatre comptes, quatre
vérités. Et vider le navigateur effaçait tout.

Maintenant, en ligne :
  1. AMORCE — avant que la page ne lise quoi que ce soit, on demande au cockpit ce qui a changé
     depuis la dernière visite (on lui envoie les versions qu'on connaît, il ne renvoie que le
     reste) et on le pose dans le navigateur, qui reste la copie de travail.
  2. SYNC — chaque `ecrit()` part au serveur avec le numéro de version sur lequel on s'appuie.
     Si quelqu'un a écrit entre-temps, le serveur refuse, renvoie sa version, et on fusionne ici
     (la même fusion qu'entre deux onglets) avant de renvoyer.
  3. Toutes les 45 s, on regarde si quelqu'un d'autre a écrit ; si oui on met la copie locale à
     jour et on propose de recharger.
En local (fichier, localhost), rien de tout ceci ne s'active : SAM marche comme avant.
"""

# Magasins qui restent propres à l'appareil (préférences d'affichage, session, clés API…).
EXCLUS = ['sam-session-v1', 'ck-token', 'ck-versions', 'crm-utilisateur-v1', 'crm-utilisateurs-v1',
          'sam-comptes-v1', 'sam-roles-v1', 'sam-comptes-demo-v1', 'frn-demo-galou-v1',
          'vue-catalogue-v1', 'tri-colonne-v1', 'retail-vue-v1', 'langue-v1',
          'dossier-outil-v1', 'repere-installation-v1', 'derniere-sauvegarde-v1',
          'derniere-sauvegarde-compte-v1', 'connecteurs-v1']

# Le GRENIER : les gros magasins quittent localStorage (5 Mo par site, plein chez Sam le 17 octobre 2026)
# pour IndexedDB (des gigaoctets), sans que le code des pages ne change d'une ligne.
GRENIER = r"""
<script>/* ============ LE GRENIER (17 oct. 2026) ============
   La mémoire « localStorage » d'un navigateur est limitée à 5 Mo par site. Le 17 octobre, celle de Sam était PLEINE
   (relevé des sites 1,1 Mo, factures 1 Mo, journal 0,75 Mo, devis 0,8 Mo…) : « This browser's storage is full », les
   dernières données n'étaient plus rangées, et la page travaillait sur une copie périmée. Les GROS magasins (24 Ko et
   plus) vont désormais au grenier : IndexedDB, qui offre des gigaoctets.
   Pour que RIEN ne change pour le code des pages — il lit et écrit localStorage, de façon synchrone — chaque gros
   magasin est gardé en mémoire vive dès l'ouverture de la page, et localStorage est doublé : getItem, setItem,
   removeItem, key et length répondent pour les deux endroits à la fois. Le grenier est chargé AVANT que la page ne
   démarre (voir l'AMORCE, qui attend window.__GRENIER). Entre deux onglets, un canal (BroadcastChannel) rejoue
   l'événement « storage » que le navigateur n'envoie plus pour ces magasins. Au premier passage, ce qui était gros
   dans localStorage déménage au grenier : la place se libère d'elle-même. */
(function(){
  const SEUIL=24*1024, MEM=new Map(); let DB=null, CANAL=null;
  const P=Storage.prototype, N={get:P.getItem,set:P.setItem,rem:P.removeItem,key:P.key,len:Object.getOwnPropertyDescriptor(P,'length').get};
  const local=s=>{ try{ return s===window.localStorage; }catch(e){ return false; } };
  /* 27 oct. 2026 : écriture « relaxed » (pas d'attente du disque) : avec plusieurs onglets ouverts qui rangent les mêmes gros
     magasins toutes les quelques secondes, les écritures s'empilaient et la lecture d'un nouvel onglet attendait derrière elles */
  const range=(k,v)=>{ if(!DB) return; try{ DB.transaction('m','readwrite',{durability:'relaxed'}).objectStore('m').put(v,k); }catch(e){ try{ DB.transaction('m','readwrite').objectStore('m').put(v,k); }catch(_){} } };
  const efface=(k)=>{ if(!DB) return; try{ DB.transaction('m','readwrite').objectStore('m').delete(k); }catch(e){} };
  const annonce=(k)=>{ try{ if(CANAL) CANAL.postMessage({k}); }catch(e){} };
  P.getItem=function(k){ if(local(this)){ const s=String(k); if(MEM.has(s)) return MEM.get(s); } return N.get.call(this,k); };
  P.setItem=function(k,v){ if(!local(this)) return N.set.call(this,k,v); const s=String(k), t=String(v);
    if(MEM.has(s)||t.length>=SEUIL){ if(MEM.get(s)===t) return; MEM.set(s,t); range(s,t); try{ if(N.get.call(this,s)!=null) N.rem.call(this,s); }catch(e){} annonce(s); return; }
    return N.set.call(this,k,v); };
  P.removeItem=function(k){ if(local(this)){ const s=String(k); if(MEM.has(s)){ MEM.delete(s); efface(s); annonce(s); } } return N.rem.call(this,k); };
  P.key=function(i){ if(local(this)){ const n=N.len.call(this); if(i>=n){ const ks=[...MEM.keys()]; return i-n<ks.length?ks[i-n]:null; } } return N.key.call(this,i); };
  Object.defineProperty(P,'length',{configurable:true,get(){ const n=N.len.call(this); return local(this)?n+MEM.size:n; }});
  const evt=(k)=>{ try{ window.dispatchEvent(new StorageEvent('storage',{key:k,storageArea:window.localStorage})); }catch(e){} };
  window.__GRENIER=new Promise(res=>{
    /* 27 oct. 2026 (Igal : « la rubrique Sales est vide ») : un onglet de l'ERP resté ouvert peut tenir le grenier sans le
       rendre ; la lecture attendait alors sans fin et la page restait blanche. Au bout de 2,5 s on démarre sans lui : ce qui
       manque est redemandé au serveur (verifCopies), et une lecture tardive du grenier n'écrase plus rien. */
    let FINI=false;
    const fini=(ok)=>{ if(FINI) return; FINI=true; res(ok);
      /* ce qui vient d'arriver du grenier : le menu (pastilles) a pu lire « rien » avant, on le prévient */
      try{ for(const k of MEM.keys()) evt(k); }catch(e){} };
    try{
      const q=indexedDB.open('sam-grenier',1);
      q.onupgradeneeded=()=>{ try{ q.result.createObjectStore('m'); }catch(e){} };
      q.onerror=()=>fini(false); q.onblocked=()=>fini(false);
      q.onsuccess=()=>{ DB=q.result;
        try{ CANAL=new BroadcastChannel('sam-grenier'); CANAL.onmessage=(m)=>{ const k=m&&m.data&&m.data.k; if(!k) return;
          try{ const r=DB.transaction('m','readonly').objectStore('m').get(k); r.onsuccess=()=>{ if(typeof r.result==='string') MEM.set(k,r.result); else MEM.delete(k); evt(k); }; }catch(e){} }; }catch(e){}
        let rk, rv;
        try{ const t=DB.transaction('m','readonly').objectStore('m'); rk=t.getAllKeys(); rv=t.getAll(); }catch(e){ fini(false); return; }
        rv.onerror=()=>fini(false);
        rv.onsuccess=()=>{ if(FINI) return; const ks=rk.result||[], vs=rv.result||[];
          ks.forEach((k,i)=>{ if(typeof vs[i]==='string') MEM.set(String(k),vs[i]); });
          /* déménagement : ce qui est gros dans localStorage part au grenier (une fois ; la place se libère) */
          try{ const L=window.localStorage, n=N.len.call(L), gros=[];
            for(let i=0;i<n;i++){ const k=N.key.call(L,i); const v=N.get.call(L,k); if(v!=null&&(MEM.has(k)||v.length>=SEUIL)) gros.push([k,v]); }
            gros.forEach(([k,v])=>{ if(!MEM.has(k)){ MEM.set(k,v); range(k,v); } N.rem.call(L,k); });
          }catch(e){}
          fini(true); };
      };
    }catch(e){ fini(false); }
    setTimeout(()=>{ if(!FINI){ window.__GRENIER_KO=true; try{ console.warn('grenier bloqué par un autre onglet : démarrage sans lui'); }catch(e){} fini(false); } },2500);
  });
})();</script>
"""

# Ce qui tourne AVANT le code de la page : on remplit le navigateur depuis le serveur, puis on lance la page.
AMORCE = r"""
(function(){
  const url=(typeof COCKPIT_URL!=='undefined'&&COCKPIT_URL)||'https://cockpit.igalbotbol.com';
  const org=(typeof COCKPIT_ORG!=='undefined'&&COCKPIT_ORG)||'dasy';
  const enLigne=location.protocol!=='file:' && !/^(localhost|127\.0\.0\.1|\[::1\])$/.test(location.hostname);
  let tok=''; try{ tok=localStorage.getItem('ck-token')||''; }catch(e){}
  const K_V='ck-versions';
  window.__CK={url,org,enLigne,hors:false,charge:null};
  function lance(){
    /* dossier « donnees » absent : le garde-fou a déjà écrit l'explication, on ne démarre pas */
    if(window.__DONNEES_MANQUENT) return;
    /* la page s'attendait à démarrer avec le document : on rejoue ces événements pour elle */
    const ael=document.addEventListener.bind(document), wael=window.addEventListener.bind(window);
    document.addEventListener=function(t,f,o){ if(t==='DOMContentLoaded'&&document.readyState!=='loading'){ setTimeout(()=>f.call(document,new Event('DOMContentLoaded')),0); } else ael(t,f,o); };
    window.addEventListener=function(t,f,o){ if((t==='load'&&document.readyState==='complete')||(t==='DOMContentLoaded'&&document.readyState!=='loading')){ setTimeout(()=>f.call(window,new Event(t)),0); } else wael(t,f,o); };
    const src=document.getElementById('page-js'); const s=document.createElement('script');
    /* un module ne signale pas sa fin (pas d'événement load sur un script en ligne) : il
       l'annonce lui-même, en dernière ligne — sinon la page attendait le délai de secours,
       2,5 s de blanc à chaque ouverture (Igal, 12 sept. 2026 : « les invoices mettent du
       temps à se charger »). */
    const montre=()=>{ try{ document.documentElement.classList.remove('pg-attente'); }catch(e){} };
    window.__pgMontre=()=>setTimeout(montre,0);
    s.textContent=src.textContent+(src.dataset.module?'\n;try{window.__pgMontre();}catch(e){}':'');
    if(src.dataset.module) s.type='module'; src.remove(); document.body.appendChild(s);
    /* La page se montre une fois dessinée, d'un seul coup. Avant, on voyait la coquille
       (titres, cadres vides), puis une demi-seconde plus tard le vrai contenu prenait sa
       place : « je vois une page, et d'un coup c'est une autre page » (Igal, 12 sept. 2026).
       Le setTimeout passe APRÈS les petits délais que le code de la page s'est donnés en
       démarrant ; un module, lui, ne tourne qu'au tour suivant : on attend qu'il ait tourné. */
    if(s.type==='module'){ s.addEventListener('error',montre); window.addEventListener('error',montre); setTimeout(montre,2500); }
    else setTimeout(montre,0);
  }
  /* le grenier (gros magasins en IndexedDB) doit être en mémoire avant tout : voir GRENIER */
  const grenier=(window.__GRENIER||Promise.resolve(false)).catch(()=>false);
  if(!enLigne||!tok){ grenier.then(lance); return; }
  let V={}; try{ V=JSON.parse(localStorage.getItem(K_V)||'{}')||{}; }catch(e){ V={}; }
  /* 30 sept. 2026 — la mémoire du navigateur (5 Mo par site) était PLEINE : une nouvelle
     version reçue ne pouvait plus être rangée, mais son numéro l'était quand même ; la page
     croyait être à jour et travaillait sur une copie périmée (les enregistrements de Sam ne
     partaient plus, une commande Amazon restait invisible). Désormais :
       - ce qui ne sert qu'au serveur (corbeille, sauvegardes, table des produits de la
         caisse, annonces Amazon) n'est plus gardé dans le navigateur ;
       - une version qui n'a pas pu être rangée n'est PAS notée : elle sera redemandée ;
       - une fois, tout est relu depuis le serveur, pour réparer les copies périmées. */
  const SEUL_SERVEUR=k=>/^(corbeille-v1|caisse-produits-v1|amazon-annonces-v1|amazon-illisibles)$|^sauvegarde-/.test(k);
  try{ Object.keys(localStorage).filter(SEUL_SERVEUR).forEach(k=>localStorage.removeItem(k)); }catch(e){}
  const K_RELU='ck-relu-20260930';
  try{ if(!localStorage.getItem(K_RELU)) V={}; }catch(e){}
  /* 13 oct. 2026 (Igal : « 8 secondes à attendre en passant du Catalogue à la Price list ») :
     ces magasins « serveur seulement » n'étaient jamais notés comme déjà lus, donc une page sur
     deux retéléchargeait ~4 Mo (dont une sauvegarde de 3 Mo) pour les jeter aussitôt. On note
     maintenant leur numéro de version à part (ck-versions-srv) et on le joint à la demande :
     le serveur ne les renvoie plus. Le numéro se met à jour à chaque relève (toutes les 8 s). */
  const K_VS='ck-versions-srv';
  let VS={}; try{ VS=JSON.parse(localStorage.getItem(K_VS)||'{}')||{}; }catch(e){ VS={}; }
  Object.keys(V).filter(SEUL_SERVEUR).forEach(k=>delete V[k]);
  const ctrl=new AbortController(); const tm=setTimeout(()=>ctrl.abort(),12000);
  const H={'Content-Type':'application/json',Authorization:'Bearer '+tok};
  /* première fois sur ce navigateur : on demande d'abord les numéros (quelques Ko) */
  /* 20 oct. 2026 : une copie qui a disparu (grenier vidé par le navigateur — Safari le fait —, page d'une
     ancienne version qui ne savait pas le lire…) ne doit jamais passer pour « à jour » parce que son numéro
     de version est resté noté : un magasin noté mais absent est redemandé en entier au serveur. */
  const verifCopies=()=>{ try{ Object.keys(V).forEach(k=>{ if(!SEUL_SERVEUR(k)&&localStorage.getItem(k)===null) delete V[k]; }); }catch(e){} };
  const avant=grenier.then(()=>{ verifCopies(); return Object.keys(VS).length?null:
    fetch(url+'/api/o/'+org+'/donnees/versions',{signal:ctrl.signal,headers:{Authorization:'Bearer '+tok}})
      .then(r=>r.ok?r.json():{}).then(v=>{ for(const k in v) if(SEUL_SERVEUR(k)) VS[k]=v[k]; }).catch(()=>{}); });
  avant.then(()=>fetch(url+'/api/o/'+org+'/donnees/lire',{method:'POST',signal:ctrl.signal,
    headers:H,body:JSON.stringify({versions:Object.assign({},V,VS)})}))
  .then(async r=>{
    clearTimeout(tm);
    if(r.status===401){
      try{ localStorage.removeItem('ck-token'); localStorage.removeItem('sam-session-v1'); }catch(e){}
      if(!/accueil\.html$/.test(location.pathname)){ location.replace('accueil.html'); return; }
      lance(); return;
    }
    if(!r.ok) throw new Error('serveur '+r.status);
    const j=await r.json();
    const vers=Object.assign({},j.versions||{}); let plein=false;
    { const vs={}; for(const k in vers) if(SEUL_SERVEUR(k)) vs[k]=vers[k]; try{ localStorage.setItem(K_VS,JSON.stringify(vs)); }catch(e){} }
    for(const k in j.magasins){ if(SEUL_SERVEUR(k)){ delete vers[k]; continue; }
      try{ localStorage.setItem(k,JSON.stringify(j.magasins[k].val)); }
      catch(e){ delete vers[k]; plein=true; try{ localStorage.removeItem(k); }catch(_){} } }
    Object.keys(vers).filter(SEUL_SERVEUR).forEach(k=>delete vers[k]);
    /* la relecture complète n'a lieu qu'une fois : si la mémoire est pleine, on avertit, mais on ne
       retélécharge pas tout à chaque page (les magasins non rangés n'ont pas de numéro : ils
       seront redemandés seuls) */
    if(plein) window.__CK.plein=true;
    try{ localStorage.setItem(K_RELU,'1'); }catch(e){}
    /* le menu de l'équipe a pu changer ailleurs : il avait déjà été posé avec l'ancien
       réglage de ce navigateur (il se dessine avant tout), on le repose avec le bon */
    if(j.magasins&&j.magasins['menu-perso-v1']){ try{ if(typeof mnApplique==='function') mnApplique(); }catch(e){} }
    (j.disparus||[]).forEach(k=>{ try{ localStorage.removeItem(k); }catch(e){} });
    try{ localStorage.setItem(K_V,JSON.stringify(vers)); }catch(e){}
    window.__CK.charge=vers;
    lance();
  })
  .catch(e=>{ clearTimeout(tm); window.__CK.hors=true; lance(); });
})();
"""

# Ce qui s'ajoute au code de la page, juste après les comptes : l'envoi au serveur.
SYNC = r"""
/* ============ EN LIGNE : LES DONNÉES VIVENT SUR LE SERVEUR ============ */
const _SY_EXCLUS=new Set(__EXCLUS__);
const _SY_ON=EN_LIGNE && !!ckTok();
const _SY_K='ck-versions';
let _SY_V={}; try{ _SY_V=JSON.parse(localStorage.getItem(_SY_K)||'{}')||{}; }catch(e){ _SY_V={}; }
const _SY_BASE={};          /* la valeur telle qu'on l'a reçue du serveur (point de comparaison pour fusionner) */
const _SY_ATT=new Map();    /* magasins en attente d'envoi : cle -> {val} */
const _SY_ENVOI=new Set();  /* envois en cours */
let _SY_HORS=!!(window.__CK&&window.__CK.hors);
const _sySauveV=()=>{ try{ localStorage.setItem(_SY_K,JSON.stringify(_SY_V)); }catch(e){} };
const _SY_SRV=k=>/^(corbeille-v1|caisse-produits-v1|amazon-annonces-v1|amazon-illisibles)$|^sauvegarde-/.test(k);   /* serveur seulement : jamais gardés ici */
const _SY_KVS='ck-versions-srv';
let _SY_VS={}; try{ _SY_VS=JSON.parse(localStorage.getItem(_SY_KVS)||'{}')||{}; }catch(e){ _SY_VS={}; }
const _syOk=cle=>_SY_ON && !_SY_EXCLUS.has(cle) && !_SY_SRV(cle) && /^[a-z0-9-]+-v\d+$/.test(cle);

/* on garde la version "serveur" de chaque magasin lu, pour savoir plus tard ce que CET appareil a changé */
{ const _lit0=lit; lit=(k,d)=>{ const v=_lit0(k,d); if(_syOk(k)&&!(k in _SY_BASE)) _SY_BASE[k]=_cp(v); return v; }; }

/* la mémoire du navigateur est pleine : on le DIT, en rouge, au lieu de travailler en silence
   sur des données périmées */
function _syPlein(){
  try{ if(document.getElementById('sy-plein')||!document.body) return;
    const b=document.createElement('div'); b.id='sy-plein';
    b.style.cssText='position:fixed;left:50%;top:10px;transform:translateX(-50%);z-index:9999;background:#8a2f2f;color:#fff;padding:10px 16px;border-radius:9px;font:600 13px Inter,system-ui,sans-serif;box-shadow:0 8px 24px rgba(0,0,0,.3);max-width:640px';
    b.textContent=(typeof L3==='function'?L3('⚠ La mémoire de ce navigateur est pleine : les dernières données ne sont pas à jour. Prévenez Igal.','⚠ This browser\'s storage is full: the latest data is not up to date. Tell Igal.','⚠ La memoria de este navegador está llena: los últimos datos no están al día. Avise a Igal.'):'⚠ La mémoire de ce navigateur est pleine.');
    document.body.appendChild(b); }catch(e){}
}
if(window.__CK&&window.__CK.plein) setTimeout(_syPlein,500);
/* le voyant : ce qui n'est pas encore parti */
function _syVoyant(){
  let b=document.getElementById('sy-voyant');
  const n=_SY_ATT.size+_SY_ENVOI.size;
  if(!n&&!_SY_HORS){ if(b) b.remove(); return; }
  if(!document.body) return;
  if(!b){ b=document.createElement('div'); b.id='sy-voyant';
    b.style.cssText='position:fixed;right:16px;bottom:16px;z-index:9998;background:#1c1b22;color:#fff;padding:8px 12px;border-radius:9px;font:500 12px Inter,system-ui,sans-serif;box-shadow:0 8px 24px rgba(0,0,0,.3);display:flex;gap:8px;align-items:center';
    document.body.appendChild(b); }
  b.textContent=_SY_HORS?('⚠ Serveur injoignable — '+n+' modification'+(n>1?'s':'')+' en attente'):('Enregistrement… '+n);
  b.style.background=_SY_HORS?'#8a2f2f':'#1c1b22';
}

/* 20 oct. 2026 — LA PAGE DIT DE QUELLE GÉNÉRATION ELLE EST. Une page ouverte depuis la veille garde son ancien code
   tant qu'on ne la recharge pas ; c'est une telle page (sans « grenier ») qui a écrasé les données le 19 octobre.
   Le serveur refuse désormais les écritures des pages qui ne portent pas ce numéro : elles affichent un bandeau
   « recharge cette page », et ne peuvent plus rien abîmer. À augmenter quand une ancienne génération devient dangereuse. */
const _SY_PROTO='3';
let _SY_PERIMEE=false;
function _syPerimee(){
  if(_SY_PERIMEE) return; _SY_PERIMEE=true;
  try{ const b=document.createElement('div');
    b.style.cssText='position:fixed;left:0;right:0;top:0;z-index:2147483647;background:#8a2f2f;color:#fff;font:600 15px/1.45 Inter,system-ui,sans-serif;padding:12px 18px;text-align:center';
    b.textContent=(typeof L3==='function')?L3("Cette page est d'une ancienne version de l'ERP : recharge-la (⌘ + R) avant de continuer. Rien n'a été enregistré depuis.",
      "This page is from an old version of the ERP: reload it (⌘ + R) before going on. Nothing has been saved since.",
      "Esta página es de una versión antigua del ERP: recárgala (⌘ + R) antes de seguir. No se ha guardado nada desde entonces.")
      :"Cette page est d'une ancienne version de l'ERP : recharge-la (⌘ + R).";
    document.body.appendChild(b); }catch(e){}
}
const _SY_T0=new Map(), _SY_LOURD=new Set();   /* début de l'envoi en cours ; envois trop gros pour survivre à un changement de page */
async function _syPut(cle,val,avant){
  /* `connu` : combien d'éléments la copie de ce poste contenait — le serveur refuse qu'un poste qui ne les
     connaissait pas en fasse disparaître la moitié (garde-fou du 20 oct. 2026, voir le cockpit) */
  const _n=v=>Array.isArray(v)?v.length:(v&&typeof v==='object')?Object.keys(v).length:0;
  const corps=JSON.stringify({val,base:_SY_V[cle]||0,connu:_n(_SY_BASE[cle])});
  /* un envoi « keepalive » continue même si on change de rubrique (limite du navigateur : 64 Ko) */
  const petit=corps.length<60000; if(petit) _SY_LOURD.delete(cle); else _SY_LOURD.add(cle);
  const r=await fetch(CK_URL+'/api/o/'+CK_ORG+'/donnees/'+encodeURIComponent(cle),{method:'PUT',keepalive:petit,
    headers:{'Content-Type':'application/json',Authorization:'Bearer '+ckTok(),'X-ERP-Proto':_SY_PROTO},
    body:corps});
  if(r.status===401){ ckPerdu(); throw new Error('session'); }
  if(r.status===426){ _syPerimee(); throw new Error('page périmée'); }
  const j=await r.json().catch(()=>({}));
  if(r.status===409){
    /* quelqu'un a écrit entre-temps : on fusionne sa version avec ce que cet appareil a changé */
    /* 22 oct. 2026 : le repère de la fusion est celui de LA COPIE de cette page (ce qu'elle avait lu), pas la dernière
       version reçue du serveur — sinon une page restée ouverte retirait ce que les autres avaient ajouté entre-temps */
    const fus=fusionne(cle,j.val,(avant!==undefined&&avant!==null)?avant:_SY_BASE[cle],val);
    _SY_V[cle]=j.ver; _SY_BASE[cle]=_cp(j.val);
    try{ localStorage.setItem(cle,JSON.stringify(fus)); }catch(e){}
    _adopte(val,fus); base(cle,val);
    avertitMaj('Quelqu\'un d\'autre vient de modifier les données ('+(j.par||'')+'). Elles ont été fusionnées.');
    return _syPut(cle,val,_cp(val));
  }
  if(!r.ok) throw new Error(j.erreur||('serveur '+r.status));
  _SY_V[cle]=j.ver; _SY_BASE[cle]=_cp(val); _sySauveV();
}

/* pour les listes à identifiant (journal, factures…) : on n'envoie que ce qui a été ajouté ou retiré */
async function _syPatch(cle,val,avant){
  const idf=_ID[cle]||_IDdef;
  const mA=new Map((avant||[]).map(x=>[idf(x),x])), mV=new Map((val||[]).map(x=>[idf(x),x]));
  const ajoute=[], retire=[];
  for(const [i,x] of mV){ if(!mA.has(i)) ajoute.push(x); else if(_sig(mA.get(i))!==_sig(x)) return _syPut(cle,val,avant); }
  for(const i of mA.keys()) if(!mV.has(i)) retire.push(i);
  if(!ajoute.length&&!retire.length) return;
  const r=await fetch(CK_URL+'/api/o/'+CK_ORG+'/donnees/'+encodeURIComponent(cle)+'/delta',{method:'POST',
    headers:{'Content-Type':'application/json',Authorization:'Bearer '+ckTok(),'X-ERP-Proto':_SY_PROTO},
    body:JSON.stringify({ajoute,retire,max:_MAX[cle]||0,date:_DATE[cle]?'t':''})});
  if(r.status===401){ ckPerdu(); throw new Error('session'); }
  if(r.status===426){ _syPerimee(); throw new Error('page périmée'); }
  const j=await r.json().catch(()=>({}));
  if(!r.ok) throw new Error(j.erreur||('serveur '+r.status));
  _SY_V[cle]=j.ver; _SY_BASE[cle]=_cp(val); _sySauveV();
}

async function _syPousse(cle){
  if(_SY_ENVOI.has(cle)||_SY_PERIMEE) return;
  const e=_SY_ATT.get(cle); if(!e) return;
  _SY_ATT.delete(cle); _SY_ENVOI.add(cle); _SY_T0.set(cle,Date.now()); _syVoyant();
  try{
    if(_UID[cle]&&Array.isArray(e.val)&&Array.isArray(e.avant)&&_SY_V[cle]) await _syPatch(cle,e.val,e.avant);
    else await _syPut(cle,e.val,e.avant);
    _SY_HORS=false;
  }catch(err){
    if(err.message==='page périmée'){ if(!_SY_ATT.has(cle)) _SY_ATT.set(cle,e); }
    else if(err.message!=='session'){ _SY_HORS=true; if(!_SY_ATT.has(cle)) _SY_ATT.set(cle,e); }
  }
  _SY_ENVOI.delete(cle); _syVoyant();
  if(_SY_ATT.has(cle)&&!_SY_HORS&&!_SY_PERIMEE) _syPousse(cle);
}
_apresEcrit.push((cle,val,avant)=>{
  if(!_syOk(cle)) return;
  const e=_SY_ATT.get(cle);
  _SY_ATT.set(cle,{val,avant:e?e.avant:avant});
  _syPousse(cle);
});
/* ce qui n'est pas parti (serveur injoignable) repart tout seul */
setInterval(()=>{ if(_SY_PERIMEE) return; if(_SY_ATT.size&&!_SY_ENVOI.size){ _SY_HORS=false; for(const k of _SY_ATT.keys()) _syPousse(k); } },20000);
/* 13 oct. 2026 (Igal : « tous les boutons ne répondent pas… ça ne fait pas sérieux » — c'était la fenêtre de
   Chrome « Quitter le site Web ? », qui bloque tous les clics, affichée à chaque changement de rubrique).
   Désormais la page ne retient celui qui part QUE pour un vrai travail en danger :
     - jamais pour ce que l'ERP enregistre tout seul (tableau des quantités, marqueur « ventes vues ») ;
     - jamais pour un petit envoi en route depuis moins de 4 s : il continue tout seul (keepalive) ;
     - oui pour un envoi qui n'est pas parti (serveur injoignable), trop gros pour continuer, ou bloqué.
   Ce qui l'a retenue est noté (ck-blocage) pour pouvoir le relire si cela se reproduit. */
const _SY_DERIVES=new Set(['stock-erp-v1','ventes-vues-v1','diffusion-erp-v1']);
const _syRetient=()=>{ const r=[];
  _SY_ATT.forEach((e,k)=>{ if(!_SY_DERIVES.has(k)) r.push(k); });
  _SY_ENVOI.forEach(k=>{ if(_SY_DERIVES.has(k)||r.includes(k)) return;
    if(_SY_HORS||_SY_LOURD.has(k)||Date.now()-(_SY_T0.get(k)||0)>4000) r.push(k); });
  return r; };
window.addEventListener('beforeunload',e=>{ const r=_syRetient();
  if(r.length){ try{ localStorage.setItem('ck-blocage',JSON.stringify({t:new Date().toISOString(),page:location.pathname,retient:r,hors:_SY_HORS})); }catch(_){}
    e.preventDefault(); e.returnValue='Des modifications ne sont pas encore enregistrées sur le serveur.'; } });

/* « Ça bug » : tout ralentissement de plus de 250 ms est noté (page, dernier clic, fonctions en cause)
   dans ck-lent, pour pouvoir le relire au lieu de deviner (13 oct. 2026). Rien n'est envoyé nulle part. */
(function(){ try{
  const K='ck-lent'; let dernier='';
  document.addEventListener('click',e=>{ try{ const t=e.target&&e.target.closest?e.target.closest('button,a,tr,select,input,.tab,label'):null;
    dernier=t?(((t.dataset&&(t.dataset.t||t.dataset.k||t.dataset.c))||t.id||String(t.className||'')||t.tagName)+' | '+String(t.textContent||'').trim().slice(0,30)):''; }catch(_){} },true);
  const note=(type,d,x)=>{ try{ const L=JSON.parse(localStorage.getItem(K)||'[]'); L.push({t:new Date().toISOString(),page:location.pathname.split('/').pop(),type:type,ms:Math.round(d),clic:dernier,x:x}); while(L.length>25) L.shift(); localStorage.setItem(K,JSON.stringify(L)); }catch(_){} };
  if(!window.PerformanceObserver) return;
  try{ new PerformanceObserver(l=>l.getEntries().forEach(e=>{ if(e.duration<250) return;
      note('image',e.duration,(e.scripts||[]).slice(0,3).map(z=>[z.invoker||'',z.sourceFunctionName||'',Math.round(z.duration)])); })).observe({type:'long-animation-frame',buffered:true}); }
  catch(_){ try{ new PerformanceObserver(l=>l.getEntries().forEach(e=>{ if(e.duration>=250) note('tâche',e.duration,null); })).observe({entryTypes:['longtask']}); }catch(__){} }
}catch(_){} })();

/* premier passage : le serveur n'a encore rien, cet appareil a tout → on l'y dépose */
if(_SY_ON && window.__CK && window.__CK.charge && !Object.keys(window.__CK.charge).length){
  const cles=[]; try{ for(let i=0;i<localStorage.length;i++){ const k=localStorage.key(i); if(_syOk(k)) cles.push(k); } }catch(e){}
  cles.forEach(k=>{ const v=_dq(k,null); if(v!=null){ _SY_ATT.set(k,{val:v,avant:null}); } });
  if(cles.length){ console.log('cockpit : premier dépôt de',cles.length,'magasins'); for(const k of _SY_ATT.keys()) _syPousse(k); }
}

/* 27 sept. 2026 (Igal) : « en démo, Sam n'a pas le même menu que moi, pas dans le même
   ordre ». Le menu réglé restait dans le navigateur qui l'avait réglé. Il est maintenant
   commun à toute l'équipe, sur le serveur. Le premier appareil qui en a un réglé l'y
   dépose, une seule fois ; ensuite chaque appareil reçoit celui du serveur. */
if(_SY_ON && window.__CK && window.__CK.charge && !window.__CK.charge['menu-perso-v1']){
  const v=_dq('menu-perso-v1',null);
  if(v&&typeof v==='object'&&((v.ordre||[]).length||Object.keys(v.noms||{}).length||(v.caches||[]).length)){
    _SY_ATT.set('menu-perso-v1',{val:v,avant:null}); _syPousse('menu-perso-v1'); }
}

/* ============ LE STOCK PART SUR LES DEUX SITES ============
   Igal, 27 sept. 2026 : « quand je rentre des factures d'achat, je veux que le stock soit
   mis à jour sur l'ERP et sur les deux sites » — et, pour savoir si c'est à chaque
   mouvement ou seulement aux achats, « fais au mieux » : à chaque mouvement (achat, vente,
   comptage, retour, expédition), sinon une vente en caisse laisse sur le site un flacon
   qui n'existe plus.
   On ne s'accroche à aucun écran en particulier : on regarde les écritures du stock
   lui-même (fiches-modifiees-v1, stock-externe-v1). Toute référence dont la quantité a
   changé est mise de côté ; quelques secondes plus tard, les nouvelles quantités partent
   au cockpit, qui les pose sur les deux sites. Rien ne part tant que l'interrupteur des
   Réglages est éteint — et le cockpit le relit de son côté. */
const _SS_K='stock-sites-attente';           /* propre à ce navigateur : pas de -vN, jamais synchronisé */
let _SS_T=0, _SS_ENV=false;
const _ssAllume=()=>{ try{ const r=JSON.parse(localStorage.getItem('reglages-v1')||'{}'); return !!(r&&r.stockSitesAuto===true); }catch(e){ return false; } };
const _ssAtt=()=>{ try{ const a=JSON.parse(localStorage.getItem(_SS_K)||'{}'); return (a&&typeof a==='object'&&!Array.isArray(a))?a:{}; }catch(e){ return {}; } };
const _ssPose=a=>{ try{ localStorage.setItem(_SS_K,JSON.stringify(a)); }catch(e){} };
/* la fiche de base d'une référence : dans le catalogue (produits.js) ou l'inventaire (inventaire.js) */
let _SS_IDX=null;
function _ssFiche(cle){
  if(!_SS_IDX){ _SS_IDX={};
    try{ (window.D_PROD||[]).forEach(r=>{ if(r&&r[15]) _SS_IDX[r[15]]={bc:String(r[0]||''),q:+r[6]||0,nom:[r[2],r[13]||r[1]].filter(Boolean).join(' ')}; }); }catch(e){}
    try{ (window.D_INV||[]).forEach(r=>{ if(r&&r[9]&&!_SS_IDX[r[9]]) _SS_IDX[r[9]]={bc:String(r[0]||''),q:+r[5]||0,nom:[r[2],r[1]].filter(Boolean).join(' ')}; }); }catch(e){} }
  return _SS_IDX[cle]||null;
}
/* Les flacons VENDUS mais pas encore partis : les commandes « à expédier » de Statut
   shipping (1er oct. 2026). L'ERP ne les déstocke qu'à l'envoi — c'est voulu : le flacon
   est encore sur l'étagère, et le recomptage de Sam doit tomber juste. Mais le SITE, lui,
   ne doit plus le proposer : un client achèterait un flacon déjà vendu. Ce qui part aux
   sites, c'est donc le stock MOINS ces commandes. */
/* Un cache de 2 s POUR L'AFFICHAGE (11 oct. 2026) : la colonne « Sur les sites » appelle ceci pour CHAQUE ligne
   du catalogue (3 800) ; relire et réanalyser les expéditions à chaque fois gelait la page. Les chemins qui
   décident d'un envoi (comparaison avant/après, envoi) demandent toujours le calcul frais : _ssAExpedier(true). */
/* LECTURES GROUPÉES (13 oct. 2026). `_dq` relit ET réanalyse tout le magasin à chaque appel ; le tableau des quantités
   le faisait une fois PAR parfum (3 800 × plusieurs Mo) : la page restait figée ~15 s, 9 s après chaque ouverture
   (« page ne répond pas »). Pendant un calcul en masse on ouvre un « memo » : chaque magasin n'est lu qu'une fois. */
let _SS_MEMO=null;
function _ssDq(cle,vide){
  if(!_SS_MEMO) return _dq(cle,vide);
  if(!(cle in _SS_MEMO)) _SS_MEMO[cle]=_dq(cle,vide);
  return _SS_MEMO[cle];
}
function _ssEnMasse(f){ const avait=_SS_MEMO; if(!avait) _SS_MEMO={}; try{ return f(); } finally{ if(!avait) _SS_MEMO=null; } }
let _SS_EXPC=null, _SS_EXPT=0;
function _ssAExpedier(frais){
  if(!frais&&_SS_EXPC&&Date.now()-_SS_EXPT<2000) return _SS_EXPC;
  const m=_ssEnMasse(_ssAExpedierCalc); _SS_EXPC=m; _SS_EXPT=Date.now(); return m;
}
function _ssAExpedierCalc(){
  const E=_ssDq('expeditions-v1',[])||[], m={};
  (Array.isArray(E)?E:[]).forEach(e=>{ if(!e||e.statut!=='attente') return;
    (Array.isArray(e.lignes)?e.lignes:[]).forEach(l=>{ const k=l&&l.cle, q=Math.round(+(l&&l.q)||0); if(k&&q>0) m[k]=(m[k]||0)+q; }); });
  /* + les commandes « on-hold » du site (en attente de paiement) : WooCommerce a déjà retiré
     leurs flacons du site ; le cockpit les lit et les range dans site-reserve-v1 (11 oct. 2026) */
  const Rv=_ssReserve(); for(const k in Rv) m[k]=(m[k]||0)+Rv[k];
  return m;
}
/* site-reserve-v1 : code-barres → flacons d'une commande on-hold. Rattachés aux fiches de l'ERP
   qui ont du stock (un code partagé par plusieurs fiches : on prend là où il y en a). */
function _ssReserve(){
  const R=((_ssDq('site-reserve-v1',null)||{}).q)||{}, m={};
  for(const bc in R){ let reste=Math.round(+R[bc])||0; if(reste<=0) continue;
    let cles=_ssFichesDuBC(bc); if(!cles.length) continue;
    /* un code partagé (boîte / ancienne boîte…) : la commande en attente retient les flacons de la fiche qui porte la même mention que le produit du site */
    if(cles.length>1){ const S=_ssDq('site-stock-v1',{})||{}, ks=_ssCleSite(bc), e=ks&&S[ks], ms=_ssMentionSite(ks||bc,e&&(e.d||e.g)); const a=cles.filter(x=>_ssMentionFiche(x)===ms); if(a.length) cles=a; }
    for(const c of cles){ if(reste<=0) break; const r=_ssQte(c,{}); const dispo=r?r.q:0; const pris=Math.min(reste,dispo);
      if(pris>0){ m[c]=(m[c]||0)+pris; reste-=pris; } }
    if(reste>0) m[cles[0]]=(m[cles[0]]||0)+reste; }
  return m;
}
/* la quantité vendable d'aujourd'hui, comme la calcule le Catalogue : la fiche corrigée,
   sinon l'import du tableur, sinon le fichier d'origine — moins ce qui attend l'envoi */
function _ssQte(cle,EXPA){
  const M=_ssDq('fiches-modifiees-v1',{})||{}, m=M[cle]||{}, f=_ssFiche(cle);
  const bc=String(m.bc||(f&&f.bc)||(/^b\d/.test(cle)?cle.slice(1):'')); if(!bc) return null;
  let q=null;
  if(m.qte!=null) q=+m.qte;
  else { const E=_ssDq('stock-externe-v1',{})||{}; const e=E.q&&E.q[bc]; if(e!=null) q=+e; else if(f) q=f.q; }
  if(q==null||!Number.isFinite(q)) return null;
  const att=((EXPA||_ssAExpedier())[cle])||0;
  return {bc, q:Math.max(0,Math.round(q)-att), att, nom:(f&&f.nom)||m.nom||''};
}
/* ---- un code-barres, plusieurs fiches (la boîte, la « (NOBOX) », le tester) : le site n'a
   qu'UNE fiche pour ce code. Avant (6-7 oct. 2026), chaque fiche envoyait sa propre quantité
   et la dernière gagnait : My Way passait de 12 à 0 à 12 à chaque envoi, et « Update the
   websites » ne finissait jamais. Règle : la fiche du site dit « no box » ou « tester » →
   la fiche de l'ERP qui porte la même mention ; sinon les fiches sans mention ; et si
   plusieurs restent (ancien / nouveau packaging), leur somme — c'est ce que le site peut
   vendre sous ce code. */
/* 10 nov. 2026 : + « OLDBOX » (l'ancienne boîte, un produit à part sur les sites — même règle que _file_auto.py) */
const _ssMention=n=>/no\s*-?\s*box|unbox|\(\s*nb\s*\)/i.test(String(n||''))?'NOBOX':(/tester|testeur|probador/i.test(String(n||''))?'TESTER':(/\boldbox\b/i.test(String(n||''))?'OLDBOX':''));
/* la mention d'une fiche : dans son code (« …oldbox », même corrigé dans l'ERP), sinon dans son nom (corrigé, sinon d'origine) */
function _ssMentionFiche(cle){
  const M=_ssDq('fiches-modifiees-v1',{})||{}, m=M[cle]||{}, f=(_SS_IDX&&_SS_IDX[cle])||{};
  return _ssMention(String(m.bc||f.bc||'').replace(/[0-9]/g,''))||_ssMention((m.nom||'')+' '+(f.nom||''));
}
/* la mention d'un produit du SITE : dans son code (« …oldbox »), sinon dans son nom */
function _ssMentionSite(k,c){ return _ssMention(String(k||'').replace(/[0-9]/g,''))||(c?_ssMention(c.nom||''):''); }
let _SS_PARBC=null;
function _ssFichesDuBC(bc){
  if(!_SS_PARBC){ _ssFiche('_'); _SS_PARBC={};
    for(const cle in _SS_IDX){ const b=String(_SS_IDX[cle].bc||'').replace(/[^0-9]/g,'').replace(/^0+/,''); if(b) (_SS_PARBC[b]=_SS_PARBC[b]||[]).push(cle); } }
  return _SS_PARBC[String(bc||'').replace(/[^0-9]/g,'').replace(/^0+/,'')]||[];
}
/* la quantité à annoncer sur un site pour ce code ; null = une seule fiche, l'appelant garde la sienne */
function _ssQteSite(bc,cote,EXPA){
  const cles=_ssFichesDuBC(bc); if(cles.length<2) return null;
  const S=_ssDq('site-stock-v1',{})||{}; const k=_ssCleSite(bc); const e=k&&S[k]; const c=e&&(e[cote]||e.d||e.g);
  const m=_ssMentionSite(k,c);
  const avec=cles.filter(x=>_ssMentionFiche(x)===m);
  const P=avec.length?avec:cles;
  let q=0; P.forEach(x=>{ const r=_ssQte(x,EXPA); if(r) q+=r.q; });
  return q;
}
/* le code tel que le SITE le range (parfois sans les 0 du début) ; absent des sites → null */
function _ssCleSite(bc){
  const S=_ssDq('site-stock-v1',{})||{}; if(S[bc]) return bc;
  const k=String(bc).replace(/^0+/,'');
  if(_SS_MEMO){                                   /* en masse : l'index sans les 0 du début est fait une seule fois */
    let I=_SS_MEMO['#sans0']; if(!I){ I=_SS_MEMO['#sans0']={}; for(const x in S){ if(x.startsWith('_')) continue; const z=x.replace(/^0+/,''); if(!(z in I)) I[z]=x;
        if(/[A-Za-z]/.test(z)){ const zl='~'+z.toLowerCase(); if(!(zl in I)) I[zl]=x; } } }   /* un code avec des lettres (« …oldbox ») : la casse du site ne compte pas */
    return I[k]||(/[A-Za-z]/.test(k)?I['~'+k.toLowerCase()]:null)||null; }
  for(const x in S){ if(!x.startsWith('_')&&x.replace(/^0+/,'')===k) return x; }
  if(/[A-Za-z]/.test(k)){ const kl=k.toLowerCase(); for(const x in S){ if(!x.startsWith('_')&&x.replace(/^0+/,'').toLowerCase()===kl) return x; } }
  return null;
}
_apresEcrit.push((cle,val,avant)=>{
  if(!_SY_ON||!_ssAllume()) return;
  if(cle==='expeditions-v1'){ _ssExpVerifie(); return; }
  if(cle!=='fiches-modifiees-v1'&&cle!=='stock-externe-v1') return;
  if(avant==null||typeof avant!=='object') return;      /* on ne sait pas ce qui a bougé : on ne devine pas */
  const A=_ssAtt(); let n=0;
  if(cle==='fiches-modifiees-v1'){
    const v=val||{}; new Set([...Object.keys(avant),...Object.keys(v)]).forEach(k=>{
      const qa=avant[k]?avant[k].qte:null, qv=v[k]?v[k].qte:null;
      if((qa==null?null:+qa)!==(qv==null?null:+qv)){ A[k]=1; n++; } });
  } else {
    const a=avant.q||{}, v=(val&&val.q)||{}; new Set([...Object.keys(a),...Object.keys(v)]).forEach(bc=>{
      if((a[bc]==null?null:+a[bc])!==(v[bc]==null?null:+v[bc])){ A['b'+bc]=1; n++; } });
  }
  if(!n) return;
  _ssPose(A); clearTimeout(_SS_T); _SS_T=setTimeout(_ssEnvoie,3000);
});
async function _ssEnvoie(){
  if(_SS_ENV||!_SY_ON||!_ssAllume()) return;
  const A=_ssAtt(), cles=Object.keys(A); if(!cles.length) return;
  const lignes=[], det=[], EXPA=_ssAExpedier(true);
  const vusBC=new Set();
  _ssEnMasse(()=>cles.forEach(k=>{ const x=_ssQte(k,EXPA); if(!x) return; const s=_ssCleSite(x.bc); if(!s) return;
    if(vusBC.has(s)) return; vusBC.add(s);
    const qs=_ssQteSite(x.bc,'d',EXPA); const q=qs==null?x.q:qs;
    lignes.push({bc:s,q}); det.push({bc:x.bc,ref:x.nom,ap:q}); }));
  if(!lignes.length){ _ssPose({}); return; }
  _SS_ENV=true;
  try{
    const r=await fetch(CK_URL+'/api/o/'+CK_ORG+'/site/stock/auto',{method:'POST',
      headers:{'Content-Type':'application/json',Authorization:'Bearer '+ckTok()},body:JSON.stringify({lignes})});
    const j=await r.json().catch(()=>({}));
    if(r.status===409&&j.eteint){ _ssPose({}); return; }
    if(!r.ok) throw new Error(j.erreur||('serveur '+r.status));
    /* ce qui est parti ne repart pas ; une nouvelle modification pendant l'envoi reste en attente */
    const reste=_ssAtt(); cles.forEach(k=>delete reste[k]); _ssPose(reste);
    const S=j.sites||{}, nb=x=>(x&&x.ecrites)||0, refus=[S.detail,S.gros].filter(x=>x&&x.err);
    if(nb(S.detail)||nb(S.gros)||refus.length){
      const J=_dq('crm-journal-v1',[])||[];
      J.push({t:new Date().toISOString(),u:(()=>{ try{ const x=(typeof session==='function')?session():null; return (x&&x.nom)||''; }catch(e){ return ''; } })(),act:'stock',
        lib:refus.length?('stock NON envoyé aux sites — '+refus.map(x=>x.err).join(' / ')):
          ('stock envoyé aux sites — '+nb(S.detail)+' fiche(s) sur perfumestrade.com, '+nb(S.gros)+' sur le site de gros'),
        n:det.length,det:det.slice(0,50)});
      ecrit('crm-journal-v1',J);
      if(refus.length) avertitMaj('Le stock n\'a pas été envoyé aux sites : '+refus[0].err+' Pour l\'envoyer quand même : Catalogue › Envoyer le stock au site.');
    }
    if(Object.keys(_ssAtt()).length){ clearTimeout(_SS_T); _SS_T=setTimeout(_ssEnvoie,3000); }
  }catch(e){ /* serveur injoignable : on garde tout, on réessaie à la prochaine occasion */
    clearTimeout(_SS_T); _SS_T=setTimeout(_ssEnvoie,60000);
  }finally{ _SS_ENV=false; }
}
/* une commande passe « à expédier » (ou part, ou est annulée) : les parfums concernés
   repartent aux sites avec leur nouvelle quantité vendable. On compare à ce qu'on avait
   vu — que le changement vienne de cette page ou d'un autre poste (ck-maj). */
let _SS_EXPVU=null;
function _ssExpVerifie(){
  if(!_SY_ON) return;
  const now=_ssAExpedier(true);
  if(_SS_EXPVU&&_ssAllume()){
    const A=_ssAtt(); let n=0;
    new Set([...Object.keys(_SS_EXPVU),...Object.keys(now)]).forEach(k=>{ if((_SS_EXPVU[k]||0)!==(now[k]||0)){ A[k]=1; n++; } });
    if(n){ _ssPose(A); clearTimeout(_SS_T); _SS_T=setTimeout(_ssEnvoie,3000); }
  }
  _SS_EXPVU=now;
}
window.addEventListener('ck-maj',e=>{ try{ if((e.detail&&e.detail.cles||[]).includes('expeditions-v1')) _ssExpVerifie(); }catch(_){} });
/* ce qui attendait (page fermée trop tôt, coupure) repart à l'ouverture suivante */
if(_SY_ON){ setTimeout(_ssEnvoie,5000); setTimeout(_ssExpVerifie,0); }

/* LE TABLEAU DE NOS QUANTITÉS (11 oct. 2026). Igal : « quand il y a 25 parfums dispo, je veux
   25 sur chaque site ». L'envoi ci-dessus ne part que quand NOUS touchons au stock ; un site qui
   bouge tout seul restait faux. Le cockpit compare maintenant, toutes les 5 minutes, ce que les
   sites annoncent à ce tableau — « code-barres du site → quantité de l'ERP, AVANT retrait des
   commandes déjà vendues » (le cockpit retire lui-même les commandes à expédier, la file et les
   commandes en attente de paiement). Publié à chaque écriture du stock (3 s après) et à
   l'ouverture de la page ; il ne contient que des codes que les sites connaissent. */
let _SS_PUB=0;
function _ssPublie(){
  if(!_SY_ON||!_ssAllume()) return;
  try{
    _ssFiche('_');
    const q=_ssEnMasse(()=>{
    const M=_ssDq('fiches-modifiees-v1',{})||{}, E=_ssDq('stock-externe-v1',{})||{}, E0={};
    const cles=new Set([...Object.keys(_SS_IDX||{}),...Object.keys(M)]);
    const q={}, vus=new Set();
    cles.forEach(k=>{
      const m=M[k]||{}, f=_ssFiche(k);
      const bc=String(m.bc||(f&&f.bc)||(/^b\d/.test(k)?k.slice(1):'')); if(!bc) return;
      const s=_ssCleSite(bc); if(!s||vus.has(s)) return; vus.add(s);
      let v=null;
      if(m.qte!=null) v=+m.qte; else { const e=E.q&&E.q[bc]; if(e!=null) v=+e; else if(f) v=f.q; }
      if(v==null||!Number.isFinite(v)) return;
      const qs=_ssQteSite(bc,'d',E0);        /* un code partagé : la somme des fiches concernées */
      q[s]=Math.max(0,qs==null?Math.round(v):qs);
    });
    return vus.size?q:null;
    });
    if(!q) return;
    ecrit('stock-erp-v1',{t:new Date().toISOString(),q});
  }catch(e){ console.warn('tableau des quantités non publié',e); }
}
_apresEcrit.push((cle)=>{
  if(!_SY_ON||!_ssAllume()) return;
  if(cle==='fiches-modifiees-v1'||cle==='stock-externe-v1'){ clearTimeout(_SS_PUB); _SS_PUB=setTimeout(_ssPublie,3000); }
});
if(_SY_ON){ setTimeout(_ssPublie,9000); }
/* les commandes en attente de paiement ont changé (lues par le cockpit) : les parfums concernés repartent */
window.addEventListener('ck-maj',e=>{ try{ if((e.detail&&e.detail.cles||[]).includes('site-reserve-v1')) _ssExpVerifie(); }catch(_){} });

/* toutes les 45 s : quelqu'un d'autre a-t-il écrit ? */
/* Un onglet CACHÉ relève aussi, une fois par minute (Igal, 1er oct. 2026 : une commande du site
   a attendu 59 min parce que l'ERP était ouvert… derrière une autre fenêtre). Et un seul onglet,
   le « chef » désigné par le serveur, enregistre les ventes qui arrivent : sinon deux ordinateurs
   ouverts en même temps faisaient chacun la facture. */
let _SY_DERH=0;
/* ===== LA VENTE SORT DU STOCK DU SERVEUR, JAMAIS D'UNE COPIE (20 oct. 2026) =====
   PC-1556 et PC-1562 (Perfume City, 19 oct.) : la page qui les a enregistrées travaillait sur une copie
   périmée de l'inventaire Perfume City — 0 flacon là où le serveur en avait 3 et 2. Les ventes sont
   passées « à découvert » et le stock n'a pas baissé. Le numéro de version de la copie disait « à jour » :
   on ne peut donc pas se fier à lui. Désormais, juste avant d'enregistrer une vente (automatique ou
   faite à la main), les magasins de stock sont RELUS sur le serveur, en entier ; si le serveur ne répond
   pas, rien n'est enregistré — la vente attend dans la file, intacte, et repasse au tour suivant. */
const _SY_STOCK=['pc-stock-v1','fiches-modifiees-v1','stock-externe-v1','caisse-file-v1'];
window.__syEnLigne=()=>!!_SY_ON;
window.__syFrais=async function(cles){
  if(!_SY_ON) return true;                                   /* outil hors ligne (essais, fichier local) : comme avant */
  if(_SY_ENVOI.size||_SY_ATT.size) return false;             /* un envoi de ce poste part encore : on repassera après */
  cles=(cles&&cles.length?cles:_SY_STOCK).filter(_syOk);
  try{
    const R=await Promise.all(cles.map(k=>fetch(CK_URL+'/api/o/'+CK_ORG+'/donnees/'+encodeURIComponent(k),
      {headers:{Authorization:'Bearer '+ckTok()},cache:'no-store'}).then(async r=>{
        if(r.status===404) return {k,vide:true};
        if(r.status===401){ ckPerdu(); throw new Error('session'); }
        if(!r.ok) throw new Error('serveur '+r.status);
        const j=await r.json(); if(!j||!('val' in j)) throw new Error('réponse sans valeur'); return Object.assign({k},j); })));
    if(_SY_ENVOI.size||_SY_ATT.size) return false;           /* une écriture est partie pendant la lecture */
    for(const x of R){ if(x.vide) continue;
      try{ localStorage.setItem(x.k,JSON.stringify(x.val)); }catch(e){ _syPlein(); return false; }
      _SY_BASE[x.k]=_cp(x.val); _SY_V[x.k]=x.ver; }
    _sySauveV();
    window.__SY_FRAIS_T=Date.now();
    return true;
  }catch(e){ try{ console.warn('stock du serveur illisible : les ventes attendent',e); }catch(_){} return false; }
};
/* Les ventes arrivées : un seul onglet (le « chef ») les enregistre, sur le stock relu à l'instant. */
let _SY_FILE_EN_COURS=false, _SY_FILE_ESSAI=0, _SY_PAS_CHEF=false;
async function _syTraiteFile(){
  if(!_SY_ON||_SY_FILE_EN_COURS) return false;
  const peut=typeof fileAuto==='function'&&Array.isArray(window.D_PROD)&&window.D_PROD.length>0;
  if(!peut) return false;
  _SY_FILE_EN_COURS=true;
  try{
    if(!(await _syChef())){ _SY_PAS_CHEF=true; return false; }
    _SY_PAS_CHEF=false;
    if(!(await window.__syFrais(_SY_STOCK))){
      /* serveur muet ou envoi en cours : on réessaie bientôt, la vente reste dans la file */
      clearTimeout(_SY_FILE_ESSAI); _SY_FILE_ESSAI=setTimeout(()=>{ _syTraiteFile(); },6000); return true; }
    let r=null; try{ r=window.__FILE_AUTO=fileAuto(); }catch(e){ try{ console.error('ventes arrivées :',e); }catch(_){} }
    if(!r||!r.faites) return true;
    const cache=!!document.hidden;
    if(_syPageCalme() && typeof window.__rafraichir==='function'){ try{ window.__rafraichir(); return true; }catch(e){} }
    if(cache){ window.__SY_A_MONTRER=true; return true; }
    if(typeof window.__rafraichir==='function'){ window.__SY_A_MONTRER=true; _syPlusTard(); return true; }
    avertitMaj('De nouvelles ventes sont arrivées et ont été enregistrées. Recharge la page pour les voir.'); return true;
  } finally { _SY_FILE_EN_COURS=false; }
}
window.__syTraiteFile=_syTraiteFile;
window.__syVeille=(f)=>_syVeille(f);   /* la vérification complète (Ventes) relit le serveur avant d'enregistrer la file */
/* le filet : une vente restée dans la file (le chef a fermé sa page, le serveur ne répondait pas)
   est reprise par n'importe quelle page ouverte, sans attendre qu'une AUTRE vente arrive */
let _SY_FILE_SIG='', _SY_FILE_SIG_T=0;
setInterval(()=>{ try{
  if(!_SY_ON||_SY_FILE_EN_COURS) return;
  const F=lit('caisse-file-v1',[]); if(!Array.isArray(F)||!F.length) return;
  const sig=F.map(v=>v&&v._i).join('|');
  /* la même file qu'au dernier essai (des références inconnues qui attendent quelqu'un) : on ne relit
     le stock qu'une fois toutes les dix minutes, pas à chaque passage */
  /* refusé parce qu'un autre onglet était chef : on redemande à chaque passage — si cet onglet-là a
     été fermé, le serveur nous donne la place au bout de 90 s et la vente n'attend pas la suivante */
  if(sig===_SY_FILE_SIG && !_SY_PAS_CHEF && Date.now()-_SY_FILE_SIG_T<600000) return;
  _SY_FILE_SIG=sig; _SY_FILE_SIG_T=Date.now();
  _syTraiteFile();
}catch(e){} },90000);
const _SY_TAB=(()=>{ try{ let t=sessionStorage.getItem('ck-onglet'); if(!t){ t='o'+Date.now().toString(36)+Math.random().toString(36).slice(2,8); sessionStorage.setItem('ck-onglet',t); } return t; }catch(e){ return 'o'+Math.random().toString(36).slice(2,10); } })();
async function _syChef(){
  if(_SY_PERIMEE) return false;
  try{ const r=await fetch(CK_URL+'/api/o/'+CK_ORG+'/file/bail',{method:'POST',headers:{'Content-Type':'application/json',Authorization:'Bearer '+ckTok(),'X-ERP-Proto':_SY_PROTO},body:JSON.stringify({tab:_SY_TAB})});
    if(r.status===404) return true;                 /* cockpit d'avant : comme avant */
    if(!r.ok) return false;
    const j=await r.json(); return !!j.chef; }catch(e){ return false; }
}
let _SY_FLUX=false, _SY_DERV=0;
async function _syVeille(force){
  if(!_SY_ON||_SY_ENVOI.size||_SY_ATT.size) return;
  const cache=!!document.hidden;
  /* le fil en direct prévient dans la seconde : la relève régulière ne sert plus que de filet */
  if(!force){
    if(_SY_FLUX && Date.now()-_SY_DERV<30000) return;
    if(cache){ if(Date.now()-_SY_DERH<55000) return; _SY_DERH=Date.now(); }
  }
  _SY_DERV=Date.now();
  try{
    const r=await fetch(CK_URL+'/api/o/'+CK_ORG+'/donnees/versions',{headers:{Authorization:'Bearer '+ckTok()}});
    if(r.status===401){ ckPerdu(); return; }
    if(!r.ok) return;
    const V=await r.json(); window.__SY_OK=Date.now();     /* le serveur a répondu : cette page est à jour à cet instant */
    { let d=false; for(const k in V){ if(_SY_SRV(k)&&_SY_VS[k]!==V[k]){ _SY_VS[k]=V[k]; d=true; } }
      if(d){ try{ localStorage.setItem(_SY_KVS,JSON.stringify(_SY_VS)); }catch(e){} } }
    const chg=Object.keys(V).filter(k=>_syOk(k)&&V[k]!==(_SY_V[k]||0));
    if(!chg.length) return;
    const r2=await fetch(CK_URL+'/api/o/'+CK_ORG+'/donnees/lire',{method:'POST',headers:{'Content-Type':'application/json',Authorization:'Bearer '+ckTok()},body:JSON.stringify({versions:Object.assign({},_SY_V,_SY_VS)})});
    if(!r2.ok) return;
    const j=await r2.json(); let qui='', touche=false, ventes=false;
    const rates=[];
    for(const k in j.magasins){ if(!_syOk(k)) continue;
      try{ localStorage.setItem(k,JSON.stringify(j.magasins[k].val)); }
      catch(e){ rates.push(k); _syPlein(); continue; }   /* pas rangée : sa version ne sera pas notée, elle sera redemandée */
      _SY_BASE[k]=_cp(j.magasins[k].val); qui=j.magasins[k].par||qui; if(k in _REF && k!=='messages-v1') touche=true;   /* les messages se redessinent seuls (ck-maj) : pas de bandeau */
      /* le cockpit a déposé des ventes du site ou de la caisse : elles s'enregistrent à
         l'ouverture d'une page (voir _file_auto.py), pas au milieu d'un travail en cours */
      if(k==='caisse-file-v1'&&Array.isArray(j.magasins[k].val)&&j.magasins[k].val.length) ventes=true;
      if(k==='menu-perso-v1'){ try{ if(typeof mnApplique==='function') mnApplique(); }catch(e){} } }
    { const nv=Object.assign({},j.versions||_SY_V); Object.keys(nv).filter(_SY_SRV).forEach(k=>delete nv[k]); rates.forEach(k=>{ if(k in _SY_V) nv[k]=_SY_V[k]; else delete nv[k]; }); _SY_V=nv; } _sySauveV();
    /* 29 sept. (Igal : « Sam ne reçoit les messages que s'il actualise ») : on prévient la
       page de ce qui vient d'arriver — la messagerie et la pastille se redessinent seules */
    try{ window.dispatchEvent(new CustomEvent('ck-maj',{detail:{cles:Object.keys(j.magasins||{})}})); }catch(e){}
    try{ (window.__SYDBG=window.__SYDBG||[]).push({t:Date.now(),cles:Object.keys(j.magasins||{}),touche,ventes}); if(window.__SYDBG.length>20) window.__SYDBG.shift(); }catch(_){}
    if(!touche&&!ventes) return;
    /* les ventes arrivées : seul le chef les enregistre ; les autres onglets les recevront
       enregistrées au tour suivant (comme une modification faite par un autre poste) */
    /* seule une page qui a le catalogue sait reconnaître les parfums : les autres (Réglages,
       Journal, Inventaire…) ne demandent pas à être chef — sinon elles garderaient la place
       sans rien pouvoir enregistrer */
    const peut=typeof fileAuto==='function'&&Array.isArray(window.D_PROD)&&window.D_PROD.length>0;
    if(ventes && peut && await _syTraiteFile()) return;     /* chef : enregistrées sur le stock relu au serveur */
    if(ventes && peut) ventes=false;     /* un autre onglet, chef, s'en charge */
    if(!touche&&!ventes) return;
    if(cache){ window.__SY_A_MONTRER=true; return; }
    /* Igal, 24 sept. 2026 : « je trouve ça long » — les ventes arrivées devaient
       entrer sans attendre. On le faisait en rechargeant la page ; Igal, 26 sept. :
       « le ERP se réactualise en plein milieu du travail, page blanche, ça ne fait
       pas sérieux ». On ne recharge donc plus JAMAIS la page tout seul : les ventes
       s'enregistrent sur place (fileAuto) et la page se redessine dans l'écran, sans
       blanc, à condition qu'elle sache le faire (window.__rafraichir) et que personne
       ne soit en train de saisir. Sinon, un bandeau propose de recharger. */
    if((ventes||touche) && _syPageCalme() && typeof window.__rafraichir==='function'){
      try{ window.__rafraichir(); return; }
      catch(e){ try{ console.error('rafraîchissement sur place :',e); }catch(_){} }
    }
    /* Igal, 17 oct. 2026 : « comment faire pour ne pas avoir ce message en bas de la page » — une page qui sait se
       redessiner ne montre plus de bandeau : elle attend d'être calme (fiche fermée, plus de saisie) et se redessine alors. */
    if(typeof window.__rafraichir==='function'){ window.__SY_A_MONTRER=true; _syPlusTard(); return; }
    if(ventes) avertitMaj('De nouvelles ventes du site ou de la caisse sont arrivées. Elles seront enregistrées au rechargement de la page.');
    else if(touche) avertitMaj('Les données ont été modifiées'+(qui?' par '+qui:'')+'.');
  }catch(e){}
}
/* on repasse toutes les 2 s : dès que la page est calme et visible, elle se redessine, sans un mot */
let _SY_PT=null, _SY_PT_T0=0;
const SY_ATTENTE_MAX=30000;
/* 20 oct. 2026 (Igal : la vente PC-1562 était enregistrée, mais la page Ventes de Sam ne l'a montrée qu'au moment où Igal s'est
   connecté) : un curseur laissé dans un champ (« Chercher un client »…) rendait la page « pas calme » pour toujours — et depuis
   le 17 oct., sans bandeau, elle attendait en silence. Désormais, au bout de 30 s, si aucune fenêtre n'est ouverte, la page se
   redessine quand même, en remettant le curseur dans le champ, avec ce qui y était tapé. Une fenêtre ouverte (fiche, vente en
   cours) continue, elle, de bloquer : on ne redessine jamais sous une saisie en cours. */
function _syFenetreOuverte(){ try{ return !!document.querySelector('.ov.on,.dov.on,.mod.on,dialog[open],.mvoile'); }catch(e){ return true; } }
function _syRedessineEnGardantLeChamp(){
  const a=document.activeElement; const id=a&&a.id, val=a&&a.value, deb=a&&a.selectionStart, fin=a&&a.selectionEnd;
  try{ window.__rafraichir(); }catch(e){}
  if(!id) return;
  try{ const b=document.getElementById(id); if(!b) return;
    if(b!==a && 'value' in b && b.value!==val) b.value=val;
    b.focus({preventScroll:true}); if(deb!=null&&typeof b.setSelectionRange==='function'){ try{ b.setSelectionRange(deb,fin); }catch(_){} } }catch(e){}
}
function _syPlusTard(){
  if(_SY_PT) return;
  _SY_PT_T0=Date.now();
  _SY_PT=setInterval(()=>{ if(!window.__SY_A_MONTRER){ clearInterval(_SY_PT); _SY_PT=null; return; }
    if(document.hidden||typeof window.__rafraichir!=='function') return;
    const calme=_syPageCalme();
    if(!calme && (Date.now()-_SY_PT_T0<SY_ATTENTE_MAX || _syFenetreOuverte())) return;
    window.__SY_A_MONTRER=false; clearInterval(_SY_PT); _SY_PT=null;
    if(calme){ try{ window.__rafraichir(); }catch(e){} } else _syRedessineEnGardantLeChamp(); },2000);
}
function _syPageCalme(){
  try{
    if(document.querySelector('.ov.on,.dov.on,.mod.on,dialog[open],.mvoile')) return false;
    const a=document.activeElement; if(a&&/^(INPUT|TEXTAREA|SELECT)$/.test(a.tagName)&&a.type!=='checkbox'&&a.type!=='radio') return false;
    return true;
  }catch(e){ return false; }
}
/* toutes les 8 s (et non plus 45) : un message doit arriver comme un message, pas une
   minute plus tard. La question posée au serveur est minuscule (des numéros de version). */
setInterval(()=>_syVeille(false),8000);
/* 20 oct. 2026 (Igal : entre le 19 à 18h35 et le 20 à 14h27, Sam ne voyait pas ses ventes — elles étaient bien sur le serveur) :
   une page qui ne reçoit plus rien ne doit JAMAIS rester silencieuse. Si le serveur n'a pas répondu à cette page depuis 2 minutes
   alors qu'elle est visible, une bande rouge le dit et propose de recharger. Elle disparaît d'elle-même quand le serveur répond. */
window.__SY_OK=Date.now();
function _syControlePerime(force){
  if(!_SY_ON&&!force) return;
  const age=Date.now()-(window.__SY_OK||0);
  let b=document.getElementById('sy-perime');
  if(document.hidden||age<120000){ if(b) b.remove(); return; }
  const lg=(typeof LANG==='string')?LANG:'fr', m=Math.max(2,Math.round(age/60000));
  const T=lg==='en'?['This page has not received anything from the server for '+m+' min: sales may be missing here. ','Reload']
    :lg==='es'?['Esta página no recibe nada del servidor desde hace '+m+' min: pueden faltar ventas aquí. ','Recargar']
    :['Cette page ne reçoit plus rien du serveur depuis '+m+' min : des ventes peuvent manquer ici. ','Recharger'];
  if(!b){ b=document.createElement('div'); b.id='sy-perime'; b.setAttribute('data-nolang','');
    b.style.cssText='position:fixed;z-index:2147483646;left:0;right:0;top:0;background:#9B2C2C;color:#fff;font:600 14px/1.4 system-ui,sans-serif;padding:10px 16px;text-align:center';
    document.body.appendChild(b); }
  b.innerHTML=''; b.appendChild(document.createTextNode(T[0]));
  const bt=document.createElement('button'); bt.textContent=T[1]; bt.style.cssText='margin-left:8px;padding:4px 12px;border:0;border-radius:6px;font-weight:700;cursor:pointer';
  bt.onclick=()=>location.reload(); b.appendChild(bt);
}
window.__syControlePerime=_syControlePerime;
setInterval(()=>_syControlePerime(),10000);
/* LE FIL EN DIRECT (1er oct. 2026, Igal : « il faut qu'à chaque fois que quelqu'un touche à
   l'ERP, les modifications soient instantanées ») : une connexion ouverte avec le cockpit, qui
   dit dans la seconde quels magasins ont changé. On va alors chercher ce qui a changé. Lu avec
   fetch (et non EventSource) pour envoyer la clé de session dans l'en-tête, pas dans l'adresse.
   Coupé (veille de l'ordinateur, réseau) : il se rebranche tout seul, et la relève toutes les
   8 s reprend en attendant. */
let _SY_TOUT_T=0;
function _syTout(){
  if(_SY_ENVOI.size||_SY_ATT.size){ clearTimeout(_SY_TOUT_T); _SY_TOUT_T=setTimeout(_syTout,400); return; }
  _syVeille(true);
}
async function _syFlux(){
  if(!_SY_ON||typeof fetch!=='function'||typeof TextDecoder!=='function') return;
  for(;;){
    try{
      const r=await fetch(CK_URL+'/api/o/'+CK_ORG+'/flux',{headers:{Authorization:'Bearer '+ckTok()},cache:'no-store'});
      if(r.status===401){ ckPerdu(); return; }
      if(r.status===404) return;                       /* cockpit d'avant : la relève suffit */
      if(!r.ok||!r.body||!r.body.getReader) throw new Error('flux');
      _SY_FLUX=true; _syTout();                        /* ce qui a pu changer pendant la coupure */
      const rd=r.body.getReader(), dec=new TextDecoder(); let buf='';
      for(;;){ const x=await rd.read(); if(x.done) break; buf+=dec.decode(x.value,{stream:true});
        let i; while((i=buf.indexOf('\n\n'))>=0){ const bloc=buf.slice(0,i); buf=buf.slice(i+2); if(/^data:/m.test(bloc)) _syTout(); } }
    }catch(e){}
    _SY_FLUX=false;
    await new Promise(ok=>setTimeout(ok,3000));
  }
}
window.__SY_FLUX=()=>_SY_FLUX;
if(_SY_ON) setTimeout(_syFlux,1500);
document.addEventListener('visibilitychange',()=>{ if(document.hidden) return;
  /* de retour sur un onglet qui a reçu des nouveautés pendant qu'il était caché */
  if(window.__SY_A_MONTRER){ window.__SY_A_MONTRER=false;
    if(_syPageCalme() && typeof window.__rafraichir==='function'){ try{ window.__rafraichir(); }catch(e){} }
    else if(typeof window.__rafraichir==='function'){ window.__SY_A_MONTRER=true; _syPlusTard(); }
    else avertitMaj('Des données ont changé pendant ton absence. Recharge la page pour les voir.'); }
  _syVeille(true); });
"""


def sync_js():
    import json
    return SYNC.replace('__EXCLUS__', json.dumps(EXCLUS))


def enligne(html):
    """Transforme la page pour que son code attende les données du serveur avant de tourner.

    Le grand <script> de fin de page devient un bloc inerte (type="text/plain"), et un petit
    script le lance une fois l'AMORCE passée. En local l'AMORCE lance tout de suite.
    """
    # le vocabulaire de la maison (« cote ») sur le texte fixe, au montage — voir _langue.vocab_html
    import _langue
    html = _langue.vocab_html(html)
    fin = '</script></body></html>'
    if not html.rstrip().endswith(fin):
        raise SystemExit('enligne : la page ne finit pas par ' + fin)
    i = html.rfind('<script>')
    if i < 0:
        raise SystemExit('enligne : pas de <script> final')
    corps = html[i + len('<script>'):html.rstrip().rfind(fin)]
    if '</script' in corps:
        raise SystemExit('enligne : "</script" dans le code de la page')
    tete = '<head><meta charset="utf-8">'
    if html.count(tete) != 1:
        raise SystemExit('enligne : pas de <head><meta charset="utf-8"> unique pour y poser le grenier')
    html = html.replace(tete, tete + GRENIER.strip(), 1)
    i = html.rfind('<script>')
    corps = html[i + len('<script>'):html.rstrip().rfind(fin)]
    return (html[:i] + '<script type="text/plain" id="page-js">' + corps + '</script>\n<script>'
            + AMORCE + '</script></body></html>\n')
