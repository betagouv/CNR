from django.test import TestCase
from django.urls import resolve

from public_website import views


class TestSurvey(TestCase):
    def test_survey_url_calls_right_view(self):
        match = resolve("/survey/")
        self.assertEqual(match.func, views.survey_view)

    def test_survey_url_calls_right_template(self):
        response = self.client.get("/survey/")
        self.assertTemplateUsed(response, "public_website/survey.html")

    def test_survey_response_contains_welcome_message(self):
        response = self.client.get("/survey/")
        self.assertContains(response, "Questionnaire")


class TestSurveyIntro(TestCase):
    def test_survey_intro_url_calls_right_view(self):
        match = resolve("/survey-intro/")
        self.assertEqual(match.func, views.survey_intro_view)

    def test_survey_intro_url_calls_right_template(self):
        response = self.client.get("/survey-intro/")
        self.assertTemplateUsed(response, "public_website/survey_intro.html")

    def test_survey_intro_response_contains_welcome_message(self):
        response = self.client.get("/survey-intro/")
        self.assertContains(response, "Votre inscription est enregistrée")


class TestSurveyOutro(TestCase):
    def test_survey_outro_url_calls_right_view(self):
        match = resolve("/survey-outro/")
        self.assertEqual(match.func, views.survey_outro_view)

    def test_survey_outro_url_calls_right_template(self):
        response = self.client.get("/survey-outro/")
        self.assertTemplateUsed(response, "public_website/survey_outro.html")

    def test_survey_outro_response_contains_welcome_message(self):
        response = self.client.get("/survey-outro/")
        self.assertContains(response, "Merci pour votre contribution")
