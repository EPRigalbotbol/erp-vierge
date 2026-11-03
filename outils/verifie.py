# -*- coding: utf-8 -*-
"""Contrôle avant livraison — à lancer après chaque modification.

    python3 verifie.py

Il refabrique les dix pages, les ouvre une par une dans un vrai navigateur et
vérifie que rien n'est cassé. Tant que ce script n'affiche pas TOUT EST BON,
on ne livre pas.

C'est ce qui manquait : le 4 septembre, une version où « ventes.html » mourait
dès la première vente enregistrée est partie chez l'utilisateur. Ce contrôle
l'aurait attrapée.
"""
import subprocess, sys, pathlib, json, re

D = pathlib.Path(__file__).parent.resolve()
# Toutes les pages sont refaites ici, sans exception. Le 9 septembre, l'Etude de
# devis, les Messages et le Retail manquaient a cette liste : une correction dans
# un module partage (les comptes, la langue, les sorties) pouvait donc partir en
# ligne sans jamais avoir ete verifiee sur ces trois pages-la.
SCRIPTS = ['build_html.py','build_stock.py','build_ventes.py','build_factures.py',
           'build_clients.py','build_frn.py','build_journal.py','build_tableau.py',
           'build_reglages.py','build_connecteurs.py','build_acces.py','build_accueil.py',
           'build_etude.py','build_messages.py','build_retail.py','build_expeditions.py','build_taches.py']
PAGES = ['catalogue.html','stock.html','inventaire_pc.html','ventes.html','quotes.html','factures.html',
         'clients.html','fournisseurs.html','journal.html','tableau.html','reglages.html',
         'connecteurs.html','acces.html','expeditions.html','taches.html']

ok = []
ko = []


def dit(etat, quoi, detail=''):
    (ok if etat else ko).append(quoi)
    print(('  OK   ' if etat else '  ÉCHEC') + '  ' + quoi + (('  — ' + detail) if detail else ''))


print('\n1. Fabrication des dix pages')
for s in SCRIPTS:
    r = subprocess.run([sys.executable, s], cwd=D, capture_output=True, text=True)
    dit(r.returncode == 0, s, (r.stderr.strip().splitlines() or [''])[-1][:110])

if ko:
    print('\nUne page ne se fabrique plus. On s\'arrête là.\n')
    sys.exit(1)

# 20 oct. 2026 : inventaire_pc.html et quotes.html étaient restées en ligne dans une version du 17 oct., sans le
# « grenier » (les gros magasins en IndexedDB) : elles voyaient l'inventaire Perfume City VIDE, et une vente
# Shopify enregistrée depuis l'une d'elles passait « à découvert ». Chaque page porte donc ces briques, et toutes
# les pages fabriquées ensemble portent le même jour de fabrication (elles partent ensemble, jamais à moitié).
print('\n1b. Chaque page porte le grenier, la lecture du stock au serveur, et la même fabrication')
import re as _re
_jours = {}
for _p in sorted(set(PAGES + ['accueil.html', 'messages.html', 'retail.html', 'etude.html'])):
    _h = (D / _p).read_text()
    dit('__GRENIER' in _h and '__syFrais' in _h, _p + ' : grenier + stock relu au serveur')
    _m = _re.findall(r'\?v=(\d{12})', _h)
    if _m or _p in PAGES: _jours[_p] = _m[0][:8] if _m else '?'   # l'accueil ne charge aucune donnée : pas de tampon
dit(len(set(_jours.values())) == 1, 'toutes les pages sont de la même fabrication', str(sorted(set(_jours.values()))))

import os
from playwright.sync_api import sync_playwright


def fabrique_xlsx(chemin):
    """Écrit un vrai .xlsx, sans bibliothèque : c'est un zip de fichiers XML.

    On le fabrique ici plutôt que de le ranger dans le dépôt, pour que le
    contrôle marche sur n'importe quel poste, et on met dedans exactement ce
    qu'Excel met : des textes mis en commun (sharedStrings), une colonne de
    dates rangées en nombres, et deux onglets — comme le Google Sheet de Sam.
    """
    import zipfile, datetime
    ser = (datetime.date(2026, 8, 28) - datetime.date(1899, 12, 30)).days
    # « Supplier price » et non « Prix d'achat » : c'est le titre réel du fichier de Sam,
    # et c'est celui que l'import n'a pas reconnu la première fois.
    mots = ["Code-barres", "Nom", "Marque", "Quantité", "Supplier price", "Date",
            "Club de Nuit Intense", "Armaf", "Asad", "Lattafa",
            "Inventaire", "Perfume City"]
    si = ''.join('<si><t>%s</t></si>' % m.replace('&', '&amp;') for m in mots)

    def c(ref, val, s=None, t=None):
        a = ' s="%d"' % s if s is not None else ''
        a += ' t="%s"' % t if t else ''
        return '<c r="%s"%s><v>%s</v></c>' % (ref, a, val)

    f1 = ('<row r="1">' + c('A1', 0, t='s') + c('B1', 1, t='s') + c('C1', 2, t='s')
          + c('D1', 3, t='s') + c('E1', 4, t='s') + c('F1', 5, t='s') + '</row>'
          '<row r="2">' + c('A2', 3607345786780) + c('B2', 6, t='s') + c('C2', 7, t='s')
          + c('D2', 24) + c('E2', '18.5') + c('F2', ser, s=1) + '</row>'
          '<row r="3">' + c('A3', 8681215990249) + c('B3', 8, t='s') + c('C3', 9, t='s')
          + c('D3', 7) + c('E3', 12) + c('F3', ser, s=1) + '</row>')
    f2 = ('<row r="1">' + c('A1', 0, t='s') + c('B1', 1, t='s') + c('C1', 2, t='s')
          + c('D1', 3, t='s') + '</row>'
          '<row r="2">' + c('A2', 8681215990249) + c('B2', 8, t='s') + c('C2', 9, t='s')
          + c('D2', 3) + '</row>')
    feuille = ('<?xml version="1.0"?><worksheet xmlns="http://schemas.openxmlformats.org'
               '/spreadsheetml/2006/main"><sheetData>%s</sheetData></worksheet>')
    z = zipfile.ZipFile(chemin, 'w', zipfile.ZIP_DEFLATED)
    z.writestr('[Content_Types].xml',
               '<?xml version="1.0"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
               '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
               '<Default Extension="xml" ContentType="application/xml"/>'
               '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
               '<Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
               '<Override PartName="/xl/worksheets/sheet2.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
               '<Override PartName="/xl/sharedStrings.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sharedStrings+xml"/>'
               '<Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>'
               '</Types>')
    z.writestr('_rels/.rels',
               '<?xml version="1.0"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
               '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>'
               '</Relationships>')
    z.writestr('xl/workbook.xml',
               '<?xml version="1.0"?><workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
               'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets>'
               '<sheet name="Inventaire" sheetId="1" r:id="rId1"/>'
               '<sheet name="Perfume City" sheetId="2" r:id="rId2"/></sheets></workbook>')
    z.writestr('xl/_rels/workbook.xml.rels',
               '<?xml version="1.0"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
               '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>'
               '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet2.xml"/>'
               '<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/sharedStrings" Target="sharedStrings.xml"/>'
               '<Relationship Id="rId4" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
               '</Relationships>')
    z.writestr('xl/sharedStrings.xml',
               '<?xml version="1.0"?><sst xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
               'count="%d" uniqueCount="%d">%s</sst>' % (len(mots), len(mots), si))
    z.writestr('xl/styles.xml',
               '<?xml version="1.0"?><styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
               '<cellXfs count="2"><xf numFmtId="0"/><xf numFmtId="14" applyNumberFormat="1"/></cellXfs>'
               '</styleSheet>')
    z.writestr('xl/worksheets/sheet1.xml', feuille % f1)
    z.writestr('xl/worksheets/sheet2.xml', feuille % f2)
    z.close()
    return chemin


print('\n2. La porte d\'entrée')
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path='/opt/pw-browsers/chromium')
    c = b.new_context(viewport={'width': 1400, 'height': 1000}, accept_downloads=True)

    P0 = c.new_page(); e0 = []
    P0.on('pageerror', lambda x, e=e0: e.append(str(x)[:120]))
    P0.goto('file://' + str(D / 'catalogue.html')); P0.wait_for_timeout(2200)
    dit(P0.url.endswith('accueil.html'), 'sans session, on est renvoyé à l\'accueil', P0.url.split('/')[-1])
    noms = P0.eval_on_selector_all('.dbtn button', 'l=>l.map(x=>x.textContent)')
    # Compté sur la liste DEMO elle-même : un compte d'essai ajouté un jour ne doit
    # pas faire tomber le contrôle, mais un compte qui DISPARAÎT doit le faire.
    nDemo = P0.evaluate("DEMO.length")
    dit(len(noms) == nDemo and nDemo >= 4,
        'tous les comptes de démonstration sont proposés', ' · '.join(noms))
    P0.click('.dbtn [data-d="ana"]'); P0.wait_for_timeout(1400)
    sA = P0.evaluate("()=>JSON.parse(localStorage.getItem('sam-session-v1')||'null')")
    dit('stock.html' in P0.url.split('/')[-1] and (sA or {}).get('role') == 'entrepot',
        'Entrepôt arrive sur l\'Inventaire', P0.url.split('/')[-1])

    # on ressort, puis on entre par identifiant et mot de passe, en patron
    P0.evaluate("()=>localStorage.removeItem('sam-session-v1')")
    P0.goto('file://' + str(D / 'accueil.html')); P0.wait_for_timeout(1200)
    P0.fill('#i', 'sam'); P0.fill('#m', 'sam123')
    P0.click('#go'); P0.wait_for_timeout(1600)
    dit(P0.url.split('/')[-1].startswith('tableau.html'), 'Patron arrive sur le Tableau de bord',
        P0.url.split('/')[-1])
    s0 = P0.evaluate("()=>JSON.parse(localStorage.getItem('sam-session-v1')||'null')")
    dit(bool(s0) and s0.get('role') == 'patron', 'la session est ouverte, rôle patron')

    # mauvais mot de passe : refusé, et on reste dehors
    P0.evaluate("()=>localStorage.removeItem('sam-session-v1')")
    P0.goto('file://' + str(D / 'accueil.html')); P0.wait_for_timeout(1200)
    P0.fill('#i', 'sam'); P0.fill('#m', 'pasdutout')
    P0.click('#go'); P0.wait_for_timeout(900)
    dit('incorrect' in P0.inner_text('#msg') and P0.url.endswith('accueil.html'),
        'un mauvais mot de passe est refusé')

    # et on se remet en patron pour la suite du contrôle
    P0.evaluate("""()=>localStorage.setItem('sam-session-v1',JSON.stringify(
      {id:'sam',nom:'Sam',role:'patron',depuis:new Date().toISOString()}))""")
    dit(not e0, 'accueil.html sans erreur', e0[0] if e0 else '')
    P0.close()

    print('\n3. Les donnees sont hors des pages')
    import os
    for f in ['produits', 'clients', 'inventaire']:
        dit(os.path.exists(D / 'donnees' / (f + '.js')), 'donnees/' + f + '.js existe')
    # aucune page ne doit plus contenir une reference du stock de Sam
    sales = [f for f in PAGES if 'Fierce' in (D / f).read_text()]
    dit(not sales, 'aucune page ne transporte les references de Sam', ', '.join(sales))
    # Ce plafond garde contre UNE chose : que les 3 830 references reviennent
    # se coller dans la page (elle pesait 2,4 Mo avant qu'on les sorte). Il ne
    # sert pas a interdire d'ecrire du code. Quand il se declenche, la question
    # est donc : est-ce que ce sont des donnees ou du code ?
    #   10/09/2026 : 500 -> 540 Ko. La colonne Amazon et l'import de releves
    #   ont ajoute 10 Ko de code ; le controle « aucune page ne transporte les
    #   references de Sam », juste au-dessus, reste le vrai garde-fou.
    #   25/09/2026 : 540 -> 560 Ko. Le bloc commun qui passe avant chaque page
    #   (clients des ventes, lignes hors parfum, prix barre + promo) a ajoute 2 Ko.
    #   27/09/2026 : 560 -> 580 Ko. L'envoi automatique du stock aux sites (bloc commun
    #   de synchronisation) et le dictionnaire de traduction grossi : du code, pas des données.
    #   30/09/2026 : 580 -> 600 Ko. La mise à jour depuis le Google Sheet reprend les prix,
    #   crée les parfums manquants et retrouve un code changé par le nom (≈ 8 Ko de code),
    #   plus la photo du site en secours : du code, pas des données.
    #   01/10/2026 : 600 -> 640 Ko. Le fil en direct (une modification d'un autre poste arrive
    #   dans la seconde), le chef unique pour les ventes, les chiffres du menu en direct, l'envoi
    #   aux sites moins les commandes à expédier : du code, pas des données.
    #   07/10/2026 : 640 -> 660 Ko. Un code-barres partagé (boîte / NOBOX / tester) n'envoie
    #   plus qu'UNE quantité aux sites (qteSiteDe, fichesMemeCode) : du code, pas des données.
    #   09/10/2026 : 660 -> 700 Ko. La recherche réécrite (accents, apostrophes, rang), le contrôle des
    #   prix site / outil avec son bouton « aligner » : du code, pas des données.
    #   11/10/2026 : 700 -> 740 Ko. Historique des ventes par parfum (rythme, marge, Excel), canaux en
    #   lignes, fiche compacte, pastille « vendu sur Amazon » : du code, pas des données.
    #   13/10/2026 : 740 -> 760 Ko. Les ventes Shopify de Perfume City entrent dans l'inventaire de Perfume City
    #   (_file_auto.py, partagé par toutes les pages) : du code, pas des données.
    #   17/10/2026 : 760 -> 780 Ko. Prix Perfume City modifiable depuis la fiche (droit prixPC), compat anciens Safari : du code.
    #   17/10/2026 : 780 -> 800 Ko. Changer la photo d'un produit (réduction d'image, recherche sur Internet) : du code.
    #   17/10/2026 : 800 -> 820 Ko. Filtre « Diffusion » et pastilles par canal, une seule case de prix, fiche sans menu : du code.
    #   17/10/2026 : 820 -> 840 Ko. Mise en ligne des parfums absents des sites (fenêtre, prix barré, photo prêtée), grenier IndexedDB : du code.
    #   20/10/2026 : 840 -> 860 Ko. La vente sort du stock relu au serveur, génération de page (X-ERP-Proto), ordinateur sur chaque vente : du code.
    #   21/10/2026 : 860 -> 880 Ko. Mise en ligne automatique à la création d'un produit, une seule validation des prix, garde-fou prix/quantité, produit modifiable/retirable : du code.
    #   22/10/2026 : 880 -> 900 Ko. La price list de gros (fenêtre, Excel, PDF en vrai texte avec logo, WhatsApp, email), alertes de publication : du code.
    #   02/11/2026 : 900 -> 920 Ko. La colonne « Prix payé » par client dans « Ventes de ce parfum » : du code.
    #   03/11/2026 : 920 -> 950 Ko. La fenêtre de Léa (centrée, sombre, sphère animée au son de la voix) : du code.
    dit((D / 'catalogue.html').stat().st_size < 950_000, 'catalogue.html a maigri',
        str((D / 'catalogue.html').stat().st_size // 1024) + ' Ko')

    print('\n4. Chaque page s\'ouvre sans erreur')
    for f in PAGES:
        p = c.new_page(); e = []
        p.on('pageerror', lambda x, e=e: e.append(str(x)[:120]))
        p.goto('file://' + str(D / f)); p.wait_for_timeout(2200)
        dit(not e, f, e[0] if e else '')
        p.close()

    print('\n5. Les gestes qui comptent')
    A = c.new_page(); ea = []
    A.on('pageerror', lambda x: ea.append(str(x)[:120]))
    A.goto('file://' + str(D / 'catalogue.html')); A.wait_for_timeout(2400)
    A.evaluate("()=>{window.confirm=()=>true;}")
    dit(A.inner_text('#sfu').startswith('Sam'), 'la barre de gauche montre qui est connecté',
        A.inner_text('#sfu').replace('\n', ' · '))

    # saisie dans la fiche, caractère par caractère
    A.evaluate("b=>{const i=cur.findIndex(x=>x.bc===b);ouvreFiche(cur[i].id);}", '8011003809219')
    A.wait_for_timeout(500)
    q0 = A.evaluate("()=>cur[FICHE.pos].qte")
    A.click('[data-k="pa"]'); A.keyboard.press('Control+a')
    A.type('[data-k="pa"]', '52.75', delay=60); A.wait_for_timeout(500)
    dit(A.input_value('[data-k="pa"]') == '52.75', 'les cases de la fiche acceptent la frappe')

    # ajustement de stock
    A.click('[data-ajust]'); A.wait_for_timeout(400)
    A.click('#ajmot label[data-m="casse"]')
    A.fill('#aj-n', '5'); A.dispatch_event('#aj-n', 'input'); A.wait_for_timeout(300)
    A.click('#ajok'); A.wait_for_timeout(700)
    dit(A.evaluate("()=>cur[FICHE.pos].qte") == q0 - 5, 'ajuster le stock retire bien les flacons')
    j = A.evaluate("()=>JSON.parse(localStorage.getItem('crm-journal-v1')).slice(-1)[0]")
    dit(j.get('u') == 'Sam' and j.get('t'), 'l\'ajustement est signé et daté', str(j.get('u')))

    # vente puis remboursement
    V = c.new_page(); ev = []
    V.on('pageerror', lambda x: ev.append(str(x)[:120]))
    V.goto('file://' + str(D / 'ventes.html')); V.wait_for_timeout(2200)
    cle = 'b8011003809219'
    V.click('#nv'); V.wait_for_timeout(500)
    V.evaluate("""c=>{ $('v-canal').value='Amazon'; $('v-canal').dispatchEvent(new Event('change'));
      PANIER=[{cle:c,q:4,p:118.25}]; peintPanier(); }""", cle)
    V.wait_for_timeout(400)
    # le client : trouvé dans le carnet, ou créé à la volée
    V.fill('#v-client', 'jav'); V.wait_for_timeout(300)
    sug = V.locator('#v-cres div').all_inner_texts()
    dit(any(x.startswith('Javier') for x in sug) and 'gros' in ' '.join(sug),
        'le champ client propose Javier (wholesale) dès trois lettres', ' | '.join(sug)[:70])
    V.keyboard.press('ArrowDown'); V.keyboard.press('Enter'); V.wait_for_timeout(200)
    dit(V.input_value('#v-client') == 'Javier' and V.evaluate("()=>document.activeElement.id") == 'v-q',
        'Entrée choisit le client et passe au parfum')
    V.fill('#v-client', 'Carlos Nuevo'); V.wait_for_timeout(300)
    dit(any('Nouveau client' in x for x in V.locator('#v-cres div').all_inner_texts()),
        'un nom inconnu propose « Nouveau client »')
    V.keyboard.press('Enter'); V.wait_for_timeout(200)
    qav = V.evaluate("c=>qteEff(c)", cle)
    V.click('#v-ok'); V.wait_for_timeout(1200)
    dit(V.evaluate("c=>qteEff(c)", cle) == qav - 4, 'une vente sort les flacons du stock')
    rl = V.evaluate("()=>JSON.parse(localStorage.getItem('retail-local-v1')||'[]').map(c=>c.nom)")
    dit('Carlos Nuevo' in rl, 'le nouveau client est entré dans Retail avec la vente', str(rl)[:60])
    dit(not ev, 'ventes.html tient après une vente', ev[0] if ev else '')
    V.reload(); V.wait_for_timeout(2400)
    dit(V.locator('#corps tbody tr').count() > 0, 'la vente est encore là après rechargement')
    V.locator('#corps tbody tr[data-d]').first.click(); V.wait_for_timeout(600)
    dit(V.locator('#d-ret').count() > 0, 'le bouton Rembourser est disponible (dans la fiche de la vente)')
    V.click('#d-ret'); V.wait_for_timeout(800)
    dit(V.is_visible('#retov'), 'la fenêtre de remboursement s\'ouvre')

    # sauvegarde : le compteur voit le travail en attente, le fichier part, le compteur retombe
    A.evaluate("()=>localStorage.removeItem('derniere-sauvegarde-compte-v1')")
    n_att = A.evaluate("()=>svSaisies()")
    dit(n_att >= 5, 'le compteur voit le travail non sauvegardé', str(n_att) + ' modifications')
    A.evaluate("()=>svTemoin()"); A.wait_for_timeout(300)
    dit(A.locator('#svtem').count() > 0, 'le témoin de sauvegarde s\'affiche')
    with A.expect_download(timeout=9000) as di:
        A.evaluate("()=>svTelecharge(false)")
    p = json.load(open(di.value.path()))
    dit(p.get('format') == 'crm-parfums-sauvegarde' and len(p.get('donnees', {})) >= 8,
        'la sauvegarde contient bien les données', str(len(p.get('donnees', {}))) + ' clés')
    dit(A.evaluate("()=>svSaisies()") == 0, 'le compteur retombe à zéro après la sauvegarde')

    # les accès et les rôles
    G = c.new_page(); eg = []
    G.on('pageerror', lambda x: eg.append(str(x)[:120]))
    G.goto('file://' + str(D / 'acces.html')); G.wait_for_timeout(2200)
    nCpt = G.evaluate("comptes().length")
    dit(G.locator('#tb tr').count() == nCpt and nCpt >= 4,
        'la page Accès liste tous les comptes',
        str(G.locator('#tb tr').count()) + ' lignes pour ' + str(nCpt) + ' comptes')
    dit(G.locator('#finidemo').count() == 1, 'la page Accès prévient que les comptes de démonstration sont ouverts')
    nRoles = G.evaluate("Object.keys(ROLES).length")
    dit(len(G.locator('.dr thead th').all()) == nRoles + 1 and nRoles >= 5,
        'tous les rôles sont décrits, Admin compris',
        str(len(G.locator('.dr thead th').all()) - 1) + ' colonnes pour ' + str(nRoles) + ' rôles')
    dit(G.evaluate("!!ROLES.admin && !!ROLES.admin.technique && !ROLES.patron.technique"),
        'Admin a le droit technique, le Patron ne l\'a pas')
    G.click('#add'); G.wait_for_timeout(500)
    G.fill('#f-nom', 'Test Entrepôt'); G.fill('#f-id', 'test.ent')
    G.select_option('#f-role', 'entrepot')
    G.fill('#f-m', 'entrepot99'); G.fill('#f-m2', 'entrepot99')
    G.click('#fok'); G.wait_for_timeout(900)
    dit(G.locator('#tb tr').count() == nCpt + 1, 'un accès de plus a été ouvert',
        str(G.locator('#tb tr').count()) + ' lignes')

    # un rôle fabriqué par le patron : nom, droits cochés, page de départ
    G.click('#addr'); G.wait_for_timeout(500)
    G.fill('#r-lib', 'Boutique Perfume City')
    G.fill('#r-aide', 'Compte le stock de la boutique et vend au comptoir')
    G.check('#r-cases input[data-d="vendre"]')
    G.check('#r-cases input[data-d="compter"]')
    G.select_option('#r-dep', 'stock.html')
    G.click('#rok'); G.wait_for_timeout(700)
    dit(len(G.locator('.dr thead th').all()) == nRoles + 2,
        'un rôle fabriqué à la main s\'ajoute aux rôles d\'origine',
        str(len(G.locator('.dr thead th').all()) - 1) + ' rôles')
    dit('Boutique Perfume City' in G.locator('.dr thead th').last.inner_text(),
        'le rôle garde son nom')
    dit(G.locator('.dr tr.dep td').last.inner_text().strip() == 'Inventaire',
        'et sa page de départ', G.locator('.dr tr.dep td').last.inner_text())
    G.click('#addr'); G.wait_for_timeout(400)
    G.fill('#r-lib', 'Rien du tout'); G.click('#rok'); G.wait_for_timeout(400)
    dit('au moins un droit' in G.locator('#rmsg').inner_text(),
        'un rôle sans aucun droit est refusé')
    G.click('#rc'); G.wait_for_timeout(300)
    G.click('#add'); G.wait_for_timeout(500)
    dit('Boutique Perfume City' in G.locator('#f-role option').all_inner_texts(),
        'le rôle fabriqué est proposé en ouvrant un accès')
    G.fill('#f-nom', 'Test Boutique'); G.fill('#f-id', 'test.pc')
    G.select_option('#f-role', label='Boutique Perfume City')
    G.fill('#f-m', 'boutique99'); G.fill('#f-m2', 'boutique99')
    G.click('#fok'); G.wait_for_timeout(900)
    dit(G.locator('#tb tr').count() == nCpt + 2, 'un compte prend ce rôle',
        str(G.locator('#tb tr').count()) + ' lignes')
    G.once('dialog', lambda d: d.accept())
    G.click('.dr tr.fin button[data-rsup]'); G.wait_for_timeout(600)
    dit(len(G.locator('.dr thead th').all()) == nRoles + 2,
        'un rôle utilisé par quelqu\'un ne peut pas être supprimé',
        str(len(G.locator('.dr thead th').all()) - 1) + ' rôles restants')
    dit(not eg, 'acces.html sans erreur', eg[0] if eg else '')

    # la personne entre avec son rôle fabriqué : ses droits sont les bons
    PC = "{id:'test.pc',nom:'Test Boutique',role:'boutique-perfume-city',depuis:new Date().toISOString()}"
    G.evaluate("()=>{ localStorage.setItem('sam-session-v1',JSON.stringify(%s)); }" % PC)
    R = c.new_page(); er = []
    R.on('pageerror', lambda x: er.append(str(x)[:120]))
    R.goto('file://' + str(D / 'stock.html')); R.wait_for_timeout(2400)
    dit(R.evaluate("()=>peut('compter') && peut('vendre')"),
        'le rôle fabriqué donne bien les droits cochés')
    dit(R.evaluate("()=>!peut('voirPA') && !peut('acces')"),
        'et refuse ceux qui ne le sont pas')
    dit(R.evaluate("()=>pageDeDepart(session().role)") == 'stock.html',
        'il arrive sur la page choisie')
    R.goto('file://' + str(D / 'acces.html')); R.wait_for_timeout(2000)
    dit(R.locator('.mur').count() == 1, 'et reste devant le mur de la page Accès')
    dit(not er, 'un rôle fabriqué ne casse aucune page', er[0] if er else '')
    G.evaluate("()=>{ const P=rolesPerso(); delete P['boutique-perfume-city']; sauveRoles(P); }")

    SESS = "()=>{ localStorage.setItem('sam-session-v1',JSON.stringify(%s)); }"
    ENT = "{id:'test.ent',nom:'Test Entrepôt',role:'entrepot',depuis:new Date().toISOString()}"
    PAT = "{id:'sam',nom:'Sam',role:'patron',depuis:new Date().toISOString()}"
    G.evaluate(SESS % ENT)
    E = c.new_page(); E.goto('file://' + str(D / 'catalogue.html')); E.wait_for_timeout(2400)
    dit(E.evaluate("()=>document.body.classList.contains('sansPA')"),
        'le rôle Entrepôt n\'a pas accès aux prix d\'achat')
    E.goto('file://' + str(D / 'acces.html')); E.wait_for_timeout(1800)
    dit(E.locator('.mur').count() == 1, 'le rôle Entrepôt est refusé sur la page Accès')
    E.goto('file://' + str(D / 'tableau.html')); E.wait_for_timeout(1800)
    dit(E.locator('.mur').count() == 1, 'le rôle Entrepôt est refusé sur le Tableau de bord')
    dit('$' not in E.inner_text('.wrap'), 'aucun montant n\'apparaît sur le Tableau de bord fermé')
    E.close()
    G.evaluate(SESS % PAT); G.close()

    # les deux inventaires, et l'import de fichier
    I = c.new_page(); ei = []
    I.on('pageerror', lambda x: ei.append(str(x)[:120]))
    I.goto('file://' + str(D / 'inventaire_pc.html')); I.wait_for_timeout(2400)
    dit(I.evaluate("()=>P.length") == 0, 'Perfume City part d\'un inventaire vide',
        str(I.evaluate("()=>P.length")) + ' lignes')
    dit(I.evaluate("()=>KEY") == 'comptage-pc-v1', 'Perfume City a sa propre saisie', I.evaluate("()=>KEY"))
    I.click('#majf'); I.wait_for_timeout(600)
    I.fill('#imptxt', 'Code-barres;Nom;Marque;Quantite;Prix achat\n'
                      '8011003809219;Eros;Versace;12;46,50\n'
                      '3700559605417;Baccarat Rouge 540;MFK;3;420')
    I.wait_for_timeout(900)
    dit('2 lignes lues' in I.inner_text('#impres'), 'le fichier est lu et montré avant de valider')
    I.click('#impok'); I.wait_for_timeout(2600)
    dit(I.evaluate("()=>P.length") == 2, 'l\'import remplit l\'inventaire de Perfume City',
        str(I.evaluate("()=>P.length")) + ' lignes')
    dit(I.locator('#impban').is_visible(), 'un bandeau dit que l\'inventaire vient d\'un fichier')
    dit(not ei, 'inventaire_pc.html sans erreur', ei[0] if ei else '')
    S2 = c.new_page(); S2.goto('file://' + str(D / 'stock.html')); S2.wait_for_timeout(2400)
    dit(S2.evaluate("()=>P.length") > 3000, 'l\'entrepôt n\'a pas bougé',
        str(S2.evaluate("()=>P.length")) + ' lignes')
    dit(S2.evaluate("()=>KEY") == 'comptage-parfums-v1', 'les deux saisies restent séparées')
    S2.close(); I.close()

    # les trois langues
    A.evaluate("()=>document.querySelectorAll('.ov.on,.dov.on').forEach(o=>o.classList.remove('on'))")
    A.wait_for_timeout(300)
    prod0 = A.eval_on_selector_all('.card .nm, .card .mq', 'l=>l.slice(0,4).map(x=>x.textContent.trim())')
    dit(A.locator('#lgsel button').count() == 3, 'le choix de langue est proposé (FR / EN / ES)')
    A.click('#lgsel button[data-l="en"]'); A.wait_for_timeout(1100)
    dit('Catalog' in A.eval_on_selector('.side nav a.nv', 'a=>a.textContent'), 'l\'écran passe en anglais')
    A.click('#lgsel button[data-l="es"]'); A.wait_for_timeout(1100)
    dit('Catálogo' in A.eval_on_selector('.side nav a.nv', 'a=>a.textContent'),
        'de l\'anglais à l\'espagnol, sans repasser par le français')
    prES = A.eval_on_selector_all('.card .nm, .card .mq', 'l=>l.slice(0,4).map(x=>x.textContent.trim())')
    dit(prES == prod0, 'les noms de parfums ne sont jamais traduits', ' · '.join(prES[:2]))
    B2 = c.new_page(); B2.goto('file://' + str(D / 'ventes.html')); B2.wait_for_timeout(2400)
    dit('Catálogo' in B2.eval_on_selector('.side nav a.nv', 'a=>a.textContent'),
        'la langue choisie suit sur les autres rubriques')
    B2.close()
    A.click('#lgsel button[data-l="fr"]'); A.wait_for_timeout(1000)
    dit('Catalogue' in A.eval_on_selector('.side nav a.nv', 'a=>a.textContent'), 'le retour au français est complet')

    # le menu de gauche, renommé et réordonné
    A.evaluate("()=>document.querySelectorAll('.ov.on,.dov.on').forEach(o=>o.classList.remove('on'))")
    A.wait_for_timeout(300)
    n0 = A.locator('.side nav a.nv').count()
    dit(A.locator('#mn-btn').count() == 1, 'le bouton « Modifier le menu » est là')
    A.click('#mn-btn'); A.wait_for_timeout(600)
    dit(A.locator('#mn-liste input[data-i]').count() == n0, 'la fenêtre liste toutes les rubriques',
        str(n0) + ' rubriques')
    # la ligne de l'Inventaire, quelle que soit sa position dans la fenêtre
    iv = A.eval_on_selector_all('#mn-liste input[data-i]',
        'l=>{const x=l.find(e=>e.value.trim()==="Inventaire"); return x?x.dataset.i:null;}')
    A.fill('#mn-liste input[data-i="%s"]' % iv, 'Mon stock')
    for _ in range(int(iv)):
        A.click('#mn-liste [data-h]:not([disabled])' if False else '#mn-liste [data-h="%d"]' % int(iv))
        A.wait_for_timeout(160)
        iv = A.eval_on_selector_all('#mn-liste input[data-i]',
            'l=>{const x=l.find(e=>e.value.trim()==="Mon stock"); return x?x.dataset.i:null;}')
        if iv is None or int(iv) == 0:
            break
    A.click('#mn-ok'); A.wait_for_timeout(2600)
    prem = A.eval_on_selector('.side nav a.nv', 'a=>a.textContent')
    dit('Mon stock' in prem, 'la rubrique est renommée et remontée en tête', prem.strip())
    dit(A.eval_on_selector('.side nav a.nv',
        'a=>a.getAttribute("href").split("?")[0]') == 'stock.html',
        'le lien de la rubrique renommée marche toujours')
    dit(A.locator('.side nav a.nv').count() == n0, 'aucune rubrique perdue au passage')
    href = A.eval_on_selector('.side nav a.nv', 'a=>a.getAttribute("href")')
    dit('?v=' in href, 'chaque lien porte le numéro de version — le navigateur ne peut plus '
        'servir une vieille page', href)
    M = c.new_page(); M.goto('file://' + str(D / 'ventes.html')); M.wait_for_timeout(2400)
    dit('Mon stock' in M.eval_on_selector('.side nav a.nv', 'a=>a.textContent'),
        'le menu réglé se retrouve sur les autres pages')
    M.close()
    A.click('#mn-btn'); A.wait_for_timeout(600)
    A.click('#mn-raz'); A.wait_for_timeout(2600)
    dit('Catalogue' in A.eval_on_selector('.side nav a.nv', 'a=>a.textContent'),
        'le menu revient par défaut quand on le demande')

    # retirer une rubrique du menu
    A.click('#mn-btn'); A.wait_for_timeout(600)
    lib = A.eval_on_selector('#mn-liste input[data-i]', 'x=>x.value')
    i0 = A.eval_on_selector('#mn-liste input[data-i]', 'x=>x.dataset.i')
    A.uncheck('#mn-liste input[data-v="%s"]' % i0); A.wait_for_timeout(300)
    A.click('#mn-ok'); A.wait_for_timeout(2600)
    vis = A.eval_on_selector_all('.side nav a.nv',
        'l=>l.filter(a=>getComputedStyle(a).display!=="none").length')
    dit(vis == n0 - 1, 'une rubrique décochée disparaît du menu',
        '« ' + lib +' » retirée, ' + str(vis) + ' visibles sur ' + str(n0))
    A.click('#mn-btn'); A.wait_for_timeout(600)
    A.click('#mn-raz'); A.wait_for_timeout(2600)
    vis = A.eval_on_selector_all('.side nav a.nv',
        'l=>l.filter(a=>getComputedStyle(a).display!=="none").length')
    dit(vis == n0, 'elle revient avec « Tout remettre comme avant »', str(vis) + ' visibles')

    # ajouter un titre de section
    A.click('#mn-btn'); A.wait_for_timeout(600)
    dej = A.locator('#mn-liste input[data-x]').count()
    dit(dej >= 3, 'les titres déjà présents sont repris dans la fenêtre', str(dej) + ' titres')
    A.click('#mn-titre'); A.wait_for_timeout(400)
    A.fill('#mn-liste input[data-x]', 'Ma boutique'); A.wait_for_timeout(300)
    # on le descend jusqu'à ce qu'une rubrique le suive
    for k in range(4):
        A.click('#mn-liste [data-b="%d"]' % k); A.wait_for_timeout(200)
    A.click('#mn-ok'); A.wait_for_timeout(2600)
    titres = A.eval_on_selector_all('.side nav .navlab',
        'l=>l.filter(e=>getComputedStyle(e).display!=="none").map(e=>e.textContent.trim())')
    dit('Ma boutique' in titres, 'un titre ajouté apparaît dans le menu', ' · '.join(titres))
    B3 = c.new_page(); B3.goto('file://' + str(D / 'ventes.html')); B3.wait_for_timeout(2400)
    t2 = B3.eval_on_selector_all('.side nav .navlab',
        'l=>l.filter(e=>getComputedStyle(e).display!=="none").map(e=>e.textContent.trim())')
    dit('Ma boutique' in t2, 'le titre ajouté suit sur les autres rubriques')
    B3.close()
    A.click('#mn-btn'); A.wait_for_timeout(600)
    A.click('#mn-raz'); A.wait_for_timeout(2600)
    t3 = A.eval_on_selector_all('.side nav .navlab',
        'l=>l.filter(e=>getComputedStyle(e).display!=="none").map(e=>e.textContent.trim())')
    dit('Ma boutique' not in t3, 'le titre disparaît avec « Tout remettre comme avant »', ' · '.join(t3))

    # deux onglets
    B = c.new_page(); B.goto('file://' + str(D / 'catalogue.html')); B.wait_for_timeout(2300)
    k1, k2 = A.evaluate("()=>[cur[0].id,cur[1].id]")
    A.evaluate("c=>{ MOD[c]=Object.assign({},MOD[c]||{},{pvr:777}); sauveMOD(); }", k1)
    A.wait_for_timeout(300)
    B.evaluate("c=>{ MOD[c]=Object.assign({},MOD[c]||{},{pvw:888}); sauveMOD(); }", k2)
    B.wait_for_timeout(400)
    m = B.evaluate("()=>JSON.parse(localStorage.getItem('fiches-modifiees-v1'))")
    dit((m.get(k1) or {}).get('pvr') == 777 and (m.get(k2) or {}).get('pvw') == 888,
        'deux onglets ne s\'effacent plus l\'un l\'autre')

    dit(not ea, 'aucune erreur dans le catalogue pendant tout le parcours', ea[0] if ea else '')

    # la rubrique Retail et le bouton « Écrire », partout où il y a quelqu'un
    T = c.new_page(); et = []
    T.on('pageerror', lambda x: et.append(str(x)[:120]))
    T.goto('file://' + str(D / 'retail.html')); T.wait_for_timeout(1200)
    # la vente de tout à l'heure y a mis « Carlos Nuevo » : on repart du fichier d'origine
    T.evaluate("()=>localStorage.removeItem('retail-local-v1')"); T.reload(); T.wait_for_timeout(2400)
    dit(T.locator('.rien h3').count() == 1, 'Retail part vide et explique pourquoi',
        T.locator('.rien h3').inner_text() if T.locator('.rien h3').count() else '')
    CSV = ("name,email,phone,city,orders,total spent,last order\n"
           "Maria Lopez,maria@example.com,+1 305 555 0142,Miami,4,318.50,2026-08-28\n"
           "John Diaz,john.diaz@example.com,3055550199,Hialeah,1,72.00,2026-07-02\n"
           "Sofia Ruiz,sofia@example.com,,Doral,9,1204.90,2026-09-01\n")
    T.click('#imp'); T.wait_for_timeout(400)
    T.fill('#imptxt', CSV); T.wait_for_timeout(600)
    dit('3 clients lus' in T.locator('#impres .hint').inner_text(),
        'le fichier est lu et montré avant de valider')
    T.click('#impok'); T.wait_for_timeout(900)
    dit(T.locator('.t tbody tr').count() == 3, 'les clients importés remplissent la liste',
        str(T.locator('.t tbody tr').count()) + ' lignes')
    dit(not T.eval_on_selector('#impban', 'e=>e.hidden'), 'un bandeau dit que la liste vient d\'un fichier')
    T.click('#v-vig'); T.wait_for_timeout(600)
    dit(T.locator('.cv').count() == 3, 'la même liste passe en vignettes')
    T.reload(); T.wait_for_timeout(2400)
    dit(T.locator('.cv').count() == 3, 'l\'affichage choisi est retrouvé au retour')
    T.click('#v-liste'); T.wait_for_timeout(500)
    T.fill('#q', 'doral'); T.wait_for_timeout(500)
    dit(T.locator('.t tbody tr').count() == 1, 'la recherche filtre sur la ville')
    T.fill('#q', ''); T.wait_for_timeout(400)

    # écrire à quelqu'un : la fenêtre partagée
    T.click('.t tbody tr:first-child button[data-e]'); T.wait_for_timeout(700)
    dit(T.locator('#ctov.on').count() == 1, 'la fenêtre « Écrire » s\'ouvre depuis une fiche')
    dit(T.input_value('#ct-mail') == 'sofia@example.com', 'avec l\'email de la personne',
        T.input_value('#ct-mail'))
    dit(T.input_value('#ct-obj') == 'Une offre pour vous', 'et un message de promotion tout prêt')
    T.click('#ct-choix button[data-m="relance"]'); T.wait_for_timeout(400)
    dit(T.input_value('#ct-obj') == 'Votre facture', 'le modèle de relance remplace le texte')
    T.fill('#ct-tel', '12'); T.click('#ct-wa'); T.wait_for_timeout(400)
    dit('pas lisible' in T.locator('#ct-msg').inner_text(),
        'un numéro WhatsApp illisible est refusé')
    T.fill('#ct-tel', '305 555 0177'); T.click('#ct-wa'); T.wait_for_timeout(500)
    dit('WhatsApp' in T.locator('#ct-msg').inner_text(), 'un numéro correct ouvre WhatsApp')
    T.fill('#ct-mail', 'pas-une-adresse'); T.click('#ct-em'); T.wait_for_timeout(400)
    dit('valable' in T.locator('#ct-msg').inner_text(), 'une adresse email invalide est refusée')
    T.fill('#ct-mail', 'sofia.ruiz@example.com'); T.click('#ct-em'); T.wait_for_timeout(600)
    T.click('#ct-non'); T.wait_for_timeout(400)
    T.reload(); T.wait_for_timeout(2400)
    T.click('.t tbody tr:first-child button[data-e]'); T.wait_for_timeout(700)
    dit(T.input_value('#ct-mail') == 'sofia.ruiz@example.com',
        'l\'email corrigé est recollé sur la fiche', T.input_value('#ct-mail'))
    T.click('#ct-non')
    j = T.evaluate("()=>JSON.parse(localStorage.getItem('crm-journal-v1')||'[]').filter(x=>x.act==='contact')")
    dit(len(j) >= 1, 'le journal garde trace des messages préparés', str(len(j)) + ' entrées')
    dit(not et, 'retail.html sans erreur', et[0] if et else '')

    # la signature et la messagerie choisies dans Réglages
    G2 = c.new_page(); eg2 = []
    G2.on('pageerror', lambda x: eg2.append(str(x)[:120]))
    G2.goto('file://' + str(D / 'reglages.html')); G2.wait_for_timeout(2400)
    G2.fill('#r-sign', 'Sam — Perfumes Trade')
    G2.fill('#r-mail', 'sam@perfumestrade.com')
    G2.fill('#r-tel', '+1 305 555 0100')
    G2.select_option('#r-boite', 'gmail'); G2.wait_for_timeout(1400)
    r = G2.evaluate("()=>JSON.parse(localStorage.getItem('reglages-v1'))")
    dit(r.get('signature') == 'Sam — Perfumes Trade' and r.get('boite') == 'gmail',
        'la signature et le choix de messagerie s\'enregistrent')
    dit(not eg2, 'reglages.html sans erreur', eg2[0] if eg2 else '')

    # un vrai fichier Excel, lu directement par la page
    XL = str(D / '_essai_import.xlsx')
    fabrique_xlsx(XL)
    X = c.new_page(); ex = []
    X.on('pageerror', lambda x: ex.append(str(x)[:120]))
    X.goto('file://' + str(D / 'stock.html')); X.wait_for_timeout(2600)
    for s_ in ('#dov', '#svtem'):
        try: X.eval_on_selector(s_, 'e=>e.remove()')
        except Exception: pass
    X.click('#majf'); X.wait_for_timeout(600)
    X.set_input_files('#impfile', XL); X.wait_for_timeout(2600)
    dit(not X.eval_on_selector('#imponglets', 'e=>e.hidden'),
        'un classeur à plusieurs onglets les propose au choix')
    ong = X.locator('#imponglets button').all_inner_texts()
    dit(any('Inventaire' in o for o in ong) and any('Perfume City' in o for o in ong),
        'les onglets portent leur vrai nom', ' · '.join(ong))
    ap = X.locator('#impres').inner_text()
    dit('2 lignes lues' in ap, 'les lignes du fichier Excel sont lues', ap.split('\n')[-1][:70])
    dit('Club de Nuit Intense' in ap and 'Armaf' in ap,
        'les textes mis en commun par Excel sont bien retrouvés')
    dit('18,50' in ap.replace('.', ','), 'et le prix d\'achat sous son titre anglais « Supplier price »')
    dit(not X.eval_on_selector('#impok', 'e=>e.disabled'), 'le fichier Excel est acceptable tel quel')
    X.locator('#imponglets button[data-o="1"]').click(); X.wait_for_timeout(900)
    dit('1 ligne lue' in X.locator('#impres').inner_text(),
        'changer d\'onglet relit le bon tableau')
    dit(not ex, 'la lecture du .xlsx ne casse rien', ex[0] if ex else '')
    # la feuille de comptage se trie par colonne
    X.click('#impx'); X.wait_for_timeout(300)
    capi = "()=>[...document.querySelectorAll('#tb tr td:nth-child(8)')].slice(0,40).map(t=>+t.textContent.replace(/[^0-9]/g,''))"
    X.click('th[data-tri="cap"]'); X.wait_for_timeout(700)
    v = X.evaluate(capi)
    dit(v == sorted(v), 'un clic sur Capital trie croissant', str(v[:4]))
    X.click('th[data-tri="cap"]'); X.wait_for_timeout(700)
    v = X.evaluate(capi)
    dit(v == sorted(v, reverse=True), 'un second clic trie décroissant', str(v[:3]))
    dit(X.eval_on_selector('th[data-tri="cap"]', 'e=>e.classList.contains("tri-desc")'),
        'la flèche montre le sens du tri')
    X.reload(); X.wait_for_timeout(2400)
    dit(X.eval_on_selector('th[data-tri="cap"]', 'e=>e.classList.contains("tri-desc")'),
        'le tri est retenu après rechargement')
    X.click('th[data-tri="cap"]'); X.wait_for_timeout(500)
    dit(not X.eval_on_selector('th[data-tri="cap"]', 'e=>e.className.includes("tri-")'),
        'un troisième clic remet l\'ordre du fichier')
    # Perfume City : les prix de vente du fichier apparaissent, l'entrepôt reste sans
    XP = c.new_page(); XP.goto('file://' + str(D / 'inventaire_pc.html')); XP.wait_for_timeout(2400)
    for s_ in ('#dov', '#svtem'):
        try: XP.eval_on_selector(s_, 'e=>e.remove()')
        except Exception: pass
    dit(XP.eval_on_selector('th.pv', 'e=>e.hidden'), 'sans fichier, pas de colonnes de prix de vente')
    XP.click('#majf'); XP.wait_for_timeout(500)
    XP.evaluate("""()=>{ $('imptxt').value='Name;Brand;Qty;Supplier price;pvr;pvw\\nAsad;Lattafa;3;12;29.9;19';
      $('imptxt').dispatchEvent(new Event('input')); }"""); XP.wait_for_timeout(900)
    XP.click('#impok'); XP.wait_for_timeout(2600)
    for s_ in ('#dov', '#svtem'):
        try: XP.eval_on_selector(s_, 'e=>e.remove()')
        except Exception: pass
    dit(not XP.eval_on_selector('th.pv', 'e=>e.hidden'), 'avec un fichier qui en porte, PV détail et PV gros s\'affichent')
    cel = XP.locator('#tb tr').first.locator('td').all_inner_texts()
    dit(any('29,90' in x for x in cel) and any('19,00' in x for x in cel),
        'les prix de vente sont ceux du fichier', ' · '.join(cel[-2:]))
    XP.on('dialog', lambda d: d.accept())      # deux questions de suite : oui aux deux
    XP.click('#raz'); XP.wait_for_timeout(2600)
    dit(XP.evaluate("()=>!!localStorage.getItem('pc-stock-v1') && !localStorage.getItem('inventaire-local-pc-v1')"),
        'Perfume City : l\'inventaire est un magasin partagé ; « Effacer la saisie » n\'efface que les comptages, pas le stock')
    XP.close()
    dit(X.locator('.ver').count() == 1 and 'version du' in X.locator('.ver').inner_text(),
        'la page affiche sa date de fabrication', X.locator('.ver').inner_text()
        if X.locator('.ver').count() else 'absente')
    dit(X.eval_on_selector('#impfile', 'e=>!e.getAttribute("accept")'),
        'aucun fichier n\'est grisé dans la fenêtre du Mac')
    # un .docx : le seul format qu'on refuse encore franchement (un PDF, meme faux,
    # se lit desormais — mais sur la version en ligne, pas depuis file://)
    faux = str(D / '_essai.docx')
    open(faux, 'wb').write(b'PK\x03\x04 rien du tout')
    X.set_input_files('#impfile', faux); X.wait_for_timeout(900)
    dit('ne se lit pas ici' in X.locator('#impres').inner_text(),
        'un fichier au mauvais format est refusé avec une explication')
    try: os.remove(faux)
    except Exception: pass

    # la même chose côté Retail, où les dates comptent
    XR = c.new_page(); exr = []
    XR.on('pageerror', lambda x: exr.append(str(x)[:120]))
    XR.goto('file://' + str(D / 'retail.html')); XR.wait_for_timeout(2400)
    XR.click('#imp'); XR.wait_for_timeout(500)
    XR.set_input_files('#impfile', XL); XR.wait_for_timeout(2600)
    apr = XR.locator('#impres').inner_text()
    dit('2026-08-28' in apr,
        'une date Excel redevient une date, pas un nombre',
        ' / '.join(l for l in apr.split('\n') if '2026' in l)[:60])
    dit(not exr, 'retail.html lit aussi le .xlsx', exr[0] if exr else '')
    try: os.remove(XL)
    except Exception: pass
    T.reload(); T.wait_for_timeout(2400)
    T.click('.t tbody tr:first-child button[data-e]'); T.wait_for_timeout(700)
    txt = T.input_value('#ct-txt')
    dit('Sam — Perfumes Trade' in txt and 'sam@perfumestrade.com' in txt,
        'le message est signé du nom mis dans Réglages')
    dit(T.evaluate("()=>ctLienMail('a@b.com','O','C')").startswith('https://mail.google.com'),
        'et « Ouvrir l\'email » passe par Gmail comme demandé')
    dit('Gmail' in T.locator('#ct-note').inner_text(), 'la fenêtre le dit à l\'écran')
    T.click('#ct-non')

    # le même bouton chez les fournisseurs
    N = c.new_page(); en_ = []
    N.on('pageerror', lambda x: en_.append(str(x)[:120]))
    N.goto('file://' + str(D / 'fournisseurs.html')); N.wait_for_timeout(2600)
    dit(N.locator('button[data-ecr]').count() >= 1, 'les fournisseurs ont le même bouton Écrire')
    N.locator('button[data-ecr]').first.click(); N.wait_for_timeout(600)
    dit(N.locator('#ctov.on').count() == 1, 'et la même fenêtre')
    N.fill('#ct-mail', 'achats@mtz-test.com'); N.click('#ct-em'); N.wait_for_timeout(600)
    N.click('#ct-non'); N.reload(); N.wait_for_timeout(2600)
    N.locator('button[data-ecr]').first.click(); N.wait_for_timeout(600)
    dit(N.input_value('#ct-mail') == 'achats@mtz-test.com',
        'l\'email corrigé revient dans la fiche fournisseur')
    # la fiche détaillée et la création à la main
    N.evaluate("""()=>localStorage.setItem('prix-achat-hist-v1',JSON.stringify({
      'b8011003809219':[{f:'Miami Trading Zone',src:'facture',q:12,p:18.5,d:'2026-07-02',num:'T-1'},
                        {f:'Miami Trading Zone',src:'facture',q:24,p:17.9,d:'2026-09-01',num:'T-2'}]}))""")
    N.reload(); N.wait_for_timeout(2600)
    for s_ in ('#dov', '#svtem'):
        try: N.eval_on_selector(s_, 'e=>e.remove()')
        except Exception: pass
    N.locator('.fcard[data-fiche="Miami Trading Zone"]').click(); N.wait_for_timeout(700)
    dit(N.locator('#fdov.on').count() == 1, 'un clic sur un fournisseur ouvre sa fiche détaillée')
    dit(N.locator('#fdov .fac').count() == 2, 'la fiche liste ses factures, une par ligne', str(N.locator('#fdov .fac').count()))
    N.locator('#fdov .fac').first.click(); N.wait_for_timeout(300)
    dit(not N.eval_on_selector('#fdov .det', 'e=>e.hidden'), 'une facture se déplie sur ses lignes')
    ev = N.locator('#fdov #fd-prods tbody tr td:nth-child(7)').first.inner_text()
    dit('-0,60' in ev and '%' in ev, 'l\'évolution du prix d\'achat est calculée', ev)
    N.click('#fd-x'); N.wait_for_timeout(300)
    N.click('#nouv'); N.wait_for_timeout(400)
    N.fill('#fr-nom', 'Test Depot'); N.fill('#fr-email', 'x@test.com'); N.click('#fr-ok'); N.wait_for_timeout(600)
    dit(N.locator('.fcard[data-fiche="Test Depot"]').count() == 1, 'un fournisseur tapé à la main apparaît dans la liste')
    N.click('#nouv'); N.wait_for_timeout(300); N.fill('#fr-nom', 'test depot'); N.click('#fr-ok'); N.wait_for_timeout(300)
    dit('existe' in N.locator('#fr-msg').inner_text(), 'un doublon de nom est refusé'); N.click('#fr-non')
    dit(not en_, 'fournisseurs.html sans erreur', en_[0] if en_ else '')

    # la messagerie interne entre les comptes
    def sess(i, nom, r):
        return ("()=>localStorage.setItem('sam-session-v1',JSON.stringify("
                "{id:'%s',nom:'%s',role:'%s',depuis:new Date().toISOString()}))" % (i, nom, r))
    M = c.new_page(); em = []
    M.on('pageerror', lambda x: em.append(str(x)[:120]))
    M.goto('file://' + str(D / 'messages.html')); M.wait_for_timeout(2400)
    # un menu réglé avant l'arrivée des titres : ils restent modifiables quand même
    A2 = c.new_page(); A2.goto('file://' + str(D / 'ventes.html')); A2.wait_for_timeout(1200)
    A2.evaluate("()=>localStorage.setItem('menu-perso-v1',JSON.stringify({ordre:['ventes.html','catalogue.html','stock.html'],noms:{},caches:[]}))")
    A2.reload(); A2.wait_for_timeout(2400)
    for s_ in ('#dov', '#svtem'):
        try: A2.eval_on_selector(s_, 'e=>e.remove()')
        except Exception: pass
    A2.click('#mn-btn'); A2.wait_for_timeout(600)
    tt = A2.evaluate("()=>[...document.querySelectorAll('#mn-liste input[data-x]')].map(i=>i.value)")
    dit('Commerce' in tt and 'Produits' in tt,
        'un menu réglé sans titres retrouve Produits / Commerce / Pilotage dans la fenêtre', ' · '.join(tt[:4]))
    A2.locator('#mn-liste input[data-x]').first.fill('BOUTIQUE'); A2.click('#mn-ok'); A2.wait_for_timeout(2600)
    dit('BOUTIQUE' in A2.locator('.side nav .navlab:visible').all_inner_texts(),
        'et un titre renommé s\'affiche en tête de sa section')
    A2.evaluate("()=>localStorage.removeItem('menu-perso-v1')"); A2.close()

    dit(M.locator('#liste button').count() >= 3, 'la messagerie liste les autres comptes',
        str(M.locator('#liste button').count()) + ' personnes')
    M.locator('#liste button[data-u="ana"]').click(); M.wait_for_timeout(400)
    M.fill('#txt', 'Ana, recompte l\'étagère B avant ce soir.')
    M.click('#env'); M.wait_for_timeout(600)
    dit(M.locator('.bulle.moi').count() == 1, 'le message part et s\'affiche')
    dit(M.locator('.jourlab').count() == 1, 'daté par jour')

    M.evaluate(sess('ana', 'Ana', 'entrepot'))
    # avant d'ouvrir Messages, la pastille doit être visible depuis n'importe quelle page
    Pz = c.new_page(); Pz.goto('file://' + str(D / 'stock.html')); Pz.wait_for_timeout(2200)
    pz = Pz.evaluate("[document.getElementById('ct-messages')?1:0, document.getElementById('ct-support')?1:0, /Support technique/.test(document.querySelector('.side nav').innerText)?1:0].join('|')")
    dit(pz == '0|1|1', 'le menu n\'a plus la rubrique Messages : « Support technique » la remplace, même pour un rôle entrepôt (9 et 17 oct. 2026)', pz)
    Pz.close()
    M.reload(); M.wait_for_timeout(2400)
    dit(M.locator('#qui').inner_text() == 'Sam',
        'Ana arrive directement sur le fil qui l\'attend', M.locator('#qui').inner_text())
    dit(M.evaluate("()=>!document.getElementById('ct-messages')"),
        'et la page Messages (non liée au menu) marche toujours seule')
    dit('étagère B' in M.locator('.bulle.lui').inner_text(), 'et lit bien le message de Sam')
    M.fill('#txt', "C'est fait, 41 flacons."); M.click('#env'); M.wait_for_timeout(600)
    dit(M.locator('.bulle').count() == 2, 'elle répond dans le même fil')

    M.evaluate(sess('compta', 'Le comptable', 'comptable')); M.reload(); M.wait_for_timeout(2400)
    dit(M.locator('.bulle').count() == 0,
        'le comptable ne voit pas la conversation des autres', str(M.locator('.bulle').count()))
    dit(M.locator('#liste .pt:not(.z)').count() == 0, 'et n\'a aucun non-lu')

    M.evaluate(sess('sam', 'Sam', 'patron')); M.reload(); M.wait_for_timeout(2400)
    dit(M.locator('#qui').inner_text() == 'Ana',
        'Sam retombe sur le fil où on lui a répondu', M.locator('#qui').inner_text())
    dit(M.locator('.bulle').count() == 2, 'le fil garde les deux messages')
    dit('lu' in M.locator('.bulle.moi').first.inner_text(), 'son message est marqué lu')
    dit(M.locator('#liste .pt:not(.z)').count() == 0,
        'et le non-lu est retombé à zéro une fois affiché')
    j = M.evaluate("()=>JSON.parse(localStorage.getItem('crm-journal-v1')||'[]').filter(x=>x.act==='message')")
    dit(len(j) == 2, 'le journal garde les envois', str(len(j)) + ' entrées')
    dit(not em, 'messages.html sans erreur', em[0] if em else '')

    # le même menu sur toutes les pages — trois pages avaient leur copie à part,
    # et Messages, Retail et Accès y manquaient sans que rien ne le dise
    menus = {}
    for pg in ('catalogue', 'stock', 'inventaire_pc', 'clients', 'ventes', 'acces', 'retail', 'messages'):
        Q = c.new_page(); Q.goto('file://' + str(D / (pg + '.html'))); Q.wait_for_timeout(1500)
        menus[pg] = tuple(Q.evaluate(
            "()=>[...document.querySelectorAll('.side nav a.nv[href]')].map(a=>a.getAttribute('href').split('?')[0])"))
        Q.close()
    ref = menus['ventes']
    diff = [p for p, m in menus.items() if m != ref]
    dit(not diff, 'toutes les pages ont exactement le même menu',
        ('différent : ' + ', '.join(diff)) if diff else str(len(ref)) + ' rubriques partout')
    dit(all(x in ref for x in ('#support', 'clients.html', 'acces.html')) and 'messages.html' not in ref,
        'Support technique, Clients et Accès sont dans le menu de chaque page ; Messages n\'y est plus')

    # les chiffres du menu (1er oct. 2026) : calculés en direct, plus figés à la fabrication.
    # Inventaire = parfums EN STOCK pas encore vérifiés, le même sur toutes les pages.
    INV = json.loads(open(D / 'donnees' / 'inventaire.js').read().split('=', 1)[1].rstrip().rstrip(';'))
    att = sum(1 for r in INV if (r[5] or 0) > 0 and r[8] != 'ok')
    vus = {}
    cx = b.new_context()   # neuf : aucune donnée laissée par les contrôles précédents
    cx.add_init_script("try{localStorage.setItem('sheet-installe-2026-09-03','1');localStorage.setItem('sam-comptes-demo-v1','0');"
                       "localStorage.setItem('sam-comptes-v1',JSON.stringify([{ident:'sam',nom:'Sam',role:'patron',actif:true,h:'x'}]));"
                       "localStorage.setItem('sam-session-v1',JSON.stringify({id:'sam',nom:'Sam',role:'patron',depuis:new Date().toISOString()}))}catch(e){}")
    for pg in ('stock', 'catalogue', 'journal'):
        Q = cx.new_page(); Q.goto('file://' + str(D / (pg + '.html'))); Q.wait_for_timeout(2500)
        vus[pg] = Q.evaluate("()=>[(document.getElementById('ct-catalogue')||{}).textContent,(document.getElementById('ct-inventaire')||{}).textContent].map(t=>+String(t||'').replace(/\\D/g,''))")
        Q.close()
    cx.close()
    # nouvelles références pour Lightspeed : fichier d'import produits, le douteux à part (3 oct. 2026)
    cth = open(D / 'catalogue.html', encoding='utf-8').read()
    dit('id="lsnv"' in cth and 'function lsTrie' in cth and "donnees/caisse-produits-v1" in cth and "'items_on_special_order_Main_Outlet'" in cth,
        "Catalogue : fichier des nouvelles références pour Lightspeed (import produits), le douteux mis à part")
    # la quantité en stock, en grand en haut de la fiche (remarque de Sam, 3 oct. 2026)
    dit('id="dqte-in" data-k="qte"' in cth and '[CH[6]].map(champ)' not in cth,
        "Catalogue : la quantité en stock se tape dans le gros chiffre en haut de la fiche")
    # remarques de Sam du 2 oct. (3 oct. 2026) : remise caisse, chèque, prix vers les sites, employés sans marges
    vh3 = open(D / 'ventes.html', encoding='utf-8').read()
    dit('remiseCaisse' in vh3 and "cheque:'Chèque'" in vh3 and 'function vmg()' in vh3,
        "Ventes : remise de la caisse comptée, paiement par chèque, marges cachées aux employés")
    dit('function planPrixSites' in cth and 'id="pxsites"' in cth and 'function remplitMarques' in cth,
        "Catalogue : un nouveau prix se propose aux sites ; une marque créée apparaît dans le filtre")
    # Price list rapide : comparaison à la fiche seule, index des mots, lignes posées par paquets (3 oct. 2026)
    eth = open(D / 'etude.html', encoding='utf-8').read()
    dit('function mScoreCle' in eth and 'function mCandidats' in eth and 'const PREM=150' in eth,
        "Price list : un devis de 1 700 lignes s'ouvre en ~1 s au lieu de 7 s")
    # Price list refaite : onglets, quantité et prix modifiables dans la ligne, codes « 6.29E12 » lus (3 oct. 2026)
    eth2 = open(D / 'etude.html', encoding='utf-8').read()
    dit('function retouche' in eth2 and 'id="filt"' in eth2 and 'const sciBC' in eth2,
        "Price list : onglets, quantité et prix modifiables dans la ligne, codes-barres d'Excel lus")
    # Amazon « pending » : la vente au jour de la confirmation, la date de commande dite (3 oct. 2026)
    dit('fa.commande=v.commande' in vh3, "Amazon : une commande confirmée après vérification du paiement se range au jour de la confirmation")
    # Price list : onglet « Pas en stock chez nous » et bon de commande (4 oct. 2026)
    dit("'stk0'" in eth2 and 'function bcOuvre' in eth2 and 'id="bdc"' in eth2 and 'const bcOffre' in eth2,
        "Price list : onglet « Pas en stock chez nous », bon de commande (PDF, Excel, texte), contre-offre dite")
    # Price list : le fournisseur se devine (nom du fichier, document), pas d'archive sans lui, archive nommable (4 oct. 2026)
    dit('function devineFrn' in eth2 and 'function frnManque' in eth2 and 'data-rn=' in eth2,
        "Price list : le fournisseur se lit dans le nom du fichier ; une étude ne se garde plus sans fournisseur ; une archive sans nom se nomme")
    # Ventes : la période « depuis le début du mois », par défaut (4 oct. 2026)
    dit('<option value="mois" selected>' in vh3 and "p==='mois'" in vh3,
        "Ventes : le chiffre depuis le début du mois, par défaut, à côté des 7 et 30 jours")
    # Ventes : frais d'envoi sur la vente saisie, et une vente enregistrée se modifie (Sam, 6 oct. 2026)
    dit('id="v-port"' in vh3 and 'function ouvreModif' in vh3 and 'function peutModifierVente' in vh3 and "Frais d'envoi" in vh3,
        "Ventes : frais d'envoi ajoutés au total de la vente ; « Modifier la vente » sur une vente saisie à la main")
    # « NOBOX » à la suite du code-barres : fiche à part, nommée « … (NOBOX) » (Sam, 6 oct. 2026)
    pjs = open(D / 'donnees' / 'produits.js', encoding='utf-8').read()
    dit('function mentionBC' in vh3 and 'function parMention' in cth and '(NOBOX)' in pjs and "'M:'+M.mention" in cth,
        "Code-barres + NOBOX : la fiche sans boîte s'appelle « … (NOBOX) », jamais confondue avec la boîte (ventes, catalogue, Sheet)")
    # un code partagé par plusieurs fiches : une seule quantité par code vers les sites ; document hors du zoom (7 oct. 2026)
    dit('function qteSiteDe' in cth and 'function _ssQteSite' in cth and "['docov','mailov','waov','edov','encov']" in vh3 and 'size:letter' in vh3,
        "Sites : une quantité par code-barres partagé (boîte / NOBOX / tester) ; facture imprimée et PDF à l'échelle 1, page Letter")
    # pièces jointes du client : privées, lues avec la session (2 oct. 2026)
    chp = open(D / 'clients.html', encoding='utf-8').read()
    dit('function pjDepose' in chp and "/pieces/'" in chp and 'Bearer' in chp and 'pj-type' in chp,
        'Clients : joindre un resale certificate ou un passeport, lu avec la session (jamais public)')

    # 15 oct. 2026 (Clemencia, Safari d'un vieux Mac) : une seule instruction trop récente fait mourir TOUTE la page
    # sans un message — le bouton « Entrer » recharge la page et rien d'autre. On interdit ce qui casse Safari 13 à 16.3.
    import re as _re
    abimes = []
    for _f in sorted(D.glob('*.html')):
        if _f.name.startswith('_'): continue
        _h = _f.read_text(encoding='utf-8', errors='replace')
        if '<script' not in _h: continue
        for _n, _l in enumerate(_h.split('\n'), 1):
            if _re.search(r'\|\|=|&&=|\?\?=', _l) and 'script' not in _l[:20]:
                if _re.search(r'[A-Za-z_\])\]]\s*(\|\||&&|\?\?)=\s*[\[{(A-Za-z0-9_]', _l): abimes.append(f'{_f.name}:{_n} affectation logique (||= &&= ??=)')
            if _re.search(r'\(\?<[=!]', _l) and 'RegExp(' not in _l and 'L_=' not in _l:
                abimes.append(f'{_f.name}:{_n} regex avec lookbehind écrite en dur')
    dit(not abimes, "Aucune page n'utilise une instruction que les anciens Safari (avant la 16.4) ne lisent pas", '; '.join(abimes[:3]))

    # Statut shipping en veille (2 oct. 2026) : hors du menu, le stock sort à la vente
    fa = open(D / 'ventes.html', encoding='utf-8').read()
    dit('expeditions.html' not in ''.join(menus.get('ventes', ())) and 'const FA_EXP_VEILLE=!window.__EXP_ACTIF' in fa and 'faVeilleExp' in fa,
        'Statut shipping en veille : hors du menu, et les commandes sortent du stock à la vente')

    # le prix d'une ligne de vente : pastilles retail / gros, case libre (2 oct. 2026)
    vh2 = open(D / 'ventes.html', encoding='utf-8').read()
    dit('function puChips' in vh2 and 'data-pk' in vh2, 'Ventes : chaque ligne propose le prix retail et le prix de gros, la case reste libre')

    # la liste du client (photo d'un Excel) dans « Enregistrer une vente », code inconnu à confirmer (2 oct. 2026)
    vh2 = open(D / 'ventes.html', encoding='utf-8').read()
    dit("bl.id='v-liste'" in vh2 and "sur:conf?'bc':sur" in vh2, 'Ventes : importer une liste dans la vente ; un code-barres inconnu se confirme à la main')

    # les favoris mis sur un poste se voient tout de suite sur l'autre (2 oct. 2026)
    ch = open(D / 'clients.html', encoding='utf-8').read()
    dit('window.__rafraichir=clRafraichit' in ch and "'ck-maj'" in ch, 'Clients : la liste et l\'étoile se redessinent quand un autre poste écrit')

    # une cote Lightspeed se supprime dans l'ERP, après une seconde validation (2 oct. 2026)
    vh = open(D / 'ventes.html', encoding='utf-8').read()
    dit('data-la="sup"' in vh and 'Seconde validation' in vh and 'erp.supprime' in vh,
        'cotes Lightspeed : bouton Supprimer avec seconde validation, et la relève ne les ramène pas')

    # la fiche d'un parfum faux sur les sites propose de les remettre à notre quantité (1er oct. 2026)
    cx = b.new_context()
    cx.add_init_script("try{localStorage.setItem('sheet-installe-2026-09-03','1');localStorage.setItem('sam-comptes-demo-v1','0');"
                       "localStorage.setItem('sam-comptes-v1',JSON.stringify([{ident:'sam',nom:'Sam',role:'patron',actif:true,h:'x'}]));"
                       "localStorage.setItem('sam-session-v1',JSON.stringify({id:'sam',nom:'Sam',role:'patron',depuis:new Date().toISOString()}));"
                       "localStorage.setItem('ck-token','jeton')}catch(e){}")
    Q = cx.new_page(); Q.goto('file://' + str(D / 'catalogue.html')); Q.wait_for_timeout(2500)
    bs = Q.evaluate("""()=>{ const p=tousLesArticles().find(x=>x.bc&&/^\\d+$/.test(x.bc)); if(!p) return '';
      SITE[p.bc]={d:{id:1,q:(p.qte||0)+7,suivi:true},g:{id:2,q:p.qte||0,suivi:true}}; _SITE0=null;
      const h=blocStockSites(p); delete SITE[p.bc]; _SITE0=null; return h; }""")
    Q.close(); cx.close()
    dit('dsst faux' in bs and 'tape la quantité dans « Quantité en stock », puis Enregistrer' in bs,
        'fiche : un parfum faux sur un site le montre et dit comment le corriger', bs[:120])
    dit(re.search(r"if\(qteTapee&&!auto\)", open(D / 'catalogue.html', encoding='utf-8').read()) is not None,
        'fiche : la quantité retapée part aux sites à l\'enregistrement, même inchangée')

    dit(all(v == [len(INV), att] for v in vus.values()),
        'menu : Catalogue = toutes les fiches, Inventaire = en stock pas vérifiés, partout pareil',
        str(vus) + ' attendu ' + str([len(INV), att]))
    b.close()

print('\n' + '─' * 62)
if ko:
    print(f'{len(ko)} contrôle(s) en échec — NE PAS LIVRER')
    for k in ko:
        print('   · ' + k)
    sys.exit(1)
print(f'TOUT EST BON — {len(ok)} contrôles passés. Livraison possible.')
