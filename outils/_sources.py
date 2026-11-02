# -*- coding: utf-8 -*-
"""Quels fichiers font le SOURCE du projet : de quoi refabriquer toutes les pages, sans rien d'autre.

Une seule définition, utilisée par trois choses qui doivent toujours être d'accord :
  - le test de reconstruction (_test_reconstruction.py) : refait les pages depuis ces fichiers seuls,
    dans un dossier vide, et vérifie qu'elles sont identiques à celles en ligne ;
  - le manifeste (MANIFESTE_SOURCES.sha256) : la liste de ces fichiers avec leur empreinte, que l'on
    peut vérifier sur le Mac (« le dépôt contient-il bien TOUT le source ? ») ;
  - le paquet de mise en ligne : le dossier outils/ du dépôt reçoit exactement ces fichiers.
"""
import glob, hashlib, os

# Les « graines » : données de départ, déjà extraites des tableurs de Sam. Les refaire demande les tableurs
# (build_data.py, build_clients_data.py, build_stock_data.py) — ce n'est pas le rôle de la reconstruction.
INGESTION = {'build_data.py', 'build_clients_data.py', 'build_stock_data.py', 'build_rapport.py'}
IMAGES = ['accueil.jpg', 'accueil_web.jpg']
DOSSIERS = ['logos', '_fixtures']

def fichiers_sources(racine='.'):
    """Chemins relatifs (avec /), triés."""
    r = []
    for motif in ('*.py', '*.css', '*.json', '*.md', '*.sh', '*.command', '_fixture*'):
        r += [os.path.basename(p) for p in glob.glob(os.path.join(racine, motif)) if os.path.isfile(p)]
    r += [i for i in IMAGES if os.path.exists(os.path.join(racine, i))]
    for d in DOSSIERS:
        for p in glob.glob(os.path.join(racine, d, '**', '*'), recursive=True):
            if os.path.isfile(p): r.append(os.path.relpath(p, racine).replace(os.sep, '/'))
    return sorted(set(x for x in r if not x.startswith('.') and not x.endswith(('.orig', '.rej'))))

def empreinte(chemin):
    h = hashlib.sha256()
    with open(chemin, 'rb') as f:
        for bloc in iter(lambda: f.read(1 << 20), b''): h.update(bloc)
    return h.hexdigest()

def manifeste(racine='.'):
    """Lignes au format de « shasum -a 256 -c » : '<empreinte>  <chemin>'."""
    return [empreinte(os.path.join(racine, p)) + '  ' + p for p in fichiers_sources(racine)]
