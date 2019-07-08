from rest_framework import serializers
from .models import Preference, PreferenceHouses


class PreferenceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Preference
        fields=('beds', 'baths')


class HouseSerializer(serializers.ModelSerializer):

    class Meta:
        model = PreferenceHouses
        fields=('beds', 'baths')
