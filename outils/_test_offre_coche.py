# COCHER = METTRE DANS L'OFFRE (Igal, 11 nov. 2026 : « j'ai sélectionné des parfums ; quand je change de marque, ils ont disparu,
# ils ne sont pas sur l'offre »). Ce test protège, page Offre :
#   1. LE POINT — cocher un parfum le met tout de suite dans l'offre (la ligne apparaît dessous) ;
#   2. LE POINT — chercher une autre marque et en cocher d'autres : les premiers restent dans l'offre ;
#   3. décocher retire la ligne ; revenir à la première marque montre les cases cochées ;
#   4. l'offre s'enregistre avec tous les parfums cochés ;
#   5. aucune erreur JS.
import subprocess, time, socket
from playwright.sync_api import sync_playwright
D = '/home/claude/catalogue'; ok = 0; ko = []
def check(n, c, i=''):
    global ok
    if c: ok += 1; print('  ok  ', n)
    else: ko.append(n); print('  KO  ', n, str(i)[:300])
s = socket.socket(); s.bind(('127.0.0.1', 0)); port = s.getsockname()[1]; s.close()
srv = subprocess.Popen(['python3', '-m', 'http.server', str(port), '--bind', '127.0.0.1'], cwd=D, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)
try:
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1280, 'height': 900}); err = []
        pg.on('pageerror', lambda e: err.append(str(e))); pg.on('dialog', lambda d: d.accept())
        base = f'http://127.0.0.1:{port}/'
        pg.goto(base + 'accueil.html'); pg.wait_for_timeout(300)
        pg.evaluate("""()=>{ localStorage.clear(); localStorage.setItem('sam-comptes-demo-v1','0'); localStorage.setItem('langue-v1','fr');
          localStorage.setItem('sam-comptes-v1',JSON.stringify([{ident:'sam',nom:'Sam',role:'patron',actif:true,h:'x'}]));
          localStorage.setItem('sam-session-v1',JSON.stringify({id:'sam',nom:'Sam',role:'patron',depuis:new Date().toISOString()})); }""")
        pg.goto(base + 'offres.html'); pg.wait_for_timeout(3000)
        pg.evaluate("window.coteNouvelle()"); pg.fill('#v-client', 'Client Test')
        pg.fill('#v-q', 'bvlgari'); pg.wait_for_timeout(600)
        pg.locator('#v-res .cand').nth(0).click(); pg.locator('#v-res .cand').nth(1).click(); pg.wait_for_timeout(300)
        check('LE POINT — cocher met tout de suite le parfum dans l\'offre', pg.evaluate("PANIER.length") == 2 and pg.locator('#v-pan tbody tr').count() == 2)
        pg.fill('#v-q', 'versace'); pg.wait_for_timeout(600)
        pg.locator('#v-res .cand').nth(0).click(); pg.wait_for_timeout(300)
        check('LE POINT — une autre marque : les deux premiers restent, le nouveau s\'ajoute (3)', pg.evaluate("PANIER.length") == 3)
        pg.fill('#v-q', 'bvlgari'); pg.wait_for_timeout(600)
        check('revenu à la première marque : ses deux parfums sont cochés', pg.locator('#v-res .cand.coche').count() == 2)
        pg.locator('#v-res .cand').nth(1).click(); pg.wait_for_timeout(300)
        check('décocher retire la ligne (2)', pg.evaluate("PANIER.length") == 2)
        pg.click('#v-cadd'); pg.wait_for_timeout(300)
        check('« Fermer la liste » vide la recherche, l\'offre garde ses parfums', not pg.locator('#v-res').is_visible() and pg.evaluate("PANIER.length") == 2)
        for i in range(2): pg.locator('#v-pan input[data-f="p"]').nth(i).fill('20'); pg.locator('#v-pan input[data-f="p"]').nth(i).press('Tab')
        pg.click('#v-ok'); pg.wait_for_timeout(1500)
        r = pg.evaluate("()=>{ const f=FACT.find(x=>x.tiers==='Client Test'); return f&&{offre:!!(f.doc&&f.doc.offre), n:(f.lignes||[]).length}; }")
        check('l\'offre s\'enregistre avec les 2 parfums', r and r['offre'] and r['n'] == 2, r)
        check('aucune erreur JS', not err, err[:3])
        b.close()
finally:
    srv.terminate()
print(f'\n{ok} ok, {len(ko)} KO', ko); raise SystemExit(1 if ko else 0)
