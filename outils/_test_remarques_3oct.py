# Les remarques de Sam du 2 oct. 2026 (traitées le 3) :
#   1. une marque créée dans l'ERP apparaît dans « Toutes les marques » ;
#   2. un prix changé dans la fiche est proposé aux sites — promo sur le détail, prix du gros ;
#   3. la remise de 10 % faite à la caisse (Nasha, 392 $ → 352,80 $) est prise en compte :
#      lignes au prix encaissé (marge juste), facture au prix affiché + remise, total 377,50 $ ;
#   4. « Chèque » dans les modes de paiement ;
#   5. la fiche d'une vente à plusieurs parfums n'a plus le nom du premier en titre ;
#   6. un employé (Commercial) ne voit ni marge ni prix d'achat ; le Patron, si.
import pathlib, subprocess, time, socket, json
from playwright.sync_api import sync_playwright
D = pathlib.Path('/home/claude/catalogue')
ok = 0; ko = []
def check(n, c, i=''):
    global ok
    if c: ok += 1; print('  ok  ', n)
    else: ko.append(n); print('  KO  ', n, i)
CAT = json.load(open(D / 'cat.json'))
R = [r for r in CAT if r[0] and r[0].isdigit() and (r[6] or 0) > 3][:3]
s = socket.socket(); s.bind(('127.0.0.1', 0)); port = s.getsockname()[1]; s.close()
srv = subprocess.Popen(['python3', '-m', 'http.server', str(port), '--bind', '127.0.0.1'], cwd=str(D), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1)
FILE = [{'_i': 'amazon|111-1794126-1149821', 'src': 'amazon', 'num': '111-1794126-1149821', 'd': '2026-10-03', 'h': '16:08', 'commande': '2026-09-30', 'lieu': 'Amazon',
         'lignes': [{'bc': str(R[0][0]), 'des': 'x', 'q': 1, 'p': 45.5}]},
        {'_i': 'lightspeed|nasha', 'src': 'lightspeed', 'num': 'nasha', 'd': '2026-10-02', 'h': '16:20', 'client': 'NASHA',
         'total': 377.5, 'taxe': 24.7, 'remise': 39.2,
         'lignes': [{'bc': str(R[0][0]), 'des': 'a', 'q': 1, 'p': 170}, {'bc': str(R[1][0]), 'des': 'b', 'q': 1, 'p': 98}, {'bc': str(R[2][0]), 'des': 'c', 'q': 1, 'p': 124}]}]
ENVOIS = []
SRV = {}
def cockpit(route, req):
    u = req.url
    if u.endswith('/site/prix'):
        b = json.loads(req.post_data or '{}'); ENVOIS.append(b)
        return route.fulfill(status=200, content_type='application/json', body=json.dumps({'ok': True, 'avant': {'barre': b['attendu']['barre'], 'promo': b['attendu']['promo']}, 'apres': {'barre': b['barre'], 'promo': None if b['promo'] == '' else b['promo']}}))
    # 20 oct. 2026 : en ligne, la file et le stock sont relus au serveur avant d'enregistrer une vente
    if '/file/bail' in u: return route.fulfill(status=200, content_type='application/json', body='{"chef":true}')
    if req.method == 'GET' and '/donnees/caisse-file-v1' in u:
        return route.fulfill(status=200, content_type='application/json', body=json.dumps({'val': SRV.get('file', FILE), 'ver': 1}))
    if req.method == 'PUT' and '/donnees/caisse-file-v1' in u:
        SRV['file'] = json.loads(req.post_data or '{}').get('val', [])
    elif req.method == 'GET' and '/donnees/' in u and '/donnees/versions' not in u:
        return route.fulfill(status=404, content_type='application/json', body='{"erreur":"Magasin vide."}')
    if '/donnees/lire' in u: return route.fulfill(status=200, content_type='application/json', body=json.dumps({'magasins': {}, 'versions': {'x-v1': 1}}))
    if '/flux' in u: return route.fulfill(status=404, content_type='application/json', body='{}')
    if '/donnees/versions' in u: return route.fulfill(status=200, content_type='application/json', body='{}')
    return route.fulfill(status=200, content_type='application/json', body=json.dumps({'ver': 1}))
def session(pg, role, extra=''):
    pg.evaluate("""([r,f])=>{ localStorage.clear(); localStorage.setItem('sam-comptes-demo-v1','0');
      localStorage.setItem('sam-comptes-v1',JSON.stringify([{ident:'sam',nom:'Sam',role:'patron',actif:true,h:'x'},{ident:'josh',nom:'Josh',role:'commercial',actif:true,h:'x'}]));
      localStorage.setItem('sam-session-v1',JSON.stringify(r==='patron'?{id:'sam',nom:'Sam',role:'patron',depuis:new Date().toISOString()}:{id:'josh',nom:'Josh',role:'commercial',depuis:new Date().toISOString()}));
      localStorage.setItem('crm-utilisateur-v1',r==='patron'?'Sam':'Josh'); localStorage.setItem('langue-v1','fr'); localStorage.setItem('sheet-installe-2026-09-03','1');
      localStorage.setItem('caisse-file-v1',JSON.stringify(f)); localStorage.setItem('ck-token','jeton'); }""", [role, FILE])
try:
    with sync_playwright() as p:
        b = p.chromium.launch(args=['--host-resolver-rules=MAP erp.test 127.0.0.1']); err = []
        ctx = b.new_context(viewport={'width': 1500, 'height': 950})
        ctx.add_init_script("window.COCKPIT_URL='http://ck.test';"); ctx.route('http://ck.test/**', cockpit)
        pg = ctx.new_page(); pg.on('pageerror', lambda e: err.append(str(e)))
        DLG = []
        def dlg(d): DLG.append(d.message); d.accept()
        pg.on('dialog', dlg)
        base = f'http://erp.test:{port}/'
        pg.goto(base + 'accueil.html'); pg.wait_for_timeout(300)
        session(pg, 'patron')
        pg.evaluate("localStorage.removeItem('caisse-file-v1')")

        print('1. une nouvelle marque')
        pg.goto(base + 'catalogue.html'); pg.wait_for_timeout(2500)
        pg.click('#add'); pg.wait_for_timeout(300)
        check("l'aide sous « Marque » dit comment créer une marque", 'Nouvelle marque' in pg.locator('#f-marque').evaluate("e=>e.parentNode.innerText"))
        pg.fill('#f-marque', 'Zeta Nova Parfums'); pg.fill('#f-nom', 'Essai'); pg.click('#mo'); pg.wait_for_timeout(600)
        # depuis le 18 oct., un nouvel article sans photo ouvre tout seul la recherche de photo : on la ferme
        pg.evaluate("()=>{ const o=document.getElementById('pw-ov'); if(o){ const x=o.querySelector('[data-pwx],.pwx,button[aria-label]'); if(x) x.click(); else o.remove(); } }"); pg.wait_for_timeout(300)
        opts = pg.eval_on_selector_all('#fb option', 'l=>l.map(o=>o.value)')
        check('LE POINT — la marque créée est dans « Toutes les marques »', 'Zeta Nova Parfums' in opts, len(opts))

        print('2. le prix changé part aux sites, sur question')
        X = pg.evaluate("""()=>{ const p=tousLesArticles().find(x=>x.qte>3&&x.pvr>30&&x.pvw>20&&x.pa>5&&/^\\d+$/.test(x.bc));
          SITE[p.bc]={d:{id:1,q:p.qte,suivi:true,pr:p.pvr,ps:null},g:{id:2,q:p.qte,suivi:true,pr:p.pvw,ps:null}}; _SITE0=null;
          ecrit('site-stock-v1',SITE); $('fs').value=''; $('fx').value=''; $('q').value=p.bc; render(); ouvreFiche(p.id); return {bc:p.bc,pvr:p.pvr,pvw:p.pvw}; }""")
        pg.wait_for_timeout(500)
        pg.fill('#ddb input[data-pc="site"]', str(X['pvr'] + 5)); pg.fill('#ddb [data-sbx="sitegros"] [data-sb]', str(X['pvw'] + 3)); pg.click('#dnom')   # 17 oct. : le gros n'a plus qu'UNE case, le prix en ligne (elle part sur le site à l'Enregistrer)   # 12 oct. : plus de cartes gros/retail, on règle le prix du canal; pg.wait_for_timeout(500)
        DLG.clear(); pg.click('#dok'); pg.wait_for_timeout(600)
        q = pg.locator('#pxb .pxsit').inner_text() if pg.locator('#pxb .pxsit').count() else ''
        # 20 oct. 2026 (une seule validation) : le prix tapé dans la case du gros est confirmé DANS cette même fenêtre ; la case « mettre aussi sur les sites » reste pour le prix de l'outil
        check('la fenêtre « Confirmer les prix » dit ce qui change sur les sites', 'perfumestrade.com' in pg.inner_text('#pxb'), pg.inner_text('#pxb')[:300])
        check('rien ne part pour le détail avant « OK, enregistrer »', not any(e['quel'] == '' for e in ENVOIS))
        pg.click('#pxok'); pg.wait_for_timeout(1500)
        dd = next((e for e in ENVOIS if e['quel'] == ''), {}); gg = next((e for e in ENVOIS if e['quel'] == 'gros'), {})
        # 11 nov. 2026 (Sam) : plus de prix barré — le détail reçoit le nouveau prix, sans promo
        check('LE POINT — détail : le nouveau prix part, sans prix barré', dd.get('barre') == X['pvr'] + 5 and dd.get('promo') == '', dd)
        check('gros sans promo : le prix du gros devient le nouveau prix de gros', gg.get('barre') == X['pvw'] + 3 and gg.get('promo') == '', gg)
        # 11 nov. 2026 (Sam) : une ligne = UN prix, celui du site — plus de « mettre aussi sur les sites » à décocher pour le détail en ligne
        print('3. la remise de la caisse')
        pg.goto(base + 'accueil.html'); pg.wait_for_timeout(200); session(pg, 'patron')
        pg.goto(base + 'ventes.html'); pg.wait_for_timeout(3000)
        F = pg.evaluate("JSON.parse(localStorage.getItem('factures-v1')||'[]')")
        f = next((x for x in F if x.get('num') == 'nasha'), {})
        Ls = f.get('lignes') or []
        check('la vente est enregistrée', bool(Ls), F[:1])
        check('LE POINT — lignes au prix encaissé : 153 / 88,20 / 111,60', [l.get('p') for l in Ls] == [153, 88.2, 111.6], [l.get('p') for l in Ls])
        check('et le prix affiché gardé (170 / 98 / 124)', [l.get('pAv') for l in Ls] == [170, 98, 124])
        Dc = f.get('doc') or {}
        check('facture : sous-total 392, remise 39,20, base 352,80, taxe 24,70 (7 %), total 377,50',
              Dc.get('sousTotal') == 392 and Dc.get('remise') == 39.2 and Dc.get('base') == 352.8 and Dc.get('taxe') == 24.7 and Dc.get('taux') == 7 and Dc.get('total') == 377.5, Dc)
        check('montant de la vente : 352,80', abs((f.get('montant') or 0) - 352.8) < 0.01, f.get('montant'))
        check('la note le dit', 'remise de 39.20 $' in (f.get('note') or ''), f.get('note'))
        V = pg.evaluate("JSON.parse(localStorage.getItem('ventes-v1')||'{}')")
        check("l'historique du parfum garde 153 $", any(e.get('p') == 153 for e in V.get(R[0][15], [])), V.get(R[0][15]))

        fa = next((x for x in F if x.get('num') == '111-1794126-1149821'), {})
        check('Amazon confirmée après « pending » : rangée au jour de la confirmation, la commande dite dans la note',
              fa.get('d') == '2026-10-03' and fa.get('commande') == '2026-09-30' and '09/30/2026' in (fa.get('note') or '') and '10/03/2026' in (fa.get('note') or ''), [fa.get('d'), fa.get('note')])
        print('4. la fiche de la vente')
        pg.locator('#corps tbody tr[data-d]', has_text='NASHA').first.click(); pg.wait_for_timeout(700)
        t = pg.locator('#d-tit').inner_text()
        check("LE POINT — le titre dit « 3 parfums — NASHA », pas le premier parfum", t.startswith('3 parfums') and 'NASHA' in t and 'code-barres' not in t, t)
        check("pas de bloc « Ce parfum » (un seul parfum) pour une vente à trois", 'Ce parfum' not in pg.eval_on_selector_all('#d-corps h4', 'l=>l.map(h=>h.innerText.trim())'))

        print('5. le chèque')
        pg.click('#d-x') if pg.locator('#d-x').is_visible() else None
        check('« Chèque » dans les modes de paiement de la facture', pg.evaluate("FMODES.cheque==='Chèque'") and pg.locator('#v-pmode option[value="cheque"]').count() == 1)

        print('6. un employé')
        check('le Patron voit la marge (colonne, chiffres du haut)', pg.locator('#kpis').inner_text().lower().count('marge') >= 1 and pg.locator('#corps th.vmg').is_visible())
        pg.goto(base + 'accueil.html'); pg.wait_for_timeout(200); session(pg, 'commercial')
        pg.goto(base + 'ventes.html'); pg.wait_for_timeout(3000)
        k = pg.locator('#kpis').inner_text().lower(); c = pg.locator('#corps').inner_text().lower()
        check('Ventes : ni marge en haut, ni colonne marge', 'marge' not in k and 'marge' not in c, (k[:200], c[:300]))
        pg.click('#corps tbody tr[data-d]'); pg.wait_for_timeout(700)
        dt = pg.locator('#d-corps').inner_text().lower()
        check("la fiche de la vente : ni marge ni prix d'achat", 'marge' not in dt and "prix d'achat" not in dt, dt[:400])
        pg.goto(base + 'catalogue.html'); pg.wait_for_timeout(2500)
        pg.evaluate("()=>{ const p=tousLesArticles().find(x=>x.qte>5&&x.pa); ouvreFiche(p.id); }"); pg.wait_for_timeout(600)
        fi = pg.locator('#dr').inner_text().lower()
        check("la fiche du parfum : ni prix d'achat, ni marge, ni « il te reste »", 'achat' not in fi and 'marge' not in fi and 'il te reste' not in fi, [l for l in fi.split('\n') if 'achat' in l or 'marge' in l][:5])
        pg.goto(base + 'factures.html'); pg.wait_for_timeout(1500)
        check('Factures (achats) : un mur, pas les prix', pg.locator('#pmur').is_visible() and "pas pour ce rôle" in pg.locator('#pmur').inner_text())
        pg.goto(base + 'reglages.html'); pg.wait_for_timeout(1500)
        check('Réglages : un mur', pg.locator('#pmur').is_visible())
        check('aucune erreur JS', not err, err[:3])
        b.close()
finally:
    srv.terminate()
print(f'\n{ok} ok, {len(ko)} KO')
if ko: print('KO :', ko); raise SystemExit(1)
