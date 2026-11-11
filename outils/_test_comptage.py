# Valider un comptage (Igal, 27 sept. 2026 : « dans la partie inventaire je ne vois pas
# où on peut valider l'inventaire »). La quantité tapée dans « Compté » se valide quand
# on quitte la case. La fonction qui validait avait disparu : rien n'était validé. Ce qui
# est en jeu : le stock prend le chiffre compté, la ligne passe « vérifiée », le journal
# le dit avec le nom — et vider la case défait tout, stock compris. La page dit comment
# on valide, dans les trois langues.
import subprocess, time, socket, json
from playwright.sync_api import sync_playwright
D = '/home/claude/catalogue'
ok = 0; ko = []
def check(n, c, i=''):
    global ok
    if c: ok += 1; print('  ok  ', n)
    else: ko.append(n); print('  KO  ', n, i)
s = socket.socket(); s.bind(('127.0.0.1', 0)); port = s.getsockname()[1]; s.close()
srv = subprocess.Popen(['python3', '-m', 'http.server', str(port), '--bind', '127.0.0.1'], cwd=D, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)
try:
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1500, 'height': 900}); err = []
        pg.on('pageerror', lambda e: err.append(str(e)))
        base = f'http://127.0.0.1:{port}/'
        pg.goto(base + 'accueil.html'); pg.wait_for_timeout(300)
        pg.evaluate("localStorage.setItem('sam-session-v1',JSON.stringify({id:'sam',nom:'Sam',role:'patron',depuis:new Date().toISOString()}));localStorage.setItem('langue-v1','fr')")
        pg.goto(base + 'stock.html'); pg.wait_for_timeout(2500)
        inp = pg.locator('input.cnt').first
        bc = inp.get_attribute('data-bc')
        p0 = pg.evaluate("bc=>{ const p=P.find(x=>x.bc===bc); return {cle:p.cle, th:qteTh(p)}; }", bc)
        inp.fill(str(p0['th'] + 2)); inp.press('Tab'); pg.wait_for_timeout(500)
        m = pg.evaluate("c=>lit('fiches-modifiees-v1',{})[c]||{}", p0['cle'])
        check('LE POINT — quitter la case valide : le stock prend le chiffre compté', m.get('qte') == p0['th'] + 2, m)
        check('la fiche passe « comptage vérifié », signée Sam', m.get('verif') == 'ok' and m.get('verifPar') == 'Sam', m)
        J = pg.evaluate("lit('crm-journal-v1',[]).map(j=>j.lib+'|'+j.u)")
        check('le journal a « comptage physique » et « quantité corrigée par comptage », signés Sam', any(j.startswith('comptage physique|Sam') for j in J) and any(j.startswith('quantité corrigée par comptage|Sam') for j in J), J[-3:])
        tr = inp.locator('xpath=ancestor::tr')
        check("la ligne l'affiche : « Vérifiée »", 'Vérifiée' in tr.inner_text(), tr.inner_text()[:200])
        inp.fill(''); inp.press('Tab'); pg.wait_for_timeout(500)
        m = pg.evaluate("c=>lit('fiches-modifiees-v1',{})[c]||{}", p0['cle'])
        check('vider la case défait tout : stock revenu, plus « vérifiée »', m.get('verif') != 'ok' and pg.evaluate("bc=>qteTh(P.find(x=>x.bc===bc))", bc) == p0['th'], m)
        # 27 sept. : « ça m'a rajouté autre chose, pourquoi ça ne l'enlève pas » — avec des prix
        # de vente importés (colonnes PV), la ligne se repeignait une colonne à côté.
        pg.evaluate("bc=>{ P.forEach(x=>{ if(x.bc===bc){ x.pvr=100; x.pvw=80; } }); rend(true); }", bc)
        inp = pg.locator(f'input.cnt[data-bc="{bc}"]'); tr = inp.locator('xpath=ancestor::tr')
        inp.fill(str(p0['th'] + 2)); inp.press('Tab'); pg.wait_for_timeout(500)
        td = tr.locator('td').all_inner_texts()
        # 11 nov. 2026 (Igal : « quand c'est vérifié, enlève le chiffre théorique ») : une fois compté, « Théorique » = le stock réel, écart 0
        check('colonnes PV présentes, rien de décalé : « Théorique » = le chiffre compté, « Écart » 0', len(td) == 10 and td[3].strip().startswith(str(p0['th'] + 2)) and td[5].strip() in ('0', '—'), td)
        inp.fill(''); inp.press('Tab'); pg.wait_for_timeout(500)
        td = tr.locator('td').all_inner_texts()
        check('… et vider la case remet « — » dans Écart, le capital en place, les PV intacts', td[5].strip() == '—' and '$' in td[7] and td[8].strip() != '—' and td[9].strip() != '—', td)
        check('la page dit comment on valide', 'quittes sa case' in pg.locator('.vhint').inner_text())
        pg.evaluate("localStorage.setItem('langue-v1','en')"); pg.goto(base + 'stock.html'); pg.wait_for_timeout(2500)
        t = pg.locator('.vhint').inner_text()
        check('… et en anglais', 'as soon as you leave its box' in t, t)
        check('aucune erreur JS', not err, err[:3])
        b.close()
finally:
    srv.terminate()
print(f"\n{ok} ok, {len(ko)} KO", ko)
