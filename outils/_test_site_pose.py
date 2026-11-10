# Envoyer notre stock sur les sites — l'écran de relecture. Igal, 16 septembre 2026.
#
# Le cockpit a ses propres garde-fous (voir _t_woo_pose.mjs). Ici on protège ce
# que Sam VOIT avant d'appuyer, parce que c'est là qu'une erreur se rattrape :
#
#   1. le bouton n'existe pas tant que le cockpit n'a pas lu le site — sinon on
#      enverrait à l'aveugle ;
#   2. il n'existe pas non plus pour qui n'a pas le droit de compter ;
#   3. l'écran montre CE QUI VA CHANGER, ligne par ligne, avant tout envoi ;
#   4. une fiche qui ne compte pas ses unités sur le site n'est pas envoyée, et
#      une référence absente du site n'y est pas créée — et les deux sont
#      COMPTÉES à l'écran, pour qu'on sache pourquoi une ligne manque ;
#   5. les passages à zéro sont annoncés en rouge avant de partir ;
#   6. le site de détail et le site de gros ne se mélangent pas.
import pathlib, subprocess, time, socket, json
from playwright.sync_api import sync_playwright

D = pathlib.Path('/home/claude/catalogue')
ok = 0; ko = []
def check(n, c, i=''):
    global ok
    if c: ok += 1; print('  ok  ', n)
    else: ko.append(n); print('  KO  ', n, i)
def port_libre():
    s = socket.socket(); s.bind(('127.0.0.1', 0)); p = s.getsockname()[1]; s.close(); return p
CAT = json.load(open(D / 'cat.json'))
# trois références en stock chez nous, une à zéro
A, B, C = [r for r in CAT if (r[6] or 0) > 3][:3]
Z = next(r for r in CAT if (r[6] or 0) == 0)

# le rôle vient de la LISTE des comptes : la session seule ne suffit pas, l'outil
# la corrige d'après la liste (et c'est bien : un rôle bricolé dans le navigateur
# ne doit pas donner de droits)
SESS = """r=>{
  localStorage.setItem('sam-comptes-demo-v1','0');
  localStorage.removeItem('sam-roles-v1');
  localStorage.setItem('sam-comptes-v1', JSON.stringify(
    [{ident:'sam',nom:'Sam',role:r,actif:true,h:'x'}]));
  localStorage.setItem('sam-session-v1', JSON.stringify(
    {id:'sam',nom:'Sam',role:r,depuis:new Date().toISOString()}));
  localStorage.setItem('ck-token','jeton-de-test');
}"""

def site(qa, qb, qc, qz):
    """ce que le cockpit a déposé : le catalogue des deux sites"""
    return {
        A[0]: {'d': {'id': 101, 'q': qa, 'suivi': True,  'etat': 'instock', 'nom': 'A'},
               'g': {'id': 901, 'q': 0,  'suivi': True,  'etat': 'outofstock', 'nom': 'A'}},
        B[0]: {'d': {'id': 102, 'q': qb, 'suivi': False, 'etat': 'instock', 'nom': 'B'}},
        C[0]: {'d': {'id': 103, 'q': qc, 'suivi': True,  'etat': 'instock', 'nom': 'C'}},
        Z[0]: {'d': {'id': 104, 'q': qz, 'suivi': True,  'etat': 'instock', 'nom': 'Z'}},
        '_maj': {'d': '2026-09-16T08:00:00Z', 'g': '2026-09-16T08:00:00Z'},
    }

port = port_libre()
srv = subprocess.Popen(['python3', '-m', 'http.server', str(port), '--bind', '127.0.0.1'],
                       cwd=str(D), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1)
try:
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1500, 'height': 1000}); err = []
        pg.on('pageerror', lambda e: err.append(str(e)))
        pg.on('dialog', lambda d: d.accept())
        base = f'http://127.0.0.1:{port}/'

        # on intercepte l'appel au cockpit : rien ne part vraiment
        pg.add_init_script("""window.__envois=[]; window.__reponse={ok:true,ecrites:0,zeros:0,refus:[]};
          const vrai=window.fetch;
          window.fetch=function(u,o){
            const s=String(u);
            if(s.includes('/site/stock')){ window.__envois.push(JSON.parse(o.body));
              const r=window.__reponse;
              return Promise.resolve(new Response(JSON.stringify(r),
                {status:r.__status||200,headers:{'Content-Type':'application/json'}})); }
            return vrai.apply(this,arguments); };""")

        pg.goto(base + 'accueil.html'); pg.wait_for_timeout(500)
        pg.evaluate(SESS, 'patron')

        print("1. le bouton n'apparaît pas tant que le site n'a pas été lu")
        pg.evaluate("localStorage.setItem('site-stock-v1', JSON.stringify({}))")
        pg.goto(base + 'catalogue.html'); pg.wait_for_timeout(2600)
        check("pas de bouton sans catalogue du site — on n'écrit jamais à l'aveugle",
              pg.locator('#psite').is_hidden())

        print('2. avec le catalogue du site, le bouton est là')
        pg.evaluate("s=>localStorage.setItem('site-stock-v1', JSON.stringify(s))",
                    site(A[6] + 5, None, C[6], 4))
        pg.goto(base + 'catalogue.html'); pg.wait_for_timeout(2600)
        # 10 nov. 2026 (Igal : « je ne veux pas de bouton… automatiquement ») : le bouton est caché pour tous ; la fenêtre reste branchée
        check('LE POINT — le bouton « Mettre les sites à jour » n\'apparaît plus (prix et stock partent tout seuls), la fenêtre reste branchée', pg.locator('#psite').is_hidden() and pg.evaluate("()=>typeof document.getElementById('psite').onclick==='function'"))
        pg.evaluate("()=>document.getElementById('psite').onclick()"); pg.wait_for_timeout(700)
        check("la fenêtre s'ouvre", pg.locator('#psov.on').count() == 1)

        print('3. ce qui va changer est montré AVANT de partir')
        t = pg.locator('#psres').inner_text()
        check('le compte des références qui vont changer est annoncé', 'vont changer sur le site' in t, t[:200])
        lignes = pg.locator('#psres .pst tbody tr').count()
        check('la liste ligne par ligne est là', lignes >= 2, lignes)
        check("A y est : le site en annonce 5 de plus que nous",
              A[0] in pg.locator('#psres').inner_text(), t[:300])
        check("C n'y est PAS : le site annonce déjà notre quantité",
              C[0] not in pg.locator('#psres').inner_text())
        check('LE POINT — B n\'y est pas non plus : sa fiche ne compte pas ses unités',
              B[0] not in pg.locator('#psres').inner_text())
        check("et le pied de page COMPTE ce qui n'a pas été envoyé, au lieu de le taire",
              'ne compte pas ses unités' in t and 'déjà à la bonne quantité' in t, t[-260:])
        check('le passage à zéro est annoncé en rouge avant de partir',
              'passeront à zéro' in t and pg.locator('#psres .psz').count() >= 1, t[:300])

        print("4. ce qui part : la quantité seule, et rien d'autre")
        pg.click('#psok'); pg.wait_for_timeout(900)
        env = pg.evaluate('window.__envois')
        check('un seul envoi', len(env) == 1, env)
        e = env[0] if env else {}
        check('sur le site de détail par défaut', e.get('quel') == '', e)
        check('pas de confirmation forcée au premier essai', e.get('confirme') is False, e)
        bcs = [l['bc'] for l in e.get('lignes', [])]
        check("A et Z partent, B et C non", set(bcs) == {A[0], Z[0]}, bcs)
        check('chaque ligne ne porte que le code-barres et la quantité',
              all(sorted(l.keys()) == ['bc', 'q'] for l in e.get('lignes', [])), e.get('lignes'))
        qz = [l['q'] for l in e['lignes'] if l['bc'] == Z[0]][0]
        check('la quantité envoyée est la nôtre, pas celle du site', qz == 0, qz)

        print("5. LE GARDE-FOU du cockpit : le refus est reposé à l'écran")
        # on repart d'un écran neuf : l'envoi précédent a mis le site d'accord avec nous
        pg.evaluate("s=>localStorage.setItem('site-stock-v1', JSON.stringify(s))",
                    site(A[6] + 5, None, C[6], 4))
        pg.goto(base + 'catalogue.html'); pg.wait_for_timeout(2600)
        pg.evaluate("""window.__reponse={__status:409,confirmable:true,
          erreur:'Refusé : ce lot mettrait 40 références à zéro sur le site.'}; window.__envois=[];""")
        pg.evaluate("()=>document.getElementById('psite').onclick()"); pg.wait_for_timeout(600)
        pg.click('#psok'); pg.wait_for_timeout(1400)
        env = pg.evaluate('window.__envois')
        check('le refus est redemandé, puis renvoyé une seule fois avec confirmation',
              len(env) == 2 and env[0].get('confirme') is False and env[1].get('confirme') is True, len(env))
        check("LE POINT — un refus qui persiste APRÈS confirmation ne reboucle pas",
              len(env) == 2, len(env))
        check("et l'écran le dit au lieu de rester muet",
              'après confirmation' in pg.locator('#psmsg').inner_text(), pg.locator('#psmsg').inner_text())

        print('6. le site de gros ne se mélange pas au détail')
        pg.evaluate("window.__reponse={ok:true,ecrites:1,zeros:0,refus:[]}; window.__envois=[]")
        pg.locator('input[name="psq"][value="gros"]').check(); pg.wait_for_timeout(700)
        t = pg.locator('#psres').inner_text()
        check("seule A est sur le site de gros : les autres sont comptées comme absentes",
              'absentes de ce site' in t, t[-200:])
        pg.click('#psok'); pg.wait_for_timeout(900)
        env = pg.evaluate('window.__envois')
        check("l'envoi est bien marqué « gros »", env and env[0].get('quel') == 'gros', env)
        check("et ne porte que la référence présente sur ce site-là",
              env and [l['bc'] for l in env[0]['lignes']] == [A[0]], env)

        print('7. quand tout concorde, il n\'y a rien à envoyer')
        pg.evaluate("s=>localStorage.setItem('site-stock-v1', JSON.stringify(s))",
                    site(A[6], None, C[6], 0))
        pg.goto(base + 'catalogue.html'); pg.wait_for_timeout(2600)
        pg.evaluate("()=>document.getElementById('psite').onclick()"); pg.wait_for_timeout(700)
        check('on le dit, et le bouton est éteint',
              'Rien à envoyer' in pg.locator('#psres').inner_text() and pg.locator('#psok').is_disabled(),
              pg.locator('#psres').inner_text()[:160])

        print("8. les droits : l'entrepôt peut, le commercial non")
        for role, doit in (('entrepot', True), ('commercial', False), ('comptable', False)):
            pg.goto(base + 'accueil.html'); pg.wait_for_timeout(400)
            pg.evaluate(SESS, role)
            pg.evaluate("s=>localStorage.setItem('site-stock-v1', JSON.stringify(s))", site(99, None, 99, 99))
            pg.goto(base + 'catalogue.html'); pg.wait_for_timeout(2600)
            vu = pg.evaluate("()=>typeof document.getElementById('psite').onclick==='function'")
            check(f'{role} : ' + ('la fenêtre est branchée' if doit else 'pas de fenêtre'), vu == doit and pg.locator('#psite').is_hidden(), vu)

        check('aucune erreur JS', not err, err[:3])
        b.close()
finally:
    srv.terminate()
print(f"\n{ok} ok, {len(ko)} KO", ko)
