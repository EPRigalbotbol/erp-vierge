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
/* 22 oct. 2026 — LA VENTE 21057 EFFACÉE. Le point de comparaison était UN PAR MAGASIN (_REF[cle]) : la moindre lecture
   faite ailleurs dans le même onglet (l'enregistrement automatique des ventes relit factures-v1, le stock, le journal)
   le remplaçait. La page, elle, gardait sa copie d'avant. À son enregistrement suivant, la règle du 18 octobre voyait
   des lignes « dans le repère mais plus dans la copie » et les retirait — la vente du site, sa sortie de stock et ses
   deux lignes de journal ont disparu sans un mot. Le repère est désormais attaché à CHAQUE COPIE lue (_SNAP) : une
   page ne retire que ce qu'elle a elle-même retiré de SA copie. _REF[cle] reste le repère de secours pour une valeur
   construite sans lecture. */
const _SNAP=(typeof WeakMap==='function')?new WeakMap():null;
const _repere=(cle,val)=>(_SNAP&&val&&typeof val==='object'&&_SNAP.has(val))?_SNAP.get(val):_REF[cle];
function base(cle,val){ const c=_cp(val); _REF[cle]=c; if(_SNAP&&val&&typeof val==='object'){ try{ _SNAP.set(val,_cp(c)); }catch(e){} } return val; }
/* identite d'une ligne, pour reconnaitre la meme entree ecrite par l'autre onglet */
const _IDdef=x=>_sig(x);
/* Les lignes ajoutées par CET onglet reçoivent un identifiant unique avant d'être écrites.
   Sans lui, deux lignes de journal écrites dans la même milliseconde (une facture de 30
   lignes en écrit 30 d'un coup) avaient la même identité et se dévoraient entre elles. */
const _UID={'crm-journal-v1':1,'factures-v1':1,'ajustements-v1':1,'articles-ajoutes-v1':1,
            'caisse-file-v1':1,'expeditions-v1':1};
let _seq=0;
const _neuf=()=>'x'+Date.now().toString(36)+(++_seq).toString(36)+Math.random().toString(36).slice(2,6);
const _ID={
  /* 18 oct. 2026 (Coach Floral) : les articles ajoutés à la main n'avaient pas d'identité ici (toute la ligne servait d'identité),
     alors que le serveur les reconnaît par leur _i : une suppression envoyée « en delta » partait avec la mauvaise identité et le
     serveur ne retirait rien — en silence. Même identité des deux côtés, désormais. */
  'articles-ajoutes-v1': x=>x._i||_sig(x),
  'crm-journal-v1': x=>x._i||[x.t,x.act||'',x.lib||'',x.ref||'',x.bc||''].join('|'),
  'factures-v1'   : x=>x._i||x.id||[x.num||'',x.d||'',x.montant].join('|'),
  'ajustements-v1': x=>x._i||[x.t,x.cle||''].join('|'),
  /* la file des ventes de caisse : l'identifiant vient du serveur, on ne le refabrique jamais */
  'caisse-file-v1' : x=>x._i||'',
  /* les commandes à expédier : même identifiant que dans la file, il vient du serveur */
  'expeditions-v1' : x=>x._i||''};
const _MAX={'crm-journal-v1':4000,'ajustements-v1':4000};
/* pour ces magasins, on garde les plus RÉCENTS quand le plafond est atteint */
const _DATE={'crm-journal-v1':x=>x.t||'','ajustements-v1':x=>x.t||''};
/* magasins objet dont chaque valeur est elle-meme une liste a fusionner */
const _IMBR={'ventes-v1'         : x=>x._i||[x.d||'',x.num||'',x.q,x.p,x.c||'',x.k||''].join('|'),
             'prix-achat-hist-v1': x=>[x.d||'',x.p,x.f||'',x.q,x.num||'',x.src||''].join('|'),
             'caisse-especes-v1' : x=>[x.t||'',x.u||'',x.montant].join('|'),
             'caisse-especes-pc-v1' : x=>[x.t||'',x.u||'',x.montant].join('|')};   /* les récoltes de la caisse de Perfume City (4 nov. 2026) */   /* les récoltes d'espèces (24 oct. 2026) */
/* magasins dont une sous-clé est elle-même une carte à fusionner clé par clé */
const _SOUSMAP={'stock-externe-v1':['q']};
/* magasins ou chaque fiche est un paquet de champs : on fusionne champ par champ,
   pour que deux onglets puissent corriger deux champs differents du meme produit */
const _CHAMPS={'pc-stock-v1':1,'testeurs-pc-v1':1,'fiches-modifiees-v1':1,'demandes-pc-v1':1,'clients-v1':1,'reglements-v1':1,'fournisseurs-v1':1,'marche-v1':1,'photos-perso-v1':1,'parfums-a-racheter-v1':1};
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
  /* 18 oct. 2026 (Igal : « Coach Floral, je l'avais supprimé, Sam le voit encore ») : une ligne que CET onglet avait
     déjà lue (ref) et n'a pas touchée, mais qui n'est plus sur le disque, a été SUPPRIMÉE AILLEURS — on ne la remet pas.
     Seules les lignes que cet onglet ne connaissait pas (absentes de ref) sont vraiment nouvelles. */
  (cour||[]).forEach(x=>{ const i=idf(x); if(!vus.has(i)&&!mR.has(i)){ out.push(x); vus.add(i); } });
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
  const ref=_repere(cle,val);
  /* on marque les lignes que cet onglet vient d'ajouter, pour qu'elles restent reconnaissables */
  if(_UID[cle]&&Array.isArray(val)){
    const deja=new Set((Array.isArray(ref)?ref:[]).map(x=>_sig(x)));
    val.forEach(x=>{ if(x&&typeof x==='object'&&!x._i&&!deja.has(_sig(x))){ x._i=_neuf();
      if(cle==='crm-journal-v1'){ /* d'où vient l'action, et avec quel rôle : le journal le montre */
        if(!x.pg) x.pg=(location.pathname.split('/').pop()||'').replace(/\.html$/,'')||'catalogue';
        if(!x.r){ try{ const sx=(typeof session==='function')?session():null; if(sx&&sx.role) x.r=sx.role; }catch(e){} } } } });
  }
  const sortie=fusionne(cle,_dq(cle,Array.isArray(val)?[]:{}),ref,val);
  /* 30 sept. 2026 : quand la mémoire du navigateur est pleine, l'enregistrement était perdu
     EN SILENCE — ni rangé ici, ni envoyé au serveur (la « new order » de Sam). Désormais on
     l'envoie quand même au serveur, et on prévient. */
  try{ localStorage.setItem(cle,typeof sortie==='string'?sortie:JSON.stringify(sortie)); }
  catch(e){ try{ if(typeof _syPlein==='function') _syPlein(); }catch(_){} }
  _adopte(val,sortie);
  /* `avant` = le repère de CETTE copie : ce que le serveur retire en delta, c'est ce que cette page a retiré de sa
     copie, jamais ce qu'une autre page a ajouté entre-temps */
  const avant=ref;
  const c=_cp(val); _REF[cle]=c; if(_SNAP&&val&&typeof val==='object'){ try{ _SNAP.set(val,_cp(c)); }catch(e){} }
  _apresEcrit.forEach(f=>{ try{ f(cle,val,avant); }catch(e){} });
  return val;
}
/* Deux pages (Factures, Étude de cote) tournent en module : leurs fonctions ne sont
   pas visibles des scripts communs (menu, langue). Le menu renommé ne s'enregistrait
   donc pas depuis ces pages, sans rien dire (Igal, 27 sept. 2026 : « elle reste à
   Étude de cote »). On les rend visibles partout. */
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
/* La boîte (x, y, largeur, hauteur) qui contient le flacon, ou null s'il n'y a rien à rogner. */
function _boiteFlacon(d,w,h){
  const px=(x,y)=>{ const i=(y*w+x)*4; return [d[i],d[i+1],d[i+2]]; };
  const C=[px(0,0),px(w-1,0),px(0,h-1),px(w-1,h-1)];
  const bg=[0,1,2].map(j=>Math.round(C.reduce((t,c)=>t+c[j],0)/4));
  if(C.some(c=>Math.max(Math.abs(c[0]-bg[0]),Math.abs(c[1]-bg[1]),Math.abs(c[2]-bg[2]))>40)) return null;
  const lig=new Array(h).fill(0), col=new Array(w).fill(0);
  for(let y=0;y<h;y++) for(let x=0;x<w;x++){
    const i=(y*w+x)*4;
    if(Math.max(Math.abs(d[i]-bg[0]),Math.abs(d[i+1]-bg[1]),Math.abs(d[i+2]-bg[2]))>34){ lig[y]++; col[x]++; }
  }
  const premier=(T,n)=>{ for(let i=0;i<T.length;i++) if(T[i]>=n) return i; return -1; };
  const dernier=(T,n)=>{ for(let i=T.length-1;i>=0;i--) if(T[i]>=n) return i; return -1; };
  const x0=premier(col,2), x1=dernier(col,2), y0=premier(lig,2), y1=dernier(lig,2);
  if(x0<0||y0<0||x1<=x0||y1<=y0) return null;
  let bw=x1-x0+1, bh=y1-y0+1;
  if(bw*bh<0.03*w*h) return null;                       /* trois grains de poussière : on ne rogne pas sur eux */
  const m=Math.round(0.04*Math.max(bw,bh));
  const X=Math.max(0,x0-m), Y=Math.max(0,y0-m), X2=Math.min(w,x1+1+m), Y2=Math.min(h,y1+1+m);
  if((X2-X)>=0.97*w&&(Y2-Y)>=0.97*h) return null;       /* déjà plein cadre */
  return [X,Y,X2-X,Y2-Y];
}
/* UNE PHOTO CHOISIE À LA MAIN (Igal, 17 oct. 2026 : « changer la photo du produit ») : l'image est
   redessinée plus petite (640 px au plus, fond blanc, JPEG) avant d'être gardée — une photo de
   téléphone fait plusieurs Mo et la mémoire du navigateur n'en garde que quelques-uns.
   Rend une promesse : l'adresse « data: » de l'image, ou une erreur lisible. */
function photoReduite(fichier,max){
  max=max||640;
  return new Promise((ok,ko)=>{
    if(!fichier||!/^image\//.test(fichier.type||'')){ ko(new Error('pas une image')); return; }
    const r=new FileReader();
    r.onerror=()=>ko(new Error('lecture impossible'));
    r.onload=()=>{
      const im=new Image();
      im.onerror=()=>ko(new Error('image illisible'));
      im.onload=()=>{
        try{
          /* Igal, 17 oct. 2026 : « elle est petite à l'intérieur, j'aimerais qu'elle soit vraiment dans le cadre ».
             Une photo trouvée sur Internet a presque toujours de larges marges blanches : on les rogne (le flacon
             remplit le cadre, avec une petite marge) avant de réduire. Le fond est reconnu aux quatre coins ; si les
             coins ne sont pas du même ton (photo d'ambiance, dégradé), on ne rogne rien. */
          const W=im.width, H=im.height, k0=Math.min(1,800/Math.max(W,H));
          const aw=Math.max(1,Math.round(W*k0)), ah=Math.max(1,Math.round(H*k0));
          const a=document.createElement('canvas'); a.width=aw; a.height=ah;
          const ga=a.getContext('2d'); ga.fillStyle='#fff'; ga.fillRect(0,0,aw,ah); ga.drawImage(im,0,0,aw,ah);
          let sx=0, sy=0, sw=W, sh=H;
          const box=_boiteFlacon(ga.getImageData(0,0,aw,ah).data,aw,ah);
          if(box){ sx=box[0]/k0; sy=box[1]/k0; sw=box[2]/k0; sh=box[3]/k0; }
          const k=Math.min(max/Math.max(sw,sh),box?1.5:1);
          const w=Math.max(1,Math.round(sw*k)), h=Math.max(1,Math.round(sh*k));
          const c=document.createElement('canvas'); c.width=w; c.height=h;
          const g=c.getContext('2d'); g.fillStyle='#fff'; g.fillRect(0,0,w,h);
          g.drawImage(im,sx,sy,sw,sh,0,0,w,h);
          ok(c.toDataURL('image/jpeg',0.86));
        }catch(e){ ko(e); }
      };
      im.src=r.result;
    };
    r.readAsDataURL(fichier);
  });
}
/* « PARFUMS À RACHETER » (Igal, 7 nov. 2026 : « dans le tableau de bord, une partie qui regroupe tous les parfums à
   recommander, pour éditer une liste et l'envoyer à un fournisseur en lui demandant une offre de prix »). Une liste
   partagée (parfums-a-racheter-v1, une fiche par parfum, synchronisée par le cockpit comme les autres magasins) :
   la tâche « Recommander » y met le parfum d'un clic ; le stock bas du tableau de bord aussi. Un parfum retiré de la
   liste n'en sort pas : il passe « retiré » et la tâche reste ignorée (sinon Sam la reverrait tous les matins).
   Une réception enregistrée dans Factures sort le parfum de la liste. */
const K_RACH='parfums-a-racheter-v1';
function rachLit(){ let R={}; try{ R=lit(K_RACH,{})||{}; }catch(e){ R={}; } return (R&&typeof R==='object'&&!Array.isArray(R))?R:{}; }
function rachAjoute(cle,inf){ if(!cle) return false; const R=rachLit(), o=R[cle]||{}, i=inf||{};
  const par=(typeof NOM_UTIL==='string'&&NOM_UTIL)?NOM_UTIL:(o.par||'');
  const n=Object.assign({},o,{bc:String(i.bc||o.bc||''),ref:String(i.ref||o.ref||''),etat:'liste',t:new Date().toISOString(),par});
  if(i.q!=null&&i.q!=='') n.q=Math.max(1,Math.round(+i.q)||1); delete n.tr; R[cle]=n; ecrit(K_RACH,R); return true; }
function rachQuantite(cle,q){ const R=rachLit(); if(!R[cle]) return false; R[cle]=Object.assign({},R[cle],{q:Math.max(1,Math.round(+q)||1)}); ecrit(K_RACH,R); return true; }
function rachRetire(cle){ const R=rachLit(); if(!R[cle]) return false; R[cle]=Object.assign({},R[cle],{etat:'retire',tr:new Date().toISOString()}); ecrit(K_RACH,R); return true; }
function rachRecu(cles){ const R=rachLit(); let n=0; (cles||[]).forEach(c=>{ if(c&&R[c]&&R[c].etat==='liste'){ delete R[c]; n++; } }); if(n) ecrit(K_RACH,R); return n; }
const rachListe=()=>Object.entries(rachLit()).filter(([,o])=>o&&o.etat==='liste').map(([cle,o])=>Object.assign({cle},o));
/* RENVOYER À SHOPIFY LE STOCK D'UNE RÉCEPTION PERFUME CITY, depuis Tâches (Igal, 7 nov. 2026 : chaque tâche se règle sur place).
   Le même envoi que Factures (pcEnvoiFacture) : le cockpit ajoute les quantités sur Shopify, la facture note le résultat
   (pcShopify), le journal aussi. Rend {ok, bon, mal, raison} ; rien n'est compté deux fois (le cockpit reconnaît la clé). */
async function pcRenvoiFacture(fid){
  let F=[]; try{ F=lit('factures-v1',[])||[]; }catch(e){ F=[]; } if(!Array.isArray(F)) F=[];
  const f=F.find(x=>x&&x.id===fid); if(!f) return {ok:false,raison:'facture introuvable'};
  const vend=l=>l.pcVend!=null?+l.pcVend:+l.pc;
  const lg=(f.lignes||[]).filter(l=>l&&vend(l)>0&&l.bc); if(!lg.length) return {ok:false,raison:'rien pour Perfume City sur cette facture'};
  const par=(typeof NOM_UTIL==='string'&&NOM_UTIL)?NOM_UTIL:'(non renseigné)';
  const maj=o=>{ f.pcShopify=Object.assign({},o,{t:new Date().toISOString()}); try{ ecrit('factures-v1',F); }catch(e){} };
  const jou=lib=>{ try{ const J=lit('crm-journal-v1',[])||[]; J.push({t:new Date().toISOString(),u:par,act:'site',lib,n:lg.length,impact:0,det:[]}); ecrit('crm-journal-v1',J); }catch(e){} };
  let j;
  try{
    if(typeof CK_URL==='undefined'||typeof ckTok!=='function'||!ckTok()) throw new Error('hors ligne');
    const r=await fetch(CK_URL+'/api/o/'+CK_ORG+'/shopify/stock-ajoute',{method:'POST',headers:{'Content-Type':'application/json',Authorization:'Bearer '+ckTok()},
      body:JSON.stringify({cle:f.id,items:lg.map(l=>({bc:l.bc,ajout:vend(l),nom:l.ref}))})});
    j=await r.json().catch(()=>({})); if(!r.ok) throw new Error(j.erreur||('erreur '+r.status));
  }catch(e){ const raison=(e&&e.message)||'erreur'; maj({etat:'echec',raison}); jou('réception '+(f.num||'')+' : stock de Perfume City NON envoyé à Shopify ('+raison+') — depuis Tâches'); return {ok:false,raison}; }
  const L=j.lignes||[], bon=L.filter(l=>l.etat==='ok'||l.etat==='deja'), mal=L.filter(l=>!(l.etat==='ok'||l.etat==='deja'||l.etat==='ignore'));
  maj({etat:mal.length?'partiel':'ok',lignes:L.map(l=>({bc:l.bc,nom:l.nom,etat:l.etat,raison:l.raison,avant:l.avant,apres:l.apres}))});
  jou('réception '+(f.num||'')+' : stock de Perfume City envoyé à Shopify ('+bon.length+' ok'+(mal.length?', '+mal.length+' non':'')+') — depuis Tâches');
  /* 8 nov. 2026 (Igal : « ça bloque toujours ces histoires d'envoyer sur Shopify — c'est un parfum, je comprends pas pourquoi il passe
     pas ») : un parfum absent de la boutique Shopify ne peut pas y recevoir de stock. On rend ses clés (absents) : la page propose de le
     créer chez Perfume City tout de suite, puis renvoie la réception. */
  const absBc=new Set(mal.filter(l=>l.etat==='absent').map(l=>String(l.bc||'').replace(/^0+/,'')));
  const absents=[...new Set(lg.filter(l=>absBc.has(String(l.bc||'').replace(/^0+/,''))).map(l=>l.cle).filter(Boolean))];
  return {ok:!mal.length,bon:bon.length,mal:mal.map(l=>(l.nom||l.bc)+' — '+(l.raison||l.etat)),absents};
}
/* LA FICHE DU PARFUM DANS UNE FENÊTRE, par-dessus la page en cours (Igal, 17 oct. 2026 : depuis une facture, puis
   depuis le détail d'une vente — « sans avoir à passer par le catalogue pour voir le produit »). C'est la fiche du
   Catalogue elle-même, ouverte en « mode cadre » (catalogue.html#cle=…&cadre=1) : mêmes champs, mêmes droits, même
   enregistrement. À la fermeture, `apres` est appelée pour que la page relise ce qui a pu changer. */
function ficheFenetre(cle,apres,plus){
  if(!cle||document.getElementById('fv-ov')) return;
  if(!document.getElementById('fv-css')){
    const st=document.createElement('style'); st.id='fv-css';
    st.textContent='.fv-ov{position:fixed;inset:0;z-index:95;background:rgba(23,23,29,.45);backdrop-filter:blur(2px);display:flex;justify-content:flex-end}'
      +'.fv-ov iframe{border:0;width:min(940px,100%);height:100%;background:var(--surface,#fff);box-shadow:-8px 0 30px rgba(0,0,0,.18)}';
    document.head.appendChild(st);
  }
  const ov=document.createElement('div'); ov.id='fv-ov'; ov.className='fv-ov';
  const fr=document.createElement('iframe'); fr.title='Fiche du parfum'; fr.src='catalogue.html#cle='+encodeURIComponent(cle)+'&cadre=1'+(plus||'');   /* plus : « &mel=1 » ouvre « Mettre en ligne » (tableau de bord) */
  ov.appendChild(fr); document.body.appendChild(ov);
  const ferme=()=>{ window.removeEventListener('message',onMsg); ov.remove(); try{ if(apres) apres(); }catch(e){} };
  const onMsg=e=>{ if(e.origin===location.origin&&e.data&&e.data.fiche==='fermee') ferme(); };
  window.addEventListener('message',onMsg);
  ov.addEventListener('click',e=>{ if(e.target===ov) ferme(); });
}
/* LA MISE EN LIGNE DES NOUVELLES RÉFÉRENCES, par-dessus la page en cours (Igal, 5 nov. 2026 : « à la validation d'une facture,
   proposer de mettre en ligne les nouveaux produits sans aller les chercher dans le Catalogue »). Même fenêtre que la fiche :
   c'est le Catalogue en mode cadre (catalogue.html#enligne=id1,id2&cadre=1) qui fait le travail, avec ses garde-fous. */
function enLigneFenetre(ids,apres,canaux){
  const L=(ids||[]).filter(Boolean); if(!L.length) return;
  const cs=(canaux||[]).filter(Boolean);
  cadreFenetre('#enligne='+encodeURIComponent(L.join(','))+(cs.length?'&canaux='+encodeURIComponent(cs.join(',')):'')+'&cadre=1',apres,'Mise en ligne');
}
/* 7 nov. 2026 : la même fenêtre pour poser des prix sur les canaux depuis Tâches (catalogue.html#prix=id&canaux=…&cadre=1) */
function prixCanauxFenetre(id,canaux,apres){
  if(!id) return;
  cadreFenetre('#prix='+encodeURIComponent(id)+'&canaux='+encodeURIComponent((canaux||[]).join(','))+'&cadre=1',apres,'Prix sur les canaux');
}
/* 7 nov. 2026 : une vente en attente à compléter, dans la même fenêtre (ventes.html#attente=<id>&cadre=1) */
function attenteFenetre(id,apres){ if(id) cadreFenetre('#attente='+encodeURIComponent(id)+'&cadre=1',apres,'Vente à compléter','ventes.html'); }
function cadreFenetre(hash,apres,titre,page){
  if(document.getElementById('fv-ov')) return;
  if(!document.getElementById('fv-css')){
    const st=document.createElement('style'); st.id='fv-css';
    st.textContent='.fv-ov{position:fixed;inset:0;z-index:95;background:rgba(23,23,29,.45);backdrop-filter:blur(2px);display:flex;justify-content:flex-end}'
      +'.fv-ov iframe{border:0;width:min(940px,100%);height:100%;background:var(--surface,#fff);box-shadow:-8px 0 30px rgba(0,0,0,.18)}';
    document.head.appendChild(st);
  }
  const ov=document.createElement('div'); ov.id='fv-ov'; ov.className='fv-ov';
  const fr=document.createElement('iframe'); fr.title=titre||'Catalogue'; fr.src=(page||'catalogue.html')+hash;
  ov.appendChild(fr); document.body.appendChild(ov);
  const ferme=()=>{ window.removeEventListener('message',onMsg); ov.remove(); try{ if(apres) apres(); }catch(e){} };
  const onMsg=e=>{ if(e.origin===location.origin&&e.data&&e.data.fiche==='fermee') ferme(); };
  window.addEventListener('message',onMsg);
  ov.addEventListener('click',e=>{ if(e.target===ov) ferme(); });
}
/* CHERCHER LA PHOTO SUR INTERNET (Igal, 17 oct. 2026 : « chercher la photo sur Internet, proposer un choix à Sam,
   qu'il puisse cliquer sur la photo et l'intégrer »). Une fenêtre : une case de recherche (préremplie), des miniatures ;
   un clic prend la photo, la réduit comme les autres et la rend. C'est le cockpit qui cherche et qui rapporte l'image
   (le navigateur n'a pas le droit de le faire seul). Rend une promesse : l'adresse « data: » de la photo, ou null si on ferme. */
function photoWeb(requete){
  const T=(typeof L3==='function')?L3:(f)=>f;
  return new Promise(fini=>{
    if(document.getElementById('pw-ov')){ fini(null); return; }
    if(!document.getElementById('pw-css')){
      const st=document.createElement('style'); st.id='pw-css';
      st.textContent='.pw-ov{position:fixed;inset:0;z-index:90;background:rgba(23,23,29,.55);backdrop-filter:blur(2px);display:flex;align-items:center;justify-content:center;padding:18px}'
      +'.pw{background:var(--surface,#fff);color:var(--ink,#17171d);border-radius:14px;width:min(780px,100%);max-height:100%;display:flex;flex-direction:column;box-shadow:0 20px 60px rgba(0,0,0,.3);overflow:hidden}'
      +'.pw-h{display:flex;justify-content:space-between;align-items:center;padding:16px 20px 10px}.pw-h h2{margin:0;font-size:18px}'
      +'.pw-x{border:0;background:none;font-size:26px;line-height:1;color:var(--ink-3,#777);cursor:pointer}.pw-x:hover{color:var(--iris,#5b3f8c)}'
      +'.pw-r{display:flex;gap:8px;padding:0 20px 10px}.pw-r input{flex:1;min-width:0;padding:9px 11px;border:1px solid var(--line,#ddd);border-radius:8px;font:inherit;font-size:14px;background:var(--surface,#fff);color:inherit}'
      +'.pw-r input:focus{border-color:var(--iris,#5b3f8c);outline:0;box-shadow:0 0 0 3px var(--iris-soft,#eee)}'
      +'.pw-r button{padding:9px 16px;border:0;border-radius:8px;background:var(--iris,#5b3f8c);color:#fff;font:inherit;font-size:14px;cursor:pointer}.pw-r button:disabled{opacity:.5;cursor:default}'
      +'.pw-m{padding:0 20px 8px;font-size:12.5px;color:var(--ink-3,#777);min-height:18px}.pw-m.bad{color:var(--bad,#c0392b)}.pw-m a{color:inherit}'
      +'.pw-g{display:grid;grid-template-columns:repeat(auto-fill,minmax(128px,1fr));gap:10px;padding:2px 20px 14px;overflow:auto;min-height:60px}'
      +'.pw-c{border:1px solid var(--line,#ddd);border-radius:10px;background:var(--surface-2,#faf9f7);padding:6px;cursor:pointer;display:flex;flex-direction:column;gap:5px;text-align:left;font:inherit;color:inherit}'
      +'.pw-c:hover,.pw-c:focus-visible{border-color:var(--iris,#5b3f8c);outline:0;box-shadow:0 0 0 3px var(--iris-soft,#eee)}'
      +'.pw-c .im{aspect-ratio:1/1;display:flex;align-items:center;justify-content:center;background:#fff;border-radius:6px;overflow:hidden}.pw-c img{max-width:100%;max-height:100%;object-fit:contain}'
      +'.pw-c small{font-size:10.5px;color:var(--ink-3,#777);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}'
      +'.pw-c.pris{opacity:.55;pointer-events:none}'
      +'.pw-n{padding:8px 20px 14px;font-size:11.5px;color:var(--ink-3,#777);border-top:1px solid var(--line,#ddd)}';
      document.head.appendChild(st);
    }
    const e=s=>String(s==null?'':s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
    const ov=document.createElement('div'); ov.id='pw-ov'; ov.className='pw-ov';
    ov.innerHTML='<div class="pw" role="dialog" aria-modal="true" aria-labelledby="pw-t">'
      +'<div class="pw-h"><h2 id="pw-t">'+e(T('Chercher la photo sur Internet','Find the photo on the Internet','Buscar la foto en Internet'))+'</h2><button type="button" class="pw-x" id="pw-x" aria-label="'+e(T('Fermer','Close','Cerrar'))+'">&times;</button></div>'
      +'<div class="pw-r"><input id="pw-q" autocomplete="off" aria-label="'+e(T('Recherche','Search','Búsqueda'))+'"><button type="button" id="pw-b">'+e(T('Chercher','Search','Buscar'))+'</button></div>'
      +'<div class="pw-m" id="pw-m" role="status"></div><div class="pw-g" id="pw-g"></div>'
      +'<div class="pw-n">'+e(T('Ces photos viennent d\'Internet : vérifie que tu as le droit de les utiliser. Clique sur celle qui convient.','These photos come from the Internet: check that you may use them. Click the one you want.','Estas fotos vienen de Internet: comprueba que puedes usarlas. Haz clic en la que te sirva.'))+'</div></div>';
    document.body.appendChild(ov);
    const g=id=>document.getElementById(id), msg=(m,mal)=>{ g('pw-m').textContent=m||''; g('pw-m').className='pw-m'+(mal?' bad':''); };
    g('pw-q').value=requete||'';
    let clos=false;
    const ferme=v=>{ if(clos) return; clos=true; document.removeEventListener('keydown',onKey); ov.remove(); fini(v||null); };
    const onKey=ev=>{ if(ev.key==='Escape') ferme(null); };
    document.addEventListener('keydown',onKey);
    g('pw-x').onclick=()=>ferme(null);
    ov.addEventListener('click',ev=>{ if(ev.target===ov) ferme(null); });
    const jeton=()=>{ try{ return (typeof ckTok==='function'&&ckTok())||''; }catch(x){ return ''; } };
    const hors=()=>{ const q=encodeURIComponent(g('pw-q').value.trim());
      return ' <a href="https://www.google.com/search?tbm=isch&q='+q+'" target="_blank" rel="noopener">'+e(T('Ouvrir la recherche d\'images dans un nouvel onglet','Open the image search in a new tab','Abrir la búsqueda de imágenes en una pestaña nueva'))+'</a>'; };
    const appel=async chemin=>{
      const t=jeton(); if(!t) throw new Error(T('Pas connecté au serveur : reconnecte-toi, ou utilise « Ajouter une photo ».','Not connected to the server: sign in again, or use "Add a photo".','Sin conexión al servidor: vuelve a entrar, o usa «Añadir una foto».'));
      return fetch(CK_URL+'/api/o/'+CK_ORG+chemin,{headers:{Authorization:'Bearer '+t}});
    };
    let enCours=false;
    const cherche=async()=>{
      const q=g('pw-q').value.trim(); if(q.length<3||enCours) { if(q.length<3) msg(T('Tape au moins trois lettres.','Type at least three letters.','Escribe al menos tres letras.'),true); return; }
      enCours=true; g('pw-b').disabled=true; g('pw-g').innerHTML=''; msg(T('Recherche en cours…','Searching…','Buscando…'));
      try{
        const r=await appel('/photos/cherche?q='+encodeURIComponent(q)); const j=await r.json().catch(()=>({}));
        if(!r.ok) throw new Error(j.erreur||('erreur '+r.status));
        const L=j.resultats||[];
        if(!L.length){ msg(T('Aucune photo trouvée. Change les mots de la recherche.','No photo found. Change the search words.','No se encontró ninguna foto. Cambia las palabras.'),true); }
        else{
          msg(L.length+' '+T('photos — clique sur la bonne.','photos — click the right one.','fotos — haz clic en la correcta.'));
          g('pw-g').innerHTML=L.map((x,i)=>'<button type="button" class="pw-c" data-i="'+i+'"><span class="im"><img src="'+e(x.mini)+'" alt="" loading="lazy" referrerpolicy="no-referrer"></span><small>'+e(x.site||x.titre||'')+(x.l&&x.h?' · '+x.l+'×'+x.h:'')+'</small></button>').join('');
          g('pw-g').querySelectorAll('.pw-c').forEach(b=>{ b.onclick=()=>prend(L[+b.dataset.i],b); b.querySelector('img').onerror=function(){ b.remove(); }; });
        }
      }catch(err){ g('pw-m').innerHTML=''; msg('',true); g('pw-m').className='pw-m bad'; g('pw-m').innerHTML=e((err&&err.message)||T('La recherche a échoué.','The search failed.','La búsqueda falló.'))+hors(); }
      enCours=false; g('pw-b').disabled=false;
    };
    const prend=async(x,b)=>{
      if(enCours) return; enCours=true; b.classList.add('pris'); msg(T('Je prends la photo…','Getting the photo…','Obteniendo la foto…'));
      let u=null;
      for(const adr of [x.image,x.mini]){
        try{
          const r=await appel('/photos/prend?u='+encodeURIComponent(adr)); if(!r.ok) continue;
          const bl=await r.blob(); u=await photoReduite(bl); if(u) break;
        }catch(err){ if(!jeton()){ msg(err.message,true); break; } }
      }
      enCours=false;
      if(u){ ferme(u); return; }
      b.classList.remove('pris'); msg(T('Cette photo n\'a pas pu être récupérée (le site la protège). Choisis-en une autre.','This photo could not be fetched (the site protects it). Pick another one.','No se pudo obtener esta foto (el sitio la protege). Elige otra.'),true);
    };
    g('pw-b').onclick=cherche; g('pw-q').onkeydown=ev=>{ if(ev.key==='Enter'){ ev.preventDefault(); cherche(); } };
    setTimeout(()=>{ g('pw-q').focus(); if((requete||'').trim().length>=3) cherche(); },30);
  });
}
/* L'HEURE, vue de la boutique : « 14:32 » à Miami, quel que soit l'ordinateur qui
   enregistre. Sert à horodater les ventes ; sans argument, c'est maintenant. */
function heureMiami(t){
  try{ const x=(t==null)?new Date():(t instanceof Date?t:new Date(t)); if(isNaN(x.getTime())) return '';
    return x.toLocaleTimeString('en-GB',{timeZone:'America/New_York',hour:'2-digit',minute:'2-digit',hour12:false}); }
  catch(e){ return ''; }
}

/* le jour à Miami d'un instant (« 2026-09-27T04:05:00Z » → « 2026-09-27 ») */
function jourMiami(t){
  try{ const x=(t==null)?new Date():(t instanceof Date?t:new Date(t)); if(isNaN(x.getTime())) return '';
    return x.toLocaleDateString('en-CA',{timeZone:'America/New_York'}); }
  catch(e){ return ''; }
}

/* Le jour et l'heure à Miami d'un instant enregistré (« 2026-09-25T02:56:00Z »
   → « 24/09/26 · 22:56 »). Igal, 25 sept. 2026 : « mets-moi tout à la même heure » —
   les horodatages étaient lus tels quels, donc en temps universel, avec un jour
   d'écart le soir. Vide si l'instant n'est pas lisible. */
function quandMiami(t){
  try{ const x=(t==null)?null:(t instanceof Date?t:new Date(t)); if(!x||isNaN(x.getTime())) return '';
    const j=x.toLocaleDateString('en-US',{timeZone:'America/New_York',day:'2-digit',month:'2-digit',year:'2-digit'});
    return j+' · '+heureMiami(x); }
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
/* (voir plus haut) visibles des scripts communs, même depuis une page en module ;
   on passe par la variable pour suivre un éventuel remplacement de lit */
try{ if(typeof window!=='undefined'){ if(!window.lit) window.lit=(k,d)=>lit(k,d); if(!window.ecrit) window.ecrit=(k,v)=>ecrit(k,v); if(!window._apresEcrit) window._apresEcrit=_apresEcrit; } }catch(e){}


/* Le catalogue complet : les références du fichier (D_PROD) + les articles ajoutés à la main
   (articles-ajoutes-v1), mis au même format. Chaque page qui indexe les produits passe par ici,
   sinon un article créé dans le catalogue n'existe ni pour les factures ni pour les ventes. */
/* 30 oct. 2026 : un nom, une marque, une contenance ou un type changés dans la fiche du Catalogue
   (fiches-modifiees-v1) ne se voyaient QUE dans le Catalogue — l'Inventaire, les Ventes et les
   Factures gardaient le nom du fichier de départ (« Nom (Clone de…) » chez
   l'un, « Nom » chez l'autre). Les lignes du fichier reçoivent l'identité de la fiche
   une fois pour toutes, à la première lecture ; le nom d'origine (colonne 1) ne bouge pas, il
   sert à reconnaître une vente du site et à chercher. */
let _identiteFaite=false;
function _identiteFiches(){
  if(_identiteFaite) return; _identiteFaite=true;
  let M={}; try{ M=_dq('fiches-modifiees-v1',{})||{}; }catch(e){ M={}; }
  if(!M||typeof M!=='object'||Array.isArray(M)) return;
  const col={nom:13,marque:2,ml:3,type:4,genre:5};
  (window.D_PROD||[]).forEach(r=>{ const m=r&&r[15]&&M[r[15]]; if(!m) return;
    for(const k in col){ if(m[k]!=null&&m[k]!=='') r[col[k]]=(k==='type'||k==='genre')?String(m[k]).toUpperCase():String(m[k]); } });
}
function D_TOUS(){
  _identiteFiches();
  const A=_dq('articles-ajoutes-v1',[]); const L=Array.isArray(A)?A:[];
  let M={}; try{ M=_dq('fiches-modifiees-v1',{})||{}; }catch(e){ M={}; }
  const n=v=>(v==null||v==='')?null:+v;
  const rows=L.map((o,i)=>{ const m=(M&&M[o.id])||{}, nom=(m.nom!=null&&m.nom!=='')?m.nom:(o.nom||'');
    return [String(o.bc||'').trim(),o.nom||'',m.marque||o.marque||'',String(m.ml!=null&&m.ml!==''?m.ml:(o.ml||'')).trim(),String(m.type||o.type||'').toUpperCase(),
    String(m.genre||o.genre||'').toUpperCase(),n(o.qte)||0,n(o.pvr),n(o.pvw),'',0,[],n(o.pa),nom,'',o.id||('a'+i),null,null]; });
  return (window.D_PROD||[]).concat(rows);
}

/* Les codes-barres extraits d'une case COLLÉE du fichier de Sam (colonne 19 des données,
   voir build_data.py) : la fiche garde sa case telle quelle — sa clé en dépend — mais
   chacun des deux codes doit la retrouver. cle → codes, sans zéros de tête. */
let _BCX=null;
function bcExtra(){
  if(!_BCX){ _BCX={}; try{
    (window.D_PROD||[]).forEach(r=>{ if(r&&r[15]&&Array.isArray(r[19])&&r[19].length) _BCX[r[15]]=r[19].map(x=>String(x).replace(/^0+/,'')); });
    /* la page Inventaire n'a que ses propres lignes (colonne 12) */
    (window.D_INV||[]).forEach(r=>{ if(r&&r[9]&&Array.isArray(r[12])&&r[12].length) _BCX[r[9]]=r[12].map(x=>String(x).replace(/^0+/,'')); });
  }catch(e){} }
  return _BCX;
}
function cleParBCX(n){ n=String(n||'').replace(/[^0-9]/g,'').replace(/^0+/,''); if(!n) return null; const B=bcExtra(); for(const c in B) if(B[c].includes(n)) return c; return null; }

/* quelqu'un d'autre (autre onglet, autre personne) vient d'écrire : on le dit, sans rien écraser */
let _averti=false;
function avertitMaj(msg){
  if(_averti||!document.body) return;
  /* la fiche ouverte dans une fenêtre (mode cadre) et la page qui l'a ouverte écrivent dans les mêmes données :
     ce n'est pas « un autre onglet », et recharger la page effacerait la facture en cours de lecture */
  if(document.documentElement.classList.contains('cadre')||document.getElementById('fv-ov')) return;
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
  /* 17 oct. 2026 : une page qui sait se redessiner le fait quand elle est calme, sans bandeau (voir _serveur.py) */
  if(typeof window.__rafraichir==='function'&&typeof _syPlusTard==='function'){ window.__SY_A_MONTRER=true; _syPlusTard(); return; }
  avertitMaj('Un autre onglet vient de modifier les données.');
});

/* ============ LE STOCK DE PERFUME CITY (13 oct. 2026) ============
   Perfume City est une boutique à part (celle de Kim). Son stock était gardé dans le navigateur
   d'UN seul ordinateur (inventaire-local-pc-v1) : Kim et Sam ne voyaient pas le même. Il vit
   maintenant dans un magasin PARTAGÉ, pc-stock-v1 : une fiche par code-barres, fusionnée champ
   par champ (deux postes qui touchent deux parfums différents ne s'écrasent pas).
   Les pages continuent de parler en « lignes » (les 12 colonnes d'avant) : pcsRows() / pcsSauve(). */
const K_PCS='pc-stock-v1', K_PCL='inventaire-local-pc-v1';
const pcsCle=r=>{ const bc=r&&r[0]?String(r[0]).replace(/^0+/,''):''; return bc||String((r&&r[9])||''); };
const pcsDe=r=>({bc:String(r[0]||''),nom:r[1]||'',m:r[2]||'',ml:String(r[3]||''),ty:r[4]||'',q:Math.round(+r[5]||0),
                 pa:r[6]==null||r[6]===''?null:+r[6],pvr:r[10]==null||r[10]===''?null:+r[10],pvw:r[11]==null||r[11]===''?null:+r[11],
                 cle:r[9]||(r[0]?'b'+r[0]:'')});
const pcsVers=o=>{ const q=+o.q||0, pa=o.pa==null?null:+o.pa;
  return [o.bc||'',o.nom||'',o.m||'',o.ml||'',o.ty||'',q,pa,pa!=null?q*pa:null,'non',o.cle||(o.bc?'b'+o.bc:''),
          o.pvr==null?null:o.pvr,o.pvw==null?null:o.pvw]; };
/* lit le magasin ; l'ancien stock gardé dans ce navigateur y entre une fois (sans écraser ce qui y est déjà) */
function pcsCarte(){
  let m=lit(K_PCS,{}); if(!m||typeof m!=='object'||Array.isArray(m)) m={};
  let vieux=null; try{ vieux=JSON.parse(localStorage.getItem(K_PCL)||'null'); }catch(e){}
  if(Array.isArray(vieux)&&vieux.length){
    let n=0; vieux.forEach(r=>{ const k=pcsCle(r); if(k&&!m[k]){ m[k]=pcsDe(r); n++; } });
    if(n) ecrit(K_PCS,m);
    try{ localStorage.removeItem(K_PCL); }catch(e){}
  }
  return m;
}
/* les lignes de l'inventaire Perfume City, rangées par marque puis nom ; null tant qu'il est vide */
function pcsRows(){
  const m=pcsCarte(), L=Object.keys(m).map(k=>pcsVers(m[k]));
  if(!L.length) return null;
  L.sort((a,b)=>String(a[2]).localeCompare(String(b[2]))||String(a[1]).localeCompare(String(b[1]))||String(a[3]).localeCompare(String(b[3])));
  return L;
}
/* écrit les lignes données : seules celles qui ont changé partent au serveur ; remplace=true vide d'abord */
function pcsSauve(rows,remplace){
  try{
    const m=remplace?(lit(K_PCS,{}),{}):pcsCarte(); let n=0;
    (rows||[]).forEach(r=>{ const k=pcsCle(r); if(!k) return; const o=pcsDe(r);
      if(JSON.stringify(m[k])!==JSON.stringify(o)){ m[k]=o; n++; } });
    if(n||remplace) ecrit(K_PCS,m);
    return true;
  }catch(e){ return false; }
}
"""
