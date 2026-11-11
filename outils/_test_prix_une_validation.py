# UNE SEULE VALIDATION POUR TOUS LES PRIX (20 oct. 2026).
# Igal : « lorsqu'on change les prix sur les différents canaux sur le même produit, Sam est obligé de valider
# plusieurs fois, en cliquant sur plusieurs fenêtres à la suite : quand il enregistre, ça doit se faire tout seul. »
# Ce test protège :
#   1. prix du site, prix du gros, prix Perfume City (Shopify) ET prix de l'outil changés ensemble (plus de prix barré : 11 nov. 2026) :
#      EXACTEMENT UNE fenêtre à l'Enregistrer, aucune boîte confirm() du navigateur ;
#   2. un clic sur « OK, enregistrer » envoie tout, dans l'ordre, sans autre question, et range la fiche ;
#   4. « Revenir à la fiche » n'envoie RIEN, et on peut ré-enregistrer ensuite (le drapeau est remis à zéro) ;
#   5. un prix de l'outil seul (sans case des sites) garde sa fenêtre unique avec la case « mettre aussi sur les sites ».
import pathlib, subprocess, time, socket, json
from playwright.sync_api import sync_playwright

D = pathlib.Path('/home/claude/catalogue')
ok = 0; ko = []
def check(n, c, i=''):
    global ok
    if c: ok += 1; print('  ok  ', n)
    else: ko.append(n); print('  KO  ', n, str(i)[:400])
CAT = json.load(open(D / 'cat.json'))
P = next(r for r in CAT if (r[6] or 0) > 2 and r[12] and r[7] and r[8] and r[7] > r[12] + 10 and r[0] and len(str(r[0])) == 12 and str(r[0]).startswith('0'))
BC = str(P[0]); K = BC.lstrip('0'); PA = float(P[12]); PVR = float(P[7]); PVW = float(P[8])
s = socket.socket(); s.bind(('127.0.0.1', 0)); port = s.getsockname()[1]; s.close()
srv = subprocess.Popen(['python3', '-m', 'http.server', str(port), '--bind', '127.0.0.1'], cwd=str(D), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1)
SITE0 = {BC: {'d': {'id': 101, 'q': 5, 'suivi': True, 'etat': 'instock', 'nom': 'x', 'pr': PVR, 'ps': None},
              'g': {'id': 201, 'q': 2, 'suivi': True, 'etat': 'instock', 'nom': 'x', 'pr': PVW, 'ps': None}}}
SHOP0 = {K: ['1', '11', 64.0, None, 1], '_t': '2026-10-20T14:00:00', '_amb': []}
try:
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1456, 'height': 950}); err = []
        pg.on('pageerror', lambda e: err.append(str(e)))
        dialogs = []
        pg.on('dialog', lambda d: (dialogs.append((d.type, d.message)), d.accept()))
        ordre = []
        def site(route):
            body = json.loads(route.request.post_data or '{}'); ordre.append(('site', body))
            route.fulfill(status=200, content_type='application/json', body=json.dumps({'ok': True, 'avant': body.get('attendu'), 'apres': {'barre': body.get('barre'), 'promo': None if body.get('promo') in ('', None) else body.get('promo')}}))
        def shop(route):
            body = json.loads(route.request.post_data or '{}'); ordre.append(('shopify', body))
            route.fulfill(status=200, content_type='application/json', body=json.dumps({'ok': True, 'avant': body.get('attendu'), 'apres': body.get('prix'), 'nom': 'x'}))
        pg.route('**/api/o/dasy/site/prix', site); pg.route('**/api/o/dasy/shopify/prix', shop)
        base = f'http://127.0.0.1:{port}/'
        pg.add_init_script("document.addEventListener('DOMContentLoaded',()=>{const s=document.createElement('style');s.textContent='#svtem{display:none!important}';document.head.appendChild(s)})")
        pg.goto(base + 'accueil.html'); pg.wait_for_timeout(400)
        def ouvre():
            pg.evaluate("""([a,b])=>{ localStorage.setItem('sam-session-v1', JSON.stringify({id:'sam',nom:'Sam',role:'patron',depuis:new Date().toISOString()}));
                localStorage.setItem('ck-token','jeton-test'); localStorage.setItem('site-stock-v1',JSON.stringify(a)); localStorage.setItem('shopify-pc-prix-v1',JSON.stringify(b));
                localStorage.removeItem('fiches-modifiees-v1'); }""", [SITE0, SHOP0])
            pg.goto(base + 'catalogue.html'); pg.wait_for_timeout(2500)
            pg.evaluate("bc=>{ $('fs').value=''; $('q').value=bc; render(); ouvreFiche(cur.find(p=>String(p.bc)===bc).id); }", BC); pg.wait_for_timeout(500)
            # compteur de fenêtres : combien de fois #pxov passe à « on »
            pg.evaluate("""()=>{ window.__ov=0; const o=document.getElementById('pxov'); let was=false;
                new MutationObserver(()=>{ const on=o.classList.contains('on'); if(on&&!was) window.__ov++; was=on; }).observe(o,{attributes:true,attributeFilter:['class']}); }""")
        def boite(cid):
            pg.evaluate("cid=>{ const d=document.querySelector('[data-sbx=\"'+cid+'\"]'); const x=d&&d.closest('details'); if(x) x.open=true; }", cid)
            return pg.locator(f'[data-sbx="{cid}"]')
        # 5 nov. 2026 (Igal) : le site de détail n'a plus de case promo — le client paie le prix retail de la fiche (case de gauche)
        def promo(cid, v):
            pg.locator('input[data-pc="site"]').fill(str(v)); pg.locator('#ddb h3').first.click(); pg.wait_for_timeout(300)
        def barre(v):
            boite('site').locator('[data-sb]').fill(str(v)); pg.wait_for_timeout(150)
        def pc(v): pg.locator('.dcanl .cn[data-cn="perfumecity"] input[data-pc="perfumecity"]').fill(str(v)); pg.wait_for_timeout(200)
        ov = lambda: pg.evaluate("()=>window.__ov")
        ouvert = lambda: pg.evaluate("()=>document.getElementById('pxov').classList.contains('on')")
        MOD = lambda: pg.evaluate("bc=>{ const p=cur.find(x=>String(x.bc)===bc); return JSON.parse(localStorage.getItem('fiches-modifiees-v1')||'{}')[p.id]||{}; }", BC)

        print('1. quatre prix changés d\'un coup : UNE fenêtre, aucune boîte du navigateur')
        ouvre()
        pr = round(PVR - 4, 2); pw = round(PVW - 3, 2)
        promo('site', pr); boite('sitegros').locator('[data-sb]').fill(str(pw)); pg.wait_for_timeout(150); pc('61.5')
        check('départ : deux boîtes de sites en attente + Perfume City en attente', pg.evaluate("boitesEnAttente().length") == 2 and bool(pg.evaluate("pcShopEnAttente()")), pg.evaluate("boitesEnAttente().length"))
        pg.click('#dok'); pg.wait_for_timeout(700)
        check('LE POINT — UNE seule fenêtre s\'ouvre à l\'Enregistrer (pas une par canal)', ov() == 1 and ouvert(), ov())
        check('LE POINT — aucune boîte confirm() du navigateur', not [d for d in dialogs if d[0] == 'confirm'], dialogs)
        check('rien n\'est parti avant le clic sur « OK, enregistrer »', not ordre, ordre)
        t = pg.inner_text('#pxb')
        check('la fenêtre montre ce qui part sur le site et sur Perfume City', 'Perfume City' in t or 'Shopify' in t.title() or '61' in t, t[:300])
        pg.click('#pxok'); pg.wait_for_timeout(1500)
        check('LE POINT — après ce seul clic : plus aucune fenêtre ouverte, et toujours UNE seule vue', not ouvert() and ov() == 1, ov())
        check('LE POINT — tout est parti : deux envois site + un envoi Shopify', [o[0] for o in ordre].count('site') == 2 and [o[0] for o in ordre].count('shopify') == 1, [o[0] for o in ordre])
        check('dans l\'ordre : les sites avant Perfume City', [o[0] for o in ordre][-1] == 'shopify', [o[0] for o in ordre])
        check('le prix Shopify envoyé est celui tapé, avec le prix attendu', next(o[1] for o in ordre if o[0] == 'shopify').get('prix') == 61.5 and next(o[1] for o in ordre if o[0] == 'shopify').get('attendu') == 64.0)
        m = MOD()
        check('Perfume City : le prix EST maintenant celui de Shopify (61,5), plus aucun prix « manuel » en attente dans la fiche',
              not (m.get('pc') or {}).get('perfumecity') and pg.locator('.dcanl .cn[data-cn="perfumecity"] input[data-pc="perfumecity"]').input_value() in ('61.5', '61,5'), (m, pg.locator('.dcanl .cn[data-cn="perfumecity"] input[data-pc="perfumecity"]').input_value()))
        check('et la fiche l\'annonce « enregistré »', 'enregistré' in pg.locator('#dst').inner_text(), pg.locator('#dst').inner_text())

        # 11 nov. 2026 (Sam) : plus de prix barré — le cas « prix barré plus bas que le retail » n'existe plus
        print('3. « Revenir à la fiche » n\'envoie rien, et on peut ré-enregistrer ensuite')
        ordre.clear(); dialogs.clear(); ouvre()
        promo('site', round(PVR - 2, 2)); pc('62')
        pg.click('#dok'); pg.wait_for_timeout(600)
        pg.click('#pxc'); pg.wait_for_timeout(500)
        check('LE POINT — refusé : rien n\'est parti, rien n\'est rangé', not ordre and not (MOD().get('pc') or {}).get('perfumecity'), (ordre, MOD()))
        pg.click('#dok'); pg.wait_for_timeout(600); pg.click('#pxok'); pg.wait_for_timeout(1500)
        check('on ré-enregistre : une nouvelle fenêtre, un clic, et tout part (le refus n\'a rien laissé de bloqué)',
              [o[0] for o in ordre].count('site') == 1 and [o[0] for o in ordre].count('shopify') == 1 and ov() == 2, ([o[0] for o in ordre], ov()))

        print('3b. case du gros + prix de l\'outil du retail : une fenêtre, chacun reçoit SON prix')
        ordre.clear(); dialogs.clear(); ouvre()
        boite('sitegros').locator('[data-sb]').fill(str(round(PVW - 2, 2))); pg.wait_for_timeout(150)
        pg.fill('#ddb input[data-k="pvr"]', str(round(PVR - 3, 2))); pg.click('#dnom'); pg.wait_for_timeout(300)
        pg.click('#dok'); pg.wait_for_timeout(700)
        check('LE POINT — UNE seule fenêtre : le message du gros ET celui du retail (le site suit le prix retail de la fiche, sans case à cocher)', ov() == 1 and 'wholesale' in pg.inner_text('#pxb') and '« Abercrombie' in pg.inner_text('#pxb') and 'sur perfumestrade.com' in pg.inner_text('#pxb'), (ov(), pg.inner_text('#pxb')[:300]))
        pg.click('#pxok'); pg.wait_for_timeout(1800)
        sites = [o[1] for o in ordre if o[0] == 'site']
        check('LE POINT — le gros reçoit le prix de SA case, le retail reçoit le prix de l\'outil (aucun des deux n\'est oublié)',
              any(x.get('quel') == 'gros' and abs(x['barre'] - round(PVW - 2, 2)) < 0.011 for x in sites) and any(x.get('quel') == '' for x in sites), sites)
        print('4. un prix de l\'outil seul : une fenêtre, avec la case « mettre aussi sur les sites »')
        ordre.clear(); dialogs.clear(); ouvre()
        n0 = pg.evaluate("()=>document.querySelectorAll('[data-sb]').length")
        champ = pg.locator('input[data-pc="site"]') if pg.locator('input[data-pc="site"]').count() else None
        if champ is not None: champ.fill(str(round(PVR - 1, 2)))
        else: pg.locator('.dcanl input[data-pc]').first.fill(str(round(PVR - 1, 2)))
        pg.wait_for_timeout(250)
        pg.click('#dok'); pg.wait_for_timeout(700)
        check('une seule fenêtre, sans boîte du navigateur', ov() == 1 and not [d for d in dialogs if d[0] == 'confirm'], (ov(), dialogs))
        pg.click('#pxok'); pg.wait_for_timeout(1200)
        check('fenêtre fermée après le clic, fiche enregistrée', not ouvert() and 'enregistré' in pg.locator('#dst').inner_text(), pg.locator('#dst').inner_text())
        check('aucune erreur JS', not err, err[:3])
        b.close()
finally:
    srv.terminate()
print(f'\n{ok} ok, {len(ko)} KO', ko)
raise SystemExit(1 if ko else 0)
