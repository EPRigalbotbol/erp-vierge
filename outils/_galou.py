# -*- coding: utf-8 -*-
"""Galou : l'assistant d'Igal dans l'ERP (3 nov. 2026).

Igal : « j'aimerais créer un agent IA qu'on va appeler Galou, tout le temps connecté sur l'ERP ; si Sam a
besoin de quelque chose il s'adresse à lui… le matin, Sam lui dit « Salut Galou, tu me fais un récap de la
journée d'hier ? » ». Une sorte de Jarvis, avec l'avatar et la voix d'Igal.

Ce fichier : la fenêtre « Parler à Galou », ouverte depuis le menu sur n'importe quelle page. Sam écrit ou
parle (micro du navigateur), Galou répond en texte et à voix haute. La réponse vient du cockpit
(/galou/parle, voir cockpit/galou.js) : les chiffres y sont calculés par l'ERP, l'IA ne fait que les dire.

3 nov. 2026 : l'agent s'appelle Léa (Igal, après « Galou » puis « Sabrina » ; voix de femme, clonée chez ElevenLabs) ; les identifiants techniques
(galou-*, /galou/…) gardent l'ancien nom. Igal : « une fenêtre qui s'ouvre au milieu, un peu futuriste, moins cheap
que la bannière en bas à droite, avec des mouvements de vibration quand la personne parle » : la fenêtre est
centrée, sombre, et une sphère lumineuse (canvas) y respire au repos, s'agite au niveau sonore réel de la voix de
Léa (analyseur Web Audio sur le mp3), bat au rythme du micro quand Sam parle, et tourne quand elle réfléchit.
"""

JS = r"""
/* ---------- Parler à Galou ---------- */
const GL_K='galou-conv-v1';          /* la conversation du moment, sur ce poste (sessionStorage : elle s'efface en fermant l'onglet) */
let GL_CONV=[], GL_ENV=false, GL_VOIX=true, GL_REC=null, GL_PRET=null;
try{ const c=JSON.parse(sessionStorage.getItem(GL_K)||'[]'); if(Array.isArray(c)) GL_CONV=c.slice(-20); }catch(e){}
try{ GL_VOIX=localStorage.getItem('galou-voix-v1')!=='0'; }catch(e){}
const glLang=()=>{ const l=(typeof LANG!=='undefined'&&LANG)||'fr'; return l==='en'?'en-US':l==='es'?'es-ES':'fr-FR'; };
const glT=(fr,en,es)=>typeof L3==='function'?L3(fr,en,es):fr;
function glPeut(){ try{ return location.protocol!=='file:' && !!ckTok(); }catch(e){ return false; } }
function glStyle(){
  if(document.getElementById('gl-css')) return;
  const s=document.createElement('style'); s.id='gl-css'; s.textContent=`
.gl-ov{position:fixed;inset:0;background:rgba(4,6,18,.72);backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);z-index:9000;display:flex;align-items:center;justify-content:center;padding:18px;animation:gl-in .25s ease-out}
@keyframes gl-in{from{opacity:0}to{opacity:1}}
.gl-m{position:relative;width:min(620px,100%);height:min(800px,calc(100vh - 36px));color:#e9ecff;background:radial-gradient(120% 80% at 50% -10%,rgba(110,120,255,.22),transparent 60%),linear-gradient(165deg,#111633 0%,#0a0d1f 55%,#070914 100%);border:1px solid rgba(140,150,255,.28);border-radius:26px;box-shadow:0 40px 120px rgba(0,0,0,.65),0 0 90px rgba(90,110,255,.16),inset 0 1px 0 rgba(255,255,255,.08);display:flex;flex-direction:column;overflow:hidden;animation:gl-pop .32s cubic-bezier(.2,.9,.3,1.2)}
@keyframes gl-pop{from{transform:scale(.92) translateY(14px);opacity:0}to{transform:none;opacity:1}}
.gl-m::before{content:"";position:absolute;inset:0;pointer-events:none;background:repeating-linear-gradient(0deg,rgba(255,255,255,.018) 0 1px,transparent 1px 4px);opacity:.6}
.gl-h{position:relative;display:flex;flex-direction:column;align-items:center;padding:18px 16px 4px;flex:none}
.gl-orbe{position:relative;width:200px;height:200px}
.gl-orbe canvas{position:absolute;inset:0;width:100%;height:100%}
.gl-av{position:absolute;left:50%;top:50%;width:92px;height:92px;margin:-46px 0 0 -46px;border-radius:50%;overflow:hidden;display:none;box-shadow:0 0 0 2px rgba(255,255,255,.35);transition:transform .08s}
.gl-av img{width:100%;height:100%;object-fit:cover;display:block}
.gl-h h2{margin:4px 0 0;font-size:22px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:#fff;text-shadow:0 0 18px rgba(140,150,255,.8)}
.gl-h small{display:block;font-size:12px;color:#9aa3d6;letter-spacing:.06em;min-height:16px}
.gl-h .x{position:absolute;right:10px;top:8px;background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.12);color:#c5cbf2;font-size:20px;line-height:1;width:34px;height:34px;border-radius:50%;cursor:pointer}
.gl-h .x:hover{background:rgba(255,255,255,.14)}
.gl-b{flex:1;overflow-y:auto;padding:10px 18px;display:flex;flex-direction:column;gap:10px;scroll-behavior:smooth}
.gl-b::-webkit-scrollbar{width:6px}.gl-b::-webkit-scrollbar-thumb{background:rgba(255,255,255,.15);border-radius:3px}
.gl-msg{max-width:86%;padding:10px 14px;border-radius:16px;font-size:14px;line-height:1.5;white-space:pre-wrap;word-break:break-word;animation:gl-in .2s}
.gl-msg.u{align-self:flex-end;background:linear-gradient(135deg,#6d7cff,#8b5cf6);color:#fff;border-bottom-right-radius:5px;box-shadow:0 6px 20px rgba(110,120,255,.25)}
.gl-msg.g{align-self:flex-start;background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.08);color:#e9ecff;border-bottom-left-radius:5px}
.gl-msg.att{color:#9aa3d6;font-style:italic}
.gl-raccs{display:flex;flex-wrap:wrap;gap:6px;padding:4px 18px 8px;justify-content:center}
.gl-raccs button{font-family:inherit;font-size:12.5px;font-weight:600;color:#c9cfff;background:rgba(120,130,255,.1);border:1px solid rgba(140,150,255,.35);border-radius:999px;padding:6px 13px;cursor:pointer;transition:all .15s}
.gl-raccs button:hover{background:rgba(120,130,255,.25);box-shadow:0 0 16px rgba(120,130,255,.35)}
.gl-f{display:flex;justify-content:center;padding:6px 14px 4px}
.gl-ecoute{color:#1fd3c0;font-style:italic;min-height:16px}
#gl-etat.err{color:#ff8a8a}
.gl-f textarea{flex:1;font-family:inherit;font-size:14px;min-height:44px;max-height:120px;resize:none;padding:11px 14px;border:1px solid rgba(140,150,255,.3);border-radius:14px;background:rgba(255,255,255,.06);color:#fff;outline:none}
.gl-f textarea:focus{border-color:rgba(160,170,255,.8);box-shadow:0 0 0 3px rgba(120,130,255,.18)}
.gl-f textarea::placeholder{color:#7f88bf}
.gl-f button{font-family:inherit;font-size:13px;font-weight:600;border:1px solid rgba(140,150,255,.3);background:rgba(255,255,255,.06);color:#dfe3ff;border-radius:14px;padding:0 14px;cursor:pointer;height:44px;white-space:nowrap;transition:all .15s}
.gl-f button:hover{background:rgba(255,255,255,.12)}
.gl-f button.pri{background:linear-gradient(135deg,#6d7cff,#8b5cf6);border-color:transparent;color:#fff;box-shadow:0 6px 20px rgba(110,120,255,.35)}
.gl-f button.mic{display:flex;align-items:center;gap:12px;height:62px;padding:0 26px 0 18px;border-radius:999px;font-size:15px;font-weight:700;background:linear-gradient(135deg,#6d7cff,#8b5cf6);border-color:transparent;color:#fff;box-shadow:0 10px 30px rgba(110,120,255,.4)}
.gl-f button.mic .ic{font-size:26px}
.gl-f button.mic:hover{transform:translateY(-1px);box-shadow:0 14px 34px rgba(110,120,255,.5)}
.gl-f button.mic.on{background:#1fd3c0;border-color:#1fd3c0;color:#06202a;box-shadow:0 0 0 0 rgba(31,211,192,.7);animation:gl-mic 1.1s infinite}
@keyframes gl-mic{0%{box-shadow:0 0 0 0 rgba(31,211,192,.6)}100%{box-shadow:0 0 0 18px rgba(31,211,192,0)}}
.gl-opts{display:flex;gap:14px;padding:0 18px 6px;font-size:12px;color:#8e97cc;align-items:center;justify-content:center}
.gl-opts label{display:flex;align-items:center;gap:5px;cursor:pointer}
.gl-opts .lnk{color:#aab2e8;background:none;border:0;cursor:pointer;font-family:inherit;text-decoration:underline}
@media(max-width:600px){.gl-ov{padding:0}.gl-m{height:100vh;border-radius:0}.gl-orbe{width:150px;height:150px}}`;
  document.head.appendChild(s);
}
function glSauve(){ try{ sessionStorage.setItem(GL_K,JSON.stringify(GL_CONV.slice(-20))); }catch(e){} }
function glAjoute(role,texte,cls){
  const b=document.getElementById('gl-b'); if(!b) return null;
  const d=document.createElement('div'); d.className='gl-msg '+(role==='user'?'u':'g')+(cls?' '+cls:''); d.textContent=texte; d.setAttribute('data-nolang','');
  b.appendChild(d); b.scrollTop=b.scrollHeight; return d;
}
/* ---------- la sphère de Léa : elle respire au repos, vibre au son de sa voix, bat au micro, tourne quand elle réfléchit ----------
   GL_MODE : 'repos' | 'ecoute' (micro ouvert) | 'pense' (réponse en cours) | 'parle' (voix en cours).
   Le niveau sonore (0..1) vient d'un analyseur Web Audio : sur le mp3 de la voix clonée, et sur le micro quand Sam parle.
   Quand il n'y a pas d'analyseur (voix du navigateur, micro refusé), un battement synthétique fait vivre la sphère quand même. */
let GL_MODE='repos', GL_AC=null, GL_ANA=null, GL_MICFLUX=null, GL_ANIM=0;
function glMode(m){ GL_MODE=m; const st=document.getElementById('gl-etat'); if(st) st.textContent=m==='ecoute'?glT('je t\'écoute…','I\'m listening…','te escucho…'):m==='pense'?glT('je réfléchis…','thinking…','estoy pensando…'):m==='parle'?glT('je te parle','speaking','te hablo'):glT('prête','ready','lista'); }
function glAudioCtx(){ try{ if(!GL_AC){ const C=window.AudioContext||window.webkitAudioContext; if(!C) return null; GL_AC=new C(); } if(GL_AC.state==='suspended') GL_AC.resume(); return GL_AC; }catch(e){ return null; } }
function glBranche(src){ const ac=glAudioCtx(); if(!ac) return null; const an=ac.createAnalyser(); an.fftSize=512; an.smoothingTimeConstant=.55; src.connect(an); GL_ANA=an; return an; }
function glNiveau(t){
  if(GL_ANA&&(GL_MODE==='parle'||GL_MODE==='ecoute')){ try{ const d=new Uint8Array(GL_ANA.fftSize); GL_ANA.getByteTimeDomainData(d); let s=0; for(let i=0;i<d.length;i++){ const v=(d[i]-128)/128; s+=v*v; } return Math.min(1,Math.sqrt(s/d.length)*4.5); }catch(e){} }
  if(GL_MODE==='parle') return .25+.35*Math.abs(Math.sin(t*7.3))*(.6+.4*Math.abs(Math.sin(t*1.9)));
  if(GL_MODE==='ecoute') return .12+.12*Math.abs(Math.sin(t*2.6));
  return 0;
}
function glOrbe(){
  const c=document.getElementById('gl-orb'); if(!c) return; const g=c.getContext('2d'); const W=c.width,H=c.height,cx=W/2,cy=H/2,R0=W*.25; let t=0, nivL=0;
  const av=document.getElementById('gl-av'); const photo=av&&av.style.display==='block';
  cancelAnimationFrame(GL_ANIM);
  function cadre(){
    if(!document.getElementById('gl-orb')){ GL_ANIM=0; return; }
    t+=1/60; const brut=glNiveau(t); nivL+=(brut-nivL)*(brut>nivL?.5:.12); const niv=nivL;
    const col=GL_MODE==='ecoute'?'31,211,192':GL_MODE==='parle'?'255,96,180':GL_MODE==='pense'?'255,186,84':'122,132,255';
    const resp=GL_MODE==='repos'?Math.sin(t*1.3)*2.5:0;
    g.clearRect(0,0,W,H);
    for(let k=3;k>=1;k--){
      const amp=(GL_MODE==='repos'?2.5:5)+niv*22*k/3;
      g.beginPath();
      for(let i=0;i<=96;i++){ const a=i/96*Math.PI*2; const w=Math.sin(a*(3+k)+t*(1.4+k*.8))*amp+Math.sin(a*(8-k)-t*2.6)*amp*.45;
        const r=R0*(1+k*.2)+w+niv*20*k/3+resp; const x=cx+Math.cos(a)*r,y=cy+Math.sin(a)*r; i?g.lineTo(x,y):g.moveTo(x,y); }
      g.closePath(); g.fillStyle='rgba('+col+','+(.07+(3-k)*.07+niv*.08)+')'; g.fill();
    }
    const r0=R0*(1+niv*.14)+resp;
    g.save(); g.shadowColor='rgba('+col+',.95)'; g.shadowBlur=26+niv*46;
    if(photo){ g.beginPath(); g.arc(cx,cy,r0*1.02,0,Math.PI*2); g.fillStyle='rgba('+col+',.55)'; g.fill(); }
    else { const gr=g.createRadialGradient(cx-R0*.32,cy-R0*.32,R0*.08,cx,cy,r0); gr.addColorStop(0,'rgba(255,255,255,.95)'); gr.addColorStop(.38,'rgba('+col+',.95)'); gr.addColorStop(1,'rgba('+col+',.3)');
      g.beginPath(); g.arc(cx,cy,r0,0,Math.PI*2); g.fillStyle=gr; g.fill(); }
    g.restore();
    if(GL_MODE==='pense'){ g.beginPath(); g.arc(cx,cy,R0*1.42,t*3.2,t*3.2+Math.PI*1.25); g.strokeStyle='rgba('+col+',.9)'; g.lineWidth=3; g.lineCap='round'; g.stroke();
      g.beginPath(); g.arc(cx,cy,R0*1.62,-t*2.1,-t*2.1+Math.PI*.6); g.strokeStyle='rgba('+col+',.45)'; g.lineWidth=2; g.stroke(); }
    if(photo&&av) av.style.transform='scale('+(1+niv*.12)+')';
    GL_ANIM=requestAnimationFrame(cadre);
  }
  GL_ANIM=requestAnimationFrame(cadre);
}
/* LA VOIX DE LÉA (clonée, produite par le cockpit). 3 nov. 2026, Igal : « elle met au moins 10 secondes avant de répondre »
   et « la voix était robotisée » (= la voix de secours du navigateur avait pris le relais sans le dire). Donc :
   - la réponse est découpée en morceaux (une ou deux phrases) : le premier morceau part chez ElevenLabs tout de suite, le
     suivant est demandé pendant que le premier se joue → Léa commence à parler en une à deux secondes, pas après tout ;
   - dès que la question part, Léa dit un mot d'accueil (« Je regarde. »), fabriqué une fois et gardé sur ce poste ;
   - si ElevenLabs rate, on réessaie une fois ; si ça rate encore, la voix du navigateur prend le relais MAIS la raison
     s'affiche sous la sphère et reste dans localStorage (galou-voix-raison) pour qu'Igal sache pourquoi. */
let GL_AUDIO=null, GL_VOIX_IGAL=null;   /* GL_VOIX_IGAL : null = on ne sait pas encore, true/false = réponse du cockpit (etat.voix) */
let GL_FILE=[], GL_LECTURE=false, GL_SERIE=0, GL_FIN=null;   /* la file des morceaux à dire, dans l'ordre ; GL_FIN : à appeler quand tout est dit */
function glMorceaux(texte){
  const ph=String(texte||'').replace(/\s+/g,' ').trim().match(/[^.!?…]+[.!?…]+["»”)]?\s*|[^.!?…]+$/g)||[texte];
  const M=[]; let cur='';
  ph.forEach(x=>{ x=x.trim(); if(!x) return; if(cur&&(cur.length+x.length>220||cur.length>120)){ M.push(cur); cur=x; } else cur=cur?cur+' '+x:x; });
  if(cur) M.push(cur); return M;
}
async function glMp3(texte){
  const r=await fetch(CK_URL+'/api/o/'+CK_ORG+'/galou/voix',{method:'POST',headers:{'Content-Type':'application/json',Authorization:'Bearer '+ckTok()},body:JSON.stringify({texte})});
  if(!r.ok){ let m='voix '+r.status; try{ const j=await r.json(); if(j&&j.erreur) m=j.erreur; }catch(e){} throw new Error(m); }
  return r.blob();
}
function glRaison(m){ const st=document.getElementById('gl-etat'); if(st){ st.textContent=glT('voix de Léa indisponible : ','Léa\'s voice unavailable: ','voz de Léa no disponible: ')+m; st.classList.add('err'); setTimeout(()=>{ st.classList.remove('err'); glMode(GL_MODE); },9000); } try{ localStorage.setItem('galou-voix-raison',new Date().toISOString()+' '+m); }catch(e){} }
function glJoue(blob){ return new Promise((ok)=>{ const u=URL.createObjectURL(blob); const a=new Audio(u); GL_AUDIO=a;
  /* la sphère suit le vrai niveau sonore de la voix : l'audio passe par un analyseur Web Audio avant les haut-parleurs */
  try{ const ac=glAudioCtx(); if(ac){ const src=ac.createMediaElementSource(a); const an=glBranche(src); if(an) an.connect(ac.destination); } }catch(e){}
  a.onplay=()=>glMode('parle'); let fait=false; const fin=()=>{ if(fait) return; fait=true; URL.revokeObjectURL(u); if(GL_AUDIO===a) GL_AUDIO=null; ok(true); }; a.onended=fin; a.onerror=fin; a._fin=fin;
  a.play().catch(e=>{ glRaison(String(e&&e.message||e).slice(0,80)); fin(); }); }); }
async function glLecture(serie){
  /* une lecture par série : quand une nouvelle réponse (ou le micro) coupe, la série change et cette boucle s'arrête d'elle-même */
  GL_LECTURE=true;
  while(GL_FILE.length&&serie===GL_SERIE){ const m=GL_FILE.shift(); let b=null;
    if(!m.p&&m.d) m.p=m.d(m.t);   /* pas encore demandé (la lecture va plus vite que la file) : on le demande maintenant */
    try{ b=await m.p; }catch(e){ b=null; }
    if(serie!==GL_SERIE) return;
    if(b) await glJoue(b); else { await new Promise(ok=>glDitNavigateur(m.t,ok)); }
  }
  if(serie===GL_SERIE){ GL_LECTURE=false; glMode('repos'); const f=GL_FIN; GL_FIN=null; if(f) f(); }
}
function glDit(texte,apres){
  glCoupe(); GL_FIN=apres||null; if(!GL_VOIX){ glMode('repos'); const f=GL_FIN; GL_FIN=null; if(f) f(); return; }
  const serie=GL_SERIE;
  if(GL_VOIX_IGAL&&glPeut()){
    const M=glMorceaux(texte);
    /* deux morceaux demandés d'avance au plus : le premier part maintenant, le deuxième pendant que le premier se joue */
    const demande=(t)=>glMp3(t).catch(()=>glMp3(t)).catch(e=>{ glRaison(String(e&&e.message||e).slice(0,90)); return null; });
    M.forEach((t,i)=>{ const o={t,p:null,d:demande}; o.p=i<2?demande(t):null; GL_FILE.push(o); });
    /* les suivants sont demandés au fur et à mesure (toujours un d'avance) */
    const suivant=()=>{ const o=GL_FILE.find(x=>!x.p); if(o){ o.p=demande(o.t); o.p.finally(()=>{ if(serie===GL_SERIE) suivant(); }); } };
    setTimeout(suivant,300);
    glLecture(serie); return;
  }
  GL_FILE.push({t:texte,p:Promise.resolve(null)}); glLecture(serie);
}
/* tout arrêter : la voix en cours, les morceaux en attente */
function glCoupe(){ GL_SERIE++; GL_FILE=[]; GL_FIN=null; GL_LECTURE=false; try{ speechSynthesis&&speechSynthesis.cancel(); }catch(e){} try{ if(GL_AUDIO){ const a=GL_AUDIO; GL_AUDIO=null; a.pause(); if(a._fin) a._fin(); } }catch(e){} }
/* le mot d'accueil, dit tout de suite quand la question part (fabriqué une fois par langue, gardé sur ce poste) */
async function glAccuse(){
  if(!GL_VOIX||!GL_VOIX_IGAL||!glPeut()) return;
  const lg=glLang().slice(0,2), txt=lg==='en'?'Let me check.':lg==='es'?'Déjame ver.':'Je regarde.'; const k='galou-accuse-v1:'+lg;
  try{ let b64=null; try{ b64=localStorage.getItem(k); }catch(e){}
    let blob; if(b64){ const bin=atob(b64); const u8=new Uint8Array(bin.length); for(let i=0;i<bin.length;i++) u8[i]=bin.charCodeAt(i); blob=new Blob([u8],{type:'audio/mpeg'}); }
    else { blob=await glMp3(txt); const buf=new Uint8Array(await blob.arrayBuffer()); let str=''; for(let i=0;i<buf.length;i++) str+=String.fromCharCode(buf[i]); try{ localStorage.setItem(k,btoa(str)); }catch(e){} }
    if(GL_MODE==='pense'&&!GL_AUDIO&&!GL_LECTURE){ await glJoue(blob); if(GL_ENV) glMode('pense'); }
  }catch(e){}
}
/* à l'oral, les marques écrites à l'ancienne se prononcent normalement (le cockpit fait pareil pour la voix de Léa) */
const GL_PRONONCE=[[/\bBvlgari\b/gi,'Bulgari'],[/\bAqva\b/gi,'Aqua']];
function glPrononcable(t){ t=String(t||''); GL_PRONONCE.forEach(([re,par])=>{ t=t.replace(re,par); }); return t; }
function glDitNavigateur(texte,apres){
  if(!('speechSynthesis' in window)){ if(apres) apres(); return; }
  try{ speechSynthesis.cancel(); const u=new SpeechSynthesisUtterance(glPrononcable(texte)); u.lang=glLang(); u.rate=1.02;
    /* à défaut de la voix clonée : une voix de femme du navigateur, dans la langue de la page */
    const V=speechSynthesis.getVoices().filter(v=>v.lang&&v.lang.toLowerCase().startsWith(glLang().slice(0,2)));
    const pref=V.find(v=>/amelie|audrey|marie|aurelie|monica|paulina|samantha|victoria|female|femme/i.test(v.name))||V.find(v=>!/thomas|nicolas|daniel|paul|jorge|diego|male|homme/i.test(v.name))||V[0];
    if(pref) u.voice=pref; GL_ANA=null; u.onstart=()=>glMode('parle'); u.onend=u.onerror=()=>{ if(apres) apres(); }; speechSynthesis.speak(u); }catch(e){ if(apres) apres(); }
}
let GL_PAR_MICRO=false;   /* la dernière question est venue du micro : après la réponse, Léa réécoute toute seule */
async function glEnvoie(texte,parMicro){
  texte=String(texte||'').trim(); if(!texte||GL_ENV) return;
  GL_PAR_MICRO=!!parMicro; glCoupe();
  GL_CONV.push({role:'user',content:texte}); glSauve(); glAjoute('user',texte);
  GL_ENV=true; glMode('pense'); glAccuse(); const att=glAjoute('assistant',glT('Léa réfléchit…','Léa is thinking…','Léa está pensando…'),'att');
  try{
    const r=await fetch(CK_URL+'/api/o/'+CK_ORG+'/galou/parle',{method:'POST',headers:{'Content-Type':'application/json',Authorization:'Bearer '+ckTok()},body:JSON.stringify({messages:GL_CONV.slice(-12),page:(document.querySelector('.main h1')||{}).textContent||''})});
    const j=await r.json().catch(()=>({}));
    if(!r.ok) throw new Error(j.erreur||('serveur '+r.status));
    /* au cas où le modèle met quand même du gras ou des puces : on les enlève, la réponse est lue à voix haute */
    const rep=String(j.texte||'').replace(/\*\*|__|^#+\s*/gm,'').replace(/^\s*[-•]\s+/gm,'').trim()||glT('(pas de réponse)','(no answer)','(sin respuesta)');
    GL_CONV.push({role:'assistant',content:rep}); glSauve();
    if(att){ att.textContent=rep; att.classList.remove('att'); }
    /* conversation continue : si Sam a parlé au micro, Léa réécoute dès qu'elle a fini (il n'a rien à appuyer) */
    GL_ENV=false; glDit(rep, ()=>{ if(GL_PAR_MICRO&&GL_SUITE&&document.getElementById('gl-ov')&&!GL_REC) glMicro(true); });
  }catch(e){
    const m=glT('Léa ne répond pas : ','Léa is not answering: ','Léa no responde: ')+(e&&e.message||e);
    if(att){ att.textContent=m; att.classList.remove('att'); }
    glCoupe(); glMode('repos'); GL_CONV.pop(); glSauve();
  }
  GL_ENV=false; const b=document.getElementById('gl-b'); if(b) b.scrollTop=b.scrollHeight;
}
/* le micro : la reconnaissance vocale du navigateur (Chrome) ; la phrase part toute seule quand elle est finie */
let GL_SUITE=true; try{ GL_SUITE=localStorage.getItem('galou-suite-v1')!=='0'; }catch(e){}
function glMicro(auto){
  const bt=document.getElementById('gl-mic'); const SR=window.SpeechRecognition||window.webkitSpeechRecognition;
  if(!SR){ alert(glT('Ce navigateur n\'a pas de micro pour Léa : utilise Chrome.','This browser has no microphone for Léa: use Chrome.','Este navegador no tiene micrófono para Léa: usa Chrome.')); return; }
  if(GL_REC){ try{ GL_REC.stop(); }catch(e){} GL_REC=null; if(bt) bt.classList.remove('on'); glMicroFerme(); return; }
  if(GL_ENV) return;
  const r=new SR(); r.lang=glLang(); r.interimResults=true; r.continuous=false; const ec=document.getElementById('gl-ecoute'); let fin='', entendu='';
  r.onresult=ev=>{ let t=''; for(let i=ev.resultIndex;i<ev.results.length;i++){ t+=ev.results[i][0].transcript; if(ev.results[i].isFinal) fin=t; } entendu=t; if(ec) ec.textContent=t; };
  r.onend=()=>{ GL_REC=null; if(bt) bt.classList.remove('on'); glMicroFerme(); if(ec) ec.textContent=''; const t=(fin||entendu||'').trim(); if(t) glEnvoie(t,true); };
  r.onerror=()=>{ GL_REC=null; if(bt) bt.classList.remove('on'); glMicroFerme(); if(ec) ec.textContent=''; };
  glCoupe();
  GL_REC=r; if(bt) bt.classList.add('on'); glMode('ecoute'); try{ r.start(); }catch(e){ GL_REC=null; if(bt) bt.classList.remove('on'); glMicroFerme(); return; }
  /* le micro aussi passe par un analyseur : la sphère bat au rythme de la voix de Sam (si le micro est refusé, battement synthétique) */
  try{ if(navigator.mediaDevices&&navigator.mediaDevices.getUserMedia){ navigator.mediaDevices.getUserMedia({audio:true}).then(f=>{ if(!GL_REC){ f.getTracks().forEach(x=>x.stop()); return; } GL_MICFLUX=f; const ac=glAudioCtx(); if(ac) glBranche(ac.createMediaStreamSource(f)); }).catch(()=>{}); } }catch(e){}
}
function glMicroFerme(){ try{ if(GL_MICFLUX){ GL_MICFLUX.getTracks().forEach(x=>x.stop()); GL_MICFLUX=null; } }catch(e){} GL_ANA=null; if(GL_MODE==='ecoute') glMode('repos'); }
function glFerme(){ const ov=document.getElementById('gl-ov'); if(ov) ov.remove(); glCoupe(); if(GL_REC){ try{ GL_REC.stop(); }catch(e){} GL_REC=null; } glMicroFerme(); cancelAnimationFrame(GL_ANIM); GL_ANIM=0; GL_MODE='repos'; }
function galouOuvre(){
  if(document.getElementById('gl-ov')) return;
  glStyle();
  const ov=document.createElement('div'); ov.id='gl-ov'; ov.className='gl-ov';
  const nom=(()=>{ try{ const s=session(); return (s&&s.nom)||''; }catch(e){ return ''; } })();
  ov.innerHTML='<div class="gl-m" role="dialog" aria-label="Léa">'
    +'<div class="gl-h"><div class="gl-orbe"><canvas id="gl-orb" width="400" height="400"></canvas><div class="gl-av" id="gl-av"></div></div><h2>Léa</h2><small id="gl-etat" data-nolang></small><small id="gl-ecoute" class="gl-ecoute" data-nolang></small><button class="x" id="gl-x" aria-label="Fermer">&times;</button></div>'
    +'<div class="gl-b" id="gl-b"></div>'
    +'<div class="gl-raccs"><button data-q="'+glT('Fais-moi le récap de la journée d\'hier.','Give me yesterday\'s recap.','Hazme el resumen de ayer.')+'">'+glT('Récap d\'hier','Yesterday\'s recap','Resumen de ayer')+'</button>'
    +'<button data-q="'+glT('Qu\'est-ce que je dois recommander rapidement ?','What should I reorder quickly?','¿Qué debo volver a pedir rápido?')+'">'+glT('À recommander','To reorder','Para pedir')+'</button>'
    +'<button data-q="'+glT('Est-ce que j\'ai loupé des ventes cette semaine ?','Did I miss any sales this week?','¿Se me escapó alguna venta esta semana?')+'">'+glT('Ventes loupées ?','Missed sales?','¿Ventas perdidas?')+'</button></div>'
    +'<div class="gl-f"><button class="mic" id="gl-mic" title="'+glT('Parler','Talk','Hablar')+'"><span class="ic">🎤</span><span class="lb">'+glT('Appuie et parle','Press and talk','Pulsa y habla')+'</span></button></div>'
    +'<div class="gl-opts"><label><input type="checkbox" id="gl-voix" '+(GL_VOIX?'checked':'')+'> '+glT('Léa parle à voix haute','Léa speaks out loud','Léa habla en voz alta')+' <span id="gl-sousvoix" data-nolang></span></label><label><input type="checkbox" id="gl-suite" '+(GL_SUITE?'checked':'')+'> '+glT('Elle réécoute après sa réponse','She listens again after answering','Vuelve a escuchar tras responder')+'</label><button class="lnk" id="gl-raz">'+glT('Nouvelle conversation','New conversation','Nueva conversación')+'</button></div></div>';
  document.body.appendChild(ov);
  ov.addEventListener('click',e=>{ if(e.target===ov) glFerme(); });
  document.getElementById('gl-x').onclick=glFerme;
  document.getElementById('gl-mic').onclick=()=>glMicro(false);
  document.getElementById('gl-voix').onchange=e=>{ GL_VOIX=e.target.checked; try{ localStorage.setItem('galou-voix-v1',GL_VOIX?'1':'0'); }catch(e2){} if(!GL_VOIX){ glCoupe(); glMode('repos'); } };
  document.getElementById('gl-suite').onchange=e=>{ GL_SUITE=e.target.checked; try{ localStorage.setItem('galou-suite-v1',GL_SUITE?'1':'0'); }catch(e2){} };
  document.getElementById('gl-raz').onclick=()=>{ glCoupe(); GL_CONV=[]; glSauve(); document.getElementById('gl-b').innerHTML=''; glAccueil(nom); };
  /* la barre d'espace = appuyer sur le micro (quand on n'écrit nulle part) */
  ov.onkeydown=e=>{ if(e.key===' '&&!/INPUT|TEXTAREA/.test((e.target||{}).tagName||'')){ e.preventDefault(); glMicro(false); } };
  ov.querySelectorAll('.gl-raccs button').forEach(b=>b.onclick=()=>glEnvoie(b.dataset.q));
  /* la photo d'Igal, si elle a été posée (Réglages › Ma société › photo de Galou, à venir) */
  try{ const R=lit('reglages-v1',{})||{}; if(R.galouPhoto){ const av=document.getElementById('gl-av'); av.innerHTML='<img src="'+R.galouPhoto+'" alt="Léa">'; av.style.display='block'; } }catch(e){}
  glMode('repos'); glOrbe();
  if(GL_CONV.length) GL_CONV.forEach(m=>glAjoute(m.role,m.content)); else glAccueil(nom);
  if(!glPeut()){ glAjoute('assistant',glT('Il faut être connecté à l\'ERP en ligne pour parler à Léa.','You need to be signed in to the online ERP to talk to Léa.','Hay que estar conectado al ERP en línea para hablar con Léa.')); return; }
  if(GL_PRET===null){ fetch(CK_URL+'/api/o/'+CK_ORG+'/galou/etat',{headers:{Authorization:'Bearer '+ckTok()}}).then(r=>r.json()).then(j=>{ GL_PRET=!!(j&&j.pret); GL_VOIX_IGAL=!!(j&&j.voix);
      const sv=document.getElementById('gl-sousvoix'); if(sv) sv.textContent=GL_VOIX_IGAL?glT('(la voix de Léa)','(Léa\'s voice)','(la voz de Léa)'):'';
      if(!GL_PRET) glAjoute('assistant',glT('Léa n\'est pas encore branchée : il manque sa clé dans le cockpit (Igal).','Léa is not connected yet: her key is missing in the cockpit (Igal).','Léa aún no está conectada: falta su clave en el cockpit (Igal).'));
      glAccuse(); /* le mot d'accueil est fabriqué d'avance, pour être prêt à la première question */ }).catch(()=>{}); }
  else if(GL_VOIX_IGAL){ const sv=document.getElementById('gl-sousvoix'); if(sv) sv.textContent=glT('(la voix de Léa)','(Léa\'s voice)','(la voz de Léa)'); }
  setTimeout(()=>{ const m=document.getElementById('gl-mic'); if(m) m.focus(); },50);
}
function glAccueil(nom){
  const p=nom?(' '+nom.split(' ')[0]):'';
  glAjoute('assistant',glT('Salut'+p+' ! Appuie sur le micro et parle-moi : le récap d\'hier, ce qu\'il faut recommander, n\'importe quel chiffre, ou comment faire quelque chose dans l\'ERP.','Hi'+p+'! Press the mic and talk to me: yesterday\'s recap, what to reorder, any number, or how to do something in the ERP.','¡Hola'+p+'! Pulsa el micro y háblame: el resumen de ayer, qué hay que pedir, cualquier cifra, o cómo hacer algo en el ERP.'));
}
window.galouOuvre=galouOuvre;
/* la pastille « Tâches » du menu : combien attendent (relue à chaque page, seulement pour qui voit les marges) */
setTimeout(()=>{ try{ const c=document.getElementById('ct-taches'); if(!c||!glPeut()||typeof peut!=='function'||!peut('voirMarge')) return;
  fetch(CK_URL+'/api/o/'+CK_ORG+'/galou/taches',{headers:{Authorization:'Bearer '+ckTok()}}).then(r=>r.ok?r.json():null).then(j=>{ if(!j) return; const n=(j.a_faire||[]).length; c.textContent=n?String(n):''; c.className=n?'ct nb':'ct'; }).catch(()=>{}); }catch(e){} },2500);
"""
