# Audit « clic partout » : on ouvre chaque page en anglais, on clique sur chaque
# bouton (fenêtres, onglets, formulaires), et on relève ce qui reste en français.
# L'audit au chargement ne voit pas les fenêtres modales : celui-ci, si.
import json, pathlib, re
from playwright.sync_api import sync_playwright
exec(open('/home/claude/catalogue/_audit_langues.py').read().split('def audit(')[0])   # FR, IGNORE, JS_COLLECTE, PAGES, SESS, D

restes={}
def _capture(pg):
    try: L=pg.evaluate(JS_COLLECTE)
    except Exception: return []
    return [x for x in L if not x['traduit'] and not IGNORE.match(x['t']) and FR.search(x['t'])
            and 'select#fb' not in x['ou'] and 'td.chg' not in x['ou']]
def releve(pg, page, ou):
    L=_capture(pg)
    if not L: return
    # un second releve plus tard : ce qui n'y est plus etait juste en cours de traduction
    pg.wait_for_timeout(900)
    encore={x['t'] for x in _capture(pg)}
    L=[x for x in L if x['t'] in encore]
    for x in L:
        t=x['t']; k=t
        if k not in restes: restes[k]={'page':page,'ou':x['ou'],'apres':ou,'vis':x['vis']}

with sync_playwright() as p:
    b=p.chromium.launch()
    for page in PAGES:
        if page=='accueil.html': continue
        pg=b.new_page(viewport={'width':1500,'height':1000})
        pg.goto('file://'+str(D/'accueil.html')); pg.wait_for_timeout(400)
        pg.evaluate(SESS); pg.evaluate("localStorage.setItem('langue-v1','en')")
        pg.goto('file://'+str(D/page)); pg.wait_for_timeout(2000)
        pg.evaluate("window.confirm=()=>false; window.alert=()=>{}; window.prompt=()=>null; window.print=()=>{};")
        n=pg.evaluate("document.querySelectorAll('button, .btn, [data-t], details summary, .tabs button').length")
        for i in range(min(n,60)):
            try:
                ok=pg.evaluate(f"""(()=>{{ const L=[...document.querySelectorAll('button, .btn, [data-t], details summary, .tabs button')];
                   const e=L[{i}]; if(!e) return 'fin'; const r=e.getBoundingClientRect(); if(!r.width||!r.height) return 'cache';
                   if(/sortir|raz|supprimer|effacer|vider|fermer l|quitter|chg|finidemo/i.test(e.id+' '+e.className+' '+e.textContent)) return 'evite';
                   if(e.closest('#lgsel, .lg')) return 'evite';
                   e.click(); return 'ok'; }})()""")
            except Exception: ok='err'
            if ok!='ok': continue
            pg.wait_for_timeout(350)
            if not pg.url.endswith(page):
                pg.goto('file://'+str(D/page)); pg.wait_for_timeout(1500)
                pg.evaluate("window.confirm=()=>false; window.alert=()=>{}; window.prompt=()=>null; window.print=()=>{};")
                continue
            releve(pg, page, f'clic #{i}')
            try: pg.keyboard.press('Escape')
            except Exception: pass
            pg.wait_for_timeout(120)
        pg.close()
    b.close()
out=D/'_audit_clics.json'; out.write_text(json.dumps(restes,ensure_ascii=False,indent=1),encoding='utf-8')
import collections
print(len(restes),'restes apres clics'); print(collections.Counter(v['page'] for v in restes.values()))
