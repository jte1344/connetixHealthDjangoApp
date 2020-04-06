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

def RxScrape(medication):

    url = "https://www.drugs.com/price-guide/{0}".format(medication)

    # Make a GET request to fetch the raw HTML content
    html_content = requests.get(url).text

    # Parse the html content
    soup = BeautifulSoup(html_content, "lxml")

    drugName = []
    table = soup.find_all("table", attrs={"class": "data-list"})
    tableName = soup.find_all("div", attrs={"class": "dosage-block"})
    for i in range(0, len(tableName)):
        drugName.append(tableName[i].text)

    quantity = []
    quantityData = table[0].find_all("td", attrs={"class": ""})
    for j in range(0, len(quantityData)):
        quantity.append(quantityData[j].text)

    unitPrice = []
    totalPrice = []
    priceData = table[0].find_all("td", attrs={"class": "text-right"})

    for k in range(0, len(quantityData)):
        unitPrice.append(priceData[0].text)
        priceData.pop(0)
        totalPrice.append(priceData[0].text)
        priceData.pop(0)

    data = []
    for i in range(0, len(drugName)):
        data.append({"title" : drugName[i], "data" : []})
        for j in range(0, len(quantity)):
                data[i]["data"].append({"quantity" : quantity[j], "unitPrice" : unitPrice[j], "totalPrice" : totalPrice[j]})


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


    #this if statement is for after the user has entered data
    if request.method == 'POST':
        form = InteractionForm(request.POST)

        #checks if the user input anything
        if form.is_valid():

            #gets user defined variables from the front end
            medications = request.POST["medications"]
            print(medications)

            '''
            We will need to split medications into seperate value bc it will be returned
            as a string. most likely will need to prompt user to input meds seperated by commas
            couldnt find django support for user inputting data into an array, or we will have
            to pre define the number of medications a user can enter
            '''



            #NIH API will go here using data gathered in the medications variable above





            #data to output after the user has input medications
            #data can be changed to be an array or a dictionary(preferably for JSON)
            data = 0

            '''
            Renders view for the user and sends in variables: data and site to be
            used in html using double curly bracket notation

            Example: <h1>{{data}}</h1>

            This would display everything in the data variable in html so output
            to the user curerntly would be 0 (this will only occur after the form
            has been submitted by the user and is on line 8 in index/templates/index/interactions.html)
            We can worry about the html later

            Check the README.md in the root directory for info on how to get the server up locally

            To view this code open localhost:8000/interactions in a web browser after running 'python manage.py runserver'

            Once you enter something into the form and submit the 0 will appear under the navbar
            '''

            return render(request, 'index/interactions.html', {'data': data, 'site': site})


        #if the form is invalid
        else:
            return render(request, 'index/interactions.html', {'site': site})#always send in site like this


    #this is for before the user has input data
    else:

        #declares forms found in index/forms.py
        form = InteractionForm()

        #sends in form and site data
        return render(request, 'index/interactions.html', {'form': form, 'site': site})


def local(request, medication):

    data = RxScrape(medication)

    print(medication)

    return JsonResponse(data, safe=False)
