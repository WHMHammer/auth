retype_password_input.style.display="none";
verification_code_input.style.display="none";
email_input.style.display="none";

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
                    alert("The username you entered has not been registered.");
                }
                else if (this.status==500) {
                    alert("unexpected error");
                }
            }
        };
        rq.open("POST","/auth/get_challenge",true);
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
                window.location.replace("/")
            }
            else if (this.status==403) {
                alert("Login failed, try again.");
            }
            else if (this.status==500) {
                alert("unexpected error");
            }
        }
    };
    rq.open("POST","/auth/login",true);
    rq.setRequestHeader("Content-Type","application/json");
    rq.send(JSON.stringify({
        "username":username_input.value,
        "response":h.getHash("HEX")
    }));
}