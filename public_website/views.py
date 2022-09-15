from django.shortcuts import render


def index_view(request):
    return render(request, 'public_website/index.html')