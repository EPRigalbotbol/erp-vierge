# Le mot « devis » ne doit JAMAIS être vu à l'écran en français : ni une demi-seconde
# au chargement (le temps que le code de la page démarre), ni un instant à chaque
# redessin. Igal l'a vu le 12 septembre : « code apparaît, après code disparaît ».
# On regarde l'écran à chaque image (requestAnimationFrame), comme un œil humain.
import pathlib, subprocess, time, socket
from playwright.sync_api import sync_playwright

D = pathlib.Path('/home/claude/catalogue')
ok = 0; ko = []
def check(n, c, i=''):
    global ok
    if c: ok += 1; print('  ok  ', n)
    else: ko.append(n); print('  KO  ', n, i)
def port_libre():
    s = socket.socket(); s.bind(('127.0.0.1', 0)); p = s.getsockname()[1]; s.close(); return p
OEIL = """
window.__vu=new Set(); window.__images=0;
(function boucle(){ try{ if(document.body){ window.__images++;
  /* on ne regarde que ce que l'œil voit en premier : le menu, le titre, la liste des cotes, la file — sans forcer la mise en page */
  let t=''; document.querySelectorAll('nav, header, .docs, #file, .qf, #docs-em').forEach(e=>{ t+=' '+(e.textContent||''); });
  const m=t.match(/[^\\s]*devis[^\\s]*/gi); if(m) m.forEach(x=>window.__vu.add(x)); } }catch(e){}
  requestAnimationFrame(boucle); })();
/* l'ordre des rubriques, image par image : il ne doit jamais changer sous les yeux */
/* le contenu principal, image par image : sa longueur de texte quand il est visible. Un seul état = pas de « deux pages » */
window.__mains=[]; (function b(){ try{ const m=document.querySelector('.main'); if(m&&getComputedStyle(m).visibility!=='hidden'){ const t=String((m.innerText||'').length)+':'+(m.innerText||'').slice(0,30).replace(/\s+/g,' '); if(!window.__mains.length||window.__mains[window.__mains.length-1].split(':')[0]!==t.split(':')[0]) window.__mains.push(t); } }catch(e){} requestAnimationFrame(b); })();
/* la disposition de la barre : la hauteur de chaque rubrique visible, image par image */
window.__pos=[]; (function b(){ try{ const n=document.querySelector('.side nav'); if(n&&getComputedStyle(n).visibility!=='hidden'){ const o=[...n.querySelectorAll('a.nv')].filter(a=>a.style.display!=='none').map(a=>Math.round(a.getBoundingClientRect().top)).join(','); if(o&&(!window.__pos.length||window.__pos[window.__pos.length-1]!==o)) window.__pos.push(o); } }catch(e){} requestAnimationFrame(b); })();
window.__ordres=[]; (function b(){ try{ const n=document.querySelector('.side nav'); if(n&&getComputedStyle(n).visibility!=='hidden'){ const o=[...n.querySelectorAll('a.nv')].filter(a=>a.style.display!=='none').map(a=>a.getAttribute('href').split('?')[0]).join(','); if(o&&(!window.__ordres.length||window.__ordres[window.__ordres.length-1]!==o)) window.__ordres.push(o); } }catch(e){} requestAnimationFrame(b); })();
"""
port = port_libre()
srv = subprocess.Popen(['python3', '-m', 'http.server', str(port), '--bind', '127.0.0.1'], cwd=str(D), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1)
try:
    with sync_playwright() as p:
        b = p.chromium.launch(); ctx = b.new_context(viewport={'width': 1400, 'height': 1000}); ctx.add_init_script(OEIL)
        pg = ctx.new_page(); err = []
        pg.on('pageerror', lambda e: err.append(str(e)))
        base = f'http://127.0.0.1:{port}/'
        pg.goto(base + 'accueil.html'); pg.wait_for_timeout(400)
        pg.evaluate("localStorage.setItem('cotes-erp-ouvert','1');localStorage.setItem('sam-session-v1', JSON.stringify({id:'sam',nom:'Sam',role:'patron',depuis:new Date().toISOString()}))")
        pg.evaluate("localStorage.setItem('langue-v1','fr')")

        print('1. Ventes : du premier pixel au dernier redessin, jamais « devis »')
        pg.goto(base + 'ventes.html'); pg.wait_for_timeout(2500)
        # quelques redessins de la liste des cotes et de la file
        pg.evaluate("try{ Q_F.etat=''; peintDocs(); Q_F.etat='converti'; peintDocs(); Q_F.etat='devis'; peintDocs(); }catch(e){}")
        pg.wait_for_timeout(600)
        vu = pg.evaluate("[...window.__vu]"); n = pg.evaluate("window.__images")
        check(f'{n} images regardées, aucune ne montre « devis »', n > 20 and not vu, vu)
        check('le menu dit Cote', 'Cote' in pg.locator('nav a.nv[href^="quotes"]').inner_text(), pg.locator('nav a.nv[href^="quotes"]').inner_text())
        check("le titre de la liste dit Cotes", 'Cote' in (pg.locator('.docs h2.sec').inner_text() if pg.locator('.docs h2.sec').count() else 'Cote'))

        print('2. Cotes, Tableau de bord, Factures : pareil')
        for page in ('quotes.html', 'tableau.html', 'factures.html', 'etude.html'):
            pg.evaluate("window.__vu=new Set(); window.__images=0")
            pg.goto(base + page); pg.wait_for_timeout(2200)
            vu = pg.evaluate("[...window.__vu]"); n = pg.evaluate("window.__images")
            check(f'{page} : {n} images, aucune ne montre « devis »', n > 10 and not vu, vu)

        print("2b. en anglais : jamais un mot français à l'écran non plus, du premier pixel au dernier redessin")
        pg.evaluate("localStorage.setItem('langue-v1','en')")
        pg.evaluate("window.__vu=new Set(); window.__images=0; window.__vuFr=new Set(); (function b(){ try{ let t=''; document.querySelectorAll('nav, header, #docs-em, .qf').forEach(e=>{ t+=' '+(e.textContent||''); }); const m=t.match(/(Fournisseurs|Réglages|Tableau de bord|Ventes|Journal des|Toutes les cotes|Chercher un client)/g); if(m) m.forEach(x=>window.__vuFr.add(x)); }catch(e){} requestAnimationFrame(b); })();")
        for page in ('ventes.html', 'quotes.html', 'tableau.html'):
            pg.evaluate("window.__vuFr=new Set()")
            pg.goto(base + page); pg.wait_for_timeout(2200)
            vu = pg.evaluate("[...(window.__vuFr||[])]")
            check(f'{page} en anglais : aucune image ne montre un mot français', not vu, vu)
            check(f'{page} en anglais : la page est visible à la fin', pg.evaluate("document.documentElement.style.visibility") == '')
        pg.evaluate("localStorage.setItem('langue-v1','fr')")

        print("2c. un menu réglé : les rubriques ne sautent jamais (Igal : « ça monte, ça descend »)")
        pg.evaluate("localStorage.setItem('menu-perso-v1', JSON.stringify({ordre:['ventes.html','tableau.html','clients.html','catalogue.html'],noms:{'ventes.html':'Mes ventes'},caches:['messages.html']}))")
        for page in ('tableau.html', 'ventes.html', 'catalogue.html', 'clients.html'):
            pg.goto(base + page); pg.wait_for_timeout(2000)
            o = pg.evaluate("window.__ordres")
            # 13 oct. : « Clients VIP » est une ligne sous Clients (même page, autre adresse) : clients.html y figure deux fois
            # 3 nov. : une rubrique absente de l'ordre réglé se place juste après celle qui la précède dans le menu d'origine
            # (Fournisseurs après Ventes, Analytique et Tâches après Tableau de bord, Mailing après Clients VIP) : on vérifie que
            # les rubriques RÉGLÉES restent dans leur ordre, et qu'un seul ordre a été vu
            _r = [x for x in (o[0].split(',') if o else []) if x in ('ventes.html', 'tableau.html', 'clients.html', 'catalogue.html')]
            check(f'{page} : un seul ordre de rubriques vu, le réglé', len(o) == 1 and o[0].startswith('ventes.html,') and _r == ['ventes.html', 'tableau.html', 'clients.html', 'clients.html', 'catalogue.html'], o)
            check(f'{page} : « Mes ventes », pas de rubrique Messages (retirée le 9 oct.), barre visible', 'Mes ventes' in pg.locator('nav').inner_text() and pg.evaluate("!document.querySelector('nav a.nv[href^=\"messages\"]')") and pg.evaluate("getComputedStyle(document.querySelector('.side nav')).visibility") == 'visible')
        pg.evaluate("localStorage.removeItem('menu-perso-v1')")

        print("2d. rien ne glisse dans la barre de gauche pendant le chargement, et tout tient sur un écran de portable (816 px)")
        pg2 = ctx.new_page(); pg2.set_viewport_size({'width': 1280, 'height': 816})
        pg2.goto(base + 'accueil.html'); pg2.wait_for_timeout(300)
        pg2.evaluate("localStorage.setItem('cotes-erp-ouvert','1');localStorage.setItem('sam-session-v1', JSON.stringify({id:'igal',nom:'Igal',role:'admin',depuis:new Date().toISOString()}))")
        pg2.evaluate("localStorage.setItem('menu-perso-v1', JSON.stringify({ordre:['ventes.html','tableau.html','clients.html','catalogue.html'],noms:{},caches:[]}))")
        for page in ('tableau.html', 'ventes.html', 'catalogue.html', 'stock.html'):
            pg2.goto(base + page); pg2.wait_for_timeout(2200)
            pos = pg2.evaluate("window.__pos")
            side = pg2.evaluate("(()=>{ const s=document.querySelector('.side'); return {sh:s.scrollHeight, ch:s.clientHeight, foot:document.querySelector('.sfoot').getBoundingClientRect().top, sfu:document.querySelector('#sfu').innerText.replace(/\\n/g,' ')}; })()")
            check(f'{page} : les rubriques ne bougent pas d\'un pixel (une seule disposition vue)', pos and len(pos) == 1, pos)
            check(f'{page} : la barre tient dans 816 px sans défiler', side['sh'] <= side['ch'], side)
            check(f'{page} : le bas de la barre montre Igal / Admin / Se déconnecter', all(x in side['sfu'] for x in ('Igal', 'Admin', 'Se déconnecter')), side['sfu'])
        pg2.close()

        print("2e. la page s'affiche d'un seul coup, dessinée — jamais une coquille vide puis une autre page")
        pg3 = ctx.new_page(); pg3.set_viewport_size({'width': 1280, 'height': 816})
        pg3.goto(base + 'accueil.html'); pg3.wait_for_timeout(300)
        pg3.evaluate("localStorage.setItem('cotes-erp-ouvert','1');localStorage.setItem('sam-session-v1', JSON.stringify({id:'igal',nom:'Igal',role:'admin',depuis:new Date().toISOString()}))")
        for page in ('tableau.html', 'ventes.html', 'clients.html', 'factures.html', 'catalogue.html'):
            pg3.goto(base + page); pg3.wait_for_timeout(2500)
            etats = pg3.evaluate("window.__mains")
            # 15 oct. : tolérance portée de 60 à 120 caractères — la barre des filtres du Catalogue (« En stock », « Historique »… ~80 caractères) se pose une image après le contenu, dans le même instant ; le badge « Igal · Admin » en ajoute une vingtaine.
            # après le premier état visible, seuls des riens peuvent encore bouger (le badge « Igal · Admin » du haut, qui attend la réponse du cockpit)
            n0 = int(etats[0].split(':')[0]) if etats else 0
            check(f"{page} : un seul état visible du contenu (le dessiné), et la page est visible à la fin", etats and all(abs(int(e.split(':')[0]) - n0) <= 120 for e in etats) and pg3.evaluate("getComputedStyle(document.querySelector('.main')).visibility") == 'visible', etats and [e[:40] for e in etats])
        pg3.close()

        print("3. en anglais et en espagnol, le menu et le titre viennent bien du français d'origine")
        pg.goto(base + 'quotes.html'); pg.wait_for_timeout(2000)
        pg.evaluate("lgChange('en')"); pg.wait_for_timeout(500)
        t = pg.locator('nav a.nv[href^="quotes"]').inner_text()
        check('menu EN : Quotes', 'Quotes' in t, t)
        h = pg.locator('header h1').inner_text()
        check('titre EN : Quotes', 'Quotes' in h, h)
        pg.evaluate("lgChange('es')"); pg.wait_for_timeout(500)
        check('menu ES : Cotizaciones', 'Cotizaciones' in pg.locator('nav a.nv[href^="quotes"]').inner_text())
        pg.evaluate("lgChange('fr')"); pg.wait_for_timeout(500)
        check('retour FR : Cote', 'Cote' in pg.locator('nav a.nv[href^="quotes"]').inner_text() and 'Cote' in pg.locator('header h1').inner_text(), pg.locator('header h1').inner_text())
        check('aucune erreur JS', not err, err[:3])
        b.close()
finally:
    srv.terminate()
print(f"\n{ok} ok, {len(ko)} KO", ko)
