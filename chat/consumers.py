from django.template.loader import render_to_string
from channels.generic.websocket import WebsocketConsumer,AsyncWebsocketConsumer
from django.shortcuts import get_object_or_404
from .models import ChatGroup , GroupMessage
import json
from asgiref.sync import async_to_sync

class ChatroomConsumer(WebsocketConsumer):
    
    def connect(self):
        self.user = self.scope['user']
        self.chatroom_name = self.scope['url_route']['kwargs']['chatroom_name']
        
        print(f"connect {self.user}")

        # Replace spaces with underscores in the chatroom name
        self.chatroom_name_sanitized = self.chatroom_name.replace(' ', '_')
        # print(self.chatroom_name_sanitized)

        self.chatroom = get_object_or_404(ChatGroup, group_name=str(self.chatroom_name))
        
        async_to_sync(self.channel_layer.group_add)(
            self.chatroom_name_sanitized, self.channel_name
        )

        # add and update users
        if self.user not in self.chatroom.user_online.all():
            self.chatroom.user_online.add(self.user)
            self.update_online_count()

        self.accept()

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.chatroom_name_sanitized , self.channel_name
        )
        
        if self.user in self.chatroom.user_online.all():
            self.chatroom.user_online.remove(self.user)
            self.update_online_count()

 

    def receive(self, text_data=None):
        text_data_dict = json.loads(text_data)
        message = text_data_dict.get('message')

        print(f"recieve from {self.user}")

        data = GroupMessage.objects.create(
           group = self.chatroom,
           author = self.user,
           body = message,
        )
        data.save()
        context = {
            "data":{
                'body':message,
                'author':self.user,
                'created':data.created
            }
        }
        
        event = {
            'type':'message_handler',
            'message_id' : data.id,
        }

        async_to_sync(self.channel_layer.group_send)(
            self.chatroom_name_sanitized , event
        )

    def message_handler(self,event):
        message_id = event['message_id']
        message = GroupMessage.objects.get(id = message_id)      
        context = {
            "data":{
                'body':message.body,
                'author':message.author,
                'file':message.file,
                'created':message.created,
            },
            "user":self.user
        }
        html  = render_to_string('chat_message_p.html',context)
        self.send(text_data=html)

    def update_online_count(self):
        online_count = self.chatroom.user_online.count()-1
        event ={
            'type':'online_count_handler',
            'online_count':online_count
        }
        
        async_to_sync(self.channel_layer.group_send)(self.chatroom_name_sanitized,event)

    def online_count_handler(self,event):
        online_count = event['online_count']
        html = render_to_string("online_count.html",{"count":online_count})
        self.send(text_data=html)





    
