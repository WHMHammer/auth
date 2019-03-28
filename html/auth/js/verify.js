var username_input=document.getElementById("username");
var username_warning=document.getElementById("username_warning");
var password_input=document.getElementById("password");
var password_warning=document.getElementById("password_warning");
var verification_code_input=document.getElementById("verification_code_input");
var verification_code_warning=document.getElementById("verification_code_warning");
var email_input=document.getElementById("email");
var email_warning=document.getElementById("email_warning");
var submit=document.getElementById("submit");
var username_err=true;
var password_err=true;
var verification_code_err=true;
var email_err=true;

username_input.onblur=check_username;
password_input.onblur=check_password;
verification_code_input.onblur=check_verification_code;
email_input.onblur=check_email;
submit.onclick=function () {
    if (username_err || password_err || verification_code_err || email_err) {
        alert("Please correct the mistakes first");
    }
    else {
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
                    let form=document.getElementById("form")
                    let success=document.getElementById("success");
                    form.style.display="none";
                    success.style.display="block";
                }
                else if (this.status==403) {
                    alert("verification failed");
                }
                else if (this.status==500) {
                    alert("unexpected error");
                }
            }
        };
        rq.open("POST","/cgi-bin/auth/verify.py",true);
        rq.setRequestHeader("Content-Type","application/json");
        rq.send(JSON.stringify({
            "username":username_input.value,
            "response":h.getHash("HEX"),
            "email":email_input.value
        }));
    }
};