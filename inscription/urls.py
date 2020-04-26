from django.conf.urls import url
import inscription.views

urlpatterns = [
    url('confirm/<slug:string>/',
        inscription.views.confirmation, name="confirmation"),
    url('payment/',
        inscription.views.paymentView, name="paymentView"),
    url('paylater/',
        inscription.views.pay_later, name="pay_later"),
    url('thanks/',
        inscription.views.thanks, name="thanks_view"),
    url('student/',
        inscription.views.registerStudentView, name="registerStudent"),
    url('coach/',
        inscription.views.registerCoachView, name="registerCoach"),
    url('',
        inscription.views.registerStudentView, name="registerStudentDefault"),
]
