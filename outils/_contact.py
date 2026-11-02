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

/* Un seul email à plusieurs personnes : les adresses partent en COPIE CACHÉE.
   C'est une offre commerciale — chaque client ne doit pas voir à qui d'autre
   elle est envoyée, ni récupérer le carnet d'adresses de la maison. */
function ctLienMailGroupe(dests,obj,txt){
  const b=ctReg().boite||'defaut';
  const cc=encodeURIComponent(dests.join(',')), o=encodeURIComponent(obj), c=encodeURIComponent(txt);
  if(b==='gmail')
    return 'https://mail.google.com/mail/?view=cm&fs=1&bcc='+cc+'&su='+o+'&body='+c;
  if(b==='outlook')
    return 'https://outlook.live.com/mail/0/deeplink/compose?bcc='+cc+'&subject='+o+'&body='+c;
  return 'mailto:?bcc='+cc+'&subject='+o+'&body='+c;
}

/* Le même texte, mais sans prénom : dans un envoi groupé, NOM ne veut plus
   rien dire. On l'enlève et on recolle la ponctuation (« Bonjour NOM, » devient
   « Bonjour, »), plutôt que d'envoyer « Bonjour , » à trente clients. */
function ctSansNom(txt){
  return String(txt).replace(/NOM/g,'').replace(/[ \t]+([,;:!?])/g,'$1').replace(/[ \t]{2,}/g,' ');
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
/* ============ ÉCRIRE À PLUSIEURS ============
   Sam coche ses clients VIP et veut leur passer la même offre. Deux façons,
   et il faut dire honnêtement ce que chacune vaut :

   — UN SEUL EMAIL, tout le monde en copie cachée. Un clic, mais pas de prénom.
   — UN PAR UN, avec le prénom, par email ou par WhatsApp. WhatsApp n'a pas
     d'autre voie : il n'existe pas de lien qui ouvre trente conversations.

   Rien ne part tout seul, ici non plus : l'outil ouvre les messages, c'est la
   personne qui appuie sur Envoyer. Les envois faits sont cochés au fur et à
   mesure pour qu'on sache où on en est si on s'interrompt. */
let CTG=null;
function ctgFenetre(){
  let ov=document.getElementById('ctgov');
  if(ov) return ov;
  ov=document.createElement('div'); ov.className='ov'; ov.id='ctgov';
  ov.innerHTML=`<div class="mod" style="max-width:720px;max-height:90vh;display:flex;flex-direction:column">
    <div class="mh"><h2 id="ctg-titre">Écrire à plusieurs</h2><button class="x" id="ctg-x">&times;</button></div>
    <div class="mb" style="overflow:auto;flex:1;min-height:0">
      <div class="ctch" id="ctg-choix"></div>
      <div class="ctf" style="margin-top:14px"><label for="ctg-obj">Objet (pour l'email)</label>
        <input id="ctg-obj" autocomplete="off"></div>
      <div class="ctf" style="margin-top:12px"><label for="ctg-txt">Message</label>
        <textarea id="ctg-txt" rows="8"></textarea></div>
      <div class="ctf" id="ctg-offre" style="margin-top:12px;display:none"><label for="ctg-q">Ajouter un parfum à l'offre (avec son prix)</label>
        <input id="ctg-q" autocomplete="off" placeholder="Tape une marque ou un nom, puis clique sur le parfum">
        <div id="ctg-res"></div>
        <div class="ctgfic" id="ctg-fic">
          <span>Ou prépare tout d'un coup dans Excel :</span>
          <button class="ctbs" id="ctg-mod" type="button">1. Télécharger le modèle d'offre (Excel)</button>
          <button class="ctbs" id="ctg-imp" type="button">2. Importer mon offre remplie</button>
          <input type="file" id="ctg-file" style="display:none"></div></div>
      <p class="ctaide">NOM est remplacé par le nom du client dans les envois un par un.
        Dans l'email unique, il n'y a pas de prénom : NOM disparaît.</p>
      <div class="ctgl" id="ctg-liste"></div>
      <p class="ctaide" id="ctg-note"></p>
    </div>
    <div class="mf" style="flex:none"><span class="msg" id="ctg-msg"></span>
      <button class="btn" id="ctg-non">Fermer</button>
      <button class="btn" id="ctg-cop" title="Copie tous les numéros, un par ligne">Copier les numéros</button>
      <button class="btn" id="ctg-vcf" title="Un fichier de contacts à importer sur le téléphone, pour créer la liste de diffusion WhatsApp">Contacts WhatsApp (.vcf)</button>
      <button class="btn pri" id="ctg-un">Email à tous</button></div>
  </div>`;
  document.body.appendChild(ov);
  const ferme=()=>ov.classList.remove('on');
  document.getElementById('ctg-x').onclick=ferme;
  document.getElementById('ctg-non').onclick=ferme;
  ov.addEventListener('click',e=>{ if(e.target===ov) ferme(); });
  document.getElementById('ctg-choix').addEventListener('click',e=>{
    const b=e.target.closest('button[data-m]'); if(b) ctgModele(b.dataset.m); });
  document.getElementById('ctg-un').onclick=ctgTous;
  document.getElementById('ctg-vcf').onclick=ctgVcf;
  document.getElementById('ctg-note').addEventListener('click',e=>{ if(e.target.closest('button[data-restaure]')) ctgRestaure(); });
  document.getElementById('ctg-cop').onclick=ctgCopie;
  document.getElementById('ctg-q').addEventListener('input',ctgCherche);
  document.getElementById('ctg-mod').onclick=()=>{ if(CTG.modeleOffre) CTG.modeleOffre(); };
  document.getElementById('ctg-imp').onclick=()=>document.getElementById('ctg-file').click();
  document.getElementById('ctg-file').addEventListener('change',async e=>{
    const f=e.target.files&&e.target.files[0]; e.target.value=''; if(!f||!CTG.importeOffre) return;
    if(/\.(numbers|pages|pdf|docx?|png|jpe?g)$/i.test(f.name)) return ctgDitMsg("Ce format n'est pas lisible ici : enregistre le fichier en Excel (.xlsx) ou en CSV, puis importe-le.");
    try{ const r=await CTG.importeOffre(f);
      if(!r||!r.lignes.length) return ctgDitMsg(r&&r.raison?r.raison:"Aucune ligne cochée dans le fichier : mets un x dans la colonne OFFRE.");
      ctgInsere(r.lignes);
      ctgDitMsg(r.lignes.length+' parfum'+(r.lignes.length>1?'s':'')+' ajouté'+(r.lignes.length>1?'s':'')+' à l\'offre'+(r.ignorees?' — '+r.ignorees+' ignoré'+(r.ignorees>1?'s':'')+' (sans prix ou parfum inconnu)':'')+'.','ok');
    }catch(err){ ctgDitMsg("Je n'ai pas pu lire ce fichier : "+((err&&err.message)||'format inconnu')); } });
  document.getElementById('ctg-res').addEventListener('click',e=>{
    const b=e.target.closest('button[data-ligne]'); if(b) ctgAjoute(b.dataset.ligne); });
  document.getElementById('ctg-liste').addEventListener('click',e=>{
    const x=e.target.closest('button[data-stop]'); if(x){ ctgStop(+x.dataset.stop); return; }
    const b=e.target.closest('button[data-par]'); if(b) ctgUn(+b.dataset.i, b.dataset.par); });
  return ov;
}

function ctgModele(m){
  CTG.modele=m;
  [...document.querySelectorAll('#ctg-choix button[data-m]')]
    .forEach(b=>b.classList.toggle('on', b.dataset.m===m));
  const L=(typeof LANG!=='undefined' && CT_MODELES[LANG]) ? LANG : 'fr';
  const t=CT_MODELES[L][m];
  document.getElementById('ctg-obj').value=t.o;
  document.getElementById('ctg-txt').value=ctSigne(t.t)+(CTG.pied?'\n\n'+CT_STOP[L]:'');
}
/* le pied d'une liste de diffusion : chacun doit pouvoir se retirer (la loi l'exige pour une offre commerciale) */
const CT_STOP={fr:"Pour ne plus recevoir nos offres, répondez STOP.", en:"To stop receiving our offers, reply STOP.", es:"Para no recibir más ofertas, responda STOP."};

function ctgDitMsg(t,c){
  const e=document.getElementById('ctg-msg');
  e.textContent=t; e.className='msg '+(c||'err');
  if(t) setTimeout(()=>{ if(e.textContent===t) e.textContent=''; },4000);
}

function ctgPeint(){
  const L=CTG.liste;
  document.getElementById('ctg-titre').textContent=CTG.titre+' ('+L.length+')';
  const nMail=L.filter(p=>ctMail(p.email)).length, nTel=L.filter(p=>ctNum(p.tel)).length;
  const faits=L.filter(p=>p.fait).length;
  document.getElementById('ctg-liste').innerHTML=
    `<div class="ctgt">${L.length} client${L.length>1?'s':''} sélectionné${L.length>1?'s':''}`
    + (faits?` · <b>${faits} envoi${faits>1?'s':''} ouvert${faits>1?'s':''}</b>`:'')
    + `</div>` + L.map((p,i)=>{
      const m=ctMail(p.email), n=ctNum(p.tel);
      return `<div class="ctgr${p.fait?' ok':''}">
        <span class="ctgn" data-nolang>${esc(p.nom)}</span>
        <span class="ctgc">${m?esc(p.email):'<i>pas d\'email</i>'}${n?'':' · <i>pas de numéro</i>'}</span>
        <span class="ctga">
          <button class="ctbs" data-par="email" data-i="${i}"${m?'':' disabled'}>Email</button>
          <button class="ctbs" data-par="whatsapp" data-i="${i}"${n?'':' disabled'}>WhatsApp</button>
          ${CTG.onStop?`<button class="ctbs" data-stop="${i}" title="Ne plus jamais lui envoyer d'offres">Désinscrire</button>`:''}</span></div>`;
    }).join('');
  const sans=L.length-nMail;
  const nLots=Math.ceil(nMail/CTG_LOT);
  document.getElementById('ctg-note').innerHTML =
    `L'email part vers <b>${nMail}</b> adresse${nMail>1?'s':''}, en copie cachée`
    + (nLots>1?`, en <b>${nLots} lots de ${CTG_LOT}</b> (un lot par clic : au-delà, les messageries refusent le lien)`:'')
    + (sans?` — <b>${sans}</b> client${sans>1?'s n\'ont':' n\'a'} pas d'email et ne recevra${sans>1?'ient':''} rien.`:'.')
    + ` ${nTel} ont un numéro pour WhatsApp. Rien ne part tout seul : l'outil ouvre le message, c'est toi qui appuies sur Envoyer.`
    + (CTG.doublons?` ${CTG.doublons} doublon${CTG.doublons>1?'s':''} ignoré${CTG.doublons>1?'s':''} (même adresse ou même numéro).`:'')
    + (CTG.desinscrits?` <button class="ecr" data-restaure="1">${CTG.desinscrits} désinscrit${CTG.desinscrits>1?'s':''} (jamais contactés) — les remettre</button>`:'');
  const b=document.getElementById('ctg-un');
  const pris=Math.min(CTG.lot||0,nLots);
  b.disabled=!nMail;
  b.textContent= nLots<=1 ? 'Email à tous ('+nMail+')' : (pris>=nLots ? 'Tous les lots sont ouverts — recommencer' : 'Email : lot '+(pris+1)+'/'+nLots+' ('+Math.min(CTG_LOT,nMail-pris*CTG_LOT)+')');
  document.getElementById('ctg-vcf').disabled=!nTel; document.getElementById('ctg-cop').disabled=!nTel;
}

function ctgLance(url){
  const a=document.createElement('a'); a.href=url; a.target='_blank'; a.rel='noopener';
  document.body.appendChild(a); a.click(); a.remove();
}

const CTG_LOT=40;
function ctgTous(){
  const obj=document.getElementById('ctg-obj').value;
  const txt=ctSansNom(document.getElementById('ctg-txt').value);
  if(!String(txt).trim()) return ctgDitMsg('Le message est vide.');
  const avec=CTG.liste.filter(p=>ctMail(p.email));
  if(!avec.length) return ctgDitMsg("Aucun des clients sélectionnés n'a d'adresse email.");
  const nLots=Math.ceil(avec.length/CTG_LOT);
  if((CTG.lot||0)>=nLots){ CTG.lot=0; avec.forEach(p=>{ p.fait=false; }); }
  const lot=CTG.lot||0, part=avec.slice(lot*CTG_LOT,(lot+1)*CTG_LOT);
  ctgLance(ctLienMailGroupe(part.map(p=>p.email.trim()),obj,txt));
  part.forEach(p=>{ p.fait=true; });
  CTG.lot=lot+1;
  if(typeof jlogContact==='function')
    part.forEach(p=>jlogContact(p.nom,'email',(CT_LIB[CTG.modele]||CTG.modele)+' (liste de diffusion)'));
  ctgPeint();
  ctgDitMsg('Mail ouvert'+(nLots>1?' (lot '+(lot+1)+'/'+nLots+')':'')+' avec '+part.length+' destinataire'+(part.length>1?'s':'')+' en copie cachée — à toi d\'appuyer sur Envoyer.','ok');
}

/* WhatsApp n'a aucun lien qui écrit à 200 personnes : la voie propre est la « liste de diffusion »
   de WhatsApp Business, qui se crée sur le téléphone à partir de CONTACTS. On donne donc le
   fichier de contacts (les gens doivent avoir le numéro de Sam enregistré pour recevoir). */
function ctgVcf(){
  const L=CTG.liste.filter(p=>ctNum(p.tel));
  if(!L.length) return ctgDitMsg("Aucun numéro lisible dans cette liste.");
  /* 9 oct. 2026 (Igal : « ça télécharge un .vcf mais ça ne marche pas ») : une fiche vCard 3.0
     DOIT porter une ligne N (nom structuré) en plus de FN — Contacts du Mac et l'iPhone
     refusent ou ignorent celles qui n'en ont pas. Un contact sans nom prend son numéro. */
  const v=L.map(p=>{ const nom=String(p.nom||'').replace(/[\r\n,;\\]/g,' ').trim()||('+'+ctNum(p.tel));
    return 'BEGIN:VCARD\r\nVERSION:3.0\r\nN:;'+nom+';;;\r\nFN:'+nom+'\r\nTEL;TYPE=CELL:+'+ctNum(p.tel)+'\r\nEND:VCARD'; }).join('\r\n')+'\r\n';
  const a=document.createElement('a'); a.href=URL.createObjectURL(new Blob([v],{type:'text/vcard;charset=utf-8'}));
  a.download='contacts-whatsapp.vcf'; document.body.appendChild(a); a.click(); a.remove();
  ctgDitMsg(L.length+' contacts téléchargés : importe le fichier sur le téléphone, puis crée la liste de diffusion dans WhatsApp Business.','ok');
}
async function ctgCopie(){
  const t=CTG.liste.map(p=>ctNum(p.tel)).filter(Boolean).map(n=>'+'+n).join('\n');
  if(!t) return ctgDitMsg("Aucun numéro lisible dans cette liste.");
  try{ await navigator.clipboard.writeText(t); }catch(e){ const x=document.createElement('textarea'); x.value=t; document.body.appendChild(x); x.select(); document.execCommand('copy'); x.remove(); }
  ctgDitMsg(t.split('\n').length+' numéros copiés.','ok');
}
/* se désinscrire : le client ne reçoit plus jamais d'offre, d'où qu'on lance la liste */
function ctgStop(i){
  const p=CTG.liste[i]; if(!p||!CTG.onStop) return;
  if(!confirm(p.nom+' ne recevra plus jamais d\'offres de cette liste. Continuer ?')) return;
  CTG.onStop(p.nom); CTG.liste.splice(i,1); CTG.desinscrits=(CTG.desinscrits||0)+1; ctgPeint();
}
function ctgRestaure(){
  if(!CTG.onRestore) return;
  const f=CTG.onRestore(); if(f) contacteGroupe(f);
}
function ctgCherche(){
  const q=document.getElementById('ctg-q').value, R=CTG.catalogue?CTG.catalogue(q):[];
  CTG.res=R;
  document.getElementById('ctg-res').innerHTML=R.map((r,i)=>`<button class="ctb" data-ligne="${i}" data-nolang>${esc(r.lib)} — ${esc(r.prix)}</button>`).join('');
}
function ctgInsere(lignes){
  const t=document.getElementById('ctg-txt'), bloc=lignes.map(l=>'• '+l).join('\n');
  const pos=Math.min(t.selectionStart==null?t.value.length:t.selectionStart,t.value.length);
  t.value=t.value.slice(0,pos)+(pos&&t.value[pos-1]!=='\n'?'\n':'')+bloc+'\n'+t.value.slice(pos);
  t.selectionStart=t.selectionEnd=pos+bloc.length+1;
}
function ctgAjoute(i){
  const r=(CTG.res||[])[+i]; if(!r) return;
  const t=document.getElementById('ctg-txt'), ligne='• '+r.lib+' — '+r.prix;
  const pos=Math.min(t.selectionStart==null?t.value.length:t.selectionStart,t.value.length);
  t.value=t.value.slice(0,pos)+(pos&&t.value[pos-1]!=='\n'?'\n':'')+ligne+'\n'+t.value.slice(pos);
  t.selectionStart=t.selectionEnd=pos+ligne.length+1;
  ctgDitMsg('Ajouté : '+r.lib,'ok');
}

function ctgUn(i,par){
  const p=CTG.liste[i]; if(!p) return;
  const obj=document.getElementById('ctg-obj').value;
  const txt=ctSigne(document.getElementById('ctg-txt').value).replace(/NOM/g,p.nom);
  if(!String(txt).trim()) return ctgDitMsg('Le message est vide.');
  if(par==='email'){
    if(!ctMail(p.email)) return ctgDitMsg("Ce client n'a pas d'adresse email valable.");
    ctgLance(ctLienMail(p.email.trim(),obj,txt));
  } else {
    const n=ctNum(p.tel);
    if(!n) return ctgDitMsg("Ce client n'a pas de numéro lisible.");
    ctgLance('https://wa.me/'+n+'?text='+encodeURIComponent(txt));
  }
  p.fait=true;
  if(typeof jlogContact==='function') jlogContact(p.nom,par,CT_LIB[CTG.modele]||CTG.modele);
  ctgPeint();
}

/* Le point d'entrée : `liste` = [{nom,email,tel}, …]. */
function contacteGroupe(o){
  /* une même adresse (ou un même numéro) ne reçoit l'offre qu'une fois, même sous deux noms
     (le site garde « redjiea8 » ET « Auguste Redjie » pour la même personne) */
  const L0=(o.liste||[]).map(p=>({nom:p.nom||'', email:p.email||'', tel:p.tel||'', fait:false}));
  const parMail={}, parTel={}, L=[]; let doublons=0;
  L0.forEach(p=>{ const m=ctMail(p.email)?p.email.trim().toLowerCase():'', n=ctNum(p.tel);
    const deja=(m&&parMail[m])||(n&&parTel[n]);
    if(deja){ doublons++; if(!ctMail(deja.email)&&m) deja.email=p.email; if(!ctNum(deja.tel)&&n) deja.tel=p.tel; if(m) parMail[m]=deja; if(n) parTel[n]=deja; return; }
    if(m) parMail[m]=p; if(n) parTel[n]=p; L.push(p); });
  if(!L.length) return;
  CTG={liste:L, modele:o.modele||'promo', pied:!!o.pied, onStop:o.onStop||null, onRestore:o.onRestore||null, desinscrits:o.desinscrits||0, catalogue:o.catalogue||null, modeleOffre:o.modeleOffre||null, importeOffre:o.importeOffre||null, doublons, lot:0, res:[]};
  const ov=ctgFenetre();
  CTG.titre=o.titre||'Écrire à plusieurs';
  const mods=o.modeles||['promo','merci','libre'];
  document.getElementById('ctg-choix').innerHTML=
    mods.map(m=>`<button class="ctb" data-m="${m}">${CT_LIB[m]||m}</button>`).join('');
  document.getElementById('ctg-offre').style.display=CTG.catalogue?'':'none';
  document.getElementById('ctg-fic').style.display=(CTG.modeleOffre&&CTG.importeOffre)?'':'none';
  document.getElementById('ctg-q').value=''; document.getElementById('ctg-res').innerHTML='';
  ctgModele(CTG.modele);
  ctgPeint();
  ov.classList.add('on');
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
/* la liste des destinataires d'un envoi groupé */
.ctgt{font-family:Inter,sans-serif;font-size:11px;letter-spacing:.09em;text-transform:uppercase;
 color:var(--ink-3);font-weight:700;margin:18px 0 8px}
.ctgt b{color:var(--iris)}
.ctgr{display:flex;align-items:center;gap:10px;padding:8px 10px;border:1px solid var(--line-2);
 border-radius:8px;margin-bottom:6px;background:var(--surface)}
.ctgr.ok{border-color:var(--iris);background:var(--iris-soft)}
.ctgn{font-weight:700;font-size:13.5px;white-space:nowrap}
.ctgc{flex:1;font-size:12px;color:var(--ink-3);overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.ctgc i{font-style:normal;color:var(--ink-3);opacity:.8}
.ctga{display:flex;gap:6px;flex:none}
.ctbs{padding:5px 10px;font-family:inherit;font-size:12px;border:1px solid var(--line);
 border-radius:7px;background:var(--surface);color:var(--ink-2);cursor:pointer;white-space:nowrap}
.ctbs:hover:not([disabled]){border-color:var(--iris);color:var(--iris)}
.ctbs[disabled]{opacity:.35;cursor:default}
#ctg-res{display:flex;flex-wrap:wrap;gap:6px;margin-top:8px}
.ctgfic{display:flex;flex-wrap:wrap;align-items:center;gap:8px;margin-top:12px;font-size:12.5px;color:var(--ink-3)}
"""
