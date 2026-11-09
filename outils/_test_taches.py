# LA RUBRIQUE « TÂCHES » (Igal, 3 nov. 2026 : « une rubrique sous Tableau de bord avec les tâches à exécuter ; Sam valide, ignore —
# elle se met en dessous — ou demande un rappel demain, dans 2, 5, 10 jours »). Un faux cockpit rend la liste. Ce test protège :
#   1. LE POINT : « Tâches » est au menu sous Tableau de bord, dans Pilotage (pas pour un commercial), avec la pastille du nombre à faire ;
#   2. LE POINT : la page montre les tâches à faire (urgentes d'abord, lien « Faire » vers la bonne page), celles en attente avec leur
#      date, les ignorées repliées en bas ;
#   3. LE POINT : Fait / Ignorer / rappel (demain, 2, 5, 10 jours) / Remettre dans la liste partent au cockpit avec l'identifiant ;
#   4. un commercial voit le mur ; en anglais, pas un mot de français ; aucune erreur JS ;
#   5. le tableau de bord publie la liste « pas en vente partout » (diffusion-erp-v1) pour le cockpit.
import pathlib, subprocess, time, socket, json, re, threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from playwright.sync_api import sync_playwright
D = pathlib.Path('/home/claude/catalogue'); ok = 0; ko = []
def check(n, c, i=''):
    global ok
    if c: ok += 1; print('  ok  ', n)
    else: ko.append(n); print('  KO  ', n, str(i)[:500])
ETATS = []
LISTE = {'jour': '2026-11-03', 'rappels': [1, 2, 5, 10], 'urgentes': 2, 'faites': 0,
  'a_faire': [
    # 8 nov. 2026 : le cockpit envoie les chiffres (ps, q90, qte, vente, margeMin, raisons, n…) ; la page écrit les textes dans la langue de l'écran
    {'id': 'rupture|b1', 'type': 'rupture', 'urgence': 'haute', 'titre': 'Recommander Ferrari Scuderia Black EDT', 'detail': 'À zéro, et ça part à 3,3 par semaine (42 vendus sur 90 jours).', 'lien': 'catalogue.html#cle=b1', 'cle': 'b1', 'etat': 'a_faire', 'ref': 'Ferrari Scuderia Black EDT', 'ps': 3.3, 'q90': 42, 'qte': 0},
    {'id': 'prix|b2', 'type': 'prix', 'urgence': 'haute', 'titre': 'Vendu à perte : Armaf Club De Nuit Bling EDP', 'detail': '02/11, Gros : vendu 30 $, acheté 45 $ → perte de 15 $. Vérifie son prix.', 'lien': 'catalogue.html#cle=b2', 'etat': 'a_faire', 'revenue': True,
     'ref': 'Armaf Club De Nuit Bling EDP', 'margeMin': 10, 'vente': {'d': '2026-11-02', 'canal': 'Gros', 'p': 30, 'pa': 45, 'mg': -15, 'pct': -50, 'n': 1, 'perte': True, 'q': 1, 'com': 0, 'carte': 0, 'envoi': 0, 'port': 0}},
    {'id': 'enligne|sitegros', 'type': 'enligne', 'urgence': 'normale', 'titre': 'Mettre en ligne 412 parfums sur wholesale.perfumestrade.com', 'detail': 'En stock mais pas en vente, dont 300 retirés faute de prix.', 'lien': 'catalogue.html?diff=sitegros', 'etat': 'a_faire'}],
  'attente': [{'id': 'manque|b4', 'type': 'manque', 'urgence': 'normale', 'titre': 'Recommander Bleu de Chanel EDP', 'detail': '2 en stock, 1,5 vendus par semaine : plus rien dans 9 jours.', 'lien': 'catalogue.html#cle=b4', 'etat': 'attente', 'jusqua': '2026-11-08', 'ref': 'Bleu de Chanel EDP', 'ps': 1.5, 'q90': 19, 'qte': 2, 'jours': 9}],
  'ignorees': [{'id': 'publication|b5', 'type': 'publication', 'urgence': 'normale', 'titre': 'Reprendre la mise en ligne de Hanae Mori HM EDP', 'detail': 'perfumestrade.com : photo manquante.', 'lien': 'catalogue.html?q=b5', 'etat': 'ignoree', 'depuis': '2026-11-01T10:00:00Z', 'ref': 'Hanae Mori HM EDP', 'bc': '5', 'raisons': [{'canal': 'site', 'nom': 'perfumestrade.com', 'r': 'photo manquante'}]}]}
class Faux(BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def _rep(self, code, obj):
        b = json.dumps(obj).encode(); self.send_response(code); self.send_header('Content-Type', 'application/json'); self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Headers', 'Authorization, Content-Type'); self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, OPTIONS'); self.end_headers(); self.wfile.write(b)
    def do_OPTIONS(self): self._rep(200, {})
    def do_GET(self):
        if self.path.endswith('/galou/taches'): return self._rep(200, LISTE)
        if self.path.endswith('/galou/etat'): return self._rep(200, {'pret': True, 'voix': False, 'voitMarge': True})
        return self._rep(200, {})
    def do_POST(self):
        n = int(self.headers.get('Content-Length') or 0); corps = json.loads(self.rfile.read(n) or b'{}')
        if self.path.endswith('/galou/taches/etat'): ETATS.append(corps); return self._rep(200, {'ok': True})
        return self._rep(200, {'ok': True})
    def do_PUT(self): n = int(self.headers.get('Content-Length') or 0); self.rfile.read(n); return self._rep(200, {'ok': True, 'ver': 1})
s = socket.socket(); s.bind(('127.0.0.1', 0)); port = s.getsockname()[1]; s.close()
s = socket.socket(); s.bind(('127.0.0.1', 0)); pck = s.getsockname()[1]; s.close()
srv = subprocess.Popen(['python3', '-m', 'http.server', str(port), '--bind', '127.0.0.1'], cwd=str(D), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
faux = HTTPServer(('127.0.0.1', pck), Faux); threading.Thread(target=faux.serve_forever, daemon=True).start(); time.sleep(0.8)
SESS = """([lg,role])=>{ localStorage.clear(); localStorage.setItem('sam-comptes-demo-v1','0');
  localStorage.setItem('sam-session-v1',JSON.stringify({id:'sam',nom:'Sam',role:role,depuis:new Date().toISOString()}));
  localStorage.setItem('langue-v1',lg); localStorage.setItem('ck-token','jeton-test'); }"""
try:
    with sync_playwright() as p:
        b = p.chromium.launch(); err = []
        def ouvre(page='taches.html', lg='fr', role='patron'):
            pg = b.new_page(viewport={'width': 1400, 'height': 1000}); pg.on('pageerror', lambda e: err.append(str(e))); pg.on('dialog', lambda d: d.accept())
            pg.add_init_script(f"window.COCKPIT_URL='http://127.0.0.1:{pck}';")
            base = f'http://127.0.0.1:{port}/'
            pg.goto(base + 'accueil.html'); pg.wait_for_timeout(300); pg.evaluate(SESS, [lg, role])
            pg.goto(base + page); pg.wait_for_timeout(3200); return pg
        print('1. au menu')
        pg = ouvre('ventes.html')
        check('LE POINT — « Tâches » est au menu, sous Tableau de bord et Analytique (9 nov. 2026), dans Pilotage', pg.evaluate("()=>{ const L=[...document.querySelectorAll('.side nav a.nv')].map(a=>a.textContent.trim().replace(/\\d+$/,'').trim()); const i=L.indexOf('Tableau de bord'); return i>=0&&L[i+1]==='Analytique'&&L[i+2]==='Tâches' && document.querySelector('a.nv[href^=\"taches.html\"]').hasAttribute('data-pilotage'); }"), pg.evaluate("()=>[...document.querySelectorAll('.side nav a.nv')].map(a=>a.textContent.trim())"))
        check('la pastille dit 3 à faire, sur une autre page que Tâches', pg.locator('#ct-taches').inner_text().strip() == '3', pg.locator('#ct-taches').inner_text())
        pg.close()
        pg = ouvre('ventes.html', role='commercial')
        check('un commercial ne voit pas « Tâches » au menu', pg.evaluate("()=>{ const a=document.querySelector('a.nv[href^=\"taches.html\"]'); return !a || getComputedStyle(a).display==='none' || !a.offsetParent; }"))
        pg.close()
        print('2. la page')
        pg = ouvre()
        t = pg.locator('#tk-corps').inner_text().replace('\u00a0', ' ')
        check('LE POINT — les trois tâches à faire, urgentes d\'abord, avec leur détail', pg.locator('#tk-corps .tk').count() == 5 and pg.locator('#tk-corps .tk').nth(0).get_attribute('class').find('haute') >= 0 and 'Recommander Ferrari' in t and 'perte de 15 $' in t, (pg.locator('#tk-corps .tk').count(), [l for l in t.split('\n') if 'perte' in l or 'Ferrari' in l][:4]))
        check('la tâche revenue d\'un rappel est marquée', pg.evaluate("()=>{ const e=document.querySelector('.tk[data-tk=\"prix|b2\"] .pt.rev'); return e?e.textContent:''; }") == 'revenue', pg.evaluate("()=>{ const e=document.querySelector('.tk[data-tk=\"prix|b2\"]'); return e?e.innerHTML.slice(0,300):'pas de tâche'; }"))
        # 3 nov. 2026 (Igal : « quand j'appuie sur Faire, je veux rester sur la même page »)
        # 7 nov. 2026 : sur « Recommander », le bouton principal met le parfum dans « Parfums à racheter » (_test_racheter.py) ;
        # la fiche s'ouvre toujours par-dessus, avec « Ouvrir »
        pg.locator('.tk[data-tk="rupture|b1"] button[data-fiche]').click(); pg.wait_for_timeout(1500)
        check('LE POINT — « Ouvrir » sur un parfum ouvre sa fiche PAR-DESSUS la liste (on reste sur Tâches)', pg.url.split('?')[0].endswith('taches.html') and pg.locator('#fv-ov iframe').count() == 1 and 'catalogue.html#cle=b1' in (pg.locator('#fv-ov iframe').get_attribute('src') or ''), pg.url)
        pg.evaluate("()=>{ document.getElementById('fv-ov').click(); }"); pg.wait_for_timeout(600)
        check('fermée, la liste est relue, toujours sur Tâches', pg.locator('#fv-ov').count() == 0 and pg.url.split('?')[0].endswith('taches.html') and pg.locator('#tk-corps .tk').count() == 5)
        a = pg.locator('.tk[data-tk="enligne|sitegros"] a.pri')
        check('« Faire » sur une tâche de page (mise en ligne par site) ouvre la page dans un NOUVEL onglet', a.get_attribute('href') == 'catalogue.html?diff=sitegros' and a.get_attribute('target') == '_blank')
        check('la tâche en attente avec sa date, la section ignorée OUVERTE en bas (Igal, 7 nov. 2026 : « ce qui est ignoré reste dans les tâches ignorées en dessous »)', 'Rappel le' in t and '11/08/26' in t and pg.locator('details.tk-ign').count() == 1 and pg.evaluate("()=>document.querySelector('details.tk-ign').open"), t[-300:])
        check('les compteurs : 2 urgentes, 3 à faire, 1 en attente', [x.strip() for x in pg.locator('#tk-tete .tk-kpi b').all_inner_texts()] == ['2', '3', '1'], pg.locator('#tk-tete').inner_text())
        print('3. les gestes partent au cockpit')
        pg.locator('.tk[data-tk="rupture|b1"] button[data-etat="faite"]').click(); pg.wait_for_timeout(500)
        check('LE POINT — « Fait » envoie l\'identifiant et l\'état', ETATS and ETATS[-1]['id'] == 'rupture|b1' and ETATS[-1]['etat'] == 'faite' and 'Ferrari' in ETATS[-1]['titre'], ETATS)
        pg.locator('.tk[data-tk="prix|b2"] button[data-etat="ignoree"]').click(); pg.wait_for_timeout(500)
        check('« Ignorer » aussi', ETATS[-1]['id'] == 'prix|b2' and ETATS[-1]['etat'] == 'ignoree', ETATS[-1])
        opts = pg.locator('.tk[data-tk="enligne|sitegros"] select[data-rappel] option').all_inner_texts()
        check('le rappel propose demain, 2, 5, 10 jours', [o.strip() for o in opts] == ['Plus tard…', 'demain', 'dans 2 jours', 'dans 5 jours', 'dans 10 jours'], opts)
        pg.locator('.tk[data-tk="enligne|sitegros"] select[data-rappel]').select_option('5'); pg.wait_for_timeout(500)
        check('LE POINT — le rappel dans 5 jours part avec jours=5', ETATS[-1]['id'] == 'enligne|sitegros' and ETATS[-1]['etat'] == 'attente' and ETATS[-1]['jours'] == 5, ETATS[-1])
        # la section ignorée est déjà ouverte (7 nov. 2026) : pas besoin de cliquer le résumé
        pg.locator('.tk[data-tk="publication|b5"] button[data-etat="a_faire"]').click(); pg.wait_for_timeout(500)
        check('« Remettre dans la liste » sur une ignorée', ETATS[-1]['id'] == 'publication|b5' and ETATS[-1]['etat'] == 'a_faire', ETATS[-1])
        pg.close()
        print('4. le mur, l\'anglais')
        pg = ouvre(role='commercial')
        check('un commercial voit le mur, pas la liste', pg.locator('.mur').count() == 1 and pg.locator('#tk-corps').count() == 0)
        pg.close()
        pg = ouvre(lg='en')
        # 8 nov. 2026 (Igal : « occupe-toi des traductions ») : les titres et détails des tâches sont réécrits par la page dans la langue de l'écran
        T = pg.locator('#tk-corps').inner_text()
        check('LE POINT — en anglais, les tâches elles-mêmes sont traduites : « Reorder Ferrari… », « Out of stock, and it sells 3.3 a week (42 sold over 90 days) », « Sold at a loss: Armaf… », « loss of », « Check its price », « Retry listing Hanae Mori… », « photo missing », « 2 in stock, 1.5 sold a week: nothing left in 9 days »',
              all(m in T for m in ['Reorder Ferrari Scuderia Black EDT', 'Out of stock, and it sells 3.3 a week (42 sold over 90 days).', 'Sold at a loss: Armaf Club De Nuit Bling EDP', 'loss of', 'Check its price.', 'Retry listing Hanae Mori HM EDP', 'photo missing', '2 in stock, 1.5 sold a week: nothing left in 9 days.']) and 'Recommander' not in T and 'Vendu à perte' not in T and 'Reprendre la mise en ligne' not in T, T[:700])
        t = pg.evaluate("()=>{ const m=document.querySelector('.main').cloneNode(true); m.querySelectorAll('[data-nolang]').forEach(e=>e.remove()); return m.innerText; }")
        FR = re.compile(r"\b(Tâches|À faire|urgentes|En attente|Fait|Ignorer|Plus tard|demain|dans \d+ jours|Rappel le|Faire|Ouvrir|Remettre)\b|[éèêàç]")
        t = t.replace('Léa', '')   # le prénom de l'assistante ne se traduit pas
        check('en anglais : pas un mot de français dans la page (hors textes venus du cockpit)', not FR.search(t), [l for l in t.split('\n') if FR.search(l)][:6])
        check('le menu dit « Tasks »', 'Tasks' in pg.locator('a.nv[href^="taches.html"]').inner_text())
        pg.close()
        # 7 nov. 2026 (Igal : « vérifier que c'est en anglais et espagnol aussi ») : le même tour en espagnol
        pg = ouvre(lg='es')
        T = pg.locator('#tk-corps').inner_text()
        check('LE POINT — en espagnol aussi : « Volver a pedir Ferrari… », « A cero, y se venden 3,3 por semana », « Vendido con pérdida: Armaf… », « pérdida de », « Revisa su precio », « Retomar la publicación de Hanae Mori… », « falta la foto », « nada en 9 días »',
              all(m in T for m in ['Volver a pedir Ferrari Scuderia Black EDT', 'A cero, y se venden 3,3 por semana', 'Vendido con pérdida: Armaf Club De Nuit Bling EDP', 'pérdida de', 'Revisa su precio.', 'Retomar la publicación de Hanae Mori HM EDP', 'falta la foto', 'nada en 9 días.']) and 'Recommander' not in T and 'Vendu à perte' not in T, T[:700])
        t = pg.evaluate("()=>{ const m=document.querySelector('.main').cloneNode(true); m.querySelectorAll('[data-nolang]').forEach(e=>e.remove()); return m.innerText; }").replace('Léa', '')
        FR2 = re.compile(r"\b(Tâches|À faire|En attente|Fait|Ignorer|Plus tard|demain|dans \d+ jours|Rappel le|Faire|Ouvrir|Remettre|Raison|ignorée|tâche)\b|[èêç]")   # « urgentes » et é/à existent en espagnol
        check('en espagnol : pas un mot de français dans la page (hors textes venus du cockpit)', not FR2.search(t) and 'Por hacer' in t and 'Ignorar' in t, [l for l in t.split('\n') if FR2.search(l)][:6])
        check('le menu dit « Tareas »', 'Tareas' in pg.locator('a.nv[href^="taches.html"]').inner_text())
        pg.close()
        print('4b. le code-barres et la contenance sur la ligne (Igal, 7 nov. 2026)')
        pg = ouvre()
        C0 = json.load(open(D / 'cat.json')); R0 = [r for r in C0 if r[0] and r[3] and len(str(r[13] or '')) > 6][0]
        LISTE['a_faire'].append({'id': 'prix|' + R0[15], 'type': 'prix', 'urgence': 'normale', 'titre': 'Marge trop faible : ' + str(R0[13]), 'detail': '8 %.', 'lien': '#', 'cle': R0[15], 'bc': str(R0[0]), 'etat': 'a_faire'})
        pg.reload(); pg.wait_for_timeout(3000)
        idp = pg.locator(f'.tk[data-tk="prix|{R0[15]}"] .tk-id').inner_text() if pg.locator(f'.tk[data-tk="prix|{R0[15]}"] .tk-id').count() else ''
        check('LE POINT — la ligne porte le code-barres et la contenance du parfum', str(R0[0]) in idp and str(R0[3]).strip() in idp, (idp, R0[0], R0[3]))
        LISTE['a_faire'].pop(); pg.close()
        print('5. le tableau de bord publie « pas en vente partout » pour le cockpit')
        pg = ouvre('tableau.html')
        C = json.load(open(D / 'cat.json')); A = [r for r in C if (r[6] or 0) > 0 and r[0] and r[0].isdigit()][0]
        pg.evaluate("S=>{ localStorage.setItem('site-stock-v1',JSON.stringify(S)); }", {A[0]: {'d': {'id': 1, 'q': 3, 'suivi': True}}, '_maj': {'d': '2026-11-01T08:00:00Z'}})
        pg.reload(); pg.wait_for_timeout(4200)
        pub = pg.evaluate("()=>JSON.parse(localStorage.getItem('diffusion-erp-v1')||'null')")
        check('LE POINT — diffusion-erp-v1 est publié : des parfums avec leur code, leur nom, leur stock et les sites où ils manquent', pub and isinstance(pub.get('L'), list) and len(pub['L']) > 10 and all(k in pub['L'][0] for k in ('cle', 'bc', 'nom', 'qte', 'manque', 'retire')) and pub['L'][0]['manque'], pub and (pub.get('n'), pub['L'][:1]))
        pg.close()
        check('aucune erreur JS', not err, err[:3])
        b.close()
finally:
    srv.terminate(); faux.shutdown()
print(f"\n{ok} ok, {len(ko)} KO", ko)
