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
.tk-ok{font-size:12.5px;font-weight:600;color:var(--good)}.tk-ok a{color:var(--iris);margin-left:4px}
.tk-px{grid-column:1/-1;display:flex;flex-wrap:wrap;gap:10px 14px;align-items:flex-end;margin-top:8px;padding:10px 12px;background:var(--surface-2);border-radius:10px}
.tk-px label{display:flex;flex-direction:column;gap:3px;font-size:11.5px;color:var(--ink-3);font-weight:600}
.tk-px input{width:92px;font:inherit;font-size:14px;padding:6px 8px;border:1px solid var(--line);border-radius:8px;background:var(--surface);color:var(--ink)}
.tk-px .tk-vente{flex-basis:100%;font-size:12.5px;color:var(--ink-2)}.tk-px .tk-vente b{color:var(--crit)}
.tk-px .tk-msg{flex-basis:100%;font-size:12.5px;color:var(--ink-2)}
.tk-px .tk-can{flex-basis:100%;display:flex;flex-wrap:wrap;gap:8px 16px;align-items:center;font-size:13px}
.tk-px .tk-can label{flex-direction:row;align-items:center;gap:6px;font-size:13px;color:var(--ink);font-weight:500}
.tk-px textarea{flex-basis:100%;font:inherit;font-size:13px;padding:7px 9px;border:1px solid var(--line);border-radius:8px;background:var(--surface);color:var(--ink);min-height:54px}
.tk-px button{font-family:inherit;font-size:12.5px;font-weight:600;border:1px solid var(--line);background:var(--surface);color:var(--ink-2);border-radius:8px;padding:6px 10px;cursor:pointer}
.tk-px button.pri{background:var(--iris);border-color:var(--iris);color:#fff}
.tk-px button:disabled{opacity:.5;cursor:default}
.tk-el{flex-basis:100%;display:grid;grid-template-columns:auto 1fr auto;gap:4px 10px;align-items:center;font-size:13px;max-height:260px;overflow:auto;padding-right:4px}
.tk-el label{display:contents;cursor:pointer}.tk-el .nm b{display:block}.tk-el .nm span{font-size:11.5px;color:var(--ink-3)}
.tk-el .st{font-size:12px;color:var(--ink-3);white-space:nowrap}.tk-el .st.ret{color:var(--warn)}
.tk-a button:hover,.tk-a a:hover{border-color:var(--iris);color:var(--iris)} .tk-a a.pri:hover,.tk-a button.pri:hover{color:#fff;filter:brightness(1.08)}
.tk-a select{color:var(--ink-2)}
.tk-vide{background:var(--surface);border:1px dashed var(--line);border-radius:12px;padding:22px;text-align:center;color:var(--ink-3);font-size:14px}
.tk-vide b{display:block;color:var(--good);font-size:16px;margin-bottom:4px}
details.tk-ign summary{cursor:pointer;color:var(--ink-3);font-size:13px;font-weight:600;margin:24px 0 10px}
@media(max-width:700px){.tk{grid-template-columns:1fr}.tk-a{justify-content:flex-start}}
"""

CORPS = r"""
<div class="tk-tete" id="tk-tete"></div>
<div id="tk-corps"><div class="tk-vide" id="tk-att">Léa regarde ce qu'il y a à faire…</div></div>
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
/* 7 nov. 2026 (Igal : « Prix à vérifier » se règle sur place) : les prix de la fiche, lus comme partout (la fiche corrigée l'emporte) */
const IDX=__IDX__; const KMOD='fiches-modifiees-v1';
const tkMod=()=>{ try{ const M=lit(KMOD,{}); return (M&&typeof M==='object')?M:{}; }catch(e){ return {}; } };
const tkPrix=cle=>{ const v=IDX[cle]||[], m=tkMod()[cle]||{}; const n=x=>(x==null||x==='')?null:+x;
  return {pa:m.pa!=null&&m.pa!==''?+m.pa:n(v[3]), pvw:m.pvw!=null&&m.pvw!==''?+m.pvw:n(v[5]), pvr:m.pvr!=null&&m.pvr!==''?+m.pvr:n(v[6]), bc:v[0]||'', ref:((v[2]||'')+' '+(v[1]||'')).trim()}; };
const m2=v=>v==null?'—':Number(v).toLocaleString('fr-FR',{minimumFractionDigits:2,maximumFractionDigits:2})+'\u00a0$';
const tkFile=()=>{ try{ const F=lit('caisse-file-v1',[]); return Array.isArray(F)?F.filter(v=>v&&!v.annule&&v._i):[]; }catch(e){ return []; } };
const tkSrc=s=>({woocommerce:'perfumestrade.com','woocommerce-gros':'wholesale.perfumestrade.com',lightspeed:'Lightspeed',shopify:'Shopify','shopify-pc':'Perfume City',amazon:'Amazon',message:'message'})[s]||s||'';
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
  /* 7 nov. 2026 (Igal) : « Recommander » se règle sur place — un clic met le parfum dans « Parfums à racheter » (tableau de
     bord), la tâche est faite, on reste ici. La fiche reste ouvrable à côté. */
  const rach=(t.type==='rupture'||t.type==='manque')&&t.cle&&typeof rachAjoute==='function';
  const px=t.type==='prix'&&t.cle&&IDX[t.cle];
  /* 7 nov. 2026 : « Reprendre la mise en ligne » se fait sur place (les raisons du refus, un bouton Réessayer) ; c'est le Catalogue
     en cadre qui fait le travail. Les tâches « Mettre en ligne N parfums sur un site » n'existent plus (Igal : « je ne veux pas de ces
     deux rubriques ») : ce qui manque sur un site reste au tableau de bord. */
  const pcs=t.type==='pcshopify'&&typeof pcRenvoiFacture==='function';
  const exp=t.type==='expedier'&&typeof faExpedier==='function'&&typeof faLitExp==='function'&&faLitExp().some(x=>x&&x._i===String(t.id).split('|')[1]&&x.statut==='attente');
  const pub=t.type==='publication'&&(t.cle||t.bc)&&typeof enLigneFenetre==='function';
  const cpl=t.type==='completer'&&typeof attenteFenetre==='function'&&tkFile().length;
  if(t.etat==='a_faire'&&cpl) actions=`${ouvre('')}<button data-etat="faite" data-id="${esc(t.id)}">${tkT('Fait','Done','Hecho')} ✓</button>${rappel}<button data-etat="ignoree" data-id="${esc(t.id)}">${tkT('Ignorer','Ignore','Ignorar')}</button>`;
  else if(t.etat==='a_faire'&&pcs) actions=`<button class="pri" data-pcs="${esc(String(t.id).split('|')[1]||'')}" data-id="${esc(t.id)}">${tkT('Renvoyer à Shopify','Send again to Shopify','Reenviar a Shopify')} →</button>${ouvre('')}<button data-etat="faite" data-id="${esc(t.id)}">${tkT('Fait','Done','Hecho')} ✓</button>${rappel}<button data-etat="ignoree" data-id="${esc(t.id)}">${tkT('Ignorer','Ignore','Ignorar')}</button>`;
  else if(t.etat==='a_faire'&&exp) actions=`${ouvre('')}<button data-etat="faite" data-id="${esc(t.id)}">${tkT('Fait','Done','Hecho')} ✓</button>${rappel}<button data-etat="ignoree" data-id="${esc(t.id)}">${tkT('Ignorer','Ignore','Ignorar')}</button>`;
  else if(t.etat==='a_faire'&&pub) actions=`<button class="pri" data-pub="${esc(t.cle||'')}" data-bc="${esc(t.bc||'')}" data-id="${esc(t.id)}" data-canaux="${esc((t.canaux||[]).join(','))}">${tkT('Réessayer la mise en ligne','Retry the listing','Reintentar la publicación')} →</button>${t.cle?ouvre(''):''}<button data-etat="faite" data-id="${esc(t.id)}">${tkT('Fait','Done','Hecho')} ✓</button>${rappel}<button data-etat="ignoree" data-id="${esc(t.id)}">${tkT('Ignorer','Ignore','Ignorar')}</button>`;
  else if(t.etat==='a_faire'&&px) actions=`${ouvre('')}<button data-etat="faite" data-id="${esc(t.id)}">${tkT('Fait','Done','Hecho')} ✓</button>${rappel}<button data-pxign="${esc(t.id)}">${tkT('Ignorer','Ignore','Ignorar')}</button>`;
  else if(t.etat==='a_faire'&&rach) actions=`<button class="pri" data-rach="${esc(t.cle)}" data-id="${esc(t.id)}" data-bc="${esc(t.bc||'')}" data-ref="${esc(t.ref||'')}">${tkT('Mettre dans Parfums à racheter','Add to Perfumes to reorder','Poner en Perfumes por recomprar')} →</button>${ouvre('')}<button data-etat="faite" data-id="${esc(t.id)}">${tkT('Fait','Done','Hecho')} ✓</button>${rappel}<button data-etat="ignoree" data-id="${esc(t.id)}">${tkT('Ignorer','Ignore','Ignorar')}</button>`;
  else if(t.etat==='a_faire') actions=`${ouvre('pri')}<button data-etat="faite" data-id="${esc(t.id)}">${tkT('Fait','Done','Hecho')} ✓</button>${rappel}<button data-etat="ignoree" data-id="${esc(t.id)}">${tkT('Ignorer','Ignore','Ignorar')}</button>`;
  else if(t.etat==='attente') actions=`${ouvre('')}<button data-etat="a_faire" data-id="${esc(t.id)}">${tkT('Remettre dans la liste','Put back in the list','Volver a la lista')}</button><button data-etat="ignoree" data-id="${esc(t.id)}">${tkT('Ignorer','Ignore','Ignorar')}</button>`;
  else actions=`${ouvre('')}<button data-etat="a_faire" data-id="${esc(t.id)}">${tkT('Remettre dans la liste','Put back in the list','Volver a la lista')}</button>`;
  const pt=t.etat==='a_faire'?(t.urgence==='haute'?`<span class="pt">${tkT('urgent','urgent','urgente')}</span>`:'')+(t.revenue?`<span class="pt rev">${tkT('revenue','back','de vuelta')}</span>`:''):'';
  const sous=t.etat==='attente'?`<small>${tkT('Rappel le','Reminder on','Recordatorio el')} <span data-nolang>${tkDate(t.jusqua)}</span></small>`:t.etat==='ignoree'?`<small>${tkT('Ignorée le','Ignored on','Ignorada el')} <span data-nolang>${tkDate(t.depuis)}</span></small>`:'';
  const raison=t.etat==='ignoree'&&t.raison?`<small class="tk-raison">${tkT('Raison','Reason','Motivo')} : <span data-nolang>${esc(t.raison)}</span></small>`:'';
  let bloc='';
  if(t.etat==='a_faire'&&px){ const P=tkPrix(t.cle), w=t.vente||{};
    const frais=[w.com?tkT('commission','commission','comisión')+' '+m2(w.com):'',w.carte?tkT('frais de carte','card fees','comisión de tarjeta')+' '+m2(w.carte):'',w.envoi?tkT('envoi','shipping','envío')+' '+m2(w.envoi):'',w.port?tkT('port payé par le client','shipping paid by the customer','portes pagados por el cliente')+' +'+m2(w.port):''].filter(Boolean);
    const vente=w.d?`<div class="tk-vente" data-nolang>${esc(tkDate(w.d))} · ${esc(w.canal||'')} : ${tkT('vendu','sold','vendido')} ${m2(w.p)}${w.q>1?' × '+w.q:''}, ${tkT('acheté','bought','comprado')} ${m2(w.pa)}${w.q>1?' × '+w.q:''}${frais.length?', '+frais.join(', '):''} → ${w.perte?`<b>${tkT('perte de','loss of','pérdida de')} ${m2(-w.mg)}</b>`:`<b>${w.pct!=null?w.pct+' %':''}</b> ${tkT('de marge','margin','de margen')}`}${w.n>1?`, ${w.n} ${tkT('ventes cette semaine','sales this week','ventas esta semana')}`:''}</div>`:'';
    bloc=`<div class="tk-px" data-px="${esc(t.cle)}" data-id="${esc(t.id)}" data-titre="${esc(t.titre)}">${vente}
      <label>${tkT("Prix d'achat","Purchase price","Precio de compra")}<input type="number" step="0.01" min="0" data-pxa value="${P.pa==null?'':P.pa}"></label>
      <label>${tkT('Prix de gros','Wholesale price','Precio mayorista')}<input type="number" step="0.01" min="0" data-pxw value="${P.pvw==null?'':P.pvw}"></label>
      <label>${tkT('Prix retail','Retail price','Precio retail')}<input type="number" step="0.01" min="0" data-pxr value="${P.pvr==null?'':P.pvr}"></label>
      <button class="pri" data-pxok>${tkT('Enregistrer les prix','Save the prices','Guardar los precios')}</button><div class="tk-msg" data-pxmsg></div></div>`; }
  if(t.etat==='a_faire'&&exp){ const e=faLitExp().find(x=>x&&x._i===String(t.id).split('|')[1]); const auj=new Date(Date.now()-new Date().getTimezoneOffset()*60000).toISOString().slice(0,10);
    bloc=`<div class="tk-px" data-exp="${esc(e._i)}" data-id="${esc(t.id)}" data-titre="${esc(t.titre)}">
      <div class="tk-vente" data-nolang>${(e.lignes||[]).map(l=>`${esc(l.ref||l.des||l.bc||'')} × ${nf(l.q||0)}`).join(' · ')}${e.ville||e.pays?` — ${esc([e.ville,e.pays].filter(Boolean).join(', '))}`:''}</div>
      <label>${tkT('Partie le','Shipped on','Enviado el')}<input type="date" data-xd value="${auj}" max="${auj}"></label>
      <label>${tkT('Transporteur','Carrier','Transportista')}<input data-xtr list="tk-trs" placeholder="USPS, UPS, FedEx…"><datalist id="tk-trs"><option>USPS</option><option>UPS</option><option>FedEx</option><option>DHL</option></datalist></label>
      <label>${tkT('N° de suivi (facultatif)','Tracking no. (optional)','N.º de seguimiento (opcional)')}<input data-xsv autocomplete="off" style="width:180px"></label>
      <button class="pri" data-xgo>${tkT('Expédiée','Shipped','Enviada')} ✓</button>
      <div class="tk-msg">${tkT('Marquer la commande expédiée fait sa facture et sort les flacons du stock — pas avant.','Marking the order shipped makes its invoice and takes the bottles out of stock — not before.','Marcar el pedido como enviado hace su factura y saca los frascos del stock — no antes.')}</div><div class="tk-msg" data-pxmsg></div></div>`; }
  if(t.etat==='a_faire'&&pcs&&t.detail) bloc=`<div class="tk-px"><div class="tk-msg" data-pxmsg-pc="${esc(t.id)}">${tkT('Le cockpit ajoute les quantités reçues sur Shopify ; rien n\'est compté deux fois.','The cockpit adds the received quantities on Shopify; nothing is counted twice.','El cockpit añade las cantidades recibidas en Shopify; nada se cuenta dos veces.')}</div></div>`;
  if(t.etat==='a_faire'&&cpl){ const F=tkFile();
    bloc=`<div class="tk-px" data-cpl="1" data-id="${esc(t.id)}"><div class="tk-msg">${tkT('Chaque vente attend qu\'on lui dise quel parfum c\'est : clique, choisis-le, elle s\'enregistre.','Each sale is waiting to be told which perfume it is: click, pick it, it gets recorded.','Cada venta espera que le digan qué perfume es: pulsa, elígelo, se registra.')}</div>
      <div class="tk-el" style="grid-template-columns:1fr auto auto">${F.slice(0,40).map(v=>`<span class="nm" data-nolang><b>${esc((v.num?v.num+' · ':'')+(tkSrc(v.src)))}${v.client?' — '+esc(typeof faNomClient==='function'?faNomClient(v.client):String(v.client&&v.client.nom||v.client||'')):''}</b><span>${esc((v.lignes||[]).map(l=>(l.des||l.bc||'?')+' ×'+(l.q||1)).join(', ').slice(0,140))}</span></span><span class="st" data-nolang>${esc(tkDate(v.d||''))}</span><button data-cplv="${esc(v._i)}">${tkT('Compléter','Complete','Completar')} →</button>`).join('')}</div>
      ${F.length>40?`<div class="tk-msg" data-nolang>… +${nf(F.length-40)}</div>`:''}</div>`; }
  if(t.etat==='a_faire'&&pub&&t.raisons&&t.raisons.length) bloc=`<div class="tk-px"><div class="tk-msg">${t.raisons.map(r=>`<div data-nolang><b>${esc(r.nom||r.canal)}</b> : ${esc(r.r)}</div>`).join('')}<div>${tkT('Règle ce qui manque (la photo, le prix : « Ouvrir » la fiche), puis réessaie.','Fix what is missing (the photo, the price: “Open” the sheet), then retry.','Arregla lo que falta (la foto, el precio: «Abrir» la ficha) y vuelve a intentar.')}</div></div></div>`;
  return `<div class="tk ${t.etat==='a_faire'?t.urgence:t.etat}" data-tk="${esc(t.id)}"><div><h3><span data-nolang>${esc(t.titre)}</span>${pt}</h3><p data-nolang>${esc(t.detail||'')}</p>${sous}${raison}<small>${typ}</small></div><div class="tk-a" data-titre="${esc(t.titre)}">${actions}</div>${bloc}</div>`;
}
function tkPeint(){
  const z=$('tk-corps'), h=$('tk-tete'); if(!TK) return;
  const n=TK.a_faire.length;
  h.innerHTML=`<div class="tk-kpi ${TK.urgentes?'hot':''}"><b>${nf(TK.urgentes)}</b><span>${tkT('urgentes','urgent','urgentes')}</span></div>
    <div class="tk-kpi"><b>${nf(n)}</b><span>${tkT('à faire','to do','por hacer')}</span></div>
    <div class="tk-kpi"><b>${nf(TK.attente.length)}</b><span>${tkT('en attente','waiting','en espera')}</span></div>
    <div class="tk-maj">${tkT('Léa relit l\'ERP à chaque ouverture de cette page.','Léa re-reads the ERP each time this page opens.','Léa relee el ERP cada vez que se abre esta página.')}</div>`;
  let s=`<h2 class="sec">${tkT('À faire','To do','Por hacer')} <em>${tkT('les plus urgentes en premier · une tâche disparaît toute seule quand le problème n\'existe plus','most urgent first · a task goes away by itself once the problem is gone','las más urgentes primero · una tarea desaparece sola cuando el problema ya no existe')}</em></h2>`;
  s+=n?TK.a_faire.map(tkLigne).join(''):`<div class="tk-vide"><b>${tkT('Rien à faire pour l\'instant','Nothing to do right now','Nada que hacer por ahora')}</b>${tkT('Léa te dira dès qu\'il y a quelque chose.','Léa will tell you as soon as there is something.','Léa te avisará en cuanto haya algo.')}</div>`;
  if(TK.attente.length) s+=`<h2 class="sec">${tkT('En attente','Waiting','En espera')} <em>${tkT('elles reviendront dans la liste à la date du rappel','they will come back to the list on the reminder date','volverán a la lista en la fecha del recordatorio')}</em></h2>`+TK.attente.map(tkLigne).join('');
  if(TK.ignorees.length) s+=`<details class="tk-ign"><summary>${tkT(`${nf(TK.ignorees.length)} tâche${TK.ignorees.length>1?'s':''} ignorée${TK.ignorees.length>1?'s':''}`,`${nf(TK.ignorees.length)} ignored task${TK.ignorees.length>1?'s':''}`,`${nf(TK.ignorees.length)} tarea${TK.ignorees.length>1?'s':''} ignorada${TK.ignorees.length>1?'s':''}`)}</summary>`+TK.ignorees.map(tkLigne).join('')+'</details>';
  z.innerHTML=s;
  z.querySelectorAll('button[data-etat]').forEach(b=>b.onclick=()=>tkStatue(b.dataset.id,b.dataset.etat,undefined,b.closest('.tk-a').dataset.titre));
  z.querySelectorAll('button[data-fiche]').forEach(b=>b.onclick=()=>{ if(typeof ficheFenetre!=='function'){ window.open('catalogue.html#cle='+encodeURIComponent(b.dataset.fiche),'_blank'); return; }
    ficheFenetre(b.dataset.fiche,()=>{ const y=window.scrollY; tkCharge().then(()=>window.scrollTo(0,y)); },b.dataset.plus||''); });
  z.querySelectorAll('button[data-rach]').forEach(b=>b.onclick=async()=>{ if(TK_ENV) return;
    try{ rachAjoute(b.dataset.rach,{bc:b.dataset.bc,ref:b.dataset.ref}); }catch(e){ alert(tkT('Pas enregistré : ','Not saved: ','No guardado: ')+(e&&e.message||e)); return; }
    const z2=b.closest('.tk'); if(z2) z2.querySelector('.tk-a').innerHTML=`<span class="tk-ok">${tkT('Dans Parfums à racheter','In Perfumes to reorder','En Perfumes por recomprar')} ✓ <a href="tableau.html#racheter">${tkT('voir le tableau de bord','see the dashboard','ver el panel')}</a></span>`;
    await tkStatue(b.dataset.id,'faite',undefined,b.closest('.tk-a')?b.closest('.tk-a').dataset.titre:''); });
  z.querySelectorAll('.tk-px').forEach(b=>tkPrixBranche(b));
  z.querySelectorAll('button[data-pxign]').forEach(b=>b.onclick=()=>tkIgnorePrix(b));
  z.querySelectorAll('.tk-px[data-exp]').forEach(b=>tkExpBranche(b));
  z.querySelectorAll('button[data-cplv]').forEach(b=>b.onclick=()=>{ if(TK_ENV) return; attenteFenetre(b.dataset.cplv,()=>{ const y=window.scrollY; tkCharge().then(()=>window.scrollTo(0,y)); }); });
  z.querySelectorAll('button[data-pcs]').forEach(b=>b.onclick=async()=>{ if(TK_ENV) return; const id=b.dataset.id, titre=(b.closest('.tk-a')||{dataset:{}}).dataset.titre;
    const m=z.querySelector(`[data-pxmsg-pc="${CSS.escape(id)}"]`); b.disabled=true; if(m) m.textContent=tkT('Envoi à Shopify…','Sending to Shopify…','Enviando a Shopify…');
    const r=await pcRenvoiFacture(b.dataset.pcs);
    if(r.ok){ if(m) m.innerHTML=`<b>${tkT('Stock de Perfume City mis à jour sur Shopify','Perfume City stock updated on Shopify','Stock de Perfume City actualizado en Shopify')} (${nf(r.bon)})</b>`; await tkStatue(id,'faite',undefined,titre); }
    else { b.disabled=false; if(m) m.innerHTML=`<b style="color:var(--crit)">${tkT('Pas envoyé','Not sent','No enviado')}</b> — <span data-nolang>${esc(r.raison||(r.mal||[]).join(' ; '))}</span>`; } });
  z.querySelectorAll('button[data-pub]').forEach(b=>b.onclick=()=>{ if(TK_ENV) return;
    let cle=b.dataset.pub; if(!cle&&b.dataset.bc){ const bc=String(b.dataset.bc).replace(/^0+/,''); cle=Object.keys(IDX).find(k=>String((IDX[k]||[])[0]||'').replace(/^0+/,'')===bc)||''; }
    if(!cle){ alert(tkT('Ce parfum n\'est plus au Catalogue.','This perfume is no longer in the Catalog.','Este perfume ya no está en el Catálogo.')); return; }
    const cs=String(b.dataset.canaux||'').split(',').filter(Boolean), id=b.dataset.id, titre=(b.closest('.tk-a')||{dataset:{}}).dataset.titre;
    enLigneFenetre([cle],()=>{ const y=window.scrollY; tkCharge().then(()=>window.scrollTo(0,y)); },cs); });
  z.querySelectorAll('select[data-rappel]').forEach(sl=>sl.onchange=()=>{ if(sl.value) tkStatue(sl.dataset.rappel,'attente',+sl.value,sl.closest('.tk-a').dataset.titre); });
  const c=document.getElementById('ct-taches'); if(c){ c.textContent=n?String(n):''; c.className=n?'ct nb':'ct'; }
}
async function tkStatue(id,etat,jours,titre,raison){
  if(TK_ENV) return; TK_ENV=true;
  try{ await tkApi('/etat',{id,etat,jours,titre,raison}); await tkCharge(); }
  catch(e){ alert(tkT('Pas enregistré : ','Not saved: ','No guardado: ')+(e&&e.message||e)); }
  TK_ENV=false;
}
/* « Enregistrer les prix » : les prix tapés deviennent ceux de la fiche du Catalogue (fiches-modifiees-v1, donc tout l'ERP),
   avec une ligne de journal par prix changé ; puis l'ERP demande sur quels canaux de vente les poser (cases cochées), et c'est le
   Catalogue en cadre qui les pose, avec ses règles. La tâche est faite. */
function tkPrixBranche(b){
  const cle=b.dataset.px, id=b.dataset.id, titre=b.dataset.titre, msg=t=>{ const e=b.querySelector('[data-pxmsg]'); if(e) e.innerHTML=t; };
  const bt=b.querySelector('[data-pxok]'); if(!bt) return;
  bt.onclick=()=>{
    const P=tkPrix(cle), M=tkMod(), m=Object.assign({},M[cle]||{}), lu=k=>{ const v=b.querySelector('[data-px'+k+']').value.trim(); return v===''?null:Math.round(+v*100)/100; };
    const nv={pa:lu('a'),pvw:lu('w'),pvr:lu('r')}; const LIB={pa:"prix d'achat",pvw:'prix de gros',pvr:'prix retail'};
    if(Object.values(nv).some(v=>v!=null&&!(v>=0))){ msg(tkT('Un prix n\'est pas lisible.','A price is not readable.','Un precio no se puede leer.')); return; }
    const chg=Object.keys(nv).filter(k=>nv[k]!=null&&nv[k]!==P[k]);
    if(!chg.length){ msg(tkT('Rien n\'a changé.','Nothing changed.','Nada cambió.')); return; }
    if(nv.pvw!=null&&nv.pa!=null&&nv.pvw<nv.pa&&!confirm(tkT('Le prix de gros est sous le prix d\'achat. Continuer ?','The wholesale price is below the purchase price. Continue?','El precio mayorista está por debajo del de compra. ¿Continuar?'))) return;
    let J=[]; try{ J=lit('crm-journal-v1',[])||[]; }catch(e){ J=[]; } if(!Array.isArray(J)) J=[];
    const u=(typeof NOM_UTIL==='string'&&NOM_UTIL)?NOM_UTIL:'(non renseigné)';
    chg.forEach(k=>{ m[k]=nv[k]; J.push({t:new Date().toISOString(),u,act:'prix',champ:k,lib:LIB[k]+' (depuis Tâches)',bc:P.bc,ref:P.ref,av:P[k],ap:nv[k]}); });
    M[cle]=m; ecrit(KMOD,M); ecrit('crm-journal-v1',J);
    b.querySelectorAll('input,[data-pxok]').forEach(e=>e.disabled=true);
    msg(`<b>${tkT('Prix enregistrés dans le Catalogue.','Prices saved in the Catalog.','Precios guardados en el Catálogo.')}</b> ${tkT('Les mettre aussi sur les canaux de vente ?','Also put them on the sales channels?','¿Ponerlos también en los canales de venta?')}
      <div class="tk-can"><label><input type="checkbox" data-can="site" checked> perfumestrade.com</label><label><input type="checkbox" data-can="sitegros" checked> wholesale.perfumestrade.com</label><label><input type="checkbox" data-can="perfumecity" checked> Perfume City (Shopify)</label>
      <button class="pri" data-pxenv>${tkT('Mettre sur ces canaux','Put on these channels','Poner en estos canales')}</button><button data-pxnon>${tkT('Pas maintenant','Not now','Ahora no')}</button></div>`);
    b.querySelector('[data-pxnon]').onclick=()=>tkStatue(id,'faite',undefined,titre);
    b.querySelector('[data-pxenv]').onclick=()=>{ const cs=[...b.querySelectorAll('[data-can]:checked')].map(x=>x.dataset.can);
      if(!cs.length){ tkStatue(id,'faite',undefined,titre); return; }
      if(typeof prixCanauxFenetre!=='function'){ window.open('catalogue.html#cle='+encodeURIComponent(cle),'_blank'); tkStatue(id,'faite',undefined,titre); return; }
      prixCanauxFenetre(cle,cs,()=>tkStatue(id,'faite',undefined,titre)); };
  };
}
function tkExpBranche(b){
  const eid=b.dataset.exp, id=b.dataset.id, titre=b.dataset.titre, go=b.querySelector('[data-xgo]'), msg=t=>{ const e=b.querySelector('[data-pxmsg]'); if(e) e.innerHTML=t; };
  go.onclick=async()=>{ if(TK_ENV) return;
    const auj=b.querySelector('[data-xd]').max, d=b.querySelector('[data-xd]').value||auj; if(d>auj){ b.querySelector('[data-xd]').focus(); return; }
    if(typeof signe==='function'&&!signe('expédier cette commande',()=>{})) return;
    const r=faExpedier(eid,{d,transporteur:b.querySelector('[data-xtr]').value,suivi:b.querySelector('[data-xsv]').value});
    if(!r){ msg(`<b style="color:var(--crit)">${tkT('La commande n\'a pas pu être expédiée : une référence n\'existe plus au catalogue.','The order could not be shipped: a reference no longer exists in the catalog.','El pedido no se pudo enviar: una referencia ya no existe en el catálogo.')}</b>`); return; }
    b.querySelectorAll('input,button').forEach(e=>e.disabled=true);
    msg(`<b>${tkT('Expédiée — facture faite, le stock a été mis à jour.','Shipped — invoice made, the stock has been updated.','Enviada — factura hecha, el stock se actualizó.')}</b>`+(r.ecarts&&r.ecarts.length?` <span data-nolang>${tkT('Vendu à découvert','Sold short','Vendido en descubierto')} : ${r.ecarts.map(x=>esc(x.ref)+' ('+x.vendu+' / '+x.stock+')').join(', ')}</span>`:''));
    await tkStatue(id,'faite',undefined,titre); };
}
/* Ignorer un prix se justifie (Igal, 7 nov. 2026 : « pourquoi ignorer ? — parfum acheté trop cher ») : la raison est obligatoire,
   gardée avec la tâche et au journal du cockpit */
function tkIgnorePrix(btn){
  const id=btn.dataset.pxign, z=btn.closest('.tk'); if(!z) return; const titre=(z.querySelector('.tk-a')||{}).dataset?z.querySelector('.tk-a').dataset.titre:'';
  let b=z.querySelector('.tk-px'); if(!b){ b=document.createElement('div'); b.className='tk-px'; z.appendChild(b); }
  b.innerHTML=`<div class="tk-msg"><b>${tkT('Pourquoi ignorer ce prix ?','Why ignore this price?','¿Por qué ignorar este precio?')}</b> ${tkT('Par exemple : parfum acheté trop cher.','For example: perfume bought too expensive.','Por ejemplo: perfume comprado demasiado caro.')}</div>
    <textarea data-pxraison placeholder="${tkT('La raison…','The reason…','El motivo…')}"></textarea>
    <button class="pri" data-pxignok>${tkT('Ignorer avec cette raison','Ignore with this reason','Ignorar con este motivo')}</button><button data-pxignnon>${tkT('Annuler','Cancel','Cancelar')}</button><div class="tk-msg" data-pxmsg></div>`;
  const ta=b.querySelector('[data-pxraison]'); ta.focus();
  b.querySelector('[data-pxignnon]').onclick=()=>{ const y=window.scrollY; tkPeint(); window.scrollTo(0,y); };
  b.querySelector('[data-pxignok]').onclick=()=>{ const r=ta.value.trim(); if(!r){ b.querySelector('[data-pxmsg]').textContent=tkT('Il faut une raison.','A reason is required.','Hace falta un motivo.'); ta.focus(); return; }
    tkStatue(id,'ignoree',undefined,titre,r); };
}
async function tkCharge(){
  try{ TK=await tkApi(''); tkPeint(); }
  catch(e){ $('tk-corps').innerHTML=`<div class="tk-vide">${tkT('Léa ne répond pas : ','Léa is not answering: ','Léa no responde: ')}${esc(e&&e.message||String(e))}</div>`; }
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
    "Ce que Léa te demande de faire aujourd'hui, trouvé dans l'ERP : parfums à recommander, prix à vérifier, mises en ligne, Perfume City, expéditions. Fais, ignore, ou demande un rappel.",
    CSS, CORPS, JS, donnees=('produits',)).replace('__IDX__', 'Object.fromEntries(D_TOUS().map(r=>[r[15],[r[0],r[13],r[2],r[12],r[6],r[8],r[7]]]))')
open('taches.html', 'w').write(html)
print('taches.html', len(html)//1024, 'Ko')
