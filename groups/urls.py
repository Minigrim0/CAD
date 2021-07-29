from django.urls import path

import groups.views as views


urlpatterns = [
    path("<str:name>/", views.old, name="groups"),
]
