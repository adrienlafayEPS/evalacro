#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Répare index.html tronqué (JSON + script manquants) et fusionne les PNG du dossier Cursor assets.
À lancer depuis le terminal si la page ne charge plus les numéros / visuels :
  python3 repair_and_merge_assets.py

Mode hors ligne : garder dans le même dossier index.html, sw.js, manifest.webmanifest, icon.svg
et (optionnel) icon-source.png pour le logo d’en-tête / écran d’accueil.
(et relancer ce script après modification des PNG sources). Incrémenter CACHE_NAME dans sw.js si besoin
de forcer le navigateur à recharger le cache après mise à jour.
"""
import base64
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HTML = ROOT / "index.html"
ASSETS = Path.home() / ".cursor/projects/Users-adrienlafay-Test-cursor/assets"
MARKER = 'id="pyramid-card-uris-data">'

APP_JS = r"""(function(){'use strict';
var STORAGE_KEY='acrosport-planner-v2';
var DUO=["160","161","162","163","164","165","166","167","168","172","173","174","175","176","177","180","181","182","183","184","185","186","187","188","192","193","194","195","196","197","198","199","200"];
var TRIO=["204","205","206","207","208","209","210","211","212","215","216","217","218","219","220","221","222","223","227","228","229","230","231","232","233","234","235","236","240","241","242","243","244","245","246","247","248","249","250","252"];
var QUAT=["254","255","256","257","259","260","261","262","263","267","268","269","270","271","272","273","276","277","278","279"];
var DIFF_A={"160":1,"161":1,"162":1,"172":1,"173":1,"180":1,"181":1,"182":1,"192":1,"193":1,"194":1,"204":1,"205":1,"206":1,"215":1,"216":1,"217":1,"227":1,"228":1,"229":1,"230":1,"240":1,"241":1,"259":1,"267":1,"268":1,"276":1,"254":1};
var DIFF_B={"163":1,"164":1,"165":1,"174":1,"175":1,"183":1,"184":1,"185":1,"195":1,"196":1,"197":1,"207":1,"208":1,"209":1,"218":1,"219":1,"220":1,"231":1,"232":1,"233":1,"242":1,"243":1,"244":1,"245":1,"256":1,"260":1,"261":1,"269":1,"270":1,"277":1,"255":1};
var DIFF_C={"166":1,"167":1,"168":1,"176":1,"177":1,"186":1,"187":1,"188":1,"198":1,"199":1,"200":1,"210":1,"211":1,"212":1,"221":1,"222":1,"223":1,"234":1,"235":1,"236":1,"246":1,"247":1,"248":1,"249":1,"257":1,"262":1,"263":1,"271":1,"272":1,"273":1,"278":1,"279":1};
var DIFF_D={"250":1,"252":1};
var floor=document.getElementById('floor');
var namesContainer=document.getElementById('names-container');
var figureNumbersInput=document.getElementById('figure-numbers-input');
var btnAddFigure=document.getElementById('btn-add-figure');
var btnPrint=document.getElementById('btn-print');
var btnReset=document.getElementById('btn-reset');
var printMeta=document.getElementById('print-meta');
var floorZonesEl=document.getElementById('floor-zones');
var dispositionSelect=document.getElementById('floor-disposition');
var btnDuo=document.getElementById('btn-duo');
var btnTrio=document.getElementById('btn-trio');
var btnQuatuor=document.getElementById('btn-quatuor');
var numberPreviewWrap=document.getElementById('number-live-preview');
var numberPreviewImg=document.getElementById('number-live-preview-img');
var cardDataEl=document.getElementById('pyramid-card-uris-data');
var cardUris={};
try{cardUris=JSON.parse(cardDataEl.textContent||'{}')||{};}catch(_){cardUris={};}
var groupSize=2,rosterNames=['','','','','',''],figureNumbersNote='',figures=[],dragState=null,floorDisposition='5';
function uid(){return 'f-'+Math.random().toString(36).slice(2,11);}
function clamp(n,a,b){return Math.min(b,Math.max(a,n));}
function normalizeType(v){if(v===4||v==='4')return 4;if(v===3||v==='3')return 3;return 2;}
function typeLabel(t){return t===2?'Duo':(t===3?'Trio':'Quatuor');}
function normalizeDisposition(v){var o=String(v||'').trim();if(['1','2v','2h','3','4','5','6'].indexOf(o)!==-1)return o;return '5';}
function applyDisposition(){if(!floorZonesEl)return;var d=normalizeDisposition(floorDisposition);floorZonesEl.className='floor-zones disp-'+d;if(dispositionSelect)dispositionSelect.value=d;}
function cardFor(num){num=String(num||'').trim();return cardUris[num]||'';}
function difficultyForNumber(num){num=String(num||'').trim();if(DIFF_A[num])return 'A';if(DIFF_B[num])return 'B';if(DIFF_C[num])return 'C';if(DIFF_D[num])return 'D';return '';}
function numbersForType(t){return t===2?DUO:(t===3?TRIO:QUAT);}
function refreshButtons(){btnDuo.classList.toggle('is-active',groupSize===2);btnTrio.classList.toggle('is-active',groupSize===3);btnQuatuor.classList.toggle('is-active',groupSize===4);}
function updateNumberPreview(){var uri=cardFor(figureNumbersInput.value);if(!uri){numberPreviewWrap.classList.remove('is-visible');numberPreviewImg.removeAttribute('src');return;}numberPreviewWrap.classList.add('is-visible');numberPreviewImg.src=uri;}
function refreshNumberOptions(){var allowed=numbersForType(groupSize),wanted=String(figureNumbersNote||'').trim();figureNumbersInput.innerHTML='';allowed.forEach(function(n){var o=document.createElement('option');o.value=n;o.textContent=n;figureNumbersInput.appendChild(o);});if(!allowed.length){figureNumbersInput.disabled=true;figureNumbersNote='';updateNumberPreview();return;}figureNumbersInput.disabled=false;if(allowed.indexOf(wanted)===-1)wanted=allowed[0];figureNumbersInput.value=wanted;figureNumbersNote=wanted;updateNumberPreview();}
function rosterDisplayName(i){var t=String(rosterNames[i]||'').trim();return t||('Élève '+(i+1));}
function countPicked(){var n=0;for(var i=0;i<6;i++){var b=document.getElementById('pick-'+i);if(b&&b.classList.contains('is-active')&&!b.disabled)n++;}return n;}
function trimExtraPicks(){while(countPicked()>groupSize){var found=false;for(var i=5;i>=0;i--){var b=document.getElementById('pick-'+i);if(b&&b.classList.contains('is-active')){b.classList.remove('is-active');found=true;break;}}if(!found)break;}}
function getPickedNames(){var out=[];for(var i=0;i<6;i++){var b=document.getElementById('pick-'+i);if(!b||!b.classList.contains('is-active')||b.disabled)continue;var nm=String(rosterNames[i]||'').trim();if(nm)out.push(nm);}return out;}
function syncPickRow(i){var b=document.getElementById('pick-'+i);if(!b)return;var t=String(rosterNames[i]||'').trim();b.textContent=rosterDisplayName(i);b.disabled=!t;if(!t)b.classList.remove('is-active');}
function onPickClick(ev){var b=ev&&ev.currentTarget;if(!b||b.disabled)return;if(b.classList.contains('is-active')){b.classList.remove('is-active');save();return;}if(countPicked()>=groupSize)return;b.classList.add('is-active');save();}
function renderRosterCheckboxes(){if(!namesContainer)return;namesContainer.innerHTML='';for(var i=0;i<6;i++){var b=document.createElement('button');b.type='button';b.className='btn btn-secondary roster-pick-btn';b.id='pick-'+i;b.dataset.rosterIndex=String(i);b.textContent=rosterDisplayName(i);var t=String(rosterNames[i]||'').trim();b.disabled=!t;b.addEventListener('click',onPickClick);namesContainer.appendChild(b);}updatePickHint();}
function hydrateRosterInputs(){for(var i=0;i<6;i++){var el=document.getElementById('roster-'+i);if(el)el.value=rosterNames[i]||'';}}
function bindRosterInputs(){for(var i=0;i<6;i++){var el=document.getElementById('roster-'+i);if(!el)continue;el.addEventListener('input',function(){var j=parseInt(this.id.replace('roster-',''),10);if(isNaN(j))return;rosterNames[j]=String(this.value||'').trim();syncPickRow(j);updatePickHint();save();});}}
function updatePickHint(){var el=document.getElementById('roster-pick-hint');var lb=document.getElementById('roster-pick-label');if(lb)lb.textContent='Participants sur cette figure ('+groupSize+' requis)';if(el)el.textContent='Sélectionne exactement '+groupSize+' prénom'+(groupSize>1?'s':'')+' comme pour Duo / Trio / Quatuor (ordre des boutons = ordre sur la pyramide).';}
function escapeHtml(s){var d=document.createElement('div');d.textContent=s;return d.innerHTML;}
function passageLabel(i){return'Pyramide '+(i+1);}
function typeClass(t){return t===2?'duo':(t===3?'trio':'quatuor');}
function updatePrintMeta(){var names=getPickedNames().join(' · ');var extra=[];if(names)extra.push(names);extra.push(typeLabel(groupSize));if(figureNumbersNote)extra.push('N° liste '+figureNumbersNote);printMeta.textContent=extra.join(' — ');}
function moveFigure(fid,dir){var i=-1;for(var k=0;k<figures.length;k++){if(figures[k].id===fid){i=k;break;}}if(i<0)return;var j=i+dir;if(j<0||j>=figures.length)return;var t=figures[i];figures[i]=figures[j];figures[j]=t;save();renderFigures();}
function removeFigure(fid){figures=figures.filter(function(f){return f.id!==fid;});save();renderFigures();}
function renderFigures(){var blocks=floor.querySelectorAll('.figure-block');for(var b=0;b<blocks.length;b++){blocks[b].remove();}figures.forEach(function(fig,idx){var uri=cardFor(fig.pyramidNumber);var tc=typeClass(fig.pyramidType);var diff=difficultyForNumber(fig.pyramidNumber);var diffTxt=diff?' · Diff. '+diff:'';var el=document.createElement('div');el.className='figure-block '+tc;el.dataset.id=fig.id;el.style.left=fig.xPct+'%';el.style.top=fig.yPct+'%';el.style.transform='translate(-50%,-50%)';var ob=document.createElement('div');ob.className='order-buttons';var b0=document.createElement('button');b0.type='button';b0.className='btn-order';b0.textContent='▲';b0.title='Descendre dans l\'ordre (pyramide suivante)';b0.disabled=idx===figures.length-1;b0.addEventListener('click',function(e){e.stopPropagation();moveFigure(fig.id,1);});var b1=document.createElement('button');b1.type='button';b1.className='btn-order';b1.textContent='▼';b1.title='Remonter vers pyramide 1';b1.disabled=idx===0;b1.addEventListener('click',function(e){e.stopPropagation();moveFigure(fig.id,-1);});ob.appendChild(b0);ob.appendChild(b1);var ol=document.createElement('div');ol.className='pyramid-order-label';ol.textContent=passageLabel(idx);var tb=document.createElement('div');tb.className='type-badge';tb.innerHTML='<span class="type-badge-title">'+escapeHtml(typeLabel(fig.pyramidType))+'</span><span class="type-badge-num">N° '+escapeHtml(String(fig.pyramidNumber||''))+escapeHtml(diffTxt)+'</span>';var gn=document.createElement('div');gn.className='group-names-static';gn.textContent=fig.groupNamesText||'';var img=null;if(uri){img=document.createElement('img');img.className='figure-card-preview';img.alt='Pyramide '+String(fig.pyramidNumber);img.decoding='async';img.src=uri;}var del=document.createElement('button');del.type='button';del.className='figure-delete-btn';del.textContent='×';del.title='Supprimer';del.addEventListener('pointerdown',function(e){e.stopPropagation();});del.addEventListener('click',function(e){e.stopPropagation();removeFigure(fig.id);});el.appendChild(ol);el.appendChild(ob);el.appendChild(tb);if(img)el.appendChild(img);el.appendChild(gn);el.appendChild(del);el.addEventListener('pointerdown',onFigurePointerDown);floor.appendChild(el);});}
function floorRect(){return floor.getBoundingClientRect();}
function onFigurePointerDown(ev){if(ev.button!==undefined&&ev.button!==0)return;var t=ev.target;if(t.closest('.btn-order')||t.closest('.figure-delete-btn'))return;var block=ev.currentTarget;var id=block.dataset.id;var fig=null;for(var i=0;i<figures.length;i++){if(figures[i].id===id){fig=figures[i];break;}}if(!fig)return;var r=floorRect();var bx=block.getBoundingClientRect();dragState={id:id,ox:ev.clientX,oy:ev.clientY,sl:fig.xPct,st:fig.yPct,pl:r.left,pt:r.top,pw:r.width,ph:r.height,bw:bx.width,bh:bx.height};block.classList.add('is-dragging');try{block.setPointerCapture(ev.pointerId);}catch(_){}window.addEventListener('pointermove',onFigurePointerMove);window.addEventListener('pointerup',onFigurePointerUp,{once:true});window.addEventListener('pointercancel',onFigurePointerUp,{once:true});ev.preventDefault();}
function onFigurePointerMove(ev){if(!dragState)return;var dx=ev.clientX-dragState.ox;var dy=ev.clientY-dragState.oy;var nx=dragState.sl+(dx/dragState.pw)*100;var ny=dragState.st+(dy/dragState.ph)*100;nx=clamp(nx,4,96);ny=clamp(ny,4,96);var fig=null;for(var i=0;i<figures.length;i++){if(figures[i].id===dragState.id){fig=figures[i];break;}}if(!fig)return;fig.xPct=nx;fig.yPct=ny;var b=floor.querySelector('.figure-block[data-id="'+dragState.id+'"]');if(b){b.style.left=nx+'%';b.style.top=ny+'%';}}
function onFigurePointerUp(ev){if(!dragState)return;var id=dragState.id;var fig=null;for(var i=0;i<figures.length;i++){if(figures[i].id===id){fig=figures[i];break;}}var b=floor.querySelector('.figure-block[data-id="'+id+'"]');if(b){b.classList.remove('is-dragging');try{b.releasePointerCapture(ev.pointerId);}catch(_){}}dragState=null;save();window.removeEventListener('pointermove',onFigurePointerMove);}
function addFigure(){var gs=normalizeType(groupSize);var picked=getPickedNames();if(picked.length!==gs){alert('Merci de sélectionner exactement '+gs+' prénom'+(gs>1?'s':'')+' parmi les boutons participants (section 2), pour correspondre au type Duo / Trio / Quatuor.');return;}if(!figureNumbersInput||figureNumbersInput.disabled){alert('Choisis un numéro de pyramide dans la liste.');return;}var num=String(figureNumbersInput.value||'').trim();if(!num){alert('Choisis un numéro de pyramide dans la liste.');return;}var names=picked.join(' · ');figures.push({id:uid(),pyramidType:normalizeType(gs),pyramidNumber:num,groupNamesText:names,xPct:clamp(18+figures.length*5,12,88),yPct:clamp(22+figures.length*7,12,78)});for(var i=0;i<6;i++){var b=document.getElementById('pick-'+i);if(b)b.classList.remove('is-active');}save();renderFigures();}
function save(){try{localStorage.setItem(STORAGE_KEY,JSON.stringify({groupSize:groupSize,roster:rosterNames,figureNumbersNote:figureNumbersNote,figures:figures,floorDisposition:floorDisposition}));}catch(_){}}
function load(){groupSize=2;rosterNames=['','','','','',''];figureNumbersNote='';figures=[];floorDisposition='5';try{var raw=localStorage.getItem(STORAGE_KEY);if(raw){var d=JSON.parse(raw);if(d.groupSize)groupSize=normalizeType(d.groupSize);if(Array.isArray(d.roster)){for(var ri=0;ri<6;ri++)rosterNames[ri]=ri<d.roster.length&&typeof d.roster[ri]==='string'?d.roster[ri]:'';}else if(Array.isArray(d.studentNames)){for(var si=0;si<6;si++)rosterNames[si]=si<d.studentNames.length&&typeof d.studentNames[si]==='string'?d.studentNames[si]:'';}if(typeof d.figureNumbersNote==='string')figureNumbersNote=d.figureNumbersNote;if(typeof d.floorDisposition==='string')floorDisposition=normalizeDisposition(d.floorDisposition);if(Array.isArray(d.figures))figures=d.figures.map(function(r){return {id:r.id||uid(),pyramidType:normalizeType(r.pyramidType!==undefined?r.pyramidType:r.type),pyramidNumber:typeof r.pyramidNumber==='string'?r.pyramidNumber:'',groupNamesText:typeof r.groupNamesText==='string'?r.groupNamesText:'',xPct:typeof r.xPct==='number'?r.xPct:10,yPct:typeof r.yPct==='number'?r.yPct:10};});}}catch(_){}hydrateRosterInputs();bindRosterInputs();refreshButtons();refreshNumberOptions();renderRosterCheckboxes();applyDisposition();renderFigures();}
function setGroupSize(n){groupSize=normalizeType(n);trimExtraPicks();refreshButtons();refreshNumberOptions();updatePickHint();save();}
btnDuo.addEventListener('click',function(){setGroupSize(2);});
btnTrio.addEventListener('click',function(){setGroupSize(3);});
btnQuatuor.addEventListener('click',function(){setGroupSize(4);});
figureNumbersInput.addEventListener('change',function(){figureNumbersNote=figureNumbersInput.value;updateNumberPreview();save();});
if(dispositionSelect){dispositionSelect.addEventListener('change',function(){floorDisposition=normalizeDisposition(this.value);applyDisposition();save();});}
if(btnAddFigure)btnAddFigure.addEventListener('click',addFigure);
btnPrint.addEventListener('click',function(){updatePrintMeta();requestAnimationFrame(function(){requestAnimationFrame(function(){window.print();});});});
btnReset.addEventListener('click',function(){if(!confirm('Effacer toutes les figures, la liste des prénoms et le numéro sélectionné ?'))return;figures=[];rosterNames=['','','','','',''];figureNumbersNote='';groupSize=2;hydrateRosterInputs();refreshButtons();refreshNumberOptions();renderRosterCheckboxes();renderFigures();save();});
window.addEventListener('resize',renderFigures);
load();
})();"""


def main():
    raw = HTML.read_text(encoding="utf-8", errors="replace")
    i = raw.find(MARKER)
    if i < 0:
        raise SystemExit("Marqueur pyramid-card-uris-data introuvable.")
    prefix = raw[: i + len(MARKER)]
    json_tail = raw[i + len(MARKER) :]

    pat = re.compile(r'"(\d{3})":"(data:image/[^"]+)"')
    obj = {k: v for k, v in pat.findall(json_tail)}

    if ASSETS.is_dir():
        png_pat = re.compile(r"^(\d{3})-.+\.png$")
        by_key = {}
        for p in ASSETS.iterdir():
            if not p.is_file():
                continue
            m = png_pat.match(p.name)
            if not m:
                continue
            k = m.group(1)
            mt = p.stat().st_mtime
            if k not in by_key or mt > by_key[k][0]:
                by_key[k] = (mt, p)
        for k, (_, p) in by_key.items():
            b64 = base64.standard_b64encode(p.read_bytes()).decode("ascii")
            obj[k] = "data:image/png;base64," + b64
        print("Images depuis assets :", len(by_key))
    else:
        print("Dossier assets absent :", ASSETS)

    json_str = json.dumps(obj, ensure_ascii=False, separators=(",", ":"))
    sw_register = (
        "<script>if(location.protocol!=='file:'&&'serviceWorker' in navigator)"
        "{navigator.serviceWorker.register('./sw.js',{scope:'./'}).catch(function(){});}"
        "</script>"
    )
    out = prefix + json_str + "</script><script>" + APP_JS + "</script>" + sw_register + "</body></html>"
    tmp = HTML.with_suffix(".html.tmp")
    tmp.write_text(out, encoding="utf-8")
    written = tmp.read_text(encoding="utf-8", errors="replace")
    if written.count("</script>") < 2 or "STORAGE_KEY" not in written or not written.rstrip().endswith("</html>"):
        tmp.unlink(missing_ok=True)
        raise SystemExit(
            "Écriture ou contenu invalide après reconstruction — index.html non remplacé. "
            "Vérifie l’espace disque et réessaie."
        )
    tmp.replace(HTML)
    print("OK —", len(out), "octets,", len(obj), "numéros de pyramide dans le JSON.")


if __name__ == "__main__":
    main()
