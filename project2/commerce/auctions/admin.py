from django.contrib import admin
from .models import User,CreateListing, WatchList, Bids

# Register your models here.

admin.site.register(User)
admin.site.register(CreateListing)
admin.site.register(WatchList)
admin.site.register(Bids)