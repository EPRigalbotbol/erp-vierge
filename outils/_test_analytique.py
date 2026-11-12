# LA RUBRIQUE ANALYTIQUE (Igal, 9 nov. 2026 : « l'analytics de tous les sites, tous les canaux de vente… voir l'amélioration
# en direct », « est-ce que c'est intéressant de faire du Google Ads ? », « personne à part les admins de l'ERP »).
# Ce test protège :
#   1. LE POINT — seuls les administrateurs (rôles Admin et Patron) voient la page et sa ligne au menu ; Commercial,
#      Comptable, Entrepôt : ni menu (même avant la première peinture), ni chiffres (un mur) ;
#   2. LE POINT — les chiffres de vente sont ceux du Tableau de bord (même calcul : rcLignes / rcAgrege) ;
#   3. l'origine de chaque commande vient du cockpit (ventes-origine-v1) : Google Shopping, Google Ads, direct… comptées à la main ;
#   4. LE POINT — Google : pub dépensée (google-pub-v1), marge des commandes venues de la pub, et « ce qui reste après la pub » ;
#   5. la période se choisit (7 j, 30 j, ce mois…), l'infobulle des colonnes dit le jour et l'origine ;
#   6. en anglais (et en espagnol, qui lit l'anglais) : plus un mot de français ; aucune erreur JS.
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
STRAT = {'courante': {'id': 'S1', 'date': '2026-11-01T12:00:00Z', 'faits': [None, {'date': '2026-11-03T14:32:00Z', 'par': 'ERP', 'comment': 'vu dans Google Ads : « PMax » active, 30 $ par jour'}], 'res': {
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
try:
    with sync_playwright() as p:
        b = p.chromium.launch(); err = []
        def ouvre(lg='fr', role='patron', page='analytique.html', avant=None, tz='America/New_York', heure=14):
            ctx = b.new_context(viewport={'width': 1440, 'height': 1000}, timezone_id=tz, locale='fr-FR')
            pg = ctx.new_page(); pg.on('pageerror', lambda e: err.append(str(e))); pg.on('dialog', lambda d: d.accept())
            pg.add_init_script("Object.defineProperty(window,'D_HG',{configurable:true,set(v){ window.__hgReel=v; },get(){ return null; }})")
            pg.clock.set_fixed_time(datetime.datetime(auj.year, auj.month, auj.day, heure, 0, tzinfo=ZoneInfo(tz)))
            base = f'http://127.0.0.1:{port}/'
            pg.goto(base + 'accueil.html'); pg.wait_for_timeout(300); pg.evaluate('s=>{ window.__ST=s; }', STRAT); pg.evaluate(SESS, [F, ORIG, PCO, GPUB, REG, lg, role])
            if avant: pg.add_init_script(avant)
            pg.goto(base + page); pg.wait_for_timeout(2600); return pg
        pg = ouvre()
        if os.environ.get('AN_SHOT'):
            pg.screenshot(path=os.environ['AN_SHOT'] + '_fr.png', full_page=True)
            pg.emulate_media(color_scheme='dark'); pg.wait_for_timeout(300); pg.screenshot(path=os.environ['AN_SHOT'] + '_sombre.png', full_page=True); pg.emulate_media(color_scheme='light')
        T = pg.inner_text('#an')
        check('la page s\'ouvre sur « 30 jours », tous les sites, onglet « Commandes en ligne »', pg.evaluate("()=>[document.querySelector('[data-an].on').dataset.an,document.querySelector('[data-ans].on').dataset.ans,document.querySelector('.ga-tab.on').dataset.anm]") == ['rel:30', 'tous', 'n'])
        check('plus de cases « Chiffre d\'affaires / Marge nette » de tous les canaux (elles sont au Tableau de bord)', pg.locator('.an-kpi').count() == 0 and 'tous les canaux' not in T.lower(), T[:300])
        # 2. même calcul que le Tableau de bord
        tot = pg.evaluate("()=>{ const P=rcPlage('rel:30'); const R=rcAgrege(rcLignes(),P.a,P.b); return [Math.round(R.T.ca*100)/100, Math.round(R.T.mg*100)/100]; }")
        pt = ouvre(page='tableau.html')
        tb = pt.evaluate("()=>{ const P=rcPlage('rel:30'); const R=rcAgrege(rcLignes(),P.a,P.b); return [Math.round(R.T.ca*100)/100, Math.round(R.T.mg*100)/100]; }")
        check('LE POINT — même calcul des ventes et des marges que tableau.html', tb == tot and tot[0] == 1290, [tb, tot])
        pt.context.close()
        # 3. les onglets, comptés à la main
        tabs = pg.locator('.ga-tab').all_inner_texts()
        check('LE POINT — « Commandes en ligne » = 6 (la vente en boutique de Perfume City n\'est pas un site)', tabs[0].split('\n')[1].strip() == '6', tabs[0])
        check('« Chiffre d\'affaires en ligne » = 100+200+100+100+60+90 = 650 $', a(tabs[1], 650), tabs[1])
        check('« Commandes via Google Ads » = 2', tabs[3].split('\n')[1].strip() == '2', tabs[3])
        k = pg.evaluate("()=>{ const L=rcLignes(); const C=__an.anCommandes(L); const o={}; C.filter(x=>x.d>='2026-10-17').forEach(x=>{ o[x.fam]=(o[x.fam]||0)+1; }); return o; }")
        check('origines : 1 Google Shopping, 2 Google Ads, 1 direct, 1 réseau social, 1 recherche Google', k == {'gshop': 1, 'gads': 2, 'direct': 1, 'social': 1, 'google': 1}, k)
        check('les sources : Instagram écrit sous « Réseaux sociaux »', 'Instagram 1' in T, T)
        # le petit « i » de chaque origine
        n_i = pg.locator('.ga-bar .ga-i').count(); nb = pg.locator('.ga-bar').count()
        pg.locator('.ga-bar .ga-i').first.hover(); pg.wait_for_timeout(150)
        info = pg.evaluate("()=>{ const t=document.getElementById('ga-info'); return t&&t.style.display==='block'?t.textContent:''; }")
        check('LE POINT — chaque origine a son « i », qui explique ce qu\'elle veut dire', n_i == nb and nb == 5 and 'publicit' in info.lower(), [n_i, nb, info])
        pg.mouse.move(5, 5); pg.wait_for_timeout(100)
        inf2 = pg.evaluate("()=>[...document.querySelectorAll('.ga-bar .ga-i')].map(b=>b.dataset.info)")
        check('« Venus directement » est expliqué (adresse tapée, favori…)', any('adresse du site' in x for x in inf2), inf2)
        # 4. Google : la pub rapporte-t-elle ?
        V = pg.inner_text('.ga-verdict')
        mgAds = pg.evaluate("()=>{ const C=__an.anCommandes(rcLignes()).filter(o=>o.site==='site'&&o.fam==='gads'&&o.d>='2026-10-17'); return Math.round(C.reduce((a,o)=>a+o.mg,0)*100)/100; }")
        check('LE POINT — le verdict = marge des commandes Google Ads − pub (50 + 70 = 120 $ ; la pub d\'il y a 40 jours n\'y est pas)', a(V, abs(round(mgAds - 120))), [mgAds, V])
        st = pg.inner_text('.ga-stats')
        check('« Ventes : selon Google / réelles » = 400 $ / 300 $ ; coût de la pub par commande = 60 $', a(st, 400) and a(st, 300) and a(st, 60), st)
        # la pub, parfum par parfum
        an = pg.evaluate("()=>{ const A=anAnalysePub(__an.anCommandes(rcLignes())); return A&&{k:A.k,L:A.L.map(o=>[o.sku,o.dec,o.m,o.mgE,o.res,o.pvr,o.pa]),gain:A.gain90}; }")
        Lp = {x[0]: x for x in (an or {}).get('L', [])}
        check('LE POINT — rapport ventes réelles / ventes Google sur 90 jours = 400 / 500 = 0,8', an and abs(an['k'] - 0.8) < 1e-9, an and an['k'])
        xa = Lp.get(bc)
        if xa:
            m = xa[5] * (1 - 0.03) - 0.3 - xa[6]; mg = 400 * 0.8 * m / xa[5]; res = mg - 50
            check('LE POINT — parfum A : marge d\'un flacon, marge rapportée et résultat calculés à la main', abs(xa[2] - m) < 0.01 and abs(xa[3] - mg) < 0.01 and abs(xa[4] - res) < 0.01 and xa[1] == ('garder' if res >= 0 else 'sortir'), [xa, m, mg, res])
        else: check('parfum A trouvé', False, an)
        check('un parfum plus en stock avec de la pub → « sortir (plus en stock) »', Lp.get(B0[0], [0, ''])[1] == 'stock', Lp.get(B0[0]))
        check('un code inconnu de l\'ERP → « à vérifier », jamais une décision inventée', Lp.get('999999999999', [0, ''])[1] == 'verif', Lp.get('999999999999'))
        check('11 nov. : la carte « parfum par parfum » prend moins de place — l\'explication est repliée, la liste défile dans une boîte', pg.locator('details.ga-expl').count() == 1 and not pg.evaluate("()=>document.querySelector('details.ga-expl').open") and pg.locator('#pp-liste .pp-boite').count() == 1)
        check('la carte dit l\'économie par mois et propose la liste en Excel', pg.locator('#an-xl').count() == 1 and 'par mois en plus pour Sam' in pg.inner_text('#an'), '')
        # la liste complète, filtrable (Igal, 9 nov. : « qu'il puisse filtrer tout ça »)
        nl = pg.locator('#pp-liste .pp-l').count()
        check('LE POINT — tous les parfums de la pub sont listés (3), pas seulement les 8 pires', nl == 3, nl)
        pg.click('[data-ppf="stock"]'); pg.wait_for_timeout(100)
        check('le filtre « Plus en stock » ne garde que le parfum B', pg.locator('#pp-liste .pp-l').count() == 1 and pg.locator('#pp-liste .pp-d.stock').count() == 1)
        pg.click('[data-ppf="tous"]'); pg.select_option('#pp-tri', 'pub'); pg.wait_for_timeout(100)
        pubs = pg.locator('#pp-liste .pp-l .pp-v:nth-child(2)').all_inner_texts()
        check('LE POINT — tri « coûtent le plus en pub » : 50 $, 30 $, 20 $ dans cet ordre', [a(x, 50) for x in pubs[:1]] == [True] and a(pubs[1], 30) and a(pubs[2], 20), pubs)
        pg.select_option('#pp-tri', 'gain'); pg.wait_for_timeout(100)
        prem = pg.locator('#pp-liste .pp-l').first.get_attribute('class'), pg.locator('#pp-liste .pp-l .pp-d').first.inner_text()
        check('tri « rapportent le plus » : le parfum à garder passe en premier', 'garder' in pg.locator('#pp-liste .pp-l .pp-d').first.get_attribute('class'), prem)
        pg.fill('#pp-q', 'inconnu'); pg.wait_for_timeout(100)
        check('la recherche trouve un parfum par son nom', pg.locator('#pp-liste .pp-l').count() == 1 and 'Inconnu' in pg.inner_text('#pp-liste'), pg.inner_text('#pp-liste'))
        pg.fill('#pp-q', ''); pg.wait_for_timeout(100)
        check('le filtre et le tri restent quand on revient sur la page', pg.evaluate("()=>{ const r=JSON.parse(localStorage.getItem('analytique-vue')||'{}'); return [r.ppf,r.pptri,r.ppq]; }") == ['tous', 'gain', None])
        with pg.expect_download() as dl:
            pg.click('#an-xl')
        check('le bouton télécharge bien un fichier Excel', dl.value.suggested_filename.endswith('.xlsx'), dl.value.suggested_filename)
        # la stratégie et le rapport du mois
        # le texte d'un bloc, même replié (les détails fermés ne sont pas dans inner_text) ; TXL : sans les textes jamais traduits
        TX = "s=>[...document.querySelectorAll(s)].map(e=>e.textContent).join(' ').replace(/\\s+/g,' ')"
        TXL = "s=>[...document.querySelectorAll(s)].map(e=>{ const c=e.cloneNode(true); c.querySelectorAll('[data-nolang]').forEach(x=>x.remove()); return c.textContent; }).join(' ').replace(/\\s+/g,' ')"
        LI = lambda p, i: p.locator(f'.st-acts > li[data-sti="{i}"]')
        stx = pg.evaluate(TX, 'section.st')
        check('LE POINT — la stratégie s\'affiche : titre, diagnostic, actions, prévision en fourchette, et ce que les vérificateurs ont retiré', 'Stratégie de novembre' in stx and 'Sortir 800 parfums de la pub' in stx and 'prudent' in stx.lower() and a(stx, 24000) and pg.locator('section.st details').count() >= 1, stx[:500])
        check('LE POINT — plus aucune case « Fait » à cocher (Igal, 11 nov.) : l\'action constatée par l\'ERP est SIGNÉE « Fait par l\'ERP le 3 novembre 2026 à … », à l\'heure de Miami, avec ce qui a été vu', pg.locator('.st-acts input[type=checkbox]').count() == 0 and 'Fait par l\'ERP le 3 novembre 2026 à 09:32' in LI(pg, 1).inner_text() and 'vu dans Google Ads' in LI(pg, 1).inner_text() and 'fait' in (LI(pg, 1).get_attribute('class') or ''), pg.evaluate(TX, '.st-acts')[:500])
        check('LE POINT — stratégie pas encore active : le bouton « Activer la stratégie », et l\'action pas faite attend l\'activation (pas de bouton « C\'est fait »)', pg.locator('#st-active').count() == 1 and 'À faire après l\'activation' in LI(pg, 0).inner_text() and pg.locator('.st-cfait').count() == 0)
        act = []
        maint = pg.evaluate("()=>[new Date().toISOString(), new Date(Date.now()+30*86400e3).toISOString()]")   # l'heure de la page (horloge du test)
        pg.route('**/strategie/active', lambda route: (act.append(1), route.fulfill(status=200, content_type='application/json', body=json.dumps({'ok': True, 'date': maint[0], 'fin': maint[1], 'constatees': 0}))))
        pg.evaluate("()=>{ window.confirm=()=>true; }")
        pg.click('#st-active'); pg.wait_for_timeout(500)
        stA = pg.evaluate(TX, 'section.st')
        check('LE POINT — « Activer la stratégie » : le cockpit est appelé, la page dit « Stratégie active le … · mesure jusqu\'au … » et le bouton disparaît', len(act) == 1 and 'Stratégie active le' in stA and 'mesure jusqu' in stA and pg.locator('#st-active').count() == 0, stA[:400])
        # 11 nov. 2026 (Igal : « pas clair du tout, pourquoi ça bouge tout le temps ») : seules les journées COMPLÈTES sont comparées
        check('LE POINT — le jour de l\'activation : « jour 1 sur 30 », et AUCUN tableau — la journée en cours ne se compare à rien', 'jour 1 sur 30' in stA and 'commence demain' in stA and pg.locator('.st-tout tbody tr').count() == 0, stA[-700:])
        pg.evaluate("()=>{ __an.STRAT().courante.active.date=new Date(Date.now()-3*86400e3).toISOString(); __an.anDessine(); }"); pg.wait_for_timeout(400)
        stB = pg.evaluate(TX, 'section.st')
        check('LE POINT — trois jours après : « jour 4 sur 30 », le tableau compare 3 jours COMPLETS aux 3 jours d\'avant (aujourd\'hui n\'est pas compté)', 'jour 4 sur 30' in stB and '3 jours complets' in stB.lower() and 'les 3 jours d\'avant' in stB.lower() and pg.locator('.st-tout tbody tr').count() == 5 and 'ne bouge donc qu\'une fois par jour' in stB, stB[-800:])
        # 12 nov. 2026 (Igal : « analyser le coût de la pub depuis le démarrage de la campagne et surtout connaître l'évolution ; je veux que
        # cette partie soit mieux faite et plus compréhensible »)
        camp = pg.evaluate(TX, '.st-camp')
        tu = pg.evaluate(TX, '.st-tuiles'); sec = pg.evaluate(TX, '.st-sec')
        check('LE POINT — les chiffres en tête, au format de la page Tâches : actions faites, dépensé, clics, commandes de la pub, résultat — et une phrase', pg.locator('.st-tuiles > div').count() == 5 and '1 / 2' in tu and 'action faite' in tu and 'dépensés en pub' in tu and 'clic' in tu and 'de la pub' in tu and 'résultat de la pub' in tu and 'la pub a coûté' in pg.inner_text('.st-camp .ga-phrase') and 'jour 4 sur 30' in pg.inner_text('.st-on'), tu[:400])
        check('LE POINT — « Évolution depuis le redémarrage » dit le jour ET l\'heure du départ, en heures de Miami', 'Évolution depuis le redémarrage' in sec and re.search(r'depuis le \d+ \w+ 2026 à 14:00', sec) is not None and 'heures de Miami' in sec, sec[:300])
        cp = pg.evaluate("()=>{ const C=__an.CAMP(); return [C.K.length, C.K[0].court, C.sp[0], C.sm[0], C.K[C.K.length-1].lib, [...C.sp].every((v,i,a)=>i===0||v>=a[i-1]-1e-9)]; }")
        check('LE POINT — l\'évolution : UNE courbe qui part du redémarrage à zéro (plus les 14 jours d\'avant), un point par jour tant qu\'il n\'y a pas de relevé par heure, et elle ne redescend jamais (tout est additionné)', pg.locator('#st-camp-c svg').count() == 1 and pg.locator('#st-camp-c .ga-rep').count() == 1 and cp[0] == 5 and '14:00' in cp[1] and cp[2] == 0 and cp[3] == 0 and 'aujourd' in cp[4] and cp[5], cp)
        check('LE POINT — jour par jour : une ligne par jour depuis le redémarrage (4), la plus récente en haut marquée « en cours », et un total', pg.locator('.st-jours tbody tr').count() == 5 and 'en cours' in pg.locator('.st-jours tbody tr').nth(0).inner_text() and 'Total' in pg.locator('.st-jours tbody tr').nth(4).inner_text(), pg.inner_text('.st-jours')[:400])
        tj = pg.evaluate("()=>{ const c=[...document.querySelectorAll('.st-jours tbody tr')].slice(0,4).map(tr=>tr.children[1].textContent); const t=document.querySelector('.st-jours .st-tot').children[1].textContent; return [c,t,document.querySelector('.st-tuiles > .st-dep b').textContent]; }")
        check('le total du tableau est le chiffre « Dépensé » du haut', tj[1] == tj[2], tj)
        check('la moyenne par jour compare les 30 jours d\'avant aux journées COMPLÈTES depuis le redémarrage (3)', 'Par jour, en moyenne' in camp and '3 jours complets' in camp.lower() and 'les 30 jours d\'avant' in camp.lower(), camp[-900:])
        check('LE POINT — le bloc se lit comme la page Tâches : des titres de section (Évolution, À faire, Fait), et tout le détail est replié (fabrication, constat, ventes de tous les sites, comparaison aux 30 jours d\'avant, prévision)', pg.locator('.st-sec').count() >= 4 and 'À faire' in sec and 'Fait' in sec and pg.evaluate("()=>['st-comment','st-constat','st-ventes','st-moy','st-prevd'].every(c=>{ const d=document.querySelector('details.'+c); return d&&!d.open; })"), sec[:300])
        cartes = pg.evaluate("()=>[...document.querySelectorAll('.st-acts > li')].map(l=>[l.dataset.sti, l.className, l.parentElement.className, !!l.querySelector('.st-ka .st-cfait'), l.querySelector('.st-det').open, (l.querySelector('.st-att')||{}).textContent||''])")
        check('LE POINT — une carte par action : celle à faire d\'abord (barre orange, bouton « C\'est fait » à droite, « gain attendu » et « délai » en une ligne), celle qui est faite dans « Fait » (barre verte) ; le pourquoi / comment est replié', len(cartes) == 2 and cartes[0][0] == '0' and 'afaire' in cartes[0][1] and cartes[0][3] and 'Gain attendu' in cartes[0][5] and 'cette semaine' in cartes[0][5] and cartes[1][0] == '1' and 'fait' in cartes[1][1] and 'st-faites' in cartes[1][2] and not cartes[1][3] and not cartes[0][4] and not cartes[1][4], cartes)
        check('LE POINT — une action à valider à la main le dit : « l\'ERP ne peut pas voir cette action tout seul : cliquez C\'est fait »', 'ne peut pas voir cette action tout seul' in pg.evaluate(TX, '.st-acts'), pg.evaluate(TX, '.st-acts')[:300])
        ph = pg.inner_text('.ga-phrase')
        check('LE POINT — « est-ce que la pub rapporte ? » se lit en une phrase : ce que la pub a coûté, les commandes amenées, leur marge, le résultat', 'la pub a coûté' in ph and 'commande' in ph and 'de marge nette' in ph and 'Résultat' in ph, ph)
        check('et la page dit pourquoi ce chiffre bouge dans la journée', 'Ce chiffre bouge dans la journée' in pg.inner_text('section.ga-card:has(.ga-verdict)'))
        fa = []
        pg.route('**/strategie/action', lambda route: (fa.append(route.request.post_data_json), route.fulfill(status=200, content_type='application/json', body='{"ok":true}')))
        check('l\'action « manuelle » a maintenant un bouton « C\'est fait » (une seule)', pg.locator('.st-cfait').count() == 1)
        pg.click('.st-cfait'); pg.wait_for_timeout(400)
        check('LE POINT — « C\'est fait » : le cockpit reçoit l\'action, la ligne dit « Fait le <aujourd\'hui> à <heure> · Essai »', fa == [{'i': 0, 'fait': True}] and re.search(r'Fait le \d+ \w+ 2026 à \d\d:\d\d · Essai', LI(pg, 0).inner_text()) is not None, [fa, LI(pg, 0).inner_text()[:200]])
        check('LE POINT — le rapport du mois s\'affiche : bilan, verdict par action, avant → après, à garder / à essayer, prudence', 'Rapport de novembre' in stx and 'a marché' in stx and '2 100 $' in stx.replace('\u202f', ' ').replace('\xa0', ' ') and 'TikTok Shop' in stx and 'Un seul mois' in stx, stx[-600:])
        check('les deux boutons : mettre à jour la stratégie, rapport du mois', pg.locator('#st-maj').count() == 1 and pg.locator('#st-rap').count() == 1)
        cal = "e=>{ const S=JSON.parse(localStorage.getItem('strategie-v1')); S.encours=e?{id:'S9',type:'strategie',etape:'trois vérificateurs relisent',depuis:new Date(Date.now()-e*60e3).toISOString(),par:'Igal',err:''}:null; localStorage.setItem('strategie-v1',JSON.stringify(S)); window.dispatchEvent(new CustomEvent('ck-maj',{detail:{cles:['strategie-v1']}})); }"
        pg.evaluate(cal, 40); pg.wait_for_timeout(400); stx2 = pg.inner_text('section.st')
        check('LE POINT — une analyse restée 40 minutes sans nouvelle étape est signalée « arrêtée en route », et le bouton est de nouveau utilisable', "arrêtée en route" in stx2 and 'trois vérificateurs relisent' in stx2 and pg.locator('#st-maj').is_enabled(), stx2[:600])
        pg.evaluate(cal, 0); pg.wait_for_timeout(300)
        # 12 nov. 2026 — Igal : « c'est à l'ERP de la valider, de mettre la date : signé, fait par l'ERP à telle date »
        ACT3 = "h=>{ const S=__an.STRAT(); S.courante.active={date:new Date(Date.now()-h*3600e3).toISOString(),fin:new Date(Date.now()+27*86400e3).toISOString(),par:'Igal'}; __an.anDessine(); }"
        sel = "f=>{ const S=JSON.parse(localStorage.getItem('strategie-v1')); window.__gardeS=window.__gardeS||JSON.stringify(S); ['fr','en'].forEach(l=>{ S.courante.res[l].actions[0].verif={type:'selection'}; S.courante.res[l].actions[0].qui='ERP'; }); S.courante.faits[0]=f; S.courante.active=S.courante.active||{date:'2026-11-11T20:18:00Z',par:'Igal',fin:'2026-12-11T20:18:00Z'}; localStorage.setItem('strategie-v1',JSON.stringify(S)); window.dispatchEvent(new CustomEvent('ck-maj',{detail:{cles:['strategie-v1']}})); }"
        pg.evaluate(sel, {'date': '2026-11-11T19:52:13Z', 'par': 'ERP', 'comment': 'sélection envoyée à Google depuis l\'ERP (bouton cliqué par Igal) : 97 gagnants gardés en pub, 796 perdants sortis', 'lu': '2026-11-12T08:10:00Z'}); pg.wait_for_timeout(400)
        l0 = LI(pg, 0); t0 = l0.inner_text()
        check('LE POINT — « sortir les perdants de la pub » est signé par l\'ERP : « Fait par l\'ERP le 11 novembre 2026 à 14:52 », ce qu\'il a fait (97 gardés, 796 sortis), et l\'heure où Google a relu la sélection',
              'Fait par l\'ERP le 11 novembre 2026 à 14:52' in t0 and '97 gagnants gardés' in t0 and '796 perdants sortis' in t0 and 'Google a relu la sélection le 12 novembre 2026 à 03:10' in t0, t0[:400])
        check('une action signée par l\'ERP n\'a ni bouton « C\'est fait » ni « annuler »', l0.locator('.st-cfait').count() == 0 and l0.locator('.st-annule').count() == 0)
        pg.evaluate(sel, None); pg.wait_for_timeout(400); t0 = LI(pg, 0).inner_text()
        check('tant que la sélection n\'est pas envoyée : « c\'est l\'ERP qui le fait », le bouton à utiliser est nommé, et il n\'y a PAS de « C\'est fait » à cliquer', 'c\'est l\'ERP qui le fait' in t0 and 'Ne garder en pub que les gagnants' in t0 and 'signe l\'action lui-même' in t0 and LI(pg, 0).locator('.st-cfait').count() == 0, repr(t0[:600]))
        pg.evaluate("()=>{ localStorage.setItem('strategie-v1',window.__gardeS); window.dispatchEvent(new CustomEvent('ck-maj',{detail:{cles:['strategie-v1']}})); }"); pg.wait_for_timeout(300)
        # 12 nov. 2026 — Igal : « je veux vraiment connaître l'évolution depuis le jour, depuis l'heure où on a commencé la campagne »
        pg.evaluate(ACT3, 72); pg.wait_for_timeout(300)
        n0 = pg.evaluate("()=>__an.CAMP().K.length")
        check('sans relevé par heure : la page le dit (« le détail heure par heure commence au prochain relevé »), et il n\'y a pas de tableau des heures', 'heure par heure commence au prochain relevé' in pg.evaluate(TX, '.st-camp') and pg.locator('.st-heures').count() == 0, pg.evaluate(TX, '.st-camp .ga-note')[:300])
        # le cas de Sam : PAS de script Google Ads — les relevés viennent de l'extension Google du site (google-pub-v1 › h)
        pg.evaluate("()=>{ const d=__an.anJM(new Date()), t=h=>new Date(Date.now()-h*3600e3).toISOString(); window.__gardeA=localStorage.getItem('google-pub-v1'); const G=JSON.parse(window.__gardeA||'{}'); G.j=G.j||{}; G.j[d]=[12,0,5,200,0,0,0]; G.h=[[t(100),d,99,0,9,999,0],[t(4),d,4,0,2,80,0],[t(3),d,9,0,3,150,0],[t(2),d,12,0,5,200,0]]; localStorage.removeItem('google-ads-v1'); localStorage.setItem('google-pub-v1',JSON.stringify(G)); window.dispatchEvent(new CustomEvent('ck-maj',{detail:{cles:['google-pub-v1','google-ads-v1']}})); }"); pg.wait_for_timeout(900)
        pg.evaluate(ACT3, 72); pg.wait_for_timeout(300)
        hp = pg.evaluate("()=>{ const C=__an.CAMP(), n=C.K.length; return [n, C.K.slice(-3).map(k=>k.court), C.sp.slice(-3).map(v=>Math.round((v-C.sp[n-4])*100)/100), C.K.slice(-3).map(k=>k.lib)]; }")
        check('LE POINT — avec les relevés du cockpit : un point PAR HEURE sur la courbe (10:00, 11:00, 12:00 à Miami), et la dépense monte de relevé en relevé (4 $, 9 $, 12 $) ; un relevé d\'avant le redémarrage ne compte pas', hp[0] == n0 + 2 and '10:00' in hp[1][0] and '11:00' in hp[1][1] and '12:00' in hp[1][2] and hp[2] == [4, 9, 12] and 'à 12:00' in hp[3][2], [n0, hp])
        pg.evaluate("()=>{ document.querySelector('details.st-heures').open=true; }")
        hh = pg.evaluate("()=>[...document.querySelectorAll('.st-heures tbody tr')].map(tr=>[...tr.children].map(td=>td.textContent.replace(/\\s+/g,' ').trim()))")
        check('LE POINT — « Heure par heure » : le relevé le plus récent en haut, ce qui a été dépensé depuis le relevé d\'avant (3 $, 5 $, 4 $) et le total de la journée (12 $, 9 $, 4 $)', len(hh) == 3 and '12:00' in hh[0][0] and [r[1] for r in hh] == ['3 $', '5 $', '4 $'] and [r[4] for r in hh] == ['12 $', '9 $', '4 $'] and hh[0][3] == '2' and hh[0][2] == '50', hh)
        check('la ligne du jour (« Jour par jour ») suit le dernier relevé : 12 $', '12 $' in pg.evaluate("()=>document.querySelector('.st-jours tbody tr').children[1].textContent.replace(/\\s+/g,' ')"), pg.evaluate(TX, '.st-jours')[:200])
        if os.environ.get('AN_SHOT'):
            pg.evaluate(sel, {'date': '2026-11-11T19:52:13Z', 'par': 'ERP', 'comment': 'sélection envoyée à Google depuis l\'ERP (bouton cliqué par Igal) : 97 gagnants gardés en pub, 796 perdants sortis, 85 sortis faute de stock', 'lu': '2026-11-12T08:10:00Z'}); pg.wait_for_timeout(1500)
            pg.locator('section.st').screenshot(path=os.environ['AN_SHOT'] + '_strategie.png')
            pg.emulate_media(color_scheme='dark'); pg.wait_for_timeout(400); pg.locator('section.st').screenshot(path=os.environ['AN_SHOT'] + '_strategie_sombre.png'); pg.emulate_media(color_scheme='light')
            pg.evaluate("()=>{ localStorage.setItem('strategie-v1',window.__gardeS); window.dispatchEvent(new CustomEvent('ck-maj',{detail:{cles:['strategie-v1']}})); }"); pg.wait_for_timeout(300)
        # et quand le script Google Ads est posé, ce sont SES relevés qui servent
        pg.evaluate("()=>{ const d=__an.anJM(new Date()), t=h=>new Date(Date.now()-h*3600e3).toISOString(); localStorage.setItem('google-ads-v1',JSON.stringify({maj:t(0),v:1,c:[],j:{[d]:[20,0,8,300,0]},h:[[t(1),d,20,0,8,300,0]]})); window.dispatchEvent(new CustomEvent('ck-maj',{detail:{cles:['google-ads-v1']}})); }"); pg.wait_for_timeout(700)
        pg.evaluate(ACT3, 72); pg.wait_for_timeout(300)
        check('script Google Ads posé : la courbe prend ses relevés à lui (un seul, à 13:00), plus ceux de l\'extension', pg.evaluate("()=>{ const C=__an.CAMP(); return C.K.filter(k=>/\\d\\d:\\d\\d/.test(k.court)).map(k=>k.court.slice(-5)); }") == ['14:00', '13:00'], pg.evaluate("()=>__an.CAMP().K.map(k=>k.court)"))
        pg.evaluate("()=>{ localStorage.removeItem('google-ads-v1'); if(window.__gardeA==null) localStorage.removeItem('google-pub-v1'); else localStorage.setItem('google-pub-v1',window.__gardeA); window.dispatchEvent(new CustomEvent('ck-maj',{detail:{cles:['google-pub-v1','google-ads-v1']}})); }"); pg.wait_for_timeout(500)
        dos = pg.evaluate("()=>{ const L=rcLignes(); const d=anDossier(L,__an.anCommandes(L)); return {ca:d.trente_derniers_jours.tous_canaux.ca, cmd:d.trente_derniers_jours.sites_en_ligne.commandes, pub:d.trente_derniers_jours.google_ads.pub_depensee, prec:typeof d.trente_jours_d_avant, manq:d.donnees_manquantes.length, pp:typeof d.pub_parfum_par_parfum_90j}; }")
        check('LE POINT — le dossier envoyé aux agents porte les vrais chiffres de la page (30 jours : 1 290 $, 6 commandes en ligne, 120 $ de pub)', dos['ca'] == 1290 and dos['cmd'] == 6 and dos['pub'] == 120 and dos['manq'] == 3 and dos['pp'] == 'object', dos)
        envoye = []
        pg.route('**/strategie/lance', lambda route: (envoye.append(route.request.post_data_json), route.fulfill(status=200, content_type='application/json', body='{"ok":true,"id":"S2"}')))
        pg.evaluate("()=>{ window.confirm=()=>true; }")
        pg.click('#st-maj'); pg.wait_for_timeout(600)
        check('le bouton envoie le dossier au cockpit et affiche « en préparation »', len(envoye) == 1 and envoye[0]['type'] == 'strategie' and envoye[0]['dossier']['trente_derniers_jours']['tous_canaux']['ca'] == 1290 and pg.locator('.sc').count() == 1, envoye[:1])
        check('LE POINT — plus de vidéo (Igal, 11 nov.) : une barre de progression, l\'étape en cours, le chrono', pg.locator('.sc video').count() == 0 and pg.locator('.sc-barre i').count() == 1 and pg.locator('.sc-etapes li.on').count() == 1 and pg.locator('.sc-chrono').count() == 1)
        pg.evaluate("()=>{ const S=JSON.parse(localStorage.getItem('strategie-v1')||'{}'); S.encours={type:'strategie',etape:'trois vérificateurs relisent',depuis:new Date().toISOString()}; localStorage.setItem('strategie-v1',JSON.stringify(S)); window.dispatchEvent(new CustomEvent('ck-maj',{detail:{cles:['strategie-v1']}})); }")
        pg.wait_for_timeout(200)
        w2 = pg.evaluate("()=>parseFloat(document.querySelector('.sc-barre i').style.width)")
        check('LE POINT — quand le serveur annonce l\'étape suivante (relève « ck-maj »), la barre passe le tiers et l\'étape 1 est cochée', pg.locator('.sc-etapes li.ok').count() == 1 and 33 <= w2 < 67, w2)
        pg.evaluate("()=>{ STRAT.encours=null; anDessine(); }")
        check('LE POINT — la stratégie est prête : la barre pleine et « Décision prise », puis le résultat', pg.locator('.sc video').count() == 0 and pg.evaluate("()=>document.querySelector('.sc-fin .sc-barre i').style.width") == '100%' and 'Décision prise' in pg.inner_text('.sc-accord'))
        att = pg.inner_text('.ga-attente') if pg.locator('.ga-attente').count() else ''
        check('LE POINT — « + 2 commandes de la pub payées, pas encore expédiées : 200 $ » (la commande directe n\'y est pas)', '2' in att and a(att, 200) and 'pas encore exp' in att, att)
        check('Google Shopping gratuit : 1 clic, 70 affichages', '1 clic' in pg.inner_text('.ga-free') and '70' in pg.inner_text('.ga-free'), pg.inner_text('.ga-free'))
        check('deux courbes cumulées (marge et pub) avec leurs étiquettes', pg.locator('#ga-c2 .ga-l').count() == 2 and pg.locator('#ga-c2 .ga-lab').count() == 2)
        check('une relecture en panne (Shopify) est dite en haut de la page', 'Access denied' in T and pg.locator('.an-alerte').count() == 1, T[:400])
        # 5. période, survol, onglets, sites
        pg.click('[data-an="rel:7"]'); pg.wait_for_timeout(1300)
        z = pg.locator('#ga-c1 .ga-zone').bounding_box()
        pg.mouse.move(z['x'] + z['width'] * 0.85, z['y'] + z['height'] / 2); pg.wait_for_timeout(150)
        tip = pg.evaluate("()=>{ const t=document.getElementById('ga-tip'); return t&&t.style.display==='block'?t.innerText:''; }")
        check('5. « 7 jours » : au survol de la courbe, une bulle dit le jour et la valeur', bool(re.search(r'\d+ nov', tip)) and '7 derniers jours' in tip, tip)
        pg.mouse.move(5, 5)
        pg.click('[data-anm="ca"]'); pg.wait_for_timeout(1100)
        check('5. l\'onglet « Chiffre d\'affaires » trace sa courbe', pg.locator('.ga-tab.on').get_attribute('data-anm') == 'ca' and pg.locator('#ga-c1 .ga-l').count() >= 1)
        pg.click('[data-an="rel:30"]'); pg.click('[data-ans="site"]'); pg.wait_for_timeout(1300)
        check('5. le choix « perfumestrade.com » ne garde que ce site (4 commandes)', pg.locator('.ga-tab').first.inner_text().split('\n')[1].strip() == '4', pg.locator('.ga-tab').first.inner_text())
        pg.click('[data-ans="tous"]'); pg.wait_for_timeout(300)
        # 1. accès
        for role in ('commercial', 'comptable', 'entrepot'):
            pr = ouvre(role=role)
            mur = pr.locator('.mur').count() == 1 and pr.locator('#an').count() == 0
            menu = pr.evaluate("()=>{ const a=document.querySelector('.side nav a.nv[href^=\"analytique.html\"]'); return a?getComputedStyle(a).display:'absent'; }")
            check(f'LE POINT — {role} : un mur, aucun chiffre, et pas de ligne Analytique au menu', mur and menu == 'none', [mur, menu])
            pr.context.close()
        # avant la première peinture : la classe qui cache la ligne est posée par l'entête
        pr = ouvre(role='comptable', page='catalogue.html')
        check('comptable : la ligne est cachée dès l\'entête (mn-pasadmin), sur une autre page aussi', pr.evaluate("()=>document.documentElement.classList.contains('mn-pasadmin')"))
        pr.context.close()
        for role in ('admin', 'patron'):
            pr = ouvre(role=role, page='tableau.html')
            vis = pr.evaluate("()=>{ const a=document.querySelector('.side nav a.nv[href^=\"analytique.html\"]'); return a?getComputedStyle(a).display:'absent'; }")
            nxt = pr.evaluate("()=>{ const L=[...document.querySelectorAll('.side nav a.nv')].map(a=>(a.getAttribute('href')||'').split('?')[0]); const i=L.indexOf('tableau.html'); return L[i+1]; }")
            check(f'{role} : « Analytique » au menu, juste sous Tableau de bord', vis != 'none' and vis != 'absent' and nxt == 'analytique.html', [vis, nxt])
            pr.context.close()
        # 7. la stratégie vue d'une autre page (Igal, 9 nov. : « qu'ils puissent aller sur une autre page, mais qu'en même temps la stratégie tourne »)
        MAJ = "([e,c])=>{ const S=JSON.parse(localStorage.getItem('strategie-v1')); S.encours=e?{id:'S77',type:'strategie',etape:'le stratège propose',depuis:new Date(Date.now()-60e3).toISOString(),par:'Igal',err:''}:null; if(c) S.courante=Object.assign({},S.courante,{id:'S77',date:'2026-12-02T12:00:00Z'});   /* après le rapport du 1er déc. de l\'exemple */ localStorage.setItem('strategie-v1',JSON.stringify(S)); window.dispatchEvent(new CustomEvent('ck-maj',{detail:{cles:['strategie-v1']}})); }"
        for lg, prete in (('fr', 'La nouvelle stratégie est prête'), ('en', 'The new strategy is ready'), ('es', 'La nueva estrategia está lista')):
            pt = ouvre(lg=lg, page='tableau.html')
            pt.evaluate(MAJ, [True, False]); pt.wait_for_timeout(300)
            c1 = pt.evaluate("()=>{ const p=document.querySelector('.side nav a.nv[href^=\"analytique.html\"] .mn-st'); return p?p.className:''; }")
            check(f'LE POINT — {lg} : pendant l\'analyse, sur une autre page (Tableau de bord), un point bleu bat à côté d\'« Analytique »', 'cours' in c1, c1)
            pt.evaluate(MAJ, [False, True]); pt.wait_for_timeout(300)
            c2 = pt.evaluate("()=>{ const p=document.querySelector('.side nav a.nv[href^=\"analytique.html\"] .mn-st'); return p?p.className:''; }")
            toast = pt.locator('.mn-st-toast').inner_text() if pt.locator('.mn-st-toast').count() else ''
            check(f'LE POINT — {lg} : quand elle est prête, un message le dit sur la page où l\'on est, avec un lien, et le point passe au vert', 'neuve' in c2 and prete in toast and pt.locator('.mn-st-toast a[href="analytique.html"]').count() == 1, [c2, toast])
            pt.evaluate(MAJ, [False, False]); pt.wait_for_timeout(200)
            check(f'{lg} : le message ne revient pas une deuxième fois pour la même stratégie', pt.locator('.mn-st-toast').count() == 1, pt.locator('.mn-st-toast').count())
            pt.goto(pt.url.replace('tableau.html', 'analytique.html')); pt.wait_for_timeout(1500)
            c3 = pt.evaluate("()=>{ const p=document.querySelector('.side nav a.nv[href^=\"analytique.html\"] .mn-st'); return p?p.className:''; }")
            check(f'{lg} : une fois la page Analytique ouverte, le point vert s\'éteint', c3 == 'mn-st', c3)
            pt.context.close()
        # 7 ter. 11 nov. 2026 — Igal : « que toutes les informations sur cette page comportent un petit i »
        SEL = ".ga-tab .ga-tl, .ga-h > h3, .ga-stats > div > span:first-child, .ga-free > b, .vis-t > b, .sel-pub > div > b:first-child, .st-acts > li > p > span, .st-acts > li > div:not(.st-etat):not(.st-ah):not(.st-kv) > span, .st-kv > div > span, .st-obj > span"
        for lg in ('fr', 'en'):
            pi = ouvre(lg=lg)
            pi.evaluate("""d=>{ localStorage.setItem('google-sources-v1',JSON.stringify({maj:new Date().toISOString(),ga:{live:3,jours:{[d]:[10,9,1,50]},sources:[['google / cpc',5,1,50]],pays:[['United States',5,1,50]]},sc:{jours:{[d]:[1,9,4]},requetes:[['perfumes trade',1,9,1.2]]}}));
              window.dispatchEvent(new CustomEvent('ck-maj',{detail:{cles:['google-sources-v1']}})); }""", (auj - datetime.timedelta(days=1)).isoformat())
            pi.wait_for_timeout(1400)
            sans = pi.evaluate("s=>[...document.querySelectorAll(s)].filter(e=>!e.querySelector('.ga-i')).map(e=>e.textContent.trim())", SEL)
            nb = pi.evaluate("s=>document.querySelectorAll(s).length", SEL)
            check(f'LE POINT — {lg} : chaque intitulé de la page (onglets, titres, cases de chiffres, tableaux) a son petit « i » ({nb} intitulés)', nb >= 25 and not sans, sans)
            bi = pi.locator('.ga-tab .ga-i').first; bi.hover(); pi.wait_for_timeout(150)
            bul = pi.evaluate("()=>{ const t=document.getElementById('ga-info'); return t&&t.style.display==='block'?t.innerText:''; }")
            check(f'{lg} : au survol du « i » de « Commandes en ligne », la bulle explique', ('remboursements' in bul) if lg == 'fr' else ('refunds' in bul), bul)
            pi.context.close()
        # 8. 11 nov. 2026 — la sélection pub (« ne garder que les gagnants ») et le journal des actions
        pj = ouvre()
        envoi = []
        pj.route('**/google/etiquettes', lambda route: (envoi.append(route.request.post_data_json), route.fulfill(status=200, content_type='application/json', body=json.dumps({'ok': True, 'n': {'garder': 1, 'stock': 1, 'verif': 1}, 'flux': 'https://cockpit.exemple/gads/dasy/j/etiquettes.csv'}))))
        sel = pj.inner_text('.sel-pub')
        check('LE POINT — le bloc « Ne garder en pub que les gagnants » dit combien sortent (perdants, plus en stock) et qu\'ils restent en vente sur le site', 'Ne garder en pub que les 1 gagnants' in sel and 'plus en stock' in sel and 'restent en vente sur le site' in sel, sel)
        pj.click('#sel-env'); pj.wait_for_timeout(500)
        Lenv = dict((x[0], x[1]) for x in (envoi[0]['L'] if envoi else []))
        check('LE POINT — le bouton envoie au cockpit la décision de CHAQUE parfum (garder / plus en stock / à vérifier)', len(envoi) == 1 and Lenv.get(bc) == 'garder' and Lenv.get(B0[0]) == 'stock' and Lenv.get('999999999999') == 'verif', envoi)
        check('chaque ligne dit aussi si le parfum était gagnant (pour le remettre en pub quand son stock revient)', envoi and all(len(x) in (3, 4) for x in envoi[0]['L']) and [x for x in envoi[0]['L'] if x[0] == bc][0][2] == 1, envoi[:1])
        # 11 nov. 2026 : le titre Google Shopping des gagnants (4e colonne), jamais pour les autres
        check('LE POINT — seuls les gagnants portent un titre Google Shopping', envoi and all(len(x) == 3 or x[1] == 'garder' for x in envoi[0]['L']), envoi[:1])
        T = pj.evaluate("""()=>[
          anTitreGoogle({marque:'Lattafa',nom:'Qaed Al Fursan',ml:'3.4',ty:'EDP',ge:'M'}),
          anTitreGoogle({marque:'Gucci',nom:'Gucci Flora Gorgeous Gardenia',ml:'3.3',ty:'EDT',ge:'W'}),
          anTitreGoogle({marque:'Dior',nom:'Sauvage EDT 2oz',ml:'2',ty:'EDT',ge:'M'}),
          anTitreGoogle({marque:'Cartier',nom:'Coffret Santos',ml:'3.3',ty:'SKIN CARE',ge:'M'}),
          anTitreGoogle({marque:'Armaf',nom:'Club de Nuit',ml:'',ty:'EDT',ge:'U'})]""")
        check('LE POINT — le titre suit l\'ordre de Google : marque, nom, type en toutes lettres, contenance, pour qui', T[0] == 'Lattafa Qaed Al Fursan Eau de Parfum 3.4 oz for Men', T)
        check('la marque n\'est pas répétée quand le nom la contient déjà', T[1] == 'Gucci Flora Gorgeous Gardenia Eau de Toilette 3.3 oz for Women', T)
        check('un nom qui contient déjà un type ou une contenance, un type inconnu, une contenance manquante : pas de titre (on ne devine pas)', T[2] == '' and T[3] == '' and T[4] == '', T)
        check('après l\'envoi : « ✓ Envoyé le … » et le bouton devient « Renvoyer la sélection à jour »', 'Envoyé le' in pj.inner_text('.sel-ok') and 'Renvoyer' in pj.inner_text('#sel-env'), pj.inner_text('.sel-pub'))
        check('après l\'envoi : un bouton copie l\'adresse du flux pour Merchant Center, sans jamais l\'afficher (elle porte un jeton)', pj.locator('#sel-copie').count() == 1 and 'etiquettes.csv' not in pj.inner_text('#an'))
        check('sans journal encore : la page dit que la première action notée sera la sélection pub', 'première action' in pj.inner_text('#jp'))
        hier = (auj - datetime.timedelta(days=1)).isoformat()
        pj.evaluate("""d=>{ localStorage.setItem('journal-pub-v1',JSON.stringify({L:[
          {t:d+'T19:32:05.000Z',src:'gads',quoi:'budget : modification — « PMax Gagnants »',detail:'budget : 45 $ → 30 $ par jour',par:'igal@exemple.com'},
          {t:d+'T15:00:00.000Z',src:'erp',quoi:'Sélection pub : seuls les 1 parfums gagnants restent en pub',detail:'1 sortis (plus en stock)',par:'Sam'}]}));
          window.dispatchEvent(new CustomEvent('ck-maj',{detail:{cles:['journal-pub-v1']}})); }""", hier)
        pj.wait_for_timeout(1500)
        jt = pj.inner_text('#jp')
        check('LE POINT — le journal liste les actions, la plus récente en haut, avec l\'heure de Miami (14:32), la source et le détail', pj.locator('#jp .jp-l li').count() == 2 and '14:32' in pj.locator('#jp .jp-l li').first.inner_text() and 'Google Ads' in pj.locator('#jp .jp-l li').first.inner_text() and '45 $ → 30 $' in jt, jt[:600])
        check('LE POINT — le jour de ces actions porte un repère sur la courbe du haut (2 événements ce jour-là)', pj.locator('#ga-c1 .ga-rep').count() == 1 and pj.locator('#ga-c1 .ga-rep-n').text_content() == '2', pj.locator('#ga-c1 .ga-rep').count())
        notes = []
        pj.route('**/journal-pub', lambda route: (notes.append(route.request.post_data_json), route.fulfill(status=200, content_type='application/json', body='{"ok":true}')))
        pj.fill('#jp-quoi', 'Sam lance une promo WhatsApp'); pj.click('#jp-ok'); pj.wait_for_timeout(500)
        check('un repère ajouté à la main part au cockpit et s\'affiche en haut du journal', notes == [{'quoi': 'Sam lance une promo WhatsApp'}] and 'Sam lance une promo WhatsApp' in pj.locator('#jp .jp-l li').first.inner_text(), notes)
        pj.evaluate("()=>{ localStorage.setItem('google-ads-v1',JSON.stringify({maj:new Date().toISOString(),v:1,c:[],j:{}})); window.dispatchEvent(new CustomEvent('ck-maj',{detail:{cles:['google-ads-v1']}})); }"); pj.wait_for_timeout(1200)
        check('un script Google Ads encore en version 1 : le journal dit de le remplacer (pour voir les changements faits dans Google Ads)', 'version 2' in pj.inner_text('#jp'), pj.inner_text('#jp')[:300])
        check('robot Google pas encore branché : la carte « visites » le dit', 'pas encore branché' in pj.inner_text('#vis'), pj.inner_text('#vis')[:200])
        pj.evaluate("""d=>{ localStorage.setItem('google-sources-v1',JSON.stringify({maj:new Date().toISOString(),ga:{live:140,jours:{[d]:[420,380,9,812.5]},sources:[['google / cpc',5000,60,5400]],pays:[['Puerto Rico',300,4,310]]},sc:{jours:{[d]:[4,900,18.4]},requetes:[['tobacco touch perfume',3,120,6.24]],err:"le robot n'a pas encore accès — il faut l'ajouter comme lecteur"}}));
          window.dispatchEvent(new CustomEvent('ck-maj',{detail:{cles:['google-sources-v1']}})); }""", hier)
        pj.wait_for_timeout(1300)
        vt = pj.inner_text('#vis')
        check('LE POINT — en direct de Google : visiteurs en ce moment (140), visites 30 jours (420), achats, sources, recherches tapées dans Google, pays (Porto Rico)', '140' in vt and '420' in vt and 'google / cpc' in vt and 'tobacco touch perfume' in vt and 'Puerto Rico' in vt and '6,2' in vt, vt[:700])
        check('un accès refusé chez Google est dit en clair sur la carte', 'pas encore accès' in vt, vt[:300])
        pj.context.close()
        # 7 bis. 11 nov. 2026 : le point bleu bat aussi tant qu'une stratégie est ACTIVE (« connectée »), sur toutes les pages
        pt = ouvre(page='tableau.html')
        pt.evaluate("()=>{ const S=JSON.parse(localStorage.getItem('strategie-v1')); S.courante.active={date:new Date().toISOString(),par:'Igal',fin:new Date(Date.now()+30*86400e3).toISOString()}; localStorage.setItem('strategie-v1',JSON.stringify(S)); window.dispatchEvent(new CustomEvent('ck-maj',{detail:{cles:['strategie-v1']}})); }")
        pt.wait_for_timeout(300)
        c4 = pt.evaluate("()=>{ const a=document.querySelector('.side nav a.nv[href^=\"analytique.html\"]'); const p=a&&a.querySelector('.mn-st'); return [p?p.className:'', a?a.title:'']; }")
        check('LE POINT — stratégie active : le point bleu bat à côté d\'« Analytique », sur une autre page, et l\'infobulle dit pourquoi', 'cours' in c4[0] and 'active' in c4[1], c4)
        pt.evaluate("()=>{ const S=JSON.parse(localStorage.getItem('strategie-v1')); S.courante.active.fin=new Date(Date.now()-60e3).toISOString(); localStorage.setItem('strategie-v1',JSON.stringify(S)); window.dispatchEvent(new CustomEvent('ck-maj',{detail:{cles:['strategie-v1']}})); }")
        pt.wait_for_timeout(300)
        c5 = pt.evaluate("()=>{ const p=document.querySelector('.side nav a.nv[href^=\"analytique.html\"] .mn-st'); return p?p.className:''; }")
        check('après les 30 jours, le point s\'éteint', c5 == 'mn-st', c5)
        pt.context.close()
        # 6. langues
        for lg in ('en', 'es'):
            pe = ouvre(lg=lg)
            te = pe.inner_text('main')
            fr = sorted(set(m.group(0) for m in FR.finditer(te)))
            check(f'6. {lg} : la page est en anglais, plus un mot de français, « i » compris', not fr and 'where orders come from' in te.lower() and all('publicit' not in x and 'adresse' not in x for x in pe.evaluate("()=>[...document.querySelectorAll('.ga-i')].map(b=>b.dataset.info)")) and 'Analytics' in pe.inner_text('.side'), fr[:12])
            pe.context.close()
        # 12 nov. 2026 : les jours sont ceux de Miami — Igal ouvre l'ERP depuis l'Europe, où il est déjà « demain » le soir de Miami
        ACT = "h=>{ const S=__an.STRAT(); S.courante.active={date:new Date(Date.now()-h*3600e3).toISOString(),fin:new Date(Date.now()+30*86400e3).toISOString(),par:'x'}; __an.anDessine(); }"
        pj = ouvre(tz='Asia/Jerusalem', heure=2); pj.evaluate(ACT, 4); pj.wait_for_timeout(500)
        check('LE POINT — écran ouvert en Europe à 2 h du matin (19 h la veille à Miami), campagne relancée 4 h plus tôt : c\'est encore le jour 1, pas le jour 2', 'jour 1 sur 30' in pj.evaluate(TX, '.st-tout') and 'jour 1 sur 30' in pj.inner_text('.st-on') and pj.locator('.st-jours tbody tr').count() == 2, [pj.evaluate(TX, '.st-tout')[:120], pj.inner_text('.st-on')])
        eu = [pj.inner_text('.st-on'), pj.evaluate(TX, '.st-sec'), LI(pj, 1).inner_text()]
        check('LE POINT — écran ouvert en Europe : toutes les heures du bloc sont celles de MIAMI (activée à 15:00 la veille, départ de la courbe à 15:00, action signée à 09:32) — pas l\'heure de l\'écran', 'à 15:00' in eu[0] and 'à 15:00' in eu[1] and 'heures de Miami' in eu[1] and 'le 3 novembre 2026 à 09:32' in eu[2], eu)
        pj.context.close()
        pe = ouvre(lg='en'); pe.evaluate(ACT, 3 * 24); pe.wait_for_timeout(500)
        te = pe.evaluate(TXL, '.st-tuiles, .st-sec, .st-camp, .st-tout, .st-acts')
        check('en : la pub depuis le redémarrage, le tableau des ventes et les actions sont en anglais, plus un mot de français', 'Progress since the restart' in te and 'Miami time' in te and 'spent on ads' in te and 'result of the ads' in te and 'To do' in te and 'Day by day' in te and 'Per day, on average' in te and 'All online sales since activation' in te and not re.search(r'Dépensé|Résultat|jour |depuis|Commandes|Pourquoi, comment', te), te[:500])
        check('en : la signature de l\'ERP est en anglais — « Done by the ERP on November 3, 2026 »', 'Done by the ERP on November 3, 2026' in pe.evaluate(TX, '.st-acts'), pe.evaluate(TX, '.st-acts')[:300])
        pe.context.close()
        check('6. aucune erreur JS', not err, err[:3])
        b.close()
finally:
    srv.terminate()
print('\n%d ok, %d KO %s' % (ok, len(ko), ko))
