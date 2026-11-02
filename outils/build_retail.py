# -*- coding: utf-8 -*-
"""La rubrique Retail : les clients du site perfumestrade.com et de la boutique.

Ce sont les clients au détail, par opposition à « VIP wholesale » qui tient les
gros comptes revendeurs. Deux populations qui n'ont rien à voir : ici, beaucoup
de monde, de petits paniers, et une adresse email qui sert surtout à relancer
et à envoyer des promos.

D'où viendront les lignes : d'un export du site (WooCommerce sait sortir un CSV
de ses clients). Tant que le serveur n'est pas là, personne ne va les chercher
tout seul — c'est l'import de fichier de cette page qui les fait entrer. Le jour
où il y a un serveur, ce même tableau se remplit tout seul et l'import reste
pour les cas particuliers.

Deux affichages parce que les deux servent : la liste pour travailler (trier,
comparer, relancer), les vignettes pour regarder qui sont ses clients.
"""
import os, json
from build_crm import coquille
import _donnees
import _lire

# Le fichier de données part vide : c'est Sam qui le remplira, par import.
if not os.path.exists('donnees/retail.js'):
    _donnees.pose('retail', [], 'D_RETAIL')

CSS = """
.bandeau{background:var(--iris-soft);border-left:3px solid var(--iris);border-radius:0 9px 9px 0;
 padding:14px 17px;font-size:13.5px;color:var(--ink-2);line-height:1.62;margin:0 0 22px;max-width:88ch}
.bandeau b{color:var(--ink)}

.barre{display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin-bottom:18px}
.rech{flex:1;min-width:230px;position:relative}
.rech input{width:100%;padding:11px 14px 11px 34px;font-family:inherit;font-size:14px;
 border:1px solid var(--line);border-radius:9px;background:var(--surface);color:var(--ink)}
.rech span{position:absolute;left:12px;top:50%;transform:translateY(-50%);color:var(--ink-3);font-size:13px}
select.tri{padding:11px 12px;font-family:inherit;font-size:13.5px;border:1px solid var(--line);
 border-radius:9px;background:var(--surface);color:var(--ink)}
.vue{display:flex;border:1px solid var(--line);border-radius:9px;overflow:hidden}
.vue button{padding:11px 15px;font-family:inherit;font-size:13.5px;border:0;background:var(--surface);
 color:var(--ink-3);cursor:pointer}
.vue button+button{border-left:1px solid var(--line)}
.vue button.on{background:var(--iris);color:#fff;font-weight:600}

.tw{border:1px solid var(--line);border-radius:10px;overflow:hidden;background:var(--surface)}
table.t{width:100%;border-collapse:collapse;font-size:13.5px}
.t th{background:var(--surface-2);color:var(--ink-3);font-size:9.5px;letter-spacing:.11em;
 text-transform:uppercase;text-align:left;padding:10px 13px;border-bottom:1px solid var(--line);
 font-weight:700;white-space:nowrap}
.t th.n,.t td.n{text-align:right}
.t td{padding:12px 13px;border-bottom:1px solid var(--line-2);vertical-align:middle;color:var(--ink-2)}
.t tr:last-child td{border-bottom:0}
.t tr:hover td{background:var(--surface-2)}
.qui b{display:block;color:var(--ink);font-size:14.5px;font-weight:600;line-height:1.3}
.qui span{display:block;font-size:11.5px;color:var(--ink-3)}
.co{font-size:12.5px;line-height:1.5}
.co i{font-style:normal;display:block;color:var(--ink-3)}
.co i.vide{color:var(--warn)}
.gros{font-size:16px;font-weight:700;font-variant-numeric:tabular-nums;color:var(--ink)}
.qd{font-size:12.5px;color:var(--ink-3);white-space:nowrap}
.act{text-align:right;white-space:nowrap}

.vig{display:grid;grid-template-columns:repeat(auto-fill,minmax(252px,1fr));gap:14px}
.cv{border:1px solid var(--line);border-radius:12px;background:var(--surface);padding:16px 17px;
 display:flex;flex-direction:column;gap:9px}
.cv .h{display:flex;gap:11px;align-items:center}
.pastille{flex:none;width:40px;height:40px;border-radius:50%;background:var(--iris-soft);
 color:var(--iris);display:flex;align-items:center;justify-content:center;
 font-size:15px;font-weight:700;letter-spacing:-.01em}
.cv .h b{font-size:14.5px;font-weight:700;color:var(--ink);line-height:1.25;display:block}
.cv .h em{font-style:normal;font-size:11.5px;color:var(--ink-3)}
.cv .ch{display:flex;gap:16px;padding:9px 0;border-top:1px solid var(--line-2);
 border-bottom:1px solid var(--line-2)}
.cv .ch div{display:flex;flex-direction:column;gap:2px}
.cv .ch u{text-decoration:none;font-size:9.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--ink-3);font-weight:700}
.cv .ch b{font-size:16px;font-weight:700;color:var(--ink);font-variant-numeric:tabular-nums}
.cv .der{font-size:12.5px;color:var(--ink-2);line-height:1.5}
.cv .der b{color:var(--ink)}
.cv .pied{display:flex;gap:10px;align-items:center;margin-top:auto;padding-top:4px}

.rien{border:1px dashed var(--line);border-radius:12px;background:var(--surface);
 padding:38px 34px;text-align:center;max-width:70ch;margin:8px auto}
.rien h3{margin:0 0 10px;font-size:17px;font-weight:700}
.rien p{margin:0 0 8px;font-size:14px;color:var(--ink-2);line-height:1.65}
.rien .btn{margin-top:14px}

.impban{background:var(--good-soft);border-left:3px solid var(--good);border-radius:0 9px 9px 0;
 padding:12px 16px;font-size:13px;color:var(--ink-2);margin:0 0 18px;line-height:1.55}
.impban button{background:none;border:0;padding:0;font-family:inherit;font-size:13px;
 color:var(--ink-3);text-decoration:underline;cursor:pointer}
.impban button:hover{color:var(--iris)}
.prev{max-height:250px;overflow:auto;border:1px solid var(--line);border-radius:8px;margin-top:13px}
.prev table{width:100%;border-collapse:collapse;font-size:12.5px}
.prev th{position:sticky;top:0;background:var(--surface-2);text-align:left;padding:8px 10px;
 border-bottom:1px solid var(--line);font-size:9.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--ink-3)}
.prev td{padding:7px 10px;border-bottom:1px solid var(--line-2);color:var(--ink-2)}
.hint{font-size:12.5px;color:var(--ink-3);line-height:1.6;margin:10px 0 0}
.msg{font-size:13px;font-weight:600}
.msg.err{color:var(--crit)} .msg.ok{color:var(--good)}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:1px;
 background:var(--line);border:1px solid var(--line);border-radius:10px;overflow:hidden;margin-bottom:22px}
.stat{background:var(--surface);padding:14px 16px;display:flex;flex-direction:column;gap:4px}
.stat .n{font-size:23px;font-weight:700;letter-spacing:-.02em;color:var(--ink)}
.stat .l{font-size:11.5px;color:var(--ink-3);line-height:1.4}
"""

CORPS = """
<div class="bandeau">
  <b>Les clients au détail.</b> Ceux du site perfumestrade.com et du comptoir — par opposition à
  <b>VIP wholesale</b>, qui tient les gros comptes revendeurs. Chaque fiche garde l'email, le
  téléphone, ce qui a été acheté et quand, pour pouvoir écrire à la personne en deux clics.
  Tant qu'il n'y a pas de serveur, les nouveaux clients du site n'arrivent pas tout seuls :
  c'est <b>Importer un fichier</b> qui les fait entrer.
</div>

<div id="impban" class="impban" hidden></div>
<div class="stats" id="stats" hidden></div>
<div class="info" id="bansite" hidden style="border-left-color:var(--iris)"></div>

<div class="barre">
  <div class="rech"><span>⌕</span><input id="q" autocomplete="off" placeholder="Chercher un nom, un email, une ville…"></div>
  <select class="tri" id="tri">
    <option value="der">Dernier achat</option>
    <option value="total">Total dépensé</option>
    <option value="nb">Nombre de commandes</option>
    <option value="nom">Nom</option>
  </select>
  <div class="vue"><button id="v-liste" class="on">Liste</button><button id="v-vig">Vignettes</button></div>
  <button class="btn" id="imp">Importer un fichier</button>
</div>

<div id="zone"></div>

<div class="ov" id="impov"><div class="mod" style="max-width:760px;max-height:88vh;display:flex;flex-direction:column">
  <div class="mh"><h2>Importer les clients du site</h2><button class="x" id="impx">&times;</button></div>
  <div class="mb" style="overflow:auto;flex:1;min-height:0">
    <p class="hint" style="margin-top:0">Un fichier <b>Excel (.xlsx)</b> ou <b>CSV</b>.
    La première ligne donne les titres de colonnes. Sont reconnus :
    <b>nom</b> (ou prénom + nom), <b>email</b>, <b>téléphone</b>, <b>ville</b>, <b>pays</b>,
    <b>nombre de commandes</b>, <b>total dépensé</b>, <b>dernier achat</b>.
    Seul le nom ou l'email est obligatoire ; tout le reste peut manquer.</p>
    <input type="file" id="impfile" accept="__ACCEPT_TAB__" style="font-size:12.5px;margin-top:12px">
    <div class="xlong" id="imponglets" hidden></div>
    <textarea id="imptxt" placeholder="…ou colle ici les lignes du tableur"
      style="width:100%;margin-top:11px;min-height:96px;padding:10px 12px;font-family:inherit;
      font-size:13px;border:1px solid var(--line);border-radius:8px;background:var(--surface);
      color:var(--ink);resize:vertical"></textarea>
    <div id="impres"></div>
    <label class="chk" id="impremp-l" style="display:flex;gap:9px;align-items:center;margin-top:13px;
      font-size:13.5px;color:var(--ink-2);cursor:pointer">
      <input type="checkbox" id="impremp" checked> Remplacer la liste entière par ce fichier
      <span style="color:var(--ink-3)">(sinon, les fiches sont mises à jour et les nouvelles ajoutées)</span></label>
  </div>
  <div class="mf" style="flex:none"><span class="msg" id="impmsg"></span>
    <button class="btn" id="impann">Annuler</button>
    <button class="btn pri" id="impok" disabled>Mettre les clients à jour</button></div>
</div></div>
"""

JS = r"""
const K_LOCAL='retail-local-v1';
const K_VUE  ='retail-vue-v1';

/* Les fiches : celles du fichier de données, remplacées par celles d'un import
   si Sam en a fait un. Les corrections faites à la main (email, téléphone)
   vivent dans la même liste : elles sont réécrites au même endroit. */
function base(){
  let t=null; try{ t=localStorage.getItem(K_LOCAL); }catch(e){}
  if(t){ try{ const L=JSON.parse(t); if(Array.isArray(L)) return L; }catch(e){} }
  return Array.isArray(window.D_RETAIL) ? window.D_RETAIL.slice() : [];
}
/* On passe par ecrit() et pas par localStorage : sans ça, un email corrigé ici
   restait sur ce navigateur et personne d'autre ne le voyait. */
function garde(L){ try{ ecrit(K_LOCAL,L); }catch(e){
  alert("Le navigateur refuse d'enregistrer : la liste est trop grosse pour lui."); } }
let R=base();

function jlogContact(nom,par,quoi){
  const s=session(); const J=lit('crm-journal-v1',[]);
  J.push({t:new Date().toISOString(),u:s?s.nom:'?',act:'contact',
          lib:'message préparé — '+quoi,ref:nom,av:null,ap:par});
  ecrit('crm-journal-v1',J);
}

const jour=v=>{ if(!v) return null; const d=new Date(v); return isNaN(d)?null:d; };
const dfr=v=>{ const d=jour(v); return d?d.toLocaleDateString('en-US',
  {day:'2-digit',month:'2-digit',year:'2-digit'}):'—'; };
const ini=n=>String(n||'?').trim().split(/\s+/).slice(0,2)
  .map(m=>m[0]||'').join('').toUpperCase()||'?';

let VUE = (()=>{ try{ return localStorage.getItem(K_VUE)==='vig'?'vig':'liste'; }catch(e){ return 'liste'; } })();

function filtre(){
  const q=$('q').value.trim().toLowerCase();
  let L=R.filter(c=>!q || [c.nom,c.email,c.ville,c.tel].some(v=>String(v||'').toLowerCase().includes(q)));
  const t=$('tri').value;
  L.sort((a,b)=>{
    if(t==='nom')   return String(a.nom||'').localeCompare(String(b.nom||''),'fr');
    if(t==='total') return (b.total||0)-(a.total||0);
    if(t==='nb')    return (b.nb||0)-(a.nb||0);
    const da=jour(a.der), db=jour(b.der);
    return (db?db.getTime():0)-(da?da.getTime():0);
  });
  return L;
}

/* Écrire à quelqu'un : la fenêtre est la même partout, on lui passe juste
   de quoi recoller l'email corrigé sur la bonne fiche. */
function ecrire(i,modele){
  const c=R[i]; if(!c) return;
  contacte({nom:c.nom, email:c.email, tel:c.tel, modele:modele||'promo',
    onSave:(mail,tel)=>{
      if(mail===c.email && tel===c.tel) return;
      c.email=mail; c.tel=tel; garde(R); peint();
    }});
}

function peint(){
  const L=filtre(), z=$('zone');
  if(!R.length){
    $('stats').hidden=true;
    z.innerHTML=`<div class="rien"><h3>Aucun client au détail pour l'instant</h3>
      <p>C'est normal : rien n'a encore été importé. Les clients du site n'arriveront tout seuls
      que le jour où Perfumes Trade tournera sur un serveur relié à perfumestrade.com.</p>
      <p>En attendant, demande à Sam un export des clients du site — WooCommerce sait le sortir
      en CSV — et charge-le ici.</p>
      <button class="btn pri" id="imp2">Importer un fichier</button></div>`;
    const b=$('imp2'); if(b) b.onclick=()=>$('impov').classList.add('on');
    $('src').innerHTML='aucun client';
    return;
  }
  const tot=R.reduce((s,c)=>s+(c.total||0),0);
  const cmd=R.reduce((s,c)=>s+(c.nb||0),0);
  const sansMail=R.filter(c=>!c.email).length;
  const duSite=R.filter(c=>c.src==='site').length;
  $('stats').hidden=false;
  $('stats').innerHTML=`
    <div class="stat"><span class="n">${nf(R.length)}</span><span class="l">clients au détail</span></div>
    <div class="stat"><span class="n">${money(tot)}</span><span class="l">acheté au total</span></div>
    <div class="stat"><span class="n">${nf(cmd)}</span><span class="l">commandes</span></div>
    <div class="stat"><span class="n">${money(R.length?tot/R.length:0)}</span><span class="l">par client en moyenne</span></div>
    <div class="stat"><span class="n">${nf(sansMail)}</span><span class="l">sans email — impossible à relancer</span></div>`;
  const b=$('bansite');
  if(b){
    if(duSite){
      b.hidden=false;
      b.innerHTML=`<b>${nf(duSite)} fiche${duSite>1?'s':''} ${duSite>1?'viennent':'vient'} du site</b>,
        remontée${duSite>1?'s':''} toutes seules depuis perfumestrade.com — un nouvel inscrit apparaît ici sans que personne le saisisse.
        Les colonnes <b>commandes</b>, <b>total</b> et <b>dernier achat</b> restent vides pour elles :
        le site ne donne pas ces chiffres avec les fiches, et les reconstituer à moitié afficherait
        un total de vie qui n'en est pas un. Ils se rempliront depuis les ventes que l'outil enregistre.
        Une correction faite ici (email, téléphone) n'est jamais écrasée par le site.`;
    } else b.hidden=true;
  }

  if(!L.length){
    z.innerHTML=`<div class="rien"><h3>Personne ne correspond</h3>
      <p>Aucun des ${nf(R.length)} clients ne contient « ${esc($('q').value.trim())} ».</p></div>`;
    $('src').innerHTML=nf(R.length)+' clients';
    return;
  }
  z.innerHTML = VUE==='vig' ? vignettes(L) : liste(L);
  $('src').innerHTML=(L.length===R.length?nf(R.length)+' clients'
    :nf(L.length)+' sur '+nf(R.length))+'<br>détail';
}

function liste(L){
  return `<div class="tw"><table class="t"><thead><tr>
    <th>Client</th><th>Coordonnées</th><th class="n">Commandes</th><th class="n">Total</th>
    <th>Dernier achat</th><th></th></tr></thead><tbody>`
   +L.map(c=>{ const i=R.indexOf(c); return `<tr>
      <td class="qui"><b>${esc(c.nom||'Sans nom')}</b>
        <span>${esc([c.ville,c.pays].filter(Boolean).join(', ')||'—')}</span></td>
      <td class="co">
        <i class="${c.email?'':'vide'}">${esc(c.email||'pas d\'email')}</i>
        <i class="${c.tel?'':'vide'}">${esc(c.tel||'pas de téléphone')}</i></td>
      <td class="n"><span class="gros">${nf(c.nb||0)}</span></td>
      <td class="n"><span class="gros">${money(c.total||0)}</span></td>
      <td class="qd">${dfr(c.der)}${c.derArt?'<br><span style="color:var(--ink-2)">'+esc(c.derArt)+'</span>':''}</td>
      <td class="act"><button class="ecr" data-e="${i}">Écrire</button></td></tr>`; }).join('')
   +'</tbody></table></div>';
}

function vignettes(L){
  return '<div class="vig">'+L.map(c=>{ const i=R.indexOf(c); return `<div class="cv">
      <div class="h"><div class="pastille">${esc(ini(c.nom))}</div>
        <div><b>${esc(c.nom||'Sans nom')}</b>
          <em>${esc([c.ville,c.pays].filter(Boolean).join(', ')||'—')}</em></div></div>
      <div class="ch">
        <div><u>Commandes</u><b>${nf(c.nb||0)}</b></div>
        <div><u>Total</u><b>${money(c.total||0)}</b></div></div>
      <div class="der">Dernier achat <b>${dfr(c.der)}</b>${c.derArt?'<br>'+esc(c.derArt):''}</div>
      <div class="der" style="color:var(--ink-3)">${esc(c.email||'pas d\'email')}<br>${esc(c.tel||'pas de téléphone')}</div>
      <div class="pied"><button class="ecr" data-e="${i}">Écrire</button>
        <button class="ecr" data-p="${i}">Envoyer une promo</button></div>
    </div>`; }).join('')+'</div>';
}

$('zone').addEventListener('click',e=>{
  const b=e.target.closest('button'); if(!b) return;
  if(b.dataset.e!==undefined) return ecrire(+b.dataset.e,'promo');
  if(b.dataset.p!==undefined) return ecrire(+b.dataset.p,'promo');
});
$('q').oninput=peint;
$('tri').onchange=peint;
const vue=v=>{ VUE=v; try{ localStorage.setItem(K_VUE,v); }catch(e){}
  $('v-liste').classList.toggle('on',v==='liste');
  $('v-vig').classList.toggle('on',v==='vig'); peint(); };
$('v-liste').onclick=()=>vue('liste');
$('v-vig').onclick=()=>vue('vig');
vue(VUE);

/* ---------- l'import ---------- */
let IMP=null;
const impNorm=s=>String(s||'').toLowerCase()
  .normalize('NFD').replace(/[̀-ͯ]/g,'').replace(/[^a-z0-9]/g,'');
const IMP_COLS={
  nom:['nom','name','client','customer','fullname','nomcomplet','billingname'],
  prenom:['prenom','firstname','billingfirstname','givenname'],
  famille:['nomdefamille','lastname','billinglastname','surname','familyname'],
  email:['email','mail','adresseemail','courriel','billingemail','emailaddress'],
  tel:['telephone','tel','phone','mobile','whatsapp','billingphone','phonenumber'],
  ville:['ville','city','billingcity','localite'],
  pays:['pays','country','billingcountry'],
  nb:['commandes','nbcommandes','orders','ordercount','nombredecommandes'],
  total:['total','totaldepense','totalspent','montant','ca','lifetimevalue','totalorders'],
  der:['dernierachat','derniercommande','lastorder','lastorderdate','datedernierachat','lastpurchase','date'],
  derArt:['dernierproduit','lastproduct','produit','article','derniersarticles']};

function impDecoupe(t){
  const l=t.split(/\r?\n/).filter(x=>x.trim());
  if(!l.length) return [];
  const sep = (l[0].match(/\t/g)||[]).length ? '\t'
            : (l[0].match(/;/g)||[]).length >= (l[0].match(/,/g)||[]).length ? ';' : ',';
  const coupe=ligne=>{
    const out=[]; let cur='', dans=false;
    for(let i=0;i<ligne.length;i++){ const c=ligne[i];
      if(c==='"'){ if(dans&&ligne[i+1]==='"'){ cur+='"'; i++; } else dans=!dans; }
      else if(c===sep && !dans){ out.push(cur); cur=''; }
      else cur+=c; }
    out.push(cur); return out.map(x=>x.trim());
  };
  return l.map(coupe);
}

function impAnalyse(t){
  const L=Array.isArray(t)?t:impDecoupe(t);
  if(L.length<2) return {err:'Il faut au moins une ligne de titres et une ligne de client.'};
  const tetes=L[0].map(impNorm), idx={};
  for(const [k,noms] of Object.entries(IMP_COLS)){
    idx[k]=tetes.findIndex(h=>noms.includes(h));
    if(idx[k]<0) idx[k]=tetes.findIndex(h=>h&&noms.some(n=>h.startsWith(n)||n.startsWith(h)));
  }
  if(idx.nom<0 && idx.prenom<0 && idx.email<0)
    return {err:"Aucune colonne de nom ni d'email reconnue dans la première ligne. "
      +"Les titres attendus : nom (ou prénom + nom), email, téléphone, ville, commandes, total, dernier achat."};
  const nb=v=>{ const x=String(v==null?'':v).replace(/[^0-9.,-]/g,'').replace(/\s/g,'');
    if(!x) return null;
    const p=x.lastIndexOf('.'), c=x.lastIndexOf(',');
    const y = c>p ? x.replace(/\./g,'').replace(',','.') : x.replace(/,/g,'');
    const n=parseFloat(y); return isFinite(n)?n:null; };
  const g=(r,k)=>idx[k]>=0?String(r[idx[k]]||'').trim():'';
  const lignes=[], vides=[];
  for(let i=1;i<L.length;i++){
    const r=L[i]; if(!r.join('').trim()) continue;
    let nom=g(r,'nom');
    if(!nom) nom=[g(r,'prenom'),g(r,'famille')].filter(Boolean).join(' ').trim();
    const email=g(r,'email');
    if(!nom && !email){ vides.push(i+1); continue; }
    lignes.push({nom: nom||email, email, tel:g(r,'tel'), ville:g(r,'ville'), pays:g(r,'pays'),
      nb: idx.nb>=0?(nb(r[idx.nb])||0):0,
      total: idx.total>=0?(nb(r[idx.total])||0):0,
      der: g(r,'der'), derArt: g(r,'derArt')});
  }
  if(!lignes.length) return {err:'Aucune ligne exploitable : chaque ligne doit avoir un nom ou un email.'};
  return {lignes, vides, tetes:L[0]};
}

function impPeint(a){
  const el=$('impres');
  if(a.err){ el.innerHTML=`<p class="hint" style="color:var(--crit)"><b>${esc(a.err)}</b></p>`;
    $('impok').disabled=true; IMP=null; return; }
  IMP=a;
  const connus={}; R.forEach(c=>{ if(c.email) connus[String(c.email).toLowerCase()]=1; });
  const dej=a.lignes.filter(l=>l.email&&connus[l.email.toLowerCase()]).length;
  const sansMail=a.lignes.filter(l=>!l.email).length;
  el.innerHTML=`<div class="prev"><table><thead><tr><th>Nom</th><th>Email</th><th>Téléphone</th>
      <th>Ville</th><th>Commandes</th><th>Total</th><th>Dernier achat</th></tr></thead><tbody>`
    +a.lignes.slice(0,40).map(l=>`<tr><td>${esc(l.nom)}</td><td>${esc(l.email||'—')}</td>
      <td>${esc(l.tel||'—')}</td><td>${esc(l.ville||'—')}</td><td>${nf(l.nb)}</td>
      <td>${money(l.total)}</td><td>${esc(l.der||'—')}</td></tr>`).join('')
    +`</tbody></table></div>
    <p class="hint"><b>${nf(a.lignes.length)} client${a.lignes.length>1?'s':''} lu${a.lignes.length>1?'s':''}</b>
     — ${nf(dej)} déjà connu${dej>1?'s':''} par l'email, ${nf(a.lignes.length-dej)} nouveau${a.lignes.length-dej>1?'x':''}.
     ${sansMail?nf(sansMail)+' sans email : ils entreront quand même, mais tu ne pourras pas leur écrire.':''}
     ${a.vides.length?'<br>'+nf(a.vides.length)+' ligne(s) ignorée(s), sans nom ni email.':''}
     ${a.lignes.length>40?'<br>L\'aperçu montre les 40 premières.':''}</p>`;
  $('impok').disabled=false;
}

function impApplique(){
  if(!IMP) return;
  const remp=$('impremp').checked;
  let L;
  if(remp){ L=IMP.lignes.slice(); }
  else {
    L=R.slice();
    const par={}; L.forEach((c,i)=>{ if(c.email) par[String(c.email).toLowerCase()]=i; });
    IMP.lignes.forEach(l=>{
      const k=l.email?String(l.email).toLowerCase():null;
      if(k && par[k]!==undefined) L[par[k]]=Object.assign({}, L[par[k]], l);
      else L.push(l);
    });
  }
  R=L; garde(R);
  const s=session(); const J=lit('crm-journal-v1',[]);
  J.push({t:new Date().toISOString(),u:s?s.nom:'?',act:'retail',
          lib:remp?'clients retail remplacés par un fichier':'clients retail mis à jour par un fichier',
          ref:'',av:null,ap:IMP.lignes.length+' lignes'});
  ecrit('crm-journal-v1',J);
  $('impov').classList.remove('on');
  bandeau(); peint();
}

function bandeau(){
  let t=null; try{ t=localStorage.getItem(K_LOCAL); }catch(e){}
  const b=$('impban');
  if(!t){ b.hidden=true; return; }
  b.hidden=false;
  b.innerHTML='Cette liste vient d\'un fichier que tu as importé, pas du fichier d\'origine. '
    +'<button id="impraz">Revenir au fichier d\'origine</button>';
  $('impraz').onclick=()=>{
    if(!confirm("Revenir au fichier d'origine ? Les clients importés et les coordonnées corrigées seront perdus.")) return;
    try{ localStorage.removeItem(K_LOCAL); }catch(e){}
    R=base(); bandeau(); peint();
  };
}

$('imp').onclick=()=>{ $('impres').innerHTML=''; $('impmsg').textContent='';
  $('impok').disabled=true; IMP=null; $('impov').classList.add('on'); };
$('impx').onclick=$('impann').onclick=()=>$('impov').classList.remove('on');
$('impov').addEventListener('click',e=>{ if(e.target.id==='impov') $('impov').classList.remove('on'); });
$('imptxt').oninput=()=>{ const t=$('imptxt').value; if(t.trim()) impPeint(impAnalyse(t)); };
$('impfile').onchange=e=>{ const f=e.target.files[0]; if(!f) return;
  if(xlEstExcel(f)) return impExcel(f);
  impOnglets(null);
  $('impres').innerHTML='<p class="hint">Lecture de '+esc(f.name)+'…</p>';
  lireFichier(f, m=>{ $('impres').innerHTML='<p class="hint">'+esc(m)+'</p>'; })
    .then(t=>{ $('imptxt').value=t; impPeint(impAnalyse(t)); })
    .catch(err=>{ $('impres').innerHTML='<p class="hint" style="color:var(--crit)"><b>'+esc(err.message||'Lecture impossible.')+'</b></p>';
      $('impok').disabled=true; IMP=null; });
  e.target.value=''; };

/* Un classeur Excel, lu ici même. Plusieurs onglets : on les propose. */
let XLONG=null;
function impOnglets(o){
  XLONG=o; const z=$('imponglets');
  if(!o||o.length<2){ z.hidden=true; z.innerHTML=''; return; }
  z.hidden=false;
  z.innerHTML='<span class="lab">Onglet</span>'+o.map((t,i)=>
    `<button class="xlb${i===0?' on':''}" data-o="${i}">${esc(t.nom)}`
    +` <span style="opacity:.65">${t.lignes.length}</span></button>`).join('');
}
$('imponglets').addEventListener('click',ev=>{
  const b=ev.target.closest('button[data-o]'); if(!b||!XLONG) return;
  [...$('imponglets').querySelectorAll('button')].forEach(x=>x.classList.remove('on'));
  b.classList.add('on');
  impPeint(impAnalyse(XLONG[+b.dataset.o].lignes));
});
async function impExcel(f){
  if(!xlsxDispo){
    $('impres').innerHTML='<p class="hint" style="color:var(--crit)"><b>Ce navigateur est trop '
      +'ancien pour lire un .xlsx.</b> Depuis Google Sheets : Fichier → Télécharger → CSV.</p>';
    $('impok').disabled=true; return;
  }
  $('impres').innerHTML='<p class="hint">Lecture du fichier Excel…</p>';
  try{
    const {onglets}=await xlLis(await f.arrayBuffer());
    const utiles=onglets.filter(o=>o.lignes.length>1);
    if(!utiles.length) throw new Error('Aucun onglet ne contient de lignes.');
    $('imptxt').value='';
    impOnglets(utiles);
    impPeint(impAnalyse(utiles[0].lignes));
  }catch(err){
    $('impres').innerHTML='<p class="hint" style="color:var(--crit)"><b>Impossible de lire ce '
      +'fichier Excel.</b> '+esc(err.message||'')+'<br>Essaie en l\'enregistrant à nouveau en '
      +'<b>.xlsx</b>, ou passe par un CSV.</p>';
    $('impok').disabled=true; IMP=null;
  }
}
$('impok').onclick=impApplique;

bandeau(); peint();
$('sfoot').innerHTML='Clients au détail';
"""

html = coquille("Retail", "Retail",
                "Les clients du site et de la boutique — et comment leur écrire",
                CSS, CORPS.replace('__ACCEPT_TAB__', _lire.ACCEPT_TAB), JS, donnees=('retail',))
open('retail.html', 'w').write(html)
print('retail.html', round(os.path.getsize('retail.html') / 1024), 'Ko')
