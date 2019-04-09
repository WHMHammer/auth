retype_password_input.style.display="none";

submit.onclick=function () {
    if (check_username() && check_password() && check_verification_code() && check_email()) {
        let challenge=verification_code_input.value.slice(0,16);
        let salt=verification_code_input.value.slice(16);
        let h=new jsSHA("SHA3-512","TEXT");
        h.update(salt+password_input.value);
        let salt_password=h.getHash("HEX");
        h=new jsSHA("SHA3-512","TEXT");
        h.update(challenge+salt_password);
        
        let rq=new XMLHttpRequest();
        rq.onreadystatechange=function () {
            if (this.readyState==4) {
                if (this.status==200) {
                    save_login(JSON.parse(this.responseText));
                    window.location.replace("/");
                }
                else if (this.status==403) {
                    alert("Verification failed, try again.");
                }
                else if (this.status==500) {
                    alert("unexpected error");
                }
            }
        };
        rq.open("POST","/auth/verify",true);
        rq.setRequestHeader("Content-Type","application/json");
        rq.send(JSON.stringify({
            "username":username_input.value,
            "response":h.getHash("HEX"),
            "email":email_input.value
        }));
    }
};