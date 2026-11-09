# LES NOUVEAUX ARRIVAGES AUX CLIENTS FAVORIS (Igal, 8 nov. 2026 : « à chaque new order, une fenêtre s'ouvre : est-ce que vous
# voulez l'envoyer à vos clients favoris ? » ; « un petit message : veuillez trouver ci-joint nos new arrivals — en anglais,
# en français, en espagnol — depuis le WhatsApp de son ordinateur »). Ce test protège :
#   1. à l'enregistrement d'une réception, la proposition (N parfums, K favoris joignables) ; « Plus tard » n'ouvre rien ;
#   2. « Préparer l'envoi » ouvre le Catalogue en cadre (#arrivage=<id>&cadre=1) : les parfums de la réception (photos), les
#      favoris AVEC numéro (doublons de nom réunis, désinscrits et non-favoris exclus, sans numéro listés à part), leur langue ;
#   3. le PDF est fabriqué d'avance dans chaque langue des favoris et déposé au cockpit (type « arrivage ») : un vrai PDF ;
#   4. les clients se cochent (aucun au départ, « Tout cocher » / « Tout décocher ») ; « Envoyer par WhatsApp » ouvre l'APPLICATION WhatsApp (whatsapp://send) avec le message dans la langue du client et le lien du PDF ;
#      « WhatsApp Web » ouvre web.whatsapp.com ; l'envoi est noté (envoyé ✓, journal) ;
#   5. décocher un parfum refait le PDF (même lien) ; « ajouter aussi » la réception du même jour ajoute ses parfums ;
#   6. « Fermer » referme le cadre ; le détail d'une réception a son bouton « Envoyer aux clients favoris » ;
#   7. le message se change dans Réglages › Ma société (par langue ; {prenom}, {lien} ; « Remettre les messages d'origine ») ;
#   8. en anglais et en espagnol, la proposition, la fenêtre et la section des Réglages sont traduites.
import pathlib, subprocess, time, socket, json, base64, io, re, urllib.parse
from playwright.sync_api import sync_playwright
from PIL import Image
D = pathlib.Path('/home/claude/catalogue')
ok = 0; ko = []
def check(n, c, i=''):
    global ok
    if c: ok += 1; print('  ok  ', n)
    else: ko.append(n); print('  KO  ', n, str(i)[:600])
s = socket.socket(); s.bind(('127.0.0.1', 0)); port = s.getsockname()[1]; s.close()
srv = subprocess.Popen(['python3', '-m', 'http.server', str(port), '--bind', '127.0.0.1'], cwd=str(D), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1)
CAT = json.load(open(D / 'cat.json'))
A = [r for r in CAT if r[0] and str(r[0]).isdigit() and len(str(r[0])) >= 12 and (D / 'photos' / (str(r[0]) + '.webp')).exists() and r[7] and r[2] and r[15]][:7]
P1, P2 = A[:5], A[5:7]
ligne = lambda r, q: f"{r[0]}  {r[2]} {r[1]} {r[3]}  {q}  {round(float(r[7]) * 0.6, 2)}"
im = Image.new('RGB', (300, 110), (255, 255, 255)); o = io.BytesIO(); im.save(o, 'PNG'); LOGO = 'data:image/png;base64,' + base64.b64encode(o.getvalue()).decode()
FACT = {'enseigne': 'Perfumes Trade', 'raison': 'DASY LLC', 'tel': '+1 (786) 483-7758', 'email': 'perfumestradellc@gmail.com', 'adresse': '1881 NW 20th street Miami, FL 33142, USA', 'logo': LOGO}
CLIENTS = {
    'Carmen': {'nom': 'Carmen', 'vip': True, 'tel': '(786) 555-0101', 'langue': 'es'},
    'Robert': {'nom': 'Robert', 'vip': True, 'langue': 'en'}, 'ROBERT': {'nom': 'ROBERT', 'tel': '305 555 0102'},   # le numéro est sur le doublon
    'Miky Chevalier': {'nom': 'Miky Chevalier', 'vip': True, 'tel': '+33 6 12 34 56 78', 'langue': 'fr', 'prenom': 'Miky'},
    'Javier': {'nom': 'Javier', 'vip': True},                                                                         # favori sans numéro
    'Desinscrit': {'nom': 'Desinscrit', 'vip': True, 'tel': '7865550199', 'nodiff': True},
    'Pas favori': {'nom': 'Pas favori', 'tel': '7865550100'}}
DOCS = []
try:
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1400, 'height': 1000}); err = []
        pg.on('pageerror', lambda e: err.append(str(e)))
        pg.on('dialog', lambda d: d.accept())
        pg.add_init_script("document.addEventListener('DOMContentLoaded',()=>{const s=document.createElement('style');s.textContent='#svtem{display:none!important}';document.head.appendChild(s)})")
        def cockpit(route):
            u = route.request.url
            m = re.search(r'/docs/([^/?]+)(/image)?(\?[^#]*)?$', u)
            if m and route.request.method == 'PUT':
                if not m.group(2):
                    DOCS.append({'num': m.group(1), 'q': dict(urllib.parse.parse_qsl((m.group(3) or '?')[1:])), 'pdf': route.request.post_data_buffer})
                route.fulfill(status=200, content_type='application/json', body=json.dumps({'ok': True, 'url': 'https://ck.test/d/dasy/jeton' + m.group(1), 'pdf': 'https://ck.test/d/dasy/jeton' + m.group(1) + '.pdf'})); return
            if '/donnees/' in u: route.fulfill(status=404, content_type='application/json', body='{}'); return
            route.fulfill(status=200, content_type='application/json', body=json.dumps({'ok': True}))
        pg.route('**/api/o/dasy/**', cockpit)
        pg.route('https://web.whatsapp.com/**', lambda r: r.fulfill(status=200, content_type='text/html', body='<p>wa</p>'))
        base = f'http://127.0.0.1:{port}/'
        def prepare(lang='fr', factures=None):
            pg.goto(base + 'accueil.html'); pg.wait_for_timeout(300)
            pg.evaluate("""([l,cli,fact,fs])=>{ localStorage.clear(); localStorage.setItem('sam-comptes-demo-v1','0');
                localStorage.setItem('sam-comptes-v1',JSON.stringify([{ident:'sam',nom:'Sam',role:'patron',actif:true,h:'x'}]));
                localStorage.setItem('sam-session-v1',JSON.stringify({id:'sam',nom:'Sam',role:'patron',depuis:new Date().toISOString()}));
                localStorage.setItem('ck-token','jeton-test'); localStorage.setItem('langue-v1',l);
                localStorage.setItem('clients-v1',JSON.stringify(cli));
                localStorage.setItem('reglages-v1',JSON.stringify({societe:'DASY LLC',fact}));
                if(fs) localStorage.setItem('factures-v1',JSON.stringify(fs)); }""", [lang, CLIENTS, FACT, factures])
        def facture(num, L):
            pg.goto(base + 'factures.html'); pg.wait_for_timeout(2500)
            pg.click('#basc'); pg.fill('#colle', '\n'.join(L) + '\n'); pg.wait_for_timeout(900)
            pg.fill('#tiers', 'Miami Trading Zone'); pg.fill('#num', num); pg.fill('#date', '2026-11-02'); pg.wait_for_timeout(700)
            pg.click('#ok'); pg.wait_for_timeout(2200)
        def cadre():
            return next((f for f in pg.frames if 'catalogue.html#arrivage=' in f.url), None)
        def attend(fr, js, ms=40000):
            t = time.time()
            while time.time() - t < ms / 1000:
                try:
                    if fr.evaluate(js): return True
                except Exception: pass
                fr.wait_for_timeout(400)
            return False

        print('1. à l\'enregistrement : la proposition')
        prepare()
        facture('MPS-2', [ligne(r, 6) for r in P2 + [P1[1]]])   # P1[1] revient aussi dans MPS-1 : un doublon
        check('LE POINT — une réception enregistrée propose l\'envoi : 3 parfums, 3 clients favoris joignables', pg.locator('#arr-propose').count() == 1 and '3 parfums reçus' in pg.inner_text('#arr-propose') and '3 clients favoris' in pg.inner_text('#arr-propose'), pg.inner_text('body')[:300] if not pg.locator('#arr-propose').count() else pg.inner_text('#arr-propose'))
        pg.click('#arrp-non'); pg.wait_for_timeout(400)
        check('« Plus tard » : rien ne s\'ouvre, rien n\'est déposé', pg.locator('#fv-ov').count() == 0 and not DOCS)
        facture('MPS-1', [ligne(r, 12) for r in P1])
        check('la réception suivante propose à son tour (5 parfums)', pg.locator('#arr-propose').count() == 1 and '5 parfums reçus' in pg.inner_text('#arr-propose'))
        FS = pg.evaluate("()=>JSON.parse(localStorage.getItem('factures-v1')||'[]')")
        fid = next(f['id'] for f in FS if f.get('num') == 'MPS-1')

        print('2. la fenêtre d\'envoi (Catalogue en cadre)')
        pg.click('#arrp-oui'); pg.wait_for_timeout(800)
        src = pg.evaluate("()=>(document.querySelector('#fv-ov iframe')||{}).src||''")
        check('LE POINT — « Préparer l\'envoi » ouvre catalogue.html#arrivage=<réception>&cadre=1', ('catalogue.html#arrivage=' + fid) in src and 'cadre=1' in src, src)
        pg.wait_for_timeout(3500); fr = cadre()
        check('le cadre est le Catalogue', fr is not None)
        attend(fr, "()=>window.__ARR&&window.__ARR.get()&&window.__ARR.get().items.length&&window.__ARR.get().items.every(x=>x.photo!==undefined)", 30000)
        S = fr.evaluate("()=>{ const A=window.__ARR.get(); return {items:A.items.map(x=>String(x.bc)), choix:A.choix.size, photos:A.items.filter(x=>x.photo).length, dest:A.dest.map(d=>[d.nom,d.tel,d.lg,d.prenom]), autres:A.memeJour.map(f=>f.num), vis:getComputedStyle(document.getElementById('arrov')).visibility}; }")
        check('LE POINT — les 5 parfums de la réception, tous cochés, avec leur photo', sorted(S['items']) == sorted(str(r[0]) for r in P1) and S['choix'] == 5 and S['photos'] == 5, S)
        dest = {d[0]: d for d in S['dest']}
        check('LE POINT — les favoris : Carmen (es), Miky (fr), Robert (en, numéro pris sur son doublon « ROBERT »), Javier sans numéro ; ni le désinscrit ni le non-favori',
              set(dest) == {'Carmen', 'Miky Chevalier', 'Robert', 'Javier'} and dest['Carmen'][1:3] == ['17865550101', 'es'] and dest['Miky Chevalier'][1:4] == ['33612345678', 'fr', 'Miky'] and dest['Robert'][1:3] == ['13055550102', 'en'] and dest['Javier'][1] == '', S['dest'])
        check('la réception du même jour (MPS-2) est proposée en « ajouter aussi »', S['autres'] == ['MPS-2'], S['autres'])
        t = fr.inner_text('#arrov')
        check('la fenêtre se voit en mode cadre, et liste Javier comme « sans numéro »', S['vis'] == 'visible' and 'Favoris sans numéro' in t and 'Javier' in t, (S['vis'], t[-300:]))

        print('3. les clients se cochent (aucun au départ) ; le PDF est prêt d\'avance dans leurs langues')
        S = fr.evaluate("()=>({sel:window.__ARR.get().sel.size, dis:document.getElementById('arr-envoi').disabled, lib:document.getElementById('arr-envoi').innerText})")
        check('LE POINT — au départ aucun client n\'est coché : le bouton dit « Coche au moins un client », éteint, et aucun PDF n\'est fabriqué', S['sel'] == 0 and S['dis'] and 'Coche au moins un client' in S['lib'] and not DOCS, (S, len(DOCS)))
        fr.click('#arr-ctous'); fr.wait_for_timeout(300)
        S = fr.evaluate("()=>({sel:window.__ARR.get().sel.size, lib:document.getElementById('arr-envoi').innerText})")
        check('LE POINT — « Tout cocher » : les 3 clients joignables cochés, « Envoyer par WhatsApp (3 clients) »', S['sel'] == 3 and 'Envoyer par WhatsApp (3 clients)' in S['lib'], S)
        attend(fr, "()=>{ const e=window.__ARR.get().etat; return e.es==='ok'&&e.fr==='ok'&&e.en==='ok'; }", 60000)
        par = {d['q'].get('langue'): d for d in DOCS}
        check('LE POINT — trois PDF déposés (es, fr, en), type « arrivage », 5 parfums, un vrai PDF d\'une page', set(par) == {'es', 'fr', 'en'} and all(d['q'].get('type') == 'arrivage' and d['q'].get('lignes') == '5' and d['pdf'][:5] == b'%PDF-' for d in par.values())
              and len(re.findall(rb'/Type\s*/Page[^s]', par['en']['pdf'])) == 1, [(d['num'], d['q'], len(d['pdf'] or b'')) for d in DOCS])
        check('les numéros des PDF : ARR-<réception>-<LANGUE>', par.get('es', {}).get('num') == 'ARR-MPS1-ES' and par.get('fr', {}).get('num') == 'ARR-MPS1-FR', [d['num'] for d in DOCS])
        (D / '_apercu_arrivage.pdf').write_bytes(par['fr']['pdf'])
        fr.click('#arr-caucun'); fr.wait_for_timeout(300)
        check('« Tout décocher » : plus personne, le bouton s\'éteint', fr.evaluate("()=>window.__ARR.get().sel.size") == 0 and fr.evaluate("()=>document.getElementById('arr-envoi').disabled"))

        print('4. un seul client, puis tous à la suite')
        fr.check('.arr-d:has-text("Carmen") input[data-arrsel]'); fr.wait_for_timeout(300)
        check('Carmen seule cochée : « Envoyer par WhatsApp (1 client) »', 'Envoyer par WhatsApp (1 client)' in fr.inner_text('#arr-envoi'), fr.inner_text('#arr-envoi'))
        fr.click('#arr-envoi'); fr.wait_for_timeout(500)
        u = fr.evaluate("()=>window.__arrDernier||''"); txt = urllib.parse.unquote(u.split('&text=')[-1]) if '&text=' in u else ''
        check('LE POINT — Carmen seule : WhatsApp Web (le seul chemin) sur son numéro, message en espagnol avec le lien du PDF espagnol',
              u.startswith('https://web.whatsapp.com/send?phone=17865550101&text=') and txt.startswith('Hola Carmen') and 'nuevos arribos' in txt and 'https://ck.test/d/dasy/jetonARR-MPS1-ES' in txt and 'Precios a solicitud' in txt, (u[:80], txt))
        E = fr.evaluate("()=>lit('arrivages-envoyes-v1',{})")
        J = fr.evaluate("()=>lit('crm-journal-v1',[]).map(j=>j.lib)")
        check('l\'envoi est noté (réception, Journal) ; le bouton dit « C\'est fait : 1 envoyé »', 'Carmen' in ((E.get(fid) or {}).get('a') or {}) and any('nouveaux arrivages envoyés à Carmen' in j for j in J) and "C'est fait : 1 envoyé" in fr.inner_text('#arr-envoi'), (E, J[-1:], fr.inner_text('#arr-envoi')))
        fr.click('#arr-caucun'); fr.wait_for_timeout(200)
        check('plus de choix « application / WhatsApp Web » (une seule façon, Igal 9 nov.)', fr.locator('input[name=arrwa]').count() == 0 and 'Ouvrir avec' not in fr.inner_text('#arrov'))
        fr.click('#arr-ctous'); fr.wait_for_timeout(300)
        vus = []
        for k in range(3):
            fr.click('#arr-envoi'); fr.wait_for_timeout(600)
            vus.append((fr.evaluate("()=>window.__arrDernier||''"), fr.inner_text('#arr-envoi')))
        noms = [urllib.parse.unquote(v[0].split('&text=')[-1]).split(',')[0] for v in vus]
        check('LE POINT — « Tout cocher » puis un clic par client : Carmen, Miky, Robert, chacun dans sa langue, « Client suivant : … (2/3) », puis « C\'est fait : 3 envoyés »',
              noms == ['Hola Carmen', 'Bonjour Miky', 'Hello Robert'] and 'Client suivant : Miky Chevalier (2/3)' in vus[0][1] and 'Client suivant : Robert (3/3)' in vus[1][1] and "C'est fait : 3 envoyés" in vus[2][1], (noms, [v[1] for v in vus]))
        u = vus[1][0]; txt = urllib.parse.unquote(u.split('&text=')[-1])
        check('LE POINT — web.whatsapp.com, Miky en français (« veuillez trouver ci-joint nos nouveaux arrivages »)',
              u.startswith('https://web.whatsapp.com/send?phone=33612345678&text=') and 'Veuillez trouver ci-joint nos nouveaux arrivages' in txt and 'jetonARR-MPS1-FR' in txt, (u[:80], txt))

        print('5. décocher un parfum, ajouter la réception du même jour')
        n0 = len(DOCS)
        fr.uncheck(f'[data-arrp="{P1[0][15]}"]'); fr.wait_for_timeout(300)
        attend(fr, "()=>{ const e=window.__ARR.get().etat; return e.es==='ok'&&e.fr==='ok'&&e.en==='ok'; }", 60000)
        nouv = DOCS[n0:]
        check('LE POINT — un parfum décoché : les PDF sont refaits avec 4 parfums, sous les mêmes numéros (le lien ne change pas)', len(nouv) == 3 and all(d['q'].get('lignes') == '4' for d in nouv) and {d['num'] for d in nouv} == {'ARR-MPS1-ES', 'ARR-MPS1-FR', 'ARR-MPS1-EN'}, [(d['num'], d['q'].get('lignes')) for d in nouv])
        fr.check('[data-arrf]'); attend(fr, "()=>window.__ARR.get().items.length===7&&window.__ARR.get().items.every(x=>x.photo!==undefined)", 30000)
        S = fr.evaluate("()=>{ const A=window.__ARR.get(); return {n:A.items.length, choix:A.choix.size}; }")
        check('LE POINT — « ajouter aussi MPS-2 » : 7 parfums et pas 8 (le parfum présent dans les deux réceptions n\'apparaît qu\'une fois), les 2 nouveaux cochés, le décoché reste décoché', S == {'n': 7, 'choix': 6}, S)
        check('la date de la réception est un jour (« 2 novembre 2026 »), sans heure ni décalage de fuseau', '2 novembre 2026' in fr.inner_text('.arr-sous') and ':' not in fr.inner_text('.arr-sous'), fr.inner_text('.arr-sous'))

        print('6. fermer ; le bouton du détail')
        fr.click('#arr-ferme'); pg.wait_for_timeout(600)
        check('« Fermer » referme le cadre', pg.locator('#fv-ov').count() == 0)
        pg.locator(f'#liste tr[data-d="{fid}"]').click(); pg.wait_for_timeout(700)
        check('LE POINT — le détail de la réception a « Envoyer aux clients favoris »', pg.locator('#d-arr').count() == 1 and pg.inner_text('#d-arr') == 'Envoyer aux clients favoris')
        pg.click('#d-arr'); pg.wait_for_timeout(800)
        check('… qui rouvre la fenêtre d\'envoi', ('#arrivage=' + fid) in pg.evaluate("()=>(document.querySelector('#fv-ov iframe')||{}).src||''"))

        print('6b. le message se change dans Réglages')
        pg.goto(base + 'reglages.html'); pg.wait_for_timeout(2500)
        pg.evaluate("()=>{ const b=[...document.querySelectorAll('#ong button')].find(x=>x.dataset.t==='soc'); if(b) b.click(); }")
        orig = pg.input_value('#am-fr')
        check('Réglages › Ma société : les trois messages, celui d\'origine affiché', 'Veuillez trouver ci-joint nos nouveaux arrivages' in orig and '{prenom}' in orig and '{lien}' in orig and pg.locator('#am-en').count() == 1 and pg.locator('#am-es').count() == 1, orig)
        pg.fill('#am-fr', 'Salut {prenom} ! Voici la sélection de la semaine.'); pg.dispatch_event('#am-fr', 'change'); pg.wait_for_timeout(3000)
        R = pg.evaluate("()=>JSON.parse(localStorage.getItem('reglages-v1')).arrMsg")
        J = pg.evaluate("()=>lit('crm-journal-v1',[]).map(j=>j.lib)")
        check('LE POINT — le message français changé est enregistré (et noté au Journal)', R == {'fr': 'Salut {prenom} ! Voici la sélection de la semaine.'} and any('message des nouveaux arrivages' in j for j in J), (R, J[-1:]))
        pg.goto(base + 'factures.html'); pg.wait_for_timeout(2500)
        pg.locator(f'#liste tr[data-d="{fid}"]').click(); pg.wait_for_timeout(700); pg.click('#d-arr'); pg.wait_for_timeout(3500); fr = cadre()
        attend(fr, "()=>window.__ARR&&window.__ARR.get()&&window.__ARR.get().items.length>0", 20000)
        fr.check('.arr-d:has-text("Miky Chevalier") input[data-arrsel]'); fr.wait_for_timeout(300)
        attend(fr, "()=>window.__ARR.get().etat.fr==='ok'", 60000)
        fr.click('#arr-envoi'); fr.wait_for_timeout(600)
        txt = urllib.parse.unquote(fr.evaluate("()=>window.__arrDernier||''").split('&text=')[-1])
        check('LE POINT — l\'envoi prend le message des Réglages : « Salut Miky ! … » et le lien ajouté à la fin (il manquait {lien})', txt.startswith('Salut Miky ! Voici la sélection de la semaine.') and txt.rstrip().endswith('jetonARR-MPS1-FR'), txt)
        pg.goto(base + 'reglages.html'); pg.wait_for_timeout(2500); pg.click('#am-defaut'); pg.wait_for_timeout(300)
        check('« Remettre les messages d\'origine »', pg.evaluate("()=>JSON.parse(localStorage.getItem('reglages-v1')).arrMsg") == {} and 'Veuillez trouver ci-joint' in pg.input_value('#am-fr'))

        print('7. en anglais et en espagnol')
        for lang, mots_p, mots in (('en', ['New arrival: send it to your favourite customers?', 'Prepare the sending', 'Later'], ['Send the new arrivals', 'Perfumes on the list', 'Favourite customers', 'See the PDF', 'Tick all', 'Untick all', 'Tick at least one customer', 'also add', 'Favourites without a number', 'Close']),
                                   ('es', ['Nuevo arribo: ¿enviarlo a sus clientes favoritos?', 'Preparar el envío', 'Más tarde'], ['Enviar los nuevos arribos', 'Perfumes de la lista', 'Clientes favoritos', 'Ver el PDF', 'Marcar todo', 'Desmarcar todo', 'Marca al menos un cliente', 'añadir también', 'Favoritos sin número', 'Cerrar'])):
            prepare(lang, FS)
            pg.goto(base + 'factures.html'); pg.wait_for_timeout(2500)
            pg.evaluate(f"()=>proposeArrivage({json.dumps(fid)})"); pg.wait_for_timeout(400)
            tp = pg.inner_text('#arr-propose') if pg.locator('#arr-propose').count() else ''
            check(f'en {lang} : la proposition est traduite', all(m in tp for m in mots_p) and 'Plus tard' not in tp, tp)
            pg.click('#arrp-oui'); pg.wait_for_timeout(3500); fr = cadre()
            attend(fr, "()=>window.__ARR&&window.__ARR.get()&&window.__ARR.get().items.length>0", 20000)
            t = fr.inner_text('#arrov')
            check(f'en {lang} : la fenêtre est traduite, aucun mot français', all(m in t for m in mots) and not any(f in t for f in ['Parfums de la liste', 'Clients favoris', 'Ouvrir avec', 'Voir le PDF', 'Fermer', 'sans numéro', 'Tout décocher', 'Coche au moins']), [m for m in mots if m not in t] or t[:300])
            pg.goto(base + 'reglages.html'); pg.wait_for_timeout(2500)
            tr = pg.inner_text('#sec-arrivages') if pg.locator('#sec-arrivages').count() else ''
            attendu = {'en': ['WhatsApp message for new arrivals', 'Message in English', 'Message in French', 'Message in Spanish', 'Restore the original messages'],
                       'es': ['Mensaje de WhatsApp de los nuevos arribos', 'Mensaje en inglés', 'Mensaje en francés', 'Mensaje en español', 'Restablecer los mensajes originales']}[lang]
            check(f'en {lang} : Réglages › le message des nouveaux arrivages est traduit (le titre est en capitales à l\'écran)', all(m.lower() in tr.lower() for m in attendu) and 'Message en anglais' not in tr and 'Remettre' not in tr, [m for m in attendu if m.lower() not in tr.lower()] or tr[:300])
        check('aucune erreur JS', not err, err[:3])
        b.close()
finally:
    srv.terminate()
print(f'\n{ok} ok, {len(ko)} KO', ko); raise SystemExit(1 if ko else 0)
