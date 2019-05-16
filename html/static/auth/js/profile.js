document.getElementById("username").innerHTML=user_token["username"];
document.getElementById("update_username").onclick=function () {
    let val=prompt("Please type in your new username:");
    if (!val) {
        return;
    }
    let xhr = new XMLHttpRequest;
    xhr.onreadystatechange=function () {
        if (this.readyState==4 && this.status==200) {
            user_token["username"]=val;
            localStorage.setItem("user_token",JSON.stringify(user_token));
            username.innerHTML=val;
        }
    };
    xhr.open("POST",`${api_domain}/auth/update_username`);
    xhr.setRequestHeader("Content-Type","application/json");
    xhr.send(JSON.stringify({
        "username": val,
        "user_token": user_token
    }));
};

document.getElementById("email").innerHTML=user_token["email"];
document.getElementById("update_email").onclick=function () {
    let val=prompt("Please type in your new email:");
    if (!val) {
        return;
    }
    let xhr = new XMLHttpRequest;
    xhr.onreadystatechange=function () {
        if (this.readyState==4 && this.status==200) {
            user_token["email"]=val;
            localStorage.setItem("user_token",JSON.stringify(user_token));
            email.innerHTML=val;
        }
    };
    xhr.open("POST",`${api_domain}/auth/update_email`);
    xhr.setRequestHeader("Content-Type","application/json");
    xhr.send(JSON.stringify({
        "email": val,
        "user_token": user_token
    }));
};

document.getElementById("avatar").setAttribute("src",user_token["avatar"]);
document.getElementById("update_avatar").onclick=function () {
    let val=prompt("Please type in the link to your new avatar:");
    if (!val) {
        return;
    }
    let xhr = new XMLHttpRequest;
    xhr.onreadystatechange=function () {
        if (this.readyState==4 && this.status==200) {
            user_token["avatar"]=val;
            localStorage.setItem("user_token",JSON.stringify(user_token));
            avatar.setAttribute("src",val);
        }
    };
    xhr.open("POST",`${api_domain}/auth/update_avatar`);
    xhr.setRequestHeader("Content-Type","application/json");
    xhr.send(JSON.stringify({
        "avatar": val,
        "user_token": user_token
    }));
};