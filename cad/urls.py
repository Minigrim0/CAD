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
    path("admin/", admin.site.urls),
    path("administration/", include("administration.urls")),
    path("inscription/", include("inscription.urls")),
    path("users/", include("users.urls")),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    path("namur/", include("default.urls")),
    path("", views.chooseLocation),
]
