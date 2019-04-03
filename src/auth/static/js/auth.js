var username_input=document.getElementById("username_input");
var username_warning=document.getElementById("username_warning");
var username_err=true;
function legal_username(s) {
    return s.length<65;
}
username_input.onblur=function () {
    if (username_input.value=="") {
        username_err=true;
        username_warning.innerHTML="Username is required";
        username_warning.style.display="block";
    }
    else if (!legal_username(username_input.value)) {
        username_err=true;
        username_warning.innerHTML="Illegal username";
        username_warning.style.display="block";
    }
    else {
        username_err=false;
        username_warning.style.display="none";
    }
}

var password_input=document.getElementById("password_input");
var password_warning=document.getElementById("password_warning");
var password_err=true;
password_input.onblur=function () {
    if (password_input.value=="") {
        password_err=true;
        password_warning.innerHTML="Password is required";
        password_warning.style.display="block";
    }
    else {
        password_err=false;
        password_warning.style.display="none";
    }
};


var retype_password_input=document.getElementById("retype_password_input");
var retype_password_warning=document.getElementById("retype_password_warning");
var retype_password_err=true;
retype_password_input.onblur=function () {
    if (retype_password_input.value=="") {
        retype_password_err=true;
        retype_password_warning.innerHTML="Retyping password is required";
        retype_password_warning.style.display="block";
    }
    else if (retype_password_input.value!=password_input.value) {
        retype_password_err=true;
        retype_password_warning.innerHTML="Your passwords don't match";
        retype_password_warning.style.display="block";
    }
    else {
        retype_password_err=false;
        retype_password_warning.style.display="none";
    }
};

var verification_code_input=document.getElementById("verification_code_input");
var verification_code_warning=document.getElementById("verification_code_warning");
var verification_code_err=true;
verification_code_input.onblur=function () {
    if (verification_code_input.value=="") {
        verification_code_err=true;
        verification_code_warning.innerHTML="Verification code is required";
        verification_code_warning.style.display="block";
    }
    else if (verification_code_input.value.length!=32) {
        verification_code_err=true;
        verification_code_warning.innerHTML="Verification code not in correct format";
        verification_code_warning.style.display="block";
    }
    else {
        verification_code_err=false;
        verification_code_warning.style.display="none";
    }
}

var email_input=document.getElementById("email_input");
var email_warning=document.getElementById("email_warning");
var email_err=true;
function legal_email(s) {
    let re=/^[\x00-\x7f]+@[\x00-\x7f]+\.[\x00-\x7f]+$/;
    return re.test(s) && s.length<65;
}
email_input.onblur=function () {
    if (email_input.value=="") {
        email_err=true;
        email_warning.innerHTML="Email address is required";
        email_warning.style.display="block";
    }
    else if (!legal_email(email_input.value)) {
        email_err=true;
        email_warning.innerHTML="Illegal email address";
        email_warning.style.display="block";
    }
    else {
        email_err=false;
        email_warning.style.display="none";
    }
};

var submit=document.getElementById("submit");