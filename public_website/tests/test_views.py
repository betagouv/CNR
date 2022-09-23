from django.test import TestCase

from public_website.models import Participant
from public_website.tests.decorators import patch_send_in_blue
from public_website.tests.factories.factory import (
    NoProfileParticipantFactory, ParticipantFactory)


class ProfileViewTest(TestCase):
    def setUp(self):
        self.no_profile_participant = NoProfileParticipantFactory()
        self.participant = ParticipantFactory()

    @patch_send_in_blue
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
                "prefered_themes": ["SANTE"],
                "csrfmiddlewaretoken": "fake-token",
            },
        )
        prudence = Participant.objects.get(email=prudence.email)
        self.assertTrue(prudence.has_profile)
        self.assertEqual(prudence.first_name, "Prudence")
        self.assertRedirects(response, "/survey-intro/")

    @patch_send_in_blue
    def test_incorrect_info_with_existing_user_create_new_participant(self):
        session = self.client.session
        session["uuid"] = str(self.no_profile_participant.uuid)
        session.save()
        self.assertEqual(self.no_profile_participant.postal_code, None)
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
                "prefered_themes": ["EDUCATION"],
                "csrfmiddlewaretoken": "fake-token",
            },
        )
        prudence = Participant.objects.get(email=self.no_profile_participant.email)
        self.assertFalse(prudence.has_profile)

        ruben = Participant.objects.filter(email=ruben_email)
        self.assertTrue(Participant.objects.filter(email=ruben_email).exists())
        self.assertTrue(ruben[0].has_profile)
        self.assertRedirects(response, "/survey-intro/")

    @patch_send_in_blue
    def test_new_participant_infos_create_new_participant(self):
        email = "esther.crandall@beta.gouv.fr"
        self.assertFalse(Participant.objects.filter(email=email).exists())
        response = self.client.post(
            "/inscription/",
            {
                "email": email,
                "email_test": email,
                "first_name": "esther",
                "postal_code": "27120",
                "participant_type": "ELU",
                "gives_gdpr_consent": True,
                "prefered_themes": ["SANTE"],
                "csrfmiddlewaretoken": "fake-token",
            },
        )
        esther = Participant.objects.filter(email=email)

        self.assertTrue(esther.exists())
        self.assertEqual(esther[0].postal_code, "27120")
        self.assertRedirects(response, "/survey-intro/")

    def test_complete_profile_cannot_update(self):
        self.assertEqual(self.participant.postal_code, "06331")
        email = self.participant.email
        response = self.client.post(
            "/inscription/",
            {
                "email": email,
                "first_name": "esther",
                "postal_code": "27120",
                "participant_type": "ELU",
                "gives_gdpr_consent": True,
                "prefered_themes": ["EDUCATION"],
                "csrfmiddlewaretoken": "fake-token",
            },
        )
        still_prudence = Participant.objects.get(email=email)
        self.assertEqual(still_prudence.postal_code, "06331")
        self.assertEqual(still_prudence.first_name, "Prudence")
        self.assertRedirects(response, "/survey-intro/")
