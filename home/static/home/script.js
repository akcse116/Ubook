function post_signup() {
    let fname = document.getElementById("firstname");
    console.log('First name is:' + fname.value);
    let lname = document.getElementById("lastname");
    let email = document.getElementById("email");
    let pass = document.getElementById("sign_password");
    if(fname.value.length != 0 && lname.value.length != 0 && email.value.length != 0 && pass.value.length != 0){
        fname.value = '';
        lname.value = '';
        email.value = '';
        pass.value = '';
        let	request	=	new	XMLHttpRequest();
        request.onreadystatechange	=	function(){
            if	(this.readyState	===	4	&&	this.status	===	200){
                console.log(this.response);
                //	Do	something	with	the	response
            }
        };
        request.open("POST",	"/path");
        let	data	=	{'first': fname.value, 'last': lname.value,	'email': email.value, 'password': pass.value}
        request.send(JSON.stringify(data));
    }
    else{
    }

}