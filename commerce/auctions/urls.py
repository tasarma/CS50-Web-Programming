from __future__ import annotations

from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register, name='register'),
    path('createlisting', views.create_listing, name='createListing'),
    path('listing/<int:key>', views.listing_page, name='listing_page'),
    path(
        'addwatchlist/<int:key>',
        views.addToWatchlist,
        name='addToWatchlist',
    ),
    path(
        'removewatchlist/<int:key>',
        views.removeFromWatchlist,
        name='removeFromWatchlist',
    ),
    path('addbit/<int:key>', views.addBid, name='add_bid'),
    path('closebid/<int:key>', views.closeBid, name='close_bid'),
    path('watchlist/<str:username>', views.watchList, name='watchList'),
]
