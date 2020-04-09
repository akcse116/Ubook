from django.shortcuts import render
from django.http import HttpResponse
from blog.models import Post

def home(request):

    posts = Post.objects.filter(parent_id=None).order_by('date_posted').reverse()
    context = {
        'posts': []
    }

    for i in posts:
        comments = Post.objects.filter(parent_id=i.id).order_by('date_posted')
        if comments:
            context['posts'].append([i, comments])
        else:
            context['posts'].append([i, []])

    return render(request, 'user_profile/profile.html', context)
