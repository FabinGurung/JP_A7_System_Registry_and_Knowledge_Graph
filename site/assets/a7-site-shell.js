/* Shared A7 site chrome: never edits content/authority or application engines. */
(() => {"use strict";
const routes=[
 ["index.html","Atlas","Explore the JP systems"],
 ["control-towers.html","Control Towers","Authorities and ownership"],
 ["repository-status.html","Mission Status","Dated provider observations"],
 ["memory-wall.html","Memory Wall","Pinned learning and visualization reminders"],
 ["roadmap.html","Roadmap","Development and priorities"],
 ["how-it-works.html","How It Works","Operator and developer guidance"],
 ["governance.html","Governance","Git and Drive control boundaries"],
 ["history.html","History & Rollback","Archived interfaces and immutable release references"],
 ["legacy-overview.html","Classic Graph","Archived advanced graph and project matrices"],
 ["milestone.html","Milestone","Pre-Galactic release record"],
 ["visualization-workspace.html","Visualization Detail","Archived technical six-view documentation"]
];
function el(tag,text,cl){const n=document.createElement(tag);if(text!==undefined)n.textContent=text;if(cl)n.className=cl;return n}
function link(path,text,active,cl){const a=el("a",text,cl);a.href=path==="index.html"?"./":path;if(active)a.setAttribute("aria-current","page");return a}
function pageId(){const last=location.pathname.split("/").pop();return routes.find(x=>x[0]===last)?last:"index.html"}
function create(){
 const id=pageId(),title=routes.find(x=>x[0]===id)||routes[0],archive=["legacy-overview.html","milestone.html","visualization-workspace.html"].includes(id);
 const header=el("header",undefined,"a7-shell-header");const brand=link("./","",false,"a7-shell-brand");
 brand.append(el("span","A7","a7-shell-emblem"));const name=el("span");
 name.append(el("strong","A7 · System Registry"),el("small","Cloud Orbit / Galactic Atlas"));brand.append(name);
 const nav=el("nav",undefined,"a7-shell-nav");nav.setAttribute("aria-label","A7 site-wide navigation");
 const primary=routes.slice(0,6);
 for(const [path,label] of primary)nav.append(link(path,label,id===path));
 const more=el("details",undefined,"a7-shell-more");const sum=el("summary","More");const menu=el("div",undefined,"a7-shell-menu");
 for(const [path,label] of routes.slice(6,8))menu.append(link(path,label,id===path));
 more.append(sum,menu);more.addEventListener("click",e=>{if(e.target.closest("a"))more.open=false;});
 document.addEventListener("click",e=>{if(more.open&&!more.contains(e.target))more.open=false;});
 nav.append(more);header.append(brand,nav);
 const ctx=el("div",undefined,"a7-shell-context");const trail=el("div");
 trail.append(el("span","A7 / "));trail.append(el("b",title[1]));
 if(archive)trail.append(el("span","  ·  Archived interface / reference"));
 ctx.append(trail);
 if(archive){const chip=el("span","History only · source preserved","a7-shell-archive-chip");ctx.append(chip)}
 else ctx.append(el("span","One site · One theme · Owner-defined data"));
 const foot=el("footer",undefined,"a7-shell-footer");const f1=el("span","A7 is a source-linked index; owning repositories remain authoritative.");
 const f2=el("span");f2.append(link("history.html","History & rollback"));f2.append(link("governance.html","Governance"));f2.append(link("memory-wall.html","Memory Wall"));foot.append(f1,f2);
 document.body.prepend(ctx);document.body.prepend(header);document.body.append(foot);
 document.body.classList.add("a7-shell-ready");if(archive)document.body.classList.add("a7-archived");
}
if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",create,{once:true});else create();
})();
