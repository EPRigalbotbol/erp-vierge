# LA COTE : LA RECHERCHE EN BAS, LA FICHE À DROITE, LE DERNIER PRIX PAYÉ PAR CE CLIENT (4 nov. 2026).
# Igal : « quand Sam a tapé plusieurs références sur la cote, il est obligé de remonter vers la barre de recherche :
# une barre en haut et une en bas » ; « qu'il puisse cliquer sur le produit qu'il a sélectionné dans la cote et avoir
# la fiche produit en latéral, comme s'il était sur le catalogue » ; « il fait une cote pour Robert et met un parfum que
# Robert a déjà commandé : je veux que Sam sache exactement le prix qu'il a payé la dernière fois ».
# Ce test protège :
#   1. la seconde barre de recherche apparaît sous les lignes dès 2 parfums, la liste des résultats vient sous elle,
#      le parfum choisi s'ajoute et la main reste EN BAS ;
#   2. un clic sur le nom d'un parfum de la cote ouvre la fiche du Catalogue en panneau à droite (mode cadre), et sa
#      fermeture rend la main à la cote ;
#   3. pour un client connu, la ligne d'un parfum qu'il a déjà acheté porte « <client> a payé le <date> <prix> »
#      (la vente la plus récente : factures de l'ERP ou historique d'avant l'ERP), un clic met ce prix ; rien pour un
#      parfum qu'il n'a jamais acheté ; rien sans client ;
#   4. tout cela en anglais et en espagnol.
import pathlib, subprocess, time, socket, json
from playwright.sync_api import sync_playwright

D = pathlib.Path('/home/claude/catalogue')
ok = 0; ko = []
def check(n, c, i=''):
    global ok
    if c: ok += 1; print('  ok  ', n)
    else: ko.append(n); print('  KO  ', n, str(i)[:400])
CAT = json.load(open(D / 'cat.json'))
R = [r for r in CAT if (r[6] or 0) > 2 and r[7] and r[8] and r[0] and len(str(r[0])) >= 12 and len(str(r[13] or '')) > 10 and str(r[13])[0].isalpha()]
A, B, C = R[0], R[1], R[2]
HG = json.loads(open(D / 'donnees/histgros.js').read().split('=', 1)[1].rstrip(';\n'))
# un parfum de l'historique d'avant l'ERP acheté par un client connu (le vrai tableur de Sam)
hist = None
for bc, L in HG['l'].items():
    for r in L:
        if r[3] and r[2] and HG['c'][r[1]] and len(HG['c'][r[1]]) > 3:
            cle = next((x[15] for x in CAT if str(x[0] or '').lstrip('0') == bc), None)
            if cle and cle not in (A[15], B[15], C[15]): hist = (bc, cle, HG['c'][r[1]], r[0], r[3]); break
    if hist: break
s = socket.socket(); s.bind(('127.0.0.1', 0)); port = s.getsockname()[1]; s.close()
srv = subprocess.Popen(['python3', '-m', 'http.server', str(port), '--bind', '127.0.0.1'], cwd=str(D), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1)
SESS = """([l,F])=>{ localStorage.clear(); localStorage.setItem('sam-comptes-demo-v1','0');
  localStorage.setItem('sam-comptes-v1',JSON.stringify([{ident:'sam',nom:'Sam',role:'patron',actif:true,h:'x'}]));
  localStorage.setItem('sam-session-v1',JSON.stringify({id:'sam',nom:'Sam',role:'patron',depuis:new Date().toISOString()}));
  localStorage.setItem('langue-v1',l); localStorage.setItem('factures-v1',JSON.stringify(F)); }"""
# Robert a acheté A deux fois (la plus récente à 45,50), jamais B ; une cote (pas une vente) à 99 ne compte pas ; un retour non plus
FACT = [
  {'id': 'f1', 'num': 'PT-2026-0001', 'd': '2026-10-02', 'h': '10:00', 'sens': 'vente', 'canal': 'Vente en gros', 'tiers': 'Robert', 'lignes': [{'cle': A[15], 'bc': A[0], 'q': 2, 'p': 40}]},
  {'id': 'f2', 'num': 'PT-2026-0002', 'd': '2026-10-20', 'h': '15:30', 'sens': 'vente', 'canal': 'Vente en gros', 'tiers': 'robert', 'lignes': [{'cle': A[15], 'bc': A[0], 'q': 1, 'p': 45.5}]},
  {'id': 'f3', 'num': 'Q-2026-0003', 'd': '2026-10-25', 'h': '09:00', 'sens': 'vente', 'canal': 'Vente en gros', 'tiers': 'Robert', 'doc': {'type': 'devis', 'num': 'Q3'}, 'lignes': [{'cle': A[15], 'bc': A[0], 'q': 1, 'p': 99}]},
  {'id': 'f4', 'num': 'PT-2026-0004', 'd': '2026-10-28', 'h': '09:00', 'sens': 'vente', 'canal': 'Vente en gros', 'tiers': 'Robert', 'retour': True, 'lignes': [{'cle': A[15], 'bc': A[0], 'q': 1, 'p': 12}]},
  {'id': 'f5', 'num': 'PT-2026-0005', 'd': '2026-10-21', 'h': '09:00', 'sens': 'vente', 'canal': 'Vente en gros', 'tiers': 'Javier', 'lignes': [{'cle': B[15], 'bc': B[0], 'q': 1, 'p': 33}]},
]
try:
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1456, 'height': 950}); err = []
        pg.on('pageerror', lambda e: err.append(str(e)))
        base = f'http://127.0.0.1:{port}/'
        def ouvre(lang='fr'):
            pg.goto(base + 'accueil.html'); pg.wait_for_timeout(300); pg.evaluate(SESS, [lang, FACT])
            pg.goto(base + 'quotes.html'); pg.wait_for_timeout(2500)
            if not pg.locator('#vov').is_visible(): pg.click('#nv'); pg.wait_for_timeout(400)
        def ajoute(r, bas=False):
            pg.fill('#v-q2' if bas else '#v-q', str(r[13])[:14]); pg.wait_for_timeout(450)
            pg.click('#v-res [data-cle="%s"]' % r[15]); pg.wait_for_timeout(150)
            if pg.locator('#v-cadd').count(): pg.click('#v-cadd'); pg.wait_for_timeout(250)
        ouvre()
        print('1. la barre de recherche du bas')
        check('avec 0 parfum : pas de barre du bas', pg.evaluate("$('v-q2w').hidden"))
        ajoute(A)
        # 11 nov. 2026 (Igal : « n'oublie pas la barre de recherche en bas ») : elle apparaît dès le premier parfum
        check('avec 1 parfum : la barre du bas est déjà là', not pg.evaluate("$('v-q2w').hidden"))
        ajoute(B)
        check('avec 2 parfums : la barre du bas apparaît sous les lignes', pg.evaluate("!$('v-q2w').hidden && $('v-q2w').compareDocumentPosition($('v-pan')) & Node.DOCUMENT_POSITION_PRECEDING"))
        pg.click('#v-q2'); pg.wait_for_timeout(100)
        pg.fill('#v-q2', str(C[13])[:14]); pg.wait_for_timeout(450)
        check('LE POINT — la liste des résultats vient se placer sous la barre du bas', pg.evaluate("$('v-res').parentNode.id==='v-q2w' && $('v-res').classList.contains('on')"))
        pg.click('#v-res [data-cle="%s"]' % C[15]); pg.wait_for_timeout(150)
        if pg.locator('#v-cadd').count(): pg.click('#v-cadd'); pg.wait_for_timeout(250)
        n = pg.evaluate("PANIER.length")
        check('le parfum choisi en bas est ajouté à la cote (3 lignes)', n == 3, n)
        check('et la main reste EN BAS : case du bas vide et active, pas de remontée', pg.evaluate("document.activeElement===$('v-q2') && $('v-q2').value===''"), pg.evaluate("document.activeElement&&document.activeElement.id"))
        pg.click('#v-q'); pg.wait_for_timeout(100)
        check('un clic sur la barre du haut la reprend : la liste des résultats la suit', pg.evaluate("$('v-res').parentNode===$('v-q').parentNode"))

        print('2. la fiche du parfum en panneau à droite')
        pg.click('#v-pan b.vfiche[data-fiche="%s"]' % A[15]); pg.wait_for_timeout(600)
        src = pg.evaluate("(document.querySelector('#fv-ov iframe')||{}).src||''")
        check('LE POINT — un clic sur le nom ouvre la fiche du Catalogue, en mode cadre, à droite', 'catalogue.html#cle=' in src and 'cadre=1' in src and A[15] in src, src)
        fr = pg.frames[-1] if len(pg.frames) > 1 else None
        if fr:
            fr.wait_for_timeout(3500)
            t = fr.evaluate("(document.querySelector('.dnom,.dh h2,#dnom')||{}).textContent||document.title")
            check('la fiche montrée est celle du bon parfum', (A[13] or '')[:10].lower() in (t or '').lower(), t)
        pg.evaluate("window.postMessage({fiche:'fermee'},location.origin)"); pg.wait_for_timeout(300)
        check('à la fermeture, le panneau disparaît et la cote est toujours là avec ses 3 lignes', pg.evaluate("!document.getElementById('fv-ov') && PANIER.length===3 && !$('vov').hidden"), pg.evaluate("[!!document.getElementById('fv-ov'), PANIER.length, $('vov').hidden]"))

        print('3. le dernier prix payé par ce client')
        check('sans client : aucune pastille « a payé »', pg.evaluate("document.querySelectorAll('#v-pan .puc.dp').length===0"))
        pg.fill('#v-client', 'Robert'); pg.dispatch_event('#v-client', 'change'); pg.wait_for_timeout(600)
        dp = pg.evaluate("[...document.querySelectorAll('#v-pan tbody tr')].map(tr=>{ const c=tr.querySelector('.puc.dp'); return c?[c.dataset.pv, c.textContent.trim()]:null; })")
        check('LE POINT — la ligne du parfum que Robert a déjà acheté porte « Robert a payé le 10/20/26 45,50 $ » (la plus récente, pas la cote à 99, pas le retour)', dp[0] and dp[0][0] == '45.5' and 'Robert a payé le 10/20/26' in dp[0][1] and '45' in dp[0][1], dp)
        check('rien sur les parfums que Robert n\'a jamais achetés (celui acheté par Javier non plus)', dp[1] is None and dp[2] is None, dp)
        pg.fill('#v-client', 'Robert '); pg.click('#v-pan .puc.dp'); pg.wait_for_timeout(500)
        check('un clic sur la pastille, même juste après avoir tapé le client, met ce prix sur la ligne', pg.evaluate("PANIER[0].p===45.5 && document.querySelector('#v-pan input[data-i=\"0\"][data-f=\"p\"]').value==='45.5'"), pg.evaluate("[PANIER[0].p, document.querySelector('#v-pan input[data-i=\"0\"][data-f=\"p\"]').value, (document.querySelector('#v-pan .puc.dp')||{}).outerHTML]"))
        if hist:
            PANIER = pg.evaluate("PANIER=[]; peintPanier(); 0")
            pg.fill('#v-client', hist[2]); pg.dispatch_event('#v-client', 'change'); pg.wait_for_timeout(600)
            pg.evaluate("c=>{ PANIER.push({cle:c,q:1,p:null}); peintPanier(); }", hist[1]); pg.wait_for_timeout(300)
            v = pg.evaluate("(document.querySelector('#v-pan .puc.dp')||{}).dataset||{}")
            attendu = pg.evaluate("([c,cli])=>dernierPrixClient(c,cNorm(cli))", [hist[1], hist[2]])
            check('l\'historique de gros d\'avant l\'ERP (tableur de Sam) compte aussi : %s a bien un dernier prix sur ce parfum' % hist[2], attendu and v.get('pv') == str(attendu['p']), (hist, v, attendu))
        pg.fill('#v-client', ''); pg.dispatch_event('#v-client', 'change'); pg.wait_for_timeout(600)
        check('le client effacé : la pastille s\'en va', pg.evaluate("document.querySelectorAll('#v-pan .puc.dp').length===0"))

        print('4. en anglais et en espagnol')
        for lang, mots, fr_interdits in (('en', ['add more perfumes', 'without scrolling up', 'robert paid on'], ['sans remonter', 'a payé']),
                                         ('es', ['añadir más perfumes', 'sin volver arriba', 'robert pagó el'], ['sans remonter', 'a payé'])):
            ouvre(lang); ajoute(A); ajoute(B)
            pg.fill('#v-client', 'Robert'); pg.dispatch_event('#v-client', 'change'); pg.wait_for_timeout(600)
            txt = (pg.inner_text('#vov') + ' ' + (pg.get_attribute('#v-q2', 'placeholder') or '')).lower()
            manque = [m for m in mots if m not in txt]; reste = [m for m in fr_interdits if m in txt]
            check(f'en {lang} : barre du bas et pastille « a payé » traduites, aucun mot français', not manque and not reste, {'manque': manque, 'reste': reste})
        check('aucune erreur JS', not err, err[:3])
        b.close()
finally:
    srv.terminate()
print(f'\n{ok} ok, {len(ko)} KO', ko); raise SystemExit(1 if ko else 0)
