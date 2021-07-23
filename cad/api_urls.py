from django.urls import path
from django.conf.urls import include


app_name = 'api'
urlpatterns = [
    path('administration/', include('administration.api_urls', namespace="adminapi")),
    path('users/', include('users.api_urls', namespace="users")),
]
