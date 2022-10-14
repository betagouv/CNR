from django.test import TestCase

from public_website.factories import NoProfileParticipantFactory, ParticipantFactory


class ParticipantModelTest(TestCase):
    def setUp(self):
        self.no_profile_participant = NoProfileParticipantFactory()
        self.participant = ParticipantFactory()

    def test_has_profile(self):
        self.assertTrue(self.participant.has_profile)
        self.assertFalse(self.no_profile_participant.has_profile)

    def test_partial_profile_is_considered_empty(self):
        participant = NoProfileParticipantFactory()
        self.assertFalse(participant.has_profile)

        participant.postal_code = "33750"
        participant.save()
        self.assertFalse(participant.has_profile)

        participant.first_name = "Prénom"
        participant.participant_type = "Particulier"
        participant.save()
        self.assertTrue(participant.has_profile)
