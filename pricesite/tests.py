from django.test import TestCase

import requests

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