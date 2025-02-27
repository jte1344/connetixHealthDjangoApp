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
    #pulls tables off parsed html content
    table = soup.find_all("table", attrs={"class": "data-list"})
    #gets tables (drug type) name
    tableName = soup.find_all("div", attrs={"class": "dosage-block"})
    #formats them in json style
    for i in range(0, len(tableName)):
        drugName.append(tableName[i].text)

        #formats quantity values for each element in table
        quantity = []
        quantityData = table[i].find_all("td", attrs={"class": ""})
        for j in range(0, len(quantityData)):
            quantity.append(quantityData[j].text)

        #formats pricing values for each element in table
        unitPrice = []
        totalPrice = []
        priceData = table[i].find_all("td", attrs={"class": "text-right"})
        for k in range(0, len(quantityData)):
            unitPrice.append(priceData[0].text)
            priceData.pop(0)
            totalPrice.append(priceData[0].text)
            priceData.pop(0)

        #formats all data into one variable to return to funct
        data.append({"title" : drugName[i], "quantity" : quantity, "unitPrice" : unitPrice, "totalPrice" : totalPrice})

    return data

#homepage call
def index(request):
    with open('siteData.JSON') as f:
      site = json.load(f)
    #responds with html and parameters
    return render(request, 'index/index.html', {'site': site})


#this method gets called when a user visits /interactions on the siteName
#call comes from index/urls.py
def interactions(request):
    #this loads in site data like the name and logo(when we make one) and saves it to the site variable
    with open('siteData.JSON') as f:
        #always send this to the front end in render calls
        site = json.load(f)
    #responds with html and parameters
    return render(request, 'index/interactions.html', {'site': site}) #always send in site like this



#this method gets called when a user visits /interactions on the siteName
#call comes from index/urls.py
def interactionsParam(request, medication):

    #this loads in site data like the name and logo(when we make one) and saves it to the site variable
    with open('siteData.JSON') as f:
        #always send this to the front end in render calls
        site = json.load(f)

    data = {"medication" : medication}
    #responds with html and parameters
    return render(request, 'index/interactionsParam.html', {'site': site, 'data': data}) #always send in site like this


#API call to local prices api (drugs.com)
def local(request, medication):
    data = RxScrape(medication)
    #responds with json
    return JsonResponse(data, safe=False)

#API call to NIH interactions API
def interactionsAPI(request, medication):
    data = NihMedicationInteraction.call_interactions(medication)
    #responds with json
    return JsonResponse(data, safe=False)

#API call to local pharmacies google maps API
def mapsAPI(request, location):
    #converts location inputted by user to a lat and longitude
    geocoding = requests.get("https://maps.googleapis.com/maps/api/geocode/json?address=" + location + "&key=YOUR_KEY_HERE").json()
    lat = str(geocoding['results'][0]['geometry']['location']['lat'])
    lng = str(geocoding['results'][0]['geometry']['location']['lng'])

    #searches for pharmacies in said lat/lng
    data = requests.get("https://maps.googleapis.com/maps/api/place/textsearch/json?query=pharmacy&location=" + lat + "," + lng + "&radius=10000&key=YOUR_KEY_HERE").json()




    #responds with json
    return JsonResponse(data, safe=False)
