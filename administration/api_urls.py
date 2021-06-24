from django.urls import path

import administration.api_endpoints as api


app_name = "api"
urlpatterns = [
    path("users/activate/", api.activate, name="activate_user"),
    path("users/unsubscribe/", api.sendUnsubscriptionMail, name="unsubscribe"),
    path("users/transaction/add/", api.modify_balance, name="modify_balance"),
    path("requests/select/", api.chooseCoach, name="request_select_coach"),
    path("requests/create/", api.create_new_request, name="request_new_coach"),
    path("users/setcoach/", api.set_new_coach, name="set_new_coach"),
    path("courses/approve/", api.approve_course, name="approve_course"),
    path("requests/details/", api.request_informations, name="request_details")
]
