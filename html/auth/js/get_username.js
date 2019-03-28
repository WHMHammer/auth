var email_input=document.getElementById("email");
var email_warning=document.getElementById("email_warning");
var submit=document.getElementById("submit");
var email_err=true;

email_input.onblur=check_email;
submit.onclick=function () {
    if (email_err) {
        alert("Please correct the mistakes first");
    }
    else {
        let rq=new XMLHttpRequest();
        rq.open("POST","/cgi-bin/auth/get_username.py",true);
        rq.setRequestHeader("Content-Type","application/json");
        rq.send(JSON.stringify({
            "email":email_input.value
        }));
    }
    let form=document.getElementById("form")
    let success=document.getElementById("success");
    form.style.display="none";
    success.style.display="block";
};