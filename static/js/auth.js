const API = "/api/"

function register(){
fetch(API+"register/",{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({
username:username.value,
email:email.value,
first_name:first_name.value,
last_name:last_name.value,
password:password.value,
password2:password2.value
})
})
.then(async r=>{
let data = await r.json()
if(!r.ok){
alert(JSON.stringify(data))
return
}
alert("Registered successfully")
location.href="/login/"
})
}


function login(){
fetch(API+"login/",{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({email:email.value,password:password.value})
}).then(r=>r.json()).then(d=>{
localStorage.access=d.access
localStorage.refresh=d.refresh
location.href="/search/"
})
}
