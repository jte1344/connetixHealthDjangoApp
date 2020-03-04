from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    # controller
    return render(request, "index/index.html")
