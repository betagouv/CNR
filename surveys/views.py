import logging
import secrets

from django.contrib import messages
from django.shortcuts import redirect, render, reverse

from public_website.models import Participant, Theme
from surveys.models import Survey

from . import forms, models

logger = logging.getLogger(__name__)


def survey_home_view(request):
    uuid = request.session.get("uuid", None)

    if not uuid:
        return redirect("index")
    try:
        current_participant = Participant.objects.get(uuid=request.session["uuid"])
    except Participant.DoesNotExist:
        return redirect("index")
    surveys = current_participant.get_available_surveys()
    subscriptions = current_participant.subscriptions.values_list("theme", flat=True)
    already_answered = set([participation.survey for participation in current_participant.participations.all()])

    if list(already_answered) == list(Survey.objects.all()):
        info_message = ("Vous avez répondu à tous les questionnaires disponibles pour l'instant. Merci pour votre contribution !")
        messages.info(request, info_message)

    return render(
        request,
        "surveys/survey_home.html",
        {
            "themes_surveys": Survey.objects.all(),
            "already_answered": already_answered,
            "title": "Contribuez dès maintenant",
        },
    )


def survey_view(request, label):

    def get_participant(session):
        uuid = session.get("uuid", None)
        try:
            return Participant.objects.get(uuid=uuid)
        except Participant.DoesNotExist:
            raise KeyError

    def label_is_known(label):
        if label in [theme for theme in Theme]:
            return True

    def format_request_session(session, label):
        uuid = session.get("uuid", None)
        selected_surveys = session.get("selected_surveys", [])
        expected_label = label in selected_surveys

        for mandatory_attribute in [uuid, expected_label, selected_surveys]:
            if not mandatory_attribute:
                logger.info(f"### missing {mandatory_attribute}")
                raise KeyError

        try:
            participant = Participant.objects.get(uuid=uuid)
        except Participant.DoesNotExist:
            raise KeyError

        return (selected_surveys, participant)

    def anonymize_and_save_answers(participant, valid_form, current_survey):
        survey_response_id = secrets.token_urlsafe(16)
        for field_name, field_object in valid_form.fields.items():
            answer = valid_form.cleaned_data[field_name]
            if answer:
                rank = int(field_name.split("-A-")[-1])
                models.SurveyAnswer(
                    survey_question=models.SurveyQuestion.objects.get(
                        label=field_object.label
                    ),
                    rank=rank,
                    answer=answer,
                    postal_code=participant.postal_code,
                    survey_response_id=survey_response_id,
                ).save()

        models.SurveyParticipation(
            participant=participant, survey=current_survey
        ).save()

    try: 
        participant = get_participant(request.session)
        current_survey = models.Survey.objects.get(label=label)
    except KeyError:
        return redirect(reverse('survey_home'))
    except Survey.DoesNotExist:
        return redirect(reverse('survey_home'))

    already_answered = set([participation.survey for participation in participant.participations.all()])
    if current_survey in already_answered:
        info_message = f"Vous avez déjà répondu au questionnaire {current_survey.hr_label}."
        messages.info(request, info_message)
        return redirect(reverse("survey_home"))

    questions = current_survey.get_questions()
    if request.method == "GET":
        form = forms.SurveyForm(questions=questions)

    if request.method == "POST": 
        form = forms.SurveyForm(request.POST, questions=questions)
        if form.is_valid():
            if set(form.cleaned_data.values()) != {''}:
                anonymize_and_save_answers(participant, form, current_survey)

            request.session.save()
            success_message = "Votre contribution a bien été enregistrée. Merci !"
            messages.success(request, success_message)
            return redirect(reverse("survey_home"))
        else:
            error_message = "Formulaire invalide. Veuillez vérifier vos réponses."
            messages.error(request, error_message)

    return render(
            request,
            "surveys/survey.html",
            {
                "form": form,
                "theme": current_survey.hr_label,
                "label": label,
                "questions": questions,
                "title": current_survey.hr_label,
            })
