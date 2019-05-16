var user_token = localStorage.getItem("user_token");
var right = document.getElementById("right");

if (user_token == null) {
    right.innerHTML = ' \
        <h6><a href="/auth/register">Register</a></h6> \
        <h6><a href="/auth/login">Login</a></h6> \
    '
}
else {
    right.innerHTML = ` \
        <h6><a href="/auth/profile">${JSON.parse(user_token)["username"]}</a></h6> \
        <h6><a href="/auth/logout">Logout</a></h6> \
    `
}