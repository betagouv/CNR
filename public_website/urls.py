from django.urls import path

from . import views

urlpatterns = [
    path("", views.index_view, name="index"),
    path("loaderio-20a1c730374bd51907e44cd42432f32a/", views.loaderio_view, name="loader"),
    path("inscription/", views.inscription_view, name="inscription"),
    path("fonctionnement/", views.fonctionnement_view, name="fonctionnement"),
    path("cgu/", views.cgu_view, name="cgu"),
    path("mentions-legales/", views.mentions_legales_view, name="mentions_legales"),
    path("accessibilite/", views.accessibilite_view, name="accessibilite"),
    path("confidentialite/", views.confidentialite_view, name="confidentialite"),
]
