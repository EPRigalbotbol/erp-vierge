# LA FEUILLE DES NOUVEAUX ARRIVAGES NE SE TASSE PLUS (Igal, 10 nov. 2026, PDF de 12 parfums à l'appui : « ça écrase la page complètement
# en bas, tout est tassé… ça ne me dérange pas qu'il y ait deux pages, mais je veux que ça reste propre », « les titres un petit peu
# plus gros » ; et pour WhatsApp : « je la reçois floue, d'autres ne voient même pas l'image »). Ce test protège :
#   1. LE POINT — 12 parfums : deux pages (8 + 4), rien ne dépasse le pied de page, le cadre « Prix sur demande » ne recouvre rien ;
#   2. 8 parfums tiennent sur une page ; 20 parfums : trois pages, toujours sans rien de tassé ; des noms très longs non plus ;
#   3. les noms des parfums sont écrits plus gros qu'avant (19 px au lieu de 16,5) ;
#   4. LE POINT — l'aperçu pour WhatsApp est un JPEG léger (moins de 300 Ko), en plus du PNG ; les deux sont déposés au cockpit.
import pathlib, subprocess, time, socket, json, sys
from playwright.sync_api import sync_playwright
D = pathlib.Path('/home/claude/catalogue')
ok = 0; ko = []
def check(n, c, i=''):
    global ok
    if c: ok += 1; print('  ok  ', n)
    else: ko.append(n); print('  KO  ', n, str(i)[:500])
s = socket.socket(); s.bind(('127.0.0.1', 0)); port = s.getsockname()[1]; s.close()
srv = subprocess.Popen(['python3', '-m', 'http.server', str(port), '--bind', '127.0.0.1'], cwd=str(D), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)
CAT = json.load(open(D / 'cat.json'))
A = [r for r in CAT if r[0] and str(r[0]).isdigit() and r[1] and r[2] and (D / 'photos' / (str(r[0]) + '.webp')).exists()][:20]
ITEMS = [{'k': str(r[0]), 'bc': str(r[0]), 'nom': r[1], 'marque': r[2], 'ml': r[3], 'type': r[4], 'genre': r[5], 'photo': f'photos/{r[0]}.webp'} for r in A]
JS = """async ([items,lg])=>{ if(typeof arrPdf!=='function') await new Promise((ok,ko)=>{ const s=document.createElement('script'); s.src='lib/arrivage.js'; s.onload=ok; s.onerror=ko; document.head.appendChild(s); });
  const r=await arrPdf(items,lg); const b64=async b=>{ const u=new Uint8Array(await b.arrayBuffer()); let t=''; for(let i=0;i<u.length;i+=8192) t+=String.fromCharCode.apply(null,u.subarray(i,i+8192)); return btoa(t); };
  return {pages:r.pages,tasse:r.tasse,png:r.png?r.png.size:0,jpg:r.jpg?r.jpg.size:0,tjpg:r.jpg?r.jpg.type:'',pdf:(window.__garde?await b64(r.pdf):''),ap:(window.__garde?await b64(r.jpg):'')}; }"""
try:
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1456, 'height': 900}); err = []
        pg.on('pageerror', lambda e: err.append(str(e)))
        pg.goto(f'http://127.0.0.1:{port}/accueil.html'); pg.wait_for_timeout(300)
        pg.evaluate("()=>{ localStorage.setItem('sam-session-v1', JSON.stringify({id:'sam',nom:'Sam',role:'patron',depuis:new Date().toISOString()})); localStorage.setItem('reglages-v1',JSON.stringify({fact:{enseigne:'Perfumes Trade',tel:'+1 (786) 555-0100',email:'contact@example.com',adresse:'1 Main street, Miami, FL'}})); }")
        pg.goto(f'http://127.0.0.1:{port}/catalogue.html'); pg.wait_for_timeout(2500)
        if len(sys.argv) > 1: pg.evaluate("()=>{ window.__garde=1; }")
        r = pg.evaluate(JS, [ITEMS[:12], 'fr'])
        if len(sys.argv) > 1:
            import base64; open(sys.argv[1] + '.pdf', 'wb').write(base64.b64decode(r['pdf'])); open(sys.argv[1] + '.jpg', 'wb').write(base64.b64decode(r['ap']))
        check('LE POINT — 12 parfums : deux pages, et rien de tassé (aucune carte ni le cadre « Prix sur demande » ne dépasse le pied de page)', r['pages'] == 2 and r['tasse'] is False, {k: r[k] for k in ('pages', 'tasse')})
        check('LE POINT — l\'aperçu pour WhatsApp : un JPEG léger (moins de 300 Ko), en plus du PNG', r['tjpg'] == 'image/jpeg' and 20000 < r['jpg'] < 300000 and r['png'] > 0, {k: r[k] for k in ('png', 'jpg', 'tjpg')})
        r8 = pg.evaluate(JS, [ITEMS[:8], 'en']); r20 = pg.evaluate(JS, [ITEMS[:20], 'es'])
        check('8 parfums : une seule page, propre', r8['pages'] == 1 and r8['tasse'] is False, r8['pages'])
        check('20 parfums : trois pages, propres', r20['pages'] == 3 and r20['tasse'] is False, r20['pages'])
        longs = [dict(x, nom=x['nom'] + ' Edition Limitee Collector Intense Absolu Extreme') for x in ITEMS[:12]]
        rl = pg.evaluate(JS, [longs, 'fr'])
        check('des noms très longs (trois lignes) : la page retire une rangée plutôt que de tasser', rl['tasse'] is False and rl['pages'] >= 2, rl['pages'])
        css = (D / 'lib' / 'arrivage.js').read_text(encoding='utf-8')
        check('les noms des parfums sont écrits plus gros (19 px)', '.an{font-family:ArrSerif;font-weight:600;font-size:19px' in css)
        check('la fenêtre dit d\'attendre l\'image avant d\'envoyer, dans les trois langues', 'attends que l\'image de la liste apparaisse' in css and 'wait until the picture of the list appears' in css and 'espera a que la imagen de la lista aparezca' in css)
        check('aucune erreur JS', not err, err[:3])
        b.close()
finally:
    srv.terminate()
print(f'\n{ok} ok, {len(ko)} KO', ko); raise SystemExit(1 if ko else 0)
