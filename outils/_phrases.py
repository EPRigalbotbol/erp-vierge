# -*- coding: utf-8 -*-
"""Les phrases d'explication de l'ERP, en anglais et en espagnol.

Séparé de _langue.py, qui garde les mots courts de l'interface : ici, ce sont
les paragraphes — ceux qui expliquent à quelqu'un ce que fait un écran et ce
qu'il ne fait pas. Ce sont eux dont le personnel de Miami a besoin.

Format identique : français : [anglais, espagnol].
"""

PHRASES = {

    # ---------- catalogue ----------
    "Ce que fait cette page et ce qu'elle ne fait pas.":
        ["What this page does, and what it does not.",
         "Lo que hace esta página, y lo que no hace."],
    "Chaque produit a":
        ["Each product has", "Cada producto tiene"],
    "une case de prix par canal":
        ["one price box per channel", "una casilla de precio por canal"],
    ". Elle est pré-remplie par la règle « prix retail + majoration du canal », et peut être écrasée à la main dans la fiche produit. La":
        [". It is pre-filled by the rule “retail price + channel mark-up”, and can be overwritten by hand in the product record. The",
         ". Se rellena con la regla “precio retail + recargo del canal”, y puede sobrescribirse a mano en la ficha del producto. La"],
    "sert à calculer la marge nette réellement encaissée sur ce canal, et le plancher sous lequel un prix est refusé (prix d'achat + seuil de marge, commission comprise). Exemple sur un parfum acheté 50 $, retail 89 $.":
        ["is used to compute the net margin actually collected on that channel, and the floor below which a price is refused (purchase price + margin threshold, commission included). Example on a perfume bought at $50, retail $89.",
         "sirve para calcular el margen neto realmente cobrado en ese canal, y el precio mínimo por debajo del cual se rechaza (precio de compra + umbral de margen, comisión incluida). Ejemplo con un perfume comprado a 50 $, retail 89 $."],
    "— 731 références sur 1 892 en portent au moins une, soit 434 572 $ de capital. Le menu « Prix » les isole. Bordure rouge : la référence perd de l'argent ou n'a pas de prix de vente. Bordure orange : marge douteuse, à contrôler.":
        ["— 731 references out of 1,892 carry at least one, i.e. $434,572 of capital. The “Prices” menu isolates them. Red border: the reference loses money or has no selling price. Orange border: doubtful margin, to be checked.",
         "— 731 referencias de 1.892 tienen al menos una, es decir 434.572 $ de capital. El menú “Precios” las aísla. Borde rojo: la referencia pierde dinero o no tiene precio de venta. Borde naranja: margen dudoso, a revisar."],
    "Les prix sans astérisque viennent du fichier d'inventaire. Les prix de gros ne viennent jamais du site.":
        ["Prices without an asterisk come from the inventory file. Wholesale prices never come from the website.",
         "Los precios sin asterisco vienen del archivo de inventario. Los precios mayoristas nunca vienen de la web."],
    "Prix retail repris de perfumestrade.com":
        ["Retail price taken from perfumestrade.com", "Precio retail tomado de perfumestrade.com"],
    "Prix du site inférieur ou égal au prix d'achat":
        ["Website price at or below the purchase price", "Precio web igual o inferior al precio de compra"],
    ", visible dans le filtre correspondant.":
        [", visible in the matching filter.", ", visible en el filtro correspondiente."],
    "— 27 références, dont 21 en stock, affichées en rouge. Ne pas les reprendre tels quels.":
        ["— 27 references, 21 of them in stock, shown in red. Do not take them as they are.",
         "— 27 referencias, 21 de ellas en stock, en rojo. No tomarlas tal cual."],
    ", absent du fichier d'inventaire — 936 références, dont 539 en stock. À valider avant toute utilisation commerciale.":
        [", missing from the inventory file — 936 references, 539 of them in stock. To be validated before any commercial use.",
         ", ausente del archivo de inventario — 936 referencias, 539 en stock. A validar antes de cualquier uso comercial."],
    "2 635 références illustrées sur 3 830 · photos locales normalisées en 800 × 800":
        ["2,635 references with a photo out of 3,830 · local photos normalised to 800 × 800",
         "2.635 referencias con foto de 3.830 · fotos locales normalizadas a 800 × 800"],
    "Aucun prix de gros (1 973)": ["No wholesale price (1,973)", "Sin precio mayorista (1.973)"],
    "Aucun prix retail (1 072)": ["No retail price (1,072)", "Sin precio retail (1.072)"],
    "Gros à perte (54)": ["Wholesale at a loss (54)", "Mayorista a pérdida (54)"],
    "Retail à perte (42)": ["Retail at a loss (42)", "Retail a pérdida (42)"],
    "Gros supérieur au retail (2)": ["Wholesale above retail (2)", "Mayorista superior a retail (2)"],
    "Gros = retail (26)": ["Wholesale = retail (26)", "Mayorista = retail (26)"],
    "Marge gros sous 10 % (163)": ["Wholesale margin under 10% (163)", "Margen mayorista bajo 10 % (163)"],
    "Marge gros au-dessus de 60 % (52)": ["Wholesale margin above 60% (52)", "Margen mayorista sobre 60 % (52)"],
    "Retail > 3x le prix d'achat (185)": ["Retail > 3× the purchase price (185)", "Retail > 3× el precio de compra (185)"],
    "⚠ Toute anomalie (2 285)": ["⚠ Any anomaly (2,285)", "⚠ Cualquier anomalía (2.285)"],
    "En stock (1 892)": ["In stock (1,892)", "En stock (1.892)"],
    "Historique, annoncées à zéro (1 938)": ["History, reported at zero (1,938)", "Histórico, declaradas a cero (1.938)"],
    "Tout (3 830)": ["All (3,830)", "Todo (3.830)"],
    "3 830 références": ["3,830 references", "3.830 referencias"],
    "1 892 en stock": ["1,892 in stock", "1.892 en stock"],
    "34 254 unités": ["34,254 units", "34.254 unidades"],
    "$ de marchandise": ["$ of merchandise", "$ de mercancía"],
    "Code-barres, marque ou nom du parfum": ["Barcode, brand or perfume name", "Código de barras, marca o nombre del perfume"],
    "Scanner ou taper un code-barres, ou chercher par nom…":
        ["Scan or type a barcode, or search by name…", "Escanear o teclear un código, o buscar por nombre…"],
    "Ajouter un parfum — scanne le code-barres ou tape le nom":
        ["Add a perfume — scan the barcode or type the name", "Añadir un perfume — escanea el código o teclea el nombre"],
    "Seuls": ["Only", "Solo"], "la marque": ["the brand", "la marca"], "le nom": ["the name", "el nombre"],
    "sont obligatoires. Tout le reste peut rester vide : l'article sera créé et marqué":
        ["are required. Everything else can stay empty: the item will be created and marked",
         "son obligatorios. Todo lo demás puede quedar vacío: el artículo se creará y se marcará"],
    "EDP, EDT…": ["EDP, EDT…", "EDP, EDT…"],
    "Précision (facultatif)": ["Detail (optional)", "Detalle (opcional)"],
    "RUBRIQUE CATALOGUE": ["CATALOG SECTION", "SECCIÓN CATÁLOGO"],
    "RUBRIQUE STOCK": ["INVENTORY SECTION", "SECCIÓN INVENTARIO"],

    # ---------- ajustement de stock ----------
    "Ajustements (casse, vol, testeur…)": ["Adjustments (breakage, theft, tester…)", "Ajustes (rotura, robo, tester…)"],
    "tombé au comptoir, carton non livré…": ["dropped at the counter, box never delivered…", "caído en el mostrador, caja no entregada…"],
    "flacon ouvert, client mécontent…": ["bottle opened, unhappy customer…", "frasco abierto, cliente descontento…"],
    "Combien de flacons": ["How many bottles", "Cuántos frascos"],
    "Aucune quantité en stock ne change.": ["No stock quantity changes.", "Ninguna cantidad de stock cambia."],

    # ---------- inventaire / comptage ----------
    "Ne compte pas tout. Compte ce qui porte l'argent.":
        ["Do not count everything. Count what carries the money.",
         "No cuentes todo. Cuenta lo que lleva el dinero."],
    "Compter 1 892 références prend des jours et personne ne le fera. Mais le stock est très concentré :":
        ["Counting 1,892 references takes days and nobody will do it. But the stock is very concentrated:",
         "Contar 1.892 referencias lleva días y nadie lo hará. Pero el stock está muy concentrado:"],
    "les 200 références les plus lourdes portent 54,5 % du capital":
        ["the 200 heaviest references carry 54.5% of the capital",
         "las 200 referencias más pesadas llevan el 54,5 % del capital"],
    ". En une demi-journée sur les bonnes étagères, on sait si l'inventaire dit vrai là où ça compte.":
        [". Half a day on the right shelves tells you whether the inventory is right where it matters.",
         ". Media jornada en las estanterías correctas dice si el inventario acierta donde importa."],
    "La liste ci-dessous est triée par argent en jeu, en remontant d'abord ce qui n'a jamais été vérifié. Choisis un lot :":
        ["The list below is sorted by money at stake, bringing up first what has never been checked. Pick a batch:",
         "La lista de abajo está ordenada por dinero en juego, primero lo que nunca se ha verificado. Elige un lote:"],
    "3 830 références · triées par capital en jeu, les jamais vérifiées en tête":
        ["3,830 references · sorted by capital at stake, never-checked first",
         "3.830 referencias · ordenadas por capital en juego, las nunca verificadas primero"],
    "1 931 d'entre elles n'ont jamais été vérifiées":
        ["1,931 of them have never been checked", "1.931 de ellas nunca se han verificado"],
    "capital en stock non vérifié": ["unchecked stock capital", "capital en stock no verificado"],
    "Pourquoi compter aussi les références annoncées à zéro.":
        ["Why also count the references reported at zero.", "Por qué contar también las referencias declaradas a cero."],
    "Il y en a 1 938, et": ["There are 1,938 of them, and", "Hay 1.938, y"],
    "à zéro — l'historique": ["at zero — the history", "a cero — el histórico"],
    ": « zéro » n'est pas un fait constaté, c'est une supposition héritée du fichier. Une ligne à zéro qui contient en réalité des flacons, c'est du stock invisible — donc de l'argent immédiatement vendable qu'on ignore posséder. Le comptage ne peut y apporter que de la bonne nouvelle. Choisis « Annoncées à zéro » dans le premier menu pour les passer en revue.":
        [": “zero” is not an observed fact, it is an assumption inherited from the file. A line at zero that actually holds bottles is invisible stock — money you could sell today without knowing you own it. Counting can only bring good news there. Pick “Reported at zero” in the first menu to review them.",
         ": “cero” no es un hecho comprobado, es una suposición heredada del archivo. Una línea a cero que en realidad tiene frascos es stock invisible — dinero vendible hoy mismo que no sabes que tienes. Contar solo puede traer buenas noticias. Elige “Declaradas a cero” en el primer menú para revisarlas."],
    "Quelles étiquettes on enlève": ["Which labels get removed", "Qué etiquetas se quitan"],
    "Seulement les fausses — celles qui viennent du fichier Excel (à choisir)":
        ["Only the false ones — those that come from the Excel file (recommended)",
         "Solo las falsas — las que vienen del archivo Excel (recomendado)"],
    "Toutes — y compris les comptages réellement faits dans SAM":
        ["All of them — including counts actually done in the tool",
         "Todas — incluidos los recuentos hechos realmente en la herramienta"],
    "Effacer aussi les chiffres déjà tapés dans la colonne « Compté » de cette feuille":
        ["Also clear the numbers already typed in the “Counted” column of this sheet",
         "Borrar también las cifras ya escritas en la columna “Contado” de esta hoja"],
    "portent l'étiquette « compté » alors que personne ne les a comptés.":
        ["carry the “counted” label although nobody counted them.",
         "llevan la etiqueta “contado” aunque nadie las ha contado."],
    "C'est une colonne du fichier Excel de départ qui l'affirmait, et SAM l'a reprise telle quelle. Tant que ces fausses étiquettes sont là, la feuille de comptage dit à l'équipe qu'il n'y a presque rien à faire — alors que tout est à faire. Ce bouton enlève les fausses étiquettes.":
        ["A column in the original Excel file claimed it, and the tool took it as it was. As long as those false labels are there, the count sheet tells the team there is almost nothing to do — when in fact everything is to do. This button removes the false labels.",
         "Una columna del archivo Excel original lo afirmaba, y la herramienta la copió tal cual. Mientras esas etiquetas falsas estén ahí, la hoja de recuento dice al equipo que casi no hay nada que hacer — cuando está todo por hacer. Este botón quita las etiquetas falsas."],
    "Si un parfum est à 7 flacons, il reste à 7 flacons. On ne touche qu'à l'étiquette. C'est écrit au journal, et le comptage se refait normalement ensuite, référence par référence.":
        ["If a perfume is at 7 bottles, it stays at 7 bottles. Only the label changes. It is written in the log, and counting then goes on as usual, reference by reference.",
         "Si un perfume está a 7 frascos, sigue a 7 frascos. Solo cambia la etiqueta. Queda escrito en el registro, y el recuento sigue normalmente, referencia por referencia."],
    "Chaque parfum porte une étiquette dans SAM :": ["Each perfume carries a label in the tool:", "Cada perfume lleva una etiqueta en la herramienta:"],
    "« quelqu'un a compté les flacons »": ["“somebody counted the bottles”", "“alguien contó los frascos”"],
    "« personne ne les a comptés »": ["“nobody counted them”", "“nadie los ha contado”"],
    ". C'est elle qui décide de ce qui apparaît dans la colonne « Jamais vérifiées ».":
        [". It decides what shows up in the “Never checked” column.",
         ". Es la que decide lo que aparece en la columna “Nunca verificadas”."],
    "vérifiées physiquement": ["physically checked", "verificadas físicamente"],
    "La saisie est conservée dans le navigateur de cet ordinateur uniquement — elle ne part nulle part et ne se synchronise pas avec un téléphone. Exporte le CSV dès qu'un lot est terminé, c'est lui qui fait foi. Le vrai comptage à plusieurs, depuis l'entrepôt, demandera la base partagée du CRM.":
        ["Entries are kept in this computer's browser only — nothing is sent anywhere and nothing syncs with a phone. Export the CSV as soon as a batch is done; that file is the record. Real counting by several people, from the warehouse, will require the shared database.",
         "Lo introducido se guarda solo en el navegador de este ordenador — no se envía a ningún sitio ni se sincroniza con un teléfono. Exporta el CSV en cuanto termines un lote; ese archivo es el que vale. El recuento real entre varias personas, desde el almacén, necesitará la base compartida."],
    "Seulement les lignes affichées à l'écran en ce moment":
        ["Only the lines currently shown on screen", "Solo las líneas mostradas ahora en pantalla"],
    "Export CSV pour la transmettre": ["CSV export to pass it on", "Exportar CSV para transmitirla"],

    # ---------- factures / achats ----------
    "Une facture d'achat ajoute les quantités reçues au stock, une facture de vente les retire. Le fournisseur ou le client, l'historique des prix et le journal se mettent à jour en même temps. Plus besoin d'un tableur à côté.":
        ["A purchase invoice adds the received quantities to stock, a sales invoice removes them. The supplier or customer, the price history and the log are updated at the same time. No more spreadsheet on the side.",
         "Una factura de compra suma las cantidades recibidas al stock, una factura de venta las resta. El proveedor o el cliente, el histórico de precios y el registro se actualizan a la vez. Ya no hace falta una hoja aparte."],
    "Enregistrer une facture ou une feuille de tarifs": ["Record an invoice or a price list", "Registrar una factura o una lista de precios"],
    "Coller des lignes de facture": ["Paste invoice lines", "Pegar líneas de factura"],
    "Colle ici les lignes d'une facture fournisseur, telles quelles. Je reconnais le format habituel :":
        ["Paste the lines of a supplier invoice here, as they are. The usual format is recognised:",
         "Pega aquí las líneas de una factura de proveedor, tal cual. Se reconoce el formato habitual:"],
    "quantité · désignation · marque · code-barres · stock · prix":
        ["quantity · description · brand · barcode · stock · price",
         "cantidad · descripción · marca · código de barras · stock · precio"],
    ". Les codes inconnus sont signalés à part. Un PDF ne peut pas être lu par la page : ouvre-le, sélectionne le tableau, copie, colle ici.":
        [". Unknown codes are listed separately. A PDF cannot be read by this page: open it, select the table, copy, paste here.",
         ". Los códigos desconocidos se señalan aparte. Un PDF no puede leerse aquí: ábrelo, selecciona la tabla, copia y pega aquí."],
    "Colle ici les lignes de la facture : un code-barres et un prix par ligne au minimum.":
        ["Paste the invoice lines here: at least a barcode and a price per line.",
         "Pega aquí las líneas de la factura: al menos un código de barras y un precio por línea."],
    ". Les produits déjà connus reçoivent un nouveau point dans leur historique de prix —":
        [". Products already known get a new point in their price history —",
         ". Los productos ya conocidos reciben un nuevo punto en su histórico de precios —"],
    "aucun doublon n'est créé": ["no duplicate is created", "no se crea ningún duplicado"],
    "Dépose la facture PDF ici, ou clique pour la choisir":
        ["Drop the PDF invoice here, or click to choose it", "Suelta aquí la factura PDF, o haz clic para elegirla"],
    "…ou coller le texte de la facture": ["…or paste the invoice text", "…o pegar el texto de la factura"],
    "Une facture en PDF ou en photo ne peut pas être lue par cette page.":
        ["A PDF or a photo of an invoice cannot be read by this page.",
         "Una factura en PDF o en foto no puede leerse en esta página."],
    "Envoie-la-moi dans la conversation : je la dépouille et je te rends les lignes prêtes à coller dans l'onglet précédent.":
        ["Send it to me in the conversation: I will read it and give you back the lines ready to paste in the previous tab.",
         "Envíamela en la conversación: la analizo y te devuelvo las líneas listas para pegar en la pestaña anterior."],
    "Lecture entièrement sur cet ordinateur — rien n'est envoyé nulle part. Un PDF scanné ou photographié n'a pas de texte lisible : dans ce cas, colle les lignes.":
        ["Read entirely on this computer — nothing is sent anywhere. A scanned or photographed PDF has no readable text: in that case, paste the lines.",
         "Se lee enteramente en este ordenador — no se envía nada. Un PDF escaneado o fotografiado no tiene texto legible: en ese caso, pega las líneas."],
    "Factures enregistrées": ["Recorded invoices", "Facturas registradas"],
    "Date de la facture": ["Invoice date", "Fecha de la factura"],
    "Date de l'achat": ["Purchase date", "Fecha de la compra"],
    "N° de facture (facultatif)": ["Invoice no. (optional)", "N.º de factura (opcional)"],
    "Nom du nouveau fournisseur": ["New supplier's name", "Nombre del nuevo proveedor"],
    "Nom tel qu'il apparaît sur les factures": ["Name as it appears on invoices", "Nombre tal como aparece en las facturas"],
    "Sert à lire les factures : le nom de ta société y figure toujours, il ne faut pas le prendre pour le fournisseur ou le client.":
        ["Used when reading invoices: your own company name always appears on them, and must not be mistaken for the supplier or the customer.",
         "Sirve para leer las facturas: el nombre de tu empresa siempre aparece en ellas, y no debe confundirse con el proveedor o el cliente."],
    "reconnu dans la facture": ["recognised in the invoice", "reconocido en la factura"],
    "lu dans la facture": ["read from the invoice", "leído en la factura"],
    "lue dans la facture": ["read from the invoice", "leída en la factura"],
    "Adopter ce prix comme prix d'achat": ["Adopt this price as the purchase price", "Adoptar este precio como precio de compra"],
    "Adopter ces prix comme": ["Adopt these prices as", "Adoptar estos precios como"],
    "Adopter ces prix comme nouveau prix d'achat": ["Adopt these prices as the new purchase price", "Adoptar estos precios como nuevo precio de compra"],
    "nouveau prix d'achat courant": ["new current purchase price", "nuevo precio de compra actual"],
    "Aujourd'hui ce prix": ["Today this price", "Hoy este precio"],
    "remplace": ["replaces", "sustituye"],
    "l'ancien. Faut-il plutôt faire la moyenne de ce qu'il a réellement payé ? C'est la question 32, à trancher avec lui.":
        ["the old one. Should it instead be the average of what was actually paid? That is question 32, to settle with him.",
         "el anterior. ¿Habría que hacer la media de lo realmente pagado? Es la pregunta 32, a decidir con él."],
    "du produit — c'est ce qu'on attend d'un achat récent. Décoche si tu saisis un vieil achat.":
        ["of the product — that is what a recent purchase is expected to do. Uncheck if you are entering an old purchase.",
         "del producto — es lo que se espera de una compra reciente. Desmarca si estás introduciendo una compra antigua."],
    "— c'est ce qu'on attend d'une facture récente.": ["— that is what a recent invoice is expected to do.", "— es lo que se espera de una factura reciente."],
    "— c'est ce qu'on veut d'une feuille de tarifs, pas d'une vieille facture.":
        ["— that is what a price list is for, not an old invoice.", "— es lo que se quiere de una lista de precios, no de una factura antigua."],
    "Ajouter la quantité au stock": ["Add the quantity to stock", "Añadir la cantidad al stock"],
    "ajouter les quantités reçues": ["add the received quantities", "añadir las cantidades recibidas"],
    "— coche si cette marchandise n'est pas encore comptée dans le stock affiché.":
        ["— tick if this merchandise is not yet counted in the stock shown.",
         "— marca si esta mercancía todavía no está contada en el stock mostrado."],
    ". Décoche si cette marchandise est déjà comptée dans le stock actuel.":
        [". Uncheck if this merchandise is already counted in the current stock.",
         ". Desmarca si esta mercancía ya está contada en el stock actual."],
    "Prix d'achat unitaire ($)": ["Unit purchase price ($)", "Precio de compra unitario ($)"],
    "ex : 74.50": ["e.g. 74.50", "ej.: 74.50"],
    "ex : 12": ["e.g. 12", "ej.: 12"],

    # ---------- ventes ----------
    "Chaque produit vendu, avec le canal sur lequel la vente a été faite : boutique, gros, site, Shopify, Amazon, Perfume City, caisse. Chiffre d'affaires et marge par canal, et la saisie d'une vente à la main.":
        ["Every product sold, with the channel the sale was made on: shop, wholesale, website, Shopify, Amazon, Perfume City, till. Revenue and margin per channel, and manual entry of a sale.",
         "Cada producto vendido, con el canal en el que se hizo la venta: tienda, mayorista, web, Shopify, Amazon, Perfume City, caja. Facturación y margen por canal, y la entrada manual de una venta."],
    "Trois façons : le bouton": ["Three ways: the button", "Tres formas: el botón"],
    "ci-dessous (on scanne ou on tape les parfums, on choisit le canal, le stock se met à jour) ; une":
        ["below (scan or type the perfumes, pick the channel, the stock updates); an",
         "de abajo (se escanean o teclean los perfumes, se elige el canal, el stock se actualiza); una"],
    "enregistrée dans la rubrique Factures ; un": ["recorded in the Invoices section; a", "registrada en la sección Facturas; una"],
    "d'un canal (Shopify, Amazon, WooCommerce, caisse) déposé dans cette même rubrique. Une vente qui ne passe par aucune des trois n'existe pas pour l'outil.":
        ["from a channel (Shopify, Amazon, WooCommerce, till) dropped in that same section. A sale that goes through none of the three does not exist for the tool.",
         "de un canal (Shopify, Amazon, WooCommerce, caja) subida en esa misma sección. Una venta que no pasa por ninguna de las tres no existe para la herramienta."],
    "Sur quel canal cette vente a-t-elle été faite ? Le": ["Which channel was this sale made on? The", "¿En qué canal se hizo esta venta? El"],
    "classe chaque vente par canal.": ["sorts every sale by channel.", "clasifica cada venta por canal."],
    "journal des ventes": ["sales log", "registro de ventas"],
    "facture de vente": ["sales invoice", "factura de venta"],

    # ---- le document envoyé au client : facture et devis ----
    # Ce papier sort de l'entreprise. Chaque étiquette y est isolée de sa donnée
    # (voir _facture.py) pour que la traduction porte, sans jamais toucher au nom
    # de la société, à celui du client ni au texte des conditions.
    "Facture": ["Invoice", "Factura"],
    "Devis": ["Quotation", "Presupuesto"],
    "Client": ["Customer", "Cliente"],
    "merci !": ["thank you!", "¡gracias!"],
    "Facturé à": ["Billed to", "Facturado a"],
    "Adressé à": ["Prepared for", "Dirigido a"],
    "Conditions": ["Terms", "Condiciones"],
    "Paiement": ["Payment", "Pago"],
    "Article": ["Item", "Artículo"],
    "Qté": ["Qty", "Cant."],
    "Prix unit.": ["Unit price", "Precio unit."],
    "Montant": ["Amount", "Importe"],
    "Sous-total": ["Subtotal", "Subtotal"],
    "Remise": ["Discount", "Descuento"],
    "Frais carte": ["Card fee", "Recargo tarjeta"],
    "Sales tax": ["Sales tax", "Sales tax"],
    "Sales tax n°": ["Sales tax no.", "Sales tax n.º"],
    "Sales tax — exonéré": ["Sales tax — exempt", "Sales tax — exento"],
    "Total": ["Total", "Total"],
    "Reçu": ["Received", "Recibido"],
    "Reste dû": ["Balance due", "Saldo pendiente"],
    "Pour régler": ["How to pay", "Para pagar"],
    "Payée": ["Paid", "Pagada"],
    "Valable 15 jours": ["Valid for 15 days", "Válido 15 días"],
    "Devis — sans engagement de stock": ["Quotation — stock not reserved",
                                          "Presupuesto — sin reserva de stock"],
    "Transformé en facture": ["Converted to invoice", "Convertido en factura"],
    "émise par": ["issued by", "emitida por"],
    "émis par": ["issued by", "emitido por"],
    # la barre au-dessus du document
    "Imprimer / enregistrer en PDF": ["Print / save as PDF", "Imprimir / guardar en PDF"],
    "Copier le texte": ["Copy as text", "Copiar el texto"],
    "Encaisser": ["Record a payment", "Registrar un pago"],
    "Encaisser le reste": ["Record the balance", "Registrar el saldo"],
    "Voir les paiements": ["See payments", "Ver los pagos"],
    "Transformer en facture": ["Turn into an invoice", "Convertir en factura"],
    "fichier de ventes importé": ["imported sales file", "archivo de ventas importado"],
    "Importer des ventes": ["Import sales", "Importar ventas"],
    "fichier exporté depuis Shopify, Amazon, Perfume City, WooCommerce, la caisse · le stock baisse":
        ["file exported from Shopify, Amazon, Perfume City, WooCommerce, the till · stock goes down",
         "archivo exportado desde Shopify, Amazon, Perfume City, WooCommerce, la caja · el stock baja"],
    "Dépose ici le fichier CSV des commandes, exporté depuis ce canal. Les colonnes sont reconnues par leur nom ; une commande déjà importée n'est jamais comptée deux fois, même si deux fichiers se chevauchent.":
        ["Drop the CSV file of orders here, exported from that channel. Columns are recognised by their name; an order already imported is never counted twice, even if two files overlap.",
         "Suelta aquí el archivo CSV de pedidos, exportado desde ese canal. Las columnas se reconocen por su nombre; un pedido ya importado nunca se cuenta dos veces, aunque dos archivos se solapen."],
    "Remettre ces flacons en stock (à décocher si la marchandise est perdue, cassée ou reste chez le client).":
        ["Put these bottles back in stock (untick if the goods are lost, broken, or stay with the customer).",
         "Devolver estos frascos al stock (desmarca si la mercancía está perdida, rota o se queda con el cliente)."],
    "Sortir ces flacons du stock (à décocher si le stock a déjà été mis à jour ailleurs).":
        ["Take these bottles out of stock (untick if the stock was already updated elsewhere).",
         "Sacar estos frascos del stock (desmarca si el stock ya se actualizó en otro sitio)."],
    "Ce qui a été rendu au client, ou « avoir » s'il garde un crédit chez toi.":
        ["What was given back to the customer, or “credit note” if they keep a credit with you.",
         "Lo devuelto al cliente, o “nota de crédito” si conserva un crédito contigo."],
    "N° de vente": ["Sale no.", "N.º de venta"],
    "facture émise · le stock baisse": ["invoice issued · stock goes down", "factura emitida · el stock baja"],
    "réception de marchandise · le stock augmente": ["goods received · stock goes up", "recepción de mercancía · el stock sube"],
    "Shopify, Amazon, Perfume City, WooCommerce, caisse · le stock baisse":
        ["Shopify, Amazon, Perfume City, WooCommerce, till · stock goes down",
         "Shopify, Amazon, Perfume City, WooCommerce, caja · el stock baja"],
    "Par canal": ["By channel", "Por canal"],

    # ---------- clients ----------
    "Les clients à qui il vend en gros. Pour chacun : ce qu'il lui a vendu, combien de commandes, quand, quels parfums — et ce qui reste à payer. Lu depuis l'onglet « carmen » du tableur.":
        ["The customers he sells wholesale to. For each: what he sold them, how many orders, when, which perfumes — and what is still unpaid. Read from the “carmen” tab of the spreadsheet.",
         "Los clientes a los que vende al por mayor. Para cada uno: lo vendido, cuántos pedidos, cuándo, qué perfumes — y lo que queda por pagar. Leído de la pestaña “carmen” de la hoja."],
    "Le texte est modifiable. L'adresse ci-dessus est celle de la fiche client ; si tu la corriges ici, elle est enregistrée dans la fiche. « Ouvrir dans Mail » prépare l'e-mail dans ton logiciel de messagerie ; WhatsApp utilise le téléphone de la fiche. SAM n'envoie rien tout seul (il faudra le serveur pour ça) : c'est toi qui appuies sur Envoyer.":
        ["The text can be edited. The address above comes from the customer record; if you correct it here, it is saved back to the record. “Open in Mail” prepares the e-mail in your mail program; WhatsApp uses the phone number from the record. The tool never sends anything by itself (that will need the server): you press Send.",
         "El texto es editable. La dirección de arriba viene de la ficha del cliente; si la corriges aquí, se guarda en la ficha. “Abrir en Mail” prepara el correo en tu programa de correo; WhatsApp usa el teléfono de la ficha. La herramienta no envía nada sola (hará falta el servidor): tú pulsas Enviar."],
    "Relance de paiement —": ["Payment reminder —", "Recordatorio de pago —"],
    "Les parfums qu'il lui prend": ["The perfumes they buy", "Los perfumes que le compra"],
    "Trier par montant acheté": ["Sort by amount purchased", "Ordenar por importe comprado"],
    "Achetés le mois dernier": ["Bought last month", "Comprados el mes pasado"],
    "Chercher un client…": ["Search a customer…", "Buscar un cliente…"],
    "adresse@exemple.com": ["address@example.com", "direccion@ejemplo.com"],
    "contact@…": ["contact@…", "contacto@…"],

    # ---------- fournisseurs ----------
    "Chaque fournisseur est construit à partir des factures enregistrées : ce qu'il vend, à quel prix, comment ses prix bougent, et sur quelles références il est battu par un autre.":
        ["Each supplier is built from the recorded invoices: what they sell, at what price, how their prices move, and on which references they are beaten by another.",
         "Cada proveedor se construye a partir de las facturas registradas: lo que vende, a qué precio, cómo se mueven sus precios, y en qué referencias otro le gana."],
    "Par date de dernière facture": ["By date of last invoice", "Por fecha de última factura"],
    "Par nombre de références": ["By number of references", "Por número de referencias"],
    "Prix le moins cher ($)": ["Cheapest price ($)", "Precio más bajo ($)"],
    "Prix obtenu": ["Price obtained", "Precio obtenido"],

    # ---------- journal ----------
    "Tout changement de prix, de quantité ou de statut de comptage est écrit ici, avec la personne, la date et l'heure. Rien ne s'efface.":
        ["Every change of price, quantity or count status is written here, with the person, the date and the time. Nothing is erased.",
         "Todo cambio de precio, cantidad o estado de recuento se escribe aquí, con la persona, la fecha y la hora. Nada se borra."],
    "Ce journal enregistre un nom déclaré, pas un nom prouvé.":
        ["This log records a declared name, not a proven one.", "Este registro guarda un nombre declarado, no un nombre probado."],
    "Un fichier ouvert sur un ordinateur n'a pas de serveur pour authentifier qui que ce soit : chacun indique son nom une fois, et il est attaché à ses actions. Pour une équipe de deux ou trois, ça répond à « qui a changé ce prix, et quand ». Ça ne vaut pas preuve devant un tiers.":
        ["A file opened on a computer has no server to authenticate anyone: each person gives their name once, and it is attached to their actions. For a team of two or three, that answers “who changed this price, and when”. It is not proof to a third party.",
         "Un archivo abierto en un ordenador no tiene servidor para autenticar a nadie: cada persona indica su nombre una vez, y queda unido a sus acciones. Para un equipo de dos o tres, responde a “quién cambió este precio, y cuándo”. No sirve como prueba ante un tercero."],
    "Toutes les actions": ["All actions", "Todas las acciones"],
    "Tout le monde": ["Everyone", "Todos"],

    # ---------- tableau de bord ----------
    "Ce qui demande une décision aujourd'hui : les références qui s'épuisent, celles qui baissent vite, et les prix qui font perdre de l'argent. Les seuils viennent des réglages.":
        ["What needs a decision today: the references running out, those dropping fast, and the prices that lose money. The thresholds come from the settings.",
         "Lo que exige una decisión hoy: las referencias que se agotan, las que bajan rápido, y los precios que hacen perder dinero. Los umbrales vienen de los ajustes."],
    "D'où viennent ces chiffres, et ce qui est approximatif":
        ["Where these figures come from, and what is approximate", "De dónde vienen estas cifras, y qué es aproximado"],
    "D'où viennent ces lignes.": ["Where these lines come from.", "De dónde vienen estas líneas."],
    "Voir le tableau de bord": ["See the dashboard", "Ver el panel"],

    # ---------- réglages ----------
    "Réglages (commissions, seuils)": ["Settings (commissions, thresholds)", "Ajustes (comisiones, umbrales)"],
    "Boutique, site, Shopify, Amazon, Perfume City, caisse… ce que tu vends réellement. La commission, c’est ce que la plateforme garde sur chaque vente.":
        ["Shop, website, Shopify, Amazon, Perfume City, till… what you actually sell on. The commission is what the platform keeps on each sale.",
         "Tienda, web, Shopify, Amazon, Perfume City, caja… donde vendes realmente. La comisión es lo que la plataforma se queda en cada venta."],
    "À partir de quand veux-tu être prévenu. Chaque réglage affiche en direct le nombre de références qu'il déclenche : tu vois tout de suite si tu crées une alerte utile ou du bruit.":
        ["From what point do you want to be warned. Each setting shows live how many references it triggers: you see straight away whether you are creating a useful alert or noise.",
         "A partir de cuándo quieres que te avisen. Cada ajuste muestra en vivo cuántas referencias activa: ves enseguida si creas una alerta útil o ruido."],
    "Une référence passe en alerte quand il en reste moins que ce nombre. Elle apparaît alors en orange dans le catalogue et remonte dans le tableau de bord.":
        ["A reference goes on alert when fewer than this number are left. It then shows in orange in the catalog and rises in the dashboard.",
         "Una referencia pasa a alerta cuando quedan menos de este número. Aparece entonces en naranja en el catálogo y sube en el panel."],
    "Indépendamment du niveau restant : si une référence a perdu une bonne partie de son stock en peu de temps, elle mérite un coup d'œil même s'il en reste encore. La baisse est mesurée sur les mouvements enregistrés dans le journal.":
        ["Regardless of what is left: if a reference has lost a good part of its stock in a short time, it deserves a look even if some remains. The drop is measured on the movements recorded in the log.",
         "Independientemente de lo que quede: si una referencia ha perdido buena parte de su stock en poco tiempo, merece una mirada aunque queden unidades. La bajada se mide sobre los movimientos registrados."],
    "Sans ce filtre, une alerte se déclenche aussi bien sur un flacon à 11 $ que sur un Creed à 225 $. En ne gardant que les références qui immobilisent au moins un certain montant, la liste d'alerte reste courte et ne contient que ce qui coûte de l'argent. Mettre 0 désactive le filtre.":
        ["Without this filter, an alert fires just as much on an $11 bottle as on a $225 Creed. By keeping only the references tying up at least a given amount, the alert list stays short and holds only what costs money. Setting 0 disables the filter.",
         "Sin este filtro, salta una alerta tanto por un frasco de 11 $ como por un Creed de 225 $. Conservando solo las referencias que inmovilizan al menos cierto importe, la lista de alertas queda corta y solo contiene lo que cuesta dinero. Poner 0 desactiva el filtro."],
    "En dessous de cette marge sur le prix de gros, la référence est signalée comme mal placée dans le catalogue et dans le tableau de bord.":
        ["Below this margin on the wholesale price, the reference is flagged as badly priced in the catalog and in the dashboard.",
         "Por debajo de este margen sobre el precio mayorista, la referencia se señala como mal fijada en el catálogo y en el panel."],
    "Prévenir en cas de baisse rapide": ["Warn on a fast drop", "Avisar si baja rápido"],
    "Prévenir si le stock a baissé de plus de": ["Warn if stock has dropped by more than", "Avisar si el stock ha bajado más de"],
    "Ne prévenir que si la référence représente au moins": ["Only warn if the reference is worth at least", "Avisar solo si la referencia representa al menos"],
    "Signaler une marge de gros inférieure à": ["Flag a wholesale margin below", "Señalar un margen mayorista inferior a"],
    "En dessous de ce nombre de flacons, la quantité s'affiche en orange":
        ["Below this number of bottles, the quantity shows in orange", "Por debajo de este número de frascos, la cantidad se muestra en naranja"],
    "Catégorie générale": ["General category", "Categoría general"],
    "Nom de la catégorie": ["Category name", "Nombre de la categoría"],
    "Beauty & Personal Care": ["Beauty & Personal Care", "Beauty & Personal Care"],
    "Men's Eau de Toilette": ["Men's Eau de Toilette", "Men's Eau de Toilette"],
    "Revenir aux valeurs de départ": ["Back to the starting values", "Volver a los valores iniciales"],

    # ---------- import du tableur ----------
    "Ouvre ton Google Sheet, sélectionne tout (": ["Open your Google Sheet, select everything (", "Abre tu Google Sheet, selecciona todo ("],
    ") puis copie (": [") then copy (", ") y copia ("],
    "), et colle ici. Un fichier CSV exporté depuis le Sheet marche aussi. Rien ne part sur Internet : tout est lu dans ce navigateur.":
        ["), and paste here. A CSV file exported from the Sheet also works. Nothing goes out to the internet: everything is read in this browser.",
         "), y pega aquí. Un archivo CSV exportado de la hoja también funciona. Nada sale a internet: todo se lee en este navegador."],
    "Colle ici les lignes du Google Sheet...": ["Paste the Google Sheet lines here...", "Pega aquí las líneas del Google Sheet..."],
    "Colle les lignes. Chaque ligne doit contenir un": ["Paste the lines. Each line must contain a", "Pega las líneas. Cada línea debe contener un"],
    ", séparé par des tabulations ou des points-virgules. La contenance, le type et le genre sont déduits de la désignation quand ils y figurent.":
        [", separated by tabs or semicolons. Size, type and gender are deduced from the description when they appear in it.",
         ", separado por tabuladores o puntos y coma. El contenido, el tipo y el género se deducen de la descripción cuando aparecen."],
    "exporté depuis Excel ou depuis le site. La première ligne doit contenir les intitulés de colonnes — je reconnais":
        ["exported from Excel or from the website. The first line must contain the column headings — recognised are",
         "exportado desde Excel o desde la web. La primera línea debe contener los títulos de columna — se reconocen"],
    ", quelle que soit leur casse ou leur ordre.": [", whatever their case or order.", ", sea cual sea su mayúscula u orden."],
    "Un fichier CSV, ou les lignes collées depuis le Google Sheet":
        ["A CSV file, or the lines pasted from the Google Sheet", "Un archivo CSV, o las líneas pegadas del Google Sheet"],
    "Choisis un fichier": ["Choose a file", "Elige un archivo"],

    # ---------- sauvegarde ----------
    "Tout ce que tu saisis vit dans": ["Everything you enter lives in", "Todo lo que introduces vive en"],
    "ce navigateur, sur cet ordinateur": ["this browser, on this computer", "este navegador, en este ordenador"],
    ". Un nettoyage de l'historique, un autre navigateur, un déplacement du dossier, et c'est perdu. Une sauvegarde est un fichier que tu gardes — c'est la seule copie qui ne dépend de rien.":
        [". Clearing the history, another browser, moving the folder, and it is gone. A backup is a file you keep — the only copy that depends on nothing.",
         ". Borrar el historial, otro navegador, mover la carpeta, y se pierde. Una copia de seguridad es un archivo que guardas — la única copia que no depende de nada."],
    "Cette sauvegarde est un fichier qui se": ["This backup is a file that", "Esta copia es un archivo que se"],
    "recharge dans l'outil": ["loads back into the tool", "recarga en la herramienta"],
    "— c'est ton filet de sécurité. L'export, lui, est un tableau lisible dans Excel, pour reporter les changements dans le fichier maître ou les transmettre à quelqu'un.":
        ["— that is your safety net. The export, on the other hand, is a table readable in Excel, to carry the changes into the master file or pass them to someone.",
         "— es tu red de seguridad. La exportación, en cambio, es una tabla legible en Excel, para llevar los cambios al archivo maestro o pasárselos a alguien."],
    "À ne pas confondre avec « Exporter mes corrections ».":
        ["Not to be confused with “Export my corrections”.", "No confundir con “Exportar mis correcciones”."],
    "Saisie conservée sur cet ordinateur": ["Entries kept on this computer", "Datos guardados en este ordenador"],

    # ---------- connecteurs ----------
    "Brancher les canaux de vente sur SAM : la marche à suivre pour créer chaque accès, l'avancement, et le contrôle des SKU. Rien ne se connecte tant qu'il n'y a pas de serveur.":
        ["Connecting the sales channels to the tool: the steps to create each access, the progress, and the SKU check. Nothing connects as long as there is no server.",
         "Conectar los canales de venta a la herramienta: los pasos para crear cada acceso, el avance, y el control de SKU. Nada se conecta mientras no haya servidor."],
    "Dans quel ordre s'y prendre": ["In what order to go about it", "En qué orden hacerlo"],
    "Le site et Shopify d'abord.": ["The website and Shopify first.", "La web y Shopify primero."],
    "Ce sont les plus simples : la boutique prévient l'outil en quelques secondes dès qu'une commande tombe, et les clés se créent en dix minutes sans validation.":
        ["They are the simplest: the shop notifies the tool within seconds of an order coming in, and the keys are created in ten minutes with no approval.",
         "Son los más sencillos: la tienda avisa a la herramienta en segundos en cuanto entra un pedido, y las claves se crean en diez minutos sin validación."],
    "Amazon ensuite.": ["Amazon next.", "Amazon después."],
    "L'inscription développeur demande une validation par Amazon : à lancer tôt, parce que ça peut prendre des jours, et le dossier se ferme sans réponse sous 5 jours.":
        ["The developer registration needs approval from Amazon: start it early, because it can take days, and the request closes without an answer after 5 days.",
         "El registro de desarrollador requiere validación de Amazon: empiézalo pronto, porque puede tardar días, y la solicitud se cierra sin respuesta a los 5 días."],
    "La caisse en dernier.": ["The till last.", "La caja al final."],
    "Il faut d'abord savoir laquelle : Lightspeed série X (jeton, ou application privée sur les comptes récents) ou série R (demande d'accès à faire auprès de Lightspeed). Sans la caisse, les ventes en boutique restent saisies à la main.":
        ["You first need to know which one: Lightspeed series X (token, or private app on recent accounts) or series R (access request to be made with Lightspeed). Without the till, in-shop sales stay entered by hand.",
         "Primero hay que saber cuál: Lightspeed serie X (token, o aplicación privada en cuentas recientes) o serie R (solicitud de acceso ante Lightspeed). Sin la caja, las ventas en tienda se siguen introduciendo a mano."],
    "Le gros ne se connecte pas.": ["Wholesale does not connect.", "El mayorista no se conecta."],
    "Une commande de Javier ou de Carmen se saisit dans SAM (Ventes → + Enregistrer une vente) : il n'y a aucune plateforme derrière.":
        ["An order from Javier or Carmen is entered in the tool (Sales → + Record a sale): there is no platform behind it.",
         "Un pedido de Javier o de Carmen se introduce en la herramienta (Ventas → + Registrar una venta): no hay ninguna plataforma detrás."],
    "clique sur un canal pour dérouler sa procédure": ["click a channel to unfold its procedure", "haz clic en un canal para desplegar su procedimiento"],
    "Le problème :": ["The problem:", "El problema:"],

    # ---------- relevé Amazon ----------
    "Relevé Amazon": ["Amazon reading", "Registro de Amazon"],
    "Ouvre la fiche Amazon du parfum, sélectionne le prix, le bloc « Best Sellers Rank », les avis, l'adresse de la page — et colle tout ici. L'outil en tire les chiffres tout seul.":
        ["Open the perfume's Amazon page, select the price, the “Best Sellers Rank” block, the reviews, the page address — and paste it all here. The tool pulls the figures out by itself.",
         "Abre la ficha de Amazon del perfume, selecciona el precio, el bloque “Best Sellers Rank”, las reseñas, la dirección de la página — y pega todo aquí. La herramienta extrae las cifras sola."],
    "Colle ici ce que tu vois sur la fiche Amazon": ["Paste here what you see on the Amazon page", "Pega aquí lo que ves en la ficha de Amazon"],
    "Lien de la fiche Amazon": ["Amazon page link", "Enlace de la ficha de Amazon"],
    "Rang général": ["Overall rank", "Rango general"],
    "Rang dans sa catégorie": ["Rank in its category", "Rango en su categoría"],
    "Nombre d'avis": ["Number of reviews", "Número de reseñas"],
    "Note (sur 5)": ["Rating (out of 5)", "Valoración (sobre 5)"],
    "Nombre de vendeurs": ["Number of sellers", "Número de vendedores"],
    "Vendu par": ["Sold by", "Vendido por"],
    "vide si indisponible": ["empty if unavailable", "vacío si no está disponible"],
    "indisponible, édition limitée, plus que 3 en stock…": ["unavailable, limited edition, only 3 left…", "no disponible, edición limitada, quedan 3…"],
    "à confirmer aussi": ["to confirm as well", "a confirmar también"],

    # ---------- accès ----------
    "Qui entre dans SAM, et ce que chacun voit": ["Who gets into the tool, and what each person sees", "Quién entra en la herramienta, y qué ve cada uno"],
    "Six caractères minimum. Note-le et donne-le à la personne : personne ne pourra le relire ensuite, pas même toi — SAM n'en garde qu'une empreinte.":
        ["Six characters minimum. Write it down and give it to the person: nobody will be able to read it again afterwards, not even you — the tool only keeps a fingerprint of it.",
         "Seis caracteres como mínimo. Anótala y dásela a la persona: nadie podrá volver a leerla, ni siquiera tú — la herramienta solo guarda una huella."],
    "Ce que chaque rôle peut faire": ["What each role can do", "Lo que puede hacer cada rol"],
    "Les comptes": ["The accounts", "Las cuentas"],
    "Les canaux": ["The channels", "Los canales"],

    # ---------- derniers morceaux de phrases ----------
    "Seulement les fausses — celles qui viennent du fichier Excel\u00a0(à choisir)":
        ["Only the false ones — those that come from the Excel file\u00a0(recommended)",
         "Solo las falsas — las que vienen del archivo Excel\u00a0(recomendado)"],
    "et": ["and", "y"],
    "ou": ["or", "o"],
    "en": ["in", "en"],
    "et un": ["and a", "y una"],
    "N°": ["No.", "N.º"],
    "Ctrl/Cmd + A": ["Ctrl/Cmd + A", "Ctrl/Cmd + A"],
    "Ctrl/Cmd + C": ["Ctrl/Cmd + C", "Ctrl/Cmd + C"],

    # ---------- Retail et « Écrire à quelqu'un » ----------
    "Retail": ["Retail", "Minorista"],
    "Les clients du site et de la boutique — et comment leur écrire":
        ["Website and shop customers — and how to write to them",
         "Clientes de la web y de la tienda — y cómo escribirles"],
    "Les clients au détail.": ["Retail customers.", "Clientes minoristas."],
    "Chercher un nom, un email, une ville…":
        ["Search a name, an email, a city…", "Buscar un nombre, un email, una ciudad…"],
    "Dernier achat": ["Last purchase", "Última compra"],
    "Total dépensé": ["Total spent", "Total gastado"],
    "Nombre de commandes": ["Number of orders", "Número de pedidos"],
    "Liste": ["List", "Lista"],
    "Vignettes": ["Tiles", "Fichas"],
    "Importer un fichier": ["Import a file", "Importar un archivo"],
    "Importer les clients du site": ["Import the website customers", "Importar los clientes de la web"],
    "Mettre les clients à jour": ["Update the customers", "Actualizar los clientes"],
    "Remplacer la liste entière par ce fichier":
        ["Replace the whole list with this file", "Reemplazar toda la lista con este archivo"],
    "Aucun client au détail pour l'instant":
        ["No retail customers yet", "Todavía no hay clientes minoristas"],
    "Personne ne correspond": ["Nobody matches", "Nadie coincide"],
    "clients au détail": ["retail customers", "clientes minoristas"],
    "acheté au total": ["bought in total", "comprado en total"],
    "commandes": ["orders", "pedidos"],
    "par client en moyenne": ["per customer on average", "por cliente de media"],
    "sans email — impossible à relancer":
        ["without an email — cannot be contacted", "sin email — imposible contactar"],
    "Client": ["Customer", "Cliente"],
    "Coordonnées": ["Contact details", "Datos de contacto"],
    "Commandes": ["Orders", "Pedidos"],
    "Écrire": ["Write", "Escribir"],
    "Envoyer une promo": ["Send an offer", "Enviar una oferta"],
    "pas d\'email": ["no email", "sin email"],
    "pas de téléphone": ["no phone", "sin teléfono"],
    "Téléphone / WhatsApp": ["Phone / WhatsApp", "Teléfono / WhatsApp"],
    "Objet (pour l\'email)": ["Subject (for the email)", "Subject (for the email)"],
    "Message": ["Message", "Mensaje"],
    "Promotion": ["Offer", "Oferta"],
    "Relance de facture": ["Invoice reminder", "Recordatorio de factura"],
    "Remerciement": ["Thank you", "Agradecimiento"],
    "Message libre": ["Free message", "Mensaje libre"],
    "Ouvrir WhatsApp": ["Open WhatsApp", "Abrir WhatsApp"],
    "Ouvrir l\'email": ["Open the email", "Abrir el email"],
    "Une adresse ou un numéro corrigé ici est enregistré sur la fiche.":
        ["An address or number corrected here is saved on the record.",
         "Una dirección o un número corregido aquí se guarda en la ficha."],
    "Perfumes Trade prépare le message et ouvre ton mail ou WhatsApp avec le texte dedans. C'est toi qui appuies sur Envoyer, une personne à la fois. L'envoi à toute une liste d'un coup demandera le serveur.":
        ["Perfumes Trade prepares the message and opens your mail app or WhatsApp with the text inside. You are the one who presses Send, one person at a time. Sending to a whole list at once will require the server.",
         "Perfumes Trade prepara el mensaje y abre tu correo o WhatsApp con el texto dentro. Eres tú quien pulsa Enviar, una persona cada vez. Enviar a toda una lista de golpe requerirá el servidor."],

    # ---------- divers ----------
    "automatique": ["automatic", "automático"],
    "Photo": ["Photo", "Foto"],
    "Clients": ["Customers", "Clientes"],

    # ---- encaissement en plusieurs fois (Factures / Ventes) ----
    "Encaisser": ["Record a payment", "Registrar un pago"],
    "Encaisser le reste": ["Collect the balance", "Cobrar el saldo"],
    "Voir les paiements": ["View payments", "Ver los pagos"],
    "Montant reçu": ["Amount received", "Importe recibido"],
    "Réglé comment": ["Paid how", "Forma de pago"],
    "Référence (facultatif)": ["Reference (optional)", "Referencia (opcional)"],
    "n° de transaction, nom sur le Zelle…": ["transaction no., name on the Zelle…", "n.º de transacción, nombre en el Zelle…"],
    "Enregistrer le paiement": ["Save the payment", "Guardar el pago"],
    "total de la facture": ["invoice total", "total de la factura"],
    "déjà reçu": ["already received", "ya recibido"],
    "reste dû": ["still owed", "queda por cobrar"],
    "Mode": ["Method", "Forma"],
    "Référence": ["Reference", "Referencia"],
    "Montant": ["Amount", "Importe"],
    "retirer": ["remove", "quitar"],
    "Retirer ce versement": ["Remove this payment", "Quitar este pago"],
    "Tout le reste": ["The whole balance", "Todo el saldo"],
    "La moitié": ["Half", "La mitad"],
    "Un tiers": ["A third", "Un tercio"],
    "paiement enregistré": ["payment saved", "pago guardado"],
    "Indique un montant.": ["Enter an amount.", "Indica un importe."],
    "repris de l'ancienne saisie": ["carried over from the old entry", "recuperado de la entrada anterior"],
    # ---- Perfume City : le flacon de vitrine ----
    "Ce que Perfume City reçoit": ["What Perfume City receives", "Lo que recibe Perfume City"],
    "en vente": ["for sale", "a la venta"],
    "en vitrine (testeur)": ["in the window (tester)", "en el escaparate (tester)"],
    "flacons livrés": ["bottles delivered", "frascos entregados"],
    "Transfert vers Perfume City": ["Transfer to Perfume City", "Traslado a Perfume City"],
    "marchandise sortie pour la boutique": ["stock sent out to the shop", "mercancía enviada a la tienda"],
    "transférée à Perfume City": ["transferred to Perfume City", "trasladada a Perfume City"],
    # ---- import d'un export de caisse ----
    "Les colonnes ne sont pas les bonnes ? Corrige-les ici": ["Wrong columns? Fix them here", "¿Columnas equivocadas? Corrígelas aquí"],
    "Code-barres (SKU)": ["Barcode (SKU)", "Código de barras (SKU)"],
    "Quantité": ["Quantity", "Cantidad"],
    "Prix unitaire": ["Unit price", "Precio unitario"],
    "N° de ticket": ["Receipt no.", "N.º de ticket"],
    "Désignation": ["Description", "Descripción"],
    "Magasin / caisse": ["Outlet / register", "Tienda / caja"],
    "Magasin à importer": ["Outlet to import", "Tienda a importar"],
    "— aucune —": ["— none —", "— ninguna —"],
    "— tous —": ["— all —", "— todas —"],

    # ---- ventes qui arrivent toutes seules ----
    "vente en attente": ["sale waiting", "venta en espera"],
    "ventes en attente": ["sales waiting", "ventas en espera"],
    "Tout ignorer": ["Ignore all", "Ignorar todo"],
    "Ignorer": ["Ignore", "Ignorar"],
    "Quand": ["When", "Cuándo"],
    "D'où": ["From", "De dónde"],
    "Contenu": ["Contents", "Contenido"],
    "Les voir": ["View them", "Verlas"],
    "Site": ["Website", "Sitio"],
    "Caisse": ["Register", "Caja"],
    "retour": ["return", "devolución"],
    "Aujourd'hui": ["Today", "Hoy"],
    "Hier": ["Yesterday", "Ayer"],
    "un lundi moyen": ["an average Monday", "un lunes promedio"],
    "Adresse du site": ["Website address", "Dirección del sitio"],

    "de plus que le stock": ["more than the stock on hand", "más que el stock"],
    "vendu à découvert": ["sold beyond stock on hand", "vendido sin stock"],

    "fiche vient du site": ["record comes from the website", "ficha viene del sitio"],
    "fiches viennent du site": ["records come from the website", "fichas vienen del sitio"],
    "Ramasser les commandes": ["Fetch the orders", "Recoger los pedidos"],
    "Ramasser les clients": ["Fetch the customers", "Recoger los clientes"],
}
