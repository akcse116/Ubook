# # message/consumers.py
import json
from channels.generic.websocket import WebsocketConsumer
from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from .models import Post
from django.conf import settings
from user_profile.models import User


connected = {}


def main(request, **kwargs):
    # print(request)
    # print("wa")
    # print(request)
    # print("aaaaa")
    # print(kwargs)
    # print(request['url_route']['kwargs'])
    cons = BlogConsumer(request)
    connected[request['client'][1]] = cons
    return cons


def createPost(request):
    body = request.POST['post-body']
    hasImg = False  # if this is true, client will call http GET through AJAX to get the image
    # if request.FILES:
    #     hasImg = True
    #     media = request.FILES['post-media']
    #     storage_file_path = settings.MEDIA_ROOT + media.name
    #     file_content = media.file.read()
    #     with open(storage_file_path, 'wb') as file:
    #         file.write(file_content)
    # else:
    #     media = None
    # post = Post(title = 'title-1', content = body, media = media, author= User.objects.get(username='tiffany'))
    # post.save()

    #send post information via websockets
    for i in connected.values():
        i.send(text_data=json.dumps({
            'type': 'post',
            'body': body,
            'author': "person",
            'date': "0",
            'media': hasImg
        }))
        record = Post(content=body)
        record.save()
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

        # for i in connected.values():
        #     if i:
        #         i.send(text_data=json.dumps({
        #             'message': message
        #         }))
        # self.send(text_data=json.dumps({
        #     'message': message
        # }))


# chat/consumers.py
# import json
# from asgiref.sync import async_to_sync
# from channels.generic.websocket import WebsocketConsumer
#
# class ChatConsumer(WebsocketConsumer):
#     def connect(self):
#         self.room_name = self.scope['url_route']['kwargs']['room_name']
#         self.room_group_name = 'chat_%s' % self.room_name
#
#         # Join room group
#         async_to_sync(self.channel_layer.group_add)(
#             self.room_group_name,
#             self.channel_name
#         )
#
#         self.accept()
#
#     def disconnect(self, close_code):
#         # Leave room group
#         async_to_sync(self.channel_layer.group_discard)(
#             self.room_group_name,
#             self.channel_name
#         )
#
#     # Receive message from WebSocket
#     def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']
#
#         # Send message to room group
#         async_to_sync(self.channel_layer.group_send)(
#             self.room_group_name,
#             {
#                 'type': 'chat_message',
#                 'message': message
#             }
#         )
#
#     # Receive message from room group
#     def chat_message(self, event):
#         message = event['message']
#
#         # Send message to WebSocket
#         self.send(text_data=json.dumps({
#             'message': message
#         }))