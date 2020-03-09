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

test = open('message/templates/message/person0:person2.txt', 'r').read()

logs = {
    ('person0', 'person2'): [i.split(": ", 1) for i in test.splitlines()]
}

user = 'person0'


def home(request):
    context = {
        'messages': messages,
        'log': logs[('person0', 'person2')],
        'user': user
    }
    return render(request, 'message/chatlog.html', context)
