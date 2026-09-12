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
  if(t) t.textContent=nom;
}
const mnNav=()=>document.querySelector('.side nav');
const mnItems=()=>mnNav()?[...mnNav().querySelectorAll('a.nv')]:[];

function mnLit(){
  try{ const v=lit(K_MENU,null);
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
  if(c.ordre&&c.ordre.length){
    const par={}; items.forEach(a=>par[mnId(a)]=a);
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
    /* une rubrique ajoutée après coup n'est dans aucun ordre : elle va à la fin */
    items.forEach(a=>{ if(!vus.includes(mnId(a))) nav.appendChild(a); });
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

/* L'ordre enregistré peut être ancien (une simple liste d'identifiants) ou
   nouveau (des rubriques et des titres mêlés). On lit les deux. */
function mnOrdre(c){
  return (c.ordre||[]).map(e=> (typeof e==='string') ? {t:'nv',id:e} : e);
}

/* ---------- la fenêtre de réglage ---------- */
function mnOuvre(){
  let ov=document.getElementById('mnov');
  if(!ov){
    ov=document.createElement('div'); ov.className='ov'; ov.id='mnov';
    ov.innerHTML=`<div class="mod" style="max-width:520px;max-height:86vh;display:flex;flex-direction:column">
      <div class="mh"><h2>Mon menu</h2><button class="x" id="mn-x">&times;</button></div>
      <div class="mb" style="overflow:auto;flex:1;min-height:0">
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
    location.reload();
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
    location.reload();
  };
  ov.classList.add('on');
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
  const p=document.querySelector('.side .sfoot'); if(!p) return;
  if(document.getElementById('mn-btn')) return;
  const b=document.createElement('button');
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
  if(n){ el.textContent=String(n); el.classList.add('pt');
         el.title=n+(n>1?' messages non lus':' message non lu'); }
  else { el.textContent='équipe'; el.classList.remove('pt'); el.title=''; }
}
window.addEventListener('storage',e=>{ if(e.key==='messages-v1'||e.key==='sam-session-v1') mnPastilleMessages(); });

(function(){
  const go=()=>{ try{ mnApplique(); mnBouton(); mnPastilleMessages(); }catch(e){} };
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',go);
  else setTimeout(go,0);
})();
"""
