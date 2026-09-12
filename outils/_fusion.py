# -*- coding: utf-8 -*-
"""Écriture partagée entre plusieurs onglets de SAM.

Avant : chaque onglet gardait sa copie des données en mémoire et réécrivait
tout le paquet. Deux onglets ouverts en même temps → le dernier à enregistrer
effaçait le travail de l'autre.

Ici, au moment d'écrire, on relit ce qui est réellement sur le disque et on n'y
applique que ce que CET onglet a changé depuis sa dernière écriture.
"""

FUSION = r"""
/* ============ ECRITURE PARTAGEE ENTRE ONGLETS ============ */
const _REF={};
const _cp=v=>{ try{ return JSON.parse(JSON.stringify(v)); }catch(e){ return null; } };
const _sig=v=>JSON.stringify(v===undefined?null:v);
const _dq=(cle,vide)=>{ try{ const t=localStorage.getItem(cle); return t==null?vide:JSON.parse(t); }catch(e){ return vide; } };
/* a appeler juste apres avoir lu un magasin : c'est le point de comparaison */
function base(cle,val){ _REF[cle]=_cp(val); return val; }
/* identite d'une ligne, pour reconnaitre la meme entree ecrite par l'autre onglet */
const _IDdef=x=>_sig(x);
/* Les lignes ajoutées par CET onglet reçoivent un identifiant unique avant d'être écrites.
   Sans lui, deux lignes de journal écrites dans la même milliseconde (une facture de 30
   lignes en écrit 30 d'un coup) avaient la même identité et se dévoraient entre elles. */
const _UID={'crm-journal-v1':1,'factures-v1':1,'ajustements-v1':1,'articles-ajoutes-v1':1,
            'caisse-file-v1':1};
let _seq=0;
const _neuf=()=>'x'+Date.now().toString(36)+(++_seq).toString(36)+Math.random().toString(36).slice(2,6);
const _ID={
  'crm-journal-v1': x=>x._i||[x.t,x.act||'',x.lib||'',x.ref||'',x.bc||''].join('|'),
  'factures-v1'   : x=>x._i||x.id||[x.num||'',x.d||'',x.montant].join('|'),
  'ajustements-v1': x=>x._i||[x.t,x.cle||''].join('|'),
  /* la file des ventes de caisse : l'identifiant vient du serveur, on ne le refabrique jamais */
  'caisse-file-v1' : x=>x._i||''};
const _MAX={'crm-journal-v1':4000,'ajustements-v1':4000};
/* pour ces magasins, on garde les plus RÉCENTS quand le plafond est atteint */
const _DATE={'crm-journal-v1':x=>x.t||'','ajustements-v1':x=>x.t||''};
/* magasins objet dont chaque valeur est elle-meme une liste a fusionner */
const _IMBR={'ventes-v1'         : x=>x._i||[x.d||'',x.num||'',x.q,x.p,x.c||'',x.k||''].join('|'),
             'prix-achat-hist-v1': x=>[x.d||'',x.p,x.f||'',x.q,x.num||'',x.src||''].join('|')};
/* magasins dont une sous-clé est elle-même une carte à fusionner clé par clé */
const _SOUSMAP={'stock-externe-v1':['q']};
/* magasins ou chaque fiche est un paquet de champs : on fusionne champ par champ,
   pour que deux onglets puissent corriger deux champs differents du meme produit */
const _CHAMPS={'fiches-modifiees-v1':1,'clients-v1':1,'reglements-v1':1,'fournisseurs-v1':1,'marche-v1':1};
function fusChamps(dq,ref,cour){
  const o=(dq&&typeof dq==='object'&&!Array.isArray(dq))?Object.assign({},dq):{};
  const r=ref||{};
  Object.keys(cour).forEach(f=>{ if(_sig(cour[f])!==_sig(r[f])) o[f]=cour[f]; });
  Object.keys(r).forEach(f=>{ if(!(f in cour)) delete o[f]; });
  return o;
}

function fusListe(disque,ref,cour,idf){
  const mR=new Map((ref||[]).map(x=>[idf(x),x])), mC=new Map((cour||[]).map(x=>[idf(x),x]));
  const out=[], vus=new Set();
  (disque||[]).forEach(x=>{ const i=idf(x);
    if(vus.has(i)) return;
    if(mR.has(i)&&!mC.has(i)) return;                 /* supprimee ici : on la retire aussi */
    out.push(mC.has(i)&&_sig(mC.get(i))!==_sig(mR.get(i)) ? mC.get(i) : x); vus.add(i); });
  (cour||[]).forEach(x=>{ const i=idf(x); if(!vus.has(i)){ out.push(x); vus.add(i); } });
  return out;
}

/* Le cœur : à partir de ce qui est sur le disque (ou sur le serveur), de ce que cet onglet
   avait lu (ref) et de ce qu'il veut écrire (val), la version à garder. */
function fusionne(cle,disque,ref,val){
  let sortie=val;
  try{
  if(ref!=null && val!=null && typeof val==='object'){
    if(Array.isArray(val)&&Array.isArray(ref)){
      sortie=fusListe(Array.isArray(disque)?disque:[],ref,val,_ID[cle]||_IDdef);
      const m=_MAX[cle];
      if(m&&sortie.length>m){
        /* on garde les plus récentes, pas les dernières arrivées dans le tableau :
           sinon des lignes anciennes ressuscitées chassaient des lignes réelles */
        const dt=_DATE[cle];
        if(dt) sortie=sortie.slice().sort((a,b)=>String(dt(a)).localeCompare(String(dt(b))));
        sortie=sortie.slice(-m);
      }
    } else if(!Array.isArray(val)&&!Array.isArray(ref)){
      const dq=(disque&&typeof disque==='object'&&!Array.isArray(disque))?disque:{}, imb=_IMBR[cle], sm=_SOUSMAP[cle]||[];
      Object.keys(val).forEach(k=>{
        if(_sig(val[k])===_sig(ref[k])) return;       /* pas touche par cet onglet */
        if(imb&&Array.isArray(val[k])) dq[k]=fusListe(Array.isArray(dq[k])?dq[k]:[],ref[k]||[],val[k],imb);
        else if(sm.indexOf(k)>=0&&val[k]&&typeof val[k]==='object'&&!Array.isArray(val[k])) dq[k]=fusChamps(dq[k],ref[k],val[k]);
        else if(_CHAMPS[cle]&&val[k]&&typeof val[k]==='object'&&!Array.isArray(val[k])) dq[k]=fusChamps(dq[k],ref[k],val[k]);
        else dq[k]=val[k]; });
      Object.keys(ref).forEach(k=>{ if(!(k in val)) delete dq[k]; });
      sortie=dq;
    }
  }
  }catch(e){ sortie=val; }   /* forme inattendue sur le disque : on écrit au moins notre version */
  return sortie;
}
/* l'onglet repart de la version fusionnée : on remplace le contenu de son objet, pas sa référence */
function _adopte(val,sortie){
  if(sortie===val || !val || typeof val!=='object') return;
  if(Array.isArray(val)&&Array.isArray(sortie)){ val.length=0; sortie.forEach(x=>val.push(x)); }
  else if(!Array.isArray(val)&&!Array.isArray(sortie)){ Object.keys(val).forEach(k=>delete val[k]); Object.assign(val,sortie); }
}
/* après une écriture locale : le serveur, s'il y en a un, est prévenu ici (voir _serveur.py) */
const _apresEcrit=[];
function ecrit(cle,val){
  const ref=_REF[cle];
  /* on marque les lignes que cet onglet vient d'ajouter, pour qu'elles restent reconnaissables */
  if(_UID[cle]&&Array.isArray(val)){
    const deja=new Set((Array.isArray(ref)?ref:[]).map(x=>_sig(x)));
    val.forEach(x=>{ if(x&&typeof x==='object'&&!x._i&&!deja.has(_sig(x))){ x._i=_neuf();
      if(cle==='crm-journal-v1'){ /* d'où vient l'action, et avec quel rôle : le journal le montre */
        if(!x.pg) x.pg=(location.pathname.split('/').pop()||'').replace(/\.html$/,'')||'catalogue';
        if(!x.r){ try{ const sx=(typeof session==='function')?session():null; if(sx&&sx.role) x.r=sx.role; }catch(e){} } } } });
  }
  const sortie=fusionne(cle,_dq(cle,Array.isArray(val)?[]:{}),ref,val);
  try{ localStorage.setItem(cle,typeof sortie==='string'?sortie:JSON.stringify(sortie)); }catch(e){ return val; }
  _adopte(val,sortie);
  const avant=_REF[cle];
  _REF[cle]=_cp(val);
  _apresEcrit.forEach(f=>{ try{ f(cle,val,avant); }catch(e){} });
  return val;
}
/* ================= LE JOUR, VU DE LA BOUTIQUE =================
   `new Date().toISOString().slice(0,10)` donne le jour à GREENWICH. Le magasin
   est à Miami, quatre heures derrière l'été, cinq l'hiver. Tout ce qui se vend
   après 20 h (19 h l'hiver) était donc daté du LENDEMAIN :

     mercredi 9 septembre, 22 h 30 à Miami  →  l'ERP écrivait « 2026-09-10 »

   Conséquences, toutes silencieuses : le chiffre du jour au tableau de bord est
   faux tous les soirs, la caisse du soir ne tombe jamais juste, une facture part
   chez le client datée de demain, et l'entrée du journal se range au mauvais
   jour. Rien ne s'affiche en rouge : les chiffres sont simplement décalés d'un
   cran, ce qui est bien pire qu'une erreur visible.

   D'où ces deux fonctions, à utiliser partout où l'on veut UN JOUR. L'heure
   pleine, elle, reste en UTC dans les champs `t:` — un instant daté en UTC est
   exact et sans ambiguïté ; c'est seulement le découpage en journées qui doit
   se faire à l'heure du comptoir. */
function isoJour(d){
  const x = (d==null) ? new Date() : (d instanceof Date ? d : new Date(d));
  if(isNaN(x.getTime())) return '';
  return x.getFullYear()+'-'+String(x.getMonth()+1).padStart(2,'0')
         +'-'+String(x.getDate()).padStart(2,'0');
}
function ajd(){ return isoJour(); }
/* L'HEURE, vue de la boutique : « 14:32 » à Miami, quel que soit l'ordinateur qui
   enregistre. Sert à horodater les ventes ; sans argument, c'est maintenant. */
function heureMiami(t){
  try{ const x=(t==null)?new Date():(t instanceof Date?t:new Date(t)); if(isNaN(x.getTime())) return '';
    return x.toLocaleTimeString('en-GB',{timeZone:'America/New_York',hour:'2-digit',minute:'2-digit',hour12:false}); }
  catch(e){ return ''; }
}

/* Un magasin dont la FORME ne correspond plus à ce qu'on attend.
   `lit` rattrapait déjà le JSON illisible. Il ne rattrapait pas le JSON
   parfaitement lisible mais de la mauvaise forme : un objet là où le code
   attend une liste, une chaîne là où il attend un objet. La page recevait
   alors sa valeur sans broncher et mourait deux lignes plus loin sur un
   « FACT.slice is not a function » — écran figé, aucune explication.
   Ça n'a rien de théorique : un onglet fermé pendant une écriture, un quota
   atteint, une synchro coupée en deux suffisent. On compare donc la forme
   reçue à celle de la valeur par défaut, et on garde le défaut si elles ne
   se ressemblent pas : mieux vaut une page vide qu'une page morte. */
function _memeForme(v,d){
  if(d===null||d===undefined) return true;      // pas d'attente : on ne juge pas
  if(Array.isArray(d)) return Array.isArray(v);
  if(typeof d==='object') return v!==null && typeof v==='object' && !Array.isArray(v);
  return typeof v===typeof d;
}
/* lecture d'un magasin : on memorise au passage le point de comparaison */
let lit=(k,d)=>{
  let v=d;
  try{ const t=localStorage.getItem(k); if(t!=null) v=JSON.parse(t); }catch(e){ v=d; }
  if(!_memeForme(v,d)){
    try{ console.warn('donnée « '+k+' » de forme inattendue : on repart du défaut'); }catch(e){}
    v=d;
  }
  return base(k,v);
};


/* Le catalogue complet : les références du fichier (D_PROD) + les articles ajoutés à la main
   (articles-ajoutes-v1), mis au même format. Chaque page qui indexe les produits passe par ici,
   sinon un article créé dans le catalogue n'existe ni pour les factures ni pour les ventes. */
function D_TOUS(){
  const A=_dq('articles-ajoutes-v1',[]); const L=Array.isArray(A)?A:[];
  const n=v=>(v==null||v==='')?null:+v;
  const rows=L.map((o,i)=>[String(o.bc||'').trim(),o.nom||'',o.marque||'',String(o.ml||'').trim(),String(o.type||'').toUpperCase(),
    String(o.genre||'').toUpperCase(),n(o.qte)||0,n(o.pvr),n(o.pvw),'',0,[],n(o.pa),o.nom||'','',o.id||('a'+i),null,null]);
  return (window.D_PROD||[]).concat(rows);
}

/* quelqu'un d'autre (autre onglet, autre personne) vient d'écrire : on le dit, sans rien écraser */
let _averti=false;
function avertitMaj(msg){
  if(_averti||!document.body) return;
  _averti=true;
  const b=document.createElement('div');
  b.style.cssText='position:fixed;left:50%;bottom:22px;transform:translateX(-50%);z-index:9999;'
   +'background:#1c1b22;color:#fff;padding:11px 16px;border-radius:10px;'
   +'font:500 13px Inter,system-ui,sans-serif;box-shadow:0 10px 34px rgba(0,0,0,.34);'
   +'display:flex;gap:13px;align-items:center;max-width:92vw';
  b.appendChild(document.createTextNode(msg||'Un autre onglet vient de modifier les données.'));
  const r=document.createElement('button'); r.textContent='Recharger cette page';
  r.style.cssText='background:#6b5cff;color:#fff;border:0;border-radius:7px;padding:7px 11px;font:600 12.5px Inter,system-ui,sans-serif;cursor:pointer;white-space:nowrap';
  r.onclick=()=>location.reload();
  const x=document.createElement('button'); x.textContent='Plus tard';
  x.style.cssText='background:none;border:0;color:#b9b7c4;font:500 12.5px Inter,system-ui,sans-serif;cursor:pointer';
  x.onclick=()=>{ b.remove(); _averti=false; };
  b.appendChild(r); b.appendChild(x); document.body.appendChild(b);
}
addEventListener('storage',e=>{
  if(!e.key||!(e.key in _REF)) return;
  avertitMaj('Un autre onglet vient de modifier les données.');
});
"""
