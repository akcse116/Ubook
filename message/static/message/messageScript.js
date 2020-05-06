window.addEventListener('DOMContentLoaded', wsHanshake, false);

let socket = '';

function wsHanshake(){
    const userId = document.getElementById('userId').innerText;

    if(userId){
        socket = new WebSocket('ws://' + window.location.host + '/ws/message/' +
            userId + '/');

        socket.onmessage = function (e) {
            console.log(e.data);
            const data = JSON.parse(e.data);
            if(!data.hasOwnProperty('error')){
                const currentId = document.getElementById('currentId').innerText;
                console.log(currentId);
                console.log(data.sender);
                if(data.sender === userId){
                    document.getElementById("messageLog").innerHTML += "<div class=\"yourMessage\">"+ data.message + "</div>"
                }else if (data.sender === currentId){
                    document.getElementById("messageLog").innerHTML += "<div class=\"otherMessage\">"+ data.message + "</div>"
                    socket.send(JSON.stringify({
                        'type': 'seen',
                        'sender': data.sender,
                        'recipient': userId
                    }))
                }else{
                    document.getElementById("notificationcontent").innerHTML += (
                        "<div class=\"note\">\n" +
                        "                <p class=\"notifuser\">" + data.sender + "</p>" +
                            "<b>" +  data.fullname + "</b>" +  ": " + data.message +
                        "</div>"
                    )
                }
            }else{
                alert(data.error);
            }
        };

        socket.onopen = function (e) {
            console.log("connected")
        };
    }
}

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
        'type': 'message',
        'sender': document.getElementById('userId').innerText,
        'recipient': document.getElementById('currentId').innerText,
        'message': val
    }));
}

function switchConvo(event){
    
    let idtracker = document.getElementById('currentId');
    if(event.className !== 'histLogsHighlighted'){
        const userswitch = new XMLHttpRequest();
        userswitch.onreadystatechange = function () {
            if(this.readyState === 4 && this.status === 200){
                console.log(JSON.parse(this.response));
                const newlog = JSON.parse(this.response);
                if(newlog){
                    document.getElementsByClassName('histLogsHighlighted')[0].className = 'histLogs';
                    event.className = 'histLogsHighlighted';
                    idtracker.innerText = event.id;
                    const log = document.getElementById("messageLog");
                    log.innerHTML = '';
                    console.log(idtracker.innerText);
                    for(let i of newlog){
                        if(String(i[0]) === event.id){
                            log.innerHTML += (
                                "<div class=\"otherMessage\">" + i[1] + "</div>"
                            );
                        }else{
                            log.innerHTML += (
                                "<div class=\"yourMessage\">" + i[1] + "</div>"
                            );
                        }
                    }
                    const notes = document.getElementsByClassName('note');
                    const notifications = document.getElementById('notificationcontent');
                    console.log(notes.length);
                    let newnotif = '';
                    for(let i of notes){
                        const user = i.querySelector('.notifuser').innerText;
                        console.log(user);
                        console.log(idtracker.innerText);
                        if(user !== idtracker.innerText){
                            newnotif += i.outerHTML;
                        }
                    }
                    notifications.innerHTML = newnotif;
                }
            }
        };

        const url = '/message/room/' + event.id + '/';
        userswitch.open('GET', url);
        userswitch.send()
    }



}
function startConvo(event) {
    var startChatElem = document.getElementById("startChat");
    console.log(startChatElem.value)
    // const url = '/message/room/' + friend + '/';
    // userswitch.open('GET', url);
    // userswitch.send()  
}



/**
 * User logout function sends a GET request to server.
 * Server clears session. On response refreshes page.
 *
 */
function logout_user() {
    let logout_request = new XMLHttpRequest();
    logout_request.onreadystatechange = function(){
        if	(this.readyState	===	4	&&	this.status	===	200){
            window.location.replace("/");
        }
    };
    logout_request.open("GET", "/login/logout/");
    logout_request.send();
}