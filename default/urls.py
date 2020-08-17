from django.views.generic.base import TemplateView
from django.conf.urls import url

import default.views

urlpatterns = [
    url('^$', default.views.home, name="home"),
    url('^contact/$', default.views.contactView, name="contact_view"),
    url('^soon/$', default.views.soon, name="soon_view"),
    url(
        "^robots.txt$",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
    ),
]
