var avatar_input = document.getElementById("avatar_input");
var avatar_warning = document.getElementById("avatar_warning");

submit.onclick = function (){
    let form = {};
    if (username_input.value != "") {
        if (check_username()) {
            form["username"] = username_input.value;
        }
    }
    if (email_input.value != "") {
        if (check_email()) {
            form["email"] = email_input.value;
        }
    }
}