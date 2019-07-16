import sklearn
import numpy as np
import scipy
#from pricesite import models
from . import models
import math
import heapq
def map_float(iterable):#make all elements in the list to float
    return map(lambda x: float(x), iterable)


class Item:
    def __init__(self, features, score, url, beds):
        self.features = features
        self.score = score
        self.url = url
        self.beds = beds
    def __gt__(self, other):
        return self.score > other.score
    def __lt__(self, other):
        return self.score < other.score

class MinHeap:
    def __init__(self, k, items: Item):
        self.heap = list()
        self.k = k
        self.items = items
    def push(self, item):
        if len(self.heap) >= self.k:
            min_item = self.heap[0]
            if item > min_item:
                heapq.heapreplace(self.heap, item)
        else:
            heapq.heappush(self.heap, item)
    def best_k(self):
        for i in self.items:
            self.push(i)
        return self.heap


class Recommendation(object):
    def __init__(self, user):
        self.user = user
        preference = models.PreferenceHouses.objects.filter(prefer=user)
        num_of_items = len(preference)
        num_of_features = 7
        self.featureVector = np.zeros((num_of_items, num_of_features))
        furnished_state_dict = {'unfurnished': 0.0, 'furnished_or_unfurnished': 1.0, 'part_furnished': 2.0,
                                'furnished': 3.0}
        property_type_dict = {'detached': 0.0, 'semi_detached': 0.0, 'terraced': 0.0, 'end_terrace': 0.0,
                              'town_house': 0.0, 'bungalow': 1.0, 'detached_bungalow': 1.0,
                              'semi_detached_bungalow': 1.0, 'studio': 2.0, 'flat': 3.0, 'maisonette': 3.0}
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


class ReccomendationContentBased:
    def __init__(self, user):
        furnished_state_dict = {'unfurnished': 0.0, 'furnished_or_unfurnished': 0.0, 'part_furnished': 1.0,
                                'furnished': 2.0}
        property_type_dict = {'detached': 0.0, 'semi_detached': 0.0, 'terraced': 0.0, 'end_terrace': 0.0,
                              'town_house': 0.0, 'bungalow': 1.0, 'detached_bungalow': 1.0,
                              'semi_detached_bungalow': 1.0,
                              'studio': 2.0, 'flat': 3.0, 'maisonette': 3.0}
        preference = models.Profile.objects.get(user=user).prefer
        x = [preference.price, preference.latitude*100, preference.longitude*100, preference.baths, preference.furniture_state, preference.property_type]
        x = np.array(list(map_float(x)))
        self.settings = x

        houses = models.House.objects.all()[0:500]
        self.items = list()
        for i in houses:
            if i.furnished_state == "":
                fs = 1.0
            else:
                fs = furnished_state_dict[i.furnished_state]

            if i.property_type=="" or i.property_type not in property_type_dict:
                pt = 1.5
            else:
                pt = property_type_dict[i.property_type]
            y = np.array([i.price_actual, i.latitude*100, i.longitude*100, i.num_baths, fs, pt])
            #print(y)
            a = x.dot(y)
            b = math.sqrt(sum(x ** 2)) * math.sqrt(sum(y ** 2))
            score = a/b#cosine similarity
            y[1] = y[1]/100
            y[2] = y[2]/100
            
            if i.num_beds >= preference.beds:
                item = Item(y, score, i.URL, i.num_beds)
                self.items.append(item)


    def get_recommended_properties(self):
        heap = MinHeap(5, self.items)
        recommendations = heap.best_k()
        print("test", recommendations)
        print(recommendations[0].score)
        print(recommendations[0].features)
        return recommendations

