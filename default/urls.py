from django.views.generic.base import TemplateView
from django.urls import path

import default.views

urlpatterns = [
    path("", default.views.home, name="home"),
    path("contact/", default.views.contactView, name="contact_view"),
    path("soon/", default.views.soon, name="soon_view"),
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
    ),
]
