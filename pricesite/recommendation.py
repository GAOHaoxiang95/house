import sklearn
import numpy as np
from django.contrib.auth.models import User
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
        furnished_state_dict = {'unfurnished': 0.0, 'furnished_or_unfurnished': 0.0, 'part_furnished': 1.0,
                                'furnished': 2.0}
        property_type_dict = {'detached': 0.0, 'semi_detached': 0.0, 'terraced': 0.0, 'end_terrace': 0.0,
                              'town_house': 0.0, 'bungalow': 1.0, 'detached_bungalow': 1.0,
                              'semi_detached_bungalow': 1.0,
                              'studio': 2.0, 'flat': 3.0, 'maisonette': 3.0}
        #alluser = User.objects.all()
        allratedhouses = models.PreferenceHouses.objects.all()
        for i in allratedhouses:
            print(i)

        preference = models.Profile.objects.get(user=user).prefer
        x = [preference.price, preference.latitude*1000000, preference.longitude*1000000, preference.baths, preference.furniture_state, preference.property_type]
        x = np.array(list(map_float(x)))
        self.settings = x


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
        x = [preference.price, preference.latitude*1000000, preference.longitude*1000000, preference.baths, preference.furniture_state, preference.property_type]
        x = np.array(list(map_float(x)))
        self.settings = x

        houses = models.House.objects.all()[0:3000]
        self.items = list()
        for i in houses:#论文可以吹 这么处理数据！！！！！！！！！！！！！！！！！！！！！
            if i.furnished_state == "":
                fs = 0.0
            else:
                fs = furnished_state_dict[i.furnished_state]
            if i.property_type=="" or i.property_type not in property_type_dict:
                pt = 1.5
            else:
                pt = property_type_dict[i.property_type]
            y = np.array([i.price_actual, i.latitude*1000000, i.longitude*1000000, i.num_baths, fs, pt])

            a = x.dot(y)
            b = math.sqrt(sum(x ** 2)) * math.sqrt(sum(y ** 2))
            score = a/b#cosine similarity
            y[1] = y[1]/1000000
            y[2] = y[2]/1000000
            if i.num_beds == preference.beds:
                item = Item(list(y), score, i.URL, i.num_beds)
                self.items.append(item)

    def get_recommended_properties(self):
        heap = MinHeap(10, self.items)
        recommendations = heap.best_k()
        return recommendations

