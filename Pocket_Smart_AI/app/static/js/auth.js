async function handleAuth(form, endpoint){
  const data=Object.fromEntries(new FormData(form).entries());
  const msg=document.getElementById('formMessage');
  try{
    const r=await fetch(endpoint,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)});
    const body=await r.json();
    if(!r.ok) throw new Error(body.detail || 'Request failed');
    msg.textContent=body.message;
    msg.style.background='#e8fff1';
    setTimeout(()=>location.href='/dashboard',500);
  }catch(e){msg.textContent=e.message;msg.style.background='#ffe8e8';}
}
const lf=document.getElementById('loginForm'); if(lf) lf.onsubmit=e=>{e.preventDefault();handleAuth(lf,'/login')};
const rf=document.getElementById('registerForm'); if(rf) rf.onsubmit=e=>{e.preventDefault();handleAuth(rf,'/register')};
