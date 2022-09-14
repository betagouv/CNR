from django.shortcuts import render


def home_view(request):
    context = {}
    return render(request, 'public_website/index.html', context)