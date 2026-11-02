# Audit « rien ne déborde » : chaque page, dans les trois langues, à plusieurs
# largeurs d'écran, avec des données réalistes (ventes de caisse aux numéros longs,
# noms de parfums longs, alertes, file d'attente, expéditions). Igal, 24 sept. 2026 :
# « vérifie toutes les listes dans toutes les langues, fais attention aux alertes,
# que ça ne déborde pas de partout ». Un tableau qui défile de côté, qui sort du
# cadre, ou un en-tête écrit deux fois = un souci.
import pathlib, subprocess, time, socket, json, random, sys
from playwright.sync_api import sync_playwright

D = pathlib.Path('/home/claude/catalogue')
CAT = json.load(open(D / 'cat.json'))
random.seed(7)
PAGES = sys.argv[3].split(',') if len(sys.argv) > 3 else ['catalogue', 'stock', 'inventaire_pc', 'quotes', 'factures', 'ventes', 'expeditions', 'fournisseurs',
         'etude', 'clients', 'connecteurs', 'messages', 'journal', 'tableau', 'acces', 'reglages']
LARGEURS = [int(x) for x in (sys.argv[1].split(',') if len(sys.argv) > 1 else ['1200', '1440', '1568', '1920'])]
LANGS = sys.argv[2].split(',') if len(sys.argv) > 2 else ['fr', 'en', 'es']
enstock = [r for r in CAT if (r[6] or 0) > 0 and r[0]]
longs = sorted(enstock, key=lambda r: -len((r[2] or '') + (r[1] or '')))[:30] + random.sample(enstock, 60)
# des ventes de tous les canaux, dont des numéros de caisse au format interne
FACT = []
for i, r in enumerate(longs):
    src = ['lightspeed', 'woocommerce', 'amazon', 'woocommerce-gros', ''][i % 5]
    canal = {'lightspeed': 'Caisse Lightspeed', 'woocommerce': 'Site perfumestrade.com', 'amazon': 'Amazon',
             'woocommerce-gros': 'Site wholesale.perfumestrade.com', '': 'Boutique'}[src]
    num = {'lightspeed': '161cfa62-e6f7-a592-11f1-b84381ae%04x' % i, 'amazon': '114-%07d-%07d' % (i * 7919, i * 104729),
           'woocommerce': str(20600 + i), 'woocommerce-gros': str(900 + i), '': 'V260924-%d' % i}[src]
    ref = ((r[2] or '') + ' ' + (r[1] or '') + (' ' + r[4] if r[4] else '')).strip()
    FACT.append({'id': 'f%d' % i, 'num': num, 'sens': 'vente', 'canal': canal, 'export': canal, 'tiers': 'Client Très Long Nom Numéro %d' % i,
                 'd': '2026-09-%02d' % (1 + i % 24), 'h': '%02d:%02d' % (8 + i % 12, i % 60),
                 'lignes': [{'cle': r[15], 'bc': r[0], 'ref': ref, 'q': 1 + i % 3, 'p': float(r[7] or 50), 'qAv': 5, 'qAp': 4, 'paAv': float(r[12] or 20)}],
                 'montant': float(r[7] or 50) * (1 + i % 3), 'stock': True, 'par': 'Sam', 't': '2026-09-%02dT12:00:00Z' % (1 + i % 24), 'auto': src})
FILE = [{'_i': 'amazon|%d' % i, 'src': 'amazon', 'd': '2026-09-%02d' % (10 + i), 'h': '10:%02d' % i, 'num': '113-%07d-5556667' % i, 'client': 'Acheteur au nom interminable %d' % i,
         'lignes': [{'bc': '9%011d' % i, 'des': 'BULGARI BULGARI EAU PARFUMEE PERFUME 2.5 OZ WHITE TEA AU THE BLANC COLOGNE SPRAY', 'q': 1, 'p': 45}]} for i in range(6)]
EXP = [{'_i': 'woocommerce|x%d' % i, 'src': ['woocommerce', 'amazon'][i % 2], 'num': str(20700 + i), 'client': 'Client Expédition %d' % i, 'd': '2026-09-%02d' % (18 + i), 'h': '09:00',
        'lignes': [{'cle': r[15], 'bc': r[0], 'des': r[1], 'q': 1, 'p': float(r[7] or 50), 'ref': ((r[2] or '') + ' ' + (r[1] or '')).strip()}],
        'montant': float(r[7] or 50), 'arrive': '2026-09-24T10:00:00Z', 'statut': 'attente'} for i, r in enumerate(longs[:8])]
MOD = {r[15]: {'qte': 2} for r in longs[:10]}
SITE = {str(r[0]): {'d': {'id': 1000 + i, 'q': (r[6] or 0) + (i % 3), 'suivi': True, 'etat': 'instock', 'nom': 'x', 'pr': float(r[7] or 50) + 10, 'ps': float(r[7] or 50)},
                    'g': {'id': 1000 + i, 'q': 0, 'suivi': True, 'etat': 'outofstock', 'nom': 'x', 'pr': float(r[8] or 30), 'ps': None}} for i, r in enumerate(longs)}
JOU = [{'t': '2026-09-%02dT1%d:00:00Z' % (1 + i % 24, i % 10), 'u': 'Sam', 'act': ['vente', 'stock', 'prix', 'annulation'][i % 4],
        'lib': 'une ligne de journal assez longue pour voir si elle passe à la ligne correctement, numéro %d' % i, 'ref': longs[i % 30][15], 'av': '10', 'ap': '12'} for i in range(80)]
# l'étude d'un devis déjà collé (brouillon) et des achats passés : c'est avec la
# colonne « Dernier achat » et ses fournisseurs que le tableau s'élargissait
HIST = {r[15]: [{'d': '2026-0%d-1%d' % (1 + k, k), 'p': float(r[12] or 20) * (1 + k / 20), 'f': 'Fournisseur au très long nom SARL', 'q': 6} for k in range(3)] for r in longs[:30]}
ETU = '\n'.join(f"{r[0]}\t{(r[2] or '')} {(r[1] or '')} EAU DE PARFUM SPRAY\t3\t{round(float(r[12] or 20) * 0.95, 2)}" for r in longs[:20]) + '\n123456789012\tUNKNOWN PRODUCT LONG DESCRIPTION\t2\t19.5'
AUDIT = open(D / '_audit_cadres.js').read()

s = socket.socket(); s.bind(('127.0.0.1', 0)); port = s.getsockname()[1]; s.close()
srv = subprocess.Popen(['python3', '-m', 'http.server', str(port), '--bind', '127.0.0.1'], cwd=str(D), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1)
soucis = {}
try:
    with sync_playwright() as p:
        b = p.chromium.launch()
        for w in LARGEURS:
            for lg in LANGS:
                pg = b.new_page(viewport={'width': w, 'height': 900}); err = []
                pg.on('pageerror', lambda e: err.append(str(e)))
                pg.goto(f'http://127.0.0.1:{port}/accueil.html'); pg.wait_for_timeout(300)
                pg.evaluate("localStorage.setItem('sam-session-v1', JSON.stringify({id:'igal',nom:'Igal',role:'admin',depuis:new Date().toISOString()}))")
                pg.evaluate("([F,Q,E,M,S,J,H,T,l])=>{ localStorage.setItem('factures-v1',JSON.stringify(F)); localStorage.setItem('caisse-file-v1',JSON.stringify(Q)); localStorage.setItem('expeditions-v1',JSON.stringify(E)); localStorage.setItem('fiches-modifiees-v1',JSON.stringify(M)); localStorage.setItem('site-stock-v1',JSON.stringify(S)); localStorage.setItem('crm-journal-v1',JSON.stringify(J)); localStorage.setItem('langue-v1',l); localStorage.setItem('prix-achat-hist-v1',JSON.stringify(H)); localStorage.setItem('etude-brouillon-v1',JSON.stringify({texte:T,frn:'',date:'2026-09-24',num:''})); localStorage.setItem('reglages-v1',JSON.stringify({exped:{woocommerce:false,amazon:false,'woocommerce-gros':false}})); }", [FACT, FILE, EXP, MOD, SITE, JOU, HIST, ETU, lg])
                for page in PAGES:
                    pg.goto(f'http://127.0.0.1:{port}/{page}.html'); pg.wait_for_timeout(1800)
                    r = json.loads(pg.evaluate(AUDIT))
                    if r['s']: soucis[f'{page} {lg} {w}'] = r['s']
                if err: soucis[f'ERREURS JS {lg} {w}'] = err[:3]
                pg.close()
        b.close()
finally:
    srv.terminate()
for k, v in soucis.items(): print(k, '→', ' | '.join(v))
print(f"\n{len(soucis)} page(s) avec un souci")
