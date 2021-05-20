from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class CreateListing(models.Model):
    owner = models.CharField(max_length=64)
    title = models.CharField(max_length=64)
    description = models.TextField()
    initialBid = models.IntegerField()
    category = models.CharField(max_length=64)
    link = models.CharField(max_length=256, blank=True, null=True, default=None)
    time = models.CharField(max_length=64)

class WatchList(models.Model):
    user = models.CharField(max_length=64)
    listingId = models.IntegerField()

class Bids(models.Model):
    user = models.CharField(max_length=64)
    title = models.CharField(max_length=64)
    bid = models.IntegerField()
    listingId = models.IntegerField()
