from django.test import TestCase

import requests

r = requests.get('http://127.0.0.1:8000/api/prefer/')
print(r.text)
# Create your tests here.
