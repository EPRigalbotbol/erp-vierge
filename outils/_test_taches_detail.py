# LE DÉTAIL DE LA VENTE SOUS UNE TÂCHE DE PRIX (15 nov. 2026 — Igal, sur « Vendu à perte : … vendu 0 $ » : « sur les tâches j'ai
# besoin d'avoir plus de détails »). Ce test protège :
#   1. LE POINT — sous la tâche : n° de facture, jour et heure, canal, client, paiement, et le ticket (lignes, flacons, total) ;
#   2. LE POINT — un parfum à 0 $ dans un ticket payé se lit tout de suite : « la seule ligne à 0 $ du ticket : un cadeau ? » ;
#   3. les plus grosses lignes du ticket, et un lien vers la facture entière (ventes.html#doc=…) ;
#   4. la vente est retrouvée par son identifiant (fid, cockpit ck152) ou, pour une tâche d'avant, par jour/canal/parfum/prix ;
#      deux ventes possibles : rien n'est deviné ;
#   5. en anglais et en espagnol, tout est traduit ; aucune erreur JS.
import pathlib, subprocess, time, socket, json, re, threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from playwright.sync_api import sync_playwright
D = pathlib.Path('/home/claude/catalogue'); ok = 0; ko = []
def check(n, c, i=''):
    global ok
    if c: ok += 1; print('  ok  ', n)
    else: ko.append(n); print('  KO  ', n, str(i)[:600])
C = json.load(open(D / 'cat.json'))
R = [r for r in C if r[15] and (r[12] or 0) > 0][:4]
L0 = [{'cle': R[0][15], 'bc': R[0][0], 'ref': 'Parfum Cadeau', 'q': 1, 'p': 0},
      {'cle': R[1][15], 'bc': R[1][0], 'ref': 'Parfum Gros A', 'q': 3, 'p': 120},
      {'cle': R[2][15], 'bc': R[2][0], 'ref': 'Parfum Petit B', 'q': 1, 'p': 15}]
F = [{'id': 'fx1', 'num': 'ls-uuid-1', 'sens': 'vente', 'canal': 'Caisse Lightspeed', 'auto': 'lightspeed', 'tiers': 'ADRIANA TEST', 'd': '2026-11-14', 'h': '15:17',
      'lignes': L0, 'montant': 375, 'paie': {'especes': 375, 'carte': 0, 'autre': 0}, 'par': 'Sam', 'doc': {'num': 'PT-2026-1234', 'total': 375}},
     {'id': 'fx2', 'num': 'ls-uuid-2', 'sens': 'vente', 'canal': 'Gros', 'tiers': 'Carmen', 'd': '2026-11-13', 'h': '10:05',
      'lignes': [{'cle': R[3][15], 'bc': R[3][0], 'ref': 'Parfum Perte C', 'q': 2, 'p': 10}], 'montant': 20, 'paie': {'especes': 0, 'carte': 20, 'autre': 0}, 'par': 'Sam', 'doc': {'num': 'PT-2026-1235', 'total': 20}}]
VTE = lambda **k: dict({'pct': None, 'n': 1, 'perte': True, 'com': 0, 'carte': 0, 'envoi': 0, 'port': 0}, **k)
ETATS = []
LISTE = {'jour': '2026-11-15', 'rappels': [1, 2, 5, 10], 'urgentes': 2, 'faites': 0, 'attente': [], 'ignorees': [], 'a_faire': [
  {'id': 'prix|' + R[0][15], 'type': 'prix', 'urgence': 'haute', 'titre': 'Vendu à perte : Parfum Cadeau', 'detail': '…', 'lien': '#', 'cle': R[0][15], 'bc': str(R[0][0]), 'etat': 'a_faire',
   'ref': 'Parfum Cadeau', 'margeMin': 10, 'vente': VTE(fid='fx1', d='2026-11-14', canal='Caisse Lightspeed', p=0, pa=23.5, mg=-23.5, q=1)},
  # une tâche d'avant ck152 : pas de fid, la vente est retrouvée par jour, canal, parfum, prix et quantité
  {'id': 'prix|' + R[3][15], 'type': 'prix', 'urgence': 'haute', 'titre': 'Vendu à perte : Parfum Perte C', 'detail': '…', 'lien': '#', 'cle': R[3][15], 'bc': str(R[3][0]), 'etat': 'a_faire',
   'ref': 'Parfum Perte C', 'margeMin': 10, 'vente': VTE(d='2026-11-13', canal='Gros', p=10, pa=30, mg=-40, q=2)}]}
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
s = socket.socket(); s.bind(('127.0.0.1', 0)); port = s.getsockname()[1]; s.close()
s = socket.socket(); s.bind(('127.0.0.1', 0)); pck = s.getsockname()[1]; s.close()
srv = subprocess.Popen(['python3', '-m', 'http.server', str(port), '--bind', '127.0.0.1'], cwd=str(D), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
faux = HTTPServer(('127.0.0.1', pck), Faux); threading.Thread(target=faux.serve_forever, daemon=True).start(); time.sleep(0.8)
SESS = """([lg,F])=>{ localStorage.clear(); localStorage.setItem('sam-comptes-demo-v1','0');
  localStorage.setItem('sam-session-v1',JSON.stringify({id:'sam',nom:'Sam',role:'patron',depuis:new Date().toISOString()}));
  localStorage.setItem('langue-v1',lg); localStorage.setItem('ck-token','jeton-test'); localStorage.setItem('factures-v1',JSON.stringify(F)); }"""
try:
    with sync_playwright() as p:
        b = p.chromium.launch(); err = []
        def ouvre(lg='fr', F=F):
            pg = b.new_page(viewport={'width': 1400, 'height': 1000}); pg.on('pageerror', lambda e: err.append(str(e)))
            pg.add_init_script(f"window.COCKPIT_URL='http://127.0.0.1:{pck}';")
            base = f'http://127.0.0.1:{port}/'
            pg.goto(base + 'accueil.html'); pg.wait_for_timeout(300); pg.evaluate(SESS, [lg, F])
            pg.goto(base + 'taches.html'); pg.wait_for_timeout(3200); return pg
        det = lambda pg, cle: pg.evaluate("c=>{ const e=document.querySelector('.tk-px[data-px=\"'+c+'\"] .tk-det'); return e?e.textContent.replace(/\\s+/g,' '):''; }", cle)
        pg = ouvre()
        t = det(pg, R[0][15])
        check('LE POINT — sous la tâche : n° de facture, jour et heure, canal, client, paiement', all(x in t for x in ['PT-2026-1234', '11/14/26 à 15:17', 'Caisse Lightspeed', 'ADRIANA TEST', 'espèces 375,00']), t)
        check('LE POINT — le ticket : 3 lignes, 5 flacons, total 375 $', '3 lignes, 5 flacons, total 375,00' in t, t)
        check('LE POINT — le parfum à 0 $ se lit tout de suite : « la seule ligne à 0 $ du ticket : un cadeau ? »', 'seule ligne à 0 $ du ticket : un cadeau ?' in t, t)
        check('vente reçue de la caisse : « reçue automatiquement »', 'reçue automatiquement' in t, t)
        check('les plus grosses lignes du ticket, la plus grosse d\'abord', t.find('Parfum Gros A') >= 0 and t.find('Parfum Gros A') < t.find('Parfum Petit B'), t)
        href = pg.evaluate("c=>{ const a=document.querySelector('.tk-px[data-px=\"'+c+'\"] .tk-det a'); return a?a.getAttribute('href'):''; }", R[0][15])
        check('un lien ouvre la facture entière', 'ventes.html' in href and href.endswith('#doc=fx1'), href)
        t2 = det(pg, R[3][15])
        check('LE POINT — tâche sans identifiant (d\'avant) : la vente est retrouvée par jour, canal, parfum, prix et quantité', 'PT-2026-1235' in t2 and 'Carmen' in t2 and 'carte 20,00' in t2 and 'un cadeau' not in t2, t2)
        pg.close()
        F2 = F + [dict(F[1], id='fx3', doc={'num': 'PT-2026-1236', 'total': 20})]
        pg = ouvre(F=F2)
        check('deux ventes possibles pour une tâche sans identifiant : rien n\'est deviné', det(pg, R[3][15]) == '' and 'PT-2026-1234' in det(pg, R[0][15]), det(pg, R[3][15]))
        pg.close()
        for lg, mots, fr in (('en', ['at 15:17', 'Customer', 'paid cash', '3 lines, 5 bottles', 'only $0 line on the ticket: a gift?', 'received automatically', 'See the full invoice'], ['Client :', 'flacons', 'cadeau', 'reçue']),
                             ('es', ['a las 15:17', 'Cliente', 'pagado efectivo', '3 líneas, 5 frascos', 'única línea a 0 $ del ticket: ¿un regalo?', 'recibida automáticamente', 'Ver la factura completa'], ['Client :', 'flacons', 'cadeau', 'reçue'])):
            pg = ouvre(lg=lg); t = det(pg, R[0][15])
            check(f'{lg} : le détail est traduit', all(x in t for x in mots) and not any(x in t for x in fr), [x for x in mots if x not in t] + [x for x in fr if x in t] + [t[:300]])
            pg.close()
        check('aucune erreur JS', not err, err[:3])
        b.close()
finally:
    srv.terminate(); faux.shutdown()
print(f'\n{ok} ok, {len(ko)} KO', ko); raise SystemExit(1 if ko else 0)
