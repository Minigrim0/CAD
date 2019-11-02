from django.conf.urls import url
import inscription.views

urlpatterns = [
    url(r'^register/confirm/(?P<string>[\w\-]+)/$',
        inscription.views.confirmation, name="confirmation"),
    url(r'^payment/$',
        inscription.views.paymentView, name="paymentView"),
    url(r'^register/$',
        inscription.views.register, name="register"),
    url(r'^connect/$',
        inscription.views.connect, name="connect"),
    url(r'^paylater/$',
        inscription.views.pay_later),
    url(r'^thanks/$',
        inscription.views.thanks),
    url(r'^$',
        inscription.views.connexion),
]
