# UNE FICHE RETIRÉE DU CATALOGUE (12 nov. 2026 — Igal : « dans Tâches, quand je fais Ouvrir sur le premier, j'ai une page blanche »).
# Deux fiches portaient le même code-barres : l'une retirée du catalogue (le 30 oct.), l'autre en service. La vente de la boutique
# s'était accrochée à la fiche RETIRÉE : mauvais prix d'achat (fausse « vente à perte »), et le bouton « Ouvrir » de la tâche ouvrait
# une fenêtre vide, parce que le Catalogue ne sait ouvrir que les fiches de sa liste. Ce test protège :
#   1. LE POINT — une vente qui arrive avec ce code va à la fiche EN SERVICE, jamais à la fiche retirée ;
#   2. si le code n'existe que sur une fiche retirée, la vente la garde quand même (une vente ne se perd pas) ;
#   3. LE POINT — un lien vers une fiche retirée ouvre CETTE fiche (avec « Remettre au catalogue »), jamais une fenêtre vide ;
#   4. un lien vers une fiche en service s'ouvre toujours ; aucune erreur JS.
import pathlib, subprocess, time, socket, json, sys
from playwright.sync_api import sync_playwright
D = pathlib.Path(__file__).resolve().parent; ok = 0; ko = []
def check(n, c, i=''):
    global ok
    if c: ok += 1; print('  ok  ', n)
    else: ko.append(n); print('  KO  ', n, str(i)[:400])
C = json.load(open(D / 'cat.json'))
simples = [r for r in C if r[0] and str(r[0]).isdigit() and len(str(r[0])) >= 12 and r[15] and sum(1 for x in C if x[0] == r[0]) == 1]
if len(simples) < 3: print('catalogue vide (copie vierge) : rien à vérifier ici'); sys.exit(0)
zeros = [r for r in simples if not (r[6] or 0)]
if len(zeros) < 2: zeros = simples          # un petit catalogue (la copie vierge) : n'importe quelles fiches font l'affaire
M, SEUL = zeros[0], zeros[1]                 # deux fiches à 0 en stock, retirées du catalogue
V = next(r for r in simples if C.index(r) > C.index(M) and r is not SEUL)   # une fiche en service, plus loin dans le fichier
s = socket.socket(); s.bind(('127.0.0.1', 0)); port = s.getsockname()[1]; s.close()
srv = subprocess.Popen(['python3', '-m', 'http.server', str(port), '--bind', '127.0.0.1'], cwd=str(D), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(0.8)
SESS = """([m,v,seul,bc])=>{ localStorage.clear(); localStorage.setItem('sam-comptes-demo-v1','0');
  localStorage.setItem('sam-session-v1',JSON.stringify({id:'sam',nom:'Sam',role:'patron',depuis:new Date().toISOString()}));
  localStorage.setItem('langue-v1','fr');
  const R={masque:true,masquePar:'Sam',masqueLe:'2026-10-30T20:00:00Z'};
  /* la fiche en service porte le MÊME code que la fiche retirée (le code posé sur la fiche) */
  localStorage.setItem('fiches-modifiees-v1',JSON.stringify({[m]:R,[seul]:R,[v]:{bc:bc}})); }"""
try:
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1400, 'height': 900}); err = []
        pg.on('pageerror', lambda e: err.append(str(e)))
        base = f'http://127.0.0.1:{port}/'
        pg.goto(base + 'accueil.html'); pg.wait_for_timeout(300); pg.evaluate(SESS, [M[15], V[15], SEUL[15], M[0]])
        print('1. la vente va à la fiche en service')
        pg.goto(base + 'ventes.html'); pg.wait_for_timeout(2500)
        r = pg.evaluate("([bc,seul])=>{ const X=faContexte(); return [X.cleDe({bc:bc,des:'x'}), X.cleDe({bc:seul,des:'x'})]; }", [M[0], SEUL[0]])
        check('LE POINT — deux fiches, le même code-barres, l\'une retirée du catalogue : la vente va à la fiche EN SERVICE', r[0] == V[15], [r[0], M[15], V[15]])
        check('un code qui n\'existe que sur une fiche retirée : la vente garde cette fiche (elle ne se perd pas)', r[1] == SEUL[15], r)
        print('2. le lien vers une fiche retirée')
        pg.goto(base + 'catalogue.html#cle=' + M[15]); pg.wait_for_timeout(3000)
        v = pg.evaluate("()=>[document.getElementById('dr').classList.contains('on'), document.getElementById('fx').value, (FICHE||{}).id, document.getElementById('dr').innerText]")
        check('LE POINT — le lien ouvre la fiche retirée (jamais une fenêtre vide), sur le filtre « Retirées du catalogue »', v[0] and v[1] == 'retire' and v[2] == M[15] and len(v[3]) > 200, [v[0], v[1], v[2], len(v[3])])
        check('… et la fiche propose « Remettre au catalogue »', 'Remettre au catalogue' in v[3], v[3][-300:])
        pg.goto(base + 'accueil.html'); pg.wait_for_timeout(200)
        pg.goto(base + 'catalogue.html#cle=' + V[15]); pg.wait_for_timeout(3000)
        v = pg.evaluate("()=>[document.getElementById('dr').classList.contains('on'), document.getElementById('fx').value, (FICHE||{}).id]")
        check('un lien vers une fiche en service s\'ouvre comme avant (filtre « toutes »)', v[0] and v[1] == '' and v[2] == V[15], v)
        check('aucune erreur JS', not err, err[:3])
        b.close()
finally:
    srv.terminate()
print(f'\n{ok} ok, {len(ko)} KO', ko); sys.exit(1 if ko else 0)
