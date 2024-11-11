from django.urls import path

from .consumers import *


web_socket_patterns=[
    path('ws/chatroom/<chatroom_name>',ChatroomConsumer.as_asgi())
]