from django.test import TestCase
from django.urls import resolve, reverse
from public_website import views

from public_website.forms import FormulaireForm


class TestFormPage(TestCase):

    def test_form_url_calls_right_view(self):
         match = resolve('/formulaire-test/')
         self.assertEqual(match.func, views.formulaire_test)

    def test_form_url_triggers_the_right_template(self):
        response = self.client.get("/formulaire-test/")
        self.assertTemplateUsed(response, "public_website/formulaire_test.html")


class ItemFormTest(TestCase):

    def test_form_renders_item_text_input(self):
        form = FormulaireForm()
        self.fail(form.as_p())

    def test_succesfully_submit(self):
        response = self.client.post(reverse('formulaire_test'),{
            "first_name": "Prudence",
            "email": "prudence.crandall@educ.gouv.fr",
            "postal_code": "06331",
            "prefered_themes": ["education"],
            "participant_type": "Citoyen",
            "consent": True,
        })
        self.assertContains(response, "Merci pour votre intérêt !")
    
    # test_cannot_submit_invalid_email
    # test_cannot_submit_without_themes
    # test_cannot_submit_without_consent