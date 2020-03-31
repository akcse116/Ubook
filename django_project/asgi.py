"""
ASGI config for django_project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')

application = get_asgi_application()


# async def application(scope, receive, send):
#     if scope['type'] == 'http':
#         # Let Django handle HTTP requests
#         await django_application(scope, receive, send)
#     elif scope['type'] == 'websocket':
#         # We'll handle Websocket connections here
#         await websocket_application(scope, receive, send)
#     else:
#         raise NotImplementedError(f"Unknown scope type {scope['type']}")
#
#
# async def websocket_application(scope, receive, send):
#     while True:
#         event = await receive()
#
#         if event['type'] == 'websocket.connect':
#             await send({
#                 'type': 'websocket.accept'
#             })
#
#         if event['type'] == 'websocket.disconnect':
#             break
#
#         if event['type'] == 'websocket.receive':
#             if event['text'] == 'ping':
#                 await send({
#                     'type': 'websocket.send',
#                     'text': 'pong!'
#                 })
