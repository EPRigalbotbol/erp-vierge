# -*- coding: utf-8 -*-
"""MAILING — une offre à chaque secteur : les grossistes et les particuliers (15 nov. 2026).

Igal, 15 nov. 2026 : « créer une nouvelle rubrique qu'on appellerait Mailing dans l'ERP, configurée pour le mailing
pour le wholesale et le mailing pour le particulier. Quelque chose de simple où on pourrait envoyer une offre à chaque
secteur. » Avant, il demandait de connaître le dernier parfum acheté par chaque client, et de faire une remise aux
clients réguliers sur ce parfum-là.

Ce que fait la page, pour le secteur choisi (Wholesale ou Particuliers) :
  1. L'OFFRE : une remise en %, une date de fin, et le message (modifiable, en français, anglais et espagnol).
  2. LES CLIENTS : chacun avec ses achats, son dernier achat, et LES PARFUMS QU'ON LUI PROPOSE —
       - particulier : le dernier parfum qu'il a acheté et qui est en stock ;
       - grossiste : ses 5 parfums les plus achetés qui sont en stock, au prix de gros ;
     et, pour chaque parfum, le prix habituel et le prix offert.
  3. L'ENVOI : WhatsApp, UN PAR UN, personnalisé (prénom, parfums, prix, dans la langue du client) — choix d'Igal.
     Pour les emails : AUCUN envoi en masse depuis Gmail (Igal : « le moins risqué pour éviter d'être spammé ») ;
     la page donne un fichier à importer dans Klaviyo ou Brevo, qui gèrent la désinscription.

LE PRIX OFFERT N'EST JAMAIS UNE PERTE :
  - particulier : après la remise, le flacon doit encore laisser au moins 15 $ une fois payés le prix d'achat, la
    commission du site (Réglages › Canaux) et l'envoi (8 $) ; la remise ne dépasse jamais 25 % (au-delà, un grand nom
    fait douter de l'authenticité — étude Black Friday du 15 nov.). Sans prix d'achat connu : pas de remise.
  - grossiste : jamais moins que le prix d'achat + 5 %.
  La colonne « Prix offert » montre le prix réel, après ces planchers.

Qui est exclu : les clients désinscrits (la même case que la liste de diffusion de Clients, « nodiff »), les clients
Amazon (Amazon interdit de démarcher ses acheteurs), les clientes de Perfume City (la boutique de Kim, à part).
Réservée aux administrateurs de l'ERP (Admin, Patron), comme l'Analytique — choix d'Igal.

Ce qui est gardé (magasin « mailing-v1 ») : l'offre en cours de chaque secteur, et qui l'a déjà reçue (date, par qui),
pour ne jamais envoyer deux fois la même offre au même client. Chaque envoi est noté au Journal.
"""
import re
from build_crm import coquille

# Les autres noms d'un même client (« Juan » = Casa del Perfume…) : UNE seule liste, celle de la rubrique Clients,
# relue ici à la fabrication — la Mailing ne peut pas réunir les clients autrement que Clients.
_CLI = open('build_clients.py', encoding='utf-8').read()
_m = re.search(r"const ALIAS_CLI=\{.*?\};\nconst canon=nom=>ALIAS_CLI\[cNorm\(nom\)\]\|\|nom;", _CLI, re.S)
assert _m, "build_clients.py : la liste ALIAS_CLI n'a pas été trouvée"
ALIAS = _m.group(0)

CSS = r'''
.mur{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:34px 32px;max-width:640px;margin:26px auto}
.mur h2{margin:0 0 10px;font-size:20px;font-weight:700;letter-spacing:-.015em}
.mur p{margin:0;color:var(--ink-2);font-size:14.5px;line-height:1.65}
.mlseg{display:flex;gap:10px;margin:4px 0 18px;flex-wrap:wrap}
.mlseg button{flex:1;min-width:220px;text-align:left;padding:14px 18px;border:1px solid var(--line);border-radius:12px;background:var(--surface);
 color:var(--ink-2);font-family:inherit;cursor:pointer}
.mlseg button b{display:block;font-size:17px;color:var(--ink);margin-bottom:3px}
.mlseg button span{font-size:12.5px;color:var(--ink-3)}
.mlseg button.on{border-color:var(--iris);box-shadow:0 0 0 2px var(--iris-soft);background:var(--iris-soft)}
.mlseg button.on b{color:var(--iris)}
.mlc{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:18px 20px;margin-bottom:16px}
.mlc h3{margin:0 0 12px;font-size:15px;font-weight:700;letter-spacing:-.01em}
.mlc h3 i{font-style:normal;display:inline-flex;align-items:center;justify-content:center;width:22px;height:22px;border-radius:50%;
 background:var(--iris);color:#fff;font-size:12px;margin-right:8px}
.mlrow{display:flex;flex-wrap:wrap;align-items:center;gap:14px;margin-bottom:10px}
.mlrow label{font-size:13px;color:var(--ink-2);display:flex;align-items:center;gap:7px}
.mlrow input[type=number]{width:70px}
.mlrow input,.mlrow select{padding:7px 9px;font-family:inherit;font-size:14px;border:1px solid var(--line);border-radius:8px;background:var(--surface);color:var(--ink)}
.mlmsg summary{cursor:pointer;font-size:13px;color:var(--iris);font-weight:600;margin-top:4px}
.mlmsg .mlml{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:10px;margin-top:10px}
.mlmsg textarea{width:100%;min-height:190px;padding:9px 10px;font-family:inherit;font-size:13px;line-height:1.5;border:1px solid var(--line);border-radius:8px;
 background:var(--surface);color:var(--ink);resize:vertical}
.mlmsg .lab{font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--ink-3);font-weight:700;margin-bottom:4px}
.mlcpt{font-size:13px;color:var(--ink-2);margin:0 0 10px}
.mlcpt b{color:var(--ink)}
.mlwrap{overflow-x:auto}
table.mlt{width:100%;border-collapse:collapse;font-size:13px}
.mlt th{text-align:left;font-size:10.5px;letter-spacing:.09em;text-transform:uppercase;color:var(--ink-3);font-weight:700;padding:8px 8px;border-bottom:1px solid var(--line)}
.mlt td{padding:9px 8px;border-bottom:1px solid var(--line-2);vertical-align:top}
.mlt td.n,.mlt th.n{text-align:right;white-space:nowrap}
.mlt tr.fait td{background:var(--good-soft)}
.mlt .cl b{display:block;font-size:13.5px}
.mlt .cl small{display:block;color:var(--ink-3);font-size:11.5px;margin-top:2px}
.mlt .pf div{margin-bottom:3px}
.mlt .pf small{color:var(--ink-3)}
.mlt .pf .px{display:block;white-space:nowrap;margin-top:1px}
.mlt .px .av{color:var(--ink-3)}
.mlt .px em,.mlt .px b{font-style:normal;color:var(--good);font-weight:700}
.mlt .px b{color:var(--ink)}
.mlt .px .pl{color:var(--warn);font-size:11px}
.mlt .act{white-space:nowrap}
.mlt .act .btn{padding:5px 10px;font-size:12px}
.mlt .wa{background:#25d366;border-color:#25d366;color:#fff;font-weight:600}
.mlt .wa:hover{background:#1ebe5b;color:#fff}
.mlt .ok{color:var(--good);font-size:11.5px;display:block;margin-top:4px}
.mlt .ok .nenv{padding:2px 8px;font-size:11px;margin-left:6px}
.mlt select{padding:4px 6px;font-size:12px;border:1px solid var(--line);border-radius:6px;background:var(--surface);color:var(--ink)}
.mlt .ap td{background:var(--surface-2)}
.mlt .ap pre{white-space:pre-wrap;font-family:inherit;font-size:12.5px;margin:0;line-height:1.5}
.mlgo{display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin-bottom:10px}
.mlgo .wa{background:#25d366;border-color:#25d366;color:#fff;font-weight:600;font-size:14.5px;padding:10px 16px}
.mlgo .wa:hover{background:#1ebe5b;color:#fff}
.mlgo .wa:disabled{background:var(--surface-2);border-color:var(--line);color:var(--ink-3)}
.mlnote{font-size:12.5px;color:var(--ink-3);line-height:1.6;margin:6px 0 0}
.mlvide{padding:22px;text-align:center;color:var(--ink-3);font-size:13.5px}
'''

CORPS = '<div id="ml"></div>'

JS = r'''
const BC2CLE=__BC2CLE__;
const KCLI='clients-v1', KFACT='factures-v1', KRET='retail-local-v1', KJOU='crm-journal-v1', ML_K='mailing-v1';
const T=(fr,en,es)=>(typeof L3==='function'?L3(fr,en,es):fr);
const cNorm=s=>String(s==null?'':s).toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/[^a-z0-9]+/g,' ').trim();
__ALIAS__
const bcN=v=>String(v==null?'':v).replace(/[^0-9A-Za-z]/g,'').replace(/^0+/,'');
let USR=NOM_UTIL; try{ window.__nomChange.push(v=>{ USR=v; }); }catch(e){}

/* LES RÈGLES DU PRIX OFFERT (voir l'en-tête du fichier) */
const ML_MARGE_DETAIL=15;     /* $ qui doivent rester à Sam par flacon, après la remise (particuliers) */
const ML_PLAFOND=25;          /* % : la remise ne va jamais au-delà */
const ML_MARGE_GROS=0.05;     /* grossiste : jamais moins que le prix d'achat + 5 % */
const ML_NB_GROS=5;           /* grossiste : ses 5 parfums les plus achetés, en stock */

/* ---- les fiches : prix, prix de gros, prix d'achat, stock — ceux du Catalogue (fiche modifiée comprise) ---- */
let _MLF=null;
function mlFiches(){
  if(_MLF) return _MLF;
  const M={}; let MOD={}, EXT={q:{}};
  try{ MOD=lit('fiches-modifiees-v1',{})||{}; }catch(e){}
  try{ const r=lit('stock-externe-v1',null); if(r&&r.q) EXT=r; }catch(e){}
  let rows=[]; try{ rows=D_TOUS(); }catch(e){}
  const n=v=>(v==null||v==='')?null:+v;
  rows.forEach(r=>{ const cle=r[15]; if(!cle) return; const m=MOD[cle]||{}, bc=String(r[0]||'');
    let q=r[6]; if(EXT.q&&EXT.q[bc]!=null) q=EXT.q[bc]; if(m.qte!=null) q=m.qte;
    const ml=String(m.ml!=null&&m.ml!==''?m.ml:(r[3]||'')).trim(), ty=String(m.type||r[4]||'').toUpperCase().trim();
    M[cle]={cle,bc,nom:String((m.nom!=null&&m.nom!=='')?m.nom:(r[13]||r[1]||'')).trim(),marque:String(m.marque||r[2]||'').trim(),ml,ty,
      pa:m.pa!=null&&m.pa!==''?+m.pa:n(r[12]),pvr:m.pvr!=null&&m.pvr!==''?+m.pvr:n(r[7]),pvw:m.pvw!=null&&m.pvw!==''?+m.pvw:n(r[8]),q:+q||0}; });
  return (_MLF=M);
}
/* le nom d'un parfum tel qu'il part dans le message : marque, nom, type, contenance (« 3.4 » devient « 3.4 oz ») */
function mlLib(f){
  const ml=/^\d+([.,]\d+)?$/.test(f.ml)?f.ml+' oz':f.ml;
  const nom=f.nom||'', avec=(x)=>x&&!new RegExp('\\b'+x.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')+'\\b','i').test(nom)?' '+x:'';
  return ((f.marque&&!nom.toLowerCase().startsWith(f.marque.toLowerCase())?f.marque+' ':'')+nom+avec(f.ty)+avec(ml)).replace(/\s+/g,' ').trim();
}

/* ---- le secteur d'une vente : wholesale, particulier, ou ni l'un ni l'autre ---- */
function mlSecteur(canal,f){
  const c=String(canal||'').toLowerCase();
  if(/amazon/.test(c)) return null;                                          /* Amazon interdit de démarcher ses acheteurs */
  if(/perfume ?(in the )?city|perfumecity|shopify/.test(c)) return null;     /* les clientes de Perfume City sont à Kim */
  if(/gros|wholesale/.test(c)||(f&&f.doc&&f.doc.fiscal==='resale')) return 'gros';
  return 'detail';
}

/* ---- TOUS les clients, réunis par le nom (comme la rubrique Clients) ---- */
let ML_CL=[];
function mlConstruit(){
  _MLF=null;
  const F=mlFiches(), M={};
  const get=nom=>{ nom=canon(String(nom||'').trim()); const k=cNorm(nom); if(!k) return null;
    return M[k]||(M[k]={nom,k,gros:false,detail:false,achats:[],co:{}}); };
  /* 1. le tableur de Sam : les commandes de gros d'avant l'ERP */
  const D=window.D_CLI||{clients:[]};
  (D.clients||[]).forEach(c=>{ const o=get(c.nom); if(!o) return; o.gros=true;
    (c.cmds||[]).forEach(x=>{ if(x.douteux||x.devis) return;
      o.achats.push({sec:'gros',d:x.d||'',L:(x.l||[]).map(l=>({cle:BC2CLE[bcN(l[0])]||'',q:+l[6]||0,p:l[5]==null?null:+l[5]}))}); }); });
  /* 2. les ventes de l'ERP (remboursées en entier : écartées) */
  let FACT=[]; try{ FACT=lit(KFACT,[])||[]; }catch(e){} if(!Array.isArray(FACT)) FACT=[];
  const RB={}; FACT.forEach(r=>{ if(r&&r.retour&&r.refId) RB[r.refId]=(RB[r.refId]||0)+Math.abs(+r.montant||0); });
  FACT.forEach(f=>{ if(!f||f.sens!=='vente'||f.retour||f.annule) return; if(f.doc&&(f.doc.offre||f.doc.type==='devis')) return;
    const nomC=(typeof faNomClient==='function')?faNomClient(f.tiers):(f.tiers&&f.tiers.nom)||f.tiers; if(!nomC) return;
    if(f.id&&(+f.montant||0)>0&&(RB[f.id]||0)>=(+f.montant||0)-0.01) return;
    const sec=mlSecteur(f.canal,f); if(!sec) return;
    const o=get(nomC); if(!o) return; o[sec]=true;
    o.achats.push({sec,d:f.d||'',L:(f.lignes||[]).map(l=>({cle:l.cle||BC2CLE[bcN(l.bc)]||'',q:+l.q||0,p:l.p==null?null:+l.p}))}); });
  /* 3. les coordonnées : la liste des clients du site, puis les fiches de l'ERP (elles l'emportent) */
  let RET=[]; try{ const t=lit(KRET,null); RET=Array.isArray(t)?t:(Array.isArray(window.D_RETAIL)?window.D_RETAIL:[]); }catch(e){}
  RET.forEach(r=>{ if(!r||!r.nom) return; const o=M[cNorm(canon(r.nom))]; if(!o) return;
    ['email','tel'].forEach(k=>{ if(r[k]&&!o.co[k]) o.co[k]=r[k]; }); });
  let CLI={}; try{ CLI=lit(KCLI,{})||{}; }catch(e){}
  Object.keys(CLI).sort((a,b)=>(canon(a)===a?1:0)-(canon(b)===b?1:0)).forEach(nom=>{ const c=CLI[nom]||{}; const o=M[cNorm(canon(nom))]; if(!o) return;
    ['email','tel','tel2','tel3','prenom','langue','nodiff','vip'].forEach(k=>{ if(c[k]) o.co[k]=c[k]; }); });
  /* 4. pour chacun : le nombre d'achats, le dernier achat, les parfums qu'on lui propose */
  ML_CL=Object.values(M).map(o=>{
    o.achats.sort((a,b)=>String(b.d).localeCompare(String(a.d)));
    o.sec=o.gros?'gros':(o.detail?'detail':null);
    const A=o.achats.filter(a=>a.sec===o.sec);
    o.nb=A.length; o.der=A.length?A[0].d:'';
    o.tel=[o.co.tel,o.co.tel2,o.co.tel3].map(v=>ctNum(v)).find(Boolean)||'';
    o.email=ctMail(o.co.email)?String(o.co.email).trim():'';
    const lg=String(o.co.langue||'').toLowerCase().slice(0,2); o.lg=['fr','en','es'].includes(lg)?lg:'en';
    o.prenom=String(o.co.prenom||'').trim()||(o.sec==='detail'?o.nom.split(/\s+/)[0]:o.nom);
    o.pf=[];
    if(o.sec==='detail'){
      /* le dernier parfum acheté qui est en stock (on remonte les achats, du plus récent au plus ancien) */
      for(const a of A){ const l=a.L.find(l=>F[l.cle]&&F[l.cle].q>0&&F[l.cle].pvr>0); if(l){ o.pf=[{f:F[l.cle],d:a.d,p:l.p}]; break; } }
    } else if(o.sec==='gros'){
      /* ses parfums les plus achetés (en flacons) qui sont en stock, avec le dernier prix qu'il a payé */
      const Q={}, DP={};
      A.forEach(a=>a.L.forEach(l=>{ if(!l.cle) return; Q[l.cle]=(Q[l.cle]||0)+l.q; if(DP[l.cle]==null&&l.p!=null) DP[l.cle]=l.p; }));
      o.pf=Object.keys(Q).filter(k=>F[k]&&F[k].q>0&&F[k].pvw>0).sort((a,b)=>Q[b]-Q[a]).slice(0,ML_NB_GROS).map(k=>({f:F[k],qt:Q[k],p:DP[k]}));
    }
    return o; }).filter(o=>o.sec);
  return ML_CL;
}

/* ---- le prix offert : la remise demandée, jamais sous le plancher ---- */
let REG={}; try{ REG=lit('reglages-v1',{})||{}; }catch(e){}
function mlPrix(f,sec,remise){
  const r=Math.max(0,Math.min(+remise||0,ML_PLAFOND))/100;
  if(sec==='gros'){
    const base=f.pvw; let p=Math.round(base*(1-r)*100)/100, plancher=null;
    if(f.pa!=null&&f.pa>0){ plancher=Math.ceil(f.pa*(1+ML_MARGE_GROS)*100)/100; if(p<plancher) p=plancher; }
    else p=base;
    if(p>base) p=base;
    return {base,p,plancher,bloque:r>0&&p>base*(1-r)+0.005};
  }
  const base=f.pvr;
  const site=(REG.canaux||[]).find(c=>c.id==='site')||{}, com=(site.com!=null&&site.com!==''&&+site.com>=0)?+site.com:2.9, fixe=(site.fixe!=null&&site.fixe!=='')?+site.fixe:0.3;
  const E=REG.envois||{}, envoi=(E.woocommerce==null||E.woocommerce===''||isNaN(+E.woocommerce))?8:Math.max(0,+E.woocommerce);
  let p=Math.round(base*(1-r)), plancher=null;
  if(f.pa!=null&&f.pa>0){ plancher=Math.ceil((f.pa+envoi+fixe+ML_MARGE_DETAIL)/(1-com/100)); if(p<plancher) p=plancher; }
  else p=base;   /* pas de prix d'achat connu : on ne sait pas jusqu'où descendre, donc pas de remise */
  if(p>base) p=base;
  return {base,p,plancher,bloque:r>0&&p>Math.round(base*(1-r))};
}

/* ---- l'offre en cours de chaque secteur, et qui l'a reçue ---- */
const ML_MSG={
 detail:{
  fr:"Bonjour {prenom},\n\nMerci d'avoir choisi Perfumes Trade. Le parfum que vous aviez pris chez nous est de nouveau disponible, avec un prix réservé à nos clients jusqu'au {fin} :\n\n{parfums}\n\nRépondez simplement à ce message pour le commander.\n\nPerfumes Trade",
  en:"Hello {prenom},\n\nThank you for choosing Perfumes Trade. The fragrance you bought from us is available again, at a price reserved for our customers until {fin}:\n\n{parfums}\n\nJust reply to this message to order it.\n\nPerfumes Trade",
  es:"Hola {prenom},\n\nGracias por elegir Perfumes Trade. El perfume que compró con nosotros está disponible de nuevo, con un precio reservado a nuestros clientes hasta el {fin}:\n\n{parfums}\n\nResponda a este mensaje para pedirlo.\n\nPerfumes Trade"},
 gros:{
  fr:"Bonjour {prenom},\n\nVos parfums habituels sont en stock à Miami. Prix valables jusqu'au {fin} :\n\n{parfums}\n\nEnvoyez-nous les quantités par WhatsApp, nous répondons dans la journée.\n\nPerfumes Trade",
  en:"Hello {prenom},\n\nYour usual fragrances are in stock in Miami. Prices valid until {fin}:\n\n{parfums}\n\nSend us the quantities on WhatsApp — we reply the same day.\n\nPerfumes Trade",
  es:"Hola {prenom},\n\nSus perfumes habituales están en stock en Miami. Precios válidos hasta el {fin}:\n\n{parfums}\n\nEnvíenos las cantidades por WhatsApp, respondemos el mismo día.\n\nPerfumes Trade"}};
const ML_AU_LIEU={fr:'au lieu de',en:'instead of',es:'en lugar de'};
const ML_LG={fr:'Français',en:'English',es:'Español'};
let ML=null;
function mlCharge(){
  let s={}; try{ s=lit(ML_K,{})||{}; }catch(e){}
  if(!s.offre) s.offre={}; if(!s.envois) s.envois={};
  ['gros','detail'].forEach(k=>{ if(!s.offre[k]) s.offre[k]={id:'',remise:k==='gros'?0:10,fin:'',msg:null}; });
  return s;
}
function mlSauve(){ try{ ecrit(ML_K,ML); }catch(e){} }
const ML_VUE={sec:'detail',gr:'',ap:{}};
const auj=()=>{ const d=new Date(); return d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0'); };
function mlFinDefaut(){ const d=new Date(Date.now()+7*864e5); return d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0'); }
const mlOffre=()=>{ const o=ML.offre[ML_VUE.sec]; if(!o.fin) o.fin=mlFinDefaut(); return o; };
const mlJours=d=>d?Math.floor((Date.now()-Date.parse(String(d).slice(0,10)+'T12:00:00'))/864e5):99999;
const dUS=d=>{ if(!d) return '—'; const [a,m,j]=String(d).slice(0,10).split('-'); return m+'/'+j+'/'+a.slice(2); };
const dMot=(d,lg)=>{ try{ return new Date(String(d).slice(0,10)+'T12:00:00').toLocaleDateString(lg==='fr'?'fr-FR':lg==='es'?'es-ES':'en-US',{day:'numeric',month:'long'}); }catch(e){ return d; } };
const pxMot=(v,lg)=>{ const s=(Math.round(v*100)%100)?v.toFixed(2):String(Math.round(v)); return lg==='fr'?s.replace('.',',')+' $':'$'+s; };

/* 15 nov. 2026 (Igal : « rajouter un lien pour qu'ils accèdent directement à leur parfum… et avoir l'analytique de ce qui s'est
   passé lorsqu'ils ont cliqué ») : chaque parfum du message porte le lien de SA page sur le site (perfumestrade.com pour un particulier,
   wholesale.perfumestrade.com pour un grossiste), avec une étiquette de suivi :
     utm_source=whatsapp · utm_medium=mailing · utm_campaign=<secteur>-<n° de l'offre> · utm_content=<code du client>
   Le code du client est un numéro calculé à partir de son nom (jamais son nom, son téléphone ni son email dans l'adresse) ; il est gardé
   avec l'envoi (mailing-v1) pour relier ensuite les visites (Google Analytics) et les commandes (attribution WooCommerce) au client.
   Vérifié le 15 nov. sur le site : l'adresse ?post_type=product&p=<n°> mène à la page du parfum en GARDANT l'étiquette. */
function mlCode(nom){ let h=2166136261; const t=cNorm(nom); for(let i=0;i<t.length;i++){ h^=t.charCodeAt(i); h=Math.imul(h,16777619)>>>0; } return 'c'+h.toString(36); }
function mlLienSite(f,sec,o){
  let S={}; try{ S=lit('site-stock-v1',{})||{}; }catch(e){}
  const cote=sec==='gros'?'g':'d', k0=String(f.bc||''), k=S[k0]?k0:Object.keys(S).find(x=>!x.startsWith('_')&&x.replace(/^0+/,'')===k0.replace(/^0+/,''));
  const e=k&&S[k], c=e&&e[cote]; if(!c||c.id==null||c.id===''||c.etat==='brouillon') return '';
  const B=(S._base&&typeof S._base==='object')?S._base:{}, base=String(B[cote]||(cote==='g'?'https://wholesale.perfumestrade.com':'https://perfumestrade.com')).replace(/\/+$/,'');
  const off=mlOffre(), camp=(sec==='gros'?'wholesale':'retail')+'-'+(off.id||'apercu');
  return base+'/?post_type=product&p='+encodeURIComponent(c.id)+'&utm_source=whatsapp&utm_medium=mailing&utm_campaign='+encodeURIComponent(camp)+'&utm_content='+mlCode(o.nom);
}
/* le message d'un client, dans SA langue, avec SES parfums */
function mlMessage(o){
  const off=mlOffre(), lg=o.lg, sec=ML_VUE.sec;
  let t=String((off.msg&&off.msg[lg])||ML_MSG[sec][lg]);
  const lignes=o.pf.map(x=>{ const P=mlPrix(x.f,sec,off.remise);
    const u=mlLienSite(x.f,sec,o);
    return '• '+mlLib(x.f)+' — '+pxMot(P.p,lg)+(P.p<P.base-0.005?' ('+ML_AU_LIEU[lg]+' '+pxMot(P.base,lg)+')':'')+(u?'\n'+u:''); }).join('\n');
  t=t.replace(/\{prenom\}/gi,o.prenom||'').replace(/\{fin\}/gi,dMot(off.fin,lg)).replace(/\{parfums\}/gi,lignes);
  if(!/\{parfums\}/i.test(String((off.msg&&off.msg[lg])||ML_MSG[sec][lg]))) t=t.replace(/\s+$/,'')+'\n\n'+lignes;
  return t.replace(/\s+$/,'')+'\n\n'+(typeof CT_STOP!=='undefined'?CT_STOP[lg]:'');
}

/* ---- qui est dans la liste ---- */
function mlListe(){
  const sec=ML_VUE.sec, gr=ML_VUE.gr;
  const S=ML_CL.filter(o=>o.sec===sec);
  const des=S.filter(o=>o.co.nodiff).length;
  const A=S.filter(o=>!o.co.nodiff);
  const sansPf=A.filter(o=>!o.pf.length).length;
  const B=A.filter(o=>o.pf.length);
  const sansCo=B.filter(o=>!o.tel&&!o.email).length;
  let L=B.filter(o=>o.tel||o.email);
  if(gr==='reg') L=L.filter(o=>o.nb>=2);
  else if(gr==='rachat') L=L.filter(o=>{ const j=mlJours(o.der); return j>=90&&j<=365; });
  else if(gr==='recent') L=L.filter(o=>mlJours(o.der)<90);
  else if(gr==='vip') L=L.filter(o=>o.co.vip);
  L.sort((a,b)=>(b.nb-a.nb)||String(b.der).localeCompare(String(a.der)));
  return {L,des,sansPf,sansCo,tous:S.length};
}
const mlEnvoye=o=>{ const id=mlOffre().id; return id&&ML.envois[id]&&ML.envois[id][o.nom]||null; };

/* ---- le dessin ---- */
function mlDessine(){
  const z=$('ml'); if(!z) return;
  const off=mlOffre(), sec=ML_VUE.sec, R=mlListe();
  const nSec=k=>ML_CL.filter(o=>o.sec===k&&!o.co.nodiff&&o.pf.length&&(o.tel||o.email)).length;
  const nWa=R.L.filter(o=>o.tel).length, nEm=R.L.filter(o=>o.email).length;
  const reste=R.L.filter(o=>o.tel&&!mlEnvoye(o)).length, faits=R.L.filter(o=>mlEnvoye(o)).length;
  const msgs=['fr','en','es'].map(lg=>`<div><div class="lab">${ML_LG[lg]}</div><textarea data-mlmsg="${lg}" data-nolang>${esc((off.msg&&off.msg[lg])||ML_MSG[sec][lg])}</textarea></div>`).join('');
  z.innerHTML=`
  <div class="mlseg">
    <button data-mlsec="gros" class="${sec==='gros'?'on':''}"><b>Wholesale</b><span>${T('Les grossistes','Wholesale customers','Los mayoristas')} · ${nSec('gros')} ${T('à contacter','to contact','por contactar')}</span></button>
    <button data-mlsec="detail" class="${sec==='detail'?'on':''}"><b>${T('Particuliers','Retail customers','Particulares')}</b><span>${T('Clients du site et de la boutique','Website and store customers','Clientes del sitio y de la tienda')} · ${nSec('detail')} ${T('à contacter','to contact','por contactar')}</span></button>
  </div>
  <div class="mlc"><h3><i>1</i>${T("L'offre","The offer","La oferta")}</h3>
    <div class="mlrow">
      <label>${T('Remise','Discount','Descuento')} <input type="number" id="ml-rem" min="0" max="${ML_PLAFOND}" step="1" value="${+off.remise||0}"> %</label>
      <label>${T("Valable jusqu'au",'Valid until','Válida hasta el')} <input type="date" id="ml-fin" value="${esc(off.fin)}"></label>
      <button class="btn" id="ml-neuve" type="button">${T('Nouvelle offre','New offer','Nueva oferta')}</button>
    </div>
    <p class="mlnote">${sec==='gros'
      ?T(`Chaque grossiste reçoit ses ${ML_NB_GROS} parfums les plus achetés qui sont en stock, au prix de gros. La remise ne descend jamais sous le prix d'achat + 5 %.`,`Each wholesale customer gets their ${ML_NB_GROS} most-bought fragrances that are in stock, at the wholesale price. The discount never goes below cost + 5%.`,`Cada mayorista recibe sus ${ML_NB_GROS} perfumes más comprados que están en stock, al precio mayorista. El descuento nunca baja del precio de compra + 5 %.`)
      :T(`Chaque client reçoit le dernier parfum qu'il a acheté et qui est en stock. La remise s'arrête au prix plancher du parfum : il reste toujours au moins ${ML_MARGE_DETAIL} $ par flacon, et jamais plus de ${ML_PLAFOND} % de remise. Sans prix d'achat dans l'ERP, pas de remise.`,`Each customer gets the last fragrance they bought that is in stock. The discount stops at the fragrance's floor price: at least $${ML_MARGE_DETAIL} always stays per bottle, and never more than ${ML_PLAFOND}% off. With no cost price in the ERP, no discount.`,`Cada cliente recibe el último perfume que compró y que está en stock. El descuento se detiene en el precio mínimo del perfume: siempre quedan al menos ${ML_MARGE_DETAIL} $ por frasco, y nunca más del ${ML_PLAFOND} % de descuento. Sin precio de compra en el ERP, no hay descuento.`)}</p>
    <details class="mlmsg"><summary>${T('Modifier le message (français, anglais, espagnol)','Edit the message (French, English, Spanish)','Modificar el mensaje (francés, inglés, español)')}</summary>
      <p class="mlnote">${T('{prenom} = le prénom du client, {parfums} = ses parfums avec leur prix, {fin} = la date de fin. La ligne pour se désinscrire est ajoutée toute seule.','{prenom} = the customer\'s first name, {parfums} = their fragrances with prices, {fin} = the end date. The unsubscribe line is added automatically.','{prenom} = el nombre del cliente, {parfums} = sus perfumes con su precio, {fin} = la fecha de fin. La línea para darse de baja se añade sola.')}</p>
      <div class="mlml">${msgs}</div>
      <button class="btn" id="ml-defaut" type="button" style="margin-top:8px">${T("Remettre le message d'origine",'Restore the original message','Restablecer el mensaje original')}</button>
    </details>
  </div>
  <div class="mlc"><h3><i>2</i>${T('Les clients','The customers','Los clientes')}</h3>
    <div class="mlrow"><label>${T('Qui','Who','Quién')} <select id="ml-gr">
      <option value="">${T('Tous','Everyone','Todos')}</option>
      <option value="reg">${T('Clients réguliers (2 achats ou plus)','Regular customers (2 purchases or more)','Clientes habituales (2 compras o más)')}</option>
      <option value="rachat">${T('Dernier achat il y a 3 à 12 mois','Last purchase 3 to 12 months ago','Última compra hace 3 a 12 meses')}</option>
      <option value="recent">${T('Achat récent (moins de 3 mois)','Recent purchase (less than 3 months)','Compra reciente (menos de 3 meses)')}</option>
      <option value="vip">${T('Favoris','Favorites','Favoritos')}</option></select></label></div>
    <p class="mlcpt"><b>${R.L.length}</b> ${T('clients','customers','clientes')} · ${nWa} ${T('avec WhatsApp','with WhatsApp','con WhatsApp')} · ${nEm} ${T('avec email','with email','con email')}${faits?` · <b style="color:var(--good)">${faits} ${T('déjà envoyés','already sent','ya enviados')}</b>`:''}
      <br><span class="mlnote">${T('Pas dans la liste','Not in the list','Fuera de la lista')} : ${R.des} ${T('désinscrits','unsubscribed','dados de baja')} · ${R.sansPf} ${T('sans parfum en stock à proposer','with no fragrance in stock to offer','sin perfume en stock que ofrecer')} · ${R.sansCo} ${T('sans numéro ni email (à compléter dans Clients)','with no number or email (to fill in Customers)','sin número ni email (completar en Clientes)')}</span></p>
    ${R.L.length?`<div class="mlwrap"><table class="mlt"><thead><tr>
      <th>${T('Client','Customer','Cliente')}</th><th>${T('Langue','Language','Idioma')}</th><th class="n">${T('Achats','Purchases','Compras')}</th><th class="n">${T('Dernier achat','Last purchase','Última compra')}</th>
      <th>${T('Parfums proposés et prix offert','Fragrances offered and offer price','Perfumes ofrecidos y precio ofrecido')}</th><th></th></tr></thead>
      <tbody>${R.L.map((o,i)=>{ const e=mlEnvoye(o);
        return `<tr class="${e?'fait':''}" data-mli="${i}">
        <td class="cl"><b data-nolang>${esc(o.nom)}</b><small data-nolang>${esc([o.tel?'+'+o.tel:'',o.email].filter(Boolean).join(' · '))}</small></td>
        <td><select data-mllg="${i}">${Object.keys(ML_LG).map(l=>`<option value="${l}"${l===o.lg?' selected':''}>${ML_LG[l]}</option>`).join('')}</select></td>
        <td class="n">${o.nb}</td><td class="n">${dUS(o.der)}</td>
        <td class="pf">${o.pf.map(x=>{ const P=mlPrix(x.f,sec,off.remise);
          /* pas de prix barré (Sam, 11 nov. 2026) : le prix habituel, une flèche, le prix offert */
          return `<div><span data-nolang>${esc(mlLib(x.f))}</span> <small>${sec==='gros'?`· ${x.qt} ${T('fl. achetés','bottles bought','fr. comprados')} · ${x.f.q} ${T('en stock','in stock','en stock')}`:`· ${T('acheté le','bought on','comprado el')} ${dUS(x.d)}`}</small>
            <span class="px">${P.p<P.base-0.005?`<span class="av">${money2(P.base)} →</span> <em>${money2(P.p)}</em>`:`<b>${money2(P.p)}</b>`}${P.bloque?` <span class="pl" title="${T('La remise est arrêtée au prix plancher de ce parfum','The discount stops at this fragrance\'s floor price','El descuento se detiene en el precio mínimo de este perfume')}">${T('plancher','floor','mínimo')}</span>`:''}</span></div>`; }).join('')}</td>
        <td class="act"><button class="btn wa" data-mlwa="${i}"${o.tel?'':' disabled'}>WhatsApp</button> <button class="btn" data-mlap="${i}">${T('Aperçu','Preview','Vista previa')}</button> <button class="btn" data-mlstop="${i}" title="${T('Le client a répondu STOP : il ne reçoit plus d\'offres, et WhatsApp s\'ouvre avec la réponse de remerciement','The customer replied STOP: no more offers, and WhatsApp opens with the thank-you reply','El cliente respondió STOP: no recibe más ofertas, y WhatsApp se abre con la respuesta de agradecimiento')}">${T('Désinscrire (STOP)','Unsubscribe (STOP)','Dar de baja (STOP)')}</button>
          ${e?`<span class="ok">${T('Envoyé le','Sent on','Enviado el')} ${dUS(e.t)} ${esc(e.h||'')} <button class="btn nenv" data-mlnon="${i}" title="${T('WhatsApp a été ouvert mais le message n\'est pas parti : la ligne redevient à envoyer','WhatsApp was opened but the message was not sent: the line goes back to « to send »','WhatsApp se abrió pero el mensaje no salió: la línea vuelve a « por enviar »')}">${T('Pas envoyé','Not sent','No enviado')}</button></span>`:''}</td></tr>
        ${ML_VUE.ap[o.nom]?`<tr class="ap"><td colspan="6"><pre data-nolang>${esc(mlMessage(o))}</pre></td></tr>`:''}`; }).join('')}</tbody></table></div>`
      :`<div class="mlvide">${T('Aucun client dans cette liste.','No customer in this list.','Ningún cliente en esta lista.')}</div>`}
  </div>
  <div class="mlc"><h3><i>3</i>${T('Envoyer','Send','Enviar')}</h3>
    <div class="mlgo">
      <button class="btn wa" id="ml-suiv"${reste?'':' disabled'}>${reste?T(`WhatsApp au client suivant (${reste} restant${reste>1?'s':''})`,`WhatsApp the next customer (${reste} left)`,`WhatsApp al siguiente cliente (${reste>1?'quedan':'queda'} ${reste})`):T('Tous les WhatsApp de cette liste sont envoyés','All WhatsApp messages in this list are sent','Todos los WhatsApp de esta lista están enviados')}</button>
      <button class="btn" id="ml-csv"${nEm?'':' disabled'}>${T(`Fichier pour Klaviyo ou Brevo (${nEm} email${nEm>1?'s':''})`,`File for Klaviyo or Brevo (${nEm} email${nEm>1?'s':''})`,`Archivo para Klaviyo o Brevo (${nEm} email${nEm>1?'s':''})`)}</button>
      <span class="msg" id="ml-msgx"></span>
    </div>
    <p class="mlnote">${T("WhatsApp : un message à la fois, chacun avec son prénom et ses parfums. WhatsApp s'ouvre avec le texte prêt ; appuie sur Envoyer, puis reviens ici pour le suivant. Envoie par petits groupes, seulement à des clients qui ont déjà acheté : si trop de gens bloquent ou signalent le numéro, WhatsApp peut le restreindre.","WhatsApp: one message at a time, each with the customer's first name and fragrances. WhatsApp opens with the text ready; press Send, then come back here for the next one. Send in small batches, only to customers who have already bought: if too many people block or report the number, WhatsApp can restrict it.","WhatsApp: un mensaje a la vez, cada uno con el nombre y los perfumes del cliente. WhatsApp se abre con el texto listo; pulsa Enviar y vuelve aquí para el siguiente. Envía en grupos pequeños, solo a clientes que ya compraron: si demasiadas personas bloquean o denuncian el número, WhatsApp puede restringirlo.")}</p>
    <p class="mlnote">${T("Emails : pas d'envoi en masse depuis Gmail, c'est le plus sûr moyen de finir en spam, et la boîte qui envoie les factures pourrait être bloquée. Le fichier s'importe dans Klaviyo ou Brevo, qui ajoutent le lien de désinscription. Avant le premier envoi, le domaine perfumestrade.com doit être authentifié dans l'outil (lignes DNS à poser par Sam).","Emails: no bulk sending from Gmail — it is the surest way to end up in spam, and the mailbox that sends the invoices could be blocked. The file imports into Klaviyo or Brevo, which add the unsubscribe link. Before the first send, the perfumestrade.com domain must be authenticated in the tool (DNS records for Sam to add).","Emails: nada de envíos masivos desde Gmail — es la forma más segura de acabar en spam, y el buzón que envía las facturas podría bloquearse. El archivo se importa en Klaviyo o Brevo, que añaden el enlace de baja. Antes del primer envío, el dominio perfumestrade.com debe estar autenticado en la herramienta (registros DNS que Sam debe añadir).")}</p>
  </div>`;
  const g=$('ml-gr'); if(g) g.value=ML_VUE.gr;
}

/* ---- les gestes ---- */
function mlLance(url){ window.__mlDernier=url; const a=document.createElement('a'); a.href=url; a.target='_blank'; a.rel='noopener'; document.body.appendChild(a); a.click(); a.remove(); }
function mlJournal(lib,ref){ try{ const J=lit(KJOU,[])||[]; J.push({t:new Date().toISOString(),u:USR||'(non renseigné)',act:'contact',lib,ref,av:null,ap:'mailing'}); ecrit(KJOU,J); }catch(e){} }
function mlDit(t,c){ const e=$('ml-msgx'); if(!e) return; e.textContent=t; e.className='msg '+(c||'ok'); }
function mlEnvoieWa(o){
  if(!o||!o.tel) return;
  const off=mlOffre();
  if(!off.id){ off.id='o'+Date.now().toString(36); off.t=new Date().toISOString(); off.u=USR||''; }
  /* 15 nov. 2026 (Igal) : toujours WhatsApp WEB — le lien wa.me pouvait ouvrir l'application WhatsApp du Mac, à un autre nom que celui
     de l'entreprise ; WhatsApp Web montre le compte branché par le QR code (comme les New Arrivals) */
  mlLance('https://web.whatsapp.com/send?phone='+o.tel+'&text='+encodeURIComponent(mlMessage(o)));
  const E=ML.envois[off.id]=ML.envois[off.id]||{};
  E[o.nom]={t:auj(),h:(typeof heureMiami==='function'?heureMiami(new Date().toISOString()):''),u:USR||'',par:'whatsapp',sec:ML_VUE.sec,code:mlCode(o.nom)};
  mlSauve();
  mlJournal('offre envoyée par WhatsApp (Mailing '+(ML_VUE.sec==='gros'?'Wholesale':'Particuliers')+', remise '+(+off.remise||0)+' %, '+o.pf.length+' parfum'+(o.pf.length>1?'s':'')+')',o.nom);
  mlDessine();
  mlDit(T('WhatsApp ouvert pour ','WhatsApp opened for ','WhatsApp abierto para ')+o.nom+T(" — appuie sur Envoyer dans WhatsApp."," — press Send in WhatsApp."," — pulsa Enviar en WhatsApp."));
}
function mlCsv(){
  const R=mlListe(), off=mlOffre(), sec=ML_VUE.sec;
  const L=R.L.filter(o=>o.email);
  if(!L.length) return;
  const q=v=>{ const s=String(v==null?'':v); return /[",\n;]/.test(s)?'"'+s.replace(/"/g,'""')+'"':s; };
  const ent=['Email','FirstName','Language','Segment','Product','UsualPrice','OfferPrice','OfferEnds','Orders','LastOrder'];
  const lignes=L.map(o=>{ const x=o.pf[0], P=mlPrix(x.f,sec,off.remise);
    return [o.email,o.prenom,o.lg,sec==='gros'?'wholesale':'retail',mlLib(x.f),P.base.toFixed(2),P.p.toFixed(2),off.fin,o.nb,o.der].map(q).join(','); });
  const txt=ent.join(',')+'\r\n'+lignes.join('\r\n')+'\r\n';
  window.__mlCsv=txt;
  const a=document.createElement('a'); a.href=URL.createObjectURL(new Blob([txt],{type:'text/csv;charset=utf-8'}));
  a.download='mailing-'+(sec==='gros'?'wholesale':'particuliers')+'-'+auj()+'.csv'; document.body.appendChild(a); a.click(); a.remove();
  mlJournal('fichier email préparé pour Klaviyo ou Brevo (Mailing '+(sec==='gros'?'Wholesale':'Particuliers')+', '+L.length+' adresses)','');
  mlDit(T(L.length+' adresses dans le fichier. Importe-le dans Klaviyo ou Brevo.',L.length+' addresses in the file. Import it into Klaviyo or Brevo.',L.length+' direcciones en el archivo. Impórtalo en Klaviyo o Brevo.'));
}
/* 15 nov. 2026 (Igal : « si le client répond STOP, qu'on puisse lui répondre qu'on a bien compris, qu'on lui souhaite une bonne
   continuation et qu'il est toujours le bienvenu ») : WhatsApp Web ne laisse pas l'ERP lire les réponses — c'est la personne qui voit
   le STOP et clique « Désinscrire (STOP) ». L'ERP le retire alors de toutes les offres (la même case que la liste de diffusion de
   Clients) et ouvre WhatsApp avec la réponse toute prête, dans la langue du client. */
const ML_STOP_REP={
  fr:"Bonjour {prenom},\n\nC'est bien noté : vous ne recevrez plus nos offres. Merci pour votre confiance, et très bonne continuation. Vous serez toujours le bienvenu chez Perfumes Trade.\n\nPerfumes Trade",
  en:"Hello {prenom},\n\nNoted: you will no longer receive our offers. Thank you for your trust, and all the best. You are always welcome at Perfumes Trade.\n\nPerfumes Trade",
  es:"Hola {prenom},\n\nQueda anotado: ya no recibirá nuestras ofertas. Gracias por su confianza, y que le vaya muy bien. Siempre será bienvenido en Perfumes Trade.\n\nPerfumes Trade"};
const mlStopTexte=o=>ML_STOP_REP[o.lg]?ML_STOP_REP[o.lg].replace(/\{prenom\}/g,o.prenom||''):ML_STOP_REP.en.replace(/\{prenom\}/g,o.prenom||'');
function mlStop(o){
  if(!o) return;
  if(!confirm(T(o.nom+' ne recevra plus jamais d\'offres. Continuer ?',o.nom+' will never receive offers again. Continue?',o.nom+' no volverá a recibir ofertas. ¿Continuar?'))) return;
  let C={}; try{ C=lit(KCLI,{})||{}; }catch(e){}
  C[o.nom]=Object.assign({},C[o.nom]||{},{nom:o.nom,nodiff:true,maj:new Date().toISOString()}); ecrit(KCLI,C);
  mlJournal('client désinscrit des offres (Mailing — STOP)',o.nom);
  if(o.tel) mlLance('https://web.whatsapp.com/send?phone='+o.tel+'&text='+encodeURIComponent(mlStopTexte(o)));
  mlConstruit(); mlDessine();
  mlDit(o.tel?T(o.nom+' est désinscrit. WhatsApp est ouvert avec la réponse prête : appuie sur Envoyer.',o.nom+' is unsubscribed. WhatsApp is open with the reply ready: press Send.',o.nom+' está dado de baja. WhatsApp está abierto con la respuesta lista: pulsa Enviar.'):T(o.nom+' est désinscrit.',o.nom+' is unsubscribed.',o.nom+' está dado de baja.'));
}
function mlLangue(o,lg){
  let C={}; try{ C=lit(KCLI,{})||{}; }catch(e){}
  C[o.nom]=Object.assign({},C[o.nom]||{},{nom:o.nom,langue:lg,maj:new Date().toISOString()}); ecrit(KCLI,C);   /* la langue du client est retenue */
  o.lg=lg; mlDessine();
}
document.addEventListener('click',e=>{
  const z=$('ml'); if(!z||!z.contains(e.target)) return;
  const R=()=>mlListe().L;
  const s=e.target.closest('[data-mlsec]'); if(s){ ML_VUE.sec=s.dataset.mlsec; ML_VUE.ap={}; mlDessine(); return; }
  const w=e.target.closest('[data-mlwa]'); if(w){ mlEnvoieWa(R()[+w.dataset.mlwa]); return; }
  const p=e.target.closest('[data-mlap]'); if(p){ const o=R()[+p.dataset.mlap]; if(o){ ML_VUE.ap[o.nom]=!ML_VUE.ap[o.nom]; mlDessine(); } return; }
  const x=e.target.closest('[data-mlstop]'); if(x){ mlStop(R()[+x.dataset.mlstop]); return; }
  /* 15 nov. 2026 (Igal : « j'ai fait un test, je ne l'ai pas envoyé, mais la ligne reste en vert ») : WhatsApp s'ouvre, mais c'est
     dans WhatsApp qu'on appuie sur Envoyer — si le message n'est pas parti, « Pas envoyé » efface la marque, la ligne redevient à envoyer */
  const nn=e.target.closest('[data-mlnon]'); if(nn){ const o=R()[+nn.dataset.mlnon], id=mlOffre().id;
    if(o&&id&&ML.envois[id]&&ML.envois[id][o.nom]){ delete ML.envois[id][o.nom]; mlSauve();
      mlJournal('envoi marqué « pas envoyé » (Mailing '+(ML_VUE.sec==='gros'?'Wholesale':'Particuliers')+')',o.nom); mlDessine();
      mlDit(T(o.nom+' : marqué « pas envoyé ».',o.nom+': marked « not sent ».',o.nom+': marcado « no enviado ».')); } return; }
  if(e.target.closest('#ml-suiv')){ const o=R().find(o=>o.tel&&!mlEnvoye(o)); if(o) mlEnvoieWa(o); return; }
  if(e.target.closest('#ml-csv')){ mlCsv(); return; }
  if(e.target.closest('#ml-defaut')){ mlOffre().msg=null; mlSauve(); mlDessine(); const d=document.querySelector('.mlmsg'); if(d) d.open=true; return; }
  if(e.target.closest('#ml-neuve')){
    if(!confirm(T('Commencer une nouvelle offre ? Les envois de l\'offre en cours restent notés au Journal, et tous les clients pourront recevoir la nouvelle.','Start a new offer? Sends of the current offer stay recorded in the Log, and every customer can receive the new one.','¿Empezar una nueva oferta? Los envíos de la oferta actual quedan anotados en el Diario, y todos los clientes podrán recibir la nueva.'))) return;
    const o=mlOffre(); o.id=''; o.fin=mlFinDefaut(); mlSauve(); mlDessine(); return; }
});
document.addEventListener('change',e=>{
  const z=$('ml'); if(!z||!z.contains(e.target)) return;
  const t=e.target;
  if(t.id==='ml-rem'){ mlOffre().remise=Math.max(0,Math.min(ML_PLAFOND,Math.round(+t.value||0))); mlSauve(); mlDessine(); return; }
  if(t.id==='ml-fin'){ mlOffre().fin=t.value||mlFinDefaut(); mlSauve(); mlDessine(); return; }
  if(t.id==='ml-gr'){ ML_VUE.gr=t.value; mlDessine(); return; }
  if(t.dataset.mllg!=null){ const o=mlListe().L[+t.dataset.mllg]; if(o) mlLangue(o,t.value); return; }
  if(t.dataset.mlmsg){ const off=mlOffre(); const sec=ML_VUE.sec; off.msg=off.msg||{fr:ML_MSG[sec].fr,en:ML_MSG[sec].en,es:ML_MSG[sec].es}; off.msg[t.dataset.mlmsg]=t.value; mlSauve(); return; }
});

/* les administrateurs de l'ERP : les rôles Admin et Patron, et eux seuls (comme l'Analytique) */
function mlAdmin(){ const s=session(); return !!s&&/^(admin|patron)$/.test(String(s.role||'')); }
window.__ml={mlStopTexte,mlConstruit,mlListe,mlPrix,mlMessage,mlDessine,ML_VUE,CL:()=>ML_CL,ETAT:()=>ML};
try{ piedSession(); }catch(e){}
(function(){
  const s=session(); if(!s) return;
  if(!mlAdmin()){
    document.querySelector('.wrap').insertAdjacentHTML('beforeend',`<div class="mur"><h2>${T('Cette rubrique n\'est pas pour ce rôle','This section is not for this role','Esta sección no es para este rol')}</h2><p>${T('Le Mailing est réservé aux administrateurs de l\'ERP.','Mailing is for the ERP administrators only.','El Mailing está reservado a los administradores del ERP.')}</p></div>`);
    const a=$('ml'); if(a) a.remove(); try{ $('src').innerHTML=T('accès refusé','access denied','acceso denegado'); }catch(e){} return;
  }
  ML=mlCharge(); mlConstruit(); mlDessine();
  try{ $('src').innerHTML=T('clients, ventes et stock<br>de l\'ERP, en direct','ERP customers, sales<br>and stock, live','clientes, ventas y stock<br>del ERP, en directo'); }catch(e){}
  /* une vente, une fiche client ou un stock qui change ailleurs (autre poste, cockpit) : la liste se refait */
  const CLES=[KFACT,KCLI,KRET,ML_K,'fiches-modifiees-v1','stock-externe-v1','articles-ajoutes-v1'];
  const relit=()=>{ try{ ML=mlCharge(); REG=lit('reglages-v1',{})||{}; }catch(_){} mlConstruit(); mlDessine(); };
  window.addEventListener('ck-maj',e=>{ const c=(e.detail&&e.detail.cles)||[]; if(c.some(k=>CLES.includes(k))&&!(document.activeElement&&document.activeElement.closest&&document.activeElement.closest('#ml textarea'))) relit(); });
  window.addEventListener('storage',e=>{ if(CLES.includes(e.key)) relit(); });
})();
'''

html = coquille("Mailing", "Mailing",
  "Envoyer une offre à chaque secteur : les grossistes et les particuliers, chacun avec ses parfums et dans sa langue. Réservé aux administrateurs de l'ERP.",
  CSS, CORPS, JS.replace('__ALIAS__', ALIAS), donnees=('produits', 'clients', 'retail'))
html = html.replace('__BC2CLE__',
  'Object.fromEntries(D_TOUS().filter(r=>r[0]).map(r=>[String(r[0]).replace(/[^0-9A-Za-z]/g,\'\').replace(/^0+/,\'\'),r[15]]))')
open('mailing.html', 'w').write(html)
print('mailing.html', len(html)//1024, 'Ko')
