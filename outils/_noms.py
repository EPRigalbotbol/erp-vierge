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
const M_VIDES=new Set(['de','du','des','la','le','les','l','d','et','en','pour','par','the','of','and','for','by','in','a','au','aux','un','une','with','avec','ml','oz','x']);

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
    else if([...p.mots].some(x=>x.length>=4 && (x.startsWith(w)||w.startsWith(x)))) pts += poids*0.6;
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

function mCherche(texte){
  const alias=lit(K_ALIASN,{}); const A=(alias&&typeof alias==='object')?alias:{};
  const brut=String(texte||'');
  const cle0=mNorm(brut);
  const taille=mTaille(brut), qte=mQte(brut);
  /* on retire de la recherche ce qui a servi à lire la quantité et la contenance :
     sinon « 2 » et « 100 » comptent comme des mots du nom du parfum */
  let t=brut;
  if(qte) t=t.replace(qte.brut,' ');
  if(taille) t=t.replace(taille.brut,' ');
  const mots=mNorm(mTypes(t)).split(' ').filter(w=>w && !/^\d+$/.test(w) && w.length>1 && (!M_VIDES.has(w) || /^(edp|edt)$/.test(w)));

  if(A[cle0] && IDX[A[cle0]]) return {mots, taille, qte, cands:[{cle:A[cle0], sc:1}], appris:true};
  /* un code-barres dans la ligne (liste Excel, export, etiquette recopiee) : on
     ne devine plus rien, c'est LUI la reference. La quantite est alors le premier
     petit entier de la ligne qui n'est ni le code ni la contenance. */
  const bcTok=(brut.match(/\b\d{8,14}\b/g)||[]).map(x=>cleDeBC(x)).find(Boolean);
  if(bcTok){
    let q=qte?qte.q:null;
    if(q==null){ let t2=brut.replace(/\b\d{8,14}\b/g,' '); if(taille) t2=t2.replace(taille.brut,' ');
      const m=t2.match(/(?:^|\s)(\d{1,3})(?:\s|$)/); if(m) q=+m[1]; }
    return {mots, taille, qte:q!=null?{q}:qte, cands:[{cle:bcTok, sc:1}], appris:true};
  }

  const R=[];
  mCatalogue().forEach(p=>{ const sc=mScore(mots,taille,p); if(sc>0.34) R.push({cle:p.cle, sc}); });
  R.sort((a,b)=>b.sc-a.sc);
  return {mots, taille, qte, cands:R.slice(0,8), appris:false};
}

'''
