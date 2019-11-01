from django.conf.urls import url
import administration.views

urlpatterns = [
    url(r'^$', administration.views.adminPage),
    url(r'users/(?P<string>[\w\-]+)/', administration.views.userAdminView),
    url(r'users/', administration.views.userAdminView),
    url(r'articles/modify/', administration.views.articleAdminModify),
    url(r'articles/', administration.views.articleAdminView),
    url(r'mails/modify/', administration.views.mailAdminModify),
    url(r'mails/create/', administration.views.mailAdminCreate),
    url(r'mails/', administration.views.mailAdminView),
    url(r'modify/', administration.views.modifyUser),
    url(r'reactivate/(?P<string>[\w\-]+)/', administration.views.reactivate),
]
