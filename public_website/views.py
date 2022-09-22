from django.contrib import messages
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse

from public_website.email_provider import send_participant_profile_to_email_provider
from public_website.forms import RegisterForm, ProfileForm

from public_website.models import Participant


def index_view(request):

    form = RegisterForm()

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_captcha_valid() and form.is_valid():
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


def inscription_view(request):

    form = ProfileForm()

    if request.method == "GET":
        if 'uuid' in request.session:
            existing_participant = Participant.objects.filter(uuid=request.session['uuid'])
            if existing_participant.exists():
                form = ProfileForm(instance=existing_participant[0])

    if request.method == "POST":
        form = ProfileForm(request.POST)

        if form.is_captcha_valid() and form.is_valid():            
            
            try:
                participant = Participant.objects.get(email=form.cleaned_data['email'])
                
                if participant.has_profile:
                    # TODO error message
                    return redirect('/survey-intro/')
                else: 
                    participant.first_name=form.cleaned_data['first_name'],
                    participant.postal_code=form.cleaned_data['postal_code'],
                    participant.participant_type=form.cleaned_data['participant_type']
                    # participant = form.save(instance=participant)
                    # form = ProfileForm(request.POST, instance=participant)
               

            except Participant.DoesNotExist:
                participant = models.Participant(
                    email=form.cleaned_data['email'],
                    first_name=form.cleaned_data['first_name'],
                    postal_code=form.cleaned_data['postal_code'],
                    participant_type=form.cleaned_data['participant_type'])
            
            participant.save()
            preferred_themes = form.cleaned_data["prefered_themes"]
            for theme in preferred_themes:
                subscription = models.Subscription(participant_id=participant.id, theme=theme)
                subscription.save()
                    
            participant.registration_success = send_participant_profile_to_email_provider(
                participant,
                has_profile_information=True)
            participant.save()
            return redirect('survey_intro')
        else:
            error_message = "Formulaire invalide. Veuillez vérifier vos réponses."
            messages.error(request, error_message)


    return render(request, "public_website/inscription.html", {"form": form})


def fonctionnement_view(request):
    return render(request, "public_website/fonctionnement.html")
