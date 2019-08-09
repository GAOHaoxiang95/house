from rest_framework.routers import DefaultRouter
from . import views
from django.conf.urls import include,url
router = DefaultRouter()

router.register(r'prefer', views.PreferenceViewSet)
#router.register(r'properties', views.HouseAllViewSet, base_name='all')
#router.register(r'properties/<str:name>/', views.HouseViewSet, base_name='some')
