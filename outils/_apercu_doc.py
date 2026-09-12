# Fabrique une facture et un devis d'exemple, avec la VRAIE identite de DASY,
# et en prend une image. Tout se passe en local : la production n'est pas touchee.
import pathlib, json
from playwright.sync_api import sync_playwright
D = pathlib.Path('/home/claude/catalogue')
LOGO = '/mnt/user-data/uploads/Desktop/cropped-logo-pt.png'

REG = {
    'raison': 'DASY LLC',
    'enseigne': 'Perfumes Trade',
    'adresse': '2035 NW 23rd Ave, Miami FL 33142-7353, USA',
    'tel': '+1 (786) 483-7758',
    'email': 'perfumestradellc@gmail.com',
    'taxid': '23-8017604432-6',
    'taux': 7, 'carte': 2.6,
    'zelle': 'Zelle : samamsellem@hotmail.com',
    'prefixe': 'PT',
    'conditions': 'Payment on receipt. Goods sold are not returnable or exchangeable.',
    'exo': 'Sale for resale — Florida Annual Resale Certificate on file.',
}
SESS = ("localStorage.setItem('sam-session-v1', JSON.stringify("
        "{id:'sam',nom:'Sam',role:'patron',depuis:new Date().toISOString()}))")

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width': 1280, 'height': 1400}, device_scale_factor=2)
    err = []
    pg.on('pageerror', lambda e: err.append(str(e)))

    # --- l'identite, par le chemin de la page elle-meme ---
    pg.goto('file://' + str(D / 'accueil.html')); pg.wait_for_timeout(600)
    pg.evaluate(SESS)
    pg.goto('file://' + str(D / 'reglages.html')); pg.wait_for_timeout(2600)
    pg.evaluate("""(R)=>{
      const m={raison:'f-raison',enseigne:'f-enseigne',adresse:'f-adresse',tel:'f-tel',
               email:'f-email',taxid:'f-taxid',taux:'f-taux',carte:'f-carte',zelle:'f-zelle',
               prefixe:'f-prefixe',conditions:'f-conditions',exo:'f-exo'};
      for(const k in m){ const el=document.getElementById(m[k]);
        if(el){ el.value=R[k]; el.dispatchEvent(new Event('input',{bubbles:true})); } }
    }""", REG)
    pg.set_input_files('#f-logofic', LOGO); pg.wait_for_timeout(2200)
    print('logo :', pg.locator('#f-logoaide').inner_text()[:60])

    # --- deux vraies references du catalogue ---
    pg.goto('file://' + str(D / 'ventes.html')); pg.wait_for_timeout(2800)
    refs = pg.evaluate("""(()=>{ const o=[];
      for(const c in IDX){ const v=IDX[c];
        if(v[0] && v[1] && v[2] && v[4]>0){ o.push({cle:c, bc:String(v[0]),
          nom:(v[2]+' '+v[1]).slice(0,54), pv:+v[4]}); }
        if(o.length>=3) break; } return o; })()""")
    print('references :', [r['nom'] for r in refs])

    def document(type_doc, opts, nom_fichier, client, remise=''):
        pg.evaluate("""([refs,type,o,client,remise])=>{
          PANIER.length=0;
          refs.forEach((r,i)=>PANIER.push({cle:r.cle,bc:r.bc,ref:r.nom,q:[6,12,3][i]||1,p:r.pv}));
          $('v-doc').value=type;
          $('v-client').value=client;
          $('v-pmode').value=o.pmode; $('v-pstat').value=o.pstat;
          $('v-fiscal').value=o.fiscal; $('v-fref').value=o.fref||'';
          $('v-remval').value=remise; $('v-remtype').value='pct';
          $('v-remlib').value= remise?'client fidèle':'';
          $('v-langue').value=o.langue||'';
          if($('v-frais')) $('v-frais').value='';
          docChampsMaj();
          const d=docPourVente(PANIER.map(l=>({q:l.q,p:l.p})),client,'2026-09-09',{});
          const f={id:'apercu',num:d.num,sens:'vente',d:'2026-09-09',tiers:client,
                   par:'Sam',t:new Date().toISOString(),doc:d,
                   lignes:PANIER.map(l=>({cle:l.cle,bc:l.bc,ref:l.ref,q:l.q,p:l.p}))};
          dessineDoc(f);
        }""", [refs, type_doc, opts, client, remise])
        pg.wait_for_timeout(1400)
        z = pg.locator('#doc-corps')
        z.screenshot(path=str(D / nom_fichier))
        print(nom_fichier, '->', z.inner_text().split('\n')[0][:50])

    document('facture',
             {'pmode': 'carte', 'pstat': 'paye', 'fiscal': 'taxable', 'langue': 'fr'},
             'apercu_facture.png', 'Boutique Aventura')

    document('devis',
             {'pmode': 'zelle', 'pstat': 'apayer', 'fiscal': 'resale',
              'fref': '23-8012345678-9', 'langue': 'en'},
             'apercu_devis.png', 'Miami Fragrance Wholesale', remise='8')

    print('erreurs JS :', err[:2] if err else 'aucune')
    b.close()
