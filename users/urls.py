from django.conf.urls import url
import users.views

urlpatterns = [
    url(r'modify',                users.views.modifyUser),
    url(r'disconnect',            users.views.disconnect),
    url(r'remove_notif',          users.views.remove_notif),
    url(r'send_notif',            users.views.send_notif),
    url(r'me/follow',             users.views.followView),
    url(r'me/students',           users.views.studentsView),
    url(r'me',                    users.views.userView),
    url(r'choose',                users.views.chooseCoach),
    url(r'manage_requests/',      users.views.requestManage),
    url(r'requests/(?P<id>\d+)/', users.views.requestView),
    url(r'requests/',             users.views.requestView),
]
