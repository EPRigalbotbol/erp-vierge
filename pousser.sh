#!/bin/bash
# Pousse l'ERP de démonstration (vierge) vers GitHub ; Coolify redéploie tout seul.
# Usage : bash ~/Desktop/erp-vierge/pousser.sh "message"
cd "$(dirname "$0")" || exit 1
rm -f .git/*.lock .git/refs/heads/*.lock 2>/dev/null
git add -A .
if git diff --cached --quiet; then echo "Rien à pousser : tout est déjà en ligne."; else
  git -c user.name="Igal Botbol" -c user.email="assistance@igalbotbol.com" commit -q -m "${1:-Mise à jour}" && echo "Enregistré : ${1:-Mise à jour}"
fi
git push origin master && echo "Poussé. Coolify redéploie (environ 40 secondes)."
