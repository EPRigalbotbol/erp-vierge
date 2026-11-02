# -*- coding: utf-8 -*-
import json
from build_crm import coquille
import _donnees, _lire
C=json.load(open('cat.json'))
IDX={r[15]:[r[0],r[13],r[2],r[12],r[6],r[8],r[4],r[5]] for r in C}   # cle -> bc,nom,marque,pa,qte,pvw,TYPE,genre

CSS = r'''
.sous{margin:5px 0 0;font-size:14px;color:var(--ink-2);max-width:74ch;line-height:1.5}
.tools{display:flex;gap:9px;flex-wrap:wrap;align-items:center;margin-bottom:18px}
.tools .sp{margin-left:auto}
.sel{padding:9px 11px;font-family:inherit;font-size:13.5px;border:1px solid var(--line);
border-radius:7px;background:var(--surface);color:var(--ink);cursor:pointer}
.sel:focus{outline:0;border-color:var(--iris)}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(168px,1fr));gap:1px;
background:var(--line-2);border:1px solid var(--line);border-radius:9px;overflow:hidden;margin-bottom:22px;
box-shadow:0 1px 2px rgba(0,0,0,.04)}
.kpi{background:var(--surface);padding:15px 17px;display:flex;flex-direction:column;gap:3px}
.kpi .v{font-family:Inter,sans-serif;font-size:24px;font-weight:700;line-height:1;
letter-spacing:-.03em;font-variant-numeric:tabular-nums}
.kpi .k{font-size:12px;color:var(--ink-3);line-height:1.4}
h2.sec{font-family:Inter,sans-serif;font-size:10px;letter-spacing:.14em;text-transform:uppercase;
color:var(--ink);font-weight:700;margin:32px 0 13px;padding-bottom:8px;border-bottom:1px solid var(--line);
display:flex;justify-content:space-between;align-items:baseline;gap:12px;flex-wrap:wrap}
h2.sec em{font-style:normal;font-family:Inter,sans-serif;font-size:12.5px;letter-spacing:0;
text-transform:none;color:var(--ink-3);font-weight:400}

.fgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(330px,1fr));gap:15px}
.fg2{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px}
.fld{display:flex;flex-direction:column;gap:5px}
.fld label{font-family:Inter,sans-serif;font-size:10px;letter-spacing:.11em;text-transform:uppercase;color:var(--ink-3);font-weight:600}
.fld label i{font-style:normal;text-transform:none;letter-spacing:0;font-weight:400}
.fld input,.fld textarea{padding:10px 12px;font-family:inherit;font-size:14px;border:1px solid var(--line);
 border-radius:8px;background:var(--surface);color:var(--ink)}
.msg{font-size:13px;font-weight:600} .msg.err{color:var(--crit)} .msg.ok{color:var(--good)}
.fcard.ouvrable{cursor:pointer;transition:box-shadow .15s,transform .15s}
.fcard.ouvrable:hover{box-shadow:0 8px 24px rgba(0,0,0,.09);transform:translateY(-1px)}
.fcard.ouvrable header button{cursor:pointer}

/* ---- la fiche détaillée ---- */
.fd{max-width:980px!important;max-height:90vh;display:flex;flex-direction:column}
.fd .mb{overflow:auto;flex:1;min-height:0}
.fd .mb>*{flex:none}
.fd-top{display:flex;gap:16px;align-items:flex-start;flex-wrap:wrap}
.fd-top .id{flex:1;min-width:240px}
.fd-top .id h2{margin:0;font-size:24px;font-weight:800;letter-spacing:-.02em;color:var(--ink)}
.fd-top .id .rs{font-size:14px;color:var(--ink-2);margin-top:4px;font-weight:500}
.fd-top .co{font-size:14px;color:var(--ink);line-height:1.6;min-width:260px;background:var(--surface-2);
 border:1px solid var(--line);border-radius:9px;padding:10px 14px}
.fd-top .co i{font-style:normal;color:var(--ink-2);display:inline-block;min-width:82px;font-weight:600;font-size:12.5px}
.demotag{display:inline-block;margin-top:10px;padding:4px 10px;border-radius:20px;background:var(--warn-soft);
 color:var(--warn);font-size:12px;font-weight:700}
.fd-k{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:1px;background:var(--line);
 border:1px solid var(--line);border-radius:10px;overflow:hidden;margin:16px 0}
.fd-k div{background:var(--surface);padding:12px 14px;display:flex;flex-direction:column;gap:3px}
.fd-k b{font-size:22px;font-weight:800;letter-spacing:-.02em;color:var(--ink);font-variant-numeric:tabular-nums}
.fd-k span{font-size:12.5px;color:var(--ink-2);line-height:1.35;font-weight:500}
.fd h3{margin:22px 0 9px;font-size:14px;font-weight:800;letter-spacing:.06em;text-transform:uppercase;color:var(--iris);
 display:flex;align-items:baseline;gap:10px}
.fd h3 em{font-style:normal;font-weight:500;font-size:13px;letter-spacing:0;text-transform:none;color:var(--ink-2)}
.fd table{width:100%;border-collapse:collapse;font-size:14px}
.fd th{text-align:left;font-family:Inter,sans-serif;font-size:11px;letter-spacing:.08em;text-transform:uppercase;
 color:var(--ink);font-weight:800;padding:9px 10px;border-bottom:1px solid var(--line);background:var(--surface-2);white-space:nowrap}
.fd td{padding:9px 10px;border-bottom:1px solid var(--line-2);vertical-align:middle;color:var(--ink)}
.fd th.n,.fd td.n{text-align:center;font-variant-numeric:tabular-nums;white-space:nowrap}
.fd th.pr,.fd td.pr{text-align:left}
.fd .facs{border:1px solid var(--line);border-radius:9px;overflow:hidden}
.fd .fac{display:flex;align-items:baseline;gap:14px;padding:11px 14px;cursor:pointer;
 border-bottom:1px solid var(--line-2);white-space:nowrap;font-size:14.5px}
.fd .fac:hover{background:var(--surface-2)}
.fd .fac::before{content:"▸";width:12px;color:var(--ink-3);font-size:11px;flex:none}
.fd .fac.on::before{content:"▾"}
.fd .fac .fnum{font-weight:700;color:var(--ink);font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:14px}
.fd .fac .fdate{color:var(--ink);font-weight:600}
.fd .fac .fdet{color:var(--ink-2);font-size:13.5px;flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis}
.fd .fac .fmt{font-size:17px;color:var(--iris);font-weight:800;font-variant-numeric:tabular-nums}
.fd .det{background:var(--surface-2);border-bottom:1px solid var(--line-2);padding:4px 10px 8px 26px}
.fd .det table{font-size:12.5px} .fd .det th{background:transparent;border-bottom-color:var(--line-2)}
.fd .det td{padding:6px 10px;border-bottom-color:var(--line-2)}
.fd .det tr:last-child td{border-bottom:0}
.fd .pr b{color:var(--ink);display:block;font-weight:700} .fd .pr span{font-size:12px;color:var(--ink-2)}
.fd .up{color:var(--crit);font-weight:600} .fd .dn{color:var(--good);font-weight:600} .fd .eq{color:var(--ink-3)}
.fd .tw{border:1px solid var(--line);border-radius:9px;overflow:auto;max-height:340px}
.fd .mois{display:flex;gap:4px;align-items:flex-end;height:70px;padding:6px 2px 0}
.fd .mois div{flex:1;display:flex;flex-direction:column;align-items:center;gap:3px;min-width:0}
.fd .mois i{display:block;width:100%;background:var(--iris-soft);border-radius:3px 3px 0 0;border-top:2px solid var(--iris)}
.fd .mois span{font-size:11px;color:var(--ink-2);white-space:nowrap;font-weight:600}
.fd .mois b{font-size:11px;color:var(--ink);font-weight:700;white-space:nowrap}
.fd .mois i{background:var(--iris);opacity:.85;border-top:0}
.fd .rech{margin:0 0 8px}
.fd .rech input{width:100%;padding:8px 11px;font-family:inherit;font-size:13px;border:1px solid var(--line);
 border-radius:7px;background:var(--surface);color:var(--ink)}
.fcard{background:var(--surface);border:1px solid var(--line);border-left:4px solid var(--iris);
border-radius:10px;padding:17px 19px;display:flex;flex-direction:column;gap:13px}
.fcard header{display:flex;align-items:flex-start;gap:10px}
.fcard h3{margin:0;font-size:18px;font-weight:700;letter-spacing:-.02em;line-height:1.2;flex:1;min-width:0}
.fcard .rs{font-size:11.5px;color:var(--ink-3);margin-top:2px;line-height:1.4}
.fk{display:grid;grid-template-columns:repeat(3,1fr);gap:10px 12px}
.fk div{display:flex;flex-direction:column;gap:1px;min-width:0}
.fk span{font-family:Inter,sans-serif;font-size:9px;letter-spacing:.11em;text-transform:uppercase;
color:var(--ink-2);font-weight:700}
.fk b{font-family:Inter,sans-serif;font-size:17px;font-weight:700;letter-spacing:-.03em;
font-variant-numeric:tabular-nums;line-height:1.1}
.coord{font-size:12.5px;color:var(--ink-2);line-height:1.65;background:var(--surface-2);
border-radius:7px;padding:11px 13px}
.coord div{display:flex;gap:7px}
.coord i{font-style:normal;color:var(--ink-3);flex:0 0 62px;font-size:11.5px}
.coord a{color:var(--iris);text-decoration:none}
.coord a:hover{text-decoration:underline}
.fnote{font-size:12px;color:var(--ink-3);line-height:1.55;font-style:italic}
.fmv{font-size:12.5px;line-height:1.55;border-radius:7px;padding:10px 12px}
.fmv.b{background:var(--good-soft);color:var(--good);font-weight:500}
.fmv.h{background:var(--crit-soft);color:var(--crit);font-weight:500}

.tbl{width:100%;border-collapse:collapse;font-size:13px;background:var(--surface);
border:1px solid var(--line);border-radius:9px;overflow:hidden}
.tbl th{text-align:left;font-family:Inter,sans-serif;font-size:9.5px;letter-spacing:.11em;
text-transform:uppercase;color:var(--ink-2);font-weight:700;padding:11px 13px;
background:var(--surface-2);border-bottom:1px solid var(--line);white-space:nowrap}
.tbl td{padding:11px 13px;border-bottom:1px solid var(--line-2);vertical-align:top}
.tbl tbody tr:last-child td{border-bottom:0}
.tbl tbody tr:hover{background:var(--surface-2)}
.tbl td.n{font-family:Inter,sans-serif;text-align:right;font-variant-numeric:tabular-nums;
white-space:nowrap;font-weight:600}
.tbl .ref b{display:block;font-weight:600}
.tbl .ref span{color:var(--ink-3);font-size:11px;font-family:Inter,sans-serif}
.tbl .win{color:var(--good);font-weight:700}
.tbl .lose{color:var(--crit);font-weight:700}
.wrapx{overflow-x:auto}
.vide{border:2px dashed var(--line);border-radius:12px;padding:40px 32px;text-align:center;
background:var(--surface-2);max-width:66ch;margin:16px auto}
.vide h3{margin:0 0 11px;font-size:20px;font-weight:700;letter-spacing:-.02em}
.vide p{margin:0 0 14px;font-size:14px;color:var(--ink-2);line-height:1.65}
.vide .btn{margin:2px 4px}
/* déposer n'importe quel document sur la page : le voile pendant le glisser */
.dpz{position:fixed;inset:0;z-index:60;background:rgba(91,75,138,.14);border:4px dashed var(--iris);display:none;align-items:center;justify-content:center;pointer-events:none}
.dpz.on{display:flex}
.dpz>div{background:var(--surface);border-radius:14px;padding:22px 30px;text-align:center;box-shadow:0 10px 40px rgba(0,0,0,.15)}
.dpz b{display:block;font-size:18px;margin-bottom:4px}.dpz span{font-size:13px;color:var(--ink-2)}
#dp-deja{color:var(--warn)}
'''

CORPS = r'''
<div class="tools">
  <a class="btn pri" href="factures.html">Enregistrer une facture</a>
  <button class="btn" id="depot" title="Une facture, une price list, un listing, une carte de visite en photo : l'outil lit le nom et les coordonnées, et crée le fournisseur">Déposer un document</button>
  <input type="file" id="dfich" accept="__ACCEPT__" hidden>
  <button class="btn" id="nouv">+ Nouveau fournisseur</button>
  <span id="exp"></span>
  <span class="sp"></span>
  <select id="tri" class="sel">
    <option value="mt">Trier par montant acheté</option>
    <option value="nb">Par nombre de références</option>
    <option value="dt">Par date de dernière facture</option></select>
</div>
<div id="kpis"></div>
<div id="corps"></div>

<div class="dpz" id="dpz"><div><b>Dépose le document ici</b><span>facture, price list, listing, photo d'une carte de visite…</span></div></div>
<div class="ov" id="dpov"><div class="mod" style="max-width:580px">
  <div class="mh"><h2 id="dp-titre">Document lu</h2><button class="x" id="dp-x">&times;</button></div>
  <div class="mb">
    <p class="hint" id="dp-quoi" style="margin:0 0 12px"></p>
    <div class="fg2">
      <div class="fld"><label for="dp-nom">Nom du fournisseur</label><input id="dp-nom" autocomplete="off"></div>
      <div class="fld"><label for="dp-email">E-mail</label><input id="dp-email" autocomplete="off"></div>
    </div>
    <div class="fg2">
      <div class="fld"><label for="dp-tel">Téléphone</label><input id="dp-tel" autocomplete="off"></div>
      <div class="fld"><label for="dp-site">Site web</label><input id="dp-site" autocomplete="off"></div>
    </div>
    <p class="hint" id="dp-deja" style="margin:0" hidden></p>
  </div>
  <div class="mf"><span class="msg" id="dp-msg"></span>
    <button class="btn" id="dp-non">Annuler</button>
    <button class="btn" id="dp-fiche">Créer la fiche</button>
    <button class="btn pri" id="dp-suite" hidden></button></div>
</div></div>
<div class="ov" id="frov"><div class="mod" style="max-width:600px;max-height:88vh;display:flex;flex-direction:column">
  <div class="mh"><h2 id="fr-titre">Nouveau fournisseur</h2><button class="x" id="fr-x">&times;</button></div>
  <div class="mb" style="overflow:auto;flex:1;min-height:0">
    <div class="fg2">
      <div class="fld"><label for="fr-nom">Nom court <i>(celui qu'on voit partout)</i></label><input id="fr-nom" autocomplete="off" placeholder="Miami Trading Zone"></div>
      <div class="fld"><label for="fr-raison">Raison sociale</label><input id="fr-raison" autocomplete="off" placeholder="Miami Trading Zone Group LLC"></div>
    </div>
    <div class="fld"><label for="fr-adresse">Adresse</label><input id="fr-adresse" autocomplete="off"></div>
    <div class="fg2">
      <div class="fld"><label for="fr-tel">Téléphone</label><input id="fr-tel" autocomplete="off"></div>
      <div class="fld"><label for="fr-email">E-mail</label><input id="fr-email" autocomplete="off"></div>
    </div>
    <div class="fg2">
      <div class="fld"><label for="fr-contact">Personne de contact</label><input id="fr-contact" autocomplete="off" placeholder="Alejandra Pombo — alejandra@…"></div>
      <div class="fld"><label for="fr-site">Site web</label><input id="fr-site" autocomplete="off"></div>
    </div>
    <div class="fld"><label for="fr-note">Note libre <i>(conditions, délais, incidents)</i></label>
      <textarea id="fr-note" rows="3" style="min-height:70px"></textarea></div>
    <p class="hint" style="margin:0">Un fournisseur créé ici apparaît tout de suite dans la liste, avec zéro facture.
    Ses achats viendront des factures que tu enregistres à son nom.</p>
    <p class="hint" style="margin:8px 0 0"><b>Tu as sa facture sous la main ?</b> Le plus court : la déposer dans
    <a href="factures.html?sens=achat">Factures</a> — le fournisseur est reconnu ou créé, et ses coordonnées
    se complètent ici après.</p>
  </div>
  <div class="mf" style="flex:none"><span class="msg" id="fr-msg"></span>
    <button class="btn" id="fr-non">Annuler</button>
    <button class="btn pri" id="fr-ok">Enregistrer</button></div>
</div></div>
'''

JS = r'''
const IDX=__IDX__, FRN_INIT=__FRNINIT__;
/* Le type (EDT, EDP, OIL…) et le genre, comme partout ailleurs. */
const GEN={M:'Homme',W:'Femme',U:'Unisexe',K:'Enfant'};
const tyBadge=cle=>{ const v=IDX[cle]||[]; const t=String(v[6]||'').trim(), g=GEN[String(v[7]||'').trim().toUpperCase()]||'';
  return (t?' <i class="ty" data-nolang>'+esc(t)+'</i>':'')+(g?' <i class="gn">'+esc(g)+'</i>':''); };
const KHIST='prix-achat-hist-v1', KFRN='fournisseurs-v1', KUSR='crm-utilisateur-v1', KJOU='crm-journal-v1',
      KMOD='fiches-modifiees-v1', KEXT='stock-externe-v1';
let HIST=lit(KHIST,{}); if(!HIST||typeof HIST!=='object'||Array.isArray(HIST)) HIST=base(KHIST,{});
let FRN =lit(KFRN ,{}); if(!FRN ||typeof FRN !=='object'||Array.isArray(FRN )) FRN =base(KFRN ,{});
/* Les price lists reçues (Étude de devis, magasin etudes-devis-v1) : rattachées au
   fournisseur par son nom. Igal, 12 sept. 2026 : « le répertoire fournisseur avec
   ses price lists enregistrées et comparées avec nos informations ». */
const KETU='etudes-devis-v1';
let ETU=lit(KETU,[]); if(!Array.isArray(ETU)) ETU=[];
const cNorm=s=>String(s==null?'':s).toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/[^a-z0-9]+/g,' ').trim();
const etudesDe=nom=>ETU.filter(e=>e&&cNorm(e.frn)===cNorm(nom)).sort((a,b)=>(b.d||'').localeCompare(a.d||'')||(b.t||'').localeCompare(a.t||''));
/* notre prix habituel : la moyenne pondérée de ce qu'on a vraiment payé (factures) */
const notrePrix=cle=>{ const l=(HIST[cle]||[]).filter(a=>a.src!=='fichier'&&a.p>0); const q=l.reduce((s,a)=>s+(+a.q||0),0);
  if(!l.length) return {moy:null,der:null,n:0}; const moy=q?l.reduce((s,a)=>s+a.p*(+a.q||0),0)/q:l.reduce((s,a)=>s+a.p,0)/l.length;
  const der=l.slice().sort((a,b)=>(a.d||'').localeCompare(b.d||'')).pop(); return {moy,der:der?der.p:null,n:l.length}; };
let USR=NOM_UTIL;
window.__nomChange.push(v=>{ USR=v; try{ majUser(); }catch(e){} });
/* le stock en vigueur : la fiche corrigée l'emporte sur le fichier d'inventaire,
   sinon cette page annonçait un « argent en jeu » calculé sur des quantités périmées */
let MOD={}; try{ MOD=JSON.parse(localStorage.getItem(KMOD)||'{}')||{}; }catch(e){ MOD={}; }
let EXT={q:{}}; try{ EXT=Object.assign({q:{}},JSON.parse(localStorage.getItem(KEXT)||'{}')); }catch(e){}
if(!EXT.q) EXT.q={};
const qteEff=cle=>{ const m=MOD[cle]; if(m&&m.qte!=null) return +m.qte;
  const inf=IDX[cle]||[]; const e=EXT.q[inf[0]]; return e!=null?+e:(inf[4]||0); };
const sauveFRN=()=>ecrit(KFRN,FRN);
(function(){ let n=0; Object.entries(FRN_INIT).forEach(([k,v])=>{
    if(!FRN[k]) { FRN[k]=v; n++; } else FRN[k]=Object.assign({},v,FRN[k]); });
  if(n) sauveFRN(); })();

/* 30 sept. 2026 (Igal : « supprime le fournisseur Galou ») : le fournisseur de démonstration
   n'est plus posé. Il l'était une fois PAR NAVIGATEUR — un nouveau poste le recréait. Celui
   qui existait a été retiré du serveur, avec ses prix inventés (copie dans corbeille-v1). */
function retireDemo(nom){
  if(!confirm('Retirer « '+nom+' » et ses factures de démonstration ? Rien d\'autre ne bouge.')) return;
  Object.keys(HIST).forEach(k=>{ HIST[k]=(HIST[k]||[]).filter(a=>!(a.demo&&a.f===nom)); if(!HIST[k].length) delete HIST[k]; });
  ecrit(KHIST,HIST); delete FRN[nom]; sauveFRN();
  const ov=document.getElementById('fdov'); if(ov) ov.classList.remove('on');
  dessine();
}

/* Un fournisseur ne se saisit pas : il tombe des factures enregistrées. */
function agrege(){
  const F={};
  Object.entries(HIST).forEach(([cle,l])=>{
    l.forEach(a=>{
      if(!a.f || a.src==='fichier') return;
      const f=(F[a.f]=F[a.f]||{nom:a.f,refs:new Set(),lignes:0,montant:0,factures:new Set(),
                                der:null,prem:null,mouv:[]});
      f.refs.add(cle); f.lignes++;
      f.montant += (a.q||0)*a.p;
      if(a.num) f.factures.add(a.num);
      if(!f.der||a.d>f.der) f.der=a.d;
      if(!f.prem||a.d<f.prem) f.prem=a.d;
      f.mouv.push({cle,d:a.d,p:a.p,q:a.q,num:a.num||''});
    });
  });
  /* Un fournisseur dont on connaît les coordonnées existe, même sans facture. */
  Object.keys(FRN).forEach(n=>{ if(!F[n]) F[n]={nom:n,refs:new Set(),lignes:0,montant:0,
    factures:new Set(),der:null,prem:null,mouv:[]}; });
  ETU.forEach(e=>{ if(!e||!e.frn||/non précisé/.test(e.frn)) return; const n=Object.keys(F).find(k=>cNorm(k)===cNorm(e.frn))||e.frn;
    if(!F[n]) F[n]={nom:n,refs:new Set(),lignes:0,montant:0,factures:new Set(),der:null,prem:null,mouv:[]}; });
  return Object.values(F).map(f=>{
    f.nrefs=f.refs.size;
    return f;
  });
}

/* Pour chaque référence achetée chez plusieurs fournisseurs : qui est le moins cher. */
function comparatif(){
  const R=[];
  Object.entries(HIST).forEach(([cle,l])=>{
    const par={};
    l.forEach(a=>{ if(!a.f||a.src==='fichier') return;
      if(!par[a.f] || a.d>=par[a.f].d) par[a.f]={p:a.p,d:a.d,q:a.q}; });
    const noms=Object.keys(par);
    if(noms.length<2) return;
    const tri=noms.map(n=>({n,...par[n]})).sort((a,b)=>a.p-b.p);
    const bas=tri[0], haut=tri[tri.length-1];
    const inf=IDX[cle]||[];
    const qte=qteEff(cle);
    R.push({cle,bc:inf[0],nom:inf[1],marque:inf[2],qte,
            bas,haut,ecart:haut.p-bas.p,pct:haut.p?(haut.p-bas.p)/haut.p*100:0,
            enjeu:(haut.p-bas.p)*qte,n:noms.length});
  });
  return R.sort((a,b)=>b.enjeu-a.enjeu||b.ecart-a.ecart);
}

function carte(f){
  const c=FRN[f.nom]||{};
  const m=f.mouv.slice().sort((a,b)=>a.d.localeCompare(b.d));
  /* mouvement de prix : on compare le premier et le dernier prix de chaque référence */
  const parRef={};
  m.forEach(x=>{ (parRef[x.cle]=parRef[x.cle]||[]).push(x); });
  let baisses=0,hausses=0,gain=0;
  Object.values(parRef).forEach(l=>{ if(l.length<2) return;
    const d=l[l.length-1].p-l[0].p;
    if(d<0) baisses++; else if(d>0) hausses++;
    gain += d*qteEff(l[0].cle); });
  const lig=[];
  if(c.raison&&c.raison!==f.nom) lig.push(['','<b>'+esc(c.raison)+'</b>']);
  if(c.adresse) lig.push(['Adresse',esc(c.adresse)]);
  if(c.tel) lig.push(['Téléphone',esc(c.tel)]);
  if(c.email) lig.push(['E-mail',`<a href="mailto:${esc(c.email)}">${esc(c.email)}</a>`]);
  if(c.site) lig.push(['Site',esc(c.site)]);
  if(c.contact) lig.push(['Contact',esc(c.contact)]);
  const dfr=d=>{ if(!d) return '—'; const [a,mo,j]=d.split('-'); return mo+'/'+j+'/'+a.slice(2); };
  return `<article class="fcard ouvrable" data-fiche="${esc(f.nom)}" title="Ouvrir la fiche détaillée">
    <header><div style="flex:1;min-width:0"><h3>${esc(f.nom)}</h3>
      <div class="rs">${f.factures.size?`${f.factures.size} facture${f.factures.size>1?'s':''} · `:''}dernière le ${dfr(f.der)}</div></div>
      <button class="btn" data-ecr="${esc(f.nom)}" style="padding:5px 11px;font-size:12px">Écrire</button>
      <button class="btn" data-ed="${esc(f.nom)}" style="padding:5px 11px;font-size:12px">Modifier</button></header>
    ${c.demo?'<div class="demotag" style="margin-top:0">Démonstration — chiffres inventés</div>':''}
    <div class="fk">
      <div><span>références</span><b>${nf(f.nrefs)}</b></div>
      <div><span>lignes</span><b>${nf(f.lignes)}</b></div>
      <div><span>montant</span><b style="color:var(--iris)">${money(f.montant)}</b></div>
      <div><span>price lists</span><b>${nf(etudesDe(f.nom).length)}</b></div>
    </div>
    ${lig.length?`<div class="coord">${lig.map(([k,v])=>`<div><i>${k}</i><span>${v}</span></div>`).join('')}</div>`:''}
    ${(baisses||hausses)?`<div class="fmv ${gain<0?'b':'h'}">${
      baisses?`${baisses} référence${baisses>1?'s ont':' a'} baissé`:''}${baisses&&hausses?', ':''}${
      hausses?`${hausses} ${hausses>1?'ont':'a'} augmenté`:''} chez lui.
      Sur le stock actuel, ça représente ${gain<0?'une économie':'un surcoût'} de <b>${money(Math.abs(gain))}</b>.</div>`:''}
    ${c.note?`<div class="fnote">${esc(c.note)}</div>`:''}
  </article>`;
}

/* ---------- les price lists d'un fournisseur, comparées en direct ---------- */
/* La comparaison n'est pas celle du jour où la liste a été lue : elle est refaite
   maintenant, avec le prix qu'on paie d'habitude (nos factures) et le stock
   d'aujourd'hui. Une price list de mars comparée aux prix de mars ne dit rien
   en septembre. */
function priceListsHTML(nom){
  const L=etudesDe(nom);
  const dfr=d=>{ if(!d) return '—'; const [a,mo,j]=String(d).slice(0,10).split('-'); return mo+'/'+j+'/'+a.slice(2); };
  if(!L.length) return `<div style="padding:12px;color:var(--ink-3);font-size:13px">Aucune price list enregistrée pour lui. « Déposer une price list » lit son devis et le compare à nos prix.</div>`;
  return `<div class="facs">${L.map((e,i)=>{
    const lignes=(e.lignes||[]).map(l=>{ const np=l.cle?notrePrix(l.cle):{moy:null,der:null,n:0}; const stock=l.cle?qteEff(l.cle):null;
      const ecart=(np.moy&&l.p)?(l.p-np.moy)/np.moy*100:null;
      const v=ecart==null?(l.cle?'inc':'inc'):ecart<=-3?'bon':ecart>=3?'cher':'ok';
      return Object.assign({},l,{np,stock,ecart,v}); });
    const nBon=lignes.filter(l=>l.v==='bon').length, nCher=lignes.filter(l=>l.v==='cher').length, nInc=lignes.filter(l=>l.v==='inc').length;
    const eco=lignes.reduce((s,l)=>s+((l.np.moy&&l.p)?(l.np.moy-l.p)*(l.q||1):0),0);
    return `<div class="fac" data-pl="${i}">
        <span class="fnum">${esc(e.num||'price list')}</span><span class="fdate">${dfr(e.d)}</span>
        <span class="fdet">${nf(lignes.length)} référence${lignes.length>1?'s':''} · <span class="dn">${nBon} moins ch${nBon>1?'ères':'ère'}</span> · <span class="up">${nCher} plus ch${nCher>1?'ères':'ère'}</span>${nInc?` · ${nInc} jamais acheté${nInc>1?'es':'e'}`:''}${e.par?' · lue par <span data-nolang>'+esc(e.par)+'</span>':''}</span>
        <b class="fmt">${money(e.montant||0)}</b></div>
      <div class="det" data-pld="${i}" hidden><table><thead><tr><th>Référence</th><th class="n">Qté</th><th class="n">Son prix</th><th class="n">Notre prix habituel</th><th class="n">Écart</th><th class="n">Stock</th><th>Verdict</th></tr></thead>
        <tbody>${lignes.map(l=>{ const vI=IDX[l.cle]||[]; const ref=l.cle?((vI[2]||'')+' '+(vI[1]||'')):(l.ref||l.bc||'?');
          return `<tr><td class="pr"><b data-nolang>${esc(ref)}${tyBadge(l.cle)}</b><span>${esc(l.bc||'')}</span></td>
            <td class="n">${l.q!=null?nf(l.q):'—'}</td><td class="n"><b>${l.p!=null?money2(l.p):'—'}</td>
            <td class="n">${l.np.moy!=null?money2(l.np.moy)+(l.np.der!=null&&Math.abs(l.np.der-l.np.moy)>0.005?`<span style="display:block;font-size:11px;color:var(--ink-3)">dernier ${money2(l.np.der)}</span>`:''):'<span style="color:var(--ink-3)">jamais acheté</span>'}</td>
            <td class="n">${l.ecart==null?'—':`<span class="${l.ecart<0?'dn':l.ecart>0?'up':'eq'}">${l.ecart>0?'+':''}${l.ecart.toFixed(1).replace('.',',')} %</span>`}</td>
            <td class="n">${l.stock!=null?nf(l.stock):'—'}</td>
            <td>${l.v==='bon'?'<span class="dn">bon prix</span>':l.v==='cher'?'<span class="up">plus cher que d\'habitude</span>':l.v==='ok'?'<span class="eq">dans les prix</span>':'<span style="color:var(--ink-3)">pas de repère</span>'}</td></tr>`; }).join('')}</tbody></table>
        <div style="padding:8px 12px;font-size:12.5px;color:var(--ink-2)">${eco>=0?'Économie':'Surcoût'} sur cette liste, aux quantités proposées : <b>${money(Math.abs(eco))}</b>. <a href="etude.html?etude=${encodeURIComponent(e.id)}">Rouvrir dans l'Étude</a></div></div>`; }).join('')}</div>`;
}

/* ---------- la fiche détaillée d'un fournisseur ---------- */
function ficheHTML(f){
  const c=FRN[f.nom]||{};
  const dfr=d=>{ if(!d) return '—'; const [a,mo,j]=d.split('-'); return mo+'/'+j+'/'+a.slice(2); };
  const m=f.mouv.slice().sort((a,b)=>a.d.localeCompare(b.d)||String(a.num).localeCompare(String(b.num)));

  /* les factures, avec leurs lignes */
  const parFac={};
  m.forEach(x=>{ const k=(x.num||'sans n°')+'|'+x.d;
    (parFac[k]=parFac[k]||{num:x.num||'sans n°',d:x.d,l:[],q:0,t:0}).l.push(x);
    parFac[k].q+=x.q||0; parFac[k].t+=(x.q||0)*x.p; });
  const facs=Object.values(parFac).sort((a,b)=>b.d.localeCompare(a.d));

  /* les produits : combien de fois, combien de flacons, premier et dernier prix */
  const parP={};
  m.forEach(x=>{ const p=(parP[x.cle]=parP[x.cle]||{cle:x.cle,fois:0,q:0,t:0,p0:null,p1:null,d0:x.d,d1:x.d,pmin:x.p,pmax:x.p});
    p.fois++; p.q+=x.q||0; p.t+=(x.q||0)*x.p;
    if(p.p0==null) p.p0=x.p; p.p1=x.p; p.d1=x.d;
    p.pmin=Math.min(p.pmin,x.p); p.pmax=Math.max(p.pmax,x.p); });
  const prods=Object.values(parP).sort((a,b)=>b.t-a.t);

  /* les douze derniers mois */
  const now=new Date(), mois=[];
  for(let i=11;i>=0;i--){ const d=new Date(now.getFullYear(),now.getMonth()-i,1);
    mois.push({k:d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0'), lib:d.toLocaleDateString((typeof lgLocale==='function'?lgLocale():'fr-FR'),{month:'short'}), t:0}); }
  m.forEach(x=>{ const k=(x.d||'').slice(0,7); const mm=mois.find(o=>o.k===k); if(mm) mm.t+=(x.q||0)*x.p; });
  const maxM=Math.max(1,...mois.map(o=>o.t));

  const evol=p=>{ if(p.fois<2||p.p0==null) return '<span class="eq">—</span>';
    const d=p.p1-p.p0; if(Math.abs(d)<0.005) return '<span class="eq">stable</span>';
    const pc=p.p0?d/p.p0*100:0;
    return `<span class="${d>0?'up':'dn'}">${d>0?'+':''}${money2(d)} · ${(pc>0?'+':'')+pc.toFixed(1).replace('.',',')} %</span>`; };
  const coord=[c.raison&&c.raison!==f.nom?['Société',c.raison]:null, c.adresse?['Adresse',c.adresse]:null,
    c.tel?['Téléphone',c.tel]:null, c.email?['E-mail',c.email]:null, c.contact?['Contact',c.contact]:null,
    c.site?['Site',c.site]:null].filter(Boolean);
  const nbHausse=prods.filter(p=>p.fois>1&&p.p1>p.p0+0.005).length, nbBaisse=prods.filter(p=>p.fois>1&&p.p1<p.p0-0.005).length;

  return `<div class="mh"><h2 style="font-size:15px;margin:0">Fiche fournisseur</h2><button class="x" id="fd-x">&times;</button></div>
  <div class="mb">
    <div class="fd-top">
      <div class="id"><h2>${esc(f.nom)}</h2>
        <div class="rs">${f.factures.size?nf(f.factures.size)+' facture'+(f.factures.size>1?'s':'')+' · ':''}
          ${f.prem?'depuis le '+dfr(f.prem)+' · ':''}dernière le ${dfr(f.der)}</div>
        <div style="margin-top:10px;display:flex;gap:8px;flex-wrap:wrap">
          <button class="btn" data-ecr2="${esc(f.nom)}" style="padding:6px 12px;font-size:12.5px">Écrire</button>
          <button class="btn" data-ed2="${esc(f.nom)}" style="padding:6px 12px;font-size:12.5px">Modifier la fiche</button>
          <a class="btn pri" href="factures.html?sens=achat&frn=${encodeURIComponent(f.nom)}" style="padding:6px 12px;font-size:12.5px;text-decoration:none">Déposer une facture</a>
          <a class="btn" href="etude.html?frn=${encodeURIComponent(f.nom)}" style="padding:6px 12px;font-size:12.5px;text-decoration:none" title="Un devis ou une price list de ce fournisseur : l'outil le lit et le compare à nos prix">Déposer une price list</a>
          ${c.demo?`<button class="btn" data-demo2="${esc(f.nom)}" style="padding:6px 12px;font-size:12.5px;color:var(--crit)">Retirer cette démonstration</button>`:''}</div>
        ${c.demo?'<div class="demotag">Fournisseur de démonstration — chiffres inventés</div>':''}</div>
      ${coord.length?`<div class="co">${coord.map(([k,v])=>`<div><i>${k}</i>${esc(v)}</div>`).join('')}</div>`:''}
    </div>
    <div class="fd-k">
      <div><b style="color:var(--iris)">${money(f.montant)}</b><span>acheté chez lui au total</span></div>
      <div><b>${nf(f.factures.size)}</b><span>facture${f.factures.size>1?'s':''}</span></div>
      <div><b>${nf(f.nrefs)}</b><span>références différentes</span></div>
      <div><b>${nf(m.reduce((a,x)=>a+(x.q||0),0))}</b><span>flacons reçus</span></div>
      <div><b>${f.factures.size?money(f.montant/f.factures.size):'—'}</b><span>par facture en moyenne</span></div>
      <div><b class="${nbHausse>nbBaisse?'up':nbBaisse?'dn':''}">${nbHausse?'+'+nbHausse:''}${nbHausse&&nbBaisse?' / ':''}${nbBaisse?'−'+nbBaisse:''}${!nbHausse&&!nbBaisse?'—':''}</b><span>prix montés / baissés</span></div>
    </div>

    <h3>Achats par mois <em>douze derniers mois</em></h3>
    <div class="mois">${mois.map(o=>`<div><b>${o.t?money(o.t):''}</b><i style="height:${Math.max(2,Math.round(o.t/maxM*46))}px"></i><span>${o.lib}</span></div>`).join('')}</div>

    <h3>Factures <em>clique une facture pour voir son contenu</em></h3>
    <div class="facs">${facs.map((x,i)=>`<div class="fac" data-f="${i}">
        <span class="fnum">${esc(x.num)}</span><span class="fdate">${dfr(x.d)}</span>
        <span class="fdet">${nf(x.l.length)} ligne${x.l.length>1?'s':''} · ${nf(x.q)} flacon${x.q>1?'s':''}</span>
        <b class="fmt">${money(x.t)}</b></div>
      <div class="det" data-fd="${i}" hidden><table><thead><tr><th>Produit</th><th class="n">Qté</th><th class="n">PU</th><th class="n">Total</th></tr></thead>
        <tbody>${x.l.map(l=>{ const v=IDX[l.cle]||[]; return `<tr><td class="pr"><b>${esc(v[2]||'')} ${esc(v[1]||l.cle)}${tyBadge(l.cle)}</b><span>${esc(v[0]||'')}</span></td>
          <td class="n">${nf(l.q||0)}</td><td class="n">${money2(l.p)}</td><td class="n">${money2((l.q||0)*l.p)}</td></tr>`; }).join('')}</tbody></table></div>`).join('')||
      '<div style="padding:12px;color:var(--ink-3);font-size:13px">Aucune facture enregistrée — seulement des coordonnées.</div>'}</div>

    <h3>Ses price lists <em>ce qu'il propose, comparé à ce qu'on paie d'habitude et au stock d'aujourd'hui</em></h3>
    ${priceListsHTML(f.nom)}

    <h3>Produits achetés <em>${nf(prods.length)} référence${prods.length>1?'s':''}, du plus gros montant au plus petit</em></h3>
    ${prods.length>8?'<div class="rech"><input id="fd-q" placeholder="Filtrer les produits…"></div>':''}
    <div class="tw"><table id="fd-prods"><thead><tr><th class="pr">Produit</th><th class="n">Fois</th><th class="n">Flacons</th><th class="n">Total</th>
      <th class="n">Premier PU</th><th class="n">Dernier PU</th><th class="n">Évolution</th><th class="n">Dernier achat</th></tr></thead>
    <tbody>${prods.map(p=>{ const v=IDX[p.cle]||[]; return `<tr data-t="${esc(((v[2]||'')+' '+(v[1]||'')+' '+(v[0]||'')).toLowerCase())}">
        <td class="pr"><b>${esc(v[2]||'')} ${esc(v[1]||p.cle)}</b><span>${esc(v[0]||'')}</span></td>
        <td class="n">${nf(p.fois)}</td><td class="n">${nf(p.q)}</td><td class="n"><b>${money(p.t)}</b></td>
        <td class="n">${money2(p.p0)}</td><td class="n">${money2(p.p1)}</td><td class="n">${evol(p)}</td><td class="n">${dfr(p.d1)}</td></tr>`; }).join('')}</tbody></table></div>
  </div>`;
}
function ouvreFiche(nom){
  const f=agrege().find(x=>x.nom===nom); if(!f) return;
  let ov=document.getElementById('fdov');
  if(!ov){ ov=document.createElement('div'); ov.className='ov'; ov.id='fdov';
    ov.innerHTML='<div class="mod fd"></div>'; document.body.appendChild(ov);
    ov.addEventListener('click',e=>{ if(e.target===ov) ov.classList.remove('on'); }); }
  const mod=ov.querySelector('.mod'); mod.innerHTML=ficheHTML(f);
  mod.querySelector('#fd-x').onclick=()=>ov.classList.remove('on');
  mod.querySelectorAll('.fac').forEach(tr=>tr.onclick=()=>{
    const d=tr.dataset.f!==undefined?mod.querySelector('.det[data-fd="'+tr.dataset.f+'"]'):mod.querySelector('.det[data-pld="'+tr.dataset.pl+'"]');
    if(!d) return; d.hidden=!d.hidden; tr.classList.toggle('on',!d.hidden); });
  const q=mod.querySelector('#fd-q'); if(q) q.oninput=()=>{ const t=q.value.trim().toLowerCase();
    mod.querySelectorAll('#fd-prods tbody tr').forEach(tr=>{ tr.hidden=t&&!tr.dataset.t.includes(t); }); };
  const e=mod.querySelector('[data-ecr2]'); if(e) e.onclick=()=>ecrire(nom);
  const ed=mod.querySelector('[data-ed2]'); if(ed) ed.onclick=()=>{ ov.classList.remove('on'); edite(nom); };
  const dm=mod.querySelector('[data-demo2]'); if(dm) dm.onclick=()=>retireDemo(nom);
  ov.classList.add('on'); mod.querySelector('.mb').scrollTop=0;
}

function dessine(){
  const F=agrege();
  const tri=$('tri').value;
  F.sort((a,b)=> tri==='nb'?b.nrefs-a.nrefs : tri==='dt'?(b.der||'').localeCompare(a.der||'') : b.montant-a.montant);
  const nref=new Set(); F.forEach(f=>f.refs.forEach(r=>nref.add(r)));
  const cmp=comparatif();
  const enjeu=cmp.reduce((a,x)=>a+x.enjeu,0);

  $('kpis').innerHTML=`<div class="kpis">
    <div class="kpi"><span class="v">${nf(F.length)}</span><span class="k">fournisseur${F.length>1?'s':''}</span></div>
    <div class="kpi"><span class="v">${nf(nref.size)}</span><span class="k">références achetées</span></div>
    <div class="kpi"><span class="v" style="color:var(--iris)">${money(F.reduce((a,f)=>a+f.montant,0))}</span><span class="k">montant enregistré</span></div>
    <div class="kpi"><span class="v">${nf(cmp.length)}</span><span class="k">références à plusieurs fournisseurs</span></div>
    ${cmp.length?`<div class="kpi"><span class="v" style="color:var(--crit)">${money(enjeu)}</span><span class="k">en jeu sur le stock actuel</span></div>`:''}
  </div>`;

  if(!F.length){
    $('corps').innerHTML=`<div class="vide"><h3>Aucun fournisseur enregistré</h3>
      <p>Un fournisseur ne se tape pas : il tombe des factures. Enregistre une facture
      dans le catalogue — colle les lignes, indique le nom et la date — et sa fiche
      apparaît ici avec ce qu'il t'a vendu, à quel prix, et comment ses prix bougent.</p>
      <p>Les codes-barres déjà connus alimentent l'historique de prix du produit.
      Aucun doublon n'est créé.</p>
      <p><a class="btn pri" href="catalogue.html">Ouvrir le catalogue</a></p></div>`;
    $('src').innerHTML='';
    return;
  }
  const dfr=d=>{ if(!d) return '—'; const [a,m,j]=d.split('-'); return m+'/'+j+'/'+a.slice(2); };
  $('corps').innerHTML=`
    <h2 class="sec">Les fournisseurs <em>${F.length} · alimentés par les factures enregistrées</em></h2>
    <div class="fgrid">${F.map(carte).join('')}</div>
    ${cmp.length?`
    <h2 class="sec">Références achetées chez plusieurs fournisseurs
      <em>classées par l'argent en jeu sur le stock actuel</em></h2>
    <div class="wrapx"><table class="tbl"><thead><tr>
      <th>Référence</th><th style="text-align:right">Stock</th>
      <th>Le moins cher</th><th style="text-align:right">Prix</th>
      <th>Le plus cher</th><th style="text-align:right">Prix</th>
      <th style="text-align:right">Écart</th><th style="text-align:right">En jeu</th>
      </tr></thead><tbody>${cmp.map(x=>`<tr>
      <td class="ref"><b>${esc(x.marque||'')} ${esc(x.nom||'')}</b><span>${esc(x.bc||'')}</span></td>
      <td class="n">${nf(x.qte||0)}</td>
      <td class="win">${esc(x.bas.n)}</td><td class="n win">${money2(x.bas.p)}</td>
      <td class="lose">${esc(x.haut.n)}</td><td class="n lose">${money2(x.haut.p)}</td>
      <td class="n">${money2(x.ecart)} · ${x.pct.toFixed(1).replace('.',',')} %</td>
      <td class="n">${money(x.enjeu)}</td></tr>`).join('')}</tbody></table></div>`
    :`<h2 class="sec">Comparaison entre fournisseurs</h2>
      <div class="vide" style="padding:26px"><p style="margin:0">Aucune référence n'est encore achetée
      chez deux fournisseurs différents. C'est en enregistrant les factures de chacun que la comparaison
      devient possible — et c'est là que se trouve l'argent.</p></div>`}`;
  $('src').innerHTML=`${nf(F.length)} fournisseur${F.length>1?'s':''}<br>${nf(Object.values(HIST).reduce((a,l)=>a+l.filter(x=>x.src!=='fichier').length,0))} lignes de facture`;
  document.querySelectorAll('[data-ed]').forEach(b=>b.onclick=ev=>{ ev.stopPropagation(); edite(b.dataset.ed); });
  document.querySelectorAll('[data-ecr]').forEach(b=>b.onclick=ev=>{ ev.stopPropagation(); ecrire(b.dataset.ecr); });
  document.querySelectorAll('.fcard[data-fiche]').forEach(a=>a.onclick=ev=>{
    if(ev.target.closest('button,a')) return; ouvreFiche(a.dataset.fiche); });
}

/* Écrire à un fournisseur : la même fenêtre que partout ailleurs. Une adresse
   corrigée dans la fenêtre revient dans la fiche du fournisseur. */
function jlogContact(nom,par,quoi){
  const J=lit(KJOU,[]);
  J.push({t:new Date().toISOString(),u:USR||'(non renseigné)',act:'contact',
          lib:'message préparé — '+quoi,ref:nom,av:null,ap:par});
  ecrit(KJOU,J);
}
function ecrire(nom){
  const c=FRN[nom]||{};
  contacte({nom, email:c.email, tel:c.tel, modele:'libre',
    modeles:['libre','relance','merci'],
    onSave:(mail,tel)=>{
      if(mail===(c.email||'') && tel===(c.tel||'')) return;
      const o=Object.assign({nom},FRN[nom]||{});
      if(mail) o.email=mail; else delete o.email;
      if(tel)  o.tel=tel;   else delete o.tel;
      FRN[nom]=o; sauveFRN(); dessine();
    }});
}

const FR_CH=['raison','adresse','tel','email','contact','site','note'];
let FR_EDIT=null;
function formFrn(nom){
  FR_EDIT=nom||null;
  const c=nom?(FRN[nom]||{}):{};
  $('fr-titre').textContent=nom?('Fiche de '+nom):'Nouveau fournisseur';
  $('fr-nom').value=nom||''; $('fr-nom').disabled=!!nom;
  FR_CH.forEach(k=>$('fr-'+k).value=c[k]||'');
  $('fr-msg').textContent=''; $('frov').classList.add('on');
  setTimeout(()=>$(nom?'fr-raison':'fr-nom').focus(),60);
}
function edite(nom){ formFrn(nom); }
$('nouv').onclick=()=>formFrn(null);
$('fr-x').onclick=$('fr-non').onclick=()=>$('frov').classList.remove('on');
$('frov').addEventListener('click',e=>{ if(e.target.id==='frov') $('frov').classList.remove('on'); });
$('fr-ok').onclick=()=>{
  const dis=t=>{ $('fr-msg').textContent=t; $('fr-msg').className='msg err'; };
  const nom=FR_EDIT||$('fr-nom').value.trim();
  if(nom.length<2) return dis('Donne un nom au fournisseur.');
  if(!FR_EDIT && Object.keys(FRN).some(k=>k.toLowerCase()===nom.toLowerCase())) return dis('Ce fournisseur existe déjà.');
  const em=$('fr-email').value.trim();
  if(em && !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(em)) return dis("L'adresse e-mail n'est pas valable.");
  const c=Object.assign({nom},FRN[nom]||{});
  FR_CH.forEach(k=>{ const v=$('fr-'+k).value.trim(); if(v) c[k]=v; else delete c[k]; });
  FRN[nom]=c; sauveFRN();
  const J=lit(KJOU,[]);
  J.push({t:new Date().toISOString(),u:USR||'(non renseigné)',act:'fournisseur',
          lib:FR_EDIT?'fiche fournisseur modifiée':'fournisseur créé à la main',ref:nom,av:null,ap:'coordonnées'});
  ecrit(KJOU,J);
  $('frov').classList.remove('on'); dessine();
  if(!FR_EDIT && confirm('Fournisseur « '+nom+' » créé. Déposer maintenant une de ses factures ?')) location.href='factures.html?sens=achat&frn='+encodeURIComponent(nom);
};

/* ---------- déposer n'importe quel document : le fournisseur naît de ce qu'on y lit ----------
   Une facture, une price list, un listing, la photo d'une carte de visite. On lit le
   texte (tableur, PDF, photo : même porte que Factures), on en tire le nom et les
   coordonnées, on crée la fiche — et si le document porte des lignes de prix, on
   l'emmène dans Factures ou dans l'Étude, sans le redéposer. */
let DP=null;
function litFrnDe(txt){
  const o={};
  const bas=txt.toLowerCase();
  let soc=''; try{ soc=String((JSON.parse(localStorage.getItem('reglages-v1')||'{}')||{}).societe||'').toLowerCase(); }catch(e){}
  const connu=Object.keys(FRN).find(n=>n.length>2&&bas.includes(n.toLowerCase()));
  if(connu) o.deja=connu;
  const li=txt.split('\n').map(x=>x.trim()).filter(Boolean);
  const pasNous=x=>!(soc&&x.toLowerCase().includes(soc))&&!/perfumes ?trade|dasy/i.test(x);
  const soc1=li.find(x=>/\b(LLC|INC\.?|CORP\.?|LTD\.?|GROUP|SAS|SARL|GMBH|S\.A\.|TRADING|DISTRIBUTION|IMPORT|EXPORT|PERFUMES?|FRAGRANCES?|COSMETICS?|BEAUTY|WHOLESALE)\b/i.test(x)&&x.length<70&&pasNous(x));
  const prem=li.find(x=>/[A-Za-z]{3}/.test(x)&&!/\d{3}/.test(x)&&x.length>=3&&x.length<50&&pasNous(x)&&!/^(invoice|facture|price ?list|date|page|tel|phone|email|www)/i.test(x));
  o.nom=connu||(soc1||prem||'').replace(/\s{2,}.*$/,'').replace(/\b(COMPANY|LOGO)\b/gi,'').trim().slice(0,60);
  const em=txt.match(/[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}/gi)||[]; o.email=em.find(e=>pasNous(e))||'';
  const tel=(txt.match(/(?:\+?\d[\d\s().-]{8,16}\d)/g)||[]).find(t=>{ const d=t.replace(/\D/g,''); return d.length>=10&&d.length<=15&&!/^\d{4}[-\/]\d{2}[-\/]\d{2}/.test(t.trim()); });
  o.tel=tel?tel.trim():'';
  const site=txt.match(/\b(?:https?:\/\/)?(?:www\.)[a-z0-9.-]+\.[a-z]{2,}(?:\/\S*)?/i); o.site=site&&pasNous(site[0])?site[0]:'';
  /* un prix avec centimes (60.00) OU un prix rond précédé d'un signe $ (juste "$60",
     très courant dans une petite liste tapée vite) : sans le $, un nombre rond seul
     ressemble trop à une quantité ou un code-barres pour compter comme un prix.
     Igal, 12 sept. 2026, sur une price list d'un fournisseur déjà connu : « rubrique
     price list à effectuer, elle était déjà créée » — la fiche se créait, mais la
     price list, elle, n'était pas reconnue comme telle (trop peu de lignes chiffrées). */
  o.nPrix=li.filter(x=>/\d+[.,]\d{2}\b/.test(x)||/\$\s?\d+(?:[.,]\d{1,2})?\b/.test(x)).length;
  if(/\b(invoice|facture|factura|total due|amount due|bill to|balance due)\b/i.test(txt)) o.type='facture';
  else if(/\b(price ?list|wholesale|tarif|catalog(ue)?|listing|offer|oferta|lista de precios)\b/i.test(txt)||o.nPrix>=2) o.type='pricelist';
  else o.type='autre';
  const m=txt.match(/(?:Invoice|Facture|N[°º]|No\.?)\s*[:#]?\s*([A-Z]{0,6}[-\/]?\d{3,}[A-Z0-9-]*)/i); if(m) o.num=m[1];
  return o;
}
async function depotDoc(file){
  if(!file) return;
  DP={file,texte:'',lu:null};
  $('dp-titre').textContent='Lecture de '+file.name+'…';
  $('dp-quoi').textContent='Un instant : on lit le document.';
  ['nom','email','tel','site'].forEach(k=>$('dp-'+k).value='');
  $('dp-deja').hidden=true; $('dp-msg').textContent=''; $('dp-suite').hidden=true; $('dp-fiche').disabled=true;
  $('dpov').classList.add('on');
  try{
    DP.texte=await lireFichier(file, m=>{ $('dp-quoi').textContent=m; });
  }catch(e){ $('dp-quoi').textContent=(e&&e.message)||'Lecture impossible.'; $('dp-fiche').disabled=false; return; }
  const o=DP.lu=litFrnDe(DP.texte);
  $('dp-titre').textContent='Document lu : '+file.name;
  $('dp-nom').value=o.nom||''; $('dp-email').value=o.email||''; $('dp-tel').value=o.tel||''; $('dp-site').value=o.site||'';
  const quoi=o.type==='facture'?`Ça ressemble à une <b>facture</b>${o.num?' n° '+esc(o.num):''}${o.nPrix?' · '+nf(o.nPrix)+' ligne'+(o.nPrix>1?'s':'')+' avec un prix':''}.`
    :o.type==='pricelist'?`Ça ressemble à une <b>price list</b> · ${nf(o.nPrix)} ligne${o.nPrix>1?'s':''} avec un prix.`
    :`Pas de lignes de prix : on garde <b>le nom et les coordonnées</b>.`;
  $('dp-quoi').innerHTML=quoi+' Vérifie le nom, corrige si besoin.';
  $('dp-fiche').disabled=false;
  if(o.deja){ $('dp-deja').hidden=false; $('dp-deja').innerHTML=`Ce fournisseur existe déjà : <b data-nolang>${esc(o.deja)}</b>. Les coordonnées ci-dessus complètent sa fiche (rien n'est écrasé).`; $('dp-fiche').textContent='Compléter la fiche'; }
  else $('dp-fiche').textContent='Créer la fiche';
  if(o.type==='facture'){ $('dp-suite').hidden=false; $('dp-suite').textContent=(o.deja?'':'Créer la fiche et ')+'enregistrer la facture →'; }
  else if(o.type==='pricelist'){ $('dp-suite').hidden=false; $('dp-suite').textContent=(o.deja?'':'Créer la fiche et ')+'lire la price list →'; }
  else $('dp-suite').hidden=true;
  setTimeout(()=>$('dp-nom').focus(),60);
}
/* crée ou complète la fiche depuis la fenêtre ; rend le nom retenu, ou null */
function depotFiche(){
  const dis=t=>{ $('dp-msg').textContent=t; $('dp-msg').className='msg err'; };
  let nom=$('dp-nom').value.trim();
  if(nom.length<2){ dis('Donne un nom au fournisseur.'); return null; }
  const exist=Object.keys(FRN).find(k=>k.toLowerCase()===nom.toLowerCase()); if(exist) nom=exist;
  const em=$('dp-email').value.trim();
  if(em && !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(em)){ dis("L'adresse e-mail n'est pas valable."); return null; }
  const c=Object.assign({nom},FRN[nom]||{});
  [['email',em],['tel',$('dp-tel').value.trim()],['site',$('dp-site').value.trim()]].forEach(([k,v])=>{ if(v&&!c[k]) c[k]=v; });
  const neuf=!FRN[nom];
  if(neuf) c.note=[c.note,'Créé depuis le document « '+(DP.file.name||'')+' »'].filter(Boolean).join(' · ');
  FRN[nom]=c; sauveFRN();
  const J=lit(KJOU,[]);
  J.push({t:new Date().toISOString(),u:USR||'(non renseigné)',act:'fournisseur',
          lib:neuf?'fournisseur créé depuis un document':'fiche fournisseur complétée depuis un document',ref:nom,av:null,ap:DP.file.name||''});
  ecrit(KJOU,J);
  return nom;
}
$('dp-fiche').onclick=()=>{ const nom=depotFiche(); if(!nom) return; $('dpov').classList.remove('on'); dessine(); ouvreFiche(nom); };
$('dp-suite').onclick=async()=>{ const nom=depotFiche(); if(!nom) return;
  $('dp-msg').className='msg'; $('dp-msg').textContent='Le document part avec toi…';
  try{ await docAttentePose(DP.file); }catch(e){ $('dp-msg').className='msg err'; $('dp-msg').textContent="Le document n'a pas pu être emporté : redépose-le sur la page suivante."; }
  location.href=(DP.lu&&DP.lu.type==='facture')?('factures.html?sens=achat&doc=attente&frn='+encodeURIComponent(nom)):('etude.html?doc=attente&frn='+encodeURIComponent(nom)); };
$('dp-x').onclick=$('dp-non').onclick=()=>$('dpov').classList.remove('on');
$('depot').onclick=()=>$('dfich').click();
$('dfich').addEventListener('change',e=>{ const f=e.target.files[0]; if(f) depotDoc(f); e.target.value=''; });
/* glisser un fichier n'importe où sur la page */
{ let n=0;
  document.addEventListener('dragenter',e=>{ if(!e.dataTransfer||![...e.dataTransfer.types].includes('Files')) return; n++; $('dpz').classList.add('on'); });
  document.addEventListener('dragleave',()=>{ n=Math.max(0,n-1); if(!n) $('dpz').classList.remove('on'); });
  document.addEventListener('dragover',e=>{ if(e.dataTransfer&&[...e.dataTransfer.types].includes('Files')) e.preventDefault(); });
  document.addEventListener('drop',e=>{ n=0; $('dpz').classList.remove('on'); if(!e.dataTransfer||!e.dataTransfer.files.length) return; e.preventDefault(); depotDoc(e.dataTransfer.files[0]); }); }
window.__FRN=Object.assign(window.__FRN||{},{litFrnDe,depotDoc,depotFiche});

$('tri').addEventListener('change',dessine);
poseSortie('exp', ()=>{
  const L=[];
  Object.entries(HIST).forEach(([cle,l])=>l.forEach(a=>{
    if(!a.f||a.src==='fichier') return;
    const i=IDX[cle]||[];
    L.push([a.f,a.d,a.num||'',i[0]||'',((i[2]||'')+' '+(i[1]||'')).trim(),a.q==null?null:+a.q,a.p==null?null:+a.p,
            (a.q!=null&&a.p!=null)?(+a.q)*(+a.p):null]);
  }));
  L.sort((x,y)=>String(y[1]||'').localeCompare(String(x[1]||'')));
  return {
    titre:'Achats fournisseurs',
    fichier:'achats-fournisseurs',
    filtre:'tous les achats enregistrés par une facture',
    colonnes:[{t:'Fournisseur'},{t:'Date',y:'d'},{t:'N° facture'},{t:'Code-barres'},{t:'Référence'},
      {t:'Quantité',y:'n'},{t:'Prix unitaire',y:'m'},{t:'Montant',y:'m'}],
    lignes:L
  };
});

function majUser(){ try{ piedSession(); }catch(e){} }
majUser();
$('sfoot').innerHTML='fiches alimentées<br>par les factures';
dessine();
'''

html = coquille("Mes fournisseurs", "Fournisseurs",
  "Chaque fournisseur est construit à partir des factures enregistrées : ce qu'il vend, "
  "à quel prix, comment ses prix bougent, et sur quelles références il est battu par un autre.",
  CSS, CORPS.replace('__ACCEPT__', _lire.ACCEPT), JS, donnees=('produits',))
html = html.replace('__IDX__', 'Object.fromEntries(D_TOUS().map(r=>[r[15],[r[0],r[13],r[2],r[12],r[6],r[8]]]))')
html = html.replace('__FRNINIT__', open('frn_seed.json').read().strip())
open('fournisseurs.html','w').write(html)
print('fournisseurs.html',len(html)//1024,'Ko')
