from django.db import models


class Theme(models.TextChoices):
    EDUCATION = "EDUCATION", "Éducation"
    SANTE = "SANTE", "Santé"


class ParticipantType(models.TextChoices):
    CITOYEN = "PARTICULIER", "Particulier"
    ELU = "ELU", "Élu"
    ASSOCIATION = "ASSOCIATION", "Représentant(e) d'une association"


class Participant(models.Model):
    email = models.EmailField(
        max_length=150, unique=True, verbose_name="Adresse électronique", blank=False, null=False
    )
    first_name = models.CharField(
        max_length=150, verbose_name="Prénom", blank=False, null=False
    )
    postal_code = models.CharField(
        max_length=5, verbose_name="Code postal", blank=False, null=False
    )
    participant_type = models.CharField(
        blank=False,
        null=False,
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


class Subscription(models.Model):
    participant = models.ForeignKey(Participant, models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    theme = models.CharField(blank=False, choices=Theme.choices, max_length=9)
