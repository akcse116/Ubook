from django.shortcuts import render
from django.http import HttpResponse
from .models import Post


def home(request):
    context = {'posts': Post.objects.all()}
    return render(request, 'blog/home.html', context)


def feed(request):
    return HttpResponse('<h1> Blog Feed </h1>')


def write_post(request):
    return render(request, 'blog/write_post.html')