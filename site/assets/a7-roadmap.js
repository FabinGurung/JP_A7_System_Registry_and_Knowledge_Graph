/* A7 L1 progress; source-built from registry, not manually copied markup. */
(()=>{"use strict";const repo="https://github.com/FabinGurung/JP_A7_System_Registry_and_Knowledge_Graph";
const $=id=>document.getElementById(id);
const el=(tag,s,cls)=>{const n=document.createElement(tag);if(s!==undefined)n.textContent=String(s);if(cls)n.className=cls;return n};
let rows=[];
function dateState(s){return /FINAL_CLOSED_PASS|DELIVERED|DEPLOYED_PROVIDER_VERIFIED/.test(s||"")?"done":"open"}
function paint(){const filter=$("roadmapSearch").value.toLowerCase().trim();
const box=$("roadmapDeveloped");box.replaceChildren();
let subset=rows.filter(x=>(x.title+" "+x.id+" "+x.stage+" "+x.detail).toLowerCase().includes(filter));
subset.reverse();
for(const x of subset){const a=el("article",undefined,"rp-item");
a.append(el("small",x.id+" · "+x.stage),el("h3",x.title));
const b=el("span",x.status,"rp-status");b.dataset.state=dateState(x.status);a.append(b,el("p",x.detail||"Source record contains no summary."));box.append(a)}
if(!subset.length)box.append(el("p","No milestones match your search."));
}
fetch("data/a7-roadmap.json",{cache:"no-store"}).then(r=>{if(!r.ok)throw Error("Not found");return r.json()}).then(d=>{
if(d.schema!=="a7-roadmap-projection.v0.1"||d.owner!=="A7_ONLY"||d.kind!=="DERIVED_NOT_AUTHORITATIVE"||!Array.isArray(d.developed)||!Array.isArray(d.next_a7))throw Error("Invalid data source");
rows=d.developed;
$("roadmapSequence").textContent=d.current_closed_sequence.replace("A7-SEQ-","");
$("roadmapMilestones").textContent=String(rows.length);
$("roadmapBacklogCount").textContent=String(d.next_a7.length);
$("roadmapSource").textContent="A7 registry projection • source "+d.source_sha256.slice(0,12)+" • build "+d.site_build_commit.slice(0,12)+" • dated snapshot; check GitHub for live runs";
$("roadmapSearch").addEventListener("input",paint);paint();
const box=$("roadmapUpcoming");box.replaceChildren();
for(const x of d.next_a7){const a=el("article",undefined,"rp-task");a.append(el("small",x.id+" · "+x.priority),el("h3",x.title),el("span",x.state,"rp-status"),el("p",x.done_when));box.append(a)}
}).catch(()=>{$("roadmapSource").textContent="Could not read this build's roadmap; consult A7's source registry on GitHub.";});
})();