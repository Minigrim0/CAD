function del_notif(notif_id) {
  $.post(
    UrlNotif,
    {
      id: notif_id,
      csrfmiddlewaretoken: csrf_token,
    },
    function (data, status) {
      if (status == "success") {
        console.log("request successfully sent");
      } else {
        console.log("request failed...");
      }
    }
  );
  document.getElementById("msg" + notif_id).style.display = "none";
}
