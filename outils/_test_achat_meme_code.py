# UN CODE-BARRES PORTÉ PAR PLUSIEURS PARFUMS, DANS UNE NEW ORDER (Igal, 11 nov. 2026 : « Sam vient de rentrer une new order ; il a un
# code-barres qui est sur trois parfums identiques, un no box, un gift et un autre ; l'ERP a choisi le mauvais parfum — est-ce que tu
# pourrais lui laisser la possibilité de choisir lequel il veut »). Avant : l'ERP prenait une des trois fiches sans rien dire.
# Ce test protège :
#   1. LE POINT — l'ERP ne choisit plus tout seul : la ligne attend, et propose les fiches qui portent ce code (nom complet, taille, stock) ;
#   2. LE POINT — le parfum choisi par Sam reçoit le stock, les autres fiches au même code ne bougent pas ;
#   3. le choix se change tant que la facture n'est pas enregistrée ;
#   4. un code-barres porté par une seule fiche se comporte comme avant (aucune liste) ;
#   5. la question est écrite en français, en anglais et en espagnol.
import pathlib, subprocess, time, socket, json
from playwright.sync_api import sync_playwright
D = pathlib.Path('/home/claude/catalogue')
ok = 0; ko = []
def check(n, c, i=''):
    global ok
    if c: ok += 1; print('  ok  ', n)
    else: ko.append(n); print('  KO  ', n, str(i)[:400])
s = socket.socket(); s.bind(('127.0.0.1', 0)); port = s.getsockname()[1]; s.close()
srv = subprocess.Popen(['python3', '-m', 'http.server', str(port), '--bind', '127.0.0.1'], cwd=str(D), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)
CAT = json.load(open(D / 'cat.json'))
LIG = [r for r in CAT if r[0] and len(r[0]) >= 12 and (r[6] or 0) > 0 and r[7]]
A, B = LIG[0], LIG[3]
def prepare(pg, base, lg):
    pg.goto(base + 'accueil.html'); pg.wait_for_timeout(300)
    pg.evaluate("""([A,B,lg])=>{ localStorage.clear(); localStorage.setItem('sam-comptes-demo-v1','0');
        localStorage.setItem('sam-comptes-v1',JSON.stringify([{ident:'u',nom:'Sam',role:'patron',actif:true,h:'x'}]));
        localStorage.setItem('sam-session-v1',JSON.stringify({id:'u',nom:'Sam',role:'patron',depuis:new Date().toISOString()}));
        localStorage.setItem('langue-v1',lg);
        localStorage.setItem('fiches-modifiees-v1',JSON.stringify({[A[15]]:{qte:10,pa:20},[B[15]]:{qte:4,pa:20}}));
        /* deux autres fiches portent le MÊME code-barres que le premier parfum : sa version sans boîte et son coffret */
        localStorage.setItem('articles-ajoutes-v1',JSON.stringify([
          {id:'zzsansboite',bc:A[0],nom:A[1]+' no box',marque:A[2],ml:'3.4',type:'EDP',genre:'U',qte:3,pa:18,pvr:null,pvw:null},
          {id:'zzcoffret',bc:A[0],nom:A[1]+' gift set',marque:A[2],ml:'3.4',type:'SET',genre:'U',qte:4,pa:25,pvr:null,pvw:null}])); }""", [A, B, lg])
    pg.goto(base + 'factures.html'); pg.wait_for_timeout(2500)
    pg.click('#basc')
    pg.fill('#colle', f"{A[2]} {A[1]}  {A[0]}  6  20.00\n{B[2]} {B[1]}  {B[0]}  5  20.00\n"); pg.wait_for_timeout(800)
    pg.fill('#tiers', 'Fournisseur US'); pg.fill('#num', 'MEME-1'); pg.wait_for_timeout(600)
try:
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1700, 'height': 1100}); err = []
        pg.on('pageerror', lambda e: err.append(str(e))); pg.on('dialog', lambda d: d.accept())
        base = f'http://127.0.0.1:{port}/'
        prepare(pg, base, 'fr')
        lig = lambda: pg.evaluate("()=>window.__F.APERCU.L.map(x=>({bc:x.bc,cle:x.cle||null,aChoisir:!!x.aChoisir,freres:(x.freres||[]).length,qAv:x.qAv,qAp:x.qAp}))")
        mod = lambda c: pg.evaluate("c=>JSON.parse(localStorage.getItem('fiches-modifiees-v1')||'{}')[c]||{}", c)
        print('1. la ligne attend le choix')
        L = lig(); la = [x for x in L if x['bc'] == A[0]][0]; lb = [x for x in L if x['bc'] == B[0]][0]
        check('LE POINT — l\'ERP ne choisit plus tout seul : la ligne au code partagé n\'a pas de parfum', la['cle'] is None and la['aChoisir'] and la['freres'] == 3, la)
        opts = pg.evaluate("()=>[...document.querySelectorAll('select[data-frere] option')].map(o=>o.textContent)")
        check('LE POINT — la liste propose les trois fiches, avec ce qui les distingue (no box, gift set) et leur stock', len(opts) == 4 and any('no box' in o and '3' in o for o in opts) and any('gift set' in o for o in opts), opts)
        check('la question est écrite en clair', 'Ce code-barres est sur 3 parfums' in pg.inner_text('#apercu'), pg.inner_text('#apercu')[:300])
        check('la ligne compte parmi celles « à reconnaître »', pg.evaluate("()=>window.__F.APERCU.inconnues") == 1)
        check('un code-barres porté par UNE seule fiche se comporte comme avant : reconnu, aucune liste', lb['cle'] == B[15] and lb['freres'] == 0 and lb['qAv'] == 4 and lb['qAp'] == 9, lb)
        print('2. Sam choisit')
        pg.select_option('select[data-frere]', 'zzsansboite'); pg.wait_for_timeout(500)
        la = [x for x in lig() if x['bc'] == A[0]][0]
        check('LE POINT — la ligne prend le parfum choisi (la version sans boîte : 3 → 9)', la['cle'] == 'zzsansboite' and la['qAv'] == 3 and la['qAp'] == 9, la)
        check('plus aucune ligne à reconnaître', pg.evaluate("()=>window.__F.APERCU.inconnues") == 0)
        check('le choix reste visible sur la ligne, et la liste est toujours là pour le changer', pg.locator('select[data-frere]').count() == 1 and 'choisi' in pg.inner_text('#apercu'))
        pg.select_option('select[data-frere]', 'zzcoffret'); pg.wait_for_timeout(500)
        la = [x for x in lig() if x['bc'] == A[0]][0]
        check('le choix se change avant l\'enregistrement (le coffret : 4 → 10)', la['cle'] == 'zzcoffret' and la['qAv'] == 4 and la['qAp'] == 10, la)
        print('3. l\'enregistrement')
        pg.click('#ok'); pg.wait_for_timeout(1500)
        check('LE POINT — le parfum choisi reçoit le stock : 4 + 6 = 10', mod('zzcoffret').get('qte') == 10, mod('zzcoffret'))
        check('LE POINT — les deux autres fiches au même code-barres ne bougent pas', mod(A[15]).get('qte') == 10 and mod('zzsansboite').get('qte') in (None, 3), (mod(A[15]), mod('zzsansboite')))
        f = pg.evaluate("()=>JSON.parse(localStorage.getItem('factures-v1')||'[]').find(f=>f.num==='MEME-1')")
        check('la facture garde la ligne sur le parfum choisi', f and any(l.get('cle') == 'zzcoffret' and l.get('q') == 6 for l in f['lignes']), f and f['lignes'])
        check('l\'autre parfum de la facture : 4 + 5 = 9', mod(B[15]).get('qte') == 9, mod(B[15]))
        print('4. les trois langues')
        for lg, txt, plh in (('en', 'This barcode is on 3 perfumes', 'choose the perfume'), ('es', 'Este código de barras está en 3 perfumes', 'elegir el perfume')):
            prepare(pg, base, lg)
            t = pg.inner_text('#apercu'); o = pg.evaluate("()=>[...document.querySelectorAll('select[data-frere] option')].map(o=>o.textContent)")
            check(f'{lg} : la question et la liste sont traduites', txt in t and plh in (o[0] if o else ''), (t[:200], o[:1]))
        check('aucune erreur JS', not err, err)
        b.close()
finally:
    srv.terminate()
print(f'\n{ok} ok, {len(ko)} KO', ko)
raise SystemExit(1 if ko else 0)
