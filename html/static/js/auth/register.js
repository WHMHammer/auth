verification_code_input.style.display="none";

submit.onclick=function () {
    if (check_username() && check_password() && check_retype_password() && check_email()) {
        if (confirm("Are you sure to register with these information?")) {
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
            rq.open("POST",`${api_domain}/auth/register`,true);
            rq.setRequestHeader("Content-Type","application/json");
            rq.send(JSON.stringify({
                "username":username_input.value,
                "salt":salt,
                "password_hash":h.getHash("HEX"),
                "email":email_input.value
            }));
        }
    }
};