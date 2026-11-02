# -*- coding: utf-8 -*-
"""Retrouver un parfum du catalogue par son nom : la marque, le nom, la contenance.

Un seul moteur pour les deux endroits qui en ont besoin : le message client de
Ventes/Quotes et l'Étude de devis (une price list sans codes-barres). Le moteur
PROPOSE, avec un score ; la page décide ce qu'elle en fait. Et il RETIENT les
corrections (alias-noms-v1) : une ligne corrigée une fois est reconnue ensuite.

La page qui l'inclut fournit : IDX (le catalogue indexé), lit() (lecture d'un
magasin), cleDeBC(code) (un code-barres → une clé, ou rien) et, de préférence,
D_TOUS() (les noms complets et les types)."""

NOMS = r'''
const K_ALIASN='alias-noms-v1';

const mNorm=s=>String(s==null?'':s).toLowerCase().normalize('NFD')
  .replace(/[\u0300-\u036f]/g,'').replace(/[^a-z0-9]+/g,' ').trim();
/* les mots-outils ne disent rien du parfum : « de » dans « Bleu de Chanel » ne doit
   pas rapprocher « Club de Nuit » — c'est exactement ce qui faisait gagner un clone */
const M_VIDES=new Set(['de','du','des','la','le','les','l','d','et','en','pour','par','the','of','and','for','by','in','a','au','aux','un','une','with','avec','ml','oz','x',
  /* les mots d'emballage des titres Amazon et des factures (« … PERFUME SPRAY », « … EDP VAPO ») :
     ils ne disent rien du parfum et diluaient le score jusqu'à ne plus rien proposer */
  'perfume','spray','vapo','vaporisateur','vaporizer','natural','fragrance','fragrances']);
/* une marque écrite de deux façons : « Bulgari » sur Amazon, « Bvlgari » au catalogue */
const M_MARQUES=[[/\bbulgari\b/g,'bvlgari'],[/\bysl\b/g,'yves saint laurent'],[/\bd\s*g\b/g,'dolce gabbana']];
const mMarques=t=>M_MARQUES.reduce((a,[re,r])=>a.replace(re,r),t);

/* Les contenances du catalogue sont en onces ; les clients écrivent les deux.
   On ramène tout en millilitres : c'est la seule façon de comparer « 100 ml » et
   « 3.4 oz », qui sont le même flacon. */
/* « Eau de Parfum » écrit en toutes lettres, c'est le type edp — pas les mots
   « eau » et « parfum », qui feraient pencher vers le Parfum pur */
const mTypes=s=>String(s||'').replace(/\beau\s+de\s+parfum\b/gi,' edp ').replace(/\beau\s+de\s+toilette\b/gi,' edt ')
  .replace(/\beau\s+de\s+cologne\b/gi,' edc ').replace(/\bextrait\s+de\s+parfum\b/gi,' extrait ').replace(/\bpure\s+parfum\b/gi,' parfum ');
const OZ_ML=29.5735;
const mMl=o=>o==null?null:Math.round(o*OZ_ML);
function mTaille(t){
  let m=t.match(/(\d+(?:[.,]\d+)?)\s*(ml|millilitres?)\b/i);
  if(m) return {ml:Math.round(parseFloat(m[1].replace(',','.'))), brut:m[0]};
  /* « 0z » : la lecture d'une photo confond volontiers le o et le zéro */
  m=t.match(/(\d+(?:[.,]\d+)?)\s*(oz|0z|onces?|fl\.?\s*oz)\b/i);
  if(m) return {ml:mMl(parseFloat(m[1].replace(',','.'))), brut:m[0]};
  /* « good girl 80 » : un nombre seul entre 5 et 500 est presque toujours une
     contenance en ml. En dessous de 5 c'est une quantité, au-dessus c'est un prix. */
  m=t.match(/(?:^|\s)(\d{2,3})(?:\s|$)/);
  if(m){ const n=+m[1]; if(n>=5&&n<=500) return {ml:n, brut:m[1], devine:true}; }
  return null;
}
/* la quantité : « 2 sauvage », « sauvage x3 », « sauvage *2 », « 3 x sauvage » */
function mQte(t){
  let m=t.match(/[x*×]\s*(\d{1,3})\s*$/i);            if(m) return {q:+m[1], brut:m[0]};
  m=t.match(/^\s*(\d{1,3})\s*[x*×]\s+/i);             if(m) return {q:+m[1], brut:m[0]};
  m=t.match(/^\s*(\d{1,3})\s+(?=[a-zà-ÿ])/i);         if(m) return {q:+m[1], brut:m[0]};
  m=t.match(/\b(?:qte|qty|quantite|quantité)\s*:?\s*(\d{1,3})\b/i); if(m) return {q:+m[1], brut:m[0]};
  return null;
}

/* La quantité d'une ligne de TABLEAU (Excel, CSV, PDF) : le code-barres, le nom, la contenance, la marque, le type,
   le prix, la quantité, le total — séparés par des blancs doubles. Igal, 13 oct. 2026 : Sam importe la liste d'un client
   et « Barakkat Rouge 540 Extrait » devient 540 flacons (le « 540 » du NOM était lu comme la quantité) ; « Azzaro Club
   Women 75 … 24 3 » donnait 24 (le prix) ; « Oud Mood … 13 2 » avait été sauvé par hasard (13 pris pour une contenance).
   On ne regarde donc que les CASES purement numériques (jamais le texte du nom) ; et si la ligne a un prix et un total,
   la quantité est la case qui les relie : prix × quantité = total. */
function mCases(brut){
  const c=String(brut||'').split(/\s{2,}/).map(x=>x.trim()).filter(Boolean);
  if(c.length<4) return null;
  return c.filter(x=>/^\d+(?:[.,]\d+)?$/.test(x)&&x.replace(/\D/g,'').length<8).map(x=>parseFloat(x.replace(',','.')));
}
/* prix unitaire × quantité = total : la ligne d'un tableau (devis Lightspeed, Excel) dit elle-même
   son prix et sa quantité. Renvoie {p,q} ou null. Le prix est celui du FICHIER : le client a reçu
   une cote à ce prix-là, c'est lui qui compte, pas le prix de l'ERP (Igal, 13 oct. 2026). */
function mPrixQteTableau(brut){
  const N=mCases(brut); if(!N) return null;
  for(let k=N.length-1;k>=2;k--) for(let j=1;j<k;j++){
    if(!Number.isInteger(N[j])||N[j]<1||N[j]>999) continue;
    for(let i=j-1;i>=0;i--) if(N[i]>0&&Math.abs(N[i]*N[j]-N[k])<=0.011) return {p:N[i],q:N[j]}; }
  return null;
}
function mQteTableau(brut,taille){
  const N=mCases(brut); if(!N) return null;
  const pq=mPrixQteTableau(brut); if(pq) return pq.q;
  /* pas de total : le premier petit entier des cases numériques, hors contenance */
  let t=N.join('  '); if(taille&&taille.brut) t=t.replace(taille.brut,' ');
  const m=t.match(/(?:^|\s)(\d{1,3})(?:\s|$)/); return m?+m[1]:null;
}

/* Le catalogue préparé une fois : marque, nom et contenance en millilitres. */
let M_CAT=null;
function mCatalogue(){
  if(M_CAT) return M_CAT;
  M_CAT=[];
  /* Le nom court (celui des listes) perd ce qui distingue les variantes : « Bleu »
     vaut pour l'EDP, l'EDT et le Parfum. Pour reconnaître une ligne de client,
     on prend le nom complet du catalogue ET le type (edp, edt, parfum…) : quand
     le client écrit « bleu de chanel edp », c'est ce mot-là qui tranche. */
  /* On lit le catalogue brut (D_TOUS) et pas l'index de la page : chaque page
     range son index à sa façon, et la contenance n'est pas toujours au même
     endroit — se tromper de colonne, c'est prendre un prix pour des onces. */
  let rows=[]; try{ rows=(typeof D_TOUS==='function'?D_TOUS():(window.D_PROD||[])); }catch(e){}
  if(rows.length){
    rows.forEach(r=>{ const cle=r[15]; if(!cle||!IDX[cle]) return;
      const oz=parseFloat(String(r[3]||'').replace(',','.'));
      const tout=mNorm(r[2])+' '+mNorm(mTypes(r[13]))+' '+mNorm(mTypes(r[1]))+' '+mNorm(r[4]);
      M_CAT.push({cle, marque:mNorm(r[2]), nom:mNorm(r[13]||r[1]),
        mots:new Set(tout.split(' ').filter(w=>w&&!/^\d+([.,]\d+)?$/.test(w)&&!M_VIDES.has(w))),
        type:mNorm(r[4]),
        ml:isFinite(oz)?mMl(oz):null}); });
    M_CAT.forEach(p=>{ p.longs=[...p.mots].filter(x=>x.length>=4); });
    return M_CAT;
  }
  /* sans catalogue brut : l'index de Ventes ([bc, nom, marque, oz, …]) */
  for(const cle in IDX){ const v=IDX[cle];
    const oz=parseFloat(String(v[3]||'').replace(',','.'));
    const tout=mNorm(v[2])+' '+mNorm(v[1]);
    M_CAT.push({cle, marque:mNorm(v[2]), nom:mNorm(v[1]),
      mots:new Set(tout.split(' ').filter(w=>w&&!/^\d+([.,]\d+)?$/.test(w))),
      ml:isFinite(oz)?mMl(oz):null});
  }
  M_CAT.forEach(p=>{ p.longs=[...p.mots].filter(x=>x.length>=4); });
  return M_CAT;
}

/* Le score : combien des mots du client se retrouvent dans le produit.
   Un mot entier vaut plus qu'un début de mot, la marque compte double, et une
   contenance qui ne correspond pas fait chuter le score — un 50 ml et un 100 ml
   sont deux produits différents, à deux prix différents. Se tromper là-dessus
   coûte plus cher que de ne rien proposer. */
function mScore(mots, taille, p){
  if(!mots.length) return 0;
  let pts=0, tot=0;
  mots.forEach(w=>{
    if(/^(edp|edt)$/.test(w)) return;            /* le type se juge à part, ci-dessous */
    const poids = w.length<=2 ? 0.4 : 1;
    tot += poids;
    if(p.mots.has(w)) pts += poids * (p.marque.split(' ').includes(w) ? 1.25 : 1);
    else if((p.longs||[...p.mots].filter(x=>x.length>=4)).some(x=>x.startsWith(w)||w.startsWith(x))) pts += poids*0.6;
  });
  if(!tot) return 0;
  let sc = pts/(tot*1.05);
  /* le type (edp, edt, parfum) tranche entre deux variantes du même nom */
  const typ=mots.find(w=>/^(edp|edt|edc|parfum|extrait|cologne|intense|elixir)$/.test(w));
  if(typ && p.type){ if(p.type===typ || (typ==='parfum'&&p.type==='p')) sc*=1.08; else if(/^(edp|edt|edc)$/.test(typ) && /^(edp|edt|edc|p)$/.test(p.type)) sc*=0.8; }
  if(taille && taille.ml!=null){
    if(p.ml==null) sc *= 0.75;
    else { const d=Math.abs(p.ml-taille.ml);
           sc *= d<=6 ? 1.15 : d<=15 ? 0.9 : 0.35; }
  }
  /* pas de plafond : deux produits « parfaits » ne le sont pas autant l'un que
     l'autre — « Le Male Elixir » et « Le Male Elixir Absolu » doivent se départager */
  return sc;
}

/* l'index des mots du catalogue : mot → produits qui le portent */
function mIndex(){
  const C=mCatalogue();
  if(C._ix&&C._ix.n===C.length) return C._ix;
  const m=new Map(); C.forEach(p=>p.mots.forEach(w=>{ let a=m.get(w); if(!a) m.set(w,a=[]); a.push(p); }));
  C._ix={n:C.length,m,vocab:[...m.keys()].filter(x=>x.length>=4)};
  return C._ix;
}
function mCandidats(mots){
  const ix=mIndex(), S=new Set();
  mots.forEach(w=>{
    if(/^(edp|edt)$/.test(w)) return;          /* ne rapporte aucun point (voir mScore) */
    (ix.m.get(w)||[]).forEach(p=>S.add(p));
    ix.vocab.forEach(x=>{ if(x.startsWith(w)||w.startsWith(x)) (ix.m.get(x)||[]).forEach(p=>S.add(p)); });
  });
  return S;
}
/* le texte d'une ligne, prêt à comparer : ses mots, sa contenance, sa quantité */
function mPrepare(texte){
  const brut=String(texte||'');
  const taille=mTaille(brut), qte=mQte(brut);
  /* on retire de la recherche ce qui a servi à lire la quantité et la contenance :
     sinon « 2 » et « 100 » comptent comme des mots du nom du parfum */
  let t=brut;
  if(qte) t=t.replace(qte.brut,' ');
  if(taille) t=t.replace(taille.brut,' ');
  const mots=[...new Set(mMarques(mNorm(mTypes(t))).split(' ').filter(w=>w && !/^\d+$/.test(w) && w.length>1 && (!M_VIDES.has(w) || /^(edp|edt)$/.test(w))))];
  return {brut,taille,qte,mots};
}
/* le score d'un texte face à UN produit (sans parcourir tout le catalogue) */
function mScoreCle(texte,cle){
  const C=mCatalogue(); if(!C._k||C._k.n!==C.length){ C._k={n:C.length,m:new Map(C.map(x=>[x.cle,x]))}; }
  const p=C._k.m.get(cle); if(!p) return 0;
  const P=mPrepare(texte); return mScore(P.mots,P.taille,p);
}
function mCherche(texte){
  const alias=lit(K_ALIASN,{}); const A=(alias&&typeof alias==='object')?alias:{};
  const {brut,taille,qte,mots}=mPrepare(texte);
  const cle0=mNorm(brut);

  if(A[cle0] && IDX[A[cle0]]) return {mots, taille, qte, cands:[{cle:A[cle0], sc:1}], appris:true};
  /* un code-barres dans la ligne (liste Excel, export, etiquette recopiee) : on
     ne devine plus rien, c'est LUI la reference. La quantite est alors le premier
     petit entier de la ligne qui n'est ni le code ni la contenance. */
  const bcTok=(brut.match(/\b\d{8,14}\b/g)||[]).map(x=>cleDeBC(x)).find(Boolean);
  if(bcTok){
    let q=qte?qte.q:null;
    if(q==null) q=mQteTableau(brut,taille);
    const pq=mPrixQteTableau(brut);
    if(q==null){ let t2=brut.replace(/\b\d{8,14}\b/g,' '); if(taille) t2=t2.replace(taille.brut,' ');
      const m=t2.match(/(?:^|\s)(\d{1,3})(?:\s|$)/); if(m) q=+m[1]; }
    return {mots, taille, qte:q!=null?{q}:qte, cands:[{cle:bcTok, sc:1}], appris:true, px:pq?pq.p:null};
  }

  /* un code-barres est écrit, mais aucune fiche de l'ERP ne le porte (Sam, 1er oct. 2026 :
     « si le code-barres n'est pas identique aux références de l'ERP, demander à Sam de confirmer
     la référence ») : on cherche quand même par le nom, mais on ne choisira pas tout seul */
  const bcInconnu=(brut.match(/\b\d{8,14}\b/g)||[])[0]||'';
  let q2=qte;
  if(bcInconnu&&!q2){ const qt=mQteTableau(brut,taille); if(qt!=null) q2={q:qt}; }
  if(bcInconnu&&!q2){ let t2=brut.replace(/\b\d{8,14}\b/g,' '); if(taille) t2=t2.replace(taille.brut,' ');
    const m=t2.match(/(?:^|\s)(\d{1,3})(?:\s|$)/); if(m) q2={q:+m[1]}; }
  const R=[];
  /* seuls les produits qui partagent au moins un mot (ou un début de mot) avec la ligne
     peuvent avoir un score : les autres valent 0. On ne note donc qu'eux (3 oct. 2026 :
     une price list de 700 lignes inconnues parcourait 700 fois les 3 800 fiches). */
  mCandidats(mots).forEach(p=>{ const sc=mScore(mots,taille,p); if(sc>0.34) R.push({cle:p.cle, sc}); });
  R.sort((a,b)=>b.sc-a.sc);
  return {mots, taille, qte:q2, cands:R.slice(0,8), appris:false, bcInconnu, px:(bcInconnu?(mPrixQteTableau(brut)||{}).p:null)};
}

'''
