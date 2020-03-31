# # message/consumers.py
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.shortcuts import render

connected = {}


def main(request, **kwargs):
    # print(request)
    # print("wa")
    print(request)
    print("aaaaa")
    print(kwargs)
    print(request['url_route']['kwargs'])
    cons = BlogConsumer(request)
    connected[request['client'][1]] = cons
    return cons

#in dms (plan): when sent, include room name in client javascript


class BlogConsumer(WebsocketConsumer):

    def connect(self):
        # print(self.scope['url_route']['kwargs'])
        # print(self.__dict__)
        self.name = self.scope['client'][1]
        self.accept()

    def disconnect(self, close_code):
        del connected[self.name]
        print("disconnected")
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print(message)

        for i in connected.values():
            if i:
                i.send(text_data=json.dumps({
                    'message': message
                }))
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