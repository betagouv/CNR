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
            participant = Participant.objects.filter(email=form.cleaned_data['email'])
            if participant.exists():
                participant = participant[0]
            else:
                new_participant = form.save()
                new_participant.registration_success = send_participant_profile_to_email_provider(
                    new_participant,
                    has_profile_information=False)
                new_participant.save()
                participant = new_participant

            request.session['uuid'] = str(participant.uuid)
            return redirect('inscription')
        else:
            error_message = "Formulaire invalide. Veuillez vérifier vos réponses."
            messages.error(request, error_message)
    
    if request.method == "GET":
        form = RegisterForm
    
    return render(request, "public_website/index.html", {'form':form})


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


def inscription_view(request, *args, **kwargs):

    if request.method == "POST":
        form = ProfileForm(request.POST)

        if 'uuid' in request.session:
            session_uuid = request.session['uuid']
            existing_participant = Participant.objects.filter(uuid=session_uuid)
        else:
            existing_participant = Participant.objects.filter(email=form.data['email'])
        if existing_participant.exists():
            form = ProfileForm(request.POST, instance=existing_participant[0])            

        if form.is_captcha_valid() and form.is_valid():
            new_participant = form.save(commit=True)
            new_participant.registration_success = send_participant_profile_to_email_provider(
                new_participant,
                has_profile_information=True)
            new_participant.save()
            # confirmation_message = "Votre inscription est enregistrée : vous serez tenu au courant des consultations à venir sur vos thématiques sélectionnées."
            # messages.success(request, confirmation_message)
            return redirect('survey_intro')
        else:
            error_message = "Formulaire invalide. Veuillez vérifier vos réponses."
            messages.error(request, error_message)

    if request.method == "GET":
        
        if 'uuid' in request.session:
            existing_participant = Participant.objects.filter(uuid=request.session['uuid'])
            if existing_participant.exists():
                form = ProfileForm(instance=existing_participant[0])
        else:
            form = ProfileForm()

    return render(request, "public_website/inscription.html", {"form": form})


def fonctionnement_view(request):
    return render(request, "public_website/fonctionnement.html")
