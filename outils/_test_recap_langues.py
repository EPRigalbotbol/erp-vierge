# LE RÉCAPITULATIF SOUS LES LIGNES, DANS LA LANGUE DE LA PAGE (photo de Sam, 10 nov. 2026, page Offre en anglais :
# « Sale de 5 bottles sur Wholesale pour 146,50 $. Ces flacons ont coûté… »). Ce test protège :
#   1. LE POINT — en anglais et en espagnol, le récapitulatif d'une offre n'a plus un mot de français ;
#   2. il dit « Offer / Oferta / Offre », pas « Vente », et le canal est traduit (Wholesale, Mayorista) ;
#   3. une offre ne sort rien du stock : pas de « stock insuffisant — la vente est enregistrée quand même » ;
#   4. dans Ventes, le récapitulatif dit toujours « Vente de … » ;
#   5. aucune erreur JS.
import subprocess, time, socket, re
from playwright.sync_api import sync_playwright
D = '/home/claude/catalogue'; ok = 0; ko = []
def check(n, c, i=''):
    global ok
    if c: ok += 1; print('  ok  ', n)
    else: ko.append(n); print('  KO  ', n, str(i)[:300])
s = socket.socket(); s.bind(('127.0.0.1', 0)); port = s.getsockname()[1]; s.close()
srv = subprocess.Popen(['python3', '-m', 'http.server', str(port), '--bind', '127.0.0.1'], cwd=D, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)
FR = re.compile(r'\b(Vente|Ventes|flacons?|sur|pour|Ces|coûté|marge|bouge|insuffisant|enregistrée|Gros)\b')
try:
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1280, 'height': 800}); err = []
        pg.on('pageerror', lambda e: err.append(str(e)))
        base = f'http://127.0.0.1:{port}/'
        def recap(page, lg):
            pg.goto(base + 'accueil.html'); pg.wait_for_timeout(300)
            pg.evaluate("""lg=>{ localStorage.clear(); localStorage.setItem('sam-comptes-demo-v1','0'); localStorage.setItem('langue-v1',lg);
              localStorage.setItem('sam-comptes-v1',JSON.stringify([{ident:'sam',nom:'Sam',role:'patron',actif:true,h:'x'}]));
              localStorage.setItem('sam-session-v1',JSON.stringify({id:'sam',nom:'Sam',role:'patron',depuis:new Date().toISOString()})); }""", lg)
            pg.goto(base + page); pg.wait_for_timeout(3000)
            return pg.evaluate("""()=>{ if(window.coteNouvelle) window.coteNouvelle(); else ouvreVente();
              const ks=Object.keys(IDX).filter(c=>pvwEff(c)>0&&stkC(c,canalCour().nom)<5).slice(0,2); ks.forEach(k=>PANIER.push({cle:k,q:9,p:prixLigne(k,canalCour())}));
              $('v-client').value='Test Client'; peintPanier(); recap(); return $('v-recap').innerText; }""")
        for lg, mot, canal in [('en', 'Offer of', 'Wholesale'), ('es', 'Oferta de', 'Mayorista')]:
            t = recap('offres.html', lg)
            check(f'LE POINT — {lg} : plus un mot de français dans le récapitulatif de l\'offre', not FR.search(t), FR.findall(t))
            check(f'{lg} : « {mot} … {canal} »', t.startswith(mot) and canal in t, t[:120])
        t = recap('offres.html', 'fr')
        check('fr : « Offre de … »', t.startswith('Offre de'), t[:80])
        check('une offre ne parle pas de stock insuffisant ni de vente enregistrée', 'insuffisant' not in t and 'enregistrée' not in t, t)
        t = recap('ventes.html', 'fr')
        check('dans Ventes : « Vente de … », et le stock insuffisant est toujours signalé', t.startswith('Vente de') and 'insuffisant' in t, t[:300])
        check('aucune erreur JS', not err, err[:3])
        b.close()
finally:
    srv.terminate()
print(f'\n{ok} ok, {len(ko)} KO', ko); raise SystemExit(1 if ko else 0)
