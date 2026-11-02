# -*- coding: utf-8 -*-
"""stock.json / stock_stats.json a partir de cat.json.
Chaque ligne porte la meme cle unique que le catalogue : les deux rubriques
designent le meme produit par le meme identifiant."""
import json
C=json.load(open('cat.json'))
rows=[]
for r in C:
    bc,nomSrc,marque,ml,typ,genre,qte,pvr,pvw,img,src,an,pa,nom,verif,cle,rang,part = r[:18]
    cap=(qte or 0)*(pa or 0)
    # la feuille de comptage ne connait que trois etats
    v = 'ok' if verif=='ok' else ('doute' if verif=='av' else 'non')
    # 10, 11 : prix de vente ; 12 : codes extraits d'une case collée (voir build_data.py)
    rows.append([bc,nom,marque,ml,typ,qte or 0,pa,round(cap,2),v,cle,pvr,pvw,(r[19] if len(r)>19 else [])])
rows.sort(key=lambda x:(-(1 if x[5]>0 else 0), 0 if x[8]!='ok' else 1, -x[7]))
json.dump(rows,open('stock.json','w'),ensure_ascii=False,separators=(',',':'),allow_nan=False)

st=[x for x in rows if x[5]>0]
tot=sum(x[7] for x in st) or 1
st2=sorted(st,key=lambda x:-x[7])
pal={str(n):round(sum(x[7] for x in st2[:n])/tot*100,1) for n in (25,50,100,200,400)}
nonv=[x for x in rows if x[8]!='ok']
S={'total':len(rows),'enstock':len(st),'rupture':len(rows)-len(st),
   'u':sum(x[5] for x in rows),'cap':round(tot),
   'ok':sum(1 for x in rows if x[8]=='ok'),'non':len(nonv),
   'doute':sum(1 for x in rows if x[8]=='doute'),
   'capnon':round(sum(x[7] for x in nonv if x[5]>0)),'paliers':pal}
json.dump(S,open('stock_stats.json','w'),ensure_ascii=False,indent=1)
print('stock.json',len(rows),'lignes · en stock',len(st),'· capital %.0f'%tot)
print(json.dumps(S,ensure_ascii=False))
