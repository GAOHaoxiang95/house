from django.db import models

# Create your models here.


class User(models.Model):
    name = models.CharField(max_length=20, null=False)
    password = models.CharField(max_length=20, null=False)
    email = models.EmailField()
    id = models
    def __str__(self):
        return self.name
