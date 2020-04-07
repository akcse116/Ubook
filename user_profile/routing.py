# profile routing for websocket exchange
from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/profile/(?P<chat>\w+)/$', consumers.main, {"profile": "post"}),
]