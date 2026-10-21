/* Arc04: read-only evidence-gated interstellar route layer, independent of Arc03 station/filter engine. */
"use strict";
(() => {
  const get=id=>document.getElementById(id);
  const svg=get("arc04Lines"), list=get("arc04RouteList"), info=get("arc04Inspect");
  if(!svg || !list || !info)return;
  const ns="http://www.w3.org/2000/svg";
  let data=null, selected=window.a7SelectedStationId||"REPO-000001", chosen=null;
  const isSafe=(url)=>{try {const u=new URL(url);return u.protocol==="https:" && u.origin==="https://github.com" && u.pathname.startsWith("/FabinGurung/");}catch{return false;}};
  const station=id=>data?.stations.find(s=>s.id===id);
  const position=s=>{
    if(s.id==="REPO-000001")return {x:50,y:50};
    const a=s.azimuth*Math.PI/180,r=s.radial*.76;
    return {x:50+Math.cos(a)*r,y:50+Math.sin(a)*r};
  };
  function visible(id){
    const node=Array.from(document.querySelectorAll(".star-node")).find(n=>n.dataset.repoId===id);
    return node && !node.hidden;
  }
  function selectedRoutes(){
    if(!data)return [];
    const allowProposed=get("arc04IncludeProposals").checked;
    const type=get("arc04Type").value;
    const routes=data.routes.map(x=>({...x,proposed:false})).concat(
      allowProposed?data.candidate_routes.map(x=>({...x,proposed:true})):[]
    );
    return routes.filter(x=>(selected==="REPO-000001" || x.from===selected || x.to===selected)
      && (type==="ALL" || (type==="DOCUMENTED"&&!x.proposed) || (type==="PROPOSED"&&x.proposed)));
  }
  function detail(route){
    info.replaceChildren();
    const heading=document.createElement("h3");
    heading.textContent=station(route.from).title+" → "+station(route.to).title;
    info.append(heading);
    const add=content=>{const p=document.createElement("p");p.textContent=content;info.append(p);};
    add("Relation: "+route.relation_type+" · "+route.verification);
    add(route.proposed?route.purpose:route.limitation);
    add("Runtime handoff: NOT VERIFIED · Ownership transfer: NO");
    if(!route.proposed){
      add("A7 source ID: "+route.id+" · Evidence recorded: "+route.evidence_observed_at.slice(0,10));
      if(isSafe(route.evidence_url)){
        const a=document.createElement("a");a.href=route.evidence_url;
        a.target="_blank";a.rel="noopener noreferrer";a.textContent="Read exact canonical source record ↗";
        info.append(a);
      }
    } else add("Design idea only. Not admitted as a canonical graph edge, source release, or provider-confirmed interface.");
    const note=document.createElement("p");note.className="arc04-caveat";
    note.textContent="A7 projects metadata, not a live dependency monitor. Consult the owning repository to verify any actual exchange.";
    info.append(note);
  }
  function paint(){
    if(!data)return;
    const relevant=selectedRoutes();
    const active=relevant.filter(x=>visible(x.from)&&visible(x.to));
    svg.replaceChildren();
    const defs=document.createElementNS(ns,"defs");
    const marker=document.createElementNS(ns,"marker");
    marker.id="arc04Arrow";marker.setAttribute("markerWidth","6");marker.setAttribute("markerHeight","6");
    marker.setAttribute("refX","5");marker.setAttribute("refY","3");
    marker.setAttribute("orient","auto");marker.setAttribute("markerUnits","strokeWidth");
    const head=document.createElementNS(ns,"path");
    head.setAttribute("d","M0 0 L6 3 L0 6 Z");head.setAttribute("fill","#258bb2");
    marker.append(head);defs.append(marker);svg.append(defs);
    for(const route of active){
      const a=position(station(route.from)), b=position(station(route.to));
      const dx=b.x-a.x,dy=b.y-a.y,length=Math.hypot(dx,dy)||1;
      const bend=route.proposed?-3:3;
      const mx=(a.x+b.x)/2+(-dy/length)*bend, my=(a.y+b.y)/2+(dx/length)*bend;
      const path=document.createElementNS(ns,"path");
      path.setAttribute("d","M"+a.x+" "+a.y+" Q"+mx+" "+my+" "+b.x+" "+b.y);
      path.setAttribute("class","arc04-route-stroke"+(route.proposed?" is-proposed":"")+(route.id===chosen?" is-active":""));
      path.setAttribute("marker-end","url(#arc04Arrow)");
      svg.append(path);
    }
    list.replaceChildren();
    const count=get("arc04Count");
    count.textContent=active.filter(x=>!x.proposed).length+" documented navigation · "+
       active.filter(x=>x.proposed).length+" proposals shown · 0 verified runtime handoffs";
    if(!relevant.length){
      const p=document.createElement("p");p.className="arc04-empty";
      p.textContent="No admitted routes match this system and filter. This is not evidence that an integration exists.";
      list.append(p);
      info.replaceChildren();
      const note=document.createElement("p");
      note.textContent="Choose another station or enable optional proposals. A7 has no provider-verified runtime handoffs.";
      info.append(note);
      return;
    }
    if(!relevant.some(x=>x.id===chosen))chosen=relevant[0].id;
    for(const route of relevant){
      const btn=document.createElement("button");btn.type="button";
      btn.className="arc04-item"+(route.proposed?" is-proposed":"")+(route.id===chosen?" is-active":"");
      btn.setAttribute("aria-pressed",String(route.id===chosen));
      const title=document.createElement("strong");
      title.textContent=station(route.from).short+" → "+station(route.to).short;
      const status=document.createElement("span");status.className="arc04-status";
      status.textContent=route.proposed?"PROPOSED / UNVERIFIED":"DOCUMENTED / NAVIGATION ONLY";
      const summary=document.createElement("small");summary.textContent=route.proposed?route.purpose:route.relation_type+" · "+route.id;
      btn.append(title,status,summary);
      btn.addEventListener("click",()=>{chosen=route.id;paint();});
      list.append(btn);
    }
    detail(relevant.find(x=>x.id===chosen));
  }
  window.addEventListener("a7:station-selected",event=>{selected=event.detail.id;chosen=null;paint();});
  get("arc04IncludeProposals").addEventListener("change",()=>{chosen=null;paint();});
  get("arc04Type").addEventListener("change",()=>{chosen=null;paint();});
  const stage=get("spaceField");
  new MutationObserver(()=>paint()).observe(stage,{subtree:true,attributes:true,attributeFilter:["hidden"]});
  async function main(){
    try {
      const response=await fetch("data/galactic-atlas.json",{cache:"no-store"});
      if(!response.ok)throw Error("Arc04 projection HTTP "+response.status);
      data=await response.json();
      if(data.non_authoritative!==true || data.relationship_arc!=="GALACTIC_ATLAS_ARC_04_EVIDENCE_GATED_ROUTES" ||
         data.route_count!==4 || data.candidate_count!==4 || data.verified_runtime_handoff_count!==0 ||
         !Array.isArray(data.routes)||!Array.isArray(data.candidate_routes))throw Error("Arc04 schema failed");
      selected=window.a7SelectedStationId||selected;
      paint();
    } catch(e) {
      const p=document.createElement("p");p.className="arc04-empty";
      p.textContent="Evidence routes unavailable; check the GitHub source. No fallback claims will be fabricated.";
      list.replaceChildren(p);
      info.textContent="Projection validation not available.";
      get("arc04Count").textContent="Evidence unavailable";
      console.error("A7 route projection read failed",e);
    }
  }
  main();
})();
