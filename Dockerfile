# Perfumes Trade — mise en ligne de la version navigateur, derrière une porte.
# Le serveur demande un identifiant et un mot de passe AVANT d'afficher quoi
# que ce soit : c'est la vraie serrure, en attendant les comptes côté serveur.
# Les scripts de fabrication (build_*.py) ne sont pas copies : seul le résultat
# (pages, données, photos) part sur le serveur.
FROM nginx:1.27-alpine
ARG SITE_USER=perfumestrade
ARG SITE_PASS
RUN test -n "$SITE_PASS" || (echo "SITE_PASS manquant" && exit 1) \
 && apk add --no-cache apache2-utils \
 && htpasswd -nbm "$SITE_USER" "$SITE_PASS" > /etc/nginx/.htpasswd \
 && apk del apache2-utils
COPY nginx.conf /etc/nginx/conf.d/default.conf
WORKDIR /usr/share/nginx/html
COPY *.html *.css accueil.jpg ./
COPY donnees ./donnees
COPY logos ./logos
COPY photos ./photos
# les moteurs de lecture des PDF et des photos (servis par l'outil : rien ne part ailleurs)
COPY lib ./lib
