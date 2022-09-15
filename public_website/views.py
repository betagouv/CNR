from django.shortcuts import render
from public_website.forms import FormulaireForm
from django.http import HttpResponseRedirect
from django.shortcuts import redirect


def index_view(request):
    return render(request, 'public_website/index.html')


def formulaire_test(request):
    if request.method == 'POST':
        form = FormulaireForm(request.POST)
        if form.is_valid():
            return redirect('formulaire_test')
        else:
            return HttpResponseRedirect('index')
    if request.method == 'GET':
        form = FormulaireForm()
    return render(request, "public_website/formulaire_test.html", {'form': form.as_p()})

