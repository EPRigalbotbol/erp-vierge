# -*- coding: utf-8 -*-
"""Le menu de gauche, réglable par l'utilisateur.

Renommer une rubrique et la monter ou la descendre. Le réglage est partagé par
toutes les pages et suit les mêmes règles d'écriture que le reste (voir _fusion),
donc deux onglets ouverts ne s'effacent pas l'un l'autre.

Une rubrique garde toujours son identité interne (le fichier vers lequel elle
pointe). Renommer « Inventaire » en « Mon stock » ne change que ce qui est écrit
à l'écran : les liens, le journal et les contrôles continuent de fonctionner.
"""

MENU = r"""
/* ============ LE MENU DE GAUCHE, RÉGLABLE ============ */
const K_MENU='menu-perso-v1';

/* Identité d'une rubrique : le fichier vers lequel elle mène.
   Pour celles qui n'existent pas encore (« bientôt »), son libellé d'origine. */
function mnId(a){
  if(a.dataset&&a.dataset.id) return a.dataset.id;   /* « Support technique » n'a pas de page */
  const h=a.getAttribute('href');
  /* le ?v=… qui force le navigateur à relire la page ne fait pas partie de
     l'identité de la rubrique : sinon le menu réglé serait perdu à chaque
     nouvelle version */
  if(h) return h.replace(/^.*\//,'').replace(/[?#].*$/,'');
  return 'soon:'+mnNomOrigine(a);
}
function mnNomOrigine(a){
  if(a.dataset.nom0!=null) return a.dataset.nom0;
  const t=[...a.childNodes].find(n=>n.nodeType===3&&n.textContent.trim());
  const v=t?t.textContent.trim():'';
  a.dataset.nom0=v;
  return v;
}
function mnEcritNom(a,nom){
  const t=[...a.childNodes].find(n=>n.nodeType===3&&n.textContent.trim());
  if(!t||t.textContent===nom) return;
  t.textContent=nom;
  /* un nom choisi par l'utilisateur est son français d'origine : la traduction
     ne doit pas le ramener au libellé d'usine */
  if(nom!==a.dataset.nom0) t.__fr=nom;
}
const mnNav=()=>document.querySelector('.side nav');
const mnItems=()=>mnNav()?[...mnNav().querySelectorAll('a.nv')]:[];

function mnLit(){
  try{ /* ce bloc tourne AVANT le code de la page (et donc avant lit) : on lit le stockage tel quel */
    const v=(typeof lit==='function')?lit(K_MENU,null):JSON.parse(localStorage.getItem(K_MENU)||'null');
    return (v&&typeof v==='object')
      ?{ordre:v.ordre||[],noms:v.noms||{},caches:v.caches||[]}
      :{ordre:[],noms:{},caches:[]}; }
  catch(e){ return {ordre:[],noms:{},caches:[]}; }
}
function mnSauve(c){ try{ ecrit(K_MENU,c); }catch(e){} }

/* Applique le réglage : d'abord les noms, puis l'ordre.
   Dès qu'un ordre existe, les titres de groupe (Produits / Commerce / Pilotage)
   disparaissent : ils ne voudraient plus rien dire une fois les rubriques
   déplacées librement. */
function mnApplique(){
  const nav=mnNav(); if(!nav) return;
  const c=mnLit(), items=mnItems();
  /* Avant de toucher à l'ordre : chaque rubrique retient sa section d'origine
     (Produits / Commerce / Pilotage). La fenêtre de réglage s'en sert pour
     retrouver les titres d'un menu réglé avant qu'ils ne soient modifiables. */
  if(!nav.dataset.sec0){ let cur=''; [...nav.children].forEach(el=>{
      if(el.classList.contains('navlab')&&!el.dataset.perso) cur=el.textContent.trim();
      else if(el.classList.contains('nv')) el.dataset.sec0=cur; });
    nav.dataset.sec0='1'; }
  items.forEach(a=>{
    mnNomOrigine(a);
    const id=mnId(a);
    const n=c.noms[id];
    mnEcritNom(a, (n&&String(n).trim())?String(n).trim():a.dataset.nom0);
    /* Retirée du menu : elle n'est plus affichée. La page existe toujours et
       reste accessible par son adresse — on cache, on ne casse pas. */
    a.style.display = (c.caches||[]).includes(id) ? 'none' : '';
  });
  /* une sous-rubrique suit sa rubrique-mère : si « Clients » est retirée du menu, « Clients VIP » aussi */
  items.forEach(a=>{ if(!a.dataset.sous) return;
    const m=items.find(x=>mnId(x)===a.dataset.sous);
    if(m&&m.style.display==='none') a.style.display='none'; });
  mnSous();
  mnPilotage();
  /* la page ouverte porte le nom que l'utilisateur a donné à sa rubrique : dans
     l'onglet du navigateur et dans le grand titre, pas seulement dans le menu */
  try{ const ici=(location.pathname.split('/').pop()||'').replace(/[?#].*$/,'');
    const nom=c.noms[ici]&&String(c.noms[ici]).trim();
    if(nom){ document.title=nom+' — Perfumes Trade'; document.__titreFr=document.title;
      const h=document.querySelector('.wrap h1, main h1, h1');
      if(h){ const t=[...h.childNodes].find(n=>n.nodeType===3&&n.textContent.trim());
        if(t&&t.textContent.trim()!==nom){ t.textContent=nom; t.__fr=nom; } } } }catch(e){}
  if(c.ordre&&c.ordre.length){
    const par={}; items.forEach(a=>par[mnId(a)]=a);
    /* 3 nov. 2026 (« je ne vois pas la partie Tâches ») : avant de réordonner, chaque rubrique retient celle qui la
       précède dans le menu d'origine — une rubrique nouvelle ira se placer juste après elle, pas tout en bas */
    items.forEach((a,i)=>{ a.dataset.apres=i>0?mnId(items[i-1]):''; });
    /* les titres d'origine s'effacent : ce sont ceux de l'utilisateur qui comptent */
    nav.querySelectorAll('.navlab').forEach(l=>{ if(!l.dataset.perso) l.style.display='none'; });
    nav.querySelectorAll('.navlab[data-perso]').forEach(l=>l.remove());
    const vus=[];
    mnOrdre(c).forEach(e=>{
      if(e.t==='h'){
        const d=document.createElement('span');
        d.className='navlab'; d.dataset.perso='1'; d.textContent=e.x||'';
        nav.appendChild(d);
      } else if(par[e.id]){ nav.appendChild(par[e.id]); vus.push(e.id); }
    });
    /* une rubrique ajoutée après coup n'est dans aucun ordre : elle se place juste après celle qui la précède dans le
       menu d'origine (« Tâches » sous « Tableau de bord », quel que soit l'ordre réglé) ; une sous-rubrique
       (« Clients VIP ») reste sous sa rubrique-mère ; sinon, à la fin */
    items.forEach(a=>{ if(vus.includes(mnId(a))) return;
      const mere=a.dataset.sous&&items.find(m=>mnId(m)===a.dataset.sous);
      const avant=!mere&&a.dataset.apres&&nav.contains(par[a.dataset.apres]||null)?par[a.dataset.apres]:null;
      if(mere) mere.insertAdjacentElement('afterend',a); else if(avant) avant.insertAdjacentElement('afterend',a); else nav.appendChild(a); });
    /* Un titre dont toutes les rubriques ont été retirées ne sert plus à rien :
       on le cache. Mais un titre volontairement seul, sans aucune rubrique
       derrière lui, est un choix de l'utilisateur — on le laisse. */
    [...nav.querySelectorAll('.navlab[data-perso]')].forEach(l=>{
      let n=l.nextElementSibling, total=0, vus=0;
      while(n&&!n.classList.contains('navlab')){
        if(n.classList.contains('nv')){ total++; if(n.style.display!=='none') vus++; }
        n=n.nextElementSibling;
      }
      l.style.display = (total>0 && vus===0) ? 'none' : '';
    });
  }
}

/* « Clients VIP » est allumée (et « Clients » éteinte) quand la liste des favoris est ouverte :
   adresse en #vip, ou filtre « Favoris (VIP) » choisi dans la page. */
/* 17 oct. 2026 (Sam) : la partie « Pilotage » du menu (Connecteurs, Journal, Tableau de bord, Accès, Paie, Réglages — « Support technique » reste pour tous)
   n'existe pas pour un rôle qui n'a ni les marges, ni l'accès aux comptes, ni les réglages : un Commercial, un Entrepôt.
   Le titre « Pilotage » part avec. On ne fait que RETIRER : un rôle autorisé garde son menu tel que réglé. */
/* 19 oct. 2026 (guide de Clemencia) : une page qui n'affiche à ce rôle qu'un mur « Cette page n'est pas pour ce rôle »
   (les pages de prix d'achat, voir _identite.py) ne reste pas dans son menu — il n'y a rien à y faire. */
const MN_MURS={'etude.html':'voirPA','fournisseurs.html':'voirPA','factures.html':'voirPA'};
function mnPilotage(){
  try{
    if(typeof peut!=='function'||typeof role!=='function'||!role()) return;
    const nav=mnNav(); if(!nav) return;
    nav.querySelectorAll('a.nv').forEach(a=>{ const h=(a.getAttribute('href')||'').replace(/[?#].*$/,'').split('/').pop();
      if(MN_MURS[h]&&!peut(MN_MURS[h])) a.style.display='none'; });
    /* 9 nov. 2026 (Igal) : « Analytique » n'existe que pour les administrateurs de l'ERP — rôles Admin et Patron, aucun autre
       (pas même le Comptable). La classe mn-pasadmin est posée dès l'entête d'après la session (build_crm.py) et confirmée ici. */
    { const s=(typeof session==='function')?session():null; const adm=!!s&&/^(admin|patron)$/.test(String(s.role||''));
      document.documentElement.classList.toggle('mn-pasadmin',!adm);
      nav.querySelectorAll('a.nv').forEach(a=>{ const h=(a.getAttribute('href')||'').replace(/[?#].*$/,'').split('/').pop();
        if(h==='analytique.html'&&!adm) a.style.display='none'; }); }
    const large=!!(peut('voirMarge')||peut('acces')||peut('reglages'));
    /* 7 nov. 2026 (Igal) : le rôle réel tranche — la classe mn-cial (posée dès l'entête d'après la session, pour qu'un Commercial
       n'aperçoive jamais Pilotage ni Léa, même une seconde) est confirmée ou retirée ici */
    document.documentElement.classList.toggle('mn-cial',!large);
    if(large) return;
    nav.querySelectorAll('[data-pilotage]').forEach(e=>{ e.style.display='none'; });
    const gl=nav.querySelector('#gl-btn'); if(gl) gl.style.display='none';   /* « Parler à Léa » : pas pour le Commercial (Igal, 7 nov. 2026) */
  }catch(e){}
}
function mnSous(){
  try{
    const nav=mnNav(); if(!nav) return;
    const ici=(location.pathname.split('/').pop()||'').replace(/[?#].*$/,'');
    nav.querySelectorAll('a.nv[data-sous]').forEach(a=>{
      const mere=[...nav.querySelectorAll('a.nv')].find(x=>mnId(x)===a.dataset.sous);
      const vip = ici===a.dataset.sous && (window.__filtreVip===true || (window.__filtreVip===undefined && /(^|[#&])vip\b/.test(location.hash)));
      a.classList.toggle('on',!!vip);
      if(mere&&ici===a.dataset.sous) mere.classList.toggle('on',!vip);
    });
  }catch(e){}
}
window.addEventListener('hashchange',()=>mnSous());
window.addEventListener('comptes-maj',()=>mnPilotage());

/* L'ordre enregistré peut être ancien (une simple liste d'identifiants) ou
   nouveau (des rubriques et des titres mêlés). On lit les deux. */
function mnOrdre(c){
  return (c.ordre||[]).map(e=> (typeof e==='string') ? {t:'nv',id:e} : e);
}

/* ---------- la fenêtre de réglage ---------- */
function mnOuvre(){
  try{ if(typeof peut==='function' && typeof session==='function' && session() && !peut('reglages')) return; }catch(e){}
  let ov=document.getElementById('mnov');
  if(!ov){
    ov=document.createElement('div'); ov.className='ov'; ov.id='mnov';
    ov.innerHTML=`<div class="mod" style="max-width:520px;max-height:86vh;display:flex;flex-direction:column">
      <div class="mh"><h2>Le menu de l'équipe</h2><button class="x" id="mn-x">&times;</button></div>
      <div class="mb" style="overflow:auto;flex:1;min-height:0">
        <p class="hint"><b>Ce menu est le même pour tout le monde.</b> Ce que tu changes ici, toute l'équipe le voit.</p>
        <p class="hint">Renomme une rubrique comme tu veux, déplace-la avec les flèches,
        ou décoche-la pour la retirer du menu. Le lien ne change pas : seul le mot affiché change,
        et une rubrique retirée n'est pas supprimée — elle disparaît du menu, c'est tout.</p>
        <button class="btn" id="mn-titre" style="width:100%;justify-content:center;margin:0 0 10px">
          + Ajouter un titre de section</button>
        <p class="hint" style="margin:0 0 12px">Le titre se pose en haut de la liste : donne-lui un nom,
        descends-le à sa place avec la flèche &darr;, et il coiffe toutes les rubriques
        qui le suivent jusqu'au titre suivant.</p>
        <div id="mn-liste" style="display:flex;flex-direction:column;gap:6px"></div>
      </div>
      <div class="mf" style="flex:none"><span class="msg" id="mn-msg"></span>
        <button class="btn" id="mn-raz">Tout remettre comme avant</button>
        <button class="btn" id="mn-non">Annuler</button>
        <button class="btn pri" id="mn-ok">Enregistrer</button></div>
    </div>`;
    document.body.appendChild(ov);
    document.getElementById('mn-x').onclick=()=>ov.classList.remove('on');
    document.getElementById('mn-non').onclick=()=>ov.classList.remove('on');
    ov.addEventListener('click',e=>{ if(e.target===ov) ov.classList.remove('on'); });
  }
  const items=mnItems(), c=mnLit();
  const fiche=a=>({t:'nv', id:mnId(a), nom0:a.dataset.nom0,
                   nom:(c.noms[mnId(a)]||a.dataset.nom0),
                   vu:!(c.caches||[]).includes(mnId(a))});
  let L;
  const ord=mnOrdre(c);
  if(ord.length){
    const par={}; items.forEach(a=>par[mnId(a)]=a);
    /* Un menu réglé avant que les titres existent n'en a aucun : on les
       retrouve depuis la page d'origine (chaque rubrique se souvient de sa
       section) et on les repose devant la première rubrique de chaque section,
       dans l'ordre choisi. Sinon Sam ne pourrait plus jamais les renommer. */
    const sansTitre=!ord.some(e=>e.t==='h');
    const section={}; if(sansTitre) items.forEach(a=>{ section[mnId(a)]=a.dataset.sec0||''; });
    L=[]; const vus=[]; let derSec=null;
    ord.forEach(e=>{
      if(e.t==='h') L.push({t:'h', x:e.x||''});
      else if(par[e.id]){
        if(sansTitre){ const sec=section[e.id]; if(sec&&sec!==derSec){ L.push({t:'h', x:sec}); derSec=sec; } }
        L.push(fiche(par[e.id])); vus.push(e.id); }
    });
    /* les rubriques absentes de l'ordre enregistré (ajoutées depuis) : à la
       fin, mais regroupées sous leur section d'origine plutôt qu'en vrac */
    let derFin=null;
    items.filter(a=>!vus.includes(mnId(a))).forEach(a=>{
      const sec=a.dataset.sec0||'';
      if(sec && sec!==derFin && !L.some(x=>x.t==='h'&&x.x===sec&&L.indexOf(x)===L.length-1)){ L.push({t:'h', x:sec}); }
      derFin=sec; L.push(fiche(a)); });
  } else {
    /* premier passage : on reprend les titres déjà écrits dans la page */
    L=[]; const nav=mnNav();
    if(nav) [...nav.children].forEach(el=>{
      if(el.classList.contains('navlab')) L.push({t:'h', x:el.textContent.trim()});
      else if(el.classList.contains('nv')) L.push(fiche(el));
    });
    if(!L.length) L=items.map(fiche);
  }
  const fl=(i)=>`<button class="btn" data-h="${i}" ${i===0?'disabled':''} style="padding:8px 11px"
      title="Monter">&uarr;</button>
    <button class="btn" data-b="${i}" ${i===L.length-1?'disabled':''} style="padding:8px 11px"
      title="Descendre">&darr;</button>`;
  const peint=()=>{
    document.getElementById('mn-liste').innerHTML=L.map((x,i)=> x.t==='h' ? `
      <div style="display:flex;gap:6px;align-items:center;margin-top:6px">
        <span style="width:26px;text-align:center;font-size:11px;color:var(--ink-3)">≡</span>
        <input type="text" data-x="${i}" value="${String(x.x||'').replace(/"/g,'&quot;')}"
               placeholder="Titre de section (ex : Boutique)"
               style="flex:1;font-family:inherit;font-size:11px;font-weight:700;letter-spacing:.1em;
               text-transform:uppercase;color:var(--ink-2);background:var(--surface-2);
               border:1px dashed var(--line);border-radius:3px;padding:8px 10px">
        <button class="btn" data-sup="${i}" style="padding:8px 11px" title="Enlever ce titre">&times;</button>
        ${fl(i)}
      </div>` : `
      <div style="display:flex;gap:6px;align-items:center;${x.vu?'':'opacity:.5'}">
        <label title="Décoche pour retirer cette rubrique du menu"
          style="display:flex;align-items:center;padding:0 3px;cursor:pointer">
          <input type="checkbox" data-v="${i}" ${x.vu?'checked':''}></label>
        <input type="text" data-i="${i}" value="${String(x.nom).replace(/"/g,'&quot;')}"
               style="flex:1;font-family:inherit;font-size:13.5px;color:var(--ink);
               background:var(--surface-2);border:1px solid var(--line);border-radius:3px;padding:8px 10px">
        ${fl(i)}
      </div>`).join('');
  };
  peint();
  const liste=document.getElementById('mn-liste');
  liste.oninput=e=>{
    const i=e.target.dataset.i; if(i!=null){ L[+i].nom=e.target.value; return; }
    const x=e.target.dataset.x; if(x!=null){ L[+x].x=e.target.value; return; }
    const v=e.target.dataset.v; if(v!=null){ L[+v].vu=e.target.checked; peint(); }
  };
  liste.onclick=e=>{
    const s=e.target.closest('[data-sup]');
    if(s){ L.splice(+s.dataset.sup,1); peint(); return; }
    const b=e.target.closest('[data-h],[data-b]'); if(!b) return;
    const bouge=(i,j)=>{ [L[i],L[j]]=[L[j],L[i]]; peint(); };
    if(b.dataset.h!=null){ const i=+b.dataset.h; if(i>0) bouge(i,i-1); }
    else { const i=+b.dataset.b; if(i<L.length-1) bouge(i,i+1); }
  };
  document.getElementById('mn-titre').onclick=()=>{
    L.unshift({t:'h', x:''}); peint();
    const c0=document.querySelector('#mn-liste input[data-x]');
    if(c0){ c0.scrollIntoView({block:'nearest'}); c0.focus(); }
  };
  document.getElementById('mn-raz').onclick=()=>{
    mnSauve({ordre:[],noms:{},caches:[]});
    if(typeof jlogMenu==='function') jlogMenu('menu remis par défaut');
    mnApresEnvoi(()=>location.reload());
  };
  document.getElementById('mn-ok').onclick=()=>{
    const noms={};
    L.filter(x=>x.t!=='h').forEach(x=>{ const v=String(x.nom||'').trim();
      if(v && v!==x.nom0) noms[x.id]=v.slice(0,28); });
    /* un titre laissé vide n'est pas enregistré */
    const ordre=L.filter(x=>x.t!=='h'||String(x.x||'').trim())
                 .map(x=> x.t==='h' ? {t:'h', x:String(x.x).trim().slice(0,28)} : {t:'nv', id:x.id});
    mnSauve({ordre, noms, caches:L.filter(x=>x.t!=='h'&&!x.vu).map(x=>x.id)});
    if(typeof jlogMenu==='function') jlogMenu('menu réorganisé');
    /* Igal, 27 sept. 2026 : « je n'arrive pas à changer le nom de la rubrique, elle
       reste à Étude de cote ». On rechargeait la page juste après avoir enregistré :
       le menu partait vers le serveur au même moment, le navigateur demandait
       « quitter la page ? », et au rechargement c'était l'ancien menu du serveur qui
       revenait — sans le nouveau nom. Plus de rechargement : le menu se refait sur
       place, tout de suite, et part au serveur tranquillement. */
    ov.classList.remove('on');
    try{ mnApplique(); }catch(e){ mnApresEnvoi(()=>location.reload()); }
  };
  ov.classList.add('on');
}

/* attend que ce qui vient d'être écrit soit parti au serveur (6 s au plus) */
function mnApresEnvoi(fn){
  const t0=Date.now();
  const tour=()=>{ const att=(typeof _SY_ATT!=='undefined'&&_SY_ATT.size)||(typeof _SY_ENVOI!=='undefined'&&_SY_ENVOI.size);
    if(!att||Date.now()-t0>6000) fn(); else setTimeout(tour,120); };
  setTimeout(tour,150);
}
/* trace au journal, comme toute modification du système */
function jlogMenu(lib){
  try{
    const J=lit('crm-journal-v1',[]);
    J.push({t:new Date().toISOString(), u:(typeof NOM_UTIL!=='undefined'?NOM_UTIL:''),
            act:'reglage', lib, ref:'menu', av:null, ap:null});
    ecrit('crm-journal-v1',J);
  }catch(e){}
}

/* le bouton, au bas de la barre de gauche */
function mnBouton(){
  const p=(document.getElementById('sfline')||document.querySelector('.side .sfoot')); if(!p) return;
  if(document.getElementById('mn-btn')) return;
  /* le menu est commun à toute l'équipe : seuls ceux qui ont les Réglages le modifient.
     Ce bloc peut tourner avant le code des comptes : on regarde maintenant, et encore
     une fois quand la page a démarré. */
  const refuse=()=>{ try{ return typeof peut==='function' && typeof session==='function' && !!session() && !peut('reglages'); }catch(e){ return false; } };
  if(refuse()) return;
  const b=document.createElement('button');
  setTimeout(()=>{ if(refuse()) b.remove(); },0); setTimeout(()=>{ if(refuse()) b.remove(); },1500);
  b.id='mn-btn'; b.className='lnk'; b.textContent='Modifier le menu';
  b.style.cssText='display:block;margin-top:7px';
  b.onclick=mnOuvre;
  p.appendChild(b);
}

/* La pastille des messages non lus, à côté de la rubrique Messages, sur
   toutes les pages. Elle lit la même boîte que la rubrique elle-même et se
   met à jour quand un autre onglet écrit dedans. */
function mnPastilleMessages(){
  const el=document.getElementById('ct-messages'); if(!el) return;
  let n=0;
  try{
    const s=(typeof session==='function')?session():null;
    const L=JSON.parse(localStorage.getItem('messages-v1')||'[]');
    if(s&&Array.isArray(L)) n=L.filter(m=>m.a===s.id && !m.lu).length;
  }catch(e){}
  /* 29 sept. (Igal) : une pastille ROUGE quand des messages attendent — et le nombre dans le
     titre de l'onglet du navigateur, pour le voir même quand l'ERP est derrière une autre fenêtre */
  if(n){ el.textContent=String(n); el.classList.add('pt'); el.style.background='#E5484D'; el.style.color='#fff';
         el.title=n+(n>1?' messages non lus':' message non lu'); }
  else { el.textContent=''; el.classList.remove('pt'); el.style.background=''; el.style.color=''; el.title=''; }
  try{ const t=document.title.replace(/^\(\d+\) /,''); const nt=n?'('+n+') '+t:t; if(document.title!==nt) document.title=nt; }catch(e){}
}
window.addEventListener('storage',e=>{ if(e.key==='messages-v1'||e.key==='sam-session-v1') mnPastilleMessages(); });
window.addEventListener('ck-maj',e=>{ try{ if((e.detail&&e.detail.cles||[]).includes('messages-v1')) mnPastilleMessages(); }catch(_){} });

/* La pastille des NOUVELLES VENTES, sur la rubrique Ventes. Igal, 12 sept. 2026 :
   « à chaque fois qu'une nouvelle vente arrive — Amazon, Shopify, le site, peu
   importe — une notification dans Ventes, jusqu'au moment où on ouvre la page ».
   Une vente « nouvelle » : une vente du site ou de la caisse enregistrée toute
   seule (facture avec `auto`) depuis la dernière fois que CETTE personne a ouvert
   Ventes sur cet appareil, ou une vente qui attend encore dans la file. */
const K_VVU='ventes-vues-v1';
function mnVentesNouvelles(){
  let sid=''; try{ const s=JSON.parse(localStorage.getItem('sam-session-v1')||'null'); sid=s&&s.id||''; }catch(e){}
  if(!sid) return 0;
  let vu=''; try{ vu=(JSON.parse(localStorage.getItem(K_VVU)||'{}')||{})[sid]||''; }catch(e){}
  let n=0;
  try{ const F=JSON.parse(localStorage.getItem('factures-v1')||'[]'); if(Array.isArray(F)) n+=F.filter(f=>f&&f.auto&&f.sens==='vente'&&!f.retour&&(f.t||'')>vu).length; }catch(e){}
  try{ const Q=JSON.parse(localStorage.getItem('caisse-file-v1')||'[]'); if(Array.isArray(Q)) n+=Q.filter(v=>v&&!v.annule).length; }catch(e){}
  return n;
}
function mnVentesVues(){
  try{ const s=JSON.parse(localStorage.getItem('sam-session-v1')||'null'); if(!s||!s.id) return;
    const V=JSON.parse(localStorage.getItem(K_VVU)||'{}')||{}; V[s.id]=new Date().toISOString(); localStorage.setItem(K_VVU,JSON.stringify(V)); }catch(e){}
}
function mnPastilleVentes(){
  const el=document.getElementById('ct-ventes'); if(!el) return;
  const ici=/ventes\.html$/.test(location.pathname);
  if(ici){ mnVentesVues(); }
  const n=ici?0:mnVentesNouvelles();
  if(n){ el.textContent=n+(n>1?' nouvelles':' nouvelle'); el.classList.add('pt'); el.title=n+(n>1?' nouvelles ventes arrivées depuis ta dernière visite':' nouvelle vente arrivée depuis ta dernière visite'); }
  else { el.textContent=''; el.classList.remove('pt'); el.title=''; }
}
window.addEventListener('storage',e=>{ if(e.key==='factures-v1'||e.key==='caisse-file-v1'||e.key===K_VVU) mnPastilleVentes(); });

/* La pastille des commandes À EXPÉDIER, sur la rubrique Expéditions : tant qu'une
   commande du site ou d'Amazon n'a pas été marquée « expédiée », elle compte. */
function mnPastilleExpeditions(){
  const el=document.getElementById('ct-expeditions'); if(!el) return;
  let n=0;
  try{ const E=JSON.parse(localStorage.getItem('expeditions-v1')||'[]'); if(Array.isArray(E)) n=E.filter(e=>e&&e.statut==='attente').length; }catch(e){}
  if(n){ el.textContent=n+' à expédier'; el.classList.add('pt'); el.title=n+(n>1?' commandes attendent d\'être expédiées':' commande attend d\'être expédiée'); }
  else { el.textContent=''; el.classList.remove('pt'); el.title=''; }
}
window.addEventListener('storage',e=>{ if(e.key==='expeditions-v1') mnPastilleExpeditions(); });
/* 4 nov. 2026 : les demandes de parfums entre Perfume City et Perfumes Trade qui attendent (demandées ou envoyées, pas encore reçues) */
function mnPastilleDemandes(){
  const el=document.getElementById('ct-demandes'); if(!el) return;
  let n=0;
  try{ const D=JSON.parse(localStorage.getItem('demandes-pc-v1')||'{}')||{}; n=Object.values(D).filter(r=>r&&(r.etat==='demandee'||r.etat==='envoyee')).length; }catch(e){}
  if(n){ el.textContent=n+' en cours'; el.classList.add('pt'); el.title=n+(n>1?' demandes de parfums en cours':' demande de parfums en cours'); }
  else { el.textContent=''; el.classList.remove('pt'); el.title=''; }
}
window.addEventListener('storage',e=>{ if(e.key==='demandes-pc-v1') mnPastilleDemandes(); });
/* dans le même onglet : dès que la page écrit des ventes (enregistrement automatique, file) */
(function(){ let ok=false; const brancher=()=>{ if(ok) return; if(typeof _apresEcrit!=='undefined'&&Array.isArray(_apresEcrit)){ ok=true; _apresEcrit.push(cle=>{ if(cle==='factures-v1'||cle==='caisse-file-v1') setTimeout(mnPastilleVentes,0); if(cle==='expeditions-v1') setTimeout(mnPastilleExpeditions,0); if(cle==='demandes-pc-v1') setTimeout(mnPastilleDemandes,0); }); } };
  setInterval(()=>{ brancher(); mnPastilleVentes(); mnPastilleExpeditions(); mnPastilleDemandes(); },30000); setTimeout(mnPastilleDemandes,2500); setTimeout(brancher,1500); setTimeout(brancher,6000); })();

/* Les chiffres de Catalogue et d'Inventaire, dans le menu, sur toutes les pages.
   Igal, 1er oct. 2026 : ils étaient écrits une fois pour toutes à la fabrication, depuis le
   fichier de septembre (3 830 fiches, 1 892 en stock) — ni les 12 parfums créés depuis le
   Sheet de Sam, ni le démarrage du 1er octobre, ni les comptages n'y apparaissaient.
   Maintenant :
   - Catalogue  = toutes les fiches (le fichier + les parfums créés dans l'ERP) ;
   - Inventaire = les parfums EN STOCK pas encore vérifiés (choix d'Igal) : il descend à
     chaque comptage et tombe à 0 quand Sam a tout recompté. Les parfums à zéro ne comptent
     pas : sinon le chiffre ne descendrait jamais sous ~1 950, personne ne recompte des
     flacons qu'il n'a pas.
   Le stock et l'état « vérifiée » se lisent comme la page Inventaire les lit : la fiche
   corrigée (fiches-modifiees-v1), puis le Sheet importé (stock-externe-v1), puis le fichier. */
function mnLignesBase(){
  if(Array.isArray(window.D_INV)) return window.D_INV.map(r=>({bc:r[0],qte:r[5],v:r[8],cle:r[9]}));
  if(Array.isArray(window.D_PROD)) return window.D_PROD.map(r=>({bc:r[0],qte:r[6],v:r[14],cle:r[15]}));
  return null;
}
function mnCompteProduits(){
  const B=mnLignesBase(); if(!B) return null;
  const J=k=>{ try{ return JSON.parse(localStorage.getItem(k)||'null'); }catch(e){ return null; } };
  let M=J('fiches-modifiees-v1'); if(!M||typeof M!=='object'||Array.isArray(M)) M={};
  let X=J('stock-externe-v1'); const XQ=(X&&X.q&&typeof X.q==='object')?X.q:{};
  let A=J('articles-ajoutes-v1'); if(!Array.isArray(A)) A=[];
  const L=B.slice(); const deja=new Set(B.map(p=>p.cle));
  A.forEach(o=>{ if(o&&o.id&&!deja.has(o.id)){ deja.add(o.id); L.push({bc:String(o.bc||''),qte:+o.qte||0,v:'non',cle:o.id}); } });
  const q=p=>{ const m=M[p.cle]; if(m&&m.qte!=null) return +m.qte; const e=XQ[p.bc]; if(e!=null) return +e; return +p.qte||0; };
  const v=p=>{ const m=M[p.cle]; return (m&&m.verif!==undefined)?m.verif:p.v; };
  return {total:L.length, aVerifier:L.filter(p=>q(p)>0&&v(p)!=='ok').length};
}
function mnCompteurs(){
  const ec=document.getElementById('ct-catalogue'), ei=document.getElementById('ct-inventaire');
  if(!ec&&!ei) return;
  if(ei) ei.title='Parfums en stock pas encore vérifiés';
  const c=mnCompteProduits();
  if(!c){
    /* une page qui n'a pas la liste des produits la charge, une fois, en arrière-plan */
    if(!mnCompteurs.charge){ mnCompteurs.charge=true;
      const a=document.querySelector('a.nv[href*="stock.html"]'); const m=a&&/[?&]v=([^&]+)/.exec(a.getAttribute('href')||'');
      const s=document.createElement('script'); s.src='donnees/inventaire.js'+(m?'?v='+m[1]:''); s.async=true;
      s.onload=()=>{ try{ mnCompteurs(); }catch(e){} }; (document.head||document.documentElement).appendChild(s); }
    return;
  }
  const nf=n=>n.toLocaleString('fr-FR');
  if(ec&&ec.textContent!==nf(c.total)) ec.textContent=nf(c.total);
  /* la page Inventaire compte elle-même, sur la liste qu'elle affiche */
  if(ei&&!window.__CT_INV_PAGE&&ei.textContent!==nf(c.aVerifier)) ei.textContent=nf(c.aVerifier);
}
window.mnCompteurs=mnCompteurs;
(function(){
  const K=['fiches-modifiees-v1','stock-externe-v1','articles-ajoutes-v1'];
  const t=()=>{ clearTimeout(t.h); t.h=setTimeout(()=>{ try{ mnCompteurs(); }catch(e){} },120); };
  window.addEventListener('storage',e=>{ if(K.includes(e.key)) t(); });
  window.addEventListener('ck-maj',e=>{ try{ if((e.detail&&e.detail.cles||[]).some(k=>K.includes(k))) t(); }catch(_){} });
  let ok=false; const brancher=()=>{ if(ok) return; if(typeof _apresEcrit!=='undefined'&&Array.isArray(_apresEcrit)){ ok=true; _apresEcrit.push(cle=>{ if(K.includes(cle)) t(); }); } };
  setTimeout(brancher,1500); setTimeout(brancher,6000);
  const go=()=>{ brancher(); t(); };
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',go); else setTimeout(go,0);
})();

/* ================= LES TABLEAUX TIENNENT DANS LEUR CADRE =================
   Igal, 24 sept. 2026 : « fais attention que ça ne déborde pas de partout ».
   Un tableau marqué `af` (sur la boîte qui le contient) retire ses colonnes
   secondaires une par une — celles marquées o1, puis o2… jusqu'à o5 — tant
   qu'il dépasse sa boîte. Il ne défile de côté qu'en tout dernier recours.
   La largeur est surveillée en continu : la traduction, les photos et les
   polices changent la largeur APRÈS le premier dessin. */
(function(){
  try{
    const st=document.createElement('style');
    st.textContent='.af.x1 .o1,.af.x2 .o2,.af.x3 .o3,.af.x4 .o4,.af.x5 .o5{display:none!important}.af{overflow-x:auto}';
    (document.head||document.documentElement).appendChild(st);
  }catch(e){}
  const ajuste=(w)=>{ if(!w||w.__afEn) return; const t=w.querySelector('table'); if(!t||!w.clientWidth) return;
    w.__afEn=true;
    try{ const trop=()=>t.scrollWidth>w.clientWidth+1;
      w.classList.remove('x1','x2','x3','x4','x5');
      for(let i=1;i<=5&&trop();i++) w.classList.add('x'+i);
    } finally { setTimeout(()=>{ w.__afEn=false; },0); } };
  let RO=null; try{ RO=new ResizeObserver(es=>es.forEach(e=>{ const w=e.target.closest?e.target.closest('.af'):null; if(w) ajuste(w); })); }catch(e){}
  const suit=()=>{ document.querySelectorAll('.af').forEach(w=>{ const t=w.querySelector('table');
      if(RO&&w.__afObs!==t){ w.__afObs=t; try{ RO.observe(w); if(t) RO.observe(t); }catch(e){} }
      ajuste(w); }); };
  window.afAjuste=suit;
  const go=()=>{ suit(); try{ new MutationObserver(()=>{ clearTimeout(go.t); go.t=setTimeout(suit,60); }).observe(document.body,{childList:true,subtree:true}); }catch(e){} };
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',go); else setTimeout(go,0);
  window.addEventListener('resize',()=>{ clearTimeout(go.r); go.r=setTimeout(suit,80); });
})();

/* ================= LA STRATÉGIE, VUE DE N'IMPORTE QUELLE PAGE =================
   Igal, 9 nov. 2026 : « qu'ils puissent aller sur une autre page, mais qu'en même temps la stratégie tourne ».
   Elle tourne déjà sur le cockpit (le serveur), pas dans la page. Ce qui manquait : le savoir ailleurs.
   Sur le lien « Analytique » du menu (Admin et Patron seulement) : un point bleu qui bat pendant l'analyse,
   un point vert quand une stratégie ou un rapport neuf n'a pas encore été regardé ; et, sur la page où l'on
   se trouve, un petit message en bas à droite quand elle est prête, avec un lien pour aller la lire. */
function mnStrategie(){
  const a=document.querySelector('.side nav a.nv[href^="analytique.html"]'); if(!a) return;
  const T=(fr,en,es)=>typeof L3==='function'?L3(fr,en,es):fr;
  let S=null; try{ S=JSON.parse(localStorage.getItem('strategie-v1')||'null'); }catch(e){}
  const E=S&&S.encours, C=S&&S.courante, R=S&&Array.isArray(S.rapports)?S.rapports[0]:null;
  const enCours=!!(E&&!E.err&&E.depuis&&Date.now()-Date.parse(E.maj||E.depuis)<30*60e3);
  /* 11 nov. 2026 (Igal : « le petit point bleu qui clignotait n'est plus là ») : il bat aussi tout le temps qu'une stratégie
     est ACTIVE (30 jours après « Activer la stratégie ») — l'ERP est branché dessus et constate les actions faites */
  const active=!!(C&&C.active&&C.active.fin&&Date.now()<Date.parse(C.active.fin));
  /* le dernier résultat : la stratégie ou le rapport le plus récent */
  const der=[C&&{id:C.id,d:C.date,r:0},R&&{id:R.id,d:R.date,r:1}].filter(Boolean).sort((x,y)=>String(y.d).localeCompare(String(x.d)))[0]||null;
  const ici=/analytique\.html/.test(location.pathname);
  let vu=''; try{ vu=localStorage.getItem('strategie-vue')||''; }catch(e){}
  if(der&&ici){ try{ localStorage.setItem('strategie-vue',der.id); }catch(e){} vu=der.id; }
  if(der&&!vu){ try{ localStorage.setItem('strategie-vue',der.id); }catch(e){} vu=der.id; }   /* première visite : l'ancienne n'est pas « neuve » */
  const neuve=!!(der&&der.id!==vu&&!enCours);
  const bat=enCours||(active&&!neuve);
  let p=a.querySelector('.mn-st'); if(!p){ p=document.createElement('i'); p.className='mn-st'; p.setAttribute('aria-hidden','true'); a.appendChild(p); }
  p.className='mn-st'+(bat?' cours':neuve?' neuve':'');
  a.title=(!enCours&&bat)?T('La stratégie est active : l\'ERP suit les actions et les résultats','The strategy is active: the ERP follows the actions and results','La estrategia está activa: el ERP sigue las acciones y los resultados')
    :enCours?T('La stratégie est en préparation — elle continue même si vous changez de page','The strategy is being prepared — it keeps going even if you change page','La estrategia se está preparando — sigue aunque cambie de página')
    :neuve?T('Nouvelle stratégie à lire','New strategy to read','Nueva estrategia para leer'):'';
  /* le petit message, une seule fois par résultat, et seulement si on l'a vu tourner depuis cette page */
  if(enCours) window.__mnStCours=E.id;
  if(!enCours&&window.__mnStCours&&der&&neuve&&!ici){
    window.__mnStCours=null;
    let an=''; try{ an=localStorage.getItem('strategie-annonce')||''; }catch(e){}
    if(an!==der.id){ try{ localStorage.setItem('strategie-annonce',der.id); }catch(e){}
      const b=document.createElement('div'); b.className='mn-st-toast'; b.setAttribute('role','status');
      b.innerHTML=`<b>${der.r?T('Le rapport du mois est prêt','The monthly report is ready','El informe del mes está listo'):T('La nouvelle stratégie est prête','The new strategy is ready','La nueva estrategia está lista')}</b><a href="analytique.html">${T('La lire','Read it','Leerla')}</a><button type="button" aria-label="${T('Fermer','Close','Cerrar')}">×</button>`;
      b.querySelector('button').onclick=()=>b.remove(); document.body.appendChild(b); setTimeout(()=>{ try{ b.remove(); }catch(e){} },30000); }
  }
  if(!enCours&&E&&E.err) window.__mnStCours=null;
}
window.mnStrategie=mnStrategie;
(function(){
  try{ const st=document.createElement('style');
    st.textContent='.side nav a.nv .mn-st{display:none;width:8px;height:8px;border-radius:50%;margin-left:auto;flex:none}'
      +'.side nav a.nv .mn-st.cours{display:inline-block;background:#1a73e8;animation:mnStBat 1.2s ease-in-out infinite}'
      +'.side nav a.nv .mn-st.neuve{display:inline-block;background:#188038}'
      +'@keyframes mnStBat{0%,100%{box-shadow:0 0 0 0 rgba(26,115,232,.55)}50%{box-shadow:0 0 0 6px rgba(26,115,232,0)}}'
      +'@media (prefers-reduced-motion:reduce){.side nav a.nv .mn-st.cours{animation:none}}'
      +'.mn-st-toast{position:fixed;right:18px;bottom:18px;z-index:9000;display:flex;align-items:center;gap:14px;background:#1f1f1f;color:#fff;padding:12px 14px 12px 16px;border-radius:12px;box-shadow:0 10px 30px rgba(0,0,0,.25);font-size:14px;max-width:calc(100vw - 36px)}'
      +'.mn-st-toast a{color:#8ab4f8;font-weight:700;text-decoration:none}.mn-st-toast button{background:none;border:0;color:#bbb;font-size:20px;line-height:1;cursor:pointer;padding:0 2px}';
    (document.head||document.documentElement).appendChild(st); }catch(e){}
  const t=()=>{ try{ mnStrategie(); }catch(e){} };
  window.addEventListener('storage',e=>{ if(e.key==='strategie-v1') t(); });
  window.addEventListener('ck-maj',e=>{ try{ if((e.detail&&e.detail.cles||[]).includes('strategie-v1')) t(); }catch(_){} });
  setInterval(t,30000);   /* le point bleu s'éteint seul après une demi-heure sans nouvelle étape, même sans nouvelle donnée */
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',t); else setTimeout(t,0);
})();

(function(){
  /* Tout de suite, avant la première peinture : le menu réglé (ordre, noms,
     rubriques cachées) s'applique pendant que la page se construit. Sinon on
     voyait le menu d'usine, puis les rubriques sauter à leur place réglée
     (Igal, 12 sept. 2026 : « les rubriques bougent, ça monte, ça descend »). */
  if(document.body){ try{ mnApplique(); mnBouton(); mnPastilleMessages(); mnPastilleVentes(); mnPastilleExpeditions(); }catch(e){} }
  try{ document.documentElement.classList.remove('mn-attente'); }catch(e){}
  /* et une fois les données du serveur arrivées (un autre appareil a pu régler
     le menu entre-temps), on réapplique : sans changement, rien ne bouge */
  const go=()=>{ try{ mnApplique(); mnBouton(); mnPastilleMessages(); mnPastilleVentes(); mnPastilleExpeditions(); }catch(e){} };
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',go);
  else setTimeout(go,0);
})();
"""
