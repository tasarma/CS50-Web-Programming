from __future__ import annotations

from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import NewPost
from .models import Profile
from .models import User


def index(request):
    if request.user.is_authenticated:
        posts = NewPost.objects.all()
        posts = posts.order_by('-timestamp').all()

        paginator = Paginator(posts, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(
            request,
            'network/index.html',
            {
                # 'posts': posts,
                'page_obj': page_obj,
            },
        )
    else:
        return HttpResponseRedirect(reverse('login'))


def login_view(request):
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
                'network/login.html',
                {
                    'message': 'Invalid username and/or password.',
                },
            )
    else:
        return render(request, 'network/login.html')


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']

        # Ensure password matches confirmation
        password = request.POST['password']
        confirmation = request.POST['confirmation']
        if password != confirmation:
            return render(
                request,
                'network/register.html',
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
                'network/register.html',
                {
                    'message': 'Username already taken.',
                },
            )
        login(request, user)
        user_profile = Profile(user=request.user)
        user_profile.save()
        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, 'network/register.html')


def new_post(request):
    if request.method == 'POST':
        user = request.user
        body = request.POST.get('new-post-body', '')
        if not body:
            return render(
                request,
                'network/new_post.html',
                {'error': 'Please enter a text for your new post.'},
            )
        new_post = NewPost(user=user, body=body)
        new_post.save()
        return redirect('index')
    else:
        return render(request, 'network/new_post.html')


@csrf_exempt
@login_required
def profile_page(request, username: str):
    try:
        user = User.objects.get(username=request.user.username)
        viewed_user = User.objects.get(username=username)
        followings = Profile.objects.get(user=user).following.all()
        follower = Profile.objects.get(user=viewed_user).follower.count()
        following = Profile.objects.get(user=viewed_user).following.count()
    except User.DoesNotExist:
        pass

    if request.method == 'GET':
        posts = viewed_user.posts.all()
        posts = posts.order_by('-timestamp').all()
        is_following = True if viewed_user in followings else False

        return render(
            request,
            'network/profile_page.html',
            {
                'user': user,
                'viewed_user': viewed_user,
                'posts': posts,
                'follower': follower,
                'following': following,
                'is_following': is_following,
            },
        )


@csrf_exempt
@login_required
def follow_user(request, username: str):
    try:
        user = User.objects.get(username=request.user.username)
        viewed_user = User.objects.get(username=username)
        user_profile = Profile.objects.get(user=user)
        viewed_user_profile = Profile.objects.get(user=viewed_user)
        followings = user_profile.following.all()
    except User.DoesNotExist:
        pass

    if request.method == 'POST':
        if viewed_user not in followings:
            user_profile.following.add(viewed_user)
            user_profile.save()

            viewed_user_profile.follower.add(user)
            viewed_user_profile.save()
            return JsonResponse({'is_following': True}, status=201)
        else:
            user_profile.following.remove(viewed_user)
            viewed_user_profile.follower.remove(user)
            return JsonResponse({'is_following': False}, status=201)
    else:
        return HttpResponseRedirect(reverse('index'))


@csrf_exempt
@login_required
def following(request):
    try:
        user = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user)
        followings = user_profile.following.all()
    except User.DoesNotExist:
        pass

    if request.method == 'GET':
        posts = NewPost.objects.filter(user__in=followings)
        posts = posts.order_by('-timestamp').all()
        return render(
            request,
            'network/index.html',
            {
                'posts': posts,
            },
        )
    else:
        return HttpResponseRedirect(reverse('login'))
