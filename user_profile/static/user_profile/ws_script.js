/*
*   handling of 'post/followup' and 'like' communication on profile page
*
*   websocket pathname is /user_profile/ws/profile/chat/
*
*
*/

let socket = new WebSocket('ws://' + window.location.host + '/ws/profile/chat/');
socket.onmessage = renderMessages;

socket.onopen = function () {
    console.log("socket connection established");
}

function renderMessages() {
    console.log(socket.data);
}