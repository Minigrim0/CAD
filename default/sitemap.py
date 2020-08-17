from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class HomeSitemap(Sitemap):
    priority = 0.6
    changefreq = 'never'

    def items(self):
        return [
            'home',
            'contact_view',
            'login_view',
            'registerStudent',
            'registerCoach',
        ]

    def location(self, item):
        return reverse(item)
