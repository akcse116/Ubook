from . import views
from . import consumers
from django.urls import path, re_path

urlpatterns = [

    path('', views.home, name='blog-home'),
    re_path(r'createpost/', consumers.createPost)
   
]
