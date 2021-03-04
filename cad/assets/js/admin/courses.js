function approveCourse(pk, approved){
    if(!approved && !confirm("Êtes vous sûr de vouloir supprimer ce cours ?")) return;

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
            $("#notification_div").html(
                $("#notification_div").html() +
                '<div class="alert alert-success fade show" role="alert" id="notif_' + pk + '">\
                    Ce cours a bien été approuvé.\
                </div>'
            );
        } else {
            $("#approved_" + pk).html('<img src="/static/admin/img/icon-no.svg" alt="True"/>');
            $("#notification_div").html(
                $("#notification_div").html() +
                '<div class="alert alert-danger fade show" role="alert" id="notif_' + pk + '">\
                    Ce cours a bien été supprimé.\
                </div>'
            );
        }
        setTimeout(function(){
            $("#notif_" + pk).alert('close');
        }, 3000);
    }).fail(function(data){
        $("#notification_div").html(
            $("#notification_div").html() +
            '<div class="alert alert-danger fade show" role="alert" id="notiffail_' + pk + '">\
                Ce cours n\'a pas pu être approuvé. Réessayez plus tard !\
            </div>'
        );
        setTimeout(function(){
            $("#notiffail_" + pk).alert('close');
        }, 5000);
    });
}