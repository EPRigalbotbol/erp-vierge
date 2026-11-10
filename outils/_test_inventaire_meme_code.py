# DEUX FICHES, UN MÊME CODE-BARRES, DANS L'INVENTAIRE (Igal, 10 nov. 2026 : « j'ai mis 43 sur le premier, ça m'a mis 43 sur le
# deuxième » — une même eau de Cologne en boîte blanche et en ancienne boîte dorée). Le comptage était rangé par code-barres : les
# deux fiches partageaient une seule case, et un chiffre tapé sur la seconde s'enregistrait sur la première. Ce test protège :
#   1. LE POINT — deux fiches au même code-barres ont chacune leur case : le chiffre tapé sur la seconde va sur LA SECONDE ;
#   2. LE POINT — le premier n'est pas touché, et son chiffre ne s'affiche pas sur l'autre ligne ;
#   3. l'ancienne case commune est rendue à la fiche déjà comptée, puis retirée ;
#   4. LE POINT — un code-barres changé sur la fiche (« …oldbox ») l'emporte sur celui du fichier : la douchette le trouve,
#      la ligne a sa propre case, et la quantité attendue reste celle du stock importé ;
#   5. la douchette sur un code partagé dit que plusieurs fiches le portent ;
#   6. aucune erreur JS.
import pathlib, subprocess, time, socket, json, collections
from playwright.sync_api import sync_playwright
D = pathlib.Path('/home/claude/catalogue')
ok = 0; ko = []
def check(n, c, i=''):
    global ok
    if c: ok += 1; print('  ok  ', n)
    else: ko.append(n); print('  KO  ', n, str(i)[:300])
CAT = json.load(open(D / 'cat.json'))
par = collections.defaultdict(list)
for r in CAT:
    if r[0] and str(r[0]).isdigit() and len(str(r[0])) >= 12 and r[15]: par[str(r[0])].append(r)
paires = [(k, v) for k, v in par.items() if len(v) == 2]
(BC, (W, G)), (BC2, (W2, G2)) = paires[0], paires[1]
s = socket.socket(); s.bind(('127.0.0.1', 0)); port = s.getsockname()[1]; s.close()
srv = subprocess.Popen(['python3', '-m', 'http.server', str(port), '--bind', '127.0.0.1'], cwd=str(D), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)
try:
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1400, 'height': 900}); err = []
        pg.on('pageerror', lambda e: err.append(str(e)))
        base = f'http://127.0.0.1:{port}/'
        pg.goto(base + 'accueil.html'); pg.wait_for_timeout(300)
        pg.evaluate("""([bc,cw,bc2,cg2])=>{ localStorage.clear(); localStorage.setItem('sam-comptes-demo-v1','0');
            localStorage.setItem('sam-comptes-v1',JSON.stringify([{ident:'sam',nom:'Sam',role:'patron',actif:true,h:'x'}]));
            localStorage.setItem('sam-session-v1',JSON.stringify({id:'sam',nom:'Sam',role:'patron',depuis:new Date().toISOString()}));
            const M={}; M[cw]={verif:'ok',qte:43,qteC:43}; M[cg2]={bc:bc2+'oldbox',qte:11}; localStorage.setItem('fiches-modifiees-v1',JSON.stringify(M));
            const S={}; S[bc]='43'; localStorage.setItem('comptage-parfums-v1',JSON.stringify(S)); }""", [BC, W[15], BC2, G2[15]])
        pg.goto(base + 'stock.html'); pg.wait_for_timeout(3000)
        kmod = pg.evaluate("KMOD")
        if kmod != 'fiches-modifiees-v1':
            pg.evaluate("""([k,cw,bc2,cg2])=>{ const M={}; M[cw]={verif:'ok',qte:43,qteC:43}; M[cg2]={bc:bc2+'oldbox',qte:11}; localStorage.setItem(k,JSON.stringify(M)); }""", [kmod, W[15], BC2, G2[15]])
            pg.reload(); pg.wait_for_timeout(3000)
        print('1. deux fiches, un même code')
        k = pg.evaluate("([a,b])=>[kc(P.find(x=>x.cle===a)),kc(P.find(x=>x.cle===b))]", [W[15], G[15]])
        check('chaque fiche a SA case (clé = sa fiche, pas le code commun)', k[0] != k[1] and k[0].startswith('#') and k[1].startswith('#'), k)
        r = pg.evaluate("([a,b,bc])=>({w:saisie['#'+a], g:saisie['#'+b], c:saisie[bc]})", [W[15], G[15], BC])
        check('l\'ancienne case commune (43) revient à la fiche déjà comptée, et elle seule', r['w'] == '43' and r['g'] is None and r['c'] is None, r)
        pg.fill('#q', BC); pg.wait_for_timeout(600)
        vals = pg.evaluate("([a,b])=>[document.querySelector(kSel('#'+a)).value, document.querySelector(kSel('#'+b)).value]", [W[15], G[15]])
        check('LE POINT — le 43 ne s\'affiche que sur la ligne comptée', vals == ['43', ''], vals)
        sel = pg.evaluate("b=>kSel('#'+b)", G[15])
        pg.fill(sel, '7'); pg.press(sel, 'Tab'); pg.wait_for_timeout(500)
        m = pg.evaluate("([a,b])=>[MOD[a]||{},MOD[b]||{}]", [W[15], G[15]])
        check('LE POINT — le chiffre tapé sur la seconde va sur LA SECONDE : vérifiée, stock 7', m[1].get('verif') == 'ok' and m[1].get('qteC') == 7, m[1])
        check('LE POINT — la première n\'est pas touchée (43)', m[0].get('qteC') == 43 and m[0].get('qte') == 43, m[0])
        print('2. un code-barres changé sur la fiche')
        r = pg.evaluate("([c,bc])=>{ const p=P.find(x=>x.cle===c), t=trouveBC(bc+'OLDBOX'); return {bc:p.bc, k:kc(p), t:t&&t.cle, th:qteTh(p)}; }", [G2[15], BC2])
        check('LE POINT — la fiche « …oldbox » se compte et se scanne sous son code', r['bc'] == BC2 + 'oldbox' and r['k'] == BC2 + 'oldbox' and r['t'] == G2[15], r)
        check('l\'autre boîte garde le code du fichier et sa propre case', pg.evaluate("c=>kc(P.find(x=>x.cle===c))", W2[15]) == BC2)
        check('la quantité attendue suit la fiche (11)', r['th'] == 11, r)
        print('3. la douchette')
        pg.fill('#q', ''); pg.wait_for_timeout(300)
        pg.evaluate("bc=>scanne(bc)", BC); pg.wait_for_timeout(500)
        check('sur un code partagé, la douchette dit que 2 fiches le portent', '2 fiches portent ce code-barres' in pg.inner_text('#scan'), pg.inner_text('#scan'))
        check('aucune erreur JS', not err, err[:3])
        b.close()
finally:
    srv.terminate()
print(f'\n{ok} ok, {len(ko)} KO', ko); raise SystemExit(1 if ko else 0)
