import uuid

from django.db import models


class Theme(models.TextChoices):
    CLIMAT = "CLIMAT", "Climat et biodiversité"
    VIEILLISSEMENT = "VIEILLISSEMENT", "Générations et vieillissement"
    SOUVERAINETE = "SOUVERAINETE", "Souveraineté économique"
    TRAVAIL = "TRAVAIL", "Futur du travail"
    SANTE = "SANTE", "Notre santé"
    EDUCATION = "EDUCATION", "Notre école"
    LOGEMENT = "LOGEMENT", "Logement"
    JEUNESSE = "JEUNESSE", "Jeunesse"
    NUMERIQUE = "NUMERIQUE", "Numérique"


class ParticipantType(models.TextChoices):
    CITOYEN = "PARTICULIER", "Particulier"
    ELU = "ELU", "Élu(e)"
    ASSOCIATION = "ASSOCIATION", "Représentant(e) d'un corps intermédiaire"


class SanteParticipantType(models.TextChoices):
    USAGER = "USAGER", "Usager ou usagère (patient(e), accompagnant(e) ...)"
    PROSANTE = "PROSANTE", "Personnel soignant"
    ASSOCIATION = (
        "ASSOCIATION",
        "Organisation ayant un lien avec mon territoire de santé",
    )
    ELU = "ELU", "Élu(e)"
    AUTRE = "AUTRE", "Autre"


class EducationParticipantType(models.TextChoices):
    PARENT = "PARENT", "Parent d’élève"
    PROFESSEUR = "PROFESSEUR", "Enseignant(e)"
    ASSOCIATION = (
        "ASSOCIATION",
        "Organisation ayant un lien avec l’établissement scolaire",
    )
    ELU = "ELU", "Élu(e)"
    AUTRE = "AUTRE", "Autre"


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
        null=False,
        choices=ParticipantType.choices,
        default=ParticipantType.CITOYEN,
        max_length=11,
    )
    sante_city = models.CharField(
        max_length=150,
        verbose_name="Ville, département ou région",
        blank=True,
        null=True,
    )
    #  insee = models.CharField("Code INSEE", max_length=7)
    sante_participant_type = models.CharField(
        blank=False,
        null=True,
        choices=SanteParticipantType.choices,
        max_length=11,
    )
    education_city = models.CharField(
        max_length=150,
        verbose_name="Ville, département ou région",
        blank=True,
        null=True,
    )
    #  insee = models.CharField("Code INSEE", max_length=7)
    education_participant_type = models.CharField(
        blank=False,
        null=True,
        choices=EducationParticipantType.choices,
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

    def get_available_surveys(self, themes: list = None):
        from surveys.models import Survey

        available_surveys = Survey.objects.exclude(
            participations__in=self.participations.all()
        )
        if themes:
            available_surveys = available_surveys.filter(theme__in=themes)
        return available_surveys.order_by("label")


class Subscription(models.Model):
    participant = models.ForeignKey(
        Participant, models.CASCADE, related_name="subscriptions"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    theme = models.CharField(blank=False, choices=Theme.choices, max_length=14)
