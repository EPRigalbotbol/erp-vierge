# RÉPARTIR UNE RÉCEPTION ENTRE PERFUMES TRADE ET PERFUME CITY (Igal, 20 oct. 2026 :
# « quand Sam rentre une new order … sur 16 parfums, il en donne 6 à Perfume City, et le stock est mis à jour
#   chez Perfume City et chez Perfumes Trade »). Ce que ce test protège :
#   1. sur une réception qui met le stock à jour, chaque ligne a DEUX cases qui se complètent (somme = quantité reçue) ;
#   2. LE POINT — le stock de Perfumes Trade n'augmente que de sa part (16 reçus, 6 à Perfume City → +10) ;
#   3. LE POINT — la part de Perfume City entre dans SON stock (pc-stock-v1), pas dans celui de Perfumes Trade ; depuis le
#      3 nov. 2026 (Igal), même règle que le transfert depuis la fiche : le premier flacon d'une référence part en tester (vitrine),
#      noté à part, et seul le vendable entre dans son stock et part sur Shopify ;
#   4. LE POINT — l'ERP envoie au cockpit exactement ce qui est donné à Perfume City, avec l'identifiant de la facture
#      (c'est lui qui empêche de compter deux fois) ;
#   5. si l'envoi à Shopify échoue : l'ERP est déjà à jour, la facture le dit, « Renvoyer à Shopify » refait l'envoi ;
#   6. annuler la facture retire la part de Perfume City (ERP et Shopify) et rend le stock d'avant ; si Shopify ne
#      répond pas, on demande avant de défaire l'ERP à moitié ;
#   7. pas de cases pour un rôle qui ne peut pas modifier les prix, ni quand le stock n'est pas mis à jour.
import pathlib, subprocess, time, socket, json
from playwright.sync_api import sync_playwright
D = pathlib.Path('/home/claude/catalogue')
ok = 0; ko = []
def check(n, c, i=''):
    global ok
    if c: ok += 1; print('  ok  ', n)
    else: ko.append(n); print('  KO  ', n, str(i)[:300])
s = socket.socket(); s.bind(('127.0.0.1', 0)); port = s.getsockname()[1]; s.close()
srv = subprocess.Popen(['python3', '-m', 'http.server', str(port), '--bind', '127.0.0.1'], cwd=str(D), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1)
CAT = json.load(open(D / 'cat.json'))
LIG = [r for r in CAT if r[0] and len(r[0]) >= 12 and (r[6] or 0) > 0 and r[7]]
A, A2 = LIG[0], LIG[3]
try:
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1700, 'height': 1100}); err = []
        pg.on('pageerror', lambda e: err.append(str(e)))
        DIAL = []; REPS = []
        def dlg(d):
            DIAL.append((d.type, d.message))
            if d.type == 'confirm': d.accept() if (REPS.pop(0) if REPS else True) else d.dismiss()
            else: d.accept()
        pg.on('dialog', dlg)
        base = f'http://127.0.0.1:{port}/'
        ENVOIS = []; MODE = {'v': 'ok'}
        def route(r):
            body = json.loads(r.request.post_data or '{}'); ENVOIS.append(body)
            if MODE['v'] == 'panne': r.fulfill(status=502, content_type='application/json', body=json.dumps({'erreur': 'Shopify ne répond pas'})); return
            lignes = []
            for it in body['items']:
                if MODE['v'] == 'absent' and it['bc'] == A2[0]: lignes.append({'bc': it['bc'], 'nom': it.get('nom'), 'etat': 'absent', 'raison': "ce parfum n'est pas (encore) chez Perfume City"})
                else: lignes.append({'bc': it['bc'], 'nom': it.get('nom'), 'etat': 'ok', 'ajout': it['ajout'], 'avant': 5, 'apres': 5 + it['ajout']})
            r.fulfill(status=200, content_type='application/json', body=json.dumps({'ok': True, 'lignes': lignes}))
        pg.route('**/shopify/stock-ajoute', route)
        def session(role):
            pg.goto(base + 'accueil.html'); pg.wait_for_timeout(300)
            pg.evaluate("""([role,A,A2])=>{ localStorage.clear(); localStorage.setItem('sam-comptes-demo-v1','0');
                localStorage.setItem('sam-comptes-v1',JSON.stringify([{ident:'u',nom:'Sam',role:role,actif:true,h:'x'}]));
                localStorage.setItem('sam-session-v1',JSON.stringify({id:'u',nom:'Sam',role:role,depuis:new Date().toISOString()}));
                localStorage.setItem('langue-v1','fr'); localStorage.setItem('ck-token','jeton-test');
                localStorage.setItem('fiches-modifiees-v1',JSON.stringify({[A[15]]:{qte:10,pa:30},[A2[15]]:{qte:4,pa:20}})); }""", [role, A, A2])
        def facture(num, qa=16, qb=5):
            pg.goto(base + 'factures.html'); pg.wait_for_timeout(2500)
            pg.click('#basc'); pg.fill('#colle', f"{A[2]} {A[1]}  {A[0]}  {qa}  36.00\n{A2[2]} {A2[1]}  {A2[0]}  {qb}  20.00\n"); pg.wait_for_timeout(700)
            pg.fill('#tiers', 'Fournisseur US'); pg.fill('#num', num); pg.wait_for_timeout(500)
        mod = lambda c: pg.evaluate("c=>JSON.parse(localStorage.getItem('fiches-modifiees-v1')||'{}')[c]||{}", c)
        pcq = lambda bc: pg.evaluate("bc=>{ const F=window.__F; const m=F.pcsCarte(); const o=m[F.pcsCle([bc])]; return o?o.q:null; }", bc)
        facts = lambda: pg.evaluate("()=>JSON.parse(localStorage.getItem('factures-v1')||'[]')")

        print('1. les deux cases')
        session('patron'); facture('PC-1')
        check('la colonne « Répartir » est là, avec deux cases par ligne reconnue', pg.locator('input.rp').count() == 4, pg.locator('input.rp').count())
        check('au départ tout va à Perfumes Trade (16 / 0)', pg.input_value('input.rp[data-i="0"][data-rp="pt"]') == '16' and pg.input_value('input.rp[data-i="0"][data-rp="pc"]') == '0')
        pg.fill('input.rp[data-i="0"][data-rp="pc"]', '6')
        check('LE POINT — taper 6 pour Perfume City règle l\'autre case à 10 (la somme reste 16)', pg.input_value('input.rp[data-i="0"][data-rp="pt"]') == '10')
        pg.fill('input.rp[data-i="1"][data-rp="pt"]', '3')
        print('   (ligne 2 : q=%s pt=%s pc=%s)' % (pg.evaluate("()=>window.__F.APERCU.L[1].q"), pg.input_value('input.rp[data-i="1"][data-rp="pt"]'), pg.input_value('input.rp[data-i="1"][data-rp="pc"]')))
        check('taper 3 pour Perfumes Trade règle Perfume City à 2 (sur 5)', pg.input_value('input.rp[data-i="1"][data-rp="pc"]') == '2')
        pg.fill('input.rp[data-i="0"][data-rp="pc"]', '7'); pg.wait_for_timeout(1100)
        check('LE POINT — pendant qu\'on tape, l\'aperçu se met à jour tout seul (+9 unités pour Perfume City) ET la case reste active', pg.evaluate("()=>document.activeElement.matches('input.rp[data-i=\"0\"][data-rp=\"pc\"]')") and '+9' in pg.locator('#apercu').inner_text(), [pg.evaluate("()=>document.activeElement.outerHTML.slice(0,120)"), pg.locator('#apercu').inner_text().replace(chr(10),' ')[:400]])
        pg.fill('input.rp[data-i="0"][data-rp="pc"]', '6'); pg.fill('input.rp[data-i="1"][data-rp="pc"]', '99'); pg.locator('input.rp[data-i="1"][data-rp="pc"]').blur(); pg.wait_for_timeout(500)
        check('une part plus grande que la quantité reçue est ramenée à la quantité (5 / 0)', pg.input_value('input.rp[data-i="1"][data-rp="pt"]') == '0' and pg.input_value('input.rp[data-i="1"][data-rp="pc"]') == '5', pg.input_value('input.rp[data-i="1"][data-rp="pc"]'))
        pg.fill('input.rp[data-i="1"][data-rp="pt"]', '3'); pg.locator('input.rp[data-i="1"][data-rp="pt"]').blur(); pg.wait_for_timeout(500)
        pg.fill('input.rp[data-i="0"][data-rp="pc"]', '6'); pg.locator('input.rp[data-i="0"][data-rp="pc"]').blur(); pg.wait_for_timeout(500)
        t = pg.locator('#apercu').inner_text()
        # 3 nov. 2026 (Sam : « j'ai besoin de savoir combien Perfume City a en stock aussi »)
        pcs = pg.evaluate("()=>document.querySelector('input.rp[data-i=\"0\"][data-rp=\"pc\"]').parentElement.querySelector('small.pcs').innerText.replace(/\u00a0/g,' ')")
        check('LE POINT — sous la case Perfume City : son stock actuel (0) et ce qu\'il deviendra (5 + 1 tester)', 'en stock 0' in pcs and '→ 5' in pcs and '1 tester' in pcs, pcs)
        pts = pg.evaluate("()=>document.querySelector('input.rp[data-i=\"0\"][data-rp=\"pt\"]').parentElement.querySelector('small.pcs').innerText.replace(/\u00a0/g,' ')")
        check('… et sous la case Perfumes Trade, son stock actuel (10)', 'en stock 10' in pts, pts)
        check('l\'aperçu : le stock de Perfumes Trade passe de 10 à 20 (+10), pas à 26', '10 → 20' in t.replace('\n', ' ') or '10 → 20' in t, t[:700])
        check('l\'aperçu compte 13 unités pour Perfumes Trade et 8 pour Perfume City', 'pour Perfumes Trade' in t and 'pour Perfume City' in t and '+13' in t and '+8' in t, t[:500])
        check('une note explique la répartition', pg.locator('.repnote').count() == 1 and 'ajoutés' in pg.locator('.repnote').inner_text().replace('\n', ' '))
        print('2. enregistrer')
        DIAL.clear(); pg.click('#ok'); pg.wait_for_timeout(1500)
        conf = next((d[1] for d in DIAL if d[0] == 'confirm'), '')
        check('la confirmation dit la répartition (13 pour Perfumes Trade, 8 pour Perfume City)', '13' in conf and 'Perfumes Trade' in conf and '8' in conf and 'Perfume City' in conf, conf)
        mA, mB = mod(A[15]), mod(A2[15])
        check('LE POINT — Perfumes Trade : 10 + 10 = 20 (et non 26), 4 + 3 = 7', mA.get('qte') == 20 and mB.get('qte') == 7, [mA, mB])
        check('LE POINT — le stock de Perfume City reçoit sa part EN VENTE : 6 → 5 et 2 → 1 (le premier flacon part en tester, règle du 3 nov. 2026)', pcq(A[0]) == 5 and pcq(A2[0]) == 1, [pcq(A[0]), pcq(A2[0])])
        T = pg.evaluate("()=>JSON.parse(localStorage.getItem('testeurs-pc-v1')||'{}')")
        check('… et un tester est noté pour chacun des deux parfums', T.get(A[0].lstrip('0'), {}).get('n') == 1 and T.get(A2[0].lstrip('0'), {}).get('n') == 1, T)
        check('prix moyen de Perfumes Trade calculé sur ses 10 flacons seulement : (10×30 + 10×36)/20 = 33', mA.get('pa') == 33, mA)
        F = facts(); f = next(x for x in F if x['num'] == 'PC-1')
        la = next(l for l in f['lignes'] if l['bc'] == A[0])
        check('la facture garde la part de chaque ligne (6 donnés = 5 en vente + 1 tester) et le stock de Perfume City avant/après', la.get('pc') == 6 and la.get('pcVend') == 5 and la.get('pcT') == 1 and la.get('pcAv') in (0, None) and la.get('pcAp') == 5 and la['q'] == 16, la)
        check('LE POINT — l\'ERP envoie au cockpit exactement le vendable, 5 et 1 (pas les testers), avec l\'identifiant de la facture', len(ENVOIS) == 1 and ENVOIS[0]['cle'] == f['id'] and sorted((i['bc'], i['ajout']) for i in ENVOIS[0]['items']) == sorted([(A[0], 5), (A2[0], 1)]), ENVOIS)
        check('la facture note que Shopify est à jour', f.get('pcShopify', {}).get('etat') == 'ok', f.get('pcShopify'))
        check('le message le dit', 'Shopify' in pg.inner_text('#msg') and 'mis à jour' in pg.inner_text('#msg'), pg.inner_text('#msg'))
        j = pg.evaluate("()=>JSON.parse(localStorage.getItem('crm-journal-v1')||'[]')")
        check('le journal garde la part de Perfume City', any('Perfume City' in (x.get('lib') or '') and 'réception' in (x.get('lib') or '') for x in j))

        print('3. Shopify en panne, puis renvoi')
        facture('PC-2', 4, 4); pg.fill('input.rp[data-i="0"][data-rp="pc"]', '4'); pg.locator('input.rp[data-i="0"][data-rp="pc"]').blur(); pg.wait_for_timeout(300)
        pcs = pg.evaluate("()=>document.querySelector('input.rp[data-i=\"0\"][data-rp=\"pc\"]').parentElement.querySelector('small.pcs').innerText.replace(/\u00a0/g,' ')")
        check('la 2e réception montre le stock de Perfume City d\'après la 1re : 5 + 1 tester → 9', 'en stock 5 + 1 tester' in pcs and '→ 9' in pcs, pcs)
        # 10 nov. 2026 (Igal : « sur tous les parfums, un tester chez Perfume City, pas plus ») : une donnée ancienne à 6 ne compte que pour 1
        pg.evaluate("bc=>{ const T=JSON.parse(localStorage.getItem('testeurs-pc-v1')||'{}'); T[bc.replace(/^0+/,'')].n=6; localStorage.setItem('testeurs-pc-v1',JSON.stringify(T)); }", A[0])
        pg.fill('input.rp[data-i="0"][data-rp="pc"]', '3'); pg.locator('input.rp[data-i="0"][data-rp="pc"]').blur(); pg.wait_for_timeout(300)
        pcs6 = pg.evaluate("()=>document.querySelector('input.rp[data-i=\"0\"][data-rp=\"pc\"]').parentElement.querySelector('small.pcs').innerText.replace(/\u00a0/g,' ')")
        check('LE POINT — un tester par parfum, jamais plus : une donnée ancienne à 6 s\'affiche « + 1 tester », et la livraison n\'en met pas un de plus de côté', 'en stock 5 + 1 tester' in pcs6 and '6 tester' not in pcs6 and '→ 8' in pcs6, pcs6)
        pg.evaluate("bc=>{ const T=JSON.parse(localStorage.getItem('testeurs-pc-v1')||'{}'); T[bc.replace(/^0+/,'')].n=1; localStorage.setItem('testeurs-pc-v1',JSON.stringify(T)); }", A[0])
        pg.fill('input.rp[data-i="0"][data-rp="pc"]', '4'); pg.locator('input.rp[data-i="0"][data-rp="pc"]').blur(); pg.wait_for_timeout(300)
        MODE['v'] = 'panne'; ENVOIS.clear(); pg.click('#ok'); pg.wait_for_timeout(1500)
        f2 = next(x for x in facts() if x['num'] == 'PC-2')
        check('LE POINT — Shopify en panne : l\'ERP est quand même à jour (Perfume City 5 + 4 = 9 : la boutique a déjà son tester, tout entre en vente)', pcq(A[0]) == 9, pcq(A[0]))
        check('la facture note l\'échec et le message dit « PAS encore sur Shopify » et « Renvoyer »', f2.get('pcShopify', {}).get('etat') == 'echec' and 'PAS encore sur Shopify' in pg.inner_text('#msg') and 'Renvoyer' in pg.inner_text('#msg'), [f2.get('pcShopify'), pg.inner_text('#msg')])
        pg.goto(base + 'factures.html'); pg.wait_for_timeout(2500)
        pg.locator(f'#liste tr[data-d="{f2["id"]}"]').click(); pg.wait_for_timeout(600)
        check('le détail de la facture montre « PAS envoyé à Shopify » et le bouton « Renvoyer à Shopify »', 'PAS envoyé' in pg.inner_text('#d-pc') and pg.locator('#d-pc-renvoi').is_visible(), pg.inner_text('#d-corps')[-300:])
        MODE['v'] = 'ok'; ENVOIS.clear(); pg.click('#d-pc-renvoi'); pg.wait_for_timeout(1500)
        f2 = next(x for x in facts() if x['num'] == 'PC-2')
        check('LE POINT — le renvoi part avec LA MÊME clé (le cockpit ne compte pas deux fois) et la facture passe à « envoyé »', len(ENVOIS) == 1 and ENVOIS[0]['cle'] == f2['id'] and f2['pcShopify']['etat'] == 'ok', [ENVOIS, f2.get('pcShopify')])
        check('le renvoi ne touche plus au stock de l\'ERP (toujours 9)', pcq(A[0]) == 9)
        print('4. un parfum absent de la boutique Perfume City')
        facture('PC-3', 2, 2); pg.fill('input.rp[data-i="1"][data-rp="pc"]', '2'); pg.locator('input.rp[data-i="1"][data-rp="pc"]').blur(); pg.wait_for_timeout(300)
        MODE['v'] = 'absent'; pg.click('#ok'); pg.wait_for_timeout(1500)
        f3 = next(x for x in facts() if x['num'] == 'PC-3')
        check('LE POINT — le parfum absent de Shopify est signalé par son nom, l\'ERP est à jour', f3['pcShopify']['etat'] == 'partiel' and "pas (encore) chez Perfume City" in pg.inner_text('#msg') and pcq(A2[0]) == 3, [f3.get('pcShopify'), pg.inner_text('#msg')])
        MODE['v'] = 'ok'

        print('5. annuler une facture')
        pg.goto(base + 'factures.html'); pg.wait_for_timeout(2500)
        f1 = next(x for x in facts() if x['num'] == 'PC-1'); ENVOIS.clear(); DIAL.clear()
        pg.locator(f'#liste tr[data-d="{f1["id"]}"] button[data-x]').click(); pg.wait_for_timeout(1500)
        check('LE POINT — l\'annulation retire le vendable, 5 et 1, chez Shopify, sous une clé « annule » distincte', len(ENVOIS) == 1 and ENVOIS[0]['cle'] == f1['id'] + '-annule' and sorted((i['bc'], i['ajout']) for i in ENVOIS[0]['items']) == sorted([(A[0], -5), (A2[0], -1)]), ENVOIS)
        check('Perfume City dans l\'ERP : 9 − 5 = 4, et 3 − 1 = 2', pcq(A[0]) == 4 and pcq(A2[0]) == 2, [pcq(A[0]), pcq(A2[0])])
        T = pg.evaluate("()=>JSON.parse(localStorage.getItem('testeurs-pc-v1')||'{}')")
        check('… et les deux testers de PC-1 sont retirés', not T.get(A[0].lstrip('0')) and not T.get(A2[0].lstrip('0')), T)
        check('LE POINT — Perfumes Trade perd exactement ce que PC-1 lui avait donné (10 et 3) : 22 − 10 = 12, 11 − 3 = 8 (les autres factures restent)', mod(A[15]).get('qte') == 12 and mod(A2[15]).get('qte') == 8, [mod(A[15]), mod(A2[15])])
        check('la facture a disparu de la liste', not any(x['num'] == 'PC-1' for x in facts()))
        f2 = next(x for x in facts() if x['num'] == 'PC-2'); MODE['v'] = 'panne'; ENVOIS.clear(); DIAL.clear(); REPS[:] = [True, False]
        av_pc, av_pt = pcq(A[0]), mod(A[15]).get('qte')
        pg.locator(f'#liste tr[data-d="{f2["id"]}"] button[data-x]').click(); pg.wait_for_timeout(1500)
        conf = [d[1] for d in DIAL if d[0] == 'confirm']
        check('LE POINT — Shopify ne répond pas à l\'annulation : on le dit et on demande avant de défaire l\'ERP', len(conf) == 2 and "n'a pas pu être retiré sur Shopify" in conf[1], conf)
        check('refusé : rien n\'est annulé (la facture et le stock de Perfume City restent)', any(x['num'] == 'PC-2' for x in facts()) and pcq(A[0]) == av_pc and mod(A[15]).get('qte') == av_pt, [pcq(A[0]), av_pc, [x['num'] for x in facts()]])

        print('6. qui voit les cases')
        session('comptable'); facture('PC-4')
        check('un rôle qui ne peut pas modifier les prix n\'a pas les cases (et ne peut donc rien envoyer à Shopify)', pg.locator('input.rp').count() == 0)
        session('patron'); facture('PC-5'); pg.locator('#o-stock').uncheck(); pg.wait_for_timeout(500)
        check('« Mettre le stock à jour » décoché : pas de cases (la facture est seulement archivée)', pg.locator('input.rp').count() == 0)
        check('aucune erreur JS', not err, err[:3])
        b.close()
finally:
    srv.terminate()
print(f'\n{ok} ok, {len(ko)} KO', ko)
raise SystemExit(1 if ko else 0)
