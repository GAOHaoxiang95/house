from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from pricesite import models, parsePostcode, forms
from pricesite.recommendation import Recommendation
from sklearn.externals import joblib
import numpy as np
from django.views.decorators.cache import cache_page
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib import auth
from pricesite.models import House
from django.core.paginator import Paginator
# Create your views here.


def homepage(request):
    if request.user.is_authenticated:
        status = 'Logout'
        name = request.user.username
    else:
        status = 'Login'
    return render(request, 'main.html', locals())


def properties(request):
    if request.user.is_authenticated:
        status = 'Logout'
        name = request.user.username
    else:
        status = 'Login'
        name = None

    all_properties = House.objects
    p = Paginator(all_properties, 9)
    page_num = request.GET.get('p', 1)
    loaded = p.page(page_num)
    

    u = User.objects.get(username=name)
    a = Recommendation(u)#recommendation Engine

    try:
        num_beds = request.GET['beds']
        num_baths = request.GET['baths']
        postcode = request.GET['postcode']
        fs = request.GET['fs']
        pt = request.GET['pt']
        price = request.GET['price']
        interest = request.GET['interest']
        u = User.objects.get(username=name)
        latitude, longitude = parsePostcode.parse_postcode(postcode)
        result = models.PreferenceHouses.objects.create(beds=num_beds, baths=num_baths, latitude=latitude, longitude=longitude, interest=interest, price=price, prefer=u)
        result.save()
        messages.add_message(request, messages.SUCCESS, 'Save successfully!')
    except:
            #messages.add_message(request, messages.WARNING, 'Save failed!')
            pass
    return render(request, 'property.html', locals())


@cache_page(60 * 15)
def result(request):
    if request.user.is_authenticated:
        status = 'Logout'
        name = request.user.username
    else:
        status = 'Login'
    try:
        num_beds = request.GET['num_beds']
        num_baths = request.GET['num_baths']
        postcode = request.GET['postcode']
        if postcode == "":
            latitude = float(request.GET['latitude'])
            longitude = float(request.GET['longitude'])
        else:
            latitude, longitude = parsePostcode.parse_postcode(postcode)

        property_type = float(request.GET['pt'])
        furniture_state = float(request.GET['fs'])

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


def enroll(request):
    if request.user.is_authenticated:
        status = 'Logout'
        name = request.user.username
    else:
        status = 'Login'
    if request.method == 'POST':
        post_form = forms.LoginForm(request.POST)
        #print(post_form.cleaned_data['email'])
        if post_form.is_valid():
            uname = request.POST['name']
            password = request.POST['password']
            email = request.POST['email']
            try:
                user = User.objects.create_user(uname, email, password)
                user.save()
                profile = models.Profile.objects.create(user=user)
                profile.save()
                messages.add_message(request, messages.SUCCESS, 'Enroll successfully!')
                return redirect('/')
            except:
                messages.add_message(request, messages.WARNING, 'This account already exists!')
        else:
            messages.add_message(request, messages.WARNING, 'Enroll failed!')
    else:
        post_form = forms.LoginForm()

    return render(request, 'sign_up.html', locals())


def logout(request):
    if request.user.is_authenticated:
        status = 'Logout'
        name = request.user.username
    else:
        status = 'Login'
    auth.logout(request)
    messages.add_message(request, messages.SUCCESS, 'Logout successfully!')
    return redirect('/')


def login(request):
    if request.user.is_authenticated:
        status = 'Logout'
        name = request.user.username
    else:
        status = 'Login'
    message = ""
    if request.method == 'POST':
        form = forms.AuthenticationForm(request.POST)
        if form.is_valid():
            username = request.POST['name'].strip()
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    auth.login(request, user)
                    messages.add_message(request, messages.SUCCESS, 'Login successfully!')
                    return redirect('/')
            else:
                message = "Please check your username and password."
    else:
        form = forms.AuthenticationForm()
    return render(request, 'login.html', locals())


@login_required(login_url='/Login/')
def feedback(request):
    if request.user.is_authenticated:
        status = 'Logout'
        name = request.user.username
    else:
        status = 'Login'
    return render(request, 'feedback.html', locals())


def map_position(request):
    return render(request, 'test2.html', locals())


from rest_framework import viewsets
from .models import Preference
from .serializers import PreferenceSerializer


class PreferenceViewSet(viewsets.ModelViewSet):
    queryset = Preference.objects.all().order_by('beds')
    serializer_class = PreferenceSerializer


@login_required(login_url='/Login/')
def recommendation(request):
    if request.user.is_authenticated:
        status = 'Logout'
        name = request.user.username
    else:
        status = 'Login'
    return render(request, 'recommendation.html', locals())


def maps(request):
    if request.user.is_authenticated:
        status = 'Logout'
        name = request.user.username
    else:
        status = 'Login'
    postcode = request.GET.get('postcode')
    latitude, longitude = parsePostcode.parse_postcode(postcode)
    return render(request, 'maps.html', locals())
