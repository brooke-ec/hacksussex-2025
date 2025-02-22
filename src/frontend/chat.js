function sendNewMessage(name, message){
    if (message == ""){
        return;
    }
    //Call Python code here
    document.getElementById("message").value = "";
    addNewMessage(name, message)
}
function addNewMessage(name, message){
    let temp = document.getElementsByTagName("template")[0];
    let clon = temp.content.cloneNode(true);
    clon.querySelector("h3").innerText = name;
    clon.querySelector(".messageTextBox").innerText = message;
    document.querySelector(".chatBorder").appendChild(clon)
    window.scrollTo(0, document.body.scrollHeight);
}
window.addEventListener("load", function(){
    addNewMessage("Bob", "No >:(")
    addNewMessage("Bob", "No >:(")
    addNewMessage("Bob", "No >:(")
    addNewMessage("Bob", "No >:(")
})