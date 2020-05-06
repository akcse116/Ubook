from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from blog.models import Post
from .models import User
from message.models import Message
from django.db.models import Q
import base64
import hashlib


def home(request):

    context = {
        'posts': [],
        'unseen': [],
        'user': ''
    }

    # this if block and the 'unseen' key in context is for dm notifications
    if request.COOKIES.get('auth_cookie'):
        token = base64.standard_b64encode(hashlib.sha256(request.COOKIES.get('auth_cookie').encode()).digest()).decode()
        print(token)
        user = User.objects.filter(token=token).first()
        if user and user.token != '':
            likes = user.likes.all()
            posts = Post.objects.filter(parent_id=None, author=user).order_by('date_posted').reverse()
            context['unseen'] = Message.objects.filter(Q(recipient=user) & Q(seen=False))
            context['user'] = user

            for i in posts:
                isliked = likes.filter(id=i.id).exists()
                comments = Post.objects.filter(parent_id=i.id).order_by('date_posted')
                if comments:
                    context['posts'].append([i, comments, isliked])
                else:
                    context['posts'].append([i, [], isliked])

            return render(request, 'user_profile/profile.html', context)
    return redirect('/')
