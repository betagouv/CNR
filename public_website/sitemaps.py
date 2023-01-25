from django.contrib import sitemaps
from django.urls import reverse


class StaticViewSitemap(sitemaps.Sitemap):
    changefreq = "weekly"

    def items(self):
        return [
            "inscription",
            "accessibilite",
            "accessibilite_demarche",
            "mentions_legales",
            "confidentialite",
            "cgu",
        ]

    def location(self, item):
        return reverse(item)
