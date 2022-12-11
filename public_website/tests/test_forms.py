from django.test import TestCase
from django.urls import resolve, reverse
from wagtail.models import Page

from cms.models import ContentPage
from public_website import views
from public_website.models import Participant


class FormPageTest(TestCase):
    def test_form_url_calls_right_view(self):
        match = resolve("/inscription/")
        self.assertEqual(match.func, views.inscription_view)

    def test_form_url_triggers_the_right_template(self):
        response = self.client.get("/inscription/")
        self.assertTemplateUsed(response, "public_website/inscription.html")


class ProfileForm(TestCase):
    def setUp(self):
        default_home = Page.objects.filter(title="Welcome to your new Wagtail site!")[0]
        target_page = ContentPage(
            slug="participez-au-conseil-national-de-la-refondation",
            title="Participez au conseil national de la refondation",
        )
        target_page.body.stream_data = [
            ('heading', 'Participez au conseil national de la refondation'),
        ]
        default_home.add_child(instance=target_page)
        default_home.save()
        target_page.save_revision().publish()
        target_page.save()

    def generate_base_user(self):
        return {
            "first_name": "Prudence",
            "email": "prudence.crandall@educ.gouv.fr",
            "postal_code": "06331",
            "participant_type": ["PARTICULIER"],
            "preferred_themes": [],
            "pick_local_theme_sante": [],
            "sante_participant_type": [],
            "sante_city": [],
            "pick_local_theme_education": [],
            "education_participant_type": [],
            "education_city": [],
            "gives_gdpr_consent": ["on"],
        }

    def generate_response(self, list_changed_param_value: list = None):
        response = self.generate_base_user()
        if list_changed_param_value:
            for changed_param, changed_value in list_changed_param_value:
                if changed_value is None:
                    del response[changed_param]
                else:
                    response[changed_param] = changed_value

        response["csrfmiddlewaretoken"] = "fake-token"
        return self.client.post(reverse("inscription"), response, follow=True)

    def test_submit_successfully(self):
        response = self.generate_response()
        participant = Participant.objects.last()
        self.assertEqual(self.client.session.get("uuid"), str(participant.uuid))
        self.assertRedirects(response, "/participez-au-conseil-national-de-la-refondation/")

    def test_submit_successfully_several_interests(self):
        response = self.generate_response(
            [("preferred_themes", ["LOGEMENT", "CLIMAT"])]
        )
        participant = Participant.objects.last()
        self.assertEqual(self.client.session.get("uuid"), str(participant.uuid))
        self.assertRedirects(response, "/participez-au-conseil-national-de-la-refondation/")
        self.assertEqual(participant.subscriptions.count(), 2)

    def test_submit_successfully_local_interests(self):
        response = self.generate_response(
            [
                ("pick_local_theme_sante", ["on"]),
                ("sante_participant_type", ["ELU"]),
                ("sante_city", ["Trouville"]),
                ("pick_local_theme_education", ["on"]),
                ("education_participant_type", ["PARENT"]),
                ("education_city", ["Rouen"]),
            ]
        )
        participant = Participant.objects.last()
        self.assertRedirects(response, "/participez-au-conseil-national-de-la-refondation/")
        subscriptions = participant.subscriptions
        self.assertEqual(subscriptions.count(), 2)
        self.assertEqual(subscriptions.first().theme, "SANTE")
        self.assertEqual(subscriptions.last().theme, "EDUCATION")

        self.assertEqual(participant.sante_participant_type, "ELU")
        self.assertEqual(participant.education_participant_type, "PARENT")
        self.assertEqual(participant.sante_city, "Trouville")
        self.assertEqual(participant.education_city, "Rouen")

    def test_submit_successfully_no_local_interests(self):
        response = self.generate_response(
            [
                ("pick_local_theme_sante", None),
                ("sante_participant_type", ["ELU"]),
                ("sante_city", ["Trouville"]),
                ("pick_local_theme_education", None),
                ("education_participant_type", ["PARENT"]),
                ("education_city", ["Rouen"]),
            ]
        )
        participant = Participant.objects.last()
        self.assertRedirects(response, "/participez-au-conseil-national-de-la-refondation/")
        subscriptions = participant.subscriptions
        self.assertEqual(subscriptions.count(), 0)
        self.assertEqual(participant.sante_participant_type, None)
        self.assertEqual(participant.education_participant_type, None)
        self.assertEqual(participant.education_city, None)
        self.assertEqual(participant.sante_city, None)

    def test_fails_without_consent(self):
        response = self.generate_response([("gives_gdpr_consent", None)])
        self.assertContains(
            response,
            "Formulaire invalide. Veuillez vérifier vos réponses.",
        )

    def test_fails_with_non_existing_participant_type(self):
        response = self.generate_response([("participant_type", ["Le Père Noel"])])
        self.assertContains(
            response, "Formulaire invalide. Veuillez vérifier vos réponses."
        )

    def test_fails_with_invalid_email(self):
        response = self.generate_response([("email", "a@acom")])
        self.assertContains(
            response, "Formulaire invalide. Veuillez vérifier vos réponses."
        )

    def test_valid_without_themes(self):
        response = self.generate_response([("preferred_themes", [])])
        self.assertRedirects(response, "/participez-au-conseil-national-de-la-refondation/")

    def test_returning_user_gets_confirmation_form_message(self):
        self.generate_response()
        participant = Participant.objects.filter(email="prudence.crandall@educ.gouv.fr")
        self.assertTrue(participant.exists())

        response = self.generate_response()
        still_participant = Participant.objects.last()
        self.assertEqual(participant[0].id, still_participant.id)

        self.assertEqual(self.client.session.get("uuid"), str(still_participant.uuid))
        self.assertRedirects(response, "/participez-au-conseil-national-de-la-refondation/")

    def test_99_validates_for_postal_code(self):
        response = self.generate_response([("postal_code", "99")])
        participant = Participant.objects.last()
        self.assertEqual(self.client.session.get("uuid"), str(participant.uuid))
        self.assertRedirects(response, "/participez-au-conseil-national-de-la-refondation/")

    def test_98_does_not_validates_for_postal_code(self):
        response = self.generate_response([("postal_code", "98")])
        self.assertContains(response, "Formulaire invalide.")

    def test_ABCDE_does_not_validates_for_postal_code(self):
        response = self.generate_response([("postal_code", "ABCDE")])
        self.assertContains(response, "Formulaire invalide.")

    def test_123456_does_not_validates_for_postal_code(self):
        response = self.generate_response([("postal_code", "123456")])
        self.assertContains(response, "Formulaire invalide.")

    def test_returning_email_should_not_duplicate(self):
        response = self.generate_response([("email", "")])
        self.assertContains(response, "Formulaire invalide.")

    def test_empty_user_doesnt_prevent_new_subscription(self):
        Participant.objects.create(email="")
        response = self.generate_response()
        self.assertRedirects(response, "/participez-au-conseil-national-de-la-refondation/")
