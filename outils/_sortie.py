# -*- coding: utf-8 -*-
"""Sortir un tableau de l'outil : Excel, PDF, CSV.

Pourquoi ce fichier existe. Chaque page avait son bouton « Exporter en CSV », et
chacun refabriquait ses colonnes dans son coin. Le CSV s'ouvre mal dans Excel —
accents cassés, tout dans une seule colonne, montants pris pour du texte — et Sam
travaille dans Excel. Il fallait donc un vrai .xlsx, et tant qu'à faire, une seule
façon de décrire un tableau pour les trois sorties.

Le principe : la page décrit UNE fois ce qu'elle affiche — un titre, le filtre en
toutes lettres, des colonnes typées, des lignes — et les trois sorties en découlent.
Excel, PDF et CSV contiennent donc exactement la même chose. Sans ça, on aurait
trois exports qui divergent, et le jour où ils divergent personne ne sait lequel
croire.

Le PDF passe par l'impression du navigateur, volontairement. Écrire un PDF à la
main pour un tableau de plusieurs milliers de lignes, c'est beaucoup de code, et
le résultat serait moins bon que ce que le navigateur produit déjà (polices,
coupures de page, numérotation). Ce qu'on fait ici, c'est préparer la page : on
cache le menu et les boutons, on répète l'en-tête du tableau à chaque page, et on
écrit en haut le titre, la date et le filtre — pour qu'un papier retrouvé dans
trois mois dise de quoi il parle.

Le .xlsx est écrit à la main. Un .xlsx est un ZIP de fichiers XML : on l'assemble
sans compression (le ZIP l'autorise, Excel l'accepte), donc sans dépendre d'aucune
bibliothèque extérieure. Les pages de Perfumes Trade s'ouvrent aussi hors ligne.
"""

CSS = r"""
/* le bouton Exporter et son petit menu */
.sbar{display:inline-block;position:relative}
.sbar>summary{list-style:none;cursor:pointer;display:inline-flex;align-items:center;gap:7px;
border:1px solid var(--line);background:var(--surface);border-radius:8px;padding:8px 14px;
font:600 13px Inter,sans-serif;color:var(--ink-2)}
.sbar>summary::-webkit-details-marker{display:none}
.sbar>summary:hover{border-color:var(--iris);color:var(--iris)}
.sbar[open]>summary{border-color:var(--iris);color:var(--iris)}
.sbar .smenu{position:absolute;top:calc(100% + 5px);right:0;z-index:30;min-width:250px;
background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:6px;
box-shadow:0 14px 34px rgba(0,0,0,.16)}
.sbar .smenu button{display:block;width:100%;text-align:left;border:0;background:none;
border-radius:7px;padding:9px 11px;font:inherit;font-size:13.5px;color:var(--ink);cursor:pointer}
.sbar .smenu button:hover{background:var(--surface-2)}
.sbar .smenu button b{display:block;font-weight:700}
.sbar .smenu button span{display:block;font-size:11.5px;color:var(--ink-3);line-height:1.4;margin-top:1px}
.sbar .smenu .squoi{padding:8px 11px 9px;border-top:1px solid var(--line-2);margin-top:4px;
font-size:11.5px;color:var(--ink-3);line-height:1.5}

/* la feuille à imprimer : invisible à l'écran, seule visible sur papier */
#imprzone{display:none}
.imprtete h2{margin:0 0 3px;font-size:19px;font-weight:800;letter-spacing:-.02em}
.imprtete p{margin:0;font-family:Inter,sans-serif;font-size:11px;color:#555;line-height:1.6}
@media print{
  body.impr-tab > *{display:none !important}
  body.impr-tab #imprzone{display:block !important}
  #imprzone .imprtete{margin:0 0 10px;padding-bottom:8px;border-bottom:2px solid #111}
  #imprzone table{width:100%;border-collapse:collapse;font-family:Inter,Arial,sans-serif;font-size:9.5px}
  #imprzone thead{display:table-header-group}       /* l'en-tête revient à chaque page */
  #imprzone tr{break-inside:avoid;page-break-inside:avoid}
  #imprzone th{text-align:left;border-bottom:1.5px solid #111;padding:5px 6px;
    font-size:8.5px;letter-spacing:.06em;text-transform:uppercase}
  #imprzone td{border-bottom:.5px solid #ddd;padding:4px 6px;vertical-align:top}
  #imprzone .r{text-align:right;white-space:nowrap}
  #imprzone tfoot td{border-top:1.5px solid #111;border-bottom:0;font-weight:700;padding-top:6px}
  @page{margin:11mm}
}
"""

JS = r"""
/* ============ SORTIR UN TABLEAU : Excel, PDF, CSV ============
   La page appelle poseSortie(id, () => ({...})) et fournit, au moment du clic :
     titre    : « Journal des ventes »
     filtre   : le filtre en toutes lettres — « 30 derniers jours · canal Boutique »
     fichier  : le début du nom de fichier
     colonnes : [{t:'Montant', y:'m'}] — y : 't' texte (défaut), 'n' nombre,
                'm' montant, 'd' date (aaaa-mm-jj), 'p' pourcentage
     lignes   : [[...], [...]] dans l'ordre des colonnes
   Les trois sorties partent de là : elles ne peuvent pas diverger. */

const _CRC=(()=>{ const t=new Uint32Array(256);
  for(let n=0;n<256;n++){ let c=n; for(let k=0;k<8;k++) c=(c&1)?(0xEDB88320^(c>>>1)):(c>>>1); t[n]=c>>>0; }
  return t; })();
function _crc32(u8){ let c=0xFFFFFFFF;
  for(let i=0;i<u8.length;i++) c=_CRC[(c^u8[i])&0xFF]^(c>>>8);
  return (c^0xFFFFFFFF)>>>0; }
const _octets=s=>new TextEncoder().encode(s);

/* Un ZIP sans compression : le format l'autorise (méthode 0) et Excel l'accepte.
   C'est ce qui permet d'écrire un vrai .xlsx sans charger la moindre bibliothèque. */
function _zip(fichiers){
  const morceaux=[], centre=[]; let pos=0;
  const heure=0, jour=((2026-1980)<<9)|(1<<5)|1;
  const u16=v=>[v&255,(v>>8)&255];
  const u32=v=>[v&255,(v>>8)&255,(v>>16)&255,(v>>>24)&255];
  fichiers.forEach(f=>{
    const nom=_octets(f.nom), d=f.data, crc=_crc32(d);
    const tete=[].concat(u32(0x04034b50),u16(20),u16(0),u16(0),u16(heure),u16(jour),
      u32(crc),u32(d.length),u32(d.length),u16(nom.length),u16(0));
    morceaux.push(new Uint8Array(tete), nom, d);
    centre.push([].concat(u32(0x02014b50),u16(20),u16(20),u16(0),u16(0),u16(heure),u16(jour),
      u32(crc),u32(d.length),u32(d.length),u16(nom.length),u16(0),u16(0),u16(0),u16(0),
      u32(0),u32(pos)), nom);
    pos+=tete.length+nom.length+d.length;
  });
  const cd=[]; let taille=0;
  for(let i=0;i<centre.length;i+=2){
    const a=new Uint8Array(centre[i]); cd.push(a,centre[i+1]); taille+=a.length+centre[i+1].length;
  }
  cd.push(new Uint8Array([].concat(u32(0x06054b50),u16(0),u16(0),
    u16(fichiers.length),u16(fichiers.length),u32(taille),u32(pos),u16(0))));
  return new Blob([...morceaux,...cd],{type:'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'});
}

const _xe=s=>String(s==null?'':s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&apos;'}[c]))
  .replace(/[\x00-\x08\x0b\x0c\x0e-\x1f]/g,'');
function _colL(n){ let s=''; n++; while(n>0){ const r=(n-1)%26; s=String.fromCharCode(65+r)+s; n=(n-r-1)/26; } return s; }
/* Excel compte les jours depuis le 30 décembre 1899. */
function _xdate(v){ const m=String(v||'').match(/^(\d{4})-(\d{2})-(\d{2})/); if(!m) return null;
  const d=Date.UTC(+m[1],+m[2]-1,+m[3]); return Math.round(d/86400000)+25569; }

function sortieXlsx(S){
  const C=S.colonnes||[], L=S.lignes||[];
  const style={t:0,n:0,m:2,d:3,p:4};
  let lignes='';
  lignes+='<row r="1">'+C.map((c,j)=>
    `<c r="${_colL(j)}1" s="1" t="inlineStr"><is><t>${_xe(c.t)}</t></is></c>`).join('')+'</row>';
  L.forEach((li,i)=>{
    const r=i+2;
    lignes+=`<row r="${r}">`+C.map((c,j)=>{
      const v=li[j], ref=_colL(j)+r, y=c.y||'t';
      if(v==null||v==='') return `<c r="${ref}" s="${style[y]||0}"/>`;
      if(y==='n'||y==='m'||y==='p'){ const n=Number(v);
        return isFinite(n)?`<c r="${ref}" s="${style[y]}"><v>${n}</v></c>`
                          :`<c r="${ref}" t="inlineStr"><is><t>${_xe(v)}</t></is></c>`; }
      if(y==='d'){ const n=_xdate(v);
        return n!=null?`<c r="${ref}" s="3"><v>${n}</v></c>`
                     :`<c r="${ref}" t="inlineStr"><is><t>${_xe(v)}</t></is></c>`; }
      return `<c r="${ref}" t="inlineStr"><is><t>${_xe(v)}</t></is></c>`;
    }).join('')+'</row>';
  });
  /* largeur des colonnes : sinon tout est à 8 caractères et Sam redimensionne à la main */
  const larg=C.map((c,j)=>{
    let m=String(c.t||'').length;
    for(let i=0;i<Math.min(L.length,400);i++) m=Math.max(m,String(L[i][j]==null?'':L[i][j]).length);
    return `<col min="${j+1}" max="${j+1}" width="${Math.min(46,Math.max(9,m+2))}" customWidth="1"/>`;
  }).join('');

  const feuille=`<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
<sheetViews><sheetView workbookViewId="0"><pane ySplit="1" topLeftCell="A2" activePane="bottomLeft" state="frozen"/></sheetView></sheetViews>
<cols>${larg}</cols><sheetData>${lignes}</sheetData>
<autoFilter ref="A1:${_colL(Math.max(0,C.length-1))}${L.length+1}"/></worksheet>`;

  const styles=`<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
<numFmts count="2"><numFmt numFmtId="164" formatCode="#,##0.00\\ &quot;$&quot;"/><numFmt numFmtId="165" formatCode="0.0\\ &quot;%&quot;"/></numFmts>
<fonts count="2"><font><sz val="11"/><name val="Calibri"/></font><font><b/><sz val="11"/><name val="Calibri"/></font></fonts>
<fills count="3"><fill><patternFill patternType="none"/></fill><fill><patternFill patternType="gray125"/></fill><fill><patternFill patternType="solid"><fgColor rgb="FFEDEDF2"/><bgColor indexed="64"/></patternFill></fill></fills>
<borders count="1"><border><left/><right/><top/><bottom/><diagonal/></border></borders>
<cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>
<cellXfs count="5">
<xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/>
<xf numFmtId="0" fontId="1" fillId="2" borderId="0" xfId="0" applyFont="1" applyFill="1"/>
<xf numFmtId="164" fontId="0" fillId="0" borderId="0" xfId="0" applyNumberFormat="1"/>
<xf numFmtId="14" fontId="0" fillId="0" borderId="0" xfId="0" applyNumberFormat="1"/>
<xf numFmtId="165" fontId="0" fillId="0" borderId="0" xfId="0" applyNumberFormat="1"/>
</cellXfs><cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles></styleSheet>`;

  const nomF=(S.titre||'Données').slice(0,28).replace(/[\\\/\?\*\[\]:]/g,' ');
  const F=[
   {nom:'[Content_Types].xml', data:_octets(`<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
<Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
<Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>
</Types>`)},
   {nom:'_rels/.rels', data:_octets(`<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/></Relationships>`)},
   {nom:'xl/workbook.xml', data:_octets(`<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
<sheets><sheet name="${_xe(nomF)}" sheetId="1" r:id="rId1"/></sheets></workbook>`)},
   {nom:'xl/_rels/workbook.xml.rels', data:_octets(`<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>
<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/></Relationships>`)},
   {nom:'xl/styles.xml', data:_octets(styles)},
   {nom:'xl/worksheets/sheet1.xml', data:_octets(feuille)}
  ];
  _telecharge(_zip(F), (S.fichier||'donnees')+'-'+ajd()+'.xlsx');
}

function sortieCsv(S){
  const C=S.colonnes||[], L=S.lignes||[];
  const g=x=>'"'+String(x==null?'':x).replace(/"/g,'""')+'"';
  /* virgule décimale et point-virgule : c'est ce qu'attend un Excel réglé en français */
  const nb=(v,y)=>(y==='n'||y==='m'||y==='p')&&v!=null&&v!==''&&isFinite(Number(v))
    ? String(Number(v)).replace('.',',') : g(v);
  const li=[C.map(c=>g(c.t)).join(';')];
  L.forEach(x=>li.push(C.map((c,j)=>nb(x[j],c.y)).join(';')));
  _telecharge(new Blob(['﻿'+li.join('\r\n')],{type:'text/csv;charset=utf-8'}),
    (S.fichier||'donnees')+'-'+ajd()+'.csv');
}

function _telecharge(blob,nom){
  const a=document.createElement('a'); a.href=URL.createObjectURL(blob); a.download=nom;
  document.body.appendChild(a); a.click(); a.remove();
  setTimeout(()=>URL.revokeObjectURL(a.href),4000);
}

/* --------- le PDF : on prépare la page, le navigateur fabrique le fichier --------- */
function sortieImprime(S){
  const C=S.colonnes||[], L=S.lignes||[];
  const fr=v=>Number(v||0).toLocaleString('fr-FR',{minimumFractionDigits:2,maximumFractionDigits:2});
  const cel=(v,y)=>{
    if(v==null||v==='') return '—';
    if(y==='m') return fr(v)+' $';
    if(y==='p') return Number(v).toFixed(1).replace('.',',')+' %';
    if(y==='n') return Number(v).toLocaleString('fr-FR');
    if(y==='d'){ const m=String(v).match(/^(\d{4})-(\d{2})-(\d{2})/);
                 return m?`${m[2]}/${m[3]}/${m[1].slice(2)}`:String(v); }
    return String(v);
  };
  const dr=y=>(y==='n'||y==='m'||y==='p')?' class="r"':'';
  /* un total par colonne chiffrée : c'est la première chose qu'on cherche sur un papier */
  const tot=C.map(c=>(c.y==='m'||c.y==='n')?L.reduce((a,x,i)=>{
      const n=Number(x[C.indexOf(c)]); return a+(isFinite(n)?n:0); },0):null);
  const aTot=tot.some(t=>t!=null);

  let z=document.getElementById('imprzone');
  if(!z){ z=document.createElement('div'); z.id='imprzone'; document.body.appendChild(z); }
  const d=new Date();
  z.innerHTML=`<div class="imprtete">
      <h2>${esc(S.titre||'')}</h2>
      <p>${esc(S.filtre||'tout')}</p>
      <p>Perfumes Trade · ${nf(L.length)} ligne${L.length>1?'s':''} · édité le ${
        String(d.getDate()).padStart(2,'0')}/${String(d.getMonth()+1).padStart(2,'0')}/${d.getFullYear()} à ${
        String(d.getHours()).padStart(2,'0')}h${String(d.getMinutes()).padStart(2,'0')}</p>
    </div>
    <table><thead><tr>${C.map(c=>`<th${dr(c.y)}>${esc(c.t)}</th>`).join('')}</tr></thead>
    <tbody>${L.map(x=>`<tr>${C.map((c,j)=>`<td${dr(c.y)}>${esc(cel(x[j],c.y))}</td>`).join('')}</tr>`).join('')}</tbody>
    ${aTot?`<tfoot><tr>${C.map((c,j)=>`<td${dr(c.y)}>${tot[j]==null?(j===0?'Total':''):esc(cel(tot[j],c.y))}</td>`).join('')}</tr></tfoot>`:''}
    </table>`;
  document.body.classList.add('impr-tab');
  const fin=()=>document.body.classList.remove('impr-tab');
  window.addEventListener('afterprint',fin,{once:true});
  setTimeout(()=>{ window.print(); setTimeout(fin,1500); },60);
}

/* --------- le bouton --------- */
function poseSortie(id, obtenir){
  const el=document.getElementById(id); if(!el) return;
  el.outerHTML=`<details class="sbar" id="${id}">
    <summary>Exporter</summary>
    <div class="smenu">
      <button data-s="x"><b>Excel (.xlsx)</b><span>vrai fichier Excel : colonnes séparées, montants calculables</span></button>
      <button data-s="p"><b>PDF (impression)</b><span>ouvre la fenêtre d'impression — choisis « Enregistrer en PDF »</span></button>
      <button data-s="c"><b>CSV</b><span>pour un autre logiciel ; Excel l'ouvre moins bien</span></button>
      <div class="squoi" data-quoi></div>
    </div></details>`;
  const d=document.getElementById(id);
  d.addEventListener('toggle',()=>{ if(!d.open) return;
    let S=null; try{ S=obtenir(); }catch(e){}
    d.querySelector('[data-quoi]').textContent = S
      ? `Ce qui sortira : ${nf((S.lignes||[]).length)} ligne${(S.lignes||[]).length>1?'s':''} — ${S.filtre||'tout'}.`
      : '';
  });
  d.querySelector('.smenu').addEventListener('click',e=>{
    const b=e.target.closest('[data-s]'); if(!b) return;
    d.open=false;
    const S=obtenir(); if(!S) return;
    if(!(S.lignes||[]).length){ alert("Il n'y a rien à exporter : le filtre affiché ne laisse aucune ligne."); return; }
    if(b.dataset.s==='x') sortieXlsx(S);
    else if(b.dataset.s==='p') sortieImprime(S);
    else sortieCsv(S);
  });
  /* un clic ailleurs referme le menu */
  document.addEventListener('click',e=>{ if(d.open && !d.contains(e.target)) d.open=false; });
}
"""
