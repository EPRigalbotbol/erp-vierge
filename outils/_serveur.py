# -*- coding: utf-8 -*-
"""Les données de l'entreprise sur le serveur (le cockpit), et plus seulement dans le navigateur.

Avant : chaque navigateur avait SON stock, SES ventes, SON journal. Quatre comptes, quatre
vérités. Et vider le navigateur effaçait tout.

Maintenant, en ligne :
  1. AMORCE — avant que la page ne lise quoi que ce soit, on demande au cockpit ce qui a changé
     depuis la dernière visite (on lui envoie les versions qu'on connaît, il ne renvoie que le
     reste) et on le pose dans le navigateur, qui reste la copie de travail.
  2. SYNC — chaque `ecrit()` part au serveur avec le numéro de version sur lequel on s'appuie.
     Si quelqu'un a écrit entre-temps, le serveur refuse, renvoie sa version, et on fusionne ici
     (la même fusion qu'entre deux onglets) avant de renvoyer.
  3. Toutes les 45 s, on regarde si quelqu'un d'autre a écrit ; si oui on met la copie locale à
     jour et on propose de recharger.
En local (fichier, localhost), rien de tout ceci ne s'active : SAM marche comme avant.
"""

# Magasins qui restent propres à l'appareil (préférences d'affichage, session, clés API…).
EXCLUS = ['sam-session-v1', 'ck-token', 'ck-versions', 'crm-utilisateur-v1', 'crm-utilisateurs-v1',
          'sam-comptes-v1', 'sam-roles-v1', 'sam-comptes-demo-v1', 'frn-demo-galou-v1',
          'vue-catalogue-v1', 'tri-colonne-v1', 'retail-vue-v1', 'langue-v1', 'menu-perso-v1',
          'dossier-outil-v1', 'repere-installation-v1', 'derniere-sauvegarde-v1',
          'derniere-sauvegarde-compte-v1', 'connecteurs-v1']

# Ce qui tourne AVANT le code de la page : on remplit le navigateur depuis le serveur, puis on lance la page.
AMORCE = r"""
(function(){
  const url=(typeof COCKPIT_URL!=='undefined'&&COCKPIT_URL)||'https://cockpit.igalbotbol.com';
  const org=(typeof COCKPIT_ORG!=='undefined'&&COCKPIT_ORG)||'dasy';
  const enLigne=location.protocol!=='file:' && !/^(localhost|127\.0\.0\.1|\[::1\])$/.test(location.hostname);
  let tok=''; try{ tok=localStorage.getItem('ck-token')||''; }catch(e){}
  const K_V='ck-versions';
  window.__CK={url,org,enLigne,hors:false,charge:null};
  function lance(){
    /* dossier « donnees » absent : le garde-fou a déjà écrit l'explication, on ne démarre pas */
    if(window.__DONNEES_MANQUENT) return;
    /* la page s'attendait à démarrer avec le document : on rejoue ces événements pour elle */
    const ael=document.addEventListener.bind(document), wael=window.addEventListener.bind(window);
    document.addEventListener=function(t,f,o){ if(t==='DOMContentLoaded'&&document.readyState!=='loading'){ setTimeout(()=>f.call(document,new Event('DOMContentLoaded')),0); } else ael(t,f,o); };
    window.addEventListener=function(t,f,o){ if((t==='load'&&document.readyState==='complete')||(t==='DOMContentLoaded'&&document.readyState!=='loading')){ setTimeout(()=>f.call(window,new Event(t)),0); } else wael(t,f,o); };
    const src=document.getElementById('page-js'); const s=document.createElement('script');
    s.textContent=src.textContent; if(src.dataset.module) s.type='module'; src.remove(); document.body.appendChild(s);
  }
  if(!enLigne||!tok){ lance(); return; }
  let V={}; try{ V=JSON.parse(localStorage.getItem(K_V)||'{}')||{}; }catch(e){ V={}; }
  const ctrl=new AbortController(); const tm=setTimeout(()=>ctrl.abort(),12000);
  fetch(url+'/api/o/'+org+'/donnees/lire',{method:'POST',signal:ctrl.signal,
    headers:{'Content-Type':'application/json',Authorization:'Bearer '+tok},body:JSON.stringify({versions:V})})
  .then(async r=>{
    clearTimeout(tm);
    if(r.status===401){
      try{ localStorage.removeItem('ck-token'); localStorage.removeItem('sam-session-v1'); }catch(e){}
      if(!/accueil\.html$/.test(location.pathname)){ location.replace('accueil.html'); return; }
      lance(); return;
    }
    if(!r.ok) throw new Error('serveur '+r.status);
    const j=await r.json();
    for(const k in j.magasins){ try{ localStorage.setItem(k,JSON.stringify(j.magasins[k].val)); }catch(e){} }
    (j.disparus||[]).forEach(k=>{ try{ localStorage.removeItem(k); }catch(e){} });
    try{ localStorage.setItem(K_V,JSON.stringify(j.versions||{})); }catch(e){}
    window.__CK.charge=j.versions||{};
    lance();
  })
  .catch(e=>{ clearTimeout(tm); window.__CK.hors=true; lance(); });
})();
"""

# Ce qui s'ajoute au code de la page, juste après les comptes : l'envoi au serveur.
SYNC = r"""
/* ============ EN LIGNE : LES DONNÉES VIVENT SUR LE SERVEUR ============ */
const _SY_EXCLUS=new Set(__EXCLUS__);
const _SY_ON=EN_LIGNE && !!ckTok();
const _SY_K='ck-versions';
let _SY_V={}; try{ _SY_V=JSON.parse(localStorage.getItem(_SY_K)||'{}')||{}; }catch(e){ _SY_V={}; }
const _SY_BASE={};          /* la valeur telle qu'on l'a reçue du serveur (point de comparaison pour fusionner) */
const _SY_ATT=new Map();    /* magasins en attente d'envoi : cle -> {val} */
const _SY_ENVOI=new Set();  /* envois en cours */
let _SY_HORS=!!(window.__CK&&window.__CK.hors);
const _sySauveV=()=>{ try{ localStorage.setItem(_SY_K,JSON.stringify(_SY_V)); }catch(e){} };
const _syOk=cle=>_SY_ON && !_SY_EXCLUS.has(cle) && /^[a-z0-9-]+-v\d+$/.test(cle);

/* on garde la version "serveur" de chaque magasin lu, pour savoir plus tard ce que CET appareil a changé */
{ const _lit0=lit; lit=(k,d)=>{ const v=_lit0(k,d); if(_syOk(k)&&!(k in _SY_BASE)) _SY_BASE[k]=_cp(v); return v; }; }

/* le voyant : ce qui n'est pas encore parti */
function _syVoyant(){
  let b=document.getElementById('sy-voyant');
  const n=_SY_ATT.size+_SY_ENVOI.size;
  if(!n&&!_SY_HORS){ if(b) b.remove(); return; }
  if(!document.body) return;
  if(!b){ b=document.createElement('div'); b.id='sy-voyant';
    b.style.cssText='position:fixed;right:16px;bottom:16px;z-index:9998;background:#1c1b22;color:#fff;padding:8px 12px;border-radius:9px;font:500 12px Inter,system-ui,sans-serif;box-shadow:0 8px 24px rgba(0,0,0,.3);display:flex;gap:8px;align-items:center';
    document.body.appendChild(b); }
  b.textContent=_SY_HORS?('⚠ Serveur injoignable — '+n+' modification'+(n>1?'s':'')+' en attente'):('Enregistrement… '+n);
  b.style.background=_SY_HORS?'#8a2f2f':'#1c1b22';
}

async function _syPut(cle,val){
  const r=await fetch(CK_URL+'/api/o/'+CK_ORG+'/donnees/'+encodeURIComponent(cle),{method:'PUT',
    headers:{'Content-Type':'application/json',Authorization:'Bearer '+ckTok()},
    body:JSON.stringify({val,base:_SY_V[cle]||0})});
  if(r.status===401){ ckPerdu(); throw new Error('session'); }
  const j=await r.json().catch(()=>({}));
  if(r.status===409){
    /* quelqu'un a écrit entre-temps : on fusionne sa version avec ce que cet appareil a changé */
    const fus=fusionne(cle,j.val,_SY_BASE[cle],val);
    _SY_V[cle]=j.ver; _SY_BASE[cle]=_cp(j.val);
    try{ localStorage.setItem(cle,JSON.stringify(fus)); }catch(e){}
    _adopte(val,fus); _REF[cle]=_cp(val);
    avertitMaj('Quelqu\'un d\'autre vient de modifier les données ('+(j.par||'')+'). Elles ont été fusionnées.');
    return _syPut(cle,val);
  }
  if(!r.ok) throw new Error(j.erreur||('serveur '+r.status));
  _SY_V[cle]=j.ver; _SY_BASE[cle]=_cp(val); _sySauveV();
}

/* pour les listes à identifiant (journal, factures…) : on n'envoie que ce qui a été ajouté ou retiré */
async function _syPatch(cle,val,avant){
  const idf=_ID[cle]||_IDdef;
  const mA=new Map((avant||[]).map(x=>[idf(x),x])), mV=new Map((val||[]).map(x=>[idf(x),x]));
  const ajoute=[], retire=[];
  for(const [i,x] of mV){ if(!mA.has(i)) ajoute.push(x); else if(_sig(mA.get(i))!==_sig(x)) return _syPut(cle,val); }
  for(const i of mA.keys()) if(!mV.has(i)) retire.push(i);
  if(!ajoute.length&&!retire.length) return;
  const r=await fetch(CK_URL+'/api/o/'+CK_ORG+'/donnees/'+encodeURIComponent(cle)+'/delta',{method:'POST',
    headers:{'Content-Type':'application/json',Authorization:'Bearer '+ckTok()},
    body:JSON.stringify({ajoute,retire,max:_MAX[cle]||0,date:_DATE[cle]?'t':''})});
  if(r.status===401){ ckPerdu(); throw new Error('session'); }
  const j=await r.json().catch(()=>({}));
  if(!r.ok) throw new Error(j.erreur||('serveur '+r.status));
  _SY_V[cle]=j.ver; _SY_BASE[cle]=_cp(val); _sySauveV();
}

async function _syPousse(cle){
  if(_SY_ENVOI.has(cle)) return;
  const e=_SY_ATT.get(cle); if(!e) return;
  _SY_ATT.delete(cle); _SY_ENVOI.add(cle); _syVoyant();
  try{
    if(_UID[cle]&&Array.isArray(e.val)&&Array.isArray(e.avant)&&_SY_V[cle]) await _syPatch(cle,e.val,e.avant);
    else await _syPut(cle,e.val);
    _SY_HORS=false;
  }catch(err){
    if(err.message!=='session'){ _SY_HORS=true; if(!_SY_ATT.has(cle)) _SY_ATT.set(cle,e); }
  }
  _SY_ENVOI.delete(cle); _syVoyant();
  if(_SY_ATT.has(cle)&&!_SY_HORS) _syPousse(cle);
}
_apresEcrit.push((cle,val,avant)=>{
  if(!_syOk(cle)) return;
  const e=_SY_ATT.get(cle);
  _SY_ATT.set(cle,{val,avant:e?e.avant:avant});
  _syPousse(cle);
});
/* ce qui n'est pas parti (serveur injoignable) repart tout seul */
setInterval(()=>{ if(_SY_ATT.size&&!_SY_ENVOI.size){ _SY_HORS=false; for(const k of _SY_ATT.keys()) _syPousse(k); } },20000);
window.addEventListener('beforeunload',e=>{ if(_SY_ATT.size||_SY_ENVOI.size){ e.preventDefault(); e.returnValue='Des modifications ne sont pas encore enregistrées sur le serveur.'; } });

/* premier passage : le serveur n'a encore rien, cet appareil a tout → on l'y dépose */
if(_SY_ON && window.__CK && window.__CK.charge && !Object.keys(window.__CK.charge).length){
  const cles=[]; try{ for(let i=0;i<localStorage.length;i++){ const k=localStorage.key(i); if(_syOk(k)) cles.push(k); } }catch(e){}
  cles.forEach(k=>{ const v=_dq(k,null); if(v!=null){ _SY_ATT.set(k,{val:v,avant:null}); } });
  if(cles.length){ console.log('cockpit : premier dépôt de',cles.length,'magasins'); for(const k of _SY_ATT.keys()) _syPousse(k); }
}

/* toutes les 45 s : quelqu'un d'autre a-t-il écrit ? */
async function _syVeille(){
  if(!_SY_ON||_SY_ENVOI.size||_SY_ATT.size||document.hidden) return;
  try{
    const r=await fetch(CK_URL+'/api/o/'+CK_ORG+'/donnees/versions',{headers:{Authorization:'Bearer '+ckTok()}});
    if(r.status===401){ ckPerdu(); return; }
    if(!r.ok) return;
    const V=await r.json();
    const chg=Object.keys(V).filter(k=>_syOk(k)&&V[k]!==(_SY_V[k]||0));
    if(!chg.length) return;
    const r2=await fetch(CK_URL+'/api/o/'+CK_ORG+'/donnees/lire',{method:'POST',headers:{'Content-Type':'application/json',Authorization:'Bearer '+ckTok()},body:JSON.stringify({versions:_SY_V})});
    if(!r2.ok) return;
    const j=await r2.json(); let qui='', touche=false;
    for(const k in j.magasins){ if(!_syOk(k)) continue;
      try{ localStorage.setItem(k,JSON.stringify(j.magasins[k].val)); }catch(e){}
      _SY_BASE[k]=_cp(j.magasins[k].val); qui=j.magasins[k].par||qui; if(k in _REF) touche=true; }
    _SY_V=j.versions||_SY_V; _sySauveV();
    if(touche) avertitMaj('Les données ont été modifiées'+(qui?' par '+qui:'')+'.');
  }catch(e){}
}
setInterval(_syVeille,45000);
"""


def sync_js():
    import json
    return SYNC.replace('__EXCLUS__', json.dumps(EXCLUS))


def enligne(html):
    """Transforme la page pour que son code attende les données du serveur avant de tourner.

    Le grand <script> de fin de page devient un bloc inerte (type="text/plain"), et un petit
    script le lance une fois l'AMORCE passée. En local l'AMORCE lance tout de suite.
    """
    fin = '</script></body></html>'
    if not html.rstrip().endswith(fin):
        raise SystemExit('enligne : la page ne finit pas par ' + fin)
    i = html.rfind('<script>')
    if i < 0:
        raise SystemExit('enligne : pas de <script> final')
    corps = html[i + len('<script>'):html.rstrip().rfind(fin)]
    if '</script' in corps:
        raise SystemExit('enligne : "</script" dans le code de la page')
    return (html[:i] + '<script type="text/plain" id="page-js">' + corps + '</script>\n<script>'
            + AMORCE + '</script></body></html>\n')
