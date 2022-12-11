from django.test import TestCase, tag
from django.urls import resolve, reverse

from public_website.factories import ParticipantFactory
from public_website.models import Theme
from surveys import views
from surveys.factories import (
    SurveyFactory,
    SurveyParticipationFactory,
    SurveyQuestionFactory,
)
from surveys.models import SurveyAnswer, SurveyParticipation, SurveyQuestion


@tag("views")
class TestSurvey(TestCase):
    def setUp(self) -> None:
        self.current_participant = ParticipantFactory()
        self.survey_1 = SurveyFactory(label="label_1")
        session = self.client.session
        session["uuid"] = str(self.current_participant.uuid)
        session["selected_surveys"] = ["label_1"]
        session.save()

    def test_survey_url_calls_right_view(self):
        match = resolve("/participation/label_1")
        self.assertEqual(match.func, views.survey_view)

    def test_survey_url_calls_right_template(self):
        response = self.client.get("/participation/label_1")
        self.assertTemplateUsed(response, "surveys/survey.html")

    def test_survey_response_contains_welcome_message(self):
        response = self.client.get("/participation/label_1")
        self.assertContains(response, "Questionnaire")


class TestSurveyView(TestCase):
    def setUp(self):
        self.answer_type = SurveyQuestion.AnswerType

        self.survey_1 = SurveyFactory(theme=Theme.EDUCATION, label="survey_test_1")
        SurveyQuestionFactory(
            survey=self.survey_1, answer_type=self.answer_type.THREE_TEXT_FIELD
        )
        SurveyQuestionFactory(
            survey=self.survey_1, answer_type=self.answer_type.ONE_TEXT_FIELD
        )

        self.survey_2 = SurveyFactory(theme=Theme.EDUCATION, label="survey_test_2")
        self.survey_2_question_1 = SurveyQuestionFactory(
            survey=self.survey_2,
            label="survey_2_Q-1",
            hr_label="Is this a good idea ?",
            answer_type=self.answer_type.FIVE_TEXT_FIELD,
        )
        SurveyQuestionFactory(
            survey=self.survey_2,
            label="survey_2_Q-2",
            answer_type=self.answer_type.ONE_TEXT_FIELD,
        )
        self.survey_3 = SurveyFactory(theme=Theme.EDUCATION, label="survey_test_3")
        self.survey_3_question_1 = SurveyQuestionFactory(
            survey=self.survey_3, hr_label="What do you think ?"
        )
        self.survey_4 = SurveyFactory(theme=Theme.SANTE)

        self.participation = SurveyParticipationFactory(survey=self.survey_1)
        self.known_participant = self.participation.participant

        self.session = self.client.session
        self.session["uuid"] = str(self.known_participant.uuid)
        self.session["selected_surveys"] = [
            "survey_test_2",
            self.survey_3.label,
        ]
        self.session.save()

    def test_survey_view_with_known_uuid_provided(self):
        response = self.client.get("/participation/" + self.survey_3.label)
        self.assertTemplateUsed(response, "surveys/survey.html")

    def test_well_formatted_post_creates_answers_instances(self):

        self.client.post(
            "/participation/survey_test_2",
            {
                "survey_2_Q-1-A-0": "Je pense que cette idée est bonne",
                "survey_2_Q-1-A-1": "J'ajouterais que j'aimerais la voir appliquée localement",
                "survey_2_Q-2-A-0": "je ne suis pas assez expert pour avoir une opinion",
            },
        )
        self.assertEqual(SurveyAnswer.objects.all().count(), 3)
        S2_Q1_answers = SurveyAnswer.objects.all().filter(
            survey_question=self.survey_2_question_1
        )
        self.assertEqual(S2_Q1_answers.first().rank, 0)
        self.assertEqual(S2_Q1_answers.last().rank, 1)
        self.assertTrue(S2_Q1_answers.first().survey_response_id)
        self.assertEqual(
            S2_Q1_answers.first().survey_response_id,
            S2_Q1_answers.last().survey_response_id,
        )
        self.assertEqual(SurveyParticipation.objects.all().count(), 2)

        # TOD0: test the attributes of the instances

    def test_all_surveys_appear_in_order(self):
        response = self.client.get("/participation/survey_test_2")
        self.assertContains(response, self.survey_2_question_1.hr_label)
        response_2 = self.client.post(
            "/participation/survey_test_2",
            {
                "survey_2_Q-1-A-0": "Je pense que cette idée est bonne",
                "survey_2_Q-1-A-1": "J'ajouterais que j'aimerais la voir appliquée localement",
                "survey_2_Q-2-A-0": "je ne suis pas assez expert pour avoir une opinion",
            },
        )

        self.assertRedirects(
            response_2,
            "/participation/" + self.survey_3.label,
            status_code=302,
            target_status_code=200,
            msg_prefix="",
            fetch_redirect_response=True,
        )

    def test_empty_participation_is_not_saved(self):
        """Checks that empty contributions are not saved and don't prevent users from re-submitting in the future."""
        survey = SurveyFactory()
        participant = ParticipantFactory()
        self.assertFalse(SurveyParticipation.objects.filter(participant=participant).exists())
        last_answer_in_db = SurveyAnswer.objects.last()

        response = self.client.post(
            '/participation/survey_test_2',
            {
                "survey_2_Q-1-A-0": "",
                "survey_2_Q-1-A-1": "",
                "survey_2_Q-1-A-2": "",
                "survey_2_Q-1-A-3": "",
                "survey_2_Q-1-A-4": "",
                "survey_2_Q-2-A-0": "",
            })
        
        self.assertFalse(SurveyParticipation.objects.filter(participant=participant).exists())
        self.assertEqual(SurveyAnswer.objects.last(), last_answer_in_db)


@tag("views")
class TestSurveyIntro(TestCase):
    def setUp(self) -> None:
        self.prudence = ParticipantFactory()
        session = self.client.session
        session["uuid"] = str(self.prudence.uuid)
        session.save()

    def test_survey_intro_url_calls_right_view(self):
        match = resolve("/participation-intro/")
        self.assertEqual(match.func, views.survey_intro_view)

    def test_survey_intro_url_calls_right_template(self):
        response = self.client.get("/participation-intro/")
        self.assertTemplateUsed(response, "surveys/survey_intro.html")

    def test_survey_intro_response_contains_welcome_message(self):
        response = self.client.get("/participation-intro/")
        self.assertContains(response, "Donnez votre avis dès maintenant")


@tag("views")
class TestSurveyOutro(TestCase):
    def setUp(self) -> None:
        self.prudence = ParticipantFactory()
        self.survey_1 = SurveyFactory(label="label_1")
        self.session = self.client.session
        self.session["uuid"] = str(self.prudence.uuid)
        self.session.save()

    def test_survey_outro_url_calls_right_view(self):
        match = resolve("/participation-fin/")
        self.assertEqual(match.func, views.survey_outro_view)

    def test_survey_outro_url_calls_right_template(self):
        response = self.client.get("/participation-fin/")
        self.assertTemplateUsed(response, "surveys/survey_outro.html")

    def test_survey_outro_response_contains_welcome_message(self):
        response = self.client.get("/participation-fin/")
        self.assertContains(response, "Merci pour votre contribution")

    def test_survey_outro_destroys_uuid(self):
        self.assertTrue(self.client.session.get("uuid", None))
        response = self.client.get("/participation-fin/")
        self.assertTemplateUsed(response, "surveys/survey_outro.html")
        self.assertFalse(self.client.session.get("uuid", None))

    def test_survey_outro_redirects_unknown_participant_to_index(self):
        self.session["uuid"] = None
        self.session.save()
        response = self.client.get("/participation-fin/")
        self.assertRedirects(response, "/")
