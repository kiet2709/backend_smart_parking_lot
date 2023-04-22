from django.db import models
from django.contrib.postgres.fields import ArrayField


class MotoInfo(models.Model):

    licencePlate = models.CharField(max_length=20, name="licence_plate")
    cardNumber = models.CharField(max_length=10, name="card_number")
    objects = models.Manager()

    def __str__(self):
        return self.licencePlate


class Camera(models.Model):
    image_url = models.CharField(max_length=100)
    locate = models.CharField(max_length=30)
    objects = models.Manager()

    def __str__(self):
        return self.locate
    
class ObjectResponse(models.Model):
    
    licencePlate = models.CharField(max_length=100)
    image_url = models.CharField(max_length=30)
    locate = models.CharField(max_length=30)
    objects = models.Manager()
