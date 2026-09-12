# -*- coding: utf-8 -*-
"""Fabriquer un ERP VIERGE, prêt à être personnalisé pour un autre client.

Pourquoi ce fichier existe : tant que l'outil ne sait se construire que pour
DASY, ce n'est pas un produit, c'est une commande. Ce script fabrique la même
application sans une seule donnée de Sam dedans, sous le nom d'une autre
entreprise, et — c'est la partie qui compte — il DIT ce qui reste malgré tout
propre à Sam dans les pages produites.

Ce deuxième point n'est pas de la politesse. Un outil « vierge » qui garde
« Site perfumestrade.com » dans une liste déroulante, ou un onglet « Inventaire
Perfume City » qui parle de la boutique de la femme de Sam, se vend une fois et
se découvre chez le client. Mieux vaut la liste maintenant, écrite noir sur
blanc, que la découverte pendant une démonstration.

    python3 nouveau_client.py "Nom de l'entreprise" identifiant_org

Ce qui est vidé : le catalogue, les statistiques, les clients, les fournisseurs,
les factures d'exemple, les relevés de marché, le comparatif Google Sheet.
Ce qui n'est PAS touché : le code. C'est le même outil, exactement.
"""
import json, os, pathlib, re, shutil, subprocess, sys

SOURCE = pathlib.Path('/home/claude/catalogue')

# ---------------------------------------------------------------- les données
# Chaque fichier de données garde sa FORME (le code lit des clés précises) mais
# perd tout contenu. Une forme absente casse le build ; une forme vide ne casse
# rien et affiche « aucune donnée », ce que les pages savent déjà faire.
VIDE = {
    'cat.json': [],
    'stock.json': [],
    'marche.json': [],
    'cat_stats.json': {"total": 0, "enstock": 0, "rupture": 0, "photos": 0,
                       "marques": 0, "unites": 0, "an": {}, "anytot": 0},
    'stock_stats.json': {"total": 0, "enstock": 0, "rupture": 0, "u": 0, "cap": 0,
                         "ok": 0, "non": 0, "doute": 0, "capnon": 0, "paliers": {}},
    'clients_seed.json': {"date": "", "src": "", "clients": []},
    'frn_seed.json': {},
    'facture_seed.json': {"num": "", "frn": "", "d": "", "lignes": []},
    'marche_seed.json': {},
    'sheet_seed.json': {"date": "", "src": "", "q": {}, "det": {}, "prix": {}},
}

# ------------------------------------------------------- ce qui trahit DASY
# Chaque motif : (expression, ce que ça veut dire pour un autre client).
# On ne cherche pas « des traces de Sam » en vrac : on cherche ce qu'un client
# VERRAIT, et on l'explique en une phrase qu'on peut lire sans le code sous les yeux.
TRACES = [
    (r'perfumestrade\.com', "l'adresse du site de Sam — apparaît dans les canaux de vente et les connecteurs"),
    (r'Perfume City',       "la boutique de la femme de Sam — une rubrique entière lui est consacrée"),
    (r'DASY',               "la raison sociale de Sam, posée comme valeur par défaut"),
    (r'samamsellem',        "l'adresse Zelle de Sam"),
    (r'Test inventory sam', "le nom du fichier d'inventaire de Sam"),
    (r'Miami Trading Zone', "le fournisseur principal de Sam"),
    (r'\bJavier\b|\bCarmen\b|\bJuan Carlos\b', "des noms de clients grossistes de Sam"),
    (r'Lightspeed',         "sa caisse — un autre client en aura une autre"),
    (r'\bASIN\b|buy box',   "des colonnes propres à la vente sur Amazon"),
    (r'resale certificate|Florida', "des règles fiscales propres à la Floride"),
]

def dis(t=''): print(t, flush=True)

def main():
    if len(sys.argv) < 3:
        dis(__doc__); sys.exit(1)
    nom, org = sys.argv[1].strip(), sys.argv[2].strip().lower()
    if not re.fullmatch(r'[a-z0-9_-]{2,30}', org):
        dis("L'identifiant d'organisation : lettres minuscules, chiffres, tiret ou souligné."); sys.exit(1)

    cible = pathlib.Path('/home/claude/clients') / org
    if cible.exists(): shutil.rmtree(cible)
    cible.mkdir(parents=True)

    dis('=' * 66)
    dis('  ERP VIERGE pour « %s »  (organisation : %s)' % (nom, org))
    dis('=' * 66); dis()

    # 1. le code, tel quel — c'est le même outil, on ne le modifie pas
    n = 0
    for f in SOURCE.iterdir():
        # build_data.py et build_clients_data.py lisent l'Excel et le Google Sheet
        # de Sam : ils n'ont rien à faire dans une instance vierge. Les autres
        # build_*.py sont le produit lui-même et partent tels quels.
        if f.suffix == '.py' and not f.name.startswith(
                ('_test', 'test_', 'nouveau_client', 'verif', 'shot', 'patch', 'review', 'analyse')) \
                and f.name not in ('build_data.py', 'build_clients_data.py'):
            shutil.copy2(f, cible / f.name); n += 1
        elif f.suffix == '.css':
            shutil.copy2(f, cible / f.name); n += 1
    # les logos des canaux et des connecteurs : ce sont des marques (WooCommerce,
    # Shopify, Amazon), pas des données de Sam — ils servent à tout le monde.
    for img in SOURCE.glob('*.jpg'):
        shutil.copy2(img, cible / img.name); n += 1
    for dossier in ('logos', '_pdfjs'):
        d = SOURCE / dossier
        if d.is_dir():
            shutil.copytree(d, cible / dossier); n += 1
    dis('  %d fichiers de code copiés — le code n\'est pas modifié, c\'est le même outil' % n)

    # 2. les données, vidées
    for f, contenu in VIDE.items():
        (cible / f).write_text(json.dumps(contenu, ensure_ascii=False), encoding='utf-8')
    dis('  %d fichiers de données remis à zéro' % len(VIDE))

    dis()

    # 4. on construit
    dis('  Construction…')
    builds = sorted(f.name for f in cible.iterdir()
                    if f.name.startswith('build_') and f.name != 'build_data.py')
    rates = []
    for b in builds:
        r = subprocess.run([sys.executable, b], cwd=cible, capture_output=True, text=True, timeout=300)
        if r.returncode != 0:
            rates.append((b, (r.stderr or r.stdout).strip().splitlines()[-1] if (r.stderr or r.stdout).strip() else '?'))
    if rates:
        dis('  %d script(s) n\'ont pas pu tourner sur une base vide :' % len(rates))
        for b, e in rates: dis('     %-24s %s' % (b, e[:110]))
    else:
        dis('  tous les scripts ont tourné sur une base vide.')
    pages = sorted(f.name for f in cible.iterdir() if f.suffix == '.html')
    dis('  %d pages produites' % len(pages))

    # ------------------------------------------------------------------
    # L'ORGANISATION, INJECTÉE DANS CHAQUE PAGE.
    # Première version de ce script : un fichier org.js posé à côté, que rien
    # ne chargeait. COCKPIT_ORG restait donc indéfini, le code retombait sur
    # sa valeur par défaut — « dasy » — et un client tout neuf se serait mis à
    # écrire DANS LES DONNÉES DE SAM. Un fichier de configuration que personne
    # ne lit est pire que pas de configuration du tout : il rassure.
    # On l'écrit donc dans les pages elles-mêmes, avant le premier script, et
    # on vérifie juste après que chacune le porte.
    marque = ('<script>/* à qui appartient cette installation : posé par '
              'nouveau_client.py, lu par _comptes.py et _serveur.py */'
              'window.COCKPIT_ORG=%s;</script>' % json.dumps(org))
    # Une page sans script ne peut écrire nulle part : la marquer n'a pas de sens,
    # et l'annoncer comme un danger apprend à ignorer les avertissements. On ne
    # s'inquiète donc que des pages qui touchent VRAIMENT aux données.
    poses, manquees, inertes = 0, [], []
    for p in pages:
        f = cible / p
        t = f.read_text(encoding='utf-8', errors='ignore')
        i = t.find('<script')
        touche = ('localStorage' in t) or ('COCKPIT' in t)
        if i < 0:
            (manquees if touche else inertes).append(p); continue
        f.write_text(t[:i] + marque + t[i:], encoding='utf-8')
        poses += 1
    dis('  organisation « %s » inscrite dans %d page(s)' % (org, poses))
    if manquees:
        dis('  ATTENTION — pas inscrite dans : %s' % ', '.join(manquees))
        dis('  Ces pages écriraient dans les données de DASY. À corriger avant usage.')
    # relecture : on ne se croit pas sur parole
    if inertes:
        dis('  (%s : page sans script, ne touche à aucune donnée)' % ', '.join(inertes))
    sans = [p for p in pages if p not in inertes and ('COCKPIT_ORG=' + json.dumps(org)) not in
            (cible / p).read_text(encoding='utf-8', errors='ignore')]
    if sans:
        dis('  RELECTURE RATÉE sur : %s' % ', '.join(sans))
    else:
        dis('  relu : les %d pages qui écrivent portent bien « %s » et non « dasy »' % (poses, org))
    dis()

    # 5. LE POINT UTILE : ce qui reste de Sam dans les pages
    dis('=' * 66)
    dis('  CE QUI RESTE PROPRE À SAM DANS LES PAGES PRODUITES')
    dis('=' * 66)
    dis('  Un client verrait ceci. Tant que la liste n\'est pas vide, l\'outil')
    dis('  n\'est pas un produit — c\'est l\'outil de Sam avec les données ôtées.')
    dis()
    # Le dictionnaire de traduction est le MÊME sur les seize pages. Compter ses
    # entrées seize fois donnait un total effrayant qui ne désigne en réalité
    # qu'un seul endroit à corriger. On sépare donc les deux : ce qu'un client
    # LIT dans l'interface, et ce qui dort dans le dictionnaire — le premier se
    # corrige page par page, le second en une fois.
    DICO = re.compile(r'const MOTS=\{.*?\};', re.S)
    texte, dicos = {}, {}
    for p in pages:
        try: brut = (cible / p).read_text(encoding='utf-8', errors='ignore')
        except Exception: continue
        m = DICO.search(brut)
        dicos[p] = m.group(0) if m else ''
        texte[p] = DICO.sub('', brut)          # l'interface, dictionnaire ôté
    reste = 0
    au_dico = 0
    for motif, explication in TRACES:
        touchees = {p: len(re.findall(motif, t)) for p, t in texte.items() if re.search(motif, t)}
        n_dico = sum(len(re.findall(motif, d)) for d in dicos.values())
        if not touchees:
            if n_dico:
                au_dico += 1
                dis('  ○ %s' % explication)
                dis('    seulement dans le dictionnaire de traduction — un seul endroit à corriger')
                dis()
            continue
        reste += 1
        total = sum(touchees.values())
        haut = sorted(touchees.items(), key=lambda x: -x[1])[:4]
        dis('  ▸ %s' % explication)
        dis('    %d fois dans l\'interface, sur %d page(s) : %s'
            % (total, len(touchees), ', '.join('%s (%d)' % (p, c) for p, c in haut)))
        if n_dico: dis('    (+ %d entrées dans le dictionnaire de traduction)' % n_dico)
        dis()
    if not reste and not au_dico:
        dis('  Rien. L\'outil est générique.')
    elif not reste:
        dis('  Rien dans l\'interface. %d sujets ne vivent que dans le dictionnaire' % au_dico)
        dis('  de traduction : un seul fichier à reprendre.')
    else:
        dis('  %d sujets à traiter avant de vendre l\'outil à quelqu\'un d\'autre.' % reste)
    dis()
    dis('  Dossier : %s' % cible)

if __name__ == '__main__':
    main()
