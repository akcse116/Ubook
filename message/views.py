from django.shortcuts import render,redirect
from django.http import HttpResponse
from user_profile.models import User
from .models import Message
from django.db.models import Q
import json
import hashlib
import base64
import blog.consumers


def home(request):
    conversations = []
    currentchatlog = []
    unseen = []
    print(request.COOKIES.get('auth_cookie'))
    if request.COOKIES.get('auth_cookie'):
        token = base64.standard_b64encode(hashlib.sha256(request.COOKIES.get('auth_cookie').encode()).digest()).decode()
        print(token)
        user = User.objects.filter(token=token).first()
        if user:
            logs = Message.objects.filter(Q(author=user) | Q(recipient=user))

            for msg in logs:
                if msg.recipient != user and msg.recipient not in conversations:
                    conversations.insert(0, msg.recipient)
                elif msg.author != user and msg.author not in conversations:
                    conversations.insert(0, msg.author)

            for msg in logs:
                if msg.recipient == conversations[0] or msg.author == conversations[0]:
                    currentchatlog.append(msg)
                    if msg.recipient == user and not msg.seen:
                        msg.seen = True
                        msg.save()
                elif msg.recipient != conversations[0] and msg.recipient == user and not msg.seen:
                    unseen.append(msg)

            print(conversations)
            print(currentchatlog)

            context = {
                'conversations': conversations,
                'log': currentchatlog,
                'user': user,
                'unseen': unseen
            }
            response = render(request, 'message/chatlog.html', context)
            if conversations:
                response.set_cookie('current_user_chat', conversations[0].username)
            else:
                response.set_cookie('current_user_chat', '0')
        else:
            response = redirect('/')
    else:
        response = redirect('/')
    return response

# get user's token from request's cookie, search it up on db
# get first message where this person is either sender or receiver, display their log
# get other messages where this person is either sender or receiver, put the other user in the messages list


def switchconvo(request, user):
    token = base64.standard_b64encode(hashlib.sha256(request.COOKIES.get('auth_cookie').encode()).digest()).decode()
    currentuser = User.objects.filter(token=token).first()
    user = User.objects.filter(username=user).first()
    currentchatlog = Message.objects.filter((Q(author=user) | Q(recipient=user)) &
                                            (Q(author=currentuser) | Q(recipient=currentuser)))

    full = []
    for i in currentchatlog:
        if not i.seen and i.recipient == currentuser:
            i.seen = True
            i.save()
        full.append((i.author.username, i.content))
    # full = [(i.author.username, i.content) for i in currentchatlog]
    recipient = currentuser.username
    sender = user.username
    print(blog.consumers.usersockets)
    print(user.username)
    if recipient in blog.consumers.usersockets:
        for i in blog.consumers.usersockets[recipient]:
            if i in blog.consumers.connected and blog.consumers.connected[i]:
                blog.consumers.connected[i].send(text_data=json.dumps({
                    'type': 'seen',
                    'sender': sender
                }))
    if full:
        response = json.dumps(full)
        response = HttpResponse(response)
        response.set_cookie('current_user_chat', user)
    else:
        response = json.dumps(False)
        response = HttpResponse(response)

    return response

