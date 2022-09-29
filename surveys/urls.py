from django.urls import path

from . import views

urlpatterns = [
    path("participation/<slug:slug>", views.survey_theme_view, name="survey_theme"),
    path("participation-intro/", views.survey_intro_view, name="survey_intro"),
    path("participation-fin/", views.survey_outro_view, name="survey_outro"),
]
