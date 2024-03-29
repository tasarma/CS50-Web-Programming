from __future__ import annotations

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class NewPost(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
    )
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    number_of_likes = models.IntegerField(default=0)


class Profile(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_profile',
    )
    follower = models.ManyToManyField(
        User, blank=True, related_name='follower',
    )
    following = models.ManyToManyField(
        User, blank=True, related_name='following',
    )
