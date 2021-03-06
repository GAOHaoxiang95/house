from django.db import models
from django.contrib.auth.models import User as u

# Create your models here.
import mongoengine


class Preference(models.Model):
    price = models.PositiveIntegerField(default=1500)
    latitude = models.DecimalField(default=51.49869386764022, max_digits=11, decimal_places=8)
    longitude = models.DecimalField(default=-0.17911445396727732, max_digits=11, decimal_places=8)
    beds = models.PositiveIntegerField(default=1)
    baths = models.PositiveIntegerField(default=1)
    school = models.DecimalField(default=0.0, max_digits=11, decimal_places=8)
    transport = models.DecimalField(default=0.0, max_digits=11, decimal_places=8)
    property_type = models.PositiveIntegerField(default=0)
    furniture_state = models.PositiveIntegerField(default=0)


class User(models.Model):
    name = models.CharField(max_length=20, default="Tourist")
    password = models.CharField(max_length=20, null=False)
    email = models.EmailField(primary_key=True)
    prefer = models.ForeignKey(Preference, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.name


class Hot(models.Model):
    postcode = models.CharField(max_length=20, default="Tourist")
    name = models.CharField(max_length=20, default="Tourist")
    def __str__(self):
        return self.postcode


class PreferenceHouses(models.Model):
    price = models.PositiveIntegerField(default=0)
    latitude = models.DecimalField(default=50.0, max_digits=11, decimal_places=8)
    longitude = models.DecimalField(default=0.0, max_digits=11, decimal_places=8)
    beds = models.PositiveIntegerField(default=1)
    baths = models.PositiveIntegerField(default=0)
    school = models.DecimalField(default=0.0, max_digits=11, decimal_places=8)
    transport = models.DecimalField(default=0.0, max_digits=11, decimal_places=8)
    property_type = models.CharField(max_length=40, default="")
    furniture_state = models.CharField(max_length=40, default="")
    postcode = models.CharField(max_length=40, default="")
    interest = models.PositiveIntegerField(default=0)
    prefer = models.ForeignKey(u, on_delete=models.CASCADE)


class Profile(models.Model):
    user = models.OneToOneField(u, on_delete=models.CASCADE)
    prefer = models.ForeignKey(Preference, on_delete=models.CASCADE, default=6)

    def __str__(self):
        return self.user.username


mongoengine.connect('Houses',host = '127.0.0.1',port = 27017)
class House(mongoengine.Document):
    postcode = mongoengine.StringField()
    price_actual = mongoengine.IntField(default=0)
    meta = {'collection':'Regular'}
    is_retirement_home = mongoengine.StringField()
    num_recepts = mongoengine.IntField(default=0)
    property_type = mongoengine.StringField()
    furnished_state = mongoengine.StringField()
    num_beds = mongoengine.IntField(default=0)
    num_baths = mongoengine.IntField(default=0)

    transport = mongoengine.StringField()
    URL = mongoengine.StringField()
    Water = mongoengine.StringField()
    Energy = mongoengine.StringField()
    Council_tax=mongoengine.StringField()
    room_to_rent=mongoengine.IntField()
    Rent = mongoengine.StringField()
    school = mongoengine.StringField()
    Home_insurance = mongoengine.StringField()
    longitude = mongoengine.FloatField()
    latitude = mongoengine.FloatField()


