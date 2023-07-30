import json, re, base64, os, binascii
from django.conf import settings
from django.shortcuts import get_object_or_404
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from .models import Chat, Message
from .helper import get_user_from_scope, json_list, message_to_json, get_url_from_scope

# consumers
class ChatConsumer(AsyncWebsocketConsumer): 
           
    async def new_message(self, data):
        chat_object = await sync_to_async(get_object_or_404)(Chat, id=self.chat_id)
        if data['message_type'] == 'text':
            # Regular text message            
            message = await sync_to_async(Message.objects.create)(
                chat=chat_object, author=self.user, type='text', text=data['text']
            )
        elif data['message_type'] == 'image':
            # Image message
            message = await sync_to_async(Message.objects.create)(
                chat=chat_object, author=self.user, type='image', image=data['image']
            )
        elif data['message_type'] == 'voice_record':
            # Voice record message
            voice_record_data = data['voice_record']
            if not voice_record_data:
                print('no voice record')
                return
            
            filename = os.path.join(settings.MEDIA_ROOT, 'voice_records', f'{self.chat_id}_{self.user.id}.wav')

            # Save the voice record data to the appropriate file
            with open(filename, 'wb') as f:
                f.write(binascii.a2b_base64(voice_record_data))

            # Create the Message object with the voice record
            message = await sync_to_async(Message.objects.create)(
                chat=chat_object, author=self.user, type='voice_record', voice_record=filename
            )
        else:
            print('Invalid message format')
            return

        reply_id = data['reply_id']
        if reply_id != 0:
            reply_to_message = await sync_to_async(get_object_or_404)(Message, id=reply_id)
            message.reply = reply_to_message
            await database_sync_to_async(message.save)()
        
        content = {
            'command': 'new_message',
            'message': message_to_json(message, self.url)
        }
        await self.send_chat_message(content)
        
    async def fetch_messages(self, data):
        # fetch messages from database
        chat_object = await database_sync_to_async(Chat.objects.get)(pk=self.chat_id)
        messages = await database_sync_to_async(Message.objects.filter)(chat=chat_object)
        messages = messages[:10]  # get the first 10 messages
        content = {
            'command': 'messages',
            'messages': await json_list(messages, self.url)
        }
        await self.send_messages(content)
    
    async def add_reaction(self, data):
        message_id = data['message_id']
        reaction_id = data['reaction_id']

        if message_id is None or reaction_id is None:
            print('message_id and reaction_id required')
            return

        message = await sync_to_async(get_object_or_404)(Message, id=message_id)
        message.reaction = reaction_id
        await database_sync_to_async(message.save)()

        content = {
            'command': 'update_reaction',
            'message_id': message_id,
            'reaction_id': reaction_id,
        }
        await self.send_chat_message(content)
    
    commands = {
        'fetch_messages' : fetch_messages,
        'new_message' : new_message,
        'add_reaction' : add_reaction
    }
     
    async def connect(self):
        self.url = get_url_from_scope(self.scope)
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
            