# -*- coding: utf-8 -*-
"""Le récap « Ventes par canal » en tête du tableau de bord.

1er nov. 2026 (Igal : « j'aimerais avoir un tableau récapitulatif du mois dernier avec un graphisme de tous les canaux
de vente par mois… un truc récapitulatif où Sam pourra sélectionner son mois, la période, l'année »).

Ce que ça fait :
  - une barre de périodes (ce mois, mois dernier, 30 jours, 90 jours, cette année, tout) + un menu Mois + un menu Année ;
  - quatre chiffres (chiffre d'affaires, marge nette, flacons, ventes) comparés à la période d'avant ;
  - un tableau canal par canal, avec la part de chacun, et pour Perfume City la part boutique / en ligne ;
  - un graphique en colonnes empilées (par jour sur une période courte, par mois sinon), bascule chiffre d'affaires /
    marge / flacons, infobulle au survol, et les mêmes chiffres dans un tableau dépliable.

Les chiffres sont CEUX DE LA PAGE VENTES : mêmes règles de marge (commission du canal, port encaissé moins coût de
l'envoi sur Amazon et les sites, frais de carte Lightspeed, remboursements en négatif, prix d'achat figé avant la mise
en service). Un test (_test_recap.py) compare canal par canal avec ventes.html. Les commandes reçues mais pas encore
expédiées ne comptent pas : elles ne sont pas des ventes faites.

Pas de camembert : des colonnes et un tableau se comparent mieux que des parts de cercle.
"""

RECAP_CSS = r'''
/* ---- le récap « Ventes par canal » (1er nov. 2026) ---- */
.rc{margin:0 0 30px}
.rc h2.sec{margin-top:0}
.rc-bar{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:0 0 14px}
.rc-chip{font-family:inherit;font-size:13px;font-weight:600;color:var(--ink-2);background:var(--surface);border:1px solid var(--line);
  border-radius:999px;padding:6px 13px;cursor:pointer;line-height:1.2}
.rc-chip:hover{border-color:var(--iris);color:var(--iris)}
.rc-chip.on{background:var(--iris);border-color:var(--iris);color:#fff}
.rc-bar label{font-size:12.5px;color:var(--ink-3);margin-left:6px}
.rc-bar select{font-family:inherit;font-size:13px;color:var(--ink);background:var(--surface);border:1px solid var(--line);border-radius:8px;padding:6px 8px}
.rc-bar select.on{border-color:var(--iris);color:var(--iris);font-weight:600}
.rc .kpis{margin-bottom:18px}
.rc .kpi .e{font-size:12.5px;font-weight:600;margin-top:4px}
.rc .kpi .e.up{color:var(--good)} .rc .kpi .e.dn{color:var(--crit)} .rc .kpi .e.eq{color:var(--ink-3)}
.rc-grid{display:grid;grid-template-columns:minmax(340px,1fr) minmax(340px,1fr);gap:18px;align-items:start}
@media(max-width:900px){.rc-grid{grid-template-columns:1fr}}
.rc-card{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:16px 18px;box-shadow:0 1px 2px rgba(0,0,0,.04);overflow-x:auto;min-width:0}
.rc-card h3{margin:0 0 10px;font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:var(--ink);font-weight:700}
.rc-tab{width:100%;border-collapse:collapse;font-size:13.5px}
.rc-tab th{font-size:10.5px;letter-spacing:.08em;text-transform:uppercase;color:var(--ink-3);font-weight:700;text-align:left;padding:4px 6px 8px;border-bottom:1px solid var(--line)}
.rc-tab td{padding:9px 6px;border-bottom:1px solid var(--line-2);vertical-align:middle}
.rc-tab .r{text-align:right;font-variant-numeric:tabular-nums}
.rc-tab tr.tot td{border-bottom:0;font-weight:700;padding-top:12px}
.rc-tab .nm{font-weight:600;display:flex;align-items:center;gap:8px}
.rc-tab .nm small{display:block;font-weight:400;color:var(--ink-3);font-size:12px;line-height:1.35}
.rc-sw{display:inline-block;width:10px;height:10px;border-radius:3px;background:var(--c);flex:none}
.rc-part{display:flex;align-items:center;gap:6px;justify-content:flex-end;margin-top:3px}
.rc-part i{display:inline-block;height:5px;border-radius:3px;background:var(--c);width:calc(var(--w)*1px);min-width:2px;max-width:60px}
.rc-part b{font-weight:500;font-size:11.5px;font-variant-numeric:tabular-nums;color:var(--ink-3);white-space:nowrap}
.rc-tab td.r{white-space:nowrap}
.rc .neg{color:var(--crit)}
.rc-met{display:flex;gap:6px;margin:0 0 10px;flex-wrap:wrap}
.rc-met .rc-chip{font-size:12.5px;padding:5px 11px}
.rc-pw{display:grid;grid-template-columns:auto 1fr;gap:0 6px}
.rc-y{display:flex;flex-direction:column;justify-content:space-between;font-size:11px;color:var(--ink-3);text-align:right;font-variant-numeric:tabular-nums;height:230px}
.rc-plot{position:relative;height:230px;border-left:0;border-bottom:1px solid var(--line)}
.rc-gl{position:absolute;left:0;right:0;border-top:1px solid var(--line-2);height:0}
.rc-gl.zero{border-top:1px solid var(--ink-3)}
.rc-cols{position:absolute;inset:0;display:flex;align-items:stretch}
.rc-col{flex:1 1 0;position:relative;min-width:0;cursor:default;outline:none}
.rc-col:hover .rc-b,.rc-col:focus .rc-b{filter:brightness(.9)}
.rc-b{position:absolute;left:50%;transform:translateX(-50%);width:62%;max-width:44px;top:0;bottom:0}
.rc-s{position:absolute;left:0;right:0;background:var(--c);border-top:2px solid var(--surface)}
.rc-s.top{border-radius:4px 4px 0 0}
.rc-s.neg{border-top:0;border-bottom:2px solid var(--surface);border-radius:0 0 4px 4px}
.rc-x{display:grid;grid-column:2;font-size:11px;color:var(--ink-3);margin-top:6px}
.rc-x span{text-align:center;overflow:hidden;white-space:nowrap}
.rc-x i{font-style:normal;font-variant-numeric:tabular-nums}
.rc-gl{border-top-style:solid;border-top-color:var(--line-2);opacity:.9}
.rc-leg{display:flex;flex-wrap:wrap;gap:6px 14px;margin:12px 0 0;font-size:12.5px;color:var(--ink-2)}
.rc-leg span{display:inline-flex;align-items:center;gap:6px}
.rc-tip{position:fixed;z-index:50;pointer-events:none;background:var(--ink);color:var(--surface);font-size:12.5px;line-height:1.5;padding:8px 11px;border-radius:8px;box-shadow:0 6px 18px rgba(0,0,0,.18);max-width:260px;display:none}
.rc-tip .t{display:block;font-weight:700;margin-bottom:3px}
.rc-tip div{display:flex;justify-content:space-between;gap:14px}
.rc-tip .tot{border-top:1px solid rgba(255,255,255,.25);margin-top:4px;padding-top:4px;font-weight:700}
.rc-tip .rc-sw{width:8px;height:8px;margin-right:5px}
.rc details{margin-top:12px}
.rc .rc-card details summary{cursor:pointer;color:var(--iris);font-weight:600;font-size:13px;list-style-position:inside}
.rc details table{margin-top:8px}
.rc-note{font-size:12.5px;color:var(--ink-3);margin:14px 0 0;line-height:1.5;max-width:90ch}
.rc .kpis+.rc-inc{margin:-8px 0 18px}
.rc-vide{background:var(--surface);border:1px dashed var(--line);border-radius:12px;padding:22px;color:var(--ink-2);font-size:14px;line-height:1.6}
:root{--rc-c-site:#0072B2;--rc-c-sitegros:#7B52AB;--rc-c-amazon:#009E73;--rc-c-gros:#E69F00;--rc-c-caisse:#D55E00;--rc-c-pc:#E0457F;--rc-c-detail:#5C6B7A;--rc-c-autre:#8C8C8C}
@media(prefers-color-scheme:dark){:root:not([data-theme="light"]){--rc-c-site:#4DA3E0;--rc-c-sitegros:#A98BD8;--rc-c-amazon:#2EC49B;--rc-c-gros:#F2B641;--rc-c-caisse:#F08A4B;--rc-c-pc:#F06A9C;--rc-c-detail:#9AA7B5;--rc-c-autre:#A6A6A6}}
:root[data-theme="dark"]{--rc-c-site:#4DA3E0;--rc-c-sitegros:#A98BD8;--rc-c-amazon:#2EC49B;--rc-c-gros:#F2B641;--rc-c-caisse:#F08A4B;--rc-c-pc:#F06A9C;--rc-c-detail:#9AA7B5;--rc-c-autre:#A6A6A6}
'''

RECAP_JS = r'''
/* ============ LE RÉCAP « VENTES PAR CANAL » (1er nov. 2026) ============
   Les règles de calcul sont celles de ventes.html (construitV) — recopiées ici parce que les deux pages sont
   fabriquées à part ; _test_recap.py vérifie qu'elles donnent les mêmes chiffres canal par canal. */
const RC_K='tableau-recap-v1';
const RC={sel:'moisdernier',metric:'ca'};
try{ const r=lit(RC_K,null); if(r&&typeof r==='object'){ if(r.sel) RC.sel=r.sel; if(r.metric) RC.metric=r.metric; } }catch(e){}
function rcSauve(){ try{ ecrit(RC_K,{sel:RC.sel,metric:RC.metric}); }catch(e){} }
/* ---- les canaux, comme dans Ventes ---- */
const RC_CANAUX_DEF=[{id:'site',nom:'Site perfumestrade.com',com:3},{id:'sitegros',nom:'Site wholesale.perfumestrade.com',com:3},
  {id:'amazon',nom:'Amazon',com:15},{id:'perfumecity',nom:'Perfume City',com:3}];
function rcCanauxReg(){ let L=(REG.canaux&&REG.canaux.length?REG.canaux:RC_CANAUX_DEF);
  if((REG.canauxV||0)<2){ L=L.filter(c=>c.id!=='shopify'); if(!L.some(c=>c.id==='sitegros')){ const i=L.findIndex(c=>c.id==='site'); L=L.slice(); L.splice(i>=0?i+1:L.length,0,RC_CANAUX_DEF[1]); } }
  if((REG.canauxV||0)<3) L=L.filter(c=>c.id!=='boutique');
  if(!REG.pcCom3) L=L.map(c=>(c.id==='perfumecity'&&!(+c.com))?Object.assign({},c,{com:3}):c);
  /* 7 nov. 2026 (Igal) : les commissions réelles — sites WooCommerce 2,9 % + 0,30 $ par transaction ; Perfume City boutique 2,5 % + 0,10 $,
     en ligne 2,7 % + 0,30 $ (et 8 $ d'envoi). Valables depuis le début de l'ERP : lues ici tant que Réglages ne les a pas écrites (comV4). */
  if(!REG.comV4) L=L.map(RC_COM_V4);
  return L; }
const RC_COM_V4=(c=>{ if(!c) return c; if(c.id==='site'||c.id==='sitegros') return Object.assign({},c,{com:2.9,fixe:0.3}); if(c.id==='perfumecity') return Object.assign({},c,{com:2.5,fixe:0.1,comLigne:2.7,fixeLigne:0.3}); return c; });
/* la part FIXE par transaction (0,30 $, 0,10 $…), retirée une fois par commande et répartie entre ses lignes */
function rcFixeDe(v){ const c=rcCanauxReg().find(x=>String(x.nom).toLowerCase()===String(v.canal||'').toLowerCase()); if(!c) return 0;
  const f=rcPcEnLigne(v)?(c.fixeLigne!=null&&c.fixeLigne!==''?c.fixeLigne:c.fixe):c.fixe; return (f==null||f===''||isNaN(+f))?0:Math.max(0,+f); }
function rcCom(nom){
  const n=String(nom||'').toLowerCase(); if(!n||n==='(non précisé)') return 0;
  const c=rcCanauxReg().find(x=>String(x.nom).toLowerCase()===n); if(c) return +c.com||0;
  if(n.includes('lightspeed')||n.includes('caisse')||n==='boutique') return 0;
  return 0;
}
/* 7 nov. 2026 (Igal : « Perfume City a deux types de vente sur Shopify, boutique et en ligne ») : la vente EN LIGNE de Perfume
   City a sa propre commission (Réglages, ligne « Perfume City — en ligne », comLigne) et un coût d'envoi par commande
   (REG.envois['shopify-pc'], 0 tant que rien n'est réglé) ; la vente en boutique garde la commission du canal, sans envoi. */
const rcPcCanal=()=>rcCanauxReg().find(c=>c.id==='perfumecity');
const rcPcEnLigne=v=>!!(v&&String(v.auto||'')==='shopify-pc'&&v.ou==='en ligne');
function rcComDe(v){ if(rcPcEnLigne(v)){ const c=rcPcCanal(); if(c&&c.comLigne!=null&&c.comLigne!==''&&!isNaN(+c.comLigne)) return Math.max(0,+c.comLigne); } return rcCom(v.canal); }
const rcEnvoiPc=()=>{ const E=(REG&&REG.envois)||{}; const v=E['shopify-pc']; return (v==null||v===''||isNaN(+v))?(REG.comV4?0:8):Math.max(0,+v); };
const rcPaAct=cle=>{ const m=MOD[cle]; if(m&&m.pa!=null) return +m.pa; const v=(IDX[cle]||[])[3]; return v==null?null:+v; };
const rcCarteTaux=()=>{ const v=REG&&REG.carteLS; return (v==null||v===''||isNaN(+v))?2.6:Math.max(0,+v); };
const rcEnvoi=src=>{ const E=(REG&&REG.envois)||{}; const v=E[src]; return (v==null||v===''||isNaN(+v))?8:Math.max(0,+v); };
let _rcPaie=null, _rcOrig=null;
function rcPaie(f){ if(f&&f.paie&&typeof f.paie==='object') return f.paie; if(!f||!f._i) return null;
  if(!_rcPaie){ try{ _rcPaie=lit('caisse-paie-v1',{})||{}; }catch(e){ _rcPaie={}; } }
  const p=_rcPaie[String(f._i).replace(/^fa\|/,'')]; return (p&&typeof p==='object')?p:null; }
function rcOrigineFn(F){ let O={}; try{ O=lit('pc-origine-v1',{})||{}; }catch(e){}
  const parNum={}; F.forEach(g=>{ if(g&&g.auto==='shopify-pc'&&!g.retour){ const o=O[String(g._i||'').replace(/^fa\|/,'')]; if(o) parNum[g.num]=o; } });
  return f=>{ if(!f||f.auto!=='shopify-pc') return ''; const k=String(f._i||'').replace(/^fa\|/,''); return O[k]||parNum[f.num]||''; }; }
/* une ligne par parfum vendu (ou par commande quand l'export en porte le détail), avec sa marge nette */
function rcLignes(){
  _rcPaie=null;
  let F=[]; try{ F=lit(KFACT,[])||[]; }catch(e){ F=FACT; } if(!Array.isArray(F)) F=[];
  const orig=rcOrigineFn(F), L=[];
  const fige=String((REG&&REG.paFigeDepuis)||'2026-10-01');
  F.filter(f=>f&&f.sens==='vente').forEach(f=>{
    const canal=f.canal||'(non précisé)';
    (f.lignes||[]).forEach(l=>{
      const paV=(l.cle&&String(f.d||'')<fige&&rcPaAct(l.cle)!=null)?rcPaAct(l.cle):l.paAv;
      const base={canal,num:f.num,cle:l.cle,pa:paV,fid:f.id,ret:!!f.retour,auto:f.auto||'',portF:f.port,paie:rcPaie(f),ou:orig(f)};
      if(l.cmds&&l.cmds.length) l.cmds.forEach(c=>L.push(Object.assign({},base,{d:c.d||f.d,cmd:c.cmd||'',q:c.q||0,p:c.p!=null?c.p:l.p})));
      else L.push(Object.assign({},base,{d:f.d,cmd:'',q:l.q||0,p:l.p}));
    });
  });
  L.forEach(v=>{ v.d=String(v.d||'').slice(0,10); v.mt=(v.q||0)*(v.p||0); v.com=rcComDe(v);
    v.comMt=v.ret?0:v.mt*v.com/100; v.net=v.mt-v.comMt;
    v.mg=(v.pa!=null&&v.p!=null)?(v.net-v.pa*(v.q||0)):null; });
  /* 7 nov. 2026 (Igal : « en quoi il perd de l'argent ? » — un parfum vendu 38,50 $, acheté 29 $, donné « à perte » parce que les
     16,45 $ de frais de carte d'un panier de 616 $ étaient posés sur lui seul). Les frais d'une COMMANDE (port payé par le client,
     8 $ d'envoi, frais de carte de la caisse) sont maintenant répartis entre ses lignes, au prorata du montant de chacune :
     les totaux par canal ne bougent pas, et plus aucun parfum ne porte les frais des autres. */
  rcRepartit(L, v=>{ const src=String(v.auto||''); if(!/^(amazon|woocommerce|woocommerce-gros)$/.test(src)||v.ret) return null; return (v.fid?'f|'+v.fid+'|'+(v.cmd||''):'a|'+src+'|'+v.num); },
    v=>{ const src=String(v.auto||''); let port=v.portF; if(port==null&&/^woocommerce/.test(src)&&typeof faStatutSite==='function'){ const st=faStatutSite(src,v.num); if(st&&+st.port>0) port=+st.port; }
      return {portMt:+port>0?+port:0, envoiMt:rcEnvoi(src)}; },
    (v,x)=>{ v.portMt=x.portMt; v.envoiMt=x.envoiMt; if(v.mg!=null) v.mg+=x.portMt-x.envoiMt; });
  /* la part fixe de la commission, une fois par transaction (commande), répartie entre ses lignes ; comptée dans la commission */
  rcRepartit(L, v=>(!v.ret&&rcFixeDe(v)>0)?(v.fid?'f|'+v.fid+'|'+(v.cmd||''):'a|'+String(v.auto||'')+'|'+v.num):null,
    v=>({fixeMt:rcFixeDe(v)}),
    (v,x)=>{ v.fixeMt=x.fixeMt; v.comMt=Math.round((v.comMt+x.fixeMt)*100)/100; v.net=v.mt-v.comMt; if(v.mg!=null) v.mg-=x.fixeMt; });
  rcRepartit(L, v=>(rcPcEnLigne(v)&&!v.ret&&rcEnvoiPc()>0)?'f|'+(v.fid||v.num):null,
    v=>({portMt:0, envoiMt:rcEnvoiPc()}),
    (v,x)=>{ v.portMt=x.portMt; v.envoiMt=x.envoiMt; if(v.mg!=null) v.mg+=x.portMt-x.envoiMt; });
  rcRepartit(L, v=>(String(v.auto||'')!=='lightspeed'||v.ret||!v.paie||!(+v.paie.carte>0))?null:'f|'+(v.fid||v.num),
    v=>({carteMt:Math.round(+v.paie.carte*rcCarteTaux())/100}),
    (v,x)=>{ v.carteMt=x.carteMt; if(v.mg!=null) v.mg-=x.carteMt; });
  /* 2 nov. 2026 : les ventes en gros d'AVANT l'ERP (tableur de Sam jusqu'au 30 sept. 2026, donnees/histgros.js) comptent
     comme dans la fiche parfum : chiffre d'affaires et flacons, sans marge (le prix d'achat de l'époque est inconnu).
     Elles ne sont pas dans Ventes : le test de parité avec Ventes les laisse de côté (hist). */
  try{ const H=window.D_HG; if(H&&H.l){ Object.keys(H.l).forEach(k=>{ (H.l[k]||[]).forEach(r=>{ if(!r||!r[0]) return;
      const q=+r[2]||0, p=r[3]==null?0:+r[3]; L.push({canal:RC_HG,num:'',cle:null,pa:null,fid:'hg|'+r[0]+'|'+(r[1]||0),ret:false,auto:'',d:String(r[0]).slice(0,10),cmd:'',q,p,mt:q*p,com:0,comMt:0,net:q*p,mg:null,hist:true,client:(H.c||[])[r[1]]||''}); }); }); } }catch(e){}
  return L;
}
/* répartit les frais d'une commande entre ses lignes, au prorata du montant (les lignes sans prix d'achat n'en portent pas,
   sauf s'il n'y en a aucune autre) ; le dernier centime va à la dernière ligne pour que la somme tombe juste */
function rcRepartit(L,cleDe,calc,pose){
  const G=new Map(); L.forEach(v=>{ const k=cleDe(v); if(!k) return; if(!G.has(k)) G.set(k,[]); G.get(k).push(v); });
  G.forEach(gr=>{ const tot=calc(gr[0]); if(!tot) return;
    const avec=gr.filter(v=>v.mg!=null), cible=avec.length?avec:[gr[0]];
    const somme=cible.reduce((a,v)=>a+Math.max(0,v.mt||0),0);
    const parts=cible.map((v,i)=>{ const r=somme>0?Math.max(0,v.mt||0)/somme:1/cible.length; const x={}; Object.keys(tot).forEach(k=>{ x[k]=Math.round(tot[k]*r*100)/100; }); return x; });
    Object.keys(tot).forEach(k=>{ const d=Math.round((tot[k]-parts.reduce((a,x)=>a+x[k],0))*100)/100; parts[parts.length-1][k]=Math.round((parts[parts.length-1][k]+d)*100)/100; });
    cible.forEach((v,i)=>pose(v,parts[i])); });
}
const RC_HG="Vente en gros · avant l'ERP";
/* le premier jour dont les chiffres sont complets sur tous les canaux (mise en service de l'ERP, Amazon compris) */
const RC_COMPLET='2026-10-01';
/* ---- les périodes ---- */
const rcISO=d=>isoJour(d);
function rcPlage(sel){
  const auj=new Date(); const y=auj.getFullYear(), m=auj.getMonth();
  const deb=(Y,M)=>new Date(Y,M,1), fin=(Y,M)=>new Date(Y,M+1,0);
  let s=String(sel||'moisdernier'), mm;
  if(s==='cemois') return {a:rcISO(deb(y,m)),b:rcISO(auj),cour:true};
  if(s==='moisdernier') return {a:rcISO(deb(y,m-1)),b:rcISO(fin(y,m-1))};
  if(s==='cetteannee') return {a:rcISO(deb(y,0)),b:rcISO(auj),cour:true,an:true};
  if(s==='tout') return {a:'0000-01-01',b:'9999-12-31',tout:true};
  if((mm=s.match(/^rel:(\d+)$/))){ const d=new Date(auj); d.setDate(d.getDate()-(+mm[1]-1)); return {a:rcISO(d),b:rcISO(auj),rel:+mm[1]}; }
  if((mm=s.match(/^mois:(\d{4})-(\d{2})$/))){ const Y=+mm[1],M=+mm[2]-1; const c=(Y===y&&M===m); return {a:rcISO(deb(Y,M)),b:c?rcISO(auj):rcISO(fin(Y,M)),cour:c}; }
  if((mm=s.match(/^annee:(\d{4})$/))){ const Y=+mm[1]; const c=(Y===y); return {a:rcISO(deb(Y,0)),b:c?rcISO(auj):rcISO(fin(Y,11)),cour:c,an:true}; }
  return rcPlage('moisdernier');
}
/* la période d'avant, de même longueur : le mois précédent, les N jours d'avant, l'année d'avant (sur le même nombre de jours écoulés) */
function rcPrec(sel,P){
  const s=String(sel||''); let mm;
  const j=x=>{ const [Y,M,D]=x.split('-').map(Number); return new Date(Y,M-1,D); };
  if(P.tout) return null;
  if(s==='cemois'||(mm=s.match(/^mois:(\d{4})-(\d{2})$/))){ const a=j(P.a); const d0=new Date(a.getFullYear(),a.getMonth()-1,1);
    if(P.cour){ const n=Math.round((j(P.b)-a)/86400e3); const d1=new Date(d0); d1.setDate(d1.getDate()+n); const f=new Date(a.getFullYear(),a.getMonth(),0); return {a:rcISO(d0),b:rcISO(d1<f?d1:f)}; }
    return {a:rcISO(d0),b:rcISO(new Date(a.getFullYear(),a.getMonth(),0))}; }
  if(s==='moisdernier'){ const a=j(P.a); return {a:rcISO(new Date(a.getFullYear(),a.getMonth()-1,1)),b:rcISO(new Date(a.getFullYear(),a.getMonth(),0))}; }
  if(s==='cetteannee'||(mm=s.match(/^annee:(\d{4})$/))){ const a=j(P.a), b=j(P.b); return {a:rcISO(new Date(a.getFullYear()-1,0,1)),b:rcISO(new Date(b.getFullYear()-1,b.getMonth(),b.getDate()))}; }
  if(P.rel){ const a=j(P.a); const b1=new Date(a); b1.setDate(b1.getDate()-1); const a1=new Date(b1); a1.setDate(a1.getDate()-(P.rel-1)); return {a:rcISO(a1),b:rcISO(b1)}; }
  return null;
}
const RC_LOC=()=>LANG==='en'?'en-US':LANG==='es'?'es-ES':'fr-FR';
const rcMoisLib=(Y,M)=>new Date(Y,M,1).toLocaleDateString(RC_LOC(),{month:'long',year:'numeric'});   /* « octobre 2026 », « October 2026 », « octubre de 2026 » */
function rcLib(sel,P){
  const s=String(sel||''); let mm;
  if(s==='cemois') return L3('Ce mois','This month','Este mes')+' · '+rcMoisLib(+P.a.slice(0,4),+P.a.slice(5,7)-1);
  if(s==='moisdernier') return L3('Mois dernier','Last month','Mes pasado')+' · '+rcMoisLib(+P.a.slice(0,4),+P.a.slice(5,7)-1);
  if(s==='cetteannee') return L3('Cette année','This year','Este año')+' · '+P.a.slice(0,4);
  if(s==='tout') return L3('Depuis le début','Since the beginning','Desde el principio');
  if((mm=s.match(/^rel:(\d+)$/))) return L3(`${mm[1]} derniers jours`,`Last ${mm[1]} days`,`Últimos ${mm[1]} días`);
  if((mm=s.match(/^mois:(\d{4})-(\d{2})$/))) return rcMoisLib(+mm[1],+mm[2]-1);
  if((mm=s.match(/^annee:(\d{4})$/))) return L3('Année','Year','Año')+' '+mm[1];
  return '';
}
function rcLibPrec(sel,Q){ const s=String(sel||''); if(!Q) return '';
  if(/^(cemois|moisdernier|mois:)/.test(s)) return rcMoisLib(+Q.a.slice(0,4),+Q.a.slice(5,7)-1);
  if(/^(cetteannee|annee:)/.test(s)) return Q.a.slice(0,4);
  return L3('la période d\'avant','the previous period','el período anterior'); }
/* ---- l'identité d'un canal : une couleur fixe, un nom à l'écran ---- */
function rcId(nom){ const n=String(nom||'').toLowerCase();
  if(/perfume\s*(in\s*the\s*)?city/.test(n)) return 'pc';
  if(n.includes('wholesale')) return 'sitegros';
  if(n.includes('perfumestrade')) return 'site';
  if(n.includes('amazon')) return 'amazon';
  if(n.includes('lightspeed')||n.includes('caisse')) return 'caisse';
  if(n==='gros'||n===RC_HG.toLowerCase()) return 'gros'; if(n==='boutique') return 'detail';
  return 'autre'; }
const rcCoul=n=>`var(--rc-c-${rcId(n)})`;
function rcNomVu(nom){ const n=String(nom||'').toLowerCase();
  if(n==='gros') return L3('Vente en gros','Wholesale sale','Venta mayorista');
  if(n===RC_HG.toLowerCase()) return L3("Vente en gros · avant l'ERP",'Wholesale · before the ERP','Mayorista · antes del ERP');
  if(n==='boutique') return L3('Vente au détail','Retail sale','Venta al detalle');
  if(n==='caisse lightspeed') return L3('Caisse Lightspeed','Lightspeed register','Caja Lightspeed');
  if(n==='(non précisé)') return L3('(non précisé)','(not specified)','(sin precisar)');
  return nom; }
const rcOuLib=o=>o==='boutique'?L3('en boutique','in store','en tienda'):o==='en ligne'?L3('en ligne','online','en línea'):L3('autre','other','otro');
/* ---- l'agrégat d'une période : total, par canal, et pour Perfume City par origine ---- */
function rcAgrege(L,a,b){
  const S=L.filter(v=>v.d>=a&&v.d<=b);
  const G={}, T={ca:0,mg:0,q:0,n:0,nR:0,sansPa:0}; const ventes=new Set(), remb=new Set();
  S.forEach(v=>{ const o=G[v.canal]=G[v.canal]||{canal:v.canal,ca:0,mg:0,q:0,n:0,nR:0,sansPa:0,ou:{},vs:new Set(),rs:new Set()};
    o.ca+=v.mt; T.ca+=v.mt; o.q+=v.q||0; T.q+=v.q||0;
    if(v.mg==null){ if(!v.ret&&!v.hist){ o.sansPa++; T.sansPa++; } if(v.hist){ o.hist=1; } } else { o.mg+=v.mg; T.mg+=v.mg; }
    const k=(v.fid||v.num||'')+'|'+(v.cmd||''); if(v.ret){ o.rs.add(k); remb.add(k); } else { o.vs.add(k); ventes.add(k); }
    if(rcId(v.canal)==='pc'){ const ou=v.ou||''; const z=o.ou[ou]=o.ou[ou]||{ca:0,q:0}; z.ca+=v.mt; z.q+=v.q||0; } });
  Object.values(G).forEach(o=>{ o.n=o.vs.size; o.nR=o.rs.size; delete o.vs; delete o.rs; });
  T.n=ventes.size; T.nR=remb.size;
  return {S,G,T};
}
/* ---- le graphique : une colonne par jour (période ≤ 92 jours) ou par mois ---- */
function rcBuckets(P,S){
  const j=x=>{ const [Y,M,D]=x.split('-').map(Number); return new Date(Y,M-1,D); };
  let a=P.a, b=P.b;
  if(P.tout){ const ds=S.map(v=>v.d).filter(Boolean).sort(); if(!ds.length) return {K:[],jour:false}; a=ds[0]; b=ds[ds.length-1]; }
  /* un mois en cours occupe tout le mois (les jours à venir restent vides), une année en cours ses douze mois :
     deux jours de ventes ne font pas deux colonnes géantes, et le dessin garde la même forme d'un mois à l'autre */
  if(P.cour&&P.an) b=rcISO(new Date(+a.slice(0,4),11,31));
  else if(P.cour) b=rcISO(new Date(+a.slice(0,4),+a.slice(5,7),0));
  const A=j(a), B=j(b); const nJ=Math.round((B-A)/86400e3)+1;
  const K=[];
  if(nJ<=92&&!P.tout&&!P.an){ for(let d=new Date(A);d<=B;d.setDate(d.getDate()+1)){ const k=rcISO(d);
      K.push({k,lib:d.toLocaleDateString(RC_LOC(),{weekday:'short',day:'numeric',month:'short'}),court:String(d.getDate())}); }
    return {K,jour:true}; }
  for(let d=new Date(A.getFullYear(),A.getMonth(),1);d<=B;d.setMonth(d.getMonth()+1)){ const k=rcISO(d).slice(0,7);
    K.push({k,lib:rcMoisLib(d.getFullYear(),d.getMonth()),court:d.toLocaleDateString(RC_LOC(),{month:'short'})+(d.getMonth()===0||K.length===0?' '+String(d.getFullYear()).slice(2):'')}); }
  return {K,jour:false};
}
function rcNice(x){ if(x<=0) return 1; const p=Math.pow(10,Math.floor(Math.log10(x))); const r=x/p; const n=r<=1?1:r<=2?2:r<=2.5?2.5:r<=5?5:10; return n*p; }
const rcFmt=(metric,v)=>metric==='q'?nf(Math.round(v)):money(v);
const rcMetLib=m=>m==='mg'?L3('Marge nette','Net margin','Margen neto'):m==='q'?L3('Flacons','Bottles','Frascos'):L3("Chiffre d'affaires",'Revenue','Facturación');
function rcChart(P,R,ordre,metric){
  const B=rcBuckets(P,R.S); if(!B.K.length) return '';
  const idx={}; B.K.forEach((k,i)=>idx[k.k]=i);
  const cel=B.K.map(()=>({}));
  R.S.forEach(v=>{ const k=B.jour?v.d:v.d.slice(0,7); const i=idx[k]; if(i==null) return;
    const val=metric==='mg'?(v.mg||0):metric==='q'?(v.q||0):v.mt; cel[i][v.canal]=(cel[i][v.canal]||0)+val; });
  let hi=0, lo=0;
  cel.forEach(c=>{ let up=0, dn=0; Object.values(c).forEach(x=>{ if(x>0) up+=x; else dn+=x; }); hi=Math.max(hi,up); lo=Math.min(lo,dn); });
  const pas=rcNice(Math.max(hi,-lo)/4); const top=Math.ceil(hi/pas)*pas||pas, bas=Math.floor(lo/pas)*pas; const tot=top-bas;
  const pc=v=>((v-bas)/tot*100);
  const ticks=[]; for(let t=bas;t<=top+1e-9;t+=pas) ticks.push(t);
  const yl=ticks.slice().reverse().map(t=>`<span>${rcFmt(metric,t)}</span>`).join('');
  const gl=ticks.map(t=>`<i class="rc-gl ${t===0?'zero':''}" style="bottom:${pc(t)}%"></i>`).join('');
  const cols=B.K.map((k,i)=>{ const c=cel[i]; let up=0, dn=0, segs='';
    const arr=ordre.filter(n=>(c[n]||0)!==0), dernierPos=arr.filter(n=>c[n]>0).pop();
    arr.forEach(n=>{ const v=c[n]; const h=Math.abs(v)/tot*100;
      if(v>0){ segs+=`<i class="rc-s ${n===dernierPos?'top':''}" style="--c:${rcCoul(n)};bottom:${pc(0)+up}%;height:${h}%"></i>`; up+=h; }
      else { dn+=h; segs+=`<i class="rc-s neg" style="--c:${rcCoul(n)};bottom:${pc(0)-dn}%;height:${h}%"></i>`; } });
    const tip=`<b class="t" data-nolang>${esc(k.lib)}</b>`+arr.map(n=>`<div><span><i class="rc-sw" style="--c:${rcCoul(n)}"></i><span data-nolang>${esc(rcNomVu(n))}</span></span><b>${rcFmt(metric,c[n])}</b></div>`).join('')
      +(arr.length>1?`<div class="tot"><span>${L3('Total','Total','Total')}</span><b>${rcFmt(metric,arr.reduce((a,n)=>a+c[n],0))}</b></div>`:'');
    const lab=k.lib+L3(' : ',': ',': ')+(arr.length?arr.map(n=>rcNomVu(n)+' '+rcFmt(metric,c[n])).join(', '):L3('rien','nothing','nada'));
    return `<div class="rc-col" tabindex="0" data-i="${i}" data-tip="${esc(tip)}" aria-label="${esc(lab)}"><div class="rc-b">${segs}</div></div>`; }).join('');
  const nX=B.K.length, pasX=B.jour?(nX<=16?1:nX<=31?2:nX<=62?4:7):(nX<=12?1:3);
  const xl=B.K.map((k,i)=>`<span>${i%pasX===0?`<i data-nolang>${esc(k.court)}</i>`:''}</span>`).join('');
  const leg=ordre.filter(n=>R.G[n]).map(n=>`<span><i class="rc-sw" style="--c:${rcCoul(n)}"></i><span data-nolang>${esc(rcNomVu(n))}</span></span>`).join('');
  const figs=`<details><summary>${L3('Voir les chiffres','See the figures','Ver las cifras')}, ${B.jour?L3('jour par jour','day by day','día a día'):L3('mois par mois','month by month','mes a mes')}</summary>
    <table class="rc-tab"><thead><tr><th>${B.jour?L3('Jour','Day','Día'):L3('Mois','Month','Mes')}</th>${ordre.filter(n=>R.G[n]).map(n=>`<th class="r" data-nolang>${esc(rcNomVu(n))}</th>`).join('')}<th class="r">${L3('Total','Total','Total')}</th></tr></thead>
    <tbody>${B.K.map((k,i)=>{ const c=cel[i]; const t=Object.values(c).reduce((a,x)=>a+x,0); if(!Object.keys(c).length) return '';
      return `<tr><td data-nolang>${esc(k.lib)}</td>${ordre.filter(n=>R.G[n]).map(n=>`<td class="r ${c[n]<0?'neg':''}">${c[n]?rcFmt(metric,c[n]):'·'}</td>`).join('')}<td class="r ${t<0?'neg':''}"><b>${rcFmt(metric,t)}</b></td></tr>`; }).join('')}</tbody></table></details>`;
  return `<div class="rc-pw"><div class="rc-y">${yl}</div><div class="rc-plot">${gl}<div class="rc-cols">${cols}</div></div><div class="rc-x" style="grid-template-columns:repeat(${nX},1fr)">${xl}</div></div>
    <div class="rc-leg">${leg}</div>${figs}`;
}
/* ---- tout dessiner ---- */
function rcDessine(){
  const z=document.getElementById('recap'); if(!z) return;
  const L=rcLignes(), P=rcPlage(RC.sel), R=rcAgrege(L,P.a,P.b), Q0=rcPrec(RC.sel,P);
  /* 3 nov. 2026 (Igal) : pas de comparaison quand la période d'avant commence avant RC_COMPLET, parce que ses chiffres
     sont incomplets (septembre 2026 n'a pas les ventes Amazon FBA). Dès novembre, octobre sert de référence et la
     comparaison revient toute seule. Si l'export Amazon de septembre est importé un jour, reculer RC_COMPLET. */
  const Q=(Q0&&Q0.a<RC_COMPLET)?null:Q0, Qinc=(Q0&&!Q)?Q0:null, RP=Q?rcAgrege(L,Q.a,Q.b):null;
  const auj=new Date(); const y=auj.getFullYear(), m=auj.getMonth();
  /* les mois et les années qui ont des ventes, pour les deux menus */
  const moisVus=new Set(L.map(v=>v.d.slice(0,7)).filter(x=>/^\d{4}-\d{2}$/.test(x))); moisVus.add(rcISO(auj).slice(0,7));
  const mois=[...moisVus].sort().reverse(), annees=[...new Set(mois.map(x=>x.slice(0,4)))];
  const chips=[['cemois',L3('Ce mois','This month','Este mes')],['moisdernier',L3('Mois dernier','Last month','Mes pasado')],['rel:30',L3('30 jours','30 days','30 días')],['rel:90',L3('90 jours','90 days','90 días')],['cetteannee',L3('Cette année','This year','Este año')],['tout',L3('Tout','All','Todo')]];
  const selM=/^mois:/.test(RC.sel)?RC.sel:'', selA=/^annee:/.test(RC.sel)?RC.sel:'';
  let h=`<h2 class="sec">${L3('Ventes par canal','Sales by channel','Ventas por canal')} <em data-nolang>${esc(rcLib(RC.sel,P))}</em><a href="ventes.html">${L3('Journal des ventes','Sales log','Diario de ventas')}</a></h2>
    <div class="rc-bar">${chips.map(([v,l])=>`<button type="button" class="rc-chip ${RC.sel===v?'on':''}" data-rc="${v}">${l}</button>`).join('')}
      <label for="rc-mois">${L3('Mois','Month','Mes')}</label><select id="rc-mois" class="${selM?'on':''}"><option value="">—</option>${mois.map(x=>`<option value="mois:${x}" ${selM==='mois:'+x?'selected':''}>${esc(rcMoisLib(+x.slice(0,4),+x.slice(5,7)-1))}</option>`).join('')}</select>
      <label for="rc-an">${L3('Année','Year','Año')}</label><select id="rc-an" class="${selA?'on':''}"><option value="">—</option>${annees.map(x=>`<option value="annee:${x}" ${selA==='annee:'+x?'selected':''}>${x}</option>`).join('')}</select></div>`;
  if(!R.S.length){
    h+=`<div class="rc-vide">${L3('Aucune vente sur cette période.','No sale in this period.','Ninguna venta en este período.')} ${L.length?L3('Choisis une autre période ci-dessus.','Pick another period above.','Elige otro período arriba.'):L3('Dès qu\'une vente est saisie, importée d\'un canal ou facturée, elle apparaît ici.','As soon as a sale is entered, imported from a channel or invoiced, it shows up here.','En cuanto una venta se registra, se importa de un canal o se factura, aparece aquí.')}</div>`;
    z.innerHTML=h; rcBranche(); return;
  }
  const pct=(a,b)=>(b==null||Math.abs(b)<0.005)?null:(a-b)/Math.abs(b)*100;
  const evo=(a,b,fmt)=>{ if(!RP) return ''; const p=pct(a,b); const lib=rcLibPrec(RC.sel,Q); fmt=fmt||money;
    if(p==null) return `<span class="e eq">${L3('rien à comparer','nothing to compare','nada que comparar')} (${esc(lib)})</span>`;
    const s=p>0.5?'up':p<-0.5?'dn':'eq'; const fl=s==='up'?'▲':s==='dn'?'▼':'=';
    /* un pourcentage à cinq chiffres ne dit rien (« +19 511 % » quand le mois d'avant n'avait presque rien) : on donne le chiffre d'avant */
    if(Math.abs(p)>500) return `<span class="e ${s}">${fl} <span data-nolang>${esc(lib)}</span> : ${fmt(b)}</span>`;
    return `<span class="e ${s}">${fl} ${nf(Math.round(Math.abs(p)))} % vs <span data-nolang>${esc(lib)}</span></span>`; };
  const T=R.T, TP=RP?RP.T:null;
  const panier=T.n?T.ca/T.n:null, pctMg=T.ca>0?T.mg/T.ca*100:null;
  h+=`<div class="kpis">
    <div class="kpi"><div class="v ${T.ca<0?'neg':''}">${money(T.ca)}</div><div class="k">${L3('Chiffre d\'affaires, remboursements déduits','Revenue, refunds deducted','Facturación, reembolsos deducidos')}</div>${evo(T.ca,TP&&TP.ca)}</div>
    <div class="kpi"><div class="v ${T.mg<0?'neg':''}">${money(T.mg)}</div><div class="k">${L3('Marge nette','Net margin','Margen neto')}${pctMg!=null?' · '+nf(Math.round(pctMg*10)/10)+' %':''}${T.sansPa?' · <span class="neg">'+L3(`${T.sansPa} ligne${T.sansPa>1?'s':''} sans prix d'achat`,`${T.sansPa} line${T.sansPa>1?'s':''} without purchase price`,`${T.sansPa} línea${T.sansPa>1?'s':''} sin precio de compra`)+'</span>':''}</div>${evo(T.mg,TP&&TP.mg)}</div>
    <div class="kpi"><div class="v">${nf(T.q)}</div><div class="k">${L3('flacons vendus','bottles sold','frascos vendidos')}</div>${evo(T.q,TP&&TP.q,nf)}</div>
    <div class="kpi"><div class="v">${nf(T.n)}</div><div class="k">${L3('ventes','sales','ventas')}${panier!=null?' · '+L3('panier moyen','average basket','cesta media')+' '+money(panier):''}${T.nR?' · '+nf(T.nR)+' '+L3('remboursement'+(T.nR>1?'s':''),'refund'+(T.nR>1?'s':''),'reembolso'+(T.nR>1?'s':'')):''}</div>${evo(T.n,TP&&TP.n,nf)}</div>
  </div>`;
  if(Qinc){ const lib=rcLibPrec(RC.sel,Qinc);
    h+=`<p class="rc-note rc-inc">${L3('Pas de comparaison avec','No comparison with','Sin comparación con')} <span data-nolang>${esc(lib)}</span> : ${L3('les chiffres d\'avant le 1er octobre 2026 sont incomplets (ventes Amazon absentes). La comparaison reviendra d\'elle-même sur les mois suivants.','figures before October 1, 2026 are incomplete (Amazon sales missing). The comparison will come back by itself on the following months.','las cifras anteriores al 1 de octubre de 2026 están incompletas (faltan las ventas de Amazon). La comparación volverá sola en los meses siguientes.')}</p>`; }
  const ordre=Object.values(R.G).sort((a,b)=>b.ca-a.ca||b.q-a.q).map(o=>o.canal);
  const caPos=Object.values(R.G).reduce((a,o)=>a+Math.max(0,o.ca),0)||1;
  const sous=o=>{ if(rcId(o.canal)!=='pc') return ''; const ks=Object.keys(o.ou).filter(k=>k&&(o.ou[k].q||o.ou[k].ca)); if(!ks.length) return '';
    return `<small>${ks.sort().map(k=>rcOuLib(k)+' <b data-nolang>'+money(o.ou[k].ca)+'</b>').join(' · ')}</small>`; };
  h+=`<div class="rc-grid"><div class="rc-card"><h3>${L3('Par canal','By channel','Por canal')}</h3>
    <table class="rc-tab" id="rc-tab"><thead><tr><th>${L3('Canal','Channel','Canal')}</th><th class="r">${L3('Ventes','Sales','Ventas')}</th><th class="r">${L3('Flacons','Bottles','Frascos')}</th><th class="r">${L3("Chiffre d'affaires",'Revenue','Facturación')}</th><th class="r">${L3('Marge nette','Net margin','Margen neto')}</th></tr></thead><tbody>
    ${ordre.map(n=>{ const o=R.G[n]; const part=Math.max(0,o.ca)/caPos*100;
      return `<tr data-c="${esc(n)}"><td><div class="nm"><i class="rc-sw" style="--c:${rcCoul(n)}"></i><span data-nolang>${esc(rcNomVu(n))}</span></div>${sous(o)}</td><td class="r">${nf(o.n)}${o.nR?` <small class="neg">−${nf(o.nR)}</small>`:''}</td><td class="r">${nf(o.q)}</td><td class="r ${o.ca<0?'neg':''}"><b>${money(o.ca)}</b><span class="rc-part" title="${esc(L3('part du chiffre d\'affaires','share of revenue','parte de la facturación'))}"><i style="--c:${rcCoul(n)};--w:${Math.round(part*0.6)}"></i><b>${nf(Math.round(part))} %</b></span></td><td class="r ${o.mg<0?'neg':''}">${o.hist?'<span title="'+esc(L3("prix d'achat de l'époque inconnu : pas de marge",'purchase price at the time unknown: no margin','precio de compra de la época desconocido: sin margen'))+'">—</span>':money(o.mg)}${o.sansPa?' <small class="neg" title="'+esc(L3('lignes sans prix d\'achat','lines without purchase price','líneas sin precio de compra'))+'">?</small>':''}</td></tr>`; }).join('')}
    <tr class="tot"><td>${L3('Total','Total','Total')}</td><td class="r">${nf(T.n)}</td><td class="r">${nf(T.q)}</td><td class="r ${T.ca<0?'neg':''}">${money(T.ca)}</td><td class="r ${T.mg<0?'neg':''}">${money(T.mg)}</td></tr></tbody></table></div>
    <div class="rc-card"><h3>${L3('Au fil du temps','Over time','A lo largo del tiempo')}</h3>
      <div class="rc-met">${['ca','mg','q'].map(mt=>`<button type="button" class="rc-chip ${RC.metric===mt?'on':''}" data-rcm="${mt}">${rcMetLib(mt)}</button>`).join('')}</div>
      ${rcChart(P,R,ordre,RC.metric)}</div></div>
    <p class="rc-note">${L3('La marge est nette : commission du canal, port et frais de carte déduits, comme dans Ventes. Les commandes reçues mais pas encore expédiées ne comptent pas. Les ventes en gros d\'avant l\'ERP (tableur, jusqu\'au 30 sept. 2026) comptent dans le chiffre d\'affaires, sans marge.','The margin is net: channel commission, shipping and card fees deducted, as in Sales. Orders received but not yet shipped do not count. Wholesale sales from before the ERP (spreadsheet, until Sept 30, 2026) count in revenue, without margin.','El margen es neto: comisión del canal, envío y comisiones de tarjeta deducidos, como en Ventas. Los pedidos recibidos pero aún no enviados no cuentan. Las ventas mayoristas de antes del ERP (hoja de cálculo, hasta el 30 sept. 2026) cuentan en la facturación, sin margen.')}</p>`;
  z.innerHTML=h; rcBranche();
}
let _rcTip=null;
function rcBranche(){
  const z=document.getElementById('recap'); if(!z) return;
  z.querySelectorAll('[data-rc]').forEach(b=>b.onclick=()=>{ RC.sel=b.dataset.rc; rcSauve(); rcDessine(); });
  z.querySelectorAll('[data-rcm]').forEach(b=>b.onclick=()=>{ RC.metric=b.dataset.rcm; rcSauve(); rcDessine(); });
  const sm=document.getElementById('rc-mois'), sa=document.getElementById('rc-an');
  if(sm) sm.onchange=()=>{ if(sm.value){ RC.sel=sm.value; rcSauve(); rcDessine(); } };
  if(sa) sa.onchange=()=>{ if(sa.value){ RC.sel=sa.value; rcSauve(); rcDessine(); } };
  if(!_rcTip){ _rcTip=document.createElement('div'); _rcTip.className='rc-tip'; document.body.appendChild(_rcTip); }
  const montre=(el,ev)=>{ _rcTip.innerHTML=el.dataset.tip||''; _rcTip.style.display='block';
    const r=el.getBoundingClientRect(); let x=(ev&&ev.clientX!=null?ev.clientX:r.left+r.width/2)+12, yy=(ev&&ev.clientY!=null?ev.clientY:r.top)-10;
    const w=_rcTip.offsetWidth||220; if(x+w>window.innerWidth-8) x=x-w-24; if(yy<8) yy=8; _rcTip.style.left=x+'px'; _rcTip.style.top=yy+'px'; };
  const cache=()=>{ _rcTip.style.display='none'; };
  z.querySelectorAll('.rc-col').forEach(c=>{ c.onmouseenter=e=>montre(c,e); c.onmousemove=e=>montre(c,e); c.onmouseleave=cache; c.onfocus=()=>montre(c,null); c.onblur=cache; });
}
window.__recap={RC,rcLignes,rcPlage,rcPrec,rcAgrege,rcDessine};
'''
