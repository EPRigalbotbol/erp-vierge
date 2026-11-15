# Igal, 13 oct. 2026 : « en sous-rubrique de Clients, je veux les clients VIP ».
# Une ligne « Clients VIP » sous « Clients » dans le menu de gauche -> la liste des favoris.
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
SESS = "localStorage.setItem('sam-session-v1', JSON.stringify({id:'sam',nom:'Sam',role:'patron',depuis:new Date().toISOString()}))"
port = port_libre()
srv = subprocess.Popen(['python3', '-m', 'http.server', str(port), '--bind', '127.0.0.1'], cwd=str(D), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1)
NAV = "[...document.querySelectorAll('.side nav a.nv')].filter(a=>a.style.display!=='none').map(a=>a.textContent.trim().replace(/\\s+/g,' '))"
try:
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1500, 'height': 1000})
        errs = []; pg.on('pageerror', lambda e: errs.append(str(e)[:150]))
        pg.route('https://**/*', lambda r: r.abort())
        base = f'http://127.0.0.1:{port}/'
        pg.goto(base + 'accueil.html'); pg.evaluate(SESS)
        pg.evaluate("localStorage.setItem('clients-v1',JSON.stringify({'Carmen':{nom:'Carmen',vip:true}}))")
        pg.goto(base + 'catalogue.html'); pg.wait_for_timeout(1500)
        m = pg.evaluate(NAV)
        i = next((k for k, x in enumerate(m) if x.startswith('Clients') and 'VIP' not in x), -1)
        check("« Clients VIP » est juste sous « Clients » (depuis le Catalogue)", i >= 0 and m[i + 1].startswith('Clients VIP'), m)
        sub = pg.locator('nav a.nv.sub')
        check("c'est une sous-rubrique (décalée, plus petite)", sub.count() == 1 and pg.evaluate("parseFloat(getComputedStyle(document.querySelector('nav a.nv.sub')).paddingLeft)") > 25)
        sub.click(); pg.wait_for_timeout(1800)
        check("on arrive sur la page Clients", pg.url.split('?')[0].endswith('clients.html'), pg.url)
        check("le filtre « Favoris (VIP) » est choisi", pg.evaluate("document.getElementById('typ').value") == 'vip')
        nom = pg.evaluate("[...document.querySelectorAll('.tbl tbody tr')].map(r=>r.dataset.c)")
        pg.select_option('#typ', ''); pg.wait_for_timeout(300); tous = pg.evaluate("document.querySelectorAll('.tbl tbody tr').length")
        pg.select_option('#typ', 'vip'); pg.wait_for_timeout(300)
        check("seuls les favoris sont listés (Carmen, et moins que « Tous »)", 'Carmen' in nom and 0 < len(nom) < tous, (len(nom), tous))
        check("« Clients VIP » est allumée, « Clients » éteinte",
              pg.evaluate("document.querySelector('nav a.nv.sub').classList.contains('on')") and
              pg.evaluate("!document.querySelector('nav a.nv[href^=\"clients.html\"]:not(.sub)').classList.contains('on')"))
        # retour à tous les clients par le filtre
        pg.select_option('#typ', ''); pg.wait_for_timeout(300)
        check("filtre remis sur « Tous » : « Clients » se rallume",
              pg.evaluate("!document.querySelector('nav a.nv.sub').classList.contains('on')") and
              pg.evaluate("document.querySelector('nav a.nv[href^=\"clients.html\"]:not(.sub)').classList.contains('on')"))
        check("l'adresse n'a plus #vip", '#vip' not in pg.url, pg.url)
        pg.select_option('#typ', 'vip'); pg.wait_for_timeout(300)
        check("filtre « Favoris (VIP) » choisi à la main : la ligne du menu s'allume et l'adresse suit",
              pg.evaluate("document.querySelector('nav a.nv.sub').classList.contains('on')") and '#vip' in pg.url, pg.url)
        # clic sur la ligne quand on est déjà sur Clients (changement d'adresse seulement)
        pg.select_option('#typ', ''); pg.wait_for_timeout(200)
        pg.locator('nav a.nv.sub').click(); pg.wait_for_timeout(500)
        check("depuis la page Clients, un clic sur « Clients VIP » filtre sans recharger", pg.evaluate("document.getElementById('typ').value") == 'vip')
        # un autre menu perso : Clients déplacé -> la sous-rubrique le suit
        pg.evaluate("localStorage.setItem('menu-perso-v1',JSON.stringify({ordre:['ventes.html','clients.html','catalogue.html'],noms:{},caches:[]}))")
        pg.goto(base + 'ventes.html'); pg.wait_for_timeout(1500)
        m = pg.evaluate(NAV)
        i = m.index('Clients') if 'Clients' in m else next((k for k, x in enumerate(m) if x.startswith('Clients') and 'VIP' not in x), -1)
        check("menu réglé par l'équipe : « Clients VIP » reste sous « Clients »", i >= 0 and m[i + 1].startswith('Clients VIP'), m)
        # 3 nov. 2026 (Igal : « je ne vois pas la partie Tâches ») : une rubrique nouvelle, absente de l'ordre réglé, se place
        # juste après celle qui la précède dans le menu d'origine — « Tâches » sous « Tableau de bord » — pas tout en bas
        pg.evaluate("localStorage.setItem('menu-perso-v1',JSON.stringify({ordre:['ventes.html','tableau.html','clients.html','catalogue.html','connecteurs.html'],noms:{},caches:[]}))")
        pg.goto(base + 'ventes.html'); pg.wait_for_timeout(1500)
        m = pg.evaluate(NAV)
        it = next((k for k, x in enumerate(m) if x.startswith('Tableau de bord')), -1)
        # depuis le 9 nov. « Analytique » est entre « Tableau de bord » et « Tâches » dans le menu d'origine, et depuis le 15 nov.
        # « Mailing » suit « Clients VIP » : chacune se place après celle qui la précède
        check("menu réglé sans « Tâches » : « Analytique » puis « Tâches » se placent sous « Tableau de bord », « Parler à Léa » sous « Connecteurs », « Mailing » sous « Clients VIP »",
              it >= 0 and m[it + 1].startswith('Analytique') and m[it + 2].startswith('Tâches') and m[m.index('Connecteurs') + 1].startswith('Parler à Léa')
              and m[m.index('Clients VIP') + 1].startswith('Mailing'), m)
        pg.evaluate("localStorage.setItem('menu-perso-v1',JSON.stringify({ordre:[],noms:{},caches:['clients.html']}))")
        pg.goto(base + 'ventes.html'); pg.wait_for_timeout(1500)
        m = pg.evaluate(NAV)
        check("« Clients » retiré du menu : « Clients VIP » part avec", not any(x.startswith('Clients') for x in m), m)
        pg.evaluate("localStorage.removeItem('menu-perso-v1')")
        # langues
        pg.evaluate("localStorage.setItem('langue-v1','en')")
        pg.goto(base + 'ventes.html'); pg.wait_for_timeout(2000)
        check("en anglais : « VIP customers »", 'VIP customers' in ' '.join(pg.evaluate(NAV)), pg.evaluate(NAV))
        pg.evaluate("localStorage.setItem('langue-v1','es')")
        pg.goto(base + 'ventes.html'); pg.wait_for_timeout(2000)
        check("en espagnol : « Clientes VIP »", 'Clientes VIP' in ' '.join(pg.evaluate(NAV)), pg.evaluate(NAV))
        check("aucune erreur de page", not errs, errs)
        b.close()
finally:
    srv.terminate()
print(ok, 'ok,', len(ko), 'KO', ko); raise SystemExit(1 if ko else 0)
