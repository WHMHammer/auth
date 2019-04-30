var user_token=JSON.parse(localStorage.getItem("user_token"));
document.getElementById("avatar").setAttribute("src",user_token["avatar"]);
document.getElementById("username").innerHTML=`<p>${user_token["username"]}</p>`;
document.getElementById("email").innerHTML=`<p>${user_token["email"]}</p>`;