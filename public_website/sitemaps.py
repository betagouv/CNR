from django.contrib import sitemaps
from django.urls import reverse


class StaticViewSitemap(sitemaps.Sitemap):
    changefreq = "weekly"

    def items(self):
        return [
            "inscription",
            "choix_thematique",
            "resultats",
            "cgu",
            "mentions_legales",
            "accessibilite",
            "accessibilite_demarche",
            "confidentialite",
        ]

    def location(self, item):
        return reverse(item)
