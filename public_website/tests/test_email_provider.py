from django.test import TestCase

from factories.factory import SubscriptionFactory
from public_website.email_provider import create_payload_for_email_provider


class EmailProviderTest(TestCase):
    def test_passing_participant_generates_correct_payload(self):
        subscription = SubscriptionFactory()
        payload_is = create_payload_for_email_provider(subscription.participant)
        payload_should_be = {
            "PRENOM": "Prudence",
            "PARTICIPANT_TYPE": 1,
            "CODE_POSTAL": "06331",
            "THEME_SANTE": False,
            "THEME_EDUCATION": True,
            "THEME_CLIMAT": False,
            "THEME_VIEILLISSEMENT": False,
            "THEME_SOUVERAINETE": False,
            "THEME_TRAVAIL": False,
            "THEME_LOGEMENT": False,
            "THEME_JEUNESSE": False,
            "THEME_NUMERIQUE": False,
        }

        self.assertEqual(payload_should_be, payload_is)

    def test_passing_participant_generates_correct_payload_2(self):
        subscription = SubscriptionFactory()
        SubscriptionFactory(participant=subscription.participant, theme="SANTE")
        payload_is = create_payload_for_email_provider(subscription.participant)
        payload_should_be = {
            "PRENOM": "Prudence",
            "PARTICIPANT_TYPE": 1,
            "CODE_POSTAL": "06331",
            "THEME_SANTE": True,
            "THEME_EDUCATION": True,
            "THEME_CLIMAT": False,
            "THEME_VIEILLISSEMENT": False,
            "THEME_SOUVERAINETE": False,
            "THEME_TRAVAIL": False,
            "THEME_LOGEMENT": False,
            "THEME_JEUNESSE": False,
            "THEME_NUMERIQUE": False,
        }
        self.assertEqual(payload_should_be, payload_is)
