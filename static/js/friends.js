document.querySelector(".btn-show-friend-request-form").onclick = function (e) {
    let friendRequestForm = document.getElementById("friend-request-form");
    if (friendRequestForm.style.display === "none") {
        this.textContent = "Hide Friend Request Form";
        friendRequestForm.style.display = "block";
    }
    else {
        this.textContent = "Add a friend";
        friendRequestForm.style.display = "none";
    }
}

document.getElementById("friend-request-form").onsubmit = function (e) {
    let fRequestForm = this;
    e.preventDefault();
    let formData = new FormData();
    const receiver = document.getElementById("input-receiver").value
    formData.append("receiver",receiver);
    formData.append("csrfmiddlewaretoken", document.querySelector("input[name=csrfmiddlewaretoken]").value)
    
    const postInformation = {
        method:'post', 
        body:formData
    }

    fetch(fRequestForm.action, postInformation).then( function (response) {
        if (response.status === 201) {
            fRequestForm.style.display = "none";
            let succesfullyRequestedMsg = document.createElement("p");
            succesfullyRequestedMsg.textContent = `Succesfuly sent a friend request to ${receiver}`;
            succesfullyRequestedMsg.style = "animation:fadeout ease 5s;";
            document.querySelector("body").append(succesfullyRequestedMsg)
        }
        else if (response.status == 404) {
            let data = response.json();
            console.log(data)
            const error = `<p style = 'color:red;'>Please enter a valid username</p>`
            document.getElementById("input-receiver").insertAdjacentHTML('afterend',error);

        }
    })
    
}