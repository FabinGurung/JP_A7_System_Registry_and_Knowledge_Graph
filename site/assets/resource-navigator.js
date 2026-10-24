/* Arc07 L1 source-derived, public-only resource navigator; never executes owner operations. */
(()=>{"use strict";
const $=id=>document.getElementById(id);
const make=(tag,text,cls)=>{const n=document.createElement(tag);if(text!==undefined)n.textContent=String(text);if(cls)n.className=cls;return n;};
let data=null,orgId=null,projectId=null,categoryId=null;
const match=(s,q)=>String(s||"").toLowerCase().includes(q);
const selected=(arr,id)=>arr.find(x=>x.id===id)||arr[0];
function button(title,detail,id,current,choose){
 const b=make("button",undefined,"rn-choice"+(current?" is-selected":""));b.type="button";b.dataset.id=id;b.setAttribute("aria-pressed",String(current));
 b.append(make("strong",title),make("small",detail));b.addEventListener("click",choose);return b;
}
function paint(){
 if(!data)return;
 const orgs=data.organizations,org=selected(orgs,orgId);
 const projects=org.projects,proj=selected(projects,projectId);
 const categories=proj.categories,cat=selected(categories,categoryId);
 orgId=org.id;projectId=proj.id;categoryId=cat.id;
 const sections=[["rnOrganizations",orgs,orgId,x=>{orgId=x.id;projectId=null;categoryId=null;paint();}],
  ["rnProjects",projects,projectId,x=>{projectId=x.id;categoryId=null;paint();}],
  ["rnCategories",categories,categoryId,x=>{categoryId=x.id;paint();}]];
 for(const [id,items,active,choose] of sections){
  const parent=$(id);parent.replaceChildren();
  for(const x of items)parent.append(button(x.name,x.description||x.owner||"Public A7 grouping",x.id,x.id===active,()=>choose(x)));
 }
 const q=$("rnSearch").value.trim().toLowerCase(),all=cat.resources;
 const rows=all.filter(x=>!q||[x.name,x.note,x.kind,x.id].some(z=>match(z,q)));
 const container=$("rnResources");container.replaceChildren();
 for(const r of rows){
  const card=make("article",undefined,"rn-resource");
  const heading=make("div",undefined,"rn-resource-heading");
  heading.append(make("span",r.kind,"rn-kind"),make("span",r.id,"rn-id"));
  const link=make("a",r.name+" ↗");link.href=r.href;
  if(r.href.startsWith("https://")){link.target="_blank";link.rel="noopener noreferrer";}
  card.append(heading,link,make("p",r.note),make("small","Public source reference · "+r.source_path));
  container.append(card);
 }
 if(!rows.length)container.append(make("p","No matching resources in this category. Try another category or reset your search.","rn-empty"));
 $("rnBreadcrumb").textContent=[org.name,proj.name,cat.name].join(" / ");
 $("rnStatus").textContent=rows.length+" of "+all.length+" resources in this category · checked-in source "+data.source_sha256.slice(0,12)+" · build "+data.site_build_commit.slice(0,12)+" · snapshot "+data.source_observed_date+" (not live status)";
}
$("rnSearch").addEventListener("input",paint);
$("rnReset").addEventListener("click",()=>{$("rnSearch").value="";orgId=projectId=categoryId=null;paint();});
fetch("data/resource-navigator.json",{cache:"no-store"}).then(r=>{if(!r.ok)throw Error("HTTP "+r.status);return r.json();}).then(d=>{
 if(d.collection_id!=="A7-RN-001"||d.kind!=="DERIVED_PUBLIC_REFERENCE_NAVIGATION"||d.public_safe!==true||!Array.isArray(d.organizations)||!d.organizations.length)throw Error("unsupported manifest");
 data=d;paint();
}).catch(e=>{$("rnStatus").textContent="Public manifest unavailable ("+e.message+"). The canonical link below remains available.";for(const id of ["rnOrganizations","rnProjects","rnCategories","rnResources"])$(id).replaceChildren(make("p","See the manifest source below."));});
})();
