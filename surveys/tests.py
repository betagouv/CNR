from django.test import TestCase, tag

from public_website.models import Theme
from surveys.factories import SurveyFactory, SurveyQuestionFactory
from surveys.models import Survey, SurveyAnswer, SurveyQuestion


@tag("models")
class SurveyModelTests(TestCase):
    def test_saving_and_retrieving_survey(self):
        survey = Survey(
            label="survey_edu_1",
            hr_label="Ceci est le premier questionnaire sur " "la thématique Education",
            theme=Theme.EDUCATION,
        )
        survey.save()
        saved_items = Survey.objects.all()
        self.assertEqual(saved_items.count(), 1)
        first_saved_item = saved_items[0]
        self.assertEqual(first_saved_item.label, "survey_edu_1")
        self.assertEqual(first_saved_item.theme, "EDUCATION")


@tag("models")
class SurveyQuestionModelTests(TestCase):
    def test_saving_and_retrieving_survey_question(self):
        survey = SurveyFactory(theme=Theme.EDUCATION)
        survey_question = SurveyQuestion(
            survey=survey,
            label="edu_1_question_1",
            hr_label="Que pensez-vous de cette réforme ?",
            rank=2,
        )

        survey_question.save()
        saved_items = SurveyQuestion.objects.all()
        self.assertEqual(saved_items.count(), 1)
        first_saved_item = saved_items[0]
        self.assertEqual(first_saved_item.label, "edu_1_question_1")
        self.assertEqual(first_saved_item.survey.theme, "EDUCATION")


@tag("models")
class SurveyAnswerModelTests(TestCase):
    def test_saving_and_retrieving_survey_answer(self):
        survey_question = SurveyQuestionFactory(
            survey=SurveyFactory(theme=Theme.EDUCATION), label="EDU_456"
        )
        survey_answer = SurveyAnswer(
            survey_question=survey_question,
            rank=1,
            answer="Lorem ipsum dolor sit amet, consectetur adipiscing elit."
            " Nulla aliquet dictum est non ornare. Donec imperdiet a"
            " lacus at porttitor.",
            postal_code="27120",
        )

        survey_answer.save()
        saved_items = SurveyAnswer.objects.all()
        self.assertEqual(saved_items.count(), 1)
        first_saved_item = saved_items[0]
        self.assertEqual(first_saved_item.survey_question.label, "EDU_456")
        self.assertEqual(first_saved_item.survey_question.survey.theme, "EDUCATION")
