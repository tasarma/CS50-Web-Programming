from __future__ import annotations

from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('wiki/<str:entry>', views.entry_page, name='entry'),
    path('search', views.search, name='search'),
    path('new', views.new, name='new'),
    path('random', views.random, name='random'),
]
