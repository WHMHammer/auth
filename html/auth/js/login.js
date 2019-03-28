var username_input=document.getElementById("username");
var username_warning=document.getElementById("username_warning");
var password_input=document.getElementById("password");
var password_warning=document.getElementById("password_warning");
var submit=document.getElementById("submit");
var username_err=true;
var password_err=true;

username_input.onblur=check_username;
password_input.onblur=check_password;
submit.onclick=function () {
    if (username_err || password_err) {
        alert("Please correct the mistakes first");
    }
    else {
        let rq=new XMLHttpRequest();
        rq.onreadystatechange=function () {
            if (this.readyState==4) {
                if (this.status==200) {
                    login(JSON.parse(this.responseText));
                }
                else if (this.status==404) {
                    alert("invalid username");
                }
                else if (this.status==500) {
                    alert("unexpected error");
                }
            }
        };
        rq.open("POST","/cgi-bin/auth/get_challenge.py",true);
        rq.setRequestHeader("Content-Type","application/json");
        rq.send(JSON.stringify({
            "username":username_input.value
        }));
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
                let form=document.getElementById("form")
                let success=document.getElementById("success");
                form.style.display="none";
                success.style.display="block";
            }
            else if (this.status==403) {
                alert("login failed");
            }
            else if (this.status==500) {
                alert("unexpected error");
            }
        }
    };
    rq.open("POST","/cgi-bin/auth/login.py",true);
    rq.setRequestHeader("Content-Type","application/json");
    rq.send(JSON.stringify({
        "username":username_input.value,
        "response":h.getHash("HEX")
    }));
}