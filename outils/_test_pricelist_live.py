# LA PRICE LIST EN DIRECT DES CLIENTS DE GROS, CÔTÉ ERP (Sam via Igal, 15 nov. 2026 : une price list « en live » comme celle de
# MTZ, ouverte par email + code, d'où le client commande ; « que la quantité qu'il ajoute ne puisse pas être supérieure à la
# quantité restante » ; choix d'Igal : seuls les clients autorisés par Sam, la commande devient une cote à valider).
# Le cockpit (cockpit/pricelist.js, _t_pricelist.mjs) sert la page ; ce test protège ce que l'ERP lui donne et ce qu'il en fait :
#   1. LE POINT — le Catalogue publie pricelist-v1 : seulement les fiches en stock avec un prix de gros (celui du canal wholesale),
#      jamais le prix d'achat ; la photo prise par Sam part en « perso:<clé> » ; un Commercial ne publie rien ;
#   2. LE POINT — Clients : la case « price list en direct » de la fiche donne l'accès (pricelist-acces-v1, email en minuscules) ;
#      la décocher le retire ; un client sans email est signalé ; un Commercial ne peut pas cocher ;
#   3. LE POINT — Cote : la commande reçue s'affiche ; « Faire la cote » prépare la cote (client, canal Gros, parfums, quantités,
#      prix de la commande) et marque la commande ; « Archiver » la range ; les demandes d'emails non autorisés sont montrées ;
#   4. traduit en anglais et en espagnol ; aucune erreur JS.
import subprocess, time, socket, json
from playwright.sync_api import sync_playwright
D = '/home/claude/catalogue'
ok = 0; ko = []
def check(n, c, i=''):
    global ok
    if c: ok += 1; print('  ok  ', n)
    else: ko.append(n); print('  KO  ', n, str(i)[:600])
C = json.load(open(D + '/cat.json'))
# des parfums réels du catalogue, choisis par leurs chiffres (jamais nommés ici) : en stock avec un prix de gros ; un à 0
P = [r for r in C if (r[6] or 0) > 2 and r[15] and (r[8] or 0) > 0 and (r[12] or 0) > 0]
A, B = P[0], P[1]
Z = [r for r in C if (r[6] or 0) <= 0 and r[15] and (r[8] or 0) > 0][0]
SG = [r for r in C if (r[6] or 0) > 0 and r[15] and not r[8] and not r[7]]
PNG = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=='
F = [{'id': 'f1', 'num': '9001', 'sens': 'vente', 'canal': 'Vente en gros', 'd': '2026-11-01', 'h': '12:00', 't': '2026-11-01T17:00:00Z', 'stock': False,
      'tiers': 'Grossiste Uno', 'lignes': [{'cle': A[15], 'bc': A[0], 'ref': A[13], 'q': 2, 'p': A[8]}], 'montant': 2 * A[8]},
     {'id': 'f2', 'num': '9002', 'sens': 'vente', 'canal': 'Vente en gros', 'd': '2026-11-02', 'h': '12:00', 't': '2026-11-02T17:00:00Z', 'stock': False,
      'tiers': 'Grossiste Sans Mail', 'lignes': [{'cle': B[15], 'bc': B[0], 'ref': B[13], 'q': 1, 'p': B[8]}], 'montant': B[8]}]
CLI = {'Grossiste Uno': {'nom': 'Grossiste Uno', 'prenom': 'Uno', 'email': 'Uno@Exemple.com', 'tel': '3055550106', 'langue': 'es'},
       'Grossiste Sans Mail': {'nom': 'Grossiste Sans Mail', 'tel': '3055550107'}}
CMD = [{'num': 'PL-1001', 't': '2026-11-15T15:00:00Z', 'email': 'uno@exemple.com', 'client': 'Grossiste Uno', 'lg': 'es', 'total': 3 * A[8] + B[8],
        'lignes': [{'k': A[15], 'bc': A[0], 'marque': A[2], 'nom': A[13], 'ml': A[3], 'type': A[4], 'q': 3, 'p': A[8]},
                   {'k': B[15], 'bc': B[0], 'marque': B[2], 'nom': B[13], 'ml': B[3], 'type': B[4], 'q': 1, 'p': B[8]}], 'note': 'Livraison mardi'},
       {'num': 'PL-1002', 't': '2026-11-15T16:00:00Z', 'email': 'uno@exemple.com', 'client': 'Grossiste Uno', 'lg': 'es', 'total': A[8],
        'lignes': [{'k': A[15], 'bc': A[0], 'marque': A[2], 'nom': A[13], 'ml': A[3], 'type': A[4], 'q': 1, 'p': A[8]}]}]
DEM = [{'email': 'inconnu@exemple.com', 't': '2026-11-15T14:00:00Z'}]
import datetime
_m = lambda h: (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(minutes=h)).strftime('%Y-%m-%dT%H:%M:%S.000Z')
VIS = [{'t': _m(2), 'quoi': 'visite', 'email': 'uno@exemple.com', 'nom': 'Grossiste Uno', 'app': 'telephone'},
       {'t': _m(5), 'quoi': 'commande', 'email': 'uno@exemple.com', 'nom': 'Grossiste Uno', 'num': 'PL-1002', 'total': 10},
       {'t': _m(8), 'quoi': 'visite', 'email': 'uno@exemple.com', 'nom': 'Grossiste Uno', 'app': 'ordinateur'},
       {'t': _m(9), 'quoi': 'entree', 'email': 'uno@exemple.com', 'nom': 'Grossiste Uno', 'app': 'ordinateur'},
       {'t': _m(10), 'quoi': 'faux', 'email': 'uno@exemple.com', 'nom': 'Grossiste Uno'},
       {'t': _m(11), 'quoi': 'refuse', 'email': 'inconnu@exemple.com'}]
s = socket.socket(); s.bind(('127.0.0.1', 0)); port = s.getsockname()[1]; s.close()
srv = subprocess.Popen(['python3', '-m', 'http.server', str(port), '--bind', '127.0.0.1'], cwd=D, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)
SESS = """([F,CLI,lg,role,X])=>{ localStorage.clear(); localStorage.setItem('sam-comptes-demo-v1','0');
  localStorage.setItem('sam-session-v1',JSON.stringify({id:'sam',nom:'Sam',role:role,depuis:new Date().toISOString()}));
  localStorage.setItem('crm-utilisateur-v1','Sam');
  localStorage.setItem('langue-v1',lg); localStorage.setItem('factures-v1',JSON.stringify(F)); localStorage.setItem('clients-v1',JSON.stringify(CLI));
  for(const k in X) localStorage.setItem(k,JSON.stringify(X[k])); }"""
try:
    with sync_playwright() as p:
        b = p.chromium.launch(); err = []
        def ouvre(page, lg='fr', role='patron', X=None, attente=2200):
            ctx = b.new_context(viewport={'width': 1500, 'height': 1000})
            pg = ctx.new_page(); pg.on('pageerror', lambda e: err.append(page + ' ' + str(e)))
            ctx.route('https://web.whatsapp.com/**', lambda r: r.abort())
            base = f'http://127.0.0.1:{port}/'
            pg.goto(base + 'accueil.html'); pg.wait_for_timeout(300); pg.evaluate(SESS, [F, CLI, lg, role, X or {}])
            pg.goto(base + page); pg.wait_for_timeout(attente); return pg, ctx
        LS = lambda pg, k: pg.evaluate("k=>JSON.parse(localStorage.getItem(k)||'null')", k)

        # ---- 1. le Catalogue publie la price list ----
        pg, ctx = ouvre('catalogue.html', X={'photos-perso-v1': {B[15]: PNG}}, attente=7000)
        T = LS(pg, 'pricelist-v1')
        check('LE POINT — le Catalogue (Patron) publie la price list pour le cockpit', bool(T) and isinstance(T.get('L'), list) and len(T['L']) > 100, (T or {}).get('t'))
        L = T['L'] if T else []
        par = {r[10]: r for r in L}
        attendu = pg.evaluate("""()=>{ const C=canaux(), cg=C.find(c=>c.id==='sitegros');
          return tousLesArticles().filter(p=>p.bc&&(+p.qte||0)>0&&!horsCanal(p,'sitegros')&&prixCanal(p,cg).v>0).length; }""")
        check('autant de lignes que de fiches en stock avec un prix de gros', len(L) == attendu, [len(L), attendu])
        check('LE POINT — chaque ligne : 11 cases, en stock, avec un prix de gros (aucune à 0)', all(len(r) == 11 and r[7] > 0 and r[6] > 0 for r in L), L[:2])
        check('LE POINT — jamais le prix d\'achat dans ce qui part vers le cockpit', A[15] in par and A[12] not in par[A[15]][:6] + par[A[15]][7:] or A[12] == par[A[15]][6], par.get(A[15]))
        px = pg.evaluate("c=>{ const p=tousLesArticles().find(x=>x.id===c); const cg=canaux().find(x=>x.id==='sitegros'); return prixCanal(p,cg).v; }", A[15])
        check('le prix est celui du canal wholesale (le même que le site de gros)', A[15] in par and abs(par[A[15]][6] - px) < 0.01, [par.get(A[15]), px])
        check('un parfum à 0 en stock n\'y est pas', Z[15] not in par)
        check('la photo prise par Sam part en « perso:<clé> » (le cockpit la sert lui-même)', B[15] in par and par[B[15]][8] == 'perso:' + B[15], par.get(B[15]))
        check('les autres photos partent avec une adresse https complète, ou vides', all((not r[8]) or r[8].startswith('https://') or r[8].startswith('perso:') for r in L))
        check('la clé de chaque ligne est celle de la fiche (la cote la retrouve)', all(r[10] for r in L) and par.get(A[15], [None] * 11)[0] == A[0])
        ctx.close()
        pg, ctx = ouvre('catalogue.html', role='commercial', attente=7000)
        check('un Commercial ne publie pas la price list', LS(pg, 'pricelist-v1') is None)
        ctx.close()

        # ---- 2. Clients : la case d'accès ----
        pg, ctx = ouvre('clients.html', X={'pricelist-visites-v1': VIS})
        pg.evaluate("()=>{ ouvre('Grossiste Uno'); onglet('coord'); }"); pg.wait_for_timeout(300)
        t = pg.inner_text('#pl-box')
        check('la fiche montre la case « price list en direct »', 'price list en direct' in t.lower() and pg.locator('#pl-on').count() == 1, t)
        pg.locator('#pl-on').check(); pg.wait_for_timeout(300)
        A1 = LS(pg, 'pricelist-acces-v1'); c1 = LS(pg, 'clients-v1')
        check('LE POINT — cocher donne l\'accès : la fiche garde la case, le cockpit reçoit l\'email (en minuscules) et la langue',
              c1['Grossiste Uno'].get('plAcces') is True and A1 and A1['L'] == [{'nom': 'Grossiste Uno', 'email': 'uno@exemple.com', 'lg': 'es'}], [A1, c1.get('Grossiste Uno')])
        t = pg.inner_text('#pl-box')
        check('la fiche du client montre sa dernière connexion et ses ouvertures sur 7 jours', 'Dernière connexion' in pg.inner_text('#pl-box') and '3 ouverture(s)' in pg.inner_text('#pl-box'), pg.inner_text('#pl-box'))
        check('la fiche dit avec quel email il entre, et propose le lien (copie, WhatsApp)', 'uno@exemple.com' in t.lower() and 'Copier le lien' in t and 'WhatsApp' in t, t)
        J = LS(pg, 'crm-journal-v1') or []
        check('l\'accès donné est signé au Journal', any('price list en direct donné' in (x.get('lib') or '') for x in J), J[-2:])
        pg.locator('#pl-on').uncheck(); pg.wait_for_timeout(300)
        A2 = LS(pg, 'pricelist-acces-v1')
        check('LE POINT — décocher retire l\'accès (la liste du cockpit est vide)', A2 and A2['L'] == [] and 'plAcces' not in LS(pg, 'clients-v1')['Grossiste Uno'], A2)
        pg.evaluate("()=>{ ouvre('Grossiste Sans Mail'); onglet('coord'); }"); pg.wait_for_timeout(300)
        pg.locator('#pl-on').check(); pg.wait_for_timeout(300)
        t = pg.inner_text('#pl-box')
        check('un client sans email : la fiche prévient qu\'il ne peut pas entrer, et il n\'est pas dans la liste', "pas d'email valable" in t and LS(pg, 'pricelist-acces-v1')['L'] == [], t)
        for lg, mot in (('en', 'Live price list'), ('es', 'Lista de precios en vivo')):
            pg.evaluate("lg=>{ localStorage.setItem('langue-v1',lg); }", lg); pg.reload(); pg.wait_for_timeout(1800)
            pg.evaluate("()=>{ ouvre('Grossiste Uno'); onglet('coord'); }"); pg.wait_for_timeout(300)
            t = pg.inner_text('#pl-box')
            check(f'la case est traduite ({lg})', mot.lower() in t.lower() and 'Ce client' not in t, t)
        ctx.close()
        pg, ctx = ouvre('clients.html', role='commercial')
        pg.evaluate("()=>{ ouvre('Grossiste Uno'); onglet('coord'); }"); pg.wait_for_timeout(300)
        check('un Commercial voit la case mais ne peut pas la cocher', pg.locator('#pl-on').is_disabled() and 'Seuls le Patron' in pg.inner_text('#pl-box'))
        ctx.close()

        # ---- 2 bis. l'onglet « Price list en direct » en haut de Clients (Igal, 16 nov. 2026) ----
        CLI2 = json.loads(json.dumps(CLI)); CLI2['Grossiste Uno'].update({'plAcces': True, 'plDepuis': '2026-11-15T15:00:00Z', 'plPar': 'Igal'})
        def ouvre2(lg='fr', role='patron', hashe='#pricelist'):
            ctx = b.new_context(viewport={'width': 1500, 'height': 1000}); pg = ctx.new_page(); pg.on('pageerror', lambda e: err.append('clients-pl ' + str(e)))
            base = f'http://127.0.0.1:{port}/'
            pg.goto(base + 'accueil.html'); pg.wait_for_timeout(300); pg.evaluate(SESS, [F, CLI2, lg, role, {'pricelist-visites-v1': VIS, 'pricelist-commandes-v1': CMD, 'pricelist-demandes-v1': DEM}])
            pg.goto(base + 'clients.html' + hashe); pg.wait_for_timeout(2200); return pg, ctx
        pg, ctx = ouvre2(hashe='')
        o = pg.inner_text('#cl-ong')
        check('LE POINT (onglet) — tout en haut de Clients : « Wholesale », « Retail » et « Price list en direct » avec le nombre', 'wholesale.perfumestrade.com' in o and 'Amazon' in o and 'Price list en direct' in o and '1' in o, o)
        pg.locator('#cl-ong button[data-o="pl"]').click(); pg.wait_for_timeout(300)
        t = pg.inner_text('#plv')
        check('l\'onglet liste les clients qui ont accès : nom, email, depuis quand et par qui, dernière connexion, commandes',
              'Grossiste Uno' in t and 'uno@exemple.com' in t and 'Igal' in t and '3 ouverture(s)' in t and 'PL-1001' in t and 'Grossiste Sans Mail' not in t, t[:800])
        check('la liste générale est cachée pendant ce temps', pg.locator('#corps').is_hidden(), '')
        check('les emails non autorisés qui ont demandé un code sont montrés', 'inconnu@exemple.com' in pg.evaluate("()=>document.querySelector('#plv details').textContent"))
        pg.once('dialog', lambda d: d.accept())
        pg.locator('#plv [data-pl="Grossiste Uno"]').uncheck(); pg.wait_for_timeout(300)
        A3 = LS(pg, 'pricelist-acces-v1')
        check('LE POINT (onglet) — décocher retire l\'accès tout de suite (le cockpit reçoit la liste vide)', A3 and A3['L'] == [] and 'plAcces' not in LS(pg, 'clients-v1')['Grossiste Uno'], A3)
        check('la ligne décochée reste visible, grisée, pour pouvoir se raviser ; le compteur passe à 0', pg.locator('#plv tr.off').count() == 1 and pg.locator('#cl-ong button[data-o="pl"] b').inner_text() == '0', pg.inner_text('#plv')[:300])
        pg.locator('#plv [data-pl="Grossiste Uno"]').check(); pg.wait_for_timeout(300)
        check('recocher redonne l\'accès (date et auteur notés)', LS(pg, 'pricelist-acces-v1')['L'] == [{'nom': 'Grossiste Uno', 'email': 'uno@exemple.com', 'lg': 'es'}] and LS(pg, 'clients-v1')['Grossiste Uno'].get('plPar') == 'Sam', LS(pg, 'clients-v1')['Grossiste Uno'])
        pg.fill('#plv-q', 'Grossiste Sans Mail'); pg.locator('#plv-ok').click(); pg.wait_for_timeout(300)
        check('donner l\'accès depuis l\'onglet ; un client sans email est signalé', LS(pg, 'clients-v1')['Grossiste Sans Mail'].get('plAcces') is True and 'pas d\'email' in pg.inner_text('#plv'), pg.inner_text('#plv-err'))
        J = LS(pg, 'crm-journal-v1') or []
        check('chaque geste est signé au Journal', sum(1 for x in J if 'price list en direct' in (x.get('lib') or '')) >= 3, [x.get('lib') for x in J[-4:]])
        ctx.close()
        pg, ctx = ouvre2()
        check('clients.html#pricelist ouvre directement l\'onglet (lien depuis la Cote)', pg.locator('#plv').is_visible() and 'Grossiste Uno' in pg.inner_text('#plv'))
        ctx.close()
        for lg, mot in (('en', 'Last sign-in'), ('es', 'Última conexión')):
            pg, ctx = ouvre2(lg=lg)
            t = pg.inner_text('#plv') + pg.inner_text('#cl-ong')
            check(f'l\'onglet est traduit ({lg})', mot.lower() in t.lower() and 'dernière connexion' not in t.lower() and 'Tous les clients' not in t, t[:300])
            ctx.close()
        pg, ctx = ouvre2(role='commercial')
        check('un Commercial voit la liste mais ne peut rien cocher', pg.locator('#plv [data-pl]').first.is_disabled() and pg.locator('#plv-ok').count() == 0)
        ctx.close()

        # ---- 3. Cote : les commandes reçues ----
        X = {'pricelist-commandes-v1': CMD, 'pricelist-demandes-v1': DEM, 'pricelist-visites-v1': VIS}
        pg, ctx = ouvre('quotes.html', X=X)
        t = pg.inner_text('#plc')
        check('LE POINT — la Cote montre les commandes reçues de la price list, avec le nombre en attente', 'Commandes reçues de la price list' in t and 'PL-1001' in t and 'PL-1002' in t and pg.locator('#plc .plc-n').inner_text() == '2', t[:600])
        check('la section passe avant les cotes de l\'ERP', pg.evaluate("()=>!!(document.getElementById('plc').compareDocumentPosition(document.getElementById('docs'))&Node.DOCUMENT_POSITION_FOLLOWING)"))
        check('la Cote dit combien de clients ont accès, avec le lien vers l\'onglet de Clients', pg.locator('#plc a[href="clients.html#pricelist"]').count() == 1)
        check('les demandes d\'emails non autorisés sont montrées', 'inconnu@exemple.com' in pg.evaluate("()=>document.querySelector('.plc-dem').textContent"))
        j = pg.inner_text('#plc .plc-j')
        check('LE POINT (journal) — aujourd\'hui, client par client : combien de fois il a ouvert la price list', 'Journal des connexions' in j and '3 ouverture(s)' in j and 'Grossiste Uno' in j and '3 fois' in j, j[:500])
        pg.locator('#plc .plc-j summary').click(); pg.wait_for_timeout(100)
        j = pg.inner_text('#plc .plc-j')
        check('le journal complet : code faux, email non autorisé, commande, appareil', 'Code faux' in j and 'Email non autorisé' in j and 'PL-1002' in j and 'téléphone' in j, j[:900])
        pg.locator('#plc tr.qr[data-plc="PL-1001"]').click(); pg.wait_for_timeout(200)
        t = pg.inner_text('#plc')
        check('le détail d\'une commande : parfums, quantités, prix, note du client', 'Livraison mardi' in t and 'Archiver sans cote' in t, t[:800])
        pg.locator('#plc tr.qd [data-plca="cote"]').click(); pg.wait_for_timeout(2500)
        S = LS(pg, 'pricelist-suivi-v1') or {}
        check('LE POINT — « Faire la cote » marque la commande (cote faite, par qui)', S.get('PL-1001', {}).get('etat') == 'cote' and S['PL-1001'].get('par') == 'Sam', S)
        pan = pg.evaluate("()=>PANIER.map(l=>[l.cle,l.q,l.p])")
        check('LE POINT — la cote est prête : les parfums, les quantités et les prix de la commande', sorted(pan) == sorted([[A[15], 3, A[8]], [B[15], 1, B[8]]]), pan)
        check('le client et le canal Gros sont posés', pg.input_value('#v-client') == 'Grossiste Uno' and pg.input_value('#v-canal') == 'Gros', [pg.input_value('#v-client'), pg.input_value('#v-canal')])
        check('le message dit d\'où vient la cote', 'commande PL-1001 reçue de la price list' in pg.inner_text('#v-msg'), pg.inner_text('#v-msg'))
        check('la commande n\'est plus « en attente » (pastille à 1)', pg.locator('#plc .plc-n').inner_text() == '1', pg.inner_text('#plc')[:300])
        pg.locator('#plc tr.qr[data-plc="PL-1002"]').click(); pg.wait_for_timeout(200)
        pg.once('dialog', lambda d: d.accept())
        pg.locator('#plc tr.qd [data-plca="arch"]').click(); pg.wait_for_timeout(300)
        S = LS(pg, 'pricelist-suivi-v1') or {}
        check('« Archiver sans cote » range la commande', S.get('PL-1002', {}).get('etat') == 'archive', S)
        J = LS(pg, 'crm-journal-v1') or []
        check('les deux gestes sont signés au Journal', sum(1 for x in J if 'de la price list' in (x.get('lib') or '')) >= 2, [x.get('lib') for x in J[-3:]])
        ctx.close()
        for lg, mot in (('en', 'Orders received from the price list'), ('es', 'Pedidos recibidos de la lista de precios')):
            pg, ctx = ouvre('quotes.html', lg=lg, X=X)
            t = pg.inner_text('#plc')
            check(f'la section est traduite ({lg})', mot in t and 'Commandes reçues' not in t and 'Faire la cote' not in t and 'voir et gérer' not in t, t[:400])
            check(f'le journal est traduit ({lg})', ('Sign-in log' if lg == 'en' else 'Registro de conexiones') in t and 'Journal des connexions' not in t, t[-400:])
            ctx.close()
        check('aucune erreur JS', not err, err[:5])
        b.close()
finally:
    srv.terminate()
print(f'{ok} ok, {len(ko)} KO')
raise SystemExit(1 if ko else 0)
