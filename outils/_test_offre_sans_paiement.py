# LA PAGE OFFRE SANS PAIEMENT NI SALES TAX (Igal, 11 nov. 2026 : « sur la partie offre, enlève toute cette partie, elle sert à rien.
# On s'en fout des paiements, puisqu'une offre ne peut pas être payée »). Ce test protège :
#   1. LE POINT — page Offre : paiement, réglé, remise, frais d'envoi, langue, taux, sales tax et totaux ne s'affichent plus ;
#   2. LE POINT — même si ces cases gardaient une valeur, l'offre enregistrée n'a ni taxe, ni remise, ni frais : total = prix × quantités ;
#   3. la fiche du client n'est pas touchée (son statut fiscal et son mode de paiement restent les siens) ;
#   4. le document de l'offre n'a ni « Conditions / Paiement », ni ligne Sales tax, ni « Pour régler » ;
#   5. la page Cote garde tous ses réglages ;
#   6. aucune erreur JS.
import subprocess, time, socket
from playwright.sync_api import sync_playwright
D = '/home/claude/catalogue'; ok = 0; ko = []
def check(n, c, i=''):
    global ok
    if c: ok += 1; print('  ok  ', n)
    else: ko.append(n); print('  KO  ', n, str(i)[:300])
s = socket.socket(); s.bind(('127.0.0.1', 0)); port = s.getsockname()[1]; s.close()
srv = subprocess.Popen(['python3', '-m', 'http.server', str(port), '--bind', '127.0.0.1'], cwd=D, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)
try:
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1280, 'height': 800}); err = []
        pg.on('pageerror', lambda e: err.append(str(e))); pg.on('dialog', lambda d: d.accept())
        base = f'http://127.0.0.1:{port}/'
        def ouvre(page):
            pg.goto(base + 'accueil.html'); pg.wait_for_timeout(300)
            pg.evaluate("""()=>{ localStorage.clear(); localStorage.setItem('sam-comptes-demo-v1','0'); localStorage.setItem('langue-v1','en');
              localStorage.setItem('sam-comptes-v1',JSON.stringify([{ident:'sam',nom:'Sam',role:'patron',actif:true,h:'x'}]));
              localStorage.setItem('sam-session-v1',JSON.stringify({id:'sam',nom:'Sam',role:'patron',depuis:new Date().toISOString()})); }""")
            pg.goto(base + page); pg.wait_for_timeout(3000)
            pg.evaluate("""()=>{ const C=lit(KCLI,{}); C['Client Test']={nom:'Client Test',fiscal:'taxable',pmode:'carte'}; ecrit(KCLI,C);
              window.coteNouvelle(); const ks=Object.keys(IDX).filter(c=>pvwEff(c)>0).slice(0,2); ks.forEach(k=>PANIER.push({cle:k,q:2,p:10,pm:true}));
              $('v-client').value='Client Test'; peintPanier(); recap(); }""")
        ouvre('offres.html')
        vis = pg.evaluate("()=>['v-pmode','v-pstat','v-remval','v-port','v-langue','v-taux','v-fiscal','v-tot'].filter(i=>$(i)&&$(i).offsetParent!==null)")
        check('LE POINT — page Offre : aucun réglage de paiement / taxe / totaux visible', vis == [], vis)
        # des valeurs restées dans les cases cachées
        pg.evaluate("()=>{ $('v-remval').value='10'; $('v-port').value='15'; $('v-taux').value='7'; $('v-fiscal').value='taxable'; $('v-pmode').value='carte'; }")
        pg.click('#v-ok'); pg.wait_for_timeout(1500)
        r = pg.evaluate("()=>{ const f=FACT.find(x=>x.tiers==='Client Test'); const D=f&&f.doc; return D&&{t:D.total,st:D.sousTotal,tx:D.taxe,rem:D.remise||0,port:D.port||0,frais:D.frais||0,offre:D.offre, cli:lit(KCLI,{})['Client Test']}; }")
        check('LE POINT — l\'offre n\'a ni taxe, ni remise, ni frais : total = 2 × 10 + 2 × 10 = 40', r and r['offre'] and r['t'] == 40 and r['st'] == 40 and not r['tx'] and not r['rem'] and not r['port'] and not r['frais'], r)
        check('la fiche du client garde son statut fiscal et son mode de paiement', r and r['cli'].get('fiscal') == 'taxable' and r['cli'].get('pmode') == 'carte', r and r['cli'])
        pg.evaluate("()=>{ const f=FACT.find(x=>x.tiers==='Client Test'); dessineDoc(f); }"); pg.wait_for_timeout(800)
        t = pg.evaluate("()=>(document.querySelector('#docov .doc')||document.querySelector('#docov')).innerText")
        check('le document de l\'offre : pas de Paiement, pas de Sales tax, pas de « Pour régler »', 'Offer' in t and 'Sales tax' not in t and 'Payment' not in t and 'Paiement' not in t and 'To pay' not in t, t[:600])
        ouvre('quotes.html')
        vis = pg.evaluate("()=>['v-pmode','v-remval','v-port','v-fiscal'].filter(i=>$(i)&&$(i).offsetParent!==null)")
        check('la page Cote garde ses réglages', len(vis) == 4, vis)
        check('aucune erreur JS', not err, err[:3])
        b.close()
finally:
    srv.terminate()
print(f'\n{ok} ok, {len(ko)} KO', ko); raise SystemExit(1 if ko else 0)
