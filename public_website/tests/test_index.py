from django.test import TestCase


class TestIndex(TestCase):

    def test_home_url_triggers_the_right_template(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "public_website/index.html")

    def test_home_response_contains_welcome_message(self):
        response = self.client.get("/")
        self.assertContains(response, "Hello world")
