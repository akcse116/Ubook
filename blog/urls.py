from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name = 'blog-home'),
    path('feed/', views.feed, name = 'blog-feed'),
    path('write/', views.write_post, name = 'blog-write'),
]
