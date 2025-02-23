function sendNewMessage(name, message){
    if (message == ""){
        return;
    }
    window.pywebview.api.send(name, message);
    document.getElementById("message").value = "";
    addNewMessage(name, message);
}
function addNewMessage(name, message){
    colour = name.toString(16);
    console.log(colour);
    let temp = document.getElementsByTagName("template")[0];
    let clon = temp.content.cloneNode(true);
    clon.querySelector("h3").innerText = name;
    clon.querySelector(".messageTextBox").innerText = message;
    clon.querySelector(".userIconThing").style.background = colour;
    document.querySelector(".chatBorder").appendChild(clon);
    window.scrollTo(0, document.body.scrollHeight);
}
window.addEventListener("load", function(){
    addNewMessage("Communiko Team", "Welcome to Communiko, a lovely messaging platform that uses Pico Ws to send messages via bluetooth!");
})