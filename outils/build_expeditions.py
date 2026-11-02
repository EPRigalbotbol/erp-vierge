# -*- coding: utf-8 -*-
"""Rubrique « Expéditions » : les commandes qui doivent partir, et qui n'ont pas
encore été marquées « expédiée ».

Igal, 24 sept. 2026 : « sur certains canaux il doit y avoir une livraison. Ça reste
en attente tant qu'une personne de chez Sam n'a pas statué la commande. C'est
seulement quand elle a dit "envoyée ce jour" que le déstock doit être fait. »

Donc : une commande du site ou d'Amazon arrive ici sans toucher au stock. Le geste
« expédiée le … » fait la facture et sort les flacons — pas avant. Une commande
annulée par le canal avant ce geste disparaît simplement : rien n'était sorti.
La mécanique (faExpedier, faRetireExp) vit dans _file_auto.py, partagée avec
l'enregistrement automatique ; cette page ne fait que la montrer.
"""
from build_crm import coquille

CSS = r"""
.stw{display:inline-block;padding:2px 9px;border-radius:999px;font-size:12.5px;font-weight:700;background:var(--surface-2);color:var(--ink-2)}
.stw.st-processing,.stw.st-on-hold{background:#FFF3D6;color:#8A5A00}
.stw.st-completed,.stw.st-shipped{background:#E3F4EA;color:#1E6B45}
.stw.st-cancelled,.stw.st-refunded,.stw.st-failed{background:#FBE5E6;color:#A4262C}
.stw.na{background:transparent;color:var(--ink-3)}

.tete{font-size:14px;color:var(--ink-2);line-height:1.6;max-width:84ch;margin:0 0 16px}
.tete b{color:var(--ink)}
.kp{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:12px;margin:0 0 18px}
.kp div{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:14px 16px}
.kp b{display:block;font-family:Inter,sans-serif;font-size:24px;font-weight:800;letter-spacing:-.03em;line-height:1.1}
.kp span{font-size:12.5px;color:var(--ink-3)}
.kp .tard b{color:var(--warn)}
h2.sec{font-size:17px;font-weight:800;letter-spacing:-.01em;margin:26px 0 10px;display:flex;align-items:center;gap:10px}
/* l'ordre de la liste (Igal, 25 sept. 2026 : « pas de filtre croissant / décroissant,
   et les premières de la liste doivent être les dernières reçues ») */
.tri{font:600 12.5px Inter,sans-serif;color:var(--ink-2);background:var(--surface);border:1px solid var(--line);
border-radius:8px;padding:5px 11px;cursor:pointer;letter-spacing:0;text-transform:none}
.tri:hover{border-color:var(--iris);color:var(--iris)}
.bloc th.tr{cursor:pointer;user-select:none}.bloc th.tr:hover{color:var(--iris)}
h2.sec .n{font-family:Inter,sans-serif;font-size:11px;font-weight:800;letter-spacing:.06em;text-transform:uppercase;
background:var(--iris-soft);color:var(--iris);padding:3px 9px;border-radius:99px}
.bloc{background:var(--surface);border:1px solid var(--line);border-radius:12px;overflow:hidden}
.bloc table{width:100%;border-collapse:collapse;font-size:13.5px}
.bloc th{text-align:left;font-family:Inter,sans-serif;font-size:10.5px;letter-spacing:.09em;text-transform:uppercase;
color:var(--ink);font-weight:800;padding:9px 14px;background:var(--surface-2);border-bottom:1px solid var(--line)}
.bloc td{padding:10px 14px;border-top:1px solid var(--line-2);vertical-align:top;line-height:1.45}
.bloc tr:first-child td{border-top:0}
.bloc td.r,.bloc th.r{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
.bloc tr.ex{cursor:pointer}
.bloc tr.ex:hover td{background:var(--iris-soft)}
.src{display:inline-block;padding:2px 8px;border-radius:99px;font:700 10.5px Inter,sans-serif;background:var(--surface-2);color:var(--ink-2);white-space:nowrap}
.lg{display:block;font-size:12px;color:var(--ink-3);margin-top:2px;line-height:1.45}
.dj{font-family:Inter,sans-serif;font-weight:700;white-space:nowrap}
.dj.tard{color:var(--warn)} .dj.tres{color:var(--crit)}
.vide{padding:26px 18px;color:var(--ink-3);font-size:13.5px;line-height:1.6;text-align:center}
.vide b{color:var(--ink)}
.btn.sm{padding:5px 10px;font-size:12.5px}
.canaux{display:flex;flex-wrap:wrap;gap:10px 18px;padding:12px 16px;font-size:13.5px;color:var(--ink-2)}
.canaux label{display:flex;align-items:center;gap:7px;cursor:pointer}
.canaux input{width:16px;height:16px;accent-color:var(--iris)}
.canaux .fix{color:var(--ink-3)}
.pied{font-size:13px;color:var(--ink-2);line-height:1.65;max-width:84ch;margin-top:22px}
.pied a{color:var(--iris)}
.info{background:var(--good-soft);border:1px solid var(--good);border-radius:9px;padding:11px 14px;font-size:13.5px;line-height:1.55;margin:0 0 14px;color:var(--ink)}
.info.warn{background:var(--warn-soft);border-color:var(--warn)}
.info a{color:var(--iris)}

/* la fiche d'une commande */
.dov{position:fixed;inset:0;background:rgba(23,23,29,.42);z-index:85;display:none}
body:has(.dov.on) #svtem{display:none!important}
.dov.on{display:block}
.dt{position:absolute;top:0;right:0;bottom:0;width:min(580px,100%);background:var(--surface);
border-left:1px solid var(--line);box-shadow:-14px 0 46px rgba(0,0,0,.20);display:flex;flex-direction:column;overflow:hidden}
.dt .dh{padding:15px 20px;border-bottom:1px solid var(--line);display:flex;gap:12px;align-items:flex-start}
.dt .dh h3{margin:0;font-size:18px;font-weight:800;letter-spacing:-.02em;flex:1;line-height:1.25}
.dt .dh .sub{display:block;font-family:Inter,sans-serif;font-size:11.5px;font-weight:500;color:var(--ink-3);margin-top:4px;line-height:1.5}
.dt .dh .x{background:none;border:1px solid var(--line);border-radius:7px;font-size:17px;color:var(--ink-2);cursor:pointer;line-height:1;padding:5px 10px;flex:none}
.dt .db{padding:2px 20px 24px;overflow-y:auto;flex:1}
.dt .df{padding:12px 20px;border-top:1px solid var(--line);background:var(--surface-2);display:flex;gap:8px;flex-wrap:wrap;align-items:center}
.blo{margin-top:19px}
.blo>h4{margin:0 0 7px;font-family:Inter,sans-serif;font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--ink);font-weight:800}
.blo table{width:100%;border-collapse:collapse;font-size:13px}
.blo td{padding:6px 5px;border-bottom:1px solid var(--line-2);vertical-align:top;line-height:1.4}
.blo td.r{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
.blo td small{display:block;font-size:11px;color:var(--ink-3)}
.blo tr:last-child td{border-bottom:0}
.pl{display:flex;justify-content:space-between;gap:14px;padding:5px 0;font-size:13.5px;border-bottom:1px solid var(--line-2)}
.pl span{color:var(--ink-2)} .pl b{font-variant-numeric:tabular-nums;white-space:nowrap}
.pl:last-child{border-bottom:0}
.pl.gr{padding-top:8px;font-weight:800;font-size:15px} .pl.gr span{color:var(--ink)}
.et{display:inline-block;padding:2px 9px;border-radius:99px;font-family:Inter,sans-serif;font-size:10.5px;font-weight:800;letter-spacing:.05em;text-transform:uppercase;vertical-align:middle}
.et.att{background:var(--warn-soft);color:var(--warn)}
.et.ok{background:var(--good-soft);color:var(--good)}
.nt{font-size:12.5px;color:var(--ink-3);line-height:1.55;margin:7px 0 0}
.frm{display:grid;grid-template-columns:1fr 1fr;gap:10px 12px}
.frm label{display:flex;flex-direction:column;gap:4px;font-size:12px;color:var(--ink-2);font-family:Inter,sans-serif;font-weight:600}
.frm input{font:inherit;font-size:14px;padding:8px 10px;border:1px solid var(--line);border-radius:8px;background:var(--surface)}
.frm .w{grid-column:1/-1}
.blo.exp{background:var(--iris-soft);border-radius:10px;padding:12px 14px}
.stk{color:var(--crit);font-weight:600}
@media(max-width:700px){ .dt{width:100%;border-left:0} .dt .db{padding:2px 16px 22px} .frm{grid-template-columns:1fr} }
"""

CORPS = r"""
<p class="tete" id="tete"></p>
<div id="msg"></div>
<div class="kp" id="kp"></div>
<h2 class="sec">À expédier <span class="n" id="n-att">0</span><span style="flex:1"></span><button class="tri" id="tri" title="Changer l'ordre de la liste"></button></h2>
<div class="bloc" id="att"></div>
<h2 class="sec">Expédiées <span class="n">30 derniers jours</span></h2>
<div class="bloc" id="fait"></div>
<h2 class="sec">Quels canaux passent par ici</h2>
<div class="bloc"><div class="canaux" id="canaux"></div></div>
<p class="pied" id="pied"></p>

<div class="dov" id="dov"><div class="dt">
  <div class="dh"><h3 id="d-tit">—</h3><button class="x" id="d-x" title="Fermer">✕</button></div>
  <div class="db" id="d-corps"></div>
  <div class="df" id="d-pied"></div>
</div></div>
"""

JS = r"""
const KEXP='expeditions-v1', KREG='reglages-v1';
const SRC={woocommerce:'Site perfumestrade.com','woocommerce-gros':'Site wholesale.perfumestrade.com',lightspeed:'Caisse Lightspeed',shopify:'Shopify',amazon:'Amazon',message:'Commande par message'};
const SRC_C={woocommerce:'Site','woocommerce-gros':'Site gros',lightspeed:'Caisse',shopify:'Shopify',amazon:'Amazon',message:'Message client'};
const dfr=d=>{ if(!d) return '—'; const m=String(d).match(/^(\d{4})-(\d\d)-(\d\d)/); return m?`${m[2]}/${m[3]}/${m[1].slice(2)}`:String(d); };
const jours=d=>{ if(!d) return 0; const a=new Date(String(d).slice(0,10)+'T12:00:00'), b=new Date(ajd()+'T12:00:00'); return Math.max(0,Math.round((b-a)/86400000)); };
let CTX=null; const ctx=()=>{ if(!CTX) CTX=faContexte(); return CTX; };
let DETAIL=null;
let SENS='desc'; try{ if(localStorage.getItem('expeditions-tri')==='asc') SENS='asc'; }catch(e){}
function inverseTri(){ SENS=SENS==='asc'?'desc':'asc'; try{ localStorage.setItem('expeditions-tri',SENS); }catch(e){} peint(); }

/* la veille du serveur redessine sur place quand des commandes arrivent (voir _serveur.py) */
window.__rafraichir=()=>{ const y=window.scrollY; peint(); window.scrollTo(0,y); };
/* 28 sept. (Igal) : le statut écrit sur WooCommerce, sur chaque commande — tel quel
   (processing, completed, on-hold…), c'est le mot que Sam voit dans WooCommerce */
function stSite(e){
  const s=(typeof faStatutSite==='function')?faStatutSite(e.src,e.num):null;
  if(!/^woocommerce/.test(String(e.src||''))) return '<span class="stw na">—</span>';
  if(!s) return '<span class="stw na" title="Pas encore relu sur le site (le cockpit le relit toutes les 5 minutes)">?</span>';
  return `<span class="stw st-${esc(s.st)}" data-nolang title="Statut de la commande sur WooCommerce">${esc(s.st)}</span>`;
}
function peint(){
  const E=faLitExp();
  /* par défaut, la dernière commande reçue en haut ; un clic inverse (retenu sur cet appareil) */
  const cle=e=>String(e.d||'')+' '+String(e.h||'').padStart(5,'0')+' '+String(e.arrive||'');
  const att=E.filter(e=>e.statut==='attente').sort((a,b)=>SENS==='asc'?cle(a).localeCompare(cle(b)):cle(b).localeCompare(cle(a)));
  $('tri').textContent=SENS==='asc'?'↑ Plus anciennes d\'abord':'↓ Plus récentes d\'abord';
  const lim=new Date(Date.now()-30*86400000).toISOString();
  const fait=E.filter(e=>e.statut==='expedie'&&e.exp&&(e.exp.t||'')>=lim).sort((a,b)=>String(b.exp.t||'').localeCompare(String(a.exp.t||'')));
  const tard=att.filter(e=>jours(e.d)>=2).length, mt=att.reduce((a,e)=>a+(e.montant||0),0);
  $('n-att').textContent=nf(att.length);
  $('kp').innerHTML=`<div><b>${nf(att.length)}</b><span>commande${att.length>1?'s':''} à expédier</span></div>
    <div class="${tard?'tard':''}"><b>${nf(tard)}</b><span>depuis 2 jours ou plus</span></div>
    <div><b>${money(mt)}</b><span>en attente de départ — pas encore sorti du stock</span></div>
    <div><b>${nf(fait.length)}</b><span>expédiée${fait.length>1?'s':''} ces 30 derniers jours</span></div>`;
  if(!att.length) $('att').innerHTML=`<div class="vide"><b>Rien à expédier.</b><br>Les commandes du site et d'Amazon apparaîtront ici dès leur arrivée, avant de toucher au stock.</div>`;
  else $('att').innerHTML=`<table><thead><tr><th class="tr" data-tri="1" title="Changer l'ordre">Commandée ${SENS==='asc'?'▲':'▼'}</th><th>D'où</th><th>N°</th><th>Client</th><th>Contenu</th><th>Statut sur le site</th><th class="r">Montant</th><th class="r">Depuis</th><th class="r"></th></tr></thead><tbody>
    ${att.map(e=>{ const j=jours(e.d); return `<tr class="ex" data-id="${esc(e._i)}" title="Cliquer pour voir la commande en entier">
      <td>${dfr(e.d)}${e.h?`<span class="lg">${esc(e.h)}</span>`:''}</td>
      <td><span class="src">${esc(SRC_C[e.src]||e.src||'')}</span></td>
      <td class="nm">${esc(e.num||'—')}</td>
      <td class="nm">${esc(faNomClient(e.client)||(e.src==='amazon'?'acheteur Amazon':'—'))}</td>
      <td>${nf(e.lignes.length)} parfum${e.lignes.length>1?'s':''}<span class="lg nm">${e.lignes.slice(0,3).map(l=>esc(l.ref||l.des)+' ×'+l.q).join(' · ')}${e.lignes.length>3?' …':''}</span></td>
      <td>${stSite(e)}</td>
      <td class="r">${money2(e.montant)}</td>
      <td class="r"><span class="dj ${j>=4?'tres':j>=2?'tard':''}">${j===0?"aujourd'hui":j===1?'hier':nf(j)+' jours'}</span></td>
      <td class="r"><button class="btn sm pri" data-exp="${esc(e._i)}">Expédiée…</button></td>
    </tr>`; }).join('')}</tbody></table>`;
  if(!fait.length) $('fait').innerHTML=`<div class="vide">Aucune expédition ces 30 derniers jours.</div>`;
  else $('fait').innerHTML=`<table><thead><tr><th>Expédiée le</th><th>Par</th><th>D'où</th><th>N°</th><th>Client</th><th>Contenu</th><th>Suivi</th><th>Statut</th><th class="r">Montant</th></tr></thead><tbody>
    ${fait.slice(0,60).map(e=>`<tr class="ex" data-id="${esc(e._i)}" title="Cliquer pour voir la commande en entier">
      <td><b>${dfr(e.exp.d)}</b>${jours(e.exp.d)!==jours(e.d)?`<span class="lg">commandée le ${dfr(e.d)}</span>`:''}</td>
      <td class="nm">${esc(e.exp.par||'')}</td>
      <td><span class="src">${esc(SRC_C[e.src]||e.src||'')}</span></td>
      <td class="nm">${esc(e.num||'—')}</td>
      <td class="nm">${esc(faNomClient(e.client)||(e.src==='amazon'?'acheteur Amazon':'—'))}</td>
      <td class="nm">${e.lignes.slice(0,3).map(l=>esc(l.ref||l.des)+' ×'+l.q).join(' · ')}${e.lignes.length>3?' …':''}</td>
      <td class="nm">${e.exp.transporteur?esc(e.exp.transporteur)+(e.exp.suivi?' · ':''):''}${esc(e.exp.suivi||'')}${!e.exp.transporteur&&!e.exp.suivi?'—':''}</td>
      <td><span class="stw st-shipped" data-nolang>shipped</span>${e.exp.auto?'<span class="lg">marquée completed sur le site</span>':''}</td>
      <td class="r">${money2(e.montant)}</td>
    </tr>`).join('')}${fait.length>60?`<tr><td colspan="9" style="color:var(--ink-3)">et ${nf(fait.length-60)} de plus…</td></tr>`:''}</tbody></table>`;
  document.querySelectorAll('tr.ex').forEach(tr=>tr.onclick=()=>ouvre(tr.dataset.id));
  $('tri').onclick=inverseTri; document.querySelectorAll('[data-tri]').forEach(th=>th.onclick=inverseTri);
  document.querySelectorAll('[data-exp]').forEach(b=>b.onclick=e=>{ e.stopPropagation(); ouvre(b.dataset.exp,true); });
  const ct=document.getElementById('ct-expeditions'); if(ct){ if(att.length){ ct.textContent=att.length+' à expédier'; ct.classList.add('pt'); } else { ct.textContent=''; ct.classList.remove('pt'); } }
  $('sfoot').innerHTML=`${nf(att.length)} à expédier<br>${nf(fait.length)} parties ces 30 jours`;
}

function peintCanaux(){
  const C=faCanauxExp();
  const L=[['woocommerce','Site perfumestrade.com'],['woocommerce-gros','Site wholesale.perfumestrade.com'],['amazon','Amazon'],['shopify','Shopify']];
  $('canaux').innerHTML=L.map(([k,n])=>`<label><input type="checkbox" data-canal="${k}"${C[k]?' checked':''}> <span data-nolang>${esc(n)}</span></label>`).join('')
    +`<span class="fix">La caisse Lightspeed n'y passe jamais : le client repart avec le flacon, la vente entre tout de suite.</span>`;
  document.querySelectorAll('[data-canal]').forEach(c=>c.onchange=()=>{
    const R=lit(KREG,{}); R.exped=Object.assign({},faCanauxExp(),{[c.dataset.canal]:c.checked}); ecrit(KREG,R);
    const J=lit('crm-journal-v1',[]); J.push({t:new Date().toISOString(),u:NOM_UTIL||'(non renseigné)',act:'reglage',lib:'expéditions : '+(SRC[c.dataset.canal]||c.dataset.canal)+(c.checked?' passe par Expéditions (le stock sort au départ)':' entre directement dans le stock'),ref:'expeditions',av:null,ap:c.checked?'oui':'non'}); ecrit('crm-journal-v1',J);
  });
}

function ferme(){ $('dov').classList.remove('on'); DETAIL=null; }
function ouvre(id,focus){
  const e=faLitExp().find(x=>x._i===id); if(!e){ peint(); return; }
  DETAIL=id; const C=ctx(); const att=e.statut==='attente';
  $('d-tit').innerHTML=`Commande <span class="nm">${esc(e.num||'')}</span> <span class="et ${att?'att':'ok'}">${att?'à expédier':'expédiée'}</span>
    <span class="sub"><span class="nm">${esc(SRC[e.src]||e.src||'')} · ${dfr(e.d)}${e.h?' · '+esc(e.h):''}${faNomClient(e.client)?' · '+esc(faNomClient(e.client)):''}</span></span>`;
  const l=[];
  if(att) l.push(`<div class="blo exp"><h4>Expédier</h4>
    <div class="frm">
      <label>Partie le<input type="date" id="x-d" value="${ajd()}" max="${ajd()}"></label>
      <label>Transporteur<input id="x-tr" list="x-trs" placeholder="USPS, UPS, FedEx…"><datalist id="x-trs"><option>USPS</option><option>UPS</option><option>FedEx</option><option>DHL</option><option>Amazon</option></datalist></label>
      <label class="w">N° de suivi (facultatif)<input id="x-sv" placeholder="" autocomplete="off"></label>
    </div>
    <p class="nt">Marquer la commande expédiée fait sa facture et sort les flacons du stock — pas avant. Tant qu'elle est ici, le stock ne bouge pas.</p></div>`);
  else l.push(`<div class="blo"><h4>Expédition</h4>
    <div class="pl"><span>Partie le</span><b>${dfr(e.exp.d)}</b></div>
    <div class="pl"><span>Par</span><b class="nm">${esc(e.exp.par||'')}</b></div>
    ${e.exp.transporteur?`<div class="pl"><span>Transporteur</span><b class="nm">${esc(e.exp.transporteur)}</b></div>`:''}
    ${e.exp.suivi?`<div class="pl"><span>N° de suivi</span><b class="nm">${esc(e.exp.suivi)}</b></div>`:''}
    <div class="pl"><span>Facture</span><b>${e.factId?'faite · voir dans Ventes':'—'}</b></div></div>`);
  l.push(`<div class="blo"><h4>La commande · ${nf(e.lignes.length)} parfum${e.lignes.length>1?'s':''}</h4>
    <table><tbody>${e.lignes.map(li=>{ const cle=C.cleDe(li); const stk=cle?C.qteEff(cle):null; const mq=(att&&cle&&li.q>stk);
      return `<tr><td><b class="nm">${esc(li.ref||li.des||'')}</b>${li.bc?`<small class="bc">${esc(li.bc)}</small>`:''}
        ${att?(cle?`<small>${mq?`<span class="stk">${nf(stk)} en stock pour ${nf(li.q)} demandé${li.q>1?'s':''}</span>`:`${nf(stk)} en stock`}</small>`:`<small class="stk">référence introuvable au catalogue</small>`):''}</td>
        <td class="r">${nf(li.q)} ×<br><small>${li.p!=null?money2(li.p):'—'}</small></td>
        <td class="r"><b>${money2(li.q*(li.p||0))}</b></td></tr>`; }).join('')}</tbody></table>
    <div class="pl gr" style="margin-top:8px"><span>${(n=>nf(n)+' flacon'+(n>1?'s':''))(e.lignes.reduce((a,l)=>a+l.q,0))}</span><b>${money2(e.montant)}</b></div>
    ${e.total!=null&&Math.abs((+e.total||0)-e.montant)>0.05?`<p class="nt"><span>Le canal annonce un total de</span> <b class="mq">${money2(+e.total)}</b> <span>(frais de port, taxes ou remise non détaillés ici).</span></p>`:''}
  </div>`);
  l.push(`<div class="blo"><h4>Reçu</h4>
    <div class="pl"><span>Commandée le</span><b>${dfr(e.d)}${e.h?' · '+esc(e.h):''}</b></div>
    <div class="pl"><span>Arrivée dans l'outil le</span><b>${e.arrive?esc(quandMiami(e.arrive)):'—'}</b></div>
    ${e.hors?`<div class="pl"><span>Lignes de service mises de côté (port, sachet…)</span><b>${nf(e.hors)}</b></div>`:''}
  </div>`);
  $('d-corps').innerHTML=l.join('');
  $('d-pied').innerHTML=att
    ?`<button class="btn" id="x-ret">Retirer sans expédier</button><span style="flex:1"></span><button class="btn" id="d-ok">Fermer</button><button class="btn pri" id="x-go">Expédiée — le stock sort</button>`
    :`<span style="flex:1"></span><button class="btn" id="d-ok">Fermer</button>`;
  $('dov').classList.add('on');
  $('d-ok').onclick=ferme; $('d-x').onclick=ferme;
  if(att){
    $('x-go').onclick=()=>{
      if(!signe('expédier cette commande',()=>{})) return;
      const d=$('x-d').value||ajd(); if(d>ajd()){ $('x-d').focus(); return; }
      const r=faExpedier(id,{d,transporteur:$('x-tr').value,suivi:$('x-sv').value});
      ferme(); CTX=null; peint();
      const b=$('msg'); if(!r){ b.innerHTML=`<div class="info warn">La commande n'a pas pu être expédiée : une référence n'existe plus au catalogue.</div>`; return; }
      b.innerHTML=`<div class="info"><b>Commande ${esc(e.num||'')} expédiée le ${dfr(d)}</b> — facture faite, le stock a été mis à jour.`
        +(r.ecarts.length?`<br><b style="color:var(--crit)">Vendu à découvert</b> : ${r.ecarts.map(x=>esc(x.ref)+' (vendu '+x.vendu+', en stock '+x.stock+')').join(', ')}. Le détail est dans le <a href="journal.html">journal</a>.`:'')+`</div>`;
      setTimeout(()=>{ b.innerHTML=''; },9000);
    };
    $('x-ret').onclick=()=>{
      if(!confirm('Retirer la commande '+(e.num||'')+' sans l\'expédier ?\n\nElle ne sera pas facturée et le stock ne bougera pas. Le site ou Amazon, eux, gardent leur trace.')) return;
      if(!signe('retirer cette commande',()=>{})) return;
      faRetireExp(id,''); ferme(); peint();
    };
    if(focus) setTimeout(()=>{ try{ $('x-tr').focus(); }catch(_){ } },50);
  }
}
$('dov').addEventListener('click',e=>{ if(e.target===$('dov')) ferme(); });
document.addEventListener('keydown',e=>{ if(e.key==='Escape'&&$('dov').classList.contains('on')) ferme(); });

$('tete').innerHTML=`<b>Les commandes qui doivent partir.</b> Une commande du site ou d'Amazon arrive ici sans toucher au stock. Quand le colis est parti, ouvre-la et marque-la « expédiée » avec la date : c'est ce geste qui fait la facture et sort les flacons. Une commande annulée avant ce geste disparaît d'elle-même — rien n'était sorti.`;
$('pied').innerHTML=`<b>Ce qui n'est pas ici.</b> Les ventes de la caisse Lightspeed entrent tout de suite dans <a href="ventes.html">Ventes</a> : le client repart avec le flacon. Une commande dont un parfum n'est pas reconnu attend d'abord dans Ventes qu'on dise lequel c'est, puis arrive ici.`;
peint(); peintCanaux();
/* venu de Ventes (clic sur une commande à expédier) : sa fiche s'ouvre directement */
try{ const q=new URLSearchParams(location.search).get('cmd'); if(q&&faLitExp().some(x=>x._i===q)) ouvre(q); }catch(e){}
/* quand un autre onglet ou le serveur écrit des expéditions, la page se redessine toute seule */
window.addEventListener('storage',e=>{ if(e.key===KEXP||e.key==='caisse-file-v1'){ CTX=null; peint(); } });
if(typeof _apresEcrit!=='undefined') _apresEcrit.push(cle=>{ if(cle===KEXP&&!DETAIL) setTimeout(peint,0); });
"""

html = coquille("Statut shipping", "Statut shipping",
    "Les commandes du site et d'Amazon qui doivent partir, avec leur statut sur WooCommerce. Le stock sort quand la commande est expédiée — ou toute seule, quand le site la marque completed.",
    CSS, CORPS, JS, donnees=('produits',))
open('expeditions.html', 'w').write(html)
print('expeditions.html', len(html)//1024, 'Ko')
