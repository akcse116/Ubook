from django.shortcuts import render
from django.http import HttpResponse

posts = [
    {
    'author': 'Tiffany Tate',
    'title': 'This is my first post on UBook!',
    'content': 'Wow this is just like facebook except better!                        ',
    'date_posted':'march, 8st, 2020'
    },
    {
    'author': 'author2',
    'title': 'author2 title',
    'content': 'author2 post content                        ',
    'date_posted':'march, 1st, 2020'
    },
    {
    'author': 'author3',
    'title': 'author3 title',
    'content': 'author3 post content                        ',
    'date_posted':'march, 1st, 2020'
    },
    {
    'author': 'author4',
    'title': 'author4 title',
    'content': 'author4 post content                        ',
    'date_posted':'march, 1st, 2020'
    },
]

def home(request):
    context = {'posts':posts}
    return render(request, 'blog/home.html', context)

def feed(request):
    return HttpResponse('<h1> Blog Feed </h1>')

def write_post(request):
    return render(request, 'blog/write_post.html')