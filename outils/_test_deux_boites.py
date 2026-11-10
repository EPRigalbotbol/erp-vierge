# DEUX BOÎTES, UN MÊME CODE-BARRES, DEUX PRIX (Sam et Igal, 10 nov. 2026 : une eau de Cologne en ancienne boîte dorée et en nouvelle
# boîte blanche — « il ne veut pas vendre les deux au même prix », « deux produits séparés, à mettre en ligne partout »).
# Avant : les deux fiches tombaient sur LE MÊME produit du site ; le prix de l'ancienne boîte partait sur ce produit, et la fiche de
# la nouvelle affichait ce prix-là sur sa ligne Wholesale (85 $) alors que la ligne du Catalogue disait 53,76 $. Ce test protège :
#   1. LE POINT — la fiche « …oldbox » ne tombe plus sur le produit de l'autre boîte : pas encore créée sur le site, elle n'y est pas ;
#   2. LE POINT — la ligne Wholesale de la fiche affiche le prix de gros du Catalogue, pas celui du site ;
#   3. LE POINT — le stock annoncé au site pour la nouvelle boîte ne compte plus les flacons de l'ancienne (43, pas 54) ;
#   4. une fois créée sur le site avec son code « …oldbox » (quelle que soit la casse), l'ancienne boîte a SON produit, SON stock ;
#   5. LE POINT — une vente du site au code « …oldbox » va sur l'ancienne boîte, une vente au code nu sur la nouvelle ;
#   6. l'ancienne boîte est proposée à la mise en ligne sur les deux sites, et son code part entier au cockpit ;
#   7. un nom « … old box » sans le mot dans le code ne change rien (six fiches s'appellent déjà ainsi).
import pathlib, subprocess, time, socket, json, collections
from playwright.sync_api import sync_playwright

D = pathlib.Path('/home/claude/catalogue')
ok = 0; ko = []
def check(n, c, i=''):
    global ok
    if c: ok += 1; print('  ok  ', n)
    else: ko.append(n); print('  KO  ', n, str(i)[:500])
CAT = json.load(open(D / 'cat.json'))
# deux fiches du catalogue qui portent le même code-barres (la paire d'origine)
par = collections.defaultdict(list)
for r in CAT:
    if r[0] and str(r[0]).isdigit() and len(str(r[0])) >= 12 and r[15]: par[str(r[0])].append(r)
BC, (W, G) = next((k, v) for k, v in par.items() if len(v) == 2 and v[0][12] and 'old' in (v[1][1] or '').lower())
CW, CG = W[15], G[15]
s = socket.socket(); s.bind(('127.0.0.1', 0)); port = s.getsockname()[1]; s.close()
srv = subprocess.Popen(['python3', '-m', 'http.server', str(port), '--bind', '127.0.0.1'], cwd=str(D), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)
SITE = {BC: {'d': {'id': 7604, 'q': 54, 'suivi': True, 'etat': 'instock', 'nom': 'Maison Eau de cologne EDC 3.4 oz', 'pr': 159, 'ps': 118},
             'g': {'id': 7604, 'q': 54, 'suivi': True, 'etat': 'instock', 'nom': 'Maison Eau de cologne EDC 3.4 oz', 'pr': 85, 'ps': None}},
        '_maj': {'d': '2026-11-10T00:00:00Z', 'g': '2026-11-10T00:00:00Z'}}
MOD = {CW: {'qte': 43, 'pa': 48, 'pvr': 109, 'pvw': 53.76}, CG: {'bc': BC + 'oldbox', 'qte': 11, 'pa': 48, 'pvr': 118, 'pvw': 85}}
try:
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1456, 'height': 900}); err = []
        pg.on('pageerror', lambda e: err.append(str(e))); pg.on('dialog', lambda d: d.accept())
        envois = []
        def cockpit(route):
            body = json.loads(route.request.post_data or '{}'); envois.append((route.request.url.split('/api/o/dasy')[-1], body))
            route.fulfill(status=200, content_type='application/json', body=json.dumps({'ok': True, 'lignes': [{'bc': it.get('bc'), 'etat': 'brouillon', 'id': 9001, 'nom': it.get('nom'), 'barre': it.get('barre'), 'promo': None, 'qte': it.get('qte')} for it in body.get('items', [])]}))
        pg.route('**/api/o/dasy/site/cree', cockpit)
        base = f'http://127.0.0.1:{port}/'
        pg.goto(base + 'accueil.html'); pg.wait_for_timeout(400)
        def pose(site):
            pg.evaluate("""([S,M])=>{ localStorage.setItem('sam-session-v1', JSON.stringify({id:'sam',nom:'Sam',role:'patron',depuis:new Date().toISOString()}));
              localStorage.setItem('ck-token','jeton-test'); localStorage.setItem('site-stock-v1',JSON.stringify(S)); localStorage.setItem('fiches-modifiees-v1',JSON.stringify(M)); }""", [site, MOD])
            pg.goto(base + 'catalogue.html'); pg.wait_for_timeout(2600)
        pose(SITE)
        F = "c=>applique(tousLesArticles().find(x=>(x.cle||x.id)===c))"
        print('1. avant que l\'ancienne boîte ait son produit sur le site')
        r = pg.evaluate("([w,g])=>{ const W=applique(tousLesArticles().find(x=>(x.cle||x.id)===w)), G=applique(tousLesArticles().find(x=>(x.cle||x.id)===g)); return {w:siteCle(W), g:siteCle(G), sw:statutDiff(W,'site'), sg:statutDiff(G,'site'), gg:statutDiff(G,'sitegros'), meme:fichesMemeCode(W).length, qw:qteSiteDe(fichesMemeCode(W),SITE[siteCle(W)].d)}; }", [CW, CG])
        check('LE POINT — la nouvelle boîte est sur le site sous son code ; l\'ancienne boîte (« …oldbox ») n\'y est PAS : elle ne tombe plus sur le produit de l\'autre', r['w'] == BC and r['g'] is None and r['sw'] == 'oui' and r['sg'] == 'non' and r['gg'] == 'non', r)
        check('LE POINT — le stock de la nouvelle boîte pour le site : 43 (ses flacons), plus 54 (43 + 11)', r['meme'] == 1 and r['qw'] == 43, r)
        q = pg.evaluate("bc=>({w:_ssQteSite(bc,'d',{}), k:_ssCleSite(bc+'oldbox')})", BC)
        check('… et le tableau envoyé au cockpit dit pareil (43), sans ligne pour l\'ancienne boîte', q['w'] == 43 and q['k'] is None, q)
        print('2. la fiche affiche le prix de gros du Catalogue')
        pg.evaluate("c=>ouvreFiche(c)", CW); pg.wait_for_timeout(700)
        v = pg.evaluate("()=>{ const i=document.querySelector('#ddb [data-sbx=\"sitegros\"] input[data-sb]'); return i?i.value:null; }")
        pw = pg.evaluate("c=>applique(tousLesArticles().find(x=>(x.cle||x.id)===c)).pvw", CW)
        check('la ligne du Catalogue lit le même prix de gros (53,76)', pw == 53.76, pw)
        print('3. les ventes du site')
        t = pg.evaluate("bc=>{ const a=trouve(bc+'oldbox'), b=trouve(bc), c=trouve(bc+'OLDBOX'); return [a&&(a.cle||a.id), b&&(b.cle||b.id), c&&(c.cle||c.id)]; }", BC)
        check('LE POINT — le code « …oldbox » (ou « …OLDBOX ») retrouve la fiche de l\'ancienne boîte, le code nu la nouvelle', t == [CG, CW, CG], t)
        c2 = pg.evaluate("bc=>{ const C=faContexte(); return [C.cleDe({bc:bc+'oldbox',des:'x'}), C.cleDe({bc:bc,des:'x'})]; }", BC)
        check('LE POINT — une vente déposée par le site : « …oldbox » → ancienne boîte, code nu → nouvelle boîte', c2 == [CG, CW], c2)
        print('4. la mise en ligne de l\'ancienne boîte')
        c = pg.evaluate("g=>{ const G=applique(tousLesArticles().find(x=>(x.cle||x.id)===g)); const r=candidatsMel([G],['site','sitegros']); return {site:r.res.site.map(x=>[x.p.bc,x.v]), gros:r.res.sitegros.map(x=>[x.p.bc,x.v])}; }", CG)
        check('LE POINT — l\'ancienne boîte est proposée à la mise en ligne sur les deux sites, avec SON prix (118 / 85) et son code entier', c['site'] == [[BC + 'oldbox', 118]] and c['gros'] == [[BC + 'oldbox', 85]], c)
        print('5. une fois créée sur le site (code en majuscules, comme Sam pourrait le taper dans WooCommerce)')
        S2 = json.loads(json.dumps(SITE)); S2[BC + 'OLDBOX'] = {'d': {'id': 9001, 'q': 0, 'suivi': True, 'etat': 'outofstock', 'nom': 'Maison Eau de cologne old gold box', 'pr': 118, 'ps': None},
                                                                 'g': {'id': 9002, 'q': 0, 'suivi': True, 'etat': 'outofstock', 'nom': 'Maison Eau de cologne old gold box', 'pr': 85, 'ps': None}}
        pose(S2)
        r = pg.evaluate("([w,g,bc])=>{ const W=applique(tousLesArticles().find(x=>(x.cle||x.id)===w)), G=applique(tousLesArticles().find(x=>(x.cle||x.id)===g)); return {w:siteCle(W), g:siteCle(G), qw:_ssQteSite(bc,'d',{}), qg:_ssQteSite(bc+'oldbox','d',{}), kg:_ssCleSite(bc+'oldbox'), pw:planPrixSites(W).plan.map(x=>[x.cid,x.v]), pg:planPrixSites(G).plan.length}; }", [CW, CG, BC])
        check('LE POINT — chaque boîte a SON produit : la nouvelle sous le code nu, l\'ancienne sous « …OLDBOX » (la casse ne compte pas)', r['w'] == BC and r['g'] == BC + 'OLDBOX' and r['kg'] == BC + 'OLDBOX', r)
        check('LE POINT — chacune annonce SON stock : 43 et 11', r['qw'] == 43 and r['qg'] == 11, r)
        check('les prix à remettre : la nouvelle boîte reprend 109 et 53,76 sur son produit ; l\'ancienne est déjà à ses prix', sorted(r['pw']) == [['site', 109], ['sitegros', 53.76]] and r['pg'] == 0, r)
        pg.evaluate("c=>ouvreFiche(c)", CG); pg.wait_for_timeout(700)
        vg = pg.evaluate("()=>{ const i=document.querySelector('#ddb [data-sbx=\"sitegros\"] input[data-sb]'); return i?i.value:null; }")
        check('la fiche de l\'ancienne boîte affiche son prix de gros (85)', vg == '85.00', vg)
        print('6. un nom « old box » sans le mot dans le code ne change rien')
        n = pg.evaluate("()=>[nomMention('Parfum old gold box'), nomMention('Parfum old box edp'), mentionBC('123456789012oldbox').mention, mentionBC('123456789012').mention, nomMention('Gold Box Edition')]")
        check('seul le mot « oldbox » collé au code compte', n == ['', '', 'OLDBOX', '', ''], n)
        check('aucune erreur JS', not err, err[:3])
        b.close()
finally:
    srv.terminate()
print(f'\n{ok} ok, {len(ko)} KO', ko); raise SystemExit(1 if ko else 0)
