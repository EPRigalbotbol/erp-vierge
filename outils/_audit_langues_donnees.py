# Audit des langues AVEC DES DONNÉES : les listes remplies (ventes, file d'attente,
# expéditions, fiche d'un parfum, étude d'un devis) — c'est là que le français resté
# en place se voit, pas sur une page vide. Igal, 24 sept. 2026 : « vérifie toutes les
# listes dans toutes les langues ».
import pathlib, subprocess, time, socket, json, random, re, sys
from playwright.sync_api import sync_playwright
D = pathlib.Path('/home/claude/catalogue')
CAT = json.load(open(D / 'cat.json'))
random.seed(7)
enstock = [r for r in CAT if (r[6] or 0) > 0 and r[0]]
longs = sorted(enstock, key=lambda r: -len((r[2] or '') + (r[1] or '')))[:30] + random.sample(enstock, 60)
# des ventes de tous les canaux, dont des numéros de caisse au format interne
FACT = []
for i, r in enumerate(longs):
    src = ['lightspeed', 'woocommerce', 'amazon', 'woocommerce-gros', ''][i % 5]
    canal = {'lightspeed': 'Caisse Lightspeed', 'woocommerce': 'Site perfumestrade.com', 'amazon': 'Amazon',
             'woocommerce-gros': 'Site wholesale.perfumestrade.com', '': 'Boutique'}[src]
    num = {'lightspeed': '161cfa62-e6f7-a592-11f1-b84381ae%04x' % i, 'amazon': '114-%07d-%07d' % (i * 7919, i * 104729),
           'woocommerce': str(20600 + i), 'woocommerce-gros': str(900 + i), '': 'V260924-%d' % i}[src]
    ref = ((r[2] or '') + ' ' + (r[1] or '') + (' ' + r[4] if r[4] else '')).strip()
    FACT.append({'id': 'f%d' % i, 'num': num, 'sens': 'vente', 'canal': canal, 'export': canal, 'tiers': 'Client Très Long Nom Numéro %d' % i,
                 'd': '2026-09-%02d' % (1 + i % 24), 'h': '%02d:%02d' % (8 + i % 12, i % 60),
                 'lignes': [{'cle': r[15], 'bc': r[0], 'ref': ref, 'q': 1 + i % 3, 'p': float(r[7] or 50), 'qAv': 5, 'qAp': 4, 'paAv': float(r[12] or 20)}],
                 'montant': float(r[7] or 50) * (1 + i % 3), 'stock': True, 'par': 'Sam', 't': '2026-09-%02dT12:00:00Z' % (1 + i % 24), 'auto': src})
FILE = [{'_i': 'amazon|%d' % i, 'src': 'amazon', 'd': '2026-09-%02d' % (10 + i), 'h': '10:%02d' % i, 'num': '113-%07d-5556667' % i, 'client': 'Acheteur au nom interminable %d' % i,
         'lignes': [{'bc': '9%011d' % i, 'des': 'BULGARI BULGARI EAU PARFUMEE PERFUME 2.5 OZ WHITE TEA AU THE BLANC COLOGNE SPRAY', 'q': 1, 'p': 45}]} for i in range(6)]
EXP = [{'_i': 'woocommerce|x%d' % i, 'src': ['woocommerce', 'amazon'][i % 2], 'num': str(20700 + i), 'client': 'Client Expédition %d' % i, 'd': '2026-09-%02d' % (18 + i), 'h': '09:00',
        'lignes': [{'cle': r[15], 'bc': r[0], 'des': r[1], 'q': 1, 'p': float(r[7] or 50), 'ref': ((r[2] or '') + ' ' + (r[1] or '')).strip()}],
        'montant': float(r[7] or 50), 'arrive': '2026-09-24T10:00:00Z', 'statut': 'attente'} for i, r in enumerate(longs[:8])]
MOD = {r[15]: {'qte': 2} for r in longs[:10]}
SITE = {str(r[0]): {'d': {'id': 1000 + i, 'q': (r[6] or 0) + (i % 3), 'suivi': True, 'etat': 'instock', 'nom': 'x', 'pr': float(r[7] or 50) + 10, 'ps': float(r[7] or 50)},
                    'g': {'id': 1000 + i, 'q': 0, 'suivi': True, 'etat': 'outofstock', 'nom': 'x', 'pr': float(r[8] or 30), 'ps': None}} for i, r in enumerate(longs)}
JOU = [{'t': '2026-09-%02dT1%d:00:00Z' % (1 + i % 24, i % 10), 'u': 'Sam', 'act': ['vente', 'stock', 'prix', 'annulation'][i % 4],
        'lib': 'une ligne de journal assez longue pour voir si elle passe à la ligne correctement, numéro %d' % i, 'ref': longs[i % 30][15], 'av': '10', 'ap': '12'} for i in range(80)]

HIST = {r[15]: [{'d': '2026-0%d-1%d' % (1 + k, k), 'p': float(r[12] or 20) * (1 + k / 20), 'f': 'Fournisseur au long nom', 'q': 6} for k in range(3)] for r in longs[:30]}
ETU = '\n'.join(f"{r[0]}\t{(r[2] or '')} {(r[1] or '')} EAU DE PARFUM SPRAY\t3\t{round(float(r[12] or 20) * 0.95, 2)}" for r in longs[:20]) + '\n123456789012\tUNKNOWN PRODUCT LONG DESCRIPTION\t2\t19.5'
PAGES = sys.argv[1].split(',') if len(sys.argv) > 1 else ['catalogue', 'stock', 'ventes', 'expeditions', 'factures', 'etude', 'journal', 'tableau', 'connecteurs', 'reglages', 'acces', 'fournisseurs', 'clients', 'quotes', 'inventaire_pc', 'messages']
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


s = socket.socket(); s.bind(('127.0.0.1', 0)); port = s.getsockname()[1]; s.close()
srv = subprocess.Popen(['python3', '-m', 'http.server', str(port), '--bind', '127.0.0.1'], cwd=str(D), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1)
res = {}; BLOCS = {}
JS_BLOCS = r'''(() => { const FRx=/[èéêàçùûôîâœ]|\b(des|du|une|et|pour|avec|sans|dans|sur|est|pas|le|la|les|de|au|aux)\b/i; const out=[];
  const it=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT); let n;
  while((n=it.nextNode())){ const el=n.parentNode; if(!el||/SCRIPT|STYLE|TEXTAREA/.test(el.nodeName)) continue; if(n.__fr!==undefined) continue;
    const t=(n.nodeValue||'').replace(/\s+/g,' ').trim(); if(!t||!FRx.test(t)) continue; if(!el.getClientRects().length) continue;
    if(el.closest(LG_DATA)) continue;
    let b=el; while(b&&b!==document.body&&!(b.matches(LG_BLOC)&&b.children.length&&b.children.length<=12&&b.textContent.length<900)) b=b.parentElement;
    if(!b||b===document.body) b=el;
    const kids=[...b.querySelectorAll('*')].map((k,i)=>(i+1)+':'+k.nodeName.toLowerCase()+'='+(k.textContent||'').trim().slice(0,30));
    out.push({t, bloc:lgTexteFr(b), tag:b.nodeName, kids}); }
  return out; })()'''
try:
    with sync_playwright() as p:
        b = p.chromium.launch()
        for lg in ['en', 'es']:
            pg = b.new_page(viewport={'width': 1600, 'height': 1000})
            pg.goto(f'http://127.0.0.1:{port}/accueil.html'); pg.wait_for_timeout(300)
            pg.evaluate("localStorage.setItem('sam-session-v1', JSON.stringify({id:'sam',nom:'Sam',role:'patron',depuis:new Date().toISOString()}))")
            pg.evaluate("([F,Q,E,M,S,J,H,T,l])=>{ localStorage.setItem('factures-v1',JSON.stringify(F)); localStorage.setItem('caisse-file-v1',JSON.stringify(Q)); localStorage.setItem('expeditions-v1',JSON.stringify(E)); localStorage.setItem('fiches-modifiees-v1',JSON.stringify(M)); localStorage.setItem('site-stock-v1',JSON.stringify(S)); localStorage.setItem('crm-journal-v1',JSON.stringify(J)); localStorage.setItem('prix-achat-hist-v1',JSON.stringify(H)); localStorage.setItem('etude-brouillon-v1',JSON.stringify({texte:T,frn:'',date:'2026-09-24',num:''})); localStorage.setItem('langue-v1',l); localStorage.setItem('ck-token','x'); }", [FACT, FILE, EXP, MOD, SITE, JOU, HIST, ETU, lg])
            for page in PAGES:
                pg.goto(f'http://127.0.0.1:{port}/{page}.html'); pg.wait_for_timeout(2000)
                vues = [('', None)]
                if page == 'catalogue': vues.append(('fiche', "()=>{ const p=cur.find(x=>(x.stock||x.qte||0)>1)||cur[0]; ouvreFiche(p.id); }"))
                # Réglages (25 oct. 2026) : un onglet à la fois, les explications derrière « ? » — on ouvre tout.
                if page == 'reglages': vues = [(t, "()=>{ __rgOnglet('%s'); document.querySelectorAll('.plus').forEach(p=>p.hidden=false); }" % t) for t in ('soc', 'pc', 'prix', 'stock', 'caisse')]
                for nom, act in vues:
                    if act:
                        try: pg.evaluate(act); pg.wait_for_timeout(900)
                        except Exception as e: print('vue?', nom, e)
                    L = pg.evaluate(JS_COLLECTE)
                    if lg == 'en' and '--blocs' in sys.argv:
                        for x in pg.evaluate(JS_BLOCS): BLOCS.setdefault(x['bloc'], x)
                    for x in L:
                        if x['traduit'] or not x['vis']: continue
                        t = x['t']
                        if IGNORE.match(t) or not FR.search(t): continue
                        res.setdefault(page + (':' + nom if nom else ''), {}).setdefault(t, set()).add(lg)
            pg.close()
        b.close()
finally:
    srv.terminate()
n = 0
for pgn, d in res.items():
    print('==', pgn, len(d))
    for t, l in sorted(d.items()): print('   ', ','.join(sorted(l)), '|', t[:150]); n += 1
print('\nTOTAL', n)
if BLOCS:
    json.dump(BLOCS, open('/tmp/claude-0/-home-claude/7f8c7d7e-a2bf-53ed-8df2-d9c17ddd87b0/scratchpad/blocs.json', 'w'), ensure_ascii=False, indent=1)
