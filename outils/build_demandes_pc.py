# -*- coding: utf-8 -*-
"""Rubrique « Transfert interstore » (Igal, 4 nov. 2026 ; d'abord « Demandes Perfume City », renommée le jour même).

« Sam m'a expliqué que certaines fois Perfume City ou Perfume Trade se font des appels de parfums : Perfume City dit
'est-ce que vous pouvez nous envoyer trois références'. Je veux la possibilité sur l'ERP de faire des demandes de parfums
entre Perfume City et Perfumes Trade. Et si une vendeuse de Perfume City demande à Sam un parfum qu'elle est censée avoir
en stock, il faut un petit message : « Attention, ce produit-là est déjà en stock chez vous. »

Une demande = un petit dossier (qui demande, quels parfums, combien, une note) qui suit un chemin simple :
  demandée → envoyée → reçue            (ou refusée par l'autre boutique, ou annulée par celui qui l'a faite)
Elle vit dans un magasin partagé (demandes-pc-v1, une fiche par demande, fusionnée champ par champ) : Kim et Sam voient
la même liste. Le mouvement de stock lui-même n'est PAS automatique : « Envoyée » ne déplace aucun flacon (l'envoi vers
Perfume City se fait comme avant, depuis une facture d'achat) ; la demande est le message, pas la livraison.
"""
from build_crm import coquille

CSS = r"""
.dm-bascule{display:inline-flex;border:1px solid var(--line);border-radius:10px;overflow:hidden;margin:0 0 14px}
.dm-bascule button{font-family:inherit;font-size:14px;font-weight:600;border:0;background:var(--surface);color:var(--ink-2);padding:10px 16px;cursor:pointer}
.dm-bascule button.on{background:var(--iris);color:#fff}
.dm-bascule button+button{border-left:1px solid var(--line)}
.dm-carte{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:16px 18px;margin:0 0 14px}
.dm-carte h3{margin:0 0 4px;font-size:15px;font-weight:700}
.dm-aide{margin:0 0 10px;font-size:13px;color:var(--ink-3);line-height:1.5}
#dm-q{width:100%;padding:11px 13px;border:1px solid var(--line);border-radius:9px;font-size:15px;font-family:inherit;box-sizing:border-box}
#dm-res{margin-top:8px}
.dm-r{display:grid;grid-template-columns:1fr auto;gap:4px 12px;align-items:center;padding:9px 11px;border:1px solid var(--line-2);border-radius:9px;margin:0 0 6px;background:var(--surface)}
.dm-r b{font-size:14px} .dm-r small{display:block;color:var(--ink-3);font-size:12.5px}
.dm-r button,.dm-btn{font-family:inherit;font-size:13px;font-weight:600;border:1px solid var(--line);background:var(--surface);color:var(--ink-2);border-radius:8px;padding:7px 12px;cursor:pointer}
.dm-r button:hover,.dm-btn:hover{border-color:var(--iris);color:var(--iris)}
.dm-btn.pri{background:var(--iris);border-color:var(--iris);color:#fff} .dm-btn.pri:hover{color:#fff;filter:brightness(1.08)}
.dm-btn[disabled]{opacity:.45;cursor:not-allowed}
.dm-l{display:grid;grid-template-columns:1fr 90px auto;gap:6px 12px;align-items:center;padding:10px 0;border-top:1px solid var(--line-2)}
.dm-l:first-child{border-top:0}
.dm-l input{width:80px;padding:8px;border:1px solid var(--line);border-radius:8px;font-size:15px;text-align:right;font-family:inherit}
.dm-att{grid-column:1/-1;background:#FFF4D6;border:1px solid #F0D58A;color:#6B4E00;border-radius:8px;padding:7px 10px;font-size:13px;font-weight:600}
.dm-inf{grid-column:1/-1;color:var(--ink-3);font-size:12.5px}
.dm-note{width:100%;padding:10px 12px;border:1px solid var(--line);border-radius:9px;font-size:14px;font-family:inherit;box-sizing:border-box;margin:10px 0}
.dm-dem{background:var(--surface);border:1px solid var(--line);border-left:4px solid var(--warn);border-radius:12px;padding:13px 16px;margin:0 0 10px}
.dm-dem.envoyee{border-left-color:var(--iris)} .dm-dem.recue{border-left-color:var(--good);opacity:.85}
.dm-dem.refusee,.dm-dem.annulee{border-left-color:var(--line);opacity:.7}
.dm-dem h3{margin:0 0 2px;font-size:15px;font-weight:700}
.dm-dem .pt{display:inline-block;font-size:10px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:var(--iris);background:var(--iris-soft);padding:2px 8px;border-radius:99px;margin-left:8px;vertical-align:middle}
.dm-dem ul{margin:8px 0 6px;padding:0;list-style:none}
.dm-dem li{padding:3px 0;font-size:14px}
.dm-dem small{display:block;color:var(--ink-3);font-size:12.5px;margin-top:3px}
.dm-act{display:flex;gap:6px;flex-wrap:wrap;margin-top:10px;align-items:center}
.dm-act input{padding:7px 10px;border:1px solid var(--line);border-radius:8px;font-size:13px;font-family:inherit;min-width:200px}
.dm-vide{background:var(--surface);border:1px dashed var(--line);border-radius:12px;padding:22px;text-align:center;color:var(--ink-3);font-size:14px}
h2.sec{font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:var(--ink);font-weight:700;margin:30px 0 12px;padding-bottom:9px;border-bottom:1px solid var(--line);display:flex;justify-content:space-between;align-items:baseline;gap:12px;flex-wrap:wrap}
h2.sec em{font-style:normal;font-size:12.5px;letter-spacing:0;text-transform:none;color:var(--ink-3);font-weight:400}
details.dm-his summary{cursor:pointer;color:var(--ink-3);font-size:13px;font-weight:600;margin:22px 0 10px}
@media(max-width:700px){.dm-l{grid-template-columns:1fr 80px}.dm-l .dm-x{grid-column:1/-1}}
"""

CORPS = r"""
<div id="dm-form"></div>
<div id="dm-liste"></div>
"""

JS = r"""
/* ---------- les demandes de parfums entre Perfume City et Perfumes Trade ---------- */
const IDX=__IDX__;
const KDM='demandes-pc-v1', KJOU='crm-journal-v1', KMOD='fiches-modifiees-v1', KEXT='stock-externe-v1';
const T=(a,b,c)=>L3(a,b,c);
const BOUTIQUE={pc:'Perfume City',pt:'Perfumes Trade'};
const autre=c=>c==='pc'?'pt':'pc';
const norm=s=>String(s||'').normalize('NFD').replace(/[̀-ͯ]/g,'').toLowerCase();
const sansZero=b=>String(b||'').replace(/^0+/,'');
/* le stock central (celui de Perfumes Trade) : le fichier, corrigé par les fiches modifiées et le stock externe, comme au tableau de bord */
function produits(){
  let MOD={},EXT={q:{}};
  try{ MOD=lit(KMOD,{})||{}; }catch(e){}
  try{ const r=lit(KEXT,null); if(r&&r.q) EXT=r; }catch(e){}
  return Object.entries(IDX).map(([cle,v])=>{
    const [bc,nom,marque,pa0,qte0]=v; const m=MOD[cle]||{};
    let q=qte0; if(EXT.q[bc]!==undefined&&EXT.q[bc]!==null) q=EXT.q[bc]; if(m.qte!=null) q=m.qte;
    return {cle,bc:String(bc||''),nom:String(nom||''),marque:String(marque||''),qte:Math.max(0,Math.round(+q||0)),clef:norm(nom+' '+marque+' '+bc)};
  });
}
/* le stock de Perfume City (la boutique de Kim) : une fiche par code-barres, partagée */
function stockPC(){
  const par={}; let rows=null; try{ rows=(typeof pcsRows==='function')&&pcsRows(); }catch(e){}
  (rows||[]).forEach(r=>{ const k=sansZero(r[0]); if(k) par[k]=(par[k]||0)+(Math.round(+r[5])||0); });
  return par;
}
let PROD=[], PCQ={};
function recharge(){ PROD=produits(); PCQ=stockPC(); }
const qteChez=(p,c)=>c==='pc'?(PCQ[sansZero(p.bc)]||0):p.qte;

let DE='pc', LIG=[], NOTE='';
const quand=iso=>{ try{ const d=new Date(iso); return d.toLocaleDateString('en-US',{timeZone:'America/New_York',month:'numeric',day:'numeric',year:'2-digit'})+' '+d.toLocaleTimeString('en-US',{timeZone:'America/New_York',hour:'numeric',minute:'2-digit'}); }catch(e){ return String(iso||'').slice(0,16); } };
function journal(lib,ref){ try{ const s=session(); const J=lit(KJOU,[])||[]; J.push({t:new Date().toISOString(),u:(s&&s.nom)||'',act:'demande',lib,ref:ref||'',av:'',ap:'',n:1,impact:0,det:[]}); ecrit(KJOU,J); }catch(e){} }

/* l'avertissement de Igal : le demandeur a DÉJÀ ce parfum en stock */
function avertit(p,c){
  const n=qteChez(p,c);
  const att=n>0?`<div class="dm-att">⚠ ${T('Attention : ce produit est déjà en stock chez vous','Warning: this product is already in stock at your place','Atención: este producto ya está en stock en su tienda')} (<span data-nolang>${esc(BOUTIQUE[c])}</span> : <span data-nolang>${nf(n)}</span> ${T('flacon'+(n>1?'s':''),'bottle'+(n>1?'s':''),'frasco'+(n>1?'s':''))}).</div>`:'';
  const o=autre(c), no=qteChez(p,o);
  const inf=no<=0?`<div class="dm-inf">${T('Pas de stock chez','No stock at','Sin stock en')} <span data-nolang>${esc(BOUTIQUE[o])}</span> ${T('pour ce parfum.','for this perfume.','de este perfume.')}</div>`:`<div class="dm-inf"><span data-nolang>${esc(BOUTIQUE[o])}</span> : <span data-nolang>${nf(no)}</span> ${T('en stock','in stock','en stock')}</div>`;
  return att+inf;
}

function dessineForm(){
  const z=$('dm-form');
  const bascule=['pc','pt'].map(c=>`<button type="button" data-de="${c}" class="${DE===c?'on':''}"><span data-nolang>${esc(BOUTIQUE[c])}</span> ${T('demande','asks','pide')} <span data-nolang>→ ${esc(BOUTIQUE[autre(c)])}</span></button>`).join('');
  const lignes=LIG.map((l,i)=>{ const p=PROD.find(x=>x.cle===l.cle)||{cle:l.cle,bc:l.bc,nom:l.nom,qte:0};
    return `<div class="dm-l"><div><b data-nolang>${esc(l.nom)}</b></div><div><input type="number" min="1" step="1" value="${l.q}" data-i="${i}" class="dm-qte" aria-label="${T('Quantité','Quantity','Cantidad')}"></div><div class="dm-x"><button type="button" class="dm-btn" data-ote="${i}">${T('Retirer','Remove','Quitar')}</button></div>${avertit(p,DE)}</div>`; }).join('');
  z.innerHTML=`<h2 class="sec" style="margin-top:6px">${T('Nouveau transfert','New transfer','Nueva transferencia')} <em>${T('Qui demande à qui ?','Who is asking whom?','¿Quién pide a quién?')}</em></h2>
    <div class="dm-bascule">${bascule}</div>
    <div class="dm-carte">
      <h3>${T('Quel parfum ?','Which perfume?','¿Qué perfume?')}</h3>
      <p class="dm-aide">${T('Tape le nom, la marque ou le code-barres, puis ajoute-le à la demande.','Type the name, brand or barcode, then add it to the request.','Escribe el nombre, la marca o el código de barras y añádelo a la solicitud.')}</p>
      <input id="dm-q" type="search" autocomplete="off" placeholder="${T('Ex. Ferrari, Sauvage, 3348…','E.g. Ferrari, Sauvage, 3348…','Ej. Ferrari, Sauvage, 3348…')}">
      <div id="dm-res"></div>
    </div>
    <div class="dm-carte" id="dm-recap">
      <h3>${T('Dans la demande','In the request','En la solicitud')} <span data-nolang>(${nf(LIG.length)})</span></h3>
      ${LIG.length?lignes:`<p class="dm-aide" style="margin:0">${T('Rien encore : cherche un parfum ci-dessus.','Nothing yet: search for a perfume above.','Nada todavía: busca un perfume arriba.')}</p>`}
      <input class="dm-note" id="dm-note" placeholder="${T('Un mot pour '+BOUTIQUE[autre(DE)]+' (facultatif)','A note for '+BOUTIQUE[autre(DE)]+' (optional)','Una nota para '+BOUTIQUE[autre(DE)]+' (opcional)')}" value="${esc(NOTE)}">
      <button type="button" class="dm-btn pri" id="dm-envoie" ${LIG.length?'':'disabled'}>${T('Envoyer la demande','Send the request','Enviar la solicitud')}</button>
    </div>`;
  z.querySelectorAll('[data-de]').forEach(b=>b.onclick=()=>{ if(DE===b.dataset.de) return; DE=b.dataset.de; dessineForm(); });
  z.querySelectorAll('.dm-qte').forEach(i=>i.oninput=()=>{ const v=Math.max(1,Math.round(+i.value)||1); LIG[+i.dataset.i].q=v; });
  z.querySelectorAll('[data-ote]').forEach(b=>b.onclick=()=>{ LIG.splice(+b.dataset.ote,1); dessineForm(); });
  $('dm-note').oninput=e=>{ NOTE=e.target.value; };
  $('dm-envoie').onclick=envoie;
  const q=$('dm-q'); q.oninput=cherche; q.focus();
}
function cherche(){
  const t=norm($('dm-q').value).trim(); const R=$('dm-res');
  if(t.length<2){ R.innerHTML=''; return; }
  const mots=t.split(/\s+/);
  const L=PROD.filter(p=>mots.every(m=>p.clef.indexOf(m)>=0)).sort((a,b)=>(qteChez(b,autre(DE))>0)-(qteChez(a,autre(DE))>0)||a.nom.localeCompare(b.nom)).slice(0,8);
  if(!L.length){ R.innerHTML=`<p class="dm-aide">${T('Aucun parfum trouvé.','No perfume found.','Ningún perfume encontrado.')}</p>`; return; }
  R.innerHTML=L.map(p=>{ const n=qteChez(p,DE);
    return `<div class="dm-r"><div><b data-nolang>${esc(p.nom)}</b><small data-nolang>${esc(p.marque)} · ${esc(BOUTIQUE[DE])} : ${nf(n)} · ${esc(BOUTIQUE[autre(DE)])} : ${nf(qteChez(p,autre(DE)))}</small>${n>0?`<small style="color:#8A5B00;font-weight:600">⚠ ${T('déjà en stock chez vous','already in stock at your place','ya en stock en su tienda')}</small>`:''}</div><button type="button" data-ajoute="${esc(p.cle)}">${LIG.some(l=>l.cle===p.cle)?T('Déjà ajouté','Already added','Ya añadido'):T('Ajouter','Add','Añadir')}</button></div>`; }).join('');
  R.querySelectorAll('[data-ajoute]').forEach(b=>b.onclick=()=>{ const p=PROD.find(x=>x.cle===b.dataset.ajoute); if(!p||LIG.some(l=>l.cle===p.cle)) return;
    LIG.push({cle:p.cle,bc:p.bc,nom:p.nom,q:1}); dessineForm(); });
}
function envoie(){
  if(!LIG.length) return;
  const s=session(), id='dm'+Date.now().toString(36)+Math.random().toString(36).slice(2,5);
  const lignes=LIG.map(l=>{ const p=PROD.find(x=>x.cle===l.cle)||{bc:l.bc,qte:0}; return {cle:l.cle,bc:l.bc,nom:l.nom,q:Math.max(1,Math.round(+l.q)||1),deja:qteChez(p,DE)}; });
  const D=lit(KDM,{}); const o=(D&&typeof D==='object'&&!Array.isArray(D))?D:{};
  o[id]={id,de:DE,t:new Date().toISOString(),par:(s&&s.nom)||'',note:NOTE.trim(),lignes,etat:'demandee',maj:new Date().toISOString(),majpar:(s&&s.nom)||''};
  ecrit(KDM,o);
  journal(`demande de parfums : ${BOUTIQUE[DE]} demande à ${BOUTIQUE[autre(DE)]} — ${lignes.map(l=>l.q+' × '+l.nom).join(', ')}${lignes.some(l=>l.deja>0)?' (certains sont déjà en stock chez le demandeur)':''}`,id);
  LIG=[]; NOTE=''; dessineForm(); dessineListe();
}

const ETAT={demandee:['Demandée','Requested','Solicitada'],envoyee:['Envoyée','Sent','Enviada'],recue:['Reçue','Received','Recibida'],refusee:['Refusée','Declined','Rechazada'],annulee:['Annulée','Cancelled','Cancelada']};
function carte(r){
  const e=r.etat||'demandee';
  const ls=(r.lignes||[]).map(l=>`<li><b data-nolang>${nf(l.q)} ×</b> <span data-nolang>${esc(l.nom)}</span>${l.deja>0?` <span style="color:#8A5B00;font-weight:600">⚠ ${T('déjà '+l.deja+' en stock chez le demandeur','already '+l.deja+' in stock at the requester','ya hay '+l.deja+' en stock en quien pide')}</span>`:''}</li>`).join('');
  let act='';
  if(e==='demandee') act=`<button class="dm-btn pri" data-a="envoyee" data-id="${esc(r.id)}">${T('Envoyé','Sent','Enviado')} ✓</button><input data-motif="${esc(r.id)}" placeholder="${T('Motif du refus (facultatif)','Reason for declining (optional)','Motivo del rechazo (opcional)')}"><button class="dm-btn" data-a="refusee" data-id="${esc(r.id)}">${T('Refuser','Decline','Rechazar')}</button><button class="dm-btn" data-a="annulee" data-id="${esc(r.id)}">${T('Annuler la demande','Cancel the request','Cancelar la solicitud')}</button>`;
  else if(e==='envoyee') act=`<button class="dm-btn pri" data-a="recue" data-id="${esc(r.id)}">${T('Bien reçu','Received','Recibido')} ✓</button>`;
  const suite=e==='demandee'?'':`<small>${T(ETAT[e][0],ETAT[e][1],ETAT[e][2])} ${T('par','by','por')} <span data-nolang>${esc(r.majpar||'')}</span> · <span data-nolang>${esc(quand(r.maj))}</span>${r.motif?' — <span data-nolang>'+esc(r.motif)+'</span>':''}</small>`;
  return `<div class="dm-dem ${e}"><h3><span data-nolang>${esc(BOUTIQUE[r.de])} → ${esc(BOUTIQUE[autre(r.de)])}</span><span class="pt">${T(ETAT[e][0],ETAT[e][1],ETAT[e][2])}</span></h3>
    <small>${T('Demandé par','Asked by','Pedido por')} <span data-nolang>${esc(r.par||'')}</span> · <span data-nolang>${esc(quand(r.t))}</span></small>
    <ul>${ls}</ul>${r.note?`<small>« <span data-nolang>${esc(r.note)}</span> »</small>`:''}${suite}${act?`<div class="dm-act">${act}</div>`:''}</div>`;
}
function change(id,etat,motif){
  const D=lit(KDM,{}); const r=D&&D[id]; if(!r) return; const s=session();
  r.etat=etat; r.maj=new Date().toISOString(); r.majpar=(s&&s.nom)||''; if(motif) r.motif=motif;
  ecrit(KDM,D);
  const v={envoyee:'envoyée',recue:'reçue',refusee:'refusée',annulee:'annulée'}[etat]||etat;
  journal(`demande de parfums ${v} : ${BOUTIQUE[r.de]} → ${BOUTIQUE[autre(r.de)]} — ${(r.lignes||[]).map(l=>l.q+' × '+l.nom).join(', ')}${motif?' (motif : '+motif+')':''}`,id);
  dessineListe();
}
function dessineListe(){
  const D=lit(KDM,{}); const T0=(D&&typeof D==='object'&&!Array.isArray(D))?Object.values(D):[];
  const en=T0.filter(r=>r&&(r.etat==='demandee'||r.etat==='envoyee')).sort((a,b)=>String(b.t).localeCompare(String(a.t)));
  const fin=T0.filter(r=>r&&!(r.etat==='demandee'||r.etat==='envoyee')).sort((a,b)=>String(b.maj||b.t).localeCompare(String(a.maj||a.t)));
  let s=`<h2 class="sec">${T('En cours','In progress','En curso')} <em>${T('une demande reste ici jusqu\'à ce que les parfums soient bien reçus','a request stays here until the perfumes are received','una solicitud queda aquí hasta que los perfumes se reciben')}</em></h2>`;
  s+=en.length?en.map(carte).join(''):`<div class="dm-vide">${T('Aucune demande en cours.','No request in progress.','Ninguna solicitud en curso.')}</div>`;
  if(fin.length) s+=`<details class="dm-his"><summary>${T('Historique','History','Historial')} (<span data-nolang>${nf(fin.length)}</span>)</summary>${fin.slice(0,60).map(carte).join('')}</details>`;
  const z=$('dm-liste'); z.innerHTML=s;
  z.querySelectorAll('[data-a]').forEach(b=>b.onclick=()=>{ const m=z.querySelector('[data-motif="'+b.dataset.id+'"]'); change(b.dataset.id,b.dataset.a,b.dataset.a==='refusee'&&m?m.value.trim():''); });
  const c=document.getElementById('ct-demandes'); if(c){ c.textContent=en.length?String(en.length):''; c.className=en.length?'ct nb':'ct'; }
}
window.__rafraichir=()=>{ recharge(); dessineListe(); };
(function(){ if(!session()) return; recharge(); dessineForm(); dessineListe(); })();
"""

html = coquille("Transfert interstore", "Transfert interstore",
    "Perfume City et Perfumes Trade se transfèrent des parfums : choisis les références et les quantités, l'autre boutique répond. "
    "Si le demandeur a déjà le parfum en stock, un avertissement le dit.",
    CSS, CORPS, JS, donnees=('produits',)).replace('__IDX__', 'Object.fromEntries(D_TOUS().map(r=>[r[15],[r[0],r[13],r[2],r[12],r[6],r[8],r[7]]]))')
open('demandes_pc.html', 'w').write(html)
print('demandes_pc.html', len(html)//1024, 'Ko')
