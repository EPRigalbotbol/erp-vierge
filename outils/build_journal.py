# -*- coding: utf-8 -*-
from build_crm import coquille

CSS = r'''
.sous{margin:5px 0 0;font-size:14px;color:var(--ink-2);max-width:74ch;line-height:1.5}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(165px,1fr));gap:1px;
background:var(--line-2);border:1px solid var(--line);border-radius:9px;overflow:hidden;
margin-bottom:20px;box-shadow:0 1px 2px rgba(0,0,0,.04)}
.kpi{background:var(--surface);padding:15px 17px;display:flex;flex-direction:column;gap:3px}
.kpi .v{font-family:Inter,sans-serif;font-size:24px;font-weight:700;line-height:1;
letter-spacing:-.03em;font-variant-numeric:tabular-nums}
.kpi .k{font-size:12px;color:var(--ink-3);line-height:1.4}
.tools{display:flex;gap:9px;flex-wrap:wrap;align-items:center;margin-bottom:16px}
.tools .sp{margin-left:auto}
.srch{position:relative;flex:1 1 220px;max-width:340px}
.srch input{width:100%;padding:9px 12px 9px 33px;font-family:inherit;font-size:13.5px;
border:1px solid var(--line);border-radius:7px;background:var(--surface);color:var(--ink)}
.srch input:focus{outline:0;border-color:var(--iris);box-shadow:0 0 0 3px var(--iris-soft)}
.srch::before{content:"⌕";position:absolute;left:11px;top:50%;transform:translateY(-50%);
color:var(--ink-3);font-size:16px}
.sel{padding:9px 11px;font-family:inherit;font-size:13.5px;border:1px solid var(--line);
border-radius:7px;background:var(--surface);color:var(--ink);cursor:pointer}
.sel:focus{outline:0;border-color:var(--iris)}

.tbl{width:100%;border-collapse:collapse;font-size:13px;background:var(--surface);
border:1px solid var(--line);border-radius:9px;overflow:hidden}
.tbl th{text-align:left;font-family:Inter,sans-serif;font-size:9.5px;letter-spacing:.11em;
text-transform:uppercase;color:var(--ink-2);font-weight:700;padding:11px 13px;
background:var(--surface-2);border-bottom:1px solid var(--line);white-space:nowrap}
.tbl td{padding:11px 13px;border-bottom:1px solid var(--line-2);vertical-align:top}
.tbl td.no,.tbl th.no{width:44px;text-align:right;padding-right:7px;color:var(--ink-3);
font-family:Inter,sans-serif;font-size:11.5px;font-variant-numeric:tabular-nums}
.tbl tbody tr:last-child td{border-bottom:0}
.tbl tbody tr:hover{background:var(--surface-2)}
.qd{font-family:Inter,sans-serif;font-size:11.5px;color:var(--ink-2);white-space:nowrap;
line-height:1.45;font-variant-numeric:tabular-nums}
.qd b{display:block;color:var(--ink);font-weight:600;font-size:12.5px}
.who{font-weight:600;white-space:nowrap}
.who .rl{display:block;font-weight:500;font-size:11px;color:var(--ink-3)}
.ou{display:block;margin-top:4px;font-size:11px;color:var(--ink-3);font-family:Inter,sans-serif}
.ref a.rlk{color:inherit;text-decoration:none}.ref a.rlk:hover b{color:var(--iris);text-decoration:underline}
.who.anon{color:var(--ink-3);font-weight:400;font-style:italic}
.ref b{display:block;font-weight:600;line-height:1.3}
.ref span{color:var(--ink-3);font-family:Inter,sans-serif;font-size:11px}
.act{display:inline-flex;align-items:center;gap:5px;font-size:11px;font-weight:700;
padding:4px 9px;border-radius:20px;white-space:nowrap;line-height:1;letter-spacing:.02em}
.act::before{content:"";width:5px;height:5px;border-radius:50%;background:currentColor}
.a-prix{background:var(--crit-soft);color:var(--crit)}
.a-acces{background:var(--iris-soft);color:var(--iris)}
.a-stock{background:var(--iris-soft);color:var(--iris)}
.a-verif{background:var(--good-soft);color:var(--good)}
.a-import{background:var(--warn-soft);color:var(--warn)}
.a-reception{background:var(--good-soft);color:var(--good)}
.a-vente{background:var(--iris-soft);color:var(--iris)}
.a-annulation{background:var(--crit-soft);color:var(--crit)}
.a-ajustement{background:var(--warn-soft);color:var(--warn)}
.a-reglage{background:var(--iris-soft);color:var(--iris)}
.a-fiche,.a-fournisseur,.a-creation,.a-client,.a-connecteur{background:var(--surface-2);color:var(--ink-2)}
.chg{font-family:Inter,sans-serif;font-size:12.5px;font-variant-numeric:tabular-nums;
line-height:1.5}
.chg .av{color:var(--ink-3);text-decoration:line-through}
.chg .fl{color:var(--ink-3);margin:0 5px}
.chg .ap{color:var(--ink);font-weight:700}
.chg .lb{display:block;font-family:Inter,sans-serif;font-size:11px;color:var(--ink-3);
letter-spacing:.02em}
.det{margin-top:7px;font-size:12px;color:var(--ink-2)}
.det summary{cursor:pointer;color:var(--iris);font-weight:600;font-size:12px}
.det ul{margin:7px 0 0;padding-left:17px;max-height:220px;overflow-y:auto;
font-family:Inter,sans-serif;font-size:11.5px;line-height:1.7}
.wrapx{overflow-x:auto}
.vide{border:2px dashed var(--line);border-radius:11px;padding:38px 30px;text-align:center;
background:var(--surface-2);max-width:62ch;margin:24px auto}
.vide h3{margin:0 0 10px;font-size:19px;font-weight:700;letter-spacing:-.02em}
.vide p{margin:0 0 12px;font-size:14px;color:var(--ink-2);line-height:1.65}
.avert{background:var(--warn-soft);border:1px solid var(--warn);border-left-width:4px;
border-radius:0 8px 8px 0;padding:14px 18px;font-size:13px;color:var(--ink-2);line-height:1.6;
margin-bottom:22px;max-width:82ch}
.avert b{color:var(--ink)}
.plus{display:block;width:100%;margin-top:14px;padding:12px;background:var(--surface);
border:1px solid var(--line);border-radius:8px;font-family:inherit;font-size:13.5px;
color:var(--ink-2);cursor:pointer;font-weight:500}
.plus:hover{border-color:var(--iris);color:var(--iris)}
'''

CORPS = r'''
<div class="avert" id="avert-local"><b>Ce journal enregistre un nom déclaré, pas un nom prouvé.</b>
Un fichier ouvert sur un ordinateur n'a pas de serveur pour authentifier qui que ce soit :
chacun indique son nom une fois, et il est attaché à ses actions. Pour une équipe de deux ou trois,
ça répond à « qui a changé ce prix, et quand ». Ça ne vaut pas preuve devant un tiers.</div>
<div class="avert" id="avert-ligne" hidden style="background:var(--good-soft);border-color:var(--good)"><b>Chaque action est signée par le compte connecté au serveur.</b>
Le nom, le rôle et la rubrique viennent du cockpit, pas d'une déclaration : « qui a changé ce prix, et quand » a une réponse vérifiable.
Le journal est gardé sur le serveur, avec ses versions précédentes.</div>

<div id="kpis"></div>

<div class="tools">
  <div class="srch"><input id="q" autocomplete="off" placeholder="Chercher une référence, un nom, un code-barres…"></div>
  <select id="fa" class="sel">
    <option value="">Toutes les actions</option>
    <option value="prix">Prix</option><option value="stock">Stock</option>
    <option value="verif">Comptage</option><option value="import">Imports</option>
    <option value="reception">Réceptions</option><option value="vente">Ventes</option><option value="annulation">Annulations</option>
    <option value="ajustement">Ajustements (casse, vol, testeur…)</option>
    <option value="reglage">Réglages (commissions, seuils)</option><option value="acces">Accès (comptes, connexions)</option>
    <option value="fournisseur">Fournisseurs</option><option value="client">Clients</option>
    <option value="connecteur">Connecteurs</option><option value="fiche">Autres champs</option>
  </select>
  <select id="fu" class="sel"><option value="">Tout le monde</option></select>
  <select id="fp" class="sel">
    <option value="">Depuis toujours</option><option value="1">Aujourd'hui</option>
    <option value="7">7 derniers jours</option><option value="30">30 derniers jours</option>
  </select>
  <span class="sp"></span>
  <span id="exp"></span>
</div>

<div id="corps"></div>
'''

JS = r'''
const KJOU='crm-journal-v1', KUSR='crm-utilisateur-v1';
let JOU=[]; try{ JOU=JSON.parse(localStorage.getItem(KJOU)||'[]'); }catch(e){ JOU=[]; }
JOU.reverse();                       // le plus récent en haut
let USR=NOM_UTIL;
window.__nomChange.push(v=>{ USR=v; try{ majUser(); }catch(e){} });
let vus=60;

if(typeof _SY_ON!=='undefined'&&_SY_ON){ $('avert-local').hidden=true; $('avert-ligne').hidden=false; }
const LIBA={acces:'Accès',prix:'Prix',stock:'Stock',verif:'Comptage',import:'Import',reception:'Réception',vente:'Vente',annulation:'Annulation',
            fournisseur:'Fournisseur',fiche:'Fiche',creation:'Création',
            client:'Client',connecteur:'Connecteur',ajustement:'Ajustement',reglage:'Réglage'};
/* un ajustement de stock (casse, vol, testeur…) est écrit avec act:'stock' :
   on le distingue pour qu'il ait sa propre pastille et son propre filtre */
const acte=e=>(e.act==='stock'&&/^ajustement/.test(e.lib||''))?'ajustement':e.act;
const OU={catalogue:'Catalogue',stock:'Inventaire',inventaire_pc:'Inventaire Perfume City',factures:'Factures',ventes:'Ventes',
          fournisseurs:'Fournisseurs',clients:'VIP wholesale',retail:'Retail',connecteurs:'Connecteurs',messages:'Messages',
          journal:'Journal',tableau:'Tableau de bord',acces:'Accès',reglages:'Réglages',accueil:'Entrée'};
const RL={patron:'Patron',commercial:'Commercial',entrepot:'Entrepôt',comptable:'Comptable'};
const ou=e=>e.pg?(OU[e.pg]||e.pg):'';
const dt=iso=>{ const d=new Date(iso);
  return {j:d.toLocaleDateString('fr-FR',{day:'2-digit',month:'2-digit',year:'2-digit'}),
          h:d.toLocaleTimeString('fr-FR',{hour:'2-digit',minute:'2-digit',second:'2-digit'}),d}; };
const fmt=v=>v==null||v===''?'—':(typeof v==='number'?v.toLocaleString('fr-FR'):String(v));

function filtre(){
  const q=$('q').value.trim().toLowerCase(), a=$('fa').value, u=$('fu').value, p=$('fp').value;
  const lim = p? Date.now()-(+p)*86400000 : 0;
  return JOU.filter(e=>{
    if(a && acte(e)!==a) return false;
    if(u && e.u!==u) return false;
    if(lim && new Date(e.t).getTime()<lim) return false;
    if(q){ const t=((e.ref||'')+' '+(e.bc||'')+' '+(e.u||'')+' '+(e.lib||'')+' '+ou(e)+' '+(e.ap??'')+' '+(e.av??'')).toLowerCase();
      if(!t.includes(q)) return false; }
    return true;
  });
}

function ligne(e,i){
  const d=dt(e.t);
  const chg = (e.act==='import'||e.act==='reception'||e.act==='vente'||e.act==='annulation')
    ? `<span class="lb">${esc(e.lib||'')}${e.n!=null?' · '+nf(e.n)+' quantité'+(e.n>1?'s':'')+' modifiée'+(e.n>1?'s':''):''}${e.note?' · '+esc(e.note):''}</span>
       <span class="ap">${e.impact>=0?'+':'−'}${money(Math.abs(e.impact))}</span> de valeur de stock
       ${e.det&&e.det.length?`<details class="det"><summary>voir le détail</summary><ul>${
         e.det.map(x=>`<li>${esc(x.ref)} : ${x.av} → <b>${x.ap}</b></li>`).join('')}</ul></details>`:''}`
    : `<span class="lb">${esc(e.lib||e.champ||'')}</span>
       <span class="av">${esc(fmt(e.av))}</span><span class="fl">→</span><span class="ap">${esc(fmt(e.ap))}</span>`;
  return `<tr>
    <td class="no">${nf((i||0)+1)}</td>
    <td class="qd"><b>${d.j}</b>${d.h}</td>
    <td class="who${e.u&&e.u!=='(non renseigné)'?'':' anon'}">${esc(e.u||'—')}${e.r?`<span class="rl">${esc(RL[e.r]||e.r)}</span>`:''}</td>
    <td><span class="act a-${acte(e)}">${LIBA[acte(e)]||acte(e)}</span>${ou(e)?`<span class="ou">${esc(ou(e))}</span>`:''}</td>
    <td class="ref">${e.ref?(e.bc?`<a class="rlk" href="catalogue.html?q=${encodeURIComponent(e.bc)}" title="Ouvrir dans le catalogue"><b>${esc(e.ref)}</b></a>`:`<b>${esc(e.ref)}</b>`):'<b style="color:var(--ink-3)">—</b>'}
      ${e.bc?`<span>${esc(e.bc)}</span>`:''}</td>
    <td class="chg">${chg}</td></tr>`;
}

function dessine(){
  const L=filtre();
  const j1=Date.now()-86400000, j7=Date.now()-7*86400000;
  const gens=[...new Set(JOU.map(e=>e.u).filter(x=>x&&x!=='(non renseigné)'))];
  $('kpis').innerHTML=`<div class="kpis">
    <div class="kpi"><span class="v">${nf(JOU.length)}</span><span class="k">actions enregistrées</span></div>
    <div class="kpi"><span class="v">${nf(JOU.filter(e=>new Date(e.t)>=j1).length)}</span><span class="k">dans les 24 heures</span></div>
    <div class="kpi"><span class="v">${nf(JOU.filter(e=>new Date(e.t)>=j7).length)}</span><span class="k">sur 7 jours</span></div>
    <div class="kpi"><span class="v">${nf(JOU.filter(e=>e.act==='prix').length)}</span><span class="k">changements de prix</span></div>
    <div class="kpi"><span class="v">${nf(gens.length)}</span><span class="k">personne${gens.length>1?'s':''} identifiée${gens.length>1?'s':''}</span></div>
  </div>`;

  if(!JOU.length){
    $('corps').innerHTML=`<div class="vide"><h3>Le journal est vide</h3>
      <p>Il se remplira tout seul. Dès qu'un prix, une quantité ou un statut de comptage change
      dans le catalogue, la ligne est écrite ici avec le nom de la personne, la date et l'heure.</p>
      <p><a class="btn pri" href="catalogue.html">Ouvrir le catalogue</a></p></div>`;
    return;
  }
  if(!L.length){
    $('corps').innerHTML=`<div class="vide"><h3>Aucune action ne correspond</h3>
      <p>Élargis la période ou enlève un filtre.</p></div>`;
    return;
  }
  const v=L.slice(0,vus);
  $('corps').innerHTML=`<div class="wrapx"><table class="tbl"><thead><tr>
    <th class="no">N°</th><th>Quand</th><th>Qui</th><th>Action</th><th>Référence</th><th>Changement</th>
    </tr></thead><tbody>${v.map((x,i)=>ligne(x,i)).join('')}</tbody></table></div>
    ${L.length>vus?`<button class="plus" id="plus">Afficher plus (${nf(L.length-vus)} restantes)</button>`:''}`;
  const b=$('plus'); if(b) b.onclick=()=>{ vus+=60; dessine(); };
  $('src').innerHTML=`${nf(L.length)} action${L.length>1?'s':''} affichée${L.length>1?'s':''}<br>sur ${nf(JOU.length)} au total`;
}

/* liste des personnes */
{
  const g=[...new Set(JOU.map(e=>e.u).filter(Boolean))].sort();
  $('fu').innerHTML='<option value="">Tout le monde</option>'+
    g.map(x=>`<option value="${esc(x)}">${esc(x)}</option>`).join('');
}
['q','fa','fu','fp'].forEach(i=>$(i).addEventListener('input',()=>{ vus=60; dessine(); }));

/* Le journal sert à expliquer un écart six mois plus tard. Ce qui sort doit donc
   dire de quoi il s'agit : le filtre part avec le fichier. */
poseSortie('exp', ()=>{
  const L=filtre();
  const lib=s=>{ const e=$(s); return e.options[e.selectedIndex].textContent; };
  const q=$('q').value.trim();
  return {
    titre:'Journal des actions',
    fichier:'journal-actions',
    filtre:[lib('fp'), $('fa').value?lib('fa'):'toutes les actions',
            $('fu').value?lib('fu'):'tout le monde', q?'recherche « '+q+' »':''].filter(Boolean).join(' · '),
    colonnes:[{t:'Date'},{t:'Heure'},{t:'Qui'},{t:'Rôle'},{t:'Rubrique'},{t:'Action'},
      {t:'Ce qui a été fait'},{t:'Code-barres'},{t:'Référence'},{t:'Avant'},{t:'Après'}],
    lignes:L.map(e=>{ const d=dt(e.t);
      return [d.j,d.h,e.u,RL[e.r]||e.r||'',ou(e),LIBA[acte(e)]||acte(e),
        e.lib||e.champ||'',e.bc||'',e.ref||'',e.det?'':fmt(e.av),e.det?fmt(e.impact):fmt(e.ap)]; })
  };
});

function majUser(){ try{ piedSession(); }catch(e){} }
majUser();
$('sfoot').innerHTML=`${nf(JOU.length)} actions<br>journal local à ce navigateur`;
dessine();
'''

html = coquille("Journal des actions", "Journal",
    "Tout changement de prix, de quantité ou de statut de comptage est écrit ici, "
    "avec la personne, la date et l'heure. Rien ne s'efface.",
    CSS, CORPS, JS)
open('journal.html','w').write(html)
print('journal.html', len(html)//1024, 'Ko')
