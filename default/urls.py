from django.conf.urls import url
import default.views

urlpatterns = [
    url(r'^$',         default.views.home),
    url(r'contact/',   default.views.contactView),
]
