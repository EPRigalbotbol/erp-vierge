# LES PRIX DES FICHES SONT PUBLIÉS POUR LES SITES (Igal, 10 nov. 2026 : « je ne veux pas qu'il y ait un bouton pour mettre à jour
# les prix et le stock, je veux que cela soit fait automatiquement »). Le Catalogue publie prix-erp-v1, que le cockpit suit pour remettre
# les prix des sites au niveau des fiches (woocommerce.js, egalisePrix). Ce test protège :
#   1. LE POINT — à l'ouverture du Catalogue (Patron), chaque produit des sites reçoit le prix de sa fiche : [retail, gros] ;
#   2. LE POINT — un prix changé dans une fiche est republié tout seul, quelques secondes après l'Enregistrer ;
#   3. un canal coupé pour ce parfum (« ne pas vendre ici ») publie « rien » pour ce site ; un parfum absent des sites n'est pas publié ;
#   4. deux fiches sur le même produit du site avec des prix différents : le code n'est pas publié (le cockpit ne devine jamais) ;
#   5. l'ancienne boîte (« …oldbox ») a sa propre ligne, distincte de la boîte ;
#   6. un rôle sans droit sur les prix des sites ne publie rien.
import pathlib, subprocess, time, socket, json, collections
from playwright.sync_api import sync_playwright
D = pathlib.Path('/home/claude/catalogue')
ok = 0; ko = []
def check(n, c, i=''):
    global ok
    if c: ok += 1; print('  ok  ', n)
    else: ko.append(n); print('  KO  ', n, str(i)[:500])
CAT = json.load(open(D / 'cat.json'))
U = [r for r in CAT if r[0] and str(r[0]).isdigit() and len(str(r[0])) >= 12 and r[7] and r[8] and r[15] and (r[6] or 0) > 0][:6]
A, Bp, C, Dp, E, F = U
par = collections.defaultdict(list)
for r in CAT:
    if r[0] and str(r[0]).isdigit() and len(str(r[0])) >= 12 and r[15]: par[str(r[0])].append(r)
BC2, (W, G) = next((k, v) for k, v in par.items() if len(v) == 2 and 'old' in (v[1][1] or '').lower())
s = socket.socket(); s.bind(('127.0.0.1', 0)); port = s.getsockname()[1]; s.close()
srv = subprocess.Popen(['python3', '-m', 'http.server', str(port), '--bind', '127.0.0.1'], cwd=str(D), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)
f = lambda pr: {'id': 1, 'q': 3, 'suivi': True, 'nom': 'x', 'pr': pr, 'ps': None}
SITE = {str(A[0]): {'d': f(1), 'g': f(1)}, str(Bp[0]): {'d': f(1), 'g': f(1)}, str(C[0]): {'d': f(1)}, BC2: {'d': f(1), 'g': f(1)}, BC2 + 'oldbox': {'d': f(1), 'g': f(1)},
        str(Dp[0]): {'d': f(1), 'g': f(1)}, '_maj': {'d': '2026-11-10T00:00:00Z', 'g': '2026-11-10T00:00:00Z'}}
# Dp et E : deux fiches sur le même code du site (E porte en plus le code de Dp), à des prix différents → ambigu
MOD = {Bp[15]: {'pcOff': ['sitegros']}, W[15]: {'pvr': 109, 'pvw': 53.76}, G[15]: {'bc': BC2 + 'oldbox', 'pvr': 118, 'pvw': 85},
       E[15]: {'bc': str(Dp[0]), 'pvr': float(Dp[7]) + 7}}
try:
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1456, 'height': 900}); err = []
        pg.on('pageerror', lambda e: err.append(str(e))); pg.on('dialog', lambda d: d.accept())
        def cockpit(route):
            body = json.loads(route.request.post_data or '{}') if route.request.post_data else {}
            j = {'ok': True, 'avant': body.get('attendu'), 'apres': {'barre': body.get('barre'), 'promo': None if body.get('promo') in ('', None) else body.get('promo')}} if '/site/prix' in route.request.url else {'ok': True}
            route.fulfill(status=200, content_type='application/json', body=json.dumps(j))
        pg.route('**/api/o/dasy/**', cockpit)
        base = f'http://127.0.0.1:{port}/'
        pg.goto(base + 'accueil.html'); pg.wait_for_timeout(300)
        def ouvre(role):
            pg.evaluate("""([S,M,role])=>{ localStorage.clear(); localStorage.setItem('sam-comptes-demo-v1','0'); localStorage.setItem('ck-token','jeton-test'); localStorage.setItem('sam-session-v1', JSON.stringify({id:'sam',nom:'Sam',role,depuis:new Date().toISOString()}));
              localStorage.setItem('site-stock-v1',JSON.stringify(S)); localStorage.setItem('fiches-modifiees-v1',JSON.stringify(M)); }""", [SITE, MOD, role])
            pg.goto(base + 'catalogue.html'); pg.wait_for_timeout(6000)
            return pg.evaluate("()=>JSON.parse(localStorage.getItem('prix-erp-v1')||'null')")
        T = ouvre('patron')
        P = (T or {}).get('p', {})
        check('LE POINT — publié à l\'ouverture : chaque produit des sites a le prix de sa fiche [retail, gros]', T and P.get(str(A[0])) == [A[7], A[8]], P.get(str(A[0])))
        check('un canal coupé (« ne pas vendre ici » sur le site de gros) publie « rien » pour ce site', P.get(str(Bp[0])) == [Bp[7], None], P.get(str(Bp[0])))
        check('un parfum présent sur un seul site : son prix de gros est publié aussi (le cockpit ne l\'écrit que là où il existe)', P.get(str(C[0])) == [C[7], C[8]], P.get(str(C[0])))
        check('LE POINT — l\'ancienne boîte a SA ligne (118 / 85), la boîte la sienne (109 / 53,76)', P.get(BC2) == [109, 53.76] and P.get(BC2 + 'oldbox') == [118, 85], [P.get(BC2), P.get(BC2 + 'oldbox')])
        check('deux fiches sur le même produit à des prix différents : pas publié, noté ambigu', str(Dp[0]) not in P and str(Dp[0]) in T.get('amb', []), [P.get(str(Dp[0])), T.get('amb')])
        check('un parfum absent des sites n\'est pas publié', str(F[0]) not in P)
        print('2. un prix changé dans une fiche est republié tout seul')
        pg.evaluate("c=>ouvreFiche(c)", A[15]); pg.wait_for_timeout(500)
        pg.fill('#ddb input[data-pc="site"]', str(A[7] + 4)); pg.locator('#ddb h3').first.click(); pg.wait_for_timeout(400)
        pg.locator('#dok').click(); pg.wait_for_timeout(600)
        if pg.evaluate("()=>document.getElementById('pxov').classList.contains('on')"):
            if pg.locator('#pxsites').count(): pg.uncheck('#pxsites')
            pg.click('#pxok')
        pg.wait_for_timeout(4500)
        T2 = pg.evaluate("()=>JSON.parse(localStorage.getItem('prix-erp-v1')||'null')")
        check('LE POINT — 4 s après l\'Enregistrer, le nouveau prix retail est publié (sans bouton)', T2['p'].get(str(A[0]))[0] == A[7] + 4 and T2['t'] > T['t'], [T2['p'].get(str(A[0])), T['t'], T2['t']])
        T3 = ouvre('commercial')
        check('un rôle sans droit sur les prix des sites ne publie rien', T3 is None, T3)
        check('aucune erreur JS', not err, err[:3])
        b.close()
finally:
    srv.terminate()
print(f'\n{ok} ok, {len(ko)} KO', ko); raise SystemExit(1 if ko else 0)
