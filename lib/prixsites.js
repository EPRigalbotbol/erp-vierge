/* ===== PRIX DES FICHES → SITES (10 nov. 2026) : le tableau que le cockpit suit pour égaliser les prix =====
   p : { code du produit sur le site : [prix détail, prix gros] } — le prix que le client doit payer d'après la fiche (prixCanal),
   null quand le canal est coupé pour ce parfum ou sans prix. Un code partagé par plusieurs fiches (boîte / NOBOX / tester) : la fiche
   qui porte la même mention que le produit du site ; si plusieurs fiches restent avec des prix différents, le code n'est pas publié
   (« amb ») — le cockpit ne devine jamais. Publié à l'ouverture du Catalogue et 3 s après chaque enregistrement d'une fiche ;
   jamais à la réception d'une donnée d'un autre poste (une page restée ouverte ne republie pas un état ancien). */
let _PX_T=null;
function prixSitesTableau(){
  const C=canaux(), cs=C.find(c=>c.id==='site'), cg=C.find(c=>c.id==='sitegros'), parK={};
  tousLesArticles().forEach(p0=>{ if(!p0.bc) return; const k=siteCle(p0); if(!k) return; (parK[k]=parK[k]||[]).push(applique(p0)); });
  const men=(typeof nomMention==='function')?nomMention:(()=>'');
  const p={}, amb=[];
  for(const k in parK){
    let P=parK[k];
    if(P.length>1){ const e=SITE[k], f=e&&(e.d||e.g), m=men(String(k).replace(/[0-9]/g,'')+' '+((f&&f.nom)||''));
      const a=P.filter(x=>men(String(x.bc||'').replace(/[0-9]/g,'')+' '+(x.nom||'')+' '+(x.nomSrc||''))===m); if(a.length) P=a; }
    const v=(c)=>{ if(!c) return null; const L=[...new Set(P.map(x=>horsCanal(x,c.id)?'off':(prixCanal(x,c).v>0?Math.round(prixCanal(x,c).v*100)/100:'0')))];
      if(L.length!==1) return 'amb'; return (L[0]==='off'||L[0]==='0')?null:L[0]; };
    const d=v(cs), g=v(cg);
    if(d==='amb'||g==='amb'){ amb.push(k); continue; }
    if(d==null&&g==null) continue;
    p[k]=[d,g];
  }
  return {t:new Date().toISOString(),p,amb};
}
/* 16 nov. 2026 (Igal : « les prix de référence sont ceux de perfumestrade… il faut que tout soit pareil » ; « quand Sam change un
   prix, prix d'achat ou prix de vente, il faut que ça change chez Perfume City aussi ») : le tableau que le cockpit suit pour
   Perfume City (Shopify), par code-barres : [prix de vente de perfumestrade.com, prix d'achat]. Un code porté par plusieurs
   fiches qui ne disent pas la même chose est mis à part (« amb ») : le cockpit n'y touche jamais. Une fiche coupée du canal
   Perfume City n'y est pas. */
function prixPcTableau(){
  const C=canaux(), cs=C.find(c=>c.id==='site'), G={};
  const nz=s=>String(s||'').replace(/[^0-9A-Za-z]/g,'').replace(/^0+/,'');
  tousLesArticles().forEach(p0=>{ const k=nz(p0.bc); if(!k) return; const p=p0; if(horsCanal(p,'perfumecity')) return;
    const v=prixCanal(p,cs).v, pa=+p.pa||0;
    (G[k]=G[k]||new Set()).add(JSON.stringify([v>0?Math.round(v*100)/100:null, pa>0?Math.round(pa*100)/100:null])); });
  const p={}, amb=[];
  for(const k in G){ if(G[k].size>1){ amb.push(k); continue; } const L=JSON.parse([...G[k]][0]); if(L[0]==null&&L[1]==null) continue; p[k]=L; }
  return {t:new Date().toISOString(),p,amb};
}
function prixPcPublie(){
  try{ if(typeof peutPrixSite!=='function'||!peutPrixSite()) return;
    const T=prixPcTableau(), av=lit('prix-pc-v1',null);
    if(av&&av.p&&JSON.stringify(av.p)===JSON.stringify(T.p)&&JSON.stringify(av.amb||[])===JSON.stringify(T.amb)) return;
    ecrit('prix-pc-v1',T);
  }catch(e){ try{ console.warn('prix de Perfume City non publiés',e); }catch(_){} }
}
function prixSitesPublie(){
  prixPcPublie();   /* Perfume City d'abord : il ne dépend pas du relevé des sites */
  try{ if(typeof peutPrixSite!=='function'||!peutPrixSite()) return;   /* Patron / admin : ceux qui ont le droit de changer un prix des sites */
    if(!SITE._maj) return;                                                /* le relevé des sites n'est pas encore lu : rien à comparer */
    const T=prixSitesTableau(), av=lit('prix-erp-v1',null);
    if(av&&av.p&&JSON.stringify(av.p)===JSON.stringify(T.p)) return;   /* rien n'a changé : on ne réveille pas le cockpit */
    ecrit('prix-erp-v1',T);
  }catch(e){ try{ console.warn('prix des sites non publiés',e); }catch(_){} }
}
(function(){
  setTimeout(prixSitesPublie,4000);
  try{ if(Array.isArray(window._apresEcrit)) window._apresEcrit.push(cle=>{ if(cle!=='fiches-modifiees-v1'&&cle!=='reglages-v1') return; clearTimeout(_PX_T); _PX_T=setTimeout(prixSitesPublie,3000); }); }catch(e){}
})();
/* 15 nov. 2026 : la price list en direct des clients de gros (lib/pricelist.js, voir _pricelist.py) se charge d'ici, à la même
   version que ce fichier — catalogue.html est à quelques octets de son plafond d'un million */
try{ const v=((document.currentScript&&document.currentScript.src)||'').split('?')[1]||''; const sc=document.createElement('script'); sc.src='lib/pricelist.js'+(v?'?'+v:''); document.head.appendChild(sc); }catch(e){}
