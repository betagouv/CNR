from django.test import TestCase
from django.urls import resolve, reverse
from public_website import views

class TestIndex(TestCase):

    def test_index_url_calls_right_view(self):
        resolved = resolve(reverse('index'))
        self.assertEqual(resolved.func, views.index_view)

    def test_index_view_calls_right_template(self):
        response = self.client.get(reverse('index'))
        self.assertTemplateUsed(response, "public_website/index.html")

    def test_index_response_contains_welcome_message(self):
        response = self.client.get("/")
        self.assertContains(response, "Hello world")
