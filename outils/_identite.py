# -*- coding: utf-8 -*-
"""Qui utilise SAM — désormais un compte, plus un prénom tapé à la volée.

Avant : une fenêtre demandait un prénom libre, que n'importe qui pouvait changer.
Maintenant : on entre par la page d'accueil avec un identifiant et un mot de passe.
Chaque page vérifie qu'une session est ouverte, sinon elle renvoie à l'accueil.

Le journal est signé par le nom du compte connecté, et ce que chacun voit dépend
de son rôle (voir _comptes.py). Ce n'est toujours pas une serrure tant qu'il n'y a
pas de serveur — c'est un badge, et c'est déjà ce qui manquait.
"""

IDENT = r"""
/* ============ SESSION OUVERTE ============ */
let NOM_UTIL='';
(function(){
  const s=session();
  if(!s){
    /* pas de session : on renvoie à l'accueil sans rien effacer */
    document.documentElement.style.visibility='hidden';
    location.replace('accueil.html');
    return;
  }
  NOM_UTIL=s.nom||'';
  try{ localStorage.setItem('crm-utilisateur-v1',NOM_UTIL); }catch(e){}
})();

window.__nomChange=window.__nomChange||[];
/* compatibilité : ces deux fonctions étaient appelées partout dans les pages */
function signe(action,apres){
  if(NOM_UTIL) return NOM_UTIL;
  location.href='accueil.html';
  return '';
}
function fenetreNom(){ location.href='acces.html'; }

/* pied de la barre latérale : qui est connecté, son rôle, et la sortie.

   « Se déconnecter » était un lien discret, de la taille du texte autour. Sur un
   ordinateur partagé c'est le bouton le plus important de la page : celui qui
   empêche la personne suivante de travailler sous le nom de la précédente. Il est
   donc dessiné comme un bouton, et il se voit. */
const CSS_SORTIR = `
.sfu{margin-bottom:9px}
.sfu b{font-size:12px;color:var(--ink);letter-spacing:-.01em}
#sortir{display:block;width:100%;margin-top:7px;padding:6px 10px;border:1px solid var(--line);
 border-radius:7px;background:var(--surface);color:var(--ink-2);font-family:Inter,sans-serif;
 font-size:11.5px;font-weight:600;cursor:pointer;text-align:center;letter-spacing:.01em}
#sortir:hover{border-color:var(--crit);color:var(--crit);background:var(--crit-soft)}
@media(max-width:900px){ #sortir{display:inline-block;width:auto;margin-top:0} }
`;
(function(){ try{ const st=document.createElement('style'); st.textContent=CSS_SORTIR;
  document.head.appendChild(st); }catch(e){} })();

function piedSession(){
  const el=document.getElementById('sfu'); if(!el) return;
  const s=session(); if(!s) return;
  const r=ROLES[s.role]||{lib:s.role};
  el.innerHTML='<b>'+String(s.nom).replace(/[&<>"]/g,'')+'</b>'
    +'<span style="display:block;color:var(--ink-3)">'+r.lib+'</span>'
    +'<button type="button" id="sortir">Se déconnecter</button>';
}
/* Le clic est posé UNE fois, sur le document, et pas sur le bouton : plusieurs
   pages réécrivent le pied de la barre après coup (Inventaire recalculait ses
   chiffres et recopiait le bloc en innerHTML). Un écouteur posé sur le bouton
   disparaissait avec lui, et « Se déconnecter » restait affiché mais mort. */
document.addEventListener('click',e=>{
  const b=e.target&&e.target.closest&&e.target.closest('#sortir'); if(!b) return;
  e.preventDefault();
  const s=session(); if(!s) return;
  try{ const J=lit('crm-journal-v1',[]);
    J.push({t:new Date().toISOString(),u:s.nom,act:'acces',lib:'déconnexion',ref:s.id,av:null,ap:null});
    ecrit('crm-journal-v1',J); }catch(e2){}
  fermeSession();
});
/* et si une page vide quand même le bloc, on le redessine */
function veillePied(){
  const p=document.querySelector('.side .sfoot'); if(!p||p.__pieduVu) return;
  p.__pieduVu=true;
  try{ new MutationObserver(()=>{ const u=document.getElementById('sfu');
    if(!u||!u.querySelector('#sortir')) piedSession(); }).observe(p,{childList:true,subtree:true}); }catch(e){}
}
function montePied(){ piedSession(); veillePied(); }
if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',montePied);
else setTimeout(montePied,0);

/* ============ CHANGER DE COMPTE, EN HAUT À DROITE ============
   Pendant une démonstration, on veut montrer qu'un message part d'une boîte et
   arrive dans une autre. Retourner à l'accueil et retaper un mot de passe entre
   chaque envoi rend la démonstration illisible : on passe son temps à se
   reconnecter au lieu de montrer l'outil.

   Hors démonstration, ce raccourci N'EXISTE PAS, et c'est délibéré. Un sélecteur
   de compte sans mot de passe sur l'ordinateur du comptoir permettrait à
   n'importe qui de devenir le patron et de voir les prix d'achat et les marges —
   tout le système de rôles ne servirait plus à rien. Hors démonstration, le
   bouton renvoie donc à l'écran de connexion, qui demande le mot de passe.

   Le sélecteur affiche aussi le nombre de messages non lus de chaque compte :
   c'est exactement ce qu'on cherche à vérifier quand on teste que les messages
   circulent. */
const _K_DEMO='sam-comptes-demo-v1', _K_MSG='messages-v1';
const _estDemo=()=>{ try{ return localStorage.getItem(_K_DEMO)==='1'; }catch(e){ return false; } };
const _ini=n=>String(n||'?').trim().split(/\s+/).slice(0,2).map(m=>m[0]||'').join('').toUpperCase()||'?';
function _nonLus(ident){
  try{ const L=lit(_K_MSG,[]); if(!Array.isArray(L)) return 0;
    return L.filter(m=>m && m.a===ident && !m.lu).length; }catch(e){ return 0; }
}

const CSS_QUI = `
.bqui{position:relative;font-family:Inter,sans-serif}
.bqui .qs{list-style:none;cursor:pointer;display:flex;align-items:center;gap:9px;
border:1px solid var(--line);background:var(--surface);border-radius:99px;padding:5px 13px 5px 5px}
.bqui .qs::-webkit-details-marker{display:none}
.bqui .qs:hover{border-color:var(--iris)}
.bqui[open] .qs{border-color:var(--iris)}
.bqui .pa{flex:none;width:30px;height:30px;border-radius:50%;background:var(--iris-soft);
color:var(--iris);display:flex;align-items:center;justify-content:center;font-size:11.5px;font-weight:800}
.bqui .nn{display:flex;flex-direction:column;line-height:1.25;text-align:left}
.bqui .nn b{font-size:13px;font-weight:700;color:var(--ink)}
.bqui .nn i{font-style:normal;font-size:10.5px;color:var(--ink-3)}
.bqui .dm{margin-left:4px;padding:1px 7px;border-radius:99px;background:var(--warn-soft);
color:var(--warn);font-size:9.5px;font-weight:800;letter-spacing:.05em;text-transform:uppercase}
.bqui .qmenu{position:absolute;top:calc(100% + 6px);right:0;z-index:60;min-width:264px;
background:var(--surface);border:1px solid var(--line);border-radius:11px;padding:6px;
box-shadow:0 16px 38px rgba(0,0,0,.17)}
.bqui .qlab{padding:8px 11px 6px;font-size:10px;letter-spacing:.1em;text-transform:uppercase;
color:var(--ink-3);font-weight:800}
.bqui .qmenu button,.bqui .qmenu a{display:flex;width:100%;align-items:center;gap:10px;
border:0;background:none;border-radius:8px;padding:8px 11px;font:inherit;font-size:13px;
color:var(--ink);cursor:pointer;text-decoration:none;text-align:left}
.bqui .qmenu button:hover,.bqui .qmenu a:hover{background:var(--surface-2)}
.bqui .qmenu .pt{margin-left:auto;flex:none;min-width:20px;height:20px;border-radius:99px;
background:var(--crit);color:#fff;font-size:11px;font-weight:800;display:flex;
align-items:center;justify-content:center;padding:0 6px}
.bqui .qmenu .pt.z{display:none}
.bqui .qnote{padding:8px 11px 9px;border-top:1px solid var(--line-2);margin-top:4px;
font-size:11.5px;color:var(--ink-3);line-height:1.5}
@media(max-width:700px){ .bqui .qmenu{right:auto;left:0} }
`;

function barreCompte(){
  const h=document.querySelector('header'); if(!h) return;
  const s=session(); if(!s) return;
  if(document.getElementById('bqui')) return;
  if(!document.getElementById('css-qui')){
    const st=document.createElement('style'); st.id='css-qui'; st.textContent=CSS_QUI;
    document.head.appendChild(st);
  }
  const demo=_estDemo();
  const r=ROLES[s.role]||{lib:s.role};
  const d=document.createElement('details'); d.className='bqui'; d.id='bqui';
  const autres=(typeof comptes==='function'?comptes():[]).filter(u=>u.ident!==s.id && u.actif!==false);
  const moiNL=_nonLus(s.id);

  d.innerHTML=`<summary class="qs">
      <span class="pa">${_ini(s.nom)}</span>
      <span class="nn"><b>${String(s.nom).replace(/[&<>"]/g,'')}</b><i>${String(r.lib||'').replace(/[&<>"]/g,'')}</i></span>
      ${demo?'<span class="dm">démo</span>':''}
      ${moiNL?`<span class="pt">${moiNL}</span>`:''}
    </summary>
    <div class="qmenu">
      <div class="qlab">${demo?"Passer sur un autre compte":'Comptes ouverts'}</div>
      ${autres.length?autres.map(u=>{ const n=_nonLus(u.ident), rl=ROLES[u.role]||{lib:u.role};
        return `<${demo?`button data-q="${String(u.ident).replace(/[&<>"]/g,'')}"`:'a href="accueil.html"'}>
          <span class="pa">${_ini(u.nom)}</span>
          <span class="nn"><b>${String(u.nom).replace(/[&<>"]/g,'')}</b><i>${String(rl.lib||'').replace(/[&<>"]/g,'')}</i></span>
          <span class="pt ${n?'':'z'}">${n}</span></${demo?'button':'a'}>`; }).join('')
       :'<div class="qnote">Il n\'y a que toi pour l\'instant. Ouvre un accès dans <b>Accès</b>.</div>'}
      <div class="qnote">${demo
        ? "Démonstration en cours : un clic suffit pour changer de compte. Le chiffre rouge est le nombre de messages non lus — c'est lui qui montre qu'un message est bien arrivé.<br><b>Ce raccourci disparaît</b> dès que les comptes d'essai sont fermés dans Accès."
        : "Changer de compte demande le mot de passe : sans ça, n'importe qui au comptoir deviendrait le patron et verrait les prix d'achat."}</div>
      <a href="accueil.html" id="qsortir">Se déconnecter</a>
    </div>`;

  const z=document.createElement('div'); z.style.cssText='display:flex;align-items:center;gap:12px';
  const src=document.getElementById('src');
  h.appendChild(z); z.appendChild(d);
  if(src && src.parentNode===h){ h.insertBefore(z, src); }

  d.querySelectorAll('[data-q]').forEach(b=>b.onclick=async()=>{
    const id=b.dataset.q;
    try{
      const u=await verifie(id, id+'123');       /* mot de passe des comptes d'essai */
      if(!u){ location.href='accueil.html'; return; }
      try{ const J=lit('crm-journal-v1',[]);
        J.push({t:new Date().toISOString(),u:u.nom,act:'acces',
                lib:'changement de compte (démonstration)',ref:u.ident,av:s.nom,ap:u.nom});
        ecrit('crm-journal-v1',J); }catch(e){}
      ouvreSession(u);
      location.reload();
    }catch(e){ location.href='accueil.html'; }
  });
  document.getElementById('qsortir').onclick=e=>{
    e.preventDefault();
    try{ const J=lit('crm-journal-v1',[]);
      J.push({t:new Date().toISOString(),u:s.nom,act:'acces',lib:'déconnexion',ref:s.id,av:null,ap:null});
      ecrit('crm-journal-v1',J); }catch(e){}
    fermeSession();
  };
  document.addEventListener('click',e=>{ if(d.open && !d.contains(e.target)) d.open=false; });
}
if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',()=>setTimeout(barreCompte,60));
else setTimeout(barreCompte,60);


/* Ce que le rôle cache à l'écran. Le prix d'achat est le plus sensible :
   il révèle la marge, et tout le monde n'a pas à la connaître. */
(function appliqueRole(){
  const pose=()=>{
    if(!document.body) return;
    const r=role(); if(!r) return;
    document.body.classList.toggle('sansPA', !r.voirPA);
    if(!r.voirPA) document.body.classList.add('client');   /* réutilise le mode qui masque déjà les prix d'achat */
  };
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',pose);
  else setTimeout(pose,0);
})();
"""
