# LES LIGNES SANS PRIX D'ACHAT, DEPUIS LE TABLEAU DE BORD (14 nov. 2026 — Igal : « en cliquant sur les 5 prix manquants, qu'une
# fenêtre latérale s'ouvre, que je puisse mettre le prix d'achat, et qu'il s'enregistre sur la fiche »). Ce test protège :
#   1. LE POINT — la mention « N lignes sans prix d'achat » se clique et ouvre une fenêtre à droite avec ces lignes-là ;
#   2. LE POINT — une fiche sans prix d'achat : le prix saisi va sur la FICHE et sur toutes les ventes de ce parfum qui n'en
#      avaient pas ; la marge revient, la mention passe à N − 1, et c'est signé au Journal ;
#   3. une fiche qui a déjà un prix : la case est pré-remplie, la vente le prend, la fiche ne change pas ;
#   4. une vente sans fiche (parfum non reconnu) : le prix va sur cette ligne seule, et la fenêtre le dit ;
#   5. un prix vide ou à 0 est refusé ; un remboursement n'est jamais compté ; quand tout est complet, la mention disparaît ;
#   6. sans le droit « Modifie les prix », les lignes se voient mais sans case ; en anglais et en espagnol tout est traduit ;
#   7. aucune erreur JS.
import subprocess, time, socket, json, re, sys, datetime
from playwright.sync_api import sync_playwright
D = '/home/claude/catalogue'
ok = 0; ko = []
def check(n, c, i=''):
    global ok
    if c: ok += 1; print('  ok  ', n)
    else: ko.append(n); print('  KO  ', n, str(i)[:500])
s = socket.socket(); s.bind(('127.0.0.1', 0)); port = s.getsockname()[1]; s.close()
srv = subprocess.Popen(['python3', '-m', 'http.server', str(port), '--bind', '127.0.0.1'], cwd=D, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)
auj = datetime.date(2026, 11, 15)
PREP = """([lg,role])=>{ localStorage.clear(); localStorage.setItem('sam-comptes-demo-v1','0');
  localStorage.setItem('sam-session-v1',JSON.stringify({id:'sam',nom:'Sam',role:role,depuis:new Date().toISOString()})); localStorage.setItem('langue-v1',lg); }"""
VENTES = """()=>{ const K=Object.keys(IDX); const sans=K.find(k=>IDX[k][3]==null&&IDX[k][1]); const avec=K.find(k=>IDX[k][3]!=null&&+IDX[k][3]>0&&k!==sans);
  const L=(cle,q,p,ref)=>({cle,bc:cle?IDX[cle][0]:'',ref:ref||(cle?IDX[cle][1]:''),q,p});
  const F=[{id:'v1',num:'PC-1',sens:'vente',canal:'Perfume City',auto:'shopify-pc',d:'2026-10-05',lignes:[L(sans,2,30)]},
    {id:'v2',num:'PC-2',sens:'vente',canal:'Perfume City',auto:'shopify-pc',d:'2026-10-06',lignes:[L(sans,1,30)]},
    {id:'v3',num:'PC-3',sens:'vente',canal:'Perfume City',auto:'shopify-pc',d:'2026-10-07',lignes:[L(avec,1,90)]},
    {id:'v4',num:'PC-4',sens:'vente',canal:'Perfume City',auto:'shopify-pc',d:'2026-10-08',lignes:[L(avec,1,50,'x'),L('',1,28,'MAITHA PURE OIL 20 ML')]},
    {id:'v5',num:'PC-5',sens:'vente',canal:'Perfume City',auto:'shopify-pc',d:'2026-10-09',retour:true,refNum:'PC-1',lignes:[L(sans,-1,30)]}];
  F[3].lignes[0].paAv=40;
  localStorage.setItem('factures-v1',JSON.stringify(F)); localStorage.setItem('crm-journal-v1','[]'); localStorage.setItem('fiches-modifiees-v1','{}');
  
  return [sans,avec,IDX[avec][3]]; }"""
mention = lambda pg: (pg.inner_text('#recap .rc-sanspa') if pg.locator('#recap .rc-sanspa').count() else '')
try:
    with sync_playwright() as p:
        b = p.chromium.launch(); err = []
        def ouvre(lg='fr', role='patron'):
            ctx = b.new_context(viewport={'width': 1400, 'height': 950}, timezone_id='America/New_York', locale='fr-FR', reduced_motion='reduce')
            pg = ctx.new_page(); pg.on('pageerror', lambda e: err.append(str(e)))
            pg.add_init_script("Object.defineProperty(window,'D_HG',{configurable:true,set(v){ window.__hgReel=v; },get(){ return null; }})")
            pg.clock.set_fixed_time(datetime.datetime(auj.year, auj.month, auj.day, 14, 0, tzinfo=datetime.timezone(datetime.timedelta(hours=-5))))
            base = f'http://127.0.0.1:{port}/'
            pg.goto(base + 'accueil.html'); pg.wait_for_timeout(300); pg.evaluate(PREP, [lg, role])
            pg.goto(base + 'tableau.html'); pg.wait_for_timeout(1500); K = pg.evaluate(VENTES)
            pg.evaluate("()=>{ RC.sel='du:2026-10-01:2026-10-31'; RC.metric='mg'; rcSauve(); }")
            pg.reload(); pg.wait_for_timeout(2500); return pg, K
        pg, K = ouvre(); SANS, AVEC, PA_AVEC = K
        print('1. la mention et la fenêtre')
        check('LE POINT — la mention dit « 4 lignes sans prix d\'achat » (le remboursement ne compte pas) et se clique', '4 lignes sans prix d\'achat' in mention(pg) and pg.locator('#recap .rc-sanspa[role=button]').count() == 1, mention(pg))
        pg.click('#recap .rc-sanspa'); pg.wait_for_timeout(400)
        n0 = pg.locator('#rc-pan .rc-pl').count(); tx = pg.inner_text('#rc-pan')
        check('LE POINT — un clic ouvre la fenêtre à droite, avec les 4 lignes (date, canal, n°, quantité × prix)', pg.locator('#rc-pan').count() == 1 and n0 == 4 and 'PC-1' in tx and 'PC-4' in tx and 'PC-5' not in tx and '2 × 30,00 $' in tx.replace('\xa0', ' ').replace(' ', ' '), [n0, tx[:400]])
        check('la ligne sans fiche est dite telle quelle : « n\'est reliée à aucune fiche », avec le nom vendu', 'MAITHA PURE OIL 20 ML' in tx and 'reliée à aucune fiche' in tx, tx[-500:])
        vals = pg.evaluate("()=>[...document.querySelectorAll('#rc-pan [data-pa]')].map(i=>i.value)")
        check('une fiche qui a déjà un prix d\'achat : la case est pré-remplie avec ce prix ; une fiche sans prix : la case est vide', vals.count(str(PA_AVEC) if '.' in str(PA_AVEC) else str(PA_AVEC)) >= 1 or any(abs(float(v) - float(PA_AVEC)) < 0.001 for v in vals if v), [vals, PA_AVEC])
        i_sans = pg.evaluate("c=>{ const L=rcSansPaLignes(); return L.findIndex(x=>x.cle===c); }", SANS)
        pg.fill(f'#rc-pan [data-pa="{i_sans}"]', '0'); pg.click(f'#rc-pan [data-pok="{i_sans}"]'); pg.wait_for_timeout(200)
        check('un prix à 0 est refusé, rien n\'est écrit', 'plus grand que 0' in pg.inner_text(f'#rc-pan [data-pm="{i_sans}"]') and pg.evaluate("()=>JSON.parse(localStorage.getItem('fiches-modifiees-v1'))") == {}, pg.inner_text('#rc-pan')[:200])
        print('2. une fiche sans prix d\'achat')
        pg.fill(f'#rc-pan [data-pa="{i_sans}"]', '12,5'); pg.click(f'#rc-pan [data-pok="{i_sans}"]'); pg.wait_for_timeout(600)
        st = pg.evaluate("c=>{ const M=JSON.parse(localStorage.getItem('fiches-modifiees-v1')); const F=JSON.parse(localStorage.getItem('factures-v1')); return [M[c]&&M[c].pa, F.filter(f=>f.lignes.some(l=>l.cle===c)).map(f=>[f.num,f.lignes.find(l=>l.cle===c).paAv]), JSON.parse(localStorage.getItem('crm-journal-v1')).filter(j=>j.champ==='pa')]; }", SANS)
        check('LE POINT — le prix (12,50 $) est enregistré sur la FICHE du parfum', st[0] == 12.5, st[0])
        check('LE POINT — … et sur toutes ses ventes qui n\'en avaient pas (PC-1, PC-2, et le remboursement PC-5)', all(x[1] == 12.5 for x in st[1]) and len(st[1]) == 3, st[1])
        check('c\'est signé au Journal : qui (Sam), quoi (prix d\'achat), combien de ventes', len(st[2]) == 1 and st[2][0]['u'] == 'Sam' and st[2][0]['champ'] == 'pa' and st[2][0]['n'] == 3 and 'fiche et ventes' in st[2][0]['lib'], st[2])
        tx = pg.inner_text('#rc-pan')
        check('LE POINT — la fenêtre reste ouverte, dit « ✓ 12,50 $ enregistré sur la fiche et sur 3 ventes », et il ne reste que 2 lignes ; la mention du tableau dit 2', '12,50 $ enregistré sur la fiche et sur 3 ventes' in tx.replace('\xa0', ' ').replace(' ', ' ') and pg.locator('#rc-pan .rc-pl').count() == 2 and '2 lignes sans prix d\'achat' in mention(pg), [tx[:300], mention(pg)])
        print('3. une fiche qui a déjà un prix')
        i_avec = pg.evaluate("c=>rcSansPaLignes().findIndex(x=>x.cle===c)", AVEC)
        pg.click(f'#rc-pan [data-pok="{i_avec}"]'); pg.wait_for_timeout(600)
        st = pg.evaluate("c=>{ const M=JSON.parse(localStorage.getItem('fiches-modifiees-v1')); const F=JSON.parse(localStorage.getItem('factures-v1')); return [M[c]||null, F.find(f=>f.num==='PC-3').lignes[0].paAv, F.find(f=>f.num==='PC-4').lignes[0].paAv]; }", AVEC)
        check('LE POINT — la vente prend le prix de la fiche ; la fiche ne change pas ; une vente qui avait déjà son prix (40 $) le garde', st[0] is None and abs(st[1] - float(PA_AVEC)) < 0.001 and st[2] == 40, st)
        check('… et la fenêtre dit que la fiche garde son prix', 'la fiche garde son prix' in pg.inner_text('#rc-pan'), pg.inner_text('#rc-pan')[:200])
        print('4. une vente sans fiche')
        pg.fill('#rc-pan [data-pa="0"]', '9'); pg.click('#rc-pan [data-pok="0"]'); pg.wait_for_timeout(600)
        st = pg.evaluate("()=>{ const F=JSON.parse(localStorage.getItem('factures-v1')); return [F.find(f=>f.num==='PC-4').lignes[1].paAv, Object.keys(JSON.parse(localStorage.getItem('fiches-modifiees-v1'))).length]; }")
        check('LE POINT — le prix va sur cette ligne seule, aucune fiche n\'est créée ni touchée', st == [9, 1], st)
        tx = pg.inner_text('#rc-pan')
        check('LE POINT — tout est complet : la fenêtre le dit, et la mention disparaît du tableau de bord', 'Tout est complet' in tx and pg.locator('#recap .rc-sanspa').count() == 0, [tx[:200], mention(pg)])
        pg.keyboard.press('Escape'); pg.wait_for_timeout(200)
        check('Échap ferme la fenêtre', pg.locator('#rc-pan').count() == 0)
        pg.context.close()
        print('5. les droits et les langues')
        pg, K = ouvre(role='commercial')
        if pg.locator('#recap .rc-sanspa').count():
            pg.evaluate("()=>rcSansPaOuvre()"); pg.wait_for_timeout(300)
            check('sans le droit « Modifie les prix » : les lignes se voient, sans case à remplir', pg.locator('#rc-pan [data-pa]').count() == 0 and 'Seuls le Patron' in pg.inner_text('#rc-pan'), pg.inner_text('#rc-pan')[:300])
        else:
            pg.evaluate("()=>rcSansPaOuvre()"); pg.wait_for_timeout(300)
            check('sans le droit « Modifie les prix » : aucune case à remplir', pg.locator('#rc-pan [data-pa]').count() == 0, pg.inner_text('#rc-pan')[:300] if pg.locator('#rc-pan').count() else '')
        pg.context.close()
        FR = re.compile(r"\b(ligne|lignes|prix d'achat|Enregistrer|fiche|vente|ventes|Fermer|parfum|seulement)\b")
        for lg, mot, bouton in (('en', 'lines without purchase price', 'Save'), ('es', 'líneas sin precio de compra', 'Guardar')):
            pg, K = ouvre(lg=lg)
            check(f'{lg} — la mention est traduite (« {mot} »)', mot in mention(pg), mention(pg))
            pg.click('#recap .rc-sanspa'); pg.wait_for_timeout(400)
            tx = pg.evaluate("()=>{ const c=document.getElementById('rc-pan').cloneNode(true); c.querySelectorAll('[data-nolang]').forEach(x=>x.remove()); return c.innerText; }")
            check(f'LE POINT — {lg} : la fenêtre est traduite (bouton « {bouton} »), plus un mot de français', bouton in tx and not FR.search(tx), [FR.findall(tx)[:6], tx[:300]])
            pg.context.close()
        check('aucune erreur JS', not err, err[:3])
        b.close()
finally:
    srv.terminate()
print(f'\n{ok} ok, {len(ko)} KO', ko); sys.exit(1 if ko else 0)
