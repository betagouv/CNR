import logging

from django.contrib import messages
from django.shortcuts import redirect, render, reverse

from public_website.models import Participant, Theme

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
            {"form": form, "checked": pre_checked_surveys},
        )

    if request.method == "POST":
        form = forms.SelectSurveysForm(data=request.POST, surveys=surveys)
        if form.is_valid():
            selected_surveys = form.cleaned_data["surveys"]
            request.session["surveys"] = selected_surveys
            request.session["survey_steps"] = len(selected_surveys)
            request.session["survey_current_step"] = 1

            request.session.save()
            return redirect("survey")
        else:
            return render(
                request,
                "surveys/survey_intro.html",
                {"form": form, "checked": pre_checked_surveys},
            )


def survey_view(request):
    def get_current_next_surveys(
        selected_surveys: list, survey_current_step: int
    ) -> tuple:
        try:
            current_label = selected_surveys[survey_current_step - 1]
            current_survey = models.Survey.objects.get(label=current_label)
            is_last_step = (len(selected_surveys) - survey_current_step) == 0
            if is_last_step:
                next_survey = None
            else:
                next_survey_label = selected_surveys[survey_current_step]
                next_survey = models.Survey.objects.get(label=next_survey_label)
        except models.Survey.DoesNotExist:
            current_survey = None

        return (current_survey, next_survey)

    uuid = request.session.get("uuid", None)
    selected_surveys = request.session.get("surveys", None)
    survey_current_step = request.session.get("survey_current_step", None)

    for mandatory_attribute in [uuid, survey_current_step, selected_surveys]:
        if not mandatory_attribute:
            logger.info(f"### missing {mandatory_attribute}")
            return redirect("survey_intro")

    try:
        current_participant = Participant.objects.get(uuid=request.session["uuid"])
    except Participant.DoesNotExist:
        return redirect("index")

    current_survey, next_survey = get_current_next_surveys(
        selected_surveys, survey_current_step
    )

    if not current_survey:
        return redirect(reverse("participation-intro"))

    has_participated_before = current_survey in current_participant.participations.all()
    if has_participated_before:
        return redirect(reverse("survey-intro"))

    if request.method == "POST":
        questions = current_survey.get_questions()
        form = forms.SurveyForm(request.POST, questions=questions)
        if form.is_valid():
            for field_name, field_object in form.fields.items():
                answer = form.cleaned_data[field_name]
                if answer:
                    rank = int(field_name.split("-")[-1])
                    models.SurveyAnswer(
                        survey_question=models.SurveyQuestion.objects.get(
                            label=field_object.label
                        ),
                        rank=rank,
                        answer=answer,
                        postal_code=current_participant.postal_code,
                    ).save()

            models.SurveyParticipation(
                participant=current_participant, survey=current_survey
            ).save()
            # TODO display this message is user tries to access
            #  survey they already filled out
            survey_current_step += 1
            if not next_survey:
                return render(
                    request,
                    "surveys/survey_outro.html",
                )
            else:
                request.session["survey_current_step"] = survey_current_step
                request.session.save()
                current_survey, next_survey = get_current_next_surveys(
                    selected_surveys, survey_current_step
                )
                questions = current_survey.get_questions()

        else:
            error_message = "Formulaire invalide. Veuillez vérifier vos réponses."
            messages.error(request, error_message)

    if survey_current_step == len(selected_surveys):
        logger.info("### No more surveys to serve")
        return redirect("survey_outro")

    questions = current_survey.get_questions()
    form = forms.SurveyForm(questions=questions)

    return render(
        request,
        "surveys/survey.html",
        {
            "form": form,
            "theme": current_survey.theme.label,
            "next_theme": next_survey.theme.label,
            "current_step": int(survey_current_step),
            "steps": len(selected_surveys),
            "questions": questions,
        },
    )


def survey_outro_view(request):
    uuid = request.session.get("uuid", None)
    if uuid:
        del request.session["uuid"]
        return render(request, "surveys/survey_outro.html")
    else:
        logging.info("## Error : no UUID, return user to index")
        return redirect("index")
