from django.contrib.auth.models import AbstractUser
from django.db import models

CATEGORY_CHOICES = (
    ('Fashion', 'Fashion'),
    ('BooksToys', "Books & Toys"),
    ('Homegoods', 'Home Goods'),
    ('Electronics', 'Electronics'))

class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=500)
    start_bid = models.IntegerField(default=0)
    image = models.URLField(blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    
### TO DO
class Bid(models.Model):
    pass

### TO DO
class Comments(models.Model):
    pass