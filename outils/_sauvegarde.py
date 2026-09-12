# -*- coding: utf-8 -*-
"""Sauvegarde automatique, sur toutes les pages.

Tant que SAM tourne dans le navigateur, tout ce qui est saisi vit dans ce
navigateur et nulle part ailleurs. Un nettoyage d'historique, un autre poste,
un profil effacé, et le travail est perdu.

Avant : un bouton de sauvegarde dans une seule page, et un rappel au bout de
sept jours qu'on pouvait ignorer.
Maintenant : un témoin visible sur les dix pages, et un fichier téléchargé
automatiquement une fois par jour dès qu'il y a du travail non sauvegardé.
"""

SAUVE = r"""
/* ============ SAUVEGARDE AUTOMATIQUE ============ */
const SV_CLES=['fiches-modifiees-v1','articles-ajoutes-v1','stock-externe-v1','comptage-parfums-v1',
  'crm-journal-v1','prix-achat-hist-v1','marche-v1','fournisseurs-v1','factures-installees-v1',
  'factures-v1','ventes-v1','clients-v1','reglements-v1','commandes-v1','connecteurs-v1',
  'ventes-numeros-v1','ajustements-v1','reglages-v1','crm-utilisateur-v1','crm-utilisateurs-v1',
  'sheet-installe-2026-09-03','repere-installation-v1','derniere-sauvegarde-compte-v1'];
const SV_DATE='derniere-sauvegarde-v1';
const SV_AUTO='derniere-sauvegarde-auto-v1';
const SV_REPERE='repere-installation-v1';

const _svLit=k=>{ try{ const t=localStorage.getItem(k); return t==null?null:JSON.parse(t); }catch(e){ return null; } };
const _svN={
  'fiches-modifiees-v1':v=>Object.keys(v||{}).length,
  'articles-ajoutes-v1':v=>(v||[]).length,
  'stock-externe-v1':v=>Object.keys((v&&v.q)||{}).length,
  'comptage-parfums-v1':v=>Object.keys(v||{}).length,
  'crm-journal-v1':v=>(v||[]).length,
  'prix-achat-hist-v1':v=>Object.values(v||{}).reduce((a,l)=>a+(l||[]).length,0),
  'marche-v1':v=>Object.keys(v||{}).length,
  'fournisseurs-v1':v=>Object.keys(v||{}).length,
  'factures-v1':v=>(v||[]).length,
  'ventes-v1':v=>Object.values(v||{}).reduce((a,l)=>a+(l||[]).length,0),
  'clients-v1':v=>Object.keys(v||{}).length,
  'reglements-v1':v=>Object.keys(v||{}).length,
  'ajustements-v1':v=>(v||[]).length};
const SV_COMPTE='derniere-sauvegarde-compte-v1';
/* Les compteurs de chaque magasin, à l'instant présent. */
function svCompte(){
  const o={}; Object.entries(_svN).forEach(([k,f])=>{ o[k]=f(_svLit(k)); }); return o;
}
/* Ce qui a changé DEPUIS LA DERNIÈRE SAUVEGARDE — c'est ça qui serait perdu.
   S'il n'y a jamais eu de sauvegarde, on part de ce que les fichiers ont installé
   eux-mêmes : ces données-là se réinstallent seules et ne peuvent pas être perdues. */
function svSaisies(){
  const ref=_svLit(SV_COMPTE)||_svLit(SV_REPERE)||{};
  const now=svCompte();
  let n=0;
  Object.keys(now).forEach(k=>{ n+=Math.abs(now[k]-(+ref[k]||0)); });
  return n;
}
function svPaquet(){
  /* on range les valeurs déjà décodées, comme le fait la fenêtre de sauvegarde :
     le fichier reste lisible et la restauration existante le comprend sans rien changer */
  const d={};
  SV_CLES.forEach(k=>{ try{ const t=localStorage.getItem(k); if(t==null) return;
    let v; try{ v=JSON.parse(t); }catch(e){ v=t; }
    d[k]=v; }catch(e){} });
  return {format:'crm-parfums-sauvegarde',version:1,le:new Date().toISOString(),
          par:(function(){try{return localStorage.getItem('crm-utilisateur-v1')||'';}catch(e){return '';}})(),
          saisies:svSaisies(), donnees:d};
}
function svTelecharge(auto){
  try{
    const p=svPaquet();
    const b=new Blob([JSON.stringify(p,null,1)],{type:'application/json'});
    const a=document.createElement('a');
    const d=new Date(), z=n=>String(n).padStart(2,'0');
    a.href=URL.createObjectURL(b);
    a.download='sam-sauvegarde-'+d.getFullYear()+'-'+z(d.getMonth()+1)+'-'+z(d.getDate())
               +(auto?'':'-'+z(d.getHours())+z(d.getMinutes()))+'.json';
    document.body.appendChild(a); a.click(); a.remove();
    setTimeout(()=>URL.revokeObjectURL(a.href),4000);
    try{ localStorage.setItem(SV_DATE,String(Date.now()));
         localStorage.setItem(SV_COMPTE,JSON.stringify(svCompte()));
         if(auto) localStorage.setItem(SV_AUTO,ajd()); }catch(e){}
    svTemoin();
    return true;
  }catch(e){ return false; }
}

/* le témoin, en bas à gauche, sur toutes les pages */
function svTemoin(){
  let el=document.getElementById('svtem');
  const n=svSaisies();
  /* en ligne, les données vivent sur le serveur : le rappel de sauvegarde n'a plus lieu d'être
     (le fichier reste disponible dans Réglages pour qui veut une copie) */
  if(typeof _SY_ON!=='undefined'&&_SY_ON){ if(el) el.remove(); return; }
  if(n<5){ if(el) el.remove(); return; }
  let d=0; try{ d=+(localStorage.getItem(SV_DATE)||0); }catch(e){}
  const j = d ? Math.floor((Date.now()-d)/86400000) : null;
  const tard = j===null || j>=2;
  if(!el){
    el=document.createElement('div'); el.id='svtem';
    document.body.appendChild(el);
  }
  /* à droite : à gauche, le témoin se posait sur le bas de la barre de navigation
     et empêchait de cliquer le choix de langue */
  el.style.cssText='position:fixed;right:14px;bottom:14px;z-index:9998;display:flex;align-items:center;'
    +'gap:9px;padding:8px 12px;border-radius:9px;font:500 12px Inter,system-ui,sans-serif;'
    +'box-shadow:0 4px 16px rgba(0,0,0,.13);max-width:330px;line-height:1.4;'
    +(tard?'background:#FBECEC;color:#7E1D22;border:1px solid #E9BFC0'
          :'background:#EDF3EF;color:#245A41;border:1px solid #CBDFD3');
  const S=n.toLocaleString('fr-FR')+' modification'+(n>1?'s':'');
  el.innerHTML='<span>'+(j===null
      ? '<b>'+S+'</b> jamais sauvegardée'+(n>1?'s':'')
      : (tard ? '<b>'+S+'</b> depuis la sauvegarde d\'il y a '+j+' jour'+(j>1?'s':'')
              : '<b>'+S+'</b> depuis la sauvegarde d\''+(j===0?"aujourd'hui":'hier')))
    +'</span>';
  const b=document.createElement('button');
  b.textContent='Sauvegarder';
  b.style.cssText='border:0;border-radius:6px;padding:5px 9px;font:600 11.5px Inter,system-ui,sans-serif;'
    +'cursor:pointer;flex:none;'+(tard?'background:#A4262C;color:#fff':'background:#2C6E4E;color:#fff');
  b.onclick=()=>svTelecharge(false);
  el.appendChild(b);
}

/* Le témoin se remet à jour tout seul : quelqu'un peut travailler une journée
   entière sans jamais recharger la page. Et une fois par jour, le fichier part
   dans Téléchargements sans qu'on ait rien à demander. */
(function svAuto(){
  const go=()=>{
    try{
      svTemoin();
      if(svSaisies()<5) return;
      const auj=ajd();
      if(localStorage.getItem(SV_AUTO)===auj) return;    /* déjà fait aujourd'hui */
      let d=0; try{ d=+(localStorage.getItem(SV_DATE)||0); }catch(e){}
      if(d && Date.now()-d < 20*3600000) return;          /* sauvegardé il y a moins de 20 h */
      svTelecharge(true);
    }catch(e){}
  };
  const demarre=()=>{ setTimeout(go,1500); setInterval(go,20000); };
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',demarre);
  else demarre();
  addEventListener('storage',()=>{ try{ svTemoin(); }catch(e){} });
  /* si on ferme la page avec du travail non sauvegardé, on prévient */
  addEventListener('beforeunload',e=>{
    try{ let d=0; try{ d=+(localStorage.getItem(SV_DATE)||0); }catch(x){}
      if(svSaisies()>=25 && (!d || Date.now()-d > 3*86400000)){ e.preventDefault(); e.returnValue=''; }
    }catch(x){}
  });
})();
"""
