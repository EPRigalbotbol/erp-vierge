# UN COMPTAGE PÉRIMÉ (Sam, 30 oct. 2026 : « Art of Universe, j'en ai acheté plusieurs, et l'Inventaire dit 0 et
# vérifié — je veux voir le stock actuel quand je recompte »). Le 2 oct. un comptage avait dit 0 ; une réception a
# ensuite mis le stock à 87. L'Inventaire montrait encore la case comptée « 0 » et le théorique d'AVANT ce comptage (1).
# Ce test protège :
#   1. LE POINT : quand le stock a bougé depuis le comptage, la ligne montre le stock d'aujourd'hui (87) et la case
#      comptée est vide — l'écart n'est pas calculé sur un vieux chiffre ;
#   2. recompter cette ligne part du stock d'aujourd'hui : compter 85 donne un écart de −2 (pas −1 ou +84), le stock
#      passe à 85, la ligne est vérifiée ;
#   3. un comptage frais (le stock n'a pas bougé depuis) reste affiché ; « Théorique » montre le stock réel (11 nov. 2026) ;
#   4. aucune erreur JS.
import subprocess, time, socket, json
from playwright.sync_api import sync_playwright
D = '/home/claude/catalogue'
ok = 0; ko = []
def check(n, c, i=''):
    global ok
    if c: ok += 1; print('  ok  ', n)
    else: ko.append(n); print('  KO  ', n, str(i)[:400])
s = socket.socket(); s.bind(('127.0.0.1', 0)); port = s.getsockname()[1]; s.close()
srv = subprocess.Popen(['python3', '-m', 'http.server', str(port), '--bind', '127.0.0.1'], cwd=D, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)
try:
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1500, 'height': 900}); err = []
        pg.on('pageerror', lambda e: err.append(str(e)))
        base = f'http://127.0.0.1:{port}/'
        pg.goto(base + 'accueil.html'); pg.wait_for_timeout(300)
        pg.evaluate("localStorage.setItem('sam-session-v1',JSON.stringify({id:'sam',nom:'Sam',role:'patron',depuis:new Date().toISOString()}));localStorage.setItem('langue-v1','fr')")
        pg.goto(base + 'stock.html'); pg.wait_for_timeout(2500)
        A, B = pg.evaluate("P.filter(p=>p.bc&&/^[0-9]+$/.test(p.bc)).slice(0,2).map(p=>({bc:p.bc,cle:p.cle}))")
        # A : compté 0 le 2 oct., puis une réception a mis 87 (périmé). B : compté 5, rien n'a bougé (frais).
        pg.evaluate("""([a,b])=>{ const M=lit('fiches-modifiees-v1',{})||{};
          M[a.cle]={verif:'ok',qteAv:1,qteTh0:1,qteC:0,verifPar:'Sam',verifLe:'2026-10-02T17:31:43.993Z',qte:87,pa:29.5};
          M[b.cle]={verif:'ok',qteTh0:7,qteC:5,qte:5,verifPar:'Sam',verifLe:'2026-10-29T10:00:00Z'};
          localStorage.setItem('fiches-modifiees-v1',JSON.stringify(M));
          localStorage.setItem('comptage-parfums-v1',JSON.stringify({[a.bc]:'0',[b.bc]:'5'})); }""", [A, B])
        pg.goto(base + 'stock.html'); pg.wait_for_timeout(2500)
        pg.fill('#q', A['bc']); pg.wait_for_timeout(500)
        tr = pg.locator(f'tr[data-bc="{A["bc"]}"]')
        tds = tr.locator('td').all_inner_texts()
        v = tr.locator('input.cnt').input_value()
        check('LE POINT — le stock a bougé depuis le comptage : la ligne montre le stock d\'aujourd\'hui (87)', '87' in tds[3], tds)
        check('… et la case comptée est vide (le vieux « 0 » ne s\'affiche plus), pas d\'écart', v == '' and tds[5].strip() in ('—', ''), [v, tds[5]])
        inp = tr.locator('input.cnt'); inp.fill('85'); inp.press('Tab'); pg.wait_for_timeout(700)
        m = pg.evaluate("c=>lit('fiches-modifiees-v1',{})[c]||{}", A['cle'])
        check('LE POINT — recompter part du stock d\'aujourd\'hui : 85 comptés, stock 85, théorique d\'avant 87', m.get('qte') == 85 and m.get('qteC') == 85 and m.get('qteTh0') == 87 and m.get('verif') == 'ok', m)
        tds = pg.locator(f'tr[data-bc="{A["bc"]}"] td').all_inner_texts()
        # 11 nov. 2026 (Igal : « quand c'est vérifié, enlève le chiffre théorique ») : vérifiée, la ligne montre le stock réel (85), écart 0 ;
        # l'ancien chiffre reste au journal (87 → 85)
        check('vérifiée : « Théorique » montre le stock réel (85), plus l\'ancien chiffre', tds[3].strip().startswith('85') and tds[5].strip() in ('0', '—'), tds)
        J = pg.evaluate("lit('crm-journal-v1',[]).filter(j=>j.lib==='quantité corrigée par comptage').slice(-1)[0]||null")
        check('le journal dit 87 → 85', J and J.get('av') == 87 and J.get('ap') == 85, J)
        pg.fill('#q', B['bc']); pg.wait_for_timeout(500)
        tr = pg.locator(f'tr[data-bc="{B["bc"]}"]')
        tds = tr.locator('td').all_inner_texts(); v = tr.locator('input.cnt').input_value()
        check('un comptage frais reste affiché : case 5, « Théorique » = 5 (le stock réel, plus le 7 d\'avant), écart 0', v == '5' and tds[3].strip().startswith('5') and tds[5].strip() in ('0', '—'), [v, tds])
        check('aucune erreur JS', not err, err[:3])
        b.close()
finally:
    srv.terminate()
print(f"\n{ok} ok, {len(ko)} KO", ko)
