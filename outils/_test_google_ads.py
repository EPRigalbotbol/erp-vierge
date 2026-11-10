# LES CAMPAGNES GOOGLE ADS EN DIRECT DANS L'ANALYTIQUE (Igal, 10 nov. 2026 : « que je puisse récupérer toutes les infos en
# live pour l'analytique de l'ERP »). Un script posé dans Google Ads envoie ses chiffres au cockpit (google-ads-v1). Ce test protège :
#   1. LE POINT — la carte « Les campagnes Google Ads » : actives / en pause, budget, coût 30 j, ventes pour 1 $, résultat estimé ;
#      les campagnes en pause sans dépense sont comptées, pas listées ;
#   2. LE POINT — les chiffres du script remplacent ceux de l'extension pour la pub payante (toutes les campagnes), les fiches
#      gratuites restent celles de l'extension ; la liste parfum par parfum vient du script ;
#   3. sans nouvelles depuis plus de 3 heures, la carte le dit ;
#   4. LE POINT — pas encore branché : un bouton affiche le script à coller (demandé au cockpit), avec les étapes et « Copier » ;
#   5. le dossier de la stratégie connaît chaque campagne ;
#   6. en anglais (et en espagnol, qui lit l'anglais) : plus un mot de français dans la carte ; aucune erreur JS.
import subprocess, time, socket, json, re, os, datetime
from zoneinfo import ZoneInfo
from playwright.sync_api import sync_playwright
D = '/home/claude/catalogue'
ok = 0; ko = []
def check(n, c, i=''):
    global ok
    if c: ok += 1; print('  ok  ', n)
    else: ko.append(n); print('  KO  ', n, str(i)[:500])
C = json.load(open(D + '/cat.json'))
def a(t, n):   # « 650 $ » (fr) ou « $650 » (en) : le montant n est-il écrit dans t ?
    t = t.replace('\u202f', ' ').replace('\xa0', ' ')
    return bool(re.search(r'(?<![\d,.])' + re.escape(format(n, ',').replace(',', ' ')) + r' \$', t) or re.search(r'\$' + re.escape(format(n, ',')) + r'(?![\d,])', t))
A = [r for r in C if (r[6] or 0) > 20 and r[0] and r[0].isdigit() and (r[12] or 0) > 0][0]
cle, bc = A[15], A[0]
auj = datetime.date(2026, 11, 15)
def J(n): return (auj - datetime.timedelta(days=n)).isoformat()
def ligne(q, p, paAv=40.0): return {'cle': cle, 'bc': bc, 'ref': 'x', 'q': q, 'p': p, 'paAv': paAv}
def site(i, n, p, jours, src='woocommerce', canal='Site perfumestrade.com'):
    return {'id': 'w%d' % i, 'num': str(i), 'sens': 'vente', 'canal': canal, 'tiers': 'X', 'd': J(jours), 'auto': src, '_i': 'fa|%s|%d' % (src, i), 'lignes': [ligne(n, p)]}
F = [site(1, 1, 100, 2), site(2, 2, 100, 3), site(3, 1, 100, 4), site(4, 1, 100, 5), site(5, 1, 60, 6, 'woocommerce-gros', 'Site wholesale.perfumestrade.com'),
     {'id': 'p1', 'num': 'PC-1', 'sens': 'vente', 'canal': 'Perfume City', 'tiers': '', 'd': J(2), 'auto': 'shopify-pc', '_i': 'fa|shopify-pc|11', 'lignes': [ligne(1, 90)]},
     {'id': 'p2', 'num': 'PC-2', 'sens': 'vente', 'canal': 'Perfume City', 'tiers': '', 'd': J(2), 'auto': 'shopify-pc', '_i': 'fa|shopify-pc|12', 'lignes': [ligne(1, 90)]},
     {'id': 'g1', 'num': 'PT-1', 'sens': 'vente', 'canal': 'Gros', 'tiers': 'Carmen', 'd': J(8), 'lignes': [ligne(10, 55)]},
     # la période d'avant (30 jours plus tôt) : une commande Google Ads
     site(9, 1, 100, 40)]
ORIG = {'woocommerce|1': 'gshop', 'woocommerce|2': 'gads', 'woocommerce|3': 'gads', 'woocommerce|4': 'direct', 'woocommerce-gros|5': 'social:instagram',
        'shopify-pc|12': 'google', 'woocommerce|9': 'gads', '_woocommerce': {'reprise': '2026-11-09T10:00:00Z', 'maj': '2026-11-15T13:50:00Z', 'lues': 9, 'connues': 9, 'err': ''},
        '_shopify-pc': {'maj': '2026-11-15T13:50:00Z', 'err': 'Shopify : Access denied for customerJourneySummary field.'},
        '_attente_woocommerce': {'maj': '2026-11-15T13:50:00Z', 'L': [{'id': 31, 'd': '2026-11-15', 'mt': 110, 'o': 'gads'}, {'id': 32, 'd': '2026-11-14', 'mt': 90, 'o': 'gads'}, {'id': 33, 'd': '2026-11-14', 'mt': 50, 'o': 'direct'}]}}
PCO = {'shopify-pc|11': 'boutique', 'shopify-pc|12': 'en ligne'}
B0 = [r for r in C if (r[6] or 0) <= 0 and r[0] and r[0].isdigit() and (r[12] or 0) > 0 and (r[7] or 0) > 0 and r[15] != cle][0]
GPUB = {'j': {J(2): [50, 300, 20, 1000, 2, 1, 40], J(3): [70, 100, 30, 1200, 1, 0, 30], J(40): [40, 100, 10, 500, 1, 0, 10]}, '_maj': '2026-11-15T13:00:00Z', '_err': '',
        'p': {'a': J(89), 'b': J(0), 'maj': '2026-11-15T13:00:00Z', 'L': [[bc, 50, 400, 4, 30, 'A', 1], [B0[0], 20, 100, 1, 9, 'B', 2], ['999999999999', 30, 0, 0, 12, 'Inconnu', 3]]}}
REG = {'comV4': 1, 'canauxV': 3, 'pcCom3': 1, 'canaux': [{'id': 'site', 'nom': 'Site perfumestrade.com', 'com': 3}, {'id': 'sitegros', 'nom': 'Site wholesale.perfumestrade.com', 'com': 3},
       {'id': 'amazon', 'nom': 'Amazon', 'com': 15}, {'id': 'perfumecity', 'nom': 'Perfume City', 'com': 3}], 'envois': {'woocommerce': 0, 'woocommerce-gros': 0, 'shopify-pc': 0}}
STRAT = {'courante': {'id': 'S1', 'date': '2026-11-01T12:00:00Z', 'faits': [False, True], 'res': {
  'fr': {'titre': 'Stratégie de novembre', 'diagnostic': 'La pub coûte plus que la marge.', 'actions': [{'titre': 'Sortir 800 parfums de la pub', 'pourquoi': 'Ils perdent 2 859 $ par mois.', 'comment': ['Télécharger la liste', 'La donner au prestataire'], 'cout': '0 $', 'gain': '+2 859 $ par mois', 'mesure': 'pub/mois : 5 667 $ → 2 100 $', 'delai': 'cette semaine'}, {'titre': 'Emails automatiques', 'pourquoi': 'Email : 1 commande en 30 jours.'}],
         'previsions': {'texte': 'Si la pub baisse…', 'ca': {'prudent': 20000, 'probable': 24000, 'haut': 28000}, 'marge': {'prudent': 1000, 'probable': 2500, 'haut': 4000}}, 'retire': ['Doubler le budget : coûte plus que la marge'], 'manques': ['Search Console']},
  'en': {'titre': 'November strategy', 'diagnostic': 'Ads cost more than the margin.', 'actions': [{'titre': 'Take 800 perfumes out of ads', 'pourquoi': 'They lose $2,859 a month.'}, {'titre': 'Automatic emails'}], 'previsions': {'ca': {'prudent': 20000, 'probable': 24000, 'haut': 28000}}, 'retire': ['Double the budget'], 'manques': ['Search Console']}}},
  'rapports': [{'id': 'R1', 'date': '2026-12-01T12:00:00Z', 'strategie': 'S1', 'res': {'fr': {'titre': 'Rapport de novembre', 'bilan': 'La marge après pub est passée de −513 $ à +900 $.', 'actions': [{'titre': 'Sortir 800 parfums', 'verdict': 'a marché', 'avant': '5 667 $', 'apres': '2 100 $', 'explication': 'La pub a baissé.'}], 'garder': ['la liste'], 'arreter': [], 'essayer': ['TikTok Shop'], 'prudence': 'Un seul mois.'},
    'en': {'titre': 'November report', 'bilan': 'Margin after ads went from −$513 to +$900.', 'actions': [{'titre': 'Take out 800 perfumes', 'verdict': 'worked'}], 'garder': ['the list'], 'essayer': ['TikTok Shop'], 'prudence': 'One month only.'}}}], 'encours': None}
SESS = """([F,O,P,G,R,lg,role])=>{ localStorage.clear(); localStorage.setItem('sam-comptes-demo-v1','0');
  localStorage.setItem('sam-session-v1',JSON.stringify({id:'x',nom:'Essai',role,depuis:new Date().toISOString()}));
  localStorage.setItem('langue-v1',lg); localStorage.setItem('factures-v1',JSON.stringify(F)); localStorage.setItem('ventes-origine-v1',JSON.stringify(O));
  localStorage.setItem('pc-origine-v1',JSON.stringify(P)); localStorage.setItem('google-pub-v1',JSON.stringify(G)); localStorage.setItem('reglages-v1',JSON.stringify(R)); localStorage.setItem('strategie-v1',JSON.stringify(window.__ST||{})); }"""
FR = re.compile(r"\b(Chiffre d'affaires|Marge nette|Commandes en ligne|Venus directement|Recherche Google|Origine inconnue|Tous les sites|Pub dépensée|est-ce que la pub rapporte|jours|Mois dernier|Cette année|Ce mois|commandes?|parfums|perdus|gagnés)\b|[éèêàç]")
s = socket.socket(); s.bind(('127.0.0.1', 0)); port = s.getsockname()[1]; s.close()
srv = subprocess.Popen(['python3', '-m', 'http.server', str(port), '--bind', '127.0.0.1'], cwd=D, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)

ADS = {'maj': '2026-11-15T18:40:00Z', 'compte': '709-551-4689', 'devise': 'USD',
       'c': [{'id': '11', 'n': 'PMAX - September', 'etat': 'ENABLED', 'type': 'PERFORMANCE_MAX', 'ench': 'MAXIMIZE_CONVERSION_VALUE', 'troas': 4, 'budget': 100, 'm30': [3962.5, 9746.3, 82.85, 1585, 114632], 'm7': [700, 2100, 18, 280, 20000]},
             {'id': '12', 'n': 'Shopping - Men', 'etat': 'PAUSED', 'type': 'SHOPPING', 'ench': 'TARGET_ROAS', 'troas': 2.75, 'budget': 65, 'm30': [469.31, 727.06, 10, 172, 10124], 'm7': [0, 0, 0, 0, 0]},
             {'id': '13', 'n': 'Old draft', 'etat': 'PAUSED', 'type': 'SEARCH', 'ench': '', 'troas': None, 'budget': 10, 'm30': [0, 0, 0, 0, 0], 'm7': [0, 0, 0, 0, 0]}],
       'j': {J(2): [111, 555, 40, 2000, 3], J(3): [0, 0, 0, 0, 0]},
       'cj': {'11': {J(2): [111, 555, 3]}},
       'p': {'a': J(89), 'b': J(1), 'maj': '2026-11-15T18:40:00Z', 'L': [[bc, 77, 600, 5, 40, 'A', 1]]}, 'ids': {}}
SCRIPT = 'var ADRESSE = "https://exemple/gads/dasy/jeton";\nfunction main(){}'
try:
    with sync_playwright() as p:
        b = p.chromium.launch(); err = []
        def ouvre(lg='fr', ads=ADS, heure=14):
            ctx = b.new_context(viewport={'width': 1440, 'height': 1000}, timezone_id='America/New_York', locale='fr-FR')
            pg = ctx.new_page(); pg.on('pageerror', lambda e: err.append(str(e))); pg.on('dialog', lambda d: d.accept())
            pg.add_init_script("Object.defineProperty(window,'D_HG',{configurable:true,set(v){ window.__hgReel=v; },get(){ return null; }})")
            pg.clock.set_fixed_time(datetime.datetime(auj.year, auj.month, auj.day, heure, 0, tzinfo=ZoneInfo('America/New_York')))
            vus = []
            pg.route('**/google/script', lambda route: (vus.append(route.request.headers.get('authorization')), route.fulfill(status=200, content_type='application/json', body=json.dumps({'script': SCRIPT, 'etat': None}))))
            base = f'http://127.0.0.1:{port}/'
            pg.goto(base + 'accueil.html'); pg.wait_for_timeout(300); pg.evaluate('s=>{ window.__ST=s; }', STRAT); pg.evaluate(SESS, [F, ORIG, PCO, GPUB, REG, lg, 'patron'])
            pg.evaluate("a=>{ if(a) localStorage.setItem('google-ads-v1',JSON.stringify(a)); localStorage.setItem('ck-token','jeton-test'); }", ads)
            pg.goto(base + 'analytique.html'); pg.wait_for_timeout(2600); pg._vus = vus; return pg
        print('1. la carte des campagnes')
        pg = ouvre()
        T = pg.inner_text('#gc')
        lignes = pg.evaluate("()=>[...document.querySelectorAll('#gc .gc-l')].map(l=>l.innerText.replace(/\\s+/g,' '))")
        check('LE POINT — les campagnes qui dépensent ou qui tournent sont listées, l\'active en premier', len(lignes) == 2 and lignes[0].startswith('PMAX - September') and 'Active' in lignes[0] and 'En pause' in lignes[1], lignes)
        check('LE POINT — budget, coût 30 j, ventes pour 1 $ (2,46) et objectif 400 %', a(lignes[0], 100) and a(lignes[0], 3963) and '2,46' in lignes[0] and '400 %' in lignes[0], lignes[0])
        check('la campagne en pause sans dépense est comptée, pas listée', '1 autre campagne en pause' in T, T[-400:])
        check('« reçu il y a » : l\'heure d\'arrivée des chiffres', 'reçu il y a' in T and 'en direct de Google Ads' in T, T[:200])
        r = pg.evaluate("()=>{ const R=anCampCalc(anCommandes(rcLignes())); return {seuil:R.seuil, res:R.C[0].res, roas:R.C[0].roas}; }")
        check('le seuil et le résultat estimé suivent la même règle que la liste parfum par parfum', r['seuil'] > 1 and abs(r['roas'] - 9746.3 / 3962.5) < 1e-6 and r['res'] < 9746.3, r)
        check('pas d\'alerte « plus de nouvelles » quand les chiffres sont frais', pg.locator('#gc .gc-alerte').count() == 0)
        print('2. la pub vient du script')
        r = pg.evaluate(f"()=>{{ const G=anPubJ(); return {{j2:G.j['{J(2)}'], j3:G.j['{J(3)}'], j40:G.j['{J(40)}'], p:G.p.L.length, p0:G.p.L[0][1]}}; }}")
        check('LE POINT — pub payante du script, fiches gratuites de l\'extension, sur le même jour', r['j2'] == [111, 555, 40, 2000, 3, 1, 40] and r['j3'] == [0, 0, 0, 0, 0, 0, 30], r)
        check('un jour que le script ne couvre pas garde les chiffres de l\'extension', r['j40'] == [40, 100, 10, 500, 1, 0, 10], r)
        check('LE POINT — la liste parfum par parfum vient du script', r['p'] == 1 and r['p0'] == 77, r)
        d = pg.evaluate("()=>anCampDossier(anCommandes(rcLignes()))")
        check('le dossier de la stratégie connaît chaque campagne (état, budget, objectif, coût, résultat)', isinstance(d, dict) and len(d['campagnes']) == 2 and d['campagnes'][0]['etat'] == 'active' and d['campagnes'][0]['budget_par_jour'] == 100 and d['autres_campagnes_en_pause_sans_depense'] == 1, d)
        print('3. plus de nouvelles')
        pg = ouvre(heure=19)
        check('plus de 3 heures sans nouvelles : la carte le dit', pg.locator('#gc .gc-alerte').count() == 1 and 'Plus de nouvelles' in pg.inner_text('#gc'))
        print('4. pas encore branché')
        pg = ouvre(ads=None)
        T = pg.inner_text('#gc')
        check('LE POINT — pas encore branché : explication et bouton', 'pas encore branchées' in T and pg.locator('#gc-voir').count() == 1, T[:300])
        pg.click('#gc-voir'); pg.wait_for_timeout(500)
        check('LE POINT — le bouton affiche le script demandé au cockpit (avec la session), les 5 étapes et « Copier »',
              pg.input_value('#gc-script textarea') == SCRIPT and pg.locator('.gc-etapes li').count() == 5 and pg.locator('#gc-copie').count() == 1 and pg._vus == ['Bearer jeton-test'], pg._vus)
        pg.context.grant_permissions(['clipboard-read', 'clipboard-write']); pg.click('#gc-copie'); pg.wait_for_timeout(200)
        check('« Copier » : le texte du bouton confirme', 'Copié' in pg.inner_text('#gc-copie'))
        check('sans le script, la pub reste celle de l\'extension', pg.evaluate(f"()=>anPubJ().j['{J(2)}'][0]") == 50)
        print('5. en anglais / espagnol')
        for lg in ('en', 'es'):
            for ads in (ADS, None):
                pg = ouvre(lg, ads)
                if not ads: pg.click('#gc-voir'); pg.wait_for_timeout(400)
                T = pg.evaluate("()=>{ const z=document.getElementById('gc').cloneNode(true); z.querySelectorAll('[data-nolang],textarea').forEach(x=>x.remove()); return z.innerText; }")
                m = FR.search(T) or re.search(r"\b(campagnes?|reçu|en pause|Résultat|Copier|Autoriser|Exécuter|heures|par jour|seuil)\b", T)
                check(f'{lg} ({"branché" if ads else "à brancher"}) : plus un mot de français dans la carte', not m, (m.group(0) if m else '', T[:400]))
        check('aucune erreur JS', not err, err[:3])
        b.close()
finally:
    srv.terminate()
print(f'\n{ok} ok, {len(ko)} KO', ko); raise SystemExit(1 if ko else 0)
