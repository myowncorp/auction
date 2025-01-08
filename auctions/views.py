from django.contrib.auth import authenticate, login, logout, admin
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required


from .models import User, Listing, WatchList, Bid, Comment
from .forms import ListingForm, BidForm, CommentForm


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


@login_required
def create_listing(request):

    if request.method == "POST":
        f = ListingForm(request.POST)
        if f.is_valid:
            f.instance.owner = request.user
            f.save()
        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, 'auctions/createlisting.html', {
            'form': ListingForm()
        })


@login_required
def listing(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    # get the comments based on the listing_id
    comments = Comment.objects.filter(listing=listing)

    # get the highest bid object
    highest_bid = listing.bid.order_by('-amount').first()
    highest_bidder = highest_bid.bidder
    if request.method == 'POST':

        # get the value of the action, we are using the value of the <input> to signify which function we should use
        action = request.POST.get('action')
        if action == 'add':
            # capture the value= submitted through the <input name=listing_id>
            listing_id = request.POST.get('listing_id')
            # Fetch the listing that the user wanted to add to their watchlist through the database
            user = request.user
            print(f"Listing ID: {listing_id} and User: {user}")
            wl_listing = WatchList(
                user=user, listing=Listing.objects.get(id=listing_id))
            # check to see if it already exists. We don't want duplicate items.
            if WatchList.objects.filter(user=user, listing_id=listing_id).exists():
                print("Listing already added to the watchlist")
            else:
                wl_listing.save()

        if action == 'bid':
            # This will pull all the relevant data
            bid = BidForm(request.POST)

            if bid.is_valid():
                amount = bid.cleaned_data['amount']
                # if the amount bid is less then the start_bid(Listing) or the highest bid, return an error to the user
                if amount <= listing.start_bid or amount <= listing.get_highest_bid():
                    return render(request, 'auctions/listing.html', {
                        'message': "Bid must be greater than starting price and highest bid",
                        'listing': listing,
                        'bidform': BidForm()})
                else:
                    bidder = request.user
                    print(f"The user of this bid: {
                          bidder} on {listing} for {amount}")
                    bid = Bid(bidder=bidder, listing=listing, amount=amount)
                    bid.save()

        if action == 'close':
            # capture the value= submitted through the <input name=listing_id> same as in add
            listing_id = request.POST.get('listing_id')
            listing = Listing.objects.get(id=listing_id)
            # set is_active to False, this way we can distinguish
            listing.is_active = not listing.is_active
            listing.save()
            return redirect('index')

        if action == 'comment':
            print(CommentForm(request.POST))
            c = CommentForm(request.POST)
            if c.is_valid():
                c = c.save(commit=False)
                # set the comment.user to request.user
                c.user = request.user
                # set comment.listing to listing
                c.listing = listing
                # we have the comment because we passed it is as a model form so comment.comment is already set
                c.save()
                return redirect('listing', listing_id=listing.id)

    return render(request, 'auctions/listing.html', {
        'highest_bidder': highest_bidder,
        'listing': listing,
        'bidform': BidForm(),
        'commentform': CommentForm(),
        'comments': comments
    })


def watch_list(request, user):
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
            return redirect('watch_list', user=request.user.username)
        else:
            return redirect('watchlist')

    return render(request, 'auctions/watchlist.html', {'watchlist': watchlist, })
