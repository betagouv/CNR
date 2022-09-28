from django.core.validators import MinLengthValidator
from django.db import models

from public_website.models import Theme


class Survey(models.Model):
    label = models.CharField(max_length=100, null=False, unique=True, blank=False)
    hr_label = models.TextField(null=True, blank=True)
    theme = models.CharField(
        null=True, blank=False, choices=Theme.choices, max_length=14
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def get_questions(self):
        return self.questions.order_by("label")


class SurveyQuestion(models.Model):
    class AnswerType(models.TextChoices):
        ONE_TEXT_FIELD = "ONE_TEXT_FIELD", "1 large text input"
        THREE_TEXT_FIELD = "THREE_TEXT_FIELD", "3 small text inputs"
        FIVE_TEXT_FIELD = "FIVE_TEXT_FIELD", "5 small text inputs"

    survey = models.ForeignKey(
        Survey, on_delete=models.CASCADE, related_name="questions"
    )
    label = models.CharField(max_length=100, null=False, unique=True, blank=False)
    hr_label = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    answer_type = models.CharField(choices=AnswerType.choices, max_length=50)


class SurveyAnswer(models.Model):
    survey_question = models.ForeignKey(SurveyQuestion, on_delete=models.CASCADE)
    rank = models.IntegerField(null=True, blank=True)
    answer = models.TextField(null=False, blank=True)
    postal_code = models.CharField(
        max_length=5, verbose_name="Code postal", blank=False
    )
    created_at = models.DateField(auto_now_add=True)
    survey_response_id = models.CharField(
        max_length=22,
        verbose_name="Identificateur de réponse au questionnaire",
        validators=[MinLengthValidator(16)],
        null=False,
    )


class SurveyParticipation(models.Model):
    survey = models.ForeignKey(
        "surveys.Survey", on_delete=models.CASCADE, related_name="participations"
    )
    participant = models.ForeignKey(
        "public_website.Participant",
        on_delete=models.CASCADE,
        related_name="participations",
    )
