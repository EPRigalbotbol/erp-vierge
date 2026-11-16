# LE TESTER DE PERFUME CITY, C'EST LA BOUTIQUE QUI LE DÉCLARE (16 nov. 2026 — Igal, à la demande de Sam : « il faut enlever la règle…
# lorsque Sam donne une quantité à Perfume City… c'est elle qui doit sélectionner j'ai un tester… il ne faut pas que ça se fasse
# automatiquement »). Et le comptage de la boutique doit arriver dans SON stock partagé (pc-stock-v1), celui que Shopify reçoit :
# constaté le même jour, 12 comptages de Kim sur 16 n'y étaient jamais entrés. Ce test protège :
#   1. LE POINT — cocher « tester » sort un flacon de la vente (5 → 4) et note le tester ; décocher le rend (4 → 5) ;
#   2. un tester venu de l'ancien fichier (pas « pris ») ne crée jamais de stock quand on le décoche ;
#   3. rien en vente : le tester est noté, la quantité reste 0 ;
#   4. LE POINT — un comptage écrit dans le stock partagé (compté 5 avec un tester = 4 en vente) ; vider la case rend l'ancien chiffre ;
#   5. la page montre le stock partagé, jamais une ancienne copie du comptage ;
#   6. traduit en anglais et en espagnol ; aucune erreur JS.
import subprocess, time, socket
from playwright.sync_api import sync_playwright
D = '/home/claude/catalogue'
ok = 0; ko = []
def check(n, c, i=''):
    global ok
    if c: ok += 1; print('  ok  ', n)
    else: ko.append(n); print('  KO  ', n, str(i)[:500])
s = socket.socket(); s.bind(('127.0.0.1', 0)); port = s.getsockname()[1]; s.close()
srv = subprocess.Popen(['python3', '-m', 'http.server', str(port), '--bind', '127.0.0.1'], cwd=D, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)
A, B, C, E = '1111111111116', '2222222222222', '3333333333338', '4444444444444'
def fiche(bc, nom, q): return {'bc': bc, 'nom': nom, 'm': 'Marque', 'ml': '3.4', 'ty': 'EDP', 'q': q, 'pa': 10, 'pvr': 30, 'pvw': 20, 'cle': 'b' + bc}
STOCK = {A: fiche(A, 'Alpha', 5), B: fiche(B, 'Beta', 3), C: fiche(C, 'Gamma', 0), E: fiche(E, 'Epsilon', 2)}
TEST = {B: {'n': 1, 'bc': B, 'ref': 'Marque Beta', 't': '2026-10-13T19:31:07.869Z', 'u': 'Igal'}}
MODPC = {'b' + E: {'qte': 9, 'qteC': 9, 'verif': 'ok'}}
SESS = """([S,T,M,lg])=>{ localStorage.clear(); localStorage.setItem('sam-comptes-demo-v1','0');
  localStorage.setItem('sam-session-v1',JSON.stringify({id:'kim',nom:'Kim',role:'patron',depuis:new Date().toISOString()}));
  localStorage.setItem('langue-v1',lg); localStorage.setItem('pc-stock-v1',JSON.stringify(S)); localStorage.setItem('testeurs-pc-v1',JSON.stringify(T));
  localStorage.setItem('fiches-modifiees-pc-v1',JSON.stringify(M)); }"""
try:
    with sync_playwright() as p:
        b = p.chromium.launch(); err = []
        def ouvre(lg='fr'):
            pg = b.new_page(viewport={'width': 1500, 'height': 1000}); pg.on('pageerror', lambda e: err.append(str(e)))
            pg.goto(f'http://127.0.0.1:{port}/accueil.html'); pg.wait_for_timeout(300); pg.evaluate(SESS, [STOCK, TEST, MODPC, lg])
            pg.goto(f'http://127.0.0.1:{port}/inventaire_pc.html'); pg.wait_for_timeout(2500)
            # 16 nov. 2026 : la page porte maintenant toutes les lignes du Catalogue — on cherche les parfums du test (codes inconnus du Catalogue)
            pg.fill('#q', 'Marque'); pg.wait_for_timeout(500); return pg
        pg = ouvre()
        q = lambda bc: pg.evaluate("b=>(lit('pc-stock-v1',{})[b]||{}).q", bc)
        tst = lambda bc: pg.evaluate("b=>lit('testeurs-pc-v1',{})[b]||null", bc)
        ligne = lambda bc: pg.locator(f'tr[data-bc="{bc}"]').inner_text()
        case = lambda bc: pg.locator(f'tr[data-bc="{bc}"] input.tck')
        # 16 nov. 2026 (Igal : « enlève le théorique sur l'inventaire ») : la colonne s'appelle « Tester » et ne montre plus de chiffre
        check('LE POINT — la colonne s\'appelle « Tester », sans chiffre théorique', pg.locator('thead th.thc').inner_text().strip().lower() == 'tester' and pg.locator(f'tr[data-bc="{A}"] td.thc').inner_text().strip().lower() == 'tester', [pg.locator('thead th.thc').inner_text(), pg.locator(f'tr[data-bc="{A}"] td.thc').inner_text()])
        check('chaque ligne porte une case « tester » ; Alpha ne l\'a pas, Beta (ancien fichier) l\'a', case(A).count() == 1 and not case(A).is_checked() and case(B).is_checked(), ligne(A))
        case(A).check(); pg.wait_for_timeout(500)
        t = tst(A)
        check('LE POINT — cocher « tester » sort un flacon de la vente : 5 → 4, tester noté', q(A) == 4 and t and t.get('n') == 1 and t.get('pris') == 1, (q(A), t))
        check('la ligne le montre : 4, « +1 tester », et « en vente : 5 → 4 »', '4' in ligne(A) and '+1 tester' in ligne(A) and '5 → 4' in ligne(A), ligne(A))
        j = pg.evaluate("lit('crm-journal-v1',[]).slice(-1)[0]")
        check('le journal le dit, avec le nom', j and 'tester déclaré par la boutique' in j.get('lib', '') and j.get('u') == 'Kim' and j.get('av') == 5 and j.get('ap') == 4, j)
        case(A).uncheck(); pg.wait_for_timeout(500)
        check('LE POINT — décocher rend le flacon à la vente : 4 → 5, plus de tester', q(A) == 5 and tst(A) is None, (q(A), tst(A)))
        case(B).uncheck(); pg.wait_for_timeout(500)
        check('LE POINT — décocher un tester de l\'ancien fichier ne crée pas de stock (3 reste 3)', q(B) == 3 and tst(B) is None, (q(B), tst(B)))
        case(C).check(); pg.wait_for_timeout(500)
        check('rien en vente : le tester est noté, la quantité reste 0', q(C) == 0 and tst(C) and tst(C).get('pris') == 0, (q(C), tst(C)))
        case(C).uncheck(); pg.wait_for_timeout(400)
        check('… et le décocher ne crée rien', q(C) == 0, q(C))
        # 4. le comptage
        def compte(bc, v):
            i = pg.locator(f'input.cnt[data-bc="{bc}"]'); i.fill(str(v)); i.dispatch_event('change'); pg.wait_for_timeout(600)
        compte(A, 3)
        check('LE POINT — compter 3 écrit 3 dans le stock partagé de Perfume City (celui que Shopify reçoit)', q(A) == 3, q(A))
        compte(A, '')
        check('vider la case rend le chiffre d\'avant (5)', q(A) == 5, q(A))
        case(A).check(); pg.wait_for_timeout(400); compte(A, 5)
        check('avec un tester, compter 5 flacons = 4 en vente + 1 tester, aucun écart', q(A) == 4 and pg.locator(f'tr[data-bc="{A}"].ecart').count() == 0, (q(A), ligne(A)))
        # 5. la page montre le stock partagé
        v = pg.evaluate("b=>{ const p=P.find(x=>x.bc===b); return [qteTh(p), cpt(p)===undefined]; }", E)
        check('LE POINT — la page montre le stock partagé (2), pas une ancienne copie du comptage (9), et ce vieux comptage est dit périmé', v == [2, True], v)
        pg.reload(); pg.wait_for_timeout(2500); pg.fill('#q', 'Marque'); pg.wait_for_timeout(500)
        check('après rechargement : Alpha 4 en vente et son tester', q(A) == 4 and case(A).is_checked() and '+1 tester' in ligne(A), ligne(A))
        pg.close()
        for lg, mot in (('en', 'on sale: 5 → 4'), ('es', 'a la venta: 5 → 4')):
            pg = ouvre(lg); case(A).check(); pg.wait_for_timeout(500); t = ligne(A)
            check(f'traduit ({lg})', mot in t and 'en vente' not in t, t); pg.close()
        # l'entrepôt garde sa colonne « Théorique » (Sam, 30 oct. 2026 : voir le stock actuel quand il recompte)
        pg = b.new_page(viewport={'width': 1500, 'height': 1000}); pg.on('pageerror', lambda e: err.append(str(e)))
        pg.goto(f'http://127.0.0.1:{port}/accueil.html'); pg.wait_for_timeout(300); pg.evaluate(SESS, [STOCK, TEST, MODPC, 'fr'])
        pg.goto(f'http://127.0.0.1:{port}/stock.html'); pg.wait_for_timeout(2500)
        check('l\'entrepôt garde « Théorique » avec son chiffre, sans case tester', pg.locator('thead th.thc').inner_text().strip().lower().startswith('théorique') and pg.locator('#tb input.tck').count() == 0 and pg.evaluate("()=>/\\d/.test(document.querySelector('#tb td.thc').innerText)"), pg.locator('thead th.thc').inner_text())
        pg.close()
        check('aucune erreur JS', not err, err[:3])
        b.close()
finally:
    srv.terminate()
print(f'{ok} ok, {len(ko)} KO')
raise SystemExit(1 if ko else 0)
