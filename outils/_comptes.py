# -*- coding: utf-8 -*-
"""Les comptes, les rôles, et la session ouverte.

Remplace la fenêtre « qui utilise SAM ? » qui demandait un prénom libre.
Maintenant : un compte, un mot de passe, un rôle. Le journal est signé par le
compte connecté, et ce que chacun voit à l'écran dépend de son rôle.

À dire honnêtement : tant qu'il n'y a pas de serveur, ce n'est pas une serrure,
c'est un badge. Les comptes vivent dans le navigateur du poste ; quelqu'un qui
sait ce qu'il fait peut les contourner. Ça répond à « qui a fait quoi » et à
« qui voit quoi à l'écran », pas à « comment j'empêche quelqu'un d'entrer ».
La vraie serrure, c'est le serveur.
"""

COMPTES = r"""
/* ============ COMPTES, RÔLES ET SESSION ============ */
const K_USERS='sam-comptes-v1';
const K_SESS ='sam-session-v1';
const K_NOM  ='crm-utilisateur-v1';     /* conservé : le journal l'utilise déjà */
const K_NOMS ='crm-utilisateurs-v1';
const K_ROLES='sam-roles-v1';           /* les rôles fabriqués par le patron */

const _cLit=(k,d)=>{ try{ const t=localStorage.getItem(k); return t==null?d:JSON.parse(t); }catch(e){ return d; } };
const _cEcr=(k,v)=>{ try{ localStorage.setItem(k,JSON.stringify(v)); }catch(e){} };

/* Les droits, une bonne fois. La rubrique Accès s'en sert pour dessiner
   les cases à cocher : ajouter un droit ici suffit à le voir apparaître là-bas. */
const DROITS=[
  ['voirPA',    "Voit les prix d'achat"],
  ['voirMarge', 'Voit les marges'],
  ['modPrix',   'Modifie les prix'],
  ['vendre',    'Saisit des ventes et des remboursements'],
  ['compter',   "Compte le stock et l'ajuste"],
  ['reglages',  'Change les réglages'],
  ['acces',     'Ouvre et ferme les accès'],
  ['annuler',   'Annule une facture enregistrée (le stock et les prix reviennent en arrière)'],
  ['prixPC',    'Change le prix de Perfume City sur Shopify'],
  ['technique', 'Branche les services extérieurs et leurs clés']];

/* Les quatre rôles d'origine. On ne les touche pas : ils servent de repère,
   et un compte qui pointe dessus doit continuer de marcher quoi qu'il arrive.
   « voirPA » est le plus sensible : le prix d'achat révèle la marge, et tout
   le monde n'a pas à la connaître. */
const ROLES_BASE={
  /* Admin est au-dessus de Patron, et d'un seul cran : la plomberie technique.
     Brancher un service extérieur, c'est manipuler des clés d'API qui donnent
     accès au site, à la caisse et à l'argent qui y transite. Sam dirige son
     entreprise ; il n'a pas à toucher à ça, et la première erreur à cet
     endroit-là ne se voit pas — elle se découvre.
     Admin peut aussi modifier le compte du Patron : sans ça, un patron qui perd
     son mot de passe n'a plus personne pour le lui rendre. */
  admin:     {lib:'Admin',             aide:'Tout, plus le branchement des services extérieurs et leurs clés',
              voirPA:1, voirMarge:1, modPrix:1, vendre:1, compter:1, reglages:1, acces:1, annuler:1, prixPC:1, technique:1},
  patron:    {lib:'Patron',            aide:'Tout sur son entreprise — sauf le branchement des services extérieurs',
              voirPA:1, voirMarge:1, modPrix:1, vendre:1, compter:1, reglages:1, acces:1, annuler:1, prixPC:1, technique:0},
  commercial:{lib:'Commercial',        aide:'Vend et voit les prix de vente — pas les prix d\'achat',
              voirPA:0, voirMarge:0, modPrix:0, vendre:1, compter:0, reglages:0, acces:0, annuler:0, prixPC:0},
  entrepot:  {lib:'Entrepôt',          aide:'Compte le stock et ajuste — ne voit aucun prix',
              voirPA:0, voirMarge:0, modPrix:0, vendre:0, compter:1, reglages:0, acces:0, annuler:0, prixPC:0},
  comptable: {lib:'Comptable',         aide:'Lit tout, y compris les prix d\'achat — ne modifie rien',
              voirPA:1, voirMarge:1, modPrix:0, vendre:0, compter:0, reglages:0, acces:0, annuler:0, prixPC:0}};

/* ROLES = les quatre d'origine + ceux que le patron a fabriqués. Toutes les
   pages lisent ROLES[...] sans savoir d'où vient le rôle : c'est le but. */
const ROLES=Object.assign({}, ROLES_BASE);
function rolesPerso(){ const P=_cLit(K_ROLES,{}); return (P&&typeof P==='object'&&!Array.isArray(P))?P:{}; }
/* Le droit « technique » n'est JAMAIS ajustable : c'est lui qui fait que le rôle
   Admin veut dire quelque chose. Le donner d'un clic à n'importe quel rôle rendrait
   la hiérarchie décorative — et elle se serait défaite sans que personne ne le voie. */
const DROITS_FIGES=['technique'];
function _rolesMonte(){
  Object.keys(ROLES).forEach(k=>{ if(!ROLES_BASE[k]) delete ROLES[k]; else ROLES[k]=Object.assign({},ROLES_BASE[k]); });
  const P=rolesPerso();
  for(const k in P){
    if(ROLES_BASE[k]){
      /* un rôle d'origine ajusté : la base, puis l'ajustement, puis les droits
         figés remis de force. « ajuste » sert à l'écran, pour qu'il puisse dire
         que ce n'est plus le rôle d'origine. */
      ROLES[k]=Object.assign({}, ROLES_BASE[k], P[k], {ajuste:1});
      DROITS_FIGES.forEach(d=>{ ROLES[k][d]=ROLES_BASE[k][d]; });
    } else {
      ROLES[k]=Object.assign({perso:1}, P[k]);
    }
  }
}
function sauveRoles(P){ _cEcr(K_ROLES,P); _rolesMonte(); }
function roleDOrigine(k){ return !!ROLES_BASE[k]; }
_rolesMonte();

function comptes(){ const L=_cLit(K_USERS,[]); return Array.isArray(L)?L:[]; }
function sauveComptes(L){ _cEcr(K_USERS,L); }
/* Le rôle est RELU dans la liste des comptes à chaque appel, jamais pris tel quel
   dans la session. Sans cela, la session garde une photo du rôle prise au moment
   de la connexion : un rôle changé ou un accès fermé n'aurait d'effet qu'à la
   prochaine connexion — or personne ne se déconnecte jamais. Quelqu'un qu'on
   vient de rétrograder continuerait de voir les prix d'achat et les marges.
   On ne touche pas au cas « compte introuvable » : la liste peut être vide une
   fraction de seconde au premier chargement, et déconnecter tout le monde
   pendant ce laps de temps serait pire que le mal. */
let _sBrut='', _sListe=null;
function session(){
  const s=_cLit(K_SESS,null);
  if(!s||!s.id) return null;
  let brut=''; try{ brut=localStorage.getItem(K_USERS)||''; }catch(e){}
  if(brut!==_sBrut){ _sBrut=brut; _sListe=comptes(); }
  const u=(_sListe||[]).find(x=>x.ident===s.id);
  if(!u) return s;
  if(u.actif===false) return null;
  return (u.role===s.role && u.nom===s.nom) ? s : Object.assign({},s,{role:u.role,nom:u.nom});
}
function role(){ const s=session(); return (s&&ROLES[s.role])?ROLES[s.role]:null; }
function peut(d){ const r=role(); return r?!!r[d]:false; }
/* Sur les pages dont le code tourne en module (Étude de devis, Factures…), ces fonctions n'étaient pas
   visibles du menu, qui s'appliquait AVANT : un Commercial y voyait toute la partie Pilotage
   (Connecteurs, Accès, Réglages…). On les rend visibles, puis on réapplique le menu (19 oct. 2026). */
try{ window.session=session; window.role=role; window.peut=peut;
  if(typeof mnApplique==='function') mnApplique(); }catch(e){}

/* empreinte du mot de passe : on ne garde jamais le mot de passe en clair,
   même si ce n'est pas une protection contre quelqu'un de déterminé */
async function empreinte(mdp,sel){
  const t=new TextEncoder().encode('sam:'+sel+':'+mdp);
  const h=await crypto.subtle.digest('SHA-256',t);
  return [...new Uint8Array(h)].map(b=>b.toString(16).padStart(2,'0')).join('');
}
const selNeuf=()=>[...crypto.getRandomValues(new Uint8Array(8))].map(b=>b.toString(16).padStart(2,'0')).join('');

async function creeCompte({nom,ident,mdp,role,par,email,provisoire}){
  const L=comptes();
  const id=String(ident||'').trim().toLowerCase();
  if(!id) throw new Error('Il faut un identifiant.');
  if(L.some(u=>u.ident===id)) throw new Error('Cet identifiant existe déjà.');
  const sel=selNeuf();
  L.push({ident:id, nom:String(nom||'').trim()||id, role:role||'commercial',
          sel, emp:await empreinte(mdp,sel), actif:true, email:String(email||'').trim(),
          /* un mot de passe pose par quelqu'un d'autre est provisoire : celui qui
             l'a choisi le connait. Le premier compte fait exception — c'est la
             personne elle-meme qui vient de le choisir. */
          doitChanger: provisoire===false ? false : true,
          cree:new Date().toISOString(), par:par||'', dernier:null});
  sauveComptes(L);
  return id;
}
async function verifie(ident,mdp){
  const id=String(ident||'').trim().toLowerCase();
  const u=comptes().find(x=>x.ident===id);
  if(!u) return null;
  if(!u.actif) return {bloque:true};
  const e=await empreinte(mdp,u.sel);
  return e===u.emp ? u : null;
}
function ouvreSession(u){
  _cEcr(K_SESS,{id:u.ident,nom:u.nom,role:u.role,depuis:new Date().toISOString()});
  try{ localStorage.setItem(K_NOM,u.nom); }catch(e){}
  const L=comptes(); const t=L.find(x=>x.ident===u.ident);
  if(t){ t.dernier=new Date().toISOString(); sauveComptes(L); }
  let N=_cLit(K_NOMS,[]); if(!Array.isArray(N)) N=[];
  if(!N.includes(u.nom)){ N.unshift(u.nom); _cEcr(K_NOMS,N.slice(0,12)); }
}
/* Quitter la session SANS quitter la page. « Ce n'est pas moi — changer de compte »,
   sur l'accueil, doit rendre le badge local ET le jeton du serveur : avant, seul le
   badge partait, et le navigateur gardait un jeton valide au nom de la personne
   précédente jusqu'à la connexion suivante — pour toujours si on refermait l'onglet
   là. Quelqu'un d'autre pouvait donc repartir avec les droits du patron. */
let quitteSession=function(){ try{ localStorage.removeItem(K_SESS); }catch(e){} };
function fermeSession(){
  quitteSession();
  location.href='accueil.html'+versUrl();
}

/* Où arrive chacun en entrant : sur ce qu'il a à faire, pas sur le catalogue.
   Le tableau de bord parle d'argent (marges, marchandise à perte) : on n'y envoie
   que ceux qui ont le droit de voir les marges. */
const ACCUEIL_ROLE={patron:'tableau.html', comptable:'tableau.html',
                    commercial:'ventes.html', entrepot:'stock.html'};
const DEPARTS=[['tableau.html','Tableau de bord'],['ventes.html','Ventes'],
               ['stock.html','Inventaire'],['catalogue.html','Catalogue'],
               ['factures.html','Factures'],['clients.html','Clients']];
/* Le ?v=… collé au bout : le navigateur garde longtemps en mémoire une page
   ouverte depuis un fichier local, et sert alors une version d'avant. Une
   adresse qui change à chaque livraison le force à relire. */
/* try : appelée avant la ligne qui pose VER_URL (session absente au chargement), le
   « typeof » ne protège pas d'une const pas encore posée — l'erreur bloquait le renvoi. */
const versUrl=()=>{ try{ return VER_URL ? ('?v='+VER_URL) : ''; }catch(e){ return ''; } };
/* pageDeDepart rend le NOM de la page — c'est une identité, comparable.
   urlDepart rend l'adresse où aller, avec le ?v=… qui force la relecture. */
function pageDeDepart(r){
  const d=(ROLES[r]||{}).depart;
  if(d && DEPARTS.some(x=>x[0]===d)) return d;
  return ACCUEIL_ROLE[r]||'catalogue.html';
}
function urlDepart(r){ return pageDeDepart(r)+versUrl(); }

/* Toute page de SAM commence par vérifier qu'une session est ouverte.
   Sinon on renvoie à l'accueil — sans effacer quoi que ce soit. */
function exigeSession(){
  if(session()) return true;
  if(!comptes().length) { location.href='accueil.html'+versUrl(); return false; }
  location.href='accueil.html'+versUrl();
  return false;
}

/* Remettre un mot de passe : en local on refait l'empreinte, en ligne on le dit au cockpit. */
/* Un TIERS repose le mot de passe de quelqu'un : il redevient provisoire, puisque
   celui qui l'a choisi le connait. */
async function remetMotDePasse(ident,mdp){
  const L=comptes(); const u=L.find(x=>x.ident===ident); if(!u) throw new Error('Compte inconnu.');
  u.sel=selNeuf(); u.emp=await empreinte(mdp,u.sel); u.doitChanger=true; sauveComptes(L);
}
/* La personne choisit ELLE-MEME le sien : l'ancien est exigé, et la marque tombe.
   Deux fonctions séparées, pas un drapeau : elles n'ont ni les mêmes droits, ni
   les mêmes vérifications, et les confondre finirait par laisser quelqu'un
   changer le mot de passe d'un autre sans le connaître. */
async function changeMonMotDePasse(ident,ancien,nouveau){
  const u=comptes().find(x=>x.ident===ident); if(!u) throw new Error('Compte inconnu.');
  if(await empreinte(ancien,u.sel)!==u.emp) throw new Error('Ancien mot de passe incorrect.');
  if(String(nouveau)===String(ancien)) throw new Error("Choisis un mot de passe différent de celui qu'on t'a donné.");
  const L=comptes(); const t=L.find(x=>x.ident===ident);
  t.sel=selNeuf(); t.emp=await empreinte(nouveau,t.sel); t.doitChanger=false; sauveComptes(L);
}

/* ============ EN LIGNE : LE COCKPIT DÉCIDE ============
   Sur le serveur, les comptes ne vivent plus dans le navigateur : c'est le cockpit
   (le socle d'Igal) qui les tient, les mêmes pour tout le monde, sur tous les
   appareils. Les fonctions ci-dessus gardent leur nom : les pages ne changent pas.
   En local (localhost, fichier), rien de tout ceci ne s'active. */
const CK_URL=(typeof COCKPIT_URL!=='undefined'&&COCKPIT_URL)||'https://cockpit.igalbotbol.com';
const CK_ORG=(typeof COCKPIT_ORG!=='undefined'&&COCKPIT_ORG)||'dasy';
const EN_LIGNE=location.protocol!=='file:' && !/^(localhost|127\.0\.0\.1|\[::1\])$/.test(location.hostname);
const K_TOK='ck-token';
const ckTok=()=>{ try{ return localStorage.getItem(K_TOK)||''; }catch(e){ return ''; } };
function ckPerdu(){
  /* session refusée par le serveur : on efface le badge local et on retourne à l'entrée */
  try{ localStorage.removeItem(K_TOK); localStorage.removeItem(K_SESS); }catch(e){}
  if(!/accueil\.html$/.test(location.pathname)) location.replace('accueil.html'+versUrl());
}
async function ck(m,u,b){
  let r;
  try{
    r=await fetch(CK_URL+'/api/o/'+CK_ORG+u,{method:m,
      headers:Object.assign({'Content-Type':'application/json'}, ckTok()?{Authorization:'Bearer '+ckTok()}:{}),
      body:b==null?undefined:JSON.stringify(b)});
  }catch(e){ throw new Error('Le serveur ne répond pas. Vérifie la connexion et réessaie.'); }
  const j=await r.json().catch(()=>({}));
  if(r.status===401 && !/\/login$|\/premier$/.test(u)){ ckPerdu(); throw new Error(j.erreur||'Session expirée.'); }
  if(!r.ok){ const e=new Error(j.erreur||('Erreur '+r.status)); e.status=r.status; throw e; }
  return j;
}
function ckMiroirRoles(R){
  const P={}; for(const k in R||{}) if(!ROLES_BASE[k] || (R[k]&&R[k].ajuste)) P[k]=R[k];
  _cEcr(K_ROLES,P); _rolesMonte();
}
/* Rafraîchit les comptes et les rôles depuis le cockpit, puis prévient les pages. */
async function pretComptes(){
  if(!EN_LIGNE||!ckTok()) return false;
  const [L,R]=await Promise.all([ck('GET','/comptes'),ck('GET','/roles')]);
  _cEcr(K_USERS,L); ckMiroirRoles(R);
  try{ window.dispatchEvent(new Event('comptes-maj')); }catch(e){}
  return true;
}
if(EN_LIGNE){
  sauveComptes=function(L){
    /* les pages modifient la liste puis l'enregistrent : on envoie au cockpit ce qui a changé */
    const avant=comptes();
    for(const u of L){
      const a=avant.find(x=>x.ident===u.ident); if(!a) continue;
      const d={};
      if(!!a.actif!==!!u.actif) d.actif=u.actif?1:0;
      if(a.role!==u.role) d.role=u.role;
      if(a.nom!==u.nom) d.nom=u.nom;
      if((a.email||'')!==(u.email||'')) d.email=u.email||'';
      if(!!a.doitChanger!==!!u.doitChanger) d.doitChanger=!!u.doitChanger;
      if(Object.keys(d).length) ck('PATCH','/comptes/'+encodeURIComponent(u.ident),d).then(pretComptes).catch(e=>alert(e.message));
    }
    _cEcr(K_USERS,L);
  };
  creeCompte=async function({nom,ident,mdp,role,email,provisoire}){
    const id=String(ident||'').trim().toLowerCase();
    const mail=String(email||'').trim();
    if(!ckTok()) await ck('POST','/premier',{nom,ident:id,mdp,email:mail});   /* tout premier compte : le patron */
    else await ck('POST','/comptes',{nom,ident:id,mdp,role:role||'commercial',email:mail,
                                     provisoire: provisoire===false?false:true});
    try{ await pretComptes(); }catch(e){}
    return id;
  };
  remetMotDePasse=async function(ident,mdp){ await ck('PATCH','/comptes/'+encodeURIComponent(ident),{mdp}); };
  changeMonMotDePasse=async function(ident,ancien,nouveau){
    await ck('POST','/moi/mdp',{ancien,nouveau});
    try{ await pretComptes(); }catch(e){}
  };
  verifie=async function(ident,mdp){
    try{
      const j=await ck('POST','/login',{ident,mdp});
      try{ localStorage.setItem(K_TOK,j.token); }catch(e){}
      ckMiroirRoles(j.roles);
      return j.compte;
    }catch(e){
      if(e.status===403) return {bloque:true};
      if(e.status===401) return null;
      throw e;
    }
  };
  quitteSession=function(){
    const t=ckTok();
    try{ localStorage.removeItem(K_SESS); localStorage.removeItem(K_TOK); }catch(e){}
    if(t) fetch(CK_URL+'/api/o/'+CK_ORG+'/logout',{method:'POST',headers:{Authorization:'Bearer '+t},keepalive:true}).catch(()=>{});
  };
  fermeSession=function(){ quitteSession(); location.href='accueil.html'+versUrl(); };
  sauveRoles=function(P){ _cEcr(K_ROLES,P); _rolesMonte();
    ck('PUT','/roles',P).then(R=>{ ckMiroirRoles(R); try{ window.dispatchEvent(new Event('comptes-maj')); }catch(e){} }).catch(e=>alert(e.message)); };
  /* à chaque page : le badge local ne suffit pas, le cockpit confirme — ou renvoie à l'entrée */
  if(session()){
    if(!ckTok()) ckPerdu();
    else pretComptes().catch(()=>{});
  }
}
"""

OEIL = r"""
/* ============ L'ŒIL SUR LES MOTS DE PASSE ============
   Tout champ « mot de passe », où qu'il apparaisse (entrée, premier démarrage, création
   d'un accès, remise d'un mot de passe), reçoit un petit œil pour afficher ce qu'on tape. */
function poseOeil(inp){
  if(!inp||inp.dataset.oeil||inp.type!=='password') return;
  inp.dataset.oeil='1';
  const w=document.createElement('span'); w.className='pw-wrap';
  w.style.cssText='position:relative;display:block';
  inp.parentNode.insertBefore(w,inp); w.appendChild(inp);
  inp.style.paddingRight='40px';
  const b=document.createElement('button'); b.type='button'; b.className='pw-oeil'; b.tabIndex=-1;
  b.setAttribute('aria-label','Afficher le mot de passe'); b.title='Afficher / masquer';
  b.style.cssText='position:absolute;right:8px;top:50%;transform:translateY(-50%);width:28px;height:28px;border:0;background:none;cursor:pointer;color:#6b6b78;padding:0;display:flex;align-items:center;justify-content:center;border-radius:6px';
  const on='<svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M1 12s4-7 11-7 11 7 11 7-4 7-11 7S1 12 1 12z"/><circle cx="12" cy="12" r="3"/></svg>';
  const off='<svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17.94 17.94A10.07 10.07 0 0112 20c-7 0-11-8-11-8a18.45 18.45 0 015.06-5.94M9.9 4.24A9.12 9.12 0 0112 4c7 0 11 8 11 8a18.5 18.5 0 01-2.16 3.19m-6.72-1.07a3 3 0 11-4.24-4.24"/><line x1="1" y1="1" x2="23" y2="23"/></svg>';
  b.innerHTML=on;
  b.onmousedown=e=>e.preventDefault();
  b.onclick=()=>{ const v=inp.type==='password'; inp.type=v?'text':'password'; b.innerHTML=v?off:on; b.style.color=v?'#4f56d8':'#6b6b78'; inp.focus(); };
  w.appendChild(b);
}
function poseOeils(r){ (r||document).querySelectorAll('input[type=password]').forEach(poseOeil); }
document.addEventListener('DOMContentLoaded',()=>{
  poseOeils();
  try{ new MutationObserver(m=>{ for(const x of m){ for(const n of x.addedNodes){ if(n.nodeType===1){ if(n.matches&&n.matches('input[type=password]')) poseOeil(n); else poseOeils(n); } } } })
    .observe(document.body,{childList:true,subtree:true}); }catch(e){}
});
"""
from _serveur import sync_js
import _aide
# _aide vient APRÈS sync_js : il se sert de CK_URL, CK_ORG et ckTok, définis là.
COMPTES = COMPTES + OEIL + sync_js() + _aide.JS
