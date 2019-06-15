from django.db import models
from django.contrib.auth.models import User as u

# Create your models here.


class Preference(models.Model):
    price = models.PositiveIntegerField(default=0)
    latitude = models.DecimalField(default=50.0, max_digits=11, decimal_places=8)
    longitude = models.DecimalField(default=0.0, max_digits=11, decimal_places=8)
    beds = models.PositiveIntegerField(default=1)
    baths = models.PositiveIntegerField(default=0)
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


class Profile(models.Model):
    user = models.OneToOneField(u, on_delete=models.CASCADE)
    prefer = models.ForeignKey(Preference, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.user.username
