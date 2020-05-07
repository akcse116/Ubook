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
            button.style.backgroundColor = "#65ff74";
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
    }else if(info.type === 'post'){
        let container = document.getElementById("feed_wall");
        let img = "";
        if(info.media){
            img = "<img src=" + info.medialink + " style=\"max-width: 300px; max-height: 300px\">";
        }
        if(info.username === document.getElementById('main_username').innerText){
            container.insertAdjacentHTML("afterbegin",
                "<div class=\"container\" >" +
                "            <div class=\"post_block\" id="+ info.id + ">" +
                "                <div class=\"post_header\">" +
                img +
                "                    <p>" + info.author + "</p>" +
                "                </div>" +
                "                <div class=\"post\">" +
                "                    <p>" +
                info.body +
                "                    </p>" +
                "                    <button class=\"likebtn\" onclick=\"sendLike(this);\">" +
                "                        <i class =\"emoji\">&#128077;</i>" +
                "                    </button>" +
                "                </div>" +
                "                <br><br>" +
                "                <div class=\"comments\">" +
                "                </div>" +
                "                <div class=\"add_comment_post_div\">" +
                "                    <textarea class=\"followup\" id=\"followup1\"></textarea>" +
                "                    <button class=\"followup_comment_btn\" onclick=\"sendComment(this);\">Comment</button>" +
                "                </div>" +
                "            </div>" +
                "        </div>"
            );
        }

    }else if(info.type === 'message'){
        console.log(info);
        document.getElementById("notificationcontent").innerHTML += (
            "<div class=\"note\">\n" +
            "                <p class=\"notifuser\">" + info.sender + "</p>" +
            "<b>" +  info.fullname + "</b>" +  ": " + info.message +
            "</div>"
        )
    }else if(info.type === 'seen'){
        console.log(info);
        const notes = document.getElementsByClassName('note');
        const notifications = document.getElementById('notificationcontent');
        console.log(notes.length);
        let newnotif = '';
        for(let i of notes){
            const user = i.querySelector('.notifuser').innerText;
            console.log(user);
            console.log(info.sender);
            if(user !== info.sender){
                newnotif += i.outerHTML;
            }
        }
        notifications.innerHTML = newnotif;
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
        id: elem.parentNode.parentNode.id,
        user: document.getElementById('main_username').innerText
    }));
}

function sendComment(elem){
    // const input = elem.querySelector("#post-comment");
    const id = elem.parentNode.parentNode.id;
    const input = elem.parentNode.querySelectorAll(".followup")[0];

    socket.send(JSON.stringify({
        type: "comment",
        id: id,
        body: input.value,
        user: document.getElementById('main_username').innerText
    }));
    input.value = ""
}