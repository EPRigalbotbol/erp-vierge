# LES ACHETEURS DES SITES DANS CLIENTS (16 nov. 2026 — Igal : « il n'y a pas toute la liste de clients… vérifier si c'est des clients
# sur le site wholesale ou sur le site retail »). Le cockpit relit toutes les commandes des deux sites (invités compris) ; ce test
# protège l'affichage :
#   1. LE POINT — un acheteur du site détail porte « Site détail » et le résumé de ses commandes (nombre, total, dernière) ;
#   2. LE POINT — un acheteur du site de gros porte « Site de gros », entre dans le filtre « Grossistes » et dans « Clients du site de gros » ;
#   3. un acheteur qui a commandé sur le site n'est pas « sans achat » ; un paiement échoué seul est dit tel quel ;
#   4. traduit en anglais et en espagnol ; aucune erreur JS ;
#   5. (16 nov. 2026, Igal : « deux sous-rubriques, wholesale et retail… pour gérer le mailing ») LE POINT — Wholesale et Retail
#      séparent les clients ; un compte sans commande est dit « jamais commandé » (cas de Valérie Gilbert).
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
CLI = {'Nuevo Mayorista': {'nom': 'Nuevo Mayorista', 'email': 'nuevo@ex.com', 'src': 'site-gros', 'siteCmd': {'cmd': 1, 'total': 400, 'prem': '2026-10-05', 'der': '2026-10-05', 'tent': 0}},
       'Valerie Compte': {'nom': 'Valerie Compte', 'email': 'valerie@ex.com', 'src': 'site-gros', 'depuis': '2026-05-03'}}
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
        noms = lambda: pg.evaluate("()=>[...document.querySelectorAll('tr[data-c]')].map(x=>x.dataset.c)")
        def onglet(o): pg.click(f'#cl-ong button[data-o="{o}"]'); pg.wait_for_timeout(300)
        def filtre(v):
            pg.select_option('#typ', v); pg.wait_for_timeout(300); return noms()
        # Wholesale (ouvert par défaut)
        L = noms()
        check('LE POINT — Wholesale par défaut : les clients du site de gros, pas ceux du site détail', 'Nuevo Mayorista' in L and 'Valerie Compte' in L and 'Ana Invitada' not in L and 'Bob Fallido' not in L, L)
        t = row('Nuevo Mayorista')
        check('LE POINT — l\'acheteur du site de gros : « Site de gros » et ses commandes', 'Site de gros' in t and '1 commande(s)' in t and 'Site détail' not in t, t)
        t = row('Valerie Compte')
        check('LE POINT — un compte du site de gros sans commande est dit « jamais commandé » (plus seulement « Site de gros »)', 'jamais commandé' in t.lower() and 'commande(s)' not in t, t)
        check('le filtre « Ont commandé sur le site de gros »', filtre('sitegros') == ['Nuevo Mayorista'], noms())
        check('le filtre « Compte sur le site de gros, jamais commandé »', filtre('compteg') == ['Valerie Compte'], noms())
        check('le filtre ne propose que les choix Wholesale', pg.evaluate("()=>[...document.querySelectorAll('#typ option')].filter(o=>!o.disabled).map(o=>o.value).join(',')") == ',vip,gros,sitegros,compteg,sans', '')
        filtre('')
        # Retail
        onglet('detail')
        L = noms()
        check('LE POINT — Retail : les clients du site détail, pas ceux du site de gros', 'Ana Invitada' in L and 'Nuevo Mayorista' not in L and 'Valerie Compte' not in L, L)
        t = row('Ana Invitada')
        check('LE POINT — l\'acheteuse du site détail : « Site détail », 2 commande(s), 151 $ (arrondi), dernière 06/01/25 ; 2 achats ≈ (d\'après le site)', 'Site détail' in t and '2 commande(s)' in t and '151' in t and '06/01/25' in t and '2 ≈' in t, t)
        check('un paiement échoué seul est dit tel quel', 'paiement échoué seulement' in row('Bob Fallido'), row('Bob Fallido'))
        g = filtre('site'); check('le filtre « Ont commandé sur le site détail »', 'Ana Invitada' in g and 'Bob Fallido' not in g, g)
        g = filtre('sans'); check('un acheteur du site n\'est pas « sans achat » ; celui qui n\'a qu\'un paiement échoué l\'est', 'Ana Invitada' not in g and 'Bob Fallido' in g, g)
        check('l\'adresse garde la sous-rubrique (#retail)', 'retail' in pg.evaluate('location.hash'), '')
        txt = pg.locator('#cl-ong').inner_text()
        check('les onglets Wholesale / Retail / Price list et leurs nombres', 'Wholesale' in txt and 'Retail' in txt and 'Price list' in txt, txt)
        pg.close()
        pg = ouvre(); pg.goto(pg.url.split('#')[0] + '#retail'); pg.reload(); pg.wait_for_timeout(2200)
        check('clients.html#retail ouvre directement Retail', 'Ana Invitada' in noms() and 'Nuevo Mayorista' not in noms(), noms()); pg.close()
        for lg, mot, op in (('en', 'Retail site', 'Ordered on the retail site'), ('es', 'Sitio minorista', 'Pidieron en el sitio minorista')):
            pg = ouvre(lg); onglet('detail'); t = row('Ana Invitada')
            ops = pg.evaluate("()=>[...document.querySelectorAll('#typ option')].map(o=>o.textContent).join('|')")
            check(f'traduit ({lg})', mot in t and 'Site détail' not in t and op in ops and 'jamais' not in ops, [t, ops]); pg.close()
        check('aucune erreur JS', not err, err[:3])
        b.close()
finally:
    srv.terminate()
print(f'{ok} ok, {len(ko)} KO')
raise SystemExit(1 if ko else 0)
