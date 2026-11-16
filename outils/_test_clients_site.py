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
       'Valerie Compte': {'nom': 'Valerie Compte', 'email': 'valerie@ex.com', 'src': 'site-gros', 'depuis': '2026-05-03'},
       'valerygilbert1989': {'nom': 'valerygilbert1989', 'email': 'valerygilbert1989@ex.com'},
       'Sans Coordonnees': {'nom': 'Sans Coordonnees'},
       'Parfums360': {'nom': 'Parfums360', 'email': 'p360@ex.com'}}
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
        check('le filtre ne propose que les choix Wholesale', pg.evaluate("()=>[...document.querySelectorAll('#typ option')].filter(o=>!o.disabled).map(o=>o.value).join(',')") == ',vip,gros,sitegros,compteg,sans,acompl', '')
        filtre('')
        # 6. fiche à compléter, non diffusable (Igal, 16 nov. 2026)
        filtre('acompl'); t1, t2 = row('valerygilbert1989'), row('Sans Coordonnees'); filtre(''); t3 = row('Nuevo Mayorista')
        check('LE POINT — en rouge « Fiche à compléter · non diffusable » : un nom qui est un identifiant, une fiche sans email ni téléphone ; pas sur une fiche complète', 'non diffusable' in t1.lower() and 'non diffusable' in t2.lower() and 'non diffusable' not in t3.lower(), [t1, t2, t3])
        g = filtre('acompl'); check('le filtre « Fiches à compléter » (même une fiche vide)', 'Sans Coordonnees' in g and 'valerygilbert1989' in g and 'Nuevo Mayorista' not in g and 'Valerie Compte' not in g and 'Parfums360' not in g, g)
        filtre('')
        pg.click('#diff'); pg.wait_for_timeout(500)
        ti = pg.locator('#ctg-titre').inner_text(); li = pg.locator('#ctg-liste').inner_text()
        check('LE POINT — la liste de diffusion laisse de côté les fiches à compléter et le dit', 'valerygilbert1989' not in li and 'Nuevo Mayorista' in li and 'fiche(s) à compléter non incluse(s)' in ti and 'wholesale.perfumestrade.com' in ti, [ti, li[:200]])
        pg.click('#ctg-x'); pg.wait_for_timeout(300)
        filtre('acompl'); pg.locator('tr[data-c="Sans Coordonnees"]').click(); pg.wait_for_timeout(500)
        d = pg.locator('#dco').inner_text()
        check('la fiche dit ce qui manque', 'il manque' in d.lower() and 'téléphone' in d, d)
        pg.keyboard.press('Escape'); pg.wait_for_timeout(300); filtre('')
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
        check('LE POINT — les onglets portent le nom des sites : wholesale.perfumestrade.com / perfumestrade.com / Amazon / Price list', 'wholesale.perfumestrade.com' in txt and '\nperfumestrade.com' in '\n'+txt.replace('wholesale.perfumestrade.com','') and 'Amazon' in txt and 'Price list' in txt, txt)
        pg.close()
        pg = ouvre(); pg.goto(pg.url.split('#')[0] + '#retail'); pg.reload(); pg.wait_for_timeout(2200)
        check('clients.html#retail ouvre directement Retail', 'Ana Invitada' in noms() and 'Nuevo Mayorista' not in noms(), noms()); pg.close()
        for lg, mot, op in (('en', 'Retail site', 'Ordered on the retail site'), ('es', 'Sitio minorista', 'Pidieron en el sitio minorista')):
            pg = ouvre(lg); onglet('detail'); t = row('Ana Invitada')
            ops = pg.evaluate("()=>[...document.querySelectorAll('#typ option')].map(o=>o.textContent).join('|')")
            check(f'traduit ({lg})', mot in t and 'Site détail' not in t and op in ops and 'jamais' not in ops, [t, ops])
            pg.click('#cl-ong button[data-o="gros"]'); pg.wait_for_timeout(300); pg.select_option('#typ', 'acompl'); pg.wait_for_timeout(300); t = row('Sans Coordonnees').lower()
            check(f'« fiche à compléter » traduit ({lg})', ('incomplete record' if lg == 'en' else 'ficha incompleta') in t and 'diffusable' not in t, t); pg.close()
        check('aucune erreur JS', not err, err[:3])
        b.close()
finally:
    srv.terminate()
print(f'{ok} ok, {len(ko)} KO')
raise SystemExit(1 if ko else 0)
