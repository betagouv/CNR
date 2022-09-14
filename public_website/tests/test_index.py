from django.test import TestCase
from django.urls import resolve, reverse
from public_website import views

class TestIndex(TestCase):

    def test_index_url_calls_right_view(self):
        match = resolve('/')
        self.assertEqual(match.func, views.index_view)

    def test_index_url_calls_right_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, "public_website/index.html")

    def test_index_response_contains_welcome_message(self):
        response = self.client.get("/")
        self.assertContains(response, "Une nouvelle méthode")
