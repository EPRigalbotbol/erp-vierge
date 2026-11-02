# Audit TOTAL des langues : chaque page, en anglais et en espagnol, avec des données
# qui ressemblent à celles de Sam (dont les vraies phrases du journal), et on CLIQUE
# tout ce qui est cliquable (curseur « main ») : lignes, tuiles, onglets, boutons,
# fiches. Après chaque clic on relève le texte visible, les options des listes, et
# les messages (alert/confirm/prompt). Tout mot français restant est noté.
import json, re, sys, time, socket, subprocess, pathlib, random
from playwright.sync_api import sync_playwright
D = pathlib.Path('/home/claude/catalogue')
OUT = pathlib.Path('/tmp')
LG = sys.argv[1] if len(sys.argv) > 1 else 'en'
PAGES = sys.argv[2].split(',') if len(sys.argv) > 2 and sys.argv[2] else ['tableau','catalogue','stock','ventes','expeditions','factures','quotes','etude','fournisseurs','clients','journal','acces','reglages','messages','connecteurs','inventaire_pc','retail','accueil']
MAXCLICS = int(sys.argv[3]) if len(sys.argv) > 3 else 140
CAT = json.load(open(D / 'cat.json'))
random.seed(3)
stk = [r for r in CAT if (r[6] or 0) > 0 and r[0]]
P = random.sample(stk, 40)
def ref(r): return ((r[2] or '') + ' ' + (r[1] or '') + (' ' + r[4] if r[4] else '')).strip()
CANAUX = [('lightspeed','Caisse Lightspeed'),('woocommerce','Site perfumestrade.com'),('amazon','Amazon'),('woocommerce-gros','Site wholesale.perfumestrade.com'),('','Boutique'),('','Gros')]
ENT = {"raison":"DASY LLC","enseigne":"Perfumes Trade","adresse":"2035 NW 23rd Ave, Miami FL","tel":"+1 786","email":"x@y.com","taxid":"1","taux":7,"carte":2.6,"zelle":"Zelle : x","prefixe":"PT","conditions":"Payment on receipt.","exo":"Sale for resale"}
FACT = []
for i, r in enumerate(P[:30]):
    src, canal = CANAUX[i % len(CANAUX)]
    q = 1 + i % 3; p = float(r[7] or 50)
    f = {'id':'f%d'%i,'num':['b8598ea5-7a8e-ab57-11f1-%012x'%i,'%d'%(20600+i),'114-%07d-%07d'%(i*7919,i*104729),'%d'%(22900+i),'V2609%02d-%03d'%(i%28+1,i),'V2609%02d-%03d'%(i%28+1,i)][i%6],
         'sens':'vente','canal':canal,'tiers':['','Maria Lopez','','Taylor Duncan','Carmen','Javier'][i%6],'d':'2026-09-%02d'%(1+i%25),'h':'%02d:%02d'%(9+i%10,i%60),
         'lignes':[{'cle':r[15],'bc':r[0],'ref':ref(r),'q':q,'p':p,'qAv':[5,0,2][i%3],'qAp':[5-q,0,max(0,2-q)][i%3],'paAv':float(r[12] or 20),'manque':[None,q,max(0,q-2) or None][i%3]}],
         'montant':p*q,'stock':True,'par':'Sam','t':'2026-09-%02dT14:00:00Z'%(1+i%25)}
    if src: f['auto']=src; f['export']=canal
    else: f['manuel']=True
    f['doc']={'type':'facture','num':'PT-2026-%04d'%(i+1),'pmode':['caisse','enligne','zelle','carte','especes','virement'][i%6],'pstat':['paye','partiel','impaye'][i%3],'fiscal':['taxable','exempt'][i%2],'langue':'en','emis':f['t'],'entete':ENT,'auto':bool(src),
              'note':'Prix du canal, taxes comprises' if src else '','sousTotal':p*q,'remType':'pct','remVal':0,'remise':0,'remPct':0,'remLib':'','base':p*q,'fraisPct':0,'frais':0,'taux':7 if i%4==0 else 0,'taxe':round(p*q*0.07,2) if i%4==0 else 0,'total':round(p*q*(1.07 if i%4==0 else 1),2),'regle':p*q if i%3==0 else (p*q/2 if i%3==1 else 0),'reste':0 if i%3==0 else (p*q/2 if i%3==1 else p*q)}
    if i % 5 == 0: f['note'] = '1 ligne hors parfum (sac, port…) — pas dans le stock'
    FACT.append(f)
# des devis (cotes)
for i, r in enumerate(P[30:34]):
    FACT.append({'id':'d%d'%i,'num':'DV-2026-%04d'%(i+1),'sens':'vente','canal':'Gros','tiers':'Carmen','d':'2026-09-2%d'%i,'lignes':[{'cle':r[15],'bc':r[0],'ref':ref(r),'q':6,'p':float(r[8] or 30),'paAv':float(r[12] or 20)}],
                 'montant':6*float(r[8] or 30),'stock':False,'par':'Sam','t':'2026-09-2%dT10:00:00Z'%i,'devis':True,
                 'doc':{'type':'devis','num':'DV-2026-%04d'%(i+1),'pstat':'impaye','fiscal':'exempt','langue':'en','entete':ENT,'sousTotal':1,'base':1,'total':6*float(r[8] or 30),'regle':0,'reste':0,'statut':['cree','termine','archive','cree'][i]}})
# des remboursements
FACT.append({'id':'r1','num':'22903-R1','sens':'vente','retour':True,'refId':'f3','refNum':FACT[3]['num'],'canal':FACT[3]['canal'],'tiers':'Taylor Duncan','d':'2026-09-25','lignes':[dict(FACT[3]['lignes'][0],q=-1)],'montant':-FACT[3]['lignes'][0]['p'],'stock':True,'mode':'carte','motif':'autre','note':'','par':'Josh','t':'2026-09-25T16:35:12Z'})
FACT.append({'id':'r2','num':'20601-R1','sens':'vente','retour':True,'refId':'','refNum':'20777','canal':'Site perfumestrade.com','tiers':'Inconnu','d':'2026-09-24','lignes':[dict(FACT[1]['lignes'][0],q=-1)],'montant':-50,'stock':False,'mode':'aucun','motif':'annulation','note':"Site perfumestrade.com — vente d'origine inconnue ici, stock inchangé",'par':'Sam','t':'2026-09-24T16:35:12Z','auto':'woocommerce'})
FILE = [
 {'_i':'amazon|q1','src':'amazon','num':'113-1111111-2222222','d':'2026-09-25','h':'13:00','lieu':'Amazon','client':'','total':149,'lignes':[{'bc':'100000000001','sku':'A100000000001','des':'SOME PERFUME COLOGNE SPRAY','q':1,'p':149}]},
 {'_i':'woocommerce|q2','src':'woocommerce','num':'20999','d':'2026-09-25','h':'14:57','lieu':'Site perfumestrade.com','client':'William Royer','total':45,'lignes':[{'bc':'9999999999999','des':'Unknown Perfume 3.4 oz','q':1,'p':45}]},
 {'_i':'woocommerce|q3|r','src':'woocommerce','num':'20601','annule':True,'motif':'retour','d':'2026-09-25','lignes':[{'bc':'SKU-X','des':'Some perfume','q':-1,'p':50}]}]
EXP = [{'_i':'amazon|e%d'%i,'src':['amazon','woocommerce','woocommerce-gros'][i%3],'num':['114-4369883-95954%02d'%i,'207%02d'%i,'229%02d'%i][i%3],'client':['','Ted Pickul','Distribuidora Cap 2018 LLC'][i%3],
        'd':'2026-09-2%d'%(i%6),'h':'1%d:2%d'%(i%10,i%10),'recu':'2026-09-25T18:28:01Z','total':29.9,'lieu':['Amazon','Site perfumestrade.com','Site wholesale.perfumestrade.com'][i%3],
        'lignes':[{'cle':r[15],'bc':r[0],'des':r[1],'q':1,'p':float(r[7] or 50),'ref':ref(r)}],'montant':float(r[7] or 50),'arrive':'2026-09-25T18:28:30Z',
        'statut':'attente' if i<6 else 'expedie', **({} if i<6 else {'exp':{'d':'2026-09-24','t':'2026-09-24T15:00:00Z','par':'Josh','suivi':'1Z999','transporteur':'UPS'},'factId':'f%d'%i})} for i, r in enumerate(P[:9])]
LIBS = ["langue de l'écran","fiche client modifiée","3 vente du site ou de la caisse enregistrée automatiquement — 3 ligne(s)","menu réorganisé",
 "4 ventes du site ou de la caisse enregistrées automatiquement — 5 ligne(s), 2 en attente (référence inconnue)","vendu à découvert — 5 flacon(s) de plus que le stock compté, sur 1 ligne(s)",
 "2 commandes à expédier reçues (Amazon, Site perfumestrade.com) — le stock sortira à l'expédition","1 commande à expédier reçue (Amazon) — le stock sortira à l'expédition",
 "accès + mot de passe provisoire envoyés — Josh","connexion","majoration — Boutique","message préparé — Promotion","mot de passe remis — Josh","devis DV-2026-0003 — Carmen",
 "règlement : Partielle","montant réglé : 120 $","statut de comptage","prix changés sur le site perfumestrade.com","vente saisie à la main — Boutique — V260925-001",
 "message envoyé à Josh","mot de passe provisoire créé pour l'envoi — Josh","déconnexion","devis DV-2026-0004 transformé en facture PT-2026-0051 — Carmen","facture annulée V260920-002 — Carmen",
 "1 vente de la file ignorée","mode de règlement : Espèces","prix Site perfumestrade.com (manuel)","Google Sheet du 3 septembre — écarts installés avec le catalogue",
 "facture PT-2026-0040 — Gros — Saidmar — V260920-004 — Zelle, reste dû 120,5 $","paiement reçu sur la facture PT-2026-0040 — $120.5 en Espèces — facture réglée",
 "mise à jour du stock depuis un tableur","remboursement 20777-R1 — commande annulée, vente d'origine inconnue, stock inchangé (automatique)",
 "6 messages de canal sans produit lisible (Amazon, Caisse Lightspeed) retirés de la file — n° 1-2-3, 4-5-6","1 vente sans parfum (bags ×1) — rien à sortir du stock, retirée de la file",
 "remboursement 22966-R1 — autre, rendu en carte","commande 20701 expédiée le 24/09/2026 (Site perfumestrade.com) — facture faite, stock sorti",
 "commande 20702 retirée des expéditions sans être expédiée — doublon — rien n'est sorti du stock","annonces Amazon importées — 90 code(s) de Sam reliés à un vrai produit"]
ACTS = ['reglage','client','vente','reglage','vente','stock','vente','vente','acces','acces','reglage','contact','acces','vente','client','client','verif','prix','vente','message','acces','acces','vente','annulation','vente','client','prix','import','vente','vente','import','annulation','vente','vente','annulation','vente','annulation','vente']
JOU = [{'t':'2026-09-%02dT1%d:%02d:00Z'%(1+i%25,i%10,i%60),'u':['Sam','Josh','Igal'][i%3],'act':ACTS[i%len(ACTS)],'lib':LIBS[i%len(LIBS)],'ref':P[i%40][15] if i%4==0 else '','av':'10' if i%3==0 else None,'ap':'12' if i%3==0 else None,'n':1,'det':[{'bc':P[i%40][0],'ref':ref(P[i%40]),'av':3,'ap':2}] if i%5==0 else []} for i in range(len(LIBS)*2)]
MOD = {r[15]:{'qte':2} for r in P[:10]}
SITE = {str(r[0]):{'d':{'id':1000+i,'q':(r[6] or 0)+(i%3),'suivi':True,'etat':'instock','nom':'x','pr':float(r[7] or 50)+10,'ps':float(r[7] or 50)},'g':{'id':2000+i,'q':0,'suivi':True,'etat':'outofstock','nom':'x','pr':float(r[8] or 30),'ps':None}} for i, r in enumerate(P)}
HIST = {r[15]:[{'d':'2026-0%d-1%d'%(1+k,k),'p':float(r[12] or 20)*(1+k/20),'f':'MTZ','q':6} for k in range(3)] for r in P[:20]}
ETU = '\n'.join(f"{r[0]}\t{ref(r)} EAU DE PARFUM SPRAY\t3\t{round(float(r[12] or 20)*0.95,2)}" for r in P[:15]) + '\n123456789012\tUNKNOWN PRODUCT\t2\t19.5'
CLI = {'Carmen':{'nom':'Carmen','tel':'+1 305 555 0101','email':'carmen@x.com','maj':'2026-09-20T10:00:00Z','taxe':'resale'},'Maria Lopez':{'nom':'Maria Lopez','email':'m@x.com','maj':'2026-09-21T10:00:00Z'}}
REG = {"seuilQte":3,"margeMin":10,"canaux":[{"id":"boutique","nom":"Boutique","maj":1,"com":0},{"id":"site","nom":"Site perfumestrade.com","maj":0,"com":3},{"id":"sitegros","nom":"Site wholesale.perfumestrade.com","base":"pvw","maj":0,"com":3},{"id":"amazon","nom":"Amazon","maj":18,"com":15},{"id":"perfumecity","nom":"Perfume City","maj":0,"com":0}],
       "fact":ENT,"exped":{"amazon":True,"woocommerce":True,"woocommerce-gros":True}}
MSG = [{'id':'m1','de':'josh','a':'sam','t':'2026-09-25T10:00:00Z','x':'Hello Sam','lu':False}]
FRN = [{'nom':'MTZ','tel':'+1 305','email':'mtz@x.com'},{'nom':'Donna','email':'d@x.com'}]

# ---- ce qui trahit du français ----
COMMUNS_ES = {'son','mes','sus','nos','te','ton','sin','con','ha','hay','del','al','ya','muy','pero','como','de','la','en','a','que','no','se','con','por','para','es','un','ha','las','los','o','y','e','si','su','al','del','lo','me','le','te','mi','tu'}
MOTS_FR = set('''le la les des du de au aux un une et est sont pour avec sans dans sur pas ne ce cette ces cet qui que quoi dont où ou mais donc car plus moins très tout tous toutes aucun aucune rien déjà encore ici hier demain aujourd jour jours mois semaine semaines année
vente ventes achat achats prix marge marges facture factures devis cote cotes fiche fiches flacon flacons parfum parfums fournisseur fournisseurs client clients commande commandes ligne lignes quantité quantités montant montants reste payé payée payées réglé réglée remboursement remboursements remboursé remboursée remise taxe frais canal canaux caisse
enregistrer enregistré enregistrée enregistrés enregistrées modifier modifié supprimer annuler annulé annulée fermer ouvrir voir afficher masquer choisir envoyer envoyé imprimer importer rechercher chercher trier filtrer ajouter garder retirer déposer valider confirmer continuer retour
nouveau nouvelle nouveaux nouvelles dernier dernière premier première autre autres même tel telle chaque celui celle ceux leur leurs notre votre nos vos mon ma mes ton ta tes son sa ses
stock inventaire réglages tableau bord journal accès compte comptes rôle rôles utilisateur identifiant mot passe entrepôt patron comptable commercial étude brouillon aperçu chargement expédition expéditions expédier expédiée expédiées envoi livraison
aussi alors avant après pendant depuis jusqu toujours jamais souvent peut peuvent doit doivent faut fait faire être avoir été avez avons suis es sera seront était
oui non merci bonjour
'''.split())
FR_ACCENTS_EN = re.compile(r"[éèêàçùûôîâœëïÉÈÊÀÇ]")
FR_ACCENTS_ES = re.compile(r"[èêàçùûôîâœëïÈÊÀÇ]")
MOT = re.compile(r"[A-Za-zÀ-ÿ']+")
NOMS = set()
for r in CAT:
    for x in (r[1], r[2], r[13], ref(r), ((r[2] or '')+' '+(r[1] or '')).strip()):
        if x: NOMS.add(str(x).strip().lower())
DONNEES = {'es','en','fr','carmen','maria lopez','taylor duncan','javier','ted pickul','distribuidora cap 2018 llc','william royer','sam','josh','igal','mtz','donna','boutique','perfume city','saidmar','promotion','habibi','inconnu'}
def francais(t):
    tl = t.lower().strip()
    if tl in NOMS or tl in DONNEES: return False
    acc = (FR_ACCENTS_EN if LG == 'en' else FR_ACCENTS_ES).search(t)
    mots = [m.lower().strip("'") for m in MOT.findall(re.sub(r'\bB0[A-Z0-9]{8}\b|\b[A-Z]{1,3}-?\d[\w-]*', ' ', t))]
    fr = [m for m in mots if m in MOTS_FR and not (LG == 'es' and m in COMMUNS_ES)]
    if LG == 'en': fr = [m for m in fr if m not in ('stock','client','clients','commande','ce','ne','ou','journal','document','plus','commercial','patron','facture','date','note','total','aucun')]
    if LG == 'es': fr = [m for m in fr if m not in ('stock','ne','canal','canaux','total','marca','prix','client')]
    # élision française : l', d', qu', n'
    elis = re.search(r"\b(l|d|qu|n|s|c|j)'[a-zà-ÿ]", t, re.I)
    return bool(acc or fr or elis)

JS_TEXTES = r"""(() => {
  const SAUT={SCRIPT:1,STYLE:1,TEXTAREA:1,CODE:1,PRE:1,NOSCRIPT:1};
  const DATA='.lnm,.lmq,.nom,.nm,.mq,.marque,.produit,.bc,.lbc,.lid,.pd,td.ref,[data-nolang],.pdt b,.ref b';
  const vis=el=>{ if(!el) return false; if(!el.getClientRects().length) return false; const s=getComputedStyle(el); return s.visibility!=='hidden'&&s.display!=='none'&&+s.opacity!==0; };
  const out=[]; const it=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT); let n;
  while((n=it.nextNode())){ const el=n.parentNode; if(!el||SAUT[el.nodeName]) continue; if(el.closest&&el.closest(DATA)) continue;
    const t=(n.nodeValue||'').replace(/\s+/g,' ').trim(); if(!t||!/[A-Za-zÀ-ÿ]{2}/.test(t)) continue; if(!vis(el)) continue;
    let b=el.closest('p,li,td,th,button,label,h1,h2,h3,h4,div,span,a,option,summary')||el;
    out.push({t, bloc:(b.innerText||'').replace(/\s+/g,' ').trim().slice(0,220), ou:(el.id?'#'+el.id:el.nodeName.toLowerCase()+(typeof el.className==='string'&&el.className?'.'+el.className.split(' ')[0]:''))}); }
  document.querySelectorAll('select').forEach(s=>{ if(!vis(s)||s.closest(DATA)||s.options.length>30) return; [...s.options].forEach(o=>{ const t=(o.textContent||'').trim(); if(t) out.push({t,bloc:'<option> de #'+(s.id||'?'),ou:'option'}); }); });
  document.querySelectorAll('[placeholder],[title]').forEach(el=>{ if(!vis(el)||el.closest(DATA)) return; ['placeholder','title'].forEach(a=>{ const t=(el.getAttribute(a)||'').trim(); if(t&&/[A-Za-zÀ-ÿ]{2}/.test(t)) out.push({t,bloc:'['+a+']',ou:a}); }); });
  (window.__MSG||[]).forEach(t=>out.push({t,bloc:'<message>',ou:'dialog'})); window.__MSG=[];
  return out; })()"""
JS_CLIQUABLES = r"""((racine) => { racine=racine?document.querySelector(racine):document.body; if(!racine) return [];
  const vis=el=>{ const r=el.getBoundingClientRect(); if(!r.width||!r.height) return false; const s=getComputedStyle(el); return s.visibility!=='hidden'&&s.display!=='none'; };
  const L=[...racine.querySelectorAll('*')].filter(el=>{ if(!vis(el)) return false; if(/^(INPUT|TEXTAREA|SELECT|OPTION|HTML|BODY)$/.test(el.tagName)) return false;
     const s=getComputedStyle(el); if(s.cursor!=='pointer'&&!/^(BUTTON|SUMMARY)$/.test(el.tagName)&&el.getAttribute('role')!=='tab') return false; if(/^(BUTTON|SUMMARY)$/.test(el.tagName)) return true; const p=el.parentElement; return !(p&&getComputedStyle(p).cursor==='pointer'&&p.tagName!=='BODY'); });
  const vu={}; const res=[];
  L.forEach((el,i)=>{ const sig=el.tagName+'|'+(el.id||'')+'|'+(typeof el.className==='string'?el.className:'')+'|'+(el.id?'':(el.textContent||'').trim().slice(0,18));
    const sig2=el.tagName+'|'+(typeof el.className==='string'?el.className:'')+'|'+(el.closest('tr')?'tr':''); vu[sig2]=(vu[sig2]||0)+1;
    if(vu[sig2]>3) return; if(res.some(x=>x.sig===sig)) return;
    const txt=(el.textContent||'').trim().slice(0,40);
    if(/sortir|déconnexion|se déconnecter|log ?out|cerrar sesi|finidemo|fin de la démo|#lg|FR$|EN$|ES$/i.test(el.id+' '+txt)) return;
    if(el.closest('#lgsel,.lg,.lang,[data-lg]')) return;
    if(el.tagName==='A'&&el.getAttribute('href')&&!/^#|javascript/.test(el.getAttribute('href'))) return;
    const pre=racine===document.body?'':'s'; el.setAttribute('data-audit',pre+String(res.length)); res.push({sig,txt,i:pre+String(res.length)}); });
  return res; })"""
FERME = r"""(() => { document.dispatchEvent(new KeyboardEvent('keydown',{key:'Escape',bubbles:true}));
  document.querySelectorAll('.ov.on,.dov.on,.mod.on,dialog[open],.on.ov').forEach(o=>{ const x=o.querySelector('.x,[id$="-x"],.fermer,[id$="-ann"]'); if(x) x.click(); o.classList&&o.classList.remove('on'); });
  return !!document.querySelector('.ov.on,.dov.on,dialog[open]'); })()"""
INIT = "0"

s = socket.socket(); s.bind(('127.0.0.1', 0)); port = s.getsockname()[1]; s.close()
srv = subprocess.Popen(['python3','-m','http.server',str(port),'--bind','127.0.0.1'], cwd=str(D), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1)
base = f'http://127.0.0.1:{port}/'
res = {}
def note(page, quand, L):
    for x in L:
        t = x['t']
        if not francais(t): continue
        k = (t[:200])
        if k not in res: res[k] = {'page':page,'quand':quand,'bloc':x['bloc'],'ou':x['ou'],'n':0}
        res[k]['n'] += 1
SEED = r"""([F,Q,E,M,S,J,H,T,C,R,MS,FR,l])=>{ localStorage.clear();
  localStorage.setItem('sam-session-v1',JSON.stringify({id:'sam',nom:'Sam',role:'patron',depuis:new Date().toISOString()}));
  localStorage.setItem('factures-v1',JSON.stringify(F)); localStorage.setItem('caisse-file-v1',JSON.stringify(Q)); localStorage.setItem('expeditions-v1',JSON.stringify(E));
  localStorage.setItem('fiches-modifiees-v1',JSON.stringify(M)); localStorage.setItem('site-stock-v1',JSON.stringify(S)); localStorage.setItem('crm-journal-v1',JSON.stringify(J));
  localStorage.setItem('prix-achat-hist-v1',JSON.stringify(H)); localStorage.setItem('etude-brouillon-v1',JSON.stringify({texte:T,frn:'MTZ',date:'2026-09-24',num:''}));
  localStorage.setItem('clients-v1',JSON.stringify(C)); localStorage.setItem('reglages-v1',JSON.stringify(R)); localStorage.setItem('messages-v1',JSON.stringify(MS));
  localStorage.setItem('fournisseurs-v1',JSON.stringify(FR)); localStorage.setItem('langue-v1',l); localStorage.setItem('sam-comptes-demo-v1','1'); }"""
ARGS = [FACT, FILE, EXP, MOD, SITE, JOU, HIST, ETU, CLI, REG, MSG, FRN, LG]
t0 = time.time()
with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context(viewport={'width':1500,'height':1000})
    ctx.add_init_script("window.__MSG=[]; (function(){ const k=(f)=>(m)=>{ (window.__MSG=window.__MSG||[]).push(String(m||'')); return f; }; window.alert=k(undefined); window.confirm=k(false); window.prompt=k(null); window.print=()=>{}; window.open=()=>null; })();")
    pg = ctx.new_page(); errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)[:200]))
    pg.goto(base + 'accueil.html'); pg.wait_for_timeout(500)
    for page in PAGES:
        pg.evaluate(SEED, ARGS)
        def charge():
            pg.goto(base + page + '.html'); pg.wait_for_timeout(1800); pg.evaluate(INIT)
        charge()
        note(page, 'chargement', pg.evaluate(JS_TEXTES))
        C = pg.evaluate(JS_CLIQUABLES, None)
        nC = min(len(C), MAXCLICS)
        for k in range(nC):
            try:
                ok = pg.evaluate(f"(()=>{{ const e=document.querySelector('[data-audit=\"{k}\"]'); if(!e) return false; e.scrollIntoView({{block:'center'}}); e.click(); return true; }})()")
            except Exception: ok = False
            if not ok: continue
            pg.wait_for_timeout(450)
            if not pg.url.split('?')[0].endswith(page + '.html'):
                note(page, 'clic « %s »' % C[k]['txt'], [])
                charge(); pg.evaluate(JS_CLIQUABLES, None); continue
            try: note(page, 'clic « %s »' % C[k]['txt'], pg.evaluate(JS_TEXTES))
            except Exception: pass
            # un niveau plus bas : ce qui s'est ouvert (fenêtre, fiche) a ses propres onglets et boutons
            try:
                ov = pg.evaluate("(()=>{ const o=[...document.querySelectorAll('.ov.on,.dov.on,.mod.on,dialog[open],.fiche.on,#fiche.on,.panneau.on')].pop(); if(!o) return null; if(!o.id) o.id='audit-ov'; return '#'+o.id; })()")
                if ov:
                    S = pg.evaluate(JS_CLIQUABLES, ov)
                    for s2 in S[:14]:
                        if re.search(r'supprim|delete|elimin|annuler la|cancel the|✕|×', s2['txt'], re.I): continue
                        try:
                            pg.evaluate(f"(()=>{{ const e=document.querySelector('[data-audit=\"{s2['i']}\"]'); if(e) e.click(); }})()"); pg.wait_for_timeout(350)
                            note(page, 'clic « %s » › « %s »' % (C[k]['txt'], s2['txt']), pg.evaluate(JS_TEXTES))
                        except Exception: pass
                        if not pg.url.split('?')[0].endswith(page + '.html'): break
                    charge(); pg.evaluate(JS_CLIQUABLES, None); continue
            except Exception: pass
            try:
                reste = pg.evaluate(FERME); pg.wait_for_timeout(150)
                if reste: charge(); pg.evaluate(JS_CLIQUABLES, None)
            except Exception:
                charge(); pg.evaluate(JS_CLIQUABLES, None)
        print(page, nC, 'clics', len(res), 'restes', int(time.time()-t0), 's', flush=True)
    b.close()
srv.terminate()
json.dump({'lg':LG,'res':res,'errs':errs[:30]}, open(OUT / f'res_{LG}.json','w'), ensure_ascii=False, indent=1)
print('TOTAL', len(res))
