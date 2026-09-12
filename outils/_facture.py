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
#mailov{position:fixed;inset:0;background:rgba(20,18,26,.55);z-index:9100;display:none;align-items:flex-start;justify-content:center;padding:60px 12px;overflow:auto}
#mailov.on{display:flex}
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

.doc .parties{display:grid;grid-template-columns:1fr 1fr;gap:38px;margin:30px 0 26px}
.doc .parties h4{margin:0 0 7px;font-size:9.5px;letter-spacing:.2em;text-transform:uppercase;
color:#8a8590;font-weight:700}
.doc .parties div{font-size:13px;color:#55525c;line-height:1.65}
.doc .parties div b{display:block;color:#16151a;font-size:14.5px;font-weight:600;margin-bottom:2px}

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
.doc .totaux .tt span{font-family:"Cormorant Garamond",Garamond,serif;font-size:22px;
font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:#16151a}
.doc .totaux .tt b{font-family:"Cormorant Garamond",Garamond,serif;font-size:26px;font-weight:600}
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
@media(max-width:640px){ .doc{padding:30px 22px} .doc .logo{max-width:150px;max-height:100px}
  .doc .tete{flex-direction:column;gap:18px} .doc .titre{text-align:left}
  .doc .parties{grid-template-columns:1fr;gap:20px} .doc .totaux{width:100%} }
/* ---- encaisser : un paiement a la fois, avec ce qui a deja ete recu ---- */
#encov{position:fixed;inset:0;background:rgba(20,18,26,.55);z-index:9200;display:none;
align-items:flex-start;justify-content:center;padding:32px 12px;overflow:auto}
#encov.on{display:flex}
#encov .mod{background:var(--surface);border:1px solid var(--line);border-radius:14px;
max-width:560px;width:100%;box-shadow:0 24px 70px rgba(0,0,0,.3)}
#encov .mh{display:flex;align-items:center;justify-content:space-between;padding:15px 18px;
border-bottom:1px solid var(--line)}
#encov .mh h3{margin:0;font-size:16px}
#encov .mh .x{background:none;border:0;font-size:20px;color:var(--ink-3);cursor:pointer;line-height:1}
#encov .mb{padding:16px 18px}
#encov .mf{display:flex;align-items:center;gap:8px;padding:13px 18px;border-top:1px solid var(--line)}
#encov .mf .msg{flex:1;font-size:12.5px;color:var(--ink-3)}
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
  body.impr-doc #docov{display:block !important;position:static;background:#fff;padding:0;overflow:visible}
  body.impr-doc .doctb{display:none !important}
  body.impr-doc .docw{max-width:none}
  body.impr-doc .doc{box-shadow:none;border-radius:0;padding:0}
  @page{margin:16mm}
}
"""

# S'insère dans la fenêtre « Enregistrer une vente », après la première grille de champs.
BLOC_VENTE = r"""
<div class="docbloc" id="v-docbloc">
  <div class="fg">
    <div class="fld"><label>Document pour le client</label>
      <select id="v-doc"><option value="">Aucun — simple vente</option><option value="facture">Facture</option><option value="devis">Devis (n'engage pas le stock)</option></select></div>
    <div class="fld"><label>Paiement</label>
      <select id="v-pmode"><option value="zelle">Zelle</option><option value="carte">Carte bancaire (frais en plus)</option><option value="especes">Espèces</option><option value="virement">Virement</option><option value="credit">Crédit chez nous (avoir)</option></select></div>
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
    <button class="btn" id="doc-conv" style="display:none">Transformer en facture</button>
    <button class="btn" id="doc-x">Fermer</button>
  </div>
  <div class="doc" id="doc-corps"></div>
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
        <select id="enc-mode"><option value="zelle">Zelle</option><option value="carte">Carte bancaire</option><option value="especes">Espèces</option><option value="virement">Virement</option><option value="credit">Crédit chez nous (avoir)</option></select></div>
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
const FMODES={zelle:'Zelle',carte:'Carte bancaire',especes:'Espèces',virement:'Virement',credit:'Crédit chez nous'};
const FSTAT={paye:'Payée',partiel:'Acompte',apayer:'À payer',devis:'Devis',converti:'Devis transformé'};
function factReg(){
  const R=lit(KREG,{}); const F=Object.assign({raison:'',enseigne:'Perfumes Trade',adresse:'',tel:'',email:'',taxid:'',taux:7,carte:2.6,zelle:'',prefixe:'PT',conditions:'',exo:'Sale for resale — Florida Annual Resale Certificate on file.'},R.fact||{});
  if(!F.raison) F.raison=R.societe||'DASY LLC';
  return F;
}
/* numéro suivant : PT-2026-0001 pour les factures, DV-2026-0001 pour les devis */
function docNum(type,d){
  const F=factReg(), an=(d||new Date().toISOString()).slice(0,4);
  const pre=(type==='devis'?'DV':(F.prefixe||'PT').toUpperCase())+'-'+an+'-';
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

function calcDoc(lignes,o){
  const F=factReg();
  const sousTotal=Math.round(lignes.reduce((a,l)=>a+nbSur(l.q)*nbSur(l.p),0)*100)/100;

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
  const total=Math.round((base+frais+taxe)*100)/100;
  const regle=o.pstat==='paye'?total:(o.pstat==='partiel'?Math.min(total,+o.regle||0):0);
  return {sousTotal,remType,remVal,remise,remPct,remLib:(o.remLib||'').slice(0,60),base,
          fraisPct,frais,taux,taxe,total,regle,reste:Math.max(0,Math.round((total-regle)*100)/100)};
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
  ['v-pmode','v-pstat','v-pregle','v-fiscal','v-fref','v-remval','v-remtype','v-remlib','v-taux','v-langue','v-frais']
    .forEach(i=>{ const e=$(i); if(e) e.disabled=!on; });
  $('v-pregle').style.display=(on&&$('v-pstat').value==='partiel')?'':'none';
  /* les frais de carte ne se montrent que quand ils peuvent servir : un champ qui
     ne change rien à l'écran est un champ qu'on remplit pour rien */
  if($('v-fraisbloc')) $('v-fraisbloc').style.display=(on&&$('v-pmode').value==='carte')?'':'none';
  $('v-fref').style.display=(on&&$('v-fiscal').value!=='taxable')?'':'none';
  if($('v-doc').value==='devis'){ $('v-stock').checked=false; $('v-stock').disabled=true; }
  else { $('v-stock').disabled=false; if(!$('v-stock').dataset.touche) $('v-stock').checked=true; }
  const F=factReg();
  $('v-docaide').textContent = !on ? '' :
    $('v-doc').value==='devis' ? 'Un devis ne sort rien du stock. Il pourra être transformé en facture en un clic, quand le client confirme.'
    : (F.raison&&F.adresse?'':'L\'en-tête de la facture est incomplet (raison sociale, adresse…) : Réglages › Factures et devis. ')
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
['v-pregle','v-remval','v-taux','v-remlib','v-frais'].forEach(i=>{ const e=$(i); if(e) e.addEventListener('input',docTotaux); });
$('v-client').addEventListener('change',docClientChange);
$('v-stock').addEventListener('change',()=>{ $('v-stock').dataset.touche='1'; });
/* ce que la fenêtre propose à l'ouverture : facture pour le gros, rien pour les autres canaux */
function docReset(){
  const c=canalCour(); $('v-doc').value=c.id==='gros'?'facture':'';
  $('v-pmode').value='zelle'; $('v-pstat').value='paye'; $('v-pregle').value=''; $('v-fiscal').value='taxable'; $('v-fref').value='';
  $('v-remval').value=''; $('v-remtype').value='pct'; $('v-remlib').value=''; $('v-taux').value='';
  if($('v-frais')) $('v-frais').value='';
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
    taux:$('v-taux').value, frais:($('v-frais')?$('v-frais').value:''), langue:$('v-langue').value};
}
function docPourVente(lignes,client,d,CLI){
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
  return Object.assign({type,num:docNum(type,d),pmode:o.pmode,pstat:o.pstat,fiscal:o.fiscal,fref:o.fref,
    langue:o.langue||(typeof LANG!=='undefined'?LANG:'fr'),note:note||undefined,
    emis:new Date().toISOString(),entete:factReg()},c);
}
/* ---- le document ---- */
let DOC=null;
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
function dessineDoc(f){
  DOC=f; const D=f.doc, E=D.entete||factReg(), CLI=lit(KCLI,{}), cl=CLI[f.tiers]||{nom:f.tiers||''};
  const st=docStatut(f), devis=D.type==='devis';
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
       ${E.logo?`<img class="logo" src="${esc(E.logo)}" alt="">`:''}
       <div class="soc" data-nolang><b>${esc(E.raison||'')}</b>${E.enseigne&&E.enseigne!==E.raison?`<span class="ens">${esc(E.enseigne)}</span>`:''}
         ${E.adresse?`<span>${esc(E.adresse)}</span>`:''}${E.tel?`<span>${esc(E.tel)}</span>`:''}${E.email?`<span>${esc(E.email)}</span>`:''}
         ${E.taxid?`<span><span class="lbl">Sales tax n°</span> ${esc(E.taxid)}</span>`:''}</div>
     </div>
     <div class="titre"><h2>${devis?'Devis':'Facture'}</h2>
       <span class="num" data-nolang>${esc(D.num)}</span>
       <span data-nolang>${dfr(f.d)}</span>
       ${devis?`<span>Valable 15 jours</span>`:''}</div>
   </div>
   <div class="parties">
     <div><h4>${devis?'Adressé à':'Facturé à'}</h4>
       <div data-nolang><b>${esc(cl.raison||cl.nom||'')}</b>${cl.raison&&cl.nom!==cl.raison?`<br>${esc(cl.nom)}`:''}${cl.adresse?`<br>${esc(cl.adresse)}`:''}${cl.tel?`<br>${esc(cl.tel)}`:''}${cl.email?`<br>${esc(cl.email)}`:''}</div></div>
     <div><h4>Conditions</h4><div><span class="lbl">Paiement</span> : <b>${esc(FMODES[D.pmode]||D.pmode)}</b>${D.fiscal!=='taxable'?`<br><span data-nolang>${esc(E.exo||'Exempt')}${D.fref?` — n° ${esc(D.fref)}`:''}</span>`:''}${E.conditions?`<br><span data-nolang>${esc(E.conditions)}</span>`:''}${D.note?`<br><span class="lbl">Note</span> : <span data-nolang>${esc(D.note)}</span>`:''}</div></div>
   </div>
   <table><thead><tr><th>#</th><th>Article</th><th class="r">Qté</th><th class="r">Prix unit.</th><th class="r">Montant</th></tr></thead>
   <tbody>${lignes.map((l,i)=>`<tr><td class="n">${i+1}</td><td data-nolang><b>${esc(l.ref)}</b><small>${esc(l.bc||'')}</small></td><td class="r">${nf(l.q)}</td><td class="r">$${dus(l.p)}</td><td class="r"><b>$${dus(nbSur(l.q)*nbSur(l.p))}</b></td></tr>`).join('')}</tbody></table>
   <div class="totaux">
     <div><span>Sous-total</span><b>$${dus(D.sousTotal)}</b></div>
     ${D.remise?`<div class="rem"><span><span class="lbl">Remise</span>${D.remType==='pct'?' '+D.remVal+' %':''}${D.remLib?` — <span data-nolang>${esc(D.remLib)}</span>`:''}</span><b>−$${dus(D.remise)}</b></div>`:''}
     ${D.frais?`<div><span><span class="lbl">Frais carte</span> ${D.fraisPct} %</span><b>$${dus(D.frais)}</b></div>`:''}
     <div><span>${D.taux?`<span class="lbl">Sales tax</span> ${D.taux} %`:'Sales tax — exonéré'}</span><b>$${dus(D.taxe)}</b></div>
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
   ${devis?`<div class="tampon devis">${st==='converti'?`<span class="lbl">Transformé en facture</span> <span data-nolang>${esc(D.convertiNum||'')}</span>`:'Devis — sans engagement de stock'}</div>`:''}
   <div class="pied"><span data-nolang>${esc(E.raison||'')}${E.adresse?' · '+esc(E.adresse):''}${E.tel?' · '+esc(E.tel):''}${E.email?' · '+esc(E.email):''}</span><br>
     <span class="lbl">${devis?'Devis':'Facture'}</span> <span data-nolang>${esc(D.num)}</span> ·
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
  $('doc-conv').style.display=(devis&&!D.converti)?'':'none';
  $('docov').classList.add('on');
  /* la feuille se photographie tout de suite, en arrière-plan : quand on clique
     WhatsApp, Email ou Partager, le PDF est déjà prêt — et « Partager » DOIT
     répondre au clic sans attendre, sinon le téléphone refuse le partage */
  docPrepare(f);
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
  const L=(f.lignes||[]).filter(l=>l.q).map(l=>`• ${l.ref} × ${l.q} — $${dus(nbSur(l.q)*nbSur(l.p))}`).join('\n');
  const salut=lg==='fr'?'Bonjour'+(f.tiers?' '+f.tiers:'')+',':lg==='es'?'Hola'+(f.tiers?' '+f.tiers:'')+',':'Hello'+(f.tiers?' '+f.tiers:'')+',';
  const intro=devis
    ?(lg==='fr'?'Merci pour votre demande de cotation. Voici votre devis':lg==='es'?'Gracias por su solicitud de cotización. Aquí tiene su cotización':'Thank you for your quote request. Here is your quote')
    :(lg==='fr'?'Voici votre facture':lg==='es'?'Aquí tiene su factura':'Here is your invoice');
  const total=T('Total').toUpperCase()+' : $'+dus(D.total);
  return `${salut}\n\n${intro} *${D.num}* (${dfr(f.d)}) :\n\n${L}\n\n`
    + `${T('Sous-total')} : $${dus(D.sousTotal)}`
    + `${D.remise?'\n'+T('Remise')+' : −$'+dus(D.remise):''}`
    + `${D.frais?'\n'+T('Frais carte')+' '+D.fraisPct+' % : $'+dus(D.frais):''}\n`
    + `${D.taux?T('Sales tax')+' '+D.taux+' % : $'+dus(D.taxe):T('Sales tax — exonéré')}\n`
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
$('doc-print').onclick=()=>{ document.body.classList.add('impr-doc'); const fin=()=>document.body.classList.remove('impr-doc');
  window.addEventListener('afterprint',fin,{once:true}); setTimeout(()=>{ window.print(); setTimeout(fin,1500); },50); };
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
async function docCanvas(){
  await _pdfLibs();
  const el=$('doc-corps');
  return await window.html2canvas(el,{scale:2,backgroundColor:'#ffffff',useCORS:true,logging:false,windowWidth:Math.max(860,el.scrollWidth)});
}
function canvasPDF(c){
  const {jsPDF}=window.jspdf;
  const pdf=new jsPDF({unit:'pt',format:'letter',orientation:'portrait',compress:true});
  const W=pdf.internal.pageSize.getWidth(), H=pdf.internal.pageSize.getHeight(), m=28;
  const w=W-2*m, ratio=w/c.width, hPage=(H-2*m)/ratio;   /* hauteur d'une page en pixels du canevas */
  for(let y=0, n=0; y<c.height; y+=hPage, n++){
    const h=Math.min(hPage,c.height-y);
    const part=document.createElement('canvas'); part.width=c.width; part.height=Math.ceil(h);
    part.getContext('2d').drawImage(c,0,y,c.width,h,0,0,c.width,h);
    if(n) pdf.addPage();
    pdf.addImage(part.toDataURL('image/jpeg',0.92),'JPEG',m,m,w,h*ratio);
  }
  return pdf.output('blob');
}
/* l'aperçu : la première page, réduite à 1000 px de large — assez pour être lue
   sur un téléphone, assez léger pour la carte WhatsApp */
function canvasPNG(c){
  const w=1000, ratio=w/c.width, h=Math.min(c.height*ratio, 1300);
  const p=document.createElement('canvas'); p.width=w; p.height=Math.round(h);
  p.getContext('2d').drawImage(c,0,0,c.width,h/ratio,0,0,w,h);
  return new Promise(r=>p.toBlob(r,'image/png'));
}
async function docPDF(){ return (await docPret(DOC)).pdf; }
const docNomPDF=f=>((f.doc.type==='devis'?((typeof vf==='function')?vf('Devis',f.doc.langue||LANG):'Devis'):'Facture')+'-')+String(f.doc.num).replace(/[^A-Za-z0-9._-]/g,'')+'.pdf';
/* le lien public du document : déposé une fois, réutilisé ensuite */
async function docLien(f){
  if(typeof CK_URL==='undefined' || typeof ckTok!=='function' || !ckTok()) throw new Error("Pas de session serveur : le texte part sans le PDF.");
  const pr=await docPret(f); const c=pr.canvas, blob=pr.pdf; const D=f.doc, E=factReg();
  const q='?type='+(D.type||'devis')+'&enseigne='+encodeURIComponent(E.enseigne||E.raison||'')+'&date='+encodeURIComponent(dfr(f.d))
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
$('doc-wa').onclick=async()=>{ const f=DOC; const tel=String(coordTiers(f.tiers).tel||'').replace(/[^0-9]/g,'');
  $('doc-wa').disabled=true; const txt=await docEnvoiTexte(f); $('doc-wa').disabled=false; if(!DOC||DOC.id!==f.id) return;
  window.open('https://wa.me/'+(tel||'')+'?text='+encodeURIComponent(txt),'_blank'); };
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
function docSujet(f){ const D=f.doc; const t=(D.type==='devis'?'Devis ':'Facture ')+D.num+' — '+(factReg().enseigne||factReg().raison); return (typeof vf==='function')?vf(t,D.langue||LANG):t; }
function docMotCourrier(f){ const t=docMotCourrier0(f); return (typeof vf==='function')?vf(t,f.doc.langue||LANG):t; }
function docMotCourrier0(f){
  const D=f.doc, E=factReg(), devis=D.type==='devis';
  const lg=D.langue||(typeof LANG!=='undefined'?LANG:'fr');
  const corps=lg==='fr'?(devis?'Bonjour,\n\nMerci pour votre demande de cotation. Veuillez trouver ci-joint le devis.':'Bonjour,\n\nVeuillez trouver ci-joint votre facture.')
    :lg==='es'?(devis?'Hola,\n\nGracias por su solicitud de cotización. Adjunto encontrará la cotización.':'Hola,\n\nAdjunto encontrará su factura.')
    :(devis?'Hello,\n\nThank you for your quote request. Please find the quote attached.':'Hello,\n\nPlease find your invoice attached.');
  const merci=lg==='fr'?'Merci,':lg==='es'?'Gracias,':'Thank you,';
  return corps+'\n\n'+merci+'\n'+(E.enseigne||E.raison)+(E.tel?' · '+E.tel:'');
}
$('doc-mail').onclick=async()=>{ const f=DOC; const co=coordTiers(f.tiers);
  $('doc-mail').disabled=true; const b=await boiteEnvoi(); $('doc-mail').disabled=false; if(!DOC||DOC.id!==f.id) return;
  if(!b.pret){
    const txt=await docEnvoiTexte(f); if(!DOC||DOC.id!==f.id) return;
    location.href='mailto:'+encodeURIComponent(co.email||'')+'?subject='+encodeURIComponent(docSujet(f))+'&body='+encodeURIComponent(txt); return; }
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
/* un devis accepté devient une facture : nouveau numéro, et cette fois le stock sort */
$('doc-conv').onclick=()=>{
  const f=DOC; if(!f||!f.doc||f.doc.type!=='devis'||f.doc.converti) return;
  if(!confirm(vf('Transformer le devis '+f.doc.num+' en facture ? Les quantités sortiront du stock.'))) return;
  const d=ajd(), JOU=lit(KJOU,[]), VENT=lit(KVENT,{});
  const lignes=[], det=[]; let sortis=0;
  (f.lignes||[]).forEach(l=>{ const qAv=qteEff(l.cle), qAp=Math.max(0,qAv-(l.q||0));
    lignes.push({cle:l.cle,bc:l.bc,ref:l.ref,q:l.q,p:l.p,qAv,qAp,manque:Math.max(0,(l.q||0)-qAv),paAv:paEff(l.cle)});
    if(qAp!==qAv){ MOD[l.cle]=Object.assign({},MOD[l.cle]||{},{qte:qAp}); det.push({bc:l.bc,ref:l.ref,av:qAv,ap:qAp}); sortis+=qAv-qAp; }
    (VENT[l.cle]=VENT[l.cle]||[]).push({d,h:heureMiami(),p:l.p,c:f.tiers||'',q:l.q,num:'',k:f.canal}); });
  const num=numAuto(d);
  const doc=Object.assign({},f.doc,{type:'facture',num:docNum('facture',d),pstat:'apayer',emis:new Date().toISOString(),deDevis:f.doc.num});
  Object.assign(doc,calcDoc(lignes,doc));
  const f2={id:'v'+Date.now().toString(36),num,sens:'vente',canal:f.canal,tiers:f.tiers,d,h:heureMiami(),lignes,montant:doc.sousTotal,stock:true,manuel:true,par:USR||'(non renseigné)',t:new Date().toISOString(),doc};
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
  const L=FACT.filter(f=>f.doc&&(f.sens==='vente'||f.sens==='devis')).sort((a,b)=>(b.t||'').localeCompare(a.t||''));
  const du=L.filter(f=>docStatut(f)==='apayer'||docStatut(f)==='partiel');
  const totDu=du.reduce((a,f)=>a+(f.doc.reste||0),0);
  $('docs-em').textContent=L.length?`${nf(L.length)} document${L.length>1?'s':''}${du.length?` · ${du.length} à encaisser pour ${money2(totDu)}`:''}`:'aucun encore — coche « Facture » ou « Devis » en enregistrant une vente';
  const chips=[['','Tous'],['apayer','À encaisser'],['paye','Payées'],['devis','Devis']];
  $('docs-chips').innerHTML=L.length?chips.map(([v,l])=>`<button class="${DOCS_F===v?'on':''}" data-f="${v}">${l}</button>`).join(''):'';
  $('docs-chips').querySelectorAll('button').forEach(b=>b.onclick=()=>{ DOCS_F=b.dataset.f; peintDocs(); });
  const V=L.filter(f=>{ const s=docStatut(f); return !DOCS_F || (DOCS_F==='apayer'?(s==='apayer'||s==='partiel'):DOCS_F==='devis'?(s==='devis'||s==='converti'):s===DOCS_F); });
  $('docs-table').innerHTML=!L.length?'':!V.length?'<p class="ecr">Rien dans cette catégorie.</p>':`<table><thead><tr><th>N°</th><th>Date</th><th>Client</th><th>Paiement</th><th class="r">Total</th><th class="r">Reste dû</th><th>État</th><th></th></tr></thead><tbody>
    ${V.slice(0,60).map(f=>{ const s=docStatut(f); return `<tr><td><b>${esc(f.doc.num)}</b></td><td>${dfr(f.d)}</td><td>${esc(f.tiers||'—')}</td><td>${esc(FMODES[f.doc.pmode]||'')}</td><td class="r">${money2(f.doc.total)}</td><td class="r">${f.doc.type==='devis'?'—':money2(f.doc.reste||0)}</td><td><span class="st ${s}">${FSTAT[s]||s}</span></td><td class="r"><button class="btn sm" data-doc="${esc(f.id)}">Voir</button></td></tr>`; }).join('')}</tbody></table>`;
  $('docs-table').querySelectorAll('[data-doc]').forEach(b=>b.onclick=()=>{ const f=FACT.find(x=>x.id===b.dataset.doc); if(f) dessineDoc(f); });
}
peintDocs();
"""
