
from rest_framework_mongoengine import serializers as s
from .models import Preference, PreferenceHouses, House
from rest_framework import serializers


class PreferenceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Preference
        fields=('beds', 'baths')


class HouseSerializer(s.DocumentSerializer):

    class Meta:
        model = House
        fields=('num_beds', 'num_baths')


