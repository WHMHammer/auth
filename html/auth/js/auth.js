function legal_username(s) {
    return s.length<65;
}

function check_username() {
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

function check_password() {
    if (password_input.value=="") {
        password_err=true;
        password_warning.innerHTML="Password is required";
        password_warning.style.display="block";
    }
    else {
        password_err=false;
        password_warning.style.display="none";
    }
}

function check_retype_password() {
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
}

function legal_email(s) {
    let re=/^.+@{1}.+\.{1}.+$/;
    return re.test(s) && s.length<65;
}

function check_email() {
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
}

function check_verification_code() {
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