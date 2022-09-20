from django.db import models

from public_website.models import Theme


class Survey(models.Model):
    label = models.CharField(max_length=100, null=False, unique=True, blank=False)
    hr_label = models.TextField(null=True, blank=True)
    theme = models.CharField(
        null=True, blank=False, choices=Theme.choices, max_length=14
    )
    created_at = models.DateTimeField(auto_now_add=True)


class SurveyQuestion(models.Model):
    survey = models.ForeignKey(Survey, models.CASCADE)
    label = models.CharField(max_length=100, null=False, unique=True, blank=False)
    hr_label = models.TextField(null=True, blank=True)
    rank = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class SurveyAnswer(models.Model):
    survey_question = models.ForeignKey(SurveyQuestion, models.CASCADE)
    rank = models.IntegerField(null=True, blank=True)
    answer = models.TextField(null=False, blank=True)
    postal_code = models.CharField(
        max_length=5, verbose_name="Code postal", blank=False, null=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
