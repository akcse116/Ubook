from django.shortcuts import render
from django.http import HttpResponse
from .models import Post
from user_profile.models import User
from django.conf import settings



def home(request):
    if request.method == 'POST':
        body = request.POST['post-body']
        if request.FILES:
            media = request.FILES['post-media']
            storage_file_path = settings.MEDIA_ROOT + '/'+ media.name
            print(storage_file_path)
            file_content = media.file.read()
            with open(storage_file_path, 'wb') as file:
                file.write(file_content)
            media = 'http://'+ 'localhost' + ':'+ request.META['SERVER_PORT'] + settings.MEDIA_URL + media.name
            # media = 'http://'+ request.META['SERVER_NAME'] + ':'+ request.META['SERVER_PORT'] + settings.MEDIA_URL + media.name
        else:
            media = None
        post = Post(title = 'title-1', content = body, media = media, author= User.objects.get(username='admin'))
        post.save()
        
    else:
        None

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

    return render(request, 'blog/home.html', context)

