//Makes a request to create a notification for a specified user
function getUsers() {
    email = document.getElementById("email_input").value;

    $.post(
        MailCheckUrl, {
            email: email,
            csrfmiddlewaretoken: csrf_token
        },
        function(data, status) {
            if (status == "success") {
                console.log(data);
            } else {
                console.log("error");
            }
        }
    );
}
