from django.conf.urls import url
import administration.views

urlpatterns = [
    url(r'^$',         administration.views.adminPage),
    url(r'modify',     administration.views.modifyUser),
    url(r'reactivate/(?P<string>[\w\-]+)/', administration.views.reactivate),
]
