retype_password_input.style.display="none";
verification_code_input.style.display="none";
email_input.style.display="none";

document.getElementById("right").innerHTML = ' \
    <h6><a href="register">Register</a></h6> \
    <h6><a href="get_username">forgot username?</a></h6> \
    <h6><a href="request_password">forgot password?</a></h6> \
';

submit.onclick=function () {
    if (check_username() && check_password()) {
        let rq=new XMLHttpRequest();
        rq.onreadystatechange=function () {
            if (this.readyState==4) {
                if (this.status==200) {
                    login(JSON.parse(this.responseText));
                }
                else if (this.status==404) {
                    alert("The username you entered has not been registered.");
                }
                else if (this.status==500) {
                    alert("unexpected error");
                }
            }
        };
        rq.open("GET",`${api_domain}/auth/login?username=${encodeURIComponent(username_input.value)}`,true);
        rq.setRequestHeader("Content-Type","application/json");
        rq.send();
    }
};

function login(rp) {
    let h=new jsSHA("SHA3-512","TEXT");
    h.update(rp["salt"]+password_input.value);
    let salt_password=h.getHash("HEX");
    h=new jsSHA("SHA3-512","TEXT");
    h.update(rp["challenge"]+salt_password);
    
    let rq=new XMLHttpRequest();
    rq.onreadystatechange=function () {
        if (this.readyState==4) {
            if (this.status==200) {
                localStorage.setItem("user_token",JSON.stringify(JSON.parse(this.responseText)["user_token"]));
                window.location.replace("/");
            }
            else if (this.status==403) {
                alert("Login failed, try again.");
            }
            else if (this.status==500) {
                alert("unexpected error");
            }
        }
    };
    rq.open("POST",`${api_domain}/auth/login`,true);
    rq.setRequestHeader("Content-Type","application/json");
    rq.send(JSON.stringify({
        "username":username_input.value,
        "response":h.getHash("HEX")
    }));
}