from __future__ import annotations

from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register, name='register'),
    path('newpost', views.new_post, name='new_post'),
    path('profile/<str:username>', views.profile_page, name='profile_page'),
    path('follow_user/<str:username>', views.follow_user, name='follow_user'),
    path('following', views.following, name='following_posts'),
]
