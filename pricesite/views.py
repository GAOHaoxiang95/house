from django.shortcuts import render
from django.http import HttpResponse, Http404
from pricesite import models, parsePostcode
from sklearn.externals import joblib
import numpy as np
# Create your views here.


def homepage(request):
    pt = ['Detached House', 'Semi-detached House', 'Terraced House', 'Townhouse', 'Bungalow', 'Studio', 'Flat', 'Maisonette']
    fs = ['Unfurnished', 'Part furnished', 'Furnished']
    num_option = [0, 1 ,2, 3, 4, 5, 6, 7, 8, 9]
    return render(request, 'main.html', locals())


def property(request):
    return render(request, 'property.html', locals())


def result(request):
    try:
        num_beds = request.GET['num_beds']
        num_baths = request.GET['num_baths']
        postcode = request.GET['postcode']
        property_type = float(request.GET['pt']) - 1
        furniture_state = float(request.GET['fs']) - 1
        latitude, longitude = parsePostcode.parse_postcode(postcode)
        model = joblib.load("train_model.mt")
        result = model.predict([[latitude, longitude, num_beds, num_baths, property_type, furniture_state]])
        # change later, property type is int
        price = '£' + str(int(np.exp(result)[0])) + ' pcm'
    except:

        num_beds = 0
        num_baths = 0
        property_type = 0
        furniture_state = 0
        latitude = 'Unknown'
        longitude = 'Unknown'
        price = 'Unknown'

    return render(request, 'result.html', locals())
