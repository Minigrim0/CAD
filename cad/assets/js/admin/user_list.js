$(document).ready(
    function(){
        var url = new URL(document.location);  // skipcq JS-0502
        value = document.getElementById('searchbar').value = url.searchParams.get('q');

        var input = document.getElementById("searchbar");  // skipcq JS-0502
        input.addEventListener("keyup", function(event) {
            if (event.keyCode === 13) { // Enter
                event.preventDefault();
                document.getElementById("searchbutton").click();
            }
        })
    }
)

/**
 * Activate or deactivate a user
 * @param {int} user_id the id of the user to (de)activate
 * @param {bool} active whether the user should be activated or not
 */
function activate(user_id, active){
    var Url = ActivateUserUrl + "?userid=" + user_id + "&active=" + active;  // skipcq JS-0502
    var message = "Voulez vous réellement ";  // skipcq JS-0502
    message += active == "true" ? "réactiver cet utilisateur ?" : "désactiver cet utilisateur ?";

    if(!confirm(message)) {
        return
    }
    
    $.post(
        Url, {
            csrfmiddlewaretoken: csrf_token
        },
        function(data, status) {
            if (status == "success") {
                status = document.getElementById("status_" + user_id);
                button = document.getElementById("activationbutton_" + user_id);
                if (active == "true"){
                    status.innerHTML = '<i class="fas fa-user-check"></i>';
                    button.setAttribute("onClick", "activate('" + user_id + "', 'false')");
                } else {
                    status.innerHTML = '<i class="fas fa-user-slash"></i>';
                    button.setAttribute("onClick", "activate('" + user_id + "', 'true')");
                }
            } else {
                unsubButton = document.getElementById("unsubbutton");
                unsubButton.innerHTML = '<p style="color:red;">La requête n\'a pas abouti, réessayez plus tard</p>';
            }
        }
    );
}

/**
 * Modifies the target url to search for what the user put in the search field
 */
function doSearch(){
    var url = new URL(document.location);  // skipcq JS-0502
    value = document.getElementById('searchbar').value;
    url.searchParams.set('q', value);
    value = document.getElementById('searchbutton').href = url;
}
