from django.contrib import messages
from django.shortcuts import render

from public_website.forms import InscriptionForm


def index_view(request):
    return render(request, "public_website/index.html")


def inscription_view(request):

    if request.method == "POST":
        form = InscriptionForm(request.POST)
        if form.is_valid():
            form.save()
            # Send information to sendinblue
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
