from django.db import models

# Create your models here.

class Event(models.Model):
    name = models.CharField(max_length=250)
    image = models.ImageField(upload_to='uploads/event/')

    def __str__(self):
        return self.name


class Group(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
    image = models.ImageField(upload_to='uploads/group')
    is_second = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
class Leadership(models.Model):
    name = models.CharField(max_length=250)
    bio = models.TextField()
    image = models.ImageField(upload_to='uploads/leadership/')
    role = models.CharField(max_length=250)

