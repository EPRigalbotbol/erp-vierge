# UN CODE-BARRES N'EST PAS FORCÉMENT QUE DES CHIFFRES (Igal, 10 nov. 2026 : « Sam est obligé de créer des barcodes pour des
# produits qui n'en ont pas, qui n'ont pas de boîte » — exemple : « 131514UNBOXED » ; une fiche porte aussi un code tout en lettres).
# Avant, l'ERP retirait tout ce qui n'était pas un chiffre : « 131514UNBOXED » devenait 131514, un code en lettres devenait vide.
# Ce test protège :
#   1. LE POINT — une vente reçue (site, caisse, Perfume City) avec « 131514UNBOXED » (majuscules ou non) retombe sur sa fiche ;
#   2. LE POINT — un code tout en lettres posé sur une fiche par Sam retrouve cette fiche (ventes reçues, Cote/Ventes) ;
#   3. le stock annoncé aux sites retrouve la fiche par ce code ;
#   4. LE POINT — dans l'Inventaire, la douchette (ou le code tapé + Entrée) trouve le parfum par ce code ;
#   5. les codes en chiffres marchent comme avant (le même code avec « nobox » collé ne se confond pas avec la boîte) ;
#   6. aucune erreur JS.
import pathlib, subprocess, time, socket, json
from playwright.sync_api import sync_playwright
D = pathlib.Path('/home/claude/catalogue')
ok = 0; ko = []
def check(n, c, i=''):
    global ok
    if c: ok += 1; print('  ok  ', n)
    else: ko.append(n); print('  KO  ', n, str(i)[:300])
CAT = json.load(open(D / 'cat.json'))
A = next(r for r in CAT if r[0] and len(str(r[0])) == 13 and str(r[0]).isdigit() and r[15])
s = socket.socket(); s.bind(('127.0.0.1', 0)); port = s.getsockname()[1]; s.close()
srv = subprocess.Popen(['python3', '-m', 'http.server', str(port), '--bind', '127.0.0.1'], cwd=str(D), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1)
NOUV = {'id': 'aunboxed1', 'bc': '131514UNBOXED', 'nom': 'Essai sans boîte', 'marque': 'Maison', 'ml': '3.4', 'type': 'EDP', 'genre': '', 'qte': 4, 'pa': 10, 'pvr': 30, 'pvw': 20}
try:
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1400, 'height': 900}); err = []
        pg.on('pageerror', lambda e: err.append(str(e)))
        base = f'http://127.0.0.1:{port}/'
        pg.goto(base + 'accueil.html'); pg.wait_for_timeout(300)
        pg.evaluate("""(N)=>{ localStorage.clear(); localStorage.setItem('sam-comptes-demo-v1','0');
            localStorage.setItem('sam-comptes-v1',JSON.stringify([{ident:'sam',nom:'Sam',role:'patron',actif:true,h:'x'}]));
            localStorage.setItem('sam-session-v1',JSON.stringify({id:'sam',nom:'Sam',role:'patron',depuis:new Date().toISOString()}));
            localStorage.setItem('articles-ajoutes-v1',JSON.stringify([N])); }""", NOUV)
        pg.goto(base + 'stock.html'); pg.wait_for_timeout(3000)
        # une fiche sans code-barres à qui Sam donne un code tout en lettres
        T = pg.evaluate("""()=>{ const p=P.find(x=>!x.bc); const M=lit(KMOD,{}); M[p.cle]=Object.assign({},M[p.cle]||{},{bc:'LEauParKenzoTester'}); ecrit(KMOD,M); return p.cle; }""")
        pg.reload(); pg.wait_for_timeout(3000)
        print('1. l\'Inventaire')
        r = pg.evaluate("([t])=>{ const a=trouveBC('131514UNBOXED'), b=trouveBC('131514unboxed'), c=trouveBC('LEAUPARKENZOTESTER'); return [a&&(a.cle||a.id), b&&(b.cle||b.id), c&&c.cle]; }", [T])
        check('LE POINT — la douchette trouve « 131514UNBOXED » (majuscules ou non) et le code tout en lettres', r[0] == NOUV['id'] and r[1] == NOUV['id'] and r[2] == T, r)
        pg.fill('#q', '131514UNBOXED'); pg.press('#q', 'Enter'); pg.wait_for_timeout(600)
        foc = pg.evaluate("(document.activeElement&&document.activeElement.dataset&&document.activeElement.dataset.bc)||''")
        check('le code tapé dans la recherche + Entrée amène sur la case à compter de ce parfum', foc.upper() == '131514UNBOXED', foc)
        check('un code en chiffres se trouve comme avant', (pg.evaluate("bc=>{ const p=trouveBC(bc); return p&&p.bc; }", A[0]) or '').lstrip('0') == str(A[0]).lstrip('0'))
        print('2. les ventes reçues et la Cote')
        pg.goto(base + 'ventes.html'); pg.wait_for_timeout(3000)
        r = pg.evaluate("""([t])=>{ const C=faContexte(); return [C.cleDe({bc:'131514UNBOXED',des:'x'}), C.cleDe({bc:'131514unboxed',des:'x'}), C.cleDe({sku:'LEauParKenzoTester',des:'x'}), C.cleDe({bc:'leau-par-kenzo-tester',des:'x'}),
            cleDeBC('131514UNBOXED'), cleDeBC('LEauParKenzoTester')]; }""", [T])
        check('LE POINT — une vente reçue au code « 131514UNBOXED » retombe sur sa fiche', r[0] == NOUV['id'] and r[1] == NOUV['id'], r)
        check('LE POINT — une vente reçue au code tout en lettres (SKU du site, tirets compris) retombe sur la fiche', r[2] == T and r[3] == T, r)
        check('la Cote et Ventes retrouvent les deux fiches par ces codes', r[4] == NOUV['id'] and r[5] == T, r)
        r = pg.evaluate("bc=>{ const C=faContexte(); return [C.cleDe({bc:bc,des:'x'}), C.cleDe({bc:bc+'nobox',des:'x'})]; }", A[0])
        check('un code en chiffres comme avant ; « …nobox » ne retombe pas sur la boîte', r[0] == A[15] and r[1] != A[15], r)
        print('3. le stock annoncé aux sites')
        r = pg.evaluate("()=>_ssFichesDuBC('LEAUPARKENZOTESTER')")
        check('le stock annoncé aux sites retrouve la fiche par le code que Sam a posé dessus', T in r, r)
        check('aucune erreur JS', not err, err[:3])
        b.close()
finally:
    srv.terminate()
print(f'\n{ok} ok, {len(ko)} KO', ko); raise SystemExit(1 if ko else 0)
