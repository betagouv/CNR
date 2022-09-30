from django.urls import path

from . import views

urlpatterns = [
    path("participation/<slug:label>", views.survey_view, name="survey"),
    path("participation-intro/", views.survey_intro_view, name="survey_intro"),
    path("participation-fin/", views.survey_outro_view, name="survey_outro"),
]
