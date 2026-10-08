(() => {
 "use strict";
 const $ = s => document.querySelector(s);
 const base = "https://github.com/FabinGurung/JP_A7_System_Registry_and_Knowledge_Graph/blob/main/";
 const label = s => s.replaceAll("_"," ");
 const el = (tag,className,text) => { const n=document.createElement(tag); if(className)n.className=className;if(text!=null)n.textContent=text;return n; };
 const art={
   CYTOSCAPE:"●──●──●\n  ╲│╱\n   ●",
   REACT_FLOW:"[PROJECT] → [PROFILE]\n              ↓\n          [MODULE]",
   TABLES:"Project | OPS | CAD\nPRJ-001 |  ✓  |  ✓\nPRJ-002 |  ✓  |  ✓",
   MERMAID:"flowchart LR\nA[Project] --> B[Module]",
   EXCALIDRAW:"┌── Human markup ──┐\n│ A7  →  Notes     │\n└──────────────────┘",
   SPATIAL_3D:"    •      ◦\n  ◦  ╱ ╲  •\n    •      ◦"
 };
 const statusClass=s=>s==="IMPLEMENTED"||s==="IMPLEMENTED_LIGHTWEIGHT"?"ws-live":s.startsWith("GENERATED")?"ws-export":"ws-planned";
 function render(data){
   $("#ws-statusline").textContent=data.decision_id+" · "+data.decision_state+" · recorded "+data.recorded_on+" · source commit "+(data.source_commit_sha||"not supplied").slice(0,12);
   const root=$("#ws-lanes");root.replaceChildren();
   for(const lane of data.ordered_pipeline){
     const card=el("article","ws-lane");
     const head=el("div","ws-lane-head");
     head.append(el("span","ws-index",String(lane.order).padStart(2,"0")),el("div",null));
     head.lastChild.append(el("h3",null,lane.technology),el("p",null,lane.role));
     card.append(head,el("span","ws-state "+statusClass(lane.implementation_state_at_record),label(lane.implementation_state_at_record)));
     card.append(el("pre","ws-art",art[lane.id]||"● → ●"));
     card.append(el("p","ws-why",lane.why));
     const now=el("div","ws-now");now.append(el("b",null,"ACTUAL IMPLEMENTATION AT DECISION"),el("p",null,lane.observed_implementation));
     const gate=el("div","ws-gate");gate.append(el("b",null,"UPGRADE / PRESERVATION RULE"),el("p",null,lane.upgrade_gate));
     card.append(now,gate);root.append(card);
   }
   const ol=$("#ws-readfirst");
   ol.replaceChildren(...data.read_first.map(s=>el("li",null,s)));
   const evidence=$("#ws-evidence-links");
   const refs=[
     ["Decision record","registry/decisions/visualization-workspace.json"],
     ["Read-first human runbook","docs/VISUALIZATION_WORKSPACE_READ_FIRST.md"],
     ["Actual graph/site JavaScript","site/assets/app.js"],
     ["Derivation generator","scripts/generate_visualizations.py"],
     ["Project routing","registry/routing/project-module-bindings.json"],
     ["Authority map","registry/authority/authority-map.json"],
     ["CI checks",".github/workflows/validate-registry.yml"],
     ["Pages deploy",".github/workflows/deploy-a7-pages.yml"],
     ["Append-only events","registry/events/a7-mutations.jsonl"]
   ];
   for(const [name,path] of refs){
     const a=el("a","ws-evidence-link");a.href=base+path;a.target="_blank";a.rel="noreferrer";
     a.append(el("strong",null,name),el("span",null,path),el("b",null,"↗")); evidence.append(a);
   }
 }
 fetch("data/visualization-workspace.json",{cache:"no-store"})
  .then(r=>{if(!r.ok)throw Error("HTTP "+r.status);return r.json()})
  .then(render)
  .catch(e=>{ $("#ws-statusline").textContent="Decision projection unavailable; verify GitHub source directly.";$("#ws-lanes").textContent="Unable to load versioned decision: "+e.message; });
})();