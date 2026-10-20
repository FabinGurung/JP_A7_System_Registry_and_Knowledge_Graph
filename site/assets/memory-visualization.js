/* Memory Wall supplemental six-lane visualization reminders.
   Reads the SAME generated source as the preserved technical detail page. */
(() => {"use strict";
const root=document.getElementById("memory-viz-cards"),status=document.getElementById("memory-viz-source");
if(!root||!status)return;
const icons={CYTOSCAPE:"✳",REACT_FLOW:"⇢",TABLES:"▦",MERMAID:"◇",EXCALIDRAW:"✎",SPATIAL_3D:"⬡"};
const cues={CYTOSCAPE:"EXPLORE CONNECTIONS",REACT_FLOW:"TRACE THE SYSTEM",TABLES:"AUDIT THE FACTS",MERMAID:"DRAW FROM CODE",EXCALIDRAW:"ANNOTATE IDEAS",SPATIAL_3D:"SEE IT IN SPACE"};
const el=(tag,text,cls)=>{const n=document.createElement(tag);if(text!==undefined)n.textContent=String(text);if(cls)n.className=cls;return n};
function render(d){
 if(d.non_authoritative!==true||d.ordered_pipeline?.length!==6)throw Error("Unsupported visualization projection");
 root.replaceChildren();
 for(const lane of d.ordered_pipeline){
  const c=el("article",undefined,"memory-viz-card");
  const heading=el("div",undefined,"memory-viz-head");
  heading.append(el("span",icons[lane.id]||"✦","memory-viz-icon"),el("span",String(lane.order).padStart(2,"0")+" / "+lane.role,"memory-viz-category"));
  c.append(heading,el("h3",lane.technology),el("strong",cues[lane.id]||"VISUALIZE","memory-viz-cue"));
  c.append(el("p",lane.why),el("small","Recorded implementation: "+lane.implementation_state_at_record.replaceAll("_"," ")));
  root.append(c);
 }
 status.textContent="Six design roles · derived from "+d.source_path+" · statuses are recorded snapshots, not live installation claims.";
}
fetch("data/visualization-workspace.json",{cache:"no-store"}).then(r=>{if(!r.ok)throw Error("HTTP "+r.status);return r.json()}).then(render).catch(e=>{
 status.textContent="Projection unavailable: "+e.message+" — consult the preserved design decision.";
 const a=el("a","Read decision source ↗");a.href="https://github.com/FabinGurung/JP_A7_System_Registry_and_Knowledge_Graph/blob/main/registry/decisions/visualization-workspace.json";root.append(a);
});
})();
