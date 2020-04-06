from django.shortcuts import render
from django.http import HttpResponse
from .models import Post
from django.contrib.auth.models import User
from django.conf import settings



def home(request):
    if request.method == 'POST':
        body = request.POST['post-body']
        if request.FILES:
            media = request.FILES['post-media']
            storage_file_path = settings.MEDIA_ROOT + media.name
            file_content = media.file.read()
            with open(storage_file_path, 'wb') as file:
                file.write(file_content)
        else:
            media = None
        post = Post(title = 'title-1', content = body, media = media, author= User.objects.get(username='superuser'))      
        post.save()
        
        
        
    else:
        None

    context = {'posts': Post.objects.order_by('date_posted').reverse()}
    return render(request, 'blog/home.html', context)

