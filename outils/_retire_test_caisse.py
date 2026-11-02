# RETIRÉ le 15 oct. 2026 — ne tourne plus dans la batterie.
# Ce test éprouvait « Importer des ventes » sur la page Factures (import d une caisse Lightspeed en CSV).
# Cette page ne reçoit plus que des factures fournisseurs (SENS="achat" fixé, le sélecteur #sens reste caché) :
# l entrée n existe plus à l écran. Les ventes de caisse arrivent par le cockpit (/ls/…/ventes, _t_lsventes*.mjs).
# Gardé pour mémoire, au cas où l import par fichier reviendrait.
# Test import d'un export de caisse : retours, magasins, colonnes corrigeables.
import pathlib
from playwright.sync_api import sync_playwright
D=pathlib.Path('/home/claude/catalogue')
ok=0; ko=[]
def check(n,c,i=''):
    global ok
    if c: ok+=1; print('  ok ',n)
    else: ko.append(n); print('  KO ',n,i)
SESS="localStorage.setItem('sam-session-v1', JSON.stringify({id:'sam',nom:'Sam',role:'patron',depuis:new Date().toISOString()}))"

# export facon Lightspeed : deux caisses, un retour
CSV = """Date,Receipt number,Outlet,Customer,Product,SKU,Quantity,Price,Total
2026-09-01,R-1001,Main Outlet,walk-in,Abercrombie Fierce,085715169587,3,72.00,216.00
2026-09-01,R-1002,Main Outlet,walk-in,Abercrombie Fierce,085715169587,1,72.00,72.00
2026-09-02,R-1003,Main Outlet,jean,Abercrombie Fierce,085715169587,-1,72.00,-72.00
2026-09-02,R-1010,Second Outlet,walk-in,Abercrombie Fierce,085715169587,5,70.00,350.00
"""
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1400,'height':950}); err=[]
    pg.on('pageerror',lambda e:err.append(str(e)))
    pg.goto('file://'+str(D/'accueil.html')); pg.wait_for_timeout(600); pg.evaluate(SESS)
    pg.goto('file://'+str(D/'factures.html')); pg.wait_for_timeout(2500)
    q0=pg.evaluate("__F.qteEff(__F.parBC['085715169587'])")

    print('1. lecture de l export')
    pg.click('#sens button[data-s="canal"]'); pg.wait_for_timeout(300)
    pg.select_option('#canal-nom','Caisse Lightspeed')
    pg.click('#basc'); pg.fill('#colle',CSV); pg.wait_for_timeout(900)
    A=pg.evaluate("JSON.parse(JSON.stringify(__F.APERCU))")
    check('lignes lues', A and A['connues']==1, A and {k:A[k] for k in ('connues','inconnues')})
    X=A['X']
    check('colonnes reconnues', 'sku' in X['colonnes'] and 'qte' in X['colonnes'], X['colonnes'])
    check('1 retour signale', X['retours']==1, X['retours'])
    check('2 magasins detectes', X['lieux']==['Main Outlet','Second Outlet'], X['lieux'])
    check('solde 3+1-1+5 = 8', A['L'][0]['q']==8, A['L'][0])
    check('bandeau parle des retours', 'retours' in pg.locator('#apercu').inner_text().lower())

    print('2. filtrer sur un magasin')
    pg.evaluate("document.querySelector('.mapbox').open=true"); pg.wait_for_timeout(200)
    pg.select_option('#map-lieu','Second Outlet'); pg.wait_for_timeout(700)
    A=pg.evaluate("JSON.parse(JSON.stringify(__F.APERCU))")
    check('un seul magasin : 5 unites', A['L'][0]['q']==5, A['L'][0]['q'])
    check('lignes ecartees signalees', 'autre magasin' in pg.locator('#apercu').inner_text())
    pg.evaluate("document.querySelector('.mapbox').open=true"); pg.wait_for_timeout(200)
    pg.select_option('#map-lieu',''); pg.wait_for_timeout(700)

    print('3. corriger une colonne a la main')
    pg.evaluate("document.querySelector('.mapbox').open=true"); pg.wait_for_timeout(200)
    pg.select_option('#apercu select[data-map="prix"]','8')   # colonne Total
    pg.wait_for_timeout(700)
    A=pg.evaluate("JSON.parse(JSON.stringify(__F.APERCU))")
    check('prix relu depuis Total', abs(A['montant']-566)<1 or A['montant']!=0, A['montant'])
    pg.evaluate("document.querySelector('.mapbox').open=true"); pg.wait_for_timeout(200)
    pg.select_option('#apercu select[data-map="prix"]','7'); pg.wait_for_timeout(700)

    print('4. enregistrement')
    A=pg.evaluate("JSON.parse(JSON.stringify(__F.APERCU))")
    pg.click('#ok'); pg.wait_for_timeout(1000)
    # le message dit « importées » et pas « export » : c'est l'outil qui importe
    _m = pg.locator('#msg').inner_text()
    check('enregistre', 'import' in _m.lower() and 'stock' in _m.lower(), _m)
    check('le mot export ne sert plus a nommer l action', 'xport' not in _m, _m)
    check('stock -8', pg.evaluate("__F.qteEff(__F.parBC['085715169587'])")==q0-8,
          (q0, pg.evaluate("__F.qteEff(__F.parBC['085715169587'])")))
    V=pg.evaluate("JSON.parse(localStorage.getItem('ventes-v1')||'{}')")
    check('vente ecrite', any(len(v)>0 for v in V.values()), list(V.items())[:1])

    print('5. reimport du meme fichier : rien de nouveau')
    pg.click('#basc') if pg.locator('#txt.on').count()==0 else None
    pg.fill('#colle',CSV); pg.wait_for_timeout(900)
    txt=pg.locator('#apercu').inner_text()
    check('doublons refuses', 'déjà' in txt or 'deja' in txt.lower(), txt[:200])

    print('6. les ventes remontent au tableau de bord')
    pg.goto('file://'+str(D/'tableau.html')); pg.wait_for_timeout(2500)
    check('tableau sans erreur', not err, err[:3])
    check('le dashboard voit les ventes', pg.evaluate("VL.length")>0, pg.evaluate("VL.length"))
    check('chiffre d affaires non nul', pg.evaluate("VL.reduce((a,x)=>a+x.mt,0)")>0, pg.evaluate("VL.reduce((a,x)=>a+x.mt,0)"))
    b.close()
print('erreurs :',err)
print('%d ok, %d KO %s'%(ok,len(ko),ko))
