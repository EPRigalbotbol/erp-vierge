# Igal, 13 oct. 2026 : « le stock de Perfume City est dans le Google Sheet (onglet « perfume city ») ; Kim gérera
# l'inventaire, Sam verra ses ventes et son stock ». Le stock de la boutique ne peut plus vivre dans UN navigateur.
# Ce qui est en jeu :
#   1. coller l'onglet du Sheet dans « Mettre l'inventaire à jour » construit l'inventaire (QTY, TESTER QTY, prix, virgules décimales) ;
#   2. le stock est un magasin PARTAGÉ (pc-stock-v1), plus la clé locale d'avant, qui disparaît ;
#   3. deux postes qui vendent deux parfums différents ne s'écrasent pas ;
#   4. les testeurs (vitrine) sont enregistrés à part, et la feuille de comptage attend qty + testeurs ;
#   5. coller de nouveau le Sheet met les quantités à jour sans doubler les lignes ;
#   6. l'ancien stock gardé dans un navigateur entre une fois dans le magasin partagé, sans écraser.
import pathlib, subprocess, time, socket, json
from playwright.sync_api import sync_playwright
D = pathlib.Path('/home/claude/catalogue')
ok = 0; ko = []
def check(n, c, i=''):
    global ok
    if c: ok += 1; print('  ok  ', n)
    else: ko.append(n); print('  KO  ', n, i)
s = socket.socket(); s.bind(('127.0.0.1', 0)); port = s.getsockname()[1]; s.close()
srv = subprocess.Popen(['python3', '-m', 'http.server', str(port), '--bind', '127.0.0.1'], cwd=str(D), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1)
CSV = '''"UPC code","NAME","ML/fl oZ","BRAND","TYPE","GENDER","QTY","TESTER QTY","Supplier price","","pvr","pvw","check ","Location"
"85715167224","First Instinct Blue for Women","3.4","Abercrombie","EDP","W","5","1","23,5","117,5","36","27","OK","ebay"
"085715169587","Fierce 3.4","3.4","Abercrombie","EDC","M","1","0","31,5","31,5","65","38","",""
"8028713001734","Acqua Di Parma Colonia 6oz","6","Acqua Di Parma","EDC","M","6","1","71,5","429","95","82","OK","ebay"
"3348901486152","Sauvage","3.4","Dior","EDT","M","0","2","60","0","110","90","",""'''
CSV2 = CSV.replace('"5","1","23,5"', '"3","1","23,5"')
try:
    with sync_playwright() as p:
        b = p.chromium.launch(); ctx = b.new_context(viewport={'width': 1400, 'height': 950}); pg = ctx.new_page(); err = []
        pg.on('pageerror', lambda e: err.append(str(e))); pg.on('dialog', lambda d: d.accept())
        base = f'http://127.0.0.1:{port}/'
        pg.goto(base + 'accueil.html'); pg.wait_for_timeout(300)
        pg.evaluate("""()=>{ localStorage.clear();
          localStorage.setItem('sam-session-v1',JSON.stringify({id:'sam',nom:'Sam',role:'patron',depuis:new Date().toISOString()}));
          localStorage.setItem('langue-v1','fr'); localStorage.setItem('sam-comptes-demo-v1','0'); }""")
        pg.goto(base + 'inventaire_pc.html'); pg.wait_for_timeout(1800)

        print('1. coller l\'onglet « perfume city » du Sheet')
        pg.click('#majf'); pg.wait_for_timeout(300)
        pg.evaluate("t=>{ $('imptxt').value=t; $('imptxt').dispatchEvent(new Event('input')); }", CSV); pg.wait_for_timeout(900)
        t = pg.locator('#impres').inner_text()
        check('4 lignes lues', '4 ligne' in t, t[:300])
        pg.click('#impok'); pg.wait_for_timeout(2200)
        rows = pg.evaluate("pcsRows()")
        check('4 références dans l\'inventaire', rows and len(rows) == 4, rows)
        R = {str(r[0]).replace('0', '', 0): r for r in rows}
        a = next(r for r in rows if str(r[0]).endswith('85715167224'))
        check('quantité vendable 5 (colonne QTY)', a[5] == 5, a)
        check('prix d\'achat 23,5 (virgule décimale)', a[6] == 23.5, a)
        check('PVR 36 et PVW 27', a[10] == 36 and a[11] == 27, a)
        T = pg.evaluate("JSON.parse(localStorage.getItem('testeurs-pc-v1')||'{}')")
        check('LE POINT — 10 nov. 2026 (Igal) : un tester par parfum, jamais plus — la colonne TESTER QTY dit 2 pour Sauvage, l\'ERP note 1 (Fierce 0 : aucun)', sorted(v['n'] for v in T.values()) == [1, 1, 1], T)
        check('LE POINT — stock dans le magasin partagé pc-stock-v1, plus dans la clé locale',
              pg.evaluate("()=>!!localStorage.getItem('pc-stock-v1') && !localStorage.getItem('inventaire-local-pc-v1')"))
        check('ligne avec QTY 0 gardée (Sauvage : que des testeurs)', any(str(r[0]) == '3348901486152' and r[5] == 0 for r in rows))
        n = pg.evaluate("document.querySelectorAll('#tb tr').length")
        check('la page les affiche', n >= 4, n)

        print('2. coller de nouveau : mise à jour, pas de doublons')
        pg.click('#majf'); pg.wait_for_timeout(300)
        pg.evaluate("t=>{ $('imptxt').value=t; $('imptxt').dispatchEvent(new Event('input')); }", CSV2); pg.wait_for_timeout(900)
        pg.click('#impok'); pg.wait_for_timeout(2200)
        rows = pg.evaluate("pcsRows()")
        a = next(r for r in rows if str(r[0]).endswith('85715167224'))
        check('toujours 4 lignes', len(rows) == 4, len(rows))
        check('quantité passée de 5 à 3', a[5] == 3, a)

        print('3. deux postes, deux ventes différentes')
        pg2 = ctx.new_page(); pg2.on('pageerror', lambda e: err.append(str(e)))
        pg.goto(base + 'catalogue.html'); pg.wait_for_timeout(1500)
        pg2.goto(base + 'catalogue.html'); pg2.wait_for_timeout(1500)
        # les deux ont lu le même stock ; chacune change un parfum différent
        pg.evaluate("()=>{ const r=pcsRows(); const x=r.find(z=>String(z[0]).endsWith('85715167224')); x[5]=2; pcsSauve([x]); }")
        pg2.evaluate("()=>{ const r=pcsRows(); const x=r.find(z=>String(z[0])==='8028713001734'); x[5]=4; pcsSauve([x]); }")
        pg.wait_for_timeout(300)
        rows = pg.evaluate("pcsRows()")
        q1 = next(r for r in rows if str(r[0]).endswith('85715167224'))[5]
        q2 = next(r for r in rows if str(r[0]) == '8028713001734')[5]
        check('LE POINT — les deux changements sont là (2 et 4)', q1 == 2 and q2 == 4, (q1, q2))
        pg2.close()

        print('4. l\'ancien stock d\'un navigateur entre une fois, sans écraser')
        pg.evaluate("""()=>{ localStorage.setItem('inventaire-local-pc-v1',JSON.stringify([
           ['85715167224','x','Abercrombie','3.4','EDP',99,10,990,'non','b85715167224',null,null],
           ['111111111111','Ancien','M','3.4','EDP',7,10,70,'non','b111111111111',null,null]])); }""")
        pg.goto(base + 'inventaire_pc.html'); pg.wait_for_timeout(1800)
        rows = pg.evaluate("pcsRows()")
        a = next(r for r in rows if str(r[0]).endswith('85715167224'))
        check('la ligne déjà dans le magasin n\'est pas écrasée (2, pas 99)', a[5] == 2, a)
        check('la ligne qui manquait y entre', any(str(r[0]) == '111111111111' and r[5] == 7 for r in rows))
        check('l\'ancienne clé locale est supprimée', pg.evaluate("()=>!localStorage.getItem('inventaire-local-pc-v1')"))
        check('aucune erreur de page', not err, err[:3])
        b.close()
finally:
    srv.terminate()
print(f'\n{ok} ok, {len(ko)} KO')
if ko: print(ko); raise SystemExit(1)
