# LA RUBRIQUE OFFRE (Sam, via Igal, 10 nov. 2026 : « Carmen demande un parfum qu'elle n'a jamais acheté : Sam lui fait une offre
# de prix ; le jour où elle veut une vraie cote, la cote prend le prix de l'offre et non celui de son dernier achat »).
# Règles validées par Sam : une offre vaut 30 jours ; entre une offre et un achat, le plus récent gagne ; « Faire la cote ».
# Ce test protège :
#   1. LE POINT — une offre s'enregistre dans la rubrique Offre : n° OF-…, marquée offre, ne sort rien du stock ;
#   2. LE POINT — elle n'apparaît JAMAIS dans la liste des cotes (et une cote n'apparaît pas dans les offres) ;
#   3. LE POINT — dans une cote pour Carmen, le parfum de l'offre prend tout seul le prix de l'offre (pastille « Offre OF-… ») ;
#      un parfum sans offre garde le prix habituel ; le client tapé APRÈS les parfums remet aussi le prix de l'offre ;
#      un prix posé à la main n'est jamais remplacé ;
#   4. LE POINT — le plus récent gagne : un achat fait APRÈS l'offre garde la règle habituelle (l'offre reste visible en pastille) ;
#   5. une offre de plus de 30 jours, ou archivée, ne compte plus ;
#   6. LE POINT — « Faire la cote » ouvre la Cote avec le client et les parfums aux prix de l'offre ;
#   7. le document s'appelle « Offre » / « Offer » / « Oferta », sans bouton « convertir en facture » ;
#   8. en anglais et en espagnol : plus un mot de français dans la rubrique ; aucune erreur JS.
import pathlib, subprocess, time, socket, json, re
from playwright.sync_api import sync_playwright

D = pathlib.Path('/home/claude/catalogue')
ok = 0; ko = []
def check(n, c, i=''):
    global ok
    if c: ok += 1; print('  ok  ', n)
    else: ko.append(n); print('  KO  ', n, str(i)[:400])
CAT = json.load(open(D / 'cat.json'))
R = [r for r in CAT if (r[6] or 0) > 2 and r[7] and r[8] and r[0] and len(str(r[0])) >= 12 and len(str(r[13] or '')) > 10 and str(r[13])[0].isalpha()]
A, B, C = R[0], R[1], R[2]
s = socket.socket(); s.bind(('127.0.0.1', 0)); port = s.getsockname()[1]; s.close()
srv = subprocess.Popen(['python3', '-m', 'http.server', str(port), '--bind', '127.0.0.1'], cwd=str(D), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1)
SESS = """([l,F])=>{ localStorage.clear(); localStorage.setItem('sam-comptes-demo-v1','0');
  localStorage.setItem('sam-comptes-v1',JSON.stringify([{ident:'sam',nom:'Sam',role:'patron',actif:true,h:'x'}]));
  localStorage.setItem('sam-session-v1',JSON.stringify({id:'sam',nom:'Sam',role:'patron',depuis:new Date().toISOString()}));
  localStorage.setItem('langue-v1',l); localStorage.setItem('factures-v1',JSON.stringify(F)); }"""
import datetime
AUJ = datetime.date.today()
def J(n): return (AUJ - datetime.timedelta(days=n)).isoformat()
def offre(i, cli, d, lignes, **x):
    D0 = {'type': 'devis', 'offre': True, 'num': 'OF-2026-%04d' % (90 + i), 'pmode': 'zelle', 'pstat': 'apayer', 'langue': 'fr', 'sousTotal': 0, 'total': 0}
    D0.update(x)
    return {'id': 'o%d' % i, 'num': 'V-O%d' % i, 'd': d, 'h': '09:00', 'sens': 'devis', 'canal': 'Vente en gros', 'tiers': cli, 'par': 'Sam', 't': d + 'T13:00:00Z',
            'lignes': [{'cle': r[15], 'bc': r[0], 'ref': r[13], 'q': 1, 'p': p} for r, p in lignes], 'doc': D0}
FACT = [
  # Javier a reçu une offre sur A à 18 il y a 10 jours, puis a ACHETÉ A à 25 il y a 5 jours : l'achat est plus récent
  offre(1, 'Javier', J(10), [(A, 18)]),
  {'id': 'v1', 'num': 'PT-2026-0001', 'd': J(5), 'h': '10:00', 'sens': 'vente', 'canal': 'Vente en gros', 'tiers': 'Javier', 'lignes': [{'cle': A[15], 'bc': A[0], 'q': 2, 'p': 25}]},
  # Robert : une offre de 40 jours (périmée), et une archivée
  offre(2, 'Robert', J(40), [(A, 15)]),
  offre(3, 'Robert', J(3), [(B, 11)], archive=True),
  # une vraie cote pour Robert (doit rester dans la Cote, jamais dans les offres)
  {'id': 'c1', 'num': 'V-C1', 'd': J(2), 'h': '09:00', 'sens': 'devis', 'canal': 'Vente en gros', 'tiers': 'Robert', 'par': 'Sam', 't': J(2) + 'T13:00:00Z',
   'lignes': [{'cle': C[15], 'bc': C[0], 'ref': C[13], 'q': 3, 'p': 50}], 'doc': {'type': 'devis', 'num': 'DV-2026-0042', 'pmode': 'zelle', 'pstat': 'apayer', 'langue': 'fr', 'sousTotal': 150, 'total': 150}},
]
try:
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1456, 'height': 950}); err = []
        pg.on('pageerror', lambda e: err.append(str(e))); pg.on('dialog', lambda d: d.accept())
        base = f'http://127.0.0.1:{port}/'
        def ouvre(page, lang='fr', F=None, garde=False):
            if not garde:
                pg.goto(base + 'accueil.html'); pg.wait_for_timeout(300); pg.evaluate(SESS, [lang, F if F is not None else FACT])
            pg.goto(base + page); pg.wait_for_timeout(2600)
        def nouvelle():
            if not pg.locator('#vov').is_visible(): pg.click('#nv'); pg.wait_for_timeout(400)
        def ajoute(r):
            pg.fill('#v-q', str(r[13])[:14]); pg.wait_for_timeout(450)
            pg.click('#v-res [data-cle="%s"]' % r[15]); pg.wait_for_timeout(150)
            if pg.locator('#v-cadd').count(): pg.click('#v-cadd'); pg.wait_for_timeout(250)
        prix = lambda i: pg.evaluate("i=>PANIER[i]&&PANIER[i].p", i)

        print('1. une offre pour Carmen')
        ouvre('offres.html')
        check('la rubrique s\'ouvre : « + Nouvelle offre », la liste « Offres », pas les cotes de Lightspeed', pg.inner_text('#nv').strip() == '+ Nouvelle offre' and 'Offres' in pg.inner_text('.docs h2.sec') and pg.locator('#lsc').count() == 0,
              [pg.inner_text('#nv'), pg.inner_text('.docs h2.sec')])
        lst = pg.evaluate("[...document.querySelectorAll('#docs-table tr.qr .num b')].map(b=>b.textContent)")
        check('LE POINT — la liste montre les offres en cours seulement (la cote DV-… n\'y est jamais, ni l\'offre périmée, ni l\'archivée)', lst == ['OF-2026-0091'], lst)
        nouvelle()
        check('la fenêtre s\'appelle « Nouvelle offre », bouton « Enregistrer l\'offre »', 'Nouvelle offre' in pg.inner_text('#vov .mh h3') and 'Enregistrer l\'offre' in pg.inner_text('#v-ok'))
        pg.fill('#v-client', 'Carmen'); pg.dispatch_event('#v-client', 'change')
        ajoute(A); ajoute(B)
        pg.fill('#v-pan input[data-i="0"][data-f="p"]', '20'); pg.fill('#v-pan input[data-i="1"][data-f="p"]', '30'); pg.wait_for_timeout(200)
        stock0 = pg.evaluate("c=>qteEff(c)", A[15])
        pg.click('#v-ok'); pg.wait_for_timeout(1500)
        F = pg.evaluate("lit('factures-v1',[])")
        o = next((f for f in F if f.get('tiers') == 'Carmen'), None)
        check('LE POINT — l\'offre est enregistrée : n° OF-2026-…, marquée offre, prix 20 et 30', o and o['doc'].get('offre') is True and re.match(r'^OF-\d{4}-\d{4}$', o['doc']['num']) and [l['p'] for l in o['lignes']] == [20, 30], o and o.get('doc'))
        check('une offre ne sort rien du stock', pg.evaluate("c=>qteEff(c)", A[15]) == stock0)
        num = o['doc']['num'] if o else ''
        lst = pg.evaluate("[...document.querySelectorAll('#docs-table tr.qr .num b')].map(b=>b.textContent)")
        check('elle apparaît dans la liste des offres', num in lst, lst)

        print('2. la cote de Carmen reprend les prix de l\'offre')
        ouvre('quotes.html', garde=True)
        lst = pg.evaluate("[...document.querySelectorAll('#docs-table tr.qr .num b')].map(b=>b.textContent)")
        check('LE POINT — la liste des cotes n\'a AUCUNE offre (seulement DV-2026-0042)', lst == ['DV-2026-0042'], lst)
        nouvelle()
        pg.fill('#v-client', 'Carmen'); pg.dispatch_event('#v-client', 'change'); pg.wait_for_timeout(500)
        ajoute(A); ajoute(C)
        gros_c = pg.evaluate("c=>prixSuggere(c,canalCour())", C[15])
        check('LE POINT — le parfum de l\'offre prend tout seul le prix de l\'offre (20)', prix(0) == 20, prix(0))
        chip = pg.evaluate("(document.querySelector('#v-pan tbody tr .puc.of')||{}).textContent||''")
        check('une pastille dit d\'où vient ce prix : « Offre OF-… »', num in chip and 'Offre' in chip, chip)
        check('un parfum sans offre garde le prix habituel', prix(1) == gros_c, [prix(1), gros_c])
        # le client tapé APRÈS les parfums
        pg.evaluate("PANIER=[]; peintPanier(); $('v-client').value=''"); pg.dispatch_event('#v-client', 'change'); pg.wait_for_timeout(500)
        ajoute(B); p_avant = prix(0)
        pg.fill('#v-client', 'Carmen'); pg.dispatch_event('#v-client', 'input'); pg.wait_for_timeout(700)
        check('LE POINT — le client choisi après les parfums : la ligne passe au prix de l\'offre (30)', prix(0) == 30 and p_avant != 30, [p_avant, prix(0)])
        pg.fill('#v-pan input[data-i="0"][data-f="p"]', '28'); pg.wait_for_timeout(100)
        pg.fill('#v-client', 'Carmen '); pg.dispatch_event('#v-client', 'input'); pg.wait_for_timeout(700)
        check('un prix posé à la main n\'est jamais remplacé', prix(0) == 28, prix(0))

        print('3. le plus récent gagne, 30 jours, archivée')
        pg.evaluate("PANIER=[]; peintPanier();")
        pg.fill('#v-client', 'Javier'); pg.dispatch_event('#v-client', 'change'); pg.wait_for_timeout(500)
        ajoute(A)
        gros_a = pg.evaluate("c=>prixSuggere(c,canalCour())", A[15])
        chips = pg.evaluate("[...document.querySelectorAll('#v-pan tbody tr .puc')].map(c=>c.className+'|'+c.dataset.pv)")
        check('LE POINT — Javier a ACHETÉ après l\'offre : la règle habituelle garde la main (pas 18)', prix(0) == gros_a and prix(0) != 18, [prix(0), gros_a])
        check('… mais l\'offre et son achat restent sous ses yeux en pastilles (18 et 25)', any('of' in c and c.endswith('|18') for c in chips) and any('dp' in c and c.endswith('|25') for c in chips), chips)
        pg.evaluate("PANIER=[]; peintPanier();")
        pg.fill('#v-client', 'Robert'); pg.dispatch_event('#v-client', 'change'); pg.wait_for_timeout(500)
        ajoute(A); ajoute(B)
        check('une offre de plus de 30 jours ne compte plus (A) ; une offre archivée non plus (B)', prix(0) != 15 and prix(1) != 11 and pg.locator('#v-pan .puc.of').count() == 0, [prix(0), prix(1)])

        print('4. « Faire la cote » depuis l\'offre')
        pg.evaluate("localStorage.removeItem('cote-brouillon')")
        ouvre('offres.html', garde=True)
        pg.click('#docs-table tr.qr[data-q="%s"]' % o['id']); pg.wait_for_timeout(300)
        btns = pg.evaluate("[...document.querySelectorAll('#docs-table .btns button')].map(b=>b.textContent.trim())")
        check('l\'offre dépliée : « Faire la cote », Modifier, WhatsApp, e-mail, voir, archiver, supprimer — jamais « convertir en facture »', btns[0] == 'Faire la cote' and not any('onvert' in x for x in btns), btns)
        pg.click('#docs-table [data-qa="cote"]'); pg.wait_for_timeout(3200)
        r = pg.evaluate("({u:location.pathname, c:$('v-client').value, L:PANIER.map(l=>[l.cle,l.p]), m:$('v-msg').textContent, vis:!$('vov').hidden})")
        check('LE POINT — la Cote s\'ouvre avec Carmen et ses parfums aux prix de l\'offre (20 et 30)', r['u'].endswith('quotes.html') and r['c'] == 'Carmen' and r['vis'] and sorted(x[1] for x in r['L']) == [20, 30], r)
        check('le message dit d\'où vient la cote', num in r['m'], r['m'])
        pg.evaluate("localStorage.removeItem('cote-brouillon')")

        print('5. le document')
        ouvre('offres.html', garde=True)
        pg.click('#docs-table tr.qr[data-q="%s"]' % o['id']); pg.wait_for_timeout(300)
        pg.click('#docs-table [data-qa="voir"]'); pg.wait_for_timeout(900)
        t = pg.evaluate("({h:document.querySelector('#doc-corps .titre h2').textContent, v:document.querySelector('#doc-corps .titre').innerText, conv:getComputedStyle($('doc-conv')).display, nom:docNomPDF(DOC)})")
        check('LE POINT — le document s\'appelle « Offre », valable 30 jours, sans « convertir en facture »', t['h'].strip() == 'Offre' and '30 jours' in t['v'] and t['conv'] == 'none' and t['nom'].startswith('Offre-OF-'), t)
        x = pg.evaluate("f=>{ const g=JSON.parse(JSON.stringify(f)); g.doc.langue='en'; dessineDoc(g); return [document.querySelector('#doc-corps .titre h2').textContent, docNomPDF(g), docSujet(g)]; }", o)
        check('en anglais pour un client anglophone : « Offer »', x[0].strip() == 'Offer' and x[1].startswith('Offer-') and x[2].startswith('Offer '), x)
        x = pg.evaluate("f=>{ const g=JSON.parse(JSON.stringify(f)); g.doc.langue='es'; dessineDoc(g); return [document.querySelector('#doc-corps .titre h2').textContent, docNomPDF(g)]; }", o)
        check('en espagnol : « Oferta »', x[0].strip() == 'Oferta' and x[1].startswith('Oferta-'), x)
        txt = pg.evaluate("f=>docTexte0(f,'')", o)
        check('le message WhatsApp parle d\'offre de prix valable 30 jours', 'offre de prix, valable 30 jours' in txt, txt[:200])
        pg.evaluate("$('doc-x').click()")

        print('6. en anglais / espagnol')
        FRW = re.compile(r"\b(Offres?|Nouvelle|Enregistrer|Faire la cote|Modifier|Envoyer|Archiver|Supprimer|Chercher|Créée|Valable|jusqu|parfums?|En cours|Expirée|aucune)\b")
        for lg in ('en', 'es'):
            ouvre('offres.html', lg, F)
            pg.click('#docs-table tr.qr[data-q="%s"]' % o['id']); pg.wait_for_timeout(300)
            nouvelle()
            T = pg.evaluate("()=>{ const z=document.createElement('div'); ['#nv','.docs h2.sec','#docs-table','#vov .mh h3','#v-ok','#v-cadd'].forEach(s=>{ const e=document.querySelector(s); if(e){ const c=e.cloneNode(true); c.querySelectorAll('[data-nolang] b,.num b,td:nth-child(3) b').forEach(x=>x.remove()); z.appendChild(c); } }); return z.innerText; }")
            m = FRW.search(T)
            check(f'{lg} : la rubrique Offre est traduite, plus un mot de français', not m, (m.group(0) if m else '', T[:500]))
            mot = {'en': 'Offer', 'es': 'Oferta'}[lg]
            check(f'{lg} : le menu dit « {mot} »', mot in pg.evaluate("(document.querySelector('a.nv[href^=\"offres.html\"]')||{}).textContent||''"), pg.evaluate("(document.querySelector('a.nv[href^=\"offres.html\"]')||{}).textContent||''"))
        check('aucune erreur JS', not err, err[:3])
        b.close()
finally:
    srv.terminate()
print(f'\n{ok} ok, {len(ko)} KO', ko); raise SystemExit(1 if ko else 0)
