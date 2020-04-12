from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import JsonResponse
from .forms import *
from time import sleep
from bs4 import BeautifulSoup
from collections import OrderedDict
from datetime import datetime
from time import time
from lxml import html,etree
import json
import requests
import bs4
import requests,re
import os,sys
import NihMedicationInteraction

def RxScrape(medication):

    url = "https://www.drugs.com/price-guide/{0}".format(medication)

    # Make a GET request to fetch the raw HTML content
    html_content = requests.get(url).text

    # Parse the html content
    soup = BeautifulSoup(html_content, "lxml")

    drugName = []
    data = []
    table = soup.find_all("table", attrs={"class": "data-list"})
    tableName = soup.find_all("div", attrs={"class": "dosage-block"})
    for i in range(0, len(tableName)):
        drugName.append(tableName[i].text)

        quantity = []
        quantityData = table[i].find_all("td", attrs={"class": ""})
        for j in range(0, len(quantityData)):
            quantity.append(quantityData[j].text)

        unitPrice = []
        totalPrice = []
        priceData = table[i].find_all("td", attrs={"class": "text-right"})
        for k in range(0, len(quantityData)):
            unitPrice.append(priceData[0].text)
            priceData.pop(0)
            totalPrice.append(priceData[0].text)
            priceData.pop(0)

        data.append({"title" : drugName[i], "quantity" : quantity, "unitPrice" : unitPrice, "totalPrice" : totalPrice})

    return data


def index(request):


    with open('siteData.JSON') as f:
      site = json.load(f)

    return render(request, 'index/index.html', {'site': site})


#this method gets called when a user visits /interactions on the siteName
#call comes from index/urls.py
def interactions(request):

    #this loads in site data like the name and logo(when we make one) and saves it to the site variable
    with open('siteData.JSON') as f:
        #always send this to the front end in render calls
        site = json.load(f)

    return render(request, 'index/interactions.html', {'site': site}) #always send in site like this



def local(request, medication):

    data = RxScrape(medication)

    return JsonResponse(data, safe=False)




def interactionsAPI(request, medication):

    data = NihMedicationInteraction.call_interactions(medication)

    return JsonResponse(data, safe=False)
