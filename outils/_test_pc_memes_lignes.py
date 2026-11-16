# L'INVENTAIRE DE PERFUME CITY A LES MÊMES LIGNES ET LES MÊMES NOMS QUE CELUI DE PERFUMES TRADE (16 nov. 2026 — Igal : « je veux que
# l'inventaire de Perfume City soit exactement comme l'inventaire de Perfumes Trade… les mêmes noms à l'identique »). Kim ne trouvait
# pas un parfum que la boutique n'avait jamais eu, et 671 lignes portaient le nom de son ancien fichier. Ce test protège :
#   1. LE POINT — toutes les lignes de l'entrepôt sont chez Perfume City (même nombre), un parfum jamais reçu y est à 0 ;
#   2. LE POINT — une ligne de la boutique porte le NOM DU CATALOGUE, pas celui de son ancien fichier, avec SA quantité ;
#   3. LE POINT — compter un parfum jamais reçu crée sa ligne dans le stock de la boutique, sous le nom du Catalogue ;
#   4. une ligne à 0 n'est pas écrite dans le stock tant qu'on ne compte pas (rien ne part vers Shopify) ;
#   5. ce que la boutique a sous un code inconnu du Catalogue reste visible, marqué « absent du Catalogue » ;
#   6. une fiche créée dans l'ERP (articles ajoutés) y est aussi ; une fiche retirée du Catalogue n'y est pas ;
#   7. anglais / espagnol ; aucune erreur JS.
import subprocess, time, socket, json
from playwright.sync_api import sync_playwright
D = '/home/claude/catalogue'
ok = 0; ko = []
def check(n, c, i=''):
    global ok
    if c: ok += 1; print('  ok  ', n)
    else: ko.append(n); print('  KO  ', n, str(i)[:500])
s = socket.socket(); s.bind(('127.0.0.1', 0)); port = s.getsockname()[1]; s.close()
srv = subprocess.Popen(['python3', '-m', 'http.server', str(port), '--bind', '127.0.0.1'], cwd=D, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)
INCONNU = '9999999999994'
SESS = """([lg])=>{ localStorage.clear(); localStorage.setItem('sam-comptes-demo-v1','0');
  localStorage.setItem('sam-session-v1',JSON.stringify({id:'kim',nom:'Kim',role:'patron',depuis:new Date().toISOString()}));
  localStorage.setItem('langue-v1',lg); }"""
try:
    with sync_playwright() as p:
        b = p.chromium.launch(); err = []
        pg = b.new_page(viewport={'width': 1500, 'height': 1000}); pg.on('pageerror', lambda e: err.append(str(e)))
        base = f'http://127.0.0.1:{port}/'
        pg.goto(base + 'accueil.html'); pg.wait_for_timeout(300); pg.evaluate(SESS, ['fr'])
        # l'entrepôt : ses lignes, et deux parfums à code-barres numérique unique
        pg.goto(base + 'stock.html'); pg.wait_for_timeout(2500)
        PT = pg.evaluate("()=>{ const n={}; P.forEach(p=>{ n[p.bc]=(n[p.bc]||0)+1; }); const L=P.filter(p=>/^\\d{11,13}$/.test(String(p.bc))&&n[p.bc]===1); return {n:P.length, a:L[0], b:L[1], c:L[2]}; }")
        A, B, C = PT['a'], PT['b'], PT['c']
        # la boutique : A sous un ANCIEN nom avec 4 flacons ; un parfum sous un code inconnu ; une fiche créée dans l'ERP ; C retiré du Catalogue
        pg.evaluate("""([A,C,INC])=>{ const z=x=>String(x).replace(/^0+/,'');
          localStorage.setItem('pc-stock-v1',JSON.stringify({[z(A.bc)]:{bc:A.bc,nom:'ANCIEN NOM DU FICHIER',m:'Vieille Marque',ml:'9.9',ty:'XXX',q:4,pa:1,pvr:2,pvw:3,cle:'b'+A.bc},
            [INC]:{bc:INC,nom:'Parfum Mystère',m:'Inconnue',ml:'3.4',ty:'EDP',q:2,pa:5,pvr:null,pvw:null,cle:'b'+INC}}));
          localStorage.setItem('articles-ajoutes-v1',JSON.stringify([{id:'a-test-1',bc:'1234500000017',nom:'Fiche Créée',marque:'Marque Neuve',ml:'3.4',type:'edp',qte:4,pa:31}]));
          localStorage.setItem('fiches-modifiees-v1',JSON.stringify({[C.cle]:{masque:true}})); }""", [A, C, INCONNU])
        pg.goto(base + 'stock.html'); pg.wait_for_timeout(2500)
        nPT = pg.evaluate("()=>P.length")
        pg.goto(base + 'inventaire_pc.html'); pg.wait_for_timeout(2500)
        nPC = pg.evaluate("()=>P.filter(p=>!p.horsCat).length")
        check('LE POINT — Perfume City a autant de lignes que l\'entrepôt (fiche créée comprise, fiche retirée exclue)', nPC == nPT and nPC > 1000, [nPC, nPT])
        la = pg.evaluate("bc=>{ const p=P.find(x=>x.bc===bc); return p?[p.marque,p.nom,String(p.ml),p.type,qteTh(p)]:null; }", A['bc'])
        check('LE POINT — la ligne de la boutique porte le nom du Catalogue (pas « ANCIEN NOM »), avec SA quantité (4)', la == [A['marque'], A['nom'], str(A['ml']), A['type'], 4], [la, A])
        lb = pg.evaluate("bc=>{ const p=P.find(x=>x.bc===bc); return p?[p.marque,p.nom,qteTh(p),p.pck]:null; }", B['bc'])
        check('LE POINT — un parfum que la boutique n\'a jamais eu est là, à 0, sous le nom du Catalogue', lb == [B['marque'], B['nom'], 0, None], lb)
        check('la fiche créée dans l\'ERP est là aussi, à 0 (le 4 de la fiche est le stock de l\'entrepôt)', pg.evaluate("()=>{ const p=P.find(x=>x.fiche==='a-test-1'); return p?[p.nom,qteTh(p)]:null; }") == ['Fiche Créée', 0])
        check('la fiche retirée du Catalogue n\'y est pas', pg.evaluate("c=>!P.some(x=>x.fiche===c)", C['cle']))
        st = pg.evaluate("()=>Object.keys(lit('pc-stock-v1',{})).length")
        check('LE POINT — rien n\'est écrit dans le stock tant qu\'on ne compte pas (toujours 2 lignes : rien ne part vers Shopify)', st == 2, st)
        pg.fill('#q', INCONNU); pg.wait_for_timeout(500)
        t = pg.locator(f'tr[data-bc="{INCONNU}"]').inner_text()
        check('le parfum sous un code inconnu du Catalogue reste visible, marqué « absent du Catalogue »', 'Parfum Mystère' in t and 'absent du catalogue' in t.lower(), t)
        # compter un parfum jamais reçu
        pg.fill('#q', B['bc']); pg.wait_for_timeout(500)
        i = pg.locator(f'input.cnt[data-bc="{B["bc"]}"]'); i.fill('3'); i.dispatch_event('change'); pg.wait_for_timeout(600)
        o = pg.evaluate("bc=>lit('pc-stock-v1',{})[String(bc).replace(/^0+/,'')]||null", B['bc'])
        check('LE POINT — compter 3 crée sa ligne dans le stock de la boutique, sous le nom du Catalogue', o and o.get('q') == 3 and o.get('nom') == B['nom'] and o.get('m') == B['marque'], o)
        # recompter A : la ligne garde sa quantité et prend le nom du Catalogue
        pg.fill('#q', A['bc']); pg.wait_for_timeout(500)
        i = pg.locator(f'input.cnt[data-bc="{A["bc"]}"]'); i.fill('6'); i.dispatch_event('change'); pg.wait_for_timeout(600)
        o = pg.evaluate("bc=>lit('pc-stock-v1',{})[String(bc).replace(/^0+/,'')]||null", A['bc'])
        check('recompter une ligne existante : 6 en stock, et son nom enregistré devient celui du Catalogue', o and o.get('q') == 6 and o.get('nom') == A['nom'], o)
        check('toujours une seule ligne par parfum (3 lignes dans le stock : A, B, l\'inconnu)', pg.evaluate("()=>Object.keys(lit('pc-stock-v1',{})).length") == 3)
        pg.reload(); pg.wait_for_timeout(2500)
        check('après rechargement : B à 3, A à 6', pg.evaluate("([a,b])=>[qteTh(P.find(x=>x.bc===a)),qteTh(P.find(x=>x.bc===b))]", [A['bc'], B['bc']]) == [6, 3])
        for lg, mot in (('en', 'not in the catalog'), ('es', 'no está en el catálogo')):
            pg.evaluate("lg=>localStorage.setItem('langue-v1',lg)", lg); pg.reload(); pg.wait_for_timeout(2500)
            pg.fill('#q', INCONNU); pg.wait_for_timeout(500); t = pg.locator(f'tr[data-bc="{INCONNU}"]').inner_text().lower()
            check(f'« absent du Catalogue » traduit ({lg})', mot in t and 'absent du catalogue' not in t, t)
        check('aucune erreur JS', not err, err[:3])
        b.close()
finally:
    srv.terminate()
print(f'{ok} ok, {len(ko)} KO')
raise SystemExit(1 if ko else 0)
