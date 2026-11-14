# « RETIRER DE LA VENTE » DEPUIS LA FICHE (Sam, via Igal, 11 nov. 2026 : « un validé vert bien voyant pour dire en ligne ; et si on veut
# le retirer, “retirer de la vente” »). Ce test protège :
#   1. LE POINT — une ligne en ligne montre « ✓ En ligne » et « Retirer de la vente » (site de détail, gros, Perfume City) ;
#   2. LE POINT — « Retirer de la vente » sur le détail : une confirmation, puis le cockpit reçoit sens « retirer » pour CE code ;
#      la fiche passe dans les retirées, la ligne dit « Pas en ligne » avec « Mettre en ligne » ;
#   3. Perfume City : la route « retire » de Shopify, le registre dit « pas en vente » ;
#   4. Annuler : rien ne part ; un refus du site : la fiche reste en ligne, l'erreur est dite ;
#   5. le bouton et les mots sont traduits (Take offline / Online) ;
#   5b. LE POINT — « Retiré de la vente : 0 en stock » seulement quand le parfum n'est pas en vente ET que son stock est à 0 ;
#   6. aucune erreur JS.
import subprocess, time, socket, json
from playwright.sync_api import sync_playwright
D = '/home/claude/catalogue'; ok = 0; ko = []
def check(n, c, i=''):
    global ok
    if c: ok += 1; print('  ok  ', n)
    else: ko.append(n); print('  KO  ', n, str(i)[:400])
C = json.load(open(D + '/cat.json'))
A = [r for r in C if (r[6] or 0) > 0 and r[0] and r[0].isdigit() and len(r[0]) == 13 and (r[8] or 0) > 0 and r[15]][7]
BC = A[0]
Z = [r for r in C if (r[6] or 0) == 0 and r[0] and r[0].isdigit() and len(r[0]) == 13 and (r[8] or 0) > 0 and r[15]][3]
SITE = {BC: {'d': {'id': 1, 'q': 3, 'suivi': True, 'pr': 99, 'ps': None, 'nom': 'x'}, 'g': {'id': 2, 'q': 3, 'suivi': True, 'pr': 60, 'ps': None, 'nom': 'x'}}, '_maj': {'d': '2026-11-10T08:00:00Z', 'g': '2026-11-10T08:00:00Z'}}
SH = {BC: [111, 222, 95, None, 1, 'h', '', 3], '_maj': '2026-11-10T08:00:00Z'}
s = socket.socket(); s.bind(('127.0.0.1', 0)); port = s.getsockname()[1]; s.close()
srv = subprocess.Popen(['python3', '-m', 'http.server', str(port), '--bind', '127.0.0.1'], cwd=D, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)
try:
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1440, 'height': 1000}); err = []; dlg = []; rep = {'ok': True, 'refus': False}
        pg.on('pageerror', lambda e: err.append(str(e)))
        pg.on('dialog', lambda d: (dlg.append(d.message), d.accept() if rep['ok'] else d.dismiss()))
        env = []
        def statut(r):
            body = json.loads(r.request.post_data or '{}'); env.append(('statut', body))
            j = {'ok': True, 'ecrites': 0, 'refus': [{'bc': BC, 'pourquoi': 'le site refuse'}]} if rep['refus'] else {'ok': True, 'ecrites': 1, 'refus': []}
            r.fulfill(status=200, content_type='application/json', body=json.dumps(j))
        pg.route('**/api/o/dasy/site/statut', statut)
        pg.route('**/api/o/dasy/shopify/retire', lambda r: (env.append(('shopify', json.loads(r.request.post_data or '{}'))), r.fulfill(status=200, content_type='application/json', body=json.dumps({'ok': True, 'nom': 'x'}))))
        base = f'http://127.0.0.1:{port}/'
        def ouvre(lg='fr'):
            pg.goto(base + 'accueil.html'); pg.wait_for_timeout(300)
            pg.evaluate("""([s,sh,lg])=>{ localStorage.clear(); localStorage.setItem('sam-comptes-demo-v1','0');
              localStorage.setItem('sam-session-v1',JSON.stringify({id:'sam',nom:'Sam',role:'patron',depuis:new Date().toISOString()}));
              localStorage.setItem('ck-token','jeton-test'); localStorage.setItem('langue-v1',lg); localStorage.setItem('site-stock-v1',JSON.stringify(s)); localStorage.setItem('shopify-pc-prix-v1',JSON.stringify(sh)); }""", [SITE, SH, lg])
            pg.goto(base + 'catalogue.html#cle=' + A[15] + '&canaux=1'); pg.wait_for_timeout(3500)
        L = lambda cid: pg.locator(f'[data-cn="{cid}"]')
        T = lambda cid: pg.evaluate("c=>{ const e=document.querySelector('[data-cn=\"'+c+'\"]'); return e?e.innerText.replace(/\\s+/g,' '):''; }", cid)
        ouvre()
        check('LE POINT — détail, gros, Perfume City : « ✓ En ligne » + « Retirer de la vente »', all('En ligne' in L(c).inner_text() and L(c).locator('[data-retv]').count() == 1 for c in ('site', 'sitegros', 'perfumecity')), [L(c).inner_text() for c in ('site', 'sitegros', 'perfumecity')])
        rep['ok'] = False; L('site').locator('[data-retv]').click(); pg.wait_for_timeout(500)
        check('Annuler : rien ne part', not env and dlg and 'Retirer' in dlg[-1], (env, dlg[-1:]))
        rep['ok'] = True; L('site').locator('[data-retv]').click(); pg.wait_for_timeout(1500)
        check('LE POINT — le cockpit reçoit « retirer » pour CE code, sur le détail', env and env[0][0] == 'statut' and env[0][1] == {'quel': '', 'sens': 'retirer', 'bcs': [BC]}, env)
        S = pg.evaluate("JSON.parse(localStorage.getItem('site-stock-v1'))")
        check('la fiche passe dans les retirées du détail', BC in ((S.get('_retires') or {}).get('d') or {}) and not (S.get(BC) or {}).get('d'), S)
        check('la ligne dit « Pas en ligne » avec « Mettre en ligne »', 'Pas en ligne' in L('site').inner_text() and L('site').locator('[data-remet="site"]').count() == 1, L('site').inner_text())
        env.clear(); L('perfumecity').locator('[data-retv]').click(); pg.wait_for_timeout(1500)
        check('Perfume City : la route « retire » de Shopify, le registre dit « pas en vente »', env and env[0] == ('shopify', {'bc': BC}) and pg.evaluate("bc=>JSON.parse(localStorage.getItem('shopify-pc-prix-v1'))[bc][4]", BC) == 0, env)
        check('et la ligne Perfume City n\'est plus « En ligne » (0 en stock chez Perfume City : « Retiré de la vente : 0 en stock »)', 'Retiré de la vente : 0 en stock' in T('perfumecity'), T('perfumecity'))
        env.clear(); rep['refus'] = True; dlg.clear(); L('sitegros').locator('[data-retv]').click(); pg.wait_for_timeout(1500)
        S = pg.evaluate("JSON.parse(localStorage.getItem('site-stock-v1'))")
        check('refus du site : l\'erreur est dite, le gros reste en ligne', any('Pas retiré' in d for d in dlg) and (S.get(BC) or {}).get('g'), dlg)
        rep['refus'] = False
        print('« Retiré de la vente : 0 en stock » — seulement quand c\'est vrai')
        check('stock > 0 et pas en vente : « Pas en ligne », pas de mention de stock', 'Pas en ligne' in L('site').inner_text() and '0 en stock' not in L('site').inner_text(), L('site').inner_text())
        # un parfum à 0 en stock : en ligne sur le gros (0 sur le site), retiré du détail
        pg.evaluate("z=>{ const S=JSON.parse(localStorage.getItem('site-stock-v1')); S[z]={g:{id:7,q:0,suivi:true,pr:60,ps:null,nom:'z'}}; S._retires=S._retires||{}; S._retires.d=Object.assign({},S._retires.d,{[z]:{id:8,q:0,suivi:true,pr:90,ps:null,nom:'z',auto:1}}); localStorage.setItem('site-stock-v1',JSON.stringify(S)); }", Z[0])
        pg.goto(base + 'catalogue.html#cle=' + Z[15] + '&canaux=1'); pg.reload(); pg.wait_for_timeout(3500)
        check('LE POINT — stock à 0 et pas en vente : « Retiré de la vente : 0 en stock »', 'Retiré de la vente : 0 en stock' in T('site'), T('site'))
        # 14 nov. 2026 (Igal, capture à l'appui : « écritures écrasées ») : la mention ne déborde jamais sur la colonne de la marge
        def chevauche():
            return pg.evaluate("()=>{ const r=document.querySelector('[data-cn=\"site\"]'); const h=r&&r.querySelector('.hors'), c=r&&r.querySelector('.c4'); if(!h||!c) return 'absent'; const a=h.getBoundingClientRect(), b=c.getBoundingClientRect(); return a.right>b.left+1&&a.bottom>b.top&&a.top<b.bottom ? [a.right,b.left] : ''; }")
        res = []
        for w in (1440, 1200, 1024):
            pg.set_viewport_size({'width': w, 'height': 1000}); pg.wait_for_timeout(300); res.append((w, chevauche()))
        pg.set_viewport_size({'width': 1440, 'height': 1000})
        check('LE POINT — « Retiré de la vente : 0 en stock · revient tout seul » reste dans sa colonne (1440, 1200, 1024 px) : rien n\'écrase la marge', all(x == '' for _, x in res) and 'revient tout seul' in T('site'), res)
        check('stock à 0 mais encore en vente (gros) : « ✓ En ligne » + « 0 en stock », pas « Retiré »', 'En ligne' in T('sitegros') and '0 en stock' in T('sitegros') and 'Retiré' not in T('sitegros'), T('sitegros'))
        ouvre('en')
        check('en anglais : « ✓ Online » et « Take offline »', 'Online' in L('site').inner_text() and 'Take offline' in L('site').inner_text(), L('site').inner_text())
        check('aucune erreur JS', not err, err[:3])
        b.close()
finally:
    srv.terminate()
print(f'\n{ok} ok, {len(ko)} KO', ko); raise SystemExit(1 if ko else 0)
