(() => {
  "use strict";

  const DATA = {};
  // Presentation palette only: do not mutate generated graph JSON/canonical node IDs.
  // Darker, distinguishable node colors stay legible on the light graph canvases.
  const NODE_PALETTE = Object.freeze({
    system:"#275674",
    execution_profile:"#7476bb",
    module:"#217ca3",
    repository:"#4c82b3",
    fact_class:"#ab782d",
    project:"#258d75",
    research_project:"#ab6a92"
  });

  const TYPE_LABELS = {
    system: "Systems",
    execution_profile: "Execution profiles",
    module: "Modules",
    repository: "Repositories",
    fact_class: "Fact classes",
    project: "Project IDs",
    research_project: "Research projects"
  };

  const $ = (s, root=document) => root.querySelector(s);
  const $$ = (s, root=document) => Array.from(root.querySelectorAll(s));
  const escapeText = (v) => String(v == null ? "" : v);

  async function fetchJson(path) {
    const response = await fetch(path, {cache:"no-store"});
    if (!response.ok) throw new Error(path + " → HTTP " + response.status);
    return response.json();
  }

  async function load() {
    const [summary, graph, search, matrix, authority, manifest, mermaid] = await Promise.all([
      fetchJson("data/a7-summary.json"),
      fetchJson("data/a7-graph.json"),
      fetchJson("data/a7-search-index.json"),
      fetchJson("data/project-module-matrix.json"),
      fetchJson("data/authority-projection.json"),
      fetchJson("data/derivation-manifest.json"),
      fetch("data/a7-architecture.mmd", {cache:"no-store"}).then(r => r.text())
    ]);
    Object.assign(DATA, {summary, graph, search, matrix, authority, manifest, mermaid});
    renderAll();
  }

  function renderAll() {
    $("#sequenceStatus").textContent = DATA.summary.source_sequence + " · " + DATA.summary.source_sequence_status;
    $("#footerBuild").textContent = shortSha(DATA.summary.source_commit_sha);
    renderMetrics();
    renderArchitecture();
    renderModules();
    setupTabs();
    setupSearch();
    setupGraph2d();
    setupGraph3d();
    renderRouting();
    renderAuthority();
    renderDerivation();
  }

  function shortSha(value) {
    if (!value || value === "UNKNOWN") return "commit unknown";
    return value.slice(0, 12);
  }

  function metric(label, value) {
    const div = document.createElement("div");
    div.className = "metric";
    const strong = document.createElement("strong");
    strong.textContent = value;
    const span = document.createElement("span");
    span.textContent = label;
    div.append(strong, span);
    return div;
  }

  function renderMetrics() {
    const m = DATA.summary;
    const root = $("#metrics");
    [
      ["Systems", m.systems],
      ["Repositories", m.repositories],
      ["Modules", m.modules],
      ["Project IDs", m.project_identities],
      ["Research projects", m.research_projects],
      ["Fact classes", m.fact_classes],
      ["Routes", m.routes],
      ["Graph edges", m.graph_edges]
    ].forEach(x => root.appendChild(metric(x[0], x[1])));
  }

  function nodeById(id) {
    return DATA.graph.nodes.find(n => n.id === id);
  }

  function renderArchitecture() {
    const root = $("#architecture");
    root.innerHTML = "";
    const left = document.createElement("div");
    const middle = document.createElement("div");
    const right = document.createElement("div");
    middle.className = "arch-stack";
    right.className = "arch-stack";

    const control = document.createElement("div");
    control.className = "arch-node control";
    control.innerHTML = "<strong>A7 Semantic Control Plane</strong><small>identity · authority · routing · lineage</small>";
    const profile = document.createElement("div");
    profile.className = "arch-node profile";
    profile.innerHTML = "<strong>EXEC-PROFILE-AEC-CORE-001</strong><small>28 project semantic IDs resolve here</small>";
    left.append(control, profile);

    DATA.matrix.route_columns.forEach(route => {
      const module = document.createElement("div");
      module.className = "arch-node module";
      module.innerHTML = "<strong>" + escapeText(route.module_label) + "</strong><small>" + escapeText(route.fact_class) + "</small>";
      middle.appendChild(module);
      const repo = document.createElement("div");
      repo.className = "arch-node repo";
      repo.innerHTML = "<strong>" + escapeText(route.repository_id) + "</strong><small>" + escapeText(route.working_ref) + "</small>";
      right.appendChild(repo);
    });
    root.append(left, middle, right);
  }

  function renderModules() {
    const root = $("#moduleGrid");
    const modules = DATA.graph.nodes.filter(n => n.type === "module");
    modules.forEach(m => {
      const card = document.createElement("article");
      card.className = "module-card" + (m.group === "JP_KNOWLEDGE_MODULES" ? " knowledge" : "");
      const dot = document.createElement("div"); dot.className = "module-dot";
      const h = document.createElement("h3"); h.textContent = m.label;
      const p = document.createElement("p"); p.textContent = m.role || m.status || "Peer module";
      card.append(dot,h,p);
      if (m.site_url) {
        const a = document.createElement("a"); a.href=m.site_url; a.target="_blank"; a.rel="noreferrer"; a.textContent="Open module site ↗"; card.appendChild(a);
      }
      root.appendChild(card);
    });
  }

  function setupTabs() {
    $$(".tab").forEach(tab => tab.addEventListener("click", () => activateView(tab.dataset.view)));
    $$("[data-go]").forEach(btn => btn.addEventListener("click", () => activateView(btn.dataset.go)));
  }

  function activateView(name) {
    $$(".tab").forEach(t => t.classList.toggle("active", t.dataset.view === name));
    $$(".view").forEach(v => v.classList.toggle("active", v.id === "view-" + name));
    if (name === "graph" && DATA.graph2d) DATA.graph2d.resize(true);
    if (name === "spatial" && DATA.graph3d) DATA.graph3d.resize();
    window.scrollTo({top: $(".tabs").offsetTop - 74, behavior:"smooth"});
  }

  function setupSearch() {
    const overlay=$("#searchOverlay"), input=$("#globalSearch"), root=$("#searchResults");
    let selected=0;
    const open=()=>{overlay.classList.add("open");overlay.setAttribute("aria-hidden","false");input.focus();input.select();renderResults("");};
    const close=()=>{overlay.classList.remove("open");overlay.setAttribute("aria-hidden","true");};
    $("#searchButton").addEventListener("click",open);
    document.addEventListener("keydown",e=>{
      if(e.key==="/" && !/INPUT|TEXTAREA|SELECT/.test(document.activeElement.tagName)){e.preventDefault();open();}
      if(e.key==="Escape") close();
      if(overlay.classList.contains("open") && e.key==="ArrowDown"){selected++;renderResults(input.value);}
      if(overlay.classList.contains("open") && e.key==="ArrowUp"){selected=Math.max(0,selected-1);renderResults(input.value);}
      if(overlay.classList.contains("open") && e.key==="Enter"){const rows=$$(".search-result",root);if(rows.length) rows[Math.min(selected,rows.length-1)].click();}
    });
    overlay.addEventListener("click",e=>{if(e.target===overlay)close();});
    input.addEventListener("input",()=>{selected=0;renderResults(input.value);});

    function renderResults(query) {
      const q=query.trim().toLowerCase();
      let rows=DATA.search.items.filter(item=>!q || item.tokens.includes(q)).slice(0,24);
      selected=Math.min(selected,Math.max(rows.length-1,0));
      root.innerHTML="";
      rows.forEach((item,i)=>{
        const div=document.createElement("div");div.className="search-result"+(i===selected?" active":"");
        const left=document.createElement("div");
        const strong=document.createElement("strong");strong.textContent=item.label;
        const small=document.createElement("small");small.textContent=item.id+(item.subtitle?" · "+item.subtitle:"");
        left.append(strong,small);
        const type=document.createElement("span");type.className="result-type";type.textContent=item.type.replace("_"," ");
        div.append(left,type);
        div.addEventListener("click",()=>{
          close();
          if(item.type==="project"){activateView("routing");$("#projectSelect").value=item.id;$("#projectSelect").dispatchEvent(new Event("change"));}
          else {activateView("graph");DATA.graph2d.select(item.id);}
        });
        root.appendChild(div);
      });
      if(!rows.length){root.innerHTML='<div class="search-result"><div><strong>No match</strong><small>Try an A7 ID, module role or fact class.</small></div></div>';}
    }
  }

  function setupGraph2d() {
    const canvas=$("#graphCanvas"), ctx=canvas.getContext("2d"), inspector=$("#graphInspector");
    const types=Array.from(new Set(DATA.graph.nodes.map(n=>n.type)));
    const enabled=new Set(types);
    const filters=$("#graphFilters");
    DATA.graph.legend.forEach(item=>{
      const label=document.createElement("label");label.className="filter-item";
      const input=document.createElement("input");input.type="checkbox";input.checked=true;
      const dot=document.createElement("i");dot.style.background=NODE_PALETTE[item.type] || item.color;
      const text=document.createElement("span");text.textContent=TYPE_LABELS[item.type]||item.type;
      input.addEventListener("change",()=>{input.checked?enabled.add(item.type):enabled.delete(item.type);draw();});
      label.append(input,dot,text);filters.appendChild(label);
    });

    let state={scale:.75,ox:60,oy:20,drag:false,lastX:0,lastY:0,selected:null};
    function resize(fit=false){const rect=canvas.parentElement.getBoundingClientRect();const dpr=Math.min(window.devicePixelRatio||1,2);canvas.width=Math.floor(rect.width*dpr);canvas.height=Math.floor(rect.height*dpr);ctx.setTransform(dpr,0,0,dpr,0,0);if(fit)fitView();else draw();}
    function visibleNodes(){return DATA.graph.nodes.filter(n=>enabled.has(n.type));}
    function fitView(){const nodes=visibleNodes();if(!nodes.length)return;const xs=nodes.map(n=>n.position2d[0]),ys=nodes.map(n=>n.position2d[1]);const w=Math.max(...xs)-Math.min(...xs)+180,h=Math.max(...ys)-Math.min(...ys)+180;const rect=canvas.parentElement.getBoundingClientRect();state.scale=Math.min(rect.width/w,rect.height/h)*.92;state.ox=(rect.width-(Math.min(...xs)+Math.max(...xs))*state.scale)/2;state.oy=(rect.height-(Math.min(...ys)+Math.max(...ys))*state.scale)/2;draw();}
    function point(n){return{x:n.position2d[0]*state.scale+state.ox,y:n.position2d[1]*state.scale+state.oy};}
    function draw(){
      const rect=canvas.parentElement.getBoundingClientRect();ctx.clearRect(0,0,rect.width,rect.height);
      ctx.lineWidth=1;
      const map=new Map(DATA.graph.nodes.map(n=>[n.id,n]));
      DATA.graph.edges.forEach(e=>{const a=map.get(e.source),b=map.get(e.target);if(!a||!b||!enabled.has(a.type)||!enabled.has(b.type))return;const p=point(a),q=point(b);ctx.strokeStyle=e.source_kind==="canonical_edge"?"#9db9c9d6":"#c1d5e2b8";ctx.beginPath();ctx.moveTo(p.x,p.y);ctx.lineTo(q.x,q.y);ctx.stroke();});
      visibleNodes().forEach(n=>{const p=point(n),r=n.type==="system"?9:n.type==="module"?7:n.type==="project"?3.6:5;ctx.beginPath();ctx.arc(p.x,p.y,r,0,Math.PI*2);ctx.fillStyle=NODE_PALETTE[n.type] || n.color;ctx.globalAlpha=state.selected&&state.selected!==n.id?.35:1;ctx.fill();ctx.globalAlpha=1;if(state.selected===n.id){ctx.strokeStyle="#1c597d";ctx.lineWidth=2;ctx.stroke();}if(state.scale>.55 && !["project","fact_class"].includes(n.type)){ctx.fillStyle="#3a627c";ctx.font="10px system-ui";ctx.fillText(n.label,p.x+r+5,p.y+3);}});
    }
    function hit(x,y){let best=null,dist=15;visibleNodes().forEach(n=>{const p=point(n),d=Math.hypot(p.x-x,p.y-y);if(d<dist){dist=d;best=n;}});return best;}
    function inspect(n){state.selected=n?n.id:null;if(!n){inspector.innerHTML='<p class="kicker">INSPECTOR</p><h3>Select a node</h3>';draw();return;}inspector.innerHTML="";const k=document.createElement("p");k.className="kicker";k.textContent="INSPECTOR";const type=document.createElement("span");type.className="inspect-type";type.textContent=n.type.replace("_"," ");const h=document.createElement("h3");h.textContent=n.label;inspector.append(k,type,h);const list=document.createElement("div");list.className="inspect-list";Object.entries(n).filter(x=>!["position2d","position3d","color","label","type"].includes(x[0])).forEach(([key,val])=>{if(val==null)return;const row=document.createElement("div");row.className="inspect-row";const b=document.createElement("b");b.textContent=key.replaceAll("_"," ");const s=document.createElement("span");s.textContent=String(val);row.append(b,s);list.appendChild(row);});inspector.appendChild(list);if(n.site_url||n.url){const a=document.createElement("a");a.href=n.site_url||n.url;a.target="_blank";a.rel="noreferrer";a.textContent="Open source destination ↗";inspector.appendChild(a);}draw();}
    canvas.addEventListener("pointerdown",e=>{state.drag=true;state.lastX=e.offsetX;state.lastY=e.offsetY;canvas.setPointerCapture(e.pointerId);});
    canvas.addEventListener("pointermove",e=>{if(!state.drag)return;state.ox+=e.offsetX-state.lastX;state.oy+=e.offsetY-state.lastY;state.lastX=e.offsetX;state.lastY=e.offsetY;draw();});
    canvas.addEventListener("pointerup",e=>{const dx=Math.abs(e.offsetX-state.lastX),dy=Math.abs(e.offsetY-state.lastY);state.drag=false;canvas.releasePointerCapture(e.pointerId);if(dx<4&&dy<4){const n=hit(e.offsetX,e.offsetY);if(n)inspect(n);}});
    canvas.addEventListener("wheel",e=>{e.preventDefault();const factor=e.deltaY<0?1.12:.89;const mx=e.offsetX,my=e.offsetY;state.ox=mx-(mx-state.ox)*factor;state.oy=my-(my-state.oy)*factor;state.scale=Math.max(.15,Math.min(3,state.scale*factor));draw();},{passive:false});
    $("#fitGraph").addEventListener("click",fitView);
    $("#resetGraph").addEventListener("click",()=>{state={scale:.75,ox:60,oy:20,drag:false,lastX:0,lastY:0,selected:null};fitView();});
    window.addEventListener("resize",()=>resize(false));
    DATA.graph2d={resize,select:(id)=>{const n=nodeById(id);if(n){enabled.add(n.type);inspect(n);fitView();setTimeout(()=>inspect(n),20);}}};
    setTimeout(()=>resize(true),50);
  }

  function setupGraph3d() {
    const canvas=$("#spatialCanvas"),ctx=canvas.getContext("2d"),inspector=$("#spatialInspector");
    let state={yaw:-.45,pitch:.25,distance:1050,drag:false,lastX:0,lastY:0,selected:null};
    DATA.graph.legend.forEach(item=>{const span=document.createElement("span");const dot=document.createElement("i");dot.style.background=NODE_PALETTE[item.type] || item.color;span.append(dot,document.createTextNode(TYPE_LABELS[item.type]||item.type));$("#spatialLegend").appendChild(span);});
    function resize(){const rect=canvas.parentElement.getBoundingClientRect(),dpr=Math.min(window.devicePixelRatio||1,2);canvas.width=Math.floor(rect.width*dpr);canvas.height=Math.floor(rect.height*dpr);ctx.setTransform(dpr,0,0,dpr,0,0);draw();}
    function project(n){let[x,y,z]=n.position3d;const cy=Math.cos(state.yaw),sy=Math.sin(state.yaw),cp=Math.cos(state.pitch),sp=Math.sin(state.pitch);const x1=x*cy-z*sy,z1=x*sy+z*cy,y1=y*cp-z1*sp,z2=y*sp+z1*cp;const rect=canvas.parentElement.getBoundingClientRect();const f=state.distance/(state.distance+z2+520);return{x:rect.width/2+x1*f,y:rect.height/2+y1*f,z:z2,f};}
    function draw(){const rect=canvas.parentElement.getBoundingClientRect();ctx.clearRect(0,0,rect.width,rect.height);const projected=new Map(DATA.graph.nodes.map(n=>[n.id,project(n)]));const sortedEdges=DATA.graph.edges.slice().sort((a,b)=>(projected.get(a.source)?.z||0)-(projected.get(b.source)?.z||0));sortedEdges.forEach(e=>{const a=projected.get(e.source),b=projected.get(e.target);if(!a||!b)return;ctx.strokeStyle=e.source_kind==="canonical_edge"?"#9ebbcbd9":"#c5dbe7c4";ctx.lineWidth=.7;ctx.beginPath();ctx.moveTo(a.x,a.y);ctx.lineTo(b.x,b.y);ctx.stroke();});const nodes=DATA.graph.nodes.slice().sort((a,b)=>projected.get(a.id).z-projected.get(b.id).z);nodes.forEach(n=>{const p=projected.get(n.id),r=Math.max(2,(n.type==="system"?10:n.type==="module"?7:4)*p.f);ctx.globalAlpha=Math.max(.28,Math.min(1,p.f));ctx.beginPath();ctx.arc(p.x,p.y,r,0,Math.PI*2);ctx.fillStyle=NODE_PALETTE[n.type] || n.color;ctx.fill();if(state.selected===n.id){ctx.globalAlpha=1;ctx.strokeStyle="#1c597d";ctx.lineWidth=2;ctx.stroke();}ctx.globalAlpha=1;});}
    function hit(x,y){let best=null,dist=18;DATA.graph.nodes.forEach(n=>{const p=project(n),d=Math.hypot(p.x-x,p.y-y);if(d<dist){dist=d;best=n;}});return best;}
    function inspect(n){state.selected=n?n.id:null;if(!n)return;inspector.innerHTML='<p class="kicker">INSPECTOR</p><span class="inspect-type">'+escapeText(n.type.replace("_"," "))+'</span><h3></h3><p class="muted"></p>';inspector.querySelector("h3").textContent=n.label;inspector.querySelector("p.muted").textContent=n.id;draw();}
    canvas.addEventListener("pointerdown",e=>{state.drag=true;state.lastX=e.offsetX;state.lastY=e.offsetY;canvas.setPointerCapture(e.pointerId);});
    canvas.addEventListener("pointermove",e=>{if(!state.drag)return;state.yaw+=(e.offsetX-state.lastX)*.006;state.pitch+=(e.offsetY-state.lastY)*.006;state.pitch=Math.max(-1.3,Math.min(1.3,state.pitch));state.lastX=e.offsetX;state.lastY=e.offsetY;draw();});
    canvas.addEventListener("pointerup",e=>{state.drag=false;canvas.releasePointerCapture(e.pointerId);const n=hit(e.offsetX,e.offsetY);if(n)inspect(n);});
    canvas.addEventListener("wheel",e=>{e.preventDefault();state.distance=Math.max(420,Math.min(2200,state.distance+e.deltaY*.7));draw();},{passive:false});
    $("#reset3d").addEventListener("click",()=>{state={yaw:-.45,pitch:.25,distance:1050,drag:false,lastX:0,lastY:0,selected:null};draw();});
    window.addEventListener("resize",resize);DATA.graph3d={resize};setTimeout(resize,50);
  }

  function renderRouting() {
    const select=$("#projectSelect"), selected=$("#selectedProject"), grid=$("#routeGrid"), table=$("#routeMatrix");
    DATA.matrix.projects.forEach(p=>{const o=document.createElement("option");o.value=p.project_id;o.textContent=p.project_id;select.appendChild(o);});
    const renderProject=()=>{selected.textContent=select.value;renderRouteCards();};
    select.addEventListener("change",renderProject);
    renderProject();

    function renderRouteCards(){
      grid.innerHTML="";
      DATA.matrix.route_columns.forEach(route=>{
        const card=document.createElement("article");card.className="route-card";
        const k=document.createElement("p");k.className="kicker";k.textContent=route.route_role;
        const h=document.createElement("h3");h.textContent=route.module_label;
        const fact=document.createElement("p");fact.className="fact";fact.textContent=route.fact_class;
        const dl=document.createElement("dl");
        [["Authority",route.authority_id],["Repository",route.repository_id],["Working ref",route.working_ref],["Instance",route.project_instance_assertion]].forEach(x=>{const wrap=document.createElement("div"),dt=document.createElement("dt"),dd=document.createElement("dd");dt.textContent=x[0];dd.textContent=x[1]||"—";wrap.append(dt,dd);dl.appendChild(wrap);});
        card.append(k,h,fact,dl);
        if(route.site_url){const a=document.createElement("a");a.href=route.site_url;a.target="_blank";a.rel="noreferrer";a.textContent="Open owning module ↗";card.appendChild(a);}
        grid.appendChild(card);
      });
    }

    const head=document.createElement("thead"),hr=document.createElement("tr");
    ["Project"].concat(DATA.matrix.route_columns.map(r=>r.route_role)).forEach(x=>{const th=document.createElement("th");th.textContent=x;hr.appendChild(th);});head.appendChild(hr);
    const body=document.createElement("tbody");
    DATA.matrix.projects.forEach(p=>{const tr=document.createElement("tr");const td=document.createElement("td");td.textContent=p.project_id;tr.appendChild(td);p.routes.forEach(()=>{const cell=document.createElement("td");cell.innerHTML='<span class="route-ok">ROUTABLE</span><br><span class="route-unknown">instance unknown</span>';tr.appendChild(cell);});body.appendChild(tr);});
    table.append(head,body);$("#matrixCount").textContent=DATA.matrix.projects.length+" projects × "+DATA.matrix.route_columns.length+" routes";
  }

  function renderAuthority() {
    const table=$("#authorityTable"),input=$("#authorityFilter");
    function draw(q=""){
      const query=q.toLowerCase();table.innerHTML="";
      const head=document.createElement("thead"),hr=document.createElement("tr");
      ["Fact class","Materiality","Authority","Owner","Writable store","Resolution"].forEach(x=>{const th=document.createElement("th");th.textContent=x;hr.appendChild(th);});head.appendChild(hr);table.appendChild(head);
      const body=document.createElement("tbody");
      DATA.authority.rows.filter(r=>!query||Object.values(r).join(" ").toLowerCase().includes(query)).forEach(r=>{const tr=document.createElement("tr");const vals=[r.fact_class,r.materiality,r.authority_id,r.owner_ref,r.writable_store,r.resolution_strategy];vals.forEach((v,i)=>{const td=document.createElement("td");if(i===1){const s=document.createElement("span");s.className="materiality"+(v==="SAFETY_CRITICAL"?" safety":"");s.textContent=v||"—";td.appendChild(s);}else td.textContent=v||"—";tr.appendChild(td);});body.appendChild(tr);});table.appendChild(body);
    }
    input.addEventListener("input",()=>draw(input.value));draw();
  }

  function renderDerivation() {
    const pipeline=$("#pipeline");
    [["Canonical JSON/JSONL","A7 identities · authority · routing"],["Python generator","deterministic projection logic"],["Website data","graph · search · matrix · Mermaid · Excalidraw"]].forEach((x,i)=>{const box=document.createElement("div");box.className="pipeline-box";const b=document.createElement("strong");b.textContent=x[0];const s=document.createElement("span");s.textContent=x[1];box.append(b,s);pipeline.appendChild(box);if(i<2){const a=document.createElement("div");a.className="pipeline-arrow";a.textContent="→";pipeline.appendChild(a);}});
    $("#buildId").textContent=shortSha(DATA.manifest.source_commit_sha);
    const dl=$("#provenance");
    [["Source sequence",DATA.manifest.source_sequence],["Sequence status",DATA.manifest.source_sequence_status],["Source commit",DATA.manifest.source_commit_sha],["Generated",DATA.manifest.generated_at],["Generator",DATA.manifest.generator],["Boundary",DATA.manifest.authority_boundary]].forEach(x=>{const dt=document.createElement("dt"),dd=document.createElement("dd");dt.textContent=x[0];dd.textContent=x[1]||"—";dl.append(dt,dd);});
    $("#mermaidSource").textContent=DATA.mermaid;
    $("#copyMermaid").addEventListener("click",async()=>{await navigator.clipboard.writeText(DATA.mermaid);$("#copyMermaid").textContent="Copied";setTimeout(()=>$("#copyMermaid").textContent="Copy",1200);});
    const root=$("#checksumList");DATA.manifest.outputs.forEach(o=>{const d=document.createElement("div");d.className="checksum";const b=document.createElement("b");b.textContent=o.path;const c=document.createElement("code");c.textContent=o.sha256;d.append(b,c);root.appendChild(d);});
  }

  load().catch(error => {
    console.error(error);
    document.querySelector(".shell").innerHTML='<div class="error-card"><strong>A7 projection failed to load.</strong><p></p></div>';
    document.querySelector(".error-card p").textContent=error.message;
  });
})();
