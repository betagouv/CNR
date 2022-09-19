from django.contrib import messages
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse

from public_website.email_provider import send_participant_profile_to_email_provider
from public_website.forms import RegisterForm, ProfileForm

from public_website.models import Participant


def index_view(request):

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            new_participant = form.save()
            new_participant.sub = make_password(new_participant.email)

            new_participant.registration_success = send_participant_profile_to_email_provider(
                new_participant, 
                has_profile_information=False)
            
            new_participant.save()
            return redirect('inscription_test', sub=new_participant.sub)
    
    if request.method == "GET":
        form = RegisterForm
    
    return render(request, "public_website/index_test.html", {'form':form})


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


def inscription_view(request, sub, *args, **kwargs):

    if request.method == "POST":
        form = ProfileForm(request.POST)
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
        form = ProfileForm()
        redirect('index')

def inscription_view_test(request, sub, *args, **kwargs):

    if request.method == "POST":

        existing_user = Participant.objects.filter(sub=sub)
        if existing_user.exists():
            form = ProfileForm(request.POST, instance=existing_user[0])
            if form.is_valid():
                new_participant = form.save(commit=True)
                new_participant.registration_success = send_participant_profile_to_email_provider(
                    new_participant,
                    has_profile_information=True)
                new_participant.save()
                thank_you_message = "Données enregistrées. Merci pour votre intérêt !"
                messages.success(request, thank_you_message)
            else:
                error_message = "Formulaire invalide. Veuillez vérifier vos réponses."
                messages.error(request, error_message)

    if request.method == "GET":
        form = ProfileForm()

    return render(request, "public_website/inscription_test.html", {"sub":sub, "form": form})


def fonctionnement_view(request):
    return render(request, "public_website/fonctionnement.html")
