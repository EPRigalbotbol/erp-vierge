# LE PRIX CHANGÉ SUR LE SITE DEVIENT LE PRIX DU CATALOGUE (Sam, 4 nov. 2026 : « il l'a mis à 81, il est à 81 sur le site, mais sur le
# Catalogue il reste à 88 »). Ce test protège :
#   1. LE POINT : le prix retail tapé dans la fiche (5 nov. 2026 : la case de gauche, le site n'a plus qu'un prix barré) devient le prix
#      RETAIL de l'outil (la colonne du Catalogue, les marges) ET le prix payé sur le site ; le gros tape son prix dans la case du site ;
#      un journal garde l'ancien et le nouveau ;
#   2. avec un prix barré, le site reçoit barré + promo = le retail ; le prix de l'outil reste le retail ;
#   3. les prix DÉJÀ changés avant le correctif (prix manuel du canal) sont alignés une seule fois, par le Patron seulement.
# (ancien en-tête du modèle : Changer les prix d'un parfum SUR LES SITES depuis la fiche du Catalogue, 24 sept. 2026.)
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


        print('1. le prix retail tapé dans la fiche devient le prix du Catalogue ET le prix payé sur le site')
        ouvre()
        retail(81)
        br = pg.evaluate("()=>JSON.parse(JSON.stringify(FICHE.brouillon))")
        check('LE POINT — 9 nov. : taper dans la case du site change le prix RETAIL de la fiche, pas un prix « manuel » à part', br.get('pvr') == 81 and not (br.get('pc') or {}).get('site'), br)
        envoie('site')
        check('le site reçoit 81 comme prix payé (pas de promo)', envois and abs(envois[-1]['barre'] - 81) < 0.001 and envois[-1]['promo'] == '', envois)
        m = pg.evaluate("bc=>{ const p=cur.find(x=>String(x.bc)===bc); return {pvr:p.pvr, pvw:p.pvw, pc:(MOD[p.id]||{}).pc||null, mod:MOD[p.id]}; }", BC)
        check('LE POINT — le prix retail du Catalogue passe à 81 (la colonne, pas seulement le canal)', abs(m['pvr'] - 81) < 0.001, m)
        check('le prix de gros ne bouge pas', abs(m['pvw'] - PVW) < 0.001, m)
        check('plus de « prix manuel » du canal site : une seule source', not (m['pc'] and 'site' in m['pc']), m)
        liste = pg.evaluate("bc=>{ const l=document.querySelectorAll('#cards, #tb, .tbl'); return document.body.innerText; }", BC)
        check('la liste du Catalogue affiche 81 (et plus l\'ancien prix)', '81,00' in liste, liste[:300])
        J = pg.evaluate("lit('crm-journal-v1',[]).filter(j=>j.act==='prix'&&j.champ==='pvr').map(j=>[j.av,j.ap])")
        check('le Journal garde l\'ancien et le nouveau prix retail', J and abs(J[-1][0] - PVR) < 0.001 and abs(J[-1][1] - 81) < 0.001, J)
        print('2. le gros')
        ouvre(); met('sitegros', barre=55); envoie('sitegros')
        m = pg.evaluate("bc=>{ const p=cur.find(x=>String(x.bc)===bc); return {pvr:p.pvr, pvw:p.pvw, pc:(MOD[p.id]||{}).pc||null}; }", BC)
        check('le prix de gros du Catalogue passe à 55, le retail reste à 81', abs(m['pvw'] - 55) < 0.001 and abs(m['pvr'] - 81) < 0.001 and not (m['pc'] and 'sitegros' in m['pc']), m)
        print('3. avec un prix barré, le site reçoit barré + promo = le retail ; le prix de l\'outil reste le retail')
        ouvre(); envois.clear(); met('site', barre=99); retail(72); envoie('site')
        m = pg.evaluate("bc=>{ const p=cur.find(x=>String(x.bc)===bc); return {pvr:p.pvr}; }", BC)
        check('barré 99, retail 72 : le site reçoit 99 / 72 et le prix retail de l\'outil = 72 (ce que le client paie)', abs(m['pvr'] - 72) < 0.001 and envois and envois[-1]['barre'] == 99 and envois[-1]['promo'] == 72, (m, envois))
        print('3b. le site refuse : rien n\'est enregistré, le Catalogue et le site disent toujours la même chose')
        ouvre(); envois.clear(); reponse['s'] = 500; reponse['j'] = {'erreur': 'panne'}
        retail(20); sauve(1500)
        reponse['s'] = 200; reponse['j'] = None
        m = pg.evaluate("bc=>{ const p=cur.find(x=>String(x.bc)===bc); return {pvr:p.pvr, pc:(MOD[p.id]||{}).pc||null}; }", BC)
        check('LE POINT — le site a refusé le prix 20 : le Catalogue reste à 72 comme le site, et aucun prix « manuel » ne traîne', abs(m['pvr'] - 72) < 0.001 and not (m['pc'] and 'site' in m['pc']), m)
        print('4. les anciens prix manuels du canal sont alignés une seule fois')
        pg.evaluate("bc=>{ const p=cur.find(x=>String(x.bc)===bc); const R=JSON.parse(localStorage.getItem('reglages-v1')||'{}'); delete R.prixAligne; localStorage.setItem('reglages-v1',JSON.stringify(R));"
                    " const M=JSON.parse(localStorage.getItem('fiches-modifiees-v1')||'{}'); M[p.id]={pc:{site:63,sitegros:40}}; localStorage.setItem('fiches-modifiees-v1',JSON.stringify(M)); }", BC)
        pg.goto(base + 'catalogue.html'); pg.wait_for_timeout(2500)
        m = pg.evaluate("bc=>{ const p=cur.find(x=>String(x.bc)===bc); return {pvr:p.pvr,pvw:p.pvw,mod:MOD[p.id]||null}; }", BC)
        check('LE POINT — un ancien prix manuel (63 / 40) devient le prix retail / gros du Catalogue', abs(m['pvr'] - 63) < 0.001 and abs(m['pvw'] - 40) < 0.001 and not (m['mod'] or {}).get('pc'), m)
        pg.reload(); pg.wait_for_timeout(2000)
        pg.evaluate("bc=>{ const p=cur.find(x=>String(x.bc)===bc); const M=JSON.parse(localStorage.getItem('fiches-modifiees-v1')||'{}'); M[p.id]=Object.assign({},M[p.id],{pc:{site:70}}); localStorage.setItem('fiches-modifiees-v1',JSON.stringify(M)); }", BC)
        pg.goto(base + 'catalogue.html'); pg.wait_for_timeout(2500)
        m = pg.evaluate("bc=>{ const p=cur.find(x=>String(x.bc)===bc); return {pvr:p.pvr,pc:(MOD[p.id]||{}).pc||null}; }", BC)
        check('LE POINT — 9 nov. : un prix manuel posé APRÈS (page ancienne restée ouverte) devient le prix du Catalogue à l\'ouverture suivante', abs(m['pvr'] - 70) < 0.001 and not m['pc'], m)
        pg.evaluate("bc=>{ const p=cur.find(x=>String(x.bc)===bc); const M=JSON.parse(localStorage.getItem('fiches-modifiees-v1')||'{}'); M[p.id]=Object.assign({},M[p.id],{pc:{site:70}}); localStorage.setItem('fiches-modifiees-v1',JSON.stringify(M)); }", BC)
        pose('commercial')
        pg.evaluate("bc=>{ const p=cur.find(x=>String(x.bc)===bc); const R=JSON.parse(localStorage.getItem('reglages-v1')||'{}'); delete R.prixAligne; localStorage.setItem('reglages-v1',JSON.stringify(R)); }", BC)
        pg.goto(base + 'catalogue.html'); pg.wait_for_timeout(2500)
        m = pg.evaluate("bc=>{ const p=cur.find(x=>String(x.bc)===bc); return {pvr:p.pvr,pc:(MOD[p.id]||{}).pc||null}; }", BC)
        check('un rôle sans droit de prix ne touche à rien', m['pc'] and m['pc'].get('site') == 70, m)
        check('aucune erreur JS', not err, err[:3])
        b.close()
finally:
    srv.terminate()
print(f'\n{ok} ok, {len(ko)} KO', ko); raise SystemExit(1 if ko else 0)
