# LES PRIX DES FICHES, PUBLIÉS POUR LES SITES (Igal, 10 nov. 2026 : « je ne veux pas qu'il y ait un bouton pour mettre à jour les
# prix et le stock, je veux que cela soit fait automatiquement »). Le stock l'était déjà (stock-erp-v1, égalisé par le cockpit toutes
# les 5 minutes). Ici, la même chose pour les prix : le Catalogue publie, pour chaque produit des deux sites, le prix que le client
# doit payer d'après la fiche (prix-erp-v1) ; le cockpit compare et remet les sites au niveau tout seul (woocommerce.js, egalisePrix).
# Écrit dans lib/prixsites.js à chaque construction du Catalogue (build_html.py), chargé par la page.
import pathlib

JS = r'''/* ===== PRIX DES FICHES → SITES (10 nov. 2026) : le tableau que le cockpit suit pour égaliser les prix =====
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
function prixSitesPublie(){
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
'''

def ecrit(dossier):
    d = pathlib.Path(dossier) / 'lib'; d.mkdir(exist_ok=True)
    (d / 'prixsites.js').write_text(JS, encoding='utf-8')
