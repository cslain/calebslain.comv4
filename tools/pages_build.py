# Puts the project page content (pages_data.py), its renderer and its styles into the site's index.html.
# To change what a project page says: edit pages_data.py, then run  python3 tools/pages_build.py
# It replaces the blocks between the PG markers in index.html and can be run any number of times.
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from pages_data import PAGES
P = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "index.html")
s = open(P).read()

RENDER = r'''
/* Fills the text column of a project page from __PG, in the order the project doc sets: section line with a
   "Watch on Vimeo" link, title, facts, logline and description, featuring, links, awards, press, then credits at the
   bottom. Long credit lists fold behind "Full credits +", long credit lines clip to two lines and open on a click, and
   long press lists show eight links with a button for the rest. A project with no entry in __PG keeps the older short page. */
function __pgFill(pg){let box=De("mpage");box.textContent="";De("modal").classList.toggle("long",!!pg);if(!pg)return;
let el=(tag,cls,txt,to=box)=>{let x=document.createElement(tag);return cls&&(x.className=cls),txt!=null&&(x.textContent=txt),to.append(x),x},
clip=x=>{x.classList.add("clip"),x.tabIndex=0,x.setAttribute("role","button"),x.title="Show all";let f=()=>x.classList.toggle("clip");x.addEventListener("click",f),x.addEventListener("keydown",e=>{(e.key==="Enter"||e.key===" ")&&(e.preventDefault(),f())})},
link=(txt,url,to)=>{let a=el("a",0,txt,to);a.href=url,a.target="_blank",a.rel="noopener"},
more=(txt,show)=>{let b=el("button","mall",txt);b.type="button",b.addEventListener("click",()=>{show(),b.remove()})},
facts=a=>{if(!a)return;let d=el("dl","mfacts");for(let[l,h]of a)el("dt",0,l,d),el("dd",0,h,d)},
body=f=>{f.log&&el("p","mlog",f.log);for(let p of f.d||[])el("p",0,p);f.note&&el("p","mnote",f.note);if(f.feat){let p=el("p","mcast");el("span","mo","Featuring",p);let n=el("span",0,f.feat,p);f.feat.length>160&&clip(n)}},
list=(title,rows)=>{if(!rows.length)return;el("h3",0,title);let u=el("ul");rows.forEach(([mk,r],i)=>{let li=el("li",0,null,u);mk(li,r),rows.length>10&&i>=8&&(li.hidden=!0)});rows.length>10&&more("Show all "+rows.length,()=>{for(let li of u.children)li.hidden=!1})},
award=(li,[y,t,h])=>{h&&li.classList.add("mhl"),el("span","mo",y,li),li.append(" "+t)},
press=(li,[o,t,h])=>{el("span","mo",o,li),li.append(" "),link(t,h,li)};
let k=De("mclient");k.textContent=pg.s+(pg.films||!pg.v?"":" · ");pg.films||!pg.v||link("Watch on Vimeo","https://vimeo.com/"+pg.v[pg.v.length-1][0],k);
De("mtitle").textContent=pg.t,De("mdesc").hidden=!0,De("mmeta").hidden=!0;
pg.k&&el("p","mline",pg.k);facts(pg.f);if(pg.films)for(let f of pg.films)el("h4",0,f.t),facts(f.f),body(f);else body(pg);
if(pg.links){let p=el("p","mlinks");for(let[l,h]of pg.links)link(l,h,p)}
let aw=(pg.aw||[]).map(r=>[award,r]),pr=(pg.pr||[]).map(r=>[press,r]);
aw.length&&pr.length&&aw.length+pr.length<=4?list("Press + Awards",[...aw,...pr]):(list("Festivals + Honors",aw),list("Press",pr));
let groups=pg.films?pg.films.filter(f=>f.cr).map(f=>[f.t,f.cr]):pg.cr?[[null,pg.cr]]:[];
if(groups.length){el("h3",0,"Credits");for(let[g,rows]of groups){g&&el("h4",0,g);let d=el("dl","mcred"),fold=rows.length>8;rows.forEach(([l,h],i)=>{let dt=el("dt",0,l,d),dd=el("dd",0,h,d);h.length>110&&clip(dd),fold&&i>=6&&(dt.hidden=dd.hidden=!0)});fold&&more("Full credits +",()=>{for(let x of d.children)x.hidden=!1})}}}
'''
JS = "/*PG-BEGIN project page content, from the 3.0 site (edit tools/pages_data.py, then run tools/pages_build.py) */\nvar __PG=" + json.dumps(PAGES, ensure_ascii=True, separators=(",", ":")) + ";" + RENDER + "/*PG-END*/"

CSS = '''/*PGCSS-BEGIN project page styles (tools/pages_build.py) */
  #mmedia .embed { position: relative; aspect-ratio: 16 / 9; max-height: 78vh; background: #0b0b0b; }
  #mmedia .embed iframe { position: absolute; inset: 0; width: 100%; height: 100%; border: 0; }
  /* a full project page: the text column runs long, so it starts at the top and the film stays in view beside it */
  #modal.long .mwrap { align-items: start; }
  #mmeta[hidden] { display: none; }
  @media (min-width: 821px) { #modal.stick #mmedia { position: sticky; top: clamp(64px, 8vh, 96px); } }
  .mk a { color: var(--g); text-decoration: none; border-bottom: 1px solid rgba(30,234,140,.35); }
  .mk a:hover, .mk a:focus-visible { border-bottom-color: var(--g); background: rgba(30,234,140,.12); outline: none; }
  /* rows folded away stay away: a clipped line sets its own display, which would otherwise beat the hidden attribute */
  #mpage [hidden] { display: none !important; }
  #mpage { font: 400 12px/1.6 var(--mono); letter-spacing: .01em; color: rgba(190,246,220,.86); }
  #mpage p { margin: 0 0 14px; max-width: 56ch; }
  #mpage .mline { margin: -8px 0 16px; font-size: 10px; font-weight: 500; letter-spacing: .14em; text-transform: uppercase; color: var(--gd); }
  #mpage .mlog { font-size: 14px; line-height: 1.55; color: #eafff5; }
  #mpage .mnote { font-style: italic; color: var(--gd); }
  #mpage .mo { margin-right: 6px; font-size: 10px; font-weight: 500; letter-spacing: .14em; text-transform: uppercase; color: var(--gd); }
  #mpage h3 { margin: 26px 0 12px; padding-top: 16px; border-top: 1px solid rgba(30,234,140,.3); font: 500 10px/1.3 var(--mono); letter-spacing: .18em; text-transform: uppercase; color: var(--g); }
  #mpage h4 { margin: 20px 0 8px; font: 500 12px/1.3 var(--mono); letter-spacing: .12em; text-transform: uppercase; color: #eafff5; }
  #mpage ul { list-style: none; margin: 0; padding: 0; display: grid; gap: 8px; max-width: 60ch; }
  #mpage li { line-height: 1.45; }
  #mpage li.mhl { color: #f1fff8; text-shadow: 0 0 14px rgba(30,234,140,.55); }
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
  #mpage .mall:hover { background: var(--g); color: #04130c; }
  /*PGCSS-END*/'''

def rep(old, new):
    global s
    assert s.count(old) == 1, (old[:70], s.count(old))
    s = s.replace(old, new)

assert "/*PG-BEGIN" in s, "index.html has no project page block: start from a copy that has one"
s = re.sub(r"/\*PG-BEGIN.*?/\*PG-END\*/", lambda m: JS, s, flags=re.S)
if "/*PGCSS-BEGIN" in s:
    s = re.sub(r"/\*PGCSS-BEGIN.*?/\*PGCSS-END\*/", lambda m: CSS, s, flags=re.S)
else:  # the first version put the styles in without markers
    a = s.index("#mmedia .embed { position: relative;"); z = "#mpage .mall:hover { background: var(--g); color: #04130c; }"
    s = s[:a] + CSS + s[s.index(z) + len(z):]
# portfolio cards and wall labels use the page's own title where there is one
if "__PG&&__PG[i.name]" not in s:
    rep('G1=i=>i.client===i.name?i.name:i.client+" \\u2014 "+i.name;', 'G1=i=>__PG&&__PG[i.name]?__PG[i.name].t:i.client===i.name?i.name:i.client+" \\u2014 "+i.name;')
open(P, "w").write(s)
print("pages:", len(PAGES), "bytes:", len(JS))
