function storeNameandRedirect(name){
    if (name == ""){
        return;
    }
    localStorage.setItem("name", name)
    window.location.replace("http://127.0.0.1:5500/chat.html")
}