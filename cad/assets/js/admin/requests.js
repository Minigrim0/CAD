function showconfirmationmodal(coach_pk, id) {
  $("#Detail" + coach_pk + "_" + id).modal("show");
  $("#tobechosen_" + coach_pk + id).css("display", "block");
}

function showdetailmodal(coach_pk, id) {
  $("#Detail" + coach_pk + "_" + id).modal("show");
  $("#tobechosen_" + coach_pk + id).css("display", "none");
}

function createTempAlert(
  parent,
  level,
  time,
  message,
  id,
  callback = null,
  args = []
) {
  $(parent).append(
    $(
      '<div class="alert alert-' +
        level +
        ' fade show" role="alert" id="notif_' +
        id +
        '">\
        ' +
        message +
        "\
    </div>"
    )
  );

  setTimeout(function () {
    $("#notif_" + id).alert("close");
    if (callback !== null) {
      callback(args);
    }
  }, time);
}

function deleteDiv(divs = []) {
  for (var x = 0; x < divs.length; x++) {
    $(divs[x]).detach();
  }
}

function updateRequestDisplay(id) {
  var infoUrl = RequestInformationUrl + "?id=" + id;
  $.get(infoUrl)
    .done(function (data) {
      $("#closed_request_" + id).empty();
      createTempAlert(
        "#closed_request_" + id,
        "success",
        5000,
        "Le coach a bien été choisi",
        id,
        deleteDiv,
        ["#closed_request_" + id]
      );

      var closedList = document.getElementById("ClosedRequestsList");
      closedList.innerHTML = data["content"] + closedList.innerHTML;
    })
    .fail(function () {
      $("#closed_request_" + id).empty();
      createTempAlert(
        "#closed_request_" + id,
        "danger",
        5000,
        "Une erreur est survenue lors de la récupération d'informations. Le coach à cependant pu être choisi",
        id,
        deleteDiv,
        ["#closed_request_" + id]
      );
    });
}

function chooseCoach(coach_pk, id) {
  var finalschedule = $("#schedulefor" + coach_pk + id).val();
  if (finalschedule == "") {
    $("#errorschedule" + coach_pk + id).text("Ce champ est obligatoire");
    $("#errorschedule" + coach_pk + id).css("display", "block");
    return;
  }

  document.getElementById("coaches_" + id).style = "filter: opacity(10%);";
  document.getElementById("spin_" + id).style.display = "block";

  $.post(
    SelectCoachUrl,
    {
      id: id,
      coach: coach_pk,
      schedule: finalschedule,
      csrfmiddlewaretoken: csrfToken,
    },
    function (data, status) {
      if (status == "success") {
        updateRequestDisplay(id);
      } else {
        document.getElementById("coaches_" + id).style = "filter: opacity(0%);";
      }
    }
  );

  $("#Detail" + coach_pk + "_" + id).modal("hide");
}

function switchTo(to) {
  if (to == "open") {
    document.getElementById("Open").style.display = "block";
    document.getElementById("Closed").style.display = "none";
    document.getElementById("tab-close").classList.remove("active");
    document.getElementById("tab-open").classList.add("active");
  } else if (to == "close") {
    document.getElementById("Open").style.display = "none";
    document.getElementById("Closed").style.display = "block";
    document.getElementById("tab-close").classList.add("active");
    document.getElementById("tab-open").classList.remove("active");
  }
}
