from django.test import TestCase, tag

from factories.factory import SubscriptionFactory
from public_website.models import Theme
from surveys import forms
from surveys.factories import SurveyFactory, SurveyQuestionFactory
from surveys.models import Survey, SurveyAnswer, SurveyParticipation, SurveyQuestion


@tag("models")
class SurveyModelTests(TestCase):
    def test_saving_and_retrieving_survey(self):
        survey = Survey(
            label="survey_edu_1",
            hr_label="Ceci est le premier questionnaire sur la thématique Education",
            theme=Theme.EDUCATION,
        )
        survey.save()
        last_saved_item = Survey.objects.last()
        self.assertEqual(last_saved_item.label, "survey_edu_1")
        self.assertEqual(last_saved_item.theme, "EDUCATION")

    def test_model_get_questions_method(self):
        answer_type = SurveyQuestion.AnswerType
        question_1 = SurveyQuestionFactory(
            answer_type=answer_type.THREE_TEXT_FIELD, label="BBB"
        )
        survey_1 = question_1.survey
        SurveyQuestionFactory(
            survey=survey_1, answer_type=answer_type.THREE_TEXT_FIELD, label="CCC"
        )
        question_3 = SurveyQuestionFactory(
            survey=survey_1, answer_type=answer_type.ONE_TEXT_FIELD, label="AAAA"
        )

        get_questions = survey_1.get_questions()

        self.assertEqual(get_questions.count(), 3)
        self.assertEqual(get_questions[0], question_3)


@tag("models")
class SurveyQuestionModelTests(TestCase):
    def test_saving_and_retrieving_survey_question(self):
        survey = SurveyFactory(theme=Theme.EDUCATION)
        SurveyQuestion(
            survey=survey,
            label="edu_1_question_1",
            hr_label="Que pensez-vous de cette réforme ?",
        ).save()

        last_saved_item = SurveyQuestion.objects.last()
        self.assertEqual(last_saved_item.label, "edu_1_question_1")
        self.assertEqual(last_saved_item.survey.theme, "EDUCATION")


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
            survey_response_id="X7NYIolv893DXLunTzeTIQ",
        )

        survey_answer.save()
        last_saved_item = SurveyAnswer.objects.last()
        self.assertEqual(last_saved_item.survey_question.label, "EDU_456")
        self.assertEqual(last_saved_item.survey_question.survey.theme, "EDUCATION")


@tag("forms")
class SurveyFormTests(TestCase):
    def test_form_generation(self):
        question1 = SurveyQuestionFactory(
            answer_type=SurveyQuestion.AnswerType.THREE_TEXT_FIELD, label="survey-1-Q-1"
        )
        form = forms.SurveyForm(questions=[question1])
        self.assertEqual(len(form.fields), 3)
        self.assertEqual(form.fields["survey-1-Q-1-A-0"].label, question1.label)


@tag("models")
class SurveyParticipationModelTest(TestCase):
    def test_saving_and_retrieving_survey_participation(self):
        SurveyFactory(theme=Theme.EDUCATION, label="first_survey_edu")
        survey_2 = SurveyFactory(theme=Theme.EDUCATION, label="second_survey_edu")
        SurveyFactory(theme=Theme.SANTE)
        subscription_edu = SubscriptionFactory(theme=Theme.EDUCATION)
        survey_participation = SurveyParticipation(
            participant=subscription_edu.participant, survey=survey_2
        )
        survey_participation.save()
        last_saved_item = SurveyParticipation.objects.last()
        self.assertEqual(last_saved_item.survey.label, "second_survey_edu")
        self.assertEqual(last_saved_item.participant.first_name, "Prudence")
