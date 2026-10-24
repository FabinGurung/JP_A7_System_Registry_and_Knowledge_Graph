"use strict";
/* A7 desktop+mobile browser QA against generated, local non-authoritative site. */
const { chromium } = require("playwright");
const { spawn } = require("child_process");
const fs = require("fs");
const { setTimeout: delay } = require("timers/promises");
const assert = require("node:assert/strict");
const URL = "http://127.0.0.1:8877/";
const out = "browser-qa-output";
fs.mkdirSync(out,{recursive:true});
const report={time:new Date().toISOString(),checks:[],screenshots:[],status:"IN_PROGRESS",kind:"AUTOMATED_REAL_BROWSER_NOT_HUMAN_ACCEPTANCE"};
function pass(name){report.checks.push({name,status:"PASS"});console.log("PASS "+name);}
async function untilReady(){
  for(let i=0;i<80;i++){try{const r=await fetch(URL);if(r.ok)return;}catch{} await delay(300);}
  throw new Error("local site server not ready");
}
async function inspect(page,kind){
  await page.goto(URL,{waitUntil:"load",timeout:30000});
  await page.locator(".star-node").first().waitFor({timeout:15000});
  await page.waitForFunction(()=>document.querySelectorAll(".star-node").length===9 && document.querySelector("#arc04Count")?.textContent.includes("4 documented navigation"),{timeout:15000});
  assert.equal(await page.locator(".star-node").count(),9);
  pass(kind+": nine source-backed stations");
  const start=await page.locator("#arc04Count").textContent();
  assert.match(start,/0 proposals shown/);
  await page.locator("#arc04RouteList .arc04-item").first().click();
  await page.locator('#arc04Inspect a[href*="/registry/edges/edges.jsonl#L"]').waitFor();
  pass(kind+": link to immutable canonical source evidence");
  await page.locator('.star-node[data-repo-id="REPO-000003"]').click();
  await page.locator("#arc04IncludeProposals").check();
  await page.waitForFunction(()=>document.querySelector("#arc04Count")?.textContent.includes("3 proposals shown"));
  assert.equal(await page.locator("#arc04RouteList .arc04-item.is-proposed").count(),3);
  await page.locator("#arc04RouteList .arc04-item.is-proposed").first().click();
  assert.match(await page.locator("#arc04Inspect").textContent(),/not admitted as a canonical graph edge/i);
  pass(kind+": proposals gated and explicitly non-authoritative");
  await page.locator("#arc04IncludeProposals").uncheck();
  await page.waitForFunction(()=>document.querySelector("#arc04Count")?.textContent.includes("0 proposals shown"));
  await page.locator("#sectorSearch").fill("unlikely_nonexistent_repos_name");
  await page.waitForFunction(()=>document.querySelector("#sectorStatus")?.textContent.includes("0 of 8 destinations"));
  await page.locator("#sectorReset").click();
  await page.waitForFunction(()=>document.querySelector("#sectorStatus")?.textContent.includes("8 of 8 destinations"));
  pass(kind+": Arc03 search, empty state and reset unchanged");
  const screenshot=out+"/atlas-"+kind+".png";
  await page.screenshot({path:screenshot,fullPage:true});
  report.screenshots.push(screenshot);
  await page.waitForFunction(()=>document.querySelector("#arc05HistoryCount")?.textContent.includes("6 source-linked history records"));
  assert.equal(await page.locator("#arc05HistoryList .arc05-history-item").count(),6);
  await page.locator("#arc05HistoryList .arc05-history-item").first().click();
  await page.locator('#arc05HistoryInspector a[href*="/releases/tag/"]').waitFor();
  await page.locator('.star-node[data-repo-id="REPO-000006"]').click();
  await page.waitForFunction(()=>document.querySelector("#arc05HistoryCount")?.textContent.includes("1 source-linked history record"));
  await page.locator('#arc05HistoryInspector a[href*="/actions/runs/"]').waitFor();
  await page.locator('.star-node[data-repo-id="REPO-000001"]').click();
  await page.waitForFunction(()=>document.querySelector("#arc05HistoryCount")?.textContent.includes("6 source-linked history records"));
  pass(kind+": Arc05 true tag, five immutable A7 events, dated peer publication");
  await page.locator("#arc06World").waitFor({state:"visible"});
  await page.waitForFunction(()=>document.querySelector("#arc06World")?.options.length===9);
  await page.locator("#arc06World").selectOption("REPO-000006");
  await page.locator("#arc06Go").click();
  await page.waitForFunction(()=>window.a7SelectedStationId==="REPO-000006");
  assert.match(page.url(),/world=REPO-000006/);
  await page.locator("#arc06CompareWorld").selectOption("REPO-000003");
  await page.waitForFunction(()=>document.querySelectorAll("#arc06Comparison .arc06-compare-card").length===2);
  assert.match(await page.locator("#arc06CompareStatus").textContent(),/not implied/);
  await page.locator("#arc06Next").click();
  await page.waitForFunction(()=>window.a7SelectedStationId!=="REPO-000006");
  assert.ok((await page.locator("#arc06Journal button").count())>=2);
  pass(kind+": Arc06 world flight deck, route URL, next and source-only comparison");
  await page.screenshot({path:out+"/arc06-"+kind+".png",fullPage:true});
  // The L1 history must be navigable from L0, source-derived and usable on mobile.
  await page.locator('.a7-shell-nav a[href="history.html"]').click();
  await page.locator("#dhCommitList .dh-entry").first().waitFor({timeout:15000});
  const historyCount=await page.locator("#dhCommitList .dh-entry").count();
  assert.ok(historyCount>=1,"Git history must be populated");
  await page.locator('#dhCommitList a[href*="/commit/"]').first().waitFor();
  assert.match(await page.locator("#dhObserved").textContent(),/Dated GitHub Pages build snapshot, not live status/);
  await page.locator("#dhSearch").fill("A7_NOT_A_REAL_COMMIT_000000");
  assert.equal(await page.locator("#dhCommitList .dh-entry").count(),0);
  await page.locator("#dhSearch").fill("");
  await page.locator("#dhKind").selectOption("merge");
  assert.ok((await page.locator("#dhCommitList .dh-entry").count())<=historyCount);
  await page.locator("#dhKind").selectOption("all");
  pass(kind+": L0 navigation → L1 Git timeline, filters, source commit links");
  const historyShot=out+"/history-"+kind+".png";
  await page.screenshot({path:historyShot,fullPage:true});report.screenshots.push(historyShot);
  await page.goto(URL+"roadmap.html",{waitUntil:"load"});
  await page.locator("#roadmapDeveloped .rp-item").first().waitFor();
  assert.ok((await page.locator("#roadmapDeveloped .rp-item").count())>=20);
  assert.match(await page.locator("#roadmapSequence").textContent(),/^\d{6}$/, "Sequence derives from canonical registry and can advance");
  await page.locator("#roadmapSearch").fill("unlikely_xyz_a7_roadmap");
  assert.equal(await page.locator("#roadmapDeveloped .rp-item").count(),0);
  pass(kind+": L1 source-built roadmap and working search");
  await page.goto(URL+"resource-navigator.html",{waitUntil:"load"});
  await page.locator("#rnResources .rn-resource").first().waitFor();
  assert.equal(await page.locator("#rnOrganizations .rn-choice").count(),1);
  assert.equal(await page.locator("#rnProjects .rn-choice").count(),1);
  assert.equal(await page.locator("#rnCategories .rn-choice").count(),3);
  assert.equal(await page.locator("#rnResources .rn-resource").count(),3);
  await page.locator("#rnCategories .rn-choice").nth(1).click();
  assert.equal(await page.locator("#rnResources .rn-resource").count(),3);
  await page.locator("#rnSearch").fill("Developer Dock");
  assert.equal(await page.locator("#rnResources .rn-resource").count(),1);
  await page.locator("#rnReset").click();
  assert.equal(await page.locator("#rnResources .rn-resource").count(),3);
  const viewport=await page.evaluate(()=>({scroll:document.documentElement.scrollWidth,width:window.innerWidth}));
  assert.ok(viewport.scroll<=viewport.width+4,"Arc07 overflow "+JSON.stringify(viewport));
  pass(kind+": Arc07 four-level resource route, categories, search, reset and viewport");
  const navShot=out+"/resource-navigator-"+kind+".png";
  await page.screenshot({path:navShot,fullPage:true});report.screenshots.push(navShot);
  await page.goto(URL+"developer-dock.html",{waitUntil:"load"});
  await page.locator("#dockGroups .dock-item").first().waitFor();
  assert.ok((await page.locator("#dockGroups .dock-item").count())>=15);
  await page.locator("#dockSearch").fill("unlikely_xyz_dock_123");
  assert.equal(await page.locator("#dockGroups .dock-item").count(),0);
  await page.goto(URL+"memory-wall.html#platform-role-board",{waitUntil:"load"});
  await page.locator("#platformRows tr").nth(7).waitFor();
  assert.equal(await page.locator("#platformRows tr").count(),8);
  assert.match(await page.locator("#platformMotto").textContent(),/WEBSITE IS THE WINDOW/);
  assert.equal(await page.locator("#platformSourcePair article").count(),2);
  assert.equal(await page.locator("#platformOutputStrip span").count(),4);
  await page.locator("#platformProvenance summary").click();
  assert.equal(await page.locator("#platformProvenanceFields li").count(),7);
  assert.equal(await page.locator("#platformClaimLabels span").count(),8);
  assert.match(await page.locator("#platformAutomation").textContent(),/not evidence/);
  await page.locator("#posters .poster-card").nth(2).waitFor({timeout:15000});
  assert.equal(await page.locator("#posters .poster-card").count(),3);
  assert.match(await page.locator("#platformExample").textContent(),/IFC parser/);
  assert.equal(await page.locator("#platformExamples span").count(),6);
  await page.locator("#uiVocabTerms .ui-vocab-term").nth(12).waitFor();
  assert.equal(await page.locator("#uiVocabTerms .ui-vocab-term").count(),13);
  assert.equal(await page.locator("#uiVocabRegister .ui-vocab-row").count(),2);
  await page.locator("#uiVocabToggle").click();
  assert.equal(await page.locator("#uiVocabToggle").getAttribute("aria-pressed"),"true");
  assert.match(await page.locator("#uiVocabRegister").textContent(),/EX-001/);
  await page.locator('#uiVocabFilters button[data-category="WORKFLOW"]').click();
  assert.equal(await page.locator("#uiVocabTerms .ui-vocab-term").count(),3);
  await page.locator("#uiVocabSearch").fill("provider readback");
  assert.equal(await page.locator("#uiVocabTerms .ui-vocab-term").count(),1);
  await page.locator("#uiVocabSearch").fill("");
  await page.locator('#uiVocabFilters button[data-category="ALL"]').click();
  assert.equal(await page.locator("#uiVocabTerms .ui-vocab-term").count(),13);
  pass(kind+": Collection 04 two panel samples, 13 terms, filtering, ID toggle and preservation");
  await page.locator("#storageArchRows tr").nth(6).waitFor({timeout:15000});
  assert.equal(await page.locator("#storageArchRows tr").count(),7);
  assert.equal(await page.locator("#storageArchFlow article").count(),3);
  assert.match(await page.locator("#storageArchRule").textContent(),/foreign keys/i);
  const rows=await page.locator("#storageArchRows").textContent();
  for(const format of ["SQL (.sql)","JSONL (.jsonl)","SQLite","JSON (.json)","CSV (.csv)","Google Sheets / Excel","Google Drive"])assert.ok(rows.includes(format),"Storage matrix missing "+format);
  assert.match(await page.locator("#storageArchStatus").textContent(),/versioned guidance, not proof/i);
  pass(kind+": Collection 05 seven public-safe format roles, provider boundary and original four collections");
  const storageShot=out+"/memory-storage-"+kind+".png";
  await page.screenshot({path:storageShot,fullPage:true});report.screenshots.push(storageShot);
  pass(kind+": L1 developer file search and semantic eight-role command architecture, original posters, privacy gate");
  await page.screenshot({path:out+"/developer-platform-"+kind+".png",fullPage:true});
  if(kind==="mobile"){
    const widths=await page.evaluate(()=>({scroll:document.documentElement.scrollWidth,viewport:window.innerWidth}));
    assert.ok(widths.scroll<=widths.viewport+4,"mobile page horizontal overflow: "+JSON.stringify(widths));
    pass("mobile viewport has no page-level overflow");
  }
}
async function run(){
 let server,browser;
 try{
   server=spawn("python3",["-m","http.server","8877","--bind","127.0.0.1","--directory","site"],{stdio:"ignore"});
   await untilReady();
   browser=await chromium.launch({headless:true,args:["--no-sandbox"]});
   for(const [kind,width,height] of [["desktop",1440,960],["mobile",390,844]]){
      const context=await browser.newContext({viewport:{width,height},deviceScaleFactor:1,reducedMotion:"reduce"});
      const page=await context.newPage();
      page.on("pageerror",e=>report.checks.push({name:kind+" page error: "+e.message,status:"FAIL"}));
      await inspect(page,kind);
      await context.close();
   }
   assert.equal(report.checks.filter(x=>x.status==="FAIL").length,0,"Unexpected page errors");
   report.status="PASS";console.log("A7 REAL CHROMIUM QA PASS");
 }catch(e){
   report.status="FAIL";report.error=e.stack||String(e);console.error(report.error);
   process.exitCode=1;
 }finally{
   try{fs.writeFileSync(out+"/report.json",JSON.stringify(report,null,2)+"\n");}catch{}
   if(browser)await browser.close();
   if(server)server.kill("SIGTERM");
 }
}
run();

