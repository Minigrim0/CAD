from django.conf.urls import url
from .autocomplete import UserAutocomplete
import users.views as views


urlpatterns = [
    url('^disconnect/$', views.disconnect, name="disconnect_view"),
    url('^remove_notif/$', views.remove_notif, name="rm_notif"),
    url('^modify_balance/$', views.modify_balance, name="modify_balance"),
    url('^send_notif/$', views.send_notif, name="send_notif"),
    url('^me/follow/$', views.followView, name="follow_up"),
    url('^me/students/$', views.studentsView, name="my_students"),
    url('^me/$', views.userView, name="my_account"),
    url('^choose/$', views.chooseCoach),
    url('^manage_requests/$', views.requestManage, name="manage_request"),
    url('^requests/<int:id>/$', views.requestView),
    url('^requests/$', views.requestView),
    url('^error/$', views.ErrorView, name="Error_view"),
    url('^user-autocomplete/$', UserAutocomplete.as_view(), name='user-autocomplete'),
    url('^login$', views.login_view, name="login_view"),
    url('^usermail$', views.get_users, name="get_users_mail"),
]
