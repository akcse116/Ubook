from django.shortcuts import render, redirect
from django.http import HttpResponse
from blog.models import Post
# from .models import User, FriendRequest
from .models import User


def home(request):

    posts = Post.objects.filter(parent_id=None).order_by('date_posted').reverse()
    context = {
        'posts': []
    }

    for i in posts:
        comments = Post.objects.filter(parent_id=i.id).order_by('date_posted')
        if comments:
            context['posts'].append([i, comments])
        else:
            context['posts'].append([i, []])

    return render(request, 'user_profile/profile.html', context)


def send_friend_request(request, id):
    from_user = request.user
    to_user = User.objects.get(id=id)
    frequest = FriendRequest.objects.get_or_create(from_user=from_user, to_user=to_user)
    #return redirect('#')


def accept_request(request, id):
    frequest = FriendRequest.objects.get(id=id)
    user1 = request.user
    user2 = frequest.from_user
    user1.friends.add(user2)
    user2.friends.add(user1)
    #return redirect('home')