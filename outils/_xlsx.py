# -*- coding: utf-8 -*-
"""Lire un fichier Excel (.xlsx) dans le navigateur, sans rien installer.

Pourquoi ce fichier existe : Sam travaille dans Google Sheets et sur Excel.
Lui demander « Fichier → Télécharger → CSV » avant chaque import, c'est une
étape de plus à rater, et c'est exactement là qu'il a buté.

Comment ça marche : un .xlsx est un fichier ZIP qui contient du XML. Le
navigateur sait décompresser tout seul depuis quelques années
(DecompressionStream), donc on ouvre le ZIP à la main, on lit deux ou trois
fichiers dedans, et on rend un tableau de lignes. Pas de bibliothèque à
charger depuis internet : les pages de Perfumes Trade s'ouvrent aussi hors
ligne, et une page qui dépend d'un serveur extérieur pour lire un fichier
local, c'est une panne qui attend son jour.

Ce qui est traité, parce que ça arrive pour de vrai dans les fichiers de Sam :
— plusieurs onglets (son Google Sheet en a) : on les propose, il choisit ;
— les dates, qui dans Excel sont des nombres (45 900 = une date) : on lit le
  format de la cellule pour savoir s'il faut les retraduire ;
— les cellules vides au milieu d'une ligne, qui décaleraient les colonnes ;
— les formules : on prend le résultat affiché, pas la formule.
"""

XLSX = r"""
/* ============ LIRE UN FICHIER EXCEL ============ */
const xlsxDispo = (typeof DecompressionStream!=='undefined');

async function xlDegonfle(u8, methode){
  if(methode===0) return u8;                     /* rangé tel quel dans le zip */
  const flux=new Blob([u8]).stream().pipeThrough(new DecompressionStream('deflate-raw'));
  return new Uint8Array(await new Response(flux).arrayBuffer());
}

/* Ouvre le ZIP : on lit son sommaire (à la fin du fichier), pas octet par octet. */
async function xlOuvre(buf){
  const v=new DataView(buf), u=new Uint8Array(buf);
  let fin=-1;
  for(let i=u.length-22; i>=Math.max(0,u.length-65557); i--){
    if(v.getUint32(i,true)===0x06054b50){ fin=i; break; }
  }
  if(fin<0) throw new Error("Ce fichier n'est pas un .xlsx lisible.");
  const nb=v.getUint16(fin+10,true);
  let p=v.getUint32(fin+16,true);
  const dec=new TextDecoder();
  const fichiers={};
  for(let k=0;k<nb;k++){
    if(v.getUint32(p,true)!==0x02014b50) break;
    const meth=v.getUint16(p+10,true);
    const taille=v.getUint32(p+20,true);
    const nl=v.getUint16(p+28,true), el=v.getUint16(p+30,true), cl=v.getUint16(p+32,true);
    const loc=v.getUint32(p+42,true);
    const nom=dec.decode(u.subarray(p+46,p+46+nl));
    fichiers[nom]={meth, taille, loc};
    p+=46+nl+el+cl;
  }
  return {
    a:n=>!!fichiers[n],
    lis: async n=>{
      const f=fichiers[n]; if(!f) return null;
      const nl=v.getUint16(f.loc+26,true), el=v.getUint16(f.loc+28,true);
      const d=f.loc+30+nl+el;
      return dec.decode(await xlDegonfle(u.subarray(d, d+f.taille), f.meth));
    },
    noms:Object.keys(fichiers)
  };
}

const xlDom=t=>new DOMParser().parseFromString(t,'application/xml');

/* Une lettre de colonne (A, B, … AA) vers un numéro. */
function xlCol(ref){
  let n=0;
  for(const c of String(ref).replace(/[0-9]/g,'')) n=n*26+(c.charCodeAt(0)-64);
  return n-1;
}

/* Excel range les dates en nombre de jours depuis le 30 décembre 1899. */
function xlDate(n){
  const d=new Date(Date.UTC(1899,11,30)+Math.round(n)*86400000);
  if(isNaN(d)) return String(n);
  const p=x=>String(x).padStart(2,'0');
  return d.getUTCFullYear()+'-'+p(d.getUTCMonth()+1)+'-'+p(d.getUTCDate());
}

/* Quels styles de cellule veulent dire « date » : les formats intégrés d'Excel,
   plus les formats sur mesure qui contiennent des jours ou des mois. */
function xlStylesDate(xml){
  if(!xml) return {};
  const d=xlDom(xml), perso={};
  [...d.getElementsByTagName('numFmt')].forEach(f=>{
    const code=f.getAttribute('formatCode')||'';
    if(/[dmy]/i.test(code) && !/[#0]/.test(code.replace(/\[[^\]]*\]/g,'')))
      perso[f.getAttribute('numFmtId')]=1;
  });
  const INT={14:1,15:1,16:1,17:1,18:1,19:1,20:1,21:1,22:1,45:1,46:1,47:1};
  const xfs=d.getElementsByTagName('cellXfs')[0];
  const out={};
  if(xfs) [...xfs.getElementsByTagName('xf')].forEach((x,i)=>{
    const id=x.getAttribute('numFmtId');
    if(INT[id]||perso[id]) out[i]=1;
  });
  return out;
}

/* Rend { onglets:[{nom, lignes:[[cellules…]]}] } */
async function xlLis(buf){
  const z=await xlOuvre(buf);

  /* les textes sont mis en commun dans un fichier à part */
  const partages=[];
  const ss=await z.lis('xl/sharedStrings.xml');
  if(ss) [...xlDom(ss).getElementsByTagName('si')].forEach(si=>{
    partages.push([...si.getElementsByTagName('t')].map(t=>t.textContent).join(''));
  });

  const dates=xlStylesDate(await z.lis('xl/styles.xml'));

  /* le nom des onglets et le fichier qui va avec */
  const wb=await z.lis('xl/workbook.xml');
  const rel=await z.lis('xl/_rels/workbook.xml.rels');
  const cible={};
  if(rel) [...xlDom(rel).getElementsByTagName('Relationship')].forEach(r=>{
    cible[r.getAttribute('Id')]=r.getAttribute('Target');
  });
  let feuilles=[];
  if(wb) [...xlDom(wb).getElementsByTagName('sheet')].forEach(s=>{
    const id=s.getAttribute('r:id')||s.getAttributeNS('http://schemas.openxmlformats.org/officeDocument/2006/relationships','id');
    let t=cible[id]||'';
    if(t && !t.startsWith('xl/')) t='xl/'+t.replace(/^\/?xl\//,'').replace(/^\//,'');
    feuilles.push({nom:s.getAttribute('name')||'Feuille', fichier:t});
  });
  if(!feuilles.length)
    feuilles=z.noms.filter(n=>/^xl\/worksheets\/sheet\d+\.xml$/.test(n))
                   .map((n,i)=>({nom:'Feuille '+(i+1), fichier:n}));

  const onglets=[];
  for(const f of feuilles){
    const xml=await z.lis(f.fichier);
    if(!xml) continue;
    const d=xlDom(xml), lignes=[];
    [...d.getElementsByTagName('row')].forEach(r=>{
      const L=[];
      [...r.getElementsByTagName('c')].forEach(c=>{
        const i=xlCol(c.getAttribute('r')||'A1');
        while(L.length<i) L.push('');
        const t=c.getAttribute('t');
        let val='';
        if(t==='inlineStr'){
          val=[...c.getElementsByTagName('t')].map(x=>x.textContent).join('');
        } else {
          const v=c.getElementsByTagName('v')[0];
          const brut=v?v.textContent:'';
          if(t==='s')      val=partages[+brut]!==undefined?partages[+brut]:'';
          else if(t==='b') val=(brut==='1')?'TRUE':'FALSE';
          else if(t==='e') val='';                       /* #N/A, #REF!… */
          else if(brut!=='' && dates[+(c.getAttribute('s')||-1)] && !isNaN(+brut))
                           val=xlDate(+brut);
          else             val=brut;
        }
        L.push(val);
      });
      lignes.push(L);
    });
    /* on jette les lignes entièrement vides de la fin */
    while(lignes.length && !lignes[lignes.length-1].join('').trim()) lignes.pop();
    onglets.push({nom:f.nom, lignes});
  }
  return {onglets};
}

/* Le fichier déposé : Excel ou texte, on rend toujours la même chose. */
const xlEstExcel=f=>/\.(xlsx|xlsm)$/i.test(f.name||'');
"""

CSS = """
.xlong{display:flex;flex-wrap:wrap;gap:7px;margin-top:13px;align-items:center}
.xlong .lab{font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--ink-3);
 font-weight:700;margin-right:3px}
.xlb{padding:6px 12px;font-family:inherit;font-size:13px;border:1px solid var(--line);
 border-radius:20px;background:var(--surface);color:var(--ink-2);cursor:pointer}
.xlb:hover{border-color:var(--iris);color:var(--iris)}
.xlb.on{background:var(--iris);border-color:var(--iris);color:#fff;font-weight:600}
"""
