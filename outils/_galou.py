# -*- coding: utf-8 -*-
"""Galou : l'assistant d'Igal dans l'ERP (3 nov. 2026).

Igal : « j'aimerais créer un agent IA qu'on va appeler Galou, tout le temps connecté sur l'ERP ; si Sam a
besoin de quelque chose il s'adresse à lui… le matin, Sam lui dit « Salut Galou, tu me fais un récap de la
journée d'hier ? » ». Une sorte de Jarvis, avec l'avatar et la voix d'Igal.

Ce fichier : la fenêtre « Parler à Galou », ouverte depuis le menu sur n'importe quelle page. Sam écrit ou
parle (micro du navigateur), Galou répond en texte et à voix haute. La réponse vient du cockpit
(/galou/parle, voir cockpit/galou.js) : les chiffres y sont calculés par l'ERP, l'IA ne fait que les dire.

Première version : la photo d'Igal n'est pas encore là (il l'envoie), la voix est celle du navigateur ; sa
voix clonée et la vidéo du récap viendront ensuite, sans rien changer ici d'autre que la source du son.
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
.gl-ov{position:fixed;inset:0;background:rgba(20,16,30,.45);z-index:9000;display:flex;align-items:flex-end;justify-content:flex-end;padding:18px}
.gl-m{width:min(520px,100%);height:min(680px,calc(100vh - 36px));background:var(--surface);border-radius:16px;box-shadow:0 20px 60px rgba(0,0,0,.3);display:flex;flex-direction:column;overflow:hidden}
.gl-h{display:flex;align-items:center;gap:12px;padding:12px 14px;border-bottom:1px solid var(--line);background:var(--surface-2)}
.gl-av{width:46px;height:46px;border-radius:50%;background:var(--iris);color:#fff;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:16px;letter-spacing:.04em;flex:none;overflow:hidden}
.gl-av img{width:100%;height:100%;object-fit:cover}
.gl-h h2{margin:0;font-size:15px;font-weight:700;color:var(--ink)}
.gl-h small{display:block;font-size:11.5px;color:var(--ink-3);font-weight:400}
.gl-h .x{margin-left:auto;background:none;border:0;font-size:22px;color:var(--ink-3);cursor:pointer;padding:4px 8px}
.gl-b{flex:1;overflow-y:auto;padding:14px;display:flex;flex-direction:column;gap:10px;scroll-behavior:smooth}
.gl-msg{max-width:88%;padding:9px 12px;border-radius:14px;font-size:14px;line-height:1.5;white-space:pre-wrap;word-break:break-word}
.gl-msg.u{align-self:flex-end;background:var(--iris);color:#fff;border-bottom-right-radius:4px}
.gl-msg.g{align-self:flex-start;background:var(--surface-2);color:var(--ink);border-bottom-left-radius:4px}
.gl-msg.att{color:var(--ink-3);font-style:italic}
.gl-raccs{display:flex;flex-wrap:wrap;gap:6px;padding:0 14px 8px}
.gl-raccs button{font-family:inherit;font-size:12.5px;font-weight:600;color:var(--iris);background:var(--surface);border:1px solid var(--iris);border-radius:999px;padding:5px 11px;cursor:pointer}
.gl-raccs button:hover{background:var(--iris-soft)}
.gl-f{display:flex;gap:8px;padding:10px 12px;border-top:1px solid var(--line);align-items:flex-end}
.gl-f textarea{flex:1;font-family:inherit;font-size:14px;min-height:42px;max-height:120px;resize:none;padding:9px 11px;border:1px solid var(--line);border-radius:10px;background:var(--surface);color:var(--ink)}
.gl-f button{font-family:inherit;font-size:13px;font-weight:600;border:1px solid var(--line);background:var(--surface);color:var(--ink-2);border-radius:10px;padding:9px 11px;cursor:pointer;height:42px;white-space:nowrap}
.gl-f button.pri{background:var(--iris);border-color:var(--iris);color:#fff}
.gl-f button.mic.on{background:var(--crit);border-color:var(--crit);color:#fff;animation:gl-pulse 1s infinite}
@keyframes gl-pulse{0%,100%{opacity:1}50%{opacity:.6}}
.gl-opts{display:flex;gap:12px;padding:0 14px 10px;font-size:12px;color:var(--ink-3);align-items:center}
.gl-opts label{display:flex;align-items:center;gap:5px;cursor:pointer}
@media(max-width:600px){.gl-ov{padding:0}.gl-m{height:100vh;border-radius:0}}`;
  document.head.appendChild(s);
}
function glSauve(){ try{ sessionStorage.setItem(GL_K,JSON.stringify(GL_CONV.slice(-20))); }catch(e){} }
function glAjoute(role,texte,cls){
  const b=document.getElementById('gl-b'); if(!b) return null;
  const d=document.createElement('div'); d.className='gl-msg '+(role==='user'?'u':'g')+(cls?' '+cls:''); d.textContent=texte; d.setAttribute('data-nolang','');
  b.appendChild(d); b.scrollTop=b.scrollHeight; return d;
}
/* la voix : celle d'Igal (clonée, produite par le cockpit) quand le cockpit la propose ; sinon, ou si elle rate (quota du
   mois, panne), celle du navigateur. Galou ne se tait jamais. */
let GL_AUDIO=null, GL_VOIX_IGAL=null;   /* GL_VOIX_IGAL : null = on ne sait pas encore, true/false = réponse du cockpit (etat.voix) */
function glDit(texte){
  if(!GL_VOIX) return;
  try{ if(GL_AUDIO){ GL_AUDIO.pause(); GL_AUDIO=null; } }catch(e){}
  if(GL_VOIX_IGAL&&glPeut()){
    fetch(CK_URL+'/api/o/'+CK_ORG+'/galou/voix',{method:'POST',headers:{'Content-Type':'application/json',Authorization:'Bearer '+ckTok()},body:JSON.stringify({texte})})
      .then(r=>{ if(!r.ok) throw new Error('voix '+r.status); return r.blob(); })
      .then(b=>{ const u=URL.createObjectURL(b); const a=new Audio(u); GL_AUDIO=a; a.onended=()=>{ URL.revokeObjectURL(u); if(GL_AUDIO===a) GL_AUDIO=null; }; return a.play(); })
      .catch(()=>glDitNavigateur(texte));
    return;
  }
  glDitNavigateur(texte);
}
function glDitNavigateur(texte){
  if(!('speechSynthesis' in window)) return;
  try{ speechSynthesis.cancel(); const u=new SpeechSynthesisUtterance(texte); u.lang=glLang(); u.rate=1.02;
    const V=speechSynthesis.getVoices().filter(v=>v.lang&&v.lang.toLowerCase().startsWith(glLang().slice(0,2)));
    const pref=V.find(v=>/thomas|nicolas|daniel|paul|jorge|diego|male|homme/i.test(v.name))||V.find(v=>!/female|femme|amelie|audrey|marie|monica|paulina|samantha|victoria/i.test(v.name))||V[0];
    if(pref) u.voice=pref; speechSynthesis.speak(u); }catch(e){}
}
async function glEnvoie(texte){
  texte=String(texte||'').trim(); if(!texte||GL_ENV) return;
  const ta=document.getElementById('gl-t'); if(ta){ ta.value=''; }
  GL_CONV.push({role:'user',content:texte}); glSauve(); glAjoute('user',texte);
  GL_ENV=true; const att=glAjoute('assistant',glT('Galou réfléchit…','Galou is thinking…','Galou está pensando…'),'att');
  try{
    const r=await fetch(CK_URL+'/api/o/'+CK_ORG+'/galou/parle',{method:'POST',headers:{'Content-Type':'application/json',Authorization:'Bearer '+ckTok()},body:JSON.stringify({messages:GL_CONV.slice(-12),page:(document.querySelector('.main h1')||{}).textContent||''})});
    const j=await r.json().catch(()=>({}));
    if(!r.ok) throw new Error(j.erreur||('serveur '+r.status));
    /* au cas où le modèle met quand même du gras ou des puces : on les enlève, la réponse est lue à voix haute */
    const rep=String(j.texte||'').replace(/\*\*|__|^#+\s*/gm,'').replace(/^\s*[-•]\s+/gm,'').trim()||glT('(pas de réponse)','(no answer)','(sin respuesta)');
    GL_CONV.push({role:'assistant',content:rep}); glSauve();
    if(att){ att.textContent=rep; att.classList.remove('att'); }
    glDit(rep);
  }catch(e){
    const m=glT('Galou ne répond pas : ','Galou is not answering: ','Galou no responde: ')+(e&&e.message||e);
    if(att){ att.textContent=m; att.classList.remove('att'); }
    GL_CONV.pop(); glSauve();
  }
  GL_ENV=false; const b=document.getElementById('gl-b'); if(b) b.scrollTop=b.scrollHeight;
}
/* le micro : la reconnaissance vocale du navigateur (Chrome) ; la phrase part toute seule quand elle est finie */
function glMicro(){
  const bt=document.getElementById('gl-mic'); const SR=window.SpeechRecognition||window.webkitSpeechRecognition;
  if(!SR){ alert(glT('Ce navigateur n\'a pas de micro pour Galou : utilise Chrome.','This browser has no microphone for Galou: use Chrome.','Este navegador no tiene micrófono para Galou: usa Chrome.')); return; }
  if(GL_REC){ try{ GL_REC.stop(); }catch(e){} GL_REC=null; if(bt) bt.classList.remove('on'); return; }
  const r=new SR(); r.lang=glLang(); r.interimResults=true; r.continuous=false; const ta=document.getElementById('gl-t'); let fin='';
  r.onresult=ev=>{ let t=''; for(let i=ev.resultIndex;i<ev.results.length;i++){ t+=ev.results[i][0].transcript; if(ev.results[i].isFinal) fin=t; } if(ta) ta.value=t; };
  r.onend=()=>{ GL_REC=null; if(bt) bt.classList.remove('on'); const t=(fin||(ta&&ta.value)||'').trim(); if(t) glEnvoie(t); };
  r.onerror=()=>{ GL_REC=null; if(bt) bt.classList.remove('on'); };
  try{ speechSynthesis&&speechSynthesis.cancel(); if(GL_AUDIO){ GL_AUDIO.pause(); GL_AUDIO=null; } }catch(e){}
  GL_REC=r; if(bt) bt.classList.add('on'); r.start();
}
function glFerme(){ const ov=document.getElementById('gl-ov'); if(ov) ov.remove(); try{ speechSynthesis&&speechSynthesis.cancel(); if(GL_AUDIO){ GL_AUDIO.pause(); GL_AUDIO=null; } }catch(e){} if(GL_REC){ try{ GL_REC.stop(); }catch(e){} GL_REC=null; } }
function galouOuvre(){
  if(document.getElementById('gl-ov')) return;
  glStyle();
  const ov=document.createElement('div'); ov.id='gl-ov'; ov.className='gl-ov';
  const nom=(()=>{ try{ const s=session(); return (s&&s.nom)||''; }catch(e){ return ''; } })();
  ov.innerHTML='<div class="gl-m">'
    +'<div class="gl-h"><div class="gl-av" id="gl-av">IB</div><div><h2>Galou</h2><small>'+glT('l\'assistant d\'Igal — pose-lui tes questions sur l\'ERP','Igal\'s assistant — ask him about the ERP','el asistente de Igal — pregúntale sobre el ERP')+'</small></div><button class="x" id="gl-x" aria-label="Fermer">&times;</button></div>'
    +'<div class="gl-b" id="gl-b"></div>'
    +'<div class="gl-raccs"><button data-q="'+glT('Fais-moi le récap de la journée d\'hier.','Give me yesterday\'s recap.','Hazme el resumen de ayer.')+'">'+glT('Récap d\'hier','Yesterday\'s recap','Resumen de ayer')+'</button>'
    +'<button data-q="'+glT('Qu\'est-ce que je dois recommander rapidement ?','What should I reorder quickly?','¿Qué debo volver a pedir rápido?')+'">'+glT('À recommander','To reorder','Para pedir')+'</button>'
    +'<button data-q="'+glT('Est-ce que j\'ai loupé des ventes cette semaine ?','Did I miss any sales this week?','¿Se me escapó alguna venta esta semana?')+'">'+glT('Ventes loupées ?','Missed sales?','¿Ventas perdidas?')+'</button></div>'
    +'<div class="gl-opts"><label><input type="checkbox" id="gl-voix" '+(GL_VOIX?'checked':'')+'> '+glT('Galou parle à voix haute','Galou speaks out loud','Galou habla en voz alta')+' <span id="gl-sousvoix" data-nolang></span></label><button class="lnk" id="gl-raz" style="font-size:12px">'+glT('Nouvelle conversation','New conversation','Nueva conversación')+'</button></div>'
    +'<div class="gl-f"><textarea id="gl-t" rows="1" placeholder="'+glT('Écris à Galou, ou appuie sur le micro et parle…','Write to Galou, or press the mic and talk…','Escribe a Galou, o pulsa el micro y habla…')+'"></textarea>'
    +'<button class="mic" id="gl-mic" title="'+glT('Parler','Talk','Hablar')+'">🎤</button><button class="pri" id="gl-go">'+glT('Envoyer','Send','Enviar')+'</button></div></div>';
  document.body.appendChild(ov);
  ov.addEventListener('click',e=>{ if(e.target===ov) glFerme(); });
  document.getElementById('gl-x').onclick=glFerme;
  document.getElementById('gl-go').onclick=()=>glEnvoie(document.getElementById('gl-t').value);
  document.getElementById('gl-mic').onclick=glMicro;
  document.getElementById('gl-voix').onchange=e=>{ GL_VOIX=e.target.checked; try{ localStorage.setItem('galou-voix-v1',GL_VOIX?'1':'0'); }catch(e2){} if(!GL_VOIX){ try{ speechSynthesis.cancel(); if(GL_AUDIO){ GL_AUDIO.pause(); GL_AUDIO=null; } }catch(e3){} } };
  document.getElementById('gl-raz').onclick=()=>{ GL_CONV=[]; glSauve(); document.getElementById('gl-b').innerHTML=''; glAccueil(nom); };
  document.getElementById('gl-t').onkeydown=e=>{ if(e.key==='Enter'&&!e.shiftKey){ e.preventDefault(); glEnvoie(e.target.value); } };
  ov.querySelectorAll('.gl-raccs button').forEach(b=>b.onclick=()=>glEnvoie(b.dataset.q));
  /* la photo d'Igal, si elle a été posée (Réglages › Ma société › photo de Galou, à venir) */
  try{ const R=lit('reglages-v1',{})||{}; if(R.galouPhoto){ document.getElementById('gl-av').innerHTML='<img src="'+R.galouPhoto+'" alt="Igal">'; } }catch(e){}
  if(GL_CONV.length) GL_CONV.forEach(m=>glAjoute(m.role,m.content)); else glAccueil(nom);
  if(!glPeut()){ glAjoute('assistant',glT('Il faut être connecté à l\'ERP en ligne pour parler à Galou.','You need to be signed in to the online ERP to talk to Galou.','Hay que estar conectado al ERP en línea para hablar con Galou.')); return; }
  if(GL_PRET===null){ fetch(CK_URL+'/api/o/'+CK_ORG+'/galou/etat',{headers:{Authorization:'Bearer '+ckTok()}}).then(r=>r.json()).then(j=>{ GL_PRET=!!(j&&j.pret); GL_VOIX_IGAL=!!(j&&j.voix);
      const sv=document.getElementById('gl-sousvoix'); if(sv) sv.textContent=GL_VOIX_IGAL?glT('(la voix d\'Igal)','(Igal\'s voice)','(la voz de Igal)'):'';
      if(!GL_PRET) glAjoute('assistant',glT('Galou n\'est pas encore branché : il manque sa clé dans le cockpit (Igal).','Galou is not connected yet: his key is missing in the cockpit (Igal).','Galou aún no está conectado: falta su clave en el cockpit (Igal).')); }).catch(()=>{}); }
  setTimeout(()=>{ const t=document.getElementById('gl-t'); if(t) t.focus(); },50);
}
function glAccueil(nom){
  const p=nom?(' '+nom.split(' ')[0]):'';
  glAjoute('assistant',glT('Salut'+p+' ! Demande-moi le récap d\'hier, ce qu\'il faut recommander, ou n\'importe quoi sur tes ventes et ton stock.','Hi'+p+'! Ask me for yesterday\'s recap, what to reorder, or anything about your sales and stock.','¡Hola'+p+'! Pídeme el resumen de ayer, qué hay que pedir, o cualquier cosa sobre tus ventas y tu stock.'));
}
window.galouOuvre=galouOuvre;
"""
