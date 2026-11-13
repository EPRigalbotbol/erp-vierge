# LA PROVENANCE D'UNE VENTE DU SITE (13 nov. 2026 — Igal : « sur la ligne des ventes, seulement sur perfumestrade.com, la provenance
# de la vente, pour savoir si c'est grâce à Google Ads »). La boutique note d'où venait l'acheteur ; le cockpit le range par commande
# (ventes-origine-v1 : « woocommerce|<n°> » → gads, gshop, google, direct, ia, site:…). Ce test protège :
#   1. LE POINT : la pastille d'une vente de perfumestrade.com dit sa provenance — « · Pub Google » en plein (bleu) pour une
#      publicité payée, les autres en clair (Recherche Google, Venu directement, IA, un autre site…) ;
#   2. seulement perfumestrade.com : le site de gros, la caisse, Perfume City et une vente saisie à la main n'ont pas cette mention ;
#   3. une vente du site dont l'origine n'est pas encore lue : la pastille reste comme avant, sans rien inventer ;
#   4. la bulle de la pastille l'explique en une phrase ; en anglais et en espagnol, tout est traduit ;
#   5. un rôle qui ne reçoit pas ce magasin (Commercial) ne voit rien de plus ; aucune erreur JS.
import subprocess, time, socket, json, sys
from playwright.sync_api import sync_playwright
D = '/home/claude/catalogue'
ok = 0; ko = []
def check(n, c, i=''):
    global ok
    if c: ok += 1; print('  ok  ', n)
    else: ko.append(n); print('  KO  ', n, str(i)[:500])
C = json.load(open(D + '/cat.json'))
A = [r for r in C if (r[6] or 0) > 0 and r[0] and r[0].isdigit() and (r[12] or 0) > 0][0]
def vente(i, num, auto, canal):
    return {'id': 'f' + i, 'num': num, 'sens': 'vente', 'canal': canal, 'auto': auto, 'd': '2026-11-11', 'h': '12:00', 't': '2026-11-11T17:00:00Z', 'stock': False,
            'par': 'auto', '_i': 'fa|' + (auto or 'main') + '|' + i, 'lignes': [{'cle': A[15], 'bc': A[0], 'ref': A[2] + ' ' + A[13], 'q': 1, 'p': 60}], 'montant': 60}
F = [vente('1', '9101', 'woocommerce', 'Site perfumestrade.com'), vente('2', '9102', 'woocommerce', 'Site perfumestrade.com'), vente('3', '9103', 'woocommerce', 'Site perfumestrade.com'),
     vente('4', '9104', 'woocommerce', 'Site perfumestrade.com'), vente('5', '9105', 'woocommerce', 'Site perfumestrade.com'), vente('6', '9106', 'woocommerce', 'Site perfumestrade.com'),
     vente('7', '9201', 'woocommerce-gros', 'Site wholesale.perfumestrade.com'), vente('8', 'PC-9301', 'shopify-pc', 'Perfume City'), vente('9', 'V-9401', '', 'Gros')]
ORI = {'woocommerce|9101': 'gads', 'woocommerce|9102': 'google', 'woocommerce|9103': 'direct', 'woocommerce|9104': 'ia', 'woocommerce|9105': 'site:fragrantica.com',
       'woocommerce-gros|9201': 'gads', 'shopify-pc|9301': 'gads', '_woocommerce': {'maj': '2026-11-11T17:00:00Z'}}
s = socket.socket(); s.bind(('127.0.0.1', 0)); port = s.getsockname()[1]; s.close()
srv = subprocess.Popen(['python3', '-m', 'http.server', str(port), '--bind', '127.0.0.1'], cwd=D, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)
SESS = """([F,O,role,lg])=>{ localStorage.clear(); localStorage.setItem('sam-comptes-demo-v1','0');
  localStorage.setItem('sam-session-v1',JSON.stringify({id:'sam',nom:'Sam',role:role,depuis:new Date().toISOString()}));
  localStorage.setItem('langue-v1',lg); localStorage.setItem('factures-v1',JSON.stringify(F)); if(O) localStorage.setItem('ventes-origine-v1',JSON.stringify(O)); }"""
PAST = "()=>Object.fromEntries([...document.querySelectorAll('tr[data-d]')].map(tr=>{ const c=tr.querySelector('.cnl .ch'); return [tr.querySelector('.num').textContent.trim(), [c.textContent.replace(/\\s+/g,' ').trim(), c.className, c.getAttribute('title')||'']]; }))"
try:
    with sync_playwright() as p:
        b = p.chromium.launch(); err = []
        def ouvre(role='patron', lg='fr', ori=ORI):
            pg = b.new_page(viewport={'width': 1500, 'height': 1000}); pg.on('pageerror', lambda e: err.append(str(e)))
            base = f'http://127.0.0.1:{port}/'
            pg.goto(base + 'accueil.html'); pg.wait_for_timeout(300); pg.evaluate(SESS, [F, ori, role, lg])
            pg.goto(base + 'ventes.html'); pg.wait_for_timeout(2500)
            pg.evaluate("()=>{ $('fp').value=''; vus=80; dessine(); }"); pg.wait_for_timeout(500); return pg
        pg = ouvre(); P = pg.evaluate(PAST)
        check('LE POINT — une vente du site venue d\'une publicité payée : la pastille dit « · Pub Google », en plein (bleu)', P['9101'][0].endswith('· Pub Google') and 'or-pub' in P['9101'][1], P.get('9101'))
        check('les autres provenances sont écrites en clair, sans le plein : Recherche Google, Venu directement, IA (ChatGPT…), fragrantica.com',
              P['9102'][0].endswith('· Recherche Google') and P['9103'][0].endswith('· Venu directement') and P['9104'][0].endswith('· IA (ChatGPT…)') and P['9105'][0].endswith('· fragrantica.com')
              and all('or-pub' not in P[k][1] and 'or-autre' in P[k][1] for k in ('9102', '9103', '9104', '9105')), [P[k][0] for k in ('9102', '9103', '9104', '9105')])
        check('LE POINT — une vente du site dont l\'origine n\'est pas encore lue : la pastille reste comme avant (rien d\'inventé)', '·' not in P['9106'][0] and 'or-' not in P['9106'][1], P.get('9106'))
        check('LE POINT — seulement perfumestrade.com : le site de gros, Perfume City et une vente saisie à la main n\'ont pas cette mention (même si le magasin en a une)',
              all('Pub Google' not in P[k][0] and 'or-pub' not in P[k][1] for k in ('9201', 'PC-9301', 'V-9401')), [P[k][0] for k in ('9201', 'PC-9301', 'V-9401')])
        check('la bulle de la pastille l\'explique : « Origine du client : un clic sur une publicité Google payée »', 'Origine du client : un clic sur une publicité Google payée' in P['9101'][2], P['9101'][2][-140:])
        pg.close()
        for lg, pub, rech, direct, bulle in (('en', 'Google Ads', 'Google search', 'Direct', 'Customer origin: a click on a paid Google ad'), ('es', 'Anuncio Google', 'Búsqueda de Google', 'Directo', 'Origen del cliente: un clic en un anuncio de Google de pago')):
            pg = ouvre(lg=lg); P = pg.evaluate(PAST)
            check(f'LE POINT — {lg} : la provenance est traduite (« {pub} », « {rech} », « {direct} ») et la bulle aussi', P['9101'][0].endswith('· ' + pub) and P['9102'][0].endswith('· ' + rech) and P['9103'][0].endswith('· ' + direct) and bulle in P['9101'][2]
                  and 'Pub Google' not in P['9101'][0] and 'Recherche' not in P['9102'][0], [P['9101'][0], P['9102'][0], P['9103'][0], P['9101'][2][-90:]])
            pg.close()
        pg = ouvre(role='commercial', ori=None); P = pg.evaluate(PAST)
        check('un Commercial, qui ne reçoit pas ce magasin, voit la pastille comme avant', all('·' not in P[k][0] for k in ('9101', '9102', '9103')), [P[k][0] for k in ('9101', '9102')])
        pg.close()
        check('aucune erreur JS', not err, err[:3])
        b.close()
finally:
    srv.terminate()
print(f'\n{ok} ok, {len(ko)} KO', ko); sys.exit(1 if ko else 0)
