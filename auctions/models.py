from django.contrib.auth.models import AbstractUser
from django.db import models

CATEGORY_CHOICES = (
    ('Fashion', 'Fashion'),
    ('BooksToys', "Books & Toys"),
    ('Homegoods', 'Home Goods'),
    ('Electronics', 'Electronics'))

class User(AbstractUser):
    ### TO DO - need to add a data field linking to the watchlist
    pass

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=500)
    start_bid = models.IntegerField(default=0)
    image = models.URLField(blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    ### TO DO - need to add a field for the highest bid should reference the bid id
    def __str__(self):
        return f"{self.id}: {self.title} - {self.description} for {self.start_bid} in {self.category} has image link {self.image}"
    

### TO DO
class Bid(models.Model):
    ### TO DO - needs to have a field indicating what Listing it goes to 
    ### Should also list the user
    pass

### TO DO
class Comments(models.Model):
    pass

class WatchList(models.Model):
    # Tie the user to the WatchList, and the Watchlist to the user
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    # Tie the listing to the WatchList and the Watchlist to the Listing 
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='list_item')
    
    def __str__(self):
        return f"User: {self.user} & Listing: {self.listing}"   