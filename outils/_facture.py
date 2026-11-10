# -*- coding: utf-8 -*-
"""Factures et devis envoyés aux clients (surtout les grossistes).

Avant : Sam envoyait des captures d'écran. Ici, une vente enregistrée peut devenir une facture
(ou un devis, qui ne touche pas au stock), avec :
  - le mode de paiement (Zelle, carte avec les frais, espèces, virement, crédit, à payer),
  - la sales tax de Floride, ou l'exonération (resale certificate, passeport étranger), gardée
    sur la fiche du client pour la fois suivante,
  - l'en-tête et le pied réglés dans Réglages > Factures et devis,
  - un document propre à imprimer / enregistrer en PDF, et un texte prêt pour WhatsApp ou l'email.
Tout vit dans factures-v1 (magasin partagé sur le serveur) : f.doc porte le document.
"""

CSS = r"""
/* ---- bloc facturation dans la fenêtre de vente ---- */
.docbloc{margin:12px 0 4px;padding:12px 14px;border:1px dashed var(--line);border-radius:10px;background:var(--surface-2)}
.docbloc .fg{margin:0}
.docbloc .tot{margin-top:8px;font-size:13px;color:var(--ink-2);display:grid;grid-template-columns:auto auto;gap:3px 18px;width:max-content}
.docbloc .tot b{color:var(--ink);font-variant-numeric:tabular-nums}
.docbloc .tot .tt{font-size:15px}
.docbloc small{display:block;color:var(--ink-3);font-size:11.5px;margin-top:3px;line-height:1.4}
/* ---- la liste des factures et devis ---- */
.docs{margin:0 0 22px}
.docs table{width:100%;border-collapse:collapse;font-size:13.5px;background:var(--surface);border:1px solid var(--line);border-radius:10px;overflow:hidden}
.docs th{text-align:left;font-family:Inter,sans-serif;font-size:10.5px;letter-spacing:.09em;text-transform:uppercase;color:var(--ink);font-weight:800;padding:9px 12px;background:var(--surface-2);border-bottom:1px solid var(--line)}
.docs td{padding:9px 12px;border-bottom:1px solid var(--line-2);vertical-align:middle}
.docs tr:last-child td{border-bottom:0}
.docs td.r,.docs th.r{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
/* sur un téléphone, la liste défile dans son cadre au lieu d'élargir toute la page */
#docs-table{overflow-x:auto;-webkit-overflow-scrolling:touch}
.docs table{min-width:100%}
.docs .st{display:inline-block;padding:3px 9px;border-radius:99px;font-family:Inter,sans-serif;font-size:11px;font-weight:700;letter-spacing:.04em}
.docs .st.paye{background:var(--good-soft);color:var(--good)}
.docs .st.partiel{background:var(--warn-soft);color:var(--warn)}
.docs .st.apayer{background:var(--crit-soft);color:var(--crit)}
.docs .st.devis{background:var(--iris-soft);color:var(--iris)}
.docs .st.converti{background:var(--surface-2);color:var(--ink-3)}
.docs .btn.sm{padding:5px 9px;font-size:12px}
.docs .chips{display:flex;gap:6px;margin:0 0 10px;flex-wrap:wrap}
.docs .chips button{border:1px solid var(--line);background:var(--surface);border-radius:99px;padding:5px 12px;font:600 12.5px Inter,sans-serif;color:var(--ink-2);cursor:pointer}
.docs .chips button.on{background:var(--ink);color:#fff;border-color:var(--ink)}
/* ---- le document ---- */
#docov{position:fixed;inset:0;background:rgba(20,18,26,.55);z-index:9000;display:none;overflow:auto;padding:24px 12px}
#docov.on{display:block}
.docw{max-width:860px;margin:0 auto}
.doctb{display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin-bottom:10px}
.doctb .sp{flex:1}
.doctb .doc-etat{font-size:12px;color:#d9d4e6;max-width:340px;line-height:1.3}
#waov,#mailov{position:fixed;inset:0;background:rgba(20,18,26,.55);z-index:9100;display:none;align-items:flex-start;justify-content:center;padding:60px 12px;overflow:auto}
#waov.on,#mailov.on{display:flex}
.mailw{background:var(--surface,#fff);border-radius:12px;width:100%;max-width:560px;padding:22px 24px;box-shadow:0 24px 60px rgba(0,0,0,.3);font-family:Inter,system-ui,sans-serif}
.mailw h3{margin:0 0 14px;font-size:18px}
.mailw .mf{display:flex;flex-direction:column;gap:5px;margin-bottom:12px}
.mailw label{font-size:10.5px;font-weight:700;letter-spacing:.09em;text-transform:uppercase;color:var(--ink-3,#777)}
.mailw input,.mailw textarea{font:14px/1.45 inherit;padding:9px 11px;border:1px solid var(--line,#ddd);border-radius:8px;width:100%;box-sizing:border-box}
.mailw .mail-note{font-size:12.5px;color:var(--ink-3,#777);margin:0 0 14px}
.mailw .mail-btns{display:flex;gap:8px;align-items:center}.mailw .sp{flex:1}
.mailw .doc-etat{font-size:12.5px;color:var(--ink-2,#555)}
/* ---------- LE DOCUMENT ENVOYÉ AU CLIENT ----------
   Ce papier-là sort de l'entreprise : c'est le seul écran de l'outil qu'un client
   voit, et il parle de parfums de luxe. Il n'a donc pas la même typographie que le
   reste de l'ERP — le reste est fait pour travailler vite, celui-ci pour être reçu.

   Le choix : un romain à empattements (Cormorant Garamond) pour la raison sociale,
   le mot FACTURE et les totaux ; une linéale (Inter) pour le tableau et les
   mentions. C'est l'appariement classique de la papeterie haut de gamme — la
   lettre dessinée pour l'apparat, la lettre dessinée pour être lue. Tout en
   Garamond serait illisible sur une colonne de chiffres ; tout en Inter ferait
   facture d'atelier.

   Le reste tient à trois règles : beaucoup de blanc, des filets fins plutôt que
   des traits épais, et des capitales espacées pour les intitulés. */
.doc{background:#fff;color:#16151a;border-radius:4px;padding:58px 62px 44px;
font:14px/1.62 Inter,system-ui,sans-serif;box-shadow:0 24px 70px rgba(0,0,0,.34);
font-variant-numeric:tabular-nums}
.doc .tete{display:flex;justify-content:space-between;gap:36px;align-items:flex-start;
padding-bottom:22px;border-bottom:1px solid #16151a}
.doc .ident{display:flex;gap:18px;align-items:flex-start;min-width:0;flex:1}
.doc .logo{flex:none;max-width:220px;max-height:150px;object-fit:contain}
.doc .soc b{font-family:"Cormorant Garamond",Garamond,"Times New Roman",serif;
font-size:31px;font-weight:600;letter-spacing:.045em;line-height:1.06;display:block;color:#16151a}
.doc .soc .ens{display:block;font-family:Inter,sans-serif;font-size:11px;font-weight:600;
letter-spacing:.19em;text-transform:uppercase;color:#8a8590;margin:5px 0 11px}
.doc .soc span{display:block;color:#55525c;font-size:12.5px;line-height:1.62;white-space:nowrap}
/* Le libellé « Sales tax n° » vit DANS une de ces lignes. Sans cette règle il
   hérite du display:block et se retrouve seul sur sa ligne, le numéro en dessous :
   ça ressemble à un défaut d'impression sur un document qui part chez un client. */
.doc .soc span span{display:inline}
.doc .titre{text-align:right;flex:none}
.doc .titre h2{margin:0;font-family:"Cormorant Garamond",Garamond,serif;font-size:36px;white-space:nowrap;
font-weight:300;letter-spacing:.16em;text-transform:uppercase;line-height:1;color:#16151a}
.doc .titre .num{display:block;margin-top:9px;font-size:12.5px;font-weight:700;
letter-spacing:.08em;color:#16151a}
.doc .titre span{display:block;color:#8a8590;font-size:12px;letter-spacing:.02em}

.doc .parties{display:grid;grid-template-columns:1fr 1fr;gap:38px;margin:14px 0 12px}
.doc .parties h4{margin:0 0 7px;font-size:9.5px;letter-spacing:.2em;text-transform:uppercase;
color:#8a8590;font-weight:700}
.doc .parties div{font-size:13px;color:#55525c;line-height:1.65}
.doc .parties div b{display:block;color:#16151a;font-size:14.5px;font-weight:600;margin-bottom:2px}
.doc .parties div b.inl{display:inline;font-size:13.5px;margin:0}

.doc table{width:100%;border-collapse:collapse;margin-top:6px}
.doc th{text-align:left;font-size:9.5px;letter-spacing:.2em;text-transform:uppercase;color:#8a8590;
font-weight:700;border-bottom:1px solid #16151a;padding:0 8px 9px}
.doc td{padding:13px 8px;border-bottom:1px solid #ebe9ee;vertical-align:top;font-size:13.5px}
.doc td.r,.doc th.r{text-align:right;white-space:nowrap}
.doc td.n{color:#b4b0bb;font-size:12px;width:26px}
.doc td b{font-weight:600}
.doc td small{display:block;color:#a8a4b0;font-size:11px;letter-spacing:.04em;margin-top:2px}

.doc .totaux{margin:22px 0 0 auto;width:340px}
.doc .totaux div{display:flex;justify-content:space-between;gap:20px;padding:6px 8px;font-size:13.5px;color:#55525c}
.doc .totaux div b{color:#16151a;font-weight:600}
.doc .totaux .rem b,.doc .totaux .rem span{color:#7a6a3f}
.doc .totaux .tt{border-top:1px solid #16151a;margin-top:7px;padding-top:13px}
/* 9 oct. 2026 (Igal : « la police du total de la facture est moche ») : le total était en Cormorant,
   dont les chiffres « elzéviriens » montent et descendent ($302.81 : le 3 et le 0 tombent sous la ligne).
   Pour un montant : Inter, chiffres de même hauteur et de même largeur, gras. */
.doc .totaux .tt span{font-family:Inter,sans-serif;font-size:13px;
font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:#16151a;align-self:center}
.doc .totaux .tt b{font-family:Inter,sans-serif;font-size:26px;font-weight:800;letter-spacing:-.01em;
font-variant-numeric:lining-nums tabular-nums;font-feature-settings:"lnum" 1,"tnum" 1}
.doc .totaux .du span,.doc .totaux .du b{color:#8f2f36;font-weight:700}

.doc .pay{margin-top:28px;padding:15px 18px;border:1px solid #ebe9ee;border-left:2px solid #16151a;
font-size:12.5px;color:#55525c;line-height:1.7}
.doc .pay b{display:block;margin-bottom:2px;font-size:9.5px;letter-spacing:.2em;
text-transform:uppercase;color:#8a8590}
.doc .pied{margin-top:34px;padding-top:14px;border-top:1px solid #ebe9ee;color:#8a8590;
font-size:11px;line-height:1.7;letter-spacing:.02em}
.doc .tampon{display:inline-block;margin-top:14px;padding:7px 18px;border:1px solid #2c6e4e;
color:#2c6e4e;font-family:"Cormorant Garamond",Garamond,serif;font-size:15px;font-weight:600;
letter-spacing:.22em;text-transform:uppercase}
.doc .tampon.devis{border-color:#5a5470;color:#5a5470}
/* ---- LES PAGES (5 nov. 2026, Sam : « pas assez de marge en haut, trop en bas ; si deux pages, bien découpées ») ----
   La feuille continue (#doc-corps) sert de source ; ce qui se voit, s'imprime et part en PDF, ce sont des PAGES Letter
   (816 × 1056 px à 96 dpi) : mêmes marges partout, aucune ligne coupée en deux, l'en-tête du tableau répété, les totaux
   jamais séparés, et le pied de page — avec « Page 1 / 2 » — toujours en bas de chaque page. */
.pages{display:flex;flex-direction:column;align-items:center;gap:22px}
.doc.pg{position:relative;width:816px;height:1056px;box-sizing:border-box;padding:58px 58px 46px;margin:0;border-radius:0;overflow:hidden;font-size:12.5px;line-height:1.55}
.doc.pg .tete{padding-bottom:18px}
.doc.pg .parties{margin:10px 0 8px}
.doc.pg table{margin-top:4px}
.doc.pg td{padding:9px 8px;font-size:12.5px}
.doc.pg .totaux{margin-top:16px}
.doc.pg .pay{margin-top:20px}
.doc.pg .pied{position:absolute;left:58px;right:58px;bottom:30px;margin:0;padding-top:10px;display:flex;justify-content:space-between;gap:16px;align-items:flex-end}
.doc.pg .pied .pgnum{flex:none;white-space:nowrap;color:#55525c;font-weight:600;letter-spacing:.08em}
.doc.pg .suite{display:flex;justify-content:space-between;align-items:baseline;gap:16px;padding-bottom:12px;margin-bottom:6px;border-bottom:1px solid #16151a}
.doc.pg .suite b{font-family:"Cormorant Garamond",Garamond,serif;font-size:22px;font-weight:600;letter-spacing:.04em}
.doc.pg .suite span{font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:#8a8590;font-weight:700}
.doc.pgmes{position:absolute;left:-20000px;top:0;visibility:hidden;width:816px;box-sizing:border-box;padding:58px 58px 46px;font-size:12.5px;line-height:1.55;box-shadow:none}
.doc.pgmes .tete{padding-bottom:18px} .doc.pgmes .parties{margin:10px 0 8px} .doc.pgmes table{margin-top:4px} .doc.pgmes td{padding:9px 8px;font-size:12.5px} .doc.pgmes .totaux{margin-top:16px} .doc.pgmes .pay{margin-top:20px}
#doc-corps.src{position:absolute;left:-20000px;top:0;width:816px;opacity:0;pointer-events:none}  /* hors écran mais rendue : les tests et les copies de texte la lisent */
@media(max-width:900px){ .pages{transform-origin:top center;transform:scale(.72)} }
@media(max-width:640px){ .doc{padding:30px 22px} .doc .logo{max-width:150px;max-height:100px}
  .doc .tete{flex-direction:column;gap:18px} .doc .titre{text-align:left}
  .doc .parties{grid-template-columns:1fr;gap:20px} .doc .totaux{width:100%} }
/* ---- encaisser : un paiement a la fois, avec ce qui a deja ete recu ---- */
#encov,#edov{position:fixed;inset:0;background:rgba(20,18,26,.55);z-index:9200;display:none;
align-items:flex-start;justify-content:center;padding:32px 12px;overflow:auto}
#encov.on,#edov.on{display:flex}
#encov .mod,#edov .mod{background:var(--surface);border:1px solid var(--line);border-radius:14px;
max-width:560px;width:100%;box-shadow:0 24px 70px rgba(0,0,0,.3)}
#encov .mh,#edov .mh{display:flex;align-items:center;justify-content:space-between;padding:15px 18px;
border-bottom:1px solid var(--line)}
#encov .mh h3,#edov .mh h3{margin:0;font-size:16px}
#encov .mh .x,#edov .mh .x{background:none;border:0;font-size:20px;color:var(--ink-3);cursor:pointer;line-height:1}
#encov .mb,#edov .mb{padding:16px 18px}
#encov .mf,#edov .mf{display:flex;align-items:center;gap:8px;padding:13px 18px;border-top:1px solid var(--line)}
#encov .mf .msg,#edov .mf .msg{flex:1;font-size:12.5px;color:var(--ink-3)}
#edov .fld input,#edov .fld select{width:100%;font-family:inherit;font-size:14px;padding:8px 10px;border:1px solid var(--line);border-radius:7px;background:var(--surface-2);color:var(--ink)}
.encres{display:grid;grid-template-columns:repeat(3,1fr);gap:1px;background:var(--line);
border:1px solid var(--line);border-radius:10px;overflow:hidden;margin:0 0 14px}
.encres>div{background:var(--surface);padding:10px 12px}
.encres .v{display:block;font-family:Inter,sans-serif;font-size:19px;font-weight:700;
color:var(--ink);font-variant-numeric:tabular-nums;line-height:1.15}
.encres .k{display:block;font-size:11px;color:var(--ink-3);margin-top:2px}
.enchist{margin:0 0 14px;border:1px solid var(--line);border-radius:9px;overflow:hidden}
.enchist table{width:100%;border-collapse:collapse;font-size:13px}
.enchist th{background:var(--surface-2);text-align:left;font:800 10px Inter,sans-serif;
letter-spacing:.09em;text-transform:uppercase;color:var(--ink);padding:7px 10px}
.enchist td{padding:7px 10px;border-top:1px solid var(--line-2)}
.enchist td.r{text-align:right;font-variant-numeric:tabular-nums}
.enchist .sup{background:none;border:0;color:var(--crit);cursor:pointer;font-size:12.5px;padding:0}
.encrap{border-left:3px solid var(--iris);background:var(--iris-soft);border-radius:0 8px 8px 0;
padding:10px 13px;font-size:13px;color:var(--ink-2);line-height:1.5}
.encrap b{color:var(--ink)}
.encv{display:flex;gap:6px;margin:5px 0 0;flex-wrap:wrap}
.encv button{border:1px solid var(--line);background:var(--surface);border-radius:99px;
padding:4px 11px;font:600 12px Inter,sans-serif;color:var(--ink-2);cursor:pointer}
.encv button:hover{border-color:var(--iris);color:var(--iris)}
@media print{
  body.impr-doc > *{display:none !important}
  body.impr-doc #docov{display:block !important;position:static;background:#fff;padding:0;overflow:visible;zoom:1}
  body.impr-doc .doctb{display:none !important}
  /* une page Letter : le document fait la largeur du papier moins les marges, jamais plus */
  body.impr-doc .docw{max-width:none;width:100%}
  /* chaque page de l'écran = une page de papier, sans marge d'imprimante par-dessus (les marges sont dans la page) */
  body.impr-doc .pages{display:block;gap:0;transform:none}
  body.impr-doc .doc.pg{box-shadow:none;margin:0;page-break-after:always;break-after:page}
  body.impr-doc .doc.pg:last-child{page-break-after:auto;break-after:auto}
  body.impr-doc #doc-corps{display:none !important}
  html,body{width:auto !important;min-width:0 !important;zoom:1 !important}
  @page{size:letter;margin:0}
}
"""

# S'insère dans la fenêtre « Enregistrer une vente », après la première grille de champs.
BLOC_VENTE = r"""
<div class="docbloc" id="v-docbloc">
  <div class="fg">
    <div class="fld"><label>Document pour le client</label>
      <select id="v-doc"><option value="">Aucun — simple vente</option><option value="facture">Facture</option><option value="devis">Devis (n'engage pas le stock)</option></select></div>
    <div class="fld"><label>Paiement</label>
      <select id="v-pmode"><option value="zelle">Zelle</option><option value="carte">Carte bancaire (frais en plus)</option><option value="especes">Espèces</option><option value="cheque">Chèque</option><option value="virement">Virement</option><option value="credit">Crédit chez nous (avoir)</option></select></div>
    <div class="fld"><label>Réglé</label>
      <select id="v-pstat"><option value="paye">Payé en totalité</option><option value="partiel">Acompte reçu</option><option value="apayer">À payer</option></select>
      <input id="v-pregle" type="number" step="0.01" min="0" placeholder="montant reçu" style="display:none;margin-top:6px"></div>
    <div class="fld"><label>Remise sur le document</label>
      <div style="display:flex;gap:6px">
        <input id="v-remval" type="number" step="0.01" min="0" placeholder="0" style="flex:1;min-width:0">
        <select id="v-remtype" style="width:96px;flex:none"><option value="pct">%</option><option value="montant">$</option></select>
      </div>
      <input id="v-remlib" placeholder="motif : fidélité, fin de série…" style="margin-top:6px">
      <span class="aide">Appliquée avant la sales tax, et répartie sur les lignes : la marge du journal des ventes reste juste.</span></div>
    <div class="fld"><label>Frais d'envoi facturés ($)</label>
      <input id="v-port" type="number" step="0.01" min="0" placeholder="0">
      <span class="aide">Ce que le client paie pour l'envoi. Ajouté au total, après la sales tax (frais indiqués à part). Vide = rien.</span></div>
    <div class="fld"><label>Langue du document</label>
      <select id="v-langue"><option value="">Comme l'écran</option><option value="fr">Français</option><option value="en">English</option><option value="es">Español</option></select>
      <span class="aide">La facture part chez le client, pas chez toi : c'est SA langue qui compte. Retenue sur sa fiche, et figée sur le document une fois émis.</span></div>
    <div class="fld"><label>Taux de sales tax (%)</label>
      <input id="v-taux" type="number" step="0.01" min="0" max="20" placeholder="réglage par défaut">
      <span class="aide">Vide = le taux des Réglages. La facture garde le taux du jour où elle est émise.</span></div>
    <div class="fld" id="v-fraisbloc"><label>Frais de carte (%)</label>
      <input id="v-frais" type="number" step="0.1" min="0" max="10" placeholder="réglage par défaut">
      <span class="aide">Vide = le taux des Réglages. Mets <b>0</b> pour ne rien facturer sur ce
      document-là : un bon client, une commande où l'on absorbe les frais. Ne sert que si le
      paiement est par carte.</span></div>
    <div class="fld"><label>Sales tax</label>
      <select id="v-fiscal"><option value="taxable">Taxable (Floride)</option><option value="resale">Exonéré — resale certificate</option><option value="etranger">Exonéré — client étranger (passeport)</option></select>
      <input id="v-fref" placeholder="n° du certificat ou du passeport" style="margin-top:6px"></div>
  </div>
  <div class="tot" id="v-tot"></div>
  <small id="v-docaide"></small>
</div>
"""

# Le document lui-même (une couche par-dessus la page) et la liste.
OVERLAY = r"""
<div id="docov"><div class="docw">
  <div class="doctb">
    <button class="btn pri" id="doc-wa">WhatsApp</button>
    <button class="btn pri" id="doc-mail">Email</button>
    <button class="btn" id="doc-pdf">Télécharger le PDF</button>
    <button class="btn" id="doc-part" style="display:none">Partager le PDF…</button>
    <button class="btn" id="doc-print">Imprimer</button>
    <button class="btn" id="doc-copie">Copier le texte</button>
    <span class="doc-etat" id="doc-etat"></span>
    <span class="sp"></span>
    <button class="btn" id="doc-paye" style="display:none">Marquer payée</button>
    <button class="btn" id="doc-edit" title="Corriger le client, la date, le paiement, la taxe, la langue ou la note">Modifier</button>
    <button class="btn" id="doc-lignes" style="display:none" title="Rouvrir la cote dans le formulaire : parfums, quantités, prix">Modifier les parfums et les prix</button>
    <button class="btn" id="doc-conv" style="display:none">Transformer en facture</button>
    <button class="btn" id="doc-x">Fermer</button>
  </div>
  <div class="doc src" id="doc-corps"></div>
  <div class="pages" id="doc-pages"></div>
</div></div>
<div id="edov" class="ov"><div class="mod" style="max-width:560px">
  <div class="mh"><h3>Modifier le document</h3><button class="x" id="ed-x" title="Fermer">&times;</button></div>
  <div class="mb" style="display:grid;grid-template-columns:1fr 1fr;gap:12px">
    <div class="fld"><label>Client</label><input id="ed-tiers" autocomplete="off"></div>
    <div class="fld"><label>Date</label><input id="ed-date" type="date"></div>
    <div class="fld"><label>Paiement</label><select id="ed-pmode"><option value="zelle">Zelle</option><option value="carte">Carte bancaire (frais en plus)</option><option value="especes">Espèces</option><option value="cheque">Chèque</option><option value="virement">Virement</option><option value="credit">Crédit chez nous (avoir)</option><option value="enligne">Payé en ligne</option><option value="caisse">Payé à la caisse</option></select></div>
    <div class="fld"><label>Langue du document</label><select id="ed-langue"><option value="fr">Français</option><option value="en">English</option><option value="es">Español</option></select></div>
    <div class="fld"><label>Sales tax</label><select id="ed-fiscal"><option value="taxable">Taxable (Floride)</option><option value="resale">Exonéré — resale certificate</option><option value="etranger">Exonéré — client étranger (passeport)</option></select></div>
    <div class="fld"><label>N° du certificat ou du passeport</label><input id="ed-fref" autocomplete="off"></div>
    <div class="fld" style="grid-column:1/-1"><label>Note sur le document</label><input id="ed-note" autocomplete="off"></div>
    <p class="ecr" style="grid-column:1/-1;margin:0;font-size:12.5px;color:var(--ink-2)">Les lignes (parfums, quantités, prix) ne se corrigent pas ici : elles ont bougé le stock. Pour les changer, annule la facture dans Factures et enregistre la bonne.</p>
  </div>
  <div class="mf"><span class="msg" id="ed-msg"></span><span class="sp"></span><button class="btn" id="ed-ann">Annuler</button><button class="btn pri" id="ed-ok">Enregistrer</button></div>
</div></div>
<div id="waov"><div class="mailw">
  <h3>Numéro WhatsApp du client</h3>
  <div class="mf"><label>Téléphone</label><input id="wa-a" type="tel" placeholder="305 555 0100" autocomplete="off"></div>
  <p class="mail-note">Pas de numéro sur la fiche de ce client : tape-le, il sera gardé pour la prochaine fois.</p>
  <div class="mail-btns"><span class="doc-etat" id="wa-etat"></span><span class="sp"></span>
    <button class="btn" id="wa-ann">Annuler</button><button class="btn pri" id="wa-ok">Ouvrir WhatsApp</button></div>
</div></div>
<div id="mailov"><div class="mailw">
  <h3>Envoyer par email</h3>
  <div class="mf"><label>À</label><input id="mail-a" type="email" placeholder="adresse du client" autocomplete="off"></div>
  <div class="mf"><label>Objet</label><input id="mail-sujet"></div>
  <div class="mf"><label>Message</label><textarea id="mail-txt" rows="6"></textarea></div>
  <p class="mail-note">Le PDF du document est joint au courrier.</p>
  <p class="mail-note"><span>Part de</span> <b id="mail-de" data-nolang></b></p>
  <div class="mail-btns"><span class="doc-etat" id="mail-etat"></span><span class="sp"></span>
    <button class="btn" id="mail-ann">Annuler</button><button class="btn pri" id="mail-ok">Envoyer</button></div>
</div></div>

<div id="encov"><div class="mod">
  <div class="mh"><h3>Encaisser</h3><button class="x" id="enc-x" title="Fermer">&times;</button></div>
  <div class="mb">
    <div class="encres" id="enc-res"></div>
    <div id="enc-hist"></div>
    <div class="fg">
      <div class="fld"><label>Montant reçu</label>
        <input id="enc-mt" type="number" step="0.01" min="0" inputmode="decimal" placeholder="0.00">
        <div class="encv" id="enc-v"></div></div>
      <div class="fld"><label>Réglé comment</label>
        <select id="enc-mode"><option value="zelle">Zelle</option><option value="carte">Carte bancaire</option><option value="especes">Espèces</option><option value="cheque">Chèque</option><option value="virement">Virement</option><option value="credit">Crédit chez nous (avoir)</option></select></div>
      <div class="fld"><label>Quand</label><input id="enc-d" type="date"></div>
      <div class="fld"><label>Référence (facultatif)</label><input id="enc-ref" placeholder="n° de transaction, nom sur le Zelle…"></div>
    </div>
    <div class="encrap" id="enc-rap"></div>
  </div>
  <div class="mf"><span class="msg" id="enc-msg"></span>
    <button class="btn" id="enc-ann">Annuler</button>
    <button class="btn pri" id="enc-ok" disabled>Enregistrer le paiement</button></div>
</div></div>
"""

LISTE = r"""
<div class="docs" id="docs">
  <h2 class="sec">Factures et devis <em id="docs-em"></em></h2>
  <div class="chips" id="docs-chips"></div>
  <div id="docs-table"></div>
</div>
"""

JS = r"""
/* ============ FACTURES ET DEVIS ============ */
/* Sam, 3 oct. 2026 : « il faut rajouter l'option Check dans les paiements » */
const FMODES={zelle:'Zelle',carte:'Carte bancaire',especes:'Espèces',cheque:'Chèque',virement:'Virement',credit:'Crédit chez nous',enligne:'Payé en ligne',caisse:'Payé à la caisse'};
const FSTAT={paye:'Payée',partiel:'Acompte',apayer:'À payer',devis:'Devis',converti:'Devis transformé'};
/* L'en-tête figé dans chaque document (raison sociale, adresse, mentions…) SANS le logo :
   le logo est une image de ~24 Ko, recopiée dans chacune des factures, et 120 factures
   remplissaient à elles seules la moitié de la mémoire du navigateur (5 Mo) — au point
   que plus rien ne s'enregistrait (30 sept. 2026). Le logo affiché est celui des Réglages. */
function enteteDoc(pc){ const e=Object.assign({},pc?factRegPC():factReg()); delete e.logo; if(pc) e.pc=true; return e; }
function logoDoc(E){ return (E&&E.pc)?(factRegPC().logo||''):((E&&E.logo)||factReg().logo||''); }
/* Perfume City : la boutique de Sam (tenue par Kim) a son propre papier à en-tête.
   Une vente faite sur ce canal, payée par exemple en Zelle, peut donner lieu à une facture
   que le client réclame : elle part au nom de PERFUME CITY, jamais de DASY (Igal, 13 oct. 2026).
   Ce n'est pas une facture de Sam à la boutique — c'est la facture de la boutique à SON client.
   Ses coordonnées vivent dans Réglages (REG.factPC) ; le taux de sales tax, les frais de carte
   et les conditions restent ceux de l'entreprise. */
const canalPC=n=>/perfume\s*(in\s*the\s*)?city/i.test(String(n||''));
function factRegPC(){
  const R=lit(KREG,{}), P=Object.assign({raison:'',enseigne:'Perfume City',adresse:'',tel:'',email:'',insta:'',taxid:'',zelle:'',prefixe:'PC',logo:''},R.factPC||{});
  if(!P.raison) P.raison=P.enseigne||'Perfume City';
  if(!P.prefixe) P.prefixe='PC';
  return Object.assign({},factReg(),P,{pc:true});
}
/* l'en-tête à lire pour un document : celui de Perfume City reste figé tel qu'émis ; les autres suivent les Réglages */
function enteteVue(D){ return (D&&D.entete&&D.entete.pc)?D.entete:factReg(); }
function factReg(){
  const R=lit(KREG,{}); const F=Object.assign({raison:'',enseigne:'Perfumes Trade',adresse:'',tel:'',email:'',taxid:'',taux:7,carte:2.6,zelle:'',prefixe:'PT',conditions:'',exo:''},R.fact||{});
  if(!F.raison) F.raison=R.societe||'DASY LLC';
  return F;
}
/* numéro suivant : PT-2026-0001 pour les factures, DV-2026-0001 pour les devis, OF-2026-0001 pour les offres (10 nov. 2026) */
/* l'offre de prix (rubrique Offre, 10 nov. 2026) : un devis marqué « offre » — même document, autre nom, jamais converti en facture */
const OFFRE_MOT={fr:'Offre',en:'Offer',es:'Oferta'};
const offreMot=D=>OFFRE_MOT[(D&&D.langue)||(typeof LANG!=='undefined'?LANG:'fr')]||'Offer';
function docNum(type,d,pc){
  const F=pc?factRegPC():factReg(), an=(d||new Date().toISOString()).slice(0,4);
  const pre=(type==='offre'?'OF':type==='devis'?'DV':(F.prefixe||'PT').toUpperCase())+'-'+an+'-';
  let n=0; FACT.forEach(f=>{ const m=f.doc&&f.doc.num&&String(f.doc.num).startsWith(pre)?+String(f.doc.num).slice(pre.length):0; if(m>n) n=m; });
  return pre+String(n+1).padStart(4,'0');
}
/* les totaux d'un document : sous-total, frais carte, sales tax, total, reste dû */
/* Un nombre, ou zéro — jamais NaN.
   `(l.p||0)` avait l'air d'un garde-fou et n'en était pas un : `||` ne rattrape
   que ce qui est faux. Une chaîne comme « abc » ou « 12,50 » est VRAIE, elle
   traversait le garde-fou intacte, et `2 * '12,50'` vaut NaN. Ce NaN remontait
   ensuite dans le sous-total, la taxe et le total : un document entier à « NaN $ »
   part chez le client sans qu'aucune erreur ne s'affiche nulle part.
   On ne devine surtout pas la virgule : aux États-Unis « 1,250 » vaut mille deux
   cent cinquante, pas 1,25. Lire la virgule comme un séparateur décimal
   fabriquerait une facture fausse d'un facteur mille — bien pire qu'un zéro.
   Une ligne à 0 $ se voit ; un NaN paralyse tout ; un montant deviné passe
   inaperçu. On prend donc le zéro, et la saisie reste à corriger à la main.
   Le nom : `nb` était déjà pris par une fonction locale de sortieCsv, dans
   _sortie.py, qui met une virgule décimale pour Excel. Les deux cohabitaient
   sans dommage — la locale masque la globale — mais deux `nb` différentes
   dans du code qui manipule des montants, c'est une chausse-trappe posée
   pour le prochain qui touchera à l'export.
   (On convertit avec Number et non parseFloat, qui lit « 12,50 » comme 12 en
   s'arrêtant à la virgule : encore un chiffre faux et silencieux.) */
const nbSur=v=>{ const n=Number(v); return Number.isFinite(n)?n:0; };
/* Le prix AFFICHÉ d'une ligne. Une remise est répartie sur les lignes à l'enregistrement :
   la ligne garde le prix encaissé (p, pour la marge et le stock) et le prix affiché (pAv).
   Le document se calcule toujours sur le prix affiché, la remise s'applique une fois en bas.
   (3 oct. 2026 : modifier une facture remisée, ou transformer un devis remisé en facture,
   recalculait sur les prix déjà remisés — la remise était comptée deux fois.) */
const puDoc=l=>(l&&l.remise&&l.pAv!=null)?l.pAv:(l?l.p:null);

function calcDoc(lignes,o){
  const F=factReg();
  const sousTotal=Math.round(lignes.reduce((a,l)=>a+nbSur(l.q)*nbSur(puDoc(l)),0)*100)/100;

  /* La remise s'applique AVANT la taxe et avant les frais de carte : on ne paie
     pas de taxe sur ce qu'on ne facture pas, et la commission de carte porte sur
     ce qui est réellement encaissé. L'inverse gonflerait la facture du client. */
  const remType=(o.remType==='montant')?'montant':'pct';
  let remVal=+o.remVal||0; if(remVal<0) remVal=0;
  if(remType==='pct' && remVal>100) remVal=100;
  let remise = remType==='pct' ? Math.round(sousTotal*remVal)/100 : Math.round(remVal*100)/100;
  if(remise>sousTotal) remise=sousTotal;                 /* jamais un sous-total négatif */
  const remPct = sousTotal>0 ? Math.round(remise/sousTotal*1000)/10 : 0;
  const base = Math.round((sousTotal-remise)*100)/100;

  /* Les frais de carte : le taux des Réglages par défaut, mais le document peut
     le remplacer — 0 compris. Le test est sur la CHAÎNE vide, pas sur la valeur :
     `+o.frais||F.carte` aurait transformé un 0 délibéré en « prends le taux par
     défaut », c'est-à-dire exactement le contraire de ce que Sam a demandé. */
  const fraisRef = (o.frais===''||o.frais==null||isNaN(+o.frais)) ? (+F.carte||0) : +o.frais;
  const fraisPct=o.pmode==='carte'?fraisRef:0, frais=Math.round(base*fraisPct)/100;
  /* Le taux de taxe vient du document quand il y est, des Réglages sinon : deux
     clients peuvent relever de deux taux, et une facture émise garde le sien même
     si le réglage change l'an prochain. */
  const tauxRef = (o.taux===''||o.taux==null||isNaN(+o.taux)) ? (+F.taux||0) : +o.taux;
  const taux=o.fiscal==='taxable'?tauxRef:0, taxe=Math.round((base+frais)*taux)/100;
  /* Les frais d'envoi (Sam, 6 oct. 2026) : indiqués à part, après la taxe, ajoutés au total.
     Ils n'entrent ni dans la remise ni dans les frais de carte. */
  let port=+o.port||0; if(port<0||isNaN(port)) port=0; port=Math.round(port*100)/100;
  const total=Math.round((base+frais+taxe+port)*100)/100;
  const regle=o.pstat==='paye'?total:(o.pstat==='partiel'?Math.min(total,+o.regle||0):0);
  return {sousTotal,remType,remVal,remise,remPct,remLib:(o.remLib||'').slice(0,60),base,
          fraisPct,frais,taux,taxe,port,total,regle,reste:Math.max(0,Math.round((total-regle)*100)/100)};
}

/* La remise répartie sur les lignes, au prorata de leur montant.
   Pourquoi c'est indispensable : si la remise n'était qu'une ligne sur le papier,
   l'ERP enregistrerait les ventes au prix plein et la marge serait fausse, à la
   hausse. Une remise de 10 % sur 2 178 $, c'est 218 $ de marge envolés que
   personne ne verrait. Le document montre la remise en clair, le journal des
   ventes enregistre les prix réellement encaissés. */
function repartitRemise(lignes,c){
  if(!c || !c.remise || !c.sousTotal) return lignes;
  const k=(c.sousTotal-c.remise)/c.sousTotal;
  return lignes.map(l=>{ const q=+l.q||0, p=l.p==null?null:+l.p;
    if(!q || p==null) return l;
    return Object.assign({},l,{p:Math.round(p*k*100)/100, pAv:p, remise:true}); });
}
function docStatut(f){
  if(!f.doc) return '';
  if(f.doc.type==='devis') return f.doc.converti?'converti':'devis';
  return f.doc.reste>0?(f.doc.regle>0?'partiel':'apayer'):'paye';
}
/* ---- dans la fenêtre de vente ---- */
function docChampsMaj(){
  const on=!!$('v-doc').value;
  ['v-pmode','v-pstat','v-pregle','v-fiscal','v-fref','v-remval','v-remtype','v-remlib','v-taux','v-langue','v-frais','v-port']
    .forEach(i=>{ const e=$(i); if(e) e.disabled=!on; });
  $('v-pregle').style.display=(on&&$('v-pstat').value==='partiel')?'':'none';
  /* les frais de carte ne se montrent que quand ils peuvent servir : un champ qui
     ne change rien à l'écran est un champ qu'on remplit pour rien */
  if($('v-fraisbloc')) $('v-fraisbloc').style.display=(on&&$('v-pmode').value==='carte')?'':'none';
  $('v-fref').style.display=(on&&$('v-fiscal').value!=='taxable')?'':'none';
  if($('v-doc').value==='devis'){ $('v-stock').checked=false; $('v-stock').disabled=true; }
  else { $('v-stock').disabled=false; if(!$('v-stock').dataset.touche) $('v-stock').checked=true; }
  const pcC=!!($('v-canal')&&canalPC($('v-canal').value));
  const F=pcC?factRegPC():factReg();
  $('v-docaide').textContent = !on ? '' :
    ($('v-doc').value==='devis'&&typeof MODE_OFFRE!=='undefined'&&MODE_OFFRE) ? r3('Une offre de prix ne sort rien du stock et ne devient jamais une facture : quand le client veut acheter, « Faire la cote ».','A price offer takes nothing out of stock and never becomes an invoice: when the customer wants to buy, “Make the quote”.','Una oferta de precio no saca nada del stock y nunca se convierte en factura: cuando el cliente quiere comprar, «Hacer la cotización».')
    : $('v-doc').value==='devis' ? 'Un devis ne sort rien du stock. Il pourra être transformé en facture en un clic, quand le client confirme.'
    : (pcC?'En-tête PERFUME CITY sur cette facture. ':'')
      + (F.raison&&F.adresse?'':'L\'en-tête de la facture est incomplet (raison sociale, adresse…) : Réglages › Factures et devis'+(pcC?' › Perfume City':'')+'. ')
      + (!$('v-client').value.trim()?'Indique le client : une facture sans client n\'a pas de sens.':'');
  docTotaux();
}
function docTotaux(){
  const on=!!$('v-doc').value; const T=$('v-tot');
  if(!on){ T.innerHTML=''; return; }
  const c=calcDoc(PANIER,docOpts());
  T.innerHTML=`<span>Sous-total</span><b>${money2(c.sousTotal)}</b>
    ${c.remise?`<span>Remise${c.remType==='pct'?' '+c.remVal+' %':''}${c.remLib?' · '+esc(c.remLib):''}</span><b style="color:var(--crit)">−${money2(c.remise)}</b>`:''}
    ${c.frais?`<span>Frais carte ${c.fraisPct} %</span><b>${money2(c.frais)}</b>`:''}
    <span>${c.taux?'Sales tax '+c.taux+' %':'Sales tax — exonéré'}</span><b>${money2(c.taxe)}</b>
    ${c.port?`<span>Frais d'envoi</span><b>${money2(c.port)}</b>`:''}
    <span class="tt">Total</span><b class="tt">${money2(c.total)}</b>
    ${c.reste>0&&$('v-doc').value!=='devis'?`<span>Reste dû</span><b style="color:var(--crit)">${money2(c.reste)}</b>`:''}`;
}
/* le statut fiscal se retient par client */
function docClientChange(){
  const nom=$('v-client').value.trim(); const c=nom?(lit(KCLI,{})[nom]||{}):{};
  if(c.fiscal){ $('v-fiscal').value=c.fiscal; $('v-fref').value=c.fiscalRef||''; }
  if(c.pmode&&FMODES[c.pmode]) $('v-pmode').value=c.pmode;
  $('v-langue').value = c.langue || '';
  docChampsMaj();
}
['v-doc','v-pmode','v-pstat','v-fiscal','v-remtype','v-langue'].forEach(i=>$(i).addEventListener('change',docChampsMaj));
['v-pregle','v-remval','v-taux','v-remlib','v-frais','v-port'].forEach(i=>{ const e=$(i); if(e) e.addEventListener('input',docTotaux); });
$('v-client').addEventListener('change',docClientChange);
/* changer de canal change l'en-tête : Perfume City signe ses propres factures */
if($('v-canal')) $('v-canal').addEventListener('change',docChampsMaj);
$('v-stock').addEventListener('change',()=>{ $('v-stock').dataset.touche='1'; });
/* ce que la fenêtre propose à l'ouverture : facture pour le gros, rien pour les autres canaux */
function docReset(){
  /* une vente saisie ici est une facture, sur tous les canaux — personne ne crée les
     factures, elles vont avec la vente (Igal, 12 sept. 2026) */
  $('v-doc').value='facture';
  $('v-pmode').value='zelle'; $('v-pstat').value='paye'; $('v-pregle').value=''; $('v-fiscal').value='taxable'; $('v-fref').value='';
  $('v-remval').value=''; $('v-remtype').value='pct'; $('v-remlib').value=''; $('v-taux').value='';
  if($('v-frais')) $('v-frais').value='';
  if($('v-port')) $('v-port').value='';
  $('v-langue').value='';
  delete $('v-stock').dataset.touche; $('v-stock').disabled=false;
  docChampsMaj();
}
/* ce que la vente enregistre en plus, si un document est demandé */
/* Un seul endroit qui lit les champs du document : sinon un champ ajouté est
   oublié quelque part, et l'aperçu à l'écran ne dit plus la même chose que la
   facture émise. */
function docOpts(){
  return {pmode:$('v-pmode').value, pstat:$('v-pstat').value, regle:$('v-pregle').value,
    fiscal:$('v-fiscal').value, fref:($('v-fref').value||'').trim(),
    remType:$('v-remtype').value, remVal:$('v-remval').value, remLib:($('v-remlib').value||'').trim(),
    taux:$('v-taux').value, frais:($('v-frais')?$('v-frais').value:''), port:($('v-port')?$('v-port').value:''), langue:$('v-langue').value};
}
function docPourVente(lignes,client,d,CLI,pc){
  const type=$('v-doc').value; if(!type) return null;
  const o=Object.assign(docOpts(),{pstat:type==='devis'?'apayer':$('v-pstat').value});
  const c=calcDoc(lignes,o);
  /* le statut fiscal et le mode habituel se retiennent sur la fiche du client (CLI est l'objet que la vente enregistre) */
  if(client&&CLI){ CLI[client]=Object.assign({nom:client},CLI[client]||{},
    {fiscal:o.fiscal,fiscalRef:o.fref,pmode:o.pmode,langue:o.langue||undefined}); }
  /* La langue est figée ici, comme l'en-tête : une facture rouverte dans six mois
     doit se relire exactement comme le client l'a reçue, même si l'écran a changé
     de langue entre-temps. Vide = celle de l'écran au moment de l'émission. */
  const note=($('v-note')&&$('v-note').value.trim())||'';
  return Object.assign({type,num:docNum(type,d,pc),pmode:o.pmode,pstat:o.pstat,fiscal:o.fiscal,fref:o.fref,
    langue:o.langue||(typeof LANG!=='undefined'?LANG:'fr'),note:note||undefined,
    emis:new Date().toISOString(),entete:enteteDoc(pc)},c);
}
/* ---- le document ---- */
let DOC=null;
/* 7 oct. 2026 (Igal : « Sam n'a pas du tout la même optimisation que moi, à l'impression la page
   est coupée sur les côtés, et le PDF bug ») : sur un grand écran (> 1300 px), l'ERP est
   grossi de 8 % (.wrap{zoom:1.08}). Le document vivait DANS ce cadre grossi : le PDF
   (fabriqué à partir de l'écran) et l'impression héritaient du zoom et débordaient de la
   page. Igal, sur un portable, n'avait pas le zoom — d'où « pas la même chose ». Les
   fenêtres du document sortent du cadre : elles se dessinent à l'échelle 1, partout. */
try{ ['docov','mailov','waov','edov','encov'].forEach(id=>{ const e=document.getElementById(id); if(e&&e.parentNode!==document.body) document.body.appendChild(e); }); }catch(e){}
/* Après chaque écriture, la fusion (voir _fusion) peut REMPLACER les objets de
   FACT par leurs copies fusionnées : le document ouvert (DOC) pointerait alors sur
   un objet mort, et tout ce qu'on lui écrirait ensuite — un lien, un paiement,
   « converti en facture » — partirait dans le vide. On le rattache donc à sa
   version vivante après chaque écriture. */
try{ _apresEcrit.push((cle)=>{ if(cle!==KFACT) return;
  if(DOC){ const n=FACT.find(x=>x.id===DOC.id); if(n) DOC=n; }
  if(typeof ENC!=='undefined' && ENC){ const n=FACT.find(x=>x.id===ENC.id); if(n) ENC=n; }
  if(typeof _PREP!=='undefined' && _PREP && _PREP.f){ const n=FACT.find(x=>x.id===_PREP.f.id); if(n) _PREP.f=n; } }); }catch(e){}
/* modifier un document et l'enregistrer : la modification est appliquée à la
   version vivante ET à celle qu'on tient en main, puis on écrit */
function docMaj(f,fn){
  const n=FACT.find(x=>x.id===f.id)||f; fn(n); if(n!==f) fn(f);
  try{ ecrit(KFACT,FACT); }catch(e){}
  return FACT.find(x=>x.id===f.id)||n;
}
const dus=v=>nbSur(v).toLocaleString('en-US',{minimumFractionDigits:2,maximumFractionDigits:2});
/* Le libellé d'une ligne sur le document que reçoit le client, TYPE compris.
   Le libellé est figé à l'enregistrement ; pour une vente d'avant, on va
   rechercher le type dans la fiche du parfum, sans rien inventer quand la
   référence n'existe plus. Le genre, lui, reste à l'écran : « Femme » sur une
   facture n'apprend rien au client et allonge la ligne. */
function docRef(l){
  const r=String((l&&l.ref)||'');
  try{
    if(!l||!l.cle||typeof TY!=='function') return r;
    const t=TY(l.cle); if(!t) return r;
    if(new RegExp('(^|[^A-Za-z])'+t.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')+'([^A-Za-z]|$)','i').test(r)) return r;
    return (r+' '+t).trim();
  }catch(e){ return r; }
}
function dessineDoc(f){
  DOC=f; const D=f.doc, E=D.entete||factReg(), CLI=lit(KCLI,{}), cl=CLI[f.tiers]||{nom:f.tiers||''};
  const st=docStatut(f), devis=D.type==='devis', offre=devis&&!!D.offre;
  const lgO=D.langue||(typeof LANG!=='undefined'?LANG:'fr'), o3=(a,b,c)=>lgO==='en'?b:lgO==='es'?c:a;
  const lignes=(f.lignes||[]).filter(l=>l.q);
  /* ---- la langue du document ----
     La traduction de l'outil remplace les textes reconnus MOT POUR MOT. Un nœud
     qui mélange une étiquette et une donnée (« Sales tax 7 % ») ne correspond à
     aucune entrée du dictionnaire et resterait en français sur une facture
     partie à un client américain. On sépare donc systématiquement l'étiquette,
     dans un <span class="lbl">, du chiffre ou du nom qui la suit.
     Et ce qui appartient à l'entreprise ou au client — raison sociale, adresse,
     motif de remise, conditions écrites par Sam — porte data-nolang : ces
     textes-là ne se traduisent jamais, ils se recopient. */
  $('doc-corps').innerHTML=`
   <div class="tete">
     <div class="ident">
       ${logoDoc(E)?`<img class="logo" src="${esc(logoDoc(E))}" alt="">`:''}
       <div class="soc" data-nolang><b>${esc(E.raison||'')}</b>${E.enseigne&&E.enseigne!==E.raison?`<span class="ens">${esc(E.enseigne)}</span>`:''}
         ${E.adresse?`<span>${esc(E.adresse)}</span>`:''}${E.tel?`<span>${esc(E.tel)}</span>`:''}${E.email?`<span>${esc(E.email)}</span>`:''}${E.insta?`<span>Instagram @${esc(String(E.insta).replace(/^@/,''))}</span>`:''}
         ${E.taxid?`<span><span class="lbl">Sales tax n°</span> ${esc(E.taxid)}</span>`:''}</div>
     </div>
     <div class="titre"><h2${offre?' data-nolang':''}>${offre?offreMot(D):devis?'Devis':'Facture'}</h2>
       <span class="num" data-nolang>${esc(D.num)}</span>
       <span data-nolang>${dfr(f.d)}</span>
       ${offre?`<span data-nolang>${o3('Valable 30 jours','Valid for 30 days','Válida 30 días')}</span>`:devis?`<span>Valable 15 jours</span>`:''}</div>
   </div>
   <div class="parties">
     <div><h4>${devis?'Adressé à':'Facturé à'}</h4>
       <div data-nolang><b>${esc(cl.raison||cl.nom||'')}</b>${[cl.raison&&cl.nom!==cl.raison?cl.nom:'',cl.adresse,cl.tel,cl.email].filter(Boolean).map(esc).join('<br>')}</div></div>
     <div><h4>Conditions</h4><div><span class="lbl">Paiement</span> : <b class="inl">${esc(FMODES[D.pmode]||D.pmode)}</b>${D.fiscal!=='taxable'&&D.fref?`<br><span class="lbl">${D.fiscal==='etranger'?'Passeport':'Resale certificate'}</span> : <span data-nolang>${esc(D.fref)}</span>`:''}${D.note?`<br><span class="lbl">Note</span> : <span data-nolang>${esc(D.note)}</span>`:''}</div></div>
   </div>
   <table><thead><tr><th>#</th><th>Article</th><th class="r">Qté</th><th class="r">Prix unit.</th><th class="r">Montant</th></tr></thead>
   <tbody>${lignes.map((l,i)=>{ /* remise répartie à l'enregistrement : la ligne garde le prix
       encaissé (p) et le prix affiché (pAv). La facture montre le prix affiché ; la remise est
       en bas, une seule fois (3 oct. 2026 — sinon 153 $ en ligne ET « Remise −39,20 » dessous). */
     const pu=puDoc(l);
     return `<tr><td class="n">${i+1}</td><td data-nolang><b>${esc(docRef(l))}</b><small>${esc(l.bc||'')}</small></td><td class="r">${nf(l.q)}</td><td class="r">$${dus(pu)}</td><td class="r"><b>$${dus(nbSur(l.q)*nbSur(pu))}</b></td></tr>`; }).join('')}</tbody></table>
   <div class="totaux">
     <div><span>Sous-total</span><b>$${dus(D.sousTotal)}</b></div>
     ${D.remise?`<div class="rem"><span><span class="lbl">Remise</span>${D.remType==='pct'?' '+D.remVal+' %':''}${D.remLib?` — <span data-nolang>${esc(D.remLib)}</span>`:''}</span><b>−$${dus(D.remise)}</b></div>`:''}
     ${D.frais?`<div><span><span class="lbl">Frais carte</span> ${D.fraisPct} %</span><b>$${dus(D.frais)}</b></div>`:''}
     <div><span>${D.taux?`<span class="lbl">Sales tax</span> ${D.taux} %`:'Sales tax — exonéré'}</span><b>$${dus(D.taxe)}</b></div>
     ${D.port?`<div><span><span class="lbl">Frais d'envoi</span></span><b>$${dus(D.port)}</b></div>`:''}
     <div class="tt"><span>Total</span><b>$${dus(D.total)}</b></div>
     ${!devis&&D.regle>0&&D.reste>0?`<div><span>Reçu</span><b>$${dus(D.regle)}</b></div>`:''}
     ${!devis&&(D.regs||[]).length>1?(D.regs||[]).map(r=>`<div style="font-size:11.5px"><span>&nbsp;&nbsp;<span data-nolang>${dfr(r.d)}</span> · ${esc(FMODES[r.m]||r.m||'')}</span><b style="font-weight:500">$${dus(r.mt)}</b></div>`).join(''):''}
     ${!devis&&D.reste>0?`<div class="du"><span>Reste dû</span><b>$${dus(D.reste)}</b></div>`:''}
   </div>
   ${(()=>{
     /* Où envoyer l'argent. Deux corrections du 9 septembre :
        — un DEVIS payable par Zelle n'affichait aucune coordonnée : le client
          acceptait le devis et ne savait pas où payer ;
        — une facture due par carte ou en espèces affichait quand même l'adresse
          Zelle, ce qui invite à payer autrement que convenu.
        On l'affiche donc quand le mode de paiement l'appelle ET qu'il reste
        quelque chose à payer — devis compris, puisqu'un devis reste toujours dû. */
     const aPayer = devis || D.reste>0;
     const parVirement = (D.pmode==='zelle'||D.pmode==='virement');
     if(!aPayer || !parVirement || !E.zelle) return '';
     return `<div class="pay"><b>Pour régler</b><span data-nolang>${esc(E.zelle)}</span></div>`;
   })()}
   ${!devis&&D.reste<=0?`<div class="tampon">Payée${D.payeLe?` <span data-nolang>· ${dfr(D.payeLe)}</span>`:''}</div>`:''}
   ${offre?`<div class="tampon devis" data-nolang>${o3('Offre de prix — sans engagement de stock','Price offer — no stock commitment','Oferta de precio — sin compromiso de stock')}</div>`:devis?`<div class="tampon devis">${st==='converti'?`<span class="lbl">Transformé en facture</span> <span data-nolang>${esc(D.convertiNum||'')}</span>`:'Devis — sans engagement de stock'}</div>`:''}
   <div class="pied"><span data-nolang>${esc(E.raison||'')}${E.adresse?' · '+esc(E.adresse):''}${E.tel?' · '+esc(E.tel):''}${E.email?' · '+esc(E.email):''}</span><br>
     ${offre?`<span data-nolang>${offreMot(D)}</span>`:`<span class="lbl">${devis?'Devis':'Facture'}</span>`} <span data-nolang>${esc(D.num)}</span> ·
     <span class="lbl">émis${devis?'':'e'} par</span> <span data-nolang>${esc(f.par||'')}</span> ·
     <span data-nolang>${dfr((D.emis||f.t||'').slice(0,10))}</span></div>`;
  /* Le document porte sa propre langue : la couche de traduction la lit sur
     data-lang et l'applique à cette zone, sans toucher au reste de l'écran. */
  try{
    const lg=D.langue||(typeof LANG!=='undefined'?LANG:'fr');
    const z=$('doc-corps');
    if(lg&&lg!=='fr') z.setAttribute('data-lang',lg); else z.setAttribute('data-lang','fr');
    if(typeof lgApplique==='function') lgApplique(z);
  }catch(e){}
  $('doc-paye').style.display=devis?'none':'';
  $('doc-paye').textContent = D.reste>0 ? (D.regle>0?'Encaisser le reste':'Encaisser') : 'Voir les paiements';
  $('doc-conv').style.display=(devis&&!D.converti&&!offre)?'':'none';
  { const bl=$('doc-lignes'); if(bl) bl.style.display=(devis&&typeof peutModifierDevis==='function'&&peutModifierDevis(f))?'':'none'; }
  $('docov').classList.add('on');
  docPagine();   /* la fenêtre doit être visible pour mesurer */
  /* la feuille se photographie tout de suite, en arrière-plan : quand on clique
     WhatsApp, Email ou Partager, le PDF est déjà prêt — et « Partager » DOIT
     répondre au clic sans attendre, sinon le téléphone refuse le partage */
  docPrepare(f);
}
/* ---------- LA MISE EN PAGES ----------
   5 nov. 2026 (Sam : « pas assez de marge en haut, trop de marge en bas ; si c'est sur deux pages il faut que ce soit bien
   découpé »). La feuille continue (#doc-corps) est mesurée hors écran à la largeur exacte d'une page Letter, puis découpée
   en pages : l'en-tête (société, client) sur la première ; les lignes du tableau l'une après l'autre, jamais coupées, avec
   l'en-tête du tableau répété en haut de chaque page ; les totaux, le paiement et le tampon ensemble, jamais séparés ;
   le pied de page en bas de CHAQUE page, avec « Page 1 / 2 ». Une page de suite porte un rappel « Facture PT-… — suite ». */
const PG_H=1056, PG_PAD_H=58, PG_PAD_B=46, PG_PIED_H=56;   /* px à 96 dpi : Letter = 816 × 1056 */
function docPagine(){
  const src=$('doc-corps'), out=$('doc-pages'); if(!src||!out) return;
  out.innerHTML='';
  /* 1. mesurer : une copie de la feuille, hors écran, à la largeur d'une page */
  const mes=document.createElement('div'); mes.className='doc pgmes'; mes.innerHTML=src.innerHTML; src.parentNode.appendChild(mes);
  const tete=mes.querySelector('.tete'), parties=mes.querySelector('.parties'), table=mes.querySelector('table'), thead=table&&table.querySelector('thead');
  const rows=table?[...table.querySelectorAll('tbody tr')]:[];
  const fin=['.totaux','.pay','.tampon'].map(k=>mes.querySelector(k)).filter(Boolean);
  const pied=mes.querySelector('.pied');
  const h=el=>el?el.getBoundingClientRect().height:0;
  const hTete=h(tete)+h(parties), hThead=h(thead)+4, hRows=rows.map(h), hFin=fin.reduce((a,e)=>a+h(e),0)+20+(fin.length-1)*8;
  const H=PG_H-PG_PAD_H-PG_PAD_B-PG_PIED_H;            /* la hauteur utile d'une page */
  const hSuite=52;
  /* 2. répartir */
  const pages=[]; let cur={items:[],y:0,rows:[]}; const neuve=()=>{ pages.push(cur); cur={items:[],y:hSuite,rows:[],suite:true}; };
  cur.y=hTete; cur.items.push('tete');
  let ouvert=false;
  rows.forEach((tr,i)=>{
    if(!ouvert){ if(cur.y+hThead+hRows[i]>H&&cur.rows.length===0&&cur.items.length&&cur.y>hSuite){ neuve(); } cur.y+=hThead; ouvert=true; }
    if(cur.y+hRows[i]>H&&cur.rows.length){ neuve(); cur.y+=hThead; }
    cur.rows.push(i); cur.y+=hRows[i];
  });
  if(cur.y+hFin>H&&(cur.rows.length||cur.items.length)){
    /* les totaux passent à la page suivante : la dernière ligne les accompagne, pour qu'une page ne porte jamais les totaux tout seuls */
    const der=cur.rows.length>1?cur.rows.pop():null; neuve();
    if(der!=null){ cur.y+=hThead+hRows[der]; cur.rows.push(der); } }
  cur.items.push('fin'); pages.push(cur);
  /* 3. dessiner les pages */
  const N=pages.length;
  const lbl=mes.querySelector('.titre h2'), num=mes.querySelector('.titre .num'), soc=mes.querySelector('.soc b');
  pages.forEach((pg,k)=>{
    const d=document.createElement('div'); d.className='doc pg'; d.setAttribute('data-lang',src.getAttribute('data-lang')||'fr');
    if(pg.suite){ const su=document.createElement('div'); su.className='suite';
      su.innerHTML=`<b data-nolang>${soc?soc.textContent:''}</b><span><span class="lbl">${lbl?lbl.textContent:''}</span> <span data-nolang>${num?num.textContent:''}</span> — <span class="lbl">suite</span></span>`; d.appendChild(su); }
    if(pg.items.includes('tete')){ if(tete) d.appendChild(tete.cloneNode(true)); if(parties) d.appendChild(parties.cloneNode(true)); }
    if(pg.rows.length&&table){ const t=document.createElement('table'); if(thead) t.appendChild(thead.cloneNode(true)); const tb=document.createElement('tbody'); pg.rows.forEach(i=>tb.appendChild(rows[i].cloneNode(true))); t.appendChild(tb); d.appendChild(t); }
    if(pg.items.includes('fin')) fin.forEach(e=>d.appendChild(e.cloneNode(true)));
    const p=pied?pied.cloneNode(true):document.createElement('div'); p.className='pied';
    const texte=document.createElement('div'); while(p.firstChild) texte.appendChild(p.firstChild); p.appendChild(texte);
    const n=document.createElement('span'); n.className='pgnum'; n.innerHTML=`<span class="lbl">Page</span> <span data-nolang>${k+1} / ${N}</span>`; p.appendChild(n);
    d.appendChild(p); out.appendChild(d);
  });
  mes.remove();
  try{ if(typeof lgApplique==='function') lgApplique(out); }catch(e){}
}
var _PREP=null;   /* {f, html, canvas, pdf} du document ouvert */
function docPrepare(f){
  const p={f,html:$('doc-corps').innerHTML,pret:null}; _PREP=p;
  p.pret=(async()=>{ try{ if(location.protocol==='file:') return null;
      const c=await docCanvas(); if(_PREP!==p) return null; p.canvas=c; p.pdf=canvasPDF(c); return p; }
    catch(e){ return null; } })();
}
/* la version prête, si la feuille n'a pas changé depuis (une langue basculée
   entre-temps, par exemple) ; sinon on la refait */
async function docPret(f){
  if(_PREP && _PREP.f && f && _PREP.f.id===f.id && _PREP.html===$('doc-corps').innerHTML){ const p=await _PREP.pret; if(p && p.pdf) return p; }
  const c=await docCanvas(); return {f,canvas:c,pdf:canvasPDF(c)};
}
/* Le texte envoyé par WhatsApp ou par email est LU PAR LE CLIENT : il suit donc
   la langue du document, pas celle de l'écran. On traduit mot à mot avec le même
   dictionnaire — un texte brut n'a pas de balises, la couche de traduction de la
   page ne peut pas l'atteindre. */
/* Le message WhatsApp (et le texte copié) : écrit comme on l'écrirait à la main —
   bonjour, merci pour la demande, les lignes, le total en gras, le lien du PDF.
   WhatsApp met en gras ce qui est entre *étoiles*. */
function docTexte(f, lien){ return (typeof vf==='function')?vf(docTexte0(f,lien),(f.doc.langue||(typeof LANG!=='undefined'?LANG:'fr'))):docTexte0(f,lien); }
function docTexte0(f, lien){
  const D=f.doc, E=D.entete||factReg(), devis=D.type==='devis';
  const lg=D.langue||(typeof LANG!=='undefined'?LANG:'fr');
  const T=(fr)=>{ try{ const v=(typeof lgMot==='function')?lgMot(fr,lg):null; return v||fr; }catch(e){ return fr; } };
  const L=(f.lignes||[]).filter(l=>l.q).map(l=>`• ${docRef(l)} × ${l.q} — $${dus(nbSur(l.q)*nbSur(puDoc(l)))}`).join('\n');
  const salut=lg==='fr'?'Bonjour'+(f.tiers?' '+f.tiers:'')+',':lg==='es'?'Hola'+(f.tiers?' '+f.tiers:'')+',':'Hello'+(f.tiers?' '+f.tiers:'')+',';
  const intro=D.offre
    ?(lg==='fr'?'Voici notre offre de prix, valable 30 jours :':lg==='es'?'Aquí tiene nuestra oferta de precio, válida 30 días:':'Here is our price offer, valid for 30 days:')
    :devis
    ?(lg==='fr'?'Merci pour votre demande de cotation. Voici votre devis':lg==='es'?'Gracias por su solicitud de cotización. Aquí tiene su cotización':'Thank you for your quote request. Here is your quote')
    :(lg==='fr'?'Voici votre facture':lg==='es'?'Aquí tiene su factura':'Here is your invoice');
  const total=T('Total').toUpperCase()+' : $'+dus(D.total);
  return `${salut}\n\n${intro}${D.offre?'':` *${D.num}* (${dfr(f.d)}) :`}\n\n${L}\n\n`
    + `${T('Sous-total')} : $${dus(D.sousTotal)}`
    + `${D.remise?'\n'+T('Remise')+' : −$'+dus(D.remise):''}`
    + `${D.frais?'\n'+T('Frais carte')+' '+D.fraisPct+' % : $'+dus(D.frais):''}\n`
    + `${D.taux?T('Sales tax')+' '+D.taux+' % : $'+dus(D.taxe):T('Sales tax — exonéré')}\n`
    + `${D.port?T("Frais d'envoi")+' : $'+dus(D.port)+'\n':''}`
    + `*${total}*`
    + `${!devis&&D.reste>0?'\n'+T('Reste dû')+' : $'+dus(D.reste):''}`
    + `${((devis||D.reste>0)&&(D.pmode==='zelle'||D.pmode==='virement')&&E.zelle)?'\n'+T('Pour régler')+' : '+E.zelle:''}`
    + `${!devis&&D.reste<=0?'\n'+T('Payée')+' — '+T('merci !'):''}`
    + `\n\n${E.enseigne||E.raison}${E.tel?' · '+E.tel:''}`
    /* le lien seul, en dernière ligne, sans phrase autour : WhatsApp en fait une
       carte (titre + image du document) — c'est elle qu'on tape */
    + (lien?'\n\n'+lien:'');
}
$('doc-x').onclick=()=>{ $('docov').classList.remove('on'); DOC=null; };
$('docov').addEventListener('click',e=>{ if(e.target===$('docov')) $('doc-x').click(); });
/* La feuille sortait BLANCHE à l'impression, et le défaut n'était pas dans la
   feuille : la règle d'impression cache tous les enfants directs du body puis
   rallume la feuille. Or depuis que la page a une charpente (body > .app >
   .main > .wrap), la feuille n'est plus un enfant du body — c'est .app qui
   était caché, et rallumer un élément dont l'ancêtre est caché ne le rallume
   pas. On sort donc la feuille au niveau du body le temps de l'impression, et
   on la remet exactement où elle était. Ça vaut aussi pour la charpente de
   demain : plus rien ne dépend de la profondeur où vit la feuille. */
$('doc-print').onclick=()=>{
  const ov=$('docov'), pere=ov.parentNode, apres=ov.nextSibling;
  if(pere!==document.body) document.body.appendChild(ov);
  document.body.classList.add('impr-doc');
  const fin=()=>{ document.body.classList.remove('impr-doc');
    if(pere && ov.parentNode!==pere) pere.insertBefore(ov,apres); };
  window.addEventListener('afterprint',fin,{once:true});
  setTimeout(()=>{ window.print(); setTimeout(fin,1500); },50); };
$('doc-copie').onclick=async()=>{ try{ await navigator.clipboard.writeText(docTexte(DOC)); $('doc-copie').textContent='Copié ✓'; setTimeout(()=>$('doc-copie').textContent='Copier le texte',1800); }catch(e){ prompt('Copie ce texte :',docTexte(DOC)); } };
/* ---------- LE PDF QUI PART CHEZ LE CLIENT ----------
   Un lien WhatsApp ou un mailto ne transporte que du texte : impossible d'y
   accrocher un fichier. Alors la feuille est dessinée en PDF ici, dans le
   navigateur (la page telle qu'on la voit, photographiée à haute résolution),
   déposée au cockpit, et c'est SON ADRESSE qui part dans le message : le client
   tape dessus, le devis s'ouvre en plein écran. L'adresse est unique par numéro
   de document : un devis corrigé et renvoyé garde le même lien, à jour.
   Sans serveur (fichier ouvert en local, ou coupure) : le texte part seul, et
   le PDF se télécharge pour être joint à la main. */
async function _pdfLibs(){
  if(window.html2canvas && window.jspdf) return;
  if(location.protocol==='file:') throw new Error("Le PDF se fabrique sur la version en ligne de l'outil.");
  const charge=src=>new Promise((res,rej)=>{ const sc=document.createElement('script'); sc.src=src; sc.onload=res;
    sc.onerror=()=>rej(new Error('Moteur PDF introuvable ('+src+')')); document.head.appendChild(sc); });
  if(!window.html2canvas) await charge('lib/pdf/html2canvas.min.js');
  if(!window.jspdf) await charge('lib/pdf/jspdf.umd.min.js');
}
/* la feuille photographiée une fois ; le PDF et l'aperçu en sortent tous les deux */
/* 5 nov. 2026 : chaque page de l'écran est photographiée entière — plus de découpe au ciseau dans une feuille continue */
/* 7 nov. 2026 (Sam, deux documents aux mots entassés les uns sur les autres : « Thecollectionperfumes », « PaymentCheck ») :
   sur une fenêtre de moins de 900 px — le portable de Sam — la feuille est réduite à 72 % à l'écran (transform:scale). Le
   photographe mesure chaque mot sur la feuille réduite, mais le dessine en taille réelle : les mots se chevauchent. Le temps
   de la photo, la feuille repasse à 100 % ; l'écran la retrouve réduite juste après. */
async function docCanvas(){
  await _pdfLibs();
  let pages=[...document.querySelectorAll('#doc-pages .doc.pg')];
  if(!pages.length){ docPagine(); pages=[...document.querySelectorAll('#doc-pages .doc.pg')]; }
  const out=[], P=document.querySelector('#doc-pages'), ov=document.getElementById('docov');
  const avant=P?P.style.transform:''; if(P) P.style.transform='none';
  const ovAvant=ov?ov.style.overflow:''; if(ov) ov.style.overflow='visible';
  try{
    for(const el of pages) out.push(await window.html2canvas(el,{scale:2,backgroundColor:'#ffffff',useCORS:true,logging:false,width:816,height:1056,windowWidth:900}));
  } finally { if(P) P.style.transform=avant; if(ov) ov.style.overflow=ovAvant; }
  return out;
}
function canvasPDF(cs){
  const {jsPDF}=window.jspdf;
  const pdf=new jsPDF({unit:'pt',format:'letter',orientation:'portrait',compress:true});
  const W=pdf.internal.pageSize.getWidth(), H=pdf.internal.pageSize.getHeight();
  (Array.isArray(cs)?cs:[cs]).forEach((c,n)=>{ if(n) pdf.addPage(); pdf.addImage(c.toDataURL('image/jpeg',0.92),'JPEG',0,0,W,H); });
  return pdf.output('blob');
}
/* l'aperçu : la première page, réduite à 1000 px de large — assez pour être lue
   sur un téléphone, assez léger pour la carte WhatsApp */
function canvasPNG(cs){
  const c=Array.isArray(cs)?cs[0]:cs;
  const w=1000, ratio=w/c.width, h=Math.min(c.height*ratio, 1300);
  const p=document.createElement('canvas'); p.width=w; p.height=Math.round(h);
  p.getContext('2d').drawImage(c,0,0,c.width,h/ratio,0,0,w,h);
  return new Promise(r=>p.toBlob(r,'image/png'));
}
async function docPDF(){ return (await docPret(DOC)).pdf; }
const docNomPDF=f=>((f.doc.offre?offreMot(f.doc):f.doc.type==='devis'?((typeof vf==='function')?vf('Devis',f.doc.langue||LANG):'Devis'):'Facture')+'-')+String(f.doc.num).replace(/[^A-Za-z0-9._-]/g,'')+'.pdf';
/* le lien public du document : déposé une fois, réutilisé ensuite */
async function docLien(f){
  if(typeof CK_URL==='undefined' || typeof ckTok!=='function' || !ckTok()) throw new Error("Pas de session serveur : le texte part sans le PDF.");
  const pr=await docPret(f); const c=pr.canvas, blob=pr.pdf; const D=f.doc, E=enteteVue(f.doc);
  const q='?type='+(D.offre?'offre':(D.type||'devis'))+'&enseigne='+encodeURIComponent(E.enseigne||E.raison||'')+'&date='+encodeURIComponent(dfr(f.d))
    +'&total='+encodeURIComponent('$'+dus(D.total))+'&lignes='+((f.lignes||[]).filter(l=>l.q).length)+'&langue='+(D.langue||(typeof LANG!=='undefined'?LANG:'fr'));
  let r;
  try{ r=await fetch(CK_URL+'/api/o/'+CK_ORG+'/docs/'+encodeURIComponent(D.num)+q,
        {method:'PUT',headers:{'Content-Type':'application/pdf',Authorization:'Bearer '+ckTok()},body:blob}); }
  catch(e){ throw new Error("Le serveur ne répond pas : le texte part sans le PDF."); }
  const j=await r.json().catch(()=>({}));
  if(!r.ok) throw new Error(j.erreur||('Dépôt du PDF refusé ('+r.status+')'));
  /* l'aperçu, pour la page et la carte WhatsApp : s'il échoue, le lien marche quand même */
  try{ const png=await canvasPNG(c); await fetch(CK_URL+'/api/o/'+CK_ORG+'/docs/'+encodeURIComponent(D.num)+'/image',
      {method:'PUT',headers:{'Content-Type':'image/png',Authorization:'Bearer '+ckTok()},body:png}); }catch(e){}
  docMaj(f,x=>{ x.doc.lien=j.url; x.doc.pdf=j.pdf||''; });
  return j.url;
}
const docEtat=(t,err)=>{ const e=$('doc-etat'); if(!e) return; e.textContent=t||''; e.style.color=err?'#ffb4a8':''; };
/* le texte + le lien : ce que reçoit le client */
async function docEnvoiTexte(f){
  docEtat('Fabrication du PDF…');
  let lien='';
  try{ lien=await docLien(f); docEtat(''); }
  catch(e){ docEtat(e.message,true); }
  return docTexte(f, lien);
}
/* WhatsApp. Deux pièges, corrigés le 9 oct. 2026 (Igal : « whatsapp ne fonctionne pas quand
   je veux envoyer une quote ») :
   1. le navigateur ne laisse ouvrir un onglet qu'au moment du clic ; ici l'onglet s'ouvrait
      APRÈS la fabrication du PDF (plusieurs secondes) et Chrome le bloquait en silence.
      On ouvre donc l'onglet tout de suite, vide, et on lui donne l'adresse ensuite ; s'il est
      quand même bloqué, un bouton « Ouvrir WhatsApp » apparaît (nouveau clic = permis).
   2. un client sans téléphone sur sa fiche partait vers « wa.me/ » sans destinataire, et un
      numéro à 10 chiffres sans le 1 ne menait nulle part. Maintenant : le numéro est
      normalisé, et s'il manque, on le demande et on le garde sur la fiche. */
function waNum(v){
  let d=String(v||'').replace(/\D/g,''); if(!d) return '';
  if(d.length===10) d='1'+d;
  return (d.length>=8&&d.length<=15)?d:'';
}
function retientTel(nom,tel){
  if(!nom||!tel) return;
  try{ const CLI=lit(KCLI,{}); const c=CLI[nom]||{nom}; if(c.tel===tel) return; c.tel=tel; c.maj=new Date().toISOString(); CLI[nom]=c; ecrit(KCLI,CLI); }catch(e){}
}
async function waEnvoi(f,num){
  const w=window.open('','_blank');
  try{ if(w&&w.document) w.document.write('<title>WhatsApp</title><body style="font:16px system-ui;padding:40px;color:#444">Préparation du message…</body>'); }catch(e){}
  $('doc-wa').disabled=true; const txt=await docEnvoiTexte(f); $('doc-wa').disabled=false;
  const url='https://wa.me/'+num+'?text='+encodeURIComponent(txt);
  window.__wa=url;                          /* point d'observation pour les tests */
  let ok=false;
  try{ if(w&&!w.closed){ w.location.href=url; ok=true; } }catch(e){}
  if(!ok){
    let b=$('doc-wa2'); if(!b){ b=document.createElement('button'); b.id='doc-wa2'; b.className='btn pri'; $('doc-wa').after(b); }
    b.textContent='Ouvrir WhatsApp'; b.style.display='';
    b.onclick=()=>{ window.open(url,'_blank'); b.style.display='none'; docEtat(''); };
    docEtat('Le navigateur a bloqué la fenêtre : clique sur « Ouvrir WhatsApp ».',true);
  }
}
$('doc-wa').onclick=()=>{ const f=DOC; if(!f) return; const num=waNum(coordTiers(f.tiers).tel);
  if(num) return waEnvoi(f,num);
  $('wa-a').value=''; $('wa-etat').textContent=''; $('waov').classList.add('on'); setTimeout(()=>$('wa-a').focus(),50); };
$('wa-ann').onclick=()=>$('waov').classList.remove('on');
$('waov').addEventListener('click',e=>{ if(e.target===$('waov')) $('wa-ann').click(); });
$('wa-ok').onclick=()=>{ const f=DOC; if(!f) return; const num=waNum($('wa-a').value);
  if(!num){ $('wa-etat').textContent="Numéro illisible. Exemple : 305 555 0100 ou +33 6 12 34 56 78."; $('wa-a').focus(); return; }
  retientTel(f.tiers,$('wa-a').value.trim()); $('waov').classList.remove('on'); waEnvoi(f,num); };
$('wa-a').addEventListener('keydown',e=>{ if(e.key==='Enter') $('wa-ok').click(); });
/* l'email et le téléphone du client : la fiche Clients d'abord, puis Retail,
   puis la liste du site — un nom peut n'avoir ses coordonnées qu'à un seul endroit */
function coordTiers(nom){
  const k=String(nom||'').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g,'').trim(); if(!k) return {};
  const out={};
  const prend=o=>{ if(!o) return; if(!out.email&&o.email) out.email=String(o.email).trim(); if(!out.tel&&o.tel) out.tel=String(o.tel).trim(); };
  try{ const CLI=lit(KCLI,{}); prend(CLI[nom]); for(const n in CLI){ if(n.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g,'').trim()===k) prend(CLI[n]); } }catch(e){}
  try{ const t=localStorage.getItem('retail-local-v1'); const R=t?JSON.parse(t):(window.D_RETAIL||[]);
       (Array.isArray(R)?R:[]).forEach(c=>{ if(String(c.nom||'').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g,'').trim()===k) prend(c); }); }catch(e){}
  try{ ((window.D_CLI||{}).clients||[]).forEach(c=>{ if(String(c.nom||'').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g,'').trim()===k) prend(c); }); }catch(e){}
  return out;
}
/* une adresse tapée dans la fenêtre d'envoi est gardée sur la fiche : la fois d'après, elle est déjà là */
function retientEmail(nom,email){
  if(!nom||!email) return;
  try{ const CLI=lit(KCLI,{}); const c=CLI[nom]||{nom}; if(c.email===email) return; c.email=email; c.maj=new Date().toISOString(); CLI[nom]=c; ecrit(KCLI,CLI); }catch(e){}
}
/* ---- l'envoi par email ----
   Deux chemins. Si la boîte de l'entreprise est réglée dans le cockpit, le
   courrier part d'ici : la feuille en image dans le corps, le PDF joint, au nom
   de l'entreprise. Sinon (pas de boîte, hors ligne) : le logiciel de courrier
   de la personne s'ouvre avec le texte et le lien du PDF — c'est tout ce qu'un
   « mailto » sait faire. */
let _boite=null;
async function boiteEnvoi(){
  if(_boite) return _boite;
  if(typeof CK_URL==='undefined'||typeof ckTok!=='function'||!ckTok()) return (_boite={pret:false});
  try{ const r=await fetch(CK_URL+'/api/o/'+CK_ORG+'/courrier/etat',{headers:{Authorization:'Bearer '+ckTok()}}); _boite=r.ok?await r.json():{pret:false}; }
  catch(e){ _boite={pret:false}; }
  return _boite;
}
function docSujet(f){ const D=f.doc, E0=enteteVue(D); if(D.offre) return offreMot(D)+' '+D.num+' — '+(E0.enseigne||E0.raison); const t=(D.type==='devis'?'Devis ':'Facture ')+D.num+' — '+(E0.enseigne||E0.raison); return (typeof vf==='function')?vf(t,D.langue||LANG):t; }
function docMotCourrier(f){ const t=docMotCourrier0(f); return (typeof vf==='function')?vf(t,f.doc.langue||LANG):t; }
function docMotCourrier0(f){
  const D=f.doc, E=enteteVue(D), devis=D.type==='devis';
  const lg=D.langue||(typeof LANG!=='undefined'?LANG:'fr');
  if(D.offre){ const c=lg==='fr'?'Bonjour,\n\nVoici notre offre de prix, valable 30 jours. Veuillez trouver le document ci-joint.':lg==='es'?'Hola,\n\nAquí tiene nuestra oferta de precio, válida 30 días. Adjunto encontrará el documento.':'Hello,\n\nHere is our price offer, valid for 30 days. Please find the document attached.';
    return c+'\n\n'+(lg==='fr'?'Merci,':lg==='es'?'Gracias,':'Thank you,')+'\n'+(E.enseigne||E.raison)+(E.tel?' · '+E.tel:''); }
  const corps=lg==='fr'?(devis?'Bonjour,\n\nMerci pour votre demande de cotation. Veuillez trouver ci-joint le devis.':'Bonjour,\n\nVeuillez trouver ci-joint votre facture.')
    :lg==='es'?(devis?'Hola,\n\nGracias por su solicitud de cotización. Adjunto encontrará la cotización.':'Hola,\n\nAdjunto encontrará su factura.')
    :(devis?'Hello,\n\nThank you for your quote request. Please find the quote attached.':'Hello,\n\nPlease find your invoice attached.');
  const merci=lg==='fr'?'Merci,':lg==='es'?'Gracias,':'Thank you,';
  return corps+'\n\n'+merci+'\n'+(E.enseigne||E.raison)+(E.tel?' · '+E.tel:'');
}
$('doc-mail').onclick=async()=>{ const f=DOC; const co=coordTiers(f.tiers);
  $('doc-mail').disabled=true; const b=await boiteEnvoi(); $('doc-mail').disabled=false; if(!DOC||DOC.id!==f.id) return;
  if(!b.pret){
    /* Pas de boîte réglée : le logiciel de courrier de la personne s'ouvre avec le
       texte, SANS le lien du cockpit — une adresse en cockpit.igalbotbol.com n'a
       rien à faire dans un e-mail au nom de l'enseigne. Le PDF se télécharge à la
       place : il ne reste qu'à le glisser dans le message avant d'envoyer.
       Igal, 12 sept. 2026, en collant l'adresse d'un document : « enlever ça des
       emails ». WhatsApp, lui, garde le lien : sans lui, pas de carte ni de PDF du tout. */
    docEtat('Fabrication du PDF…');
    try{ const pdf=await docPDF(); if(!DOC||DOC.id!==f.id) return;
      const a=document.createElement('a'); a.href=URL.createObjectURL(pdf); a.download=docNomPDF(f); a.click();
      setTimeout(()=>URL.revokeObjectURL(a.href),4000);
      docEtat('');
    }catch(e){ docEtat(e.message,true); }
    const txt=docTexte(f); if(!DOC||DOC.id!==f.id) return;
    const lien='mailto:'+encodeURIComponent(co.email||'')+'?subject='+encodeURIComponent(docSujet(f))+'&body='+encodeURIComponent(txt);
    window.__mailto=lien;                 /* point d'observation pour les tests */
    location.href=lien; return; }
  $('mail-a').value=co.email||''; $('mail-sujet').value=docSujet(f); $('mail-txt').value=docMotCourrier(f); $('mail-de').textContent=b.de||'';
  $('mail-etat').textContent=co.email?'':'Pas d\'adresse sur la fiche de ce client : tape-la, elle sera gardée.';
  $('mailov').classList.add('on'); setTimeout(()=>$(co.email?'mail-txt':'mail-a').focus(),50); };
$('mail-ann').onclick=()=>$('mailov').classList.remove('on');
$('mailov').addEventListener('click',e=>{ if(e.target===$('mailov')) $('mail-ann').click(); });
$('mail-ok').onclick=async()=>{
  const f=DOC; if(!f) return; const a=$('mail-a').value.trim();
  if(!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(a)){ $('mail-etat').textContent='L\'adresse n\'est pas valable.'; $('mail-a').focus(); return; }
  $('mail-ok').disabled=true;
  try{
    $('mail-etat').textContent='Fabrication du PDF…';
    await docLien(f);
    $('mail-etat').textContent='Envoi…';
    const r=await fetch(CK_URL+'/api/o/'+CK_ORG+'/docs/'+encodeURIComponent(f.doc.num)+'/courrier',
      {method:'POST',headers:{'Content-Type':'application/json',Authorization:'Bearer '+ckTok()},
       body:JSON.stringify({a,sujet:$('mail-sujet').value.trim(),texte:$('mail-txt').value})});
    const j=await r.json().catch(()=>({}));
    if(!r.ok) throw new Error(j.erreur||('Envoi refusé ('+r.status+')'));
    retientEmail(f.tiers,a);
    docMaj(f,x=>{ x.doc.envoye=(x.doc.envoye||[]).concat([{a,t:new Date().toISOString()}]); });
    $('mailov').classList.remove('on'); docEtat('Envoyé à '+a+' ✓');
  }catch(e){ $('mail-etat').textContent=e.message; }
  $('mail-ok').disabled=false;
};
$('doc-pdf').onclick=async()=>{ const f=DOC; docEtat('Fabrication du PDF…'); $('doc-pdf').disabled=true;
  try{ const b=await docPDF(); const a=document.createElement('a'); a.href=URL.createObjectURL(b); a.download=docNomPDF(f); a.click();
       setTimeout(()=>URL.revokeObjectURL(a.href),4000); docEtat(''); }
  catch(e){ docEtat(e.message,true); }
  $('doc-pdf').disabled=false; };
/* le partage natif (téléphone, Mac) : le PDF lui-même part dans WhatsApp, Mail, AirDrop… */
/* Sur un téléphone ou une tablette, c'est LE bon bouton : le PDF lui-même part
   dans WhatsApp, Mail, AirDrop. Sur un Mac ou un PC, la feuille de partage du
   système ne propose pas WhatsApp et Chrome la gère mal — on ne montre pas un
   bouton qui décevrait. */
const SUR_MOBILE=/Android|iPhone|iPad|iPod|Mobile/i.test(navigator.userAgent)||(navigator.userAgentData&&navigator.userAgentData.mobile)||(navigator.maxTouchPoints>1&&/Macintosh/.test(navigator.userAgent));
(function(){ try{ if(SUR_MOBILE && navigator.share && navigator.canShare && navigator.canShare({files:[new File(['x'],'x.pdf',{type:'application/pdf'})]})) $('doc-part').style.display=''; }catch(e){} })();
var _partage=false;
$('doc-part').onclick=async()=>{ const f=DOC; if(_partage) return; _partage=true;
  try{
    /* le PDF est prêt d'avance (docPrepare) : le partage part dans la foulée du clic */
    const pr=await docPret(f); const file=new File([pr.pdf],docNomPDF(f),{type:'application/pdf'}); docEtat('');
    await navigator.share({files:[file],title:docNomPDF(f).replace('.pdf',''),text:docTexte(f)}); }
  catch(e){ if(e&&e.name!=='AbortError') docEtat(e.name==='NotAllowedError'?'Le téléphone veut un clic direct : réessaie une fois le PDF prêt.':e.message,true); }
  _partage=false; };
/* ============ ENCAISSER ============
   Un gros client paie rarement d'un coup : un acompte a la commande, le solde a la
   livraison, parfois trois versements. « Marquer payee » ne savait dire que « tout
   est regle » — ce qui obligeait a mentir sur les factures reglees en plusieurs fois.
   Ici chaque versement est enregistre avec sa date, son mode et sa reference ; le
   reste du se recalcule tout seul, et la facture passe payee quand il tombe a zero.
   Les versements vivent dans f.doc.regs : les anciennes factures, qui n'en ont pas,
   gardent leur montant regle comme premier versement. */
function encRegs(f){
  const D=f.doc||{};
  if(Array.isArray(D.regs)) return D.regs;
  /* facture d'avant : on reconstitue un versement a partir de ce qui etait note */
  if((+D.regle||0)>0) return [{mt:+D.regle,m:D.pmode||'zelle',d:D.payeLe||f.d||'',ref:'',
                               u:f.par||'',t:D.emis||f.t||'',repris:true}];
  return [];
}
function encTotal(f){ return Math.round(encRegs(f).reduce((a,r)=>a+(+r.mt||0),0)*100)/100; }
function encMaj(f){
  const D=f.doc; const regs=encRegs(f);
  D.regs=regs;
  D.regle=encTotal(f);
  D.reste=Math.max(0,Math.round((D.total-D.regle)*100)/100);
  D.pstat = D.reste<=0 ? 'paye' : (D.regle>0?'partiel':'apayer');
  if(regs.length) D.pmode=regs[regs.length-1].m||D.pmode;
  D.payeLe = D.reste<=0 && regs.length ? (regs[regs.length-1].d||ajd()) : undefined;
}
let ENC=null;
function encOuvre(f){
  if(!f||!f.doc) return;
  ENC=f; encMaj(f);
  $('enc-d').value=ajd();
  $('enc-mode').value=f.doc.pmode||'zelle';
  $('enc-ref').value='';
  $('enc-mt').value= f.doc.reste>0 ? String(f.doc.reste) : '';
  $('enc-msg').textContent='';
  encPeint();
  $('encov').classList.add('on');
  setTimeout(()=>$('enc-mt').focus(),60);
}
function encPeint(){
  const f=ENC; if(!f) return;
  const D=f.doc, regs=encRegs(f);
  $('enc-res').innerHTML=`
    <div><span class="v">$${dus(D.total)}</span><span class="k">total de la facture</span></div>
    <div><span class="v" style="color:var(--good)">$${dus(D.regle)}</span><span class="k">déjà reçu</span></div>
    <div><span class="v" style="color:${D.reste>0?'var(--crit)':'var(--ink-3)'}">$${dus(D.reste)}</span><span class="k">reste dû</span></div>`;
  $('enc-hist').innerHTML = regs.length ? `<div class="enchist"><table>
      <thead><tr><th>Date</th><th>Mode</th><th>Référence</th><th class="r">Montant</th><th></th></tr></thead>
      <tbody>${regs.map((r,i)=>`<tr><td>${dfr(r.d)||'—'}</td><td>${esc(FMODES[r.m]||r.m||'—')}</td>
        <td>${esc(r.ref||'')}${r.repris?'<small style="color:var(--ink-3)"> repris de l\'ancienne saisie</small>':''}</td>
        <td class="r">$${dus(r.mt)}</td>
        <td class="r"><button class="sup" data-reg="${i}" title="Retirer ce versement">retirer</button></td></tr>`).join('')}
      </tbody></table></div>` : '';
  const v=Math.round((+$('enc-mt').value||0)*100)/100;
  const apres=Math.round((D.reste-v)*100)/100;
  const rap=$('enc-rap');
  if(!(v>0)){ rap.innerHTML = D.reste>0
      ? `Indique le montant reçu. Le reste dû passera de <b>$${dus(D.reste)}</b> à ce qu'il restera.`
      : `Cette facture est <b>réglée en totalité</b>. Tu peux quand même corriger un versement ci-dessus.`;
    $('enc-ok').disabled=true; }
  else { rap.innerHTML = apres<=0
      ? `Après ce versement de <b>$${dus(v)}</b>, la facture est <b>réglée en totalité</b>.${apres<0?` Le client verse <b>$${dus(-apres)}</b> de plus que le total — vérifie le montant.`:''}`
      : `Après ce versement de <b>$${dus(v)}</b>, il restera <b>$${dus(apres)}</b> à encaisser.`;
    $('enc-ok').disabled=false; }
  /* raccourcis : la moitié, le tiers, tout */
  $('enc-v').innerHTML = D.reste>0 ? [['Tout le reste',D.reste],['La moitié',Math.round(D.reste/2*100)/100],
      ['Un tiers',Math.round(D.reste/3*100)/100]].map(([l,m])=>`<button type="button" data-v="${m}">${l} · $${dus(m)}</button>`).join('') : '';
  $('enc-v').querySelectorAll('[data-v]').forEach(b=>b.onclick=()=>{ $('enc-mt').value=b.dataset.v; encPeint(); });
  $('enc-hist').querySelectorAll('[data-reg]').forEach(b=>b.onclick=()=>{
    const i=+b.dataset.reg; const r=encRegs(f)[i];
    if(!confirm('Retirer le versement de $'+dus(r.mt)+' du '+(dfr(r.d)||'?')+' ?\n\nLe reste dû remontera d\'autant.')) return;
    if(!signe("retirer un versement",()=>{})) return;
    f.doc.regs=encRegs(f).filter((_,j)=>j!==i); encMaj(f); ecrit(KFACT,FACT);
    const JOU=lit(KJOU,[]);
    JOU.push({t:new Date().toISOString(),u:USR||'(non renseigné)',act:'annulation',
      lib:'versement retiré sur la facture '+f.doc.num+' — $'+dus(r.mt),ref:f.tiers||'',
      av:'reste $'+dus(Math.max(0,f.doc.reste-r.mt)),ap:'reste $'+dus(f.doc.reste)});
    ecrit(KJOU,JOU);
    encPeint(); dessineDoc(f); peintDocs();
  });
}
['enc-mt','enc-mode'].forEach(i=>$(i).addEventListener('input',encPeint));
$('enc-x').onclick=$('enc-ann').onclick=()=>{ $('encov').classList.remove('on'); ENC=null; };
$('encov').addEventListener('click',e=>{ if(e.target===$('encov')) $('enc-x').click(); });
$('enc-ok').onclick=()=>{
  const f=ENC; if(!f||!f.doc) return;
  const mt=Math.round((+$('enc-mt').value||0)*100)/100;
  if(!(mt>0)){ $('enc-msg').textContent='Indique un montant.'; return; }
  if(!signe("ce paiement",()=>$('enc-ok').click())) return;
  const avant=f.doc.reste;
  const r={mt,m:$('enc-mode').value,d:$('enc-d').value||ajd(),
           ref:$('enc-ref').value.trim(),u:USR||'(non renseigné)',t:new Date().toISOString()};
  f.doc.regs=encRegs(f).concat([r]);
  encMaj(f); ecrit(KFACT,FACT);
  const JOU=lit(KJOU,[]);
  JOU.push({t:new Date().toISOString(),u:USR||'(non renseigné)',act:'vente',
    lib:'paiement reçu sur la facture '+f.doc.num+' — $'+dus(mt)+' en '+(FMODES[r.m]||r.m)
        +(f.doc.reste<=0?' — facture réglée':'')+(r.ref?' ('+r.ref+')':''),
    ref:f.tiers||'',av:'reste $'+dus(avant),ap:'reste $'+dus(f.doc.reste)});
  ecrit(KJOU,JOU);
  $('enc-mt').value=''; $('enc-ref').value='';
  encPeint(); dessineDoc(f); peintDocs();
  if(f.doc.reste<=0){ $('encov').classList.remove('on'); ENC=null; }
  else $('enc-msg').textContent='paiement enregistré';
};
$('doc-paye').onclick=()=>{ if(DOC) encOuvre(DOC); };
/* ---- modifier un document émis : l'en-tête, pas les lignes ---- */
$('doc-edit').onclick=()=>{ const f=DOC; if(!f||!f.doc) return; const D=f.doc;
  $('ed-tiers').value=f.tiers||''; $('ed-date').value=(f.d||'').slice(0,10); $('ed-pmode').value=D.pmode||'zelle';
  $('ed-langue').value=D.langue||'fr'; $('ed-fiscal').value=D.fiscal||'taxable'; $('ed-fref').value=D.fref||''; $('ed-note').value=D.note||'';
  $('ed-msg').textContent=''; $('edov').classList.add('on'); };
$('ed-x').onclick=$('ed-ann').onclick=()=>$('edov').classList.remove('on');
$('ed-ok').onclick=()=>{ const f=DOC; if(!f||!f.doc) return;
  const tiers=$('ed-tiers').value.trim(); if(!tiers){ $('ed-msg').textContent='il faut un nom de client'; return; }
  const avant={tiers:f.tiers,d:f.d,pmode:f.doc.pmode,fiscal:f.doc.fiscal,total:f.doc.total};
  const g=docMaj(f,x=>{ const D=x.doc; x.tiers=tiers; if($('ed-date').value) x.d=$('ed-date').value;
    D.pmode=$('ed-pmode').value; D.langue=$('ed-langue').value; D.fiscal=$('ed-fiscal').value; D.fref=$('ed-fref').value.trim(); D.note=$('ed-note').value.trim()||undefined;
    /* la taxe et les frais suivent le nouveau statut ; ce qui a été réglé ne change pas */
    const o={pmode:D.pmode,fiscal:D.fiscal,remType:D.remType,remVal:D.remVal,remLib:D.remLib,frais:D.fraisPct,taux:D.auto?0:D.taux,port:D.port,
      pstat:(D.reste||0)<=0?'paye':((+D.regle||0)>0?'partiel':'apayer'),regle:D.regle};
    if(D.type!=='devis'){ const c=calcDoc(x.lignes||[],o); const regle=+D.regle||0; Object.assign(D,c,{regle,reste:Math.max(0,Math.round((c.total-regle)*100)/100)}); D.pstat=D.reste<=0?'paye':(regle>0?'partiel':'apayer'); }
    else Object.assign(D,calcDoc(x.lignes||[],Object.assign(o,{pstat:'apayer'})));
    x.montant=D.type==='devis'?x.montant:D.total; });
  try{ if(typeof CLI!=='undefined'&&CLI&&tiers){ CLI[tiers]=Object.assign({nom:tiers},CLI[tiers]||{},{fiscal:g.doc.fiscal,fiscalRef:g.doc.fref,pmode:g.doc.pmode,langue:g.doc.langue}); ecrit(KCLI,CLI); } }catch(e){}
  try{ const J=lit(KJOU,[]); J.push({t:new Date().toISOString(),u:USR||'(non renseigné)',act:'vente',lib:(g.doc.type==='devis'?'devis ':'facture ')+g.doc.num+' modifié'+(g.doc.type==='devis'?'':'e')+' — '+tiers,ref:g.id,av:avant.tiers+' · '+(FMODES[avant.pmode]||avant.pmode)+' · '+money2(avant.total),ap:tiers+' · '+(FMODES[g.doc.pmode]||g.doc.pmode)+' · '+money2(g.doc.total)}); ecrit(KJOU,J); }catch(e){}
  $('edov').classList.remove('on'); dessineDoc(g); try{ if(typeof peintDocs==='function') peintDocs(); }catch(e){} };
/* un devis accepté devient une facture : nouveau numéro, et cette fois le stock sort */
$('doc-conv').onclick=()=>{
  const f=DOC; if(!f||!f.doc||f.doc.type!=='devis'||f.doc.converti||f.doc.offre) return;
  if(!confirm(vf('Transformer le devis '+f.doc.num+' en facture ? Les quantités sortiront du stock.'))) return;
  const d=ajd(), JOU=lit(KJOU,[]), VENT=lit(KVENT,{});
  const lignes=[], det=[]; let sortis=0;
  (f.lignes||[]).forEach(l=>{ const qAv=qteEff(l.cle), qAp=Math.max(0,qAv-(l.q||0));
    lignes.push(Object.assign({cle:l.cle,bc:l.bc,ref:l.ref,q:l.q,p:l.p,qAv,qAp,manque:Math.max(0,(l.q||0)-qAv),paAv:paEff(l.cle)},
      l.remise&&l.pAv!=null?{pAv:l.pAv,remise:true}:{}));
    if(qAp!==qAv){ MOD[l.cle]=Object.assign({},MOD[l.cle]||{},{qte:qAp}); det.push({bc:l.bc,ref:l.ref,av:qAv,ap:qAp}); sortis+=qAv-qAp; }
    (VENT[l.cle]=VENT[l.cle]||[]).push({d,h:heureMiami(),p:l.p,c:f.tiers||'',q:l.q,num:'',k:f.canal}); });
  const num=numAuto(d);
  const doc=Object.assign({},f.doc,{type:'facture',num:docNum('facture',d),pstat:'apayer',emis:new Date().toISOString(),deDevis:f.doc.num});
  Object.assign(doc,calcDoc(lignes,doc));
  const f2={id:'v'+Date.now().toString(36),num,sens:'vente',canal:f.canal,tiers:f.tiers,d,h:heureMiami(),lignes,montant:Math.round(lignes.reduce((a,l)=>a+(+l.q||0)*(+l.p||0),0)*100)/100,stock:true,manuel:true,par:USR||'(non renseigné)',t:new Date().toISOString(),doc};
  docMaj(f,x=>{ x.doc.converti=f2.id; x.doc.convertiNum=doc.num; });
  FACT.push(f2); noteRang(num,d);
  ecrit(KFACT,FACT); ecrit(KMOD,MOD); ecrit(KVENT,VENT);
  JOU.push({t:new Date().toISOString(),u:USR||'(non renseigné)',act:'vente',lib:'devis '+f.doc.num+' transformé en facture '+doc.num+(f.tiers?' — '+f.tiers:''),n:det.length,impact:-Math.round(doc.sousTotal),det});
  ecrit(KJOU,JOU);
  construitV(); vus=80; dessine(); peintDocs(); dessineDoc(f2);
};
/* ---- la liste ---- */
let DOCS_F='';
function peintDocs(){
  const L=FACT.filter(f=>f.doc&&!f.doc.offre&&(f.sens==='vente'||f.sens==='devis')).sort((a,b)=>(b.t||'').localeCompare(a.t||''));
  const du=L.filter(f=>docStatut(f)==='apayer'||docStatut(f)==='partiel');
  const totDu=du.reduce((a,f)=>a+(f.doc.reste||0),0);
  $('docs-em').textContent=L.length?`${nf(L.length)} document${L.length>1?'s':''}${du.length?` · ${du.length} à encaisser pour ${money2(totDu)}`:''}`:'aucun encore — coche « Facture » ou « Devis » en enregistrant une vente';
  const chips=[['','Tous'],['apayer','À encaisser'],['paye','Payées'],['devis','Devis']];
  $('docs-chips').innerHTML=L.length?chips.map(([v,l])=>`<button class="${DOCS_F===v?'on':''}" data-f="${v}">${l}</button>`).join(''):'';
  $('docs-chips').querySelectorAll('button').forEach(b=>b.onclick=()=>{ DOCS_F=b.dataset.f; peintDocs(); });
  const V=L.filter(f=>{ const s=docStatut(f); return !DOCS_F || (DOCS_F==='apayer'?(s==='apayer'||s==='partiel'):DOCS_F==='devis'?(s==='devis'||s==='converti'):s===DOCS_F); });
  $('docs-table').innerHTML=!L.length?'':!V.length?'<p class="ecr">Rien dans cette catégorie.</p>':`<table><thead><tr><th>N°</th><th>Date</th><th>Client</th><th>Paiement</th><th class="r">Total</th><th class="r">Reste dû</th><th>Par</th><th>État</th><th></th></tr></thead><tbody>
    ${V.slice(0,60).map(f=>{ const s=docStatut(f); return `<tr><td><b>${esc(f.doc.num)}</b></td><td>${dfr(f.d)}</td><td>${esc(f.tiers||'—')}</td><td>${esc(FMODES[f.doc.pmode]||'')}</td><td class="r">${money2(f.doc.total)}</td><td class="r">${f.doc.type==='devis'?'—':money2(f.doc.reste||0)}</td><td style="color:var(--ink-3);font-size:12px" data-nolang>${esc(f.par||'')}</td><td><span class="st ${s}">${FSTAT[s]||s}</span></td><td class="r"><button class="btn sm" data-doc="${esc(f.id)}">Voir</button></td></tr>`; }).join('')}</tbody></table>`;
  $('docs-table').querySelectorAll('[data-doc]').forEach(b=>b.onclick=()=>{ const f=FACT.find(x=>x.id===b.dataset.doc); if(f) dessineDoc(f); });
}
peintDocs();
"""
