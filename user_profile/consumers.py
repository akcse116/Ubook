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

        # if text_data_json['type'] == 'like':
        #     changelike = Post.objects.get(id=int(text_data_json['id']))
        #     if changelike.likes == 0:
        #         changelike.likes += 1
        #     else:
        #         changelike.likes -= 1
        #     userlike = bool(changelike.likes)
        #     changelike.save()
        #
        #     for i in connecteduser.values():
        #         if i:
        #             i.send(text_data=json.dumps({
        #                 'type': 'like',
        #                 'id': text_data_json['id'],
        #                 'status': userlike
        #             }))
        # elif text_data_json['type'] == 'comment':
        #     record = Post(title="C", content=text_data_json['body'], parent_id=text_data_json['id'])
        #     record.save()
        #
        #     for i in connecteduser.values():
        #         if i:
        #             i.send(text_data=json.dumps({
        #                 'type': 'comment',
        #                 'id': record.id,
        #                 'parentid': record.parent_id,
        #                 'date': str(record.date_posted),
        #                 'body': text_data_json['body'],
        #                 'author': str(record.author)
        #             }))
