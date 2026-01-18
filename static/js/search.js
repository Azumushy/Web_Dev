function search(){
fetch("/api/search/?q="+q.value,{
headers:{Authorization:"Bearer "+localStorage.access}
}).then(r=>r.json()).then(data=>{
results.innerHTML=""
data.forEach(u=>{
results.innerHTML+=`<li>${u.username} (${u.email})</li>`
})
})
}
