# Igal, 13 oct. 2026 : l'historique de gros du tableur (jusqu'au 30 sept.) — règles de noms, top 10/20 dans la
# fiche client, total commandé dans la fiche Catalogue. Rien après le 30 sept. (l'ERP les enregistre lui-même).
import pathlib, subprocess, time, socket, json, re
from playwright.sync_api import sync_playwright
D = pathlib.Path('/home/claude/catalogue')
ok = 0; ko = []
def check(n, c, i=''):
    global ok
    if c: ok += 1; print('  ok  ', n)
    else: ko.append(n); print('  KO  ', n, i)
SEED = json.load(open(D / 'clients_seed.json'))
CAT = json.load(open(D / 'cat.json'))
norm = lambda b: re.sub(r'^0+', '', re.sub(r'\D', '', str(b or '')))
HG = json.loads(open(D / 'donnees/histgros.js').read().split('=', 1)[1].rstrip(';\n'))['l']
dates = [x['date'] for c in SEED['clients'] for x in c['cmds'] if x['date']]
check("aucune commande du tableur après le 30 sept.", max(dates) <= '2026-09-30', max(dates))
noms = {c['nom'] for c in SEED['clients']}
check("« Juan », « Juan Carlos », « La Casa del Perfume » sont un seul client", 'Casa del Perfume' in noms and not noms & {'Juan', 'Juan Carlos', 'La Casa del Perfume', 'Juan Bis'}, sorted(noms & {'Juan', 'Juan Carlos', 'La Casa del Perfume', 'Juan Bis'}))
check("« Collection » est rangé chez Carmen", 'Collection' not in noms and 'Carmen' in noms)
check("« Myriam » est rangé chez Robert", 'Myriam' not in noms and 'Robert' in noms)
check("« Miriam » est rangé chez Robert aussi (Igal, 7 nov. 2026 : « c'est le même client, tu regroupes les deux »)", 'Miriam' not in noms)
rob = next(c for c in SEED['clients'] if c['nom'] == 'Robert')
check("Robert porte alors les deux historiques (83 commandes, ~91 690 $)", rob['nb'] >= 80 and rob['total'] > 90000, (rob['nb'], rob['total']))
sk = max(HG, key=lambda k: sum(r[2] for r in HG[k]))
row = next(r for r in CAT if norm(r[0]) == sk)
sans = next(r for r in CAT if norm(r[0]) not in HG and r[0])
def port_libre():
    s = socket.socket(); s.bind(('127.0.0.1', 0)); p = s.getsockname()[1]; s.close(); return p
SESS = "localStorage.setItem('sam-session-v1', JSON.stringify({id:'sam',nom:'Sam',role:'patron',depuis:new Date().toISOString()}))"
port = port_libre()
srv = subprocess.Popen(['python3', '-m', 'http.server', str(port), '--bind', '127.0.0.1'], cwd=str(D), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1)
try:
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1500, 'height': 1000})
        errs = []; pg.on('pageerror', lambda e: errs.append(str(e)[:150]))
        pg.route('https://**/*', lambda r: r.abort())
        base = f'http://127.0.0.1:{port}/'
        pg.goto(base + 'accueil.html'); pg.evaluate(SESS)
        FACT = [{'id': 'j1', 'num': 'PT-2026-0100', 'sens': 'vente', 'canal': 'Vente en gros', 'tiers': 'Juan Carlos', 'd': '2026-10-05', 'h': '10:00',
                 'lignes': [{'cle': row[15], 'bc': row[0], 'ref': 'x', 'q': 2, 'p': 50}], 'montant': 100, 'stock': True, 'par': 'Sam', 't': '2026-10-05T14:00:00Z'}]
        pg.evaluate("f=>{ localStorage.setItem('factures-v1',JSON.stringify(f)); localStorage.setItem('clients-v1',JSON.stringify({'Juan Carlos':{nom:'Juan Carlos',vip:true,fiscal:'resale'}})); }", FACT)
        pg.goto(base + 'clients.html'); pg.wait_for_timeout(2500)
        T = pg.evaluate("window.__C.TOUS().map(o=>({n:o.nom,nb:o.achats.length,erp:o.achats.filter(a=>a.src==='erp').length}))")
        nn = {t['n'] for t in T}
        check("un seul client « Casa del Perfume », ni « Juan Carlos » ni « La Casa del Perfume »", 'Casa del Perfume' in nn and not nn & {'Juan Carlos', 'Juan', 'La Casa del Perfume'}, sorted(n for n in nn if 'uan' in n or 'asa' in n))
        casa = next(t for t in T if t['n'] == 'Casa del Perfume')
        sc = next(c for c in SEED['clients'] if c['nom'] == 'Casa del Perfume')
        check("sa vente faite dans l'outil sous « Juan Carlos » rejoint la même fiche", casa['erp'] == 1, casa)
        check("ses commandes du tableur sont toutes là", casa['nb'] - casa['erp'] == len([x for x in sc['cmds'] if not x['devis'] and not x['douteux']]), casa)
        check("sa fiche enregistrée sous « Juan Carlos » (favori) lui est rattachée", pg.evaluate("window.__C.parNom('Juan Carlos')!==null && window.__C.parNom('casa del perfume')!==null"))
        pg.evaluate("window.__C.ouvre('Casa del Perfume')"); pg.wait_for_timeout(400)
        check("l'étoile favori de l'ancienne fiche est reprise", pg.evaluate("document.getElementById('dfav').textContent")=='★')
        pg.evaluate("document.querySelector('.tab[data-t=prod]').click()"); pg.wait_for_timeout(200)
        def lignes(): return pg.evaluate("[...document.querySelectorAll('#p-prod tbody tr')].map(r=>[r.querySelector('.nom').innerText.split('\\n')[0],+r.children[4].innerText.replace(/[^0-9]/g,''),r.children[5].innerText])")
        L = lignes()
        check("par défaut : le top 10", len(L) == 10, len(L))
        check("classé par flacons, du plus au moins", [x[1] for x in L] == sorted([x[1] for x in L], reverse=True), [x[1] for x in L])
        pg.evaluate("document.querySelector('#p-prod [data-top=\"20\"]').click()"); pg.wait_for_timeout(300)
        check("Top 20 : vingt parfums", len(lignes()) == 20, len(lignes()))
        check("on reste sur l'onglet des parfums", pg.evaluate("document.querySelector('.tab.on').dataset.t") == 'prod')
        pg.evaluate("document.querySelector('#p-prod [data-top=\"0\"]').click()"); pg.wait_for_timeout(300)
        check("Tous : plus de vingt parfums", len(lignes()) > 20, len(lignes()))
        pg.evaluate("document.querySelector('#p-prod [data-ptri=\"mt\"]').click()"); pg.wait_for_timeout(300)
        mt = pg.evaluate("[...document.querySelectorAll('#p-prod tbody tr')].map(r=>+r.children[5].innerText.replace(/[^0-9.,]/g,'').replace(/,/g,''))")
        check("classé par montant, du plus au moins", mt == sorted(mt, reverse=True), mt[:5])
        # Catalogue
        pg.goto(base + 'catalogue.html#cle=' + row[15]); pg.wait_for_timeout(2500)
        pg.screenshot(path='/tmp/claude-0/cat_hg.png')
        HGL = json.loads(open(D / 'donnees/histgros.js').read().split('=', 1)[1].rstrip(';\n'))
        att = sum(r[2] for r in HGL['l'][sk]); nclients = len({r[1] for r in HGL['l'][sk]})
        check("le bloc « Ventes de ce parfum » est ouvert d'office, avec les totaux", pg.evaluate("(()=>{const d=document.getElementById('dvtes');return !!d&&d.open&&!!d.querySelector('.hst')})()"))
        fl = pg.evaluate("+document.querySelector('#dvtes .hst .v').innerText.replace(/[^0-9]/g,'')")
        check("le total de flacons vendus contient l'historique de gros d'avant l'ERP", fl >= att and fl <= att + 50, (fl, att))
        canaux = pg.evaluate("[...document.querySelectorAll('#dvtes .vdeux table')[0].querySelectorAll('tbody td:first-child')].map(e=>e.innerText)")
        check("« Par canal » montre la vente en gros d'avant l'ERP", any("avant l'ERP" in c for c in canaux), canaux)
        clients = pg.evaluate("[...document.querySelectorAll('#dvtes .vcli li b:first-child')].map(e=>e.innerText)")
        check("« Par client » dit à qui (les plus gros clients de ce parfum)", len(clients) >= min(5, nclients), clients)
        mg = pg.evaluate("(()=>{const r=[...document.querySelectorAll('#dvtes .vdeux table')[0].querySelectorAll('tbody tr')].find(t=>/avant l'ERP/.test(t.innerText)); return r?r.children[3].innerText.trim():null})()")
        check("pas de marge inventée sur l'historique d'avant l'ERP (« — »)", mg == '—', mg)
        pg.evaluate("document.getElementById('dvtes').open=false"); pg.wait_for_timeout(200)
        pg.evaluate("document.getElementById('dvtes').open=true"); pg.wait_for_timeout(200)
        pg.screenshot(path='/tmp/claude-0/cat_vte.png')
        check("plus de bloc à part « Commandé en gros avant l'ERP »", pg.evaluate("!document.querySelector('.dhg')"))
        pg.goto('about:blank'); pg.goto(base + 'catalogue.html#cle=' + sans[15]); pg.wait_for_timeout(2500)
        check("une référence jamais commandée en gros n'a pas de ligne d'avant l'ERP", pg.evaluate("!document.body.innerText.includes(\"avant l'ERP\")"))
        check("aucune erreur de page", not errs, errs[:3])
        b.close()
finally: srv.terminate()
print(ok, 'ok,', len(ko), 'KO', ko); raise SystemExit(1 if ko else 0)
