# LE RÉGLAGE « RETRAIT AUTOMATIQUE À 0 EN STOCK » (Igal, 11 nov. 2026 : « explique-moi ce que c'est le réglage… l'interrupteur »).
# Ce test protège : 1. LE POINT — la case existe dans Réglages, décochée au départ ; cochée (et confirmée), le réglage retraitZero
# est enregistré (le cockpit le relit) et le journal le dit ; 2. Annuler la confirmation ne l'allume pas ; 3. décochée : éteint ;
# 4. en anglais et en espagnol, plus un mot de français dans cette ligne ; 5. aucune erreur JS.
import subprocess, time, socket, re
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
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1400, 'height': 900}); err = []; rep = {'ok': True}
        pg.on('pageerror', lambda e: err.append(str(e))); pg.on('dialog', lambda d: d.accept() if rep['ok'] else d.dismiss())
        base = f'http://127.0.0.1:{port}/'
        def ouvre(lg='fr'):
            pg.goto(base + 'accueil.html'); pg.wait_for_timeout(300)
            pg.evaluate("""lg=>{ localStorage.setItem('sam-comptes-demo-v1','0'); localStorage.setItem('langue-v1',lg);
              localStorage.setItem('sam-session-v1',JSON.stringify({id:'sam',nom:'Sam',role:'patron',depuis:new Date().toISOString()})); }""", lg)
            pg.goto(base + 'reglages.html'); pg.wait_for_timeout(2500)
            pg.evaluate("()=>{ const e=document.getElementById('sec-zero'); if(e){ let x=e; while(x){ if(x.tagName==='DETAILS') x.open=true; x=x.parentElement; } } }")
        pg.goto(base + 'accueil.html'); pg.evaluate("localStorage.clear()"); ouvre()
        check('LE POINT — la case existe, décochée au départ', pg.locator('#r-zero').count() == 1 and not pg.is_checked('#r-zero'))
        rep['ok'] = False; pg.evaluate("()=>{ const c=document.getElementById('r-zero'); c.checked=true; c.dispatchEvent(new Event('change')); }"); pg.wait_for_timeout(300)
        check('Annuler la confirmation : reste éteint', pg.evaluate("lit('reglages-v1',{}).retraitZero") is not True and not pg.is_checked('#r-zero'))
        rep['ok'] = True; pg.evaluate("()=>{ const c=document.getElementById('r-zero'); c.checked=true; c.dispatchEvent(new Event('change')); }"); pg.wait_for_timeout(300)
        check('LE POINT — cochée et confirmée : retraitZero enregistré, « Allumé »', pg.evaluate("lit('reglages-v1',{}).retraitZero") is True and 'Allumé' in pg.inner_text('#e-zero'))
        pg.wait_for_timeout(1200)
        check('le journal le dit', any('retrait automatique' in (j.get('lib') or '') for j in pg.evaluate("lit('crm-journal-v1',[])")))
        pg.evaluate("()=>{ const c=document.getElementById('r-zero'); c.checked=false; c.dispatchEvent(new Event('change')); }"); pg.wait_for_timeout(300)
        check('décochée : éteint', pg.evaluate("lit('reglages-v1',{}).retraitZero") is False)
        FR = re.compile(r'\b(parfum|retiré|stock revient|Coché|Décoché|toi-même|Éteint|rien)\b')
        for lg in ('en', 'es'):
            ouvre(lg)
            t = pg.evaluate("()=>{ const e=document.getElementById('sec-zero')||document.getElementById('r-zero').closest('section'); return e?e.innerText:''; }")
            check(f'{lg} : la ligne est traduite, plus un mot de français', t and not FR.search(t), FR.findall(t))
        check('aucune erreur JS', not err, err[:3])
        b.close()
finally:
    srv.terminate()
print(f'\n{ok} ok, {len(ko)} KO', ko); raise SystemExit(1 if ko else 0)
