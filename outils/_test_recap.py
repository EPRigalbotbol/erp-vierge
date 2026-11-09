# LE RÉCAP « VENTES PAR CANAL » EN TÊTE DU TABLEAU DE BORD (Igal, 1er nov. 2026 : « un tableau récapitulatif du mois
# dernier avec un graphisme de tous les canaux de vente… où Sam pourra sélectionner son mois, la période, l'année »).
# Ce test protège :
#   1. LE POINT : le récap est le premier bloc du tableau de bord, ouvert sur « Mois dernier » ;
#   2. LE POINT : ses chiffres sont CEUX DE LA PAGE VENTES, canal par canal (chiffre d'affaires, marge nette, flacons) ;
#   3. les règles de marge, vérifiées à la main : commission du canal, port encaissé − coût d'envoi, frais de carte ;
#   4. un remboursement vient en déduction ; Perfume City montre boutique / en ligne ;
#   5. les périodes : ce mois, mois dernier, 30/90 jours, cette année, tout, un mois choisi, une année choisie ; une période
#      vide le dit sans planter ;
#   6. le graphique : une colonne par jour, l'infobulle dit le jour et le canal, la bascule marge / flacons, les chiffres
#      sont aussi dans un tableau ;
#   7. en anglais et en espagnol, plus un mot de français ;
#   8. aucune erreur JS ;
#   9. LE POINT : pas de comparaison avec un mois d'avant le 1er oct. 2026 (septembre n'a pas Amazon) ; dès novembre, la
#      comparaison avec octobre revient d'elle-même (Igal, 3 nov. 2026).
import subprocess, time, socket, json, re, os, datetime
from zoneinfo import ZoneInfo
from playwright.sync_api import sync_playwright
D = '/home/claude/catalogue'
ok = 0; ko = []
def check(n, c, i=''):
    global ok
    if c: ok += 1; print('  ok  ', n)
    else: ko.append(n); print('  KO  ', n, str(i)[:500])
C = json.load(open(D + '/cat.json'))
A = [r for r in C if (r[6] or 0) > 20 and r[0] and r[0].isdigit() and (r[12] or 0) > 0][0]
cle, bc, pa = A[15], A[0], 40.0   # le prix d'achat de la ligne (paAv) : 40 $, pour des calculs à la main
# les dates : « aujourd'hui » est celui du navigateur (Miami) ; on l'impose au navigateur pour que le test soit stable
auj = datetime.date(2026, 11, 15)
def LM(j):   # un jour du mois dernier
    y, m = (auj.year, auj.month - 1) if auj.month > 1 else (auj.year - 1, 12)
    return '%04d-%02d-%02d' % (y, m, j)
y2, m2 = (auj.year, auj.month - 2) if auj.month > 2 else (auj.year - 1, auj.month + 10)
def ligne(q, p, paAv=pa): return {'cle': cle, 'bc': bc, 'ref': 'x', 'q': q, 'p': p, 'paAv': paAv}
F = [
  {'id': 's1', 'num': 'W-1', 'sens': 'vente', 'canal': 'Site perfumestrade.com', 'tiers': 'Ana', 'd': LM(5), 'auto': 'woocommerce', 'port': 12, 'lignes': [ligne(2, 100)]},
  {'id': 'a1', 'num': 'A-1', 'sens': 'vente', 'canal': 'Amazon', 'tiers': 'Bob', 'd': LM(10), 'auto': 'amazon', 'lignes': [ligne(1, 150)]},
  {'id': 'a1r', 'num': 'A-1', 'sens': 'vente', 'canal': 'Amazon', 'tiers': 'Bob', 'd': LM(12), 'auto': 'amazon', 'retour': True, 'refNum': 'A-1', 'lignes': [ligne(-1, 150)]},
  {'id': 'c1', 'num': 'LS-1', 'sens': 'vente', 'canal': 'Caisse Lightspeed', 'tiers': '', 'd': LM(11), 'auto': 'lightspeed', 'paie': {'especes': 40, 'carte': 200}, 'lignes': [ligne(3, 80, 50)]},
  {'id': 'p1', 'num': 'PC-1', 'sens': 'vente', 'canal': 'Perfume City', 'tiers': '', 'd': LM(15), 'auto': 'shopify-pc', '_i': 'fa|shopify-pc|1', 'lignes': [ligne(2, 90)]},
  {'id': 'p2', 'num': 'PC-2', 'sens': 'vente', 'canal': 'Perfume City', 'tiers': '', 'd': LM(16), 'auto': 'shopify-pc', '_i': 'fa|shopify-pc|2', 'lignes': [ligne(1, 90)]},
  {'id': 'g1', 'num': 'PT-1', 'sens': 'vente', 'canal': 'Gros', 'tiers': 'Carmen', 'd': LM(20), 'lignes': [ligne(12, 55)]},
  {'id': 'g0', 'num': 'PT-0', 'sens': 'vente', 'canal': 'Gros', 'tiers': 'Carmen', 'd': '%04d-%02d-08' % (y2, m2), 'lignes': [ligne(5, 55)]},
  {'id': 'sj', 'num': 'W-9', 'sens': 'vente', 'canal': 'Site perfumestrade.com', 'tiers': 'Zoe', 'd': auj.isoformat(), 'auto': 'woocommerce', 'lignes': [ligne(1, 100)]},
]
ORIG = {'shopify-pc|1': 'boutique', 'shopify-pc|2': 'en ligne'}
SESS = """([F,O,lg])=>{ localStorage.clear(); localStorage.setItem('sam-comptes-demo-v1','0');
  localStorage.setItem('sam-session-v1',JSON.stringify({id:'sam',nom:'Sam',role:'patron',depuis:new Date().toISOString()}));
  localStorage.setItem('langue-v1',lg); localStorage.setItem('factures-v1',JSON.stringify(F)); localStorage.setItem('pc-origine-v1',JSON.stringify(O));
  /* 7 nov. 2026 : les commissions réelles (2,9 % + 0,30 $…) sont posées par défaut ; ce test garde ses calculs à la main à 3 % en les réglant lui-même */
  localStorage.setItem('reglages-v1',JSON.stringify({comV4:1,canauxV:3,pcCom3:1,canaux:[{id:'site',nom:'Site perfumestrade.com',com:3},{id:'sitegros',nom:'Site wholesale.perfumestrade.com',base:'pvw',com:3},{id:'amazon',nom:'Amazon',com:15},{id:'perfumecity',nom:'Perfume City',com:3}]})); }"""
FR = re.compile(r"\b(Ventes par canal|Mois dernier|Ce mois|Marge nette|Par canal|Au fil du temps|Tous les canaux|Flacons vendus|Ventes|Voir les chiffres|Chiffre d'affaires|flacons vendus|Journal des ventes|Cette année|panier moyen|remboursement|jour par jour|Aucune vente|Part|Mois|Année|Tout|Canal)\b|[éèêàç]")
s = socket.socket(); s.bind(('127.0.0.1', 0)); port = s.getsockname()[1]; s.close()
srv = subprocess.Popen(['python3', '-m', 'http.server', str(port), '--bind', '127.0.0.1'], cwd=D, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)
try:
    with sync_playwright() as p:
        b = p.chromium.launch(); err = []
        def ouvre(lg='fr', page='tableau.html'):
            ctx = b.new_context(viewport={'width': 1500, 'height': 1100}, timezone_id='America/New_York', locale='fr-FR', reduced_motion='reduce')
            pg = ctx.new_page(); pg.on('pageerror', lambda e: err.append(str(e))); pg.on('dialog', lambda d: d.accept())
            # l'historique de gros réel (donnees/histgros.js) est tenu à l'écart : le test pose le sien (window.__hgTest)
            pg.add_init_script("Object.defineProperty(window,'D_HG',{configurable:true,set(v){ window.__hgReel=v; },get(){ return window.__hgTest||null; }})")
            pg.clock.set_fixed_time(datetime.datetime(auj.year, auj.month, auj.day, 14, 0, tzinfo=ZoneInfo('America/New_York')))
            base = f'http://127.0.0.1:{port}/'
            pg.goto(base + 'accueil.html'); pg.wait_for_timeout(300); pg.evaluate(SESS, [F, ORIG, lg])
            pg.goto(base + page); pg.wait_for_timeout(2800); return pg
        pg = ouvre()
        if os.environ.get('RECAP_SHOT'):
            pg.locator('#recap').screenshot(path=os.environ['RECAP_SHOT'] + '_fr.png')
            pg.emulate_media(color_scheme='dark'); pg.wait_for_timeout(300); pg.locator('#recap').screenshot(path=os.environ['RECAP_SHOT'] + '_fr_sombre.png'); pg.emulate_media(color_scheme='light')
        check('LE POINT — le récap est le PREMIER bloc du tableau de bord', pg.evaluate("()=>{ const r=document.getElementById('recap'); if(!r||!r.children.length) return false; const w=r.parentElement; return [...w.children].find(e=>['recap','kpis','corps'].includes(e.id)).id==='recap'; }"))
        check('il s\'ouvre sur « Mois dernier »', pg.evaluate("()=>document.querySelector('.rc-chip.on').dataset.rc") == 'moisdernier')
        check('le titre dit « Ventes par canal » et le mois', 'VENTES PAR CANAL' in pg.inner_text('#recap h2').upper() and 'octobre' in pg.inner_text('#recap h2').lower(), pg.inner_text('#recap h2'))
        rows = pg.evaluate("()=>{ const P=rcPlage('moisdernier'); const R=rcAgrege(rcLignes(),P.a,P.b); return Object.fromEntries(Object.values(R.G).map(o=>[o.canal,[Math.round(o.ca*100)/100,Math.round(o.mg*100)/100,o.q]])); }")
        check('3. à la main — Gros : 12 flacons à 55 $ = 660 $, marge 660 − 12×40 = 180 $', rows.get('Gros') == [660, 180, 12], rows)
        check('3. à la main — Site : 200 $, marge 200 − 6 (3 %) − 80 + 12 (port) − 8 (envoi) = 118 $', rows.get('Site perfumestrade.com') == [200, 118, 2], rows)
        check('3. à la main — Caisse : 240 $, marge 240 − 150 − 5,20 (2,6 % de 200 $ payés par carte) = 84,80 $', rows.get('Caisse Lightspeed') == [240, 84.8, 3], rows)
        check('4. le remboursement vient en déduction : Amazon 150 − 150 = 0 $, 0 flacon', rows.get('Amazon', [None])[0] == 0 and rows.get('Amazon', [0, 0, None])[2] == 0, rows)
        check('4. Perfume City : 3 flacons, 270 $, marge nette 270 − 8,10 (3 %) − 120 = 141,90 $', rows.get('Perfume City') == [270, 141.9, 3], rows)
        T = pg.inner_text('#recap')
        check('4. Perfume City montre « en boutique » et « en ligne »', 'en boutique' in T and 'en ligne' in T, T[:400])
        nCanaux = pg.evaluate("document.querySelectorAll('#rc-tab tbody tr:not(.tot)').length")
        check('le tableau a une ligne par canal + le total', nCanaux == 5 and pg.locator('#rc-tab tr.tot').count() == 1, nCanaux)
        kp = lambda: pg.inner_text('#recap .ga-tabs').replace('\xa0', ' ').replace('\u202f', ' ')
        # 2. la parité avec Ventes
        pv = ouvre('fr', 'ventes.html')
        dv = pv.evaluate("""([a,b])=>{ const G={}; V.filter(v=>(v.d||'')>=a&&(v.d||'')<=b&&!v.att).forEach(v=>{ const o=G[v.canal]=G[v.canal]||[0,0,0]; o[0]+=v.mt; o[1]+=(v.mg||0); o[2]+=(v.q||0); });
          return Object.fromEntries(Object.entries(G).map(([k,o])=>[k,o.map(x=>Math.round(x*100)/100)])); }""", [LM(1), LM(28)])
        check('2. LE POINT — mêmes chiffres que la page Ventes, canal par canal (chiffre d\'affaires, marge nette, flacons)', dv == rows, {'ventes': dv, 'tableau': rows})
        pv.context.close()
        # 2b. les ventes en gros d'AVANT l'ERP (tableur de Sam) : chiffre d'affaires et flacons, sans marge
        pg.evaluate("j=>{ window.__hgTest={c:['Carmen'],l:{'123':[[j,0,4,50]]}}; rcDessine(); }", LM(3)); pg.wait_for_timeout(300)
        hg = pg.evaluate("()=>{ const tr=[...document.querySelectorAll('#rc-tab tbody tr')].find(t=>/avant l/.test(t.innerText)); return tr?tr.innerText.replace(/\\s+/g,' '):null; }")
        check('2b. « Vente en gros · avant l\'ERP » : 4 flacons, 200 $, marge « — »', hg is not None and '200 $' in hg.replace('\xa0', ' ') and ' 4 ' in hg and '—' in hg, hg)
        check('2b. le chiffre d\'affaires total les compte (1 370 + 200 = 1 570 $)', '1 570 $' in kp(), kp())
        pg.evaluate("()=>{ window.__hgTest=null; rcDessine(); }"); pg.wait_for_timeout(300)
        # 5. les périodes
        kp = lambda: pg.inner_text('#recap .ga-tabs').replace('\xa0', ' ').replace(' ', ' ')
        k0 = kp()
        check('5. mois dernier : le chiffre d\'affaires total est celui des canaux (200 + 0 + 240 + 270 + 660 = 1 370 $)', '1 370 $' in k0, k0)
        check('5. la marge totale : 180 + 118 + 84,80 + 141,90 − 30,50 (Amazon : vente 79,50 puis remboursement −110) = 494 $', '494 $' in k0, k0)
        # 3 nov. 2026 (Igal) : septembre n'a pas les ventes Amazon FBA, donc octobre ne se compare à rien ; novembre se compare à octobre
        inc = lambda: pg.inner_text('#recap .rc-inc').replace('\xa0', ' ') if pg.locator('#recap .rc-inc').count() else ''
        check('LE POINT — octobre 2026 ne se compare PAS à septembre (septembre est incomplet : pas d\'Amazon), même s\'il avait des ventes', 'vs' not in k0 and 'septembre' not in k0, k0)
        check('5. … et le récap dit pourquoi, en nommant septembre et Amazon', 'septembre 2026' in inc() and 'Amazon' in inc(), inc())
        pg.click('[data-rc="cemois"]'); pg.wait_for_timeout(300)
        k1 = kp()
        check('5. « Ce mois » change les chiffres (une seule vente du jour : 100 $)', k1 != k0 and '100 $' in k1, k1)
        check('5. LE POINT — le 15 novembre se compare au 1er–15 octobre, jour pour jour, et l\'étiquette le dit (« vs 1–15 oct. 2026 »)', 'vs' in k1 and '1–15 oct. 2026' in k1 and not inc(), k1 + ' | ' + inc())
        pg.click('[data-rc="tout"]'); pg.wait_for_timeout(300)
        check('5. « Tout » réunit tous les mois : 1 370 + 275 + 100 = 1 745 $', '1 745 $' in kp(), kp())
        check('5. « Tout » : un point par mois sur la courbe (3 mois)', pg.evaluate("()=>document.querySelectorAll('#rc-c .ga-xl').length")==3, pg.evaluate("()=>[...document.querySelectorAll('#rc-c .ga-xl')].map(t=>t.textContent)"))
        pg.select_option('#rc-mois', 'mois:%04d-%02d' % (y2, m2)); pg.wait_for_timeout(300)
        check('5. le choix d\'un mois (il y a deux mois) montre ses 275 $ (5 × 55)', '275 $' in kp(), kp())
        pg.select_option('#rc-an', 'annee:%d' % auj.year); pg.wait_for_timeout(300)
        check('5. le choix d\'une année s\'applique (1 745 $)', pg.evaluate("()=>document.getElementById('rc-an').classList.contains('on')") and '1 745 $' in kp(), kp())
        pg.click('[data-rc="rel:30"]'); pg.wait_for_timeout(200)
        check('5. « 30 jours » : du 17 oct. au 15 nov. → 660 + 100 = 760 $', '760 $' in kp(), kp())
        pg.evaluate("()=>{ RC.sel='mois:1999-01'; rcDessine(); }"); pg.wait_for_timeout(300)
        check('5. une période sans vente le dit, sans planter', 'Aucune vente' in pg.inner_text('#recap'), pg.inner_text('#recap')[:300])
        # 6. la courbe (9 nov. 2026 : les colonnes empilées sont remplacées par une courbe « à la Google »)
        pg.click('[data-rc="moisdernier"]'); pg.wait_for_timeout(300)
        survol = lambda f: (lambda z: (pg.mouse.move(z['x'] + z['width'] * f, z['y'] + z['height'] / 2), pg.wait_for_timeout(150)))(pg.locator('#rc-c .ga-zone').bounding_box())
        tipde = lambda q: q.evaluate("()=>{ const t=document.getElementById('ga-tip'); return t&&t.style.display==='block'?t.innerText:''; }").replace('\xa0', ' ').replace('\u202f', ' ')
        check('6. une courbe pleine (le mois) se dessine, avec l\'onglet « Chiffre d\'affaires » choisi', pg.locator('#rc-c .ga-l').count() >= 1 and pg.locator('.ga-tab.on').get_attribute('data-rcm') == 'ca')
        survol(14 / 30)
        tip = tipde(pg)
        check('6. la bulle dit le jour et le détail par canal (Perfume City le 15, 180 $)', '15' in tip and 'Perfume City' in tip and '180 $' in tip, tip)
        pg.mouse.move(5, 5)
        pg.click('[data-rcm="mg"]'); pg.wait_for_timeout(300); survol(19 / 30)
        check('6. l\'onglet « Marge nette » redessine la courbe (le 20 : 180 $ de Vente en gros)', 'Vente en gros' in tipde(pg) and '180 $' in tipde(pg), tipde(pg))
        pg.mouse.move(5, 5)
        pg.click('[data-rcm="q"]'); pg.wait_for_timeout(300); survol(19 / 30)
        check('6. l\'onglet « Flacons » aussi (12 flacons de gros le 20)', re.search(r'\b12\b', tipde(pg)) is not None, tipde(pg))
        pg.mouse.move(5, 5)
        check('6. les chiffres sont aussi dans un tableau (jour par jour)', pg.locator('#recap details table').count() == 1 and 'jour par jour' in pg.inner_text('#recap details summary'))
        check('6. un bouton par canal, plus « Tous les canaux »', pg.locator('#recap .rc-chs button').count() == 6)
        pg.click('#recap .rc-chs button >> text=Perfume City'); pg.wait_for_timeout(300)
        check('6. choisir un canal ne trace que lui, dans sa couleur', 'rc-c-pc' in (pg.locator('#rc-c .ga-l').first.get_attribute('style') or ''), pg.locator('#rc-c .ga-l').first.get_attribute('style'))
        pg.click('#recap .rc-chs button >> nth=0'); pg.wait_for_timeout(200)
        pg.evaluate("()=>{ RC.metric='ca'; rcDessine(); }")
        check('l\'ancien bloc « D\'où vient l\'argent » est remplacé', "D'où vient l'argent" not in pg.inner_text('body'))
        pg.context.close()
        # 7. anglais et espagnol
        for lg, mots in (('en', ['Sales by channel', 'Last month', 'Net margin', 'By channel', 'All channels', 'See the figures', 'Revenue']), ('es', ['Ventas por canal', 'Mes pasado', 'Margen neto', 'Por canal', 'Todos los canales', 'Ver las cifras', 'Facturación'])):
            pe = ouvre(lg)
            T = pe.inner_text('#recap')
            check(f'7. {lg} — les titres, boutons et légendes sont écrits en {lg}', all(m.lower() in T.lower() for m in mots), [m for m in mots if m.lower() not in T.lower()])
            vu = pe.evaluate("()=>[...document.querySelectorAll('#recap *')].filter(e=>!e.closest('[data-nolang]')&&e.children.length===0&&e.textContent.trim()).map(e=>e.textContent.trim()).concat([...document.querySelectorAll('#recap [title],#recap [aria-label]')].map(e=>(e.title||'')+' '+(e.getAttribute('aria-label')||'')))")
            fr = sorted({t for t in vu if FR.search(re.sub(r'\b(mié|sáb)\b', '', t) if lg == 'es' else t)})
            if lg == 'es': fr = [t for t in fr if t not in ('Canal', 'Mes', 'Total', 'Tout')]   # « Canal » et « Total » s'écrivent pareil en espagnol
            fr = [t for t in fr if not re.fullmatch(r'[\d\s.,$%/—·+-]+', t)]
            check(f'7. LE POINT — {lg} : plus un mot de français dans le récap', not fr, fr)
            zz = pe.locator('#rc-c .ga-zone').bounding_box(); pe.mouse.move(zz['x'] + zz['width'] * 14 / 30, zz['y'] + zz['height'] / 2); pe.wait_for_timeout(200)
            tip = tipde(pe)
            check(f'7. {lg} — la date de l\'infobulle est dans la langue', ('Oct' in tip) if lg == 'en' else ('oct' in tip and 'jue' in tip), tip)
            pe.click('[data-rc="cetteannee"]'); pe.wait_for_timeout(300)
            h2 = pe.inner_text('#recap h2')
            check(f'7. {lg} — « cette année » : la période est dans la langue', ('This year' in h2) if lg == 'en' else ('Este año' in h2), h2)
            pe.context.close()
        check('8. aucune erreur JS', not err, err[:3])
        b.close()
finally:
    srv.terminate()
print(f"\n{ok} ok, {len(ko)} KO", ko)
