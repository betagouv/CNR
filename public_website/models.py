from django.db import models


class Theme(models.TextChoices):
    EDUCATION = "EDUCATION", "Éducation"
    SANTE = "SANTE", "Santé"


class ParticipantType(models.TextChoices):
    CITOYEN = "CITOYEN", "Citoyen"
    ELU = "ELU", "Élu"
    ASSOCIATION = "ASSOCIATION", "Représentant d'une association"


class Participant(models.Model):
    email = models.EmailField(
        unique=True, verbose_name="Courriel", blank=False, null=False
    )
    first_name = models.CharField(
        max_length=100, verbose_name="Prénom", blank=False, null=False
    )
    postal_code = models.CharField(
        max_length=10, verbose_name="Code Postal", blank=False, null=False
    )
    participant_type = models.CharField(
        blank=False,
        null=False,
        choices=ParticipantType.choices,
        max_length=30,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Subscription(models.Model):
    participant = models.ForeignKey(Participant, models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    theme = models.CharField(blank=False, choices=Theme.choices, max_length=30)
