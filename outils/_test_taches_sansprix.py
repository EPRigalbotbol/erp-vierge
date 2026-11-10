# LES PRODUITS SANS PRIX DES SITES : UNE TÂCHE, RÉGLÉE SUR PLACE (Igal, 10 nov. 2026 : prix et stock automatiques, « fais ce qu'il y a
# de mieux » — le bouton « Mettre les sites à jour » n'apparaît plus ; son seul travail qui restait, retirer de la vente les fiches à
# 0,00 $, devient une tâche). Ce test protège :
#   1. LE POINT — la tâche liste les produits sans prix d'un site et porte le bouton « Retirer de la vente » ;
#   2. LE POINT — un clic envoie au cockpit les codes à retirer (brouillon), sur le bon site ; le journal le dit ;
#   3. en anglais et en espagnol, la tâche et son bouton sont traduits.
import pathlib, subprocess, time, socket, json, threading, datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
from playwright.sync_api import sync_playwright
D = pathlib.Path('/home/claude/catalogue'); ok = 0; ko = []
def check(n, c, i=''):
    global ok
    if c: ok += 1; print('  ok  ', n)
    else: ko.append(n); print('  KO  ', n, str(i)[:500])
CAT = json.load(open(D / 'cat.json'))
A, B = [r for r in CAT if r[7] and r[8] and r[12] and r[0] and str(r[0]).isdigit() and len(str(r[0])) >= 12 and len(str(r[13] or '')) > 8 and (r[6] or 0) > 2][:2]
def nom(r): return ((r[2] or '') + ' ' + (r[13] or '')).strip()
AUJ = datetime.date.today(); J = lambda n: (AUJ - datetime.timedelta(days=n)).isoformat()
ETATS = []; AJOUTS = []; CREES = []; STATUT = []
LISTE = {'jour': J(0), 'rappels': [1, 2, 5, 10], 'urgentes': 1, 'faites': 0, 'attente': [], 'ignorees': [],
  'a_faire': [{'id': 'sansprix|d', 'type': 'sansprix', 'urgence': 'haute', 'quel': '', 'site': 'perfumestrade.com', 'n': 2, 'enStock': 1, 'etat': 'a_faire',
    'titre': 'Retirer de la vente 2 produits sans prix sur perfumestrade.com', 'detail': 'Ces fiches du site sont à 0,00 $.',
    'produits': [{'bc': '1234567890123', 'nom': 'Parfum A sans prix', 'q': 3}, {'bc': '1234567890124', 'nom': 'Parfum B sans prix', 'q': 0}]}]}
class Faux(BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def _rep(self, code, obj):
        b = json.dumps(obj).encode(); self.send_response(code); self.send_header('Content-Type', 'application/json'); self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Headers', 'Authorization, Content-Type'); self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, OPTIONS'); self.end_headers(); self.wfile.write(b)
    def do_OPTIONS(self): self._rep(200, {})
    def do_GET(self):
        if self.path.endswith('/galou/taches'): return self._rep(200, LISTE)
        if self.path.endswith('/galou/etat'): return self._rep(200, {'pret': True, 'voix': False, 'voitMarge': True})
        if self.path.endswith('/shopify/droits'): return self._rep(200, {'stock': True, 'ecriture': True, 'pub': True})
        return self._rep(200, {})
    def do_POST(self):
        n = int(self.headers.get('Content-Length') or 0); corps = json.loads(self.rfile.read(n) or b'{}')
        if self.path.endswith('/galou/taches/etat'): ETATS.append(corps); return self._rep(200, {'ok': True})
        if self.path.endswith('/site/statut'): STATUT.append(corps); return self._rep(200, {'ok': True, 'ecrites': len(corps.get('bcs', [])), 'refus': []})
        if self.path.endswith('/shopify/stock-ajoute'):
            AJOUTS.append(corps)
            # F-10 (8 nov. 2026) : le parfum n'est pas chez Perfume City au premier envoi ; une fois créé (/shopify/cree), il passe
            if corps.get('cle') == 'f10' and not CREES: return self._rep(200, {'ok': True, 'lignes': [{'bc': x['bc'], 'nom': x.get('nom'), 'etat': 'absent', 'raison': "ce parfum n'est pas (encore) chez Perfume City"} for x in corps.get('items', [])]})
            return self._rep(200, {'ok': True, 'lignes': [{'bc': x['bc'], 'nom': x.get('nom'), 'etat': 'ok', 'avant': 0, 'apres': x['ajout']} for x in corps.get('items', [])]})
        if self.path.endswith('/cree'):
            CREES.append(corps); L = corps.get('lignes') or corps.get('produits') or []
            return self._rep(200, {'ok': True, 'faites': [{'bc': x.get('bc'), 'id': 900 + i, 'statut': 'publish', 'prix': x.get('prix') or x.get('v')} for i, x in enumerate(L)], 'refus': []})
        return self._rep(200, {'ok': True})
    def do_PUT(self): n = int(self.headers.get('Content-Length') or 0); self.rfile.read(n); return self._rep(200, {'ok': True, 'ver': 1})
s = socket.socket(); s.bind(('127.0.0.1', 0)); port = s.getsockname()[1]; s.close()
s = socket.socket(); s.bind(('127.0.0.1', 0)); pck = s.getsockname()[1]; s.close()
srv = subprocess.Popen(['python3', '-m', 'http.server', str(port), '--bind', '127.0.0.1'], cwd=str(D), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
faux = HTTPServer(('127.0.0.1', pck), Faux); threading.Thread(target=faux.serve_forever, daemon=True).start(); time.sleep(0.8)
FACT = [{'id': 'f9', 'num': 'F-9', 'sens': 'achat', 'tiers': 'MTZ', 'd': J(1), 'stock': True, 'pcShopify': {'etat': 'echec', 'raison': 'hors ligne'},
         'lignes': [{'cle': A[15], 'bc': str(A[0]), 'ref': nom(A), 'q': 6, 'pc': 6, 'p': 20}]},
        {'id': 'f10', 'num': 'F-10', 'sens': 'achat', 'tiers': 'MTZ', 'd': J(1), 'stock': True, 'pcShopify': {'etat': 'partiel', 'lignes': [{'bc': str(B[0]), 'etat': 'absent'}]},
         'lignes': [{'cle': B[15], 'bc': str(B[0]), 'ref': nom(B), 'q': 4, 'pc': 2, 'p': 18}]}]
EXP = [{'_i': 'e1', 'src': 'woocommerce', 'num': '21330', 'client': 'Robert', 'd': J(3), 'h': '10:12', 'recu': J(3) + 'T15:12:00Z', 'total': 40, 'ville': 'Miami', 'pays': 'US',
        'lignes': [{'cle': B[15], 'bc': str(B[0]), 'des': nom(B), 'q': 1, 'p': 40, 'ref': nom(B)}], 'montant': 40, 'arrive': J(3) + 'T15:13:00Z', 'statut': 'attente'}]
FILE = [{'_i': 'v1', 'src': 'woocommerce', 'num': '21340', 'client': 'Carmen', 'd': J(0), 'h': '09:00', 'total': 30, 'lignes': [{'bc': '0000000000019', 'des': 'Mystery Perfume Z', 'q': 1, 'p': 30}]}]
SESS = """([lg,F,E,FI])=>{ localStorage.clear(); localStorage.setItem('sam-comptes-demo-v1','0');
  localStorage.setItem('sam-comptes-v1',JSON.stringify([{ident:'sam',nom:'Sam',role:'patron',actif:true,h:'x'}]));
  localStorage.setItem('sam-session-v1',JSON.stringify({id:'sam',nom:'Sam',role:'patron',depuis:new Date().toISOString()}));
  localStorage.setItem('langue-v1',lg); localStorage.setItem('ck-token','jeton-test'); localStorage.setItem('reglages-v1',JSON.stringify({societe:'DASY LLC'}));
  localStorage.setItem('factures-v1',JSON.stringify(F)); localStorage.setItem('expeditions-v1',JSON.stringify(E)); localStorage.setItem('caisse-file-v1',JSON.stringify(FI));
  localStorage.setItem('shopify-pc-prix-v1',JSON.stringify({'5550001':[1,2]})); localStorage.setItem('site-stock-v1',JSON.stringify({})); }"""
try:
    with sync_playwright() as p:
        b = p.chromium.launch(); err = []
        pg = b.new_page(viewport={'width': 1500, 'height': 1000}); pg.on('pageerror', lambda e: err.append(str(e))); pg.on('dialog', lambda d: d.accept())
        pg.add_init_script(f"window.COCKPIT_URL='http://127.0.0.1:{pck}';")
        base = f'http://127.0.0.1:{port}/'
        def prepare(lg='fr'):
            pg.goto(base + 'accueil.html'); pg.wait_for_timeout(300); pg.evaluate(SESS, [lg, [], [], []])
            pg.goto(base + 'taches.html'); pg.wait_for_timeout(3200)
        prepare()
        T = '.tk[data-tk="sansprix|d"]'
        txt = pg.inner_text(T) if pg.locator(T).count() else ''
        check('LE POINT — la tâche est là, avec les produits sans prix et le bouton « Retirer de la vente »', 'Parfum A sans prix' in txt and pg.locator(T + ' button[data-spx]').count() == 1, txt[:300])
        pg.click(T + ' button[data-spx]'); pg.wait_for_timeout(1500)
        check('LE POINT — un clic : le cockpit reçoit les deux codes à retirer de la vente sur le site détail', len(STATUT) == 1 and STATUT[0].get('sens') == 'retirer' and STATUT[0].get('quel') == '' and sorted(STATUT[0].get('bcs', [])) == ['1234567890123', '1234567890124'], STATUT)
        J0 = pg.evaluate("()=>lit('crm-journal-v1',[]).map(j=>j.lib)")
        check('le journal le dit', any('sans prix retirée' in l and 'perfumestrade.com' in l for l in J0), J0[-3:])
        for lg, mots in (('en', ['Take 2 products with no price off sale on perfumestrade.com', 'Take off sale', 'in stock']), ('es', ['Retirar de la venta 2 productos sin precio en perfumestrade.com', 'Retirar de la venta', 'en stock'])):
            prepare(lg); t = pg.inner_text(T) if pg.locator(T).count() else ''
            check(f'{lg} : la tâche et son bouton sont traduits', all(m in t for m in mots), t[:300])
        check('aucune erreur JS', not err, err[:3])
        b.close()
finally:
    srv.terminate(); faux.shutdown()
print(f'\n{ok} ok, {len(ko)} KO', ko); raise SystemExit(1 if ko else 0)
