from django.conf.urls import url
import inscription.views

urlpatterns = [
    url(r'^studentRegister/confirm/(?P<string>[\w\-]+)/$',
        inscription.views.confirmation),
    url(r'^payment/$',
        inscription.views.paymentView),
    url(r'^register/$',
        inscription.views.register),
    url(r'^connect/$',
        inscription.views.connect),
    url(r'^paylater/$',
        inscription.views.pay_later),
    url(r'^thanks/$',
        inscription.views.thanks),
    url(r'^$',
        inscription.views.connexion),
]
