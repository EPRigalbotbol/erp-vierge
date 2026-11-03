# -*- coding: utf-8 -*-
import json
from build_crm import coquille
from _recap import RECAP_CSS, RECAP_JS
import _donnees
C=json.load(open('cat.json'))
IDX={r[15]:[r[0],r[13],r[2],r[12],r[6],r[8],r[7],r[14],r[4],r[5]] for r in C}  # bc,nom,marque,pa,qte,pvw,pvr,verif,TYPE,genre

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
.tbl th.c,.tbl td.c{text-align:center}
.tbl .dpx{font-size:12px;color:var(--ink-2);font-weight:600;margin-top:2px;white-space:nowrap} .tbl .dok{color:var(--good);font-weight:700} .tbl .dko{color:var(--crit);font-weight:700} .tbl .dna{color:var(--ink-3)}
.tbl a.btn{padding:5px 10px;font-size:12.5px;white-space:nowrap}
.tbl input[type=checkbox]{width:17px;height:17px;accent-color:var(--iris);cursor:pointer;vertical-align:middle}
.cmdbar{display:flex;align-items:center;gap:12px;flex-wrap:wrap;margin:8px 0 10px;font-size:13px;color:var(--ink-2)}
.cmdbar label{display:flex;align-items:center;gap:7px;cursor:pointer}
.mvoile{position:fixed;inset:0;background:rgba(20,16,32,.45);z-index:60;display:flex;align-items:center;justify-content:center;padding:20px}
.mfen{background:var(--surface);border-radius:14px;padding:22px 24px;max-width:920px;width:100%;max-height:92vh;overflow:auto;box-shadow:0 20px 60px rgba(0,0,0,.25)}
.mfen h3{margin:0 0 6px;font-size:18px}
.mfen .sous2{font-size:13px;color:var(--ink-3);margin:0 0 12px}
.mfen table{width:100%;border-collapse:collapse;font-size:13.5px}
.mfen th{text-align:left;font-size:10px;letter-spacing:.1em;text-transform:uppercase;color:var(--ink-3);padding:6px 8px;border-bottom:1px solid var(--line)}
.mfen td{padding:7px 8px;border-bottom:1px solid var(--line-2);vertical-align:middle}
.mfen td.r,.mfen th.r{text-align:right}
.mfen input[type=number]{width:70px;padding:6px 8px;font:inherit;font-weight:700;text-align:center;border:1px solid var(--line);border-radius:7px;background:var(--surface-2)}
.mfen .mbtn{display:flex;gap:10px;flex-wrap:wrap;justify-content:flex-end;margin-top:16px}
.mfen .mrep{font-size:13px;margin-top:10px;color:var(--ink-2)} .mfen .mrep.bad{color:var(--crit)}
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
.reg a.crit{border-left-color:var(--crit)} .reg a.warn{border-left-color:var(--warn)} .reg a.info{border-left-color:var(--iris)}
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
.pcbloc{border-left:4px solid #E0457F;padding-left:14px;margin-bottom:6px}
'''

CORPS = '<div id="recap"></div><div id="kpis"></div><div id="corps"></div>'

CSS += RECAP_CSS

JS = r'''
/*__RECAP__*/
const IDX=__IDX__;
/* Le type (EDT, EDP, OIL…) et le genre, comme partout ailleurs. */
const GEN={M:'Homme',W:'Femme',U:'Unisexe',K:'Enfant'};
const tyBadge=cle=>{ const v=IDX[cle]||[]; const t=String(v[8]||'').trim(), g=GEN[String(v[9]||'').trim().toUpperCase()]||'';
  return (t?' <i class="ty" data-nolang>'+esc(t)+'</i>':'')+(g?' <i class="gn">'+esc(g)+'</i>':''); };
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
  const [bc,nom,marque,pa0,qte0,pvw0,pvr0,verif0,,,img0]=v;
  const m=MOD[cle]||{};
  let q=qte0;
  if(EXT.q[bc]!==undefined&&EXT.q[bc]!==null) q=EXT.q[bc];
  if(m.qte!=null) q=m.qte;
  return {cle,bc,nom,marque,qte:q,
          pa:m.pa!=null?m.pa:pa0, pvw:m.pvw!=null?m.pvw:pvw0, pvr:m.pvr!=null?m.pvr:pvr0,
          verif:m.verif!=null?m.verif:verif0, img:img0||''};
});
const enStock=ART.filter(p=>p.qte>0);
const cap=p=>p.qte*(p.pa||0);
const capTot=enStock.reduce((a,p)=>a+cap(p),0);
/* 25 oct. 2026 (Igal : « je veux des alertes quand un produit n'a pas de photo ») — même règle que le Catalogue :
   une photo du fichier, une photo prise dans l'ERP (photos-perso-v1), celle d'un des deux sites (site-stock-v1)
   ou celle de la boutique Perfume City (shopify-pc-prix-v1). Sans aucune des quatre, le parfum est listé. */
function photosAilleurs(){
  const I={};
  try{ const S=JSON.parse(localStorage.getItem('site-stock-v1')||'null')||{};
    Object.keys(S).forEach(k=>{ if(k.startsWith('_')) return; const e=S[k]||{}; if((e.d&&e.d.img)||(e.g&&e.g.img)) I[k.replace(/^0+/,'')]=1; }); }catch(e){}
  try{ const P=JSON.parse(localStorage.getItem('shopify-pc-prix-v1')||'null')||{};
    Object.keys(P).forEach(k=>{ if(k.startsWith('_')) return; const r=P[k]; if(Array.isArray(r)&&r[6]&&/^https?:\/\//.test(r[6])) I[k.replace(/^0+/,'')]=1; }); }catch(e){}
  return I;
}
const sansPhoto=(function(){ let PHO={}; try{ PHO=JSON.parse(localStorage.getItem('photos-perso-v1')||'{}')||{}; }catch(e){}
  const I=photosAilleurs();
  /* deux codes collés dans la même case du fichier : chacun des deux peut porter la photo (même règle que le Catalogue) */
  const aPhoto=p=>{ const b=String(p.bc||''); if(I[b.replace(/^0+/,'')]) return true;
    if(/^\d{16,28}$/.test(b)) for(let i=8;i<=b.length-8;i++){ const g=b.slice(0,i), d=b.slice(i);
      if((/^\d{11,14}$/.test(g)&&I[g.replace(/^0+/,'')])||(/^\d{11,14}$/.test(d)&&I[d.replace(/^0+/,'')])) return true; }
    return false; };
  return enStock.filter(p=>!p.img&&!PHO[p.cle]&&!aPhoto(p)).sort((a,b)=>cap(b)-cap(a)); })();

const bas = REG.seuilQte>0
  ? enStock.filter(p=>p.qte<REG.seuilQte).sort((a,b)=>cap(b)-cap(a))
  : [];
/* 25 oct. 2026 (Igal) : l'alerte « baisse rapide » est retirée, avec son réglage — personne ne la comprenait. */
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
const estPCt=n=>/perfume\s*(in\s*the\s*)?city/i.test(String(n||''));
const coulCanal=(n,i)=>estPCt(n)?'#E0457F':COUL[i%COUL.length];   /* Perfume City : toujours rose */


/* ---- Perfume City : la boutique de Kim, à part (13 oct. 2026) ----
   Sam veut voir d'un coup d'œil si elle vend bien : ses ventes, son stock, ce qui part vite. */
function blocPC(){
  const rows=(typeof pcsRows==='function'&&pcsRows())||[];
  let T={}; try{ T=lit('testeurs-pc-v1',{})||{}; }catch(e){}
  const flac=rows.reduce((a,r)=>a+(+r[5]||0),0), vit=Object.values(T).reduce((a,v)=>a+(+(v&&v.n)||0),0);
  const capPC=rows.reduce((a,r)=>a+(r[6]!=null?(+r[5]||0)*(+r[6]):0),0);
  const enSt=rows.filter(r=>(+r[5]||0)>0).length;
  const V=entre(J30).filter(x=>estPCt(x.canal));
  const ca=V.reduce((a,x)=>a+x.mt,0), q=V.reduce((a,x)=>a+(x.q||0),0), mg=V.reduce((a,x)=>a+(x.mg||0),0);
  const pcQ={}; rows.forEach(r=>{ const k=String(r[0]||'').replace(/^0+/,''); if(k) pcQ[k]=+r[5]||0; });
  const P={}; V.forEach(x=>{ const o=P[x.cle]=P[x.cle]||{p:x.p,q:0,ca:0,mg:0}; o.q+=x.q||0; o.ca+=x.mt; o.mg+=x.mg||0; });
  const tops=Object.values(P).sort((a,b)=>b.ca-a.ca).slice(0,5);
  let h=`<h2 class="sec">Perfume City <em>la boutique de Kim · 30 derniers jours</em>
      <a href="inventaire_pc.html">Son inventaire</a></h2><div class="pcbloc">`;
  h+=`<div class="kpis">
    <div class="kpi"><span class="v">${money(ca)}</span><span class="k">vendu en 30 jours${q?` · ${nf(q)} flacon${q>1?'s':''}`:''}</span></div>
    <div class="kpi"><span class="v ${mg<0?'':'iris'}">${V.length?money(mg):'—'}</span><span class="k">marge sur ces ventes</span></div>
    <div class="kpi"><span class="v">${nf(flac)}</span><span class="k">flacons en rayon · ${nf(enSt)} référence${enSt>1?'s':''}${vit?` · + ${nf(vit)} tester${vit>1?'s':''}`:''}</span></div>
    <div class="kpi"><span class="v">${money(capPC)}</span><span class="k">stock de la boutique, au prix d'achat</span></div></div>`;
  if(!rows.length) h+=`<div class="vide"><p>L'inventaire de Perfume City est encore vide : <a href="inventaire_pc.html">le remplir</a>.</p></div>`;
  if(!V.length) h+=`<div class="vide"><p>Aucune vente Perfume City sur les 30 derniers jours. Elles arrivent ici dès qu'on en enregistre
      (Ventes → canal Perfume City) ; celles du Shopify de la boutique viendront quand il sera relié.</p></div>`;
  else h+=`<div class="wrapx"><table class="tbl"><thead><tr><th>Ce qu'elle vend le mieux</th><th class="r">Flacons</th><th class="r">Vendu</th><th class="r">Marge</th><th class="r">Reste en boutique</th></tr></thead><tbody>
    ${tops.map(o=>`<tr><td class="ref"><div class="mq">${esc(o.p.marque||'')}</div><b>${esc(o.p.nom||'')}${tyBadge(o.p.cle)}</b><span>${esc(o.p.bc||'')}</span></td>
      <td class="r">${nf(o.q)}</td><td class="r">${money2(o.ca)}</td><td class="r ${o.mg<0?'neg':o.mg>0?'pos':''}">${o.mg?money2(o.mg):'—'}</td>
      <td class="r">${nf(pcQ[String(o.p.bc||'').replace(/^0+/,'')]||0)}</td></tr>`).join('')}</tbody></table></div>`;
  return h+`</div>`;
}

/* ---- l'argent à encaisser : les factures avec un reste dû ---- */
const DOCS=FACT.filter(f=>f&&f.doc&&f.doc.type==='facture'&&(f.doc.reste||0)>0)
  .sort((a,b)=>String(a.d||'').localeCompare(String(b.d||'')));
const duTot=DOCS.reduce((a,f)=>a+(f.doc.reste||0),0);
const duVieux=DOCS.filter(f=>f.d&&f.d<jourMoins(30));
const devisOuverts=FACT.filter(f=>f&&f.doc&&f.doc.type==='devis'&&!f.doc.converti);

/* ---- deux alertes « l'ERP ne ment pas en silence » (21 oct. 2026) ----
   1. une mise en ligne EN VENTE qui n'a pas abouti sur un canal (notée par le Catalogue dans publications-v1, retirée toute seule
      dès que le parfum est vu en vente) ; 2. une réception d'achat dont la part de Perfume City n'est pas (ou pas toute) partie sur Shopify.
   Chacune se coupe dans Réglages. Une alerte coupée ne compte plus dans « points à traiter ». */
const CAN_NOM={site:'perfumestrade.com',sitegros:'le site de gros',perfumecity:'Perfume City'};
/* ---- « Pas en vente partout » (Igal, 25 oct. 2026 : « je veux la liste des parfums dans une rubrique du dashboard et qu'on
   puisse intervenir dessus directement ») — même règle que le filtre Diffusion du Catalogue : un parfum en stock, avec un
   code-barres, est « non » sur un canal quand le relevé de ce canal est lu et qu'il n'y figure pas en vente (brouillon = non).
   « na » (pas de code, relevé jamais lu, canal coupé exprès pour ce parfum) n'est jamais compté. */
const CAN_DIFF=[['site','perfumestrade.com'],['sitegros','wholesale.perfumestrade.com'],['perfumecity','Perfume City']];
/* 30 oct. 2026 (Igal : « j'aimerais pouvoir les mettre en ligne rapidement de cette page, avec le prix d'achat et le prix
   de vente aux endroits où c'est déjà en ligne ») : le relevé se refait après chaque mise en ligne faite depuis le tableau de
   bord, et chaque canal où le parfum est EN VENTE donne son prix (celui que le client paie : la promo s'il y en a une). */
const calcDiff=()=>(function(){
  let SITE={}, S=null; try{ const x=lit('site-stock-v1',{}); if(x&&typeof x==='object'&&!Array.isArray(x)) SITE=x; }catch(e){}
  try{ const x=lit('shopify-pc-prix-v1',null); if(x&&typeof x==='object') S=x; }catch(e){}
  const cles=o=>Object.keys(o||{}).filter(k=>k[0]!=='_');
  const OK={site:cles(SITE).some(k=>SITE[k]&&SITE[k].d), sitegros:cles(SITE).some(k=>SITE[k]&&SITE[k].g), perfumecity:!!S&&cles(S).length>0};
  const S0={}; cles(SITE).forEach(k=>{ S0[k.replace(/^0+/,'')]=k; });
  const siteCle=p=>{ const b=String(p.bc||'').replace(/[^0-9]/g,''); if(!b) return null; if(SITE[b]) return b; return S0[b.replace(/^0+/,'')]||null; };
  const s0=x=>String(x||'').replace(/[^0-9A-Za-z]/g,'').replace(/^0+/,'');
  function statut(p,id){
    const off=(MOD[p.cle]||{}).pcOff; if((Array.isArray(off)&&off.includes(id))||!p.bc||!OK[id]) return 'na';
    if(id==='site'||id==='sitegros'){ const k=siteCle(p); if(!k) return 'non'; const e=SITE[k]; return e&&e[id==='site'?'d':'g']?'oui':'non'; }
    const ks=[p.bc].concat(String((MOD[p.cle]||{}).bcs||'').split(/[\s,;]+/)).map(s0).filter(Boolean);
    for(const k of ks){ const e=S[k]; if(Array.isArray(e)&&e[2]>0) return e[4]===1?'oui':'non'; }
    return ks.some(k=>(S._amb||[]).includes(k))?'oui':'non';
  }
  const L=[]; const n={site:0,sitegros:0,perfumecity:0};
  enStock.forEach(p=>{ const st={}; let manque=false;
    CAN_DIFF.forEach(([id])=>{ st[id]=statut(p,id); if(st[id]==='non'){ n[id]++; manque=true; } });
    if(manque) L.push({p,st}); });
  L.sort((a,b)=>cap(b.p)-cap(a.p));
  /* le prix là où le parfum est en vente */
  function prix(p,id){
    if(id==='site'||id==='sitegros'){ const k=siteCle(p); const e=k&&SITE[k]&&SITE[k][id==='site'?'d':'g']; if(!e) return null;
      const ps=+e.ps, pr=+e.pr; return ps>0&&(!(pr>0)||ps<pr)?ps:(pr>0?pr:null); }
    const ks=[p.bc].concat(String((MOD[p.cle]||{}).bcs||'').split(/[\s,;]+/)).map(s0).filter(Boolean);
    for(const k of ks){ const e=S&&S[k]; if(Array.isArray(e)&&e[2]>0) return +e[2]; }
    return null;
  }
  /* le parfum est-il sur ce site, mais RETIRÉ de la vente (brouillon) ? (31 oct. 2026 : 494 fiches du gros dans ce cas) */
  function retire(p,id){ if(id!=='site'&&id!=='sitegros') return false; const R=SITE._retires&&SITE._retires[id==='site'?'d':'g']; if(!R) return false;
    const b=String(p.bc||'').replace(/[^0-9]/g,''); if(!b) return false; if(R[b]) return true; const b0=b.replace(/^0+/,''); return Object.keys(R).some(k=>k.replace(/^0+/,'')===b0); }
  return {OK,L,n,prix,retire};
})();
let DIFF=calcDiff();
const PUB_KO=(()=>{ let O={}; try{ O=lit('publications-v1',{})||{}; }catch(e){}
  return Object.keys(O).map(k=>Object.assign({k},O[k])).filter(e=>e&&e.ko&&typeof e.ko==='object'&&Object.keys(e.ko).length)
    .sort((a,b)=>String(b.t||'').localeCompare(String(a.t||''))); })();
const PC_KO=(REG.alerteStockPC===false)?[]:FACT.filter(f=>f&&f.sens==='achat'&&f.pcShopify&&(f.lignes||[]).some(l=>l.pc>0)
    &&(f.pcShopify.etat==='echec'||f.pcShopify.etat==='partiel'
       ||(f.pcShopify.etat==='attente'&&Date.now()-new Date(f.t||0).getTime()>180000)))   /* « attente » trop longue : la page a été fermée avant la fin de l'envoi */
  .sort((a,b)=>String(b.t||'').localeCompare(String(a.t||'')));
const quand=t=>{ if(!t) return ''; try{ return new Date(t).toLocaleString('en-US',{timeZone:'America/New_York',month:'2-digit',day:'2-digit',hour:'2-digit',minute:'2-digit'}); }catch(e){ return ''; } };
function blocDiff(){
  const L=DIFF.L, n=DIFF.n, tot=L.length;
  const lu=CAN_DIFF.filter(([id])=>DIFF.OK[id]);
  let h=`<h2 class="sec">Pas en vente partout <em>en stock, mais absent d'au moins un canal</em>
      <a href="catalogue.html?diff=any">Voir dans le Catalogue</a></h2>`;
  if(!lu.length) return h+`<div class="vide"><p>Les relevés des sites ne sont pas encore lus : ouvre le Catalogue une fois, puis reviens.</p></div>`;
  if(!tot) return h+`<div class="alerte ok"><h3>Tout le stock est en vente sur les trois canaux</h3></div>`;
  const pz=(st,p,id)=>{ if(st==='oui'){ const v=DIFF.prix(p,id); return '<span class="dok">✓</span>'+(v!=null?'<div class="dpx" data-nolang>'+money2(v)+'</div>':''); }
    return st==='non'?'<span class="dko">✗</span>'+(DIFF.retire(p,id)?'<div class="dpx" style="color:var(--ink-3)">'+L3('retiré de la vente','withdrawn from sale','retirado de la venta')+'</div>':''):'<span class="dna">—</span>'; };
  h+=`<div class="alerte"><h3>${nf(tot)} parfum${tot>1?'s':''} en stock pas en vente partout</h3>
      <p>${CAN_DIFF.map(([id,nom])=>DIFF.OK[id]?`<a href="catalogue.html?diff=${id}" data-nolang><b>${nf(n[id])}</b> ${esc(nom)}</a>`:'').filter(Boolean).join(' · ')}.
      « Mettre en ligne » ouvre la fiche du parfum sur « Mes canaux de vente » : chaque site où il manque a son bouton
      (« Mettre en ligne », ou « Remettre en vente » s'il y est retiré de la vente), avec son prix à côté. La liste se met à jour quand tu fermes la fiche.</p></div>
    <div class="wrapx"><table class="tbl"><thead><tr><th>Référence</th><th class="r">Reste</th><th class="r">Prix d'achat</th>
      ${CAN_DIFF.map(([id,nom])=>`<th class="c" data-nolang>${esc(nom)}</th>`).join('')}<th></th></tr></thead><tbody>
    ${L.slice(0,vusDiff).map(({p,st})=>`<tr>
      <td class="ref"><div class="mq">${esc(p.marque||'')}</div><b>${esc(p.nom||'')}${tyBadge(p.cle)}</b><span>${esc(p.bc||'')}</span></td>
      <td class="r">${nf(p.qte)}</td>
      <td class="r" data-nolang>${p.pa!=null&&p.pa!==''?money2(+p.pa):'—'}</td>
      ${CAN_DIFF.map(([id])=>`<td class="c">${pz(st[id],p,id)}</td>`).join('')}
      <td class="r"><button class="btn" data-mel="${esc(p.cle)}">Mettre en ligne</button></td></tr>`).join('')}
    </tbody></table></div>
    ${tot>vusDiff?`<p><button class="btn" id="plusDiff">Afficher plus (${nf(tot-vusDiff)} restants)</button></p>`:''}`;
  return h;
}
let vusDiff=25;
function cmdOuvre(){
  const L=bas.filter(p=>CMD.has(p.cle)); if(!L.length) return;
  const Q={}; L.forEach(p=>{ const h=dernierAchat(p.cle); Q[p.cle]=Math.max(1,(h&&+h.q)||6); });
  const v=document.createElement('div'); v.className='mvoile';
  const lig=()=>L.map(p=>{ const h=dernierAchat(p.cle);
    return `<tr><td><div class="mq" style="font-size:10px;color:var(--iris);font-weight:700;letter-spacing:.06em;text-transform:uppercase">${esc(p.marque||'')}</div><b>${esc(p.nom||'')}</b><div style="font-size:11.5px;color:var(--ink-3)" data-nolang>${esc(p.bc||'')}</div></td>
      <td class="r">${nf(p.qte)}</td>
      <td class="r"><input type="number" min="1" step="1" data-q="${esc(p.cle)}" value="${Q[p.cle]}"></td>
      <td class="r" data-nolang>${h?money2(h.p)+'<div style="font-size:11.5px;color:var(--ink-3)">'+esc(String(h.d).slice(0,10))+'</div>':'—'}</td>
      <td>${h&&h.f?esc(h.f):'—'}</td></tr>`; }).join('');
  v.innerHTML=`<div class="mfen" role="dialog" aria-modal="true"><h3>Liste à commander</h3>
    <p class="sous2">${nf(L.length)} parfum${L.length>1?'s':''} sous le seuil. Corrige les quantités, puis Excel, WhatsApp ou copier. Rien ne change dans l'ERP.</p>
    <table><thead><tr><th>Référence</th><th class="r">Reste</th><th class="r">À commander</th><th class="r">Dernier prix payé</th><th>Dernier fournisseur</th></tr></thead><tbody>${lig()}</tbody></table>
    <div id="cmd-rep" class="mrep"></div>
    <div class="mbtn"><button class="btn" id="cmd-ferme">Fermer</button><button class="btn" id="cmd-copie">Copier</button><button class="btn" id="cmd-wa">WhatsApp</button><button class="btn pri" id="cmd-xlsx">Excel</button></div></div>`;
  document.body.appendChild(v);
  v.querySelectorAll('[data-q]').forEach(i=>i.oninput=()=>{ Q[i.dataset.q]=Math.max(1,parseInt(i.value,10)||1); });
  const lignes=()=>L.map(p=>{ const h=dernierAchat(p.cle); return {p,q:Q[p.cle],h}; });
  const texte=()=>'Commande — Perfumes Trade — '+new Date().toLocaleDateString('en-US',{timeZone:'America/New_York'})+'\n'
    +lignes().map(x=>`• ${(x.p.marque||'')+' '+(x.p.nom||'')} (${x.p.bc||''}) × ${x.q}`).join('\n');
  v.querySelector('#cmd-ferme').onclick=()=>v.remove();
  v.querySelector('#cmd-xlsx').onclick=()=>{ try{ sortieXlsx({titre:'Liste à commander',filtre:nf(L.length)+' parfum(s) sous le seuil de '+REG.seuilQte,fichier:'liste-a-commander',
      colonnes:[{t:'Marque'},{t:'Parfum'},{t:'Code-barres'},{t:'Reste',y:'n'},{t:'À commander',y:'n'},{t:'Dernier prix payé',y:'m'},{t:'Date',y:'d'},{t:'Dernier fournisseur'}],
      lignes:lignes().map(x=>[x.p.marque||'',x.p.nom||'',x.p.bc||'',x.p.qte,x.q,x.h?x.h.p:'',x.h?String(x.h.d).slice(0,10):'',x.h&&x.h.f?x.h.f:''])});
      v.querySelector('#cmd-rep').textContent='Fichier Excel téléchargé.'; }catch(e){ v.querySelector('#cmd-rep').textContent='Excel impossible : '+((e&&e.message)||e); } };
  v.querySelector('#cmd-wa').onclick=()=>{ window.open('https://wa.me/?text='+encodeURIComponent(texte()),'_blank','noopener'); };
  v.querySelector('#cmd-copie').onclick=async()=>{ try{ await navigator.clipboard.writeText(texte()); v.querySelector('#cmd-rep').textContent='Liste copiée.'; }catch(e){ v.querySelector('#cmd-rep').textContent='Copie impossible : sélectionne le texte à la main.'; } };
}
/* ---- un envoi de stock aux sites BLOQUÉ (plus de 25 parfums à zéro d'un coup, ou refus du site) : jusqu'ici seulement au
   Journal (« stock NON envoyé aux sites — … »). Igal, 25 oct. 2026 : au tableau de bord, avec « Envoyer quand même ». */
const STB=(function(){
  const sept=Date.now()-7*86400000;
  const L=JOU.filter(e=>e&&e.act==='stock'&&/^stock (NON )?envoyé aux sites/.test(e.lib||'')&&new Date(e.t||0).getTime()>sept)
    .sort((a,b)=>String(b.t||'').localeCompare(String(a.t||'')));
  const d=L[0]; if(!d||!/^stock NON/.test(d.lib)) return null;   /* le dernier envoi est passé : rien à reprendre */
  return {t:d.t,raison:String(d.lib).replace(/^stock NON envoyé aux sites\s*—\s*/,''),det:Array.isArray(d.det)?d.det:[],n:d.n||(d.det||[]).length};
})();
function blocStockBloque(){
  if(!STB) return '';
  const peutEnv=(()=>{ try{ const s=session(); return !!(s&&['patron','admin'].includes(s.role)&&typeof ckTok==='function'&&ckTok()); }catch(e){ return false; } })();
  return `<h2 class="sec">Stock pas envoyé aux sites <em>le dernier envoi automatique a été refusé</em>
      <a href="journal.html">Voir le journal</a></h2>
    <div class="alerte crit"><h3>${nf(STB.n)} parfum${STB.n>1?'s':''} dont le stock n'est pas parti sur les sites</h3>
      <p><span data-nolang>${esc(quand(STB.t))}</span> — ${esc(STB.raison)}</p>
      <p>${STB.det.slice(0,12).map(x=>`<span data-nolang>${esc(x.ref||x.bc||'')} → ${nf(x.ap)}</span>`).join(' · ')}${STB.det.length>12?' · …':''}</p>
      ${peutEnv?`<p><button class="btn pri" id="stb-go">Envoyer quand même</button> <span style="font-size:12.5px;color:var(--ink-3)">les quantités actuelles de l'ERP, sur les deux sites</span></p>`
               :`<p style="font-size:12.5px;color:var(--ink-3)">Seul le Patron, relié au cockpit, peut forcer l'envoi (Catalogue › Envoyer le stock au site).</p>`}
      <div id="stb-rep" class="mrep"></div></div>`;
}
async function stockBloqueEnvoie(btn){
  if(!STB||!STB.det.length){ return; }
  let Qt={}; try{ Qt=(lit('stock-erp-v1',{})||{}).q||{}; }catch(e){}
  const lignes=STB.det.map(x=>{ const b=String(x.bc||''); const q=Qt[b]!=null?Qt[b]:(Qt[b.replace(/^0+/,'')]!=null?Qt[b.replace(/^0+/,'')]:x.ap); return b&&q!=null?{bc:b,q:+q}:null; }).filter(Boolean);
  if(!lignes.length) return;
  if(!confirm('Envoyer maintenant le stock de '+lignes.length+' parfum(s) sur les deux sites, en passant outre le garde-fou ?')) return;
  btn.disabled=true; btn.textContent='Envoi…'; const rep=$('stb-rep');
  const out=[];
  for(const quel of ['','gros']){
    try{ const r=await fetch(CK_URL+'/api/o/'+CK_ORG+'/site/stock',{method:'POST',headers:{'Content-Type':'application/json',Authorization:'Bearer '+ckTok()},body:JSON.stringify({quel,confirme:true,lignes})});
      const j=await r.json().catch(()=>({})); out.push((quel?'site de gros':'perfumestrade.com')+' : '+(r.ok?nf(j.ecrites||0)+' fiche(s) mise(s) à jour':'refusé — '+(j.erreur||r.status)));
    }catch(e){ out.push((quel?'site de gros':'perfumestrade.com')+' : serveur injoignable'); }
  }
  try{ const J=lit('crm-journal-v1',[])||[]; J.push({t:new Date().toISOString(),u:(session()||{}).nom||'',act:'stock',lib:'stock envoyé aux sites — forcé depuis le tableau de bord : '+out.join(' / '),n:lignes.length,det:STB.det.slice(0,50)}); ecrit('crm-journal-v1',J); }catch(e){}
  rep.textContent=out.join(' · '); btn.textContent='Envoyé';
}
function blocPubKo(){
  if(!PUB_KO.length) return '';
  return `<h2 class="sec">Mises en ligne à reprendre <em>le parfum a été envoyé, il n'est pas en vente</em>
      <a href="catalogue.html">Ouvrir le Catalogue</a></h2>
    <div class="alerte crit"><h3>${nf(PUB_KO.length)} parfum${PUB_KO.length>1?'s':''} pas vraiment en ligne</h3>
      <p>Chaque ligne dit sur quel canal, et pourquoi. Elle disparaît toute seule dès que le parfum est vu en vente sur ce canal
      (le relevé est lu quand le Catalogue s'ouvre). Après correction : bouton « Mettre en ligne » sur la fiche.</p></div>
    <div class="wrapx"><table class="tbl"><thead><tr><th>Parfum</th><th>Canal et raison</th><th>Depuis</th><th></th></tr></thead><tbody>
    ${PUB_KO.slice(0,30).map(e=>`<tr>
      <td class="ref"><b>${esc(e.nom||'(sans nom)')}</b><span>${esc(e.bc||'')}</span></td>
      <td>${Object.keys(e.ko).map(c=>`<div><b>${esc(CAN_NOM[c]||c)}</b> — ${esc((e.ko[c]||{}).r||'')}</div>`).join('')}</td>
      <td data-nolang>${esc(quand(e.t))}</td>
      <td class="r" style="white-space:nowrap">${e.bc?`<a href="catalogue.html?q=${encodeURIComponent(e.bc)}" style="color:var(--iris);font-weight:600;text-decoration:none">Voir la fiche</a> · `:''}<button type="button" class="plus" data-pubx="${esc(e.k)}" style="display:inline;width:auto;margin:0;padding:3px 9px;font-size:12px">C'est réglé</button></td></tr>`).join('')}
    </tbody></table></div>${PUB_KO.length>30?`<p class="rien">… et ${nf(PUB_KO.length-30)} autre(s).</p>`:''}`;
}
function blocPcKo(){
  if(!PC_KO.length) return '';
  return `<h2 class="sec">Stock de Perfume City à renvoyer à Shopify <em>l'ERP est à jour, la boutique pas encore</em>
      <a href="factures.html">Ouvrir les factures</a></h2>
    <div class="alerte crit"><h3>${nf(PC_KO.length)} réception${PC_KO.length>1?'s':''} où le stock n'a pas suivi sur Shopify</h3>
      <p>Ouvre la facture et clique « Renvoyer à Shopify » : l'envoi ne compte jamais deux fois. La ligne disparaît quand l'envoi a réussi.</p></div>
    <div class="wrapx"><table class="tbl"><thead><tr><th>Facture</th><th>Fournisseur</th><th>Flacons Perfume City</th><th>Ce qui s'est passé</th><th></th></tr></thead><tbody>
    ${PC_KO.slice(0,20).map(f=>{ const P=f.pcShopify||{};
      const mal=(P.lignes||[]).filter(l=>!['ok','deja','ignore'].includes(l.etat));
      const u=(f.lignes||[]).reduce((a,l)=>a+(l.pc||0),0);
      const dit=P.etat==='echec'?('envoi raté — '+(P.raison||'raison inconnue'))
        :P.etat==='partiel'?(nf(mal.length)+' parfum'+(mal.length>1?'s':'')+' pas partis : '+mal.slice(0,3).map(l=>(l.nom||l.bc)+' ('+(l.raison||l.etat)+')').join(' ; ')+(mal.length>3?' …':''))
        :"envoi jamais terminé (la page a été fermée ou l'ERP n'était pas relié au cockpit)";
      return `<tr><td><b>${esc(f.num||'')}</b><div class="rien" data-nolang>${esc(dfr(f.d))}</div></td><td>${esc(f.tiers||'—')}</td><td class="r">${nf(u)}</td><td>${esc(dit)}</td>
        <td class="r"><a href="factures.html?ouvre=${encodeURIComponent(f.id)}" style="color:var(--iris);font-weight:600;text-decoration:none">Ouvrir</a></td></tr>`; }).join('')}
    </tbody></table></div>`;
}

/* ---- LES ESPÈCES EN CAISSE (Igal, 24 oct. 2026) ----
   Sam laisse un fonds de caisse (200 $, Réglages) dans le tiroir de Lightspeed et récolte les espèces chaque semaine.
   Chaque vente de la caisse porte depuis le 24 oct. sa façon de paiement (paie.especes) : on additionne les espèces entrées
   depuis la dernière récolte (les remboursements en espèces viennent en moins), et le bouton « Récolte faite » note ce que
   Sam a vraiment pris. L'écart entre ce qu'il a pris et ce que l'ERP attendait est gardé et va au Journal : c'est lui qui
   révèle une vente oubliée ou une erreur de caisse. Point de départ : le 23 oct. 2026 à 23 h (Miami), 200 $ dans le tiroir. */
const K_CAISSE='caisse-especes-v1', CAISSE_DEBUT='2026-10-24T03:00:00.000Z';
const cash=v=>(typeof _usd==='function')?_usd(v,2):('$'+Number(v||0).toFixed(2));   /* les espèces se comptent au centime */
function caisseLit(){ let C=null; try{ C=lit(K_CAISSE,null); }catch(e){} if(!C||typeof C!=='object') C={}; if(!Array.isArray(C.recoltes)) C.recoltes=[]; if(!C.debut) C.debut=CAISSE_DEBUT; return C; }
const caisseFond=()=>(REG.fondCaisse!=null&&isFinite(+REG.fondCaisse))?+REG.fondCaisse:200;
/* les espèces d'une vente : ce que la caisse a dit (paie), sinon une vente/un retour saisi « espèces » dans l'ERP */
/* 27 oct. 2026 : le paiement gardé à part par le cockpit (caisse-paie-v1) complète une vente enregistrée sans paiement */
let _PAIE=null;
function paieDe(f){ if(f&&f.paie&&typeof f.paie==='object') return f.paie; if(!f||!f._i) return null;
  if(!_PAIE){ try{ _PAIE=lit('caisse-paie-v1',{})||{}; }catch(e){ _PAIE={}; } }
  const p=_PAIE[String(f._i).replace(/^fa\|/,'')]; return (p&&typeof p==='object')?p:null; }
function especesDe(f){
  if(!f||f.sens!=='vente'||f.annule) return 0;
  /* le paiement détaillé ne vaut que pour la caisse de Sam (Lightspeed) : les espèces de Perfume City (Shopify) sont dans
     le tiroir de la boutique, pas dans le sien (27 oct. 2026) */
  if(String(f.auto||'')!=='lightspeed'&&f.paie) return 0;
  { const p=String(f.auto||'')==='lightspeed'?paieDe(f):null; if(p&&isFinite(+p.especes)) return +p.especes; }
  if(String(f.auto||'')==='shopify-pc') return 0;
  const mode=(f.doc&&f.doc.pmode)||f.mode||'';
  if(mode!=='especes') return 0;
  const tot=(f.doc&&isFinite(+f.doc.total))?+f.doc.total:(+f.montant||0);
  return f.retour?-Math.abs(tot):tot;
}
function caisseEtat(){
  const C=caisseLit(), derniere=C.recoltes.length?C.recoltes[C.recoltes.length-1]:null, depuis=derniere?derniere.t:C.debut;
  let FA=[]; try{ FA=lit(KFACT,[])||[]; }catch(e){ FA=FACT; }
  const V=FA.filter(f=>f&&String(f.t||'')>depuis&&especesDe(f)!==0);
  const entrees=Math.round(V.reduce((a,f)=>a+especesDe(f),0)*100)/100;
  return {C,derniere,depuis,entrees,nV:V.length,fond:caisseFond(),enCaisse:Math.round((caisseFond()+entrees)*100)/100};
}
function blocCaisse(){
  const s=session(); if(!s||!['patron','admin'].includes(String(s.role||''))) return '';
  const e=caisseEtat();
  const quand=t=>{ try{ const d=new Date(t); return d.toLocaleDateString('en-US',{timeZone:'America/New_York',month:'numeric',day:'numeric',year:'numeric'})+' '+d.toLocaleTimeString('en-US',{timeZone:'America/New_York',hour:'numeric',minute:'2-digit'}); }catch(x){ return String(t).slice(0,16); } };
  const R=e.C.recoltes.slice(-10).reverse(); const nR=e.C.recoltes.length;
  return `<h2 class="sec">${L3('Espèces en caisse','Cash in the till','Efectivo en caja')} <em>${L3('fonds de caisse','till float','fondo de caja')} <span data-nolang>${cash(e.fond)}</span>, ${L3('réglable dans Réglages','adjustable in Settings','ajustable en Ajustes')}</em></h2>
    <div class="alerte ok" id="caisse-bloc">
      <div class="kpis" style="margin:0 0 10px">
        <div class="kpi"><span class="v" data-nolang>${cash(e.entrees)}</span><span class="k">${L3('encaissé en espèces depuis la dernière récolte','cash taken since the last collection','efectivo cobrado desde la última recogida')}${e.nV?' · <span data-nolang>'+nf(e.nV)+'</span> '+L3('vente'+(e.nV>1?'s':''),'sale'+(e.nV>1?'s':''),'venta'+(e.nV>1?'s':'')):''}</span></div>
        <div class="kpi iris"><span class="v" data-nolang>${cash(e.enCaisse)}</span><span class="k">${L3('en caisse maintenant','in the till now','en caja ahora')} (${L3('fonds','float','fondo')} <span data-nolang>${cash(e.fond)}</span> + ${L3('espèces','cash','efectivo')})</span></div>
        <div class="kpi"><span class="v" style="font-size:18px" data-nolang>${e.derniere?quand(e.derniere.t):quand(e.depuis)}</span><span class="k">${e.derniere?L3('dernière récolte :','last collection:','última recogida:')+' <span data-nolang>'+cash(e.derniere.montant)+'</span> '+L3('par','by','por')+' <span data-nolang>'+esc(e.derniere.u||'')+'</span>'+(e.derniere.ecart?' · '+L3('écart','difference','diferencia')+' <span data-nolang>'+(e.derniere.ecart>0?'+':'')+cash(e.derniere.ecart)+'</span>':''):L3('point de départ (200 $ dans le tiroir)','starting point ($200 in the drawer)','punto de partida (200 $ en el cajón)')}</span></div>
      </div>
      <div id="caisse-form" style="display:flex;gap:10px;align-items:center;flex-wrap:wrap">
        <button class="btn pri" id="caisse-go" style="padding:9px 16px;border-radius:9px;border:0;background:var(--iris);color:#fff;font-weight:700;cursor:pointer">${L3('Récolte faite','Collection done','Recogida hecha')}</button>
        <span class="rien">${L3('Sam compte ce qu\'il a pris en laissant','Sam counts what he took, leaving','Sam cuenta lo que se llevó dejando')} <span data-nolang>${cash(e.fond)}</span> ${L3('dans le tiroir, et le note ici.','in the drawer, and notes it here.','en el cajón, y lo anota aquí.')}</span>
      </div>
      ${R.length?`<details style="margin-top:10px"><summary style="cursor:pointer;color:var(--ink-2);font-size:13px"><span data-nolang>${nf(nR)}</span> ${L3('récolte'+(nR>1?'s':'')+' notée'+(nR>1?'s':''),'collection'+(nR>1?'s':'')+' noted','recogida'+(nR>1?'s':'')+' anotada'+(nR>1?'s':''))}</summary>
        <table class="tbl" style="margin-top:8px"><thead><tr><th>${L3('Quand','When','Cuándo')}</th><th>${L3('Qui','Who','Quién')}</th><th class="r">${L3('Pris','Taken','Retirado')}</th><th class="r">${L3('Attendu','Expected','Esperado')}</th><th class="r">${L3('Écart','Difference','Diferencia')}</th></tr></thead><tbody>
        ${R.map(r=>`<tr><td data-nolang>${esc(quand(r.t))}</td><td data-nolang>${esc(r.u||'')}</td><td class="r" data-nolang>${cash(r.montant)}</td><td class="r" data-nolang>${cash(r.attendu)}</td><td class="r" data-nolang style="${r.ecart?'color:var(--crit);font-weight:700':''}">${r.ecart?(r.ecart>0?'+':'')+cash(r.ecart):'—'}</td></tr>`).join('')}
        </tbody></table></details>`:''}
    </div>`;
}
function caisseBranche(){
  const b=$('caisse-go'); if(!b) return;
  b.onclick=()=>{
    const e=caisseEtat(); const f=$('caisse-form');
    f.innerHTML=`<label style="display:flex;gap:8px;align-items:center;font-weight:600">${L3('Montant pris','Amount taken','Importe retirado')}
        <input type="number" id="caisse-mt" min="0" step="0.01" value="${e.entrees.toFixed(2)}" style="width:120px;padding:8px;border:1px solid var(--line);border-radius:8px;font-size:15px;text-align:right"> $</label>
      <button class="btn pri" id="caisse-ok" style="padding:9px 16px;border-radius:9px;border:0;background:var(--iris);color:#fff;font-weight:700;cursor:pointer">${L3('Noter la récolte','Record the collection','Anotar la recogida')}</button>
      <button id="caisse-ann" style="padding:9px 14px;border-radius:9px;border:1px solid var(--line);background:var(--surface);cursor:pointer">${L3('Annuler','Cancel','Cancelar')}</button>
      <span class="rien">${L3('L\'ERP attendait','The ERP expected','El ERP esperaba')} <span data-nolang>${cash(e.entrees)}</span> ; ${L3('le tiroir garde','the drawer keeps','el cajón conserva')} <span data-nolang>${cash(e.fond)}</span>.</span>`;
    setTimeout(()=>{ const i=$('caisse-mt'); if(i){ i.focus(); i.select(); } },30);
    $('caisse-ann').onclick=()=>dessine();
    $('caisse-ok').onclick=()=>{
      const v=parseFloat(String($('caisse-mt').value).replace(',','.')); if(!isFinite(v)||v<0){ $('caisse-mt').focus(); return; }
      const e2=caisseEtat(); const montant=Math.round(v*100)/100, ecart=Math.round((montant-e2.entrees)*100)/100;
      const s=session(); const u=(s&&s.nom)||'(non renseigné)';
      const C=caisseLit(); C.recoltes.push({t:new Date().toISOString(),u,montant,attendu:e2.entrees,ecart,nV:e2.nV}); if(C.recoltes.length>200) C.recoltes=C.recoltes.slice(-200);
      ecrit(K_CAISSE,C);
      try{ const J=lit(KJOU,[])||[]; J.push({t:new Date().toISOString(),u,act:'caisse',lib:'récolte des espèces : '+cash(montant)+' pris'+(ecart?' — écart de '+(ecart>0?'+':'')+cash(ecart)+' avec ce que l\'ERP attendait ('+cash(e2.entrees)+')':' — comme attendu')+', fonds de caisse '+cash(e2.fond)+' laissé',ref:'',av:cash(e2.entrees),ap:cash(montant),n:e2.nV,impact:0,det:[]}); ecrit(KJOU,J); }catch(x){}
      dessine();
    };
  };
}

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

/* ---- Les ventes du site et de la caisse s'enregistrent toutes seules à l'ouverture (voir
   _file_auto.py). Ce qui reste ici, c'est ce qui n'a PAS pu l'être : une référence inconnue. ---- */
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
  /* les commandes qui attendent d'être expédiées : le stock n'a pas encore bougé */
  let EXPA=[]; try{ const e=JSON.parse(localStorage.getItem('expeditions-v1')||'[]'); if(Array.isArray(e)) EXPA=e.filter(x=>x&&x.statut==='attente'); }catch(e){}
  if(EXPA.length){ const tard=EXPA.filter(x=>x.d&&x.d<=isoJour(new Date(Date.now()-2*86400000))).length;
    regards.push({t:tard?'warn':'info',lib:`${nf(EXPA.length)} commande${EXPA.length>1?'s':''} à expédier`,
      d:`${money2(EXPA.reduce((a,x)=>a+(x.montant||0),0))} pas encore sortis du stock${tard?' · '+nf(tard)+' depuis 2 jours ou plus':''}`,lien:'expeditions.html'}); }
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
  return `<span class="ev ${k}"><span data-nolang>${k==='eq'?'≈':(p>0?'▲':'▼')}</span> ${Math.abs(Math.round(p))} % ${quoi}</span>`;
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
/* ---- « Liste à commander » (Igal, 25 oct. 2026 : « des cases pour pouvoir intervenir ») : on coche les parfums en stock
   bas, et on obtient la liste à envoyer au fournisseur — quantité à racheter (modifiable), dernier prix payé et dernier
   fournisseur (prix-achat-hist-v1) — en Excel, en WhatsApp ou copiée. Rien n'est modifié dans l'ERP. */
const CMD=new Set();
let HIST={}; try{ HIST=lit('prix-achat-hist-v1',{})||{}; }catch(e){}
function dernierAchat(cle){ const l=(HIST[cle]||[]).filter(x=>x&&x.d).slice().sort((a,b)=>String(b.d).localeCompare(String(a.d))); return l[0]||null; }
function cmdBarre(){
  const n=CMD.size;
  return `<div class="cmdbar"><label><input type="checkbox" id="cmd-tout">Tout cocher</label>
    <button class="btn pri" id="cmd-go" ${n?'':'disabled'}>Liste à commander${n?' ('+nf(n)+')':''}</button>
    <span>${n?'':'Coche les parfums à commander, puis fais la liste : Excel, WhatsApp ou copier.'}</span></div>`;
}
function tblBas(){
  const l=bas.slice(0,vus);
  return cmdBarre()+`<div class="wrapx"><table class="tbl"><thead><tr><th></th>
    <th>Référence</th><th class="r">Reste</th><th class="r">Prix d'achat</th>
    <th class="r">Marchandise</th><th class="r">Prix de gros</th></tr></thead><tbody>
    ${l.map(p=>`<tr>
      <td><input type="checkbox" data-cmd="${esc(p.cle)}" ${CMD.has(p.cle)?'checked':''}></td>
      <td class="ref"><div class="mq">${esc(p.marque||'')}</div>
        <b>${esc(p.nom||'')}${tyBadge(p.cle)}</b><span>${esc(p.bc||'')}</span></td>
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
      Les ventes arrivent toutes seules des sites, de la caisse et d'Amazon, ou à la main par
      <a href="ventes.html">Ventes → Enregistrer une vente</a>.</p></div>` : '';
  /* Les ventes déposées par le site et la caisse : une action à faire, donc en premier. */
  const attente = FILE_ATT.length ? `<div class="att">
      <b>${nf(FILE_ATT.length)} vente${FILE_ATT.length>1?'s':''} en attente d'une référence</b>
      <span class="d">Le site ou la caisse ${FILE_ATT.length>1?'les ont':"l'a"} déposée${FILE_ATT.length>1?'s':''}, mais une ligne porte un code que le catalogue
      ne connaît pas : le stock n'a pas bougé. Dans Ventes, dis quel parfum c'est, et c'est enregistré.</span>
      <a class="go" href="ventes.html">Régler</a></div>` : '';

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

  /* --- les espèces en caisse, puis les deux alertes qui ne doivent jamais rester silencieuses --- */
  h+=blocCaisse()+blocPcKo()+blocStockBloque()+blocDiff()+blocPubKo();

  /* --- par canal : depuis le 1er nov. 2026, c'est le récap « Ventes par canal » en tête de page (_recap.py),
     avec le choix de la période ; l'ancien bloc « D'où vient l'argent · 30 derniers jours » est retiré. --- */

  h+=blocPC();

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
        <td class="ref"><div class="mq">${esc(x.p.marque||'')}</div><b>${esc(x.p.nom||'')}${tyBadge(x.p.cle)}</b><span>${esc(x.p.bc||'')}</span></td>
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
        <td class="ref"><div class="mq">${esc(o.p.marque||'')}</div><b>${esc(o.p.nom||'')}${tyBadge(o.p.cle)}</b><span>${esc(o.p.bc||'')}</span></td>
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
        <td class="ref"><div class="mq">${esc(p.marque||'')}</div><b>${esc(p.nom||'')}${tyBadge(p.cle)}</b><span>${esc(p.bc||'')}</span></td>
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
        <p>Aucune référence en stock ne descend sous <b>${REG.seuilQte} flacons</b>.</p></div>`;
  else {
    const c=bas.reduce((a,p)=>a+cap(p),0);
    const un=bas.filter(p=>p.qte<=1).length;
    h+=`<div class="alerte"><h3>${nf(bas.length)} référence${bas.length>1?'s':''} sous ${REG.seuilQte} flacons</h3>
      <p>Elles représentent <b>${money(c)}</b> de marchandise${un?`, dont <b>${nf(un)}</b> à un seul flacon ou moins`:''}.
</p></div>`
      +tblBas();
  }

  h+=`<h2 class="sec">Sans photo <em>en stock, et aucune photo nulle part</em>
      <a href="catalogue.html?photo=0">Voir dans le catalogue</a></h2>`;
  if(!sansPhoto.length)
    h+=`<div class="alerte ok"><h3>Tout le stock a une photo</h3></div>`;
  else {
    const c=sansPhoto.reduce((a,p)=>a+cap(p),0);
    h+=`<div class="alerte"><h3>${nf(sansPhoto.length)} parfum${sansPhoto.length>1?'s':''} en stock sans photo</h3>
      <p>Ni dans le fichier, ni prise dans l'ERP, ni sur un des deux sites, ni chez Perfume City. Soit <b>${money(c)}</b> de marchandise qu'on ne peut pas montrer.</p></div>
      <div class="wrapx"><table class="tbl"><thead><tr><th>Référence</th><th class="r">Reste</th><th class="r">Marchandise</th></tr></thead><tbody>
      ${sansPhoto.slice(0,25).map(p=>`<tr>
        <td class="ref"><div class="mq">${esc(p.marque||'')}</div><b>${esc(p.nom||'')}${tyBadge(p.cle)}</b><span>${esc(p.bc||'')}</span></td>
        <td class="r">${nf(p.qte)}</td><td class="r">${money(cap(p))}</td></tr>`).join('')}</tbody></table></div>
      ${sansPhoto.length>25?`<p style="font-size:13px;color:var(--ink-3)">et ${nf(sansPhoto.length-25)} autres dans le catalogue.</p>`:''}`;
  }

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
  try{ caisseBranche(); }catch(e){}
  const b=$('plus'); if(b) b.onclick=()=>{ vus+=25; dessine(); };
  const bd=$('plusDiff'); if(bd) bd.onclick=()=>{ vusDiff+=50; dessine(); };
  /* la fiche du Catalogue s'ouvre par-dessus le tableau de bord, la fenêtre « Mettre en ligne » déjà ouverte ; à la fermeture
     le relevé des canaux est relu et la liste redessinée à la même hauteur */
  document.querySelectorAll('[data-mel]').forEach(b=>b.onclick=()=>{
    if(typeof ficheFenetre!=='function'){ location.href='catalogue.html#cle='+encodeURIComponent(b.dataset.mel)+'&mel=1'; return; }
    ficheFenetre(b.dataset.mel,()=>{ const y=window.scrollY; try{ DIFF=calcDiff(); }catch(e){} dessine(); window.scrollTo(0,y); },'&canaux=1'); });
  document.querySelectorAll('[data-cmd]').forEach(c=>c.onchange=()=>{ if(c.checked) CMD.add(c.dataset.cmd); else CMD.delete(c.dataset.cmd);
    const g=$('cmd-go'); if(g){ g.disabled=!CMD.size; g.textContent='Liste à commander'+(CMD.size?' ('+nf(CMD.size)+')':''); } });
  const ct=$('cmd-tout'); if(ct) ct.onchange=()=>{ bas.slice(0,vus).forEach(p=>{ if(ct.checked) CMD.add(p.cle); else CMD.delete(p.cle); }); dessine(); };
  const cg=$('cmd-go'); if(cg) cg.onclick=cmdOuvre;
  const sb=$('stb-go'); if(sb) sb.onclick=()=>stockBloqueEnvoie(sb);
  document.querySelectorAll('[data-pubx]').forEach(b=>b.onclick=()=>{ try{ const O=lit('publications-v1',{})||{}; delete O[b.dataset.pubx]; ecrit('publications-v1',O); }catch(e){} location.reload(); });
  const pts=rupture.length+perte.length+DOCS.length+PUB_KO.length+PC_KO.length+DIFF.L.length+(STB?1:0);
  $('src').innerHTML=`${nf(pts)} point${pts>1?'s':''} à traiter<br>${nf(enStock.length)} références en stock`;
}
function majUser(){ try{ piedSession(); }catch(e){} }
majUser();
$('sfoot').innerHTML=VL.length?`${nf(VL.length)} lignes de vente<br>seuils dans Réglages`:'seuils réglables<br>dans Réglages';
const dfr=d=>{ if(!d) return '—'; const [a,m,j]=String(d).slice(0,10).split('-'); return j?`${m}/${j}/${a.slice(2)}`:d; };

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
  dessine(); rcDessine();
})();
'''

html = coquille("Tableau de bord", "Tableau de bord",
  "Ce qui demande une décision aujourd'hui : les références qui s'épuisent, celles qui "
  "n'ont pas de photo, et les prix qui font perdre de l'argent. Les seuils viennent des réglages.",
  CSS, CORPS, JS.replace('/*__RECAP__*/', RECAP_JS), donnees=('produits','histgros')).replace('__IDX__', 'Object.fromEntries(D_TOUS().map(r=>[r[15],[r[0],r[13],r[2],r[12],r[6],r[8],r[7],r[14],r[4],r[5],r[9]]]))')
open('tableau.html','w').write(html)
print('tableau.html',len(html)//1024,'Ko')
