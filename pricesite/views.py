from django.shortcuts import render
from django.http import HttpResponse, Http404

# Create your views here.


def homepage(request):
    return render(request, 'main.html', locals())
