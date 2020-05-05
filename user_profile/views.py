from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from blog.models import Post
from .models import User
from message.models import Message
from django.db.models import Q
import base64
import hashlib


def home(request):

    posts = Post.objects.filter(parent_id=None).order_by('date_posted').reverse()
    context = {
        'posts': [],
        'unseen': []
    }

    # this if block and the 'unseen' key in context is for dm notifications
    if request.COOKIES.get('auth_cookie'):
        token = base64.standard_b64encode(hashlib.sha256(request.COOKIES.get('auth_cookie').encode()).digest()).decode()
        print(token)
        user = User.objects.filter(token=token).first()
        if user:
            context['unseen'] = Message.objects.filter(Q(recipient=user) & Q(seen=False))

    for i in posts:
        comments = Post.objects.filter(parent_id=i.id).order_by('date_posted')
        if comments:
            context['posts'].append([i, comments])
        else:
            context['posts'].append([i, []])

    return render(request, 'user_profile/profile.html', context)
