from __future__ import unicode_literals

from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length = 255)
    username = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True, null = True, blank = True)

class Trip(models.Model):
    destination = models.CharField(max_length = 255, null = True, blank = True)
    description = models.TextField(null = True, blank = True)
    date_from = models.DateField(null = True, blank= True)
    date_to = models.DateField(null = True, blank = True)
    created_at = models.DateTimeField(auto_now_add = True, null = True, blank = True)
    user = models.ManyToManyField(User)

class UserTrip(models.Model):
    the_user = models.ForeignKey(User, related_name = 'trip_creator')
    the_trip = models.ForeignKey(Trip, related_name = 'created_trip')
    created_at = models.DateTimeField(auto_now_add = True)
