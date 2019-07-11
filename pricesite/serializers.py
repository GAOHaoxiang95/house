from rest_framework import serializers
from .models import Preference, PreferenceHouses, House


class PreferenceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Preference
        fields=('beds', 'baths')


class HouseSerializer(serializers.ModelSerializer):

    class Meta:
        model = House
        fields=('num_beds', 'num_baths')


