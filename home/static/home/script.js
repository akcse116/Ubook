/**
*   Handling of user signup and login
*
*   Signup function user_signup() communicates on route '/signup'
*
*   Login function login_user() communicates on route '/login'
*
*
* */


function user_signup() {
    let warn = document.getElementsByClassName('warning');
    let firstname = document.getElementById('firstname');
    let lastname = document.getElementById('lastname');
    let email = document.getElementById('email');
    let password = document.getElementById('sign_password');
    const input = new FormData(document.getElementById("signup-form"));
    if(warn[0].style.visibility === 'visible'){
        warn[0].style.visibility = 'hidden';
    }
    let	request	= new XMLHttpRequest();
    request.onreadystatechange = function(){
        if (this.readyState === 4 && this.status === 200){
            if(this.response !== "Account successfully registered"){
                warn[0].style.color = "red";
            }else{
                warn[0].style.color = "blue";
                firstname.value = '';
                lastname.value = '';
                email.value = '';
                password.value = '';
            }
            warn[0].innerHTML = this.response;
            warn[0].style.visibility = 'visible';
            /*	Do	something	with	the	response*/
            /*if input deemed invalid inform user and reprompt else user is redirected*/
        }
    };
    request.open("POST", window.location + "signup/");
    request.send(input);

}



function login_user(){
    /*let warn = document.getElementsByClassName('warning');*/
    let user = document.getElementById("login_username");
    let pass = document.getElementById("login_password");

    user.value = '';
    pass.value = '';
    let	request	= new XMLHttpRequest();
    const input = new FormData(document.getElementById("login"));
    request.onreadystatechange = function(){
        if	(this.readyState === 4 && this.status === 200){
            console.log(this.response);
            //	Do	something	with	the	response
            /*if input deemed invalid inform user and reprompt else user is redirected*/
        }
    };
    request.open("POST", window.location + "login/");
    request.send(input);

    // if(user.value.length != 0 && pass.value.length != 0){
    //     /*if(warn[1].style.visibility === 'visible'){
    //         warn[1].style.visibility = 'hidden';
    //     }*/
    //
    // }
    // else{
    //     // warn[1].style.visibility = 'visible';
    // }
}