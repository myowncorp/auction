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
    def __str__(self):
        return f"{self.id}: {self.title} - {self.description} for {self.start_bid} in {self.category} has image link {self.image}"
   
    def get_highest_bid(self):
        # This retrieves the highest bid amount related to the listing
        highest_bid = self.bid.order_by('-amount').first()
        return highest_bid.amount if highest_bid else None

class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bid')
    # if it's saved here, it has to be the highest bid.
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bid')
    amount = models.IntegerField()
    def __str__(self):
        return f"{self.bidder}: bid {self.amount} on {self.listing}"

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