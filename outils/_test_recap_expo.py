# L'EXPORT POUR LE COMPTABLE (14 nov. 2026 — Igal : « quand il sort le chiffre d'affaires sur son dashboard, sur 1 mois, sur 2 mois,
# qu'il puisse exporter un document à son comptable. En anglais, bien sûr. » ; choix : Excel + PDF, résumé PAR CANAL, avec coût et
# marge). Ce test protège :
#   1. LE POINT — deux boutons au tableau de bord (Excel, PDF), sur la période choisie, réservés à qui voit les marges ;
#   2. LE POINT — les chiffres du fichier sont CEUX DU TABLEAU DE BORD : net sales = chiffre d'affaires, net margin = marge nette ;
#   3. le détail par canal : ventes, remboursements, sales tax enregistrée, flacons, coût d'achat, frais, marge — vérifié à la main ;
#   4. sur deux mois, le même tableau est donné mois par mois, et ses totaux refont le total ;
#   5. une ligne sans prix d'achat est dite en note (comptée dans les ventes, pas dans la marge) ; un canal sans taxe le dit ;
#   6. LE POINT — tout est en anglais, Excel comme PDF : plus un mot de français ;
#   7. aucune erreur JS.
import subprocess, time, socket, json, re, sys, datetime, os, io
from playwright.sync_api import sync_playwright
import openpyxl
D = '/home/claude/catalogue'
ok = 0; ko = []
def check(n, c, i=''):
    global ok
    if c: ok += 1; print('  ok  ', n)
    else: ko.append(n); print('  KO  ', n, str(i)[:600])
s = socket.socket(); s.bind(('127.0.0.1', 0)); port = s.getsockname()[1]; s.close()
srv = subprocess.Popen(['python3', '-m', 'http.server', str(port), '--bind', '127.0.0.1'], cwd=D, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)
OUT = '/tmp/claude-0/-home-claude/7f8c7d7e-a2bf-53ed-8df2-d9c17ddd87b0/scratchpad/expo'; os.makedirs(OUT, exist_ok=True)
auj = datetime.date(2026, 11, 20)
PREP = """([lg,role])=>{ localStorage.clear(); localStorage.setItem('sam-comptes-demo-v1','0');
  localStorage.setItem('sam-session-v1',JSON.stringify({id:'sam',nom:'Sam',role:role,depuis:new Date().toISOString()})); localStorage.setItem('langue-v1',lg);
  localStorage.setItem('reglages-v1',JSON.stringify({comV4:1,canauxV:3,pcCom3:1,canaux:[{id:'site',nom:'Site perfumestrade.com',com:3},{id:'sitegros',nom:'Site wholesale.perfumestrade.com',base:'pvw',com:3},{id:'amazon',nom:'Amazon',com:15},{id:'perfumecity',nom:'Perfume City',com:3}],
    fact:{raison:'DASY LLC',enseigne:'Perfumes Trade',adresse:'1881 NW 20th St, Miami FL 33142',tel:'',email:'',taxid:'',taux:7}})); }"""
VENTES = """()=>{ const K=Object.keys(IDX); const A=K.find(k=>IDX[k][3]!=null&&+IDX[k][3]>0); const B=K.find(k=>IDX[k][3]==null&&IDX[k][1]);
  const L=(cle,q,p,pa)=>{ const l={cle,bc:IDX[cle][0],ref:'x',q,p}; if(pa!=null) l.paAv=pa; return l; };
  const F=[{id:'g1',num:'PT-1',sens:'vente',canal:'Gros',tiers:'Carmen',d:'2026-10-10',lignes:[L(A,10,50,30)],doc:{base:500,taxe:35,total:535,taux:7}},
    {id:'c1',num:'LS-1',sens:'vente',canal:'Caisse Lightspeed',auto:'lightspeed',d:'2026-10-12',taxe:14,lignes:[L(A,2,100,30)],paie:{especes:214,carte:0}},
    {id:'s1',num:'W-1',sens:'vente',canal:'Site perfumestrade.com',auto:'woocommerce',d:'2026-10-15',port:10,lignes:[L(A,1,120,30)]},
    {id:'p1',num:'PC-1',sens:'vente',canal:'Perfume City',auto:'shopify-pc',_i:'fa|shopify-pc|1',d:'2026-10-20',taxe:6.3,lignes:[L(A,1,90,30)]},
    {id:'a1',num:'A-1',sens:'vente',canal:'Amazon',auto:'amazon',d:'2026-10-21',lignes:[L(A,1,150,30)]},
    {id:'s2',num:'W-2',sens:'vente',canal:'Site perfumestrade.com',auto:'woocommerce',d:'2026-11-05',lignes:[L(A,2,100,30)]},
    {id:'s2r',num:'W-2',sens:'vente',canal:'Site perfumestrade.com',auto:'woocommerce',d:'2026-11-07',retour:true,refNum:'W-2',lignes:[L(A,-1,100,30)]},
    {id:'g2',num:'PT-2',sens:'vente',canal:'Gros',tiers:'Robert',d:'2026-11-08',lignes:[L(B,4,25)]}];
  localStorage.setItem('factures-v1',JSON.stringify(F));
  localStorage.setItem('site-taxes-v1',JSON.stringify({'woocommerce|W-1':8.4,'woocommerce|W-2':14,_depuis:{woocommerce:'2026-09-01T00:00:00'}})); return [A,B]; }"""
FR = re.compile(r"(\b(Vente|Ventes|vente|ventes|Caisse|Gros|Marge|marge|Remboursement|remboursement|prix d'achat|Canal|Chiffre|Flacons|mois|Taxe|Période|novembre|octobre|Total des)\b|[éèêàçù])")
try:
    with sync_playwright() as p:
        b = p.chromium.launch(); err = []
        def ouvre(lg='fr', role='patron'):
            ctx = b.new_context(viewport={'width': 1400, 'height': 950}, timezone_id='America/New_York', locale='fr-FR', reduced_motion='reduce', accept_downloads=True)
            pg = ctx.new_page(); pg.on('pageerror', lambda e: err.append(str(e)))
            pg.add_init_script("Object.defineProperty(window,'D_HG',{configurable:true,set(v){ window.__hgReel=v; },get(){ return null; }})")
            pg.clock.set_fixed_time(datetime.datetime(auj.year, auj.month, auj.day, 14, 0, tzinfo=datetime.timezone(datetime.timedelta(hours=-5))))
            base = f'http://127.0.0.1:{port}/'
            pg.goto(base + 'accueil.html'); pg.wait_for_timeout(300); pg.evaluate(PREP, [lg, role])
            pg.goto(base + 'tableau.html'); pg.wait_for_timeout(1500); pg.evaluate(VENTES)
            pg.evaluate("()=>{ RC.sel='mois2:2026-10:2026-11'; RC.metric='ca'; rcSauve(); }"); pg.reload(); pg.wait_for_timeout(2500); return pg
        pg = ouvre()
        bar = pg.inner_text('#recap .rc-expo') if pg.locator('#recap .rc-expo').count() else ''
        check('LE POINT — au tableau de bord : « Pour le comptable », document en anglais, deux boutons Excel et PDF', 'Pour le comptable' in bar and 'anglais' in bar and pg.locator('#recap [data-rcx="xlsx"]').count() == 1 and pg.locator('#recap [data-rcx="pdf"]').count() == 1, bar)
        dash = pg.evaluate("()=>{ const P=rcPlage(RC.sel), T=rcAgrege(rcLignes(),P.a,P.b).T; return [Math.round(T.ca*100)/100, Math.round(T.mg*100)/100, T.q]; }")
        print('2. Excel')
        with pg.expect_download() as dl: pg.click('#recap [data-rcx="xlsx"]')
        fx = os.path.join(OUT, dl.value.suggested_filename); dl.value.save_as(fx)
        check('le fichier Excel porte la période dans son nom', dl.value.suggested_filename.startswith('Perfumes-Trade-sales-2026-10-01_2026-11-20') and fx.endswith('.xlsx'), dl.value.suggested_filename)
        ws = openpyxl.load_workbook(fx).active; R = [[c for c in r] for r in ws.iter_rows(values_only=True)]
        H = R[0]; idx = {h: i for i, h in enumerate(H)}
        tot = next(r for r in R if r[1] == 'TOTAL')
        check('LE POINT — net sales du fichier = chiffre d\'affaires du tableau de bord ; net margin = marge nette ; bouteilles = flacons', abs(tot[idx['Net sales']] - dash[0]) < 0.01 and abs(tot[idx['Net margin']] - dash[1]) < 0.01 and tot[idx['Bottles']] == dash[2], [tot, dash])
        row = {r[1]: r for r in R[1:] if r and r[0] and r[0].startswith('October 1') and r[1] != 'TOTAL'}
        g, c, w = row.get('Wholesale (in store)'), row.get('Retail store (Lightspeed)'), row.get('perfumestrade.com')
        pc, am, wg = row.get('Perfume City'), row.get('Amazon'), row.get('wholesale.perfumestrade.com')
        check('LE POINT — les canaux ont leur nom en anglais (Wholesale, Retail store, perfumestrade.com)', g is not None and c is not None and w is not None, list(row))
        check('Wholesale : 2 commandes, 600 $ (10 × 50 + 4 × 25), taxe 35 $, coût 300 $ (la ligne sans prix d\'achat n\'a pas de coût)', g[idx['Orders']] == 2 and g[idx['Net sales']] == 600 and g[idx['Sales tax collected']] == 35 and g[idx['Cost of goods']] == 300, g)
        check('Site : 2 commandes, 1 remboursement, ventes brutes 320 $, remboursé 100 $, net 220 $', w[idx['Orders']] == 2 and w[idx['Refunds']] == 1 and w[idx['Gross sales']] == 320 and w[idx['Refunds ($)']] == -100 and w[idx['Net sales']] == 220, w)
        # 14 nov. 2026 — Igal : « tous les canaux de vente de l'ERP », « les sales tax », « les frais de transport »
        check('LE POINT — TOUS les canaux de l\'ERP sont là, même sans vente (le site de gros à 0)', all(x is not None for x in (g, c, w, pc, am, wg)) and wg[idx['Net sales']] == 0 and wg[idx['Orders']] == 0, sorted(row))
        check('LE POINT — la sales tax collectée, canal par canal : caisse 14 $, factures 35 $, Perfume City 6,30 $, site 8,40 + 14 − 7 (la moitié remboursée) = 15,40 $', c[idx['Sales tax collected']] == 14 and g[idx['Sales tax collected']] == 35 and pc[idx['Sales tax collected']] == 6.3 and abs(w[idx['Sales tax collected']] - 15.4) < 0.001, [c[idx['Sales tax collected']], g[idx['Sales tax collected']], pc[idx['Sales tax collected']], w[idx['Sales tax collected']]])
        check('Amazon collecte sa taxe lui-même : « n/a », et une note le dit', am[idx['Sales tax collected']] == 'n/a', am)
        check('LE POINT — le transport à part : port payé par le client (site 10 $), coût des envois (8 $ par commande du site et d\'Amazon)', w[idx['Shipping charged']] == 10 and w[idx['Shipping costs']] == 16 and am[idx['Shipping costs']] == 8 and c[idx['Shipping costs']] == 0, [w[idx['Shipping charged']], w[idx['Shipping costs']], am[idx['Shipping costs']]])
        check('la marge se refait à la main : ventes nettes − coût − commissions et frais + port encaissé − envois (site, toutes ses lignes ont un prix d\'achat)', abs(w[idx['Net sales']] - w[idx['Cost of goods']] - w[idx['Commissions & card fees']] + w[idx['Shipping charged']] - w[idx['Shipping costs']] - w[idx['Net margin']]) < 0.02, w)
        bm = [r for r in R if r and r[0] in ('October 2026', 'November 2026')]
        tm = [r for r in bm if str(r[1]).startswith('Total ')]
        check('LE POINT — sur deux mois : le tableau mois par mois (octobre, novembre), et ses deux totaux refont le total', len(tm) == 2 and abs(sum(r[idx['Net sales']] for r in tm) - tot[idx['Net sales']]) < 0.01 and abs(sum(r[idx['Net margin']] for r in tm) - tot[idx['Net margin']]) < 0.01, tm)
        txt = ' '.join(str(x) for r in R for x in r if x is not None)
        check('une note dit la ligne sans prix d\'achat (100 $ de ventes, hors coût et marge) et qu\'Amazon collecte sa taxe lui-même', '1 sale line ($100.00 of sales) had no purchase price' in txt and 'n/a: Amazon collects the sales tax on its own marketplace orders' in txt, txt[-700:])
        check('LE POINT — Excel : plus un mot de français', not FR.search(txt), FR.findall(txt)[:8])
        print('3. PDF')
        with pg.expect_download() as dl: pg.click('#recap [data-rcx="pdf"]')
        fp = os.path.join(OUT, dl.value.suggested_filename); dl.value.save_as(fp)
        t = subprocess.run(['pdftotext', '-layout', fp, '-'], capture_output=True, text=True).stdout
        check('le PDF est fait (paysage), avec la société, le titre et la période', fp.endswith('.pdf') and 'DASY LLC' in t and 'Sales report by channel' in t and 'Period: October 1 – November 20, 2026' in t, t[:400])
        check('LE POINT — le PDF donne les mêmes totaux (net sales, net margin) que le tableau de bord', ('$%s' % format(dash[0], ',.2f')) in t and ('$%s' % format(dash[1], ',.2f')) in t, [dash, t[:900]])
        check('le PDF a le tableau mois par mois et les notes', 'By month' in t and 'October 2026' in t and 'November 2026' in t and 'Notes' in t and 'had no purchase price' in t, t[-700:])
        check('le PDF n\'a aucun signe que sa police ne sait pas écrire (− × ÷ sortaient en guillemets) : les remboursements s\'écrivent -$100.00', '"' not in t and '-$100.00' in t, [l for l in t.splitlines() if '"' in l][:3])
        check('une marge en % sans aucun prix d\'achat connu n\'est pas « 0.0% » : un tiret', ' 0.0%' not in t, [l for l in t.splitlines() if '0.0%' in l][:3])
        check('dans le PDF, les noms des canaux sont écrits en entier (pas coupés par « … »)', '…' not in t and 'wholesale.perfumestrade.com' in t and 'Retail store (Lightspeed)' in t, [l for l in t.splitlines() if '…' in l][:3])
        check('LE POINT — PDF : plus un mot de français', not FR.search(t), FR.findall(t)[:8])
        pg.context.close()
        print('4. les droits et les langues de la barre')
        pg = ouvre(role='commercial')
        check('un rôle qui ne voit pas les marges n\'a pas les boutons', pg.locator('#recap [data-rcx]').count() == 0)
        pg.context.close()
        for lg, mot in (('en', 'For the accountant'), ('es', 'Para el contador')):
            pg = ouvre(lg=lg); bar = pg.inner_text('#recap .rc-expo')
            check(f'{lg} — la barre est traduite (« {mot} »)', mot in bar and 'comptable' not in bar and 'anglais' not in bar, bar)
            pg.context.close()
        check('aucune erreur JS', not err, err[:3])
        b.close()
finally:
    srv.terminate()
print(f'\n{ok} ok, {len(ko)} KO', ko); sys.exit(1 if ko else 0)
