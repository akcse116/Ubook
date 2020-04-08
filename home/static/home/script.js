function post_signup() {
    let fname = document.getElementById("firstname");
    console.log('First name is :' + fname.value);
    let lname = document.getElementById("lastname");
    let email = document.getElementById("email");
    let pass = document.getElementById("sign_password");
    var	request	=	new	XMLHttpRequest();
    request.onreadystatechange	=	function(){
        if	(this.readyState	===	4	&&	this.status	===	200){
            console.log(this.response);
            //	Do	something	with	the	response
        }
    };
    request.open("POST",	"/path");
    let	data	=	{'first': fname, 'last': lname,	'email': email, 'password': pass}
    request.send(JSON.stringify(data));
}