var username_input=document.getElementById("username");
var username_warning=document.getElementById("username_warning");
var password_input=document.getElementById("password");
var password_warning=document.getElementById("password_warning");
var retype_password_input=document.getElementById("retype_password");
var retype_password_warning=document.getElementById("retype_password_warning");
var email_input=document.getElementById("email");
var email_warning=document.getElementById("email_warning");
var submit=document.getElementById("submit");
var username_err=true;
var password_err=true;
var retype_password_err=true;
var email_err=true;

username_input.onblur=check_username;
password_input.onblur=check_password;
retype_password_input.onblur=check_retype_password;
email_input.onblur=check_email;
submit.onclick=function () {
    if (username_err || password_err || retype_password_err || email_err) {
        alert("Please correct the mistakes first");
    }
    else {
        if (confirm("Are you sure to register with these information?")) {
            var alnum="1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM";
            var salt="";
            var rand;
            for (let i=0;i<16;i++) {
                rand=Math.floor(Math.random()*62);
                salt+=alnum.slice(rand,rand+1);
            }
            var h=new jsSHA("SHA3-512","TEXT");
            h.update(salt+password_input.value);
            
            var rq=new XMLHttpRequest();
            rq.onreadystatechange=function () {
                if (this.readyState==4) {
                    if (this.status==200) {
                        var form=document.getElementById("form")
                        var success=document.getElementById("success");
                        form.style.display="none";
                        success.style.display="block";
                    }
                    else if (this.status==403) {
                        alert("invalid username or email address");
                    }
                    else if (this.status==500) {
                        alert("unexpected error");
                    }
                }
            };
            rq.open("POST","/cgi-bin/auth/register.py",true);
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