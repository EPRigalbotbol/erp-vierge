/* ===== PRICE LIST EN DIRECT (15 nov. 2026) : le tableau que le cockpit montre aux clients de gros autorisés =====
   Une ligne par fiche : [code-barres, marque, nom, contenance, type, genre, prix de gros, quantité, photo, dernier arrivage, clé].
   Seulement les fiches en stock, avec un prix de gros (prixCanal du canal wholesale, comme sur le site de gros) et pas coupées
   du canal wholesale. JAMAIS le prix d'achat. La photo : celle du site (adresse complète) ; une photo prise par Sam part sous la
   forme « perso:<clé> », que le cockpit sert lui-même (photos-perso-v1) ; sans photo, la page met un flacon dessiné.
   Le dernier arrivage : la date de la dernière facture d'achat qui contient la fiche (onglet « Just arrived » de la page).
   Publié à l'ouverture du Catalogue et 3 s après chaque enregistrement d'une fiche, d'un parfum ajouté, d'une photo ou des
   réglages — par le Patron ou un admin seulement, et seulement quand le tableau a changé. La quantité vivante, elle, suit le
   tableau du stock (stock-erp-v1) que l'ERP publie à chaque vente. */
let _PL_T=null;
const plNz=s=>String(s||'').replace(/[^0-9A-Za-z]/g,'').replace(/^0+/,'');
function plArrivages(){
  const M={}; let F=[]; try{ F=lit('factures-v1',[])||[]; }catch(e){}
  (Array.isArray(F)?F:[]).forEach(f=>{ if(!f||f.sens!=='achat'||f.annule||!f.d) return;
    (f.lignes||[]).forEach(l=>{ if(!l||!(+l.q>0)) return;
      [l.cle?'k:'+l.cle:'', l.bc?'b:'+plNz(l.bc):''].filter(k=>k&&k!=='b:').forEach(k=>{ if(!M[k]||f.d>M[k]) M[k]=f.d; }); }); });
  return M;
}
function plTableau(){
  const C=canaux(), cg=C.find(c=>c.id==='sitegros'), A=plArrivages(), L=[];
  if(!cg) return {t:new Date().toISOString(),L};
  tousLesArticles().forEach(p=>{
    if(!p||!p.bc) return;
    const q=Math.floor(+p.qte||0); if(!(q>0)) return;
    if(horsCanal(p,'sitegros')) return;
    const px=prixCanal(p,cg).v; if(!(px>0)) return;
    const k=String(p.id||p.cle||'');
    let img='';
    if(p.imgPerso) img='perso:'+(p.id||k);
    else if(/^https:\/\//.test(p.img||'')) img=p.img;
    else if(/^http:\/\//.test(p.img||'')) img='https://'+String(p.img).slice(7);
    const arr=A['k:'+k]||A['b:'+plNz(p.bc)]||'';
    L.push([String(p.bc),String(p.marque||''),String(p.nom||''),String(p.ml||''),String(p.type||''),String(p.genre||''),Math.round(px*100)/100,q,img,arr,k]);
  });
  return {t:new Date().toISOString(),L};
}
function plPublie(){
  try{ if(typeof peutPrixSite!=='function'||!peutPrixSite()) return;   /* Patron / admin : ceux qui fixent les prix */
    const T=plTableau(), av=lit('pricelist-v1',null);
    if(av&&Array.isArray(av.L)&&JSON.stringify(av.L)===JSON.stringify(T.L)) return;   /* rien n'a changé : on ne réveille pas le cockpit */
    ecrit('pricelist-v1',T);
  }catch(e){ try{ console.warn('price list non publiée',e); }catch(_){} }
}
(function(){
  setTimeout(plPublie,5000);
  try{ if(Array.isArray(window._apresEcrit)) window._apresEcrit.push(cle=>{
    if(!['fiches-modifiees-v1','reglages-v1','articles-ajoutes-v1','photos-perso-v1'].includes(cle)) return;
    clearTimeout(_PL_T); _PL_T=setTimeout(plPublie,3000); }); }catch(e){}
})();
