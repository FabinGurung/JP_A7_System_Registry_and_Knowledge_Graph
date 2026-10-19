(() => {"use strict";
const $=x=>document.querySelector(x); let rows=[];
function el(tag,text,cls){const x=document.createElement(tag);x.textContent=String(text??"");if(cls)x.className=cls;return x}
function render(){
 const q=$("#health-filter").value.toLowerCase().trim();const holder=$("#health-cards");holder.replaceChildren();
 for(const r of rows){if(q&&!(r.name+" "+r.slug+" "+r.health+" "+r.attention).toLowerCase().includes(q))continue;
 const card=el("article",null,"health-card");const warning=r.health.includes("FAILED");const older=r.health.includes("OLDER");
 card.append(el("span",warning?"OWNER ACTION NEEDED":older?"OLDER VERIFIED PUBLISH":"LAST OBSERVED SUCCESS","health-chip"+(warning?" issue":older?" older":"")));
 card.append(el("h2",r.name),el("p",r.attention),el("small","Production source: "+r.production_branch),el("div","Observed main SHA: "+r.main_sha.slice(0,12),"health-code"));
 const links=el("div",null,"health-links");
 for(const [title,url] of [["Owning GitHub","https://github.com/FabinGurung/"+r.slug],["Published site","https://fabingurung.github.io/"+r.slug+"/"],["Actions evidence","https://github.com/FabinGurung/"+r.slug+"/actions/runs/"+r.deployment_run]]){
 const a=el("a",title+" ↗");a.href=url;a.target="_blank";a.rel="noopener noreferrer";links.append(a)
 }card.append(links);holder.append(card);
 }
 if(!holder.children.length)holder.append(el("p","No matching recorded systems."))
}
fetch("data/repository-health.json",{cache:"no-store"}).then(r=>{if(!r.ok)throw Error("HTTP "+r.status);return r.json()}).then(data=>{
 if(data.schema_version!=="1.0.0"||data.non_authoritative!==true||data.records.length!==9)throw Error("Unvalidated projection");
 rows=data.records;$("#health-meta").textContent="PROVIDER OBSERVATION · "+data.snapshot_date+" · 9 repository records · historical snapshot only · build "+data.site_build_commit_sha.slice(0,12);
 $("#health-filter").addEventListener("input",render);render()
}).catch(e=>{$("#health-meta").textContent="Snapshot unavailable: "+e.message+" — verify GitHub directly."});
})();