from django.urls import path
from . import views


urlpatterns = [
    path('', views.index_view, name='index'),
    path('formulaire-test', views.formulaire_test, name='formulaire_test'),
]
