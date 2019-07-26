var username_input=document.getElementById("username_input");
var username_warning=document.getElementById("username_warning");
function legal_username(s) {
    return s.length<65;
}
function check_username() {
    if (username_input.value=="") {
        username_warning.innerHTML="Username is required";
        username_warning.style.display="block";
        return false;
    }
    else if (!legal_username(username_input.value)) {
        username_warning.innerHTML="Illegal username";
        username_warning.style.display="block";
        return false;
    }
    else {
        username_warning.style.display="none";
        return true;
    }
}

var password_input=document.getElementById("password_input");
var password_warning=document.getElementById("password_warning");
function check_password() {
    if (password_input.value=="") {
        password_warning.innerHTML="Password is required";
        password_warning.style.display="block";
        return false;
    }
    else {
        password_warning.style.display="none";
        return true;
    }
}


var retype_password_input=document.getElementById("retype_password_input");
var retype_password_warning=document.getElementById("retype_password_warning");
function check_retype_password() {
    if (retype_password_input.value=="") {
        retype_password_warning.innerHTML="Retyping password is required";
        retype_password_warning.style.display="block";
        return false;
    }
    else if (retype_password_input.value!=password_input.value) {
        retype_password_warning.innerHTML="Your passwords don't match";
        retype_password_warning.style.display="block";
        return false;
    }
    else {
        retype_password_warning.style.display="none";
        return true;
    }
}

var verification_code_input=document.getElementById("verification_code_input");
var verification_code_warning=document.getElementById("verification_code_warning");
function check_verification_code() {
    if (verification_code_input.value=="") {
        verification_code_warning.innerHTML="Verification code is required";
        verification_code_warning.style.display="block";
        return false;
    }
    else if (verification_code_input.value.length!=32) {
        verification_code_warning.innerHTML="Verification code not in correct format";
        verification_code_warning.style.display="block";
        return false;
    }
    else {
        verification_code_warning.style.display="none";
        return true;
    }
}

var email_input=document.getElementById("email_input");
var email_warning=document.getElementById("email_warning");
function legal_email(s) {
    let re=/^[\x00-\x7f]+@[\x00-\x7f]+\.[\x00-\x7f]+$/;
    return re.test(s) && s.length<65;
}
function check_email() {
    if (email_input.value=="") {
        email_warning.innerHTML="Email address is required";
        email_warning.style.display="block";
        return false;
    }
    else if (!legal_email(email_input.value)) {
        email_warning.innerHTML="Illegal email address";
        email_warning.style.display="block";
        return false;
    }
    else {
        email_warning.style.display="none";
        return true;
    }
}

var submit=document.getElementById("submit");