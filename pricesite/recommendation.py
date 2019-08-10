import sklearn
import numpy as np
from django.contrib.auth.models import User
#from pricesite import models
from . import models
import math
import heapq


def similarity(x: list, y: list):
    a = x.dot(y)
    b = math.sqrt(sum(x ** 2)) * math.sqrt(sum(y ** 2))
    score = float(a) / float(b)
    return score


def map_float(iterable):#make all elements in the list to float
    return map(lambda x: float(x), iterable)


class Item:
    def __init__(self, features, score, url, beds, postcode):
        self.features = features
        self.score = score
        self.url = url
        self.beds = beds
        self.postcode = postcode
        self.flag = 0
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

        preference = models.Profile.objects.get(user=user).prefer
        y = ([preference.price, preference.latitude * 1000000, preference.longitude * 1000000,
             preference.beds*10, preference.baths*10, preference.furniture_state*10, preference.property_type*10])
        y = np.array(list(map_float(y)))
        print(y)
        other = models.PreferenceHouses.objects.exclude(prefer=user)
        duplicate = set()
        self.reco = list()
        for i in other:
            if (i.latitude, i.longitude) not in duplicate:# avoid computing repeatly
                duplicate.add((i.latitude, i.longitude))
                allpro = models.PreferenceHouses.objects.filter(latitude=i.latitude, longitude=i.longitude)
                flag = True
                score = 0
                RS = 0
                for j in allpro:
                    #print(j.prefer)
                    preference = models.Profile.objects.get(user=j.prefer).prefer
                    x = ([preference.price, preference.latitude * 1000000, preference.longitude * 1000000,
                         preference.beds*10, preference.baths*10, preference.furniture_state*10, preference.property_type*10])

                    x = np.array(list(map_float(x)))
                    cur = similarity(x, y)
                    RS = j.interest*cur + RS
                    score = score + cur
                    if j.prefer == user:
                        flag = False
                if flag is True:
                    final_score = RS / score
                    r = models.House.objects.filter(postcode=i.postcode)[0]
                    #print(r)
                    pro = np.array([r.price_actual, r.latitude, r.longitude, r.num_baths, r.furnished_state, r.property_type])
                    item = Item(list(pro), final_score, r.URL, r.num_beds, r.postcode)
                    #print(item.features)
                    #print(item.postcode)
                    #print(final_score)
                    self.reco.append(item)

    def get_recommendation(self):
        return self.reco


class ReccomendationContentBased:
    def __init__(self, user):
        furnished_state_dict = {'unfurnished': 0.0, 'furnished_or_unfurnished': 0.0, 'part_furnished': 1.0,
                                'furnished': 2.0}
        property_type_dict = {'detached': 0.0, 'semi_detached': 0.0, 'terraced': 0.0, 'end_terrace': 0.0,
                              'town_house': 0.0, 'bungalow': 1.0, 'detached_bungalow': 1.0,
                              'semi_detached_bungalow': 1.0,
                              'studio': 2.0, 'flat': 3.0, 'maisonette': 3.0}
        preference = models.Profile.objects.get(user=user).prefer
        x = [preference.price, preference.latitude*1000000, preference.longitude*1000000, preference.baths*10, preference.furniture_state*10, preference.property_type*10]
        x = np.array(list(map_float(x)))
        self.settings = x

        houses = models.House.objects.all().order_by('-id')[0:3000]
        self.items = list()
        for i in houses:#论文可以吹 这么处理数据！！！！！！！！！！！！！！！！！！！！！
            if i.furnished_state == "":
                fs = 0.0
            else:
                fs = furnished_state_dict[i.furnished_state]
            if i.property_type=="" or i.property_type not in property_type_dict:
                pt = 2.0
            else:
                pt = property_type_dict[i.property_type]
            y = np.array([i.price_actual, i.latitude*1000000, i.longitude*1000000, i.num_baths*10, fs*10, pt*10])
            score = similarity(x, y)
            #cosine similarity
            y[1] = y[1]/1000000
            y[2] = y[2]/1000000
            y[3] = y[3]/10
            y[4] = y[4]/10
            y[5] = y[5]/10
            if i.num_beds >= preference.beds:
                item = Item(list(y), score, i.URL, i.num_beds, i.postcode)
                self.items.append(item)

    def get_recommended_properties(self):
        heap = MinHeap(6, self.items)
        recommendations = heap.best_k()
        return recommendations

