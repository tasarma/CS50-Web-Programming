from __future__ import annotations

from django.contrib import admin

from .models import Bids
from .models import CreateListing
from .models import User
from .models import WatchList

# Register your models here.

admin.site.register(User)
admin.site.register(CreateListing)
admin.site.register(WatchList)
admin.site.register(Bids)
