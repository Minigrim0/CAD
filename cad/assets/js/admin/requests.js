/**
 * Shows a confirmation modal to confirm the coach selection
 * @param {int} coach_pk the pk of the selected coach
 * @param {int} id the id of the request
 */
function showconfirmationmodal(coach_pk, id) {
    $('#Detail' + coach_pk + '_' + id).modal('show');
    $('#tobechosen_' + coach_pk + id).css('display', 'block');
}

/**
 * Shows details obout a coach
 * @param {int} coach_pk the pk of the coach
 * @param {int} id the id of the student request
 */
function showdetailmodal(coach_pk, id){
    $('#Detail' + coach_pk + '_' + id).modal('show');
    $('#tobechosen_' + coach_pk + id).css('display', 'none');
}

/**
 * Creates a temporary alert
 * @param {string} parent the id of the parent DOM element
 * @param {string} level the type of the alert (danger, warning, success)
 * @param {int} time the duration of the alert
 * @param {str} message the message inside the alert
 * @param {int} id the id of the alert
 * @param {callback} callback the function to call once the aert is closed
 * @param {list} args the arguments for the callback
 */
function createTempAlert(parent, level, time, message, id, callback=null, args=[]){
    $(parent).append($('<div class="alert alert-' + level + ' fade show" role="alert" id="notif_' + id + '">\
        ' + message + '\
    </div>'));

    setTimeout(function(){
        $("#notif_" + id).alert('close');
        if(callback !== null){
            callback(args);
        }
    }, time);
}

/**
 * Deletes a list of divs
 * @param {list} divs the list of the divs' ids
 */
function deleteDiv(divs=[]){
    for(var x=0;x<divs.length; x++){  // skipcq JS-0502
        $(divs[x]).detach();
    }
}

/**
 * Updates the page, deleting the request from opened and showing it in closed
 * @param {int} id the id of the student request
 */
function updateRequestDisplay(id){
    var infoUrl = RequestInformationUrl + "?id=" + id;  // skipcq JS-0502
    $.get(
        infoUrl
    ).done(
        function(data) {
            $("#closed_request_" + id).empty();
            createTempAlert("#closed_request_" + id, "success", 5000, "Le coach a bien été choisi", id, deleteDiv, ["#closed_request_" + id]);

            var closedList = document.getElementById("ClosedRequestsList");  // skipcq JS-0502
            closedList.innerHTML = data["content"] + closedList.innerHTML;
        }
    ).fail(
        function() {
            $("#closed_request_" + id).empty();
            createTempAlert("#closed_request_" + id, "danger", 5000, "Une erreur est survenue lors de la récupération d'informations. Le coach à cependant pu être choisi", id, deleteDiv, ["#closed_request_" + id]);
        }
    )
}

/**
 * Allows the administration to choose the coach for a certain student request
 * @param {int} coach_pk the pk of the coach
 * @param {int} id the id of the student request
 */
function chooseCoach(coach_pk, id) {
    var finalschedule = $('#schedulefor' + coach_pk + id).val();  // skipcq JS-0502
    if(finalschedule == ""){
        $('#errorschedule' + coach_pk + id).text("Ce champ est obligatoire");
        $('#errorschedule' + coach_pk + id).css("display", "block");
        return;
    }

    document.getElementById("coaches_" + id).style = "filter: opacity(10%);";
    document.getElementById("spin_" + id).style.display = "block";

    $.post(
        SelectCoachUrl, {
            id: id,
            coach: coach_pk,
            schedule: finalschedule,
            csrfmiddlewaretoken: csrfToken
        },
        function(data, status) {
            if (status == "success") {
                updateRequestDisplay(id);
            } else {
                document.getElementById("coaches_" + id).style = "filter: opacity(0%);";
            }
        }
    );

    $('#Detail' + coach_pk + '_' + id).modal('hide');
}

/**
 * Switch between opened and closed student requests
 * @param {str} to the panel to switch to
 */
function switchTo(to){
    if (to == "open"){
        document.getElementById("Open").style.display = 'block';
        document.getElementById("Closed").style.display = 'none';
        document.getElementById("tab-close").classList.remove("active");
        document.getElementById("tab-open").classList.add("active");
    }
    else if (to == "close"){
        document.getElementById("Open").style.display = 'none';
        document.getElementById("Closed").style.display = 'block';
        document.getElementById("tab-close").classList.add("active");
        document.getElementById("tab-open").classList.remove("active");
    }
}
