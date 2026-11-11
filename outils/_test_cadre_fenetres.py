import subprocess, time, socket, json
# LES FENÊTRES DE LA FICHE OUVERTE DEPUIS LE TABLEAU DE BORD (Igal, 31 oct. 2026 : « Remettre en vente, ça bug : il ne se passe rien,
# la case reste »). En mode cadre, .main est cachée ; la fenêtre « Confirmer les prix » y vit : elle s'ouvrait INVISIBLE. Ce test protège :
#   1. LE POINT : depuis le tableau de bord, « Remettre en vente » montre la fenêtre de confirmation, VISIBLE ;
#   2. « OK, enregistrer » remet la fiche en vente (route du prix, republier) ;
#   3. aucune erreur JS.
ok = 0; ko = []
def check(n, c, i=''):
    global ok
    if c: ok += 1; print('  ok  ', n)
    else: ko.append(n); print('  KO  ', n, str(i)[:400])
from playwright.sync_api import sync_playwright
D='/home/claude/catalogue'
C=json.load(open(D+'/cat.json'))
A=[r for r in C if (r[6] or 0)>0 and r[0] and r[0].isdigit() and (r[8] or 0)>(r[12] or 0)>0 and len(r[0])==13][0]
B=[r for r in C if (r[6] or 0)>0 and r[0] and r[0].isdigit() and r[0]!=A[0]][0]
# 11 nov. 2026 : le parfum n'est que sur le gros (retiré) — le test porte sur « Remettre en vente » du gros, rien d'autre ne doit partir
SITE={B[0]:{'g':{'id':2,'q':1,'suivi':True,'pr':50}},'_retires':{'g':{A[0]:{'id':8072,'q':3,'suivi':True,'etat':'instock','nom':'x','pr':None,'ps':None}}},'_maj':{'d':'2026-10-31T08:00:00Z'}}
s=socket.socket(); s.bind(('127.0.0.1',0)); port=s.getsockname()[1]; s.close()
srv=subprocess.Popen(['python3','-m','http.server',str(port),'--bind','127.0.0.1'],cwd=D,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL); time.sleep(1)
try:
  with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1400,'height':850}); err=[]
    pg.on('pageerror',lambda e: err.append(str(e))); pg.on('dialog',lambda d:d.accept())
    env=[]
    pg.route('**/api/o/dasy/site/prix',lambda r:(env.append(r.request.post_data),r.fulfill(status=200,content_type='application/json',body=json.dumps({'ok':True,'apres':{'barre':80,'promo':None}}))))
    base=f'http://127.0.0.1:{port}/'
    pg.goto(base+'accueil.html'); pg.wait_for_timeout(300)
    pg.evaluate("""s=>{ localStorage.clear(); localStorage.setItem('sam-comptes-demo-v1','0');
      localStorage.setItem('sam-session-v1',JSON.stringify({id:'sam',nom:'Sam',role:'patron',depuis:new Date().toISOString()}));
      localStorage.setItem('ck-token','jeton-test'); localStorage.setItem('langue-v1','fr'); localStorage.setItem('site-stock-v1',JSON.stringify(s)); }""",SITE)
    pg.goto(base+'tableau.html'); pg.wait_for_timeout(3000)
    pg.evaluate("()=>{ vusDiff=100000; dessine(); }"); pg.wait_for_timeout(500)
    pg.evaluate("bc=>[...document.querySelectorAll('[data-mel]')].find(x=>x.closest('tr').innerText.includes(bc)).click()",A[0]); pg.wait_for_timeout(4000)
    fr=pg.frames[-1]
    # 11 nov. 2026 : le bouton s'appelle « Mettre en ligne » (data-remet) sur une fiche retirée de la vente
    check('la fiche (dans le tableau de bord) a le bouton « Mettre en ligne » du gros (fiche retirée)', fr.locator('[data-remet="sitegros"]').count()==1)
    fr.locator('[data-remet="sitegros"]').click(); pg.wait_for_timeout(1500)
    vis=fr.evaluate("()=>{ const e=document.getElementById('pxov'); const r=e.getBoundingClientRect(); const cs=getComputedStyle(e); return {on:e.classList.contains('on'),vis:cs.visibility,disp:cs.display,w:r.width}; }")
    check('LE POINT — la fenêtre « Confirmer les prix » est VISIBLE dans la fiche ouverte depuis le tableau de bord', vis['on'] and vis['vis']=='visible' and vis['disp']=='flex' and vis['w']>100, vis)
    fr.locator('#pxok').click(); pg.wait_for_timeout(1500)
    check('« OK, enregistrer » remet la fiche en vente (route du prix, republier)', len(env)==1 and json.loads(env[0]).get('republier') is True, env)
    check('aucune erreur JS', not err, err[:3])
    b.close()
finally: srv.terminate()
print(f"\n{ok} ok, {len(ko)} KO", ko)
