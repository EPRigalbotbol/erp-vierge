# Changer les prix d'un parfum SUR LES SITES depuis la fiche du Catalogue (24 sept. 2026 ; refait le 5 nov., puis le 11 nov. 2026).
# 11 nov. 2026 (Sam, via Igal) : « plus de prix barré » — une ligne par canal : LE prix, « ✓ En ligne », le bouton. Le client paie le
# prix de la ligne ; un prix barré qui traîne sur le site est enlevé à l'Enregistrer.
# Igal : « au lieu de 64 je mets 63, et ça le modifie directement sur le site ; seul Sam,
# en tant que dirigeant, peut le faire » — puis : « le prix barré et la promo, qu'on
# puisse gérer les deux sans aller dans WooCommerce ». Le cockpit est simulé : on
# vérifie ce que l'ERP lui envoie, et ce que l'ERP fait de la réponse.
import pathlib, subprocess, time, socket, json
from playwright.sync_api import sync_playwright

D = pathlib.Path('/home/claude/catalogue')
ok = 0; ko = []
def check(n, c, i=''):
    global ok
    if c: ok += 1; print('  ok  ', n)
    else: ko.append(n); print('  KO  ', n, i)
CAT = json.load(open(D / 'cat.json'))
# un parfum en stock, prix d'achat/retail/gros connus, code-barres qui commence par 0
P = next(r for r in CAT if (r[6] or 0) > 2 and r[12] and r[7] and r[8] and r[7] > r[12] + 10 and r[0] and len(str(r[0])) == 12 and str(r[0]).startswith('0'))
BC, PA, PVR, PVW = str(P[0]), float(P[12]), float(P[7]), float(P[8])
def port_libre():
    s = socket.socket(); s.bind(('127.0.0.1', 0)); p = s.getsockname()[1]; s.close(); return p
port = port_libre()
srv = subprocess.Popen(['python3', '-m', 'http.server', str(port), '--bind', '127.0.0.1'], cwd=str(D), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1)
SITE0 = {BC: {'d': {'id': 101, 'q': 5, 'suivi': True, 'etat': 'instock', 'nom': 'x', 'pr': PVR, 'ps': None},
              'g': {'id': 201, 'q': 2, 'suivi': True, 'etat': 'instock', 'nom': 'x', 'pr': PVW, 'ps': None}}}
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
        envois = []; reponse = {'s': 200, 'j': None}
        def cockpit(route):
            body = json.loads(route.request.post_data or '{}'); envois.append(body)
            j = reponse['j'] or {'ok': True, 'avant': body.get('attendu'), 'apres': {'barre': body.get('barre'), 'promo': None if body.get('promo') in ('', None) else body.get('promo')}}
            route.fulfill(status=reponse['s'], content_type='application/json', body=json.dumps(j))
        pg.route('**/api/o/dasy/site/prix', cockpit)
        base = f'http://127.0.0.1:{port}/'
        pg.add_init_script("document.addEventListener('DOMContentLoaded',()=>{const s=document.createElement('style');s.textContent='#svtem{display:none!important}';document.head.appendChild(s)})")
        pg.goto(base + 'accueil.html'); pg.wait_for_timeout(400)
        def pose(role):
            pg.evaluate("r=>localStorage.setItem('sam-session-v1', JSON.stringify({id:r==='patron'?'sam':'juan',nom:r==='patron'?'Sam':'Juan',role:r,depuis:new Date().toISOString()}))", role)
        pose('patron')
        pg.evaluate("localStorage.setItem('ck-token','jeton-test')")
        def site(S): pg.evaluate("s=>localStorage.setItem('site-stock-v1', JSON.stringify(s))", S)
        def lsite(): return pg.evaluate("JSON.parse(localStorage.getItem('site-stock-v1'))")
        site(SITE0)
        def ouvre():
            pg.goto(base + 'catalogue.html'); pg.wait_for_timeout(2500)
            pg.evaluate("bc=>ouvreFiche(cur.find(p=>String(p.bc)===bc).id)", BC); pg.wait_for_timeout(500)
        def boite(cid):
            # 11 oct. 2026 : les cases du site sont repliées sous « régler » ; on les déplie pour le test
            pg.evaluate("cid=>{ const d=document.querySelector('[data-sbx=\"'+cid+'\"]'); const x=d&&d.closest('details'); if(x) x.open=true; }", cid)
            return pg.locator(f'[data-sbx="{cid}"]')
        def met(cid, barre=None):
            if barre is not None: boite(cid).locator('[data-sb]').fill(str(barre))
            pg.wait_for_timeout(150)
        def retail(v):
            pg.locator('input[data-pc="site"]').fill(str(v)); pg.locator('#ddb h3').first.click(); pg.wait_for_timeout(400)
        def envoie(cid):
            # 12 oct. 2026 (Igal : « on a déjà Enregistrer en bas ») : plus de bouton dans la boîte — c'est l'Enregistrer du bas qui envoie
            sauve(1200)

        print('1. la ligne du détail : UN prix, « ✓ En ligne », pas de prix barré')
        ouvre()
        ln = pg.locator('[data-cn="site"]')
        check('LE POINT — aucune case « prix barré » visible, aucun texte d\'explication', 'barré' not in ln.inner_text().lower() and 'le client paie' not in ln.inner_text().lower() and ln.locator('input:visible').count() == 1, ln.inner_text())
        check('le prix retail de la fiche est dans SA case', abs(float(pg.locator('input[data-pc="site"]').input_value()) - PVR) < 0.001)
        check('« ✓ En ligne » et « Retirer de la vente »', 'En ligne' in ln.inner_text() and ln.locator('[data-retv="site"]').count() == 1, ln.inner_text())
        check('rien de changé : rien en attente', pg.evaluate("boitesEnAttente().length") == 0)
        print('2. le gros : une case, le prix de gros de la fiche')
        S = lsite(); S[BC]['g']['pr'] = round(PVW + 3, 2); site(S); ouvre()
        gx = pg.locator('[data-cn="sitegros"]')
        check('gros : UNE case, avec le prix de gros de la fiche (pas celui du site)', gx.locator('input[data-sb]').count() == 1 and abs(float(gx.locator('input[data-sb]').input_value()) - PVW) < 0.001, gx.inner_text())
        check('le site de gros dit un autre prix : en attente', pg.evaluate("boitesEnAttente().map(x=>x.cid)") == ['sitegros'])
        envois.clear(); dialogs.clear(); sauve()
        check('envoyé avec quel=gros, le prix du gros, sans promo', len(envois) == 1 and envois[0]['quel'] == 'gros' and abs(envois[0]['barre'] - PVW) < 0.001 and envois[0].get('promo') in ('', None), envois)
        print('3. changer le prix retail')
        nouveau = round(PVR + 7, 2)
        ouvre(); envois.clear(); dialogs.clear(); retail(nouveau)
        check('la ligne est en attente', pg.evaluate("boitesEnAttente().length") == 1)
        sauve()
        check('LE POINT — UN envoi : le nouveau prix, sans promo (pas de prix barré)', len(envois) == 1 and abs(envois[0]['barre'] - nouveau) < 0.001 and envois[0]['promo'] == '', envois)
        check('la confirmation dit ce que le client paiera', any('Le client paiera' in d for d in dialogs), dialogs)
        S = lsite()
        check('l\'outil range le nouveau prix du site, sans promo', abs(S[BC]['d']['pr'] - nouveau) < 0.001 and S[BC]['d']['ps'] is None, S[BC]['d'])
        J = pg.evaluate("lit('crm-journal-v1',[]).map(j=>j.lib)")
        check('le journal : « prix changés sur le site perfumestrade.com »', any('prix changés sur le site perfumestrade.com' in l for l in J), J[-2:])
        print('4. LE CAS DE SAM : un ancien prix barré sur le site (barré 90, le client paie le retail)')
        S = lsite(); S[BC]['d']['pr'] = 90; S[BC]['d']['ps'] = nouveau; site(S)
        ouvre(); envois.clear(); dialogs.clear()
        check('LE POINT — à l\'ouverture, la fiche sait qu\'il faut enlever le prix barré : en attente', pg.evaluate("boitesEnAttente().map(x=>x.cid)") == ['site'])
        sauve()
        check('LE POINT — envoyé : le prix payé, promo vide — le prix barré disparaît du site', len(envois) == 1 and abs(envois[0]['barre'] - nouveau) < 0.001 and envois[0]['promo'] == '', envois)
        check('l\'outil range : plus de prix barré', lsite()[BC]['d']['ps'] is None and abs(lsite()[BC]['d']['pr'] - nouveau) < 0.001, lsite()[BC]['d'])
        print('5. sous le prix d\'achat : prévenu, pas bloqué')
        ouvre(); envois.clear(); dialogs.clear(); retail(round(PA - 1, 2)); sauve()
        check('« Tu vends à perte », et ça part quand même', any('moins que le prix d\'achat' in d and 'à perte' in d for d in dialogs) and len(envois) == 1, dialogs)
        S = lsite(); S[BC]['d']['pr'] = nouveau; S[BC]['d']['ps'] = None; site(S)
        print('6. le site a changé entre-temps : refus, l\'outil range les vrais prix')
        ouvre(); envois.clear(); dialogs.clear()
        reponse['s'] = 409; reponse['j'] = {'erreur': 'Les prix ont changé sur le site entre-temps : prix barré 90.00 $, promo 61.50 $.', 'avant': {'barre': 90, 'promo': 61.5}}
        retail(round(nouveau + 1, 2)); sauve()
        check('le refus est dit', any('changé sur le site entre-temps' in d for d in dialogs), dialogs)
        check('l\'outil range les vrais prix du site (90 / 61,50)', lsite()[BC]['d']['pr'] == 90 and lsite()[BC]['d']['ps'] == 61.5, lsite()[BC]['d'])
        reponse['s'] = 200; reponse['j'] = None
        print('7. le 0 perdu au début du code-barres')
        S = lsite(); S[BC]['d']['pr'] = nouveau; S[BC]['d']['ps'] = None; site({BC.lstrip('0'): S[BC]})
        ouvre(); envois.clear(); dialogs.clear(); retail(round(nouveau + 2, 2)); sauve()
        check('le code envoyé est celui du SITE (sans le 0)', envois and envois[0]['bc'] == BC.lstrip('0'), envois)
        site(S)
        print('8. seul le dirigeant, et seulement en ligne')
        pose('commercial'); ouvre()
        t = pg.locator('[data-cn="site"]')
        check('commercial : « ✓ En ligne » sans bouton, rien à envoyer', 'En ligne' in t.inner_text() and t.locator('button').count() == 0 and pg.locator('[data-sbx]').count() == 0, t.inner_text())
        pose('patron'); pg.evaluate("localStorage.removeItem('ck-token')"); ouvre()
        check('hors ligne : aucun bouton de mise en ligne / retrait', pg.locator('[data-cn="site"] button').count() == 0)
        check('aucune erreur JS', not err, err[:3])
        b.close()
finally:
    srv.terminate()
print(f'\n{ok} ok, {len(ko)} KO', ko); raise SystemExit(1 if ko else 0)
