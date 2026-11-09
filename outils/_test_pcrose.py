# Igal, 13 oct. 2026 : « que les ventes Perfume City soient dans les ventes de l'ERP, différenciées par une ligne de
# couleur rose » et « sur le dashboard, une partie Perfume City ».
# Ce qui est en jeu :
#   1. une vente Perfume City est une ligne ROSE du journal des ventes, avec une pastille rose, et les autres ne le sont pas ;
#   2. le tableau de bord a un bloc Perfume City : vendu, marge, flacons en rayon, testeurs, capital, ce qui part vite ;
#   3. le bloc dit les choses simplement quand il n'y a pas encore de vente.
import pathlib, subprocess, time, socket, json
from playwright.sync_api import sync_playwright
D = pathlib.Path('/home/claude/catalogue')
ok = 0; ko = []
def check(n, c, i=''):
    global ok
    if c: ok += 1; print('  ok  ', n)
    else: ko.append(n); print('  KO  ', n, i)
CAT = json.load(open(D / 'cat.json'))
EN = [r for r in CAT if r[0] and r[0].isdigit() and len(r[0]) == 13 and (r[6] or 0) > 8 and r[2] and r[1]]
A, B = EN[0], EN[5]
s = socket.socket(); s.bind(('127.0.0.1', 0)); port = s.getsockname()[1]; s.close()
srv = subprocess.Popen(['python3', '-m', 'http.server', str(port), '--bind', '127.0.0.1'], cwd=str(D), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1)
PCINV = [[A[0], A[1], A[2], '', '', 5, 10, 50, 'non', 'b' + A[0], None, None]]
try:
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1500, 'height': 1000}); err = []
        pg.on('pageerror', lambda e: err.append(str(e))); pg.on('dialog', lambda d: d.accept())
        base = f'http://127.0.0.1:{port}/'
        pg.goto(base + 'accueil.html'); pg.wait_for_timeout(300)
        pg.evaluate("""inv=>{ localStorage.clear();
          localStorage.setItem('sam-session-v1',JSON.stringify({id:'sam',nom:'Sam',role:'patron',depuis:new Date().toISOString()}));
          localStorage.setItem('langue-v1','fr'); localStorage.setItem('sam-comptes-demo-v1','0'); localStorage.setItem('inventaire-local-pc-v1',JSON.stringify(inv));
          localStorage.setItem('testeurs-pc-v1',JSON.stringify({[inv[0][0]]:{n:2}})); }""", PCINV)

        print('3. le tableau de bord, avant toute vente')
        pg.goto(base + 'tableau.html'); pg.wait_for_timeout(2500)
        T = pg.locator('.pcbloc').inner_text()
        check('le bloc Perfume City est là', pg.locator('.pcbloc').count() == 1 and 'Perfume City' in pg.locator('body').inner_text())
        check('LE POINT — 5 flacons en rayon, et un seul tester même si la donnée ancienne en disait 2 (10 nov. 2026 : un par parfum, jamais plus)', '5' in T and '1 tester' in T and '2 testers' not in T, T[:300])
        check('capital 50 $ au prix d\'achat', '50' in T, T[:300])
        check('sans vente : il le dit simplement', 'Aucune vente Perfume City' in T, T[:400])

        print('1. une vente Perfume City, une vente ailleurs')
        pg.goto(base + 'ventes.html'); pg.wait_for_timeout(2500)
        def vend(cle, q, canal, client):
            pg.click('#nv'); pg.wait_for_timeout(250)
            pg.evaluate("([c,q])=>{ PANIER.push({cle:c,q:q,p:50}); peintPanier(); }", [cle, q])
            pg.evaluate("n=>{ $('v-canal').value=n; $('v-canal').dispatchEvent(new Event('change')); }", canal)
            pg.evaluate("()=>{ PANIER.forEach(l=>l.p=50); peintPanier(); }")   # le canal propose son prix : on fixe 50 $
            pg.fill('#v-client', client); pg.wait_for_timeout(150)
            pg.click('#v-ok'); pg.wait_for_timeout(600)
            pg.evaluate("()=>{ document.getElementById('docov').classList.remove('on'); }")
        pg.click('#nv'); pg.wait_for_timeout(250)
        opts = pg.evaluate("()=>[...$('v-canal').options].map(o=>o.value)")
        PC = next(o for o in opts if 'perfume' in o.lower() and 'city' in o.lower()); AUTRE = next(o for o in opts if o != PC)
        pg.evaluate("()=>{ $('vov').classList.remove('on'); }")
        vend(A[15], 2, PC, 'Cliente PC'); vend(B[15], 1, AUTRE, 'Client Autre')
        pg.evaluate("()=>{ $('fp').value='mois'; dessine(); }"); pg.wait_for_timeout(500)
        n_pc = pg.locator('tr.pcr').count(); n_tot = pg.evaluate("document.querySelectorAll('.tv2 tbody tr[data-d]').length")
        check('LE POINT — une seule ligne repérée Perfume City (la vente Perfume City)', n_pc == 1 and n_tot >= 2, (n_pc, n_tot))
        bg = pg.evaluate("()=>{ const t=document.querySelector('tr.pcr td:nth-child(3)'); return getComputedStyle(t).backgroundColor; }")
        bg2 = pg.evaluate("()=>{ const t=[...document.querySelectorAll('.tv2 tbody tr[data-d]')].find(r=>!r.classList.contains('pcr')); return getComputedStyle(t.querySelector('td:nth-child(3)')).backgroundColor; }")
        check('LE POINT — la ligne Perfume City n\'a PLUS de fond rose (Igal, 17 oct. : seule la pastille est rose)', bg == bg2 and 'rgb(253, 237, 243)' not in bg, (bg, bg2))
        check('pastille de canal rose', pg.locator('tr.pcr .ch.cpc').count() == 1)
        check('aucune autre pastille rose', pg.locator('tr:not(.pcr) .ch.cpc').count() == 0)

        print('2. le tableau de bord, après la vente')
        pg.goto(base + 'tableau.html'); pg.wait_for_timeout(2500)
        T = pg.locator('.pcbloc').inner_text()
        check('vendu 100 $ (2 × 50) et 2 flacons', '100' in T and '2 flacon' in T, T[:300])
        check('3 flacons en rayon après la vente', '3' in T.split('en rayon')[0][-12:], T[:300])
        check('le parfum vendu est dans « ce qu\'elle vend le mieux »', (A[1] or '').lower()[:8] in T.lower(), T[-300:])
        check('aucune erreur de page', not err, err[:3])
        b.close()
finally:
    srv.terminate()
print(f'\n{ok} ok, {len(ko)} KO')
if ko: print(ko); raise SystemExit(1)
