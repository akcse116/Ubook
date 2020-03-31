# chat/routing.py
from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/message/(?P<user>\w+)/$', consumers.main, {"group": "all"}),
]