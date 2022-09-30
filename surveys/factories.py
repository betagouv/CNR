import factory

from public_website.factories import ParticipantFactory
from public_website.models import Theme
from surveys import models


class SurveyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Survey

    label = factory.LazyAttributeSequence(
        lambda survey, counter: f"{survey.theme.label}-{counter}"
    )
    hr_label = factory.LazyAttributeSequence(
        lambda survey, counter: f"Voici le questionnaire n°{counter} du thème "
        f"{survey.theme.label}"
    )
    theme = Theme.EDUCATION


class SurveyQuestionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.SurveyQuestion

    survey = factory.SubFactory(SurveyFactory)
    label = factory.LazyAttributeSequence(
        lambda question, counter: f"{question.survey.label}-Q-{counter}"
    )
    hr_label = "Que pensez vous de cette réforme ?"
    answer_type = models.SurveyQuestion.AnswerType.THREE_TEXT_FIELD


class SurveyAnswerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.SurveyAnswer

    survey_question = factory.SubFactory(SurveyQuestionFactory)
    answer = (
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
        "Nulla aliquet dictum est non ornare. "
        "Donec imperdiet a lacus at porttitor !"
    )
    postal_code = "34567"


class SurveyParticipationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.SurveyParticipation

    survey = factory.SubFactory(SurveyFactory)
    participant = factory.SubFactory(ParticipantFactory)
