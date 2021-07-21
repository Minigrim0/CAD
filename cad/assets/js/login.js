var id;

/**
 * Gets the user using the given email address, launching adequate animation afterwards
 */
function getUsers() {
    email = document.getElementById("email_input").value;

    $.post(
        MailCheckUrl, {
            email: email,
            csrfmiddlewaretoken: csrf_token
        },
        function(data, status) {
            if (status == "success") {
                if (data["users"].length == 1){
                    // There only is one user linked to this email address

                    document.getElementById("user_name").innerHTML = data["users"][0][0];
                    document.getElementById("username").value = data["users"][0][1];
                    document.getElementById("askmail").classList.add("bounceOutLeft");
                    id = setInterval(emailtopassword, 500);
                } else if (data["users"].length == 0) {
                    // There is no account linked to this email address

                    document.getElementById("mailerror").style.display = "block";
                    document.getElementById("askmail").classList.add("shake");
                    id = setInterval(delShake, 1000);
                } else {
                    // There is more than one account linked to this email address

                    document.getElementById("askmail").classList.add("bounceOutLeft");
                    document.getElementById("nbraccounts").innerHTML = data['users'].length;
                    
                    choose_div = document.getElementById("chooseAccount");
                    for(var user_id=0;user_id<data["users"].length;user_id++){  // skipcq JS-0502
                        choose_div.innerHTML += "<button class='btn btn-primary' onclick='chooseUser(\""
                        + data["users"][user_id][1] + "\", \"" + data["users"][user_id][0]
                        + "\")'>Se connecter en tant que " + data["users"][user_id][0] + "</button><br/>"
                    }
                    id = setInterval(emailtochoice, 500);
                }
            } else {
                // Add visual error
            }
        }
    );
}

/**
 * Lets the user choose which account hes wants to connect to
 * @param {string} username the username of the chosen account
 * @param {string} user_name the username of the chosen account
 */
function chooseUser(username, user_name){
    // Fill his username in the form field
    document.getElementById("user_name").innerHTML = user_name;
    document.getElementById("username").value = username;
    document.getElementById("chooseAccountContainer").classList.add("bounceOutLeft");
    id = setInterval(choicetopassword, 1000);
}

/**
 * Makes the transition animation from email to password
 */
function emailtopassword() {
    document.getElementById("askmail").style.display = "none";
    document.getElementById("formlogin").classList.add("bounceInRight");
    document.getElementById("formlogin").style.display = "block";
    clearInterval(id);
}

/**
 * Makes the transition animation from choice to password
 */
function choicetopassword() {
    document.getElementById("chooseAccountContainer").style.display = "none";
    document.getElementById("formlogin").classList.add("bounceInRight");
    document.getElementById("formlogin").style.display = "block";
    clearInterval(id);
}

/**
 * Makes the transition animation from email to choice
 */
function emailtochoice() {
    document.getElementById("askmail").style.display = "none";
    document.getElementById("chooseAccountContainer").classList.add("bounceInRight");
    document.getElementById("chooseAccountContainer").style.display = "block";
    clearInterval(id);
}

/**
 * Deletes the shake class to stop the animation
 */
function delShake(){
    document.getElementById("askmail").classList.remove("shake");
    clearInterval(id);
}
