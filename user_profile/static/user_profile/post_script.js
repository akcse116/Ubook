function send_followup(input_text){
    socket.send(JSON.stringify(input_text));
}