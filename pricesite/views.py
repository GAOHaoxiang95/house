from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from pricesite import models, parsePostcode, forms
from pricesite.recommendation import Recommendation, ReccomendationContentBased
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


@login_required(login_url='/Login/')
def properties(request):
    if request.user.is_authenticated:
        status = 'Logout'
        name = request.user.username
    else:
        status = 'Login'
        name = None

    all_properties = House.objects.all().order_by('-id')
    p = Paginator(all_properties, 10)
    page_num = request.GET.get('p', 1)
    loaded = p.page(page_num)

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
        result = models.PreferenceHouses.objects.create(postcode=postcode, beds=num_beds, baths=num_baths, latitude=latitude,
                                                        longitude=longitude,furniture_state=fs, property_type=pt, interest=interest, price=price, prefer=u)
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

    ptd = {0:'Detached House', 1:'Semi-detached House', 2:'Terraced House', 3:'Townhouse', 4:'Bungalow', 5:'Studio', 6:'Flat', 7:'Maisonette'}
    fsd = {0:'unfurnished', 1:'part_furnished', 2:'furnished'}

    try:
        num_beds = float(request.GET['num_beds'])
        num_baths = float(request.GET['num_baths'])
        num_recepts = float(request.GET['num_recepts'])
        postcode = request.GET['postcode']
        if postcode == "":
            latitude = float(request.GET['latitude'])
            longitude = float(request.GET['longitude'])
        else:
            latitude, longitude = parsePostcode.parse_postcode(postcode)

        property_type = float(request.GET['pt'])
        furniture_state = float(request.GET['fs'])
        model = joblib.load("train_model.mt")

        result = model.predict([[latitude, longitude, num_beds, num_baths, num_recepts, property_type, furniture_state]])

        # change later, property type is int
        price = '£' + str(int(np.exp(result)[0])) + ' pcm'
        property_type = ptd[int(property_type)]
        #furniture_state = fsd[int(furniture_state)]
    except:
        num_beds = 0
        num_baths = 0
        property_type = 'Unknown'
        furniture_state = 'Unknown'
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
                p = models.Preference.objects.create()
                p.save()
                profile = models.Profile.objects.create(user=user, prefer=p)
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


def feedback(request):
    if request.user.is_authenticated:
        status = 'Logout'
        name = request.user.username
    else:
        status = 'Login'
    return redirect('https://docs.google.com/forms/d/1omEnqOOMWmJXIlR0DtMOSqZjFXWBqaz73oIiO8wjGK0/viewform?edit_requested=true')


from rest_framework import viewsets
from .models import Preference, PreferenceHouses, House
from .serializers import PreferenceSerializer, HouseSerializer
from rest_framework_mongoengine.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response


class PreferenceViewSet(viewsets.ModelViewSet):
    queryset = Preference.objects.all()
    serializer_class = PreferenceSerializer


from rest_framework.decorators import api_view
#from rest_framework.authentication import SessionAuthentication, BasicAuthentication


class HouseAllViewSet(APIView):
    #authentication_classes = [SessionAuthentication]
    def get(self, request, format=None):
        if request.user.is_authenticated:
            snippets = PreferenceHouses.objects.all()
            serializer = HouseSerializer(snippets, many=True)
            return Response(serializer.data)
        else:
            return Http404


from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated


class CsrfExemptSessionAuthentication(SessionAuthentication): #SHUT DOWN CSRF VERIFICATION

    def enforce_csrf(self, request):
        return


class HouseViewSet(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (BasicAuthentication, CsrfExemptSessionAuthentication)

    def get(self, request, name, format=None):
        if request.user.is_authenticated:
            u = User.objects.get(username=name)
            item = PreferenceHouses.objects.filter(prefer=u)
            serializer = HouseSerializer(item, many=True)
            return Response(serializer.data)
        else:
            return Http404

    def delete(self, request, name, format=None):
            try:
                #name = request.GET['name']
                postcode = request.GET['postcode']
                u = request.user
                print(u)
                PreferenceHouses.objects.filter(prefer=u, postcode=postcode).delete()
                item = PreferenceHouses.objects.filter(prefer=u)
                serializer = HouseSerializer(item, many=True)
                return Response(serializer.data)
            except:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@cache_page(60 * 15)
@login_required(login_url='/Login/')
def recommendation(request):
    if request.user.is_authenticated:
        status = 'Logout'
        name = request.user.username
    else:
        status = 'Login'

    furnished_state_dict = {'0.0':'unfurnished', '1.0':'part_furnished', '2.0':'furnished'}
    property_type_dict = {'0.0': 'house', '1.0': 'bungalow', '2.0': 'studio', '3.0': 'flat'}
    u = User.objects.get(username=name)
    a = ReccomendationContentBased(u)#recommendation Engine
    properties = a.get_recommended_properties()
    ctr = 0
    for item in properties:
        check = models.Hot.objects.filter(postcode=item.postcode, name=name)
        print(check)
        print('tttttttttttttttttt')
        if not check.exists():
            item.flag = 1
            result = models.Hot.objects.create(postcode=item.postcode, name=name)
            result.save()
        (properties[ctr].features)[4] = furnished_state_dict[str((item.features)[4])]
        (properties[ctr].features)[5] = property_type_dict[str((item.features)[5])]
        ctr += 1
    user = User.objects.get(username=name)
    a = Recommendation(user)
    i = a.get_recommendation()
    i = sorted(i)
    try:
        cof = i[-1]
        cof2 = i[-2]
        check = models.Hot.objects.filter(postcode=cof.postcode, name=name)
        if not check.exists():
            cof.flag = 1
            result = models.Hot.objects.create(postcode=cof.postcode, name=name)
            result.save()
        check = models.Hot.objects.filter(postcode=cof2.postcode, name=name)
        if not check.exists():
            cof2.flag = 1
            result = models.Hot.objects.create(postcode=cof2.postcode, name=name)
            result.save()
    except:
        pass
    return render(request, 'recommendation.html', locals())


def maps(request):
    if request.user.is_authenticated:
        status = 'Logout'
        name = request.user.username
    else:
        status = 'Login'
    try:
        postcode = request.GET.get('postcode')
        latitude, longitude = parsePostcode.parse_postcode(postcode)
    except:
        pass
    try:
        latitude = request.GET.get('latitude')
        longitude = request.GET.get('longitude')
    except:
        pass
    return render(request, 'maps.html', locals())


@login_required(login_url='/Login/')
def profile(request):
    if request.user.is_authenticated:
        status = 'Logout'
        name = request.user.username
    else:
        status = 'Login'
    try:
        name2 = request.GET['name']
        if name2 != name: #safety check
            return Http404
        else:
            name2 = name
        postcode = request.GET['postcode']
        u = User.objects.get(username=name)
        PreferenceHouses.objects.filter(prefer=u, postcode=postcode).delete()
        messages.add_message(request, messages.SUCCESS, 'Delete successfully!')
    except:
        pass

    try:
        user = User.objects.get(username=name)
        userinfo = models.Profile.objects.get(user=user)
        price=userinfo.prefer.price
        beds=userinfo.prefer.beds
        baths=userinfo.prefer.baths
        pt = int(userinfo.prefer.property_type)
        pt_list=['House', 'Bungalow', 'Studio', 'Flat']
        pt_string = pt_list[pt]
        fs = int(userinfo.prefer.furniture_state)
        fs_list=['Unfurnished', 'Part furnished', 'Furnished']
        fs_string=fs_list[fs]
        latitude= userinfo.prefer.latitude
        longitude=userinfo.prefer.longitude
    except:
        pass
    try:
        beds = request.GET['num_beds']
        baths = request.GET['num_baths']
        postcode = request.GET['postcode']
        latitude=request.GET['latitude']
        longitude=request.GET['longitude']
        fs = int(request.GET['fs'])
        pt = int(request.GET['pt'])
        pt_string = pt_list[pt]
        fs_string=fs_list[fs]
        price = request.GET['price']
        #latitude, longitude = parsePostcode.parse_postcode(postcode)
        userinfo.prefer.price=price
        userinfo.prefer.beds=beds
        userinfo.prefer.baths=baths
        userinfo.prefer.latitude=latitude
        userinfo.prefer.longitude=longitude
        userinfo.prefer.furniture_state=fs
        userinfo.prefer.property_type=pt
        userinfo.prefer.save()
        messages.add_message(request, messages.SUCCESS, 'Save successfully!')
    except:
            #messages.add_message(request, messages.WARNING, 'Save failed!')
            pass

    return render(request, 'profile.html', locals())
