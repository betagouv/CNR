from django.test import TestCase
from django.urls import resolve, reverse

from public_website import views
from public_website.models import Participant


class FormPageTest(TestCase):

    def test_form_url_calls_right_view(self):
        match = resolve("/inscription/")
        self.assertEqual(match.func, views.inscription_view)

    def test_form_url_triggers_the_right_template(self):
        response = self.client.get("/inscription/")
        self.assertTemplateUsed(response, "public_website/inscription.html")


class RegisterFormTest(TestCase):

    def generate_base_user(self):
        return {
            "email": "prudence.crandall@educ.gouv.fr",
            "gives_gdpr_consent": True
        }
    
    def generate_response(self, changed_param=None, changed_value=None):
        user = self.generate_base_user()
        if changed_param:
            user[changed_param] = changed_value
            if changed_value is None:
                del user[changed_param]

        return self.client.post(reverse("index"), user)        

    def test_valid_registerform_registers_participant(self):
        self.generate_response()
        new_participant = Participant.objects.filter(email=self.generate_base_user()['email'])
        self.assertTrue(new_participant.exists())
        # self.assertTrue(new_participant[0].registration_success)

    def test_valid_registerform_sends_uuid_to_session(self):
        self.generate_response()
        new_participant = Participant.objects.filter(email=self.generate_base_user()['email'])
        self.assertTrue('uuid' in self.client.session)


class ProfileForm(TestCase):
    def generate_base_user(self):
        return {
            "first_name": "Prudence",
            "email": "prudence.crandall@educ.gouv.fr",
            "postal_code": "06331",
            "prefered_themes": ["EDUCATION"],
            "participant_type": ["PARTICULIER"],
            "gives_gdpr_consent": ["on"],
        }

    def generate_response(self, changed_param=None, changed_value=None):
        response = self.generate_base_user()
        if changed_param:
            response[changed_param] = changed_value
            if changed_value is None:
                del response[changed_param]

        response["csrfmiddlewaretoken"] = "fake-token"
        return self.client.post(reverse("inscription"), response)

    def test_submit_successfully(self):
        # self.simulate_user_filled_registered_form()
        response = self.generate_response()
        self.assertContains(response, "Merci pour votre intérêt !")

    def test_submit_successfully_several_interests(self):
        response = self.generate_response("prefered_themes", ["EDUCATION", "SANTE"])
        self.assertContains(response, "Merci pour votre intérêt !")

    def test_fails_without_consent(self):
        response = self.generate_response("gives_gdpr_consent", None)
        self.assertContains(
            response,
            "Formulaire invalide. Veuillez vérifier vos réponses.",
        )

    def test_fails_with_non_existing_participant_type(self):
        response = self.generate_response("participant_type", ["Le Père Noel"])
        self.assertContains(
            response, "Formulaire invalide. Veuillez vérifier vos réponses."
        )

    def test_fails_with_invalid_email(self):
        response = self.generate_response("email", "a@acom")
        self.assertContains(
            response, "Formulaire invalide. Veuillez vérifier vos réponses."
        )

    def test_fails_without_themes(self):
        response = self.generate_response("prefered_themes", "[]")
        self.assertContains(
            response, "Formulaire invalide. Veuillez vérifier vos réponses."
        )

    def test_returning_user_gets_confirmation_form_message(self):
        self.generate_response()
        self.assertTrue(
            Participant.objects.filter(email="prudence.crandall@educ.gouv.fr").exists()
        )
        response2 = self.generate_response()
        self.assertContains(
            response2, "Données enregistrées. Merci pour votre intérêt !"
        )

    def test_99_validates_for_postal_code(self):
        response = self.generate_response("postal_code", "99")
        self.assertContains(response, "Merci pour votre intérêt !")

    def test_98_does_not_validates_for_postal_code(self):
        response = self.generate_response("postal_code", "98")
        self.assertContains(response, "Formulaire invalide.")

    def test_ABCDE_does_not_validates_for_postal_code(self):
        response = self.generate_response("postal_code", "ABCDE")
        self.assertContains(response, "Formulaire invalide.")

    def test_123456_does_not_validates_for_postal_code(self):
        response = self.generate_response("postal_code", "ABCDE")
        self.assertContains(response, "Formulaire invalide.")
