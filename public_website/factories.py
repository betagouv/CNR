import factory

from public_website import models


class NoProfileParticipantFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Participant

    email = factory.Sequence("prudence.crandall_{}@noeduc.gouv.fr".format)
    registration_success = True


class ParticipantFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Participant

    first_name = "Prudence"
    email = factory.Sequence("prudence.crandall_{}@educ.gouv.fr".format)
    postal_code = "06331"
    participant_type = models.ParticipantType.CITOYEN
    registration_success = True


class SubscriptionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Subscription

    participant = factory.SubFactory(ParticipantFactory)
    theme = models.Theme.CLIMAT
