from channels.generic.websocket import WebsocketConsumer


connected = {}


def main(request, **kwargs):
    print("========\nprofile received:\n"+str(request['url_route']['kwargs'])+"\n=========")
    cons = ChatConsumer(request)
    connected[request['client'][1]] = cons
    return cons


class ChatConsumer(WebsocketConsumer):

    def connect(self):
        # print(self.scope['url_route']['kwargs'])
        # print(self.__dict__)
        print("connected")
        self.name = self.scope['client'][1]
        self.accept()
        self.send(text_data="[Welcome %s!]" % self.name)

    def disconnect(self, close_code):
        del connected[self.name]
        print("disconnected")
        pass

    def receive(self, *, text_data):
        print("Socket received: " + text_data)
