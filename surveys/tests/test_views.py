import uuid

from django.test import TestCase, tag
from django.urls import resolve, reverse

from public_website.factories import ParticipantFactory
from public_website.models import Participant, Theme
from surveys import views
from surveys.factories import (
    SurveyFactory,
    SurveyParticipationFactory,
    SurveyQuestionFactory,
)
from surveys.models import Survey, SurveyAnswer, SurveyParticipation, SurveyQuestion


@tag("views")
class TestSurveyIntro(TestCase):
    def setUp(self) -> None:
        self.participant = ParticipantFactory()
        session = self.client.session
        session["uuid"] = str(self.participant.uuid)
        session.save()

    def test_survey_home_url_calls_right_view(self):
        match = resolve("/participation-intro/")
        self.assertEqual(match.func, views.survey_home_view)

    def test_survey_home_url_calls_right_template(self):
        response = self.client.get("/participation-intro/")
        self.assertTemplateUsed(response, "surveys/survey_home.html")

    def test_survey_home_response_contains_welcome_message(self):
        response = self.client.get("/participation-intro/")
        self.assertContains(response, "Donnez votre avis dès maintenant")

    def test_no_uuid_returns_to_index(self):
        """Checks that the page cannot be reached without providing an uuid."""
        session = self.client.session
        session.pop("uuid")
        session.save()
        response = self.client.get("/participation-intro/")
        self.assertRedirects(response, reverse("index"))

    def test_invalid_uuid_returns_to_index(self):
        """Checks that the page cannot be reached with an unregistered uuid."""
        random_uuid = uuid.uuid4()
        self.assertFalse(Participant.objects.filter(uuid=random_uuid).exists())

        session = self.client.session
        session["uuid"] = str(random_uuid)
        session.save()
        response = self.client.get("/participation-intro/")
        self.assertRedirects(response, reverse("index"))

    def test_survey_home_links_to_all_existing_surveys(self):
        response = self.client.get("/participation-intro/")
        for survey in Survey.objects.all():
            self.assertContains(response, f'<a href="/participation/{survey.label}">')

    def test_displays_special_message_when_answered_every_survey(self):
        """Checks that participant gets a special message when all surveys are answered."""
        for survey in Survey.objects.all():
            SurveyParticipation(participant=self.participant, survey=survey).save()

        already_answered = set(
            [
                participation.survey
                for participation in self.participant.participations.all()
            ]
        )
        self.assertTrue(list(already_answered) == list(Survey.objects.all()))
        response = self.client.get("/participation-intro/")
        self.assertContains(
            response,
            "Vous avez répondu à tous les questionnaires disponibles pour l&#x27;instant. Merci pour votre contribution !",
        )


@tag("views")
class TestSurvey(TestCase):
    def setUp(self) -> None:
        self.current_participant = ParticipantFactory()
        self.youth_survey = SurveyFactory(label="label_1", theme=Theme.JEUNESSE)

        SurveyParticipationFactory(
            participant=self.current_participant, survey=self.youth_survey
        )
        self.climate_survey = SurveyFactory(label="CLIMAT_1", theme=Theme.CLIMAT)
        session = self.client.session
        session["uuid"] = str(self.current_participant.uuid)
        session.save()

    def test_survey_url_calls_right_view(self):
        valid_label = self.climate_survey.label
        match = resolve(f"/participation/{valid_label}")
        self.assertEqual(match.func, views.survey_view)

    def test_survey_url_calls_right_template(self):
        valid_label = self.climate_survey.label
        response = self.client.get(f"/participation/{valid_label}")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "surveys/survey.html")

    def test_invalid_survey_returns_to_survey_intro(self):
        response = self.client.get("/participation/not_a_label")
        self.assertRedirects(response, reverse("survey_home"))

    def test_survey_response_contains_welcome_message(self):
        self.assertFalse(
            SurveyParticipation.objects.filter(
                participant=self.current_participant, survey=self.climate_survey
            ).exists()
        )
        response = self.client.get(f"/participation/{self.climate_survey.label}")
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            f"<h1>Questions sur la thématique « {self.climate_survey.hr_label} »</h1>",
        )

    def test_cannot_reach_already_answered_survey(self):
        """Tests that participant cannot reach a survey to which they already answered, and that they get an error message saying so."""
        self.assertTrue(
            SurveyParticipation.objects.filter(
                participant=self.current_participant, survey=self.youth_survey
            ).exists()
        )
        response = self.client.get(
            f"/participation/{self.youth_survey.label}", follow=True
        )
        self.assertRedirects(response, "/participation-intro/")
        self.assertContains(
            response,
            f"Vous avez déjà répondu au questionnaire {self.youth_survey.hr_label}.",
        )


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

    def test_valid_contribution_returns_to_survey_home(self):
        """Checks valid contributions returns to survey_home and get confirmation message"""
        response = self.client.get("/participation/survey_test_2")
        self.assertContains(response, self.survey_2_question_1.hr_label)
        response_2 = self.client.post(
            "/participation/survey_test_2",
            {
                "survey_2_Q-1-A-0": "Je pense que cette idée est bonne",
                "survey_2_Q-1-A-1": "J'ajouterais que j'aimerais la voir appliquée localement",
                "survey_2_Q-2-A-0": "je ne suis pas assez expert pour avoir une opinion",
            },
            follow=True,
        )
        self.assertRedirects(
            response_2,
            "/participation-intro/",
            status_code=302,
            target_status_code=200,
            msg_prefix="",
            fetch_redirect_response=True,
        )
        self.assertContains(
            response_2, "Votre contribution a bien été enregistrée. Merci !"
        )

    def test_empty_participation_is_not_saved(self):
        """Checks that empty contributions are not saved and don't prevent users from re-submitting in the future."""
        survey = SurveyFactory()
        participant = ParticipantFactory()
        self.assertFalse(
            SurveyParticipation.objects.filter(
                participant=participant, survey=survey
            ).exists()
        )
        last_answer_in_db = SurveyAnswer.objects.last()

        self.client.post(
            "/participation/survey_test_2",
            {
                "survey_2_Q-1-A-0": "",
                "survey_2_Q-1-A-1": "",
                "survey_2_Q-1-A-2": "",
                "survey_2_Q-1-A-3": "",
                "survey_2_Q-1-A-4": "",
                "survey_2_Q-2-A-0": "",
            },
        )
        self.assertFalse(
            SurveyParticipation.objects.filter(
                participant=participant, survey=survey
            ).exists()
        )
        self.assertEqual(SurveyAnswer.objects.last(), last_answer_in_db)

    # TODO can't resubmit an already submitted survey + message
