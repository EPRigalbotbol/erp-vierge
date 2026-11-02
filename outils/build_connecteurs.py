# -*- coding: utf-8 -*-
"""Rubrique « Connecteurs » : l'état RÉEL des branchements, canal par canal.

Avant, cette page était une liste d'étapes à cocher à la main, écrite avant que le
cockpit n'existe — elle ne connectait rien, et disait « aucun connecté » alors que
le site l'était depuis des jours (Igal, 12 sept. 2026 : « elle sert à quelque
chose ? et si oui pourquoi rien n'est connecté ? »).

Maintenant : ce que le cockpit sait (relié, en panne, absent — jamais une clé), et ce
que l'outil a reçu (la dernière vente arrivée de chaque canal, combien attendent).
La plomberie elle-même — déposer une clé, relier un site — se fait dans le cockpit.
"""
from build_crm import coquille

CSS = r"""
.tete{font-size:14px;color:var(--ink-2);line-height:1.6;max-width:80ch;margin:0 0 18px}
.tete b{color:var(--ink)}
.grille{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:14px;margin-bottom:22px}
.cx{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:16px 18px;display:flex;flex-direction:column;gap:10px}
.cx h3{margin:0;font-size:16px;font-weight:800;letter-spacing:-.01em;display:flex;align-items:center;gap:9px;flex-wrap:wrap}
.cx h3 [data-nolang]{min-width:0;overflow-wrap:anywhere}
.cx h3 .ic{font-size:18px;opacity:.8}
.et{display:inline-block;flex:none;white-space:nowrap;font-family:Inter,sans-serif;font-size:10.5px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;padding:3px 9px;border-radius:99px;margin-left:auto}
.et.relie{background:var(--good-soft);color:var(--good)}
.et.panne{background:var(--crit-soft);color:var(--crit)}
.et.attente{background:var(--warn-soft);color:var(--warn)}
.et.fichier{background:var(--line-2);color:var(--ink-2)}
.et.main{background:var(--iris-soft);color:var(--iris)}
.et.hors{background:var(--line-2);color:var(--ink-3)}
.cx:has(.et.hors){opacity:.72}
.cx .ligne{font-size:13px;color:var(--ink-2);line-height:1.55}
.cx .ligne b{color:var(--ink)}
.cx .chiffres{display:grid;grid-template-columns:1fr 1fr;gap:8px}
.cx .chiffres div{background:var(--surface-2);border:1px solid var(--line-2);border-radius:8px;padding:8px 10px}
.cx .chiffres b{display:block;font-family:Inter,sans-serif;font-size:18px;font-weight:800;letter-spacing:-.02em}
.cx .chiffres span{font-size:11.5px;color:var(--ink-3)}
.cx .note{font-size:12.5px;color:var(--ink-3);line-height:1.5;border-top:1px dashed var(--line-2);padding-top:8px}
.cx .note a{color:var(--iris)}

.pied{font-size:13px;color:var(--ink-2);line-height:1.65;max-width:80ch}
.pied a{color:var(--iris)}
#hors{font-size:12.5px;color:var(--warn);background:var(--warn-soft);border-radius:8px;padding:9px 12px;margin:0 0 16px;display:none}
#hors.on{display:block}
"""

CORPS = r"""
<p class="tete" id="tete"></p>
<div class="hors" id="hors"></div>
<div class="grille" id="grille"></div>
<p class="pied" id="pied"></p>
"""

JS = r"""
const KFACT='factures-v1', KFILE='caisse-file-v1';
/* Les canaux, et comment chacun arrive dans l'outil. `service` = le nom de la liaison
   dans le cockpit ; `src` = ce que porte une vente arrivée par ce canal (`auto`). */
const CANAUX=[
  {id:'site',    ic:'🛒', nom:'Site perfumestrade.com',           service:'woocommerce',      src:['woocommerce'],      comment:'Le cockpit relève les commandes payées toutes les 2 minutes ; chaque vente entre ici toute seule, avec sa facture.'},
  {id:'gros',    ic:'📦', nom:'Site wholesale.perfumestrade.com', service:'woocommerce-gros', src:['woocommerce-gros'], comment:'Même mécanique que le site de détail, canal « gros ».'},
  {id:'amazon',  ic:'📮', nom:'Amazon',                           service:'amazon-boite',     src:['amazon'],           comment:'Le cockpit lit les e-mails « Sold, ship now » de la boîte du compte vendeur. Chaque commande entre ici toute seule, avec sa facture : le stock sort à la vente. Une annulation Amazon fait un retour.'},
  {id:'caisse',  ic:'🧾', nom:'Caisse Lightspeed',                service:'hook:lightspeed',  src:['lightspeed'],       comment:"Chaque vente fermée à la caisse arrive ici par Zapier, avec le parfum reconnu par son code-barres (le cockpit connaît les produits de la caisse). Au besoin, l'export de fichier marche toujours : Factures → Importer des ventes.", fichier:true},
  {id:'shopify', ic:'🏬', nom:'Shopify (Perfume City)',           service:'shopify',          src:['shopify'],          comment:"Perfume City est la boutique de la femme de Sam : ses ventes restent sur Shopify, par décision de Sam (10 septembre). Rien n'est à brancher ici ; ce que Perfumes Trade lui livre passe par une sortie « Perfume City » dans l'Inventaire.", hors:true},
  {id:'envoi',   ic:'✉️', nom:"Boîte d'envoi (cotes et factures par e-mail)", service:'email', src:[],               comment:"La boîte Gmail qui envoie les cotes et les factures aux clients. Sans elle, l'envoi passe par WhatsApp ou par ton propre logiciel de messagerie.", pasVente:true},
];
const LIB={relie:'relié',panne:'en panne',attente:'à brancher',fichier:'par fichier',main:'à la main',hors:'hors périmètre'};
const dfr=d=>{ if(!d) return '—'; const [a,m,j]=String(d).slice(0,10).split('-'); return m+'/'+j+'/'+a.slice(2); };

/* ce que l'outil a reçu, canal par canal */
function recu(){
  const F=lit(KFACT,[]), Q=lit(KFILE,[]); const R={};
  (Array.isArray(F)?F:[]).forEach(f=>{ if(!f||f.sens!=='vente'||!f.auto) return; const s=String(f.auto);
    const r=(R[s]=R[s]||{n:0,der:'',mt:0,att:0}); if(!f.retour){ r.n++; r.mt+=f.montant||0; } if((f.d||'')>r.der) r.der=f.d; });
  (Array.isArray(Q)?Q:[]).forEach(v=>{ if(!v) return; const r=(R[v.src]=R[v.src]||{n:0,der:'',mt:0,att:0}); r.att++; });
  return R;
}
let LIAISONS=null, HORS=false;
async function litLiaisons(){
  if(typeof EN_LIGNE==='undefined'||!EN_LIGNE||!ckTok()) return null;
  try{ const r=await fetch(CK_URL+'/api/o/'+CK_ORG+'/liaisons',{headers:{Authorization:'Bearer '+ckTok()}});
    if(!r.ok) throw new Error('serveur '+r.status); const j=await r.json(); return j.liaisons||[]; }
  catch(e){ HORS=true; return null; }
}
function etatDe(c,R){
  const l=(LIAISONS||[]).find(x=>x.service===c.service);
  const rec=c.src.map(s=>R[s]).filter(Boolean);
  if(c.hors) return {k:'hors',lib:LIB.hors,note:''};
  if(l){ if(l.etat==='panne') return {k:'panne',lib:LIB.panne,note:l.note||''}; return {k:'relie',lib:LIB.relie,note:l.note||''}; }
  if(c.fichier) return {k:'fichier',lib:LIB.fichier,note:''};
  if(c.pasVente) return {k:'attente',lib:LIB.attente,note:''};
  /* pas de liaison connue mais des ventes reçues : relié quand même (le cockpit n'a pas répondu) */
  if(rec.some(r=>r.n)) return {k:'relie',lib:LIB.relie,note:''};
  return {k:'attente',lib:LIB.attente,note:''};
}
function dessine(){
  const R=recu();
  const cartes=CANAUX.map(c=>{
    const e=etatDe(c,R); const rec=c.src.map(s=>R[s]).filter(Boolean);
    const n=rec.reduce((a,r)=>a+r.n,0), mt=rec.reduce((a,r)=>a+r.mt,0), att=rec.reduce((a,r)=>a+r.att,0), der=rec.reduce((a,r)=>r.der>a?r.der:a,'');
    return `<article class="cx" data-c="${c.id}">
      <h3><span class="ic">${c.ic}</span><span data-nolang>${esc(c.nom)}</span><span class="et ${e.k}">${e.lib}</span></h3>
      <div class="ligne">${c.comment}</div>
      ${c.pasVente?'':`<div class="chiffres">
        <div><b>${nf(n)}</b><span>vente${n>1?'s':''} reçue${n>1?'s':''} ici${mt?' · '+money(mt):''}</span></div>
        <div><b>${der?dfr(der):'—'}</b><span>dernière vente reçue${att?' · <span style="color:var(--warn)">'+nf(att)+' en attente</span>':''}</span></div>
      </div>`}
      ${e.note?`<div class="note" data-nolang>${esc(e.note)}</div>`:''}
      ${e.k==='attente'&&c.id==='amazon'?`<div class="note">Il manque le mot de passe d'application de la boîte du compte vendeur — il se crée depuis le compte Google de cette boîte (validation par SMS sur le téléphone de Sam), puis se dépose dans le cockpit, carte « Ventes Amazon ».</div>`:''}
      ${e.k==='attente'&&c.id==='envoi'?`<div class="note">Un mot de passe d'application de la boîte Gmail d'envoi, à déposer dans le cockpit, carte « Boîte d'envoi ».</div>`:''}
    </article>`; }).join('');
  $('grille').innerHTML=cartes;
  const nRel=CANAUX.filter(c=>etatDe(c,R).k==='relie').length;
  $('src').innerHTML=`${nf(nRel)} relié${nRel>1?'s':''} sur ${CANAUX.length}`;
  const ct=document.getElementById('ct-connecteurs'); if(ct) ct.textContent='';
  $('hors').classList.toggle('on',HORS); if(HORS) $('hors').textContent="Le cockpit n'a pas répondu : l'état affiché vient de ce que l'outil a reçu, pas de ce que le cockpit sait.";
}
$('tete').innerHTML=`<b>Ce que chaque canal fait entrer dans l'outil, et s'il est relié.</b> Les ventes de la caisse s'enregistrent toutes seules, avec leur facture, à l'ouverture de n'importe quelle page. Les commandes du site et d'Amazon aussi : le stock sort à la vente. Brancher ou débrancher un canal — déposer une clé, relier un site — se fait dans le cockpit, pas ici.`;
$('pied').innerHTML=`<b>Ce qui restera à la main, même tout branché.</b> Une commande de gros prise au téléphone ou par WhatsApp se saisit dans <a href="ventes.html">Ventes</a>, canal « Gros » : il n'y a aucune plateforme derrière. Une vente encaissée en boutique sans passer par la caisse, pareil.`;
$('sfoot').innerHTML="l'état des branchements<br>vu depuis l'outil";

dessine();
litLiaisons().then(L=>{ LIAISONS=L; dessine(); });
window.__CX={recu,etatDe,CANAUX,dessine,pose:(L)=>{ LIAISONS=L; dessine(); }};
"""

html = coquille("Connecteurs", "Connecteurs",
    "Quels canaux sont reliés, ce que chacun a fait entrer, et ce qui manque. La plomberie se fait dans le cockpit.",
    CSS, CORPS, JS, donnees=('produits',))
open('connecteurs.html', 'w').write(html)
print('connecteurs.html', len(html)//1024, 'Ko')
