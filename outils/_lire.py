# -*- coding: utf-8 -*-
"""Lire un fichier déposé : Excel, CSV, TSV, texte, PDF (avec texte ou scanné), photo.

Pourquoi ce module existe : un fournisseur qui envoie un devis l'envoie en Excel
une fois sur deux. Jusqu'ici la zone de dépôt lisait le .xlsx comme du texte —
c'est un ZIP, donc elle en tirait du charabia binaire, sans rien dire. Pire qu'un
refus : l'outil avait l'air de marcher.

Le classeur est converti en colonnes séparées par des tabulations, exactement la
forme que le reste de l'outil sait déjà lire. Aucun code de lecture de devis n'a
donc à connaître Excel.

Pas de bibliothèque : un .xlsx est un ZIP de XML, et le navigateur sait
décompresser (DecompressionStream) et lire du XML (DOMParser).
"""

LIRE = r"""
/* ---------- ouvrir un ZIP (c'est ce qu'est un .xlsx) ---------- */
async function _zipOuvre(buf){
  const d=new DataView(buf.buffer||buf), u=new Uint8Array(buf.buffer||buf);
  /* On part de la fin : le catalogue central est en queue de fichier, et c'est
     lui qui fait autorité — les en-têtes locaux, eux, peuvent mentir sur les
     tailles quand le fichier a été écrit en flux. */
  let fin=-1;
  for(let i=u.length-22;i>=0 && i>u.length-66000;i--){ if(d.getUint32(i,true)===0x06054b50){ fin=i; break; } }
  if(fin<0) throw new Error('zip');
  const n=d.getUint16(fin+10,true); let p=d.getUint32(fin+16,true);
  const dec=new TextDecoder(), out={};
  for(let k=0;k<n;k++){
    if(d.getUint32(p,true)!==0x02014b50) break;
    const meth=d.getUint16(p+10,true), taille=d.getUint32(p+20,true);
    const ln=d.getUint16(p+28,true), lx=d.getUint16(p+30,true), lc=d.getUint16(p+32,true);
    const debut=d.getUint32(p+42,true);
    const nom=dec.decode(u.subarray(p+46,p+46+ln));
    /* l'en-tête local n'a pas la même longueur d'extra que le catalogue */
    const lnL=d.getUint16(debut+26,true), lxL=d.getUint16(debut+28,true);
    const dep=debut+30+lnL+lxL;
    out[nom]={meth, brut:u.subarray(dep,dep+taille)};
    p+=46+ln+lx+lc;
  }
  return out;
}
async function _zipTexte(e){
  if(!e) return '';
  if(e.meth===0) return new TextDecoder().decode(e.brut);
  if(e.meth!==8) throw new Error('compression '+e.meth);
  if(typeof DecompressionStream==='undefined') throw new Error('vieux navigateur');
  const fl=new Blob([e.brut]).stream().pipeThrough(new DecompressionStream('deflate-raw'));
  return await new Response(fl).text();
}

/* ---------- un classeur Excel -> des colonnes ---------- */
const _colNum=r=>{ const m=/^([A-Z]+)/.exec(r||''); if(!m) return 0;
  let n=0; for(const c of m[1]) n=n*26+(c.charCodeAt(0)-64); return n-1; };

/* 28 sept. 2026 (Igal : « les fichiers xls ne marchent pas, ça reste gris quand je veux le
   choisir ») : le vieil Excel (.xls), l'OpenDocument (.ods) et les « .xls » qui sont en
   fait une page HTML ou un CSV (exports de sites de fournisseurs) passent par SheetJS,
   servi par l'outil (lib/sheetjs/, Apache-2.0) et chargé seulement quand on en a besoin.
   Même sortie que lireClasseur : la première feuille, une ligne par rangée, cases
   séparées par des tabulations. */
async function _sheetjs(){
  if(window.XLSX) return window.XLSX;
  await new Promise((res,rej)=>{ const sc=document.createElement('script'); sc.src='lib/sheetjs/xlsx.full.min.js';
    sc.onload=res; sc.onerror=()=>rej(new Error("Le lecteur des vieux fichiers Excel n'a pas pu être chargé (lib/sheetjs manquant)."));
    document.head.appendChild(sc); });
  return window.XLSX;
}
async function lireVieuxClasseur(buf){
  const X=await _sheetjs(); let wb;
  const NON="Ce fichier n'a pas pu être ouvert comme un classeur Excel. Ouvre-le dans Excel et fais « Enregistrer sous » en .xlsx ou en .csv.";
  try{ wb=X.read(buf,{type:'array',cellDates:false}); }
  catch(e){ throw new Error(NON); }
  const nom=(wb.SheetNames||[])[0]; if(!nom) throw new Error("Ce classeur ne contient aucune feuille lisible.");
  const rows=X.utils.sheet_to_json(wb.Sheets[nom],{header:1,raw:false,defval:'',blankrows:true});
  const lignes=rows.map(r=>r.map(v=>String(v==null?'':v).replace(/[\t\r\n]+/g,' ').trim()).join('\t'));
  while(lignes.length && !lignes[lignes.length-1].replace(/\t/g,'').trim()) lignes.pop();
  if(!lignes.length) throw new Error("Cette feuille est vide.");
  /* un binaire quelconque, SheetJS le prend pour du texte : on ne fait pas semblant */
  const t=lignes.join('\n');
  if(/[\u0000-\u0008\u000b\u000c\u000e-\u001f\ufffd]/.test(t.slice(0,4000))) throw new Error(NON);
  return t;
}
async function lireClasseur(fichier){
  const buf=new Uint8Array(await fichier.arrayBuffer());
  if(!(buf[0]===0x50&&buf[1]===0x4b)) return await lireVieuxClasseur(buf);
  let z; try{ z=await _zipOuvre(buf); }catch(e){ throw new Error("Ce classeur n'a pas pu être ouvert. Réenregistre-le en .xlsx ou en .csv."); }

  /* les textes sont rangés à part, dans une table commune à tout le classeur */
  let SS=[];
  if(z['xl/sharedStrings.xml']){
    const x=new DOMParser().parseFromString(await _zipTexte(z['xl/sharedStrings.xml']),'application/xml');
    SS=[...x.getElementsByTagName('si')].map(si=>[...si.getElementsByTagName('t')].map(t=>t.textContent).join(''));
  }

  /* la première feuille au sens du classeur, pas au sens du nom de fichier :
     sheet1.xml n'est pas toujours l'onglet de gauche */
  let cible='xl/worksheets/sheet1.xml';
  try{
    const wb=new DOMParser().parseFromString(await _zipTexte(z['xl/workbook.xml']),'application/xml');
    const f=wb.getElementsByTagName('sheet')[0];
    const id=f&&(f.getAttribute('r:id')||f.getAttribute('id'));
    if(id){
      const rl=new DOMParser().parseFromString(await _zipTexte(z['xl/_rels/workbook.xml.rels']),'application/xml');
      for(const r of rl.getElementsByTagName('Relationship')){
        if(r.getAttribute('Id')===id){ let t=r.getAttribute('Target')||'';
          t=t.replace(/^\/?xl\//,'').replace(/^\.\//,''); cible='xl/'+t; break; }
      }
    }
  }catch(e){}
  if(!z[cible]) cible=Object.keys(z).find(k=>/^xl\/worksheets\/.*\.xml$/.test(k))||cible;
  if(!z[cible]) throw new Error("Ce classeur ne contient aucune feuille lisible.");

  const sh=new DOMParser().parseFromString(await _zipTexte(z[cible]),'application/xml');
  const lignes=[];
  for(const row of sh.getElementsByTagName('row')){
    const cells=[];
    for(const c of row.getElementsByTagName('c')){
      const i=_colNum(c.getAttribute('r')), t=c.getAttribute('t')||'';
      let v='';
      if(t==='inlineStr'){ v=[...c.getElementsByTagName('t')].map(x=>x.textContent).join(''); }
      else { const n=c.getElementsByTagName('v')[0]; const b=n?n.textContent:'';
             v = (t==='s') ? (SS[+b]||'') : b; }
      /* une case vide au milieu ne doit pas decaler les colonnes suivantes */
      while(cells.length<i) cells.push('');
      cells[i]=String(v).replace(/[\t\r\n]+/g,' ').trim();
    }
    lignes.push(cells.join('\t'));
  }
  /* on coupe les lignes vides de fin : Excel en fabrique souvent des centaines */
  while(lignes.length && !lignes[lignes.length-1].replace(/\t/g,'').trim()) lignes.pop();
  if(!lignes.length) throw new Error("Cette feuille est vide.");
  return lignes.join('\n');
}

/* ---------- PDF : le texte s'il y en a, sinon l'image de chaque page ---------- */
/* pdf.js est soit deja dans la page (les rubriques qui l'embarquent), soit charge
   a la demande depuis lib/pdfjs/. Depuis un fichier ouvert en local (file://) le
   navigateur refuse de charger un module : on le dit, au lieu d'echouer en silence. */
async function _pdfjs(){
  if(window.pdfjsLib) return window.pdfjsLib;
  if(location.protocol==='file:') throw new Error("Les PDF se lisent sur la version en ligne de l'outil, pas depuis un fichier ouvert en local.");
  const m=await import('./lib/pdfjs/pdf.min.mjs');
  m.GlobalWorkerOptions.workerSrc='lib/pdfjs/pdf.worker.min.mjs';
  window.pdfjsLib=m; return m;
}
async function lirePDFTexte(buf){
  const pdfjs=await _pdfjs();
  const pdf=await pdfjs.getDocument({data:buf}).promise; const out=[];
  for(let i=1;i<=pdf.numPages;i++){
    const pg=await pdf.getPage(i), tc=await pg.getTextContent(), L={};
    tc.items.forEach(it=>{ if(!it.str.trim()) return; const y=Math.round(it.transform[5]/2)*2;
      (L[y]=L[y]||[]).push({x:it.transform[4],s:it.str}); });
    Object.keys(L).map(Number).sort((a,b)=>b-a).forEach(y=>out.push(L[y].sort((a,b)=>a.x-b.x).map(o=>o.s).join('  ')));
  }
  return {texte:out.join('\n'), pages:pdf.numPages, pdf};
}
/* un PDF scanne n'a pas de texte : on dessine chaque page et on la lit comme une photo */
async function _pdfPagesEnImages(pdf, max){
  const out=[];
  for(let i=1;i<=Math.min(pdf.numPages,max||6);i++){
    const pg=await pdf.getPage(i), vp=pg.getViewport({scale:2});
    const c=document.createElement('canvas'); c.width=vp.width; c.height=vp.height;
    await pg.render({canvasContext:c.getContext('2d'),viewport:vp}).promise;
    out.push(await new Promise(r=>c.toBlob(r,'image/png')));
  }
  return out;
}

/* ---------- photo : reconnaissance de caracteres, dans le navigateur ---------- */
/* tesseract.js, servi par l'outil lui-meme (lib/tesseract/) : l'image ne part
   nulle part. Le premier usage telecharge environ 15 Mo (moteur + anglais), que
   le navigateur garde ensuite. L'anglais lit tres bien un devis ou une liste de
   parfums : ce sont des noms propres et des chiffres, pas des phrases. */
let _ocrWorker=null;
async function _ocr(){
  if(_ocrWorker) return _ocrWorker;
  if(location.protocol==='file:') throw new Error("Les photos se lisent sur la version en ligne de l'outil, pas depuis un fichier ouvert en local.");
  if(!window.Tesseract){
    await new Promise((res,rej)=>{ const sc=document.createElement('script'); sc.src='lib/tesseract/tesseract.min.js';
      sc.onload=res; sc.onerror=()=>rej(new Error("Le moteur de lecture des photos n'a pas pu être chargé (lib/tesseract manquant)."));
      document.head.appendChild(sc); });
  }
  _ocrWorker=await window.Tesseract.createWorker('eng',1,{
    workerPath:'lib/tesseract/worker.min.js', corePath:'lib/tesseract/', langPath:'lib/tesseract/lang',
    logger:m=>{ try{ if(window.__lireAvance) window.__lireAvance(m); }catch(e){} } });
  return _ocrWorker;
}
async function lireImage(img){
  const w=await _ocr();
  const r=await w.recognize(img);
  /* on garde les lignes telles que lues : une ligne = un article, la plupart du temps */
  return (r.data&&r.data.text||'').replace(/[ \t]+\n/g,'\n').trim();
}

/* ---------- la porte d'entree unique ---------- */
/* Rend TOUJOURS du texte a lignes, ou une erreur en francais clair.
   `avance(msg)` est appele pendant les lectures longues (photo, PDF scanne).
   Tout passe : tableur, CSV, texte, PDF avec texte, PDF scanne, photo. */
async function lireFichier(fichier, avance){
  const n=(fichier.name||'').toLowerCase(), type=fichier.type||'';
  window.__lireAvance = avance ? (m=>{ if(m&&m.status==='recognizing text') avance('Lecture de la photo… '+Math.round((m.progress||0)*100)+' %');
    else if(m&&/loading|initializ/.test(m.status||'')) avance('Chargement du moteur de lecture (première fois : ~15 Mo)…'); }) : null;
  if(/\.xlsx$/.test(n) || type==='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    return await lireClasseur(fichier);
  if(/\.(xls|xlsm|xlsb|ods)$/.test(n) || type==='application/vnd.ms-excel' || type==='application/vnd.oasis.opendocument.spreadsheet'){
    const buf=new Uint8Array(await fichier.arrayBuffer());
    if(buf[0]===0x50&&buf[1]===0x4b&&/\.(xls|xlsm)$/.test(n)) return await lireClasseur(fichier);
    return await lireVieuxClasseur(buf);
  }
  if(/\.numbers$/.test(n))
    throw new Error("Ce format de tableur ne se lit pas ici. Exporte-le en .xlsx ou en .csv.");
  if(/\.pdf$/.test(n) || type==='application/pdf'){
    const buf=new Uint8Array(await fichier.arrayBuffer());
    const r=await lirePDFTexte(buf);
    if(r.texte.replace(/\s/g,'').length>=40) return r.texte;
    /* pas de texte : un scan ou une photo mise en PDF — on lit l'image */
    if(avance) avance('PDF sans texte : lecture comme une photo…');
    const imgs=await _pdfPagesEnImages(r.pdf, 6); const parts=[];
    for(const b of imgs) parts.push(await lireImage(b));
    const t=parts.join('\n').trim();
    if(t.replace(/\s/g,'').length<10) throw new Error("Ce PDF n'a rien de lisible, même en le regardant comme une image.");
    return t;
  }
  if(/\.heic$/.test(n)||type==='image/heic') throw new Error("Les photos HEIC (iPhone) ne se lisent pas dans le navigateur : envoie-la par WhatsApp ou par email, elle deviendra un JPEG.");
  if(/\.(png|jpe?g|webp|gif|bmp|tiff?)$/.test(n) || /^image\//.test(type)){
    const t=await lireImage(fichier);
    if(t.replace(/\s/g,'').length<6) throw new Error("Rien de lisible sur cette photo. Prends-la de plus près, bien droite, sans reflet.");
    return t;
  }
  if(/\.(docx?|pages|zip|rar|7z)$/.test(n))
    throw new Error("Ce type de fichier ne se lit pas ici. Dépose un PDF, un Excel (.xlsx ou .xls), un CSV ou une photo.");
  const t=await fichier.text();
  /* un binaire lu comme du texte donne des caracteres de controle : mieux vaut
     le dire que de faire semblant d'avoir compris */
  if(/[\u0000-\u0008\u000b\u000c\u000e-\u001f]/.test(t.slice(0,2000)))
    throw new Error("Ce fichier n'est pas lisible comme du texte. Dépose un PDF, un Excel (.xlsx ou .xls), un CSV ou une photo.");
  return t;
}

/* ---------- un document qui passe d'une page a l'autre ----------
   Depose dans Fournisseurs, lu dans Factures ou dans l'Etude : le fichier voyage par
   IndexedDB (localStorage ne porte pas un PDF). Il n'est valable que dix minutes, et
   il est repris une seule fois. (Igal, 12 sept. 2026 : « ajouter un supplier simplement
   en rentrant n'importe quel type de document ».) */
const _DA_DB='pt-attente';
function _daOuvre(){ return new Promise((res,rej)=>{ const r=indexedDB.open(_DA_DB,1);
  r.onupgradeneeded=()=>{ r.result.createObjectStore('docs'); }; r.onsuccess=()=>res(r.result); r.onerror=()=>rej(r.error); }); }
async function docAttentePose(file){ const db=await _daOuvre();
  await new Promise((res,rej)=>{ const t=db.transaction('docs','readwrite');
    t.objectStore('docs').put({nom:file.name,type:file.type,blob:file,t:Date.now()},'doc'); t.oncomplete=res; t.onerror=()=>rej(t.error); }); }
async function docAttentePrend(){
  try{ const db=await _daOuvre();
    const o=await new Promise((res,rej)=>{ const t=db.transaction('docs','readwrite'); const st=t.objectStore('docs');
      const r=st.get('doc'); st.delete('doc'); r.onsuccess=()=>res(r.result); r.onerror=()=>rej(r.error); });
    if(!o||!o.blob||Date.now()-o.t>10*60*1000) return null;
    return new File([o.blob],o.nom||'document',{type:o.type||''});
  }catch(e){ return null; }
}
window.docAttentePose=docAttentePose; window.docAttentePrend=docAttentePrend;
"""

# Ce que les zones de dépôt doivent annoncer et accepter.
ACCEPT = "application/pdf,.pdf,.txt,.csv,.tsv,.xlsx,.xls,.xlsm,.ods,application/vnd.ms-excel,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,image/*,.png,.jpg,.jpeg,.webp"
ACCEPT_TAB = ".csv,.tsv,.txt,.xlsx,.xls,.xlsm,.ods,application/vnd.ms-excel,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,application/pdf,.pdf,image/*,.png,.jpg,.jpeg,.webp"


def bloc():
    """Le code à insérer dans une page."""
    return LIRE
