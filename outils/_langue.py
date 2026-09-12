# -*- coding: utf-8 -*-
"""L'ERP en trois langues : français, anglais, espagnol.

Le principe, tenu volontairement simple : les pages restent écrites en français,
et une couche de traduction remplace les mots à l'affichage. Un dictionnaire
français → anglais / espagnol, appliqué au texte visible et aux libellés
(placeholder, title, aria-label), y compris sur ce que le JavaScript ajoute
après coup (un observateur repasse dessus).

Pourquoi comme ça plutôt qu'en réécrivant les douze pages : parce qu'on peut
avancer par étapes. Ce qui est dans le dictionnaire est traduit, le reste reste
en français et se voit — donc se complète au fur et à mesure, sans jamais rien
casser.

Ce qui n'est jamais traduit : les données de l'entreprise. Une marque, un nom de
parfum, un nom de client ne se traduisent pas — et comme la traduction ne
s'applique qu'aux textes reconnus mot pour mot, ils passent au travers.
"""

# Le dictionnaire. Une entrée = français : [anglais, espagnol].
MOTS = {
    # ---- barre de gauche ----
    "Produits": ["Products", "Productos"],
    "Commerce": ["Sales", "Comercial"],
    "Pilotage": ["Management", "Dirección"],
    "Catalogue": ["Catalog", "Catálogo"],
    "Inventaire": ["Inventory", "Inventario"],
    "Prix & marges": ["Prices & margins", "Precios y márgenes"],
    "Factures": ["Invoices", "Facturas"],
    "Ventes": ["Sales", "Ventas"],
    "Fournisseurs": ["Suppliers", "Proveedores"],
    "Mes fournisseurs": ["My suppliers", "Mis proveedores"],
    "VIP wholesale": ["VIP wholesale", "Mayoristas VIP"],
    "Offres": ["Offers", "Ofertas"],
    "Connecteurs": ["Connectors", "Conectores"],
    "Journal": ["Activity log", "Registro"],
    "Journal des actions": ["Activity log", "Registro de acciones"],
    "Journal des ventes": ["Sales log", "Registro de ventas"],
    "Tableau de bord": ["Dashboard", "Panel de control"],
    "Accès": ["Access", "Accesos"],
    "Réglages": ["Settings", "Ajustes"],
    "bientôt": ["soon", "pronto"],
    "à brancher": ["to connect", "por conectar"],
    "par canal": ["by channel", "por canal"],
    "comptes": ["accounts", "cuentas"],
    "actions": ["actions", "acciones"],
    "Se déconnecter": ["Sign out", "Cerrar sesión"],
    "Modifier le menu": ["Edit the menu", "Editar el menú"],
    "Mon menu": ["My menu", "Mi menú"],
    "Patron": ["Owner", "Jefe"],
    "Commercial": ["Sales rep", "Comercial"],
    "Entrepôt": ["Warehouse", "Almacén"],
    "Comptable": ["Accountant", "Contable"],

    # ---- recherche et filtres ----
    "Rechercher": ["Search", "Buscar"],
    "Rechercher une marque, un nom, un code-barres…":
        ["Search a brand, a name, a barcode…", "Buscar una marca, un nombre, un código de barras…"],
    "Rechercher une marque, un nom, un code-barres… ou scanner":
        ["Search a brand, a name, a barcode… or scan", "Buscar marca, nombre, código… o escanear"],
    "Chercher un produit, un client, un numéro…":
        ["Search a product, a customer, a number…", "Buscar un producto, un cliente, un número…"],
    "Chercher un client…": ["Search a customer…", "Buscar un cliente…"],
    "Chercher une référence, un nom, un code-barres…":
        ["Search a reference, a name, a barcode…", "Buscar una referencia, un nombre, un código…"],
    "Effacer la recherche": ["Clear the search", "Borrar la búsqueda"],
    "En stock": ["In stock", "En stock"],
    "Historique": ["History", "Histórico"],
    "Tout": ["All", "Todo"],
    "Toutes les marques": ["All brands", "Todas las marcas"],
    "Tous genres": ["All genders", "Todos los géneros"],
    "Tous types": ["All types", "Todos los tipos"],
    "Tous les canaux": ["All channels", "Todos los canales"],
    "Tous les statuts": ["All statuses", "Todos los estados"],
    "Toutes les ventes": ["All sales", "Todas las ventas"],
    "Toutes les actions": ["All actions", "Todas las acciones"],
    "Plus de filtres": ["More filters", "Más filtros"],
    "Affiner": ["Refine", "Afinar"],
    "Photo : toutes": ["Photo: all", "Foto: todas"],
    "Avec photo": ["With photo", "Con foto"],
    "Sans photo": ["Without photo", "Sin foto"],
    "Fiches : toutes": ["Records: all", "Fichas: todas"],
    "Ajoutées à la main": ["Added by hand", "Añadidas a mano"],
    "Modifiées": ["Modified", "Modificadas"],
    "À compléter": ["To complete", "Por completar"],
    "à compléter": ["to complete", "por completar"],
    "Prix : tous": ["Prices: all", "Precios: todos"],
    "Tri": ["Sort", "Orden"],
    "Tri : marque": ["Sort: brand", "Orden: marca"],
    "Tri : stock ↓": ["Sort: stock ↓", "Orden: stock ↓"],
    "Tri : prix gros ↑": ["Sort: wholesale price ↑", "Orden: precio mayorista ↑"],
    "Stock faible sous": ["Low stock below", "Stock bajo por debajo de"],
    "Mode client": ["Customer mode", "Modo cliente"],
    "Prix repris du site *": ["Prices taken from the site *", "Precios tomados de la web *"],
    "Disponibilité": ["Availability", "Disponibilidad"],
    "Vignettes": ["Cards", "Fichas"],
    "Liste": ["List", "Lista"],
    "▦ Vignettes": ["▦ Cards", "▦ Fichas"],
    "☰ Liste": ["☰ List", "☰ Lista"],
    "Tout afficher": ["Show all", "Mostrar todo"],
    "Afficher plus": ["Show more", "Mostrar más"],
    "Vider": ["Clear", "Vaciar"],

    # ---- colonnes et champs ----
    "Marque": ["Brand", "Marca"],
    "marque": ["brand", "marca"],
    "Produit": ["Product", "Producto"],
    "Type": ["Type", "Tipo"],
    "type": ["type", "tipo"],
    "Genre": ["Gender", "Género"],
    "genre": ["gender", "género"],
    "Homme": ["Men", "Hombre"],
    "Femme": ["Women", "Mujer"],
    "Unisexe": ["Unisex", "Unisex"],
    "Enfant": ["Kids", "Niños"],
    "Stock": ["Stock", "Stock"],
    "Code-barres": ["Barcode", "Código de barras"],
    "code-barres": ["barcode", "código de barras"],
    "Contenance (oz)": ["Size (oz)", "Contenido (oz)"],
    "contenance": ["size", "contenido"],
    "Prix": ["Price", "Precio"],
    "Prix d'achat": ["Purchase price", "Precio de compra"],
    "prix achat": ["purchase price", "precio de compra"],
    "Prix retail": ["Retail price", "Precio retail"],
    "Prix de gros": ["Wholesale price", "Precio mayorista"],
    "prix unitaire": ["unit price", "precio unitario"],
    "Prix d'achat unitaire ($)": ["Unit purchase price ($)", "Precio de compra unitario ($)"],
    "Marge nette": ["Net margin", "Margen neto"],
    "Achat": ["Purchase", "Compra"],
    "Gros": ["Wholesale", "Mayorista"],
    "gros": ["wholesale", "mayorista"],
    "retail": ["retail", "retail"],
    "Capital": ["Capital", "Capital"],
    "Quantité en stock": ["Quantity in stock", "Cantidad en stock"],
    "Quantité achetée": ["Quantity purchased", "Cantidad comprada"],
    "quantité": ["quantity", "cantidad"],
    "flacons": ["bottles", "frascos"],
    "Nom du parfum": ["Perfume name", "Nombre del perfume"],
    "nom": ["name", "nombre"],
    "Nom du client": ["Customer name", "Nombre del cliente"],
    "Nom du fournisseur": ["Supplier name", "Nombre del proveedor"],
    "Nom de la personne": ["Person's name", "Nombre de la persona"],
    "Fournisseur": ["Supplier", "Proveedor"],
    "Client (facultatif)": ["Customer (optional)", "Cliente (opcional)"],
    "Note (facultatif)": ["Note (optional)", "Nota (opcional)"],
    "Numéro (facultatif)": ["Number (optional)", "Número (opcional)"],
    "Numéro": ["Number", "Número"],
    "Date": ["Date", "Fecha"],
    "Quand": ["When", "Cuándo"],
    "Canal": ["Channel", "Canal"],
    "Canal de vente": ["Sales channel", "Canal de venta"],
    "Statut": ["Status", "Estado"],
    "Motif": ["Reason", "Motivo"],
    "Remarque": ["Note", "Observación"],
    "Coordonnées": ["Contact details", "Datos de contacto"],
    "Téléphone du fournisseur": ["Supplier phone", "Teléfono del proveedor"],
    "E-mail du fournisseur": ["Supplier e-mail", "Correo del proveedor"],
    "Identifiant": ["Username", "Usuario"],
    "Mot de passe": ["Password", "Contraseña"],
    "Répéter": ["Repeat", "Repetir"],
    "Rôle": ["Role", "Rol"],
    "Personne": ["Person", "Persona"],
    "Ouvert le": ["Opened on", "Abierto el"],
    "Dernière connexion": ["Last sign-in", "Última conexión"],
    "Envoyer à": ["Send to", "Enviar a"],
    "Écart": ["Difference", "Diferencia"],
    "Théorique": ["Expected", "Teórico"],
    "Compté": ["Counted", "Contado"],
    "Comptage": ["Count", "Recuento"],
    "Vente": ["Sale", "Venta"],
    "Ses commandes": ["Their orders", "Sus pedidos"],
    "Fiche": ["Record", "Ficha"],

    # ---- boutons ----
    "Enregistrer": ["Save", "Guardar"],
    "Enregistrer la vente": ["Save the sale", "Guardar la venta"],
    "Enregistrer une vente": ["Record a sale", "Registrar una venta"],
    "+ Enregistrer une vente": ["+ Record a sale", "+ Registrar una venta"],
    "Enregistrer la facture": ["Save the invoice", "Guardar la factura"],
    "Enregistrer une facture": ["Record an invoice", "Registrar una factura"],
    "Enregistrer l'achat": ["Save the purchase", "Guardar la compra"],
    "Enregistrer un achat": ["Record a purchase", "Registrar una compra"],
    "Enregistrer l'ajustement": ["Save the adjustment", "Guardar el ajuste"],
    "Enregistrer le remboursement": ["Save the refund", "Guardar el reembolso"],
    "Enregistrer le relevé": ["Save the reading", "Guardar el registro"],
    "Annuler": ["Cancel", "Cancelar"],
    "Fermer": ["Close", "Cerrar"],
    "Fermer (Échap)": ["Close (Esc)", "Cerrar (Esc)"],
    "Appliquer": ["Apply", "Aplicar"],
    "Ajouter": ["Add", "Añadir"],
    "+ Nouvel article": ["+ New item", "+ Nuevo artículo"],
    "Nouvel article": ["New item", "Nuevo artículo"],
    "+ Ajouter un canal": ["+ Add a channel", "+ Añadir un canal"],
    "+ Ouvrir un accès": ["+ Open an access", "+ Abrir un acceso"],
    "Ouvrir un accès": ["Open an access", "Abrir un acceso"],
    "Ouvrir l'accès": ["Open the access", "Abrir el acceso"],
    "Imprimer": ["Print", "Imprimir"],
    "Exporter": ["Export", "Exportar"],
    "Exporter en CSV": ["Export to CSV", "Exportar a CSV"],
    "Exporter (CSV)": ["Export (CSV)", "Exportar (CSV)"],
    "Exporter mes corrections": ["Export my corrections", "Exportar mis correcciones"],
    "Sauvegarder mon travail": ["Back up my work", "Guardar mi trabajo"],
    "Télécharger la sauvegarde": ["Download the backup", "Descargar la copia"],
    "Restaurer un fichier…": ["Restore a file…", "Restaurar un archivo…"],
    "Mettre à jour le stock": ["Update the stock", "Actualizar el stock"],
    "Mettre le stock à jour": ["Update the stock", "Actualizar el stock"],
    "Mettre à jour depuis un fichier…": ["Update from a file…", "Actualizar desde un archivo…"],
    "Importer un fichier": ["Import a file", "Importar un archivo"],
    "Choisis un fichier": ["Choose a file", "Elige un archivo"],
    "Analyser les lignes": ["Analyse the lines", "Analizar las líneas"],
    "Préparer un inventaire": ["Prepare a count", "Preparar un inventario"],
    "Préparer un inventaire…": ["Prepare a count…", "Preparar un inventario…"],
    "Feuille de comptage": ["Count sheet", "Hoja de recuento"],
    "Enlever les étiquettes": ["Remove the labels", "Quitar las etiquetas"],
    "Effacer la saisie": ["Clear the entries", "Borrar lo introducido"],
    "Ajuster le stock": ["Adjust the stock", "Ajustar el stock"],
    "Confirmer les prix": ["Confirm the prices", "Confirmar los precios"],
    "Relance de paiement": ["Payment reminder", "Recordatorio de pago"],
    "Copier le texte": ["Copy the text", "Copiar el texto"],
    "Ouvrir dans Mail": ["Open in Mail", "Abrir en Mail"],
    "Revenir à la fiche": ["Back to the record", "Volver a la ficha"],
    "Revenir aux valeurs de départ": ["Back to the starting values", "Volver a los valores iniciales"],
    "Voir le tableau de bord": ["See the dashboard", "Ver el panel"],
    "Précédent": ["Previous", "Anterior"],
    "Suivant": ["Next", "Siguiente"],
    "Précédent (←)": ["Previous (←)", "Anterior (←)"],
    "Suivant (→)": ["Next (→)", "Siguiente (→)"],
    "Un de plus": ["One more", "Uno más"],
    "Un de moins": ["One less", "Uno menos"],
    "OK, enregistrer": ["OK, save", "OK, guardar"],
    "Annuler une vente ou rembourser": ["Cancel a sale or refund", "Anular una venta o reembolsar"],
    "Mode de remboursement": ["Refund method", "Forma de reembolso"],
    "Annulations": ["Cancellations", "Anulaciones"],
    "Saisie manuelle": ["Manual entry", "Entrada manual"],
    "Réceptions": ["Receipts", "Recepciones"],
    "Imports": ["Imports", "Importaciones"],

    # ---- périodes ----
    "Aujourd'hui": ["Today", "Hoy"],
    "7 derniers jours": ["Last 7 days", "Últimos 7 días"],
    "30 derniers jours": ["Last 30 days", "Últimos 30 días"],
    "90 derniers jours": ["Last 90 days", "Últimos 90 días"],
    "3 derniers mois": ["Last 3 months", "Últimos 3 meses"],
    "6 derniers mois": ["Last 6 months", "Últimos 6 meses"],
    "12 derniers mois": ["Last 12 months", "Últimos 12 meses"],
    "12 mois": ["12 months", "12 meses"],
    "Depuis toujours": ["All time", "Desde siempre"],
    "Toute la période": ["Whole period", "Todo el periodo"],
    "jours": ["days", "días"],

    # ---- réglages ----
    "Ma société": ["My company", "Mi empresa"],
    "Canaux de vente et règle de prix": ["Sales channels and pricing rule", "Canales de venta y regla de precios"],
    "Majoration": ["Mark-up", "Recargo"],
    "Commission": ["Commission", "Comisión"],
    "commission": ["commission", "comisión"],
    "Seuil de marge": ["Margin threshold", "Umbral de margen"],
    "Plancher": ["Floor price", "Precio mínimo"],
    "Prévenir quand le stock devient bas": ["Warn when stock runs low", "Avisar cuando el stock baje"],
    "Prévenir en dessous de": ["Warn below", "Avisar por debajo de"],
    "Prévenir en cas de baisse rapide": ["Warn on a fast drop", "Avisar si baja rápido"],
    "Ignorer les petites références": ["Ignore small references", "Ignorar referencias pequeñas"],
    "Autres champs": ["Other fields", "Otros campos"],
    "Catégorie générale": ["General category", "Categoría general"],
    "Nom de la catégorie": ["Category name", "Nombre de la categoría"],

    # ---- états et messages courts ----
    "Aucun produit ne correspond à ces filtres.":
        ["No product matches these filters.", "Ningún producto coincide con estos filtros."],
    "Déjà comptées": ["Already counted", "Ya contadas"],
    "Déjà vérifiées": ["Already checked", "Ya verificadas"],
    "Jamais vérifiées": ["Never checked", "Nunca verificadas"],
    "Reste à compter": ["Left to count", "Falta contar"],
    "À vérifier": ["To check", "Por verificar"],
    "Avec écart": ["With a difference", "Con diferencia"],
    "Comptage et écarts": ["Count and differences", "Recuento y diferencias"],
    "Valeur écart": ["Value of the difference", "Valor de la diferencia"],
    "Anomalies de prix": ["Price anomalies", "Anomalías de precio"],
    "Ce que chaque rôle peut faire": ["What each role can do", "Lo que puede hacer cada rol"],
    "Les comptes": ["The accounts", "Las cuentas"],
    "Les canaux": ["The channels", "Los canales"],
    "Tout le monde": ["Everyone", "Todos"],
    "Autre": ["Other", "Otro"],
    "— inconnu —": ["— unknown —", "— desconocido —"],
    "Boutique": ["Shop", "Tienda"],
    "Caisse Lightspeed": ["Lightspeed till", "Caja Lightspeed"],
    "Site perfumestrade.com": ["perfumestrade.com website", "Web perfumestrade.com"],
    "Catalogue Parfums": ["Perfume catalog", "Catálogo de perfumes"],
    "sans photo": ["no photo", "sin foto"],
    "Revenir au fichier d'origine": ["Back to the original file", "Volver al archivo original"],
    "stock importé": ["stock imported", "stock importado"],
    "unités": ["units", "unidades"],
    "références en stock": ["references in stock", "referencias en stock"],
    "Photos : perfumestrade.com": ["Photos: perfumestrade.com", "Fotos: perfumestrade.com"],
    "Aucune quantité en stock ne change.": ["No stock quantity changes.", "Ninguna cantidad de stock cambia."],
    "Saisie conservée sur cet ordinateur": ["Entries kept on this computer", "Datos guardados en este ordenador"],
}

LANGUE = r"""
/* ============ TROIS LANGUES ============ */
const K_LANG='langue-v1';
/* Le dictionnaire vit dans donnees/langue.js, chargé par chaque page avant son
   propre code — comme les produits. Avant, il était recopié dans chaque page :
   700 phrases en deux langues, seize fois. S'il manque, MOTS est vide et la
   page reste simplement en français. */
const MOTS=(typeof window!=='undefined'&&window.D_LANGUE)||{};
const LANGUES={fr:'Français', en:'English', es:'Español'};
const lgLit=()=>{ try{ const v=localStorage.getItem(K_LANG); return LANGUES[v]?v:'fr'; }catch(e){ return 'fr'; } };
let LANG=lgLit();

/* i = 0 pour l'anglais, 1 pour l'espagnol */
/* Les nombres varient, la phrase autour non : « 1 892 références en stock » est
   la même phrase que « 40 références en stock ». On remplace chaque nombre par
   {n}, on cherche la phrase à trous dans le dictionnaire, puis on remet les
   nombres dans l'ordre. Un « [s] » dans la traduction devient « s » si le premier
   nombre n'est pas 1 : « {n} reference[s] ». Les montants gardent leur forme
   d'origine (l'espace fine, la virgule) : ce sont des données, pas du texte. */
const LG_NUM=/\bB0[A-Z0-9]{8}\b|\d(?:[\d\s  .,:/h]*\d)?/g;   /* nombres, et codes ASIN */
function lgTrous(k,lg){
  if(!/\d|«/.test(k)) return null;
  /* les « mots entre guillemets » sont des trous eux aussi : « Facture » ou
     « Devis » se traduisent à part, et la phrase autour reste une seule entrée */
  const cit=[]; let gab=k.replace(/«\s*([^»]*?)\s*»/g,(m,q)=>{ cit.push(q); return '{q}'; });
  const nums=[]; gab=gab.replace(LG_NUM,m=>{ nums.push(m); return '{n}'; });
  const e=MOTS[gab]; if(!e) return null;
  let v=e[lg==='en'?0:1]; if(!v||v===gab) return null;
  const un=String(nums[0]||'').replace(/[\s  ]/g,'')==='1';
  v=v.replace(/\[s\]/g,un?'':'s').replace(/\[es\]/g,un?'':'es');
  let i=0; v=v.replace(/\{n\}/g,()=>nums[i++]!==undefined?nums[i-1]:'');
  let j=0; v=v.replace(/\{q\}/g,()=>{ const q=cit[j++]; if(q===undefined) return '';
    const t=lgMot(q,lg)||q; return lg==='en'?('“'+t+'”'):('«\u00a0'+t+'\u00a0»'); });
  return v;
}
/* ---- le vocabulaire de la maison, en français ----
   Sam et son équipe ne disent pas « devis » : ils disent « cote » (la quote de
   la caisse). Plutôt que de réécrire des centaines de phrases à la main — avec
   les fautes d'accord que ça sème — le mot est remplacé au moment de l'affichage,
   avec ses articles et ses participes. Le dictionnaire EN/ES, lui, part toujours
   du français d'origine : rien ne change pour les autres langues. */
const LG_VOCAB_EXACT=[
  ["Un devis ne sort rien du stock. Il pourra être transformé en facture en un clic, quand le client confirme.",
   "Une cote ne sort rien du stock. Elle pourra être transformée en facture en un clic, quand le client confirme."],
  ["Le devis est gardé et devient une facture en un clic.","La cote est gardée et devient une facture en un clic."],
  ["Un fournisseur propose un devis : vaut-il le coup ?","Un fournisseur propose une cote : vaut-elle le coup ?"],
  ["Un devis de fournisseur, ligne par ligne, comparé à","Une cote de fournisseur, ligne par ligne, comparée à"],
  ["Dépose le devis ici, ou clique pour le choisir","Dépose la cote ici, ou clique pour la choisir"],
  ["Un devis se lit s'il porte","Une cote se lit si elle porte"],
  ["Un devis, c'est une ligne","Une cote, c'est une ligne"],
  ["Devis restés sans commande","Cotes restées sans commande"],
  ["Devis proposé","Cote proposée"],
  ["Devis chargé","Cote chargée"],
  ["Étudier un autre devis","Étudier une autre cote"],
  ["Étudier un devis","Étudier une cote"],
  ["Faire un devis","Faire une cote"],
  ["Factures et devis","Factures et cotes"]];
const LG_PART='(enregistré|converti|archivé|désarchivé|gardé|chargé|supprimé|envoyé|ouvert|jeté|corrigé|refermé|émis|payé|transformé|créé|accepté|refusé|mémorisé|déposé|lu|reçu|proposé|effacé|retrouvé|rangé)';
/* \b ne connaît pas les lettres accentuées en JavaScript : on borne à la main */
const L_='(?<![A-Za-zÀ-ÿ])', _L='(?![A-Za-zÀ-ÿ])';
function lgVocab(t){
  let s=String(t); if(!/devis/i.test(s)) return s;
  LG_VOCAB_EXACT.forEach(([a,b])=>{ if(s.includes(a)) s=s.split(a).join(b); });
  /* le pluriel : « les devis », « des devis », « 3 devis », « factures et devis » */
  s=s.replace(new RegExp(L_+'(tous|certains|nouveaux|derniers|anciens|vieux)\\s+(les\\s+|des\\s+)?devis'+_L,'gi'),(m,a,b)=>{
    const A={tous:'toutes',certains:'certaines',nouveaux:'nouvelles',derniers:'dernières',anciens:'anciennes',vieux:'vieilles'};
    let r=A[a.toLowerCase()]||a; if(a[0]===a[0].toUpperCase()) r=r[0].toUpperCase()+r.slice(1); return r+' '+(b||'')+'cotes'; });
  s=s.replace(new RegExp(L_+'(les|des|ces|mes|tes|ses|nos|vos|leurs|aux|plusieurs|quelques|deux|trois|\\d+)\\s+devis'+_L,'gi'),(m,a)=>a+' cotes');
  s=s.replace(new RegExp(L_+'devis (clients|restés|gardés|convertis|archivés|créés|en attente)'+_L,'gi'),(m,a)=>'cotes '+a.replace(/és$/,'ées'));
  s=s.replace(/(Factures?|factures?) et devis/g,(m,a)=>a+' et cotes');
  /* le singulier avec son article */
  s=s.replace(new RegExp(L_+'(le|un|ce|du|au|mon|ton|son|nouveau|premier|dernier|seul|quel|tout|aucun|chaque|cet)\\s+devis'+_L,'gi'),(m,a)=>{
    const A={le:'la',un:'une',ce:'cette',cet:'cette',du:'de la',au:'à la',mon:'ma',ton:'ta',son:'sa',nouveau:'nouvelle',premier:'première',dernier:'dernière',seul:'seule',quel:'quelle',tout:'toute',aucun:'aucune',chaque:'chaque'};
    const k=a.toLowerCase(); let r=A[k]||a; if(a[0]===a[0].toUpperCase()) r=r[0].toUpperCase()+r.slice(1); return r+' cote'; });
  /* le mot seul, majuscules respectées */
  s=s.replace(new RegExp(L_+'DEVIS'+_L,'g'),'COTE').replace(new RegExp(L_+'Devis'+_L,'g'),'Cote').replace(new RegExp(L_+'devis'+_L,'g'),'cote');
  /* l'accord du participe qui suit : « cote DV-2026-0003 enregistré » → « enregistrée »,
     « la cote a été enregistré » → « enregistrée », « 1 cotes créées » → « 1 cote créée » */
  s=s.replace(new RegExp(L_+'([Cc]otes?)((?:\\s+[A-Z]{2}-[\\d-]+)?)((?:\\s+(?:a été|est|sera|ont été|sont|seront))?)\\s+'+LG_PART+'s?'+_L,'g'),(m,c,n,v,p)=>c+n+v+' '+p+(c.endsWith('s')?'es':'e'));
  s=s.replace(new RegExp(L_+'1 cotes'+_L,'g'),'1 cote').replace(new RegExp(L_+'1 cote ([a-zé]+)es'+_L,'g'),'1 cote $1e');
  return s;
}
/* pour les textes fabriqués en JavaScript (WhatsApp, courrier, fenêtres de confirmation) */
function vf(t,l){ return ((l||LANG)==='fr')?lgVocab(t):t; }
function lgMot(t,l){
  const lg=l||LANG;
  if(lg==='fr'){ const k=String(t).replace(/\s+/g,' ').trim(); const v=lgVocab(k); return v!==k?v:null; }
  const k=String(t).replace(/\s+/g,' ').trim();
  const e=MOTS[k];
  if(e){ const v=e[lg==='en'?0:1]; return (v&&v!==k)?v:null; }
  return lgTrous(k,lg);
}
/* ---- une zone peut imposer SA langue, quelle que soit celle de l'écran ----
   Une facture ne part pas chez celui qui la regarde : elle part chez le client.
   Elle porte donc data-lang="en" et reste en anglais même si Sam travaille en
   français — et le contraire est vrai aussi. C'est la seule façon d'avoir un
   outil en français et des documents dans la langue du destinataire. */
function lgLangDe(n){
  let e=(n&&n.nodeType===1)?n:(n&&n.parentNode);
  while(e&&e.nodeType===1){
    const v=e.getAttribute&&e.getAttribute('data-lang');
    if(v&&LANGUES[v]) return v;
    e=e.parentNode;
  }
  return LANG;
}
/* on garde le français d'origine pour pouvoir revenir en arrière sans recharger */
function lgTexte(n){
  /* On repart toujours du français d'origine, jamais de ce qui est affiché :
     sinon, passer de l'anglais à l'espagnol chercherait « Catalogue » dans un
     texte qui dit déjà « Catalog », et ne trouverait rien. */
  const orig=(n.__fr!==undefined)?n.__fr:n.nodeValue;
  if(!orig||!/[A-Za-zÀ-ÿ]/.test(orig)) return;
  const v=lgMot(orig,lgLangDe(n));
  if(v!==null){ if(n.__fr===undefined) n.__fr=orig; n.nodeValue=orig.replace(orig.trim(),v); }
  else if(n.__fr!==undefined && n.nodeValue!==n.__fr) n.nodeValue=n.__fr;
}
const LG_ATTR=['placeholder','title','aria-label'];
function lgAttrs(el){
  LG_ATTR.forEach(a=>{
    if(!el.hasAttribute(a)) return;
    const cle='__fr_'+a;
    const src=el[cle]!==undefined?el[cle]:el.getAttribute(a);
    const v=lgMot(src,lgLangDe(el));
    if(v!==null){ if(el[cle]===undefined) el[cle]=src; el.setAttribute(a,v); }
    else if(el[cle]!==undefined) el.setAttribute(a,el[cle]);
  });
}
/* Les zones de saisie ne sont jamais touchées : ce que l'utilisateur a tapé
   lui appartient. Les données non plus — elles ne sont pas dans le dictionnaire. */
const LG_SAUT={SCRIPT:1,STYLE:1,TEXTAREA:1,CODE:1,PRE:1,INPUT:1,OPTION:0};
/* Les noms de parfums, de marques et de clients ne se traduisent jamais.
   Le dictionnaire ne les contient pas — mais on met en plus une barrière :
   tout ce qui porte une de ces classes est laissé strictement intact. */
const LG_DATA='.lnm,.lmq,.nom,.nm,.mq,.marque,.produit,.bc,.lbc,.lid,.pd,td.ref,[data-nolang]';
function lgDonnee(n){
  let e=n.parentNode;
  while(e&&e!==document.body){
    if(e.nodeType===1&&(e.matches&&e.matches(LG_DATA))) return true;
    e=e.parentNode;
  }
  return false;
}
/* ---- les phrases coupées par un mot en gras ----
   « Compte ce qui porte <b>l'argent</b> » fait trois morceaux de texte, et
   aucun des trois n'est une phrase du dictionnaire. On regarde donc aussi
   l'élément entier : si son texte complet est au dictionnaire, on remplace son
   contenu — la traduction peut porter ses propres <b>. On ne le fait que sur des
   éléments courts qui contiennent une balise, jamais sur une zone de données. */
const LG_BLOC='p,li,span,label,small,div,td,th,h1,h2,h3,h4,button,a,em,strong,summary,legend,dt,dd';
function lgTexteFr(el){
  /* les morceaux sont joints par une espace : « Sam<br>Patron » se lit
     « Sam Patron », pas « SamPatron » — la clé du dictionnaire reste lisible */
  let s=''; const it=document.createTreeWalker(el,NodeFilter.SHOW_TEXT);
  let n; while((n=it.nextNode())) s+=' '+(n.__fr!==undefined?n.__fr:n.nodeValue);
  return s.replace(/\s+/g,' ').trim();
}
/* La traduction d'un bloc peut désigner les balises d'origine par leur rang :
   <1>texte</1> reprend la 1re balise du bloc (avec son href, sa classe, son id)
   et y met ce texte ; <3/> recopie la 3e telle quelle (un <br>, un chiffre, un
   nom). Les balises écrites en clair (<b>…</b>) passent aussi. Ainsi un lien
   traduit reste un lien, et un bouton traduit garde son identifiant. */
function lgRendBloc(el,v){
  if(!/<\d+\/?>/.test(v)){ el.innerHTML=v; return; }
  const tpl=document.createElement('template'); tpl.innerHTML=el.__frHTML;
  const kids=[...tpl.content.querySelectorAll('*')];
  let html=v.replace(/<(\d+)\/>/g,(m,i)=>{ const k=kids[+i-1]; return k?k.outerHTML:''; });
  html=html.replace(/<(\d+)>([\s\S]*?)<\/\1>/g,(m,i,txt)=>{ const k=kids[+i-1]; if(!k) return txt;
    const c=k.cloneNode(false); c.innerHTML=txt; return c.outerHTML; });
  el.innerHTML=html;
}
function lgHtmlFr(el){
  /* le HTML français d'origine, reconstruit : chaque nœud de texte garde son __fr */
  const c=el.cloneNode(true);
  const A=document.createTreeWalker(el,NodeFilter.SHOW_TEXT), B=document.createTreeWalker(c,NodeFilter.SHOW_TEXT);
  let x,y; while((x=A.nextNode())&&(y=B.nextNode())){ if(x.__fr!==undefined) y.nodeValue=x.__fr; }
  return c.innerHTML;
}
function lgBlocs(r){
  if(!r.querySelectorAll) return;
  r.querySelectorAll(LG_BLOC).forEach(el=>{
    if(LG_SAUT[el.nodeName]||el.children.length===0||el.children.length>12) return;
    if(el.querySelector('input,textarea,select,table,ul,ol,img,svg,canvas')) return;
    if(el.textContent.length>1200) return;      /* un conteneur, pas une phrase */
    if(el.matches(LG_DATA)||lgDonnee(el)) return;
    const lg=lgLangDe(el);
    /* « rendu » : le bloc est encore exactement tel que je l'ai laissé. Sinon, la
       page l'a réécrit (un compteur qui change) : on relit le français dedans. */
    const rendu = el.__lgRendu!==undefined && el.innerHTML===el.__lgRendu;
    if(rendu && lg==='fr'){ el.innerHTML=el.__frHTML; el.__lgRendu=undefined; el.__lgLang=undefined; return; }
    if(lg==='fr') return;
    const orig=rendu?el.__frTxt:lgTexteFr(el);
    if(!orig||orig.length>900||!/[A-Za-zÀ-ÿ]/.test(orig)) return;
    const v=lgMot(orig,lg); if(v===null) return;
    if(rendu && lg===el.__lgLang) return;
    if(!rendu){ el.__frHTML=lgHtmlFr(el); el.__frTxt=orig; }
    lgRendBloc(el,v); el.__lgLang=lg; el.__lgRendu=el.innerHTML;
  });
}
function lgApplique(racine){
  const r=racine||document.body; if(!r) return;
  lgBlocs(r);
  const it=document.createTreeWalker(r,NodeFilter.SHOW_TEXT,{acceptNode:n=>
    ((n.parentNode&&LG_SAUT[n.parentNode.nodeName])||lgDonnee(n))
      ?NodeFilter.FILTER_REJECT:NodeFilter.FILTER_ACCEPT});
  const L=[]; let n; while((n=it.nextNode())) L.push(n);
  L.forEach(lgTexte);
  if(r.querySelectorAll) r.querySelectorAll('[placeholder],[title],[aria-label]').forEach(lgAttrs);
  if(r.nodeType===1) lgAttrs(r);
}
function lgChange(l){
  if(!LANGUES[l]) return;
  LANG=l; try{ localStorage.setItem(K_LANG,l); }catch(e){}
  lgApplique(document.body);
  document.querySelectorAll('#lgsel button').forEach(b=>b.classList.toggle('on',b.dataset.l===l));
  document.documentElement.lang=l;
  try{ const J=lit('crm-journal-v1',[]);
    J.push({t:new Date().toISOString(),u:(typeof NOM_UTIL!=='undefined'?NOM_UTIL:''),
            act:'reglage',lib:'langue de l\'écran',ref:'langue',av:null,ap:LANGUES[l]});
    ecrit('crm-journal-v1',J); }catch(e){}
}
/* le choix, au bas de la barre de gauche */
function lgBouton(){
  const p=document.querySelector('.side .sfoot'); if(!p||document.getElementById('lgsel')) return;
  const d=document.createElement('div'); d.id='lgsel';
  d.style.cssText='display:flex;gap:4px;margin-top:8px';
  d.innerHTML=Object.keys(LANGUES).map(l=>
    `<button data-l="${l}" class="${l===LANG?'on':''}" title="${LANGUES[l]}"
      style="font-family:inherit;font-size:10.5px;font-weight:600;letter-spacing:.06em;
      padding:3px 7px;border-radius:3px;cursor:pointer;border:1px solid var(--line-2);
      background:transparent;color:var(--ink-3)">${l.toUpperCase()}</button>`).join('');
  p.appendChild(d);
  d.addEventListener('click',e=>{ const b=e.target.closest('[data-l]'); if(b) lgChange(b.dataset.l); });
  const st=document.createElement('style');
  st.textContent='#lgsel button.on{background:var(--iris);border-color:var(--iris);color:#fff}';
  document.head.appendChild(st);
}
/* En français, le vocabulaire de la maison (« cote ») demande de parcourir la page
   aussi. On s'en dispense sur les pages à milliers de lignes (catalogue, stock),
   où le mot n'apparaît pas et où le parcours coûterait cher à chaque redessin. */
const LG_FR_PARCOURS=!/catalogue|stock|inventaire/.test(location.pathname);
(function(){
  const go=()=>{
    try{ lgBouton();
      if(LANG!=='fr'){ document.documentElement.lang=LANG; lgApplique(document.body); }
      else if(LG_FR_PARCOURS) lgApplique(document.body);
      else document.querySelectorAll('[data-lang]').forEach(z=>{ try{ lgApplique(z); }catch(e){} });
    }catch(e){}
    /* le JavaScript des pages redessine des morceaux en permanence :
       on repasse dessus, mais groupé, pour ne pas ralentir l'écran */
    try{
      let t=null;
      /* En français, on ne repasse PAS sur toute la page : sur le catalogue, ce
         serait parcourir des milliers de lignes à chaque redessin. On ne visite
         alors que les zones qui imposent leur propre langue — un document. */
      new MutationObserver(()=>{ if(t) return;
        if(LANG==='fr' && !LG_FR_PARCOURS && !document.querySelector('[data-lang]')) return;
        t=setTimeout(()=>{ t=null; try{
          if(LANG==='fr' && !LG_FR_PARCOURS) document.querySelectorAll('[data-lang]').forEach(z=>lgApplique(z));
          else lgApplique(document.body);
        }catch(e){} },120); })
        .observe(document.body,{childList:true,subtree:true});
    }catch(e){}
  };
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',go);
  else setTimeout(go,0);
})();
"""

# Les paragraphes d'explication vivent à part, dans _phrases.py
try:
    from _phrases import PHRASES
    MOTS.update(PHRASES)
except Exception:
    pass

import json as _json
# Le gros du dictionnaire vit dans _langue_mots2.py (audit du 11 septembre 2026 :
# plus de 500 phrases restaient en français en anglais et en espagnol). Ici ne
# restent que les premières entrées ; les deux fichiers se fondent en un seul
# dictionnaire, les entrées de _langue_mots2 l'emportant en cas de doublon.
try:
    from _langue_mots2 import MOTS2 as _M2
    MOTS.update(_M2)
except ImportError:
    pass
import _donnees
_donnees.pose('langue', MOTS, 'D_LANGUE')
# La balise que chaque page doit poser AVANT son script : le dictionnaire commun.
BALISE = '<script src="donnees/langue.js"></script>'
