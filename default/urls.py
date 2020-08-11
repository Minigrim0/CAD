from django.conf.urls import url

import default.views

urlpatterns = [
    url('^$', default.views.home, name="home"),
    url('^contact/$', default.views.contactView, name="contact_view"),
]
