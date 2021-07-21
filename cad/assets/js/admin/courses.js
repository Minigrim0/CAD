function approveCourse(pk, approved){
    if(!approved && !confirm("Êtes vous sûr de vouloir supprimer ce cours ?")) return;

    var alert_type;
    var alert_text = "default-alert";  // skipcq JS-0502
    var alert_id;

    $.post(
        approveCourseUrl,
        {
            pk: pk,
            csrfmiddlewaretoken: csrfToken,
            isApproved: approved
        }
    ).done(function(data){
        if(approved){
            $("#approved_" + pk).html('<img src="/static/admin/img/icon-yes.svg" alt="True"/>');
            alert_type = "alert-success";
            alert_text = "Ce cours a bien été approuvé.";
            alert_id = "notif_" + pk;
        } else {
            $("#approved_" + pk).html('<img src="/static/admin/img/icon-no.svg" alt="True"/>');
            alert_type = "alert-danger";
            alert_text = "Ce cours a bien été supprimé.";
            alert_id = "notif_" + pk;
        }

        createNotif(alert_id, alert_type, alert_text);
    }).fail(function(data){
        alert_type = "alert-danger";
        alert_text = "Ce cours n'a pas pu être approuvé. Réessayez plus tard !";
        alert_id = "notiffail_" + pk;

        createNotif(alert_id, alert_type, alert_text);
    });
}


function createNotif(alert_id, alert_type, alert_text){
    var new_notif = $("#notification_template").clone().children()[0];  // skipcq JS-0502
    new_notif.setAttribute("id", alert_id);
    new_notif.classList.add(alert_type)
    new_notif.children[1].innerText = alert_text;
    $("#notification_div").append(new_notif);

    setTimeout(function(){
        $("#" + alert_id).alert('close');
    }, 5000);
}
