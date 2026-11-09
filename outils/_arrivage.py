# NOUVEAUX ARRIVAGES → CLIENTS FAVORIS (Igal, 8 nov. 2026). Le code de la fenêtre et de la feuille PDF, écrit dans
# lib/arrivage.js à chaque construction du Catalogue (build_html.py) : il n'est chargé que lorsque la fenêtre s'ouvre.
import pathlib, json
# les messages d'origine (Igal, 8 nov. 2026 : « veuillez trouver ci-joint nos new arrivals ») — modifiables dans Réglages
MSG_DEF = {
    'en': 'Hello {prenom},\n\nPlease find attached our New Arrivals:\n{lien}\n\nPrices on request — reply with the barcode and the quantity.\n\nPerfumes Trade',
    'fr': 'Bonjour {prenom},\n\nVeuillez trouver ci-joint nos nouveaux arrivages :\n{lien}\n\nPrix sur demande — répondez-nous avec le code-barres et la quantité.\n\nPerfumes Trade',
    'es': 'Hola {prenom},\n\nLe enviamos adjuntos nuestros nuevos arribos:\n{lien}\n\nPrecios a solicitud — respóndanos con el código de barras y la cantidad.\n\nPerfumes Trade'}
CSS = r'''/* ===== NOUVEAUX ARRIVAGES (8 nov. 2026) : la fenêtre d'envoi, puis la feuille photographiée en PDF ===== */
#arrov .mod{max-width:900px;width:100%}
.arr-sous{margin:0 0 6px;color:var(--ink-3);font-size:13px}
.arr-autre{display:block;font-size:13px;margin:2px 0 6px;color:var(--ink-2)}
.arr-tete{display:flex;justify-content:space-between;align-items:center;gap:10px;flex-wrap:wrap;margin:14px 0 8px}
.arr-tete b{font-size:15px}
.arr-grille{display:grid;grid-template-columns:repeat(auto-fill,minmax(118px,1fr));gap:8px;max-height:300px;overflow:auto;padding:2px}
.arr-p{position:relative;display:flex;flex-direction:column;gap:4px;border:1px solid var(--line);border-radius:8px;padding:6px;cursor:pointer;opacity:.45;background:var(--surface)}
.arr-p.on{opacity:1;border-color:#b08d57;box-shadow:0 0 0 1px #b08d57 inset}
.arr-p input{position:absolute;top:6px;left:6px}
.arr-ph{display:flex;align-items:center;justify-content:center;aspect-ratio:1;background:#fff;border-radius:5px;overflow:hidden}
.arr-ph img{width:100%;height:100%;object-fit:contain}.arr-ph em{font-size:11px;color:var(--ink-3)}
.arr-pn{font-size:12px;line-height:1.25}.arr-pn small{display:block;font-size:10px;letter-spacing:.08em;text-transform:uppercase;color:#a8854f}
.arr-wa-choix{font-size:13px;color:var(--ink-2)}.arr-wa-choix label{margin-left:8px;white-space:nowrap}
.arr-etat{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:8px}
.arr-pill{font-size:12px;padding:3px 9px;border-radius:999px;background:var(--surface-2);color:var(--ink-2)}
.arr-pill.ok{background:#e6f4ea;color:#1e6b34}.arr-pill.err{background:var(--crit-soft,#fdecea);color:var(--crit,#b3261e)}
.arr-d{display:flex;align-items:center;gap:10px;padding:8px 10px;border:1px solid var(--line);border-radius:8px;margin-bottom:6px;cursor:pointer}
.arr-d.on{border-color:#25d366;box-shadow:0 0 0 1px #25d366 inset}
.arr-sel{display:flex;gap:8px;align-items:center;margin-bottom:8px}.arr-sel .hint{margin:0}
.arr-go{display:flex;justify-content:flex-end;margin-top:10px}.arr-go .btn{font-size:15px;padding:10px 18px}
.btn.arr-wa:disabled{background:var(--surface-2);border-color:var(--line);color:var(--ink-3)}

.arr-d.fait{background:#f3faf5}
.arr-dn{flex:1;min-width:0}.arr-dn small{display:block;color:var(--ink-3);font-size:12px}
.arr-st{font-size:12.5px;color:#1e6b34;min-width:70px;text-align:right}
.btn.arr-wa{background:#25d366;border-color:#25d366;color:#fff;font-weight:600}
.btn.arr-wa:hover{background:#1ebe5b}
/* la feuille (816 × 1056 px = une page Letter), hors de l'écran le temps de la photo */
.arr-feuille{position:absolute;left:-12000px;top:0;width:816px;background:#fff;color:#1c1b19;font-family:ArrSans,Inter,Helvetica,Arial,sans-serif}
.arr-feuille *{box-sizing:border-box;margin:0;padding:0;border:0;float:none;text-transform:none;letter-spacing:normal;font-style:normal;line-height:1.3}
.arr-feuille .apg{width:816px;height:1056px;padding:36px 38px 38px;position:relative;display:flex;flex-direction:column;background:#fff;overflow:hidden}
.arr-feuille .ah1{text-align:center;margin-bottom:15px}
.arr-feuille .alogo{width:211px;display:block;margin:0 auto}
.arr-feuille .alogot{font-family:ArrSerif;font-size:30px;letter-spacing:.2em;text-transform:uppercase}
.arr-feuille .afil{display:flex;align-items:center;justify-content:center;gap:10px;margin:10px auto 6px;width:326px}
.arr-feuille .afil span{flex:1;height:1px;background:#c9ad7f}
.arr-feuille .afil b{width:5px;height:5px;background:#a8854f;transform:rotate(45deg);display:block}
.arr-feuille .atitre{font-family:ArrSerif;font-weight:600;font-size:34px;letter-spacing:.3em;text-transform:uppercase;padding-left:.3em;line-height:1.15}
.arr-feuille .amois{font-size:9.5px;letter-spacing:.22em;text-transform:uppercase;color:#8a7a62;margin-top:4px}
.arr-feuille .aintro{font-family:ArrSerif;font-weight:500;font-size:15.5px;font-style:italic;color:#4a453d;margin-top:7px}
.arr-feuille .atel{font-size:10.5px;letter-spacing:.08em;margin-top:6px}
.arr-feuille .atel b{font-weight:600}
.arr-feuille .ah2{display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid #c9ad7f;padding-bottom:9px;margin-bottom:18px}
.arr-feuille .alogo2{height:40px}
.arr-feuille .at2{font-family:ArrSerif;font-weight:600;font-size:17px;letter-spacing:.2em;text-transform:uppercase}
.arr-feuille .at2 span{font-family:ArrSans;font-weight:400;font-size:8.5px;letter-spacing:.16em;color:#8a7a62;text-transform:uppercase}
.arr-feuille .asans{font-family:ArrSerif;font-weight:500;font-size:15px;letter-spacing:.12em;text-transform:uppercase;color:#c9ad7f;padding:0 12px;text-align:center}
.arr-feuille .ag{display:grid;grid-template-columns:repeat(4,1fr);gap:12px 12px;align-content:start}
.arr-feuille .ac{text-align:center}
.arr-feuille .aph{width:161px;height:161px;margin:0 auto;border:1px solid #ece6dc;border-radius:3px;display:flex;align-items:center;justify-content:center;overflow:hidden;background:#fff}
.arr-feuille .aph img{width:100%;height:100%;object-fit:contain}
.arr-feuille .am{font-size:8.5px;font-weight:600;letter-spacing:.2em;text-transform:uppercase;color:#a8854f;margin-top:7px}
.arr-feuille .an{font-family:ArrSerif;font-weight:600;font-size:16.5px;line-height:1.08;margin-top:2px}
.arr-feuille .ad{font-size:9px;color:#5f5a52;margin-top:3px}
.arr-feuille .abc{font-size:9.5px;letter-spacing:.02em;margin-top:4px;display:inline-block;border-top:1px solid #ece6dc;padding-top:3px}
.arr-feuille .acta{margin-top:auto;margin-bottom:22px;border:1px solid #c9ad7f;padding:13px 19px;text-align:center;background:#faf7f1}
.arr-feuille .act1{font-family:ArrSerif;font-weight:600;font-size:18px;letter-spacing:.14em;text-transform:uppercase}
.arr-feuille .act2{font-size:9.5px;color:#4a453d;margin-top:4px}
.arr-feuille .act3{font-size:11px;font-weight:600;letter-spacing:.06em;margin-top:5px}
.arr-feuille .apied{position:absolute;left:38px;right:38px;bottom:25px;display:flex;justify-content:space-between;font-size:7.5px;color:#8a8478;border-top:1px solid #ece6dc;padding-top:5px}'''
JS = r'''/* ============ NOUVEAUX ARRIVAGES → CLIENTS FAVORIS (Igal, 8 nov. 2026) ============
   « À chaque fois que Sam rentre une new order, une fenêtre s'ouvre : est-ce que vous voulez l'envoyer à vos clients favoris ? »
   La liste des parfums reçus, SANS prix (photo, marque, nom, contenance, code-barres), avec le logo et le WhatsApp de Sam, en PDF ;
   un petit message « veuillez trouver ci-joint nos nouveaux arrivages » en anglais, français ou espagnol (la langue du client) ;
   envoyé depuis le WhatsApp de l'ORDINATEUR de Sam (l'application, ou WhatsApp Web).
   WhatsApp ne laisse aucun site joindre un fichier : le message porte le lien du PDF, que WhatsApp montre en carte avec l'image
   de la première page (la page publique du cockpit, comme les cotes). Le PDF est fabriqué ici, une fois par langue, PRÊT avant
   le clic : un clic sur un client ouvre WhatsApp tout de suite (un lien ouvert après une longue attente serait bloqué).
   Ouvert en cadre depuis Factures (catalogue.html#arrivage=<id facture>&cadre=1) : ici vivent les photos et les fiches. */
const K_ARR_E='arrivages-envoyes-v1';
const ARR_LG={en:'English',fr:'Français',es:'Español'};
const ARR_T={
  en:{titre:'New Arrivals',intro:n=>`${n} fragrance${n>1?'s':''} just landed in our Miami warehouse. Available now for our partners.`,prix:'Prices on request',cta:'Send us the barcode and the quantity on WhatsApp — we reply the same day.',g:{M:'Men',W:'Women',F:'Women',U:'Unisex'},fic:'New-Arrivals',},
  fr:{titre:'Nouveaux arrivages',intro:n=>`${n} parfum${n>1?'s':''} vien${n>1?'nent':'t'} d'arriver dans notre entrepôt de Miami. Disponible${n>1?'s':''} dès maintenant pour nos partenaires.`,prix:'Prix sur demande',cta:'Envoyez-nous le code-barres et la quantité sur WhatsApp — réponse le jour même.',g:{M:'Homme',W:'Femme',F:'Femme',U:'Mixte'},fic:'Nouveaux-arrivages',},
  es:{titre:'Nuevos arribos',intro:n=>`${n} perfume${n>1?'s':''} acaba${n>1?'n':''} de llegar a nuestro almacén de Miami. Disponible${n>1?'s':''} ya para nuestros socios.`,prix:'Precios a solicitud',cta:'Envíenos el código de barras y la cantidad por WhatsApp — respondemos el mismo día.',g:{M:'Hombre',W:'Mujer',F:'Mujer',U:'Unisex'},fic:'Nuevos-arribos',}};
/* le message qui part avec le lien : celui des Réglages (Ma société › Message des nouveaux arrivages), sinon celui d'origine.
   {prenom} = le prénom du client, {lien} = le lien du PDF ; sans {lien}, le lien est ajouté à la fin (il ne peut pas manquer) */
const ARR_MSG_DEF=__MSG_DEF__;
function arrMessage(lg,prenom,lien){
  let R={}; try{ R=(lit('reglages-v1',{})||{}).arrMsg||{}; }catch(e){}
  let t=String((R&&R[lg])||ARR_MSG_DEF[lg]||ARR_MSG_DEF.en);
  if(!/\{lien\}/i.test(t)) t=t.replace(/\s+$/,'')+'\n\n{lien}';
  t=prenom?t.replace(/\{prenom\}/gi,prenom):t.replace(/ ?\{prenom\}/gi,'');
  return t.replace(/\{lien\}/gi,lien);
}
const ARR_TYPE={EDP:'Eau de Parfum',EDT:'Eau de Toilette',EDC:'Eau de Cologne',P:'Parfum',PARFUM:'Parfum',EXTRAIT:'Extrait de Parfum',ELIXIR:'Elixir'};
let ARR=null;
const arrT=(a,b,c)=>(typeof L3==='function'?L3(a,b,c):a);
const arrNum=v=>{ let d=String(v||'').replace(/\D/g,''); if(!d) return ''; if(d.length===10) d='1'+d; if(d.length===11&&d[0]==='1') return d; return (d.length>=8&&d.length<=15)?d:''; };
const arrNorm=s=>String(s||'').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g,'').replace(/[^a-z0-9]+/g,'');
/* les mots tout en capitales deviennent lisibles (« PURE PLATINUM » → « Pure Platinum ») ; les sigles courts restent */
const arrCasse=s=>String(s||'').split(/\s+/).filter(Boolean).map(w=>(w.length>3&&w===w.toUpperCase()&&/[A-Z]/.test(w)&&!/^(EDP|EDT|EDC|VIP|NYC)$/.test(w))?w[0]+w.slice(1).toLowerCase():w).join(' ');
/* les clients favoris (l'étoile de Clients), avec un numéro : la fiche favorite et ses doublons de nom sont réunis */
function arrFavoris(){
  const C=lit('clients-v1',{})||{}, G={};
  Object.keys(C).forEach(k=>{ const c=C[k]; if(!c||typeof c!=='object') return; const g=arrNorm(k); if(!g) return; (G[g]=G[g]||[]).push(Object.assign({nom:k},c)); });
  const out=[];
  Object.values(G).forEach(L=>{ if(!L.some(c=>c.vip)) return;
    const v=L.find(c=>c.vip)||L[0], prend=k=>{ const c=[v].concat(L).find(x=>x[k]); return c?c[k]:''; };
    const tel=[prend('tel'),prend('tel2'),prend('tel3')].map(arrNum).find(Boolean)||'';
    const lg=String(prend('langue')||'').toLowerCase().slice(0,2);
    const prenom=String(prend('prenom')||'').trim()||String(v.nom||'').trim().split(/\s+/)[0]||'';
    if(prend('nodiff')) return;   /* désinscrit de la liste de diffusion */
    out.push({nom:v.nom,tel,lg:ARR_LG[lg]?lg:'en',prenom}); });
  return out.sort((a,b)=>a.nom.localeCompare(b.nom));
}
/* les parfums d'une réception (et des autres réceptions du même jour, cochables) */
function arrReceptions(fid){
  const F=lit('factures-v1',[])||[]; const f=F.find(x=>x&&x.id===fid);
  if(!f) return null;
  const memeJour=F.filter(x=>x&&x.id!==fid&&x.sens==='achat'&&!x.annule&&x.d===f.d&&!x.canal);
  return {f,memeJour};
}
function arrLignes(factures){
  const arts=tousLesArticles(), par={}; arts.forEach(a=>{ if(a.cle) par[a.cle]=a; if(a.id) par[a.id]=par[a.id]||a; });
  const parBc={}; arts.forEach(a=>{ const k=String(a.bc||'').replace(/^0+/,''); if(k&&!parBc[k]) parBc[k]=a; });
  const vus=new Set(), out=[];
  factures.forEach(f=>(f.lignes||[]).forEach(l=>{ if(!l||!(+l.q>0)) return;
    const a=par[l.cle]||parBc[String(l.bc||'').replace(/^0+/,'')]; if(!a) return;
    /* 9 nov. 2026 (Igal : « si un parfum revient sur les 2 ou 3 dernières commandes, pas de doublon ») : un parfum n'apparaît
       qu'une fois, reconnu par sa fiche, par son code-barres ou par marque + nom + contenance + type */
    const ks=[a.cle||a.id, 'bc:'+String(a.bc||'').replace(/[^0-9A-Za-z]/g,'').replace(/^0+/,''), 'n:'+arrNorm([a.marque,a.nom,a.ml,a.type].join(' '))]
      .filter(k=>k&&k!=='bc:'&&k!=='n:');
    if(ks.some(k=>vus.has(k))) return; ks.forEach(k=>vus.add(k)); out.push(a); }));
  return out.sort((x,y)=>(String(x.marque||'')+' '+x.nom).toLowerCase().localeCompare((String(y.marque||'')+' '+y.nom).toLowerCase()));
}
/* la photo, recadrée sur le flacon et posée au centre d'un carré blanc : chaque parfum occupe la même place sur la feuille */
const ARR_PH={};
async function arrPhoto(a){
  const k=a.cle||a.id; if(ARR_PH[k]!==undefined) return ARR_PH[k];
  const srcs=[a.imgPerso&&a.img, a.bc&&('photos/'+a.bc+'.webp'), !a.imgPerso&&a.img].filter(Boolean);
  for(const s of srcs){
    try{
      let url=s;
      if(!/^data:/.test(s)){ const r=await fetch(s,{cache:'force-cache'}); if(!r.ok) continue; const b=await r.blob(); if(!/^image\//.test(b.type)) continue; url=URL.createObjectURL(b); }
      const im=await new Promise((ok,ko)=>{ const i=new Image(); i.onload=()=>ok(i); i.onerror=ko; i.src=url; });
      const z=Math.min(1,800/Math.max(im.naturalWidth,im.naturalHeight)), w=Math.max(1,Math.round(im.naturalWidth*z)), h=Math.max(1,Math.round(im.naturalHeight*z));
      const c=document.createElement('canvas'); c.width=w; c.height=h; const x=c.getContext('2d'); x.fillStyle='#fff'; x.fillRect(0,0,w,h); x.drawImage(im,0,0,w,h);
      const d=x.getImageData(0,0,w,h).data; let x0=w,y0=h,x1=-1,y1=-1;
      for(let yy=0;yy<h;yy+=2) for(let xx=0;xx<w;xx+=2){ const i=(yy*w+xx)*4; if(d[i]<244||d[i+1]<244||d[i+2]<244){ if(xx<x0)x0=xx; if(xx>x1)x1=xx; if(yy<y0)y0=yy; if(yy>y1)y1=yy; } }
      if(x1<0){ x0=0;y0=0;x1=w-1;y1=h-1; }
      const cw=x1-x0+1, ch=y1-y0+1, s2=Math.round(Math.max(cw,ch)*1.12), o=document.createElement('canvas'); o.width=o.height=480;
      const ox=o.getContext('2d'); ox.fillStyle='#fff'; ox.fillRect(0,0,480,480); const f=480/s2;
      ox.drawImage(c,x0,y0,cw,ch,(480-cw*f)/2,(480-ch*f)/2,cw*f,ch*f);
      if(url!==s) URL.revokeObjectURL(url);
      return ARR_PH[k]=o.toDataURL('image/jpeg',0.86);
    }catch(e){}
  }
  return ARR_PH[k]=null;
}
/* la date d'une réception (« 2026-11-02 ») est un JOUR : lue telle quelle, sans fuseau (sinon Miami affichait « 1 novembre à 19:00 ») */
const arrJour=d=>{ const m=/^(\d{4})-(\d{2})-(\d{2})/.exec(String(d||'')); if(!m) return String(d||'');
  return new Date(+m[1],+m[2]-1,+m[3]).toLocaleDateString(typeof lgLocale==='function'?lgLocale():'fr-FR',{day:'numeric',month:'long',year:'numeric'}); };
const arrTaille=m=>{ const v=parseFloat(String(m||'').replace(',','.')); return isFinite(v)&&v>0?(Math.round(v*10)/10)+' oz':String(m||''); };
/* ---- la feuille : 12 parfums par page, la première avec le grand titre, la dernière avec « Prix sur demande » ---- */
function arrFeuilles(items,lg,F){
  /* le trait d'union devient insécable : le photographe (html2canvas) coupait « code-barres » en « code- barres » */
  const T=ARR_T[lg]||ARR_T.en, e=v=>esc(v).replace(/-/g,'\u2011'), logo=F.logo||'', tel=F.tel||'', N=Math.max(1,Math.ceil(items.length/12));
  const mois=new Date().toLocaleDateString(lg==='fr'?'fr-FR':lg==='es'?'es-ES':'en-US',{month:'long',year:'numeric'});
  const carte=x=>`<div class="ac"><div class="aph">${x.photo?`<img src="${x.photo}">`:`<span class="asans">${e(arrCasse(x.marque||''))}</span>`}</div><div class="am">${e(arrCasse(x.marque||''))}</div><div class="an">${e(arrCasse(x.nom||''))}</div>`
    +`<div class="ad">${e([arrTaille(x.ml),ARR_TYPE[String(x.type||'').toUpperCase()]||x.type||'',T.g[String(x.genre||'').toUpperCase()]||''].filter(Boolean).join(' · '))}</div><div class="abc">${e(String(x.bc||''))}</div></div>`;
  let h='';
  for(let i=0;i<N;i++){ const p=items.slice(i*12,i*12+12);
    h+=`<div class="apg">`+(i===0?`<div class="ah1">${logo?`<img class="alogo" src="${logo}">`:`<div class="alogot">${e(F.enseigne||'Perfumes Trade')}</div>`}<div class="afil"><span></span><b></b><span></span></div>`
        +`<div class="atitre">${e(T.titre)}</div><div class="amois">${e(mois)}</div><p class="aintro">${e(T.intro(items.length))}</p><div class="atel">${e(T.prix)} · WhatsApp <b>${e(tel)}</b></div></div>`
      :`<div class="ah2">${logo?`<img class="alogo2" src="${logo}">`:''}<div class="at2">${e(T.titre)} <span>· ${e(mois)}</span></div></div>`)
      +`<div class="ag">${p.map(carte).join('')}</div>`
      +(i===N-1?`<div class="acta"><div class="act1">${e(T.prix)}</div><div class="act2">${e(T.cta)}</div><div class="act3">WhatsApp ${e(tel)}</div></div>`:'')
      +`<div class="apied"><span>${e(F.enseigne||'')}${F.adresse?' · '+e(F.adresse):''}</span><span>${e(F.email||'')}${tel?' · '+e(tel):''}</span><span>${i+1} / ${N}</span></div></div>`; }
  return h;
}
async function arrPolices(){
  if(!document.getElementById('arr-fontes')){ const st=document.createElement('style'); st.id='arr-fontes';
    st.textContent="@font-face{font-family:ArrSerif;src:url(lib/fonts/cormorant-garamond-500.woff2) format('woff2');font-weight:500}@font-face{font-family:ArrSerif;src:url(lib/fonts/cormorant-garamond-600.woff2) format('woff2');font-weight:600}@font-face{font-family:ArrSans;src:url(lib/fonts/inter-400.woff2) format('woff2');font-weight:400}@font-face{font-family:ArrSans;src:url(lib/fonts/inter-600.woff2) format('woff2');font-weight:600}";
    document.head.appendChild(st); }
  try{ await Promise.all(['500 20px ArrSerif','600 20px ArrSerif','400 12px ArrSans','600 12px ArrSans'].map(f=>document.fonts.load(f))); }catch(e){}
}
/* le PDF d'une langue : la feuille photographiée page par page (comme les factures), puis rangée en Letter */
async function arrPdf(items,lg){
  if(typeof plPdfLibs==='function') await plPdfLibs();
  if(!window.html2canvas) await new Promise((ok,ko)=>{ const sc=document.createElement('script'); sc.src='lib/pdf/html2canvas.min.js'; sc.onload=ok; sc.onerror=()=>ko(new Error('Moteur PDF introuvable')); document.head.appendChild(sc); });
  await arrPolices();
  const F=((typeof REG!=='undefined'&&REG&&REG.fact)||(lit('reglages-v1',{})||{}).fact||{});
  const z=document.createElement('div'); z.className='arr-feuille'; z.innerHTML=arrFeuilles(items,lg,F); document.body.appendChild(z);
  try{
    await Promise.all([...z.querySelectorAll('img')].map(i=>i.complete?0:new Promise(r=>{ i.onload=i.onerror=r; })));
    const {jsPDF}=window.jspdf; const pdf=new jsPDF({unit:'pt',format:'letter',orientation:'portrait',compress:true});
    const W=pdf.internal.pageSize.getWidth(), H=pdf.internal.pageSize.getHeight(); let apercu=null;
    const pages=[...z.querySelectorAll('.apg')];
    for(let n=0;n<pages.length;n++){
      const c=await window.html2canvas(pages[n],{scale:2,backgroundColor:'#ffffff',useCORS:true,logging:false,width:816,height:1056,windowWidth:900});
      if(n) pdf.addPage(); pdf.addImage(c.toDataURL('image/jpeg',0.88),'JPEG',0,0,W,H);
      if(!n){ const p=document.createElement('canvas'); p.width=1000; p.height=Math.round(1000*c.height/c.width); p.getContext('2d').drawImage(c,0,0,p.width,p.height); apercu=await new Promise(r=>p.toBlob(r,'image/png')); }
    }
    return {pdf:pdf.output('blob'),png:apercu,pages:pages.length};
  } finally { z.remove(); }
}
async function arrDepot(lg){
  if(typeof CK_URL==='undefined'||typeof ckTok!=='function'||!ckTok()) throw new Error(arrT("Il faut ouvrir l'ERP en ligne pour envoyer la liste.","Open the online ERP to send the list.","Hay que abrir el ERP en línea para enviar la lista."));
  const items=ARR.items.filter(x=>ARR.choix.has(x.k)), sig=lg+'|'+items.map(x=>x.k).join(',');
  if(ARR.liens[lg]&&ARR.liens[lg].sig===sig) return ARR.liens[lg].url;
  if(ARR.enCours[lg]&&ARR.enCours[lg].sig===sig) return ARR.enCours[lg].p;
  const p=(async()=>{
    const r0=await arrPdf(items,lg); const F=((typeof REG!=='undefined'&&REG&&REG.fact)||{});
    const num=('ARR-'+String(ARR.f.num||ARR.f.id).replace(/[^A-Za-z0-9]/g,'').slice(0,28)+'-'+lg.toUpperCase());
    const q='?type=arrivage&enseigne='+encodeURIComponent(F.enseigne||'Perfumes Trade')+'&date='+encodeURIComponent(new Date().toLocaleDateString('en-US'))+'&lignes='+items.length+'&langue='+lg;
    const r=await fetch(CK_URL+'/api/o/'+CK_ORG+'/docs/'+encodeURIComponent(num)+q,{method:'PUT',headers:{'Content-Type':'application/pdf',Authorization:'Bearer '+ckTok()},body:r0.pdf});
    const j=await r.json().catch(()=>({})); if(!r.ok) throw new Error(j.erreur||('PDF refusé ('+r.status+')'));
    if(r0.png){ try{ await fetch(CK_URL+'/api/o/'+CK_ORG+'/docs/'+encodeURIComponent(num)+'/image',{method:'PUT',headers:{'Content-Type':'image/png',Authorization:'Bearer '+ckTok()},body:r0.png}); }catch(e){} }
    ARR.liens[lg]={sig,url:j.url,blob:r0.pdf}; return j.url; })();
  ARR.enCours[lg]={sig,p};
  try{ return await p; } finally { if(ARR.enCours[lg]&&ARR.enCours[lg].p===p) delete ARR.enCours[lg]; }
}
/* les langues des destinataires sont préparées d'avance, l'une après l'autre */
let ARR_PREP=null;
function arrPrepare(){
  clearTimeout(ARR_PREP); ARR_PREP=setTimeout(async()=>{
    if(!ARR||!ARR.choix.size) { arrPeint(); return; }
    const lgs=arrLangues();
    for(const lg of lgs){ ARR.etat[lg]='prep'; arrPeintEtat();
      try{ await arrDepot(lg); ARR.etat[lg]='ok'; }catch(e){ ARR.etat[lg]='err'; ARR.err=(e&&e.message)||'échec'; }
      arrPeintEtat(); }
  },500);
}
/* 9 nov. 2026 (Igal : « tout décocher les clients et en choisir qu'un ; soit tout sélectionner, soit un seul ») : les clients se
   cochent (aucun au départ) ; le PDF n'est préparé que dans les langues des clients cochés */
const arrCoches=()=>ARR.dest.map((d,i)=>i).filter(i=>ARR.sel.has(i)&&ARR.dest[i].tel);
const arrLangues=()=>[...new Set(arrCoches().map(i=>ARR.dest[i].lg))];
const arrEnvois=()=>{ const E=lit(K_ARR_E,{})||{}; return (E&&typeof E==='object')?E:{}; };
/* 9 nov. 2026 (Igal : « deux types d'application WhatsApp, ça porte à confusion ») : un seul chemin, WhatsApp Web — il marche sur
   tout ordinateur, sans rien installer ; la première fois, WhatsApp montre un QR code à scanner avec le téléphone. Tous les envois
   d'une tournée s'ouvrent dans le MÊME onglet. */
function arrLien(tel,txt){ return 'https://web.whatsapp.com/send?phone='+tel+'&text='+encodeURIComponent(txt); }
function arrOuvre(url){
  window.__arrDernier=url;   /* pour les tests */
  if(/^https:/.test(url)){ const w=window.open(url,'arr-whatsapp-web'); if(w) return; }
  const a=document.createElement('a'); a.href=url; a.rel='noopener'; document.body.appendChild(a); a.click(); a.remove();
}
async function arrEnvoie(i){
  const d=ARR.dest[i]; if(!d||!d.tel) return;
  const m=$('arr-msg');
  if(!ARR.choix.size){ m.textContent=arrT('Coche au moins un parfum.','Tick at least one perfume.','Marca al menos un perfume.'); m.className='msg err'; return; }
  let url=ARR.liens[d.lg]&&ARR.liens[d.lg].sig===d.lg+'|'+ARR.items.filter(x=>ARR.choix.has(x.k)).map(x=>x.k).join(',')?ARR.liens[d.lg].url:null;
  if(!url){ m.textContent=arrT('Le PDF se prépare… clique à nouveau dans un instant.','The PDF is being prepared… click again in a moment.','El PDF se está preparando… vuelve a hacer clic en un momento.'); m.className='msg';
    try{ await arrDepot(d.lg); ARR.etat[d.lg]='ok'; arrPeintEtat(); m.textContent=arrT('PDF prêt : clique à nouveau sur WhatsApp.','PDF ready: click WhatsApp again.','PDF listo: vuelve a hacer clic en WhatsApp.'); m.className='msg ok'; }
    catch(e){ m.textContent=(e&&e.message)||'échec'; m.className='msg err'; } return; }
  const txt=arrMessage(d.lg,d.prenom,url);
  arrOuvre(arrLien(d.tel,txt)); ARR.faits.add(i);
  const E=arrEnvois(), k=ARR.f.id; E[k]=Object.assign({t:'',n:0,a:{}},E[k]||{}); E[k].a[d.nom]={t:new Date().toISOString(),lg:d.lg,u:USR||''}; E[k].t=new Date().toISOString(); E[k].n=ARR.choix.size; ecrit(K_ARR_E,E);
  log({act:'vente',lib:'nouveaux arrivages envoyés à '+d.nom+' par WhatsApp ('+(ARR_LG[d.lg]||d.lg)+', '+ARR.choix.size+' parfums, réception '+(ARR.f.num||'')+')',n:ARR.choix.size,impact:0,det:[]});
  const reste=arrCoches().filter(j=>!ARR.faits.has(j)).length;
  m.textContent=arrT(`WhatsApp ouvert pour ${d.nom} : appuie sur Envoyer dans WhatsApp${reste?', puis reviens ici pour le client suivant':''}.`,`WhatsApp opened for ${d.nom}: press Send in WhatsApp${reste?', then come back here for the next customer':''}.`,`WhatsApp abierto para ${d.nom}: pulsa Enviar en WhatsApp${reste?' y luego vuelve aquí para el siguiente cliente':''}.`); m.className='msg ok';
  arrPeintDest();
}
function arrPeintEtat(){
  const z=$('arr-etat'); if(!z||!ARR) return;
  const lgs=arrLangues();
  z.innerHTML=lgs.map(lg=>{ const s=ARR.etat[lg]; return `<span class="arr-pill ${s==='ok'?'ok':s==='err'?'err':''}">PDF ${lg.toUpperCase()} · ${s==='ok'?arrT('prêt','ready','listo'):s==='err'?arrT('échec','failed','error'):arrT('en préparation…','being prepared…','preparándose…')}</span>`; }).join('')
    +(Object.values(ARR.etat).includes('err')?`<span class="arr-pill err">${esc(ARR.err||'')}</span>`:'');
}
function arrPeintDest(){
  const z=$('arr-dest'); if(!z||!ARR) return; const E=(arrEnvois()[ARR.f.id]||{}).a||{};
  const avec=ARR.dest.filter(d=>d.tel), sans=ARR.dest.filter(d=>!d.tel);
  const C=arrCoches(), reste=C.filter(i=>!ARR.faits.has(i)), prochain=reste.length?ARR.dest[reste[0]]:null, fait=C.length-reste.length;
  const lib=!C.length?arrT('Coche au moins un client','Tick at least one customer','Marca al menos un cliente')
    :!prochain?arrT(`C'est fait : ${C.length} envoyé${C.length>1?'s':''} ✓`,`Done: ${C.length} sent ✓`,`Hecho: ${C.length} enviado${C.length>1?'s':''} ✓`)
    :fait?arrT(`Client suivant : ${prochain.nom} (${fait+1}/${C.length})`,`Next customer: ${prochain.nom} (${fait+1}/${C.length})`,`Siguiente cliente: ${prochain.nom} (${fait+1}/${C.length})`)
    :arrT(`Envoyer par WhatsApp (${C.length} client${C.length>1?'s':''})`,`Send by WhatsApp (${C.length} customer${C.length>1?'s':''})`,`Enviar por WhatsApp (${C.length} cliente${C.length>1?'s':''})`);
  z.innerHTML=(avec.length?`<div class="arr-sel"><button class="btn" id="arr-ctous">${arrT('Tout cocher','Tick all','Marcar todo')}</button><button class="btn" id="arr-caucun">${arrT('Tout décocher','Untick all','Desmarcar todo')}</button><span class="hint">${nf(C.length)} / ${nf(avec.length)} ${arrT('coché(s)','ticked','marcado(s)')}</span></div>`
      +avec.map(d=>{ const i=ARR.dest.indexOf(d), s=E[d.nom], on=ARR.sel.has(i);
      return `<label class="arr-d${on?' on':''}${s?' fait':''}"><input type="checkbox" data-arrsel="${i}"${on?' checked':''}><span class="arr-dn"><b data-nolang>${esc(d.nom)}</b><small data-nolang>+${esc(d.tel)}</small></span>`
        +`<select data-arrlg="${i}">${Object.keys(ARR_LG).map(l=>`<option value="${l}"${l===d.lg?' selected':''}>${ARR_LG[l]}</option>`).join('')}</select>`
        +`<span class="arr-st">${ARR.faits.has(i)?arrT('ouvert dans WhatsApp','opened in WhatsApp','abierto en WhatsApp')+' ✓':s?arrT('déjà envoyé','already sent','ya enviado')+' ✓':''}</span></label>`; }).join('')
      +`<div class="arr-go"><button class="btn arr-wa" id="arr-envoi"${prochain?'':' disabled'}>${esc(lib)}</button></div>`
      :`<p class="hint">${arrT("Aucun client favori n'a de numéro de téléphone. Mets l'étoile à tes meilleurs clients dans Clients, avec leur numéro.","No favourite customer has a phone number. Star your best customers in Customers, with their number.","Ningún cliente favorito tiene número de teléfono. Marca con la estrella a tus mejores clientes en Clientes, con su número.")}</p>`)
    +(sans.length?`<p class="hint">${arrT('Favoris sans numéro (à compléter dans Clients) :','Favourites without a number (complete them in Customers):','Favoritos sin número (complétalos en Clientes):')} <span data-nolang>${sans.map(d=>esc(d.nom)).join(', ')}</span></p>`:'');
  const change=()=>{ arrPeintDest(); arrPeintEtat(); arrPrepare(); };
  z.querySelectorAll('[data-arrsel]').forEach(b=>b.onchange=()=>{ const i=+b.dataset.arrsel; b.checked?ARR.sel.add(i):ARR.sel.delete(i); change(); });
  const t=$('arr-ctous'); if(t) t.onclick=()=>{ ARR.dest.forEach((d,i)=>{ if(d.tel) ARR.sel.add(i); }); change(); };
  const a=$('arr-caucun'); if(a) a.onclick=()=>{ ARR.sel.clear(); ARR.faits.clear(); change(); };
  const g=$('arr-envoi'); if(g) g.onclick=()=>{ const r=arrCoches().filter(i=>!ARR.faits.has(i)); if(r.length) arrEnvoie(r[0]); };
  z.querySelectorAll('[data-arrlg]').forEach(s=>{ s.onclick=e=>e.preventDefault&&e.stopPropagation(); s.onchange=()=>{ const d=ARR.dest[+s.dataset.arrlg]; d.lg=s.value;
    const C=lit('clients-v1',{})||{}; if(C[d.nom]){ C[d.nom]=Object.assign({},C[d.nom],{langue:d.lg,maj:new Date().toISOString()}); ecrit('clients-v1',C); }   /* la langue du client est retenue */
    arrPeintEtat(); arrPrepare(); }; });
}
function arrPeint(){
  if(!ARR) return; const c=$('arr-corps');
  const autres=ARR.memeJour.map(f=>`<label class="arr-autre"><input type="checkbox" data-arrf="${esc(f.id)}"${ARR.factures.includes(f)?' checked':''}> ${arrT('ajouter aussi','also add','añadir también')} <span data-nolang>${esc(f.num||'')} · ${esc(f.tiers||'')}</span> (${nf((f.lignes||[]).filter(l=>l&&+l.q>0).length)})</label>`).join('');
  c.innerHTML=`<p class="arr-sous" data-nolang>${esc(ARR.f.num||'')} · ${esc(ARR.f.tiers||'')} · ${esc(arrJour(ARR.f.d))}</p>${autres}
    <div class="arr-tete"><b>${arrT('Parfums de la liste','Perfumes on the list','Perfumes de la lista')} (${nf(ARR.choix.size)}/${nf(ARR.items.length)})</b>
      <span><button class="btn" id="arr-tous">${arrT('Tout cocher','Tick all','Marcar todo')}</button> <button class="btn" id="arr-voir">${arrT('Voir le PDF','See the PDF','Ver el PDF')}</button></span></div>
    <div class="arr-grille">${ARR.items.map(x=>`<label class="arr-p${ARR.choix.has(x.k)?' on':''}"><input type="checkbox" data-arrp="${esc(x.k)}"${ARR.choix.has(x.k)?' checked':''}><span class="arr-ph">${x.photo?`<img src="${x.photo}">`:(x.photo===null?`<em>${arrT('sans photo','no photo','sin foto')}</em>`:'')}</span><span class="arr-pn" data-nolang><small>${esc(x.marque||'')}</small>${esc(x.nom||'')}</span></label>`).join('')}</div>
    <div class="arr-tete"><b>${arrT('Clients favoris','Favourite customers','Clientes favoritos')}</b>
</div>
    <div id="arr-etat" class="arr-etat"></div><div id="arr-dest"></div>
    <p class="hint">${arrT("Coche les clients, puis « Envoyer par WhatsApp » : WhatsApp s'ouvre dans un onglet, pour le premier, avec le message dans sa langue et le lien du PDF. Appuie sur Envoyer dans WhatsApp, puis reviens ici pour le suivant. La première fois, WhatsApp demande de scanner un QR code avec le téléphone. Le message se change dans Réglages › Ma société.","Tick the customers, then “Send by WhatsApp”: WhatsApp opens in a tab, for the first one, with the message in their language and the PDF link. Press Send in WhatsApp, then come back here for the next one. The first time, WhatsApp asks you to scan a QR code with your phone. The message can be changed in Settings › My company.","Marca los clientes y luego « Enviar por WhatsApp »: WhatsApp se abre en una pestaña, para el primero, con el mensaje en su idioma y el enlace del PDF. Pulsa Enviar en WhatsApp y vuelve aquí para el siguiente. La primera vez, WhatsApp pide escanear un código QR con el teléfono. El mensaje se cambia en Ajustes › Mi empresa.")}</p>`;
  c.querySelectorAll('[data-arrp]').forEach(b=>b.onchange=()=>{ b.checked?ARR.choix.add(b.dataset.arrp):ARR.choix.delete(b.dataset.arrp); b.closest('.arr-p').classList.toggle('on',b.checked);
    c.querySelector('.arr-tete b').textContent=`${arrT('Parfums de la liste','Perfumes on the list','Perfumes de la lista')} (${nf(ARR.choix.size)}/${nf(ARR.items.length)})`; ARR.etat={}; arrPeintEtat(); arrPrepare(); });
  c.querySelectorAll('[data-arrf]').forEach(b=>b.onchange=()=>{ const f=ARR.memeJour.find(x=>x.id===b.dataset.arrf); if(!f) return;
    ARR.factures=b.checked?ARR.factures.concat([f]):ARR.factures.filter(x=>x!==f); arrCharge(); });
  $('arr-tous').onclick=()=>{ ARR.items.forEach(x=>ARR.choix.add(x.k)); ARR.etat={}; arrPeint(); arrPrepare(); };
  $('arr-voir').onclick=async()=>{ const lg=(arrLangues()[0])||(typeof LANG!=='undefined'&&ARR_T[LANG]?LANG:'en'); const w=window.open('','_blank');
    try{ const items=ARR.items.filter(x=>ARR.choix.has(x.k)); const r=ARR.liens[lg]&&ARR.liens[lg].blob?{pdf:ARR.liens[lg].blob}:await arrPdf(items,lg);
      const u=URL.createObjectURL(r.pdf); if(w&&!w.closed) w.location.href=u; else window.open(u,'_blank'); }
    catch(e){ try{ if(w) w.close(); }catch(_){} $('arr-msg').textContent=(e&&e.message)||'échec'; $('arr-msg').className='msg err'; } };
  arrPeintEtat(); arrPeintDest();
}
async function arrCharge(){
  const vus=new Set(ARR.items.map(x=>x.k)), anc=new Set(ARR.choix);
  const arts=arrLignes(ARR.factures);
  ARR.items=arts.map(a=>({k:a.cle||a.id,a,marque:a.marque,nom:a.nom,ml:a.ml,type:a.type,genre:a.genre,bc:a.bc,photo:ARR_PH[a.cle||a.id]}));
  ARR.choix=new Set(ARR.items.filter(x=>!vus.has(x.k)||anc.has(x.k)).map(x=>x.k));
  ARR.etat={}; arrPeint();
  for(const x of ARR.items){ if(x.photo===undefined){ x.photo=await arrPhoto(x.a);
    const s=document.querySelector(`[data-arrp="${CSS.escape(x.k)}"]`); const ph=s&&s.parentNode.querySelector('.arr-ph');
    if(ph) ph.innerHTML=x.photo?`<img src="${x.photo}">`:`<em>${arrT('sans photo','no photo','sin foto')}</em>`; } }
  arrPrepare();
}
function arrivageFenetreOuvre(fid){
  const R=arrReceptions(fid); const ov=$('arrov');
  $('arr-t').textContent=arrT('Envoyer les nouveaux arrivages','Send the new arrivals','Enviar los nuevos arribos');
  $('arr-ferme').textContent=arrT('Fermer','Close','Cerrar');
  $('arr-msg').textContent=''; $('arr-msg').className='msg';
  if(!R){ $('arr-corps').innerHTML=`<p class="hint">${arrT('Réception introuvable.','Receipt not found.','Recepción no encontrada.')}</p>`; ov.classList.add('on'); return; }
  ARR={f:R.f,memeJour:R.memeJour,factures:[R.f],items:[],choix:new Set(),dest:arrFavoris(),sel:new Set(),faits:new Set(),liens:{},enCours:{},etat:{}};
  ov.classList.add('on'); arrCharge();
}
function arrFerme(){ $('arrov').classList.remove('on'); ARR=null;
  if(document.documentElement.classList.contains('cadre')){ try{ window.parent.postMessage({fiche:'fermee'},location.origin); }catch(e){} } }
$('arr-x').onclick=arrFerme; $('arr-ferme').onclick=arrFerme;
window.__ARR={get(){ return ARR; }, ouvre:arrivageFenetreOuvre, favoris:arrFavoris, pdf:arrPdf, feuilles:arrFeuilles};'''
def ecrit(dossier):
    d = pathlib.Path(dossier) / 'lib'; d.mkdir(exist_ok=True)
    corps = ("(function(){ const st=document.createElement('style'); st.id='arr-css'; st.textContent="
             + json.dumps(CSS) + "; document.head.appendChild(st); })();\n" + JS.replace('__MSG_DEF__', json.dumps(MSG_DEF, ensure_ascii=False)) + "\n")
    (d / 'arrivage.js').write_text(corps, encoding='utf-8')
