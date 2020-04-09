/*
*   handling of 'post/followup' and 'like' communication on profile page
*
*   websocket pathname is /user_profile/ws/profile/chat/
*
*
*/

let socket = new WebSocket('ws://' + window.location.host + '/ws/profile/chat/');
socket.onmessage = function (e) {
    const info = JSON.parse(e.data);
    if(info.type === 'like'){
        const div = document.getElementById(info.id);
        const button = div.querySelectorAll("div.post")[0].querySelectorAll("button")[0];
        console.log(button);
        if(info.status){
            button.style.backgroundColor = "blue";
        }else{
            button.style.backgroundColor = "#f0f0f0";
        }
    }else if(info.type === 'comment'){
        const div = document.getElementById(info.parentid);
        const commentsection = div.querySelectorAll('div.comments')[0];
        commentsection.innerHTML += "<div class=\"commentbox\" id=" + info.id + ">" +
            "   <div class=\"post_header\">" +
            "            <p>" + info.author + "</p>" +
            "   </div>" +
            "   <div class=\"post\">" +
            "     <p>" +
                    info.body +
            "     </p>" +
            // "     <button class=\"likebtn\" onclick=\"sendLike(this);\" style=\"background-color: #f0f0f0\">" +
            // "         <img class=\"likebtn\" src=\"{% static 'user_profile/like.png' %}\">" +
            // "     </button>" +
            "   </div>" +
            "</div>";
        console.log(info.body);
    }
};

socket.onopen = function () {
    console.log("socket connection established");
};

// function renderMessages() {
//     console.log(socket.data);
// }

function sendLike(elem){
    console.log(elem.parentNode.parentNode.id);
    socket.send(JSON.stringify({
        type: "like",
        id: elem.parentNode.parentNode.id
    }));
}

function sendComment(elem){
    // const input = elem.querySelector("#post-comment");
    const id = elem.parentNode.parentNode.id;
    const input = elem.parentNode.querySelectorAll(".followup")[0];

    socket.send(JSON.stringify({
        type: "comment",
        id: id,
        body: input.value
    }));
    input.value = ""
}