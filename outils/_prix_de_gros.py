# Les références en stock qui n'ont AUCUN prix de gros.
#
# 530 références, 126 889 $ de marchandise au prix d'achat. Elles existent dans
# l'outil, elles sont physiquement sur les étagères, mais elles ne peuvent entrer
# dans aucun devis wholesale : il n'y a pas de prix à mettre dans la colonne.
#
# Trois décisions de fabrication :
#
#   - TRIÉ PAR VALEUR, pas par marque. Sam remplira ce fichier assis, pas en
#     marchant : l'ordre utile est celui de l'argent. Il peut s'arrêter à la
#     centième ligne en ayant couvert l'essentiel.
#   - LE PRIX D'ACHAT ET LE PRIX RETAIL SONT AFFICHÉS À CÔTÉ. Une colonne vide
#     sans repère se remplit au hasard ; avec les deux bornes sous les yeux, la
#     décision est informée.
#   - LA MARGE SE CALCULE PENDANT LA SAISIE. C'est le seul moyen de voir qu'on
#     vient de taper un prix sous le prix d'achat — ça s'est produit 35 fois dans
#     l'historique de la boutique, et personne ne l'avait remarqué.
import json, pathlib
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.formatting.rule import CellIsRule

D = pathlib.Path('/home/claude/catalogue')
d = json.load(open(D / 'cat.json'))
avec = [r for r in d if (r[6] or 0) > 0]
sans = [r for r in avec if not r[8]]                      # 8 = prix de gros
def val(r): return (r[6] or 0) * (r[12] or 0)
sans.sort(key=val, reverse=True)
total = sum(val(r) for r in sans)
def dollars(x): return format(round(x), ',d').replace(',', ' ')

wb = Workbook(); ws = wb.active; ws.title = "Prix de gros"
INK = 'FF1B201D'; VERT = 'FF2F5E4D'; GRIS = 'FF7D8783'; ROUGE = 'FF9C3D2C'
f_tete = Font(name='Arial', size=9, bold=True, color='FFFFFFFF')
f_corps = Font(name='Arial', size=10, color=INK)
f_sous = Font(name='Arial', size=10, color=GRIS)
fill_tete = PatternFill('solid', fgColor=VERT)
fill_saisie = PatternFill('solid', fgColor='FFFFF3C4')
fill_alt = PatternFill('solid', fgColor='FFF4F5F2')
bord = Border(*[Side(style='thin', color='FFD6DAD5')] * 4)

ws['A1'] = "Prix de gros à fixer — Perfumes Trade"
ws['A1'].font = Font(name='Arial', size=15, bold=True, color=INK)
ws['A2'] = (str(len(sans)) + " références en stock n'ont aucun prix de gros — "
            + dollars(total) + " $ de marchandise au prix d'achat. "
            "Sans ce prix, elles ne peuvent entrer dans aucun devis.")
ws['A2'].font = f_sous
ws['A3'] = ("Rangées de la plus grosse valeur à la plus petite : tu peux t'arrêter quand tu veux, "
            "l'essentiel sera fait.")
ws['A3'].font = f_sous
ws['A4'] = "À remplir : la colonne jaune « Prix de gros ». La marge se calcule pendant que tu tapes."
ws['A4'].font = Font(name='Arial', size=10, bold=True, color=VERT)

COLS = [("#", 5), ("Marque", 22), ("Nom", 32), ("Cont.", 7), ("Type", 7),
        ("Code-barres", 18), ("Stock", 8), ("Prix d'achat", 12), ("Prix retail", 11),
        ("PRIX DE GROS", 14), ("Marge", 9), ("Valeur du stock", 14)]
L = 6
for i, (t, w) in enumerate(COLS, 1):
    c = ws.cell(L, i, t); c.font = f_tete; c.fill = fill_tete
    c.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
    ws.column_dimensions[get_column_letter(i)].width = w
ws.row_dimensions[L].height = 26

for n, r in enumerate(sans, 1):
    ln = L + n
    lignes = [n, r[2] or '', r[1] or '', r[3] or '', r[4] or '', str(r[0] or ''),
              r[6], r[12] or 0, r[7],
              None,                                            # à remplir
              '=IF(J%d="","",IF(J%d<=0,"",(J%d-H%d)/J%d))' % (ln, ln, ln, ln, ln),
              val(r)]
    for i, v in enumerate(lignes, 1):
        c = ws.cell(ln, i, v); c.font = f_corps; c.border = bord
        if n % 2 == 0: c.fill = fill_alt
        if i in (1, 4, 5, 7): c.alignment = Alignment(horizontal='center')
        if i == 7: c.number_format = '#,##0'
        if i in (8, 9, 10): c.number_format = '#,##0.00 $'
        if i == 11: c.number_format = '0 %'
        if i == 12: c.number_format = '#,##0 $'
        if i == 10:
            c.fill = fill_saisie
            c.alignment = Alignment(horizontal='center')
    ws.row_dimensions[ln].height = 17

fin = L + len(sans)
# Une marge sous 10 % passe inapercue dans une colonne de 530 nombres. Elle se
# colore donc toute seule : rouge sous zero (on vend a perte), orange sous 10 %.
ws.conditional_formatting.add('K%d:K%d' % (L + 1, fin),
    CellIsRule(operator='lessThan', formula=['0'],
               font=Font(color='FFFFFFFF', bold=True), fill=PatternFill('solid', fgColor='FFB3261E')))
ws.conditional_formatting.add('K%d:K%d' % (L + 1, fin),
    CellIsRule(operator='between', formula=['0', '0.1'],
               font=Font(color='FF8A5A00', bold=True), fill=PatternFill('solid', fgColor='FFFBF3E2')))

f = fin + 1
c = ws.cell(f, 9, "Total"); c.font = Font(name='Arial', size=10, bold=True, color=INK)
c.alignment = Alignment(horizontal='right')
c = ws.cell(f, 10, '=COUNT(J%d:J%d)&" / %d remplis"' % (L + 1, fin, len(sans)))
c.font = f_sous
c = ws.cell(f, 12, '=SUM(L%d:L%d)' % (L + 1, fin))
c.font = Font(name='Arial', size=10, bold=True, color=INK); c.number_format = '#,##0 $'

g = f + 2
ws.cell(g, 1, "Comment lire les couleurs").font = Font(name='Arial', size=11, bold=True, color=INK)
for k, (t, col) in enumerate([
    ("Marge en ROUGE : le prix tapé est sous le prix d'achat. On vend à perte.", ROUGE),
    ("Marge en ORANGE : sous 10 %. C'est le seuil que l'ERP signale déjà sur le tableau de bord.", 'FF8A5A00'),
    ("Le prix retail est là comme borne haute : le prix de gros se situe entre les deux.", INK),
    ("Les 7 références sans aucun prix nulle part sont dans prix_a_valider.xlsx, pas ici.", GRIS),
], 1):
    ws.cell(g + k, 1, "• " + t).font = Font(name='Arial', size=10, color=col)

s = g + 6
ws.cell(s, 1, "D'où viennent ces chiffres").font = Font(name='Arial', size=11, bold=True, color=INK)
for k, t in enumerate([
    "Source : l'inventaire de DASY LLC repris dans l'ERP — " + str(len(avec))
    + " références en stock, dont " + str(len(sans)) + " sans prix de gros.",
    "Prix d'achat : la moyenne des achats, telle que l'ERP la calcule.",
    "Prix retail : celui du catalogue ; vide quand la référence n'en a pas.",
    "Valeur du stock : quantité × prix d'achat. Total sur ces " + str(len(sans))
    + " références : " + dollars(total) + " $.",
    "Fichier produit le 10 septembre 2026 par l'ERP Perfumes Trade.",
], 1):
    ws.cell(s + k, 1, "• " + t).font = Font(name='Arial', size=9, color=GRIS)

ws.freeze_panes = 'A7'
ws.auto_filter.ref = 'A%d:L%d' % (L, fin)
wb.save(D / 'prix_de_gros_a_fixer.xlsx')
print('%d références, %s $ de stock concerné' % (len(sans), dollars(total)))
