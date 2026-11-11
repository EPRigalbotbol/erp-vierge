# « VOIR LA FICHE » SUR LA LISTE DES PARFUMS À COCHER (Igal, 11 nov. 2026 : « dans l'offre, lorsqu'on choisit un parfum, sur la ligne
# du parfum, “voir la fiche” »). Ce test protège, sur les pages Offre et Cote :
#   1. LE POINT — chaque parfum de la liste à cocher a son bouton « Voir la fiche », qui ouvre SA fiche du Catalogue en panneau à droite ;
#   2. le clic n'a ni coché ni décoché la ligne, et la liste est toujours là à la fermeture ;
#   3. le bouton est traduit (See the sheet) ;
#   4. aucune erreur JS.
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
        pg.on('pageerror', lambda e: err.append(str(e)))
        base = f'http://127.0.0.1:{port}/'
        pg.goto(base + 'accueil.html'); pg.wait_for_timeout(300)
        pg.evaluate("""()=>{ localStorage.clear(); localStorage.setItem('sam-comptes-demo-v1','0'); localStorage.setItem('langue-v1','en');
          localStorage.setItem('sam-comptes-v1',JSON.stringify([{ident:'sam',nom:'Sam',role:'patron',actif:true,h:'x'}]));
          localStorage.setItem('sam-session-v1',JSON.stringify({id:'sam',nom:'Sam',role:'patron',depuis:new Date().toISOString()})); }""")
        for page in ['offres.html', 'quotes.html']:
            pg.goto(base + page); pg.wait_for_timeout(3000)
            pg.evaluate("window.coteNouvelle()"); pg.fill('#v-q', 'night'); pg.wait_for_timeout(800)
            n = pg.evaluate("[document.querySelectorAll('#v-res .cand').length, document.querySelectorAll('#v-res .cand [data-vfc]').length, (document.querySelector('#v-res [data-vfc]')||{}).textContent||'']")
            check(f'{page} : chaque parfum de la liste a son bouton (« See the sheet »)', n[0] > 1 and n[0] == n[1] and 'See the sheet' in n[2], n)
            cle = pg.evaluate("document.querySelectorAll('#v-res [data-vfc]')[1].dataset.vfc")
            pg.click('#v-res [data-vfc] >> nth=1'); pg.wait_for_timeout(900)
            src = pg.evaluate("(document.querySelector('#fv-ov iframe')||{}).src||''")
            check(f'LE POINT — {page} : le bouton ouvre la fiche de CE parfum en panneau à droite', ('cle=' + cle) in src and 'cadre=1' in src, (cle, src))
            coch = pg.evaluate("document.querySelectorAll('#v-res .cand.coche').length")
            pg.evaluate("window.postMessage({fiche:'fermee'},location.origin)"); pg.wait_for_timeout(500)
            check(f'{page} : rien de coché, la liste est toujours là à la fermeture', coch == 0 and pg.evaluate("$('v-res').classList.contains('on') && document.querySelectorAll('#v-res .cand').length") == n[0], coch)
        check('aucune erreur JS', not err, err[:3])
        b.close()
finally:
    srv.terminate()
print(f'\n{ok} ok, {len(ko)} KO', ko); raise SystemExit(1 if ko else 0)
