username_input.style.display="none";
password_input.style.display="none";
retype_password_input.style.display="none";
verification_code_input.style.display="none";

submit.onclick=function () {
    if (check_email()) {
        let rq=new XMLHttpRequest();
        rq.onreadystatechange=function () {
            if (this.readyState==4) {
                window.location.replace("/auth/login")
            }
        }
        rq.open("POST","/auth/get_username",true);
        rq.setRequestHeader("Content-Type","application/json");
        rq.send(JSON.stringify({
            "email":email_input.value
        }));
    }
};