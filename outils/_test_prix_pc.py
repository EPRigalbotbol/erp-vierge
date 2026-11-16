# PERFUME CITY SUIT LES PRIX DE L'ERP (16 nov. 2026 — Kim : « Hayaati Florence, sur mon Shopify il est à 20, sur le logiciel à 19 » ;
# Igal : « les prix de référence sont ceux de perfumestrade… quand Sam change un prix, prix d'achat ou prix de vente, il faut que
# ça change chez Perfume City aussi »). Le Catalogue publie prix-pc-v1 ; le cockpit l'applique (cockpit/_t_prix_pc.mjs). Ce test protège :
#   1. LE POINT — chaque code-barres porte [prix de vente de perfumestrade.com, prix d'achat de la fiche] ;
#   2. LE POINT — un prix changé dans la fiche (vente ou achat) est republié tout seul, sans bouton ;
#   3. un code porté par deux fiches qui ne disent pas la même chose est mis à part (amb) ; une fiche coupée de Perfume City n'y est pas ;
#   4. seuls le Patron et un admin publient ; aucune erreur JS.
import subprocess, time, socket, json
from playwright.sync_api import sync_playwright
D = '/home/claude/catalogue'
ok = 0; ko = []
def check(n, c, i=''):
    global ok
    if c: ok += 1; print('  ok  ', n)
    else: ko.append(n); print('  KO  ', n, str(i)[:600])
C = json.load(open(D + '/cat.json'))
P = [r for r in C if r[15] and r[0] and str(r[0]).isdigit() and (r[7] or 0) > 0 and (r[12] or 0) > 0 and r[15] == 'b' + r[0]]
A, Bf = P[0], P[1]
nz = lambda s: str(s).lstrip('0')
s = socket.socket(); s.bind(('127.0.0.1', 0)); port = s.getsockname()[1]; s.close()
srv = subprocess.Popen(['python3', '-m', 'http.server', str(port), '--bind', '127.0.0.1'], cwd=D, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)
SESS = """([role,X])=>{ localStorage.clear(); localStorage.setItem('sam-comptes-demo-v1','0');
  localStorage.setItem('sam-session-v1',JSON.stringify({id:'sam',nom:'Sam',role:role,depuis:new Date().toISOString()}));
  localStorage.setItem('crm-utilisateur-v1','Sam'); localStorage.setItem('langue-v1','fr'); for(const k in X) localStorage.setItem(k,JSON.stringify(X[k])); }"""
try:
    with sync_playwright() as p:
        b = p.chromium.launch(); err = []
        def ouvre(role='patron', X=None):
            ctx = b.new_context(); pg = ctx.new_page(); pg.on('pageerror', lambda e: err.append(str(e)))
            pg.goto(f'http://127.0.0.1:{port}/accueil.html'); pg.wait_for_timeout(300); pg.evaluate(SESS, [role, X or {}])
            pg.goto(f'http://127.0.0.1:{port}/catalogue.html'); pg.wait_for_timeout(6500); return pg, ctx
        LS = lambda pg, k: pg.evaluate("k=>JSON.parse(localStorage.getItem(k)||'null')", k)
        pg, ctx = ouvre()
        T = LS(pg, 'prix-pc-v1')
        check('le Catalogue (Patron) publie les prix pour Perfume City', bool(T) and isinstance(T.get('p'), dict) and len(T['p']) > 100, (T or {}).get('t'))
        att = pg.evaluate("c=>{ const p=tousLesArticles().find(x=>x.id===c); const cs=canaux().find(x=>x.id==='site'); return [prixCanal(p,cs).v, +p.pa]; }", A[15])
        check('LE POINT — un code-barres porte [prix de vente de perfumestrade.com, prix d\'achat]', T['p'].get(nz(A[0])) == att, [T['p'].get(nz(A[0])), att])
        # un prix de vente et un prix d'achat changés dans la fiche
        pg.evaluate("c=>{ const M=lit('fiches-modifiees-v1',{}); M[c]=Object.assign({},M[c]||{},{pvr:123.45,pa:61.5}); MOD[c]=M[c]; ecrit('fiches-modifiees-v1',M); }", A[15])
        pg.wait_for_timeout(4500)
        T2 = LS(pg, 'prix-pc-v1')
        check('LE POINT — prix de vente et prix d\'achat changés dans la fiche : republiés tout seuls (sans bouton)', T2['p'].get(nz(A[0])) == [123.45, 61.5], T2['p'].get(nz(A[0])))
        # deux fiches au même code, prix différents → à part ; fiche coupée de Perfume City → absente
        pg.evaluate("""([a,b])=>{ const M=lit('fiches-modifiees-v1',{}); M[b]=Object.assign({},M[b]||{},{pcOff:['perfumecity']}); ecrit('fiches-modifiees-v1',M);
          const AJ=lit('articles-ajoutes-v1',[]); AJ.push({id:'aDouble',bc:a,nom:'Double essai',marque:'X',ml:'3.4',type:'EDP',qte:1,pvr:99,pa:10}); ecrit('articles-ajoutes-v1',AJ); }""", [A[0], Bf[15]])
        pg.reload(); pg.wait_for_timeout(6500)
        T3 = LS(pg, 'prix-pc-v1')
        check('un code porté par deux fiches qui ne disent pas la même chose est mis à part (jamais touché)', nz(A[0]) in T3.get('amb', []) and nz(A[0]) not in T3['p'], [T3.get('amb', [])[:5]])
        check('une fiche coupée du canal Perfume City n\'est pas publiée', nz(Bf[0]) not in T3['p'])
        ctx.close()
        pg, ctx = ouvre(role='commercial')
        check('un Commercial ne publie rien', LS(pg, 'prix-pc-v1') is None)
        ctx.close()
        check('aucune erreur JS', not err, err[:4])
        b.close()
finally:
    srv.terminate()
print(f'{ok} ok, {len(ko)} KO')
raise SystemExit(1 if ko else 0)
