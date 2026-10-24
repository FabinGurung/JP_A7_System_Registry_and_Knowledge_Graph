/* Collection 05: always-visible, source-derived guidance. No private providers queried. */
(()=>{"use strict";
const get=id=>document.getElementById(id);
const el=(tag,txt,cls)=>{const n=document.createElement(tag);if(txt!==undefined)n.textContent=String(txt);if(cls)n.className=cls;return n;};
fetch("data/memory-storage-architecture.json",{cache:"no-store"}).then(r=>{if(!r.ok)throw Error("HTTP "+r.status);return r.json();}).then(d=>{
 if(d.collection_id!=="A7-MEM-STORAGE-ARCH-007"||d.kind!=="DERIVED_PUBLIC_OPERATING_REFERENCE"||!d.public_safe||d.formats?.length!==7||d.distinctions?.length!==3)throw Error("Unsupported source");
 const flow=get("storageArchFlow"),rows=get("storageArchRows");flow.replaceChildren();rows.replaceChildren();
 for(const item of d.distinctions){
  const card=el("article",undefined,"storage-arch-role");
  card.append(el("small",item.label),el("h3",item.name),el("p",item.meaning));flow.append(card);
 }
 for(const item of d.formats){
  const tr=el("tr");
  const format=el("th",item.format);format.scope="row";
  const role=el("td",item.responsibility),limit=el("td",item.qualification);
  tr.append(format,role,limit);rows.append(tr);
 }
 get("storageArchRule").textContent=d.rule;
 get("storageArchStatus").textContent="Collection 05 · source digest "+d.source_sha256.slice(0,12)+" · build "+d.site_build_commit.slice(0,12)+" · versioned guidance, not proof of deployed services";
}).catch(()=>{get("storageArchStatus").textContent="Derived curation unavailable. Read the canonical source at the link below.";});
})();
