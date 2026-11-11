# METTRE EN LIGNE UN PARFUM SANS STOCK (11 nov. 2026). Le matin : « prévenir, pas refuser » ; puis, avec le retrait automatique à 0 :
# « on le refuse avec un message » (sinon il serait retiré aussitôt). Ce test protège LA DÉCISION FINALE :
# Ce test protège :
#   1. LE POINT — à 0, « Mettre en ligne » est refusé avec un message clair, rien ne part au site ;
#   2. chez Perfume City, le message parle de son inventaire ;
#   3. aucune erreur JS.
import subprocess, time, socket, json
from playwright.sync_api import sync_playwright
D = '/home/claude/catalogue'; ok = 0; ko = []
def check(n, c, i=''):
    global ok
    if c: ok += 1; print('  ok  ', n)
    else: ko.append(n); print('  KO  ', n, str(i)[:400])
C = json.load(open(D + '/cat.json'))
A = [r for r in C if r[0] and r[0].isdigit() and len(r[0]) == 13 and (r[8] or 0) > 0 and r[15]][3]
s = socket.socket(); s.bind(('127.0.0.1', 0)); port = s.getsockname()[1]; s.close()
srv = subprocess.Popen(['python3', '-m', 'http.server', str(port), '--bind', '127.0.0.1'], cwd=D, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)
try:
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1500, 'height': 1000}); err = []; dialogues = []; repond = {'ok': True}
        pg.on('pageerror', lambda e: err.append(str(e)))
        pg.on('dialog', lambda d: (dialogues.append(d.message), d.accept() if repond['ok'] else d.dismiss()))
        envois = []
        def creation(route):
            body = json.loads(route.request.post_data or '{}'); envois.append((route.request.url, body)); it = body['items'][0]
            route.fulfill(status=200, content_type='application/json', body=json.dumps({'ok': True, 'creees': 1, 'lignes': [{'bc': it['bc'], 'etat': 'en ligne', 'id': 9001, 'zero': True, 'prix': it.get('barre')}]}))
        pg.route('**/api/o/dasy/site/cree', creation); pg.route('**/api/o/dasy/shopify/cree', creation)
        pg.route('**/api/o/dasy/shopify/droits', lambda r: r.fulfill(status=200, content_type='application/json', body=json.dumps({'relie': True, 'ecriture': True, 'stock': True})))
        base = f'http://127.0.0.1:{port}/'
        pg.goto(base + 'accueil.html'); pg.wait_for_timeout(300)
        pg.evaluate("""a=>{ localStorage.clear(); localStorage.setItem('sam-comptes-demo-v1','0');
          localStorage.setItem('sam-session-v1',JSON.stringify({id:'sam',nom:'Sam',role:'patron',depuis:new Date().toISOString()}));
          localStorage.setItem('ck-token','jeton-test'); localStorage.setItem('langue-v1','fr');
          localStorage.setItem('site-stock-v1',JSON.stringify({_maj:{d:'2026-11-10T08:00:00Z'}}));
          localStorage.setItem('shopify-pc-prix-v1',JSON.stringify({_maj:'2026-11-10T08:00:00Z'}));
          const M={}; M[a]={qte:0}; localStorage.setItem('fiches-modifiees-v1',JSON.stringify(M)); }""", A[15])
        pg.goto(base + 'catalogue.html#cle=' + A[15] + '&canaux=1'); pg.wait_for_timeout(3500)
        q = pg.evaluate("c=>{ const p=tousLesArticles().find(x=>x.id===c); return p&&p.qte; }", A[15])
        bt = pg.locator('[data-mel1="site"]')
        check('à 0 en stock, le bouton « Mettre en ligne » est là', q == 0 and bt.count() == 1, (q, bt.count()))
        bt.click(); pg.wait_for_timeout(1200)
        check('LE POINT — refusé avec le message « 0 en stock : il n\'est pas mis en ligne », rien ne part', dialogues and "à 0 en stock : il n'est pas mis en ligne" in dialogues[-1] and not envois, (dialogues[-1:], envois))
        pc = pg.locator('[data-mel1="perfumecity"]'); dialogues.clear()
        if pc.count(): pc.click(); pg.wait_for_timeout(1200)
        check('Perfume City : refusé, le message parle de l\'inventaire Perfume City, rien ne part', dialogues and "Perfume City n'a pas ce parfum en stock" in dialogues[-1] and not envois, dialogues)
        check('aucune erreur JS', not err, err[:3])
        b.close()
finally:
    srv.terminate()
print(f'\n{ok} ok, {len(ko)} KO', ko); raise SystemExit(1 if ko else 0)
