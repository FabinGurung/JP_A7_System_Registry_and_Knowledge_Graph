/* Source-governed Memory Wall collection 03. No external API reads or file permission bypass. */
(()=>{"use strict";
const $=id=>document.getElementById(id);
const node=(tag,txt,cls)=>{const x=document.createElement(tag);if(txt!==undefined)x.textContent=String(txt);if(cls)x.className=cls;return x};
const fill=(id,obj)=>{const host=$(id);host.replaceChildren();for(const x of obj)host.append(node("span",x))};
fetch("data/platform-responsibilities.json",{cache:"no-store"}).then(r=>{if(!r.ok)throw Error("Source unavailable");return r.json()}).then(d=>{
 if(d.document_id!=="A7-MEM-PLATFORM-ROLES-005"||d.non_authoritative!==true||d.entries.length!==8||
 !d.architecture_poster||d.architecture_poster.id!==d.document_id||!d.architecture_poster.motto)throw Error("Invalid source");
 const p=d.architecture_poster;
 const body=$("platformRows");body.replaceChildren();
 for(const e of d.entries){const tr=node("tr");const sys=node("td"),type=node("small",e.kind);
  sys.append(node("strong",e.label),type);tr.append(sys,node("td",e.purpose),node("td",e.boundary));body.append(tr);}
 const compose=(id,v)=>{const el=$(id);el.querySelector("strong").textContent=v.label;el.querySelector("p").textContent=v.description};
 compose("platformCommand",p.input);compose("platformAI",p.commander);
 compose("platformActions",p.execution);compose("platformPages",p.output);
 const pair=$("platformSourcePair");pair.replaceChildren();
 for(const s of p.sources){const card=node("article");card.append(node("small",s.role.replaceAll("_"," ")),node("strong",s.label),node("p",s.caption));pair.append(card);}
 fill("platformOutputStrip",p.outputs);$("platformMotto").textContent=p.motto;
 $("platformAuthority").textContent=p.authority_disclaimer;
 $("platformPrivacy").textContent=p.privacy_disclaimer;
 $("platformAutomation").textContent=p.automation_disclaimer;
 $("platformProof").textContent=p.proof_disclaimer;
 const list=$("platformProvenanceFields");list.replaceChildren();
 for(const s of p.provenance_fields)list.append(node("li",s));
 fill("platformClaimLabels",p.claim_labels);
 $("platformPrinciple").textContent=d.principle;
 $("platformExample").textContent=d.example;
 $("platformActionsNote").textContent=d.actions_hint;
 fill("platformExamples",d.suggested_workflows);
 $("platformSource").textContent="A7 versioned curation · digest "+d.source_sha256.slice(0,12)+" · Pages build "+d.site_build_commit.slice(0,12)+" · guidance only, no automated Drive integration asserted";
}).catch(()=>{
 $("platformSource").textContent="Curated guide unavailable. Verify the versioned A7 source on GitHub.";
});
})();