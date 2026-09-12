import pandas as pd, numpy as np, re, json, unicodedata

SRC='/root/.claude/uploads/7f8c7d7e-a2bf-53ed-8df2-d9c17ddd87b0/de95abdd-Test_inventory_sam.xlsx'
raw = pd.read_excel(SRC, header=0, dtype=object)
raw.columns=['barcode','name','size','brand','type','gender','qty','unit_price','stock_val','pvr','pvw','inv_clem','location','shop1','shop2','asin','buybox','notes','x'][:len(raw.columns)]
raw=raw.dropna(how='all').reset_index(drop=True)
D={'rows_in':len(raw)}

def num(s):
    if pd.isna(s): return np.nan
    if isinstance(s,(int,float)): return float(s)
    t=str(s).replace('$','').replace(' ','').replace(' ','').replace(',','.')
    t=re.sub(r'[^0-9.\-]','',t)
    if t in ('','-','.'): return np.nan
    try: return float(t)
    except: return np.nan
for c in ['qty','unit_price','pvr','pvw','size']: raw[c+'_n']=raw[c].apply(num)

# ---------- CODES-BARRES ----------
def digits(x): return re.sub(r'\D','',str(x)) if pd.notna(x) else ''
raw['bc_raw']=raw.barcode.apply(digits)

def chk(code):
    """valide la cle de controle UPC-A (12) / EAN-13 (13)"""
    if len(code) not in (12,13) or not code.isdigit(): return False
    body,c=code[:-1],int(code[-1])
    if len(code)==12: w=[3 if i%2==0 else 1 for i in range(11)]
    else:             w=[1 if i%2==0 else 3 for i in range(12)]
    s=sum(int(d)*wi for d,wi in zip(body,w))
    return (-s)%10==c

PLACEHOLDER=set()
vc=raw[raw.bc_raw!=''].bc_raw.value_counts()
for code,n in vc.items():
    if len(code)<8 or (n>2 and raw[raw.bc_raw==code].name.nunique()>2):
        PLACEHOLDER.add(code)

def fix_bc(c):
    if c=='' : return '', 'MANQUANT'
    if c in PLACEHOLDER: return '', 'BIDON'
    if chk(c): return c, 'OK'
    for cand in (c.zfill(12), c.zfill(13), c.zfill(14)[1:]):
        if chk(cand): return cand, 'REPARE'
    if len(c)in(12,13): return c, 'CLE_INVALIDE'
    return c, 'FORMAT_DOUTEUX'

res=raw.bc_raw.apply(fix_bc)
raw['bc']=[r[0] for r in res]; raw['bc_status']=[r[1] for r in res]
D['bc']=raw.bc_status.value_counts().to_dict()

# doublons reels
ok=raw[raw.bc!='']
dcount=ok.bc.value_counts(); dups=set(dcount[dcount>1].index)
raw['bc_doublon']=raw.bc.apply(lambda x: x!='' and x in dups)
D['bc_doublons_codes']=len(dups); D['bc_doublons_lignes']=int(raw.bc_doublon.sum())

# ---------- MARQUE ----------
def norm_brand(b):
    if pd.isna(b): return ''
    s=' '.join(str(b).split()).strip(' .')
    return s
raw['brand_c']=raw.brand.apply(norm_brand)
canon={}
for b in raw.brand_c.unique():
    k=unicodedata.normalize('NFKD',b.lower()).encode('ascii','ignore').decode()
    k=re.sub(r'[^a-z0-9]','',k)
    canon.setdefault(k,[]).append(b)
mapping={}
merged=0
for k,v in canon.items():
    if len(v)>1: merged+=len(v)-1
    best=max(v,key=lambda s:(sum(c.isupper() for c in s),len(s)))
    for x in v: mapping[x]=best
raw['brand_c']=raw.brand_c.map(mapping)
D['brands_before']=raw.brand.nunique(); D['brands_after']=raw.brand_c.nunique(); D['brands_merged']=merged

# ---------- GENRE ----------
G={'W':'W','F':'W','WOMEN':'W','M':'M','MEN':'M','U':'U','UNI':'U','UNISEX':'U','MIX':'U','B':'K','BB':'K','G':'K','KIDS':'K','E':''}
raw['gender_c']=raw.gender.apply(lambda x:'' if pd.isna(x) else G.get(str(x).strip().upper(),''))
D['gender_after']=raw.gender_c.replace('',np.nan).value_counts().to_dict()
D['gender_vides']=int((raw.gender_c=='').sum())

# ---------- TYPE ----------
def norm_type(t):
    if pd.isna(t): return ''
    s=str(t).strip().upper().replace('.','')
    return ' '.join(s.split())
raw['type_c']=raw.type.apply(norm_type)
D['type_before']=raw.type.nunique(); D['type_after']=raw.type_c.replace('',np.nan).nunique()

# ---------- VERIF INVENTAIRE ----------
def norm_inv(v):
    if pd.isna(v): return ''
    s=str(v).strip().upper().rstrip('.')
    if s.startswith('OK'): return 'OK'
    if s.startswith('?'): return 'A VERIFIER'
    if s=='-': return 'NON VERIFIE'
    return 'A VERIFIER'
raw['inv_c']=raw.inv_clem.apply(norm_inv)
D['inv']=raw.inv_c.replace('',np.nan).value_counts().to_dict()

# ---------- CALCULS ----------
raw['stock_value']=(raw.qty_n.fillna(0)*raw.unit_price_n.fillna(0)).round(2)
raw['marge_w_pct']=np.where((raw.pvw_n>0)&(raw.unit_price_n>0),((raw.pvw_n-raw.unit_price_n)/raw.pvw_n*100).round(1),np.nan)
raw['marge_r_pct']=np.where((raw.pvr_n>0)&(raw.unit_price_n>0),((raw.pvr_n-raw.unit_price_n)/raw.pvr_n*100).round(1),np.nan)

ins=raw[raw.qty_n>0]
D.update(dict(
  sku_total=len(raw), sku_en_stock=int(len(ins)), sku_zero=int((raw.qty_n==0).sum()),
  unites=int(ins.qty_n.sum()), capital=round(float(ins.stock_value.sum())),
  marge_w_med=round(float(ins.marge_w_pct.median()),1), marge_r_med=round(float(ins.marge_r_pct.median()),1),
  perte_w=int((ins.pvw_n<=ins.unit_price_n).sum()), perte_r=int((ins.pvr_n<=ins.unit_price_n).sum()),
  sans_pvw=int(ins.pvw_n.isna().sum()), sans_pvr=int(ins.pvr_n.isna().sum()),
  sans_asin=int(ins.asin.isna().sum()), avec_asin=int(raw.asin.notna().sum()),
))
sp=ins[ins.pvw_n.isna()&ins.pvr_n.isna()]
D['invendable_sku']=len(sp); D['invendable_u']=int(sp.qty_n.sum()); D['invendable_cap']=round(float(sp.stock_value.sum()))

srt=ins.sort_values('stock_value',ascending=False)
tot=srt.stock_value.sum()
D['conc']={str(n):[round(float(srt.head(n).stock_value.sum())),round(100*float(srt.head(n).stock_value.sum())/tot,1)] for n in (10,50,100,200)}
D['top']=[{'brand':r.brand_c,'name':str(r['name']),'qty':int(r.qty_n),'pu':float(r.unit_price_n),'val':float(r.stock_value)} for _,r in srt.head(15).iterrows()]
D['bc_bidon_ex']=sorted(list(PLACEHOLDER))[:12]
D['bc_bidon_lignes']=int((raw.bc_status=='BIDON').sum())

top_brands=ins.groupby('brand_c').agg(sku=('name','size'),u=('qty_n','sum'),cap=('stock_value','sum')).sort_values('cap',ascending=False).head(15)
D['brands_top']=[{'b':i,'sku':int(r.sku),'u':int(r.u),'cap':round(float(r.cap))} for i,r in top_brands.iterrows()]

# ---------- SORTIE A-L ----------
out=pd.DataFrame({
 'A_BARCODE':raw.bc,'B_NOM':raw.name,'C_CONTENANCE':raw.size_n,'D_MARQUE':raw.brand_c,
 'E_TYPE':raw.type_c,'F_GENRE':raw.gender_c,'G_QTE':raw.qty_n,'H_PRIX_ACHAT':raw.unit_price_n,
 'I_VALEUR_STOCK':raw.stock_value,'J_PVR':raw.pvr_n,'K_PVW':raw.pvw_n,'L_VERIF':raw.inv_c,
 '_ASIN':raw.asin,'_BC_STATUT':raw.bc_status,'_BC_DOUBLON':raw.bc_doublon,
 '_MARGE_W_%':raw.marge_w_pct,'_MARGE_R_%':raw.marge_r_pct})
out['A_BARCODE']=out['A_BARCODE'].astype(str)
out['_ASIN']=out['_ASIN'].astype(str).replace('nan','')
import openpyxl
with pd.ExcelWriter('/home/claude/catalogue/inventaire_propre.xlsx',engine='openpyxl') as xw:
    out.to_excel(xw,index=False,sheet_name='INVENTAIRE')
    ws=xw.sheets['INVENTAIRE']
    for row in ws.iter_rows(min_row=2,min_col=1,max_col=1):
        for c in row: c.number_format='@'
    for row in ws.iter_rows(min_row=2,min_col=13,max_col=13):
        for c in row: c.number_format='@'
    for col,w in zip('ABCDEFGHIJKLMNOPQ',[16,46,12,22,12,8,9,13,15,11,11,14,14,15,12,12,12]):
        ws.column_dimensions[col].width=w
    ws.freeze_panes='B2'
out.to_csv('/home/claude/catalogue/inventaire_propre.csv',index=False)
json.dump(D,open('/home/claude/catalogue/diag.json','w'),indent=1,default=str)
print(json.dumps(D,indent=1,default=str)[:2600])
