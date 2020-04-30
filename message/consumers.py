# # message/consumers.py
import json
# from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.shortcuts import render, redirect
# from django.shortcuts import render
from .models import Message
import blog.consumers
from user_profile.models import User
import hashlib
import base64

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
    cons = ChatConsumer(request)
    # username = request['url_route']['kwargs']['user']
    # addr = request['client'][1]
    # connected[addr] = cons
    # addrtouser[addr] = username
    # if username in usersockets:
    #     usersockets[username].append(addr)
    # else:
    #     usersockets[username] = [addr]
    return cons

# in dms (plan): when sent, include room name in client javascript


class ChatConsumer(WebsocketConsumer):

    def connect(self):
        # print(self.scope['url_route']['kwargs'])
        # print(self.__dict__)
        username = self.scope['url_route']['kwargs']['user']
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
            if user and user.username == username:
                print('correct user')
                addr = self.scope['client'][1]
                connected[addr] = self
                addrtouser[addr] = username
                if username in usersockets:
                    usersockets[username].append(addr)
                else:
                    usersockets[username] = [addr]
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
        if text_data_json['type'] == 'message':
            message = text_data_json['message']
            sender = text_data_json['sender']
            recipient = text_data_json['recipient']

            senderuser = User.objects.filter(username=sender).first()
            recipientuser = User.objects.filter(username=recipient).first()

            if senderuser and recipientuser:
                msg = Message(content=message, author=senderuser, recipient=recipientuser)
                msg.save()
                if sender in usersockets:
                    for i in usersockets[sender]:
                        if i in connected and connected[i]:
                            connected[i].send(text_data=json.dumps({
                                'type': 'message',
                                'sender': sender,
                                'fullname': senderuser.first_name + ' ' + senderuser.last_name,
                                'message': message
                            }))
                if recipient in usersockets:
                    for i in usersockets[recipient]:
                        if i in connected and connected[i]:
                            connected[i].send(text_data=json.dumps({
                                'type': 'message',
                                'sender': sender,
                                'fullname': senderuser.first_name + ' ' + senderuser.last_name,
                                'message': message
                            }))
                if recipient in blog.consumers.usersockets:
                    for i in blog.consumers.usersockets[recipient]:
                        if i in blog.consumers.connected and blog.consumers.connected[i]:
                            blog.consumers.connected[i].send(text_data=json.dumps({
                                'type': 'message',
                                'sender': sender,
                                'fullname': senderuser.first_name + ' ' + senderuser.last_name,
                                'message': message
                            }))
            else:
                self.send(text_data=json.dumps({
                    'error': 'You are not a valid sender!'
                }))
        elif text_data_json['type'] == 'seen':
            sender = text_data_json['sender']
            recipient = text_data_json['recipient']
            recipientuser = User.objects.filter(username=recipient).first()
            msgs = Message.objects.filter(recipient=recipientuser)
            for msg in msgs:
                msg.seen = True
                msg.save()
            if recipient in blog.consumers.usersockets:
                for i in blog.consumers.usersockets[recipient]:
                    if i in blog.consumers.connected and blog.consumers.connected[i]:
                        blog.consumers.connected[i].send(text_data=json.dumps({
                            'type': 'seen',
                            'sender': sender
                        }))


