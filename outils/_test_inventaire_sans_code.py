# L'INVENTAIRE : LES PARFUMS SANS CODE-BARRES, ET LA FICHE EN PANNEAU (10 nov. 2026).
# Igal : « ils ont rempli les chiffres de l'inventaire, c'est toujours Jamais vérifiée, est-ce normal ? » — le comptage était
# rangé par code-barres : les 50 parfums SANS code-barres partageaient une seule case (le 26 compté sur l'un s'affichait sur
# tous, et un chiffre tapé sur n'importe lequel s'enregistrait sur le premier de la liste). Puis : « sur l'inventaire, cliquer
# sur le produit et avoir le panneau latéral avec la fiche produit ». Ce test protège :
#   1. LE POINT — deux parfums sans code-barres ont chacun leur case : le chiffre tapé sur le second va sur LE SECOND
#      (vérifié, son stock), le premier n'est pas touché ;
#   2. l'ancienne case commune (clé vide) est retirée au chargement : elle ne s'affiche plus sur aucune ligne ;
#   3. un parfum avec code-barres se compte comme avant ;
#   4. LE POINT — un clic sur le parfum ouvre sa fiche du Catalogue en panneau à droite (mode cadre), la fermeture rend la liste ;
#   5. LE POINT — un parfum sans code-barres à qui Sam a donné un code-barres sur sa fiche est trouvé par ce code
#      (recherche et douchette), son chiffre déjà compté le suit ;
#   6. aucune erreur JS.
import pathlib, subprocess, time, socket
from playwright.sync_api import sync_playwright
D = pathlib.Path('/home/claude/catalogue')
ok = 0; ko = []
def check(n, c, i=''):
    global ok
    if c: ok += 1; print('  ok  ', n)
    else: ko.append(n); print('  KO  ', n, str(i)[:300])
s = socket.socket(); s.bind(('127.0.0.1', 0)); port = s.getsockname()[1]; s.close()
srv = subprocess.Popen(['python3', '-m', 'http.server', str(port), '--bind', '127.0.0.1'], cwd=str(D), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1)
try:
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1400, 'height': 900}); err = []
        pg.on('pageerror', lambda e: err.append(str(e)))
        base = f'http://127.0.0.1:{port}/'
        pg.goto(base + 'accueil.html'); pg.wait_for_timeout(300)
        pg.evaluate("""()=>{ localStorage.clear(); localStorage.setItem('sam-comptes-demo-v1','0');
            localStorage.setItem('sam-comptes-v1',JSON.stringify([{ident:'sam',nom:'Sam',role:'patron',actif:true,h:'x'}]));
            localStorage.setItem('sam-session-v1',JSON.stringify({id:'sam',nom:'Sam',role:'patron',depuis:new Date().toISOString()}));
            localStorage.setItem('comptage-parfums-v1',JSON.stringify({'':'26'})); }""")
        pg.goto(base + 'stock.html'); pg.wait_for_timeout(3000)
        sans = pg.evaluate("P.filter(x=>!x.bc).slice(0,2).map(x=>({cle:x.cle,k:kc(x),nom:x.nom}))")
        check('il y a bien des parfums sans code-barres dans l\'inventaire', len(sans) == 2, sans)
        check('l\'ancienne case commune (26) est retirée : aucune ligne ne l\'affiche', pg.evaluate("!('' in saisie) && ![...document.querySelectorAll('.cnt')].some(i=>i.value==='26'&&!i.dataset.bc)"))
        # les deux lignes visibles
        pg.evaluate("ks=>{ $('q').value=''; rend(true); }", [])
        pg.fill('#q', sans[1]['nom'][:20]); pg.wait_for_timeout(600)
        sel = lambda k: '.cnt[data-bc="%s"]' % k.replace('"', '\\"')
        check('chaque parfum sans code-barres a SA case (clé = sa fiche)', pg.locator(sel(sans[1]['k'])).count() == 1 and sans[0]['k'] != sans[1]['k'], sans)
        pg.fill(sel(sans[1]['k']), '7'); pg.press(sel(sans[1]['k']), 'Tab'); pg.wait_for_timeout(500)
        m = pg.evaluate("([a,b])=>[MOD[a]||{},MOD[b]||{}]", [sans[0]['cle'], sans[1]['cle']])
        check('LE POINT — le chiffre tapé sur le second va sur LE SECOND : vérifié, stock 7', m[1].get('verif') == 'ok' and m[1].get('qteC') == 7, m[1])
        check('LE POINT — le premier parfum sans code-barres n\'est pas touché', m[0].get('verif') != 'ok' or m[0].get('qteC') != 7, m[0])
        check('la ligne dit « Vérifiée »', 'Vérifiée' in pg.evaluate("k=>document.querySelector(`tr[data-bc=\"${CSS.escape(k)}\"] td:nth-child(3)`).innerText", sans[1]['k']))
        pg.fill('#q', ''); pg.wait_for_timeout(500)
        autres = pg.evaluate("k=>[...document.querySelectorAll('.cnt')].filter(i=>i.value==='7'&&i.dataset.bc!==k).length", sans[1]['k'])
        check('le 7 ne s\'affiche sur aucune autre ligne', autres == 0, autres)
        print('2. un parfum avec code-barres')
        bc = pg.evaluate("P.find(x=>x.bc).bc")
        pg.fill('#q', bc); pg.wait_for_timeout(500)
        pg.fill(sel(bc), '4'); pg.press(sel(bc), 'Tab'); pg.wait_for_timeout(500)
        check('se compte comme avant', pg.evaluate("bc=>{ const p=P.find(x=>x.bc===bc); return (MOD[p.cle]||{}).qteC; }", bc) == 4)
        print('3. la fiche en panneau')
        pg.fill('#q', ''); pg.wait_for_timeout(400)
        cle = pg.evaluate("document.querySelector('#tb .pd[data-fiche]').dataset.fiche")
        pg.click('#tb .pd[data-fiche] .n >> nth=0'); pg.wait_for_timeout(700)
        src = pg.evaluate("(document.querySelector('#fv-ov iframe')||{}).src||''")
        check('LE POINT — un clic sur le parfum ouvre sa fiche du Catalogue en panneau à droite', 'catalogue.html#cle=' in src and 'cadre=1' in src and cle in src, src)
        pg.evaluate("window.postMessage({fiche:'fermee'},location.origin)"); pg.wait_for_timeout(400)
        check('la fermeture rend la liste', pg.evaluate("!document.getElementById('fv-ov') && document.querySelectorAll('#tb tr').length>10"))
        print('4. le code-barres posé sur la fiche')
        cle3 = pg.evaluate("P.filter(x=>!x.bc)[2].cle")
        pg.evaluate("""c=>{ const M=lit(KMOD,{}); M[c]=Object.assign({},M[c]||{},{bc:'9990001112223'}); ecrit(KMOD,M);
            const S=lit('comptage-parfums-v1',{}); S['#'+c]='5'; ecrit('comptage-parfums-v1',S); }""", cle3)
        pg.reload(); pg.wait_for_timeout(3000)
        r = pg.evaluate("c=>{ const p=P.find(x=>x.cle===c); const t=trouveBC('9990001112223'); return {bc:p.bc, t:t&&t.cle, s:saisie['9990001112223'], vieux:saisie['#'+c]}; }", cle3)
        check('LE POINT — le code-barres de la fiche est repris par l\'Inventaire : la douchette le trouve', r['bc'] == '9990001112223' and r['t'] == cle3, r)
        check('le chiffre déjà compté sous la fiche suit le code-barres', r['s'] == '5' and r['vieux'] is None, r)
        pg.fill('#q', '9990001112223'); pg.wait_for_timeout(600)
        check('la recherche par ce code-barres montre la ligne', pg.locator('.cnt[data-bc="9990001112223"]').count() == 1)
        check('aucune erreur JS', not err, err[:3])
        b.close()
finally:
    srv.terminate()
print(f'\n{ok} ok, {len(ko)} KO', ko); raise SystemExit(1 if ko else 0)
