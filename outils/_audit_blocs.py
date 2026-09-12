# Complément de l'audit : pour chaque texte resté en français, remonte au bloc
# entier (le paragraphe coupé par un mot en gras) et sort son HTML, pour écrire la
# traduction du bloc avec ses propres <b>.
import json, pathlib, re
from playwright.sync_api import sync_playwright
D = pathlib.Path('/home/claude/catalogue')
PAGES = ['tableau.html','catalogue.html','stock.html','ventes.html','factures.html','etude.html',
         'fournisseurs.html','clients.html','retail.html','journal.html','acces.html','reglages.html',
         'messages.html','connecteurs.html','inventaire_pc.html','accueil.html']
SESS = ("localStorage.setItem('sam-session-v1', JSON.stringify("
        "{id:'sam',nom:'Sam',role:'patron',depuis:new Date().toISOString()}))")
JS = r"""
(() => {
  const LG_SAUT={SCRIPT:1,STYLE:1,TEXTAREA:1,CODE:1,PRE:1,INPUT:1};
  const LG_DATA='.lnm,.lmq,.nom,.nm,.mq,.marque,.produit,.bc,.lbc,.lid,[data-nolang]';
  const BLOC='p,li,span,label,small,div,td,th,h1,h2,h3,h4,button,a,em,strong,summary,legend,dt,dd';
  const donnee=(n)=>{ let e=n.parentNode; while(e&&e!==document.body){ if(e.nodeType===1&&e.matches&&e.matches(LG_DATA)) return true; e=e.parentNode; } return false; };
  const out={};
  const it=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT,{acceptNode:n=>((n.parentNode&&LG_SAUT[n.parentNode.nodeName])||donnee(n))?NodeFilter.FILTER_REJECT:NodeFilter.FILTER_ACCEPT});
  let n; while((n=it.nextNode())){
    const t=(n.nodeValue||'').replace(/\s+/g,' ').trim(); if(!t||!/[A-Za-zÀ-ÿ]/.test(t)) continue;
    if(n.__fr!==undefined) continue;
    // bloc = ancetre le plus proche qui a des enfants elements (donc un texte coupe)
    let e=n.parentNode, bloc=null;
    while(e&&e!==document.body){
      if(e.matches(BLOC)&&e.children.length>0&&e.children.length<=12&&!e.querySelector('input,textarea,select,table,ul,ol,img,svg,canvas')&&!e.matches(LG_DATA)){ bloc=e; break; }
      if(e.matches(BLOC)&&e.children.length===0){ break; }
      e=e.parentNode;
    }
    if(bloc){
      // texte et html FRANÇAIS d'origine : chaque nœud traduit garde son __fr
      const c=bloc.cloneNode(true);
      const A=document.createTreeWalker(bloc,NodeFilter.SHOW_TEXT), B=document.createTreeWalker(c,NodeFilter.SHOW_TEXT);
      let x,y,txt=''; while((x=A.nextNode())&&(y=B.nextNode())){ const f=(x.__fr!==undefined?x.__fr:x.nodeValue); y.nodeValue=f; txt+=' '+f; }
      txt=txt.replace(/\s+/g,' ').trim();
      if(txt.length<=900 && !out[txt]) out[txt]={html:c.innerHTML.replace(/\s+/g,' ').trim(), tag:bloc.tagName.toLowerCase()};
    }
  }
  return out;
})()
"""
res={}
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1500,'height':1000})
    pg.goto('file://'+str(D/'accueil.html')); pg.wait_for_timeout(500)
    pg.evaluate(SESS); pg.evaluate("localStorage.setItem('langue-v1','en')")
    for page in PAGES:
        pg.goto('file://'+str(D/page)); pg.wait_for_timeout(2200)
        for k,v in pg.evaluate(JS).items():
            if k not in res: res[k]=dict(v,page=page.replace('.html',''))
    b.close()
(D/'_audit_blocs.json').write_text(json.dumps(res,ensure_ascii=False,indent=1),encoding='utf-8')
print(len(res),'blocs')
