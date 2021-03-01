from django.urls import path
from django.conf.urls import include

import administration.views as views


urlpatterns = [
    path("", views.adminPage, name="home_admin"),
    path("users/", views.user_admin_view, name="user_admin_view"),
    path("users/all/", views.user_list, name="userlist"),
    path("users/transaction/", views.transactions, name="transactions"),
    path("requests/", views.student_requests, name="requests_admin"),
    path("articles/", views.articleAdminView, name="articles_admin"),
    path("mails/", views.mailAdminView, name="mails_admin"),
    path("mails/create/", views.mailAdminCreate, name="createMail"),
    path("courses/", views.courses, name="given_courses"),
    path("messages/", views.message_admin_view, name="message_admin_view"),
    path("messages/all/", views.message_list, name="messagelist"),
    path("api/", include("administration.api_urls", namespace="api")),
]
