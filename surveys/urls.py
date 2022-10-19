from django.urls import path

from . import views

urlpatterns = [
    path("participation/<slug:label>", views.survey_view, name="survey"),
    path("participation-intro/", views.survey_home_view, name="survey_home"),
]
