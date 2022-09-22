from django.test import TestCase
from public_website.tests.factories.factory import ParticipantFactory, NoProfileParticipantFactory

from public_website.models import Participant


class ParticipantModelTest(TestCase):

    def setUp(self):
        self.no_profile_participant = NoProfileParticipantFactory()
        self.participant = ParticipantFactory()

    def test_has_profile(self):
        self.assertTrue(self.participant.has_profile)
        self.assertFalse(self.no_profile_participant.has_profile)
