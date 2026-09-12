# -*- coding: utf-8 -*-
import json
R=json.load(open('marche.json'))
for r in R:
    a,e=r['az'],r['ebay_prix']
    if a and e:
        ratio=max(a,e)/min(a,e)
        r['croise']= 'ok' if ratio<2 else 'incoherent'
        r['ratio']=ratio
        r['marche']= (a+e)/2 if ratio<1.35 else None   # accord etroit -> prix de marche
        r['marche_bas']=min(a,e); r['marche_haut']=max(a,e)
    else:
        r['croise']='invérifiable'; r['ratio']=None; r['marche']=None
        r['marche_bas']=r['marche_haut']=None
json.dump(R,open('marche.json','w'),indent=1)
pb=[]
print('%-34s %6s %6s %6s %6s %8s %8s %6s %s'%('produit','cap','PA','K','J','AMZ','eBay','x','croisement'))
for r in R:
    print('%-34s %6.0f %6.1f %6s %6s %8s %8s %6s %s'%((r['nom'][:28]+' '+r['ml'])[:34],r['cap'],r['pa'],
      r['K'] or '-',r['J'] or '-',r['az'] or '-',('%.2f'%r['ebay_prix']) if r['ebay_prix'] else '-',
      ('%.2f'%r['ratio']) if r['ratio'] else '-', r['croise']))
print()
print('=== REFERENCES VERIFIEES AVEC UN PROBLEME DE PRIX ===')
tot=0
for r in R:
    if r['croise']!='ok': continue
    bas=r['marche_bas']
    prob=[]
    if r['K'] and r['K']>=bas*0.92: prob.append('gros a %.0f$ vs marche a %.0f$'%(r['K'],bas))
    if r['pa']>=bas*0.92: prob.append("ACHAT a %.2f$ >= marche %.0f$"%(r['pa'],bas))
    if r['J'] and r['az'] and r['J']>r['az']*1.05: prob.append('retail %.0f$ > Amazon %.2f$'%(r['J'],r['az']))
    if prob:
        tot+=r['cap']; pb.append(r)
        print('%-34s %8.0f $  %s'%((r['nom'][:28]+' '+r['ml'])[:34],r['cap'],' | '.join(prob)))
print('\ncapital concerne : %.0f $ sur %.0f $ testes (%.0f%%)'%(tot,sum(x['cap'] for x in R),tot/sum(x['cap'] for x in R)*100))
json.dump([r['bc'] for r in pb],open('pb.json','w'))
