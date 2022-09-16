from django.test import TestCase
from django.urls import resolve, reverse
from public_website import views

from public_website.forms import InscriptionForm


class TestFormPage(TestCase):

    def test_form_url_calls_right_view(self):
         match = resolve('/inscription/')
         self.assertEqual(match.func, views.inscription_view)

    def test_form_url_triggers_the_right_template(self):
        response = self.client.get("/inscription/")
        self.assertTemplateUsed(response, "public_website/inscription.html")


class ItemFormTest(TestCase):
    base_user = {
            "first_name": "Prudence",
            "email": "prudence.crandall@educ.gouv.fr",
            "postal_code": "06331",
            "prefered_themes": ['education'],
            "participant_type": ['citoyen'],
            "consent": True,
        }

    def test_submit_successfully(self):
        response = self.client.post(reverse('inscription'), self.base_user)
        self.assertContains(response, "Merci pour votre intérêt !")

    def test_submit_successfully_several_interests(self):
        response = self.client.post(reverse('inscription'),{
            "first_name": "Prudence",
            "email": "prudence.crandall@educ.gouv.fr",
            "postal_code": "06331",
            "prefered_themes": ['education', 'sante'],
            "participant_type": ['citoyen'],
            "consent": True,
        })
        self.assertContains(response, "Merci pour votre intérêt !")

    def test_fails_without_consent(self):
        response = self.client.post(reverse('inscription'),{
            "first_name": "Prudence",
            "email": "prudence.crandall@educ.gouv.fr",
            "postal_code": "06331",
            "prefered_themes": ['education'],
            "participant_type": ['citoyen'],
            "consent": False,
        })
        # self.assertEqual(response.status_code, 400)
        self.assertContains(response, "Formulaire invalide. Veuillez vérifier vos réponses.")

    # test_cannot_submit_invalid_email
    # test_cannot_submit_without_themes
