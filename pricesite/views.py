from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from pricesite import models, parsePostcode, forms
from sklearn.externals import joblib
import numpy as np
from django.views.decorators.cache import cache_page
from django.contrib import messages
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib import auth
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
        property_type = float(request.GET['pt'])
        furniture_state = float(request.GET['fs'])
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
            name = request.POST['name']
            password = request.POST['password']
            email = request.POST['email']
            user = User.objects.create_user(name, email, password)
            user.save()

            messages.add_message(request, messages.SUCCESS, 'Enroll successfully!')
            return redirect('/')
            #print('no')
        else:
            pass
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
            name = request.POST['name'].strip()
            password = request.POST['password']
            print(name)
            user = authenticate(username=name, password=password)
            print(user)
            if user is not None:
                if user.is_active:
                    auth.login(request, user)
                    messages.add_message(request, messages.SUCCESS, 'Login successfully!')
                    return redirect('/')
            else:
                message = "Please check your username and password."
            '''
            try:
                user = models.User.objects.get(email=email)
                if user.password == password:
                    request.session['email'] = email#login successfully
                    request.session['name'] = user.name

                    messages.add_message(request, messages.SUCCESS, 'Login successfully!')
                    return redirect('/')
                else:
                    message = "Please check your password."
            except:
                message = "Please check your email."
            '''
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
