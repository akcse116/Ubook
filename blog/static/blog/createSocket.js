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
        const user = document.getElementById('main_username').innerText;
        let friendbtn = '';
        if(info.username !== user){
            if(info.friend){
                friendbtn = '<button type=\'submit\' class="btn" name="friendBtn" onclick="friend(this);">Unfriend User</button>';
            }else{
                friendbtn = '<button type=\'submit\' class="btn" name="friendBtn" onclick="friend(this);">Friend User</button>';
            }
        }
        container.insertAdjacentHTML("afterbegin",
            "<article class = \"post\" id=" + info.id + ">"+
            "            <div class = \"post-content\">" +
            "                <div class =\"post-box\">" +
                                img + "<br>" +
                                info.body +
            "                </div>" +
            "                <div class=\"interact\">" + friendbtn +
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
            "                <p class=\"post-user\" style=\"display: none\">" + info.username + "</p>"+
            "            </div>" +
            "        </article>"
        );
    }else if(info.type === 'like'){
        const div = document.getElementById(info.id);
        const button = div.querySelectorAll("div.interact")[0].querySelectorAll(".button")[0];
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
        id: elem.parentNode.parentNode.parentNode.id,
        user: document.getElementById('main_username').innerText
    }));
}

function sendComment(elem){
    // console.log(document.getElementById('main_username').innerText);
    const input = elem.querySelector("#post-comment");
    const id = elem.parentNode.parentNode.parentNode.id;
    socket.send(JSON.stringify({
        type: "comment",
        id: id,
        body: input.value,
        user: document.getElementById('main_username').innerText
    }));
    input.value = ""
}

function friend(elem){
    const friend = elem.parentNode.parentNode.parentNode.querySelector('.post-user').innerText;
    const user = document.getElementById('main_username').innerText;
    console.log(elem.innerText);
    if(elem.innerText === 'Friend User'){
        const friendrequest = new XMLHttpRequest();
        friendrequest.onreadystatechange = function () {
            if(this.readyState === 4 && this.status === 200){
                console.log(this.response);
                if(this.response === 'added'){
                    const metas = document.getElementsByClassName('post-meta');
                    for(let i of metas){
                        if(i.querySelector('.post-user').innerText === friend){
                            i.parentNode.querySelector('.btn').innerText = 'Unfriend User';
                        }
                    }
                    elem.innerText = 'Unfriend User';
                }
            }
        };

        friendrequest.open("GET", "/blog/addfriend/" + user + '/' + friend + '/');
        friendrequest.send();
    }else{
        const unfriendrequest = new XMLHttpRequest();
        unfriendrequest.onreadystatechange = function () {
            if(this.readyState === 4 && this.status === 200){
                console.log(this.response);
                const metas = document.getElementsByClassName('post-meta');
                for(let i of metas){
                    if(i.querySelector('.post-user').innerText === friend){
                        i.parentNode.querySelector('.btn').innerText = 'Friend User';
                    }
                }
                if(this.response === 'removed'){
                    elem.innerText = 'Friend User';
                }
            }
        };

        unfriendrequest.open("GET", "/blog/removefriend/" + user + '/' + friend + '/');
        unfriendrequest.send();
    }
}