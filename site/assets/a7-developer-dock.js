/* A7-only generated source locator. No network calls except local Pages JSON. */
(()=>{"use strict";const $=id=>document.getElementById(id);const host="https://github.com/FabinGurung/JP_A7_System_Registry_and_Knowledge_Graph/blob/";
const node=(tag,text,cls)=>{const e=document.createElement(tag);if(text!==undefined)e.textContent=text;if(cls)e.className=cls;return e};let groups=[];
function paint(){
 const query=$("dockSearch").value.toLowerCase().trim(),box=$("dockGroups");box.replaceChildren();let count=0;
 for(const g of groups){const items=g.items.filter(x=>(x.name+" "+x.path+" "+x.summary).toLowerCase().includes(query));if(!items.length)continue;
 const section=node("section",undefined,"dock-group");section.append(node("h3",g.name),node("p",g.description));
 const list=node("div",undefined,"dock-items");
 for(const item of items){const row=node("div",undefined,"dock-item"),a=node("a",item.name+" ↗");
  if(!item.source_url.startsWith(host))continue;
  a.href=item.source_url;a.target="_blank";a.rel="noopener noreferrer";
  row.append(a,node("small",item.summary),node("code",item.path));list.append(row);count++;}
 section.append(list);box.append(section);}
 if(!count)box.append(node("p","No checked-in A7 source files match this search."))}
fetch("data/a7-developer-dock.json",{cache:"no-store"}).then(r=>{if(!r.ok)throw Error("Fetch");return r.json()}).then(x=>{
 if(x.collection_id!=="A7-DEV-DOCK-001"||x.projection_kind!=="DERIVED_READ_ONLY_A7_SOURCE_DIRECTORY"||!Array.isArray(x.groups))throw Error("Invalid");
 groups=x.groups;$("dockSource").textContent="Checked into A7 · "+groups.length+" tool categories · source "+x.site_build_commit.slice(0,12)+" · links pinned to this commit";
 $("dockSearch").addEventListener("input",paint);paint();
}).catch(()=>{$("dockSource").textContent="Source directory unavailable. Open A7 GitHub for verified current files.";});
})();