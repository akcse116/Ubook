# # message/consumers.py
import json
import random
from channels.generic.websocket import WebsocketConsumer
from django.shortcuts import render
from django.http import HttpResponse
from .models import Post
from django.conf import settings
from user_profile.models import User
import base64
import hashlib


connected = {}
usersockets = {}
addrtouser = {}


def main(request):
    cons = BlogConsumer(request)
    connected[request['client'][1]] = cons
    return cons


def createPost(request):
    body = request.POST['post-body']
    print(request.META['HTTP_HOST'])
    hasImg = False  # if this is true, client will call http GET through AJAX to get the image
    if request.FILES:
        hasImg = True
        media = request.FILES['post-media']
        media_ID = random.randrange(1000000)
        media_type = media.name.split('.')[1]
        upload_name = 'upload_'+ str(media_ID) +'.'+ media_type
        media_name = 'http://'+ request.META['HTTP_HOST'] + settings.MEDIA_URL + upload_name
        while Post.objects.filter(media = media_name):
            media_ID = random.randrange(1000000)
            media_type = media.name.split('.')[1]
            upload_name = 'upload_'+ str(media_ID) +'.'+ media_type
            media_name = 'http://'+ request.META['HTTP_HOST'] + settings.MEDIA_URL + upload_name
        storage_file_path = settings.MEDIA_ROOT + '/'+ upload_name
        file_content = media.file.read()
        with open(storage_file_path, 'wb') as file:
            file.write(file_content)
    else:
        media = None
        media_name = None

    if request.COOKIES.get('auth_cookie'):
        token = base64.standard_b64encode(hashlib.sha256(request.COOKIES.get('auth_cookie').encode()).digest()).decode()
        print(token)
        user = User.objects.filter(token=token).first()

        if user:
            print(user.username)
            record = Post(title="Post", content=body, media=media_name, author=user)
            record.save()

            body = body.replace('&', '&amp;')
            body = body.replace('<', '&lt;')
            body = body.replace('>', '&gt;')
            name = record.author.first_name + ' ' + record.author.last_name
            name = name.replace('&', '&amp;')
            name = name.replace('<', '&lt;')
            name = name.replace('>', '&gt;')

            friends = user.friends.all()

            #send post information via websockets
            for i in connected.keys():
                if connected[i]:
                    otheruser = User.objects.filter(username=addrtouser[i]).first()
                    isfriend = False
                    if otheruser:
                        isfriend = friends.filter(id=otheruser.id).exists()
                    print(isfriend)
                    print(otheruser)
                    print(friends)
                    print(addrtouser[i])
                    connected[i].send(text_data=json.dumps({
                        'type': 'post',
                        'body': body,
                        'author': name,
                        'username': record.author.username,
                        'date': str(record.date_posted),
                        'media': hasImg,
                        'id': record.id,
                        'medialink': media_name,
                        'friend': isfriend
                    }))
            return HttpResponse("received")
        return HttpResponse("error invalid auth_cookie")
    return HttpResponse("error invalid auth_cookie")


class BlogConsumer(WebsocketConsumer):

    def connect(self):
        # print(self.scope['url_route']['kwargs'])
        # print(self.__dict__)

        cookiebytes = [elem for elem in self.scope['headers'] if elem[0] == b'cookie']
        if len(cookiebytes) > 0 and len(cookiebytes[0]) > 0:
            cookies = cookiebytes[0][1].split(b"; ")
            token = ''
            for cookie in cookies:
                kv = cookie.split(b'=', 1)
                if kv[0] == b'auth_cookie':
                    token = kv[1]
            print(token)
            token = base64.standard_b64encode(hashlib.sha256(token).digest()).decode()
            print(token)
            user = User.objects.filter(token=token).first()
            if user:
                username = user.username
                print('correct user')
                addr = self.scope['client'][1]
                connected[addr] = self
                addrtouser[addr] = username
                if username in usersockets:
                    usersockets[username].append(addr)
                else:
                    usersockets[username] = [addr]
                print(usersockets)
                print(addrtouser)

        self.name = self.scope['client'][1]
        print("connect blog")
        self.accept()

    def disconnect(self, close_code):
        del connected[self.name]
        print("disconnected")
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print(text_data_json)

        if text_data_json['type'] == 'like':
            user = User.objects.filter(username=text_data_json['user']).first()
            if user:
                likes = user.likes.all()
                isliked = likes.filter(id=int(text_data_json['id'])).first()
                if isliked:
                    changelike = Post.objects.get(id=int(text_data_json['id']))
                    changelike.likes = changelike.likes - 1
                    changelike.save()
                    user.likes.remove(changelike)
                    user.save()
                    likestatus = False
                else:
                    changelike = Post.objects.get(id=int(text_data_json['id']))
                    changelike.likes = changelike.likes + 1
                    changelike.save()
                    user.likes.add(changelike)
                    user.save()
                    likestatus = True

                print(usersockets)

                for i in usersockets[user.username]:
                    if i in connected and connected[i]:
                        connected[i].send(text_data=json.dumps({
                            'type': 'like',
                            'id': text_data_json['id'],
                            'status': likestatus,
                            'user': text_data_json['user']
                        }))
        elif text_data_json['type'] == 'comment':
            body = text_data_json['body']
            user = User.objects.filter(username=text_data_json['user']).first()
            if user:
                record = Post(title="Comment", content=text_data_json['body'], parent_id=text_data_json['id'], author=user)
                record.save()

                body = body.replace('&', '&amp;')
                body = body.replace('<', '&lt;')
                body = body.replace('>', '&gt;')
                name = record.author.first_name + ' ' + record.author.last_name
                name = name.replace('&', '&amp;')
                name = name.replace('<', '&lt;')
                name = name.replace('>', '&gt;')

                for i in connected.values():
                    if i:
                        i.send(text_data=json.dumps({
                            'type': 'comment',
                            'id': record.id,
                            'parentid': record.parent_id,
                            'date': str(record.date_posted),
                            'body': body,
                            'author': name,
                            'username': record.author.username,
                        }))
