# L'OFFRE S'ENREGISTRE MÊME QUAND LA PAGE EST EN TRAIN D'ENVOYER AUTRE CHOSE (Sam, 10 nov. 2026 : « l'offre ne se save pas et ça
# ne se ferme pas »). Avant d'enregistrer, le stock est relu sur le serveur ; tant qu'un autre envoi de la page est en route, cette
# relecture répond « non » et l'enregistrement était refusé (« le serveur ne répond pas »). Ce test protège :
#   1. LE POINT — page Offre : serveur « occupé », l'offre s'enregistre quand même, la fenêtre repart à zéro, pas d'alerte ;
#   2. même chose pour une cote ;
#   3. une VENTE qui sort du stock attend toujours la relecture : serveur occupé → alerte, rien d'enregistré ;
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
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1280, 'height': 800}); err = []; alertes = []
        pg.on('pageerror', lambda e: err.append(str(e))); pg.on('dialog', lambda d: (alertes.append(d.message), d.accept()))
        base = f'http://127.0.0.1:{port}/'
        def ouvre(page):
            pg.goto(base + 'accueil.html'); pg.wait_for_timeout(300)
            pg.evaluate("""()=>{ localStorage.clear(); localStorage.setItem('sam-comptes-demo-v1','0'); localStorage.setItem('langue-v1','en');
              localStorage.setItem('sam-comptes-v1',JSON.stringify([{ident:'sam',nom:'Sam',role:'patron',actif:true,h:'x'}]));
              localStorage.setItem('sam-session-v1',JSON.stringify({id:'sam',nom:'Sam',role:'patron',depuis:new Date().toISOString()})); }""")
            pg.goto(base + page); pg.wait_for_timeout(3000)
            pg.evaluate("""()=>{ window.__syEnLigne=()=>true; window.__syFrais=()=>Promise.resolve(false);   /* un autre envoi est en route */
              if(window.coteNouvelle) window.coteNouvelle(); else ouvreVente();
              const ks=Object.keys(IDX).filter(c=>pvwEff(c)>0).slice(0,2); ks.forEach(k=>PANIER.push({cle:k,q:1,p:prixLigne(k,canalCour())}));
              $('v-client').value='Client Test'; peintPanier(); recap(); }""")
        for page, quoi in [('offres.html', 'offre'), ('quotes.html', 'cote')]:
            alertes.clear(); ouvre(page)
            pg.click('#v-ok'); pg.wait_for_timeout(1500)
            r = pg.evaluate("()=>({n:FACT.filter(f=>f.tiers==='Client Test').length, pan:PANIER.length})")
            check(f'LE POINT — {quoi} : serveur occupé, elle s\'enregistre quand même et la fenêtre repart à zéro, sans alerte', r['n'] == 1 and r['pan'] == 0 and not alertes, (r, alertes))
        alertes.clear(); ouvre('ventes.html')
        pg.evaluate("()=>{ $('v-stock').checked=true; recap(); }")
        pg.click('#v-ok'); pg.wait_for_timeout(1500)
        r = pg.evaluate("()=>FACT.filter(f=>f.tiers==='Client Test').length")
        check('une vente qui sort du stock attend la relecture : serveur occupé → alerte, rien d\'enregistré', r == 0 and any('server' in a.lower() or 'serveur' in a.lower() for a in alertes), (r, alertes))
        check('aucune erreur JS', not err, err[:3])
        b.close()
finally:
    srv.terminate()
print(f'\n{ok} ok, {len(ko)} KO', ko); raise SystemExit(1 if ko else 0)
