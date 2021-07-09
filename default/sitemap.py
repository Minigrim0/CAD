from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class HomeSitemap(Sitemap):
    priority = 0.6
    changefreq = "never"

    def items(self) -> list:
        """The diffrent parts of the sitemap

        Returns:
            list: The list of url names
        """
        return [
            "home",
            "contact_view",
            "login_view",
            "registerUser",
        ]

    def location(self, item: str) -> str:
        """Returns the location as url of the given url name

        Args:
            item (str): The name of the url

        Returns:
            str: The reversed url
        """
        return reverse(item)
