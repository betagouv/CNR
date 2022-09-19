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
    uuid = request.session.get("uuid", None)
    selected_surveys = request.session.get("surveys", None)
    survey_steps = request.session.get("survey_steps", None)
    survey_current_step = request.session.get("survey_current_step", None)

    if not selected_surveys:
        logger.info("### ERROR No more surveys to serve")
        return redirect("survey_outro")

    for mandatory_attribute in [uuid, survey_steps, survey_current_step]:
        if not mandatory_attribute:
            logger.info(f"### missing {mandatory_attribute}")
            return redirect("survey_intro")

    try:
        current_participant = Participant.objects.get(uuid=request.session["uuid"])
    except Participant.DoesNotExist:
        return redirect("index")
    try:
        current_label = selected_surveys[0]
        current_survey = models.Survey.objects.get(label=current_label)
        current_theme = Theme[current_survey.theme].label
        if len(selected_surveys) > 1:
            next_label = selected_surveys[1]
            next_survey_theme = models.Survey.objects.get(label=next_label).theme
            next_theme = Theme[next_survey_theme].label
        else:
            next_theme = None
    except models.Survey.DoesNotExist:
        return redirect(reverse("index"))

    questions = current_survey.get_questions()

    if request.method == "GET":
        form = forms.SurveyForm(questions=questions)

    elif request.method == "POST":

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
            thank_you_message = "Données enregistrées. Merci pour votre intérêt !"
            messages.success(request, thank_you_message)
            if not request.session["surveys"]:
                return render(
                    request,
                    "surveys/survey_outro.html",
                )

            session = request.session
            session["surveys"].remove(current_label)
            session["survey_current_step"] += 1
            session.save()

        else:
            error_message = "Formulaire invalide. Veuillez vérifier vos réponses."
            messages.error(request, error_message)

    return render(
        request,
        "surveys/survey.html",
        {
            "form": form,
            "theme": current_theme,
            "next_theme": next_theme,
            "current_step": int(survey_current_step),
            "steps": int(survey_steps),
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
