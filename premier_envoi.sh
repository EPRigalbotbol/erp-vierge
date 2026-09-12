#!/bin/bash
# Premier envoi de l'ERP vierge vers GitHub. À lancer UNE fois, après avoir créé
# le dépôt privé « erp-vierge » sur github.com/EPRigalbotbol.
# Usage : bash ~/Desktop/erp-vierge/premier_envoi.sh
cd "$(dirname "$0")" || exit 1
[ -d .git ] || git init -q -b master
git add -A .
git -c user.name="Igal Botbol" -c user.email="assistance@igalbotbol.com" commit -q -m "ERP vierge : premiere version" || true
git remote remove origin 2>/dev/null
git remote add origin git@github.com:EPRigalbotbol/erp-vierge.git
git push -u origin master && echo "Poussé sur GitHub : EPRigalbotbol/erp-vierge"
