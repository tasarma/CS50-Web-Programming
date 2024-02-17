from __future__ import annotations

from datetime import datetime

from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.db import IntegrityError
from django.http import HttpRequest
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Bids
from .models import CreateListing
from .models import User
from .models import WatchList

# from django.http import HttpResponse
# from django.shortcuts import redirect


def index(request: HttpRequest) -> HttpResponse:
    return render(
        request,
        'auctions/index.html',
        {
            'items': CreateListing.objects.all(),
        },
    )


def login_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':

        # Attempt to sign user in
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(
                request,
                'auctions/login.html',
                {
                    'message': 'Invalid username and/or password.',
                },
            )
    else:
        return render(request, 'auctions/login.html')


def logout_view(request: HttpRequest) -> HttpResponse:
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']

        # Ensure password matches confirmation
        password = request.POST['password']
        confirmation = request.POST['confirmation']
        if password != confirmation:
            return render(
                request,
                'auctions/register.html',
                {
                    'message': 'Passwords must match.',
                },
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request,
                'auctions/register.html',
                {
                    'message': 'Username already taken.',
                },
            )
        login(request, user)
        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, 'auctions/register.html')


def create_listing(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        data = CreateListing()
        data.owner = request.user.username
        data.title = request.POST['title']
        data.description = request.POST['description']
        data.initialBid = request.POST['initialBid']
        data.category = request.POST['category']
        now = datetime.now()
        data.time = now.strftime(' %d %B %Y, %X')

        # Check if there is a link
        if request.POST['url']:
            data.link = request.POST['url']
        else:
            data.link = 'https://bitsofco.de/content/images/2018/12/broken-1.png'
        data.save()
        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, 'auctions/createlisting.html')


def listing_page(request: HttpRequest, key: int) -> HttpResponse:
    if request.method == 'GET':

        # Check if there is listing
        try:
            item = CreateListing.objects.get(id=key)
        except ValueError:
            item = 'Sorry! Listing not exist'

        return render(
            request,
            'auctions/listing_page.html',
            {
                'item': item,
                'owner': True if item.owner == request.user.username else False,
                'errorgreen': request.COOKIES.get('errorgreen'),
                'watchListItem': (
                    True
                    if WatchList.objects.filter(
                        user=request.user.username,
                        listingId=key,
                    )
                    else False
                ),
            },
        )
    else:
        return HttpResponseRedirect(reverse('index'))


def addToWatchlist(request: HttpRequest, key: int) -> HttpResponse:
    if request.user.username:
        watchlisting = WatchList()
        watchlisting.user = request.user.username
        watchlisting.listingId = key
        watchlisting.save()
        return HttpResponseRedirect(reverse('listing_page', args=(key,)))
    else:
        return HttpResponseRedirect(reverse('index'))


def removeFromWatchlist(request: HttpRequest, key: int) -> HttpResponse:
    if request.user.is_authenticated:
        try:
            watchlisting = WatchList.objects.get(
                user=request.user.username,
                listingId=key,
            )
            watchlisting.delete()
            return HttpResponseRedirect(reverse('listing_page', args=(key,)))
        except ValueError:
            return HttpResponseRedirect(reverse('listing_page', args=(key,)))
    else:
        return HttpResponseRedirect(reverse('index'))


def addBid(request: HttpRequest, key: int) -> HttpResponse:
    current_bid = CreateListing.objects.get(id=key).initialBid
    if request.method == 'POST':
        entered_bid = int(request.POST['bid'])
        if entered_bid > current_bid:
            item = CreateListing.objects.get(id=key)
            item.initialBid = entered_bid
            item.save()

            # Set new bid
            try:
                if Bids.objects.filter(id=key):
                    Bids.objects.filter(id=key).delete()
                item_data = Bids()
                item_data.user = request.user.username
                item_data.title = item.title
                item_data.bid = entered_bid
                item_data.listingId = key
                item.save()
            except ValueError:
                item_data = Bids()
                item_data.user = request.user.username
                item_data.title = item.title
                item_data.bid = entered_bid
                item_data.listingId = key
                item.save()
            response = HttpResponseRedirect(
                reverse('listing_page', args=(key,)),
            )
            response.set_cookie('errorgreen', 'Bid changed!', max_age=3)
            return response
        else:
            return HttpResponseRedirect(reverse('listing_page', args=(key,)))
    else:
        return HttpResponseRedirect(reverse('index'))


def closeBid(request: HttpRequest, key: int) -> HttpResponse:
    return HttpResponseRedirect(reverse('listing_page', args=(key,)))


def watchList(request: HttpRequest, username: str) -> HttpResponse:
    if request.user.is_authenticated:
        try:
            userData = WatchList.objects.filter(user=request.user.username)
            items = []
            for i in userData:
                items.append(CreateListing.objects.filter(id=i.listingId))
            try:
                userData = WatchList.objects.filter(user=request.user.username)
                wcount = len(userData)
            except ValueError:
                wcount = None
            return render(
                request,
                'auctions/watchlist_page.html',
                {
                    'items': items,
                    'wcount': wcount,
                },
            )

        except ValueError:
            try:
                userData = WatchList.objects.filter(user=request.user.username)
                wcount = len(userData)
            except ValueError:
                wcount = None
            return render(
                request,
                'auctions/watchlist_page.html',
                {
                    'items': None,
                    'wcount': wcount,
                },
            )
