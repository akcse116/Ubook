/**
 * User logout function sends a GET request to server.
 * Server clears session. On response refreshes page.
 *
 */
function logout_user() {
    let logout_request = new XMLHttpRequest();
    logout_request.onreadystatechange = function(){
        if	(this.readyState	===	4	&&	this.status	===	200){
            window.location.replace("/");
        }
    };
    logout_request.open("GET", "/user_logout");
    logout_request.send();
}