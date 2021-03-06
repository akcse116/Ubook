/*
*   gets and renders profile message wall
*
*   route: /profile_wall
*
* */

function get_wall_posts(){
    let	request	=	new	XMLHttpRequest();
    request.onreadystatechange	=	function(){
        if	(this.readyState	===	4	&&	this.status	===	200){
            if(this.response != undefined && this.response.length != 0){
                /* loop to generate posts  */
            }
            /* console.log(this.response); */
        }
    };
    request.open("GET",	window.location.host + "/profile_wall");
    request.send();
}


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
    logout_request.open("GET", "/login/logout/");
    logout_request.send();
}