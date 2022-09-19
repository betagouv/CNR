import factory

from public_website.models import Theme
from surveys import models


class SurveyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Survey

    label = factory.Sequence("Q_EDU_{}".format)
    hr_label = "Voici le premier questionnaire du thème Education"
    theme = Theme.EDUCATION


class SurveyQuestionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.SurveyQuestion

    survey = factory.SubFactory(SurveyFactory)
    label = factory.Sequence("Q_EDU_{}".format)
    hr_label = "Que pensez vous de cette réforme ?"
    rank = factory.Sequence("{}".format)


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
