/*
*   Handling of user signup and login
*
*   Signup function do_signup() communicates on route '/user_signup'
*
*   Login function do_login() cummunicates on route '/user_login'
*
*
* */


function do_signup() {
    let warn = document.getElementsByClassName('warning');
    let fname = document.getElementById("firstname");
    let lname = document.getElementById("lastname");
    let email = document.getElementById("email");
    let pass = document.getElementById("sign_password");
    if(fname.value.length != 0 && lname.value.length != 0 && email.value.length != 0 && pass.value.length != 0){
        if(warn[0].style.visibility === 'visible'){
            warn[0].style.visibility = 'hidden';
        }
        fname.value = '';
        lname.value = '';
        email.value = '';
        pass.value = '';
        let	request	=	new	XMLHttpRequest();
        request.onreadystatechange	=	function(){
            if	(this.readyState	===	4	&&	this.status	===	200){
                console.log(this.response);
                //	Do	something	with	the	response
                /*if input deemed invalid inform user and reprompt else user is redirected*/
            }
        };
        request.open("POST",	window.location.host + "/user_signup");
        let	data	=	{'first': fname.value, 'last': lname.value,	'email': email.value, 'password': pass.value};
        request.send(JSON.stringify(data));
    }
    else{
        warn[0].style.visibility = 'visible';
    }
}

function do_login(){
    /*let warn = document.getElementsByClassName('warning');*/
    let user = document.getElementById("login_username");
    let pass = document.getElementById("login_password");
    if(user.value.length != 0 && pass.value.length != 0){
        /*if(warn[1].style.visibility === 'visible'){
            warn[1].style.visibility = 'hidden';
        }*/
        user.value = '';
        pass.value = '';
        let	request	=	new	XMLHttpRequest();
        request.onreadystatechange	=	function(){
            if	(this.readyState	===	4	&&	this.status	===	200){
                console.log(this.response);
                //	Do	something	with	the	response
                /*if input deemed invalid inform user and reprompt else user is redirected*/
            }
        };
        request.open("POST",	window.location.host + "/user_signup");
        let	data	=	{'user': user.value, 'password': pass.value};
        request.send(JSON.stringify(data));
    }
    else{
        warn[1].style.visibility = 'visible';
    }
}