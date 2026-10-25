/* A7 Memory Wall contents + Collection 06: read-only, public-safe sources. */
(()=>{"use strict";
const $=id=>document.getElementById(id);
const mk=(tag,value,cls)=>{const x=document.createElement(tag);if(value!==undefined)x.textContent=String(value);if(cls)x.className=cls;return x;};
const get=path=>fetch("data/"+path,{cache:"no-store"}).then(r=>{if(!r.ok)throw Error("HTTP "+r.status);return r.json();});
get("memory-wall-contents.json").then(data=>{
 if(data.manifest_id!=="A7-MEM-WALL-CONTENTS-001"||data.kind!=="NON_AUTHORITATIVE_PUBLIC_GUIDANCE"||data.collections?.length!==6||!data.public_safe)throw Error("Wrong contents manifest");
 const host=$("mwContentsList");host.replaceChildren();
 for(const c of data.collections){
  if(!/^[a-z][a-z0-9-]+$/.test(c.anchor)||!document.getElementById(c.anchor))throw Error("Broken local anchor "+c.anchor);
  const a=mk("a",undefined,"mw-toc-card mw-accent-"+c.accent);a.href="#"+c.anchor;
  const top=mk("span",undefined,"mw-toc-line");top.append(mk("b",String(c.number).padStart(2,"0"),"mw-toc-index"),mk("span",c.icon,"mw-toc-symbol"));
  a.append(top,mk("strong",c.title),mk("span",c.subtitle,"mw-toc-sub"),mk("small",c.detail),mk("span","Explore section ↗","mw-toc-cta"));host.append(a);
 }
 $("mwTocTotal").textContent=String(data.collections.length).padStart(2,"0");
 $("mwTocStatus").textContent="Six linked collections · canonical index sha256 "+data.source_sha256.slice(0,12)+" · build "+data.site_build_commit.slice(0,12);
}).catch(()=>{$("mwTocStatus").textContent="Using built-in section navigation; machine index unavailable.";});
let guide=null;
let query="",group="ALL";
function renderFormats(){
 const grid=$("mwFormatGrid");grid.replaceChildren();let shown=0;
 for(const f of guide.formats){
  if(group!=="ALL"&&f.group!==group)continue;
  if(!(f.label+" "+f.extension+" "+f.method+" "+f.group).toLowerCase().includes(query))continue;
  shown++;
  const card=mk("article",undefined,"mw-format-card");
  const header=mk("div",undefined,"mw-format-card-head");header.append(mk("small",f.group),mk("code",f.extension));
  card.append(header,mk("h4",f.label));
  for(const [label,value] of [["READER / METHOD",f.method],["STRUCTURED OUTPUT",f.output],["EXACT LOCATOR",f.locator],["DO NOT ASSUME",f.hold]]){
   const line=mk("div",undefined,"mw-format-detail");line.append(mk("strong",label),mk("p",value));card.append(line);
  }
  grid.append(card);
 }
 if(!shown)grid.append(mk("p","No matches. Clear search or switch family.","mw-no-match"));
 $("mwFormatCount").textContent=shown+" of "+guide.formats.length+" file families · documentation only, no files were accessed";
}
$("mwFormatSearch").addEventListener("input",e=>{query=e.target.value.toLowerCase().trim();if(guide)renderFormats();});
$("mwFormatGroup").addEventListener("change",e=>{group=e.target.value;if(guide)renderFormats();});
get("memory-extraction-retrieval.json").then(d=>{
 if(d.collection_id!=="A7-MEM-EXTRACTION-008"||d.kind!=="NON_AUTHORITATIVE_PUBLIC_GUIDANCE"||d.formats?.length!==17||d.pipeline?.length!==7||!d.public_safe)throw Error("Unsupported extraction contract");
 guide=d;
 const steps=$("mwExtractionPipeline");steps.replaceChildren();
 for(const s of d.pipeline){const li=mk("li");li.append(mk("span",s.step),mk("strong",s.title),mk("p",s.description));steps.append(li);}
 const groupSelect=$("mwFormatGroup");
 for(const label of d.groups){const option=mk("option",label);option.value=label;groupSelect.append(option);}
 const outputs=$("mwExtractionOutputs");outputs.replaceChildren();
 for(const o of d.outputs){const c=mk("article");c.append(mk("h4",o.format),mk("p",o.role));outputs.append(c);}
 const fields=$("mwEvidenceFields");fields.replaceChildren();
 for(const f of d.evidence_fields)fields.append(mk("code",f));
 const safety=$("mwExtractionSafeguards");safety.replaceChildren();
 for(const s of d.safeguards)safety.append(mk("li",s));
 $("mwEvidenceExample").textContent=JSON.stringify(d.synthetic_example,null,2);
 const refs=$("mwExtractionSources");refs.replaceChildren();
 for(const s of d.vendor_references){const a=mk("a",s.label+" ↗");a.href=s.url;a.target="_blank";a.rel="noopener noreferrer";refs.append(a);}
 $("mwExtractionStatus").textContent="Collection 06 · source digest "+d.source_sha256.slice(0,12)+" · "+d.status+" · no private ingestion";
 renderFormats();
}).catch(()=>{$("mwExtractionStatus").textContent="Extraction guidance unavailable. See the canonical source link above.";});
})();
