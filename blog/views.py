import random
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Post
from user_profile.models import User
from message.models import Message
from django.db.models import Q
from django.conf import settings
import base64
import hashlib


def home(request):
    if request.method == 'POST':
        body = request.POST['post-body']
        if request.FILES:
            media = request.FILES['post-media']
            media_ID = random.randrange(1000000)
            media_type = media.name.split('.')[1]
            upload_name = 'upload_'+ str(media_ID) +'.'+ media_type
            # media_name = 'http://'+ request.META['HTTP_HOST'] + settings.MEDIA_URL + upload_name
            media_name = settings.MEDIA_URL + upload_name
            while Post.objects.filter(media = media_name):
                media_ID = random.randrange(1000000)
                media_type = media.name.split('.')[1]
                upload_name = 'upload_'+ str(media_ID) +'.'+ media_type
                # media_name = 'http://'+ request.META['HTTP_HOST'] + settings.MEDIA_URL + upload_name
                media_name = settings.MEDIA_URL + upload_name
            storage_file_path = settings.MEDIA_ROOT + '/'+ upload_name
            file_content = media.file.read()
            with open(storage_file_path, 'wb') as file:
                file.write(file_content)
        # media = 'http://'+ request.META['SERVER_NAME'] + ':'+ request.META['SERVER_PORT'] + settings.MEDIA_URL + media.name
        else:
            media_name = None
            record = Post(title="A", content=body, media=media_name)
            record.save()
        
    else:
        None

    posts = Post.objects.filter(parent_id=None).order_by('date_posted').reverse()
    context = {
        'friendposts': [],
        'posts': [],
        'unseen': [],
        'user': ''
    }

    if request.COOKIES.get('auth_cookie'):
        token = base64.standard_b64encode(hashlib.sha256(request.COOKIES.get('auth_cookie').encode()).digest()).decode()
        print(token)
        user = User.objects.filter(token=token).first()
        if user and user.token != '':
            context['unseen'] = Message.objects.filter(Q(recipient=user) & Q(seen=False))
            context['user'] = user
            friends = user.friends.all()
            likes = user.likes.all()
            hostname = 'http://'+ request.META['HTTP_HOST']

            for i in posts:
                comments = Post.objects.filter(parent_id=i.id).order_by('date_posted')
                isself = i.author == user
                isfriend = friends.filter(id=i.author.id).exists()
                isliked = likes.filter(id=i.id).exists()
                if comments:
                    if isfriend:
                        context['friendposts'].append([i, comments, isself, isfriend, isliked, hostname + str(i.media)])
                    else:
                        context['posts'].append([i, comments, isself, isfriend, isliked, hostname + str(i.media)])
                else:
                    if isfriend:
                        context['friendposts'].append([i, [], isself, isfriend, isliked, hostname + str(i.media)])
                    else:
                        context['posts'].append([i, [], isself, isfriend, isliked, hostname + str(i.media)])
            return render(request, 'blog/home.html', context)
    return redirect('/')


def add_friend(request, username, friend):
    print(username)
    print(friend)
    friendobj = User.objects.filter(username=friend).first()
    user = User.objects.filter(username=username).first()
    if friendobj and user:
        friends = user.friends.all()
        if not friends.filter(username=friendobj).exists():
            user.friends.add(friendobj)
            user.save()
            return HttpResponse('added')
        return HttpResponse('friend already added')
    return HttpResponse('error')


def remove_friend(request, username, friend):
    user = User.objects.filter(username=username).first()
    friendobj = User.objects.filter(username=friend).first()
    if friendobj and user:
        friends = user.friends.all()
        if friends.filter(username=friendobj).exists():
            user.friends.remove(friendobj)
            user.save()
            return HttpResponse('removed')
        return HttpResponse('not originally friended')
    return HttpResponse('error')
