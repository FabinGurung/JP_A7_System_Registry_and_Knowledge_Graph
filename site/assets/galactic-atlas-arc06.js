/* A7 Arc06 — source-driven keyboard-accessible world flight deck.
   It never writes owner data, runs engineering computations, or polls providers. */
"use strict";(()=>{
 const $=id=>document.getElementById(id), root="REPO-000001";
 const star=id=>Array.from(document.querySelectorAll(".star-node")).find(n=>n.dataset.repoId===id);
 const dom=(tag,value,cls)=>{const n=document.createElement(tag);if(value!==undefined)n.textContent=String(value);if(cls)n.className=cls;return n};
 let data=null,worlds=[],current=root,visits=[],initialConsumed=false;
 const valid=id=>worlds.some(s=>s.id===id);
 const station=id=>worlds.find(s=>s.id===id);
 const go=(id,focus=false)=>{
  if(!valid(id))return;
  let node=star(id);
  if(!node)return;
  if(node.hidden){const reset=$("sectorReset");if(reset)reset.click();node=star(id);}
  if(!node || node.hidden)return;
  node.click();
  if(focus)node.focus({preventScroll:true});
 };
 const detailCard=(s)=>{
  const article=dom("article",undefined,"arc06-compare-card");
  article.append(dom("span",s.sector+" · "+s.role.replaceAll("_"," "),"arc06-card-eyebrow"));
  article.append(dom("h3",s.title));
  article.append(dom("p",s.summary));
  const dl=dom("dl");
  for(const [term,val] of [["Domain owner",s.owns],["Observed snapshot",s.provider_evidence?.observed_date||"Unverified"],["Owner's verification gate",s.provider_evidence?.owner_gate||"Check original source"]]){
    const row=dom("div"),dt=dom("dt",term),dd=dom("dd",val);row.append(dt,dd);dl.append(row);
  }
  article.append(dl);
  const a=dom("a","Inspect original GitHub repository ↗");
  if(s.github_url.startsWith("https://github.com/FabinGurung/")){a.href=s.github_url;a.target="_blank";a.rel="noopener noreferrer";article.append(a);}
  return article;
 };
 function paint(){
  if(!data)return;
  const selected=station(current)||station(root);if(!selected)return;
  $("arc06World").value=selected.id;
  $("arc06Current").textContent=selected.title;
  $("arc06Sector").textContent=selected.sector;
  $("arc06Visited").textContent=visits.length+" worlds examined this visit";
  const button=$("arc06Share"),url=new URL(location.href);url.searchParams.set("world",selected.id);
  button.href=url.toString();
  $("arc06Source").textContent="Source-backed navigation · provider observations dated "+(selected.provider_evidence?.observed_date||"unknown")+" · not a live status feed";
  const last=$("arc06Journal");last.replaceChildren();
  for(const id of visits.slice(-6).reverse()){
    const s=station(id),item=dom("button",s.short+" · "+s.title);
    item.type="button";item.dataset.world=id;
    item.addEventListener("click",()=>go(id));last.append(item);
  }
  const compare=$("arc06CompareWorld");const match=station(compare.value);
  const target=$("arc06Comparison");target.replaceChildren();
  if(match&&match.id!==selected.id){
    target.append(detailCard(selected),detailCard(match));
    $("arc06CompareStatus").textContent="Two separately governed catalog entries. Comparison is descriptive; integration and approvals are not implied.";
  }else{
    target.append(dom("p","Choose another world to compare source-stated ownership and dated verification gates.","arc06-placeholder"));
    $("arc06CompareStatus").textContent="No comparison selected.";
  }
 }
 function picked(id){
  if(!data||!valid(id))return;
  current=id;
  if(!visits.includes(id))visits.push(id);
  // URL changes contain only a validated repo identity; leave the actual GitHub source unchanged.
  const u=new URL(location.href);u.searchParams.set("world",id);
  history.replaceState(null,"",u.pathname+u.search+u.hash);
  paint();
 }
 function cycle(step,focus){
  if(!data)return;
  const i=worlds.findIndex(s=>s.id===current);
  const next=worlds[(i+step+worlds.length)%worlds.length];
  if(next)go(next.id,focus);
 }
 window.addEventListener("a7:station-selected",event=>picked(event.detail?.id));
 $("arc06Go").addEventListener("click",()=>go($("arc06World").value,true));
 $("arc06Prev").addEventListener("click",()=>cycle(-1,true));
 $("arc06Next").addEventListener("click",()=>cycle(1,true));
 $("arc06CompareWorld").addEventListener("change",paint);
 $("arc06World").addEventListener("keydown",e=>{if(e.key==="Enter"){e.preventDefault();go(e.currentTarget.value,true);}});
 $("arc06FlightDeck").addEventListener("keydown",e=>{
  if(e.target.matches("input,select,textarea") || !["ArrowLeft","ArrowRight"].includes(e.key))return;
  e.preventDefault();cycle(e.key==="ArrowRight"?1:-1,true);
 });
 (async()=>{
  try{
    const res=await fetch("data/galactic-atlas.json",{cache:"no-store"});
    if(!res.ok)throw Error("Galaxy projection unavailable");
    const value=await res.json();
    if(value.non_authoritative!==true||value.station_count!==9||!Array.isArray(value.stations)||value.stations.length!==9||
      value.verified_runtime_handoff_count!==0)throw Error("Arc06 requires proven source projection");
    data=value;worlds=value.stations;const ids=new Set(worlds.map(s=>s.id));
    if(ids.size!==9||!ids.has(root)||worlds.some(s=>!s.github_url?.startsWith("https://github.com/FabinGurung/")))throw Error("Invalid source station IDs");
    for(const target of [$("arc06World"),$("arc06CompareWorld")]){
      for(const s of worlds){const opt=dom("option",s.short+" · "+s.title);opt.value=s.id;target.append(opt);}
    }
    const placeholder=document.createElement("option");placeholder.value="";placeholder.textContent="Choose second world…";
    $("arc06CompareWorld").prepend(placeholder);$("arc06CompareWorld").value="";
    $("arc06World").disabled=false;$("arc06CompareWorld").disabled=false;
    for(const id of ["arc06Go","arc06Prev","arc06Next"])$(id).disabled=false;
    const request=new URL(location.href).searchParams.get("world");
    const wanted=valid(request)?request:null;
    const apply=()=>{
      if(initialConsumed)return;
      if(document.querySelectorAll(".star-node").length!==9)return;
      initialConsumed=true;
      if(wanted)go(wanted);
      else picked(window.a7SelectedStationId||root);
    };
    apply();
    if(!initialConsumed){
      const observer=new MutationObserver(()=>{apply();if(initialConsumed)observer.disconnect();});
      observer.observe($("spaceField"),{childList:true,subtree:true});
    }
    paint();
  }catch(error){
    $("arc06Source").textContent="Flight deck unavailable: source projection could not be verified. Open the GitHub catalogue.";
    $("arc06CompareStatus").textContent="No verified source. No inference or fallback applied.";
  }
 })();
})();