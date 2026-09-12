# -*- coding: utf-8 -*-
"""Écrire à quelqu'un — depuis n'importe quelle rubrique où il y a des coordonnées.

Un fournisseur, un client wholesale, un client du site : partout où l'outil
connaît un nom, il doit pouvoir ouvrir un message tout prêt. C'est le même
bouton et la même fenêtre partout, d'où ce fichier partagé.

Ce que ça fait vraiment, et il faut le dire clairement à l'écran :
ça PRÉPARE le message et ça ouvre le mail ou WhatsApp avec le texte dedans.
C'est la personne qui appuie sur Envoyer. Un vrai envoi en masse — une promo
à trois cents clients d'un coup — demande un service d'envoi et un serveur ;
tant que Perfumes Trade tourne dans le navigateur, c'est un à la fois.

Le numéro : WhatsApp veut le numéro en chiffres avec l'indicatif pays. On
enlève tout ce qui n'est pas un chiffre, et un numéro américain à dix chiffres
reçoit le 1 devant. Si le numéro est étranger et mal écrit, on le dit au lieu
d'ouvrir une conversation avec le mauvais numéro.
"""

CONTACT = r"""
/* ============ ÉCRIRE À QUELQU'UN ============ */
const CT_MODELES={
 fr:{
  promo:{o:"Une offre pour vous", t:"Bonjour NOM,\n\nNous avons en ce moment de belles pièces à des prix intéressants. Dites-moi ce qui vous intéresse et je vous prépare une offre.\n\nÀ bientôt,\nPerfumes Trade"},
  relance:{o:"Votre facture", t:"Bonjour NOM,\n\nJe reviens vers vous au sujet de votre facture, qui reste ouverte à ce jour. Pouvez-vous me dire où cela en est de votre côté ?\n\nMerci d'avance,\nPerfumes Trade"},
  merci:{o:"Merci pour votre commande", t:"Bonjour NOM,\n\nMerci pour votre commande. Elle est bien enregistrée. N'hésitez pas si vous avez la moindre question.\n\nÀ bientôt,\nPerfumes Trade"},
  libre:{o:"", t:"Bonjour NOM,\n\n"}},
 en:{
  promo:{o:"An offer for you", t:"Hello NOM,\n\nWe currently have some great pieces at good prices. Let me know what you are looking for and I will put together an offer.\n\nBest regards,\nPerfumes Trade"},
  relance:{o:"Your invoice", t:"Hello NOM,\n\nI am following up on your invoice, which is still open. Could you let me know where things stand on your side?\n\nThank you,\nPerfumes Trade"},
  merci:{o:"Thank you for your order", t:"Hello NOM,\n\nThank you for your order — it is confirmed. Please reach out with any question.\n\nBest regards,\nPerfumes Trade"},
  libre:{o:"", t:"Hello NOM,\n\n"}},
 es:{
  promo:{o:"Una oferta para usted", t:"Hola NOM,\n\nTenemos ahora mismo buenas piezas a precios interesantes. Dígame qué le interesa y le preparo una oferta.\n\nUn saludo,\nPerfumes Trade"},
  relance:{o:"Su factura", t:"Hola NOM,\n\nLe escribo por su factura, que sigue pendiente. ¿Puede decirme cómo está por su parte?\n\nGracias,\nPerfumes Trade"},
  merci:{o:"Gracias por su pedido", t:"Hola NOM,\n\nGracias por su pedido, queda registrado. Cualquier duda, aquí estoy.\n\nUn saludo,\nPerfumes Trade"},
  libre:{o:"", t:"Hola NOM,\n\n"}}};

const CT_LIB={promo:'Promotion', relance:'Relance de facture',
              merci:'Remerciement', libre:'Message libre'};

const ctMail=v=>/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(String(v||'').trim());

/* Ce que le patron a mis dans Réglages : sa signature, son adresse, et par où
   il veut que le message s'ouvre. Réglages vit dans le même navigateur, donc
   on le relit à chaque fois plutôt que de le figer au chargement. */
function ctReg(){
  try{ const r=JSON.parse(localStorage.getItem('reglages-v1')||'null');
    return (r&&typeof r==='object')?r:{}; }catch(e){ return {}; }
}

/* La signature : ce que le patron a écrit dans Réglages remplace le
   « Perfumes Trade » des modèles, et son adresse et son téléphone suivent. */
function ctSigne(txt){
  const r=ctReg();
  const nom=String(r.signature||'').trim();
  let bas=nom||'Perfumes Trade';
  const co=[String(r.monMail||'').trim(), String(r.monTel||'').trim()].filter(Boolean);
  if(co.length) bas+='\n'+co.join(' · ');
  return String(txt).replace(/Perfumes Trade$/, bas);
}

/* Où s'ouvre le message. « mailto: » passe par le logiciel de mail du poste ;
   ceux qui lisent leur courrier dans Gmail ou Outlook.com ne verraient rien
   s'ouvrir — d'où le choix dans Réglages. */
function ctLienMail(dest,obj,txt){
  const b=ctReg().boite||'defaut';
  const d=encodeURIComponent(dest), o=encodeURIComponent(obj), c=encodeURIComponent(txt);
  if(b==='gmail')
    return 'https://mail.google.com/mail/?view=cm&fs=1&to='+d+'&su='+o+'&body='+c;
  if(b==='outlook')
    return 'https://outlook.live.com/mail/0/deeplink/compose?to='+d+'&subject='+o+'&body='+c;
  return 'mailto:'+d+'?subject='+o+'&body='+c;
}

/* Le numéro tel qu'il part chez WhatsApp : que des chiffres, indicatif compris. */
function ctNum(v){
  let d=String(v||'').replace(/\D/g,'');
  if(!d) return '';
  if(d.length===10) d='1'+d;                 /* numéro américain sans indicatif */
  if(d.length===11 && d[0]==='1') return d;
  return (d.length>=8 && d.length<=15) ? d : '';
}

let CT=null;
function ctFenetre(){
  let ov=document.getElementById('ctov');
  if(ov) return ov;
  ov=document.createElement('div'); ov.className='ov'; ov.id='ctov';
  ov.innerHTML=`<div class="mod" style="max-width:600px;max-height:88vh;display:flex;flex-direction:column">
    <div class="mh"><h2 id="ct-titre">Écrire</h2><button class="x" id="ct-x">&times;</button></div>
    <div class="mb" style="overflow:auto;flex:1;min-height:0">
      <div class="ctco">
        <div class="ctf"><label for="ct-mail">Email</label>
          <input id="ct-mail" autocomplete="off" placeholder="pas encore renseigné"></div>
        <div class="ctf"><label for="ct-tel">Téléphone / WhatsApp</label>
          <input id="ct-tel" autocomplete="off" placeholder="+1 305 555 0100"></div>
      </div>
      <p class="ctaide" id="ct-corrige">Une adresse ou un numéro corrigé ici est enregistré sur la fiche.</p>
      <div class="ctch" id="ct-choix"></div>
      <div class="ctf" style="margin-top:14px"><label for="ct-obj">Objet (pour l'email)</label>
        <input id="ct-obj" autocomplete="off"></div>
      <div class="ctf" style="margin-top:12px"><label for="ct-txt">Message</label>
        <textarea id="ct-txt" rows="9"></textarea></div>
      <p class="ctaide" id="ct-note"></p>
    </div>
    <div class="mf" style="flex:none"><span class="msg" id="ct-msg"></span>
      <button class="btn" id="ct-non">Fermer</button>
      <button class="btn" id="ct-wa">Ouvrir WhatsApp</button>
      <button class="btn pri" id="ct-em">Ouvrir l'email</button></div>
  </div>`;
  document.body.appendChild(ov);
  document.getElementById('ct-x').onclick=()=>ov.classList.remove('on');
  document.getElementById('ct-non').onclick=()=>ov.classList.remove('on');
  ov.addEventListener('click',e=>{ if(e.target===ov) ov.classList.remove('on'); });

  document.getElementById('ct-choix').addEventListener('click',e=>{
    const b=e.target.closest('button[data-m]'); if(!b) return;
    ctModele(b.dataset.m);
  });
  document.getElementById('ct-em').onclick=()=>ctOuvre('email');
  document.getElementById('ct-wa').onclick=()=>ctOuvre('whatsapp');
  return ov;
}

function ctModele(m){
  CT.modele=m;
  [...document.querySelectorAll('#ct-choix button[data-m]')]
    .forEach(b=>b.classList.toggle('on', b.dataset.m===m));
  const L=(typeof LANG!=='undefined' && CT_MODELES[LANG]) ? LANG : 'fr';
  const t=CT_MODELES[L][m];
  document.getElementById('ct-obj').value=t.o;
  document.getElementById('ct-txt').value=ctSigne(t.t.replace(/NOM/g, CT.nom||''));
}

function ctDitMsg(t,c){
  const e=document.getElementById('ct-msg');
  e.textContent=t; e.className='msg '+(c||'err');
  if(t) setTimeout(()=>{ if(e.textContent===t){ e.textContent=''; } },4000);
}

function ctOuvre(par){
  const mail=document.getElementById('ct-mail').value.trim();
  const tel =document.getElementById('ct-tel').value.trim();
  const obj =document.getElementById('ct-obj').value;
  const txt =document.getElementById('ct-txt').value;
  if(!String(txt).trim()) return ctDitMsg('Le message est vide.');
  if(CT.onSave) { try{ CT.onSave(mail,tel); }catch(e){} }
  let url;
  if(par==='email'){
    if(!ctMail(mail)) return ctDitMsg("L'adresse email n'est pas valable — corrige-la ci-dessus.");
    url=ctLienMail(mail,obj,txt);
  } else {
    const n=ctNum(tel);
    if(!n) return ctDitMsg("Le numéro n'est pas lisible. Écris-le avec l'indicatif, par exemple +1 305 555 0100.");
    url='https://wa.me/'+n+'?text='+encodeURIComponent(txt);
  }
  const a=document.createElement('a');
  a.href=url; a.target='_blank'; a.rel='noopener';
  document.body.appendChild(a); a.click(); a.remove();
  if(typeof jlogContact==='function')
    jlogContact(CT.nom, par, CT_LIB[CT.modele]||CT.modele);
  ctDitMsg(par==='email' ? 'Mail ouvert — à toi d\'appuyer sur Envoyer.'
                         : 'WhatsApp ouvert — à toi d\'appuyer sur Envoyer.', 'ok');
}

/* Le point d'entrée. `onSave(email,tel)` sert à recoller les coordonnées
   corrigées sur la fiche d'origine — chaque rubrique sait où les ranger. */
function contacte(o){
  CT={nom:o.nom||'', modele:o.modele||'promo', onSave:o.onSave||null};
  const ov=ctFenetre();
  document.getElementById('ct-titre').textContent='Écrire à '+(o.nom||'');
  document.getElementById('ct-mail').value=o.email||'';
  document.getElementById('ct-tel').value=o.tel||'';
  const mods=o.modeles||['promo','relance','merci','libre'];
  document.getElementById('ct-choix').innerHTML=mods.map(m=>
    `<button class="ctb" data-m="${m}">${CT_LIB[m]||m}</button>`).join('');
  const OU={defaut:'ton logiciel de mail', gmail:'Gmail', outlook:'Outlook.com'};
  document.getElementById('ct-note').textContent=
    "Perfumes Trade prépare le message et ouvre "+(OU[ctReg().boite||'defaut']||'ton mail')
   +" ou WhatsApp avec le texte dedans. C'est toi qui appuies sur Envoyer, une personne à la fois. "
   +"Ta signature et le choix de la messagerie se règlent dans Réglages. "
   +"L'envoi à toute une liste d'un coup demandera le serveur.";
  document.getElementById('ct-msg').textContent='';
  ctModele(CT.modele);
  ov.classList.add('on');
  setTimeout(()=>document.getElementById('ct-txt').focus(),80);
}
"""

CSS = """
.ctco{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:13px}
.ctf{display:flex;flex-direction:column;gap:5px}
.ctf label{font-family:Inter,sans-serif;font-size:10px;letter-spacing:.11em;text-transform:uppercase;
 color:var(--ink-3);font-weight:600}
.ctf input,.ctf textarea{padding:10px 12px;font-family:inherit;font-size:14px;
 border:1px solid var(--line);border-radius:8px;background:var(--surface);color:var(--ink)}
.ctf textarea{resize:vertical;line-height:1.6}
.ctaide{font-size:12px;color:var(--ink-3);line-height:1.55;margin:8px 0 0}
.ctch{display:flex;flex-wrap:wrap;gap:7px;margin-top:16px}
.ctb{padding:7px 13px;font-family:inherit;font-size:13px;border:1px solid var(--line);
 border-radius:20px;background:var(--surface);color:var(--ink-2);cursor:pointer}
.ctb:hover{border-color:var(--iris);color:var(--iris)}
.ctb.on{background:var(--iris);border-color:var(--iris);color:#fff;font-weight:600}
.ecr{background:none;border:0;padding:4px 7px;font-family:inherit;font-size:12.5px;
 color:var(--ink-3);text-decoration:underline;cursor:pointer;border-radius:5px}
.ecr:hover{color:var(--iris)}
"""
