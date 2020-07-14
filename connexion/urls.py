from django.conf.urls import url

import connexion.views

urlpatterns = [
    url(r'^$', connexion.views.connexion, name="connect_home"),
]
