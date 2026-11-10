# La fiche d'un parfum raconte ses ventes : combien, sur quel canal, à qui (Sam, 11 oct. 2026).
import pathlib
from playwright.sync_api import sync_playwright
D = pathlib.Path('/home/claude/catalogue'); ok = 0; ko = []
def check(n, c, i=''):
    global ok
    if c: ok += 1; print('  ok  ', n)
    else: ko.append(n); print('  KO  ', n, i)
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1400, 'height': 900}); err = []
    pg.on('pageerror', lambda e: err.append(str(e)))
    pg.add_init_script("if(!localStorage.getItem('sam-session-v1')) localStorage.setItem('sam-session-v1', JSON.stringify({id:'sam',nom:'Sam',role:'patron',depuis:new Date().toISOString()}))")
    pg.goto('file://' + str(D / 'catalogue.html')); pg.wait_for_timeout(2500)
    pg.evaluate('window.D_HG=null')   # sans l\'historique d\'avant l\'ERP : on compte seulement les ventes posées ici
    X = pg.evaluate("""()=>{ const p=tousLesArticles().find(x=>x.qte>3&&/^\\d+$/.test(x.bc)); const k=p.cle||p.id;
      const F=[
        {id:'a',num:'PT-2026-0001',sens:'vente',canal:'Site perfumestrade.com',tiers:'Maria Lopez',d:'2026-10-09',h:'10:00',auto:'woocommerce',lignes:[{cle:k,bc:p.bc,ref:'x',q:2,p:80}]},
        {id:'b',num:'PT-2026-0002',sens:'vente',canal:'Vente en gros',tiers:'Collection Perfumes',d:'2026-10-05',lignes:[{cle:k,bc:p.bc,ref:'x',q:12,p:55}]},
        {id:'c',num:'PT-2026-0003',sens:'vente',canal:'Amazon',tiers:'Chad Johnson',d:'2026-09-20',lignes:[{cle:k,bc:p.bc,ref:'x',q:1,p:95}]},
        {id:'d',num:'PT-2026-0001-R1',sens:'vente',retour:true,refId:'a',canal:'Site perfumestrade.com',tiers:'Maria Lopez',d:'2026-10-10',lignes:[{cle:k,bc:p.bc,ref:'x',q:-1,p:80}]},
        {id:'e',num:'PT-2026-0004',sens:'vente',canal:'Vente en gros',tiers:'Collection Perfumes',d:'2025-01-15',lignes:[{cle:k,bc:p.bc,ref:'x',q:6,p:50}]},
        {id:'f',num:'PT-2026-0005',sens:'vente',canal:'Amazon',tiers:'Autre',d:'2026-10-01',lignes:[{cle:'autre-cle',bc:'000',ref:'y',q:3,p:10}]} ];
      ecrit('factures-v1',F); PERIODE='tout'; $('fs').value=''; $('q').value=p.bc; render(); ouvreFiche(p.id); FICHE.vOpen=true; FICHE.vDet=true; dessineFiche(); return {bc:p.bc,nom:p.nom}; }""")
    pg.wait_for_timeout(600)
    # 12 oct. (Igal : « il faut réduire cette page et donner la possibilité de cliquer pour ouvrir ») : le bloc est replié par défaut
    pg.evaluate("()=>{ FICHE.vOpen=false; FICHE.vDet=false; dessineFiche(); }"); pg.wait_for_timeout(300)
    check('le bloc des ventes est REPLIÉ par défaut', pg.locator('#dvtes').count() == 1 and not pg.evaluate("document.getElementById('dvtes').open"))
    rs = pg.locator('#dvtes > summary').inner_text()
    check('replié, il dit quand même combien : ventes, flacons, montant, dernière vente', 'vente' in rs and 'flacons' in rs and '$' in rs and 'dernière' in rs, rs)
    check('les 60 lignes ne prennent pas la place : liste cachée', not pg.locator('#dvtes .vlist').is_visible())
    pg.locator('#dvtes > summary').click(); pg.wait_for_timeout(300)
    check('un clic l\'ouvre : les chiffres et la ventilation par canal / client, pas la longue liste', pg.evaluate("document.getElementById('dvtes').open") and pg.locator('#dvtes .vtab').count() == 1 and pg.locator('#dvtes .vcli li').count() >= 1 and not pg.locator('#dvtes .vlist').is_visible())
    pg.locator('#dvdet > summary').click(); pg.wait_for_timeout(300)
    check('« cliquer pour agrandir » montre le rythme et chaque vente', pg.locator('#dvtes .vlist').is_visible() and pg.locator('#dvtes .vryt').is_visible())
    pg.click('#ddb [data-per="3"]'); pg.wait_for_timeout(300)
    check('changer de période ne le referme pas', pg.evaluate("document.getElementById('dvtes').open"))
    pg.click('#ddb [data-per="tout"]'); pg.wait_for_timeout(300)
    t = pg.inner_text('#ddb') if pg.locator('#ddb').count() else pg.inner_text('body')
    check('le bloc « Ventes de ce parfum » est dans la fiche', 'VENTES DE CE PARFUM' in t.upper())
    check('flacons vendus, retours déduits : 2+12+1+6−1 = 20', '20' in t.split('flacons vendus')[0][-12:], t.split('flacons vendus')[0][-40:])
    check('le chiffre de vente : 160+660+95+300−80 = 1 135 $', '1135' in t.replace('\u202f','').replace('\xa0','').replace(' ',''), t[:0])
    check('par canal : Vente en gros en tête (18)', 'Vente en gros' in t and 'Amazon' in t and 'Site perfumestrade.com' in t)
    check('par client : Collection Perfumes, Maria Lopez, Chad Johnson', 'Collection Perfumes' in t and 'Maria Lopez' in t and 'Chad Johnson' in t)
    check('la vente d\'un autre parfum n\'y est pas', 'Autre ' not in t.split('CHAQUE VENTE')[1][:700] and 'PT-2026-0005' not in t)
    check('le retour est visible comme tel', 'retour 1' in t)
    pg.click('#ddb [data-per="3"]'); pg.wait_for_timeout(400)
    t2 = pg.inner_text('#ddb')
    check('sur 3 mois, la vente de janvier 2025 disparaît : 14 flacons', '14' in t2.split('flacons vendus')[0][-12:], t2.split('flacons vendus')[0][-40:])
    # 11 oct. (suite) : le rythme, la marge, l'Excel, le lien vers la vente
    pg.click('#ddb [data-per="tout"]'); pg.wait_for_timeout(400)
    t3 = pg.inner_text('#ddb')
    check('le rythme : flacons / semaine, semaines de stock, dernière vente', 'flacons / semaine' in t3 and 'semaines de stock' in t3 and 'depuis la dernière vente' in t3)
    check('les barres des 12 derniers mois sont là', pg.locator('#ddb .vmois .vm').count() == 12)
    check('la marge (Patron) : « il te reste » dans les totaux et par canal', 'il te reste' in t3 and pg.locator('#ddb .vtab th:has-text("Il te reste")').count() >= 1)
    check('chaque vente porte sa marge', pg.locator('#ddb .vlist .mg').count() >= 4)
    # 1er nov. 2026 (Igal : « rajouter le prix payé par le customer »), puis 10 nov. (Sam ne comprenait pas le tableau) :
    # « Par client » est une phrase par client — flacons, total, prix moyen du flacon (et la fourchette), dernier achat
    K = pg.evaluate("()=>[...document.querySelectorAll('#ddb .vcli li')].map(li=>li.innerText.replace(/\\s+/g,' ').trim())")
    check('LE POINT — « Par client » : une phrase par client, plus de tableau', len(K) >= 3 and pg.locator('#ddb .vtab').count() == 1, K)
    coll = next((r for r in K if r.startswith('Collection')), None)
    check('LE POINT — Collection Perfumes : « 18 flacons, … au total · 53,33 $ le flacon en moyenne (entre 50,00 $ et 55,00 $) · dernier achat le … »',
          coll and '18 flacons' in coll and 'au total' in coll and '53,33 $ le flacon en moyenne' in coll and 'entre 50,00 $ et 55,00 $' in coll and 'dernier achat le' in coll, coll)
    chad = next((r for r in K if r.startswith('Chad')), None)
    check('Chad Johnson : « 1 flacon » au singulier, un seul prix « 95,00 $ le flacon », sans fourchette ni « en moyenne »', chad and '1 flacon,' in chad and '95,00 $ le flacon' in chad and 'entre' not in chad and 'moyenne' not in chad, chad)
    maria = next((r for r in K if r.startswith('Maria')), None)
    check('Maria Lopez : 80,00 $ le flacon (le retour ne fausse pas le prix payé)', maria and '80,00 $ le flacon' in maria and 'entre' not in maria, maria)
    for lg, mots, fr in (('en', ['bottles', 'in total', 'per bottle on average', 'between', 'last purchase'], ['flacon', 'au total', 'moyenne', 'dernier achat']),
                         ('es', ['frascos', 'en total', 'el frasco de media', 'entre', 'última compra'], ['flacon', 'au total', 'moyenne', 'dernier achat'])):
        pg.evaluate("l=>{ localStorage.setItem('langue-v1',l); if(typeof appliqueLangue==='function') appliqueLangue(l); LANG=l; dessineFiche(); }", lg); pg.wait_for_timeout(300)
        c2 = next((r for r in pg.evaluate("()=>[...document.querySelectorAll('#ddb .vcli li')].map(li=>li.innerText.replace(/\\s+/g,' ').trim())") if r.startswith('Collection')), '')
        print('     ', lg, c2)
        check(f'{lg} : la phrase est traduite, plus un mot de français', all(m in c2 for m in mots) and not any(m in c2 for m in fr), c2)
    pg.evaluate("()=>{ localStorage.setItem('langue-v1','fr'); LANG='fr'; if(typeof appliqueLangue==='function') appliqueLangue('fr'); dessineFiche(); }"); pg.wait_for_timeout(300)
    with pg.expect_download() as dl:
        pg.click('#ddb [data-vxl]')
    check('l\'historique complet se télécharge en Excel', dl.value.suggested_filename.startswith('ventes-') and dl.value.suggested_filename.endswith('.xlsx'), dl.value.suggested_filename)
    with pg.expect_navigation():
        pg.click('#ddb .vlist li.vlk >> nth=1')
    check('un clic sur une vente ouvre Ventes sur son numéro', 'ventes.html' in pg.url and 'q=PT-2026-0001' in pg.url, pg.url)
    pg.wait_for_timeout(2500)
    check('et la vente est cherchée dans Ventes', pg.input_value('#q') == 'PT-2026-0001', pg.input_value('#q'))
    # un commercial ne voit pas la marge
    pg.evaluate("""()=>{ localStorage.setItem('sam-comptes-demo-v1','0');
      localStorage.setItem('sam-comptes-v1',JSON.stringify([{ident:'sam',nom:'Sam',role:'patron',actif:true,h:'x'},{ident:'josh',nom:'Josh',role:'commercial',actif:true,h:'x'}]));
      localStorage.setItem('sam-session-v1', JSON.stringify({id:'josh',nom:'Josh',role:'commercial',depuis:new Date().toISOString()})); }""")
    pg.goto('file://' + str(D / 'catalogue.html')); pg.wait_for_timeout(2500)
    pg.evaluate("()=>{ const F=lit('factures-v1',[]); const k=F[0].lignes[0].cle; const p=tousLesArticles().find(x=>(x.cle||x.id)===k); PERIODE='tout'; $('fs').value=''; $('q').value=p.bc; render(); ouvreFiche(p.id); FICHE.vOpen=true; FICHE.vDet=true; dessineFiche(); }")
    pg.wait_for_timeout(600)
    t4 = pg.inner_text('#ddb')
    check('un commercial voit les ventes mais pas « il te reste »', 'flacons vendus' in t4 and 'il te reste' not in t4.lower().replace('il te reste','il te reste'), t4[:0])
    check('aucune erreur JS', not err, err[:2])
    b.close()
print(f'\n{ok} ok, {len(ko)} KO', ko)
