# ERP vierge (démonstration)

La même application que Perfumes Trade, sans une seule donnée de Sam : catalogue,
stock, clients, fournisseurs, ventes sont vides. Organisation cockpit : `demo`.

- `outils/` : les scripts de fabrication (build_*.py). Pour refabriquer les pages :
  `cd outils && for b in build_*.py; do python3 $b; done` puis copier les .html à la racine.
- `outils/nouveau_client.py` : fabrique une instance vierge pour une autre organisation.
- `pousser.sh` : met en ligne (GitHub → Coolify).
- Mise en ligne : Coolify, image Dockerfile, argument de build SITE_PASS, domaine demo.igalbotbol.com,
  et `https://demo.igalbotbol.com` ajouté à CORS_ORIGINS du cockpit.
