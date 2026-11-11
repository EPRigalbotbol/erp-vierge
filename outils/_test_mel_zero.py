# METTRE EN LIGNE UN PARFUM SANS STOCK : PRÉVENIR, PAS REFUSER (Igal, 11 nov. 2026 : « si Sam met en ligne un produit alors qu'il n'y a
# pas de stock, je ne veux pas que l'ERP le refuse. Juste un message : attention, ton stock est à zéro… as-tu reçu de la marchandise ? »).
# Ce test protège :
#   1. LE POINT — un parfum à 0 a quand même son bouton « Mettre en ligne » dans la fiche (site et Perfume City) ;
#   2. LE POINT — le clic montre l'avertissement « ton stock est à zéro … As-tu reçu de la marchandise ? », et, accepté, la mise en
#      ligne part (plus de « Pas de stock : rien à mettre en vente ») ;
#   3. chez Perfume City, l'avertissement parle du stock de Perfume City (son inventaire) ;
#   4. refusé (Annuler), rien ne part ;
#   5. aucune erreur JS.
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
        check('LE POINT — à 0 en stock, le bouton « Mettre en ligne » du site est là', q == 0 and bt.count() == 1, (q, bt.count()))
        repond['ok'] = False; bt.click(); pg.wait_for_timeout(800)
        check('refusé (Annuler) : rien ne part', not envois and dialogues and 'ton stock est à zéro' in dialogues[-1], dialogues[-1:])
        repond['ok'] = True; dialogues.clear()
        pg.locator('[data-mel1="site"]').click(); pg.wait_for_timeout(2500)
        check('LE POINT — l\'avertissement : « ton stock est à zéro … As-tu reçu de la marchandise ? »', dialogues and 'ton stock est à zéro' in dialogues[0] and 'As-tu reçu de la marchandise' in dialogues[0], dialogues)
        check('LE POINT — accepté, la mise en ligne part quand même (plus de refus)', len(envois) == 1 and envois[0][0].endswith('/site/cree') and envois[0][1]['items'][0]['qte'] == 0, envois)
        pc = pg.locator('[data-mel1="perfumecity"]')
        if pc.count():
            dialogues.clear(); pc.click(); pg.wait_for_timeout(2500)
            check('Perfume City : l\'avertissement parle du stock de Perfume City, et ça part', dialogues and 'stock de Perfume City est à zéro' in dialogues[0] and envois[-1][0].endswith('/shopify/cree'), dialogues)
        else:
            check('Perfume City : le bouton est là aussi', False, 'pas de bouton data-mel1=perfumecity')
        check('aucune erreur JS', not err, err[:3])
        b.close()
finally:
    srv.terminate()
print(f'\n{ok} ok, {len(ko)} KO', ko); raise SystemExit(1 if ko else 0)
