from . import views
from . import consumers
from django.urls import path, re_path

urlpatterns = [

    path('', views.home, name='blog-home'),
    re_path(r'createpost/', consumers.createPost),
    re_path(r'addfriend/(?P<username>\w+)/(?P<friend>\w+)/$', views.add_friend),
    re_path(r'removefriend/(?P<username>\w+)/(?P<friend>\w+)/$', views.remove_friend)
]
