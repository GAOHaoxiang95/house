from django.db import models

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
    name = models.CharField(max_length=20, null=False)
    password = models.CharField(max_length=20, null=False)
    email = models.EmailField()
    prefer = models.ForeignKey(Preference, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
