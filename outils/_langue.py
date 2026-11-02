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
    "Commerce": ["Trade", "Comercial"],
    "Paie": ["Payroll", "Nómina"],
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

VOCAB = r"""
/* ===== LE VOCABULAIRE DE LA MAISON, AVANT LA PREMIÈRE PEINTURE =====
   Ce script n'est PAS différé : il tourne pendant que la page se construit, avant
   que l'écran ne s'affiche. Sinon on voyait « Devis » une demi-seconde, puis
   « Cote » — le temps que le cockpit réponde et que le code de la page démarre.
   Igal l'a vu le 12 septembre : « code apparaît, après code disparaît ». */
(function(){
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
/* 15 oct. 2026 : une instruction « lookbehind » dans une page la fait mourir tout entière sur les Safari d'avant la 16.4
   (la page se recharge sans rien faire, sans message). On ne l'utilise que si le navigateur la connaît. */
const LG_LB=(function(){ try{ new RegExp('(?<!a)b'); return true; }catch(e){ return false; } })();
const L_=LG_LB?'(?<![A-Za-zÀ-ÿ])':'\\b', _L='(?![A-Za-zÀ-ÿ])';
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

window.__lgVocab=lgVocab;
/* le premier passage, sur ce que la page contient déjà (menu, titre, filtres) */
try{
  let l='fr'; try{ l=localStorage.getItem('langue-v1')||'fr'; }catch(e){}
  if(l!=='fr' || /catalogue|stock|inventaire/.test(location.pathname) || !document.body) return;
  const DATA='.lnm,.lmq,.nom,.nm,.mq,.marque,.produit,.bc,.lbc,.lid,.pd,td.ref,[data-nolang]';
  const saute=n=>{ let e=n.parentNode; while(e&&e.nodeType===1){ if(/^(SCRIPT|STYLE|TEXTAREA|CODE|PRE|INPUT)$/.test(e.nodeName)||(e.matches&&e.matches(DATA))) return true; e=e.parentNode; } return false; };
  const it=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT,{acceptNode:n=>saute(n)?NodeFilter.FILTER_REJECT:NodeFilter.FILTER_ACCEPT});
  const L=[]; let n; while((n=it.nextNode())) L.push(n);
  L.forEach(n=>{ const o=n.nodeValue; if(!/devis/i.test(o)) return; const v=lgVocab(o); if(v!==o){ n.__fr=o; n.nodeValue=v; } });
  document.body.querySelectorAll('[placeholder],[title],[aria-label]').forEach(el=>['placeholder','title','aria-label'].forEach(a=>{
    const s0=el.getAttribute(a); if(!s0||!/devis/i.test(s0)) return; const v=lgVocab(s0); if(v!==s0){ el['__fr_'+a]=s0; el.setAttribute(a,v); } }));
}catch(e){}
})();
"""

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
const LG_NUM=(function(){ try{ return new RegExp(String.raw`\bB0[A-Z0-9]{8}\b|(?:(?<![\w-])[-−])?\d(?:[\d\s  .,:/h]*\d)?`,'g'); }catch(e){ return /\bB0[A-Z0-9]{8}\b|\d(?:[\d\s  .,:/h]*\d)?/g; } })();   /* nombres, et codes ASIN */
const LG_NUM0=/\bB0[A-Z0-9]{8}\b|\d(?:[\d\s  .,:/h]*\d)?/g;   /* nombres, et codes ASIN */
function lgTrous(k,lg){
  if(!/\d|«/.test(k)) return null;
  /* les « mots entre guillemets » sont des trous eux aussi : « Facture » ou
     « Devis » se traduisent à part, et la phrase autour reste une seule entrée */
  const cit=[]; let gab=k.replace(/«\s*([^»]*?)\s*»/g,(m,q)=>{ cit.push(q); return '{q}'; });
  /* deux lectures : le signe moins collé au nombre (« -1 flacon »), puis sans (les
     entrées plus anciennes écrivent « −{n} $ » avec le signe en dur) */
  let nums=[], g1=gab.replace(LG_NUM,m=>{ nums.push(m); return '{n}'; });
  let e=MOTS[g1];
  if(!e){ const n2=[]; const g2=gab.replace(LG_NUM0,m=>{ n2.push(m); return '{n}'; }); if(MOTS[g2]){ e=MOTS[g2]; nums=n2; g1=g2; } }
  gab=g1; if(!e) return null;
  let v=e[lg==='en'?0:1]; if(!v||v===gab) return null;
  const un=String(nums[0]||'').replace(/[\s  ]/g,'')==='1';
  v=v.replace(/\[s\]/g,un?'':'s').replace(/\[es\]/g,un?'':'es');
  let i=0; v=v.replace(/\{n\}/g,()=>nums[i++]!==undefined?nums[i-1]:'');
  let j=0; v=v.replace(/\{q\}/g,()=>{ const q=cit[j++]; if(q===undefined) return '';
    const t=lgMot(q,lg)||q; return lg==='en'?('“'+t+'”'):('«\u00a0'+t+'\u00a0»'); });
  return v;
}
/* le vocabulaire de la maison (« cote ») vit dans VOCAB, un script non différé
   qui passe avant la première peinture ; ici on s'en sert seulement */
function lgVocab(t){ return (window.__lgVocab)?window.__lgVocab(t):String(t); }
/* pour les textes fabriqués en JavaScript (WhatsApp, courrier, fenêtres de confirmation) */
function vf(t,l){ return ((l||LANG)==='fr')?lgVocab(t):t; }
function lgMot(t,l,entier){
  const lg=l||LANG;
  if(lg==='fr'){ const k=String(t).replace(/\s+/g,' ').trim(); const v=lgVocab(k); return v!==k?v:null; }
  const k=String(t).replace(/\s+/g,' ').trim();
  const e=MOTS[k];
  if(e){ const v=e[lg==='en'?0:1]; return (v&&v!==k)?v:null; }
  const tr=lgTrous(k,lg); if(tr!==null||entier) return tr;
  return lgMorceaux(k,lg);
}
/* ---- une phrase faite de morceaux ----
   Le journal, les notes, les motifs sont écrits une fois, en français, avec des
   données au milieu : « commande 20701 expédiée le 24/09/2026 (Site perfumestrade.com)
   — facture faite, stock sorti ». La phrase entière n'est jamais au dictionnaire (les
   noms et les numéros changent), mais chacun de ses morceaux l'est. On coupe aux
   séparateurs (tiret long, point médian, virgule, deux-points, parenthèses), on
   traduit chaque morceau, et on recolle. Un morceau qui n'est qu'une donnée (un nom,
   un numéro) reste tel quel. On ne rend rien si aucun morceau n'a bougé. */
const LG_COUPE=/( — | – | · |, |; | : |: | \()/;
/* des phrases avec un NOM au milieu (un client, un fournisseur, un canal) : le nom
   n'est ni un nombre ni entre « » — on le reconnaît par la forme de la phrase */
const LG_MODELES=[
  [/^message envoyé à (.+)$/,'message sent to $1','mensaje enviado a $1'],
  [/^Fiche de (.+)$/,'Record of $1','Ficha de $1'],
  [/^Écrire à (.+)$/,'Write to $1','Escribir a $1'],
  [/^devis (.+) du (\S+)$/,'quote $1 of $2','cotización $1 del $2'],
  [/^cote (.+) du (\S+)$/,'quote $1 of $2','cotización $1 del $2'],
  [/^canal (.+)$/,(m,a)=>'channel '+(lgMot(a,'en')||a),(m,a)=>'canal '+(lgMot(a,'es')||a)],
  [/^saisi par (.+)$/,'entered by $1','registrado por $1'],
  [/^enregistrée par (.+?)\.?$/,'recorded by $1.','registrada por $1.'],
  [/^Vente (\S+) du (\S+) sur (.+)$/,'Sale $1 of $2 on $3','Venta $1 del $2 en $3'],
  [/^Vente (\S+)$/,'Sale $1','Venta $1'],
  [/^commande (\S+)$/,'order $1','pedido $1'],
  [/^Ventes importées (\S+)$/,'Imported sales $1','Ventas importadas $1'],
  [/^commande (\S+) annulée par (.+)$/,'order $1 cancelled by $2','pedido $1 anulado por $2'],
  [/^canal coupé pour ce parfum : (.+)$/,'channel turned off for this perfume: $1','canal desactivado para este perfume: $1'],
  [/^canal remis pour ce parfum : (.+)$/,'channel turned back on for this perfume: $1','canal reactivado para este perfume: $1'],
  [/^facture enregistrée n° (\S+)$/,'invoice recorded no. $1','factura registrada n.º $1'],
  [/^facture enregistrée$/,'invoice recorded','factura registrada'],
  [/^facture installée n° (\S+)$/,'invoice installed no. $1','factura instalada n.º $1'],
  [/^article créé depuis la facture (\S*)$/,'item created from invoice $1','artículo creado desde la factura $1'],
  [/^prix d'achat, facture (\S+)$/,"purchase price, invoice $1",'precio de compra, factura $1'],
  [/^prix d'achat, depuis (.+)$/,"purchase price, from $1",'precio de compra, desde $1'],
  [/^prix d'achat rétabli \(facture (\S+) annulée\)$/,'purchase price restored (invoice $1 cancelled)','precio de compra restablecido (factura $1 anulada)'],
  [/^réception — achat (.+)$/,'receipt — purchase $1','recepción — compra $1'],
  [/^ventes (.+) — export (\S+)$/,'sales $1 — export $2','ventas $1 — exportación $2'],
  [/^nom reconnu : « (.+) » = (.+)$/,'name recognized: “$1” = $2','nombre reconocido: «$1» = $2'],
  [/^le code (\S+) est ajouté à la fiche \(autres codes-barres\)$/,'code $1 is added to the record (other barcodes)','el código $1 se añade a la ficha (otros códigos de barras)'],
  [/^Retirer le canal « (.+) » \?/,'Remove the channel “$1”?','¿Quitar el canal «$1»?'],
];
LG_MODELES.push(
  [/^(.+) ↑ croissant$/,(m,a)=>(lgMot(a)||a)+' ↑ ascending',(m,a)=>(lgMot(a)||a)+' ↑ ascendente'],
  [/^(.+) ↓ décroissant$/,(m,a)=>(lgMot(a)||a)+' ↓ descending',(m,a)=>(lgMot(a)||a)+' ↓ descendente'],
  [/^Annuler la facture (\S+) \((.*)\) \?$/,'Cancel invoice $1 ($2)?','¿Anular la factura $1 ($2)?'],
  [/^Supprimer (.+) \?$/,'Delete $1?','¿Eliminar $1?'],
  [/^Marge nette : prix de vente moins le prix d'achat et la commission (.+) \((\d+) %\)$/,'Net margin: selling price minus the purchase price and the $1 fee ($2%)','Margen neto: precio de venta menos el precio de compra y la comisión de $1 ($2 %)'],
  [/^Envoyer ses accès à (.+) \?$/,'Send their access to $1?','¿Enviar sus accesos a $1?'],
  [/^Impossible : (.+) (?:a|ont) ce rôle\. Change-leur d'abord le rôle, puis supprime celui-ci\.$/,'Not possible: $1 has this role. Change their role first, then delete this one.','Imposible: $1 tiene este rol. Cámbiales primero el rol y luego elimina este.']);
function lgModele(k,lg){
  for(const [re,en,es] of LG_MODELES){ if(re.test(k)) return k.replace(re,lg==='en'?en:es); }
  return null;
}
function lgMorceaux(k,lg){
  const m0=lgModele(k,lg); if(m0!==null) return m0;
  /* un séparateur en tête (« · 1 parfum », « — reste dû ») : on le garde tel quel */
  const tete=(k.match(/^[·—–,:;]\s*/)||[''])[0]; if(tete){ const v=lgMot(k.slice(tete.length),lg); return v!==null?tete+v:null; }
  if(!LG_COUPE.test(k)||k.length>600) return null;
  /* on coupe aux séparateurs ; une parenthèse fermante coupe aussi, sauf dans « (s) » */
  const P0=k.split(LG_COUPE), P=[];
  P0.forEach((m,i)=>{ if(i%2===1){ P.push(m); return; }
    const x=m.match(/^(.*?[^(\s][^(]*?)(\)(?!\w))(.*)$/);
    if(x&&!/\((s|es|x)$/.test(x[1])&&x[1].indexOf('(')<0){ P.push(x[1]); P.push(x[2]); P.push(x[3]); } else P.push(m); });
  let chg=false;
  const R=P.map((m,i)=>{ if(i%2===1||!m.trim()) return m;
    const t=m.trim(); const e=MOTS[t]; let v=e?e[lg==='en'?0:1]:null;
    if(!v||v===t) v=lgTrous(t,lg);
    if(!v||v===t) v=lgModele(t,lg);
    if(v!==null&&v!==undefined&&v!==t){ chg=true; return m.replace(t,v); }
    return m; });
  return chg?R.join(''):null;
}
/* la langue des dates et des mois fabriqués par Intl (« déc. », « vendredi ») */
function lgLocale(l){ const lg=l||LANG; return lg==='en'?'en-US':lg==='es'?'es-ES':'fr-FR'; }
/* une phrase écrite d'un bloc dans les trois langues, quand elle porte des données
   (un nom, un canal) au milieu et ne peut donc pas passer par le dictionnaire */
function L3(fr,en,es){ return LANG==='en'?en:LANG==='es'?es:fr; }
/* les fenêtres du navigateur (alert, confirm, prompt) ne passent pas par la page : on
   traduit leur texte au vol, ligne par ligne. Igal, 26 sept. 2026 : « j'ai des gens
   qui ne comprennent pas un mot de français ». */
(function(){
  if(typeof window==='undefined') return;
  const tr=m=>{ try{ if(LANG==='fr') return m; return String(m==null?'':m).split('\n').map(l=>{ const t=l.trim(); if(!t) return l; const v=lgMot(t); return v!==null?l.replace(t,v):l; }).join('\n'); }catch(e){ return m; } };
  const a=window.alert, c=window.confirm, p=window.prompt;
  if(a&&!a.__lg){ window.alert=function(m){ return a.call(window,tr(m)); }; window.alert.__lg=1; }
  if(c&&!c.__lg){ window.confirm=function(m){ return c.call(window,tr(m)); }; window.confirm.__lg=1; }
  if(p&&!p.__lg){ window.prompt=function(m,d){ return p.call(window,tr(m),d); }; window.prompt.__lg=1; }
})();
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
  /* on n'écrit que si ça change : réécrire la même valeur relance l'observateur, sans fin */
  if(v!==null){ if(n.__fr===undefined) n.__fr=orig; const nv=orig.replace(orig.trim(),v); if(n.nodeValue!==nv) n.nodeValue=nv; }
  else if(n.__fr!==undefined && n.nodeValue!==n.__fr) n.nodeValue=n.__fr;
}
const LG_ATTR=['placeholder','title','aria-label'];
function lgAttrs(el){
  LG_ATTR.forEach(a=>{
    if(!el.hasAttribute(a)) return;
    const cle='__fr_'+a, mis='__lg_'+a, cur=el.getAttribute(a);
    /* la page a posé un NOUVEAU texte (placeholder changé par le code) : c'est le
       nouveau français d'origine. Ce que j'ai moi-même posé ne compte pas. */
    if(el[cle]!==undefined && cur!==el[mis] && cur!==el[cle]) el[cle]=cur;
    const src=el[cle]!==undefined?el[cle]:cur;
    const v=lgMot(src,lgLangDe(el));
    if(v!==null){ if(el[cle]===undefined) el[cle]=src; el[mis]=v; if(cur!==v) el.setAttribute(a,v); }
    else if(el[cle]!==undefined){ el[mis]=el[cle]; if(cur!==el[cle]) el.setAttribute(a,el[cle]); }
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
  /* le bloc ajouté lui-même compte aussi : un avertissement posé d'un coup dans la page
     (« 1 ligne pas encore reconnue… ») est l'élément ajouté, pas un de ses enfants */
  [...((r.matches&&r.matches(LG_BLOC))?[r]:[]), ...r.querySelectorAll(LG_BLOC)].forEach(el=>{
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
    const v=lgMot(orig,lg,true); if(v===null) return;   /* un bloc : phrase entière seulement, jamais recollée par morceaux (elle perdrait ses balises) */
    /* une traduction sans repères <1>…</1> remplacerait tout le HTML du bloc, boutons
       et identifiants compris (la page ne les retrouverait plus) : on la laisse aux
       mots un par un, sauf si le bloc n'a que des sauts de ligne */
    if(!/<\d+\/?>/.test(v) && [...el.children].some(c=>!/^(BR|WBR)$/.test(c.nodeName))) return;
    if(rendu && lg===el.__lgLang) return;
    if(!rendu){ el.__frHTML=lgHtmlFr(el); el.__frTxt=orig; }
    lgRendBloc(el,v); el.__lgLang=lg; el.__lgRendu=el.innerHTML;
  });
}
function lgApplique(racine,sansBlocs){
  const r=racine||document.body; if(!r) return;
  if(!sansBlocs) lgBlocs(r);
  const it=document.createTreeWalker(r,NodeFilter.SHOW_TEXT,{acceptNode:n=>
    ((n.parentNode&&LG_SAUT[n.parentNode.nodeName])||lgDonnee(n))
      ?NodeFilter.FILTER_REJECT:NodeFilter.FILTER_ACCEPT});
  const L=[]; let n; while((n=it.nextNode())) L.push(n);
  L.forEach(lgTexte);
  if(r.querySelectorAll) r.querySelectorAll('[placeholder],[title],[aria-label]').forEach(lgAttrs);
  if(r.nodeType===1) lgAttrs(r);
}
/* le français d'origine d'un élément déjà traduit à l'écran : pour le code qui relit un
   libellé dans la page (une option choisie) et le réutilise dans une autre phrase */
function lgFr(el){ if(!el) return ''; let t=''; const it=document.createTreeWalker(el,NodeFilter.SHOW_TEXT); let n; while((n=it.nextNode())) t+=(n.__fr!==undefined?n.__fr:n.nodeValue); return t; }
function lgChange(l){
  if(!LANGUES[l]) return;
  LANG=l; try{ localStorage.setItem(K_LANG,l); }catch(e){}
  lgApplique(document.body);
  document.querySelectorAll('#lgsel button').forEach(b=>b.classList.toggle('on',b.dataset.l===l));
  document.documentElement.lang=l; lgTitre();
  try{ const J=lit('crm-journal-v1',[]);
    J.push({t:new Date().toISOString(),u:(typeof NOM_UTIL!=='undefined'?NOM_UTIL:''),
            act:'reglage',lib:'langue de l\'écran',ref:'langue',av:null,ap:LANGUES[l]});
    ecrit('crm-journal-v1',J); }catch(e){}
}
/* le titre de l'onglet du navigateur (« Étude de cote — Perfumes Trade ») */
function lgTitre(){
  try{ if(document.__titreFr===undefined) document.__titreFr=document.title;
    const m=String(document.__titreFr).split(' — ');
    const v=LANG==='fr'?lgVocab(m[0]):lgMot(m[0]);
    document.title=((v&&v!==m[0])?v:m[0])+(m.length>1?' — '+m.slice(1).join(' — '):''); }catch(e){}
}
/* le choix, au bas de la barre de gauche */
function lgBouton(){
  const p=(document.getElementById('sfline')||document.querySelector('.side .sfoot')); if(!p||document.getElementById('lgsel')) return;
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
  /* Deux temps. 1) Tout de suite, avant que le code de la page ne tourne : les mots,
     un par un — pour que l'écran ne montre jamais un texte dans la mauvaise langue
     (Igal, 12 sept. 2026 : « code apparaît, après code disparaît »). 2) Au tour
     suivant, comme avant : les phrases en bloc (lgBlocs), qui réécrivent un
     paragraphe entier ; elles doivent passer APRÈS que la page a pris ses repères
     dans le HTML, sinon elle ne retrouve plus ses éléments. */
  const tot=()=>{
    try{ lgBouton(); }catch(e){}
    try{ lgTitre(); }catch(e){}
    try{
      if(LANG!=='fr'){ document.documentElement.lang=LANG; lgApplique(document.body,true); }
      else if(LG_FR_PARCOURS) lgApplique(document.body,true);
    }catch(e){}
    /* l'en-tête de la page avait caché l'écran en attendant : on le montre */
    try{ document.documentElement.style.visibility=''; }catch(e){}
  };
  const go=()=>{
    try{ lgTitre(); }catch(e){}
    try{ lgBouton();
      if(LANG!=='fr'){ document.documentElement.lang=LANG; lgApplique(document.body); }
      else if(LG_FR_PARCOURS) lgApplique(document.body);
      else document.querySelectorAll('[data-lang]').forEach(z=>{ try{ lgApplique(z); }catch(e){} });
    }catch(e){}
  };
  /* Le JavaScript des pages redessine des morceaux en permanence. On traite ce qui
     vient d'être ajouté TOUT DE SUITE : le rappel de l'observateur tourne avant que
     l'écran ne soit repeint, donc le mot n'est jamais vu dans la mauvaise langue.
     Avant, on attendait 120 ms puis on repassait sur toute la page : on voyait
     « Devis » clignoter en « Cote » à chaque redessin. En français sur le catalogue
     et le stock (des milliers de lignes), on ne visite que les zones qui imposent
     leur propre langue — un document. */
  const veille=()=>{
    try{
      /* les phrases en bloc, elles, passent un peu après (comme avant) : elles
         réécrivent le HTML du bloc, et la page doit d'abord y avoir pris ses repères */
      let t=null; const attente=new Set();
      const blocsPlusTard=()=>{ if(t) return; t=setTimeout(()=>{ t=null; const L=[...attente]; attente.clear();
        try{ L.forEach(n=>{ if(n.isConnected) lgBlocs(n); }); }catch(e){} },120); };
      new MutationObserver(recs=>{ try{
        if(LANG==='fr' && !LG_FR_PARCOURS){ if(document.querySelector('[data-lang]')) document.querySelectorAll('[data-lang]').forEach(z=>lgApplique(z)); return; }
        const vus=new Set();
        recs.forEach(r=>{
          if(r.type==='attributes'){ const el=r.target; if(el&&el.nodeType===1&&el.getAttribute(r.attributeName)!==el['__lg_'+r.attributeName]) lgAttrs(el); return; }
          if(r.type==='characterData'){ const n=r.target; if(n.nodeType===3&&!vus.has(n)&&!(n.parentNode&&LG_SAUT[n.parentNode.nodeName])&&!lgDonnee(n)){ vus.add(n); lgTexte(n); } return; }
          r.addedNodes.forEach(n=>{ if(vus.has(n)) return; vus.add(n);
            if(n.nodeType===3){ if(!(n.parentNode&&LG_SAUT[n.parentNode.nodeName])&&!lgDonnee(n)) lgTexte(n); }
            else if(n.nodeType===1&&n.isConnected){ lgApplique(n,true); if(LANG!=='fr'){ attente.add(n); blocsPlusTard(); } } }); });
      }catch(e){} })
        .observe(document.body,{childList:true,subtree:true,characterData:true,attributes:true,attributeFilter:['placeholder','title','aria-label']});
    }catch(e){}
  };
  if(document.body){ tot(); veille(); } else { try{ document.documentElement.style.visibility=''; }catch(e){} }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',go); else setTimeout(go,0);
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
try:
    from _langue_mots3 import MOTS3 as _M3
    MOTS.update(_M3)
except ImportError:
    pass
# ---- le vocabulaire de la maison, appliqué AU MONTAGE ----
# Le remplacement « devis » → « cote » se faisait à l'affichage : on voyait « Devis »
# un instant, puis « Cote » (Igal, 12 sept. 2026 : « code apparaît, après code
# disparaît »). Le texte fixe des pages (menu, titres, filtres) est donc converti
# ici, au montage, avec EXACTEMENT les mêmes règles : on fait tourner le bloc VOCAB
# dans Node plutôt que de le recopier en Python, pour que les deux ne divergent jamais.
import subprocess as _sp, re as _re, functools as _ft
_VOCAB_CACHE = {}
def vocab_fr(textes):
    """Applique lgVocab (le JS) à une liste de textes, via Node. Renvoie la liste convertie."""
    todo = [t for t in dict.fromkeys(textes) if t not in _VOCAB_CACHE and _re.search('devis', t, _re.I)]
    if todo:
        js = ("var window={};" + VOCAB + "\nconst L=JSON.parse(require('fs').readFileSync(0,'utf8'));"
              "process.stdout.write(JSON.stringify(L.map(t=>window.__lgVocab(t))));")
        r = _sp.run(['node', '-e', js], input=_json.dumps(todo), capture_output=True, text=True)
        if r.returncode != 0:
            raise SystemExit('vocab_fr : node a échoué — ' + r.stderr[:300])
        for a, b in zip(todo, _json.loads(r.stdout)): _VOCAB_CACHE[a] = b
    return [_VOCAB_CACHE.get(t, t) for t in textes]

def vocab_html(html):
    """Convertit le texte FIXE d'une page (nœuds texte, placeholder/title/aria-label, <title>),
    sans toucher aux scripts, aux styles ni aux attributs de logique (value, data-…)."""
    if not _re.search('devis', html, _re.I): return html
    morceaux = _re.split(r'(<script\b.*?</script>|<style\b.*?</style>)', html, flags=_re.S | _re.I)
    textes = []
    for i, m in enumerate(morceaux):
        if i % 2: continue
        textes += [t for t in _re.findall(r'>([^<]*)<', m) if _re.search('devis', t, _re.I)]
        textes += [t for t in _re.findall(r'\b(?:placeholder|title|aria-label)="([^"]*)"', m) if _re.search('devis', t, _re.I)]
    conv = dict(zip(textes, vocab_fr(textes)))
    out = []
    for i, m in enumerate(morceaux):
        if i % 2: out.append(m); continue
        m = _re.sub(r'>([^<]*)<', lambda x: '>' + conv.get(x.group(1), x.group(1)) + '<', m)
        m = _re.sub(r'\b(placeholder|title|aria-label)="([^"]*)"', lambda x: x.group(1) + '="' + conv.get(x.group(2), x.group(2)) + '"', m)
        out.append(m)
    return ''.join(out)

# Le dictionnaire EN/ES est écrit à partir du français d'ORIGINE (« devis »). Comme le
# texte fixe des pages porte maintenant « cote », chaque phrase du dictionnaire qui
# contient « devis » existe aussi sous sa forme « cote », avec la même traduction.
_cles = [k for k in MOTS if _re.search('devis', k, _re.I)]
for k, k2 in zip(_cles, vocab_fr(_cles)):
    if k2 != k and k2 not in MOTS: MOTS[k2] = MOTS[k]
import _donnees
_donnees.pose('langue', MOTS, 'D_LANGUE')
# La balise que chaque page doit poser AVANT son script : le dictionnaire commun.
BALISE = '<script src="donnees/langue.js"></script>'
