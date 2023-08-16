import cv2, base64, json
import numpy as np
from django.shortcuts import get_object_or_404
from asgiref.sync import sync_to_async
from chat.helper import get_user_from_scope
from channels.generic.websocket import AsyncWebsocketConsumer

from .models import Live

# consumer
class LiveVideoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = await sync_to_async(get_user_from_scope)(self.scope)    
        print(self.user)
        
        if self.user:
            self.live_id = self.scope["url_route"]["kwargs"]["live_id"]
            
            print(self.live_id)
            self.live = await sync_to_async(get_object_or_404)(Live, pk=self.live_id)
            self.GROUP_NAME = f'live-{self.live_id}'
            # Join room group
            await self.channel_layer.group_add(
                self.GROUP_NAME, self.channel_name
            )       
            await self.accept()
            # self.cap = cv2.VideoCapture(0)
        else:
            await self.close()

    async def disconnect(self, close_code):
        # self.live.delete()
        # Leave room group
        await self.channel_layer.group_discard(self.GROUP_NAME, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        streamer_id = await sync_to_async(lambda: self.live.streamer.id)() 
        # if self.user.id == streamer_id:
        #     print('streamer')
        if bytes_data:
            print('bytes')
        if text_data:
            print('text')
        try:
            data = json.loads(text_data)
            print(data)
            await self.channel_layer.group_send(
                self.GROUP_NAME,
                {
                    'type': 'image_data',
                    'content':  data
                }
            )
        except Exception as e:
            print("Error:", e)
            
    # Send message to WebSocket
    async def image_data(self, event):
        try:
            await self.send(text_data=json.dumps(event['content']))
        except Exception as e:
            print('Exception in consumer: ', e)
            
