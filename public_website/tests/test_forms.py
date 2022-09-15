from django.test import TestCase
from django.urls import resolve, reverse
from public_website import views

from public_website.forms import FormulaireForm

class TestFormPage(TestCase):
    def test_form_url_calls_right_view(self):
         match = resolve('/formulaire-test')
         self.assertEqual(match.func, views.formulaire_test)

    def test_form_url_triggers_the_right_template(self):
        response = self.client.get("/formulaire-test")
        self.assertTemplateUsed(response, "public_website/formulaire_test.html")

class ItemFormTest(TestCase):

    def test_form_renders_item_text_input(self):
        form = FormulaireForm()
        self.fail(form.as_p())

