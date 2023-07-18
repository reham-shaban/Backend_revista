import json, re
from django.shortcuts import get_object_or_404
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from .models import Chat, Message
from .helper import get_user_from_scope, json_list, message_to_json

# consumers
class ChatConsumer(AsyncWebsocketConsumer): 
    
    async def new_message(self, data):
        # save message to database
        chat_object = await sync_to_async(get_object_or_404)(Chat, id=self.chat_id)
        message = await sync_to_async(Message.objects.create)(chat=chat_object, author=self.user, text=data['text'])
        # send message
        content = {
            'command': 'new_message',
            'message': message_to_json(message)
        }
        await self.send_chat_message(content)
           
    async def fetch_messages(self, data):
        # fetch messages from database
        chat_object = await database_sync_to_async(Chat.objects.get)(pk=self.chat_id)
        messages = await database_sync_to_async(Message.objects.filter)(chat=chat_object)
        messages = messages[:10]  # get the first 10 messages
        content = {
            'command': 'messages',
            'messages': await json_list(messages)
        }
        await self.send_messages(content)
    
    commands = {
        'fetch_messages' : fetch_messages,
        'new_message' : new_message
    }
                     
    async def connect(self):     
        self.user = await sync_to_async(get_user_from_scope)(self.scope)    
        print(self.user)
        
        if self.user:
            self.chat_id = self.scope["url_route"]["kwargs"]["chat_id"]
            self.chat_group_name = "chat_%s" % self.chat_id
            # Join room group
            await self.channel_layer.group_add(
                self.chat_group_name, self.channel_name
            )       
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.chat_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        await self.commands[data['command']](self, data)
        
    # Send messages to WebSocket
    async def send_messages(self, content):
        try:
            await self.send(text_data=json.dumps(content))
        except Exception as e:
            print('Exception in consumer: ', e)
    
    # Send message to room group   
    async def send_chat_message(self, content):
        await self.channel_layer.group_send(
            self.chat_group_name, 
            {
                'type': 'chat_message',
                'content': content
            }
        )

    # Send message to WebSocket
    async def chat_message(self, event):
        try:
            await self.send(text_data=json.dumps(event['content']))
        except Exception as e:
            print('Exception in consumer: ', e)
            