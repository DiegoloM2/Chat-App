const makeMainChat = async function (username) {


    let response = await fetch(`http://127.0.0.1:8000/chat/private/${username}/`)
    if (response.status === 200) {
        var data = await response.text()
        data = JSON.parse(data)

        document.querySelector("#selected-user-name").innerText = username;
        //delete chat-message-output innerHtml and add each message in turn
        let msgOutput = document.getElementById("chat-messages-output");
        msgOutput.innerHTML = '';
    
        data['messages'].forEach((message) => {
            
            if (message.sender == username) {
                received = true
                user = message.sender
                msgOutput.innerHTML += getMsgHtml(usernameParam=user, content = message.text, received = received, timeParam = message.created_at )
            }
    
            else {
                received = false
                user = message.sender
                msgOutput.innerHTML += getMsgHtml(usernameParam=user, content = message.text, received = received, timeParam = message.created_at )
            }
    
             
        })
    }




}

function getMsgHtml (usernameParam, content, received, imgPath = null, timeParam = null) {
        
    var now = new Date();
    let chatAvatar = `<div class="chat-avatar">
            <img src="{% static 'images/default-avatar.svg' %}" alt="avatarPic">
            <div class="chat-name">${usernameParam}</div>
        </div>`
    let chatHour = `<div class="chat-hour">${timeParam ? timeParam:now.getHours() + ":" + now.getMinutes()}<span class="fa "></span></div>`

    if (received) {
        let html = `
        <li class="chat-left">
            ${chatAvatar}
            <div class="chat-text">${content.replaceAll("\n", '<br/>')}</div>
            ${chatHour}    
        </li>`;
        return html;
    }
    else {
        let html = `
        <li class="chat-right">
            ${chatHour}
            <div class="chat-text">${content.replaceAll("\n", '<br/>')}</div>
            ${chatAvatar}    
        </li>`
        return html;
    }
}