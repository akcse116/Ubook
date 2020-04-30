from channels.generic.websocket import WebsocketConsumer
from blog.models import Post
import blog.consumers
import json

connecteduser = {}


def main(request, **kwargs):
    print("========\nprofile received:\n"+str(request['url_route']['kwargs'])+"\n=========")
    cons = UserConsumer(request)
    connecteduser[request['client'][1]] = cons
    return cons


class UserConsumer(WebsocketConsumer):

    def connect(self):
        # print(self.scope['url_route']['kwargs'])
        # print(self.__dict__)
        print("connecteduser")
        self.name = self.scope['client'][1]
        self.accept()
        self.send(text_data="[Welcome %s!]" % self.name)

    def disconnect(self, close_code):
        del connecteduser[self.name]
        print("disconnected")
        pass

    def receive(self, *, text_data):
        text_data_json = json.loads(text_data)
        print(text_data_json)

