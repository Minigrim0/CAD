function del_notif(notif_id) {
  $.post(
    UrlNotif,
    {
      id: notif_id,
      csrfmiddlewaretoken: csrf_token,
    },
    function (data, status) {
      if (status == "success") {
        // Add visual confirmation
      } else {
        // Add visual error
      }
    }
  );
  document.getElementById("msg" + notif_id).style.display = "none";
}
