# -*- coding: utf-8 -*-
"""Rubrique « VIP wholesale » : les gros clients, leurs commandes et ce qu'ils achètent.
Source : clients_seed.json (fabriqué par build_clients_data.py depuis l'onglet « carmen » du Google Sheet),
complété par les factures de vente enregistrées dans SAM (clients-v1) pour les coordonnées."""
import json
from build_crm import coquille
import _donnees
C = json.load(open('cat.json'))
BC2CLE = {r[0].lstrip('0'): r[15] for r in C if r[0]}
SEED = json.load(open('clients_seed.json'))

# ---- version compacte pour la page : chaque ligne devient un tableau ----
K = ['bc', 'nom', 'ml', 'marque', 'type', 'p', 'q', 't', 'fact', 'sorti', 'note']
def compact(cl):
    return {'nom': cl['nom'], 'total': cl['total'], 'nb': cl['nb'], 'nbDevis': cl['nbDevis'],
            'totalDevis': cl['totalDevis'], 'q': cl['q'], 'prem': cl['prem'], 'der': cl['der'],
            'ecritures': cl['ecritures'],
            'cmds': [{'num': c['num'], 'd': c['date'], 'de': c['date_estimee'], 'devis': c['devis'],
                      'note': c['note'], 'total': c['total'], 'sous': c['sous'], 'ecart': c['ecart_sous'],
                      'douteux': c['douteux'], 'sl': c['sans_lignes'], 'ls': c['ligne_sheet'],
                      'f': c.get('fact', ''), 's': c.get('sorti', ''),
                      'l': [[l[k] for k in K] for l in c['lignes']]} for c in cl['cmds']]}
DATA = {'date': SEED['date'], 'src': SEED['src'], 'clients': [compact(c) for c in SEED['clients']]}

CSS = r"""
.reldest{display:flex;align-items:center;gap:9px;margin-bottom:11px}
.reldest label{font-size:9.5px;letter-spacing:.12em;text-transform:uppercase;color:var(--ink-3);
font-weight:600;flex:none}
.reldest input{flex:1;font-family:inherit;font-size:13.5px;color:var(--ink);background:var(--surface-2);
border:1px solid var(--line);border-radius:3px;padding:8px 10px}
.reldest input:focus{outline:2px solid var(--iris);outline-offset:1px;background:var(--surface)}
.reldest input.manque{border-color:var(--crit);background:var(--crit-soft)}
.reldest span{font-size:12px;color:var(--ink-3)}
.reldest span.err{color:var(--crit);font-weight:600}

.sous{margin:5px 0 0;font-size:14px;color:var(--ink-2);max-width:74ch;line-height:1.5}
.tools{display:flex;gap:9px;flex-wrap:wrap;align-items:center;margin-bottom:16px}
.tools .sp{margin-left:auto}
.srch{position:relative;flex:1 1 220px;max-width:360px}
.srch input{width:100%;padding:10px 12px 10px 34px;font-family:inherit;font-size:14px;
border:1px solid var(--line);border-radius:7px;background:var(--surface);color:var(--ink)}
.srch input:focus{outline:0;border-color:var(--iris);box-shadow:0 0 0 3px var(--iris-soft)}
.srch::before{content:"⌕";position:absolute;left:11px;top:50%;transform:translateY(-50%);color:var(--ink-3);font-size:16px}
.sel{padding:10px 11px;font-family:inherit;font-size:14px;border:1px solid var(--line);border-radius:7px;background:var(--surface);color:var(--ink);cursor:pointer}
.sel:focus{outline:0;border-color:var(--iris)}
.btn{font-family:inherit;font-size:14px;font-weight:500;color:var(--ink-2);background:var(--surface);border:1px solid var(--line);border-radius:7px;padding:10px 16px;cursor:pointer}
.btn:hover{border-color:var(--iris);color:var(--iris)}
.btn.pri{background:var(--iris);border-color:var(--iris);color:#fff;font-weight:600}
.btn.pri:hover{filter:brightness(1.08);color:#fff}

/* trois chiffres, pas plus */
.kpis{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-bottom:22px}
.kpi{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:16px 20px}
.kpi .v{font-family:Inter,sans-serif;font-size:30px;font-weight:800;line-height:1;letter-spacing:-.03em;font-variant-numeric:tabular-nums;color:var(--ink)}
.kpi .v.i{color:var(--iris)}
.kpi .k{font-size:13px;color:var(--ink-2);margin-top:6px}

/* la liste des clients : un tableau, une ligne par client */
.tbl{width:100%;border-collapse:collapse;font-size:14px;background:var(--surface);border:1px solid var(--line);border-radius:10px;overflow:hidden}
.tbl th{text-align:left;font-family:Inter,sans-serif;font-size:11.5px;letter-spacing:.09em;text-transform:uppercase;color:var(--ink);
font-weight:800;padding:12px 14px;background:var(--surface-2);border-bottom:2px solid var(--line);white-space:nowrap;cursor:pointer;user-select:none}
.tbl th:hover{color:var(--iris)}
.tbl th.on::after{content:" ▾";color:var(--iris)}
.tbl th.n,.tbl td.n{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
.tbl td{padding:12px 14px;border-bottom:1px solid var(--line-2);vertical-align:middle}
.tbl tbody tr:last-child td{border-bottom:0}
.tbl tbody tr{cursor:pointer}
.tbl tbody tr:hover td{background:var(--iris-soft)}
.tbl td.rg{color:var(--ink-3);font-family:Inter,sans-serif;font-size:12px;width:34px}
.tbl td.nom{font-weight:700;font-size:15px}
.tbl td.nom small{display:block;font-weight:400;font-size:12px;color:var(--ink-3);margin-top:2px}
.tbl td.mt{font-family:Inter,sans-serif;font-weight:800;font-size:15px;color:var(--iris)}
.tbl td.mt .bar{height:5px;border-radius:3px;background:var(--line-2);margin-top:6px;overflow:hidden;min-width:120px}
.tbl td.mt .bar i{display:block;height:100%;background:var(--iris)}
.tbl td.dim{color:var(--ink-2)}
.warn{display:inline-block;font-family:Inter,sans-serif;font-size:10.5px;font-weight:700;padding:2px 7px;border-radius:99px;background:var(--crit-soft);color:var(--crit);margin-left:8px;vertical-align:middle}
.wrapx{overflow-x:auto}
.foot{margin-top:18px;font-size:12.5px;color:var(--ink-3);line-height:1.6}
.foot a{color:var(--iris)}
details.src{margin-top:12px;font-size:13px;color:var(--ink-2);line-height:1.65;max-width:80ch}
details.src summary{cursor:pointer;color:var(--iris);font-weight:600}
details.src b{color:var(--ink)}

/* fiche client : un tiroir, trois onglets */
.dr{position:fixed;top:0;right:0;bottom:0;width:min(980px,100%);background:var(--surface);
box-shadow:-12px 0 40px rgba(0,0,0,.18);transform:translateX(102%);transition:transform .18s;z-index:60;display:flex;flex-direction:column}
.dr.on{transform:none}
.drov{position:fixed;inset:0;background:rgba(23,23,29,.35);z-index:59;display:none}
.drov.on{display:block}
.dh{padding:20px 28px 0;border-bottom:1px solid var(--line)}
.dh .row{display:flex;align-items:flex-start;gap:14px}
.dh h2{margin:0;font-size:28px;font-weight:800;letter-spacing:-.025em;line-height:1.1;flex:1}
.dh .x{background:none;border:1px solid var(--line);border-radius:7px;font-size:18px;color:var(--ink-2);cursor:pointer;line-height:1;padding:6px 11px}
.dh .x:hover{border-color:var(--ink);color:var(--ink)}
.dk{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:18px 0 20px}
.dk div{background:var(--surface-2);border:1px solid var(--line);border-radius:9px;padding:12px 14px}
.dk b{display:block;font-family:Inter,sans-serif;font-size:22px;font-weight:800;letter-spacing:-.03em;line-height:1;font-variant-numeric:tabular-nums}
.dk b.i{color:var(--iris)}
.dk span{display:block;font-size:12px;color:var(--ink-2);margin-top:5px}
.tabs{display:flex;gap:4px}
.tab{background:none;border:0;border-bottom:3px solid transparent;padding:10px 16px;font-family:inherit;font-size:14.5px;font-weight:600;color:var(--ink-3);cursor:pointer}
.tab.on{color:var(--iris);border-bottom-color:var(--iris)}
.db{padding:20px 28px 40px;overflow-y:auto;flex:1}
.pane{display:none}.pane.on{display:block}
.t2{width:100%;border-collapse:collapse;font-size:14px;background:var(--surface);border:1px solid var(--line);border-radius:10px;overflow:hidden}
.t2 th{text-align:left;font-family:Inter,sans-serif;font-size:11.5px;letter-spacing:.09em;text-transform:uppercase;color:var(--ink);font-weight:800;padding:11px 14px;background:var(--surface-2);border-bottom:2px solid var(--line);white-space:nowrap}
.t2 th.n,.t2 td.n{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
.t2 td{padding:11px 14px;border-bottom:1px solid var(--line-2);vertical-align:middle}
.t2 tbody tr:last-child td{border-bottom:0}
.t2 tr.cmd{cursor:pointer}
.t2 tr.cmd:hover td{background:var(--surface-2)}
.t2 tr.cmd.on td{background:var(--iris-soft)}
.t2 td.mt{font-family:Inter,sans-serif;font-weight:800}
.t2 td .est{color:var(--ink-3)}
.t2 tr.lig td{background:var(--surface-2);padding:6px 14px 14px 40px}
.t2 tr.lig table{width:100%;border-collapse:collapse;font-size:13px}
.t2 tr.lig table th{font-size:10px;padding:8px 8px 6px;background:none;border-bottom:1px solid var(--line)}
.t2 tr.lig table td{padding:7px 8px;border-bottom:1px dashed var(--line-2);background:none}
.t2 tr.lig table td.n{font-family:Inter,sans-serif}
.t2 tr.lig a{color:var(--ink);text-decoration:none;border-bottom:1px dotted var(--ink-3)}
.t2 tr.lig a:hover{color:var(--iris);border-bottom-color:var(--iris)}
.t2 td.nom{font-weight:600}
.t2 td.nom small{display:block;font-weight:400;font-size:12px;color:var(--ink-3)}
.ok{color:var(--good);font-weight:700}.non{color:var(--ink-3)}
.avert{background:var(--warn-soft);border-left:3px solid var(--warn);border-radius:0 8px 8px 0;padding:11px 14px;font-size:13px;color:var(--ink-2);line-height:1.6;margin:0 0 16px}
.avert b{color:var(--ink)}
.ed{display:grid;grid-template-columns:repeat(2,1fr);gap:14px;max-width:640px}
.ed label{display:flex;flex-direction:column;gap:5px;font-family:Inter,sans-serif;font-size:11px;letter-spacing:.09em;text-transform:uppercase;color:var(--ink);font-weight:800}
.ed input,.ed textarea{font-family:inherit;font-size:14px;color:var(--ink);background:var(--surface-2);border:1px solid var(--line);border-radius:7px;padding:10px 12px;letter-spacing:0;text-transform:none;font-weight:400}
.ed input:focus,.ed textarea:focus{outline:0;border-color:var(--iris);background:var(--surface);box-shadow:0 0 0 3px var(--iris-soft)}
.ed textarea{min-height:80px;resize:vertical;grid-column:1/-1}
.ecr{margin-top:22px;font-size:13px;color:var(--ink-2);line-height:1.7}
.ecr b{color:var(--ink)}
.vide{border:2px dashed var(--line);border-radius:12px;padding:40px 32px;text-align:center;background:var(--surface-2);max-width:66ch;margin:16px auto;color:var(--ink-2)}
.t2 select.pay{font-family:inherit;font-size:13px;padding:5px 7px;border:1px solid var(--line);border-radius:6px;background:var(--surface);color:var(--ink);cursor:pointer}
.t2 select.pay.du{border-color:var(--crit);color:var(--crit);font-weight:700;background:var(--crit-soft)}
.t2 select.pay.ok{border-color:var(--good);color:var(--good);font-weight:700;background:var(--good-soft)}
.t2 select.pay.part{border-color:var(--warn);color:var(--warn);font-weight:700;background:var(--warn-soft)}
.t2 input.part{width:80px;font-family:inherit;font-size:13px;padding:5px 7px;border:1px solid var(--line);border-radius:6px;text-align:right}
.t2 td .rel{display:block;font-size:11px;color:var(--ink-3);margin-top:3px}
.dk b.c{color:var(--crit)}
.dh .btn.rel{white-space:nowrap}
.dh .btn.rel[disabled]{opacity:.45;cursor:default}
.barre2{display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin:0 0 14px;font-size:13px;color:var(--ink-2)}
.barre2 .sp{margin-left:auto}
.btn.sm{padding:6px 12px;font-size:13px}
.ov{position:fixed;inset:0;background:rgba(23,23,29,.5);z-index:80;display:none;align-items:flex-start;justify-content:center;padding:40px 18px;overflow-y:auto}
.ov.on{display:flex}
.mod{background:var(--surface);border:1px solid var(--line);border-radius:10px;width:100%;max-width:720px;box-shadow:0 18px 48px rgba(0,0,0,.22)}
.mod .mh{padding:18px 22px;border-bottom:1px solid var(--line);display:flex;align-items:center;gap:12px}
.mod .mh h3{margin:0;font-size:18px;font-weight:800;letter-spacing:-.02em;flex:1}
.mod .mb{padding:18px 22px;display:flex;flex-direction:column;gap:12px}
.mod textarea{width:100%;min-height:260px;font-family:inherit;font-size:14px;line-height:1.55;color:var(--ink);background:var(--surface-2);border:1px solid var(--line);border-radius:7px;padding:12px 14px;resize:vertical}
.mod textarea:focus{outline:0;border-color:var(--iris);background:var(--surface);box-shadow:0 0 0 3px var(--iris-soft)}
.mod .mf{padding:14px 22px;border-top:1px solid var(--line);display:flex;gap:9px;align-items:center;flex-wrap:wrap;background:var(--surface-2);border-radius:0 0 10px 10px}
.mod .mf .msg{font-size:12.5px;color:var(--ink-3);margin-right:auto}
.lang{display:flex;gap:4px}
.lang button{font-family:inherit;font-size:12.5px;font-weight:600;padding:5px 10px;border:1px solid var(--line);border-radius:99px;background:var(--surface);color:var(--ink-2);cursor:pointer}
.lang button.on{background:var(--iris);border-color:var(--iris);color:#fff}
@media(max-width:900px){.kpis,.dk{grid-template-columns:repeat(2,1fr)}}
"""

CORPS = r"""
<div class="tools">
  <div class="srch"><input id="q" autocomplete="off" placeholder="Chercher un client…"></div>
  <select id="per" class="sel">
    <option value="0">Toute la période</option>
    <option value="30">30 derniers jours</option>
    <option value="90">3 derniers mois</option>
    <option value="180">6 derniers mois</option>
    <option value="365">12 derniers mois</option></select>
  <span class="sp"></span>
  <span id="exp"></span>
</div>
<div id="kpis"></div>
<div id="corps"></div>
<details class="src" id="note"><summary>D'où viennent ces chiffres, et ce qui est approximatif</summary><div id="notetxt"></div></details>

<div class="drov" id="drov"></div>
<aside class="dr" id="dr" aria-hidden="true">
  <div class="dh">
    <div class="row"><h2 id="dnom"></h2><button class="btn" id="decr">Écrire</button><button class="btn pri rel" id="drel">Relance de paiement</button><button class="x" id="dx" title="Fermer">✕</button></div>
    <div class="dk" id="dk"></div>
    <div class="tabs">
      <button class="tab on" data-t="cmd">Ses commandes</button>
      <button class="tab" data-t="prod">Les parfums qu'il lui prend</button>
      <button class="tab" data-t="coord">Coordonnées</button>
    </div>
  </div>
  <div class="db">
    <div class="pane on" id="p-cmd"></div>
    <div class="pane" id="p-prod"></div>
    <div class="pane" id="p-coord"></div>
  </div>
</aside>

<div class="ov" id="relov"><div class="mod">
  <div class="mh"><h3>Relance de paiement — <span id="relnom"></span></h3><div class="lang" id="rellang"><button data-l="fr" class="on">FR</button><button data-l="en">EN</button><button data-l="es">ES</button></div></div>
  <div class="mb">
    <div class="reldest">
      <label for="reldest">Envoyer à</label>
      <input type="email" id="reldest" placeholder="adresse@exemple.com" autocomplete="off">
      <span id="reldn"></span>
    </div>
    <textarea id="reltxt"></textarea>
    <p class="ecr" style="margin:0">Le texte est modifiable. L'adresse ci-dessus est celle de la fiche client ;
    si tu la corriges ici, elle est enregistrée dans la fiche. « Ouvrir dans Mail » prépare l'e-mail dans ton
    logiciel de messagerie ; WhatsApp utilise le téléphone de la fiche. SAM n'envoie rien tout seul
    (il faudra le serveur pour ça) : c'est toi qui appuies sur Envoyer.</p></div>
  <div class="mf"><span class="msg" id="relmsg"></span>
    <button class="btn" id="relcopy">Copier le texte</button>
    <button class="btn" id="relwa">WhatsApp</button>
    <button class="btn pri" id="relmail">Ouvrir dans Mail</button>
    <button class="btn" id="relx">Fermer</button></div>
</div></div>
"""

JS = r"""
const D=__DATA__, BC2CLE=__BC2CLE__;
const KCLI='clients-v1', KUSR='crm-utilisateur-v1', KJOU='crm-journal-v1', KPAY='reglements-v1';
let CLI={}, USR='', PAY={};
CLI=lit(KCLI,{}); if(!CLI||typeof CLI!=='object') CLI=base(KCLI,{});
PAY=lit(KPAY,{}); if(!PAY||typeof PAY!=='object') PAY=base(KPAY,{});
const sauvePAY=()=>ecrit(KPAY,PAY);
const journal=(act,lib,ref,ap)=>{ const J=lit(KJOU,[]);
  J.push({t:new Date().toISOString(),u:USR||'(non renseigné)',act,lib,ref,av:null,ap:ap||null});
  ecrit(KJOU,J); };
const MODES=[['','—'],['especes','Espèces'],['zelle','Zelle'],['virement','Virement'],['carte','Carte'],['cheque','Chèque'],['credit','Crédit / store credit'],['autre','Autre']];
const STATUTS=[['','non renseigné'],['du','À payer'],['paye','Payée'],['part','Partielle']];
const pkey=(nom,x)=>nom+'|'+(x.num||'l'+x.ls);
/* ce que le tableur dit déjà : « paid in cash », « paid zelle »… */
function payInit(nom,x){
  const k=pkey(nom,x); if(PAY[k]) return PAY[k];
  const txt=[x.note,x.f,x.s,...x.l.map(l=>l[FACT]+' '+l[SORTI]+' '+l[NOTE])].join(' ').toLowerCase();
  if(/\bpaid\b/.test(txt)){ const p={st:'paye',mode:/cash/.test(txt)?'especes':/zelle/.test(txt)?'zelle':'',src:'tableur'};
    if(/paid in \d+ parts?/.test(txt)) p.st='paye'; return p; }
  return {st:'',mode:''};
}
const reste=(x,p)=>p.st==='du'?x.total:p.st==='part'?Math.max(0,x.total-(+p.regle||0)):0;
USR=NOM_UTIL;
window.__nomChange.push(v=>{ USR=v; try{ majUser(); }catch(e){} });
const sauveCLI=()=>ecrit(KCLI,CLI);
const [BC,NOM,ML,MARQUE,TYPE,P,Q,T,FACT,SORTI,NOTE]=[0,1,2,3,4,5,6,7,8,9,10];
const dfr=d=>{ if(!d) return '—'; const [a,m,j]=d.split('-'); return j+'/'+m+'/'+a.slice(2); };
const AUJ=new Date(D.date);
const fl=c=>c.l.reduce((s,l)=>s+(l[Q]||0),0);
let TRI='mt';

function lignes(){
  const per=+$('per').value, q=$('q').value.trim().toLowerCase();
  const lim=per?isoJour(new Date(AUJ.getTime()-per*864e5)):null;
  return D.clients.filter(c=>!q||c.nom.toLowerCase().includes(q)).map(c=>{
    const v=c.cmds.filter(x=>!x.devis&&!x.douteux&&(!lim||(x.d&&x.d>=lim)));
    return {c,v,total:v.reduce((a,x)=>a+x.total,0),nb:v.length,
            der:v.reduce((a,x)=>x.d&&x.d>a?x.d:a,''),fl:v.reduce((a,x)=>a+fl(x),0)};
  }).filter(r=>r.nb);
}
/* Ceux qui n'ont eu qu'un devis, jamais commandé : ce ne sont pas des clients, ce sont des occasions ratées. */
function devisSeuls(){
  const q=$('q').value.trim().toLowerCase();
  return D.clients.filter(c=>!c.cmds.some(x=>!x.devis&&!x.douteux) && (!q||c.nom.toLowerCase().includes(q)))
    .map(c=>({c,dv:c.cmds.filter(x=>x.devis),tot:c.cmds.filter(x=>x.devis).reduce((a,x)=>a+x.total,0)}));
}

function dessine(){
  const R=lignes();
  R.sort((a,b)=> TRI==='nb'?b.nb-a.nb : TRI==='dt'?(b.der||'').localeCompare(a.der||'') : TRI==='az'?a.c.nom.localeCompare(b.c.nom,'fr') : TRI==='fl'?b.fl-a.fl : b.total-a.total);
  const tot=R.reduce((a,r)=>a+r.total,0), ncmd=R.reduce((a,r)=>a+r.nb,0), max=Math.max(...R.map(r=>r.total),0);
  $('kpis').innerHTML=`<div class="kpis">
    <div class="kpi"><div class="v">${nf(R.length)}</div><div class="k">clients grossistes — ils lui achètent en gros</div></div>
    <div class="kpi"><div class="v i">${money(tot)}</div><div class="k">ce qu'il leur a vendu au total</div></div>
    <div class="kpi"><div class="v">${nf(ncmd)}</div><div class="k">commandes passées par ces clients</div></div></div>`;
  const th=(k,l,cls)=>`<th class="${cls||''}${TRI===k?' on':''}" data-k="${k}">${l}</th>`;
  $('corps').innerHTML = R.length ? `<div class="wrapx"><table class="tbl"><thead><tr>
      <th></th>${th('az','Client')}${th('mt','Vendu à ce client','n')}${th('nb','Commandes','n')}${th('fl','Flacons','n')}${th('dt','Dernière commande','n')}</tr></thead>
      <tbody>${R.map((r,i)=>`<tr data-c="${esc(r.c.nom)}">
        <td class="rg">${i+1}</td>
        <td class="nom">${esc(r.c.nom)}${r.c.cmds.some(x=>x.douteux)?'<span class="warn">à vérifier</span>':''}</td>
        <td class="n mt">${money(r.total)}<div class="bar"><i style="width:${max?Math.max(1,r.total/max*100):0}%"></i></div></td>
        <td class="n">${nf(r.nb)}</td><td class="n dim">${nf(Math.round(r.fl))}</td><td class="n dim">${dfr(r.der)}</td></tr>`).join('')}</tbody>
      <tfoot><tr><td></td><td style="font-weight:700">${R.length} clients</td><td class="n mt">${money(tot)}</td><td class="n" style="font-weight:700">${nf(ncmd)}</td><td class="n dim">${nf(Math.round(R.reduce((a,r)=>a+r.fl,0)))}</td><td></td></tr></tfoot></table></div>`
    : `<div class="vide">Aucun client sur cette période.</div>`;
  const DS=devisSeuls();
  if(DS.length) $('corps').insertAdjacentHTML('beforeend',
    `<h3 style="font-family:Inter,sans-serif;font-size:12px;letter-spacing:.09em;text-transform:uppercase;font-weight:800;margin:26px 0 10px;color:var(--ink)">Devis restés sans commande <span style="font-weight:500;text-transform:none;letter-spacing:0;font-size:13px;color:var(--ink-2);margin-left:8px">${DS.length} personnes ont reçu un prix, n'ont jamais acheté — ${money(DS.reduce((a,d)=>a+d.tot,0))} proposés</span></h3>
     <div class="wrapx"><table class="tbl"><thead><tr><th></th><th>Nom</th><th class="n">Devis proposé</th><th class="n">Devis</th><th class="n">Date</th></tr></thead><tbody>${
      DS.map((o,i)=>`<tr data-c="${esc(o.c.nom)}"><td class="rg">${i+1}</td><td class="nom">${esc(o.c.nom)}</td>
        <td class="n dim">${money(o.tot)}</td><td class="n dim">${o.dv.length}</td><td class="n dim">${dfr(o.dv[0]&&o.dv[0].d)}</td></tr>`).join('')}</tbody></table></div>`);
  document.querySelectorAll('.tbl tbody tr').forEach(el=>el.onclick=()=>ouvre(el.dataset.c));
  document.querySelectorAll('.tbl th[data-k]').forEach(el=>el.onclick=()=>{ TRI=el.dataset.k; dessine(); });
  $('src').innerHTML=`onglet « carmen »<br>lu le ${dfr(D.date)}`;
  const ct=document.getElementById('ct-vip'); if(ct) ct.textContent=nf(D.clients.filter(c=>c.cmds.some(x=>!x.devis&&!x.douteux)).length);
}

/* Écrire à un client wholesale : même fenêtre que le Retail et les Fournisseurs.
   La relance de paiement garde son bouton à elle, qui sait de quelles commandes
   il parle ; celui-ci sert à tout le reste — une promo, un mot, une réponse. */
function jlogContact(nom,par,quoi){
  const J=lit(KJOU,[]);
  J.push({t:new Date().toISOString(),u:USR||'(non renseigné)',act:'contact',
          lib:'message préparé — '+quoi,ref:nom,av:null,ap:par});
  ecrit(KJOU,J);
}
function ecrire(nom){
  const co=CLI[nom]||{};
  contacte({nom, email:co.email, tel:co.tel, modele:'promo',
    onSave:(mail,tel)=>{
      if(mail===(co.email||'') && tel===(co.tel||'')) return;
      CLI[nom]=Object.assign({},CLI[nom]||{},
        {email:mail||undefined, tel:tel||undefined, maj:new Date().toISOString()});
      sauveCLI();
    }});
}

/* ---------- fiche client ---------- */
let OUV=null;
function ouvre(nom){
  const c=D.clients.find(x=>x.nom===nom); if(!c) return; OUV=c;
  const co=CLI[nom]||{};
  const v=c.cmds.filter(x=>!x.devis&&!x.douteux), dv=c.cmds.filter(x=>x.devis), dout=c.cmds.filter(x=>x.douteux);
  const tot=v.reduce((a,x)=>a+x.total,0);
  $('dnom').textContent=nom;
  const dus=v.map(x=>({x,p:payInit(nom,x)})).filter(o=>reste(o.x,o.p)>0), du=dus.reduce((a,o)=>a+reste(o.x,o.p),0);
  $('dk').innerHTML=`<div><b class="i">${money(tot)}</b><span>vendu à ce client au total</span></div>
    <div><b>${nf(v.length)}</b><span>commandes · ${v.length?money(tot/v.length):'—'} en moyenne</span></div>
    <div><b class="${du>0?'c':''}">${money(du)}</b><span>reste à payer${dus.length?' · '+dus.length+' commande'+(dus.length>1?'s':''):''}</span></div>
    <div><b>${dfr(c.der)}</b><span>dernière commande${c.prem?' · première le '+dfr(c.prem):''}</span></div>`;
  $('drel').disabled=!dus.length; $('drel').title=dus.length?'':'Aucune commande marquée « À payer » : indique le statut de règlement dans la liste des commandes.';
  $('drel').onclick=()=>relance(nom,c,dus);
  $('decr').onclick=()=>ecrire(nom);

  /* onglet commandes */
  const cmds=c.cmds.slice().sort((a,b)=>(b.d||'').localeCompare(a.d||'')||(b.num||'').localeCompare(a.num||''));
  $('p-cmd').innerHTML=`${dout.length?`<div class="avert"><b>À vérifier dans le tableur :</b> ${dout.map(x=>`commande ${esc(x.num||'sans n°')} notée ${money(x.total)} (ligne ${x.ls})`).join(', ')} — montant invraisemblable, laissé de côté.</div>`:''}
    <div class="barre2"><span>Clique sur une commande pour voir ses parfums. « Facturée » et « sortie du stock » viennent des croix du tableur ; le règlement se note ici.</span>
      <span class="sp"></span><button class="btn sm" id="toutpaye">Marquer toutes les commandes comme payées</button></div>
    <table class="t2"><thead><tr><th>Date</th><th>Commande</th><th class="n">Parfums</th><th class="n">Montant</th><th>Facturée · sortie</th><th>Règlement</th><th>Mode</th></tr></thead>
    <tbody>${cmds.map((x,i)=>{
      const f=/x/i.test(x.f)||(x.l.length&&x.l.every(l=>/x/i.test(l[FACT]))), s=/x/i.test(x.s)||(x.l.length&&x.l.every(l=>/x/i.test(l[SORTI])));
      const p=payInit(nom,x), k=pkey(nom,x), cls=p.st==='du'?'du':p.st==='paye'?'ok':p.st==='part'?'part':'';
      return `<tr class="cmd" data-i="${i}">
        <td>${x.d?(x.de?`<span class="est" title="date absente du tableur, reprise de la commande voisine">≈ ${dfr(x.d)}</span>`:dfr(x.d)):'—'}</td>
        <td>${x.num?'n° '+esc(x.num):'<span class="est">sans n°</span>'}${x.devis?' · devis':''}${x.douteux?' · <span class="warn">à vérifier</span>':''}${x.note?` · <span class="est">${esc(x.note)}</span>`:''}${p.rel?`<span class="rel">relancé le ${dfr(p.rel)}</span>`:''}</td>
        <td class="n">${x.l.length?nf(x.l.length):'<span class="est">total seul</span>'}</td><td class="n mt">${money(x.total)}</td>
        <td>${f?'<span class="ok">facturée</span>':'<span class="non">—</span>'} · ${s?'<span class="ok">sortie</span>':'<span class="non">—</span>'}</td>
        <td>${x.devis?'<span class="non">devis</span>':`<select class="pay ${cls}" data-k="${esc(k)}" data-f="st" onclick="event.stopPropagation()">${STATUTS.map(([v,l])=>`<option value="${v}"${p.st===v?' selected':''}>${l}</option>`).join('')}</select>${p.st==='part'?` <input class="part" data-k="${esc(k)}" data-f="regle" type="number" step="any" value="${p.regle||''}" placeholder="réglé $" onclick="event.stopPropagation()">`:''}`}</td>
        <td>${x.devis?'':`<select class="pay" data-k="${esc(k)}" data-f="mode" onclick="event.stopPropagation()">${MODES.map(([v,l])=>`<option value="${v}"${p.mode===v?' selected':''}>${l}</option>`).join('')}</select>`}</td></tr>
      <tr class="lig" data-i="${i}" hidden><td colspan="7">${x.l.length?`<table><thead><tr><th>Parfum</th><th>Marque</th><th>Cont.</th><th class="n">Prix</th><th class="n">Qté</th><th class="n">Montant</th></tr></thead><tbody>${
        x.l.map(l=>{ const k=BC2CLE[(l[BC]||'').replace(/^0+/,'')];
          return `<tr><td>${k?`<a href="catalogue.html#cle=${esc(k)}" title="ouvrir la fiche catalogue">${esc(l[NOM])}</a>`:esc(l[NOM])}</td><td>${esc(l[MARQUE])}</td><td>${esc(l[ML])}</td><td class="n">${l[P]!=null?money2(l[P]):'—'}</td><td class="n">${nf(l[Q]||0)}</td><td class="n"><b>${money2(l[T]||0)}</b></td></tr>`; }).join('')}</tbody></table>`
        :'<span class="est">Le tableur ne donne que le total de cette commande.</span>'}</td></tr>`; }).join('')}</tbody></table>
    ${dv.length?`<p class="ecr">${dv.length} devis (« quote ») pour ${money(dv.reduce((a,x)=>a+x.total,0))}, non comptés dans les achats.</p>`:''}`;
  document.querySelectorAll('#p-cmd tr.cmd').forEach(tr=>tr.onclick=e=>{ if(e.target.closest('select,input')) return;
    const l=document.querySelector(`#p-cmd tr.lig[data-i="${tr.dataset.i}"]`); l.hidden=!l.hidden; tr.classList.toggle('on',!l.hidden); });
  document.querySelectorAll('#p-cmd .pay, #p-cmd input.part').forEach(el=>el.onchange=()=>{
    const k=el.dataset.k, x=cmds.find(y=>pkey(nom,y)===k); const p=Object.assign({},payInit(nom,x),PAY[k]||{});
    if(el.dataset.f==='regle') p.regle=+el.value||0; else p[el.dataset.f]=el.value;
    delete p.src; p.maj=new Date().toISOString(); p.u=USR||''; PAY[k]=p; sauvePAY();
    const lib=el.dataset.f==='st'?'règlement : '+(STATUTS.find(s=>s[0]===p.st)||['','—'])[1]:el.dataset.f==='mode'?'mode de règlement : '+(MODES.find(m=>m[0]===p.mode)||['','—'])[1]:'montant réglé : '+money(p.regle);
    journal('client',lib,nom+' · commande '+(x.num||'sans n°'),money(x.total)); ouvre(nom); onglet('cmd'); });
  $('toutpaye').onclick=()=>{ let n=0; v.forEach(x=>{ const k=pkey(nom,x); const p=Object.assign({},payInit(nom,x),PAY[k]||{}); if(p.st!=='paye'){ p.st='paye'; delete p.src; p.maj=new Date().toISOString(); p.u=USR||''; PAY[k]=p; n++; } });
    if(n){ sauvePAY(); journal('client',n+' commandes marquées payées',nom,null); ouvre(nom); onglet('cmd'); } };

  /* onglet produits */
  const M={}; v.forEach(x=>x.l.forEach(l=>{ const k=l[BC]||l[NOM]; const m=(M[k]=M[k]||{nom:l[NOM],marque:l[MARQUE],ml:l[ML],bc:l[BC],q:0,t:0,n:0}); m.q+=l[Q]||0; m.t+=l[T]||0; m.n++; }));
  const prods=Object.values(M).sort((a,b)=>b.t-a.t);
  const MQ={}; prods.forEach(p=>{ if(p.marque) MQ[p.marque]=(MQ[p.marque]||0)+p.t; });
  const mq=Object.entries(MQ).sort((a,b)=>b[1]-a[1]).slice(0,8);
  $('p-prod').innerHTML=`<p class="ecr" style="margin:0 0 14px">${nf(prods.length)} parfums différents. Ses marques : ${mq.map(([m,t])=>`<b>${esc(m)}</b> ${money(t)}`).join(' · ')}.</p>
    <table class="t2"><thead><tr><th></th><th>Parfum</th><th>Marque</th><th class="n">Fois commandé</th><th class="n">Flacons</th><th class="n">Montant</th></tr></thead>
    <tbody>${prods.map((p,i)=>{ const k=BC2CLE[(p.bc||'').replace(/^0+/,'')];
      return `<tr><td class="n" style="color:var(--ink-3);width:30px">${i+1}</td><td class="nom">${k?`<a href="catalogue.html#cle=${esc(k)}" style="color:inherit;text-decoration:none">${esc(p.nom)}</a>`:esc(p.nom)}<small>${p.ml?esc(p.ml)+' oz':''}${p.bc?' · '+esc(p.bc):''}</small></td><td>${esc(p.marque)}</td><td class="n">${nf(p.n)}</td><td class="n">${nf(Math.round(p.q))}</td><td class="n mt">${money(p.t)}</td></tr>`; }).join('')}</tbody></table>`;

  /* onglet coordonnées */
  $('p-coord').innerHTML=`<div class="ed">
      <label>Téléphone<input id="e-tel" value="${esc(co.tel||'')}"></label>
      <label>E-mail<input id="e-email" value="${esc(co.email||'')}"></label>
      <label>Société<input id="e-raison" value="${esc(co.raison||'')}"></label>
      <label>Adresse<input id="e-adresse" value="${esc(co.adresse||'')}"></label>
      <label style="grid-column:1/-1">Note<textarea id="e-note" placeholder="Conditions, délais, remarques…">${esc(co.note||'')}</textarea></label>
    </div>
    <p style="margin:14px 0 0"><button class="btn pri" id="e-ok">Enregistrer</button> <span id="e-msg" style="font-size:13px;color:var(--good);margin-left:8px"></span></p>
    <p class="ecr">Ces coordonnées sont gardées dans SAM, pas dans le tableur.${c.ecritures.length?`<br>Dans le tableur, ce client est écrit : <b>${c.ecritures.slice(0,6).map(esc).join('</b>, <b>')}</b>${c.ecritures.length>6?' …':''}.`:''}</p>`;
  $('e-ok').onclick=()=>{
    const o={nom}; ['tel','email','raison','adresse','note'].forEach(k=>{ const v=$('e-'+k).value.trim(); if(v) o[k]=v; });
    CLI[nom]=Object.assign({},CLI[nom]||{},o,{maj:new Date().toISOString()}); sauveCLI();
    journal('client','fiche client modifiée',nom,'coordonnées');
    $('e-msg').textContent='enregistré'; setTimeout(()=>$('e-msg').textContent='',2000); dessine(); };
  onglet('cmd');
  $('dr').classList.add('on'); $('drov').classList.add('on'); document.querySelector('.db').scrollTop=0;
}
/* ---------- relance de paiement ---------- */
let REL=null;
const mon=(v,l)=>l==='fr'?money2(v):'$'+Number(v).toLocaleString(l==='es'?'es-ES':'en-US',{minimumFractionDigits:2,maximumFractionDigits:2});
const dl=(d,l)=>{ if(!d) return '—'; const [a,m,j]=d.split('-'); return l==='en'?m+'/'+j+'/'+a.slice(2):j+'/'+m+'/'+a.slice(2); };
const TXT={
 fr:(nom,L,tot,soc)=>`Bonjour ${nom},\n\nSauf erreur de notre part, ${L.length>1?'les commandes suivantes restent':'la commande suivante reste'} à régler :\n\n${L.map(o=>`  • ${o.x.num?'n° '+o.x.num:'commande'} du ${dfr(o.x.d)} — ${money2(reste(o.x,o.p))}${o.p.st==='part'?' (solde)':''}`).join('\n')}\n\nTotal : ${money2(tot)}\n\nMerci de nous indiquer la date de règlement, ou de nous signaler si un paiement a déjà été fait.\n\nBien cordialement,\n${soc}`,
 en:(nom,L,tot,soc)=>`Hi ${nom},\n\nUnless we missed something, the following ${L.length>1?'orders are':'order is'} still unpaid:\n\n${L.map(o=>`  • ${o.x.num?'#'+o.x.num:'order'} of ${dl(o.x.d,'en')} — ${mon(reste(o.x,o.p),'en')}${o.p.st==='part'?' (balance)':''}`).join('\n')}\n\nTotal due: ${mon(tot,'en')}\n\nCould you let us know when the payment will be made, or tell us if it was already sent?\n\nThank you,\n${soc}`,
 es:(nom,L,tot,soc)=>`Hola ${nom},\n\nSalvo error de nuestra parte, ${L.length>1?'los siguientes pedidos siguen pendientes':'el siguiente pedido sigue pendiente'} de pago:\n\n${L.map(o=>`  • ${o.x.num?'n.º '+o.x.num:'pedido'} del ${dl(o.x.d,'es')} — ${mon(reste(o.x,o.p),'es')}${o.p.st==='part'?' (saldo)':''}`).join('\n')}\n\nTotal: ${mon(tot,'es')}\n\n¿Nos puede indicar la fecha de pago, o avisarnos si ya fue realizado?\n\nGracias,\n${soc}`};
function relance(nom,c,dus){
  let soc='Perfumes Trade'; try{ const r=JSON.parse(localStorage.getItem('reglages-v1')||'{}'); if(r.societe) soc=r.societe; }catch(e){}
  const tot=dus.reduce((a,o)=>a+reste(o.x,o.p),0);
  REL={nom,dus,tot,soc,lang:'fr'};
  $('relnom').textContent=nom; $('reltxt').value=TXT.fr(nom,dus,tot,soc); $('relmsg').textContent='';
  const co0=CLI[nom]||{};
  $('reldest').value=co0.email||''; $('reldest').classList.remove('manque');
  $('reldn').textContent=co0.email?'':'aucune adresse dans la fiche — écris-la ici';
  $('reldn').className=co0.email?'':'err';
  document.querySelectorAll('#rellang button').forEach(b=>b.classList.toggle('on',b.dataset.l==='fr'));
  $('relov').classList.add('on'); $('reltxt').scrollTop=0;
}
document.querySelectorAll('#rellang button').forEach(b=>b.onclick=()=>{ if(!REL) return; REL.lang=b.dataset.l;
  document.querySelectorAll('#rellang button').forEach(x=>x.classList.toggle('on',x===b)); $('reltxt').value=TXT[b.dataset.l](REL.nom,REL.dus,REL.tot,REL.soc); });
function relFaite(voie){ if(!REL) return; const d=ajd();
  REL.dus.forEach(o=>{ const k=pkey(REL.nom,o.x); PAY[k]=Object.assign({},payInit(REL.nom,o.x),PAY[k]||{},{rel:d}); }); sauvePAY();
  journal('client','relance de paiement ('+voie+')',REL.nom,money(REL.tot)+' · '+REL.dus.length+' commande'+(REL.dus.length>1?'s':''));
  $('relmsg').textContent='relance notée dans le journal — '+voie;
  /* la fenêtre se referme d'elle-même : laissée ouverte, on croit qu'il ne s'est rien passé */
  setTimeout(()=>{ $('relov').classList.remove('on'); REL=null; }, 1400);
  ouvre(REL.nom); onglet('cmd'); }
$('relmail').onclick=()=>{ if(!REL) return;
  const dest=$('reldest').value.trim();
  /* Sans adresse, on ne note rien : une relance inscrite au journal alors qu'aucun
     message n'est parti, c'est pire que pas de relance du tout. */
  if(!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(dest)){
    $('reldest').classList.add('manque'); $('reldest').focus();
    $('reldn').textContent='adresse manquante ou mal écrite'; $('reldn').className='err';
    $('relmsg').textContent='rien n\'a été envoyé'; return; }
  $('reldest').classList.remove('manque'); $('reldn').textContent=''; $('reldn').className='';
  /* l'adresse tapée ici est gardée dans la fiche : on ne la retape pas au prochain retard */
  const co=CLI[REL.nom]||{};
  if(co.email!==dest){ CLI[REL.nom]=Object.assign({},co,{nom:REL.nom,email:dest,maj:new Date().toISOString()});
    sauveCLI(); journal('client','e-mail du client enregistré',REL.nom,dest); }
  const suj={fr:'Rappel de règlement',en:'Payment reminder',es:'Recordatorio de pago'}[REL.lang];
  const url='mailto:'+encodeURIComponent(dest)+'?subject='+encodeURIComponent(suj+' — '+REL.soc)
    +'&body='+encodeURIComponent($('reltxt').value);
  /* un lien cliqué ouvre le logiciel de messagerie sans quitter la page ;
     location.href, lui, faisait parfois disparaître la fenêtre sans rien ouvrir */
  const a=document.createElement('a'); a.href=url; a.style.display='none';
  document.body.appendChild(a); a.click(); setTimeout(()=>a.remove(),0);
  relFaite('e-mail'); };
$('relwa').onclick=()=>{ if(!REL) return; const co=CLI[REL.nom]||{}; const tel=(co.tel||'').replace(/[^0-9]/g,'');
  if(!tel){ $('relmsg').textContent='pas de téléphone dans la fiche : ajoute-le dans Coordonnées'; return; }
  window.open('https://wa.me/'+(tel.length===10?'1'+tel:tel)+'?text='+encodeURIComponent($('reltxt').value),'_blank'); relFaite('WhatsApp'); };
$('relcopy').onclick=async()=>{ try{ await navigator.clipboard.writeText($('reltxt').value); }catch(e){ $('reltxt').select(); document.execCommand('copy'); } relFaite('texte copié'); };
$('relx').onclick=()=>{ $('relov').classList.remove('on'); REL=null; };

function onglet(t){ document.querySelectorAll('.tab').forEach(b=>b.classList.toggle('on',b.dataset.t===t));
  document.querySelectorAll('.pane').forEach(p=>p.classList.toggle('on',p.id==='p-'+t)); }
document.querySelectorAll('.tab').forEach(b=>b.onclick=()=>onglet(b.dataset.t));
/* Les coordonnées ne s'enregistrent qu'au bouton : on ne referme pas la fiche sur une
   saisie non enregistrée sans le dire. */
function coordChangees(){
  if(!OUV) return false;
  const co=CLI[OUV.nom]||{};
  return ['tel','email','raison','adresse','note'].some(k=>{
    const el=$('e-'+k); return el && el.value.trim()!==((co[k]||'').trim()); });
}
function ferme(force){
  if(!force && coordChangees() && !confirm("Les coordonnées saisies ne sont pas enregistrées.\n\nFermer quand même ? Ce qui a été tapé sera perdu.")) return;
  $('dr').classList.remove('on'); $('drov').classList.remove('on'); OUV=null;
}
$('dx').onclick=()=>ferme(false); $('drov').onclick=()=>ferme(false);
document.addEventListener('keydown',e=>{ if(e.key==='Escape'){ if(REL){ $('relov').classList.remove('on'); REL=null; } else if(OUV) ferme(false); } });

['q','per'].forEach(i=>$(i).addEventListener('input',dessine));
poseSortie('exp', ()=>{
  const L=[];
  D.clients.forEach(cl=>cl.cmds.forEach(x=>x.l.forEach(l=>L.push([
    cl.nom, x.d||'', x.de?'estimée':'', x.num, x.devis?'devis':'',
    l[BC], l[NOM], l[ML], l[MARQUE], l[TYPE],
    l[P]==null?null:+l[P], l[Q]==null?null:+l[Q], l[T]==null?null:+l[T],
    l[FACT], l[SORTI], l[NOTE]]))));
  return {
    titre:'VIP wholesale',
    fichier:'vip-wholesale',
    filtre:'toutes les commandes du tableur, lues le '+dfr(D.date),
    colonnes:[{t:'Client'},{t:'Date',y:'d'},{t:'Date estimée'},{t:'N° commande'},{t:'Devis'},
      {t:'Code-barres'},{t:'Parfum'},{t:'Contenance'},{t:'Marque'},{t:'Type'},
      {t:'Prix',y:'m'},{t:'Quantité',y:'n'},{t:'Montant',y:'m'},
      {t:'Facturée'},{t:'Sortie du stock'},{t:'Note'}],
    lignes:L
  };
});

$('notetxt').innerHTML=`Tout vient de l'onglet « carmen » du Google Sheet, lu le ${dfr(D.date)} : ${nf(D.clients.reduce((a,c)=>a+c.cmds.length,0))} commandes,
  ${nf(D.clients.reduce((a,c)=>a+c.cmds.reduce((s,x)=>s+x.l.length,0),0))} lignes.<br>
  <b>Dates</b> : elles sont lues dans le titre de la commande (« Javier 1669 10/5 ») ; quand elles manquent, la date de la commande voisine est reprise et marquée ≈.<br>
  <b>Noms</b> : Juan / Juan Carlos, Nelli / Nelly, Aroma / Aroma360, George / Signature Scent… sont regroupés sous un seul client (onglet Coordonnées : comment il est écrit dans le tableur).<br>
  <b>Devis</b> : les « quote » ne comptent pas dans les achats. <b>À vérifier</b> : deux commandes portent un montant invraisemblable, elles sont laissées de côté.<br>
  Mise à jour : exporter l'onglet en CSV, puis <code>outils/build_clients_data.py</code> et <code>build_clients.py</code>.`;

$('sfu').innerHTML = USR ? `Connecté : <b>${esc(USR)}</b>` : '';
$('sfoot').innerHTML='gros clients<br>depuis le tableur';
dessine();
"""

html = coquille("VIP wholesale", "VIP wholesale",
  "Les clients à qui il vend en gros. Pour chacun : ce qu'il lui a vendu, combien de commandes, "
  "quand, quels parfums — et ce qui reste à payer. Lu depuis l'onglet « carmen » du tableur.",
  CSS, CORPS, JS, donnees=('produits','clients'))
_donnees.pose('clients', DATA, 'D_CLI')
html = html.replace('__DATA__', 'window.D_CLI')
html = html.replace('__BC2CLE__',
  'Object.fromEntries(D_TOUS().filter(r=>r[0]).map(r=>[String(r[0]).replace(/^0+/,\'\'),r[15]]))')
open('clients.html', 'w').write(html)
print('clients.html', len(html)//1024, 'Ko')
