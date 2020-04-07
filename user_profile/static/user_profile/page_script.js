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
    request.open("GET",	window.location.host + "/post");
    request.send();
}