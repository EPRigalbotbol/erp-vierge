# La rubrique Quotes : un devis client en trois gestes — le client, sa liste, l'envoi.
#
# Ce que Sam fait vraiment : il reçoit la liste d'un grossiste en WhatsApp, en Excel ou
# en photo, et doit renvoyer un prix. Ici on vérifie que chacune de ces entrées finit
# en devis enregistré, avec les bons parfums, les bonnes quantités, le prix de gros
# pré-rempli, et un texte prêt à partir par WhatsApp. Et que rien ne touche au stock.
import pathlib, subprocess, time, io, socket, base64, json
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw, ImageFont

D = pathlib.Path('/home/claude/catalogue')
ok = 0; ko = []
def check(n, c, i=''):
    global ok
    if c: ok += 1; print('  ok  ', n)
    else: ko.append(n); print('  KO  ', n, i)

CAT = json.load(open(D / 'cat.json'))
# deux références bien connues, avec leur code-barres
def ref(marque, nom):
    for r in CAT:
        if r[2] == marque and r[1] == nom and (r[6] or 0) > 0: return r
    raise SystemExit('référence introuvable ' + marque + ' ' + nom)
A = ref('Jean Paul Gaultier', 'Le Male Elixir Absolu 4.2'); B = ref('Chanel', 'Bleu edp 3.4')
BC_A, BC_B = A[0], B[0]
PVW_A = A[8]   # prix de gros

def port_libre():
    s = socket.socket(); s.bind(('127.0.0.1', 0)); p = s.getsockname()[1]; s.close(); return p
def photo(lignes):
    im = Image.new('RGB', (1000, 300), 'white'); d = ImageDraw.Draw(im)
    f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 38)
    for i, l in enumerate(lignes): d.text((40, 40 + i * 100), l, fill='black', font=f)
    b = io.BytesIO(); im.save(b, 'JPEG', quality=92); return b.getvalue()
DEPOSE = """async ([nom, type, b64]) => {
  const bin=atob(b64); const u=new Uint8Array(bin.length); for(let i=0;i<bin.length;i++) u[i]=bin.charCodeAt(i);
  await mFichier(new File([u], nom, {type})); return $('m-lect').textContent; }"""

port = port_libre()
srv = subprocess.Popen(['python3', '-m', 'http.server', str(port), '--bind', '127.0.0.1'], cwd=str(D),
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1.2)
try:
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1400, 'height': 1000}); err = []
        pg.on('pageerror', lambda e: err.append(str(e)))
        base = f'http://127.0.0.1:{port}/'
        pg.goto(base + 'accueil.html'); pg.wait_for_timeout(600)
        pg.evaluate("localStorage.setItem('cotes-erp-ouvert','1');localStorage.setItem('sam-session-v1', JSON.stringify({id:'sam',nom:'Sam',role:'patron',depuis:new Date().toISOString()}))")
        pg.evaluate("localStorage.setItem('clients-v1', JSON.stringify({'Carmen':{nom:'Carmen',tel:'+1 305 555 0100',email:'carmen@test.com'}}))")
        pg.goto(base + 'quotes.html'); pg.wait_for_timeout(2800)

        print('0. à l\'arrivée : deux gestes en haut, la fenêtre de la cote s\'ouvre à la demande')
        check('« + Nouvelle cote » est en haut, visible', pg.locator('#nv').is_visible() and 'Nouvelle cote' in pg.locator('#nv').inner_text(), pg.locator('#nv').inner_text())
        check('« Coller un message du client » est en haut, visible', pg.locator('#msgb').is_visible() and 'Coller un message' in pg.locator('#msgb').inner_text(), pg.locator('#msgb').inner_text())
        check('la fenêtre de la cote est fermée tant qu\'on ne la demande pas', not pg.locator('#vov').is_visible())
        check('les cotes faites dans l\'ERP sont visibles d\'emblée, sans repli', pg.locator('#docs').is_visible() and pg.locator('#lsc-erp-b').count() == 0)
        pg.click('#nv'); pg.wait_for_timeout(600)

        print('1. la page EST le devis : le client, les parfums, les prix — rien d\'autre')
        check('Cote est dans le menu, à sa place', 'Cote' in pg.locator('nav a.nv.on').inner_text())
        check('« + Nouvelle cote » ouvre la fenêtre de la cote', pg.locator('#vov').is_visible() and pg.locator('#v-q').is_visible())
        check('elle s\'appelle « Nouveau devis »', pg.locator('#vov .mh h3').inner_text() == 'Nouvelle cote', pg.locator('#vov .mh h3').inner_text())
        check('le journal des ventes n\'est pas là', not pg.locator('#corps').is_visible() and not pg.locator('#kpis').is_visible())
        check('le canal est Gros', pg.locator('#v-canal').input_value() == 'Gros', pg.locator('#v-canal').input_value())
        check('document = devis, déjà choisi', pg.locator('#v-doc').input_value() == 'devis')
        check('la sortie de stock n\'est pas proposée', not pg.locator('#v-stock').is_visible())
        check('le raccourci « coller ou déposer la liste » est là', pg.locator('#v-liste').is_visible())
        check('la liste collée n\'est pas ouverte toute seule', not pg.locator('#msgov').is_visible())

        print('2. le client se choisit en tapant, la liste ne se déroule pas d\'un coup')
        pg.click('#v-client'); pg.wait_for_timeout(200)
        check('un clic dans le champ n\'affiche rien', not pg.locator('#v-cres').is_visible())
        pg.type('#v-client', 'ca'); pg.wait_for_timeout(300)
        check('deux lettres : Carmen est proposée', pg.locator('#v-cres').is_visible() and 'Carmen' in pg.locator('#v-cres').inner_text(), pg.locator('#v-cres').inner_text())
        pg.keyboard.press('ArrowDown'); pg.keyboard.press('Enter'); pg.wait_for_timeout(200)
        check('choisie au clavier', pg.locator('#v-client').input_value() == 'Carmen', pg.locator('#v-client').input_value())

        print('3. le sélectionneur : une marque tapée, tous ses parfums, on coche, on ajoute')
        pg.fill('#v-q', 'paco rabanne'); pg.wait_for_timeout(500)
        n = pg.evaluate("CANDIDATS.length")
        check('tous les Paco Rabanne s\'affichent (bien plus que 40)', n > 40 and pg.locator('#v-res').is_visible(), n)
        premier = pg.locator('#v-res .cand b').first.inner_text()
        check('la marque elle-même d\'abord, pas les parfums qui la citent', premier.startswith('Paco Rabanne'), premier)
        ligne = pg.locator('#v-res .cand').first.inner_text()
        check('chaque ligne : la vignette, le nom, le stock — pas de prix', pg.locator('#v-res .cand .vig').count() == n and 'stock' in ligne and 'achat' not in ligne and '$' not in ligne, ligne)
        # 11 nov. 2026 (Igal) : cocher = mettre dans la cote, tout de suite — plus de bouton « Ajouter » qui attend
        check('rien n\'est dans la cote tant qu\'on n\'a rien coché', pg.evaluate("PANIER.length") == 0)
        pg.locator('#v-res .cand').nth(0).click(); pg.locator('#v-res .cand').nth(1).click(); pg.locator('#v-res .cand').nth(2).click(); pg.wait_for_timeout(200)
        pg.locator('#v-res .cand').nth(1).click(); pg.wait_for_timeout(200)
        check('coché, décoché : 2 sont déjà dans la cote', pg.evaluate("PANIER.length") == 2 and pg.locator('#v-res .cand.coche').count() == 2, pg.evaluate("PANIER.length"))
        # LE POINT — chercher une autre marque ne fait rien perdre
        pg.fill('#v-q', 'versace'); pg.wait_for_timeout(500); pg.fill('#v-q', 'paco rabanne'); pg.wait_for_timeout(500)
        check('LE POINT — une autre marque cherchée puis revenue : les 2 sont toujours dans la cote, et cochés dans la liste', pg.evaluate("PANIER.length") == 2 and pg.locator('#v-res .cand.coche').count() == 2)
        pg.click('#v-cadd'); pg.wait_for_timeout(400)
        pan = pg.evaluate("PANIER.map(l=>({cle:l.cle,q:l.q,p:l.p}))")
        check('les 2 cochés sont dans le devis, la recherche s\'est refermée', len(pan) == 2 and not pg.locator('#v-res').is_visible(), pan)
        check('la vignette suit le parfum dans le devis', pg.locator('#v-pan tbody .vig').count() == 2)
        tetes = pg.locator('#v-pan thead').inner_text().lower()
        check('les lignes montrent prix d\'achat, tarif gros et prix proposé', "prix d'achat" in tetes and 'tarif gros' in tetes and 'prix proposé' in tetes, tetes)
        pg.evaluate("PANIER.length=0; peintPanier();")
        pg.fill('#v-q', 'Le Male Elixir Absolu'); pg.wait_for_timeout(400)
        pg.keyboard.press('Enter'); pg.wait_for_timeout(300)
        pan = pg.evaluate("PANIER.map(l=>({cle:l.cle,q:l.q,p:l.p}))")
        check('Entrée sans rien cocher : le premier trouvé entre seul', len(pan) == 1 and pan[0]['cle'] == A[15], (pan, pg.evaluate("CANDIDATS.slice(0,3)")))
        check('avec le prix de gros pré-rempli', abs(pan[0]['p'] - PVW_A) < 0.01, (pan[0]['p'], PVW_A))
        pg.fill('#v-pan input[data-f="q"]', '5'); pg.keyboard.press('Tab'); pg.wait_for_timeout(300)
        pg.fill('#v-pan input[data-f="p"]', str(round(PVW_A * 0.9, 2))); pg.keyboard.press('Tab'); pg.wait_for_timeout(300)
        pan = pg.evaluate("PANIER.map(l=>({cle:l.cle,q:l.q,p:l.p}))")
        check('quantité et prix corrigés à la main', pan[0]['q'] == 5 and abs(pan[0]['p'] - round(PVW_A * 0.9, 2)) < 0.01, pan)

        print('4. le raccourci : une liste collée ou déposée REJOINT le devis en cours')
        pg.click('#v-liste'); pg.wait_for_timeout(400)
        check('la fenêtre de la liste s\'ouvre', pg.locator('#msgov').is_visible())
        check('le client y est repris', pg.locator('#m-client').input_value() == 'Carmen')
        check('la zone de dépôt accepte tout', 'image/*' in (pg.get_attribute('#m-fichier', 'accept') or ''))
        pg.fill('#m-txt', 'Bleu de Chanel edp 3.4 oz x 3'); pg.wait_for_timeout(500)
        pg.click('#m-devis'); pg.wait_for_timeout(500)
        pan = pg.evaluate("PANIER.map(l=>({cle:l.cle,q:l.q,p:l.p}))")
        check('la ligne reconnue s\'ajoute SANS effacer ce qui était déjà là', len(pan) == 2 and pan[0]['q'] == 5 and pan[1]['cle'] == B[15] and pan[1]['q'] == 3, pan)
        check('la fenêtre de la liste s\'est refermée', not pg.locator('#msgov').is_visible())
        pg.click('#v-liste'); pg.wait_for_timeout(300)
        csv = f"code-barres;nom;quantite\n{BC_A};n'importe quoi;4\n"
        m = pg.evaluate(DEPOSE, ['liste.csv', 'text/csv', base64.b64encode(csv.encode()).decode()])
        check('un fichier déposé est lu', 'Lu : liste.csv' in m, m)
        pg.click('#m-devis'); pg.wait_for_timeout(500)
        pan = pg.evaluate("PANIER.map(l=>({cle:l.cle,q:l.q,p:l.p}))")
        check('un parfum déjà présent voit sa quantité s\'ajouter (5 + 4)', len(pan) == 2 and pan[0]['q'] == 9, pan)
        pg.fill('#v-pan input[data-f="q"]', '5'); pg.wait_for_timeout(200)
        pg.click('#v-liste'); pg.wait_for_timeout(300)
        m = pg.evaluate(DEPOSE, ['liste.jpg', 'image/jpeg', base64.b64encode(photo(['Le Male Elixir Absolu 4.2 oz x 2', 'Chanel Bleu edp 3.4 oz x 3'])).decode()])
        L = pg.evaluate("M_L.map(l=>({cle:l.cle,q:l.q,sur:l.sur}))")
        check('une photo passe par la même porte', 'Lu : liste.jpg' in m and len(L) == 2 and all(l['cle'] for l in L), (m, L))
        pg.click('#m-ann'); pg.wait_for_timeout(200)
        check('« Annuler » la liste ne touche pas au devis', pg.evaluate("PANIER.length") == 2 and not pg.locator('#msgov').is_visible())

        print('5. l\'enregistrement : le stock ne bouge pas')
        stock_avant = pg.evaluate(f"qteEff({json.dumps(A[15])})")
        pg.click('#v-ok'); pg.wait_for_timeout(1200)
        F = pg.evaluate("lit('factures-v1',[]).filter(f=>f.sens==='devis')")
        check('un devis est enregistré', len(F) == 1, len(F))
        f = F[0] if F else {}
        check('numéro DV-', f.get('doc', {}).get('num', '').startswith('DV-'), f.get('doc', {}).get('num'))
        check('client Carmen, 5 flacons au prix corrigé', f.get('tiers') == 'Carmen' and f['lignes'][0]['q'] == 5 and abs(f['lignes'][0]['p'] - round(PVW_A * 0.9, 2)) < 0.01, f.get('lignes', [{}])[0])
        stock_apres = pg.evaluate(f"qteEff({json.dumps(A[15])})")
        check('le stock n\'a pas bougé', stock_avant == stock_apres, (stock_avant, stock_apres))

        print('6. l\'envoi : le document avec WhatsApp et email')
        check('le document est ouvert', pg.locator('#docov').is_visible())
        check('bouton WhatsApp', pg.locator('#doc-wa').is_visible())
        check('bouton Email', pg.locator('#doc-mail').is_visible())
        t = pg.evaluate("docTexte(DOC)")
        check('le texte est écrit comme à la main : bonjour, merci, le numéro, la ligne, le total', t.startswith('Bonjour Carmen,') and 'Merci pour votre demande de cotation' in t and '*DV-' in t and '× 5' in t and '*TOTAL' in t, t[:200])
        # l'envoi tente d'abord de fabriquer le PDF (ici sans serveur : il le dit et part en texte)
        wa = pg.evaluate("""async()=>{ let u=''; const o=window.open; window.open=x=>({closed:false,document:{write(){}},location:{set href(v){u=v;}}});
            $('doc-wa').click(); for(let i=0;i<100&&!u;i++) await new Promise(r=>setTimeout(r,100)); window.open=o; return u; }""")
        check('sans serveur, l\'outil le dit au lieu de bloquer', 'sans le PDF' in pg.locator('#doc-etat').inner_text(), pg.locator('#doc-etat').inner_text())
        check('WhatsApp part vers le numéro de la fiche client', wa.startswith('https://wa.me/13055550100?text='), wa[:60])
        # 9 oct. 2026 — WhatsApp « ne fonctionne pas » : client sans numéro, et fenêtre bloquée
        sav = pg.evaluate("DOC.tiers"); pg.evaluate("DOC.tiers='Client Sans Telephone'")
        pg.evaluate("window.__wa=''; $('doc-wa').click()"); pg.wait_for_timeout(300)
        check('client sans numéro : on le demande au lieu d\'ouvrir wa.me/ vide', pg.locator('#waov').is_visible() and pg.evaluate("window.__wa") == '')
        pg.fill('#wa-a', 'abc'); pg.click('#wa-ok'); pg.wait_for_timeout(200)
        check('un numéro illisible est refusé', pg.locator('#waov').is_visible() and 'illisible' in pg.locator('#wa-etat').inner_text())
        wa2 = pg.evaluate("""async()=>{ const o=window.open; window.open=x=>null; $('wa-a').value='305 555 0199'; $('wa-ok').click();
            for(let i=0;i<100&&!window.__wa;i++) await new Promise(r=>setTimeout(r,100)); window.open=o; return window.__wa; }""")
        check('le numéro tapé part avec l\'indicatif 1', wa2.startswith('https://wa.me/13055550199?text='), wa2[:50])
        check('fenêtre bloquée : un bouton « Ouvrir WhatsApp » prend le relais', pg.locator('#doc-wa2').is_visible())
        check('et le numéro est gardé sur la fiche client', '3055550199' in pg.evaluate("JSON.stringify(coordTiers('Client Sans Telephone'))").replace(' ', ''))
        pg.evaluate("DOC.tiers=%s" % json.dumps(sav))
        check('le devis est dans la liste de la page', 'DV-' in pg.locator('#docs-table').inner_text())

        print('7. le document refermé, un devis vierge attend le suivant')
        pg.click('#doc-x'); pg.wait_for_timeout(400)
        check('le devis est vide', pg.evaluate("PANIER.length") == 0 and pg.locator('#v-client').input_value() == '')
        check('« Vider » remet à zéro sans rien enregistrer', pg.locator('#v-ann').inner_text() == 'Vider')

        print('8. un devis qui ne sert à rien se supprime, pour de bon')
        n0 = pg.evaluate("lit('factures-v1',[]).filter(f=>f.doc&&f.doc.type==='devis').length")
        pg.locator('#docs-table tr.qr').first.click(); pg.wait_for_timeout(300)
        check('le devis déplié a un bouton Supprimer', pg.locator('#docs-table [data-qa="sup"]').count() == 1)
        pg.evaluate("window.__confirmMsg='';window.confirm=m=>{window.__confirmMsg=m;return false;}")
        pg.locator('#docs-table [data-qa="sup"]').first.click(); pg.wait_for_timeout(300)
        check('on demande confirmation, en parlant de « cote » ; refuser ne supprime rien', 'Supprimer la cote' in pg.evaluate("window.__confirmMsg") and pg.evaluate("lit('factures-v1',[]).filter(f=>f.doc&&f.doc.type==='devis').length") == n0, pg.evaluate("window.__confirmMsg"))
        pg.evaluate("window.confirm=()=>true")
        pg.locator('#docs-table [data-qa="sup"]').first.click(); pg.wait_for_timeout(500)
        check('accepter le retire de la liste et des données', pg.evaluate("lit('factures-v1',[]).filter(f=>f.doc&&f.doc.type==='devis').length") == n0 - 1 and 'DV-' not in pg.locator('#docs-table').inner_text())
        J = pg.evaluate("lit('crm-journal-v1',[]).slice(-1)[0].lib")
        check('le journal le dit', 'supprimé' in J and 'DV-' in J, J)
        check('aucune erreur JS', not err, err[:3])
        b.close()
finally:
    srv.terminate()
print(f"\n{ok} ok, {len(ko)} KO", ko)
