from django.test import TestCase
from wagtail.models import Page

from cms.models import ContentPage
from public_website.factories import (NoProfileParticipantFactory,
                                      ParticipantFactory)
from public_website.models import Participant


class ProfileViewTest(TestCase):
    def setUp(self):
        self.no_profile_participant = NoProfileParticipantFactory()
        self.participant = ParticipantFactory()

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

    def test_correct_info_with_existing_user_updates_profile(self):
        prudence = Participant.objects.get(email=self.no_profile_participant.email)
        self.assertFalse(prudence.has_profile)

        response = self.client.post(
            "/inscription/",
            {
                "email": prudence.email,
                "first_name": "Prudence",
                "postal_code": "27120",
                "participant_type": "ELU",
                "gives_gdpr_consent": True,
                "preferred_themes": ["TRAVAIL"],
                "csrfmiddlewaretoken": "fake-token",
            },
            follow=True,
        )
        prudence = Participant.objects.get(email=prudence.email)
        self.assertTrue(prudence.has_profile)
        self.assertEqual(prudence.first_name, "Prudence")

        self.assertEqual(self.client.session.get("uuid"), str(prudence.uuid))
        self.assertRedirects(response, "/participez-au-conseil-national-de-la-refondation/")

    def test_incorrect_info_with_existing_user_create_new_participant(self):
        session = self.client.session
        session["uuid"] = str(self.no_profile_participant.uuid)
        session.save()
        self.assertFalse(self.no_profile_participant.has_profile)
        ruben_email = "ruben.crandall@educ.gouv.fr"
        self.assertFalse(Participant.objects.filter(email=ruben_email).exists())

        response = self.client.post(
            "/inscription/",
            {
                "email": ruben_email,
                "first_name": "ruben",
                "postal_code": "27120",
                "participant_type": "ELU",
                "gives_gdpr_consent": True,
                "preferred_themes": ["CLIMAT"],
                "csrfmiddlewaretoken": "fake-token",
            },
            follow=True,
        )
        prudence = Participant.objects.get(email=self.no_profile_participant.email)
        self.assertFalse(prudence.has_profile)

        ruben = Participant.objects.filter(email=ruben_email)
        self.assertTrue(ruben.exists())
        self.assertTrue(ruben[0].has_profile)

        self.assertEqual(self.client.session.get("uuid"), str(ruben[0].uuid))
        self.assertRedirects(response, "/participez-au-conseil-national-de-la-refondation/")

    def test_new_participant_infos_create_new_participant(self):
        email = "esther.crandall@beta.gouv.fr"
        self.assertFalse(Participant.objects.filter(email=email).exists())
        response = self.client.post(
            "/inscription/",
            {
                "email": email,
                "first_name": "esther",
                "postal_code": "27120",
                "participant_type": "ELU",
                "gives_gdpr_consent": True,
                "preferred_themes": ["LOGEMENT"],
                "csrfmiddlewaretoken": "fake-token",
            },
            follow=True,
        )
        esther = Participant.objects.filter(email=email)
        self.assertTrue(esther.exists())
        self.assertEqual(esther[0].postal_code, "27120")

        self.assertEqual(self.client.session.get("uuid"), str(esther[0].uuid))
        self.assertRedirects(response, "/participez-au-conseil-national-de-la-refondation/")

    def test_complete_profile_cannot_update(self):
        self.assertTrue(self.participant.has_profile)
        email = self.participant.email
        response = self.client.post(
            "/inscription/",
            {
                "email": email,
                "first_name": "esther",
                "postal_code": "27120",
                "participant_type": "ELU",
                "gives_gdpr_consent": True,
                "preferred_themes": ["TRAVAIL"],
                "csrfmiddlewaretoken": "fake-token",
            },
            follow=True,
        )
        still_prudence = Participant.objects.get(email=email)
        self.assertEqual(still_prudence.postal_code, "06331")
        self.assertEqual(still_prudence.first_name, "Prudence")

        self.assertEqual(self.client.session.get("uuid"), str(still_prudence.uuid))
        self.assertRedirects(response, "/participez-au-conseil-national-de-la-refondation/")

    def test_invalid_form_returns_invalid_data_for_correction(self):
        response = self.client.post(
            "/inscription/",
            {
                "email": "not_an_email",
                "first_name": "",
                "postal_code": "123",
                "gives_gdpr_consent": True,
                "csrfmiddlewaretoken": "fake-token",
            },
        )
        self.assertContains(response, "Formulaire invalide")
        self.assertContains(response, "not_an_email")
        self.assertContains(response, "123")
