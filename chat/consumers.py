import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Message
from .serializers import MessageSerializer
from rest_framework.renderers import JSONRenderer
from django.contrib.auth import get_user_model
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404
from channels.consumer import SyncConsumer
from django.contrib.auth.models import User
from chat.models import Thread, Message



User = get_user_model()

class RoomConsumer(WebsocketConsumer):

    def fetch_messages(self, data):
        messages = Message.objects.all()
        serializer = MessageSerializer(messages, many = True)
        jsonSerializedMessages = JSONRenderer().render(serializer.data)
        content = {
            "messages":jsonSerializedMessages
        }

        self.send_message(content)

    def new_message(self, data):
        # thread_obj = Thread.objects.get_or_create_personal_thread()
        author = data['from']
        # user = get_object_or_404(User, username = author)
        # message = Message.objects.create(sender = user, text = data['message'], thread)

        content = {
            'command':'new_message', 
            'message': data['message'], 
            'author': author
        }

        return self.send_chat_message(content)

    commands = {
        'fetch_messages':fetch_messages, 
        'new_message':new_message
    }



    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        print("hey")
        data = json.loads(text_data)
        command = data['command']
        self.commands[command](self, data)
        # send_chat_message(message)


    def send_chat_message(self, data):



        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chatMessage', #this is the name 
                                        #of the callback function 
                                        #that then sends the message
                                        #to the websocket
                'data':data
            }
        )


    def send_message(self, message):
        self.send(text_data = json.dumps(message))

    # Receive message from room group
    def chatMessage(self, event):
        data = event['data']

        # Send message to WebSocket
        self.send(text_data=json.dumps(data))

class ChatConsumer(SyncConsumer):
    def websocket_connect(self, event):
        me = self.scope['user']
        otherUser = self.scope['url_route']['kwargs']['username']
        otherUser = User.objects.get(username = otherUser)
        self.thread_obj = Thread.objects.get_or_create_personal_thread(me, otherUser)
         
        self.room_name = f'personal_thread{self.thread_obj.id}'
        async_to_sync(self.channel_layer.group_add)(self.room_name, self.channel_name)

        self.send({
            "type":"websocket.accept"
        })

        print(f'[self.channel_name] - you are connected')
    
    def websocket_disconnect(self, event):
        async_to_sync(self.channel_layer.group_discard)(self.room_name, self.channel_name)

    def websocket_receive(self, event):
        print(f"[{self.channel_name}] - Received message - {event['text']}")

        text = json.loads(event.get('text'))
        msg = json.dumps({
            'text':text, 
            'username': self.scope['user'].username
        })
        self.store_message(text)



        async_to_sync(self.channel_layer.group_send)(
            self.room_name, {
                'type':'websocket.message', 
                'text': msg
            })

    def websocket_message(self, event):
        print(f"[{self.channel_name}] - Messagge sent - {event['text']}")
        
        self.send({
            'type':'websocket.send', 
            'text':event.get('text')
        }) 
    
    def store_message(self, text):
        Message.objects.create(
            thread = self.thread_obj, 
            sender = self.scope['user'],
            text = text
        )