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
.a-annulation,.a-suppression{background:var(--crit-soft);color:var(--crit)}
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
.tbl tbody tr.lgn{cursor:pointer}
.tbl tbody tr.lgn:hover td{background:var(--surface-2)}

/* la fenêtre d'explication : une vraie phrase, pas un rappel des colonnes */
.jov{position:fixed;inset:0;background:rgba(20,18,30,.4);display:none;align-items:flex-start;
justify-content:center;padding:6vh 16px;z-index:80;overflow-y:auto}
.jov.on{display:flex}
.jmod{background:var(--surface);border-radius:14px;max-width:640px;width:100%;
box-shadow:0 20px 60px rgba(0,0,0,.25);margin-bottom:6vh}
.jmod .jh{display:flex;align-items:flex-start;gap:12px;padding:20px 24px 14px;border-bottom:1px solid var(--line-2)}
.jmod .jh .act{margin-top:2px}
.jmod .jh .jx{margin-left:auto;background:none;border:0;font-size:20px;line-height:1;color:var(--ink-3);cursor:pointer;padding:2px 6px}
.jmod .jh .jx:hover{color:var(--ink)}
.jmod .jb{padding:18px 24px 22px}
.jmod .phrase{font-size:15px;line-height:1.65;color:var(--ink)}
.jmod .phrase b{font-weight:700}
.jmod .qui{font-size:12.5px;color:var(--ink-3);margin-top:10px}
.jmod .grille{display:grid;grid-template-columns:1fr 1fr;gap:8px 20px;margin-top:16px;padding-top:16px;border-top:1px solid var(--line-2)}
.jmod .grille div{font-size:12.5px;color:var(--ink-3)}
.jmod .grille b{display:block;font-size:13.5px;color:var(--ink);font-weight:600;margin-top:2px}
.jmod .lignes{margin-top:14px;font-size:12.5px}
.jmod .lignes table{width:100%;border-collapse:collapse}
.jmod .lignes th{text-align:left;font-size:10px;text-transform:uppercase;letter-spacing:.08em;
color:var(--ink-3);padding:4px 8px 4px 0;border-bottom:1px solid var(--line-2)}
.jmod .lignes td{padding:5px 8px 5px 0;border-bottom:1px solid var(--line-2)}
.jmod .lignes tr:last-child td{border-bottom:0}
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

<div class="jov" id="jov"><div class="jmod">
  <div class="jh"><span id="j-act"></span><h2 id="j-titre" style="margin:0;font-size:15px;flex:1"></h2><button class="jx" id="j-x">&times;</button></div>
  <div class="jb">
    <div class="phrase" id="j-phrase"></div>
    <div class="qui" id="j-qui"></div>
    <div class="grille" id="j-grille"></div>
    <div class="lignes" id="j-lignes"></div>
  </div>
</div></div>
'''

JS = r'''
const KJOU='crm-journal-v1', KUSR='crm-utilisateur-v1';
let JOU=[]; try{ JOU=JSON.parse(localStorage.getItem(KJOU)||'[]'); }catch(e){ JOU=[]; }
JOU.reverse();                       // le plus récent en haut
let USR=NOM_UTIL;
window.__nomChange.push(v=>{ USR=v; try{ majUser(); }catch(e){} });
let vus=60;

if(typeof _SY_ON!=='undefined'&&_SY_ON){ $('avert-local').hidden=true; $('avert-ligne').hidden=false; }
const LIBA={acces:'Accès',prix:'Prix',stock:'Stock',verif:'Comptage',import:'Import',reception:'Réception',vente:'Vente',annulation:'Annulation',suppression:'Suppression',
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
  return {j:d.toLocaleDateString('en-US',{timeZone:'America/New_York',day:'2-digit',month:'2-digit',year:'2-digit'}),
          h:d.toLocaleTimeString('fr-FR',{timeZone:'America/New_York',hour:'2-digit',minute:'2-digit',second:'2-digit'}),d}; };
const fmt=v=>v==null||v===''?'—':(typeof v==='number'?v.toLocaleString('fr-FR'):String(v));

function filtre(){
  const q=$('q').value.trim().toLowerCase(), a=$('fa').value, u=$('fu').value, p=$('fp').value;
  const lim = p? Date.now()-(+p)*86400000 : 0;
  /* sans le droit de voir les prix d'achat : pas de ligne qui en montre un (3 oct. 2026) */
  const VPA=typeof peut!=='function'||peut('voirPA');
  return JOU.filter(e=>{
    if(!VPA && (e.champ==='pa'||e.act==='fournisseur'||e.act==='reception'||/prix d.achat|facture d.achat|achat fournisseur/i.test(e.lib||''))) return false;
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
       <span class="ap">${e.impact>=0?'+':'−'}${money(Math.abs(e.impact))}</span> de valeur de stock`
    : `<span class="lb">${esc(e.lib||e.champ||'')}</span>
       <span class="av">${esc(fmt(e.av))}</span><span class="fl">→</span><span class="ap">${esc(fmt(e.ap))}</span>`;
  return `<tr class="lgn" data-i="${i||0}" title="Cliquer pour une explication complète">
    <td class="no">${nf((i||0)+1)}</td>
    <td class="qd"><b>${d.j}</b>${d.h}</td>
    <td class="who${e.u&&e.u!=='(non renseigné)'?'':' anon'}">${esc(e.u||'—')}${e.r?`<span class="rl">${esc(RL[e.r]||e.r)}</span>`:''}</td>
    <td><span class="act a-${acte(e)}">${LIBA[acte(e)]||acte(e)}</span>${ou(e)?`<span class="ou">${esc(ou(e))}</span>`:''}</td>
    <td class="ref">${e.ref?(e.bc?`<a class="rlk" href="catalogue.html?q=${encodeURIComponent(e.bc)}" title="Ouvrir dans le catalogue" onclick="event.stopPropagation()"><b>${esc(e.ref)}</b></a>`:`<b>${esc(e.ref)}</b>`):'<b style="color:var(--ink-3)">—</b>'}
      ${e.bc?`<span>${esc(e.bc)}</span>`:''}</td>
    <td class="chg">${chg}</td></tr>`;
}

/* ---------- la fenêtre d'explication : une vraie phrase, pas un rappel des colonnes ----------
   Cliquer sur une ligne ne montrait rien de plus que les cellules du tableau — souvent
   un simple « avant → après » sans dire de quoi il s'agissait vraiment. Igal, 12 sept.
   2026 : « une vraie explication », pas un rappel trop vague de ce qui est déjà affiché. */
let AFF=[];
function explique(e){
  /* Écrite dans la langue de l'écran, d'un seul tenant (Igal, 26 sept. 2026 : « des gens
     qui ne comprennent pas un mot de français ») : la phrase porte des noms et des
     montants au milieu, le dictionnaire mot à mot ne pouvait pas la reconnaître. */
  const d=dt(e.t), a=acte(e);
  const T=x=>{ try{ const v=(typeof lgMot==='function'&&LANG!=='fr')?lgMot(String(x)):null; return v||String(x); }catch(_){ return String(x); } };
  const qui = e.u && e.u!=='(non renseigné)' ? e.u : L3('quelqu\'un sans nom déclaré','someone with no declared name','alguien sin nombre declarado');
  const role = e.r ? ' ('+T(RL[e.r]||e.r)+')' : '';
  const rub = ou(e) ? T(ou(e)) : '';
  const rubrique = rub ? L3(' dans ',' in ',' en ')+rub : '';
  const refTxt = e.ref ? (e.bc ? `${e.ref} (${L3('code-barres','barcode','código de barras')} ${e.bc})` : e.ref) : '';
  const avap = (av,ap) => `<b>${esc(T(fmt(av)))}</b> → <b>${esc(T(fmt(ap)))}</b>`;
  const Q=`<b data-nolang>${esc(qui)}</b>${role}`, LIB=`<b data-nolang>${esc(T(e.lib||e.champ||''))}</b>`;
  const n=e.n, pl=n>1;
  let phrase;
  if(a==='prix')
    phrase = Q+L3(' a changé le prix',' changed the price',' cambió el precio')+(refTxt?L3(' de ',' of ',' de ')+`<b data-nolang>${esc(refTxt)}</b>`:'')+rubrique+' : '+avap(e.av,e.ap)+'.';
  else if(a==='import'||a==='reception'||a==='vente'||a==='annulation')
    phrase = Q+L3(' a enregistré : ',' recorded: ',' registró: ')+LIB
      +(n!=null?', '+nf(n)+' '+L3('référence'+(pl?'s':'')+' concernée'+(pl?'s':''),'reference'+(pl?'s':'')+' concerned','referencia'+(pl?'s':'')+' afectada'+(pl?'s':'')):'')
      +rubrique+', '+(e.impact>=0?L3('ajoutant','adding','añadiendo'):L3('retirant','removing','retirando'))
      +` <b>${money(Math.abs(e.impact||0))}</b> `+L3('de valeur de stock.','of stock value.','de valor de stock.')
      +(e.note?` <span data-nolang>${esc(T(e.note))}</span>`:'');
  else if(a==='ajustement'||a==='stock')
    phrase = Q+L3(' a fait un ajustement de stock',' made a stock adjustment',' hizo un ajuste de stock')+(refTxt?L3(' sur ',' on ',' en ')+`<b data-nolang>${esc(refTxt)}</b>`:'')+rubrique+' : '+LIB
      +(n!=null?', '+nf(n)+' '+L3('flacon'+(pl?'s':'')+' concerné'+(pl?'s':''),'bottle'+(pl?'s':'')+' concerned','frasco'+(pl?'s':'')+' afectado'+(pl?'s':'')):'')
      +(e.impact!=null?', '+(e.impact>=0?L3('plus','plus','más'):L3('moins','minus','menos'))+' '+money(Math.abs(e.impact))+' '+L3('de valeur de stock','of stock value','de valor de stock'):'')+'.';
  else if(a==='acces')
    phrase = `<b data-nolang>${esc(qui)}</b> : ${LIB}`+(e.ref?' — '+L3('compte','account','cuenta')+` <b data-nolang>${esc(e.ref)}</b>`:'')+'.'
      + (e.av!=null||e.ap!=null ? ' '+(e.av!=null?L3('Avant','Before','Antes')+` : <b data-nolang>${esc(T(fmt(e.av)))}</b>. `:'')+(e.ap!=null?L3('Après','After','Después')+` : <b data-nolang>${esc(T(fmt(e.ap)))}</b>.`:'') : '');
  else if(a==='reglage')
    phrase = Q+L3(' a changé un réglage',' changed a setting',' cambió un ajuste')+rubrique+' : '+LIB+' — '+avap(e.av,e.ap)+'.';
  else if(e.av!=null||e.ap!=null)
    phrase = Q+' : '+LIB+(refTxt?` — ${esc(refTxt)}`:'')+rubrique+' : '+avap(e.av,e.ap)+'.';
  else
    phrase = Q+' : '+LIB+(refTxt?` — ${esc(refTxt)}`:'')+rubrique+'.';
  return {phrase:`<span data-nolang>${phrase}</span>`,d,a};
}
function ouvreExplication(e){
  const {phrase,d,a}=explique(e);
  $('j-act').innerHTML=`<span class="act a-${a}">${LIBA[a]||a}</span>`;
  $('j-titre').textContent='';
  $('j-phrase').innerHTML=phrase;
  $('j-qui').textContent=L3(`Le ${d.j} à ${d.h}`,`On ${d.j} at ${d.h}`,`El ${d.j} a las ${d.h}`);
  $('j-grille').innerHTML=[
    ['Quand', L3(`${d.j} à ${d.h}`,`${d.j} at ${d.h}`,`${d.j} a las ${d.h}`)],
    ['Qui', (e.u&&e.u!=='(non renseigné)'?e.u:'—')+(e.r?' · '+((typeof lgMot==='function'&&lgMot(RL[e.r]||e.r))||RL[e.r]||e.r):'')],
    ['Rubrique', ou(e)?((typeof lgMot==='function'&&lgMot(ou(e)))||ou(e)):'—'],
    ['Référence', e.ref?(e.ref+(e.bc?' · '+e.bc:'')):'—'],
  ].map(([k,v])=>`<div>${k}<b data-nolang>${esc(v)}</b></div>`).join('');
  $('j-lignes').innerHTML = (e.det&&e.det.length)
    ? `<table><thead><tr><th>Référence</th><th>Avant</th><th>Après</th></tr></thead><tbody>${
        e.det.map(x=>`<tr><td data-nolang>${esc(x.ref)}</td><td data-nolang>${esc(x.av)}</td><td data-nolang><b>${esc(x.ap)}</b></td></tr>`).join('')}</tbody></table>`
    : '';
  $('jov').classList.add('on');
}
$('j-x').onclick=()=>$('jov').classList.remove('on');
$('jov').addEventListener('click',e=>{ if(e.target.id==='jov') $('jov').classList.remove('on'); });
$('corps').addEventListener('click',e=>{
  const tr=e.target.closest('tr.lgn'); if(!tr) return;
  const x=AFF[+tr.dataset.i]; if(x) ouvreExplication(x);
});

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
  const v=L.slice(0,vus); AFF=v;
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
/* LE FIL EN DIRECT (1er oct. 2026) : une action faite sur un autre poste apparaît ici dans la
   seconde, sans recharger */
window.__rafraichir=()=>{ const y=window.scrollY; try{ JOU=JSON.parse(localStorage.getItem(KJOU)||'[]'); }catch(e){} try{ dessine(); }catch(e){} window.scrollTo(0,y); };
window.addEventListener('ck-maj',e=>{ try{ if((e.detail&&e.detail.cles||[]).includes(KJOU) && _syPageCalme()) window.__rafraichir(); }catch(_){} });
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
