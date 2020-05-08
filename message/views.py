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
        if user and user.token != '':
            logs = Message.objects.filter(Q(author=user) | Q(recipient=user))
            friends = user.friends.all()
            for userfriend in friends:
                otherfriends = userfriend.friends.all()
                if otherfriends.filter(id=user.id).exists():
                    conversations.append(userfriend)

            for msg in logs:
                if msg.recipient == conversations[0] or msg.author == conversations[0]:
                    if msg.recipient == user and not msg.seen:
                        msg.seen = True
                        msg.save()
                        if msg.recipient.username in blog.consumers.usersockets:
                            for i in blog.consumers.usersockets[msg.recipient.username]:
                                if i in blog.consumers.connected and blog.consumers.connected[i]:
                                    blog.consumers.connected[i].send(text_data=json.dumps({
                                        'type': 'seen',
                                        'sender': msg.author.username
                                    }))
                    currentchatlog.append(msg)
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
    if user and currentuser:
        friends = user.friends.all()
        otherfriends = currentuser.friends.all()
        legitfriends = friends.filter(id=currentuser.id).exists() and otherfriends.filter(id=user.id).exists()
        if legitfriends:
            currentchatlog = Message.objects.filter((Q(author=user) | Q(recipient=user)) &
                                                    (Q(author=currentuser) | Q(recipient=currentuser)))

            full = []
            for i in currentchatlog:
                if not i.seen and i.recipient == currentuser:
                    i.seen = True
                    i.save()
                message = i.content
                message = message.replace('&', '&amp;')
                message = message.replace('<', '&lt;')
                message = message.replace('>', '&gt;')
                full.append((i.author.username, message))
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
            response = json.dumps(full)
            response = HttpResponse(response)
            return response

    response = json.dumps(False)
    response = HttpResponse(response)

    return response

