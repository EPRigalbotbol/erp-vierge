# LA RUBRIQUE MAILING (15 nov. 2026 — Igal : « une rubrique Mailing… configurée pour le mailing pour le wholesale et le
# mailing pour le particulier, quelque chose de simple où on pourrait envoyer une offre à chaque secteur » ; avant :
# « savoir quel est le dernier parfum qu'ils ont acheté… leur faire une remise sur ce parfum »). Ce test protège :
#   1. LE POINT — deux secteurs : un grossiste n'est jamais dans Particuliers, un particulier jamais dans Wholesale ;
#   2. LE POINT — un particulier se voit proposer LE DERNIER parfum qu'il a acheté et qui est en stock ;
#   3. LE POINT — le prix offert n'est jamais une perte : il s'arrête au plancher (15 $ de marge, 25 % au plus ; prix d'achat
#      + 5 % en gros) ; sans prix d'achat, pas de remise ;
#   4. exclus : désinscrits, clients Amazon, clientes de Perfume City, clients sans parfum en stock ;
#   5. LE POINT — WhatsApp part UN PAR UN, personnalisé : prénom, parfums, prix, langue du client, ligne STOP ; l'envoi est
#      noté (jamais deux fois la même offre au même client) et signé au Journal ;
#   6. les emails : un fichier pour Klaviyo/Brevo (aucun envoi Gmail en masse) — seulement les adresses valables ;
#   7. réservé à Admin et Patron (un Commercial voit un mur, la ligne du menu est cachée) ; traduit en anglais et en espagnol ;
#      aucune erreur JS.
import subprocess, time, socket, json, math, re
from playwright.sync_api import sync_playwright
D = '/home/claude/catalogue'
ok = 0; ko = []
def check(n, c, i=''):
    global ok
    if c: ok += 1; print('  ok  ', n)
    else: ko.append(n); print('  KO  ', n, str(i)[:600])
C = json.load(open(D + '/cat.json'))
# des parfums réels du catalogue, choisis par leurs chiffres (jamais nommés ici) : en stock, prix, prix de gros, prix d'achat
P = [r for r in C if (r[6] or 0) > 2 and r[15] and (r[7] or 0) > 60 and (r[8] or 0) > 0 and (r[12] or 0) > 0 and (r[12] or 0) < (r[7] or 0) * 0.45]
A, B, G = P[0], P[1], P[2]
# un parfum cher à l'achat : la remise s'arrête au plancher
_pl = lambda r: math.ceil((r[12] + 8 + 0.3 + 15) / (1 - 0.029))
H = [r for r in C if (r[6] or 0) > 0 and r[15] and (r[7] or 0) > 60 and (r[12] or 0) > 0 and (r[8] or 0) > 0 and round(r[7] * 0.75) < _pl(r) < r[7] - 2][0]
Z = [r for r in C if (r[6] or 0) <= 0 and r[15] and (r[7] or 0) > 0][0]   # pas en stock
lig = lambda r, q=1, p=None: {'cle': r[15], 'bc': r[0], 'ref': r[13], 'q': q, 'p': p if p is not None else r[7]}
def vente(i, nom, canal, d, L):
    return {'id': 'f' + str(i), 'num': str(9000 + i), 'sens': 'vente', 'canal': canal, 'd': d, 'h': '12:00', 't': d + 'T17:00:00Z', 'stock': False,
            'tiers': nom, 'lignes': L, 'montant': sum(l['q'] * l['p'] for l in L)}
F = [vente(1, 'Laura Testa', 'Site perfumestrade.com', '2026-07-01', [lig(B)]),          # ancien achat
     vente(2, 'Laura Testa', 'Site perfumestrade.com', '2026-08-15', [lig(Z), lig(A)]),  # dernier achat : Z pas en stock → A
     vente(3, 'Marc Prueba', 'Caisse Lightspeed', '2026-11-01', [lig(H)]),
     vente(4, 'Ana Amazon', 'Amazon', '2026-10-01', [lig(A)]),
     vente(5, 'Kim Cliente', 'Perfume City', '2026-10-01', [lig(A)]),
     vente(6, 'Pedro Stop', 'Site perfumestrade.com', '2026-10-01', [lig(A)]),
     vente(7, 'Zed Rupture', 'Site perfumestrade.com', '2026-10-01', [lig(Z)]),
     vente(8, 'Grossiste Uno', 'Vente en gros', '2026-10-10', [lig(G, 12, G[8]), lig(A, 3, A[8])]),
     vente(9, 'Grossiste Uno', 'Vente en gros', '2026-11-05', [lig(G, 6, G[8])])]
CLI = {'Laura Testa': {'nom': 'Laura Testa', 'email': 'laura@example.com', 'tel': '305 555 0101', 'langue': 'es'},
       'Marc Prueba': {'nom': 'Marc Prueba', 'tel': '+33 6 12 34 56 78', 'langue': 'fr'},
       'Ana Amazon': {'nom': 'Ana Amazon', 'tel': '3055550102'}, 'Kim Cliente': {'nom': 'Kim Cliente', 'tel': '3055550103'},
       'Pedro Stop': {'nom': 'Pedro Stop', 'tel': '3055550104', 'nodiff': True}, 'Zed Rupture': {'nom': 'Zed Rupture', 'tel': '3055550105'},
       'Grossiste Uno': {'nom': 'Grossiste Uno', 'prenom': 'Uno', 'tel': '3055550106', 'langue': 'en'}}
s = socket.socket(); s.bind(('127.0.0.1', 0)); port = s.getsockname()[1]; s.close()
srv = subprocess.Popen(['python3', '-m', 'http.server', str(port), '--bind', '127.0.0.1'], cwd=D, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)
SESS = """([F,CLI,lg,role])=>{ localStorage.clear(); localStorage.setItem('sam-comptes-demo-v1','0');
  localStorage.setItem('sam-session-v1',JSON.stringify({id:'sam',nom:'Sam',role:role,depuis:new Date().toISOString()}));
  localStorage.setItem('langue-v1',lg); localStorage.setItem('factures-v1',JSON.stringify(F)); localStorage.setItem('clients-v1',JSON.stringify(CLI)); }"""
def plancher(r):  # le prix plancher d'un particulier, avec les réglages par défaut (2,9 % + 0,30 $, envoi 8 $)
    return math.ceil((r[12] + 8 + 0.3 + 15) / (1 - 0.029))
try:
    with sync_playwright() as p:
        b = p.chromium.launch(); err = []
        def ouvre(lg='fr', role='patron'):
            ctx = b.new_context(viewport={'width': 1500, 'height': 1000}); ctx.on('page', lambda q: None)
            pg = ctx.new_page(); pg.on('pageerror', lambda e: err.append(str(e)))
            base = f'http://127.0.0.1:{port}/'
            pg.goto(base + 'accueil.html'); pg.wait_for_timeout(300); pg.evaluate(SESS, [F, CLI, lg, role])
            ctx.route('https://wa.me/**', lambda r: r.abort())
            pg.goto(base + 'mailing.html'); pg.wait_for_timeout(2200); return pg, ctx
        pg, ctx = ouvre()
        noms = lambda: pg.evaluate("()=>__ml.mlListe().L.map(o=>o.nom)")
        dl = noms()
        check('LE POINT — Particuliers : Laura (site) et Marc (caisse) y sont, le grossiste n\'y est pas', 'Laura Testa' in dl and 'Marc Prueba' in dl and 'Grossiste Uno' not in dl, dl)
        check('exclus : client Amazon, cliente de Perfume City, désinscrit, client sans parfum en stock', not any(n in dl for n in ('Ana Amazon', 'Kim Cliente', 'Pedro Stop', 'Zed Rupture')), dl)
        t = pg.inner_text('#ml')
        check('les exclusions sont comptées et dites (désinscrits, sans parfum en stock)', re.search(r'1 désinscrits', t) is not None and 'sans parfum en stock' in t, t[:900])
        laura = pg.evaluate("()=>{ const o=__ml.mlListe().L.find(o=>o.nom==='Laura Testa'); return {pf:o.pf.map(x=>x.f.cle), d:o.pf[0].d, nb:o.nb, lg:o.lg}; }")
        check('LE POINT — Laura : le dernier parfum acheté EN STOCK lui est proposé (le plus récent n\'est plus en stock)', laura['pf'] == [A[15]] and laura['d'] == '2026-08-15' and laura['nb'] == 2, laura)
        # le prix : 10 % par défaut, jamais sous le plancher
        pa = pg.evaluate("c=>{ const f=__ml.mlConstruit().find(o=>o.nom==='Laura Testa').pf[0].f; return __ml.mlPrix(f,'detail',10); }", A[15])
        attendu = max(round(A[7] * 0.9), plancher(A)); attendu = min(attendu, A[7])
        check('LE POINT — prix offert à Laura = 10 % de remise, mais jamais sous le plancher', abs(pa['p'] - attendu) < 0.01, [pa, attendu])
        ph = pg.evaluate("()=>{ const f=__ml.CL().find(o=>o.nom==='Marc Prueba').pf[0].f; return __ml.mlPrix(f,'detail',25); }")
        check('LE POINT — parfum cher à l\'achat : 25 % demandés, la remise s\'arrête au plancher (15 $ de marge)', abs(ph['p'] - min(H[7], plancher(H))) < 0.01 and ph['bloque'] and ph['p'] >= plancher(H) - 0.01, [ph, plancher(H)])
        sans = pg.evaluate("()=>{ const f=Object.assign({},__ml.CL().find(o=>o.nom==='Laura Testa').pf[0].f,{pa:null}); return __ml.mlPrix(f,'detail',20); }")
        check('sans prix d\'achat dans l\'ERP : pas de remise', abs(sans['p'] - A[7]) < 0.01, sans)
        cap = pg.evaluate("()=>{ const f=Object.assign({},__ml.CL().find(o=>o.nom==='Laura Testa').pf[0].f,{pa:1}); return __ml.mlPrix(f,'detail',60); }")
        check('jamais plus de 25 % de remise, même si on en tape plus', abs(cap['p'] - round(A[7] * 0.75)) < 0.01, cap)
        # WhatsApp un par un
        pg.locator('#ml-suiv').click(); pg.wait_for_timeout(400)
        u = pg.evaluate("()=>window.__mlDernier||''")
        m = __import__('urllib.parse').parse.unquote(u.split('text=')[1]) if 'text=' in u else ''
        prem = noms()[0]
        exp_tel = '13055550101' if prem == 'Laura Testa' else '33612345678'
        check('LE POINT — « client suivant » ouvre WhatsApp au bon numéro', u.startswith('https://wa.me/' + exp_tel + '?text='), u[:80])
        o = pg.evaluate("()=>{ const o=__ml.CL().find(o=>o.nom==='Laura Testa'); return __ml.mlMessage(o); }")
        check('LE POINT — le message de Laura est en espagnol, avec son prénom, son parfum, le prix et « en lugar de », et la ligne STOP',
              o.startswith('Hola Laura') and A[13].split()[0] in o and 'en lugar de' in o and 'STOP' in o and '$' in o, o)
        pg.locator('#ml-suiv').click(); pg.wait_for_timeout(400)
        u2 = pg.evaluate("()=>window.__mlDernier||''")
        check('le client suivant n\'est pas le même : l\'envoi est noté', u2 != u and 'wa.me/' in u2, [u[:40], u2[:40]])
        check('plus personne à envoyer : le bouton le dit et se grise', pg.locator('#ml-suiv').is_disabled(), pg.inner_text('#ml-suiv'))
        st = pg.evaluate("()=>JSON.parse(localStorage.getItem('mailing-v1'))")
        off = st['offre']['detail']['id']
        check('l\'envoi est gardé (mailing-v1) avec la date et qui l\'a fait', off and set(st['envois'][off].keys()) == {'Laura Testa', 'Marc Prueba'} and st['envois'][off]['Laura Testa']['u'] == 'Sam', st)
        J = pg.evaluate("()=>JSON.parse(localStorage.getItem('crm-journal-v1')||'[]')")
        check('chaque envoi est signé au Journal', sum(1 for j in J if 'Mailing' in j.get('lib', '') and j.get('u') == 'Sam') >= 2, J[-3:])
        check('les lignes envoyées sont marquées « Envoyé le »', pg.locator('.mlt tr.fait').count() == 2 and 'Envoyé le' in pg.inner_text('.mlt'))
        # 15 nov. 2026 : « Pas envoyé » — WhatsApp ouvert mais message pas parti : la ligne redevient à envoyer
        pg.locator('[data-mlnon]').first.click(); pg.wait_for_timeout(300)
        st2 = pg.evaluate("()=>JSON.parse(localStorage.getItem('mailing-v1'))")
        check('LE POINT — « Pas envoyé » : la marque est effacée, la ligne redevient normale, le bouton « client suivant » revient',
              len(st2['envois'][off]) == 1 and pg.locator('.mlt tr.fait').count() == 1 and not pg.locator('#ml-suiv').is_disabled(), [st2['envois'][off], pg.locator('.mlt tr.fait').count()])
        J2 = pg.evaluate("()=>JSON.parse(localStorage.getItem('crm-journal-v1')||'[]')")
        check('« Pas envoyé » est noté au Journal', any('pas envoyé' in j.get('lib', '') for j in J2), J2[-2:])
        pg.locator('#ml-suiv').click(); pg.wait_for_timeout(300)
        # le fichier pour Klaviyo / Brevo
        pg.locator('#ml-csv').click(); pg.wait_for_timeout(300)
        csv = pg.evaluate("()=>window.__mlCsv||''")
        check('le fichier email : en-tête Email + Laura seulement (Marc n\'a pas d\'email)', csv.startswith('Email,FirstName') and 'laura@example.com' in csv and 'Marc' not in csv, csv[:300])
        # Wholesale
        pg.locator('[data-mlsec="gros"]').click(); pg.wait_for_timeout(300)
        gl = noms()
        check('LE POINT — Wholesale : le grossiste y est, Laura n\'y est pas', 'Grossiste Uno' in gl and 'Laura Testa' not in gl, gl[:10])
        g = pg.evaluate("()=>{ const o=__ml.CL().find(o=>o.nom==='Grossiste Uno'); return {pf:o.pf.map(x=>[x.f.cle,x.qt]), msg:__ml.mlMessage(o)}; }")
        check('grossiste : ses parfums les plus achetés en premier (18 puis 3 flacons), au prix de gros', g['pf'] == [[G[15], 18], [A[15], 3]], g['pf'])
        check('grossiste : le message (anglais) liste ses parfums avec le prix de gros, sans « instead of » quand il n\'y a pas de remise',
              g['msg'].startswith('Hello Uno') and ('$' + (str(int(G[8])) if G[8] == int(G[8]) else f"{G[8]:.2f}")) in g['msg'] and 'instead of' not in g['msg'], g['msg'])
        pgw = pg.evaluate("()=>{ const f=__ml.CL().find(o=>o.nom==='Grossiste Uno').pf[0].f; return __ml.mlPrix(f,'gros',25); }")
        check('LE POINT — grossiste : jamais sous le prix d\'achat + 5 %', pgw['p'] >= round(G[12] * 1.05, 2) - 0.01 and pgw['p'] <= G[8] + 0.001, [pgw, G[12]])
        # la nouvelle offre remet les compteurs à zéro
        pg.locator('[data-mlsec="detail"]').click(); pg.wait_for_timeout(200)
        pg.once('dialog', lambda d: d.accept()); pg.locator('#ml-neuve').click(); pg.wait_for_timeout(300)
        check('« Nouvelle offre » : tout le monde peut recevoir la nouvelle', not pg.locator('#ml-suiv').is_disabled() and pg.locator('.mlt tr.fait').count() == 0)
        # désinscrire depuis la Mailing : la fiche client garde nodiff
        pg.once('dialog', lambda d: d.accept()); pg.locator('[data-mlstop]').first.click(); pg.wait_for_timeout(300)
        nd = pg.evaluate("()=>Object.values(JSON.parse(localStorage.getItem('clients-v1'))).filter(c=>c.nodiff).map(c=>c.nom)")
        check('« Désinscrire » : le client sort de la liste et sa fiche est marquée (même case que la liste de diffusion)', len(nd) == 2 and len(noms()) == 1, [nd, noms()])
        ctx.close()
        # Commercial : un mur, et la ligne du menu cachée
        pg, ctx = ouvre(role='commercial')
        check('Commercial : un mur, pas de liste', pg.locator('.mur').count() == 1 and pg.locator('#ml').count() == 0)
        check('Commercial : la ligne « Mailing » est cachée dans le menu', not pg.locator('.side nav a.nv[href^="mailing.html"]').is_visible())
        ctx.close()
        pg, ctx = ouvre()
        check('Patron : la ligne « Mailing » est dans le menu', pg.locator('.side nav a.nv[href^="mailing.html"]').is_visible())
        ctx.close()
        for lg, mots, fr in (('en', ['The offer', 'Retail customers', 'Fragrances offered and offer price', 'File for Klaviyo or Brevo'], ['Particuliers', "L'offre", 'prix offert', 'Les clients']),
                             ('es', ['La oferta', 'Particulares', 'Perfumes ofrecidos y precio ofrecido', 'Archivo para Klaviyo o Brevo'], ['Particuliers', "L'offre", 'prix offert', 'Les clients'])):
            pg, ctx = ouvre(lg=lg); t = pg.evaluate("()=>document.querySelector('.main').textContent")
            check(f'{lg} : la page est traduite', all(x in t for x in mots) and not any(x in t for x in fr), [x for x in mots if x not in t] + [x for x in fr if x in t])
            pg.locator('#ml-suiv').click(); pg.wait_for_timeout(300)
            nn = pg.locator('[data-mlnon]').first.inner_text() if pg.locator('[data-mlnon]').count() else ''
            check(f'{lg} : le bouton « Pas envoyé » est traduit', nn == {'en': 'Not sent', 'es': 'No enviado'}[lg], nn)
            ctx.close()
        check('aucune erreur JS', not err, err[:3])
        b.close()
finally:
    srv.terminate()
print(f'\n{ok} ok, {len(ko)} KO', ko); raise SystemExit(1 if ko else 0)
