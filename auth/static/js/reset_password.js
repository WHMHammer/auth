function check_verification_code() {
    if (verification_code_input.value=="") {
        verification_code_warning.innerHTML="Verification code is required";
        verification_code_warning.style.display="block";
        return false;
    }
    else if (verification_code_input.value.length!=16) {
        verification_code_warning.innerHTML="Verification code not in correct format";
        verification_code_warning.style.display="block";
        return false;
    }
    else {
        verification_code_warning.style.display="none";
        return true;
    }
}

submit.onclick=function () {
    if (check_username() && check_password() && check_retype_password() && check_verification_code() && check_email()) {
        if (confirm("Are you sure to reset your password with these information?")) {
            let alnum="1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM";
            let salt="";
            let rand;
            for (let i=0;i<16;i++) {
                rand=Math.floor(Math.random()*62);
                salt+=alnum.slice(rand,rand+1);
            }
            let h=new jsSHA("SHA3-512","TEXT");
            h.update(salt+password_input.value);
            
            let rq=new XMLHttpRequest();
            rq.onreadystatechange=function () {
                if (this.readyState==4) {
                    if (this.status==200) {
                        save_login(JSON.parse(this.responseText));
                        window.location.replace("/auth/verify");
                    }
                    else if (this.status==403) {
                        alert(JSON.parse(this.responseText)["err_msg"].join("\n"))
                    }
                    else if (this.status==500) {
                        alert("unexpected error");
                    }
                }
            };
            rq.open("POST","/auth/reset_password",true);
            rq.setRequestHeader("Content-Type","application/json");
            rq.send(JSON.stringify({
                "username":username_input.value,
                "email":email_input.value,
                "response":verification_code_input.value,
                "salt":salt,
                "password_hash":h.getHash("HEX")
            }));
        }
    }
};