from django.test import TestCase

from public_website.email_provider import create_payload_for_email_provider
from public_website.tests.factories.factory import SubscriptionFactory


class EmailProviderTest(TestCase):
    def test_passing_participant_generates_correct_payload(self):
        subscription = SubscriptionFactory()
        payload_is = create_payload_for_email_provider(subscription.participant)
        payload_should_be = {
            "PRENOM": "Prudence",
            "THEME_SANTE": False,
            "THEME_EDUCATION": True,
            "PARTICIPANT_TYPE": 1,
            "CODE_POSTAL": "06331",
        }
        self.assertEqual(payload_should_be, payload_is)

    def test_passing_participant_generates_correct_payload_2(self):
        subscription = SubscriptionFactory()
        SubscriptionFactory(participant=subscription.participant, theme="SANTE")
        payload_is = create_payload_for_email_provider(subscription.participant)
        payload_should_be = {
            "PRENOM": "Prudence",
            "THEME_SANTE": True,
            "THEME_EDUCATION": True,
            "PARTICIPANT_TYPE": 1,
            "CODE_POSTAL": "06331",
        }
        self.assertEqual(payload_should_be, payload_is)

    # TODO -> Mock email provider API
    # def test_creating_a_contact(self):
    #     subscription = SubscriptionFactory()
    #     SubscriptionFactory(participant=subscription.participant, theme="SANTE")
    #     send_participant_profile_to_email_provider(subscription.participant)
    #     pass
