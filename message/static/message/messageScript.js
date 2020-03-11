function addToLog(){
    const log = document.getElementById("messageLog");
    const message = document.getElementById("inputMessage");
    const val = message.value;
    console.log(val);
    message.value = "";
    if(val !== ""){
        log.innerHTML += (
            "<div class=\"yourMessage\">" + val + "</div>"
        );
    }
    message.focus();

}