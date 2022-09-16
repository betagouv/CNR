from django.shortcuts import render
from public_website.forms import InscriptionForm
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib import messages


def index_view(request):
    return render(request, 'public_website/index.html')


def inscription_view(request):
    if request.method == 'POST':
        form = InscriptionForm(request.POST)
        print(form.data)
        if form.is_valid():
            # Send information to sendinblue
            # print(form.cleaned_data)
            thank_you_message = 'Données enregistrées. Merci pour votre intérêt !'
            messages.success(request, thank_you_message)
        else:
            # Bad Request ? 
            error_message = "Formulaire invalide. Veuillez vérifier vos réponses."            
            messages.error(request, error_message)
    if request.method == 'GET':
        form = InscriptionForm()
    return render(request, "public_website/inscription.html", {'form': form})
