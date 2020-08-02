from django.conf.urls import url

import administration.views

urlpatterns = [
    url(r'^$', administration.views.adminPage, name="home_admin"),
    url(r'users/(?P<string>[\w\-]+)/', administration.views.userAdminView),
    url(r'users/', administration.views.userAdminView, name="user_admin"),
    url(r'articles/',
        administration.views.articleAdminView, name="articles_admin"),
    url(r'mails/create/', administration.views.mailAdminCreate, name="createMail"),
    url(r'mails/', administration.views.mailAdminView, name="mails_admin"),
    url(r'courses/', administration.views.courses, name="given_courses"),
    url(r'modify/', administration.views.modifyUser),
    url(r'reactivate/(?P<string>[\w\-]+)/', administration.views.reactivate, name="reactivate_user"),
    url(r'unsubscribe/',
        administration.views.sendUnsubscriptionMail, name="unsubscribe"),
]
