from django.contrib.auth import authenticate, login, logout, admin
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Listing, WatchList
from .forms import ListingForm, BidForm


def index(request):
    return render(request, "auctions/index.html", 
                  {'listings': Listing.objects.all()})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def create_listing(request):

    if request.method == "POST":
        f = ListingForm(request.POST)
        print(f"{f}")
        if f.is_valid:
            f.save()
        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, 'auctions/createlisting.html', {
            'form': ListingForm()
        })
        
        
@login_required  
def listing(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    
    if request.method=='POST':
        
        # get the value of the action, we are using the value of the <input> to signify which function we should use
        action = request.POST.get('action')
        if action == 'add':
            # capture the value submitted through the <input> tag
            listing_id=request.POST.get('listing_id')
            # Fetch the listing that the user wanted to add to their watchlist through the database
            user = request.user
            print(f"Listing ID: {listing_id} and User: {user}")
            wl_listing=WatchList(user=user, listing=Listing.objects.get(id=listing_id))
            # check to see if it already exists. We don't want duplicate items.
            if WatchList.objects.filter(user=user, listing_id=listing_id).exists():
                print("Listing already added to the watchlist")
            else:
                wl_listing.save()   
    
    return render(request, 'auctions/listing.html',{
        'listing': listing,
        'bidform': BidForm()
    })
    
def watch_list(request, user):
    ### TO DO - Need to add a remove button to remove an item from the watch list
    # need to pass the users watch list in
    watchlist = WatchList.objects.filter(user_id=request.user.id)
    
    if request.method == 'POST':
        # capture the value of the listing assigned to that removal button
        # don't confuse listing_id with the model Listing, this is a listing in the WatchList
        watchlist_id = request.POST.get('watchlist_id')
        # get the WatchList with that exact id
        watchlist = WatchList.objects.get(id=watchlist_id)
        print(f'{watchlist.user.id}')
        watchlist.delete()
        if watchlist_id: 
            ### TO DO - Figure out why its user=request.user.username and not watchlist=watchlist ie(why pass the user and not the watchlist)
            return redirect('watch_list', user=request.user.username)
        else:
            return redirect('watchlist')
        
    
    return render(request, 'auctions/watchlist.html',{'watchlist': watchlist})