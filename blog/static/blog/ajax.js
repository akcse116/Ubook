function logout_user() {
    let logout_request = new XMLHttpRequest();
    logout_request.onreadystatechange = function(){
        if	(this.readyState	===	4	&&	this.status	===	200){
            window.location.replace("/");
        }
    };
    logout_request.open("POST", window.location.host + "/user_logout");
    logout_request.send(JSON.stringify({"cookies" : document.cookie}));
}