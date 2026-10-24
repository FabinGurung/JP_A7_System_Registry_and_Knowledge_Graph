/* Collection 04: public-safe vocabulary generated from a versioned A7 curation. */
(()=>{"use strict";
const $=id=>document.getElementById(id);
const node=(tag,txt,cls)=>{const n=document.createElement(tag);if(txt!==undefined)n.textContent=String(txt);if(cls)n.className=cls;return n};
let data=null,category="ALL",showIds=false;
const registerText=()=>data.example.register.map(row=>(showIds?row.id+" · ":"")+row.name+" — "+row.detail).join("\n");
function register(){
 const host=$("uiVocabRegister");host.replaceChildren();
 for(const r of data.example.register){
  const row=node("div",undefined,"ui-vocab-row"),label=node("span",r.name),id=node("code",showIds?r.id:"");
  row.append(label,id);host.append(row);
 }
 const btn=$("uiVocabToggle");btn.textContent=showIds?"Hide IDs":"Show IDs";btn.setAttribute("aria-pressed",String(showIds));
}
function renderTerms(){
 const host=$("uiVocabTerms"),q=$("uiVocabSearch").value.toLowerCase().trim();host.replaceChildren();
 let count=0;
 for(const term of data.terms){
  if(category!=="ALL"&&term.category!==category)continue;
  if(!(term.title+" "+term.description+" "+term.prompt).toLowerCase().includes(q))continue;
  const card=node("article",undefined,"ui-vocab-term");
  card.append(node("small",term.category.replace("WORKFLOW","AUDIT / QA")),
              node("h4",term.title),node("p",term.description),node("blockquote",term.prompt));
  host.append(card);count++;
 }
 if(!count)host.append(node("p","No matching terms; clear the search or category."));
}
function setup(){
 $("uiVocabTree").textContent=data.example.tree;
 $("uiVocabToggle").addEventListener("click",()=>{showIds=!showIds;register();});
 $("uiVocabCopy").addEventListener("click",async()=>{
  const result=$("uiVocabCopyStatus");
  if(!navigator.clipboard?.writeText){result.textContent="Clipboard unavailable here; select the example text instead.";return;}
  try{await navigator.clipboard.writeText(registerText());result.textContent="Copied illustrative register.";}
  catch{result.textContent="Copy was blocked; select the displayed rows instead.";}
 });
 const filters=$("uiVocabFilters");
 for(const c of data.categories){const b=node("button",c.label);b.type="button";b.dataset.category=c.id;b.setAttribute("aria-pressed","false");filters.append(b);}
 filters.addEventListener("click",e=>{
  const b=e.target.closest("button[data-category]");if(!b)return;
  category=b.dataset.category;
  for(const x of filters.querySelectorAll("button")){const active=x===b;x.classList.toggle("is-active",active);x.setAttribute("aria-pressed",String(active));}
  renderTerms();
 });
 $("uiVocabSearch").addEventListener("input",renderTerms);
 $("uiVocabStatus").textContent="Source-derived A7 vocabulary · 13 terms · synthetic examples · SHA256 "+data.source_sha256.slice(0,12)+" · built "+String(data.site_build_commit).slice(0,12);
 register();renderTerms();
}
fetch("data/memory-ui-vocabulary.json",{cache:"no-store"}).then(r=>{if(!r.ok)throw Error("source missing");return r.json()}).then(d=>{
 if(d.collection_id!=="A7-MEM-UI-VOCAB-006"||d.kind!=="DERIVED_READ_ONLY_GLOSSARY"||d.terms.length!==13||d.example.kind!=="DEMONSTRATION_ONLY")throw Error("invalid source");
 data=d;setup();
}).catch(()=>{$("uiVocabStatus").textContent="This vocabulary cannot be verified in this build. Check the canonical A7 curation.";});
})();