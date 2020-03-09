from django.shortcuts import render
from django.http import HttpResponse

messages = [
    {
        'user': 'person1',
        'lastmessage': 'hi',
        'lastsent': 'Jan. 1, 2020'
    },
    {
        'user': 'person2',
        'lastmessage': 'hello',
        'lastsent': 'Jan. 1, 2020'
    },
    {
        'user': 'person3',
        'lastmessage': 'oh nooooooooooo whyyyyy',
        'lastsent': 'Jan. 1, 2020'
    },
    {
        'user': 'person3',
        'lastmessage': 'oh nooooooooooo whyyyyy',
        'lastsent': 'Jan. 1, 2020'
    },
    {
        'user': 'person3',
        'lastmessage': 'oh nooooooooooo whyyyyy',
        'lastsent': 'Jan. 1, 2020'
    },
    {
        'user': 'person3',
        'lastmessage': 'oh nooooooooooo whyyyyy',
        'lastsent': 'Jan. 1, 2020'
    }
]

# logs = {
#     'person1':
# }


def home(request):
    context = {
        'messages': messages
    }
    return render(request, 'message/chatlog.html', context)
