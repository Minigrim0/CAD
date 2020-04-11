from django.conf.urls import url
import default.views

urlpatterns = [
    url(r'^$', default.views.home, name="home"),
    url(r'contact/', default.views.contactView, name="contact_view"),
]
