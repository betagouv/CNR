from django.urls import path

from . import views

urlpatterns = [
    path("inscription/", views.inscription_view, name="inscription"),
    path("cgu/", views.cgu_view, name="cgu"),
    path("mentions-legales/", views.mentions_legales_view, name="mentions_legales"),
    path("accessibilite/", views.accessibilite_view, name="accessibilite"),
    path("confidentialite/", views.confidentialite_view, name="confidentialite"),
    path("resultats/", views.resultats_view, name="resultats"),
    path("choix-thematique/", views.choix_thematique_view, name="choix_thematique"),
    path(
        "accessibilite-demarche/",
        views.accessibilite_demarche_view,
        name="accessibilite_demarche",
    ),
]
