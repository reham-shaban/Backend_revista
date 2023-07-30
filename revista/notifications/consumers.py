from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

from accounts.models import CustomUser
from chat.helper import get_user_from_scope
import re, json

# Consumers
class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):     
        self.user = await sync_to_async(get_user_from_scope)(self.scope)    
        print(self.user)
      
        if self.user:
            self.GROUP_NAME = f'user-notifications-{self.user.id}'
            # Add the consumer to the user notifications group
            await self.channel_layer.group_add(self.GROUP_NAME, self.channel_name)
            # Accept the WebSocket connection
            await self.accept()           
        else:
            await self.close()

    async def disconnect(self, close_code):
       # Remove the consumer from the user notifications group
        await self.channel_layer.group_discard(self.GROUP_NAME, self.channel_name)

    async def notification(self, event):
        try:
            await self.send(text_data = json.dumps({'text': event['text']}) )                       
        except Exception as e:
            print('Exception in consumer: ', e)
        