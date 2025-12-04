from django.db import models
from cloudinary.models import CloudinaryField

class Event(models.Model):
    name = models.CharField(max_length=250)
    image = CloudinaryField('image')  # FIXED

    def __str__(self):
        return self.name


class Group(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
    image = CloudinaryField('image')  # FIXED
    is_second = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Leadership(models.Model):
    name = models.CharField(max_length=250)
    bio = models.TextField()
    image = CloudinaryField('image')  # FIXED
    role = models.CharField(max_length=250)

    def __str__(self):
        return self.name
