/* A7 Arc 01. Presentation only: public-safe read model generated from
   registry/entities/repositories.json + galactic-atlas-ui.v0.1.json.
   This script has no cross-repository or API write capabilities. */
"use strict";
(() => {
  const ROOT_ID = "REPO-000001";
  const OWNER_PREFIX = "FabinGurung/";
  const get = (id) => document.getElementById(id);
  const stage = get("spaceField");
  const edges = get("flightLines");
  const spinner = get("planetLoading");
  const message = get("galaxyError");
  const nodes = new Map();
  const segments = new Map();
  let stations = [];
  let sectors = [];
  let activeSector = "ALL";
  let searchQuery = "";
  let selected = ROOT_ID;

  const safeUrl = (url, kind) => {
    try {
      const address = new URL(url);
      return address.protocol === "https:" &&
        ((kind === "github" && address.origin === "https://github.com" &&
          address.pathname.startsWith("/FabinGurung/")) ||
        (kind === "pages" && address.origin === "https://fabingurung.github.io") ||
        (kind === "other" && (
          (address.origin === "https://github.com" && address.pathname.startsWith("/FabinGurung/")) ||
          address.origin === "https://fabingurung.github.io"
        )));
    } catch {
      return false;
    }
  };

  function point(station) {
    if (station.id === ROOT_ID) return {x:50, y:50};
    const a = Number(station.azimuth) * Math.PI / 180;
    const radius = Number(station.radial) * .76;
    return {x: 50 + Math.cos(a) * radius, y: 50 + Math.sin(a) * radius};
  }

  function link(anchor, url, kind, label) {
    if (!safeUrl(url, kind)) {
      anchor.removeAttribute("href");
      anchor.textContent = "Unavailable link — check catalogue";
      return;
    }
    anchor.href = url;
    anchor.target = "_blank";
    anchor.rel = "noopener noreferrer";
    if (label) anchor.textContent = label;
  }

  function selectStation(id, shouldFocus=false) {
    const selectedRecord = stations.find(x => x.id === id);
    if (!selectedRecord) return;
    selected = id;
    window.a7SelectedStationId = id;
    window.dispatchEvent(new CustomEvent("a7:station-selected", {detail:{id}}));
    for (const [key, button] of nodes) {
      const active = key === id;
      button.classList.toggle("is-selected", active);
      button.setAttribute("aria-pressed", String(active));
      if (shouldFocus && active) button.focus();
    }
    for (const [key, segment] of segments) segment.classList.toggle(
      "is-selected", key === id);
    get("selectedEmblem").textContent = selectedRecord.short;
    get("selectedRole").textContent = selectedRecord.role.replaceAll("_", " ");
    get("selectedSector").textContent = sectors.find(s=>s.id===selectedRecord.sector)?.label || "Unassigned";
    get("selectedTitle").textContent = selectedRecord.title;
    get("selectedSummary").textContent = selectedRecord.summary;
    get("selectedOwner").textContent = selectedRecord.owns;
    const isCentral = id === ROOT_ID;
    const homepage = isCentral
      ? new URL("control-towers.html", location.href).href
      : selectedRecord.website_url;
    if (isCentral) {
      get("selectedSite").href = homepage;
      get("selectedSite").textContent = "Open A7 Control Towers ↗";
      get("selectedSite").target = "_self";
      get("selectedSite").removeAttribute("rel");
    } else link(get("selectedSite"), homepage, "pages", "Visit system website ↗");
    link(get("selectedRepo"), selectedRecord.github_url, "github", "Repository, version history ↗");

    const extras = get("selectedExtras");
    extras.replaceChildren();
    for (const item of selectedRecord.deep_links || []) {
      if (!safeUrl(item.url, "other")) continue;
      const a = document.createElement("a");
      a.textContent = item.label + " ↗";
      a.href = item.url;
      a.target = "_blank";
      a.rel = "noopener noreferrer";
      extras.append(a);
    }
    renderProviderEvidence(selectedRecord);
    const when = selectedRecord.source_observed_at
      ? selectedRecord.source_observed_at.slice(0,10)
      : "undated";
    get("selectedEvidence").textContent =
      "Directory observation " + when + " · The owning GitHub repository and source provider establish the current version and actual operational status. This map cannot approve or edit it.";
  }


  /* Recorded provider snapshots are authored on A7 only after GitHub
     readback. No API calls, speculative dependencies, or release approvals. */
  function renderProviderEvidence(station) {
    const e = station.provider_evidence;
    if (!e || !e.not_live || !e.last_successful_publication) return;
    get("inspectorObservationDate").textContent = "Observed " + e.observed_date + " (snapshot)";
    const status = get("inspectorStatus");
    status.textContent = e.provider_label.replaceAll("_"," ");
    status.classList.toggle("arc02-review",/FAILED|PENDING|OLDER|MIXED|SEPARATE|FEATURE/.test(e.provider_label));
    get("inspectorMainSha").textContent = e.main_sha.slice(0,12);
    get("inspectorPublishedBranch").textContent = e.publication_branch;
    get("inspectorDeployedSha").textContent = e.last_successful_publication.sha.slice(0,12);
    get("inspectorDeployedAt").textContent = e.last_successful_publication.at.slice(0,16).replace("T"," ")+" UTC";
    get("inspectorCapabilities").textContent = e.capability;
    get("inspectorGate").textContent = e.owner_gate;
    get("inspectorDependency").textContent = e.dependency_note;
    const anchors = get("inspectorProviderLinks");
    anchors.replaceChildren();
    const base="https://github.com/" + station.module_repository;
    function add(label,url) {
      if(!safeUrl(url,"other")) return;
      const a=document.createElement("a");
      a.href=url; a.target="_blank"; a.rel="noopener noreferrer";
      a.textContent=label+" ↗";anchors.append(a);
    }
    add("Successful deployment evidence",base+"/actions/runs/"+e.last_successful_publication.id);
    if(e.related_workflow?.id!==e.last_successful_publication.id) {
      add("Additional workflow observation",base+"/actions/runs/"+e.related_workflow.id);
    }
    add("Main source at recorded SHA",base+"/tree/"+e.main_sha);
    if(e.publication_branch!=="main")
      add("Publication commit",base+"/tree/"+e.last_successful_publication.sha);
  }

  /* Arc 03: UI filtering only; never a runtime relationship or authority claim. */
  function eligible(station) {
    if(station.id===ROOT_ID) return true;
    if(activeSector!=="ALL" && station.sector!==activeSector) return false;
    if(!searchQuery) return true;
    const terms=[station.title,station.short,station.summary,station.role,
      station.module_repository,station.provider_evidence?.capability].join(" ").toLocaleLowerCase();
    return terms.includes(searchQuery);
  }
  function visibleStations(){ return stations.filter(eligible); }
  function applySectors(){
    let visible=0;
    for(const station of stations){
      const show=eligible(station);
      if(show && station.id!==ROOT_ID)visible++;
      const node=nodes.get(station.id);
      if(node){node.hidden=!show;node.setAttribute("aria-hidden",String(!show));}
      const line=segments.get(station.id);
      if(line)line.style.display=show?"":"none";
    }
    const current=stations.find(s=>s.id===selected);
    if(current && !eligible(current))selectStation(ROOT_ID);
    get("sectorStatus").textContent="Showing "+visible+" of "+(stations.length-1)+" destinations · A7 hub stays visible · Navigation only";
    for(const chip of get("sectorFilters").querySelectorAll("button[data-sector]")){
      const on=chip.dataset.sector===activeSector;
      chip.classList.toggle("is-active",on);
      chip.setAttribute("aria-pressed",String(on));
    }
  }
  function setupSectors(){
    const target=get("sectorFilters");
    target.replaceChildren();
    const choices=[{id:"ALL",label:"All sectors",count:stations.length-1},
      ...sectors.filter(s=>s.id!=="CONTROL")];
    for(const sector of choices){
      const button=document.createElement("button");
      button.type="button";button.className="galaxy-sector-chip";
      button.dataset.sector=sector.id;
      button.textContent=sector.label+" · "+sector.count;
      button.setAttribute("aria-pressed","false");
      button.addEventListener("click",()=>{activeSector=sector.id;applySectors();});
      target.append(button);
    }
    const input=get("sectorSearch");
    input.addEventListener("input",()=>{searchQuery=input.value.trim().toLocaleLowerCase();applySectors();});
    input.addEventListener("keydown",event=>{if(event.key==="Escape"){
      input.value="";searchQuery="";applySectors();
    }});
    get("sectorReset").addEventListener("click",()=>{
      activeSector="ALL";searchQuery="";input.value="";applySectors();input.focus();
    });
    applySectors();
  }

  function valid(data) {
    if (!data || data.schema !== "a7://galactic-atlas-read-projection/0.1" ||
      data.non_authoritative !== true || data.station_count !== 9 ||
      !Array.isArray(data.stations) || data.stations.length !== 9 ||
      !Array.isArray(data.links) || data.links.length !== 8 ||
      data.navigation_arc!=="GALACTIC_ATLAS_ARC_03_SECTORS" ||
      data.sector_taxonomy_presentation_only!==true ||
      data.sector_count!==5 || !Array.isArray(data.sectors) ||
      data.sectors.length!==5) return false;
    const sectorNames=new Set(data.sectors.map(s=>s.id));
    if(sectorNames.size!==5 || !sectorNames.has("CONTROL"))return false;
    const ids = new Set();
    for (const station of data.stations) {
      if (!station.id || ids.has(station.id) ||
          typeof station.title !== "string" ||
          typeof station.summary !== "string" ||
          !sectorNames.has(station.sector) ||
          (station.id===ROOT_ID && station.sector!=="CONTROL") ||
          typeof station.owns !== "string" ||
          !station.module_repository?.startsWith(OWNER_PREFIX) ||
          !safeUrl(station.github_url, "github") ||
          !safeUrl(station.website_url, "pages") ||
          !station.provider_evidence?.not_live ||
          !station.provider_evidence?.last_successful_publication?.id ||
          !station.provider_evidence?.owner_gate ||
          !Number.isFinite(Number(station.azimuth)) ||
          !Number.isFinite(Number(station.radial))) return false;
      ids.add(station.id);
    }
    return ids.has(ROOT_ID) && data.links.every(l =>
      l.from === ROOT_ID && ids.has(l.to) && l.to !== ROOT_ID &&
      l.authority_transfer === false);
  }

  function render(data) {
    stations = data.stations;
    sectors = data.sectors;
    nodes.clear(); segments.clear();
    edges.replaceChildren();
    stage.querySelectorAll(".star-node").forEach(node => node.remove());
    for (const station of stations) {
      const {x, y} = point(station);
      if (station.id !== ROOT_ID) {
        const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
        line.setAttribute("x1", "50");
        line.setAttribute("y1", "50");
        line.setAttribute("x2", String(x));
        line.setAttribute("y2", String(y));
        edges.append(line);
        segments.set(station.id, line);
      }
      const button = document.createElement("button");
      button.type = "button";
      button.className = "star-node" + (station.id === ROOT_ID ? " star-hub" : "");
      button.dataset.zone = station.zone;
      button.dataset.sector = station.sector;
      button.dataset.repoId = station.id;
      button.dataset.role = station.role;
      button.style.left = x + "%";
      button.style.top = y + "%";
      button.setAttribute("aria-label", "Inspect " + station.title);
      button.setAttribute("aria-pressed", "false");
      const emblem = document.createElement("span");
      emblem.className = "star-planet";
      emblem.textContent = station.short;
      emblem.setAttribute("aria-hidden", "true");
      const name = document.createElement("span");
      name.className = "star-name";
      name.textContent = station.title;
      button.append(emblem, name);
      button.addEventListener("click", () => selectStation(station.id));
      button.addEventListener("keydown", (event) => {
        if (!["ArrowLeft","ArrowRight","ArrowUp","ArrowDown"].includes(event.key)) return;
        event.preventDefault();
        const step = event.key === "ArrowLeft" || event.key === "ArrowUp" ? -1 : 1;
        const available=visibleStations();
        const index=available.findIndex(x => x.id === station.id);
        const next=available[(index + step + available.length) % available.length];
        selectStation(next.id, true);
      });
      stage.append(button);
      nodes.set(station.id, button);
    }
    spinner?.remove();
    const observed = stations.map(x => x.source_observed_at).filter(Boolean).sort().at(-1);
    get("readStatus").textContent = observed
      ? "Catalogue records dated up to " + observed.slice(0,10)
      : "Recorded catalogue / date unverified";
    selectStation(ROOT_ID);
    setupSectors();
  }

  async function main() {
    try {
      const response = await fetch("data/galactic-atlas.json", {cache:"no-store"});
      if (!response.ok) throw Error("Catalogue data HTTP " + response.status);
      const data = await response.json();
      if (!valid(data)) throw Error("Catalogue schema/provenance failed");
      render(data);
    } catch (error) {
      spinner.textContent = "Directory not available";
      message.hidden = false;
      get("readStatus").textContent = "Directory readback unavailable";
      // No fabricated or hardcoded fallback repository records.
      console.error("A7 public projection read failed", error);
    }
  }
  main();
})();
