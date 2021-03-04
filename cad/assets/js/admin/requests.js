function showconfirmationmodal(coach_pk, id){
    $('#Detail' + coach_pk + '_' + id).modal('show');
    $('#tobechosen_' + coach_pk + id).css('display', 'block');
}

function showdetailmodal(coach_pk, id){
    $('#Detail' + coach_pk + '_' + id).modal('show');
    $('#tobechosen_' + coach_pk + id).css('display', 'none');
}

function chooseCoach(coach_pk, id) {
    var finalschedule = $('#schedulefor' + coach_pk + id).val()
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
                document.getElementById("coaches_" + id).style = "filter: opacity(100%);";;
                document.getElementById("spin_" + id).style.display = "none";

                var cards = document.getElementsByClassName("card");
                for (var x = 0; x < cards.length; x++) {
                    if (cards[x].id == "card_" + id + "_" + coach_pk) {
                        cards[x].style = "filter: opacity(100%)";
                        cards[x].getElementsByClassName("choose")[0].style.display = "none";
                    } else if (cards[x].id.search("card_" + id + "_") != -1) {
                        cards[x].style = "filter: opacity(25%)";
                        cards[x].getElementsByClassName("choose")[0].style.display = "none";
                    }
                }
            } else {
                document.getElementById("coaches_" + id).style = "filter: opacity(0%);";
            }
        }
    );

    $('#Detail' + coach_pk + '_' + id).modal('hide');
}

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