# LE PRIX DE PERFUME CITY, DEPUIS LA FICHE DU CATALOGUE (15 oct. 2026).
# Igal : « je veux pouvoir modifier sur la fiche produit le site Perfume City qui est sur Shopify ».
# Le cockpit est simulé : on vérifie ce que l'ERP lui envoie, et ce que l'ERP fait de sa réponse.
#
# Ce qui est vraiment en jeu :
#   1. la ligne Perfume City dit « ventes reliées » et montre le prix que le client paie CHEZ SHOPIFY ;
#   2. ce prix devient le prix de l'outil pour ce canal (comme l'annonce Amazon) — pas un prix calculé à côté ;
#   3. un prix tapé part sur Shopify à l'Enregistrer, après confirmation, avec le prix ATTENDU — jamais en silence ;
#   4. si Shopify refuse (prix changé entre-temps, droit manquant), rien n'est enregistré de faux, et le vrai prix s'affiche ;
#   5. seul le Patron/admin envoie sur Shopify ; un autre compte n'enregistre que dans l'outil ;
#   6. un code-barres porté par deux produits Shopify, ou absent de Shopify, n'est JAMAIS envoyé.
import pathlib, subprocess, time, socket, json
from playwright.sync_api import sync_playwright

D = pathlib.Path('/home/claude/catalogue')
ok = 0; ko = []
def check(n, c, i=''):
    global ok
    if c: ok += 1; print('  ok  ', n)
    else: ko.append(n); print('  KO  ', n, i)
CAT = json.load(open(D / 'cat.json'))
P = next(r for r in CAT if (r[6] or 0) > 2 and r[12] and r[7] and r[8] and r[7] > r[12] + 10 and r[0] and len(str(r[0])) == 12 and str(r[0]).startswith('0'))
BC = str(P[0]); K = BC.lstrip('0'); PA = float(P[12])
P2 = next(r for r in CAT if r is not P and (r[6] or 0) > 2 and r[12] and r[7] and r[0] and len(str(r[0])) >= 12 and not str(r[0]).startswith('0'))
BC2 = str(P2[0])
def port_libre():
    s = socket.socket(); s.bind(('127.0.0.1', 0)); p = s.getsockname()[1]; s.close(); return p
port = port_libre()
srv = subprocess.Popen(['python3', '-m', 'http.server', str(port), '--bind', '127.0.0.1'], cwd=str(D), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1)
try:
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1456, 'height': 900}); err = []
        pg.on('pageerror', lambda e: err.append(str(e)))
        dialogs = []; accepte = {'v': True}
        def dlg(d):
            dialogs.append((d.type, d.message))
            d.accept() if (accepte['v'] or d.type == 'alert') else d.dismiss()
        pg.on('dialog', dlg)
        def sauve(ms=1200):
            # la fenêtre unique de l'Enregistrer (20 oct.) : son texte tient la place de l'ancienne confirmation, on la valide
            pg.locator('#dok').click(); pg.wait_for_timeout(500)
            if pg.evaluate("()=>document.getElementById('pxov').classList.contains('on')"):
                dialogs.append(('confirm',pg.inner_text('#pxb'))); pg.click('#pxok' if accepte['v'] else '#pxc')
            pg.wait_for_timeout(ms)
        envois = []; reponse = {'s': 200, 'j': None}
        def cockpit(route):
            body = json.loads(route.request.post_data or '{}'); envois.append(body)
            j = reponse['j'] or {'ok': True, 'avant': body.get('attendu'), 'apres': body.get('prix'), 'nom': 'x'}
            route.fulfill(status=reponse['s'], content_type='application/json', body=json.dumps(j))
        pg.route('**/api/o/dasy/shopify/prix', cockpit)
        base = f'http://127.0.0.1:{port}/'
        pg.goto(base + 'accueil.html'); pg.wait_for_timeout(400)
        def pose(role):
            pg.evaluate("r=>localStorage.setItem('sam-session-v1', JSON.stringify({id:r==='patron'?'sam':'juan',nom:r==='patron'?'Sam':'Juan',role:r,depuis:new Date().toISOString()}))", role)
        pose('patron')
        pg.evaluate("localStorage.setItem('ck-token','jeton-test')")
        def shop(S): pg.evaluate("s=>localStorage.setItem('shopify-pc-prix-v1', JSON.stringify(s))", S)
        SHOP0 = {K: ['1', '11', 64.0, None, 1], '_t': '2026-10-15T14:00:00', '_amb': [BC2.lstrip('0')]}
        def ouvre(bc=BC):
            pg.goto(base + 'catalogue.html'); pg.wait_for_timeout(2500)
            pg.evaluate("""bc=>{ $('fs').value=''; $('q').value=bc; render(); ouvreFiche(cur.find(p=>String(p.bc)===bc).id); }""", bc); pg.wait_for_timeout(500)
        def ligne(): return pg.locator('.dcanl .cn[data-cn="perfumecity"]')
        def champ(): return ligne().locator('input[data-pc="perfumecity"]')
        def enregistre(): sauve(900)
        def mod(): return pg.evaluate("bc=>{ const p=cur.find(x=>String(x.bc)===bc); return (MOD[p.id]||{}).pc||null; }", BC)
        def journal(): return pg.evaluate("()=>JSON.parse(localStorage.getItem('crm-journal-v1')||'[]')")

        print('1. la ligne Perfume City montre le prix de Shopify')
        shop(SHOP0); ouvre()
        t = ligne().inner_text()
        # 11 nov. 2026 (Sam) : la ligne ne montre plus que le prix, « ✓ En ligne » et le bouton
        check('la ligne dit « ✓ En ligne » (le produit est actif chez Perfume City)', 'en ligne' in t.lower() and 'pas en ligne' not in t.lower(), t[:200])
        check('LE POINT — le prix de l\'outil pour ce canal EST celui de Shopify (clé sans zéro de tête retrouvée)', champ().input_value() in ('64', '64.0'), champ().input_value())
        check('aucun avertissement tant que l\'outil et Shopify sont d\'accord', ligne().locator('.sbw').count() == 0)

        print('2. un prix tapé part sur Shopify, après confirmation, avec le prix attendu')
        champ().fill('61.5'); pg.wait_for_timeout(300)
        enregistre()
        confirms = [m for t_, m in dialogs if t_ == 'confirm' and 'Shopify' in m]
        check('une confirmation dit l\'ancien et le nouveau prix', confirms and '64' in confirms[0] and '61' in confirms[0] and 'Perfume City' in confirms[0], dialogs)
        check('UN envoi, avec le code-barres, le nouveau prix ET le prix attendu', len(envois) == 1 and envois[0].get('bc') == BC and envois[0].get('prix') == 61.5 and envois[0].get('attendu') == 64, envois)
        check('rien d\'autre ne part (ni stock, ni autre champ) — sauf « sansBarre » : plus de prix barré (11 nov. 2026)', envois and sorted(envois[0].keys()) == ['attendu', 'bc', 'prix', 'sansBarre'] and envois[0]['sansBarre'] is True, envois)
        pg.wait_for_timeout(300)   # (sans recharger : le cockpit simulé ne range rien ; c'est la réponse de Shopify qui s'affiche)
        check('la fiche montre ensuite le nouveau prix de Shopify (61,50 $)', champ().input_value() in ('61.5', '61.50'), champ().input_value())
        check('plus de prix « manuel » en attente dans la fiche', not (mod() or {}).get('perfumecity'), mod())
        J = [x for x in journal() if 'Perfume City' in (x.get('lib') or '')]
        check('le journal garde le changement : avant 64, après 61,50', J and '64' in str(J[-1].get('av')) and '61' in str(J[-1].get('ap')), J[-1:] )

        print('3. annuler : rien ne part')
        envois.clear(); dialogs.clear(); shop(SHOP0); ouvre()
        champ().fill('59'); pg.wait_for_timeout(300); accepte['v'] = False; enregistre(); accepte['v'] = True
        check('refus de la confirmation : aucun envoi', not envois, envois)

        print('4. Shopify refuse')
        envois.clear(); dialogs.clear(); shop(SHOP0); ouvre()
        reponse.update(s=409, j={'erreur': 'Le prix a changé sur Shopify entre-temps : il est maintenant de 60.00 $ (l\'outil montrait 64.00 $). Rien n\'a été écrit — regarde, puis recommence.', 'avant': 60.0})
        champ().fill('58'); pg.wait_for_timeout(300); enregistre()
        alertes = [m for t_, m in dialogs if t_ == 'alert']
        check('le message de Shopify est montré tel quel (« 60.00 $ »)', alertes and '60.00' in alertes[-1], dialogs)
        check('rien n\'est enregistré comme prix manuel à la place', not (mod() or {}).get('perfumecity'), mod())
        t = ligne().inner_text()
        pg.evaluate("()=>{ const b=cur[FICHE.pos]; ouvreFiche(b.id); }"); pg.wait_for_timeout(400)
        check('la fiche rouverte montre le VRAI prix de Shopify (60 $)', champ().input_value() in ('60', '60.0', '60.00'), champ().input_value())
        reponse.update(s=200, j=None)
        envois.clear(); dialogs.clear(); shop(SHOP0); ouvre()
        reponse.update(s=403, j={'erreur': "Shopify refuse d'écrire : l'application « ERP Perfume in the city » n'a que le droit de LIRE. Sam doit ajouter write_products."})
        champ().fill('57'); pg.wait_for_timeout(300); enregistre()
        alertes = [m for t_, m in dialogs if t_ == 'alert']
        check('droit manquant : le message dit quoi faire (write_products)', alertes and 'write_products' in alertes[-1], dialogs)
        reponse.update(s=200, j=None)

        print('5. seul le Patron envoie sur Shopify')
        envois.clear(); dialogs.clear(); pose('commercial'); shop(SHOP0); ouvre()
        champ().fill('55'); pg.wait_for_timeout(300); enregistre()
        check('un commercial : aucun envoi à Shopify', not envois, envois)
        # un rôle fabriqué avec le seul droit « prixPC » (Clemencia/Kim) : il envoie, mais ne voit ni achat ni marge, et ne vend jamais sous le coût
        pg.evaluate("localStorage.setItem('sam-roles-v1', JSON.stringify({'prix-pc':{lib:'Prix Perfume City',aide:'essai',vendre:1,prixPC:1}}))")
        envois.clear(); dialogs.clear(); pose('prix-pc'); shop(SHOP0); ouvre()
        t = ligne().inner_text()
        check('rôle avec le droit prixPC : la ligne propose d\'envoyer à Shopify', 'envoie le nouveau prix' in t.lower() or champ().count() == 1)
        champ().fill('61'); pg.wait_for_timeout(300); enregistre()
        check('LE POINT — ce rôle, sans voir les marges, envoie bien le prix à Shopify', len(envois) == 1 and envois[0].get('prix') == 61, envois)
        envois.clear(); dialogs.clear(); shop(SHOP0); ouvre()
        bas = round(PA - 1, 2)
        champ().fill(str(bas)); pg.wait_for_timeout(300); enregistre()
        al = [m for t_, m in dialogs if t_ == 'alert']
        check('sous le prix d\'achat : refusé, rien n\'est envoyé', not envois and al and 'trop bas' in al[-1].lower(), [envois, dialogs])
        check('et le message ne révèle PAS le prix d\'achat', al and not any(x in al[-1] for x in (str(PA), ('%.2f' % PA).replace('.', ','), '%.2f' % PA)), al)
        pose('patron'); pg.evaluate("localStorage.removeItem('ck-token')"); envois.clear(); shop(SHOP0); ouvre()
        champ().fill('54'); pg.wait_for_timeout(300); enregistre()
        check('sans connexion au cockpit : aucun envoi', not envois, envois)
        pg.evaluate("localStorage.setItem('ck-token','jeton-test')")

        print('6. ce qui n\'est jamais envoyé')
        envois.clear(); shop(SHOP0); ouvre(BC2)
        t = ligne().inner_text()
        check('un code-barres sur plusieurs produits Shopify : avertissement, pas de prix proposé', 'plusieurs produits' in t.lower(), t[:250])
        champ().fill('33'); pg.wait_for_timeout(300); enregistre()
        check('et rien n\'est envoyé même si on tape un prix', not envois, envois)
        shop({'_t': '2026-10-15T14:00:00', '_amb': []}); ouvre()
        t = ligne().inner_text()
        check('un parfum absent de Shopify : « Pas en ligne »', 'pas en ligne' in t.lower(), t[:250])
        envois.clear(); champ().fill('44'); pg.wait_for_timeout(300); enregistre()
        check('et rien n\'est envoyé', not envois, envois)
        check('aucune erreur JS', not err, err[:3])
        b.close()
finally:
    srv.terminate()
print(f'\n{ok} ok, {len(ko)} KO', ko)
