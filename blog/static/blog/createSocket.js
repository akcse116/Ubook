const socket = new WebSocket('ws://' + window.location.host + '/ws/blog/');

socket.onmessage = function (e) {
    const info = JSON.parse(e.data);
    console.log(info);
    if(info.type === 'post'){
        let container = document.getElementsByClassName('posts')[0];
        let img = "";
        if(info.media){
            console.log(info.medialink);
            img = "<img src=" + info.medialink + " style=\"max-width: 300px; max-height: 300px\">";
        }
        container.insertAdjacentHTML("afterbegin",
            "<article class = \"post\" id=" + info.id + ">"+
            "            <div class = \"post-content\">" +
            "                <div class =\"post-box\">" +
                                img + "<br>" +
                                info.body +
            "                </div>" +
            "                <div class=\"interact\">" +
            "                    <button class = \"button\" type=\"button\" onclick=\"sendLike(this);\">" +
            "                        <i class =\"emoji\">&#128077;</i>" +
            "                    </button>" +
            "                    <form id=\"commentinput\" action=\"\" method=\"POST\" enctype=\"multipart/form-data\" onsubmit=\"sendComment(this);return false;\">" +
            "                        <label for = \"post-comment\">comment: </label>" +
            "                        <input id= \"post-comment\" type=\"text\" name=\"comment\">" +
            "                        <input type=\"submit\" value=\"comment\">" +
            "                    </form>" +
            "                </div>" +
            "            </div>" +
            "                    <div class=\"comments\">" +
            "                     </div>" +
            "            <div class = \"post-meta\">" +
                            info.author +
            "                Published: " + info.date +
            "            </div>" +
            "        </article>"
        );
    }else if(info.type === 'like'){
        const div = document.getElementById(info.id);
        const button = div.querySelectorAll("div.interact")[0].querySelectorAll("button")[0];
        console.log(button);
        if(info.status){
            button.style.backgroundColor = "blue";
        }else{
            button.style.backgroundColor = "white";
        }
    }else if(info.type === 'comment'){
        const div = document.getElementById(info.parentid);
        const commentsection = div.querySelectorAll('div.comments')[0];
        commentsection.innerHTML += "<div class=\"commentbox\" id=" + info.id + ">" +
                                        info.author + ": " + info.body +
                                    "</div>";
        console.log(info.body);
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

socket.onopen = function (e) {
    console.log("connected")
};

function sendPost(){
    const input = new FormData(document.getElementById("postinput"));
    const file = document.querySelector('#post-media');
    const reader = new FileReader();
    const textinput = document.getElementById("post-body");

    if(textinput.value || file.value){
        const upload = new XMLHttpRequest();
        upload.onreadystatechange = function () {
            if(this.readyState === 4 && this.status === 200){
                console.log(this.response);
            }
        };

        upload.open("POST", "/blog/createpost/");
        upload.send(input);

        textinput.value = "";
        file.value = "";
    }else{
        console.log("there's nothing!")
    }

}

function sendLike(elem){
    socket.send(JSON.stringify({
        type: "like",
        id: elem.parentNode.parentNode.parentNode.id
    }));
}

function sendComment(elem){
    const input = elem.querySelector("#post-comment");
    const id = elem.parentNode.parentNode.parentNode.id;
    socket.send(JSON.stringify({
        type: "comment",
        id: id,
        body: input.value
    }));
    input.value = ""
}

