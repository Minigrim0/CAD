function copyKey() {
    /* Get the text field */
    var copyText = document.getElementById("id_secret_key");

    /* Select the text field */
    copyText.select();
    copyText.setSelectionRange(0, 99999); /*For mobile devices*/

    /* Copy the text inside the text field */
    document.execCommand("copy");

    /* Alert the copied text */

    var copyText = document.getElementById("buttoncopy");
    copyText.innerHTML = "copié!";
}


//Makes a request to create a notification for a specified user
function sendNotif(_user) {
    _title = document.getElementById("notifTitle").value;
    _content = document.getElementById("notifContent").value;
    _sender = document.getElementById("notifSender").value;

    $.post(
        UrlNotif, {
            title: _title,
            content: _content,
            sender: _sender,
            user: _user,

            csrfmiddlewaretoken: csrf_token
        },
        function(data, status) {
            if (status == "success") {
                document.getElementById("successSend").style.display = "block";
                var IntervalID = setInterval(
                    function() {
                        document.getElementById("successSend").style.display = "none";
                        $('#SendNotif').modal('toggle')
                        clearInterval(IntervalID);
                    }, 1500);
            } else {
                document.getElementById("errorSend").style.display = "block";
                var IntervalID = setInterval(
                    function() {
                        document.getElementById("errorSend").style.display = "none";
                        $('#SendNotif').modal('toggle')
                        clearInterval(IntervalID);
                    }, 1500);
            }
        }
    );
}


function updBalance(user, admin) {
    amout_add = document.getElementById("new_balance").value;
    isFirst = document.getElementById("isFirstPayment").checked;

    $.post(
        UrlBalance, {
            amout_add: +amout_add,
            isFirstPayment: isFirst,
            approver: admin,
            user: user,
            csrfmiddlewaretoken: csrf_token
        },
        function(data, status) {
            if (status == "success") {
                document.getElementById("successBalance").style.display = "block";
                document.getElementById("id_balance").value = data["new_balance"];
                var IntervalID = setInterval(
                    function() {
                        document.getElementById("successBalance").style.display = "none";
                        $('#UpdateBalance').modal('toggle')
                        clearInterval(IntervalID);
                    }, 1500);
            } else {
                document.getElementById("errorBalance").style.display = "block";
                var IntervalID = setInterval(
                    function() {
                        document.getElementById("errorBalance").style.display = "none";
                        $('#UpdateBalance').modal('toggle')
                        clearInterval(IntervalID);
                    }, 1500);
            }
        }
    );
}


function unsub(user_key){
    $.post(
        UrlUnsub, {
            user_key: user_key,
            csrfmiddlewaretoken: csrf_token
        },
        function(data, status) {
            console.log(status);
            if (status == "success") {
                unsubButton = document.getElementById("unsubbutton");
                unsubButton.innerHTML = '<p style="color:red;">Proposition de désinscription envoyée</p>';
            } else {
                unsubButton = document.getElementById("unsubbutton");
                unsubButton.innerHTML = '<p style="color:red;">La requête n\'a pas abouti, réessayez plus tard</p>';
            }
        }
    );
}


function reloadCoach(){
    if(!confirm("Êtes vous sûr de vouloir relancer une recherche ?")) return;

    id = Math.floor(Math.random() * 100);

    $.post(
        new_coach_url,
        {
            user: user,
            csrfmiddlewaretoken: csrf_token,
        }
    ).done(function(data){
        if(data['accepted']){
            $("#notification_div").html(
                $("#notification_div").html() +
                '<div class="alert alert-success alert-dismissible fade show m-2" role="alert" id="notif_' + id + '">\
                    Une nouvelle requete a bien ete creee.\
                </div>'
            );
        } else {
            $("#notification_div").html(
                $("#notification_div").html() +
                '<div class="alert alert-danger alert-dismissible fade show m-2" role="alert" id="notif_' + id + '">\
                    La requete n\'a pas pu etre creee. Raison : ' + data['reason'] + '.\
                </div>'
            );
        }
        setTimeout(function(){
            $("#notif_" + id).alert('close');
        }, 3000);
    }).fail(function(data){
        $("#notification_div").html(
            $("#notification_div").html() +
            '<div class="alert alert-danger alert-dismissible fade show m-2" role="alert" id="notiffail_' + id + '">\
                La requete n\'a pas pu etre creee ! Essayez a nouveau plus tard\
            </div>'
        );
        setTimeout(function(){
            $("#notiffail_" + id).alert('close');
        }, 5000);
    });
}


function updCoach(){
    if(!$("#newCoachForm").valid()){
        $("#id_coach-error").css("display", "none");
        $("#errorNewCoachForm").css("display", "block");
        return;
    }
    $("#errorNewCoachForm").css("display", "none");
    var dataArray = $("#newCoachForm").serializeArray();

    var post_data = {
        csrfmiddlewaretoken: csrf_token,
        student: user
    }

    for(var x = 0;x<dataArray.length;x++){
        post_data[dataArray[x]["name"]] = dataArray[x]["value"];
    }

    $.post(newCoachUrl, post_data).done(
        function(data) {
            $(".coach_readonly").val(data["coach_name"]);
            $("#successNewCoach").css("display", "block");
            setTimeout(function(){
                $("#chooseCoach").modal('hide');
                $("#successNewCoach").css("display", "none");
            }, 1500);
        }
    ).fail(
        function() {
            $("#errorNewCoach").css("display", "block");
            setTimeout(function(){
                $("#errorNewCoach").css("display", "none");
            }, 5000);
        }
    );
}
