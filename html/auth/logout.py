import flask

import auth


@auth.bp.route("/logout", methods=("GET",))
def logout():
    return """
        <script src="js/auth.js"></script>
        <script>
            check_login(true);
            var rq=new XMLHttpRequest();
            rq.onreadystatechange=function () {
                if (this.readyState==4) {
                    localStorage.removeItem("user_token");
                    window.location.replace("/");
                }
            };
            rq.open("POST",`${api_domain}/auth/logout`,true);
            rq.setRequestHeader("Content-Type","application/json");
            rq.send();
        </script>
    """
