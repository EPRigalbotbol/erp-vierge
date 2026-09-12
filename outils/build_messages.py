# -*- coding: utf-8 -*-
"""La rubrique Messages : écrire à quelqu'un de l'équipe, dans l'outil.

À ne pas confondre avec le bouton « Écrire » des fiches : celui-là s'adresse au
dehors — un client, un fournisseur — et passe par le mail ou WhatsApp. Ici, on
parle entre comptes de Perfumes Trade : Sam laisse une consigne à Javier, Ana
signale qu'il manque douze flacons, le comptable réclame une facture.

Ce qu'il faut dire à Sam avant qu'il ne compte dessus. Tant que l'outil tourne
dans le navigateur, les messages restent dans CE navigateur, sur CET ordinateur.
C'est donc un cahier de consignes partagé par les gens qui se relaient sur le
même poste — l'entrepôt, la boutique — et rien d'autre : un message écrit ici
n'arrivera jamais sur le téléphone de Javier. Le jour où il y a un serveur, le
même écran devient une vraie messagerie, sans rien changer à ce qui est écrit
là ; c'est pour ça que ça vaut la peine de le construire maintenant.

Ce qui est fait pour tenir jusqu'au serveur : un message est immuable une fois
envoyé (pas de modification, pas d'effacement — sinon la consigne ne vaut rien),
il est signé du compte connecté, et il est lu ou non lu par destinataire.
"""
import os
from build_crm import coquille

CSS = """
.bandeau{background:var(--warn-soft);border-left:3px solid var(--warn);border-radius:0 9px 9px 0;
 padding:14px 17px;font-size:13.5px;color:var(--ink-2);line-height:1.62;margin:0 0 22px;max-width:88ch}
.bandeau b{color:var(--ink)}

.deux{display:grid;grid-template-columns:280px 1fr;gap:18px;align-items:start}
@media(max-width:900px){.deux{grid-template-columns:1fr}}

.gens{border:1px solid var(--line);border-radius:12px;background:var(--surface);overflow:hidden}
.gens h3{margin:0;padding:12px 15px;font-size:9.5px;letter-spacing:.11em;text-transform:uppercase;
 color:var(--ink-3);font-weight:700;background:var(--surface-2);border-bottom:1px solid var(--line)}
.gens button{display:flex;width:100%;gap:11px;align-items:center;padding:12px 15px;background:none;
 border:0;border-bottom:1px solid var(--line-2);font-family:inherit;text-align:left;cursor:pointer}
.gens button:last-child{border-bottom:0}
.gens button:hover{background:var(--surface-2)}
.gens button.on{background:var(--iris-soft)}
.gens .pa{flex:none;width:34px;height:34px;border-radius:50%;background:var(--surface-2);
 color:var(--ink-2);display:flex;align-items:center;justify-content:center;font-size:12.5px;font-weight:700}
.gens button.on .pa{background:var(--iris);color:#fff}
.gens .nn{flex:1;min-width:0}
.gens .nn b{display:block;font-size:14px;font-weight:600;color:var(--ink);line-height:1.25}
.gens .nn span{display:block;font-size:11.5px;color:var(--ink-3)}
.gens .pt{flex:none;min-width:20px;height:20px;padding:0 6px;border-radius:10px;background:var(--crit);
 color:#fff;font-size:11px;font-weight:700;display:flex;align-items:center;justify-content:center}
.gens .pt.z{display:none}

.fil{border:1px solid var(--line);border-radius:12px;background:var(--surface);
 display:flex;flex-direction:column;min-height:440px}
.fil .th{padding:14px 18px;border-bottom:1px solid var(--line);display:flex;align-items:baseline;gap:10px}
.fil .th b{font-size:16px;font-weight:700;color:var(--ink)}
.fil .th span{font-size:12.5px;color:var(--ink-3)}
.fil .co{flex:1;overflow-y:auto;max-height:480px;padding:18px;display:flex;flex-direction:column;gap:13px}
.fil .vide{margin:auto;text-align:center;color:var(--ink-3);font-size:13.5px;line-height:1.7;max-width:44ch}

.bulle{max-width:78%;padding:11px 14px;border-radius:13px;font-size:13.5px;line-height:1.6;
 color:var(--ink);white-space:pre-wrap;word-break:break-word}
.bulle.moi{align-self:flex-end;background:var(--iris);color:#fff;border-bottom-right-radius:4px}
.bulle.lui{align-self:flex-start;background:var(--surface-2);border:1px solid var(--line);
 border-bottom-left-radius:4px}
.bulle .q{display:block;margin-top:6px;font-size:11px;opacity:.72}
.bulle.moi .q{color:#fff}
.jourlab{align-self:center;font-size:11px;letter-spacing:.08em;text-transform:uppercase;
 color:var(--ink-3);font-weight:600;padding:2px 0}

.ecr{border-top:1px solid var(--line);padding:13px 15px;display:flex;gap:10px;align-items:flex-end}
.ecr textarea{flex:1;min-height:44px;max-height:150px;padding:11px 13px;font-family:inherit;
 font-size:14px;border:1px solid var(--line);border-radius:10px;background:var(--surface);
 color:var(--ink);resize:vertical;line-height:1.55}
.ecr .btn{flex:none}
.aidefld{font-size:12px;color:var(--ink-3);line-height:1.55;margin:9px 0 0}
.mur{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:34px 32px;
 max-width:62ch;margin:40px auto;text-align:center}
.mur h2{margin:0 0 10px;font-size:20px;font-weight:700}
.mur p{margin:0;color:var(--ink-2);font-size:14.5px;line-height:1.65}
"""

CORPS = """
<div class="bandeau" id="ban"></div>
<div class="deux" id="tout" hidden>
  <div class="gens"><h3>L'équipe</h3><div id="liste"></div></div>
  <div class="fil">
    <div class="th"><b id="qui">—</b><span id="role"></span></div>
    <div class="co" id="co"></div>
    <div class="ecr">
      <textarea id="txt" rows="2" placeholder="Écris ton message…"></textarea>
      <button class="btn pri" id="env">Envoyer</button>
    </div>
  </div>
</div>
"""

JS = r"""
const K_MSG='messages-v1';

function msgs(){ const L=lit(K_MSG,[]); return Array.isArray(L)?L:[]; }
function sauveMsgs(L){ ecrit(K_MSG,L); }

const MOI=session();
const autres=()=>comptes().filter(u=>u.ident!==(MOI&&MOI.id));
let CIBLE=null;

const ini=n=>String(n||'?').trim().split(/\s+/).slice(0,2).map(m=>m[0]||'').join('').toUpperCase()||'?';
const hm=iso=>{ const d=new Date(iso); return d.toLocaleTimeString('fr-FR',{hour:'2-digit',minute:'2-digit'}); };
const jourDe=iso=>new Date(iso).toDateString();
function libJour(iso){
  const d=new Date(iso), a=new Date(), h=new Date(a.getTime()-86400000);
  if(d.toDateString()===a.toDateString()) return "Aujourd'hui";
  if(d.toDateString()===h.toDateString()) return 'Hier';
  return d.toLocaleDateString('fr-FR',{weekday:'long',day:'2-digit',month:'long'});
}

/* Le fil entre moi et une personne : les deux sens, dans l'ordre. */
const filAvec=id=>msgs().filter(m=>
  (m.de===MOI.id && m.a===id) || (m.de===id && m.a===MOI.id));
const nonLus=id=>msgs().filter(m=>m.de===id && m.a===MOI.id && !m.lu).length;

function peintGens(){
  $('liste').innerHTML=autres().map(u=>{
    const n=nonLus(u.ident);
    return `<button data-u="${esc(u.ident)}" class="${u.ident===CIBLE?'on':''}">
      <span class="pa">${esc(ini(u.nom))}</span>
      <span class="nn"><b>${esc(u.nom)}</b><span>${esc((ROLES[u.role]||{}).lib||u.role)}${u.actif?'':' · accès fermé'}</span></span>
      <span class="pt ${n?'':'z'}">${n}</span></button>`;
  }).join('') || '<div style="padding:20px 15px;font-size:13px;color:var(--ink-3);line-height:1.6">'
    +'Il n\'y a que toi pour l\'instant. Ouvre un accès dans <b>Accès</b> et tu pourras lui écrire.</div>';
  const t=msgs().filter(m=>m.a===MOI.id && !m.lu).length;
  $('src').innerHTML = t ? t+' message'+(t>1?'s':'')+' non lu'+(t>1?'s':'') : 'aucun message non lu';
}

function peintFil(){
  const co=$('co');
  if(!CIBLE){
    $('qui').textContent='—'; $('role').textContent='';
    co.innerHTML='<div class="vide">Choisis quelqu\'un dans la liste de gauche pour lui écrire.</div>';
    return;
  }
  const u=comptes().find(x=>x.ident===CIBLE)||{nom:CIBLE};
  $('qui').textContent=u.nom;
  $('role').textContent=(ROLES[u.role]||{}).lib||'';
  const F=filAvec(CIBLE);
  if(!F.length){
    co.innerHTML=`<div class="vide">Rien d'échangé avec ${esc(u.nom)} pour l'instant.<br>
      Écris le premier message en bas.</div>`;
    return;
  }
  let j=null, out=[];
  F.forEach(m=>{
    const dj=jourDe(m.t);
    if(dj!==j){ j=dj; out.push(`<div class="jourlab">${esc(libJour(m.t))}</div>`); }
    const moi=m.de===MOI.id;
    out.push(`<div class="bulle ${moi?'moi':'lui'}">${esc(m.txt)}
      <span class="q">${hm(m.t)}${moi?(m.lu?' · lu':' · envoyé'):''}</span></div>`);
  });
  co.innerHTML=out.join('');
  co.scrollTop=co.scrollHeight;
}

/* Ouvrir un fil marque comme lus les messages de cette personne. */
function ouvre(id){
  CIBLE=id;
  const L=msgs(); let bouge=false;
  L.forEach(m=>{ if(m.de===id && m.a===MOI.id && !m.lu){ m.lu=new Date().toISOString(); bouge=true; } });
  if(bouge) sauveMsgs(L);
  peintGens(); peintFil();
  if(typeof mnPastilleMessages==='function') mnPastilleMessages();
}

function envoie(){
  const t=$('txt').value.trim();
  if(!CIBLE) return alert('Choisis d\'abord à qui tu écris.');
  if(!t) return;
  const L=msgs();
  L.push({id:Date.now().toString(36)+Math.random().toString(36).slice(2,7),
          t:new Date().toISOString(), de:MOI.id, deNom:MOI.nom, a:CIBLE, txt:t.slice(0,2000), lu:null});
  sauveMsgs(L);
  const J=lit('crm-journal-v1',[]);
  const u=comptes().find(x=>x.ident===CIBLE)||{nom:CIBLE};
  J.push({t:new Date().toISOString(),u:MOI.nom,act:'message',
          lib:'message envoyé à '+u.nom,ref:CIBLE,av:null,ap:null});
  ecrit('crm-journal-v1',J);
  $('txt').value=''; peintFil(); peintGens();
}

$('liste').addEventListener('click',e=>{
  const b=e.target.closest('button[data-u]'); if(!b) return; ouvre(b.dataset.u);
});
$('env').onclick=envoie;
$('txt').addEventListener('keydown',e=>{
  if(e.key==='Enter' && (e.metaKey||e.ctrlKey)){ e.preventDefault(); envoie(); }
});

/* Deux onglets ouverts sur le même poste : ce qui est écrit dans l'un
   apparaît dans l'autre. C'est le seul « direct » qu'on sache faire sans serveur. */
window.addEventListener('storage',e=>{
  if(e.key===K_MSG){ peintGens(); if(CIBLE) peintFil(); }
});

(function(){
  if(!MOI) return;
  $('ban').innerHTML=`<b>Ce que c'est, et ce que ce n'est pas encore.</b>
    Ici on écrit aux gens de l'équipe — pas aux clients : pour eux, c'est le bouton
    <b>Écrire</b> sur leur fiche. Tant que Perfumes Trade tourne sur cet ordinateur et pas
    sur un serveur, <b>les messages restent sur cet ordinateur</b> : c'est un cahier de
    consignes pour ceux qui se relaient sur le même poste, pas une messagerie qui arrive
    sur le téléphone de Javier. Le jour où il y a un serveur, cet écran ne change pas et
    devient une vraie messagerie — ce qui est écrit maintenant n'est pas perdu.`;
  $('tout').hidden=false;
  peintGens();
  /* On ouvre d'abord le fil de celui qui attend une réponse : sinon la page
     ouvre le premier venu et consomme silencieusement ses non-lus. */
  const A=autres();
  const attend=A.find(u=>nonLus(u.ident));
  ouvre(attend ? attend.ident : (A.length?A[0].ident:null));
  $('sfoot').innerHTML='Messages internes';
})();
"""

html = coquille("Messages", "Messages",
                "Écrire aux gens de l'équipe, sans sortir de l'outil",
                CSS, CORPS, JS)
open('messages.html', 'w').write(html)
print('messages.html', round(os.path.getsize('messages.html') / 1024), 'Ko')
