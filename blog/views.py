import random
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
            media_ID = random.randrange(1000000)
            media_type = media.name.split('.')[1]
            upload_name = 'upload_'+ str(media_ID) +'.'+ media_type
            media_name = 'http://'+ 'localhost' + ':'+ request.META['SERVER_PORT'] + settings.MEDIA_URL + upload_name 
            while Post.objects.filter(media = media_name):
                media_ID = random.randrange(1000000)
                media_type = media.name.split('.')[1]
                upload_name = 'upload_'+ str(media_ID) +'.'+ media_type
                media_name = 'http://'+ 'localhost' + ':'+ request.META['SERVER_PORT'] + settings.MEDIA_URL + upload_name  
            storage_file_path = settings.MEDIA_ROOT + '/'+ upload_name
            file_content = media.file.read()
            with open(storage_file_path, 'wb') as file:
                file.write(file_content)
        # media = 'http://'+ request.META['SERVER_NAME'] + ':'+ request.META['SERVER_PORT'] + settings.MEDIA_URL + media.name
        else:
            media = None
            record = Post(title="A", content=body, media=media_name)
            record.save()
        
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

    print(request.META['HTTP_HOST'] + ':'+ request.META['SERVER_PORT'])
    print('aaaaa')

    return render(request, 'blog/home.html', context)

