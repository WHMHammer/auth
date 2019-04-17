var username=localStorage.getItem("username");
var header=document.getElementById("header");
if (username==null) {
    var register=document.createElement("div");
    register.className="header";
    register.innerHTML="<p><a href='auth/register'>Register</a></p>";
    var login=document.createElement("div");
    login.className="header";
    login.innerHTML="<p><a href='auth/login'>Login</a></p>";
    header.appendChild(register);
    header.appendChild(login);
}
else {
    var logout=document.createElement("div");
    logout.className="header";
    logout.innerHTML="<p><a href='auth/logout'>Logout</a></p>";
    var profile=document.createElement("div");
    profile.className="header";
    profile.innerHTML=`<p><a href='auth/profile'>${username}</a></p>`;
    header.appendChild(logout);
    header.appendChild(profile);
}