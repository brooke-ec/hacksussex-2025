function storeNameandRedirect(name){
    if (name == ""){
        return;
    }
    localStorage.setItem("name", name)
    window.location.replace("/chat.html")
}