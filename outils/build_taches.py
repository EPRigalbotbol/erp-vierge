# -*- coding: utf-8 -*-
"""Rubrique « Tâches » (Igal, 3 nov. 2026).

« Une rubrique en dessous de Tableau de bord, Tâches à planifier. Je veux que cet agent puisse donner à Sam les
informations importantes et que ça lui mette une liste de tâches à exécuter. Il pourra valider la tâche et faire le
nécessaire, ignorer la tâche — qu'elle se mette en dessous — ou mettre en attente (rappel demain, dans 2, 5, 10 jours).
Sinon elle reste dans la liste. Je veux qu'il soit vraiment le bras droit de Sam. »

Les tâches sont calculées par le cockpit (cockpit/galou.js, tachesBrutes) à partir des faits de l'ERP — jamais par l'IA.
Cette page les montre et enregistre ce que Sam en fait (état partagé entre les postes). Galou (la fenêtre) lit la même
liste. Réservée à qui voit les marges, comme le tableau de bord.
"""
from build_crm import coquille

CSS = r"""
.mur{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:34px 32px;max-width:640px;margin:26px auto}
.mur h2{margin:0 0 10px;font-size:20px;font-weight:700;letter-spacing:-.015em}
.mur p{margin:0;color:var(--ink-2);font-size:14.5px;line-height:1.65}
.tk-tete{display:flex;gap:14px;flex-wrap:wrap;align-items:center;margin:0 0 18px}
.tk-kpi{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:12px 16px;min-width:150px}
.tk-kpi b{display:block;font-family:Inter,sans-serif;font-size:24px;font-weight:800;letter-spacing:-.03em;line-height:1.1}
.tk-kpi span{font-size:12.5px;color:var(--ink-3)}
.tk-kpi.hot b{color:var(--crit)}
.tk-maj{margin-left:auto;font-size:12.5px;color:var(--ink-3)}
h2.sec{font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:var(--ink);font-weight:700;margin:30px 0 12px;padding-bottom:9px;border-bottom:1px solid var(--line);display:flex;justify-content:space-between;align-items:baseline;gap:12px;flex-wrap:wrap}
h2.sec em{font-style:normal;font-size:12.5px;letter-spacing:0;text-transform:none;color:var(--ink-3);font-weight:400}
.tk{background:var(--surface);border:1px solid var(--line);border-left:4px solid var(--line);border-radius:12px;padding:13px 16px;margin:0 0 10px;display:grid;grid-template-columns:1fr auto;gap:8px 16px;align-items:start}
.tk.haute{border-left-color:var(--crit)} .tk.normale{border-left-color:var(--warn)}
.tk.attente{border-left-color:var(--ink-3);opacity:.85} .tk.ignoree{border-left-color:var(--line);opacity:.7}
.tk h3{margin:0 0 3px;font-size:15px;font-weight:700;letter-spacing:-.01em}
.tk h3 .pt{display:inline-block;font-size:10px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:var(--crit);background:var(--crit-soft,#FBE5E6);padding:2px 7px;border-radius:99px;margin-left:8px;vertical-align:middle}
.tk h3 .pt.rev{color:var(--iris);background:var(--iris-soft)}
.tk p{margin:0;font-size:13.5px;color:var(--ink-2);line-height:1.5}
.tk small{display:block;margin-top:4px;font-size:12px;color:var(--ink-3)}
.tk-a{display:flex;gap:6px;flex-wrap:wrap;justify-content:flex-end;align-items:center}
.tk-a a,.tk-a button,.tk-a select{font-family:inherit;font-size:12.5px;font-weight:600;border:1px solid var(--line);background:var(--surface);color:var(--ink-2);border-radius:8px;padding:6px 10px;cursor:pointer;text-decoration:none;white-space:nowrap}
.tk-a a.pri,.tk-a button.pri{background:var(--iris);border-color:var(--iris);color:#fff}
.tk-a button:hover,.tk-a a:hover{border-color:var(--iris);color:var(--iris)} .tk-a a.pri:hover,.tk-a button.pri:hover{color:#fff;filter:brightness(1.08)}
.tk-a select{color:var(--ink-2)}
.tk-vide{background:var(--surface);border:1px dashed var(--line);border-radius:12px;padding:22px;text-align:center;color:var(--ink-3);font-size:14px}
.tk-vide b{display:block;color:var(--good);font-size:16px;margin-bottom:4px}
details.tk-ign summary{cursor:pointer;color:var(--ink-3);font-size:13px;font-weight:600;margin:24px 0 10px}
@media(max-width:700px){.tk{grid-template-columns:1fr}.tk-a{justify-content:flex-start}}
"""

CORPS = r"""
<div class="tk-tete" id="tk-tete"></div>
<div id="tk-corps"><div class="tk-vide" id="tk-att">Galou regarde ce qu'il y a à faire…</div></div>
"""

JS = r"""
/* ---------- la rubrique Tâches : la liste du cockpit, et ce que Sam en fait ---------- */
let TK=null, TK_ENV=false;
const tkT=(fr,en,es)=>typeof L3==='function'?L3(fr,en,es):fr;
const tkPeut=()=>{ try{ return location.protocol!=='file:' && !!ckTok(); }catch(e){ return false; } };
async function tkApi(chemin,corps){
  const r=await fetch(CK_URL+'/api/o/'+CK_ORG+'/galou/taches'+chemin,{method:corps===undefined?'GET':'POST',headers:{'Content-Type':'application/json',Authorization:'Bearer '+ckTok()},body:corps===undefined?undefined:JSON.stringify(corps)});
  const j=await r.json().catch(()=>({})); if(!r.ok) throw new Error(j.erreur||('serveur '+r.status)); return j;
}
const tkDate=iso=>{ if(!iso) return ''; const [Y,M,D]=String(iso).slice(0,10).split('-'); return `${M}/${D}/${String(Y).slice(2)}`; };
const TYPES={rupture:['Réassort','Restock','Reposición'],manque:['Réassort','Restock','Reposición'],prix:['Prix','Price','Precio'],enligne:['Mise en ligne','Listing','Publicación'],pcshopify:['Perfume City','Perfume City','Perfume City'],publication:['Mise en ligne','Listing','Publicación'],expedier:['Expédition','Shipping','Envío'],completer:['Ventes','Sales','Ventas']};
function tkLigne(t){
  const typ=TYPES[t.type]?tkT(...TYPES[t.type]):t.type;
  const rappel=`<select data-rappel="${esc(t.id)}" title="${tkT('Me le rappeler plus tard','Remind me later','Recordármelo más tarde')}"><option value="">${tkT('Plus tard…','Later…','Más tarde…')}</option>${(TK.rappels||[1,2,5,10]).map(n=>`<option value="${n}">${n===1?tkT('demain','tomorrow','mañana'):tkT(`dans ${n} jours`,`in ${n} days`,`en ${n} días`)}</option>`).join('')}</select>`;
  let actions='';
  /* 3 nov. 2026 (Igal : « quand j'appuie sur Faire, je veux rester sur la même page ») : un parfum s'ouvre dans sa fiche,
     par-dessus la liste (ficheFenetre, _fusion.py) ; une page de l'ERP s'ouvre dans un nouvel onglet. La liste est relue à la fermeture. */
  const ouvre=cls=>t.cle?`<button class="${cls}" data-fiche="${esc(t.cle)}" data-plus="${t.type==='publication'?'&canaux=1':''}">${cls==='pri'?tkT('Faire','Do it','Hacerlo'):tkT('Ouvrir','Open','Abrir')} →</button>`
                        :`<a class="${cls}" href="${esc(t.lien||'#')}" target="_blank" rel="noopener">${cls==='pri'?tkT('Faire','Do it','Hacerlo'):tkT('Ouvrir','Open','Abrir')} ↗</a>`;
  if(t.etat==='a_faire') actions=`${ouvre('pri')}<button data-etat="faite" data-id="${esc(t.id)}">${tkT('Fait','Done','Hecho')} ✓</button>${rappel}<button data-etat="ignoree" data-id="${esc(t.id)}">${tkT('Ignorer','Ignore','Ignorar')}</button>`;
  else if(t.etat==='attente') actions=`${ouvre('')}<button data-etat="a_faire" data-id="${esc(t.id)}">${tkT('Remettre dans la liste','Put back in the list','Volver a la lista')}</button><button data-etat="ignoree" data-id="${esc(t.id)}">${tkT('Ignorer','Ignore','Ignorar')}</button>`;
  else actions=`${ouvre('')}<button data-etat="a_faire" data-id="${esc(t.id)}">${tkT('Remettre dans la liste','Put back in the list','Volver a la lista')}</button>`;
  const pt=t.etat==='a_faire'?(t.urgence==='haute'?`<span class="pt">${tkT('urgent','urgent','urgente')}</span>`:'')+(t.revenue?`<span class="pt rev">${tkT('revenue','back','de vuelta')}</span>`:''):'';
  const sous=t.etat==='attente'?`<small>${tkT('Rappel le','Reminder on','Recordatorio el')} <span data-nolang>${tkDate(t.jusqua)}</span></small>`:t.etat==='ignoree'?`<small>${tkT('Ignorée le','Ignored on','Ignorada el')} <span data-nolang>${tkDate(t.depuis)}</span></small>`:'';
  return `<div class="tk ${t.etat==='a_faire'?t.urgence:t.etat}" data-tk="${esc(t.id)}"><div><h3><span data-nolang>${esc(t.titre)}</span>${pt}</h3><p data-nolang>${esc(t.detail||'')}</p>${sous}<small>${typ}</small></div><div class="tk-a" data-titre="${esc(t.titre)}">${actions}</div></div>`;
}
function tkPeint(){
  const z=$('tk-corps'), h=$('tk-tete'); if(!TK) return;
  const n=TK.a_faire.length;
  h.innerHTML=`<div class="tk-kpi ${TK.urgentes?'hot':''}"><b>${nf(TK.urgentes)}</b><span>${tkT('urgentes','urgent','urgentes')}</span></div>
    <div class="tk-kpi"><b>${nf(n)}</b><span>${tkT('à faire','to do','por hacer')}</span></div>
    <div class="tk-kpi"><b>${nf(TK.attente.length)}</b><span>${tkT('en attente','waiting','en espera')}</span></div>
    <div class="tk-maj">${tkT('Galou relit l\'ERP à chaque ouverture de cette page.','Galou re-reads the ERP each time this page opens.','Galou relee el ERP cada vez que se abre esta página.')}</div>`;
  let s=`<h2 class="sec">${tkT('À faire','To do','Por hacer')} <em>${tkT('les plus urgentes en premier · une tâche disparaît toute seule quand le problème n\'existe plus','most urgent first · a task goes away by itself once the problem is gone','las más urgentes primero · una tarea desaparece sola cuando el problema ya no existe')}</em></h2>`;
  s+=n?TK.a_faire.map(tkLigne).join(''):`<div class="tk-vide"><b>${tkT('Rien à faire pour l\'instant','Nothing to do right now','Nada que hacer por ahora')}</b>${tkT('Galou te dira dès qu\'il y a quelque chose.','Galou will tell you as soon as there is something.','Galou te avisará en cuanto haya algo.')}</div>`;
  if(TK.attente.length) s+=`<h2 class="sec">${tkT('En attente','Waiting','En espera')} <em>${tkT('elles reviendront dans la liste à la date du rappel','they will come back to the list on the reminder date','volverán a la lista en la fecha del recordatorio')}</em></h2>`+TK.attente.map(tkLigne).join('');
  if(TK.ignorees.length) s+=`<details class="tk-ign"><summary>${tkT(`${nf(TK.ignorees.length)} tâche${TK.ignorees.length>1?'s':''} ignorée${TK.ignorees.length>1?'s':''}`,`${nf(TK.ignorees.length)} ignored task${TK.ignorees.length>1?'s':''}`,`${nf(TK.ignorees.length)} tarea${TK.ignorees.length>1?'s':''} ignorada${TK.ignorees.length>1?'s':''}`)}</summary>`+TK.ignorees.map(tkLigne).join('')+'</details>';
  z.innerHTML=s;
  z.querySelectorAll('button[data-etat]').forEach(b=>b.onclick=()=>tkStatue(b.dataset.id,b.dataset.etat,undefined,b.closest('.tk-a').dataset.titre));
  z.querySelectorAll('button[data-fiche]').forEach(b=>b.onclick=()=>{ if(typeof ficheFenetre!=='function'){ window.open('catalogue.html#cle='+encodeURIComponent(b.dataset.fiche),'_blank'); return; }
    ficheFenetre(b.dataset.fiche,()=>{ const y=window.scrollY; tkCharge().then(()=>window.scrollTo(0,y)); },b.dataset.plus||''); });
  z.querySelectorAll('select[data-rappel]').forEach(sl=>sl.onchange=()=>{ if(sl.value) tkStatue(sl.dataset.rappel,'attente',+sl.value,sl.closest('.tk-a').dataset.titre); });
  const c=document.getElementById('ct-taches'); if(c){ c.textContent=n?String(n):''; c.className=n?'ct nb':'ct'; }
}
async function tkStatue(id,etat,jours,titre){
  if(TK_ENV) return; TK_ENV=true;
  try{ await tkApi('/etat',{id,etat,jours,titre}); await tkCharge(); }
  catch(e){ alert(tkT('Pas enregistré : ','Not saved: ','No guardado: ')+(e&&e.message||e)); }
  TK_ENV=false;
}
async function tkCharge(){
  try{ TK=await tkApi(''); tkPeint(); }
  catch(e){ $('tk-corps').innerHTML=`<div class="tk-vide">${tkT('Galou ne répond pas : ','Galou is not answering: ','Galou no responde: ')}${esc(e&&e.message||String(e))}</div>`; }
}
(function(){
  const s=session(); if(!s) return;
  if(!peut('voirMarge')){
    document.querySelector('.wrap').insertAdjacentHTML('beforeend',`<div class="mur"><h2>${tkT('Cette rubrique n\'est pas pour ce rôle','This section is not for this role','Esta sección no es para este rol')}</h2><p>${tkT('Les tâches parlent de prix d\'achat et de marges, et ce rôle ne les voit pas.','The tasks mention purchase prices and margins, and this role does not see them.','Las tareas hablan de precios de compra y márgenes, y este rol no los ve.')}</p></div>`);
    $('tk-tete').remove(); $('tk-corps').remove(); return;
  }
  if(!tkPeut()){ $('tk-corps').innerHTML=`<div class="tk-vide">${tkT('Il faut être connecté à l\'ERP en ligne pour voir les tâches.','You need to be signed in to the online ERP to see the tasks.','Hay que estar conectado al ERP en línea para ver las tareas.')}</div>`; return; }
  tkCharge();
})();
"""

html = coquille("Tâches", "Tâches",
    "Ce que Galou te demande de faire aujourd'hui, trouvé dans l'ERP : parfums à recommander, prix à vérifier, mises en ligne, Perfume City, expéditions. Fais, ignore, ou demande un rappel.",
    CSS, CORPS, JS, donnees=('produits',))
open('taches.html', 'w').write(html)
print('taches.html', len(html)//1024, 'Ko')
