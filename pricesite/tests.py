from django.test import TestCase

import requests

r = requests.get('http://127.0.0.1:8000/api/prefer/')
print(r.text)
# Create your tests here.

from collections import deque


class Stack:
    def __init__(self):
        self.items = deque()
    def push(self, val):
        return self.items.append(val)
    def pop(self):
        return self.items.pop()
    def empty(self):
        return len(self.items)==0
