$(document).ready(function () {
  var url = new URL(document.location);
  value = document.getElementById("searchbar").value =
    url.searchParams.get("q");

  var input = document.getElementById("searchbar");
  input.addEventListener("keyup", function (event) {
    if (event.keyCode === 13) {
      // Enter
      event.preventDefault();
      document.getElementById("searchbutton").click();
    }
  });
});

function activate(user_id, active) {
  var Url = ActivateUserUrl + "?userid=" + user_id + "&active=" + active;
  var message = "Voulez vous réellement ";
  if (active == "true") {
    message += "réactiver cet utilisateur ?";
  } else {
    message += "désactiver cet utilisateur ?";
  }

  if (!confirm(message)) {
    return;
  }

  $.post(
    Url,
    {
      csrfmiddlewaretoken: csrf_token,
    },
    function (data, status) {
      if (status == "success") {
        status = document.getElementById("status_" + user_id);
        button = document.getElementById("activationbutton_" + user_id);
        if (active == "true") {
          status.innerHTML = '<i class="fas fa-user-check"></i>';
          button.setAttribute(
            "onClick",
            "activate('" + user_id + "', 'false')"
          );
        } else {
          status.innerHTML = '<i class="fas fa-user-slash"></i>';
          button.setAttribute("onClick", "activate('" + user_id + "', 'true')");
        }
      } else {
        unsubButton = document.getElementById("unsubbutton");
        unsubButton.innerHTML =
          '<p style="color:red;">La requête n\'a pas abouti, réessayez plus tard</p>';
      }
    }
  );
}

function doSearch() {
  var url = new URL(document.location);
  value = document.getElementById("searchbar").value;
  url.searchParams.set("q", value);
  value = document.getElementById("searchbutton").href = url;
}
