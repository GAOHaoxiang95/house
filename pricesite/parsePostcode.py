import requests
import json

API = 'http://api.postcodes.io/postcodes/'


def parse_postcode(postcode):
    text = requests.get(API + postcode).text
    r = json.loads(text)
    longitude = r['result']['longitude']
    latitude = r['result']['latitude']
    return latitude, longitude


if __name__=='__main__':
    la, long = parse_postcode('sw11')
    print(la, long)
