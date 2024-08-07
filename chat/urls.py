from django.contrib import admin
from django.urls import path,include
from .views import chat,get_or_creteroom,create_group,chatroom_leave,chat_file,chathome

urlpatterns = [
    path('chathome/<str:username>/',chathome,name='chathome'),
    path('chat/room/<str:chatroom>/',chat,name='chatroom'),
    path('chat/<str:username>/',get_or_creteroom,name='start-chat'),
    path('new_groupchat/',create_group,name='new_group'),
    path('chat/leave/<str:chatroom>',chatroom_leave,name='leave_group'),
    path('chat/file/<str:chatroom>',chat_file,name="chat-file")
]