from django.shortcuts import render


def index_view(request):
    context = {}
    return render(request, 'public_website/index.html', context)