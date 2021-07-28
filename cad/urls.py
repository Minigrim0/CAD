from django.urls import path
from django.contrib import admin
from django.conf.urls import include
from django.contrib.sitemaps.views import sitemap

from default.sitemap import HomeSitemap
import cad.views as views


sitemaps = {
    "static": HomeSitemap,
}

urlpatterns = [
    path("bruxelles/", include("old_site.urls")),
    # path("namur/", include("default.urls")),
    # path("administration/", include("administration.urls")),
    # path("inscription/", include("inscription.urls")),
    # path("users/", include("users.urls")),
    path("admin/", admin.site.urls),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    # path('auth/reset/done/', views.password_reset_done),
    # path('auth/', include('django.contrib.auth.urls')),
    # path('api/', include('cad.api_urls', namespace="api")),
    path("", views.chooseLocation),
]
