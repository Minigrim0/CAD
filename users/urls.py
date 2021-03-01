from django.urls import path
from users.autocomplete import CoachAutocomplete
import users.views as views


urlpatterns = [
    path("", views.user_home, name="user_home"),
    path("disconnect/", views.disconnect, name="disconnect_view"),
    path("remove_notif/", views.remove_notif, name="rm_notif"),
    path("send_notif/", views.send_notif, name="send_notif"),
    path("me/follow/", views.followView, name="follow_up"),
    path("me/students/", views.studentsView, name="my_students"),
    path("me/students/add/", views.addFollowElement, name="add_follow"),
    path("me/", views.userView, name="my_account"),
    path("requests/", views.requestView, name="request_view"),
    path("requests/accept/", views.acceptRequest, name="manage_request"),
    path("user-autocomplete/", CoachAutocomplete.as_view(), name="coach-autocomplete"),
    path("login/", views.login_view, name="login_view"),
    path("usermail/", views.get_users, name="get_users_mail"),
]
