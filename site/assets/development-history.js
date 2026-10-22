/* A7 L1 GitHub development readout. Static, owner-scoped, never a write or live polling client. */
(() => {"use strict";
const repo="https://github.com/FabinGurung/JP_A7_System_Registry_and_Knowledge_Graph";
const $=id=>document.getElementById(id);
let snapshot=null;
function node(tag,txt,cls){const el=document.createElement(tag);if(txt!==undefined)el.textContent=String(txt);if(cls)el.className=cls;return el}
function link(label,url){const a=node("a",label);if(typeof url==="string"&&url.startsWith(repo+"/")){a.href=url;a.target="_blank";a.rel="noopener noreferrer"}return a}
function date(v){if(!v)return"—";const d=new Date(v);return Number.isNaN(d.getTime())?"Unknown time":d.toLocaleString(undefined,{dateStyle:"medium",timeStyle:"short",timeZone:"UTC"})+" UTC"}
function empty(target,msg){target.replaceChildren(node("p",msg,"dh-empty"))}
function safeURL(u,kind){return typeof u==="string"&&u.startsWith(repo+"/"+kind+"/")}
function paint(){
 if(!snapshot)return;
 const search=$("dhSearch").value.trim().toLowerCase(),kind=$("dhKind").value;
 const prsBySha=new Map(snapshot.pull_requests.map(p=>[p.merge_sha,p]));
 const entries=snapshot.commits.filter(c=>(kind==="all"||kind===c.kind)&&(!search||(c.subject+" "+c.sha+" "+(c.sequence||"")).toLowerCase().includes(search)));
 const timeline=$("dhCommitList");timeline.replaceChildren();
 for(const c of entries){
  const li=node("li",undefined,"dh-entry"),body=node("div",undefined,"dh-entry-main");
  const head=node("div",undefined,"dh-entry-head");
  head.append(node("span",c.kind==="merge"?"Merged change":"Git commit","dh-kind"));
  if(c.sequence)head.append(node("span",c.sequence,"dh-seq"));
  const title=node("h3");title.append(link(c.subject,c.url));body.append(head,title);
  const foot=node("div",undefined,"dh-entry-meta");
  foot.append(node("time",date(c.committed_at)),node("code",c.sha.slice(0,10)));
  const pr=prsBySha.get(c.sha);
  if(pr&&safeURL(pr.url,"pull"))foot.append(link("PR #"+pr.number+" ↗",pr.url));
  body.append(foot);li.append(body);timeline.append(li);
 }
 if(!entries.length)empty(timeline,"No commits match these filters.");
 $("dhMatching").textContent=entries.length+" of "+snapshot.commits.length+" commits shown";
}
function showPRs(){
 const target=$("dhPrList");target.replaceChildren();
 if(!snapshot.pull_requests.length){empty(target,"PR evidence is not included in this offline test build. The published Pages build uses GitHub provider records.");return}
 for(const p of snapshot.pull_requests){
  if(!safeURL(p.url,"pull"))continue;
  const row=node("li",undefined,"dh-compact-row");
  const left=node("div");left.append(node("small","MERGED PR #"+p.number+" · "+date(p.merged_at)));
  const title=node("strong");title.append(link(p.title,p.url));left.append(title);
  row.append(left,link(p.merge_sha.slice(0,9)+" ↗",repo+"/commit/"+p.merge_sha));target.append(row);
 }
}
function showActions(){
 const target=$("dhActionList");target.replaceChildren();
 if(!snapshot.workflow_runs.length){empty(target,"Actions evidence is not included in this offline test build. See the source workflows on GitHub.");return}
 for(const run of snapshot.workflow_runs){
  if(!safeURL(run.url,"actions/runs"))continue;
  const row=node("li",undefined,"dh-compact-row");
  const left=node("div");left.append(node("small",date(run.created_at)+" · "+run.head_sha.slice(0,9)));
  const title=node("strong");title.append(link(run.name,run.url));left.append(title);
  const outcome=run.status==="completed"?(run.conclusion||"completed"):run.status;
  const status=node("span",outcome.replace(/_/g," "),"dh-run-outcome");
  status.dataset.state=outcome;row.append(left,status);target.append(row);
 }
}
function showTags(){
 const target=$("dhTagList");target.replaceChildren();
 for(const tag of snapshot.tags){
  if(!safeURL(tag.url,"releases/tag"))continue;
  const row=node("li",undefined,"dh-compact-row");
  row.append(link(tag.name,tag.url),node("small","Source commit "+tag.sha.slice(0,10)+" · "+date(tag.committed_at)));target.append(row);
 }
 if(!snapshot.tags.length)empty(target,"No source-confirmed Git tags in this checked-out history.");
}
async function start(){
 try{
  const res=await fetch("data/development-history.json",{cache:"no-store"});
  if(!res.ok)throw new Error("HTTP "+res.status);
  const data=await res.json();
  if(data.schema!=="a7-development-history.v0.1"||data.scope!=="THIS_A7_REPOSITORY_ONLY"||
    !Array.isArray(data.commits)||!Array.isArray(data.pull_requests)||!Array.isArray(data.workflow_runs)||
    data.repository!=="FabinGurung/JP_A7_System_Registry_and_Knowledge_Graph")throw new Error("Unexpected history dataset");
  snapshot=data;
  $("dhCommitCount").textContent=String(data.commits.length);
  $("dhPrCount").textContent=String(data.pull_requests.length);
  $("dhActionCount").textContent=String(data.workflow_runs.length);
  $("dhSource").textContent="Source "+data.source_sha.slice(0,12)+" · Built "+date(data.generated_at_utc);
  $("dhObserved").textContent="Dated GitHub Pages build snapshot, not live status. Counts show only the displayed sample.";
  $("dhSourceLink").href=repo+"/commit/"+data.source_sha;
  $("dhSourceLink").target="_blank";$("dhSourceLink").rel="noopener noreferrer";
  $("dhSearch").addEventListener("input",paint);$("dhKind").addEventListener("change",paint);
  paint();showPRs();showActions();showTags();
 }catch(error){
  $("dhObserved").textContent="History snapshot unavailable; authoritative records remain on GitHub.";
  for(const id of ["dhCommitList","dhPrList","dhActionList","dhTagList"])empty($(id),"Could not load this build's history. Open the linked GitHub repository to inspect its current history.");
  $("dhMatching").textContent="Not loaded";
 }
}
if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",start,{once:true});else start();
})();