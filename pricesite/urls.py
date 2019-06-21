from rest_framework.routers import DefaultRouter
from . import views
from django.conf.urls import include,url
router = DefaultRouter()

router.register(r'prefer', views.PreferenceViewSet)

