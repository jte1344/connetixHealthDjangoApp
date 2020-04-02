from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import UserForm
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


def index(request):
    with open('siteData.JSON') as f:
      site = json.load(f)

    if request.method == 'POST':
        form = UserForm(request.POST)

        if form.is_valid():

            #gets user defined variables
            location = request.POST["location"]
            medication = request.POST["medication"]

            data = RxScrape(location, medication)

            data = {'location': location, 'medication': medication}

            return render(request, 'index/index.html', {'data': data, 'site': site})

    else:

        form = UserForm()
        return render(request, 'index/index.html', {'form': form, 'site': site})

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

    sleep(10)

    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "fw-btn-orange fw-gtm-getcard fw-ptr-cardmodalbutton"))
    )

    elem = driver.find_element_by_xpath("//*")
    source_code = elem.get_attribute("outerHTML")

    with open('test.html', 'a') as f:
        f.write(source_code)

    driver.quit()




    return data
