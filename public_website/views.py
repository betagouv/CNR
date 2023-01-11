from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import redirect, render

from public_website.email_provider import send_participant_profile_to_email_provider
from public_website.forms import ProfileForm
from public_website.models import Participant


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
                    return redirect(
                        "/participez-au-conseil-national-de-la-refondation/"
                    )
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
            return redirect("/participez-au-conseil-national-de-la-refondation/")
        else:
            form = ProfileForm(request.POST, initial=form.data)
            error_message = "Formulaire invalide. Veuillez vérifier vos réponses."
            messages.error(request, error_message)

    return render(
        request,
        "public_website/inscription.html",
        {"form": form, "title": "Inscription"},
    )


def resultats_view(request):
    return render(request, "public_website/resultats.html", {"title": "Résultats"})


def choix_thematique_view(request):
    return render(
        request,
        "public_website/choix-thematique.html",
        {"title": "Choix de la thématique"},
    )
