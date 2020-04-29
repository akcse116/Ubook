from django.shortcuts import render
from django.http import HttpResponse

messages = [
    {
        'user': 'person1',
        'lastmessage': 'hi',
        'lastsent': 'Jan. 1, 2020'
    },
]

test = open('message/templates/message/person0___person2.txt', 'r').read()

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

# get user's token from request's cookie, search it up on db
# get first message where this person is either sender or receiver, display their log
# get other messages where this person is either sender or receiver, put the other user in the messages list
