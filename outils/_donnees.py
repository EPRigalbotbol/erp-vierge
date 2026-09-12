# -*- coding: utf-8 -*-
"""Les données de l'entreprise, posées à côté de l'outil et non plus dedans.

Avant : chaque page recopiait les 3 830 références de Sam dans son propre HTML.
`catalogue.html` pesait 1,1 Mo dont 70 % de son stock, `factures.html` 2,1 Mo.
Installer SAM ailleurs revenait à livrer le stock de Sam avec.

Maintenant : un seul fichier `donnees/produits.js` que toutes les pages chargent
avant de démarrer. L'outil d'un côté, l'entreprise de l'autre. C'est aussi la
marche à suivre pour la suite : le jour où il y a un serveur, ce fichier est
remplacé par un appel à la base, et les pages ne changent pas.
"""
import json, os


def pose(nom, valeur, variable):
    """Écrit donnees/<nom>.js contenant `window.<variable> = <valeur>;`"""
    os.makedirs('donnees', exist_ok=True)
    txt = valeur if isinstance(valeur, str) else json.dumps(
        valeur, ensure_ascii=False, separators=(',', ':'))
    chemin = os.path.join('donnees', nom + '.js')
    open(chemin, 'w').write('window.%s=%s;\n' % (variable, txt))
    return chemin


def produits():
    """Le catalogue brut, tel que le lisent toutes les rubriques."""
    return pose('produits', open('cat.json').read(), 'D_PROD')


def projection(indices):
    """L'expression JS qui refait, à partir de D_PROD, l'index que la page attendait.

    `indices` est la liste des colonnes voulues, dans l'ordre — les mêmes numéros
    que ceux qui étaient écrits en Python dans chaque build_*.py.
    """
    cols = ','.join('r[%d]' % i for i in indices)
    return 'Object.fromEntries(window.D_PROD.map(r=>[r[15],[%s]]))' % cols


# Quel fichier remplit quelle variable. Sert au garde-fou ci-dessous.
GLOBALS = {'produits': 'D_PROD', 'clients': 'D_CLI', 'inventaire': 'D_INV',
           'inventaire_pc': 'D_INV_PC', 'retail': 'D_RETAIL'}


def garde(noms):
    """Si un fichier de données manque, la page le dit au lieu de planter.

    Le cas arrive pour de vrai : quelqu'un copie « catalogue.html » tout seul
    sur un autre poste et se retrouve devant une page morte, sans savoir pourquoi.
    """
    manque = [(n, GLOBALS[n]) for n in noms if n in GLOBALS]
    if not manque:
        return ''
    tests = ' || '.join("typeof window.%s==='undefined'" % v for _, v in manque)
    liste = ', '.join('donnees/%s.js' % n for n, _ in manque)
    return """<script>
if (%s) {
  /* Le code de la page est lancé plus tard par l'amorce (voir _serveur.py) : ce drapeau
     l'empêche de démarrer sur des données absentes — sinon la page enchaîne les erreurs
     au lieu d'afficher l'explication ci-dessous. */
  window.__DONNEES_MANQUENT = true;
  document.addEventListener('DOMContentLoaded', function () {
    document.body.innerHTML =
      '<div style="max-width:620px;margin:80px auto;padding:34px 32px;font-family:Inter,system-ui,sans-serif;'
      + 'background:#fff;border:1px solid #E4DFD7;border-radius:12px;color:#17171D">'
      + '<h2 style="margin:0 0 12px;font-size:20px">Il manque le dossier des donn&eacute;es</h2>'
      + '<p style="margin:0 0 10px;font-size:14.5px;line-height:1.65;color:#4A4A56">'
      + 'Cette page a besoin de <b>%s</b>, qui doit se trouver dans un dossier '
      + '<b>donnees</b> plac&eacute; juste &agrave; c&ocirc;t&eacute;.</p>'
      + '<p style="margin:0;font-size:14.5px;line-height:1.65;color:#4A4A56">'
      + 'Cela arrive quand on copie une page toute seule ailleurs. Rouvre SAM depuis le dossier '
      + '<b>perfumestrade</b>, o&ugrave; tout est au bon endroit.</p></div>';
  });
}
</script>""" % (tests, liste)
