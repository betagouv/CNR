from django.shortcuts import render
from public_website.forms import FormulaireForm
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib import messages


def index_view(request):
    return render(request, 'public_website/index.html')


def formulaire_test(request):
    if request.method == 'POST':
        form = FormulaireForm(request.POST)
        if form.is_valid():
            thank_you_message = 'Données enregistrées. Merci pour votre intérêt !'
            messages.success(request, thank_you_message)
        else:
            error_message = "Formulaire invalide. Veuillez vérifier vos réponses."
            messages.error(request, error_message)
    if request.method == 'GET':
        form = FormulaireForm()
    return render(request, "public_website/formulaire_test.html", {'form': form.as_p()})
