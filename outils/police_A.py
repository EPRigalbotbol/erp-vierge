# -*- coding: utf-8 -*-
"""Passage à Inter sur toutes les pages. Plus de police machine à écrire :
les colonnes de chiffres tiennent grâce aux chiffres de largeur fixe."""
import re, pathlib
LIEN='https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap'
FICH=['build_html.py','build_stock.py','build_crm.py','build_journal.py','build_frn.py',
      '_base.css','_modales.css']
for f in FICH:
    p=pathlib.Path(f)
    if not p.exists(): print('absent :',f); continue
    s=p.read_text(); av=s
    s=re.sub(r'https://fonts\.googleapis\.com/css2\?family=[^"\']*', LIEN, s)
    s=s.replace('Archivo,-apple-system','Inter,-apple-system')
    s=s.replace('Archivo,sans-serif','Inter,sans-serif')
    s=s.replace('"IBM Plex Mono",monospace','Inter,sans-serif')
    s=s.replace('"IBM Plex Mono",ui-monospace,monospace','Inter,sans-serif')
    s=s.replace("'IBM Plex Mono',monospace","Inter,sans-serif")
    if s!=av: p.write_text(s); print('ok  ',f)
    else: print('rien',f)

# chiffres de largeur fixe partout : sans monospace, c'est ce qui aligne les colonnes
for f in ['build_html.py','build_stock.py','build_crm.py','build_journal.py','build_frn.py']:
    p=pathlib.Path(f); s=p.read_text()
    if 'font-variant-numeric:tabular-nums;font-feature-settings' in s: continue
    marque='*{box-sizing:border-box}'
    if marque in s:
        s=s.replace(marque, marque+'\nbody{font-variant-numeric:tabular-nums;font-feature-settings:"tnum" 1,"cv05" 1}',1)
        p.write_text(s); print('chiffres alignés :',f)
