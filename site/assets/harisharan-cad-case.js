(() => {
  const host=document.getElementById('a7HarisharanMemoryCase');
  if(!host)return;
  const safeUrl=(value)=>{try{const u=new URL(value);return u.protocol==='https:'&&(u.hostname==='github.com'||u.hostname==='fabingurung.github.io')?u.href:null;}catch{return null}};
  fetch('./data/harisharan-cad-evidence-mnemonic.json',{cache:'no-store'}).then(x=>{if(!x.ok)throw Error('Source unavailable');return x.json()}).then(data=>{
    if(data?.id!=='A7-MEM-CAD-HAR-20261110-001'||data?.constructionApproval!==false||data?.sourceApproval!==false||data?.reminders?.length!==3)throw Error('Unadmitted source');
    const items=host.querySelector('.a7-har-cards');items.replaceChildren();
    for(const entry of data.reminders){
      const card=document.createElement('article');card.className='a7-har-card';
      const h=document.createElement('h4');h.textContent=entry.heading;
      const p=document.createElement('p');p.textContent=entry.text;
      const small=document.createElement('small');small.textContent=entry.status.replaceAll('_',' ');
      card.append(h,p,small);items.append(card);
    }
    const links=host.querySelector('.a7-har-links');links.replaceChildren();
    for(const x of data.sourceLinks){const url=safeUrl(x.url);if(!url)continue;const a=document.createElement('a');a.href=url;a.textContent=x.label;a.rel='noopener';links.append(a);}
    host.querySelector('.a7-har-status').textContent='Version '+data.revision+' · '+data.observed_on+' · SOURCE REFERENCE ONLY · NOT FOR CONSTRUCTION';
  }).catch(()=>{host.querySelector('.a7-har-status').textContent='Source not verified in this session — refer to owning CAD review; no approvals assumed';});
})();