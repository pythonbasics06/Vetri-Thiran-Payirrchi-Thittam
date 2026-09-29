async function loadDashboard(){
  const welcome=document.getElementById('welcome'), list=document.getElementById('dashboardHistory');
  try{
    const s=await fetch('/session-info'); if(!s.ok){location.href='/login';return;}
    const user=(await s.json()).user; welcome.textContent=`Hello, ${user.name}. Here are your recent plans.`;
    const r=await fetch('/history'); if(!r.ok) throw new Error('Could not load history');
    const rows=await r.json();
    list.innerHTML=rows.length?rows.slice(0,5).map(x=>`<div class="history-row"><div><b>${escapeHtml(x.planner)}</b><div>${escapeHtml(x.response.title||'Recommendation')}</div></div><small>${new Date(x.created_at).toLocaleString()}</small></div>`).join(''):'<p>No saved recommendations yet.</p>';
  }catch(e){list.textContent=e.message;}
}
document.addEventListener('DOMContentLoaded',loadDashboard);
