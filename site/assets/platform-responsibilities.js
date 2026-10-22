/* Semantic, accessible platform responsibility matrix. Derived from A7 curation only. */
(()=>{"use strict";const $=id=>document.getElementById(id);
const node=(tag,txt,cls)=>{const x=document.createElement(tag);if(txt!==undefined)x.textContent=String(txt);if(cls)x.className=cls;return x};
fetch("data/platform-responsibilities.json",{cache:"no-store"}).then(r=>{if(!r.ok)throw Error("Source missing");return r.json()}).then(d=>{
 if(d.document_id!=="A7-MEM-PLATFORM-ROLES-005"||d.non_authoritative!==true||d.entries.length!==7)throw Error("Invalid curation");
 const body=$("platformRows");body.replaceChildren();
 for(const e of d.entries){const tr=node("tr");const sys=node("td"),type=node("small",e.kind);
  sys.append(node("strong",e.label),type);tr.append(sys,node("td",e.purpose),node("td",e.boundary));body.append(tr);}
 $("platformPrinciple").textContent=d.principle;$("platformExample").textContent=d.example;$("platformActionsNote").textContent=d.actions_hint;
 const chips=$("platformExamples");chips.replaceChildren();for(const v of d.suggested_workflows)chips.append(node("span",v));
 $("platformSource").textContent="A7 public presentation curation · source digest "+d.source_sha256.slice(0,12)+" · build "+d.site_build_commit.slice(0,12)+" · guidance, not proof of workflow implementation";
}).catch(()=>{$("platformSource").textContent="Could not load the curated matrix; check A7 GitHub source.";});
})();