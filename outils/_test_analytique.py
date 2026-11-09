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
        '_shopify-pc': {'maj': '2026-11-15T13:50:00Z', 'err': 'Shopify : Access denied for customerJourneySummary field.'}}
PCO = {'shopify-pc|11': 'boutique', 'shopify-pc|12': 'en ligne'}
GPUB = {'j': {J(2): [50, 300, 20, 1000, 2, 1, 40], J(3): [70, 100, 30, 1200, 1, 0, 30], J(40): [40, 100, 10, 500, 1, 0, 10]}, '_maj': '2026-11-15T13:00:00Z', '_err': ''}
REG = {'comV4': 1, 'canauxV': 3, 'pcCom3': 1, 'canaux': [{'id': 'site', 'nom': 'Site perfumestrade.com', 'com': 3}, {'id': 'sitegros', 'nom': 'Site wholesale.perfumestrade.com', 'com': 3},
       {'id': 'amazon', 'nom': 'Amazon', 'com': 15}, {'id': 'perfumecity', 'nom': 'Perfume City', 'com': 3}], 'envois': {'woocommerce': 0, 'woocommerce-gros': 0, 'shopify-pc': 0}}
SESS = """([F,O,P,G,R,lg,role])=>{ localStorage.clear(); localStorage.setItem('sam-comptes-demo-v1','0');
  localStorage.setItem('sam-session-v1',JSON.stringify({id:'x',nom:'Essai',role,depuis:new Date().toISOString()}));
  localStorage.setItem('langue-v1',lg); localStorage.setItem('factures-v1',JSON.stringify(F)); localStorage.setItem('ventes-origine-v1',JSON.stringify(O));
  localStorage.setItem('pc-origine-v1',JSON.stringify(P)); localStorage.setItem('google-pub-v1',JSON.stringify(G)); localStorage.setItem('reglages-v1',JSON.stringify(R)); }"""
FR = re.compile(r"\b(Chiffre d'affaires|Marge nette|Ventes des sites|Commandes en ligne|Venues de Google|Venus directement|Recherche Google|Origine inconnue|Au fil des jours|Le classement|Site par site|Tous les canaux|Ce qui reste|pub dépensée|Comment c'est compté|jours|Mois dernier|Cette année|Ce mois|commandes?|Voir les chiffres)\b|[éèêàç]")
s = socket.socket(); s.bind(('127.0.0.1', 0)); port = s.getsockname()[1]; s.close()
srv = subprocess.Popen(['python3', '-m', 'http.server', str(port), '--bind', '127.0.0.1'], cwd=D, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)
try:
    with sync_playwright() as p:
        b = p.chromium.launch(); err = []
        def ouvre(lg='fr', role='patron', page='analytique.html', avant=None):
            ctx = b.new_context(viewport={'width': 1440, 'height': 1000}, timezone_id='America/New_York', locale='fr-FR')
            pg = ctx.new_page(); pg.on('pageerror', lambda e: err.append(str(e))); pg.on('dialog', lambda d: d.accept())
            pg.add_init_script("Object.defineProperty(window,'D_HG',{configurable:true,set(v){ window.__hgReel=v; },get(){ return null; }})")
            pg.clock.set_fixed_time(datetime.datetime(auj.year, auj.month, auj.day, 14, 0, tzinfo=ZoneInfo('America/New_York')))
            base = f'http://127.0.0.1:{port}/'
            pg.goto(base + 'accueil.html'); pg.wait_for_timeout(300); pg.evaluate(SESS, [F, ORIG, PCO, GPUB, REG, lg, role])
            if avant: pg.add_init_script(avant)
            pg.goto(base + page); pg.wait_for_timeout(2600); return pg
        pg = ouvre()
        if os.environ.get('AN_SHOT'):
            pg.screenshot(path=os.environ['AN_SHOT'] + '_fr.png', full_page=True)
            pg.emulate_media(color_scheme='dark'); pg.wait_for_timeout(300); pg.screenshot(path=os.environ['AN_SHOT'] + '_sombre.png', full_page=True); pg.emulate_media(color_scheme='light')
        T = pg.inner_text('#an')
        check('la page s\'ouvre sur « 30 jours »', pg.evaluate("()=>document.querySelector('[data-an].on').dataset.an") == 'rel:30')
        # 2. mêmes chiffres que le Tableau de bord
        tot = pg.evaluate("()=>{ const P=rcPlage('rel:30'); const R=rcAgrege(rcLignes(),P.a,P.b); return [Math.round(R.T.ca*100)/100, Math.round(R.T.mg*100)/100]; }")
        check('LE POINT — le chiffre d\'affaires de la page = celui du calcul du Tableau de bord (100+200+100+100+60+90+90+550 = 1 290 $)', tot[0] == 1290 and a(T, 1290), [tot, T[:300]])
        pt = ouvre(page='tableau.html')
        tb = pt.evaluate("()=>{ const P=rcPlage('rel:30'); const R=rcAgrege(rcLignes(),P.a,P.b); return [Math.round(R.T.ca*100)/100, Math.round(R.T.mg*100)/100]; }")
        check('LE POINT — même total et même marge que tableau.html', tb == tot, [tb, tot])
        pt.context.close()
        # 3. origines comptées à la main
        k = pg.evaluate("()=>{ const L=rcLignes(); const C=__an.anCommandes(L); const o={}; C.filter(x=>x.d>='2026-10-17').forEach(x=>{ o[x.fam]=(o[x.fam]||0)+1; }); return o; }")
        check('3. origines : 1 Google Shopping, 2 Google Ads, 1 direct, 1 réseau social, 1 recherche Google, PC boutique exclue', k == {'gshop': 1, 'gads': 2, 'direct': 1, 'social': 1, 'google': 1}, k)
        kp = pg.locator('.an-kpi').all_inner_texts()
        check('« Ventes des sites » = 100+200+100+100+60+90 = 650 $ (la vente en boutique de Perfume City n\'est pas un site)', a(kp[2], 650), kp[2])
        check('« Commandes en ligne » = 6, panier moyen 108 $', kp[3].split('\n')[1].strip() == '6' and a(kp[3], 108), kp[3])
        check('« Venues de Google » = 4 commandes sur 6 = 67 %', '67 %' in kp[4] and '4 ' in kp[4], kp[4])
        check('le classement montre Instagram sous « Réseaux sociaux »', 'Instagram 1' in T, T)
        # 4. Google : pub vs marge
        g = pg.locator('.an-kpi').all_inner_texts()[5:10]
        check('LE POINT — pub dépensée sur 30 jours = 50 + 70 = 120 $ (la pub d\'il y a 40 jours n\'y est pas)', a(g[0], 120), g[0])
        check('ventes « selon Google » = 400 $, rapport 3,3 ×', a(g[1], 400) and '3,3' in g[1], g[1])
        mgAds = pg.evaluate("()=>{ const C=__an.anCommandes(rcLignes()).filter(o=>o.site==='site'&&o.fam==='gads'&&o.d>='2026-10-17'); return Math.round(C.reduce((a,o)=>a+o.mg,0)*100)/100; }")
        check('LE POINT — « ce qui reste après la pub » = marge des commandes Google Ads − 120 $', a(g[3], round(mgAds - 120)), [mgAds, g[3]])
        check('les fiches gratuites : 1 clic, 70 affichages', '1 clic' in g[4] and '70' in g[4], g[4])
        check('une relecture en panne (Shopify) est dite en haut de la page', 'Access denied' in T and pg.locator('.an-alerte').count() == 1, T[:400])
        # 5. période et infobulle
        pg.click('[data-an="rel:7"]'); pg.wait_for_timeout(300)
        check('5. « 7 jours » : 7 colonnes', pg.locator('.rc-col').count() == 7, pg.locator('.rc-col').count())
        col = pg.locator('.rc-col').nth(4); col.hover(); pg.wait_for_timeout(150)
        tip = pg.evaluate("()=>{ const t=[...document.querySelectorAll('.rc-tip')].find(x=>x.style.display==='block'); return t?t.innerText:''; }")
        check('5. l\'infobulle dit le jour et l\'origine', 'Google' in tip, tip)
        pg.click('[data-anm="n"]'); pg.wait_for_timeout(200)
        check('5. la bascule « Commandes » redessine', pg.locator('[data-anm="n"].on').count() == 1)
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
        # 6. langues
        for lg in ('en', 'es'):
            pe = ouvre(lg=lg)
            te = pe.inner_text('main')
            fr = sorted(set(m.group(0) for m in FR.finditer(te)))
            check(f'6. {lg} : la page est en anglais, plus un mot de français', not fr and 'where website orders come from' in te.lower() and 'Analytics' in pe.inner_text('.side'), fr[:12])
            pe.context.close()
        check('6. aucune erreur JS', not err, err[:3])
        b.close()
finally:
    srv.terminate()
print('\n%d ok, %d KO %s' % (ok, len(ko), ko))
