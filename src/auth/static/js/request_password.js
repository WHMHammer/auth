username_input.style.display="none";
password_input.style.display="none";
retype_password_input.style.display="none";
verification_code_input.style.display="none";

submit.onclick=function () {
    if (email_err) {
        alert("Please correct the mistakes first");
    }
    else {
        let rq=new XMLHttpRequest();
        rq.onreadystatechange=function () {
            if (this.readyState==4) {
                window.location.replace("reset_password");
            }
        };
        rq.open("POST","/auth/request_password",true);
        rq.setRequestHeader("Content-Type","application/json");
        rq.send(JSON.stringify({
            "email":email_input.value
        }));
    }
};