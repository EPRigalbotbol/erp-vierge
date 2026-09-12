# -*- coding: utf-8 -*-
"""La page d'accueil de SAM : on s'identifie avant d'entrer.

Grande image plein écran à gauche, le formulaire à droite.
Si un fichier « accueil.jpg » est posé à côté des pages, il devient l'image ;
sinon un fond sombre travaillé prend sa place — la page ne dépend d'aucun
fichier extérieur pour être présentable.
"""
import base64, os
from _comptes import COMPTES
from _serveur import enligne
from _fusion import FUSION
from _langue import LANGUE

LOGO = base64.b64encode(open('logos/site.png', 'rb').read()).decode()
FOND = base64.b64encode(open('accueil_web.jpg', 'rb').read()).decode()

TPL = r'''<!DOCTYPE html>
<html lang="fr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta http-equiv="Cache-Control" content="no-store, no-cache, must-revalidate">
<meta http-equiv="Pragma" content="no-cache">
<meta http-equiv="Expires" content="0">

<title>Perfumes Trade — ERP</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;500&family=Inter:wght@400;500;600;700&display=swap">
<style>
:root{
  --nuit:#120A18; --violet:#3A1D4E; --magenta:#7E2A72; --indigo:#2C2F7C;
  --lavande:#C9AEDC; --bronze:#C89A5C; --bronze-clair:#E0BB86;
  --creme:#FAF7F3; --blanc:#FFFFFF;
  --ink:#17171D; --ink-2:#4A4A56; --ink-3:#8B857A;
  --line:#E4DFD7; --crit:#A4262C; --good:#2F6B4F;
}
*{box-sizing:border-box}
html,body{height:100%}
body{margin:0;color:var(--ink);background:var(--nuit);
 font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;
 font-size:15px;-webkit-font-smoothing:antialiased}

/* ---------- la photo, plein écran ---------- */
.fond{position:fixed;inset:0;z-index:0;
 background-image:url('accueil.jpg'),url('data:image/jpeg;base64,__FOND__');
 background-size:cover;background-position:center bottom;background-repeat:no-repeat}
/* un voile pour que le texte et la carte se lisent, plus dense au centre */
.voile{position:fixed;inset:0;z-index:1;
 background:
   radial-gradient(52% 54% at 50% 56%, rgba(18,10,24,.34) 0%, rgba(18,10,24,.20) 50%, rgba(18,10,24,0) 84%),
   linear-gradient(180deg, rgba(18,10,24,.52) 0%, rgba(18,10,24,.14) 22%, rgba(18,10,24,.10) 58%, rgba(18,10,24,.66) 100%)}

.ecran{position:relative;z-index:2;min-height:100vh;display:flex;flex-direction:column;
 align-items:center;justify-content:space-between;padding:30px 24px 24px;gap:18px}

.marque{display:flex;align-items:center;gap:15px}
.marque img{height:44px;width:auto;filter:brightness(0) invert(1);opacity:.95}
.marque .sep{width:1px;height:30px;background:rgba(255,255,255,.28)}
.marque .app{font-family:"Cormorant Garamond",Georgia,serif;font-size:21px;font-weight:400;
 letter-spacing:.14em;color:#fff;line-height:1}

/* ---------- la carte ---------- */
.centre{display:flex;flex-direction:column;align-items:center;gap:18px;width:100%}
.titre{text-align:center;max-width:22ch}
/* Le choix de la langue, dès la porte : la personne qui arrive ne lit pas forcément
   le français, et c'est ici qu'elle doit pouvoir le dire — pas après être entrée. */
.lg{position:absolute;top:14px;right:16px;display:flex;gap:4px;z-index:3}
.lg button{font:600 10.5px/1 Inter,sans-serif;letter-spacing:.06em;padding:6px 8px;border-radius:4px;cursor:pointer;
 border:1px solid rgba(255,255,255,.35);background:rgba(0,0,0,.25);color:#fff}
.lg button.on{background:#fff;color:#111;border-color:#fff}
.titre h1{font-family:"Cormorant Garamond",Georgia,serif;font-weight:300;
 font-size:clamp(30px,3.6vw,46px);line-height:1.1;letter-spacing:-.01em;margin:0 0 8px;color:#fff;
 text-shadow:0 2px 24px rgba(18,10,24,.6)}
.titre h1 em{font-style:italic;color:var(--bronze-clair)}
.titre p{margin:0;font-size:14px;line-height:1.6;color:rgba(255,255,255,.72);
 text-shadow:0 1px 14px rgba(18,10,24,.7)}

/* ---------- la carte : ivoire sur la photo, pour qu'elle se détache ---------- */
.carte{position:relative;width:100%;max-width:396px;background:var(--creme);
 border-radius:4px;padding:30px 32px 26px;
 box-shadow:0 30px 80px rgba(6,2,10,.55),0 2px 6px rgba(6,2,10,.30)}
/* un mince trait doré posé en haut, seule touche de couleur */
.carte::before{content:'';position:absolute;left:0;right:0;top:0;height:3px;
 border-radius:4px 4px 0 0;
 background:linear-gradient(90deg,var(--bronze) 0%,var(--bronze-clair) 50%,var(--bronze) 100%)}
.carte h2{font-family:"Cormorant Garamond",Georgia,serif;font-weight:400;font-size:30px;
 margin:0 0 6px;line-height:1.1;color:var(--ink)}
.carte .sous{margin:0 0 22px;font-size:13px;color:var(--ink-2);line-height:1.6;max-width:36ch}

label.f{display:block;font-size:10px;letter-spacing:.16em;text-transform:uppercase;
 color:var(--ink-3);font-weight:700;margin:0 0 6px}
.champ{margin-bottom:16px}
input[type=text],input[type=password]{width:100%;padding:11px 13px;font-family:inherit;font-size:15px;
 border:1px solid var(--line);border-radius:6px;background:var(--blanc);color:var(--ink);
 transition:border-color .15s,box-shadow .15s}
input[type=text]::placeholder,input[type=password]::placeholder{color:#B6AEA2}
input[type=text]:focus,input[type=password]:focus{outline:0;border-color:var(--bronze);
 box-shadow:0 0 0 3px rgba(200,154,92,.20)}

.btn{width:100%;margin-top:4px;padding:13px 16px;border:0;border-radius:6px;
 background:var(--nuit);color:#fff;font-family:Inter,sans-serif;font-size:14px;font-weight:600;
 cursor:pointer;letter-spacing:.02em;transition:background .16s}
.btn:hover{background:#2C1A3A}
.btn.or{background:var(--bronze);color:#1B1020}
.btn.or:hover{background:#B4863F}
/* bouton secondaire : même taille, mais il ne tire pas l'oeil */
.btn.cl{margin-top:8px;background:transparent;color:var(--ink-2);
 border:1px solid var(--line);font-weight:500}
.btn.cl:hover{background:#F1ECE4;color:var(--ink)}

.msg{margin:12px 0 0;font-size:13px;line-height:1.5;min-height:18px}
.msg.err{color:var(--crit);font-weight:600}
.msg.ok{color:var(--good);font-weight:600}

.note{margin:18px 0 0;padding-top:14px;border-top:1px solid var(--line);
 font-size:11.5px;color:var(--ink-3);line-height:1.62}
.note b{color:var(--ink-2);font-weight:600}

/* ---------- les comptes d'essai : une ligne discrète, pas un tableau ---------- */
.demo{margin:16px 0 0;padding-top:13px;border-top:1px solid var(--line)}
.demo .lab{display:block;font-size:10px;letter-spacing:.16em;text-transform:uppercase;
 color:var(--ink-3);font-weight:700;margin-bottom:8px}
.dbtn{display:flex;flex-wrap:wrap;gap:6px}
.dbtn button{border:1px solid var(--line);background:var(--blanc);border-radius:20px;
 padding:5px 12px;font-family:inherit;font-size:12.5px;color:var(--ink-2);cursor:pointer;
 transition:border-color .15s,color .15s}
.dbtn button:hover{border-color:var(--bronze);color:var(--ink)}
.dnote{margin:9px 0 0;font-size:11px;color:var(--ink-3);line-height:1.6}
.dnote b{color:var(--ink-2);font-weight:600}


@media(max-width:760px){
  .fond{background-position:70% center}
  .ecran{padding:26px 18px 22px;gap:20px}
  .marque img{height:40px} .marque .app{font-size:22px}
  .titre h1{font-size:27px}
  .carte{padding:26px 22px 22px}
  .carte h2{font-size:30px}
    }
@media(max-height:1030px){ .titre p{display:none} .titre h1{font-size:28px;margin-bottom:0;line-height:1.15} }
@media(max-height:860px){ .titre{display:none} }
@media(max-height:740px){ .ecran{padding:20px 24px 18px} }
@media(prefers-reduced-motion:reduce){*{transition:none!important}}
</style></head><body>

<div class="fond"></div>
<div class="voile"></div>

<div class="ecran">

  <div class="marque">
    <img src="data:image/png;base64,__LOGO__" alt="Perfumes Trade">
    <span class="sep"></span>
    <span class="app">ERP</span>
  </div>

  <div class="centre">
    <div class="lg" id="lg"><button data-l="fr">FR</button><button data-l="en">EN</button><button data-l="es">ES</button></div>
    <div class="titre">
      <h1>Le stock, les prix,<br><em>au clair.</em></h1>
      <p>Chaque flacon qui entre, chaque prix qui change — écrit, daté, signé.</p>
    </div>
    <div class="carte" id="carte"></div>
  </div>


</div>

<script src="donnees/langue.js"></script>
<script>
__FUSION__
__COMPTES__
__LANGUE__

const VER_URL='__VER__';
/* Les trois boutons de langue de la porte. On ne passe pas par lgChange : il
   écrit une ligne au journal au nom du compte connecté, et ici personne ne l'est
   encore. On change la langue, on l'enregistre, on retraduit l'écran. */
(function(){
  const z=document.getElementById('lg'); if(!z) return;
  const peint=()=>z.querySelectorAll('button').forEach(b=>b.classList.toggle('on',b.dataset.l===LANG));
  peint();
  z.addEventListener('click',e=>{ const b=e.target.closest('[data-l]'); if(!b||!LANGUES[b.dataset.l]) return;
    LANG=b.dataset.l; try{ localStorage.setItem(K_LANG,LANG); }catch(err){}
    document.documentElement.lang=LANG; lgApplique(document.body); peint(); });
})();
const $=i=>document.getElementById(i);
const esc=s=>String(s==null?'':s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));

/* ---------- premier démarrage : on crée le compte admin ----------
   Le tout premier compte est celui de la personne qui installe l'outil et qui
   branchera les services extérieurs : c'est un Admin, pas un Patron. Le compte
   du patron de l'entreprise se crée ensuite, depuis Accès. Sur une installation
   déjà en service, rien ne change : les comptes existants gardent leur rôle. */
function ecranPremier(){
  $('carte').innerHTML=`
    <h2>Premier démarrage</h2>
    <p class="sous">Aucun compte n'existe encore. Crée celui du patron : c'est le seul
    qui pourra ensuite ouvrir des accès aux autres.</p>
    <div class="champ"><label class="f" for="n">Nom de la personne</label>
      <input type="text" id="n" autocomplete="off" placeholder="Sam"></div>
    <div class="champ"><label class="f" for="i">Identifiant</label>
      <input type="text" id="i" autocomplete="off" placeholder="sam"></div>
    <div class="champ"><label class="f" for="m">Mot de passe</label>
      <input type="password" id="m" autocomplete="new-password" placeholder="au moins 6 caractères"></div>
    <div class="champ"><label class="f" for="m2">Répète le mot de passe</label>
      <input type="password" id="m2" autocomplete="new-password"></div>
    <button class="btn or" id="go">Créer le compte et entrer</button>
    <p class="msg" id="msg"></p>
    ${EN_LIGNE
      ? `<p class="note"><b>Ce compte vit sur le serveur.</b> Il vaut sur tous les appareils, et seul
         le patron pourra ensuite ouvrir, fermer ou changer les accès des autres.</p>`
      : `<p class="note"><b>À savoir.</b> Tant que l'outil tourne sur cet ordinateur et pas sur un serveur,
    ce mot de passe est un <b>badge, pas une serrure</b> : il dit qui travaille et ce que chacun voit.
    La vraie serrure viendra avec le serveur.</p>`}`;
  const val=async()=>{
    const n=$('n').value.trim(), i=$('i').value.trim(), m=$('m').value, m2=$('m2').value;
    const dis=t=>{ $('msg').textContent=t; $('msg').className='msg err'; };
    if(n.length<2) return dis('Mets le nom de la personne.');
    if(!/^[a-zA-Z0-9._-]{2,}$/.test(i)) return dis('Identifiant : lettres, chiffres, point ou tiret, sans espace.');
    if(m.length<6) return dis('Le mot de passe doit faire au moins 6 caractères.');
    if(m!==m2) return dis('Les deux mots de passe ne sont pas identiques.');
    try{
      /* provisoire:false — cette personne vient de choisir son mot de passe
         elle-même, sur cet écran. Lui redemander d'en changer serait absurde. */
      await creeCompte({nom:n,ident:i,mdp:m,role:'admin',par:'premier démarrage',provisoire:false});
      const u=await verifie(i,m); ouvreSession(u);
      journalConnexion(u,'compte patron créé');
      $('msg').textContent='Compte créé. On entre…'; $('msg').className='msg ok';
      setTimeout(()=>location.href=urlDepart(u.role),600);
    }catch(e){ dis(e.message||'Impossible de créer le compte.'); }
  };
  $('go').onclick=val;
  ['n','i','m','m2'].forEach(k=>$(k).addEventListener('keydown',e=>{ if(e.key==='Enter'){ e.preventDefault(); val(); } }));
  setTimeout(()=>$('n').focus(),80);
}

/* ---------- connexion ---------- */
function ecranConnexion(){
  const L=comptes().filter(u=>u.actif);
  const der=L.slice().sort((a,b)=>String(b.dernier||'').localeCompare(String(a.dernier||'')))[0];
  $('carte').innerHTML=`
    <h2>Bonjour</h2>
    <p class="sous">Identifie-toi : chaque prix modifié et chaque flacon qui sort du stock
    sera écrit au journal à ton nom.</p>
    <div class="champ"><label class="f" for="i">Identifiant</label>
      <input type="text" id="i" autocomplete="username"></div>
    <div class="champ"><label class="f" for="m">Mot de passe</label>
      <input type="password" id="m" autocomplete="current-password"></div>
    <button class="btn" id="go">Entrer</button>
    <p class="msg" id="msg"></p>
    ${blocDemo()}
    <p class="note">Mot de passe oublié ? Seul le patron peut en remettre un, depuis <b>Accès</b>.
    Personne ne peut le relire : SAM n'en garde qu'une empreinte.</p>`;
  if(der&&!estDemo()) $('i').value=der.ident;
  const val=async()=>{
    const i=$('i').value.trim(), m=$('m').value;
    if(!i||!m){ $('msg').textContent='Identifiant et mot de passe.'; $('msg').className='msg err'; return; }
    /* Trois issues, et il faut les distinguer : mauvais mot de passe, compte fermé,
       et « le socle ne répond pas ». Sans ce try, une panne du cockpit faisait un
       bouton mort : aucun message, rien à l'écran, et personne ne peut entrer un
       matin d'ouverture sans comprendre pourquoi. */
    let u;
    try{ u=await verifie(i,m); }
    catch(e){
      $('msg').innerHTML='<b>Le socle ne répond pas.</b> Ton identifiant et ton mot de passe '
        +"n'ont pas pu être vérifiés — ce n'est pas toi, c'est la liaison avec le serveur. "
        +'Réessaie dans un instant ; si ça dure, préviens Igal.';
      $('msg').className='msg err';
      return;
    }
    if(u&&u.bloque){ $('msg').textContent='Ce compte est désactivé. Vois avec le patron.';
      $('msg').className='msg err'; return; }
    if(!u){ $('msg').textContent='Identifiant ou mot de passe incorrect.';
      $('msg').className='msg err'; $('m').value=''; $('m').focus(); return; }
    /* Mot de passe provisoire : on n'ouvre PAS la session tant qu'il n'en a pas
       choisi un autre. Ouvrir d'abord et demander ensuite laisserait entrer avec
       un mot de passe qu'un tiers connaît — et que la personne pourrait ignorer
       en fermant l'onglet. */
    if(u.doitChanger) return ecranNouveauMdp(u,m);
    ouvreSession(u); journalConnexion(u,'connexion');
    $('msg').textContent='Bienvenue '+u.nom+'.'; $('msg').className='msg ok';
    setTimeout(()=>location.href=urlDepart(u.role),420);
  };
  $('go').onclick=val;
  ['i','m'].forEach(k=>$(k).addEventListener('keydown',e=>{ if(e.key==='Enter'){ e.preventDefault(); val(); } }));
  setTimeout(()=>$((der&&!estDemo())?'m':'i').focus(),80);
}

/* ---------- premier passage : choisir son propre mot de passe ----------
   Celui qu'on a reçu a été choisi par quelqu'un d'autre, et il a pu passer par un
   email — où il restera des années. Tant qu'il n'est pas remplacé, il n'ouvre
   rien : la session ne s'ouvre qu'après. */
function ecranNouveauMdp(u,ancien){
  $('carte').innerHTML=`
    <h2>Bienvenue ${esc(u.nom)}</h2>
    <p class="sous">Le mot de passe qu'on t'a donné est provisoire : quelqu'un d'autre
    l'a choisi, et il a pu passer par un email. Choisis le tien, il ne sera connu
    que de toi — pas même du patron.</p>
    <div class="champ"><label class="f" for="n1">Ton nouveau mot de passe</label>
      <input type="password" id="n1" autocomplete="new-password"></div>
    <div class="champ"><label class="f" for="n2">Répète-le</label>
      <input type="password" id="n2" autocomplete="new-password"></div>
    <button class="btn" id="ngo">Choisir et entrer</button>
    <p class="msg" id="msg"></p>
    <p class="note">Six caractères au minimum. Personne ne pourra le relire ensuite :
    SAM n'en garde qu'une empreinte. Si tu l'oublies, le patron t'en remettra un autre.</p>`;
  const dis=(t,c)=>{ $('msg').textContent=t; $('msg').className='msg '+(c||'err'); };
  const val=async()=>{
    const a=$('n1').value, b=$('n2').value;
    if(a.length<6) return dis('Six caractères au minimum.');
    if(a!==b) return dis('Les deux ne sont pas identiques.');
    if(a===ancien) return dis("Choisis-en un autre que celui qu'on t'a donné.");
    try{
      await changeMonMotDePasse(u.ident,ancien,a);
      const v=await verifie(u.ident,a);
      if(!v||v.bloque) return dis('Impossible de rouvrir la session. Réessaie.');
      ouvreSession(v); journalConnexion(v,'mot de passe choisi, première connexion');
      dis('C\'est enregistré. Bienvenue.','ok');
      setTimeout(()=>location.href=urlDepart(v.role),420);
    }catch(e){ dis((e&&e.message)||'Impossible.'); }
  };
  $('ngo').onclick=val;
  ['n1','n2'].forEach(k=>$(k).addEventListener('keydown',e=>{ if(e.key==='Enter'){ e.preventDefault(); val(); } }));
  setTimeout(()=>$('n1').focus(),80);
}

function journalConnexion(u,lib){
  try{
    const J=lit('crm-journal-v1',[]);
    J.push({t:new Date().toISOString(),u:u.nom,act:'acces',lib,
            ref:u.ident,av:null,ap:(ROLES[u.role]||{}).lib||u.role});
    ecrit('crm-journal-v1',J);
  }catch(e){}
}

/* ---------- comptes de démonstration ----------
   Pour essayer SAM tout de suite, et pour montrer les rôles à quelqu'un.
   Ils portent un mot de passe connu : à supprimer avant la vraie mise en service. */
const DEMO=[
  {nom:'Igal',       ident:'igal',     mdp:'igal123',     role:'admin'},
  {nom:'Sam',        ident:'sam',      mdp:'sam123',      role:'patron'},
  {nom:'Javier',     ident:'javier',   mdp:'javier123',   role:'commercial'},
  {nom:'Ana',        ident:'ana',      mdp:'ana123',      role:'entrepot'},
  {nom:'Le comptable',ident:'compta',  mdp:'compta123',   role:'comptable'}];
const K_DEMO='sam-comptes-demo-v1';

async function poseDemo(){
  /* provisoire:false — les comptes d'essai s'ouvrent d'un clic et leur mot de
     passe est écrit à l'écran juste en dessous. Leur demander d'en choisir un
     autre transformerait une démonstration de trente secondes en formulaire. */
  for(const d of DEMO){ try{ await creeCompte({...d, par:'démonstration', provisoire:false}); }catch(e){} }
  try{ localStorage.setItem(K_DEMO,'1'); }catch(e){}
}
const estDemo=()=>{ try{ return localStorage.getItem(K_DEMO)==='1'; }catch(e){ return false; } };
/* '1' = démonstration en cours, '0' = terminée (on ne remet jamais les comptes),
   absent = SAM n'a encore jamais démarré sur ce poste. */
const demoJamais=()=>{ try{ return localStorage.getItem(K_DEMO)===null; }catch(e){ return false; } };

function blocDemo(){
  if(!estDemo()) return '';
  return `<div class="demo">
    <span class="lab">Comptes d\'essai</span>
    <div class="dbtn">${DEMO.map(d=>{
      const r=ROLES[d.role]||{};
      return `<button data-d="${esc(d.ident)}" title="${esc(r.lib||d.role)}">${esc(d.nom)}</button>`;
    }).join('')}</div>
    <p class="dnote">Un clic pour entrer — un compte par rôle. Mot de passe : le prénom + 123.
    <b>À fermer dans Accès</b> avant la vraie mise en service.</p>
  </div>`;
}
function brancheDemo(){
  const z=document.querySelector('.dbtn'); if(!z) return;
  z.addEventListener('click',async e=>{
    const b=e.target.closest('[data-d]'); if(!b) return;
    const d=DEMO.find(x=>x.ident===b.dataset.d); if(!d) return;
    const u=await verifie(d.ident,d.mdp);
    if(!u){ $('msg').textContent='Ce compte de démonstration a été modifié — entre son mot de passe.';
      $('msg').className='msg err'; $('i').value=d.ident; $('m').focus(); return; }
    ouvreSession(u); journalConnexion(u,'connexion (démonstration)');
    $('msg').textContent='Bienvenue '+u.nom+'.'; $('msg').className='msg ok';
    setTimeout(()=>location.href=urlDepart(u.role),380);
  });
}

/* ---------- déjà connecté ----------
   Avant, la page sautait toute seule au catalogue : on avait l'impression que
   l'accueil avait disparu. Maintenant elle se montre et laisse le choix. */
function ecranDejaLa(s){
  const r=ROLES[s.role]||{lib:s.role};
  $('carte').innerHTML=`
    <h2>Te revoilà</h2>
    <p class="sous">Une session est déjà ouverte sur cet ordinateur, au nom de
    <b>${esc(s.nom)}</b> — ${esc(r.lib)}. Tout ce qui sera modifié sera écrit au journal
    à ce nom-là.</p>
    <button class="btn" id="go">Continuer comme ${esc(s.nom)}</button>
    <button class="btn cl" id="chg">Ce n'est pas moi — changer de compte</button>
    <p class="msg" id="msg"></p>
    <p class="note">Tu peux aussi te déconnecter à tout moment depuis le bas de la barre
    de gauche, dans n'importe quelle rubrique de SAM.</p>`;
  $('go').onclick=()=>location.href=urlDepart(s.role);
  $('chg').onclick=()=>{
    try{ const J=lit('crm-journal-v1',[]);
      J.push({t:new Date().toISOString(),u:s.nom,act:'acces',lib:'déconnexion',ref:s.id,av:null,ap:null});
      ecrit('crm-journal-v1',J); }catch(e){}
    /* quitteSession, pas un simple removeItem : en ligne il faut aussi rendre le
       jeton du serveur, sinon la personne suivante hérite d'une session valide. */
    quitteSession();
    ecranConnexion(); brancheDemo();
  };
}

/* En ligne (sur le serveur), jamais de comptes d'essai : leurs mots de passe
   sont connus de tous. Ils n'existent que sur un poste local, pour montrer.
   EN_LIGNE vient de _comptes : en ligne, c'est le cockpit qui tient les comptes. */
function retireDemo(){
  const L=comptes().filter(u=>u.par!=='démonstration');
  if(L.length!==comptes().length) sauveComptes(L);
  try{ localStorage.setItem(K_DEMO,'0'); }catch(e){}
}

(async function(){
  const s=session();
  if(s && EN_LIGNE && comptes().some(u=>u.ident===s.id && u.par==='démonstration')){
    try{ localStorage.removeItem('sam-session-v1'); }catch(e){}
  }
  else if(s){ ecranDejaLa(s); return; }
  if(EN_LIGNE){
    retireDemo();
    /* c'est le cockpit qui sait s'il y a déjà quelqu'un */
    try{
      const e=await ck('GET','/etat');
      if(e.premier){ ecranPremier(); return; }
    }catch(err){
      $('carte').innerHTML='<h2>Le serveur ne répond pas</h2><p class="sous">'+String(err.message).replace(/[<>]/g,'')+'</p>'
        +'<button class="btn" id="go">Réessayer</button>';
      $('go').onclick=()=>location.reload(); return;
    }
    ecranConnexion(); return;
  }
  /* premier démarrage de SAM sur ce poste : on pose les comptes d'essai.
     Une fois la démonstration terminée, on ne les remet jamais. */
  if(!comptes().length && demoJamais()) await poseDemo();
  if(!comptes().length){ ecranPremier(); return; }
  ecranConnexion(); brancheDemo();
})();
</script></body></html>'''

out = (TPL.replace('__FUSION__', FUSION)
          .replace('__COMPTES__', COMPTES)
          .replace('__LANGUE__', LANGUE)
          .replace('__LOGO__', LOGO)
          .replace('__FOND__', FOND)
          .replace('__VER__', __import__('datetime').datetime.now().strftime('%Y%m%d%H%M')))
open('accueil.html', 'w').write(enligne(out))
print('accueil.html', round(os.path.getsize('accueil.html') / 1024), 'Ko')
