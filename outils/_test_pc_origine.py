# PERFUME CITY : EN BOUTIQUE OU EN LIGNE (Igal, 31 oct. 2026 : « repérer les ventes du site Shopify de Perfume City et les
# ventes en boutique » ; « dans la case Perfume City du haut, deux chiffres, boutique et online »). Le cockpit garde l'origine
# de chaque commande Shopify (pc-origine-v1 : « boutique » = la caisse POS, « en ligne » = perfumeinthecity.com). Ce test protège :
#   1. LE POINT : la ligne d'une vente de Perfume City dit « en boutique » ou « en ligne », à côté du paiement ;
#   2. un remboursement prend l'origine de sa commande (même numéro) ;
#   3. LE POINT : la tuile Perfume City de « Par canal » donne deux chiffres, Boutique et Online ; les autres canaux n'en ont pas ;
#   4. l'Inventaire Perfume City dit « tester », plus « vitrine » ;
#   5. LE POINT (7 nov. 2026, Igal : « Perfume City a deux types de vente sur Shopify, boutique et en ligne — le rajouter en
#      réglages ») : Réglages › Canaux a une ligne « Perfume City — en ligne » avec sa commission et son envoi ; une commission
#      en ligne de 10 % et un envoi de 5 $ ne touchent que la vente EN LIGNE (PC-102 : 80 − 8 − 5 = marge réduite de 13 $), la
#      boutique garde ses 3 % ; le tableau de bord (récap) fait le même calcul ;
#   6. aucune erreur JS.
import subprocess, time, socket, json
from playwright.sync_api import sync_playwright
D = '/home/claude/catalogue'
ok = 0; ko = []
def check(n, c, i=''):
    global ok
    if c: ok += 1; print('  ok  ', n)
    else: ko.append(n); print('  KO  ', n, str(i)[:400])
C = json.load(open(D + '/cat.json'))
A = [r for r in C if (r[6] or 0) > 0 and r[0] and r[0].isdigit() and (r[12] or 0) > 0][0]
def vente(i, num, q, p, retour=False, auto='shopify-pc', canal='Perfume City'):
    f = {'id': 'f' + i, 'num': num, 'sens': 'vente', 'canal': canal, 'auto': auto, 'd': '2026-10-30', 'h': '12:00', 't': '2026-10-30T16:00:00Z',
         'stock': False, 'par': 'auto', '_i': 'fa|' + auto + '|' + i, 'lignes': [{'cle': A[15], 'bc': A[0], 'ref': A[2] + ' ' + A[13], 'q': q, 'p': p}],
         'montant': q * p}
    if retour: f.update({'retour': True, 'refNum': num, 'montant': q * p, '_i': 'fa|' + auto + '|r|' + i})
    return f
F = [vente('101', 'PC-101', 2, 50), vente('102', 'PC-102', 1, 80), vente('9001', 'PC-101', -1, 50, retour=True),
     vente('w1', 'W-1', 1, 40, auto='woocommerce', canal='Site perfumestrade.com'),
     vente('1867', 'PC-1867', 1, 17.5)]   # 8 nov. 2026 : commande passée par une application (source « 3890849 »), reçue sur le poste de Sam
F[-1]['par'] = 'Sam'; F[-1]['paie'] = {'especes': 13.39, 'carte': 13.39, 'autre': 0, 'approx': True}
ORIG = {'shopify-pc|101': 'boutique', 'shopify-pc|102': 'en ligne', 'shopify-pc|1867': 'Shopify Collective'}
PAIE = {'shopify-pc|101': {'especes': 100, 'carte': 0, 'autre': 0}, 'shopify-pc|1867': {'especes': 0, 'carte': 26.78, 'autre': 0, 'port': 6.9}}
s = socket.socket(); s.bind(('127.0.0.1', 0)); port = s.getsockname()[1]; s.close()
srv = subprocess.Popen(['python3', '-m', 'http.server', str(port), '--bind', '127.0.0.1'], cwd=D, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)
try:
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1500, 'height': 1000}); err = []
        pg.on('pageerror', lambda e: err.append(str(e)))
        base = f'http://127.0.0.1:{port}/'
        pg.goto(base + 'accueil.html'); pg.wait_for_timeout(300)
        pg.evaluate("""([F,O,bc,P])=>{ localStorage.clear(); localStorage.setItem('sam-comptes-demo-v1','0'); localStorage.setItem('caisse-paie-v1',JSON.stringify(P));
          localStorage.setItem('sam-session-v1',JSON.stringify({id:'sam',nom:'Sam',role:'patron',depuis:new Date().toISOString()}));
          localStorage.setItem('langue-v1','fr'); localStorage.setItem('factures-v1',JSON.stringify(F)); localStorage.setItem('pc-origine-v1',JSON.stringify(O));
          localStorage.setItem('pc-stock-v1',JSON.stringify({[bc.replace(/^0+/,'')]:{bc:bc,nom:'x',m:'y',ml:'',ty:'',q:4,pa:null,pvr:null,pvw:null,cle:'b'+bc}}));
          localStorage.setItem('testeurs-pc-v1',JSON.stringify({[bc.replace(/^0+/,'')]:{n:2}})); }""", [F, ORIG, A[0], PAIE])
        pg.goto(base + 'ventes.html'); pg.wait_for_timeout(2500)
        pg.evaluate("()=>{ $('fp').value=''; vus=80; dessine(); }"); pg.wait_for_timeout(500)
        ou = pg.evaluate("()=>Object.fromEntries(V.map(v=>[v.num+(v.ret?'-R':''),v.ou||'']))")
        check('LE POINT — PC-101 en boutique, PC-102 en ligne ; la vente du site n\'a pas d\'origine Perfume City', ou.get('PC-101') == 'boutique' and ou.get('PC-102') == 'en ligne' and ou.get('W-1') == '', ou)
        check('le remboursement de PC-101 prend l\'origine de sa commande (boutique)', ou.get('PC-101-R') == 'boutique', ou)
        T = pg.inner_text('#tb') if pg.query_selector('#tb') else pg.inner_text('body')
        chips = pg.evaluate("()=>[...document.querySelectorAll('#tb .ch, .ch')].filter(c=>/Perfume City/.test(c.textContent)).map(c=>[c.textContent.replace(/\s+/g,' ').trim(), c.className])")
        check('LE POINT (8 nov. 2026, Igal : « online ou boutique directement sur le logo, beaucoup plus visible ») — la pastille dit « Perfume City · Boutique » / « Perfume City · En ligne », la version en ligne en plein',
              any(c[0] == 'Perfume City · Boutique' for c in chips) and any(c[0] == 'Perfume City · En ligne' and 'ou-ligne' in c[1] for c in chips), chips[:6])
        print('1b. 8 nov. 2026 — la fenêtre d\'une vente de Perfume City : origine vraie, encaissement détaillé, « Sam » n\'est que le poste')
        def detail(num, lang='fr'):
            if lang != 'fr':
                pg.evaluate("l=>localStorage.setItem('langue-v1',l)", lang); pg.reload(); pg.wait_for_timeout(2500)
                pg.evaluate("()=>{ $('fp').value=''; vus=80; dessine(); }"); pg.wait_for_timeout(400)
            pg.evaluate("n=>{ const x=V.find(r=>r.num===n&&!r.ret); ouvreDetail(x); }", num); pg.wait_for_timeout(400)
            t = pg.inner_text('#d-corps'); pg.evaluate("()=>fermeDetail()"); return t
        t = detail('PC-1867')
        check('LE POINT — PC-1867 : « passée par « Shopify Collective » », pas « facture créée dans l\'ERP par Sam »', 'Shopify Collective' in t and 'ni la caisse de la boutique' in t and 'créée dans l\'ERP' not in t, t[t.find('Saisie'):t.find('Saisie') + 400])
        check('LE POINT — enregistrée « Automatique — Perfume City », reçue par l\'ERP ouvert chez Sam', 'Automatique' in t and 'Reçue par l\'ERP ouvert chez' in t and 'Sam' in t, t[t.find('Saisie'):t.find('Saisie') + 300])
        check('LE POINT — encaissement détaillé relu par le cockpit : carte 26,78 $, pas d\'espèces, pas « estimé »', 'Carte bancaire' in t and '26,78' in t and 'Espèces' not in t[t.find('Encaissé'):t.find('Encaissé') + 200] and 'ESTIMÉ' not in t, t[t.find('Paiement'):t.find('Paiement') + 400])
        pf = pg.evaluate("()=>{ const x=V.find(r=>r.num==='PC-1867'&&!r.ret); return [x.portF, x.portMt, x.mg, x.mt, x.pa, x.comMt||0, x.envoiMt||0]; }")
        check('LE POINT — le port payé par le client (6,90 $, relu chez Shopify avec le paiement) compte pour PC-1867, dans la marge', pf and pf[0] == 6.9 and pf[1] == 6.9 and (pf[4] is None or abs(pf[2] - (pf[3] - pf[4] - pf[5] - pf[6] + 6.9)) < 0.02), pf)
        pg.goto(base + 'tableau.html'); pg.wait_for_timeout(2500)
        pf2 = pg.evaluate("()=>{ try{ const L=rcLignes?rcLignes():null; const x=(L||[]).find(r=>r.num==='PC-1867'); return x?[x.portF,x.portMt]:'absent'; }catch(e){ return 'erreur '+e.message; } }")
        check('… et au tableau de bord aussi', isinstance(pf2, list) and pf2[0] == 6.9 and pf2[1] == 6.9, pf2)
        pg.goto(base + 'ventes.html'); pg.wait_for_timeout(2500); pg.evaluate("()=>{ $('fp').value=''; vus=80; dessine(); }"); pg.wait_for_timeout(400)
        t = detail('PC-101')
        check('PC-101 : « caisse Shopify (POS) de la boutique », espèces 100 $', 'caisse Shopify (POS)' in t and 'Espèces' in t and '100,00' in t, t[t.find('Paiement'):t.find('Paiement') + 300])
        check('8 nov. 2026 (Igal) : plus de ligne « Prix pratiqués » dans la fenêtre', 'Prix pratiqués' not in t and 'Prices charged' not in t)
        t = detail('PC-1867', 'en')
        check('en anglais : « through “Shopify Collective” », « Automatic », « Collected, per Shopify », « Card »', 'Shopify Collective' in t and 'Automatic' in t and 'Collected, per Shopify' in t and 'Card' in t and 'Received by the ERP open at' in t, t[:600])
        ch = pg.evaluate("()=>[...document.querySelectorAll('.ch')].map(c=>c.textContent.replace(/\s+/g,' ').trim())")
        check('en anglais : pastilles « Perfume City · Store » et « Perfume City · Online »', 'Perfume City · Store' in ch and 'Perfume City · Online' in ch, [c for c in ch if 'Perfume' in c][:4])
        t = detail('PC-1867', 'es')
        check('en espagnol : « hecho por « Shopify Collective » », « Automático », « Cobrado, según Shopify », « Tarjeta »', 'Shopify Collective' in t and 'Automático' in t and 'Cobrado, según Shopify' in t and 'Tarjeta' in t, t[:600])
        ch = pg.evaluate("()=>[...document.querySelectorAll('.ch')].map(c=>c.textContent.replace(/\s+/g,' ').trim())")
        check('en espagnol : pastilles « Perfume City · Tienda » et « Perfume City · En línea »', 'Perfume City · Tienda' in ch and 'Perfume City · En línea' in ch, [c for c in ch if 'Perfume' in c][:4])
        pg.evaluate("l=>localStorage.setItem('langue-v1',l)", 'fr'); pg.reload(); pg.wait_for_timeout(2500); pg.evaluate("()=>{ $('fp').value=''; vus=80; dessine(); }"); pg.wait_for_timeout(400)
        tuile = pg.evaluate("()=>{ const t=[...document.querySelectorAll('.cxt')].find(x=>/perfume/i.test(x.dataset.c)); return t?t.innerText:null; }")
        check('LE POINT — la tuile Perfume City donne Boutique et Online (100 − 50 de remboursement = 50 $ ; 80 $)', tuile and 'Boutique' in tuile and 'Online' in tuile and '50' in tuile and '80' in tuile, tuile)
        autre = pg.evaluate("()=>{ const t=[...document.querySelectorAll('.cxt')].find(x=>/perfumestrade/i.test(x.dataset.c)); return t?t.innerText:null; }")
        check('la tuile du site n\'a pas ces deux chiffres', autre is not None and 'Boutique' not in autre, autre)
        pg.goto(base + 'inventaire_pc.html'); pg.wait_for_timeout(2500)
        pg.fill('#q', A[0]); pg.wait_for_timeout(500)
        T = pg.inner_text('body')
        check('LE POINT — l\'Inventaire Perfume City dit « +1 tester » (un par parfum, même si la donnée ancienne en disait 2), plus « vitrine »', '+1 tester' in T and '+2 testers' not in T and 'vitrine' not in T.lower(), T[T.find('tester') - 80:T.find('tester') + 40] if 'tester' in T else T[:200])
        print('5. Réglages : Perfume City — en ligne')
        pg.goto(base + 'reglages.html'); pg.wait_for_timeout(2000)
        pg.evaluate("()=>{ const b=document.querySelector('[data-t=\"prix\"]'); if(b) b.click(); }"); pg.wait_for_timeout(400)
        T = pg.inner_text('#canaux')
        check('LE POINT — la ligne « Perfume City — en ligne (perfumeinthecity.com) » est là, sous Perfume City, avec commission et envoi', 'en ligne' in T and pg.locator('#canaux input[data-k="comLigne"]').count() == 1 and pg.locator('#env-shopify-pc').count() == 1, T[:300])
        pg.fill('#canaux input[data-k="comLigne"]', '10'); pg.locator('#canaux input[data-k="comLigne"]').dispatch_event('input'); pg.wait_for_timeout(200)
        pg.fill('#env-shopify-pc', '5'); pg.locator('#env-shopify-pc').dispatch_event('input'); pg.wait_for_timeout(600)
        R = pg.evaluate("()=>JSON.parse(localStorage.getItem('reglages-v1')||'{}')")
        pc = next((c for c in R.get('canaux', []) if c.get('id') == 'perfumecity'), {})
        check('réglé : commission en ligne 10 %, envoi 5 $ ; la boutique garde ses 2,5 % + 0,10 $', pc.get('comLigne') == 10 and (R.get('envois') or {}).get('shopify-pc') == 5 and pc.get('com') == 2.5 and pc.get('fixe') == 0.1, (pc, R.get('envois')))
        pg.goto(base + 'ventes.html'); pg.wait_for_timeout(2500)
        pg.evaluate("()=>{ $('fp').value=''; vus=80; dessine(); }"); pg.wait_for_timeout(500)
        M = pg.evaluate("()=>Object.fromEntries(V.filter(v=>!v.ret).map(v=>[v.num,{com:v.com,comMt:v.comMt,envoi:v.envoiMt||0,mg:v.mg}]))")
        check('LE POINT — Ventes : PC-102 (en ligne) commission 10 % de 80 + 0,30 fixe = 8,30 $ et envoi 5 $ ; PC-101 (boutique) 2,5 % + 0,10 $, pas d\'envoi', M['PC-102']['com'] == 10 and abs(M['PC-102']['comMt'] - 8.3) < 0.005 and M['PC-102']['envoi'] == 5 and M['PC-101']['com'] == 2.5 and abs(M['PC-101']['comMt'] - 2.6) < 0.005 and M['PC-101']['envoi'] == 0, M)
        pg.goto(base + 'tableau.html'); pg.wait_for_timeout(3000)
        M2 = pg.evaluate("()=>Object.fromEntries(rcLignes().filter(v=>!v.ret&&/^PC-/.test(v.num)).map(v=>[v.num,{com:v.com,comMt:v.comMt,envoi:v.envoiMt||0}]))")
        check('LE POINT — le tableau de bord fait le même calcul', M2['PC-102']['com'] == 10 and abs(M2['PC-102']['comMt'] - 8.3) < 0.005 and M2['PC-102']['envoi'] == 5 and M2['PC-101']['com'] == 2.5 and abs(M2['PC-101']['comMt'] - 2.6) < 0.005, M2)
        check('aucune erreur JS', not err, err[:3])
        b.close()
finally:
    srv.terminate()
print(f"\n{ok} ok, {len(ko)} KO", ko)
