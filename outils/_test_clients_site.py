# LES ACHETEURS DES SITES DANS CLIENTS (16 nov. 2026 — Igal : « il n'y a pas toute la liste de clients… vérifier si c'est des clients
# sur le site wholesale ou sur le site retail »). Le cockpit relit toutes les commandes des deux sites (invités compris) ; ce test
# protège l'affichage :
#   1. LE POINT — un acheteur du site détail porte « Site détail » et le résumé de ses commandes (nombre, total, dernière) ;
#   2. LE POINT — un acheteur du site de gros porte « Site de gros », entre dans le filtre « Grossistes » et dans « Clients du site de gros » ;
#   3. un acheteur qui a commandé sur le site n'est pas « sans achat » ; un paiement échoué seul est dit tel quel ;
#   4. traduit en anglais et en espagnol ; aucune erreur JS.
import subprocess, time, socket
from playwright.sync_api import sync_playwright
D = '/home/claude/catalogue'
ok = 0; ko = []
def check(n, c, i=''):
    global ok
    if c: ok += 1; print('  ok  ', n)
    else: ko.append(n); print('  KO  ', n, str(i)[:600])
RET = [{'wid': None, 'nom': 'Ana Invitada', 'email': 'ana@ex.com', 'tel': '3055550001', 'src': 'site', 'invite': True, 'siteCmd': {'cmd': 2, 'total': 150.5, 'prem': '2024-03-01', 'der': '2025-06-01', 'tent': 1}},
       {'wid': None, 'nom': 'Bob Fallido', 'email': 'bob@ex.com', 'src': 'site', 'invite': True, 'siteCmd': {'cmd': 0, 'total': 0, 'prem': '', 'der': '', 'tent': 1}}]
CLI = {'Nuevo Mayorista': {'nom': 'Nuevo Mayorista', 'email': 'nuevo@ex.com', 'src': 'site-gros', 'siteCmd': {'cmd': 1, 'total': 400, 'prem': '2026-10-05', 'der': '2026-10-05', 'tent': 0}}}
s = socket.socket(); s.bind(('127.0.0.1', 0)); port = s.getsockname()[1]; s.close()
srv = subprocess.Popen(['python3', '-m', 'http.server', str(port), '--bind', '127.0.0.1'], cwd=D, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)
SESS = """([R,C,lg])=>{ localStorage.clear(); localStorage.setItem('sam-comptes-demo-v1','0');
  localStorage.setItem('sam-session-v1',JSON.stringify({id:'sam',nom:'Sam',role:'patron',depuis:new Date().toISOString()}));
  localStorage.setItem('langue-v1',lg); localStorage.setItem('retail-local-v1',JSON.stringify(R)); localStorage.setItem('clients-v1',JSON.stringify(C)); }"""
try:
    with sync_playwright() as p:
        b = p.chromium.launch(); err = []
        def ouvre(lg='fr'):
            pg = b.new_page(viewport={'width': 1500, 'height': 1000}); pg.on('pageerror', lambda e: err.append(str(e)))
            pg.goto(f'http://127.0.0.1:{port}/accueil.html'); pg.wait_for_timeout(300); pg.evaluate(SESS, [RET, CLI, lg])
            pg.goto(f'http://127.0.0.1:{port}/clients.html'); pg.wait_for_timeout(2200); return pg
        pg = ouvre()
        row = lambda n: pg.locator(f'tr[data-c="{n}"]').inner_text() if pg.locator(f'tr[data-c="{n}"]').count() else ''
        t = row('Ana Invitada')
        check('LE POINT — l\'acheteuse du site détail : « Site détail », 2 commandes, 151 $ (arrondi), dernière 06/01/25', 'Site détail' in t and '2 commande(s)' in t and '151' in t and '06/01/25' in t, t)
        t = row('Nuevo Mayorista')
        check('LE POINT — l\'acheteur du site de gros : « Site de gros » et ses commandes', 'Site de gros' in t and '1 commande(s)' in t, t)
        check('un paiement échoué seul est dit tel quel', 'paiement échoué seulement' in row('Bob Fallido'), row('Bob Fallido'))
        def filtre(v):
            pg.select_option('#typ', v); pg.wait_for_timeout(300)
            return pg.evaluate("()=>[...document.querySelectorAll('tr[data-c]')].map(x=>x.dataset.c)")
        g = filtre('gros'); check('LE POINT — le filtre « Grossistes » contient l\'acheteur du site de gros', 'Nuevo Mayorista' in g and 'Ana Invitada' not in g, g)
        g = filtre('sitegros'); check('le filtre « Clients du site de gros »', g == ['Nuevo Mayorista'], g)
        g = filtre('site'); check('le filtre « Clients du site détail »', 'Ana Invitada' in g and 'Nuevo Mayorista' not in g, g)
        g = filtre('sans'); check('un acheteur du site n\'est pas « sans achat » ; celui qui n\'a qu\'un paiement échoué l\'est', 'Ana Invitada' not in g and 'Nuevo Mayorista' not in g and 'Bob Fallido' in g, g)
        pg.close()
        for lg, mot in (('en', 'Retail site'), ('es', 'Sitio minorista')):
            pg = ouvre(lg); t = row('Ana Invitada')
            check(f'traduit ({lg})', mot in t and 'Site détail' not in t, t); pg.close()
        check('aucune erreur JS', not err, err[:3])
        b.close()
finally:
    srv.terminate()
print(f'{ok} ok, {len(ko)} KO')
raise SystemExit(1 if ko else 0)
