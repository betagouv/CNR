import logging
import secrets

from django.contrib import messages
from django.shortcuts import redirect, render, reverse

from public_website.models import Participant

from . import forms, models

logger = logging.getLogger(__name__)


def survey_intro_view(request):
    uuid = request.session.get("uuid", None)

    if not uuid:
        return redirect("index")
    try:
        current_participant = Participant.objects.get(uuid=request.session["uuid"])
    except Participant.DoesNotExist:
        return redirect("index")
    surveys = current_participant.get_available_surveys()
    subscriptions = current_participant.subscriptions.values_list("theme", flat=True)
    pre_checked_surveys = [
        survey.label for survey in surveys.filter(theme__in=subscriptions)
    ]

    if request.method == "GET":
        form = forms.SelectSurveysForm(surveys=surveys)
        return render(
            request,
            "surveys/survey_intro.html",
            {
                "form": form,
                "checked": pre_checked_surveys,
                "title": "Contribuez dès maintenant",
            },
        )

    if request.method == "POST":
        form = forms.SelectSurveysForm(data=request.POST, surveys=surveys)
        if form.is_valid():
            selected_surveys = form.cleaned_data["surveys"]
            request.session["selected_surveys"] = selected_surveys
            request.session.save()
            return redirect(reverse("survey", kwargs={"label": selected_surveys[0]}))
        else:
            return redirect(reverse("survey_outro"))


def survey_view(request, label):
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

    def get_current_next_surveys(survey_list: list, current_label: str) -> tuple:
        try:
            current_survey = models.Survey.objects.get(label=current_label)
            current_survey_step = survey_list.index(current_label) + 1
            is_last_step = len(survey_list) == current_survey_step
            if is_last_step:
                next_survey = None
            else:
                next_survey_label = survey_list[current_survey_step]
                next_survey = models.Survey.objects.get(label=next_survey_label)
        except models.Survey.DoesNotExist:
            current_survey = None

        return (current_survey, next_survey, current_survey_step)

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
        selected_surveys, participant = format_request_session(request.session, label)
    except KeyError:
        return redirect(reverse("survey_intro"))

    current_survey, next_survey, current_survey_step = get_current_next_surveys(
        selected_surveys, label
    )

    if not current_survey:
        return redirect(reverse("survey_outro"))

    has_participated_before = current_survey in participant.participations.all()
    if has_participated_before:
        # TODO display this message is user tries to access
        #  survey they already filled out
        return redirect(reverse("survey-intro"))

    if request.method == "POST":
        questions = current_survey.get_questions()
        form = forms.SurveyForm(request.POST, questions=questions)
        if form.is_valid():
            anonymize_and_save_answers(participant, form, current_survey)

            if not next_survey:
                return redirect(reverse("survey_outro"))
            else:
                request.session.save()
                return redirect(reverse("survey", kwargs={"label": next_survey.label}))
        else:
            error_message = "Formulaire invalide. Veuillez vérifier vos réponses."
            messages.error(request, error_message)

    next_theme = next_survey.hr_label if next_survey else "fin du questionnaire"
    questions = current_survey.get_questions()
    form = forms.SurveyForm(questions=questions)
    return render(
        request,
        "surveys/survey.html",
        {
            "form": form,
            "theme": current_survey.hr_label,
            "label": label,
            "next_theme": next_theme,
            "current_step": current_survey_step,
            "steps": len(selected_surveys),
            "questions": questions,
            "title": current_survey.hr_label,
        },
    )


def survey_outro_view(request):
    uuid = request.session.get("uuid", None)
    if uuid:
        del request.session["uuid"]
        return render(
            request,
            "surveys/survey_outro.html",
            {"title": "Merci pour votre contribution"},
        )
    else:
        logging.info("## Error : no UUID, return user to index")
        return redirect("index")
