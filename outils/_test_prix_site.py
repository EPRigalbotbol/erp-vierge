# Changer les prix d'un parfum SUR LES SITES depuis la fiche du Catalogue (24 sept. 2026 ; refait le 5 nov. 2026).
# 5 nov. 2026 (Igal) : « je ne veux plus que cette case rouge existe… la seule chose que je veux qui existe, c'est prix barré » :
# sur perfumestrade.com le client paie LE PRIX RETAIL de la fiche ; la boîte du site n'a qu'une case, le prix barré (promo).
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

        print('1. la ligne du détail : le prix retail à gauche, UNE case « prix barré » à droite, rien d\'autre')
        ouvre()
        bx = boite('site'); ln = pg.locator('[data-cn="site"]')
        check('LE POINT — une seule case dans la boîte, le prix barré, vide (pas de promo sur le site)',
              bx.count() == 1 and bx.locator('[data-sb]').count() == 1 and bx.locator('[data-sb]').input_value() == '' and bx.locator('[data-sp]').count() == 0, bx.inner_text() if bx.count() else '—')
        check('LE POINT — plus de case rouge, plus de « payé par le client », plus de lien « mettre le prix de l\'outil », plus de « + ajouter un prix promo »',
              ln.locator('.sbw').count() == 0 and 'payé par le client' not in ln.inner_text() and ln.locator('[data-prend]').count() == 0 and pg.locator('[data-promo-ouvre]').count() == 0, ln.inner_text())
        check('le prix retail de la fiche est à gauche, dans sa case', abs(float(pg.locator('input[data-pc="site"]').input_value()) - PVR) < 0.001)
        check('rien de changé : rien en attente', pg.evaluate("boitesEnAttente().length") == 0)
        S = lsite(); S[BC]['g']['pr'] = PVW + 2; site(S); ouvre()
        gx = boite('sitegros')
        # 10 nov. 2026 (Igal, capture à l'appui : « la ligne du Catalogue dit 53,76 $, la fiche dit 85 $ ») : la case affiche le prix de gros
        # de la FICHE, plus celui du site ; un site qui dit autre chose est « en attente » : l'Enregistrer l'y remet
        check('LE POINT — gros : toujours UNE seule case, et elle affiche le prix de gros de la fiche (celui du Catalogue), pas celui du site', gx.locator('[data-sb]').count() == 1 and abs(float(gx.locator('[data-sb]').input_value()) - PVW) < 0.001
              and pg.locator('[data-cn="sitegros"] [data-pc]').count() == 0 and pg.locator('[data-cn="sitegros"] .sbw').count() == 0, pg.locator('[data-cn="sitegros"]').inner_text())
        check('le site de gros dit un autre prix : il est « en attente », l\'Enregistrer y remettra le prix de la fiche', pg.evaluate("boitesEnAttente().map(x=>x.cid)") == ['sitegros'])
        site(SITE0); ouvre(); bx = boite('site')

        print('2. Sam tape un prix barré : le site reçoit barré + promo = le prix retail')
        barre = round(PVR + 60, 2)
        met('site', barre=barre)
        check('la boîte est « en attente » : l\'Enregistrer du bas va l\'envoyer', pg.evaluate("boitesEnAttente().length") == 1)
        envoie('site')
        check('une confirmation dit que le client paiera le prix retail', any('Le client paiera' in d and 'prix retail' in d for d in dialogs), dialogs)
        check('LE POINT — UN envoi : barré = ce que Sam a tapé, promo = le prix retail de la fiche',
              len(envois) == 1 and envois[0]['quel'] == '' and abs(envois[0]['barre'] - barre) < 0.001 and abs(envois[0]['promo'] - PVR) < 0.001 and envois[0]['attendu'] == {'barre': PVR, 'promo': None}, envois)
        S = lsite()
        check('l\'outil range les nouveaux prix du site', abs(S[BC]['d']['pr'] - barre) < 0.001 and abs(S[BC]['d']['ps'] - PVR) < 0.001, S[BC]['d'])
        M = pg.evaluate("JSON.parse(localStorage.getItem('fiches-modifiees-v1')||'{}')")
        cle = pg.evaluate("bc=>cur.find(p=>String(p.bc)===bc).id", BC)
        check('le prix retail de l\'outil n\'a pas bougé, pas de prix manuel du canal', abs(M.get(cle, {}).get('pvr', PVR) - PVR) < 0.001 and 'site' not in (M.get(cle, {}).get('pc') or {}), M.get(cle))
        J = pg.evaluate("JSON.parse(localStorage.getItem('crm-journal-v1')||'[]').map(j=>j.lib)")
        check('le journal : « prix changés sur le site perfumestrade.com »', any('prix changés sur le site perfumestrade.com' in l for l in J), J[-2:])
        ouvre()
        check('la fiche rouverte montre le prix barré dans sa case', abs(float(boite('site').locator('[data-sb]').input_value()) - barre) < 0.001)

        print('3. Sam change le prix RETAIL de la fiche : le site suit (promo = nouveau retail, même prix barré)')
        envois.clear(); dialogs.clear()
        nouveau = round(PVR - 4, 2)
        retail(nouveau)
        check('le prix payé sur le site n\'est plus le retail : en attente', pg.evaluate("boitesEnAttente().length") == 1)
        sauve(1500)
        check('LE POINT — le site reçoit barré inchangé, promo = le nouveau retail', len(envois) == 1 and abs(envois[0]['barre'] - barre) < 0.001 and abs(envois[0]['promo'] - nouveau) < 0.001, envois)
        M = pg.evaluate("JSON.parse(localStorage.getItem('fiches-modifiees-v1')||'{}')")
        check('et le retail de l\'outil est le nouveau', abs(M.get(cle, {}).get('pvr', 0) - nouveau) < 0.001, M.get(cle))
        check('le site aussi', abs(lsite()[BC]['d']['ps'] - nouveau) < 0.001)

        print('4. les garde-fous : un prix barré pas plus haut que le retail = pas de promo ; sous le prix d\'achat = prévenu, pas bloqué')
        ouvre(); envois.clear(); dialogs.clear()
        met('site', barre=round(nouveau - 10, 2)); envoie('site')
        check('barré plus bas que le retail : envoyé SANS promo, le client paie le retail, et la fenêtre le dit',
              len(envois) == 1 and envois[0]['promo'] == '' and abs(envois[0]['barre'] - nouveau) < 0.001 and any('ne compte pas' in d for d in dialogs), (envois, dialogs))
        ouvre(); envois.clear(); dialogs.clear()
        retail(round(PA / 10, 2)); sauve(1500)
        # 9 oct. 2026 (Igal : « ne refuse jamais, pour Sam et moi ») : sous le prix d'achat, le Patron est prévenu mais pas bloqué
        check('le client paierait moins que le prix d\'achat : prévenu (« Tu vends à perte »), pas bloqué', any('moins que le prix d\'achat' in d and 'à perte' in d for d in dialogs) and len(envois) == 1, dialogs)
        pg.evaluate("()=>{ const M=JSON.parse(localStorage.getItem('fiches-modifiees-v1')||'{}'); for(const k in M){ if(M[k]&&M[k].pvr!=null) M[k].pvr=%s; } localStorage.setItem('fiches-modifiees-v1',JSON.stringify(M)); }" % nouveau)
        S = lsite(); S[BC]['d']['pr'] = nouveau; S[BC]['d']['ps'] = None; site(S)

        print('5. le site a changé entre-temps : le cockpit refuse, l\'outil montre les vrais prix')
        ouvre(); envois.clear(); dialogs.clear()
        reponse['s'] = 409; reponse['j'] = {'erreur': 'Les prix ont changé sur le site entre-temps : prix barré 90.00 $, promo 61.50 $.', 'avant': {'barre': 90, 'promo': 61.5}}
        met('site', barre=round(nouveau + 30, 2)); envoie('site')
        check('le refus est dit', any('changé sur le site entre-temps' in d for d in dialogs), dialogs)
        S = lsite()
        check('l\'outil range les vrais prix du site (90 / 61,50)', S[BC]['d']['pr'] == 90 and S[BC]['d']['ps'] == 61.5, S[BC]['d'])
        reponse['s'] = 200; reponse['j'] = None

        print('6. arrêter la promo : la case prix barré vidée')
        ouvre(); envois.clear(); dialogs.clear()
        met('site', barre=''); envoie('site')
        check('envoyé avec promo vide ("") et barré = le prix retail — le cockpit arrête la promo', len(envois) == 1 and envois[0]['promo'] == '' and abs(envois[0]['barre'] - nouveau) < 0.001, envois)
        check('l\'outil range : plus de promo', lsite()[BC]['d']['ps'] is None)

        print('7. le site de gros')
        envois.clear(); dialogs.clear()
        met('sitegros', barre=round(PVW - 1, 2)); envoie('sitegros')
        check('envoyé avec quel=gros, le prix du gros', len(envois) == 1 and envois[0]['quel'] == 'gros' and abs(envois[0]['barre'] - (PVW - 1)) < 0.001, envois)
        check('LE GROS n\'a PAS de prix barré : un seul champ « prix de vente », pas de promo (Igal, 12 oct.)',
              boite('sitegros').locator('[data-sp]').count() == 0 and 'promo' not in boite('sitegros').inner_text().lower() and 'prix de vente' in boite('sitegros').inner_text().lower(), boite('sitegros').inner_text())
        check('et son envoi n\'emporte aucune promo', envois and envois[0]['quel'] == 'gros' and envois[0].get('promo') in ('', None), envois)

        print('8. le 0 perdu au début du code-barres')
        S = lsite(); site({BC.lstrip('0'): S[BC]})
        ouvre(); envois.clear(); dialogs.clear()
        check('la carte retrouve la fiche du site', boite('site').count() == 1)
        met('site', barre=round(nouveau + 9, 2)); envoie('site')
        check('le code envoyé est celui du SITE (sans le 0)', envois and envois[0]['bc'] == BC.lstrip('0'), envois)
        site(S)

        print('8b. LE CAS DE SAM (12 oct., relu le 5 nov.) : 58 $ de retail avec un prix barré 65 → le site vend 58, barré 65')
        S = lsite(); S[BC]['d']['pr'] = 35; S[BC]['d']['ps'] = 29; site(S)
        ouvre(); envois.clear(); dialogs.clear()
        met('site', barre=65); retail(58)
        sauve(1500)
        check('LE POINT — barré 65 et promo 58 partent', len(envois) == 1 and envois[0]['barre'] == 65 and envois[0]['promo'] == 58, envois)
        check('et le site range 65 / 58 (la ligne barrée est là)', lsite()[BC]['d']['pr'] == 65 and lsite()[BC]['d']['ps'] == 58, lsite()[BC]['d'])

        print('9. seul le dirigeant, et seulement en ligne')
        pose('commercial'); ouvre()
        t = pg.locator('[data-cn="site"]').inner_text().lower()
        check('commercial : pas de cases, seulement « prix barré 65 » en lecture seule, pas de « payé par le client »', boite('site').count() == 0 and 'prix barré' in t and 'payé par le client' not in t, t)
        pose('patron'); pg.evaluate("localStorage.removeItem('ck-token')"); ouvre()
        check('hors ligne : pas de cases', boite('site').count() == 0)
        check('aucune erreur JS', not err, err[:3])
        b.close()
finally:
    srv.terminate()
print(f"\n{ok} ok, {len(ko)} KO", ko)
