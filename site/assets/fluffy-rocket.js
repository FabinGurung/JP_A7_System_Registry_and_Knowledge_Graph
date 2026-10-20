/* A7 Cloud Orbit, purely decorative mascot, no data or navigation mutations. */
(() => {"use strict";
const reduced=window.matchMedia("(prefers-reduced-motion: reduce)");
const allowed=()=>!reduced.matches && !document.hidden && !(navigator.connection && navigator.connection.saveData);
let timer=null,flight=null,rocket=null,retired=false;
const random=(a,b)=>a+Math.random()*(b-a);
function stop(){if(timer!==null){clearTimeout(timer);timer=null;}if(flight){flight.cancel();flight=null;}if(rocket)rocket.style.opacity="0";}
function schedule(){if(retired||!allowed())return;timer=setTimeout(()=>{timer=null;fly();},Math.round(random(17000,32000)));}
function fly(){
 if(!allowed()||!rocket)return;
 const w=window.innerWidth,h=window.innerHeight;
 if(w<300||h<260)return;
 const f=Math.random()<.5,sz=rocket.getBoundingClientRect().width||90;
 const points=[
 [f?-sz-30:w+sz+30,random(.18,.78)*h],
 [w*.18,random(.13,.36)*h],
 [w*.42,random(.55,.88)*h],
 [w*.63,random(.18,.52)*h],
 [w*.83,random(.42,.79)*h],
 [f?w+sz+30:-sz-30,random(.24,.74)*h]
 ];
 if(!f){for(let i=1;i<points.length-1;i++)points[i][0]=w-points[i][0];}
 const frames=points.map(([x,y],i)=>{
  const next=points[Math.min(i+1,points.length-1)],prev=points[Math.max(i-1,0)];
  const rotation=Math.atan2(next[1]-prev[1],next[0]-prev[0])*180/Math.PI+90;
  return {offset:i/(points.length-1),transform:`translate3d(${x}px,${y}px,0) rotate(${rotation}deg)`,opacity:(i===0||i===points.length-1)?"0":"0.95"};
 });
 flight=rocket.animate(frames,{duration:Math.round(random(9000,14500)),easing:"ease-in-out",fill:"both",iterations:1});
 flight.onfinish=()=>{flight=null;rocket.style.opacity="0";schedule();};
}
function create(){
 if(reduced.matches||rocket)return;
 rocket=document.createElement("div");rocket.className="a7-rocket-mascot";rocket.setAttribute("aria-hidden","true");rocket.setAttribute("role","presentation");
 const pic=document.createElement("img");pic.src="assets/fluffy-rocket.svg";pic.alt="";pic.decoding="async";rocket.append(pic);document.body.append(rocket);
 timer=setTimeout(()=>{timer=null;fly();},Math.round(random(4500,8200)));
}
document.addEventListener("visibilitychange",()=>{stop();if(allowed())schedule();});
if(reduced.addEventListener)reduced.addEventListener("change",()=>{stop();if(allowed()){if(!rocket)create();else schedule();}});
window.addEventListener("pagehide",()=>{retired=true;stop();},{once:true});
if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",create,{once:true});else create();
})();