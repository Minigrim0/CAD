from django.conf.urls import url
from .autocomplete import UserAutocomplete
import users.views as views


urlpatterns = [
    url(r'disconnect', views.disconnect, name="disconnect_view"),
    url(r'remove_notif', views.remove_notif, name="rm_notif"),
    url(r'modify_balance', views.modify_balance, name="modify_balance"),
    url(r'send_notif', views.send_notif, name="send_notif"),
    url(r'me/follow', views.followView, name="follow_up"),
    url(r'me/students', views.studentsView, name="my_students"),
    url(r'me', views.userView, name="my_account"),
    url(r'choose', views.chooseCoach),
    url(r'manage_requests/', views.requestManage, name="manage_request"),
    url(r'requests/(?P<id>\d+)/', views.requestView),
    url(r'requests/', views.requestView),
    url(r'error/', views.ErrorView, name="Error_view"),
    url(r'^user-autocomplete/$', UserAutocomplete.as_view(), name='user-autocomplete'),
]
