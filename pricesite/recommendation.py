import sklearn
import numpy as np
#from pricesite import models
from . import models


class Recommendation(object):
    def __init__(self, user):
        self.user = user
        preference = models.PreferenceHouses.objects.filter(prefer=user)
        num_of_items = len(preference)
        num_of_features = 7
        self.featureVector = np.zeros((num_of_items, num_of_features))
        furnished_state_dict = {'unfurnished': 0.0, 'furnished_or_unfurnished': 1.0, 'part_furnished': 2.0,
                                'furnished': 3.0}
        property_type_dict = {'detached': 0.0, 'semi_detached': 1.0, 'terraced': 2.0, 'end_terrace': 2.0,
                              'town_house': 3.0, 'bungalow': 4.0, 'detached_bungalow': 4.0,
                              'semi_detached_bungalow': 4.0, 'studio': 5.0, 'flat': 6.0, 'maisonette': 7.0}
        for i in range(num_of_items):
            price = preference[i].price
            latitude = preference[i].latitude
            longitude = preference[i].longitude
            #print(type(price))
            pt = preference[i].property_type
            fs = preference[i].furniture_state
            if fs == "":
                furnished_state = 1.0
            else:
                furnished_state = furnished_state_dict[fs]
            if pt in property_type_dict:
                property_type = property_type_dict[pt]
            else:
                property_type = 8.0
            baths = preference[i].baths
            beds = preference[i].beds
            x = np.array([price, latitude, longitude, baths, beds, furnished_state, property_type])
            self.featureVector[i,:] = x

    def computePreference(self):
        pass


