from django.contrib import messages
from django.shortcuts import render

from public_website.email_provider import send_participant_profile_to_email_provider
from public_website.forms import InscriptionForm


def index_view(request):
    return render(request, "public_website/index.html")


def cgu_view(request):
    return render(request, "public_website/cgu.html")


def mentions_legales_view(request):
    return render(request, "public_website/mentions_legales.html")


def accessibilite_view(request):
    return render(request, "public_website/accessibilite.html")


def donnees_personnelles_view(request):
    return render(request, "public_website/donnees_personnelles.html")

def survey_view(request):
    return render(request, "public_website/survey.html")

def survey_intro_view(request):
    return render(request, "public_website/survey_intro.html")

def survey_outro_view(request):
    return render(request, "public_website/survey_outro.html")


def inscription_view(request):

    if request.method == "POST":
        form = InscriptionForm(request.POST)

        if form.is_captcha_valid() and form.is_valid():
            new_participant = form.save()
            new_participant.registration_success = (
                send_participant_profile_to_email_provider(new_participant)
            )
            new_participant.save()
            thank_you_message = "Données enregistrées. Merci pour votre intérêt !"
            messages.success(request, thank_you_message)
        else:
            error_message = "Formulaire invalide. Veuillez vérifier vos réponses."
            messages.error(request, error_message)

    if request.method == "GET":
        form = InscriptionForm()
    return render(request, "public_website/inscription.html", {"form": form})


def fonctionnement_view(request):
    return render(request, "public_website/fonctionnement.html")
