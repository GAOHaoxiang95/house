"""house URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import staticfiles
from django.contrib import admin
from django.urls import path,re_path
from pricesite.views import homepage, properties, result, enroll, login, logout, feedback, recommendation, maps, profile, HouseAllViewSet,HouseViewSet
from django.conf.urls import include, url
from pricesite .urls import router


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homepage),
    path('property/', properties),
    path('result/', result),
    path('register/', enroll),
    path('property/maps/', maps),
    path('recommendation/maps/', maps),
    path('Login/', login),
    path('Logout/', logout),
    path('feedback/', feedback),
    path('profile/', profile),
    path('recommendation/', recommendation),
    path('accounts/', include('registration.backends.default.urls')),
    #url(r'^api-auth/', include('rest_framework.urls')),
    path('api/', include(router.urls)),
    path('properties/', HouseAllViewSet.as_view()),
    path('properties/<str:name>/',HouseViewSet.as_view())
    #path('api/properties/<str:name>', snippet_list)
]
urlpatterns += staticfiles_urlpatterns()