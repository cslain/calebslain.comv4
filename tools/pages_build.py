# Puts the project page content (pages_data.py) and its renderer into the site's index.html.
# To change what a project page says: edit pages_data.py, then run  python3 tools/pages_build.py
# It replaces the block between the PG markers in index.html and can be run any number of times.
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from pages_data import PAGES
P = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "index.html")
s = open(P).read()

RENDER = r'''
/* Fills the text column of a project page from __PG: facts, logline and description, cast, links, awards, press, then
   credits at the bottom. Long credit lines are clipped to two lines and open on a click; long press lists show eight
   links with a button for the rest. A project with no entry in __PG keeps the older short page. */
function __pgFill(pg){let box=De("mpage");box.textContent="";De("modal").classList.toggle("long",!!pg);if(!pg)return;
De("mclient").textContent=pg.k,De("mtitle").textContent=pg.t,De("mdesc").hidden=!0,De("mmeta").hidden=!0;
let el=(tag,cls,txt,to=box)=>{let x=document.createElement(tag);return cls&&(x.className=cls),txt!=null&&(x.textContent=txt),to.append(x),x},
clip=x=>{x.classList.add("clip"),x.tabIndex=0,x.setAttribute("role","button"),x.title="Show all";let f=()=>x.classList.toggle("clip");x.addEventListener("click",f),x.addEventListener("keydown",e=>{(e.key==="Enter"||e.key===" ")&&(e.preventDefault(),f())})},
link=(txt,url,to)=>{let a=el("a",0,txt,to);a.href=url,a.target="_blank",a.rel="noopener"},
facts=a=>{if(!a)return;let d=el("dl","mfacts");for(let[l,h]of a)el("dt",0,l,d),el("dd",0,h,d)},
body=f=>{f.log&&el("p","mlog",f.log);for(let p of f.d||[])el("p",0,p);f.note&&el("p","mnote",f.note);for(let[l,h]of[["Cast",f.cast],["Appearances",f.app]])if(h){let p=el("p","mcast");el("span","mo",l,p);let n=el("span",0,h,p);h.length>160&&clip(n)}},
list=(title,rows,mk)=>{if(!rows)return;el("h3",0,title);let u=el("ul");rows.forEach((r,i)=>{let li=el("li",0,null,u);mk(li,r),rows.length>10&&i>=8&&(li.hidden=!0)});if(rows.length>10){let b=el("button","mall","Show all "+rows.length);b.type="button",b.addEventListener("click",()=>{for(let li of u.children)li.hidden=!1;b.remove()})}};
facts(pg.f);if(pg.films)for(let f of pg.films)el("h4",0,f.t),facts(f.f),body(f);else body(pg);
if(pg.links){let p=el("p","mlinks");for(let[l,h]of pg.links)link(l,h,p)}
list("Awards and festivals",pg.aw,(li,[y,t])=>{el("span","mo",y,li),li.append(" "+t)});
list("Press",pg.pr,(li,[o,t,h])=>{el("span","mo",o,li),li.append(" "),link(t,h,li)});
let groups=pg.films?pg.films.filter(f=>f.cr).map(f=>[f.t,f.cr]):pg.cr?[[null,pg.cr]]:[];
if(groups.length){el("h3",0,"Credits");for(let[g,rows]of groups){g&&el("h4",0,g);let d=el("dl","mcred");for(let[l,h]of rows){el("dt",0,l,d);let dd=el("dd",0,h,d);h.length>110&&clip(dd)}}}}
'''
block = "/*PG-BEGIN project page content, from the 3.0 site (edit tools/pages_data.py, then run tools/pages_build.py) */\nvar __PG=" + json.dumps(PAGES, ensure_ascii=True, separators=(",", ":")) + ";" + RENDER + "/*PG-END*/"

def rep(old, new):
    global s
    assert s.count(old) == 1, (old[:70], s.count(old))
    s = s.replace(old, new)

if "/*PG-BEGIN" in s:
    s = re.sub(r"/\*PG-BEGIN.*?/\*PG-END\*/", lambda m: block, s, flags=re.S)
else:
    rep("function Sa(i){if(i.piano)return;", block + "function Sa(i){if(i.piano)return;")
    # the page asks __PG first
    rep('if(!n)return;_h=e?e.id:"adv:"+n.name,', 'if(!n)return;let pg=__PG[e?e.id:n.name];_h=e?e.id:"adv:"+n.name,')
    rep('f.textContent=h,s.append(c,f)}let a=De("mmedia");a.textContent="";let r=e?t.vimeo:n.vimeo;if(r&&Hh){let l=document.createElement("figure");l.className="embed";let h=document.createElement("iframe"),[c,f]=String(r).split("/");h.src="https://player.vimeo.com/video/"+c+"?"+(f?"h="+f+"&":"")+"title=0&byline=0&portrait=0&dnt=1",h.title=n.name,h.allow="autoplay; fullscreen; picture-in-picture",h.allowFullscreen=!0,l.append(h),a.append(l)}else if(e){',
        'f.textContent=h,s.append(c,f)}__pgFill(pg);let a=De("mmedia");a.textContent="";let r=pg?pg.v:e?t.vimeo:n.vimeo;De("modal").classList.toggle("stick",!!(pg&&Hh&&r&&r.length===1));if(r&&Hh)for(let[vid,ar,cap]of pg?r:[[r]]){let l=document.createElement("figure"),bx=document.createElement("div");bx.className="embed",ar&&(bx.style.aspectRatio=ar);let h=document.createElement("iframe"),[c,f]=String(vid).split("/");if(h.src="https://player.vimeo.com/video/"+c+"?"+(f?"h="+f+"&":"")+"title=0&byline=0&portrait=0&dnt=1",h.title=cap||n.name,h.allow="autoplay; fullscreen; picture-in-picture",h.allowFullscreen=!0,bx.append(h),l.append(bx),cap){let g=document.createElement("figcaption");g.textContent=cap,l.append(g)}a.append(l)}else if(e){')
    rep('<dl id="mmeta"></dl>', '<dl id="mmeta"></dl>\n      <div id="mpage"></div>')
    rep('#mmedia figure.embed { position: relative; aspect-ratio: 16 / 9; background: #0b0b0b; }\n  #mmedia figure.embed iframe { position: absolute; inset: 0; width: 100%; height: 100%; border: 0; }',
        '''#mmedia .embed { position: relative; aspect-ratio: 16 / 9; max-height: 78vh; background: #0b0b0b; }
  #mmedia .embed iframe { position: absolute; inset: 0; width: 100%; height: 100%; border: 0; }
  /* a full project page: the text column runs long, so it starts at the top and the film stays in view beside it */
  #modal.long .mwrap { align-items: start; }
  #mmeta[hidden] { display: none; }
  @media (min-width: 821px) { #modal.stick #mmedia { position: sticky; top: clamp(64px, 8vh, 96px); } }
  #mpage { font: 400 12px/1.6 var(--mono); letter-spacing: .01em; color: rgba(190,246,220,.86); }
  #mpage p { margin: 0 0 14px; max-width: 56ch; }
  #mpage .mlog { font-size: 14px; line-height: 1.55; color: #eafff5; }
  #mpage .mnote { font-style: italic; color: var(--gd); }
  #mpage .mo { margin-right: 6px; font-size: 10px; font-weight: 500; letter-spacing: .14em; text-transform: uppercase; color: var(--gd); }
  #mpage h3 { margin: 26px 0 12px; padding-top: 16px; border-top: 1px solid rgba(30,234,140,.3); font: 500 10px/1.3 var(--mono); letter-spacing: .18em; text-transform: uppercase; color: var(--g); }
  #mpage h4 { margin: 20px 0 8px; font: 500 12px/1.3 var(--mono); letter-spacing: .12em; text-transform: uppercase; color: #eafff5; }
  #mpage ul { list-style: none; margin: 0; padding: 0; display: grid; gap: 8px; max-width: 60ch; }
  #mpage li { line-height: 1.45; }
  #mpage a { color: var(--g); text-decoration: none; border-bottom: 1px solid rgba(30,234,140,.35); }
  #mpage a:hover, #mpage a:focus-visible { border-bottom-color: var(--g); background: rgba(30,234,140,.12); outline: none; }
  #mpage .mlinks { display: flex; flex-wrap: wrap; gap: 6px 18px; }
  #mpage dl { display: grid; grid-template-columns: auto 1fr; gap: 4px 16px; margin: 0 0 14px; max-width: 60ch; }
  #mpage dt { padding-top: 2px; font-size: 9.5px; font-weight: 500; letter-spacing: .12em; text-transform: uppercase; color: var(--gd); }
  #mpage dd { margin: 0; font-size: 11px; line-height: 1.45; }
  #mpage [role=button] { cursor: pointer; }
  #mpage .clip { display: -webkit-box; -webkit-box-orient: vertical; -webkit-line-clamp: 2; overflow: hidden; }
  #mpage [role=button]:focus-visible { outline: 1px solid var(--g); outline-offset: 2px; }
  #mpage .mall { margin-top: 10px; font: 500 10px/1 var(--mono); letter-spacing: .14em; text-transform: uppercase; color: var(--g); background: none; border: 1px solid rgba(30,234,140,.42); padding: 8px 11px 7px; cursor: pointer; }
  #mpage .mall:hover { background: var(--g); color: #04130c; }''')
open(P, "w").write(s)
print("pages:", len(PAGES), "bytes:", len(block))
