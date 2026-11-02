# -*- coding: utf-8 -*-
"""Demander de l'aide, depuis n'importe quelle page.

Le problème qu'on cherche à résoudre n'est pas « comment envoyer un message ».
C'est : quelqu'un est bloqué devant son écran, il ne sait pas à qui écrire, il
attend le lendemain, et pendant ce temps il fait la vente à la main sur un
carnet. Le lendemain il dit « ça marchait pas » et personne ne sait de quoi il
parle.

Donc trois décisions, et elles ne sont pas décoratives :

1. Le bouton est sur TOUTES les pages, au même endroit. Une aide qu'il faut
   aller chercher dans un menu Réglages n'est jamais utilisée par celui qui en
   a besoin — celui-là est déjà perdu.

2. La question part avec la page d'où elle a été posée, ajoutée toute seule.
   « Ça ne marche pas » depuis Ventes et depuis Accès ne sont pas le même
   problème, et personne ne pense jamais à le préciser.

3. Trois niveaux, pas cinq : une question · ça me gêne · je suis bloqué.
   Quelqu'un de bloqué doit pouvoir le dire en un clic, sans se demander si
   c'est « moyen » ou « élevé ».

La réponse revient au même endroit : le bouton porte une pastille quand une
réponse est arrivée. Sinon il faudrait dire aux gens d'aller regarder, et
personne ne va regarder.
"""

CSS = """
.aid-b{display:block;margin-top:7px;position:relative}
.aid-b .pt{display:inline-block;min-width:16px;padding:0 5px;margin-left:6px;border-radius:99px;
background:var(--iris);color:#fff;font-size:10px;font-weight:700;line-height:16px;text-align:center;
text-decoration:none}
.aid-ov{position:fixed;inset:0;background:rgba(23,23,29,.55);backdrop-filter:blur(2px);z-index:9990;
display:none;align-items:flex-start;justify-content:center;padding:40px 18px;overflow-y:auto}
.aid-ov.on{display:flex}
.aid-m{background:var(--surface);border:1px solid var(--line);border-radius:8px;width:100%;
max-width:560px;box-shadow:0 18px 48px rgba(0,0,0,.24)}
.aid-h{padding:16px 20px;border-bottom:1px solid var(--line);display:flex;align-items:center;gap:12px}
.aid-h h2{margin:0;font-size:17px;font-weight:700;letter-spacing:-.02em}
.aid-h .x{margin-left:auto;background:none;border:0;font-size:22px;color:var(--ink-3);cursor:pointer;
line-height:1;padding:2px 6px;font-family:inherit}
.aid-h .x:hover{color:var(--ink)}
.aid-b2{padding:18px 20px;display:flex;flex-direction:column;gap:13px}
.aid-lab{font-family:Inter,sans-serif;font-size:9.5px;letter-spacing:.12em;text-transform:uppercase;
color:var(--ink-3);font-weight:500}
.aid-u{display:flex;gap:8px;flex-wrap:wrap}
.aid-u button{font-family:inherit;font-size:13px;font-weight:600;padding:8px 13px;border-radius:99px;
border:1px solid var(--line);background:var(--surface-2);color:var(--ink-2);cursor:pointer}
.aid-u button.on{background:var(--iris);border-color:var(--iris);color:#fff}
.aid-u button.on[data-u="bloque"]{background:var(--crit);border-color:var(--crit)}
.aid-m textarea{font-family:Inter,sans-serif;font-size:13.5px;line-height:1.6;color:var(--ink);
background:var(--surface-2);border:1px solid var(--line);border-radius:4px;padding:10px 12px;
width:100%;min-height:110px;resize:vertical}
.aid-m textarea:focus{outline:2px solid var(--iris);outline-offset:1px;background:var(--surface)}
.aid-ou{font-size:12.5px;color:var(--ink-3);line-height:1.6}
.aid-ou b{color:var(--ink-2)}
.aid-go{font-family:inherit;font-size:14px;font-weight:600;padding:10px 18px;border-radius:5px;
border:1px solid var(--iris);background:var(--iris);color:#fff;cursor:pointer;align-self:flex-start}
.aid-go:disabled{opacity:.5;cursor:default}
.aid-msg{font-size:13px;line-height:1.6;margin:0}
.aid-msg.ok{color:var(--ok,#1e7a3c)}.aid-msg.err{color:var(--crit)}
.aid-hist{border-top:1px solid var(--line);padding:14px 20px 18px;max-height:280px;overflow-y:auto}
.aid-q{border-left:2px solid var(--line);padding:2px 0 2px 11px;margin-bottom:12px}
.aid-q .m{font-size:11.5px;color:var(--ink-3);margin-bottom:3px}
.aid-q .t{font-size:13px;white-space:pre-wrap}
.aid-q .r{margin-top:7px;background:var(--surface-2);border-radius:5px;padding:8px 11px;
font-size:13px;white-space:pre-wrap}
.aid-q .r b{display:block;font-size:10px;letter-spacing:.1em;text-transform:uppercase;
color:var(--iris);margin-bottom:3px}
"""

JS = r"""
/* ---------- Poser une question au support technique ---------- */
/* Elle part vers le cockpit, pas dans le navigateur : une question enfermée
   dans le localStorage de celui qui est bloqué n'a jamais aidé personne. */
const AID_VU='aide-vu-v1';
let AID_URG='question', AID_LISTE=[];

function aidPage(){
  const h=document.querySelector('.main h1');
  return ((h&&h.textContent)||document.title||'').replace(/ — Perfumes Trade.*$/,'').trim().slice(0,60);
}
function aidPeut(){
  try{ return location.protocol!=='file:' && !!ckTok(); }catch(e){ return false; }
}
async function aidApi(methode,corps){
  const r=await fetch(CK_URL+'/api/o/'+CK_ORG+'/support',{method:methode,
    headers:{'Content-Type':'application/json',Authorization:'Bearer '+ckTok()},
    body:corps===undefined?undefined:JSON.stringify(corps)});
  const j=await r.json().catch(()=>({}));
  if(!r.ok) throw new Error(j.erreur||('serveur '+r.status));
  return j;
}

/* La pastille : une réponse est arrivée et n'a pas encore été ouverte. On
   retient le dernier numéro vu — pas « lu / non lu » par question, parce
   qu'une case à cocher de plus est une case qu'on oublie de cocher. */
function aidVu(){ try{ return +(localStorage.getItem(AID_VU)||0)||0; }catch(e){ return 0; } }
function aidPastille(n){
  /* la pastille se pose sur la ligne « Support technique » du menu */
  const c=document.getElementById('ct-support'), b=document.getElementById('aid-btn'); if(!c||!b) return;
  c.textContent=n?String(n):''; c.className=n?'ct pt':'ct';
  b.title=n?(n+(n>1?' réponses du support':' réponse du support')):'';
}
async function aidRegarde(){
  if(!aidPeut()) return;
  try{
    AID_LISTE=await aidApi('GET');
    const vu=aidVu();
    aidPastille(AID_LISTE.filter(q=>q.reponse&&q.id>vu).length);
  }catch(e){}
}

function aidOuvre(){
  let ov=document.getElementById('aid-ov');
  if(!ov){
    ov=document.createElement('div'); ov.id='aid-ov'; ov.className='aid-ov';
    ov.innerHTML='<div class="aid-m">'
      +'<div class="aid-h"><h2>Support technique</h2><button class="x" id="aid-x">&times;</button></div>'
      +'<div class="aid-b2">'
      +'<div><div class="aid-lab">C\'est à quel point gênant ?</div>'
      +'<div class="aid-u" id="aid-u">'
      +'<button data-u="question" class="on">Juste une question</button>'
      +'<button data-u="gene">Ça me gêne</button>'
      +'<button data-u="bloque">Je suis bloqué</button></div></div>'
      +'<div><div class="aid-lab">Ton message ou ta réclamation</div>'
      +'<textarea id="aid-t" placeholder="Décris le problème : ce que tu essayais de faire, et ce qui s\'est passé."></textarea></div>'
      +'<div class="aid-ou" id="aid-ou"></div>'
      +'<button class="aid-go" id="aid-go">Envoyer</button>'
      +'<p class="aid-msg" id="aid-msg"></p></div>'
      +'<div class="aid-hist" id="aid-hist"></div></div>';
    document.body.appendChild(ov);
    ov.addEventListener('click',e=>{ if(e.target===ov) aidFerme(); });
    document.getElementById('aid-x').onclick=aidFerme;
    document.getElementById('aid-u').addEventListener('click',e=>{
      const b=e.target.closest('[data-u]'); if(!b) return;
      AID_URG=b.dataset.u;
      ov.querySelectorAll('#aid-u button').forEach(x=>x.classList.toggle('on',x===b));
    });
    document.getElementById('aid-go').onclick=aidEnvoie;
    document.addEventListener('keydown',e=>{ if(e.key==='Escape'&&ov.classList.contains('on')) aidFerme(); });
  }
  const util=(typeof NOM_UTIL!=='undefined'&&NOM_UTIL)?NOM_UTIL:'';
  document.getElementById('aid-ou').innerHTML=
    'Partent avec ta question, sans que tu aies à les écrire : la page <b>'+aidEsc(aidPage())+'</b>'
    +(util?' et ton nom, <b>'+aidEsc(util)+'</b>':'')+'.';
  const msg=document.getElementById('aid-msg'); msg.textContent=''; msg.className='aid-msg';
  const go=document.getElementById('aid-go');
  if(!aidPeut()){
    msg.textContent='Cette copie de l\'outil n\'est pas reliée au serveur : la question ne peut pas partir d\'ici.';
    msg.className='aid-msg err'; go.disabled=true;
  } else { go.disabled=false; }
  ov.classList.add('on');
  const t=document.getElementById('aid-t'); if(t&&aidPeut()) setTimeout(()=>t.focus(),60);
  aidHistorique();
}
function aidFerme(){
  const ov=document.getElementById('aid-ov'); if(ov) ov.classList.remove('on');
  /* fermer, c'est avoir vu : les réponses affichées ne clignotent plus */
  const max=AID_LISTE.reduce((a,q)=>Math.max(a,q.reponse?q.id:0),0);
  if(max){ try{ localStorage.setItem(AID_VU,String(max)); }catch(e){} }
  aidPastille(0);
}
function aidEsc(s){ return String(s==null?'':s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c])); }

async function aidEnvoie(){
  const t=document.getElementById('aid-t'), msg=document.getElementById('aid-msg'),
        go=document.getElementById('aid-go');
  const texte=(t.value||'').trim();
  if(texte.length<3){ msg.textContent='Écris ton message, même en deux mots.'; msg.className='aid-msg err'; t.focus(); return; }
  go.disabled=true; msg.textContent='Envoi…'; msg.className='aid-msg';
  try{
    await aidApi('POST',{texte,urgence:AID_URG,page:aidPage()});
    t.value='';
    msg.textContent=AID_URG==='bloque'
      ? 'C\'est parti, et le téléphone d\'Igal sonne. Laisse cet onglet ouvert.'
      : 'C\'est parti. La réponse reviendra ici même, dans « Support technique ».';
    msg.className='aid-msg ok';
    await aidRegarde(); aidHistorique();
  }catch(e){
    msg.textContent='Pas partie : '+e.message+'. Réessaie dans un instant — rien n\'est perdu, ton texte est toujours là.';
    msg.className='aid-msg err';
  }
  go.disabled=false;
}

function aidHistorique(){
  const h=document.getElementById('aid-hist'); if(!h) return;
  if(!AID_LISTE.length){ h.innerHTML=''; return; }
  const dfr=s=>{ try{ return new Date(s).toLocaleString('en-US',{timeZone:'America/New_York',day:'2-digit',month:'2-digit',hour:'2-digit',minute:'2-digit'}); }catch(e){ return ''; } };
  const nom={question:'question',gene:'gêne',bloque:'bloqué'};
  h.innerHTML='<div class="aid-lab" style="margin-bottom:9px">Tes questions précédentes</div>'
    +AID_LISTE.slice(0,12).map(q=>'<div class="aid-q"><div class="m">'+dfr(q.cree)+' · '
      +aidEsc(nom[q.urgence]||q.urgence)+(q.page?' · '+aidEsc(q.page):'')+'</div>'
      +'<div class="t">'+aidEsc(q.texte)+'</div>'
      +(q.reponse?'<div class="r"><b>Réponse du support</b>'+aidEsc(q.reponse)+'</div>'
                 :'<div class="m" style="margin-top:5px">en attente de réponse</div>')
      +'</div>').join('');
}

/* Le bouton, au bas de la barre de gauche, sur toutes les pages.
   Il se remet tout seul : l'Inventaire réécrit le bas de sa barre une fois ses
   chiffres calculés (« 4 812 références, 1 203 en stock… »), et cette
   réécriture emportait le bouton. Le défaut ne se voyait que sur deux pages
   sur quinze, et il aurait suffi qu'une autre page fasse pareil demain pour
   qu'il revienne ailleurs. Plutôt que de courir après l'ordre d'exécution, on
   surveille : si le bas de la barre est refait, le bouton revient. */
/* Depuis le 9 oct. 2026 le bouton n'est plus au pied de la barre : c'est la rubrique
   « Support technique » du menu (id aid-btn), qui ouvre cette fenêtre. */
let AID_PREMIER=true;
function aidBouton(){
  const b=document.getElementById('aid-btn'); if(!b) return;
  if(AID_PREMIER){ AID_PREMIER=false; aidRegarde(); }
}
if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',aidBouton);
else aidBouton();
window.addEventListener('load',()=>setTimeout(aidBouton,0));
/* on regarde de temps en temps : une réponse arrivée pendant la journée doit
   se voir sans recharger la page */
setInterval(aidRegarde,180000);
"""
