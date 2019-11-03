from django.conf.urls import url
import inscription.views

urlpatterns = [
    url(r'^confirm/(?P<string>[\w\-]+)/$',
        inscription.views.confirmation, name="confirmation"),
    url(r'^payment/$',
        inscription.views.paymentView, name="paymentView"),
    url(r'^paylater/$',
        inscription.views.pay_later, name="pay_later"),
    url(r'^thanks/$',
        inscription.views.thanks, name="thanks_view"),
    url(r'^$',
        inscription.views.register, name="register"),
]
