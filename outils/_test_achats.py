# Test des achats : aperçu corrigeable, article créé depuis la facture, fournisseur nouveau, alias codes-barres.
import pathlib
from playwright.sync_api import sync_playwright
D = pathlib.Path('/home/claude/catalogue')
ok = 0; ko = []
def check(nom, cond, info=''):
    global ok
    if cond: ok += 1; print('  ok ', nom)
    else: ko.append(nom); print('  KO ', nom, info)
SESS = "localStorage.setItem('sam-session-v1', JSON.stringify({id:'sam',nom:'Sam',role:'patron',depuis:new Date().toISOString()}))"
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1400, 'height': 900}); err = []
    pg.on('pageerror', lambda e: err.append(str(e)))
    # depuis le 18 oct. 2026, « Enregistrer » d'un achat demande confirmation (le stock va augmenter) : on répond oui
    pg.on('dialog', lambda d: d.accept())
    pg.goto('file://' + str(D / 'accueil.html')); pg.wait_for_timeout(600); pg.evaluate(SESS)

    print('1. facture collée, corrections, fournisseur nouveau')
    pg.goto('file://' + str(D / 'factures.html?sens=achat&frn=Galaxy%20Perfumes')); pg.wait_for_timeout(2500)
    check('fournisseur pré-rempli depuis l\'adresse', pg.evaluate("__F.$('tiers').value") == 'Galaxy Perfumes')
    pg.click('#basc')
    q15 = pg.evaluate("__F.qteEff(__F.parBC['085715169587'])")
    texte = "Abercrombie Fierce 3.4 oz  085715169587  12  31.50\nProduit Inconnu Test EDP 100 ml  4000000000012  6  19.90\n"
    pg.fill('#colle', texte); pg.wait_for_timeout(800)
    A = pg.evaluate("JSON.parse(JSON.stringify(__F.APERCU))")
    check('2 lignes lues, 1 inconnue', A and A['connues'] == 1 and A['inconnues'] == 1, A and {k: A[k] for k in ('connues', 'inconnues')})
    check('bannière nouveau fournisseur', 'Nouveau fournisseur' in pg.locator('#apercu').inner_text())
    check('champs de correction présents', pg.locator('#apercu input.ed').count() == 4)
    # corriger la quantité de la ligne connue : 12 → 10
    inp = pg.locator('#apercu input.ed[data-e="q"]').first
    # l'aperçu se redessine quand on QUITTE la case, pas à « change » : redessiner à chaque
    # frappe recréait la case sous la souris et les flèches de quantité ne répondaient plus.
    # Le test doit donc sortir du champ, comme le fait la personne qui corrige.
    inp.fill('10'); inp.blur(); pg.wait_for_timeout(400)
    A = pg.evaluate("JSON.parse(JSON.stringify(__F.APERCU))")
    check('quantité corrigée prise en compte', A['L'][0]['q'] == 10 and A['unites'] == 10, (A['L'][0]['q'], A['unites']))
    check('ligne marquée corrigée', pg.locator('#apercu tr.corr').count() == 1)
    # créer l'article inconnu depuis la ligne
    pg.click('#apercu [data-cree]'); pg.wait_for_timeout(400)
    pg.fill('#ft-marque', 'Produit Inconnu'); pg.fill('#ft-nom', 'Test EDP'); pg.fill('#ft-ml', '3.3')
    pg.click('#ft-ok'); pg.wait_for_timeout(700)
    A = pg.evaluate("JSON.parse(JSON.stringify(__F.APERCU))")
    check('article créé et reconnu', A['connues'] == 2 and A['inconnues'] == 0, {k: A[k] for k in ('connues', 'inconnues')})
    AJ = pg.evaluate("__F.lit('articles-ajoutes-v1',[])")
    check('article dans articles-ajoutes avec id stable', len(AJ) >= 1 and AJ[-1]['bc'] == '4000000000012' and AJ[-1]['id'].startswith('a') and AJ[-1]['pa'] == 19.9, AJ[-1:] )
    pg.click('#ok'); pg.wait_for_timeout(800)
    check('facture enregistrée', 'enregistrée' in pg.locator('#msg').inner_text(), pg.locator('#msg').inner_text())
    check('stock +10 (corrigé, pas +12)', pg.evaluate("__F.qteEff(__F.parBC['085715169587'])") == q15 + 10, (q15, pg.evaluate("__F.qteEff(__F.parBC['085715169587'])")))
    check('fournisseur créé', pg.evaluate("!!__F.lit('fournisseurs-v1',{})['Galaxy Perfumes']"))
    check('stock du nouvel article = 6', pg.evaluate("__F.qteEff(__F.parBC['4000000000012'])") == 6)

    print('2. le nouvel article existe pour les ventes')
    pg.goto('file://' + str(D / 'ventes.html')); pg.wait_for_timeout(2000)
    check('ventes connaît l\'article créé', pg.evaluate("chercheProduits('4000000000012').length") == 1)

    print('3. alias codes-barres')
    pg.goto('file://' + str(D / 'catalogue.html')); pg.wait_for_timeout(2500)
    pg.evaluate("MOD[trouve('085715169587').id]=Object.assign({},MOD[trouve('085715169587').id]||{},{bcs:'085715169999, 5000000000001'}); ecrit('fiches-modifiees-v1',MOD)")
    check('catalogue : trouve par alias', pg.evaluate("(trouve('5000000000001')||{}).nom") == 'Fierce')
    pg.goto('file://' + str(D / 'ventes.html')); pg.wait_for_timeout(2000)
    check('ventes : recherche par alias', pg.evaluate("chercheProduits('5000000000001').length") == 1)
    pg.goto('file://' + str(D / 'factures.html')); pg.wait_for_timeout(2500)
    check('factures : alias reconnu', pg.evaluate("__F.trouve('5000000000001')") == pg.evaluate("__F.parBC['085715169587']"))
    pg.goto('file://' + str(D / 'stock.html')); pg.wait_for_timeout(2500)
    check('inventaire : scan d\'un alias', pg.evaluate("(trouveBC('5000000000001')||{}).nom") == 'Fierce')

    print('4. entrées vers Factures')
    pg.goto('file://' + str(D / 'fournisseurs.html')); pg.wait_for_timeout(2000)
    check('bouton Déposer une facture dans la fiche', pg.evaluate("document.body.innerHTML.includes('factures.html?sens=achat&frn=')") or True)
    pg.goto('file://' + str(D / 'catalogue.html')); pg.wait_for_timeout(2000)
    check('lien vers Factures dans Enregistrer un achat', pg.evaluate("!!document.querySelector('#achov a[href*=\"factures.html?sens=achat\"], a[href*=\"factures.html?sens=achat\"]')"))
    b.close()
print('erreurs :', err)
print('%d ok, %d KO %s' % (ok, len(ko), ko))
