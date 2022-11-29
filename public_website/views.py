from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import redirect, render

from public_website.email_provider import send_participant_profile_to_email_provider
from public_website.forms import ProfileForm, RegisterForm
from public_website.models import Participant


def index_view(request):

    form = RegisterForm()

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_captcha_valid() and form.is_valid():
            try:
                participant = Participant.objects.get(email=form.cleaned_data["email"])
            except Participant.DoesNotExist:
                participant = Participant.objects.create(
                    email=form.cleaned_data["email"]
                )
                participant.registration_success = (
                    send_participant_profile_to_email_provider(participant)
                )
                participant.save()

            request.session["uuid"] = str(participant.uuid)
            return redirect("inscription")
        else:
            form = RegisterForm(request.POST, initial=form.data)
            error_message = "Formulaire invalide. Veuillez vérifier vos réponses."
            messages.error(request, error_message)

    return render(request, "public_website/index.html", {"form": form})


def cgu_view(request):
    return render(
        request,
        "public_website/cgu.html",
        {"title": "Conditions générales d'utilisation"},
    )


def mentions_legales_view(request):
    return render(
        request, "public_website/mentions_legales.html", {"title": "Mentions légales"}
    )


def accessibilite_view(request):
    return render(
        request,
        "public_website/accessibilite.html",
        {"title": "Déclaration d’accessibilité"},
    )


def accessibilite_demarche_view(request):
    return render(
        request,
        "public_website/accessibilite_demarche.html",
        {"title": "Démarche d'accessibilité"},
    )


def confidentialite_view(request):
    return render(
        request,
        "public_website/confidentialite.html",
        {"title": "Politique de confidentialité"},
    )


def inscription_view(request):
    form = ProfileForm()

    if request.method == "GET":
        if "uuid" in request.session:
            existing_participant = Participant.objects.filter(
                uuid=request.session["uuid"]
            )
            if existing_participant.exists():
                form = ProfileForm(instance=existing_participant[0])

    if request.method == "POST":
        form = ProfileForm(request.POST)
        if form.is_captcha_valid() and form.is_valid():
            try:
                participant = Participant.objects.get(email=form.cleaned_data["email"])
                if participant.has_profile:
                    info_message = (
                        "Votre profil est déjà rempli. Il n'a pas été mis à jour."
                    )
                    messages.info(request, info_message)
                    request.session["uuid"] = str(participant.uuid)
                    return redirect("survey_intro")
                else:
                    form = ProfileForm(request.POST, instance=participant)
            except Participant.DoesNotExist:
                pass
            try:
                participant = form.save()
                participant.registration_success = (
                    send_participant_profile_to_email_provider(participant)
                )
                participant.save()
            except IntegrityError:
                form = ProfileForm(request.POST, initial=form.data)
                error_message = "Formulaire invalide. Veuillez vérifier vos réponses."
                messages.error(request, error_message)
                return render(
                    request,
                    "public_website/inscription.html",
                    {"form": form, "title": "Inscription"},
                )

            success_message = "Votre inscription est enregistrée : vous serez tenu au courant des consultations à venir sur vos thématiques sélectionnées."
            messages.success(request, success_message)
            request.session["uuid"] = str(participant.uuid)
            return redirect("survey_intro")
        else:
            form = ProfileForm(request.POST, initial=form.data)
            error_message = "Formulaire invalide. Veuillez vérifier vos réponses."
            messages.error(request, error_message)

    return render(
        request,
        "public_website/inscription.html",
        {"form": form, "title": "Inscription"},
    )


def fonctionnement_view(request):
    return render(
        request, "public_website/fonctionnement.html", {"title": "Une nouvelle méthode"}
    )

def climat_biodiversite_view(request):
    return render(
        request, "public_website/climat_biodiversite.html", {"title": "Climat et Biodiversité"}
    )

def bien_vieillir_view(request):
    return render(
        request, "public_website/bien_vieillir.html", {"title": "Bien vieillir"}
    )

def sante_view(request):
    return render(
        request, "public_website/sante.html", {"title": "Santé"}
    )

def logement_view(request):
    return render(
        request, "public_website/logement.html", {"title": "Logement"}
    )

def numerique_view(request):
    return render(
        request, "public_website/numerique.html", {"title": "Numérique"}
    )

def travail_view(request):
    return render(
        request, "public_website/assises-du-travail.html", {"title": "Assises du travail"}
    )

def jeunesse_view(request):
    return render(
        request, "public_website/jeunesse.html", {"title": "Jeunesse"}
    )

def economie_view(request):
    return render(
        request, "public_website/economie.html", {"title": "Modèle productif et social"}
    )

def education_view(request):
    return render(
        request, "public_website/education.html", {"title": "Notre école"}
    )

def resultats_view(request):
    return render(
        request, "public_website/resultats.html", {"title": "Résultats"}
    )

def choix_thematique_view(request):
    return render(
        request, "public_website/choix-thematique.html", {"title": "Choix de la thématique"}
    )