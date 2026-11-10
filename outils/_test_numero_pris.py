# LE NUMÉRO PROPOSÉ, PRIS ENTRE-TEMPS PAR QUELQU'UN D'AUTRE (Sam, 10 nov. 2026 : « je clique sur Save the offer, un message apparaît
# et rien ne bouge »). Le numéro de la pièce est proposé à l'ouverture ; si Miguel enregistre une cote entre-temps, il prend ce numéro
# et l'enregistrement de Sam était refusé (« ce numéro existe déjà ») — sur la page Offre, la case du numéro ne se voit même pas.
# Ce test protège :
#   1. LE POINT — page Offre : le numéro proposé pris entre-temps est remplacé par le suivant libre, l'offre s'enregistre ;
#   2. même chose pour une cote ;
#   3. un numéro TAPÉ à la main et déjà pris reste refusé, avec le message dans la langue de la page ;
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
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1280, 'height': 800}); err = []
        pg.on('pageerror', lambda e: err.append(str(e))); pg.on('dialog', lambda d: d.accept())
        base = f'http://127.0.0.1:{port}/'
        def ouvre(page, lg):
            pg.goto(base + 'accueil.html'); pg.wait_for_timeout(300)
            pg.evaluate("""lg=>{ localStorage.clear(); localStorage.setItem('sam-comptes-demo-v1','0'); localStorage.setItem('langue-v1',lg);
              localStorage.setItem('sam-comptes-v1',JSON.stringify([{ident:'sam',nom:'Sam',role:'patron',actif:true,h:'x'}]));
              localStorage.setItem('sam-session-v1',JSON.stringify({id:'sam',nom:'Sam',role:'patron',depuis:new Date().toISOString()})); }""", lg)
            pg.goto(base + page); pg.wait_for_timeout(3000)
            return pg.evaluate("""()=>{ window.coteNouvelle(); const ks=Object.keys(IDX).filter(c=>pvwEff(c)>0).slice(0,2); ks.forEach(k=>PANIER.push({cle:k,q:1,p:prixLigne(k,canalCour())}));
              $('v-client').value='Client Test'; peintPanier(); recap(); return $('v-num').value; }""")
        def autre_prend(num):   # Miguel enregistre une cote avec ce numéro, depuis un autre poste
            pg.evaluate("""n=>{ FACT.push({id:'miguel1',num:n,sens:'devis',tiers:'Autre',d:ajd(),lignes:[]}); ecrit('factures-v1',FACT); }""", num)
        for page, quoi in [('offres.html', 'offre'), ('quotes.html', 'cote')]:
            n0 = ouvre(page, 'en'); autre_prend(n0)
            pg.click('#v-ok'); pg.wait_for_timeout(1500)
            r = pg.evaluate("n=>({n:FACT.filter(f=>f.tiers==='Client Test').map(f=>f.num), msg:$('v-msg').textContent})", n0)
            check(f'LE POINT — {quoi} : le numéro {n0} pris entre-temps → la pièce s\'enregistre sous le suivant libre', len(r['n']) == 1 and r['n'][0] != n0 and 'exists' not in r['msg'], r)
        n0 = ouvre('quotes.html', 'en'); autre_prend('V999999-001')
        pg.evaluate("()=>{ $('v-num').value='V999999-001'; $('v-num').dispatchEvent(new Event('input',{bubbles:true})); }"); pg.click('#v-ok'); pg.wait_for_timeout(1200)
        r = pg.evaluate("()=>({n:FACT.filter(f=>f.tiers==='Client Test').length, msg:$('v-msg').textContent})")
        check('un numéro tapé à la main et déjà pris reste refusé, message en anglais', r['n'] == 0 and r['msg'].startswith('Number V999999-001 already exists'), r)
        check('aucune erreur JS', not err, err[:3])
        b.close()
finally:
    srv.terminate()
print(f'\n{ok} ok, {len(ko)} KO', ko); raise SystemExit(1 if ko else 0)
