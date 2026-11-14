# LES COMMANDES DES SITES PAYÉES, PAS ENCORE EXPÉDIÉES, DANS VENTES (14 nov. 2026 — Igal : « même les commandes pas expédiées, je veux
# qu'elles soient notées quand même… je devrais les voir sur les lignes des ventes »). Ce test protège :
#   1. LE POINT — elles sont montrées au-dessus des ventes, dans un cadre à part : date, heure, n°, client, parfums, montant, origine ;
#   2. LE POINT — elles n'entrent dans AUCUN total (le chiffre d'affaires et le nombre de commandes ne bougent pas) — règle du 5 nov. :
#      une commande des sites n'est une vente qu'une fois « completed » ;
#   3. seules celles de la période, et jamais d'avant le démarrage de l'ERP (les vieilles commandes de 2023 restées « en cours ») ;
#   4. le filtre par canal : une commande du site de gros ne sort pas sous perfumestrade.com ;
#   5. le numéro ouvre la commande dans WooCommerce ; en anglais et en espagnol, tout est traduit ; aucune erreur JS.
import subprocess, time, socket, json
from playwright.sync_api import sync_playwright
D = '/home/claude/catalogue'
ok = 0; ko = []
def check(n, c, i=''):
    global ok
    if c: ok += 1; print('  ok  ', n)
    else: ko.append(n); print('  KO  ', n, str(i)[:500])
C = json.load(open(D + '/cat.json'))
A = [r for r in C if (r[6] or 0) > 0 and r[0] and r[0].isdigit() and (r[12] or 0) > 0][0]
F = [{'id': 'f1', 'num': '9101', 'sens': 'vente', 'canal': 'Site perfumestrade.com', 'auto': 'woocommerce', 'd': '2026-11-11', 'h': '12:00', 't': '2026-11-11T17:00:00Z', 'stock': False,
      'par': 'auto', '_i': 'fa|woocommerce|1', 'lignes': [{'cle': A[15], 'bc': A[0], 'ref': A[2] + ' ' + A[13], 'q': 1, 'p': 60}], 'montant': 60}]
ATT = {'maj': '2026-11-14T15:00:00Z', 'L': [
    {'id': 21450, 'n': '21450', 'd': '2026-11-13', 'h': '18:42', 'st': 'processing', 'mt': 110, 'port': 8, 'o': 'gads', 'cl': 'Laura J.', 'L': [['3614272732278', 'Valentino Uomo Intense EDP 3.4 oz', 1, 110]]},
    {'id': 21449, 'n': '21449', 'd': '2026-11-12', 'h': '09:05', 'st': 'on-hold', 'mt': 75, 'port': 0, 'o': 'direct', 'cl': 'Marc D.', 'L': [['1', 'Lattafa Asad EDP 3.4 oz', 3, 75]]},
    {'id': 5897, 'd': '2023-05-13', 'mt': 100, 'o': 'inconnu'}]}
ATTG = {'maj': '2026-11-14T15:00:00Z', 'L': [{'id': 777, 'n': '777', 'd': '2026-11-13', 'h': '10:00', 'st': 'processing', 'mt': 500, 'o': 'direct', 'cl': 'Shop X.', 'L': [['2', 'Coffret', 10, 500]]}]}
ORI = {'woocommerce|9101': 'gads', '_attente_woocommerce': ATT, '_attente_woocommerce-gros': ATTG}
s = socket.socket(); s.bind(('127.0.0.1', 0)); port = s.getsockname()[1]; s.close()
srv = subprocess.Popen(['python3', '-m', 'http.server', str(port), '--bind', '127.0.0.1'], cwd=D, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)
SESS = """([F,O,lg])=>{ localStorage.clear(); localStorage.setItem('sam-comptes-demo-v1','0');
  localStorage.setItem('sam-session-v1',JSON.stringify({id:'sam',nom:'Sam',role:'patron',depuis:new Date().toISOString()}));
  localStorage.setItem('langue-v1',lg); localStorage.setItem('factures-v1',JSON.stringify(F)); if(O) localStorage.setItem('ventes-origine-v1',JSON.stringify(O)); }"""
try:
    with sync_playwright() as p:
        b = p.chromium.launch(); err = []
        def ouvre(lg='fr', ori=ORI):
            pg = b.new_page(viewport={'width': 1500, 'height': 1000}); pg.on('pageerror', lambda e: err.append(str(e)))
            base = f'http://127.0.0.1:{port}/'
            pg.goto(base + 'accueil.html'); pg.wait_for_timeout(300); pg.evaluate(SESS, [F, ori, lg])
            pg.goto(base + 'ventes.html'); pg.wait_for_timeout(2500)
            pg.evaluate("()=>{ $('fp').value=''; canalSel=''; vus=80; dessine(); }"); pg.wait_for_timeout(500); return pg
        pg = ouvre()
        t = pg.inner_text('.vatt') if pg.locator('.vatt').count() else ''
        rows = pg.locator('.vatt tbody tr').all_inner_texts()
        check('LE POINT — un cadre « Payées sur le site, pas encore expédiées » au-dessus des ventes, avec date, heure, n°, client, parfums, montant et origine',
              'Payées sur le site, pas encore expédiées' in t and any('21450' in r and '18:42' in r and 'Laura J.' in r and 'Valentino Uomo Intense' in r and '110' in r and 'pub google' in r.lower() for r in rows), [t[:200], rows])
        check('l\'état est dit : « payée, à expédier » / « en attente (contrôle) » (bloquée par l\'anti-fraude)', any('payée, à expédier' in r for r in rows) and any('en attente (contrôle)' in r for r in rows), rows)
        check('LE POINT — les vieilles commandes restées « en cours » depuis 2023 n\'y sont pas (rien d\'avant le démarrage de l\'ERP)', not any('5897' in r for r in rows), rows)
        check('les deux sites y sont : 3 commandes (2 détail + 1 gros), 685 $', len(rows) == 3 and '685' in t, [len(rows), t[:160]])
        kp = ' '.join(pg.inner_text('#kpis').split())
        check('LE POINT — elles n\'entrent dans AUCUN total : le chiffre d\'affaires reste 60 $, 1 commande', '60' in kp and '685' not in kp and '1 commande' in kp, kp)
        href = pg.get_attribute('.vatt tbody tr:first-child .num a', 'href') or ''
        check('le numéro ouvre la commande dans WooCommerce (nouvel onglet)', 'perfumestrade.com/wp-admin/post.php?post=21450' in href, href)
        pg.evaluate("()=>{ canalSel='Site perfumestrade.com'; dessine(); }"); pg.wait_for_timeout(300)
        rows2 = pg.locator('.vatt tbody tr').all_inner_texts()
        check('filtre par canal : sous perfumestrade.com, la commande du site de gros n\'apparaît pas', len(rows2) == 2 and not any('777' in r for r in rows2), rows2)
        pg.evaluate("()=>{ canalSel=''; $('fp').value='jour'; $('fj').value='2026-11-12'; dessine(); }"); pg.wait_for_timeout(300)
        rows3 = pg.locator('.vatt tbody tr').all_inner_texts()
        check('un jour choisi : seulement les commandes de ce jour-là', len(rows3) == 1 and '21449' in rows3[0], rows3)
        pg.close()
        pg = ouvre(ori={'woocommerce|9101': 'gads'})
        check('sans commande en attente : pas de cadre du tout', pg.locator('.vatt').count() == 0)
        pg.close()
        for lg, titre, etat in (('en', 'Paid on the website, not shipped yet', 'paid, to ship'), ('es', 'Pagadas en el sitio, aún no enviadas', 'pagada, por enviar')):
            pg = ouvre(lg=lg); t = pg.inner_text('.vatt')
            check(f'{lg} : le cadre est traduit (« {titre} », « {etat} »)', titre in t and etat in t and 'Payées' not in t and 'expédier' not in t, t[:300])
            pg.close()
        check('aucune erreur JS', not err, err[:3])
        b.close()
finally:
    srv.terminate()
print(f'\n{ok} ok, {len(ko)} KO', ko); raise SystemExit(1 if ko else 0)
