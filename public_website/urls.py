from django.urls import path

from . import views

urlpatterns = [
    path("", views.index_view, name="index"),
    path("inscription/", views.inscription_view, name="inscription"),
    path("fonctionnement/", views.fonctionnement_view, name="fonctionnement"),
    path("climat-biodiversite/", views.climat_biodiversite_view, name="climat-biodiversite"),
    path("bien-vieillir/", views.bien_vieillir_view, name="bien-vieillir"),
    path("sante/", views.sante_view, name="sante"),
    path("logement/", views.logement_view, name="logement"),
    path("numerique/", views.numerique_view, name="numerique"),
    path("jeunesse/", views.jeunesse_view, name="jeunesse"),
    path("travail/", views.travail_view, name="travail"),
    path("economie/", views.economie_view, name="economie"),
    path("cgu/", views.cgu_view, name="cgu"),
    path("mentions-legales/", views.mentions_legales_view, name="mentions_legales"),
    path("accessibilite/", views.accessibilite_view, name="accessibilite"),
    path("confidentialite/", views.confidentialite_view, name="confidentialite"),
    path(
        "accessibilite-demarche/",
        views.accessibilite_demarche_view,
        name="accessibilite_demarche",
    ),
]
