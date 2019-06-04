from django.shortcuts import render
from django.http import HttpResponse, Http404
from pricesite import models, parsePostcode
from sklearn.externals import joblib
import numpy as np
from django.views.decorators.cache import cache_page
# Create your views here.


def homepage(request):
    return render(request, 'main.html', locals())


def properties(request):
    return render(request, 'property.html', locals())


@cache_page(60 * 15)
def result(request):
    try:
        num_beds = request.GET['num_beds']
        num_baths = request.GET['num_baths']
        postcode = request.GET['postcode']
        property_type = float(request.GET['pt'])
        furniture_state = float(request.GET['fs'])
        latitude, longitude = parsePostcode.parse_postcode(postcode)
        model = joblib.load("train_model.mt")
        result = model.predict([[latitude, longitude, num_beds, num_baths, property_type, furniture_state]])
        # change later, property type is int
        price = '£' + str(int(np.exp(result)[0])) + ' pcm'
        j = 0
        for i in range(1000000000):
            j = j + 1
    except:
        num_beds = 0
        num_baths = 0
        property_type = 0
        furniture_state = 0
        latitude = 'Unknown'
        longitude = 'Unknown'
        price = 'Unknown'

    return render(request, 'result.html', locals())
