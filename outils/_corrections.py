# -*- coding: utf-8 -*-
"""Deux corrections du catalogue de départ, demandées par Sam le 30 oct. 2026, appliquées
aux lignes de cat.json (voir build_data.py) et au même moment, dans l'ERP, aux fiches
déjà en ligne (fiches-modifiees-v1) pour que les deux disent la même chose.

1. LA PARENTHÈSE : « Nom (Clone de tel parfum) » devient
   « Nom ». La parenthèse ne disparaît que du nom affiché (colonne 13) ; le nom
   d'origine (colonne 1) la garde, c'est lui qui sert à reconnaître une vente du site ou à
   chercher. Quelques parenthèses restent, exprès : elles distinguent deux fiches qui
   porteraient sinon le même nom — (NOBOX), (Tester), (2 PCS)/(3 PCS), les contenances
   d'un coffret, (black box)/(white box), (coral), (collector …).

2. LA CONTENANCE : la case s'affiche en oz mais le fichier y avait souvent des ml
   (« 90 » pour un flacon de 90 ml, soit 3 oz). Un chiffre rond d'au moins 20, hors
   coffret, est un ml : on l'écrit comme sur le flacon (100 → 3.4, 90 → 3, 75 → 2.5,
   50 → 1.7). Les coffrets et les petits chiffres (13.5, 17…) restent tels quels : Sam
   les vérifie à la main (contenances_a_verifier.xlsx)."""
import re

GARDE = re.compile(r'nobox|tester|pcs|pc\b|piece|\d\s*x\s*\d|ml|oz|^\s*coral\s*$|white box|black box|collector', re.I)
COFFRET = re.compile(r'set|coffret|gift|mini|x\s*\d|\d\s*x|pcs|pc\b|kit', re.I)
OZ = {100: '3.4', 90: '3', 75: '2.5', 50: '1.7', 125: '4.2', 80: '2.7', 200: '6.7', 60: '2', 150: '5', 30: '1',
      85: '2.8', 20: '0.7', 250: '8.4', 400: '13.5', 120: '4', 110: '3.7', 65: '2.2', 500: '16.9', 88: '3',
      115: '3.9', 55: '1.9', 45: '1.5', 105: '3.5', 40: '1.4', 35: '1.2', 25: '0.8', 70: '2.4'}


def nettoie_nom(nom):
    """Le nom sans sa parenthèse — ou le nom tel quel si la parenthèse doit rester."""
    n = str(nom or '')
    if '(' not in n:
        return n
    def rempl(m):
        return m.group(0) if GARDE.search(m.group(1)) else ''
    out = re.sub(r'\s*\(([^)]*)\)?', rempl, n)
    out = re.sub(r'\s{2,}', ' ', out).strip()
    return out if out else n


def contenance_oz(ml, nom, typ):
    """La contenance en oz quand la case contenait des ml ; sinon la valeur d'origine."""
    s = str(ml if ml is not None else '').strip()
    m = re.match(r'^(\d+(?:[.,]\d+)?)$', s)
    if not m:
        return ml
    v = float(m.group(1).replace(',', '.'))
    if v <= 10 or v < 20 or v != int(v) or COFFRET.search(str(nom or '') + ' ' + str(typ or '')):
        return ml
    return OZ.get(int(v), str(round(v / 29.5735, 1)))


def corrige_rows(rows):
    """Applique les deux corrections aux lignes de cat.json ; renvoie (noms changés, contenances changées)."""
    n_nom = n_ml = 0
    for r in rows:
        nouveau = nettoie_nom(r[13])
        if nouveau != r[13]:
            r[13] = nouveau; n_nom += 1
        oz = contenance_oz(r[3], r[13], r[4])
        if oz != r[3]:
            r[3] = oz; n_ml += 1
    return n_nom, n_ml
