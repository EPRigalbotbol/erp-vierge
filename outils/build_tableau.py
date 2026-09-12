# -*- coding: utf-8 -*-
import json
from build_crm import coquille
import _donnees
C=json.load(open('cat.json'))
IDX={r[15]:[r[0],r[13],r[2],r[12],r[6],r[8],r[7],r[14]] for r in C}  # bc,nom,marque,pa,qte,pvw,pvr,verif

CSS = r'''
.mur{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:34px 32px;
 max-width:640px;margin:26px auto}
.mur h2{margin:0 0 10px;font-size:20px;font-weight:700;letter-spacing:-.015em}
.mur p{margin:0;color:var(--ink-2);font-size:14.5px;line-height:1.65}
.sous{margin:5px 0 0;font-size:14px;color:var(--ink-2);max-width:76ch;line-height:1.5}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(176px,1fr));gap:1px;
background:var(--line-2);border:1px solid var(--line);border-radius:10px;overflow:hidden;
margin-bottom:26px;box-shadow:0 1px 2px rgba(0,0,0,.04)}
.kpi{background:var(--surface);padding:16px 18px;display:flex;flex-direction:column;gap:3px}
.kpi .v{font-size:25px;font-weight:700;line-height:1;letter-spacing:-.03em}
.kpi .k{font-size:12px;color:var(--ink-3);line-height:1.4}
.kpi.hot .v{color:var(--crit)} .kpi.warm .v{color:var(--warn)} .kpi.iris .v{color:var(--iris)}

h2.sec{font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:var(--ink);font-weight:700;
margin:34px 0 13px;padding-bottom:9px;border-bottom:1px solid var(--line);
display:flex;justify-content:space-between;align-items:baseline;gap:12px;flex-wrap:wrap}
h2.sec em{font-style:normal;font-size:12.5px;letter-spacing:0;text-transform:none;
color:var(--ink-3);font-weight:400}
h2.sec a{font-size:12px;letter-spacing:0;text-transform:none;color:var(--iris);font-weight:600;
text-decoration:none} h2.sec a:hover{text-decoration:underline}

.alerte{background:var(--surface);border:1px solid var(--line);border-left:4px solid var(--warn);
border-radius:10px;padding:18px 20px;margin-bottom:16px}
.alerte.crit{border-left-color:var(--crit)}
.alerte.ok{border-left-color:var(--good)}
.alerte h3{margin:0 0 5px;font-size:16px;font-weight:700;letter-spacing:-.015em}
.alerte p{margin:0;font-size:13.5px;color:var(--ink-2);line-height:1.6;max-width:78ch}
.alerte p b{color:var(--ink)}

.tbl{width:100%;border-collapse:collapse;font-size:13.5px;background:var(--surface);
border:1px solid var(--line);border-radius:10px;overflow:hidden}
.tbl th{text-align:left;font-size:9.5px;letter-spacing:.11em;text-transform:uppercase;
color:var(--ink-2);font-weight:700;padding:12px 13px;background:var(--surface-2);
border-bottom:1px solid var(--line);white-space:nowrap}
.tbl th.r{text-align:right}
.tbl td{padding:12px 13px;border-bottom:1px solid var(--line-3);vertical-align:middle}
.tbl tbody tr:nth-child(even){background:var(--surface-2)}
.tbl tbody tr:last-child td{border-bottom:0}
.tbl td.r{text-align:right;white-space:nowrap;font-weight:700}
.tbl .ref b{display:block;font-weight:700;font-size:14px}
.tbl .ref span{color:var(--ink-3);font-size:11.5px}
.tbl .mq{font-size:11px;font-weight:700;letter-spacing:.07em;text-transform:uppercase;
color:var(--iris);line-height:1.4}
.rest{display:inline-flex;align-items:center;gap:7px;font-weight:700;font-size:16px}
.rest.c{color:var(--crit)} .rest.w{color:var(--warn)}
.rest::before{content:"";width:7px;height:7px;border-radius:50%;background:currentColor}
.chute{color:var(--crit);font-weight:700}
.wrapx{overflow-x:auto;margin-bottom:8px}
.vide{border:2px dashed var(--line);border-radius:11px;padding:30px 28px;text-align:center;
background:var(--surface-2);max-width:64ch;margin:0 auto}
.vide p{margin:0;font-size:14px;color:var(--ink-2);line-height:1.65}
.plus{display:block;width:100%;margin-top:12px;padding:12px;background:var(--surface);
border:1px solid var(--line);border-radius:9px;font-family:inherit;font-size:13.5px;
color:var(--ink-2);cursor:pointer;font-weight:600}
.plus:hover{border-color:var(--iris);color:var(--iris)}

/* ---- l'argent : ce qui est entré, ce qui reste à encaisser ---- */
/* la file d'attente : une action, donc en tête et impossible à manquer */
.att{display:flex;align-items:center;gap:14px;flex-wrap:wrap;border:1px solid var(--iris);
background:var(--iris-soft);border-radius:12px;padding:13px 17px;margin:0 0 16px}
.att b{font-size:15.5px;color:var(--ink)}
.att .d{font-size:13px;color:var(--ink-2);flex:1;min-width:220px;line-height:1.5}
.att .go{display:inline-block;background:var(--iris);color:#fff;border-radius:9px;padding:8px 15px;
font:600 13.5px Inter,sans-serif;text-decoration:none;white-space:nowrap}
.att .go:hover{filter:brightness(1.08)}
/* ce qui mérite un regard : rien du tout les jours où il n'y a rien */
.reg{display:grid;gap:8px;margin:0 0 16px}
.reg a{display:flex;gap:11px;align-items:baseline;text-decoration:none;border:1px solid var(--line);
border-left-width:3px;border-radius:0 9px 9px 0;background:var(--surface);padding:10px 14px}
.reg a:hover{background:var(--surface-2)}
.reg a.crit{border-left-color:var(--crit)} .reg a.warn{border-left-color:var(--warn)}
.reg .l{font-size:13.5px;font-weight:600;color:var(--ink)}
.reg .s{font-size:12.5px;color:var(--ink-3)}
.arg{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:14px;margin-bottom:8px}
.ca{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:18px 20px}
.ca .t{font-size:10px;letter-spacing:.13em;text-transform:uppercase;color:var(--ink-3);font-weight:700}
.ca .v{font-size:30px;font-weight:800;letter-spacing:-.035em;line-height:1.1;margin:7px 0 2px;
font-variant-numeric:tabular-nums}
.ca .d{font-size:12.5px;color:var(--ink-2);line-height:1.5}
.ca .d b{color:var(--ink)}
.ca .ev{font-size:12.5px;font-weight:700;margin-top:6px;display:inline-flex;align-items:center;gap:5px}
.ca .ev.up{color:var(--good)} .ca .ev.dn{color:var(--crit)} .ca .ev.eq{color:var(--ink-3)}
.ca.due .v{color:var(--crit)}
/* les heures où ça vend : 24 colonnes, les meilleures en couleur */
.heures{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:18px 20px 12px}
.heures .hg{display:grid;grid-template-columns:repeat(24,1fr);gap:3px;align-items:end;height:120px}
.heures .hc{position:relative;height:100%;display:flex;align-items:flex-end}
.heures .hc i{display:block;width:100%;background:var(--line);border-radius:3px 3px 0 0;min-height:2px}
.heures .hc.top i{background:var(--iris)}
.heures .hc.ferme i{background:var(--line-2)}
.heures .hc b{position:absolute;left:0;right:0;bottom:100%;text-align:center;font-size:10px;color:var(--ink-2);font-weight:600;padding-bottom:2px;opacity:0}
.heures .hc.top b,.heures .hc:hover b{opacity:1}
.heures .hx{display:grid;grid-template-columns:repeat(24,1fr);gap:3px;margin-top:6px;font-size:10px;color:var(--ink-3);text-align:center;font-variant-numeric:tabular-nums}
.heures .hx span:nth-child(odd){visibility:hidden}
@media(max-width:700px){ .heures .hx span:not(:nth-child(6n+1)){visibility:hidden} }
.heures .hl{display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;margin-top:12px;font-size:13px;color:var(--ink-2)}
.heures .hl b{color:var(--ink)}
.bar{display:flex;height:9px;border-radius:5px;overflow:hidden;margin:12px 0 9px;background:var(--line-2)}
.bar i{display:block;height:100%}
.leg{display:flex;flex-wrap:wrap;gap:9px 16px;font-size:12.5px;color:var(--ink-2)}
.leg span{display:inline-flex;align-items:center;gap:6px}
.leg i{width:9px;height:9px;border-radius:3px;display:inline-block}
.leg b{color:var(--ink);font-variant-numeric:tabular-nums}
.mini{width:100%;height:46px;display:block;margin-top:10px}
.rien{color:var(--ink-3);font-size:13.5px;line-height:1.6}
.tbl td.neg{color:var(--crit)} .tbl td.pos{color:var(--good)}
.jrs{font-size:11.5px;color:var(--ink-3);font-weight:400}
'''

CORPS = '<div id="kpis"></div><div id="corps"></div>'

JS = r'''
const IDX=__IDX__;
const KREG='reglages-v1', KJOU='crm-journal-v1', KMOD='fiches-modifiees-v1', KEXT='stock-externe-v1',
      KVENT='ventes-v1', KFACT='factures-v1';
const DEF={seuilQte:3,capMin:0,baissePct:30,baisseJours:30,margeMin:10};
let REG=Object.assign({},DEF);
try{ const r=JSON.parse(localStorage.getItem(KREG)||'null'); if(r) REG=Object.assign({},DEF,r); }catch(e){}
let MOD={},EXT={q:{}},JOU=[];
try{ MOD=JSON.parse(localStorage.getItem(KMOD)||'{}'); }catch(e){}
try{ const r=JSON.parse(localStorage.getItem(KEXT)||'null'); if(r&&r.q) EXT=r; }catch(e){}
try{ JOU=JSON.parse(localStorage.getItem(KJOU)||'[]'); }catch(e){}
let VENT={},FACT=[];
try{ VENT=JSON.parse(localStorage.getItem(KVENT)||'{}')||{}; }catch(e){}
try{ FACT=JSON.parse(localStorage.getItem(KFACT)||'[]')||[]; }catch(e){}
if(!Array.isArray(FACT)) FACT=[];

const ART=Object.entries(IDX).map(([cle,v])=>{
  const [bc,nom,marque,pa0,qte0,pvw0,pvr0,verif0]=v;
  const m=MOD[cle]||{};
  let q=qte0;
  if(EXT.q[bc]!==undefined&&EXT.q[bc]!==null) q=EXT.q[bc];
  if(m.qte!=null) q=m.qte;
  return {cle,bc,nom,marque,qte:q,
          pa:m.pa!=null?m.pa:pa0, pvw:m.pvw!=null?m.pvw:pvw0, pvr:m.pvr!=null?m.pvr:pvr0,
          verif:m.verif!=null?m.verif:verif0};
});
const enStock=ART.filter(p=>p.qte>0);
const cap=p=>p.qte*(p.pa||0);
const capTot=enStock.reduce((a,p)=>a+cap(p),0);

const bas = REG.seuilQte>0
  ? enStock.filter(p=>p.qte<REG.seuilQte && cap(p)>=REG.capMin).sort((a,b)=>cap(b)-cap(a))
  : [];
function baisses(){
  const lim=Date.now()-REG.baisseJours*86400000, mv={};
  JOU.forEach(e=>{
    if(new Date(e.t).getTime()<lim) return;
    if((e.act==='import'||e.act==='reception'||e.act==='vente'||e.act==='annulation')&&e.det) e.det.forEach(d=>{ (mv[d.bc]=mv[d.bc]||[]).push([d.av,d.ap]); });
    else if(e.act==='stock'&&e.bc&&e.av!=null&&e.ap!=null) (mv[e.bc]=mv[e.bc]||[]).push([+e.av,+e.ap]);
  });
  const out=[];
  Object.entries(mv).forEach(([bc,l])=>{
    const av=l[0][0], ap=l[l.length-1][1];
    if(!(av>0)||ap>=av) return;
    const pct=(av-ap)/av*100;
    if(pct<REG.baissePct) return;
    const p=ART.find(x=>x.bc===bc); if(!p) return;
    out.push({p,av,ap,pct});
  });
  return out.sort((a,b)=>b.pct-a.pct);
}
const chutes=baisses();
const perte=enStock.filter(p=>p.pvw!=null&&p.pa!=null&&p.pvw<=p.pa);
const faible=enStock.filter(p=>p.pvw!=null&&p.pa!=null&&p.pvw>p.pa&&((p.pvw-p.pa)/p.pvw*100)<REG.margeMin);
const jamais=enStock.filter(p=>p.verif!=='ok');

/* ============ CE QUI EST VENDU ============
   Une ligne de vente par référence et par jour, avec son canal, son prix et la marge.
   Le prix d'achat retenu est celui d'aujourd'hui : c'est une approximation assumée
   (l'historique exact ligne par ligne vit dans les factures), mais elle suffit pour
   dire « on gagne ou on ne gagne pas » le matin. */
const parCle={}; ART.forEach(p=>parCle[p.cle]=p);
const VL=[];
Object.entries(VENT).forEach(([cle,l])=>{ const p=parCle[cle]; if(!p||!Array.isArray(l)) return;
  l.forEach(x=>{ if(!x||!x.d||!(x.q)) return;
    const mt=(x.q||0)*(x.p||0);
    VL.push({cle,p,d:String(x.d).slice(0,10),h:x.h||'',q:x.q,pu:x.p,mt,canal:x.k||'(non précisé)',
             mg:(p.pa!=null&&x.p!=null)?mt-p.pa*x.q:null}); }); });
VL.sort((a,b)=>b.d.localeCompare(a.d));

const AUJ=new Date(); const iso=d=>isoJour(d);
const jourMoins=n=>{ const d=new Date(AUJ); d.setDate(d.getDate()-n); return iso(d); };
const HIER=jourMoins(1), J7=jourMoins(7), J14=jourMoins(14), J30=jourMoins(30), J60=jourMoins(60), J90=jourMoins(90);
const somme=(L)=>({n:L.length,q:L.reduce((a,x)=>a+(x.q||0),0),ca:L.reduce((a,x)=>a+x.mt,0),
                   mg:L.reduce((a,x)=>a+(x.mg||0),0),sansPa:L.some(x=>x.mg==null)});
const entre=(a,b)=>VL.filter(x=>x.d>=a&&(b?x.d<b:true));
const vHier=somme(VL.filter(x=>x.d===HIER)), vAuj=somme(VL.filter(x=>x.d===iso(AUJ)));
const v7=somme(entre(J7)), v7av=somme(entre(J14,J7));
const v30=somme(entre(J30)), v30av=somme(entre(jourMoins(60),J30));
const v90=somme(entre(J90));
/* les ventes des 30 derniers jours, canal par canal */
const parCanal={}; entre(J30).forEach(x=>{ const c=parCanal[x.canal]=parCanal[x.canal]||{ca:0,q:0,mg:0};
  c.ca+=x.mt; c.q+=x.q||0; c.mg+=x.mg||0; });
const canaux=Object.entries(parCanal).sort((a,b)=>b[1].ca-a[1].ca);
const COUL=['#6b5cff','#2c6e4e','#c98a1a','#a4262c','#3f7fb5','#7a5299','#5c6b7a'];

/* ---- l'argent à encaisser : les factures avec un reste dû ---- */
const DOCS=FACT.filter(f=>f&&f.doc&&f.doc.type==='facture'&&(f.doc.reste||0)>0)
  .sort((a,b)=>String(a.d||'').localeCompare(String(b.d||'')));
const duTot=DOCS.reduce((a,f)=>a+(f.doc.reste||0),0);
const duVieux=DOCS.filter(f=>f.d&&f.d<jourMoins(30));
const devisOuverts=FACT.filter(f=>f&&f.doc&&f.doc.type==='devis'&&!f.doc.converti);

/* ---- ce qui va manquer : le rythme réel, pas un seuil fixe ---- */
const vendu90={}; entre(J90).forEach(x=>{ vendu90[x.cle]=(vendu90[x.cle]||0)+(x.q||0); });
const rupture=enStock.map(p=>{ const v=vendu90[p.cle]||0; if(!v) return null;
    const parJour=v/90, jours=p.qte/parJour;
    return jours<=21?{p,v,jours,parJour}:null; }).filter(Boolean).sort((a,b)=>a.jours-b.jours);
/* ---- ce qui dort : en stock, jamais vendu depuis 90 jours, et ça pèse ---- */
const dort=enStock.filter(p=>!(vendu90[p.cle]>0)&&cap(p)>0).sort((a,b)=>cap(b)-cap(a));
const dortTot=dort.reduce((a,p)=>a+cap(p),0);
/* ---- les meilleures ventes du mois ---- */
const parProd={}; entre(J30).forEach(x=>{ const o=parProd[x.cle]=parProd[x.cle]||{p:x.p,q:0,ca:0,mg:0};
  o.q+=x.q||0; o.ca+=x.mt; o.mg+=(x.mg||0); });
const tops=Object.values(parProd).sort((a,b)=>b.ca-a.ca);

/* ---- Aujourd'hui, comparé à ce que vaut d'habitude ce jour de la semaine ----
   Un montant seul ne dit rien : 1 240 $ un mardi, est-ce bien ou mal ? On compare
   donc au même jour de la semaine sur les quatre dernières semaines. En dessous de
   deux jours de référence, on ne compare pas — on ne bâtit pas une moyenne sur rien. */
const JOUR_SEM=AUJ.getDay();
const memesJours=(()=>{ const M={};
  VL.filter(x=>x.d<iso(AUJ)&&x.d>=jourMoins(28)).forEach(x=>{
    const d=new Date(x.d+'T12:00:00'); if(d.getDay()!==JOUR_SEM) return;
    (M[x.d]=M[x.d]||{ca:0,q:0}); M[x.d].ca+=x.mt; M[x.d].q+=x.q||0; });
  return Object.values(M); })();
const habitude = memesJours.length>=2
  ? memesJours.reduce((a,x)=>a+x.ca,0)/memesJours.length : null;
const NOMJ=['dimanche','lundi','mardi','mercredi','jeudi','vendredi','samedi'][JOUR_SEM];

/* ---- Les ventes déposées par le site et la caisse, pas encore enregistrées ---- */
let FILE_ATT=[]; try{ const f=JSON.parse(localStorage.getItem('caisse-file-v1')||'[]'); if(Array.isArray(f)) FILE_ATT=f; }catch(e){}

/* ---- Ce qui mérite un regard : trois lignes au plus, rien s'il n'y a rien ----
   Un bandeau vide la plupart du temps est un bandeau qu'on lit quand il ne l'est pas. */
const regards=[];
(function(){
  /* vendu en dessous du prix d'achat, sur 7 jours */
  const perte=entre(J7).filter(x=>x.p.pa!=null&&x.pu!=null&&x.q>0&&x.pu<x.p.pa);
  if(perte.length){
    const m=perte.reduce((a,x)=>a+(x.p.pa-x.pu)*x.q,0);
    regards.push({t:'crit',lib:`${nf(perte.length)} vente${perte.length>1?'s':''} en dessous du prix d'achat cette semaine`,
      d:`${money2(m)} perdus · ${perte.slice(0,2).map(x=>esc((x.p.marque||'')+' '+(x.p.nom||''))).join(', ')}`,
      lien:'ventes.html'});
  }
  /* remboursements sur 7 jours */
  const ret=FACT.filter(f=>f&&f.retour&&f.d&&f.d>=J7);
  if(ret.length) regards.push({t:'warn',lib:`${nf(ret.length)} remboursement${ret.length>1?'s':''} cette semaine`,
    d:money2(Math.abs(ret.reduce((a,f)=>a+(f.montant||0),0)))+' rendus',lien:'ventes.html'});
  /* ce qui vient de passer sous le seuil, et se vend */
  const urgent=rupture.filter(r=>r.jours<=7);
  if(urgent.length) regards.push({t:'crit',lib:`${nf(urgent.length)} référence${urgent.length>1?'s':''} manquera${urgent.length>1?'ont':''} sous une semaine`,
    d:urgent.slice(0,2).map(r=>esc((r.p.marque||'')+' '+(r.p.nom||''))+' ('+Math.round(r.jours)+' j)').join(', '),
    lien:'catalogue.html'});
})();

const pctEv=(a,b)=>(b>0)?((a-b)/b*100):(a>0?100:0);
function evo(a,b,quoi){
  if(b<=0&&a<=0) return '';
  const p=pctEv(a,b), k=Math.abs(p)<3?'eq':(p>0?'up':'dn');
  return `<span class="ev ${k}">${k==='eq'?'≈':(p>0?'▲':'▼')} ${Math.abs(Math.round(p))} % ${quoi}</span>`;
}
/* une petite courbe des 30 derniers jours */
function courbe(){
  const J=[]; for(let i=29;i>=0;i--){ const d=jourMoins(i); J.push(VL.filter(x=>x.d===d).reduce((a,x)=>a+x.mt,0)); }
  const mx=Math.max(...J,1), w=100, h=46;
  const pts=J.map((v,i)=>`${(i/(J.length-1)*w).toFixed(2)},${(h-2-v/mx*(h-6)).toFixed(2)}`).join(' ');
  return `<svg class="mini" viewBox="0 0 ${w} ${h}" preserveAspectRatio="none" aria-hidden="true">
    <polyline points="${pts}" fill="none" stroke="var(--iris)" stroke-width="1.4" vector-effect="non-scaling-stroke"/>
    <polyline points="0,${h} ${pts} ${w},${h}" fill="var(--iris-soft)" stroke="none"/></svg>`;
}

let vus=25;
function tblBas(){
  const l=bas.slice(0,vus);
  return `<div class="wrapx"><table class="tbl"><thead><tr>
    <th>Référence</th><th class="r">Reste</th><th class="r">Prix d'achat</th>
    <th class="r">Marchandise</th><th class="r">Prix de gros</th></tr></thead><tbody>
    ${l.map(p=>`<tr>
      <td class="ref"><div class="mq">${esc(p.marque||'')}</div>
        <b>${esc(p.nom||'')}</b><span>${esc(p.bc||'')}</span></td>
      <td class="r"><span class="rest ${p.qte<=1?'c':'w'}">${p.qte}</span></td>
      <td class="r">${money2(p.pa)}</td>
      <td class="r">${money(cap(p))}</td>
      <td class="r">${money2(p.pvw)}</td></tr>`).join('')}
    </tbody></table></div>
    ${bas.length>vus?`<button class="plus" id="plus">Afficher plus (${nf(bas.length-vus)} restantes)</button>`:''}`;
}

function dessine(){
  /* --- ce qui est entré, ce qui reste à rentrer --- */
  const argent = VL.length ? `<div class="arg">
      <div class="ca"><div class="t">Aujourd'hui</div>
        <div class="v">${money2(vAuj.ca)}</div>
        <div class="d">${
          habitude==null
            ? (vAuj.n?`<b>${nf(vAuj.q)}</b> flacon${vAuj.q>1?'s':''} · pas encore assez d'historique pour comparer`
                     :'rien encore aujourd\'hui')
            : (()=>{ const p=Math.round(pctEv(vAuj.ca,habitude));
                const k=Math.abs(p)<10?'eq':(p>0?'up':'dn');
                return `un ${NOMJ} moyen : <b>${money2(habitude)}</b>
                  <span class="ev ${k}">${k==='eq'?'≈':(p>0?'▲':'▼')} ${Math.abs(p)} %</span>
                  <span style="display:block;font-size:11.5px;color:var(--ink-3)">moyenne des ${memesJours.length} derniers ${NOMJ}s</span>`; })()
        }</div>
        <div class="d" style="margin-top:5px">Hier : <b>${money2(vHier.ca)}</b>${vHier.n?` · marge ${vHier.sansPa?'—':money2(vHier.mg)}`:''}</div></div>
      <div class="ca"><div class="t">7 derniers jours</div>
        <div class="v">${money2(v7.ca)}</div>
        <div class="d">marge <b>${v7.sansPa?'—':money2(v7.mg)}</b>${v7.ca>0&&!v7.sansPa?` · ${Math.round(v7.mg/v7.ca*100)} %`:''}</div>
        ${evo(v7.ca,v7av.ca,'vs 7 jours d\'avant')}</div>
      <div class="ca"><div class="t">30 derniers jours</div>
        <div class="v">${money(v30.ca)}</div>
        <div class="d">marge <b>${v30.sansPa?'—':money(v30.mg)}</b>${v30.ca>0&&!v30.sansPa?` · ${Math.round(v30.mg/v30.ca*100)} %`:''}</div>
        ${evo(v30.ca,v30av.ca,'vs 30 jours d\'avant')}
        ${courbe()}</div>
      <div class="ca ${duTot?'due':''}"><div class="t">À encaisser</div>
        <div class="v">${money2(duTot)}</div>
        <div class="d">${DOCS.length?`<b>${nf(DOCS.length)}</b> facture${DOCS.length>1?'s':''} non réglée${DOCS.length>1?'s':''}${duVieux.length?` · <b>${nf(duVieux.length)}</b> de plus de 30 jours`:''}`:'tout est réglé'}</div>
        ${devisOuverts.length?`<div class="d" style="margin-top:5px"><b>${nf(devisOuverts.length)}</b> devis en attente de réponse</div>`:''}</div>
    </div>` : '';

  const rienEncore = !VL.length ? `<div class="alerte" style="border-left-color:var(--iris);margin-bottom:18px">
      <h3>Aucune vente n'est encore entrée dans l'outil</h3>
      <p>Ce tableau de bord est fait pour l'argent : ce qui est rentré hier, ce qui reste à encaisser,
      ce qui va manquer. Tant qu'aucune vente n'est enregistrée, il ne peut montrer que le stock.
      Les ventes arrivent par <a href="ventes.html">Ventes → Enregistrer une vente</a>,
      par une facture dans <a href="factures.html">Factures</a>, ou par l'export d'un canal.</p></div>` : '';
  /* Les ventes déposées par le site et la caisse : une action à faire, donc en premier. */
  const attente = FILE_ATT.length ? `<div class="att">
      <b>${nf(FILE_ATT.length)} vente${FILE_ATT.length>1?'s':''} en attente</b>
      <span class="d">Le site et la caisse les ont déposées. Elles n'ont pas encore touché au stock :
      il faut les regarder et les enregistrer.</span>
      <a class="go" href="ventes.html">Les voir</a></div>` : '';

  const regard = regards.length ? `<div class="reg">${regards.slice(0,3).map(r=>
      `<a class="${r.t}" href="${r.lien}"><span class="l">${r.lib}</span><span class="s">${r.d}</span></a>`).join('')}</div>` : '';

  $('kpis').innerHTML=attente+rienEncore+regard+argent+`<div class="kpis">
    ${VL.length
      ? `<div class="kpi ${rupture.length?'hot':''}"><span class="v">${nf(rupture.length)}</span>
          <span class="k">vont manquer sous 3 semaines, au rythme où ça part</span></div>`
      : `<div class="kpi ${bas.length?'warm':''}"><span class="v">${nf(bas.length)}</span>
          <span class="k">sous ${REG.seuilQte} flacons — en attendant l'historique des ventes</span></div>`}
    ${VL.length
      ? `<div class="kpi ${dort.length?'warm':''}"><span class="v">${money(dortTot)}</span>
          <span class="k">dort — en stock, rien vendu depuis 90 jours</span></div>`
      : `<div class="kpi"><span class="v" style="color:var(--ink-3)">—</span>
          <span class="k">argent qui dort : inconnu tant qu'aucune vente n'est enregistrée</span></div>`}
    <div class="kpi ${perte.length?'hot':''}"><span class="v">${nf(perte.length)}</span>
      <span class="k">vendues en gros à perte</span></div>
    <div class="kpi ${faible.length?'warm':''}"><span class="v">${nf(faible.length)}</span>
      <span class="k">sous ${REG.margeMin} % de marge de gros</span></div>
    <div class="kpi iris"><span class="v">${money(capTot)}</span>
      <span class="k">de marchandise en stock</span></div>
    <div class="kpi"><span class="v">${nf(jamais.length)}</span>
      <span class="k">jamais comptées, ou à recompter</span></div>
  </div>`;

  let h='';

  /* --- par canal --- */
  h+=`<h2 class="sec">D'où vient l'argent <em>30 derniers jours</em>
      <a href="ventes.html">Journal des ventes</a></h2>`;
  if(!canaux.length)
    h+=`<div class="vide"><p>Aucune vente enregistrée sur les 30 derniers jours.
        Dès qu'une vente est saisie, importée d'un canal ou facturée, elle apparaît ici,
        avec ce qu'elle rapporte réellement.</p></div>`;
  else {
    const tot=canaux.reduce((a,[,c])=>a+c.ca,0)||1;
    h+=`<div class="alerte ok" style="border-left-color:var(--iris)">
      <div class="bar">${canaux.map(([n,c],i)=>`<i style="width:${(c.ca/tot*100).toFixed(2)}%;background:${COUL[i%COUL.length]}" title="${esc(n)}"></i>`).join('')}</div>
      <div class="leg">${canaux.map(([n,c],i)=>`<span><i style="background:${COUL[i%COUL.length]}"></i>${esc(n)} <b>${money(c.ca)}</b> <span class="jrs">${Math.round(c.ca/tot*100)} %${c.mg?` · marge ${money(c.mg)}`:''}</span></span>`).join('')}</div></div>`;
  }

  /* --- ce qui va manquer --- */
  h+=`<h2 class="sec">Ce qui va manquer <em>au rythme des 90 derniers jours</em>
      <a href="etude.html">Étudier un devis</a></h2>`;
  if(!VL.length)
    h+=`<div class="vide"><p>Il faut des ventes enregistrées pour prévoir une rupture.
        Cette liste se remplira toute seule dès que les ventes entreront dans l'outil.</p></div>`;
  else if(!rupture.length)
    h+=`<div class="alerte ok"><h3>Rien d'urgent à racheter</h3>
        <p>Aucune référence qui se vend ne tombe à zéro dans les trois prochaines semaines.</p></div>`;
  else {
    h+=`<div class="alerte crit"><h3>${nf(rupture.length)} référence${rupture.length>1?'s':''} à racheter</h3>
      <p>Au rythme des trois derniers mois, elles seront à zéro dans moins de trois semaines.
      ${rupture.filter(x=>x.jours<=7).length?`<b>${nf(rupture.filter(x=>x.jours<=7).length)}</b> tiennent moins d'une semaine.`:''}</p></div>
      <div class="wrapx"><table class="tbl"><thead><tr>
      <th>Référence</th><th class="r">Reste</th><th class="r">Tient</th><th class="r">Vendus / 90 j</th>
      <th class="r">Prix d'achat</th><th class="r">Marge gros</th></tr></thead><tbody>
      ${rupture.slice(0,20).map(x=>`<tr>
        <td class="ref"><div class="mq">${esc(x.p.marque||'')}</div><b>${esc(x.p.nom||'')}</b><span>${esc(x.p.bc||'')}</span></td>
        <td class="r"><span class="rest ${x.jours<=7?'c':'w'}">${nf(x.p.qte)}</span></td>
        <td class="r ${x.jours<=7?'neg':''}">${x.jours<1?'moins d\'un jour':x.jours<7?Math.round(x.jours)+' jours':Math.round(x.jours/7)+' semaines'}</td>
        <td class="r">${nf(x.v)}</td>
        <td class="r">${money2(x.p.pa)}</td>
        <td class="r">${(x.p.pvw!=null&&x.p.pa!=null)?Math.round((x.p.pvw-x.p.pa)/x.p.pvw*100)+' %':'—'}</td></tr>`).join('')}
      </tbody></table></div>`;
  }

  /* --- les heures où ça vend ---
     Ce que Sam a demandé : « à quelles heures je vends le plus ». Une colonne par
     heure de la journée (heure de Miami), sur les 90 derniers jours, pour les
     ventes qui portent une heure : celles saisies dans l'outil, celles du site et
     celles des fichiers de caisse qui donnent l'heure. Les autres ne comptent pas
     et on le dit — deviner une heure fausserait le tableau. */
  {
    const H=VL.filter(x=>x.d>=J90 && /^\d{2}:\d{2}$/.test(x.h) && x.q>0);
    const parH=Array.from({length:24},()=>({n:0,ca:0,q:0}));
    H.forEach(x=>{ const k=+x.h.slice(0,2); if(k>=0&&k<24){ parH[k].n++; parH[k].ca+=x.mt; parH[k].q+=x.q; } });
    const sansH=VL.filter(x=>x.d>=J90 && x.q>0).length-H.length;
    const max=Math.max(1,...parH.map(o=>o.ca));
    const tops3=parH.map((o,k)=>({k,ca:o.ca,n:o.n})).filter(o=>o.n>0).sort((a,b)=>b.ca-a.ca).slice(0,3).map(o=>o.k);
    /* les heures qui se suivent se disent d'un trait : « entre 14 h et 17 h » */
    const plage=(()=>{ if(!tops3.length) return ''; const t=[...tops3].sort((a,b)=>a-b);
      if(t.length>=2 && t[t.length-1]-t[0]<=t.length) return 'entre '+t[0]+' h et '+(t[t.length-1]+1)+' h';
      return t.map(k=>'à '+k+' h').join(', '); })();
    h+=`<h2 class="sec">Les heures où ça vend <em>90 derniers jours · heure de Miami</em></h2>`;
    if(H.length<10)
      h+=`<div class="vide"><p>Pas encore assez de ventes avec une heure (${nf(H.length)} sur 90 jours).
          Les ventes saisies dans l'outil, celles du site et celles d'un fichier de caisse qui donne l'heure
          remplissent ce tableau au fil des semaines.</p></div>`;
    else
      h+=`<div class="heures">
        <div class="hg">${parH.map((o,k)=>`<div class="hc ${tops3.includes(k)?'top':''} ${o.n?'':'ferme'}" title="${k} h — ${nf(o.n)} vente${o.n>1?'s':''} · ${money(o.ca)}">
          <b>${o.n?money(o.ca):''}</b><i style="height:${Math.max(2,Math.round(o.ca/max*100))}%"></i></div>`).join('')}</div>
        <div class="hx">${parH.map((o,k)=>`<span>${k} h</span>`).join('')}</div>
        <div class="hl"><span><span>Ça vend le plus</span> <b>${plage}</b> — ${tops3.map(k=>`<span>${nf(parH[k].n)} vente${parH[k].n>1?'s':''} à ${k} h</span>`).join(', ')}.</span>
          <span><span>${nf(H.length)} vente${H.length>1?'s':''} avec une heure</span>${sansH?` · <span>${nf(sansH)} sans heure, pas comptée${sansH>1?'s':''}</span>`:''}</span></div>
      </div>`;
  }

  /* --- ce qui se vend le mieux --- */
  if(tops.length){
    h+=`<h2 class="sec">Ce qui se vend <em>30 derniers jours</em></h2>
      <div class="wrapx"><table class="tbl"><thead><tr>
      <th>Référence</th><th class="r">Flacons</th><th class="r">Chiffre d'affaires</th>
      <th class="r">Marge</th><th class="r">Reste en stock</th></tr></thead><tbody>
      ${tops.slice(0,10).map(o=>`<tr>
        <td class="ref"><div class="mq">${esc(o.p.marque||'')}</div><b>${esc(o.p.nom||'')}</b><span>${esc(o.p.bc||'')}</span></td>
        <td class="r">${nf(o.q)}</td><td class="r">${money2(o.ca)}</td>
        <td class="r ${o.mg<0?'neg':o.mg>0?'pos':''}">${o.mg?money2(o.mg):'—'}</td>
        <td class="r">${nf(o.p.qte)}</td></tr>`).join('')}
      </tbody></table></div>`;
  }

  /* --- ce qui dort --- */
  h+=`<h2 class="sec">L'argent qui dort <em>en stock, rien vendu depuis 90 jours</em>
      <a href="catalogue.html">Ouvrir le catalogue</a></h2>`;
  if(!VL.length)
    h+=`<div class="vide"><p>Sans historique de ventes, impossible de dire ce qui dort.
        Reviens ici quand quelques semaines de ventes seront entrées.</p></div>`;
  else if(!dort.length)
    h+=`<div class="alerte ok"><h3>Tout tourne</h3><p>Chaque référence en stock a été vendue au moins une fois ces trois derniers mois.</p></div>`;
  else
    h+=`<div class="alerte"><h3>${money(dortTot)} immobilisés sur ${nf(dort.length)} référence${dort.length>1?'s':''}</h3>
      <p>Elles sont en stock et n'ont rien vendu depuis 90 jours. C'est de l'argent posé sur une étagère :
      une promotion, une offre au gros ou un déstockage vers Perfume City le remettent en circulation.</p></div>
      <div class="wrapx"><table class="tbl"><thead><tr>
      <th>Référence</th><th class="r">En stock</th><th class="r">Argent immobilisé</th>
      <th class="r">Prix de gros</th><th class="r">Prix retail</th></tr></thead><tbody>
      ${dort.slice(0,15).map(p=>`<tr>
        <td class="ref"><div class="mq">${esc(p.marque||'')}</div><b>${esc(p.nom||'')}</b><span>${esc(p.bc||'')}</span></td>
        <td class="r">${nf(p.qte)}</td><td class="r">${money(cap(p))}</td>
        <td class="r">${money2(p.pvw)}</td><td class="r">${money2(p.pvr)}</td></tr>`).join('')}
      </tbody></table></div>`;

  /* --- les factures à encaisser --- */
  if(DOCS.length){
    h+=`<h2 class="sec">Factures à encaisser <a href="ventes.html">Voir les documents</a></h2>
      <div class="wrapx"><table class="tbl"><thead><tr>
      <th>N°</th><th>Date</th><th>Client</th><th>Paiement</th><th class="r">Total</th><th class="r">Reste dû</th><th class="r">Âge</th></tr></thead><tbody>
      ${DOCS.slice(0,15).map(f=>{ const j=f.d?Math.round((Date.now()-new Date(f.d).getTime())/86400000):null;
        return `<tr><td><b>${esc(f.doc.num)}</b></td><td>${dfr(f.d)}</td><td>${esc(f.tiers||'—')}</td>
        <td>${esc(({zelle:'Zelle',carte:'Carte',especes:'Espèces',virement:'Virement',credit:'Crédit'})[f.doc.pmode]||'')}</td>
        <td class="r">${money2(f.doc.total)}</td><td class="r neg">${money2(f.doc.reste)}</td>
        <td class="r ${j>30?'neg':''}">${j==null?'—':j+' j'}</td></tr>`; }).join('')}
      </tbody></table></div>`;
  }
  h+=`<h2 class="sec">Sous le seuil de ${REG.seuilQte} flacons <em>${bas.length?`classées par l'argent qu'elles représentent`:''}</em>
      <a href="reglages.html">Changer le seuil</a></h2>`;
  if(!REG.seuilQte)
    h+=`<div class="vide"><p>L'alerte de niveau est désactivée. Choisis un seuil dans les
        <a href="reglages.html">réglages</a> pour voir apparaître ici les références qui s'épuisent.</p></div>`;
  else if(!bas.length)
    h+=`<div class="alerte ok"><h3>Rien sous le seuil</h3>
        <p>Aucune référence en stock ne descend sous <b>${REG.seuilQte} flacons</b>${REG.capMin?` parmi celles qui pèsent au moins ${money(REG.capMin)}`:''}.</p></div>`;
  else {
    const c=bas.reduce((a,p)=>a+cap(p),0);
    const un=bas.filter(p=>p.qte<=1).length;
    h+=`<div class="alerte"><h3>${nf(bas.length)} référence${bas.length>1?'s':''} sous ${REG.seuilQte} flacons</h3>
      <p>Elles représentent <b>${money(c)}</b> de marchandise${un?`, dont <b>${nf(un)}</b> à un seul flacon ou moins`:''}.
      ${REG.capMin?`Les références de moins de ${money(REG.capMin)} sont écartées.`:
        `Aucun filtre de valeur : les petites références remontent aussi. Le réglage « ignorer les petites références » raccourcit la liste.`}</p></div>`
      +tblBas();
  }

  h+=`<h2 class="sec">Baisses récentes <em>mesurées sur le journal des mouvements</em>
      <a href="journal.html">Voir le journal</a></h2>`;
  const nmv=JOU.filter(e=>['import','stock','reception','vente','annulation'].includes(e.act)).length;
  if(!nmv)
    h+=`<div class="vide"><p>Aucun mouvement de stock enregistré pour l'instant.
        Cette section se remplira dès la première mise à jour du stock ou le premier comptage —
        c'est de là que vient l'information de baisse.</p></div>`;
  else if(!chutes.length)
    h+=`<div class="alerte ok"><h3>Aucune baisse notable</h3>
        <p>Sur ${REG.baisseJours} jours, aucune référence n'a perdu plus de <b>${REG.baissePct} %</b> de son stock.</p></div>`;
  else
    h+=`<div class="wrapx"><table class="tbl"><thead><tr>
      <th>Référence</th><th class="r">Avant</th><th class="r">Après</th>
      <th class="r">Baisse</th><th class="r">Reste en valeur</th></tr></thead><tbody>
      ${chutes.slice(0,25).map(x=>`<tr>
        <td class="ref"><div class="mq">${esc(x.p.marque||'')}</div><b>${esc(x.p.nom||'')}</b>
          <span>${esc(x.p.bc||'')}</span></td>
        <td class="r">${nf(x.av)}</td><td class="r">${nf(x.ap)}</td>
        <td class="r chute">−${Math.round(x.pct)} %</td>
        <td class="r">${money(cap(x.p))}</td></tr>`).join('')}</tbody></table></div>`;

  h+=`<h2 class="sec">Prix à corriger <a href="catalogue.html">Ouvrir le catalogue</a></h2>`;
  if(perte.length){
    const c=perte.reduce((a,p)=>a+cap(p),0);
    h+=`<div class="alerte crit"><h3>${nf(perte.length)} référence${perte.length>1?'s':''} vendues en gros à perte</h3>
      <p>Le prix de gros est inférieur ou égal au prix d'achat, sur <b>${money(c)}</b> de marchandise.
      Chaque vente creuse le trou.</p></div>`;
  }
  if(faible.length){
    const c=faible.reduce((a,p)=>a+cap(p),0);
    h+=`<div class="alerte"><h3>${nf(faible.length)} référence${faible.length>1?'s':''} sous ${REG.margeMin} % de marge</h3>
      <p><b>${money(c)}</b> de marchandise qui rapporte à peine de quoi couvrir les frais.</p></div>`;
  }
  if(!perte.length&&!faible.length)
    h+=`<div class="alerte ok"><h3>Aucun prix sous le seuil</h3>
        <p>Aucune vente à perte, aucune marge de gros sous ${REG.margeMin} %.</p></div>`;

  $('corps').innerHTML=h;
  const b=$('plus'); if(b) b.onclick=()=>{ vus+=25; dessine(); };
  const pts=rupture.length+perte.length+DOCS.length;
  $('src').innerHTML=`${nf(pts)} point${pts>1?'s':''} à traiter<br>${nf(enStock.length)} références en stock`;
}
function majUser(){ try{ piedSession(); }catch(e){} }
majUser();
$('sfoot').innerHTML=VL.length?`${nf(VL.length)} lignes de vente<br>seuils dans Réglages`:'seuils réglables<br>dans Réglages';
const dfr=d=>{ if(!d) return '—'; const [a,m,j]=String(d).slice(0,10).split('-'); return j?`${j}/${m}/${a.slice(2)}`:d; };

/* Le mur : cette page ne dit que des prix d'achat et des marges. */
(function(){
  const s=session(); if(!s) return;
  if(!peut('voirMarge')){
    document.querySelector('.wrap').insertAdjacentHTML('beforeend',
      `<div class="mur"><h2>Ce tableau de bord n'est pas pour ce rôle</h2>
       <p>Tu es connecté comme <b>${(s.nom||'').replace(/[&<>"]/g,'')}</b>
       (${((ROLES[s.role]||{}).lib||s.role)}). Il ne parle que de prix d'achat et de marges,
       et ce rôle ne les voit pas. Le reste de SAM t'est ouvert par la barre de gauche.</p></div>`);
    $('src').innerHTML='accès refusé';
    return;
  }
  dessine();
})();
'''

html = coquille("Tableau de bord", "Tableau de bord",
  "Ce qui demande une décision aujourd'hui : les références qui s'épuisent, celles qui "
  "baissent vite, et les prix qui font perdre de l'argent. Les seuils viennent des réglages.",
  CSS, CORPS, JS, donnees=('produits',)).replace('__IDX__', 'Object.fromEntries(D_TOUS().map(r=>[r[15],[r[0],r[13],r[2],r[12],r[6],r[8],r[7],r[14]]]))')
open('tableau.html','w').write(html)
print('tableau.html',len(html)//1024,'Ko')
