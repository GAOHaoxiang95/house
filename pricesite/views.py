from django.shortcuts import render
from django.http import HttpResponse, Http404

# Create your views here.


def homepage(request):
    try:
        num_beds = request.GET['num_beds']
        num_baths = request.GET['num_baths']
        num_recepts = request.GET['num_recepts']
        postcode = request.GET['postcode']
    except:
        num_beds = 0
        num_baths = 0
        num_recepts = 0
        postcode = None

    price = 90 + int(num_beds) + int(num_baths) + int(num_recepts)
    return render(request, 'main.html', locals())
