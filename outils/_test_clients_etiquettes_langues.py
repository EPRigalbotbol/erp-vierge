# LES ÉTIQUETTES DE LA LISTE DES CLIENTS SONT TRADUITES (16 nov. 2026 — écran de Sam en anglais : « GROS », « BOUTIQUE » et
# « 520 $ à payer » restaient en français). La case du nom est exclue de la traduction automatique (le nom du client y vit) :
# ses étiquettes doivent donc se traduire elles-mêmes. Ce test protège :
#   1. LE POINT — en anglais : Wholesale, Shop, « to pay » ; en espagnol : Mayorista, Tienda, « por pagar » ;
#   2. en français, rien ne change (Gros, Boutique, « à payer ») ; le nom du client n'est jamais traduit ;
#   3. aucune erreur JS.
import subprocess, time, socket, json
from playwright.sync_api import sync_playwright
D = '/home/claude/catalogue'
ok = 0; ko = []
def check(n, c, i=''):
    global ok
    if c: ok += 1; print('  ok  ', n)
    else: ko.append(n); print('  KO  ', n, str(i)[:400])
C = json.load(open(D + '/cat.json'))
A = [r for r in C if (r[6] or 0) > 0 and r[0] and r[0].isdigit()][0]
L = [{'cle': A[15], 'bc': A[0], 'ref': 'x', 'q': 2, 'p': 50}]
NOM = 'Boutique Gros Test'
F = [{'id': 'v1', 'num': 'v1', 'sens': 'vente', 'canal': 'Gros', 'tiers': NOM, 'd': '2026-10-27', 'montant': 300, 'lignes': L, 'stock': True,
      'doc': {'type': 'facture', 'num': 'PT-4', 'pstat': 'apayer', 'pmode': 'zelle', 'reste': 300, 'regle': 0, 'total': 300}},
     {'id': 'v2', 'num': 'v2', 'sens': 'vente', 'canal': 'Boutique', 'tiers': NOM, 'd': '2026-10-28', 'montant': 50, 'lignes': L, 'stock': True}]
s = socket.socket(); s.bind(('127.0.0.1', 0)); port = s.getsockname()[1]; s.close()
srv = subprocess.Popen(['python3', '-m', 'http.server', str(port), '--bind', '127.0.0.1'], cwd=D, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)
try:
    with sync_playwright() as p:
        b = p.chromium.launch(); err = []
        def ligne(lg):
            pg = b.new_page(viewport={'width': 1500, 'height': 1000}); pg.on('pageerror', lambda e: err.append(str(e)))
            pg.goto(f'http://127.0.0.1:{port}/accueil.html'); pg.wait_for_timeout(300)
            pg.evaluate("""([F,lg])=>{ localStorage.clear(); localStorage.setItem('sam-comptes-demo-v1','0');
              localStorage.setItem('sam-session-v1',JSON.stringify({id:'sam',nom:'Sam',role:'patron',depuis:new Date().toISOString()}));
              localStorage.setItem('langue-v1',lg); localStorage.setItem('factures-v1',JSON.stringify(F)); }""", [F, lg])
            pg.goto(f'http://127.0.0.1:{port}/clients.html'); pg.wait_for_timeout(3000)
            t = pg.evaluate("n=>{ const tr=document.querySelector('tr[data-c=\"'+n+'\"]'); return tr?[...tr.querySelectorAll('.tg,.warn')].map(x=>x.textContent.replace(/\\u00a0/g,' ')).concat([tr.querySelector('td.nom span').textContent]):null; }", NOM)
            pg.close(); return t or []
        t = ligne('en')
        check('LE POINT — anglais : Wholesale, Shop, « 300 $ to pay »', 'Wholesale' in t and 'Shop' in t and '300 $ to pay' in t and not any(x in ('Gros', 'Boutique') or 'à payer' in x for x in t[:-1]), t)
        check('le nom du client n\'est pas traduit', t and t[-1] == NOM, t)
        t = ligne('es')
        check('LE POINT — espagnol : Mayorista, Tienda, « 300 $ por pagar »', 'Mayorista' in t and 'Tienda' in t and '300 $ por pagar' in t, t)
        t = ligne('fr')
        check('français inchangé : Gros, Boutique, « 300 $ à payer »', 'Gros' in t and 'Boutique' in t and '300 $ à payer' in t, t)
        check('aucune erreur JS', not err, err[:3])
        b.close()
finally:
    srv.terminate()
print(f"\n{ok} ok, {len(ko)} KO", ko)
raise SystemExit(1 if ko else 0)
