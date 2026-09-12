# Feuille de comptage prioritaire.
#
# Le 9 septembre, en préparant le rendez-vous avec Sam, un chiffre est sorti du
# catalogue : 636 références EN STOCK n'ont jamais été comptées ou sont marquées
# « à vérifier », et elles portent 568 494 $ au prix d'achat — 41 % de la valeur
# de tout l'inventaire.
#
# On ne ferme pas la boutique pour compter 1 892 références. Mais on n'a pas
# besoin de tout compter : vingt références suffisent à couvrir 17 % de la
# valeur. C'est cette liste-là.
#
# Deux décisions qui ne se voient pas dans le résultat :
#
#   - On CHOISIT par la valeur (quantité × prix d'achat) et on MARCHE par
#     l'alphabet. L'entrepôt de Sam est rangé par ordre alphabétique de marque ;
#     une feuille triée par valeur ferait traverser le dépôt vingt fois.
#   - On compte en flacons, pas en dollars, mais on affiche la valeur de l'écart
#     à côté : un écart de trois flacons ne veut rien dire tant qu'on ne sait
#     pas s'il s'agit d'un Armaf à 18,50 $ ou d'un Xerjoff à 120 $.
import json, pathlib
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

D = pathlib.Path('/home/claude/catalogue')
d = json.load(open(D / 'cat.json'))

# colonnes du catalogue : 0 code-barres, 1 nom, 2 marque, 3 contenance, 4 type,
# 6 quantité, 12 prix d'achat moyen, 14 état du comptage
avec = [r for r in d if (r[6] or 0) > 0]
def val(r): return (r[6] or 0) * (r[12] or 0)
total_stock = sum(val(r) for r in avec)
douteux = sorted([r for r in avec if str(r[14]).lower() != 'ok'], key=val, reverse=True)
total_douteux = sum(val(r) for r in douteux)
top = douteux[:20]
total_top = sum(val(r) for r in top)
top.sort(key=lambda r: ((r[2] or '').lower(), (r[1] or '').lower()))   # l'ordre des étagères

def dollars(x): return format(round(x), ',d').replace(',', ' ')

wb = Workbook(); ws = wb.active; ws.title = "Comptage"

INK = 'FF1B201D'; VERT = 'FF2F5E4D'; GRIS = 'FF7D8783'; ROUGE = 'FF9C3D2C'
f_titre = Font(name='Arial', size=15, bold=True, color=INK)
f_sous  = Font(name='Arial', size=10, color=GRIS)
f_tete  = Font(name='Arial', size=9, bold=True, color='FFFFFFFF')
f_corps = Font(name='Arial', size=10, color=INK)
f_gras  = Font(name='Arial', size=10, bold=True, color=INK)
fill_tete   = PatternFill('solid', fgColor=VERT)
fill_saisie = PatternFill('solid', fgColor='FFFFF3C4')
fill_alt    = PatternFill('solid', fgColor='FFF4F5F2')
bord = Border(*[Side(style='thin', color='FFD6DAD5')] * 4)

ws['A1'] = "Comptage prioritaire — Perfumes Trade"; ws['A1'].font = f_titre
ws['A2'] = ("20 références sur les 1 892 en stock. Elles n'ont jamais été comptées et portent "
            + dollars(total_top) + " $ au prix d'achat, soit "
            + str(round(total_top / total_stock * 100)) + " % de la valeur de tout l'inventaire.")
ws['A2'].font = f_sous
ws['A3'] = ("Choisies par la valeur, rangées par ordre alphabétique de marque : c'est l'ordre "
            "des étagères, pas celui de l'importance. On ne traverse le dépôt qu'une fois.")
ws['A3'].font = f_sous
ws['A4'] = "À remplir : la colonne jaune « Compté ». Le reste se calcule tout seul."
ws['A4'].font = Font(name='Arial', size=10, bold=True, color=VERT)

COLS = [("#", 4), ("Marque", 22), ("Nom", 30), ("Cont.", 7), ("Type", 7),
        ("Code-barres", 19), ("Attendu", 9), ("Compté", 10), ("Écart", 8),
        ("Prix d'achat", 11), ("Valeur de l'écart", 14), ("Remarque", 30)]
L = 6
for i, (t, w) in enumerate(COLS, 1):
    c = ws.cell(L, i, t); c.font = f_tete; c.fill = fill_tete
    c.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
    ws.column_dimensions[get_column_letter(i)].width = w
ws.row_dimensions[L].height = 26

for n, r in enumerate(top, 1):
    ln = L + n
    bc = str(r[0] or '')
    # deux codes-barres collés dans la même case du fichier d'origine : repéré le 8 sept.
    casse = len(bc) > 14
    lignes = [n, r[2] or '', r[1] or '', r[3] or '', r[4] or '',
              (bc[:13] + " ??") if casse else bc, r[6], None,
              '=IF(H%d="","",H%d-G%d)' % (ln, ln, ln),
              r[12] or 0,
              '=IF(H%d="","",(H%d-G%d)*J%d)' % (ln, ln, ln, ln),
              "Code-barres illisible : relever celui du flacon" if casse else ""]
    for i, v in enumerate(lignes, 1):
        c = ws.cell(ln, i, v); c.font = f_corps; c.border = bord
        if n % 2 == 0: c.fill = fill_alt
        if i in (1, 4, 5, 7, 9): c.alignment = Alignment(horizontal='center')
        if i == 7:  c.number_format = '#,##0'
        if i == 10: c.number_format = '#,##0.00 $'
        if i == 11: c.number_format = '#,##0 $;[Red]-#,##0 $;-'
        if i == 8:
            c.fill = fill_saisie; c.number_format = '#,##0'
            c.alignment = Alignment(horizontal='center')
        if i == 12:
            # sans retour a la ligne, la remarque deborde de sa colonne et se fait
            # couper au bord de la page a l'impression : l'instruction devient illisible
            # exactement sur la ligne ou elle sert.
            c.alignment = Alignment(wrap_text=True, vertical='center')
            if casse: c.font = Font(name='Arial', size=8.5, color=ROUGE)
    ws.row_dimensions[ln].height = 26 if casse else 17

F = L + len(top) + 1
c = ws.cell(F, 6, "Total"); c.font = f_gras; c.alignment = Alignment(horizontal='right')
c = ws.cell(F, 7, '=SUM(G%d:G%d)' % (L + 1, L + len(top))); c.font = f_gras; c.number_format = '#,##0'
c = ws.cell(F, 8, '=IF(COUNT(H%d:H%d)=0,"",SUM(H%d:H%d))' % (L + 1, L + len(top), L + 1, L + len(top)))
c.font = f_gras; c.number_format = '#,##0'; c.fill = fill_saisie
c = ws.cell(F, 11, '=IF(COUNT(H%d:H%d)=0,"",SUM(K%d:K%d))' % (L + 1, L + len(top), L + 1, L + len(top)))
c.font = f_gras; c.number_format = '#,##0 $;[Red]-#,##0 $;-'
# Combien de lignes sont réellement faites : sans ce repère, le total « Compté »
# se lit à côté du total « Attendu » comme s'il portait sur les mêmes références,
# alors qu'il ne compte que ce qui est rempli. Deux lignes comptées sur vingt
# afficheraient un manque énorme qui n'existe pas.
c = ws.cell(F, 12, '=COUNT(H%d:H%d)&" ligne(s) comptée(s) sur %d"' % (L + 1, L + len(top), len(top)))
c.font = f_sous

# L'écart rapporté à ce qui était attendu : c'est LUI qui décide, pas le montant
# brut. Le dénominateur ne porte QUE sur les lignes déjà comptées — sinon, tant
# que le comptage est en cours, on divise un écart partiel par une valeur totale
# et le pourcentage minimise le problème exactement quand on le regarde.
c = ws.cell(F + 1, 6, "Écart en % de la valeur des lignes comptées"); c.font = f_sous
c.alignment = Alignment(horizontal='right')
c = ws.cell(F + 1, 11,
            '=IF(COUNT(H%d:H%d)=0,"",SUM(K%d:K%d)/SUMPRODUCT((H%d:H%d<>"")*G%d:G%d*J%d:J%d))'
            % (L + 1, L + len(top), L + 1, L + len(top), L + 1, L + len(top),
               L + 1, L + len(top), L + 1, L + len(top)))
c.font = f_gras; c.number_format = '0.0%'
c = ws.cell(F + 1, 12, "Sous 2 % : on importe.\nAu-delà : on cherche d'abord.")
c.font = Font(name='Arial', size=9, color=VERT)
c.alignment = Alignment(wrap_text=True, vertical='top')
ws.row_dimensions[F + 1].height = 28

G = F + 3
ws.cell(G, 1, "Comment lire le résultat").font = Font(name='Arial', size=11, bold=True, color=INK)
for k, t in enumerate([
    ("Écart négatif : il y a moins de flacons que ce que dit le Google Sheet. "
     "C'est le cas le plus courant, et le plus coûteux.", INK),
    ("Écart positif : il y en a plus. Souvent une réception saisie deux fois, "
     "ou un retour jamais enregistré.", INK),
    ("Si l'écart total tient sous 2 % de la valeur attendue, le Google Sheet est fiable : "
     "on l'importe tel quel et on n'en reparle plus.", VERT),
    ("Au-delà : on ne l'importe pas sans avoir compris d'où vient l'écart. Sinon toutes "
     "les marges de l'ERP héritent de la même erreur.", ROUGE),
], 1):
    ws.cell(G + k, 1, "• " + t[0]).font = Font(name='Arial', size=10, color=t[1])

S = G + 6
ws.cell(S, 1, "D'où viennent ces chiffres").font = Font(name='Arial', size=11, bold=True, color=INK)
for k, t in enumerate([
    "Source : l'inventaire Excel de DASY LLC repris dans l'ERP, colonne « vérifié » — "
    + str(len(avec)) + " références en stock sur " + str(len(d)) + ".",
    "Prix d'achat : la moyenne des achats, telle que l'ERP la calcule — règle fixée par Sam.",
    "Sélection : les 20 plus grosses valeurs (quantité × prix d'achat) parmi les "
    + str(len(douteux)) + " références en stock jamais comptées ou marquées « à vérifier ».",
    "Ces " + str(len(douteux)) + " références portent " + dollars(total_douteux) + " $, soit "
    + str(round(total_douteux / total_stock * 100)) + " % de la valeur totale du stock ("
    + dollars(total_stock) + " $).",
    "Feuille produite le 9 septembre 2026 par l'ERP Perfumes Trade.",
], 1):
    ws.cell(S + k, 1, "• " + t).font = Font(name='Arial', size=9, color=GRIS)

ws.freeze_panes = 'A7'
ws.print_area = 'A1:L%d' % (S + 6)
ws.page_setup.orientation = 'landscape'
ws.page_setup.fitToWidth = 1
ws.sheet_properties.pageSetUpPr.fitToPage = True
wb.save(D / 'comptage_prioritaire.xlsx')

print('%d références retenues, %s $ sur %s $ de stock' % (len(top), dollars(total_top), dollars(total_stock)))
print('jamais comptées : %d réf., %s $ (%d %%)'
      % (len(douteux), dollars(total_douteux), round(total_douteux / total_stock * 100)))
