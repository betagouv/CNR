import uuid

from django.db import models


class Theme(models.TextChoices):
    CLIMAT = "CLIMAT", "Climat"
    VIEILLISSEMENT = "VIEILLISSEMENT", "Générations et vieillissement"
    SOUVERAINETE = "SOUVERAINETE", "Souveraineté économique"
    TRAVAIL = "TRAVAIL", "Futur du travail"
    SANTE = "SANTE", "Santé"
    EDUCATION = "EDUCATION", "Éducation"
    LOGEMENT = "LOGEMENT", "Logement"
    JEUNESSE = "JEUNESSE", "Jeunesse"
    NUMERIQUE = "NUMERIQUE", "Numérique"


class ParticipantType(models.TextChoices):
    CITOYEN = "PARTICULIER", "Particulier"
    ELU = "ELU", "Élu"
    ASSOCIATION = "ASSOCIATION", "Représentant(e) d'une association"


class Participant(models.Model):
    email = models.EmailField(
        max_length=150,
        unique=True,
        verbose_name="Adresse électronique",
        blank=False,
        null=False,
    )
    uuid = models.UUIDField(default=uuid.uuid4)
    first_name = models.CharField(
        max_length=150, verbose_name="Prénom", blank=False, null=True
    )
    postal_code = models.CharField(
        max_length=5, verbose_name="Code postal", blank=False, null=True
    )
    participant_type = models.CharField(
        blank=False,
        null=True,
        choices=ParticipantType.choices,
        max_length=11,
    )
    registration_success = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_subscription_list(self):
        return Subscription.objects.filter(participant=self).values_list(
            "theme", flat=True
        )

    @property
    def has_profile(self):
        return self.postal_code is not None


class Subscription(models.Model):
    participant = models.ForeignKey(Participant, models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    theme = models.CharField(blank=False, choices=Theme.choices, max_length=14)
