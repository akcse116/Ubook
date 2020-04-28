const socket = new WebSocket('ws://' + window.location.host + '/ws/message/user/');

socket.onmessage = function (e) {
    console.log(e.data);
    const data = JSON.parse(e.data);
    document.getElementById("messageLog").innerHTML += "<div class=\"otherMessage\">"+ data.message + "</div>"
};

socket.onopen = function (e) {
    console.log("connected")
};

function addToLog(){
    const log = document.getElementById("messageLog");
    const message = document.getElementById("inputMessage");
    const val = message.value;
    // console.log(val);
    message.value = "";
    // if(val !== ""){
    //     log.innerHTML += (
    //         "<div class=\"yourMessage\">" + val + "</div>"
    //     );
    // }
    message.focus();
    socket.send(JSON.stringify({
        'sender': "a",
        'recepient': "b",
        'message': val
    }));
}