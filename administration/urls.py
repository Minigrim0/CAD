from django.urls import path

import administration.views as views


urlpatterns = [
    path('', views.adminPage, name="home_admin"),
    path('users/', views.user_admin_view, name="user_admin_view"),
    path('users/all/', views.user_list, name="userlist"),
    path('users/activate/', views.activate, name="activate_user"),
    path('users/unsubscribe/', views.sendUnsubscriptionMail, name="unsubscribe"),
    path('users/transaction/add/', views.modify_balance, name="modify_balance"),
    path('users/transaction/', views.transactions, name="transactions"),
    path('requests/', views.student_requests, name="requests_admin"),
    path('requests/select/', views.chooseCoach, name="request_select_coach"),
    path('requests/create/', views.create_new_request, name="request_new_coach"),
    path('users/setcoach/', views.set_new_coach, name="set_new_coach"),
    path('articles/', views.articleAdminView, name="articles_admin"),
    path('mails/', views.mailAdminView, name="mails_admin"),
    path('mails/create/', views.mailAdminCreate, name="createMail"),
    path('courses/', views.courses, name="given_courses"),
    path('courses/approve/', views.approve_course, name="approve_course"),
    path('messages/', views.message_admin_view, name="message_admin_view"),
    path('messages/all/', views.message_list, name="messagelist"),
]
