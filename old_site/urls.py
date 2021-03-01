from django.urls import path

import old_site.views as views


urlpatterns = [
    path("<str:name>/", views.old, name="old_site"),
]
