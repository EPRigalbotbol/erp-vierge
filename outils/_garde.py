# -*- coding: utf-8 -*-
"""Le garde-fou « copie téléchargée » : ajouté à la fin de chaque page."""
GARDE = r"""
/* ---------------------------------------------------------------
   Ouvert depuis une copie (Téléchargements, Bureau) : les autres
   rubriques ne sont pas à côté du fichier, les liens tombent dans le
   vide. On répare les liens avec le dossier de l'outil mémorisé, et on
   le dit clairement.
   --------------------------------------------------------------- */
(function(){
  if(location.protocol!=='file:') return;
  try{
    var p=decodeURIComponent(location.pathname);
    var i=p.lastIndexOf('/'), fichier=p.slice(i+1);
    var dossier=p.slice(0,i).split('/').filter(Boolean).pop()||'';
    var K='dossier-outil-v1';
    var copie=/_\d+\.html$/i.test(fichier)
      || /^(downloads|t[ée]l[ée]chargements|desktop|bureau|documents)$/i.test(dossier);
    var base=location.href.slice(0,location.href.lastIndexOf('/')+1);
    if(!copie){ try{ localStorage.setItem(K,base); }catch(e){} return; }
    var vrai=''; try{ vrai=localStorage.getItem(K)||''; }catch(e){}
    var n=0;
    if(vrai && vrai!==base){
      document.querySelectorAll('a[href$=".html"]').forEach(function(a){
        var h=a.getAttribute('href');
        if(!h || /^([a-z]+:|\/|#)/i.test(h)) return;
        a.setAttribute('href',vrai+h); n++;
      });
    }
    var d=document.createElement('div');
    d.setAttribute('style','margin:0 0 18px;padding:13px 16px;border-radius:0 8px 8px 0;'
      +'background:var(--warn-soft,#FBF3E2);border-left:3px solid var(--warn,#8A5A00);'
      +'color:var(--ink-2,#4A4A56);font-size:13.5px;line-height:1.6;max-width:88ch');
    d.innerHTML='<b style="color:var(--ink,#17171D)">Tu as ouvert une copie de la page, pas l\'outil.</b> '
      +'Ce fichier est dans « '+dossier+' » : les autres rubriques ne sont pas à côté de lui. '
      +(n? 'J\'ai réparé les '+n+' liens de la barre de gauche pour cette fois. ' : '')
      +'Pour de bon : ouvre le dossier <b>perfumestrade</b> sur ton Bureau et double-clique le fichier qui s\'y trouve '
      +'(pas la copie des Téléchargements). Tes saisies ne sont pas dans le fichier : elles restent dans le navigateur.';
    var cible=document.querySelector('.wrap')||document.body;
    cible.insertBefore(d,cible.firstChild);
  }catch(e){}
})();
"""
