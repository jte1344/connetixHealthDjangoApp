from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import UserForm
import json
import requests
from collections import OrderedDict
from datetime import datetime
from time import time
from lxml import html,etree
import requests,re
import os,sys


def index(request):
    with open('siteData.JSON') as f:
      site = json.load(f)

      print(site)

    if request.method == 'POST':
        form = UserForm(request.POST)

        if form.is_valid():

            #gets user defined variables
            location = request.POST["location"]
            medication = request.POST["medication"]

            location = parse(location)

            print(location)


            data = {'location': location, 'date': date}

            return render(request, 'index/index.html', {'data': data, 'site': site})

    else:

        form = UserForm()
        return render(request, 'index/index.html', {'form': form, 'site': site})
