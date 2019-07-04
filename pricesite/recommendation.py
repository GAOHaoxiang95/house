import sklearn
#from pricesite import models
from . import models


class Recommendation(object):
    def __init__(self, user):
        self.user = user
        preference = models.PreferenceHouses.objects.filter(prefer=user)
        print(preference[0].price)
    def computePreference(self):
        pass


