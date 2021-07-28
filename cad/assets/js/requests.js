//Makes a request to remove the notification with the specified ID
//Has to be an id related to the current user's notification

/**
 * Accepts or denies the student request
 * @param {int} id the id of the request 
 * @param {boolean} decision the decision the user made
 * @param {string} coach the name of the coach who made the decision
 */
function acceptRequest(id, decision, coach) {
    schedule = document.getElementById("coach_schedule").value;
    document.getElementById("error_schedule").innerHTML = "";
    if (decision == "true") {
        if (schedule == "") {
            document.getElementById("error_schedule").innerHTML = "Vous devez renseigner ces informations pour pouvoir accepter la mission";
            return;
        }
    }

    $.post(
        Url, {
        id: id,
        decision: decision,
        schedule: schedule,
        coach: coach,
        csrfmiddlewaretoken: csrfToken,
    },
        function (data, status) {
            if (status == "success") {
                document.getElementById("buttons").style.display = "none";
                document.getElementById("dejarepondu").innerHTML = '<p style="color:red;">Merci d\'avoir répondu à cette mission</p>';
            } else {
                document.getElementById("dejarepondu").innerHTML = '<p style="color:red;">Une erreur est survenue, veuillez réessayer plus tard</p>';
            }
        }
    );
}
