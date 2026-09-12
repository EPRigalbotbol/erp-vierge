# -*- coding: utf-8 -*-
import json
R=json.load(open('marche.json'))
R.sort(key=lambda r:-r['cap'])
def f(v,d=0):
    if v is None: return '—'
    t=('%.*f'%(d,v)).split('.')
    e=t[0]; neg=e.startswith('-'); e=e.lstrip('-')
    g=''
    while len(e)>3: g='\u202f'+e[-3:]+g; e=e[:-3]
    e=('-' if neg else '')+e+g
    return e+(','+t[1] if len(t)>1 else '')
def usd(v,d=0): return '—' if v is None else f(v,d)+' $'

OK=[r for r in R if r['croise']=='ok']
INC=[r for r in R if r['croise']=='incoherent']
INV=[r for r in R if r['croise']=='invérifiable']

def probs(r):
    if r['croise']!='ok': return []
    bas=r['marche_bas']; p=[]
    if r['pa']>=bas*0.92: p.append(('crit',"il l'achète %s, le marché le vend %s"%(usd(r['pa'],2),usd(bas,2))))
    if r['K'] and r['K']>=bas*0.92: p.append(('crit','son prix de gros %s est au niveau du marché : son client ne peut rien gagner'%usd(r['K'])))
    elif r['K'] and r['K']>=bas*0.80: p.append(('warn','son prix de gros %s laisse moins de 20 %% à son client'%usd(r['K'])))
    if r['J'] and r['az'] and r['J']>r['az']*1.05:
        p.append(('warn','son prix retail %s dépasse Amazon (%s) de %s'%(usd(r['J']),usd(r['az'],2),usd(r['J']-r['az']))))
    return p

pbs=[r for r in OK if probs(r)]
cap_pb=sum(r['cap'] for r in pbs); cap_tot=sum(r['cap'] for r in R)
achat_ko=[r for r in OK if r['pa']>=r['marche_bas']*0.92]
cap_achat=sum(r['cap'] for r in achat_ko)

def ruler(r):
    vals=[v for v in [r['pa'],r['K'],r['J'],r['az'],r['ebay_prix']] if v]
    if not vals: return '<div class="rl rl-vide">aucune donnée</div>'
    mx=max(vals)*1.12
    def pc(v): return v/mx*100
    h=[]
    if r['marche_bas'] and r['marche_haut']:
        a,b=pc(r['marche_bas']),pc(r['marche_haut'])
        h.append('<div class="band" style="left:%.2f%%;width:%.2f%%"></div>'%(a,max(b-a,0.7)))
    for v,cls,lab in [(r['pa'],'pa','achat'),(r['K'],'k','gros'),(r['J'],'j','retail')]:
        if v: h.append('<div class="mk mk-%s" style="left:%.2f%%"><span>%s</span></div>'%(cls,pc(v),lab))
    return '<div class="rl">'+''.join(h)+'</div>'

def bloc(r,idx=None):
    ps=probs(r)
    sev='crit' if any(s=='crit' for s,_ in ps) else ('warn' if ps else 'ok')
    if r['croise']=='incoherent': sev='inc'
    if r['croise']=='invérifiable': sev='inv'
    lib={'crit':'à corriger','warn':'à surveiller','ok':'bien placé','inc':'relevé incohérent','inv':'invérifiable'}[sev]
    li=''.join('<li class="%s">%s</li>'%(s,t) for s,t in ps)
    if not ps and sev=='ok': li='<li class="ok">prix cohérents avec le marché relevé</li>'
    if sev=='inc': li='<li class="inc">Amazon dit %s, eBay dit %s — un écart de %s×. Le code-barres tombe sur une autre contenance ou sur des contrefaçons. Aucune conclusion possible.</li>'%(usd(r['az'],2),usd(r['ebay_prix'],2),f(r['ratio'],1))
    if sev=='inv': li='<li class="inc">%s. Sans deuxième source, le relevé eBay ne peut pas être recoupé.</li>'%('Absent d\'Amazon' if r['ebay_prix'] else 'Absent des deux plateformes')
    return f'''<article class="ref s-{sev}">
 <header>
  <div class="idm">
   <h3>{r['nom']}</h3>
   <p class="meta">{r['mq']} · {r['ml']} · <span class="bc">{r['bc']}</span></p>
  </div>
  <div class="stk"><b>{f(r['qte'])}</b><span>flacons</span></div>
  <div class="stk"><b>{usd(r['cap'])}</b><span>immobilisés</span></div>
  <div class="tag t-{sev}">{lib}</div>
 </header>
 <div class="prix">
  <div class="pc"><span>achat</span><b>{usd(r['pa'],2)}</b></div>
  <div class="pc"><span>gros</span><b>{usd(r['K'],2)}</b></div>
  <div class="pc"><span>retail</span><b>{usd(r['J'],2)}</b></div>
  <div class="pc sep"><span>Amazon</span><b>{usd(r['az'],2)}</b>{'<em>'+r['dem']+' /mois</em>' if r['dem'] else ''}</div>
  <div class="pc"><span>eBay ({f(r['en'])} annonces)</span><b>{usd(r['ebay_prix'],2)}</b></div>
 </div>
 {ruler(r)}
 <ul class="dg">{li}</ul>
</article>'''

sections=[]
sections.append('<h2 class="sec">Relevés recoupés <span>%d références · les deux plateformes se rejoignent</span></h2>'%len(OK))
sections.append('\n'.join(bloc(r) for r in OK))
sections.append('<h2 class="sec">Relevés à jeter <span>%d références · les deux plateformes se contredisent</span></h2>'%len(INC))
sections.append('\n'.join(bloc(r) for r in INC))
sections.append('<h2 class="sec">Non recoupables <span>%d références · une seule plateforme, ou aucune</span></h2>'%len(INV))
sections.append('\n'.join(bloc(r) for r in INV))

HTML=f'''<title>Plus cher ou moins cher qu'Amazon&nbsp;?</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap">
<style>
:root{{
 --bg:#F6F5F9; --surface:#FFFFFF; --surface2:#EFEDF4; --line:#DEDAE6; --line2:#C9C3D8;
 --ink:#1B1924; --ink2:#4A4557; --muted:#767085;
 --iris:#5B4B8A; --iris-soft:#EDE9F6;
 --good:#2E7D5B; --good-s:#E4F2EB; --warn:#B8811F; --warn-s:#FBF0DA; --crit:#A93448; --crit-s:#FBE7EA;
 --band:rgba(91,75,138,.16);
}}
@media (prefers-color-scheme:dark){{ :root:not([data-theme="light"]){{
 --bg:#131219; --surface:#1C1A24; --surface2:#252231; --line:#332E42; --line2:#453E58;
 --ink:#ECEAF2; --ink2:#BEB8CC; --muted:#8F89A0;
 --iris:#A99AE0; --iris-soft:#252134;
 --good:#5FBE90; --good-s:#1A2C24; --warn:#DDAA55; --warn-s:#2E2517; --crit:#E0798C; --crit-s:#31191F;
 --band:rgba(169,154,224,.20);
}} }}
:root[data-theme="dark"]{{
 --bg:#131219; --surface:#1C1A24; --surface2:#252231; --line:#332E42; --line2:#453E58;
 --ink:#ECEAF2; --ink2:#BEB8CC; --muted:#8F89A0;
 --iris:#A99AE0; --iris-soft:#252134;
 --good:#5FBE90; --good-s:#1A2C24; --warn:#DDAA55; --warn-s:#2E2517; --crit:#E0798C; --crit-s:#31191F;
 --band:rgba(169,154,224,.20);
}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--ink);
 font-family:Archivo,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
 font-size:15px;line-height:1.55;-webkit-font-smoothing:antialiased}}
.wrap{{max-width:1060px;margin:0 auto;padding:44px 24px 90px}}
h1,h2,h3{{text-wrap:balance;margin:0}}
b,strong{{font-weight:600}}
.mono,.bc,.pc b,.stk b,.kpi b{{font-family:"IBM Plex Mono",ui-monospace,monospace;font-variant-numeric:tabular-nums}}

/* en-tete */
.hd{{border-bottom:2px solid var(--ink);padding-bottom:26px;margin-bottom:34px}}
.eyebrow{{font-size:11.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--iris);font-weight:600;margin:0 0 12px}}
.hd h1{{font-size:clamp(30px,4.6vw,46px);line-height:1.06;letter-spacing:-.022em;font-weight:700;max-width:16ch}}
.lede{{margin:16px 0 0;font-size:17px;line-height:1.5;color:var(--ink2);max-width:62ch}}
.stamp{{margin-top:18px;font-size:12.5px;color:var(--muted);font-family:"IBM Plex Mono",monospace}}

/* chiffres cles */
.kpis{{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:1px;background:var(--line);
 border:1px solid var(--line);margin:0 0 14px}}
.kpi{{background:var(--surface);padding:18px 20px;display:flex;flex-direction:column;gap:3px}}
.kpi b{{font-size:27px;font-weight:600;letter-spacing:-.02em;line-height:1.1}}
.kpi span{{font-size:12.5px;color:var(--muted)}}
.kpi.hot b{{color:var(--crit)}}

/* encadres */
.note{{border-left:3px solid var(--iris);background:var(--surface);padding:18px 22px;margin:26px 0}}
.note h4{{margin:0 0 8px;font-size:15px;font-weight:600}}
.note p{{margin:0 0 10px;color:var(--ink2);max-width:66ch}}
.note p:last-child{{margin-bottom:0}}

/* sections */
.sec{{font-size:13px;letter-spacing:.1em;text-transform:uppercase;font-weight:600;color:var(--ink);
 margin:46px 0 16px;padding-bottom:9px;border-bottom:1px solid var(--line2);
 display:flex;justify-content:space-between;align-items:baseline;gap:14px;flex-wrap:wrap}}
.sec span{{letter-spacing:0;text-transform:none;font-weight:400;font-size:13px;color:var(--muted)}}

/* fiche reference */
.ref{{background:var(--surface);border:1px solid var(--line);border-left:4px solid var(--line2);
 padding:18px 20px;margin-bottom:12px}}
.ref.s-crit{{border-left-color:var(--crit)}}
.ref.s-warn{{border-left-color:var(--warn)}}
.ref.s-ok{{border-left-color:var(--good)}}
.ref.s-inc,.ref.s-inv{{border-left-color:var(--line2);background:var(--surface2)}}
.ref header{{display:flex;align-items:flex-start;gap:18px;flex-wrap:wrap}}
.idm{{flex:1 1 260px;min-width:0}}
.ref h3{{font-size:17px;font-weight:600;letter-spacing:-.012em;line-height:1.25}}
.meta{{margin:3px 0 0;font-size:12.5px;color:var(--muted)}}
.bc{{font-size:12px;color:var(--muted)}}
.stk{{display:flex;flex-direction:column;align-items:flex-end;gap:1px;flex:0 0 auto}}
.stk b{{font-size:16px;font-weight:600}}
.stk span{{font-size:11px;color:var(--muted)}}
.tag{{flex:0 0 auto;font-size:11px;font-weight:600;letter-spacing:.05em;text-transform:uppercase;
 padding:5px 10px;border-radius:2px;white-space:nowrap}}
.t-crit{{background:var(--crit-s);color:var(--crit)}}
.t-warn{{background:var(--warn-s);color:var(--warn)}}
.t-ok{{background:var(--good-s);color:var(--good)}}
.t-inc,.t-inv{{background:var(--surface2);color:var(--muted);border:1px solid var(--line)}}

.prix{{display:flex;flex-wrap:wrap;gap:0 26px;margin:15px 0 4px;padding-top:14px;border-top:1px solid var(--line)}}
.pc{{display:flex;flex-direction:column;gap:0}}
.pc span{{font-size:10.5px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted)}}
.pc b{{font-size:16px;font-weight:500}}
.pc em{{font-size:11px;font-style:normal;color:var(--iris);font-weight:500}}
.pc.sep{{padding-left:26px;border-left:1px dashed var(--line2)}}

/* regle de position */
.rl{{position:relative;height:34px;margin:16px 0 2px;border-bottom:1px solid var(--line2)}}
.rl-vide{{color:var(--muted);font-size:12.5px;border:0;height:auto}}
.band{{position:absolute;bottom:0;top:8px;background:var(--band);border-left:1px solid var(--iris);border-right:1px solid var(--iris)}}
.mk{{position:absolute;bottom:0;width:0}}
.mk::before{{content:"";position:absolute;bottom:0;left:-1px;width:2px;height:15px;background:var(--ink)}}
.mk span{{position:absolute;bottom:17px;left:0;transform:translateX(-50%);font-size:10px;letter-spacing:.05em;
 text-transform:uppercase;color:var(--ink2);white-space:nowrap;font-weight:500;
 background:var(--surface);padding:0 3px;border-radius:2px}}
.ref.s-inc .mk span,.ref.s-inv .mk span{{background:var(--surface2)}}
.mk-pa::before{{background:var(--muted)}} .mk-pa span{{color:var(--muted)}}
.mk-k::before{{background:var(--crit);width:3px;left:-1.5px}} .mk-k span{{color:var(--crit);font-weight:600}}
.mk-j::before{{background:var(--iris);width:3px;left:-1.5px}} .mk-j span{{color:var(--iris);font-weight:600}}

.dg{{list-style:none;margin:12px 0 0;padding:0;display:flex;flex-direction:column;gap:5px}}
.dg li{{font-size:13.5px;color:var(--ink2);padding-left:16px;position:relative;max-width:78ch}}
.dg li::before{{content:"";position:absolute;left:0;top:8px;width:6px;height:6px;border-radius:50%;background:var(--line2)}}
.dg li.crit::before{{background:var(--crit)}}
.dg li.warn::before{{background:var(--warn)}}
.dg li.ok::before{{background:var(--good)}}

/* legende */
.leg{{display:flex;gap:20px;flex-wrap:wrap;font-size:12px;color:var(--muted);margin:6px 0 0;
 padding:12px 16px;background:var(--surface);border:1px solid var(--line)}}
.leg i{{font-style:normal;display:inline-flex;align-items:center;gap:6px}}
.sw{{width:12px;height:3px;display:inline-block}}
.sw-band{{background:var(--band);border-left:1px solid var(--iris);border-right:1px solid var(--iris);height:11px;width:22px}}

/* decision */
.opt{{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:14px;margin:18px 0}}
.card{{background:var(--surface);border:1px solid var(--line);padding:20px}}
.card h4{{margin:0 0 4px;font-size:16px;font-weight:600}}
.card .price{{font-family:"IBM Plex Mono",monospace;font-size:13px;color:var(--iris);font-weight:500;margin:0 0 10px}}
.card p{{margin:0 0 9px;font-size:13.5px;color:var(--ink2)}}
.card ul{{margin:0;padding-left:17px;font-size:13px;color:var(--ink2)}}
.card li{{margin-bottom:4px}}
.reco{{border-color:var(--iris);border-width:2px}}

.q{{counter-reset:q;list-style:none;padding:0;margin:16px 0 0;display:flex;flex-direction:column;gap:10px}}
.q li{{counter-increment:q;background:var(--surface);border:1px solid var(--line);padding:14px 18px 14px 46px;position:relative;font-size:14px}}
.q li::before{{content:"Q" counter(q);position:absolute;left:16px;top:14px;font-family:"IBM Plex Mono",monospace;
 font-size:12px;font-weight:600;color:var(--iris)}}
.q b{{display:block;margin-bottom:3px}}
.q span{{color:var(--muted);font-size:13px}}
footer{{margin-top:56px;padding-top:20px;border-top:1px solid var(--line);font-size:12.5px;color:var(--muted);max-width:70ch}}
@media (max-width:620px){{ .pc.sep{{padding-left:0;border-left:0}} .prix{{gap:0 18px}} }}
</style>

<div class="wrap">
<header class="hd">
 <p class="eyebrow">Perfumes Trade · relevé de marché</p>
 <h1>Plus cher ou moins cher qu'Amazon&nbsp;?</h1>
 <p class="lede">Vingt références passées à la main sur Amazon et eBay, recherchées par code-barres.
 Douze pèsent le plus gros du capital, huit sont tirées au hasard pour mesurer la couverture.
 Verdict&nbsp;: sur les références où les deux plateformes se rejoignent,
 <b>{usd(cap_pb)} de stock est mal positionné</b>, dont {usd(cap_achat)} acheté au-dessus du prix de vente du marché.</p>
 <p class="stamp">Relevé du 2 septembre 2026 · prix Amazon = premier résultat organique · prix eBay = médiane des vendeurs américains établis, Buy It Now</p>
</header>

<div class="kpis">
 <div class="kpi"><b>19/20</b><span>trouvées sur au moins une plateforme</span></div>
 <div class="kpi"><b>14/20</b><span>trouvées sur Amazon</span></div>
 <div class="kpi"><b>19/20</b><span>trouvées sur eBay</span></div>
 <div class="kpi hot"><b>{usd(cap_pb)}</b><span>de stock mal positionné, sur {usd(cap_tot)} testés</span></div>
</div>

<div class="note">
 <h4>Pourquoi une seule plateforme ne suffit pas</h4>
 <p>La recherche par code-barres n'est pas une correspondance exacte&nbsp;: eBay cherche le chiffre
 dans le texte de l'annonce. Une annonce pour le format 30&nbsp;ml qui cite le code-barres du 100&nbsp;ml
 remonte quand même. Sur trois références, eBay affiche un prix deux à trois fois inférieur à Amazon —
 ce ne sont pas des bonnes affaires, ce sont de mauvaises correspondances.</p>
 <p>D'où la règle appliquée ici&nbsp;: <b>si les deux plateformes s'écartent de plus du double, le relevé
 est jeté</b>, pas transformé en alerte. C'est ce filtre qui rend les chiffres ci-dessous utilisables —
 et c'est la raison pour laquelle surveiller eBay seul ne marcherait pas.</p>
</div>

{sections[0]}
<div class="leg">
 <i><span class="sw sw-band"></span> fourchette du marché (eBay ↔ Amazon)</i>
 <i><span class="sw" style="background:var(--muted)"></span> son prix d'achat</i>
 <i><span class="sw" style="background:var(--crit)"></span> son prix de gros</i>
 <i><span class="sw" style="background:var(--iris)"></span> son prix retail</i>
</div>
<div style="height:14px"></div>
{sections[1]}
{sections[2]}
{sections[3]}
{sections[4]}
{sections[5]}

<h2 class="sec">Ce qu'il faut décider <span>avant d'écrire une ligne de code</span></h2>
<div class="note">
 <h4>Ni le catalogue ni le site ne peuvent faire cette surveillance</h4>
 <p>Le catalogue est un fichier&nbsp;: quand il est fermé, rien ne tourne. Une vérification automatique
 a besoin d'une machine qui s'exécute toute seule — son Mac allumé en permanence, ou un petit serveur.
 C'est le premier choix, et il conditionne tout le reste.</p>
 <p>Deuxième point&nbsp;: <b>deux fois par jour ne sert à rien.</b> Un prix de parfum ne bouge pas deux fois
 dans la journée. Une fois par jour sur les 200 références qui portent la moitié du capital donne
 la même information, pour un dixième du volume et sans risque de blocage.</p>
</div>
<div class="opt">
 <div class="card reco">
  <h4>Étape 1 — eBay par l'API officielle</h4>
  <p class="price">gratuit · compte développeur eBay, 10 minutes</p>
  <p>Recherche par identifiant produit structuré, pas par mots-clés&nbsp;: les mauvaises
  correspondances vues ci-dessus disparaissent en grande partie.</p>
  <ul>
   <li>1 873 références en stock à code-barres valide</li>
   <li>un passage par jour tient dans le quota gratuit</li>
   <li>ne donne ni le rang ni le prix Amazon</li>
  </ul>
 </div>
 <div class="card">
  <h4>Étape 2 — Amazon, payant</h4>
  <p class="price">service tiers facturé à la requête · montant à chiffrer</p>
  <p>Sans Amazon, pas de recoupement, donc pas d'alerte fiable. L'API officielle exige
  un compte vendeur ou affilié qu'il n'a peut-être pas.</p>
  <ul>
   <li>donne le prix, le rang et la demande mensuelle</li>
   <li>à n'engager que si l'étape 1 change vraiment ses décisions</li>
   <li>le rang est bien public&nbsp;: Versace Eros est n°18 des eaux de toilette homme</li>
  </ul>
 </div>
 <div class="card">
  <h4>Ce qu'on ne fera pas</h4>
  <p class="price">aspiration automatisée d'Amazon</p>
  <p>Le fichier robots.txt d'Amazon l'interdit, et 3 700 pages par jour font tomber
  l'accès en quelques heures. Ce n'est pas une limite technique&nbsp;: c'est un choix.</p>
 </div>
</div>

<h2 class="sec">À lui demander vendredi <span>les réponses décident de l'étape 2</span></h2>
<ol class="q">
 <li><b>Savais-tu que tu achètes le Tiffany Rose Gold {usd(79.25,2)} alors qu'Amazon le vend {usd(64.59,2)}&nbsp;?</b>
 <span>119 flacons, {usd(9431)}. Si le prix d'achat est juste, c'est le fournisseur qu'il faut changer, pas le prix de vente.</span></li>
 <li><b>Sur le JPG Le Beau Paradise Garden, tu vends en gros à {usd(95)} et le marché eBay est à {usd(97.59,2)}. Ton client en fait quoi&nbsp;?</b>
 <span>438 flacons, {usd(41391)} — sa deuxième plus grosse ligne.</span></li>
 <li><b>Ton retail Bvlgari Thé Blanc est à {usd(149)}, Amazon est à {usd(129.98,2)}. C'est voulu&nbsp;?</b>
 <span>782 flacons, {usd(58259)} — sa première ligne.</span></li>
 <li><b>Est-ce que tu vends toi-même sur Amazon ou eBay, sous quel compte&nbsp;?</b>
 <span>Change tout&nbsp;: s'il est vendeur Amazon, l'API officielle devient gratuite pour lui.</span></li>
 <li><b>Sur quelle machine ça tourne&nbsp;?</b>
 <span>Son Mac allumé en permanence, ou un petit serveur à quelques dollars par mois.</span></li>
 <li><b>Une alerte par jour ou un récapitulatif par semaine&nbsp;?</b>
 <span>Une alerte qu'on ne lit pas coûte plus cher qu'elle ne rapporte.</span></li>
</ol>

<footer>
 Relevé manuel du 2 septembre 2026 sur amazon.com et ebay.com, recherche par code-barres, livraison États-Unis.
 Prix eBay&nbsp;: annonces Buy It Now de vendeurs américains à 95&nbsp;% d'avis positifs minimum et au moins
 100 évaluations, médiane du noyau à ±25&nbsp;%. Les prix constatés bougent&nbsp;; ce document est une photo,
 pas une surveillance. Quantités et prix d'achat issus de <span class="mono">inventaire_enrichi.xlsx</span>.
</footer>
</div>'''
open('rapport_marche.html','w').write(HTML)
print('ok',len(HTML),'octets ·',len(OK),'recoupées ·',len(INC),'incohérentes ·',len(INV),'invérifiables')
print('capital mal positionne : %.0f / %.0f'%(cap_pb,cap_tot))
