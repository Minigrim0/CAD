from django.conf.urls import url
import users.views

urlpatterns = [
    url(r'disconnect', users.views.disconnect, name="disconnect_view"),
    url(r'remove_notif', users.views.remove_notif, name="rm_notif"),
    url(r'modify_balance', users.views.modify_balance, name="modify_balance"),
    url(r'send_notif', users.views.send_notif, name="send_notif"),
    url(r'me/follow', users.views.followView, name="follow_up"),
    url(r'me/students', users.views.studentsView, name="my_students"),
    url(r'me', users.views.userView, name="my_account"),
    url(r'choose', users.views.chooseCoach),
    url(r'manage_requests/', users.views.requestManage, name="manage_request"),
    url(r'requests/(?P<id>\d+)/', users.views.requestView),
    url(r'requests/', users.views.requestView),
    url(r'error/', users.views.ErrorView, name="Error_view"),
]
