# Mes canaux de vente, en lignes (11 oct. 2026) : le prix Amazon est celui de l'annonce de Sam.
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
    pg.add_init_script("localStorage.setItem('sam-session-v1', JSON.stringify({id:'sam',nom:'Sam',role:'patron',depuis:new Date().toISOString()}))")
    pg.goto('file://' + str(D / 'catalogue.html')); pg.wait_for_timeout(2500)
    X = pg.evaluate("""()=>{ const p=tousLesArticles().find(x=>x.qte>3&&x.pa>5&&x.pvr>30&&/^\\d+$/.test(x.bc)&&!(x.pc&&x.pc.amazon));
      $('fs').value=''; $('q').value=p.bc; render(); ouvreFiche(p.id); return {bc:p.bc,pvr:p.pvr}; }""")
    pg.wait_for_timeout(500)
    t = pg.inner_text('#ddb details.dcanw')
    # 11 nov. 2026 (Sam) : colonnes Prix · En ligne ? · Il te reste
    check('une ligne par canal, avec les colonnes', pg.locator('.dcanl .cn').count() >= 2 and 'PRIX' in t.upper() and 'EN LIGNE ?' in t.upper())
    check('plus de ligne Amazon dans les canaux (Igal, 11 oct. 2026 : « elle ne sert à rien »)', pg.locator('input[data-pc="amazon"]').count() == 0 and 'amazon' not in t.lower())
    check('le lien vers la fiche Amazon reste en haut', pg.locator('a.damz').count() == 1)
    check('aucune erreur JS', not err, err[:2])
    b.close()
print(f'\n{ok} ok, {len(ko)} KO', ko)
