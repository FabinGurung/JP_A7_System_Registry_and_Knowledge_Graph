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

