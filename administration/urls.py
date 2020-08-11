from django.conf.urls import url

import administration.views as views

urlpatterns = [
    url('^$', views.adminPage, name="home_admin"),
    url('^test/$', views.test),
    url('^users/$', views.test, name="user_admin_view"),
    url('^users/all/$', views.user_list, name="userlist"),
    url('^users/modify/$', views.modifyUser, name="modify_user"),
    url('^users/activate/<slug:username>/$', views.reactivate, name="reactivate_user"),
    url('^users/unsubscribe/$', views.sendUnsubscriptionMail, name="unsubscribe"),
    url('^articles/$', views.articleAdminView, name="articles_admin"),
    url('^mails/$', views.mailAdminView, name="mails_admin"),
    url('^mails/create/$', views.mailAdminCreate, name="createMail"),
    url('^courses/$', views.courses, name="given_courses"),
    url('^transactions/$', views.transactions, name="transactions"),
]
