# -*- coding: utf-8 -*-
"""Trois variantes typographiques du meme catalogue, pour choisir sur pieces."""
import re, pathlib
base=open('catalogue.html').read()

V = {
 'A_inter': {
   'lien':'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap',
   'ui':'Inter', 'data':'Inter',
   'titre':'A — Inter partout, chiffres alignés'},
 'B_jakarta': {
   'lien':'https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap',
   'ui':'Plus Jakarta Sans', 'data':'JetBrains Mono',
   'titre':'B — Plus Jakarta Sans + JetBrains Mono'},
 'C_franklin': {
   'lien':'https://fonts.googleapis.com/css2?family=Libre+Franklin:wght@400;500;600;700;800&display=swap',
   'ui':'Libre Franklin', 'data':'Libre Franklin',
   'titre':'C — Libre Franklin partout, chiffres alignés'},
}

for k,v in V.items():
    h=base
    h=re.sub(r'<link rel="stylesheet" href="https://fonts\.googleapis\.com[^"]*">',
             f'<link rel="stylesheet" href="{v["lien"]}">', h)
    h=h.replace('Archivo,-apple-system', v['ui']+',-apple-system')
    h=h.replace('Archivo,sans-serif', v['ui']+',sans-serif')
    h=h.replace('"IBM Plex Mono",monospace', f'"{v["data"]}",monospace' if v['data']!=v['ui'] else f'"{v["ui"]}",sans-serif')
    if v['data']==v['ui']:
        # sans monospace : on impose des chiffres de meme largeur pour que les colonnes s'alignent
        h=h.replace('<style>','<style>\n*{font-variant-numeric:tabular-nums}',1)
    pathlib.Path(f'var_{k}.html').write_text(h)
    print('var_'+k+'.html',len(h)//1024,'Ko')
