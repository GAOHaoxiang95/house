from django.test import TestCase
import requests
#test API
'''
r = requests.get('http://127.0.0.1:8000/api/prefer/')
print(r.text)
'''
# Create your tests here.

from collections import deque
import sklearn
import numpy as np
class Stack:
    def __init__(self):
        self.items = deque()
    def push(self, val):
        return self.items.append(val)
    def pop(self):
        return self.items.pop()
    def empty(self):
        return len(self.items)==0
import math
x = np.array([0.000001,0.00002,30])
y = np.array([10000,0.002,4000])
a = x.dot(y)

b= math.sqrt(sum(x**2))*math.sqrt(sum(y**2))
print(a/b)


class Item:
    def __init__(self, features, score):
        self.features = features
        self.score = score
    def __gt__(self, other):
        return self.score > other.score
    def __lt__(self, other):
        return self.score < other.score

import heapq
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

a = Item([1,2,3,4], 3)
b = Item([3,4,5,6], 9)
c = Item([1,2,1,1], 2)
d = Item([6,6,6,6], 5)
e = Item([3,3,3,3], 100)

test = MinHeap(2, [a,b,c,d,e])
t = test.best_k()
print(t[0].score, t[1].score)
