# # message/consumers.py
import json
# from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
# from django.shortcuts import render

connected = {}


def main(request, **kwargs):
    # print(request)
    # print("wa")
    # print(request)
    # print("aaaaa")
    # print(kwargs)
    # print(request['url_route']['kwargs'])
    cons = ChatConsumer(request)
    connected[request['client'][1]] = cons
    return cons

#in dms (plan): when sent, include room name in client javascript


class ChatConsumer(WebsocketConsumer):

    def connect(self):
        # print(self.scope['url_route']['kwargs'])
        # print(self.__dict__)
        print("connect message")
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

