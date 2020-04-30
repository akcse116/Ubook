from . import views
from django.urls import path, re_path

urlpatterns = [
    path('', views.home, name='message-home'),
    re_path(r'room/(?P<user>\w+)/$', views.switchconvo)
]