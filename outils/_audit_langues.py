# Audit des trois langues : ce qui reste en français quand l'écran est en anglais
# ou en espagnol.
#
# La traduction marche par dictionnaire : une phrase française exacte → sa version.
# Tout ce qui n'y est pas reste en français à l'écran. Ce script charge chaque page
# dans chaque langue, parcourt le texte visible exactement comme le fait le
# traducteur (mêmes zones exclues : données, saisies), et relève ce qui est resté
# en français. Il produit un fichier JSON et un résumé lisible.
import json, pathlib, re, sys
from playwright.sync_api import sync_playwright

D = pathlib.Path('/home/claude/catalogue')
PAGES = ['tableau.html', 'catalogue.html', 'stock.html', 'ventes.html', 'factures.html',
         'etude.html', 'fournisseurs.html', 'clients.html', 'retail.html', 'journal.html',
         'acces.html', 'reglages.html', 'messages.html', 'connecteurs.html',
         'inventaire_pc.html', 'accueil.html']
SESS = ("localStorage.setItem('sam-session-v1', JSON.stringify("
        "{id:'sam',nom:'Sam',role:'patron',depuis:new Date().toISOString()}))")

# Ce qui trahit du français dans un écran anglais ou espagnol.
FR = re.compile(r"[èêàçùûôîâœ]|\b(des|du|une|et|ou|pour|avec|sans|dans|sur|ce|cette|ces|tous|toutes|tout|"
                r"aucun|aucune|depuis|encore|déjà|ici|hier|aujourd'hui|mois|jours|jour|semaine|ligne|lignes|"
                r"prix|achat|vente|ventes|marge|marges|fournisseur|fournisseurs|facture|factures|devis|"
                r"enregistrer|déposer|rechercher|modifier|supprimer|annuler|fermer|garder|nouveau|nouvelle|"
                r"ajouter|choisir|envoyer|imprimer|importer|exporter|voir|afficher|masquer|chercher|trier|"
                r"filtrer|référence|références|quantité|unités|montant|reste|dû|payé|payée|est|sont|pas|moins|"
                r"rien|personne|qui|quoi|dont|où|mais|donc|code-barres|codes-barres|marque|nom|contenance|"
                r"utilisateur|identifiant|mot de passe|compte|comptes|rôle|rôles|accès|réglages|tableau|bord|"
                r"inventaire|chargement|aperçu|brouillon|étude|entrepôt|patron|comptable|écrire|écrit|"
                r"jamais|toujours|chaque|celui|celle|ceux|leur|leurs|notre|votre|ton|ta|tes|mon|ma|mes)\b", re.I)
# Faux positifs à écarter : marques, noms propres, jetons techniques
IGNORE = re.compile(r"^(\d[\d\s.,%$€:/\-–—]*|[A-Z0-9\-_.]{2,}|v\d.*|•|—|–|·|\.{3}|…)$")

JS_COLLECTE = r"""
(() => {
  const LG_SAUT={SCRIPT:1,STYLE:1,TEXTAREA:1,CODE:1,PRE:1,INPUT:1};
  const LG_DATA='.lnm,.lmq,.nom,.nm,.mq,.marque,.produit,.bc,.lbc,.lid,.pd,td.ref,[data-nolang]';
  const donnee=(n)=>{ let e=n.parentNode; while(e&&e!==document.body){
    if(e.nodeType===1&&e.matches&&e.matches(LG_DATA)) return true; e=e.parentNode; } return false; };
  const visible=(el)=>{ if(!el) return false; const r=el.getClientRects(); if(!r.length) return false;
    const s=getComputedStyle(el); return s.visibility!=='hidden' && s.display!=='none'; };
  const out=[];
  const it=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT,{acceptNode:n=>
    ((n.parentNode&&LG_SAUT[n.parentNode.nodeName])||donnee(n))?NodeFilter.FILTER_REJECT:NodeFilter.FILTER_ACCEPT});
  let n; while((n=it.nextNode())){
    const t=(n.nodeValue||'').replace(/\s+/g,' ').trim(); if(!t||!/[A-Za-zÀ-ÿ]/.test(t)) continue;
    const traduit = n.__fr!==undefined;
    const el=n.parentNode;
    let chemin=[]; let e=el; let k=0;
    while(e&&e!==document.body&&k<4){ chemin.unshift(e.tagName.toLowerCase()+(e.id?'#'+e.id:'')+(e.className&&typeof e.className==='string'?'.'+e.className.trim().split(/\s+/).slice(0,2).join('.'):'')); e=e.parentNode; k++; }
    out.push({t, traduit, vis:visible(el), ou:chemin.join('>'), genre:'texte'});
  }
  document.querySelectorAll('[placeholder],[title],[aria-label]').forEach(el=>{
    ['placeholder','title','aria-label'].forEach(a=>{ if(!el.hasAttribute(a)) return;
      const t=(el.getAttribute(a)||'').replace(/\s+/g,' ').trim(); if(!t||!/[A-Za-zÀ-ÿ]/.test(t)) return;
      out.push({t, traduit: el['__fr_'+a]!==undefined, vis:visible(el), ou:el.tagName.toLowerCase()+(el.id?'#'+el.id:'')+'['+a+']', genre:a}); });
  });
  return out;
})()
"""

def audit(pg, page, lang):
    pg.goto('file://' + str(D / page)); pg.wait_for_timeout(2500)
    return pg.evaluate(JS_COLLECTE)

rapport = {}
with sync_playwright() as p:
    b = p.chromium.launch()
    for lang in ['en', 'es']:
        pg = b.new_page(viewport={'width': 1500, 'height': 1000})
        pg.goto('file://' + str(D / 'accueil.html')); pg.wait_for_timeout(600)
        pg.evaluate(SESS); pg.evaluate(f"localStorage.setItem('langue-v1','{lang}')")
        for page in PAGES:
            try:
                L = audit(pg, page, lang)
            except Exception as e:
                rapport[f'{page}|{lang}'] = {'erreur': str(e)}; continue
            total = len(L); trad = sum(1 for x in L if x['traduit'])
            restes = {}
            for x in L:
                if x['traduit']: continue
                t = x['t']
                if IGNORE.match(t): continue
                if not FR.search(t): continue
                k = t
                r = restes.setdefault(k, {'n': 0, 'vis': False, 'ou': x['ou'], 'genre': x['genre']})
                r['n'] += 1; r['vis'] = r['vis'] or x['vis']
            rapport[f'{page}|{lang}'] = {'total': total, 'traduits': trad, 'restes': restes}
        pg.close()
    b.close()

out = D / '_audit_langues.json'
out.write_text(json.dumps(rapport, ensure_ascii=False, indent=1), encoding='utf-8')

# résumé
print(f"{'page':22} {'lang':4} {'textes':>7} {'traduits':>9} {'restes FR':>10}  (dont visibles)")
tot_r = 0; tot_v = 0
for k, v in rapport.items():
    page, lang = k.split('|')
    if 'erreur' in v: print(f"{page:22} {lang:4} ERREUR {v['erreur'][:60]}"); continue
    nv = sum(1 for r in v['restes'].values() if r['vis'])
    tot_r += len(v['restes']); tot_v += nv
    print(f"{page:22} {lang:4} {v['total']:7} {v['traduits']:9} {len(v['restes']):10}  ({nv})")
print(f"\nTOTAL restes distincts : {tot_r}  dont visibles au chargement : {tot_v}")
print(f"détail : {out}")
