from django.urls import path
from .consumers import *

websocket_urlpatterns=[
    path('ws/<str:chatroom>/<str:username>/',VideoChatroom.as_asgi()),
    path('ws/<int:username_me>/<int:username_other>/',VideoChatroomText.as_asgi())
]