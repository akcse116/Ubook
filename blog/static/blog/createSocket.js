const socket = new WebSocket('ws://' + window.location.host + '/ws/blog');

socket.onmessage = function (e) {
    console.log(e.data);
    const data = JSON.parse(e.data);
    document.getElementById("messageLog").innerHTML += "<div class=\"otherMessage\">"+ data.message + "</div>"
};

socket.onopen = function (e) {
    console.log("connected")
};