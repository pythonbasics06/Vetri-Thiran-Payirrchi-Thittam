async function getSession(){
  try { const r=await fetch('/session-info'); return r.ok ? await r.json() : null; } catch(e){ return null; }
}
async function setupNav(){
  const s=await getSession();
  const login=document.getElementById('loginLink'), logout=document.getElementById('logoutBtn');
  if(s){ if(login) login.classList.add('hidden'); if(logout){logout.classList.remove('hidden'); logout.onclick=async()=>{await fetch('/logout',{method:'POST'}); location.href='/';};}}
}
document.addEventListener('DOMContentLoaded', setupNav);
function escapeHtml(v){return String(v??'').replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[m]));}
