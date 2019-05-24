from django.shortcuts import render
from django.http import HttpResponse, Http404
from pricesite import models, parsePostcode
# Create your views here.


def homepage(request):
    return render(request, 'main.html', locals())


def property(request):
    return render(request, 'property.html', locals())


def result(request):
    try:
        num_beds = request.GET['num_beds']
        num_baths = request.GET['num_baths']
        num_recepts = request.GET['num_recepts']
        postcode = request.GET['postcode']
        property_type = request.GET['pt']
        furniture_state = request.GET['fs']
        latitude, longitude = parsePostcode.parse_postcode('parse_postcode')

    except:
        num_beds = 0
        num_baths = 0
        num_recepts = 0
    #clf = joblib.load("train_model.mt")
    price = 90 + int(num_beds) + int(num_baths) + int(num_recepts)
    return render(request, 'result.html', locals())
