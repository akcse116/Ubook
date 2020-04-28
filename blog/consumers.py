# # message/consumers.py
import json
import random
from channels.generic.websocket import WebsocketConsumer
from django.shortcuts import render
from django.http import HttpResponse
from .models import Post
from django.conf import settings
from user_profile.models import User


connected = {}


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
    # media = 'http://'+ request.META['SERVER_NAME'] + ':'+ request.META['SERVER_PORT'] + settings.MEDIA_URL + media.name
    else:
        media = None
        media_name = None
    record = Post(title="A", content=body, media=media_name)
    record.save()

    body = body.replace('&', '&amp;')
    body = body.replace('<', '&lt;')
    body = body.replace('>', '&gt;')

    #send post information via websockets
    for i in connected.values():
        i.send(text_data=json.dumps({
            'type': 'post',
            'body': body,
            'author': str(record.author),
            'date': str(record.date_posted),
            'media': hasImg,
            'id': record.id,
            'medialink': media_name
        }))
    return HttpResponse("received")


class BlogConsumer(WebsocketConsumer):

    def connect(self):
        # print(self.scope['url_route']['kwargs'])
        # print(self.__dict__)
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
            changelike = Post.objects.get(id=int(text_data_json['id']))
            changelike.likes = changelike.likes + 1
            userlike = bool(changelike.likes)
            changelike.save()

            for i in connected.values():
                if i:
                    i.send(text_data=json.dumps({
                        'type': 'like',
                        'id': text_data_json['id'],
                        'status': userlike
                    }))
        elif text_data_json['type'] == 'comment':
            record = Post(title="C", content=text_data_json['body'], parent_id=text_data_json['id'])
            record.save()

            for i in connected.values():
                if i:
                    i.send(text_data=json.dumps({
                        'type': 'comment',
                        'id': record.id,
                        'parentid': record.parent_id,
                        'date': str(record.date_posted),
                        'body': text_data_json['body'],
                        'author': str(record.author)
                    }))
