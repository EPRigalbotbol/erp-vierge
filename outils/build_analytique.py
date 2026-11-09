# -*- coding: utf-8 -*-
"""ANALYTIQUE — la rubrique des admins, sous le Tableau de bord (9 nov. 2026).

Igal, 8 nov. 2026 : « qu'on crée une rubrique en dessous de dashboard… l'analytics de tous les sites référencés, tous les
canaux de vente… voir l'amélioration en direct » (le but premier : savoir si Google Shopping fait vendre), puis
« fais-moi un très beau truc », et « c'est vraiment une rubrique qu'on crée pour les admins » : en français et en
anglais seulement (en espagnol, la page est en anglais), et fermée au Commercial (mur « voirMarge », comme le Tableau de bord).

Ce que la page montre, sur la période choisie (7 jours, 30 jours, ce mois, mois dernier, 90 jours, cette année),
comparée à la période d'avant de même longueur :
  1. cinq chiffres : chiffre d'affaires de tous les canaux, marge nette, ventes des sites en ligne, commandes en ligne
     (panier moyen), part venue de Google — chacun avec sa courbe jour par jour ;
  2. D'OÙ VIENNENT LES COMMANDES DES SITES : Google Shopping, Google Ads, recherche Google, réseaux sociaux, email,
     venus directement, autres — en colonnes empilées jour par jour, et en classement ;
  3. les mêmes origines, site par site (perfumestrade.com, wholesale, Perfume City en ligne) ;
  4. tous les canaux de vente (sites, Amazon, caisse, gros, Perfume City), avec leur évolution ;
  5. les parfums qui se vendent en ligne, et la part de Google pour chacun.

Les chiffres de vente sont CEUX DU TABLEAU DE BORD ET DE LA PAGE VENTES : la page reprend le même calcul (_recap.py,
rcLignes / rcAgrege). L'origine d'une commande vient du cockpit (magasin « ventes-origine-v1 », origines.js), qui la
lit chez WooCommerce (attribution de commande) et chez Shopify (parcours client) — en lecture seule.
"""
import json
from build_crm import coquille
from _recap import RECAP_CSS, RECAP_JS

CSS = RECAP_CSS + r'''
.mur{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:34px 32px;max-width:640px;margin:26px auto}
.mur h2{margin:0 0 10px;font-size:20px;font-weight:700;letter-spacing:-.015em}
.mur p{margin:0;color:var(--ink-2);font-size:14.5px;line-height:1.65}
/* ---- la page Analytique (9 nov. 2026) ---- */
h2.sec{font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:var(--ink);font-weight:700;margin:30px 0 13px;padding-bottom:9px;border-bottom:1px solid var(--line);display:flex;justify-content:space-between;align-items:baseline;gap:12px;flex-wrap:wrap}
h2.sec em{font-style:normal;font-size:12.5px;letter-spacing:0;text-transform:none;color:var(--ink-3);font-weight:400;margin-right:auto}
h2.sec a{font-size:12px;letter-spacing:0;text-transform:none;color:var(--iris);font-weight:600;text-decoration:none} h2.sec a:hover{text-decoration:underline}
.an-kpi .v.neg,.an-note .neg,.neg{color:var(--crit)}
:root{--an-1:#2a78d6;--an-2:#eb6834;--an-3:#1baf7a;--an-4:#eda100;--an-5:#e87ba4;--an-6:#008300;--an-7:#6250d6;--an-0:#a3a29b}
@media(prefers-color-scheme:dark){:root:not([data-theme="light"]){--an-1:#3987e5;--an-2:#d95926;--an-3:#199e70;--an-4:#c98500;--an-5:#d55181;--an-6:#008300;--an-7:#9085e9;--an-0:#6e6d66}}
:root[data-theme="dark"]{--an-1:#3987e5;--an-2:#d95926;--an-3:#199e70;--an-4:#c98500;--an-5:#d55181;--an-6:#008300;--an-7:#9085e9;--an-0:#6e6d66}
.an-bar{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:4px 0 6px}
.an-per{font-size:13px;color:var(--ink-3);margin:0 0 18px}
.an-per b{color:var(--ink-2);font-weight:600}
.an-kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:12px;margin:0 0 22px}
.an-kpi{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:15px 16px 12px;display:flex;flex-direction:column;gap:4px;box-shadow:0 1px 2px rgba(0,0,0,.04);min-width:0}
.an-kpi .k{font-size:10.5px;letter-spacing:.11em;text-transform:uppercase;color:var(--ink-3);font-weight:700}
.an-kpi .v{font-size:27px;font-weight:700;letter-spacing:-.03em;line-height:1.1;color:var(--ink)}
.an-kpi .s{font-size:12.5px;color:var(--ink-3);line-height:1.4}
.an-kpi .e{font-size:12.5px;font-weight:600}
.an-kpi .e.up{color:var(--good)} .an-kpi .e.dn{color:var(--crit)} .an-kpi .e.eq{color:var(--ink-3)}
.an-kpi.g{border-top:3px solid var(--an-1)}
.an-sp{display:block;width:100%;height:36px;margin-top:6px;color:var(--iris);overflow:visible}
.an-sp path.l{fill:none;stroke:currentColor;stroke-width:2;stroke-linejoin:round;stroke-linecap:round}
.an-sp path.a{fill:currentColor;opacity:.10;stroke:none}
.an-sp circle{fill:currentColor;stroke:var(--surface);stroke-width:2}
.an-grid{display:grid;grid-template-columns:minmax(0,1.35fr) minmax(0,1fr);gap:18px;align-items:start;margin-bottom:18px}
@media(max-width:1000px){.an-grid{grid-template-columns:1fr}}
.an-card{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:16px 18px;box-shadow:0 1px 2px rgba(0,0,0,.04);min-width:0;overflow-x:auto}
.an-card h3{margin:0 0 4px;font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:var(--ink);font-weight:700}
.an-card .an-st{font-size:12.5px;color:var(--ink-3);margin:0 0 12px;line-height:1.45}
.an-sw{display:inline-block;width:10px;height:10px;border-radius:3px;background:var(--c);flex:none}
.an-rk{display:flex;flex-direction:column;gap:2px}
.an-r{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:2px 12px;padding:8px 2px;border-bottom:1px solid var(--line-2);align-items:center}
.an-r:last-child{border-bottom:0}
.an-r .n{display:flex;align-items:center;gap:8px;font-weight:600;font-size:13.5px;min-width:0}
.an-r .n span{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.an-r .m{text-align:right;font-size:13.5px;font-weight:700;white-space:nowrap;font-variant-numeric:tabular-nums}
.an-r .d{grid-column:1/-1;display:flex;align-items:center;gap:8px;font-size:12px;color:var(--ink-3)}
.an-r .d i{display:block;height:6px;border-radius:3px;background:var(--c);min-width:2px}
.an-r .d .t{margin-left:auto;white-space:nowrap}
.an-r .d .e.up{color:var(--good);font-weight:600}.an-r .d .e.dn{color:var(--crit);font-weight:600}
.an-r small.det{grid-column:1/-1;font-size:11.5px;color:var(--ink-3);line-height:1.4}
.an-tab{width:100%;border-collapse:collapse;font-size:13.5px}
.an-tab th{font-size:10.5px;letter-spacing:.08em;text-transform:uppercase;color:var(--ink-3);font-weight:700;text-align:left;padding:4px 8px 8px;border-bottom:1px solid var(--line);white-space:nowrap}
.an-tab td{padding:9px 8px;border-bottom:1px solid var(--line-2);vertical-align:middle}
.an-tab .r{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
.an-tab tr.tot td{border-bottom:0;font-weight:700;padding-top:12px}
.an-tab .nm{display:flex;align-items:center;gap:8px;font-weight:600}
.an-tab td small{display:block;color:var(--ink-3);font-size:11.5px;font-weight:400}
.an-tab .e.up{color:var(--good);font-weight:600}.an-tab .e.dn{color:var(--crit);font-weight:600}.an-tab .e.eq{color:var(--ink-3)}
.an-tab .neg{color:var(--crit)}
.an-g{display:inline-block;font-size:11px;font-weight:700;color:var(--an-1);background:color-mix(in srgb,var(--an-1) 12%,transparent);border-radius:999px;padding:1px 7px}
.an-note{font-size:12.5px;color:var(--ink-3);margin:6px 0 0;line-height:1.55;max-width:96ch}
.an-note b{color:var(--ink-2)}
.an-alerte{background:var(--warn-soft);color:var(--warn);border-radius:10px;padding:10px 13px;font-size:13px;margin:0 0 16px;line-height:1.5}
.an-vide{background:var(--surface);border:1px dashed var(--line);border-radius:12px;padding:20px;color:var(--ink-2);font-size:14px;line-height:1.6}
.an-card .rc-met{margin-bottom:12px}
'''

CORPS = '<div id="an"></div>'

JS = r'''
/*__RECAP__*/
const IDX=__IDX__;
const KREG='reglages-v1', KMOD='fiches-modifiees-v1', KFACT='factures-v1';
let REG={}, MOD={}, FACT=[];
try{ REG=JSON.parse(localStorage.getItem(KREG)||'{}')||{}; }catch(e){}
try{ MOD=JSON.parse(localStorage.getItem(KMOD)||'{}')||{}; }catch(e){}
try{ FACT=JSON.parse(localStorage.getItem(KFACT)||'[]')||[]; }catch(e){}
if(!Array.isArray(FACT)) FACT=[];
/* une rubrique des admins : en français ou en anglais (Igal, 9 nov. 2026) — l'espagnol lit l'anglais */
const A3=(fr,en)=>L3(fr,en,en);
const AN_K='analytique-vue';      /* la période et la mesure choisies : propres à ce navigateur, jamais envoyées au serveur */
const AN={sel:'rel:30',met:'ca'};
try{ const r=JSON.parse(localStorage.getItem(AN_K)||'null'); if(r&&typeof r==='object'){ if(r.sel) AN.sel=r.sel; if(r.met) AN.met=r.met; } }catch(e){}
const anSauve=()=>{ try{ localStorage.setItem(AN_K,JSON.stringify(AN)); }catch(e){} };

/* ---- les origines : sept familles + « inconnue », une couleur fixe chacune (palette validée, clair et sombre) ---- */
const AN_GR=[
  {k:'gshop',c:1,fr:'Google Shopping',en:'Google Shopping',aide:['les fiches produits gratuites de Google','Google\'s free product listings']},
  {k:'gads',c:2,fr:'Google Ads (payant)',en:'Google Ads (paid)',aide:['un clic sur une publicité Google','a click on a Google ad']},
  {k:'google',c:3,fr:'Recherche Google',en:'Google search',aide:['les résultats ordinaires de Google','Google\'s regular results']},
  {k:'social',c:4,fr:'Réseaux sociaux',en:'Social media',aide:['Instagram, Facebook, TikTok…','Instagram, Facebook, TikTok…']},
  {k:'email',c:5,fr:'Email',en:'Email',aide:['un email ou une newsletter','an email or a newsletter']},
  {k:'direct',c:6,fr:'Venus directement',en:'Direct',aide:['adresse tapée, favori, lien sans source','typed address, bookmark, link without source']},
  {k:'autre',c:7,fr:'Autres sources',en:'Other sources',aide:['autres sites, autres moteurs, IA, commandes saisies à la main','other sites, other search engines, AI, orders entered by hand']},
  {k:'inconnu',c:0,fr:'Origine inconnue',en:'Unknown origin',aide:['la boutique ne l\'a pas notée','the store did not record it']}];
const anGr=k=>AN_GR.find(g=>g.k===k)||AN_GR[AN_GR.length-1];
const anCoul=k=>`var(--an-${anGr(k).c})`;
const anNomGr=k=>{ const g=anGr(k); return A3(g.fr,g.en); };
const GOOGLE=new Set(['gshop','gads','google']);
function anFamille(code){ const c=String(code||''); const t=c.split(':')[0];
  if(t==='gshop'||t==='gads'||t==='google'||t==='email'||t==='direct') return t;
  if(t==='social') return 'social';
  if(!c||t==='inconnu') return 'inconnu';
  return 'autre'; }
/* le détail d'une origine (« instagram », « fragrantica.com », « IA »…), pour les sous-lignes */
function anDetail(code){ const c=String(code||''); const [t,d]=c.split(/:(.*)/s);
  if(t==='social') return ({instagram:'Instagram',facebook:'Facebook',tiktok:'TikTok',pinterest:'Pinterest',youtube:'YouTube',whatsapp:'WhatsApp',x:'X',snapchat:'Snapchat',linkedin:'LinkedIn',reddit:'Reddit',threads:'Threads'})[d]||d||'';
  if(t==='site') return d||''; if(t==='moteur') return A3('autres moteurs','other search engines'); if(t==='ia') return A3('IA (ChatGPT…)','AI (ChatGPT…)');
  if(t==='manuel') return A3('saisie à la main','entered by hand'); return ''; }

/* ---- les sites en ligne ---- */
const AN_SITES=[{id:'site',auto:'woocommerce',nom:'perfumestrade.com'},{id:'sitegros',auto:'woocommerce-gros',nom:'wholesale.perfumestrade.com'},
  {id:'pc',auto:'shopify-pc',ou:'en ligne',nom:'Perfume City',sous:['en ligne','online']}];
const anSiteDe=v=>{ const a=String(v.auto||''); if(a==='woocommerce') return 'site'; if(a==='woocommerce-gros') return 'sitegros'; if(a==='shopify-pc'&&v.ou==='en ligne') return 'pc'; return ''; };
const anSiteNom=id=>{ const s=AN_SITES.find(x=>x.id===id); return s?(s.nom+(s.sous?' '+A3(s.sous[0],s.sous[1]):'')):id; };

let ORI={};
try{ ORI=JSON.parse(localStorage.getItem('ventes-origine-v1')||'{}')||{}; }catch(e){ ORI={}; }

/* les commandes des sites, une par facture (les lignes du même calcul que Ventes, regroupées) */
function anCommandes(L){
  const I={}; FACT.forEach(f=>{ if(f&&f.id) I[f.id]=String(f._i||'').replace(/^fa\|/,''); });
  const M=new Map();
  L.forEach(v=>{ const s=anSiteDe(v); if(!s||v.hist) return;
    const k=(v.fid||v.num)+'|'+(v.cmd||'');
    let o=M.get(k); if(!o){ const id=I[v.fid]||''; const code=id?ORI[id]:'';
      o={k,site:s,d:v.d,ca:0,mg:0,q:0,ret:!!v.ret,code:code||'',fam:anFamille(code),lu:!!code,lignes:[]}; M.set(k,o); }
    o.ca+=v.mt||0; o.mg+=v.mg||0; o.q+=v.q||0; o.lignes.push(v); });
  return [...M.values()];
}
const anDans=(X,a,b)=>X.filter(o=>o.d>=a&&o.d<=b);
function anSomme(C){ const T={ca:0,mg:0,n:0,q:0}; C.forEach(o=>{ T.ca+=o.ca; T.mg+=o.mg; T.q+=o.q; if(!o.ret) T.n++; }); return T; }
function anParFam(C){ const G={}; C.forEach(o=>{ const g=G[o.fam]=G[o.fam]||{ca:0,n:0,q:0,det:{}}; g.ca+=o.ca; g.q+=o.q; if(!o.ret){ g.n++; const d=anDetail(o.code); if(d) g.det[d]=(g.det[d]||0)+1; } }); return G; }

/* ---- formats ---- */
const anPct=(a,b)=>(b==null||Math.abs(b)<0.005)?null:(a-b)/Math.abs(b)*100;
function anEvo(a,b,lib,fmt){ if(b==null) return '';
  fmt=fmt||money; const p=anPct(a,b);
  if(p==null) return a?`<span class="e up">▲ ${A3('nouveau','new')}</span>`:'';
  const s=p>0.5?'up':p<-0.5?'dn':'eq'; const fl=s==='up'?'▲':s==='dn'?'▼':'=';
  if(Math.abs(p)>500) return `<span class="e ${s}">${fl} ${A3('avant','before')} : ${fmt(b)}</span>`;
  return `<span class="e ${s}">${fl} ${nf(Math.round(Math.abs(p)))} %${lib?` <span data-nolang>vs ${esc(lib)}</span>`:''}</span>`; }
function anEvoPts(a,b,lib){ if(a==null||b==null) return ''; const d=a-b; const s=d>0.5?'up':d<-0.5?'dn':'eq';
  return `<span class="e ${s}">${s==='up'?'▲':s==='dn'?'▼':'='} ${nf(Math.round(Math.abs(d)))} ${A3('pts','pts')} <span data-nolang>vs ${esc(lib)}</span></span>`; }

/* ---- la petite courbe d'un chiffre, jour par jour (ou mois par mois) ---- */
function anSpark(vals){
  const n=vals.length; if(n<2) return '';
  const W=200,H=36,lo=Math.min(0,...vals),hi=Math.max(...vals,lo+1e-9);
  const x=i=>i/(n-1)*W, y=v=>H-2-((v-lo)/(hi-lo||1))*(H-6);
  const pts=vals.map((v,i)=>[x(i),y(v)]);
  const l='M'+pts.map(p=>p[0].toFixed(1)+' '+p[1].toFixed(1)).join(' L');
  const a=l+` L${W} ${H} L0 ${H} Z`; const z=pts[n-1];
  return `<svg class="an-sp" viewBox="0 0 ${W} ${H}" preserveAspectRatio="none" aria-hidden="true"><path class="a" d="${a}"/><path class="l" d="${l}" vector-effect="non-scaling-stroke"/><circle cx="${z[0].toFixed(1)}" cy="${z[1].toFixed(1)}" r="3" vector-effect="non-scaling-stroke"/></svg>`;
}
function anSerie(B,X,val){ const idx={}; B.K.forEach((k,i)=>idx[k.k]=i); const s=B.K.map(()=>0);
  X.forEach(o=>{ const i=idx[B.jour?o.d:o.d.slice(0,7)]; if(i!=null) s[i]+=val(o); }); return s; }

/* ---- les colonnes empilées des origines ---- */
function anColonnes(P,C,met){
  const B=rcBuckets(P,C); if(!B.K.length) return '';
  const idx={}; B.K.forEach((k,i)=>idx[k.k]=i);
  const cel=B.K.map(()=>({}));
  C.forEach(o=>{ const i=idx[B.jour?o.d:o.d.slice(0,7)]; if(i==null) return; const v=met==='n'?(o.ret?0:1):o.ca; if(!v) return; cel[i][o.fam]=(cel[i][o.fam]||0)+v; });
  const fmt=v=>met==='n'?nf(Math.round(v)):money(v);
  let hi=0, lo=0; cel.forEach(c=>{ let u=0,d=0; Object.values(c).forEach(x=>{ if(x>0) u+=x; else d+=x; }); hi=Math.max(hi,u); lo=Math.min(lo,d); });
  const pas=rcNice(Math.max(hi,-lo,met==='n'?1:10)/4); const top=Math.ceil(hi/pas)*pas||pas, bas=Math.floor(lo/pas)*pas, tot=top-bas;
  const pc=v=>((v-bas)/tot*100); const ticks=[]; for(let t=bas;t<=top+1e-9;t+=pas) ticks.push(t);
  const ordre=AN_GR.map(g=>g.k);
  const cols=B.K.map((k,i)=>{ const c=cel[i]; let up=0,dn=0,segs='';
    const arr=ordre.filter(n=>(c[n]||0)!==0), dern=arr.filter(n=>c[n]>0).pop();
    arr.forEach(n=>{ const v=c[n], h=Math.abs(v)/tot*100;
      if(v>0){ segs+=`<i class="rc-s ${n===dern?'top':''}" style="--c:${anCoul(n)};bottom:${pc(0)+up}%;height:${h}%"></i>`; up+=h; }
      else { dn+=h; segs+=`<i class="rc-s neg" style="--c:${anCoul(n)};bottom:${pc(0)-dn}%;height:${h}%"></i>`; } });
    const tip=`<b class="t" data-nolang>${esc(k.lib)}</b>`+(arr.length?arr.map(n=>`<div><span><i class="rc-sw" style="--c:${anCoul(n)}"></i>${esc(anNomGr(n))}</span><b>${fmt(c[n])}</b></div>`).join(''):`<div><span>${A3('rien','nothing')}</span></div>`)
      +(arr.length>1?`<div class="tot"><span>${A3('Total','Total')}</span><b>${fmt(arr.reduce((a,n)=>a+c[n],0))}</b></div>`:'');
    const lab=k.lib+' : '+(arr.length?arr.map(n=>anNomGr(n)+' '+fmt(c[n])).join(', '):A3('rien','nothing'));
    return `<div class="rc-col" tabindex="0" data-tip="${esc(tip)}" aria-label="${esc(lab)}"><div class="rc-b">${segs}</div></div>`; }).join('');
  const nX=B.K.length, pasX=B.jour?(nX<=16?1:nX<=31?2:nX<=62?4:7):(nX<=12?1:3);
  const xl=B.K.map((k,i)=>`<span>${i%pasX===0?`<i data-nolang>${esc(k.court)}</i>`:''}</span>`).join('');
  const vus=ordre.filter(n=>cel.some(c=>c[n]));
  const leg=vus.map(n=>`<span><i class="rc-sw" style="--c:${anCoul(n)}"></i>${esc(anNomGr(n))}</span>`).join('');
  const figs=`<details><summary>${A3('Voir les chiffres','See the figures')}, ${B.jour?A3('jour par jour','day by day'):A3('mois par mois','month by month')}</summary>
    <table class="rc-tab"><thead><tr><th>${B.jour?A3('Jour','Day'):A3('Mois','Month')}</th>${vus.map(n=>`<th class="r">${esc(anNomGr(n))}</th>`).join('')}<th class="r">${A3('Total','Total')}</th></tr></thead>
    <tbody>${B.K.map((k,i)=>{ const c=cel[i]; if(!Object.keys(c).length) return ''; const t=Object.values(c).reduce((a,x)=>a+x,0);
      return `<tr><td data-nolang>${esc(k.lib)}</td>${vus.map(n=>`<td class="r ${c[n]<0?'neg':''}">${c[n]?fmt(c[n]):'·'}</td>`).join('')}<td class="r"><b>${fmt(t)}</b></td></tr>`; }).join('')}</tbody></table></details>`;
  return `<div class="rc-pw"><div class="rc-y">${ticks.slice().reverse().map(t=>`<span>${fmt(t)}</span>`).join('')}</div><div class="rc-plot">${ticks.map(t=>`<i class="rc-gl ${t===0?'zero':''}" style="bottom:${pc(t)}%"></i>`).join('')}<div class="rc-cols">${cols}</div></div><div class="rc-x" style="grid-template-columns:repeat(${nX},1fr)">${xl}</div></div>
    <div class="rc-leg">${leg}</div>${figs}`;
}

/* ---- l'état des relectures du cockpit (dernière lecture, panne) ---- */
function anEtat(){
  const E=[['_woocommerce','perfumestrade.com'],['_woocommerce-gros','wholesale.perfumestrade.com'],['_shopify-pc','Perfume City']];
  const vu=E.map(([k,n])=>({n,e:ORI[k]})).filter(x=>x.e);
  const pannes=vu.filter(x=>x.e.err);
  const date=s=>{ try{ return new Date(s).toLocaleString(A3('fr-FR','en-US'),{day:'numeric',month:'short',hour:'2-digit',minute:'2-digit'}); }catch(e){ return String(s||''); } };
  return {vu,pannes,txt:vu.map(x=>`<span data-nolang>${esc(x.n)}</span> : ${x.e.err?`<b class="neg">${A3('lecture en panne','reading failed')}</b>`:A3('lu le','read on')+' <span data-nolang>'+esc(date(x.e.maj))+'</span>'}`).join(' · '),
    pannesTxt:pannes.map(x=>`<span data-nolang>${esc(x.n)} — ${esc(String(x.e.err).slice(0,160))}</span>`).join('<br>')};
}

/* ================= LE DESSIN ================= */
function anDessine(){
  const z=document.getElementById('an'); if(!z) return;
  const L=rcLignes(), P=rcPlage(AN.sel), R=rcAgrege(L,P.a,P.b), Q0=rcPrec(AN.sel,P);
  /* comme le Tableau de bord : pas de comparaison avec une période d'avant le 1er oct. 2026 (chiffres incomplets) */
  const Q=(Q0&&Q0.a<RC_COMPLET)?null:Q0, RP=Q?rcAgrege(L,Q.a,Q.b):null, lib=Q?rcLibPrec(AN.sel,Q):'';
  const CMD=anCommandes(L), C=anDans(CMD,P.a,P.b), CP=Q?anDans(CMD,Q.a,Q.b):null;
  const S=anSomme(C), SP=CP?anSomme(CP):null;
  const nG=C.filter(o=>!o.ret&&GOOGLE.has(o.fam)).length, nGP=CP?CP.filter(o=>!o.ret&&GOOGLE.has(o.fam)).length:null;
  const partG=S.n?nG/S.n*100:null, partGP=(SP&&SP.n)?nGP/SP.n*100:null;
  const caShop=C.filter(o=>o.fam==='gshop').reduce((a,o)=>a+o.ca,0), nShop=C.filter(o=>o.fam==='gshop'&&!o.ret).length;
  const chips=[['rel:7',A3('7 jours','7 days')],['rel:30',A3('30 jours','30 days')],['cemois',A3('Ce mois','This month')],['moisdernier',A3('Mois dernier','Last month')],['rel:90',A3('90 jours','90 days')],['cetteannee',A3('Cette année','This year')]];
  let h=`<div class="an-bar">${chips.map(([v,l])=>`<button type="button" class="rc-chip ${AN.sel===v?'on':''}" data-an="${v}">${l}</button>`).join('')}</div>
    <p class="an-per"><b data-nolang>${esc(rcLib(AN.sel,P))}</b>${Q?` · ${A3('comparé à','compared with')} <span data-nolang>${esc(lib)}</span>`:(Q0?` · ${A3('pas de comparaison : avant le 1er octobre 2026, les chiffres sont incomplets','no comparison: figures before October 1, 2026 are incomplete')}`:'')}</p>`;
  const etat=anEtat();
  if(etat.pannes.length) h+=`<div class="an-alerte">${A3('Le cockpit n\'arrive pas à lire l\'origine des commandes de :','The cockpit cannot read the origin of orders from:')}<br>${etat.pannesTxt}</div>`;
  if(!R.S.length){ h+=`<div class="an-vide">${A3('Aucune vente sur cette période. Choisis-en une autre ci-dessus.','No sale in this period. Pick another one above.')}</div>`; z.innerHTML=h; anBranche(); return; }
  /* ---- 1. les cinq chiffres ---- */
  const B=rcBuckets(P,R.S);
  const spT=anSpark(anSerie(B,R.S,v=>v.mt)), spM=anSpark(anSerie(B,R.S,v=>v.mg||0));
  const spS=anSpark(anSerie(B,C,o=>o.ca)), spN=anSpark(anSerie(B,C,o=>o.ret?0:1));
  const spG=anSpark(anSerie(B,C,o=>(!o.ret&&GOOGLE.has(o.fam))?1:0));
  const T=R.T, TP=RP?RP.T:null, pctMg=T.ca>0?T.mg/T.ca*100:null;
  h+=`<div class="an-kpis">
    <div class="an-kpi"><span class="k">${A3("Chiffre d'affaires",'Revenue')}</span><span class="v">${money(T.ca)}</span><span class="s">${A3('tous les canaux, remboursements déduits','all channels, refunds deducted')}</span>${anEvo(T.ca,TP&&TP.ca,lib)}${spT}</div>
    <div class="an-kpi"><span class="k">${A3('Marge nette','Net margin')}</span><span class="v ${T.mg<0?'neg':''}">${money(T.mg)}</span><span class="s">${pctMg!=null?nf(Math.round(pctMg*10)/10)+' % '+A3('du chiffre d\'affaires','of revenue'):'&nbsp;'}</span>${anEvo(T.mg,TP&&TP.mg,lib)}${spM}</div>
    <div class="an-kpi"><span class="k">${A3('Ventes des sites','Website sales')}</span><span class="v">${money(S.ca)}</span><span class="s">${A3('perfumestrade.com, wholesale, Perfume City en ligne','perfumestrade.com, wholesale, Perfume City online')}</span>${anEvo(S.ca,SP&&SP.ca,lib)}${spS}</div>
    <div class="an-kpi"><span class="k">${A3('Commandes en ligne','Online orders')}</span><span class="v">${nf(S.n)}</span><span class="s">${S.n?A3('panier moyen','average basket')+' '+money(S.ca/S.n):'&nbsp;'}</span>${anEvo(S.n,SP&&SP.n,lib,nf)}${spN}</div>
    <div class="an-kpi g"><span class="k">${A3('Venues de Google','From Google')}</span><span class="v">${partG==null?'—':nf(Math.round(partG))+' %'}</span><span class="s">${nf(nG)} ${A3('commande'+(nG>1?'s':''),'order'+(nG>1?'s':''))} · ${A3('dont Google Shopping','incl. Google Shopping')} ${nf(nShop)} (${money(caShop)})</span>${anEvoPts(partG,partGP,lib)}${spG}</div>
  </div>`;
  /* ---- 2. d'où viennent les commandes ---- */
  const G=anParFam(C), GP=CP?anParFam(CP):null;
  const nTot=Math.max(1,S.n), caMax=Math.max(1,...Object.values(G).map(g=>Math.max(0,g.ca)));
  const lus=C.filter(o=>!o.ret&&o.lu).length;
  const rangs=AN_GR.filter(g=>G[g.k]&&(G[g.k].n||G[g.k].ca)).sort((a,b)=>(a.k==='inconnu')-(b.k==='inconnu')||G[b.k].ca-G[a.k].ca);
  const det=g=>{ const d=Object.entries(g.det).sort((a,b)=>b[1]-a[1]); return d.length?`<small class="det" data-nolang>${d.slice(0,5).map(([n,c])=>esc(n)+' '+c).join(' · ')}</small>`:''; };
  h+=`<h2 class="sec">${A3('D\'où viennent les commandes des sites','Where website orders come from')} <em>${A3('commandes de perfumestrade.com, wholesale et Perfume City en ligne','orders from perfumestrade.com, wholesale and Perfume City online')}</em></h2>
  <div class="an-grid"><div class="an-card"><h3>${A3('Au fil des jours','Day by day')}</h3>
    <div class="rc-met">${[['ca',A3("Chiffre d'affaires",'Revenue')],['n',A3('Commandes','Orders')]].map(([m,l])=>`<button type="button" class="rc-chip ${AN.met===m?'on':''}" data-anm="${m}">${l}</button>`).join('')}</div>
    ${C.length?anColonnes(P,C,AN.met):`<p class="an-st">${A3('Aucune commande en ligne sur cette période.','No online order in this period.')}</p>`}</div>
    <div class="an-card"><h3>${A3('Le classement','The ranking')}</h3><p class="an-st">${A3('Part des commandes, chiffre d\'affaires, et évolution','Share of orders, revenue, and change')}${lib?' vs <span data-nolang>'+esc(lib)+'</span>':''}</p>
    <div class="an-rk">${rangs.length?rangs.map(gr=>{ const g=G[gr.k], gp=GP&&GP[gr.k]; const part=g.n/nTot*100;
      return `<div class="an-r" title="${esc(A3(gr.aide[0],gr.aide[1]))}"><div class="n"><i class="an-sw" style="--c:${anCoul(gr.k)}"></i><span>${esc(anNomGr(gr.k))}</span></div><div class="m">${money(g.ca)}</div>
        <div class="d"><i style="--c:${anCoul(gr.k)};width:${Math.max(2,Math.round(Math.max(0,g.ca)/caMax*100))}%"></i><span class="t">${nf(g.n)} ${A3('cmd','ord.')} · ${nf(Math.round(part))} %${GP?' · '+(gp?anEvo(g.ca,gp.ca,'',money):`<span class="e up">${A3('nouveau','new')}</span>`):''}</span></div>${det(g)}</div>`; }).join(''):`<p class="an-st">${A3('Rien sur cette période.','Nothing in this period.')}</p>`}</div></div></div>`;
  /* ---- 3. site par site ---- */
  const sites=AN_SITES.filter(s=>C.some(o=>o.site===s.id));
  if(sites.length){
    const cell=(fam,site)=>{ const X=C.filter(o=>o.fam===fam&&o.site===site); const n=X.filter(o=>!o.ret).length, ca=X.reduce((a,o)=>a+o.ca,0);
      return (n||ca)?`<td class="r"><b>${money(ca)}</b><small>${nf(n)} ${A3('cmd','ord.')}</small></td>`:'<td class="r">·</td>'; };
    const tot=site=>{ const X=C.filter(o=>o.site===site); return `<td class="r"><b>${money(X.reduce((a,o)=>a+o.ca,0))}</b><small>${nf(X.filter(o=>!o.ret).length)} ${A3('cmd','ord.')}</small></td>`; };
    h+=`<div class="an-card" style="margin-bottom:18px"><h3>${A3('Site par site','Site by site')}</h3><p class="an-st">${A3('La même chose, pour chaque site : chiffre d\'affaires et nombre de commandes par origine.','The same, for each site: revenue and number of orders by origin.')}</p>
      <table class="an-tab"><thead><tr><th>${A3('Origine','Origin')}</th>${sites.map(s=>`<th class="r" data-nolang>${esc(anSiteNom(s.id))}</th>`).join('')}<th class="r">${A3('Total','Total')}</th></tr></thead><tbody>
      ${AN_GR.filter(g=>G[g.k]).map(g=>`<tr><td><div class="nm"><i class="an-sw" style="--c:${anCoul(g.k)}"></i>${esc(anNomGr(g.k))}</div></td>${sites.map(s=>cell(g.k,s.id)).join('')}<td class="r"><b>${money(G[g.k].ca)}</b><small>${nf(G[g.k].n)} ${A3('cmd','ord.')}</small></td></tr>`).join('')}
      <tr class="tot"><td>${A3('Total','Total')}</td>${sites.map(s=>tot(s.id)).join('')}<td class="r">${money(S.ca)}<small>${nf(S.n)} ${A3('cmd','ord.')}</small></td></tr></tbody></table></div>`;
  }
  /* ---- 3b. Google : ce que la pub coûte, ce qu'elle rapporte (Igal, 9 nov. 2026 : « est-ce que c'est intéressant de faire du
     Google Ads ? ») — la pub dépensée vient de Google (extension Google for WooCommerce, lue par le cockpit) ; la marge vient de
     l'ERP, commande par commande. La pub tourne sur perfumestrade.com : on compare avec ce site seulement. ---- */
  h+=anGoogle(P,Q,lib,C,CP);
  /* ---- 4. tous les canaux ---- */
  const ordre=Object.values(R.G).sort((a,b)=>b.ca-a.ca||b.q-a.q).map(o=>o.canal);
  const caPos=Object.values(R.G).reduce((a,o)=>a+Math.max(0,o.ca),0)||1;
  h+=`<h2 class="sec">${A3('Tous les canaux de vente','All sales channels')} <a href="tableau.html">${A3('Tableau de bord','Dashboard')}</a></h2>
  <div class="an-card" style="margin-bottom:18px"><table class="an-tab"><thead><tr><th>${A3('Canal','Channel')}</th><th class="r">${A3("Chiffre d'affaires",'Revenue')}</th><th class="r">${A3('Part','Share')}</th><th class="r">${A3('Évolution','Change')}</th><th class="r">${A3('Ventes','Sales')}</th><th class="r">${A3('Panier moyen','Avg basket')}</th><th class="r">${A3('Marge nette','Net margin')}</th></tr></thead><tbody>
  ${ordre.map(n=>{ const o=R.G[n], op=RP&&RP.G[n]; const part=Math.max(0,o.ca)/caPos*100; const pm=o.ca>0&&!o.hist?o.mg/o.ca*100:null;
    return `<tr><td><div class="nm"><i class="rc-sw" style="--c:${rcCoul(n)}"></i><span data-nolang>${esc(rcNomVu(n))}</span></div>${anPcSous(o)}</td><td class="r ${o.ca<0?'neg':''}"><b>${money(o.ca)}</b></td>
      <td class="r"><span class="rc-part"><i style="--c:${rcCoul(n)};--w:${Math.round(part*0.6)}"></i><b>${nf(Math.round(part))} %</b></span></td>
      <td class="r">${RP?(op?anEvo(o.ca,op.ca,'',money):`<span class="e up">${A3('nouveau','new')}</span>`):'—'}</td><td class="r">${nf(o.n)}</td><td class="r">${o.n?money(o.ca/o.n):'—'}</td>
      <td class="r ${o.mg<0?'neg':''}">${o.hist?'—':money(o.mg)}${pm!=null?`<small>${nf(Math.round(pm))} %</small>`:''}</td></tr>`; }).join('')}
  <tr class="tot"><td>${A3('Total','Total')}</td><td class="r">${money(T.ca)}</td><td class="r">100 %</td><td class="r">${RP?anEvo(T.ca,TP.ca,'',money):'—'}</td><td class="r">${nf(T.n)}</td><td class="r">${T.n?money(T.ca/T.n):'—'}</td><td class="r">${money(T.mg)}</td></tr></tbody></table></div>`;
  /* ---- 5. les parfums qui se vendent en ligne ---- */
  const PF={}; C.forEach(o=>o.lignes.forEach(v=>{ if(!v.cle) return; const p=PF[v.cle]=PF[v.cle]||{cle:v.cle,q:0,ca:0,qG:0}; p.q+=v.q||0; p.ca+=v.mt||0; if(GOOGLE.has(o.fam)) p.qG+=v.q||0; }));
  const top=Object.values(PF).filter(p=>p.q>0).sort((a,b)=>b.ca-a.ca).slice(0,10);
  if(top.length){
    h+=`<h2 class="sec">${A3('Les parfums qui se vendent en ligne','Perfumes selling online')} <em>${A3('les dix premiers, sur les trois sites','the top ten, across the three sites')}</em></h2>
    <div class="an-card" style="margin-bottom:18px"><table class="an-tab"><thead><tr><th>${A3('Parfum','Perfume')}</th><th class="r">${A3('Flacons','Bottles')}</th><th class="r">${A3("Chiffre d'affaires",'Revenue')}</th><th class="r">${A3('Via Google','Via Google')}</th></tr></thead><tbody>
    ${top.map(p=>{ const r=IDX[p.cle]||[]; return `<tr><td><a href="catalogue.html#fiche=${encodeURIComponent(p.cle)}" style="color:inherit;text-decoration:none"><b data-nolang>${esc(r[1]||p.cle)}</b><small data-nolang>${esc(r[2]||'')}</small></a></td><td class="r">${nf(p.q)}</td><td class="r"><b>${money(p.ca)}</b></td><td class="r">${p.qG?`<span class="an-g">${nf(p.qG)} / ${nf(p.q)}</span>`:'·'}</td></tr>`; }).join('')}</tbody></table></div>`;
  }
  /* ---- comment c'est compté ---- */
  const nC=C.filter(o=>!o.ret).length;
  h+=`<p class="an-note"><b>${A3('Comment c\'est compté.','How it is counted.')}</b> ${A3('Les ventes et les marges sont celles du Tableau de bord et de la page Ventes (commandes expédiées, remboursements déduits). L\'origine d\'une commande est notée par la boutique elle-même : WooCommerce (perfumestrade.com, wholesale) et Shopify (Perfume City en ligne) retiennent la visite qui a mené à l\'achat ; le cockpit la relit toutes les 10 minutes. « Google Shopping » = les fiches produits gratuites de Google ; « Google Ads » = un clic sur une publicité payante (Shopping payant compris).','Sales and margins are those of the Dashboard and the Sales page (shipped orders, refunds deducted). The origin of an order is recorded by the store itself: WooCommerce (perfumestrade.com, wholesale) and Shopify (Perfume City online) keep the visit that led to the purchase; the cockpit re-reads it every 10 minutes. "Google Shopping" = Google\'s free product listings; "Google Ads" = a click on a paid ad (paid Shopping included).')}
    ${nC?'<br>'+A3(`Origine connue pour ${nf(lus)} des ${nf(nC)} commandes en ligne de la période.`,`Origin known for ${nf(lus)} of the ${nf(nC)} online orders in the period.`):''}
    ${etat.vu.length?'<br>'+etat.txt:'<br>'+A3('Le cockpit n\'a pas encore lu l\'origine des commandes : la première lecture (180 jours) se fait dans les minutes qui suivent sa mise à jour.','The cockpit has not read the order origins yet: the first reading (180 days) happens within minutes of its update.')}</p>`;
  z.innerHTML=h; anBranche();
}
/* la pub Google (google-pub-v1, jour par jour : [pub, ventes Google, clics, affichages, conversions, clics gratuits, affichages gratuits]) */
function anPub(a,b){ let G={}; try{ G=JSON.parse(localStorage.getItem('google-pub-v1')||'{}')||{}; }catch(e){}
  const J=(G&&G.j)||{}; const T={pub:0,ventes:0,clics:0,aff:0,conv:0,gClics:0,gAff:0,jours:0};
  Object.keys(J).forEach(d=>{ if(d<a||d>b) return; const r=J[d]||[]; T.jours++; T.pub+=+r[0]||0; T.ventes+=+r[1]||0; T.clics+=+r[2]||0; T.aff+=+r[3]||0; T.conv+=+r[4]||0; T.gClics+=+r[5]||0; T.gAff+=+r[6]||0; });
  return {T,lu:Object.keys(J).length>0,maj:G._maj||'',err:G._err||''}; }
function anGoogle(P,Q,lib,C,CP){
  const g=anPub(P.a,P.b), gp=Q?anPub(Q.a,Q.b):null;
  let h=`<h2 class="sec">${A3('Google : ce que la pub coûte, ce qu\'elle rapporte','Google: what ads cost, what they bring')} <em data-nolang>perfumestrade.com</em></h2>`;
  if(!g.lu){ return h+`<div class="an-vide">${g.err?A3('Le cockpit n\'arrive pas à lire les chiffres de Google : ','The cockpit cannot read Google\'s figures: ')+'<span data-nolang>'+esc(g.err)+'</span>':A3('Les chiffres de Google arrivent : le cockpit les lit une fois par heure dans l\'extension Google for WooCommerce du site.','Google\'s figures are on their way: the cockpit reads them once an hour from the site\'s Google for WooCommerce extension.')}</div>`; }
  const site=X=>X.filter(o=>o.site==='site');
  const S=site(C), SP=CP?site(CP):null;
  const ads=S.filter(o=>o.fam==='gads'), adsP=SP?SP.filter(o=>o.fam==='gads'):null;
  const caAds=ads.reduce((a,o)=>a+o.ca,0), mgAds=ads.reduce((a,o)=>a+o.mg,0), nAds=ads.filter(o=>!o.ret).length;
  const mgSite=S.reduce((a,o)=>a+o.mg,0), caSite=S.reduce((a,o)=>a+o.ca,0);
  const reste=mgAds-g.T.pub, resteP=adsP?adsP.reduce((a,o)=>a+o.mg,0)-gp.T.pub:null;
  const resteSite=mgSite-g.T.pub;
  const cl=v=>v<0?'dn':'up';
  h+=`<div class="an-kpis">
    <div class="an-kpi"><span class="k">${A3('Pub Google Ads dépensée','Google Ads spend')}</span><span class="v">${money(g.T.pub)}</span><span class="s">${nf(Math.round(g.T.clics))} ${A3('clics','clicks')} · ${A3('coût par clic','cost per click')} ${g.T.clics?money2(g.T.pub/g.T.clics):'—'}</span>${gp?anEvo(g.T.pub,gp.T.pub,lib):''}</div>
    <div class="an-kpi"><span class="k">${A3('Ventes que Google s\'attribue','Sales Google claims')}</span><span class="v">${money(g.T.ventes)}</span><span class="s">${A3('selon Google','according to Google')} · ${nf(Math.round(g.T.conv))} ${A3('conversions','conversions')}${g.T.pub?' · '+A3('rapport','ratio')+' '+nf(Math.round(g.T.ventes/g.T.pub*10)/10)+' ×':''}</span></div>
    <div class="an-kpi"><span class="k">${A3('Commandes venues de la pub','Orders from the ads')}</span><span class="v">${money(caAds)}</span><span class="s">${nf(nAds)} ${A3('commande'+(nAds>1?'s':''),'order'+(nAds>1?'s':''))} ${A3('expédiée'+(nAds>1?'s':''),'shipped')} · ${A3('marge nette','net margin')} ${money(mgAds)}</span></div>
    <div class="an-kpi"><span class="k">${A3('Ce qui reste après la pub','What is left after ads')}</span><span class="v ${reste<0?'neg':''}">${money(reste)}</span><span class="s">${A3('marge des commandes venues de la pub, moins la pub','margin of orders from the ads, minus ad spend')}</span>${resteP!=null?`<span class="e ${cl(reste-resteP)}">${A3('avant','before')} : ${money(resteP)}</span>`:''}</div>
    <div class="an-kpi g"><span class="k">${A3('Google Shopping gratuit','Free Google Shopping')}</span><span class="v">${nf(Math.round(g.T.gClics))} ${A3('clic'+(g.T.gClics>1?'s':''),'click'+(g.T.gClics>1?'s':''))}</span><span class="s">${nf(Math.round(g.T.gAff))} ${A3('affichages des fiches gratuites','free listing impressions')}</span>${gp?anEvo(g.T.gClics,gp.T.gClics,lib,nf):''}</div>
  </div>`;
  h+=`<p class="an-note">${A3(`Sur la période, tout le site perfumestrade.com a fait <b>${money(caSite)}</b> de ventes pour <b>${money(mgSite)}</b> de marge nette ; après la pub (${money(g.T.pub)}), il reste <b class="${resteSite<0?'neg':''}">${money(resteSite)}</b>, même si toutes ses ventes venaient de Google.`,`Over the period, the whole perfumestrade.com site made <b>${money(caSite)}</b> in sales for <b>${money(mgSite)}</b> net margin; after ads (${money(g.T.pub)}), <b class="${resteSite<0?'neg':''}">${money(resteSite)}</b> is left, even if all its sales came from Google.`)}
    ${A3('La marge nette est celle de l\'ERP (prix d\'achat, commission, envoi) ; elle ne compte ni l\'emballage ni les salaires. Les ventes « selon Google » sont souvent plus hautes que les vraies : Google compte aussi les commandes pas encore expédiées et celles où la pub n\'a fait que passer.','The net margin is the ERP\'s (purchase price, commission, shipping); it counts neither packaging nor wages. Sales “according to Google” are often higher than the real ones: Google also counts orders not shipped yet and those where the ad only played a small part.')}
    ${g.err?'<br><b class="neg">'+A3('Dernière lecture de Google en panne : ','Last Google reading failed: ')+'</b><span data-nolang>'+esc(g.err)+'</span>':''}</p>`;
  return h;
}
/* Perfume City = deux points de vente : la boutique et le site (Igal, 9 nov. 2026 : « tous les différents points de vente de Sam ») */
function anPcSous(o){ if(rcId(o.canal)!=='pc'||!o.ou) return ''; const ks=Object.keys(o.ou).filter(k=>k&&(o.ou[k].q||o.ou[k].ca)); if(!ks.length) return '';
  return `<small>${ks.sort().map(k=>(k==='boutique'?A3('en boutique','in store'):k==='en ligne'?A3('en ligne','online'):A3('autre','other'))+' <b data-nolang>'+money(o.ou[k].ca)+'</b>').join(' · ')}</small>`; }
let _anTip=null;
function anBranche(){
  const z=document.getElementById('an'); if(!z) return;
  z.querySelectorAll('[data-an]').forEach(b=>b.onclick=()=>{ AN.sel=b.dataset.an; anSauve(); anDessine(); });
  z.querySelectorAll('[data-anm]').forEach(b=>b.onclick=()=>{ AN.met=b.dataset.anm; anSauve(); anDessine(); });
  if(!_anTip){ _anTip=document.createElement('div'); _anTip.className='rc-tip'; document.body.appendChild(_anTip); }
  const montre=(el,ev)=>{ _anTip.innerHTML=el.dataset.tip||''; _anTip.style.display='block';
    const r=el.getBoundingClientRect(); let x=(ev&&ev.clientX!=null?ev.clientX:r.left+r.width/2)+12, y=(ev&&ev.clientY!=null?ev.clientY:r.top)-10;
    const w=_anTip.offsetWidth||220; if(x+w>window.innerWidth-8) x=x-w-24; if(y<8) y=8; _anTip.style.left=x+'px'; _anTip.style.top=y+'px'; };
  const cache=()=>{ _anTip.style.display='none'; };
  z.querySelectorAll('.rc-col').forEach(c=>{ c.onmouseenter=e=>montre(c,e); c.onmousemove=e=>montre(c,e); c.onmouseleave=cache; c.onfocus=()=>montre(c,null); c.onblur=cache; });
}
/* les administrateurs de l'ERP : les rôles Admin et Patron, et eux seuls (un Comptable, qui voit les marges, n'y entre pas) */
function anAdmin(){ const s=session(); return !!s&&/^(admin|patron)$/.test(String(s.role||'')); }
window.__an={AN,anCommandes,anFamille,anDessine,ORI:()=>ORI};
function majUser(){ try{ piedSession(); }catch(e){} }
majUser();
(function(){
  const s=session(); if(!s) return;
  /* Igal, 9 nov. 2026 : « personne à part les admins de l'ERP ne peut la regarder » — Admin (Igal) et Patron (Sam), aucun autre rôle */
  if(!anAdmin()){
    document.querySelector('.wrap').insertAdjacentHTML('beforeend',`<div class="mur"><h2>${A3('Cette rubrique n\'est pas pour ce rôle','This section is not for this role')}</h2><p>${A3('L\'analytique est réservée aux administrateurs de l\'ERP.','Analytics is for the ERP administrators only.')}</p></div>`);
    const a=$('an'); if(a) a.remove(); try{ $('src').innerHTML=A3('accès refusé','access denied'); }catch(e){} return;
  }
  anDessine();
  try{ $('src').innerHTML=A3('origine des commandes<br>relue toutes les 10 min','order origin<br>re-read every 10 min'); }catch(e){}
  /* une nouvelle version des factures ou des origines arrive du serveur (toutes les 8 s) : on relit et on redessine */
  window.addEventListener('storage',e=>{ if(e.key==='ventes-origine-v1'||e.key==='google-pub-v1'||e.key===KFACT){ try{ ORI=JSON.parse(localStorage.getItem('ventes-origine-v1')||'{}')||{}; FACT=JSON.parse(localStorage.getItem(KFACT)||'[]')||[]; }catch(_){} anDessine(); } });
})();
'''

html = coquille("Analytique", "Analytique",
  "D'où viennent les ventes : tous les canaux, et pour les sites, l'origine de chaque commande (Google Shopping, Google Ads, réseaux sociaux…). Réservé aux administrateurs de l'ERP.",
  CSS, CORPS, JS.replace('/*__RECAP__*/', RECAP_JS), donnees=('produits', 'histgros')).replace('__IDX__', 'Object.fromEntries(D_TOUS().map(r=>[r[15],[r[0],r[13],r[2],r[12],r[6],r[8],r[7],r[14],r[4],r[5],r[9]]]))')
open('analytique.html', 'w').write(html)
print('analytique.html', len(html)//1024, 'Ko')
