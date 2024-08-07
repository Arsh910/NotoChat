from django.template.loader import render_to_string
from channels.generic.websocket import WebsocketConsumer,AsyncWebsocketConsumer,async_to_sync
import json
from User_profile.models import Profile
import random

class VideoChatroom(WebsocketConsumer):
    def connect(self):
        self.user = self.scope['user']
        self.videoroom_name = self.scope['url_route']['kwargs']['username']
        self.videoroom_name_sanitized = self.videoroom_name.replace(' ', '_')

        self.accept()
    
    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.videoroom_name_sanitized, self.channel_name
        )
    
    # def receive(self, text_data=None, bytes_data=None):
    #     text_data_dict = json.loads(text_data)
    #     command = text_data_dict.get('command')  
    #     room = text_data_dict.get('room')   
        
    #     if command == "join_room":
    #         async_to_sync(self.channel_layer.group_add)(
    #             room,self.channel_name
    #         )


    #     elif command == "cancel":
            
    #         event = {
    #             'type':'cancel_message_handler',
    #         }

    #         async_to_sync(self.channel_layer.group_send)(
    #             room,event
    #     )

    #     elif command == "join":
            
    #         event = {
    #             'type':'join_message_handler',
    #         }

    #         async_to_sync(self.channel_layer.group_send)(
    #             room,event
    #         )

    #     elif command == 'offer':
    
    #         event = {
    #             'type':'offer_message_handler',
    #             'offer': text_data_dict.get('offer'),
    #             'other': text_data_dict.get('other'),
    #         }
            
    #         async_to_sync(self.channel_layer.group_send)(
    #             room,event
    #         )

    #     elif command == 'answer':

    #         event = {
    #             'type':'answer_message_handler',
    #             'answer': text_data_dict.get('answer'),
    #         }
            
    #         async_to_sync(self.channel_layer.group_send)(
    #             room,event
    #         )

    #     elif command == 'candidate':

    #         event = {
    #             'type':'candidate_message_handler',
    #             'candidate': text_data_dict.get('candidate'),
    #             # 'is_created': text_data_dict.get('is_created')
    #         }
            
    #         async_to_sync(self.channel_layer.group_send)(
    #             room,event
    #         )
        


    # def join_message_handler(self,event):
    #     self.send(json.dumps({
    #         'command':'join'

    #     }))

    # def offer_message_handler(self,event):     
    #     print(event['other'])
    #     self.send(json.dumps({
    #         'command':'offer',
    #         'offer':event['offer'],
    #         'other': event['other'],
    #     }))
    
    # def answer_message_handler(self,event):
    #     self.send(json.dumps({
    #         'command':'answer',
    #         'answer' : event['answer'],
    #     }))

    # def candidate_message_handler(self,event):
    #     self.send(json.dumps({
    #         'command':'candidate',
    #         'candidate' : event['candidate'],
    #         # 'is_created': event['is_created'],
    #     }))
    
    # def cancel_message_handler(self,event):
    #     self.send(json.dumps({
    #         'command':'cancel',
    #     }))

    def receive(self, text_data=None, bytes_data=None):
               
        text_data_dict = json.loads(text_data)
        command = text_data_dict.get('command')
        room = text_data_dict.get('room')

        if command == "join_room":
            async_to_sync(self.channel_layer.group_add)(
                room,self.channel_name
            )

        elif command == 'b_offer':
            my_id = text_data_dict.get('my_id')
            selected = text_data_dict.get('selected')
            offer = text_data_dict.get('offer')
    
            print(f'{my_id} is me')
            print(f'{selected} is other')

            event = {
                'type':'b_offer_message_handler',
                'my_id':my_id,
                'room':room,
                'selected':selected,
                'offer': offer
            }

            async_to_sync(self.channel_layer.group_send)(
                room,event
            )
        
        elif command == 'answer':
            answer = text_data_dict.get('answer')
            my_id = text_data_dict.get('my_id')
            selected = text_data_dict.get('selected')
            event = {
                'type':'answer_message_handler',
                'room':room,
                'answer': answer,
                'selected':selected,
                'my_id':my_id
            }

            async_to_sync(self.channel_layer.group_send)(
                room,event
            )
            
        elif command == 'candidate':
            room = text_data_dict.get('room')
            event = {
                'type':'candidate_message_handler',
                'candidate': text_data_dict.get('candidate'),
            }
            
            async_to_sync(self.channel_layer.group_send)(
                room,event
            )

        elif command == "cancel":
            room = text_data_dict.get('room')
            other = text_data_dict.get('to')
            me = text_data_dict.get('from')
            event = {
                'type':'cancel_message_handler',
                'other':other,
                'me':me
            }

            async_to_sync(self.channel_layer.group_send)(
                room,event
            )


    

    def b_offer_message_handler(self,event):
        self.send(json.dumps({
            'command':'b_offer',
            'my_id': event['my_id'],
            'room':event['room'],
            'selected':event['selected'],
            'offer':event['offer']            
        }))

    def answer_message_handler(self,event):
        self.send(json.dumps({
            'command':'answer',
            'answer':event['answer'],
            'my_id': event['my_id'],
            'room':event['room'],
            'selected':event['selected']           
        }))

    def candidate_message_handler(self,event):
        # print(event['candidate'])
        self.send(json.dumps({
            'command':'candidate',
            'candidate' : event['candidate'],
        }))

    def cancel_message_handler(self,event):
        print(f"{event['other']} , {event['me']} , other , me")
        self.send(json.dumps({
            'command':'cancel',
            'other':event['other'],
            'me':event['me']
        }))


class VideoChatroomText(WebsocketConsumer):
    
    def connect(self):
        self.user = self.scope['user']
        self.name_me = self.scope['url_route']['kwargs']['username_me']
        self.name_other = self.scope['url_route']['kwargs']['username_from']
        self.name = 'omegle'
        self.accept()


    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.name, self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):
        return super().receive(text_data, bytes_data)