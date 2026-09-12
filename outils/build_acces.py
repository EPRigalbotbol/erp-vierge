# -*- coding: utf-8 -*-
"""La rubrique Accès : les comptes, leurs rôles, et ce que chaque rôle voit.

Réservée au patron. Les autres y arrivent sur un mur poli qui explique pourquoi.
"""
import os
from build_crm import coquille

CSS = """
.bandeau{background:var(--iris-soft);border-left:3px solid var(--iris);border-radius:0 9px 9px 0;
 padding:14px 17px;font-size:13.5px;color:var(--ink-2);line-height:1.62;margin:0 0 24px;max-width:88ch}
.bandeau b{color:var(--ink)}
.bandeau code{font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:11.5px;
 background:var(--surface);border:1px solid var(--line);border-radius:4px;padding:1px 5px}
.mur{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:34px 32px;
 max-width:62ch;margin:40px auto;text-align:center}
.mur h2{margin:0 0 10px;font-size:20px;font-weight:700;letter-spacing:-.015em}
.mur p{margin:0;color:var(--ink-2);font-size:14.5px;line-height:1.65}

.tw{border:1px solid var(--line);border-radius:10px;overflow:hidden;background:var(--surface);margin-bottom:26px}
table.t{width:100%;border-collapse:collapse;font-size:13.5px}
.t th{background:var(--surface-2);color:var(--ink-3);font-size:9.5px;letter-spacing:.11em;
 text-transform:uppercase;text-align:left;padding:10px 13px;border-bottom:1px solid var(--line);
 font-weight:700;white-space:nowrap}
.t td{padding:12px 13px;border-bottom:1px solid var(--line-2);vertical-align:middle;color:var(--ink-2)}
.t tr:last-child td{border-bottom:0}
.t tr.off td{opacity:.5}
.qui b{display:block;color:var(--ink);font-size:14.5px;font-weight:600;line-height:1.3}
.qui span{display:block;font-size:11.5px;color:var(--ink-3);font-family:"IBM Plex Mono",monospace}
.rl{display:inline-flex;align-items:center;gap:6px;padding:4px 10px;border-radius:20px;
 font-size:11.5px;font-weight:600;white-space:nowrap;background:var(--surface-2);color:var(--ink-2)}
.rl::before{content:"";width:5px;height:5px;border-radius:50%;background:currentColor}
.rl.patron{background:var(--iris-soft);color:var(--iris)}
.rl.commercial{background:var(--good-soft);color:var(--good)}
.rl.entrepot{background:var(--warn-soft);color:var(--warn)}
.rl.comptable{background:var(--surface-2);color:var(--ink-2)}
.qd{font-family:Inter,sans-serif;font-size:12.5px;color:var(--ink-3);white-space:nowrap}
.act{text-align:right;white-space:nowrap}
.act button{background:none;border:0;padding:4px 7px;font-family:inherit;font-size:12.5px;
 color:var(--ink-3);text-decoration:underline;cursor:pointer;border-radius:5px}
.act button:hover{color:var(--iris)}
.act button.dg:hover{color:var(--crit)}
.moi{font-size:11px;color:var(--ink-3);font-weight:600;letter-spacing:.06em;text-transform:uppercase}

section{display:flex;flex-direction:column;gap:15px;margin-bottom:34px}
.shead{border-bottom:1px solid var(--line);padding-bottom:10px;display:flex;
 align-items:baseline;gap:12px;flex-wrap:wrap}
.count{font-size:12.5px;color:var(--ink-3)}
.sdesc{font-size:13.5px;color:var(--ink-2);max-width:76ch;margin:0;line-height:1.6}

/* La grille des rôles : les droits en lignes, les rôles en colonnes.
   Quatre cartes côte à côte répétaient sept fois la même liste ; en tableau,
   on lit une ligne et on voit d'un coup qui a le droit et qui ne l'a pas. */
.dw{border:1px solid var(--line);border-radius:10px;background:var(--surface);overflow-x:auto}
table.dr{border-collapse:collapse;font-size:13.5px;min-width:100%}
.dr th,.dr td{padding:11px 15px;text-align:center;border-bottom:1px solid var(--line-2)}
.dr thead th{background:var(--surface-2);border-bottom:1px solid var(--line);
 vertical-align:bottom;padding:13px 15px;min-width:132px}
.dr thead th b{display:block;font-size:14px;font-weight:700;color:var(--ink);letter-spacing:-.01em}
.dr thead th i{display:block;font-style:normal;font-size:11px;color:var(--ink-3);
 font-weight:400;margin-top:3px;line-height:1.35}
.dr .lab{text-align:left;color:var(--ink-2);white-space:nowrap;font-weight:500}
.dr thead th:first-child{min-width:210px;text-align:left}
.dr tbody tr:hover td{background:var(--surface-2)}
.dr tbody tr:hover td.lab{background:var(--surface-2)}
.oui{color:var(--good);font-weight:700}
.non{color:var(--line);font-weight:700}
/* une case cliquable doit se voir comme telle AVANT le clic : sinon on découvre
   qu'on pouvait cliquer en ayant déjà changé un droit par hasard */
.dr td.cli{padding:4px}
.dr td.cli button{width:38px;height:34px;border:1px solid transparent;border-radius:7px;
 background:none;font:inherit;font-size:15px;font-weight:700;color:inherit;cursor:pointer;
 transition:background .12s,border-color .12s}
.dr td.cli button:hover{background:var(--surface-2);border-color:var(--line)}
.dr td.cli button:focus-visible{outline:2px solid var(--iris);outline-offset:1px}
.cad{font-size:10px;letter-spacing:.08em;text-transform:uppercase;color:var(--ink-3);
 border:1px solid var(--line);border-radius:4px;padding:1px 5px;margin-left:7px;font-weight:600}
.dr tr.fin .modif{font-size:12px;color:var(--warn);font-weight:600;margin-right:8px}
.dr tr.dep td{border-top:1px solid var(--line);font-size:12.5px;color:var(--ink-2)}
.dr tr.dep td.lab,.dr tr.fin td.lab{color:var(--ink-3);font-weight:400}
.dr tr.fin td{border-bottom:0;padding-top:12px;padding-bottom:13px}
.dr tr.fin .fixe{font-size:12px;color:var(--ink-3)}
.dr tr.fin button{background:none;border:0;padding:2px 4px;font-family:inherit;font-size:12.5px;
 color:var(--ink-3);text-decoration:underline;cursor:pointer}
.dr tr.fin button:hover{color:var(--iris)}
.dr tr.fin button.dg:hover{color:var(--crit)}

.cases{display:grid;grid-template-columns:1fr;gap:2px;border:1px solid var(--line);
 border-radius:8px;padding:6px;background:var(--surface-2)}
.fld .cases label{display:flex;gap:10px;align-items:center;padding:8px 9px;border-radius:6px;
 font-family:inherit;font-size:13.5px;font-weight:400;letter-spacing:0;text-transform:none;
 text-align:left;color:var(--ink-2);cursor:pointer}
.fld .cases label:hover{background:var(--surface)}
.cases input{margin:0;flex:none;width:15px;height:15px;accent-color:var(--iris)}

.mf .btn{margin-left:0}
.fg2{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:14px}
.fld{display:flex;flex-direction:column;gap:5px}
.fld label{font-family:Inter,sans-serif;font-size:10px;letter-spacing:.11em;text-transform:uppercase;
 color:var(--ink-3);font-weight:600}
.fld input,.fld select{padding:10px 12px;font-family:inherit;font-size:14px;border:1px solid var(--line);
 border-radius:8px;background:var(--surface);color:var(--ink)}
.aidefld{font-size:12px;color:var(--ink-3);line-height:1.5;margin:6px 0 0}
.msg{font-size:13px;font-weight:600}
.opt{font-weight:400;color:var(--ink-3)}
.genr{display:flex;gap:8px;align-items:center;margin-top:10px;flex-wrap:wrap}
.genval{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:15px;letter-spacing:.5px;
  background:var(--bg-1);border:1px solid var(--tr);border-radius:8px;padding:7px 12px;
  color:var(--ink-1);user-select:all}
.coche{display:flex;gap:9px;align-items:flex-start;margin-top:16px;cursor:pointer;font-size:14px}
.coche input{margin:2px 0 0;flex:none}
.lgb{display:flex;gap:6px}
.lgb button{border:1px solid var(--tr);background:var(--bg-1);color:var(--ink-2);
  border-radius:8px;padding:6px 14px;font:inherit;font-size:13px;cursor:pointer}
.lgb button.on{background:var(--ink-1);color:var(--bg-0);border-color:var(--ink-1);font-weight:600}
.objl{border:1px solid var(--tr);border-radius:8px;padding:9px 12px;background:var(--bg-1);
  font-size:14px;color:var(--ink-1)}
#m-corps{width:100%;box-sizing:border-box;border:1px solid var(--tr);border-radius:8px;
  padding:10px 12px;font:inherit;font-size:13.5px;line-height:1.55;background:var(--bg-1);
  color:var(--ink-1);resize:vertical}
.msg.err{color:var(--crit)} .msg.ok{color:var(--good)}
"""

CORPS = """
<div class="bandeau" id="ban"></div>
<div id="tout" hidden>

  <section>
    <div class="shead"><h2>Les comptes</h2><span class="count" id="nb"></span>
      <button class="btn pri" id="add" style="margin-left:auto">+ Ouvrir un accès</button></div>
    <div class="tw"><table class="t">
      <thead><tr><th>Personne</th><th>Rôle</th><th>Dernière connexion</th><th>Ouvert le</th><th></th></tr></thead>
      <tbody id="tb"></tbody></table></div>
  </section>

  <section>
    <div class="shead"><h2>Les rôles</h2><span class="count" id="nbr"></span>
      <button class="btn pri" id="addr" style="margin-left:auto">+ Créer un rôle</button></div>
    <p class="sdesc">Un rôle, c'est une liste de droits avec un nom. Tu en crées autant que tu veux,
    et tu le choisis ensuite en ouvrant un accès. Les quatre rôles d'origine servent de repère et ne
    se modifient pas.</p>
    <div class="dw"><table class="dr" id="dr"></table></div>
  </section>

</div>

<div class="ov" id="fov">
 <div class="mod" style="max-width:560px">
  <div class="mh"><h2 id="ftitre">Ouvrir un accès</h2><button class="x" id="fx">&times;</button></div>
  <div class="mb">
   <div class="fg2">
     <div class="fld"><label for="f-nom">Nom de la personne</label><input id="f-nom" autocomplete="off"></div>
     <div class="fld"><label for="f-id">Identifiant</label><input id="f-id" autocomplete="off"></div>
   </div>
   <div class="fld"><label for="f-role">Rôle</label><select id="f-role"></select>
     <p class="aidefld" id="f-aide"></p></div>
   <div class="fld" id="f-mailbloc"><label for="f-mail">Son email <span class="opt">— facultatif</span></label>
     <input id="f-mail" type="email" autocomplete="off" placeholder="javier@exemple.com">
     <p class="aidefld">Sert à lui envoyer l'adresse du site et son identifiant, rien d'autre.
     Le mot de passe ne part jamais par email : donne-le de vive voix ou par SMS.</p></div>
   <div class="fg2">
     <div class="fld"><label for="f-m">Mot de passe</label><input id="f-m" type="password" autocomplete="new-password"></div>
     <div class="fld"><label for="f-m2">Répéter</label><input id="f-m2" type="password" autocomplete="new-password"></div>
   </div>
   <p class="aidefld">Six caractères minimum. <b>Il est provisoire</b> : la personne devra
   en choisir un autre à sa première connexion, et lui seul comptera ensuite.
   Personne ne pourra le relire, pas même toi — SAM n'en garde qu'une empreinte.</p>
   <div class="genr">
     <button class="btn" type="button" id="f-gen">Générer un mot de passe</button>
     <button class="btn" type="button" id="f-copie" hidden>Copier</button>
     <code class="genval" id="f-genval" hidden></code>
   </div>
   <label class="coche" id="f-envbloc"><input type="checkbox" id="f-env">
     <span>Envoyer l'accès par email à la personne</span></label>
   <p class="aidefld" id="f-envaide">Décoché, <b>rien ne part</b> : le compte est créé, c'est tout.
   Coché, tu relis le message dans ton logiciel de courrier avant de l'envoyer toi-même.</p>
  </div>
  <div class="mf"><span class="msg" id="fmsg"></span>
   <button class="btn" id="fc">Annuler</button>
   <button class="btn pri" id="fok">Ouvrir l'accès</button></div>
 </div>
</div>

<div class="ov" id="mov">
 <div class="mod" style="max-width:620px">
  <div class="mh"><h2>Envoyer l'accès</h2><button class="x" id="mx">&times;</button></div>
  <div class="mb">
   <p class="aidefld" style="margin:0 0 12px">À <b id="m-a"></b> — le message s'ouvrira dans ton
   logiciel de courrier, tu le relis et c'est toi qui l'envoies.</p>
   <div class="lgb" data-nolang>
     <button data-lg="fr">Français</button><button data-lg="en">English</button><button data-lg="es">Español</button>
   </div>
   <div class="fld" style="margin-top:12px"><label>Objet</label>
     <div class="objl" id="m-obj"></div></div>
   <div class="fld" style="margin-top:12px"><label for="m-corps">Message</label>
     <textarea id="m-corps" rows="12"></textarea></div>
   <p class="aidefld">Le mot de passe du compte est <b>provisoire</b> : la personne devra en
   choisir un autre dès sa première connexion, et lui seul comptera ensuite. Il ne reste
   donc rien d'utilisable dans sa boîte mail.<br>
   <b>Une ligne est à compléter</b> : le mot de passe du site, celui que le navigateur demande
   avant l'outil. L'ERP ne le connaît pas — il vit dans Coolify — alors écris-le toi-même
   ci-dessus, ou donne-le à l'équipe une fois pour toutes.</p>
  </div>
  <div class="mf"><span class="msg" id="mmsg"></span>
   <button class="btn" id="mcopie">Copier le texte</button>
   <button class="btn" id="mc">Fermer</button>
   <button class="btn pri" id="mok">Ouvrir mon email</button></div>
 </div>
</div>

<div class="ov" id="rov">
 <div class="mod" style="max-width:560px;max-height:86vh;display:flex;flex-direction:column">
  <div class="mh"><h2 id="rtitre">Créer un rôle</h2><button class="x" id="rx">&times;</button></div>
  <div class="mb" style="overflow:auto;flex:1;min-height:0">
   <div class="fld"><label for="r-lib">Nom du rôle</label>
     <input id="r-lib" autocomplete="off" placeholder="Boutique Perfume City"></div>
   <div class="fld" style="margin-top:14px"><label for="r-aide">En une phrase, ce qu'il fait</label>
     <input id="r-aide" autocomplete="off" placeholder="Compte le stock de la boutique et vend au comptoir"></div>
   <div class="fld" style="margin-top:16px"><label>Ce qu'il a le droit de faire</label>
     <div class="cases" id="r-cases"></div></div>
   <div class="fld" style="margin-top:16px"><label for="r-dep">Où il arrive en entrant</label>
     <select id="r-dep"></select>
     <p class="aidefld">La première page qu'il voit après s'être connecté. Choisis celle où il
     a quelque chose à faire — pas le Tableau de bord s'il ne voit pas les marges.</p></div>
  </div>
  <div class="mf" style="flex:none"><span class="msg" id="rmsg"></span>
   <button class="btn" id="rc">Annuler</button>
   <button class="btn pri" id="rok">Créer le rôle</button></div>
 </div>
</div>
"""

JS = r"""
const D=DROITS;
const dfr=iso=>{ if(!iso) return 'jamais'; const d=new Date(iso);
  return d.toLocaleDateString('fr-FR',{day:'2-digit',month:'2-digit',year:'2-digit'})
    +' à '+d.toLocaleTimeString('fr-FR',{hour:'2-digit',minute:'2-digit'}); };

function jlog(lib,ref,ap){
  const s=session(); const J=lit('crm-journal-v1',[]);
  J.push({t:new Date().toISOString(),u:s?s.nom:'?',act:'acces',lib,ref,av:null,ap:ap||null});
  ecrit('crm-journal-v1',J);
}

const libDep=v=>{ const t=DEPARTS.find(x=>x[0]===v); return t?t[1]:'Catalogue'; };

function dessineDroits(){
  const U=comptes(), K=Object.keys(ROLES);
  const n=Object.keys(rolesPerso()).length;
  $('nbr').textContent = n ? (n>1 ? n+' rôles à toi + les 4 d\'origine' : '1 rôle à toi + les 4 d\'origine')
                           : '4 rôles d\'origine';
  const combien=k=>{ const c=U.filter(u=>u.role===k).length;
    return c ? c+(c>1?' personnes':' personne') : 'aucun compte'; };
  const tete='<thead><tr><th></th>'+K.map(k=>
      `<th><b>${esc(ROLES[k].lib)}</b><i>${esc(combien(k))}</i></th>`).join('')+'</tr></thead>';
  /* Chaque case est un bouton : on clique sur le droit, on ne passe plus par une
     fenêtre. Deux exceptions, et elles ne sont pas décoratives :
       — sans le droit « accès », on ne touche à rien (on regarde) ;
       — la ligne « technique » est verrouillée pour tout le monde, y compris
         l'Admin : c'est elle qui fait tenir la hiérarchie des rôles. */
  const jePeux = peut('acces');
  const lignes=D.map(([d,lib])=>{
    const fige = DROITS_FIGES.indexOf(d)>=0;
    return `<tr><td class="lab">${esc(lib)}${fige?' <span class="cad" title="Ce droit ne se donne pas : il définit le rôle Admin.">verrouillé</span>':''}</td>`
      +K.map(k=>{
        const on=!!ROLES[k][d];
        if(fige||!jePeux) return `<td class="${on?'oui':'non'}">${on?'✓':'—'}</td>`;
        return `<td class="${on?'oui':'non'} cli"><button data-tog="${esc(k)}:${esc(d)}"
          title="${on?'Retirer':'Donner'} « ${esc(lib)} » au rôle ${esc(ROLES[k].lib)}">${on?'✓':'—'}</button></td>`;
      }).join('')
      +'</tr>';
  }).join('');
  const dep=`<tr class="dep"><td class="lab">Arrive sur, en entrant</td>`
    +K.map(k=>`<td>${esc(libDep(pageDeDepart(k)))}</td>`).join('')+'</tr>';
  const fin='<tr class="fin"><td class="lab"></td>'+K.map(k=> roleDOrigine(k)
      ? (ROLES[k].ajuste
          ? `<td><span class="modif">ajusté</span><button data-rraz="${esc(k)}">revenir à l'origine</button></td>`
          : '<td><span class="fixe">rôle d\'origine</span></td>')
      : `<td><button data-rmod="${esc(k)}">modifier</button>`
        +`<button class="dg" data-rsup="${esc(k)}">supprimer</button></td>`).join('')+'</tr>';
  $('dr').innerHTML=tete+'<tbody>'+lignes+dep+fin+'</tbody>';
}

/* ---------- fabriquer un rôle ---------- */
let REDIT=null;
function cle(lib){
  const b=String(lib).normalize('NFD').replace(/[\u0300-\u036f]/g,'')
    .toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'').slice(0,24);
  return b||('role-'+Date.now().toString(36));
}
function ouvreRole(k){
  REDIT=k||null;
  const r=k?ROLES[k]:{};
  $('rtitre').textContent = k?('Le rôle '+r.lib):'Créer un rôle';
  $('rok').textContent = k?'Enregistrer':'Créer le rôle';
  $('r-lib').value=k?r.lib:''; $('r-aide').value=k?(r.aide||''):'';
  $('r-cases').innerHTML=D.map(([d,lib])=>
    `<label><input type="checkbox" data-d="${d}" ${k&&r[d]?'checked':''}>${esc(lib)}</label>`).join('');
  $('r-dep').innerHTML=DEPARTS.map(([v,lib])=>`<option value="${v}">${esc(lib)}</option>`).join('');
  $('r-dep').value = k?pageDeDepart(k):'catalogue.html';
  $('rmsg').textContent='';
  $('rov').classList.add('on');
  setTimeout(()=>$('r-lib').focus(),60);
}
$('rx').onclick=$('rc').onclick=()=>$('rov').classList.remove('on');
$('rov').addEventListener('click',e=>{ if(e.target.id==='rov') $('rov').classList.remove('on'); });
$('addr').onclick=()=>ouvreRole(null);

$('dr').addEventListener('click',e=>{
  const b=e.target.closest('button'); if(!b) return;

  /* ---- un clic sur une case : on donne ou on retire le droit ---- */
  if(b.dataset.tog){
    if(!peut('acces')) return;
    const [k,d]=b.dataset.tog.split(':');
    const r=ROLES[k]; if(!r) return;
    const nouveau = r[d] ? 0 : 1;

    /* Le garde-fou qui compte : si on retire « accès » au dernier rôle qui
       l'a encore parmi les comptes actifs, plus personne ne peut rouvrir cette
       page — et on ne peut plus rendre le droit qu'on vient d'enlever. La porte
       se refermerait de l'intérieur, avec la clé restée dedans. */
    if(d==='acces' && !nouveau){
      const U=comptes().filter(u=>u.actif);
      const restants=U.filter(u=>u.role!==k && ROLES[u.role] && ROLES[u.role].acces).length;
      if(!restants) return alert(
        'Impossible : c\'est le dernier rôle qui peut ouvrir cette page.\n\n'
        +'En lui retirant « Ouvre et ferme les accès », plus personne ne pourrait '
        +'y revenir — pas même toi — et le droit serait perdu pour de bon.');
    }

    /* Puis : on ne se retire pas le droit sur SON PROPRE rôle. Le garde-fou
       ci-dessus ne couvre pas ce cas — il laisse passer la situation où
       quelqu'un d'autre garde le droit : la porte reste ouverte pour lui, mais
       pas pour soi. L'ordre compte : quand les deux raisons sont vraies en même
       temps, c'est la plus grave qui doit s'afficher — un droit perdu pour tout
       le monde et pour de bon pèse plus lourd qu'un onglet perdu pour soi. */
    if(!nouveau && DROITS_RETOUR.indexOf(d)>=0){
      const s=session();
      if(s && s.role===k) return refusSaborder(
        'Ce droit-là est sur TON rôle ('+(r.lib||k)+') : en le retirant, '
        +'tu fermes cette page pour toi le temps de relâcher le bouton.');
    }

    const P=rolesPerso();
    /* on part de ce que le rôle vaut À L'ÉCRAN, pas de la base : sinon un
       ajustement précédent serait effacé au clic suivant */
    const def={}; D.forEach(([x])=>{ def[x]=r[x]?1:0; });
    def[d]=nouveau; def.lib=r.lib; def.aide=r.aide;
    if(r.depart) def.depart=r.depart;
    P[k]=def; sauveRoles(P);
    const lib=(D.find(([x])=>x===d)||[,d])[1];
    jlog(nouveau?'droit donné':'droit retiré', k, null, lib+' — rôle '+r.lib);
    dessineDroits(); dessine();
    return;
  }

  /* ---- rendre à un rôle d'origine sa définition d'origine ---- */
  if(b.dataset.rraz){
    const k=b.dataset.rraz, r=ROLES[k];
    if(!peut('acces')) return;
    if(!confirm(`Remettre le rôle « ${r.lib} » tel qu'il était d'origine ?\n\n`
      +`Tous tes ajustements sur cette colonne seront perdus. `
      +`Les personnes qui ont ce rôle le gardent — ce sont leurs droits qui changent.`)) return;
    const P=rolesPerso(); delete P[k]; sauveRoles(P);
    jlog('rôle remis à l\'origine',k,r.lib);
    dessineDroits(); dessine();
    return;
  }

  if(b.dataset.rmod) return ouvreRole(b.dataset.rmod);
  if(b.dataset.rsup){
    const k=b.dataset.rsup, r=ROLES[k];
    const pris=comptes().filter(u=>u.role===k);
    if(pris.length) return alert(`Impossible : ${pris.map(u=>u.nom).join(', ')} `
      +`${pris.length>1?'ont':'a'} ce rôle. Change-leur d'abord le rôle, puis supprime celui-ci.`);
    if(!confirm(`Supprimer le rôle « ${r.lib} » ? Personne ne l'utilise, rien d'autre ne bouge.`)) return;
    const P=rolesPerso(); delete P[k]; sauveRoles(P);
    jlog('rôle supprimé',k,r.lib);
    dessineDroits(); dessine();
  }
});

$('rok').onclick=()=>{
  const dis=(t,c)=>{ $('rmsg').textContent=t; $('rmsg').className='msg '+(c||'err'); };
  const lib=$('r-lib').value.trim();
  if(lib.length<2) return dis('Donne un nom au rôle.');
  const P=rolesPerso();
  const k=REDIT||cle(lib);
  if(!REDIT && (ROLES_BASE[k]||P[k])) return dis('Un rôle porte déjà ce nom.');
  if(!REDIT && Object.values(ROLES).some(r=>r.lib.toLowerCase()===lib.toLowerCase()))
    return dis('Un rôle porte déjà ce nom.');
  const r={lib:lib.slice(0,28), aide:$('r-aide').value.trim().slice(0,120), depart:$('r-dep').value};
  [...$('r-cases').querySelectorAll('input[data-d]')].forEach(c=>{ r[c.dataset.d]=c.checked?1:0; });
  /* un rôle qui ne peut rien faire n'est pas un rôle, c'est un piège */
  if(!D.some(([d])=>r[d])) return dis('Coche au moins un droit, sinon la personne ne pourra rien faire.');
  P[k]=r; sauveRoles(P);
  jlog(REDIT?'rôle modifié':'rôle créé',k,lib+' — '+D.filter(([d])=>r[d]).map(([,l])=>l).join(', '));
  $('rov').classList.remove('on');
  dessineDroits(); dessine();
};

function dessine(){
  const L=comptes(), moi=session();
  $('nb').textContent=L.length+(L.length>1?' comptes':' compte');
  $('tb').innerHTML=L.map((u,i)=>{
    const r=ROLES[u.role]||{lib:u.role};
    const estMoi=moi&&moi.id===u.ident;
    const patrons=L.filter(x=>x.role==='patron'&&x.actif).length;
    const dernierPatron=u.role==='patron'&&u.actif&&patrons<2;
    return `<tr class="${u.actif?'':'off'}" data-i="${i}">
      <td class="qui"><b>${esc(u.nom)}${estMoi?' <span class="moi">— toi</span>':''}</b><span>${esc(u.ident)}${u.email?' · '+esc(u.email):''}</span></td>
      <td><span class="rl ${esc(u.role)}">${esc(r.lib)}</span></td>
      <td class="qd">${u.actif?dfr(u.dernier):'compte fermé'}</td>
      <td class="qd">${dfr(u.cree)}</td>
      <td class="act">
        <button data-mod="${i}">rôle</button>
        <button data-mdp="${i}">mot de passe</button>
        <button data-mail="${i}">${u.email?'envoyer l\'accès':'email'}</button>
        ${dernierPatron?'' : `<button class="dg" data-off="${i}">${u.actif?'fermer':'rouvrir'}</button>`}
      </td></tr>`;
  }).join('');
}

/* ---------- ouvrir un accès ---------- */
let EDIT=null;
function ouvre(mode,i){
  EDIT={mode,i};
  const u=i!=null?comptes()[i]:null;
  $('ftitre').textContent = mode==='new'?'Ouvrir un accès'
    : mode==='role'?('Rôle de '+u.nom)
    : mode==='mail'?('Email de '+u.nom) : ('Nouveau mot de passe pour '+u.nom);
  $('f-role').innerHTML=Object.entries(ROLES).map(([k,r])=>
    `<option value="${k}">${esc(r.lib)}</option>`).join('');
  const maj=()=>{ const r=ROLES[$('f-role').value]; $('f-aide').textContent=r?r.aide:''; };
  $('f-role').onchange=maj;
  $('f-nom').value=u?u.nom:''; $('f-id').value=u?u.ident:'';
  $('f-mail').value=u?(u.email||''):'';
  $('f-role').value=u?u.role:'commercial'; maj();
  $('f-m').value=''; $('f-m2').value=''; $('fmsg').textContent='';
  $('f-nom').closest('.fg2').hidden = mode!=='new';
  $('f-role').closest('.fld').hidden = (mode==='mdp'||mode==='mail');
  $('f-mailbloc').hidden = (mode==='role'||mode==='mdp');
  /* le générateur sert quand il y a un mot de passe à poser ; la case d'envoi
     n'a de sens que si l'on connaît une adresse */
  const avecMdp = (mode==='new'||mode==='mdp');
  if($('f-gen')) $('f-gen').closest('.genr').hidden = !avecMdp;
  if($('f-genval')){ $('f-genval').hidden=true; $('f-genval').textContent=''; }
  if($('f-copie')) $('f-copie').hidden=true;
  if($('f-env')){
    $('f-env').checked=false;                    /* rien ne part sans un geste */
    const aUnMail = mode==='new' || !!(u&&u.email);
    $('f-envbloc').hidden = !aUnMail;
    $('f-envaide').hidden = !aUnMail;
  }
  $('f-m').closest('.fg2').hidden = (mode==='role'||mode==='mail');
  $('f-m').closest('.fg2').nextElementSibling.hidden = (mode==='role'||mode==='mail');
  $('fok').textContent = mode==='new'?"Ouvrir l'accès" : mode==='role'?'Changer le rôle'
    : mode==='mail'?'Enregistrer' : 'Changer le mot de passe';
  $('fov').classList.add('on');
  setTimeout(()=>$(mode==='new'?'f-nom':(mode==='role'?'f-role':'f-m')).focus(),60);
}
$('fx').onclick=$('fc').onclick=()=>$('fov').classList.remove('on');
$('fov').addEventListener('click',e=>{ if(e.target.id==='fov') $('fov').classList.remove('on'); });
/* ---- qui peut toucher à qui ----
   Un compte Patron ou Admin ne se modifie que par un Admin. Sans cette règle,
   n'importe quel compte ayant le droit « accès » pourrait se hisser lui-même en
   Admin, ou changer le mot de passe du patron : le rôle Admin ne vaudrait alors
   plus rien du tout. */
function ilExisteUnAdmin(){ return comptes().some(x=>x.role==='admin'&&x.actif); }
function peutToucher(u){
  if(!u) return true;
  const haut = (u.role==='admin'||u.role==='patron');
  if(!haut) return true;
  if(peut('technique')) return true;
  /* L'AMORCE. Sans elle, le rôle Admin est inatteignable : seul un Admin peut
     nommer un Admin, et il n'en existe aucun au départ. Tant qu'aucun compte
     Admin actif n'existe, le Patron peut donc franchir ce pas — une fois. Dès
     qu'un Admin existe, la porte se referme et ne se rouvre plus. */
  return !ilExisteUnAdmin() && peut('acces');
}
function refusToucher(u){
  alert('Le compte de '+u.nom+' est un compte '+((ROLES[u.role]||{}).lib||u.role)+'.\n\n'
    +"Seul un compte Admin peut le modifier. C'est ce qui empêche quelqu'un de se "
    +"donner lui-même les pleins droits, ou de changer le mot de passe du patron.");
}

/* ============ ON NE SE RETIRE PAS SES PROPRES DROITS ============
   Le tableau écrit « — toi » à côté de son compte. C'était une étiquette, pas
   un garde-fou : rien n'empêchait de se passer soi-même en Commercial, de
   fermer son propre accès, ou de décocher « Ouvre et ferme les accès » sur son
   propre rôle. Dans les trois cas l'onglet Accès disparaît dans la seconde, et
   il faut la session de quelqu'un d'autre pour revenir.

   Le garde-fou du « dernier compte qui a la main » existait déjà, mais il ne
   couvrait pas ce cas-là : tant qu'un autre Patron reste actif, se saborder
   était parfaitement autorisé. Or c'est presque toujours une fausse manœuvre —
   personne ne décide de se couper l'accès à l'outil qu'il administre. Et quand
   c'est vraiment voulu (passer la main puis se retirer), l'ordre correct est
   d'ouvrir l'accès de l'autre D'ABORD et de se faire rétrograder par lui.

   On refuse donc, avec la marche à suivre dans le message plutôt qu'un « non »
   sec. Les changements qui ne coûtent aucun droit — se renommer, changer son
   propre mot de passe, passer de Patron à Admin — restent libres. */
function estMonCompte(u){
  const s=session();
  return !!(s && u && s.id===u.ident);
}
/* les droits sans lesquels on ne peut plus revenir sur cette page */
const DROITS_RETOUR=['acces','technique'];
function perdSonRetour(roleAvant, roleApres){
  const a=ROLES[roleAvant]||{}, b=ROLES[roleApres]||{};
  return DROITS_RETOUR.some(d=>a[d]&&!b[d]);
}
/* Le texte, séparé de la façon de le montrer : dans la fenêtre de modification
   il s'affiche EN PLACE, comme les autres refus voisins — la fenêtre reste
   ouverte, on corrige et on continue. Ailleurs (fermeture d'un accès, clic dans
   le tableau des droits) il n'y a pas de fenêtre où l'écrire, c'est donc une
   alerte. Faire sortir un refus par un canal différent de ses voisins, c'est
   déjà une petite incohérence ; le faire sortir en fermant la fenêtre que la
   personne venait d'ouvrir, c'en est une vraie. */
function texteSaborder(quoi){
  return "Tu ne peux pas te retirer tes propres droits. "+quoi
    +" Si tu veux vraiment passer la main : ouvre d'abord un accès Admin à "
    +"quelqu'un d'autre, connecte-toi avec ce compte-là, et c'est lui qui te "
    +"rétrogradera. Dans l'autre sens, tu perdrais cette page avant d'avoir fini.";
}
function refusSaborder(quoi){ alert(texteSaborder(quoi)); }

$('add').onclick=()=>ouvre('new',null);

$('tb').addEventListener('click',async e=>{
  const b=e.target.closest('button'); if(!b) return;
  const iC = b.dataset.mod ?? b.dataset.mdp ?? b.dataset.off;
  if(iC!==undefined && iC!==null){
    const cible=comptes()[+iC];
    if(!peutToucher(cible)) return refusToucher(cible);
  }
  if(b.dataset.mail!==undefined){
    const u=comptes()[+b.dataset.mail];
    if(!u.email) return ouvre('mail',+b.dataset.mail);
    /* On ne « renvoie » pas le mot de passe : il n'existe plus. SAM n'en garde
       qu'une empreinte — c'est ce qui fait que personne, pas même le patron, ne
       peut relire celui de quelqu'un. On en pose donc un NEUF au moment de
       l'envoi. Effet de bord voulu : ce qui a pu traîner ailleurs meurt ici. */
    if(!confirm(`Envoyer ses accès à ${u.nom} ?\n\n`
      +`Un mot de passe provisoire tout neuf va être créé et mis dans le message. `
      +`L'ancien, s'il en avait un, cessera de fonctionner immédiatement.\n\n`
      +`Rien ne part avant que tu aies relu le message et cliqué « envoyer » dans ton logiciel de courrier.`)) return;
    const neuf=motDePasseNeuf();
    await remetMotDePasse(u.ident,neuf);
    jlog('mot de passe provisoire créé pour l\'envoi — '+u.nom,u.ident,null);
    dessine();
    return envoieAcces(comptes().find(x=>x.ident===u.ident), neuf);
  }
  if(b.dataset.mod!==undefined) return ouvre('role',+b.dataset.mod);
  if(b.dataset.mdp!==undefined) return ouvre('mdp',+b.dataset.mdp);
  if(b.dataset.off!==undefined){
    const L=comptes(), u=L[+b.dataset.off];
    const ferme=u.actif;
    if(ferme && estMonCompte(u))
      return refusSaborder("Fermer ton propre accès te déconnecterait, et tu ne "
        +"pourrais pas le rouvrir toi-même.");
    if(!confirm(ferme
      ? `Fermer l'accès de ${u.nom} ? Il ne pourra plus entrer. Tout ce qu'il a fait reste au journal.`
      : `Rouvrir l'accès de ${u.nom} ?`)) return;
    u.actif=!ferme; sauveComptes(L);
    jlog(ferme?'accès fermé':'accès rouvert',u.ident,(ROLES[u.role]||{}).lib);
    dessine();
  }
});

$('fok').onclick=async()=>{
  const dis=(t,c)=>{ $('fmsg').textContent=t; $('fmsg').className='msg '+(c||'err'); };
  const m=$('f-m').value, m2=$('f-m2').value;
  try{
    if(EDIT.mode==='new'){
      const nom=$('f-nom').value.trim(), id=$('f-id').value.trim();
      if(nom.length<2) return dis('Mets le nom de la personne.');
      if(!/^[a-zA-Z0-9._-]{2,}$/.test(id)) return dis('Identifiant : lettres, chiffres, point ou tiret, sans espace.');
      if(m.length<6) return dis('Le mot de passe doit faire au moins 6 caractères.');
      if(m!==m2) return dis('Les deux mots de passe ne sont pas identiques.');
      const s=session();
      if(($('f-role').value==='admin'||$('f-role').value==='patron') && !peut('technique'))
        return dis('Seul un compte Admin peut ouvrir un accès Patron ou Admin.');
      const mail=$('f-mail').value.trim();
      if(mail && !/^[^@\s]+@[^@\s.]+\.[^@\s]{2,}$/.test(mail))
        return dis("Cette adresse n'a pas l'air d'en être une.");
      await creeCompte({nom,ident:id,mdp:m,role:$('f-role').value,par:s?s.nom:'',email:mail});
      jlog('accès ouvert',id,(ROLES[$('f-role').value]||{}).lib);
      /* On n'envoie QUE si la case est cochée. Ouvrir la fenêtre d'envoi tout seul,
         comme le faisait la version précédente, revenait à décider à la place de
         Sam le moment où la personne reçoit ses accès. */
      if(mail && $('f-env') && $('f-env').checked){
        $('fov').classList.remove('on'); dessine();
        envoieAcces(comptes().find(x=>x.ident===id), m); return;
      }
    } else {
      const L=comptes(), u=L[EDIT.i];
      if(EDIT.mode==='role'){
        const av=(ROLES[u.role]||{}).lib, nv=$('f-role').value;
        if(nv===u.role){ $('fov').classList.remove('on'); return; }
        const amorce = !ilExisteUnAdmin() && peut('acces');   // voir peutToucher
        if((nv==='admin'||nv==='patron') && !peut('technique') && !amorce)
          return dis('Seul un compte Admin peut donner le rôle Patron ou Admin.');
        if(estMonCompte(u) && perdSonRetour(u.role,nv))
          return dis(texteSaborder('Passer ton propre compte en '
            +((ROLES[nv]||{}).lib||nv)+" te ferait perdre l'onglet Accès tout de suite."));
        /* On compte les comptes qui gardent la main sur l'outil : patrons ET admins.
           Ne compter que les patrons laissait fermer le dernier accès complet.
           Et on ne bloque que si le compte PERD ce statut : passer de Patron à
           Admin ne retire la main à personne — l'interdire enfermait l'outil. */
        const maitres=L.filter(x=>(x.role==='patron'||x.role==='admin')&&x.actif).length;
        const restaitMaitre=(nv==='patron'||nv==='admin');
        if((u.role==='patron'||u.role==='admin')&&maitres<2&&!restaitMaitre)
          return dis('C\'est le seul compte qui a la main sur l\'outil : ouvres-en un autre avant de changer celui-ci.');
        u.role=nv; sauveComptes(L);
        jlog('rôle changé — '+u.nom,u.ident,av+' → '+(ROLES[nv]||{}).lib);
        if(amorce&&nv==='admin')
          jlog('premier Admin nommé — la porte se referme',u.ident,
               'seul un Admin peut désormais toucher aux comptes Patron et Admin');
      } else if(EDIT.mode==='mail'){
        const av=u.email||'', nv=$('f-mail').value.trim();
        if(nv && !/^[^@\s]+@[^@\s.]+\.[^@\s]{2,}$/.test(nv))
          return dis("Cette adresse n'a pas l'air d'en être une.");
        if(nv===av){ $('fov').classList.remove('on'); return; }
        u.email=nv; sauveComptes(L);
        jlog(nv?'email noté — '+u.nom:'email effacé — '+u.nom, u.ident, av||null, nv||null);
        $('fov').classList.remove('on'); dessine();
        /* on note l'adresse, on n'envoie rien : le bouton « envoyer l'accès » est
           là pour ça, quand Sam le décidera */
        return;
      } else {
        if(m.length<6) return dis('Le mot de passe doit faire au moins 6 caractères.');
        if(m!==m2) return dis('Les deux mots de passe ne sont pas identiques.');
        await remetMotDePasse(u.ident,m);
        jlog('mot de passe remis — '+u.nom,u.ident,null);
        if(u.email && $('f-env') && $('f-env').checked){
          $('fov').classList.remove('on'); dessine();
          envoieAcces(comptes().find(x=>x.ident===u.ident), m); return;
        }
      }
    }
    $('fov').classList.remove('on'); dessine();
  }catch(err){ dis(err.message||'Impossible.'); }
};



/* ---------- générer un mot de passe provisoire ----------
   Pourquoi pas « Perfumes2026 » ou un mot du dictionnaire : ce mot de passe part
   parfois par email, donc il doit résister à quelqu'un qui lirait la boîte. On
   tire au sort dans un alphabet SANS les caractères qui se confondent à l'oral
   ou à l'écrit — ni O ni 0, ni I ni l ni 1 — parce qu'il sera souvent dicté au
   téléphone, et qu'un mot de passe mal recopié est un appel de plus. */
const GEN_LETTRES='abcdefghjkmnpqrstuvwxyz';
const GEN_MAJ    ='ABCDEFGHJKMNPQRSTUVWXYZ';
const GEN_CHIFFRE='23456789';
function motDePasseNeuf(){
  const tout=GEN_LETTRES+GEN_MAJ+GEN_CHIFFRE;
  const tire=(s)=>s[crypto.getRandomValues(new Uint32Array(1))[0] % s.length];
  /* au moins une majuscule et un chiffre, le reste au hasard : on ne veut pas
     tirer douze minuscules d'affilée et appeler ça un mot de passe */
  const c=[tire(GEN_MAJ), tire(GEN_CHIFFRE)];
  while(c.length<12) c.push(tire(tout));
  /* mélange de Fisher-Yates, pour que la majuscule ne soit pas toujours en tête */
  for(let i=c.length-1;i>0;i--){
    const j=crypto.getRandomValues(new Uint32Array(1))[0] % (i+1);
    [c[i],c[j]]=[c[j],c[i]];
  }
  return c.join('');
}
if($('f-gen')) $('f-gen').onclick=()=>{
  const m=motDePasseNeuf();
  $('f-m').value=m; $('f-m2').value=m;
  $('f-genval').textContent=m; $('f-genval').hidden=false;
  $('f-copie').hidden=false; $('fmsg').textContent='';
};
if($('f-copie')) $('f-copie').onclick=async()=>{
  const m=$('f-genval').textContent;
  try{ await navigator.clipboard.writeText(m);
       $('fmsg').textContent='Mot de passe copié.'; $('fmsg').className='msg ok'; }
  catch(e){ $('fmsg').textContent='Sélectionne-le et fais ⌘C.'; $('fmsg').className='msg'; }
};

/* ---------- envoyer l'accès à la personne ----------
   Ce qui part : l'adresse du site et l'identifiant. Rien d'autre.
   Ce qui NE part JAMAIS : les mots de passe — ni celui du compte, ni celui de la
   porte du site. Un mot de passe posé dans une boîte mail n'est plus un mot de
   passe : il y reste des années, il est lu par le fournisseur de messagerie, et
   il suit la personne quand elle quitte l'entreprise. On le dit à la personne de
   vive voix ou par SMS, et le message le rappelle noir sur blanc.

   Trois langues : à Miami, l'équipe n'écrit pas toute en français. Ce sont trois
   textes écrits à la main, pas une traduction automatique — un accès mal compris
   est un accès qu'on redemande. */
const M_TXT={
 fr:(u,url,mdp)=>({obj:'Ton accès à Perfumes Trade',
  corps:`Bonjour ${u.nom},

Ton accès à l'outil est ouvert.

Adresse du site : ${url}
Ton identifiant : ${u.ident}${mdp?`
Mot de passe provisoire : ${mdp}`:''}
${mdp?`
Ce mot de passe est provisoire : à ta première connexion, l'outil te demandera d'en choisir un autre, que toi seul connaîtras. Fais-le tout de suite, et supprime ce message ensuite.
`:`
Le mot de passe n'est pas dans ce message, c'est volontaire : je te le donne de vive voix ou par SMS.
`}
Le site demande aussi un mot de passe à l'entrée, avant l'outil lui-même. Il est le même pour toute l'équipe :

Mot de passe du site : ...........  (à remplir avant d'envoyer)

À bientôt.`}),
 en:(u,url,mdp)=>({obj:'Your Perfumes Trade access',
  corps:`Hello ${u.nom},

Your access to the tool is open.

Website: ${url}
Your username: ${u.ident}${mdp?`
Temporary password: ${mdp}`:''}
${mdp?`
This password is temporary: the first time you log in, the tool will ask you to choose your own, known only to you. Do it right away, then delete this message.
`:`
The password is deliberately not in this message: I will give it to you in person or by text.
`}
The site also asks for a password at the door, before the tool itself. It is the same for the whole team:

Site password: ...........  (fill this in before sending)

Talk soon.`}),
 es:(u,url,mdp)=>({obj:'Tu acceso a Perfumes Trade',
  corps:`Hola ${u.nom},

Tu acceso a la herramienta ya está abierto.

Dirección del sitio: ${url}
Tu usuario: ${u.ident}${mdp?`
Contraseña provisional: ${mdp}`:''}
${mdp?`
Esta contraseña es provisional: la primera vez que entres, la herramienta te pedirá que elijas la tuya, que solo tú conocerás. Hazlo enseguida y borra después este mensaje.
`:`
La contraseña no está en este mensaje, es a propósito: te la doy en persona o por mensaje de texto.
`}
El sitio también pide una contraseña en la entrada, antes de la herramienta. Es la misma para todo el equipo:

Contraseña del sitio: ...........  (rellénala antes de enviar)

Hasta pronto.`})
};
/* M_MDP ne vit que le temps de la fenêtre : il n'est ni enregistré, ni synchronisé,
   ni relisible ensuite. Fermer la fenêtre l'efface — c'est voulu. */
let M_U=null, M_LG='fr', M_MDP='';
function mPeintAcces(){
  if(!M_U) return;
  const url=(location.protocol==='file:')?'(l\'adresse du site)':location.origin;
  const t=M_TXT[M_LG](M_U,url,M_MDP);
  $('m-obj').textContent=t.obj;
  $('m-corps').value=t.corps;
  $('mov').querySelectorAll('[data-lg]').forEach(b=>b.classList.toggle('on',b.dataset.lg===M_LG));
}
function envoieAcces(u,mdp){
  if(!u||!u.email) return;
  M_U=u; M_MDP=String(mdp||'');
  M_LG=(typeof LANG!=='undefined'&&M_TXT[LANG])?LANG:'fr';
  $('m-a').textContent=u.email;
  mPeintAcces();
  $('mov').classList.add('on');
}
$('mov').addEventListener('click',e=>{ if(e.target.id==='mov') $('mov').classList.remove('on'); });
$('mx').onclick=$('mc').onclick=()=>{ $('mov').classList.remove('on'); M_MDP=''; };
$('mov').querySelectorAll('[data-lg]').forEach(b=>b.onclick=()=>{ M_LG=b.dataset.lg; mPeintAcces(); });
$('mcopie').onclick=async()=>{
  try{ await navigator.clipboard.writeText($('m-corps').value);
       $('mmsg').textContent='Texte copié.'; $('mmsg').className='msg ok'; }
  catch(e){ $('m-corps').select(); $('mmsg').textContent='Fais ⌘C pour copier.'; $('mmsg').className='msg'; }
};
$('mok').onclick=()=>{
  /* on prend le sujet et le corps DANS la fenetre, pas dans le modele : Sam a pu
     les retoucher avant d'envoyer, et c'est sa version qui doit partir */
  const lien='mailto:'+encodeURIComponent(M_U.email)
    +'?subject='+encodeURIComponent($('m-obj').textContent)
    +'&body='+encodeURIComponent($('m-corps').value);
  window.__mailto=lien;                 /* point d'observation pour les tests */
  /* Le journal note QU'ON a envoyé, jamais CE QU'ON a envoyé : un mot de passe
     recopié dans le journal serait lisible par tous ceux qui y ont accès. */
  jlog(M_MDP?'accès + mot de passe provisoire envoyés — '+M_U.nom
            :'accès envoyé par email — '+M_U.nom, M_U.ident, null, M_U.email);
  $('mov').classList.remove('on'); M_MDP='';
  location.href=lien;
};

/* en ligne : quand le cockpit renvoie la liste à jour, on redessine */
window.addEventListener('comptes-maj',()=>{ try{ dessine(); dessineDroits(); }catch(e){} });

/* ---------- le mur : seul le patron entre ici ---------- */
(function(){
  const s=session(); if(!s) return;
  if(!peut('acces')){
    $('ban').hidden=true;
    document.querySelector('.wrap').insertAdjacentHTML('beforeend',
      `<div class="mur"><h2>Cette page est réservée au patron</h2>
       <p>Tu es connecté comme <b>${esc(s.nom)}</b> (${esc((ROLES[s.role]||{}).lib||s.role)}).
       Ouvrir ou fermer un accès, changer un rôle ou un mot de passe :
       seul un compte Patron peut le faire. C'est voulu — sinon la signature du journal
       ne voudrait plus rien dire.</p></div>`);
    $('src').innerHTML='accès refusé';
    return;
  }
  $('ban').innerHTML=`<b>Ce que fait cette page, et ce qu'elle ne fait pas.</b>
    Elle décide qui entre dans SAM, sous quel nom le journal signe ses actions, et ce que
    chacun voit à l'écran. Tant que SAM tourne sur cet ordinateur et pas sur un serveur,
    c'est un <b>badge, pas une serrure</b> : quelqu'un de déterminé peut ouvrir les fichiers
    autrement. Ça répond à « qui a fait quoi » et à « qui voit les prix d'achat » — pas à
    « comment j'empêche quelqu'un d'entrer ». La vraie serrure viendra avec le serveur.`;
  if(localStorage.getItem('sam-comptes-demo-v1')==='1'){
    $('ban').insertAdjacentHTML('afterend',
      `<div class="bandeau" style="background:var(--warn-soft);border-left-color:var(--warn)">
        <b>Des comptes de démonstration sont encore ouverts.</b> Sam, Javier, Ana et Le comptable ont
        un mot de passe connu de tous (<code>sam123</code>…), affiché sur la page d'accueil. Ils servent
        à essayer l'outil et à montrer les rôles. <b>Avant la vraie mise en service :</b> ferme ceux qui
        ne servent pas, et change le mot de passe de ceux que tu gardes — le bouton
        « mot de passe » sur chaque ligne. L'avertissement disparaîtra tout seul.
        <button class="btn" id="finidemo" style="margin-left:10px">C'est fait, enlever l'avertissement</button>
      </div>`);
    const f=document.getElementById('finidemo');
    if(f) f.onclick=()=>{ if(!confirm('Enlever l\'avertissement ? À ne faire qu\'une fois les mots de passe changés.')) return;
      /* '0' et non pas effacé : la page d'accueil saura qu'elle ne doit
         plus jamais reposer les comptes de démonstration. */
      try{ localStorage.setItem('sam-comptes-demo-v1','0'); }catch(e){}
      jlog('fin des comptes de démonstration','',null); location.reload(); };
  }
  $('tout').hidden=false;
  dessine(); dessineDroits();
  const nr=Object.keys(ROLES).length;
  $('src').innerHTML=comptes().length+' compte'+(comptes().length>1?'s':'')+'<br>'+nr+' rôles';
})();
$('sfoot').innerHTML='Accès et rôles';
"""

html = coquille("Accès", "Accès", "Qui entre dans SAM, et ce que chacun voit", CSS, CORPS, JS)
open('acces.html', 'w').write(html)
print('acces.html', round(os.path.getsize('acces.html') / 1024), 'Ko')
