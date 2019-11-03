from django.conf.urls import url
import connexion.views


urlpatterns = [
    url(r'^connect/$', connexion.views.connect, name="connect"),
    url(r'^$', connexion.views.connexion, name="connect_home"),
]
