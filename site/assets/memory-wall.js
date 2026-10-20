/* A7 Memory Wall: passive-recall posters. Not an Anki/quiz or Drive/registry editor. */
(() => {"use strict";
const get=id=>document.getElementById(id);
const holder=get("posters"),meta=get("board-source"),filters=get("category-filters"),count=get("wall-count");
let entries=[], categories=[], active="all";
function create(tag,className,text){
 const n=document.createElement(tag);
 if(className)n.className=className;
 if(text!==undefined)n.textContent=String(text);
 return n;
}
function validLink(value){
 try{const x=new URL(value);return x.protocol==="https:" && x.hostname==="github.com" && /^\/[a-zA-Z0-9_.-]+\/[a-zA-Z0-9_.-]+\/?$/.test(x.pathname);}
 catch{return false;}
}
function render(){
 holder.replaceChildren();
 const shown=active==="all"?entries:entries.filter(p=>p.category===active);
 count.textContent=String(shown.length).padStart(2,"0")+" POSTER"+(shown.length===1?"":"S");
 if(!shown.length){holder.append(create("p","loading-poster","No posters match this category."));return;}
 for(const [i,p] of shown.entries()){
  const card=create("article","poster-card");
  card.dataset.theme=p.theme;card.setAttribute("aria-label",p.title+" reference poster");
  const head=create("div","poster-meta");
  head.append(create("span",null,p.label),create("span","poster-numeral",p.id));
  card.append(head,create("div","poster-icon",p.icon),create("h3","poster-title",p.title),create("p","poster-summary",p.summary));
  const memory=create("div","poster-action");
  memory.append(create("small",null,"REMEMBER THIS"),create("strong",null,p.big_word));
  const when=create("p","poster-when",p.remember);
  memory.append(when);card.append(memory);
  const url=validLink(p.url)?p.url:null;
  if(url){
   const a=create("a","poster-link","Open "+p.repository+" ↗");
   a.href=url;a.target="_blank";a.rel = "noopener noreferrer";
   card.append(a);
  }else{card.append(create("p","poster-foot","Source URL not verified; link unavailable."));}
  card.append(create("div","poster-foot","PUBLIC BOOKMARK · NOT AN A7 MODULE"));
  holder.append(card);
 }
}
function setup(data){
 if(data.non_authoritative!==true || data.schema_version!=="1.0.0" || !Array.isArray(data.posters))throw Error("Invalid derived collection");
 if(!data.posters.length)throw Error("Empty wall");
 entries=data.posters;categories=data.categories;
 for(const cat of categories){
  const b=create("button","filter-chip",cat.label);b.type="button";b.dataset.filter=cat.id;b.setAttribute("aria-pressed","false");
  filters.append(b);
 }
 filters.addEventListener("click",event=>{
  const b=event.target.closest("button[data-filter]");
  if(!b || !filters.contains(b))return;
  active=b.dataset.filter;
  filters.querySelectorAll("button").forEach(x=>{const selected=x.dataset.filter===active;x.classList.toggle("active",selected);x.setAttribute("aria-pressed",String(selected));});
  render();
 });
 meta.textContent="Verified public links "+data.verified_on+" · GitHub source snapshot · machine projection "+String(data.site_build_commit_sha||"").slice(0,12)+" · not live monitoring";
 render();
}
get("print-posters").addEventListener("click",()=>window.print());
fetch("data/memory-posters.json",{cache:"no-store"})
 .then(r=>{if(!r.ok)throw Error("HTTP "+r.status);return r.json()}).then(setup)
 .catch(e=>{
  holder.replaceChildren();
  const fallback=create("div","fallback-note","Poster data temporarily unavailable. Open the three verified links:");
  for(const [name,url] of [
   ["Developer Roadmap","https://github.com/nilbuild/developer-roadmap"],
   ["Public APIs","https://github.com/public-apis/public-apis"],
   ["React Interview Questions","https://github.com/sudheerj/reactjs-interview-questions"]
  ]){const a=create("a",null,name);a.href=url;a.target="_blank";a.rel="noopener noreferrer";fallback.append(a);}
  holder.append(fallback);
  meta.textContent="Read-only fallback · "+e.message;
 });
})();