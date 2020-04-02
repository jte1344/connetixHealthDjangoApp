from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import *
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from collections import OrderedDict
from datetime import datetime
from time import time
from lxml import html,etree
import json
import requests
import bs4
import requests,re
import os,sys

def RxScrape(medication, location):

    data = 0

    url = "https://familywize.org/drug-price-look-up-tool" #.format(medication, location)

    opts = Options()
    opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36")


    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    driver = webdriver.Chrome(chrome_options=opts, executable_path=os.path.join(BASE_DIR, 'chromedriver.exe'))


    ##driver=webdriver.Chrome()
    driver.get(url)
    #innerHTML = driver.execute_script("return document.body.innerHTML")
    ##print(driver.page_source)

    driver.find_element_by_name("DrugName").send_keys("lipitor")
    driver.find_element_by_name("ZipCode").send_keys("80907")

    element = driver.find_element_by_css_selector("button.fw-btn-orange").click()

    sleep(5)

    element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "fw-btn-orange fw-gtm-getcard fw-ptr-cardmodalbutton"))
    )

    elem = driver.find_element_by_xpath("//*")
    source_code = elem.get_attribute("outerHTML")

    with open('test.html', 'a') as f:
        f.write(source_code)

        driver.quit()

        return data

def index(request):
    with open('siteData.JSON') as f:
      site = json.load(f)

    if request.method == 'POST':
        form = LocalDrug(request.POST)

        if form.is_valid():

            #gets user defined variables
            location = request.POST["location"]
            medication = request.POST["medication"]

            #localPrice = RxScrape(location, medication)

            data = {'location': location, 'medication': medication}

            return render(request, 'index/index.html', {'data': data, 'site': site})

    else:

        form = LocalDrug()
        return render(request, 'index/index.html', {'form': form, 'site': site})


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
