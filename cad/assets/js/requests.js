//Makes a request to remove the notification with the specified ID
//Has to be an id related to the current user's notification
function acceptRequest(id, decision, coach) {
  schedule = document.getElementById("coach_schedule").value;
  document.getElementById("error_schedule").innerHTML = "";
  if (decision == "true") {
    if (schedule == "") {
      document.getElementById("error_schedule").innerHTML =
        "Vous devez renseigner ces informations pour pouvoir accepter la requête";
      return;
    }
  }

  $.post(
    Url,
    {
      id: id,
      decision: decision,
      schedule: schedule,
      coach: coach,
      csrfmiddlewaretoken: csrfToken,
    },
    function (data, status) {
      if (status == "success") {
        document.getElementById("buttons").style.display = "none";
        document.getElementById("dejarepondu").innerHTML =
          '<p style="color:red;">Merci d\'avoir répondu à cette requête</p>';
      } else {
        document.getElementById("dejarepondu").innerHTML =
          '<p style="color:red;">Une erreur est survenue, veuillez réessayer plus tard</p>';
      }
    }
  );
}
