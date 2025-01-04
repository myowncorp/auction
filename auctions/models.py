from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(length=64)
    description = models.CharField(length=500)
    start_bid = models.IntegerField
    image = models.URLField(blank=True)
    category = models.CharField(length=50)
    
    
class Bid(models.Model):
    pass
class Comments(models.Model):
    pass