from django.urls import path

import inscription.views

urlpatterns = [
    path("confirm/", inscription.views.confirmation_view, name="confirmation"),
    path("payment/", inscription.views.paymentView, name="paymentView"),
    path("paylater/", inscription.views.pay_later, name="pay_later"),
    path("thanks/", inscription.views.thanks, name="thanks_view"),
    path("student/", inscription.views.registerUserView, name="registerUser"),
    path("", inscription.views.registerUserView, name="registerStudentDefault"),
]
