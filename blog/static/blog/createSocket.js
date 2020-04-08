const socket = new WebSocket('ws://' + window.location.host + '/ws/blog');

socket.onmessage = function (e) {
    const info = JSON.parse(e.data);
    console.log(info);
    if(info.type === 'post'){
        let container = document.getElementsByClassName('posts')[0];
        let img = "";
        if(info.media){

        }
        container.innerHTML +=
            "<article class = \"post\" >"+
            "            <div class = \"post-content\">" +
            "                <div class =\"post-box\">" +
                                img +
                                info.body +
            "                </div>" +
            "                <div class=\"interact\">" +
            "                    <button class = \"button\" type=\"button\">" +
            "                        <i class =\"emoji\">&#128077;</i>" +
            "                    </button>" +
            "                    <form>" +
            "                        <label for = \"post-comment\">comment: </label>" +
            "                        <input id= \"post-comment\" type=\"text\" name=\"comment\">" +
            "                        <input type=\"submit\" value=\"comment\">" +
            "                    </form>" +
            "                </div>" +
            "            </div>" +
            "            <div class = \"post-meta\">" +
                            info.author +
            "                Published: " + info.date +
            "            </div>" +
            "        </article>"
    }else if(info.type === 'like'){
        const div = document.getElementById(info.id);
        const button = div.querySelectorAll("div.interact")[0].querySelectorAll("button")[0];
        console.log(button);
        if(info.status){
            button.style.backgroundColor = "blue";
        }else{
            button.style.backgroundColor = "white";
        }
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

    // const body = {
    //     text: input.get("post-body"),
    //     media: ""
    // };
    //
    // if(file.files[0] !== undefined){
    //     reader.onloadend = function () {
    //         body.media = JSON.stringify(reader.result);
    //
    //         socket.send(reader.result);
    //         textinput.value = "";
    //         file.value = "";
    //     };
    //
    //     reader.readAsArrayBuffer(file.files[0]);
    // }else{
    //     socket.send(JSON.stringify(body));
    //     textinput.value = "";
    //     file.value = "";
    // }
}

function sendLike(elem){
    socket.send(JSON.stringify({
        type: "like",
        id: elem.parentNode.parentNode.parentNode.id
    }));
}

function sendComment(){

}

