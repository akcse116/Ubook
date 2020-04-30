# # message/consumers.py
import json
# from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
# from django.shortcuts import render
from .models import Message
from user_profile.models import User

connected = {}
usersockets = {}
addrtouser = {}

# change connected to list {address:[e-mail, websocket]}
# in js send e-mail of sender and e-mail of receiver as websocket
# check the people connected and see if receiver e-mail is in value,
# if yes, send to their socket and sender's socket and save to db, if no, just send to sender's socket and save to db

# switching between chatlogs: AJAX GET request with the two users' id/email in the path
# go to db, search for where the sender is user 1 and receiver is user 2 or vice versa,
# make sure in chronological order (order_by('date_posted'))
# order them in an array [[user, message], [], ....]


def main(request):
    # print(request)
    # print("wa")
    # print(request)
    # print("aaaaa")
    # print(user)
    # print(request['url_route']['kwargs']['user'])
    cons = ChatConsumer(request)
    username = request['url_route']['kwargs']['user']
    addr = request['client'][1]
    connected[addr] = cons
    addrtouser[addr] = username
    if username in usersockets:
        usersockets[username].append(addr)
    else:
        usersockets[username] = [addr]
    return cons

# in dms (plan): when sent, include room name in client javascript


class ChatConsumer(WebsocketConsumer):

    def connect(self):
        # print(self.scope['url_route']['kwargs'])
        # print(self.__dict__)
        print("connect message")
        self.name = self.scope['client'][1]
        self.accept()

    def disconnect(self, close_code):
        print(usersockets)
        usersock = addrtouser[self.name]
        try:
            usersockets[usersock].remove(self.name)
        except ValueError:
            pass
        del connected[self.name]
        del addrtouser[self.name]
        if len(usersockets[usersock]) <= 0:
            del usersockets[usersock]
        print("disconnected")
        print(usersockets)
        print(addrtouser)
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender = text_data_json['sender']
        recipient = text_data_json['recipient']

        senderuser = User.objects.filter(username=sender).first()
        recipientuser = User.objects.filter(username=recipient).first()

        msg = Message(content=message, author=senderuser, recipient=recipientuser)
        msg.save()
        print(message)

        if sender in usersockets:
            for i in usersockets[sender]:
                if i in connected and connected[i]:
                    connected[i].send(text_data=json.dumps({
                        'sender': sender,
                        'message': message
                    }))
        if recipient in usersockets:
            for i in usersockets[recipient]:
                if i in connected and connected[i]:
                    connected[i].send(text_data=json.dumps({
                        'sender': sender,
                        'message': message
                    }))


