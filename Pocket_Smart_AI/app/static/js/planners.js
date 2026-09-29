function money(n){return '₹'+Number(n||0).toLocaleString('en-IN',{maximumFractionDigits:0});}
function renderResult(el,d){
  el.classList.add('show');
  el.innerHTML=`<div class="card"><div class="result-head"><div><p class="eyebrow">${escapeHtml(d.source_mode||'AI')}</p><h2>${escapeHtml(d.title)}</h2><p>${escapeHtml(d.summary)}</p></div></div>
  <div class="stat-grid"><div class="stat"><small>Budget</small><b>${money(d.budget)}</b></div><div class="stat"><small>Estimated total</small><b>${money(d.estimated_total)}</b></div><div class="stat"><small>Remaining</small><b>${money(d.remaining_budget)}</b></div></div>
  <h3>Recommendations</h3>${(d.recommendations||[]).map(x=>`<div class="rec"><div><span class="platform">${escapeHtml(x.platform)} · ${escapeHtml(x.category)}</span><h4>${escapeHtml(x.name)}</h4><p>${escapeHtml(x.reason)}</p><a href="${escapeHtml(x.url)}" target="_blank" rel="noopener">Open platform search ↗</a></div><div class="price">${money(x.estimated_price*x.quantity)}</div></div>`).join('')}
  <h3>Tips</h3><ul class="tips">${(d.tips||[]).map(x=>`<li>${escapeHtml(x)}</li>`).join('')}</ul></div>`;
}
function errorResult(el,msg){el.classList.add('show');el.innerHTML=`<div class="card"><b>Could not generate the plan.</b><p>${escapeHtml(msg)}</p></div>`;}

const homeForm=document.getElementById('homeForm');
if(homeForm){
  const list=document.getElementById('homeItems');
  function addItem(cat='Ceiling light',qty=1,notes=''){const row=document.createElement('div');row.className='item-row';row.innerHTML=`<input placeholder="Item/category" value="${escapeHtml(cat)}"><input type="number" min="1" value="${qty}"><input placeholder="Notes" value="${escapeHtml(notes)}"><button type="button" class="remove">×</button>`;row.querySelector('.remove').onclick=()=>row.remove();list.appendChild(row);}
  addItem('Ceiling light',2,'Warm white'); addItem('Dining table',1,'Compact');
  document.getElementById('addHomeItem').onclick=()=>addItem();
  homeForm.onsubmit=async e=>{e.preventDefault();const f=new FormData(homeForm);const rows=[...list.children].map(r=>({category:r.children[0].value,quantity:Number(r.children[1].value),notes:r.children[2].value})).filter(x=>x.category);const payload={budget:Number(f.get('budget')),rooms:f.get('rooms').split(',').map(x=>x.trim()).filter(Boolean),style:f.get('style'),location:f.get('location'),items:rows};await sendJson('/generate-home',payload,document.getElementById('result'));};
}
const partyForm=document.getElementById('partyForm');
if(partyForm) partyForm.onsubmit=async e=>{e.preventDefault();const f=new FormData(partyForm);await sendJson('/generate-party',{budget:Number(f.get('budget')),guests:Number(f.get('guests')),event_type:f.get('event_type'),venue:f.get('venue'),city:f.get('city'),preferences:f.get('preferences')},document.getElementById('result'));};
const jewelryForm=document.getElementById('jewelryForm');
if(jewelryForm) jewelryForm.onsubmit=async e=>{e.preventDefault();const f=new FormData(jewelryForm);await sendForm('/generate-jewelry',f,document.getElementById('result'));};
async function sendJson(url,payload,el){el.innerHTML='<div class="card">Generating...</div>';el.classList.add('show');try{const r=await fetch(url,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});const d=await r.json();if(!r.ok)throw new Error(d.detail||'Request failed');renderResult(el,d);}catch(e){errorResult(el,e.message);}}
async function sendForm(url,form,el){el.innerHTML='<div class="card">Analyzing and generating...</div>';el.classList.add('show');try{const r=await fetch(url,{method:'POST',body:form});const d=await r.json();if(!r.ok)throw new Error(d.detail||'Request failed');renderResult(el,d);}catch(e){errorResult(el,e.message);}}
