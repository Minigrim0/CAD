from django.urls import path

import users.api_endpoints as api


app_name = "users"
urlpatterns = [
    path("usermail/", api.get_users, name="get_users_mail"),
    path("notif/send/", api.send_notif, name="send_notif"),
    path("notif/del/", api.remove_notif, name="rm_notif"),
    path("requests/accept/", api.acceptRequest, name="manage_request"),
]
