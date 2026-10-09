(() => {
"use strict";
const $=s=>document.querySelector(s);
const escapeValue=x=>String(x==null?"":x);
const nodeById=new Map(); let data; let tier="all"; let selected=null;
const make=(tag,cls,value)=>{const d=document.createElement(tag);if(cls)d.className=cls;if(value!==undefined)d.textContent=escapeValue(value);return d};
const human=id=>(id||"").replaceAll("_"," ");
function renderInspector(id) {
 const n=nodeById.get(id);if(!n)return;selected=id;
 const root=$("#ct-inspector");root.replaceChildren();
 root.append(make("p","ct-eyebrow",n.tier.toUpperCase()+" / "+human(n.kind)),make("h3",null,n.label),make("p",null,n.summary));
 root.append(make("p",null,"Owning authority: "+n.owner));
 root.append(make("p",null,"Evidence/status: "+human(n.status)));
 const code=make("p",null,"Read-first or contract: ");code.append(make("code",null,n.code));root.append(code);
 if(n.link){const a=make("a",null,"Open verified source ↗");a.href=n.link;a.rel="noopener noreferrer";if(n.link.startsWith("https://"))a.target="_blank";root.append(a);}
 else root.append(make("p",null,"Private provider object. Fetch live via your authorized Google Drive account; this public site does not expose its ID."));
 root.append(make("h3",null,"Related controls"));
 for(const e of data.edges.filter(x=>x.source===id||x.target===id)){
  const other=nodeById.get(e.source===id?e.target:e.source);
  if(!other)continue;
  const b=make("button","ct-connection");b.type="button";b.style.cssText="background:transparent;border:0;border-bottom:1px solid #dfeaf2;width:100%;text-align:left;cursor:pointer";
  b.append(make("strong",null,other.label),make("span",null,human(e.relation)));b.onclick=()=>{renderInspector(other.id);document.querySelector('[data-node-id="'+other.id+'"]')?.scrollIntoView({block:"nearest",behavior:"smooth"});};root.append(b);
 }
 document.querySelectorAll(".ct-card").forEach(x=>x.setAttribute("aria-pressed",String(x.dataset.nodeId===id)));
}
function renderCards(){
 const q=$("#ct-search").value.trim().toLowerCase();
 const root=$("#ct-cards");root.replaceChildren();
 let count=0;
 for(const n of data.nodes){
  if(tier!=="all"&&n.tier!==tier)continue;
  if(q&&!([n.label,n.owner,n.code,n.summary,n.kind,n.tier].join(" ").toLowerCase().includes(q)))continue;
  const b=make("button","ct-card");b.type="button";b.setAttribute("role","listitem");b.dataset.nodeId=n.id;b.setAttribute("aria-pressed",String(n.id===selected));
  b.append(make("span","ct-kind",data.node_tiers.find(t=>t.id===n.tier)?.label||n.tier),make("strong",null,n.label),make("small",null,n.summary.slice(0,145)),make("span","ct-chip",human(n.status)));
  b.onclick=()=>renderInspector(n.id);root.append(b);count++;
 }
 if(!count)root.append(make("p",null,"No matching controls. Clear the filter."));
}
function render(dataIn){
 data=dataIn;
 $("#ct-metadata").textContent=data.map_id+" · source commit "+(data.source_commit_sha||"UNKNOWN").slice(0,12)+" · machine derived / not domain authority";
 data.nodes.forEach(n=>nodeById.set(n.id,n));
 const f=$("#ct-filters");
 for(const item of [{id:"all",label:"All towers"},...data.node_tiers]){
  const b=make("button",null,item.label);b.type="button";b.setAttribute("aria-pressed",String(item.id===tier));b.onclick=()=>{tier=item.id;Array.from(f.children).forEach(x=>x.setAttribute("aria-pressed",String(x===b)));renderCards()};f.append(b);
 }
 $("#ct-search").addEventListener("input",renderCards);renderCards();renderInspector("a7");
 const relations=$("#ct-relations");
 for(const e of data.edges){
  const d=make("div","ct-edge");
  d.append(make("b",null,nodeById.get(e.source).label+" → "+nodeById.get(e.target).label),make("span",null,human(e.relation)));
  relations.append(d);
 }
 const plan=$("#ct-plan");
 for(const step of data.prioritized_roadmap){
  const a=make("article","ct-step");a.append(make("span",null,step.priority+" · "+human(step.status)),make("h3",null,step.title),make("p",null,step.done_when));plan.append(a);
 }
}
fetch("data/control-tower-map.json",{cache:"no-store"}).then(r=>{if(!r.ok)throw Error("HTTP "+r.status);return r.json()}).then(render).catch(e=>{$("#ct-metadata").textContent="Control projection unavailable; verify GitHub source.";$("#ct-cards").textContent=e.message});
})();