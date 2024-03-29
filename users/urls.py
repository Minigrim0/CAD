from django.urls import path
from users.autocomplete import CoachAutocomplete
import users.views as views


urlpatterns = [
    path("", views.user_home, name="user_home"),
    path("disconnect/", views.disconnect, name="disconnect_view"),
    path("me/follow/", views.followView, name="follow_up"),
    path("me/students/", views.studentsView, name="my_students"),
    path("me/students/add/", views.addFollowElement, name="add_follow"),
    path("me/", views.userView, name="my_account"),
    path("requests/", views.requestView, name="request_view"),
    path("user-autocomplete/", CoachAutocomplete.as_view(), name="coach-autocomplete"),
    path("login/", views.login_view, name="login_view"),
    path("mail/resend", views.send_confirmation_email, name="resend_confirm_mail"),
]
