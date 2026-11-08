# METTRE À JOUR LIGHTSPEED (Igal, 8 nov. 2026 : « en un clic, transférer le fichier Wholesale et le fichier Retail sur Lightspeed pour
# mettre à niveau les prix, avec un formulaire déjà pré-rempli par l'ERP » ; « un beau bouton rouge Lightspeed dans le Catalogue »).
# Ce test protège :
#   1. le bouton rouge « Mettre à jour Lightspeed » est dans le Catalogue (Patron), pas pour un Commercial ;
#   2. la fenêtre lit l'export de la caisse gardé par le cockpit, rapproche chaque produit par code-barres (zéros de tête, « nobox »),
#      compte les prix retail à changer et les prix de gros à poser, liste les non-reconnus avec une fiche probable ;
#   3. « Même parfum » confirme une équivalence (mémorisée, synchronisée), « Pas dans l'ERP » l'écarte ;
#   4. « Préparer les fichiers » : le fichier RETAIL reprend les colonnes de l'export (sans le stock), seulement les lignes dont le prix
#      change, retail_price = prix du Catalogue ; le fichier WHOLESALE est au modèle de tarif de Lightspeed (sku, handle, retail_price…)
#      avec le prix de gros du Catalogue ; le journal le note ;
#   5. déposer un export envoie le fichier au cockpit (route de l'ERP, pas celle de l'admin) ;
#   6. en anglais et en espagnol, la fenêtre et le bouton sont traduits.
#   7. « ON N'A PAS LE DROIT À L'ERREUR » (Igal, 8 nov. 2026) : un prix qui change de plus du double / moins de la moitié, ou un prix de
#      gros au-dessus du retail, n'est pas envoyé (liste « à vérifier ») ; le fichier Retail n'emporte que id, handle, name, retail_price ;
#      le fichier Wholesale est au format de l'export du catalogue de prix, avec l'IDENTIFIANT de chaque ligne existante (sans lui,
#      Lightspeed crée un doublon) ; après un envoi, il faut des exports plus récents, sinon les fichiers sont bloqués ;
#   8. « Même parfum » marche aussi sur une fiche sans « cle » ; « Voir la fiche » ouvre la fiche sur le côté et la fenêtre revient.
import pathlib, subprocess, time, socket, json, csv, io
from playwright.sync_api import sync_playwright
D = pathlib.Path('/home/claude/catalogue')
ok = 0; ko = []
def check(n, c, i=''):
    global ok
    if c: ok += 1; print('  ok  ', n)
    else: ko.append(n); print('  KO  ', n, str(i)[:500])
s = socket.socket(); s.bind(('127.0.0.1', 0)); port = s.getsockname()[1]; s.close()
srv = subprocess.Popen(['python3', '-m', 'http.server', str(port), '--bind', '127.0.0.1'], cwd=str(D), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1)
CAT = json.load(open(D / 'cat.json'))
L = [r for r in CAT if r[7] and r[8] and r[12] and r[0] and str(r[0]).isdigit() and len(str(r[0])) >= 12 and len(str(r[13] or '')) > 8 and (r[6] or 0) > 2]
A, B, C, E, D = L[:5]   # A : prix différent ; B : même prix ; C : rapproché par le nom ; E : code avec un zéro de tête ; D : prix ×3 (douteux)
G = next(r for r in L if float(r[8]) > float(r[7]))   # fiche dont le prix de gros dépasse le prix retail
import datetime
def iso(h=0): return (datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None) - datetime.timedelta(hours=h)).strftime('%Y-%m-%dT%H:%M:%S.000Z')
COLS = ['id', 'handle', 'sku', 'name', 'description', 'tags', 'supply_price', 'retail_price', 'brand_name', 'active', 'inventory_Main_Outlet']
def row(i, sku, name, prix, brand):
    return {'id': 'u-%d' % i, 'handle': sku, 'sku': sku, 'name': name, 'description': '', 'tags': 'Homme, été', 'supply_price': '10', 'retail_price': prix, 'brand_name': brand, 'active': '1', 'inventory_Main_Outlet': '5'}
EXPORT = {'t': iso(), 'cols': [c for c in COLS if c != 'inventory_Main_Outlet'], 'n': 8, 'lignes': [
    row(1, str(A[0]), f'{A[2]} {A[13]} EDP 3.4 oz', '%.2f' % (float(A[7]) + 7), A[2]),             # prix caisse ≠ ERP → retail à changer
    row(2, str(B[0]), f'{B[2]} {B[13]}', '%.2f' % float(B[7]), B[2]),                              # même prix → pas dans le fichier retail
    row(3, 'XTESTER' + str(C[0])[-4:], f'{C[2]} {C[13]} Tester EDP 3.4 oz', '%.2f' % (float(C[7]) - 5), C[2]),   # pas de code : rapproché par le nom
    row(4, 'bags', 'bags', '0.30', ''),                                                            # ligne technique : pas dans l'ERP
    row(5, str(E[0]).lstrip('0'), f'{E[2]} {E[13]}', '%.2f' % (float(E[7]) + 1), E[2]),           # code sans le zéro de tête → reconnu quand même
    row(6, str(D[0]), f'{D[2]} {D[13]}', '%.2f' % (float(D[7]) / 3), D[2]),                        # l'ERP triplerait le prix → à vérifier
    row(7, str(G[0]), f'{G[2]} {G[13]}', '%.2f' % float(G[7]), G[2]),                              # gros au-dessus du retail → à vérifier
    row(8, 'VelNuitNobox', 'Maison Testeur Velours Imaginaire Nuit no box', '50.00', 'Maison Testeur'),   # fiche créée dans l'ERP, SANS « cle »
]}
V = 'VelNuitNobox'
AJOUT = [{'id': 'amutest1', 'bc': 'ZZNOBOX1', 'nom': 'Velours Imaginaire Nuit', 'marque': 'Maison Testeur', 'pvr': 50, 'pvw': 30, 'qte': 3}]
for l in EXPORT['lignes']: l.pop('inventory_Main_Outlet', None)
RECUS = []
try:
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1400, 'height': 1000}); err = []
        pg.on('pageerror', lambda e: err.append(str(e)))
        pg.on('dialog', lambda d: d.accept())
        def cockpit(route):
            u = route.request.url
            if '/donnees/lightspeed-export-v1' in u:
                route.fulfill(status=200, content_type='application/json', body=json.dumps({'ver': 1, 'maj': EXPORT['t'], 'par': 'test', 'val': EXPORT})); return
            if '/lightspeed/export' in u and route.request.method == 'POST':
                RECUS.append(route.request.post_data or ''); EXPORT['t'] = iso(); route.fulfill(status=200, content_type='application/json', body=json.dumps({'exportGarde': 7, 'appris': 7})); return
            if '/donnees/' in u: route.fulfill(status=404, content_type='application/json', body='{}'); return
            route.fulfill(status=200, content_type='application/json', body='{"ok":true}')
        pg.route('**/api/o/dasy/**', cockpit)
        base = f'http://127.0.0.1:{port}/'
        def prepare(lang='fr', role='patron'):
            pg.goto(base + 'accueil.html'); pg.wait_for_timeout(300)
            pg.evaluate("""([l,role,aj])=>{ localStorage.clear(); localStorage.setItem('sam-comptes-demo-v1','0');
                localStorage.setItem('sam-comptes-v1',JSON.stringify([{ident:'sam',nom:'Sam',role:'patron',actif:true,h:'x'},{ident:'josh',nom:'Josh',role:'commercial',actif:true,h:'x'}]));
                localStorage.setItem('sam-session-v1',JSON.stringify({id:role==='patron'?'sam':'josh',nom:role==='patron'?'Sam':'Josh',role,depuis:new Date().toISOString()}));
                localStorage.setItem('ck-token','jeton-test'); localStorage.setItem('langue-v1',l); localStorage.setItem('reglages-v1',JSON.stringify({societe:'DASY LLC'}));
                localStorage.setItem('articles-ajoutes-v1',JSON.stringify(aj)); }""", [lang, role, AJOUT])
            pg.goto(base + 'catalogue.html'); pg.wait_for_timeout(3500)

        print('1. le bouton')
        prepare()
        st = pg.evaluate("()=>{ const b=document.getElementById('lsmaj'); if(!b) return null; const cs=getComputedStyle(b); return {vis:b.offsetParent!==null, bg:cs.backgroundColor, txt:b.textContent.trim(), svg:!!b.querySelector('svg')}; }")
        check('LE POINT — le bouton « Mettre à jour Lightspeed » est dans le Catalogue, rouge, avec sa flamme', st and st['vis'] and st['txt'] == 'Mettre à jour Lightspeed' and st['svg'] and st['bg'] == 'rgb(232, 65, 44)', st)
        prepare(role='commercial')
        check('un Commercial ne le voit pas', pg.evaluate("()=>{ const b=document.getElementById('lsmaj'); return !b || b.offsetParent===null; }"))

        print('2. la fenêtre : export, reconnaissance, garde-fous, non-reconnus')
        prepare()
        pg.click('#lsmaj'); pg.wait_for_timeout(1500)
        t = pg.inner_text('#lsmcorps'); S = pg.evaluate("()=>{ const L=window.__LSM.get(); return {rec:L.rec.length, inc:L.inc.map(x=>[x.r.sku,x.sug.length]), n:L.n, dout:L.dout.map(x=>[x.r.sku,x.quoi]), B:L.bloque}; }")
        check('LE POINT — 5 produits reconnus par le code-barres (dont le code sans zéro de tête), 3 non reconnus', S['rec'] == 5 and len(S['inc']) == 3, S)
        check('LE POINT — 2 prix retail à changer (A et E) ; 3 prix de gros à envoyer ; rien de bloqué la première fois', S['n']['retail'] == 2 and S['n']['gros'] == 3 and S['B'] == {}, S)
        check('LE POINT — GARDE-FOU : le prix qui triplerait (D) ne part pas, ni son prix de gros (au-dessus du prix qui reste en caisse), ni le gros de G au-dessus du retail : « à vérifier »', sorted(S['dout']) == sorted([[str(D[0]), 'retail'], [str(D[0]), 'gros'], [str(G[0]), 'gros']]), S['dout'])
        check('la fiche créée dans l\'ERP sans « cle » est proposée (par son identifiant)', dict(S['inc']).get(V, 0) >= 1 and pg.evaluate(f"()=>document.querySelector('[data-lsmsel=\"{V}\"]').value") == 'amutest1', S['inc'])

        check('le testeur sans code a une fiche probable proposée ; « bags » n\'en a aucune', dict(S['inc']).get('XTESTER' + str(C[0])[-4:], 0) >= 1 and dict(S['inc']).get('bags') == 0, S['inc'])
        check('la fenêtre dit l\'export, 8 produits, les compteurs et la liste « à vérifier »', 'Export de la caisse du' in t and '8 produits' in t and 'prix retail à changer' in t and 'Prix à vérifier dans le Catalogue' in t and 'Non reconnus par le code-barres' in t and 'pas encore déposé' in t, t[:600])

        print('2b. voir la fiche sans quitter la page')
        pg.click(f'[data-lsmvoir="{V}"]'); pg.wait_for_timeout(700)
        S = pg.evaluate("()=>({ov:document.getElementById('lsmov').classList.contains('on'), dr:document.getElementById('dr').classList.contains('on'), id:FICHE&&FICHE.id, q:document.getElementById('q').value})")
        check('LE POINT — « Voir la fiche » : la fenêtre s\'efface, la fiche du Catalogue s\'ouvre sur le côté', not S['ov'] and S['dr'] and S['id'] == 'amutest1', S)
        pg.evaluate("()=>fermeFiche()"); pg.wait_for_timeout(700)
        S = pg.evaluate("()=>({ov:document.getElementById('lsmov').classList.contains('on'), dr:document.getElementById('dr').classList.contains('on'), q:document.getElementById('q').value, n:window.__LSM.get().inc.length})")
        check('LE POINT — la fiche fermée, la fenêtre Lightspeed revient telle quelle, la recherche du Catalogue est remise', S['ov'] and not S['dr'] and S['q'] == '' and S['n'] == 3, S)
        pg.click(f'[data-lsmfiche]'); pg.wait_for_timeout(700)
        S = pg.evaluate("()=>({dr:document.getElementById('dr').classList.contains('on'), id:FICHE&&FICHE.id})")
        check('un nom dans « à vérifier » ouvre sa fiche (pour corriger le prix)', S['dr'] and S['id'] in (str(D[0]), str(G[0])) or (S['dr'] and bool(S['id'])), S)
        pg.evaluate("()=>fermeFiche()"); pg.wait_for_timeout(500)
        print('3. confirmer une équivalence, écarter une ligne technique')
        sku_t = 'XTESTER' + str(C[0])[-4:]
        pg.click(f'[data-lsmoui="{sku_t}"]'); pg.wait_for_timeout(500)
        pg.click('[data-lsmnon="bags"]'); pg.wait_for_timeout(500)
        pg.click(f'[data-lsmoui="{V}"]'); pg.wait_for_timeout(500)
        S = pg.evaluate("()=>{ const L=window.__LSM.get(); return {rec:L.rec.length, inc:L.inc.length, n:L.n, P:lit('lightspeed-paires-v1',{})}; }")
        check('LE POINT — « Même parfum » : le testeur est rapproché de la fiche (équivalence mémorisée) ; « Pas dans l\'ERP » : bags écarté', S['rec'] == 7 and S['inc'] == 0 and S['n']['ignores'] == 1 and bool(S['P'].get(sku_t)) and S['P'].get(sku_t) != '-' and S['P'].get('bags') == '-', S)
        check('LE POINT — « Même parfum » marche aussi sur une fiche sans « cle » (Ariana Grande Cloud, 8 nov.)', S['P'].get(V) == 'amutest1', S['P'])
        J = pg.evaluate("()=>lit('crm-journal-v1',[]).map(j=>j.lib)")
        check('le Journal garde la confirmation', any('Lightspeed' in j and 'même parfum' in j for j in J), J[-2:])

        print('4. les deux fichiers')
        pg.click('#lsmok'); pg.wait_for_timeout(1500)
        F = pg.evaluate("()=>window.__LSM.get().derniers")
        R = list(csv.reader(io.StringIO('\n'.join(F['R'])))); W = list(csv.reader(io.StringIO('\n'.join(F['W']))))
        hdr = R[0]
        check('LE POINT — RETAIL : SEULEMENT id, handle, name, retail_price (une colonne absente, Lightspeed n\'y touche pas) ; 3 lignes (A, E, le testeur), prix du Catalogue ; ni D ni G',
              hdr == ['id', 'handle', 'name', 'retail_price'] and len(R) == 4 and {r[0] for r in R[1:]} == {'u-1', 'u-5', 'u-3'}
              and next(r for r in R[1:] if r[0] == 'u-1')[3] == '%.2f' % float(A[7]) and next(r for r in R[1:] if r[0] == 'u-1')[2] == f'{A[2]} {A[13]} EDP 3.4 oz', R)
        check('LE POINT — WHOLESALE : au format de l\'export d\'un catalogue de prix (sku, handle, id…), 5 lignes (A, B, E, testeur, fiche sans cle), identifiants vides la première fois, prix de gros du Catalogue ; pas G',
              W[0] == ['sku', 'handle', 'id', 'retail_price', 'loyalty_value', 'min_units', 'max_units'] and len(W) == 6 and all(r[2] == '' for r in W[1:])
              and next(r for r in W[1:] if r[0] == str(A[0]))[3] == '%.2f' % float(A[8]) and str(G[0]) not in {r[0] for r in W[1:]} and str(D[0]) not in {r[0] for r in W[1:]} and next(r for r in W[1:] if r[0] == V)[3] == '30.00', W)
        m = pg.inner_text('#lsmmsg'); J = pg.evaluate("()=>lit('crm-journal-v1',[]).map(j=>j.lib)")
        check('le message dit les deux fichiers (3 retail, 5 wholesale), le Journal aussi, avec les 2 prix à vérifier', 'Retail (3' in m and 'Wholesale (5' in m and any('fichiers Lightspeed préparés : 3 prix retail' in j and '5 prix de gros' in j and '3 prix à vérifier' in j for j in J), (m, J[-1:]))

        print('5. après un envoi : il faut des exports plus récents (sinon : doublons dans le catalogue de prix)')
        pg.click('#lsmannul'); pg.click('#lsmaj'); pg.wait_for_timeout(1500)
        S = pg.evaluate("()=>{ const L=window.__LSM.get(); return {B:L.bloque, dis:document.getElementById('lsmok').disabled, t:document.getElementById('lsmcorps').innerText}; }")
        check('LE POINT — les deux fichiers sont BLOQUÉS : l\'export des produits est plus ancien que l\'envoi, et le catalogue wholesale n\'a pas été exporté depuis ; le bouton est éteint',
              S['B'] == {'retail': 'vieux', 'gros': 'tarif'} and S['dis'] and 'Fichier RETAIL bloqué' in S['t'] and 'Fichier WHOLESALE bloqué' in S['t'] and 'doublons' in S['t'], S)
        pg.set_input_files('#lsm-fic', [{'name': 'general-price-book-all-products-2026.csv', 'mimeType': 'text/csv', 'buffer': ('sku,handle,id,retail_price,loyalty_value,min_units,max_units\r\n%s,%s,pg-1,99.00,,,\r\n' % (A[0], A[0])).encode()}])
        pg.wait_for_timeout(1200)
        check('le catalogue de prix GÉNÉRAL est refusé (ce n\'est pas le wholesale)', 'autre catalogue de prix' in pg.inner_text('#lsmmsg') and pg.evaluate("()=>lit('lightspeed-tarif-wholesale-v1',null)") is None, pg.inner_text('#lsmmsg'))
        tarif = 'sku,handle,id,retail_price,loyalty_value,min_units,max_units\r\n' + '\r\n'.join([
            '%s,%s,pb-A,%.2f,,,' % (A[0], A[0], float(A[8])),            # même prix : ne repart pas
            '%s,%s,pb-B,%.2f,,,' % (B[0], B[0], float(B[8]) - 2),        # prix différent : repart AVEC son identifiant
            '%s,%s,pb-E,%.2f,,,' % (str(E[0]).lstrip('0'), str(E[0]).lstrip('0'), float(E[8]) + 1)]) + '\r\n'
        pg.set_input_files('#lsm-fic', [{'name': 'product-export.csv', 'mimeType': 'text/csv', 'buffer': b'id,handle,sku,name,retail_price\r\nu-9,1,1,Test,5.00\r\n'},
                                        {'name': 'wholesale-2026-11-08.csv', 'mimeType': 'text/csv', 'buffer': ('\ufeff' + tarif).encode()}])
        pg.wait_for_timeout(2000)
        m = pg.inner_text('#lsmmsg'); S = pg.evaluate("()=>{ const L=window.__LSM.get(); return {B:L.bloque, n:L.n, dis:document.getElementById('lsmok').disabled}; }")
        check('LE POINT — les deux exports déposés d\'un coup : produits → cockpit (route de l\'ERP), catalogue wholesale → 3 identifiants gardés ; plus rien de bloqué', len(RECUS) == 1 and RECUS[0].startswith('id,handle,sku') and 'Export reçu' in m and 'Catalogue wholesale reçu : 3 prix' in m and S['B'] == {} and not S['dis'], (m, S))
        check('LE POINT — 4 prix de gros à envoyer, 1 déjà au bon prix (A)', S['n']['gros'] == 4 and S['n']['memes'] == 1, S['n'])
        pg.click('#lsmok'); pg.wait_for_timeout(1500)
        W = list(csv.reader(io.StringIO('\n'.join(pg.evaluate("()=>window.__LSM.get().derniers.W")))))
        ids = {r[0]: r[2] for r in W[1:]}
        check('LE POINT — WHOLESALE : la ligne déjà au catalogue repart avec SON identifiant (B → pb-B, E → pb-E), une nouvelle sans ; A (même prix) ne repart pas',
              ids.get(str(B[0])) == 'pb-B' and ids.get(str(E[0]).lstrip('0')) == 'pb-E' and str(A[0]) not in ids and ids.get(sku_t) == '' and ids.get(V) == '' and len(W) == 5, W)
        EXPORT['t'] = iso(30)
        pg.click('#lsmannul'); pg.evaluate("()=>{ localStorage.removeItem('lightspeed-envoye-v1'); }"); pg.click('#lsmaj'); pg.wait_for_timeout(1500)
        check('un export des produits de plus de 24 h bloque le fichier Retail', pg.evaluate("()=>window.__LSM.get().bloque.retail") == 'vieux')
        EXPORT['t'] = iso()

        print('6. en anglais et en espagnol')
        for lang, mots in (('en', ['Update Lightspeed', 'Register export of', 'retail prices to change', 'Prices to check in the Catalog', 'wholesale above retail', 'Not matched by barcode', 'Same perfume', 'Not in the ERP', 'Prepare the files', 'Wholesale price book: not dropped yet']),
                           ('es', ['Actualizar Lightspeed', 'Exportación de la caja del', 'precios retail a cambiar', 'Precios a verificar en el Catálogo', 'mayorista por encima del retail', 'No reconocidos por el código de barras', 'Mismo perfume', 'No está en el ERP', 'Preparar los archivos', 'Catálogo wholesale: todavía no depositado'])):
            prepare(lang)
            pg.click('#lsmaj'); pg.wait_for_timeout(1500)
            t = pg.inner_text('#lsmov') + ' ' + pg.inner_text('#lsmaj')
            check(f'en {lang} : bouton, fenêtre, boutons de la fenêtre traduits ; aucun mot français', all(m in t for m in mots) and 'Mettre à jour' not in t and 'Préparer' not in t and 'Non reconnus par le code' not in t and 'à vérifier' not in t and 'pas encore déposé' not in t, [m for m in mots if m not in t] or t[:300])
        check('aucune erreur JS', not err, err[:3])
        b.close()
finally:
    srv.terminate()
print(f'\n{ok} ok, {len(ko)} KO', ko); raise SystemExit(1 if ko else 0)
