/* Arc05: public read-only release constellation, sourced by JSONL events and dated owner observations. */
"use strict";
(()=>{
 const $=id=>document.getElementById(id);
 const list=$("arc05HistoryList"),inspector=$("arc05HistoryInspector"),count=$("arc05HistoryCount");
 if(!list||!inspector||!count)return;
 let data=null,selected=window.a7SelectedStationId||"REPO-000001",active=null;
 const safeUrl=url=>{if(!url)return false;try{const x=new URL(url);return x.protocol==="https:"&&x.origin==="https://github.com"&&x.pathname.startsWith("/FabinGurung/");}catch{return false;}};
 const link=(title,url)=>{if(!safeUrl(url))return;const a=document.createElement("a");a.textContent=title+" ↗";a.href=url;a.target="_blank";a.rel="noopener noreferrer";inspector.append(a);};
 function inspect(record){
   inspector.replaceChildren();
   const h=document.createElement("h3");h.textContent=record.title;inspector.append(h);
   const note=(message)=>{const p=document.createElement("p");p.textContent=message;inspector.append(p);};
   note(record.kind.replaceAll("_"," ")+" · "+record.date);
   note("Immutable source commit "+record.commit_sha+" · This is historical provider evidence, not a live version monitor.");
   note(record.limitation);
   link("View commit",record.commit_url);
   link("Published release tag",record.release_url);
   link("Registry CI evidence",record.run_ci_url);
   link("Pages workflow evidence",record.run_pages_url);
   if(record.evidence_url!==record.release_url)link("Source provenance",record.evidence_url);
   if(record.artifact_sha256)note("Recorded Pages artifact SHA-256: "+record.artifact_sha256);
   note("Drive/private A9 artifacts and scientific sign-offs are never reconstructed from a public release marker.");
 }
 function paint(){
   if(!data)return;
   const repo=data.stations.find(x=>x.id===selected);
   const items=selected==="REPO-000001"?data.history:data.peer_publications.filter(x=>x.station_id===selected);
   const name=repo?repo.title:"Unknown system";
   $("arc05SelectedSystem").textContent=name;
   count.textContent=items.length+" source-linked history record"+(items.length===1?"":"s");
   list.replaceChildren();
   if(!items.length){
     inspector.replaceChildren();const p=document.createElement("p");
     p.textContent="No dated publication evidence for this system in this pinned A7 view.";
     inspector.append(p);return;
   }
   if(!items.some(x=>x.id===active))active=items.at(-1).id;
   for(const item of items){
     const b=document.createElement("button");b.type="button";
     b.className="arc05-history-item"+(item.id===active?" is-active":"");
     b.setAttribute("aria-pressed",String(item.id===active));
     const stamp=document.createElement("span");stamp.className="arc05-date";stamp.textContent=item.date;
     const name=document.createElement("strong");name.textContent=item.title;
     const meta=document.createElement("small");
     meta.textContent=item.kind.replaceAll("_"," ")+" · "+item.commit_sha.slice(0,12);
     b.append(stamp,name,meta);
     b.addEventListener("click",()=>{active=item.id;paint();});
     list.append(b);
   }
   inspect(items.find(x=>x.id===active));
 }
 window.addEventListener("a7:station-selected",event=>{selected=event.detail.id;active=null;paint();});
 (async()=>{
   try{
     const response=await fetch("data/galactic-atlas.json",{cache:"no-store"});
     if(!response.ok)throw Error("Arc05 history projection unavailable");
     data=await response.json();
     if(data.non_authoritative!==true ||
       data.history_arc!=="GALACTIC_ATLAS_ARC_05_IMMUTABLE_RELEASE_HISTORY" ||
       data.history_event_count!==6 || data.peer_publication_count!==8 ||
       !Array.isArray(data.history)||!Array.isArray(data.peer_publications))
       throw Error("Arc05 history contract mismatch");
     selected=window.a7SelectedStationId||selected;paint();
   }catch(error){
     list.textContent="Release evidence unavailable. No guessed history displayed.";
     count.textContent="Evidence unavailable";
     console.error("A7 history projection read failed",error);
   }
 })();
})();

