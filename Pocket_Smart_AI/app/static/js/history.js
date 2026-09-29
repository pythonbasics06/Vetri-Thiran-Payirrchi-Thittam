async function loadHistory(){
  const el=document.getElementById('historyList');
  try{
    const r=await fetch('/history'); if(r.status===401){location.href='/login';return;} const rows=await r.json();
    el.innerHTML=rows.length?rows.map(x=>`<div class="history-row"><div><b>${escapeHtml(x.response.title||x.planner)}</b><div>${escapeHtml(x.response.summary||'')}</div><small>${escapeHtml(x.planner)} · ${new Date(x.created_at).toLocaleString()}</small></div><strong>${money(x.response.budget)}</strong></div>`).join(''):'<p>No history found.</p>';
  }catch(e){el.textContent=e.message;}
}
document.addEventListener('DOMContentLoaded',loadHistory);
function money(n){return '₹'+Number(n||0).toLocaleString('en-IN',{maximumFractionDigits:0});}
