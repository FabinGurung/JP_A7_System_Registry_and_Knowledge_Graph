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
if(d.schema!=="a7-roadmap-projection.v0.1"||d.owner!=="A7_ONLY"||d.kind!=="DERIVED_NOT_AUTHORITATIVE"||!Array.isArray(d.developed)||!Array.isArray(d.next_a7)||!Array.isArray(d.pinned_a7))throw Error("Invalid data source");
rows=d.developed;
$("roadmapSequence").textContent=d.current_closed_sequence.replace("A7-SEQ-","");
$("roadmapMilestones").textContent=String(rows.length);
$("roadmapBacklogCount").textContent=String(d.next_a7.length);
$("roadmapSource").textContent="A7 registry projection • source "+d.source_sha256.slice(0,12)+" • build "+d.site_build_commit.slice(0,12)+" • dated snapshot; check GitHub for live runs";
// Dated provider evidence from the owning A7 bootstrap, never a live-status claim.
const evidenceBox=$("roadmapEvidence");evidenceBox.replaceChildren();
const proof=d.verified_a7_provider_evidence;
if(proof&&proof.historical_not_live===true&&/^[0-9a-f]{40}$/.test(proof.verified_commit_sha)&&proof.conclusions&&Object.values(proof.conclusions).every(v=>v==="success")){
 evidenceBox.append(el("p",proof.sequence+" • verified historical main "+proof.verified_commit_sha.slice(0,12)+" • not live provider monitoring"));
 for(const [caption,key] of [["Registry validation","registry_run"],["Pages deployment","pages_run"],["Release safeguard","release_safeguard_run"]]){
  const run=proof[key];if(!Number.isSafeInteger(run)||run<1)continue;
  const a=el("a",caption+" · #"+run);a.href=repo+"/actions/runs/"+run;a.target="_blank";a.rel="noopener noreferrer";evidenceBox.append(a);
 }
 evidenceBox.append(el("small",proof.independent_http_body_readback?"Independent page HTTP readback recorded.":"Independent served-page HTTP readback NOT verified."));
}else evidenceBox.append(el("p","No verified A7 source-backed GitHub closeout snapshot is available; consult GitHub Actions."));
// Project only aggregate QA counts and public governance metadata; never render case payloads.
const govBox=$("roadmapGovernance");govBox.replaceChildren();
const gov=d.a7_governance;
if(gov&&gov.qa?.scope==="PUBLIC_A7_REGISTRY_ONLY"&&gov.external?.scope==="EXTERNAL_NON_GATE__DATED_NOT_LIVE"){
 const q=gov.qa,ext=gov.external;
 const qaCard=el("article",undefined,"rp-gov-card");
 qaCard.append(el("h3","Public A7 QA ledger"),el("strong",q.no_records_in_public_source?"No public cases recorded":q.active+" active / "+q.cases+" recorded","rp-gov-total"),
  el("p",q.no_records_in_public_source?"This public A7 source has no records. No claim is made about private or specialist QA.":"Latest recorded status per case, counted within this A7 file only."),
  el("small","Source "+q.source_path+" • SHA-256 "+q.source_sha256.slice(0,12)));
 const debtCard=el("article",undefined,"rp-gov-card");
 debtCard.append(el("h3","External dependencies"),el("strong",String(ext.count)+" recorded non-gates","rp-gov-total"),
  el("p","Assessment "+ext.assessment_date+" • historical A7 governance boundary, not live provider statuses."),
  el("small","Source "+ext.source_path+" • SHA-256 "+ext.source_sha256.slice(0,12)));
 const list=el("ul",undefined,"rp-gov-list");
 for(const x of ext.entries){
  const li=el("li");li.append(el("strong",x.id+" · "+x.status),el("span",x.why_not_closed),el("small","Condition: "+x.gate));list.append(li);
 }
 debtCard.append(list);govBox.append(qaCard,debtCard);
}else govBox.append(el("p","No validated public A7 governance projection. Check the canonical sources."));
$("roadmapSearch").addEventListener("input",paint);paint();
const pinnedBox=$("roadmapPinned");pinnedBox.replaceChildren();const pinnedIds=new Set();
for(const x of d.pinned_a7){
 if(pinnedIds.has(x.id)||!d.next_a7.some(t=>t.id===x.id))throw Error("Invalid pinned task reference");
 pinnedIds.add(x.id);const a=el("article",undefined,"rp-pin");
 a.append(el("small",x.id+" · "+x.priority),el("h3",x.title),el("span",x.task_boundary,"rp-pin-boundary"),el("p",x.pin_reason),el("small","Source state: "+x.state));pinnedBox.append(a);
}
const box=$("roadmapUpcoming");box.replaceChildren();
for(const x of d.next_a7.filter(x=>!pinnedIds.has(x.id))){const a=el("article",undefined,"rp-task");a.append(el("small",x.id+" · "+x.priority),el("h3",x.title),el("span",x.state,"rp-status"),el("p",x.done_when));box.append(a)}
}).catch(()=>{$("roadmapSource").textContent="Could not read this build's roadmap; consult A7's source registry on GitHub.";});
})();