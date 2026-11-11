# UNE FICHE RETIRÉE DE LA VENTE REPASSE EN LIGNE (12 oct. 2026, refait le 11 nov. 2026 — Sam : « plus de prix barré » ; « Pas en ligne »
# et un bouton « Mettre en ligne »). Ce test protège :
#   1. un commercial voit « Pas en ligne », sans bouton ;
#   2. le Patron voit « Pas en ligne » + « Mettre en ligne » ; un Enregistrer ordinaire ne republie JAMAIS une fiche retirée exprès ;
#   3. LE POINT — « Mettre en ligne » (une fenêtre, OK) : le gros repart au prix de la ligne, republier:true, sans promo ; la fiche quitte
#      les retirées et la ligne dit « ✓ En ligne » ;
#   4. LE POINT — le détail repart au prix retail de la fiche, SANS prix barré (même si le site en gardait un) ;
#   5. Annuler n'envoie rien ; un refus du cockpit laisse la fiche retirée ;
#   6. aucune erreur JS.
import pathlib, subprocess, time, socket, json
from playwright.sync_api import sync_playwright
D = pathlib.Path('/home/claude/catalogue')
ok = 0; ko = []
def check(n, c, i=''):
    global ok
    if c: ok += 1; print('  ok  ', n)
    else: ko.append(n); print('  KO  ', n, i)
CAT = json.load(open(D / 'cat.json'))
P = next(r for r in CAT if (r[6] or 0) > 2 and r[12] and r[0] and len(str(r[0])) == 12 and str(r[0]).startswith('0') and sum(1 for x in CAT if x[0] == r[0]) == 1)
BC, PA, PVR = str(P[0]), float(P[12]), float(P[7] or 0)
s = socket.socket(); s.bind(('127.0.0.1', 0)); port = s.getsockname()[1]; s.close()
srv = subprocess.Popen(['python3', '-m', 'http.server', str(port), '--bind', '127.0.0.1'], cwd=str(D), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1)
SANS0 = BC.lstrip('0')
SITE0 = {BC: {'d': {'id': 101, 'q': 5, 'suivi': True, 'etat': 'instock', 'nom': 'x', 'pr': PVR + 20, 'ps': PVR}},
         '_retires': {'g': {SANS0: {'id': 201, 'q': 4, 'suivi': True, 'nom': 'x', 'pr': None, 'ps': None, 't': '2026-10-07T21:00:00Z'}}}}
try:
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1456, 'height': 900}); err = []
        pg.on('pageerror', lambda e: err.append(str(e)))
        dialogs = []
        def dlg(d): dialogs.append(d.message); d.accept()
        pg.on('dialog', dlg)
        def sauve(ms=1200):
            # la fenêtre unique de l'Enregistrer (20 oct.) : son texte tient la place de l'ancienne confirmation, on la valide
            pg.locator('#dok').click(); pg.wait_for_timeout(500)
            if pg.evaluate("()=>document.getElementById('pxov').classList.contains('on')"):
                dialogs.append(pg.inner_text('#pxb')); pg.click('#pxok')
            pg.wait_for_timeout(ms)
        envois = []; rep = {'s': 200, 'j': None}
        def cockpit(route):
            body = json.loads(route.request.post_data or '{}'); envois.append(body)
            j = rep['j'] or {'ok': True, 'republie': True, 'avant': {'barre': None, 'promo': None}, 'apres': {'barre': body.get('barre'), 'promo': None if body.get('promo') in ('', None) else body.get('promo')}}
            route.fulfill(status=rep['s'], content_type='application/json', body=json.dumps(j))
        pg.route('**/api/o/dasy/site/prix', cockpit)
        base = f'http://127.0.0.1:{port}/'
        pg.goto(base + 'accueil.html'); pg.wait_for_timeout(400)
        def pose(role): pg.evaluate("r=>localStorage.setItem('sam-session-v1', JSON.stringify({id:r==='patron'?'sam':'juan',nom:r==='patron'?'Sam':'Juan',role:r,depuis:new Date().toISOString()}))", role)
        def ouvre(S=None):
            pg.evaluate("s=>localStorage.setItem('site-stock-v1', JSON.stringify(s))", S or SITE0)
            pg.goto(base + 'catalogue.html'); pg.wait_for_timeout(2500)
            pg.evaluate("bc=>ouvreFiche(cur.find(p=>String(p.bc)===bc).id)", BC); pg.wait_for_timeout(500)
        def boite(cid='sitegros'):
            pg.evaluate("c=>{ const d=document.querySelector('[data-sbr=\"'+c+'\"]'); const x=d&&d.closest('details'); if(x) x.open=true; }", cid)
            return pg.locator(f'[data-sbr="{cid}"]')
        def enregistre(): sauve(1300)
        def retail(v):
            pg.locator('input[data-pc="site"]').fill(str(v)); pg.locator('#ddb h3').first.click(); pg.wait_for_timeout(400)
        pg.add_init_script("document.addEventListener('DOMContentLoaded',()=>{const s=document.createElement('style');s.textContent='#svtem{display:none!important}';document.head.appendChild(s)})")
        pg.evaluate("localStorage.setItem('ck-token','jeton-test')")
        def ligne(cid): return pg.locator(f'[data-cn="{cid}"]')
        print('1. un commercial')
        pose('commercial'); ouvre()
        check('« Pas en ligne » sur le gros, sans bouton', 'Pas en ligne' in ligne('sitegros').inner_text() and ligne('sitegros').locator('button').count() == 0, ligne('sitegros').inner_text())
        print('2. le Patron')
        pose('patron'); ouvre()
        check('« Pas en ligne » + « Mettre en ligne » sur le gros retiré', 'Pas en ligne' in ligne('sitegros').inner_text() and ligne('sitegros').locator('[data-remet="sitegros"]').count() == 1)
        check('le détail (en ligne) : « ✓ En ligne » + « Retirer de la vente »', 'En ligne' in ligne('site').inner_text() and ligne('site').locator('[data-retv="site"]').count() == 1)
        check('rien n\'est en attente : un Enregistrer ordinaire ne republie jamais une fiche retirée', pg.evaluate("boitesEnAttente().filter(x=>x.retire).length") == 0)
        print('3. « Mettre en ligne » le gros')
        pg.locator('input[data-pc="sitegros"]').fill('62.5'); pg.locator('#ddb h3').first.click(); pg.wait_for_timeout(300)
        envois.clear(); dialogs.clear()
        pg.locator('[data-remet="sitegros"]').click(); pg.wait_for_timeout(700)
        if pg.evaluate("()=>document.getElementById('pxov').classList.contains('on')"): dialogs.append(pg.inner_text('#pxb')); pg.click('#pxok')
        pg.wait_for_timeout(1500)
        g = [e for e in envois if e.get('quel') == 'gros']
        check('LE POINT — le cockpit reçoit le gros à 62,50 avec republier:true, sans promo', len(g) == 1 and g[0]['barre'] == 62.5 and g[0].get('promo') in ('', None) and g[0].get('republier') is True, envois)
        check('la fenêtre dit « repasse EN VENTE »', any('repasse EN VENTE' in d for d in dialogs), dialogs)
        S = pg.evaluate("JSON.parse(localStorage.getItem('site-stock-v1'))")
        check('la fiche est sortie des retirées et revenue sur le gros', SANS0 not in ((S.get('_retires') or {}).get('g') or {}) and ((S.get(BC) or S.get(SANS0) or {}).get('g') or {}).get('id') == 201, S)
        check('la ligne dit maintenant « ✓ En ligne »', 'En ligne' in ligne('sitegros').inner_text() and 'Pas en ligne' not in ligne('sitegros').inner_text(), ligne('sitegros').inner_text())
        J = pg.evaluate("lit('crm-journal-v1',[])")
        check('le journal garde la remise en vente', any('remise en vente' in (j.get('lib') or '') for j in J), [j.get('lib') for j in J][-3:])
        print('4. le détail retiré, avec un ancien prix barré sur le site')
        SITE2 = {'_retires': {'d': {SANS0: {'id': 401, 'q': 8, 'suivi': True, 'nom': 'x', 'pr': 79, 'ps': 65, 't': '2026-10-20T23:26:00Z'}}}}
        envois.clear(); dialogs.clear(); ouvre(SITE2)
        retail(58)
        pg.locator('[data-remet="site"]').click(); pg.wait_for_timeout(700)
        if pg.evaluate("()=>document.getElementById('pxov').classList.contains('on')"): dialogs.append(pg.inner_text('#pxb')); pg.click('#pxok')
        pg.wait_for_timeout(1500)
        d = [e for e in envois if e.get('quel') == '']
        check('LE POINT — le détail repart au prix retail (58), SANS prix barré (promo vide), republier:true', len(d) == 1 and d[0]['barre'] == 58 and d[0].get('promo') in ('', None) and d[0].get('republier') is True, envois)
        print('5. Annuler, et refus du cockpit')
        envois.clear(); dialogs.clear(); ouvre(SITE2)
        pg.locator('[data-remet="site"]').click(); pg.wait_for_timeout(600)
        if pg.evaluate("()=>document.getElementById('pxov').classList.contains('on')"): pg.click('#pxc')
        pg.wait_for_timeout(400)
        check('Annuler : rien n\'est parti', not envois, envois)
        pg.locator('#dok').click(); pg.wait_for_timeout(800)
        check('et un Enregistrer ensuite ne republie pas la fiche', not [e for e in envois if e.get('republier')], envois)
        pg.evaluate("()=>{ const o=document.getElementById('pxov'); if(o) o.classList.remove('on'); }")
        envois.clear(); dialogs.clear(); rep.update(s=502, j={'erreur': 'Le site a répondu, mais la fiche est « draft ».'})
        ouvre({'_retires': SITE0['_retires']})   # seulement le gros retiré : c'est lui que le cockpit refuse
        pg.locator('[data-remet="sitegros"]').click(); pg.wait_for_timeout(700)
        if pg.evaluate("()=>document.getElementById('pxov').classList.contains('on')"): pg.click('#pxok')
        pg.wait_for_timeout(1500)
        S = pg.evaluate("JSON.parse(localStorage.getItem('site-stock-v1'))")
        check('refus du cockpit : l\'erreur est dite, la fiche reste retirée', any('reste retirée' in x for x in dialogs) and SANS0 in S['_retires']['g'], dialogs)
        check('aucune erreur JS', not err, err[:3])
        b.close()
finally:
    srv.terminate()
print(f'\n{ok} ok, {len(ko)} KO', ko); raise SystemExit(1 if ko else 0)
